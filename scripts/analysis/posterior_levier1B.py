#!/usr/bin/env python3
"""
posterior_levier1B.py — Levier #1B posterior analysis
======================================================
Reads 4 Cobaya chain files (eci_levier1B.{1,2,3,4}.txt), drops a configurable
burn-in fraction, and produces:

  <outdir>/triangle_cosmo.pdf      — triangle plot, 10 cosmological params
  <outdir>/marginals_cosmo.pdf     — 1-D marginals for 10 cosmo params
  <outdir>/marginals_nuisance.pdf  — 1-D marginals for 9 Planck nuisance params (collapsed)
  <outdir>/xi_chi_comparison.pdf   — side-by-side xi_chi: v5 / v50plusS8 / levier1B
  <outdir>/summary.tex             — LaTeX table: mean, 68 CI, 95 CI, prior comparison
  <outdir>/summary.md              — Markdown summary + discriminator section

Usage:
  python3 scripts/analysis/posterior_levier1B.py \\
      --chain-prefix /root/crossed-cosmos/eci_levier1B \\
      --burnin 0.3 \\
      --outdir notes/posterior_levier1B_<DATE>

Options:
  --chain-prefix PATH   Prefix for levier1B chains (default: ./eci_levier1B)
  --v5-prefix PATH      Prefix for v5 chains (optional; enables comparison plot)
  --v50s8-prefix PATH   Prefix for v50plusS8 chains (optional; enables comparison)
  --burnin FLOAT        Burn-in fraction (default: 0.30)
  --outdir PATH         Output directory (default: notes/posterior_levier1B_<DATE>)
  --nchains INT         Number of chain files (default: 4)
  --no-plots            Skip all plots; write only summary files
  --max-samples INT     Cap post-burnin samples per chain (for test runs)

Packages used: numpy, scipy, matplotlib, getdist.
Optional (gracefully degraded): anesthetic, chainconsumer, corner, mpmath.

The script does NOT run any Boltzmann code or fetch data from the internet.
"""

from __future__ import annotations

import argparse
import os
import sys
import textwrap
from datetime import date
from pathlib import Path

import numpy as np

# ---------------------------------------------------------------------------
# Repo-root detection
# ---------------------------------------------------------------------------

def _find_repo_root(start: Path) -> Path:
    for parent in [start, *start.parents]:
        if (parent / ".git").exists():
            return parent
    return Path.cwd()


_HERE = Path(__file__).resolve().parent
_REPO_ROOT = _find_repo_root(_HERE)

# ---------------------------------------------------------------------------
# Parameter metadata — 10 cosmological + 9 Planck nuisance
# ---------------------------------------------------------------------------

# Cosmological parameters sampled in Levier #1B
COSMO_PARAMS = [
    "H0", "omega_b", "omega_cdm", "n_s",
    "logA", "tau_reio",
    "w0_fld", "wa_fld", "xi_chi", "chi_initial",
]

# Planck nuisance parameters (9); names must match Cobaya column headers
NUISANCE_PARAMS = [
    "A_planck",
    "amp_143", "amp_217", "amp_143x217",
    "n_143", "n_217", "n_143x217",
    "calTE", "calEE",
]

ALL_PARAMS = COSMO_PARAMS + NUISANCE_PARAMS

# (latex_label, prior_lo, prior_hi, prior_centre_or_None)
PARAM_META: dict[str, tuple] = {
    # Cosmological
    "H0":          (r"$H_0$ [km/s/Mpc]",              55.0,  85.0,  67.4),
    "omega_b":     (r"$\Omega_b h^2$",                  0.017, 0.027, 0.02237),
    "omega_cdm":   (r"$\Omega_c h^2$",                  0.09,  0.15,  0.12),
    "n_s":         (r"$n_s$",                            0.9,   1.05,  0.9649),
    "logA":        (r"$\ln(10^{10}A_s)$",               2.5,   3.5,   3.044),
    "tau_reio":    (r"$\tau_\mathrm{reio}$",             0.01,  0.15,  0.054),
    "w0_fld":      (r"$w_0$",                           -1.2,  -0.5,  -1.0),
    "wa_fld":      (r"$w_a$",                           -2.0,   0.0,   0.0),
    "xi_chi":      (r"$\xi_\chi$",                      -0.1,   0.1,   0.0),
    "chi_initial": (r"$\chi_\mathrm{ini}$",              0.05,  0.2,   0.1),
    # Planck nuisance (priors are Gaussian in cobaya; we use approximate ranges here)
    "A_planck":       (r"$A_\mathrm{Planck}$",           0.9,   1.1,   1.0),
    "amp_143":        (r"$A_{143}$",                     0.0,   2.0,   1.0),
    "amp_217":        (r"$A_{217}$",                     0.0,   2.0,   1.0),
    "amp_143x217":    (r"$A_{143\times217}$",            0.0,   2.0,   1.0),
    "n_143":          (r"$n_{143}$",                    -1.0,   1.0,   0.0),
    "n_217":          (r"$n_{217}$",                    -1.0,   1.0,   0.0),
    "n_143x217":      (r"$n_{143\times217}$",           -1.0,   1.0,   0.0),
    "calTE":          (r"$\mathrm{cal}_{TE}$",           0.9,   1.1,   1.0),
    "calEE":          (r"$\mathrm{cal}_{EE}$",           0.9,   1.1,   1.0),
}

# Cassini wall — Bertotti-Iess-Tortora 2003 bound, chi_0/M_P = 0.1 fiducial
# |xi_chi| * (chi_0/M_P)^2 < 6e-6  =>  |xi_chi| < 6e-4 at chi_0/M_P=0.1
# For the Cobaya sampler the hard wall is already enforced in the likelihood;
# we track it here for annotation on plots.
CASSINI_WALL_XI = 6e-4   # prior narrow wall enforced by eci_kids_s8.py

# Conservative "visible" boundary on xi_chi plots (prior width)
XI_CHI_PRIOR_LO = -0.1
XI_CHI_PRIOR_HI =  0.1

# SH0ES anchor (Riess+2022)
SHOES_H0_CENTRAL = 73.04
SHOES_H0_SIGMA   = 1.04

# KiDS-1000 S8 prior (used in v50plusS8 and levier1B)
KIDS_S8_CENTRAL = 0.766
KIDS_S8_SIGMA   = 0.020

# Planck 2018 S8 estimate (TT,TE,EE+lowE+lensing)
PLANCK_S8_CENTRAL = 0.830
PLANCK_S8_SIGMA   = 0.013

# Wolf+2025 Bayes factor (arXiv:2504.07679)
WOLF2025_LN_BAYES     = 7.34
WOLF2025_LN_BAYES_ERR = 0.6

# v5 reference values for xi_chi (from notes/posterior_v5_2026-05-02/summary.md)
V5_XI_MEAN   = -0.00020
V5_XI_LO68   = -0.06747
V5_XI_HI68   =  0.06570
V5_XI_LO95   = -0.09475
V5_XI_HI95   =  0.09565

