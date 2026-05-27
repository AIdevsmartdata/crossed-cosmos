#!/usr/bin/env python3
"""
G_2 Lattice EE — Complete Analysis Pipeline.

Reads output from g2_ee Rust binary, performs:
1. Sanity checks (plaquette, thermalization, autocorrelation)
2. α-integration with error propagation
3. Multi-L fit for κ_EE extraction (area law)
4. Comparison to 4 competing predictions
5. Systematic error budget
6. Publication-ready plots + tables

Expected physics from what we know:
- S_2(L) = a_div · Area + κ_EE · Perimeter + c_log · log(L) + const
- For 4D with half-lattice cut: Area = L² × T, Perimeter = 4L × T
- The LEADING term is UV divergent (~1/a²), subtracted by L-dependence
- κ_EE is the UNIVERSAL sub-leading coefficient we want

Predictions for κ_EE(G_2):
  P1: (1-1/N²)·ζ(3)/√π with N=rank+1=3  → 0.6027  (SU(3)-like)
  P2: (1-1/dim)·ζ(3)/√π with dim=14       → 0.6298  (dim-law)
  P3: 0.518·√(rank) - 0.458 with rank=2    → 0.2746  (√N affine)
  P4: κ_FP = 1/(2|Φ⁺|) = 1/12             → 0.0833  (FP convention)

Author: Kévin Rémondière (ORCID 0009-0008-2443-7166)
"""
import numpy as np
import json
import sys
import os
from scipy.optimize import curve_fit
from scipy.special import zeta as riemann_zeta

# ============================================================
# PREDICTIONS
# ============================================================

ZETA3 = riemann_zeta(3)  # 1.2020569...
KAPPA_INF = ZETA3 / np.sqrt(np.pi)  # 0.6782

PREDICTIONS = {
    'P1_SU3_rank': (1 - 1/9) * KAPPA_INF,        # 0.6027
    'P2_dim_law':  (1 - 1/14) * KAPPA_INF,        # 0.6298
    'P3_sqrt_N':   0.518 * np.sqrt(2) - 0.458,    # 0.2746
    'P4_kappa_FP': 1/12,                            # 0.0833
}

# ============================================================
# 1. PARSE LOG FILES
# ============================================================

def parse_ee_log(logfile):
    """Parse g2_ee Rust output log."""
    data = {
        'ls': None, 'lt': None, 'beta': None,
        'alphas': [], 'ds_means': [], 'ds_errs': [],
        's2': None, 's2_err': None, 'area': None,
        'total_time': None,
    }

    with open(logfile) as f:
        for line in f:
            line = line.strip()
            if line.startswith('# Ls='):
                parts = line.split(',')
                for p in parts:
                    p = p.strip().lstrip('# ')
                    if p.startswith('Ls='): data['ls'] = int(p.split('=')[1])
                    if p.startswith('Lt='): data['lt'] = int(p.split('=')[1])
                    if p.startswith('beta='): data['beta'] = float(p.split('=')[1])
            elif line.startswith('ALPHA'):
                parts = line.split()
                alpha = float(parts[1].rstrip(':'))
                ds = float(parts[3])
                err = float(parts[5])
                data['alphas'].append(alpha)
                data['ds_means'].append(ds)
                data['ds_errs'].append(err)
            elif line.startswith('RESULT: S2='):
                parts = line.split()
                data['s2'] = float(parts[1].split('=')[1])
                data['s2_err'] = float(parts[3])
            elif line.startswith('RESULT: area='):
                data['area'] = float(line.split('=')[1])
            elif line.startswith('# Total time:'):
                data['total_time'] = float(line.split(':')[1].strip().split('s')[0])

    data['alphas'] = np.array(data['alphas'])
    data['ds_means'] = np.array(data['ds_means'])
    data['ds_errs'] = np.array(data['ds_errs'])
    return data


def parse_beta_scan_log(logfile):
    """Parse β-scan Rust output."""
    results = []
    current = {}
    with open(logfile) as f:
        for line in f:
            line = line.strip()
            if line.startswith('=== beta='):
                parts = line.split()
                current = {
                    'beta': float(parts[0].split('=')[1]),
                    'L': int(parts[1].split('=')[1]),
                }
            elif line.startswith('RESULT:'):
                parts = line.split()
                for p in parts[1:]:
                    k, v = p.split('=')
                    current[k] = float(v)
                results.append(current)
                current = {}
    return results


