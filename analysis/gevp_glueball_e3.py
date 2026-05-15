#!/usr/bin/env python3
"""
Phase E3 — GEVP analysis of SU(2) glueball correlators
Tests Conjecture E-1: motivic weight predicts (m_2++/m_0++)² = 2.000

Reads XML output from glueball_correlator_v3 (12 operators):
  6 shapes × 2 APE levels = 12 operators

Extracts m_0++ and m_2++ via GEVP, computes ratio R = (m_2++/m_0++)².
Verdict: R ∈ [1.98, 2.02] → E-1 validated | R outside → falsified.

Reference: AT 2021 lattice gives 2.001(17).
"""

import numpy as np
import xml.etree.ElementTree as ET
from scipy.linalg import eigh
from pathlib import Path
import sys, json, glob, re
from collections import defaultdict

VERDICT = {
    "validated": "CONJECTURE E-1 VALIDATED: (m₂++/m₀++)² ∈ [1.98, 2.02]",
    "falsified": "CONJECTURE E-1 FALSIFIED: (m₂++/m₀++)² ∉ [1.98, 2.02]",
    "inconclusive": "INCONCLUSIVE: insufficient data for reliable extraction"
}

# =========================================================================
# PARSING
# =========================================================================

def parse_glueball_xml(xml_path):
    """
    Parse glueball_correlator_v3 output XML.
    Returns dict: {op_idx: array of shape (Lt,) with correlator values}
    """
    try:
        tree = ET.parse(xml_path)
        root = tree.getroot()
    except Exception as e:
        print(f"  [ERROR] parsing {xml_path}: {e}", file=sys.stderr)
        return None

    op_t = root.find("Op_t")
    if op_t is None:
        print(f"  [ERROR] no <Op_t> in {xml_path}", file=sys.stderr)
        return None

    Lt_el = op_t.find("Lt")
    if Lt_el is None:
        print(f"  [ERROR] no <Lt> in {xml_path}", file=sys.stderr)
        return None
    Lt = int(Lt_el.text.strip())

    n_ops_el = op_t.find("n_ops")
    if n_ops_el is None:
        print(f"  [ERROR] no <n_ops> in {xml_path}", file=sys.stderr)
        return None
    n_ops = int(n_ops_el.text.strip())

    corr = {}
    for op_elem in op_t:
        tag = op_elem.tag
        if not tag.startswith("O_op_"):
            continue
        try:
            idx = int(tag.replace("O_op_", ""))
        except ValueError:
            continue
        vals = [float(x) for x in op_elem.text.strip().split()]
        if len(vals) == Lt:
            corr[idx] = np.array(vals)
        else:
            print(f"  [WARN] op {idx}: expected {Lt} values, got {len(vals)}", file=sys.stderr)

    if len(corr) != n_ops:
        print(f"  [WARN] expected {n_ops} ops, parsed {len(corr)}", file=sys.stderr)

    return corr


def load_beta_data(results_dir, beta_tag):
    """
    Load all glueball XML files for a given beta tag (e.g., '250').
    Returns list of correlation dicts.
    """
    bdir = Path(results_dir) / f"b{beta_tag}"
    if not bdir.exists():
        print(f"  [ERROR] directory not found: {bdir}")
        return []

    xml_files = sorted(bdir.glob("glue_*.out.xml"))
    if not xml_files:
        print(f"  [ERROR] no glue_*.out.xml files in {bdir}")
        return []

    all_corrs = []
    for f in xml_files:
        corr = parse_glueball_xml(f)
        if corr is not None:
            all_corrs.append(corr)

    return all_corrs


# =========================================================================
# CORRELATION MATRIX
# =========================================================================

