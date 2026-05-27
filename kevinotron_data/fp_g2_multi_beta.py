"""H_NEW3: FP adjoint neg evals G₂ multi-β — Gribov copies vs coupling"""
import os
os.environ["JAX_ENABLE_X64"] = "1"
import numpy as np
import jax
import jax.numpy as jnp
from time import time
import json

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

def adjoint_rep_batch_real(links_mu, gens):
    d_adj = len(gens)
    n_links = links_mu.shape[0]
    Ad = np.zeros((n_links, d_adj, d_adj))
    for a in range(d_adj):
        for b in range(d_adj):
            TaU = np.einsum('ij,njk->nik', gens[a], links_mu)
            TaUTbUt = np.einsum('nij,jk,nlk->ni', TaU, gens[b], links_mu)
            Ad[:, a, b] = np.einsum('ni->n', TaUTbUt)
    return Ad

def build_fp_laplacian_fast(config, gens):
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
    for mu in range(4):
        all_links = config[mu].reshape(-1, config.shape[-2], config.shape[-1])
        all_Ad = adjoint_rep_batch_real(all_links, gens)
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
                        M[ri:ri+d_adj, rk:rk+d_adj] -= all_Ad[site_map[tuple(coords2)]].T
                        idx += 1
    return M

def spectral_dimension(evals_np):
    pos = evals_np[evals_np > 1e-6]
    if len(pos) == 0:
        return 0.0, 0.0
    t_vals = np.logspace(-2, 2, 50)
    log_P = np.array([np.log(np.sum(np.exp(-t * pos))) for t in t_vals])
    log_t = np.log(t_vals)
    ds = -2 * np.gradient(log_P, log_t)
    return float(np.mean(ds[15:30])), float(np.std(ds[15:30]))

gens = build_g2_generators()
print(f"G₂ generators: {len(gens)}")

betas = [9.6, 9.8, 10.0, 10.2, 10.4]
results = []

for beta in betas:
    path = f"/root/kevinotron/config_g2_L4_beta{beta}.npy"
    if not os.path.exists(path):
        print(f"\nβ={beta}: config not found, skip")
        continue

    data = np.load(path)
    Ls, Lt = data.shape[1], data.shape[4]
    dim = Ls**3 * Lt * 14  # G₂ adjoint = 14
    print(f"\n{'='*60}")
    print(f"G₂ β={beta}: FP adjoint {dim}×{dim}")

    t0 = time()
    M = build_fp_laplacian_fast(data, gens)
    t_build = time() - t0
    print(f"  Build: {t_build:.1f}s, |M-M^T|={np.max(np.abs(M-M.T)):.2e}")

    M_gpu = jnp.array(M)
    t0 = time()
    evals = jnp.linalg.eigvalsh(M_gpu)
    jax.block_until_ready(evals)
    t_diag = time() - t0
    evals_np = np.array(evals)

    n_neg = int(np.sum(evals_np < -1e-6))
    n_zero = int(np.sum(np.abs(evals_np) < 1e-6))
    lam_min = float(evals_np[0])
    lam_max = float(evals_np[-1])
    gap = float(evals_np[evals_np > 1e-6][0]) if np.any(evals_np > 1e-6) else 0.0
    ds_mid, ds_std = spectral_dimension(evals_np)

    neg_evals_list = sorted(evals_np[evals_np < -1e-6])[:20]

    print(f"  GPU diag: {t_diag:.2f}s")
    print(f"  λ range: [{lam_min:.4f}, {lam_max:.4f}]")
    print(f"  Negative evals: {n_neg}")
    print(f"  Zero modes: {n_zero}")
    print(f"  Gap (λ_min pos): {gap:.6f}")
    print(f"  d_s(mid): {ds_mid:.3f} ± {ds_std:.3f}")
    if n_neg > 0:
        print(f"  Bottom 10 neg: {[f'{x:.4f}' for x in neg_evals_list[:10]]}")

    results.append({
        "beta": beta,
        "dim": dim,
        "n_neg": n_neg,
        "n_zero": n_zero,
        "lam_min": lam_min,
        "lam_max": lam_max,
        "gap": gap,
        "ds_mid": ds_mid,
        "ds_std": ds_std,
        "build_time": t_build,
        "diag_time": t_diag,
        "bottom_neg": [float(x) for x in neg_evals_list[:20]],
    })

out_path = "/root/kevinotron/h_new3_g2_fp_multi_beta.json"
with open(out_path, 'w') as f:
    json.dump(results, f, indent=2)
print(f"\n{'='*60}")
print(f"Results saved to {out_path}")
print(f"\nSUMMARY:")
print(f"{'β':>6} {'n_neg':>8} {'λ_min':>10} {'gap':>10} {'d_s':>8}")
for r in results:
    print(f"{r['beta']:6.1f} {r['n_neg']:8d} {r['lam_min']:10.4f} {r['gap']:10.6f} {r['ds_mid']:8.3f}")
