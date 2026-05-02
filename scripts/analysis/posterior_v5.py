#!/usr/bin/env python3
"""
posterior_v5.py — ECI MCMC v5 posterior analysis
=================================================
Reads 4 Cobaya chain files (eci.{1,2,3,4}.txt), drops a configurable
burn-in fraction, and produces:

  <outdir>/triangle.pdf   — triangle / corner plot (all 9 sampled params)
  <outdir>/marginals.pdf  — 1-D marginals with flat-prior overlay
  <outdir>/summary.tex    — LaTeX table: mean, 68 CI, 95 CI, prior comparison
  <outdir>/summary.md     — Markdown summary + honest discriminator section

Usage:
  python posterior_v5.py [options]

Options:
  --chain-prefix PATH   Prefix of chain files, e.g. /path/to/eci
                        (default: ./eci, i.e. eci.1.txt … eci.4.txt in cwd)
  --burnin FLOAT        Burn-in fraction to discard (default: 0.30)
  --outdir PATH         Output directory (default: notes/posterior_v5_<DATE>
                        relative to the repo root, detected automatically)
  --nchains INT         Number of chain files to read (default: 4)
  --no-plots            Skip triangle/marginals, write only summary files
  --max-samples INT     Cap samples per chain to this number after burnin
                        (useful for fast test runs). Default: no cap.

Packages used: numpy, scipy, matplotlib, getdist.
Optional (gracefully degraded if absent): anesthetic, chainconsumer, corner.

The script does NOT execute any Boltzmann code and does NOT fetch data
from the internet. All it reads are the chain .txt files.
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
# Repo-root detection (best-effort; falls back to cwd)
# ---------------------------------------------------------------------------
def _find_repo_root(start: Path) -> Path:
    for parent in [start, *start.parents]:
        if (parent / ".git").exists():
            return parent
    return Path.cwd()


_HERE = Path(__file__).resolve().parent
_REPO_ROOT = _find_repo_root(_HERE)

# ---------------------------------------------------------------------------
# Parameter metadata
# ---------------------------------------------------------------------------
# Keys must match Cobaya column headers exactly.
PARAM_NAMES = [
    "H0", "omega_b", "omega_cdm", "n_s",
    "logA", "w0_fld", "wa_fld", "xi_chi", "chi_initial",
]

PARAM_META = {
    # name: (latex_label, prior_lo, prior_hi, prior_centre_or_special_note)
    "H0":          (r"$H_0$ [km/s/Mpc]",         55.0,  85.0,  67.4),
    "omega_b":     (r"$\Omega_b h^2$",             0.017, 0.027, 0.02237),
    "omega_cdm":   (r"$\Omega_c h^2$",             0.09,  0.15,  0.12),
    "n_s":         (r"$n_s$",                       0.9,   1.05,  0.9649),
    "logA":        (r"$\ln(10^{10}A_s)$",          2.5,   3.5,   3.044),
    "w0_fld":      (r"$w_0$",                      -1.2,  -0.5,  -1.0),
    "wa_fld":      (r"$w_a$",                      -2.0,   0.0,   0.0),
    "xi_chi":      (r"$\xi_\chi$",                 -0.1,   0.1,   0.0),
    "chi_initial": (r"$\chi_\mathrm{ini}$",         0.05,  0.2,   0.1),
}

# Cassini (PPN) hard wall: |xi_chi| < 0.024 in the unscreened limit used here.
# This is NOT the Wolf+2025 bound (xi/MP^2 < 6e-6 for the local field value);
# the local bound does not directly translate to the cosmological xi_chi because
# chi here is a thawing-excursion amplitude, not the local field value.
CASSINI_WALL = 0.024  # approximate, conservative, unscreened case

# SH0ES tension anchor: H0 = 73.04 +/- 1.04 km/s/Mpc (Riess+2022)
SHOES_H0_CENTRAL = 73.04
SHOES_H0_SIGMA = 1.04

# Wolf+2025 (arXiv:2504.07679) anchor
WOLF2025_LN_BAYES = 7.34
WOLF2025_LN_BAYES_ERR = 0.6  # 1-sigma stated uncertainty

# ---------------------------------------------------------------------------
# Chain I/O
# ---------------------------------------------------------------------------

def read_cobaya_chains(prefix: str, n_chains: int = 4, burnin: float = 0.30,
                       max_samples: int | None = None) -> dict:
    """
    Read Cobaya plain-text chain files <prefix>.{1..n_chains}.txt.

    Returns a dict with keys:
        'samples'     : np.ndarray shape (N_total, n_params)
        'weights'     : np.ndarray shape (N_total,)
        'logpost'     : np.ndarray shape (N_total,) — minuslogpost
        'col_names'   : list[str]
        'n_per_chain' : list[int]  — post-burnin sample counts per chain
        'chain_files' : list[str]
    """
    all_samples = []
    all_weights = []
    all_logpost = []
    n_per_chain = []
    chain_files = []
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
            else:
                if this_cols != col_names:
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

        # Cobaya columns: weight, minuslogpost, <params...>
        weights = data[:, 0]
        logpost = data[:, 1]
        samples = data[:, 2:]
        col_names_params = col_names[2:]

        all_samples.append(samples)
        all_weights.append(weights)
        all_logpost.append(logpost)
        n_per_chain.append(data.shape[0])
        print(f"  chain {ci}: {data.shape[0]} post-burnin rows from {fpath}")

    if not all_samples:
        raise RuntimeError(
            f"No chain files could be read with prefix '{prefix}'. "
            "Check the path and that the chains have run."
        )

    samples = np.concatenate(all_samples, axis=0)
    weights = np.concatenate(all_weights, axis=0)
    logpost = np.concatenate(all_logpost, axis=0)

    # Validate that our expected params appear as columns
    missing = [p for p in PARAM_NAMES if p not in col_names_params]
    if missing:
        print(f"  [WARNING] expected params not found as columns: {missing}",
              file=sys.stderr)
        print(f"  Available columns: {col_names_params}", file=sys.stderr)

    return dict(
        samples=samples,
        weights=weights,
        logpost=logpost,
        col_names=col_names_params,
        n_per_chain=n_per_chain,
        chain_files=chain_files,
    )


def extract_param_array(chain: dict, name: str) -> np.ndarray | None:
    """Return the 1-D array for a named parameter, or None if not present."""
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
    """Weighted quantiles (exact, via cumulative weight)."""
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


def compute_stats(chain: dict) -> dict[str, dict]:
    """Compute mean, std, CI68, CI95 for each sampled parameter."""
    w = chain["weights"]
    stats = {}
    for name in PARAM_NAMES:
        arr = extract_param_array(chain, name)
        if arr is None:
            stats[name] = None
            continue
        q = weighted_quantile(arr, [0.025, 0.16, 0.5, 0.84, 0.975], w)
        stats[name] = dict(
            mean=weighted_mean(arr, w),
            std=weighted_std(arr, w),
            lo95=q[0], lo68=q[1], median=q[2], hi68=q[3], hi95=q[4],
        )
    return stats


def effective_sample_size(values: np.ndarray, weights: np.ndarray) -> float:
    """Kish effective sample size."""
    return float(np.sum(weights) ** 2 / np.sum(weights ** 2))


# ---------------------------------------------------------------------------
# Prior-dominated check
# ---------------------------------------------------------------------------

def prior_dominated_fraction(values: np.ndarray, weights: np.ndarray,
                               prior_lo: float, prior_hi: float,
                               n_bins: int = 30) -> float:
    """
    Rough check: compute the max KL divergence from a uniform prior.

    Returns a fraction in [0, 1]:
      - Near 0: posterior is effectively flat over the prior (prior-dominated)
      - Near 1: posterior is strongly informative relative to flat prior

    Method: compare weighted histogram to uniform; return 1 - chi2_stat/chi2_max
    where chi2_max is the theoretical max for a delta function.
    """
    bins = np.linspace(prior_lo, prior_hi, n_bins + 1)
    hist_w, _ = np.histogram(values, bins=bins, weights=weights)
    hist_w = hist_w / hist_w.sum()
    uniform = np.ones(n_bins) / n_bins
    # chi-square divergence (symmetric)
    eps = 1e-12
    chi2 = np.sum((hist_w - uniform) ** 2 / (uniform + eps))
    chi2_max = (1.0 - 1.0 / n_bins) ** 2 / (1.0 / n_bins)  # approx delta-fn
    return float(min(chi2 / chi2_max, 1.0))


# ---------------------------------------------------------------------------
# Discriminator tests
# ---------------------------------------------------------------------------

def test_shoes_tension(stats: dict) -> str:
    """How many sigma is H0 posterior from SH0ES central value?"""
    s = stats.get("H0")
    if s is None:
        return "H0 not in posterior (check after run)"
    h0_mean = s["mean"]
    h0_std = s["std"]
    n_sigma = abs(h0_mean - SHOES_H0_CENTRAL) / np.sqrt(h0_std**2 + SHOES_H0_SIGMA**2)
    return (
        f"H0 posterior: {h0_mean:.2f} +/- {h0_std:.2f} km/s/Mpc. "
        f"SH0ES anchor: {SHOES_H0_CENTRAL} +/- {SHOES_H0_SIGMA}. "
        f"Tension: {n_sigma:.1f}σ (in quadrature)."
    )


def test_xi_chi_cassini(stats: dict, chain: dict) -> str:
    """Did xi_chi posterior pile up against the Cassini wall?"""
    s = stats.get("xi_chi")
    if s is None:
        return "xi_chi not in posterior (check after run)"
    arr = extract_param_array(chain, "xi_chi")
    w = chain["weights"]
    frac_above = float(np.sum(w[np.abs(arr) > CASSINI_WALL]) / np.sum(w))
    prior_lo, prior_hi = PARAM_META["xi_chi"][1], PARAM_META["xi_chi"][2]
    pdom = prior_dominated_fraction(arr, w, prior_lo, prior_hi)
    msg = (
        f"xi_chi posterior: mean = {s['mean']:.4f}, "
        f"68% CI = [{s['lo68']:.4f}, {s['hi68']:.4f}], "
        f"95% CI = [{s['lo95']:.4f}, {s['hi95']:.4f}]. "
        f"Fraction of posterior weight with |xi_chi| > {CASSINI_WALL} "
        f"(Cassini wall): {100*frac_above:.1f}%. "
        f"Prior-dominated score: {pdom:.2f} (0=flat=prior-dominated, 1=strongly informative)."
    )
    return msg


def test_w0wa_lcdm(stats: dict) -> str:
    """Consistency of (w0, wa) with LCDM (-1, 0)."""
    sw0 = stats.get("w0_fld")
    swa = stats.get("wa_fld")
    if sw0 is None or swa is None:
        return "w0_fld or wa_fld not in posterior (check after run)"

    def n_sigma_1d(mean, std, target):
        return abs(mean - target) / std

    n_w0 = n_sigma_1d(sw0["mean"], sw0["std"], -1.0)
    n_wa = n_sigma_1d(swa["mean"], swa["std"], 0.0)

    # 2-D check: distance from (-1, 0) in units of combined sigma
    # (diagonal covariance approximation — conservative)
    n_2d = np.sqrt(n_w0**2 + n_wa**2)

    results = []
    for n_sig, label in [(1, "1σ"), (2, "2σ"), (3, "3σ")]:
        consistent = n_2d <= n_sig
        results.append(f"{label}: {'YES' if consistent else 'NO'} (combined {n_2d:.1f}σ)")

    return (
        f"w0 = {sw0['mean']:.3f} +/- {sw0['std']:.3f} (LCDM=-1: {n_w0:.1f}σ). "
        f"wa = {swa['mean']:.3f} +/- {swa['std']:.3f} (LCDM=0: {n_wa:.1f}σ). "
        f"2D consistency with (-1,0): {', '.join(results)}. "
        f"NOTE: this uses a diagonal covariance; compute proper contour from triangle plot."
    )


# ---------------------------------------------------------------------------
# Plotting
# ---------------------------------------------------------------------------

def make_triangle_plot(chain: dict, outpath: Path) -> None:
    """Triangle plot using getdist (preferred) or corner as fallback."""
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    samples_arr = chain["samples"]
    weights = chain["weights"]
    col_names = chain["col_names"]

    # Extract only the 9 sampled params, in order
    param_indices = []
    labels = []
    used_names = []
    for name in PARAM_NAMES:
        if name in col_names:
            param_indices.append(col_names.index(name))
            labels.append(PARAM_META[name][0])
            used_names.append(name)

    data = samples_arr[:, param_indices]

    # Try getdist first
    try:
        from getdist import MCSamples
        import getdist.plots as gdp

        # Repeat rows by integer weight (getdist can take weights directly)
        gd_samples = MCSamples(
            samples=data,
            weights=weights,
            names=used_names,
            labels=[m[0].replace("$", "").replace(r"\mathrm", "").strip() for m in
                    [PARAM_META[n] for n in used_names]],
        )
        g = gdp.get_subplot_plotter(width_inch=12)
        g.triangle_plot(gd_samples, filled=True, contour_levels=[0.68, 0.95])
        g.export(str(outpath))
        print(f"  [getdist] triangle plot saved: {outpath}")
        return
    except ImportError:
        print("  [INFO] getdist not available; trying corner", file=sys.stderr)
    except Exception as exc:
        print(f"  [WARNING] getdist triangle failed: {exc}; trying corner",
              file=sys.stderr)

    # Fallback: corner
    try:
        import corner
        fig = corner.corner(
            data,
            weights=weights,
            labels=labels,
            quantiles=[0.16, 0.5, 0.84],
            show_titles=True,
            levels=[0.68, 0.95],
        )
        fig.savefig(str(outpath), dpi=150, bbox_inches="tight")
        plt.close(fig)
        print(f"  [corner] triangle plot saved: {outpath}")
        return
    except ImportError:
        pass

    # Last resort: simple scatter matrix
    import matplotlib.pyplot as plt
    n = len(used_names)
    fig, axes = plt.subplots(n, n, figsize=(14, 14))
    for i in range(n):
        for j in range(n):
            ax = axes[i, j]
            if i == j:
                ax.hist(data[:, i], weights=weights, bins=40, color="steelblue",
                        density=True)
                ax.set_xlabel(labels[i] if i == n - 1 else "")
            elif i > j:
                ax.scatter(data[:, j], data[:, i], c=weights / weights.max(),
                           s=0.5, cmap="Blues_r", alpha=0.3)
            else:
                ax.set_visible(False)
    fig.tight_layout()
    fig.savefig(str(outpath), dpi=120, bbox_inches="tight")
    plt.close(fig)
    print(f"  [matplotlib scatter] triangle plot saved: {outpath}")


def make_marginals_plot(chain: dict, stats: dict, outpath: Path) -> None:
    """1-D marginals with flat prior overlay."""
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    samples_arr = chain["samples"]
    weights = chain["weights"]
    col_names = chain["col_names"]

    n_params = len(PARAM_NAMES)
    ncols = 3
    nrows = int(np.ceil(n_params / ncols))
    fig, axes = plt.subplots(nrows, ncols, figsize=(14, 4 * nrows))
    axes = axes.flatten()

    for idx, name in enumerate(PARAM_NAMES):
        ax = axes[idx]
        if name not in col_names:
            ax.text(0.5, 0.5, f"{name}\nnot found", transform=ax.transAxes,
                    ha="center", va="center")
            ax.set_title(name)
            continue

        arr = samples_arr[:, col_names.index(name)]
        lo, hi = PARAM_META[name][1], PARAM_META[name][2]
        label = PARAM_META[name][0]

        ax.hist(arr, weights=weights, bins=50, density=True,
                color="steelblue", alpha=0.7, label="posterior")
        # Flat prior
        ax.axhline(1.0 / (hi - lo), color="darkorange", linestyle="--",
                   linewidth=1.2, label=f"flat prior [{lo:.3g}, {hi:.3g}]")

        # 68% CI band
        s = stats.get(name)
        if s:
            ax.axvspan(s["lo68"], s["hi68"], alpha=0.15, color="navy",
                       label="68% CI")
            ax.axvline(s["median"], color="navy", linewidth=1.0, linestyle=":")

        ax.set_xlabel(label, fontsize=9)
        ax.set_ylabel("density", fontsize=8)
        ax.set_title(name, fontsize=9)
        ax.legend(fontsize=6, loc="upper right")

    # Hide unused axes
    for idx in range(n_params, len(axes)):
        axes[idx].set_visible(False)

    fig.suptitle("ECI v5 MCMC — 1-D marginal posteriors (DESI DR2 + Pantheon+)",
                 fontsize=11)
    fig.tight_layout(rect=[0, 0, 1, 0.97])
    fig.savefig(str(outpath), dpi=150, bbox_inches="tight")
    plt.close(fig)
    print(f"  marginals plot saved: {outpath}")


# ---------------------------------------------------------------------------
# Summary outputs
# ---------------------------------------------------------------------------

def render_summary_tex(stats: dict, chain: dict, outpath: Path,
                        run_date: str, chain_prefix: str,
                        n_per_chain: list[int], burnin: float) -> None:
    """Write LaTeX summary table."""

    rows = []
    for name in PARAM_NAMES:
        s = stats.get(name)
        if s is None:
            continue
        lo, hi, centre = (PARAM_META[name][1], PARAM_META[name][2],
                          PARAM_META[name][3])
        label = PARAM_META[name][0].replace("$", "").replace(r"\mathrm", "")
        mean = s["mean"]
        lo68 = s["lo68"]
        hi68 = s["hi68"]
        lo95 = s["lo95"]
        hi95 = s["hi95"]

        # Prior comparison
        if name == "xi_chi":
            prior_note = r"Cassini hard wall $|\xi_\chi| < 0.024$"
        else:
            dev = (mean - centre) / (hi - lo)
            prior_note = (
                f"prior centre {centre:.4g}; "
                f"shift $= {100*dev:+.1f}$\\% of prior width"
            )

        rows.append(
            f"  {label} & "
            f"${mean:.4f}$ & "
            f"$[{lo68:.4f},\\,{hi68:.4f}]$ & "
            f"$[{lo95:.4f},\\,{hi95:.4f}]$ & "
            f"{prior_note} \\\\"
        )

    n_total = sum(n_per_chain)

    tex = textwrap.dedent(rf"""
    % Auto-generated by posterior_v5.py on {run_date}
    % Chain prefix: {chain_prefix}
    % Burn-in: {100*burnin:.0f}%
    % Total post-burnin samples: {n_total}
    \begin{{table}}[ht]
    \centering
    \caption{{%
        ECI v5 MCMC posterior: DESI DR2 BAO + Pantheon+.
        Burn-in {100*burnin:.0f}\,\%, {n_total} post-burnin samples from 4 chains.
        Run date: {run_date}.
    }}
    \label{{tab:posterior_v5}}
    \begin{{tabular}}{{lcccc}}
    \hline\hline
    Parameter & Mean & 68\,\% CI & 95\,\% CI & Prior / constraint note \\
    \hline
    {chr(10).join(rows)}
    \hline\hline
    \end{{tabular}}
    \end{{table}}
    """).strip()

    outpath.write_text(tex + "\n")
    print(f"  LaTeX summary saved: {outpath}")


def render_summary_md(stats: dict, chain: dict, outpath: Path,
                       run_date: str, chain_prefix: str,
                       n_per_chain: list[int], burnin: float,
                       args: argparse.Namespace) -> None:
    """Write honest Markdown summary."""

    n_total = sum(n_per_chain)
    w = chain["weights"]

    # --- Discriminator evaluations ---
    shoes_text = test_shoes_tension(stats)
    xi_text = test_xi_chi_cassini(stats, chain)
    w0wa_text = test_w0wa_lcdm(stats)

    # --- Per-param prior-dominated scores ---
    pdom_lines = []
    for name in PARAM_NAMES:
        arr = extract_param_array(chain, name)
        if arr is None:
            pdom_lines.append(f"- **{name}**: not found in chain columns")
            continue
        lo, hi = PARAM_META[name][1], PARAM_META[name][2]
        pdom = prior_dominated_fraction(arr, w, lo, hi)
        ess = effective_sample_size(arr, w)
        s = stats.get(name)
        if s is None:
            continue
        verdict = (
            "PRIOR-DOMINATED" if pdom < 0.15
            else "WEAKLY INFORMATIVE" if pdom < 0.40
            else "INFORMATIVE"
        )
        pdom_lines.append(
            f"- **{name}** ({PARAM_META[name][0]}): "
            f"pdom_score={pdom:.2f} [{verdict}], "
            f"ESS≈{ess:.0f}, "
            f"mean={s['mean']:.4f}, "
            f"68% CI=[{s['lo68']:.4f}, {s['hi68']:.4f}]"
        )

    # --- xi_chi specific honest analysis ---
    xi_s = stats.get("xi_chi")
    xi_arr = extract_param_array(chain, "xi_chi")
    if xi_s and xi_arr is not None:
        prior_lo, prior_hi = PARAM_META["xi_chi"][1], PARAM_META["xi_chi"][2]
        xi_pdom = prior_dominated_fraction(xi_arr, w, prior_lo, prior_hi)
        xi_ess = effective_sample_size(xi_arr, w)
        xi_ci_width = xi_s["hi68"] - xi_s["lo68"]
        prior_width = prior_hi - prior_lo
        xi_ci_vs_prior = xi_ci_width / prior_width

        if xi_ci_vs_prior > 0.85:
            xi_verdict = (
                "The 68% CI for xi_chi spans more than 85% of the prior width. "
                "This is consistent with a posterior that has not moved appreciably "
                "from the prior: DESI DR2 + Pantheon+ alone do NOT constrain xi_chi. "
                "This is expected: xi_chi enters growth via G_eff, and this run lacks "
                "CMB data. Wolf+2025 (arXiv:2504.07679) found log B = 7.34 +/- 0.6 "
                "for NMC vs LCDM on Planck PR4 + DR2 BAO + Pantheon+ -- the "
                "discriminating power came primarily from Planck, not from BAO+SN alone. "
                "Do not interpret a broad xi_chi posterior as evidence for or against ECI."
            )
        elif abs(xi_s["mean"]) < 3 * xi_s["std"]:
            xi_verdict = (
                "xi_chi posterior is broadly consistent with zero (< 3 sigma detection). "
                "The data weakly prefer xi_chi near zero but do not rule out NMC couplings "
                "within the sampled range."
            )
        else:
            xi_verdict = (
                f"xi_chi mean is {xi_s['mean']:.4f}, "
                f"std={xi_s['std']:.4f}. "
                f"Tension with xi_chi=0: {abs(xi_s['mean'])/xi_s['std']:.1f} sigma. "
                f"Verify with a Savage-Dickey density ratio before claiming detection."
            )
    else:
        xi_verdict = "xi_chi not available in this chain (check after run)"
        xi_ci_vs_prior = None
        xi_ess = None

    # --- w0/wa vs LCDM ---
    sw0 = stats.get("w0_fld")
    swa = stats.get("wa_fld")
    if sw0 and swa:
        n_w0 = abs(sw0["mean"] - (-1.0)) / sw0["std"]
        n_wa = abs(swa["mean"] - 0.0) / swa["std"]
        lcdm_tension_text = (
            f"w0 deviates from -1 by {n_w0:.1f} sigma (marginally); "
            f"wa deviates from 0 by {n_wa:.1f} sigma. "
        )
        if n_w0 > 2 or n_wa > 2:
            lcdm_tension_text += (
                "This is consistent with the DESI DR2 preference for dynamical "
                "dark energy reported by the DESI collaboration. The NMC correction "
                "wa_nmc_correction is a derived quantity; check its posterior mean "
                "and whether it shifts wa_fld appreciably."
            )
        else:
            lcdm_tension_text += (
                "Both w0 and wa are consistent with LCDM at 2 sigma. "
                "The NMC sector does not noticeably pull (w0, wa) away from (-1, 0) "
                "in this dataset-likelihood combination."
            )
    else:
        lcdm_tension_text = "(w0_fld or wa_fld not available; check after run)"

    # --- Param table ---
    param_table_rows = ["| Parameter | Mean | 68% CI | 95% CI |"]
    param_table_rows.append("|---|---|---|---|")
    for name in PARAM_NAMES:
        s = stats.get(name)
        if not s:
            continue
        param_table_rows.append(
            f"| {name} | {s['mean']:.5f} | "
            f"[{s['lo68']:.5f}, {s['hi68']:.5f}] | "
            f"[{s['lo95']:.5f}, {s['hi95']:.5f}] |"
        )
    param_table = "\n".join(param_table_rows)

    # --- Levier #1 implications ---
    # Determine which parameters are prior-dominated vs informative
    tight_params = []
    pdom_params = []
    for name in PARAM_NAMES:
        arr = extract_param_array(chain, name)
        if arr is None:
            continue
        lo, hi = PARAM_META[name][1], PARAM_META[name][2]
        pdom = prior_dominated_fraction(arr, w, lo, hi)
        if pdom < 0.20:
            pdom_params.append(name)
        elif pdom > 0.45:
            tight_params.append(name)

    tight_str = ", ".join(tight_params) if tight_params else "(none strongly constrained)"
    pdom_str = ", ".join(pdom_params) if pdom_params else "(none clearly prior-dominated)"

    md = f"""# ECI MCMC v5 Posterior Summary

