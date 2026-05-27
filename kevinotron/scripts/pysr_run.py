#!/usr/bin/env python3
"""
KEVINOTRON PySR SYMBOLIC REGRESSION RUNNER
============================================
Run PySR (symbolic regression via genetic programming) on combined
EE data from kevinotron (new format) + legacy (g2_lattice_rs).

Reads analysis_results.json (from analyze.py) or takes data inline.
Searches for S2/A = f(beta, n_roots, dim_adj, L, rank, dim_fund).

Usage:
    python3 pysr_run.py --input analysis_results.json
    python3 pysr_run.py --input analysis_results.json --complexity 30 --niterations 200

Saves Pareto-optimal formulas to pysr_output/.

Author: Kevin Remondiere (ORCID 0009-0008-2443-7166)
"""

import numpy as np
import json
import os
import sys
import argparse

# ============================================================
# GROUP PROPERTIES (same as analyze.py)
# ============================================================

GROUP_PROPS = {
    'SU(2)': {'dim_fund': 2, 'dim_adj': 3,  'rank': 1, 'n_roots': 2,  'is_complex': 1},
    'SU(3)': {'dim_fund': 3, 'dim_adj': 8,  'rank': 2, 'n_roots': 6,  'is_complex': 1},
    'SU(4)': {'dim_fund': 4, 'dim_adj': 15, 'rank': 3, 'n_roots': 12, 'is_complex': 1},
    'G2':    {'dim_fund': 7, 'dim_adj': 14, 'rank': 2, 'n_roots': 12, 'is_complex': 0},
    'Sp(4)': {'dim_fund': 4, 'dim_adj': 10, 'rank': 2, 'n_roots': 8,  'is_complex': 1},
    'SO(7)': {'dim_fund': 7, 'dim_adj': 21, 'rank': 3, 'n_roots': 18, 'is_complex': 0},
}


def load_data(input_path):
    """Load data from analysis_results.json into feature matrix."""
    with open(input_path) as f:
        data = json.load(f)

    measurements = data.get('measurements', [])
    if not measurements:
        print("ERROR: no measurements in input file")
        sys.exit(1)

    rows = []
    for m in measurements:
        group = m.get('group')
        if group not in GROUP_PROPS:
            print(f"  Skipping unknown group: {group}")
            continue
        props = GROUP_PROPS[group]
        rows.append({
            'beta': m['beta'],
            'L': m['ls'],
            'dim_fund': props['dim_fund'],
            'dim_adj': props['dim_adj'],
            'rank': props['rank'],
            'n_roots': props['n_roots'],
            'is_complex': props['is_complex'],
            's2_a': m['s2_a'],
            's2_a_err': m.get('s2_a_err', 0.01),
        })

    print(f"Loaded {len(rows)} data points from {len(set(m.get('group') for m in measurements))} groups")
    return rows


