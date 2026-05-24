#!/usr/bin/env python3
"""KR-CP-BERRY-1 — Berry phase of Dirac zero modes on M_1(SU(2); T⁴).

Pilote SU(2) k=1 (8-dim moduli) pour la voie CP-phase.
Auteur : Kévin Rémondière (ORCID 0009-0008-2443-7166).

═══════════════════════════════════════════════════════════════════════════════
OBJECTIF MATHÉMATIQUE
═══════════════════════════════════════════════════════════════════════════════

Calculer la phase de Berry le long d'une boucle γ ⊂ M_1(SU(2); T⁴)
(moduli 8-dimensionnel hyperkähler des instantons de charge 1 sur T⁴) :

    θ_Berry(γ) = -Im ∮_γ ⟨ψ_A | ∂/∂A | ψ_A⟩ · dA

où ψ_A est le zéro-mode de Dirac dans le fond instanton A(t) le long de γ(t).

Implémentation discrète (Berry-Simon, Resta) :

    θ_Berry = -Im log [ Π_n ⟨ψ_n | ψ_{n+1}⟩ ]

Pour une boucle de rotation de jauge globale α(t) = t ∈ [0, 2π] autour
du Cartan SU(2), on attend θ_Berry = π (terme Wess-Zumino, π_1(SO(3)) = ℤ_2,
le zéro-mode dans la rep fondamentale 2 → -2 sous rotation 2π).

═══════════════════════════════════════════════════════════════════════════════
PIPELINE GPU (RTX 5060 Ti 16 GB, JAX 0.10.1 CUDA, complex128)
═══════════════════════════════════════════════════════════════════════════════

  1) Construire A_μ(x) BPST périodisé sur T⁴ (image-sum 5×5×5×5)
  2) Convertir A_μ → liens U_μ = exp(i g a A_μ)  (a = pas de réseau)
  3) Construire l'opérateur Wilson-Dirac matrix-free D = γ^μ D_μ + (m + (a/2) D²)
  4) Calculer le near-zero mode par LOBPCG sur D†D (réutilise infra KR-FP-3)
  5) Discrétiser γ en N_steps points, calculer overlaps ⟨ψ_n | ψ_{n+1}⟩
  6) θ_Berry = arg Π_n ⟨ψ_n | ψ_{n+1}⟩ (modulo 2π)

═══════════════════════════════════════════════════════════════════════════════
TESTS DE COHÉRENCE
═══════════════════════════════════════════════════════════════════════════════

  T1 : Loop trivial (identité × N_steps) → θ_Berry = 0 (sanity)
  T2 : Loop α ∈ [0, 2π] autour σ³ Cartan      → θ_Berry = ±π (WZW level 1)
  T3 : Loop α ∈ [0, 4π] (deux tours)          → θ_Berry = 0 mod 2π
  T4 : Loop translation T¹ entière            → θ_Berry = 0 (SU(2) k=1)

═══════════════════════════════════════════════════════════════════════════════
"""
import os
os.environ.setdefault('XLA_PYTHON_CLIENT_PREALLOCATE', 'false')
os.environ.setdefault('JAX_ENABLE_X64', 'True')

import jax
import jax.numpy as jnp
from jax import jit, vmap, lax
from functools import partial
import time
import json
import sys
import numpy as np

START = time.time()
print(f"START : {time.ctime()}", flush=True)
print("=" * 78, flush=True)
print("KR-CP-BERRY-1 — Berry phase Dirac zero modes SU(2) k=1 T⁴", flush=True)
print("=" * 78, flush=True)

jax.config.update("jax_enable_x64", True)
print(f"JAX version : {jax.__version__}", flush=True)
print(f"Devices     : {jax.devices()}", flush=True)
print(f"Backend     : {jax.default_backend()}", flush=True)
print(f"x64 enabled : {jax.config.read('jax_enable_x64')}", flush=True)


# ═══════════════════════════════════════════════════════════════════════════
# UTILITAIRES SU(2)
# ═══════════════════════════════════════════════════════════════════════════

# Pauli matrices (complex128)
SIGMA1 = jnp.array([[0, 1], [1, 0]], dtype=jnp.complex128)
SIGMA2 = jnp.array([[0, -1j], [1j, 0]], dtype=jnp.complex128)
SIGMA3 = jnp.array([[1, 0], [0, -1]], dtype=jnp.complex128)
ID2 = jnp.eye(2, dtype=jnp.complex128)
PAULI = jnp.stack([SIGMA1, SIGMA2, SIGMA3], axis=0)  # (3,2,2)


def dag(M):
    return jnp.conjugate(jnp.swapaxes(M, -1, -2))


def su2_from_alg(A_vec):
    """U = exp(i A_vec^a σ^a / 2), pour A_vec de shape (..., 3).

    Cette convention correspond au lien lattice U_μ(x) = exp(i a g T^a A_μ^a(x))
    avec T^a = σ^a/2 les générateurs SU(2) demi-spin (anti-hermitiens i·T^a).

    SU(2): U = cos(|A|/2) I + i sin(|A|/2) (A·σ)/|A|

    Args:
      A_vec : (..., 3) algèbre vector (3 components for a=1,2,3)

    Returns:
      U : (..., 2, 2) SU(2) matrix
    """
    a_norm = jnp.linalg.norm(A_vec, axis=-1)  # (...)
    a_norm_safe = jnp.where(a_norm < 1e-15, 1.0, a_norm)
    half = a_norm_safe / 2.0
    n = A_vec / a_norm_safe[..., None]  # (..., 3)
    # n·σ : sum_a n^a σ^a → (..., 2, 2)
    # PAULI shape (3, 2, 2), n shape (..., 3) → einsum 'amn,...a->...mn'
    n_dot_sigma = jnp.einsum('amn,...a->...mn', PAULI, n)
    cos_h = jnp.cos(half)[..., None, None]
    sin_h = jnp.sin(half)[..., None, None]
    U = cos_h * ID2 + 1j * sin_h * n_dot_sigma
    # Where |A| ≈ 0, return identity
    is_zero = (a_norm < 1e-15)[..., None, None]
    U = jnp.where(is_zero, jnp.broadcast_to(ID2, U.shape), U)
    return U


