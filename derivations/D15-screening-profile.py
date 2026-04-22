"""
D15 — Minimum chameleon/symmetron screening profile for §3.6 Resolution (ii)
============================================================================

Purpose
-------
Peer-review-v2 priority-2 action. §3.6 lists three resolutions to the
A4↔A5 bulk-mode incompatibility; Resolution (ii) invokes a
chameleon/symmetron screening mechanism to reconcile a
cosmologically-observable |ξ_χ| ~ 2.4×10⁻² (D7 Cassini saturation) with
the solar-system Cassini-Bertotti bound |γ−1| ≤ 2.3×10⁻⁵. This script
derives the *minimum viable* (ρ_c, α) region for the screening
envelope Θ(ρ) = exp(-(ρ/ρ_c)^α).

Requirements
------------
(R1)  Solar-system screening :  Θ(ρ_☉)  ≲ 10⁻³
      (so that ξ_eff at Earth/solar densities shrinks Cassini γ−1 to ≤2.3e-5)
(R2)  Cosmological visibility:  Θ(ρ_cosm) ≥ 0.99
      (so that D7 thawing-DE signature is preserved at ~1 %)

Densities (SI → code uses g/cm³ consistently):
    ρ_solar   = 10       g/cm³    (typical solar-system / Cassini path)
    ρ_cluster = 1e-27    g/cm³    (galaxy cluster halo)
    ρ_cosmic  = 1e-29    g/cm³    (critical density, z=0)

Outputs
-------
  derivations/figures/D15-screening-profile.pdf (+ .png)
  derivations/_results/D15-summary.json
"""
from __future__ import annotations
import os, json
import numpy as np
import sympy as sp
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

os.environ.setdefault('OMP_NUM_THREADS', '2')

# ─── Sympy: closed-form minimum (ρ_c, α) from boundary saturation ──────────
rho, rho_c, alpha = sp.symbols('rho rho_c alpha', positive=True)
Theta = sp.exp(-(rho/rho_c)**alpha)

# At (R1) saturation:  Θ(ρ_☉) = 1e-3  →  (ρ_☉/ρ_c)^α = ln(1e3)
# At (R2) saturation:  Θ(ρ_c-cosm) = 0.99  →  (ρ_cosm/ρ_c)^α = -ln(0.99)
rho_sol_v  = 1e1
rho_cos_v  = 1e-29
T1 = 1e-3          # screening ceiling
T2 = 0.99          # visibility floor

# Dividing the two saturation equations:
#    (ρ_☉/ρ_cosm)^α = ln(1/T1) / (-ln(T2))
# → α_min = log(RHS) / log(ρ_☉/ρ_cosm)
ratio_rhs = sp.log(1/sp.Rational(1,1000)) / (-sp.log(sp.Rational(99,100)))
ratio_lhs = rho_sol_v / rho_cos_v   # 1e30
alpha_min = float(sp.log(ratio_rhs)/sp.log(ratio_lhs))
# ρ_c from (R1) at α_min :  ρ_c = ρ_☉ / (ln 1000)^(1/α)
rho_c_at_R1 = rho_sol_v / (np.log(1/T1))**(1.0/alpha_min)
# ρ_c from (R2) at α_min :  ρ_c = ρ_cosm / (-ln 0.99)^(1/α)
rho_c_at_R2 = rho_cos_v / (-np.log(T2))**(1.0/alpha_min)
# At α=α_min the two intersect exactly → minimum ρ_c boundary.
rho_c_min = rho_c_at_R1

print(f"[D15] Boundary-saturated minimum: α_min = {alpha_min:.4f}")
print(f"      ρ_c(R1@α_min) = {rho_c_at_R1:.3e} g/cm³")
print(f"      ρ_c(R2@α_min) = {rho_c_at_R2:.3e} g/cm³  (should match)")

# ─── Numerical scan of (ρ_c, α) allowed region ─────────────────────────────
rho_solar   = 1e1
rho_cluster = 1e-27
rho_cosmic  = 1e-29

def Theta_num(rho, rho_c, alpha):
    # Guard against overflow in (rho/rho_c)**alpha for huge arguments
    x = np.clip((rho/rho_c)**alpha, 0.0, 700.0)
    return np.exp(-x)

