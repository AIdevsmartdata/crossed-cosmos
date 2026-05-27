#!/usr/bin/env python3
"""SU(5) BP2008b — TEST DISCRIMINANT cross-N (1-1/N²) vs √N.

Mesuré 2026-05-25 SU(2) : κ = 0.5080, SU(3) : κ = 0.6025
Fit (1-1/N²)·κ_∞ → κ_∞ ≈ 0.6779
Prédiction SU(5) : κ = 0.6779 · 15/16 = 0.6356

vs √N : κ = 0.5080·√2 = 0.719

Diff = 0.083 → discriminant à ~15σ avec précision ~0.005.

β=9.6 matched 't Hooft λ=10/3 (SU(2) β=2.4 ↔ SU(N) β=N²·2.4/4).

Author : Kévin Rémondière (ORCID 0009-0008-2443-7166).
"""
import os
os.environ.setdefault('XLA_PYTHON_CLIENT_PREALLOCATE', 'false')
os.environ.setdefault('JAX_ENABLE_X64', 'True')

import sys
sys.path.insert(0, '/tmp')

# Load SU(5) primitives
with open('/tmp/jax_su5_lattice_2026-05-25.py') as f:
    src = f.read()
src = src.split('if __name__')[0]
g_su5 = {}
exec(src, g_su5)

random_su5_haar = g_su5['random_su5_haar']
random_su5_near_identity = g_su5['random_su5_near_identity']
wilson_action_su5 = g_su5['wilson_action_su5']
plaquette_mean_su5 = g_su5['plaquette_mean_su5']
N_GROUP = g_su5['N_GROUP']  # = 4

import jax
import jax.numpy as jnp
from jax import jit, random
from functools import partial
import time
import json
import numpy as np


# ============================================================================
# Deformed-lattice helpers (geometry, same as SU(2)/SU(3))
# ============================================================================

def make_next_t_arrays(T_half):
    twoT = 2 * T_half
    next_t_2T = jnp.array([(t + 1) % twoT for t in range(twoT)])
    next_t_T = jnp.array([
        (t + 1) % T_half if t < T_half
        else T_half + ((t - T_half + 1) % T_half)
        for t in range(twoT)
    ])
    return next_t_T, next_t_2T


def make_prev_t_arrays(T_half):
    twoT = 2 * T_half
    prev_t_2T = jnp.array([(t - 1) % twoT for t in range(twoT)])
    prev_t_T = jnp.array([
        (t - 1) % T_half if t < T_half
        else T_half + ((t - T_half - 1) % T_half)
        for t in range(twoT)
    ])
    return prev_t_T, prev_t_2T


def gather_link_at_t(U_link, next_t_arr):
    return U_link[:, :, :, next_t_arr]


def make_A_junction_link_mask(L_x, L_y, L_z, T_half, A_spatial_mask):
    twoT = 2 * T_half
    A_4d = jnp.broadcast_to(A_spatial_mask[..., None], (L_x, L_y, L_z, twoT))
    junction_mask_t = jnp.zeros(twoT, dtype=bool)
    junction_mask_t = junction_mask_t.at[T_half - 1].set(True)
    junction_mask_t = junction_mask_t.at[twoT - 1].set(True)
    junction_4d = jnp.broadcast_to(junction_mask_t[None, None, None, :], (L_x, L_y, L_z, twoT))
    A_junction_site = A_4d & junction_4d
    A_junction_link = jnp.broadcast_to(A_junction_site[..., None], (L_x, L_y, L_z, twoT, 4))
    return A_junction_link


# ============================================================================
# Staples K_T, K_2T (standard order post-fix, same einsums work for any N)
# ============================================================================

@partial(jit, static_argnames=('mu', 'L_x', 'L_y', 'L_z', 'T_half'))
def compute_staples_K_T_K_2T_su5(U, mu, L_x, L_y, L_z, T_half):
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
            U_nu_at_xpmu_real = jnp.roll(U_nu, -1, axis=mu)
            K_T_fwd = jnp.einsum('...ij,...kj,...lk->...il',
                                  U_nu_at_xpmu_real, jnp.conjugate(U_mu_at_xpnu_T),
                                  jnp.conjugate(U_nu))
            K_2T_fwd = jnp.einsum('...ij,...kj,...lk->...il',
                                   U_nu_at_xpmu_real, jnp.conjugate(U_mu_at_xpnu_2T),
                                   jnp.conjugate(U_nu))
            K_T += K_T_fwd
            K_2T += K_2T_fwd
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


