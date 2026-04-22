"""
V8-chi-z-Cassini.py
-------------------
Validate the frozen-field approximation for the Cassini PPN bound in v5.

Physics:
  - Scalar χ satisfies thawing quintessence Klein-Gordon on FLRW.
  - Slow-roll regime: χ' ≈ -V_{χ,χ}/(3H) where prime = d/d(ln a).
  - Potential: V_χ = V_0 exp(-α χ/M_P)  →  V_{χ,χ} = -(α/M_P) V_χ
  - Thus: dχ/dN ≈ (α V_χ)/(3 H² M_P)   where dN = d ln a = -dz/(1+z)
  - H²(z) = H_0² [Ω_m (1+z)³ + Ω_Λ f_DE(z)]
  - f_DE(z) = exp(3 ∫_0^z [1+w(z')]/(1+z') dz') with CPL w(z)=w_0+w_a z/(1+z)

MAP cosmology (v5 D17 MCMC):
  w_0 = -0.881, w_a = -0.272, α = 0.095
  Ω_m = 0.3153, Ω_Λ = 0.6847, H_0 = 67.36 km/s/Mpc (Planck 2018 fiducial)

Units: M_P = 1 (reduced Planck mass normalization throughout).
χ_0 = M_P/10 = 0.1 at z = 0 (initial condition, thawing field starts frozen).

Decision threshold (pre-registered V8-Cassini-frozen-field):
  PASS        : |Δχ|/χ_0 < 5%   across full α ∈ (0, 0.1]
  BORDERLINE  : 5% ≤ |Δχ|/χ_0 < 15%
  FAIL        : |Δχ|/χ_0 ≥ 15%
"""

import numpy as np
from scipy.integrate import solve_ivp, quad
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import os

# =============================================================================
# Parameters
# =============================================================================
MP   = 1.0          # reduced Planck mass (natural units)
chi0 = MP / 10.0    # fiducial field value at z = 0

# MAP cosmology
w0   = -0.881
wa   = -0.272
alpha_map = 0.095

Om   = 0.3153
OL   = 0.6847       # = 1 - Om (flat)
H0   = 1.0          # set H_0 = 1; drops out in dχ/dz because H² appears in
                    # both numerator (via V_0 = 3 H_0² OL from normalisation)
                    # and denominator — see below.

# =============================================================================
# Dark energy equation-of-state integral for f_DE(z)
# f_DE(z) = exp(3 ∫_0^z [1+w(z')]/(1+z') dz')
# CPL: w(z) = w0 + wa * z/(1+z)  →  1+w(z) = (1+w0+wa) - wa/(1+z)
# Analytic: ∫_0^z (1+w)/(1+z') dz'
#          = (1+w0+wa) ln(1+z) + wa [1/(1+z) - 1]
# =============================================================================

def f_DE(z):
    """Dark energy density relative to z=0 value: rho_DE(z)/rho_DE(0)."""
    # CPL analytic integral
    exponent = 3.0 * ((1 + w0 + wa) * np.log(1 + z) + wa * (1.0/(1+z) - 1.0))
    return np.exp(exponent)

def H2(z):
    """H²(z)/H_0² — dimensionless squared Hubble parameter."""
    return Om * (1 + z)**3 + OL * f_DE(z)

# =============================================================================
# V_0 normalisation
# At z = 0, the dark energy component is Ω_Λ H_0² (in units H_0 = 1).
# The exponential potential contributes V_χ(z=0) = V_0 exp(-α χ_0/M_P).
# We impose 3 H_0² Ω_Λ = V_0 exp(-α χ_0/M_P) at z=0, treating dark energy as
# the quintessence field:
#   V_0 = 3 H_0² Ω_Λ / exp(-α χ_0/M_P) = 3 OL exp(α χ_0/M_P)
# (H_0 = 1, M_P = 1)
# =============================================================================

def V0_from_normalisation(alpha):
    return 3.0 * OL * np.exp(alpha * chi0 / MP)

