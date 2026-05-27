#!/usr/bin/env python3
"""JAX SU(2) Renyi-2 EE — BP2008b CORRECT method (1 lattice deformed connectivity).

Référence : Buividovich-Polikarpov 2008b arXiv:0802.4247 (SU(2) numérique)
Modern state-of-art : Rabenstein 2019 arXiv:1812.04279 (C(SU(2)) ≈ 0.054)
Anti-BAR : Rindlisbacher 2022 arXiv:2211.00425 §3 (BAR overlap problem documented)

# Architecture

Un SEUL lattice L³ × 2T avec connectivité temporelle déformée :
- Region A (x_0 < L/2) : temporal links wrap sur 2T (continuous)
- Region Ā (x_0 ≥ L/2) : temporal links wrap sur T (2 indep copies de T)
- α ∈ [0,1] : interpolation continue
  - α=0 : tout en période T → 2 indep copies → Z_1²
  - α=1 : A en période 2T → conifold → Z_2

# Action

Standard Wilson action sur le lattice déformé. Les plaquettes "junction"
(impliquant un temporal link wrapping à t=T-1 ou t=2T-1) sont interpolées :

  contribution_junction(α) = (1-α) · (1 - tr(P_T_period)/2)
                            + α · (1 - tr(P_2T_period)/2)

# Estimateur

S_2 = ∫₀¹ dα ⟨∂S/∂α⟩_α

où ⟨∂S/∂α⟩_α = β · Σ_{junction in A} [tr(P_T)/2 - tr(P_2T)/2]
   sur configurations sampled de exp(-S(α))

# Pourquoi ça marche (vs anciens fails)

- Phase space IDENTIQUE entre α=0 et α=1 (mêmes link variables, juste
  connectivité interpolée)
- Pas de cross-sheet plaquettes, pas de mix U_1/U_2
- Pas de DoF "libre" (Haar) qui biaise l'évaluation
- α-intégration smooth → pas d'overlap problem (vs BAR)
- Rindlisbacher 2022 §3 documente l'overlap problem de BAR : confirmé

Author : Kévin Rémondière (ORCID 0009-0008-2443-7166).
"""
import os
os.environ.setdefault('XLA_PYTHON_CLIENT_PREALLOCATE', 'false')
os.environ.setdefault('JAX_ENABLE_X64', 'True')

import jax
import jax.numpy as jnp
from jax import jit, random
from functools import partial
import time
import json
import numpy as np

START = time.time()
print(f"START : {time.ctime()}", flush=True)
print("=" * 78, flush=True)
print(f"JAX SU(2) Renyi-2 EE — BP2008b CORRECT (1 lattice deformed + α-integration)", flush=True)
print(f"Ref: arXiv:0802.4247 (BP2008b), Rabenstein 2019 arXiv:1812.04279", flush=True)
print(f"Anti-BAR: Rindlisbacher 2022 arXiv:2211.00425 §3 (overlap problem)", flush=True)
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


# ============================================================================
# Deformed temporal connectivity
# ============================================================================

def make_deformed_next_t(T_half, A_spatial_mask):
    """For each spatial site, return the "next t" array of shape (2T,).

    Conventions :
    - For x ∈ Ā : period T within each half block
        t ∈ [0, T-1]: next = (t+1) mod T (within first half)
        t ∈ [T, 2T-1]: next = T + ((t-T+1) mod T) (within second half)
    - For x ∈ A : period 2T (standard)
        t ∈ [0, 2T-1]: next = (t+1) mod 2T

    Returns array of shape (L, L, L, 2T) giving next-t per (x, t).
    """
    L = A_spatial_mask.shape[0]
    twoT = 2 * T_half
    # Period-2T (standard) connectivity
    next_t_2T = jnp.array([(t + 1) % twoT for t in range(twoT)])  # (2T,)
    # Period-T (split) connectivity
    next_t_T = jnp.array([
        (t + 1) % T_half if t < T_half
        else T_half + ((t - T_half + 1) % T_half)
        for t in range(twoT)
    ])  # (2T,)
    # Broadcast: for each (x, t), pick the right connectivity
    # Output shape (L, L, L, 2T)
    A_4d = jnp.broadcast_to(A_spatial_mask[..., None], (L, L, L, twoT))
    next_t_2T_4d = jnp.broadcast_to(next_t_2T[None, None, None, :], (L, L, L, twoT))
    next_t_T_4d = jnp.broadcast_to(next_t_T[None, None, None, :], (L, L, L, twoT))
    next_t_eff = jnp.where(A_4d, next_t_2T_4d, next_t_T_4d)  # (L,L,L,2T)
    return next_t_2T_4d, next_t_T_4d, next_t_eff