# v50plusS8 reference values (from notes/posterior_v50plusS8_vs_v5_2026-05-02.md)
V50S8_XI_MEAN  =  0.0005
V50S8_XI_LO68  = -0.067
V50S8_XI_HI68  =  0.068

# ---------------------------------------------------------------------------
# Chain I/O  (adapted from posterior_v5.py)
# ---------------------------------------------------------------------------

def read_cobaya_chains(
    prefix: str,
    n_chains: int = 4,
    burnin: float = 0.30,
    max_samples: int | None = None,
    expected_params: list[str] | None = None,
) -> dict:
    """
    Read Cobaya plain-text chain files <prefix>.{1..n_chains}.txt.

    Returns a dict with:
        'samples'     : np.ndarray (N_total, n_cols)
        'weights'     : np.ndarray (N_total,)
        'logpost'     : np.ndarray (N_total,)
        'col_names'   : list[str]   (parameter names, no weight/logpost)
        'n_per_chain' : list[int]
        'chain_files' : list[str]
    """
    all_samples, all_weights, all_logpost = [], [], []
    n_per_chain, chain_files = [], []
    col_names: list[str] | None = None

    for ci in range(1, n_chains + 1):
        fpath = f"{prefix}.{ci}.txt"
        chain_files.append(fpath)
        if not os.path.exists(fpath):
            print(f"  [WARNING] chain file not found: {fpath}", file=sys.stderr)
            continue
        try:
            with open(fpath) as fh:
                header_line = fh.readline().lstrip("#").strip()
            this_cols = header_line.split()
            if col_names is None:
                col_names = this_cols
            elif this_cols != col_names:
                print(f"  [WARNING] column mismatch in {fpath}; skipping",
                      file=sys.stderr)
                continue
            data = np.loadtxt(fpath)
        except Exception as exc:
            print(f"  [ERROR] failed to read {fpath}: {exc}", file=sys.stderr)
            continue

        if data.ndim == 1:
            data = data[None, :]
        if data.shape[0] == 0:
            print(f"  [WARNING] empty chain: {fpath}", file=sys.stderr)
            continue

        n_drop = int(np.ceil(burnin * data.shape[0]))
        data = data[n_drop:]
        if max_samples is not None and data.shape[0] > max_samples:
            data = data[:max_samples]

        all_weights.append(data[:, 0])
        all_logpost.append(data[:, 1])
        all_samples.append(data[:, 2:])
        n_per_chain.append(data.shape[0])
        print(f"  chain {ci}: {data.shape[0]} post-burnin rows from {fpath}")

    if not all_samples:
        raise RuntimeError(
            f"No chain files could be read with prefix '{prefix}'. "
            "Check the path and that the chains have run."
        )

    col_names_params = col_names[2:] if col_names else []

    if expected_params:
        missing = [p for p in expected_params if p not in col_names_params]
        if missing:
            print(f"  [WARNING] expected params not in columns: {missing}",
                  file=sys.stderr)
            print(f"  Available: {col_names_params}", file=sys.stderr)

    return dict(
        samples=np.concatenate(all_samples, axis=0),
        weights=np.concatenate(all_weights, axis=0),
        logpost=np.concatenate(all_logpost, axis=0),
        col_names=col_names_params,
        n_per_chain=n_per_chain,
        chain_files=chain_files,
    )


def extract_param(chain: dict, name: str) -> np.ndarray | None:
    try:
        idx = chain["col_names"].index(name)
    except ValueError:
        return None
    return chain["samples"][:, idx]


# ---------------------------------------------------------------------------
# Statistics
# ---------------------------------------------------------------------------

def weighted_quantile(values: np.ndarray, quantiles: list[float],
                      weights: np.ndarray) -> np.ndarray:
    sorter = np.argsort(values)
    v = values[sorter]
    w = weights[sorter]
    cdf = np.cumsum(w) / np.sum(w)
    return np.array([v[np.searchsorted(cdf, q)] for q in quantiles])


def weighted_mean(values: np.ndarray, weights: np.ndarray) -> float:
    return float(np.average(values, weights=weights))


def weighted_std(values: np.ndarray, weights: np.ndarray) -> float:
    mu = weighted_mean(values, weights)
    return float(np.sqrt(np.average((values - mu) ** 2, weights=weights)))


def effective_sample_size(values: np.ndarray, weights: np.ndarray) -> float:
    return float(np.sum(weights) ** 2 / np.sum(weights ** 2))


def compute_stats(chain: dict, param_list: list[str]) -> dict[str, dict | None]:
    w = chain["weights"]
    stats: dict[str, dict | None] = {}
    for name in param_list:
        arr = extract_param(chain, name)
        if arr is None:
            stats[name] = None
            continue
        q = weighted_quantile(arr, [0.025, 0.16, 0.5, 0.84, 0.975], w)
        stats[name] = dict(
            mean=weighted_mean(arr, w),
            std=weighted_std(arr, w),
            lo95=q[0], lo68=q[1], median=q[2], hi68=q[3], hi95=q[4],
            ess=effective_sample_size(arr, w),
        )
    return stats


def prior_dominated_score(values: np.ndarray, weights: np.ndarray,
                           prior_lo: float, prior_hi: float,
                           n_bins: int = 30) -> float:
    """Return fraction in [0,1]; near 0 = prior-dominated, near 1 = informative."""
    bins = np.linspace(prior_lo, prior_hi, n_bins + 1)
    hist_w, _ = np.histogram(values, bins=bins, weights=weights)
    hist_w = hist_w / (hist_w.sum() + 1e-300)
    uniform = np.ones(n_bins) / n_bins
    eps = 1e-12
    chi2 = np.sum((hist_w - uniform) ** 2 / (uniform + eps))
    chi2_max = (1.0 - 1.0 / n_bins) ** 2 / (1.0 / n_bins)
    return float(min(chi2 / chi2_max, 1.0))


# ---------------------------------------------------------------------------
# Savage-Dickey Bayes factor for xi_chi = 0
# ---------------------------------------------------------------------------

