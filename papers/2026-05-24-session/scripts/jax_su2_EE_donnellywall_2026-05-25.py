#!/usr/bin/env python3
"""JAX SU(2) Donnelly-Wall Renyi-2 entanglement entropy — Attempt B rigorous test.

Méthode : thermodynamic integration (Caraglio-Gliozzi 2008 arXiv:0808.4094,
Alba-Tagliacozzo-Calabrese 2010 arXiv:1005.0148) on interpolating ensemble.

Pour 2 réplicas SU(2) Wilson lattice + region A planaire {x_0 < L/2} :

   S_λ(U1, U2) = (1-λ)[S(U1) + S(U2)] + λ[S(U1_swap) + S(U2_swap)]

   Z(λ) = ∫ DU1 DU2 exp(-S_λ)
   Z(0) = Z_1²       (two indep copies, single trace)
   Z(1) = Z_2        (replica-2 partition function, swapped boundary)

   S_2(A) = -log[Z(1)/Z(0)] = ∫₀¹ dλ ⟨ΔS⟩_λ

où ⟨ΔS⟩_λ = ⟨S(U1_swap) + S(U2_swap) - S(U1) - S(U2)⟩_λ
   = mean action increment when swapping under ensemble S_λ.

Leading area term : S_2 ≈ c · A_boundary, A = L^{d-1} = L³ pour 4D.
Prediction Bekenstein-Hawking (Attempt B) : c = 1/4 = κ²(SU(2)).

Author : Kévin Rémondière (ORCID 0009-0008-2443-7166).
Overnight budget : ~8h sur RTX 5060 Ti.
"""
import os
os.environ.setdefault('XLA_PYTHON_CLIENT_PREALLOCATE', 'false')
os.environ.setdefault('JAX_ENABLE_X64', 'True')

import jax
import jax.numpy as jnp
from jax import jit, vmap, lax, random
from functools import partial
import time
import json
import sys
import numpy as np

START = time.time()
print(f"START : {time.ctime()}", flush=True)
print("=" * 78, flush=True)
print(f"JAX SU(2) Donnelly-Wall Renyi-2 EE via thermodynamic integration", flush=True)
print(f"Caraglio-Gliozzi 2008 + Alba-Tagliacozzo-Calabrese 2010 method", flush=True)
print(f"Attempt B test : c =? kappa^2(SU(2)) = 1/4 (Bekenstein-Hawking)", flush=True)
print("=" * 78, flush=True)
jax.config.update("jax_enable_x64", True)
print(f"JAX : {jax.__version__}, backend : {jax.default_backend()}", flush=True)
print(f"Devices : {jax.devices()}", flush=True)


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


def make_link_swap_mask(L, axis=0):
    indices = jnp.indices((L, L, L, L))
    site_mask = indices[axis] < L // 2
    link_mask = jnp.zeros((L, L, L, L, 4), dtype=bool)
    for mu in range(4):
        endpoint2 = jnp.roll(site_mask, -1, axis=mu)
        link_mask = link_mask.at[..., mu].set(site_mask & endpoint2)
    return link_mask


def swap_pair(U1, U2, link_mask):
    mask = link_mask[..., None, None]
    U1_swap = jnp.where(mask, U2, U1)
    U2_swap = jnp.where(mask, U1, U2)
    return U1_swap, U2_swap


@jit
def interpolating_action(U1, U2, beta, lam, link_mask):
    U1s, U2s = swap_pair(U1, U2, link_mask)
    S_unswapped = wilson_action(U1, beta) + wilson_action(U2, beta)
    S_swapped = wilson_action(U1s, beta) + wilson_action(U2s, beta)
    return (1.0 - lam) * S_unswapped + lam * S_swapped


