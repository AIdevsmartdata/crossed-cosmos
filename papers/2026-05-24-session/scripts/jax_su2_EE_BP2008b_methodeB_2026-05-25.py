#!/usr/bin/env python3
"""JAX SU(2) Renyi-2 EE — Méthode B : direct area-law fit S_2 = κ·|∂A| + const.

Stratégie : à β fixe (β=2.4), L_x=L_τ fixé, varier L_y=L_z pour obtenir
multiples |∂A| = L_y·L_z. Fit linéaire S_2(|∂A|) extrait κ leading
directement (pas besoin de β-scan continuum extrapolation).

DS Bot proposition (méthode B) : la plus économique pour extraire κ leading.

Lattice asymétrique : L_x × L_y × L_z × 2T  (2T temporal doublé pour α-integration)
Region A = {x_0 < L_x/2}
∂A = (y, z) plane at x_0 = L_x/2 → |∂A| = L_y × L_z

Run grid : L_x = L_τ = 8, L_y = L_z ∈ {4, 6, 8, 10, 12} → |∂A| ∈ {16, 36, 64, 100, 144}

Fit attendu : S_2 = κ · |∂A| / a²(β=2.4) + C · log(|∂A|) + const

Si fit linéaire bon : κ_leading extracted directly.
Comparer à κ²(SU(2)) = 1/4 = Bekenstein prediction (after a→0 conversion).

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
print(f"JAX SU(2) Renyi-2 EE — Méthode B (asymmetric lattice, vary ∂A)", flush=True)
print(f"Goal : extract κ_leading via direct area-law fit S_2 = κ·|∂A| + ...", flush=True)
print("=" * 78, flush=True)
jax.config.update("jax_enable_x64", True)
print(f"JAX : {jax.__version__}, backend : {jax.default_backend()}", flush=True)


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
    """Standard Wilson on asymmetric lattice (L_x, L_y, L_z, L_tau)."""
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


def make_deformed_next_t(L_x, L_y, L_z, T_half, A_spatial_mask):
    twoT = 2 * T_half
    next_t_2T = jnp.array([(t + 1) % twoT for t in range(twoT)])
    next_t_T = jnp.array([
        (t + 1) % T_half if t < T_half
        else T_half + ((t - T_half + 1) % T_half)
        for t in range(twoT)
    ])
    A_4d = jnp.broadcast_to(A_spatial_mask[..., None], (L_x, L_y, L_z, twoT))
    next_t_2T_4d = jnp.broadcast_to(next_t_2T[None, None, None, :], (L_x, L_y, L_z, twoT))
    next_t_T_4d = jnp.broadcast_to(next_t_T[None, None, None, :], (L_x, L_y, L_z, twoT))
    return next_t_2T_4d, next_t_T_4d


@partial(jit, static_argnames=('L_x', 'L_y', 'L_z', 'T_half'))
def wilson_action_deformed_asym(U, beta, alpha, L_x, L_y, L_z, T_half, A_spatial_mask):
    """Wilson action on asymmetric deformed lattice with α interpolation."""
    twoT = 2 * T_half
    next_t_2T_4d, next_t_T_4d = make_deformed_next_t(L_x, L_y, L_z, T_half, A_spatial_mask)

    total = 0.0

    # Pure spatial plaquettes (μ, ν ∈ {0,1,2}): standard
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

    # Temporal plaquettes
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

        junction_mask_t = jnp.zeros(twoT, dtype=bool)
        junction_mask_t = junction_mask_t.at[T_half - 1].set(True)
        junction_mask_t = junction_mask_t.at[twoT - 1].set(True)
        junction_mask_4d = jnp.broadcast_to(junction_mask_t[None, None, None, :], (L_x, L_y, L_z, twoT))
        A_4d = jnp.broadcast_to(A_spatial_mask[..., None], (L_x, L_y, L_z, twoT))

        is_junction = junction_mask_4d
        is_A = A_4d

        contrib_non_junction = 1.0 - tr_T
        contrib_junction_Abar = 1.0 - tr_T
        contrib_junction_A = 1.0 - ((1.0 - alpha) * tr_T + alpha * tr_2T)

        contrib = jnp.where(
            is_junction,
            jnp.where(is_A, contrib_junction_A, contrib_junction_Abar),
            contrib_non_junction
        )

        total += jnp.sum(contrib)

    return beta * total


@partial(jit, static_argnames=('L_x', 'L_y', 'L_z', 'T_half'))
def alpha_observable_asym(U, beta, L_x, L_y, L_z, T_half, A_spatial_mask):
    twoT = 2 * T_half
    next_t_2T_4d, next_t_T_4d = make_deformed_next_t(L_x, L_y, L_z, T_half, A_spatial_mask)

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

        junction_mask_t = jnp.zeros(twoT, dtype=bool)
        junction_mask_t = junction_mask_t.at[T_half - 1].set(True)
        junction_mask_t = junction_mask_t.at[twoT - 1].set(True)
        junction_mask_4d = jnp.broadcast_to(junction_mask_t[None, None, None, :], (L_x, L_y, L_z, twoT))
        A_4d = jnp.broadcast_to(A_spatial_mask[..., None], (L_x, L_y, L_z, twoT))
        mask_A_junction = junction_mask_4d & A_4d

        dS_per_plaq = (tr_T - tr_2T)
        total += jnp.sum(dS_per_plaq * mask_A_junction)

    return (beta / 2.0) * total


def adaptive_eps(alpha, eps0=0.3):
    return eps0 / (1.0 + 3.0 * alpha)


@partial(jit, static_argnames=('L_x', 'L_y', 'L_z', 'T_half'))
def metropolis_sweep_perlink_asym(U, beta, alpha, key, L_x, L_y, L_z, T_half, A_spatial_mask, eps=0.3):
    for mu in range(4):
        key, k_prop, k_acc = random.split(key, 3)
        X = random_su2_near_identity(k_prop, U[..., mu, :, :].shape[:-2], eps=eps)
        U_proposed_mu = jnp.einsum('...ij,...jk->...ik', X, U[..., mu, :, :])
        U_proposed = U.at[..., mu, :, :].set(U_proposed_mu)
        S_old = wilson_action_deformed_asym(U, beta, alpha, L_x, L_y, L_z, T_half, A_spatial_mask)
        S_new = wilson_action_deformed_asym(U_proposed, beta, alpha, L_x, L_y, L_z, T_half, A_spatial_mask)
        dS = S_new - S_old
        rand_u = random.uniform(k_acc)
        accept = rand_u < jnp.exp(jnp.minimum(0.0, -dS))
        U = jnp.where(accept, U_proposed, U)
    return U


def thermalize_asym(key, beta, alpha, L_x, L_y, L_z, T_half, A_spatial_mask, n_sweeps, eps0=0.3):
    k, sk = random.split(key)
    U = random_su2_haar(sk, (L_x, L_y, L_z, 2*T_half, 4))
    eps_eff = adaptive_eps(alpha, eps0)
    for i in range(n_sweeps):
        k, sk = random.split(k)
        U = metropolis_sweep_perlink_asym(U, beta, alpha, sk, L_x, L_y, L_z, T_half, A_spatial_mask, eps_eff)
    return U, k


def alpha_integrate_asym(L_x, L_y, L_z, T_half, beta, alpha_grid, n_thermalize, n_decorr, n_samples, key, eps0=0.3):
    A_spatial_mask = jnp.indices((L_x, L_y, L_z))[0] < L_x // 2
    boundary_area = L_y * L_z  # |∂A| = L_y · L_z

    print(f"\n--- L_x={L_x}, L_y={L_y}, L_z={L_z}, T_half={T_half}, β={beta} ---", flush=True)
    print(f"    |∂A| = L_y × L_z = {boundary_area}", flush=True)

    print(f"Thermalize α=0 ({n_thermalize} sweeps)...", flush=True)
    t0 = time.time()
    U, key = thermalize_asym(key, beta, 0.0, L_x, L_y, L_z, T_half, A_spatial_mask, n_thermalize, eps0)
    print(f"Thermalized in {time.time()-t0:.1f}s", flush=True)

    results_per_alpha = {}

    for alpha in alpha_grid:
        t_a = time.time()
        eps_eff = adaptive_eps(alpha, eps0)
        n_reequil = max(50, n_decorr * 10)
        for _ in range(n_reequil):
            key, sk = random.split(key)
            U = metropolis_sweep_perlink_asym(U, beta, alpha, sk, L_x, L_y, L_z, T_half, A_spatial_mask, eps_eff)

        dS_samples = []
        for s in range(n_samples):
            for _ in range(n_decorr):
                key, sk = random.split(key)
                U = metropolis_sweep_perlink_asym(U, beta, alpha, sk, L_x, L_y, L_z, T_half, A_spatial_mask, eps_eff)
            dS = float(alpha_observable_asym(U, beta, L_x, L_y, L_z, T_half, A_spatial_mask))
            dS_samples.append(dS)
            if s == 0 or (s+1) % max(1, n_samples//4) == 0 or s == n_samples-1:
                print(f"  α={alpha:.3f} (eps={eps_eff:.3f}) sample {s+1}/{n_samples}: "
                      f"∂S/∂α = {dS:.4e}, t={time.time()-t_a:.1f}s", flush=True)

        dS_arr = np.array(dS_samples)
        results_per_alpha[float(alpha)] = {
            'mean': float(dS_arr.mean()),
            'std': float(dS_arr.std()),
            'sem': float(dS_arr.std() / np.sqrt(len(dS_arr))),
            'samples': dS_samples,
            'elapsed_s': time.time() - t_a,
        }

    alphas = np.array(sorted(results_per_alpha.keys()))
    means = np.array([results_per_alpha[float(a)]['mean'] for a in alphas])
    sems = np.array([results_per_alpha[float(a)]['sem'] for a in alphas])
    trap_fn = np.trapezoid if hasattr(np, 'trapezoid') else np.trapz
    S_2 = float(trap_fn(means, alphas))
    S_2_err = float(trap_fn(sems, alphas))

    print(f"\n→ |∂A|={boundary_area}: S_2 = {S_2:.4e} +/- {S_2_err:.4e}", flush=True)

    return {
        'L_x': L_x, 'L_y': L_y, 'L_z': L_z, 'T_half': T_half, 'beta': beta,
        'boundary_area': boundary_area,
        'alpha_grid': alphas.tolist(),
        'mean_dS_per_alpha': means.tolist(),
        'sem_per_alpha': sems.tolist(),
        'S_2': S_2, 'S_2_err': S_2_err,
        'results_per_alpha': results_per_alpha,
    }


def main():
    BETA = 2.4
    L_x = 8
    T_half = 8
    ALPHA_GRID = list(np.linspace(0.0, 1.0, 11))  # 11 points

    # Vary L_y = L_z to get multiple |∂A|
    LY_LZ_LIST = [4, 6, 8, 10]  # |∂A| ∈ {16, 36, 64, 100}

    config = {'n_thermalize': 500, 'n_decorr': 10, 'n_samples': 80}

    all_results = []
    for L_yz in LY_LZ_LIST:
        print(f"\n{'='*78}", flush=True)
        print(f"L_x={L_x}, L_y=L_z={L_yz}, T={T_half} → |∂A|={L_yz**2}", flush=True)
        print(f"{'='*78}", flush=True)
        key = random.PRNGKey(2032 + 17 * L_yz)
        try:
            r = alpha_integrate_asym(L_x, L_yz, L_yz, T_half, BETA, ALPHA_GRID,
                                       config['n_thermalize'], config['n_decorr'],
                                       config['n_samples'], key, eps0=0.3)
            all_results.append(r)
        except Exception as e:
            print(f"L_yz={L_yz} FAILED : {e}", flush=True)
            import traceback
            traceback.print_exc()
        # Checkpoint
        with open('/tmp/jax_su2_EE_BP2008b_methodeB.json', 'w') as f:
            json.dump({
                'method': 'Méthode B : vary |∂A| at fixed L_x, T, β',
                'L_x': L_x, 'T_half': T_half, 'beta': BETA, 'alpha_grid': ALPHA_GRID,
                'config': config,
                'results': all_results,
                'partial': True,
                'total_elapsed_s': time.time() - START,
            }, f, indent=2)

    # Linear fit S_2 = κ·|∂A| + const
    print(f"\n{'='*78}", flush=True)
    print(f"AREA-LAW FIT — extracting κ_leading from S_2(|∂A|)", flush=True)
    print(f"{'='*78}", flush=True)

    areas = np.array([r['boundary_area'] for r in all_results])
    S2s = np.array([r['S_2'] for r in all_results])
    S2_errs = np.array([r['S_2_err'] for r in all_results])

    print(f"{'|∂A|':>6} {'S_2':>16} {'S_2/|∂A|':>14}", flush=True)
    print("-" * 45, flush=True)
    for a, s2, s2e in zip(areas, S2s, S2_errs):
        print(f"{a:>6} {s2:>10.4e}+/-{s2e:>3.0e} {s2/a:>14.6f}", flush=True)

    # Weighted linear regression : S_2 = κ·|∂A| + b
    if len(areas) >= 2:
        weights = 1.0 / np.maximum(S2_errs**2, 1e-10)
        S_w = np.sum(weights)
        Sx_w = np.sum(weights * areas)
        Sy_w = np.sum(weights * S2s)
        Sxx_w = np.sum(weights * areas**2)
        Sxy_w = np.sum(weights * areas * S2s)
        delta = S_w * Sxx_w - Sx_w**2
        kappa = (S_w * Sxy_w - Sx_w * Sy_w) / delta
        b = (Sxx_w * Sy_w - Sx_w * Sxy_w) / delta
        kappa_err = np.sqrt(S_w / delta)
        b_err = np.sqrt(Sxx_w / delta)
        print(f"\nLinear fit S_2 = κ·|∂A| + b :", flush=True)
        print(f"  κ = {kappa:.6e} ± {kappa_err:.2e}", flush=True)
        print(f"  b = {b:.6e} ± {b_err:.2e}", flush=True)
        print(f"\nCompare to predictions :", flush=True)
        candidates = {
            '1/4 (kappa^2(SU(2)) Bekenstein)': 0.25,
            'C(SU(2)) Rabenstein 2019 = 0.054': 0.054,
            'log(3)/(2*pi*sqrt(2)) = 0.1237': np.log(3)/(2*np.pi*np.sqrt(2)),
            '3/(4*pi^2) = 0.0760': 3/(4*np.pi**2),
        }
        for name, c_pred in candidates.items():
            z = (kappa - c_pred) / max(kappa_err, 1e-6)
            sig = "OK" if abs(z) < 2 else "~" if abs(z) < 3 else "X"
            print(f"  vs {name:<45} : ratio={kappa/c_pred:.3f}, |Z|={abs(z):.2f} {sig}", flush=True)

        output = {
            'method': 'Méthode B : direct area-law fit',
            'L_x': L_x, 'T_half': T_half, 'beta': BETA,
            'alpha_grid': ALPHA_GRID,
            'config': config,
            'boundary_areas': areas.tolist(),
            'S_2_values': S2s.tolist(),
            'S_2_errors': S2_errs.tolist(),
            'fit': {
                'kappa': float(kappa),
                'kappa_err': float(kappa_err),
                'b': float(b),
                'b_err': float(b_err),
            },
            'results': all_results,
            'total_elapsed_s': time.time() - START,
        }
        with open('/tmp/jax_su2_EE_BP2008b_methodeB.json', 'w') as f:
            json.dump(output, f, indent=2)

    print(f"\nTotal elapsed : {time.time() - START:.1f}s "
          f"({(time.time() - START)/60:.1f}min)", flush=True)
    print(f"Saved : /tmp/jax_su2_EE_BP2008b_methodeB.json", flush=True)
    print(f"END : {time.ctime()}", flush=True)
    print(f"DONE.", flush=True)


if __name__ == "__main__":
    main()