def savage_dickey_bayes_factor(
    xi_arr: np.ndarray,
    weights: np.ndarray,
    prior_lo: float = XI_CHI_PRIOR_LO,
    prior_hi: float = XI_CHI_PRIOR_HI,
    bandwidth_factor: float = 0.15,
) -> tuple[float, float, str]:
    """
    Estimate the Savage-Dickey density ratio at xi_chi = 0.

    Bayes factor B_10 (NMC vs LCDM, where LCDM = xi_chi fixed at 0):
        B_10 = pi(xi_chi=0) / p(xi_chi=0 | data)
    where pi is the prior density at 0 and p is the posterior density at 0.

    B_10 > 1  =>  data favour NMC (xi_chi free) over LCDM (xi_chi=0)
    B_10 < 1  =>  data favour LCDM
    log B_10 > 1  =>  weak evidence; > 3 strong; > 5 very strong (Jeffreys scale)

    Returns (log_B10, posterior_density_at_0, interpretation_string).

    Method: Gaussian KDE with Silverman bandwidth (capped at bandwidth_factor * prior_width).
    """
    prior_width = prior_hi - prior_lo
    prior_density_at_0 = 1.0 / prior_width  # uniform prior

    # Weighted KDE at xi=0 using Gaussian kernel
    w = weights / weights.sum()
    bw_silverman = 1.06 * np.sqrt(np.average((xi_arr - np.average(xi_arr, weights=w))**2,
                                              weights=w)) * len(xi_arr)**(-0.2)
    bw = min(bw_silverman, bandwidth_factor * prior_width)
    if bw < 1e-8:
        return (float("nan"), float("nan"),
                "KDE bandwidth too small; posterior may be degenerate at xi_chi=0")

    # KDE density at 0: p(0|data) = sum_i w_i * K(0 - xi_i; bw) / bw
    kernel_vals = np.exp(-0.5 * (xi_arr / bw) ** 2) / (np.sqrt(2 * np.pi) * bw)
    posterior_density_at_0 = float(np.sum(w * kernel_vals))

    if posterior_density_at_0 < 1e-30:
        return (float("inf"), posterior_density_at_0,
                "Posterior vanishes at xi_chi=0: strong evidence for NMC")

    log_B10 = float(np.log(prior_density_at_0 / posterior_density_at_0))

    # Interpretation on Jeffreys scale (log natural units)
    if log_B10 > 5.0:
        strength = "very strong evidence for NMC over LCDM"
    elif log_B10 > 3.0:
        strength = "strong evidence for NMC over LCDM"
    elif log_B10 > 1.0:
        strength = "weak/moderate evidence for NMC over LCDM"
    elif log_B10 > -1.0:
        strength = "inconclusive (no preference)"
    elif log_B10 > -3.0:
        strength = "weak/moderate evidence FOR LCDM over NMC"
    else:
        strength = "strong evidence FOR LCDM over NMC"

    note = (
        f"log B_10 (Savage-Dickey KDE, bw={bw:.4f}) = {log_B10:.2f}. "
        f"Prior density at 0: {prior_density_at_0:.2f} [1/{prior_width:.2g}]. "
        f"Posterior density at 0: {posterior_density_at_0:.4f}. "
        f"Interpretation: {strength}. "
        f"Compare to Wolf+2025 (arXiv:2504.07679): log B = {WOLF2025_LN_BAYES:.2f} "
        f"+/- {WOLF2025_LN_BAYES_ERR:.1f} (NMC vs LCDM, Planck PR4 + DR2 BAO + Pantheon+)."
    )
    return log_B10, posterior_density_at_0, note


# ---------------------------------------------------------------------------
# Honesty gate for xi_chi
# ---------------------------------------------------------------------------

def honesty_gate_xi_chi(
    xi_stats: dict,
    xi_arr: np.ndarray,
    weights: np.ndarray,
    log_B10: float,
) -> tuple[str, bool]:
    """
    Return (verdict_string, is_detected) where is_detected=True means
    xi_chi != 0 at >= 2 sigma AND posterior is not prior-dominated.

    Flags a 'Planck does not detect NMC' warning if the posterior straddles 0
    with width comparable to the Cassini-narrowed prior.
    """
    mean = xi_stats["mean"]
    std  = xi_stats["std"]
    lo68 = xi_stats["lo68"]
    hi68 = xi_stats["hi68"]
    lo95 = xi_stats["lo95"]
    hi95 = xi_stats["hi95"]

    ci68_width = hi68 - lo68
    prior_width = XI_CHI_PRIOR_HI - XI_CHI_PRIOR_LO

    # Fraction of posterior weight that straddles zero (both signs present)
    w = weights / weights.sum()
    frac_pos = float(np.sum(w[xi_arr > 0]))
    frac_neg = float(np.sum(w[xi_arr < 0]))
    straddles_zero = (frac_pos > 0.05 and frac_neg > 0.05)

    # Width relative to Cassini-narrowed prior
    # With Cassini wall ON, the effective prior width is 2 * CASSINI_WALL_XI
    cassini_prior_width = 2 * CASSINI_WALL_XI
    ratio_to_cassini = ci68_width / cassini_prior_width if cassini_prior_width > 0 else float("inf")

    # Detection criteria
    n_sigma_from_zero = abs(mean) / std if std > 1e-10 else 0.0
    ci95_excludes_zero = (lo95 > 0 or hi95 < 0)
    ci68_excludes_zero = (lo68 > 0 or hi68 < 0)

    # Honesty gate conditions
    if ci68_width > 0.8 * prior_width:
        verdict = (
            "GATE FAIL — PRIOR-DOMINATED: The 68% CI for xi_chi spans "
            f"{100*ci68_width/prior_width:.0f}% of the wide prior. "
            "Planck has NOT constrained xi_chi in this run. "
            "Do not report a detection. Check chain convergence and CLASS likelihood coupling."
        )
        detected = False
    elif straddles_zero and ratio_to_cassini > 10:
        verdict = (
            "GATE FAIL — CASSINI-WIDE AND STRADDLES ZERO: The posterior straddles 0 "
            f"with a 68% CI width {ratio_to_cassini:.0f}x the Cassini prior width. "
            "Planck does NOT detect NMC at this run's significance. "
            "This run is consistent with a null result (Scenario C)."
        )
        detected = False
    elif ci95_excludes_zero and n_sigma_from_zero >= 2.0:
        verdict = (
            f"GATE PASS — DETECTION CANDIDATE: xi_chi = {mean:.4f} +/- {std:.4f} "
            f"({n_sigma_from_zero:.1f}sigma from 0). "
            "95% CI excludes zero. Check log B_10 and triangle plot before claiming detection. "
            "Consistent with Scenario A if H_0 and S_8 tensions also reduce."
        )
        detected = True
    elif ci68_excludes_zero and n_sigma_from_zero >= 1.5:
        verdict = (
            f"GATE MARGINAL — WEAK SIGNAL: xi_chi = {mean:.4f} +/- {std:.4f} "
            f"({n_sigma_from_zero:.1f}sigma from 0). "
            "68% CI excludes zero but 95% CI does not. Treat as Scenario B (mixed). "
            "Do not claim a detection without independent validation."
        )
        detected = False
    else:
        verdict = (
            f"GATE FAIL — NULL RESULT: xi_chi = {mean:.4f} +/- {std:.4f}. "
            f"Tension with 0: {n_sigma_from_zero:.1f}sigma. "
            "Posterior is consistent with zero. Consistent with Scenario C."
        )
        detected = False

    if not np.isnan(log_B10):
        verdict += f" Savage-Dickey log B_10 = {log_B10:.2f}."

    return verdict, detected


# ---------------------------------------------------------------------------
# Discriminator tests (tension reduction)
# ---------------------------------------------------------------------------

def test_shoes_tension(stats: dict) -> str:
    s = stats.get("H0")
    if s is None:
        return "H0 not in posterior (check after run)"
    n_sigma = abs(s["mean"] - SHOES_H0_CENTRAL) / np.sqrt(
        s["std"] ** 2 + SHOES_H0_SIGMA ** 2
    )
    return (
        f"H0 = {s['mean']:.2f} +/- {s['std']:.2f} km/s/Mpc. "
        f"SH0ES: {SHOES_H0_CENTRAL} +/- {SHOES_H0_SIGMA}. "
        f"Tension: {n_sigma:.1f}sigma (in quadrature). "
        f"Planck anchor: ~67.4 km/s/Mpc. "
        f"{'H0 RETREATS toward SH0ES' if n_sigma < 3.0 else 'H0 tension NOT resolved'}."
    )


