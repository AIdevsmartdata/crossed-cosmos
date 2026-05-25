#!/usr/bin/env python3
"""JAX SU(3) lattice gauge primitives — port from SU(2) FAST V3 + bug fixes.

Includes :
- Gell-Mann matrices + SU(3) generators
- Random SU(3) Haar (QR + det correction)
- Random SU(3) near-identity (Taylor expm of small Hermitian)
- Wilson action SU(3) (Tr / N=3)
- compute_staple_sum SU(3) (post bug fix, standard order)
- metropolis_sweep_standard SU(3) (uses K not K_dag — post bug fix)
- thermalize_standard SU(3)

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


# ============================================================================
# Gell-Mann generators (λ_a / 2 are SU(3) generators)
# ============================================================================

def gell_mann_matrices():
    """Return 8 Gell-Mann matrices λ_a (Hermitian, traceless)."""
    L = [
        # λ1
        jnp.array([[0, 1, 0], [1, 0, 0], [0, 0, 0]], dtype=jnp.complex128),
        # λ2
        jnp.array([[0, -1j, 0], [1j, 0, 0], [0, 0, 0]], dtype=jnp.complex128),
        # λ3
        jnp.array([[1, 0, 0], [0, -1, 0], [0, 0, 0]], dtype=jnp.complex128),
        # λ4
        jnp.array([[0, 0, 1], [0, 0, 0], [1, 0, 0]], dtype=jnp.complex128),
        # λ5
        jnp.array([[0, 0, -1j], [0, 0, 0], [1j, 0, 0]], dtype=jnp.complex128),
        # λ6
        jnp.array([[0, 0, 0], [0, 0, 1], [0, 1, 0]], dtype=jnp.complex128),
        # λ7
        jnp.array([[0, 0, 0], [0, 0, -1j], [0, 1j, 0]], dtype=jnp.complex128),
        # λ8
        jnp.array([[1, 0, 0], [0, 1, 0], [0, 0, -2]], dtype=jnp.complex128) / jnp.sqrt(3.0),
    ]
    return jnp.stack(L, axis=0)  # (8, 3, 3)


GELL_MANN = gell_mann_matrices()


# ============================================================================
# Random SU(3) matrices
# ============================================================================

def random_su3_haar(key, shape):
    """Generate Haar-random SU(3) matrices of given shape (batch, 3, 3).

    Method : 3 random complex vectors → QR decomp → fix det=1.
    """
    # Sample complex Gaussian 3x3 matrix
    key1, key2 = random.split(key)
    real_part = random.normal(key1, shape + (3, 3))
    imag_part = random.normal(key2, shape + (3, 3))
    M = (real_part + 1j * imag_part) / jnp.sqrt(2.0)

    # QR decomposition
    Q, R = jnp.linalg.qr(M)

    # Sign-correct diagonal of R (so Q has Haar distribution on U(3))
    diag_R = jnp.diagonal(R, axis1=-2, axis2=-1)
    phase = diag_R / jnp.abs(diag_R)  # unit complex per diag entry
    Q = Q * phase[..., None, :]  # multiply each column by phase

    # Now Q is Haar on U(3). Divide by det(Q)^(1/3) to get SU(3).
    det_Q = jnp.linalg.det(Q)
    cube_root = det_Q ** (1.0 / 3.0)
    Q = Q / cube_root[..., None, None]

    return Q


def random_su3_near_identity(key, shape, eps=0.2):
    """Generate SU(3) matrices close to identity via Taylor expm of small Hermitian.

    Sample 8 small θ_a ~ N(0, eps²), build H = (1/2) Σ θ_a λ_a (Hermitian),
    return U = expm(iH) ≈ I + iH - H²/2 - iH³/6 + H⁴/24 (4-term Taylor).
    """
    # Sample 8 real Gaussians
    theta = random.normal(key, shape + (8,)) * eps  # (..., 8)

    # H = (1/2) Σ_a θ_a λ_a
    # GELL_MANN shape (8, 3, 3). theta shape (..., 8). Broadcasting :
    H = 0.5 * jnp.einsum('...a,abc->...bc', theta, GELL_MANN)  # (..., 3, 3)
    # H is Hermitian. Compute U = expm(iH) via Taylor.

    iH = 1j * H
    iH2 = jnp.einsum('...ij,...jk->...ik', iH, iH)
    iH3 = jnp.einsum('...ij,...jk->...ik', iH2, iH)
    iH4 = jnp.einsum('...ij,...jk->...ik', iH2, iH2)
    iH5 = jnp.einsum('...ij,...jk->...ik', iH4, iH)

    I = jnp.eye(3, dtype=jnp.complex128)
    U = I + iH + iH2 / 2.0 + iH3 / 6.0 + iH4 / 24.0 + iH5 / 120.0

    # Project to SU(3) : (a) normalize each row, (b) ensure det=1
    # For small eps the U is already close to SU(3); just fix det
    det_U = jnp.linalg.det(U)
    cube_root = det_U ** (1.0 / 3.0)
    U = U / cube_root[..., None, None]
    return U


# ============================================================================
# Wilson action SU(3)
# ============================================================================

def wilson_action_su3(U, beta):
    """SU(3) Wilson action : S = β Σ_plaq (1 - Re Tr P / 3).

    Returns total action (β-multiplied).
    """
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
            tr_real = jnp.real(jnp.trace(P, axis1=-2, axis2=-1)) / 3.0
            total += jnp.sum(1.0 - tr_real)
    return beta * total


def plaquette_mean_su3(U):
    """⟨P⟩ = ⟨Re Tr P / 3⟩ averaged over all plaquettes."""
    return 1.0 - float(wilson_action_su3(U, 1.0)) / (6 * U.shape[0]**4)


# ============================================================================
# Staple sum SU(3) — STANDARD ORDER (post bug fix)
# ============================================================================

def compute_staple_sum_su3(U, mu, L):
    """Standard staple sum K(x, μ) for SU(3) Wilson : Σ_ν of forward + backward.

    Forward staple : U_ν(x+μ̂) · U_μ(x+ν̂)† · U_ν(x)†   [STANDARD ORDER post fix]
    Backward staple : U_ν(x-ν̂+μ̂)† · U_μ(x-ν̂)† · U_ν(x-ν̂)
    """
    U_mu = U[..., mu, :, :]
    K = jnp.zeros_like(U_mu)
    for nu in range(4):
        if nu == mu:
            continue
        U_nu = U[..., nu, :, :]
        U_nu_pmu = jnp.roll(U_nu, -1, axis=mu)
        U_mu_pnu = jnp.roll(U_mu, -1, axis=nu)
        # Forward : U_ν(x+μ̂) · U_μ(x+ν̂)† · U_ν(x)†
        K_fwd = jnp.einsum('...ij,...kj,...lk->...il',
                           U_nu_pmu,
                           jnp.conjugate(U_mu_pnu),
                           jnp.conjugate(U_nu))
        K += K_fwd
        # Backward
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
# Metropolis sweep SU(3) — POST BUG FIX (uses K, not K_dag)
# ============================================================================

@partial(jit, static_argnames=('L',))
def metropolis_sweep_su3(U, beta, key, L, eps=0.2):
    """Standard per-link Metropolis SU(3) using K (NOT K_dag — post bug fix).

    dS = -β/N · (Re Tr(U_new · K) - Re Tr(U_old · K)) with N=3.
    """
    for mu in range(4):
        K_mu = compute_staple_sum_su3(U, mu, L)
        key, k_prop, k_acc = random.split(key, 3)
        X = random_su3_near_identity(k_prop, U[..., mu, :, :].shape[:-2], eps=eps)
        U_proposed_mu = jnp.einsum('...ij,...jk->...ik', X, U[..., mu, :, :])
        # FIX : use K_mu directly (not K_dag)
        new_term = jnp.real(jnp.trace(jnp.einsum('...ij,...jk->...ik', U_proposed_mu, K_mu),
                                        axis1=-2, axis2=-1))
        old_term = jnp.real(jnp.trace(jnp.einsum('...ij,...jk->...ik', U[..., mu, :, :], K_mu),
                                        axis1=-2, axis2=-1))
        dS = -beta / 3.0 * (new_term - old_term)
        rand_u = random.uniform(k_acc, dS.shape)
        accept = rand_u < jnp.exp(jnp.minimum(0.0, -dS))
        U_mu_new = jnp.where(accept[..., None, None], U_proposed_mu, U[..., mu, :, :])
        U = U.at[..., mu, :, :].set(U_mu_new)
    return U


def thermalize_standard_su3(key, beta, L, n_sweeps, eps=0.2):
    """Thermalize SU(3) Wilson lattice from random Haar start."""
    k, sk = random.split(key)
    U = random_su3_haar(sk, (L, L, L, L, 4))
    for i in range(n_sweeps):
        k, sk = random.split(k)
        U = metropolis_sweep_su3(U, beta, sk, L, eps)
    return U, k


# ============================================================================
# Self-test (only if run directly)
# ============================================================================

if __name__ == "__main__":
    import time

    print("Self-test SU(3) primitives", flush=True)
    print("=" * 60, flush=True)

    # Test 1: Haar SU(3) — det should be 1, U†U should be I
    key = random.PRNGKey(42)
    U_test = random_su3_haar(key, (4,))  # 4 samples
    print(f"\nTest 1 : random_su3_haar shape={U_test.shape}", flush=True)
    dets = jnp.linalg.det(U_test)
    print(f"  det(U) = {dets} (should be 1+0j)", flush=True)
    UU = jnp.einsum('...ij,...kj->...ik', U_test, jnp.conjugate(U_test))
    err = jnp.max(jnp.abs(UU - jnp.eye(3, dtype=jnp.complex128)))
    print(f"  max|U·U† - I| = {err:.2e}", flush=True)

    # Test 2: Near-identity SU(3)
    U_ni = random_su3_near_identity(key, (4,), eps=0.2)
    print(f"\nTest 2 : random_su3_near_identity (eps=0.2)", flush=True)
    print(f"  det(U) = {jnp.linalg.det(U_ni)}", flush=True)
    UU_ni = jnp.einsum('...ij,...kj->...ik', U_ni, jnp.conjugate(U_ni))
    err_ni = jnp.max(jnp.abs(UU_ni - jnp.eye(3, dtype=jnp.complex128)))
    print(f"  max|U·U† - I| = {err_ni:.2e}", flush=True)

    # Test 3: Thermalize at β=5.4 (matched 't Hooft to SU(2) β=2.4)
    # Expected ⟨P⟩ at β=5.4 ≈ 0.55-0.60 (Lucini-Teper)
    print(f"\nTest 3 : Thermalize L=6, β=5.4 (matched 't Hooft λ=10/3 to SU(2) β=2.4)", flush=True)
    L = 6
    beta = 5.4
    print(f"  Initial random Haar...", flush=True)
    t0 = time.time()
    key, sk = random.split(key)
    U = random_su3_haar(sk, (L, L, L, L, 4))
    p_init = plaquette_mean_su3(U)
    print(f"  ⟨P⟩ initial Haar = {p_init:.4f}", flush=True)

    print(f"  Thermalizing 100 sweeps...", flush=True)
    for i in range(100):
        key, sk = random.split(key)
        U = metropolis_sweep_su3(U, beta, sk, L, eps=0.2)
        if (i + 1) % 25 == 0:
            p = plaquette_mean_su3(U)
            print(f"    sweep {i+1}: ⟨P⟩ = {p:.4f}  (t={time.time()-t0:.1f}s)", flush=True)

    p_final = plaquette_mean_su3(U)
    print(f"\n  Final ⟨P⟩ = {p_final:.4f}", flush=True)
    print(f"  Lucini-Teper SU(3) β=5.4 → ⟨P⟩ ≈ 0.55-0.60", flush=True)
    if 0.45 < p_final < 0.70:
        print(f"  ✅ ⟨P⟩ dans range littérature", flush=True)
    else:
        print(f"  ❌ ⟨P⟩ hors range — debug needed", flush=True)
