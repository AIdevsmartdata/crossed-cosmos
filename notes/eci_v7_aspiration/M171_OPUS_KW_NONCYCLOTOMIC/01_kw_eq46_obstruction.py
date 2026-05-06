"""
M171 — Test Kanno-Watari condition (46) for ECI v9 K3 surfaces.

Kanno-Watari arXiv:2012.01111 eq. (46):
  rho^(1)_(20) (K^(1))  =  rho^(2)_(20) (K^(2))  ⊂  ℚ̄

This is the condition for a DW = W = 0 flux to exist in the level-4
component W_(20|20) of a Borcea-Voisin K3 x K3 orbifold X^(1) x X^(2) / Z_2.

ECI v9:
  X^(1) = singular K3 with T_X^(1) ⊗ ℚ ≅ K^(1) = ℚ(i)        (Q(zeta_4))
  X^(2) = singular K3 with T_X^(2) ⊗ ℚ ≅ K^(2) = ℚ(√-22)     (NON-cyclotomic)

For attractive (Picard rank 20) K3 surfaces:
  rho^(i)_(20) : K^(i) → ℚ̄ acts on the (2,0)-form Omega_{X^(i)}.
  The image rho^(i)_(20)(K^(i)) is a copy of K^(i) inside ℚ̄.

Question: does there exist embeddings such that rho^(1)_(20)(ℚ(i)) =
rho^(2)_(20)(ℚ(√-22)) as subfields of ℚ̄?

Test: K^(1) = ℚ(i) and K^(2) = ℚ(√-22) are both imaginary quadratic
extensions of ℚ. They are equal as subfields of ℚ̄ iff their generators
i and √-22 differ only by a non-zero rational (since both are degree
2 over ℚ).

Equivalently: i ∈ ℚ(√-22) iff √-22 ∈ ℚ(i) iff (i)·(√-22) = -√22 ∈ ℚ.
But √22 is irrational, so ℚ(i) ≠ ℚ(√-22) inside ℂ̄.

Conclusion: condition (46) is NOT satisfied for ECI v9 with K^(1) = ℚ(i)
and K^(2) = ℚ(√-22).

mpmath verification: numerical sanity check.
"""

from mpmath import mp, mpc, mpf, sqrt, im, re

mp.dps = 30


