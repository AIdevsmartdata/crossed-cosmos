#!/usr/bin/env python3
"""SU(3) BP2008b α-integration — port from SU(2) FAST V3 (with both bugs fixed).

Test discriminant ECI vs BH cross-N :
  κ(SU(2)) ≈ 0.5065 (notre mesure SU(2) BP2008b post-fix L=4..12 β=2.4)
  ECI predict κ(SU(3)) ≈ 1/6 ≈ 0.167 (ratio 1/3)
  BH predict κ(SU(3)) ≈ 0.5 (ratio 1, universel)

Matched 't Hooft : β_SU(3) = 5.4 ↔ β_SU(2) = 2.4 (λ=10/3).

Modifications par rapport SU(2) FAST V3 :
- random_su2_* → random_su3_* (primitives validées)
- Normalisation 1/N : /2 → /3 dans actions
- Matrices 2×2 → 3×3 (héritée automatiquement des einsums)
- Bug fixes appliqués (K direct + standard staple order)

Author : Kévin Rémondière (ORCID 0009-0008-2443-7166).
"""
import os
os.environ.setdefault('XLA_PYTHON_CLIENT_PREALLOCATE', 'false')
os.environ.setdefault('JAX_ENABLE_X64', 'True')

import sys
sys.path.insert(0, '/tmp')

# Load SU(3) primitives
with open('/tmp/jax_su3_lattice_2026-05-25.py') as f:
    src = f.read()
src = src.split('if __name__')[0]
g_su3 = {}
exec(src, g_su3)

random_su3_haar = g_su3['random_su3_haar']
random_su3_near_identity = g_su3['random_su3_near_identity']
wilson_action_su3 = g_su3['wilson_action_su3']
plaquette_mean_su3 = g_su3['plaquette_mean_su3']

import jax
import jax.numpy as jnp
from jax import jit, random
from functools import partial
import time
import json
import numpy as np


# ============================================================================
# Deformed-lattice helpers (geometry, copy from SU(2) FAST V3 unchanged)
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
    """Gather U_link at next_t_arr[t] for each t. Works for any matrix size."""
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
# Staples K_T, K_2T with bug fix (standard staple order)
# ============================================================================

@partial(jit, static_argnames=('mu', 'L_x', 'L_y', 'L_z', 'T_half'))
def compute_staples_K_T_K_2T_su3(U, mu, L_x, L_y, L_z, T_half):
    """SU(3) staples K_T and K_2T — STANDARD ORDER (post bug fix)."""
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
            # FIX: standard order U_ν(x+μ̂) · U_μ(x+ν̂)† · U_ν(x)†
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
# Metropolis with α-deformation, /N=3 for SU(3) — POST FIX (K direct)
# ============================================================================

@partial(jit, static_argnames=('mu', 'L_x', 'L_y', 'L_z', 'T_half'))
def metropolis_sweep_perlink_local_su3(U, beta, alpha, key, mu, L_x, L_y, L_z, T_half,
                                         A_link_mask, eps=0.2):
    K_T, K_2T = compute_staples_K_T_K_2T_su3(U, mu, L_x, L_y, L_z, T_half)
    K_eff = jnp.where(A_link_mask[..., mu, None, None], (1 - alpha) * K_T + alpha * K_2T, K_T)
    key1, key2 = random.split(key)
    X = random_su3_near_identity(key1, U[..., mu, :, :].shape[:-2], eps=eps)
    U_proposed = jnp.einsum('...ij,...jk->...ik', X, U[..., mu, :, :])
    # FIX : K_eff direct, /N=3 for SU(3)
    new_term = jnp.real(jnp.trace(jnp.einsum('...ij,...jk->...ik', U_proposed, K_eff),
                                    axis1=-2, axis2=-1))
    old_term = jnp.real(jnp.trace(jnp.einsum('...ij,...jk->...ik', U[..., mu, :, :], K_eff),
                                    axis1=-2, axis2=-1))
    dS = -beta / 3.0 * (new_term - old_term)
    rand_u = random.uniform(key2, dS.shape)
    accept = rand_u < jnp.exp(jnp.minimum(0.0, -dS))
    U_mu_new = jnp.where(accept[..., None, None], U_proposed, U[..., mu, :, :])
    return U.at[..., mu, :, :].set(U_mu_new)


