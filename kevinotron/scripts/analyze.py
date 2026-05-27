#!/usr/bin/env python3
"""
KEVINOTRON ANALYSIS PIPELINE
==============================
Parse log outputs from kevinotron Rust binary, perform:
  1. Trapezoidal alpha-integration with error propagation
  2. Multi-L area law fit: S2/A = a_div + c/L^2
  3. Three-parameter regression: S2/A = f(beta, n_roots, dim_adj, L)
  4. PySR formula test
  5. Cross-group ratios and tables
  6. Comparison to kappa predictions
  7. Publication-ready LaTeX table output
  8. Leave-one-group-out cross-validation

Parses BOTH new format (# KEVINOTRON v1.x header + ALPHA lines)
and legacy format (g2_ee_L*_beta*_parallel.log from ~/g2_lattice_rs/).

Author: Kevin Remondiere (ORCID 0009-0008-2443-7166)
"""

import numpy as np
import os
import sys
import json
import re
import glob
import argparse
from scipy.optimize import curve_fit
from scipy.special import zeta as riemann_zeta

# ============================================================
# GROUP PROPERTIES DATABASE
# ============================================================

GROUP_PROPS = {
    'SU(2)': {'dim_fund': 2, 'dim_adj': 3,  'rank': 1, 'n_roots': 2,  'is_complex': True},
    'SU(3)': {'dim_fund': 3, 'dim_adj': 8,  'rank': 2, 'n_roots': 6,  'is_complex': True},
    'SU(4)': {'dim_fund': 4, 'dim_adj': 15, 'rank': 3, 'n_roots': 12, 'is_complex': True},
    'G2':    {'dim_fund': 7, 'dim_adj': 14, 'rank': 2, 'n_roots': 12, 'is_complex': False},
    'Sp(4)': {'dim_fund': 4, 'dim_adj': 10, 'rank': 2, 'n_roots': 8,  'is_complex': True},
    'SO(7)': {'dim_fund': 7, 'dim_adj': 21, 'rank': 3, 'n_roots': 18, 'is_complex': False},
}

# ============================================================
# PHYSICAL PREDICTIONS
# ============================================================

ZETA3 = riemann_zeta(3)  # 1.2020569...
KAPPA_INF = ZETA3 / np.sqrt(np.pi)  # 0.6782

PREDICTIONS = {
    'SU(2)': {
        'kappa_1_minus_1_N2': (1 - 1/4) * KAPPA_INF,     # 0.5087
        'kappa_sqrt_N_affine': 0.518 * np.sqrt(2) - 0.458, # 0.275
        'kappa_FP': 1/2,
    },
    'SU(3)': {
        'kappa_1_minus_1_N2': (1 - 1/9) * KAPPA_INF,     # 0.6029
        'kappa_sqrt_N_affine': 0.518 * np.sqrt(3) - 0.458, # 0.439
        'kappa_FP': 1/6,
    },
    'SU(4)': {
        'kappa_1_minus_1_N2': (1 - 1/16) * KAPPA_INF,    # 0.6358
        'kappa_sqrt_N_affine': 0.518 * 2.0 - 0.458,       # 0.578
        'kappa_FP': 1/12,
    },
    'G2': {
        'kappa_SU3_like': (1 - 1/9) * KAPPA_INF,          # 0.6027 (N=rank+1=3)
        'kappa_dim_law': (1 - 1/14) * KAPPA_INF,          # 0.6298 (dim=14)
        'kappa_sqrt_rank': 0.518 * np.sqrt(2) - 0.458,    # 0.275 (rank=2)
        'kappa_FP': 1/12,
    },
    'Sp(4)': {
        'kappa_1_minus_dim': (1 - 1/10) * KAPPA_INF,      # 0.6104
        'kappa_FP': 1/8,
    },
    'SO(7)': {
        'kappa_1_minus_dim': (1 - 1/21) * KAPPA_INF,      # 0.6459
        'kappa_FP': 1/30,
    },
}

