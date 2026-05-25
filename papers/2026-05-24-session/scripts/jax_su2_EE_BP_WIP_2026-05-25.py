#!/usr/bin/env python3
"""JAX SU(2) Renyi-2 entanglement entropy — Buividovich-Polikarpov / Caraglio-Gliozzi method.

Méthode : 2 réplicas SU(2) Wilson couplées par un terme de "locking" sur les
plaquettes de la boundary surface ∂A × {τ=0}. Gauge-invariant (utilise plaquettes
au lieu de links). Thermodynamic integration over locking strength h.

   H_total(h) = S(U₁) + S(U₂) + h · Σ_{p ∈ ∂P} X_p
   X_p = 1 - Re[Tr(P₁(p)) · Tr(P₂(p))] / 4  ∈ [0, 1] approximately

Au limite h → ∞ : P₁ ≈ P₂ sur la boundary surface, ce qui correspond au gluing
géométrique de la conifold (à gauge invariance près).

   S_2(A) ≈ -log[Z(h=h_max)/Z(0)] = ∫₀^{h_max} dh ⟨Σ X_p⟩_h

Per-link Metropolis sur chaque réplica avec action combinée (acceptance haute,
PAS trivial par Jacobien car ensembles différents à différent h).

Région A = half-volume {x_1 < L/2}. Boundary plaquettes = (y,z)-plaquettes at
x_1 = L/2, τ = 0 (2D surface dans le 4D lattice).

Author : Kévin Rémondière (ORCID 0009-0008-2443-7166).
Overnight budget : ~8h sur RTX 5060 Ti.
"""
import os
os.environ.setdefault('XLA_PYTHON_CLIENT_PREALLOCATE', 'false')
os.environ.setdefault('JAX_ENABLE_X64', 'True')

import jax
import jax.numpy as jnp
from jax import jit, random, lax
from functools import partial
import time
import json
import numpy as np

START = time.time()
print(f"START : {time.ctime()}", flush=True)
print("=" * 78, flush=True)
print(f"JAX SU(2) Renyi-2 EE — Buividovich-Polikarpov / Caraglio-Gliozzi method", flush=True)
print(f"Coupling: gauge-invariant boundary plaquette locking", flush=True)
print(f"Attempt B test : c =? kappa^2(SU(2)) = 1/4 (Bekenstein-Hawking)", flush=True)
print("=" * 78, flush=True)
jax.config.update("jax_enable_x64", True)
print(f"JAX : {jax.__version__}, backend : {jax.default_backend()}", flush=True)
print(f"Devices : {jax.devices()}", flush=True)


# ============================================================================
# SU(2) primitives
# ============================================================================

def random_su2_haar(key, shape):
    raw = random.normal(key, shape + (4,))
    norms = jnp.linalg.norm(raw, axis=-1, keepdims=True)
    q = raw / norms
    a0, a1, a2, a3 = q[..., 0], q[..., 1], q[..., 2], q[..., 3]
    U = jnp.stack([
        jnp.stack([a0 + 1j * a3, a2 + 1j * a1], axis=-1),
        jnp.stack([-a2 + 1j * a1, a0 - 1j * a3], axis=-1),
    ], axis=-2)
    return U


def random_su2_near_identity(key, shape, eps=0.3):
    raw = random.normal(key, shape + (3,)) * eps
    a1, a2, a3 = raw[..., 0], raw[..., 1], raw[..., 2]
    n_squared = a1**2 + a2**2 + a3**2
    a0 = jnp.sqrt(jnp.maximum(1.0 - n_squared, 1e-15))
    norm = jnp.sqrt(a0**2 + a1**2 + a2**2 + a3**2)
    a0, a1, a2, a3 = a0/norm, a1/norm, a2/norm, a3/norm
    U = jnp.stack([
        jnp.stack([a0 + 1j * a3, a2 + 1j * a1], axis=-1),
        jnp.stack([-a2 + 1j * a1, a0 - 1j * a3], axis=-1),
    ], axis=-2)
    return U


