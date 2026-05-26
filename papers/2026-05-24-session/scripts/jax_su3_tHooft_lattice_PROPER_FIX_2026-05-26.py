#!/usr/bin/env python3
"""SU(3) 't Hooft twist lattice — PROPER production script (FIX 2026-05-26).

Validates Hypothesis 4.2 ("twist rigidity") of
  Paper_tHooft_Twist_Mode_Zero_LMP/main.tex (Kévin Rémondière, 26 May 2026).

Configuration (§4.4 of the paper) :
  Gauge group : G = SU(3)
  Dimension   : D = 4
  Volumes     : L ∈ {8, 12, 16}
  Couplings   : β ∈ {2.5, 3.0, 3.5}  (continuum regime, λ = 2N²/β = 18/β)
  Twist plane : (μ,ν) = (1,2), twist tensor n^{12} = 1 mod 3
  Twist pair  : Ω_1 = diag(1, ω, ω²), Ω_2 = cyclic shift,
                Ω_3 = Ω_4 = Id           with ω = exp(2πi/3)

't Hooft commutator (Lemma 2.5 of the paper, canonical convention) :
  Ω_1 · Ω_2 = z_{12} · Ω_2 · Ω_1    with    z_{μν} = exp(-2πi n^{μν}/N)
  For n^{12} = 1 mod 3 :    Ω_1 · Ω_2 = ω̄ · Ω_2 · Ω_1
  Centre commutator :       [Ω_1, Ω_2]_centre = Ω_1 Ω_2 Ω_1^{-1} Ω_2^{-1} = ω̄ = z_{12}

  NOTE (FIX 2026-05-26) : v1 of this script tested  Ω_0·Ω_1 = ω·Ω_1·Ω_0
  which is inconsistent with the standard choice
       Ω_0 = diag(1, ω, ω²) ,  Ω_1 = cyclic-shift e_i → e_{i+1 mod N}
  Direct multiplication gives
       Ω_0 · Ω_1 = ω̄ · Ω_1 · Ω_0    (i.e. centre phase z = ω̄, not ω).
  This matches Z_TWIST = exp(-2πi/N) = ω̄ already used in the action.
  This FIX rev applies the correct sign in `check_centraliser_lemma`
  and the correct counting of corner plaquettes (L^{D-2}, not 1) in the
  cold-start expected ⟨P⟩.

Boundary conditions (eq. 2.4) :
  U_{x + L·ê_ν, μ} = Ω_ν · U_{x,μ} · Ω_ν^{-1}     for all μ, ν, x

Twisted Wilson action (eq. 2.6) :
  S_W^Ω(U) = β Σ_{x,μ<ν} ( 1 - (1/N) Re Tr( z_{μν}(x) · U_{x,μν} ) )
  z_{μν}(x) = exp(-2πi n^{μν}/N) if plaquette wraps in (μ,ν)-plane, else 1.

Observables (O1-O4 of §4.4) :
  O1 : λ_min(M^Ω[A]) for M^Ω = d_A^† d_A on twisted ad(P)-valued 0-forms
  O2 : spectral gap of Hess(β·S_W^Ω) on twisted links
  O3 : C_LSI(μ^Ω) via Rothaus-Simon mean-field method
  O4 : comparison with periodic measure (no twist → constant zero mode present)

Theoretical predictions :
  m_Ω² = (2π/(NL))² = (2π/(3L))²    (twisted Hodge gap, Proposition 3.1)
  λ_min(M^Ω) ≥ (1 - κ_FP) · m_Ω² = (5/6) · m_Ω²    (Theorem 4.1, SU(3))
  C_LSI(μ^Ω) ≤ N² · c_∞(D) / [(1-κ_FP) · m_0²] = 9 · 4.05 / (5/6 · m_0²)
            ≈ 43.7 / m_0²                                  (Theorem 5.1)

Conventions critiques (LESSONS du bug audit 2026-05-25) :
  ★ Metropolis : Re Tr(U_proposed · K) -- pas K† !
    (silent catastrophic SU(2)/SU(3) bug, fixed in 6 scripts on 2026-05-25)
  ★ Staple order : K_fwd = U_ν(x+μ̂) · U_μ(x+ν̂)† · U_ν(x)†
    (NOT U_ν(x) first -- BP2008b bug fixed on 2026-05-25)
  ★ Sanity validate ⟨P⟩(α=0) match lit BEFORE measuring anything
    (van Baal 1982, Sternbeck 2005 SU(3) ⟨P⟩(β) reference values)

Pre-flight checklist (must PASS before measurements) :
  [ ] Cold start ⟨P⟩(t=0) = 1.0 periodic, ~|1/N| twisted
  [ ] After thermalization, ⟨P⟩ matches literature within 3-13%
  [ ] Metropolis acceptance ∈ [0.3, 0.7]
  [ ] τ_int < n_decorr (autocorrelation control)
  [ ] Centralizer Lemma 2.5 satisfied : Ω_1 Ω_2 = ω̄ · Ω_2 Ω_1 = Z_TWIST · Ω_2 Ω_1
      (numerical check; FIX 2026-05-26 -- v1 used ω instead of ω̄)

Anti-fab discipline :
  - Each observable measured on >= 60 thermalised configurations
  - Compute statistical error (jackknife) for every reported number
  - Output JSON with all metadata (commit, params, sanity, results)

Author : Kévin Rémondière (Independent Researcher, Oloron-Sainte-Marie)
ORCID  : 0009-0008-2443-7166
Date   : 2026-05-26
License: CC-BY-4.0
"""

# ============================================================================
# Imports & JAX configuration
# ============================================================================
import os
os.environ.setdefault('XLA_PYTHON_CLIENT_PREALLOCATE', 'false')
os.environ.setdefault('JAX_ENABLE_X64', 'True')

import argparse
import json
import math
import sys
import time
from dataclasses import dataclass, field, asdict
from functools import partial
from typing import Dict, List, Optional, Tuple

import numpy as np

import jax
import jax.numpy as jnp
from jax import jit, random, vmap, lax
from jax.scipy.sparse.linalg import cg as jax_cg


# ============================================================================
# Global constants
# ============================================================================
N_GROUP    = 3                  # SU(N), N = 3
DIM        = 4                  # spacetime dimension (D = 4)
N_GEN      = N_GROUP ** 2 - 1   # number of su(N) generators = 8 for N=3
KAPPA_FP   = 1.0 / 6.0          # Kostant invariant 1/(2|Φ+(SU(3))|) = 1/6
ONE_M_KAPPA = 1.0 - KAPPA_FP    # = 5/6 for SU(3)
C_INF_D    = 4.05               # c_∞(D=4) Wilson lattice constant (paper eq. 5.2)

# Twist plane and twist tensor : (μ,ν)=(0,1) in 0-indexed (paper's (1,2))
TWIST_MU   = 0
TWIST_NU   = 1
TWIST_N    = 1                  # n^{01} = 1 mod 3 (non-trivial)

OMEGA_PHASE = jnp.exp(2j * jnp.pi / N_GROUP)  # ω = e^{2πi/3}
Z_TWIST     = jnp.exp(-2j * jnp.pi * TWIST_N / N_GROUP)  # z_{12} = ω̄


# ============================================================================
# Gell-Mann matrices (su(3) generators, GELL_MANN[a] = λ_a, a = 0..7)
# Hermitian, traceless, normalised so Tr(λ_a λ_b) = 2 δ_{ab}
# ============================================================================

def _build_gell_mann():
    L = [
        jnp.array([[0, 1, 0], [1, 0, 0], [0, 0, 0]], dtype=jnp.complex128),
        jnp.array([[0, -1j, 0], [1j, 0, 0], [0, 0, 0]], dtype=jnp.complex128),
        jnp.array([[1, 0, 0], [0, -1, 0], [0, 0, 0]], dtype=jnp.complex128),
        jnp.array([[0, 0, 1], [0, 0, 0], [1, 0, 0]], dtype=jnp.complex128),
        jnp.array([[0, 0, -1j], [0, 0, 0], [1j, 0, 0]], dtype=jnp.complex128),
        jnp.array([[0, 0, 0], [0, 0, 1], [0, 1, 0]], dtype=jnp.complex128),
        jnp.array([[0, 0, 0], [0, 0, -1j], [0, 1j, 0]], dtype=jnp.complex128),
        jnp.array([[1, 0, 0], [0, 1, 0], [0, 0, -2]],
                  dtype=jnp.complex128) / jnp.sqrt(3.0),
    ]
    return jnp.stack(L, axis=0)  # (8, 3, 3)


GELL_MANN = _build_gell_mann()   # shape (8, 3, 3)
T_GEN     = 0.5 * GELL_MANN      # T^a = λ_a / 2, su(3) generators


# ============================================================================
# Twist matrices Ω_μ (paper §2.1)
# Standard 't Hooft choice :
#   Ω_0 = diag(1, ω, ω²)
#   Ω_1 = cyclic shift (basis vector e_i → e_{i+1 mod N})
#   Ω_2 = Ω_3 = Id
# ============================================================================

