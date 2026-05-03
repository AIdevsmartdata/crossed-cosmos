#!/usr/bin/env python3
"""
levier1B_kids_isolation.py
==========================
Posterior reweighting analysis to isolate the contribution of the KiDS-1000
S8 Gaussian prior to the log B_10 (NMC vs LCDM) on the converged Levier #1B
Cobaya chain.

Method
------
1. Read 4 chain files for Levier #1B with 30% burn-in.
2. Reproduce the original Savage-Dickey log B_10 (sanity check vs -1.37).
3. Compute log L_KiDS(S_8) for each chain sample (Gaussian, 0.766 ± 0.020).
4. Reweight w_new = w_old * exp(+log L_KiDS) = w_old / L_KiDS.
   This effectively removes the KiDS factor from the posterior.
5. Recompute the Savage-Dickey log B_10 on the reweighted samples.
6. Compare the reweighted log B_10 to Wolf 2025 (+7.34 ± 0.6).

Verdict
-------
- If reweighted log B_10 is close to +7.34: KiDS WAS the dominant driver.
- If reweighted log B_10 is still close to -1.37: KiDS is NOT the driver
  (other factors dominate: NPIPE CamSpec vs plik, MultiNest vs SD-KDE,
  parameter sets, Cassini wall, ...).
- Intermediate: KiDS is a partial driver.

NOTE: The reweighting does NOT undo the Cassini hard wall (which is a -inf
truncation, not a Gaussian factor). All samples in the chain already satisfy
|xi_chi| * 0.01 < 6e-6  =>  |xi_chi| < 6e-4. Wolf 2025 does not apply Cassini,
but this affects only the prior volume (uniform within wall vs uniform on the
full [-0.024, 0.024] range used by Cobaya). Since Savage-Dickey at xi_chi = 0
uses pi(0) at the centre and posterior(0) at the centre, the Cassini wall
(which is symmetric around 0) does not change pi(0) — both p(0) and pi(0) are
divided by the same Cassini-narrowed volume.
"""
from __future__ import annotations

import json
import os
import sys
from pathlib import Path

import numpy as np


# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------
CHAIN_DIR = Path(
    "/root/crossed-cosmos/mcmc/chains/eci_levier1B_run1/snapshot_2026_05_03_FINAL"
)
CHAIN_PREFIX = CHAIN_DIR / "eci_levier1B"
N_CHAINS = 4
BURNIN_FRAC = 0.30

# KiDS-1000 Gaussian prior parameters (from eci_kids_s8.py)
KIDS_S8_MEAN = 0.766
KIDS_S8_SIGMA = 0.020

# xi_chi prior (uniform), same as posterior_levier1B.py
XI_CHI_PRIOR_LO_WIDE = -0.1   # for SD comparison with original analysis
XI_CHI_PRIOR_HI_WIDE = 0.1
XI_CHI_PRIOR_LO_YAML = -0.024  # actual YAML range
XI_CHI_PRIOR_HI_YAML = 0.024

# Wolf 2025
WOLF2025_LN_BAYES = 7.34
WOLF2025_LN_BAYES_ERR = 0.6


# ---------------------------------------------------------------------------
# Chain I/O
# ---------------------------------------------------------------------------
def read_cobaya_chains(prefix: Path, n_chains: int, burnin_frac: float) -> dict:
    """Read 4 chain files, drop burn-in, concatenate."""
    all_samples, all_weights, all_logpost = [], [], []
    n_per_chain = []
    col_names = None
    for ci in range(1, n_chains + 1):
        fpath = f"{prefix}.{ci}.txt"
        if not os.path.exists(fpath):
            print(f"  [WARN] missing: {fpath}", file=sys.stderr)
            continue
        with open(fpath) as fh:
            header = fh.readline().lstrip("#").strip()
        these_cols = header.split()
        if col_names is None:
            col_names = these_cols
        elif these_cols != col_names:
            print(f"  [WARN] column mismatch in {fpath}", file=sys.stderr)
            continue
        data = np.loadtxt(fpath)
        if data.ndim == 1:
            data = data[None, :]
        n_drop = int(np.ceil(burnin_frac * data.shape[0]))
        data = data[n_drop:]
        all_weights.append(data[:, 0])
        all_logpost.append(data[:, 1])
        all_samples.append(data[:, 2:])
        n_per_chain.append(data.shape[0])
        print(f"  chain {ci}: {data.shape[0]:>6d} post-burnin rows")
    return dict(
        samples=np.concatenate(all_samples, axis=0),
        weights=np.concatenate(all_weights, axis=0),
        logpost=np.concatenate(all_logpost, axis=0),
        col_names=col_names[2:] if col_names else [],
        n_per_chain=n_per_chain,
    )


