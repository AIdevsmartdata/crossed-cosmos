"""M103 — COMPUTE BAYES FACTORS from nested sampling results

Loads 5 ns_{MODEL}_result.pkl files, computes:
  - log Z and SE for each model
  - Bayes factors BF(M_i / LCDM) for i in {ECI, Wolf, Karam, DESI}
  - Jeffreys-scale interpretation
  - Cross-check against M96 bridge sampling divergence flags

Jeffreys (1961) scale for |ln BF|:
  < 1.0  : inconclusive
  1.0-2.5: weak evidence
  2.5-5.0: moderate evidence
  > 5.0  : strong evidence

References:
  - dynesty: Speagle (2019) arXiv:1904.02180, MNRAS staa278
  - Jeffreys (1961) "Theory of Probability" Oxford Univ. Press
  - Kass & Raftery (1995) J. Amer. Statist. Assoc. 90(430):773-795
"""

import pickle
import os
import sys
import numpy as np

RESULT_DIR = "/home/remondiere/pc_calcs"
OUTPUT_DIR = os.path.dirname(os.path.abspath(__file__))

# M96 bridge sampling divergence rates (from c4_v5_overnight.py NUTS run)
M96_DIVERGENCE = {
    "LCDM":          0.00,
    "ECI_NMC":       65.40,
    "Wolf_NMC":      38.73,
    "Karam_Palatini": 74.96,
    "DESI_w0wa":     45.03,
}

# M96 NUTS posterior means (for consistency cross-check)
M96_POSTERIORS = {
    "LCDM":           {"H0": 68.957, "obh2": 0.02250, "och2": 0.11950},
    "ECI_NMC":        {"H0": 64.042, "obh2": 0.02240, "och2": 0.11200, "xi": 0.0004, "lambda": 1.298},
    "Wolf_NMC":       {"H0": 64.538, "obh2": 0.02250, "och2": 0.11300, "xi": -3.120, "lambda": 0.582},
    "Karam_Palatini": {"H0": 64.370, "obh2": 0.02240, "och2": 0.11200, "xi": -0.914, "lambda": 1.102,
                        "xi_eff_factor": 0.308},
    "DESI_w0wa":      {"H0": 64.637, "obh2": 0.02250, "och2": 0.12500, "w0": -0.423, "wa": -1.877},
}

# ---------------------------------------------------------------------------
# Jeffreys scale
# ---------------------------------------------------------------------------
def jeffreys_interpretation(ln_bf):
    """Interpret ln(BF) on Kass-Raftery (1995) / Jeffreys (1961) scale."""
    abs_lnbf = abs(ln_bf)
    if abs_lnbf < 1.0:
        strength = "inconclusive"
    elif abs_lnbf < 2.5:
        strength = "weak"
    elif abs_lnbf < 5.0:
        strength = "moderate"
    else:
        strength = "strong"
    if ln_bf > 0:
        direction = f"favors model over LCDM ({strength})"
    elif ln_bf < 0:
        direction = f"favors LCDM over model ({strength})"
    else:
        direction = "no preference"
    return strength, direction

# ---------------------------------------------------------------------------
# Load results
# ---------------------------------------------------------------------------
MODEL_NAMES = ["LCDM", "ECI_NMC", "Wolf_NMC", "Karam_Palatini", "DESI_w0wa"]

def load_results():
    results = {}
    missing = []
    for name in MODEL_NAMES:
        path = os.path.join(RESULT_DIR, f"ns_{name}_result.pkl")
        if not os.path.exists(path):
            missing.append(name)
            continue
        with open(path, "rb") as f:
            r = pickle.load(f)
        results[name] = r
        if r.get("status") != "complete":
            print(f"WARNING: {name} status = {r.get('status')} — may be incomplete")
    return results, missing

# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
def main():
    print("=" * 72)
    print("M103 BAYES FACTORS — nested sampling evidence computation")
    print("=" * 72)

    results, missing = load_results()

    if missing:
        print(f"\nMISSING models (nested sampling not yet complete): {missing}")
        if "LCDM" in missing:
            print("ERROR: LCDM reference model missing. Cannot compute Bayes factors.")
            sys.exit(1)
        print("Will compute partial Bayes factors for available models.\n")

    # -----------------------------------------------------------------------
    # Table 1: log Z values
    # -----------------------------------------------------------------------
    print("\n--- TABLE 1: log Z (Bayesian Evidence) ---\n")
    print(f"{'Model':<20} {'ndim':>5} {'nlive':>6} {'niter':>7} "
          f"{'log Z':>10} {'±SE':>8} {'elapsed':>10}  M96_div%")
    print("-" * 80)

    logz_values = {}
    logz_errors = {}

    for name in MODEL_NAMES:
        if name not in results:
            print(f"{name:<20}  [NOT AVAILABLE]")
            continue
        r = results[name]
        logz = r["logz"]
        logz_err = r["logz_err"]
        ndim = r.get("ndim", "?")
        nlive = r.get("nlive", "?")
        niter = r.get("n_iter", "?")
        elapsed = r.get("elapsed_sec", 0)
        div_pct = M96_DIVERGENCE.get(name, float("nan"))
        print(f"{name:<20} {ndim:>5} {nlive:>6} {niter:>7} "
              f"{logz:>10.4f} {logz_err:>8.4f} {elapsed:>9.1f}s  {div_pct:>6.1f}%")
        logz_values[name] = logz
        logz_errors[name] = logz_err

    # -----------------------------------------------------------------------
    # Table 2: Bayes factors vs LCDM
    # -----------------------------------------------------------------------
    if "LCDM" not in logz_values:
        print("\nCannot compute Bayes factors: LCDM missing.")
        return

    logz_ref = logz_values["LCDM"]
    logz_ref_err = logz_errors["LCDM"]

    print("\n--- TABLE 2: Bayes Factors BF(M_i / LCDM) ---\n")
    print(f"  ln BF = log Z(M_i) - log Z(LCDM)  [LCDM: log Z = {logz_ref:.4f} ± {logz_ref_err:.4f}]")
    print(f"  BF > 1 (ln BF > 0): data prefer M_i over LCDM\n")
    print(f"{'Model':<20} {'ln BF':>10} {'±SE':>8} {'BF':>12}  Jeffreys")
    print("-" * 78)

    for name in ["ECI_NMC", "Wolf_NMC", "Karam_Palatini", "DESI_w0wa"]:
        if name not in logz_values:
            print(f"{name:<20}  [NOT AVAILABLE]")
            continue
        ln_bf = logz_values[name] - logz_ref
        # Error propagation: quadrature sum of both SE estimates
        se_bf = np.sqrt(logz_errors[name]**2 + logz_ref_err**2)
        bf = np.exp(ln_bf)
        strength, direction = jeffreys_interpretation(ln_bf)
        print(f"{name:<20} {ln_bf:>10.4f} {se_bf:>8.4f} {bf:>12.4f}  {direction}")

    # -----------------------------------------------------------------------
    # Table 3: Posterior cross-check vs M96
    # -----------------------------------------------------------------------
    print("\n--- TABLE 3: Posterior means — NS vs M96 NUTS (consistency check) ---\n")
    print(f"{'Model/Param':<30} {'NS mean':>12} {'M96 mean':>12} {'delta/sigma':>12}")
    print("-" * 70)

    for name in MODEL_NAMES:
        if name not in results:
            continue
        r = results[name]
        ns_means = r.get("posterior_means", {})
        ns_stds = r.get("posterior_stds", {})
        m96 = M96_POSTERIORS.get(name, {})
        div_pct = M96_DIVERGENCE.get(name, 0)

        # Note on M96 reliability
        if div_pct > 10:
            print(f"  [{name}] M96 divergence={div_pct:.1f}% → M96 posteriors unreliable; NS is authoritative")
        print(f"  [{name}]")
        for pname in r.get("param_names", []):
            ns_m = ns_means.get(pname, float("nan"))
            ns_s = ns_stds.get(pname, 1.0)
            m96_m = m96.get(pname, float("nan"))
            if np.isnan(m96_m):
                print(f"    {pname:<26} {ns_m:>12.5f} {'N/A':>12}")
            else:
                delta_sigma = (ns_m - m96_m) / max(ns_s, 1e-10)
                flag = "  *** TENSION ***" if abs(delta_sigma) > 2.0 else ""
                print(f"    {pname:<26} {ns_m:>12.5f} {m96_m:>12.5f} {delta_sigma:>12.2f}σ{flag}")

    # -----------------------------------------------------------------------
    # Summary verdict
    # -----------------------------------------------------------------------
    print("\n--- VERDICT ---\n")
    print("Nested sampling log Z values are divergence-free (unlike M96 NUTS).")
    print("M96 divergence flags: ECI 65%, Wolf 39%, Karam 75%, DESI_w0wa 45%")
    print("→ M96 bridge evidences were upper bounds only; NS results are authoritative.\n")

    for name in ["ECI_NMC", "Wolf_NMC", "Karam_Palatini", "DESI_w0wa"]:
        if name not in logz_values:
            continue
        ln_bf = logz_values[name] - logz_ref
        se_bf = np.sqrt(logz_errors[name]**2 + logz_ref_err**2)
        strength, direction = jeffreys_interpretation(ln_bf)
        print(f"  {name}: ln BF = {ln_bf:+.4f} ± {se_bf:.4f}  → {direction}")

    # -----------------------------------------------------------------------
    # Save summary to text file
    # -----------------------------------------------------------------------
    summary_path = os.path.join(OUTPUT_DIR, "bayes_factors_results.txt")
    with open(summary_path, "w") as f:
        f.write("M103 BAYES FACTORS — nested sampling\n")
        f.write(f"Generated: {__import__('time').strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write("=" * 72 + "\n\n")
        f.write("log Z values:\n")
        for name in MODEL_NAMES:
            if name in logz_values:
                f.write(f"  {name}: log Z = {logz_values[name]:.4f} ± {logz_errors[name]:.4f}\n")
        f.write("\nBayes factors vs LCDM:\n")
        for name in ["ECI_NMC", "Wolf_NMC", "Karam_Palatini", "DESI_w0wa"]:
            if name in logz_values:
                ln_bf = logz_values[name] - logz_ref
                se_bf = np.sqrt(logz_errors[name]**2 + logz_ref_err**2)
                bf = np.exp(ln_bf)
                strength, direction = jeffreys_interpretation(ln_bf)
                f.write(f"  {name}: ln BF = {ln_bf:+.4f} ± {se_bf:.4f}  BF = {bf:.4f}  [{direction}]\n")
    print(f"\nSummary saved to: {summary_path}")

if __name__ == "__main__":
    main()
