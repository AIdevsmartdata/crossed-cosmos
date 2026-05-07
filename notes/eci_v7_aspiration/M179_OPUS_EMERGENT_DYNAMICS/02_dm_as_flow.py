"""
M179 Test 1 — DM as DYNAMIC EMERGENT density Σ_t Ω_DM(t)

Reframing intuition (user M179 brief):
  M174 found static moduli-as-DM excluded.  Reframe as RG/thermodynamic
  flow Σ_t Ω_DM(t) on ECI substrate, evaluated at late time.

Possible mechanisms:
  (a) Connes-Takesaki σ_t on type II_∞ → entropy production → effective
      DM density.
  (b) Bianchi IX BKL bouncing → Lochs-Khinchin entropy → thermal DM.
  (c) Modular Laplacian eigenvalue tower {λ_n = 1/4 + r_n²} as "DM mass
      spectrum" via thermal occupation.
  (d) Granular nearest-neighbor on Farey/Stern-Brocot tessellation.

We test each rigorously against M174 obstructions:

OBSTRUCTION-1 (Banks-Dine): if DM is a particle, m < 30 TeV decays after
  BBN by gravitational coupling Γ ~ m³/M_Pl² unless lifetime > age universe.
OBSTRUCTION-2 (trans-Planckian): bare m_τ² ~ 10^10 M_Pl² (lepton)
  or 10^74 M_Pl² (quark).
OBSTRUCTION-3 (Lyman-α): Rogers-Peiris 2021 PRL m_a > 2e-20 eV.

The KEY QUESTION: does an EMERGENT dynamical reframing bypass these?
"""
import mpmath
mpmath.mp.dps = 30

# Constants
M_Pl = mpmath.mpf("2.435e18")            # GeV (reduced Planck mass)
M_Pl_eV = M_Pl * mpmath.mpf("1e9")
H0_eV = mpmath.mpf("1.44e-33")           # eV (today, ~67-70 km/s/Mpc)
T_CMB_eV = mpmath.mpf("2.348e-4")        # eV at z=0
T_eq_eV = mpmath.mpf("0.75")             # matter-radiation equality eV (~ z_eq 3400)
H_eq_eV = mpmath.mpf("3e-29")            # H at radiation-matter equality
H_inflation_eV = mpmath.mpf("1e13")      # GeV scale * 1e9 = 1e22 eV (illustrative)

print("="*68)
print("Mechanism (a): Connes-Takesaki σ_t as DM source")
print("="*68)
print()
print("In Connes-Rovelli 1994, σ_t for the photon-gas KMS state IS the")
print("Friedmann time.  Entropy production in σ_t = entropy of CMB photons +")
print("decoupled species.  For thermal DM a la WIMP this gives Ω_DM h² via")
print("Boltzmann freeze-out --- NO ARITHMETIC INPUT.")
print()
print("ECI specifically: σ_t for the type II_∞ algebra (M28+M101+M141+M148)")
print("acts on the WEDGE-COMPLEMENT observer algebra.  The wedge for FRW")
print("comoving observer is the past lightcone (Speranza dS_2 case is")
print("static patch).  This σ_t = γ_{βt} is just the comoving clock.")
print()
print("Crucial: σ_t carries [T]-dimension via β = 1/(k_B T).  The DM density")
print("a particle physicist computes is ρ_DM = (s_today/s_freeze) m_DM Y_∞")
print("with s the entropy density.  σ_t enters s only through the standard")
print("Boltzmann equation, NOT the arithmetic spectrum of the modular surface.")
print()
print("=> Mechanism (a) does NOT bypass Banks-Dine.  σ_t is the Friedmann")
print("   clock, which is exactly the framework Banks-Dine 1995 worked in.")
print()

