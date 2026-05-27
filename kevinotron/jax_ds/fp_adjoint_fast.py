"""FP adjoint d_s — FAST version: vectorized build + GPU diag"""
import os
os.environ["JAX_ENABLE_X64"] = "1"
import numpy as np
import jax
import jax.numpy as jnp
from time import time
import sys

print(f"JAX {jax.__version__}, {jax.devices()}")

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
            if norm > 1e-10: g *= np.sqrt(2.0)/norm
            gens.append(g)
    return np.array(gens)

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
    return np.array(gens)

def adjoint_rep_batch_real(links_mu, gens):
    """Vectorized Ad(U) for all links in one direction. Real groups."""
    d_adj = len(gens)
    n_links = links_mu.shape[0]
    Ad = np.zeros((n_links, d_adj, d_adj))
    for a in range(d_adj):
        for b in range(d_adj):
            TaU = np.einsum('ij,njk->nik', gens[a], links_mu)
            TaUTbUt = np.einsum('nij,jk,nlk->ni', TaU, gens[b], links_mu)
            Ad[:, a, b] = np.einsum('ni->n', TaUTbUt)
    return Ad

def adjoint_rep_batch_complex(links_mu, gens):
    """Vectorized Ad(U) for all links. Complex groups."""
    d_adj = len(gens)
    n_links = links_mu.shape[0]
    Ad = np.zeros((n_links, d_adj, d_adj))
    for a in range(d_adj):
        for b in range(d_adj):
            TaU = np.einsum('ij,njk->nik', gens[a], links_mu)
            Ud = np.conj(np.swapaxes(links_mu, -2, -1))
            TbUd = np.einsum('ij,njk->nik', gens[b], Ud)
            prod = np.einsum('nij,njk->nik', TaU, TbUd)
            Ad[:, a, b] = 2.0 * np.einsum('nii->n', prod).real
    return Ad

def build_fp_laplacian_fast(config, gens, is_complex):
    """Build FP Laplacian — vectorized over sites."""
    Ls = config.shape[1]
    Lt = config.shape[4]
    d_adj = len(gens)
    N_sites = Ls**3 * Lt
    dim = N_sites * d_adj
    sizes = np.array([Ls, Ls, Ls, Lt])

    M = np.zeros((dim, dim))

    site_map = np.zeros((Ls, Ls, Ls, Lt), dtype=int)
    for x0 in range(Ls):
        for x1 in range(Ls):
            for x2 in range(Ls):
                for x3 in range(Lt):
                    site_map[x0,x1,x2,x3] = ((x0*Ls+x1)*Ls+x2)*Lt+x3

    adj_func = adjoint_rep_batch_complex if is_complex else adjoint_rep_batch_real

    for mu in range(4):
        all_links = config[mu].reshape(-1, config.shape[-2], config.shape[-1])
        all_Ad = adj_func(all_links, gens)

        idx = 0
        for x0 in range(Ls):
            for x1 in range(Ls):
                for x2 in range(Ls):
                    for x3 in range(Lt):
                        i = site_map[x0,x1,x2,x3]
                        ri = i * d_adj

                        M[ri:ri+d_adj, ri:ri+d_adj] += 2.0 * np.eye(d_adj)

                        coords = [x0,x1,x2,x3]
                        coords[mu] = (coords[mu]+1) % sizes[mu]
                        j = site_map[tuple(coords)]
                        rj = j * d_adj
                        M[ri:ri+d_adj, rj:rj+d_adj] -= all_Ad[idx]

                        coords2 = [x0,x1,x2,x3]
                        coords2[mu] = (coords2[mu]-1) % sizes[mu]
                        k = site_map[tuple(coords2)]
                        rk = k * d_adj
                        back_idx = site_map[tuple(coords2)]
                        M[ri:ri+d_adj, rk:rk+d_adj] -= all_Ad[back_idx].T

                        idx += 1

    return M

def spectral_dimension(evals_np):
    pos = evals_np[evals_np > 1e-6]
    if len(pos) == 0:
        return {"UV": (0,0), "mid": (0,0), "IR": (0,0)}
    t_vals = np.logspace(-2, 2, 50)
    log_P = np.array([np.log(np.sum(np.exp(-t * pos))) for t in t_vals])
    log_t = np.log(t_vals)
    ds = -2 * np.gradient(log_P, log_t)
    return {
        "UV": (np.mean(ds[5:15]), np.std(ds[5:15])),
        "mid": (np.mean(ds[15:30]), np.std(ds[15:30])),
        "IR": (np.mean(ds[30:45]), np.std(ds[30:45])),
    }

configs = [
    ("SU(2)", "/root/kevinotron/config_su2_L4_beta2.5.npy", True, 2, 3),
    ("SU(3)", "/root/kevinotron/config_su3_L4_beta6.1.npy", True, 3, 8),
    ("Sp(4)", "/root/kevinotron/config_sp4_L4_beta8.0.npy", True, 4, 10),
    ("G2", "/root/kevinotron/config_g2_L4_beta10.0.npy", False, 7, 14),
]

for name, path, is_complex, d_fund, d_adj_expected in configs:
    if not os.path.exists(path):
        print(f"\n{name}: {path} not found, skip")
        continue

    data = np.load(path)
    Ls, Lt = data.shape[1], data.shape[4]
    dim = Ls**3 * Lt * d_adj_expected
    mem_gb = dim**2 * 8 / 1e9

    print(f"\n{'='*60}")
    print(f"{name}: FP adjoint {dim}×{dim} ({mem_gb:.2f} GB)")

    if mem_gb > 14:
        print(f"  TOO LARGE for 16GB GPU, skip")
        continue

    if is_complex:
        gens = build_sun_generators(d_fund)
    else:
        gens = build_g2_generators()
    print(f"  {len(gens)} generators")

    t0 = time()
    M = build_fp_laplacian_fast(data, gens, is_complex)
    t1 = time()
    print(f"  Build: {t1-t0:.1f}s")
    print(f"  Symmetry: |M-M^T| = {np.max(np.abs(M-M.T)):.2e}")

    print(f"  GPU diag...")
    M_gpu = jnp.array(M)
    t2 = time()
    evals = jnp.linalg.eigvalsh(M_gpu)
    jax.block_until_ready(evals)
    t3 = time()
    evals_np = np.array(evals)
    print(f"  GPU diag: {t3-t2:.2f}s")
    print(f"  λ range: [{evals_np[0]:.4f}, {evals_np[-1]:.4f}]")
    print(f"  Zero modes: {np.sum(np.abs(evals_np) < 1e-6)}")
    print(f"  Negative: {np.sum(evals_np < -1e-6)}")
    print(f"  λ_min(positive): {evals_np[evals_np > 1e-6][0]:.6f}" if np.any(evals_np > 1e-6) else "  No positive evals!")

    ds = spectral_dimension(evals_np)
    print(f"  d_s({name} FP adj):")
    for label, (m, s) in ds.items():
        print(f"    {label}: {m:.3f} ± {s:.3f}")

print(f"\nPrediction: d_s = 7/3 = {7/3:.4f}")
