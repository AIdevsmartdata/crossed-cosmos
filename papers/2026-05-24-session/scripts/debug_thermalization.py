#!/usr/bin/env python3
"""Debug : ⟨P⟩ from cold vs random start, multiple sweep counts."""
import os
os.environ.setdefault('XLA_PYTHON_CLIENT_PREALLOCATE', 'false')
os.environ.setdefault('JAX_ENABLE_X64', 'True')

import sys
sys.path.insert(0, '/tmp')

with open('/tmp/jax_su2_EE_MODULAR_2026-05-25.py') as f:
    src = f.read()
src = src.split('if __name__')[0]
g = {}
exec(src, g)

import jax
import jax.numpy as jnp
import numpy as np
from jax import random

random_su2_haar = g['random_su2_haar']
metropolis_sweep_standard = g['metropolis_sweep_standard']
wilson_action = g['wilson_action']


def plaquette_mean(U):
    return 1.0 - float(wilson_action(U, 1.0)) / (6 * U.shape[0]**4)


def main():
    L = 8
    beta = 2.3

    print(f"=== Debug thermalization at L={L}, β={beta} ===\n", flush=True)
    print(f"Expected ⟨P⟩ at β=2.3 ≈ 0.62 (well thermalized)", flush=True)
    print(f"           ⟨P⟩ at β=∞ → 1 (cold)", flush=True)
    print(f"           ⟨P⟩ at β=0 (Haar) ≈ 0\n", flush=True)

    key = random.PRNGKey(42)

    # COLD start
    print("-- COLD start (U = I) --", flush=True)
    U_cold = jnp.zeros((L,)*4 + (4, 2, 2), dtype=jnp.complex128)
    # Set identity at each link
    I_mat = jnp.eye(2, dtype=jnp.complex128)
    U_cold = U_cold + I_mat
    print(f"  initial ⟨P⟩ = {plaquette_mean(U_cold):.4f}  (should be 1.0)", flush=True)
    for n in [10, 50, 100, 300, 500, 1000]:
        U = U_cold
        k = key
        for _ in range(n):
            k, sk = random.split(k)
            U = metropolis_sweep_standard(U, beta, sk, L, eps=0.3)
        p = plaquette_mean(U)
        print(f"  After {n:>4} sweeps : ⟨P⟩ = {p:.4f}", flush=True)

    print()
    # HOT start (random Haar)
    print("-- HOT start (Haar random) --", flush=True)
    key, sk = random.split(key)
    U_hot_init = random_su2_haar(sk, (L,)*4 + (4,))
    print(f"  initial ⟨P⟩ = {plaquette_mean(U_hot_init):.4f}  (should be ~0)", flush=True)
    for n in [10, 50, 100, 300, 500, 1000]:
        U = U_hot_init
        k = key
        for _ in range(n):
            k, sk = random.split(k)
            U = metropolis_sweep_standard(U, beta, sk, L, eps=0.3)
        p = plaquette_mean(U)
        print(f"  After {n:>4} sweeps : ⟨P⟩ = {p:.4f}", flush=True)

    print()
    # Try smaller eps (higher acceptance)
    print("-- COLD start, eps=0.1 (smaller proposal, higher acceptance) --", flush=True)
    for n in [100, 300, 500]:
        U = U_cold
        k = key
        for _ in range(n):
            k, sk = random.split(k)
            U = metropolis_sweep_standard(U, beta, sk, L, eps=0.1)
        p = plaquette_mean(U)
        print(f"  After {n:>4} sweeps eps=0.1 : ⟨P⟩ = {p:.4f}", flush=True)


if __name__ == "__main__":
    main()
