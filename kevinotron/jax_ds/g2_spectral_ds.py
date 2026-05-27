import os
os.environ["JAX_ENABLE_X64"] = "1"
import jax
import jax.numpy as jnp
import numpy as np
from time import time

print(f"JAX {jax.__version__}, {jax.devices()}")

data = np.load("/root/kevinotron/config_g2_L4_beta10.0.npy")
Ls, Lt, d = 4, 8, 7
N_sites = Ls**3 * Lt
dim = N_sites * d
print(f"G2 config: {data.shape}, building {dim}x{dim} covariant Laplacian")

t0 = time()
M = np.zeros((dim, dim))
links = data

def site_idx(x0,x1,x2,x3):
    return ((x0*Ls + x1)*Ls + x2)*Lt + x3

sizes = [Ls, Ls, Ls, Lt]
for x0 in range(Ls):
    for x1 in range(Ls):
        for x2 in range(Ls):
            for x3 in range(Lt):
                i = site_idx(x0,x1,x2,x3)
                ri = i*d
                M[ri:ri+d, ri:ri+d] += 8.0 * np.eye(d)
                for mu in range(4):
                    coords = [x0,x1,x2,x3]
                    coords[mu] = (coords[mu]+1) % sizes[mu]
                    j = site_idx(*coords)
                    rj = j*d
                    U = links[mu, x0, x1, x2, x3]
                    M[ri:ri+d, rj:rj+d] -= U
                    coords2 = [x0,x1,x2,x3]
                    coords2[mu] = (coords2[mu]-1) % sizes[mu]
                    k = site_idx(*coords2)
                    rk = k*d
                    U_back = links[mu, coords2[0], coords2[1], coords2[2], coords2[3]]
                    M[ri:ri+d, rk:rk+d] -= U_back.T

print(f"Laplacian built in {time()-t0:.1f}s (numpy)")
print(f"Symmetry: |M-M^T|_max = {np.max(np.abs(M - M.T)):.2e}")

print("Diagonalizing on GPU...")
M_gpu = jnp.array(M)
t2 = time()
evals = jnp.linalg.eigvalsh(M_gpu)
jax.block_until_ready(evals)
t3 = time()
print(f"GPU diag: {t3-t2:.2f}s")

evals_np = np.array(evals)
print(f"Eigenvalue range: [{evals_np[0]:.6f}, {evals_np[-1]:.6f}]")
print(f"Zero modes (< 1e-6): {np.sum(np.abs(evals_np) < 1e-6)}")

nonzero = evals_np[evals_np > 1e-6]
t_vals = np.logspace(-2, 2, 50)
log_P = np.array([np.log(np.sum(np.exp(-t * nonzero))) for t in t_vals])
log_t = np.log(t_vals)
ds = -2 * np.gradient(log_P, log_t)

print(f"\nd_s(G2, covariant Laplacian, beta=10.0, L=4):")
ranges = [("UV", 5, 15), ("mid", 15, 30), ("IR", 30, 45)]
for label, a, b in ranges:
    d_mean = np.mean(ds[a:b])
    d_std = np.std(ds[a:b])
    print(f"  {label}: d_s = {d_mean:.3f} +/- {d_std:.3f}")

print(f"\nPrediction d_s = {7/3:.4f} (if 7/3)")
print(f"Standard d_s = 4.0 (4D)")
