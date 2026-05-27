#!/usr/bin/env python3
"""Test fix : Re Tr(U · K) au lieu de Re Tr(U · K†) dans Metropolis."""
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
from jax import random, jit
from functools import partial

random_su2_haar = g['random_su2_haar']
random_su2_near_identity = g['random_su2_near_identity']
compute_staple_sum = g['compute_staple_sum']
wilson_action = g['wilson_action']


@partial(jit, static_argnames=('L',))
def metropolis_sweep_FIXED(U, beta, key, L, eps=0.3):
    """Fixed Metropolis using Re Tr(U · K) instead of Re Tr(U · K†)."""
    for mu in range(4):
        K_mu = compute_staple_sum(U, mu, L)
        key, k_prop, k_acc = random.split(key, 3)
        X = random_su2_near_identity(k_prop, U[..., mu, :, :].shape[:-2], eps=eps)
        U_proposed_mu = jnp.einsum('...ij,...jk->...ik', X, U[..., mu, :, :])
        # FIX: use K_mu directly (not K_dag) for Tr(U · K) = Tr(plaquette)
        new_term = jnp.real(jnp.trace(jnp.einsum('...ij,...jk->...ik',
                                                  U_proposed_mu, K_mu),
                                       axis1=-2, axis2=-1))
        old_term = jnp.real(jnp.trace(jnp.einsum('...ij,...jk->...ik',
                                                  U[..., mu, :, :], K_mu),
                                       axis1=-2, axis2=-1))
        dS = -beta * 0.5 * (new_term - old_term)
        rand_u = random.uniform(k_acc, dS.shape)
        accept = rand_u < jnp.exp(jnp.minimum(0.0, -dS))
        U_mu_new = jnp.where(accept[..., None, None], U_proposed_mu, U[..., mu, :, :])
        U = U.at[..., mu, :, :].set(U_mu_new)
    return U


def plaquette_mean(U):
    return 1.0 - float(wilson_action(U, 1.0)) / (6 * U.shape[0]**4)


def main():
    L = 8

    print("=== FIXED Metropolis test ===\n", flush=True)
    print("Expected ⟨P⟩ values from literature (Creutz, Lucini-Teper):")
    print("  β=2.0  → ⟨P⟩ ≈ 0.55")
    print("  β=2.3  → ⟨P⟩ ≈ 0.62")
    print("  β=2.5  → ⟨P⟩ ≈ 0.66")
    print("  β=2.7  → ⟨P⟩ ≈ 0.70\n")

    for beta in [2.0, 2.3, 2.5, 2.7]:
        key = random.PRNGKey(2024 + int(beta * 100))
        # Cold start
        I_mat = jnp.eye(2, dtype=jnp.complex128)
        U = jnp.zeros((L,)*4 + (4, 2, 2), dtype=jnp.complex128) + I_mat

        for s in range(500):
            key, sk = random.split(key)
            U = metropolis_sweep_FIXED(U, beta, sk, L, eps=0.3)

        p = plaquette_mean(U)
        print(f"β={beta:.1f}: ⟨P⟩ = {p:.4f}  ({'✅' if 0.4 < p < 0.85 else '❌'})", flush=True)


if __name__ == "__main__":
    main()