# Bianchi IX BKL flow
print("="*68)
print("Mechanism (b): Bianchi IX BKL → Lochs-Khinchin → thermal DM?")
print("="*68)
print()
print("BKL flow is t→0+ singular regime.  λ_BKL = π²/(6 log 2) is the")
print("Lyapunov rate per Gauss-shift iteration on the Misner billiard.")
print("Energy density ρ_BKL ~ (anisotropy)^4/t^2 diverges as t→0.")
print()
print("To reframe BKL as DM source:")
print("  - BKL phase ends at t_planck or shortly after")
print("  - Inflation washes out anisotropies if t_inflation > t_BKL")
print("  - Late-time DM cannot 'remember' BKL fluctuations through")
print("    inflation by no-hair theorem (Wald 1983)")
print()
print("=> Mechanism (b) FAILS structurally: BKL is early-time, late-time DM")
print("   density requires Boltzmann not Misner billiard.")
print()

# Modular Laplacian tower
print("="*68)
print("Mechanism (c): Maass-Laplacian tower {λ_n = 1/4 + r_n²} as DM spectrum")
print("="*68)
print()
# Hejhal 1992 + BSV 2005 verified eigenvalues
r_vals = [mpmath.mpf("9.5336952613536"),
          mpmath.mpf("12.173008325585"),
          mpmath.mpf("13.779751351891"),
          mpmath.mpf("14.358509518131"),
          mpmath.mpf("16.138073172222")]
lam_vals = [mpmath.mpf("0.25") + r**2 for r in r_vals]
print(f"r_1 ≈ {r_vals[0]}, λ_1 = {lam_vals[0]}")
print(f"r_2 ≈ {r_vals[1]}, λ_2 = {lam_vals[1]}")
print(f"r_3 ≈ {r_vals[2]}, λ_3 = {lam_vals[2]}")
print()

# Convert eigenvalues to "masses" — Selberg trace formula
# m^2 = λ_n at SOME scale Λ.  What scale ?
# If Λ = M_Pl: m_1 = sqrt(91.14) M_Pl ≈ 9.54 M_Pl, trans-Planckian!
# If Λ = H_0: m_1 ≈ 9.54 H_0, ultra-light DM
# If Λ = m_τ (M134 = 1.61e5 M_Pl in M_Pl=1 units): m_1 ≈ 9.54 * m_τ trans-Planckian

# Critical observation: λ_n DIMENSIONLESS, need a physical scale Λ.
# Test: if Λ = some combination of T_CMB, H_0, etc. — is there a natural choice?
print(f"At Λ = M_Pl:    m_DM_1 = √λ_1 · M_Pl = {mpmath.sqrt(lam_vals[0]) * M_Pl} GeV (trans-Planckian)")
print(f"At Λ = H_0:     m_DM_1 = √λ_1 · H_0  = {mpmath.sqrt(lam_vals[0]) * H0_eV} eV (well below FDM bound)")
print(f"At Λ = T_CMB:   m_DM_1 = √λ_1 · T_γ  = {mpmath.sqrt(lam_vals[0]) * T_CMB_eV} eV (thermal, Lyman-α excluded)")
print(f"At Λ = m_neutrino mass scale (~0.1 eV): m_DM_1 ~ 1 eV thermal DM, excluded")
print()

# Test: thermal occupation of modular Laplacian tower
# n(λ) = 1/(e^{β λ} - 1) at temperature T = 1/β
# Total DM density: ρ_DM = sum_n m_n · n(λ_n) at some T
# If we set T = T_CMB and m_n = √λ_n · Λ for various Λ:

def dm_density_thermal(Lambda_scale_eV, T_eV):
    """Total energy density from thermally occupied Maass tower (just first 5)"""
    rho = mpmath.mpf(0)
    for lam in lam_vals:
        m = mpmath.sqrt(lam) * Lambda_scale_eV
        x = m / T_eV
        if x > 100:
            n = mpmath.exp(-x)
        else:
            n = 1 / (mpmath.exp(x) - 1)
        rho += m * n   # energy density per mode (×g, schematic)
    return rho

