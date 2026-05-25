#!/usr/bin/env python3
"""JAX SU(2) Modular Hamiltonian observable (Bisognano-Wichmann lattice).

Goal : extract leading area-law coefficient κ for SU(2) 4D EE directly,
WITHOUT the BP α-integration cancellation.

Observable :
  K_A^(w) = 2π · Σ_{k=0}^{w-1} (k+0.5) · Σ_{x_⊥} T^00(x_0 = L/2-1-k, x_⊥)

where T^00 is the lattice clover energy-momentum tensor at site x.

Method :
1. Sample U ~ exp(-β S_W) (standard Wilson)
2. Compute T^00 via clover field strength
3. Sum strip-weighted near boundary x_0 = L/2 - 1/2
4. Vacuum-subtract using same operator far from boundary (x_0 = L/4)
5. Fit S_2(L) = κ·L³·ζ_w(3) + C·log(L) + const → extract κ

Reference : OP_MODULAR_HAMILTONIAN_SPEC_2026-05-25.md

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
print(f"JAX SU(2) Modular Hamiltonian — Bisognano-Wichmann lattice", flush=True)
print(f"Goal : extract leading area-law κ for SU(2) 4D EE", flush=True)
print("=" * 78, flush=True)
jax.config.update("jax_enable_x64", True)
print(f"JAX : {jax.__version__}, backend : {jax.default_backend()}", flush=True)


# ============================================================================
# SU(2) primitives + Wilson action (reuse FAST V3)
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
# Clover field strength F_{mu, nu}(x)
# ============================================================================

@partial(jit, static_argnames=('mu', 'nu'))
def clover_F_munu(U, mu, nu):
    """Compute lattice clover field strength F_{mu, nu}(x) for all x.

    U shape (L, L, L, L, 4, 2, 2)  (last 3 axes : μ ∈ {0,1,2,3}, SU(2))
    Returns (L, L, L, L, 2, 2) complex traceless-anti-Hermitian.

    The 4 oriented plaquettes meeting at site x in the (mu, nu) plane :
      Q1 (FF) : x → x+μ → x+μ+ν → x+ν → x
      Q2 (FB) : x → x+ν → x+ν-μ → x-μ → x  (backward in μ)
      Q3 (BB) : x → x-μ → x-μ-ν → x-ν → x
      Q4 (BF) : x → x-ν → x-ν+μ → x+μ → x  (backward in ν, forward in μ)
    """
    U_mu = U[..., mu, :, :]   # (L,L,L,L,2,2)
    U_nu = U[..., nu, :, :]

    # Forward-forward plaquette Q1:
    # U_μ(x) U_ν(x+μ) U_μ†(x+ν) U_ν†(x)
    U_nu_pmu = jnp.roll(U_nu, -1, axis=mu)  # U_ν(x+μ)
    U_mu_pnu = jnp.roll(U_mu, -1, axis=nu)  # U_μ(x+ν)
    Q1 = jnp.einsum('...ij,...jk,...lk,...ml->...im',
                     U_mu, U_nu_pmu,
                     jnp.conjugate(U_mu_pnu),
                     jnp.conjugate(U_nu))

    # Forward in ν, backward in μ: Q2 = U_ν(x) U_μ†(x-μ+ν) U_ν†(x-μ) U_μ(x-μ)
    U_mu_mmu_pnu = jnp.roll(jnp.roll(U_mu, 1, axis=mu), -1, axis=nu)  # U_μ(x-μ+ν)
    U_nu_mmu = jnp.roll(U_nu, 1, axis=mu)                              # U_ν(x-μ)
    U_mu_mmu = jnp.roll(U_mu, 1, axis=mu)                              # U_μ(x-μ)
    Q2 = jnp.einsum('...ij,...kj,...lk,...lm->...im',
                     U_nu,
                     jnp.conjugate(U_mu_mmu_pnu),
                     jnp.conjugate(U_nu_mmu),
                     U_mu_mmu)

    # Backward-backward Q3: U_μ†(x-μ) U_ν†(x-μ-ν) U_μ(x-μ-ν) U_ν(x-ν)
    U_mu_mmu_mnu = jnp.roll(jnp.roll(U_mu, 1, axis=mu), 1, axis=nu)
    U_nu_mmu_mnu = jnp.roll(jnp.roll(U_nu, 1, axis=mu), 1, axis=nu)
    U_nu_mnu = jnp.roll(U_nu, 1, axis=nu)
    Q3 = jnp.einsum('...ji,...kj,...kl,...lm->...im',
                     jnp.conjugate(U_mu_mmu),
                     jnp.conjugate(U_nu_mmu_mnu),
                     U_mu_mmu_mnu,
                     U_nu_mnu)

    # Backward in ν, forward in μ: Q4 = U_ν†(x-ν) U_μ(x-ν) U_ν(x-ν+μ) U_μ†(x)
    U_mu_mnu = jnp.roll(U_mu, 1, axis=nu)
    U_nu_mnu_pmu = jnp.roll(jnp.roll(U_nu, 1, axis=nu), -1, axis=mu)
    Q4 = jnp.einsum('...ji,...jk,...kl,...ml->...im',
                     jnp.conjugate(U_nu_mnu),
                     U_mu_mnu,
                     U_nu_mnu_pmu,
                     jnp.conjugate(U_mu))

    Q = Q1 + Q2 + Q3 + Q4

    # Clover F = (Q - Q†) / (8i)
    Q_dag = jnp.conjugate(jnp.swapaxes(Q, -1, -2))
    F = (Q - Q_dag) / (8j)

    # Traceless projection: F - (1/2) Tr(F) · I_{2x2}
    tr_F = jnp.trace(F, axis1=-2, axis2=-1)
    I2 = jnp.eye(2, dtype=F.dtype)
    # Broadcast tr_F over last 2 dims
    F = F - 0.5 * tr_F[..., None, None] * I2

    return F


# ============================================================================
# Energy-momentum tensor T^00
# ============================================================================

@jit
def energy_momentum_T00(U, beta):
    """Returns (L, L, L, L) real array of T^00(x) per site.

    T^00 = (1/g²) · Σ_i [F_{0i}^a]² + (1/2)·(1/g²) · Σ_{i<j} [F_{ij}^a]²

    For SU(2): β = 4/g², so 1/g² = β/4
    Tr(F·F) for traceless 2x2 anti-Hermitian gives -Σ_a (F^a)^2 / 2
    So we need -2·Tr(F·F) to get Σ_a (F^a)^2.

    Convention : T^00 should be ≥ 0 (positive energy density).

    F = (Q-Q†)/(8i) is HERMITIAN (since (Q-Q†)/i is Hermitian).
    For Hermitian F = F^a T^a with T^a = σ^a/2 :
      Tr(F·F) = F^a F^b · Tr(T^a T^b) = (1/2) F^a F^a > 0
    So T^00 = +2·inv_g2·Tr(F·F) for electric, +inv_g2·Tr(F·F) for magnetic.
    """
    inv_g2 = beta / 4.0
    T00 = jnp.zeros(U.shape[:4])

    # Electric : i ∈ {1, 2, 3}, weight +2·inv_g2
    for i in (1, 2, 3):
        F_0i = clover_F_munu(U, 0, i)
        FF = jnp.einsum('...ij,...jk->...ik', F_0i, F_0i)
        tr_FF = jnp.real(jnp.trace(FF, axis1=-2, axis2=-1))
        T00 = T00 + 2.0 * inv_g2 * tr_FF

    # Magnetic : (i, j) ∈ {(1,2), (1,3), (2,3)}, weight +inv_g2 each (= 2·1/2)
    for i, j in [(1, 2), (1, 3), (2, 3)]:
        F_ij = clover_F_munu(U, i, j)
        FF = jnp.einsum('...ij,...jk->...ik', F_ij, F_ij)
        tr_FF = jnp.real(jnp.trace(FF, axis1=-2, axis2=-1))
        T00 = T00 + inv_g2 * tr_FF

    return T00


# ============================================================================
# Modular Hamiltonian observable
# ============================================================================

@partial(jit, static_argnames=('w', 'x0_center'))
def modular_hamiltonian_K(U, beta, w, x0_center):
    """K_A^(w) = 2π Σ_{k=0}^{w-1} (k+0.5) · Σ_{x_⊥} T^00(x_0_center - 1 - k, x_⊥)

    Boundary at x_0 = x0_center - 0.5 (cut between sites x0_center-1 and x0_center).
    Strip [x0_center - w, x0_center) of width w.

    x_⊥ = (k + 0.5) = distance to boundary surface in lattice units.

    Returns scalar real.
    """
    T00 = energy_momentum_T00(U, beta)  # (L, L, L, L)
    L = T00.shape[0]
    K = 0.0
    for k in range(w):
        x0 = x0_center - 1 - k
        x0_idx = x0 % L  # PBC
        # Sum T^00 over transverse volume (axes 1, 2, 3)
        T00_slice = T00[x0_idx]  # (L, L, L)
        T00_sum = jnp.sum(T00_slice)
        weight = (k + 0.5)
        K = K + weight * T00_sum
    return 2.0 * jnp.pi * K


@partial(jit, static_argnames=('w',))
def modular_hamiltonian_K_at_boundary(U, beta, w):
    """K_A at the entangling boundary x_0 = L/2 - 1/2 (cut between L/2-1 and L/2)."""
    L = U.shape[0]
    return modular_hamiltonian_K(U, beta, w, L // 2)


@partial(jit, static_argnames=('w',))
def modular_hamiltonian_K_vacuum(U, beta, w):
    """Vacuum subtraction at x_0 = L/4 + L/2 separately (average of 2 bulk locations).

    We compute the SAME observable centered at a generic bulk location far from any
    boundary. For a half-region cut at L/2, bulk locations are x_0 = L/4 and 3L/4.
    """
    L = U.shape[0]
    K1 = modular_hamiltonian_K(U, beta, w, L // 4)
    K2 = modular_hamiltonian_K(U, beta, w, (3 * L) // 4)
    return 0.5 * (K1 + K2)


# ============================================================================
# Wilson action + standard Metropolis (reuse FAST V3 logic)
# ============================================================================

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


def compute_staple_sum(U, mu, L):
    """Standard staple sum K(x, μ) for SU(2) Wilson."""
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


@partial(jit, static_argnames=('L',))
def metropolis_sweep_standard(U, beta, key, L, eps=0.3):
    """Standard per-link Metropolis on Wilson SU(2)."""
    for mu in range(4):
        K_mu = compute_staple_sum(U, mu, L)
        key, k_prop, k_acc = random.split(key, 3)
        X = random_su2_near_identity(k_prop, U[..., mu, :, :].shape[:-2], eps=eps)
        U_proposed_mu = jnp.einsum('...ij,...jk->...ik', X, U[..., mu, :, :])
        K_dag = jnp.conjugate(jnp.swapaxes(K_mu, -1, -2))
        new_term = jnp.real(jnp.trace(jnp.einsum('...ij,...jk->...ik', U_proposed_mu, K_dag),
                                        axis1=-2, axis2=-1))
        old_term = jnp.real(jnp.trace(jnp.einsum('...ij,...jk->...ik', U[..., mu, :, :], K_dag),
                                        axis1=-2, axis2=-1))
        dS = -beta * 0.5 * (new_term - old_term)
        rand_u = random.uniform(k_acc, dS.shape)
        accept = rand_u < jnp.exp(jnp.minimum(0.0, -dS))
        U_mu_new = jnp.where(accept[..., None, None], U_proposed_mu, U[..., mu, :, :])
        U = U.at[..., mu, :, :].set(U_mu_new)
    return U


def thermalize_standard(key, beta, L, n_sweeps, eps=0.3):
    k, sk = random.split(key)
    U = random_su2_haar(sk, (L, L, L, L, 4))
    for i in range(n_sweeps):
        k, sk = random.split(k)
        U = metropolis_sweep_standard(U, beta, sk, L, eps)
    return U, k


# ============================================================================
# MC measurement
# ============================================================================

def measure_modular_observable(L, beta, w, n_thermalize, n_decorr, n_samples, key, eps=0.3):
    """Measure ⟨K_A^(w)⟩ at boundary AND ⟨K^(w)⟩_vac."""
    print(f"\n--- L={L}, β={beta}, w={w} ---", flush=True)
    print(f"Thermalize {n_thermalize} sweeps...", flush=True)
    t0 = time.time()
    U, key = thermalize_standard(key, beta, L, n_thermalize, eps)
    print(f"Thermalized in {time.time()-t0:.1f}s ({(time.time()-t0)/n_thermalize*1000:.1f}ms/sweep)", flush=True)

    K_boundary_samples = []
    K_vacuum_samples = []
    t0 = time.time()
    for s in range(n_samples):
        for _ in range(n_decorr):
            key, sk = random.split(key)
            U = metropolis_sweep_standard(U, beta, sk, L, eps)
        K_b = float(modular_hamiltonian_K_at_boundary(U, beta, w))
        K_v = float(modular_hamiltonian_K_vacuum(U, beta, w))
        K_boundary_samples.append(K_b)
        K_vacuum_samples.append(K_v)
        if s == 0 or (s+1) % max(1, n_samples//5) == 0 or s == n_samples-1:
            print(f"  sample {s+1}/{n_samples}: K_b={K_b:.3e}, K_v={K_v:.3e}, diff={K_b-K_v:.3e}, "
                  f"t={time.time()-t0:.1f}s", flush=True)

    K_b_arr = np.array(K_boundary_samples)
    K_v_arr = np.array(K_vacuum_samples)
    K_diff = K_b_arr - K_v_arr

    return {
        'L': L, 'beta': beta, 'w': w,
        'n_samples': n_samples, 'n_decorr': n_decorr,
        'K_boundary_mean': float(K_b_arr.mean()),
        'K_boundary_sem': float(K_b_arr.std() / np.sqrt(n_samples)),
        'K_vacuum_mean': float(K_v_arr.mean()),
        'K_vacuum_sem': float(K_v_arr.std() / np.sqrt(n_samples)),
        'K_diff_mean': float(K_diff.mean()),
        'K_diff_sem': float(K_diff.std() / np.sqrt(n_samples)),
        'K_boundary_samples': K_boundary_samples,
        'K_vacuum_samples': K_vacuum_samples,
    }


# ============================================================================
# κ extraction from L-scaling fit
# ============================================================================

def zeta_w(w):
    """ζ_w(3) = Σ_{k=0}^{w-1} 1/(k+0.5)^3"""
    return sum(1.0 / (k + 0.5)**3 for k in range(w))


def fit_kappa(L_values, K_diff_means, K_diff_sems, w_values):
    """Linear fit K_diff = κ·L³·ζ_w(3) + C·log(L) + const.

    Returns (κ, κ_err, C, const).
    """
    L_arr = np.array(L_values, dtype=float)
    Kd_arr = np.array(K_diff_means)
    err_arr = np.array(K_diff_sems)
    zeta_arr = np.array([zeta_w(w) for w in w_values])

    # Design matrix
    A = np.stack([L_arr**3 * zeta_arr, np.log(L_arr), np.ones_like(L_arr)], axis=1)

    # Weighted least squares
    W = np.diag(1.0 / np.maximum(err_arr**2, 1e-20))
    AT_W = A.T @ W
    M = AT_W @ A
    coeffs = np.linalg.solve(M, AT_W @ Kd_arr)
    cov = np.linalg.inv(M)

    kappa, C, const = coeffs
    kappa_err = np.sqrt(cov[0, 0])
    C_err = np.sqrt(cov[1, 1])

    return {
        'kappa': float(kappa),
        'kappa_err': float(kappa_err),
        'C_sub': float(C),
        'C_sub_err': float(C_err),
        'const': float(const),
        'residuals': (Kd_arr - A @ coeffs).tolist(),
    }


# ============================================================================
# Main
# ============================================================================

def main():
    BETA = 2.4

    configs = {
        8:  {'w': 2, 'n_thermalize': 100, 'n_decorr': 5,  'n_samples': 100},
        12: {'w': 3, 'n_thermalize': 200, 'n_decorr': 8,  'n_samples': 50},
        16: {'w': 4, 'n_thermalize': 400, 'n_decorr': 12, 'n_samples': 30},
    }

    all_results = {}
    for L in [8, 12, 16]:
        cfg = configs[L]
        print(f"\n{'='*78}\nLATTICE L = {L}, w = {cfg['w']}\n{'='*78}", flush=True)
        key = random.PRNGKey(2040 + 53 * L)
        try:
            r = measure_modular_observable(L, BETA, cfg['w'],
                                            cfg['n_thermalize'], cfg['n_decorr'], cfg['n_samples'],
                                            key)
            all_results[L] = r
            print(f"\nL={L} : K_b={r['K_boundary_mean']:.3e}±{r['K_boundary_sem']:.0e}", flush=True)
            print(f"        K_v={r['K_vacuum_mean']:.3e}±{r['K_vacuum_sem']:.0e}", flush=True)
            print(f"        K_diff={r['K_diff_mean']:.3e}±{r['K_diff_sem']:.0e}", flush=True)
        except Exception as e:
            print(f"L={L} FAILED : {e}", flush=True)
            import traceback
            traceback.print_exc()
        # Checkpoint
        with open('/tmp/jax_su2_EE_MODULAR_results.json', 'w') as f:
            json.dump({
                'method': 'Modular Hamiltonian Bisognano-Wichmann SU(2) lattice',
                'beta': BETA,
                'configs': {str(L): configs[L] for L in configs},
                'results': {str(L): all_results[L] for L in all_results},
                'partial': True,
                'total_elapsed_s': time.time() - START,
            }, f, indent=2)

    # Fit κ from L-scaling
    print(f"\n{'='*78}\nκ EXTRACTION FIT — K_diff = κ·L³·ζ_w(3) + C·log(L) + const\n{'='*78}", flush=True)
    if len(all_results) >= 3:
        L_vals = sorted(all_results.keys())
        K_means = [all_results[L]['K_diff_mean'] for L in L_vals]
        K_sems = [all_results[L]['K_diff_sem'] for L in L_vals]
        w_vals = [configs[L]['w'] for L in L_vals]

        fit_result = fit_kappa(L_vals, K_means, K_sems, w_vals)
        print(f"\n  L values : {L_vals}")
        print(f"  K_diff   : {[f'{k:.3e}' for k in K_means]}")
        print(f"  K_diff err: {[f'{k:.0e}' for k in K_sems]}")
        print(f"  ζ_w(3)   : {[f'{zeta_w(w):.4f}' for w in w_vals]}")
        print(f"\n  κ        = {fit_result['kappa']:.6e} ± {fit_result['kappa_err']:.2e}")
        print(f"  C_sub    = {fit_result['C_sub']:.6e} ± {fit_result['C_sub_err']:.2e}")
        print(f"  const    = {fit_result['const']:.6e}")
        print(f"  residuals: {[f'{r:.2e}' for r in fit_result['residuals']]}")

        print(f"\n  vs predictions :")
        candidates = {
            'κ²=1/4 (κ=1/2) Bekenstein-Hawking': 0.5,
            '1/4 = 0.25': 0.25,
            'log(3)/(2π√2) = 0.124': np.log(3)/(2*np.pi*np.sqrt(2)),
        }
        for name, pred in candidates.items():
            ratio = fit_result['kappa'] / pred if pred != 0 else 0
            z = (fit_result['kappa'] - pred) / max(fit_result['kappa_err'], 1e-10)
            print(f"    {name:<45} : ratio = {ratio:.3f}, Z = {z:+.2f}σ")
    else:
        print("  Need 3+ L values for fit", flush=True)

    output = {
        'method': 'Modular Hamiltonian Bisognano-Wichmann SU(2) lattice',
        'beta': BETA,
        'configs': {str(L): configs[L] for L in configs},
        'results': {str(L): all_results[L] for L in all_results},
        'fit': fit_result if len(all_results) >= 3 else None,
        'total_elapsed_s': time.time() - START,
    }
    with open('/tmp/jax_su2_EE_MODULAR_results.json', 'w') as f:
        json.dump(output, f, indent=2)

    print(f"\nTotal elapsed : {time.time() - START:.1f}s ({(time.time() - START)/60:.1f}min)", flush=True)
    print(f"END : {time.ctime()}", flush=True)
    print(f"DONE.", flush=True)


if __name__ == "__main__":
    main()
