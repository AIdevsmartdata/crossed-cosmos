#!/usr/bin/env python3
"""Diagnostic SU(3) BP2008b : ⟨P⟩=-0.22 anomaly.

Test : remplacer compute_staples_K_T_K_2T_su3 par standard compute_staple_sum_su3.
À α=0, K_eff doit être équivalent au standard (non-junction sites identiques).
Si ⟨P⟩ → 0.45 → bug dans K_T_K_2T variant.
Si ⟨P⟩ reste négatif → bug dans Metropolis logique elle-même.
"""
import os
os.environ.setdefault('XLA_PYTHON_CLIENT_PREALLOCATE', 'false')
os.environ.setdefault('JAX_ENABLE_X64', 'True')

import sys
sys.path.insert(0, '/tmp')

# Load SU(3) primitives standalone (validated)
with open('/tmp/jax_su3_lattice_2026-05-25.py') as f:
    src = f.read()
src = src.split('if __name__')[0]
g_su3 = {}
exec(src, g_su3)

# Also load BP2008b structure — strip lines 26-36 (loader block) + final __main__ block
with open('/tmp/jax_su3_EE_BP2008b_FAST_2026-05-25.py') as f:
    src_bp_lines = f.readlines()
# Skip lines 25-36 (0-indexed: 25 to 35 inclusive, which are the loader)
src_bp = ''.join(src_bp_lines[:25] + src_bp_lines[36:])
src_bp = src_bp.split('if __name__')[0]
g_bp = {}
g_bp.update(g_su3)  # pre-populate with SU(3) primitives
exec(src_bp, g_bp)

import jax
import jax.numpy as jnp
from jax import jit, random
from functools import partial
import time
import numpy as np

random_su3_haar = g_su3['random_su3_haar']
random_su3_near_identity = g_su3['random_su3_near_identity']
compute_staple_sum_su3 = g_su3['compute_staple_sum_su3']  # standalone (WORKS)
metropolis_sweep_su3 = g_su3['metropolis_sweep_su3']      # standalone
plaquette_mean_su3 = g_su3['plaquette_mean_su3']
wilson_action_su3 = g_su3['wilson_action_su3']

compute_staples_K_T_K_2T_su3 = g_bp['compute_staples_K_T_K_2T_su3']  # BP2008b variant
make_A_junction_link_mask = g_bp['make_A_junction_link_mask']


# ============================================================================
# Diagnostic A : Compare K_T (BP2008b) vs K_standard at NON-junction sites
# ============================================================================

def diag_A_compare_staples(L, T_half):
    """Build random U, compute K_T(BP) and K_std at non-junction.
    Should be IDENTICAL."""
    print(f"\n=== Diagnostic A : K_T vs K_std at non-junction (L={L} T_half={T_half}) ===",
          flush=True)
    key = random.PRNGKey(2026)
    twoT = 2 * T_half
    U = random_su3_haar(key, (L, L, L, twoT, 4))

    for mu in range(4):
        K_T, K_2T = compute_staples_K_T_K_2T_su3(U, mu, L, L, L, T_half)
        # compute_staple_sum_su3 takes single L but works on asymmetric shape via jnp.roll
        # It will treat the 4th axis as another spatial dim with PBC over its size (twoT)
        K_std = compute_staple_sum_su3(U, mu, L)

        # Compare at non-junction t (e.g., t=1)
        for t_test in [1, T_half + 1]:  # non-junction in both copies
            K_T_t = K_T[:, :, :, t_test, :, :]
            K_std_t = K_std[:, :, :, t_test, :, :]
            diff = jnp.max(jnp.abs(K_T_t - K_std_t))
            print(f"  μ={mu} t={t_test}: max|K_T - K_std| = {float(diff):.3e}", flush=True)


# ============================================================================
# Diagnostic B : Metropolis with STANDARD staples on BP2008b geometry
# ============================================================================

@partial(jit, static_argnames=('mu', 'L'))
def metropolis_sweep_standard_in_bp_geom(U, beta, key, mu, L, eps=0.2):
    """Metropolis with STANDARD K (compute_staple_sum_su3), not K_T_K_2T."""
    K_mu = compute_staple_sum_su3(U, mu, L)
    key, k_prop, k_acc = random.split(key, 3)
    X = random_su3_near_identity(k_prop, U[..., mu, :, :].shape[:-2], eps=eps)
    U_proposed = jnp.einsum('...ij,...jk->...ik', X, U[..., mu, :, :])
    new_term = jnp.real(jnp.trace(jnp.einsum('...ij,...jk->...ik', U_proposed, K_mu),
                                    axis1=-2, axis2=-1))
    old_term = jnp.real(jnp.trace(jnp.einsum('...ij,...jk->...ik', U[..., mu, :, :], K_mu),
                                    axis1=-2, axis2=-1))
    dS = -beta / 3.0 * (new_term - old_term)
    rand_u = random.uniform(k_acc, dS.shape)
    accept = rand_u < jnp.exp(jnp.minimum(0.0, -dS))
    U_mu_new = jnp.where(accept[..., None, None], U_proposed, U[..., mu, :, :])
    return U.at[..., mu, :, :].set(U_mu_new)


