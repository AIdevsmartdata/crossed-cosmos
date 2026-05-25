#!/usr/bin/env python3
"""Wilson loops + Creutz ratios V2 — 200 configs, APE smearing.

Post bug-fix : enough statistics + smearing to extract σ_string cleanly.

APE smearing (Albanese-Pendleton-Caracciolo-Falcioni-Sancho 1987) projects
to su(2) the smeared link to enhance long-distance signal :
  U_smeared = Proj_SU(2)( ρ · U + Σ staples )

Multiple smearing levels (n_smear=0, 4, 8, 16) to find plateau.

Author : Kévin Rémondière (ORCID 0009-0008-2443-7166).
"""
import os
os.environ.setdefault('XLA_PYTHON_CLIENT_PREALLOCATE', 'false')
os.environ.setdefault('JAX_ENABLE_X64', 'True')

import sys
sys.path.insert(0, '/tmp')

with open('/tmp/jax_su2_EE_MODULAR_2026-05-25.py') as f:
    src = f.read()
src = src.split('if __name__')[0]
g = {}
exec(src, g)

import time
import json
import numpy as np
import jax
import jax.numpy as jnp
from jax import random, jit
from functools import partial

metropolis_sweep_standard = g['metropolis_sweep_standard']
thermalize_standard = g['thermalize_standard']
compute_staple_sum = g['compute_staple_sum']
wilson_action = g['wilson_action']

START = time.time()
print(f"START : {time.ctime()}", flush=True)
print("=" * 78, flush=True)
print(f"Wilson loops V2 — 200 configs, APE smearing — POST BUG FIX", flush=True)
print("=" * 78, flush=True)


# ============================================================================
# APE smearing for SU(2)
# ============================================================================

@partial(jit, static_argnames=('mu', 'L'))
def ape_smear_one_link(U, mu, L, rho=0.5):
    """One step APE smearing of links in direction μ.

    U_smeared = SU(2)-projection of (1-ρ)·U + ρ·sum_of_staples
    For SU(2), projection = normalize a-vector.
    """
    K_mu = compute_staple_sum(U, mu, L)
    # Smeared raw matrix: (1-ρ)·U + ρ·K
    M = (1 - rho) * U[..., mu, :, :] + rho * K_mu
    # SU(2) projection : write M = a₀·I + i·(a·σ) and normalize
    # For SU(2): U = [[a₀+i·a₃, a₂+i·a₁], [-a₂+i·a₁, a₀-i·a₃]]
    # Extract from M (which is general complex 2×2):
    a0 = 0.5 * jnp.real(M[..., 0, 0] + M[..., 1, 1])
    a3 = 0.5 * jnp.imag(M[..., 0, 0] - M[..., 1, 1])
    a2 = 0.5 * jnp.real(M[..., 0, 1] - M[..., 1, 0])
    a1 = 0.5 * jnp.imag(M[..., 0, 1] + M[..., 1, 0])
    norm = jnp.sqrt(a0**2 + a1**2 + a2**2 + a3**2)
    a0 = a0 / norm
    a1 = a1 / norm
    a2 = a2 / norm
    a3 = a3 / norm
    U_new = jnp.stack([
        jnp.stack([a0 + 1j * a3, a2 + 1j * a1], axis=-1),
        jnp.stack([-a2 + 1j * a1, a0 - 1j * a3], axis=-1),
    ], axis=-2)
    return U_new


def ape_smear_all(U, L, rho=0.5, n_steps=4):
    """N steps of APE smearing on ALL links."""
    for _ in range(n_steps):
        U_new = jnp.zeros_like(U)
        for mu in range(4):
            U_smeared_mu = ape_smear_one_link(U, mu, L, rho)
            U_new = U_new.at[..., mu, :, :].set(U_smeared_mu)
        U = U_new
    return U


# ============================================================================
# Wilson loops (reuse from V1)
# ============================================================================

@partial(jit, static_argnames=('mu', 'length'))
def parallel_transport(U, mu, length):
    P = U[..., mu, :, :]
    for k in range(1, length):
        U_shift = jnp.roll(U[..., mu, :, :], -k, axis=mu)
        P = jnp.einsum('...ij,...jk->...ik', P, U_shift)
    return P


