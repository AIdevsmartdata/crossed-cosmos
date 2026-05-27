"""FP adjoint L=6 in float32 to fit 16GB GPU + H-QW3 test on SU(3)"""
import os
os.environ["JAX_ENABLE_X64"] = "0"  # Force float32
import numpy as np
import jax
import jax.numpy as jnp
from time import time

print(f"JAX {jax.__version__}, {jax.devices()}, x64={jax.config.jax_enable_x64}")

def build_sun_generators(N):
    gens = []
    for j in range(N):
        for k in range(j+1, N):
            g = np.zeros((N,N), dtype=np.complex64)
            g[j,k] = 0.5j; g[k,j] = 0.5j
            gens.append(g)
    for j in range(N):
        for k in range(j+1, N):
            g = np.zeros((N,N), dtype=np.complex64)
            g[j,k] = 0.5; g[k,j] = -0.5
            gens.append(g)
    for l in range(1, N):
        g = np.zeros((N,N), dtype=np.complex64)
        s = np.sqrt(1.0/(2*l*(l+1)))
        for j in range(l): g[j,j] = 1j*s
        g[l,l] = -1j*l*s
        gens.append(g)
    return gens

def build_fp_laplacian_f32(config, gens, Ls, Lt):
    d_adj = len(gens)
    d_fund = config.shape[-1]
    N_sites = Ls**3 * Lt
    dim = N_sites * d_adj
    sizes = [Ls, Ls, Ls, Lt]

    M = np.zeros((dim, dim), dtype=np.float32)

    site_map = np.zeros((Ls, Ls, Ls, Lt), dtype=int)
    for x0 in range(Ls):
        for x1 in range(Ls):
            for x2 in range(Ls):
                for x3 in range(Lt):
                    site_map[x0,x1,x2,x3] = ((x0*Ls+x1)*Ls+x2)*Lt+x3

    for mu in range(4):
        all_links = config[mu].reshape(-1, d_fund, d_fund).astype(np.complex64)
        n_links = all_links.shape[0]

        all_Ad = np.zeros((n_links, d_adj, d_adj), dtype=np.float32)
        for a in range(d_adj):
            for b in range(d_adj):
                Ud = np.conj(np.swapaxes(all_links, -2, -1))
                TaU = np.einsum('ij,njk->nik', gens[a], all_links)
                TbUd = np.einsum('ij,njk->nik', gens[b], Ud)
                prod = np.einsum('nij,njk->nik', TaU, TbUd)
                all_Ad[:, a, b] = 2.0 * np.einsum('nii->n', prod).real

        idx = 0
        for x0 in range(Ls):
            for x1 in range(Ls):
                for x2 in range(Ls):
                    for x3 in range(Lt):
                        i = site_map[x0,x1,x2,x3]
                        ri = i * d_adj
                        M[ri:ri+d_adj, ri:ri+d_adj] += 2.0 * np.eye(d_adj, dtype=np.float32)

                        c = [x0,x1,x2,x3]
                        c[mu] = (c[mu]+1) % sizes[mu]
                        j = site_map[tuple(c)]
                        rj = j * d_adj
                        M[ri:ri+d_adj, rj:rj+d_adj] -= all_Ad[idx]

                        c2 = [x0,x1,x2,x3]
                        c2[mu] = (c2[mu]-1) % sizes[mu]
                        k = site_map[tuple(c2)]
                        rk = k * d_adj
                        M[ri:ri+d_adj, rk:rk+d_adj] -= all_Ad[site_map[tuple(c2)]].T

                        idx += 1
    return M

# SU(3) L=6
path = "/root/kevinotron/config_su3_L6_beta6.1.npy"
if os.path.exists(path):
    data = np.load(path)
    Ls, Lt = 6, 12
    gens = build_sun_generators(3)
    d_adj = 8
    N_sites = Ls**3 * Lt
    dim = N_sites * d_adj
    mem_gb = dim**2 * 4 / 1e9  # float32 = 4 bytes
    print(f"\nSU(3) L=6 FP adjoint: {dim}x{dim} ({mem_gb:.1f} GB float32)")

    if mem_gb < 15:
        t0 = time()
        M = build_fp_laplacian_f32(data, gens, Ls, Lt)
        print(f"Build: {time()-t0:.1f}s, Sym: {np.max(np.abs(M-M.T)):.1e}")

        print(f"GPU diag (float32)...")
        M_gpu = jnp.array(M)
        t1 = time()
        evals = jnp.linalg.eigvalsh(M_gpu)
        jax.block_until_ready(evals)
        t2 = time()
        print(f"GPU: {t2-t1:.1f}s")

        ev = np.array(evals)
        neg = int(np.sum(ev < -1e-4))
        print(f"λ range: [{ev[0]:.4f}, {ev[-1]:.4f}]")
        print(f"Negative eigenvalues: {neg}")
        print(f"Zero modes: {int(np.sum(np.abs(ev) < 1e-4))}")

        # H-QW3 test
        pred_neg = 3**2 * N_sites / d_adj
        print(f"\nH-QW3: pred neg = |Φ⁺|²×N/d = {3}²×{N_sites}/{d_adj} = {pred_neg:.0f}")
        print(f"Measured: {neg}")
        if neg > 0:
            err = 100*abs(neg - pred_neg)/pred_neg
            print(f"Error: {err:.1f}%")
        else:
            print("No negative evals for SU(3) (as expected from L=4 data)")

        # d_s
        pos = ev[ev > 1e-4]
        t_vals = np.logspace(-2, 2, 50)
        log_P = np.array([np.log(np.sum(np.exp(-t * pos))) for t in t_vals])
        ds = -2 * np.gradient(log_P, np.log(t_vals))
        print(f"d_s: UV={np.mean(ds[5:15]):.2f}, mid={np.mean(ds[15:30]):.2f}, IR={np.mean(ds[30:45]):.2f}")
    else:
        print(f"Still too large ({mem_gb:.1f} GB)")
else:
    print(f"Config not found: {path}")

print("\nDone.")
