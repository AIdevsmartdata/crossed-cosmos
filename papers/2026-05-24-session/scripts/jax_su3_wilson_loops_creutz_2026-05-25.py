#!/usr/bin/env python3
"""SU(3) Wilson loops Creutz ratios → κ² extraction direct.

TEST CRITIQUE ECI : ratio σ_phys(SU(3))/σ_phys(SU(2)) = κ²_SU(3)/κ²_SU(2) = 1/9

À matched 't Hooft scale :
  β_SU(2) = 2.4  ↔  β_SU(3) = 5.4
  β_SU(2) = 2.6  ↔  β_SU(3) = 5.85

Prédictions ECI vs BH :
  ECI |Φ⁺(SU(3))|⁻² = 1/(3·2)² = 1/36 = 0.0278
  BH κ² = 1/4 = 0.25 (universel)

Ratio prédit ECI : σ_lat(SU(3))/σ_lat(SU(2)) = 1/9 ≈ 0.111
Ratio prédit BH  : σ_lat(SU(3))/σ_lat(SU(2)) = 1  (factor 1)

→ test discriminant facteur 9 sur observable mesurable propre.

Author : Kévin Rémondière (ORCID 0009-0008-2443-7166).
"""
import os
os.environ.setdefault('XLA_PYTHON_CLIENT_PREALLOCATE', 'false')
os.environ.setdefault('JAX_ENABLE_X64', 'True')

import sys
sys.path.insert(0, '/tmp')

with open('/tmp/jax_su3_lattice_2026-05-25.py') as f:
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

random_su3_haar = g['random_su3_haar']
metropolis_sweep_su3 = g['metropolis_sweep_su3']
wilson_action_su3 = g['wilson_action_su3']
plaquette_mean_su3 = g['plaquette_mean_su3']

START = time.time()
print(f"START : {time.ctime()}", flush=True)
print("=" * 78, flush=True)
print(f"SU(3) Wilson loops Creutz — κ² test cross-N (ECI vs BH)", flush=True)
print("=" * 78, flush=True)


# ============================================================================
# Wilson loops SU(3) — BATCH JIT same pattern as V6
# ============================================================================

@partial(jit, static_argnames=('R_max',))
def measure_all_wilson_loops_su3(U, R_max):
    """All W(R, T) for R, T ∈ 1..R_max, 6 planes averaged. Single JIT compile.

    SU(3) normalization : Re Tr(W) / 3.
    """
    pairs = [(0, 1), (0, 2), (0, 3), (1, 2), (1, 3), (2, 3)]
    W_sum = jnp.zeros((R_max + 1, R_max + 1))
    for mu, nu in pairs:
        U_mu = U[..., mu, :, :]
        P_mu_list = [U_mu]
        P = U_mu
        for k in range(1, R_max):
            U_shift = jnp.roll(U_mu, -k, axis=mu)
            P = jnp.einsum('...ij,...jk->...ik', P, U_shift)
            P_mu_list.append(P)
        U_nu = U[..., nu, :, :]
        P_nu_list = [U_nu]
        P = U_nu
        for k in range(1, R_max):
            U_shift = jnp.roll(U_nu, -k, axis=nu)
            P = jnp.einsum('...ij,...jk->...ik', P, U_shift)
            P_nu_list.append(P)
        for R in range(1, R_max + 1):
            for T in range(1, R_max + 1):
                T_mu = P_mu_list[R - 1]
                T_nu_atμ = jnp.roll(P_nu_list[T - 1], -R, axis=mu)
                T_mu_atν = jnp.roll(P_mu_list[R - 1], -T, axis=nu)
                T_nu = P_nu_list[T - 1]
                W_mat = jnp.einsum('...ij,...jk,...lk,...ml->...im',
                                   T_mu, T_nu_atμ,
                                   jnp.conjugate(T_mu_atν),
                                   jnp.conjugate(T_nu))
                w_val = jnp.real(jnp.trace(W_mat, axis1=-2, axis2=-1)).mean() / 3.0  # /N=3
                W_sum = W_sum.at[R, T].add(w_val)
    return W_sum / 6.0


def creutz_ratio_RT(W, R, T):
    num = W[R, T] * W[R-1, T-1]
    den = W[R, T-1] * W[R-1, T]
    if num <= 0 or den <= 0:
        return float('nan')
    return -np.log(num / den)


def a2_1loop_su3(beta):
    """1-loop a²(β) for SU(3) Wilson. b₀ = 11N/(48π²) = 33/(48π²) for SU(3)."""
    g2 = 6.0 / beta  # for SU(3) Wilson β = 2N/g² = 6/g²
    return g2 * np.exp(-48 * np.pi**2 * beta / 33.0)