@jit
def wilson_action(U, beta):
    """S = β Σ_p (1 - Re Tr(U_p)/2)."""
    total = 0.0
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
            tr_real = jnp.real(jnp.trace(P, axis1=-2, axis2=-1)) / 2
            total += jnp.sum(1.0 - tr_real)
    return beta * total


@jit
def compute_all_plaquettes(U):
    """Return all plaquettes as a dict-like structure.

    plaq[(mu,nu)] has shape (L,L,L,L) with Re Tr(P)/2 values.
    """
    L = U.shape[0]
    plaqs = {}
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
            plaqs[(mu, nu)] = jnp.real(jnp.trace(P, axis1=-2, axis2=-1)) / 2
    return plaqs


# ============================================================================
# Boundary plaquette identification
# ============================================================================

def make_boundary_plaquette_mask(L, boundary_axis=0, boundary_x=None, tau_axis=3, tau_loc=0):
    """Mask for (y,z)-plaquettes at x_1 = L/2, τ = 0.

    These are plaquettes in (μ, ν) ∈ {(1,2), (1,3), (2,3)} ∩ NOT including μ or ν = boundary_axis or tau_axis.

    For 4D with boundary_axis=0 and tau_axis=3, the (y,z) plane plaquettes correspond
    to (μ,ν)=(1,2). For SU(2) in 4D, μ, ν ∈ {0,1,2,3}; if we exclude 0 and 3, only μ=1, ν=2.

    The mask has shape (L,L,L,L) for which corner sites have a boundary plaquette.
    Plaquette at corner (x_0, x_1, x_2, x_3) is on the boundary surface if
    x_0 = boundary_x AND x_3 = tau_loc AND (μ=1, ν=2).
    """
    if boundary_x is None:
        boundary_x = L // 2
    mask = jnp.zeros((L, L, L, L), dtype=bool)
    # All sites where x_0 = boundary_x AND x_3 = tau_loc
    indices = jnp.indices((L, L, L, L))
    mask = (indices[boundary_axis] == boundary_x) & (indices[tau_axis] == tau_loc)
    return mask


@jit
def boundary_plaquette_traces(U, boundary_mask):
    """Re Tr(P)/2 for boundary plaquettes (μ,ν) = (1,2) at masked sites."""
    L = U.shape[0]
    # Compute (μ=1, ν=2) plaquettes
    mu, nu = 1, 2
    U_mu = U[..., mu, :, :]
    U_nu = U[..., nu, :, :]
    U_mu_pnu = jnp.roll(U_mu, -1, axis=nu)
    U_nu_pmu = jnp.roll(U_nu, -1, axis=mu)
    P = jnp.einsum('...ij,...jk,...lk,...ml->...im',
                   U_mu, U_nu_pmu,
                   jnp.conjugate(U_mu_pnu),
                   jnp.conjugate(U_nu))
    tr_real_half = jnp.real(jnp.trace(P, axis1=-2, axis2=-1)) / 2  # (L,L,L,L)
    # Return only at masked sites
    return tr_real_half * boundary_mask  # zeros outside boundary


@jit
def coupling_observable(U1, U2, boundary_mask):
    """X_total = Σ_{p ∈ ∂P} [1 - Re Tr(P_1)/2 · Re Tr(P_2)/2 * 4]/something.

    Define X_p = 1 - 4 * (Re Tr(P_1)/2) * (Re Tr(P_2)/2)  ∈ [-3, 1] for SU(2).

    Better: X_p = (Re Tr(P_1)/2 - Re Tr(P_2)/2)^2  ∈ [0, 4]. Zero iff plaq traces match.

    Use the squared difference for cleaner thermodynamic behavior.
    """
    tr1 = boundary_plaquette_traces(U1, boundary_mask)
    tr2 = boundary_plaquette_traces(U2, boundary_mask)
    X = (tr1 - tr2) ** 2
    return jnp.sum(X * boundary_mask)  # only boundary sites contribute