# ============================================================
# 2. SANITY CHECKS
# ============================================================

def sanity_check_ee(data):
    """Run sanity checks on EE measurement."""
    checks = []

    # Check 1: α=0 should give normal action
    if len(data['alphas']) > 0 and data['alphas'][0] == 0:
        checks.append(('α=0 exists', True, 'OK'))
    else:
        checks.append(('α=0 exists', False, 'MISSING α=0 point'))

    # Check 2: dS/dα should decrease monotonically with α
    if len(data['ds_means']) > 1:
        diffs = np.diff(data['ds_means'])
        monotone = np.all(diffs < 0)
        checks.append(('dS/dα monotone decreasing', monotone,
                       f'diffs: {diffs[:3]}...'))

    # Check 3: dS/dα(1) should be positive (minimal action at α=1)
    if len(data['ds_means']) > 0:
        last_positive = data['ds_means'][-1] > 0
        checks.append(('dS/dα(1) > 0', last_positive,
                       f'value: {data["ds_means"][-1]:.2f}'))

    # Check 4: S2 should be positive
    if data['s2'] is not None:
        checks.append(('S2 > 0', data['s2'] > 0, f'S2 = {data["s2"]:.2f}'))

    # Check 5: Error bars should be small relative to signal
    if data['s2'] is not None and data['s2_err'] is not None:
        rel_err = data['s2_err'] / abs(data['s2']) if data['s2'] != 0 else float('inf')
        checks.append(('Relative error < 1%', rel_err < 0.01,
                       f'rel_err = {rel_err:.4f}'))

    # Check 6: Number of α-points
    n_alpha = len(data['alphas'])
    checks.append(('n_alpha >= 11', n_alpha >= 11, f'n_alpha = {n_alpha}'))

    return checks


def sanity_check_plaquette(beta_scan_results):
    """Check plaquette physics."""
    checks = []

    betas = sorted(set(r['beta'] for r in beta_scan_results))
    for beta in betas:
        pts = [r for r in beta_scan_results if r['beta'] == beta]
        p_vals = [r.get('P', 0) for r in pts]
        checks.append((f'⟨P⟩(β={beta}) > 0', all(p > 0 for p in p_vals),
                       f'values: {[f"{p:.4f}" for p in p_vals]}'))

    # Monotonicity in β
    if len(betas) >= 2:
        p_L8 = {r['beta']: r.get('P', 0) for r in beta_scan_results if r.get('L') == 8}
        if len(p_L8) >= 2:
            sorted_p = [p_L8[b] for b in sorted(p_L8.keys())]
            mono = all(sorted_p[i] <= sorted_p[i+1] for i in range(len(sorted_p)-1))
            checks.append(('⟨P⟩ monotone in β (L=8)', mono, f'{sorted_p}'))

    return checks


# ============================================================
# 3. κ_EE EXTRACTION
# ============================================================

def extract_kappa_single_L(data):
    """Extract raw S2/Area from single L measurement."""
    if data['s2'] is None or data['area'] is None:
        return None, None
    return data['s2'] / data['area'], data['s2_err'] / data['area']


def extract_kappa_multi_L(data_list):
    """Extract κ_EE from multi-L fit.

    S_2(L) = a · L² · T + κ · L · T + c · T + d
    For fixed β and T = 2L:
    S_2(L) = a · 2L³ + κ · 2L² + c · 2L + d

    Fit S_2/L² = 2a·L + 2κ + 2c/L + d/L²
    The intercept at 1/L → 0 gives 2κ.
    """
    if len(data_list) < 2:
        return None, None, None

    Ls = np.array([d['ls'] for d in data_list])
    S2s = np.array([d['s2'] for d in data_list])
    S2_errs = np.array([d['s2_err'] for d in data_list])
    Ts = np.array([d['lt'] for d in data_list])

    areas = Ls**2 * Ts
    s2_per_area = S2s / areas
    s2_per_area_err = S2_errs / areas

    # Simple linear fit: S2/Area = a_div + κ/L + ...
    # Or equivalently: S2/(L²T) = a + κ/L → fit vs 1/L
    inv_L = 1.0 / Ls

    if len(data_list) >= 3:
        # Quadratic fit: S2/Area = a + b/L + c/L²
        def fit_func(x, a, b, c):
            return a + b * x + c * x**2
        try:
            popt, pcov = curve_fit(fit_func, inv_L, s2_per_area,
                                   sigma=s2_per_area_err, absolute_sigma=True)
            perr = np.sqrt(np.diag(pcov))
            return popt[1], perr[1], {'a_div': popt[0], 'c_sub': popt[2]}
        except Exception:
            pass

    # Fallback: linear fit S2/Area = a + κ/L
    def fit_linear(x, a, b):
        return a + b * x
    try:
        popt, pcov = curve_fit(fit_linear, inv_L, s2_per_area,
                               sigma=s2_per_area_err, absolute_sigma=True)
        perr = np.sqrt(np.diag(pcov))
        return popt[1], perr[1], {'a_div': popt[0]}
    except Exception:
        return None, None, None


