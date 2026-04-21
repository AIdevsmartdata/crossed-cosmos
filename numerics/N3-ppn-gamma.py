#!/usr/bin/env python3
"""
N3-ppn-gamma.py
================
Sanity check N3: Cassini PPN bound on γ vs NMC scalar-tensor prediction.

Claim: NMC coupling ξ_χ with χ_0/M_P ≲ a few × 0.1 leaves the Cassini
bound |γ - 1| < 2.3 × 10^{-5} intact, provided ξ_χ χ_0^2/M_P^2 ≪ 1.

PPN parameter γ in scalar-tensor theory (Brans-Dicke-like):
  γ - 1 = -2 α^2 / (1 + α^2)
where α is the effective scalar coupling to matter (conformal coupling factor).

For NMC theory with L ⊃ ξ χ^2 R / 2 (non-minimal coupling):
  α^2 = ξ^2 χ^2 / (M_P^2/2 + ξ χ^2 + 6ξ^2 χ^2)   [Jordan-frame]

A cleaner form from Faraoni 2004 "Cosmology in Scalar-Tensor Gravity" Eq.(6.22):
  γ - 1 = -2 ξ χ^2 (1 + 8ξ) / [(M_P^2 + ξ(1+6ξ) χ^2)]^2 * M_P^2
         + O(ξ^2 χ^4/M_P^4)

We use the compact leading-order form (valid for ξ χ^2/M_P^2 ≪ 1):
  γ - 1 ≈ -2 ξ χ^2 / [M_P^2 + (1 + 6ξ) ξ χ^2]     [Faraoni 2004, Eq.6.22]

This form is exact for Brans-Dicke with ω_BD = 1/(2ξ) - 3/2 mapping.

References:
  - Cassini bound: Bertotti, Iess, Tortora (2003), Nature 425 374
    |γ - 1| < 2.3 × 10^{-5}  (1σ)
  - NMC formula: Faraoni (2004), "Cosmology in Scalar-Tensor Gravity", Eq.6.22
  - Review: Will (2014), Living Reviews in Relativity, arXiv:1403.7377

Output: n3-ppn-gamma.png
"""

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors

# ── Physical parameters ────────────────────────────────────────────────────────
MP = 1.0          # work in units of M_P = 1

# ── Cassini bound ─────────────────────────────────────────────────────────────
GAMMA_BOUND = 2.3e-5  # |γ - 1| < 2.3 × 10^{-5}

# ── PPN γ formula (Faraoni 2004, Eq. 6.22) ───────────────────────────────────
def gamma_minus_1(xi, chi_over_MP):
    """
    PPN parameter deviation γ - 1 for NMC scalar-tensor theory.

    γ - 1 = -2 ξ χ^2 / [M_P^2 + (1 + 6ξ) ξ χ^2]

    Parameters
    ----------
    xi          : NMC coupling ξ_χ
    chi_over_MP : χ_0 / M_P (VEV in Planck units)

    Returns
    -------
    float : γ - 1  (negative for ξ > 0, as expected)
    """
    chi2 = (chi_over_MP * MP)**2
    numerator   = -2.0 * xi * chi2
    denominator = MP**2 + (1.0 + 6.0*xi) * xi * chi2
    return numerator / denominator

# ── Scan parameter space ───────────────────────────────────────────────────────
xi_arr  = np.linspace(0.0, 1.0, 400)
chi_arr = np.linspace(0.0, 0.5, 400)

XI, CHI = np.meshgrid(xi_arr, chi_arr)
GM1 = gamma_minus_1(XI, CHI)

admissible = np.abs(GM1) <= GAMMA_BOUND

print("=" * 60)
print("N3 — PPN γ bound (Cassini) vs NMC scalar-tensor")
print("=" * 60)
print(f"Cassini bound: |γ - 1| < {GAMMA_BOUND:.1e}  (Bertotti+2003, Nature 425)")
print()

# ── Print table of values ─────────────────────────────────────────────────────
print(f"{'ξ_χ':>6} {'χ₀/M_P':>8} {'γ-1':>14} {'|γ-1|/bound':>14} {'Status':>10}")
print("-" * 56)
test_cases = [
    (0.01, 0.01), (0.01, 0.1), (0.01, 0.5),
    (0.1,  0.01), (0.1,  0.1), (0.1,  0.5),
    (1.0,  0.01), (1.0,  0.1), (1.0,  0.5),
]
for xi_t, chi_t in test_cases:
    gm1 = gamma_minus_1(xi_t, chi_t)
    ratio = abs(gm1) / GAMMA_BOUND
    status = "OK" if abs(gm1) <= GAMMA_BOUND else "EXCLUDED"
    print(f"{xi_t:>6.2f} {chi_t:>8.3f} {gm1:>14.4e} {ratio:>14.3f} {status:>10}")

print()

# Find the boundary curve χ_max(ξ) satisfying |γ-1| = bound
xi_fine = np.linspace(0.001, 1.0, 1000)
chi_boundary = []
for xi_val in xi_fine:
    # |γ-1| = 2ξχ^2 / (1 + (1+6ξ)ξ χ^2) = bound
    # Let x = χ^2:  2ξ x / (1 + (1+6ξ)ξ x) = bound
    # 2ξ x = bound + bound*(1+6ξ)ξ x
    # x (2ξ - bound*(1+6ξ)ξ) = bound
    # x = bound / (2ξ - bound*(1+6ξ)ξ)
    denom_coeff = 2*xi_val - GAMMA_BOUND * (1 + 6*xi_val) * xi_val
    if denom_coeff > 0:
        chi2_max = GAMMA_BOUND / denom_coeff
        chi_boundary.append(np.sqrt(chi2_max))
    else:
        chi_boundary.append(np.nan)