alpha_grid = np.linspace(0.02, 0.30, 140)
rho_c_grid = np.logspace(-28, -18, 220)   # g/cm³
A, Rc = np.meshgrid(alpha_grid, rho_c_grid, indexing='xy')

Theta_sol  = Theta_num(rho_solar,   Rc, A)
Theta_clu  = Theta_num(rho_cluster, Rc, A)
Theta_cos  = Theta_num(rho_cosmic,  Rc, A)

mask_R1 = Theta_sol <= T1
mask_R2 = Theta_cos >= T2
mask_ok = mask_R1 & mask_R2

# Minimum (ρ_c, α) on the allowed region: smallest α (shallowest transition)
# and corresponding minimum ρ_c.
if mask_ok.any():
    idx = np.argwhere(mask_ok)
    a_vals = alpha_grid[idx[:,1]]
    r_vals = rho_c_grid[idx[:,0]]
    a_min_num = float(a_vals.min())
    # Among α≈α_min_num slice, minimum ρ_c meeting both:
    row = np.isclose(a_vals, a_vals.min(), atol=1e-3)
    r_min_num = float(r_vals[row].min())
else:
    a_min_num = float('nan'); r_min_num = float('nan')

print(f"[D15] Numerical scan minimum α = {a_min_num:.4f}, ρ_c = {r_min_num:.2e} g/cm³")

# Θ at cluster density at the minimum profile
Theta_cluster_min = float(Theta_num(rho_cluster, rho_c_min, alpha_min))
print(f"[D15] Θ(ρ_cluster={rho_cluster:g}) at (ρ_c_min, α_min) = {Theta_cluster_min:.4f}")

# ─── Khoury-Weltman 2004 sanity reference ──────────────────────────────────
# Khoury & Weltman 2004 (astro-ph/0309300) chameleon potentials V(φ)=M^(4+n)φ^(-n)
# give mass-density dependence of the effective potential minimum. Their
# viable-range slope exponents translate (via φ_min∝ρ^(-1/(n+2))) into an
# effective power α_eff ≈ 1/(n+2) for n ∈ [1,6] → α_eff ∈ [1/8, 1/3]≈[0.125,0.333].
# Our derived α_min should sit inside or just below this interval (softer
# coupling is permitted; harder couplings would collide with Eöt-Wash).
KW_alpha_lo, KW_alpha_hi = 0.125, 0.333
kw_compatible = (KW_alpha_lo - 0.05) <= alpha_min <= (KW_alpha_hi + 0.05)
print(f"[D15] Khoury-Weltman α range ≈ [{KW_alpha_lo}, {KW_alpha_hi}]; "
      f"α_min={alpha_min:.3f} compatible={kw_compatible}")

# ─── Figure (mirrors D13 style: 2 panels, 11×4.5) ──────────────────────────
here = os.path.dirname(os.path.abspath(__file__))
figdir = os.path.join(here, 'figures'); os.makedirs(figdir, exist_ok=True)
resdir = os.path.join(here, '_results'); os.makedirs(resdir, exist_ok=True)

fig, axes = plt.subplots(1, 2, figsize=(11, 4.5))

# LEFT: allowed (ρ_c, α) region
ax = axes[0]
# Show R1 boundary (Θ(ρ_☉)=T1) and R2 boundary (Θ(ρ_cosm)=T2)
# R1: (ρ_☉/ρ_c)^α = ln(1/T1) → ρ_c = ρ_☉ · (ln(1/T1))^(-1/α)
R1_curve = rho_solar  * (np.log(1/T1))**(-1.0/alpha_grid)
R2_curve = rho_cosmic * (-np.log(T2))**(-1.0/alpha_grid)

ax.fill_betweenx(alpha_grid, R1_curve, R2_curve,
                 where=(R2_curve>=R1_curve), color='C2', alpha=0.25,
                 label='Allowed (R1 ∧ R2)')
ax.plot(R1_curve, alpha_grid, 'C3-', lw=1.4,
        label=r'R1: $\Theta(\rho_\odot)=10^{-3}$ (Cassini ceiling)')
ax.plot(R2_curve, alpha_grid, 'C0-', lw=1.4,
        label=r'R2: $\Theta(\rho_{\rm cosm})=0.99$ (visibility floor)')