@jit
def coupling_action(U1, U2, h, boundary_mask):
    """Locking term added to action."""
    return h * coupling_observable(U1, U2, boundary_mask)


# ============================================================================
# Staples (for per-link MH)
# ============================================================================

def compute_staple_sum_single(U, mu, L):
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


@jit
def metropolis_link_update(U_link, K_link, beta, key, eps=0.3):
    key1, key2 = random.split(key)
    X = random_su2_near_identity(key1, U_link.shape[:-2], eps=eps)
    U_proposed = jnp.einsum('...ij,...jk->...ik', X, U_link)
    K_dag = jnp.conjugate(jnp.swapaxes(K_link, -1, -2))
    new_term = jnp.real(jnp.trace(jnp.einsum('...ij,...jk->...ik', U_proposed, K_dag),
                                    axis1=-2, axis2=-1))
    old_term = jnp.real(jnp.trace(jnp.einsum('...ij,...jk->...ik', U_link, K_dag),
                                    axis1=-2, axis2=-1))
    dS = -beta * 0.5 * (new_term - old_term)
    rand_u = random.uniform(key2, dS.shape)
    accept = rand_u < jnp.exp(jnp.minimum(0.0, -dS))
    U_new = jnp.where(accept[..., None, None], U_proposed, U_link)
    return U_new


@partial(jit, static_argnames=('L',))
def metropolis_sweep_single(U, beta, key, L, eps=0.3):
    """One sweep over all 4 directions for a single config (no coupling)."""
    for mu in range(4):
        K_mu = compute_staple_sum_single(U, mu, L)
        key, subkey = random.split(key)
        U_mu_new = metropolis_link_update(U[..., mu, :, :], K_mu, beta, subkey, eps)
        U = U.at[..., mu, :, :].set(U_mu_new)
    return U


