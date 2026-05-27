#!/usr/bin/env python3
"""
KEVINOTRON — JAX/GPU Spectral Analysis Module
===============================================

Given a thermalized gauge field configuration (from Rust .npy dump),
constructs and diagonalizes:

1. Covariant Laplacian (fundamental rep)
     Delta_ij = sum_mu [ 2 delta_xy delta_ij
                       - U_mu(x)_ij delta_{y,x+mu}
                       - U_mu(y)^dag_ij delta_{y,x-mu} ]

2. Faddeev-Popov operator (adjoint rep)
     M_FP^{ab}(x,y) = sum_mu [ 2 delta_xy delta_ab
                              - Ad(U_mu(x))^{ab} delta_{y,x+mu}
                              - Ad(U_mu(y))^{ab,dag} delta_{y,x-mu} ]

3. Spectral dimension d_s from heat kernel
     P(t) = sum_k exp(-t * lambda_k)
     d_s(t) = -2 d(ln P) / d(ln t)

Memory: dense matrix (N_sites * d)^2 * 8 bytes (f64) or *16 (c128).
See ARCHITECTURE.md for the VRAM budget table.

Author: Kevin Remondiere (ORCID 0009-0008-2443-7166)
"""

import os
os.environ['JAX_ENABLE_X64'] = '1'

import jax
import jax.numpy as jnp
import numpy as np
import argparse
import time
import sys

print(f"JAX {jax.__version__}, x64={jax.config.jax_enable_x64}, devices: {jax.devices()}", file=sys.stderr)


# ============================================================
# ADJOINT REPRESENTATION
# ============================================================

def adjoint_su_n(U, N):
    """Compute Ad(U) for SU(N): dim_adj = N^2-1.

    Ad(U)^{ab} = 2 Tr(T_a U T_b U^dag)

    where T_a are the N^2-1 generators (anti-Hermitian, Tr(T_a T_b) = -delta_ab/2).

    For numerical stability, compute in complex128.

    Returns: (N^2-1, N^2-1) real matrix.
    """
    dim_adj = N * N - 1
    gens = build_sun_generators_jax(N)  # (dim_adj, N, N) complex128

    Ad = jnp.zeros((dim_adj, dim_adj))
    U_dag = U.conj().T

    for a in range(dim_adj):
        for b in range(dim_adj):
            # Ad(U)_ab = -2 Tr(T_a U T_b U^dag)
            # With our convention T = i*lambda/2 (anti-Hermitian),
            # Tr(T_a T_b) = -1/2 delta_ab
            # So Ad(U)_ab = -2 Tr(T_a U T_b U^dag)
            val = -2.0 * jnp.trace(gens[a] @ U @ gens[b] @ U_dag).real
            Ad = Ad.at[a, b].set(val)

    return Ad


def adjoint_g2(U):
    """Compute Ad(U) for G2: dim_adj = 14.

    For G2 in 7-dim fundamental, the adjoint acts on g2 (14-dim).
    Ad(U)^{ab} = Tr(T_a U T_b U^T) * normalization.

    With our convention (T_a antisymmetric, Tr(T_a T_b) = -delta_ab):
    Ad(U)_ab = -Tr(T_a U T_b U^T)

    Returns: (14, 14) real matrix.
    """
    gens = build_g2_generators_jax()  # (14, 7, 7) real
    dim_adj = 14

    Ad = jnp.zeros((dim_adj, dim_adj))
    U_T = U.T

    for a in range(dim_adj):
        for b in range(dim_adj):
            val = -jnp.trace(gens[a] @ U @ gens[b] @ U_T)
            Ad = Ad.at[a, b].set(val)

    return Ad


# ============================================================
# GENERATORS (JAX versions)
# ============================================================