# Best PySR formula from kevinotron_ml.py:
#   S2/A = 5.68 * beta - 4.05 * n_roots - dim_adj + 3.5 / L^2
def pysr_formula(beta, n_roots, dim_adj, L):
    """Best PySR symbolic regression formula."""
    return 5.68 * beta - 4.05 * n_roots - dim_adj + 3.5 / L**2


# ============================================================
# LOG PARSING -- NEW FORMAT (kevinotron v1.x)
# ============================================================

def parse_alpha_lines(filepath):
    """Parse ALPHA lines from any kevinotron log."""
    pairs = []
    with open(filepath) as f:
        for line in f:
            line = line.strip()
            m = re.match(r'ALPHA\s+([\d.]+)\s*:\s*dS/dalpha\s*=\s*([-\d.e+]+)\s*\+/-\s*([-\d.e+]+)', line)
            if m:
                alpha = float(m.group(1))
                ds = float(m.group(2))
                err = float(m.group(3))
                pairs.append((alpha, ds, err))
    pairs.sort(key=lambda x: x[0])
    return pairs


def parse_result_lines(filepath):
    """Parse RESULT lines."""
    results = {}
    with open(filepath) as f:
        for line in f:
            line = line.strip()
            if line.startswith('RESULT:'):
                parts = line.split()
                for p in parts[1:]:
                    if '=' in p:
                        k, v = p.split('=', 1)
                        try:
                            results[k] = float(v)
                        except ValueError:
                            results[k] = v
    return results


def extract_metadata(filepath):
    """Extract Ls, Lt, beta, group from log header (both old and new format)."""
    meta = {'ls': None, 'lt': None, 'beta': None, 'group': None}
    with open(filepath) as f:
        for line in f:
            # New format: "# Ls=8, Lt=16, beta=10"
            if 'Ls=' in line:
                m = re.search(r'Ls=(\d+)', line)
                if m: meta['ls'] = int(m.group(1))
                m = re.search(r'Lt=(\d+)', line)
                if m: meta['lt'] = int(m.group(1))
                m = re.search(r'beta=([\d.]+)', line)
                if m: meta['beta'] = float(m.group(1))

            # Group detection (priority: longer names first to avoid mismatches)
            if 'Sp(4)' in line or 'sp4' in line.lower():
                meta['group'] = 'Sp(4)'
            elif 'SO(7)' in line or 'so7' in line.lower():
                meta['group'] = 'SO(7)'
            elif 'SU(4)' in line or 'su4' in line.lower():
                meta['group'] = 'SU(4)'
            elif 'SU(3)' in line or 'su3' in line.lower():
                meta['group'] = 'SU(3)'
            elif 'SU(2)' in line or 'su2' in line.lower():
                meta['group'] = 'SU(2)'
            elif 'G2' in line or 'g2' in line.lower():
                meta['group'] = 'G2'

    # Fallback: try to infer from filename
    if meta['group'] is None:
        bname = os.path.basename(filepath).lower()
        if 'sp4' in bname: meta['group'] = 'Sp(4)'
        elif 'so7' in bname: meta['group'] = 'SO(7)'
        elif 'su4' in bname: meta['group'] = 'SU(4)'
        elif 'su3' in bname: meta['group'] = 'SU(3)'
        elif 'su2' in bname: meta['group'] = 'SU(2)'
        elif 'g2' in bname: meta['group'] = 'G2'

    if meta['ls'] is None:
        # Try old filename format: g2_ee_L8_beta10.0_parallel.log
        bname = os.path.basename(filepath)
        m = re.search(r'_L(\d+)_', bname)
        if m: meta['ls'] = int(m.group(1))
        m = re.search(r'_beta([\d.]+)', bname)
        if m: meta['beta'] = float(m.group(1))

    return meta


# ============================================================
# LEGACY FORMAT PARSING (g2_lattice_rs logs)
# ============================================================

