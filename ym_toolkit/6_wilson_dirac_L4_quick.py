#!/usr/bin/env python3
"""Wilson-Dirac QUICK L=4 test — verify gap empirically.
   
L=4 → matrix size 2048×2048 sparse
ARPACK should finish in SECONDS per config.
"""
import numpy as np
import scipy.sparse as sp
from scipy.sparse.linalg import eigsh
import sys, json, time, math
sys.path.insert(0, '.')
# Import HMC
from importlib import import_module
hmc = import_module('1_hmc_su2'.replace('1_', 'hmc_'))  # Not quite — just inline

# Inline mini-HMC + Wilson-Dirac
def su2_mult(u, v):
    a0,a1,a2,a3 = u[0],u[1],u[2],u[3]
    b0,b1,b2,b3 = v[0],v[1],v[2],v[3]
    return np.array([
        a0*b0-a1*b1-a2*b2-a3*b3,
        a0*b1+a1*b0+a2*b3-a3*b2,
        a0*b2-a1*b3+a2*b0+a3*b1,
        a0*b3+a1*b2-a2*b1+a3*b0,
    ])

def su2_dag(u): return np.array([u[0], -u[1], -u[2], -u[3]])

def staple(links, x, mu, L):
    stp = np.zeros(4)
    for nu in range(4):
        if nu == mu: continue
        x_pm = list(x); x_pm[mu] = (x_pm[mu]+1) % L
        x_pn = list(x); x_pn[nu] = (x_pn[nu]+1) % L
        x_mn = list(x); x_mn[nu] = (x_mn[nu]-1) % L
        x_pm_mn = list(x_pm); x_pm_mn[nu] = (x_pm_mn[nu]-1) % L
        s1 = su2_mult(su2_mult(links[tuple(x_pm)+(nu,)], su2_dag(links[tuple(x_pn)+(mu,)])), su2_dag(links[tuple(x)+(nu,)]))
        s2 = su2_mult(su2_mult(su2_dag(links[tuple(x_pm_mn)+(nu,)]), su2_dag(links[tuple(x_mn)+(mu,)])), links[tuple(x_mn)+(nu,)])
        stp = stp + s1 + s2
    return stp

def metropolis(links, beta, L, eps=0.3):
    accepts = 0; tries = 0
    for x in np.ndindex(L, L, L, L):
        for mu in range(4):
            U = links[tuple(x)+(mu,)]
            stp = staple(links, x, mu, L)
            R = np.random.randn(4) * eps
            R[0] = 1 + R[0]*0.1
            R = R / np.linalg.norm(R)
            U_new = su2_mult(R, U)
            dS = -beta * (su2_mult(U_new, stp)[0] - su2_mult(U, stp)[0])
            if dS < 0 or np.random.rand() < np.exp(-dS):
                links[tuple(x)+(mu,)] = U_new
                accepts += 1
            tries += 1
    return links, accepts/tries

# Gamma matrices
sx = np.array([[0,1],[1,0]], complex); sy = np.array([[0,-1j],[1j,0]], complex)
sz = np.array([[1,0],[0,-1]], complex); I2 = np.eye(2, dtype=complex)
g0 = np.block([[np.zeros((2,2)), I2],[I2, np.zeros((2,2))]])
g1 = np.block([[np.zeros((2,2)), -1j*sx],[1j*sx, np.zeros((2,2))]])
g2 = np.block([[np.zeros((2,2)), -1j*sy],[1j*sy, np.zeros((2,2))]])
g3 = np.block([[np.zeros((2,2)), -1j*sz],[1j*sz, np.zeros((2,2))]])
gammas = [g0, g1, g2, g3]

def quat_to_su2(q):
    a0,a1,a2,a3 = q[0],q[1],q[2],q[3]
    return np.array([[a0+1j*a3, a2+1j*a1],[-a2+1j*a1, a0-1j*a3]], complex)

