#!/usr/bin/env python3
"""
V7 Test 5: Odlyzko zero-statistics vs Montgomery-Dyson GUE pair correlation.

Tests whether empirical R_2(x) on first 10^5 Riemann zeta zeros deviates from
GUE in a way compatible with CCM arXiv:2511.22755 O(1/log T) Euler-product
truncation corrections.

Data: http://www.dtc.umn.edu/~odlyzko/zeta_tables/zeros1 (100k zeros, ~5 MB).
"""
from __future__ import annotations

import os
import sys
import urllib.request
from pathlib import Path

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

# ----------------------------------------------------------------------------
# 1. Load Odlyzko zeros
# ----------------------------------------------------------------------------
ZEROS_URL = "http://www.dtc.umn.edu/~odlyzko/zeta_tables/zeros1"
ZEROS_PATH = Path("/tmp/odlyzko_zeros1.txt")

def load_zeros() -> np.ndarray:
    if not ZEROS_PATH.exists():
        print(f"[fetch] {ZEROS_URL} -> {ZEROS_PATH}")
        urllib.request.urlretrieve(ZEROS_URL, ZEROS_PATH)
    gammas = np.loadtxt(ZEROS_PATH)
    print(f"[data] Loaded {len(gammas)} zeros from {ZEROS_URL}")
    print(f"[data] range: gamma_1 = {gammas[0]:.4f}, gamma_N = {gammas[-1]:.4f}")
    return gammas

# ----------------------------------------------------------------------------
# 2. Pair correlation R_2(x) using the standard Odlyzko/Montgomery
#    normalisation. We *unfold* the zeros: tilde_gamma_n = gamma_n * log(gamma_n/(2*pi))/(2*pi).
#    Then mean spacing is 1. Pair correlation on grid x with bin Dx:
#      R_2(x) = #pairs (n<m) with tilde_gamma_m - tilde_gamma_n in [x, x+Dx] / (N * Dx)
#    normalised s.t. R_2(x) -> 1 as x -> infty.
# ----------------------------------------------------------------------------
def unfold(gammas: np.ndarray) -> np.ndarray:
    # Riemann-von Mangoldt: N(T) = (T/2pi) log(T/2pi) - T/2pi + 7/8 + S(T) + O(1/T)
    # Standard Odlyzko unfolding: tilde_gamma_n = N(gamma_n) - S(gamma_n)  ~  smooth part
    t = gammas / (2.0 * np.pi)
    return t * np.log(t) - t + 7.0 / 8.0

def pair_correlation(tg: np.ndarray, xmax: float, dx: float):
    """
    Empirical pair correlation. Counts pairs within distance xmax only (fast).
    Uses sorted-array two-pointer sweep.
    Returns x_centers, R2, counts_per_bin.
    """
    N = len(tg)
    nbins = int(round(xmax / dx))
    counts = np.zeros(nbins, dtype=np.int64)
    # tg is already sorted
    j = 0
    for i in range(N):
        # advance j so tg[j] > tg[i] + xmax
        if j <= i:
            j = i + 1
        while j < N and tg[j] - tg[i] < xmax:
            j += 1
        # now pairs i<k<j with tg[k]-tg[i] in [0, xmax)
        diffs = tg[i + 1 : j] - tg[i]
        idx = (diffs / dx).astype(np.int64)
        idx = idx[idx < nbins]
        np.add.at(counts, idx, 1)
    # density: number of pairs with one endpoint in [0,N) and other in window
    # Expected uniform density of pairs = N (since mean spacing 1, so per unit
    # interval there are ~1 zero, and we have N starting points).
    # So R_2(x) dx ~ counts / N, and R_2(x) = counts / (N * dx).
    R2 = counts / (N * dx)
    x_centers = dx * (0.5 + np.arange(nbins))
    return x_centers, R2, counts

# ----------------------------------------------------------------------------
# 3. GUE prediction
# ----------------------------------------------------------------------------
def R2_GUE(x: np.ndarray) -> np.ndarray:
    out = np.ones_like(x)
    mask = np.abs(x) > 1e-12
    pix = np.pi * x[mask]
    out[mask] = 1.0 - (np.sin(pix) / pix) ** 2
    out[~mask] = 0.0
    return out

