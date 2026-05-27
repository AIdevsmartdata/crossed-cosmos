#!/usr/bin/env python3
"""Bigger lattice production : L = 14, 16, 20 with deep sampling."""
import os
os.environ.setdefault('XLA_PYTHON_CLIENT_PREALLOCATE', 'false')
os.environ.setdefault('JAX_ENABLE_X64', 'True')

import sys
sys.path.insert(0, '/tmp')

with open('/tmp/jax_su2_EE_BP2008b_v2.py') as f:
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
print(f"JAX SU(2) EE — BIGGER LATTICE L=14,16,20", flush=True)
print("=" * 78, flush=True)

BETA = 2.4
ALPHA_GRID = list(np.linspace(0.0, 1.0, 11))

runs_config = {
    14: {'T_half': 14, 'n_thermalize': 1500, 'n_decorr': 30, 'n_samples': 40},
    16: {'T_half': 16, 'n_thermalize': 2000, 'n_decorr': 40, 'n_samples': 25},
    20: {'T_half': 20, 'n_thermalize': 3000, 'n_decorr': 60, 'n_samples': 15},
}

all_results = {}
for L in [14, 16, 20]:
    cfg = runs_config[L]
    print(f"\n{'='*78}\nLATTICE L = {L}\n{'='*78}", flush=True)
    key = random.PRNGKey(2033 + 41 * L)
    try:
        r = g['alpha_integrate'](L, cfg['T_half'], BETA, ALPHA_GRID,
                                  cfg['n_thermalize'], cfg['n_decorr'], cfg['n_samples'],
                                  key)
        all_results[L] = r
        print(f"L={L}: S_2 = {r['S_2']:.4e} +/- {r['S_2_err']:.4e}", flush=True)
        print(f"      c = {r['c_per_2D']:.6e}", flush=True)
    except Exception as e:
        print(f"L={L} FAILED : {e}", flush=True)
        import traceback
        traceback.print_exc()
    with open('/tmp/jax_su2_EE_BP2008b_BIGL.json', 'w') as f:
        json.dump({
            'method': 'BP2008b BIGL extension : L=14,16,20',
            'beta': BETA, 'alpha_grid': ALPHA_GRID,
            'runs_config': runs_config,
            'results': {str(L): all_results[L] for L in all_results},
            'partial': True,
            'total_elapsed_s': time.time() - START,
        }, f, indent=2)

print(f"\n{'='*78}\nFINAL SCALING — BP2008b BIGL\n{'='*78}", flush=True)
for L in sorted(all_results.keys()):
    r = all_results[L]
    print(f"L={L:>4} |dA|={r['boundary_2D']:>6} S_2={r['S_2']:.4e}+/-{r['S_2_err']:.0e} c={r['c_per_2D']:.6e}", flush=True)

print(f"\nTotal elapsed : {time.time() - START:.1f}s ({(time.time() - START)/60:.1f}min)", flush=True)
print(f"END : {time.ctime()}", flush=True)
print(f"DONE.", flush=True)