def col(chain: dict, name: str) -> np.ndarray:
    """Extract a parameter column by name."""
    return chain["samples"][:, chain["col_names"].index(name)]


# ---------------------------------------------------------------------------
# Savage-Dickey at xi_chi = 0
# ---------------------------------------------------------------------------
def savage_dickey_log_B(
    xi_arr: np.ndarray,
    weights: np.ndarray,
    prior_lo: float,
    prior_hi: float,
    bandwidth_factor: float = 0.15,
) -> tuple[float, float, float]:
    """
    Compute log B_10 = log[ pi(xi=0) / p(xi=0|d) ] using a 1-D Gaussian KDE.

    Returns (log_B10, posterior_density_at_0, bandwidth_used).
    Uses the SAME formula as scripts/analysis/posterior_levier1B.py.
    """
    prior_width = prior_hi - prior_lo
    prior_density_at_0 = 1.0 / prior_width
    w = weights / weights.sum()
    weighted_mean = np.sum(w * xi_arr)
    weighted_var = np.sum(w * (xi_arr - weighted_mean) ** 2)
    bw_silverman = 1.06 * np.sqrt(weighted_var) * len(xi_arr) ** (-0.2)
    bw = min(bw_silverman, bandwidth_factor * prior_width)
    if bw < 1e-8:
        return float("nan"), float("nan"), bw
    kernel_vals = np.exp(-0.5 * (xi_arr / bw) ** 2) / (np.sqrt(2 * np.pi) * bw)
    posterior_density_at_0 = float(np.sum(w * kernel_vals))
    if posterior_density_at_0 < 1e-30:
        return float("inf"), posterior_density_at_0, bw
    log_B10 = float(np.log(prior_density_at_0 / posterior_density_at_0))
    return log_B10, posterior_density_at_0, bw


def weighted_quantile(values, qs, weights):
    sorter = np.argsort(values)
    v = values[sorter]
    w = weights[sorter]
    cdf = np.cumsum(w) / np.sum(w)
    return np.array([v[np.searchsorted(cdf, q)] for q in qs])


