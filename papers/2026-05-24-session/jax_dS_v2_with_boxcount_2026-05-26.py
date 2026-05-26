#!/usr/bin/env python3
"""
ADAPTATEUR v2 : d_s + d_∂ box-counting proxy + multi-L scaling.

v2 changes :
- Larger L (8, 10, 12)
- N_eigs = 400 (twice better statistics)
- Box-counting proxy via near-zero-mode spatial support
- Multi-scale scaling test
- BETTER thermalization (heat-bath approximation)

Author : Kévin Rémondière (ORCID 0009-0008-2443-7166).
"""
import os
os.environ.setdefault('JAX_ENABLE_X64', 'True')

import numpy as np
from scipy.sparse import csr_matrix, lil_matrix
from scipy.sparse.linalg import eigsh
from scipy.optimize import curve_fit
import json
import time

L_VALUES = [int(x) for x in os.environ.get('L_VALUES', '6,8,10').split(',')]
N_EIGS = int(os.environ.get('N_EIGS', 400))
N_CONFIGS = int(os.environ.get('N_CONFIGS', 8))
BETA = float(os.environ.get('BETA', 2.4))

print(f"=== d_s + d_∂ box-counting v2 ===", flush=True)
print(f"L_VALUES={L_VALUES}, N_EIGS={N_EIGS}, N_CONFIGS={N_CONFIGS}, β={BETA}", flush=True)


def site_idx(x, y, z, a, L, dim_adj=3):
    return ((z * L + y) * L + x) * dim_adj + a


def build_M_FP_heat_bath(L, key, n_thermalize=200):
    """Build M_FP for SU(2) field after rough heat-bath thermalization.

    Returns M_FP sparse matrix + U field (for box-counting later).
    """
    sigma = np.array([
        [[0,1],[1,0]],
        [[0,-1j],[1j,0]],
        [[1,0],[0,-1]],
    ]) / 2.0

    np.random.seed(key)

    # Initialize with small random SU(2) fluctuations
    U = np.zeros((L, L, L, 3, 2, 2), dtype=complex)
    for x in range(L):
        for y in range(L):
            for z in range(L):
                for mu in range(3):
                    # Random SU(2) near identity
                    a = np.array([1.0,
                                  0.2*np.random.randn(),
                                  0.2*np.random.randn(),
                                  0.2*np.random.randn()])
                    a = a / np.linalg.norm(a)
                    U[x,y,z,mu] = np.array([[a[0]+1j*a[3], a[2]+1j*a[1]],
                                             [-a[2]+1j*a[1], a[0]-1j*a[3]]])

    # Quick heat-bath sweeps on 3D spatial slice (simplified)
    for sweep in range(n_thermalize):
        for x in range(L):
            for y in range(L):
                for z in range(L):
                    for mu in range(3):
                        # Compute spatial staple
                        staple = np.zeros((2, 2), dtype=complex)
                        for nu in range(3):
                            if nu == mu: continue
                            # +nu staple
                            x2 = (x + (1 if mu==0 else 0)) % L
                            y2 = (y + (1 if mu==1 else 0)) % L
                            z2 = (z + (1 if mu==2 else 0)) % L
                            x3 = (x + (1 if nu==0 else 0)) % L
                            y3 = (y + (1 if nu==1 else 0)) % L
                            z3 = (z + (1 if nu==2 else 0)) % L
                            U_nu_a = U[x2,y2,z2,nu]
                            U_mu_b = U[x3,y3,z3,mu]
                            U_nu_c = U[x,y,z,nu]
                            staple += U_nu_a @ np.conj(U_mu_b).T @ np.conj(U_nu_c).T
                        # Heat-bath proposal : sample from action ~ exp(β/2 Tr(U·staple†))
                        # Simplified : update U by SU(2) noise scaled by 1/β
                        proposal_a = np.array([1.0,
                                                np.random.randn()/np.sqrt(BETA),
                                                np.random.randn()/np.sqrt(BETA),
                                                np.random.randn()/np.sqrt(BETA)])
                        proposal_a = proposal_a / np.linalg.norm(proposal_a)
                        U_prop = np.array([[proposal_a[0]+1j*proposal_a[3], proposal_a[2]+1j*proposal_a[1]],
                                            [-proposal_a[2]+1j*proposal_a[1], proposal_a[0]-1j*proposal_a[3]]])
                        # Accept ~ probability based on staple
                        # Simplified Metropolis
                        U_new = U_prop @ U[x,y,z,mu]
                        dS = -BETA/2 * (np.real(np.trace(U_new @ staple)) - np.real(np.trace(U[x,y,z,mu] @ staple)))
                        if np.random.rand() < np.exp(-dS):
                            U[x,y,z,mu] = U_new

    # Build M_FP
    N = L**3 * 3
    M = lil_matrix((N, N), dtype=np.float64)

    for z in range(L):
        for y in range(L):
            for x in range(L):
                for a in range(3):
                    idx = site_idx(x, y, z, a, L)
                    M[idx, idx] += 6.0
                    for mu, (dx, dy, dz) in enumerate([(1,0,0), (0,1,0), (0,0,1)]):
                        x2 = (x + dx) % L; y2 = (y + dy) % L; z2 = (z + dz) % L
                        x1 = (x - dx) % L; y1 = (y - dy) % L; z1 = (z - dz) % L
                        U_x = U[x, y, z, mu]
                        U_x1 = U[x1, y1, z1, mu]
                        for aa in range(3):
                            for bb in range(3):
                                Uadj_ab = np.real(np.trace(sigma[aa] @ U_x @ sigma[bb] @ np.conj(U_x).T))
                                U1adj_ab = np.real(np.trace(sigma[aa] @ U_x1 @ sigma[bb] @ np.conj(U_x1).T))
                                if aa == a:
                                    idx2 = site_idx(x2, y2, z2, bb, L)
                                    M[idx, idx2] -= Uadj_ab
                                    idx1 = site_idx(x1, y1, z1, bb, L)
                                    M[idx, idx1] -= U1adj_ab

    return csr_matrix(M), U


