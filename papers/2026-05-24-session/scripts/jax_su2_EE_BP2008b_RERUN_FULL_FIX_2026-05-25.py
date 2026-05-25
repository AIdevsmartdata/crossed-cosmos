#!/usr/bin/env python3
"""BP2008b RERUN FULL FIX — α-integration β-scan + ⟨P⟩ sanity check pre-run.

Production rerun avec deux bugs corrigés :
1. K_dag → K_eff dans Metropolis trace (commit 33ac134)
2. compute_staples_K_T_K_2T : staple order corrigé (commit 1629f1d)

Sanity check ⟨P⟩ avant chaque (L, β) — abort si ⟨P⟩ hors [0.4, 0.85].

L ∈ {4, 6, 8, 10}, β ∈ {2.3, 2.4, 2.5, 2.6}.
Sortie : c(L, β) per (L, β) + comparison to literature.

Author : Kévin Rémondière (ORCID 0009-0008-2443-7166).
"""
import os
os.environ.setdefault('XLA_PYTHON_CLIENT_PREALLOCATE', 'false')
os.environ.setdefault('JAX_ENABLE_X64', 'True')

import sys
sys.path.insert(0, '/tmp')

with open('/tmp/jax_su2_EE_BP2008b_FAST_2026-05-25.py') as f:
    src = f.read()
src = src.split('if __name__')[0]
g = {}
exec(src, g)

with open('/tmp/jax_su2_EE_MODULAR_2026-05-25.py') as f:
    src2 = f.read()
src2 = src2.split('if __name__')[0]
g2 = {}
exec(src2, g2)

import time
import json
import numpy as np
import jax
import jax.numpy as jnp
from jax import random

# Pull functions from BP2008b
alpha_integrate = g['alpha_integrate']
random_su2_haar = g['random_su2_haar']
metropolis_sweep_4dir = g['metropolis_sweep_4dir']
adaptive_eps = g['adaptive_eps']
make_A_junction_link_mask = g['make_A_junction_link_mask']
wilson_action = g2['wilson_action']


START = time.time()
print(f"START : {time.ctime()}", flush=True)
print("=" * 78, flush=True)
print(f"BP2008b RERUN FULL FIX (2 bugs corrigés) — β-scan", flush=True)
print("=" * 78, flush=True)


def sanity_check_plaquette(L, beta, n_thermalize=200, eps=0.3):
    """Mesure ⟨P⟩ via FAST V3 metropolis pre-production."""
    T_half = L
    twoT = 2 * T_half
    A_spatial_mask = jnp.zeros((L, L, L), dtype=bool)  # alpha=0 always at junction
    A_link_mask = make_A_junction_link_mask(L, L, L, T_half, A_spatial_mask)
    alpha = 0.0  # no deformation for sanity check

    key = random.PRNGKey(2026 + 47 * L + int(beta * 100))
    U = random_su2_haar(key, (L, L, L, twoT, 4))
    k = key
    for _ in range(n_thermalize):
        k, sk = random.split(k)
        U = metropolis_sweep_4dir(U, beta, alpha, sk, L, L, L, T_half, A_link_mask, eps)
    p = 1.0 - float(wilson_action(U, 1.0)) / (6 * L**3 * twoT)
    return p


