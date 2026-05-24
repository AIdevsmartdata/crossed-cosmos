#!/usr/bin/env python3
"""KR-FP-3 SU(2) lattice — JAX GPU version with matrix-free LOBPCG.

Tests :
  - inf_{A∈Λ} ||A||²_{L⁴} ≤ K  (Lemma KR-FP-3 from FP uniform bound program)
  - inf_{A∈Λ} λ_min(M[A]) > 0  (Zwanziger horizon condition, equivalent under bounds)

GPU strategy :
  - Hot start SU(2) random Haar field
  - Landau gauge fix via JIT'd overrelaxation (lax.scan)
  - Matrix-free Faddeev-Popov : M·ψ stencil via jnp.roll + jnp.cross
  - LOBPCG with shift c·I - M for smallest eigenvalues
  - vmap over many configs for GPU batching

Hardware : RTX 5060 Ti 16GB VRAM, JAX 0.10.1 CUDA.

Theoretical statement (Singer 1978 CMP 60 + Dell'Antonio-Zwanziger 1991 CMP 138) :
  Λ = fundamental modular domain ⊂ Ω (Gribov region)
  Λ = {A : F[A] = ||A||² minimal on gauge orbit}
  → λ_min(M[A]) > 0 on Λ (by construction of Ω)
  Question : uniform spectral gap ?
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
print("KR-FP-3 SU(2) JAX GPU — matrix-free LOBPCG", flush=True)
print("=" * 78, flush=True)

jax.config.update("jax_enable_x64", True)
print(f"JAX version : {jax.__version__}", flush=True)
print(f"Devices     : {jax.devices()}", flush=True)
print(f"Backend     : {jax.default_backend()}", flush=True)
print(f"x64 enabled : {jax.config.read('jax_enable_x64')}", flush=True)


def random_su2_field(key, L):
    """Hot-start: uniform Haar SU(2) at every link via 4-quaternion sampling.

    SU(2) ≅ S³ : x ∈ R⁴, |x|=1 → U = x₀ I + i x_a σ^a
    """
    key1, _ = jax.random.split(key)
    raw = jax.random.normal(key1, (L, L, L, L, 4, 4))
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


def project_su2_omega(K, omega):
    """SU(2) projection of K with overrelaxation power G^omega.

    G_opt = K^† / |K| is the SU(2) closest to K^† (maximizes Re tr(g K^†)).
    G^omega = exp(omega · log(G_opt)) for ω > 1 accelerates convergence.

    For SU(2): G_opt = cos(θ) I + sin(θ) n·σ → G_opt^ω = cos(ωθ) I + sin(ωθ) n·σ
    """
    K00, K01 = K[..., 0, 0], K[..., 0, 1]
    K10, K11 = K[..., 1, 0], K[..., 1, 1]
    a0 = 0.5 * jnp.real(K00 + K11)
    a1 = -0.5 * jnp.imag(K01 + K10)
    a2 = -0.5 * jnp.real(K01 - K10)
    a3 = -0.5 * jnp.imag(K00 - K11)
    r = jnp.sqrt(a0 ** 2 + a1 ** 2 + a2 ** 2 + a3 ** 2)
    r = jnp.where(r < 1e-15, 1.0, r)
    a0n, a1n, a2n, a3n = a0 / r, a1 / r, a2 / r, a3 / r
    a_perp = jnp.sqrt(jnp.maximum(a1n ** 2 + a2n ** 2 + a3n ** 2, 1e-30))
    theta = jnp.arctan2(a_perp, a0n)
    omega_theta = omega * theta
    factor = jnp.sin(omega_theta) / a_perp
    b0 = jnp.cos(omega_theta)
    b1 = a1n * factor
    b2 = a2n * factor
    b3 = a3n * factor
    G00 = b0 + 1j * b3
    G01 = b2 + 1j * b1
    G10 = -b2 + 1j * b1
    G11 = b0 - 1j * b3
    G = jnp.stack([
        jnp.stack([G00, G01], axis=-1),
        jnp.stack([G10, G11], axis=-1),
    ], axis=-2)
    return G


def apply_gauge_at_mask(U, G, mask4d):
    """Apply gauge transform U_μ(x) → G(x) U_μ(x) G(x+μ̂)^† only where mask is True."""
    mask = mask4d[..., None, None]
    G_eff = jnp.where(mask, G, jnp.broadcast_to(jnp.eye(2, dtype=complex),
                                                   G.shape))
    new_U_list = []
    for mu in range(4):
        G_xpmu = jnp.roll(G_eff, -1, axis=mu)
        G_xpmu_dag = dag(G_xpmu)
        new_mu = jnp.einsum('...ij,...jk,...kl->...il',
                            G_eff, U[..., mu, :, :], G_xpmu_dag, optimize=True)
        new_U_list.append(new_mu)
    return jnp.stack(new_U_list, axis=-3)


def overrelaxation_step_checkerboard(U, omega, mask_even, mask_odd):
    """One sweep of checkerboard overrelaxation: even sites, then odd."""
    for mask in [mask_even, mask_odd]:
        K = jnp.zeros_like(U[..., 0, :, :])
        for mu in range(4):
            K = K + U[..., mu, :, :]
            U_back = jnp.roll(U[..., mu, :, :], 1, axis=mu)
            K = K + dag(U_back)
        G = project_su2_omega(K, omega)
        U = apply_gauge_at_mask(U, G, mask)
    return U


def make_parity_masks(L):
    """Return (mask_even, mask_odd) boolean arrays of shape (L,L,L,L)."""
    xi, yi, zi, ti = jnp.indices((L, L, L, L))
    parity = (xi + yi + zi + ti) % 2
    return (parity == 0), (parity == 1)


def landau_gauge_fix(U, n_iter, omega=1.7):
    """Run n_iter sweeps of checkerboard overrelaxation with ω."""
    L = U.shape[0]
    mask_even, mask_odd = make_parity_masks(L)
    def body(carry, _):
        U_ = carry
        return overrelaxation_step_checkerboard(U_, omega, mask_even, mask_odd), None
    U_final, _ = lax.scan(body, U, jnp.arange(n_iter))
    return U_final


def compute_A_field(U):
    """A_μ^a(x) = -(1/2) Im tr(σ^a U_μ(x)) en composantes SU(2)."""
    U00 = U[..., 0, 0]
    U01 = U[..., 0, 1]
    U10 = U[..., 1, 0]
    U11 = U[..., 1, 1]
    A1 = -0.5 * jnp.imag(U01 + U10)
    A2 = -0.5 * jnp.real(U01 - U10)
    A3 = -0.5 * jnp.imag(U00 - U11)
    return jnp.stack([A1, A2, A3], axis=-1)


def gauge_div_error(U):
    """||∂A|| as gauge fixing quality metric."""
    A = compute_A_field(U)
    divA = jnp.zeros_like(A[..., 0, :])
    for mu in range(4):
        divA = divA + A[..., mu, :] - jnp.roll(A[..., mu, :], 1, axis=mu)
    return jnp.sqrt(jnp.mean(divA ** 2))


def apply_FP(psi, A):
    """Matrix-free FP operator M[A]·ψ.

    M ψ^a(x) = -Σ_μ {ψ^a(x+μ̂) + ψ^a(x-μ̂) - 2 ψ^a(x)
                     + ε^abc A_μ^b(x)   [ψ^c(x+μ̂) - ψ^c(x)]
                     - ε^abc A_μ^b(x-μ̂)[ψ^c(x-μ̂) - ψ^c(x)] }
    ψ shape : (L,L,L,L,3)
    A shape : (L,L,L,L,4,3)
    """
    result = jnp.zeros_like(psi)
    for mu in range(4):
        psi_p = jnp.roll(psi, -1, axis=mu)
        psi_m = jnp.roll(psi, 1, axis=mu)
        result = result - (psi_p + psi_m - 2.0 * psi)
        A_mu = A[..., mu, :]
        A_mu_back = jnp.roll(A_mu, 1, axis=mu)
        cross_fwd = jnp.cross(A_mu, psi_p - psi, axis=-1)
        cross_bwd = jnp.cross(A_mu_back, psi_m - psi, axis=-1)
        result = result - cross_fwd + cross_bwd
    return result


def project_zero_modes(psi):
    """Remove the 3 zero modes (constant per color) from periodic-BC FP operator."""
    n_sites = psi.shape[0] * psi.shape[1] * psi.shape[2] * psi.shape[3]
    psi_2d = psi.reshape(n_sites, 3)
    means = psi_2d.mean(axis=0)
    psi_2d = psi_2d - means
    return psi_2d.reshape(psi.shape)


def lobpcg_smallest(apply_M_func, shape, n_eigs, key, n_iter=80, shift=20.0):
    """LOBPCG matrix-free for smallest eigenvalues via shift c·I - M.

    Largest of (c·I - M) = c - (smallest of M)
    Iterations : Rayleigh-Ritz on span {X, P, W}.
    Fixed n_iter for JIT compatibility (no early termination).
    """
    n_total = int(np.prod(shape))

    def matvec_shifted(psi):
        return shift * psi - apply_M_func(psi)

    def matvec_block(X_block):
        return vmap(matvec_shifted, in_axes=-1, out_axes=-1)(X_block)

    X = jax.random.normal(key, shape + (n_eigs,), dtype=jnp.float64)
    X = vmap(project_zero_modes, in_axes=-1, out_axes=-1)(X)
    X_flat = X.reshape(n_total, n_eigs)
    Q, _ = jnp.linalg.qr(X_flat)
    X = Q.reshape(shape + (n_eigs,))
    P = jnp.zeros_like(X)

    def lobpcg_iter(carry, _):
        X, P = carry
        AX = matvec_block(X)
        residual = AX - jnp.einsum('...i,...i->...', X, AX)[..., None] * X
        residual = vmap(project_zero_modes, in_axes=-1, out_axes=-1)(residual)

        basis = jnp.concatenate([
            X.reshape(n_total, n_eigs),
            residual.reshape(n_total, n_eigs),
            P.reshape(n_total, n_eigs),
        ], axis=-1)
        Q, _ = jnp.linalg.qr(basis)
        nz = Q.shape[1]
        Q_block = Q.reshape(shape + (nz,))
        AQ = matvec_block(Q_block)
        H = jnp.einsum('...i,...j->ij', Q_block, AQ)
        H = 0.5 * (H + H.T)
        sub_vals, sub_vecs = jnp.linalg.eigh(H)
        idx = jnp.argsort(-sub_vals)
        sub_vals_top = sub_vals[idx][:n_eigs]
        sub_vecs_top = sub_vecs[:, idx][:, :n_eigs]

        X_new = (Q @ sub_vecs_top).reshape(shape + (n_eigs,))
        P_new = X_new - X
        return (X_new, P_new), sub_vals_top

    (X_final, _), eigvals_history = lax.scan(lobpcg_iter, (X, P), jnp.arange(n_iter))
    eigvals_shifted = eigvals_history[-1]
    eigvals_M = shift - eigvals_shifted
    sort = jnp.argsort(eigvals_M)
    return eigvals_M[sort]


@partial(jit, static_argnames=('L', 'n_gauge_iter', 'n_eigs', 'n_lobpcg_iter'))
def measure_one_config(key, L, n_gauge_iter=2000, n_eigs=6, n_lobpcg_iter=60):
    """Full pipeline for one config: hot start → gauge fix → A → λ_min."""
    key_init, key_lobpcg = jax.random.split(key)
    U = random_su2_field(key_init, L)
    U_fixed = landau_gauge_fix(U, n_gauge_iter, omega=1.7)
    gauge_err = gauge_div_error(U_fixed)
    A = compute_A_field(U_fixed)

    A_sq = jnp.sum(A ** 2, axis=-1)
    A_L4 = jnp.power(jnp.mean(A_sq ** 2), 0.25)
    A_L2 = jnp.sqrt(jnp.mean(A_sq))

    def apply_M_psi(psi):
        return apply_FP(psi, A)

    eigvals = lobpcg_smallest(
        apply_M_psi,
        shape=(L, L, L, L, 3),
        n_eigs=n_eigs,
        key=key_lobpcg,
        n_iter=n_lobpcg_iter,
        shift=40.0,
    )

    return A_L4, A_L2, eigvals, gauge_err


def run_L(L, n_cfgs, base_seed=2026, n_gauge_iter=300, n_eigs=6, n_lobpcg_iter=60):
    """Run n_cfgs configs at lattice size L, sequentially (avoid OOM)."""
    print(f"\n{'='*78}", flush=True)
    print(f"L = {L} : {n_cfgs} configs, FP dim = {3*L**4}, n_eigs = {n_eigs}", flush=True)
    print(f"{'='*78}", flush=True)

    A_L4_list = []
    A_L2_list = []
    lambda_min_list = []
    eigs_all = []
    gauge_errs = []

    t_run_start = time.time()
    for i in range(n_cfgs):
        seed = base_seed + 17 * i
        key = jax.random.PRNGKey(seed)
        t_cfg = time.time()
        A_L4, A_L2, eigvals, gauge_err = measure_one_config(
            key, L, n_gauge_iter, n_eigs, n_lobpcg_iter,
        )
        A_L4 = float(A_L4)
        A_L2 = float(A_L2)
        eigvals = np.asarray(eigvals)
        gauge_err = float(gauge_err)
        elapsed_cfg = time.time() - t_cfg

        nonzero = eigvals[np.abs(eigvals) > 1e-4]
        lambda_min = float(nonzero[0]) if len(nonzero) > 0 else float(eigvals[0])

        A_L4_list.append(A_L4)
        A_L2_list.append(A_L2)
        lambda_min_list.append(lambda_min)
        eigs_all.append(eigvals.tolist())
        gauge_errs.append(gauge_err)

        if i < 5 or (i + 1) % 10 == 0 or i == n_cfgs - 1:
            print(
                f"  cfg {i+1}/{n_cfgs}: λ_min={lambda_min:.5f}, "
                f"||A||_L4={A_L4:.4f}, gauge_err={gauge_err:.2e}, "
                f"t={elapsed_cfg:.1f}s",
                flush=True
            )

    elapsed_total = time.time() - t_run_start
    print(f"L={L} total elapsed : {elapsed_total:.1f}s ({elapsed_total/60:.1f}min)", flush=True)

    stats = {
        'L': L,
        'n_cfgs': n_cfgs,
        'fp_dim': 3 * L ** 4,
        'elapsed_s': elapsed_total,
        'lambda_min_mean': float(np.mean(lambda_min_list)),
        'lambda_min_min': float(np.min(lambda_min_list)),
        'lambda_min_max': float(np.max(lambda_min_list)),
        'lambda_min_std': float(np.std(lambda_min_list)),
        'lambda_min_median': float(np.median(lambda_min_list)),
        'A_L4_mean': float(np.mean(A_L4_list)),
        'A_L4_max': float(np.max(A_L4_list)),
        'A_L4_std': float(np.std(A_L4_list)),
        'A_L2_mean': float(np.mean(A_L2_list)),
        'A_L2_max': float(np.max(A_L2_list)),
        'gauge_err_max': float(np.max(gauge_errs)),
        'gauge_err_mean': float(np.mean(gauge_errs)),
        'all_lambda_min': lambda_min_list,
        'all_A_L4': A_L4_list,
        'all_eigvals': eigs_all,
        'all_gauge_errs': gauge_errs,
    }
    print(
        f"  ||A||_L4 : mean={stats['A_L4_mean']:.4f}, max={stats['A_L4_max']:.4f}, "
        f"std={stats['A_L4_std']:.4f}",
        flush=True
    )
    print(
        f"  λ_min   : mean={stats['lambda_min_mean']:.5f}, MIN={stats['lambda_min_min']:.5f}, "
        f"max={stats['lambda_min_max']:.5f}, std={stats['lambda_min_std']:.5f}",
        flush=True
    )
    print(f"  gauge   : err max={stats['gauge_err_max']:.2e}", flush=True)
    return stats


if __name__ == "__main__":
    L_VALUES = [4, 8, 12, 16, 20]
    N_CFGS = {4: 80, 8: 60, 12: 40, 16: 25, 20: 12}
    N_GAUGE_ITER = 500
    N_EIGS = 8
    N_LOBPCG_ITER = 80

    all_results = {}
    for L in L_VALUES:
        try:
            stats = run_L(L, N_CFGS[L], 2026, N_GAUGE_ITER, N_EIGS, N_LOBPCG_ITER)
            all_results[L] = stats
        except Exception as ex:
            print(f"ERROR at L={L} : {ex}", flush=True)
            import traceback; traceback.print_exc()

    print(f"\n{'='*78}", flush=True)
    print(f"VERDICT KR-FP-3 — scaling vs L", flush=True)
    print(f"{'='*78}", flush=True)
    print(
        f"{'L':>5} {'A_L4 mean':>12} {'A_L4 max':>12} "
        f"{'λ_min mean':>14} {'λ_min MIN':>14} {'cfgs':>6}",
        flush=True
    )
    print("-" * 78, flush=True)
    for L in sorted(all_results.keys()):
        s = all_results[L]
        print(
            f"{L:>5} {s['A_L4_mean']:>12.4f} {s['A_L4_max']:>12.4f} "
            f"{s['lambda_min_mean']:>14.5f} {s['lambda_min_min']:>14.5f} {s['n_cfgs']:>6}",
            flush=True
        )

    Ls = np.array(sorted(all_results.keys()), dtype=float)
    if len(Ls) >= 2:
        lmins = np.array([all_results[int(L)]['lambda_min_min'] for L in Ls])
        lmeans = np.array([all_results[int(L)]['lambda_min_mean'] for L in Ls])
        A_maxs = np.array([all_results[int(L)]['A_L4_max'] for L in Ls])
        A_means = np.array([all_results[int(L)]['A_L4_mean'] for L in Ls])

        valid_min = lmins > 1e-6
        if valid_min.sum() >= 2:
            try:
                exp_min = np.polyfit(np.log(Ls[valid_min]), np.log(lmins[valid_min]), 1)[0]
                exp_mean = np.polyfit(np.log(Ls), np.log(lmeans), 1)[0]
                exp_A_max = np.polyfit(np.log(Ls), np.log(A_maxs), 1)[0]
                exp_A_mean = np.polyfit(np.log(Ls), np.log(A_means), 1)[0]

                print(f"\nScaling exponents (log-log fit) :", flush=True)
                print(f"  inf λ_min  ~ L^{exp_min:+.3f}", flush=True)
                print(f"  mean λ_min ~ L^{exp_mean:+.3f}", flush=True)
                print(f"  max ||A||_L4  ~ L^{exp_A_max:+.3f}", flush=True)
                print(f"  mean ||A||_L4 ~ L^{exp_A_mean:+.3f}", flush=True)

                print(f"\n--- KR-FP-3 verdict ---", flush=True)
                if exp_min < -1.5 and exp_mean < -1.5:
                    print(f"  λ_min decays ≤ 1/L² → continuum gap CLOSES → KR-FP-3 FALSIFIED", flush=True)
                elif exp_min < -0.3:
                    print(f"  λ_min decays slowly L^{exp_min:.2f} → finite-volume effect plausible", flush=True)
                    print(f"  Indecisive : need L=24,32 extrapolation", flush=True)
                else:
                    print(f"  λ_min STABILIZES (exp ≈ 0) → KR-FP-3 numerically SUPPORTED", flush=True)

                if exp_A_max > 0.5:
                    print(f"  ||A||_L4 diverges L^{exp_A_max:.2f} → uniform bound FALSIFIED", flush=True)
                elif abs(exp_A_max) < 0.2:
                    print(f"  ||A||_L4 STABILIZES → uniform bound SUPPORTED", flush=True)
                else:
                    print(f"  ||A||_L4 mild scaling L^{exp_A_max:.2f}", flush=True)
            except Exception as ex:
                print(f"  Scaling fit failed : {ex}", flush=True)
                exp_min = exp_mean = exp_A_max = exp_A_mean = None
        else:
            exp_min = exp_mean = exp_A_max = exp_A_mean = None
    else:
        exp_min = exp_mean = exp_A_max = exp_A_mean = None

    summary = {
        'L_values': sorted(all_results.keys()),
        'lambda_min_min_per_L': {str(L): all_results[L]['lambda_min_min'] for L in all_results},
        'lambda_min_mean_per_L': {str(L): all_results[L]['lambda_min_mean'] for L in all_results},
        'A_L4_max_per_L': {str(L): all_results[L]['A_L4_max'] for L in all_results},
        'A_L4_mean_per_L': {str(L): all_results[L]['A_L4_mean'] for L in all_results},
        'gauge_err_max_per_L': {str(L): all_results[L]['gauge_err_max'] for L in all_results},
        'scaling_exp_lambda_min': float(exp_min) if exp_min is not None else None,
        'scaling_exp_lambda_mean': float(exp_mean) if exp_mean is not None else None,
        'scaling_exp_A_max': float(exp_A_max) if exp_A_max is not None else None,
        'scaling_exp_A_mean': float(exp_A_mean) if exp_A_mean is not None else None,
        'total_elapsed_s': time.time() - START,
    }

    with open("/tmp/kr_fp3_jax_gpu_results.json", "w") as f:
        json.dump({
            'summary': summary,
            'by_L': {
                str(L): {k: v for k, v in s.items() if k not in ('all_eigvals',)}
                for L, s in all_results.items()
            },
        }, f, indent=2)

    print(f"\nTotal elapsed : {time.time()-START:.1f}s ({(time.time()-START)/60:.1f}min)", flush=True)
    print(f"Saved : /tmp/kr_fp3_jax_gpu_results.json", flush=True)
    print(f"END : {time.ctime()}", flush=True)
    print(f"DONE.", flush=True)