def build_sun_generators_jax(N):
    """Build N^2-1 anti-Hermitian generators of su(N)."""
    gens = []
    # Symmetric off-diagonal
    for j in range(N):
        for k in range(j+1, N):
            g = np.zeros((N, N), dtype=np.complex128)
            g[j, k] = 0.5j
            g[k, j] = 0.5j
            gens.append(g)
    # Anti-symmetric off-diagonal
    for j in range(N):
        for k in range(j+1, N):
            g = np.zeros((N, N), dtype=np.complex128)
            g[j, k] = 0.5
            g[k, j] = -0.5
            gens.append(g)
    # Diagonal
    for l in range(1, N):
        g = np.zeros((N, N), dtype=np.complex128)
        s = np.sqrt(1.0 / (2 * l * (l + 1)))
        for j in range(l):
            g[j, j] = 1j * s
        g[l, l] = -1j * l * s
        gens.append(g)
    return jnp.array(gens)


def build_g2_generators_jax():
    """Build 14 generators of g2 subset of so(7)."""
    signed_triples = [
        (0,1,2,1.0),(0,3,4,1.0),(0,5,6,1.0),(1,3,5,1.0),
        (1,4,6,-1.0),(2,3,6,-1.0),(2,4,5,-1.0),
    ]
    f = np.zeros((7, 7, 7))
    for i, j, k, s in signed_triples:
        f[i,j,k]=s; f[j,k,i]=s; f[k,i,j]=s
        f[j,i,k]=-s; f[k,j,i]=-s; f[i,k,j]=-s

    triples = [(i,j,k) for i in range(7) for j in range(i+1,7) for k in range(j+1,7)]
    pairs = [(p,q) for p in range(7) for q in range(p+1,7)]

    M = np.zeros((35, 21))
    for ti, (i,j,k) in enumerate(triples):
        for gi, (p,q) in enumerate(pairs):
            v = 0.0
            if i==p: v += f[q,j,k]
            if i==q: v -= f[p,j,k]
            if j==p: v += f[i,q,k]
            if j==q: v -= f[i,p,k]
            if k==p: v += f[i,j,q]
            if k==q: v -= f[i,j,p]
            M[ti, gi] = v

    _, S, Vt = np.linalg.svd(M, full_matrices=True)
    gens = []
    for r in range(21):
        if (S[r] < 1e-10) if r < len(S) else True:
            g = np.zeros((7, 7))
            for idx, (p, q) in enumerate(pairs):
                g[p, q] = Vt[r, idx]
                g[q, p] = -Vt[r, idx]
            gsq = np.sum(g * g)
            norm = np.sqrt(max(-gsq, 0.0))
            if norm > 1e-10:
                g *= np.sqrt(2.0) / norm
            gens.append(g)
    assert len(gens) == 14
    return jnp.array(gens)


# ============================================================
# COVARIANT LAPLACIAN (fundamental rep)
# ============================================================

def build_covariant_laplacian_fund(links, group, Ls, Lt):
    """Build the covariant Laplacian in the fundamental representation.

    links: array of shape (4, Ls, Ls, Ls, Lt, d, d)
    Returns: dense Hermitian matrix of shape (N_sites*d, N_sites*d)

    Delta_{(x,i),(y,j)} = sum_mu [ 2 delta_xy delta_ij
                                  - U_mu(x)_{ij} delta_{y, x+mu}
                                  - U_mu(y)^dag_{ij} delta_{y, x-mu} ]

    This is the negative of the covariant Laplacian, so eigenvalues >= 0.
    """
    d = links.shape[-1]
    N_sites = Ls * Ls * Ls * Lt
    dim = N_sites * d
    is_complex = jnp.iscomplexobj(links)

    dtype = jnp.complex128 if is_complex else jnp.float64
    lap = jnp.zeros((dim, dim), dtype=dtype)

    def site_to_flat(s):
        return ((s[0] * Ls + s[1]) * Ls + s[2]) * Lt + s[3]

    def shift(s, mu, direction):
        sizes = [Ls, Ls, Ls, Lt]
        s_new = list(s)
        s_new[mu] = (s_new[mu] + direction) % sizes[mu]
        return tuple(s_new)

    print(f"  Building {dim}x{dim} Laplacian ({dtype.__name__})...", file=sys.stderr)
    t0 = time.time()

    # Diagonal: 2*4 = 8 per site (sum over 4 directions)
    for x0 in range(Ls):
        for x1 in range(Ls):
            for x2 in range(Ls):
                for x3 in range(Lt):
                    x_flat = site_to_flat((x0, x1, x2, x3))
                    for i in range(d):
                        lap = lap.at[x_flat*d + i, x_flat*d + i].add(8.0)

    # Off-diagonal: -U_mu(x) for forward, -U_mu(y)^dag for backward
    for mu in range(4):
        for x0 in range(Ls):
            for x1 in range(Ls):
                for x2 in range(Ls):
                    for x3 in range(Lt):
                        x = (x0, x1, x2, x3)
                        x_flat = site_to_flat(x)
                        y = shift(x, mu, 1)
                        y_flat = site_to_flat(y)

                        U = links[mu, x[0], x[1], x[2], x[3]]  # (d, d)

                        # Forward: -U_mu(x)_{ij} at (x*d+i, y*d+j)
                        for i in range(d):
                            for j in range(d):
                                lap = lap.at[x_flat*d + i, y_flat*d + j].add(-U[i, j])

                        # Backward: -U_mu(x)^dag_{ij} at (y*d+i, x*d+j)
                        if is_complex:
                            U_dag = U.conj().T
                        else:
                            U_dag = U.T
                        for i in range(d):
                            for j in range(d):
                                lap = lap.at[y_flat*d + i, x_flat*d + j].add(-U_dag[i, j])

    elapsed = time.time() - t0
    print(f"  Laplacian built in {elapsed:.1f}s", file=sys.stderr)

    return lap