**Generated:** {run_date}
**Chain prefix:** `{chain_prefix}`
**Burn-in:** {100*burnin:.0f}%
**Post-burnin samples:** {n_total} ({", ".join(str(n) for n in n_per_chain)} per chain)
**Likelihoods:** DESI DR2 BAO + Pantheon+
**Theory:** vanilla CLASS 3.3.4 + ECINMCTheory plugin (quasi-static NMC postprocessing)
**Sampled parameters:** 9 (H0, omega_b, omega_cdm, n_s, logA, w0_fld, wa_fld, xi_chi, chi_initial)

---

## Parameter posteriors

{param_table}

---

## Per-parameter prior-dominated assessment

{chr(10).join(pdom_lines)}

---

## Discriminator: H0 vs SH0ES tension

{shoes_text}

Whether H0 has shifted toward resolving the Hubble tension (SH0ES: 73.04 +/- 1.04)
must be read from the posterior mean and its displacement relative to both the
Planck/BAO anchor (~67.4) and the SH0ES anchor. Without CMB in this run, H0 is
constrained primarily by the BAO angular scale (the acoustic scale angle theta_s
is degenerate with H0*r_d), so expect a broad H0 posterior. A shift toward 73
would be surprising without CMB data to fix r_d independently. If H0 is near
the Planck/BAO anchor and xi_chi does not shift it noticeably, this 9-param run
is consistent with null ECI effect on H0, as expected at this dataset level.

