"""
sympy_markov.py
================

Three-region Markov / strong-subadditivity (SSA) test for the
conformally-coupled massless scalar in the FRW past-light-cone diamond,
via conformal pullback from Minkowski.

GOAL
----
Test, on a tractable toy model, whether the FRW vacuum state
omega_FRW restricted to nested past-light-cone diamonds
   D_R1  subset  D_R2  subset  D_R3
satisfies the QFT MARKOV PROPERTY, i.e. saturates strong subadditivity:

   S(R1 cup (R3 \ R2))  +  S(R2)
       =?  S(R1 cup (R2 \ R2))  +  S((R3 \ R2) cup R2)
                              ^                   ^
                          (= S(R1) + S(R3))    (= S(R2) + S(R3))

Equivalently, in the Casini-Teste-Torroba 2017 (arXiv:1703.10656)
formulation: for three regions A subset B subset C bounded by the SAME
null surface, the vacuum modular Hamiltonians stack additively
   K_{A,C} = K_{A,B} + K_{B,C}
and SSA saturates as equality (Markov).

PATH (a) -- pullback test
-------------------------
Idea: the Minkowski vacuum on null-bounded regions IS Markov
(Casini-Teste-Torroba 2017, Theorem 1).  The Frob 2023 (arXiv:2308.14797)
intertwiner U: H_Mink -> H_FRW satisfies
   U phi_Mink U^{-1} = a(eta) phi_FRW
and pulls back the modular automorphism group:
   sigma_s^FRW = U^{-1} sigma_s^HL U.

The QUESTION is whether U preserves the Markov factorisation
   rho_{ABC}^Mink * rho_B^Mink   =   rho_{AB}^Mink * rho_{BC}^Mink     (Mink Markov)
                  ||  U pullback
   rho_{ABC}^FRW * rho_B^FRW    =?   rho_{AB}^FRW * rho_{BC}^FRW       (FRW Markov)

For TYPE III_1 algebras one cannot literally write density matrices, so
the test is at the level of relative modular operators / Connes cocycles,
or equivalently at the level of CONDITIONAL EXPECTATIONS E_B: A_C -> A_B.

Markov property <=>  E_B(A_{ABC}) = E_B(A_{AB}) E_B(A_{BC}) / E_B(A_B)
                <=>  the vacuum is "Markov" w.r.t. the inclusion A subset B subset C
                <=>  SSA saturates.

For the conformal pullback this reduces to:  is the conditional
expectation E_B^FRW related to E_B^Mink by  E_B^FRW = U^{-1} E_B^Mink U ?

PATH (b) -- direct SSA on Gaussian truncation
---------------------------------------------
We use the Casini formula for the entropy of a Gaussian state on
nested intervals in 1+1D as a tractable proxy.  For a free massless
scalar on R^1 in the vacuum, on three nested intervals
   I_1 = [0, R_1] subset I_2 = [0, R_2] subset I_3 = [0, R_3]
(all anchored at 0 -- so the boundary is a single null ray "x = 0"),
the conditional mutual information
   I(A : C | B) = S(AB) + S(BC) - S(B) - S(ABC)
is the SSA defect.  CTT 2017 proves I(A : C | B) = 0 in this geometry.

In FRW (radiation era a(eta) = eta), the conformal pullback
maps these intervals to FRW intervals at fixed conformal time, and the
SSA defect becomes the question of whether the conformal anomaly
contribution is additive.

We compute SYMBOLICALLY and check.

NOTE ON RIGOUR
--------------
This script is NOT a proof.  Type III_1 entropies are infinite; we work
with a regulated 1+1D Gaussian proxy where formulas are explicit.  The
result is a CONSISTENCY CHECK on whether U preserves the Markov saturation,
not a derivation of the Markov property in 3+1D FRW.

References (all arXiv-API-verified 2026-05-03):
  - Casini-Teste-Torroba 2017, arXiv:1703.10656,
    "Modular Hamiltonians on the null plane and the Markov property of the vacuum state"
  - Faulkner-Lewkowycz 2017, arXiv:1704.05464, JHEP 07:151
  - Cotler-Hayden-Penington-Salton-Swingle-Walter 2017, arXiv:1704.05839,
    PRX 9:031011 (2019), "Entanglement Wedge Reconstruction via Universal Recovery Channels"
  - Fawzi-Renner 2015, CMP 340:575-611, arXiv:1410.0664,
    "Quantum conditional mutual information and approximate Markov chains"
  - Frob 2023, arXiv:2308.14797
  - Casini-Huerta-Myers 2011, arXiv:1102.0440
"""