# ============================================================
# FADDEEV-POPOV OPERATOR (adjoint rep)
# ============================================================

def build_faddeev_popov(links, group, Ls, Lt):
    """Build the Faddeev-Popov (ghost) operator in the adjoint representation.

    M_FP^{ab}(x,y) = sum_mu [ 2 delta_xy delta_ab
                             - Ad(U_mu(x))_{ab} delta_{y,x+mu}
                             - Ad(U_mu(y)^dag)_{ab} delta_{y,x-mu} ]

    Returns: dense real matrix of shape (N_sites*d_adj, N_sites*d_adj)
    """
    d_fund = links.shape[-1]
    is_complex = jnp.iscomplexobj(links)

    if group == 'g2':
        d_adj = 14
        adjoint_fn = adjoint_g2
    else:
        N = d_fund
        d_adj = N * N - 1
        adjoint_fn = lambda U: adjoint_su_n(U, N)

    N_sites = Ls * Ls * Ls * Lt
    dim = N_sites * d_adj

    # FP operator is always real (adjoint rep is real)
    fp = jnp.zeros((dim, dim))

    def site_to_flat(s):
        return ((s[0] * Ls + s[1]) * Ls + s[2]) * Lt + s[3]

    def shift(s, mu, direction):
        sizes = [Ls, Ls, Ls, Lt]
        s_new = list(s)
        s_new[mu] = (s_new[mu] + direction) % sizes[mu]
        return tuple(s_new)

    print(f"  Building {dim}x{dim} FP operator (d_adj={d_adj})...", file=sys.stderr)
    t0 = time.time()

    # Diagonal: 2*4 = 8 per site
    for x0 in range(Ls):
        for x1 in range(Ls):
            for x2 in range(Ls):
                for x3 in range(Lt):
                    x_flat = site_to_flat((x0, x1, x2, x3))
                    for a in range(d_adj):
                        fp = fp.at[x_flat*d_adj + a, x_flat*d_adj + a].add(8.0)

    # Off-diagonal
    for mu in range(4):
        for x0 in range(Ls):
            for x1 in range(Ls):
                for x2 in range(Ls):
                    for x3 in range(Lt):
                        x = (x0, x1, x2, x3)
                        x_flat = site_to_flat(x)
                        y = shift(x, mu, 1)
                        y_flat = site_to_flat(y)

                        U = links[mu, x[0], x[1], x[2], x[3]]
                        Ad_U = adjoint_fn(U)  # (d_adj, d_adj) real

                        # Forward: -Ad(U)_{ab}
                        for a in range(d_adj):
                            for b in range(d_adj):
                                fp = fp.at[x_flat*d_adj + a, y_flat*d_adj + b].add(-Ad_U[a, b])

                        # Backward: -Ad(U)^T_{ab} = -Ad(U^dag)_{ab}
                        for a in range(d_adj):
                            for b in range(d_adj):
                                fp = fp.at[y_flat*d_adj + a, x_flat*d_adj + b].add(-Ad_U[b, a])

    elapsed = time.time() - t0
    print(f"  FP operator built in {elapsed:.1f}s", file=sys.stderr)

    return fp