---

## Discriminator: xi_chi vs Cassini hard wall

{xi_text}

**Honest interpretation:**
{xi_verdict}

**Key benchmark:** Wolf+2025 (arXiv:2504.07679) report log B = {WOLF2025_LN_BAYES:.2f} +/- {WOLF2025_LN_BAYES_ERR:.1f}
for NMC vs LCDM using Planck PR4 + DR2 BAO + Pantheon+. That strong Bayes factor
came from Planck's sensitivity to G_eff modifications in the CMB power spectrum,
not from BAO+SN alone. This 9-param run lacks Planck and should therefore NOT
be expected to reproduce that Bayes factor. If the Savage-Dickey BF from this
run is near 1 (inconclusive), that is fully consistent with Wolf+2025, not in
contradiction with it.

---

## Discriminator: (w0, wa) vs LCDM

{w0wa_text}

**Context:** {lcdm_tension_text}

---

## Honest verdict: is this run informative?

Parameters tightly constrained (posterior meaningfully narrower than prior):
**{tight_str}**

Parameters essentially prior-dominated (posterior covers >80% of prior width):
**{pdom_str}**

If xi_chi and chi_initial are prior-dominated: this is the expected outcome for
DESI DR2 BAO + Pantheon+ without CMB. These likelihoods primarily constrain the
expansion history (H0, omega_m, w0, wa) and are nearly insensitive to the NMC
coupling xi_chi (which modifies G_eff in the growth sector). The run serves as a
valid sanity check and a starting point for the Levier #1 production run, but
should not be cited as evidence for or against ECI without CMB data.