@jit
def deltaS_swap(U1, U2, beta, link_mask):
    U1s, U2s = swap_pair(U1, U2, link_mask)
    return (wilson_action(U1s, beta) + wilson_action(U2s, beta)
            - wilson_action(U1, beta) - wilson_action(U2, beta))


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
def metropolis_link_update(U_link, K_link, beta_eff, key, eps=0.3):
    key1, key2 = random.split(key)
    X = random_su2_near_identity(key1, U_link.shape[:-2], eps=eps)
    U_proposed = jnp.einsum('...ij,...jk->...ik', X, U_link)
    K_dag = jnp.conjugate(jnp.swapaxes(K_link, -1, -2))
    new_term = jnp.real(jnp.trace(jnp.einsum('...ij,...jk->...ik', U_proposed, K_dag),
                                    axis1=-2, axis2=-1))
    old_term = jnp.real(jnp.trace(jnp.einsum('...ij,...jk->...ik', U_link, K_dag),
                                    axis1=-2, axis2=-1))
    dS = -beta_eff * 0.5 * (new_term - old_term)
    rand_u = random.uniform(key2, dS.shape)
    accept = rand_u < jnp.exp(jnp.minimum(0.0, -dS))
    U_new = jnp.where(accept[..., None, None], U_proposed, U_link)
    return U_new


@partial(jit, static_argnames=('L',))
def metropolis_sweep_single(U, beta, key, L, eps=0.3):
    for mu in range(4):
        K_mu = compute_staple_sum_single(U, mu, L)
        key, subkey = random.split(key)
        U_mu_new = metropolis_link_update(U[..., mu, :, :], K_mu, beta, subkey, eps)
        U = U.at[..., mu, :, :].set(U_mu_new)
    return U


@partial(jit, static_argnames=('L',))
def metropolis_sweep_full_lambda(U1, U2, beta, lam, key, L, link_mask, eps=0.3):
    """Full-pair MH sweep under S_lambda — slower but correct for any lambda."""
    key1, key2, key3 = random.split(key, 3)
    X1 = random_su2_near_identity(key1, (L, L, L, L, 4), eps=eps)
    X2 = random_su2_near_identity(key2, (L, L, L, L, 4), eps=eps)
    U1_prop = jnp.einsum('...ij,...jk->...ik', X1, U1)
    U2_prop = jnp.einsum('...ij,...jk->...ik', X2, U2)
    S_old = interpolating_action(U1, U2, beta, lam, link_mask)
    S_new = interpolating_action(U1_prop, U2_prop, beta, lam, link_mask)
    dS = S_new - S_old
    rand_u = random.uniform(key3)
    accept = rand_u < jnp.exp(jnp.minimum(0.0, -dS))
    U1_out = jnp.where(accept, U1_prop, U1)
    U2_out = jnp.where(accept, U2_prop, U2)
    return U1_out, U2_out, accept


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


def reweighted_integrand(deltaS_samples, lam):
    """Compute reweighted <dS>_lam from samples drawn from S_0 ensemble.

    <dS>_lam = <dS · exp(-lam·dS)>_0 / <exp(-lam·dS)>_0

    Use log-sum-exp trick to avoid overflow for large lam·dS.
    """
    dS = np.asarray(deltaS_samples, dtype=np.float64)
    w_log = -lam * dS
    w_log_max = w_log.max()
    w_shifted = np.exp(w_log - w_log_max)
    Z = w_shifted.sum()
    mean = (dS * w_shifted).sum() / Z
    # SEM via jackknife / effective sample size
    ess = (w_shifted.sum())**2 / (w_shifted**2).sum()  # Kish's ESS
    # Sample variance under reweighted distribution
    var = ((dS - mean)**2 * w_shifted).sum() / Z
    sem = np.sqrt(var / max(ess, 1.0))
    return float(mean), float(sem), float(ess)


