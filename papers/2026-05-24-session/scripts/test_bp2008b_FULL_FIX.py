#!/usr/bin/env python3
"""Test BP2008b avec FULL FIX : staple order + K_eff direct (pas K_dag)."""
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

import jax
import jax.numpy as jnp
import numpy as np
from jax import random, jit
from functools import partial

# Pull functions
random_su2_haar = g['random_su2_haar']
random_su2_near_identity = g['random_su2_near_identity']
gather_link_at_t = g['gather_link_at_t']
make_next_t_arrays = g['make_next_t_arrays']
make_prev_t_arrays = g['make_prev_t_arrays']
wilson_action = g2['wilson_action']


def plaquette_mean(U):
    L = U.shape[0]
    return 1.0 - float(wilson_action(U, 1.0)) / (6 * L**4)


# CORRECT compute_staples : standard order U_ν(x+μ̂) · U_μ(x+ν̂)† · U_ν(x)†
@partial(jit, static_argnames=('mu', 'L_x', 'L_y', 'L_z', 'T_half'))
def compute_staples_K_T_K_2T_FIXED(U, mu, L_x, L_y, L_z, T_half):
    twoT = 2 * T_half
    next_t_T, next_t_2T = make_next_t_arrays(T_half)
    prev_t_T, prev_t_2T = make_prev_t_arrays(T_half)

    K_T = jnp.zeros_like(U[..., mu, :, :])
    K_2T = jnp.zeros_like(U[..., mu, :, :])

    for nu in range(4):
        if nu == mu:
            continue
        U_nu = U[..., nu, :, :]
        U_mu = U[..., mu, :, :]

        if nu == 3:
            U_mu_at_xpnu_T = gather_link_at_t(U_mu, next_t_T)
            U_mu_at_xpnu_2T = gather_link_at_t(U_mu, next_t_2T)
            U_nu_at_xpmu = jnp.roll(U_nu, -1, axis=mu)
            # FIXED: standard forward staple = U_ν(x+μ̂) · U_μ(x+ν̂)† · U_ν(x)†
            K_T_fwd = jnp.einsum('...ij,...kj,...lk->...il',
                                  U_nu_at_xpmu, jnp.conjugate(U_mu_at_xpnu_T),
                                  jnp.conjugate(U_nu))
            K_2T_fwd = jnp.einsum('...ij,...kj,...lk->...il',
                                   U_nu_at_xpmu, jnp.conjugate(U_mu_at_xpnu_2T),
                                   jnp.conjugate(U_nu))
            K_T += K_T_fwd
            K_2T += K_2T_fwd
            # Backward staple : U_ν(x-ν̂+μ̂)† · U_μ(x-ν̂)† · U_ν(x-ν̂)
            U_nu_at_xmnu_T = gather_link_at_t(U_nu, prev_t_T)
            U_nu_at_xmnu_2T = gather_link_at_t(U_nu, prev_t_2T)
            U_mu_at_xmnu_T = gather_link_at_t(U_mu, prev_t_T)
            U_mu_at_xmnu_2T = gather_link_at_t(U_mu, prev_t_2T)
            U_nu_at_xmnu_pmu_T = jnp.roll(U_nu_at_xmnu_T, -1, axis=mu)
            U_nu_at_xmnu_pmu_2T = jnp.roll(U_nu_at_xmnu_2T, -1, axis=mu)
            K_T_bwd = jnp.einsum('...ji,...kj,...kl->...il',
                                  jnp.conjugate(U_nu_at_xmnu_pmu_T),
                                  jnp.conjugate(U_mu_at_xmnu_T),
                                  U_nu_at_xmnu_T)
            K_2T_bwd = jnp.einsum('...ji,...kj,...kl->...il',
                                   jnp.conjugate(U_nu_at_xmnu_pmu_2T),
                                   jnp.conjugate(U_mu_at_xmnu_2T),
                                   U_nu_at_xmnu_2T)
            K_T += K_T_bwd
            K_2T += K_2T_bwd
        else:
            U_nu_at_xpmu = jnp.roll(U_nu, -1, axis=mu)
            if mu == 3:
                U_mu_at_xpnu = jnp.roll(U_mu, -1, axis=nu)
                K_fwd = jnp.einsum('...ij,...kj,...lk->...il',
                                    U_nu_at_xpmu, jnp.conjugate(U_mu_at_xpnu),
                                    jnp.conjugate(U_nu))
                K_T += K_fwd
                K_2T += K_fwd
                U_nu_at_xmnu = jnp.roll(U_nu, 1, axis=nu)
                U_mu_at_xmnu = jnp.roll(U_mu, 1, axis=nu)
                U_nu_at_xmnu_pmu = jnp.roll(U_nu_at_xmnu, -1, axis=mu)
                K_bwd = jnp.einsum('...ji,...kj,...kl->...il',
                                    jnp.conjugate(U_nu_at_xmnu_pmu),
                                    jnp.conjugate(U_mu_at_xmnu),
                                    U_nu_at_xmnu)
                K_T += K_bwd
                K_2T += K_bwd
            else:
                U_mu_at_xpnu = jnp.roll(U_mu, -1, axis=nu)
                K_fwd = jnp.einsum('...ij,...kj,...lk->...il',
                                    U_nu_at_xpmu, jnp.conjugate(U_mu_at_xpnu),
                                    jnp.conjugate(U_nu))
                K_T += K_fwd
                K_2T += K_fwd
                U_nu_at_xmnu = jnp.roll(U_nu, 1, axis=nu)
                U_mu_at_xmnu = jnp.roll(U_mu, 1, axis=nu)
                U_nu_at_xmnu_pmu = jnp.roll(U_nu_at_xmnu, -1, axis=mu)
                K_bwd = jnp.einsum('...ji,...kj,...kl->...il',
                                    jnp.conjugate(U_nu_at_xmnu_pmu),
                                    jnp.conjugate(U_mu_at_xmnu),
                                    U_nu_at_xmnu)
                K_T += K_bwd
                K_2T += K_bwd
    return K_T, K_2T