def parse_legacy_log(filepath):
    """Parse legacy format: g2_ee_L*_beta*_parallel.log from old Rust binaries.

    These have lines like:
      alpha=0.000: <dS/dalpha> = 123.456 +/- 7.89
    or the newer ALPHA format.
    """
    pairs = []
    with open(filepath) as f:
        for line in f:
            line = line.strip()
            # Try new format first
            m = re.match(r'ALPHA\s+([\d.]+)\s*:\s*dS/dalpha\s*=\s*([-\d.e+]+)\s*\+/-\s*([-\d.e+]+)', line)
            if m:
                pairs.append((float(m.group(1)), float(m.group(2)), float(m.group(3))))
                continue
            # Try legacy format
            m = re.match(r'alpha=([\d.]+)\s*:\s*<dS/dalpha>\s*=\s*([-\d.e+]+)\s*\+/-\s*([-\d.e+]+)', line)
            if m:
                pairs.append((float(m.group(1)), float(m.group(2)), float(m.group(3))))
                continue
            # Another legacy variant
            m = re.match(r'([\d.]+)\s+([-\d.e+]+)\s+([-\d.e+]+)', line)
            if m and not line.startswith('#'):
                pairs.append((float(m.group(1)), float(m.group(2)), float(m.group(3))))

    pairs.sort(key=lambda x: x[0])
    return pairs


# ============================================================
# JSON PARSING (kevinotron v1.1 structured output)
# ============================================================

def load_json_results(json_files):
    """Load structured JSON results from kevinotron v1.1."""
    results = []
    for jf in json_files:
        if not os.path.exists(jf):
            continue
        with open(jf) as f:
            data = json.load(f)

        group = data.get('group', 'unknown')
        ls = data.get('ls')
        lt = data.get('lt', 2 * ls if ls else None)
        beta = data.get('beta')
        s2 = data.get('s2')
        area = data.get('area', ls * ls * lt if ls and lt else None)
        s2_err = data.get('s2_err_bootstrap', data.get('s2_err_propagated', 0))

        if s2 is not None and area:
            results.append({
                'file': jf,
                'group': group,
                'ls': ls,
                'lt': lt,
                'beta': beta,
                's2': s2,
                's2_err': s2_err,
                'area': area,
                's2_a': s2 / area,
                's2_a_err': s2_err / area,
                'n_alpha': data.get('n_alpha', 0),
                'source': 'json',
            })
    return results


# ============================================================
# INTEGRATION
# ============================================================

def trapezoidal_integrate(pairs):
    """Trapezoidal integration of dS/dalpha over alpha in [0,1]."""
    alphas = np.array([p[0] for p in pairs])
    ds_vals = np.array([p[1] for p in pairs])
    ds_errs = np.array([p[2] for p in pairs])

    S2 = np.trapezoid(ds_vals, alphas)

    # Error: sum of (da/2 * err)^2 for each pair
    S2_err_sq = 0.0
    for i in range(len(alphas) - 1):
        da = alphas[i+1] - alphas[i]
        S2_err_sq += (da/2)**2 * (ds_errs[i]**2 + ds_errs[i+1]**2)
    S2_err = np.sqrt(S2_err_sq)

    return S2, S2_err


# ============================================================
# MULTI-FILE ANALYSIS
# ============================================================

