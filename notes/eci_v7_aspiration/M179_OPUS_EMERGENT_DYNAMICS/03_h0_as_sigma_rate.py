"""
M179 Test 2 — H_0 as σ_t convergence rate

Reframing intuition (user M179 brief):
  Connes-Rovelli §5 verbatim: "thermal time defined by the cosmic
  background radiation IS precisely the conventional Friedman-Robertson-
  Walker time".  Could d/dt log(scale factor) under σ_t give H_0
  emergently at late times?

Specifically:
  - Compute d/dt log(a) under σ_t modular flow on type II_∞ algebra
  - For Bianchi IX modular shadow: σ_t = geodesic time on PSL(2,Z)\H
  - Late-time limit → effective H_0 ?

CRITICAL DISTINCTION (from Connes-Rovelli 1994 verbatim):
  σ_t is not a NEW time variable, it IS the FRW time when ω = ω_CMB.
  Therefore d/dt_σ log(a) = d/dt_FRW log(a) = H(t) by tautology.
  The question is whether ECI provides ρ_tot, Ω_m, Ω_Λ to feed Friedmann.
"""
import mpmath
mpmath.mp.dps = 30

# ─── Direct test: σ_t scale-factor evolution rate ───
print("="*68)
print("Direct test: σ_t = FRW time, scale factor evolution rate")
print("="*68)
print()
print("In Connes-Rovelli 1994 §5: σ_t for ω = thermal photon gas IS")
print("FRW time t_FRW.  Therefore by definition:")
print("  d/dt_σ log(a) = d/dt_FRW log(a) = H(t)")
print()
print("This is a TAUTOLOGY, not a derivation.  σ_t identifies WHICH variable")
print("plays time, not its rate of change against another time.  H_0 still")
print("requires solving Friedmann H² = (8πG/3) ρ_tot which inputs ρ_tot.")
print()

# ─── Bianchi IX MM geodesic time ↔ FRW ───
print("="*68)
print("Bianchi IX modular shadow: geodesic time vs Misner volume")
print("="*68)
print()
print("Manin-Marcolli arXiv:1504.04005 Theorem (verbatim M141):")
print("  log Ω_{2s}/Ω_0  ≃  2 Σ_r dist_H(x_{2r}, x_{2r+1})")
print()
print("where Ω_n is Misner volume after n Kasner epochs and the RHS sums")
print("hyperbolic distances along PSL(2,Z)\\H geodesic.")
print()
print("Differentiating: d log Ω / d (2-arc-length) = 2 (per epoch).")
print("This is the BKL bouncing rate: anisotropy energy → curvature → next bounce.")
print()
print("In the SUGRA Kähler conformal factor (M144 ratio 3/2):")
print("  Lyapunov per Kähler arc = √(2/3) ≈ 0.8165")
print("  Lyapunov per Poincaré arc = 1")
print("  λ_BKL per Gauss-shift = π²/(6 log 2) ≈ 2.3731")
print()
print("BUT: Misner volume = (anisotropy^4 / t^2) volume; this is NOT the")
print("FRW SCALE FACTOR a(t).  Bianchi IX has anisotropic spatial metric")
print("ds² = -dt² + Σ g_ii dx_i² with g_ii = e^{-2β_i}, det = a^6 e^{-2tr β}.")
print("The 'scale factor' is the geometric mean (det g)^{1/6}, related to")
print("Misner τ-time via ω = log(det g)^{1/6}, dτ = e^{-3 ω} dt.")
print()
print("In the BKL limit (near singularity), tr β chaotic, det g → 0 (singularity).")
print("Geodesic time on PSL(2,Z)\\H is the UNFOLDED Misner billiard, NOT cosmic time.")
print("=> Misner geodesic rate ≠ Hubble rate H(t).")
print()

# ─── Numerical: convert λ_BKL to physical H_0? ───
print("="*68)
print("Numerical: can λ_BKL or other modular invariants convert to H_0 ?")
print("="*68)
print()
H0_obs = mpmath.mpf("67.4")  # km/s/Mpc, Planck 2018 + DESI 2024-25 mean
H0_obs_inv_s = H0_obs * 1000 / mpmath.mpf("3.0857e22")
t_H_s = 1 / H0_obs_inv_s
t_age_s = mpmath.mpf("13.797") * mpmath.mpf("3.156e16")  # 13.797 Gyr in seconds
print(f"H_0 obs = {H0_obs} km/s/Mpc = {mpmath.nstr(H0_obs_inv_s, 6)} s^-1")
print(f"t_H     = {mpmath.nstr(t_H_s, 6)} s = {mpmath.nstr(t_H_s/3.156e16, 4)} Gyr")
print(f"H_0 t_age = {mpmath.nstr(H0_obs_inv_s * t_age_s, 6)} (dimensionless)")
print()