# ============================================================================
# Metropolis with α-deformation (post-fix : K direct, /N=4)
# ============================================================================

@partial(jit, static_argnames=('mu', 'L_x', 'L_y', 'L_z', 'T_half'))
def metropolis_sweep_perlink_local_su5(U, beta, alpha, key, mu, L_x, L_y, L_z, T_half,
                                         A_link_mask, eps=0.12):
    K_T, K_2T = compute_staples_K_T_K_2T_su5(U, mu, L_x, L_y, L_z, T_half)
    K_eff = jnp.where(A_link_mask[..., mu, None, None], (1 - alpha) * K_T + alpha * K_2T, K_T)
    key1, key2 = random.split(key)
    X = random_su5_near_identity(key1, U[..., mu, :, :].shape[:-2], eps=eps)
    U_proposed = jnp.einsum('...ij,...jk->...ik', X, U[..., mu, :, :])
    new_term = jnp.real(jnp.trace(jnp.einsum('...ij,...jk->...ik', U_proposed, K_eff),
                                    axis1=-2, axis2=-1))
    old_term = jnp.real(jnp.trace(jnp.einsum('...ij,...jk->...ik', U[..., mu, :, :], K_eff),
                                    axis1=-2, axis2=-1))
    dS = -beta / N_GROUP * (new_term - old_term)
    rand_u = random.uniform(key2, dS.shape)
    accept = rand_u < jnp.exp(jnp.minimum(0.0, -dS))
    U_mu_new = jnp.where(accept[..., None, None], U_proposed, U[..., mu, :, :])
    return U.at[..., mu, :, :].set(U_mu_new)


@partial(jit, static_argnames=('L_x', 'L_y', 'L_z', 'T_half'))
def metropolis_sweep_4dir_su5(U, beta, alpha, key, L_x, L_y, L_z, T_half, A_link_mask, eps=0.12):
    for mu in range(4):
        key, sk = random.split(key)
        U = metropolis_sweep_perlink_local_su5(U, beta, alpha, sk, mu, L_x, L_y, L_z, T_half,
                                                A_link_mask, eps)
    return U


# ============================================================================
# α-observable SU(5) /N=4 normalization
# ============================================================================

@partial(jit, static_argnames=('L_x', 'L_y', 'L_z', 'T_half'))
def alpha_observable_su5(U, beta, L_x, L_y, L_z, T_half, A_spatial_mask):
    twoT = 2 * T_half
    next_t_T, next_t_2T = make_next_t_arrays(T_half)
    A_4d = jnp.broadcast_to(A_spatial_mask[..., None], (L_x, L_y, L_z, twoT))
    junction_mask_t = jnp.zeros(twoT, dtype=bool)
    junction_mask_t = junction_mask_t.at[T_half - 1].set(True)
    junction_mask_t = junction_mask_t.at[twoT - 1].set(True)
    junction_4d = jnp.broadcast_to(junction_mask_t[None, None, None, :], (L_x, L_y, L_z, twoT))
    mask_A_junction = junction_4d & A_4d

    total = 0.0
    nu = 3
    U_nu = U[..., nu, :, :]
    for mu in range(3):
        U_mu = U[..., mu, :, :]
        U_nu_pmu = jnp.roll(U_nu, -1, axis=mu)
        U_mu_at_nextT = gather_link_at_t(U_mu, next_t_T)
        U_mu_at_next2T = gather_link_at_t(U_mu, next_t_2T)
        P_T = jnp.einsum('...ij,...jk,...lk,...ml->...im',
                          U_mu, U_nu_pmu,
                          jnp.conjugate(U_mu_at_nextT),
                          jnp.conjugate(U_nu))
        tr_T = jnp.real(jnp.trace(P_T, axis1=-2, axis2=-1)) / N_GROUP
        P_2T = jnp.einsum('...ij,...jk,...lk,...ml->...im',
                           U_mu, U_nu_pmu,
                           jnp.conjugate(U_mu_at_next2T),
                           jnp.conjugate(U_nu))
        tr_2T = jnp.real(jnp.trace(P_2T, axis1=-2, axis2=-1)) / N_GROUP
        dS_per_plaq = (tr_T - tr_2T)
        total += jnp.sum(dS_per_plaq * mask_A_junction)
    return (beta / N_GROUP) * total


# ============================================================================
# Pipeline
# ============================================================================

def adaptive_eps(alpha, eps0=0.12):
    return eps0 / (1.0 + 3.0 * alpha)