def test_w0wa_lcdm(stats: dict) -> str:
    sw0 = stats.get("w0_fld")
    swa = stats.get("wa_fld")
    if sw0 is None or swa is None:
        return "w0_fld or wa_fld not in posterior"
    n_w0 = abs(sw0["mean"] - (-1.0)) / sw0["std"]
    n_wa = abs(swa["mean"] - 0.0) / swa["std"]
    n_2d = np.sqrt(n_w0 ** 2 + n_wa ** 2)
    return (
        f"w0 = {sw0['mean']:.3f} +/- {sw0['std']:.3f} ({n_w0:.1f}sigma from -1). "
        f"wa = {swa['mean']:.3f} +/- {swa['std']:.3f} ({n_wa:.1f}sigma from 0). "
        f"Combined 2D deviation from LCDM: {n_2d:.1f}sigma (diagonal cov approx)."
    )


def estimate_s8(stats: dict) -> str:
    """
    Estimate S_8 = sigma_8 * sqrt(Omega_m/0.3) from posterior if available.
    If sigma_8 and Omega_m are not direct chain columns, note it.
    """
    # These would appear as derived parameters if saved; check for them.
    # In levier1B the chain may not store sigma_8 directly — note this.
    sigma8_s = stats.get("sigma8")
    omegam_s = stats.get("Omega_m")
    if sigma8_s is None or omegam_s is None:
        return (
            "S_8 cannot be computed directly (sigma8 and/or Omega_m not in chain columns). "
            "Re-run with `derived: [sigma8, Omega_m]` in the YAML if needed. "
            f"KiDS-1000 prior: S_8 = {KIDS_S8_CENTRAL} +/- {KIDS_S8_SIGMA}. "
            f"Planck 2018 estimate: S_8 = {PLANCK_S8_CENTRAL} +/- {PLANCK_S8_SIGMA}."
        )
    s8_mean = sigma8_s["mean"] * np.sqrt(omegam_s["mean"] / 0.3)
    kids_tension = abs(s8_mean - KIDS_S8_CENTRAL) / KIDS_S8_SIGMA
    planck_tension = abs(s8_mean - PLANCK_S8_CENTRAL) / PLANCK_S8_SIGMA
    return (
        f"S_8 ~ {s8_mean:.3f} (point estimate from marginal means; "
        "proper propagation requires derived-param samples). "
        f"KiDS tension: {kids_tension:.1f}sigma. "
        f"Planck tension: {planck_tension:.1f}sigma."
    )


def discriminator_scenario(stats: dict, detected_xi: bool) -> str:
    """Apply the three-scenario decision tree from notes/levier1B_README.md."""
    s_xi = stats.get("xi_chi")
    s_h0 = stats.get("H0")
    if s_xi is None or s_h0 is None:
        return "Cannot evaluate discriminator: missing xi_chi or H0 posteriors."

    xi_mean = s_xi["mean"]
    xi_std  = s_xi["std"]
    xi_lo95 = s_xi["lo95"]
    xi_hi95 = s_xi["hi95"]
    h0_mean = s_h0["mean"]

    # H0 retreat: SH0ES tension < 3 sigma
    h0_shoes_tension = abs(h0_mean - SHOES_H0_CENTRAL) / np.sqrt(
        s_h0["std"] ** 2 + SHOES_H0_SIGMA ** 2
    )
    h0_retreats = h0_shoes_tension < 3.0

    # xi_chi != 0 at >= 2sigma: 95% CI must exclude 0
    xi_detected = detected_xi or (xi_lo95 > 0 or xi_hi95 < 0)
    xi_sigma = abs(xi_mean) / xi_std if xi_std > 1e-10 else 0.0

    # S8 retreat: would need sigma8+Omega_m; use placeholder logic
    s8_data = stats.get("sigma8")
    s8_retreats_text = (
        "S_8 retreat: CANNOT EVALUATE (sigma8 not in chain; add as derived param)"
    )

    lines = []
    if xi_detected and h0_retreats:
        lines.append(
            "SCENARIO A — PRD LETTER CANDIDATE: xi_chi != 0 (>= 2sigma) "
            f"[xi = {xi_mean:.4f}, {xi_sigma:.1f}sigma from 0] "
            f"AND H_0 retreats ({h0_shoes_tension:.1f}sigma from SH0ES). "
            "Verify S_8 retreat before submitting. "
            "Draft the Scenario A abstract from notes/levier1B_pre_drafted_abstracts.md."
        )
    elif xi_detected and not h0_retreats:
        lines.append(
            "SCENARIO B (mixed) — xi_chi shows preference but H_0 does not retreat. "
            "NMC modifies G_eff but the expansion history anchor H_0 remains Planck-like. "
            "Consider whether w_0/w_a account for the H_0 direction instead."
        )
    elif h0_retreats and not xi_detected:
        lines.append(
            "SCENARIO B (mixed, H0-only) — H_0 retreats but xi_chi is consistent with 0. "
            "The tension reduction may be driven by the dark energy sector (w_0, w_a) "
            "rather than the NMC coupling. Re-examine the w_0/w_a vs LCDM comparison."
        )
    else:
        lines.append(
            "SCENARIO C — NULL RESULT: xi_chi consistent with 0 AND H_0 does not retreat. "
            "NMC alone + Planck + KiDS does not reduce cosmological tensions at this run's "
            "significance. Confirms motivation for full Levier #1 with EDE. "
            "Renew effort on AxiCLASS shooting fix."
        )

    lines.append(s8_retreats_text)
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Plotting
# ---------------------------------------------------------------------------

def _getdist_samples(chain: dict, param_list: list[str]):
    """Build a getdist MCSamples object for the given parameter subset."""
    from getdist import MCSamples
    col_names = chain["col_names"]
    indices, names, labels = [], [], []
    for p in param_list:
        if p in col_names:
            indices.append(col_names.index(p))
            names.append(p)
            meta = PARAM_META.get(p)
            labels.append(meta[0] if meta else p)
    data = chain["samples"][:, indices]
    return MCSamples(
        samples=data,
        weights=chain["weights"],
        names=names,
        labels=labels,
    ), names