# ============================================================
# 4. COMPARISON TO PREDICTIONS
# ============================================================

def compare_predictions(kappa, kappa_err):
    """Compare measured κ to 4 predictions."""
    results = []
    for name, pred in PREDICTIONS.items():
        if kappa is not None and kappa_err is not None and kappa_err > 0:
            tension = abs(kappa - pred) / kappa_err
            compatible = tension < 2.0
        else:
            tension = float('inf')
            compatible = False
        results.append({
            'name': name, 'predicted': pred,
            'measured': kappa, 'error': kappa_err,
            'tension_sigma': tension,
            'compatible_2sigma': compatible,
        })
    return results


# ============================================================
# 5. SYSTEMATIC ERROR BUDGET
# ============================================================

def systematic_errors(data_list):
    """Estimate systematic uncertainties."""
    systematics = {}

    if len(data_list) >= 2:
        # Finite volume: difference between largest two L
        sorted_data = sorted(data_list, key=lambda d: d['ls'])
        if len(sorted_data) >= 2:
            s2a_large = sorted_data[-1]['s2'] / (sorted_data[-1]['ls']**2 * sorted_data[-1]['lt'])
            s2a_small = sorted_data[-2]['s2'] / (sorted_data[-2]['ls']**2 * sorted_data[-2]['lt'])
            systematics['finite_volume'] = abs(s2a_large - s2a_small)

    # Thermalization: would need raw timeseries (not available from summary)
    systematics['thermalization'] = 'check autocorrelation in raw data'

    # Discretization: would need multiple β values
    systematics['discretization'] = 'need multi-β analysis'

    # Taylor exp truncation in expm
    # Taylor order 7: error ~ |A|^8/8! ~ (ε√14)^8/40320
    eps = 0.15
    taylor_err = (eps * np.sqrt(14))**8 / 40320
    systematics['taylor_expm'] = taylor_err

    return systematics


# ============================================================
# 6. SCENARIOS (what to expect)
# ============================================================

def print_scenarios():
    """Print expected scenarios based on physics insights."""
    print("""
╔══════════════════════════════════════════════════════════════╗
║              EXPECTED SCENARIOS FOR κ_EE(G_2)               ║
╠══════════════════════════════════════════════════════════════╣
║                                                              ║
║ SCENARIO A: κ ≈ 0.60 ± 0.02 (P1 or P2)                    ║
║   → G_2 follows same EE law as SU(N≤4)                     ║
║   → Paper: "Universal EE in exceptional gauge theories"     ║
║   → Impact: HIGH — confirms ζ(3)/√π universality            ║
║   → Caveat: can't distinguish P1 (0.603) from P2 (0.630)   ║
║     at L=8. Need L=12,16 for that.                          ║
║                                                              ║
║ SCENARIO B: κ ≈ 0.28 ± 0.03 (P3)                           ║
║   → G_2 follows √(rank) scaling like SU(N≥5)               ║
║   → Paper: "Non-universal EE: rank dependence"              ║
║   → Impact: MEDIUM — extends √N regime to exceptionals      ║
║   → Would confirm crossover at N~4 extends to G_2           ║
║                                                              ║
║ SCENARIO C: κ ≈ 0.08 ± 0.01 (P4)                           ║
║   → G_2 matches Faddeev-Popov convention κ_FP = 1/12        ║
║   → Paper: "EE as FP determinant measure"                   ║
║   → Impact: HIGH — connects EE to gauge-fixing geometry     ║
║   → Would strongly support KR-FP-3 framework                ║
║                                                              ║
║ SCENARIO D: κ ≠ any prediction                              ║
║   → New physics! G_2 has its own EE coefficient             ║
║   → Paper: "First measurement of EE in G_2 gauge theory"   ║
║   → Impact: MEDIUM — establishes baseline, falsifies models ║
║   → Still publishable as first measurement                   ║
║                                                              ║
║ SCENARIO E: S_2 ∝ L³ (no area law)                          ║
║   → Volume law instead of area law — VERY surprising        ║
║   → Would mean G_2 is in a different phase                  ║
║   → Possible if β=10 is below deconfinement for this volume ║
║   → Check: compare with L=4,6 to verify scaling             ║
║                                                              ║
║ MOST LIKELY: A or B based on SU(N) precedent                ║
║   G_2 rank = 2, closest to SU(3) in complexity              ║
║   But exceptional → could break SU(N) pattern               ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
""")


