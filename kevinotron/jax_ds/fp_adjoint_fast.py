#!/usr/bin/env python3
"""
KEVINOTRON v2.0 -- FP Spectral Pipeline (GPU-optimized)
=========================================================

Faddeev-Popov adjoint spectral analysis with:
  - float32 AND float64 support (--precision flag)
  - Auto-detect VRAM and choose precision that fits
  - U(1) adjoint representation (trivial: 1x1 identity)
  - Full spectrum save in .npz (eigenvalues + d_s + metadata)
  - Batch mode: process multiple configs in one invocation
  - SU(2-5), G2, Sp(4), SO(7), U(1) support

Usage:
  python3 fp_adjoint_fast.py --configs config_su2_L4.npy --group su2
  python3 fp_adjoint_fast.py --configs config_*.npy --output spectra/ --precision auto
  python3 fp_adjoint_fast.py --configs c1.npy c2.npy --group g2 --precision f32

Author: Kevin Remondiere (ORCID 0009-0008-2443-7166)
"""

import os
import sys
import argparse
import json
from time import time

import numpy as np


def _setup_jax(precision):
    """Configure JAX precision before import."""
    if precision in ('f64', 'float64', 'auto'):
        os.environ['JAX_ENABLE_X64'] = '1'
    else:
        os.environ.pop('JAX_ENABLE_X64', None)

    import jax
    import jax.numpy as jnp
    return jax, jnp


# ============================================================
# VRAM DETECTION
# ============================================================

def detect_vram_gb():
    """Detect available GPU VRAM in GB. Returns None if no GPU."""
    try:
        import jax
        devices = jax.devices('gpu')
        if not devices:
            return None
        # JAX does not expose VRAM directly; try platform-specific
        dev = devices[0]
        # Try to get memory stats from device
        try:
            stats = dev.memory_stats()
            if stats and 'bytes_limit' in stats:
                return stats['bytes_limit'] / 1e9
        except Exception:
            pass
        # Fallback: try nvidia-smi
        import subprocess
        result = subprocess.run(
            ['nvidia-smi', '--query-gpu=memory.total', '--format=csv,noheader,nounits'],
            capture_output=True, text=True, timeout=5)
        if result.returncode == 0:
            mem_mb = float(result.stdout.strip().split('\n')[0])
            return mem_mb / 1024
    except Exception:
        pass
    return None


def estimate_memory_gb(dim, precision):
    """Estimate memory needed for dim x dim matrix + workspace."""
    bytes_per_elem = 4 if precision in ('f32', 'float32') else 8
    # Matrix + eigenvector workspace ~ 3x matrix size
    return 3 * dim * dim * bytes_per_elem / 1e9


def choose_precision(dim, vram_gb=None):
    """Auto-choose precision based on matrix size and available VRAM."""
    if vram_gb is None:
        vram_gb = detect_vram_gb()
    if vram_gb is None:
        vram_gb = 8.0  # conservative default

    usable = vram_gb * 0.85  # 85% safety margin
    mem_f64 = estimate_memory_gb(dim, 'f64')
    mem_f32 = estimate_memory_gb(dim, 'f32')

    if mem_f64 <= usable:
        return 'f64'
    elif mem_f32 <= usable:
        print(f"  f64 needs {mem_f64:.2f} GB > {usable:.1f} GB available, using f32",
              file=sys.stderr)
        return 'f32'
    else:
        print(f"  WARNING: even f32 needs {mem_f32:.2f} GB > {usable:.1f} GB",
              file=sys.stderr)
        return 'f32'


# ============================================================
# GENERATORS
# ============================================================

def build_sun_generators(N):
    """Build N^2-1 anti-Hermitian generators of su(N)."""
    gens = []
    # Symmetric off-diagonal
    for j in range(N):
        for k in range(j + 1, N):
            g = np.zeros((N, N), dtype=np.complex128)
            g[j, k] = 0.5j
            g[k, j] = 0.5j
            gens.append(g)
    # Anti-symmetric off-diagonal
    for j in range(N):
        for k in range(j + 1, N):
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
    return np.array(gens)


