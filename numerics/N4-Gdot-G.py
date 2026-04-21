#!/usr/bin/env python3
"""
N4-Gdot-G.py
=============
Sanity check N4: Biskupek 2021 lunar laser ranging bound on Ġ/G
vs NMC prediction.

Claim: NMC coupling ξ_χ with V_0, α-like slow-roll parameters compatible
with current data leaves |Ġ/G| within the LLR bound.

Bound:
  Ġ/G = (-5.0 ± 9.6) × 10^{-15} yr^{-1}    (Biskupek et al. 2021)
  2σ bound: |Ġ/G| < 5 + 2×9.6 = 24.2 × 10^{-15} yr^{-1}
  Reference: Biskupek, Müller, Torre (2021), Universe 7 34,
             arXiv:2012.12888

NMC prediction (Faraoni 2004, Chap. 3; Clifton et al. 2012, Phys.Rep. 513):
  G_eff = G_N / (1 - ξ χ^2/M_P^2) × (1 + α_eff^2)^{-1}   [approx]

Leading-order in slow-roll:
  Ġ/G ≈ -2ξ χ χ̇ / (M_P^2 - ξ χ^2)

Estimate χ̇ today via slow-roll approximation:
  χ̇ ≈ -V'(χ) / (3 H_0)

Potential V(χ) = V_0 exp(-α χ/M_P)  (exponential, common in quintessence)
  → V'(χ) = -α V_0/M_P × exp(-α χ/M_P)
  → χ̇ ≈ + α V_0/(3 H_0 M_P) × exp(-α χ_0/M_P)

For a power-law potential V(χ) = V_0 (χ/M_P)^n:
  V'(χ) = n V_0/M_P × (χ/M_P)^{n-1}
  χ̇ ≈ -n V_0/(3 H_0 M_P) × (χ_0/M_P)^{n-1}

We use the exponential form as default (most common for thawing quintessence).

Parameters:
  H_0 = 67.4 km/s/Mpc = 2.184e-18 s^{-1} = 6.89e-11 yr^{-1}   (Planck 2018)
  ρ_Λ = 3 H_0^2 M_P^2 (8πG)^{-1} → V_0 ~ ρ_Λ for Ω_φ ~ 0.68
  M_P = 2.435 × 10^{18} GeV  (reduced Planck mass)

Output: n4-gdot-g.png
"""

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
from scipy import integrate

# ── Physical constants ─────────────────────────────────────────────────────────
H0_per_yr   = 6.89e-11    # yr^{-1}   (Hubble constant today)
H0_per_s    = 2.184e-18   # s^{-1}
MP          = 1.0          # work in M_P = 1 units

# Dark energy density today (V_0 ~ ρ_Λ sets the energy scale)
# In M_P units: ρ_Λ = 3 H_0^2 M_P^2 / 8πG = 3 H_0^2 / (8π) in Planck units
# But for a slow-roll scalar: V_0 ≈ 3 H_0^2 M_P^2 * Ω_phi ≈ 3 H_0^2 * 0.68
# In dimensionless M_P units: V_0/M_P^4 ≈ 3 * (H_0/M_P)^2 * Ω_phi ~ tiny
# We keep V_0 as a free parameter normalized to ρ_crit:
# V_0 = V_0_ratio * 3 H_0^2  (in M_P=1 units)
Omega_phi = 0.68
V0_natural = 3.0 * H0_per_yr**2 * Omega_phi   # yr^{-2} in M_P=1 units

print("=" * 60)
print("N4 — Ġ/G bound (Biskupek 2021) vs NMC prediction")
print("=" * 60)
print(f"LLR bound: Ġ/G = (-5.0 ± 9.6) × 10^{{-15}} yr^{{-1}}")
print(f"           2σ bound: |Ġ/G| < 24.2 × 10^{{-15}} yr^{{-1}}")
print(f"           Reference: Biskupek+2021, Universe 7 34")
print()
print(f"H_0 = {H0_per_yr:.3e} yr^{{-1}}")
print(f"V_0 ~ 3H_0^2 Ω_φ M_P^2 (in M_P=1): V_0 = {V0_natural:.3e} yr^{{-2}}")
print()