def box_count_near_zero(eigs, eigvecs, L, threshold_pct=10):
    """Box-counting proxy : near-zero-mode spatial support fractal dim.

    Take the lowest threshold_pct% of modes, compute their joint spatial
    support, then box-count for fractal dim.
    """
    n_modes = max(5, len(eigs) * threshold_pct // 100)
    low_modes = eigvecs[:, :n_modes]  # shape (3·L³, n_modes)

    # Total spatial probability density (sum over color, modes)
    rho_xyz = np.zeros((L, L, L))
    for i in range(n_modes):
        psi = low_modes[:, i].reshape(L, L, L, 3)
        rho_xyz += np.sum(np.abs(psi)**2, axis=3)

    # Threshold to get support
    thresh = np.percentile(rho_xyz, 80)  # top 20% sites
    support_mask = rho_xyz > thresh

    # Box-counting
    box_sizes = [1, 2]
    counts = []
    for bs in box_sizes:
        if L // bs < 2:
            continue
        n_box = 0
        for bx in range(0, L, bs):
            for by in range(0, L, bs):
                for bz in range(0, L, bs):
                    if support_mask[bx:bx+bs, by:by+bs, bz:bz+bs].any():
                        n_box += 1
        counts.append((bs, n_box))

    # Fit log(N) = -d_f log(bs) + const
    if len(counts) >= 2:
        log_bs = np.log([c[0] for c in counts])
        log_N = np.log([c[1] for c in counts])
        d_f = -(log_N[-1] - log_N[0]) / (log_bs[-1] - log_bs[0])
    else:
        d_f = None

    return {'counts': counts, 'd_f_boxcount': d_f, 'n_modes_used': n_modes, 'total_support_voxels': int(support_mask.sum())}


def fit_d_s_and_alpha(eigs):
    """Comprehensive fit of d_s from spectrum."""
    eigs = np.array(eigs)
    eigs_nonzero = eigs[eigs > 1e-9]

    # 1. ρ(λ) ~ λ^α small-λ tail
    n_low = max(20, len(eigs_nonzero) // 4)
    low_eigs = eigs_nonzero[:n_low]
    # Linear bins
    bins = np.linspace(low_eigs.min(), low_eigs.max(), 15)
    hist, edges = np.histogram(low_eigs, bins=bins)
    centers = (edges[:-1] + edges[1:]) / 2
    widths = edges[1:] - edges[:-1]
    rho = hist / (widths * len(low_eigs))
    mask = (rho > 0) & (centers > 0)
    if mask.sum() >= 4:
        log_c = np.log(centers[mask])
        log_r = np.log(rho[mask])
        p = np.polyfit(log_c, log_r, 1)
        alpha = p[0]
        d_s_density = 2 * (alpha + 1)
    else:
        alpha = None
        d_s_density = None

    # 2. Z(t) ~ t^{-d_s/2} small-t (excluding both very small and large t)
    lambda_min = eigs_nonzero.min()
    lambda_max = eigs_nonzero.max()
    t_min = 0.05 / lambda_max
    t_max = 1.0 / lambda_min
    ts = np.logspace(np.log10(t_min), np.log10(t_max), 40)
    Z = np.array([np.sum(np.exp(-t * eigs_nonzero)) for t in ts])
    log_t = np.log(ts)
    log_Z = np.log(Z + 1e-15)
    # Use SMALL-t regime: first 30%
    n_use = max(8, len(ts) * 30 // 100)
    p_heat = np.polyfit(log_t[:n_use], log_Z[:n_use], 1)
    d_s_heat = -2 * p_heat[0]

    # 3. Weyl law : N(λ) ~ λ^{d_s/2}
    sorted_eigs = np.sort(eigs_nonzero)
    n_lambda = np.arange(1, len(sorted_eigs)+1)
    # Use first 50% for Weyl fit (cleanest scaling near origin)
    n_use_weyl = len(sorted_eigs) // 2
    log_lambda = np.log(sorted_eigs[:n_use_weyl])
    log_N = np.log(n_lambda[:n_use_weyl])
    p_weyl = np.polyfit(log_lambda, log_N, 1)
    d_s_weyl = 2 * p_weyl[0]

    return {
        'alpha_density': alpha,
        'd_s_density': d_s_density,
        'd_s_heat': d_s_heat,
        'd_s_weyl': d_s_weyl,
    }


def main():
    all_results = {}

    for L in L_VALUES:
        print(f"\n{'='*50}", flush=True)
        print(f"L = {L}, dim(M_FP) = {3*L**3}", flush=True)
        print(f"{'='*50}", flush=True)

        all_eigs = []
        all_eigvecs = []

        for cfg in range(N_CONFIGS):
            t0 = time.time()
            print(f"\n  Config {cfg+1}/{N_CONFIGS} ...", flush=True)
            M, U = build_M_FP_heat_bath(L, key=cfg*7919 + L*1000)
            print(f"    M_FP built {time.time()-t0:.1f}s", flush=True)

            t1 = time.time()
            try:
                k_use = min(N_EIGS, M.shape[0]-2)
                eigs, vecs = eigsh(M, k=k_use, which='SM', tol=1e-8)
                idx_sort = np.argsort(eigs)
                eigs = eigs[idx_sort]
                vecs = vecs[:, idx_sort]
                print(f"    Lanczos {k_use} eigs {time.time()-t1:.1f}s, λ_min={eigs[0]:.4e}, λ_max={eigs[-1]:.4e}", flush=True)
                all_eigs.append(eigs)
                all_eigvecs.append(vecs)
            except Exception as ex:
                print(f"    Lanczos failed: {ex}", flush=True)

        if not all_eigs:
            continue

        # Combine
        eigs_combined = np.concatenate(all_eigs)
        eigs_combined = np.sort(eigs_combined)

        # Spectral fits
        spec_fit = fit_d_s_and_alpha(eigs_combined)
        print(f"\n  SPECTRAL FITS L={L}:", flush=True)
        print(f"    α (density) = {spec_fit['alpha_density']:.4f}  (predict 1/6 = 0.1667)", flush=True)
        print(f"    d_s (density) = {spec_fit['d_s_density']:.4f}  (predict 7/3 = 2.333)", flush=True)
        print(f"    d_s (heat trace) = {spec_fit['d_s_heat']:.4f}  (predict 7/3 = 2.333)", flush=True)
        print(f"    d_s (Weyl) = {spec_fit['d_s_weyl']:.4f}  (predict 7/3 = 2.333)", flush=True)

        # Box-counting on first config (largest L sample)
        bc = box_count_near_zero(all_eigs[0], all_eigvecs[0], L, threshold_pct=5)
        print(f"  BOX-COUNTING (first config) :", flush=True)
        print(f"    n_modes used = {bc['n_modes_used']}", flush=True)
        print(f"    support voxels = {bc['total_support_voxels']}/{L**3}", flush=True)
        print(f"    d_f (boxcount) = {bc['d_f_boxcount']}  (predict d_∂ = 2/3 ≈ 0.667)", flush=True)

        all_results[f"L_{L}"] = {
            'L': L,
            'dim_M_FP': 3*L**3,
            'n_configs': len(all_eigs),
            'n_eigs_per_config': k_use,
            'spectral_fits': spec_fit,
            'box_counting': bc,
            'eigs_first_10': eigs_combined[:10].tolist(),
            'eigs_last_10': eigs_combined[-10:].tolist(),
        }

    out = {
        'beta': BETA,
        'L_values': L_VALUES,
        'N_eigs': N_EIGS,
        'N_configs': N_CONFIGS,
        'results_per_L': all_results,
        'predictions': {
            'd_s = 7/3 (decoder)': 7/3,
            'α (density) = 1/6': 1/6,
            'd_∂ = 2/3 (Gribov horizon fractal)': 2/3,
        }
    }

    fout = f'/tmp/jax_dS_v2_results.json'
    with open(fout, 'w') as f:
        json.dump(out, f, indent=2, default=lambda x: float(x) if hasattr(x, 'item') else x)
    print(f"\n→ Saved {fout}", flush=True)

    # Final summary
    print(f"\n{'='*70}", flush=True)
    print(f"FINAL SUMMARY", flush=True)
    print(f"{'='*70}", flush=True)
    print(f"{'L':<5} {'α_dens':>10s} {'d_s_dens':>10s} {'d_s_heat':>10s} {'d_s_weyl':>10s} {'d_∂_box':>10s}")
    for sk, sv in all_results.items():
        L = sv['L']
        sf = sv['spectral_fits']
        bc = sv['box_counting']
        a = sf['alpha_density']
        ds_d = sf['d_s_density']
        ds_h = sf['d_s_heat']
        ds_w = sf['d_s_weyl']
        d_f = bc['d_f_boxcount']
        print(f"{L:<5} {a if a else 'N/A':>10} {ds_d if ds_d else 'N/A':>10} {ds_h:>10.4f} {ds_w:>10.4f} {d_f if d_f else 'N/A':>10}")
    print(f"\nDECODER PREDICTIONS : d_s = 7/3 = 2.333, α = 1/6 = 0.167, d_∂ = 2/3 = 0.667")


if __name__ == '__main__':
    main()
