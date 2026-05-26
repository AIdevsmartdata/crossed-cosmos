#!/usr/bin/env python3
"""
λ_min DISTRIBUTION sur MANY configs → test ρ(λ) ~ λ^{1/6}.

Stratégie : génère N_configs (200-1000) thermalisées SU(2) Wilson β=2.4,
extrait λ_min(Δ_FP) seulement (cheap ARPACK k=1), construit histogramme.

Si α (slope log-log) = 1/6 ± 0.02 → d_s = 7/3 CONFIRMÉ.

Author : Kévin Rémondière (ORCID 0009-0008-2443-7166).
"""
import os
os.environ.setdefault('JAX_ENABLE_X64', 'True')

import numpy as np
from scipy.sparse import csr_matrix, lil_matrix
from scipy.sparse.linalg import eigsh
import json
import time

L = int(os.environ.get('L', 8))
BETA = float(os.environ.get('BETA', 2.4))
N_CONFIGS = int(os.environ.get('N_CONFIGS', 200))
N_THERM = int(os.environ.get('N_THERM', 500))  # quick thermalize per config
N_KEEP_LOWEST = int(os.environ.get('N_KEEP_LOWEST', 5))  # lowest k eigs per config

print(f"=== λ_min distribution test, L={L}, β={BETA}, N_configs={N_CONFIGS} ===", flush=True)

sigma_pauli = np.array([
    [[0,1],[1,0]],
    [[0,-1j],[1j,0]],
    [[1,0],[0,-1]],
]) / 2.0


def site_idx(x, y, z, a, L, dim_adj=3):
    return ((z * L + y) * L + x) * dim_adj + a


def heat_bath_su2(U, beta, L, n_sweeps):
    """Quick heat-bath sweep on spatial links (3D)."""
    for sweep in range(n_sweeps):
        for x in range(L):
            for y in range(L):
                for z in range(L):
                    for mu in range(3):
                        # Compute spatial staple
                        staple = np.zeros((2, 2), dtype=complex)
                        for nu in range(3):
                            if nu == mu: continue
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
                            # -nu staple
                            xm = (x + (1 if mu==0 else 0) - (1 if nu==0 else 0)) % L
                            ym = (y + (1 if mu==1 else 0) - (1 if nu==1 else 0)) % L
                            zm = (z + (1 if mu==2 else 0) - (1 if nu==2 else 0)) % L
                            x_minus = (x - (1 if nu==0 else 0)) % L
                            y_minus = (y - (1 if nu==1 else 0)) % L
                            z_minus = (z - (1 if nu==2 else 0)) % L
                            U_nu_m = U[x_minus, y_minus, z_minus, nu]
                            U_mu_m = U[x_minus, y_minus, z_minus, mu]
                            U_nu_mp = U[xm, ym, zm, nu]
                            staple += np.conj(U_nu_m).T @ U_mu_m @ U_nu_mp
                        # Metropolis proposal scaled by 1/sqrt(β)
                        proposal_a = np.array([1.0,
                                                np.random.randn()/np.sqrt(beta),
                                                np.random.randn()/np.sqrt(beta),
                                                np.random.randn()/np.sqrt(beta)])
                        proposal_a = proposal_a / np.linalg.norm(proposal_a)
                        U_prop_mat = np.array([[proposal_a[0]+1j*proposal_a[3], proposal_a[2]+1j*proposal_a[1]],
                                                [-proposal_a[2]+1j*proposal_a[1], proposal_a[0]-1j*proposal_a[3]]])
                        U_new = U_prop_mat @ U[x,y,z,mu]
                        dS = -beta/2 * (np.real(np.trace(U_new @ staple)) - np.real(np.trace(U[x,y,z,mu] @ staple)))
                        if np.random.rand() < np.exp(-dS):
                            U[x,y,z,mu] = U_new
    return U


def build_M_FP(U, L):
    """Build Δ_FP sparse matrix on 3D spatial slice."""
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
                        Uadj_a_bb = np.array([np.real(np.trace(sigma_pauli[a] @ U_x @ sigma_pauli[bb] @ np.conj(U_x).T)) for bb in range(3)])
                        U1adj_a_bb = np.array([np.real(np.trace(sigma_pauli[a] @ U_x1 @ sigma_pauli[bb] @ np.conj(U_x1).T)) for bb in range(3)])
                        for bb in range(3):
                            idx2 = site_idx(x2, y2, z2, bb, L)
                            M[idx, idx2] -= Uadj_a_bb[bb]
                            idx1 = site_idx(x1, y1, z1, bb, L)
                            M[idx, idx1] -= U1adj_a_bb[bb]

    return csr_matrix(M)