# Verbose thermalize for SU(3)
def thermalize_verbose_su3(key, beta, L, n_sweeps, eps=0.2):
    k, sk = random.split(key)
    U = random_su3_haar(sk, (L, L, L, L, 4))
    t0 = time.time()
    for i in range(n_sweeps):
        k, sk = random.split(k)
        U = metropolis_sweep_su3(U, beta, sk, L, eps)
        if i == 0:
            U.block_until_ready()
            print(f"  thermalize sweep 1 done (JIT compile) in {time.time()-t0:.1f}s", flush=True)
        elif (i+1) % max(1, n_sweeps // 5) == 0:
            U.block_until_ready()
            elapsed = time.time() - t0
            print(f"  thermalize {i+1}/{n_sweeps} sweeps, {elapsed:.1f}s "
                  f"({elapsed/(i+1)*1000:.1f}ms/sweep)", flush=True)
    return U, k


def run_one_LB(L, beta, n_thermalize, n_decorr, n_samples, key, R_max=6, eps=0.2):
    print(f"\n{'='*78}\nL={L}, β={beta} (SU(3)), R_max={R_max}, n_samples={n_samples}\n"
          f"{'='*78}", flush=True)
    t0 = time.time()
    U, key = thermalize_verbose_su3(key, beta, L, n_thermalize, eps=eps)
    p_init = plaquette_mean_su3(U)
    print(f"Thermalized in {time.time()-t0:.1f}s, ⟨P⟩={p_init:.4f}", flush=True)
    if p_init < 0.25 or p_init > 0.75:
        print(f"  ⚠️ ⟨P⟩ hors range raisonnable — SKIP", flush=True)
        return None

    print(f"JIT compile measure_all_wilson_loops_su3(R_max={R_max})...", flush=True)
    t_jit = time.time()
    W_warmup = measure_all_wilson_loops_su3(U, R_max)
    W_warmup.block_until_ready()
    print(f"JIT done in {time.time()-t_jit:.1f}s", flush=True)

    W_samples = []
    t0 = time.time()
    for s in range(n_samples):
        for _ in range(n_decorr):
            key, sk = random.split(key)
            U = metropolis_sweep_su3(U, beta, sk, L, eps=eps)
        W = np.array(measure_all_wilson_loops_su3(U, R_max))
        W_samples.append(W)
        if s == 0 or (s+1) % max(1, n_samples//10) == 0 or s == n_samples-1:
            elapsed = time.time() - t0
            eta = elapsed * (n_samples - s - 1) / (s + 1)
            print(f"  s={s+1}/{n_samples} W(3,3)={W[3,3]:.4e} t={elapsed:.1f}s ETA={eta/60:.1f}min",
                  flush=True)

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
        print(f"  R={R} : χ = {chi_mean[i]:.5f} ± {chi_err[i]:.5f}", flush=True)

    return {
        'L': L, 'beta': beta, 'R_max': R_max, 'n_samples': n_samples,
        'plaquette_initial': p_init,
        'W_mean': W_arr.mean(axis=0).tolist(),
        'W_sem': (W_arr.std(axis=0) / np.sqrt(n_samples)).tolist(),
        'chi_R_values': list(range(2, R_max + 1)),
        'chi_mean': chi_mean.tolist(),
        'chi_err': chi_err.tolist(),
    }


def main():
    # Matched 't Hooft to SU(2) β=2.3,2.4,2.5,2.6,2.7 → SU(3) β=5.175, 5.4, 5.625, 5.85, 6.075
    # Round to nice values : β=5.2, 5.4, 5.6, 5.8, 6.0
    BETAS = [5.2, 5.4, 5.6, 5.8, 6.0]
    L = 12
    cfg = {'n_thermalize': 1000, 'n_decorr': 20, 'n_samples': 500}
    R_max = 6

    all_results = {}
    for beta in BETAS:
        key = random.PRNGKey(13301 + int(beta * 100))
        try:
            r = run_one_LB(L, beta, cfg['n_thermalize'], cfg['n_decorr'],
                            cfg['n_samples'], key, R_max=R_max, eps=0.2)
            if r is not None:
                all_results[beta] = r
        except Exception as e:
            print(f"L={L} β={beta} FAILED: {e}", flush=True)
            import traceback
            traceback.print_exc()
        with open('/tmp/jax_su3_wilson_loops_creutz.json', 'w') as f:
            json.dump({
                'method': 'SU(3) Wilson loops Creutz — ECI vs BH test',
                'L': L, 'betas': BETAS, 'config': cfg,
                'results': {str(b): all_results[b] for b in all_results},
                'partial': True,
                'total_elapsed_s': time.time() - START,
            }, f, indent=2)

    print(f"\n{'='*78}\nκ²(SU(3)) extraction\n{'='*78}", flush=True)
    print(f"\n{'β':>5} {'⟨P⟩':>8} {'a²(β)':>11} ", end="")
    for R in range(3, 7):
        print(f"{'χ(R=' + str(R) + ')':>15}", end="")
    print()
    for beta in BETAS:
        if beta not in all_results:
            continue
        r = all_results[beta]
        chi_arr = np.array(r['chi_mean'])
        chi_err_arr = np.array(r['chi_err'])
        a2 = a2_1loop_su3(beta)
        print(f"{beta:>5.2f} {r['plaquette_initial']:>8.4f} {a2:>11.3e}", end="")
        for i, R in enumerate(range(2, 7)):
            if i < len(chi_arr):
                s = f"{chi_arr[i]:.4f}±{chi_err_arr[i]:.4f}"
                print(f"{s:>15}", end="")
        print()

    # Extract sigma_lat plateau
    sigma_data = []
    for beta in BETAS:
        if beta not in all_results:
            continue
        r = all_results[beta]
        chi_arr = np.array(r['chi_mean'])
        chi_err_arr = np.array(r['chi_err'])
        R_use = [2, 3, 4]  # χ(R=4,5,6)
        chi_vals = chi_arr[R_use]
        chi_errs = chi_err_arr[R_use]
        finite = ~np.isnan(chi_vals) & (chi_errs > 0)
        if finite.sum() == 0:
            continue
        w = 1.0 / chi_errs[finite]**2
        sigma_est = np.sum(w * chi_vals[finite]) / np.sum(w)
        sigma_err_est = 1.0 / np.sqrt(np.sum(w))
        a2 = a2_1loop_su3(beta)
        sigma_data.append((beta, sigma_est, sigma_err_est, a2))

    print(f"\n=== Fit σ_lat = κ²·a²(β) ===", flush=True)
    for beta, s_e, s_err, a2 in sigma_data:
        print(f"  β={beta}: σ_lat = {s_e:.5f} ± {s_err:.5f}  (a²={a2:.3e})", flush=True)

    kappa_sq = None
    if len(sigma_data) >= 2:
        sd = np.array(sigma_data)
        sig = sd[:, 1]
        err = sd[:, 2]
        a2 = sd[:, 3]
        w = 1.0 / err**2
        kappa_sq = np.sum(w * sig * a2) / np.sum(w * a2**2)
        kappa_sq_err = 1.0 / np.sqrt(np.sum(w * a2**2))
        residuals = sig - kappa_sq * a2
        chi2 = np.sum(w * residuals**2)
        dof = len(sig) - 1
        print(f"\n  κ²(SU(3)) = {kappa_sq:.4e} ± {kappa_sq_err:.2e}", flush=True)
        print(f"  χ²/dof = {chi2:.2f}/{dof}", flush=True)
        print(f"\n  Comparaisons :", flush=True)
        print(f"    ECI |Φ⁺(SU(3))|⁻² = 1/36 = {1/36:.4e}", flush=True)
        print(f"    BH κ² = 1/4 = {1/4:.4e}", flush=True)
        if abs(kappa_sq - 1/36) / max(kappa_sq_err, abs(kappa_sq) * 0.1) < 3:
            print(f"  ★★★ Compatible ECI κ²=1/36 dans {abs(kappa_sq-1/36)/kappa_sq_err:.2f}σ", flush=True)
        if abs(kappa_sq - 1/4) / max(kappa_sq_err, abs(kappa_sq) * 0.1) < 3:
            print(f"  ★★★ Compatible BH κ²=1/4 dans {abs(kappa_sq-1/4)/kappa_sq_err:.2f}σ", flush=True)

    output = {
        'method': 'SU(3) Wilson loops Creutz — ECI vs BH test',
        'L': L, 'betas': BETAS, 'config': cfg,
        'results': {str(b): all_results[b] for b in all_results},
        'sigma_data': [{'beta': float(s[0]), 'sigma_lat': float(s[1]),
                        'sigma_err': float(s[2]), 'a2': float(s[3])} for s in sigma_data],
        'kappa_squared_fit': {'kappa_sq': float(kappa_sq) if kappa_sq is not None else None,
                               'kappa_sq_err': float(kappa_sq_err) if kappa_sq is not None else None,
                               'chi2_dof': f'{chi2:.2f}/{dof}' if kappa_sq is not None else None},
        'total_elapsed_s': time.time() - START,
    }
    with open('/tmp/jax_su3_wilson_loops_creutz.json', 'w') as f:
        json.dump(output, f, indent=2)
    print(f"\nTotal elapsed : {time.time() - START:.1f}s ({(time.time() - START)/60:.1f}min)", flush=True)


if __name__ == "__main__":
    main()