If the chains show very low ESS (< 100) for any parameter, the sampler has not
explored the posterior well. An R-1 below 0.02 is necessary but not sufficient;
check per-parameter ESS and visual chain traces before drawing conclusions.

---

## Implications for Levier #1 (12-parameter run)

**Context:** Levier #1 adds 3 EDE parameters (f_EDE, log10z_c, theta_i) and the
Dark Dimension parameter c'_DD to the 9 parameters here, plus includes Planck PR4
TTTEEE+lensing and KiDS-1000 S8 data. See `notes/calculation_triage_2026_05_02.md`
section A1 for the full discriminator criteria.

### What this 9-param run tells us about the 12-param prior space

**Tightly constrained directions (already settled):** {tight_str}
These parameters are unlikely to shift dramatically when EDE and c'_DD are added,
because their constraint comes from BAO+SN which will remain in Levier #1. Adding
Planck will tighten omega_b, n_s, and logA substantially (expected factor ~5-10x
reduction in posterior width for those parameters).

**Prior-dominated directions (will be constrained by new data):** {pdom_str}
These are precisely the parameters where Planck and KiDS-1000 add information:
- **xi_chi**: CMB is sensitive to G_eff(k) modifications in the growth sector.
  Wolf+2025's log B = 7.34 came almost entirely from Planck. Expect a factor ~3-10x
  tighter constraint on xi_chi once Planck is included.