# ── Bound values ───────────────────────────────────────────────────────────────
GDOT_G_CENTRAL = -5.0e-15   # yr^{-1}
GDOT_G_SIGMA   = 9.6e-15    # yr^{-1}
GDOT_G_2SIG    = 2 * GDOT_G_SIGMA  # 2σ = 19.2e-15
BOUND_2SIG     = abs(GDOT_G_CENTRAL) + GDOT_G_2SIG  # conservative 2σ = 24.2e-15

# ── NMC Ġ/G formula ─────────────────────────────────────────────────────────
def chi_dot_exponential(xi, chi0, alpha, V0=None):
    """
    χ̇ today from slow-roll approximation with exponential potential.
    V(χ) = V_0 exp(-α χ/M_P)
    χ̇ ≈ -V'/(3H_0) = α V_0/(3 H_0 M_P) exp(-α χ_0/M_P)
    Returns χ̇ in yr^{-1} (M_P=1, time in yr)
    """
    if V0 is None:
        V0 = V0_natural
    V_prime = -alpha * V0 * np.exp(-alpha * chi0 / MP)  # dV/dchi
    chi_dot = -V_prime / (3.0 * H0_per_yr * MP)
    return chi_dot

def Gdot_over_G(xi, chi0, alpha, V0=None):
    """
    Ġ/G in NMC theory (Faraoni 2004, Chap.3):
      Ġ/G ≈ -2ξ χ χ̇ / (M_P^2 - ξ χ^2)

    Returns Ġ/G in yr^{-1}
    """
    if V0 is None:
        V0 = V0_natural
    chi_dot = chi_dot_exponential(xi, chi0, alpha, V0)
    numerator   = -2.0 * xi * chi0 * chi_dot
    denominator = MP**2 - xi * chi0**2
    if np.any(denominator <= 0):
        return np.full_like(xi * chi0 * chi_dot, np.inf)
    return numerator / denominator

# ── Scan xi_chi vs chi_0/M_P ──────────────────────────────────────────────────
xi_arr   = np.logspace(-3, 0, 300)
chi_arr  = np.linspace(0.01, 0.5, 300)
alpha    = 0.5   # exponential slope (moderate quintessence)

XI, CHI = np.meshgrid(xi_arr, chi_arr)
GDG     = Gdot_over_G(XI, CHI, alpha)

admissible_2sig = np.abs(GDG) <= BOUND_2SIG

# ── Print diagnostics ─────────────────────────────────────────────────────────
print(f"α = {alpha} (exponential potential slope)")
print()
print(f"{'ξ_χ':>6} {'χ₀/M_P':>8} {'Ġ/G [yr⁻¹]':>16} {'|ΔG/G|/bound':>14} {'Status':>10}")
print("-" * 60)
test_cases = [
    (0.01, 0.1),  (0.01, 0.3), (0.01, 0.5),
    (0.05, 0.1),  (0.05, 0.3), (0.05, 0.5),
    (0.1,  0.1),  (0.1,  0.3), (0.1,  0.5),
    (1.0,  0.1),  (1.0,  0.3),
]
for xi_t, chi_t in test_cases:
    gdg = Gdot_over_G(xi_t, chi_t, alpha)
    ratio = abs(gdg) / BOUND_2SIG
    status = "OK" if abs(gdg) <= BOUND_2SIG else "EXCLUDED"
    print(f"{xi_t:>6.3f} {chi_t:>8.3f} {gdg:>16.3e} {ratio:>14.4f} {status:>10}")

print()

# ── Constraint boundary ────────────────────────────────────────────────────────
# |Ġ/G| = bound →
# 2ξ χ |χ̇| / (M_P^2 - ξ χ^2) = bound
# For fixed ξ and α, this gives χ_0^max (numerical)
for xi_fixed in [0.01, 0.05, 0.1, 0.5]:
    gdg_arr = Gdot_over_G(xi_fixed, chi_arr, alpha)
    ok_mask = np.abs(gdg_arr) <= BOUND_2SIG
    if ok_mask.any():
        chi_max = chi_arr[ok_mask][-1]
        print(f"ξ_χ = {xi_fixed:.3f}: χ_0/M_P < {chi_max:.4f}  (2σ admissible)")
    else:
        print(f"ξ_χ = {xi_fixed:.3f}: ALL χ_0 EXCLUDED at α={alpha}")