def process_logfiles(logfiles):
    """Process a list of log files into structured results."""
    results = []
    for lf in logfiles:
        if not os.path.exists(lf) or os.path.getsize(lf) == 0:
            continue

        meta = extract_metadata(lf)

        # Try new format first, then legacy
        pairs = parse_alpha_lines(lf)
        if not pairs:
            pairs = parse_legacy_log(lf)

        result_lines = parse_result_lines(lf)

        if not pairs:
            continue

        # Try to get S2 from RESULT lines first
        if 'S2' in result_lines and 'area' in result_lines:
            S2 = result_lines['S2']
            # Parse S2 error from the log format "S2=X +/- Y"
            S2_err = 0.0
            with open(lf) as f:
                for line in f:
                    m = re.match(r'RESULT:\s*S2=([-\d.e+]+)\s*\+/-\s*([-\d.e+]+)', line)
                    if m:
                        S2_err = float(m.group(2))
            # Prefer bootstrap error if available
            with open(lf) as f:
                for line in f:
                    m = re.match(r'RESULT:\s*S2_bootstrap=([-\d.e+]+)\s*\+/-\s*([-\d.e+]+)', line)
                    if m:
                        S2_err = float(m.group(2))
            area = result_lines['area']
        else:
            # Compute from alpha-integration
            S2, S2_err = trapezoidal_integrate(pairs)
            ls = meta['ls']
            lt = meta['lt'] if meta['lt'] else 2 * ls
            area = ls * ls * lt

        S2_A = S2 / area
        S2_A_err = S2_err / area

        results.append({
            'file': lf,
            'group': meta['group'],
            'ls': meta['ls'],
            'lt': meta['lt'],
            'beta': meta['beta'],
            's2': S2,
            's2_err': S2_err,
            'area': area,
            's2_a': S2_A,
            's2_a_err': S2_A_err,
            'n_alpha': len(pairs),
            'source': 'log',
        })

    return results


def area_law_fit(results_group):
    """Fit S2/A = a_inf + c/L^2 for one group."""
    Ls = np.array([r['ls'] for r in results_group])
    vals = np.array([r['s2_a'] for r in results_group])
    errs = np.array([r['s2_a_err'] for r in results_group])

    if len(Ls) < 3:
        return None

    def model(L, a_inf, c):
        return a_inf + c / L**2

    try:
        popt, pcov = curve_fit(model, Ls, vals, p0=[vals[-1], 1.0],
                               sigma=errs, absolute_sigma=True)
        perr = np.sqrt(np.diag(pcov))
        chi2 = np.sum(((vals - model(Ls, *popt)) / errs)**2)
        ndof = len(Ls) - 2
        return {
            'a_inf': popt[0], 'a_inf_err': perr[0],
            'c': popt[1], 'c_err': perr[1],
            'chi2': chi2, 'ndof': ndof,
        }
    except Exception:
        return None


def three_param_regression(results):
    """3-parameter regression: S2/A = a0 + a1*beta + a2*dim_adj + a3/L^2.

    Uses all data points across all groups.
    """
    rows = []
    for r in results:
        g = r['group']
        if g not in GROUP_PROPS:
            continue
        props = GROUP_PROPS[g]
        rows.append({
            'beta': r['beta'],
            'n_roots': props['n_roots'],
            'dim_adj': props['dim_adj'],
            'L': r['ls'],
            's2_a': r['s2_a'],
            's2_a_err': r['s2_a_err'],
        })

    if len(rows) < 5:
        return None

    X = np.array([[rr['beta'], rr['n_roots'], rr['dim_adj'], 1.0/rr['L']**2] for rr in rows])
    y = np.array([rr['s2_a'] for rr in rows])
    w = np.array([1.0/max(rr['s2_a_err'], 1e-10)**2 for rr in rows])

    # Weighted least squares
    Xw = X * np.sqrt(w)[:, None]
    yw = y * np.sqrt(w)
    try:
        coeffs, residuals, rank, sv = np.linalg.lstsq(Xw, yw, rcond=None)
        y_pred = X @ coeffs
        chi2 = np.sum(w * (y - y_pred)**2)
        ndof = len(y) - len(coeffs)
        return {
            'coeffs': coeffs.tolist(),
            'labels': ['beta', 'n_roots', 'dim_adj', '1/L^2'],
            'chi2': float(chi2),
            'ndof': int(ndof),
        }
    except Exception:
        return None


def pysr_formula_test(results):
    """Test the PySR formula: S2/A = 5.68*beta - 4.05*n_roots - dim_adj + 3.5/L^2."""
    rows = []
    for r in results:
        g = r['group']
        if g not in GROUP_PROPS:
            continue
        props = GROUP_PROPS[g]
        pred = pysr_formula(r['beta'], props['n_roots'], props['dim_adj'], r['ls'])
        rows.append({
            'group': g, 'L': r['ls'], 'beta': r['beta'],
            'measured': r['s2_a'], 'predicted': pred,
            'residual': r['s2_a'] - pred,
        })

    return rows


