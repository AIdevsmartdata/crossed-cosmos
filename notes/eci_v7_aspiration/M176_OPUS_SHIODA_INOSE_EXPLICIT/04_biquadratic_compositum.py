"""
M176 sub-task 4 — Biquadratic compositum K^(1) · K^(2) = Q(i, sqrt(-22))
=========================================================================

GOAL: investigate whether a rank-4 transcendental lattice CM K3 X with
T(X) ⊗ Q ≅ K = Q(i, sqrt(-22)) (biquadratic, degree 4 over Q) provides an
ALTERNATIVE realization of the F-theory ECI v9 setup that side-steps the
KW eq (46) obstruction (which requires K^(1) ≅ K^(2) as fields).

KEY STRUCTURAL FACTS (number theory)
====================================

K = Q(i) · Q(sqrt(-22)) = Q(i, sqrt(-22)) = Q(sqrt(-1), sqrt(-22))

Galois group V_4 = Z/2 x Z/2:
   sigma1: i -> -i,    sqrt(-22) -> sqrt(-22)
   sigma2: i -> i,     sqrt(-22) -> -sqrt(-22)
   sigma3 = sigma1 sigma2: i -> -i, sqrt(-22) -> -sqrt(-22)

Three quadratic subfields:
   F_1 = Q(i)            (fixed by sigma2)
   F_2 = Q(sqrt(-22))    (fixed by sigma1)
   F_3 = Q(sqrt(22))     (fixed by sigma3, since (i)*(sqrt(-22)) = i*sqrt(-22) = sqrt(22) up to sign)

Wait: i * sqrt(-22) = i * i * sqrt(22) = -sqrt(22). So sigma3(i*sqrt(-22)) = (-i)*(-sqrt(-22)) = i*sqrt(-22).
So F_3 = Q(i * sqrt(-22)) = Q(-sqrt(22)) = Q(sqrt(22)). REAL quadratic field, fundamental disc 88 (= 4 * 22).

K is therefore a CM field of degree 4 with maximal real subfield F_3 = Q(sqrt(22)).
K is a "biquadratic CM field" -- both F_1 and F_2 are imaginary quadratic, F_3 is real.

CLASS NUMBER OF K (LMFDB-equivalent computation)
==================================================
K = Q(i, sqrt(-22)) has signature (0, 2) (totally complex, degree 4),
discriminant disc(K) = disc(F_1) * disc(F_2) * disc(F_3) ... actually for biquadratic K
with subfields F_1, F_2, F_3 of disc d_1, d_2, d_3 (with d_3 = d_1 * d_2 / gcd^2 etc.):

  disc(K) = d_1 d_2 d_3 / lcm-stuff ... for our case, using formula
  disc(Q(sqrt a, sqrt b)) = (disc(Q(sqrt a)) * disc(Q(sqrt b)) * disc(Q(sqrt(ab))))^?

Actually for biquadratic Q(sqrt(m), sqrt(n)) with m, n squarefree distinct primes etc.,
the formula is disc = (d_1 d_2 d_3) where d_i are the three quadratic discs.

For our K: d_1 = -4 (disc Q(i)), d_2 = -88 (disc Q(sqrt(-22)) = 4 * (-22)), d_3 = 8 (disc Q(sqrt(2)))?
Wait F_3 = Q(sqrt(22)), so d_3 = 88 (since 22 = 2 * 11 squarefree, > 1, mod 4 = 2 -> d = 4*22 = 88).

Hence disc(K) = product = (-4) * (-88) * 88 = 4 * 88 * 88 = 30976.

Hmm let me double-check — for biquadratic Q(sqrt m, sqrt n), the discriminant is more
subtle: disc(K/Q) = disc(F_1/Q) * disc(F_2/Q) * disc(F_3/Q) / gcd^2 in certain cases.

LMFDB lookup (heuristic / exhaustive search): the field Q(i, sqrt(-22)) should be
one of the listed CM fields of degree 4 with discriminant in the standard tables.

The relevant LMFDB number field label would be 4.0.30976.1 (degree 4, signature 0+2,
disc 30976) or similar -- exact lookup deferred but structurally:
   h_K = 1 or 2 most likely for this small discriminant
   class group of small order
"""

import sympy as sp
from sympy import sqrt, I, simplify, expand, factor, gcd

print("="*72)
print("M176 sub-task 4: Biquadratic compositum K = Q(i, sqrt(-22))")
print("="*72)

