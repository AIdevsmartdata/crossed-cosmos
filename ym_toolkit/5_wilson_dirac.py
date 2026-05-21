#!/usr/bin/env python3
"""Wilson-Dirac operator spectrum on HMC configs.
   
Goal : Diagonalize D_W on SU(2) configs, compare smallest non-zero eigenvalue
       with our framework m²/σ prediction.

D_W ψ(x) = (1/2) Σ_μ [(1-γ_μ) U_μ(x) ψ(x+μ̂) - (1+γ_μ) U_μ(x-μ̂)† ψ(x-μ̂)] + m_0 ψ(x)

For SU(2), fermion in fundamental rep, link U_μ is 2x2 SU(2) matrix.
Spinors ψ have 4 Dirac components × 2 color = 8 components per site.

Use scipy.sparse.linalg.eigsh for smallest absolute eigenvalues.
Goal : test relation eigenvalue spectrum ↔ c² framework.
"""
import numpy as np
import scipy.sparse as sp
from scipy.sparse.linalg import eigsh
import sys, glob, json, time, os

# Dirac gamma matrices (chiral rep)
# γ_0, γ_1, γ_2, γ_3 in 4D Euclidean
def gamma_matrices():
    sigma_x = np.array([[0, 1], [1, 0]], dtype=complex)
    sigma_y = np.array([[0, -1j], [1j, 0]], dtype=complex)
    sigma_z = np.array([[1, 0], [0, -1]], dtype=complex)
    I2 = np.eye(2, dtype=complex)
    
    # Euclidean γ_i = ((0, σ_i), (σ_i, 0)) chiral
    g0 = np.block([[np.zeros((2,2)), I2], [I2, np.zeros((2,2))]])
    g1 = np.block([[np.zeros((2,2)), -1j*sigma_x], [1j*sigma_x, np.zeros((2,2))]])
    g2 = np.block([[np.zeros((2,2)), -1j*sigma_y], [1j*sigma_y, np.zeros((2,2))]])
    g3 = np.block([[np.zeros((2,2)), -1j*sigma_z], [1j*sigma_z, np.zeros((2,2))]])
    return [g0, g1, g2, g3]

def quat_to_su2(q):
    """SU(2) quaternion to 2x2 matrix."""
    a0, a1, a2, a3 = q[0], q[1], q[2], q[3]
    return np.array([
        [a0 + 1j*a3, a2 + 1j*a1],
        [-a2 + 1j*a1, a0 - 1j*a3]
    ], dtype=complex)