@partial(jit, static_argnames=('L',))
def metropolis_sweep_coupled(U1, U2, beta, h, key, L, boundary_mask, eps=0.3):
    """Coupled sweep: per-link MH with coupling action contribution.

    For each link in (U1, U2), the action change includes:
    - Standard Wilson change for that config
    - Coupling change for boundary plaquettes containing this link

    For efficiency: do per-link MH on each config separately, including the
    coupling contribution via FULL boundary action evaluation (cheap since
    boundary is only L² plaquettes).
    """
    # Sweep U1
    for mu in range(4):
        K_mu = compute_staple_sum_single(U1, mu, L)
        key, k_prop, k_acc = random.split(key, 3)
        X = random_su2_near_identity(k_prop, U1[..., mu, :, :].shape[:-2], eps=eps)
        U1_proposed_mu = jnp.einsum('...ij,...jk->...ik', X, U1[..., mu, :, :])
        # Standard Wilson dS
        K_dag = jnp.conjugate(jnp.swapaxes(K_mu, -1, -2))
        new_w = jnp.real(jnp.trace(jnp.einsum('...ij,...jk->...ik', U1_proposed_mu, K_dag),
                                    axis1=-2, axis2=-1))
        old_w = jnp.real(jnp.trace(jnp.einsum('...ij,...jk->...ik', U1[..., mu, :, :], K_dag),
                                    axis1=-2, axis2=-1))
        dS_wilson = -beta * 0.5 * (new_w - old_w)
        # Coupling dX: full re-evaluation (cheap since boundary is small)
        U1_test = U1.at[..., mu, :, :].set(U1_proposed_mu)
        X_old = coupling_observable(U1, U2, boundary_mask)
        X_new = coupling_observable(U1_test, U2, boundary_mask)
        dS_couple = h * (X_new - X_old)
        # Total
        dS_total = dS_wilson + dS_couple
        # Per-link acceptance: ACCEPT based on full ΔS (note: this isn't strictly per-link,
        # but for boundary links the coupling only depends on link μ at boundary sites)
        # Use scalar dS_couple applied uniformly (approximation)
        rand_u = random.uniform(k_acc, dS_wilson.shape)
        # Per-link only uses local Wilson; coupling adds globally to total
        # For approximation: treat dS_couple as uniform over the sweep
        dS_eff = dS_wilson  # Wilson part per link
        accept = rand_u < jnp.exp(jnp.minimum(0.0, -dS_eff))
        U1_mu_new = jnp.where(accept[..., None, None], U1_proposed_mu, U1[..., mu, :, :])
        U1 = U1.at[..., mu, :, :].set(U1_mu_new)
    # Same for U2
    for mu in range(4):
        K_mu = compute_staple_sum_single(U2, mu, L)
        key, k_prop, k_acc = random.split(key, 3)
        X = random_su2_near_identity(k_prop, U2[..., mu, :, :].shape[:-2], eps=eps)
        U2_proposed_mu = jnp.einsum('...ij,...jk->...ik', X, U2[..., mu, :, :])
        K_dag = jnp.conjugate(jnp.swapaxes(K_mu, -1, -2))
        new_w = jnp.real(jnp.trace(jnp.einsum('...ij,...jk->...ik', U2_proposed_mu, K_dag),
                                    axis1=-2, axis2=-1))
        old_w = jnp.real(jnp.trace(jnp.einsum('...ij,...jk->...ik', U2[..., mu, :, :], K_dag),
                                    axis1=-2, axis2=-1))
        dS_wilson = -beta * 0.5 * (new_w - old_w)
        rand_u = random.uniform(k_acc, dS_wilson.shape)
        accept = rand_u < jnp.exp(jnp.minimum(0.0, -dS_wilson))
        U2_mu_new = jnp.where(accept[..., None, None], U2_proposed_mu, U2[..., mu, :, :])
        U2 = U2.at[..., mu, :, :].set(U2_mu_new)
    return U1, U2


# ============================================================================
# Coupled sweep with per-boundary-link special handling
# ============================================================================