# ============================================================================
# Wilson action with deformed temporal connectivity + α interpolation
# ============================================================================

@partial(jit, static_argnames=('L', 'T_half'))
def wilson_action_deformed(U, beta, alpha, L, T_half, A_spatial_mask):
    """Wilson action on deformed lattice with α interpolation.

    For non-junction plaquettes: standard Wilson.
    For junction plaquettes (involving temporal link at t=T-1 or t=2T-1) in A:
      contribution = (1-α) · (1 - tr(P_T_period)/2) + α · (1 - tr(P_2T_period)/2)
    For junction plaquettes in Ā: just period-T (unchanged).

    Returns: S(α)
    """
    twoT = 2 * T_half
    next_t_2T_4d, next_t_T_4d, next_t_eff = make_deformed_next_t(T_half, A_spatial_mask)
    # next_t_eff has the "true" connectivity (mixed A/Ā) for non-interpolation parts

    total = 0.0

    # Pure spatial plaquettes (μ, ν ∈ {0,1,2}): standard, no τ involvement
    for mu in range(3):
        for nu in range(mu+1, 3):
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

    # Mixed plaquettes (μ_s ∈ {0,1,2}, ν=τ=3):
    # P(x, t, μ_s, τ) = U_μ_s(x, t) · U_τ(x+e_μ_s, t) · U_μ_s(x, next_t)^† · U_τ(x, t)^†
    # The "next_t" depends on (x, t) for A vs Ā connectivity
    nu = 3  # temporal
    U_nu = U[..., nu, :, :]  # (L, L, L, 2T, 2, 2)

    for mu in range(3):
        U_mu = U[..., mu, :, :]  # (L, L, L, 2T, 2, 2)
        # U_τ at (x+e_μ_s, t)
        U_nu_pmu = jnp.roll(U_nu, -1, axis=mu)  # (L, L, L, 2T, 2, 2)

        # We need U_μ_s at (x, next_t(x, t)) — gather along τ axis using next_t_eff
        # For each (x, t), get U_mu[x, next_t_eff[x, t]]
        # Use jnp.take_along_axis
        def gather_along_t(arr, next_t):
            """arr shape (..., L, L, L, 2T, 2, 2), next_t shape (L, L, L, 2T)."""
            # Reshape next_t to broadcast as index
            idx = next_t[..., None, None]  # (L, L, L, 2T, 1, 1)
            idx_b = jnp.broadcast_to(idx, next_t.shape + (2, 2))
            return jnp.take_along_axis(arr, idx_b, axis=3)

        # Period-T connectivity for the spatial link at "next_t" (the modified one)
        U_mu_at_nextT = gather_along_t(U_mu, next_t_T_4d)  # (L, L, L, 2T, 2, 2)
        # Period-2T connectivity
        U_mu_at_next2T = gather_along_t(U_mu, next_t_2T_4d)

        # Compute both plaquette variants
        P_T_form = jnp.einsum('...ij,...jk,...lk,...ml->...im',
                               U_mu, U_nu_pmu,
                               jnp.conjugate(U_mu_at_nextT),
                               jnp.conjugate(U_nu))
        tr_T = jnp.real(jnp.trace(P_T_form, axis1=-2, axis2=-1)) / 2

        P_2T_form = jnp.einsum('...ij,...jk,...lk,...ml->...im',
                                U_mu, U_nu_pmu,
                                jnp.conjugate(U_mu_at_next2T),
                                jnp.conjugate(U_nu))
        tr_2T = jnp.real(jnp.trace(P_2T_form, axis1=-2, axis2=-1)) / 2

        # Junction times: t = T-1 or t = 2T-1
        junction_mask_t = jnp.zeros(twoT, dtype=bool)
        junction_mask_t = junction_mask_t.at[T_half - 1].set(True)
        junction_mask_t = junction_mask_t.at[twoT - 1].set(True)
        junction_mask_4d = jnp.broadcast_to(junction_mask_t[None, None, None, :], (L, L, L, twoT))

        # A_mask : spatial sites in A. Broadcast to time.
        A_4d = jnp.broadcast_to(A_spatial_mask[..., None], (L, L, L, twoT))

        # For non-junction times: use period-T (= same as period-2T at non-wraparound)
        # Actually at non-junction times, T-period and 2T-period give same next_t = t+1
        # So tr_T = tr_2T at non-junction times. Use either; choose tr_T.

        # At junction times:
        # - For Ā sites: use period-T only (no interpolation), contribution = 1 - tr_T/2
        # - For A sites: interpolate, contribution = (1-α)·(1-tr_T/2) + α·(1-tr_2T/2)

        is_junction = junction_mask_4d
        is_A = A_4d

        # Contribution per plaquette
        # Standard (non-junction): 1 - tr_T/2  (= 1 - tr_2T/2 since they agree)
        # Junction Ā: 1 - tr_T/2
        # Junction A: (1-α)·(1-tr_T/2) + α·(1-tr_2T/2) = 1 - ((1-α)·tr_T + α·tr_2T)/2

        contrib_non_junction = 1.0 - tr_T  # (using tr_T since they agree off-junction)
        contrib_junction_Abar = 1.0 - tr_T
        contrib_junction_A = 1.0 - ((1.0 - alpha) * tr_T + alpha * tr_2T)

        # Combine via masks
        contrib = jnp.where(
            is_junction,
            jnp.where(is_A, contrib_junction_A, contrib_junction_Abar),
            contrib_non_junction
        )

        total += jnp.sum(contrib)

    return beta * total


