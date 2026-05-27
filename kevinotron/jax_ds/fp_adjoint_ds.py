"""C1: FP adjoint d_s for SU(2), SU(3), G₂ on GPU"""
import os
os.environ["JAX_ENABLE_X64"] = "1"
import numpy as np
from time import time

# Build adjoint representation Ad(U) from fundamental links
# Ad(U)_{ab} = 2 Re Tr(T_a U T_b U†) for complex groups
# Ad(U)_{ab} = Tr(T_a U T_b U^T) for real groups (G₂)

def build_sun_generators(N):
    gens = []
    for j in range(N):
        for k in range(j+1, N):
            g = np.zeros((N,N), dtype=np.complex128)
            g[j,k] = 0.5j; g[k,j] = 0.5j
            gens.append(g)
    for j in range(N):
        for k in range(j+1, N):
            g = np.zeros((N,N), dtype=np.complex128)
            g[j,k] = 0.5; g[k,j] = -0.5
            gens.append(g)
    for l in range(1, N):
        g = np.zeros((N,N), dtype=np.complex128)
        s = np.sqrt(1.0/(2*l*(l+1)))
        for j in range(l): g[j,j] = 1j*s
        g[l,l] = -1j*l*s
        gens.append(g)
    return gens

def build_g2_generators():
    signed_triples = [(0,1,2,1.0),(0,3,4,1.0),(0,5,6,1.0),(1,3,5,1.0),
                      (1,4,6,-1.0),(2,3,6,-1.0),(2,4,5,-1.0)]
    f = np.zeros((7,7,7))
    for i,j,k,s in signed_triples:
        f[i,j,k]=s; f[j,k,i]=s; f[k,i,j]=s
        f[j,i,k]=-s; f[k,j,i]=-s; f[i,k,j]=-s
    triples = [(i,j,k) for i in range(7) for j in range(i+1,7) for k in range(j+1,7)]
    pairs = [(p,q) for p in range(7) for q in range(p+1,7)]
    M = np.zeros((35,21))
    for ti,(i,j,k) in enumerate(triples):
        for gi,(p,q) in enumerate(pairs):
            v = 0.0
            if i==p: v+=f[q,j,k]
            if i==q: v-=f[p,j,k]
            if j==p: v+=f[i,q,k]
            if j==q: v-=f[i,p,k]
            if k==p: v+=f[i,j,q]
            if k==q: v-=f[i,j,p]
            M[ti,gi]=v
    _,S,Vt = np.linalg.svd(M, full_matrices=True)
    gens = []
    for r in range(21):
        if (S[r] < 1e-10) if r < len(S) else True:
            g = np.zeros((7,7))
            for idx,(p,q) in enumerate(pairs):
                g[p,q]=Vt[r,idx]; g[q,p]=-Vt[r,idx]
            norm = np.sqrt(max(-np.sum(g*g), 0))
            if norm > 1e-10:
                g *= np.sqrt(2.0)/norm
            gens.append(g)
    return gens

def adjoint_rep_complex(U, gens):
    """Ad(U)_{ab} = 2 Re Tr(T_a U T_b U†)"""
    d_adj = len(gens)
    Ad = np.zeros((d_adj, d_adj))
    Ud = U.conj().T
    for a in range(d_adj):
        for b in range(d_adj):
            Ad[a,b] = 2 * np.trace(gens[a] @ U @ gens[b] @ Ud).real
    return Ad

def adjoint_rep_real(U, gens):
    """Ad(U)_{ab} = Tr(T_a U T_b U^T) for real groups"""
    d_adj = len(gens)
    Ad = np.zeros((d_adj, d_adj))
    for a in range(d_adj):
        for b in range(d_adj):
            Ad[a,b] = np.trace(gens[a] @ U @ gens[b] @ U.T)
    return Ad