def V_chi(chi, alpha):
    """Quintessence potential."""
    return V0_from_normalisation(alpha) * np.exp(-alpha * chi / MP)

def dV_dchi(chi, alpha):
    """V_{χ,χ} = dV/dχ."""
    return -alpha / MP * V_chi(chi, alpha)

# =============================================================================
# ODE: dχ/dz under slow-roll approximation
#
# dN = d ln a = -dz/(1+z)
# dχ/dN ≈ -V_{χ,χ}/(3 H²)   [slow-roll, Klein-Gordon]
# dχ/dz = dχ/dN * dN/dz = -V_{χ,χ}/(3 H²) * (-1/(1+z))
#        = V_{χ,χ}/(3 H²(z) (1+z))
#
# Note: V_{χ,χ} = -(α/M_P) V_χ < 0 (since α > 0, V_χ > 0)
# So dχ/dz = -(α/M_P) V_χ / (3 H²(z) (1+z))
#
# This drives χ to larger values as z increases (backward in time),
# consistent with thawing: field is displaced at early times and
# slowly rolls toward minimum.
#
# H²(z) here is H_0² * H2(z) = H2(z) (H_0 = 1)
# V_χ = V0 exp(-α χ/M_P) is in units H_0² M_P² (dimensionless here)
# =============================================================================

def ode_dchi_dz(z, chi, alpha):
    """Return dχ/dz under slow-roll approximation."""
    vchi = V_chi(chi, alpha)
    h2   = H2(z)
    # dχ/dN = -V_{χ,χ}/(3H²) = (α/MP) * V_χ/(3H²)
    # dχ/dz = dχ/dN * (-1/(1+z))^{-1} = -dχ/dN / (1+z)
    # BUT: dN = -dz/(1+z) → dχ/dz = dχ/dN * (-1/(1+z))  ← sign
    # Let me be explicit:
    #   z increases → a decreases → N decreases
    #   dN/dz = -1/(1+z)
    #   dχ/dz = (dχ/dN) * (dN/dz) = [-V_{χ,χ}/(3H²)] * [-1/(1+z)]
    #          = V_{χ,χ} / (3 H²(z) (1+z))
    #          = -(α/MP) V_χ / (3 H²(z) (1+z))     since V_{χ,χ} = -(α/MP)V_χ
    return -(alpha / MP) * vchi / (3.0 * h2 * (1 + z))

# =============================================================================
# Slow-roll validity check: ε_SR = (χ')² / (2 H²) = (dχ/dN)²/(2H²)
# Slow-roll requires ε_SR ≪ 1 and |η_SR| = |χ''/(H χ')| ≪ 1
# Here we just check ε_SR = (V_{χ,χ})²/(2 * (3H²)² * H²)
# More practically, check |dχ/dN| * α/(H) << 1
# =============================================================================

def slow_roll_epsilon(z, chi, alpha):
    """ε_SR = (1/2)(dχ/dN / MP)² — slow-roll parameter."""
    vchi = V_chi(chi, alpha)
    h2   = H2(z)
    dchi_dN = (alpha / MP) * vchi / (3.0 * h2)   # |dχ/dN|, positive value
    return 0.5 * (dchi_dN / MP)**2

# =============================================================================
# Main integration
# Integrate from z=0 (χ=χ_0) forward to z=0.3 using solve_ivp.
# We want to know χ at z=0.1.
# Note: we integrate in increasing z direction (0 → 0.3).
# =============================================================================

def integrate_chi(alpha, z_start=0.0, z_end=0.3, chi_init=chi0):
    """Integrate χ(z) from z_start to z_end with χ(z_start) = chi_init."""
    sol = solve_ivp(
        fun=lambda z, chi: [ode_dchi_dz(z, chi[0], alpha)],
        t_span=(z_start, z_end),
        y0=[chi_init],
        method="RK45",
        dense_output=True,
        rtol=1e-10,
        atol=1e-12,
    )
    return sol

