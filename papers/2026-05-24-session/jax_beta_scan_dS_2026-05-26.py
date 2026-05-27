#!/usr/bin/env python3
"""β-scan test : α = 1/6 universel ? Run λ_min distribution à β=2.0, 2.4, 2.8.

Si α=1/6 ± 0.02 indep de β → universalité confirmée, d_s = 7/3 robust.
"""
import os
os.environ.setdefault('JAX_ENABLE_X64', 'True')
import numpy as np
from scipy.sparse import csr_matrix, lil_matrix
from scipy.sparse.linalg import eigsh
import json, time

L = 6  # small to be fast
N_CONFIGS = 80
N_THERM = 300
BETAS = [2.0, 2.4, 2.8]

sigma_pauli = np.array([
    [[0,1],[1,0]], [[0,-1j],[1j,0]], [[1,0],[0,-1]],
]) / 2.0


def site_idx(x, y, z, a, L): return ((z*L+y)*L+x)*3+a


def hb_su2(U, beta, L, n_sweeps):
    for _ in range(n_sweeps):
        for x in range(L):
            for y in range(L):
                for z in range(L):
                    for mu in range(3):
                        staple = np.zeros((2,2), dtype=complex)
                        for nu in range(3):
                            if nu==mu: continue
                            x2=(x+(1 if mu==0 else 0))%L; y2=(y+(1 if mu==1 else 0))%L; z2=(z+(1 if mu==2 else 0))%L
                            x3=(x+(1 if nu==0 else 0))%L; y3=(y+(1 if nu==1 else 0))%L; z3=(z+(1 if nu==2 else 0))%L
                            staple += U[x2,y2,z2,nu] @ np.conj(U[x3,y3,z3,mu]).T @ np.conj(U[x,y,z,nu]).T
                        a = np.array([1.0, np.random.randn()/np.sqrt(beta), np.random.randn()/np.sqrt(beta), np.random.randn()/np.sqrt(beta)])
                        a = a/np.linalg.norm(a)
                        Up = np.array([[a[0]+1j*a[3], a[2]+1j*a[1]], [-a[2]+1j*a[1], a[0]-1j*a[3]]])
                        Un = Up @ U[x,y,z,mu]
                        dS = -beta/2 * (np.real(np.trace(Un@staple)) - np.real(np.trace(U[x,y,z,mu]@staple)))
                        if np.random.rand() < np.exp(-dS): U[x,y,z,mu] = Un
    return U


def build_M_FP(U, L):
    N = L**3*3
    M = lil_matrix((N,N), dtype=np.float64)
    for z in range(L):
        for y in range(L):
            for x in range(L):
                for a in range(3):
                    idx = site_idx(x,y,z,a,L)
                    M[idx,idx] += 6.0
                    for mu,(dx,dy,dz) in enumerate([(1,0,0),(0,1,0),(0,0,1)]):
                        x2=(x+dx)%L; y2=(y+dy)%L; z2=(z+dz)%L
                        x1=(x-dx)%L; y1=(y-dy)%L; z1=(z-dz)%L
                        for bb in range(3):
                            Uadj = np.real(np.trace(sigma_pauli[a]@U[x,y,z,mu]@sigma_pauli[bb]@np.conj(U[x,y,z,mu]).T))
                            U1adj = np.real(np.trace(sigma_pauli[a]@U[x1,y1,z1,mu]@sigma_pauli[bb]@np.conj(U[x1,y1,z1,mu]).T))
                            M[idx,site_idx(x2,y2,z2,bb,L)] -= Uadj
                            M[idx,site_idx(x1,y1,z1,bb,L)] -= U1adj
    return csr_matrix(M)


def main():
    results = {}
    for beta in BETAS:
        np.random.seed(int(beta*1000)+42)
        print(f"\n=== β = {beta} ===", flush=True)
        U = np.zeros((L,L,L,3,2,2), dtype=complex)
        for x in range(L):
            for y in range(L):
                for z in range(L):
                    for mu in range(3):
                        a = np.array([1.0]+[0.2*np.random.randn() for _ in range(3)])
                        a = a/np.linalg.norm(a)
                        U[x,y,z,mu] = np.array([[a[0]+1j*a[3], a[2]+1j*a[1]], [-a[2]+1j*a[1], a[0]-1j*a[3]]])
        t0=time.time()
        U = hb_su2(U, beta, L, 500)
        print(f"  Therm done {time.time()-t0:.1f}s", flush=True)
        lmins = []
        for cfg in range(N_CONFIGS):
            U = hb_su2(U, beta, L, 20)
            M = build_M_FP(U, L)
            eigs = eigsh(M, k=3, which='SM', return_eigenvectors=False, tol=1e-7)
            lmins.append(float(np.sort(eigs)[0]))
            if cfg % 20 == 0:
                print(f"  cfg {cfg}: λ_min={lmins[-1]:.4e}, t={time.time()-t0:.1f}s", flush=True)
        lmins = np.array(lmins)
        # CDF fit α
        sorted_lmin = np.sort(lmins)
        F = np.arange(1, len(sorted_lmin)+1) / len(sorted_lmin)
        n_use = len(sorted_lmin) // 2
        log_l = np.log(sorted_lmin[:n_use])
        log_F = np.log(F[:n_use])
        p = np.polyfit(log_l, log_F, 1)
        alpha = p[0] - 1
        d_s = 2*(alpha+1)
        print(f"\n  β={beta}: α_CDF={alpha:.4f} (predict 1/6=0.1667), d_s={d_s:.4f} (predict 7/3)", flush=True)
        results[f"beta_{beta}"] = {'beta':beta, 'N_configs':len(lmins), 'alpha':float(alpha), 'd_s':float(d_s), 'lambda_mins':lmins.tolist()}

    out = {'L':L, 'N_CONFIGS':N_CONFIGS, 'BETAS':BETAS, 'results':results, 'predictions':{'α':1/6, 'd_s':7/3}}
    with open('/tmp/beta_scan_dS.json','w') as f: json.dump(out, f, indent=2)
    print(f"\n=== SUMMARY ===", flush=True)
    print(f"{'β':>6s} {'α':>10s} {'d_s':>10s} {'σ from 1/6':>12s}")
    for r in results.values():
        sigma = (r['alpha'] - 1/6) / 0.05
        print(f"{r['beta']:>6.2f} {r['alpha']:>10.4f} {r['d_s']:>10.4f} {sigma:>+12.2f}", flush=True)


if __name__=='__main__': main()