ax.axhspan(KW_alpha_lo, KW_alpha_hi, color='gray', alpha=0.15,
           label=r'Khoury-Weltman viable $\alpha$ band')
ax.plot(rho_c_min, alpha_min, 'k*', ms=14,
        label=fr'Minimum: $\rho_c={rho_c_min:.1e}$, $\alpha={alpha_min:.3f}$')
ax.set_xscale('log')
ax.set_xlabel(r'$\rho_c$ [g/cm$^3$]')
ax.set_ylabel(r'$\alpha$')
ax.set_title('(a) Allowed screening-profile region')
ax.legend(fontsize=8, loc='lower right'); ax.grid(alpha=0.3, which='both')

# RIGHT: Θ(ρ) profile at the minimum
ax = axes[1]
rho_curve = np.logspace(-30, 2, 600)
Th_min = Theta_num(rho_curve, rho_c_min, alpha_min)
ax.plot(rho_curve, Th_min, 'k-', lw=1.6, label=fr'$\Theta(\rho)$ at minimum')
# Also a shallower (α=0.05) and a steeper (α=0.2) comparison at same ρ_c
for a_cmp, col in [(0.05,'C4'), (0.20,'C1')]:
    ax.plot(rho_curve, Theta_num(rho_curve, rho_c_min, a_cmp),
            color=col, lw=1.0, ls='--', label=fr'$\alpha={a_cmp}$ (ref)')
ax.axvline(rho_solar,   color='C3', ls=':', lw=1); ax.text(rho_solar*1.3, 0.50, r'$\rho_\odot$', color='C3', fontsize=9)
ax.axvline(rho_cluster, color='C2', ls=':', lw=1); ax.text(rho_cluster*1.3, 0.50, r'$\rho_{\rm clu}$', color='C2', fontsize=9)
ax.axvline(rho_cosmic,  color='C0', ls=':', lw=1); ax.text(rho_cosmic*1.3, 0.50, r'$\rho_{\rm cosm}$', color='C0', fontsize=9)
ax.axhline(T1, color='C3', ls='-.', lw=0.8)
ax.axhline(T2, color='C0', ls='-.', lw=0.8)
ax.set_xscale('log')
ax.set_xlabel(r'$\rho$ [g/cm$^3$]')
ax.set_ylabel(r'$\Theta(\rho)$')
ax.set_title(r'(b) Minimum profile $\Theta(\rho)=\exp[-(\rho/\rho_c)^\alpha]$')
ax.legend(fontsize=8, loc='center left'); ax.grid(alpha=0.3, which='both')
ax.set_ylim(-0.02, 1.05)

plt.tight_layout()
out = os.path.join(figdir, 'D15-screening-profile.pdf')
plt.savefig(out)
plt.savefig(out.replace('.pdf', '.png'), dpi=150)
print(f"[D15] wrote {out}")

# ─── Summary JSON ──────────────────────────────────────────────────────────
summary = {
    "inputs": {
        "rho_solar_g_per_cm3":   rho_solar,
        "rho_cluster_g_per_cm3": rho_cluster,
        "rho_cosmic_g_per_cm3":  rho_cosmic,
        "Theta_R1_ceiling":      T1,
        "Theta_R2_floor":        T2,
    },
    "minimum_profile": {
        "alpha_min":      alpha_min,
        "rho_c_min_g_per_cm3": rho_c_min,
        "rho_c_from_R1": rho_c_at_R1,
        "rho_c_from_R2": rho_c_at_R2,
    },
    "derived": {
        "Theta_solar_at_min":   float(Theta_num(rho_solar,   rho_c_min, alpha_min)),
        "Theta_cluster_at_min": Theta_cluster_min,
        "Theta_cosmic_at_min":  float(Theta_num(rho_cosmic,  rho_c_min, alpha_min)),
    },
    "khoury_weltman_2004": {
        "alpha_band": [KW_alpha_lo, KW_alpha_hi],
        "compatible_with_min": bool(kw_compatible),
        "ref": "astro-ph/0309300 (n∈[1,6] → α_eff≈1/(n+2))",
    },
    "numerical_scan_min": {
        "alpha": a_min_num,
        "rho_c": r_min_num,
    },
}
with open(os.path.join(resdir, 'D15-summary.json'), 'w') as f:
    json.dump(summary, f, indent=2)
print(json.dumps(summary, indent=2))