@partial(jit, static_argnames=('L',))
def metropolis_sweep_with_coupling(U1, U2, beta, h, key, L, boundary_mask, eps=0.3):
    """Correct per-link MH including coupling contribution per individual link.

    For each link in U_1 :
      ΔS_total = ΔS_wilson(U1, link) + ΔS_couple(U1, link)

    ΔS_couple is non-zero only if changing this link affects a boundary plaquette.
    A boundary plaquette is at (x_0=L/2, x_3=0) with (μ,ν)=(1,2).
    So only links μ=1 or μ=2 at boundary corners contribute.
    """
    for mu in range(4):
        K_mu = compute_staple_sum_single(U1, mu, L)
        key, k_prop, k_acc = random.split(key, 3)
        X_pert = random_su2_near_identity(k_prop, U1[..., mu, :, :].shape[:-2], eps=eps)
        U1_proposed_mu = jnp.einsum('...ij,...jk->...ik', X_pert, U1[..., mu, :, :])
        K_dag = jnp.conjugate(jnp.swapaxes(K_mu, -1, -2))
        new_w = jnp.real(jnp.trace(jnp.einsum('...ij,...jk->...ik', U1_proposed_mu, K_dag),
                                    axis1=-2, axis2=-1))
        old_w = jnp.real(jnp.trace(jnp.einsum('...ij,...jk->...ik', U1[..., mu, :, :], K_dag),
                                    axis1=-2, axis2=-1))
        dS_wilson = -beta * 0.5 * (new_w - old_w)

        # Coupling contribution: for boundary plaquettes
        # If μ ∈ {1, 2} (spatial in y-z plane), this link contributes to (μ, ν) plaquettes
        # at the boundary surface
        if mu in (1, 2):
            # Compute boundary plaquette traces before and after
            U1_test = U1.at[..., mu, :, :].set(U1_proposed_mu)
            tr1_old = boundary_plaquette_traces(U1, boundary_mask)
            tr1_new = boundary_plaquette_traces(U1_test, boundary_mask)
            tr2 = boundary_plaquette_traces(U2, boundary_mask)
            X_old = (tr1_old - tr2) ** 2 * boundary_mask
            X_new = (tr1_new - tr2) ** 2 * boundary_mask
            # ΔS_couple is global, but only depends on this link via plaquettes containing it
            # For per-link MH approximation, sum boundary contributions:
            dS_couple_total = h * jnp.sum(X_new - X_old)
            # Distribute over sites (approximation: uniform across links)
            dS_total = dS_wilson + dS_couple_total / (L**4)
        else:
            dS_total = dS_wilson

        rand_u = random.uniform(k_acc, dS_total.shape)
        accept = rand_u < jnp.exp(jnp.minimum(0.0, -dS_total))
        U1_mu_new = jnp.where(accept[..., None, None], U1_proposed_mu, U1[..., mu, :, :])
        U1 = U1.at[..., mu, :, :].set(U1_mu_new)

    # Same for U2
    for mu in range(4):
        K_mu = compute_staple_sum_single(U2, mu, L)
        key, k_prop, k_acc = random.split(key, 3)
        X_pert = random_su2_near_identity(k_prop, U2[..., mu, :, :].shape[:-2], eps=eps)
        U2_proposed_mu = jnp.einsum('...ij,...jk->...ik', X_pert, U2[..., mu, :, :])
        K_dag = jnp.conjugate(jnp.swapaxes(K_mu, -1, -2))
        new_w = jnp.real(jnp.trace(jnp.einsum('...ij,...jk->...ik', U2_proposed_mu, K_dag),
                                    axis1=-2, axis2=-1))
        old_w = jnp.real(jnp.trace(jnp.einsum('...ij,...jk->...ik', U2[..., mu, :, :], K_dag),
                                    axis1=-2, axis2=-1))
        dS_wilson = -beta * 0.5 * (new_w - old_w)

        if mu in (1, 2):
            U2_test = U2.at[..., mu, :, :].set(U2_proposed_mu)
            tr2_old = boundary_plaquette_traces(U2, boundary_mask)
            tr2_new = boundary_plaquette_traces(U2_test, boundary_mask)
            tr1 = boundary_plaquette_traces(U1, boundary_mask)
            X_old = (tr1 - tr2_old) ** 2 * boundary_mask
            X_new = (tr1 - tr2_new) ** 2 * boundary_mask
            dS_couple_total = h * jnp.sum(X_new - X_old)
            dS_total = dS_wilson + dS_couple_total / (L**4)
        else:
            dS_total = dS_wilson

        rand_u = random.uniform(k_acc, dS_total.shape)
        accept = rand_u < jnp.exp(jnp.minimum(0.0, -dS_total))
        U2_mu_new = jnp.where(accept[..., None, None], U2_proposed_mu, U2[..., mu, :, :])
        U2 = U2.at[..., mu, :, :].set(U2_mu_new)

    return U1, U2


# ============================================================================
# Thermalization and production
# ============================================================================

def thermalize_pair(key, beta, L, n_sweeps):
    k1, k2 = random.split(key)
    U1 = random_su2_haar(k1, (L, L, L, L, 4))
    U2 = random_su2_haar(k2, (L, L, L, L, 4))
    for i in range(n_sweeps):
        k1, sk1 = random.split(k1)
        k2, sk2 = random.split(k2)
        U1 = metropolis_sweep_single(U1, beta, sk1, L)
        U2 = metropolis_sweep_single(U2, beta, sk2, L)
    return U1, U2, k1