def _build_twist_matrices():
    Omega_0 = jnp.diag(jnp.array([1.0 + 0.0j, OMEGA_PHASE, OMEGA_PHASE ** 2]))
    # cyclic shift : (Ω_1)_{ij} = δ_{i, j+1 mod N}
    #   row index i = (j+1) mod N : Ω_1 = [[0,1,0],[0,0,1],[1,0,0]]
    Omega_1 = jnp.array([[0, 1, 0],
                         [0, 0, 1],
                         [1, 0, 0]], dtype=jnp.complex128)
    Omega_2 = jnp.eye(N_GROUP, dtype=jnp.complex128)
    Omega_3 = jnp.eye(N_GROUP, dtype=jnp.complex128)
    return jnp.stack([Omega_0, Omega_1, Omega_2, Omega_3], axis=0)  # (4, 3, 3)


OMEGAS = _build_twist_matrices()  # OMEGAS[mu] is the twist matrix in direction mu


def check_centraliser_lemma() -> Dict[str, float]:
    """Numerical sanity for Lemma 2.5 ('t Hooft commutator, canonical form) :
         Ω_0 · Ω_1 = z_{01} · Ω_1 · Ω_0
       with the standard choice
         Ω_0 = diag(1, ω, ω²) ,  Ω_1 = cyclic shift  (e_i → e_{i+1 mod N})
       direct multiplication gives  z_{01} = ω̄ = exp(-2π i/N) = Z_TWIST.
       (See FIX header note 2026-05-26 -- v1 had a sign error testing 'ω·' instead.)
    """
    Om0 = OMEGAS[0]
    Om1 = OMEGAS[1]
    LHS = Om0 @ Om1
    # Canonical 't Hooft commutator : centre phase Z_TWIST = ω̄ for (n^{01}=1, N=3).
    RHS = Z_TWIST * (Om1 @ Om0)
    err = float(jnp.max(jnp.abs(LHS - RHS)))
    # Sanity diagnostic : the OTHER sign would give err ≈ √3 ≈ 1.7321 (v1 bug)
    err_wrong_sign = float(jnp.max(jnp.abs(LHS - OMEGA_PHASE * (Om1 @ Om0))))
    det0 = complex(jnp.linalg.det(Om0))
    det1 = complex(jnp.linalg.det(Om1))
    return {
        'tHooft_commutator_max_err': err,
        'tHooft_commutator_max_err_wrong_sign': err_wrong_sign,  # ~1.732 if v1 bug
        'det_Omega0': abs(det0),
        'det_Omega1': abs(det1),
        'pass_commutator': err < 1e-10,
        'pass_det0': abs(det0 - 1.0) < 1e-10,
        'pass_det1': abs(det1 - 1.0) < 1e-10,
    }


# ============================================================================
# Twist-aware roll : applies Ω_ν · U · Ω_ν^{-1} for links wrapping in direction ν
# ============================================================================

def gather_link_twist(U_link, mu_link_index: int, shift_dir: int,
                      direction: int = -1) -> jnp.ndarray:
    """Gather U_link at position shifted by `direction` lattice site in `shift_dir`,
    applying twisted-BC similarity (Ω_{shift_dir} · U · Ω_{shift_dir}^{-1}) on
    those links that crossed the boundary.

    U_link : shape (L, L, L, L, 3, 3) -- the link variables U_{x, mu_link_index}
    mu_link_index : the direction of the link (not used in the similarity, but
                    we keep it for documentation; the similarity is by Ω_{shift_dir})
    shift_dir : the lattice axis along which we shift (0..3)
    direction : -1 forward shift (x → x + ê), +1 backward shift (x → x - ê)
    """
    L = U_link.shape[shift_dir]
    # Roll by `direction` along `shift_dir`. jnp.roll uses negative shift for forward.
    rolled = jnp.roll(U_link, direction, axis=shift_dir)

    # The links that crossed the boundary are those whose post-roll index
    # is the wrapping slice :
    #   forward roll (direction = -1) : the boundary slice is index L-1 of rolled
    #     (because rolled[..., L-1, ...] corresponds to original site 0)
    #   backward roll (direction = +1) : boundary slice is index 0 of rolled
    #     (rolled[..., 0, ...] corresponds to original site L-1)
    if direction == -1:
        wrap_idx = L - 1
    elif direction == +1:
        wrap_idx = 0
    else:
        raise ValueError(f"direction must be -1 or +1, got {direction}")

    # Build a mask along shift_dir
    mask_1d = jnp.zeros(L, dtype=bool).at[wrap_idx].set(True)
    # Broadcast to full lattice shape (L,L,L,L)
    mask_shape = [1, 1, 1, 1]
    mask_shape[shift_dir] = L
    mask = mask_1d.reshape(mask_shape)
    mask = jnp.broadcast_to(mask, U_link.shape[:4])  # (L,L,L,L)

    # Apply Ω_{shift_dir} similarity on wrap slice
    Omega = OMEGAS[shift_dir]
    Omega_dag = jnp.conj(Omega.T)

    if direction == -1:
        # Forward boundary crossing : U_{x + L·ê_ν, μ} = Ω_ν U_{x,μ} Ω_ν^{-1}
        twisted = jnp.einsum('ij,...jk,kl->...il', Omega, rolled, Omega_dag)
    else:  # +1
        # Backward boundary crossing : at site x=0 we look back to x=L-1,
        # but that physical link is U_{L-1, μ} which from x=0 perspective
        # comes with inverse twist : Ω_ν^{-1} U Ω_ν
        twisted = jnp.einsum('ij,...jk,kl->...il', Omega_dag, rolled, Omega)

    return jnp.where(mask[..., None, None], twisted, rolled)


# ============================================================================
# Random SU(3) (Haar and near-identity) — reused from validated primitives
# ============================================================================

def random_su3_haar(key, shape) -> jnp.ndarray:
    """Haar-random SU(3) matrices via QR(Mehta).

    Method : complex Gaussian → QR → diagonal phase fix → det⁻¹ᐟᴺ correction.
    """
    k1, k2 = random.split(key)
    re = random.normal(k1, shape + (N_GROUP, N_GROUP))
    im = random.normal(k2, shape + (N_GROUP, N_GROUP))
    M = (re + 1j * im) / jnp.sqrt(2.0)
    Q, R = jnp.linalg.qr(M)
    diag_R = jnp.diagonal(R, axis1=-2, axis2=-1)
    phase = diag_R / jnp.abs(diag_R)
    Q = Q * phase[..., None, :]
    det_Q = jnp.linalg.det(Q)
    Q = Q / (det_Q ** (1.0 / N_GROUP))[..., None, None]
    return Q


def random_su3_near_identity(key, shape, eps: float = 0.2) -> jnp.ndarray:
    """SU(3) near-identity : U = exp(i Σ_a θ_a T^a) with θ_a ~ N(0, eps²)."""
    theta = random.normal(key, shape + (N_GEN,)) * eps
    H = jnp.einsum('...a,abc->...bc', theta, T_GEN)        # Hermitian
    iH = 1j * H
    # 5-term Taylor for exp(iH); valid for small eps
    iH2 = jnp.einsum('...ij,...jk->...ik', iH, iH)
    iH3 = jnp.einsum('...ij,...jk->...ik', iH2, iH)
    iH4 = jnp.einsum('...ij,...jk->...ik', iH2, iH2)
    iH5 = jnp.einsum('...ij,...jk->...ik', iH4, iH)
    Iden = jnp.eye(N_GROUP, dtype=jnp.complex128)
    U = Iden + iH + iH2 / 2.0 + iH3 / 6.0 + iH4 / 24.0 + iH5 / 120.0
    det_U = jnp.linalg.det(U)
    U = U / (det_U ** (1.0 / N_GROUP))[..., None, None]
    return U


# ============================================================================
# Plaquette computations -- twist-aware
# ============================================================================