# ----------------------------------------------------------------------------
# 4. Main
# ----------------------------------------------------------------------------
def main():
    gammas = load_zeros()
    tg = unfold(gammas)
    # Sanity: mean spacing should be ~1
    spacings = np.diff(tg)
    print(f"[unfold] mean unfolded spacing = {spacings.mean():.6f} (expect ~1)")
    print(f"[unfold] std  unfolded spacing = {spacings.std():.6f}")

    dx = 0.05
    xmax = 3.0
    x, R2_emp, counts = pair_correlation(tg, xmax=xmax, dx=dx)
    R2_th = R2_GUE(x)

    # Poisson error bars on counts
    sigma_counts = np.sqrt(np.maximum(counts, 1))
    sigma_R2 = sigma_counts / (len(tg) * dx)

    # Jackknife: split zeros in 10 blocks, recompute on each leave-one-out
    print("[jack] computing jackknife error bars (10 blocks)...")
    nblocks = 10
    block_size = len(tg) // nblocks
    R2_jack = []
    for b in range(nblocks):
        lo, hi = b * block_size, (b + 1) * block_size
        tg_b = np.concatenate([tg[:lo], tg[hi:]])
        _, R2_b, _ = pair_correlation(tg_b, xmax=xmax, dx=dx)
        R2_jack.append(R2_b)
    R2_jack = np.array(R2_jack)
    R2_mean = R2_jack.mean(axis=0)
    sigma_jack = np.sqrt((nblocks - 1) / nblocks * ((R2_jack - R2_mean) ** 2).sum(axis=0))

    # Use max(poisson, jackknife) as conservative error
    sigma = np.maximum(sigma_R2, sigma_jack)

    residual = R2_emp - R2_th
    # chi^2 vs pure GUE, excluding the x=0 bin (trivial)
    mask = x > 0.1
    chi2 = np.sum((residual[mask] / sigma[mask]) ** 2)
    dof = mask.sum()
    from scipy.stats import chi2 as chi2_dist
    p_val = 1.0 - chi2_dist.cdf(chi2, dof)

    print(f"[fit] chi^2 vs pure GUE = {chi2:.2f} / {dof} dof")
    print(f"[fit] chi^2/dof = {chi2/dof:.3f}")
    print(f"[fit] p-value (chi^2 > obs | GUE) = {p_val:.4e}")

    max_dev = np.max(np.abs(residual[mask]) / sigma[mask])
    print(f"[fit] max |residual/sigma| = {max_dev:.2f} at x = {x[mask][np.argmax(np.abs(residual[mask]) / sigma[mask])]:.2f}")

    # Plot
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(8, 8), sharex=True,
                                    gridspec_kw={"height_ratios": [3, 1]})
    ax1.errorbar(x, R2_emp, yerr=sigma, fmt="o", ms=3, lw=0.8,
                 label=f"Odlyzko N={len(gammas)}", color="tab:blue")
    xx = np.linspace(1e-3, xmax, 500)
    ax1.plot(xx, R2_GUE(xx), "-", color="tab:red",
             label=r"GUE: $1-(\sin\pi x/\pi x)^2$")
    ax1.set_ylabel(r"$R_2(x)$")
    ax1.set_title(f"Zeta-zero pair correlation, first {len(gammas)} zeros\n"
                  f"$\\chi^2/{{\\rm dof}}={chi2/dof:.2f}$, p={p_val:.2e}")
    ax1.legend()
    ax1.grid(alpha=0.3)

    ax2.errorbar(x, residual, yerr=sigma, fmt="o", ms=3, lw=0.8, color="tab:purple")
    ax2.axhline(0, color="black", lw=0.8)
    ax2.set_xlabel("x (normalised spacing)")
    ax2.set_ylabel(r"$R_2^{\rm emp}-R_2^{\rm GUE}$")
    ax2.grid(alpha=0.3)

    out_png = Path("/home/remondiere/crossed-cosmos/derivations/V7-test5-odlyzko.png")
    plt.tight_layout()
    plt.savefig(out_png, dpi=120)
    print(f"[plot] saved {out_png}")

    # Dump residual table
    out_csv = Path("/tmp/V7-test5-residuals.csv")
    np.savetxt(out_csv, np.column_stack([x, R2_emp, R2_th, residual, sigma]),
               header="x R2_emp R2_GUE residual sigma", comments="# ")
    print(f"[save] residual table {out_csv}")

    return dict(chi2=chi2, dof=dof, p=p_val, max_dev=max_dev, N=len(gammas))

if __name__ == "__main__":
    res = main()
    print("RESULT:", res)