def diag_B_thermalize_standard(L, T_half, beta, n_sweeps=300):
    """Thermalize on L³×2T_half geometry but with STANDARD staples.
    Should give ⟨P⟩ ≈ lit value for SU(3) β=5.4."""
    print(f"\n=== Diag B : Standard staples on L={L} × twoT={2*T_half} geom, β={beta} ===",
          flush=True)
    key = random.PRNGKey(2027)
    twoT = 2 * T_half
    U = random_su3_haar(key, (L, L, L, twoT, 4))
    p_init = plaquette_mean_su3(U)
    print(f"  Initial Haar ⟨P⟩ = {p_init:.4f}", flush=True)

    t0 = time.time()
    for i in range(n_sweeps):
        for mu in range(4):
            key, sk = random.split(key)
            U = metropolis_sweep_standard_in_bp_geom(U, beta, sk, mu, L, eps=0.2)
        if (i+1) % 50 == 0:
            print(f"  sweep {i+1}: ⟨P⟩ = {plaquette_mean_su3(U):.4f} (t={time.time()-t0:.1f}s)",
                  flush=True)
    p_final = plaquette_mean_su3(U)
    print(f"  FINAL ⟨P⟩ = {p_final:.4f}  (lit SU(3) β={beta} ≈ 0.45)", flush=True)
    return p_final


# ============================================================================
# Diagnostic C : Run BP2008b metropolis_sweep_perlink_local_su3 directly
# ============================================================================

def diag_C_thermalize_bp(L, T_half, beta, n_sweeps=300):
    """Use the actual BP2008b metropolis at α=0 (K_eff = K_T everywhere)."""
    metropolis_sweep_4dir_su3 = g_bp['metropolis_sweep_4dir_su3']

    print(f"\n=== Diag C : BP2008b metropolis_sweep_4dir_su3 at α=0, L={L} twoT={2*T_half}, β={beta} ===",
          flush=True)
    key = random.PRNGKey(2028)
    twoT = 2 * T_half
    U = random_su3_haar(key, (L, L, L, twoT, 4))
    A_spatial_mask = jnp.indices((L, L, L))[0] < L // 2
    A_link_mask = make_A_junction_link_mask(L, L, L, T_half, A_spatial_mask)
    alpha = 0.0
    eps = 0.2

    p_init = plaquette_mean_su3(U)
    print(f"  Initial Haar ⟨P⟩ = {p_init:.4f}", flush=True)

    t0 = time.time()
    for i in range(n_sweeps):
        key, sk = random.split(key)
        U = metropolis_sweep_4dir_su3(U, beta, alpha, sk, L, L, L, T_half, A_link_mask, eps)
        if (i+1) % 50 == 0:
            print(f"  sweep {i+1}: ⟨P⟩ = {plaquette_mean_su3(U):.4f} (t={time.time()-t0:.1f}s)",
                  flush=True)
    p_final = plaquette_mean_su3(U)
    print(f"  FINAL ⟨P⟩ = {p_final:.4f}", flush=True)
    return p_final


def main():
    print(f"START : {time.ctime()}", flush=True)
    print("=" * 70, flush=True)

    L = 4
    T_half = 4

    # Diagnostic A : K_T vs K_std at non-junction
    diag_A_compare_staples(L, T_half)

    # Diagnostic B : standard staples on BP2008b geometry, α=0
    p_std = diag_B_thermalize_standard(L, T_half, beta=5.4, n_sweeps=200)

    # Diagnostic C : BP2008b metropolis at α=0
    p_bp = diag_C_thermalize_bp(L, T_half, beta=5.4, n_sweeps=200)

    print(f"\n{'='*70}\nVERDICT", flush=True)
    print(f"  Diag B (standard K) : ⟨P⟩ = {p_std:.4f}", flush=True)
    print(f"  Diag C (BP K_T)    : ⟨P⟩ = {p_bp:.4f}", flush=True)
    print(f"  Diff = {p_std - p_bp:.4f}", flush=True)
    if abs(p_bp - p_std) < 0.05:
        print(f"  ✅ K_T and standard give SAME ⟨P⟩ → bug ailleurs", flush=True)
    elif abs(p_std - 0.45) < 0.1 and abs(p_bp + 0.22) < 0.1:
        print(f"  ❌ BUG CONFIRMED in K_T_K_2T variant", flush=True)
    else:
        print(f"  ⚠️ Pattern inattendu — investigate further", flush=True)


if __name__ == "__main__":
    main()
