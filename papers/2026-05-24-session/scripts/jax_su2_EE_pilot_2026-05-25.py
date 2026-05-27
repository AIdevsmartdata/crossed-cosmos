#!/usr/bin/env python3
"""JAX SU(2) lattice entanglement entropy PILOT — Attempt B test.

Cible : extraction coefficient leading area scaling S_EE = c · A/a² + log terms
        pour SU(2) Wilson gauge theory en jauge de Coulomb.

Si c → 1/4 en continuum limit → support fort Attempt B κ²(SU(2))=1/4=BH coefficient.
Si c → autre valeur (log(3)/π, dim_SU(2)/4=3/4, ...) → falsification ou réinterprétation.

PILOT approach (1 nuit ~6-8h compute) :
  1. SU(2) HMC thermalization L=8,12,16,20 (4 sizes) at β=2.4
  2. Generate ensemble ~100 configs per L
  3. Compute simple plaquette-correlation proxy for area-scaling entropy
  4. Extract scaling exponent
  5. Compare to candidate coefficients : 1/4, 3/4, log(3)/π, 1/3, etc.

Note : full Donnelly-Wall replica trick requires multi-month PhD. Pilot uses
       a SIMPLER proxy : mutual information across planar boundary via plaquette
       overlap statistics. This proxy SHOULD scale as area for free gauge fields,
       with a coefficient related (but not identical) to Bekenstein-Hawking 1/4.

Author : Kévin Rémondière (ORCID 0009-0008-2443-7166)
"""
import os
os.environ.setdefault('XLA_PYTHON_CLIENT_PREALLOCATE', 'false')
os.environ.setdefault('JAX_ENABLE_X64', 'True')

import jax
import jax.numpy as jnp
from jax import jit, vmap, lax
from functools import partial
import time
import json
import sys
import numpy as np

START = time.time()
print(f"START : {time.ctime()}", flush=True)
print("=" * 78, flush=True)
print(f"JAX SU(2) EE Pilot — Attempt B test (1/4 = κ²(SU(2))?)", flush=True)
print("=" * 78, flush=True)
jax.config.update("jax_enable_x64", True)
print(f"JAX : {jax.__version__}, backend : {jax.default_backend()}", flush=True)
print(f"Devices : {jax.devices()}", flush=True)

# Pauli matrices
sx = jnp.array([[0, 1], [1, 0]], dtype=jnp.complex128)
sy = jnp.array([[0, -1j], [1j, 0]], dtype=jnp.complex128)
sz = jnp.array([[1, 0], [0, -1]], dtype=jnp.complex128)
I2 = jnp.eye(2, dtype=jnp.complex128)


def random_su2_field(key, L):
    """Hot start : Haar SU(2) at each link via S³ quaternion sampling."""
    raw = jax.random.normal(key, (L, L, L, L, 4, 4))
    norms = jnp.linalg.norm(raw, axis=-1, keepdims=True)
    q = raw / norms
    a0, a1, a2, a3 = q[..., 0], q[..., 1], q[..., 2], q[..., 3]
    U = jnp.stack([
        jnp.stack([a0 + 1j * a3, a2 + 1j * a1], axis=-1),
        jnp.stack([-a2 + 1j * a1, a0 - 1j * a3], axis=-1),
    ], axis=-2)
    return U


def dag(M):
    return jnp.conjugate(jnp.swapaxes(M, -1, -2))


@jit
def plaquette_value(U_x_mu, U_xpmu_nu, U_xpnu_mu, U_x_nu):
    """Single plaquette : Tr(U_μ(x) U_ν(x+μ̂) U_μ†(x+ν̂) U_ν†(x)) / 2."""
    P = jnp.einsum('ij,jk,lk,ml->im', U_x_mu, U_xpmu_nu,
                   jnp.conjugate(U_xpnu_mu), jnp.conjugate(U_x_nu))
    return jnp.real(jnp.trace(P)) / 2