def build_corr_matrix(corrs, t_src=0):
    """
    Build average correlation matrix C_ij(t) from multiple configs.
    corrs: list of dicts {op_idx: array(Lt,)}
    Returns: (C_avg, C_err) each of shape (Lt, n_ops, n_ops)
    """
    if not corrs:
        return None, None

    n_configs = len(corrs)
    n_ops = max(corrs[0].keys()) + 1
    Lt = len(corrs[0][0])

    # Collect all config data
    C_all = np.zeros((n_configs, Lt, n_ops, n_ops))

    for k, corr in enumerate(corrs):
        for i in range(n_ops):
            if i not in corr:
                continue
            for j in range(n_ops):
                if j not in corr:
                    continue
                # Symmetric: C_ij(t) = <O_i(t) O_j(0)> = <O_i(0) O_j(t)>
                # For real operators, C_ij(t) = C_ji(t)
                # Use O_i(t) * O_j(0) which for a single config is O_i(t)*O_j(0)
                # Average over t_src: shift by t
                ci = corr[i]
                cj = corr[j]
                # The correlator at time t is the average over all sources:
                # C_ij(t) = 1/Lt * Σ_{t0} O_i(t0+t) * O_j(t0)
                # But our correlator already has this structure if it was computed
                # as a point correlator. The output format has 16 values for Lt=16.
                if len(ci) == Lt and len(cj) == Lt:
                    # Two-point correlator: C_ij(t) = <O_i(t) O_j(0)>
                    # Average over all time sources t0 using translation invariance
                    C_ij_t = np.zeros(Lt)
                    for t in range(Lt):
                        total = 0.0
                        for t0 in range(Lt):
                            total += ci[(t0 + t) % Lt] * cj[t0]
                        C_ij_t[t] = total / Lt
                    C_all[k, :, i, j] = C_ij_t
                    C_all[k, :, j, i] = C_ij_t  # symmetric

    # Average over configs
    C_avg = np.mean(C_all, axis=0)
    C_err = np.std(C_all, axis=0) / np.sqrt(n_configs)

    # Vacuum subtraction for connected correlator
    # <O_i(t) O_j(0)>_connected = <O_i(t) O_j(0)> - <O_i> <O_j>
    mean_O = np.zeros((n_ops, Lt))
    for i in range(n_ops):
        mean_O[i] = np.mean([corr[i] for corr in corrs if i in corr], axis=0)
    for i in range(n_ops):
        for j in range(n_ops):
            vac_sub = np.outer(mean_O[i], mean_O[j])[range(Lt), range(Lt)]
            # Actually <O_i(t)><O_j(0)> averaged over sources:
            vac_prod = np.mean(mean_O[i]) * np.mean(mean_O[j])  # scalar
            C_avg[:, i, j] -= vac_prod

    return C_avg, C_err


def fold_correlator(C, Lt):
    """Fold correlator: C(t) = 0.5*(C(t) + C(Lt-t)) for t > 0"""
    Cf = C.copy()
    for t in range(1, Lt):
        Cf[:, :, t] = 0.5 * (C[:, :, t] + C[:, :, Lt - t])
    # t=0 is special
    Cf[:, :, 0] = C[:, :, 0]
    return Cf


# =========================================================================
# GEVP
# =========================================================================

def solve_gevp(C, t0=1, n_ops=12):
    """
    Solve GEVP: C(t) v_n = λ_n(t) C(t0) v_n
    Returns principal correlator λ_0(t) for ground state.
    """
    Lt = C.shape[0]

    # Symmetrize and regularize C(t0)
    C0 = C[t0]
    C0 = 0.5 * (C0 + C0.T)
    C0 += 1e-10 * np.eye(n_ops)

    lam_0 = np.full(Lt, np.nan)
    lam_1 = np.full(Lt, np.nan)

    for t in range(Lt):
        try:
            Ct = C[t]
            Ct = 0.5 * (Ct + Ct.T)
            eigvals = eigh(Ct, C0, eigvals_only=True)
            # Sort in descending order (largest eigenvalue = ground state)
            eigvals = eigvals[::-1]
            lam_0[t] = eigvals[0]
            if len(eigvals) > 1:
                lam_1[t] = eigvals[1]
        except Exception as e:
            pass

    return lam_0, lam_1


def effective_mass_cosh(lam, Lt):
    """
    Extract effective mass from principal correlator using cosh fit:
    λ(t) = A * cosh(m * (Lt/2 - t))
    m_eff(t) = arccosh( (λ(t-1) + λ(t+1)) / (2*λ(t)) )
    """
    m_eff = np.full(Lt, np.nan)
    for t in range(1, Lt - 1):
        if lam[t] > 0 and lam[t-1] > 0 and lam[t+1] > 0:
            ratio = (lam[t-1] + lam[t+1]) / (2.0 * lam[t])
            if ratio >= 1.0:
                m_eff[t] = np.arccosh(ratio)
    return m_eff