@partial(jit, static_argnames=('L', 'T_half'))
def alpha_observable(U, beta, L, T_half, A_spatial_mask):
    """⟨∂S/∂α⟩ observable: sum over A junction plaquettes of β·(tr_T - tr_2T)/2.

    Actually : ∂S/∂α = β · Σ [(1-tr_2T/2) - (1-tr_T/2)] · indicator(A junction)
                      = β · Σ [tr_T - tr_2T]/2 · indicator(A junction)

    Note : in the action, contribution = 1 - ((1-α)tr_T + α tr_2T)/2
           ∂(contribution)/∂α = (tr_T - tr_2T)/2  [no: -(tr_2T - tr_T)/2 = (tr_T - tr_2T)/2]

    Wait: let me recompute. contribution(α) = 1 - ((1-α)tr_T + α tr_2T)/2
          = 1 - tr_T/2 + α·(tr_T - tr_2T)/2

    ∂(contribution)/∂α = (tr_T - tr_2T)/2

    So ∂S/∂α = β · Σ_{A junction} (tr_T - tr_2T)/2  (per plaquette)
            = (β/2) · Σ_{A junction} (tr_T - tr_2T)
    """
    twoT = 2 * T_half
    next_t_2T_4d, next_t_T_4d, _ = make_deformed_next_t(T_half, A_spatial_mask)

    total = 0.0
    nu = 3
    U_nu = U[..., nu, :, :]

    for mu in range(3):
        U_mu = U[..., mu, :, :]
        U_nu_pmu = jnp.roll(U_nu, -1, axis=mu)

        def gather_along_t(arr, next_t):
            idx = next_t[..., None, None]
            idx_b = jnp.broadcast_to(idx, next_t.shape + (2, 2))
            return jnp.take_along_axis(arr, idx_b, axis=3)

        U_mu_at_nextT = gather_along_t(U_mu, next_t_T_4d)
        U_mu_at_next2T = gather_along_t(U_mu, next_t_2T_4d)

        P_T_form = jnp.einsum('...ij,...jk,...lk,...ml->...im',
                               U_mu, U_nu_pmu,
                               jnp.conjugate(U_mu_at_nextT),
                               jnp.conjugate(U_nu))
        tr_T = jnp.real(jnp.trace(P_T_form, axis1=-2, axis2=-1)) / 2

        P_2T_form = jnp.einsum('...ij,...jk,...lk,...ml->...im',
                                U_mu, U_nu_pmu,
                                jnp.conjugate(U_mu_at_next2T),
                                jnp.conjugate(U_nu))
        tr_2T = jnp.real(jnp.trace(P_2T_form, axis1=-2, axis2=-1)) / 2

        # Junction times AND A sites
        junction_mask_t = jnp.zeros(twoT, dtype=bool)
        junction_mask_t = junction_mask_t.at[T_half - 1].set(True)
        junction_mask_t = junction_mask_t.at[twoT - 1].set(True)
        junction_mask_4d = jnp.broadcast_to(junction_mask_t[None, None, None, :],
                                             (U.shape[0], U.shape[1], U.shape[2], twoT))
        A_4d = jnp.broadcast_to(A_spatial_mask[..., None],
                                  (U.shape[0], U.shape[1], U.shape[2], twoT))
        mask_A_junction = junction_mask_4d & A_4d

        # Note: tr_T - tr_2T can be ± , depending on configs. We expect ⟨tr_T - tr_2T⟩ < 0
        # because at α=0 (sampling Z_1²), tr_T values are thermalized (positive),
        # tr_2T are "off-equilibrium" (smaller), so tr_T > tr_2T → ∂S/∂α > 0.
        # At α=1 (Z_2), it's the opposite (tr_2T > tr_T).
        dS_per_plaq = (tr_T - tr_2T)
        total += jnp.sum(dS_per_plaq * mask_A_junction)

    return (beta / 2.0) * total  # /2 because of the action formula