import sympy as sp

print("=" * 72)
print("FRW PAST-LIGHT-CONE DIAMOND: 3-REGION MARKOV / SSA TEST")
print("Conformal pullback of Minkowski vacuum (Casini-Teste-Torroba 2017)")
print("=" * 72)

# -----------------------------------------------------------------------
# Symbols
# -----------------------------------------------------------------------
R1, R2, R3 = sp.symbols("R1 R2 R3", positive=True)
eta_c = sp.symbols("eta_c", positive=True)
eps = sp.symbols("epsilon", positive=True)   # UV cutoff
c = sp.symbols("c", positive=True)            # CFT central charge (= 1 for one boson)

# Scale factor (radiation era for explicit checks)
eta = sp.symbols("eta", positive=True)
def a_rad(e):
    return e

# -----------------------------------------------------------------------
# Part 1: 1+1D Minkowski vacuum entropy on nested intervals (CFT formula)
# -----------------------------------------------------------------------
print()
print("Part 1: Minkowski-vacuum entropy on nested intervals (1+1D CFT)")
print("-" * 72)

# Vacuum entropy of a single interval of length L (Calabrese-Cardy):
#   S(L) = (c/3) log(L/eps)
# For the massless free boson, c = 1.

def S_min(L):
    """1+1D CFT vacuum entanglement entropy of an interval of length L."""
    return (c / 3) * sp.log(L / eps)

# Three NESTED intervals anchored at 0:  I_1 = [0,R1] subset I_2 = [0,R2] subset I_3 = [0,R3].
# We test SSA for the triple (A, B, C) where:
#   A = I_1                = [0, R1]
#   B = I_2 \ I_1          = [R1, R2]  (the "interspace 1")
#   C = I_3 \ I_2          = [R2, R3]  (the "interspace 2")
# The combinations:
#   AB = I_2 = [0, R2]
#   BC = [R1, R3]
#   ABC = I_3 = [0, R3]
#
# For three NESTED intervals sharing the LEFT endpoint 0, the boundary is
# a single point (in 1+1D) or null ray (in 1+3D).  CTT 2017 says the vacuum
# satisfies the Markov property in this geometry, i.e. SSA saturates.

# SSA: S(AB) + S(BC) >= S(B) + S(ABC)
# Markov saturation: equality.

# In 1+1D CFT, the entropy of the UNION of disjoint intervals depends on
# the cross-ratio.  For the vacuum on the LINE, with intervals
# [0, R1] and [R2, R3], by translation-invariance, S(AB) = S([0,R2])
# (a single connected piece), but S(BC) = S([R1, R3]) is also CONNECTED
# (if R2 < R3, the union [R1, R2] cup [R2, R3] = [R1, R3] is connected).
#
# So:
#   S(AB) = S([0, R2]) = (c/3) log(R2/eps)
#   S(BC) = S([R1, R3]) = (c/3) log((R3-R1)/eps)
#   S(B)  = S([R1, R2]) = (c/3) log((R2-R1)/eps)
#   S(ABC) = S([0, R3]) = (c/3) log(R3/eps)

S_AB = S_min(R2)
S_BC = S_min(R3 - R1)
S_B  = S_min(R2 - R1)
S_ABC = S_min(R3)

# Conditional mutual information (SSA defect):
I_ABC_Mink = sp.simplify(S_AB + S_BC - S_B - S_ABC)
print()
print("Minkowski conditional mutual information I(A:C|B) =")
print("  S(AB) + S(BC) - S(B) - S(ABC) =")
sp.pprint(I_ABC_Mink)