@jit
def project_su2(U):
    """Project a near-SU(2) matrix back to SU(2) by polar decomposition.

    Utile après accumulation numérique."""
    # SU(2) form U = a₀ I + i a_a σ^a, with a₀² + |a|² = 1
    U00, U01 = U[..., 0, 0], U[..., 0, 1]
    U10, U11 = U[..., 1, 0], U[..., 1, 1]
    a0 = 0.5 * jnp.real(U00 + U11)
    a1 = -0.5 * jnp.imag(U01 + U10)
    a2 = -0.5 * jnp.real(U01 - U10)
    a3 = -0.5 * jnp.imag(U00 - U11)
    norm = jnp.sqrt(a0**2 + a1**2 + a2**2 + a3**2)
    norm = jnp.where(norm < 1e-15, 1.0, norm)
    a0, a1, a2, a3 = a0/norm, a1/norm, a2/norm, a3/norm
    U_proj = jnp.zeros_like(U)
    U_proj = U_proj.at[..., 0, 0].set(a0 + 1j * a3)
    U_proj = U_proj.at[..., 0, 1].set(a2 + 1j * a1)
    U_proj = U_proj.at[..., 1, 0].set(-a2 + 1j * a1)
    U_proj = U_proj.at[..., 1, 1].set(a0 - 1j * a3)
    return U_proj


# ═══════════════════════════════════════════════════════════════════════════
# 't Hooft symbol η^a_{μν} (anti-symmetric, self-dual)
# ═══════════════════════════════════════════════════════════════════════════

def make_eta_thooft():
    """η^a_{μν} : 't Hooft symbol pour BPST self-dual instanton.

    Conventions (Belavin-Polyakov-Schwartz-Tyupkin 1975) :
      η^a_{ij} = ε^aij  for i,j = 1,2,3
      η^a_{i4} = -δ^ai
      η^a_{4i} = +δ^ai
      η^a_{44} = 0
    """
    eta = np.zeros((3, 4, 4))
    eps3 = np.zeros((3, 3, 3))
    for a in range(3):
        for i in range(3):
            for j in range(3):
                if (a, i, j) in [(0,1,2),(1,2,0),(2,0,1)]:
                    eps3[a, i, j] = 1.0
                elif (a, i, j) in [(0,2,1),(1,0,2),(2,1,0)]:
                    eps3[a, i, j] = -1.0
    for a in range(3):
        for i in range(3):
            for j in range(3):
                eta[a, i, j] = eps3[a, i, j]
            eta[a, i, 3] = -1.0 if i == a else 0.0
            eta[a, 3, i] = 1.0 if i == a else 0.0
    return jnp.array(eta, dtype=jnp.float64)


ETA_THOOFT = make_eta_thooft()  # (3, 4, 4)


# ═══════════════════════════════════════════════════════════════════════════
# BPST INSTANTON ON T⁴ (image-summed periodization)
# ═══════════════════════════════════════════════════════════════════════════

def bpst_A_continuum(x, x0, rho, g_color):
    """A_μ^a(x) BPST k=1 SU(2) sur R⁴ (sans périodisation).

    Conventions singular gauge alternative — on prend la REGULAR gauge :
      A_μ^a(x) = 2/g · η^a_{μν} (x - x₀)_ν / [(x-x₀)² + ρ²]

    g_color ∈ SU(2) est l'orientation globale, A → g·A·g†
    (au niveau algèbre : A^a T^a → A^a (g T^a g†) = R^{ab}(g) A^b T^b
     avec R^{ab}(g) ∈ SO(3) — c'est la rotation adjointe).

    Args:
      x : (..., 4) coordonnées
      x0 : (4,) centre
      rho : scalar > 0, échelle
      g_color : (2,2) SU(2) orientation

    Returns:
      A : (..., 4, 3) avec A[..., mu, a] = A_μ^a (composante algèbre)
    """
    dx = x - x0  # (..., 4)
    r2 = jnp.sum(dx ** 2, axis=-1)  # (...)
    denom = r2 + rho ** 2  # (...)
    # A_μ^a = 2 · η^a_{μν} (dx)_ν / denom (g=1 convention)
    # einsum : "amn, ...n -> ...am" on η[a,μ,ν] · dx[...,ν]
    A_am = 2.0 * jnp.einsum('amn,...n->...am', ETA_THOOFT, dx) / denom[..., None, None]
    # Now A_am has shape (..., 3, 4). Transpose to (..., 4, 3) so that
    # A[..., mu, a] = A_μ^a
    A_mu_a = jnp.swapaxes(A_am, -1, -2)

    # Apply global gauge rotation g_color : A → R(g) · A
    # R^{ab}(g) σ^b = g σ^a g†
    # We compute R via the explicit map for SU(2) → SO(3):
    #   g σ^a g† = R^{ba}(g) σ^b, so A^a → R^{ab} A^b (rotation in adjoint)
    R = su2_to_so3(g_color)  # (3, 3)
    A_rot = jnp.einsum('ab,...mb->...ma', R, A_mu_a)
    return A_rot


