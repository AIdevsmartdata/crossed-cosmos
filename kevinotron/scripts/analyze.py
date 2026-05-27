#!/usr/bin/env python3
"""
KEVINOTRON v2.0 ANALYSIS PIPELINE
====================================
Parse log outputs from kevinotron Rust binary (v1.x, v2.x, legacy g2_lattice_rs),
perform comprehensive analysis:

  1. Trapezoidal alpha-integration with error propagation
  2. Multi-L area law fit: S2/A = a_div + c/L^2
  3. Three-parameter regression: S2/A = f(beta, n_roots, dim_adj, L)
  4. PySR formula test + screening law
  5. Cross-group ratios and tables
  6. Comparison to kappa predictions
  7. Creutz ratio sigma*a^2 extraction
  8. Publication-ready LaTeX table output
  9. Leave-one-group-out cross-validation
 10. Structured JSON output with all data
 11. U(1) support

Parses ALL formats:
  - New format (# KEVINOTRON v1.x/v2.x header + ALPHA lines)
  - Legacy format (g2_ee_L*_beta*_parallel.log from ~/g2_lattice_rs/)
  - JSON structured output (kevinotron v1.1+)
  - Plaquette logs (PLAQ lines for Creutz ratio)

Usage:
  python3 analyze.py --all-logs ~/kevinotron/ ~/g2_lattice_rs/
  python3 analyze.py *.log --all
  python3 analyze.py --json results.json --latex --ratios

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
# GROUP PROPERTIES DATABASE (extended for v2.0)
# ============================================================

GROUP_PROPS = {
    'U(1)':  {'dim_fund': 1, 'dim_adj': 1,  'rank': 1, 'n_roots': 0,
              'C2_fund': 0.0,  'is_complex': True,  'n_pos_roots': 0},
    'SU(2)': {'dim_fund': 2, 'dim_adj': 3,  'rank': 1, 'n_roots': 2,
              'C2_fund': 0.75, 'is_complex': True,  'n_pos_roots': 1},
    'SU(3)': {'dim_fund': 3, 'dim_adj': 8,  'rank': 2, 'n_roots': 6,
              'C2_fund': 4/3,  'is_complex': True,  'n_pos_roots': 3},
    'SU(4)': {'dim_fund': 4, 'dim_adj': 15, 'rank': 3, 'n_roots': 12,
              'C2_fund': 15/8, 'is_complex': True,  'n_pos_roots': 6},
    'SU(5)': {'dim_fund': 5, 'dim_adj': 24, 'rank': 4, 'n_roots': 20,
              'C2_fund': 12/5, 'is_complex': True,  'n_pos_roots': 10},
    'G2':    {'dim_fund': 7, 'dim_adj': 14, 'rank': 2, 'n_roots': 12,
              'C2_fund': 2.0,  'is_complex': False, 'n_pos_roots': 6},
    'Sp(4)': {'dim_fund': 4, 'dim_adj': 10, 'rank': 2, 'n_roots': 8,
              'C2_fund': 15/8, 'is_complex': True,  'n_pos_roots': 4},
    'SO(7)': {'dim_fund': 7, 'dim_adj': 21, 'rank': 3, 'n_roots': 18,
              'C2_fund': 3.0,  'is_complex': False, 'n_pos_roots': 9},
}

# ============================================================
# PHYSICAL PREDICTIONS
# ============================================================

ZETA3 = riemann_zeta(3)  # 1.2020569...
KAPPA_INF = ZETA3 / np.sqrt(np.pi)  # 0.6782

PREDICTIONS = {
    'SU(2)': {
        'kappa_1_minus_1_N2': (1 - 1/4) * KAPPA_INF,
        'kappa_sqrt_N_affine': 0.518 * np.sqrt(2) - 0.458,
        'kappa_FP': 1/2,
    },
    'SU(3)': {
        'kappa_1_minus_1_N2': (1 - 1/9) * KAPPA_INF,
        'kappa_sqrt_N_affine': 0.518 * np.sqrt(3) - 0.458,
        'kappa_FP': 1/6,
    },
    'SU(4)': {
        'kappa_1_minus_1_N2': (1 - 1/16) * KAPPA_INF,
        'kappa_sqrt_N_affine': 0.518 * 2.0 - 0.458,
        'kappa_FP': 1/12,
    },
    'SU(5)': {
        'kappa_1_minus_1_N2': (1 - 1/25) * KAPPA_INF,
        'kappa_sqrt_N_affine': 0.518 * np.sqrt(5) - 0.458,
        'kappa_FP': 1/20,
    },
    'G2': {
        'kappa_SU3_like': (1 - 1/9) * KAPPA_INF,
        'kappa_dim_law': (1 - 1/14) * KAPPA_INF,
        'kappa_sqrt_rank': 0.518 * np.sqrt(2) - 0.458,
        'kappa_FP': 1/12,
    },
    'Sp(4)': {
        'kappa_1_minus_dim': (1 - 1/10) * KAPPA_INF,
        'kappa_FP': 1/8,
    },
    'SO(7)': {
        'kappa_1_minus_dim': (1 - 1/21) * KAPPA_INF,
        'kappa_FP': 1/30,
    },
}


# ============================================================
# FORMULAS
# ============================================================

def pysr_formula(beta, n_roots, dim_adj, L):
    """Best PySR symbolic regression formula.
    S2/A = 5.68 * beta - 4.05 * n_roots - dim_adj + 3.5 / L^2
    """
    return 5.68 * beta - 4.05 * n_roots - dim_adj + 3.5 / L**2


def screening_law(beta, dim_adj, C2, rank, L):
    """PySR screening law variant.
    S2/A ~ beta * C2 / dim_adj - rank + c/L^2
    """
    return beta * C2 / dim_adj - rank + 2.0 / L**2


# ============================================================
# LOG PARSING -- ALL FORMATS
# ============================================================

def parse_alpha_lines(filepath):
    """Parse ALPHA lines from any kevinotron log."""
    pairs = []
    with open(filepath) as f:
        for line in f:
            line = line.strip()
            m = re.match(
                r'ALPHA\s+([\d.]+)\s*:\s*dS/dalpha\s*=\s*([-\d.e+]+)\s*\+/-\s*([-\d.e+]+)',
                line)
            if m:
                pairs.append((float(m.group(1)), float(m.group(2)), float(m.group(3))))
    pairs.sort(key=lambda x: x[0])
    return pairs


def parse_legacy_log(filepath):
    """Parse legacy format: g2_ee_L*_beta*_parallel.log from old Rust binaries.

    Handles:
      ALPHA 0.000 : dS/dalpha = 123.456 +/- 7.89
      alpha=0.000: <dS/dalpha> = 123.456 +/- 7.89
      0.000  123.456  7.89  (bare 3-column)
    """
    pairs = []
    with open(filepath) as f:
        for line in f:
            line = line.strip()
            # New ALPHA format
            m = re.match(
                r'ALPHA\s+([\d.]+)\s*:\s*dS/dalpha\s*=\s*([-\d.e+]+)\s*\+/-\s*([-\d.e+]+)',
                line)
            if m:
                pairs.append((float(m.group(1)), float(m.group(2)), float(m.group(3))))
                continue
            # Legacy alpha= format
            m = re.match(
                r'alpha=([\d.]+)\s*:\s*<dS/dalpha>\s*=\s*([-\d.e+]+)\s*\+/-\s*([-\d.e+]+)',
                line)
            if m:
                pairs.append((float(m.group(1)), float(m.group(2)), float(m.group(3))))
                continue
            # Bare 3-column (alpha, ds, err)
            m = re.match(r'([\d.]+)\s+([-\d.e+]+)\s+([-\d.e+]+)', line)
            if m and not line.startswith('#'):
                pairs.append((float(m.group(1)), float(m.group(2)), float(m.group(3))))

    pairs.sort(key=lambda x: x[0])
    return pairs


def parse_result_lines(filepath):
    """Parse RESULT lines (kevinotron v1.x+)."""
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


def parse_plaquette_lines(filepath):
    """Parse PLAQ lines for Creutz ratio extraction.

    Handles:
      PLAQ: <P> = 0.5678 +/- 0.0012
      PLAQ 0.5678
      plaquette = 0.5678
    """
    plaq_vals = []
    with open(filepath) as f:
        for line in f:
            line = line.strip()
            m = re.match(r'PLAQ\s*:?\s*<?P>?\s*=?\s*([\d.e+-]+)', line, re.IGNORECASE)
            if m:
                plaq_vals.append(float(m.group(1)))
                continue
            m = re.match(r'plaquette\s*=\s*([\d.e+-]+)', line, re.IGNORECASE)
            if m:
                plaq_vals.append(float(m.group(1)))
    return plaq_vals


def parse_wilson_loops(filepath):
    """Parse Wilson loop W(R,T) data for Creutz ratio."""
    loops = {}
    with open(filepath) as f:
        for line in f:
            line = line.strip()
            m = re.match(r'W\((\d+),(\d+)\)\s*=\s*([-\d.e+]+)\s*\+/-\s*([-\d.e+]+)', line)
            if m:
                R, T = int(m.group(1)), int(m.group(2))
                val, err = float(m.group(3)), float(m.group(4))
                loops[(R, T)] = (val, err)
    return loops


def extract_metadata(filepath):
    """Extract Ls, Lt, beta, group from log header (both old and new format)."""
    meta = {'ls': None, 'lt': None, 'beta': None, 'group': None, 'version': None}
    with open(filepath) as f:
        for line in f:
            # Version detection
            m = re.search(r'KEVINOTRON\s+v?([\d.]+)', line, re.IGNORECASE)
            if m:
                meta['version'] = m.group(1)

            # New format: "# Ls=8, Lt=16, beta=10"
            if 'Ls=' in line:
                m = re.search(r'Ls=(\d+)', line)
                if m:
                    meta['ls'] = int(m.group(1))
                m = re.search(r'Lt=(\d+)', line)
                if m:
                    meta['lt'] = int(m.group(1))
                m = re.search(r'beta=([\d.]+)', line)
                if m:
                    meta['beta'] = float(m.group(1))

            # v2.0 format: "GROUP: SU(3)" or "group=su3"
            m = re.search(r'GROUP:\s*(\S+)', line, re.IGNORECASE)
            if m:
                meta['group'] = _normalize_group_name(m.group(1))
            m = re.search(r'group=(\S+)', line, re.IGNORECASE)
            if m and meta['group'] is None:
                meta['group'] = _normalize_group_name(m.group(1))

            # Group detection from any line (priority: longer names first)
            if meta['group'] is None:
                if 'Sp(4)' in line or 'sp4' in line.lower():
                    meta['group'] = 'Sp(4)'
                elif 'SO(7)' in line or 'so7' in line.lower():
                    meta['group'] = 'SO(7)'
                elif 'SU(5)' in line or 'su5' in line.lower():
                    meta['group'] = 'SU(5)'
                elif 'SU(4)' in line or 'su4' in line.lower():
                    meta['group'] = 'SU(4)'
                elif 'SU(3)' in line or 'su3' in line.lower():
                    meta['group'] = 'SU(3)'
                elif 'SU(2)' in line or 'su2' in line.lower():
                    meta['group'] = 'SU(2)'
                elif 'U(1)' in line or 'u1' in line.lower():
                    meta['group'] = 'U(1)'
                elif 'G2' in line or 'g2' in line.lower():
                    meta['group'] = 'G2'

    # Fallback: try to infer from filename
    if meta['group'] is None:
        bname = os.path.basename(filepath).lower()
        meta['group'] = _normalize_group_name(bname)

    if meta['ls'] is None:
        bname = os.path.basename(filepath)
        m = re.search(r'_L(\d+)_', bname)
        if m:
            meta['ls'] = int(m.group(1))
        m = re.search(r'_beta([\d.]+)', bname)
        if m:
            meta['beta'] = float(m.group(1))

    return meta


def _normalize_group_name(s):
    """Normalize group name from various formats."""
    s_lower = s.lower().replace(' ', '').replace('_', '')
    mapping = {
        'u1': 'U(1)', 'u(1)': 'U(1)',
        'su2': 'SU(2)', 'su(2)': 'SU(2)',
        'su3': 'SU(3)', 'su(3)': 'SU(3)',
        'su4': 'SU(4)', 'su(4)': 'SU(4)',
        'su5': 'SU(5)', 'su(5)': 'SU(5)',
        'g2': 'G2',
        'sp4': 'Sp(4)', 'sp(4)': 'Sp(4)',
        'so7': 'SO(7)', 'so(7)': 'SO(7)',
    }
    for key, val in mapping.items():
        if key in s_lower:
            return val
    return None


# ============================================================
# JSON PARSING (kevinotron v1.1+ structured output)
# ============================================================

def load_json_results(json_files):
    """Load structured JSON results from kevinotron v1.1+."""
    results = []
    for jf in json_files:
        if not os.path.exists(jf):
            continue
        with open(jf) as f:
            try:
                data = json.load(f)
            except json.JSONDecodeError:
                continue

        # Handle both single-result and array-of-results
        if isinstance(data, list):
            for item in data:
                r = _parse_json_entry(item, jf)
                if r:
                    results.append(r)
        elif isinstance(data, dict):
            r = _parse_json_entry(data, jf)
            if r:
                results.append(r)
    return results


def _parse_json_entry(data, filepath):
    """Parse one JSON result entry."""
    group = data.get('group', 'unknown')
    if group != 'unknown':
        group = _normalize_group_name(group) or group
    ls = data.get('ls')
    lt = data.get('lt', 2 * ls if ls else None)
    beta = data.get('beta')
    s2 = data.get('s2', data.get('S2'))
    area = data.get('area', ls * ls * lt if ls and lt else None)
    s2_err = data.get('s2_err_bootstrap', data.get('s2_err_propagated',
             data.get('s2_err', 0)))

    if s2 is not None and area:
        return {
            'file': filepath,
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
            'plaquette': data.get('plaquette'),
        }
    return None


# ============================================================
# INTEGRATION
# ============================================================

def trapezoidal_integrate(pairs):
    """Trapezoidal integration of dS/dalpha over alpha in [0,1]."""
    alphas = np.array([p[0] for p in pairs])
    ds_vals = np.array([p[1] for p in pairs])
    ds_errs = np.array([p[2] for p in pairs])

    S2 = np.trapezoid(ds_vals, alphas)

    # Error: sum of (da/2 * err)^2 for each interval endpoint
    S2_err_sq = 0.0
    for i in range(len(alphas) - 1):
        da = alphas[i + 1] - alphas[i]
        S2_err_sq += (da / 2)**2 * (ds_errs[i]**2 + ds_errs[i + 1]**2)
    S2_err = np.sqrt(S2_err_sq)

    return S2, S2_err


# ============================================================
# CREUTZ RATIO
# ============================================================

def creutz_ratio(wilson_loops, R=1, T=1):
    """Compute Creutz ratio chi(R,T) = -ln(W(R,T)*W(R-1,T-1)/(W(R,T-1)*W(R-1,T))).

    sigma*a^2 ~ chi(R,T) at large R,T.
    Returns (chi, chi_err) or None.
    """
    keys_needed = [(R, T), (R - 1, T - 1), (R, T - 1), (R - 1, T)]
    for k in keys_needed:
        if k not in wilson_loops or k[0] < 1 or k[1] < 1:
            return None

    W_RT, e_RT = wilson_loops[(R, T)]
    W_11, e_11 = wilson_loops[(R - 1, T - 1)]
    W_R1, e_R1 = wilson_loops[(R, T - 1)]
    W_1T, e_1T = wilson_loops[(R - 1, T)]

    if W_RT <= 0 or W_11 <= 0 or W_R1 <= 0 or W_1T <= 0:
        return None

    ratio = (W_RT * W_11) / (W_R1 * W_1T)
    if ratio <= 0:
        return None

    chi = -np.log(ratio)

    # Error propagation (relative errors sum in quadrature for log of product)
    rel_err = np.sqrt((e_RT / W_RT)**2 + (e_11 / W_11)**2 +
                       (e_R1 / W_R1)**2 + (e_1T / W_1T)**2)
    chi_err = rel_err  # d(log(x)) ~ dx/x

    return chi, chi_err


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
        plaq_vals = parse_plaquette_lines(lf)
        wilson_loops = parse_wilson_loops(lf)

        if not pairs and not result_lines:
            continue

        # Try to get S2 from RESULT lines first
        if 'S2' in result_lines and 'area' in result_lines:
            S2 = result_lines['S2']
            S2_err = 0.0
            with open(lf) as f:
                for line in f:
                    m = re.match(r'RESULT:\s*S2=([-\d.e+]+)\s*\+/-\s*([-\d.e+]+)', line)
                    if m:
                        S2_err = float(m.group(2))
            with open(lf) as f:
                for line in f:
                    m = re.match(r'RESULT:\s*S2_bootstrap=([-\d.e+]+)\s*\+/-\s*([-\d.e+]+)', line)
                    if m:
                        S2_err = float(m.group(2))
            area = result_lines['area']
        elif pairs:
            S2, S2_err = trapezoidal_integrate(pairs)
            ls = meta['ls']
            lt = meta['lt'] if meta['lt'] else (2 * ls if ls else None)
            area = ls * ls * lt if ls and lt else None
        else:
            continue

        if area is None or area == 0:
            continue

        S2_A = S2 / area
        S2_A_err = S2_err / area

        entry = {
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
            'version': meta.get('version'),
        }

        if plaq_vals:
            entry['plaquette'] = np.mean(plaq_vals)
            entry['plaquette_err'] = np.std(plaq_vals) / np.sqrt(len(plaq_vals)) if len(plaq_vals) > 1 else 0

        # Creutz ratio from Wilson loops
        if wilson_loops:
            for R in range(2, 5):
                for T in range(2, 5):
                    cr = creutz_ratio(wilson_loops, R, T)
                    if cr is not None:
                        entry[f'creutz_{R}_{T}'] = cr[0]
                        entry[f'creutz_{R}_{T}_err'] = cr[1]

        results.append(entry)

    return results


def scan_directories(dirs):
    """Recursively scan directories for log and JSON files."""
    all_files = []
    for d in dirs:
        d = os.path.expanduser(d)
        if os.path.isfile(d):
            all_files.append(d)
        elif os.path.isdir(d):
            for ext in ('*.log', '*.json', '*.out', '*.dat'):
                all_files.extend(glob.glob(os.path.join(d, '**', ext), recursive=True))
    return sorted(set(all_files))


# ============================================================
# ANALYSIS FUNCTIONS
# ============================================================

def area_law_fit(results_group):
    """Fit S2/A = a_inf + c/L^2 for one group at fixed beta."""
    Ls = np.array([r['ls'] for r in results_group if r.get('ls')])
    vals = np.array([r['s2_a'] for r in results_group if r.get('ls')])
    errs = np.array([r['s2_a_err'] for r in results_group if r.get('ls')])

    if len(Ls) < 3:
        return None

    # Guard against zero errors
    errs = np.where(errs < 1e-10, 1.0, errs)

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


def slope_analysis(results_group):
    """Compute dS2/dA slope for multi-L data at fixed beta."""
    data = [(r['ls'], r['s2']) for r in results_group
            if r.get('ls') and r.get('s2')]
    if len(data) < 2:
        return None

    data.sort()
    Ls = np.array([d[0] for d in data])
    S2s = np.array([d[1] for d in data])
    areas = np.array([L**2 * 2 * L for L in Ls])

    # Linear fit S2 = slope * A + intercept
    try:
        coeffs = np.polyfit(areas, S2s, 1)
        slope = coeffs[0]
        intercept = coeffs[1]
        S2_pred = np.polyval(coeffs, areas)
        residuals = S2s - S2_pred
        return {
            'slope': slope, 'intercept': intercept,
            'rms_residual': np.sqrt(np.mean(residuals**2)),
        }
    except Exception:
        return None


def three_param_regression(results):
    """3-parameter regression: S2/A = a0 + a1*beta + a2*dim_adj + a3/L^2."""
    rows = []
    for r in results:
        g = r['group']
        if g not in GROUP_PROPS or r.get('ls') is None:
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

    X = np.array([[rr['beta'], rr['n_roots'], rr['dim_adj'], 1.0 / rr['L']**2]
                   for rr in rows])
    y = np.array([rr['s2_a'] for rr in rows])
    w = np.array([1.0 / max(rr['s2_a_err'], 1e-10)**2 for rr in rows])

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
    """Test the PySR formula + screening law."""
    rows = []
    for r in results:
        g = r['group']
        if g not in GROUP_PROPS or r.get('ls') is None:
            continue
        props = GROUP_PROPS[g]
        pred_pysr = pysr_formula(r['beta'], props['n_roots'], props['dim_adj'], r['ls'])
        pred_screen = screening_law(
            r['beta'], props['dim_adj'], props.get('C2_fund', 1.0),
            props['rank'], r['ls'])
        rows.append({
            'group': g, 'L': r['ls'], 'beta': r['beta'],
            'measured': r['s2_a'],
            'pred_pysr': pred_pysr,
            'resid_pysr': r['s2_a'] - pred_pysr,
            'pred_screen': pred_screen,
            'resid_screen': r['s2_a'] - pred_screen,
        })
    return rows


def leave_one_group_out_cv(results):
    """Leave-one-group-out cross-validation for the 3-param regression."""
    groups = sorted(set(r['group'] for r in results
                        if r['group'] in GROUP_PROPS and r.get('ls')))
    cv_results = []

    for held_out in groups:
        train = [r for r in results
                 if r['group'] != held_out and r['group'] in GROUP_PROPS and r.get('ls')]
        test = [r for r in results if r['group'] == held_out and r.get('ls')]

        if len(train) < 4 or not test:
            continue

        fit = three_param_regression(train)
        if fit is None:
            continue

        coeffs = np.array(fit['coeffs'])
        for r in test:
            props = GROUP_PROPS[r['group']]
            x = np.array([r['beta'], props['n_roots'], props['dim_adj'], 1.0 / r['ls']**2])
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
        print(f"\n{'='*80}")
        print(f"  {title}")
        print(f"{'='*80}")

    grouped = {}
    for r in results:
        key = (r.get('group') or 'unknown', r.get('beta', 0))
        if key not in grouped:
            grouped[key] = []
        grouped[key].append(r)

    for (group, beta), rr in sorted(grouped.items()):
        rr.sort(key=lambda x: x.get('ls', 0) or 0)
        print(f"\n  {group} (beta={beta}):")
        header = f"  {'L':>4} | {'S2/A':>12} | {'error':>10} | {'n_alpha':>7} | {'source':>6}"
        if any('plaquette' in r for r in rr):
            header += f" | {'<P>':>8}"
        print(header)
        print(f"  {'-'*len(header)}")
        for r in rr:
            src = r.get('source', 'log')[:6]
            line = f"  {r.get('ls', 0):4d} | {r['s2_a']:12.6f} | {r['s2_a_err']:10.6f} | {r.get('n_alpha', 0):7d} | {src:>6}"
            if 'plaquette' in r and r['plaquette'] is not None:
                line += f" | {r['plaquette']:8.4f}"
            print(line)

        # Area law fit
        fit = area_law_fit(rr)
        if fit:
            print(f"  Fit: S2/A = {fit['a_inf']:.6f}(+-{fit['a_inf_err']:.6f}) "
                  f"+ {fit['c']:.2f}(+-{fit['c_err']:.2f})/L^2")
            print(f"  chi2/dof = {fit['chi2']:.2f}/{fit['ndof']}")

        # Slope
        sl = slope_analysis(rr)
        if sl:
            print(f"  Slope: dS2/dA = {sl['slope']:.6f}, intercept = {sl['intercept']:.2f}")

        # Creutz ratios
        creutz_found = False
        for r in rr:
            for key in sorted(r.keys()):
                if key.startswith('creutz_') and not key.endswith('_err'):
                    if not creutz_found:
                        print(f"  Creutz ratios (sigma*a^2):")
                        creutz_found = True
                    R, T = key.split('_')[1], key.split('_')[2]
                    err_key = f"{key}_err"
                    err = r.get(err_key, 0)
                    print(f"    chi({R},{T}) = {r[key]:.6f} +/- {err:.6f}")


def print_latex_table(results):
    """Print LaTeX-ready table."""
    print("\n% LaTeX table -- Kevinotron v2.0 (copy into paper)")
    print("\\begin{table}[h]")
    print("\\centering")
    print("\\caption{Entanglement entropy $S_2/A$ for 4D lattice gauge theories "
          "measured via $\\alpha$-integration (BP2008b method).}")
    print("\\label{tab:ee_v2}")
    print("\\begin{tabular}{l c c c r@{$\\pm$}l}")
    print("\\hline\\hline")
    print("Group & $d_{\\mathrm{adj}}$ & $\\beta$ & $L$ & "
          "\\multicolumn{2}{c}{$S_2/A$} \\\\")
    print("\\hline")

    results_sorted = sorted(results,
        key=lambda r: (r.get('group') or '', r.get('beta', 0), r.get('ls', 0)))

    prev_group = None
    for r in results_sorted:
        grp = r.get('group', '')
        d_adj = GROUP_PROPS.get(grp, {}).get('dim_adj', '?')
        if grp != prev_group and prev_group is not None:
            print("\\hline")
        prev_group = grp

        # Format S2/A with appropriate precision
        if r['s2_a_err'] > 0.01:
            fmt_val, fmt_err = f"{r['s2_a']:.2f}", f"{r['s2_a_err']:.2f}"
        else:
            fmt_val, fmt_err = f"{r['s2_a']:.4f}", f"{r['s2_a_err']:.4f}"

        grp_latex = grp.replace('SU(', 'SU(').replace('Sp(', 'Sp(')  # already OK
        if grp == 'G2':
            grp_latex = '$G_2$'
        print(f"{grp_latex} & {d_adj} & {r.get('beta', 0):.2f} & "
              f"{r.get('ls', 0)} & {fmt_val} & {fmt_err} \\\\")

    print("\\hline\\hline")
    print("\\end{tabular}")
    print("\\end{table}")


def print_ratios(results):
    """Print cross-group ratios."""
    by_group_beta_L = {}
    for r in results:
        key = (r['group'], r.get('beta'), r.get('ls'))
        by_group_beta_L[key] = r['s2_a']

    print(f"\n{'='*80}")
    print(f"  CROSS-GROUP RATIOS (vs SU(3))")
    print(f"{'='*80}")

    Ls = sorted(set(r.get('ls') for r in results if r.get('ls')))
    groups = sorted(set(r['group'] for r in results if r['group']))

    # Find SU(3) reference beta
    su3_betas = sorted(set(r.get('beta') for r in results
                           if r.get('group') == 'SU(3)'))
    if not su3_betas:
        print("  No SU(3) data for ratio computation")
        return

    for g in groups:
        if g == 'SU(3)':
            continue
        ratios_found = []
        for L in Ls:
            for su3_beta in su3_betas:
                if ('SU(3)', su3_beta, L) in by_group_beta_L:
                    su3_val = by_group_beta_L[('SU(3)', su3_beta, L)]
                    # Find matching L for this group (any beta)
                    for key, val in by_group_beta_L.items():
                        if key[0] == g and key[2] == L:
                            r = val / su3_val
                            ratios_found.append((L, key[1], r))
        if ratios_found:
            mean_r = np.mean([r[2] for r in ratios_found])
            std_r = np.std([r[2] for r in ratios_found]) if len(ratios_found) > 1 else 0
            details = ", ".join([f"L={r[0]}:{r[2]:.4f}" for r in ratios_found[:5]])
            print(f"  {g}/SU(3): {details}  ->  mean={mean_r:.4f}+-{std_r:.4f}")


def print_predictions_comparison(results):
    """Compare measured S2/A to predicted kappa values."""
    print(f"\n{'='*80}")
    print(f"  PREDICTIONS vs MEASUREMENTS")
    print(f"{'='*80}")

    for group, preds in sorted(PREDICTIONS.items()):
        group_results = [r for r in results if r['group'] == group]
        if not group_results:
            continue

        group_results.sort(key=lambda r: r.get('ls', 0))
        best = group_results[-1]

        print(f"\n  {group} (L={best.get('ls')}, beta={best.get('beta')}):")
        print(f"    Measured S2/A = {best['s2_a']:.6f} +/- {best['s2_a_err']:.6f}")
        for name, val in sorted(preds.items()):
            diff = best['s2_a'] - val
            sigma = abs(diff) / max(best['s2_a_err'], 1e-10)
            print(f"    {name:30s} = {val:.6f}  (diff={diff:+.6f}, {sigma:.1f}sigma)")


def build_structured_json(results):
    """Build comprehensive structured JSON output."""
    output = {
        'metadata': {
            'version': '2.0',
            'author': 'Kevin Remondiere (ORCID 0009-0008-2443-7166)',
            'constants': {
                'zeta3': float(ZETA3),
                'kappa_inf': float(KAPPA_INF),
            },
        },
        'group_properties': {
            g: {k: (int(v) if isinstance(v, (int, np.integer))
                     else bool(v) if isinstance(v, (bool, np.bool_))
                     else float(v))
                for k, v in props.items()}
            for g, props in GROUP_PROPS.items()
        },
        'predictions': {
            g: {k: float(v) for k, v in preds.items()}
            for g, preds in PREDICTIONS.items()
        },
        'measurements': [],
    }

    for r in results:
        entry = {}
        for k, v in r.items():
            if k == 'file':
                entry['file'] = str(v)
            elif isinstance(v, (np.floating, np.integer)):
                entry[k] = float(v)
            elif isinstance(v, np.bool_):
                entry[k] = bool(v)
            else:
                entry[k] = v
        output['measurements'].append(entry)

    # Add fit results per group
    grouped = {}
    for r in results:
        key = (r.get('group', 'unknown'), r.get('beta', 0))
        if key not in grouped:
            grouped[key] = []
        grouped[key].append(r)

    fits = {}
    for (group, beta), rr in grouped.items():
        fit = area_law_fit(rr)
        if fit:
            fits[f"{group}_beta{beta}"] = fit
        sl = slope_analysis(rr)
        if sl:
            fits[f"{group}_beta{beta}_slope"] = sl

    output['fits'] = fits

    # Regression
    reg = three_param_regression(results)
    if reg:
        output['regression'] = reg

    return output


# ============================================================
# MAIN
# ============================================================

def main():
    parser = argparse.ArgumentParser(
        description='Kevinotron v2.0 Analysis Pipeline')
    parser.add_argument('logfiles', nargs='*', help='Log files to analyze')
    parser.add_argument('--glob', default='', help='Glob pattern for log files')
    parser.add_argument('--json', default='',
                        help='JSON results file (all_results.json)')
    parser.add_argument('--json-dir', default='',
                        help='Directory with per-run .json files')
    parser.add_argument('--legacy-dir', default='',
                        help='Directory with legacy logs (~/g2_lattice_rs/)')
    parser.add_argument('--all-logs', nargs='+', default=[],
                        help='Directories to scan recursively for all log formats')
    parser.add_argument('--latex', action='store_true', help='Output LaTeX table')
    parser.add_argument('--ratios', action='store_true', help='Cross-group ratios')
    parser.add_argument('--regression', action='store_true', help='3-param regression')
    parser.add_argument('--pysr-test', action='store_true',
                        help='Test PySR + screening formulas')
    parser.add_argument('--cv', action='store_true',
                        help='Leave-one-group-out cross-validation')
    parser.add_argument('--predictions', action='store_true',
                        help='Compare to kappa predictions')
    parser.add_argument('--all', action='store_true', help='Run all analyses')
    parser.add_argument('--output-json', default='analysis_results.json',
                        help='Output JSON path')
    args = parser.parse_args()

    results = []

    # 1. Load from orchestrator JSON
    if args.json and os.path.exists(args.json):
        with open(args.json) as f:
            try:
                loaded = json.load(f)
                if isinstance(loaded, list):
                    results.extend(loaded)
                elif isinstance(loaded, dict) and 'measurements' in loaded:
                    results.extend(loaded['measurements'])
            except json.JSONDecodeError:
                pass

    # 2. Load per-run JSON files
    if args.json_dir:
        json_files = glob.glob(os.path.join(args.json_dir, '*.json'))
        results.extend(load_json_results(json_files))

    # 3. Parse explicit log files
    logfiles = list(args.logfiles)
    if args.glob:
        logfiles.extend(glob.glob(args.glob))

    # 4. Parse legacy logs
    if args.legacy_dir:
        logfiles.extend(glob.glob(os.path.join(args.legacy_dir, '*.log')))

    # 5. Scan directories recursively
    if args.all_logs:
        all_scanned = scan_directories(args.all_logs)
        json_scanned = [f for f in all_scanned if f.endswith('.json')]
        log_scanned = [f for f in all_scanned if not f.endswith('.json')]
        if json_scanned:
            results.extend(load_json_results(json_scanned))
        if log_scanned:
            logfiles.extend(log_scanned)

    # 6. Try defaults if nothing found
    if not logfiles and not results:
        logfiles = glob.glob('results/*.log')
        logfiles.extend(glob.glob('*.json'))
        if not logfiles:
            logfiles = glob.glob(os.path.expanduser('~/g2_lattice_rs/*.log'))
            logfiles.extend(glob.glob(os.path.expanduser('~/kevinotron/results/*.log')))

    if logfiles:
        json_files = [f for f in logfiles if f.endswith('.json')]
        log_files = [f for f in logfiles if not f.endswith('.json')]
        if json_files:
            results.extend(load_json_results(json_files))
        if log_files:
            results.extend(process_logfiles(log_files))

    if not results:
        print("No valid results found.")
        print("Usage: analyze.py *.log")
        print("       analyze.py --all-logs ~/kevinotron/ ~/g2_lattice_rs/")
        print("       analyze.py --json results.json")
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

    n_groups = len(set(r.get('group') for r in results))
    print(f"Loaded {len(results)} data points from {n_groups} groups")
    print(f"Groups: {sorted(set(r.get('group', '?') for r in results))}")

    # Always print table
    print_table(results, "KEVINOTRON v2.0 ANALYSIS RESULTS")

    run_all = args.all

    if args.ratios or run_all:
        print_ratios(results)

    if args.predictions or run_all:
        print_predictions_comparison(results)

    if args.regression or run_all:
        print(f"\n{'='*80}")
        print(f"  3-PARAMETER REGRESSION")
        print(f"{'='*80}")
        fit = three_param_regression(results)
        if fit:
            for label, coeff in zip(fit['labels'], fit['coeffs']):
                print(f"  {label:10s}: {coeff:+.4f}")
            print(f"  chi2/dof = {fit['chi2']:.2f}/{fit['ndof']}")
        else:
            print("  Not enough data for regression")

    if args.pysr_test or run_all:
        print(f"\n{'='*80}")
        print(f"  PySR FORMULA TEST")
        print(f"  F1: S2/A = 5.68*beta - 4.05*n_roots - dim_adj + 3.5/L^2")
        print(f"  F2: S2/A = beta*C2/dim_adj - rank + 2.0/L^2  (screening)")
        print(f"{'='*80}")
        rows = pysr_formula_test(results)
        if rows:
            print(f"  {'Group':>6} {'L':>3} {'beta':>6} {'meas':>8} "
                  f"{'F1':>8} {'r1':>8} {'F2':>8} {'r2':>8}")
            for rr in rows:
                print(f"  {rr['group']:>6} {rr['L']:3d} {rr['beta']:6.2f} "
                      f"{rr['measured']:8.2f} {rr['pred_pysr']:8.2f} "
                      f"{rr['resid_pysr']:+8.2f} {rr['pred_screen']:8.2f} "
                      f"{rr['resid_screen']:+8.2f}")
            rms1 = np.sqrt(np.mean([rr['resid_pysr']**2 for rr in rows]))
            rms2 = np.sqrt(np.mean([rr['resid_screen']**2 for rr in rows]))
            print(f"  RMS residual (F1 PySR):     {rms1:.4f}")
            print(f"  RMS residual (F2 screening): {rms2:.4f}")

    if args.cv or run_all:
        print(f"\n{'='*80}")
        print(f"  LEAVE-ONE-GROUP-OUT CROSS-VALIDATION")
        print(f"{'='*80}")
        cv = leave_one_group_out_cv(results)
        if cv:
            for rr in cv:
                print(f"  held_out={rr['held_out']:>6} L={rr['ls']:3d}: "
                      f"meas={rr['measured']:.4f} pred={rr['predicted']:.4f} "
                      f"resid={rr['residual']:+.4f}")
            rms = np.sqrt(np.mean([rr['residual']**2 for rr in cv]))
            print(f"  RMS residual: {rms:.4f}")
        else:
            print("  Not enough data for cross-validation")

    if args.latex or run_all:
        print_latex_table(results)

    # Save structured JSON
    output = build_structured_json(results)
    with open(args.output_json, 'w') as f:
        json.dump(output, f, indent=2)
    print(f"\nSaved structured JSON to {args.output_json}")


if __name__ == '__main__':
    main()