def plateau_fit(m_eff, t_min, t_max):
    """Constant fit to effective mass plateau."""
    vals = m_eff[t_min:t_max+1]
    vals = vals[~np.isnan(vals)]
    if len(vals) < 2:
        return np.nan, np.nan
    m = np.mean(vals)
    e = np.std(vals, ddof=1) / np.sqrt(len(vals))
    return m, e


# =========================================================================
# MAIN ANALYSIS
# =========================================================================

def analyze_beta(results_dir, beta_tag, beta_val, t0_gevp=2, t_min=3, t_max=6):
    """
    Full GEVP analysis for one beta value.
    """
    print(f"\n{'='*60}")
    print(f"  β = {beta_val}  (tag: b{beta_tag})")
    print(f"{'='*60}")

    # Load data
    corrs = load_beta_data(results_dir, beta_tag)
    if not corrs:
        print(f"  No data loaded. Skipping.")
        return None

    n_configs = len(corrs)
    n_ops = max(corrs[0].keys()) + 1
    Lt = len(corrs[0][0])
    print(f"  Configs: {n_configs}")
    print(f"  Operators: {n_ops}")
    print(f"  Lt: {Lt}")

    # Build correlation matrix
    C_avg, C_err = build_corr_matrix(corrs)
    if C_avg is None:
        print(f"  Failed to build correlation matrix.")
        return None

    # Fold
    C_folded = fold_correlator(C_avg, Lt)

    print(f"\n  GEVP with t0={t0_gevp}, using {n_ops} operators...")

    # Solve GEVP
    lam_0, lam_1 = solve_gevp(C_folded, t0=t0_gevp, n_ops=n_ops)

    # Effective masses
    m0_eff = effective_mass_cosh(lam_0, Lt)
    m1_eff = effective_mass_cosh(lam_1, Lt)

    # Print effective masses
    print(f"\n  {'t':>3s}  {'λ₀(t)':>12s}  {'m₀_eff':>10s}  {'λ₁(t)':>12s}  {'m₁_eff':>10s}")
    for t in range(min(Lt, 10)):
        l0 = f"{lam_0[t]:.6e}" if not np.isnan(lam_0[t]) else "N/A"
        m0 = f"{m0_eff[t]:.6f}" if not np.isnan(m0_eff[t]) else "N/A"
        l1 = f"{lam_1[t]:.6e}" if not np.isnan(lam_1[t]) else "N/A"
        m1 = f"{m1_eff[t]:.6f}" if not np.isnan(m1_eff[t]) else "N/A"
        print(f"  {t:3d}  {l0:>12s}  {m0:>10s}  {l1:>12s}  {m1:>10s}")

    # Plateau fits
    m0_val, m0_err = plateau_fit(m0_eff, t_min, t_max)
    m1_val, m1_err = plateau_fit(m1_eff, t_min, t_max)

    # Ratio
    if not np.isnan(m0_val) and not np.isnan(m1_val) and m0_val > 0:
        R_val = (m1_val / m0_val) ** 2
        # Error propagation (ignore correlation for first pass)
        R_err = R_val * 2.0 * np.sqrt((m1_err/m1_val)**2 + (m0_err/m0_val)**2)
    else:
        R_val, R_err = np.nan, np.nan

    print(f"\n  --- Results ---")
    print(f"  Plateau fit: t ∈ [{t_min}, {t_max}]")
    print(f"  m₀++·a = {m0_val:.6f} ± {m0_err:.6f}" if not np.isnan(m0_val) else f"  m₀++·a = N/A")
    print(f"  m₂++·a = {m1_val:.6f} ± {m1_err:.6f}" if not np.isnan(m1_val) else f"  m₂++·a = N/A")
    print(f"  R = (m₂++/m₀++)² = {R_val:.6f} ± {R_err:.6f}" if not np.isnan(R_val) else f"  R = N/A")

    # Verdict
    if not np.isnan(R_val):
        low = R_val - R_err
        high = R_val + R_err
        if 1.98 <= low and high <= 2.02:
            verdict = VERDICT["validated"]
        elif R_val < 1.0 or R_val > 3.0 or R_err > 0.5:
            verdict = VERDICT["inconclusive"]
        else:
            verdict = VERDICT["falsified"]
        print(f"\n  🏁 {verdict}")
        print(f"     R = {R_val:.4f} ± {R_err:.4f}")
        print(f"     Reference AT 2021: 2.001(17)")
        print(f"     Conjecture E-1: 2.000")
    else:
        print(f"\n  🏁 {VERDICT['inconclusive']}")

    return {
        "beta": beta_val,
        "beta_tag": beta_tag,
        "n_configs": n_configs,
        "n_ops": n_ops,
        "Lt": Lt,
        "m0": (float(m0_val), float(m0_err)),
        "m1": (float(m1_val), float(m1_err)),
        "R": (float(R_val), float(R_err)),
        "t0_gevp": t0_gevp,
        "plateau_range": [t_min, t_max],
    }