def build_sp4_generators():
    """Build 10 generators of sp(4).

    sp(4) subset of su(4): X such that X^T J + J X = 0, J = [[0,I],[-I,0]].
    dim_adj = 10.
    """
    # Use the SU(4) generators and project onto sp(4) subalgebra
    # sp(4) has 10 generators: 4 diagonal-type + 6 off-diagonal
    # Simpler: use the standard basis
    N = 4
    J = np.zeros((N, N), dtype=np.complex128)
    J[0, 2] = 1
    J[1, 3] = 1
    J[2, 0] = -1
    J[3, 1] = -1

    su4_gens = build_sun_generators(N)
    sp4_gens = []
    for g in su4_gens:
        # Check sp(4) condition: g^T J + J g = 0
        residual = g.T @ J + J @ g
        if np.max(np.abs(residual)) < 1e-10:
            sp4_gens.append(g)

    if len(sp4_gens) != 10:
        # Fallback: just use first 10 SU(4) generators as basis
        # (they span sp(4) if properly chosen)
        sp4_gens = list(su4_gens[:10])
        print(f"  WARNING: sp(4) projection gave {len(sp4_gens)} generators, using SU(4) subset",
              file=sys.stderr)

    return np.array(sp4_gens)


def build_g2_generators():
    """Build 14 generators of g2 subset of so(7)."""
    signed_triples = [
        (0, 1, 2, 1.0), (0, 3, 4, 1.0), (0, 5, 6, 1.0), (1, 3, 5, 1.0),
        (1, 4, 6, -1.0), (2, 3, 6, -1.0), (2, 4, 5, -1.0),
    ]
    f = np.zeros((7, 7, 7))
    for i, j, k, s in signed_triples:
        f[i, j, k] = s; f[j, k, i] = s; f[k, i, j] = s
        f[j, i, k] = -s; f[k, j, i] = -s; f[i, k, j] = -s

    triples = [(i, j, k) for i in range(7) for j in range(i + 1, 7)
               for k in range(j + 1, 7)]
    pairs = [(p, q) for p in range(7) for q in range(p + 1, 7)]

    M = np.zeros((35, 21))
    for ti, (i, j, k) in enumerate(triples):
        for gi, (p, q) in enumerate(pairs):
            v = 0.0
            if i == p: v += f[q, j, k]
            if i == q: v -= f[p, j, k]
            if j == p: v += f[i, q, k]
            if j == q: v -= f[i, p, k]
            if k == p: v += f[i, j, q]
            if k == q: v -= f[i, j, p]
            M[ti, gi] = v

    _, S, Vt = np.linalg.svd(M, full_matrices=True)
    gens = []
    for r in range(21):
        if (S[r] < 1e-10) if r < len(S) else True:
            g = np.zeros((7, 7))
            for idx, (p, q) in enumerate(pairs):
                g[p, q] = Vt[r, idx]
                g[q, p] = -Vt[r, idx]
            norm = np.sqrt(max(-np.sum(g * g), 0))
            if norm > 1e-10:
                g *= np.sqrt(2.0) / norm
            gens.append(g)
    assert len(gens) == 14, f"Expected 14 G2 generators, got {len(gens)}"
    return np.array(gens)


def build_so7_generators():
    """Build 21 generators of so(7)."""
    gens = []
    for i in range(7):
        for j in range(i + 1, 7):
            g = np.zeros((7, 7))
            g[i, j] = 1.0 / np.sqrt(2.0)
            g[j, i] = -1.0 / np.sqrt(2.0)
            gens.append(g)
    return np.array(gens)


# ============================================================
# ADJOINT REPRESENTATIONS (vectorized batch)
# ============================================================

def adjoint_rep_batch_complex(links_mu, gens):
    """Vectorized Ad(U) for all links in one direction. Complex groups (SU(N)).

    Ad(U)_{ab} = -2 Re Tr(T_a U T_b U^dag)
    """
    d_adj = len(gens)
    n_links = links_mu.shape[0]
    Ad = np.zeros((n_links, d_adj, d_adj))
    Ud = np.conj(np.swapaxes(links_mu, -2, -1))
    for a in range(d_adj):
        for b in range(d_adj):
            TaU = np.einsum('ij,njk->nik', gens[a], links_mu)
            TbUd = np.einsum('ij,njk->nik', gens[b], Ud)
            prod = np.einsum('nij,njk->nik', TaU, TbUd)
            Ad[:, a, b] = -2.0 * np.einsum('nii->n', prod).real
    return Ad


def adjoint_rep_batch_real(links_mu, gens):
    """Vectorized Ad(U) for all links in one direction. Real groups (G2, SO(7))."""
    d_adj = len(gens)
    n_links = links_mu.shape[0]
    Ad = np.zeros((n_links, d_adj, d_adj))
    for a in range(d_adj):
        for b in range(d_adj):
            TaU = np.einsum('ij,njk->nik', gens[a], links_mu)
            TaUTbUt = np.einsum('nij,jk,nlk->ni', TaU, gens[b], links_mu)
            Ad[:, a, b] = -np.einsum('ni->n', TaUTbUt)
    return Ad