@partial(jit, static_argnames=('mu', 'nu', 'R', 'T'))
def wilson_loop_plane(U, mu, nu, R, T):
    T_mu = parallel_transport(U, mu, R)
    T_nu_atμ = jnp.roll(parallel_transport(U, nu, T), -R, axis=mu)
    T_mu_atν = jnp.roll(parallel_transport(U, mu, R), -T, axis=nu)
    T_nu = parallel_transport(U, nu, T)
    W = jnp.einsum('...ij,...jk,...lk,...ml->...im',
                   T_mu, T_nu_atμ,
                   jnp.conjugate(T_mu_atν),
                   jnp.conjugate(T_nu))
    return jnp.real(jnp.trace(W, axis1=-2, axis2=-1)).mean() / 2.0


def measure_wilson_loops_grid(U, R_max):
    W = np.zeros((R_max + 1, R_max + 1))
    pairs = [(0, 1), (0, 2), (0, 3), (1, 2), (1, 3), (2, 3)]
    for R in range(1, R_max + 1):
        for T in range(1, R_max + 1):
            total = 0.0
            for mu, nu in pairs:
                total += float(wilson_loop_plane(U, mu, nu, R, T))
            W[R, T] = total / 6.0
    return W


def creutz_ratio_RT(W, R, T):
    num = W[R, T] * W[R-1, T-1]
    den = W[R, T-1] * W[R-1, T]
    if num <= 0 or den <= 0:
        return float('nan')
    return -np.log(num / den)


def a2_1loop_su2(beta):
    g2 = 4.0 / beta
    return g2 * np.exp(-12 * np.pi**2 * beta / 22.0)


def plaquette_mean(U):
    return 1.0 - float(wilson_action(U, 1.0)) / (6 * U.shape[0]**4)