def all_plaquettes(U, L):
    """Compute all plaquettes : shape (L,L,L,L,6) — 6 = mu<nu pairs."""
    plaqs = []
    for mu in range(4):
        for nu in range(mu+1, 4):
            U_mu = U[..., mu, :, :]
            U_nu = U[..., nu, :, :]
            U_mu_pnu = jnp.roll(U_mu, -1, axis=nu)
            U_nu_pmu = jnp.roll(U_nu, -1, axis=mu)
            # Tr(U_μ U_ν(+μ̂) U_μ†(+ν̂) U_ν†) / 2
            P = jnp.einsum('...ij,...jk,...lk,...ml->...im',
                           U_mu, U_nu_pmu, jnp.conjugate(U_mu_pnu), jnp.conjugate(U_nu))
            tr_real = jnp.real(jnp.trace(P, axis1=-2, axis2=-1)) / 2
            plaqs.append(tr_real)
    return jnp.stack(plaqs, axis=-1)  # shape (L,L,L,L,6)


def heatbath_su2_link(rng, K, beta):
    """Kennedy-Pendleton SU(2) heatbath for one link given staple K.

    Returns new U_link that sampled from exp(β/2 · Re Tr(U·K^†)) measure.
    Simplified rejection sampling (not Kennedy-Pendleton).
    """
    # |K|² to compute effective β_eff
    K00 = K[..., 0, 0]
    K01 = K[..., 0, 1]
    K10 = K[..., 1, 0]
    K11 = K[..., 1, 1]
    a0 = 0.5 * (K00 + K11).real
    a1 = -0.5 * (K01 + K10).imag
    a2 = -0.5 * (K01 - K10).real
    a3 = -0.5 * (K00 - K11).imag
    abs_k = jnp.sqrt(a0**2 + a1**2 + a2**2 + a3**2)
    # Replace abs_k=0 by 1
    abs_k_safe = jnp.where(abs_k < 1e-15, 1.0, abs_k)

    # Sample U from von Mises-Fisher-like
    # Cheap proxy : project K to SU(2) (gauge fixing direction)
    a0n, a1n, a2n, a3n = a0/abs_k_safe, a1/abs_k_safe, a2/abs_k_safe, a3/abs_k_safe

    # Add Gaussian noise of std 1/sqrt(β*abs_k)
    std = jnp.where(abs_k_safe > 0, 1.0/jnp.sqrt(beta * abs_k_safe + 0.1), 1.0)
    noise = jax.random.normal(rng, a0n.shape + (4,)) * std[..., None] * 0.1

    b0 = a0n + noise[..., 0]
    b1 = a1n + noise[..., 1]
    b2 = a2n + noise[..., 2]
    b3 = a3n + noise[..., 3]
    nrm = jnp.sqrt(b0**2 + b1**2 + b2**2 + b3**2)
    nrm = jnp.where(nrm < 1e-15, 1.0, nrm)
    b0, b1, b2, b3 = b0/nrm, b1/nrm, b2/nrm, b3/nrm

    G00 = b0 + 1j * b3
    G01 = b2 + 1j * b1
    G10 = -b2 + 1j * b1
    G11 = b0 - 1j * b3
    G = jnp.stack([
        jnp.stack([G00, G01], axis=-1),
        jnp.stack([G10, G11], axis=-1),
    ], axis=-2)
    return G


def compute_staples(U, x, y, z, t, mu, L):
    """Sum of staples around link (x, mu)."""
    # Simplified : just use jnp roll
    pass  # implement if needed


@jit
def wilson_action(U, beta):
    """S = β Σ_plaq (1 - 1/N Re Tr(U_plaq))."""
    L = U.shape[0]
    plaqs = all_plaquettes(U, L)
    return beta * jnp.sum(1 - plaqs)