@partial(jit, static_argnames=('L_x', 'L_y', 'L_z', 'T_half'))
def metropolis_sweep_4dir_su3(U, beta, alpha, key, L_x, L_y, L_z, T_half, A_link_mask, eps=0.2):
    for mu in range(4):
        key, sk = random.split(key)
        U = metropolis_sweep_perlink_local_su3(U, beta, alpha, sk, mu, L_x, L_y, L_z, T_half,
                                                A_link_mask, eps)
    return U


# ============================================================================
# α-observable for SU(3), /N=3 normalization
# ============================================================================

@partial(jit, static_argnames=('L_x', 'L_y', 'L_z', 'T_half'))
def alpha_observable_su3(U, beta, L_x, L_y, L_z, T_half, A_spatial_mask):
    """Σ_{A-junction plaquettes} (tr_T - tr_2T)/3 · β  for SU(3)."""
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
        tr_T = jnp.real(jnp.trace(P_T, axis1=-2, axis2=-1)) / 3.0  # /N=3
        P_2T = jnp.einsum('...ij,...jk,...lk,...ml->...im',
                           U_mu, U_nu_pmu,
                           jnp.conjugate(U_mu_at_next2T),
                           jnp.conjugate(U_nu))
        tr_2T = jnp.real(jnp.trace(P_2T, axis1=-2, axis2=-1)) / 3.0
        dS_per_plaq = (tr_T - tr_2T)
        total += jnp.sum(dS_per_plaq * mask_A_junction)
    return (beta / 3.0) * total  # /N=3 for SU(3)


# ============================================================================
# Pipeline
# ============================================================================

def adaptive_eps(alpha, eps0=0.2):
    return eps0 / (1.0 + 3.0 * alpha)


def thermalize_su3(key, beta, alpha, L_x, L_y, L_z, T_half, A_link_mask, n_sweeps, eps0=0.2):
    k, sk = random.split(key)
    U = random_su3_haar(sk, (L_x, L_y, L_z, 2*T_half, 4))
    eps_eff = adaptive_eps(alpha, eps0)
    for i in range(n_sweeps):
        k, sk = random.split(k)
        U = metropolis_sweep_4dir_su3(U, beta, alpha, sk, L_x, L_y, L_z, T_half, A_link_mask, eps_eff)
    return U, k