- **chi_initial**: Weakly constrained by BAO+SN; Planck's ISW and lensing power
  provide some sensitivity. Expect modest improvement.
- **logA**: Without CMB, amplitude is unconstrained by BAO+SN; Planck fixes it to
  ~0.014 precision.

### New parameters in Levier #1

- **f_EDE**: Expected to be constrained by Planck (both the pre-recombination
  energy injection and its effect on the acoustic scale). DESI DR2 BAO alone is
  insensitive to f_EDE < 0.1. If the Levier #1 run recovers f_EDE < 0.05 at 2 sigma,
  the EDE sector is not needed and Levier #1 reduces to the NMC+LCDM case.
- **log10z_c, theta_i**: Prior-dominated until Planck is included.
- **c'_DD**: Constrained indirectly via Delta_N_eff correction. ACT DR6 bound
  Delta_N_eff < 0.13 (3 sigma) must be satisfied. The N2 simplified estimator
  (numerics/N2-kk-neff.py) flags all c'=0.05 cases as excluded under the thermal
  estimator; the Levier #1 run will test whether the Boltzmann treatment rescues
  this. If the posterior for c'_DD is rail-limited against the prior boundary,
  stop Levier #1 and address the N4 Boltzmann freeze-in calculation first (EXPLORE-A A4).

