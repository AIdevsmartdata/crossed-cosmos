#!/usr/bin/env python3
"""L=4 high-stat λ_min distribution : 1000 configs, statistical precision sur α."""
import os
os.environ.setdefault('JAX_ENABLE_X64', 'True')
import numpy as np
from scipy.sparse import csr_matrix, lil_matrix
from scipy.sparse.linalg import eigsh
import json, time

L = 4
N_CONFIGS = 1000
N_THERM = 200
BETA = 2.4

sigma_pauli = np.array([[[0,1],[1,0]], [[0,-1j],[1j,0]], [[1,0],[0,-1]]]) / 2.0


def site_idx(x,y,z,a,L): return ((z*L+y)*L+x)*3+a


def hb(U, beta, L, n):
    for _ in range(n):
        for x in range(L):
            for y in range(L):
                for z in range(L):
                    for mu in range(3):
                        staple = np.zeros((2,2),dtype=complex)
                        for nu in range(3):
                            if nu==mu: continue
                            x2=(x+(1 if mu==0 else 0))%L; y2=(y+(1 if mu==1 else 0))%L; z2=(z+(1 if mu==2 else 0))%L
                            x3=(x+(1 if nu==0 else 0))%L; y3=(y+(1 if nu==1 else 0))%L; z3=(z+(1 if nu==2 else 0))%L
                            staple += U[x2,y2,z2,nu] @ np.conj(U[x3,y3,z3,mu]).T @ np.conj(U[x,y,z,nu]).T
                        a = np.array([1.0, np.random.randn()/np.sqrt(beta), np.random.randn()/np.sqrt(beta), np.random.randn()/np.sqrt(beta)])
                        a = a/np.linalg.norm(a)
                        Up = np.array([[a[0]+1j*a[3], a[2]+1j*a[1]], [-a[2]+1j*a[1], a[0]-1j*a[3]]])
                        Un = Up @ U[x,y,z,mu]
                        dS = -beta/2*(np.real(np.trace(Un@staple))-np.real(np.trace(U[x,y,z,mu]@staple)))
                        if np.random.rand()<np.exp(-dS): U[x,y,z,mu]=Un
    return U


def build_M(U, L):
    N = L**3*3
    M = lil_matrix((N,N),dtype=np.float64)
    for z in range(L):
        for y in range(L):
            for x in range(L):
                for a in range(3):
                    idx = site_idx(x,y,z,a,L)
                    M[idx,idx]+=6.0
                    for mu,(dx,dy,dz) in enumerate([(1,0,0),(0,1,0),(0,0,1)]):
                        x2=(x+dx)%L;y2=(y+dy)%L;z2=(z+dz)%L
                        x1=(x-dx)%L;y1=(y-dy)%L;z1=(z-dz)%L
                        for bb in range(3):
                            Uadj=np.real(np.trace(sigma_pauli[a]@U[x,y,z,mu]@sigma_pauli[bb]@np.conj(U[x,y,z,mu]).T))
                            U1adj=np.real(np.trace(sigma_pauli[a]@U[x1,y1,z1,mu]@sigma_pauli[bb]@np.conj(U[x1,y1,z1,mu]).T))
                            M[idx,site_idx(x2,y2,z2,bb,L)]-=Uadj
                            M[idx,site_idx(x1,y1,z1,bb,L)]-=U1adj
    return csr_matrix(M)


def main():
    np.random.seed(123)
    print(f"L={L} N={N_CONFIGS} β={BETA}", flush=True)
    U = np.zeros((L,L,L,3,2,2), dtype=complex)
    for x in range(L):
        for y in range(L):
            for z in range(L):
                for mu in range(3):
                    a = np.array([1.0]+[0.2*np.random.randn() for _ in range(3)])
                    a = a/np.linalg.norm(a)
                    U[x,y,z,mu] = np.array([[a[0]+1j*a[3], a[2]+1j*a[1]], [-a[2]+1j*a[1], a[0]-1j*a[3]]])
    t0=time.time()
    U = hb(U, BETA, L, N_THERM)
    print(f"Therm {time.time()-t0:.1f}s", flush=True)
    lmins = []
    l2s = []
    l5s = []
    for cfg in range(N_CONFIGS):
        U = hb(U, BETA, L, 10)
        M = build_M(U, L)
        eigs = eigsh(M, k=5, which='SM', return_eigenvectors=False, tol=1e-7)
        eigs = np.sort(eigs)
        lmins.append(float(eigs[0]))
        l2s.append(float(eigs[1]))
        l5s.append(float(eigs[4]))
        if cfg%100==0:
            print(f"  cfg {cfg}: λ_min={eigs[0]:.4e}, t={time.time()-t0:.1f}s", flush=True)
    lmins=np.array(lmins); l2s=np.array(l2s); l5s=np.array(l5s)
    # CDF fit
    for name, vals in [("λ_min", lmins), ("λ_2", l2s), ("λ_5", l5s)]:
        sl = np.sort(vals)
        F = np.arange(1,len(sl)+1)/len(sl)
        n = len(sl)//2
        p = np.polyfit(np.log(sl[:n]), np.log(F[:n]), 1)
        alpha = p[0]-1
        print(f"  {name} CDF α={alpha:.4f}, d_s={2*(alpha+1):.4f}", flush=True)
    # Save
    out = {'L':L,'N':N_CONFIGS,'BETA':BETA,
           'lambda_mins':lmins.tolist(),'lambda_2':l2s.tolist(),'lambda_5':l5s.tolist(),
           'predictions':{'α=1/6':1/6,'d_s=7/3':7/3}}
    with open('/tmp/L4_highstat.json','w') as f: json.dump(out,f,indent=2)
    print(f"Saved /tmp/L4_highstat.json, total time {time.time()-t0:.1f}s")


if __name__=='__main__': main()