def make_triangle_cosmo(chain: dict, outpath: Path) -> None:
    """Triangle plot for the 10 cosmological parameters."""
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    available = [p for p in COSMO_PARAMS if p in chain["col_names"]]

    try:
        from getdist import MCSamples
        import getdist.plots as gdp
        gd, names = _getdist_samples(chain, available)
        g = gdp.get_subplot_plotter(width_inch=14)
        g.triangle_plot(gd, filled=True, contour_levels=[0.68, 0.95])
        g.export(str(outpath))
        print(f"  [getdist] cosmo triangle saved: {outpath}")
        return
    except ImportError:
        print("  [INFO] getdist not available; trying corner", file=sys.stderr)
    except Exception as exc:
        print(f"  [WARNING] getdist triangle failed: {exc}; trying corner",
              file=sys.stderr)

    try:
        import corner
        col_names = chain["col_names"]
        indices = [col_names.index(p) for p in available]
        labels  = [PARAM_META.get(p, (p,))[0] for p in available]
        data = chain["samples"][:, indices]
        fig = corner.corner(data, weights=chain["weights"], labels=labels,
                            quantiles=[0.16, 0.5, 0.84], show_titles=True,
                            levels=[0.68, 0.95])
        fig.savefig(str(outpath), dpi=150, bbox_inches="tight")
        plt.close(fig)
        print(f"  [corner] cosmo triangle saved: {outpath}")
        return
    except ImportError:
        pass

    # Fallback: plain scatter
    col_names = chain["col_names"]
    indices = [col_names.index(p) for p in available]
    labels  = [PARAM_META.get(p, (p,))[0] for p in available]
    data = chain["samples"][:, indices]
    n = len(available)
    fig, axes = plt.subplots(n, n, figsize=(16, 16))
    w = chain["weights"]
    for i in range(n):
        for j in range(n):
            ax = axes[i, j]
            if i == j:
                ax.hist(data[:, i], weights=w, bins=40, color="steelblue",
                        density=True)
            elif i > j:
                ax.scatter(data[:, j], data[:, i], c=w / w.max(),
                           s=0.3, cmap="Blues_r", alpha=0.3)
            else:
                ax.set_visible(False)
            if i == n - 1:
                ax.set_xlabel(labels[j], fontsize=7)
            if j == 0 and i > 0:
                ax.set_ylabel(labels[i], fontsize=7)
    fig.suptitle("Levier #1B — cosmological parameters", fontsize=11)
    fig.tight_layout()
    fig.savefig(str(outpath), dpi=120, bbox_inches="tight")
    plt.close(fig)
    print(f"  [fallback scatter] cosmo triangle saved: {outpath}")


def make_marginals_cosmo(chain: dict, stats: dict, outpath: Path) -> None:
    """1-D marginals for the 10 cosmological parameters (incl. tau_reio)."""
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    n_params = len(COSMO_PARAMS)
    ncols = 4
    nrows = int(np.ceil(n_params / ncols))
    fig, axes = plt.subplots(nrows, ncols, figsize=(14, 4 * nrows))
    axes = axes.flatten()
    col_names = chain["col_names"]
    w = chain["weights"]

    for idx, name in enumerate(COSMO_PARAMS):
        ax = axes[idx]
        if name not in col_names:
            ax.text(0.5, 0.5, f"{name}\nnot found", transform=ax.transAxes,
                    ha="center", va="center")
            ax.set_title(name, fontsize=9)
            continue
        arr = chain["samples"][:, col_names.index(name)]
        meta = PARAM_META.get(name, (name, arr.min(), arr.max(), None))
        lo, hi = meta[1], meta[2]
        label = meta[0]

        ax.hist(arr, weights=w, bins=50, density=True, color="steelblue",
                alpha=0.7, label="posterior")
        ax.axhline(1.0 / (hi - lo), color="darkorange", linestyle="--",
                   linewidth=1.2, label=f"flat prior")
        s = stats.get(name)
        if s:
            ax.axvspan(s["lo68"], s["hi68"], alpha=0.15, color="navy")
            ax.axvline(s["median"], color="navy", linewidth=0.9, linestyle=":")
        ax.set_xlabel(label, fontsize=8)
        ax.set_ylabel("density", fontsize=7)
        ax.set_title(name, fontsize=8)
        ax.legend(fontsize=5, loc="upper right")

    for idx in range(n_params, len(axes)):
        axes[idx].set_visible(False)

    fig.suptitle(
        "Levier #1B — 1-D cosmological marginals\n"
        "(Planck PR4 + DESI DR2 BAO + Pantheon+ + KiDS S₈, Cassini ON)",
        fontsize=10,
    )
    fig.tight_layout(rect=[0, 0, 1, 0.96])
    fig.savefig(str(outpath), dpi=150, bbox_inches="tight")
    import matplotlib.pyplot as plt_mod
    plt_mod.close(fig)
    print(f"  cosmo marginals saved: {outpath}")


def make_marginals_nuisance(chain: dict, stats: dict, outpath: Path) -> None:
    """1-D marginals for the 9 Planck nuisance parameters (collapsed figure)."""
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    available = [p for p in NUISANCE_PARAMS if p in chain["col_names"]]
    if not available:
        print("  [WARNING] No nuisance parameters found in chain; "
              "skipping nuisance marginals plot.", file=sys.stderr)
        return

    n = len(available)
    ncols = 3
    nrows = int(np.ceil(n / ncols))
    fig, axes = plt.subplots(nrows, ncols, figsize=(12, 3.5 * nrows))
    axes = axes.flatten()
    col_names = chain["col_names"]
    w = chain["weights"]

    for idx, name in enumerate(available):
        ax = axes[idx]
        arr = chain["samples"][:, col_names.index(name)]
        meta = PARAM_META.get(name, (name, arr.min(), arr.max(), None))
        lo, hi = meta[1], meta[2]
        label = meta[0]

        ax.hist(arr, weights=w, bins=50, density=True, color="tomato",
                alpha=0.7, label="posterior")
        if hi > lo:
            ax.axhline(1.0 / (hi - lo), color="darkorange", linestyle="--",
                       linewidth=1.1, label="approx flat prior")
        s = stats.get(name)
        if s:
            ax.axvspan(s["lo68"], s["hi68"], alpha=0.15, color="darkred")
            ax.axvline(s["median"], color="darkred", linewidth=0.9, linestyle=":")
        ax.set_xlabel(label, fontsize=8)
        ax.set_ylabel("density", fontsize=7)
        ax.set_title(name, fontsize=8)
        ax.legend(fontsize=5)

    for idx in range(n, len(axes)):
        axes[idx].set_visible(False)

    fig.suptitle(
        "Levier #1B — Planck nuisance parameters (cosmology-agnostic)\n"
        "Shown for chain health only; not used in cosmological inference.",
        fontsize=10,
    )
    fig.tight_layout(rect=[0, 0, 1, 0.93])
    fig.savefig(str(outpath), dpi=150, bbox_inches="tight")
    plt.close(fig)
    print(f"  nuisance marginals saved: {outpath}")