def run_TI_one_L(L, beta, lambda_grid, n_thermalize, n_decorr, n_samples, key, eps=0.3):
    """TI via per-link MH on each config independently at S_0, then reweight.

    Strategy:
      1. Per-link Metropolis on each config at full beta (samples from product ensemble).
      2. Measure dS = S(U1_swap) + S(U2_swap) - S(U1) - S(U2) on the swap pair.
      3. Reweight to estimate <dS>_lam for each lam (and ESS as quality metric).
      4. Integrate over lam.
    """
    link_mask = make_link_swap_mask(L, axis=0)
    print(f"\n--- L = {L}, beta = {beta}, A = L^3 = {L**3} ---", flush=True)

    print(f"Thermalize ({n_thermalize} sweeps per config)...", flush=True)
    t0 = time.time()
    U1, U2, key = thermalize_pair(key, beta, L, n_thermalize)
    print(f"Thermalized in {time.time()-t0:.1f}s", flush=True)

    print(f"Producing {n_samples} samples (decorr={n_decorr} sweeps)...", flush=True)
    t_prod = time.time()
    deltaS_samples = []
    S1_samples = []
    S2_samples = []
    for s in range(n_samples):
        for _ in range(n_decorr):
            key, k1, k2 = random.split(key, 3)
            U1 = metropolis_sweep_single(U1, beta, k1, L)
            U2 = metropolis_sweep_single(U2, beta, k2, L)
        dS = float(deltaS_swap(U1, U2, beta, link_mask))
        S1 = float(wilson_action(U1, beta))
        S2 = float(wilson_action(U2, beta))
        deltaS_samples.append(dS)
        S1_samples.append(S1)
        S2_samples.append(S2)
        if s == 0 or (s + 1) % max(1, n_samples // 10) == 0 or s == n_samples - 1:
            print(f"  sample {s+1}/{n_samples}: dS={dS:.4e}, S1={S1:.2f}, S2={S2:.2f}, "
                  f"t={time.time()-t_prod:.1f}s", flush=True)

    dS_arr = np.array(deltaS_samples)
    print(f"\nDS samples: mean={dS_arr.mean():.4e}, std={dS_arr.std():.4e}, "
          f"min={dS_arr.min():.4e}, max={dS_arr.max():.4e}", flush=True)

    # Reweighted integrand at each lambda
    print(f"Reweighting...", flush=True)
    integrand_means = []
    integrand_sems = []
    integrand_ess = []
    for lam in lambda_grid:
        m, sem, ess = reweighted_integrand(deltaS_samples, lam)
        integrand_means.append(m)
        integrand_sems.append(sem)
        integrand_ess.append(ess)
        ess_frac = ess / len(deltaS_samples)
        flag = "OK" if ess_frac > 0.1 else "LOW" if ess_frac > 0.01 else "DEGEN"
        print(f"  lam={lam:.3f}: <dS>_lam={m:.4e} +/- {sem:.4e}, ESS={ess:.1f} "
              f"({ess_frac:.2%}) {flag}", flush=True)

    lams = np.array(lambda_grid, dtype=float)
    means = np.array(integrand_means)
    sems = np.array(integrand_sems)

    S2_trap = float(np.trapezoid(means, lams)) if hasattr(np, 'trapezoid') else float(np.trapz(means, lams))
    try:
        from scipy.integrate import simpson
        S2_simp = float(simpson(means, x=lams))
    except Exception:
        S2_simp = S2_trap

    if len(lams) >= 2:
        dlam = lams[1] - lams[0]
        S2_err = float(dlam * np.sqrt(np.sum(sems**2)))
    else:
        S2_err = 0.0

    A_b = L * L * L
    return {
        'L': L, 'beta': beta, 'A_boundary': A_b,
        'method': 'per-link MH at S_0 + reweighting to S_lambda',
        'lambda_grid': lams.tolist(),
        'integrand_mean': means.tolist(),
        'integrand_sem': sems.tolist(),
        'integrand_ess': integrand_ess,
        'deltaS_samples': deltaS_samples,
        'S_2_simpson': S2_simp,
        'S_2_trapezoidal': S2_trap,
        'S_2': S2_simp,
        'S_2_err': S2_err,
        'c_proxy': S2_simp / A_b,
        'c_err': S2_err / A_b,
        'elapsed_s': time.time() - t0,
    }


def main():
    BETA = 2.4
    LAMBDAS = np.linspace(0.0, 1.0, 21).tolist()  # finer grid for reweighting

    # Per-link MH = fast per-sample, so we can take many samples
    runs_config = {
        4:  {'n_thermalize': 200, 'n_decorr': 5,  'n_samples': 2000},
        6:  {'n_thermalize': 300, 'n_decorr': 8,  'n_samples': 1500},
        8:  {'n_thermalize': 400, 'n_decorr': 10, 'n_samples': 1000},
        10: {'n_thermalize': 500, 'n_decorr': 15, 'n_samples': 500},
        12: {'n_thermalize': 600, 'n_decorr': 20, 'n_samples': 250},
    }

    all_results = {}

    for L in [4, 6, 8, 10, 12]:
        cfg = runs_config[L]
        print(f"\n{'='*78}\nLATTICE L = {L}\n{'='*78}", flush=True)
        key = random.PRNGKey(2026 + 31 * L)
        try:
            r = run_TI_one_L(L, BETA, LAMBDAS,
                             cfg['n_thermalize'], cfg['n_decorr'], cfg['n_samples'],
                             key)
            all_results[L] = r
            print(f"\nL={L}: S_2 = {r['S_2']:.4e} +/- {r['S_2_err']:.4e}", flush=True)
            print(f"      c = S_2/A = {r['c_proxy']:.6e} +/- {r['c_err']:.6e}", flush=True)
            print(f"      c / (1/4) = {r['c_proxy'] / 0.25:.4f}", flush=True)
        except Exception as e:
            print(f"L={L} FAILED : {e}", flush=True)
            import traceback
            traceback.print_exc()
        with open('/tmp/jax_su2_EE_donnellywall_results.json', 'w') as f:
            json.dump({
                'method': 'Donnelly-Wall Renyi-2 via thermodynamic integration',
                'reference': 'Caraglio-Gliozzi 2008 arXiv:0808.4094 + Alba et al 2010 arXiv:1005.0148',
                'beta': BETA, 'lambdas': LAMBDAS,
                'runs_config': runs_config,
                'results': {str(L): all_results[L] for L in all_results},
                'partial': True,
                'total_elapsed_s': time.time() - START,
            }, f, indent=2)

    print(f"\n{'='*78}\nSCALING ANALYSIS — Donnelly-Wall TI Renyi-2 EE\n{'='*78}", flush=True)
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
            'log(3)/(2*pi*sqrt(2)) = 0.1237 (Donnelly-Wall lit)': np.log(3) / (2 * np.pi * np.sqrt(2)),
            '2 * log(3)/(2*pi*sqrt(2)) = 0.2474 (horizon doubling)': np.log(3) / (np.pi * np.sqrt(2)),
            '3/(4*pi^2) = 0.0760 (lattice plaquette)': 3 / (4 * np.pi**2),
            '1/(2*pi) = 0.1592 (Cardy CFT)': 1 / (2 * np.pi),
            '1/12 = 0.0833 (CFT)': 1/12,
        }
        print(f"\nLeading coefficient candidates (vs L={L_max}) :", flush=True)
        for name, c_pred in candidates.items():
            z = (c_meas - c_pred) / max(c_err, 1e-6)
            sig = "OK" if abs(z) < 2 else "~" if abs(z) < 3 else "X"
            print(f"  {name:<55} : c_meas/c_pred = {c_meas/c_pred:.3f}, "
                  f"|Z|={abs(z):.2f} {sig}", flush=True)

    output = {
        'method': 'Donnelly-Wall Renyi-2 via thermodynamic integration',
        'reference': 'Caraglio-Gliozzi 2008 arXiv:0808.4094 + Alba et al 2010 arXiv:1005.0148',
        'beta': BETA, 'lambdas': LAMBDAS,
        'runs_config': runs_config,
        'results': {str(L): all_results[L] for L in all_results},
        'total_elapsed_s': time.time() - START,
    }
    with open('/tmp/jax_su2_EE_donnellywall_results.json', 'w') as f:
        json.dump(output, f, indent=2)

    print(f"\nTotal elapsed : {time.time() - START:.1f}s "
          f"({(time.time() - START)/60:.1f}min "
          f"= {(time.time() - START)/3600:.2f}h)", flush=True)
    print(f"Saved : /tmp/jax_su2_EE_donnellywall_results.json", flush=True)
    print(f"END : {time.ctime()}", flush=True)
    print(f"DONE.", flush=True)


if __name__ == "__main__":
    main()