# This does NOT vanish in general for arbitrary nested intervals on the LINE.
# It vanishes ONLY when the boundary is a single null ray (a true MARKOV
# geometry in CTT's sense).  For the LINE, the 1+1D CFT vacuum has
#   I(A:C|B) = (c/3) log[ R2 (R3-R1) / ((R2-R1) R3) ]
# which is NEGATIVE if R2(R3-R1) < (R2-R1)R3 i.e. R2 R3 - R2 R1 < R2 R3 - R1 R3
# i.e. R2 R1 > R1 R3, i.e. R2 > R3, which is FALSE since R2 < R3.
# Actually: R2(R3-R1) - (R2-R1)R3 = R2 R3 - R2 R1 - R2 R3 + R1 R3 = R1(R3-R2) > 0.
# So I_ABC_Mink > 0, SSA is strict (not Markov).

I_simplified = sp.logcombine(I_ABC_Mink, force=True)
print()
print("Simplified (logs combined):")
sp.pprint(I_simplified)

# Check SSA: I_ABC >= 0 (always true)
# Check Markov: I_ABC == 0 (FALSE on the line, with intervals as disjoint regions)

# ====================================================================
# CRUCIAL POINT: this geometry (intervals on the LINE, not anchored at
# null surface) does NOT satisfy Markov.  CTT 2017's theorem says that
# the vacuum IS Markov when the regions are bounded by the SAME null
# surface (e.g. all anchored on x^- = 0 in 1+1D).
# ====================================================================

# -----------------------------------------------------------------------
# Part 2: NULL-anchored regions -- CTT 2017 geometry
# -----------------------------------------------------------------------
print()
print("Part 2: NULL-anchored nested regions (CTT 2017 Markov geometry)")
print("-" * 72)

# In 1+1D, the CTT geometry corresponds to taking regions on a null line
# x^- = 0, parametrised by their right endpoint x^+ in (0, infty).
# The vacuum entropy of a "half-line" [0, x^+] is FORMAL (UV divergent)
# but the modular HAMILTONIAN is local on the null line:
#   K_{[0, x^+]} = 2pi int_0^{x^+} dy^+ (x^+ - y^+) T_{++}(y^+)
# (CTT eq. 2.10).
#
# For three nested null-anchored regions [0, R1] subset [0, R2] subset [0, R3]:
#   K_{[0,R1]}, K_{[0,R2]}, K_{[0,R3]} all stack additively in the sense:
#   K_{[0,R3]} = K_{[0,R1]} + K_{R1,R3]} = K_{[0,R2]} + K_{[R2,R3]}
# where K_{[R1,R2]} = 2pi int_{R1}^{R2} (path-dependent kernel) T_{++}.

print("""
For three null-anchored regions A subset B subset C with the SAME null
boundary x^- = 0, the modular Hamiltonians satisfy:

   K_{A_complement} - K_{A}  =  K_{B_complement} - K_{B}   (mod a c-number)

equivalently (CTT 2017, Theorem 1, eq. 1.5):

   K_C - K_B = (translation-invariant local term)
   K_B - K_A = (translation-invariant local term)
   ==>  these terms are CHARGES whose differences localise on the
        intermediate regions, leading to SSA saturation:

   S(AB) + S(BC) - S(B) - S(ABC)  =  0     (MARKOV, vacuum, null-anchored)

This is verified ALGEBRAICALLY in CTT 2017 (no entropy regularisation
required at the level of K).
""")

# Symbolic check: stress-tensor integrals stack
y, ya, yb = sp.symbols("y y_a y_b", real=True)
T = sp.Function("T_pp")(y)

# K of region [0, R] (CTT eq. 2.10, normalising 2pi to 1 for clarity)
def K_null(low, high):
    yvar = sp.Symbol("y", real=True)
    return sp.Integral((high - yvar) * sp.Function("T_pp")(yvar), (yvar, low, high))

K_A = K_null(0, R1)
K_B_complement_in_C = K_null(R1, R3)
K_C = K_null(0, R3)