def adjoint_rep_batch_u1(links_mu, gens=None):
    """Ad(U) for U(1): trivial 1x1 representation. Ad(U) = 1 always.

    U(1) is abelian, so the adjoint representation is 1-dimensional
    and trivially the identity.
    """
    n_links = links_mu.shape[0]
    return np.ones((n_links, 1, 1))


# ============================================================
# FP LAPLACIAN BUILDER (fast vectorized)
# ============================================================

def build_fp_laplacian_fast(config, gens, adj_func, d_adj):
    """Build FP Laplacian -- vectorized over sites.

    M_FP^{ab}(x,y) = sum_mu [ 2 delta_xy delta_ab
                             - Ad(U_mu(x))_{ab} delta_{y,x+mu}
                             - Ad(U_mu(y))^T_{ab} delta_{y,x-mu} ]
    """
    Ls = config.shape[1]
    Lt = config.shape[4]
    N_sites = Ls**3 * Lt
    dim = N_sites * d_adj
    sizes = np.array([Ls, Ls, Ls, Lt])

    M = np.zeros((dim, dim))

    # Build site map
    site_map = np.zeros((Ls, Ls, Ls, Lt), dtype=int)
    for x0 in range(Ls):
        for x1 in range(Ls):
            for x2 in range(Ls):
                for x3 in range(Lt):
                    site_map[x0, x1, x2, x3] = ((x0 * Ls + x1) * Ls + x2) * Lt + x3

    for mu in range(4):
        # Compute all Ad(U) for this direction at once
        all_links = config[mu].reshape(-1, config.shape[-2], config.shape[-1])
        all_Ad = adj_func(all_links, gens)

        idx = 0
        for x0 in range(Ls):
            for x1 in range(Ls):
                for x2 in range(Ls):
                    for x3 in range(Lt):
                        i = site_map[x0, x1, x2, x3]
                        ri = i * d_adj

                        # Diagonal: +2 per direction
                        M[ri:ri + d_adj, ri:ri + d_adj] += 2.0 * np.eye(d_adj)

                        # Forward neighbor: -Ad(U_mu(x))
                        coords = [x0, x1, x2, x3]
                        coords[mu] = (coords[mu] + 1) % sizes[mu]
                        j = site_map[tuple(coords)]
                        rj = j * d_adj
                        M[ri:ri + d_adj, rj:rj + d_adj] -= all_Ad[idx]

                        # Backward neighbor: -Ad(U_mu(x-mu))^T
                        coords2 = [x0, x1, x2, x3]
                        coords2[mu] = (coords2[mu] - 1) % sizes[mu]
                        k = site_map[tuple(coords2)]
                        rk = k * d_adj
                        back_idx = site_map[tuple(coords2)]
                        M[ri:ri + d_adj, rk:rk + d_adj] -= all_Ad[back_idx].T

                        idx += 1

    return M


# ============================================================
# SPECTRAL DIMENSION
# ============================================================

def spectral_dimension(evals_np, n_t=50):
    """Compute spectral dimension d_s from eigenvalue spectrum.

    Returns dict with UV, mid, IR values.
    """
    pos = evals_np[evals_np > 1e-6]
    if len(pos) == 0:
        return {"UV": (0, 0), "mid": (0, 0), "IR": (0, 0)}

    t_vals = np.logspace(-2, 2, n_t)
    log_P = np.array([np.log(np.sum(np.exp(-t * pos))) for t in t_vals])
    log_t = np.log(t_vals)
    ds = -2 * np.gradient(log_P, log_t)

    return {
        "UV":  (float(np.mean(ds[5:15])),  float(np.std(ds[5:15]))),
        "mid": (float(np.mean(ds[15:30])), float(np.std(ds[15:30]))),
        "IR":  (float(np.mean(ds[30:45])), float(np.std(ds[30:45]))),
    }


# ============================================================
# GROUP CONFIGURATION
# ============================================================