def leave_one_group_out_cv(results):
    """Leave-one-group-out cross-validation for the 3-param regression."""
    groups = sorted(set(r['group'] for r in results if r['group'] in GROUP_PROPS))
    cv_results = []

    for held_out in groups:
        train = [r for r in results if r['group'] != held_out and r['group'] in GROUP_PROPS]
        test = [r for r in results if r['group'] == held_out]

        if len(train) < 4 or not test:
            continue

        fit = three_param_regression(train)
        if fit is None:
            continue

        coeffs = np.array(fit['coeffs'])
        for r in test:
            props = GROUP_PROPS[r['group']]
            x = np.array([r['beta'], props['n_roots'], props['dim_adj'], 1.0/r['ls']**2])
            pred = float(x @ coeffs)
            cv_results.append({
                'held_out': held_out,
                'ls': r['ls'],
                'beta': r['beta'],
                'measured': r['s2_a'],
                'predicted': pred,
                'residual': r['s2_a'] - pred,
            })

    return cv_results


# ============================================================
# OUTPUT
# ============================================================

def print_table(results, title=""):
    """Print a formatted results table."""
    if title:
        print(f"\n{'='*70}")
        print(f"  {title}")
        print(f"{'='*70}")

    # Group by (group, beta)
    grouped = {}
    for r in results:
        key = (r['group'] or 'unknown', r.get('beta', 0))
        if key not in grouped:
            grouped[key] = []
        grouped[key].append(r)

    for (group, beta), rr in sorted(grouped.items()):
        rr.sort(key=lambda x: x.get('ls', 0) or 0)
        print(f"\n  {group} (beta={beta}):")
        print(f"  {'L':>4} | {'S2/A':>12} | {'error':>10} | {'n_alpha':>7} | {'source':>6}")
        print(f"  {'-'*4}-+-{'-'*12}-+-{'-'*10}-+-{'-'*7}-+-{'-'*6}")
        for r in rr:
            src = r.get('source', 'log')[:6]
            print(f"  {r['ls']:4d} | {r['s2_a']:12.6f} | {r['s2_a_err']:10.6f} | {r['n_alpha']:7d} | {src:>6}")

        # Area law fit
        fit = area_law_fit(rr)
        if fit:
            print(f"  Fit: S2/A = {fit['a_inf']:.6f}(+-{fit['a_inf_err']:.6f}) + {fit['c']:.2f}(+-{fit['c_err']:.2f})/L^2")
            print(f"  chi2/dof = {fit['chi2']:.2f}/{fit['ndof']}")


def print_latex_table(results):
    """Print LaTeX-ready table."""
    print("\n% LaTeX table (copy into paper)")
    print("\\begin{table}[h]")
    print("\\centering")
    print("\\begin{tabular}{l c c r@{$\\pm$}l}")
    print("\\hline\\hline")
    print("Group & $\\beta$ & $L$ & \\multicolumn{2}{c}{$S_2/A$} \\\\")
    print("\\hline")

    results_sorted = sorted(results, key=lambda r: (r['group'] or '', r.get('beta', 0), r.get('ls', 0)))
    for r in results_sorted:
        print(f"{r['group']} & {r['beta']:.2f} & {r['ls']} & {r['s2_a']:.4f} & {r['s2_a_err']:.4f} \\\\")

    print("\\hline\\hline")
    print("\\end{tabular}")
    print("\\caption{Entanglement entropy $S_2/A$ for 4D lattice gauge theories.}")
    print("\\label{tab:ee}")
    print("\\end{table}")


