"""
V8-agent-11: Bekenstein-Hawking 1/4 factor — KMS modular flow vs Euclidean action.

Question: Does the KMS structure ALONE derive the 1/4 in S_BH = A/(4 ℓ_P²),
or is it a circular re-expression of the gravitational action input?

Strategy:
  1. Euclidean Schwarzschild geometry (Gibbons-Hawking 1977).
  2. On-shell Euclidean action → S_E = β F (thermodynamic relation).
  3. Entropy via S = (1 - β ∂_β) (-S_E).
  4. Track each factor: 16πG (Einstein-Hilbert prefactor), β_H = 8πGM/c³,
     surface gravity κ = c⁴/(4GM), area A = 16πG²M²/c⁴.
  5. KMS period identification: β_KMS = 2π/κ (Unruh/Bisognano-Wichmann).
  6. Show 1/4 = (2π) / (8π) only after the gravitational prefactor 1/(16πG)
     is already fixed — i.e., the KMS period *identifies* β_H but does NOT
     fix the 1/4 without the action input.

All in natural units: G=1, c=1, ħ=1, k_B=1.
"""

import sympy as sp

# ── Symbols ──────────────────────────────────────────────────────────────────
M, G, hbar, kB, c = sp.symbols('M G hbar kB c', positive=True)
beta, kappa_sym, A_sym = sp.symbols('beta kappa A', positive=True)

# ── Step 1 : Euclidean Schwarzschild geometry ─────────────────────────────────
# Metric: ds² = f dτ² + f⁻¹ dr² + r² dΩ²,  f = 1 - 2GM/r
# Near horizon r → r_h = 2GM: write r = r_h + ρ²/(8GM) → τ periodic.
# Regularity: avoid conical singularity ↔ τ ~ τ + β_H.
print("=" * 70)
print("STEP 1: Horizon regularity → Hawking temperature")
print("=" * 70)

r_h = 2*G*M          # Schwarzschild radius (c=1)
kappa = 1/(4*G*M)    # surface gravity κ = c⁴/(4GM) in c=1,G units

# Near-horizon: ds² ≈ κ²ρ² dτ² + dρ² → Rindler
# Regularity (no conical singularity) requires τ ~ τ + 2π/κ
beta_H_from_regularity = 2*sp.pi / kappa
beta_H_from_regularity = sp.simplify(beta_H_from_regularity)
print(f"  Surface gravity:  κ = 1/(4GM) = {kappa}")
print(f"  Regularity condition: β_H = 2π/κ = {beta_H_from_regularity}")
# = 8πGM  ✓ (Hawking T = 1/(8πGM))

T_H = 1 / beta_H_from_regularity
print(f"  Hawking temperature T_H = κ/(2π) = {sp.simplify(T_H)}")

# ── Step 2 : Euclidean action (Gibbons-Hawking 1977) ─────────────────────────
print()
print("=" * 70)
print("STEP 2: On-shell Euclidean action")
print("=" * 70)

# The Einstein-Hilbert action (Euclidean) + Gibbons-Hawking boundary term:
#   I_E = -1/(16πG) ∫ R √g d⁴x - 1/(8πG) ∮ K √h d³x
#
# On-shell for Schwarzschild: bulk R=0, boundary term gives:
#   I_E^{on-shell} = β_H M/2  (standard result, Gibbons-Hawking 1977)
#
# But let's track the 1/(16πG) prefactor explicitly.
#
# The GH boundary term for a sphere at r→∞:
#   -(1/(8πG)) ∮ K √h d³x
# Extrinsic curvature of r=R sphere in flat space vs Schwarzschild:
#   ΔK ≈ M/R² + O(M²/R³),  √h d²Ω = R² β_H  →  ∮ ΔK √h = β_H M
# So:
#   I_E = -(1/(8πG)) * β_H * M  [with sign: Euclidean, note sign conventions vary]
# Using the convention where I_E = β F (free energy):
#   β F = I_E = β_H M / 2  (the /2 from subtracting reference flat space)
#   → F = M/2  ... this is just β_H * M - T*S reorganised.

# Standard result (see e.g. Hawking-Page, York):
# I_E^{on-shell} = β_H^2 / (16π G)   [in terms of β_H and G only]
beta_H = sp.Symbol('beta_H', positive=True)
I_E_onshell = beta_H**2 / (16*sp.pi*G)
print(f"  I_E^{{on-shell}} = β_H² / (16πG) = {I_E_onshell}")
print(f"  (This uses M = β_H/(8πG) from T_H = κ/(2π))")

