#!/usr/bin/env python3
"""
KEVINOTRON ORCHESTRATOR
========================
Multi-group x multi-L x multi-beta automated scan.

Dispatches Rust kevinotron binary in parallel (one process per alpha-point).
Collects results, performs trapezoidal integration, fits kappa_EE.

Usage:
    python3 orchestrate.py --groups g2 su3 --ls 4 6 8 --betas 10.0
    python3 orchestrate.py --groups su2 --ls 4 6 8 10 12 --betas 2.50 --n-parallel 11
    python3 orchestrate.py --analyze-only --log-dir results/

Author: Kevin Remondiere (ORCID 0009-0008-2443-7166)
"""

import subprocess
import os
import sys
import time
import json
import argparse
import numpy as np
from pathlib import Path
from concurrent.futures import ProcessPoolExecutor, as_completed
from scipy.optimize import curve_fit

# ============================================================
# DEFAULT PARAMETERS
# ============================================================

# Standard betas (matched sigma*a^2 ~ 0.22 for scaling window)
DEFAULT_BETAS = {
    'su2': [2.50],
    'su3': [6.06],
    'su4': [10.80],
    'g2':  [10.0],
    'sp4': [8.0],
    'so7': [10.0],
}

DEFAULT_THERM = {
    'su2': 500, 'su3': 500, 'su4': 500, 'g2': 500, 'sp4': 500, 'so7': 500,
}

DEFAULT_MEAS = {
    'su2': 200, 'su3': 200, 'su4': 200, 'g2': 200, 'sp4': 200, 'so7': 200,
}

DEFAULT_EPS = {
    'su2': 0.20, 'su3': 0.15, 'su4': 0.12, 'g2': 0.15, 'sp4': 0.12, 'so7': 0.15,
}


# ============================================================
# LAUNCH ONE ALPHA-POINT
# ============================================================

def run_alpha_point(binary, group, ls, beta, alpha, n_therm, n_meas, n_skip, eps, log_dir):
    """Run a single kevinotron alpha-point and capture output."""
    cmd = [
        binary,
        '--group', group,
        '--ls', str(ls),
        '--beta', str(beta),
        '--alpha', str(alpha),
        '--n-therm', str(n_therm),
        '--n-meas', str(n_meas),
        '--n-skip', str(n_skip),
        '--epsilon', str(eps),
    ]

    logfile = os.path.join(log_dir, f"{group}_L{ls}_beta{beta:.2f}_alpha{alpha:.2f}.log")

    t0 = time.time()
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=7200)
    elapsed = time.time() - t0

    with open(logfile, 'w') as f:
        f.write(result.stdout)
        f.write(result.stderr)

    # Parse ALPHA line
    for line in result.stdout.split('\n'):
        if line.startswith('ALPHA'):
            parts = line.split()
            alpha_val = float(parts[1].rstrip(':'))
            ds_mean = float(parts[3])
            ds_err = float(parts[5])
            return {
                'alpha': alpha_val, 'ds_mean': ds_mean, 'ds_err': ds_err,
                'time': elapsed, 'logfile': logfile,
            }

    return {'alpha': alpha, 'ds_mean': None, 'ds_err': None, 'time': elapsed, 'logfile': logfile}


# ============================================================
# RUN ONE FULL EE (all alpha-points)
# ============================================================

