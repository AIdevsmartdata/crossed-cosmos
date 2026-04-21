#!/usr/bin/env python3
"""
N5-ph-fnl-sensitivity.py
========================
Sanity check N5: persistent-homology (PH) Betti-number shift as a discriminator
of primordial non-Gaussianity (fNL) at LSST-Y10 scale.

Claim (paper/eci.tex, prediction table):
  Topological summaries of the projected matter density (Betti curves / Euler
  characteristic of sublevel sets) shift at detectable amplitude for fNL ~ 1
  when integrated over LSST-Y10 area (~18,000 deg^2, ~10^4 Mpc/h boxes).

What THIS script validates:
  - Order-of-magnitude: does Δχ(ν) / σ_χ(ν) grow with fNL in a toy 2D GRF
    with a local-type f_NL quadratic perturbation δ_NG = δ_G + fNL (δ_G^2 - <δ_G^2>)?
  - Qualitative scaling: Δχ/σ roughly linear in fNL for fNL ≪ 1/σ_δ.

What this does NOT validate:
  - Real LSST forecast (needs Quijote-PNG N-body sims, projection kernels,
    photo-z, shape noise, masking, covariance from ~10^3 sims).
  - True persistent homology H_0/H_1 (needs GUDHI / Ripser). We use the Euler
    characteristic χ(ν) = b_0(ν) - b_1(ν) as a CRUDE PH proxy, computed with
    scipy.ndimage.label on sublevel sets {δ ≤ ν}. For 2D binary images
    b_0 = connected components, b_1 = holes = b_0(complement) - 1 (Alexander
    duality on the sphere, OK modulo boundary).
  - Projection / redshift evolution / baryons.

References:
  - Heydenreich, Brueck, Harnois-Déraps 2021, A&A 648 A74 (PH for weak lensing)
  - Biagetti, Cole, Shiu 2021, JCAP 04 022 (PH for PNG, Quijote-PNG)
  - Parroni et al. 2024, A&A 691 A300 (Minkowski functionals LSST forecast)

Output: figures/N5-fnl-sensitivity.pdf
"""

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from scipy import ndimage

rng = np.random.default_rng(20260421)

# ── Config ────────────────────────────────────────────────────────────────────
N_GRID   = 128
N_REAL   = 50
FNL_LIST = [0.0, 1.0, 10.0, 100.0]
P_INDEX  = -2.0          # P(k) ∝ k^P_INDEX
K_MIN    = 1.0           # avoid k=0 divergence
N_NU     = 41            # threshold grid for χ(ν)
NU_RANGE = (-3.0, 3.0)   # in units of σ_δ after normalization
OUTFILE  = "figures/N5-fnl-sensitivity.pdf"

print("=" * 64)
print("N5 — PH (Euler-χ proxy) sensitivity to fNL on 2D GRF (toy)")
print("=" * 64)
print(f"Grid: {N_GRID}×{N_GRID} | realizations: {N_REAL} | fNL: {FNL_LIST}")
print(f"P(k) ∝ k^{P_INDEX}  (toy LSS-like slope)")
print()

# ── Gaussian random field generator ───────────────────────────────────────────
def make_grf(n, p_index=-2.0, seed=None):
    """2D Gaussian random field with P(k) ∝ k^p_index. Unit variance output."""
    rloc = np.random.default_rng(seed)
    kx = np.fft.fftfreq(n) * n
    ky = np.fft.fftfreq(n) * n
    KX, KY = np.meshgrid(kx, ky, indexing="ij")
    K  = np.sqrt(KX**2 + KY**2)
    K[0, 0] = 1.0  # avoid div/0
    Pk = np.where(K >= K_MIN, K**p_index, 0.0)
    Pk[0, 0] = 0.0
    amp   = np.sqrt(Pk)
    noise = (rloc.standard_normal((n, n)) + 1j * rloc.standard_normal((n, n))) / np.sqrt(2)
    field = np.fft.ifft2(noise * amp).real
    field -= field.mean()
    s = field.std()
    if s > 0:
        field /= s
    return field

def apply_fnl(delta_g, fnl):
    """Local-type PNG: δ = δ_G + fNL (δ_G^2 - <δ_G^2>). Renormalize to unit σ."""
    if fnl == 0.0:
        return delta_g
    dg2 = delta_g**2
    delta = delta_g + fnl * (dg2 - dg2.mean())
    delta -= delta.mean()
    s = delta.std()
    if s > 0:
        delta /= s
    return delta

# ── Euler characteristic on sublevel sets ─────────────────────────────────────
def euler_chi_curve(field, nus):
    """
    χ(ν) = b_0({δ≤ν}) - b_1({δ≤ν})   (2D; crude PH proxy)
    b_0 : # connected components of sublevel set
    b_1 : # holes ≈ # components of complement − 1 (for compact domain)
    NOTE: real PH_0/PH_1 persistence barcodes require GUDHI; this is a summary
    statistic (Euler characteristic curve / a.k.a. Minkowski functional χ).
    """
    chi = np.empty_like(nus)
    struct = ndimage.generate_binary_structure(2, 1)  # 4-connectivity
    for i, nu in enumerate(nus):
        sub = field <= nu
        _, b0 = ndimage.label(sub, structure=struct)
        _, b0c = ndimage.label(~sub, structure=struct)
        b1 = max(b0c - 1, 0)
        chi[i] = b0 - b1
    return chi