# Verify: β_H M/2 = β_H * (β_H/(8πG)) / 2 = β_H²/(16πG) ✓
M_from_beta = beta_H / (8*sp.pi*G)   # from T_H = 1/β_H = 1/(8πGM) → M = 1/(8πG T_H) = β_H/(8πG)
check = sp.simplify(beta_H * M_from_beta / 2 - I_E_onshell)
print(f"  Check β_H*M/2 == β_H²/(16πG): residual = {check}  ✓")

# ── Step 3 : Entropy from Euclidean action ────────────────────────────────────
print()
print("=" * 70)
print("STEP 3: Entropy S = (1 - β ∂_β)(-I_E) at fixed G")
print("=" * 70)

# Free energy: F = I_E / β_H = β_H / (16πG)
# Entropy:     S = β_H² ∂F/∂β_H ... use S = β²(-∂F/∂β) with F = I_E/β:
#
# More directly: S = (1 - β_H ∂_{β_H}) I_E
#   = I_E - β_H * ∂I_E/∂β_H
#   = β_H²/(16πG) - β_H * 2β_H/(16πG)
#   = β_H²/(16πG) - 2β_H²/(16πG)
#   = -β_H²/(16πG)   [sign issue from conventions]
# Correct formula: S = β_H * E - I_E  (Legendre transform)
# where E = -∂ ln Z/∂β = ∂I_E/∂β_H = 2β_H/(16πG) = β_H/(8πG) = M ✓
E = sp.diff(I_E_onshell, beta_H)
print(f"  Energy E = ∂I_E/∂β_H = {E} = M ✓")

S_BH_raw = beta_H * E - I_E_onshell
S_BH_raw = sp.simplify(S_BH_raw)
print(f"  S = β_H*E - I_E = {S_BH_raw}")
# = β_H²/(16πG)

# ── Step 4 : Express in terms of Area ────────────────────────────────────────
print()
print("=" * 70)
print("STEP 4: Map entropy to area A = 4π r_h² = 16πG²M²")
print("=" * 70)

# r_h = 2GM, A = 4π(2GM)² = 16πG²M²
# M = β_H/(8πG) → A = 16πG²*(β_H/(8πG))² = 16πG²*β_H²/(64π²G²) = β_H²/(4π)
A_from_beta = beta_H**2 / (4*sp.pi)   # A in units where G=1 absorbed ... let's keep G explicit
# A = 16πG²M² = 16πG²*(β_H/(8πG))² = 16πG²*β_H²/(64π²G²) = β_H²/(4π)
A_exact = 16*sp.pi*G**2*(beta_H/(8*sp.pi*G))**2
A_exact = sp.simplify(A_exact)
print(f"  A = 16πG²M² = {A_exact}  (with M = β_H/(8πG))")
# = β_H² / (4π)   [G-independent!  because r_h=2GM brings G²M²=G²*(β_H/8πG)²=β_H²/(64π²G⁰)]
# Wait: G²*(1/(8πG))² = G²/(64π²G²) = 1/(64π²) → A=16π*β_H²/(64π²) = β_H²/(4π). G cancels ✓

# Now: S = β_H²/(16πG)
# And: A/(4G) = β_H²/(4π) / (4G) = β_H²/(16πG) ✓
ratio = sp.simplify(S_BH_raw / (A_exact / (4*G)))
print(f"  S / (A/(4G)) = {ratio}  → S = A/(4G) = A/(4 ℓ_P²) ✓")

print()
print("  EXPLICIT FACTOR ACCOUNTING:")
print(f"  S_BH = β_H²/(16πG)")
print(f"       = [β_H²/(4π)] * [1/(4G)]")
print(f"       = A * (1/4) * (1/G)")
print(f"       = A / (4G)  = A / (4 ℓ_P²)")
print()
print("  The 1/4 comes from:  (2π)² / (4π * 16πG) * something?")
print("  More precisely, track the factors:")
print("  β_H = 2π/κ   [regularity, KMS period]")
print("  κ   = 1/(4GM) [surface gravity]")
print("  A   = 16πG²M²")
print()
print("  S = β_H²/(16πG)")
print("    = (2π/κ)² / (16πG)")
print("    = (2π)² / (κ² * 16πG)")

kappa_expr = sp.Rational(1,4) / (G*M)
S_via_kappa = (2*sp.pi/kappa_expr)**2 / (16*sp.pi*G)
S_via_kappa = sp.simplify(S_via_kappa)
print(f"    = {S_via_kappa}")

# ── Step 5 : KMS / Bisognano-Wichmann analysis ───────────────────────────────
print()
print("=" * 70)
print("STEP 5: KMS structure — what it fixes and what it doesn't")
print("=" * 70)

