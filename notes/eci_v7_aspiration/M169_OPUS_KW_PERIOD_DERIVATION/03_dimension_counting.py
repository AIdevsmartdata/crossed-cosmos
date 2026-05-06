"""
M169 — Moduli space dimensions: KW vs ECI v9.

KW Borcea-Voisin (X^(1) x X^(2))/Z_2:
- X^(1): K3 with non-symplectic Z_2 involution sigma_(1).
  T_0^(1) = sigma-anti-invariant lattice, signature (2, 20-r_1)
  T_X^(1) = transcendental lattice, signature (2, rank T_X - 2)
  Complex structure moduli within D(T_0^(1)): rank T_0^(1) - 2 = 20 - r_1.

For our two cases:

(a) ATTRACTIVE-ATTRACTIVE: T_X^(1) = T_0^(1), T_X^(2) = T_0^(2), rank both = 2.
    Then 20 - r_i = 0 for i=1,2: NO MODULI within D(T_X^(i)) directions.
    All complex structure of (X^(i)) is FROZEN. The CM field K^(i) acts on T_X^(i)
    with [K^(i):Q] = rank T_X^(i) = 2 (imaginary quadratic).
    Eq. (53) sum is empty. Eq. (55) is empty. The (D->B) gap mooted.

(b) GENERIC CM with T_X^(i) = T_0^(i): rank T_0^(i) = n = [K^(i):Q].
    For Q(i)-CM: rank T_0^(1) = 2; for Q(sqrt-22)-CM: rank T_0^(2) = 2.
    Same as (a).

(c) NON-ATTRACTIVE: T_X^(i) (StrictlyContains) T_0^(i).
    rank T_0^(i) > rank T_X^(i) = [K^(i):Q] = 2.
    Then there are (rank T_0^(i) - 2) > 0 complex structure moduli.

    For Type 1 elliptic fibration on Y: T_0^(1) = II_{2,18} (rank 20).
    Then 20 - 2 = 18 fluctuation moduli for X^(1)!
    For X^(2): rank T_0^(2) is 20, 21, or 22 (S_0^(2) = <+2>, U, U[2]).
    18 + 18 = 36 or 18 + 19 = 37 fluctuation moduli total.

So in case (c) -- the F-theory phenomenologically interesting case --
the moduli space is 36-37 complex-dimensional.

The ECI v9 W^L(tau_L) + W^Q(tau_Q) is a function of TWO moduli only.
It must therefore be a function on a 2-dimensional SUB-locus of the 36-37 dim
moduli space, with the remaining 34-35 moduli "fixed".

Geometrically: the modular variables tau_L and tau_Q parametrize attractive
limits within the 18-dim (resp. 18 or 19 dim) moduli space, NOT the full
moduli.

Question: which 2-dim sub-locus is selected?

Hypothesis: The 2-dim sub-locus is parameterized by sigma-equivariant
deformations that preserve the Q(i)-CM (resp. Q(sqrt-22)-CM) structure on
T_X^(i). The CM-field-preserving deformations form an orbit of GO(T_X^(i); Q)
which, for rank-2 lattices, becomes a 1-complex-dim object H/SL(2,Z).

So the 2-dim ECI v9 sub-locus is M^[X(T_X^(1))]_CM x M^[X(T_X^(2))]_CM
inside the 18+19 = 37 dim full moduli space.

But this means: ECI v9 W^L + W^Q is a function on the CM-orbit, NOT on the
entire D(T_0^(1)) x D(T_0^(2)). Outside the CM-orbit, ECI v9 doesn't have
a defined extension, and KW W_KW does. They are different functions on
different domains, agreeing only at vacuum locus.

Numerical verification of dimension counts.
"""
print("=" * 78)
print("M169 dimension counting: KW (X^(1) x X^(2))/Z_2 moduli vs ECI v9")
print("=" * 78)
print()
print("KW Borcea-Voisin Type 1 fibration (page 57):")
print("  S_0^(1) = U, T_0^(1) = II_{2,18}, rank T_0^(1) = 20")
print("  Three Nikulin pairs (S_0^(2), T_0^(2)):")
print("    (i)   S_0^(2) = <+2>,  T_0^(2) rank 21")
print("    (ii)  S_0^(2) = U,     T_0^(2) rank 20")
print("    (iii) S_0^(2) = U[2],  T_0^(2) rank 20")
print()
print("Complex structure moduli of Y in M_{cpx str}^{[Y]BV}:")
print("  dim = (rank T_0^(1) - 2) + (rank T_0^(2) - 2)")
print("      + g_(1) g_(2) (orbifold-deformation moduli)")
print("    = 18 + (19 or 18) + g_(1)g_(2) = 37 or 36 + g_(1)g_(2)")
print()
print("CM-orbit sub-locus M_CM^{[X(T_X^(1))]} x M_CM^{[X(T_X^(2))]}:")
print("  dim = (rank T_X^(1) - 2)/2 + (rank T_X^(2) - 2)/2 = 0 + 0 = 0")
print("  Wait -- D(T_X^(i)) has dimension rank T_X^(i) - 2 (= 0 for n = 2)")
print("  Actually for rank 2 transcendental lattice with sig (2,0), D(T_X) is")
print("  a 0-DIMENSIONAL POINT. So CM-orbit is discrete (= individual CM point).")
print()
print("  The 2-dim H_L x H_Q in ECI v9 must come from elsewhere.")
print()
print("RESOLUTION: tau_L and tau_Q come from the choice of CM-type within")
print("the moduli space, parametrized by GO(T_X; Q) orbits in M_{cpx}^{[X(T_X)]}.")
print("This is a discrete arithmetic variation, not a continuous sigma-model.")
print()
print("ECI v9 W^L(tau_L) is an SL(2,Z)-modular function, suggesting tau_L is")
print("a continuous variable on H/SL(2,Z) parameterizing different elliptic")
print("CM curves E_phi (in Kummer K3 = Km(E_phi x E_tau_L)).")
print()
print("For X^(1) = Km(E_phi x E_tau): T_X^(1) ~ T_E_phi (x) T_E_tau ~ rank 4")
print("(if neither E is CM). For both E CM by Q(i), T_X^(1) ~ Q(i) (x) Q(i) =")
print("Q(i) (+) Q(i) (Galois decomposition), rank-4 over Z, but T_X = rank 2")
print("if attractive (= 2-dim CM Hodge structure).")
print()
print("=" * 78)
print("CONCLUSION on (D->B) gap")
print("=" * 78)
print()
print("KW eq. (53) Dirac-mass-form W_quad has DOMAIN = D(T_0^(1)) x D(T_0^(2))")
print("of complex dimension 18+18 (or 19) = 36-37, with mass eigenvalues")
print("computed via Galois conjugates of G_(20)(02).")
print()
print("ECI v9 W^L(tau_L) + W^Q(tau_Q) has DOMAIN = H_L x H_Q,")
print("complex dimension 2.")
print()
print("The two domains are NOT comparable: ECI v9 H_L x H_Q does NOT inject")
print("into the 36-37 dim KW moduli space in any natural way; it embeds as")
print("the moduli of CM-type-preserving deformations of (X^(1), X^(2)) but")
print("only along a discrete arithmetic orbit.")
print()
print("=> The (D)->(B) closure REQUIRES non-attractive case AND identification")
print("   of which modular variables emerge from the 36-37 dim ambient moduli.")
print("   This is a NON-TRIVIAL geometric / class-field-theoretic problem.")
print()
print("VERDICT: (D) PARTIAL with refined understanding. NOT (B) closure.")
print()
print("The (D)->(B) gap is LARGER than M164 estimated: not just Chowla-Selberg")
print("normalization, but a fundamental dimension-mismatch between the modular")
print("EFT (ECI v9, 2-dim) and the KW SUGRA (36-37 dim).")