def print_ratios(results):
    """Print cross-group ratios."""
    by_group_L = {}
    for r in results:
        key = (r['group'], r.get('ls'))
        by_group_L[key] = r['s2_a']

    print(f"\n{'='*70}")
    print(f"  CROSS-GROUP RATIOS (vs SU(3))")
    print(f"{'='*70}")

    Ls = sorted(set(r.get('ls') for r in results if r.get('ls')))
    groups = sorted(set(r['group'] for r in results if r['group']))

    for g in groups:
        if g == 'SU(3)':
            continue
        ratios = []
        for L in Ls:
            if (g, L) in by_group_L and ('SU(3)', L) in by_group_L:
                r = by_group_L[(g, L)] / by_group_L[('SU(3)', L)]
                ratios.append((L, r))
        if ratios:
            mean_r = np.mean([r[1] for r in ratios])
            std_r = np.std([r[1] for r in ratios]) if len(ratios) > 1 else 0
            pairs_str = ", ".join([f"L={r[0]}:{r[1]:.4f}" for r in ratios])
            print(f"  {g}/SU(3): {pairs_str}  ->  mean={mean_r:.4f}+-{std_r:.4f}")


def print_predictions_comparison(results):
    """Compare measured S2/A to predicted kappa values."""
    print(f"\n{'='*70}")
    print(f"  PREDICTIONS vs MEASUREMENTS")
    print(f"{'='*70}")

    for group, preds in sorted(PREDICTIONS.items()):
        group_results = [r for r in results if r['group'] == group]
        if not group_results:
            continue

        # Use largest L for comparison
        group_results.sort(key=lambda r: r.get('ls', 0))
        best = group_results[-1]

        print(f"\n  {group} (L={best['ls']}, beta={best['beta']}):")
        print(f"    Measured S2/A = {best['s2_a']:.6f} +/- {best['s2_a_err']:.6f}")
        for name, val in sorted(preds.items()):
            diff = best['s2_a'] - val
            sigma = abs(diff) / max(best['s2_a_err'], 1e-10)
            print(f"    {name:30s} = {val:.6f}  (diff={diff:+.6f}, {sigma:.1f}sigma)")


# ============================================================
# MAIN
# ============================================================