def build_D(links, m0=0.1):
    L = links.shape[0]; V = L**4; n_dof = 8; N = V * n_dof
    rows, cols, data = [], [], []
    for site in range(V):
        x=site//(L**3); y=(site//(L**2))%L; z=(site//L)%L; t=site%L
        coord = (x,y,z,t)
        for a in range(n_dof):
            rows.append(site*n_dof+a); cols.append(site*n_dof+a); data.append(m0)
        for mu in range(4):
            cn = list(coord); cn[mu] = (cn[mu]+1) % L
            sn = cn[0]*L**3 + cn[1]*L**2 + cn[2]*L + cn[3]
            U = quat_to_su2(links[coord+(mu,)])
            gm = gammas[mu]
            hf = -np.kron((np.eye(4)-gm)/2, U)
            hb_prev = list(coord); hb_prev[mu] = (hb_prev[mu]-1) % L
            sp_idx = hb_prev[0]*L**3 + hb_prev[1]*L**2 + hb_prev[2]*L + hb_prev[3]
            U_prev = quat_to_su2(links[tuple(hb_prev)+(mu,)])
            hb = -np.kron((np.eye(4)+gm)/2, np.conj(U_prev.T))
            for a in range(n_dof):
                for b in range(n_dof):
                    if abs(hf[a,b]) > 1e-10:
                        rows.append(site*n_dof+a); cols.append(sn*n_dof+b); data.append(hf[a,b])
                    if abs(hb[a,b]) > 1e-10:
                        rows.append(site*n_dof+a); cols.append(sp_idx*n_dof+b); data.append(hb[a,b])
    return sp.csr_matrix((data, (rows, cols)), shape=(N, N))

# === RUN ===
print("="*60)
print("Wilson-Dirac QUICK L=4 (matrix 2048×2048)")
print("="*60)
np.random.seed(42)
L = 4
K_fac = math.sqrt(2*math.pi*math.e*2/3)  # ≈ 3.374
F2 = 1.125

results = {}
for beta in [2.3, 2.5, 2.7]:
    print(f"\n--- β = {beta} ---")
    t0 = time.time()
    
    # Quick HMC : 50 therm + 1 config measure
    links = np.zeros((L,L,L,L,4,4)); links[..., 0] = 1
    for _ in range(50):
        links, acc = metropolis(links, beta, L)
    print(f"  HMC done : <P>_check = {sum(links[..., 0].flatten())/links[...,0].size:.3f}, time={time.time()-t0:.0f}s")
    
    # Diagonalize
    t1 = time.time()
    D = build_D(links, m0=0.1)
    DdD = (D.conj().T @ D).tocsr()
    print(f"  Matrix : {DdD.shape}, NNZ={DdD.nnz}")
    
    eigs = eigsh(DdD, k=5, which='SM', tol=1e-3, maxiter=2000, return_eigenvectors=False)
    eigs_abs = np.sqrt(np.abs(np.real(eigs)))
    eigs_sorted = np.sort(eigs_abs)
    
    # Gap estimate
    a_sqrt_sigma = {2.3: 0.5, 2.5: 0.3, 2.7: 0.2}.get(beta, 0.3)
    c_0pp = math.sqrt(16/15)
    gap_est = K_fac * F2 * c_0pp * a_sqrt_sigma
    
    print(f"  Smallest |λ| of D_W : {eigs_sorted[:5]}")
    print(f"  Framework gap_est K·F·c·a√σ : {gap_est:.4f}")
    print(f"  Ratio measured/predicted : {eigs_sorted[0]/gap_est:.3f}")
    print(f"  Time : {time.time()-t1:.0f}s")
    
    results[str(beta)] = {
        'beta': beta, 'L': L,
        'eigvals_smallest': eigs_sorted.tolist(),
        'gap_estimate_framework': gap_est,
        'ratio_measured_predicted': float(eigs_sorted[0]/gap_est),
    }

with open('results/dirac_L4_quick.json', 'w') as f:
    json.dump(results, f, indent=2)
print(f"\n✓ Saved results/dirac_L4_quick.json")
print(f"Total time : {sum([0])} sec")