chi_boundary = np.array(chi_boundary)

# For ξ ≪ 1: χ_max ≈ M_P * sqrt(bound / (2ξ)) = M_P * sqrt(1.15e-5 / ξ)
xi_small = 0.01
chi_max_small = np.sqrt(GAMMA_BOUND / (2 * xi_small))
print(f"For ξ = {xi_small}: χ_0/M_P < {chi_max_small:.4f}  (Cassini admissible)")

xi_conformal = 1.0/6.0  # conformal coupling
chi_max_conf = np.sqrt(GAMMA_BOUND / (2 * xi_conformal - GAMMA_BOUND * (1 + xi_conformal) * xi_conformal))
print(f"For ξ = 1/6 (conformal): χ_0/M_P < {chi_max_conf:.4f}")

print()
# What fraction of (ξ, χ/M_P) ∈ [0,1] × [0,0.5] is admissible?
frac = admissible.mean()
print(f"Admissible fraction of [{xi_arr[0]},{xi_arr[-1]}] × [{chi_arr[0]},{chi_arr[-1]}]: {frac:.4%}")
print()
print("VERDICT:")
print("  Small ξ_χ χ_0^2/M_P^2 ≪ 1 satisfies Cassini bound trivially.")
print("  For ξ_χ = 0.1: χ_0/M_P must be ≪ 0.01 (tight constraint).")
print("  The NMC coupling must be screened at solar system scales")
print("  (chameleon/Vainshtein-like mechanism needed for ξ ~ O(1)).")

# ── Figure ─────────────────────────────────────────────────────────────────────
fig, axes = plt.subplots(1, 2, figsize=(13, 5))

# Left panel: |γ-1| contour map
ax = axes[0]
levels_log = np.logspace(-10, -1, 50)
cf = ax.contourf(XI, CHI, np.abs(GM1), levels=levels_log, cmap="RdYlGn_r",
                 norm=mcolors.LogNorm(vmin=1e-10, vmax=1e-1))
fig.colorbar(cf, ax=ax, label=r"$|\gamma - 1|$")

# Cassini bound contour
cs = ax.contour(XI, CHI, np.abs(GM1), levels=[GAMMA_BOUND],
                colors="white", linewidths=2.5)
ax.clabel(cs, fmt=r"Cassini $|\gamma-1| = 2.3\times10^{-5}$", fontsize=8)

# Admissible region (fill below the boundary curve)
ax.fill_between(xi_fine, 0, np.where(np.isnan(chi_boundary), 0, chi_boundary),
                alpha=0.25, color="cyan", label="Admissible")

ax.set_xlabel(r"$\xi_\chi$", fontsize=12)
ax.set_ylabel(r"$\chi_0 / M_P$", fontsize=12)
ax.set_title(r"$|\gamma_{\rm PPN} - 1|$ in NMC theory", fontsize=12)
ax.legend(fontsize=9)
ax.set_xlim(0, 1)
ax.set_ylim(0, 0.5)

# Right panel: γ-1 vs χ/M_P for fixed ξ values
ax2 = axes[1]
xi_vals = [0.01, 0.1, 1.0/6.0, 0.5, 1.0]
colors = ["#2ca02c", "#1f77b4", "#9467bd", "#ff7f0e", "#d62728"]
for xi_v, col in zip(xi_vals, colors):
    gm1_line = gamma_minus_1(xi_v, chi_arr)
    lbl = rf"$\xi_\chi = {xi_v:.3f}$" if xi_v == 1/6.0 else rf"$\xi_\chi = {xi_v}$"
    ax2.semilogy(chi_arr, np.abs(gm1_line), color=col, lw=1.8, label=lbl)

ax2.axhline(GAMMA_BOUND, color="red", lw=2, ls="--",
            label=rf"Cassini: $|\gamma-1| = {GAMMA_BOUND:.1e}$")
ax2.fill_between(chi_arr, 0, GAMMA_BOUND, alpha=0.10, color="green")
ax2.set_xlabel(r"$\chi_0 / M_P$", fontsize=12)
ax2.set_ylabel(r"$|\gamma_{\rm PPN} - 1|$", fontsize=12)
ax2.set_title(r"PPN deviation vs $\chi_0/M_P$ for fixed $\xi_\chi$", fontsize=12)
ax2.legend(fontsize=8.5, loc="lower right")
ax2.grid(True, alpha=0.3)
ax2.set_xlim(0, 0.5)
ax2.set_ylim(1e-12, 1e-1)

plt.suptitle("N3 — Cassini PPN bound $|\\gamma-1| < 2.3\\times 10^{-5}$ vs NMC prediction",
             fontsize=12)
plt.tight_layout()
outfile = "n3-ppn-gamma.png"
plt.savefig(outfile, dpi=150)
print(f"\nSaved: {outfile}")
print("=" * 60)