def main():
    parser = argparse.ArgumentParser(description='Kevinotron Analysis Pipeline')
    parser.add_argument('logfiles', nargs='*', help='Log files to analyze')
    parser.add_argument('--glob', default='', help='Glob pattern for log files')
    parser.add_argument('--json', default='', help='JSON results file from orchestrator (all_results.json)')
    parser.add_argument('--json-dir', default='', help='Directory with per-run .json files from kevinotron v1.1')
    parser.add_argument('--legacy-dir', default='', help='Directory with legacy logs (~/g2_lattice_rs/)')
    parser.add_argument('--latex', action='store_true', help='Output LaTeX table')
    parser.add_argument('--ratios', action='store_true', help='Print cross-group ratios')
    parser.add_argument('--regression', action='store_true', help='Run 3-param regression')
    parser.add_argument('--pysr-test', action='store_true', help='Test PySR formula')
    parser.add_argument('--cv', action='store_true', help='Leave-one-group-out cross-validation')
    parser.add_argument('--predictions', action='store_true', help='Compare to kappa predictions')
    parser.add_argument('--all', action='store_true', help='Run all analyses')
    args = parser.parse_args()

    results = []

    # 1. Load from orchestrator JSON
    if args.json and os.path.exists(args.json):
        with open(args.json) as f:
            results.extend(json.load(f))

    # 2. Load per-run JSON files (kevinotron v1.1)
    if args.json_dir:
        json_files = glob.glob(os.path.join(args.json_dir, '*.json'))
        results.extend(load_json_results(json_files))

    # 3. Parse log files
    logfiles = list(args.logfiles)
    if args.glob:
        logfiles.extend(glob.glob(args.glob))

    # 4. Parse legacy logs
    if args.legacy_dir:
        logfiles.extend(glob.glob(os.path.join(args.legacy_dir, '*.log')))

    if not logfiles and not results:
        # Try default locations
        logfiles = glob.glob('results/*.log')
        logfiles.extend(glob.glob('*.json'))
        if not logfiles:
            logfiles = glob.glob(os.path.expanduser('~/g2_lattice_rs/*.log'))

    if logfiles:
        # Separate .json from .log
        json_files = [f for f in logfiles if f.endswith('.json')]
        log_files = [f for f in logfiles if not f.endswith('.json')]

        if json_files:
            results.extend(load_json_results(json_files))
        if log_files:
            results.extend(process_logfiles(log_files))

    if not results:
        print("No valid results found. Usage: analyze.py *.log or analyze.py --json results.json")
        sys.exit(1)

    # Deduplicate by (group, ls, beta)
    seen = set()
    unique_results = []
    for r in results:
        key = (r.get('group'), r.get('ls'), r.get('beta'))
        if key not in seen:
            seen.add(key)
            unique_results.append(r)
    results = unique_results

    print(f"Loaded {len(results)} data points from {len(set(r.get('group') for r in results))} groups")

    # Always print table
    print_table(results, "KEVINOTRON ANALYSIS RESULTS")

    run_all = args.all

    if args.ratios or run_all:
        print_ratios(results)

    if args.predictions or run_all:
        print_predictions_comparison(results)

    if args.regression or run_all:
        print(f"\n{'='*70}")
        print(f"  3-PARAMETER REGRESSION")
        print(f"{'='*70}")
        fit = three_param_regression(results)
        if fit:
            for label, coeff in zip(fit['labels'], fit['coeffs']):
                print(f"  {label:10s}: {coeff:+.4f}")
            print(f"  chi2/dof = {fit['chi2']:.2f}/{fit['ndof']}")
        else:
            print("  Not enough data for regression")

    if args.pysr_test or run_all:
        print(f"\n{'='*70}")
        print(f"  PySR FORMULA TEST")
        print(f"  S2/A = 5.68*beta - 4.05*n_roots - dim_adj + 3.5/L^2")
        print(f"{'='*70}")
        rows = pysr_formula_test(results)
        if rows:
            print(f"  {'Group':>6} {'L':>3} {'beta':>6} {'measured':>10} {'predicted':>10} {'residual':>10}")
            for rr in rows:
                print(f"  {rr['group']:>6} {rr['L']:3d} {rr['beta']:6.2f} {rr['measured']:10.4f} {rr['predicted']:10.4f} {rr['residual']:+10.4f}")
            rms = np.sqrt(np.mean([rr['residual']**2 for rr in rows]))
            print(f"  RMS residual: {rms:.4f}")

    if args.cv or run_all:
        print(f"\n{'='*70}")
        print(f"  LEAVE-ONE-GROUP-OUT CROSS-VALIDATION")
        print(f"{'='*70}")
        cv = leave_one_group_out_cv(results)
        if cv:
            for rr in cv:
                print(f"  held_out={rr['held_out']:>6} L={rr['ls']:3d}: meas={rr['measured']:.4f} pred={rr['predicted']:.4f} resid={rr['residual']:+.4f}")
            rms = np.sqrt(np.mean([rr['residual']**2 for rr in cv]))
            print(f"  RMS residual: {rms:.4f}")
        else:
            print("  Not enough data for cross-validation")

    if args.latex or run_all:
        print_latex_table(results)

    # Save processed results
    out = {
        'predictions': {g: {k: float(v) for k, v in preds.items()}
                        for g, preds in PREDICTIONS.items()},
        'group_properties': {g: {k: (int(v) if isinstance(v, (int, np.integer)) else bool(v) if isinstance(v, (bool, np.bool_)) else float(v))
                                  for k, v in props.items()}
                              for g, props in GROUP_PROPS.items()},
        'measurements': [{k: v for k, v in r.items() if k != 'file'}
                          for r in results],
    }
    with open('analysis_results.json', 'w') as f:
        json.dump(out, f, indent=2)
    print(f"\nSaved to analysis_results.json")


if __name__ == '__main__':
    main()