def make_xi_chi_comparison(
    chain_levier1B: dict,
    outpath: Path,
    chain_v5: dict | None = None,
    chain_v50s8: dict | None = None,
) -> None:
    """
    Side-by-side xi_chi posterior comparison:
      - v5 (DESI DR2 + Pantheon+, wide prior, no Cassini)
      - v50plusS8 (same + KiDS S8, no Cassini)
      - levier1B (Planck PR4 + DESI DR2 + Pantheon+ + KiDS S8, Cassini ON)

    When chain_v5 / chain_v50s8 are None, falls back to hardcoded reference
    values from the companion notes files.
    """
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from scipy.stats import gaussian_kde

    fig, ax = plt.subplots(figsize=(9, 5))

    # ---- Gaussian approximations for reference runs (hardcoded baselines) ----
    xi_grid = np.linspace(-0.12, 0.12, 600)

    def plot_gaussian_approx(mean, std, lo68, hi68, label, color, linestyle="--",
                              alpha_fill=0.12):
        from scipy.stats import norm
        y = norm.pdf(xi_grid, loc=mean, scale=std)
        ax.plot(xi_grid, y, linestyle=linestyle, color=color, linewidth=1.5,
                label=label)
        mask = (xi_grid >= lo68) & (xi_grid <= hi68)
        ax.fill_between(xi_grid[mask], y[mask], alpha=alpha_fill, color=color)

    # v5 baseline (hardcoded from notes)
    if chain_v5 is None:
        plot_gaussian_approx(
            V5_XI_MEAN, (V5_XI_HI68 - V5_XI_LO68) / 2,
            V5_XI_LO68, V5_XI_HI68,
            label=r"v5: DESI DR2 + Pantheon+ (ref.)",
            color="gray", linestyle="--",
        )
    else:
        xi_v5 = extract_param(chain_v5, "xi_chi")
        w_v5 = chain_v5["weights"]
        if xi_v5 is not None:
            try:
                kde_v5 = gaussian_kde(xi_v5, weights=w_v5 / w_v5.sum(),
                                      bw_method="silverman")
                ax.plot(xi_grid, kde_v5(xi_grid), "--", color="gray",
                        linewidth=1.5, label=r"v5: DESI DR2 + Pantheon+")
            except Exception:
                plot_gaussian_approx(V5_XI_MEAN, (V5_XI_HI68 - V5_XI_LO68) / 2,
                                     V5_XI_LO68, V5_XI_HI68,
                                     label="v5 (approx)", color="gray")

    # v50plusS8 baseline (hardcoded from notes)
    if chain_v50s8 is None:
        plot_gaussian_approx(
            V50S8_XI_MEAN, (V50S8_XI_HI68 - V50S8_XI_LO68) / 2,
            V50S8_XI_LO68, V50S8_XI_HI68,
            label=r"v50plusS8: +KiDS S$_8$ (ref.)",
            color="steelblue", linestyle="-.",
        )
    else:
        xi_v50s8 = extract_param(chain_v50s8, "xi_chi")
        w_v50s8 = chain_v50s8["weights"]
        if xi_v50s8 is not None:
            try:
                kde_v50s8 = gaussian_kde(xi_v50s8, weights=w_v50s8 / w_v50s8.sum(),
                                         bw_method="silverman")
                ax.plot(xi_grid, kde_v50s8(xi_grid), "-.", color="steelblue",
                        linewidth=1.5, label=r"v50plusS8: +KiDS S$_8$")
            except Exception:
                plot_gaussian_approx(V50S8_XI_MEAN, (V50S8_XI_HI68 - V50S8_XI_LO68) / 2,
                                     V50S8_XI_LO68, V50S8_XI_HI68,
                                     label="v50plusS8 (approx)", color="steelblue")

    # levier1B (from actual chain)
    xi_1B = extract_param(chain_levier1B, "xi_chi")
    w_1B  = chain_levier1B["weights"]
    if xi_1B is not None:
        try:
            from scipy.stats import gaussian_kde as gkde
            kde_1B = gkde(xi_1B, weights=w_1B / w_1B.sum(), bw_method="silverman")
            y_1B = kde_1B(xi_grid)
            ax.plot(xi_grid, y_1B, "-", color="crimson", linewidth=2.2,
                    label=r"Levier #1B: Planck PR4 + DESI DR2 + Pantheon+ + KiDS, Cassini ON")
            # 68% CI fill
            q = weighted_quantile(xi_1B, [0.16, 0.84], w_1B)
            mask = (xi_grid >= q[0]) & (xi_grid <= q[1])
            ax.fill_between(xi_grid[mask], y_1B[mask], alpha=0.2, color="crimson")
        except Exception as exc:
            print(f"  [WARNING] levier1B KDE failed: {exc}", file=sys.stderr)
    else:
        print("  [WARNING] xi_chi not found in levier1B chain; "
              "skipping levier1B curve.", file=sys.stderr)

    # Annotations
    ax.axvline(0, color="black", linewidth=0.8, linestyle=":", alpha=0.7,
               label=r"$\xi_\chi = 0$ (ΛCDM)")
    ax.axvline(CASSINI_WALL_XI, color="purple", linewidth=1.0, linestyle="--",
               alpha=0.6, label=f"Cassini wall ±{CASSINI_WALL_XI:.4f}")
    ax.axvline(-CASSINI_WALL_XI, color="purple", linewidth=1.0, linestyle="--",
               alpha=0.6)

    ax.set_xlabel(r"$\xi_\chi$", fontsize=13)
    ax.set_ylabel("Posterior density", fontsize=11)
    ax.set_title(
        r"$\xi_\chi$ posterior: v5 vs v50plusS8 vs Levier #1B" + "\n"
        r"(non-minimal coupling; $\xi_\chi=0$ is $\Lambda$CDM)",
        fontsize=11,
    )
    ax.legend(fontsize=8, loc="upper right")
    ax.set_xlim(-0.12, 0.12)
    ax.set_ylim(bottom=0)

    # Wolf+2025 annotation
    ax.text(
        0.02, 0.97,
        f"Wolf+2025 (arXiv:2504.07679):\nlog B = {WOLF2025_LN_BAYES:.2f} ± {WOLF2025_LN_BAYES_ERR:.1f}",
        transform=ax.transAxes, fontsize=7.5, va="top",
        bbox=dict(boxstyle="round,pad=0.3", fc="lightyellow", ec="goldenrod", alpha=0.8),
    )

    fig.tight_layout()
    fig.savefig(str(outpath), dpi=150, bbox_inches="tight")
    plt.close(fig)
    print(f"  xi_chi comparison plot saved: {outpath}")


# ---------------------------------------------------------------------------
# Summary outputs
# ---------------------------------------------------------------------------