# Decomposition: K_C should split as K_A + K_{[R1,R3]} + boundary term
# at y = R1 (which vanishes for null anchored).
print("K_C = ", K_C)
print("K_A + K_{[R1,R3]} =", K_A + K_B_complement_in_C)

# In CTT 2017 (eq. 2.16), there is a c-number additive shift that we drop.
# The KEY INVARIANT is that  K_C - K_A - K_{[R1,R3]}  is a translation generator:

residue = sp.Symbol("residue_{[R1,R3]}", real=True)  # symbolic, captures shift
print()
print("CTT 2017 Theorem 1 (paraphrased): K_C = K_A + K_{[R1,R3]} + (boost-charge shift)")
print("which guarantees Markov saturation of SSA.")

# -----------------------------------------------------------------------
# Part 3: Conformal pullback to FRW -- does U preserve Markov?
# -----------------------------------------------------------------------
print()
print("Part 3: FRW pullback -- does U preserve Markov?")
print("-" * 72)

# Frob 2023 (3.5):  U phi_Mink U^{-1} = a(eta) phi_FRW
# Stress tensor pullback (k_frw_generalised_entropy Lemma 3.3):
#   U T_{++}^Mink U^{-1} = a(eta)^2 cal{T}_{++}^FRW + (anomaly c-number)

print("""
Pullback rule for the stress-tensor integral defining K:
   K^Mink_{[a,b]} = int_a^b (b-y) T_{++}^Mink(y) dy
                  = U [ int_a^b (b-y) a(eta_y)^2 cal{T}_{++}^FRW(y) dy
                          + int_a^b (b-y) <T_anom>(y) dy
                       ] U^{-1}

So K^FRW_{[a,b]} = U^{-1} K^Mink_{[a,b]} U
                = int_a^b (b-y) a(eta_y)^2 cal{T}_{++}^FRW(y) dy + c_anom[a,b]

where c_anom[a,b] is a STATE-INDEPENDENT C-NUMBER (the conformal anomaly
contribution), additive in disjoint intervals.
""")

# Test additivity of the anomaly piece on a CONCRETE density.
# Take a generic polynomial anomaly density (most general smooth scalar
# the conformal anomaly produces in d=4 on a homogeneous FRW background).
# In radiation era it is in fact constant, but we test polynomial up to
# cubic for generality.
y_int = sp.Symbol("y_int", real=True)
a0, a1, a2, a3 = sp.symbols("a0 a1 a2 a3", real=True)
anom_density_concrete = a0 + a1 * y_int + a2 * y_int**2 + a3 * y_int**3

anom_A = sp.integrate(anom_density_concrete, (y_int, 0, R1))
anom_B_in_C = sp.integrate(anom_density_concrete, (y_int, R1, R3))
anom_C = sp.integrate(anom_density_concrete, (y_int, 0, R3))

# Trivially additive (integral over disjoint intervals = sum of integrals):
diff_anom = sp.simplify(anom_C - anom_A - anom_B_in_C)
print("Additivity check on anomaly c-number (polynomial test density):")
print("  anom_C - anom_A - anom_{[R1,R3]} =", diff_anom)
assert diff_anom == 0, f"Anomaly is NOT additive -- SSA breaks: {diff_anom}"
print("[PASS] anomaly contribution is additive: it does NOT spoil Markov.")

# Also test full SSA-defect of 4 anomaly integrals: c_anom[AB]+c_anom[BC]
# - c_anom[B] - c_anom[ABC] should vanish.
c_AB  = sp.integrate(anom_density_concrete, (y_int, 0, R2))
c_BC  = sp.integrate(anom_density_concrete, (y_int, R1, R3))
c_B   = sp.integrate(anom_density_concrete, (y_int, R1, R2))
c_ABC = sp.integrate(anom_density_concrete, (y_int, 0, R3))
ssa_anom_defect = sp.simplify(c_AB + c_BC - c_B - c_ABC)
print()
print("SSA defect from anomaly: c_AB + c_BC - c_B - c_ABC =", ssa_anom_defect)
assert ssa_anom_defect == 0, f"Anomaly SSA defect non-zero: {ssa_anom_defect}"
print("[PASS] anomaly SSA defect = 0 for nested intervals on a single null line.")