def run_one_LB(L, beta, n_thermalize, n_decorr, n_samples, key, R_max=None,
                ape_n_steps=4, ape_rho=0.5):
    if R_max is None:
        R_max = L // 2
    print(f"\n{'='*78}\nL={L}, β={beta}, R_max={R_max}, n_samples={n_samples}, "
          f"ape_smear_n={ape_n_steps}\n{'='*78}", flush=True)
    t0 = time.time()
    U, key = thermalize_standard(key, beta, L, n_thermalize, eps=0.3)
    p_init = plaquette_mean(U)
    print(f"Thermalized {n_thermalize} sweeps in {time.time()-t0:.1f}s, ⟨P⟩={p_init:.4f}", flush=True)

    W_samples_unsmeared = []
    W_samples_smeared = []

    t0 = time.time()
    for s in range(n_samples):
        for _ in range(n_decorr):
            key, sk = random.split(key)
            U = metropolis_sweep_standard(U, beta, sk, L, eps=0.3)

        # Measure unsmeared Wilson loops
        W_unsm = measure_wilson_loops_grid(U, R_max)
        W_samples_unsmeared.append(W_unsm)

        # APE smear then measure
        if ape_n_steps > 0:
            U_smeared = ape_smear_all(U, L, rho=ape_rho, n_steps=ape_n_steps)
            W_sm = measure_wilson_loops_grid(U_smeared, R_max)
            W_samples_smeared.append(W_sm)

        if s == 0 or (s+1) % max(1, n_samples//5) == 0 or s == n_samples-1:
            elapsed = time.time() - t0
            eta = elapsed * (n_samples - s - 1) / (s + 1)
            print(f"  s={s+1}/{n_samples} W(2,2)_unsm={W_unsm[2,2]:.4f}"
                  + (f" W(2,2)_sm={W_sm[2,2]:.4f}" if ape_n_steps > 0 else "")
                  + f" t={elapsed:.1f}s ETA={eta:.1f}s", flush=True)

    result = {'L': L, 'beta': beta, 'R_max': R_max, 'n_samples': n_samples,
              'plaquette_initial': p_init, 'ape_n_steps': ape_n_steps, 'ape_rho': ape_rho}

    for name, W_list in [('unsmeared', W_samples_unsmeared), ('smeared', W_samples_smeared)]:
        if not W_list:
            continue
        W_arr = np.array(W_list)
        # Jackknife Creutz
        chi_jack = []
        for skip in range(n_samples):
            mask = np.arange(n_samples) != skip
            W_jack = W_arr[mask].mean(axis=0)
            chi_R = [creutz_ratio_RT(W_jack, R, R) for R in range(2, R_max + 1)]
            chi_jack.append(chi_R)
        chi_jack = np.array(chi_jack)
        chi_mean = chi_jack.mean(axis=0)
        chi_err = np.sqrt((n_samples - 1) / n_samples * ((chi_jack - chi_mean)**2).sum(axis=0))
        print(f"\n  [{name}] Creutz χ(R,R):", flush=True)
        for i, R in enumerate(range(2, R_max + 1)):
            print(f"  R={R} : χ = {chi_mean[i]:.4f} ± {chi_err[i]:.4f}", flush=True)
        result[name] = {
            'W_mean': W_arr.mean(axis=0).tolist(),
            'W_sem': (W_arr.std(axis=0) / np.sqrt(n_samples)).tolist(),
            'chi_R_values': list(range(2, R_max + 1)),
            'chi_mean': chi_mean.tolist(),
            'chi_err': chi_err.tolist(),
        }

    return result


def main():
    BETAS = [2.3, 2.4, 2.5, 2.6, 2.7]
    L = 12

    cfg = {'n_thermalize': 500, 'n_decorr': 10, 'n_samples': 200,
           'ape_n_steps': 4, 'ape_rho': 0.5}

    all_results = {}
    for beta in BETAS:
        key = random.PRNGKey(9101 + int(beta * 100))
        try:
            r = run_one_LB(L, beta, cfg['n_thermalize'], cfg['n_decorr'],
                            cfg['n_samples'], key, R_max=L//2,
                            ape_n_steps=cfg['ape_n_steps'], ape_rho=cfg['ape_rho'])
            all_results[beta] = r
        except Exception as e:
            print(f"L={L} β={beta} FAILED: {e}", flush=True)
            import traceback
            traceback.print_exc()
        with open('/tmp/jax_su2_wilson_loops_creutz_v2.json', 'w') as f:
            json.dump({
                'method': 'Wilson loops V2 — 200 configs + APE smearing — POST BUG FIX',
                'L': L, 'betas': BETAS, 'config': cfg,
                'results': {str(b): all_results[b] for b in all_results},
                'partial': True,
                'total_elapsed_s': time.time() - START,
            }, f, indent=2)

    # Final summary
    print(f"\n{'='*78}\nσ_lattice from APE-smeared Creutz plateau\n{'='*78}", flush=True)
    print(f"\n{'β':>5} {'a²(β)':>12} {'σ_lat smeared (R=4)':>22} {'σ_lat unsm (R=4)':>20}")
    print("-" * 70)
    for beta in BETAS:
        if beta not in all_results:
            continue
        r = all_results[beta]
        a2 = a2_1loop_su2(beta)
        sigma_sm = r.get('smeared', {}).get('chi_mean', [np.nan]*5)[2]  # R=4 = index 2
        sigma_un = r.get('unsmeared', {}).get('chi_mean', [np.nan]*5)[2]
        print(f"{beta:>5.2f} {a2:>12.4e} {sigma_sm:>10.4f}              {sigma_un:>10.4f}")

    output = {
        'method': 'Wilson loops V2 — 200 configs + APE smearing — POST BUG FIX',
        'L': L, 'betas': BETAS, 'config': cfg,
        'results': {str(b): all_results[b] for b in all_results},
        'total_elapsed_s': time.time() - START,
    }
    with open('/tmp/jax_su2_wilson_loops_creutz_v2.json', 'w') as f:
        json.dump(output, f, indent=2)
    print(f"\nTotal elapsed : {time.time() - START:.1f}s ({(time.time() - START)/60:.1f}min)", flush=True)
    print(f"END : {time.ctime()}", flush=True)


if __name__ == "__main__":
    main()