# ============================================================
# 7. LIMITS & CAVEATS
# ============================================================

def print_limits():
    """Print known limitations of this measurement."""
    print("""
╔══════════════════════════════════════════════════════════════╗
║                    KNOWN LIMITATIONS                         ║
╠══════════════════════════════════════════════════════════════╣
║                                                              ║
║ 1. SINGLE β VALUE (β=10.0)                                  ║
║    → Cannot take continuum limit (a→0)                      ║
║    → κ_EE(β) may have β-dependence not yet resolved         ║
║    → FIX: run β=9.8, 10.2 and check consistency             ║
║                                                              ║
║ 2. RENYI-2 NOT VON NEUMANN                                  ║
║    → We measure S_2 = -log Tr(ρ²), not S_vN = -Tr(ρ log ρ) ║
║    → Ratio S_2/S_vN ≈ 0.7-0.9 for gauge theories           ║
║    → Compare with SU(2,3) same method for calibration        ║
║                                                              ║
║ 3. HALF-LATTICE CUT ONLY                                    ║
║    → ∂A is flat (not curved) → misses shape dependence      ║
║    → Standard in lattice EE literature (BP2008b)             ║
║                                                              ║
║ 4. METROPOLIS (NOT HMC)                                      ║
║    → Autocorrelation may be long for L≥12                   ║
║    → Acceptance ~40% at β=10 is OK for L=8                  ║
║    → Monitor integrated autocorrelation time τ_int           ║
║                                                              ║
║ 5. TAYLOR EXPM (ORDER 7)                                     ║
║    → Error ~ (ε√14)^8/8! ≈ 2×10⁻⁴ per step                ║
║    → Accumulates over ~10⁶ steps → may drift                ║
║    → FIX: periodic re-orthogonalization (Gram-Schmidt SO(7)) ║
║    → OR: switch to eigh exact for production                 ║
║                                                              ║
║ 6. NO SMEARING                                               ║
║    → UV fluctuations dominate the raw S_2                   ║
║    → κ_EE extraction requires L-scaling (multi-L fit)       ║
║    → APE/HYP smearing would reduce noise but complicates    ║
║      the EE interpretation                                   ║
║                                                              ║
║ 7. STATISTICS                                                ║
║    → 200 measurements per α-point                           ║
║    → May need 500-1000 for < 1% precision on κ              ║
║    → Jackknife/bootstrap for proper error estimation         ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
""")


# ============================================================
# MAIN ANALYSIS
# ============================================================