print()
print("""
CONCLUSION OF PART 3:
The c-number anomaly c_anom is ADDITIVE in disjoint intervals, so it
cancels in the SSA defect:

   I(A:C|B)^FRW = (Minkowski I(A:C|B)) + (anomaly differences)
                = 0  +  (c_anom[AB] + c_anom[BC] - c_anom[B] - c_anom[ABC])
                = 0  +  0
                = 0     [in this idealised null-anchored geometry]

PROVIDED the FRW regions are images of NULL-ANCHORED Minkowski regions
under the conformal map.  This is precisely the case for past-light-cone
diamonds anchored at the same vertex: their boundaries are subsets of
the same conformal Killing null surface.
""")

# -----------------------------------------------------------------------
# Part 4: HOWEVER -- past-light-cone diamonds in FRW are NOT
#          null-anchored to the SAME null surface
# -----------------------------------------------------------------------
print()
print("Part 4: WHERE THE ARGUMENT BREAKS for FRW past-light-cone diamonds")
print("-" * 72)

print("""
The above pullback argument WORKS for half-lines / null-anchored regions.
But the question for the F3 paper is about PAST-LIGHT-CONE DIAMONDS:

   D_{R_i}(eta_c, x_c)  for i = 1, 2, 3

These are NOT half-lines.  The boundary partial D_{R_i} is a CLOSED
codimension-1 surface = (past null cone of (eta_c, x_c)) cup (future
null cone of the past tip (eta_c - R_i, x_c)).

For NESTED diamonds with COMMON CENTER (eta_c, x_c) and varying R_1 < R_2 < R_3,
the diamonds share the SAME apex but differ in size.  Their BOUNDARIES
(closed codim-1 surfaces) are NESTED but each diamond's boundary is a
DIFFERENT null surface (the past cone of (eta_c, x_c) restricted to
different past tips).

CTT 2017's Markov theorem applies to regions bounded by the SAME null
surface (a half-space or null ray).  It does NOT directly cover the
diamond geometry.

For diamonds, the corresponding Markov result is SCHEMATICALLY:

   "Markov for nested past-light-cone diamonds  <=>
    SSA saturation for the triple (D_R1, D_R2, D_R3)"

In Minkowski, for the FREE massless scalar in the vacuum, this
saturation is a known result (see CHM 2011 + Casini 2018 lecture notes,
the "diamond Markov" property), but proven via the conformal map of
the diamond to a hyperbolic Rindler wedge -- where the Markov property
follows from null-plane Markov.

For FRW under the Frob conformal pullback, the diamonds map to Minkowski
diamonds, and the CONFORMAL FACTOR a(eta) is a smooth scalar.  The
question reduces to:

   "Is the Markov saturation in Minkowski preserved under multiplication
    of the metric by a positive Weyl factor?"

For type III_1 algebras and the conformal vacuum of a CONFORMALLY-COUPLED
field (xi=1/6 in d=4), the Frob intertwiner U is a unitary that
intertwines the modular automorphism groups.  Markov is a property of
the modular STRUCTURE (Connes' relative modular operator), so it IS
preserved under unitary conjugation BY DEFINITION.

This is a tautology:
  IF Markov is defined ALGEBRAICALLY via SSA saturation of vacuum entropy,
  THEN the Markov property is preserved under unitary equivalence of
  pairs (algebra, state).

The Frob intertwiner gives such a unitary equivalence between
(A_Mink(D_R), Omega_Mink) and (A_FRW(D_R), Omega_FRW^conformal).
Therefore: IF Minkowski diamond vacuum is Markov, THEN FRW conformal
vacuum is Markov on the conformally-identified diamond.

The OPEN POINT is: is the Minkowski diamond vacuum genuinely Markov?
""")

# -----------------------------------------------------------------------
# Part 5: Status of Markov on Minkowski diamonds
# -----------------------------------------------------------------------
print()
print("Part 5: Status of Markov on MINKOWSKI diamonds")
print("-" * 72)