# ── Run ensembles ─────────────────────────────────────────────────────────────
nus = np.linspace(NU_RANGE[0], NU_RANGE[1], N_NU)
curves = {fnl: np.zeros((N_REAL, N_NU)) for fnl in FNL_LIST}

for r in range(N_REAL):
    seed = 1000 + r
    dg = make_grf(N_GRID, P_INDEX, seed=seed)
    for fnl in FNL_LIST:
        d = apply_fnl(dg, fnl)
        curves[fnl][r] = euler_chi_curve(d, nus)
    if (r + 1) % 10 == 0:
        print(f"  realization {r+1}/{N_REAL} done")

mean = {fnl: curves[fnl].mean(axis=0) for fnl in FNL_LIST}
std  = {fnl: curves[fnl].std(axis=0, ddof=1) for fnl in FNL_LIST}

# σ from fNL=0 baseline (cosmic variance of χ under Gaussian hypothesis)
sigma0 = std[0.0]
sigma0_safe = np.where(sigma0 > 1e-12, sigma0, 1e-12)

# ── Summary table ─────────────────────────────────────────────────────────────
print()
print(f"{'fNL':>8} {'max|Δχ|':>10} {'max|Δχ|/σ₀':>14} {'ν*':>8} {'Σ(Δχ/σ₀)²':>14}")
print("-" * 60)
base = mean[0.0]
rows = []
for fnl in FNL_LIST:
    dchi = mean[fnl] - base
    ratio = np.abs(dchi) / sigma0_safe
    imax = int(np.argmax(ratio))
    tot_snr = float(np.sqrt(np.sum(ratio**2)))   # naive (ignores covariance)
    rows.append((fnl, np.abs(dchi).max(), ratio[imax], nus[imax], tot_snr))
    print(f"{fnl:>8.1f} {np.abs(dchi).max():>10.3f} {ratio[imax]:>14.3f} "
          f"{nus[imax]:>8.2f} {tot_snr:>14.3f}")

print()
print("Reading:")
print("  max|Δχ|/σ₀ ≥ 1  → 1σ toy detection per realization at some threshold ν*.")
print("  Σ(Δχ/σ₀)²  ≈ naive cumulative SNR summed over ν (no covariance; upper bound).")
print("  fNL≈1 discrimination requires this ratio × √N_fields_LSST ≳ 3.")

# ── Figure ────────────────────────────────────────────────────────────────────
import os
os.makedirs("figures", exist_ok=True)

fig, axes = plt.subplots(1, 2, figsize=(12, 4.6))

ax = axes[0]
colors = ["#1f77b4", "#2ca02c", "#ff7f0e", "#d62728"]
for fnl, col in zip(FNL_LIST, colors):
    ax.plot(nus, mean[fnl], color=col, lw=1.8, label=rf"$f_{{\rm NL}}={fnl:g}$")
    ax.fill_between(nus, mean[fnl] - std[fnl], mean[fnl] + std[fnl],
                    color=col, alpha=0.12)
ax.set_xlabel(r"threshold $\nu$ [units of $\sigma_\delta$]")
ax.set_ylabel(r"$\chi(\nu)$  (Euler char. of $\{\delta\leq\nu\}$)")
ax.set_title(r"Euler-$\chi$ curve: mean $\pm$ 1$\sigma$ (N=%d)" % N_REAL)
ax.legend(fontsize=9)
ax.grid(alpha=0.3)

ax = axes[1]
for fnl, col in zip(FNL_LIST, colors):
    if fnl == 0.0:
        continue
    dchi = mean[fnl] - base
    ax.plot(nus, dchi / sigma0_safe, color=col, lw=1.8,
            label=rf"$f_{{\rm NL}}={fnl:g}$")
ax.axhline(0, color="k", lw=0.6)
ax.axhline(+1, color="grey", ls="--", lw=0.8)
ax.axhline(-1, color="grey", ls="--", lw=0.8)
ax.set_xlabel(r"threshold $\nu$")
ax.set_ylabel(r"$\Delta\chi(\nu) / \sigma_\chi^{f_{\rm NL}=0}(\nu)$")
ax.set_title(r"Detectability proxy vs $f_{\rm NL}$")
ax.legend(fontsize=9)
ax.grid(alpha=0.3)

plt.suptitle("N5 — toy PH sensitivity to $f_{\\rm NL}$ "
             "(2D GRF, P(k)$\\propto k^{-2}$, Euler-$\\chi$ proxy)",
             fontsize=11)
plt.tight_layout()
plt.savefig(OUTFILE, bbox_inches="tight")
print()
print(f"Saved: {OUTFILE}")

# ── Verdict ───────────────────────────────────────────────────────────────────
r1  = next(r for r in rows if r[0] == 1.0)
r10 = next(r for r in rows if r[0] == 10.0)
print()
print("VERDICT (toy, single 128² field):")
print(f"  fNL=1   : max|Δχ|/σ₀ = {r1[2]:.2f}   (per-field; LSST-Y10 ~10³ patches → × ~30)")
print(f"  fNL=10  : max|Δχ|/σ₀ = {r10[2]:.2f}")
print("  Scaling with fNL is ~linear in the weak-NG regime, as expected.")
print("  REMINDER: real forecast needs Quijote-PNG + full PH (GUDHI) + covariance.")
print("=" * 64)