def main():
    # PRIORITÉ Kevin : β=2.4 fixé d'abord, puis 2.5/2.3/2.6 si temps. L=4..16 progressif.
    BETAS = [2.4, 2.5, 2.3, 2.6]
    L_VALUES = [4, 6, 8, 10, 12, 16]
    ALPHA_GRID = list(np.linspace(0.0, 1.0, 11))

    runs_config = {
        4:  {'T_half': 4,  'n_thermalize': 300, 'n_decorr': 8,  'n_samples': 100},
        6:  {'T_half': 6,  'n_thermalize': 400, 'n_decorr': 12, 'n_samples': 80},
        8:  {'T_half': 8,  'n_thermalize': 500, 'n_decorr': 18, 'n_samples': 60},
        10: {'T_half': 10, 'n_thermalize': 600, 'n_decorr': 22, 'n_samples': 40},
        12: {'T_half': 12, 'n_thermalize': 700, 'n_decorr': 25, 'n_samples': 30},
        16: {'T_half': 16, 'n_thermalize': 1000, 'n_decorr': 35, 'n_samples': 15},
    }

    all_results = {}
    for beta in BETAS:
        all_results[beta] = {}
        for L in L_VALUES:
            print(f"\n{'='*78}", flush=True)
            print(f"L = {L}, β = {beta}", flush=True)
            print(f"{'='*78}", flush=True)

            # Sanity check first
            print(f"\n--- Sanity check ⟨P⟩ ---", flush=True)
            t_check = time.time()
            p_check = sanity_check_plaquette(L, beta, n_thermalize=200, eps=0.3)
            print(f"⟨P⟩(L={L}, β={beta}, alpha=0) = {p_check:.4f} (t={time.time()-t_check:.1f}s)", flush=True)
            if p_check < 0.4 or p_check > 0.85:
                print(f"  ⚠️ HORS RANGE — SKIPPING (P={p_check:.4f})", flush=True)
                continue

            # Production with FAST V3 alpha integrate
            cfg = runs_config[L]
            key = random.PRNGKey(2030 + 51 * L + int(beta * 100))
            try:
                r = alpha_integrate(L, L, L, cfg['T_half'], beta, ALPHA_GRID,
                                     cfg['n_thermalize'], cfg['n_decorr'], cfg['n_samples'],
                                     key)
                all_results[beta][L] = r
                print(f"\n✓ L={L} β={beta}: c = {r['c_per_2D']:.4e} ± {r['c_err']:.2e}", flush=True)
            except Exception as e:
                print(f"FAILED L={L} β={beta}: {e}", flush=True)
                import traceback
                traceback.print_exc()

            with open('/tmp/jax_su2_EE_BP2008b_RERUN_FULL_FIX.json', 'w') as f:
                json.dump({
                    'method': 'BP2008b RERUN FULL FIX β-scan',
                    'betas': BETAS, 'L_values': L_VALUES, 'runs_config': runs_config,
                    'results': {str(b): {str(L): all_results[b][L] for L in all_results[b]}
                                for b in all_results},
                    'partial': True,
                    'total_elapsed_s': time.time() - START,
                }, f, indent=2)

    # Summary
    print(f"\n{'='*78}\nc(L, β) summary post FULL FIX\n{'='*78}", flush=True)
    print(f"\n{'L':>4} | " + " ".join(f"β={b:.1f}" for b in BETAS), flush=True)
    print("-" * 60)
    for L in L_VALUES:
        row = f"{L:>4} | "
        for beta in BETAS:
            if beta in all_results and L in all_results[beta]:
                c = all_results[beta][L]['c_per_2D']
                row += f"{c:.4f}  "
            else:
                row += "  N/A   "
        print(row, flush=True)

    print(f"\nComparison pre-fix vs post-fix needed for c(L=6, β=2.4) ≈ 0.122 claim\n", flush=True)
    print(f"BH leading κ² = 1/4 = 0.25", flush=True)
    print(f"Rabenstein 2019 C(SU(2)) ≈ 0.054 (sub-leading)", flush=True)

    output = {
        'method': 'BP2008b RERUN FULL FIX β-scan',
        'betas': BETAS, 'L_values': L_VALUES, 'runs_config': runs_config,
        'results': {str(b): {str(L): all_results[b][L] for L in all_results[b]} for b in all_results},
        'total_elapsed_s': time.time() - START,
    }
    with open('/tmp/jax_su2_EE_BP2008b_RERUN_FULL_FIX.json', 'w') as f:
        json.dump(output, f, indent=2)

    print(f"\nTotal elapsed : {time.time() - START:.1f}s ({(time.time() - START)/60:.1f}min)", flush=True)
    print(f"END : {time.ctime()}", flush=True)


if __name__ == "__main__":
    main()