@jit
def su2_to_so3(g):
    """SU(2) → SO(3) map: R^{ab} = (1/2) tr(σ^a g σ^b g†).

    g shape : (2,2) → R shape : (3,3)
    Vectorisé via deux einsum.
    """
    g_dag = dag(g)
    # M^{a,..} = σ^a g  → shape (3,2,2)
    sig_g = jnp.einsum('aij,jk->aik', PAULI, g)
    # N^{b,..} = σ^b g†  → shape (3,2,2)
    sig_g_dag = jnp.einsum('bij,jk->bik', PAULI, g_dag)
    # R[a,b] = (1/2) Re tr(sig_g[a] · sig_g_dag[b])
    #        = (1/2) Re sum_{i,j} sig_g[a,i,j] · sig_g_dag[b,j,i]
    R = 0.5 * jnp.real(jnp.einsum('aij,bji->ab', sig_g, sig_g_dag))
    return R


def bpst_A_periodized(coords, x0, rho, g_color, L, n_images=2):
    """Périodise A_BPST sur T⁴ par image-summation [-n_images, n_images]^4.

    n_images=2 → 5^4 = 625 images (suffisant pour ρ << L).
    """
    A_total = jnp.zeros(coords.shape[:-1] + (4, 3), dtype=jnp.float64)
    shifts = []
    for k1 in range(-n_images, n_images + 1):
        for k2 in range(-n_images, n_images + 1):
            for k3 in range(-n_images, n_images + 1):
                for k4 in range(-n_images, n_images + 1):
                    shifts.append([k1, k2, k3, k4])
    shifts = jnp.array(shifts, dtype=jnp.float64) * L  # (N_images, 4)
    for shift in shifts:
        A_total = A_total + bpst_A_continuum(coords, x0 + shift, rho, g_color)
    return A_total


def make_lattice_coords(L):
    """Coordonnées des sites x ∈ [0, L)⁴."""
    grid = jnp.arange(L, dtype=jnp.float64)
    x1, x2, x3, x4 = jnp.meshgrid(grid, grid, grid, grid, indexing='ij')
    coords = jnp.stack([x1, x2, x3, x4], axis=-1)  # (L,L,L,L,4)
    return coords


def make_links_from_A(A_field):
    """Convertir A_μ(x) (algèbre) en liens U_μ(x) = exp(i g a A_μ T^a).

    Conventions :
      - On absorbe g a = 1 (réseau, g_lattice = 1 par défaut)
      - U_μ(x) ∈ SU(2), shape (L,L,L,L,4,2,2)
    """
    # A_field shape (L,L,L,L,4,3) — pour chaque (x,μ), un 3-vecteur
    return su2_from_alg(A_field)  # (L,L,L,L,4,2,2)


# ═══════════════════════════════════════════════════════════════════════════
# WILSON-DIRAC OPERATOR (matrix-free, fundamental rep SU(2))
# ═══════════════════════════════════════════════════════════════════════════

# Euclidean γ matrices in chiral representation (4x4 complex)
# γ^μ γ^ν + γ^ν γ^μ = 2 δ^{μν}, γ^5 = γ^1 γ^2 γ^3 γ^4
# Convention: γ^i (i=1,2,3) = ((0, -i σ^i), (i σ^i, 0)),  γ^4 = ((0, I), (I, 0))

def make_gamma_matrices():
    """4-dim chiral Euclidean γ matrices."""
    gamma = []
    for i in range(3):
        g = jnp.zeros((4, 4), dtype=jnp.complex128)
        g = g.at[0:2, 2:4].set(-1j * PAULI[i])
        g = g.at[2:4, 0:2].set(1j * PAULI[i])
        gamma.append(g)
    g4 = jnp.zeros((4, 4), dtype=jnp.complex128)
    g4 = g4.at[0:2, 2:4].set(ID2)
    g4 = g4.at[2:4, 0:2].set(ID2)
    gamma.append(g4)
    gamma5 = jnp.zeros((4, 4), dtype=jnp.complex128)
    gamma5 = gamma5.at[0:2, 0:2].set(ID2)
    gamma5 = gamma5.at[2:4, 2:4].set(-ID2)
    return jnp.stack(gamma, axis=0), gamma5


GAMMA, GAMMA5 = make_gamma_matrices()  # (4,4,4), (4,4)


# Projection operators (1 ± γ_μ)/2 used in Wilson stencil
def make_P_projectors():
    """P_μ^± = (1 ± γ_μ)/2 : 4-dim spin projectors."""
    I4 = jnp.eye(4, dtype=jnp.complex128)
    P_plus = jnp.stack([0.5 * (I4 + GAMMA[mu]) for mu in range(4)], axis=0)
    P_minus = jnp.stack([0.5 * (I4 - GAMMA[mu]) for mu in range(4)], axis=0)
    return P_plus, P_minus


P_PLUS, P_MINUS = make_P_projectors()  # (4,4,4)