# =============================================================================
# Run at MAP alpha
# =============================================================================
print("=" * 60)
print("V8-chi-z-Cassini: Frozen-field approximation validation")
print("=" * 60)
print(f"MAP cosmology: w_0={w0}, w_a={wa}, alpha={alpha_map}")
print(f"χ_0 = {chi0} M_P,  Ω_m={Om}, Ω_Λ={OL}")
print()

sol_map = integrate_chi(alpha_map)

# Evaluate at key redshifts
z_eval = np.array([0.0, 0.05, 0.10, 0.15, 0.20, 0.25, 0.30])
chi_eval = sol_map.sol(z_eval)[0]

chi_at_0   = chi_eval[0]
chi_at_01  = np.interp(0.1, z_eval, chi_eval)

delta_chi  = chi_at_01 - chi_at_0
frac_delta = abs(delta_chi) / chi0 * 100.0  # percent

print("χ(z) at key redshifts (MAP α=0.095):")
for z, c in zip(z_eval, chi_eval):
    eps = slow_roll_epsilon(z, c, alpha_map)
    print(f"  z={z:.2f}  χ={c:.8f}  ε_SR={eps:.3e}")

print()
print(f"χ(z=0)   = {chi_at_0:.8f}")
print(f"χ(z=0.1) = {chi_at_01:.8f}")
print(f"Δχ       = χ(z=0.1) - χ(z=0) = {delta_chi:.6e}")
print(f"|Δχ|/χ_0 = {frac_delta:.4f}%")
print()

# Decision
if frac_delta < 5.0:
    verdict = "PASS"
    explanation = "Frozen-field approx validated; v5 Cassini bound is honest."
elif frac_delta < 15.0:
    verdict = "BORDERLINE"
    explanation = f"Approx marginal ({frac_delta:.1f}%). Flag caveat."
else:
    verdict = "FAIL"
    explanation = "Frozen-field approx invalid. χ(z)-aware PPN bound needed."

print(f"VERDICT: {verdict}")
print(f"  {explanation}")
print()

# =============================================================================
# Sensitivity scan over alpha ∈ (0, 0.1]
# =============================================================================
alpha_range = np.linspace(0.005, 0.100, 40)
frac_delta_scan = []
chi_01_scan = []

for a in alpha_range:
    sol_a = integrate_chi(a)
    chi_z = sol_a.sol(np.array([0.0, 0.1]))[0]
    fd = abs(chi_z[1] - chi_z[0]) / chi0 * 100.0
    frac_delta_scan.append(fd)
    chi_01_scan.append(chi_z[1])

frac_delta_scan = np.array(frac_delta_scan)
max_frac = frac_delta_scan.max()
max_alpha = alpha_range[np.argmax(frac_delta_scan)]

print(f"Sensitivity scan α ∈ [0.005, 0.100]:")
print(f"  Max |Δχ|/χ_0 = {max_frac:.4f}% at α = {max_alpha:.3f}")
print(f"  At MAP α={alpha_map}: |Δχ|/χ_0 = {frac_delta:.4f}%")
if max_frac < 5.0:
    scan_verdict = "PASS (full α range)"
elif max_frac < 15.0:
    scan_verdict = "BORDERLINE (full α range)"
else:
    scan_verdict = "FAIL (full α range)"
print(f"  Scan verdict: {scan_verdict}")
print()

# =============================================================================
# Plot χ(z) from z=0 to z=0.3
# =============================================================================
z_plot = np.linspace(0.0, 0.30, 500)
chi_plot = sol_map.sol(z_plot)[0]

# Also plot scan envelopes (α_min and α_max)
sol_amin = integrate_chi(0.005)
sol_amax = integrate_chi(0.100)
chi_amin = sol_amin.sol(z_plot)[0]
chi_amax = sol_amax.sol(z_plot)[0]

fig, axes = plt.subplots(1, 2, figsize=(12, 5))

