#!/usr/bin/env python3
"""Wilson-Dirac spectrum FAST version with 4 optimizations :
   1. k=3 (only need gap, not 10 eigenvalues)
   2. tol=1e-3 (gap is O(1), no need machine precision)
   3. sigma near gap_estimate (shift-invert converges fast)
   4. which='LM' with shift (numerically stable)
   
Plus : use D†D instead of D_W (Hermitian → eigsh proper).
"""
import numpy as np
import scipy.sparse as sp
from scipy.sparse.linalg import eigsh, lobpcg
import sys, glob, json, time, os, math

def gamma_matrices():
    sigma_x = np.array([[0, 1], [1, 0]], dtype=complex)
    sigma_y = np.array([[0, -1j], [1j, 0]], dtype=complex)
    sigma_z = np.array([[1, 0], [0, -1]], dtype=complex)
    I2 = np.eye(2, dtype=complex)
    
    g0 = np.block([[np.zeros((2,2)), I2], [I2, np.zeros((2,2))]])
    g1 = np.block([[np.zeros((2,2)), -1j*sigma_x], [1j*sigma_x, np.zeros((2,2))]])
    g2 = np.block([[np.zeros((2,2)), -1j*sigma_y], [1j*sigma_y, np.zeros((2,2))]])
    g3 = np.block([[np.zeros((2,2)), -1j*sigma_z], [1j*sigma_z, np.zeros((2,2))]])
    return [g0, g1, g2, g3]

def quat_to_su2(q):
    a0, a1, a2, a3 = q[0], q[1], q[2], q[3]
    return np.array([
        [a0 + 1j*a3, a2 + 1j*a1],
        [-a2 + 1j*a1, a0 - 1j*a3]
    ], dtype=complex)

def build_wilson_dirac(links, m0=0.1):
    L = links.shape[0]
    V = L**4
    n_dof = 8  # 4 Dirac × 2 color
    N_total = V * n_dof
    gammas = gamma_matrices()
    
    rows, cols, data = [], [], []
    print(f"  V={V} N_total={N_total}", end=' ', flush=True)
    
    for site_idx in range(V):
        x = site_idx // (L**3); y = (site_idx // (L**2)) % L
        z = (site_idx // L) % L; t = site_idx % L
        coord = (x, y, z, t)
        
        # Mass term
        for a in range(n_dof):
            idx = site_idx * n_dof + a
            rows.append(idx); cols.append(idx); data.append(m0)
        
        for mu in range(4):
            coord_next = list(coord); coord_next[mu] = (coord_next[mu]+1) % L
            site_next = coord_next[0]*L**3 + coord_next[1]*L**2 + coord_next[2]*L + coord_next[3]
            U_mu = quat_to_su2(links[coord + (mu,)])
            
            gm = gammas[mu]
            proj_f = (np.eye(4) - gm)/2
            proj_b = (np.eye(4) + gm)/2
            
            hop_f = -np.kron(proj_f, U_mu)
            for a in range(n_dof):
                for b in range(n_dof):
                    if abs(hop_f[a, b]) > 1e-10:
                        rows.append(site_idx * n_dof + a)
                        cols.append(site_next * n_dof + b)
                        data.append(hop_f[a, b])
            
            coord_prev = list(coord); coord_prev[mu] = (coord_prev[mu]-1) % L
            site_prev = coord_prev[0]*L**3 + coord_prev[1]*L**2 + coord_prev[2]*L + coord_prev[3]
            U_mu_prev = quat_to_su2(links[tuple(coord_prev) + (mu,)])
            hop_b = -np.kron(proj_b, np.conj(U_mu_prev.T))
            
            for a in range(n_dof):
                for b in range(n_dof):
                    if abs(hop_b[a, b]) > 1e-10:
                        rows.append(site_idx * n_dof + a)
                        cols.append(site_prev * n_dof + b)
                        data.append(hop_b[a, b])
    
    H = sp.csr_matrix((data, (rows, cols)), shape=(N_total, N_total))
    print(f"NNZ={H.nnz}", end=' ', flush=True)
    return H

def main():
    files = sorted(glob.glob("results/hmc_b*_L*.npz"))
    if not files:
        print("No HMC configs found.")
        sys.exit(1)
    
    # Framework gap estimates per β
    K = math.sqrt(2*math.pi*math.e*2/3)  # ≈ 3.374
    F2 = 1.125  # F(N=2)
    
    for npz in files:
        print(f"\n=== {os.path.basename(npz)} ===")
        data = np.load(npz)
        configs = data['configs']
        L = int(data['L'])
        beta = float(data['beta'])
        n_configs = min(3, len(configs))  # 3 configs (fast)
        
        # Bali sqrt(sigma)*a from beta
        # SU(2) : a√σ ≈ 0.5 at β=2.3, 0.3 at β=2.5, 0.2 at β=2.7 (Lucini-Teper)
        a_sqrt_sigma = {2.3: 0.5, 2.5: 0.3, 2.7: 0.2}.get(round(beta, 1), 0.3)
        # gap estimate in lattice units : K·F·c·√sigma_lat
        c_su2_0pp = math.sqrt(16/15)  # c²(0++) ≈ 1.067
        gap_est = K * F2 * c_su2_0pp * a_sqrt_sigma
        print(f"  L={L} β={beta} configs={n_configs} gap_est ≈ {gap_est:.3f}")
        
        results_b = []
        for i in range(n_configs):
            t0 = time.time()
            D = build_wilson_dirac(configs[i], m0=0.1)
            print(f"\n  Config {i}: ", end='', flush=True)
            
            # Use D†D (Hermitian, positive) for eigsh
            DdD = (D.conj().T @ D).tocsr()
            
            try:
                # OPTIM 1+2+3+4 : k=3, tol=1e-3, sigma near gap², LM mode
                sigma_shift = gap_est**2 * 0.5  # near smallest non-zero |λ|² of D†D
                eigs = eigsh(DdD, k=3, sigma=sigma_shift, which='LM', 
                             tol=1e-3, maxiter=500, return_eigenvectors=False)
                eigs_abs = np.sqrt(np.abs(eigs))  # back to |λ| of D
                eigs_sorted = np.sort(eigs_abs)
                print(f"|λ|_smallest = {eigs_sorted[0]:.4f}, {eigs_sorted[1]:.4f}, {eigs_sorted[2]:.4f}")
                print(f"  Time: {time.time()-t0:.0f}s")
                results_b.append({'config': i, 'eigs': eigs_sorted.tolist(), 'time_s': time.time()-t0})
            except Exception as e:
                print(f"ERROR : {e}")
                # Fallback : LOBPCG
                try:
                    X = np.random.randn(DdD.shape[0], 3) + 1j*np.random.randn(DdD.shape[0], 3)
                    eigs_l, _ = lobpcg(DdD, X, largest=False, tol=1e-3, maxiter=200)
                    print(f"  LOBPCG : eigs = {np.sort(np.sqrt(np.abs(eigs_l)))[:3]}")
                except Exception as e2:
                    print(f"  LOBPCG also failed : {e2}")
                    results_b.append({'config': i, 'error': str(e)})
        
        out = f"results/dirac_b{int(beta*10)}.json"
        with open(out, 'w') as f:
            json.dump({
                'beta': beta, 'L': L,
                'gap_estimate_framework': gap_est,
                'configs': results_b,
                'n_configs': len(results_b),
            }, f, indent=2)
        print(f"\n  ✓ Saved {out}")

if __name__ == "__main__":
    main()