def build_wilson_dirac(links, m0=0.1):
    """Build sparse Wilson-Dirac operator for SU(2) lattice."""
    L = links.shape[0]
    V = L**4
    n_spinor = 4  # Dirac
    n_color = 2   # SU(2) fundamental
    n_dof = n_spinor * n_color  # 8 per site
    N_total = V * n_dof
    
    gammas = gamma_matrices()
    
    rows, cols, data = [], [], []
    
    print(f"  Building sparse Wilson-Dirac : V={V}, N_total={N_total}")
    
    for site_idx in range(V):
        # Compute coordinates
        x, y, z, t = site_idx // (L**3), (site_idx // (L**2)) % L, (site_idx // L) % L, site_idx % L
        coord = (x, y, z, t)
        
        # Mass term : m_0 · I
        for a in range(n_dof):
            idx = site_idx * n_dof + a
            rows.append(idx); cols.append(idx); data.append(m0)
        
        # Hopping terms : for each direction μ
        for mu in range(4):
            coord_next = list(coord); coord_next[mu] = (coord_next[mu]+1) % L
            site_next = coord_next[0]*L**3 + coord_next[1]*L**2 + coord_next[2]*L + coord_next[3]
            
            U_mu = quat_to_su2(links[coord + (mu,)])
            
            gm = gammas[mu]
            # I - γ_μ for forward hop (Wilson term)
            proj_f = (np.eye(4) - gm)/2
            # I + γ_μ for backward hop
            proj_b = (np.eye(4) + gm)/2
            
            # Forward hop coefficient : -(1/2)·(I - γ_μ) ⊗ U_μ(x)
            hop_f = -np.kron(proj_f, U_mu)
            # Backward hop : -(1/2)·(I + γ_μ) ⊗ U_μ†(x-μ̂)
            
            # Insert hop_f matrix elements
            for a in range(n_dof):
                for b in range(n_dof):
                    if abs(hop_f[a, b]) > 1e-10:
                        idx_from = site_next * n_dof + b
                        idx_to = site_idx * n_dof + a
                        rows.append(idx_to); cols.append(idx_from); data.append(hop_f[a, b])
                    # Backward : need to compute hop from site_prev to site_idx
            
            # Backward : look at neighbor in -μ direction
            coord_prev = list(coord); coord_prev[mu] = (coord_prev[mu]-1) % L
            site_prev = coord_prev[0]*L**3 + coord_prev[1]*L**2 + coord_prev[2]*L + coord_prev[3]
            U_mu_prev = quat_to_su2(links[tuple(coord_prev) + (mu,)])
            hop_b = -np.kron(proj_b, np.conj(U_mu_prev.T))  # U†
            
            for a in range(n_dof):
                for b in range(n_dof):
                    if abs(hop_b[a, b]) > 1e-10:
                        idx_from = site_prev * n_dof + b
                        idx_to = site_idx * n_dof + a
                        rows.append(idx_to); cols.append(idx_from); data.append(hop_b[a, b])
        
        if site_idx % max(1, V//10) == 0:
            print(f"    Build progress {site_idx}/{V}", end='\r')
    
    print(f"\n    NNZ : {len(data)}, sparse density : {len(data)/N_total**2*100:.3f}%")
    H = sp.csr_matrix((data, (rows, cols)), shape=(N_total, N_total))
    return H

def main():
    # Find configs
    files = sorted(glob.glob("results/hmc_b*_L*.npz"))
    if not files:
        print("No HMC configs found.")
        sys.exit(1)
    
    for npz in files:
        print(f"\n=== {os.path.basename(npz)} ===")
        data = np.load(npz)
        configs = data['configs']
        L = int(data['L'])
        beta = float(data['beta'])
        n_configs = min(5, len(configs))  # Use only 5 configs (cost)
        print(f"  L={L}, β={beta}, using {n_configs} configs")
        
        # Diagonalize D_W on first few configs
        eigvals_low = []
        for i in range(n_configs):
            t0 = time.time()
            D_W = build_wilson_dirac(configs[i], m0=0.1)
            print(f"    Diag : compute 10 smallest eigenvalues...")
            # Smallest absolute eigenvalues
            try:
                eigs = eigsh(D_W, k=10, sigma=0, which='LM', return_eigenvectors=False, maxiter=2000)
                eigs_sorted = np.sort(np.abs(eigs))
                eigvals_low.append(eigs_sorted)
                print(f"    Config {i}: smallest |λ| = {eigs_sorted[:5]}")
                print(f"    Time : {time.time()-t0:.0f}s")
            except Exception as e:
                print(f"    ERROR : {e}")
                continue
        
        if eigvals_low:
            eigvals_low = np.array(eigvals_low)
            print(f"\n  Mean smallest |λ| (across {len(eigvals_low)} configs):")
            print(f"    {eigvals_low.mean(axis=0)[:5]}")
            print(f"\n  First non-zero eigenvalue ≈ {eigvals_low.mean(axis=0)[1]:.4f}")
            print(f"  Compare with framework c² × scale_factor")
            
            # Save
            out = f"results/dirac_b{int(beta*10)}.json"
            with open(out, 'w') as f:
                json.dump({
                    'beta': beta, 'L': L, 'n_configs': len(eigvals_low),
                    'mean_smallest_5': eigvals_low.mean(axis=0)[:5].tolist(),
                    'first_nonzero': float(eigvals_low.mean(axis=0)[1] if len(eigvals_low[0]) > 1 else 0),
                }, f, indent=2)
            print(f"  ✓ Saved {out}")

if __name__ == "__main__":
    main()