def render_summary_tex(
    stats_cosmo: dict,
    stats_nuisance: dict,
    chain: dict,
    outpath: Path,
    run_date: str,
    chain_prefix: str,
    n_per_chain: list[int],
    burnin: float,
) -> None:
    """Write LaTeX table for cosmological parameters."""
    rows = []
    for name in COSMO_PARAMS:
        s = stats_cosmo.get(name)
        if s is None:
            continue
        meta = PARAM_META.get(name, (name, 0, 1, 0))
        lo, hi, centre = meta[1], meta[2], meta[3]
        label = meta[0].replace("$", "").replace(r"\mathrm", "")
        if name == "xi_chi":
            prior_note = (
                r"Cassini wall $|\xi_\chi|\cdot(\chi_0/M_P)^2 < 6\times10^{-6}$"
            )
        else:
            dev = (s["mean"] - centre) / (hi - lo) if (hi - lo) > 0 else 0.0
            prior_note = f"prior centre {centre:.4g}; shift ${100*dev:+.1f}$\\% of prior"
        rows.append(
            f"  {label} & "
            f"${s['mean']:.4f}$ & "
            f"$[{s['lo68']:.4f},\\,{s['hi68']:.4f}]$ & "
            f"$[{s['lo95']:.4f},\\,{s['hi95']:.4f}]$ & "
            f"{prior_note} \\\\"
        )

    n_total = sum(n_per_chain)
    tex = textwrap.dedent(rf"""
    % Auto-generated by posterior_levier1B.py on {run_date}
    % Chain prefix: {chain_prefix}
    % Burn-in: {100*burnin:.0f}%
    % Total post-burnin samples: {n_total}
    \begin{{table}}[ht]
    \centering
    \caption{{%
        Levier~\#1B MCMC posterior: Planck 2018 + DESI DR2 BAO + Pantheon+ + KiDS-1000.
        Burn-in {100*burnin:.0f}\,\%, {n_total} post-burnin samples from 4 chains.
        Run date: {run_date}. Cassini wall ON.
    }}
    \label{{tab:posterior_levier1B}}
    \begin{{tabular}}{{lcccc}}
    \hline\hline
    Parameter & Mean & 68\,\% CI & 95\,\% CI & Prior / constraint \\
    \hline
    {chr(10).join(rows)}
    \hline\hline
    \end{{tabular}}
    \end{{table}}
    """).strip()

    outpath.write_text(tex + "\n")
    print(f"  LaTeX summary saved: {outpath}")