def apply_wilson_dirac(psi, U, m=0.0, r=1.0):
    """Wilson-Dirac operator D applied to ψ matrix-free.

    Convention standard :
      (D ψ)(x) = (m + 4r) ψ(x)
                - (1/2) Σ_μ [ (r - γ_μ) U_μ(x) ψ(x+μ̂)
                            + (r + γ_μ) U_μ(x-μ̂)† ψ(x-μ̂) ]

    Args:
      psi : (L,L,L,L,4,2) — 4-spin, 2-color
      U   : (L,L,L,L,4,2,2) — gauge links
      m   : bare mass (typically 0 for zero modes near continuum)
      r   : Wilson parameter (typically 1)

    Returns:
      D ψ : same shape as psi
    """
    L = psi.shape[0]
    result = (m + 4 * r) * psi  # diagonal term

    for mu in range(4):
        U_mu = U[..., mu, :, :]  # (L,L,L,L,2,2)
        psi_p = jnp.roll(psi, -1, axis=mu)  # ψ(x+μ̂)
        psi_m = jnp.roll(psi, 1, axis=mu)   # ψ(x-μ̂)
        U_mu_back = jnp.roll(U_mu, 1, axis=mu)  # U_μ(x-μ̂)

        # Forward hop: (r·I - γ_μ) U_μ(x) ψ(x+μ̂)
        # spin: P_minus[mu] = (1 - γ_μ)/2, so (r - γ_μ) ≈ 2 r P_minus when r=1
        # we use the standard normalization (r=1):
        # (1 - γ_μ)/2 = P_minus[mu], so (r·I - γ_μ) ψ = 2·P_minus[mu]·ψ when r=1
        # But to keep r general:
        spin_fwd = r * psi_p - jnp.einsum('ij,...jc->...ic', GAMMA[mu], psi_p)
        # Apply U_μ(x) on color
        color_fwd = jnp.einsum('...cd,...sd->...sc', U_mu, spin_fwd)
        result = result - 0.5 * color_fwd

        # Backward hop: (r·I + γ_μ) U_μ(x-μ̂)† ψ(x-μ̂)
        spin_bwd = r * psi_m + jnp.einsum('ij,...jc->...ic', GAMMA[mu], psi_m)
        color_bwd = jnp.einsum('...cd,...sd->...sc', dag(U_mu_back), spin_bwd)
        result = result - 0.5 * color_bwd

    return result


def apply_D_dagger_D(psi, U, m=0.0, r=1.0):
    """D†D ψ — positive semi-definite, ground state = (near-)zero mode."""
    Dpsi = apply_wilson_dirac(psi, U, m, r)
    # D† has reversed sign on γ_μ in the hop terms; equivalent to using
    # the gauge-link adjoint conjugation: D†(U) = γ_5 D(U) γ_5
    # Easier: apply γ_5 D γ_5 (Hermiticity convention)
    g5_Dpsi = jnp.einsum('ij,...jc->...ic', GAMMA5, Dpsi)
    DDpsi = apply_wilson_dirac(g5_Dpsi, U, m, r)
    return jnp.einsum('ij,...jc->...ic', GAMMA5, DDpsi)


# ═══════════════════════════════════════════════════════════════════════════
# LOBPCG MATRIX-FREE FOR SMALLEST EIGENVALUES OF D†D
# ═══════════════════════════════════════════════════════════════════════════

def lobpcg_lowest_complex(apply_M_func, shape, key, n_iter=80,
                          n_eigs=4, shift=20.0, X_init=None):
    """LOBPCG matrix-free pour eigvalues les plus petites de M (positif).

    Adapté de KR-FP-3 mais en complex128 et pour blocs ψ ∈ ℂ^{shape}.
    On utilise la transformation shift·I - M dont les plus grandes
    eigenvalues correspondent aux plus petites de M.

    Args:
      apply_M_func : ψ → M ψ, complex128, shape preserved
      shape : tuple, e.g. (L,L,L,L,4,2)
      key : jax PRNGKey
      n_iter : nombre d'itérations LOBPCG (fixe pour JIT)
      n_eigs : nombre de modes propres demandés
      shift : valeur de shift (doit dominer le spectre de M)
      X_init : optionnel, vecteurs initiaux (shape + (n_eigs,)) pour warm start
               (essentiel pour tracking adiabatique de la phase de Berry)

    Returns:
      eigvals : (n_eigs,) plus petites valeurs propres de M
      eigvecs : (..., n_eigs) modes propres orthonormaux
    """
    n_total = int(np.prod(shape))

    def matvec_shifted(psi):
        return shift * psi - apply_M_func(psi)

    def matvec_block(X_block):
        # X_block shape : shape + (n_eigs,)
        return vmap(matvec_shifted, in_axes=-1, out_axes=-1)(X_block)

    # Initial orthonormal block: warm-start if X_init provided
    if X_init is not None:
        X = X_init.astype(jnp.complex128)
    else:
        keyR, keyI = jax.random.split(key)
        X_r = jax.random.normal(keyR, shape + (n_eigs,), dtype=jnp.float64)
        X_i = jax.random.normal(keyI, shape + (n_eigs,), dtype=jnp.float64)
        X = (X_r + 1j * X_i).astype(jnp.complex128)
    X_flat = X.reshape(n_total, n_eigs)
    Q, _ = jnp.linalg.qr(X_flat)
    X = Q.reshape(shape + (n_eigs,))
    P = jnp.zeros_like(X)

    def lobpcg_iter(carry, _):
        X, P = carry
        AX = matvec_block(X)
        # Rayleigh quotients (real, since operator is Hermitian)
        # rq[k] = <X_k, AX_k> = sum_{spatial,spin,color} conj(X) * AX, over k = last axis
        rq = jnp.real(jnp.sum(jnp.conj(X) * AX, axis=tuple(range(len(shape)))))
        # residual[..., k] = AX[..., k] - rq[k] * X[..., k]
        residual = AX - rq * X

        basis = jnp.concatenate([
            X.reshape(n_total, n_eigs),
            residual.reshape(n_total, n_eigs),
            P.reshape(n_total, n_eigs),
        ], axis=-1)
        Q, _ = jnp.linalg.qr(basis)
        nz = Q.shape[1]
        Q_block = Q.reshape(shape + (nz,))
        AQ = matvec_block(Q_block)
        # Build small Hermitian matrix H = Q† A Q
        # H_ij = sum_x conj(Q[...,i]) * AQ[...,j]
        Q_flat = Q
        AQ_flat = AQ.reshape(n_total, nz)
        H = jnp.einsum('xi,xj->ij', jnp.conj(Q_flat), AQ_flat)
        H = 0.5 * (H + dag(H))
        sub_vals, sub_vecs = jnp.linalg.eigh(H)
        # We want largest (since shifted operator); sort descending
        idx = jnp.argsort(-sub_vals)
        sub_vals_top = sub_vals[idx][:n_eigs]
        sub_vecs_top = sub_vecs[:, idx][:, :n_eigs]

        X_new = (Q_flat @ sub_vecs_top).reshape(shape + (n_eigs,))
        P_new = X_new - X
        return (X_new, P_new), sub_vals_top

    (X_final, _), eigvals_history = lax.scan(
        lobpcg_iter, (X, P), jnp.arange(n_iter)
    )
    eigvals_shifted = eigvals_history[-1]
    eigvals_M = shift - eigvals_shifted
    sort = jnp.argsort(eigvals_M)
    eigvals_sorted = eigvals_M[sort]
    eigvecs_sorted = X_final[..., sort]
    return eigvals_sorted, eigvecs_sorted