# ============================================================
# SPECTRAL DIMENSION
# ============================================================

def spectral_dimension(eigenvalues, t_range=None, n_t=200):
    """Compute spectral dimension d_s(t) from eigenvalues of the Laplacian.

    P(t) = sum_k exp(-t * lambda_k)
    d_s(t) = -2 d(ln P) / d(ln t)

    Returns: (t_arr, ds_arr, P_arr)
    """
    # Filter positive eigenvalues (skip near-zero modes)
    evals = eigenvalues[eigenvalues > 1e-10]

    if t_range is None:
        # Heuristic range: 0.01/lambda_max to 10/lambda_min
        lam_min = jnp.min(evals)
        lam_max = jnp.max(evals)
        t_min = 0.01 / lam_max
        t_max = 10.0 / lam_min
        t_range = (float(t_min), float(t_max))

    t_arr = jnp.logspace(jnp.log10(t_range[0]), jnp.log10(t_range[1]), n_t)

    # P(t) = sum exp(-t * lambda)
    # Use vmap for efficiency
    def heat_kernel(t):
        return jnp.sum(jnp.exp(-t * evals))

    P_arr = jax.vmap(heat_kernel)(t_arr)

    # d_s = -2 d(ln P)/d(ln t) via finite differences on log scale
    ln_t = jnp.log(t_arr)
    ln_P = jnp.log(P_arr)
    d_ln_P = jnp.gradient(ln_P, ln_t)
    ds_arr = -2.0 * d_ln_P

    return np.array(t_arr), np.array(ds_arr), np.array(P_arr)


# ============================================================
# MAIN
# ============================================================

