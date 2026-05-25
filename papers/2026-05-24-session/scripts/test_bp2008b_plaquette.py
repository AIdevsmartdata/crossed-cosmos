#!/usr/bin/env python3
"""Test ⟨P⟩ via BP2008b FAST V3 metropolis_sweep_4dir — DEUX versions :
1. POST-FIX (utilise K_eff directement)
2. BUGGY restaurée (utilise K_dag = K_eff† dans trace)

Verdict : ⟨P⟩ ≈ +0.62 = FIX OK ; ⟨P⟩ ≈ -0.18 = BUG.
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

# Also load wilson_action from MODULAR
with open('/tmp/jax_su2_EE_MODULAR_2026-05-25.py') as f:
    src2 = f.read()
src2 = src2.split('if __name__')[0]
g2 = {}
exec(src2, g2)

import jax
import jax.numpy as jnp
import numpy as np
from jax import random, jit
from functools import partial

# Pull functions
random_su2_haar = g['random_su2_haar']
compute_staples_K_T_K_2T = g['compute_staples_K_T_K_2T']
random_su2_near_identity = g['random_su2_near_identity']
metropolis_sweep_4dir = g['metropolis_sweep_4dir']
wilson_action = g2['wilson_action']


def plaquette_mean(U):
    L = U.shape[0]
    return 1.0 - float(wilson_action(U, 1.0)) / (6 * L**4)


# Re-define a BUGGY version metropolis_sweep_perlink_local for comparison
@partial(jit, static_argnames=('mu', 'L_x', 'L_y', 'L_z', 'T_half'))
def metropolis_sweep_perlink_local_BUGGY(U, beta, alpha, key, mu, L_x, L_y, L_z, T_half, A_link_mask, eps=0.3):
    K_T, K_2T = compute_staples_K_T_K_2T(U, mu, L_x, L_y, L_z, T_half)
    K_eff = jnp.where(A_link_mask[..., mu, None, None], (1 - alpha) * K_T + alpha * K_2T, K_T)
    key1, key2 = random.split(key)
    X = random_su2_near_identity(key1, U[..., mu, :, :].shape[:-2], eps=eps)
    U_proposed = jnp.einsum('...ij,...jk->...ik', X, U[..., mu, :, :])
    # BUGGY: uses K_dag instead of K_eff
    K_dag = jnp.conjugate(jnp.swapaxes(K_eff, -1, -2))
    new_term = jnp.real(jnp.trace(jnp.einsum('...ij,...jk->...ik', U_proposed, K_dag), axis1=-2, axis2=-1))
    old_term = jnp.real(jnp.trace(jnp.einsum('...ij,...jk->...ik', U[..., mu, :, :], K_dag), axis1=-2, axis2=-1))
    dS = -beta * 0.5 * (new_term - old_term)
    rand_u = random.uniform(key2, dS.shape)
    accept = rand_u < jnp.exp(jnp.minimum(0.0, -dS))
    U_mu_new = jnp.where(accept[..., None, None], U_proposed, U[..., mu, :, :])
    return U.at[..., mu, :, :].set(U_mu_new)


@partial(jit, static_argnames=('L_x', 'L_y', 'L_z', 'T_half'))
def metropolis_sweep_4dir_BUGGY(U, beta, alpha, key, L_x, L_y, L_z, T_half, A_link_mask, eps=0.3):
    for mu in range(4):
        key, sk = random.split(key)
        U = metropolis_sweep_perlink_local_BUGGY(U, beta, alpha, sk, mu, L_x, L_y, L_z, T_half, A_link_mask, eps)
    return U


def main():
    L = 8
    beta = 2.4

    print(f"Test BP2008b FAST V3 thermalization at L={L}, β={beta}\n", flush=True)
    print("Expected ⟨P⟩ at β=2.4 ≈ 0.64 (Wilson SU(2) lit)", flush=True)
    print()

    # Build A_link_mask : alpha = 0 → no junction → standard Wilson everywhere
    # For pure-action test, A_link_mask all False so K_eff = K_T always
    A_link_mask = jnp.zeros((L, L, L, L, 4), dtype=bool)
    alpha = 0.0

    key = random.PRNGKey(2024)

    # COLD start
    I_mat = jnp.eye(2, dtype=jnp.complex128)
    U_cold = jnp.zeros((L,)*4 + (4, 2, 2), dtype=jnp.complex128) + I_mat
    print(f"Initial ⟨P⟩ cold = {plaquette_mean(U_cold):.4f}\n", flush=True)

    # FIXED version
    U = U_cold
    k = key
    for s in range(300):
        k, sk = random.split(k)
        U = metropolis_sweep_4dir(U, beta, alpha, sk, L, L, L, L//2, A_link_mask, eps=0.3)
    p_fixed = plaquette_mean(U)
    print(f"After 300 sweeps FIXED (K_eff direct) : ⟨P⟩ = {p_fixed:.4f}", flush=True)

    # BUGGY version
    U = U_cold
    k = key
    for s in range(300):
        k, sk = random.split(k)
        U = metropolis_sweep_4dir_BUGGY(U, beta, alpha, sk, L, L, L, L//2, A_link_mask, eps=0.3)
    p_buggy = plaquette_mean(U)
    print(f"After 300 sweeps BUGGY (K_dag) : ⟨P⟩ = {p_buggy:.4f}", flush=True)

    print(f"\nVerdict :", flush=True)
    if 0.5 < p_fixed < 0.75:
        print(f"  FIXED : ⟨P⟩ = {p_fixed:.4f} ≈ littérature ✅ — patch correct", flush=True)
    if p_buggy < 0:
        print(f"  BUGGY : ⟨P⟩ = {p_buggy:.4f} < 0 ❌ — bug confirmé → tous résultats BP2008b INVALIDES", flush=True)
    elif 0.5 < p_buggy < 0.75:
        print(f"  BUGGY : ⟨P⟩ = {p_buggy:.4f} ≈ littérature ⚠️ — bug compensé quelque part, résultats peut-être sauvés", flush=True)
    else:
        print(f"  BUGGY : ⟨P⟩ = {p_buggy:.4f} étrange — investigate plus loin", flush=True)


if __name__ == "__main__":
    main()