def run_pysr(rows, args):
    """Run PySR symbolic regression."""
    try:
        from pysr import PySRRegressor
    except ImportError:
        print("ERROR: PySR not installed. Install with: pip install pysr")
        print("Falling back to manual formula scan...")
        return run_manual_scan(rows, args)

    # Build feature matrix
    feature_names = ['beta', 'n_roots', 'dim_adj', 'L', 'rank', 'dim_fund', 'is_complex']
    X = np.array([[r[f] for f in feature_names] for r in rows])
    y = np.array([r['s2_a'] for r in rows])
    weights = np.array([1.0 / max(r['s2_a_err'], 1e-10)**2 for r in rows])
    weights /= weights.max()  # Normalize

    print(f"\nFeature matrix: {X.shape}")
    print(f"Target: {y.shape}")
    print(f"Features: {feature_names}")

    model = PySRRegressor(
        niterations=args.niterations,
        binary_operators=["+", "-", "*", "/"],
        unary_operators=["square", "sqrt", "log", "exp"],
        maxsize=args.complexity,
        populations=args.populations,
        population_size=args.population_size,
        ncycles_per_iteration=550,
        weight_optimize=0.001,
        parsimony=0.0032,
        adaptive_parsimony_scaling=20.0,
        turbo=True,
        precision=64,
        random_state=42,
        deterministic=True,
        procs=args.procs,
        warm_start=False,
        progress=True,
        temp_equation_file=True,
    )

    print(f"\nRunning PySR (niterations={args.niterations}, maxsize={args.complexity})...")
    model.fit(X, y, weights=weights, variable_names=feature_names)

    # Save results
    os.makedirs(args.output_dir, exist_ok=True)

    # Save Pareto front
    pareto_path = os.path.join(args.output_dir, 'pareto_front.txt')
    with open(pareto_path, 'w') as f:
        f.write("# PySR Pareto-optimal formulas for S2/A\n")
        f.write("# Features: beta, n_roots, dim_adj, L, rank, dim_fund, is_complex\n")
        f.write(f"# {len(rows)} data points, {len(set(r.get('group', '') for r in rows))} groups\n\n")
        for i, eq in enumerate(model.equations_):
            f.write(f"# Complexity {eq['complexity']}, Loss {eq['loss']:.6f}\n")
            f.write(f"  {eq['equation']}\n\n")

    # Save model
    model_path = os.path.join(args.output_dir, 'pysr_model.pkl')
    try:
        import pickle
        with open(model_path, 'wb') as f:
            pickle.dump(model, f)
    except Exception as e:
        print(f"  Warning: could not save model: {e}")

    # Save predictions
    y_pred = model.predict(X)
    pred_path = os.path.join(args.output_dir, 'predictions.json')
    pred_data = []
    for i, r in enumerate(rows):
        pred_data.append({
            'group': r.get('group', 'unknown'),
            'L': r['L'],
            'beta': r['beta'],
            'measured': float(y[i]),
            'predicted': float(y_pred[i]),
            'residual': float(y[i] - y_pred[i]),
        })
    with open(pred_path, 'w') as f:
        json.dump(pred_data, f, indent=2)

    print(f"\nBest formula: {model.get_best()}")
    print(f"Saved to {args.output_dir}/")

    return model


def run_manual_scan(rows, args):
    """Manual scan of candidate formulas when PySR is not available."""
    from scipy.special import zeta as riemann_zeta
    zeta3 = riemann_zeta(3)
    kappa_inf = zeta3 / np.sqrt(np.pi)

    formulas = {
        'PySR_best: 5.68*b - 4.05*nr - da + 3.5/L^2':
            lambda r: 5.68*r['beta'] - 4.05*r['n_roots'] - r['dim_adj'] + 3.5/r['L']**2,
        'kappa_EE: (1-1/da)*kappa_inf + c/L^2':
            lambda r: (1 - 1/r['dim_adj']) * kappa_inf + 0.5/r['L']**2,
        'linear: a*b + c*da + d/L^2':
            None,  # Fit below
    }

    os.makedirs(args.output_dir, exist_ok=True)

    y = np.array([r['s2_a'] for r in rows])

    results_path = os.path.join(args.output_dir, 'manual_scan.txt')
    with open(results_path, 'w') as f:
        f.write("# Manual formula scan (PySR not available)\n\n")

        for name, fn in formulas.items():
            if fn is None:
                continue
            try:
                y_pred = np.array([fn(r) for r in rows])
                rms = np.sqrt(np.mean((y - y_pred)**2))
                f.write(f"Formula: {name}\n")
                f.write(f"  RMS = {rms:.6f}\n\n")
                print(f"  {name}: RMS = {rms:.6f}")
            except Exception as e:
                print(f"  {name}: ERROR {e}")

    print(f"Saved to {results_path}")


def main():
    parser = argparse.ArgumentParser(description='Kevinotron PySR Runner')
    parser.add_argument('--input', required=True, help='Path to analysis_results.json')
    parser.add_argument('--output-dir', default='pysr_output', help='Output directory')
    parser.add_argument('--niterations', type=int, default=100, help='PySR iterations')
    parser.add_argument('--complexity', type=int, default=25, help='Max formula complexity')
    parser.add_argument('--populations', type=int, default=30, help='Number of populations')
    parser.add_argument('--population-size', type=int, default=33, help='Population size')
    parser.add_argument('--procs', type=int, default=4, help='Number of processes')
    args = parser.parse_args()

    if not os.path.exists(args.input):
        print(f"ERROR: input file not found: {args.input}")
        sys.exit(1)

    rows = load_data(args.input)
    if len(rows) < 3:
        print("ERROR: need at least 3 data points")
        sys.exit(1)

    run_pysr(rows, args)


if __name__ == '__main__':
    main()
