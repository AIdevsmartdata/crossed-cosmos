"""sparse_fp.py — Sparse Lanczos FP spectral."""
import os, sys, argparse, json, numpy as np
from scipy.sparse import lil_matrix
from scipy.sparse.linalg import eigsh
from time import time

sys.path.insert(0, os.path.dirname(__file__))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from adjoint import adjoint_rep_batch

def _build_gens(group):
    fast = os.path.join(os.path.dirname(__file__), '..', 'fp_adjoint_fast.py')
    exec(open(fast).read().split('configs = [')[0], globals())
    s = 1.0/np.sqrt(2.0)
    if group == 'g2': return build_g2_generators(), False
    elif group.startswith('su'): return build_sun_generators(int(group[2:])), True
    elif group == 'sp4': return build_sun_generators(4), True
    elif group == 'so7':
        g = []
        for i in range(7):
            for j in range(i+1,7):
                m = np.zeros((7,7)); m[i,j]=s; m[j,i]=-s; g.append(m)
        return np.array(g), False
    elif group == 'f4':
        return np.load(os.path.join(os.path.dirname(__file__), '..', 'f4_generators_26x26.npy')), False
    raise ValueError(group)

def build_fp_sparse(config, gens):
    Ls=config.shape[1]; Lt=config.shape[4]; da=len(gens)
    N=Ls**3*Lt; dim=N*da; sizes=np.array([Ls,Ls,Ls,Lt])
    M = lil_matrix((dim, dim), dtype=np.float64)
    sm = np.zeros((Ls,Ls,Ls,Lt), dtype=int)
    for a in range(Ls):
        for b in range(Ls):
            for c in range(Ls):
                for d in range(Lt):
                    sm[a,b,c,d]=((a*Ls+b)*Ls+c)*Lt+d
    for mu in range(4):
        print(f'  mu={mu}', flush=True)
        lnk = config[mu].reshape(-1, config.shape[-2], config.shape[-1])
        aAd = adjoint_rep_batch(lnk, gens)
        idx = 0
        for a in range(Ls):
            for b in range(Ls):
                for c in range(Ls):
                    for d in range(Lt):
                        i=sm[a,b,c,d]; ri=i*da
                        for x in range(da): M[ri+x,ri+x] += 2.0
                        co=[a,b,c,d]; co[mu]=(co[mu]+1)%sizes[mu]; j=sm[tuple(co)]; rj=j*da
                        for x in range(da):
                            for y in range(da):
                                v=aAd[idx,x,y]
                                if abs(v)>1e-15: M[ri+x,rj+y] -= v
                        c2=[a,b,c,d]; c2[mu]=(c2[mu]-1)%sizes[mu]; k=sm[tuple(c2)]; rk=k*da
                        bk=sm[tuple(c2)]
                        for x in range(da):
                            for y in range(da):
                                v=aAd[bk,y,x]
                                if abs(v)>1e-15: M[ri+x,rk+y] -= v
                        idx += 1
    return M.tocsr()

if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument('--config', required=True)
    p.add_argument('--group', required=True)
    p.add_argument('--k', type=int, default=200)
    a = p.parse_args()
    gens, _ = _build_gens(a.group)
    data = np.load(a.config)
    dim = data.shape[1]**3 * data.shape[4] * len(gens)
    print(f'{a.group.upper()} Sparse FP: dim={dim}', flush=True)
    t0=time(); M=build_fp_sparse(data, gens); tb=time()-t0
    print(f'Build: {tb:.1f}s, nnz={M.nnz} ({100*M.nnz/dim**2:.1f}%)', flush=True)
    print(f'Lanczos k={a.k}...', flush=True)
    t0=time()
    evals=eigsh(M, k=min(a.k, dim-2), sigma=0.0, which='SA', return_eigenvectors=False)
    evals=np.sort(evals); ts=time()-t0
    nn=int(np.sum(evals<-1e-6))
    gap=float(evals[evals>1e-6][0]) if np.any(evals>1e-6) else 0.0
    print(f'Done: {ts:.1f}s, n_neg={nn}, gap={gap:.6f}, range=[{evals[0]:.4f},{evals[-1]:.4f}]', flush=True)
    out=a.config.replace('.npy','_sfp.json')
    json.dump({'n_neg':nn,'gap':gap,'dim':dim,'k':len(evals),'build':tb,'solve':ts,
               'lam_min':float(evals[0]),'lam_max':float(evals[-1])}, open(out,'w'), indent=2)
    print(f'Saved {out}', flush=True)