print("""
  KMS condition (Bisognano-Wichmann 1975, Unruh 1976, Sewell 1982):
  ─────────────────────────────────────────────────────────────────
  For a QFT in the Rindler wedge (or near a bifurcate Killing horizon),
  the vacuum state restricted to one wedge is a KMS state with respect
  to boost time t_boost, at inverse temperature:

      β_KMS = 2π / κ

  where κ is the surface gravity (Killing normalisation at infinity).

  For Schwarzschild: κ = 1/(4GM)  →  β_KMS = 8πGM = β_H  ✓

  This KMS identification is EXACT and fixes the Hawking temperature
  *kinematically* from the geometry, without knowing the gravitational
  action.

  WHAT KMS DOES:
    ✓ Identifies β_H = 2π/κ  (periodicity of modular flow)
    ✓ Fixes T_H = κ/(2π)     (Hawking temperature)
    ✗ Does NOT fix the entropy coefficient
    ✗ Does NOT give S = A/(4G) without additional input

  The entropy is obtained from:
    S = -Tr(ρ log ρ)  with ρ = exp(-β_H H_ζ) / Z

  But H_ζ (the modular Hamiltonian = Rindler Hamiltonian / Killing energy)
  is NOT determined by the KMS condition alone — it requires knowing the
  stress-energy content and the gravitational coupling.

  In the Euclidean path integral route:
    Z = exp(-I_E^{on-shell})
    I_E^{on-shell} = β_H M / 2 = β_H² / (16πG)
    ↑ This requires the 1/(16πG) prefactor of the Einstein-Hilbert action.

  The 1/4 in S = A/(4G) therefore descends from:
    1/(16πG)  [EH action prefactor]  ×  (2π/κ)²  [β_H²]  /  A
    = 1/(16πG) × (2π)² κ⁻²  /  (4π(2GM)²)
    where each piece is needed.
""")

# ── Step 6 : The 2π/8π claim from F-3 ────────────────────────────────────────
print("=" * 70)
print("STEP 6: Analysing the '2π/8π' claim from F-3")
print("=" * 70)
print("""
  F-3 claimed: 1/4 = 2π / (8π)  from KMS modular flow normalisation.

  This is NUMERICALLY TRUE but LOGICALLY CIRCULAR:
    - The 8π in the denominator arises from β_H = 8πGM.
    - But β_H = 8πGM requires knowing κ = 1/(4GM), which requires
      the Schwarzschild solution, not KMS structure alone.
    - More critically: even if β_H = 2π/κ is fixed by KMS,
      the ratio 2π/(β_H * κ) = 2π/(2π) = 1,  not 1/4.
    - The actual 1/4 comes from:
        S = β_H * M - β_H²/(16πG)
      and the β_H² vs A comparison requires M = β_H/(8πG)
      which uses the specific dynamics (Schwarzschild solution).

  Explicit check: can KMS alone give S = A/(4G)?
    KMS gives: β_H = 2π/κ  (period)
    Modular Hamiltonian for half-space in Rindler: H_mod = ∫ x T_{tt} d³x
    In flat space (Rindler): S_entanglement is UV-divergent.
    Gravitational dressing regularises it: S = A/(4G) only when
    Newton's constant G appears, which is the gravitational action input.

  VERDICT: CIRCULAR-IDENTIFICATION
    The "2π/8π = 1/4" is a post-hoc numerical coincidence in the
    specific case of Schwarzschild.  It rearranges known results but
    does not DERIVE the 1/4 from KMS kinematics.
    The 1/(16πG) EH prefactor is the true origin of the 1/4.
""")

# ── Step 7 : Numerical verification ──────────────────────────────────────────
print("=" * 70)
print("STEP 7: Numerical check (G=1, M=1)")
print("=" * 70)

G_val = 1
M_val = 1
beta_H_val = 8 * sp.pi * G_val * M_val
kappa_val = 1 / (4 * G_val * M_val)
r_h_val = 2 * G_val * M_val
A_val = 4 * sp.pi * r_h_val**2
I_E_val = beta_H_val**2 / (16 * sp.pi * G_val)
E_val = beta_H_val / (8 * sp.pi * G_val)   # = M
S_val = beta_H_val * E_val - I_E_val
S_exact = A_val / (4 * G_val)