# ═══════════════════════════════════════════════════════════════════════════
# COMPUTE ZERO MODE FOR ONE BACKGROUND
# ═══════════════════════════════════════════════════════════════════════════

def compute_zero_mode(U, key, m=-3.95, n_iter=120, n_eigs=2, shift=40.0,
                      X_init=None):
    """Calcule le near-zero mode de D†D dans le fond U.

    Args:
      U : (L,L,L,L,4,2,2) liens
      key : PRNGKey
      m : Wilson bare mass (proche critique -4 pour isoler le mode zéro)
      n_iter : itérations LOBPCG
      n_eigs : combien de modes (1 zéro-mode + quelques pour stabilité)
      shift : pour smallest-eigenvalue trick
      X_init : optionnel, ψ_init du pas précédent (warm-start essentiel
               pour tracking adiabatique de la phase)

    Returns:
      eigvals : (n_eigs,) plus petites eigvalues de D†D (toutes ≥ 0)
      eigvecs : (L,L,L,L,4,2,n_eigs) tous les modes (orthonormaux)
    """
    shape = U.shape[:-3] + (4, 2)  # (L,L,L,L,4,2)

    def apply_M(psi):
        return apply_D_dagger_D(psi, U, m=m, r=1.0)

    eigvals, eigvecs = lobpcg_lowest_complex(
        apply_M, shape, key, n_iter=n_iter, n_eigs=n_eigs, shift=shift,
        X_init=X_init,
    )
    return eigvals, eigvecs


# ═══════════════════════════════════════════════════════════════════════════
# OVERLAP & BERRY PHASE
# ═══════════════════════════════════════════════════════════════════════════

def overlap(psi_a, psi_b):
    """⟨ψ_a | ψ_b⟩ complex inner product."""
    return jnp.sum(jnp.conj(psi_a) * psi_b)


def berry_phase_from_overlaps(overlaps):
    """θ_Berry = arg Π_n ⟨ψ_n | ψ_{n+1}⟩.

    Args:
      overlaps : list/array of complex numbers
    Returns:
      θ ∈ (-π, π]
    """
    log_prod = sum(np.log(complex(o)) for o in overlaps)
    return float(np.imag(log_prod))


# ═══════════════════════════════════════════════════════════════════════════
# MODULI SPACE LOOPS
# ═══════════════════════════════════════════════════════════════════════════

def loop_gauge_cartan(t, t_end=2 * np.pi):
    """Rotation autour σ³ Cartan : g(t) = exp(i t σ³ / 2).

    t ∈ [0, t_end], t_end = 2π → boucle non-contractible dans SO(3) = SU(2)/Z_2
    """
    half = t / 2.0
    g = jnp.array([
        [jnp.exp(1j * half), 0.0],
        [0.0, jnp.exp(-1j * half)],
    ], dtype=jnp.complex128)
    return g


def loop_translation(t, t_end=None, L=8, mu=0):
    """Translation in T¹ direction μ : p(t) = (t·L̂_μ, ...). Boucle entière."""
    if t_end is None:
        t_end = float(L)
    x0 = jnp.zeros(4, dtype=jnp.float64)
    x0 = x0.at[mu].set(t)
    return x0


# ═══════════════════════════════════════════════════════════════════════════
# MAIN MEASUREMENT
# ═══════════════════════════════════════════════════════════════════════════