@partial(jit, static_argnames=('mu', 'L_x', 'L_y', 'L_z', 'T_half'))
def metropolis_FULL_FIX(U, beta, alpha, key, mu, L_x, L_y, L_z, T_half, A_link_mask, eps=0.3):
    K_T, K_2T = compute_staples_K_T_K_2T_FIXED(U, mu, L_x, L_y, L_z, T_half)
    K_eff = jnp.where(A_link_mask[..., mu, None, None], (1 - alpha) * K_T + alpha * K_2T, K_T)
    key1, key2 = random.split(key)
    X = random_su2_near_identity(key1, U[..., mu, :, :].shape[:-2], eps=eps)
    U_proposed = jnp.einsum('...ij,...jk->...ik', X, U[..., mu, :, :])
    new_term = jnp.real(jnp.trace(jnp.einsum('...ij,...jk->...ik', U_proposed, K_eff), axis1=-2, axis2=-1))
    old_term = jnp.real(jnp.trace(jnp.einsum('...ij,...jk->...ik', U[..., mu, :, :], K_eff), axis1=-2, axis2=-1))
    dS = -beta * 0.5 * (new_term - old_term)
    rand_u = random.uniform(key2, dS.shape)
    accept = rand_u < jnp.exp(jnp.minimum(0.0, -dS))
    U_mu_new = jnp.where(accept[..., None, None], U_proposed, U[..., mu, :, :])
    return U.at[..., mu, :, :].set(U_mu_new)


@partial(jit, static_argnames=('L_x', 'L_y', 'L_z', 'T_half'))
def sweep_full_fix_4dir(U, beta, alpha, key, L_x, L_y, L_z, T_half, A_link_mask, eps=0.3):
    for mu in range(4):
        key, sk = random.split(key)
        U = metropolis_FULL_FIX(U, beta, alpha, sk, mu, L_x, L_y, L_z, T_half, A_link_mask, eps)
    return U


def main():
    L = 8
    beta = 2.4
    print(f"Test BP2008b FULL FIX (staple order + K_eff direct) at L={L}, β={beta}", flush=True)
    print(f"Expected ⟨P⟩ ≈ 0.64\n", flush=True)
    A_link_mask = jnp.zeros((L, L, L, L, 4), dtype=bool)
    alpha = 0.0
    key = random.PRNGKey(2024)
    I_mat = jnp.eye(2, dtype=jnp.complex128)
    U_cold = jnp.zeros((L,)*4 + (4, 2, 2), dtype=jnp.complex128) + I_mat
    U = U_cold
    k = key
    for s in range(500):
        k, sk = random.split(k)
        U = sweep_full_fix_4dir(U, beta, alpha, sk, L, L, L, L//2, A_link_mask, eps=0.3)
        if (s+1) % 100 == 0:
            print(f"  After {s+1} sweeps : ⟨P⟩ = {plaquette_mean(U):.4f}", flush=True)
    p_full = plaquette_mean(U)
    print(f"\nFINAL ⟨P⟩ = {p_full:.4f}", flush=True)
    if 0.5 < p_full < 0.75:
        print(f"  ✅ MATCH LITERATURE — BP2008b FULL FIX correct", flush=True)
    else:
        print(f"  ❌ Still off — need deeper debug", flush=True)


if __name__ == "__main__":
    main()
