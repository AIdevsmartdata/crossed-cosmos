#!/usr/bin/env python3
"""Wilson loops V3 — 300 configs + σ(β) = κ²/a²(β) fit pour extraire κ² direct.

Plus de configs, plus de β, fit final extraction κ².

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
wilson_action = g['wilson_action']

START = time.time()
print(f"START : {time.ctime()}", flush=True)
print("=" * 78, flush=True)
print(f"Wilson loops V3 — 300 configs, fit σ(β)=κ²/a²(β) extract κ²", flush=True)
print("=" * 78, flush=True)


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
    """1-loop a²(β) for SU(2) Wilson. b₀=11/(48π²) for N=2."""
    g2 = 4.0 / beta
    return g2 * np.exp(-12 * np.pi**2 * beta / 22.0)


def plaquette_mean(U):
    return 1.0 - float(wilson_action(U, 1.0)) / (6 * U.shape[0]**4)


def run_one_LB(L, beta, n_thermalize, n_decorr, n_samples, key, R_max=None):
    if R_max is None:
        R_max = L // 2
    print(f"\n{'='*78}\nL={L}, β={beta}, R_max={R_max}, n_samples={n_samples}\n{'='*78}", flush=True)
    t0 = time.time()
    U, key = thermalize_standard(key, beta, L, n_thermalize, eps=0.3)
    p_init = plaquette_mean(U)
    print(f"Thermalized {n_thermalize} sweeps in {time.time()-t0:.1f}s, ⟨P⟩={p_init:.4f}", flush=True)

    if p_init < 0.4 or p_init > 0.85:
        print(f"  ⚠️ WARNING ⟨P⟩ hors range [0.4, 0.85] — thermalisation suspecte", flush=True)

    W_samples = []
    t0 = time.time()
    for s in range(n_samples):
        for _ in range(n_decorr):
            key, sk = random.split(key)
            U = metropolis_sweep_standard(U, beta, sk, L, eps=0.3)
        W = measure_wilson_loops_grid(U, R_max)
        W_samples.append(W)
        if s == 0 or (s+1) % max(1, n_samples//5) == 0 or s == n_samples-1:
            elapsed = time.time() - t0
            eta = elapsed * (n_samples - s - 1) / (s + 1)
            print(f"  s={s+1}/{n_samples} W(2,2)={W[2,2]:.4f} t={elapsed:.1f}s ETA={eta:.1f}s", flush=True)

    W_arr = np.array(W_samples)
    chi_jack = []
    for skip in range(n_samples):
        mask = np.arange(n_samples) != skip
        W_jack = W_arr[mask].mean(axis=0)
        chi_R = [creutz_ratio_RT(W_jack, R, R) for R in range(2, R_max + 1)]
        chi_jack.append(chi_R)
    chi_jack = np.array(chi_jack)
    chi_mean = chi_jack.mean(axis=0)
    chi_err = np.sqrt((n_samples - 1) / n_samples * ((chi_jack - chi_mean)**2).sum(axis=0))
    print(f"\n  Creutz χ(R,R) :", flush=True)
    for i, R in enumerate(range(2, R_max + 1)):
        print(f"  R={R} : χ = {chi_mean[i]:.4f} ± {chi_err[i]:.4f}", flush=True)

    return {
        'L': L, 'beta': beta, 'R_max': R_max, 'n_samples': n_samples,
        'plaquette_initial': p_init,
        'W_mean': W_arr.mean(axis=0).tolist(),
        'W_sem': (W_arr.std(axis=0) / np.sqrt(n_samples)).tolist(),
        'chi_R_values': list(range(2, R_max + 1)),
        'chi_mean': chi_mean.tolist(),
        'chi_err': chi_err.tolist(),
        'W_samples': W_arr.tolist(),
    }


def main():
    BETAS = [2.3, 2.4, 2.5, 2.6, 2.7]
    L = 12
    cfg = {'n_thermalize': 500, 'n_decorr': 10, 'n_samples': 300}

    all_results = {}
    for beta in BETAS:
        key = random.PRNGKey(10501 + int(beta * 100))
        try:
            r = run_one_LB(L, beta, cfg['n_thermalize'], cfg['n_decorr'],
                            cfg['n_samples'], key, R_max=L//2)
            all_results[beta] = r
        except Exception as e:
            print(f"L={L} β={beta} FAILED: {e}", flush=True)
            import traceback
            traceback.print_exc()
        with open('/tmp/jax_su2_wilson_loops_creutz_v3.json', 'w') as f:
            json.dump({
                'method': 'Wilson loops V3 — 300 configs + σ fit κ²',
                'L': L, 'betas': BETAS, 'config': cfg,
                'results': {str(b): all_results[b] for b in all_results},
                'partial': True,
                'total_elapsed_s': time.time() - START,
            }, f, indent=2)

    # =========================================================================
    # Fit σ_lat(β) ∝ 1/a²(β) → extraction κ²
    # =========================================================================
    print(f"\n{'='*78}\nσ_lat(β) from Creutz χ at largest R\n{'='*78}", flush=True)
    print(f"\n{'β':>5} {'⟨P⟩':>8} {'a²(β)':>12} {'σ_lat (R=L/2-1)':>18} {'σ_lat/a²':>14}")
    print("-" * 70)
    sigma_data = {}
    for beta in BETAS:
        if beta not in all_results:
            continue
        r = all_results[beta]
        chi_arr = np.array(r['chi_mean'])
        chi_err_arr = np.array(r['chi_err'])
        # Use R = L/2 - 1 = 5 as best estimate (largest R that has reasonable stats)
        idx = -2  # second-to-last (R=L/2-1 in chi list)
        sigma = chi_arr[idx]
        sigma_err = chi_err_arr[idx]
        a2 = a2_1loop_su2(beta)
        sigma_physical = sigma / a2 if a2 > 0 else float('nan')
        sigma_data[beta] = (sigma, sigma_err, a2)
        print(f"{beta:>5.2f} {r['plaquette_initial']:>8.4f} {a2:>12.4e} "
              f"{sigma:>10.4f} ± {sigma_err:>5.4f}     {sigma_physical:>10.3e}")

    # Linear fit through origin: σ_lat = κ² · a²(β) — extract κ²
    print(f"\n=== Linear fit σ_lat = κ² · a²(β) (no const) ===", flush=True)
    if len(sigma_data) >= 2:
        beta_arr = np.array(sorted(sigma_data.keys()))
        sig = np.array([sigma_data[b][0] for b in beta_arr])
        err = np.array([sigma_data[b][1] for b in beta_arr])
        a2 = np.array([sigma_data[b][2] for b in beta_arr])

        w = 1.0 / np.maximum(err**2, 1e-20)
        # σ = κ² · a² → κ² = Σ(w·σ·a²) / Σ(w·a⁴)
        kappa_sq = np.sum(w * sig * a2) / np.sum(w * a2**2)
        kappa_sq_err = 1.0 / np.sqrt(np.sum(w * a2**2))
        # χ²/dof
        residuals = sig - kappa_sq * a2
        chi2 = np.sum(w * residuals**2)
        dof = len(sig) - 1
        print(f"  κ² = {kappa_sq:.4e} ± {kappa_sq_err:.2e}", flush=True)
        print(f"  χ²/dof = {chi2:.2f}/{dof}", flush=True)
        print(f"\n  Comparaisons :", flush=True)
        print(f"    BH leading κ² = 1/4 = 0.25", flush=True)
        print(f"    ECI |Φ⁺(SU(2))|⁻² = 1 (avec κ=1, κ²=1)", flush=True)
        print(f"    ECI 1/(N(N-1))² = 1/4 = 0.25 (avec κ=1/(N(N-1))=1/2 pour N=2)", flush=True)
        if abs(kappa_sq - 0.25) / max(kappa_sq_err, abs(kappa_sq) * 0.1) < 3:
            print(f"  ★★★ Compatible avec κ²=1/4 dans {abs(kappa_sq-0.25)/kappa_sq_err:.1f}σ", flush=True)

    output = {
        'method': 'Wilson loops V3 — 300 configs + σ fit κ²',
        'L': L, 'betas': BETAS, 'config': cfg,
        'results': {str(b): all_results[b] for b in all_results},
        'sigma_data': {str(b): list(sigma_data[b]) for b in sigma_data},
        'kappa_squared_fit': {'kappa_sq': float(kappa_sq) if len(sigma_data) >= 2 else None,
                               'kappa_sq_err': float(kappa_sq_err) if len(sigma_data) >= 2 else None,
                               'chi2_dof': f'{chi2:.2f}/{dof}' if len(sigma_data) >= 2 else None},
        'total_elapsed_s': time.time() - START,
    }
    with open('/tmp/jax_su2_wilson_loops_creutz_v3.json', 'w') as f:
        json.dump(output, f, indent=2)

    print(f"\nTotal elapsed : {time.time() - START:.1f}s ({(time.time() - START)/60:.1f}min)", flush=True)
    print(f"END : {time.ctime()}", flush=True)


if __name__ == "__main__":
    main()