def run_full_ee(binary, group, ls, beta, n_alpha, n_parallel, n_therm, n_meas, n_skip, eps, log_dir):
    """Run all alpha-points for one (group, L, beta) config."""
    alphas = np.linspace(0.0, 1.0, n_alpha)
    results = [None] * n_alpha

    print(f"\n{'='*60}")
    print(f"  {group} L={ls} beta={beta} -- {n_alpha} alpha-points")
    print(f"{'='*60}")

    t0 = time.time()

    with ProcessPoolExecutor(max_workers=n_parallel) as executor:
        futures = {}
        for i, alpha in enumerate(alphas):
            f = executor.submit(
                run_alpha_point, binary, group, ls, beta, alpha,
                n_therm, n_meas, n_skip, eps, log_dir
            )
            futures[f] = i

        for future in as_completed(futures):
            i = futures[future]
            try:
                res = future.result()
                results[i] = res
                print(f"  alpha={alphas[i]:.2f}: dS/da = {res['ds_mean']:.2f} +/- {res['ds_err']:.2f} ({res['time']:.0f}s)")
            except Exception as e:
                print(f"  alpha={alphas[i]:.2f}: FAILED ({e})")
                results[i] = {'alpha': alphas[i], 'ds_mean': None, 'ds_err': None}

    total_time = time.time() - t0

    # Filter successful results
    good = [r for r in results if r and r['ds_mean'] is not None]
    if len(good) < n_alpha:
        print(f"  WARNING: {n_alpha - len(good)} alpha-points failed")

    if len(good) < 2:
        print("  ERROR: too few successful alpha-points for integration")
        return None

    # Sort by alpha
    good.sort(key=lambda r: r['alpha'])
    alphas_ok = np.array([r['alpha'] for r in good])
    ds_means = np.array([r['ds_mean'] for r in good])
    ds_errs = np.array([r['ds_err'] for r in good])

    # Trapezoidal integration
    S2 = np.trapezoid(ds_means, alphas_ok)
    # Error propagation (trapezoidal)
    S2_err = np.sqrt(np.sum([
        (ds_errs[i] * (alphas_ok[min(i+1, len(alphas_ok)-1)] - alphas_ok[max(i-1, 0)]) / 2)**2
        for i in range(len(ds_errs))
    ]))

    Lt = 2 * ls
    area = ls * ls * Lt
    S2_A = S2 / area
    S2_A_err = S2_err / area

    print(f"\n  S2 = {S2:.4f} +/- {S2_err:.4f}")
    print(f"  A = {area}")
    print(f"  S2/A = {S2_A:.6f} +/- {S2_A_err:.6f}")
    print(f"  Total wall time: {total_time:.0f}s = {total_time/60:.1f}min")

    return {
        'group': group, 'ls': ls, 'lt': Lt, 'beta': beta,
        's2': float(S2), 's2_err': float(S2_err),
        'area': float(area), 's2_a': float(S2_A), 's2_a_err': float(S2_A_err),
        'n_alpha_ok': len(good), 'wall_time': total_time,
        'alphas': alphas_ok.tolist(),
        'ds_means': ds_means.tolist(),
        'ds_errs': ds_errs.tolist(),
    }


# ============================================================
# ANALYSIS
# ============================================================

def analyze_results(all_results):
    """Analyze multi-L results: fit kappa_EE, compare to predictions."""
    from scipy.special import zeta as riemann_zeta

    zeta3 = riemann_zeta(3)
    kappa_inf = zeta3 / np.sqrt(np.pi)

    predictions = {
        'SU(2)': {'kappa_FP': 0.5, 'kappa_EE': (1 - 0.25) * kappa_inf},
        'SU(3)': {'kappa_FP': 1/6, 'kappa_EE': (1 - 1/9) * kappa_inf},
        'SU(4)': {'kappa_FP': 1/12, 'kappa_EE': (1 - 1/16) * kappa_inf},
        'G2':    {'kappa_FP': 1/12, 'kappa_EE_P1': (1 - 1/9) * kappa_inf,
                  'kappa_EE_P2': (1 - 1/14) * kappa_inf},
        'Sp(4)': {'kappa_FP': 1/8, 'kappa_EE': (1 - 1/10) * kappa_inf},
        'SO(7)': {'kappa_FP': 1/30, 'kappa_EE': (1 - 1/21) * kappa_inf},
    }

    # Group results by (group, beta)
    grouped = {}
    for r in all_results:
        key = (r['group'], r['beta'])
        if key not in grouped:
            grouped[key] = []
        grouped[key].append(r)

    print(f"\n{'='*70}")
    print(f"  ANALYSIS SUMMARY")
    print(f"{'='*70}")

    for (group, beta), results in sorted(grouped.items()):
        results.sort(key=lambda r: r['ls'])
        Ls = np.array([r['ls'] for r in results])
        S2_A = np.array([r['s2_a'] for r in results])
        S2_A_err = np.array([r['s2_a_err'] for r in results])

        print(f"\n  {group} beta={beta}:")
        print(f"  {'L':>4} | {'S2/A':>10} | {'error':>10}")
        print(f"  {'-'*4}-+-{'-'*10}-+-{'-'*10}")
        for i in range(len(Ls)):
            print(f"  {Ls[i]:4d} | {S2_A[i]:10.6f} | {S2_A_err[i]:10.6f}")

        # Fit S2/A = a_div + c/L^2
        if len(Ls) >= 3:
            def area_law(L, a_inf, c):
                return a_inf + c / L**2

            try:
                popt, pcov = curve_fit(area_law, Ls, S2_A, p0=[S2_A[-1], 1.0],
                                       sigma=S2_A_err, absolute_sigma=True)
                perr = np.sqrt(np.diag(pcov))
                chi2 = np.sum(((S2_A - area_law(Ls, *popt)) / S2_A_err)**2)
                ndof = len(Ls) - 2
                print(f"\n  Fit: S2/A = {popt[0]:.6f} + {popt[1]:.2f}/L^2")
                print(f"  a_inf = {popt[0]:.6f} +/- {perr[0]:.6f}")
                print(f"  c = {popt[1]:.2f} +/- {perr[1]:.2f}")
                print(f"  chi2/dof = {chi2:.2f}/{ndof}")
            except Exception as e:
                print(f"  Fit failed: {e}")

    # Cross-group ratios at common L values
    print(f"\n{'='*70}")
    print(f"  CROSS-GROUP RATIOS (at L=4)")
    print(f"{'='*70}")

    l4_data = {}
    for r in all_results:
        if r['ls'] == 4:
            l4_data[r['group']] = r['s2_a']

    if 'su3' in l4_data:
        su3_val = l4_data['su3']
        for g, val in sorted(l4_data.items()):
            if g != 'su3':
                print(f"  {g}/SU(3) = {val/su3_val:.4f}")