def thermalize_su5(key, beta, alpha, L_x, L_y, L_z, T_half, A_link_mask, n_sweeps, eps0=0.12):
    k, sk = random.split(key)
    U = random_su5_haar(sk, (L_x, L_y, L_z, 2*T_half, 4))
    eps_eff = adaptive_eps(alpha, eps0)
    for i in range(n_sweeps):
        k, sk = random.split(k)
        U = metropolis_sweep_4dir_su5(U, beta, alpha, sk, L_x, L_y, L_z, T_half, A_link_mask, eps_eff)
    return U, k


def alpha_integrate_su5(L_x, L_y, L_z, T_half, beta, alpha_grid, n_thermalize, n_decorr,
                         n_samples, key, eps0=0.12):
    A_spatial_mask = jnp.indices((L_x, L_y, L_z))[0] < L_x // 2
    A_link_mask = make_A_junction_link_mask(L_x, L_y, L_z, T_half, A_spatial_mask)
    boundary_2D = L_y * L_z
    print(f"\n--- L={L_x}×{L_y}×{L_z}×{2*T_half}, β={beta} (SU(5)), |∂A|={boundary_2D} ---",
          flush=True)
    t0 = time.time()
    U, key = thermalize_su5(key, beta, 0.0, L_x, L_y, L_z, T_half, A_link_mask, n_thermalize, eps0)
    print(f"Thermalized {n_thermalize} sweeps in {time.time()-t0:.1f}s", flush=True)
    p_init = plaquette_mean_su5(U)
    print(f"  ⟨P⟩(α=0) = {p_init:.4f}", flush=True)

    results_per_alpha = {}
    for alpha in alpha_grid:
        t_a = time.time()
        eps_eff = adaptive_eps(alpha, eps0)
        n_reequil = max(50, n_decorr * 5)
        for _ in range(n_reequil):
            key, sk = random.split(key)
            U = metropolis_sweep_4dir_su5(U, beta, alpha, sk, L_x, L_y, L_z, T_half,
                                            A_link_mask, eps_eff)
        dS_samples = []
        for s in range(n_samples):
            for _ in range(n_decorr):
                key, sk = random.split(key)
                U = metropolis_sweep_4dir_su5(U, beta, alpha, sk, L_x, L_y, L_z, T_half,
                                                A_link_mask, eps_eff)
            dS = float(alpha_observable_su5(U, beta, L_x, L_y, L_z, T_half, A_spatial_mask))
            dS_samples.append(dS)
        dS_arr = np.array(dS_samples)
        results_per_alpha[float(alpha)] = {
            'mean': float(dS_arr.mean()),
            'std': float(dS_arr.std()),
            'sem': float(dS_arr.std() / np.sqrt(len(dS_arr))),
            'samples': dS_samples,
        }
        print(f"  α={alpha:.2f}: <dS/dα>={dS_arr.mean():.3e}±{dS_arr.std()/np.sqrt(len(dS_arr)):.0e} "
              f"({time.time()-t_a:.1f}s)", flush=True)

    alphas = np.array(sorted(results_per_alpha.keys()))
    means = np.array([results_per_alpha[float(a)]['mean'] for a in alphas])
    sems = np.array([results_per_alpha[float(a)]['sem'] for a in alphas])
    trap_fn = np.trapezoid if hasattr(np, 'trapezoid') else np.trapz
    S_2 = float(trap_fn(means, alphas))
    S_2_err = float(trap_fn(sems, alphas))
    print(f"L={L_x}: S_2 = {S_2:.4e} ± {S_2_err:.4e}, c={S_2/boundary_2D:.6e}", flush=True)

    return {
        'L_x': L_x, 'L_y': L_y, 'L_z': L_z, 'T_half': T_half, 'beta': beta,
        'boundary_2D': boundary_2D, 'plaquette_initial': p_init,
        'alpha_grid': alphas.tolist(),
        'mean_dS_per_alpha': means.tolist(),
        'sem_per_alpha': sems.tolist(),
        'S_2': S_2, 'S_2_err': S_2_err,
        'c_per_2D': S_2 / boundary_2D, 'c_err': S_2_err / boundary_2D,
        'results_per_alpha': results_per_alpha,
    }