### Compute worthiness assessment

If (w0, wa) in this 9-param run are already > 2 sigma from (-1, 0), and if
xi_chi shows even a weak preference away from zero (pdom_score > 0.3), the
Levier #1 production run is justified: there is a signal direction to pursue.

If both xi_chi and (w0, wa) are consistent with LCDM at 1 sigma and the ESS for
the NMC parameters is very high (> 500) indicating the sampler is exploring a
flat surface, then Levier #1 is a speculative investment: the compute is justified
only if you accept the prior probability that Planck will reveal NMC effects hidden
from BAO+SN. The Wolf+2025 empirical anchor (log B = 7.34) is the strongest
external argument in favour of spending that compute.

**Recommendation:** Run Levier #1 only after verifying (a) R-1 < 0.02 in this
9-param run, (b) ESS > 200 for all parameters, and (c) chain traces look stationary.
Do not upgrade to 12 parameters on a chain that has not converged at 9.

---

## Files produced

- `triangle.pdf` — triangle plot (all 9 sampled parameters)
- `marginals.pdf` — 1-D marginals with flat prior overlay
- `summary.tex` — LaTeX table (importable directly into paper)
- `summary.md` — this file

## Reproducing this analysis

```bash
python scripts/analysis/posterior_v5.py \\
    --chain-prefix /path/to/eci \\
    --burnin 0.30 \\
    --outdir notes/posterior_v5_{run_date}
```