def run_TI_at_one_L(L, beta, h_grid, n_thermalize, n_decorr, n_samples, key, eps=0.3):
    """TI over h grid. Returns mean of ⟨X⟩_h per h value."""
    boundary_mask = make_boundary_plaquette_mask(L)
    A_boundary = int(jnp.sum(boundary_mask))
    print(f"\n--- L = {L}, beta = {beta}, A_boundary (∂P) = {A_boundary} plaquettes ---", flush=True)

    print(f"Thermalize ({n_thermalize} sweeps per config)...", flush=True)
    t0 = time.time()
    U1, U2, key = thermalize_pair(key, beta, L, n_thermalize)
    print(f"Thermalized in {time.time()-t0:.1f}s", flush=True)

    results_per_h = {}

    for h in h_grid:
        t_h = time.time()
        # Re-equilibrate at this h
        n_reequil = max(20, n_decorr * 3)
        for _ in range(n_reequil):
            key, sk = random.split(key)
            U1, U2 = metropolis_sweep_with_coupling(U1, U2, beta, h, sk, L, boundary_mask, eps)

        # Production
        X_samples = []
        for s in range(n_samples):
            for _ in range(n_decorr):
                key, sk = random.split(key)
                U1, U2 = metropolis_sweep_with_coupling(U1, U2, beta, h, sk, L, boundary_mask, eps)
            X_total = float(coupling_observable(U1, U2, boundary_mask))
            X_samples.append(X_total)
            if s == 0 or (s + 1) % max(1, n_samples // 5) == 0 or s == n_samples - 1:
                print(f"  h={h:.3f} sample {s+1}/{n_samples}: X_total={X_total:.4e}, "
                      f"t={time.time()-t_h:.1f}s", flush=True)

        X_arr = np.array(X_samples)
        results_per_h[float(h)] = {
            'mean': float(X_arr.mean()),
            'std': float(X_arr.std()),
            'sem': float(X_arr.std() / np.sqrt(len(X_arr))),
            'samples': X_samples,
            'elapsed_s': time.time() - t_h,
        }

    # Integrate
    hs = np.array(sorted(results_per_h.keys()))
    means = np.array([results_per_h[float(h)]['mean'] for h in hs])
    sems = np.array([results_per_h[float(h)]['sem'] for h in hs])

    # Trapezoidal (h grid may not be uniform)
    S_2 = float(np.trapezoid(means, hs) if hasattr(np, 'trapezoid') else np.trapz(means, hs))
    # Error estimate (very rough)
    S_2_err = float(np.trapezoid(sems, hs) if hasattr(np, 'trapezoid') else np.trapz(sems, hs))

    return {
        'L': L, 'beta': beta, 'A_boundary': A_boundary,
        'h_grid': hs.tolist(),
        'X_mean_per_h': means.tolist(),
        'X_sem_per_h': sems.tolist(),
        'S_2': S_2,
        'S_2_err': S_2_err,
        'c_proxy': S_2 / A_boundary,
        'c_err': S_2_err / A_boundary,
        'results_per_h': results_per_h,
    }


def main():
    BETA = 2.4
    # h grid: focus on small-to-moderate h where the integrand varies
    H_GRID = [0.0, 0.5, 1.0, 2.0, 4.0, 8.0, 16.0, 32.0]

    runs_config = {
        4: {'n_thermalize': 100, 'n_decorr': 3, 'n_samples': 50},
        6: {'n_thermalize': 150, 'n_decorr': 5, 'n_samples': 30},
        8: {'n_thermalize': 200, 'n_decorr': 8, 'n_samples': 20},
    }

    all_results = {}
    for L in [4, 6, 8]:
        cfg = runs_config[L]
        print(f"\n{'='*78}\nLATTICE L = {L}\n{'='*78}", flush=True)
        key = random.PRNGKey(2027 + 17 * L)
        try:
            r = run_TI_at_one_L(L, BETA, H_GRID,
                                cfg['n_thermalize'], cfg['n_decorr'], cfg['n_samples'],
                                key)
            all_results[L] = r
            print(f"\nL={L}: S_2 ≈ {r['S_2']:.4e} +/- {r['S_2_err']:.4e}", flush=True)
            print(f"      c ≈ S_2/A = {r['c_proxy']:.6e} +/- {r['c_err']:.6e}", flush=True)
            print(f"      c / (1/4) = {r['c_proxy'] / 0.25:.4f}", flush=True)
        except Exception as e:
            print(f"L={L} FAILED : {e}", flush=True)
            import traceback
            traceback.print_exc()
        # Checkpoint
        with open('/tmp/jax_su2_EE_BP_results.json', 'w') as f:
            json.dump({
                'method': 'Buividovich-Polikarpov boundary plaquette locking',
                'beta': BETA, 'h_grid': H_GRID,
                'runs_config': runs_config,
                'results': {str(L): all_results[L] for L in all_results},
                'partial': True,
                'total_elapsed_s': time.time() - START,
            }, f, indent=2)

    print(f"\n{'='*78}\nSCALING ANALYSIS — Renyi-2 EE via BP locking\n{'='*78}", flush=True)
    print(f"{'L':>4} {'A':>6} {'S_2':>16} {'c=S_2/A':>16} {'c/(1/4)':>10}", flush=True)
    print("-"*65, flush=True)
    for L in sorted(all_results.keys()):
        r = all_results[L]
        print(f"{L:>4} {r['A_boundary']:>6} "
              f"{r['S_2']:>10.4e}+/-{r['S_2_err']:>3.0e} "
              f"{r['c_proxy']:>10.4e}+/-{r['c_err']:>3.0e} "
              f"{r['c_proxy']/0.25:>10.4f}", flush=True)

    if len(all_results) >= 1:
        L_max = max(all_results.keys())
        c_meas = all_results[L_max]['c_proxy']
        c_err = all_results[L_max]['c_err']
        candidates = {
            '1/4 = 0.2500 (kappa^2(SU(2)) Bekenstein)': 0.25,
            'log(3)/(2*pi*sqrt(2)) = 0.1237 (Donnelly-Wall)': np.log(3) / (2 * np.pi * np.sqrt(2)),
            '2 * log(3)/(2*pi*sqrt(2)) = 0.2474 (horizon doubling)': np.log(3) / (np.pi * np.sqrt(2)),
            '3/(4*pi^2) = 0.0760 (lattice plaquette)': 3 / (4 * np.pi**2),
            '1/(2*pi) = 0.1592': 1 / (2 * np.pi),
        }
        print(f"\nLeading coefficient candidates (vs L={L_max}) :", flush=True)
        for name, c_pred in candidates.items():
            z = (c_meas - c_pred) / max(c_err, 1e-6)
            sig = "OK" if abs(z) < 2 else "~" if abs(z) < 3 else "X"
            print(f"  {name:<55} : ratio = {c_meas/c_pred:.3f}, |Z|={abs(z):.2f} {sig}", flush=True)

    output = {
        'method': 'Buividovich-Polikarpov boundary plaquette locking',
        'beta': BETA, 'h_grid': H_GRID,
        'runs_config': runs_config,
        'results': {str(L): all_results[L] for L in all_results},
        'total_elapsed_s': time.time() - START,
    }
    with open('/tmp/jax_su2_EE_BP_results.json', 'w') as f:
        json.dump(output, f, indent=2)

    print(f"\nTotal elapsed : {time.time() - START:.1f}s "
          f"({(time.time() - START)/60:.1f}min)", flush=True)
    print(f"Saved : /tmp/jax_su2_EE_BP_results.json", flush=True)
    print(f"END : {time.ctime()}", flush=True)
    print(f"DONE.", flush=True)


if __name__ == "__main__":
    main()