# --- 1. Verify field structure ----------------------------------------
i_ = I
s22 = sqrt(-22)

# Three quadratic generators
print("\n--- Quadratic subfields of K = Q(i, sqrt(-22)) ---")
print(f"  F_1 = Q(i)            = Q(sqrt(-1))   disc = -4")
print(f"  F_2 = Q(sqrt(-22))    = Q(sqrt(-22))  disc = -88  (= 4 * -22)")

# F_3 = Q(i * sqrt(-22))
prod_gen = expand(i_ * s22)
prod_sq = expand(prod_gen * prod_gen)
print(f"  i * sqrt(-22) = {prod_gen}")
print(f"  (i sqrt(-22))^2 = i^2 * (-22) = -1 * -22 = 22")
print(f"  Hence i sqrt(-22) is a square root of 22 (real), so F_3 = Q(sqrt(22))")
print(f"  F_3 = Q(sqrt(22))     disc = +88  (= 4 * 22, since 22 = 2 mod 4)")

# --- 2. Discriminant calculation --------------------------------------
print("\n--- Discriminant of K/Q ---")
print("Conductor-discriminant formula for abelian Q-extension:")
print("  K = Q(i) Q(sqrt(-22)) is abelian over Q with Galois group V_4 = Z/2 x Z/2")
print("  By conductor-discriminant formula:")
print("    disc(K/Q) = prod over chi in Gal(K/Q)^ of conductor(chi)")
print("  Three nontrivial characters of V_4: chi_1, chi_2, chi_3 = chi_1 * chi_2")
print("  Conductors:")
print("    f(chi_1) = 4   (chi_1 = quadratic char of conductor 4 cutting out Q(i))")
print("    f(chi_2) = 88  (chi_2 = quadratic char mod 88 cutting out Q(sqrt(-22)))")
print("    f(chi_3) = 88  (chi_3 = chi_1 * chi_2 cuts out Q(sqrt(22)), conductor 88)")
print("    f(trivial) = 1")
print("  disc(K/Q) = 1 * 4 * 88 * 88 = 30976 = 2^6 * 11^2 = 4 * 7744")
disc_K = 1 * 4 * 88 * 88
print(f"  Numerical: {disc_K} = {sp.factor(disc_K)}")

# --- 3. Ring of integers and class group ------------------------------
print("\n--- Ring of integers O_K and class group ---")
print("For biquadratic K = Q(sqrt(m), sqrt(n)) with appropriate m, n, the ring of integers")
print("is generally NOT Z[sqrt(m), sqrt(n)] but contains additional units like (1 + sqrt(m))/2.")
print("")
print("LMFDB lookup heuristic for K = Q(i, sqrt(-22)):")
print("  - Degree 4")
print("  - Signature (0, 2) (totally imaginary)")
print("  - Disc 30976 = 2^6 * 11^2")
print("  - Galois V_4")
print("  - This narrows to LMFDB 4.0.30976.X for some X")
print("")
print("Genus theory for class group of biquadratic field:")
print("  By Gauss genus theory (extended to biquadratic),")
print("  |Cl(K)| relates to |Cl(F_1)|, |Cl(F_2)|, |Cl(F_3)| and unit groups.")
print("  F_1 = Q(i):       Cl = trivial, h = 1")
print("  F_2 = Q(sqrt(-22)): Cl = Z/2, h = 2")
print("  F_3 = Q(sqrt(22)): Cl = trivial, h = 1 (real quadratic, small disc)")
print("")
print("  By Brauer's formula (or class number of biquadratic):")
print("    h_K = h_{F_1} h_{F_2} h_{F_3} * Q / (2^{r_K} unit index)")
print("  where Q is index of subgroup of units. For our setup we expect h_K = 1 or 2.")
print("")
print("  HEURISTIC: most likely h_K = 1 (the class number 2 of Q(sqrt(-22)) becomes")
print("  trivial in the compositum K, since the principal ideal (sqrt(-22)) of Q(sqrt(-22))")
print("  capitulates -- it is principal in K, generated by (sqrt(-22)) which already lies in K)")
print("  But this is genus / capitulation argument and needs PARI/sage verification.")

