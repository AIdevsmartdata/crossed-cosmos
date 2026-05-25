#!/usr/bin/env python3
"""JAX SU(6) lattice primitives — pour test discriminant cross-N ECI.

Test critique : (N²-1)/N² scaling vs √N scaling.

SU(2) : κ = 0.5080 ± 0.0036 (mesuré L=8..12 β=2.4)
SU(3) : κ = 0.6025 ± 0.0033 (mesuré L=8..12 β=5.4 matched)

(N²-1)/N² fit : κ_∞ ≈ 0.6779
  → SU(6) prédit κ = κ_∞ · 15/16 = 0.6356

√N fit : κ_∞ A ≈ 0.359
  → SU(6) prédit κ = A · √4 = 0.719

Diff = 0.083 → ~15σ discriminating si précision ~0.005.

Approche : générique pour 4×4 matrices via Hermitian traceless basis random.

Author : Kévin Rémondière (ORCID 0009-0008-2443-7166).
"""
import os
os.environ.setdefault('XLA_PYTHON_CLIENT_PREALLOCATE', 'false')
os.environ.setdefault('JAX_ENABLE_X64', 'True')

import jax
import jax.numpy as jnp
from jax import jit, random
from functools import partial
import numpy as np

N_GROUP = 6  # SU(N=4)


# ============================================================================
# Random SU(6) matrices via complex Gaussian + projection
# ============================================================================

def random_su6_haar(key, shape):
    """Haar-random SU(6) matrices : QR decomp + det^(1/4) normalization."""
    key1, key2 = random.split(key)
    real_part = random.normal(key1, shape + (N_GROUP, N_GROUP))
    imag_part = random.normal(key2, shape + (N_GROUP, N_GROUP))
    M = (real_part + 1j * imag_part) / jnp.sqrt(2.0)
    Q, R = jnp.linalg.qr(M)
    diag_R = jnp.diagonal(R, axis1=-2, axis2=-1)
    phase = diag_R / jnp.abs(diag_R)
    Q = Q * phase[..., None, :]
    det_Q = jnp.linalg.det(Q)
    fourth_root = det_Q ** (1.0 / N_GROUP)
    Q = Q / fourth_root[..., None, None]
    return Q


def random_su6_near_identity(key, shape, eps=0.10):
    """SU(6) near identity : Taylor expm of small Hermitian traceless H."""
    key1, key2 = random.split(key)
    real_M = random.normal(key1, shape + (N_GROUP, N_GROUP)) * eps
    imag_M = random.normal(key2, shape + (N_GROUP, N_GROUP)) * eps
    M = real_M + 1j * imag_M
    # Hermitian part : (M + M†)/2
    H = 0.5 * (M + jnp.conjugate(jnp.swapaxes(M, -1, -2)))
    # Traceless : H -= Tr(H)/N · I
    tr_H = jnp.trace(H, axis1=-2, axis2=-1)
    I = jnp.eye(N_GROUP, dtype=jnp.complex128)
    H = H - (tr_H[..., None, None] / N_GROUP) * I
    # exp(iH) Taylor 5 terms
    iH = 1j * H
    iH2 = jnp.einsum('...ij,...jk->...ik', iH, iH)
    iH3 = jnp.einsum('...ij,...jk->...ik', iH2, iH)
    iH4 = jnp.einsum('...ij,...jk->...ik', iH2, iH2)
    iH5 = jnp.einsum('...ij,...jk->...ik', iH4, iH)
    U = I + iH + iH2 / 2.0 + iH3 / 6.0 + iH4 / 24.0 + iH5 / 120.0
    # Project to SU(N)
    det_U = jnp.linalg.det(U)
    fourth_root = det_U ** (1.0 / N_GROUP)
    U = U / fourth_root[..., None, None]
    return U


# ============================================================================
# Wilson action SU(6) — /N=4 normalization
# ============================================================================

def wilson_action_su6(U, beta):
    total = 0.0
    for mu in range(4):
        for nu in range(mu + 1, 4):
            U_mu = U[..., mu, :, :]
            U_nu = U[..., nu, :, :]
            U_mu_pnu = jnp.roll(U_mu, -1, axis=nu)
            U_nu_pmu = jnp.roll(U_nu, -1, axis=mu)
            P = jnp.einsum('...ij,...jk,...lk,...ml->...im',
                           U_mu, U_nu_pmu,
                           jnp.conjugate(U_mu_pnu),
                           jnp.conjugate(U_nu))
            tr_real = jnp.real(jnp.trace(P, axis1=-2, axis2=-1)) / N_GROUP
            total += jnp.sum(1.0 - tr_real)
    return beta * total


def plaquette_mean_su6(U):
    """⟨P⟩ for asymmetric shapes too."""
    n_plaq = 6 * int(np.prod(U.shape[:4]))
    return 1.0 - float(wilson_action_su6(U, 1.0)) / n_plaq