# ============================================================================
# Per-link Metropolis (full action eval, slow but correct)
# ============================================================================

@partial(jit, static_argnames=('L', 'T_half'))
def metropolis_sweep_global(U, beta, alpha, key, L, T_half, A_spatial_mask, eps=0.05):
    """Global proposal sweep with full action evaluation.

    Slower than per-link but simpler. Use small eps for reasonable acceptance.
    """
    key1, key2, key3 = random.split(key, 3)
    X = random_su2_near_identity(key1, U.shape[:-2], eps=eps)
    U_proposed = jnp.einsum('...ij,...jk->...ik', X, U)
    S_old = wilson_action_deformed(U, beta, alpha, L, T_half, A_spatial_mask)
    S_new = wilson_action_deformed(U_proposed, beta, alpha, L, T_half, A_spatial_mask)
    dS = S_new - S_old
    rand_u = random.uniform(key2)
    accept = rand_u < jnp.exp(jnp.minimum(0.0, -dS))
    U_out = jnp.where(accept, U_proposed, U)
    return U_out, accept


@partial(jit, static_argnames=('L', 'T_half'))
def metropolis_sweep_perlink(U, beta, alpha, key, L, T_half, A_spatial_mask, eps=0.3):
    """Per-link Metropolis using FULL ACTION eval before/after each direction sweep.

    Sweep all links in one direction, then full action delta as one MC step.
    This is "subgroup-Metropolis" : sample whole direction's links, accept/reject globally.
    """
    twoT = 2 * T_half
    for mu in range(4):
        key, k_prop, k_acc = random.split(key, 3)
        X = random_su2_near_identity(k_prop, U[..., mu, :, :].shape[:-2], eps=eps)
        U_proposed_mu = jnp.einsum('...ij,...jk->...ik', X, U[..., mu, :, :])
        U_proposed = U.at[..., mu, :, :].set(U_proposed_mu)

        S_old = wilson_action_deformed(U, beta, alpha, L, T_half, A_spatial_mask)
        S_new = wilson_action_deformed(U_proposed, beta, alpha, L, T_half, A_spatial_mask)
        dS = S_new - S_old
        rand_u = random.uniform(k_acc)
        accept = rand_u < jnp.exp(jnp.minimum(0.0, -dS))
        U = jnp.where(accept, U_proposed, U)
    return U


# ============================================================================
# Thermalization + α-integration
# ============================================================================

def thermalize(key, beta, alpha, L, T_half, A_spatial_mask, n_sweeps, eps=0.3):
    k, sk = random.split(key)
    U = random_su2_haar(sk, (L, L, L, 2*T_half, 4))
    for i in range(n_sweeps):
        k, sk = random.split(k)
        U = metropolis_sweep_perlink(U, beta, alpha, sk, L, T_half, A_spatial_mask, eps)
    return U, k