def build_fp_laplacian(config, gens, is_complex, Ls, Lt):
    """Build Faddeev-Popov Laplacian in adjoint representation."""
    d_adj = len(gens)
    N_sites = Ls**3 * Lt
    dim = N_sites * d_adj
    M = np.zeros((dim, dim))
    sizes = [Ls, Ls, Ls, Lt]

    adj_func = adjoint_rep_complex if is_complex else adjoint_rep_real

    def site_idx(x0,x1,x2,x3):
        return ((x0*Ls + x1)*Ls + x2)*Lt + x3

    for x0 in range(Ls):
        for x1 in range(Ls):
            for x2 in range(Ls):
                for x3 in range(Lt):
                    i = site_idx(x0,x1,x2,x3)
                    ri = i * d_adj
                    M[ri:ri+d_adj, ri:ri+d_adj] += 8.0 * np.eye(d_adj)

                    for mu in range(4):
                        U = config[mu, x0, x1, x2, x3]
                        Ad_U = adj_func(U, gens)

                        coords = [x0,x1,x2,x3]
                        coords[mu] = (coords[mu]+1) % sizes[mu]
                        j = site_idx(*coords)
                        rj = j * d_adj
                        M[ri:ri+d_adj, rj:rj+d_adj] -= Ad_U

                        coords2 = [x0,x1,x2,x3]
                        coords2[mu] = (coords2[mu]-1) % sizes[mu]
                        k = site_idx(*coords2)
                        rk = k * d_adj
                        U_back = config[mu, coords2[0], coords2[1], coords2[2], coords2[3]]
                        Ad_back = adj_func(U_back, gens)
                        M[ri:ri+d_adj, rk:rk+d_adj] -= Ad_back.T

    return M

def spectral_dimension(evals_np):
    nonzero = evals_np[evals_np > 1e-6]
    t_vals = np.logspace(-2, 2, 50)
    log_P = np.array([np.log(np.sum(np.exp(-t * nonzero))) for t in t_vals])
    log_t = np.log(t_vals)
    ds = -2 * np.gradient(log_P, log_t)
    ranges = [("UV", 5, 15), ("mid", 15, 30), ("IR", 30, 45)]
    results = {}
    for label, a, b in ranges:
        results[label] = (np.mean(ds[a:b]), np.std(ds[a:b]))
    return results

# Process each config
configs = [
    ("SU(2)", "/root/kevinotron/config_su2_L4_beta2.5.npy", True, 2, 3),
    ("G₂", "/root/kevinotron/config_g2_L4_beta10.0.npy", False, 7, 14),
]

for name, path, is_complex, d_fund, d_adj in configs:
    if not os.path.exists(path):
        print(f"{name}: config not found at {path}")
        continue

    data = np.load(path)
    Ls = data.shape[1]
    Lt = data.shape[4]
    N_sites = Ls**3 * Lt
    dim = N_sites * d_adj

    print(f"\n{'='*60}")
    print(f"{name}: FP adjoint Laplacian {dim}×{dim}")
    print(f"  Config: {data.shape}, Ls={Ls}, Lt={Lt}")
    print(f"  d_adj={d_adj}, N_sites={N_sites}")
    mem_gb = dim**2 * 8 / 1e9
    print(f"  Memory: {mem_gb:.2f} GB", end="")

    if mem_gb > 14:
        print(" — TOO LARGE for GPU (16GB), skipping")
        continue
    print(" — fits GPU")

    if is_complex:
        gens = build_sun_generators(d_fund)
    else:
        gens = build_g2_generators()

    print(f"  Generators: {len(gens)}")

    t0 = time()
    M = build_fp_laplacian(data, gens, is_complex, Ls, Lt)
    t1 = time()
    print(f"  FP Laplacian built in {t1-t0:.1f}s")
    print(f"  Symmetry: |M-M^T|_max = {np.max(np.abs(M - M.T)):.2e}")

    # Diagonalize
    print(f"  Diagonalizing {dim}×{dim}...")
    t2 = time()
    evals = np.linalg.eigvalsh(M)
    t3 = time()
    print(f"  Diag done in {t3-t2:.1f}s")
    print(f"  Eigenvalue range: [{evals[0]:.4f}, {evals[-1]:.4f}]")
    print(f"  Zero modes (<1e-6): {np.sum(np.abs(evals) < 1e-6)}")
    print(f"  Negative eigenvalues: {np.sum(evals < -1e-6)}")

    ds_results = spectral_dimension(evals)
    print(f"\n  d_s({name}, FP adjoint):")
    for label, (mean, std) in ds_results.items():
        print(f"    {label}: d_s = {mean:.3f} ± {std:.3f}")

    print(f"\n  Prediction d_s = 7/3 = {7/3:.4f}")
    print(f"  Standard d_s = 4.0")