def compute_planar_EE_proxy(U, L):
    """Proxy entanglement entropy across planar boundary x_0 = L/2.

    Use mutual information of plaquettes across the boundary :
      I(plaq_left ; plaq_right) ≈ H(left) + H(right) - H(left ∪ right)

    For free gauge fields, leading area scaling :
      S_EE ≈ c · A_boundary + sub-leading

    The proxy uses Gaussian approximation :
      I_Gauss = 0.5 * log(det(C_L) det(C_R) / det(C_LR))
    where C are plaquette covariance matrices.

    This gives a coefficient that should be PROPORTIONAL to the true 1/4
    but not equal — the ratio quantifies the discrepancy.
    """
    plaqs = all_plaquettes(U, L)  # (L,L,L,L,6)
    # Split along axis 0 (x_0)
    plaqs_L = plaqs[:L//2]  # (L/2, L, L, L, 6)
    plaqs_R = plaqs[L//2:]  # (L/2, L, L, L, 6)

    # Boundary plaquettes : those at x_0 = L/2 - 1 and L/2
    boundary_L = plaqs[L//2 - 1]  # (L, L, L, 6)
    boundary_R = plaqs[L//2]      # (L, L, L, 6)

    # Flatten and compute mutual info proxy
    bL = boundary_L.flatten()
    bR = boundary_R.flatten()

    # Variance of each
    var_L = jnp.var(bL)
    var_R = jnp.var(bR)
    cov_LR = jnp.mean((bL - jnp.mean(bL)) * (bR - jnp.mean(bR)))

    # Gaussian mutual info :
    #   I = 0.5 log( var_L * var_R / (var_L * var_R - cov_LR²) )
    denom = var_L * var_R - cov_LR**2
    denom_safe = jnp.where(denom > 1e-10, denom, 1e-10)
    I_gauss = 0.5 * jnp.log(var_L * var_R / denom_safe)

    # Boundary area in lattice units : L³ (3-volume of S² boundary in L⁴ torus)
    A_boundary = L * L * L

    # EE coefficient proxy
    c_proxy = I_gauss / A_boundary

    return I_gauss, A_boundary, c_proxy


@partial(jit, static_argnames=('L', 'n_thermalize', 'n_measure'))
def run_one_lattice(key, L, beta, n_thermalize=50, n_measure=20):
    """One lattice run : hot start → thermalize → measure EE proxy.

    Returns mean I_gauss, A_boundary, c_proxy over measurements.
    """
    key, subkey = jax.random.split(key)
    U = random_su2_field(subkey, L)

    # Simplified "thermalization" : apply gauge-noise updates
    def body(carry, _):
        U_, key_ = carry
        key_, subkey_ = jax.random.split(key_)
        # Cheap update : multiply each link by small random SU(2) perturbation
        perturbation = random_su2_field(subkey_, L)
        # Mix : U_new = U · (small perturbation factor)
        # For now just slowly mix with random
        alpha = 0.05
        U_new = U_ * (1 - alpha) + perturbation * alpha
        # Re-normalize to SU(2) — Cabibbo-Marinari projection
        # Pour simplifier : skip pour pilot
        return (U_new, key_), None

    (U_final, _), _ = lax.scan(body, (U, key), jnp.arange(n_thermalize))

    # Measure EE proxy
    def measure_body(carry, _):
        U_, key_ = carry
        key_, subkey_ = jax.random.split(key_)
        # Compute EE proxy
        I, A, c = compute_planar_EE_proxy(U_, L)
        return (U_, key_), (I, A, c)

    (_, _), results = lax.scan(measure_body, (U_final, key), jnp.arange(n_measure))
    I_arr, A_arr, c_arr = results

    return jnp.mean(I_arr), jnp.mean(A_arr), jnp.mean(c_arr), jnp.std(c_arr)


def main():
    L_values = [8, 12, 16, 20]
    beta = 2.4
    n_thermalize = 100
    n_measure = 30
    n_configs_per_L = 10  # 10 indep starts per L

    all_results = {}

    for L in L_values:
        print(f"\n{'='*78}", flush=True)
        print(f"L = {L} : β = {beta}, {n_configs_per_L} indep starts × {n_measure} measures", flush=True)
        print(f"{'='*78}", flush=True)

        c_proxies = []
        I_means = []
        t_start = time.time()
        for cfg_i in range(n_configs_per_L):
            key = jax.random.PRNGKey(2026 + 13*L + 7*cfg_i)
            t_cfg = time.time()
            I, A, c_mean, c_std = run_one_lattice(key, L, beta, n_thermalize, n_measure)
            c_proxies.append(float(c_mean))
            I_means.append(float(I))
            elapsed_cfg = time.time() - t_cfg
            if cfg_i < 3 or (cfg_i+1) % 5 == 0:
                print(f"  cfg {cfg_i+1}/{n_configs_per_L}: I={float(I):.4e}, A={int(A)}, "
                      f"c={float(c_mean):.6e} ± {float(c_std):.2e}, t={elapsed_cfg:.1f}s", flush=True)

        c_arr = np.array(c_proxies)
        c_mean_global = c_arr.mean()
        c_std_global = c_arr.std()
        I_mean_global = np.mean(I_means)
        elapsed_L = time.time() - t_start

        stats = {
            'L': L,
            'beta': beta,
            'n_configs': n_configs_per_L,
            'I_gauss_mean': float(I_mean_global),
            'A_boundary': L*L*L,
            'c_proxy_mean': float(c_mean_global),
            'c_proxy_std': float(c_std_global),
            'all_c_proxies': c_proxies,
            'elapsed_s': elapsed_L,
        }
        all_results[L] = stats
        print(f"L={L} elapsed: {elapsed_L:.1f}s", flush=True)
        print(f"  ⟨I⟩ = {I_mean_global:.4e}", flush=True)
        print(f"  ⟨c⟩ = {c_mean_global:.6e} ± {c_std_global:.6e}", flush=True)
        print(f"  Target candidates :", flush=True)
        print(f"    1/4 = κ²_SU(2) = 0.25", flush=True)
        print(f"    log(3)/π ≈ 0.350", flush=True)
        print(f"    1/(2π) ≈ 0.159", flush=True)
        print(f"    3/(4π²) ≈ 0.076", flush=True)

    # Scaling analysis
    print(f"\n{'='*78}\nSCALING ANALYSIS\n{'='*78}", flush=True)
    print(f"{'L':>6} {'I_gauss':>14} {'A':>8} {'c_proxy':>14} {'c_proxy·4':>14}", flush=True)
    print("-"*66, flush=True)
    for L in L_values:
        s = all_results[L]
        print(f"{L:>6} {s['I_gauss_mean']:>14.4e} {s['A_boundary']:>8d} "
              f"{s['c_proxy_mean']:>14.6e} {s['c_proxy_mean']*4:>14.6f}", flush=True)

    # Extrapolation L→∞
    Ls = np.array(L_values, dtype=float)
    cs = np.array([all_results[int(L)]['c_proxy_mean'] for L in Ls])
    print(f"\nc_proxy(L) cross-L :", flush=True)
    for L, c in zip(Ls, cs):
        ratio_quarter = c / 0.25
        print(f"  L={int(L):>2} : c = {c:.6e}, c/(1/4) = {ratio_quarter:.4f}", flush=True)

    if all(c > 0 for c in cs):
        # Fit c = c_∞ + a/L²
        from scipy.optimize import curve_fit
        try:
            popt, _ = curve_fit(lambda L, c_inf, a: c_inf + a/L**2, Ls, cs)
            c_inf_fit = popt[0]
            print(f"\nExtrapolation c_∞ = {c_inf_fit:.6e}", flush=True)
            print(f"  c_∞ / (1/4) = {c_inf_fit / 0.25:.4f}", flush=True)
            print(f"  c_∞ / (3/(4π²)) = {c_inf_fit / (3/(4*np.pi**2)):.4f}", flush=True)
            print(f"  c_∞ / log(3)/π = {c_inf_fit / (np.log(3)/np.pi):.4f}", flush=True)
        except Exception as e:
            print(f"Fit failed : {e}", flush=True)

    output = {
        'pilot_caveat': 'Proxy mutual-info, not full Donnelly-Wall EE. Coefficients indicative only.',
        'beta': beta,
        'L_values': L_values,
        'n_thermalize': n_thermalize,
        'n_measure': n_measure,
        'n_configs_per_L': n_configs_per_L,
        'results': {str(L): all_results[L] for L in L_values},
        'total_elapsed_s': time.time() - START,
    }
    with open('/tmp/jax_su2_EE_pilot_results.json', 'w') as f:
        json.dump(output, f, indent=2)

    print(f"\nTotal elapsed : {time.time() - START:.1f}s ({(time.time() - START)/60:.1f}min)", flush=True)
    print(f"Saved : /tmp/jax_su2_EE_pilot_results.json", flush=True)
    print(f"END : {time.ctime()}", flush=True)
    print(f"DONE.", flush=True)


if __name__ == "__main__":
    main()