def alpha_integrate(L, T_half, beta, alpha_grid, n_thermalize, n_decorr, n_samples, key, eps=0.3):
    """For each α in grid, sample ⟨∂S/∂α⟩, then integrate."""
    L_x = L
    A_spatial_mask = jnp.indices((L_x, L_x, L_x))[0] < L_x // 2  # (L, L, L)

    boundary_2D = L_x * L_x  # ∂A = (y, z) plane at x_0 = L/2

    print(f"\n--- L = {L}, T_half = {T_half} (2T = {2*T_half}), beta = {beta} ---", flush=True)
    print(f"    Boundary ∂A = {boundary_2D} sites", flush=True)

    results_per_alpha = {}

    # Thermalize at α=0 (Z_1²)
    print(f"Thermalize α=0 ({n_thermalize} sweeps)...", flush=True)
    t0 = time.time()
    U, key = thermalize(key, beta, 0.0, L, T_half, A_spatial_mask, n_thermalize, eps)
    print(f"Thermalized in {time.time()-t0:.1f}s", flush=True)

    for alpha in alpha_grid:
        t_a = time.time()
        # Re-equilibrate at this α
        n_reequil = max(20, n_decorr * 3)
        for _ in range(n_reequil):
            key, sk = random.split(key)
            U = metropolis_sweep_perlink(U, beta, alpha, sk, L, T_half, A_spatial_mask, eps)

        # Sample
        dS_samples = []
        for s in range(n_samples):
            for _ in range(n_decorr):
                key, sk = random.split(key)
                U = metropolis_sweep_perlink(U, beta, alpha, sk, L, T_half, A_spatial_mask, eps)
            dS = float(alpha_observable(U, beta, L, T_half, A_spatial_mask))
            dS_samples.append(dS)
            if s == 0 or (s+1) % max(1, n_samples//5) == 0 or s == n_samples-1:
                print(f"  α={alpha:.3f} sample {s+1}/{n_samples}: ∂S/∂α = {dS:.4e}, "
                      f"t={time.time()-t_a:.1f}s", flush=True)

        dS_arr = np.array(dS_samples)
        results_per_alpha[float(alpha)] = {
            'mean': float(dS_arr.mean()),
            'std': float(dS_arr.std()),
            'sem': float(dS_arr.std() / np.sqrt(len(dS_arr))),
            'samples': dS_samples,
            'elapsed_s': time.time() - t_a,
        }

    # Integrate ∫₀¹ dα ⟨∂S/∂α⟩_α
    alphas = np.array(sorted(results_per_alpha.keys()))
    means = np.array([results_per_alpha[float(a)]['mean'] for a in alphas])
    sems = np.array([results_per_alpha[float(a)]['sem'] for a in alphas])
    trap_fn = np.trapezoid if hasattr(np, 'trapezoid') else np.trapz
    S_2 = float(trap_fn(means, alphas))
    S_2_err = float(trap_fn(sems, alphas))

    print(f"\nL={L}: S_2 = {S_2:.4e} +/- {S_2_err:.4e}", flush=True)
    print(f"      c per ∂A = S_2/L^2 = {S_2/boundary_2D:.6e}", flush=True)
    print(f"      c / (1/4) = {(S_2/boundary_2D)/0.25:.4f}", flush=True)

    return {
        'L': L, 'T_half': T_half, 'beta': beta,
        'boundary_2D': boundary_2D,
        'alpha_grid': alphas.tolist(),
        'mean_dS_per_alpha': means.tolist(),
        'sem_per_alpha': sems.tolist(),
        'S_2': S_2, 'S_2_err': S_2_err,
        'c_per_2D': S_2 / boundary_2D,
        'c_err': S_2_err / boundary_2D,
        'results_per_alpha': results_per_alpha,
    }


def main():
    BETA = 2.4
    # α grid : fine for accurate Simpson integration
    ALPHA_GRID = list(np.linspace(0.0, 1.0, 21))  # 21 points, dα=0.05

    runs_config = {
        4:  {'T_half': 4,  'n_thermalize': 300, 'n_decorr': 5,  'n_samples': 200},
        6:  {'T_half': 6,  'n_thermalize': 400, 'n_decorr': 8,  'n_samples': 100},
        8:  {'T_half': 8,  'n_thermalize': 500, 'n_decorr': 10, 'n_samples': 50},
        10: {'T_half': 10, 'n_thermalize': 600, 'n_decorr': 15, 'n_samples': 30},
    }

    all_results = {}
    for L in [4, 6, 8, 10]:
        cfg = runs_config[L]
        print(f"\n{'='*78}\nLATTICE L = {L}\n{'='*78}", flush=True)
        key = random.PRNGKey(2031 + 29 * L)
        try:
            r = alpha_integrate(L, cfg['T_half'], BETA, ALPHA_GRID,
                                 cfg['n_thermalize'], cfg['n_decorr'], cfg['n_samples'],
                                 key)
            all_results[L] = r
        except Exception as e:
            print(f"L={L} FAILED : {e}", flush=True)
            import traceback
            traceback.print_exc()
        # Checkpoint
        with open('/tmp/jax_su2_EE_BP2008b_results.json', 'w') as f:
            json.dump({
                'method': 'BP2008b: 1 lattice deformed connectivity + α-integration Fodor-Endrödi',
                'references': ['arXiv:0802.4247', 'arXiv:1812.04279', 'arXiv:2211.00425'],
                'beta': BETA, 'alpha_grid': ALPHA_GRID,
                'runs_config': runs_config,
                'results': {str(L): all_results[L] for L in all_results},
                'partial': True,
                'total_elapsed_s': time.time() - START,
            }, f, indent=2)

    print(f"\n{'='*78}\nSCALING — Renyi-2 EE via BP2008b α-integration\n{'='*78}", flush=True)
    print(f"{'L':>4} {'|∂A|':>6} {'S_2':>16} {'c=S_2/∂A':>16} {'c/(1/4)':>10}", flush=True)
    print("-"*65, flush=True)
    for L in sorted(all_results.keys()):
        r = all_results[L]
        print(f"{L:>4} {r['boundary_2D']:>6} "
              f"{r['S_2']:>10.4e}+/-{r['S_2_err']:>3.0e} "
              f"{r['c_per_2D']:>10.4e}+/-{r['c_err']:>3.0e} "
              f"{r['c_per_2D']/0.25:>10.4f}", flush=True)

    if len(all_results) >= 1:
        L_max = max(all_results.keys())
        c_meas = all_results[L_max]['c_per_2D']
        c_err = all_results[L_max]['c_err']
        candidates = {
            '1/4 (kappa^2(SU(2)) Bekenstein)': 0.25,
            'C(SU(2)) Rabenstein 2019 = 0.054': 0.054,
            'log(3)/(2*pi*sqrt(2)) = 0.1237': np.log(3)/(2*np.pi*np.sqrt(2)),
            '3/(4*pi^2) = 0.0760': 3/(4*np.pi**2),
        }
        print(f"\nCoefficient candidates (vs L={L_max}) :", flush=True)
        for name, c_pred in candidates.items():
            z = (c_meas - c_pred) / max(c_err, 1e-6)
            sig = "OK" if abs(z) < 2 else "~" if abs(z) < 3 else "X"
            print(f"  {name:<45} : ratio={c_meas/c_pred:.3f}, |Z|={abs(z):.2f} {sig}", flush=True)

    output = {
        'method': 'BP2008b: 1 lattice deformed connectivity + α-integration Fodor-Endrödi',
        'references': ['arXiv:0802.4247', 'arXiv:1812.04279', 'arXiv:2211.00425'],
        'beta': BETA, 'alpha_grid': ALPHA_GRID,
        'runs_config': runs_config,
        'results': {str(L): all_results[L] for L in all_results},
        'total_elapsed_s': time.time() - START,
    }
    with open('/tmp/jax_su2_EE_BP2008b_results.json', 'w') as f:
        json.dump(output, f, indent=2)

    print(f"\nTotal elapsed : {time.time() - START:.1f}s "
          f"({(time.time() - START)/60:.1f}min)", flush=True)
    print(f"Saved : /tmp/jax_su2_EE_BP2008b_results.json", flush=True)
    print(f"END : {time.ctime()}", flush=True)
    print(f"DONE.", flush=True)


if __name__ == "__main__":
    main()