def main():
    np.random.seed(42)
    print(f"\nGénération {N_CONFIGS} configs avec {N_THERM} sweeps each", flush=True)

    # Initialize SU(2) field
    U = np.zeros((L, L, L, 3, 2, 2), dtype=complex)
    for x in range(L):
        for y in range(L):
            for z in range(L):
                for mu in range(3):
                    a = np.array([1.0,
                                  0.2*np.random.randn(),
                                  0.2*np.random.randn(),
                                  0.2*np.random.randn()])
                    a = a / np.linalg.norm(a)
                    U[x,y,z,mu] = np.array([[a[0]+1j*a[3], a[2]+1j*a[1]],
                                             [-a[2]+1j*a[1], a[0]-1j*a[3]]])

    # Initial thermalization
    print("Thermalisation initiale...", flush=True)
    t0 = time.time()
    U = heat_bath_su2(U, BETA, L, 1000)
    print(f"  Done in {time.time()-t0:.1f}s", flush=True)

    # Generate configs and extract λ_min, λ_2, ..., λ_k
    lambda_mins = []
    low_eigs_all = []
    plaquettes = []

    for cfg in range(N_CONFIGS):
        # Decorrelation sweeps
        U = heat_bath_su2(U, BETA, L, 30)

        # Build M_FP
        M = build_M_FP(U, L)

        # Lanczos lowest k
        try:
            eigs = eigsh(M, k=N_KEEP_LOWEST, which='SM', return_eigenvectors=False, tol=1e-7)
            eigs = np.sort(eigs)
            lambda_mins.append(eigs[0])
            low_eigs_all.append(eigs.tolist())
        except Exception as ex:
            print(f"  Config {cfg} Lanczos failed: {ex}", flush=True)
            continue

        # Quick plaquette
        if cfg % 10 == 0:
            t_now = time.time() - t0
            plaq_sample = 0.0
            count = 0
            for x in range(0, L, 2):
                for y in range(0, L, 2):
                    for z in range(0, L, 2):
                        for mu in range(2):
                            for nu in range(mu+1, 3):
                                x2 = (x + (1 if mu==0 else 0)) % L
                                y2 = (y + (1 if mu==1 else 0)) % L
                                z2 = (z + (1 if mu==2 else 0)) % L
                                x3 = (x + (1 if nu==0 else 0)) % L
                                y3 = (y + (1 if nu==1 else 0)) % L
                                z3 = (z + (1 if nu==2 else 0)) % L
                                P = U[x,y,z,mu] @ U[x2,y2,z2,nu] @ np.conj(U[x3,y3,z3,mu]).T @ np.conj(U[x,y,z,nu]).T
                                plaq_sample += np.real(np.trace(P))/2
                                count += 1
            plaquette = plaq_sample / count
            plaquettes.append(plaquette)
            print(f"  Config {cfg+1}/{N_CONFIGS}: ⟨P⟩~{plaquette:.4f}, λ_min={eigs[0]:.4e}, t={t_now:.1f}s", flush=True)

    lambda_mins = np.array(lambda_mins)
    print(f"\nCollected {len(lambda_mins)} λ_min values", flush=True)
    print(f"  Range : [{lambda_mins.min():.4e}, {lambda_mins.max():.4e}]", flush=True)
    print(f"  Mean : {lambda_mins.mean():.4e}, std : {lambda_mins.std():.4e}", flush=True)

    # Build histogram on log scale
    print("\n=== Fit ρ(λ_min) ~ λ^α ===", flush=True)
    # Use linear bins on lower tail
    n_use = max(20, len(lambda_mins) // 3)
    sorted_lmin = np.sort(lambda_mins)
    tail = sorted_lmin[:n_use]
    bins = np.linspace(tail.min(), tail.max(), 12)
    hist, edges = np.histogram(tail, bins=bins)
    centers = (edges[:-1] + edges[1:]) / 2
    widths = edges[1:] - edges[:-1]
    rho = hist / (widths * n_use)
    mask = (rho > 0) & (centers > 0)
    if mask.sum() >= 4:
        log_c = np.log(centers[mask])
        log_r = np.log(rho[mask])
        p = np.polyfit(log_c, log_r, 1)
        alpha = p[0]
        d_s_density = 2 * (alpha + 1)
        print(f"  α = {alpha:.4f} (predict 1/6 = 0.1667)", flush=True)
        print(f"  d_s = 2(α+1) = {d_s_density:.4f} (predict 7/3 = 2.333)", flush=True)
        print(f"  σ from 1/6 : Δ = {alpha - 1/6:+.4f}", flush=True)
    else:
        alpha = None
        d_s_density = None
        print("  Not enough points for fit", flush=True)

    # Also compute integrated CDF : N(λ) = ∫_0^λ ρ(λ') dλ'
    # If ρ ~ λ^α then N(λ) ~ λ^{α+1}
    # Test by ranking : F_emp(λ_n) = n/N_total
    sorted_all = np.sort(lambda_mins)
    rank = np.arange(1, len(sorted_all)+1)
    F = rank / len(sorted_all)
    # Use first 50% to fit power law
    n_cdf = len(sorted_all) // 2
    log_lambda = np.log(sorted_all[:n_cdf])
    log_F = np.log(F[:n_cdf])
    p_cdf = np.polyfit(log_lambda, log_F, 1)
    alpha_cdf = p_cdf[0] - 1  # F ~ λ^{α+1} → log F = (α+1) log λ + b
    print(f"\n  CDF fit (more robust) : α_cdf = {alpha_cdf:.4f} (predict 1/6 = 0.1667)", flush=True)
    print(f"  d_s_cdf = {2*(alpha_cdf+1):.4f}", flush=True)

    # Save
    out = {
        'L': L, 'BETA': BETA, 'N_CONFIGS': N_CONFIGS, 'N_THERM': N_THERM,
        'lambda_mins': lambda_mins.tolist(),
        'plaquettes': plaquettes,
        'alpha_histogram': float(alpha) if alpha else None,
        'd_s_histogram': float(d_s_density) if d_s_density else None,
        'alpha_cdf': float(alpha_cdf),
        'd_s_cdf': float(2*(alpha_cdf+1)),
        'low_eigs_first_20': low_eigs_all[:20],
        'predictions': {
            'd_s = 7/3': 7/3,
            'α = 1/6': 1/6,
        }
    }
    with open(f'/tmp/lambda_min_dist_L{L}.json', 'w') as f:
        json.dump(out, f, indent=2)
    print(f"\n→ Saved /tmp/lambda_min_dist_L{L}.json", flush=True)


if __name__ == '__main__':
    main()