# ============================================================================
# Compute staple sum (standard, post-fix order) — works for any SU(N)
# ============================================================================

def compute_staple_sum_su6(U, mu, L):
    U_mu = U[..., mu, :, :]
    K = jnp.zeros_like(U_mu)
    for nu in range(4):
        if nu == mu:
            continue
        U_nu = U[..., nu, :, :]
        U_nu_pmu = jnp.roll(U_nu, -1, axis=mu)
        U_mu_pnu = jnp.roll(U_mu, -1, axis=nu)
        K_fwd = jnp.einsum('...ij,...kj,...lk->...il',
                           U_nu_pmu,
                           jnp.conjugate(U_mu_pnu),
                           jnp.conjugate(U_nu))
        K += K_fwd
        U_nu_pmu_mnu = jnp.roll(U_nu_pmu, 1, axis=nu)
        U_mu_mnu = jnp.roll(U_mu, 1, axis=nu)
        U_nu_mnu = jnp.roll(U_nu, 1, axis=nu)
        K_bwd = jnp.einsum('...ji,...kj,...kl->...il',
                           jnp.conjugate(U_nu_pmu_mnu),
                           jnp.conjugate(U_mu_mnu),
                           U_nu_mnu)
        K += K_bwd
    return K


# ============================================================================
# Metropolis (post-fix : K direct, /N=4)
# ============================================================================

@partial(jit, static_argnames=('L',))
def metropolis_sweep_su6(U, beta, key, L, eps=0.10):
    for mu in range(4):
        K_mu = compute_staple_sum_su6(U, mu, L)
        key, k_prop, k_acc = random.split(key, 3)
        X = random_su6_near_identity(k_prop, U[..., mu, :, :].shape[:-2], eps=eps)
        U_proposed_mu = jnp.einsum('...ij,...jk->...ik', X, U[..., mu, :, :])
        new_term = jnp.real(jnp.trace(jnp.einsum('...ij,...jk->...ik', U_proposed_mu, K_mu),
                                        axis1=-2, axis2=-1))
        old_term = jnp.real(jnp.trace(jnp.einsum('...ij,...jk->...ik', U[..., mu, :, :], K_mu),
                                        axis1=-2, axis2=-1))
        dS = -beta / N_GROUP * (new_term - old_term)
        rand_u = random.uniform(k_acc, dS.shape)
        accept = rand_u < jnp.exp(jnp.minimum(0.0, -dS))
        U_mu_new = jnp.where(accept[..., None, None], U_proposed_mu, U[..., mu, :, :])
        U = U.at[..., mu, :, :].set(U_mu_new)
    return U


def thermalize_standard_su6(key, beta, L, n_sweeps, eps=0.10):
    k, sk = random.split(key)
    U = random_su6_haar(sk, (L, L, L, L, 4))
    for i in range(n_sweeps):
        k, sk = random.split(k)
        U = metropolis_sweep_su6(U, beta, sk, L, eps)
    return U, k


# ============================================================================
# Self-test
# ============================================================================

if __name__ == "__main__":
    import time
    print("=== SU(6) self-test ===", flush=True)
    print("Expected ⟨P⟩ at SU(6) matched 't Hooft β=9.6 ≈ 0.40-0.45 (extrap lit)\n",
          flush=True)

    # Test 1: Haar
    key = random.PRNGKey(42)
    U_h = random_su6_haar(key, (4,))
    print(f"Haar SU(6) :")
    print(f"  det = {jnp.linalg.det(U_h)}")
    err = jnp.max(jnp.abs(jnp.einsum('...ij,...kj->...ik', U_h, jnp.conjugate(U_h))
                          - jnp.eye(4, dtype=jnp.complex128)))
    print(f"  max|UU† - I| = {float(err):.2e}\n")

    # Test 2: Near identity
    U_ni = random_su6_near_identity(key, (4,), eps=0.10)
    print(f"Near-identity SU(6) (eps=0.10) :")
    print(f"  det = {jnp.linalg.det(U_ni)}")
    err = jnp.max(jnp.abs(jnp.einsum('...ij,...kj->...ik', U_ni, jnp.conjugate(U_ni))
                          - jnp.eye(4, dtype=jnp.complex128)))
    print(f"  max|UU† - I| = {float(err):.2e}\n")

    # Test 3: thermalize at multiple β
    L = 4
    for beta in [9.6, 10.0, 10.5, 11.0]:
        key = random.PRNGKey(2026 + int(beta * 100))
        key, sk = random.split(key)
        U = random_su6_haar(sk, (L, L, L, L, 4))
        t0 = time.time()
        for i in range(300):
            key, sk = random.split(key)
            U = metropolis_sweep_su6(U, beta, sk, L, eps=0.10)
        p = plaquette_mean_su6(U)
        print(f"SU(6) L={L} β={beta:.1f} 300 sweeps : ⟨P⟩ = {p:.4f} ({time.time()-t0:.1f}s)",
              flush=True)