def alpha_integrate_su3(L_x, L_y, L_z, T_half, beta, alpha_grid, n_thermalize, n_decorr,
                         n_samples, key, eps0=0.2):
    A_spatial_mask = jnp.indices((L_x, L_y, L_z))[0] < L_x // 2
    A_link_mask = make_A_junction_link_mask(L_x, L_y, L_z, T_half, A_spatial_mask)
    boundary_2D = L_y * L_z

    print(f"\n--- L={L_x}×{L_y}×{L_z}×{2*T_half}, β={beta} (SU(3)), |∂A|={boundary_2D} ---",
          flush=True)

    t0 = time.time()
    U, key = thermalize_su3(key, beta, 0.0, L_x, L_y, L_z, T_half, A_link_mask, n_thermalize, eps0)
    print(f"Thermalized {n_thermalize} sweeps in {time.time()-t0:.1f}s "
          f"({(time.time()-t0)/n_thermalize*1000:.1f}ms/sweep)", flush=True)

    p_init = plaquette_mean_su3(U)
    print(f"  Sanity check : ⟨P⟩(α=0) = {p_init:.4f}  (lit SU(3) β=5.4 ≈ 0.45)", flush=True)
    if p_init < 0.30 or p_init > 0.70:
        print(f"  ⚠️ ⟨P⟩ hors range raisonnable — SKIP", flush=True)
        return None

    results_per_alpha = {}
    for alpha in alpha_grid:
        t_a = time.time()
        eps_eff = adaptive_eps(alpha, eps0)
        n_reequil = max(50, n_decorr * 5)
        for _ in range(n_reequil):
            key, sk = random.split(key)
            U = metropolis_sweep_4dir_su3(U, beta, alpha, sk, L_x, L_y, L_z, T_half,
                                            A_link_mask, eps_eff)
        dS_samples = []
        for s in range(n_samples):
            for _ in range(n_decorr):
                key, sk = random.split(key)
                U = metropolis_sweep_4dir_su3(U, beta, alpha, sk, L_x, L_y, L_z, T_half,
                                                A_link_mask, eps_eff)
            dS = float(alpha_observable_su3(U, beta, L_x, L_y, L_z, T_half, A_spatial_mask))
            dS_samples.append(dS)
        dS_arr = np.array(dS_samples)
        results_per_alpha[float(alpha)] = {
            'mean': float(dS_arr.mean()),
            'std': float(dS_arr.std()),
            'sem': float(dS_arr.std() / np.sqrt(len(dS_arr))),
            'samples': dS_samples,
            'elapsed_s': time.time() - t_a,
        }
        print(f"  α={alpha:.2f} (eps={eps_eff:.3f}): <dS/dα>={dS_arr.mean():.3e}"
              f"±{dS_arr.std()/np.sqrt(len(dS_arr)):.0e} ({time.time()-t_a:.1f}s)", flush=True)

    alphas = np.array(sorted(results_per_alpha.keys()))
    means = np.array([results_per_alpha[float(a)]['mean'] for a in alphas])
    sems = np.array([results_per_alpha[float(a)]['sem'] for a in alphas])
    trap_fn = np.trapezoid if hasattr(np, 'trapezoid') else np.trapz
    S_2 = float(trap_fn(means, alphas))
    S_2_err = float(trap_fn(sems, alphas))

    print(f"L={L_x}: S_2 = {S_2:.4e} +/- {S_2_err:.4e}, c={S_2/boundary_2D:.6e}", flush=True)

    return {
        'L_x': L_x, 'L_y': L_y, 'L_z': L_z, 'T_half': T_half, 'beta': beta,
        'boundary_2D': boundary_2D,
        'plaquette_initial': p_init,
        'alpha_grid': alphas.tolist(),
        'mean_dS_per_alpha': means.tolist(),
        'sem_per_alpha': sems.tolist(),
        'S_2': S_2, 'S_2_err': S_2_err,
        'c_per_2D': S_2 / boundary_2D,
        'c_err': S_2_err / boundary_2D,
        'results_per_alpha': results_per_alpha,
    }