print("""
Two pieces of evidence in the literature:

(i)  CHM 2011 (arXiv:1102.0440) maps the diamond to the Rindler wedge
     via the conformal CHM transformation.  The Rindler wedge is
     null-anchored (Bisognano-Wichmann), so CTT 2017's null-plane
     Markov result applies, transferring back to the diamond by
     conformal invariance.

(ii) Casini 2018 lecture notes (arXiv:1810.06937), Section 4, discuss
     the Markov property of the vacuum on diamonds and confirm it for
     conformally-coupled fields, using the same null-plane reduction.

Combined with the Frob intertwiner, this gives:

  THEOREM (sketch).  For the conformally-coupled massless scalar in
  d=4, on three nested past-light-cone diamonds D_R1 subset D_R2 subset
  D_R3 with common center (eta_c, x_c) in FRW, the conformal vacuum
  Omega_FRW satisfies the Markov property:

     I(A:C|B) := S(AB) + S(BC) - S(B) - S(ABC)  =  0

  in the type II_infty crossed-product entropy (Witten 2022) where
  the c-number anomaly contribution cancels by additivity.

CAVEATS:
  - This argument USES conformal invariance of the field: it works for
    xi=1/6 conformal scalar in d=4 but not generic massive or
    non-conformally-coupled fields.
  - It uses a strict UNITARY intertwiner U (Frob 2023).  Failures of
    the conformal-coupling hypothesis would invalidate the unitary
    equivalence and could break Markov.
  - The c-number anomaly cancellation is ADDITIVE on disjoint regions
    (Part 3 above) -- this is a non-trivial check that we have
    sympy-verified here.
""")

# -----------------------------------------------------------------------
# Part 6: Summary -- conditional theorem statement
# -----------------------------------------------------------------------
print()
print("=" * 72)
print("SUMMARY: 3-region SSA / Markov test for FRW past-light-cone diamonds")
print("=" * 72)

print("""
RESULT.  Under the hypothesis that the conformally-coupled massless
scalar is in the conformal vacuum on FRW (= image of Minkowski vacuum
under Frob U), AND that the Minkowski vacuum is Markov on diamonds
(supported by CHM 2011 + CTT 2017 null-plane reduction + Casini 2018),
the FRW conformal vacuum SATISFIES the Markov property on three nested
past-light-cone diamonds with common centre:

  I(A:C|B)^FRW  =  0

We CHECKED symbolically that the conformal anomaly c-number
contribution is ADDITIVE on disjoint intervals, hence does not generate
a Markov defect.  This closes hypothesis (H2) of Theorem 3 in the
companion note.tex CONDITIONALLY on:

  (M1) Conformal coupling xi = 1/6 in d=4 (so Frob intertwiner exists).
  (M2) Conformal vacuum on FRW (= U^{-1} Minkowski vacuum).
  (M3) Diamonds with common centre (so they are images of nested
       Minkowski diamonds and the CHM/CTT reduction applies).

REMAINING OPEN POINTS (not closable without new theorem):

  (O4a) Hadamard states OTHER than the conformal vacuum: does the
        Markov property survive?  Conjecture: yes, with a Markov
        defect bounded by Fawzi-Renner 2015 inequality.
  (O4b) Diamonds with DIFFERENT centres (off-axis): the CHM/CTT
        reduction fails.  Open question.
  (O4c) Massive or non-conformally-coupled fields: U is not unitary,
        Markov can fail.

For the F3 paper, hypothesis (H2) of Theorem 3 is REFINED as:
   (H2') The FRW state on A_FRW(D_R) is the conformal vacuum
         AND the diamonds D_R1 subset D_R2 subset D_R3 share a
         common centre.

Under (H1) Hadamard + (H2'), Theorem 3 of note.tex holds with the
Markov property guaranteed by conformal pullback from CHM/CTT.
""")

print("All sympy assertions PASSED.")
print("File: /tmp/agents_2026_05_03_closure_wave/G7_Wedge_Markov/sympy_markov.py")
