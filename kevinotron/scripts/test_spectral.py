#!/usr/bin/env python3
"""
KEVINOTRON SPECTRAL TEST
=========================
Test the JAX spectral module with an SU(2) L=4 cold-start configuration.

Steps:
  1. Generate a cold-start config (all links = identity)
  2. Build the covariant Laplacian in the fundamental rep
  3. Diagonalize and compute spectral dimension d_s
  4. Verify d_s ~ 4.0 for the cold start (free theory)

The cold start should give a flat Laplacian eigenspectrum
corresponding to the free 4D lattice Laplacian, and the spectral
dimension should be d_s = 4.0 at intermediate diffusion times.

Usage:
    python3 test_spectral.py
    python3 test_spectral.py --config config_su2_L4.npy --group su2 --ls 4
    python3 test_spectral.py --cold --group su2 --ls 4

Author: Kevin Remondiere (ORCID 0009-0008-2443-7166)
"""

import os
import sys
import argparse
import time
import numpy as np

# Setup JAX
os.environ['JAX_ENABLE_X64'] = '1'

try:
    import jax
    import jax.numpy as jnp
    HAS_JAX = True
    print(f"JAX {jax.__version__}, x64={jax.config.jax_enable_x64}, devices: {jax.devices()}", file=sys.stderr)
except ImportError:
    HAS_JAX = False
    print("WARNING: JAX not available, using numpy fallback", file=sys.stderr)

# Add parent for spectral module
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'jax_ds'))


def generate_cold_config(group, Ls, Lt):
    """Generate a cold-start config (all identity matrices)."""
    d = {'su2': 2, 'su3': 3, 'su4': 4, 'g2': 7, 'sp4': 4, 'so7': 7}[group]
    is_complex = group in ('su2', 'su3', 'su4', 'sp4')

    if is_complex:
        links = np.zeros((4, Ls, Ls, Ls, Lt, d, d), dtype=np.complex128)
        for mu in range(4):
            for x0 in range(Ls):
                for x1 in range(Ls):
                    for x2 in range(Ls):
                        for x3 in range(Lt):
                            links[mu, x0, x1, x2, x3] = np.eye(d, dtype=np.complex128)
    else:
        links = np.zeros((4, Ls, Ls, Ls, Lt, d, d), dtype=np.float64)
        for mu in range(4):
            for x0 in range(Ls):
                for x1 in range(Ls):
                    for x2 in range(Ls):
                        for x3 in range(Lt):
                            links[mu, x0, x1, x2, x3] = np.eye(d, dtype=np.float64)

    return links


def build_free_laplacian_numpy(Ls, Lt, d, is_complex):
    """Build covariant Laplacian with identity links (= free lattice Laplacian x I_d).

    Uses numpy (no JAX needed).
    """
    N_sites = Ls * Ls * Ls * Lt
    dim = N_sites * d
    dtype = np.complex128 if is_complex else np.float64

    print(f"  Building {dim}x{dim} free Laplacian ({dtype.__name__})...", file=sys.stderr)
    t0 = time.time()

    lap = np.zeros((dim, dim), dtype=dtype)

    def site_to_flat(s):
        return ((s[0] * Ls + s[1]) * Ls + s[2]) * Lt + s[3]

    sizes = [Ls, Ls, Ls, Lt]

    for x0 in range(Ls):
        for x1 in range(Ls):
            for x2 in range(Ls):
                for x3 in range(Lt):
                    x = (x0, x1, x2, x3)
                    x_flat = site_to_flat(x)

                    # Diagonal: 2*4 = 8 per (site, color)
                    for i in range(d):
                        lap[x_flat * d + i, x_flat * d + i] += 8.0

                    # Off-diagonal: identity link = -delta_{ij}
                    for mu in range(4):
                        y = list(x)
                        y[mu] = (y[mu] + 1) % sizes[mu]
                        y_flat = site_to_flat(tuple(y))

                        z = list(x)
                        z[mu] = (z[mu] - 1) % sizes[mu]
                        z_flat = site_to_flat(tuple(z))

                        for i in range(d):
                            lap[x_flat * d + i, y_flat * d + i] -= 1.0
                            lap[x_flat * d + i, z_flat * d + i] -= 1.0

    elapsed = time.time() - t0
    print(f"  Built in {elapsed:.1f}s", file=sys.stderr)
    return lap