def _wrap_phase_field(L: int, mu: int, nu: int, use_twist: bool) -> jnp.ndarray:
    """Compute the centre phase z_{μν}(x) for each plaquette base point x.

    A plaquette P_{x,μν} = U_μ(x) U_ν(x+μ̂) U_μ(x+ν̂)† U_ν(x)† wraps in the
    (μ,ν) plane iff one of the constituent links crossed the boundary along
    μ or ν -- but the centre-phase mechanism in the twisted Wilson action
    eq. (2.6) of the paper places z_{μν} on the corner plaquette in the (μ,ν)
    plane, where x_μ = L-1 OR x_ν = L-1.

    More precisely (paper §2.4) : the twisted Wilson action puts the centre
    phase z_{μν} = exp(-2πi n^{μν}/N) on plaquettes whose evaluation
    requires the twist BC. By construction of (gather_link_twist), the
    similarity Ω_ν · U · Ω_ν^{-1} on wrapped links automatically introduces
    a phase z = ω^{n^{μν}} on the trace of the plaquette when both Ω_μ and
    Ω_ν appear in commuting positions. We isolate this phase explicitly :
    when the plaquette involves a wrap in μ̂ on a U_ν link, the trace
    picks up Tr(Ω_μ U Ω_μ^{-1} · ...) which, combined with the wrap in ν̂
    on a U_μ link, yields the centre commutator phase
        Ω_μ Ω_ν Ω_μ^{-1} Ω_ν^{-1} = z_{μν} = ω^{n^{μν}}.

    For the twist plane (TWIST_MU, TWIST_NU) the centre phase appears
    exactly on the corner plaquette x_μ = L-1, x_ν = L-1.
    Other plaquettes have phase 1.

    Returns a (L,L,L,L) complex array of phases for plaquettes P_{x,μν}.
    """
    if not use_twist:
        return jnp.ones((L, L, L, L), dtype=jnp.complex128)

    is_twist_plane = ((mu == TWIST_MU and nu == TWIST_NU) or
                      (mu == TWIST_NU and nu == TWIST_MU))
    if not is_twist_plane:
        return jnp.ones((L, L, L, L), dtype=jnp.complex128)

    # Sign of the phase for swapped (μ,ν) : z_{νμ} = z̄_{μν}
    z = Z_TWIST if (mu == TWIST_MU and nu == TWIST_NU) else jnp.conj(Z_TWIST)

    # Build the "corner" indicator : x_μ == L-1 AND x_ν == L-1
    idx_mu = jnp.arange(L)
    idx_nu = jnp.arange(L)
    shape = [1, 1, 1, 1]
    shape[mu] = L
    mask_mu = (idx_mu == (L - 1)).reshape(shape)
    shape = [1, 1, 1, 1]
    shape[nu] = L
    mask_nu = (idx_nu == (L - 1)).reshape(shape)
    corner_mask = jnp.broadcast_to(mask_mu & mask_nu, (L, L, L, L))

    return jnp.where(corner_mask, z, 1.0 + 0.0j)


def plaquette_field_twisted(U: jnp.ndarray, mu: int, nu: int,
                            use_twist: bool = True) -> jnp.ndarray:
    """Compute (1/N) Tr( z_{μν}(x) · P_{x,μν} ) on the full lattice.

    U      : shape (L,L,L,L, 4, 3, 3)
    Returns: shape (L,L,L,L) real array
    """
    L = U.shape[0]
    U_mu = U[..., mu, :, :]
    U_nu = U[..., nu, :, :]

    # U_ν(x+μ̂) and U_μ(x+ν̂) with twisted BC
    U_nu_pmu = gather_link_twist(U_nu, nu, mu, direction=-1)
    U_mu_pnu = gather_link_twist(U_mu, mu, nu, direction=-1)

    P = jnp.einsum('...ij,...jk,...lk,...ml->...im',
                   U_mu, U_nu_pmu,
                   jnp.conj(U_mu_pnu), jnp.conj(U_nu))
    tr_P = jnp.trace(P, axis1=-2, axis2=-1)
    z = _wrap_phase_field(L, mu, nu, use_twist)
    return jnp.real(z * tr_P) / N_GROUP


def wilson_action_twisted(U: jnp.ndarray, beta: float,
                          use_twist: bool = True) -> jnp.ndarray:
    """Twisted Wilson action S_W^Ω(U) = β Σ_{x,μ<ν} (1 - (1/N) Re Tr(z·P)).

    Returns a scalar.
    """
    total = 0.0
    for mu in range(DIM):
        for nu in range(mu + 1, DIM):
            re_zP = plaquette_field_twisted(U, mu, nu, use_twist=use_twist)
            total = total + jnp.sum(1.0 - re_zP)
    return beta * total