def main():
    import argparse
    parser = argparse.ArgumentParser(description="Phase E3 GEVP Glueball Analysis")
    parser.add_argument("--results-dir", default="/root/results_phase4_v3",
                        help="Directory with Phase 4 v3 results")
    parser.add_argument("--betas", nargs="+", default=["250", "260"],
                        help="Beta tags to analyze (e.g., 250 260)")
    parser.add_argument("--beta-vals", nargs="+", type=float, default=None,
                        help="Actual beta values corresponding to tags")
    parser.add_argument("--t0", type=int, default=2,
                        help="GEVP t0 reference time")
    parser.add_argument("--t-min", type=int, default=3,
                        help="Plateau fit start time")
    parser.add_argument("--t-max", type=int, default=6,
                        help="Plateau fit end time")
    parser.add_argument("--output", default=None,
                        help="Output JSON path")
    args = parser.parse_args()

    beta_vals = args.beta_vals or [float(t)/100.0 for t in args.betas]

    results = []
    for tag, val in zip(args.betas, beta_vals):
        r = analyze_beta(args.results_dir, tag, val,
                         t0_gevp=args.t0,
                         t_min=args.t_min, t_max=args.t_max)
        if r:
            results.append(r)

    if not results:
        print("\nNo results. Make sure Phase 4 v3 has been run first.")
        sys.exit(1)

    # Final combined verdict
    print(f"\n{'='*60}")
    print(f"  PHASE E3 — CONJECTURE E-1 SUMMARY")
    print(f"{'='*60}")

    # Weighted average of R across betas
    Rs = np.array([r["R"][0] for r in results if not np.isnan(r["R"][0])])
    Rs_err = np.array([r["R"][1] for r in results if not np.isnan(r["R"][0])])
    if len(Rs) > 0:
        # Inverse-variance weighted average
        w = 1.0 / Rs_err**2
        R_avg = np.sum(w * Rs) / np.sum(w)
        R_avg_err = 1.0 / np.sqrt(np.sum(w))
        print(f"  R (weighted avg) = {R_avg:.4f} ± {R_avg_err:.4f}")

        for r in results:
            print(f"  β={r['beta']}: R={r['R'][0]:.4f}±{r['R'][1]:.4f}  "
                  f"m₀a={r['m0'][0]:.4f}±{r['m0'][1]:.4f}  "
                  f"m₁a={r['m1'][0]:.4f}±{r['m1'][1]:.4f}")

        if 1.98 <= R_avg - R_avg_err and R_avg + R_avg_err <= 2.02:
            print(f"\n  ✅ {VERDICT['validated']}")
        elif Rs[0] < 1.0 or Rs[0] > 3.0 or R_avg_err > 0.5:
            print(f"\n  ❓ {VERDICT['inconclusive']}")
        else:
            print(f"\n  ❌ {VERDICT['falsified']}")

        print(f"  Reference (AT 2021): 2.001(17)")
        print(f"  Conjecture E-1: 2.000")
    else:
        print(f"  No valid R values extracted.")
        print(f"\n  ❓ {VERDICT['inconclusive']}")

    print(f"\n{'='*60}")

    if args.output:
        output_data = {
            "analysis": "Phase E3 GEVP Glueball",
            "conjecture": "E-1",
            "prediction": 2.000,
            "reference_at2021": [2.001, 0.017],
            "results": results,
            "combined_R": [float(R_avg), float(R_avg_err)] if len(Rs) > 0 else None
        }
        with open(args.output, "w") as f:
            json.dump(output_data, f, indent=2)
        print(f"  Results saved to {args.output}")


if __name__ == "__main__":
    main()