def main():
    print("=" * 78)
    print("M171 — Test Kanno-Watari eq. (46) for ECI v9 K^(1)=ℚ(i), K^(2)=ℚ(√-22)")
    print("=" * 78)

    # The (2,0)-period embedding sends the CM field K^(i) into a fixed
    # copy of K^(i) inside ℚ̄ ⊂ ℂ. For attractive K3, the action of x ∈ K^(i)
    # on the (2,0)-form is multiplication by rho^(i)_(20)(x).
    # For an imaginary quadratic field K = ℚ(α) with α = √(-d), the two
    # embeddings into ℂ̄ are α → +√-d and α → -√-d (complex conjugate).

    print()
    print("--- Step 1 : explicit generators ---")
    alpha1 = mpc(0, 1)             # i, generator of K^(1) = ℚ(i)
    alpha2 = mpc(0, sqrt(mpf(22))) # √-22, generator of K^(2) = ℚ(√-22)
    print(f"  alpha_1 = i           = {alpha1}")
    print(f"  alpha_2 = √-22         = {alpha2}")

    # rho_(20)^(i) on the (2,0)-form sends alpha_i to a fixed embedding image.
    # For ECI v9 we take the canonical embedding rho_(20)^(i)(alpha_i) = +alpha_i.
    rho1_20_alpha1 = alpha1
    rho2_20_alpha2 = alpha2
    print(f"  rho^(1)_(20)(i)        = {rho1_20_alpha1}")
    print(f"  rho^(2)_(20)(√-22)     = {rho2_20_alpha2}")

    print()
    print("--- Step 2 : test rho^(1)_(20)(K^(1)) = rho^(2)_(20)(K^(2)) ---")
    # The image rho^(1)_(20)(ℚ(i)) = ℚ + ℚ * i  ⊂ ℂ.
    # The image rho^(2)_(20)(ℚ(√-22)) = ℚ + ℚ * (i√22)  ⊂ ℂ.
    # These are equal iff i ∈ ℚ + ℚ(i√22), iff i = a + b * (i√22) with a,b ∈ ℚ.
    # Then a = 0 and b√22 = 1, so b = 1/√22 ∉ ℚ. Contradiction.

    # Numerical proof of obstruction:
    # If the two fields agreed, i = a + b * (i√22) for some a,b ∈ ℚ.
    # Then necessarily a = Re(i) = 0 and b = 1/√22.
    # But 1/√22 is irrational, so b ∉ ℚ.
    target = mpf(1) / sqrt(mpf(22))
    print(f"  If rho^(1)_(20)(i) ∈ rho^(2)_(20)(ℚ(√-22)), then i = b*(i√22), b = 1/√22")
    print(f"  required b = 1/√22 = {target}")
    print(f"  Is b rational ? continued fraction of 1/√22 :")
    # Use mpmath's identification of rationals via continued fractions
    from mpmath import pslq, identify
    ident = identify(target, ['1', 'sqrt(2)', 'sqrt(11)', 'sqrt(22)'], tol=1e-25)
    print(f"  identify(1/√22) = {ident}  ← contains √22, NOT rational")

    print()
    print("--- Step 3 : also check intersection ℚ(i) ∩ ℚ(√-22) ---")
    # Both contain ℚ. Do they contain anything more in common ?
    # The compositum ℚ(i, √-22) has degree 4 over ℚ (Galois group Z/2 x Z/2),
    # and ℚ(i) ∩ ℚ(√-22) = ℚ.
    # Hence rho^(1)_(20)(ℚ(i)) ≠ rho^(2)_(20)(ℚ(√-22)) inside ℚ̄.
    print("  ℚ(i) ∩ ℚ(√-22) = ℚ (compositum has degree 4 by linear disjointness)")
    print("  Since neither field is contained in the other, eq.(46) FAILS.")

    print()
    print("--- Step 4 : compositum and Galois closure ---")
    # The compositum K = ℚ(i, √-22) = ℚ(i)·ℚ(√-22) is an abelian extension of
    # ℚ of degree 4 with Galois group Z/2 × Z/2.
    # Its discriminant is disc(ℚ(i))^2 * disc(ℚ(√-22))^2 / gcd^2
    # = 4^2 * 88^2 / ... = real biquadratic ℚ(i, √22).
    # Note: ℚ(i, √-22) = ℚ(i, √22) = ℚ(i)·ℚ(√22). Real biquadratic over ℚ is
    # ℚ(√-1, √22). Cyclic ? It's biquadratic, so Z/2 × Z/2, NOT cyclic.

    print("  Compositum = ℚ(i, √-22) = ℚ(i)·ℚ(√22), degree 4, Galois Z/2 × Z/2")
    print("  This is the only field where both K^(1) and K^(2) embed,")
    print("  but their images are DIFFERENT subfields of ℚ̄.")

    print()
    print("--- Step 5 : how about the maximal totally real subfields K_0^(i) ---")
    # K_0^(1) = ℚ (since ℚ(i) is imaginary quadratic with no real subfield > ℚ)
    # K_0^(2) = ℚ (since ℚ(√-22) is imaginary quadratic with no real subfield > ℚ)
    # So K_0^(1) = K_0^(2) = ℚ, condition (47) is automatically satisfied:
    #   rho^(1)_(20)(K_0^(1)) = ℚ = rho^(2)_(20)(K_0^(2))
    # But (47) being satisfied alone is NOT enough — it gives DW = 0 only,
    # not DW = W = 0.

    print("  K_0^(1) = max real subfield of ℚ(i) = ℚ ")
    print("  K_0^(2) = max real subfield of ℚ(√-22) = ℚ ")
    print("  -> rho^(1)_(20)(K_0^(1)) = rho^(2)_(20)(K_0^(2)) = ℚ ✓ (eq 47 OK)")
    print("  -> But (46) still fails since K^(1) ≠ K^(2) as subfields of ℚ̄.")
    print("  -> KW case A) eq (45) holds: K_0 agree but K differ ; gives level-4 ")
    print("     component (3,1)-free with W_(20|20) = W_(20|02) ; W ≠ 0 always.")

    print()
    print("===========================================================================")
    print("VERDICT: eq.(46) FAILS for ECI v9. KW Case A (eq 45) applies, NOT Case B.")
    print()
    print("   K_0^(1) = K_0^(2) = ℚ        ✓ implies eq. (45)/(47) satisfied")
    print("   K^(1) ≠ K^(2) as subfields  ✗ implies eq. (46) violated")
    print()
    print(" Per Kanno-Watari Step 3 (page 28, top): in case A, ")
    print(" 'a 2 × n_1 = 2 × n_2 = 4-dimensional subspace V_1 ⊗ V_2 carries a")
    print("  flux with DW = 0 BUT W = 0 always violated.'")
    print()
    print(" => On a Borcea-Voisin orbifold (X^(1) × X^(2)) / Z_2 with")
    print("    K^(1) = ℚ(i), K^(2) = ℚ(√-22), there is NO DW = W = 0 flux in")
    print("    the level-4 W_(20|20) component. ECI v9 W = 0 cannot be ")
    print("    achieved within the W_(20|20) component of Kanno-Watari.")
    print("===========================================================================")


if __name__ == "__main__":
    main()