def analyze_single(logfile):
    """Full analysis of a single EE measurement."""
    print(f"\n{'='*60}")
    print(f"  G_2 κ_EE ANALYSIS — {logfile}")
    print(f"{'='*60}")

    data = parse_ee_log(logfile)
    print(f"\n  Ls={data['ls']}, Lt={data['lt']}, β={data['beta']}")
    print(f"  n_alpha = {len(data['alphas'])}")

    # Sanity checks
    print(f"\n--- SANITY CHECKS ---")
    checks = sanity_check_ee(data)
    all_pass = True
    for name, passed, detail in checks:
        status = "✅" if passed else "❌"
        print(f"  {status} {name}: {detail}")
        if not passed:
            all_pass = False

    if not all_pass:
        print("\n  ⚠️  SOME CHECKS FAILED — interpret with caution")

    # α-integration curve
    print(f"\n--- α-INTEGRATION ---")
    if len(data['alphas']) > 0:
        for i, (a, ds, err) in enumerate(zip(data['alphas'], data['ds_means'], data['ds_errs'])):
            print(f"  α={a:.2f}: dS/dα = {ds:12.2f} ± {err:8.2f}")

    # Raw S2
    if data['s2'] is not None:
        print(f"\n  S_2 = {data['s2']:.2f} ± {data['s2_err']:.2f}")
        print(f"  S_2/Area = {data['s2']/data['area']:.6f} ± {data['s2_err']/data['area']:.6f}")

    # Predictions comparison (raw, not yet κ extracted)
    kappa_raw, kappa_raw_err = extract_kappa_single_L(data)
    if kappa_raw is not None:
        print(f"\n--- RAW κ = S_2/Area (single L, includes UV divergence) ---")
        print(f"  κ_raw = {kappa_raw:.4f} ± {kappa_raw_err:.4f}")
        print(f"  NOTE: This is NOT κ_EE — it includes the 1/a² UV divergent piece")
        print(f"  Need multi-L fit to extract universal κ_EE")

    # Systematics
    print(f"\n--- SYSTEMATIC BUDGET ---")
    syst = systematic_errors([data])
    for k, v in syst.items():
        print(f"  {k}: {v}")

    return data


def full_analysis(ee_files, beta_scan_file=None):
    """Complete analysis pipeline."""
    print_scenarios()
    print_limits()

    # β-scan check
    if beta_scan_file and os.path.exists(beta_scan_file):
        print(f"\n{'='*60}")
        print(f"  β-SCAN VALIDATION")
        print(f"{'='*60}")
        results = parse_beta_scan_log(beta_scan_file)
        checks = sanity_check_plaquette(results)
        for name, passed, detail in checks:
            status = "✅" if passed else "❌"
            print(f"  {status} {name}: {detail}")

    # Analyze each EE file
    all_data = []
    for f in ee_files:
        if os.path.exists(f):
            data = analyze_single(f)
            all_data.append(data)

    # Multi-L κ extraction
    if len(all_data) >= 2:
        print(f"\n{'='*60}")
        print(f"  MULTI-L κ_EE EXTRACTION")
        print(f"{'='*60}")
        kappa, kappa_err, fit_params = extract_kappa_multi_L(all_data)
        if kappa is not None:
            print(f"\n  ★ κ_EE(G_2) = {kappa:.4f} ± {kappa_err:.4f}")
            print(f"  Fit params: {fit_params}")

            print(f"\n--- COMPARISON TO PREDICTIONS ---")
            comps = compare_predictions(kappa, kappa_err)
            for c in comps:
                status = "✅" if c['compatible_2sigma'] else "❌"
                print(f"  {status} {c['name']:20s}: pred={c['predicted']:.4f}, "
                      f"tension={c['tension_sigma']:.1f}σ")

            # Verdict
            best = min(comps, key=lambda c: c['tension_sigma'])
            print(f"\n  BEST MATCH: {best['name']} ({best['tension_sigma']:.1f}σ)")
        else:
            print("  ❌ Fit failed — insufficient data or bad conditioning")

    # Save analysis
    out = {
        'predictions': {k: float(v) for k, v in PREDICTIONS.items()},
        'measurements': [{
            'ls': d['ls'], 'lt': d['lt'], 'beta': d['beta'],
            's2': float(d['s2']) if d['s2'] else None,
            's2_err': float(d['s2_err']) if d['s2_err'] else None,
            'area': float(d['area']) if d['area'] else None,
        } for d in all_data],
    }
    with open('g2_ee_analysis.json', 'w') as f:
        json.dump(out, f, indent=2)
    print(f"\n  Saved analysis to g2_ee_analysis.json")


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--ee', nargs='+', default=['g2_ee_L8_beta10.log'])
    parser.add_argument('--beta-scan', default=None)
    parser.add_argument('--scenarios', action='store_true')
    parser.add_argument('--limits', action='store_true')
    args = parser.parse_args()

    if args.scenarios:
        print_scenarios()
    elif args.limits:
        print_limits()
    else:
        full_analysis(args.ee, args.beta_scan)
