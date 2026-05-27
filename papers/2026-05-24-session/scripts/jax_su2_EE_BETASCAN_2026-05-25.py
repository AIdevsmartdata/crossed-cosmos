#!/usr/bin/env python3
"""β-scan FAST V3 : test universality of C-function.

Goal : measure c_3D(L, β) for β ∈ {2.3, 2.4, 2.5, 2.6} and L ∈ {8, 10, 12}.

If C is universal : c_3D(β) ≈ const ≈ 0.124 across β.
This is a STRONG test of universality. β-independence = robust result.

Compute budget : ~2.5-3h on RTX 5060 Ti with FAST V3.

Bonus : extracting C(β) helps build the asymptotic form for separating
leading κ/a²(β) from sub-leading C (Future work for κ²=1/4 test).
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

import time
import json
import numpy as np
import jax
from jax import random

START = time.time()
print(f"START : {time.ctime()}", flush=True)
print("=" * 78, flush=True)
print(f"JAX SU(2) β-scan : C-function universality test", flush=True)
print("β ∈ {{2.3, 2.4, 2.5, 2.6}} × L ∈ {{8, 10, 12}}", flush=True)
print("=" * 78, flush=True)

ALPHA_GRID = list(np.linspace(0.0, 1.0, 11))

BETAS = [2.3, 2.4, 2.5, 2.6]
L_VALUES = [8, 10, 12]

runs_config = {
    8:  {'T_half': 8,  'n_thermalize': 400, 'n_decorr': 15, 'n_samples': 60},
    10: {'T_half': 10, 'n_thermalize': 500, 'n_decorr': 20, 'n_samples': 40},
    12: {'T_half': 12, 'n_thermalize': 700, 'n_decorr': 25, 'n_samples': 30},
}

all_results = {}
for beta in BETAS:
    all_results[beta] = {}
    for L in L_VALUES:
        cfg = runs_config[L]
        print(f"\n{'='*78}\nβ={beta}, L={L}\n{'='*78}", flush=True)
        key = random.PRNGKey(2035 + int(beta * 100) * L)
        try:
            r = g['alpha_integrate'](L, L, L, cfg['T_half'], beta, ALPHA_GRID,
                                      cfg['n_thermalize'], cfg['n_decorr'], cfg['n_samples'],
                                      key)
            all_results[beta][L] = r
            A_3D = 2 * L * L * cfg['T_half']
            c_3D = r['S_2'] / A_3D
            print(f"β={beta}, L={L}: c_3D = {c_3D:.6f}", flush=True)
        except Exception as e:
            print(f"β={beta} L={L} FAILED: {e}", flush=True)
            import traceback
            traceback.print_exc()
        # Checkpoint
        with open('/tmp/jax_su2_EE_BETASCAN.json', 'w') as f:
            json.dump({
                'method': 'BP2008b FAST V3 β-scan : C-function universality',
                'betas': BETAS, 'L_values': L_VALUES,
                'alpha_grid': ALPHA_GRID,
                'runs_config': runs_config,
                'results': {str(b): {str(L): all_results[b][L] for L in all_results[b]} for b in all_results},
                'partial': True,
                'total_elapsed_s': time.time() - START,
            }, f, indent=2)

print(f"\n{'='*78}\nFINAL β-scan TABLE — C-function universality test\n{'='*78}", flush=True)
print(f"{'L':>4} {'β=2.3':>10} {'β=2.4':>10} {'β=2.5':>10} {'β=2.6':>10}", flush=True)
print("-" * 50, flush=True)
for L in L_VALUES:
    row = f"{L:>4}"
    for beta in BETAS:
        if beta in all_results and L in all_results[beta]:
            r = all_results[beta][L]
            A_3D = 2 * L * L * runs_config[L]['T_half']
            c_3D = r['S_2'] / A_3D
            row += f" {c_3D:>10.6f}"
        else:
            row += f" {'N/A':>10}"
    print(row, flush=True)

C_PRED = np.log(3) / (2 * np.pi * np.sqrt(2))
print(f"\nPrediction log(3)/(2π√2) = {C_PRED:.6f}", flush=True)
print(f"Universality test : c_3D should be ~constant across β\n", flush=True)

print(f"Total elapsed : {time.time() - START:.1f}s ({(time.time() - START)/60:.1f}min)", flush=True)
print(f"END : {time.ctime()}", flush=True)
print(f"DONE.", flush=True)