# --- Left panel: χ(z) trajectory ---
ax = axes[0]
ax.fill_between(z_plot, chi_amin, chi_amax, alpha=0.2, color="steelblue",
                label="α ∈ [0.005, 0.100] band")
ax.plot(z_plot, chi_plot, "b-", lw=2, label=f"MAP α={alpha_map}")
ax.axhline(chi0, color="k", ls="--", lw=1, label="χ₀ = M_P/10 (frozen)")
ax.axvline(0.10, color="red", ls=":", lw=1, alpha=0.7, label="z=0.1 (Cassini epoch)")
ax.set_xlabel("Redshift z", fontsize=12)
ax.set_ylabel("χ / M_P", fontsize=12)
ax.set_title("χ(z) under slow-roll (v5 MAP cosmology)", fontsize=12)
ax.legend(fontsize=9)
ax.grid(True, alpha=0.3)

# Annotate the field value at z=0.1
chi_annotate = float(sol_map.sol(np.array([0.10]))[0][0])
ax.annotate(
    f"χ(z=0.1)={chi_annotate:.6f}\n|Δχ|/χ₀={frac_delta:.3f}%",
    xy=(0.10, chi_annotate),
    xytext=(0.15, chi_annotate + (chi_amax[250]-chi_amin[250])*0.3),
    arrowprops=dict(arrowstyle="->", color="red"),
    fontsize=9, color="red"
)

# --- Right panel: |Δχ|/χ₀ vs α ---
ax2 = axes[1]
ax2.plot(alpha_range, frac_delta_scan, "b-o", ms=3, lw=1.5)
ax2.axhline(5.0, color="green", ls="--", lw=1.5, label="5% PASS threshold")
ax2.axhline(15.0, color="orange", ls="--", lw=1.5, label="15% BORDERLINE threshold")
ax2.axvline(alpha_map, color="red", ls=":", lw=1.5, label=f"MAP α={alpha_map}")
ax2.set_xlabel("α (potential slope)", fontsize=12)
ax2.set_ylabel("|Δχ|/χ₀  (%)", fontsize=12)
ax2.set_title("Frozen-field error vs α\n(z=0.1 → z=0)", fontsize=12)
ax2.legend(fontsize=9)
ax2.grid(True, alpha=0.3)

# Annotate max
ax2.annotate(
    f"Max: {max_frac:.3f}% at α={max_alpha:.3f}",
    xy=(max_alpha, max_frac),
    xytext=(max_alpha - 0.03, max_frac + 0.01),
    fontsize=9, color="darkred",
    arrowprops=dict(arrowstyle="->", color="darkred")
)

plt.tight_layout()
outpath = os.path.join(os.path.dirname(__file__), "V8-chi-z-Cassini.png")
plt.savefig(outpath, dpi=150, bbox_inches="tight")
print(f"Plot saved: {outpath}")

# =============================================================================
# Print summary for report
# =============================================================================
print()
print("=" * 60)
print("SUMMARY FOR REPORT")
print("=" * 60)
print(f"  χ(z=0)             = {chi_at_0:.8f} M_P")
print(f"  χ(z=0.1)           = {chi_at_01:.8f} M_P")
print(f"  Δχ = χ(0.1)-χ(0)  = {delta_chi:+.4e} M_P")
print(f"  |Δχ|/χ₀            = {frac_delta:.4f}%")
print(f"  Slow-roll ε_SR(0)  = {slow_roll_epsilon(0.0, chi0, alpha_map):.3e}")
print(f"  Slow-roll ε_SR(0.1)= {slow_roll_epsilon(0.1, chi_at_01, alpha_map):.3e}")
print(f"  Scan max |Δχ|/χ₀   = {max_frac:.4f}% (at α={max_alpha:.3f})")
print(f"  PRE-REGISTERED VERDICT: {verdict}")
print(f"  SCAN VERDICT:           {scan_verdict}")
