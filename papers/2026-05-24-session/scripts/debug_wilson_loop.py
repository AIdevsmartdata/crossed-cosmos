#!/usr/bin/env python3
"""Debug Wilson loop construction vs standard plaquette computation."""
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
from functools import partial
from jax import jit

thermalize_standard = g['thermalize_standard']
wilson_action = g['wilson_action']

# Compute standard plaquette mean
def plaquette_mean(U):
    pl = 0.0
    n_pl = 0
    for mu in range(4):
        for nu in range(mu+1, 4):
            U_mu = U[..., mu, :, :]
            U_nu = U[..., nu, :, :]
            U_mu_pnu = jnp.roll(U_mu, -1, axis=nu)
            U_nu_pmu = jnp.roll(U_nu, -1, axis=mu)
            P = jnp.einsum('...ij,...jk,...lk,...ml->...im',
                           U_mu, U_nu_pmu,
                           jnp.conjugate(U_mu_pnu),
                           jnp.conjugate(U_nu))
            tr = jnp.real(jnp.trace(P, axis1=-2, axis2=-1)) / 2
            pl += float(tr.mean())
            n_pl += 1
    return pl / n_pl


# My parallel transport
def parallel_transport(U, mu, length):
    P = U[..., mu, :, :]
    for k in range(1, length):
        U_shift = jnp.roll(U[..., mu, :, :], -k, axis=mu)
        P = jnp.einsum('...ij,...jk->...ik', P, U_shift)
    return P


def wilson_loop_plane_v1(U, mu, nu, R, T):
    """My version."""
    T_mu = parallel_transport(U, mu, R)
    T_nu_atμ = parallel_transport(U, nu, T)
    T_nu_atμ = jnp.roll(T_nu_atμ, -R, axis=mu)
    T_mu_atν = parallel_transport(U, mu, R)
    T_mu_atν = jnp.roll(T_mu_atν, -T, axis=nu)
    T_nu = parallel_transport(U, nu, T)

    W = jnp.einsum('...ij,...jk,...lk,...ml->...im',
                   T_mu, T_nu_atμ,
                   jnp.conjugate(T_mu_atν),
                   jnp.conjugate(T_nu))
    return jnp.real(jnp.trace(W, axis1=-2, axis2=-1)).mean() / 2.0


def wilson_loop_plane_v2_direct(U, mu, nu, R, T):
    """Alternative version with explicit conjugate-transpose."""
    T_mu = parallel_transport(U, mu, R)
    T_nu_atμ = jnp.roll(parallel_transport(U, nu, T), -R, axis=mu)
    T_mu_atν = jnp.roll(parallel_transport(U, mu, R), -T, axis=nu)
    T_nu = parallel_transport(U, nu, T)

    # Explicit dagger: swap last two axes then conjugate
    T_mu_atν_dag = jnp.conjugate(jnp.swapaxes(T_mu_atν, -1, -2))
    T_nu_dag = jnp.conjugate(jnp.swapaxes(T_nu, -1, -2))

    W = jnp.einsum('...ij,...jk,...kl,...lm->...im',
                   T_mu, T_nu_atμ, T_mu_atν_dag, T_nu_dag)
    return jnp.real(jnp.trace(W, axis1=-2, axis2=-1)).mean() / 2.0


def main():
    L = 8
    beta = 2.3

    print(f"Test Wilson loop at L={L}, β={beta}", flush=True)
    print(f"Thermalize 200 sweeps...", flush=True)
    key = random.PRNGKey(42)
    U, key = thermalize_standard(key, beta, L, 200, eps=0.3)

    print(f"\n=== Standard plaquette (wilson_action verified) ===")
    pl = plaquette_mean(U)
    print(f"⟨P⟩ = {pl:.4f}  (expected ~0.62 at β=2.3)")

    print(f"\n=== My wilson_loop R=1 T=1 in plane (0, 1) — should equal plaquette in (0,1) ===")
    # Compute plaquette only in (0,1) plane for fair comparison
    U_mu = U[..., 0, :, :]
    U_nu = U[..., 1, :, :]
    U_mu_pnu = jnp.roll(U_mu, -1, axis=1)
    U_nu_pmu = jnp.roll(U_nu, -1, axis=0)
    P = jnp.einsum('...ij,...jk,...lk,...ml->...im',
                   U_mu, U_nu_pmu,
                   jnp.conjugate(U_mu_pnu),
                   jnp.conjugate(U_nu))
    tr_pl_01 = jnp.real(jnp.trace(P, axis1=-2, axis2=-1)) / 2
    pl_01 = float(tr_pl_01.mean())
    print(f"plaquette(0,1) = {pl_01:.4f}")

    w_v1 = wilson_loop_plane_v1(U, 0, 1, 1, 1)
    print(f"wilson_loop_v1 R=T=1 (mu=0, nu=1) = {w_v1:.4f}")

    w_v2 = wilson_loop_plane_v2_direct(U, 0, 1, 1, 1)
    print(f"wilson_loop_v2_direct R=T=1 (mu=0, nu=1) = {w_v2:.4f}")

    print(f"\n=== W(2,2) (mu=0, nu=1) — expected exp(-σ·4) ~0.15 ===")
    w_v1_22 = wilson_loop_plane_v1(U, 0, 1, 2, 2)
    w_v2_22 = wilson_loop_plane_v2_direct(U, 0, 1, 2, 2)
    print(f"v1 = {w_v1_22:.4f}, v2 = {w_v2_22:.4f}")


if __name__ == "__main__":
    main()