def spectral_dimension_numpy(eigenvalues, n_t=200):
    """Compute spectral dimension from eigenvalues (numpy version)."""
    evals = eigenvalues[eigenvalues > 1e-10]
    if len(evals) == 0:
        return np.array([]), np.array([]), np.array([])

    lam_min = np.min(evals)
    lam_max = np.max(evals)
    t_min = 0.01 / lam_max
    t_max = 10.0 / lam_min
    t_arr = np.logspace(np.log10(t_min), np.log10(t_max), n_t)

    # P(t) = sum exp(-t * lambda)
    P_arr = np.array([np.sum(np.exp(-t * evals)) for t in t_arr])

    # d_s = -2 d(ln P)/d(ln t)
    ln_t = np.log(t_arr)
    ln_P = np.log(np.maximum(P_arr, 1e-300))
    d_ln_P = np.gradient(ln_P, ln_t)
    ds_arr = -2.0 * d_ln_P

    return t_arr, ds_arr, P_arr


def test_cold_start(group, Ls, Lt):
    """Run the full cold-start spectral test."""
    d = {'su2': 2, 'su3': 3, 'su4': 4, 'g2': 7, 'sp4': 4, 'so7': 7}[group]
    is_complex = group in ('su2', 'su3', 'su4', 'sp4')
    N_sites = Ls * Ls * Ls * Lt
    dim = N_sites * d

    print(f"\n{'='*60}")
    print(f"  SPECTRAL TEST: {group.upper()} cold start, L={Ls}, Lt={Lt}")
    print(f"  d_fund={d}, N_sites={N_sites}, matrix_dim={dim}")
    print(f"{'='*60}")

    # Memory check
    mem_bytes = dim * dim * (16 if is_complex else 8)
    mem_gb = mem_bytes / 1e9
    print(f"  Memory: {mem_gb:.2f} GB")
    if mem_gb > 12:
        print(f"  WARNING: {mem_gb:.1f} GB exceeds typical GPU memory, may OOM")

    # Build Laplacian
    lap = build_free_laplacian_numpy(Ls, Lt, d, is_complex)

    # Verify symmetry
    if is_complex:
        sym_err = np.max(np.abs(lap - lap.conj().T))
    else:
        sym_err = np.max(np.abs(lap - lap.T))
    print(f"  Hermiticity check: max|L - L^dag| = {sym_err:.2e}")
    assert sym_err < 1e-12, f"Laplacian not Hermitian! err={sym_err}"

    # Diagonalize
    print("  Diagonalizing...", file=sys.stderr)
    t0 = time.time()
    if is_complex:
        evals = np.linalg.eigvalsh(lap)
    else:
        evals = np.linalg.eigvalsh(lap)
    elapsed = time.time() - t0
    print(f"  Diagonalization: {elapsed:.1f}s")

    # Report eigenvalues
    n_zero = np.sum(np.abs(evals) < 1e-8)
    print(f"  lambda_min = {evals[0]:.8f}")
    print(f"  lambda_max = {evals[-1]:.8f}")
    print(f"  n_zero (|lambda| < 1e-8) = {n_zero}")
    print(f"  Expected n_zero = {d} (d_fund constant modes)")

    # For cold start, eigenvalues should be d-fold degenerate free lattice eigenvalues
    # Free lattice: lambda_k = 2*sum_mu(1 - cos(2*pi*k_mu/L_mu))
    # Smallest nonzero: 2*(1 - cos(2*pi/L)) for one direction

    lam_min_expected = 2 * (1 - np.cos(2 * np.pi / Ls))
    print(f"  Smallest nonzero expected: {lam_min_expected:.8f}")
    evals_nonzero = evals[evals > 1e-8]
    if len(evals_nonzero) > 0:
        print(f"  Smallest nonzero measured: {evals_nonzero[0]:.8f}")
        ratio = evals_nonzero[0] / lam_min_expected
        print(f"  Ratio: {ratio:.6f} (should be ~1.0)")

    # Spectral dimension
    print("\n  Computing spectral dimension...")
    t_arr, ds_arr, P_arr = spectral_dimension_numpy(evals)

    if len(ds_arr) > 0:
        # Find plateau region (middle third of log-t range)
        n = len(ds_arr)
        mid_start = n // 3
        mid_end = 2 * n // 3
        ds_plateau = np.mean(ds_arr[mid_start:mid_end])
        ds_std = np.std(ds_arr[mid_start:mid_end])

        print(f"  d_s at plateau: {ds_plateau:.4f} +/- {ds_std:.4f}")
        print(f"  Expected: 4.0 for 4D lattice")

        # PASS/FAIL
        if abs(ds_plateau - 4.0) < 0.5:
            print(f"\n  PASS: d_s = {ds_plateau:.3f} ~ 4.0")
            return True
        else:
            print(f"\n  FAIL: d_s = {ds_plateau:.3f}, expected ~4.0")
            return False
    else:
        print("  No nonzero eigenvalues -- cannot compute d_s")
        return False