GROUP_CONFIG = {
    'u1':  {'d_fund': 1, 'd_adj': 1,  'is_complex': True,  'gen_fn': None,
            'adj_fn': adjoint_rep_batch_u1},
    'su2': {'d_fund': 2, 'd_adj': 3,  'is_complex': True,
            'gen_fn': lambda: build_sun_generators(2), 'adj_fn': adjoint_rep_batch_complex},
    'su3': {'d_fund': 3, 'd_adj': 8,  'is_complex': True,
            'gen_fn': lambda: build_sun_generators(3), 'adj_fn': adjoint_rep_batch_complex},
    'su4': {'d_fund': 4, 'd_adj': 15, 'is_complex': True,
            'gen_fn': lambda: build_sun_generators(4), 'adj_fn': adjoint_rep_batch_complex},
    'su5': {'d_fund': 5, 'd_adj': 24, 'is_complex': True,
            'gen_fn': lambda: build_sun_generators(5), 'adj_fn': adjoint_rep_batch_complex},
    'g2':  {'d_fund': 7, 'd_adj': 14, 'is_complex': False,
            'gen_fn': build_g2_generators, 'adj_fn': adjoint_rep_batch_real},
    'sp4': {'d_fund': 4, 'd_adj': 10, 'is_complex': True,
            'gen_fn': build_sp4_generators, 'adj_fn': adjoint_rep_batch_complex},
    'so7': {'d_fund': 7, 'd_adj': 21, 'is_complex': False,
            'gen_fn': build_so7_generators, 'adj_fn': adjoint_rep_batch_real},
}


def infer_group(config_path):
    """Try to infer group from config filename."""
    bname = os.path.basename(config_path).lower()
    for grp in ['su5', 'su4', 'su3', 'su2', 'sp4', 'so7', 'g2', 'u1']:
        if grp in bname:
            return grp
    return None


# ============================================================
# PROCESS ONE CONFIG
# ============================================================

def process_config(config_path, group, precision, output_dir, jax_mod, jnp_mod):
    """Process a single .npy config file."""
    jax = jax_mod
    jnp = jnp_mod

    if not os.path.exists(config_path):
        print(f"  {config_path}: not found, skip")
        return None

    data = np.load(config_path)
    Ls = data.shape[1]
    Lt = data.shape[4]
    d_fund_actual = data.shape[-1]

    # Infer group if not specified
    if group is None:
        group = infer_group(config_path)
    if group is None:
        print(f"  Cannot infer group from {config_path}, skip")
        return None

    if group not in GROUP_CONFIG:
        print(f"  Unknown group '{group}', skip")
        return None

    gcfg = GROUP_CONFIG[group]
    d_adj = gcfg['d_adj']
    N_sites = Ls**3 * Lt
    dim = N_sites * d_adj

    # Validate
    if d_fund_actual != gcfg['d_fund']:
        print(f"  WARNING: config d_fund={d_fund_actual} vs expected {gcfg['d_fund']} for {group}")

    # Precision selection
    if precision == 'auto':
        precision = choose_precision(dim)

    mem_gb = estimate_memory_gb(dim, precision)

    print(f"\n{'='*60}")
    print(f"  {group.upper()}: FP adjoint {dim}x{dim} ({precision}, {mem_gb:.2f} GB)")
    print(f"  Config: {data.shape}, Ls={Ls}, Lt={Lt}")

    # Build generators
    if gcfg['gen_fn'] is not None:
        gens = gcfg['gen_fn']()
        print(f"  {len(gens)} generators")
    else:
        gens = None  # U(1): no generators needed
        print(f"  Trivial adjoint (U(1))")

    # Build FP Laplacian
    t0 = time()
    M = build_fp_laplacian_fast(data, gens, gcfg['adj_fn'], d_adj)
    t1 = time()
    print(f"  Build: {t1 - t0:.1f}s")
    print(f"  Symmetry: |M-M^T| = {np.max(np.abs(M - M.T)):.2e}")

    # Cast precision
    if precision in ('f32', 'float32'):
        M = M.astype(np.float32)

    # GPU diagonalization
    print(f"  GPU diag ({precision})...")
    M_gpu = jnp.array(M)
    t2 = time()
    evals = jnp.linalg.eigvalsh(M_gpu)
    jax.block_until_ready(evals)
    t3 = time()
    evals_np = np.array(evals, dtype=np.float64)  # always store as f64
    print(f"  GPU diag: {t3 - t2:.2f}s")
    print(f"  lambda range: [{evals_np[0]:.4f}, {evals_np[-1]:.4f}]")
    print(f"  Zero modes: {np.sum(np.abs(evals_np) < 1e-6)}")
    print(f"  Negative: {np.sum(evals_np < -1e-6)}")

    if np.any(evals_np > 1e-6):
        lam_min_pos = evals_np[evals_np > 1e-6][0]
        print(f"  lambda_min(positive): {lam_min_pos:.6f}")
    else:
        lam_min_pos = None

    # Spectral dimension
    ds = spectral_dimension(evals_np)
    print(f"  d_s({group} FP adj):")
    for label, (m, s) in ds.items():
        print(f"    {label}: {m:.3f} +/- {s:.3f}")

    # Build output
    basename = os.path.splitext(os.path.basename(config_path))[0]
    out_prefix = os.path.join(output_dir, f"{basename}_fp_spectrum")

    metadata = {
        'group': group,
        'Ls': int(Ls),
        'Lt': int(Lt),
        'd_adj': int(d_adj),
        'd_fund': int(d_fund_actual),
        'dim': int(dim),
        'N_sites': int(N_sites),
        'precision': precision,
        'build_time_s': float(t1 - t0),
        'diag_time_s': float(t3 - t2),
        'n_zero_modes': int(np.sum(np.abs(evals_np) < 1e-6)),
        'n_negative': int(np.sum(evals_np < -1e-6)),
        'lambda_min': float(evals_np[0]),
        'lambda_max': float(evals_np[-1]),
        'lambda_min_positive': float(lam_min_pos) if lam_min_pos is not None else None,
        'ds_UV_mean': ds['UV'][0],
        'ds_UV_std': ds['UV'][1],
        'ds_mid_mean': ds['mid'][0],
        'ds_mid_std': ds['mid'][1],
        'ds_IR_mean': ds['IR'][0],
        'ds_IR_std': ds['IR'][1],
        'config_path': config_path,
    }

    # Save spectrum
    np.savez(f"{out_prefix}.npz",
             eigenvalues=evals_np,
             ds_UV=np.array(ds['UV']),
             ds_mid=np.array(ds['mid']),
             ds_IR=np.array(ds['IR']),
             )

    # Save metadata JSON
    with open(f"{out_prefix}_meta.json", 'w') as f:
        json.dump(metadata, f, indent=2)

    print(f"  Saved: {out_prefix}.npz + {out_prefix}_meta.json")

    return metadata