# Critical density today
rho_crit_eV4 = mpmath.mpf("8.0992e-11") * mpmath.mpf("1e-36")  # eV^4, = 8.1e-47 GeV^4
# Standard: rho_crit = 3 H_0^2 M_Pl^2 / 8π
# = 3 (1.44e-33)^2 (2.435e27)^2 / 8π eV^4 = 3 * 2.07e-66 * 5.93e54 / (25.13)
# = 3 * 1.23e-11 / 25.13 = 1.47e-12 eV^4? Let me recompute:
rho_crit = 3 * H0_eV**2 * M_Pl_eV**2 / (8 * mpmath.pi)
print(f"rho_crit = 3 H_0^2 M_Pl^2 / 8π = {rho_crit} eV^4")
print()

# For Λ = T_CMB: thermal modular tower
T_today = T_CMB_eV
for Lambda_test in [H0_eV, T_today, mpmath.mpf("1.0"), mpmath.mpf("1e3")]:
    rho_dm = dm_density_thermal(Lambda_test, T_today)
    Omega_dm = rho_dm / rho_crit
    print(f"Λ = {Lambda_test} eV: thermal ρ_DM = {mpmath.nstr(rho_dm, 4)} eV^4, Ω_DM = {mpmath.nstr(Omega_dm, 4)}")

print()
print("None of these Λ choices give Ω_DM ≈ 0.27.  Even if Λ is freely chosen")
print("the modular tower has SUM diverging (semiclassical Weyl law).  We'd need")
print("a UV cutoff which is ad hoc.")
print()

# Granular Farey/Stern-Brocot
print("="*68)
print("Mechanism (d): Granular Farey/Stern-Brocot tessellation as DM source")
print("="*68)
print()
print("The Farey/Stern-Brocot tessellation parameterizes rationals p/q with")
print("the Stern-Brocot tree.  Manin-Marcolli use it for the BKL geodesic")
print("flow on PSL(2,Z)\\H.  In the modular shadow:")
print("  - Each Farey neighbor relation ↔ a Möbius transformation in PSL(2,Z)")
print("  - Density of rationals in [0,1] with denominator ≤ Q ~ (3/π²) Q²")
print()
print("Could the count of Farey representatives encode an emergent DM density?")
print("Mertens theorem: Σ_{q≤Q} φ(q)/q ~ (6/π²) Q.  Asymptotic density 6/π².")
print()
print("PROBLEM: 6/π² ≈ 0.6079 is a DIMENSIONLESS density of rationals, not")
print("a physical Ω_DM h² ≈ 0.12.  No conversion factor available.")
print()
mertens = 6 / mpmath.pi**2
print(f"6/π² = {mertens}")
print(f"Ω_DM h² ≈ 0.12.  Ratio (Ω_DM h²)/(6/π²) = {mpmath.mpf('0.12')/mertens}")
print(f"No structural interpretation of this ratio.")
print()

# Final synthesis
print("="*68)
print("VERDICT Test 1 (DM as Σ_t Ω_DM(t) emergent):")
print("="*68)
print()
print("All four mechanisms (a-d) FAIL to bypass the M174 obstructions.")
print()
print("  (a) Connes-Takesaki σ_t IS the FRW Friedmann time (Connes-Rovelli")
print("      §5).  Boltzmann freeze-out / Banks-Dine 1995 lives in this clock.")
print("      No emergent DM density is computed --- σ_t is a CLOCK, not a")
print("      MATTER SOURCE.  Banks-Dine constraint applies unchanged.")
print()
print("  (b) BKL bouncing is t→0+ singular regime.  Inflation washes out by")
print("      no-hair (Wald 1983).  Late-time DM cannot remember BKL phase.")
print()
print("  (c) Modular Laplacian {λ_n = 1/4 + r_n²} dimensionless; need an")
print("      external scale Λ.  Choosing Λ ≃ T_CMB or M_Pl gives Lyman-α-")
print("      excluded or trans-Planckian masses respectively.  No natural Λ.")
print()
print("  (d) Farey density 6/π² ≈ 0.608 is dimensionless; no conversion to")
print("      Ω_DM h² ≈ 0.12.")
print()
print("Conclusion: the M174 (C) NEGATIVE verdict survives the emergent")
print("reframing.  Static or dynamic, the same dimensional bridge problem")
print("blocks DM as an arithmetic invariant.")