def main():
    BETA = 15.0  # matched 't Hooft λ=10/3 ↔ SU(2) β=2.4, SU(3) β=5.4
    ALPHA_GRID = list(np.linspace(0.0, 1.0, 11))
    runs_config = {
        4:  {'T_half': 4,  'n_thermalize': 400, 'n_decorr': 10, 'n_samples': 60},
        6:  {'T_half': 6,  'n_thermalize': 500, 'n_decorr': 15, 'n_samples': 40},
        8:  {'T_half': 8,  'n_thermalize': 600, 'n_decorr': 20, 'n_samples': 30},
        10: {'T_half': 10, 'n_thermalize': 800, 'n_decorr': 25, 'n_samples': 20},
        12: {'T_half': 12, 'n_thermalize': 1000, 'n_decorr': 30, 'n_samples': 15},
    }
    L_VALUES = [4, 6, 8, 10, 12]

    START_TIME = time.time()
    print(f"START : {time.ctime()}", flush=True)
    print("=" * 78, flush=True)
    print(f"SU(5) BP2008b α-integration — matched 't Hooft β=9.6", flush=True)
    print(f"Test discriminant : κ ∝ (1-1/N²) vs κ ∝ √N", flush=True)
    print(f"Prédictions :  (1-1/N²)·κ_∞=0.6779·15/16 = 0.636", flush=True)
    print(f"               √N : 0.5080·√2 = 0.719", flush=True)
    print("=" * 78, flush=True)

    all_results = {}
    for L in L_VALUES:
        cfg = runs_config[L]
        print(f"\n{'='*78}\nLATTICE L = {L} (SU(5) β={BETA})\n{'='*78}", flush=True)
        key = random.PRNGKey(6040 + 67 * L + int(BETA * 100))
        try:
            r = alpha_integrate_su5(L, L, L, cfg['T_half'], BETA, ALPHA_GRID,
                                     cfg['n_thermalize'], cfg['n_decorr'], cfg['n_samples'], key)
            if r is not None:
                all_results[L] = r
                c = abs(r['c_per_2D'])
                print(f"\n✓ L={L} SU(5) β={BETA}: |c| = {c:.4f} ± {r['c_err']:.4f}", flush=True)
                print(f"  c/L = {c/L:.4f} ± {r['c_err']/L:.4f}", flush=True)
        except Exception as e:
            print(f"FAILED L={L}: {e}", flush=True)
            import traceback
            traceback.print_exc()

        with open('/tmp/jax_su5_EE_BP2008b.json', 'w') as f:
            json.dump({
                'method': 'SU(5) BP2008b cross-N test : (1-1/N²) vs √N',
                'beta': BETA, 'L_values': L_VALUES, 'runs_config': runs_config,
                'results': {str(L): all_results[L] for L in all_results},
                'partial': True,
                'total_elapsed_s': time.time() - START_TIME,
            }, f, indent=2)

    # Summary + verdict
    print(f"\n{'='*78}\nκ(SU(5)) extraction\n{'='*78}", flush=True)
    if len(all_results) >= 3:
        Ls = sorted(all_results.keys())
        cs_L = np.array([abs(all_results[L]['c_per_2D']) for L in Ls if L >= 8])
        ks_L = np.array([abs(all_results[L]['c_per_2D'])/L for L in Ls if L >= 8])
        errs_L = np.array([all_results[L]['c_err']/L for L in Ls if L >= 8])
        if len(ks_L) > 0:
            kappa_su5 = np.average(ks_L, weights=1/errs_L**2)
            kappa_err = 1/np.sqrt(np.sum(1/errs_L**2))
            print(f"\nκ(SU(5)) plateau (L≥8) = {kappa_su5:.4f} ± {kappa_err:.4f}", flush=True)
            print(f"\nVERDICT :", flush=True)
            print(f"  (1-1/N²)·κ_∞ pred 0.6356 : Δ = {abs(kappa_su5-0.6356):.4f}, "
                  f"{abs(kappa_su5-0.6356)/kappa_err:.1f}σ", flush=True)
            print(f"  √N pred 0.719            : Δ = {abs(kappa_su5-0.719):.4f}, "
                  f"{abs(kappa_su5-0.719)/kappa_err:.1f}σ", flush=True)
            print(f"  BH 1/4 pred 0.25         : Δ = {abs(kappa_su5-0.25):.4f}, "
                  f"{abs(kappa_su5-0.25)/kappa_err:.1f}σ", flush=True)

    with open('/tmp/jax_su5_EE_BP2008b.json', 'w') as f:
        json.dump({
            'method': 'SU(5) BP2008b cross-N test',
            'beta': BETA, 'L_values': L_VALUES, 'runs_config': runs_config,
            'results': {str(L): all_results[L] for L in all_results},
            'total_elapsed_s': time.time() - START_TIME,
        }, f, indent=2)
    print(f"\nTotal elapsed : {time.time() - START_TIME:.1f}s "
          f"({(time.time() - START_TIME)/3600:.2f}h)", flush=True)


if __name__ == "__main__":
    main()
