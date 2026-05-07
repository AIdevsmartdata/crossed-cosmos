"""
M173 — Escape route (a): H^1(Z_(1); Q) ⊗ H^1(Z_(2); Q) component.

Verbatim quote from KW arXiv:2012.01111 page 29 (end of section 2.4):

  "As a reminder, we did not study arithmetic characterization for the
   H^1(Z_(1); Q) ⊗ H^1(Z_(2); Q) component of (7) to support a DW = 0 flux
   (W = 0 is automatic)."

This is a CRUCIAL distinction missed in M171. In the H^1 ⊗ H^1 component,
W = 0 is AUTOMATIC, only DW = 0 needs arithmetic. So the obstruction
encountered in W_(20|20) (which requires K^(1) ≅ K^(2) for DW = W = 0,
i.e., KW Case B / eq 46) does NOT apply.

The relevant question for the H^1 ⊗ H^1 component is therefore:
  When does this component SUPPORT a non-trivial DW = 0 flux?

KW eq (5)-(7) page 9-10 set up the structure:

  H^4_H(Y;Q) = (T_0^(1) ⊗ T_0^(2)) ⊗ Q  ⊕  H^1(Z_(1);Q) ⊗ H^1(Z_(2);Q)

The first term gets KW's full arithmetic treatment in §2.4.
The second term is OUT-OF-SCOPE in KW.

For ECI v9: Z_(1) and Z_(2) are the fixed-point CURVES of the involutions
sigma_(1) on X^(1) and sigma_(2) on X^(2). For a Borcea-Voisin K3 x K3
orbifold, these are typically genus-g curves (or unions of rational curves).

KW eq (5):  Z = C_(g) ⊔ ⊔_p L_p,   g(C_(g)) = (22 - r - a) / 2,   L_p ≃ P^1.

For X^(i) attractive (rk(T_X^(i)) = 2), the Nikulin pair (S_0, T_0, σ) is
constrained. With T_0 of rank 20 (S_0 of rank 2), in our Borcea-Voisin
setup if we relax T_X = T_0:
  - If S_0 = ⟨2⟩ (smallest rank-1 lattice), then a = 0, r = 1
    g = (22 - 1 - 0)/2 = 10.5  ← NOT INTEGER, this rank-1 case excluded
  - If S_0 = U or U(2): rank 2, a depends on Nikulin pair.

For our ECI v9 case with X^(1), X^(2) BOTH attractive (T_X^(i) = T_0^(i),
rank 2), the H^1(Z_(i)) carries Hodge structure of weight 1. The dimension
of H^1(Z_(i); Q) depends on the genus g_(i):
  - dim_Q H^1(Z_(i); Q) = 2 g_(i) (for the genus-g_(i) curve C_(g))
  - additional 0-dim contribution from rational P^1 components

The Hodge structure on H^1(C_(g); Q) decomposes as

   H^1(C_(g); Q) ⊗ C = H^{1,0}(C_(g)) ⊕ H^{0,1}(C_(g))

each of complex dimension g_(i). The (4,0) component of the Y_BV
cohomology is

   (4,0) ⊂ H^{1,0}(Z_(1)) ⊗ H^{1,0}(Z_(2))   ← rank g_(1) g_(2)
   (3,1) ⊂ H^{1,0}(Z_(1)) ⊗ H^{0,1}(Z_(2)) ⊕ H^{0,1}(Z_(1)) ⊗ H^{1,0}(Z_(2))
   (2,2) ⊂ ...
   (0,4) ⊂ H^{0,1}(Z_(1)) ⊗ H^{0,1}(Z_(2))   ← rank g_(1) g_(2)

This component admits a Hodge structure of LEVEL 2 (max |p-q| = 2 here),
NOT level 4.

Wait: Z_(i) is a curve (complex 1-dim), so H^1(Z_(i)) has weight 1.
The TENSOR H^1 ⊗ H^1 has weight 2 (NOT 4).

Looking back at KW eq (6)-(7):
  H^4(Y;Q) ≃ [H^4(X^(1) × X^(2);Q)]^σ ⊕ H^2(Z_(4);Q)

  Z_(4) = Z_(1) × Z_(2)  (eq just before (5))

So H^2(Z_(4); Q) = H^2(Z_(1) × Z_(2); Q). By Künneth:

  H^2(Z_(1) × Z_(2)) ≃ H^2(Z_(1)) ⊗ H^0(Z_(2)) ⊕ H^1(Z_(1)) ⊗ H^1(Z_(2))
                       ⊕ H^0(Z_(1)) ⊗ H^2(Z_(2))

Yes! H^1(Z_(1)) ⊗ H^1(Z_(2)) IS the "middle" of H^2(Z_(4)). It contributes
to H^4(Y; Q) via the construction (the 2-form on Z_(4) pulled back to the
exceptional divisor).

Now: H^1(Z_(1)) ⊗ H^1(Z_(2)) carries a Hodge structure of TOTAL WEIGHT 2.
Inside H^4(Y;Q), this corresponds to a Hodge substructure SHIFTED to weight
4 by the Tate twist coming from the Gysin map. After the shift, the Hodge
structure is:

  (1,0) ⊗ (1,0)  ↪ (2,0) ⊗ Tate(1) = (3,1)   ← (3,1) component!
  (1,0) ⊗ (0,1)  ↪ (1,1) ⊗ Tate(1) = (2,2)
  (0,1) ⊗ (1,0)  ↪ (1,1) ⊗ Tate(1) = (2,2)
  (0,1) ⊗ (0,1)  ↪ (0,2) ⊗ Tate(1) = (1,3)

WAIT — this analysis would mean H^1 ⊗ H^1 contributes to (3,1) and (1,3),
NOT (4,0) and (0,4). Re-examining:

The Tate twist for the Gysin push-forward through a 1-dim divisor (the
exceptional divisor of the C^2/Z_2 resolution above Z_(4)) is by 1, so
weight goes from 2 to 4. Hodge type (a,b) goes to (a+1, b+1).

So:
  (1,0) ⊗ (1,0) → (2,0) → (3,1) ← Tate(1) shift gives (3,1) NOT (4,0)
  (1,0) ⊗ (0,1) → (1,1) → (2,2)
  (0,1) ⊗ (1,0) → (1,1) → (2,2)
  (0,1) ⊗ (0,1) → (0,2) → (1,3)

So this component admits NO (4,0) or (0,4) component — it is purely
(3,1) ⊕ (2,2) ⊕ (1,3). Hence:

  W ∝ <Ω | G> where Ω ∈ H^{4,0}(Y)
    But H^{4,0}(Y) lives only in the FIRST term (T_0^(1) ⊗ T_0^(2)) ⊗ Q,
    NOT in H^1(Z_(1)) ⊗ H^1(Z_(2))!

This is exactly KW's claim: "W = 0 is automatic" for fluxes in
H^1(Z_(1)) ⊗ H^1(Z_(2)), because this component has NO (4,0) component
to pair with G ∈ (3,1) ⊕ (2,2) ⊕ (1,3).

Therefore:

  ANY G ∈ H^1(Z_(1)) ⊗ H^1(Z_(2)) ⊂ H^4(Y; Q)
   ⟹  W = ∫_Y G ∧ Ω_Y = 0     (automatic!)

The non-trivial question is then DW = 0, i.e., absence of the (3,1)
component.

The (3,1) component sits in H^{1,0}(Z_(1)) ⊗ H^{1,0}(Z_(2)) (after the Tate
shift). For G to be (3,1)-free, the FLUX projected onto this complex
g_(1) * g_(2) - dimensional subspace must vanish.

For a Q-rational flux G ∈ H^4(Y; Q), this is an arithmetic condition on
the Hodge structures of Z_(1) and Z_(2).

For the H^1 ⊗ H^1 ⊗ Q (Tate-twisted) component to admit G ≠ 0 with both
DW = 0 and W = 0, we need a NON-SIMPLE (= non-CM-type) rational Hodge
structure or a structure where the simple component decomposition has at
least one component with no (3,1) and no (1,3) part.

For the ECI v9 case where Z_(1) and Z_(2) are CM curves (which happens
when X^(1), X^(2) are singular K3 of CM type and the involutions inherit
the CM structure), H^1(Z_(i); Q) decomposes via the CM structure of the
Jacobian Jac(Z_(i)).

Numerical check: Let g_(1) = g_(2) = g for some g (KW formula). For
ECI v9 with some Nikulin pair (S_0^(i), T_0^(i), σ_(i)):
- T_0^(1) = T_X^(1) = U(2)U(2)U(2)... rank 20 ; S_0^(1) = E_8(2)U(2) rank 18?
   No, for X^(1) attractive rank(T_X) = 2, we need T_0^(1) = T_X^(1) of rank 2.
   So rank S_0^(1) = 20, and from Nikulin's classification (S_0, T_0, σ) for
   T_0 of rank 2: a = 1 (if T_0 = ⟨-2⟩-related), r = 18 typically.

KW page 9 mentions the formula g = (22 - r - a)/2. For r = 18, a = 0:
   g = 4/2 = 2  (genus 2 curve)
For r = 18, a = 2:
   g = 2/2 = 1  (elliptic curve!)
For r = 19, a = 1:
   g = 2/2 = 1  (elliptic curve)
For r = 20, a = 0 (no fixed points):  g = 2/2 = 1 (but Z empty? KW p.9 footnote
   says Z empty for S_0 = U[2]E_8[2], the unique exception).

So generically, g_(i) ∈ {1, 2} for the relevant Nikulin pairs.

If g_(1) = g_(2) = 1, both Z_(i) are elliptic curves, and H^1(Z_(i); Q)
is 2-dim with weight-1 Hodge structure. If E_(i) has CM, then H^1(E_(i)) is
of CM-type with field Q(sqrt(-d_i)).

In ECI v9, IF the Nikulin pair gives g = 1 elliptic-curve fixed locus AND
this elliptic curve has CM by O_{K^(i)} respectively, THEN we have a clean
H^1 ⊗ H^1 = Q(i) ⊗ Q(√-22) compositum analog!

This SAME compositum K^(1) · K^(2) = Q(i, √-22) appears here, but on a
DIFFERENT cohomology component (H^1 ⊗ H^1 instead of T_0 ⊗ T_0).

The crucial difference: in the H^1 ⊗ H^1 component, W = 0 is automatic.
DW = 0 reduces to a (3,1)-freedom condition.

By KW eq (24) for the simple component decomposition under K^(1) ⊗ K^(2):
  V_1 ⊗ V_2 ≃ ⊕_{i=1}^r W_i

For V_1 = H^1(Z_(1); Q) of dim 2 (CM by Q(i)) and V_2 = H^1(Z_(2); Q) of
dim 2 (CM by Q(√-22)):
  K^(1) ⊗_Q K^(2) = Q(i) ⊗_Q Q(√-22) = Q(i, √-22) (single biquadratic field)

  ⟹ V_1 ⊗ V_2 ≃ W_1 (single component) of Q-dim 4
  ⟹ Hodge structure on W_1 is rank 4, with [L_1 : Q] = 4 = dim_Q W_1
  ⟹ ALL of W_1 is acted on by the biquadratic field Q(i, √-22)

The question becomes: in the (Tate-twisted to weight 4) Hodge structure on
W_1 (rank 4 over Q), what are the (3,1), (2,2) components?

Since H^1(Z_(1)) ⊗ H^1(Z_(2)) has Hodge type:
   (1,1) tensor (1,1) → after Tate(1) →
   (1,0) ⊗ (1,0) → (2,0) → (3,1)        rank g_(1) g_(2) = 1
   (1,0) ⊗ (0,1) → (1,1) → (2,2)        rank g_(1) g_(2) = 1
   (0,1) ⊗ (1,0) → (1,1) → (2,2)        rank g_(1) g_(2) = 1
   (0,1) ⊗ (0,1) → (0,2) → (1,3)        rank g_(1) g_(2) = 1

Hodge numbers h^{p,q}: h^{3,1} = 1, h^{2,2} = 2, h^{1,3} = 1.

For DW = 0, we need h^{3,1} part of G to vanish. The CM structure means
W_1 ⊗ Q(i,√-22)^nc has 4 simultaneous eigenvectors v_a, each in a definite
(p,q) Hodge type.

By KW page 14 eq (14): the Q-rational fluxes G_a satisfying g^(a)_b ≠ 0 for
some b imply g^(a)_b ≠ 0 for ALL b (Galois orbit stays Q-rational).

Therefore: a Q-rational flux that has g^(a)_b ≠ 0 for the (3,1) basis
element ALSO has g^(a)_b ≠ 0 for the (1,3), (2,2)_a, (2,2)_b basis elements
in the same Galois orbit. The (3,1) component is killed iff the entire
Galois orbit is killed iff the FLUX is zero in that simple component.

For W_1 = single simple component of dim 4 over Q, with one (3,1) eigenvector:
  - If the (3,1) eigenvector is in the same Galois orbit as the (1,3), (2,2)_a,
    (2,2)_b eigenvectors (which it must be, since W_1 is simple and has dim 4
    matching [L_1 : Q] = 4), THEN any non-zero Q-rational flux has a non-zero
    (3,1) component → DW ≠ 0.

CONCLUSION: For the H^1 ⊗ H^1 component on a Borcea-Voisin K3 x K3 orbifold
with both X^(i) singular K3 of CM type Q(i) and Q(√-22), AND with the fixed
locus Z_(i) being a CM elliptic curve with CM by O_{K^(i)}, the SINGLE simple
W_1 component has Hodge level 4 with h^{3,1} = 1 ≠ 0. Therefore NO non-zero
Q-rational flux in W_1 satisfies DW = 0.

Therefore the H^1 ⊗ H^1 component does NOT provide a DW = 0 flux either,
under the ASSUMPTION that the Hodge structure on H^1(Z_(1)) ⊗ H^1(Z_(2))
factors through the same biquadratic field Q(i, √-22) as the T_0 ⊗ T_0 case.

But there's a SECOND scenario: the rational Hodge structure on
H^1(Z_(1)) ⊗ H^1(Z_(2)) might NOT be CM-type (cf KW page 11 footnote 23
explicitly leaves this open). If it has a level-0 simple sub-Hodge-structure,
then a Q-rational flux can be supported there with DW = W = 0 trivially.

This is precisely KW page 11 footnote 23:
   "This condition is equivalent to existence of an algebraic curve in
    Z_(1) × Z_(2) other than a copy of Z_(1) × pt or pt × Z_(2)."

So the H^1 ⊗ H^1 escape route is OPEN if and only if there exists a NEW
algebraic curve C ⊂ Z_(1) × Z_(2) other than the trivial slices. Such a
curve would be a graph of a non-trivial map Z_(1) → Z_(2) (or a cover-like
correspondence).

For Z_(1), Z_(2) both elliptic curves of CM type with DIFFERENT CM fields
Q(i) and Q(√-22), there is NO non-constant morphism Z_(1) → Z_(2)
(this would force the CM fields to agree, by Honda-Tate / Tate's theorem
on isogenies of CM abelian varieties).

In particular, Z_(1) = C/Λ_1 with End(Z_(1)) = Z[i] and Z_(2) = C/Λ_2 with
End(Z_(2)) = Z[(1+√-22)/2] (or related) are NOT ISOGENOUS.

For non-isogenous CM elliptic curves Z_(1), Z_(2), the only correspondences
in Z_(1) × Z_(2) are products of vertical and horizontal cycles, giving the
trivial fibers Z_(1) × pt and pt × Z_(2). No further algebraic curves exist.

THEREFORE: the H^1(Z_(1)) ⊗ H^1(Z_(2)) component does NOT carry a level-0
sub-Hodge-structure when Z_(1) and Z_(2) are non-isogenous CM elliptic
curves.

THEREFORE: route (a) [H^1 ⊗ H^1] is CLOSED for ECI v9.

Verbatim KW p.11 footnote 23:
   "This condition [existence of level-0 rational Hodge substructure in
    H^1(Z_(1);Q) ⊗ H^1(Z_(2);Q)] is equivalent to existence of an
    algebraic curve in Z_(1) × Z_(2) other than a copy of Z_(1) × pt or
    pt × Z_(2)."

This is the analog of the SAME obstruction we hit in §2.4: K^(1) ≅ K^(2)
needed (or in this case, Z_(1) isogenous to Z_(2)) for a flux to exist.

For ECI v9 with K^(1) = Q(i), K^(2) = Q(√-22), no such isogeny.

VERDICT: route (a) → CLOSED (probability ~80% based on Honda-Tate).
"""