# --- 4. Class group of Q(sqrt(-22)) capitulates? ---------------------
print("\n--- Does Cl(Q(sqrt(-22))) capitulate in K? ---")
print("The class group Cl(Q(sqrt(-22))) = Z/2 has generator the prime ideal p_2 = (2, sqrt(-22))")
print("which is non-principal in Q(sqrt(-22)) (its square = (2)).")
print("")
print("In K = Q(i, sqrt(-22)), the ideal p_2 generates an ideal in O_K.")
print("Is p_2 O_K principal?  I.e. does there exist alpha in O_K with (alpha) = p_2 O_K?")
print("")
print("p_2 has norm 2. We need alpha in O_K with N_{K/Q}(alpha) = 2^2 = 4.")
print("Try alpha = 1 + i: N_{Q(i)/Q}(1+i) = 2, so N_{K/Q}(1+i) = 2^2 = 4 (since [K:Q(i)] = 2).")
print("Indeed (1+i) in Z[i] generates the prime above 2 in Q(i).")
print("In K, (1+i) generates an ideal of norm 4.")
print("")
print("Now p_2 O_K (the prime of Q(sqrt(-22)) above 2 lifted to O_K):")
print("p_2 O_K should split or stay inert depending on discriminant relations.")
print("")
print("The principal ideal (1+i) in K has norm 4. The prime decomposition of 2 in O_K:")
print("  In Q(i): (2) = (1+i)^2, so (1+i) is the unique prime of Q(i) above 2.")
print("  In Q(sqrt(-22)): (2) = p_2^2 with p_2 = (2, sqrt(-22)) non-principal (h=2).")
print("  In K = Q(i, sqrt(-22)): (2) ramifies further. Genus theory gives ramification index e = 4.")
print("  Hence 2 = pi^4 * unit for some prime pi of O_K.")
print("")
print("This pi has norm 2 in K, i.e. N_{K/Q}(pi) = 2.")
print("If we can write pi = (1+i)*sqrt(?) or similar in O_K, then pi is principal in O_K.")
print("")
print("By genus theory, the ideal class p_2 in Cl(Q(sqrt(-22))) DOES capitulate in K when")
print("the genus field of Q(sqrt(-22)) is contained in K. The genus field of Q(sqrt(-22))")
print("is Q(sqrt(-22), sqrt(-1)) = K itself (since -22 = (-1)(2)(11) and the genus field is")
print("generated by sqrt of each prime factor with appropriate sign).")
print("")
print("Indeed, Q(sqrt(-22)) has 'genus field' = compositum of Q(sqrt(-2)), Q(sqrt(11))? ...")
print("More precisely the genus field of Q(sqrt(d)) for d = -22 = (-2) * 11 is")
print("Q(sqrt(-22), sqrt(-2)) = Q(sqrt(-2), sqrt(11)). NOT equal to our K.")
print("")
print("Our K = Q(i, sqrt(-22)) = Q(sqrt(-1), sqrt(-22)) is a DIFFERENT extension")
print("(it adjoins sqrt(-1) instead of sqrt(-2) or sqrt(-11)).")
print("So genus capitulation argument is more subtle here.")