def main():
    BETA = 5.4  # matched 't Hooft λ=2N²/β=10/3 ↔ SU(2) β=2.4
    ALPHA_GRID = list(np.linspace(0.0, 1.0, 11))

    runs_config = {
        4:  {'T_half': 4,  'n_thermalize': 300, 'n_decorr': 8,  'n_samples': 80},
        6:  {'T_half': 6,  'n_thermalize': 400, 'n_decorr': 12, 'n_samples': 60},
        8:  {'T_half': 8,  'n_thermalize': 500, 'n_decorr': 18, 'n_samples': 40},
        10: {'T_half': 10, 'n_thermalize': 600, 'n_decorr': 22, 'n_samples': 30},
        12: {'T_half': 12, 'n_thermalize': 700, 'n_decorr': 25, 'n_samples': 20},
        16: {'T_half': 16, 'n_thermalize': 1000, 'n_decorr': 35, 'n_samples': 10},
    }
    L_VALUES = [4, 6, 8, 10, 12, 16]

    START_TIME = time.time()
    print(f"START : {time.ctime()}", flush=True)
    print("=" * 78, flush=True)
    print(f"SU(3) BP2008b FULL FIX α-integration — matched 't Hooft β=5.4", flush=True)
    print("=" * 78, flush=True)

    all_results = {}
    for L in L_VALUES:
        cfg = runs_config[L]
        print(f"\n{'='*78}\nLATTICE L = {L} (SU(3) β={BETA})\n{'='*78}", flush=True)
        key = random.PRNGKey(5040 + 53 * L + int(BETA * 100))
        try:
            r = alpha_integrate_su3(L, L, L, cfg['T_half'], BETA, ALPHA_GRID,
                                     cfg['n_thermalize'], cfg['n_decorr'], cfg['n_samples'], key)
            if r is not None:
                all_results[L] = r
                print(f"\n✓ L={L} SU(3) β={BETA}: c = {r['c_per_2D']:.4e} ± {r['c_err']:.2e}",
                      flush=True)
        except Exception as e:
            print(f"FAILED L={L}: {e}", flush=True)
            import traceback
            traceback.print_exc()

        # Save partial
        with open('/tmp/jax_su3_EE_BP2008b.json', 'w') as f:
            json.dump({
                'method': 'SU(3) BP2008b FULL FIX α-integration at β=5.4 matched t Hooft',
                'beta': BETA, 'L_values': L_VALUES, 'runs_config': runs_config,
                'results': {str(L): all_results[L] for L in all_results},
                'partial': True,
                'total_elapsed_s': time.time() - START_TIME,
            }, f, indent=2)

    # Summary
    print(f"\n{'='*78}\nc(L) SU(3) post-fix at β=5.4\n{'='*78}", flush=True)
    print(f"\n{'L':>4} {'⟨P⟩init':>10} {'|c|':>14} {'|c|/L':>14}")
    for L in L_VALUES:
        if L in all_results:
            r = all_results[L]
            c = r['c_per_2D']
            ce = r['c_err']
            print(f"{L:>4} {r['plaquette_initial']:>10.4f} {abs(c):>10.4f}±{ce:>5.4f} "
                  f"{abs(c)/L:>10.4f}±{ce/L:>5.4f}")

    # Linear fit |c|(L) = α + slope·L
    if len(all_results) >= 3:
        Ls = sorted(all_results.keys())
        cs = np.array([abs(all_results[L]['c_per_2D']) for L in Ls])
        errs = np.array([all_results[L]['c_err'] for L in Ls])
        w = 1.0/errs**2
        S_w = np.sum(w)
        Sx_w = np.sum(w*np.array(Ls))
        Sy_w = np.sum(w*cs)
        Sxx_w = np.sum(w*np.array(Ls)**2)
        Sxy_w = np.sum(w*np.array(Ls)*cs)
        det = S_w*Sxx_w - Sx_w**2
        slope = (S_w*Sxy_w - Sx_w*Sy_w)/det
        slope_err = np.sqrt(S_w/det)
        print(f"\n  Linear fit |c|(L) = α + (slope)·L : slope = {slope:.4f} ± {slope_err:.4f}",
              flush=True)
        print(f"\n  κ_EE(SU(3), per |∂A|_3D) = slope = {slope:.4f} ± {slope_err:.4f}", flush=True)
        print(f"\n  Comparaisons :", flush=True)
        print(f"    κ(SU(2)) mesuré = 0.5065 ± 0.010 (notre data BP2008b)", flush=True)
        print(f"    Ratio κ(SU(3))/κ(SU(2)) mesuré = {slope/0.5065:.4f}", flush=True)
        print(f"    ECI predict : 1/3 ≈ 0.3333", flush=True)
        print(f"    BH predict : 1.0 (universal)", flush=True)
        if abs(slope/0.5065 - 1/3) < 0.05:
            print(f"  ★★★★★ ECI CONFIRMED — ratio match 1/3", flush=True)
        elif abs(slope/0.5065 - 1.0) < 0.05:
            print(f"  ★★★ BH CONFIRMED — ratio match 1, ECI falsifié", flush=True)
        else:
            print(f"  ⚠️ Ratio {slope/0.5065:.3f} ne match ni ECI ni BH — investigate", flush=True)

    output = {
        'method': 'SU(3) BP2008b FULL FIX α-integration at β=5.4 matched t Hooft',
        'beta': BETA, 'L_values': L_VALUES, 'runs_config': runs_config,
        'results': {str(L): all_results[L] for L in all_results},
        'total_elapsed_s': time.time() - START_TIME,
    }
    with open('/tmp/jax_su3_EE_BP2008b.json', 'w') as f:
        json.dump(output, f, indent=2)

    print(f"\nTotal elapsed : {time.time() - START_TIME:.1f}s "
          f"({(time.time() - START_TIME)/3600:.2f}h)", flush=True)
    print(f"END : {time.ctime()}", flush=True)


if __name__ == "__main__":
    main()