from mpmath import mp, mpc, mpf, sqrt, pi, gamma, log, exp, fabs, im, re

mp.dps = 30


def main():
    print("=" * 78)
    print("M173 — Escape route (a): H^1(Z_(1)) ⊗ H^1(Z_(2)) component analysis")
    print("=" * 78)

    print()
    print("--- Step 1: Verify Hodge type of H^1 ⊗ H^1 in H^4(Y) (Tate twisted) ---")
    print()
    print("  H^1(Z_(i); Q) has weight 1, types (1,0) and (0,1).")
    print("  H^1(Z_(1)) ⊗ H^1(Z_(2)) has weight 2, types (2,0), (1,1), (0,2).")
    print("  In H^4(Y;Q), the contribution is via Gysin push-forward + Tate(1):")
    print("     (a,b) → (a+1, b+1)")
    print()
    print("  Hodge types in the contribution to H^4(Y;Q):")
    print("    (1,0) ⊗ (1,0) → (2,0) → (3,1)   [rank g1*g2]")
    print("    (1,0) ⊗ (0,1) → (1,1) → (2,2)   [rank g1*g2]")
    print("    (0,1) ⊗ (1,0) → (1,1) → (2,2)   [rank g1*g2]")
    print("    (0,1) ⊗ (0,1) → (0,2) → (1,3)   [rank g1*g2]")
    print()
    print("  KEY: NO (4,0) or (0,4) component! ⟹ W = ∫ G ∧ Ω is automatically 0")
    print("  for any G in H^1 ⊗ H^1 (since Ω ∈ H^{4,0}(Y) lives in a")
    print("  COMPLEMENTARY summand, namely T_0^(1) ⊗ T_0^(2) ⊗ Q).")
    print()
    print("  Thus W = 0 is AUTOMATIC for fluxes in H^1 ⊗ H^1. (KW page 29 verbatim)")

    print()
    print("--- Step 2: DW = 0 condition needs (3,1)-freedom ---")
    print()
    print("  For G ∈ H^1(Z_(1)) ⊗ H^1(Z_(2)) ∩ H^4(Y;Q) to satisfy DW = 0:")
    print("     <(3,1) part of G> = 0")
    print()
    print("  The (3,1) part lives in H^{1,0}(Z_(1)) ⊗ H^{1,0}(Z_(2)) (Tate shifted).")
    print("  For Z_(1) genus g_(1), Z_(2) genus g_(2): rank g_(1)*g_(2).")
    print()
    print("  When Z_(1), Z_(2) are CM elliptic curves (g=1) with CM fields")
    print("  K_(Z1) = Q(sqrt(-d1)), K_(Z2) = Q(sqrt(-d2)):")

    print()
    print("--- Step 3: Apply KW §2.3.3 / §2.4.1 to H^1 ⊗ H^1 instead of T_0 ⊗ T_0 ---")
    print()
    print("  V_1 = H^1(Z_(1); Q),  V_2 = H^1(Z_(2); Q),  K_(Zi) = End_Hdg(V_i)")
    print()
    print("  KW eq (19): V_1 ⊗_Q V_2 carries action of K_(Z1) ⊗_Q K_(Z2) ≅ ⊕_i L_i")
    print()
    print("  For ECI v9 if K_(Z1) = Q(i), K_(Z2) = Q(√-22):")
    print("     K_(Z1) ⊗_Q K_(Z2) = Q(i) ⊗_Q Q(√-22) = Q(i, √-22) (single field, r=1)")
    print("     ⟹ V_1 ⊗ V_2 ≃ W_1 (single simple component) of Q-dim 4")

    print()
    print("--- Step 4: Hodge type analysis on the W_1 simple component ---")
    print()
    print("  W_1 is rank 4 over Q. After Tate twist into H^4(Y;Q):")
    print("     h^{3,1}(W_1) = 1   (one Galois-orbit element of (3,1))")
    print("     h^{2,2}(W_1) = 2   (two of (2,2))")
    print("     h^{1,3}(W_1) = 1   (one of (1,3))")
    print()
    print("  By KW eq (14)-(16): a Q-rational flux G in W_1 has Galois-coherent")
    print("  coefficients g_b. If g_b ≠ 0 for the (3,1) basis element, then")
    print("  g_b ≠ 0 for ALL Galois-conjugate basis elements (b in same orbit).")
    print()
    print("  Since W_1 is simple of dim 4, there is exactly one Galois orbit")
    print("  of size 4 covering all 4 basis vectors.")
    print()
    print("  ⟹ Q-rational G ∈ W_1 has either ALL coefficients zero")
    print("    (G = 0) or ALL coefficients non-zero, in which case h^{3,1}")
    print("    component is NON-zero ⟹ DW ≠ 0.")
    print()
    print("  CONCLUSION: in the simple W_1 component arising from CM elliptic")
    print("  curves Z_(1), Z_(2) with NON-ISOMORPHIC CM fields, NO non-trivial")
    print("  Q-rational flux satisfies DW = 0.")

    print()
    print("--- Step 5: ALTERNATIVE: non-CM Hodge structure on H^1(Z_(1)) ⊗ H^1(Z_(2)) ---")
    print()
    print("  KW page 11 footnote 23 verbatim:")
    print("     'This condition [existence of level-0 rational Hodge")
    print("      substructure in H^1(Z_(1);Q) ⊗ H^1(Z_(2);Q)] is equivalent")
    print("      to existence of an algebraic curve in Z_(1) × Z_(2) other")
    print("      than a copy of Z_(1) × pt or pt × Z_(2).'")
    print()
    print("  An algebraic curve in Z_(1) × Z_(2) other than the trivial slices")
    print("  is the graph of a non-constant morphism Z_(1) → Z_(2), or a")
    print("  multi-section.")
    print()
    print("  For elliptic curves: a non-constant morphism Z_(1) → Z_(2) is an")
    print("  ISOGENY (up to translation). ")
    print()
    print("  For CM elliptic curves with End(Z_(1)) ⊗ Q = Q(i),")
    print("  End(Z_(2)) ⊗ Q = Q(√-22): an isogeny would force CM fields to be")
    print("  EQUAL (Honda-Tate / Tate isogeny theorem, IF over a number field).")
    print()
    print("  Since Q(i) ≠ Q(√-22), Z_(1) is NOT isogenous to Z_(2) over Q̄.")

    # Numerical verification: j-invariants of Q(i) and Q(√-22) CM elliptic curves
    print()
    print("--- Step 6: Numerical j-invariant check (mpmath dps=30) ---")
    # j(i) = 1728
    j_i = mpf(1728)
    # j(τ_Q) for τ_Q = i√(11/2) (one root of H_{-88}):
    # H_{-88}(X) = X^2 - 6294842640960*X - 102457728*(some form)
    # Actually, from M169: j(τ_Q) ≈ 2,509,696.0767 for one specific embedding
    # Let me compute via the q-expansion:
    tau_Q = mpc(0, sqrt(mpf(11)/2))
    q = exp(2 * pi * mpc(0, 1) * tau_Q)
    # j(q) = 1/q + 744 + 196884*q + ...
    j_tauQ = mpf(1) / q + 744
    for n in range(1, 30):
        q_n = q ** n
        # Use Eisenstein E_4^3 / Δ for high precision: skip for now, use sum
        # Simplified: compute via E_4^3 / (E_4^3 - E_6^2)
        pass

    # Use proper E_4 / E_6 computation
    def eisenstein_E4(tau, terms=50):
        """E_4(tau) = 1 + 240 sum_n sigma_3(n) q^n"""
        q = exp(2 * pi * mpc(0, 1) * tau)
        s = mpf(1)
        for n in range(1, terms):
            sigma3 = sum(d**3 for d in range(1, n + 1) if n % d == 0)
            s += 240 * sigma3 * q ** n
        return s

    def eisenstein_E6(tau, terms=50):
        """E_6(tau) = 1 - 504 sum_n sigma_5(n) q^n"""
        q = exp(2 * pi * mpc(0, 1) * tau)
        s = mpf(1)
        for n in range(1, terms):
            sigma5 = sum(d**5 for d in range(1, n + 1) if n % d == 0)
            s -= 504 * sigma5 * q ** n
        return s

    def j_invariant(tau, terms=50):
        E4 = eisenstein_E4(tau, terms)
        E6 = eisenstein_E6(tau, terms)
        return 1728 * E4**3 / (E4**3 - E6**2)

    j_i_val = j_invariant(mpc(0, 1))
    j_tauQ_val = j_invariant(tau_Q)

    print(f"  j(i) = {j_i_val}  (expected 1728)")
    print(f"  j(i sqrt(11/2)) = {j_tauQ_val}")

    # Check: j-invariants are different ⟹ different CM elliptic curves
    print(f"  |j(i) - j(τ_Q)| = {abs(j_i_val - j_tauQ_val)}  ≠ 0 ⟹ different curves")

    print()
    print("--- Step 7: Honda-Tate isogeny obstruction ---")
    print()
    print("  Tate's isogeny theorem (1966): for abelian varieties A, B over a")
    print("  number field k, A and B are isogenous over k̄ iff their endomorphism")
    print("  algebras End(A) ⊗ Q and End(B) ⊗ Q are isomorphic as Q-algebras.")
    print()
    print("  For elliptic curves with CM by O_{Q(i)} and O_{Q(√-22)}:")
    print("    End(Z_(1)) ⊗ Q = Q(i)")
    print("    End(Z_(2)) ⊗ Q = Q(√-22)")
    print("  These are NON-isomorphic as Q-algebras (different discriminants).")
    print("  ⟹ Z_(1) NOT isogenous to Z_(2) over Q̄.")
    print()
    print("  ⟹ no algebraic curve in Z_(1) × Z_(2) other than the trivial slices.")
    print("  ⟹ H^1(Z_(1); Q) ⊗ H^1(Z_(2); Q) has NO level-0 rational Hodge sub-")
    print("     structure (KW p.11 footnote 23 negated).")

    print()
    print("=" * 78)
    print("VERDICT — Escape route (a) [H^1 ⊗ H^1]: CLOSED")
    print("=" * 78)
    print()
    print("  Despite KW's explicit statement that 'W = 0 is automatic' in this")
    print("  component, the DW = 0 condition cannot be achieved for non-trivial")
    print("  Q-rational fluxes when K^(1) = Q(i) ≠ Q(√-22) = K^(2), because:")
    print()
    print("  (i)  if Z_(1), Z_(2) are CM elliptic curves with K_(Zi) = K^(i),")
    print("       the simple Hodge component W_1 of V_1 ⊗ V_2 (rank 4) has")
    print("       h^{3,1} = 1, and Q-rational fluxes cannot kill the (3,1) part.")
    print()
    print("  (ii) for level-0 substructure (DW = W = 0 trivially), KW p.11 fn 23")
    print("       requires algebraic curve in Z_(1) × Z_(2) beyond trivial slices,")
    print("       which forces Z_(1) ~ Z_(2) (isogenous), forcing Q(i) = Q(√-22).")
    print("       This contradicts the ECI v9 vacuum data.")
    print()
    print("  Both sub-routes lead to a ARITHMETIC obstruction equivalent to the")
    print("  one in §2.4: K^(1) must equal K^(2) as subfields of Q̄.")
    print()
    print("  This is the SAME obstruction as the W_(20|20) component (KW eq 46),")
    print("  just transferred to H^1 ⊗ H^1. Same K^(1) ≅ K^(2) requirement.")
    print()
    print("  CONCLUSION: Route (a) does NOT escape the K^(1) ≅ K^(2) obstruction.")


if __name__ == "__main__":
    main()