# --- 5. Singular K3 with rank-4 transcendental lattice -----------------
print("\n--- Rank-4 transcendental lattice CM K3 ---")
print("FACT (Mukai, Nikulin): A K3 surface X over C has Picard rank rho(X) <= 20.")
print("Hence transcendental lattice T(X) = NS(X)^perp in H^2(X, Z) has rank")
print("  rk T(X) = 22 - rho(X) >= 2.")
print("")
print("A K3 with rho = 18 has rk T(X) = 4.")
print("If T(X) has CM by a CM field K of degree 4 (= rk T(X)), then X has CM by K.")
print("Such K3 surfaces EXIST -- they are 'exceptional CM K3' or 'K3 with full CM by K'.")
print("")
print("EXAMPLE (Borcea 1992, Nikulin 1979 extended): for K = Q(sqrt(-1), sqrt(-22)),")
print("a K3 with T(X) ⊗ Q ≅ K is a CM K3 of rho(X) = 18 (NOT singular K3 which has rho = 20).")
print("")
print("Construction options:")
print("  (a) Hodge-theoretic: T(X) = lattice on which K acts via complex multiplication;")
print("      Hodge structure is induced by complex structure on T(X) ⊗ R = K ⊗_Q R = C^2.")
print("  (b) Geometric: X = Kummer of an abelian surface A with CM by K;")
print("      A = E_1 x E_2 with E_1 CM by Q(i), E_2 CM by Q(sqrt(-22)) ?")
print("      Then T(A) has rk 4 and CM by Q(i) x Q(sqrt(-22)) = K (as Q-algebra)?")
print("      But Q(i) x Q(sqrt(-22)) is NOT a field, it's a product of fields!")
print("      For CM by K (a field of degree 4), need A simple abelian surface with CM by K.")
print("")
print("DISTINCTION: ")
print("  - 'A = E_1 x E_2' with two non-isogenous CM elliptic curves over different fields")
print("    gives an abelian surface with CM by K_1 x K_2 (a product of fields, NOT a field).")
print("  - 'A simple abelian surface with CM by quartic CM field K' (irreducible)")
print("    gives a NEW elliptic structure not factoring through a product.")
print("")
print("For ECI v9 alternative to KW Case B, we want option (a) or (b) with K = Q(i, sqrt(-22)).")
print("")
print("SHIODA-INOSE FOR PRODUCT A = E_1 x E_2 (NON-isogenous, different CM):")
print("  Pjateckii-Shapiro / Shafarevich (Schütt p.2 Theorem 3 caveat): the bijection")
print("  is between SINGULAR K3 (rho = 20) and rank-2 lattices.")
print("  For non-singular K3 with rk T = 4 and CM, the correspondence is")
print("  ABELIAN SURFACE A (rk H^1 = 4) <-> RANK-2 lattice T(A) inside H^2(A) ?")
print("  That's a different correspondence.")
print("")
print("STATUS: Rank-4 CM K3 with T(X) ⊗ Q ≅ Q(i, sqrt(-22)) DOES exist by general")
print("Nikulin/Mukai theory, but the EXPLICIT construction is harder than rank-2.")
print("Schütt 2008 does NOT cover this case; specialist references would be:")
print("  - Borcea 1986/1992 'Calabi-Yau threefolds and complex multiplication'")
print("  - Voisin 1993 'Miroirs et involutions sur les surfaces K3'")
print("  - Nikulin 1979 / 1980 lattice classification")
print("")
print("RANK-4 CM K3 X with CM by K_4 = Q(i, sqrt(-22)) has Picard rank rho = 18,")
print("MORE moduli than singular K3 (which has rho = 20, no moduli).")
print("Specifically, X^{rk T = 4, CM by K_4} forms a 0-dim moduli (point) since CM forces")
print("the Hodge structure to be rigid.")

# --- 6. Connection to KW Case B alternative ---------------------------
print("\n--- KW Case B alternative via biquadratic compositum ---")
print("Original KW Case B: requires K^(1) ≅ K^(2) (eq 46), so K^(1) = K^(2) as subfields of Q-bar.")
print("")
print("ECI v9 has K^(1) = Q(i) ≇ Q(sqrt(-22)) = K^(2). So Case B fails.")
print("")
print("ALTERNATIVE proposed by M171 + M176: replace K^(1), K^(2) with the COMPOSITUM")
print("K^(1) * K^(2) = Q(i, sqrt(-22)) and ask whether a generalized W = 0 condition exists")
print("for CM K3 X with T(X) ⊗ Q ≅ Q(i, sqrt(-22)).")
print("")
print("This is OUTSIDE the scope of KW (they only treat Borcea-Voisin Z_2 orbifolds with")
print("two factor K3's, not general CM CY 4-folds).")
print("")
print("NEW CONSTRUCTION: replace Borcea-Voisin Z_2 = (-1) on K3 x K3 with a Z_2 x Z_2 = V_4")
print("orbifold action on X^{rk T = 4} where the V_4 = Gal(K/Q) acts on the CM K3 X via")
print("the Hodge structure / non-symplectic automorphism of order 2.")
print("")
print("Such actions are classified by Nikulin's involution / Z/2 x Z/2 K3 orbifold classification.")
print("They lead to NEW CY 4-fold geometries beyond Borcea-Voisin which deserve a separate paper.")
print("")
print("NET: M176 sub-task 4 partially addresses the M171 'open route (b)' by IDENTIFYING")
print("the compositum K = Q(i, sqrt(-22)) as a 4-dim CM field with V_4 Galois group,")
print("disc 30976, and (most likely) class number 1 or 2. The EXPLICIT rank-4 CM K3")
print("construction is reduced to Nikulin/Borcea moduli but not fully written down here.")
print("")
print("VERDICT (D) PARTIAL for sub-task 4: structural identification, no explicit Weierstrass.")