def test_from_config(config_path, group, Ls, Lt):
    """Test spectral properties from an .npy config file."""
    if not HAS_JAX:
        print("ERROR: JAX required for config file analysis")
        sys.exit(1)

    from spectral import (
        build_covariant_laplacian_fund,
        spectral_dimension as spectral_dimension_jax,
    )

    print(f"\n{'='*60}")
    print(f"  SPECTRAL TEST: {group.upper()} from {config_path}")
    print(f"{'='*60}")

    links = jnp.array(np.load(config_path))
    print(f"  Config shape: {links.shape}, dtype: {links.dtype}")

    d = links.shape[-1]
    N_sites = Ls * Ls * Ls * Lt
    dim = N_sites * d

    print(f"  d_fund={d}, N_sites={N_sites}, matrix_dim={dim}")

    # Build Laplacian
    lap = build_covariant_laplacian_fund(links, group, Ls, Lt)

    # Diagonalize
    print("  Diagonalizing...", file=sys.stderr)
    t0 = time.time()
    evals = jnp.linalg.eigvalsh(lap)
    evals = jax.block_until_ready(evals)
    elapsed = time.time() - t0
    print(f"  Diagonalization: {elapsed:.1f}s")

    evals_np = np.array(evals)
    n_zero = np.sum(np.abs(evals_np) < 1e-8)
    print(f"  lambda_min = {evals_np[0]:.8f}")
    print(f"  lambda_max = {evals_np[-1]:.8f}")
    print(f"  n_zero = {n_zero}")

    # Spectral dimension
    t_arr, ds_arr, P_arr = spectral_dimension_jax(evals)
    t_arr, ds_arr, P_arr = np.array(t_arr), np.array(ds_arr), np.array(P_arr)

    n = len(ds_arr)
    mid_start = n // 3
    mid_end = 2 * n // 3
    ds_plateau = np.mean(ds_arr[mid_start:mid_end])

    print(f"  d_s at plateau: {ds_plateau:.4f}")
    print(f"  Expected: 4.0")

    return ds_plateau


def main():
    parser = argparse.ArgumentParser(description='Kevinotron Spectral Test')
    parser.add_argument('--config', default='', help='Path to .npy config file')
    parser.add_argument('--group', default='su2', choices=['su2','su3','su4','g2','sp4','so7'])
    parser.add_argument('--ls', type=int, default=4)
    parser.add_argument('--lt', type=int, default=0)
    parser.add_argument('--cold', action='store_true', help='Run cold-start test (no config file needed)')
    args = parser.parse_args()

    Lt = args.lt if args.lt > 0 else 2 * args.ls

    if args.config and os.path.exists(args.config):
        test_from_config(args.config, args.group, args.ls, Lt)
    elif args.cold or not args.config:
        # Default: cold-start test
        success = test_cold_start(args.group, args.ls, Lt)
        sys.exit(0 if success else 1)
    else:
        print(f"ERROR: config file not found: {args.config}")
        sys.exit(1)


if __name__ == '__main__':
    main()
