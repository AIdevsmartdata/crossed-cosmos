#!/usr/bin/env python3
"""MH β-scan : extract κ leading via pente K_diff(β) en 1/a²(β).

À L fixé, sub-leading (C·log(L), const) gelés. Variation avec β isole leading.

Run β ∈ {2.3, 2.4, 2.5, 2.6} à L ∈ {8, 12} fixe.
Fit : K_diff(β) = κ · L³ · ζ_w(3) / a²(β) + C_indep_β
1-loop a²(β) ratio (β=2.6 vs 2.3) = 5.7 → discrimine κ=0.5 vs κ=0.05 (5× vs 0.5×).

Reuse MH measurement code (v1, sans Wilson flow pour rapidité test).
"""
import os
os.environ.setdefault('XLA_PYTHON_CLIENT_PREALLOCATE', 'false')
os.environ.setdefault('JAX_ENABLE_X64', 'True')

import sys
sys.path.insert(0, '/tmp')

# Reuse MH v1 module
with open('/tmp/jax_su2_EE_MODULAR_2026-05-25.py') as f:
    src = f.read()
src = src.split('if __name__')[0]
g = {}
exec(src, g)

import time
import json
import numpy as np
import jax
from jax import random

START = time.time()
print(f"START : {time.ctime()}", flush=True)
print("=" * 78, flush=True)
print(f"MH β-scan SU(2) — extract leading κ via slope in 1/a²(β)", flush=True)
print("=" * 78, flush=True)


def a2_1loop(beta):
    """1-loop a²(β) for SU(2) Wilson."""
    g2 = 4.0 / beta
    return g2 * np.exp(-12 * np.pi**2 * beta / 22.0)


def zeta_w(w):
    return sum(1.0 / (k + 0.5)**3 for k in range(w))


def main():
    BETAS = [2.3, 2.4, 2.5, 2.6]
    L_VALUES = [8, 12]

    # Higher sample count, no Wilson flow (separate route)
    configs = {
        8:  {'w': 2, 'n_thermalize': 200, 'n_decorr': 5,  'n_samples': 200},
        12: {'w': 3, 'n_thermalize': 300, 'n_decorr': 8,  'n_samples': 80},
    }

    all_results = {}
    for L in L_VALUES:
        all_results[L] = {}
        for beta in BETAS:
            cfg = configs[L]
            print(f"\n{'='*78}\nL={L}, β={beta}, w={cfg['w']}\n{'='*78}", flush=True)
            key = random.PRNGKey(2060 + 73 * L + int(beta*100))
            try:
                r = g['measure_modular_observable'](L, beta, cfg['w'],
                                                       cfg['n_thermalize'], cfg['n_decorr'],
                                                       cfg['n_samples'], key)
                all_results[L][beta] = r
                print(f"\nL={L} β={beta} : K_diff = {r['K_diff_mean']:.3e} ± {r['K_diff_sem']:.2e}",
                      flush=True)
            except Exception as e:
                print(f"L={L} β={beta} FAILED: {e}", flush=True)
                import traceback
                traceback.print_exc()
            with open('/tmp/jax_su2_EE_MH_BETASCAN.json', 'w') as f:
                json.dump({
                    'method': 'MH β-scan: K_diff(β) at fixed L → κ via slope in 1/a²',
                    'betas': BETAS, 'L_values': L_VALUES, 'configs': configs,
                    'results': {str(L): {str(b): all_results[L][b] for b in all_results[L]}
                                for L in all_results},
                    'partial': True,
                    'total_elapsed_s': time.time() - START,
                }, f, indent=2)

    # Analyse
    print(f"\n{'='*78}\nK_diff(L, β) — pente en 1/a²(β) extrait κ\n{'='*78}", flush=True)

    print(f"\n{'L':>4} {'β':>5} {'K_diff':>16} {'1/a²(β) norm':>14}")
    print("-" * 50)
    for L in L_VALUES:
        for beta in BETAS:
            if beta in all_results[L]:
                r = all_results[L][beta]
                inv_a2 = 1.0 / a2_1loop(beta)
                print(f"{L:>4} {beta:>5.1f} {r['K_diff_mean']:>10.3e}±{r['K_diff_sem']:>3.0e} {inv_a2:>14.4e}")

    # Fit κ at each L : K_diff(β) = (κ · L³ · ζ_w(3)) · (1/a²(β)) + const
    print(f"\nFit K_diff(β) = A·(1/a²(β)) + B at each L :", flush=True)
    print(f"  A = κ · L³ · ζ_w(3) → κ = A / (L³ · ζ_w(3))")
    print(f"  Goal : κ should match across L for universality")
    print()

    for L in L_VALUES:
        if not all_results[L]:
            continue
        betas_arr = np.array([b for b in BETAS if b in all_results[L]])
        K_arr = np.array([all_results[L][b]['K_diff_mean'] for b in betas_arr])
        err_arr = np.array([all_results[L][b]['K_diff_sem'] for b in betas_arr])
        inv_a2_arr = np.array([1.0 / a2_1loop(b) for b in betas_arr])

        # Normalize 1/a² to first β
        x = inv_a2_arr / inv_a2_arr[0]

        # Linear fit K = A·x + B
        w_lst = configs[L]['w']
        z_w = zeta_w(w_lst)
        norm_factor = L**3 * z_w * inv_a2_arr[0]

        # Weighted linear regression
        weights = 1.0 / np.maximum(err_arr**2, 1e-20)
        S_w = np.sum(weights)
        Sx_w = np.sum(weights * x)
        Sy_w = np.sum(weights * K_arr)
        Sxx_w = np.sum(weights * x**2)
        Sxy_w = np.sum(weights * x * K_arr)
        delta = S_w * Sxx_w - Sx_w**2
        if delta > 0:
            A_fit = (S_w * Sxy_w - Sx_w * Sy_w) / delta
            B_fit = (Sxx_w * Sy_w - Sx_w * Sxy_w) / delta
            A_err = np.sqrt(S_w / delta)

            kappa = A_fit / norm_factor
            kappa_err = A_err / norm_factor

            print(f"L={L}: A = {A_fit:.3e} ± {A_err:.2e}, B = {B_fit:.3e}")
            print(f"      κ = A/(L³·ζ_w(3)·1/a²(β=2.3)) = {kappa:.4e} ± {kappa_err:.2e}")
            print(f"      vs 1/2 (BH) : ratio = {kappa/0.5:.3f}, Z = {(kappa-0.5)/max(kappa_err,1e-10):+.2f}σ")

    output = {
        'method': 'MH β-scan: K_diff(β) at fixed L → κ via slope in 1/a²',
        'betas': BETAS, 'L_values': L_VALUES, 'configs': configs,
        'results': {str(L): {str(b): all_results[L][b] for b in all_results[L]} for L in all_results},
        'total_elapsed_s': time.time() - START,
    }
    with open('/tmp/jax_su2_EE_MH_BETASCAN.json', 'w') as f:
        json.dump(output, f, indent=2)

    print(f"\nTotal elapsed : {time.time() - START:.1f}s ({(time.time() - START)/60:.1f}min)", flush=True)
    print(f"END : {time.ctime()}", flush=True)


if __name__ == "__main__":
    main()