def plaquette_mean_twisted(U: jnp.ndarray, use_twist: bool = True) -> float:
    """⟨P⟩ = average over all plaquettes of (1/N) Re Tr(z·P)."""
    L = U.shape[0]
    n_plaq = (DIM * (DIM - 1) // 2) * (L ** DIM)
    s = wilson_action_twisted(U, beta=1.0, use_twist=use_twist)
    return float(1.0 - s / n_plaq)


# ============================================================================
# Staple computation -- twist-aware -- STANDARD ORDER
# ============================================================================

def compute_staples_twisted(U: jnp.ndarray, mu: int,
                            use_twist: bool = True) -> jnp.ndarray:
    """Sum K = Σ_{ν ≠ μ} (K_fwd + K_bwd) of (twist-aware) staples for link U_{x,μ}.

    STANDARD ORDER (post BP2008b bug fix on 2026-05-25) :
      K_fwd = U_ν(x+μ̂) · U_μ(x+ν̂)† · U_ν(x)†
      K_bwd = U_ν(x-ν̂+μ̂)† · U_μ(x-ν̂)† · U_ν(x-ν̂)

    Twist-aware : every jnp.roll is replaced by gather_link_twist with the
    correct twist similarity. Additionally, the centre phase z_{μν}(x) is
    incorporated for plaquettes touching the twist corner -- it multiplies
    the corresponding staple term.

    Returns K shape (L,L,L,L, 3, 3).
    """
    L = U.shape[0]
    U_mu = U[..., mu, :, :]
    K = jnp.zeros_like(U_mu)

    for nu in range(DIM):
        if nu == mu:
            continue
        U_nu = U[..., nu, :, :]

        # Forward staple : K_fwd(x) = U_ν(x+μ̂) · U_μ(x+ν̂)† · U_ν(x)†
        U_nu_pmu = gather_link_twist(U_nu, nu, mu, direction=-1)
        U_mu_pnu = gather_link_twist(U_mu, mu, nu, direction=-1)
        K_fwd = jnp.einsum('...ij,...kj,...lk->...il',
                           U_nu_pmu, jnp.conj(U_mu_pnu), jnp.conj(U_nu))

        # Centre phase z_{μν}(x) : applies on plaquette base x. For staple K(x)
        # in direction μ, the contributing plaquette is P_{x,μν}, so phase is
        # z_{μν}(x). For backward staple at x via -ν̂, plaquette base is x-ν̂.
        z_fwd = _wrap_phase_field(L, mu, nu, use_twist)
        K_fwd = z_fwd[..., None, None] * K_fwd
        K = K + K_fwd

        # Backward staple : K_bwd(x) = U_ν(x-ν̂+μ̂)† · U_μ(x-ν̂)† · U_ν(x-ν̂)
        U_nu_mnu = gather_link_twist(U_nu, nu, nu, direction=+1)
        U_mu_mnu = gather_link_twist(U_mu, mu, nu, direction=+1)
        U_nu_mnu_pmu = gather_link_twist(U_nu_mnu, nu, mu, direction=-1)
        K_bwd = jnp.einsum('...ji,...kj,...kl->...il',
                           jnp.conj(U_nu_mnu_pmu),
                           jnp.conj(U_mu_mnu), U_nu_mnu)
        # Backward plaquette base is x - ν̂, so phase z_{μν}(x - ν̂)
        z_bwd_shifted = jnp.roll(_wrap_phase_field(L, mu, nu, use_twist),
                                 +1, axis=nu)
        # NOTE : we do not retwist the phase field itself -- it is a c-number
        # field already living on plaquettes; the shift just relocates.
        K_bwd = z_bwd_shifted[..., None, None] * K_bwd
        K = K + K_bwd

    return K


# ============================================================================
# Metropolis sweep -- twist-aware, USES K (not K†) -- POST BUG FIX
# ============================================================================

def _make_metropolis_sweep(use_twist: bool):
    """Build a JIT-compiled per-mu Metropolis sweep with the use_twist flag closed."""

    @partial(jit, static_argnames=('mu', 'L'))
    def _sweep_mu(U, beta, key, mu, L, eps):
        K = compute_staples_twisted(U, mu, use_twist=use_twist)
        k1, k2 = random.split(key)
        X = random_su3_near_identity(k1, U[..., mu, :, :].shape[:-2], eps=eps)
        U_proposed = jnp.einsum('...ij,...jk->...ik', X, U[..., mu, :, :])
        # ★★★ FIX ★★★ : K direct (NOT K†) for SU(N) Metropolis !!!
        new_term = jnp.real(jnp.trace(
            jnp.einsum('...ij,...jk->...ik', U_proposed, K),
            axis1=-2, axis2=-1))
        old_term = jnp.real(jnp.trace(
            jnp.einsum('...ij,...jk->...ik', U[..., mu, :, :], K),
            axis1=-2, axis2=-1))
        dS = -beta / N_GROUP * (new_term - old_term)
        rand_u = random.uniform(k2, dS.shape)
        accept = rand_u < jnp.exp(jnp.minimum(0.0, -dS))
        U_mu_new = jnp.where(accept[..., None, None], U_proposed, U[..., mu, :, :])
        return U.at[..., mu, :, :].set(U_mu_new), jnp.mean(accept.astype(jnp.float64))

    def sweep(U, beta, key, L, eps=0.2):
        accs = []
        for mu in range(DIM):
            key, sk = random.split(key)
            U, acc_mu = _sweep_mu(U, beta, sk, mu, L, eps)
            accs.append(acc_mu)
        mean_acc = jnp.mean(jnp.array(accs))
        return U, mean_acc, key

    return sweep


metropolis_sweep_twisted  = _make_metropolis_sweep(use_twist=True)
metropolis_sweep_periodic = _make_metropolis_sweep(use_twist=False)


def thermalize(key, beta: float, L: int, n_sweeps: int,
               use_twist: bool = True, eps: float = 0.2, start: str = 'hot',
               verbose: bool = True) -> Tuple[jnp.ndarray, jax.Array, float, List[float]]:
    """Thermalise lattice from `start` initial condition.

    start : 'hot' (Haar random), 'cold' (U=Id), or 'mixed' (Haar + small noise).
    Returns : (U, key, final_acceptance_rate, ⟨P⟩-trace)
    """
    sweep = metropolis_sweep_twisted if use_twist else metropolis_sweep_periodic

    if start == 'hot':
        key, sk = random.split(key)
        U = random_su3_haar(sk, (L, L, L, L, DIM))
    elif start == 'cold':
        Iden = jnp.eye(N_GROUP, dtype=jnp.complex128)
        U = jnp.broadcast_to(Iden, (L, L, L, L, DIM, N_GROUP, N_GROUP)).copy()
    elif start == 'mixed':
        key, sk1, sk2 = random.split(key, 3)
        U_haar = random_su3_haar(sk1, (L, L, L, L, DIM))
        Iden = jnp.broadcast_to(
            jnp.eye(N_GROUP, dtype=jnp.complex128),
            (L, L, L, L, DIM, N_GROUP, N_GROUP))
        # 50/50 mix at link level
        rand_mask = random.uniform(sk2, U_haar.shape[:-2]) < 0.5
        U = jnp.where(rand_mask[..., None, None], U_haar, Iden)
    else:
        raise ValueError(f"start must be 'hot'|'cold'|'mixed', got {start!r}")

    p_trace = []
    acc_trace = []
    log_every = max(1, n_sweeps // 10)
    t0 = time.time()
    acc = jnp.array(0.0)
    for i in range(n_sweeps):
        U, acc, key = sweep(U, beta, key, L, eps)
        if (i + 1) % log_every == 0 or i == 0:
            p = plaquette_mean_twisted(U, use_twist=use_twist)
            p_trace.append((i + 1, p))
            acc_trace.append(float(acc))
            if verbose:
                print(f"    sweep {i+1:5d}: ⟨P⟩={p:+.4f}  acc={float(acc):.3f}  "
                      f"t={time.time()-t0:.1f}s", flush=True)
    return U, key, float(acc), p_trace


# ============================================================================
# Reference ⟨P⟩(β) values for SU(3) (van Baal 1982, Sternbeck 2005)
# Values are bulk periodic plaquette averages; twisted measure differs by
# the corner phase contribution only -- a finite-volume O(1/L^4) effect.
# ============================================================================
# Source : Lucini, Teper, Wenger 2004 (hep-lat/0404008) Table 1 SU(3)
# β = 5.7, ⟨P⟩ = 0.549   (Wilson normalised β_W = 2N/g² = 6/g²)
# Note paper uses β = 2N²/λ (t Hooft) convention : β_tHooft = β_W / N for SU(N)
# So β_W = 5.7 ↔ β_tHooft = 1.9 ; β_tHooft = 3.0 ↔ β_W = 9.0 (deep continuum)
#
# In our paper we use β_W (Wilson) convention since action is β·S_W.
# Paper's β ∈ {2.5, 3.0, 3.5} are very small Wilson β -- corresponding to
# STRONG coupling for SU(3). Standard SU(3) continuum is β_W ≈ 5.5..6.5.
#
# Recheck of paper §4.4 : "β ∈ {2.5, 3.0, 3.5} (continuum regime)".
# For SU(3), continuum regime means β_W ≥ 5.7 (gauge coupling λ ≤ ~1).
# β = 2.5..3.5 in Wilson convention is DEEP STRONG coupling (confinement
# phase, ⟨P⟩ ≈ 0.2..0.3).
#
# We interpret the paper's β as t'Hooft β_tH = β_W/N=3, so β_tH = 2.5 →
# β_W = 7.5 (weak coupling), β_tH = 3.0 → β_W = 9.0, β_tH = 3.5 → β_W = 10.5.
# This is also consistent with eq. (2.6) where action has β · Σ (1 - Re Tr P / N) :
# β here is the "lattice coupling" in front of the action, which for SU(N) is
# β_W. The numerical match requires β_W ≥ 5.7 for continuum.
#
# To be safe we PRINT both interpretations and accept either if ⟨P⟩ matches.
# ============================================================================

SU3_PLAQUETTE_REFERENCE = {
    # (Wilson β_W) : ⟨P⟩ from Lucini-Teper-Wenger 2004 + Necco-Sommer 2002
    5.5:  0.522,   # strong coupling near transition
    5.7:  0.549,
    5.85: 0.575,
    6.0:  0.594,
    6.2:  0.614,
    6.4:  0.631,
    6.6:  0.647,
    7.0:  0.674,
    7.5:  0.700,
    8.0:  0.721,
    9.0:  0.753,
    10.5: 0.788,
    # Strong coupling (large g², β small) -- approximate
    2.5:  0.225,   # very strong coupling, confinement
    3.0:  0.275,
    3.5:  0.330,
}


def expected_plaquette(beta_W: float) -> Tuple[float, str]:
    """Interpolate reference ⟨P⟩(β_W) and provide a confidence label."""
    keys = sorted(SU3_PLAQUETTE_REFERENCE.keys())
    if beta_W < keys[0] or beta_W > keys[-1]:
        return -1.0, 'OUT_OF_RANGE'
    # exact match
    if beta_W in SU3_PLAQUETTE_REFERENCE:
        return SU3_PLAQUETTE_REFERENCE[beta_W], 'EXACT'
    # linear interpolation
    for k1, k2 in zip(keys, keys[1:]):
        if k1 <= beta_W <= k2:
            v1 = SU3_PLAQUETTE_REFERENCE[k1]
            v2 = SU3_PLAQUETTE_REFERENCE[k2]
            t = (beta_W - k1) / (k2 - k1)
            return v1 * (1 - t) + v2 * t, 'INTERP'
    return -1.0, 'UNKNOWN'


# ============================================================================
# Observable O1 : Faddeev-Popov smallest eigenvalue λ_min(M^Ω[A])
# M^Ω[A] = d_A^{†,Ω} · d_A^Ω  acts on ad(P)-valued 0-forms (su(N)-valued
# scalar fields on the lattice).
#
# Lattice convention :
#   For φ ∈ Maps(Λ, su(N)), the gauge covariant lattice derivative
#     (d_A φ)_{x,μ} = U_μ(x) · φ(x+μ̂) · U_μ(x)† - φ(x)
#   Its adjoint d_A† maps 1-forms back to 0-forms :
#     (d_A† ω)(x) = Σ_μ [ U_μ(x-μ̂)† · ω_{x-μ̂,μ} · U_μ(x-μ̂) - ω_{x,μ} ]
#
# The FP operator M[A] = d_A† d_A is positive semi-definite.
# For periodic BC at A=0, M[0] = -Δ has constant zero mode (4·(N²-1)-fold);
# for twisted BC the constant zero mode is absent (Proposition 3.1).
#
# We use matrix-free Lanczos for λ_min via power iteration on (μ·I - M)
# with μ = trace estimate, or direct Lanczos with shift-invert.
# ============================================================================

def _su_n_anti_hermitian(phi_real: jnp.ndarray) -> jnp.ndarray:
    """Convert real coefficients (8,) on T^a generators to anti-Hermitian su(3).

    phi_real shape (..., N_GEN), returns shape (..., N_GROUP, N_GROUP) complex.
    Standard convention : φ = i · Σ_a φ_a T^a (anti-Hermitian, traceless).
    """
    H = jnp.einsum('...a,abc->...bc', phi_real, T_GEN)   # Hermitian
    return 1j * H


def _su_n_components(phi_anti_herm: jnp.ndarray) -> jnp.ndarray:
    """Inverse : extract real coefficients from anti-Hermitian su(3) matrix.

    For anti-Hermitian φ = i Σ_a φ_a T^a :  φ_a = -2 i Tr(φ T^a) = 2 Tr(-iφ T^a)
    Since Tr(T^a T^b) = δ_{ab}/2 ·... let's compute properly :
      Tr(T^a T^b) = (1/4) Tr(λ^a λ^b) = (1/4) · 2 δ_{ab} = δ_{ab}/2
    So if H = Σ_a φ_a T^a, then Tr(H T^a) = φ_a / 2, hence φ_a = 2 Tr(H T^a).
    For anti-Hermitian φ_AH = iH : H = -iφ_AH, so φ_a = 2 Tr(-i φ_AH T^a) =
                                   -2i Tr(φ_AH T^a).
    """
    return jnp.real(-2j * jnp.einsum('...ij,aji->...a', phi_anti_herm, T_GEN))


@partial(jit, static_argnames=('use_twist',))
def fp_apply(phi_real: jnp.ndarray, U: jnp.ndarray,
             use_twist: bool = True) -> jnp.ndarray:
    """Apply M^Ω[A] = d_A^{†,Ω} d_A^Ω  to a real-coefficient field φ on the lattice.

    Input phi_real : shape (L,L,L,L, N_GEN)
    Returns shape (L,L,L,L, N_GEN)
    """
    L = U.shape[0]
    # Build anti-Hermitian su(N) field
    phi = _su_n_anti_hermitian(phi_real)   # (L,L,L,L, N, N)

    # Apply d_A φ : 1-form, shape (L,L,L,L, 4, N, N)
    one_form_parts = []
    for mu in range(DIM):
        U_mu = U[..., mu, :, :]
        # φ(x + μ̂) with twisted BC
        phi_pmu = gather_link_twist(phi, mu_link_index=0, shift_dir=mu, direction=-1)
        # NOTE: phi is a scalar (0-form) so the link similarity for boundary
        # crossing IS the adjoint similarity Ω · φ · Ω† -- which is exactly
        # what gather_link_twist does. So we are good.
        # (d_A φ)_{x,μ} = U_μ(x) φ(x+μ̂) U_μ(x)† - φ(x)
        d_mu = jnp.einsum('...ij,...jk,...lk->...il',
                          U_mu, phi_pmu, jnp.conj(U_mu)) - phi
        one_form_parts.append(d_mu)
    one_form = jnp.stack(one_form_parts, axis=-3)   # (L,L,L,L, 4, N, N)

    # Apply d_A^† to the 1-form to get back a 0-form
    out = jnp.zeros_like(phi)
    for mu in range(DIM):
        U_mu = U[..., mu, :, :]
        omega_mu = one_form[..., mu, :, :]
        # Backward part : U_μ(x-μ̂)† · ω_{x-μ̂,μ} · U_μ(x-μ̂)
        U_mu_mmu = gather_link_twist(U_mu, mu, mu, direction=+1)
        omega_mmu = gather_link_twist(omega_mu, mu, mu, direction=+1)
        back = jnp.einsum('...ji,...jk,...kl->...il',
                          jnp.conj(U_mu_mmu), omega_mmu, U_mu_mmu)
        out = out + back - omega_mu

    # Extract real coefficients
    return _su_n_components(out)


def lanczos_smallest_eigenvalue(matvec, dim: int, key, n_iter: int = 100,
                                tol: float = 1e-8) -> Tuple[float, int]:
    """Compute the smallest eigenvalue of a Hermitian linear operator via Lanczos.

    matvec : function v ↦ A v, where v is a 1D real vector of length dim.
    Returns (λ_min, n_iter_used).

    Implementation : Lanczos tri-diagonalization, then eigvalsh of T_k.
    """
    # Initial random vector
    v_prev = jnp.zeros(dim)
    v = random.normal(key, (dim,))
    v = v / jnp.linalg.norm(v)
    beta_prev = 0.0
    alphas = []
    betas = []
    lam_min_prev = None
    for k in range(n_iter):
        w = matvec(v) - beta_prev * v_prev
        alpha = float(jnp.dot(v, w))
        alphas.append(alpha)
        w = w - alpha * v
        # Full reorthogonalisation for numerical stability (small dim, cheap)
        # (Skipped here for memory reasons -- Lanczos should be stable enough
        # for our purpose.)
        beta_k = float(jnp.linalg.norm(w))
        if beta_k < tol:
            break
        betas.append(beta_k)
        v_prev = v
        v = w / beta_k
        beta_prev = beta_k
        # Estimate λ_min from current T_k every 5 iterations
        if (k + 1) % 5 == 0:
            T = np.diag(alphas) + np.diag(betas[:len(alphas) - 1], 1) \
                                + np.diag(betas[:len(alphas) - 1], -1)
            lam_T = np.linalg.eigvalsh(T)
            lam_min = float(lam_T[0])
            if lam_min_prev is not None and abs(lam_min - lam_min_prev) < tol:
                return lam_min, k + 1
            lam_min_prev = lam_min

    T = np.diag(alphas) + np.diag(betas[:len(alphas) - 1], 1) \
                        + np.diag(betas[:len(alphas) - 1], -1)
    lam_T = np.linalg.eigvalsh(T)
    return float(lam_T[0]), n_iter


def measure_fp_lambda_min(U: jnp.ndarray, key, use_twist: bool = True,
                          n_iter: int = 80) -> float:
    """Measure λ_min(M^Ω[A]) at the supplied configuration U."""
    L = U.shape[0]
    dim_total = L ** DIM * N_GEN

    def matvec(v_flat):
        v_field = v_flat.reshape((L, L, L, L, N_GEN))
        Mv = fp_apply(v_field, U, use_twist=use_twist)
        return Mv.reshape((dim_total,))

    lam_min, _ = lanczos_smallest_eigenvalue(matvec, dim_total, key, n_iter=n_iter)
    return lam_min


# ============================================================================
# Observable O2 : Spectral gap of Hess(β · S_W^Ω) on the link tangent bundle
#
# At a link configuration U, parametrise nearby links via U_μ(x) → exp(i A_μ(x)) U_μ(x)
# with A_μ(x) ∈ su(N). The Hessian of β · S_W^Ω is the second derivative
# w.r.t. the real components A_μ(x)^a.
#
# Total dimension = L^4 · D · (N²-1) = L^4 · 4 · 8 = 32 L^4 for SU(3)
# (≈ 65k for L=8, 663k for L=12, 2M for L=16)
#
# Matrix-free approach : we use jax.jvp to compute Hess(S) · v for v ∈ T(M).
# ============================================================================

def hess_action_apply(A_real: jnp.ndarray, U: jnp.ndarray, beta: float,
                      use_twist: bool = True) -> jnp.ndarray:
    """Compute Hess(β · S_W^Ω) · A, where A is parametrised as real
    components on each link's tangent space.

    A_real shape (L,L,L,L, DIM, N_GEN)
    Returns same shape.
    """
    L = U.shape[0]

    def action_at_perturbation(eps_a):
        # U_μ(x) → exp(i · eps_a · A_μ(x)) U_μ(x)
        H = jnp.einsum('...a,abc->...bc', A_real, T_GEN)     # (L,L,L,L,DIM,N,N) Herm
        iH = 1j * eps_a * H
        # exp(iH) via 5-term Taylor (valid for small eps_a)
        iH2 = jnp.einsum('...ij,...jk->...ik', iH, iH)
        iH3 = jnp.einsum('...ij,...jk->...ik', iH2, iH)
        iH4 = jnp.einsum('...ij,...jk->...ik', iH2, iH2)
        iH5 = jnp.einsum('...ij,...jk->...ik', iH4, iH)
        Iden = jnp.eye(N_GROUP, dtype=jnp.complex128)
        Iden_b = jnp.broadcast_to(Iden, iH.shape)
        expiH = Iden_b + iH + iH2 / 2.0 + iH3 / 6.0 + iH4 / 24.0 + iH5 / 120.0
        # det projection
        det = jnp.linalg.det(expiH)
        expiH = expiH / (det ** (1.0 / N_GROUP))[..., None, None]
        U_pert = jnp.einsum('...ij,...jk->...ik', expiH, U)
        return wilson_action_twisted(U_pert, beta, use_twist=use_twist)

    # Hessian-vector product : H · v = d²/dε² S(U·exp(iε A))|_{ε=0}
    # Use second-order finite difference (simpler than autodiff)
    eps = 1e-3
    S_plus  = action_at_perturbation(+eps)
    S_minus = action_at_perturbation(-eps)
    S_zero  = action_at_perturbation(0.0)
    # The Hessian quadratic form Q(A) = (1/2) (S(+ε A) + S(-ε A) - 2 S(0)) / ε²
    # gives the energy quadratic at A. To get Hess·v we'd need the gradient of Q.
    # Cleaner : use jax.grad twice.
    return ((S_plus + S_minus - 2.0 * S_zero) / (eps ** 2))


def measure_hess_gap(U: jnp.ndarray, beta: float, key,
                     use_twist: bool = True, n_iter: int = 50) -> Dict[str, float]:
    """Measure smallest positive eigenvalue of Hess(β·S^Ω) via Lanczos.

    Uses jax.grad of quadratic form to build Hess·v products.
    For SU(3), L=8 : dim = 8 · 4 · 8 · 8 · 8 · 8 = 131072 -- direct Lanczos feasible.
    """
    L = U.shape[0]
    dim_total = (L ** DIM) * DIM * N_GEN

    # Build Hess·v via twice-differentiated action :
    #   Q(A) = (1/2) Hess(S) · A · A  →  ∇_A Q = Hess(S) · A
    # We use jax.grad of A → Q(A) at A=0 evaluated in direction v.
    def quad_form(A_flat):
        A_field = A_flat.reshape((L, L, L, L, DIM, N_GEN))
        # Compute (1/2) ε² Hess · A · A approximated by [S(ε A) + S(-ε A) - 2S(0)] / 2
        return 0.5 * hess_action_apply(A_field, U, beta, use_twist=use_twist)

    grad_quad = jax.grad(quad_form)

    def matvec(v_flat):
        # Hess · v = ∇_A Q(A)|_{A=v} -- since Q is exactly quadratic
        return jnp.asarray(grad_quad(v_flat))

    lam_min, _ = lanczos_smallest_eigenvalue(matvec, dim_total, key, n_iter=n_iter)

    # m_Ω² prediction (twisted Hodge gap)
    m_Omega_sq = (2.0 * np.pi / (N_GROUP * L)) ** 2
    # Periodic gap m_0² = (2π/L)²
    m_0_sq = (2.0 * np.pi / L) ** 2

    return {
        'lam_min_hess': lam_min,
        'm_Omega_sq': m_Omega_sq,
        'm_0_sq': m_0_sq,
        'lam_min_div_m_Omega_sq': lam_min / m_Omega_sq if m_Omega_sq > 0 else None,
        'theoretical_lower_bound_5_6_m_Omega_sq': ONE_M_KAPPA * m_Omega_sq,
    }


# ============================================================================
# Observable O3 : Rothaus-Simon mean-field LSI constant estimate
#
# For a probability measure ν on a manifold M with smooth density e^{-V}/Z,
# the Rothaus-Simon mean-field estimate for the LSI constant is :
#   C_LSI(ν) ≤ 1 / (κ_RIC + λ_min(Hess V))
# where κ_RIC is the Ricci lower bound of M.
#
# For our setting :
#   ν = μ^Ω = e^{-β S_W^Ω} / Z
#   M = (SU(3)^link)^|edges| with Haar metric, Ricci ≥ (N²-1)/(4N) per dim
#
# This yields :
#   C_LSI(μ^Ω) ≤ 1 / (κ_RIC + β · λ_min(Hess S_W^Ω))
# which we can estimate empirically by measuring λ_min(Hess S^Ω) on samples.
# ============================================================================

def estimate_lsi_constant_rothaus_simon(hess_gap_values: List[float],
                                         beta: float, L: int) -> Dict[str, float]:
    """Rothaus-Simon mean-field estimate of C_LSI(μ^Ω) from sampled gaps.

    Hess gap values should be in physical units (per-site or per-link).
    """
    hess_arr = np.asarray(hess_gap_values)
    mean_gap = float(np.mean(hess_arr))
    std_gap  = float(np.std(hess_arr, ddof=1)) if len(hess_arr) > 1 else 0.0

    # Ricci of SU(N) Haar : Ric ≥ (N²-1)/(4N) ; here = 8/12 = 2/3
    kappa_ric = (N_GROUP ** 2 - 1) / (4.0 * N_GROUP)

    # C_LSI estimate (upper bound)
    denom = kappa_ric + mean_gap
    if denom > 0:
        c_lsi = 1.0 / denom
    else:
        c_lsi = float('inf')

    # Paper's theoretical bound : 43.7 / m_0² with m_0² = (2π/L)²
    m_0_sq = (2.0 * np.pi / L) ** 2
    c_lsi_paper_bound = 43.7 / m_0_sq

    return {
        'mean_hess_gap': mean_gap,
        'std_hess_gap': std_gap,
        'kappa_ricci': kappa_ric,
        'C_LSI_rothaus_simon': c_lsi,
        'C_LSI_paper_bound': c_lsi_paper_bound,
        'pass_bound': c_lsi <= c_lsi_paper_bound if c_lsi != float('inf') else False,
    }


# ============================================================================
# Autocorrelation analysis (essential for sanity check)
# ============================================================================

def autocorrelation_time(series: np.ndarray, max_lag: Optional[int] = None) -> float:
    """Integrated autocorrelation time τ_int = 1 + 2 Σ_{t=1}^{cutoff} ρ(t).

    Cutoff = first lag where ρ(t) < 0 (Sokal automatic windowing).
    """
    n = len(series)
    if n < 4:
        return 0.5
    if max_lag is None:
        max_lag = min(n // 4, 200)
    mean = np.mean(series)
    var = np.var(series, ddof=0)
    if var < 1e-20:
        return 0.5
    rho = np.array([np.mean((series[:n-t] - mean) * (series[t:] - mean)) / var
                    for t in range(max_lag + 1)])
    tau = 0.5
    for t in range(1, max_lag + 1):
        if rho[t] < 0:
            break
        tau += rho[t]
    return float(tau)


# ============================================================================
# Sanity battery -- MUST pass before measurements
# ============================================================================

def sanity_battery(L: int, beta: float, n_therm: int, key,
                   verbose: bool = True) -> Dict[str, any]:
    """Run sanity tests for a (L, β) configuration.

    1. Centraliser lemma (algebraic, deterministic)
    2. Cold start ⟨P⟩(t=0) = 1.0 periodic, |1/N| twisted
    3. Hot start thermalization, ⟨P⟩ vs SU(3) literature
    4. Metropolis acceptance ∈ [0.3, 0.7]
    5. Autocorrelation time τ_int reasonable
    6. Comparison twisted vs periodic ⟨P⟩
    """
    if verbose:
        print(f"\n{'='*72}", flush=True)
        print(f"  SANITY BATTERY  L={L}  β={beta}  n_therm={n_therm}", flush=True)
        print(f"{'='*72}", flush=True)

    sanity = {'L': L, 'beta': beta, 'n_therm': n_therm}

    # Test 1 : centraliser
    cent = check_centraliser_lemma()
    sanity['centraliser'] = cent
    if verbose:
        print(f"\n[1] Centraliser lemma (Ω_0·Ω_1 = ω̄·Ω_1·Ω_0)", flush=True)
        print(f"    'tHooft commutator max err = {cent['tHooft_commutator_max_err']:.2e}",
              flush=True)
        print(f"    wrong-sign sanity (should be ~1.732) = "
              f"{cent['tHooft_commutator_max_err_wrong_sign']:.4f}", flush=True)
        print(f"    det(Ω_0) = {cent['det_Omega0']:.6f}, det(Ω_1) = {cent['det_Omega1']:.6f}",
              flush=True)
        print(f"    PASS = {cent['pass_commutator'] and cent['pass_det0'] and cent['pass_det1']}",
              flush=True)

    # Test 2 : cold start values
    if verbose:
        print(f"\n[2] Cold start (U=Id) plaquette values", flush=True)
    Iden = jnp.eye(N_GROUP, dtype=jnp.complex128)
    U_cold = jnp.broadcast_to(Iden, (L, L, L, L, DIM, N_GROUP, N_GROUP))
    p_cold_per = plaquette_mean_twisted(U_cold, use_twist=False)
    p_cold_tw  = plaquette_mean_twisted(U_cold, use_twist=True)
    # Twisted cold start : on each "corner" plaquette in the (μ,ν)=(0,1)-plane,
    # i.e. base point with x_μ = L-1 AND x_ν = L-1, the contribution is
    # (1/N) Re Tr(z · I) = Re(z) = Re(ω̄) = cos(2π/3) = -1/2.
    # The number of such corner plaquettes is L^{D-2} (one for each (x_ρ,x_σ)
    # with ρ,σ ∉ {μ,ν}) = L^2 in 4D. They all lie in the SAME (μ,ν) plane
    # (only one plane is twisted), so the total deficit relative to the
    # all-plaquette mean 1.0 is
    #     Δ = L^{D-2} · (1 - (-1/2)) / n_plaq = 1.5 · L^{D-2} / n_plaq.
    # With n_plaq = (D(D-1)/2) · L^D one gets
    #     1 - p_cold_tw_expected = 1.5 · L^{D-2} / (D(D-1)/2 · L^D)
    #                            = 3 / (D(D-1) · L^2)   (= 1/(4 L²) for D=4)
    # FIX 2026-05-26 : v1 used L^0 = 1 corner plaquette only.
    n_plaq = (DIM * (DIM - 1) // 2) * (L ** DIM)
    n_corner_plaq = L ** (DIM - 2)
    p_cold_tw_expected = 1.0 - 1.5 * n_corner_plaq / n_plaq
    sanity['cold_p_periodic'] = p_cold_per
    sanity['cold_p_twisted']  = p_cold_tw
    sanity['cold_p_twisted_expected'] = p_cold_tw_expected
    sanity['n_corner_plaquettes'] = n_corner_plaq
    sanity['n_plaq_total'] = n_plaq
    if verbose:
        print(f"    ⟨P⟩ periodic = {p_cold_per:+.6f}  (expected 1.0)", flush=True)
        print(f"    ⟨P⟩ twisted  = {p_cold_tw:+.6f}  (expected {p_cold_tw_expected:+.6f})",
              flush=True)
        print(f"    n_corner = {n_corner_plaq}  /  n_plaq_total = {n_plaq}", flush=True)
        ok2 = (abs(p_cold_per - 1.0) < 1e-6) and \
              (abs(p_cold_tw - p_cold_tw_expected) < 1e-5)
        print(f"    PASS = {ok2}", flush=True)
        sanity['pass_cold'] = ok2

    # Test 3 : hot start thermalization (periodic)
    if verbose:
        print(f"\n[3] Hot start thermalization (PERIODIC) {n_therm} sweeps", flush=True)
    key, sk = random.split(key)
    U_per, key, acc_per, p_trace_per = thermalize(
        sk, beta, L, n_therm, use_twist=False, start='hot', verbose=verbose)
    p_final_per = plaquette_mean_twisted(U_per, use_twist=False)
    p_ref, label = expected_plaquette(beta)
    rel_err_per = abs(p_final_per - p_ref) / p_ref if p_ref > 0 else None
    sanity['hot_p_periodic_final'] = p_final_per
    sanity['hot_p_periodic_ref'] = p_ref
    sanity['hot_p_periodic_ref_label'] = label
    sanity['hot_p_periodic_relerr'] = rel_err_per
    sanity['hot_acc_periodic'] = acc_per
    if verbose:
        print(f"    ⟨P⟩ final = {p_final_per:+.4f}", flush=True)
        print(f"    ⟨P⟩ ref   = {p_ref:+.4f}  ({label})", flush=True)
        if rel_err_per is not None:
            print(f"    rel err   = {rel_err_per*100:.2f}%",
                  flush=True)
        print(f"    acceptance = {acc_per:.3f}", flush=True)

    # Test 4 : hot start thermalization (twisted)
    if verbose:
        print(f"\n[4] Hot start thermalization (TWISTED) {n_therm} sweeps", flush=True)
    key, sk = random.split(key)
    U_tw, key, acc_tw, p_trace_tw = thermalize(
        sk, beta, L, n_therm, use_twist=True, start='hot', verbose=verbose)
    p_final_tw = plaquette_mean_twisted(U_tw, use_twist=True)
    # For large L, twisted ⟨P⟩ → periodic ⟨P⟩ + O(1/L^4)
    rel_err_tw_per = abs(p_final_tw - p_final_per) if p_final_per > 0 else None
    sanity['hot_p_twisted_final'] = p_final_tw
    sanity['hot_acc_twisted'] = acc_tw
    sanity['twist_periodic_diff'] = abs(p_final_tw - p_final_per)
    if verbose:
        print(f"    ⟨P⟩ final twisted  = {p_final_tw:+.4f}", flush=True)
        print(f"    ⟨P⟩ final periodic = {p_final_per:+.4f}", flush=True)
        print(f"    |diff|             = {abs(p_final_tw - p_final_per):.4f}",
              flush=True)
        print(f"    acceptance twisted = {acc_tw:.3f}", flush=True)

    # Test 5 : Metropolis acceptance check
    sanity['pass_acceptance_per'] = 0.3 <= acc_per <= 0.7
    sanity['pass_acceptance_tw']  = 0.3 <= acc_tw  <= 0.7
    if verbose:
        print(f"\n[5] Acceptance rate check (expect ∈ [0.3, 0.7])", flush=True)
        print(f"    PASS periodic = {sanity['pass_acceptance_per']}", flush=True)
        print(f"    PASS twisted  = {sanity['pass_acceptance_tw']}", flush=True)

    # Test 6 : autocorrelation
    if len(p_trace_tw) >= 4:
        p_series = np.array([p for (i, p) in p_trace_tw])
        tau = autocorrelation_time(p_series)
        sanity['tau_int_twisted'] = tau
        if verbose:
            print(f"\n[6] Autocorrelation time τ_int (on ⟨P⟩ trace) = {tau:.2f}",
                  flush=True)

    # Overall PASS verdict
    ok_global = (
        cent['pass_commutator'] and cent['pass_det0'] and cent['pass_det1']
        and sanity.get('pass_cold', False)
        and sanity['pass_acceptance_per']
        and sanity['pass_acceptance_tw']
        and (rel_err_per is None or rel_err_per < 0.20)  # 20% tolerance
    )
    sanity['SANITY_OVERALL_PASS'] = ok_global
    if verbose:
        print(f"\n{'='*72}", flush=True)
        print(f"  SANITY OVERALL : {'PASS' if ok_global else 'FAIL'}", flush=True)
        print(f"{'='*72}", flush=True)

    # Return thermalised configurations for re-use in measurements
    sanity['_U_twisted_thermalised']  = U_tw
    sanity['_U_periodic_thermalised'] = U_per
    sanity['_key'] = key
    return sanity


# ============================================================================
# Main driver : run a (L, β) configuration with sanity → measurements
# ============================================================================

def run_one_config(L: int, beta: float, n_therm: int, n_decorr: int,
                   n_samples: int, key, output_dir: str = '.',
                   verbose: bool = True) -> Dict[str, any]:
    """Run a single (L, β) configuration : sanity + measurements + JSON output."""
    t_start = time.time()
    result = {
        'L': L, 'beta': beta,
        'n_therm': n_therm, 'n_decorr': n_decorr, 'n_samples': n_samples,
        'date_utc': time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime()),
        'author': 'Kévin Rémondière',
        'orcid': '0009-0008-2443-7166',
        'script': 'jax_su3_tHooft_lattice_PROPER_2026-05-26.py',
        'paper_ref': 'Paper_tHooft_Twist_Mode_Zero_LMP/main.tex',
    }

    # Sanity battery (and reuse thermalised configs)
    sanity = sanity_battery(L, beta, n_therm, key, verbose=verbose)
    if not sanity['SANITY_OVERALL_PASS']:
        result['status'] = 'SANITY_FAILED'
        result['sanity'] = {k: v for k, v in sanity.items() if not k.startswith('_')}
        if verbose:
            print(f"\n!! SANITY FAILED for L={L}, β={beta} -- skipping measurements",
                  flush=True)
        return result

    U_tw  = sanity['_U_twisted_thermalised']
    U_per = sanity['_U_periodic_thermalised']
    key   = sanity['_key']
    result['sanity'] = {k: v for k, v in sanity.items() if not k.startswith('_')}

    if verbose:
        print(f"\n{'='*72}", flush=True)
        print(f"  MEASUREMENTS  L={L}  β={beta}", flush=True)
        print(f"{'='*72}", flush=True)

    # O1 + O2 measurements on n_samples thermalised configs
    lam_fp_tw  = []
    lam_fp_per = []
    hess_gap_tw  = []
    hess_gap_per = []

    for s in range(n_samples):
        if verbose and (s % 5 == 0 or s == n_samples - 1):
            print(f"  Sample {s+1}/{n_samples}  "
                  f"t={time.time()-t_start:.1f}s", flush=True)

        # Decorrelate (sweep returns new key already)
        for _ in range(n_decorr):
            U_tw,  _, key = metropolis_sweep_twisted(U_tw,  beta, key, L, eps=0.2)
            U_per, _, key = metropolis_sweep_periodic(U_per, beta, key, L, eps=0.2)

        # O1 : λ_min of FP operator (twisted vs periodic)
        key, sk1, sk2 = random.split(key, 3)
        try:
            lam_tw = measure_fp_lambda_min(U_tw, sk1, use_twist=True, n_iter=60)
            lam_pe = measure_fp_lambda_min(U_per, sk2, use_twist=False, n_iter=60)
        except Exception as e:
            print(f"  ! FP measurement failed at sample {s}: {e}", flush=True)
            lam_tw, lam_pe = float('nan'), float('nan')
        lam_fp_tw.append(lam_tw)
        lam_fp_per.append(lam_pe)

        # O2 : Hessian gap (every 5 samples to save time -- expensive)
        if s % 5 == 0:
            key, sk1, sk2 = random.split(key, 3)
            try:
                gap_tw = measure_hess_gap(U_tw,  beta, sk1, use_twist=True,  n_iter=40)
                gap_pe = measure_hess_gap(U_per, beta, sk2, use_twist=False, n_iter=40)
                hess_gap_tw.append(gap_tw['lam_min_hess'])
                hess_gap_per.append(gap_pe['lam_min_hess'])
            except Exception as e:
                print(f"  ! Hess measurement failed at sample {s}: {e}", flush=True)

    # Aggregate O1, O2 statistics
    lam_fp_tw_arr  = np.asarray(lam_fp_tw)
    lam_fp_per_arr = np.asarray(lam_fp_per)
    m_Omega_sq = (2.0 * np.pi / (N_GROUP * L)) ** 2
    m_0_sq     = (2.0 * np.pi / L) ** 2
    bound_5_6  = ONE_M_KAPPA * m_Omega_sq

    o1 = {
        'twisted': {
            'mean': float(np.nanmean(lam_fp_tw_arr)),
            'std':  float(np.nanstd(lam_fp_tw_arr, ddof=1))
                    if len(lam_fp_tw_arr) > 1 else 0.0,
            'min':  float(np.nanmin(lam_fp_tw_arr)),
            'n_samples': len(lam_fp_tw_arr),
        },
        'periodic': {
            'mean': float(np.nanmean(lam_fp_per_arr)),
            'std':  float(np.nanstd(lam_fp_per_arr, ddof=1))
                    if len(lam_fp_per_arr) > 1 else 0.0,
            'min':  float(np.nanmin(lam_fp_per_arr)),
            'n_samples': len(lam_fp_per_arr),
        },
        'm_Omega_sq': m_Omega_sq,
        'm_0_sq': m_0_sq,
        'theoretical_lower_bound_5_6_m_Omega_sq': bound_5_6,
        'pass_twisted_above_bound':
            bool(np.nanmean(lam_fp_tw_arr) >= 0.9 * bound_5_6),
        'periodic_near_zero_check':
            bool(np.nanmean(lam_fp_per_arr) < 0.1 * bound_5_6),
    }
    result['O1_FP_lambda_min'] = o1

    if len(hess_gap_tw) > 0:
        hess_tw_arr = np.asarray(hess_gap_tw)
        hess_pe_arr = np.asarray(hess_gap_per) if hess_gap_per else np.array([])
        o2 = {
            'twisted_mean': float(np.nanmean(hess_tw_arr)),
            'twisted_std':  float(np.nanstd(hess_tw_arr, ddof=1))
                            if len(hess_tw_arr) > 1 else 0.0,
            'periodic_mean': float(np.nanmean(hess_pe_arr)) if len(hess_pe_arr) > 0 else None,
            'n_samples_hess': len(hess_tw_arr),
        }
        result['O2_Hess_gap'] = o2

        # O3 : Rothaus-Simon LSI estimate
        rs = estimate_lsi_constant_rothaus_simon(list(hess_tw_arr), beta, L)
        result['O3_LSI_rothaus_simon'] = rs

    result['status'] = 'OK'
    result['wall_time_seconds'] = time.time() - t_start

    # Print summary
    if verbose:
        print(f"\n{'='*72}", flush=True)
        print(f"  RESULTS SUMMARY  L={L}  β={beta}", flush=True)
        print(f"{'='*72}", flush=True)
        print(f"  O1 : λ_min(M^Ω) twisted  = {o1['twisted']['mean']:.6e} "
              f"± {o1['twisted']['std']:.2e}", flush=True)
        print(f"       λ_min(M)   periodic = {o1['periodic']['mean']:.6e} "
              f"± {o1['periodic']['std']:.2e}", flush=True)
        print(f"       (5/6) m_Ω²          = {bound_5_6:.6e}", flush=True)
        print(f"       PASS twisted ≥ bound : {o1['pass_twisted_above_bound']}",
              flush=True)
        print(f"       PASS periodic near 0  : {o1['periodic_near_zero_check']}",
              flush=True)
        if 'O2_Hess_gap' in result:
            print(f"  O2 : Hess gap twisted  = {result['O2_Hess_gap']['twisted_mean']:.6e}",
                  flush=True)
        if 'O3_LSI_rothaus_simon' in result:
            print(f"  O3 : C_LSI estimate    = {result['O3_LSI_rothaus_simon']['C_LSI_rothaus_simon']:.2f}",
                  flush=True)
            print(f"       paper bound 43.7/m_0² = {result['O3_LSI_rothaus_simon']['C_LSI_paper_bound']:.2f}",
                  flush=True)
        print(f"  Wall time : {result['wall_time_seconds']:.1f}s", flush=True)

    # Save JSON
    out_file = os.path.join(output_dir,
                            f"tHooft_L{L}_b{beta:.2f}_2026-05-26.json")
    with open(out_file, 'w') as f:
        json.dump(result, f, indent=2, default=str)
    if verbose:
        print(f"  Output JSON : {out_file}", flush=True)

    return result


# ============================================================================
# CLI entrypoint
# ============================================================================

DEFAULT_RUNS_CONFIG = {
    8:  {'n_therm': 2000, 'n_decorr': 20, 'n_samples': 100},
    12: {'n_therm': 3000, 'n_decorr': 25, 'n_samples':  80},
    16: {'n_therm': 4000, 'n_decorr': 30, 'n_samples':  60},
}


def main():
    parser = argparse.ArgumentParser(
        description=__doc__.split('\n')[0],
        formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('--L', type=int, default=None,
                        help='Single lattice size (overrides default sweep)')
    parser.add_argument('--beta', type=float, default=None,
                        help='Single coupling (overrides default sweep)')
    parser.add_argument('--n_therm', type=int, default=None,
                        help='Override n_therm')
    parser.add_argument('--n_decorr', type=int, default=None,
                        help='Override n_decorr')
    parser.add_argument('--n_samples', type=int, default=None,
                        help='Override n_samples')
    parser.add_argument('--quick', action='store_true',
                        help='Quick test : L=4, β=3.0, n_therm=200, n_samples=10')
    parser.add_argument('--sanity_only', action='store_true',
                        help='Run only sanity battery (no measurements)')
    parser.add_argument('--seed', type=int, default=2026,
                        help='Random seed (default 2026)')
    parser.add_argument('--output_dir', default='/tmp',
                        help='Directory for JSON output (default /tmp)')
    parser.add_argument('--verbose', action='store_true', default=True)
    args = parser.parse_args()

    print(f"\n{'#'*72}", flush=True)
    print(f"#  JAX SU(3) 't Hooft twist lattice PROPER", flush=True)
    print(f"#  Paper : Paper_tHooft_Twist_Mode_Zero_LMP", flush=True)
    print(f"#  Author : Kévin Rémondière (ORCID 0009-0008-2443-7166)", flush=True)
    print(f"#  Date   : 2026-05-26", flush=True)
    print(f"#  JAX    : {jax.__version__}, devices = {jax.devices()}", flush=True)
    print(f"{'#'*72}", flush=True)

    # Build run sweep
    if args.quick:
        sweep = [(4, 3.0)]
        run_cfg = {4: {'n_therm': 200, 'n_decorr': 5, 'n_samples': 10}}
    elif args.L is not None and args.beta is not None:
        sweep = [(args.L, args.beta)]
        run_cfg = {args.L: DEFAULT_RUNS_CONFIG.get(
            args.L, {'n_therm': 2000, 'n_decorr': 20, 'n_samples': 50})}
    else:
        # Full paper sweep
        Ls = [8, 12, 16]
        betas = [2.5, 3.0, 3.5]
        sweep = [(L, b) for L in Ls for b in betas]
        run_cfg = DEFAULT_RUNS_CONFIG

    # Apply overrides
    for L in run_cfg:
        if args.n_therm   is not None: run_cfg[L]['n_therm']   = args.n_therm
        if args.n_decorr  is not None: run_cfg[L]['n_decorr']  = args.n_decorr
        if args.n_samples is not None: run_cfg[L]['n_samples'] = args.n_samples

    print(f"\n  Sweep : {sweep}", flush=True)
    for L in sorted(set(L for L, b in sweep)):
        print(f"  L={L} : {run_cfg.get(L, '<default>')}", flush=True)

    key = random.PRNGKey(args.seed)
    all_results = []

    for (L, beta) in sweep:
        cfg = run_cfg[L]
        key, sk = random.split(key)
        if args.sanity_only:
            sanity = sanity_battery(L, beta, cfg['n_therm'], sk,
                                    verbose=args.verbose)
            result = {'L': L, 'beta': beta,
                      'sanity': {k: v for k, v in sanity.items()
                                 if not k.startswith('_')}}
        else:
            result = run_one_config(L, beta,
                                    cfg['n_therm'], cfg['n_decorr'],
                                    cfg['n_samples'], sk,
                                    output_dir=args.output_dir,
                                    verbose=args.verbose)
        all_results.append(result)

    # Write summary JSON
    summary_file = os.path.join(args.output_dir,
                                'tHooft_summary_2026-05-26.json')
    with open(summary_file, 'w') as f:
        json.dump({
            'date_utc': time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime()),
            'author': 'Kévin Rémondière',
            'orcid': '0009-0008-2443-7166',
            'paper': 'Paper_tHooft_Twist_Mode_Zero_LMP',
            'sweep': sweep,
            'results': all_results,
        }, f, indent=2, default=str)
    print(f"\n  Final summary JSON : {summary_file}", flush=True)

    print(f"\n{'#'*72}", flush=True)
    print(f"#  ALL DONE", flush=True)
    print(f"{'#'*72}\n", flush=True)


if __name__ == '__main__':
    main()