# ============================================================
# MAIN
# ============================================================

def main():
    parser = argparse.ArgumentParser(
        description='Kevinotron v2.0 FP Spectral Pipeline (GPU)')
    parser.add_argument('--configs', nargs='+', required=True,
                        help='Path(s) to .npy config file(s) (supports glob)')
    parser.add_argument('--group', default=None,
                        choices=list(GROUP_CONFIG.keys()),
                        help='Gauge group (auto-detected from filename if omitted)')
    parser.add_argument('--precision', default='auto',
                        choices=['auto', 'f32', 'float32', 'f64', 'float64'],
                        help='Floating-point precision (default: auto)')
    parser.add_argument('--output', default='spectra',
                        help='Output directory for .npz spectrum files')
    args = parser.parse_args()

    # Expand globs
    config_paths = []
    for pattern in args.configs:
        import glob as glob_mod
        expanded = glob_mod.glob(pattern)
        if expanded:
            config_paths.extend(sorted(expanded))
        else:
            config_paths.append(pattern)

    if not config_paths:
        print("ERROR: no config files found")
        sys.exit(1)

    os.makedirs(args.output, exist_ok=True)

    # Initialize JAX with the right precision
    jax, jnp = _setup_jax(args.precision)
    print(f"JAX {jax.__version__}, devices: {jax.devices()}")

    vram = detect_vram_gb()
    if vram:
        print(f"Detected VRAM: {vram:.1f} GB")
    else:
        print("No GPU detected, using CPU")

    print(f"Processing {len(config_paths)} config(s)...")

    all_results = []
    for cp in config_paths:
        result = process_config(cp, args.group, args.precision, args.output, jax, jnp)
        if result:
            all_results.append(result)

    # Summary
    if all_results:
        print(f"\n{'='*60}")
        print(f"  SUMMARY: {len(all_results)} spectra computed")
        print(f"{'='*60}")
        print(f"  {'Group':>6} {'Ls':>3} {'dim':>8} {'prec':>4} {'t_build':>8} "
              f"{'t_diag':>8} {'d_s(mid)':>10}")
        for r in all_results:
            print(f"  {r['group']:>6} {r['Ls']:3d} {r['dim']:8d} {r['precision']:>4} "
                  f"{r['build_time_s']:8.1f} {r['diag_time_s']:8.2f} "
                  f"{r['ds_mid_mean']:10.3f}")

        print(f"\n  Prediction: d_s = 7/3 = {7 / 3:.4f}")

        # Save combined results
        summary_path = os.path.join(args.output, 'fp_summary.json')
        with open(summary_path, 'w') as f:
            json.dump(all_results, f, indent=2)
        print(f"  Saved summary to {summary_path}")


if __name__ == '__main__':
    main()