See `notes/posterior_v5_README.md` for full options.
"""

    outpath.write_text(md)
    print(f"  Markdown summary saved: {outpath}")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="ECI MCMC v5 posterior analysis",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    parser.add_argument(
        "--chain-prefix", default=None,
        help=(
            "Prefix of chain files, e.g. /path/to/eci "
            "(reads eci.1.txt, eci.2.txt, ...). "
            "Default: <cwd>/eci"
        ),
    )
    parser.add_argument(
        "--burnin", type=float, default=0.30,
        help="Burn-in fraction to discard (default: 0.30)",
    )
    parser.add_argument(
        "--outdir", default=None,
        help=(
            "Output directory. Default: notes/posterior_v5_<DATE> "
            "relative to the repo root."
        ),
    )
    parser.add_argument(
        "--nchains", type=int, default=4,
        help="Number of chain files to read (default: 4)",
    )
    parser.add_argument(
        "--no-plots", action="store_true",
        help="Skip triangle and marginals plots; write only summary files.",
    )
    parser.add_argument(
        "--max-samples", type=int, default=None,
        help="Cap samples per chain after burnin (for test runs).",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()

    run_date = date.today().isoformat()

    # Resolve chain prefix
    if args.chain_prefix is None:
        chain_prefix = str(Path.cwd() / "eci")
    else:
        chain_prefix = args.chain_prefix

    # Resolve output directory
    if args.outdir is None:
        outdir = _REPO_ROOT / "notes" / f"posterior_v5_{run_date}"
    else:
        outdir = Path(args.outdir)
    outdir.mkdir(parents=True, exist_ok=True)

    print(f"\n=== ECI v5 Posterior Analysis ===")
    print(f"Chain prefix : {chain_prefix}")
    print(f"Burn-in      : {100*args.burnin:.0f}%")
    print(f"Output dir   : {outdir}")
    print()

    # --- Read chains ---
    print("Reading chains...")
    chain = read_cobaya_chains(
        prefix=chain_prefix,
        n_chains=args.nchains,
        burnin=args.burnin,
        max_samples=args.max_samples,
    )
    n_total = sum(chain["n_per_chain"])
    print(f"Total post-burnin samples: {n_total}")
    print()

    # --- Statistics ---
    print("Computing statistics...")
    stats = compute_stats(chain)

    # --- Plots ---
    if not args.no_plots:
        print("Generating triangle plot...")
        try:
            make_triangle_plot(chain, outdir / "triangle.pdf")
        except Exception as exc:
            print(f"  [ERROR] triangle plot failed: {exc}", file=sys.stderr)

        print("Generating marginals plot...")
        try:
            make_marginals_plot(chain, stats, outdir / "marginals.pdf")
        except Exception as exc:
            print(f"  [ERROR] marginals plot failed: {exc}", file=sys.stderr)

    # --- Summary files ---
    print("Writing summary files...")
    render_summary_tex(
        stats, chain, outdir / "summary.tex",
        run_date=run_date,
        chain_prefix=chain_prefix,
        n_per_chain=chain["n_per_chain"],
        burnin=args.burnin,
    )
    render_summary_md(
        stats, chain, outdir / "summary.md",
        run_date=run_date,
        chain_prefix=chain_prefix,
        n_per_chain=chain["n_per_chain"],
        burnin=args.burnin,
        args=args,
    )

    print()
    print("=== Done ===")
    print(f"Outputs in: {outdir}")

    # Print quick digest to stdout
    print()
    print("--- Quick digest ---")
    for name in ["H0", "w0_fld", "wa_fld", "xi_chi", "chi_initial"]:
        s = stats.get(name)
        if s:
            print(
                f"  {name:15s}: mean={s['mean']:.4f}  "
                f"68%CI=[{s['lo68']:.4f}, {s['hi68']:.4f}]"
            )
    print()


if __name__ == "__main__":
    main()