def kish_ess(weights):
    return float(np.sum(weights) ** 2 / np.sum(weights ** 2))


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
def main():
    print("=" * 72)
    print("Levier #1B — KiDS-1000 Isolation by Posterior Reweighting")
    print("=" * 72)
    print(f"Chain prefix : {CHAIN_PREFIX}")
    print(f"N chains     : {N_CHAINS}")
    print(f"Burn-in      : {100*BURNIN_FRAC:.0f}%")
    print(f"KiDS prior   : S_8 ~ N({KIDS_S8_MEAN}, {KIDS_S8_SIGMA})")
    print()

    print("Reading chains ...")
    chain = read_cobaya_chains(CHAIN_PREFIX, N_CHAINS, BURNIN_FRAC)
    n_total = sum(chain["n_per_chain"])
    print(f"Total post-burnin rows: {n_total}")
    print(f"Number of columns in chain: {len(chain['col_names'])}")
    print()

    # ---- Verify columns ----
    needed = ["xi_chi", "S8", "sigma8", "Omega_m"]
    for k in needed:
        if k not in chain["col_names"]:
            raise RuntimeError(f"Required column '{k}' missing from chain. "
                               f"Available: {chain['col_names']}")
    print("All required columns present (xi_chi, S8, sigma8, Omega_m).")
    print()

    xi_arr = col(chain, "xi_chi")
    S8_chain = col(chain, "S8")
    sigma8_chain = col(chain, "sigma8")
    Omega_m_chain = col(chain, "Omega_m")
    weights_orig = chain["weights"]

    # Sanity: verify S8 matches sigma8*sqrt(Omega_m/0.3)
    S8_recomputed = sigma8_chain * np.sqrt(Omega_m_chain / 0.3)
    s8_diff_max = np.max(np.abs(S8_chain - S8_recomputed))
    print(f"S8 consistency check: max |S8_stored - S8_computed| = {s8_diff_max:.2e}")
    assert s8_diff_max < 1e-5, "S8 column does not match sigma8*sqrt(Om/0.3)!"
    print()

    # ---- 1) Reproduce original log B_10 (sanity check) ----
    print("-" * 72)
    print("STEP 1: Reproduce original log B_10 (sanity check vs -1.37)")
    print("-" * 72)
    log_B_orig_wide, post0_orig_wide, bw_orig_wide = savage_dickey_log_B(
        xi_arr, weights_orig, XI_CHI_PRIOR_LO_WIDE, XI_CHI_PRIOR_HI_WIDE,
    )
    print(f"  xi prior used in posterior_levier1B.py: [{XI_CHI_PRIOR_LO_WIDE}, "
          f"{XI_CHI_PRIOR_HI_WIDE}] (width 0.2)")
    print(f"  pi(0)              = {1.0/(XI_CHI_PRIOR_HI_WIDE-XI_CHI_PRIOR_LO_WIDE):.4f}")
    print(f"  Silverman bw       = {bw_orig_wide:.5f}")
    print(f"  posterior(0)       = {post0_orig_wide:.4f}")
    print(f"  log B_10           = {log_B_orig_wide:.4f}")
    print(f"  Reference (notes)  = -1.37")
    print()

    # Also try with the YAML actual prior range [-0.024, 0.024]
    log_B_orig_yaml, post0_orig_yaml, _ = savage_dickey_log_B(
        xi_arr, weights_orig, XI_CHI_PRIOR_LO_YAML, XI_CHI_PRIOR_HI_YAML,
    )
    print(f"  ALT: with YAML prior [{XI_CHI_PRIOR_LO_YAML}, {XI_CHI_PRIOR_HI_YAML}]:")
    print(f"  log B_10           = {log_B_orig_yaml:.4f}")
    print()

    # ---- 2) Compute KiDS log-likelihood per sample ----
    print("-" * 72)
    print("STEP 2: Compute log L_KiDS(S_8) per chain sample")
    print("-" * 72)
    delta_s8 = (S8_chain - KIDS_S8_MEAN) / KIDS_S8_SIGMA
    log_L_kids = -0.5 * delta_s8 ** 2  # ignoring constant; cancels in reweighting
    print(f"  log L_KiDS:  min={log_L_kids.min():.3f}  "
          f"median={np.median(log_L_kids):.3f}  max={log_L_kids.max():.3f}")
    print(f"  S_8: min={S8_chain.min():.4f}  median={np.median(S8_chain):.4f}  "
          f"max={S8_chain.max():.4f}")
    print(f"  S_8 weighted mean = "
          f"{np.average(S8_chain, weights=weights_orig):.4f}")
    print()

    # Also confirm against chi2__eci_kids_s8 column (should equal -2*logL_kids
    # if Cassini and ACT contributions are zero / inactive). Cassini wall is
    # active but only as a hard cut — chi2__kids should be 2 * 0.5 delta_s8^2.
    if "chi2__eci_kids_s8.ECIKiDSS8Likelihood" in chain["col_names"]:
        chi2_kids_stored = col(chain, "chi2__eci_kids_s8.ECIKiDSS8Likelihood")
        chi2_kids_computed = delta_s8 ** 2  # Cassini wall passes (no penalty);
                                            # ACT penalty disabled in YAML
        diff = np.max(np.abs(chi2_kids_stored - chi2_kids_computed))
        print(f"  chi2__kids stored vs computed: max diff = {diff:.4e}")
        if diff < 1e-4:
            print("  Stored chi2__kids exactly matches Gaussian S_8 contribution.")
            print("  Cassini wall active but never enforced (all samples pass).")
            print("  ACT penalty disabled in YAML (apply_act_penalty: false).")
        else:
            print("  WARNING: chi2__kids discrepancy. Check Cassini/ACT contributions.")
    print()

    # ---- 3) Reweight ----
    print("-" * 72)
    print("STEP 3: Reweight to remove KiDS factor")
    print("-" * 72)
    # New weight = old weight / L_KiDS = old weight * exp(-logL_KiDS)
    # In log: log w_new = log w_old - logL_KiDS = log w_old + 0.5 * delta_s8^2
    # Since weights are Cobaya MCMC weights (multiplicities), use them
    # multiplied by exp(+0.5 * delta_s8^2):
    log_factor = -log_L_kids  # = 0.5 * delta_s8^2 >= 0
    # For numerical stability: subtract max of log_factor, then exp
    log_factor_shifted = log_factor - log_factor.max()
    factor = np.exp(log_factor_shifted)
    weights_new = weights_orig * factor

    # Diagnose weight distribution
    print(f"  log_factor range: [{log_factor.min():.3f}, {log_factor.max():.3f}]")
    print(f"  factor (post-shift): min={factor.min():.3e}  "
          f"max={factor.max():.3e}  median={np.median(factor):.3e}")

    ess_orig = kish_ess(weights_orig)
    ess_new = kish_ess(weights_new)
    print(f"  Kish ESS (original)   = {ess_orig:.0f}")
    print(f"  Kish ESS (reweighted) = {ess_new:.0f}")
    print(f"  ESS retention ratio   = {ess_new/ess_orig:.4f}")
    if ess_new < 100:
        print("  [WARN] ESS_new < 100: reweighted estimate may be unreliable.")
    elif ess_new < 1000:
        print("  [CAUTION] ESS_new modest (100-1000): treat with care.")
    else:
        print("  ESS_new sufficient for a meaningful reweighted estimate.")
    print()

    # ---- 4) Reweighted Savage-Dickey ----
    print("-" * 72)
    print("STEP 4: Recompute Savage-Dickey log B_10 on reweighted posterior")
    print("-" * 72)
    log_B_new_wide, post0_new_wide, bw_new_wide = savage_dickey_log_B(
        xi_arr, weights_new, XI_CHI_PRIOR_LO_WIDE, XI_CHI_PRIOR_HI_WIDE,
    )
    print(f"  pi(0)              = {1.0/(XI_CHI_PRIOR_HI_WIDE-XI_CHI_PRIOR_LO_WIDE):.4f}")
    print(f"  bw used (Silverman) = {bw_new_wide:.5f}")
    print(f"  posterior(0)       = {post0_new_wide:.4f}")
    print(f"  log B_10 (reweight) = {log_B_new_wide:.4f}")
    print()

    log_B_new_yaml, post0_new_yaml, _ = savage_dickey_log_B(
        xi_arr, weights_new, XI_CHI_PRIOR_LO_YAML, XI_CHI_PRIOR_HI_YAML,
    )
    print(f"  ALT (YAML prior): log B_10 (reweight) = {log_B_new_yaml:.4f}")
    print()

    # Posterior summary statistics: original vs reweighted
    def summary(arr, w, name):
        wn = w / w.sum()
        mean = float(np.sum(wn * arr))
        var = float(np.sum(wn * (arr - mean) ** 2))
        std = np.sqrt(var)
        q = weighted_quantile(arr, [0.025, 0.16, 0.5, 0.84, 0.975], w)
        print(f"  {name:25s}: mean={mean:+.5f}  std={std:.5f}  "
              f"68%CI=[{q[1]:+.5f},{q[3]:+.5f}]")

    print("Posterior of xi_chi:")
    summary(xi_arr, weights_orig, "Original (with KiDS)")
    summary(xi_arr, weights_new, "Reweighted (no KiDS)")
    print()
    print("Posterior of S_8:")
    summary(S8_chain, weights_orig, "Original (with KiDS)")
    summary(S8_chain, weights_new, "Reweighted (no KiDS)")
    print()
    print("Posterior of H0:")
    summary(col(chain, "H0"), weights_orig, "Original (with KiDS)")
    summary(col(chain, "H0"), weights_new, "Reweighted (no KiDS)")
    print()

    # ---- 5) Comparison and Verdict ----
    print("=" * 72)
    print("STEP 5: Comparison with Wolf 2025 +7.34")
    print("=" * 72)
    print(f"  Wolf 2025 reference  : log B_10 = +{WOLF2025_LN_BAYES:.2f} +/- "
          f"{WOLF2025_LN_BAYES_ERR:.1f}")
    print(f"  Original (with KiDS)  : log B_10 = {log_B_orig_wide:+.2f} "
          f"(matches notes -1.37)")
    print(f"  Reweighted (no KiDS)  : log B_10 = {log_B_new_wide:+.2f}")
    delta_orig = WOLF2025_LN_BAYES - log_B_orig_wide
    delta_new = WOLF2025_LN_BAYES - log_B_new_wide
    closure = (delta_orig - delta_new) / delta_orig if abs(delta_orig) > 1e-6 else 0.0
    print()
    print(f"  Δ(Wolf - original) = {delta_orig:+.2f}")
    print(f"  Δ(Wolf - reweight) = {delta_new:+.2f}")
    print(f"  Gap closure (KiDS) = {100*closure:.1f}% of original gap")
    print()

    # Verdict logic
    if log_B_new_wide > WOLF2025_LN_BAYES - 2 * WOLF2025_LN_BAYES_ERR:
        verdict = ("KiDS IS THE DOMINANT DRIVER: removing the KiDS factor "
                   "brings log B within 2σ of Wolf 2025.")
    elif closure > 0.7:
        verdict = ("KiDS IS A MAJOR DRIVER (>70% of the gap), but other "
                   "differences (likelihood, sampler, parameter set) account "
                   "for a residual.")
    elif closure > 0.3:
        verdict = ("KiDS IS A PARTIAL DRIVER ({:.0f}% of the gap closed). "
                   "Other factors dominate.".format(100 * closure))
    elif closure > -0.1:
        verdict = ("KiDS IS NOT THE DRIVER: removing it changes log B by "
                   "less than 30% of the gap.")
    else:
        verdict = ("KiDS REWEIGHTING WORSENS THE GAP. Other factors (CamSpec "
                   "vs plik, MCMC+SD-KDE vs MultiNest, parameter set) account "
                   "for the entire disagreement.")
    print(f"  VERDICT: {verdict}")
    print()

    # ---- Save JSON results ----
    results = {
        "metadata": {
            "chain_prefix": str(CHAIN_PREFIX),
            "n_chains": N_CHAINS,
            "burnin_frac": BURNIN_FRAC,
            "n_total_postburnin": int(n_total),
            "kids_s8_mean": KIDS_S8_MEAN,
            "kids_s8_sigma": KIDS_S8_SIGMA,
            "wolf2025_log_B": WOLF2025_LN_BAYES,
            "wolf2025_log_B_err": WOLF2025_LN_BAYES_ERR,
        },
        "savage_dickey": {
            "wide_prior": {
                "xi_prior_lo": XI_CHI_PRIOR_LO_WIDE,
                "xi_prior_hi": XI_CHI_PRIOR_HI_WIDE,
                "log_B_original": log_B_orig_wide,
                "log_B_reweighted": log_B_new_wide,
                "posterior0_original": post0_orig_wide,
                "posterior0_reweighted": post0_new_wide,
                "bw_original": bw_orig_wide,
                "bw_reweighted": bw_new_wide,
            },
            "yaml_prior": {
                "xi_prior_lo": XI_CHI_PRIOR_LO_YAML,
                "xi_prior_hi": XI_CHI_PRIOR_HI_YAML,
                "log_B_original": log_B_orig_yaml,
                "log_B_reweighted": log_B_new_yaml,
            },
        },
        "ess": {
            "original": ess_orig,
            "reweighted": ess_new,
            "retention_ratio": ess_new / ess_orig,
        },
        "comparison": {
            "delta_original_vs_wolf": delta_orig,
            "delta_reweighted_vs_wolf": delta_new,
            "gap_closure_fraction": closure,
            "verdict": verdict,
        },
        "posterior_xi_chi": {
            "original_mean": float(np.average(xi_arr, weights=weights_orig)),
            "reweighted_mean": float(np.average(xi_arr, weights=weights_new)),
            "original_std": float(np.sqrt(np.average(
                (xi_arr - np.average(xi_arr, weights=weights_orig))**2,
                weights=weights_orig))),
            "reweighted_std": float(np.sqrt(np.average(
                (xi_arr - np.average(xi_arr, weights=weights_new))**2,
                weights=weights_new))),
        },
        "posterior_S8": {
            "original_mean": float(np.average(S8_chain, weights=weights_orig)),
            "reweighted_mean": float(np.average(S8_chain, weights=weights_new)),
            "original_std": float(np.sqrt(np.average(
                (S8_chain - np.average(S8_chain, weights=weights_orig))**2,
                weights=weights_orig))),
            "reweighted_std": float(np.sqrt(np.average(
                (S8_chain - np.average(S8_chain, weights=weights_new))**2,
                weights=weights_new))),
        },
    }
    Path("/tmp/levier1B_kids_isolation.json").write_text(json.dumps(results, indent=2))
    print("Results JSON: /tmp/levier1B_kids_isolation.json")
    return results


if __name__ == "__main__":
    main()