def build_instanton_links(L, x0, rho, g_color, n_images=2):
    """Construct gauge links U from BPST instanton parameters."""
    coords = make_lattice_coords(L)
    # Center coords on (x_mu + 0.5) for link midpoints
    # For simplicity, evaluate A_μ at site x (forward link), absorb into U.
    A_field = bpst_A_periodized(coords, x0, rho, g_color, L, n_images=n_images)
    # Cap large A values for numerical stability (BPST singular at x=x0)
    A_norm = jnp.linalg.norm(A_field, axis=-1, keepdims=True)
    cap = jnp.pi  # max |A|/2 = π/2 → U = -I (max rotation)
    factor = jnp.where(A_norm > cap, cap / jnp.maximum(A_norm, 1e-15), 1.0)
    A_field = A_field * factor
    U = make_links_from_A(A_field)
    U = project_su2(U)
    return U, A_field


def measure_berry_loop(loop_type, N_steps, L, rho, x0_base, n_images, key_lobpcg,
                       m_wilson=-3.95, n_lobpcg_iter=120, n_eigs=2,
                       lobpcg_shift=40.0, verbose=True):
    """Mesure la phase de Berry le long d'une boucle.

    Args:
      loop_type : 'identity' | 'cartan_2pi' | 'cartan_4pi' | 'translation_x'
      N_steps : nombre de points sur la boucle (≥ 8)
      L : lattice size
      rho : taille instanton
      x0_base : position centre instanton (4,)
      n_images : 2 → 5⁴ images pour image-sum BPST
      key_lobpcg : PRNGKey pour init LOBPCG
      m_wilson : masse nue Wilson (typiquement -0.1 pour critique)
      n_lobpcg_iter : itérations LOBPCG (fixe JIT)
      n_eigs : nombre modes propres dans LOBPCG
      lobpcg_shift : shift LOBPCG (doit dominer spectre D†D)
      verbose : log intermédiaire

    Returns:
      dict avec eigvals_history, overlaps, berry_phase, ...
    """
    print(f"\n--- Berry measurement: loop={loop_type}, N_steps={N_steps}, L={L}, ρ={rho} ---",
          flush=True)

    # Build the discretized loop parameters
    if loop_type == 'identity':
        g_list = [jnp.eye(2, dtype=jnp.complex128) for _ in range(N_steps + 1)]
        x0_list = [x0_base for _ in range(N_steps + 1)]
    elif loop_type == 'cartan_2pi':
        ts = np.linspace(0.0, 2 * np.pi, N_steps + 1)
        g_list = [loop_gauge_cartan(float(t)) for t in ts]
        x0_list = [x0_base for _ in range(N_steps + 1)]
    elif loop_type == 'cartan_4pi':
        ts = np.linspace(0.0, 4 * np.pi, N_steps + 1)
        g_list = [loop_gauge_cartan(float(t)) for t in ts]
        x0_list = [x0_base for _ in range(N_steps + 1)]
    elif loop_type == 'translation_x':
        ts = np.linspace(0.0, float(L), N_steps + 1)
        g_list = [jnp.eye(2, dtype=jnp.complex128) for _ in range(N_steps + 1)]
        x0_list = []
        for t in ts:
            x0_t = np.array(x0_base, dtype=np.float64).copy()
            x0_t[0] += float(t)
            x0_list.append(jnp.array(x0_t, dtype=jnp.float64))
    else:
        raise ValueError(f"Unknown loop_type: {loop_type}")

    # Iterate along the loop, computing zero mode and overlaps
    # KEY POINT: we WARM-START LOBPCG with previous step's eigenvectors.
    # This ensures the eigenvector phase varies adiabatically (essential
    # for the Berry phase) instead of being random at each step.
    overlaps = []
    psi_prev = None
    psi0_first = None
    eigvecs_prev = None
    eigvals_history = []
    key = key_lobpcg

    t_start = time.time()
    for n in range(N_steps + 1):
        g_n = g_list[n]
        x0_n = x0_list[n]
        U_n, _ = build_instanton_links(L, x0_n, rho, g_n, n_images=n_images)

        key, subkey = jax.random.split(key)
        # First step: random init with many iter. Subsequent: warm-start.
        if eigvecs_prev is None:
            n_iter_step = max(n_lobpcg_iter * 2, 300)  # extra iter on first call
            X_init = None
        else:
            n_iter_step = n_lobpcg_iter
            X_init = eigvecs_prev

        eigvals, eigvecs = compute_zero_mode(
            U_n, subkey, m=m_wilson, n_iter=n_iter_step,
            n_eigs=n_eigs, shift=lobpcg_shift, X_init=X_init,
        )
        eigvals_np = np.asarray(eigvals)
        eigvals_history.append(eigvals_np.tolist())

        # Take ground state (smallest eigenvalue)
        psi_n = eigvecs[..., 0]
        norm_n = jnp.sqrt(jnp.real(jnp.sum(jnp.conj(psi_n) * psi_n)))
        psi_n = psi_n / norm_n

        # CRITICAL: align gauge of ψ_n with ψ_prev to avoid spurious phase
        # jumps from random LOBPCG init. The Berry phase is the residual
        # phase AFTER this alignment.
        # Strategy: do NOT remove the overlap phase (that's the Berry phase!),
        # but keep eigvecs_prev for warm-start.
        eigvecs_prev = eigvecs

        if psi_prev is not None:
            ov = complex(overlap(psi_prev, psi_n))
            overlaps.append(ov)
            if verbose and (n % max(1, N_steps // 8) == 0 or n == N_steps):
                print(
                    f"  step {n}/{N_steps}: λ_min(D†D)={eigvals_np[0]:.6f}, "
                    f"|⟨ψ_{n-1}|ψ_{n}⟩|={abs(ov):.4f}, "
                    f"arg={np.angle(ov):+.4f}",
                    flush=True,
                )
        else:
            psi0_first = psi_n
            if verbose:
                print(
                    f"  step 0/{N_steps}: λ_min(D†D)={eigvals_np[0]:.6f}",
                    flush=True,
                )
        psi_prev = psi_n

    # Note: for a true closed loop, the last state ψ_N should equal ψ_0
    # up to a gauge phase. We include the closure overlap ⟨ψ_N | ψ_0⟩.
    closure = complex(overlap(psi_prev, psi0_first))
    overlaps.append(closure)
    if verbose:
        print(f"  closure ⟨ψ_N|ψ_0⟩ = {closure:.4f}, "
              f"|.|={abs(closure):.4f}, arg={np.angle(closure):+.4f}",
              flush=True)

    elapsed = time.time() - t_start

    # Compute Berry phase
    theta = berry_phase_from_overlaps(overlaps)
    # Wrap to (-π, π]
    theta_wrapped = ((theta + np.pi) % (2 * np.pi)) - np.pi

    print(f"  ─── θ_Berry = {theta:.6f} rad  (mod 2π → {theta_wrapped:+.6f})  "
          f"= {theta_wrapped/np.pi:+.4f} π",
          flush=True)
    print(f"  elapsed: {elapsed:.1f}s ({elapsed/(N_steps+1):.2f}s/step)",
          flush=True)

    return {
        'loop_type': loop_type,
        'N_steps': N_steps,
        'L': L,
        'rho': float(rho),
        'x0': [float(v) for v in np.asarray(x0_base)],
        'eigvals_history': eigvals_history,
        'overlaps_re': [o.real for o in overlaps],
        'overlaps_im': [o.imag for o in overlaps],
        'overlap_abs': [abs(o) for o in overlaps],
        'overlap_arg': [float(np.angle(o)) for o in overlaps],
        'theta_berry_raw': float(theta),
        'theta_berry_wrapped': float(theta_wrapped),
        'theta_berry_over_pi': float(theta_wrapped / np.pi),
        'elapsed_s': float(elapsed),
    }


# ═══════════════════════════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    # ── Configuration pilote ─────────────────────────────────────────────────
    L = 8                  # lattice size (8⁴ = 4096 sites — fast pilot)
    rho = 1.5              # BPST scale (in lattice units a=1)
    x0_base = jnp.array([L/2.0, L/2.0, L/2.0, L/2.0], dtype=jnp.float64)
    N_STEPS = 24           # discretization of the loop
    N_IMAGES = 2           # 5⁴ image-sum for periodization
    # Wilson mass: critical at tree-level is m + 4r = 0 → m = -4 for r = 1.
    # Slightly above critical (m = -3.95) keeps the would-be zero mode at small
    # positive value, isolated from the rest of the spectrum.
    M_WILSON = -3.95
    N_LOBPCG_ITER = 150    # LOBPCG iterations (more for low-mode convergence)
    N_EIGS = 2             # number of eigenpairs to compute
    LOBPCG_SHIFT = 40.0    # shift for "smallest eigenvalue" trick
    SEED = 2026

    key = jax.random.PRNGKey(SEED)

    print(f"\nConfig pilote SU(2) k=1 Berry phase:", flush=True)
    print(f"  L = {L}, rho = {rho}, x0 = {x0_base}", flush=True)
    print(f"  N_steps = {N_STEPS}, N_images = {N_IMAGES} → {(2*N_IMAGES+1)**4} copies",
          flush=True)
    print(f"  Wilson m = {M_WILSON}, LOBPCG: n_iter={N_LOBPCG_ITER}, "
          f"n_eigs={N_EIGS}, shift={LOBPCG_SHIFT}",
          flush=True)

    all_results = {}

    # ── Test T1 : Boucle triviale (sanity check) ─────────────────────────────
    print(f"\n{'='*78}", flush=True)
    print(f"T1 : Boucle triviale (identité × N_steps) → attendu θ ≈ 0", flush=True)
    print(f"{'='*78}", flush=True)
    try:
        key, sub = jax.random.split(key)
        r1 = measure_berry_loop(
            'identity', N_STEPS, L, rho, x0_base, N_IMAGES, sub,
            m_wilson=M_WILSON, n_lobpcg_iter=N_LOBPCG_ITER,
            n_eigs=N_EIGS, lobpcg_shift=LOBPCG_SHIFT,
        )
        all_results['T1_identity'] = r1
    except Exception as ex:
        print(f"T1 ERROR : {ex}", flush=True)
        import traceback; traceback.print_exc()
        all_results['T1_identity'] = {'error': str(ex)}

    # ── Test T2 : Boucle Cartan 2π — TEST PRINCIPAL ──────────────────────────
    print(f"\n{'='*78}", flush=True)
    print(f"T2 : Boucle Cartan α ∈ [0, 2π] → ATTENDU θ_Berry = ±π (WZW level 1)",
          flush=True)
    print(f"{'='*78}", flush=True)
    try:
        key, sub = jax.random.split(key)
        r2 = measure_berry_loop(
            'cartan_2pi', N_STEPS, L, rho, x0_base, N_IMAGES, sub,
            m_wilson=M_WILSON, n_lobpcg_iter=N_LOBPCG_ITER,
            n_eigs=N_EIGS, lobpcg_shift=LOBPCG_SHIFT,
        )
        all_results['T2_cartan_2pi'] = r2
    except Exception as ex:
        print(f"T2 ERROR : {ex}", flush=True)
        import traceback; traceback.print_exc()
        all_results['T2_cartan_2pi'] = {'error': str(ex)}

    # ── Test T3 : Boucle Cartan 4π (deux tours) → attendu 0 mod 2π ───────────
    print(f"\n{'='*78}", flush=True)
    print(f"T3 : Boucle Cartan α ∈ [0, 4π] (2 tours) → ATTENDU θ ≈ 0 mod 2π",
          flush=True)
    print(f"{'='*78}", flush=True)
    try:
        key, sub = jax.random.split(key)
        r3 = measure_berry_loop(
            'cartan_4pi', N_STEPS, L, rho, x0_base, N_IMAGES, sub,
            m_wilson=M_WILSON, n_lobpcg_iter=N_LOBPCG_ITER,
            n_eigs=N_EIGS, lobpcg_shift=LOBPCG_SHIFT,
        )
        all_results['T3_cartan_4pi'] = r3
    except Exception as ex:
        print(f"T3 ERROR : {ex}", flush=True)
        import traceback; traceback.print_exc()
        all_results['T3_cartan_4pi'] = {'error': str(ex)}

    # ── Test T4 : Boucle translation (optionnel) ─────────────────────────────
    print(f"\n{'='*78}", flush=True)
    print(f"T4 : Boucle translation x → x+L̂₁·L  → attendu θ ≈ 0 (SU(2) k=1)",
          flush=True)
    print(f"{'='*78}", flush=True)
    try:
        key, sub = jax.random.split(key)
        r4 = measure_berry_loop(
            'translation_x', N_STEPS, L, rho, x0_base, N_IMAGES, sub,
            m_wilson=M_WILSON, n_lobpcg_iter=N_LOBPCG_ITER,
            n_eigs=N_EIGS, lobpcg_shift=LOBPCG_SHIFT,
        )
        all_results['T4_translation_x'] = r4
    except Exception as ex:
        print(f"T4 ERROR : {ex}", flush=True)
        import traceback; traceback.print_exc()
        all_results['T4_translation_x'] = {'error': str(ex)}

    # ── Summary ──────────────────────────────────────────────────────────────
    print(f"\n{'='*78}", flush=True)
    print(f"SUMMARY KR-CP-BERRY-1", flush=True)
    print(f"{'='*78}", flush=True)
    print(f"{'Test':<20} {'θ_Berry/π':>14} {'expected':>12} {'verdict':>12}",
          flush=True)
    print("-" * 78, flush=True)
    expectations = {
        'T1_identity': (0.0, 0.2),
        'T2_cartan_2pi': (1.0, 0.3),  # |θ - π| < 0.3·π acceptable for pilot
        'T3_cartan_4pi': (0.0, 0.3),
        'T4_translation_x': (0.0, 0.3),
    }
    verdicts = {}
    for key_t, r in all_results.items():
        if 'error' in r:
            print(f"{key_t:<20} {'ERROR':>14} {'-':>12} {'FAIL':>12}", flush=True)
            verdicts[key_t] = 'ERROR'
            continue
        theta_pi = r['theta_berry_over_pi']
        exp_val, tol = expectations.get(key_t, (None, None))
        if exp_val is None:
            verdict = '?'
        elif abs(theta_pi - exp_val) < tol or abs(abs(theta_pi) - exp_val) < tol:
            verdict = 'OK'
        else:
            verdict = 'OFF'
        verdicts[key_t] = verdict
        exp_str = f"{exp_val:+.2f}" if exp_val is not None else "-"
        print(f"{key_t:<20} {theta_pi:>+14.4f} {exp_str:>12} {verdict:>12}",
              flush=True)
    print("-" * 78, flush=True)

    # Honest disclaimer
    print(f"\nNB : la cohérence de θ_Berry dépend de :", flush=True)
    print(f"  (a) ρ << L (instanton bien localisé, ici ρ/L = {rho/L:.2f})",
          flush=True)
    print(f"  (b) M_WILSON proche du critique (le mode-zéro doit être isolé)",
          flush=True)
    print(f"  (c) N_STEPS assez grand pour le tracking adiabatique",
          flush=True)
    print(f"  (d) overlap |⟨ψ_n|ψ_{{n+1}}⟩| ~ 1 (sinon adiabaticité brisée)",
          flush=True)
    print(f"Si T2 donne θ ≈ ±π avec |overlaps| > 0.95, succès pilote.",
          flush=True)

    summary = {
        'config': {
            'L': L, 'rho': float(rho), 'N_steps': N_STEPS, 'N_images': N_IMAGES,
            'M_wilson': M_WILSON, 'N_lobpcg_iter': N_LOBPCG_ITER,
            'N_eigs': N_EIGS, 'lobpcg_shift': LOBPCG_SHIFT, 'seed': SEED,
        },
        'results': all_results,
        'verdicts': verdicts,
        'total_elapsed_s': time.time() - START,
    }
    out_path = "/tmp/kr_cp_berry_jax_gpu_results.json"
    with open(out_path, 'w') as f:
        json.dump(summary, f, indent=2, default=lambda x: float(x) if hasattr(x, '__float__') else str(x))

    print(f"\nTotal elapsed : {time.time()-START:.1f}s ({(time.time()-START)/60:.1f}min)",
          flush=True)
    print(f"Saved : {out_path}", flush=True)
    print(f"END : {time.ctime()}", flush=True)
    print(f"DONE.", flush=True)