# ============================================================
# MAIN
# ============================================================

def main():
    parser = argparse.ArgumentParser(description='Kevinotron Orchestrator')
    parser.add_argument('--binary', default='./target/release/kevinotron',
                       help='Path to kevinotron binary')
    parser.add_argument('--groups', nargs='+', default=['g2'],
                       choices=['su2','su3','su4','g2','sp4','so7'])
    parser.add_argument('--ls', nargs='+', type=int, default=[4, 6, 8])
    parser.add_argument('--betas', nargs='+', type=float, default=None,
                       help='Override default betas (applies to all groups)')
    parser.add_argument('--n-alpha', type=int, default=11)
    parser.add_argument('--n-parallel', type=int, default=11,
                       help='Parallel alpha-point processes (default: 11 = all at once)')
    parser.add_argument('--n-therm', type=int, default=0, help='Override thermalization')
    parser.add_argument('--n-meas', type=int, default=0, help='Override measurements')
    parser.add_argument('--n-skip', type=int, default=5)
    parser.add_argument('--log-dir', default='results', help='Output directory')
    parser.add_argument('--analyze-only', action='store_true',
                       help='Only analyze existing results')
    parser.add_argument('--dump-config', action='store_true',
                       help='Also dump .npy config from alpha=0 run')
    args = parser.parse_args()

    os.makedirs(args.log_dir, exist_ok=True)

    if args.analyze_only:
        # Load previous results
        results_file = os.path.join(args.log_dir, 'all_results.json')
        if os.path.exists(results_file):
            with open(results_file) as f:
                all_results = json.load(f)
            analyze_results(all_results)
        else:
            print(f"No results file found at {results_file}")
        return

    # Check binary
    if not os.path.exists(args.binary):
        print(f"ERROR: binary not found at {args.binary}")
        print(f"Build with: cd kevinotron && cargo build --release")
        sys.exit(1)

    all_results = []

    for group in args.groups:
        betas = args.betas if args.betas else DEFAULT_BETAS.get(group, [10.0])
        n_therm = args.n_therm if args.n_therm > 0 else DEFAULT_THERM.get(group, 500)
        n_meas = args.n_meas if args.n_meas > 0 else DEFAULT_MEAS.get(group, 200)
        eps = DEFAULT_EPS.get(group, 0.15)

        for beta in betas:
            for ls in args.ls:
                result = run_full_ee(
                    args.binary, group, ls, beta,
                    args.n_alpha, args.n_parallel,
                    n_therm, n_meas, args.n_skip, eps,
                    args.log_dir,
                )
                if result:
                    all_results.append(result)

    # Save all results
    results_file = os.path.join(args.log_dir, 'all_results.json')
    with open(results_file, 'w') as f:
        json.dump(all_results, f, indent=2)
    print(f"\nSaved {len(all_results)} results to {results_file}")

    # Run analysis
    if all_results:
        analyze_results(all_results)


if __name__ == '__main__':
    main()