print(f"  G={G_val}, M={M_val}")
print(f"  β_H = 8πGM = {sp.simplify(beta_H_val)}")
print(f"  κ   = 1/(4GM) = {kappa_val}")
print(f"  β_H = 2π/κ = {sp.simplify(2*sp.pi/kappa_val)}  ✓ (KMS period)")
print(f"  A   = 4π(2GM)² = {sp.simplify(A_val)}")
print(f"  I_E = β²/(16πG) = {sp.simplify(I_E_val)}")
print(f"  E   = ∂I_E/∂β  = {sp.simplify(E_val)} = M ✓")
print(f"  S   = β*E - I_E = {sp.simplify(S_val)}")
print(f"  A/(4G) = {sp.simplify(S_exact)}")
print(f"  S == A/(4G): {sp.simplify(S_val - S_exact) == 0}  ✓")
print()
print(f"  Factor breakdown of S = A/(4G):")
print(f"    Numerator:   β_H² = (8πGM)² = 64π²G²M²")
print(f"    Denominator: 16πG")
print(f"    → S = 64π²G²M²/(16πG) = 4πG M²")
print(f"    A/(4G) = 4π(2GM)²/(4G) = 4π*4G²M²/(4G) = 4πGM²  ✓")
print()
print(f"  The '1/4' appears as:  A/(4G) = [A/G] * (1/4)")
print(f"  Origin: 64π²/(16π) = 4π,  then A=16πGM² (in G=1) → ratio 4π/A*G*M²")
print(f"  The exact path: (2π)²/κ² ÷ (16πG) = 4π²*16G²M²/(16πG) = 4πGM² = A/(4G)")
print()
print(f"  Where does the 4 come from in the denominator?")
print(f"    (2π)² = 4π² from KMS period squared")
print(f"    16π from Euclidean action denominator (= 16πG from EH prefactor)")
print(f"    κ²   = 1/(16G²M²) from geometry")
print(f"    Net: 4π² * 16G²M² / (16πG) = 4πG M²")
print(f"    Factor of 4 in denominator: 16π/4π² = 4/π ... no.")
print()
print(f"  Cleaner: S = β_H²/(16πG) = (2π/κ)²/(16πG) = 4π²/(κ² 16πG)")
print(f"           A  = 4π/κ² (in G=1: A=4π*(4GM)²=64πG²M², κ=1/(4GM))")

# In terms of κ and G only:
# A = 4π r_h² = 4π*(2GM)² = 16πG²M², κ=1/(4GM) → κ²=1/(16G²M²) → M²=1/(16G²κ²)
# A = 16πG²/(16G²κ²) = π/κ²   ... wait:
# A = 16πG²M²,  M = 1/(4Gκ)  → M²=1/(16G²κ²)  → A = 16πG²/(16G²κ²) = π/κ²
A_kappa = sp.pi / kappa_sym**2  # A in terms of κ (G-independent!)
S_kappa = 4*sp.pi**2 / (kappa_sym**2 * 16*sp.pi*G)
S_kappa_simplified = sp.simplify(S_kappa)
print(f"\n  In terms of κ: A = π/κ²,  S = 4π²/(16πG κ²) = π/(4Gκ²) = A/(4G)  ✓")
print(f"  Ratio 4π²/(16π) = π/4  →  S = (π/4) * (1/(Gκ²)) = A/(4G)  ✓")
print(f"\n  The '1/4' = π/(4π) ratio from (2π period)² / (16π EH-factor)")
print(f"  ↑ The 16π is 16πG from the EH action 1/(16πG).")
print(f"  ↑ KMS gives (2π)² = 4π². The ratio 4π²/16π = π/4.")
print(f"  ↑ The remaining 1/G comes from the EH action, not KMS.")

print()
print("=" * 70)
print("FINAL VERDICT: CIRCULAR-IDENTIFICATION")
print("=" * 70)
print("""
  Summary of logical dependencies:

  [KMS / Bisognano-Wichmann]
    ↓ fixes β_H = 2π/κ  (the period of modular flow)
    ↓ fixes T_H = κ/(2π)  (Hawking temperature — kinematic)

  [Euclidean path integral + Einstein-Hilbert action 1/(16πG)]
    ↓ fixes I_E^{on-shell} = β_H²/(16πG)
    ↓ → entropy S = β_H * M - I_E = β_H²/(16πG) = A/(4G)

  The 1/4 requires BOTH inputs:
    1. KMS period β_H = 2π/κ  (fixes numerator factor (2π)² = 4π²)
    2. EH action prefactor 1/(16πG)  (fixes denominator 16πG)

  Numerical check: 4π² / (16π) = π/4,  A = π/κ²  →  S = A/(4G)
  The 1/4 is (2π)²/(16π) = π/4 per unit (κ⁻² G⁻¹) — not a pure KMS ratio.

  F-3's claim "1/4 = 2π/8π" confuses:
    - The PERIOD β_H = 2π/κ = 8πGM  (where 8πGM is the specific value for M)
    - With the ENTROPY COEFFICIENT, which requires the EH prefactor.

  VERDICT: CIRCULAR-IDENTIFICATION
  The KMS modular structure IDENTIFIES T_H but does NOT DERIVE S_BH = A/(4G).
  The 1/4 is not a consequence of KMS normalisation — it is a consequence of
  the 1/(16πG) coefficient of the Einstein-Hilbert action.
""")