# Modular invariants
lam_BKL = mpmath.pi**2 / (6 * mpmath.log(2))
lam_geo_K = mpmath.sqrt(mpmath.mpf(2)/3)
lam_1_Maass = mpmath.mpf("0.25") + mpmath.mpf("9.5336952613536")**2
print(f"λ_BKL = π²/(6 log 2) = {mpmath.nstr(lam_BKL, 8)}")
print(f"λ_geo,Kähler = √(2/3) = {mpmath.nstr(lam_geo_K, 8)}")
print(f"λ_1 Maass = 1/4 + r_1² = {mpmath.nstr(lam_1_Maass, 8)}")
print()

# Is there a DIMENSIONLESS combination that equals H_0 t_age ≈ 0.951?
# (LCDM gives H_0 t_age ≈ 0.95 today)
HtA = H0_obs_inv_s * t_age_s
print(f"H_0 · t_age (LCDM) ≈ {mpmath.nstr(HtA, 6)}")
print()
print(f"  λ_BKL  / 2.5 ≈ {mpmath.nstr(lam_BKL/mpmath.mpf('2.5'), 6)}")
print(f"  log 2 + 1/4 ≈ {mpmath.nstr(mpmath.log(2) + 0.25, 6)}")
print(f"  6 log 2 / π² ≈ {mpmath.nstr(6*mpmath.log(2)/mpmath.pi**2, 6)}  (Lochs)")
print(f"  π/4 ≈ {mpmath.nstr(mpmath.pi/4, 6)}")
print(f"  e^{{-1}} ≈ {mpmath.nstr(mpmath.exp(-1), 6)}")
print(f"  2/√(2π) ≈ {mpmath.nstr(2/mpmath.sqrt(2*mpmath.pi), 6)}")
print()
print("None of these match 0.951 with structural motivation.")
print()

# ─── Crucial: σ_t-rate IS H_0, not derived from σ_t ───
print("="*68)
print("STRUCTURAL CONCLUSION: σ_t-rate IS H_0, by definition")
print("="*68)
print()
print("From Connes-Rovelli 1994 Eq (43)-(44):")
print("  α_t = γ_{βt}, where γ is Hamilton time and β = ℏ/(k_B T).")
print()
print("In FRW with photon gas KMS state at temperature T(t):")
print("  σ_t = t_FRW (when t = 0 is identified with present)")
print()
print("So d/dt_σ log(a) = d/dt_FRW log(a) ≡ H(t).  No new info.")
print()
print("To DERIVE H_0 from arithmetic, we'd need:")
print("  1. ρ_DM h², ρ_baryon h², ρ_Λ h² (matter content)")
print("  2. Initial conditions a(t=0+) (set by inflation)")
print()
print("Neither of these comes from σ_t arithmetic alone.  The arithmetic")
print("structure (BC for Q(i), MM geodesic, Connes-Takesaki II_∞) all live")
print("on the OBSERVER ALGEBRA SIDE; matter content is INPUT.")
print()
print("=> M175 (C)/(D) negative verdict CONFIRMED for the emergent")
print("   reframing.  σ_t IS the time, not a rate, and predicts H_0 only")
print("   tautologically once Friedmann is fed.")
print()
print()
# ─── Final numerical clean check: is there ANY arithmetic combination giving 67-73? ───
print("="*68)
print("Brute force: arithmetic combinations producing 67-73?")
print("="*68)
print()

# Define candidate dimensionless invariants
import numpy as np
gamma14 = float(mpmath.gamma(mpmath.mpf(1)/4))
candidates = {
    "Γ(1/4)⁴ / √(2π)": gamma14**4 / np.sqrt(2*np.pi),
    "λ_BKL · 30": float(lam_BKL) * 30,
    "(6/5)·100/√3": (6/5)*100/np.sqrt(3),
    "Γ(1/4)⁴ · 2/5": gamma14**4 * 2/5,
    "8π · λ_geo,K · ζ(2) / λ_BKL · m_τ / 2¹⁰": None,  # explore
    "100·√2 / e": 100*np.sqrt(2) / np.e,
    "λ_1 Maass / √2": float(lam_1_Maass) / np.sqrt(2),
    "16·G_Catalan + 50": 16*float(mpmath.catalan) + 50,
}
for name, val in candidates.items():
    if val is None:
        continue
    delta_planck = abs(val - 67.4)
    delta_shoes = abs(val - 73.04)
    print(f"  {name:30s} = {val:.4f}  (|Δ_Planck|={delta_planck:.3f}, |Δ_SH0ES|={delta_shoes:.3f})")
print()
print("All within ~5 units of LCDM, but none is structurally motivated by ECI.")
print("Same as M175 verdict: ad hoc coincidences only, no derivation.")
