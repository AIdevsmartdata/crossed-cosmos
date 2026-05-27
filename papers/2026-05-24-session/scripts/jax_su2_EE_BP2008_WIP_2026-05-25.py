#!/usr/bin/env python3
"""JAX SU(2) Renyi-2 entanglement entropy — Buividovich-Polikarpov 2008 conifold.

Vrai BP2008 (arXiv:0806.3376) : custom lattice topology via tying constraint.

Setup :
- Lattice doublé L^3 × 2L_τ avec PBC en τ (period 2L_τ)
- Region A = {x_1 < L/2} dans spatial volume
- Region B = complement
- B-region : hard constraint U(x ∈ B, τ+L_τ, μ) = U(x ∈ B, τ, μ) (period L_τ in B)
- A-region : soft penalty h · Σ_{x∈A, μ, τ ∈ [0, L_τ)} X(x, τ, μ)
  où X = 1 - Re Tr[U_μ(x, τ+L_τ) U_μ(x, τ)^†]/2  ∈ [0, 1]

Au limite h=0 : A entièrement libre → 2L_τ period dans A → conifold = Z_2
Au limite h→∞ : A tied → L_τ period partout → 2 indep copies = Z_1²

S_2 = -log(Z_2/Z_1²) = log(Z(h=∞)/Z(h=0)) = ∫₀^h_max dh ⟨Σ X⟩_h ≥ 0

Le constraint NE TRIVIALISE PAS par Jacobien : c'est une RESTRICTION sur l'espace
de mesure (DoF reduces from 2L_τ × |A| → L_τ × |A| at h=∞), pas un re-étiquetage.

Per-link MH sur le lattice doublé avec acceptance haute (proposal local).

Author : Kévin Rémondière (ORCID 0009-0008-2443-7166).
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
print(f"JAX SU(2) Renyi-2 EE — BP2008 conifold (doubled lattice + A-tying TI)", flush=True)
print(f"Attempt B : test c =? kappa^2(SU(2)) = 1/4 = Bekenstein-Hawking", flush=True)
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
def wilson_action_doubled(U, beta, L, L_tau_total):
    """Wilson action on doubled lattice L^3 x L_tau_total."""
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


# ============================================================================
# Region masks + tying
# ============================================================================

def make_region_A_site_mask(L, L_tau_total, A_axis=0):
    """Mask of sites in region A = {x_{A_axis} < L/2}."""
    indices = jnp.indices((L, L, L, L_tau_total))
    site_in_A = indices[A_axis] < L // 2  # shape (L,L,L,L_tau_total)
    return site_in_A


def make_region_A_link_mask(L, L_tau_total, A_axis=0):
    """Mask of links (x, τ, μ) where site x belongs to A.

    Returns shape (L, L, L, L_tau_total, 4) bool.
    """
    site_in_A = make_region_A_site_mask(L, L_tau_total, A_axis)  # (L,L,L,L_tau_total)
    link_in_A = jnp.broadcast_to(site_in_A[..., None], (L, L, L, L_tau_total, 4))
    return link_in_A


@partial(jit, static_argnames=('L_tau',))
def enforce_B_tying(U, L_tau, site_in_A):
    """Hard-tie B-region: U(x ∈ B, τ + L_tau, μ) = U(x ∈ B, τ, μ).

    Applied for τ ∈ [0, L_tau) → forces U at τ ∈ [L_tau, 2L_tau) to match.

    Mask of sites in B: ~site_in_A. For these sites, copy U[..., τ, :] to U[..., τ+L_tau, :].
    """
    # site_in_A : (L,L,L, 2L_tau)
    # We need: for τ ∈ [L_tau, 2L_tau) and x ∈ B, set U[x, τ] = U[x, τ - L_tau]
    L_tau_total = U.shape[3]
    # Build new array
    U_new = U
    U_first_half = U[..., :L_tau, :, :, :]  # (L,L,L,L_tau,4,2,2)
    # The "second half" we want to compute:
    site_in_A_first_half = site_in_A[..., :L_tau]  # (L,L,L,L_tau)
    site_in_B_first_half = ~site_in_A_first_half
    # For B sites: second half = first half
    # For A sites: keep current second half
    U_second_orig = U[..., L_tau:, :, :, :]
    mask_b = site_in_B_first_half[..., None, None, None]
    U_second_new = jnp.where(mask_b, U_first_half, U_second_orig)
    U_new = jnp.concatenate([U_first_half, U_second_new], axis=3)
    return U_new


@partial(jit, static_argnames=('L_tau',))
def tying_observable(U, L_tau, site_in_A):
    """Compute Σ_{x∈A, μ, τ ∈ [0, L_tau)} [1 - Re Tr(U(x, τ+L_tau, μ) · U(x, τ, μ)^†)/2].

    This is the integrand for thermodynamic integration over A-tying coupling h.
    """
    L_tau_total = U.shape[3]
    U_first = U[..., :L_tau, :, :, :]   # (L,L,L,L_tau,4,2,2)
    U_second = U[..., L_tau:, :, :, :]  # (L,L,L,L_tau,4,2,2)
    site_in_A_first = site_in_A[..., :L_tau]  # (L,L,L,L_tau)
    # Compute U_second · U_first^†
    U_first_dag = jnp.conjugate(jnp.swapaxes(U_first, -1, -2))
    prod = jnp.einsum('...ij,...jk->...ik', U_second, U_first_dag)  # (L,L,L,L_tau,4,2,2)
    tr_real = jnp.real(jnp.trace(prod, axis1=-2, axis2=-1)) / 2  # (L,L,L,L_tau,4)
    X = 1.0 - tr_real  # (L,L,L,L_tau,4) ∈ [0, 2]
    # Mask: only A sites
    mask = site_in_A_first[..., None]  # (L,L,L,L_tau,1) → broadcast to (..., 4)
    X_masked = X * mask
    return jnp.sum(X_masked)


@partial(jit, static_argnames=('L_tau',))
def tying_observable_per_link_change(U_old, U_new, mu_index, axis_index, target_idx,
                                       L_tau, site_in_A):
    """Compute ΔX from a single link update (lighter than full re-eval).

    Not used in current implementation (we use full re-eval for simplicity).
    """
    return tying_observable(U_new, L_tau, site_in_A) - tying_observable(U_old, L_tau, site_in_A)


# ============================================================================
# Per-link Metropolis with full action evaluation
# ============================================================================

def compute_staple_sum_doubled(U, mu, L, L_tau_total):
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


@partial(jit, static_argnames=('L', 'L_tau'))
def metropolis_sweep_with_tying(U, beta, h, key, L, L_tau, site_in_A, eps=0.3):
    """One sweep over all links, with:
    - Wilson action via standard staples
    - For x ∈ A: additional tying penalty term per link
    - For x ∈ B: hard tying (just copy after each link update)

    The tying penalty for A-links at (x, τ, μ) where τ ∈ [0, L_tau):
      penalty = h · (1 - Re Tr[U(x, τ+L_tau, μ) · U(x, τ, μ)^†] / 2)
    Similarly for τ ∈ [L_tau, 2L_tau): penalty involves U at τ - L_tau.
    """
    L_tau_total = U.shape[3]
    site_in_B = ~site_in_A
    site_in_A_link = jnp.broadcast_to(site_in_A[..., None], U[..., 0, :, :].shape[:-2] + (4,))
    site_in_B_link = jnp.broadcast_to(site_in_B[..., None], U[..., 0, :, :].shape[:-2] + (4,))

    for mu in range(4):
        K_mu = compute_staple_sum_doubled(U, mu, L, L_tau_total)
        key, k_prop, k_acc = random.split(key, 3)
        X_pert = random_su2_near_identity(k_prop, U[..., mu, :, :].shape[:-2], eps=eps)
        U_proposed_mu = jnp.einsum('...ij,...jk->...ik', X_pert, U[..., mu, :, :])

        # Wilson action change per link
        # FIX 2026-05-25: K_mu bug removed (Re Tr(U·K) ≠ Re Tr(U·K†) for SU(2))
        new_w = jnp.real(jnp.trace(jnp.einsum('...ij,...jk->...ik', U_proposed_mu, K_mu),
                                    axis1=-2, axis2=-1))
        old_w = jnp.real(jnp.trace(jnp.einsum('...ij,...jk->...ik', U[..., mu, :, :], K_mu),
                                    axis1=-2, axis2=-1))
        dS_wilson = -beta * 0.5 * (new_w - old_w)

        # Tying penalty change per link (for A-region only)
        # For τ ∈ [0, L_tau), this link's tying partner is at τ + L_tau (in A only)
        # For τ ∈ [L_tau, 2L_tau), this link's tying partner is at τ - L_tau (in A only)
        # Compute U_partner for each τ:
        # Build shifted U along τ axis by L_tau (i.e., roll by L_tau)
        U_mu_partner = jnp.roll(U[..., mu, :, :], -L_tau, axis=3)  # (L,L,L,L_tau_total,2,2)
        # X_old = 1 - Re Tr[U_old · U_partner^†] / 2 (per link)
        partner_dag_old = jnp.conjugate(jnp.swapaxes(U_mu_partner, -1, -2))
        tr_old = jnp.real(jnp.trace(jnp.einsum('...ij,...jk->...ik',
                                                 U[..., mu, :, :], partner_dag_old),
                                      axis1=-2, axis2=-1)) / 2
        tr_new = jnp.real(jnp.trace(jnp.einsum('...ij,...jk->...ik',
                                                 U_proposed_mu, partner_dag_old),
                                      axis1=-2, axis2=-1)) / 2
        X_old_perlink = 1.0 - tr_old
        X_new_perlink = 1.0 - tr_new
        dX_perlink = X_new_perlink - X_old_perlink  # (L,L,L,L_tau_total)
        # Active only for A-region links
        site_in_A_link_mu = site_in_A_link[..., mu]  # (L,L,L,L_tau_total)
        dS_tying = h * dX_perlink * site_in_A_link_mu

        dS_total = dS_wilson + dS_tying

        rand_u = random.uniform(k_acc, dS_total.shape)
        accept = rand_u < jnp.exp(jnp.minimum(0.0, -dS_total))
        U_mu_new = jnp.where(accept[..., None, None], U_proposed_mu, U[..., mu, :, :])
        U = U.at[..., mu, :, :].set(U_mu_new)

        # Enforce B-tying after each link update
        U = enforce_B_tying(U, L_tau, site_in_A)

    return U


# ============================================================================
# Thermalization at h=0 (B-tied, A-free)
# ============================================================================

def thermalize(key, beta, L, L_tau, n_sweeps, site_in_A, eps=0.3):
    """Hot start with B-tying enforced, A free."""
    L_tau_total = 2 * L_tau
    k, sk = random.split(key)
    U = random_su2_haar(sk, (L, L, L, L_tau_total, 4))
    U = enforce_B_tying(U, L_tau, site_in_A)
    for i in range(n_sweeps):
        k, sk = random.split(k)
        U = metropolis_sweep_with_tying(U, beta, 0.0, sk, L, L_tau, site_in_A, eps)
    return U, k


# ============================================================================
# TI run
# ============================================================================

def run_TI_one_L(L, L_tau, beta, h_grid, n_thermalize, n_decorr, n_samples, key, eps=0.3):
    L_tau_total = 2 * L_tau
    site_in_A = make_region_A_site_mask(L, L_tau_total, A_axis=0)
    n_A_sites_first_half = int(jnp.sum(site_in_A[..., :L_tau]))
    A_boundary = (L // 2) * L * L  # |A| = L/2 * L * L spatial sites
    boundary_area = L * L  # ∂A = (y,z) plane at x=L/2

    print(f"\n--- L = {L}, L_tau = {L_tau} (doubled to {L_tau_total}), beta = {beta} ---", flush=True)
    print(f"    |A| = {A_boundary} spatial sites x L_tau = {A_boundary*L_tau} A-links per direction", flush=True)
    print(f"    Boundary area ∂A = {boundary_area} (in y-z plane at x=L/2)", flush=True)

    print(f"Thermalize ({n_thermalize} sweeps at h=0)...", flush=True)
    t0 = time.time()
    U, key = thermalize(key, beta, L, L_tau, n_thermalize, site_in_A, eps)
    print(f"Thermalized in {time.time()-t0:.1f}s", flush=True)

    results_per_h = {}

    for h in h_grid:
        t_h = time.time()
        # Re-equilibrate at this h
        n_reequil = max(20, n_decorr * 3)
        for _ in range(n_reequil):
            key, sk = random.split(key)
            U = metropolis_sweep_with_tying(U, beta, h, sk, L, L_tau, site_in_A, eps)

        # Production
        X_samples = []
        for s in range(n_samples):
            for _ in range(n_decorr):
                key, sk = random.split(key)
                U = metropolis_sweep_with_tying(U, beta, h, sk, L, L_tau, site_in_A, eps)
            X = float(tying_observable(U, L_tau, site_in_A))
            X_samples.append(X)
            if s == 0 or (s + 1) % max(1, n_samples // 5) == 0 or s == n_samples - 1:
                print(f"  h={h:.3f} sample {s+1}/{n_samples}: X={X:.4e}, "
                      f"t={time.time()-t_h:.1f}s", flush=True)

        X_arr = np.array(X_samples)
        results_per_h[float(h)] = {
            'mean': float(X_arr.mean()),
            'std': float(X_arr.std()),
            'sem': float(X_arr.std() / np.sqrt(len(X_arr))),
            'samples': X_samples,
            'elapsed_s': time.time() - t_h,
        }

    # Integrate ∫₀^h_max ⟨X⟩_h dh
    hs = np.array(sorted(results_per_h.keys()))
    means = np.array([results_per_h[float(h)]['mean'] for h in hs])
    sems = np.array([results_per_h[float(h)]['sem'] for h in hs])

    trap_fn = np.trapezoid if hasattr(np, 'trapezoid') else np.trapz
    S_2_full = float(trap_fn(means, hs))  # ∫₀^h_max ⟨X⟩ dh
    S_2_err = float(trap_fn(sems, hs))

    # Multiple area normalizations (different conventions)
    A_4D_surface = L * L * 2 * L_tau  # full 3D boundary surface in doubled lattice
    A_2D_perp = L * L  # 2D area perpendicular to time (standard EE convention)
    A_3D_with_tau = L * L * L_tau  # 3D area at fixed time-slice in doubled

    return {
        'L': L, 'L_tau': L_tau, 'beta': beta,
        'A_sites': int(A_boundary),
        'boundary_area_2D_perp': A_2D_perp,
        'boundary_area_3D_with_tau': A_3D_with_tau,
        'boundary_area_4D_surface': A_4D_surface,
        'h_grid': hs.tolist(),
        'X_mean_per_h': means.tolist(),
        'X_sem_per_h': sems.tolist(),
        'S_2': S_2_full,
        'S_2_err': S_2_err,
        'c_per_2D_area': S_2_full / A_2D_perp,
        'c_per_3D_area': S_2_full / A_3D_with_tau,
        'c_per_4D_surface': S_2_full / A_4D_surface,
        'c_per_lattice_area': S_2_full / A_2D_perp,  # backward compat
        'c_per_lattice_area_err': S_2_err / A_2D_perp,
        'results_per_h': results_per_h,
    }


def main():
    BETA = 2.4
    # h grid : extend to high h so integrand converges to 0
    H_GRID = [0.0, 0.25, 0.5, 1.0, 2.0, 4.0, 8.0, 16.0, 32.0, 64.0, 128.0]

    runs_config = {
        4:  {'L_tau': 4, 'n_thermalize': 200, 'n_decorr': 5,  'n_samples': 200},
        6:  {'L_tau': 6, 'n_thermalize': 300, 'n_decorr': 8,  'n_samples': 100},
        8:  {'L_tau': 8, 'n_thermalize': 400, 'n_decorr': 10, 'n_samples': 50},
        12: {'L_tau': 8, 'n_thermalize': 500, 'n_decorr': 15, 'n_samples': 20},
    }

    all_results = {}
    for L in [4, 6, 8, 12]:
        cfg = runs_config[L]
        print(f"\n{'='*78}\nLATTICE L = {L}, L_tau = {cfg['L_tau']}\n{'='*78}", flush=True)
        key = random.PRNGKey(2028 + 19 * L)
        try:
            r = run_TI_one_L(L, cfg['L_tau'], BETA, H_GRID,
                             cfg['n_thermalize'], cfg['n_decorr'], cfg['n_samples'],
                             key)
            all_results[L] = r
            print(f"\nL={L}: S_2 = {r['S_2']:.4e} +/- {r['S_2_err']:.4e}", flush=True)
            print(f"      c = S_2/A_boundary = {r['c_per_lattice_area']:.6e} "
                  f"+/- {r['c_per_lattice_area_err']:.6e}", flush=True)
            print(f"      c / (1/4) = {r['c_per_lattice_area'] / 0.25:.4f}", flush=True)
        except Exception as e:
            print(f"L={L} FAILED : {e}", flush=True)
            import traceback
            traceback.print_exc()
        # Checkpoint
        with open('/tmp/jax_su2_EE_BP2008_results.json', 'w') as f:
            json.dump({
                'method': 'BP2008 conifold via doubled lattice + A-tying TI',
                'beta': BETA, 'h_grid': H_GRID,
                'runs_config': runs_config,
                'results': {str(L): all_results[L] for L in all_results},
                'partial': True,
                'total_elapsed_s': time.time() - START,
            }, f, indent=2)

    print(f"\n{'='*78}\nSCALING ANALYSIS — Renyi-2 EE via BP2008 conifold\n{'='*78}", flush=True)
    print(f"{'L':>4} {'A_bound':>8} {'S_2':>16} {'c=S_2/A':>16} {'c/(1/4)':>10}", flush=True)
    print("-"*65, flush=True)
    for L in sorted(all_results.keys()):
        r = all_results[L]
        print(f"{L:>4} {r['boundary_area_lattice']:>8} "
              f"{r['S_2']:>10.4e}+/-{r['S_2_err']:>3.0e} "
              f"{r['c_per_lattice_area']:>10.4e}+/-{r['c_per_lattice_area_err']:>3.0e} "
              f"{r['c_per_lattice_area']/0.25:>10.4f}", flush=True)

    if len(all_results) >= 1:
        L_max = max(all_results.keys())
        c_meas = all_results[L_max]['c_per_lattice_area']
        c_err = all_results[L_max]['c_per_lattice_area_err']
        candidates = {
            '1/4 = 0.2500 (kappa^2(SU(2)) Bekenstein)': 0.25,
            'log(3)/(2*pi*sqrt(2)) = 0.1237 (Donnelly-Wall)': np.log(3) / (2 * np.pi * np.sqrt(2)),
            '2 * log(3)/(2*pi*sqrt(2)) = 0.2474 (horizon doubling)': np.log(3) / (np.pi * np.sqrt(2)),
            '3/(4*pi^2) = 0.0760 (lattice plaquette)': 3 / (4 * np.pi**2),
            '1/(2*pi) = 0.1592': 1 / (2 * np.pi),
            '1/12 = 0.0833 (CFT)': 1/12,
        }
        print(f"\nLeading coefficient candidates (vs L={L_max}) :", flush=True)
        for name, c_pred in candidates.items():
            z = (c_meas - c_pred) / max(c_err, 1e-6)
            sig = "OK" if abs(z) < 2 else "~" if abs(z) < 3 else "X"
            print(f"  {name:<55} : ratio = {c_meas/c_pred:.3f}, |Z|={abs(z):.2f} {sig}", flush=True)

    output = {
        'method': 'BP2008 conifold via doubled lattice + A-tying TI',
        'beta': BETA, 'h_grid': H_GRID,
        'runs_config': runs_config,
        'results': {str(L): all_results[L] for L in all_results},
        'total_elapsed_s': time.time() - START,
    }
    with open('/tmp/jax_su2_EE_BP2008_results.json', 'w') as f:
        json.dump(output, f, indent=2)

    print(f"\nTotal elapsed : {time.time() - START:.1f}s "
          f"({(time.time() - START)/60:.1f}min "
          f"= {(time.time() - START)/3600:.2f}h)", flush=True)
    print(f"Saved : /tmp/jax_su2_EE_BP2008_results.json", flush=True)
    print(f"END : {time.ctime()}", flush=True)
    print(f"DONE.", flush=True)


if __name__ == "__main__":
    main()