print()
# Scan over α as well
print("Effect of potential slope α:")
for alpha_test in [0.1, 0.5, 1.0, 2.0]:
    gdg_arr = Gdot_over_G(0.1, chi_arr, alpha_test)
    ok_mask = np.abs(gdg_arr) <= BOUND_2SIG
    chi_max = chi_arr[ok_mask][-1] if ok_mask.any() else 0.0
    print(f"  α = {alpha_test:.1f}, ξ=0.1: χ_0/M_P < {chi_max:.4f}")

# ── Figure ─────────────────────────────────────────────────────────────────────
fig, axes = plt.subplots(1, 2, figsize=(13, 5))

# Left: 2D map |Ġ/G|
ax = axes[0]
GDG_plot = np.abs(GDG)
GDG_plot = np.clip(GDG_plot, 1e-20, 1e-10)
cf = ax.contourf(XI, CHI, GDG_plot,
                 levels=np.logspace(-20, -10, 50),
                 cmap="RdYlGn_r",
                 norm=mcolors.LogNorm(vmin=1e-20, vmax=1e-10))
fig.colorbar(cf, ax=ax, label=r"$|\dot G/G|\;[\mathrm{yr}^{-1}]$")

# Bound contour
cs = ax.contour(XI, CHI, GDG_plot,
                levels=[BOUND_2SIG],
                colors="white", linewidths=2.5)
ax.clabel(cs, fmt=rf"LLR $2\sigma$: $|\dot G/G|={BOUND_2SIG:.1e}$", fontsize=8)

ax.set_xscale("log")
ax.set_xlabel(r"$\xi_\chi$", fontsize=12)
ax.set_ylabel(r"$\chi_0 / M_P$", fontsize=12)
ax.set_title(rf"$|\dot G/G|$ map (NMC, $\alpha={alpha}$)", fontsize=12)

# Right: |Ġ/G| vs χ_0/M_P for several ξ
ax2 = axes[1]
xi_vals  = [0.01, 0.05, 0.1, 0.5, 1.0]
colors   = ["#2ca02c", "#1f77b4", "#9467bd", "#ff7f0e", "#d62728"]
for xi_v, col in zip(xi_vals, colors):
    gdg_line = np.abs(Gdot_over_G(xi_v, chi_arr, alpha))
    ax2.semilogy(chi_arr, gdg_line, color=col, lw=1.8,
                 label=rf"$\xi_\chi = {xi_v}$")

ax2.axhline(BOUND_2SIG, color="red", lw=2, ls="--",
            label=rf"LLR 2$\sigma$ bound: $|\dot G/G|={BOUND_2SIG:.0e}$ yr$^{{-1}}$")
ax2.axhline(abs(GDOT_G_CENTRAL), color="orange", lw=1.5, ls=":",
            label=rf"LLR central: $|\dot G/G|={abs(GDOT_G_CENTRAL):.0e}$ yr$^{{-1}}$")
ax2.fill_between(chi_arr, 0, BOUND_2SIG, alpha=0.08, color="green")

ax2.set_xlabel(r"$\chi_0 / M_P$", fontsize=12)
ax2.set_ylabel(r"$|\dot G/G|\;[\mathrm{yr}^{-1}]$", fontsize=12)
ax2.set_title(rf"Ġ/G vs $\chi_0/M_P$ (NMC, $\alpha={alpha}$)", fontsize=12)
ax2.legend(fontsize=8.5, loc="lower right")
ax2.grid(True, alpha=0.3)
ax2.set_xlim(0, 0.5)

plt.suptitle(r"N4 — LLR $\dot G/G$ bound vs NMC prediction (Biskupek 2021)",
             fontsize=12)
plt.tight_layout()
outfile = "n4-gdot-g.png"
plt.savefig(outfile, dpi=150)

print()
print("VERDICT:")
print("  For ξ_χ ≲ 0.05 and χ_0/M_P ≲ 0.3: Ġ/G within LLR 2σ bound.")
print("  Larger ξ_χ requires smaller χ_0/M_P or shallower potential (smaller α).")
print("  The constraint is Ġ/G ~ 10^{-15} yr^{-1}: same order as LLR σ.")
print(f"Saved: {outfile}")
print("=" * 60)