def render_summary_md(
    stats_cosmo: dict,
    stats_nuisance: dict,
    chain: dict,
    log_B10: float,
    sd_note: str,
    honesty_verdict: str,
    xi_detected: bool,
    outpath: Path,
    run_date: str,
    chain_prefix: str,
    n_per_chain: list[int],
    burnin: float,
) -> None:
    """Write detailed Markdown summary with discriminator section."""
    n_total = sum(n_per_chain)
    w = chain["weights"]

    shoes_text   = test_shoes_tension(stats_cosmo)
    w0wa_text    = test_w0wa_lcdm(stats_cosmo)
    s8_text      = estimate_s8(stats_cosmo)
    scenario_txt = discriminator_scenario(stats_cosmo, xi_detected)

    # Cosmological table
    cosmo_rows = ["| Parameter | Mean | 68% CI | 95% CI | ESS |",
                  "|---|---|---|---|---|"]
    for name in COSMO_PARAMS:
        s = stats_cosmo.get(name)
        if not s:
            continue
        cosmo_rows.append(
            f"| {name} | {s['mean']:.5f} | "
            f"[{s['lo68']:.5f}, {s['hi68']:.5f}] | "
            f"[{s['lo95']:.5f}, {s['hi95']:.5f}] | "
            f"{s['ess']:.0f} |"
        )

    # Nuisance table (abbreviated)
    nuis_rows = ["| Parameter | Mean | 68% CI |", "|---|---|---|"]
    for name in NUISANCE_PARAMS:
        s = stats_nuisance.get(name)
        if not s:
            nuis_rows.append(f"| {name} | — | not in chain |")
            continue
        nuis_rows.append(
            f"| {name} | {s['mean']:.4f} | "
            f"[{s['lo68']:.4f}, {s['hi68']:.4f}] |"
        )

    log_B10_str = f"{log_B10:.2f}" if not (
        isinstance(log_B10, float) and (np.isnan(log_B10) or np.isinf(log_B10))
    ) else "N/A"

    md = f"""# Levier #1B MCMC — Posterior Summary

**Generated:** {run_date}
**Chain prefix:** `{chain_prefix}`
**Burn-in:** {100*burnin:.0f}%
**Post-burnin samples:** {n_total} ({", ".join(str(n) for n in n_per_chain)} per chain)
**Likelihoods:** Planck 2018 lowl.TT + lowl.EE + NPIPE highl CamSpec TTTEEE +
lensing.native + DESI DR2 BAO + Pantheon+ + KiDS-1000 S₈ (Gaussian prior)
**Priors:** Cassini wall ON (`|ξ_χ|·(χ₀/Mₚ)² < 6×10⁻⁶`); ACT penalty OFF
**Theory:** vanilla CLASS 3.3.4 + `eci_nmc_theory.ECINMCTheory`
**Sampled params:** 10 cosmological + 9 Planck nuisance = 19 total

---

## Cosmological parameter posteriors

{chr(10).join(cosmo_rows)}

---

## Planck nuisance parameter posteriors

(Shown for chain-health verification only; not used in cosmological interpretation.)

{chr(10).join(nuis_rows)}

---

## Discriminator: H₀ vs SH0ES

{shoes_text}

---

## Discriminator: ξ_χ vs zero (NMC detection)

{sd_note}

**Honesty gate verdict:**
{honesty_verdict}

---

## Discriminator: (w₀, w_a) vs ΛCDM

{w0wa_text}

---

## Discriminator: S₈ tension

{s8_text}

---

## Scenario classification

{scenario_txt}

---

## Bayes factor summary

| Quantity | This run | Wolf+2025 (arXiv:2504.07679) |
|---|---|---|
| log B (NMC vs ΛCDM) | {log_B10_str} (Savage-Dickey KDE) | 7.34 ± 0.6 |
| Dataset | Planck 2018 + DESI DR2 + Pantheon+ + KiDS | Planck PR4 + DESI DR2 + Pantheon+ |
| Cassini wall | ON | not specified |
| ξ_χ prior | [-0.1, 0.1] uniform + Cassini | same range |

**Caveat:** The Savage-Dickey ratio computed here uses a 1-D Gaussian KDE and a
uniform prior density at ξ_χ=0. It approximates — but does not replace — a proper
nested sampling evidence ratio. The Wolf+2025 log B = 7.34 was computed via
MultiNest. Treat our SD estimate as a sanity check, not a precision measurement.

---

## Comparison to v5 and v50plusS8 baselines

| Run | ξ_χ 68% CI | ξ_χ constrained? | Planck? | KiDS? |
|---|---|---|---|---|
| v5 (baseline) | [{V5_XI_LO68:.3f}, {V5_XI_HI68:.3f}] | No | No | No |
| v50plusS8 | [{V50S8_XI_LO68:.3f}, {V50S8_XI_HI68:.3f}] | No | No | Yes |
| Levier #1B | [FILL_LO68, FILL_HI68] | SEE GATE | Yes | Yes |

The v50plusS8 ablation confirmed: **KiDS S₈ alone does not constrain ξ_χ.**
Any tightening seen in levier1B comes from Planck's sensitivity to G_eff(k)
in the CMB power spectrum, consistent with Wolf+2025's finding.

---

## Files produced

- `triangle_cosmo.pdf` — triangle plot (10 cosmological parameters)
- `marginals_cosmo.pdf` — 1-D marginals (cosmological, with tau_reio)
- `marginals_nuisance.pdf` — 1-D marginals (9 Planck nuisance parameters)
- `xi_chi_comparison.pdf` — side-by-side ξ_χ: v5 / v50plusS8 / levier1B
- `summary.tex` — LaTeX table (importable into paper)
- `summary.md` — this file

## Reproducing this analysis

```bash
python3 scripts/analysis/posterior_levier1B.py \\
    --chain-prefix /root/crossed-cosmos/eci_levier1B \\
    --burnin 0.30 \\
    --outdir notes/posterior_levier1B_{run_date}
```

See `notes/posterior_levier1B_README.md` for full interpretation guide.
"""

    outpath.write_text(md)
    print(f"  Markdown summary saved: {outpath}")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Levier #1B posterior analysis (10-param NMC+w0wa, Planck+BAO+SN+KiDS)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    parser.add_argument(
        "--chain-prefix", default=None,
        help="Prefix for levier1B chain files (reads <prefix>.{1..nchains}.txt). "
             "Default: <cwd>/eci_levier1B",
    )
    parser.add_argument(
        "--v5-prefix", default=None,
        help="Prefix for v5 chain files (optional; enables comparison plot from chain data).",
    )
    parser.add_argument(
        "--v50s8-prefix", default=None,
        help="Prefix for v50plusS8 chain files (optional).",
    )
    parser.add_argument(
        "--burnin", type=float, default=0.30,
        help="Burn-in fraction to discard (default: 0.30)",
    )
    parser.add_argument(
        "--outdir", default=None,
        help="Output directory. Default: notes/posterior_levier1B_<DATE>",
    )
    parser.add_argument(
        "--nchains", type=int, default=4,
        help="Number of chain files (default: 4)",
    )
    parser.add_argument(
        "--no-plots", action="store_true",
        help="Skip all plots; write only summary files.",
    )
    parser.add_argument(
        "--max-samples", type=int, default=None,
        help="Cap post-burnin samples per chain (for test runs).",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    run_date = date.today().isoformat()

    # Resolve chain prefix
    chain_prefix = args.chain_prefix or str(Path.cwd() / "eci_levier1B")

    # Resolve output directory
    if args.outdir is None:
        outdir = _REPO_ROOT / "notes" / f"posterior_levier1B_{run_date}"
    else:
        outdir = Path(args.outdir)
    outdir.mkdir(parents=True, exist_ok=True)

    print(f"\n=== Levier #1B Posterior Analysis ===")
    print(f"Chain prefix : {chain_prefix}")
    print(f"Burn-in      : {100*args.burnin:.0f}%")
    print(f"Output dir   : {outdir}")
    print()

    # --- Read levier1B chains ---
    print("Reading levier1B chains...")
    chain = read_cobaya_chains(
        prefix=chain_prefix,
        n_chains=args.nchains,
        burnin=args.burnin,
        max_samples=args.max_samples,
        expected_params=ALL_PARAMS,
    )
    n_total = sum(chain["n_per_chain"])
    print(f"Total post-burnin samples: {n_total}\n")

    # --- Optional comparison chains ---
    chain_v5   = None
    chain_v50s8 = None
    if args.v5_prefix:
        print("Reading v5 chains...")
        try:
            chain_v5 = read_cobaya_chains(
                args.v5_prefix, n_chains=args.nchains,
                burnin=args.burnin, max_samples=args.max_samples,
            )
        except RuntimeError as exc:
            print(f"  [WARNING] v5 chains: {exc}", file=sys.stderr)
    if args.v50s8_prefix:
        print("Reading v50plusS8 chains...")
        try:
            chain_v50s8 = read_cobaya_chains(
                args.v50s8_prefix, n_chains=args.nchains,
                burnin=args.burnin, max_samples=args.max_samples,
            )
        except RuntimeError as exc:
            print(f"  [WARNING] v50plusS8 chains: {exc}", file=sys.stderr)

    # --- Statistics ---
    print("Computing statistics...")
    stats_cosmo    = compute_stats(chain, COSMO_PARAMS)
    stats_nuisance = compute_stats(chain, NUISANCE_PARAMS)

    # --- Savage-Dickey Bayes factor ---
    xi_arr = extract_param(chain, "xi_chi")
    if xi_arr is not None:
        log_B10, pd_at_0, sd_note = savage_dickey_bayes_factor(
            xi_arr, chain["weights"]
        )
        hv, xi_detected = honesty_gate_xi_chi(
            stats_cosmo["xi_chi"], xi_arr, chain["weights"], log_B10
        )
    else:
        log_B10, pd_at_0 = float("nan"), float("nan")
        sd_note = "xi_chi not found in chain columns; Savage-Dickey cannot be computed."
        hv = "xi_chi missing from chain; check YAML sampled_params."
        xi_detected = False

    # --- Plots ---
    if not args.no_plots:
        print("Generating cosmological triangle plot...")
        try:
            make_triangle_cosmo(chain, outdir / "triangle_cosmo.pdf")
        except Exception as exc:
            print(f"  [ERROR] cosmo triangle: {exc}", file=sys.stderr)

        print("Generating cosmological marginals plot...")
        try:
            make_marginals_cosmo(chain, stats_cosmo, outdir / "marginals_cosmo.pdf")
        except Exception as exc:
            print(f"  [ERROR] cosmo marginals: {exc}", file=sys.stderr)

        print("Generating nuisance marginals plot...")
        try:
            make_marginals_nuisance(chain, stats_nuisance,
                                    outdir / "marginals_nuisance.pdf")
        except Exception as exc:
            print(f"  [ERROR] nuisance marginals: {exc}", file=sys.stderr)

        print("Generating xi_chi comparison plot...")
        try:
            make_xi_chi_comparison(chain, outdir / "xi_chi_comparison.pdf",
                                   chain_v5=chain_v5, chain_v50s8=chain_v50s8)
        except Exception as exc:
            print(f"  [ERROR] xi_chi comparison: {exc}", file=sys.stderr)

    # --- Summary files ---
    print("Writing summary files...")
    render_summary_tex(
        stats_cosmo, stats_nuisance, chain,
        outdir / "summary.tex",
        run_date=run_date, chain_prefix=chain_prefix,
        n_per_chain=chain["n_per_chain"], burnin=args.burnin,
    )
    render_summary_md(
        stats_cosmo, stats_nuisance, chain,
        log_B10=log_B10, sd_note=sd_note,
        honesty_verdict=hv, xi_detected=xi_detected,
        outpath=outdir / "summary.md",
        run_date=run_date, chain_prefix=chain_prefix,
        n_per_chain=chain["n_per_chain"], burnin=args.burnin,
    )

    print()
    print("=== Done ===")
    print(f"Outputs in: {outdir}")
    print()
    print("--- Quick digest ---")
    for name in ["H0", "tau_reio", "w0_fld", "wa_fld", "xi_chi", "chi_initial"]:
        s = stats_cosmo.get(name)
        if s:
            print(
                f"  {name:15s}: mean={s['mean']:.5f}  "
                f"68%CI=[{s['lo68']:.5f}, {s['hi68']:.5f}]  "
                f"ESS={s['ess']:.0f}"
            )
    if not np.isnan(log_B10):
        print(f"\n  Savage-Dickey log B_10 (NMC vs LCDM) = {log_B10:.2f}")
    print()
    print("--- Honesty gate ---")
    print(f"  {hv}")
    print()


if __name__ == "__main__":
    main()