def main():
    parser = argparse.ArgumentParser(description='Kevinotron Spectral Analysis (JAX/GPU)')
    parser.add_argument('--config', required=True, help='Path to .npy config file')
    parser.add_argument('--group', required=True, choices=['su2','su3','su4','g2'])
    parser.add_argument('--ls', type=int, required=True)
    parser.add_argument('--lt', type=int, default=0, help='Temporal size (default: 2*ls)')
    parser.add_argument('--laplacian', action='store_true', help='Build fundamental Laplacian')
    parser.add_argument('--fp', action='store_true', help='Build Faddeev-Popov operator')
    parser.add_argument('--ds', action='store_true', help='Compute spectral dimension')
    parser.add_argument('--n-evals', type=int, default=0, help='Print N smallest eigenvalues')
    parser.add_argument('--output', default='', help='Output prefix for eigenvalue files')
    args = parser.parse_args()

    Lt = args.lt if args.lt > 0 else 2 * args.ls
    Ls = args.ls

    # Load configuration
    print(f"Loading {args.config}...", file=sys.stderr)
    links = jnp.array(np.load(args.config))
    print(f"  shape: {links.shape}, dtype: {links.dtype}", file=sys.stderr)

    expected_d = {'su2': 2, 'su3': 3, 'su4': 4, 'g2': 7}[args.group]
    assert links.shape == (4, Ls, Ls, Ls, Lt, expected_d, expected_d), \
        f"Shape mismatch: got {links.shape}, expected (4,{Ls},{Ls},{Ls},{Lt},{expected_d},{expected_d})"

    N_sites = Ls * Ls * Ls * Lt
    print(f"  N_sites = {N_sites}", file=sys.stderr)

    output_prefix = args.output if args.output else f"{args.group}_L{Ls}"

    # Fundamental Laplacian
    if args.laplacian or args.ds:
        print("\n=== COVARIANT LAPLACIAN (fundamental) ===", file=sys.stderr)
        dim_fund = N_sites * expected_d
        mem_gb = dim_fund * dim_fund * (16 if jnp.iscomplexobj(links) else 8) / 1e9
        print(f"  Matrix size: {dim_fund} x {dim_fund} ({mem_gb:.2f} GB)", file=sys.stderr)

        lap = build_covariant_laplacian_fund(links, args.group, Ls, Lt)

        print("  Diagonalizing...", file=sys.stderr)
        t0 = time.time()
        if jnp.iscomplexobj(lap):
            evals = jnp.linalg.eigvalsh(lap)
        else:
            evals = jnp.linalg.eigvalsh(lap)
        evals = jax.block_until_ready(evals)
        elapsed = time.time() - t0
        print(f"  Diagonalization: {elapsed:.1f}s", file=sys.stderr)

        evals_np = np.array(evals)
        np.save(f"{output_prefix}_evals_fund.npy", evals_np)

        n_print = args.n_evals if args.n_evals > 0 else min(20, len(evals_np))
        print(f"\n  {n_print} smallest eigenvalues:")
        for i in range(n_print):
            print(f"    lambda_{i} = {evals_np[i]:.8f}")

        print(f"\n  lambda_min = {evals_np[0]:.8f}")
        print(f"  lambda_max = {evals_np[-1]:.8f}")
        print(f"  n_zero (< 1e-8) = {np.sum(evals_np < 1e-8)}")
        print(f"  Saved to {output_prefix}_evals_fund.npy")

        # Spectral dimension
        if args.ds:
            print("\n=== SPECTRAL DIMENSION ===", file=sys.stderr)
            t_arr, ds_arr, P_arr = spectral_dimension(evals)

            # Find plateau: d_s should plateau at 4 for short diffusion times
            # and drop at long times (finite volume)
            mid = len(t_arr) // 2
            ds_plateau = np.mean(ds_arr[mid-10:mid+10])
            print(f"\n  d_s at midrange: {ds_plateau:.4f}")
            print(f"  Expected: 4.0 for 4D gauge theory")

            # Save
            np.savez(f"{output_prefix}_ds.npz",
                     t=t_arr, ds=ds_arr, P=P_arr)
            print(f"  Saved to {output_prefix}_ds.npz")

    # Faddeev-Popov
    if args.fp:
        d_adj = {'su2': 3, 'su3': 8, 'su4': 15, 'g2': 14}[args.group]
        print(f"\n=== FADDEEV-POPOV OPERATOR (adjoint, d_adj={d_adj}) ===", file=sys.stderr)
        dim_fp = N_sites * d_adj
        mem_gb = dim_fp * dim_fp * 8 / 1e9  # always real
        print(f"  Matrix size: {dim_fp} x {dim_fp} ({mem_gb:.2f} GB)", file=sys.stderr)

        fp = build_faddeev_popov(links, args.group, Ls, Lt)

        print("  Diagonalizing...", file=sys.stderr)
        t0 = time.time()
        fp_evals = jnp.linalg.eigvalsh(fp)
        fp_evals = jax.block_until_ready(fp_evals)
        elapsed = time.time() - t0
        print(f"  Diagonalization: {elapsed:.1f}s", file=sys.stderr)

        fp_evals_np = np.array(fp_evals)
        np.save(f"{output_prefix}_evals_fp.npy", fp_evals_np)

        n_print = args.n_evals if args.n_evals > 0 else min(20, len(fp_evals_np))
        print(f"\n  {n_print} smallest FP eigenvalues:")
        for i in range(n_print):
            print(f"    mu_{i} = {fp_evals_np[i]:.8f}")

        n_zero = np.sum(fp_evals_np < 1e-8)
        print(f"\n  mu_min = {fp_evals_np[0]:.8f}")
        print(f"  n_zero (< 1e-8) = {n_zero}")
        print(f"  Expected n_zero: {d_adj} (global gauge zero modes)")
        print(f"  Saved to {output_prefix}_evals_fp.npy")


if __name__ == '__main__':
    main()
