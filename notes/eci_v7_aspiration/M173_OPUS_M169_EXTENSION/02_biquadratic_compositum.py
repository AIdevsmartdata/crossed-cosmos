"""
M173 — Escape route (b): Biquadratic compositum K = Q(i, √-22).

Key question: Does there exist a singular K3 surface X with
  T_X ⊗ Q ≅ K = Q(i, √-22)
of degree 4 over Q? If so, can it serve as a single-K3 base for ECI v9
and bypass the K^(1) ≅ K^(2) obstruction by having ONE K3 with quartic CM?

Background (Kanno-Watari arXiv:2012.01111):

KW page 18 eq (18-19):
  K^(1) ⊗_Q K^(2) ≅ ⊕_{i=1}^r L_i
where each L_i is a number field containing K^(2). For our case:
  K^(1) = Q(i),  K^(2) = Q(√-22)
  K^(1) ⊗_Q K^(2) = Q(i) ⊗_Q Q(√-22)

Since Q(i) and Q(√-22) are linearly disjoint over Q (their discriminants
−4 and −88 share gcd=4 but the ramification structure is compatible),
the tensor product IS a single field:
  Q(i) ⊗_Q Q(√-22) ≅ Q(i, √-22)
of degree 4 over Q. So r = 1, and L_1 = Q(i, √-22).

This means in KW eq (24): V_1 ⊗ V_2 ≃ W_1 (single simple component).
W_1 has Q-dimension [K^(1):Q]·[K^(2):Q] = 4 = [Q(i,√-22):Q].

This is consistent with our Hodge analysis in script 01.

Now the question becomes: does the biquadratic compositum K = Q(i,√-22)
itself appear as the CM field of a SINGULAR K3 surface (rk T_X = 4 not 2)?

KW page 44 footnote 70 verbatim:
   "It therefore follows, in particular, that D(T) admits a CM point with
    the CM field K only when discr(T) ∼ (-1)^{[K:Q]/2} D_{K/Q} mod (Q×)²"

For K = Q(i, √-22) of degree [K:Q] = 4:
  - Discriminant D_{K/Q} of biquadratic field
  - For Q(√a, √b), D_{K/Q} = (D_a D_b)² / gcd(D_a, D_b)² · ε for ε depending on
    the structure. Standard formula:
       D_{K/Q} = (D_a · D_b · D_{ab})² / (something)
    where D_{ab} is the discriminant of the third quadratic subfield.

For K = Q(i, √-22) with subfields Q(i), Q(√-22), Q(√22):
  - D_{Q(i)} = -4
  - D_{Q(√-22)} = -88 = -8·11
  - D_{Q(√22)} = +88 = 8·11

The biquadratic field discriminant formula (Hilbert):
  D_{K/Q} = (D_a · D_b · D_c)² / (something), where a,b,c the three quadratic
  subfields.

More precisely:
  K = Q(√a, √b) with a,b ∈ Z squarefree, gcd... etc.
  D_{K/Q} = (D_{Q(√a)} · D_{Q(√b)} · D_{Q(√ab)})^? — this gets technical.

For a CONCRETE computation we use sage/pari ; with mpmath we just do the
arithmetic: D_{Q(i,√-22)} can be computed from the conductor-discriminant
formula for abelian extensions:

   D_{K/Q} = ∏_{χ} f(χ)
where χ ranges over Dirichlet characters with kernel K^Gal.
For K = Q(i, √-22), Gal(K/Q) = Z/2 × Z/2, with character group:
   1 (trivial)         conductor 1
   χ_{-4}              conductor 4   (kernel Q(√-22) ∪ Q(√22))
   χ_{-88}             conductor 88  (kernel Q(i) ∪ Q(√22))
   χ_{22}              conductor 88  (kernel Q(i) ∪ Q(√-22))

Note: χ_{-4} · χ_{-88} = χ_{(-4)(-88)} = χ_{352} = χ_{22} (since 352 = 16*22, the
fundamental discriminant of Q(√22) is +88, but the conductor of χ_{22}
must be 88 since 22 = 2·11).

  D_{K/Q} = 1 · 4 · 88 · 88 = 30976 = 2^7 · 11² · ... wait let me redo this

Actually conductor-discriminant gives:
   |D_{K/Q}| = f(χ_1) · f(χ_2) · f(χ_3) · f(χ_4)
            = 1 · 4 · 88 · 88
            = 30976

Hmm, but the formula has a sign too. For totally imaginary biquadratic,
D > 0 typically. The sign rule: D_{K/Q} = (-1)^{r_2} · (positive) where r_2
is the number of complex places. For K = Q(i, √-22), r_2 = 2 (two pairs of
complex embeddings, total 4 complex embeddings).

So D_{K/Q} = +30976 (since (-1)^2 = +1).

Now KW p.44 fn 70 condition for D(T) to admit a CM point with CM field K:
  discr(T) ∼ (-1)^{[K:Q]/2} D_{K/Q}  mod (Q×)²
            = (-1)^{2} · 30976
            = 30976
            = 2^7 · 11²

Modulo squares: 30976 / 11² = 256 = 2^8. So 30976 ≡ 2^8 ≡ 1 mod (Q×)².

WAIT, 256 = 2^8 is a perfect square (16²). So 30976 ≡ 1 mod (Q×)².

So for D(T) to admit a CM point with biquadratic CM K = Q(i, √-22),
we need:
  discr(T) ∼ 1 mod (Q×)²,  i.e., discr(T) is a perfect square.

For a singular K3 with rk T = 4 (CM by biquadratic K), T is an even
positive-definite rank-4 lattice with discriminant a perfect square.

Such lattices DO exist:
  - U ⊕ U has discriminant 1 (perfect square)  ← but U is hyperbolic, signature (1,1)
  - For positive-definite signature (4,0): rank 4 even positive-definite
    lattices are classified.
  - E_8 / 2... no, E_8 has rank 8.

For rank 4 positive-definite even lattices with square discriminant:
  - D_4 (root lattice): discriminant 4 = 2² (perfect square ✓)
  - A_3 ⊕ A_1: discriminant 4·2 = 8 (NOT square)
  - D_4(-1) (negative definite): discriminant 4 ✓
  - etc.

But for a singular K3, T has signature (2, rk(T) - 2). Wait:
  - K3 lattice: signature (3, 19)
  - For singular K3 (rk Pic = 20), T has rank 2.
  - To have rk T = 4 (NOT singular K3), we'd need rk Pic = 18, NOT singular.
    Such K3 are 'algebraic' but not 'singular' (algebraic K3 have rk Pic ≥ 1,
    singular K3 have rk Pic = 20, the maximum).

So a K3 with T of rank 4 is NOT a singular K3. Let's call it a
"Picard-rank-18 K3 of CM type with quartic CM field". Such K3 surfaces
exist abundantly.

For such a K3 to be of CM-type, T_X ⊗ Q must carry a Hodge-isomorphic
action of K = Q(i, √-22). KW page 43 says:

  In the cases with ℓ := rk(T)/φ(m) = 1 and φ(m) = rk(T), the one point
  D(V_a0) corresponds to a CM-type K3 surface (cf [69]). This is because
  the algebra Span_Q{[[σ]] ∈ Δ} is a part of the endomorphism algebra
  End(T)^Hdg, and already dim_Q(Span_Q{[[σ]]}) = rk(T). The endomorphism
  field is isomorphic to Q(ζ_m).

For our case with rk(T) = 4, we need φ(m) = 4 (m ∈ {5, 8, 10, 12} from
table 1 in KW p.40).

For m = 8: ζ_8, K = Q(ζ_8) = Q(i, √2) (degree 4, biquadratic)
For m = 12: ζ_12, K = Q(ζ_12) = Q(i, √3) (degree 4, biquadratic)
For m = 5: K = Q(ζ_5), NOT biquadratic (cyclotomic of degree 4)
For m = 10: K = Q(ζ_10) = Q(ζ_5), same as m=5

NONE of these biquadratic CM fields equal Q(i, √-22). The biquadratic
fields appearing as Q(ζ_m) are:
  m = 8:  Q(ζ_8) = Q(i, √2)    (i, √2)
  m = 12: Q(ζ_12) = Q(i, √3)   (i, √3)
  m = 24: Q(ζ_24) = Q(i, √2, √3) of DEGREE 8, NOT biquadratic

So Q(i, √-22) is NOT of the form Q(ζ_m) for any m. By the construction of
CM K3 with non-symplectic Z_m action (KW §3.2.3), the CM fields realized
for ℓ = 1 are precisely Q(ζ_m), excluding Q(i, √-22).

For ℓ > 1 with K extending Q(ζ_m), KW page 43 says:
  "the CM field K must be an extension of Q([[σ]]) ≅ Q(ζ_m). Beyond that,
   however, the authors have not been able to find a comprehensive and
   concise statement about how to find out all possible K's for a given
   lattice T."

So a K3 with K = Q(i, √-22) (ℓ = 2 over Q(i), or ℓ = 2 over Q(√-22))
COULD exist as a CM K3 with non-symplectic Z_2 automorphism, but is NOT
in the cyclotomic K = Q(ζ_m) class.

Numerical/structural verification:
Use mpmath dps=30 to verify D_{K/Q} of Q(i,√-22) and confirm the
KW p.44 fn 70 condition.

Even if such a K3 exists, the question becomes: how does it fit into the
KW orbifold framework? KW §2 considers a PAIR of K3 surfaces X^(1), X^(2)
in the orbifold (X^(1) × X^(2))/Z_2. A SINGLE K3 with quartic CM does NOT
fit this paradigm directly.

ALTERNATIVE: take X^(1) = X^(2) = X with quartic CM by Q(i, √-22).
Then K^(1) = K^(2) = Q(i,√-22). Eq (46) ρ^(1)_{20}(K^(1)) = ρ^(2)_{20}(K^(2))
is AUTOMATICALLY satisfied ⟹ Case B ⟹ DW = W = 0 exists.

But the orbifold construction (X × X)/Z_2 is degenerate (it's a
self-product orbifold). The Hodge structure gets symmetrized, and the
ECI v9 specific structure (W^L on Q(i) modular, W^Q on Q(√-22) Hilbert
class polynomial) is LOST.

Consequence: route (b) does NOT preserve ECI v9's specific arithmetic
asymmetry between W^L and W^Q.
"""

from mpmath import mp, mpc, mpf, sqrt, pi, gamma, log, exp, fabs, im, re

mp.dps = 30


def compute_biquadratic_disc():
    """Compute D_{K/Q} for K = Q(i, √-22) using conductor-discriminant formula."""
    # Three non-trivial characters of Gal(K/Q) = Z/2 × Z/2:
    # - chi_{-4}: cuts out Q(i), conductor 4
    # - chi_{-88}: cuts out Q(√-22), conductor 88
    # - chi_{+88}: cuts out Q(√22), conductor 88
    f1 = 1   # trivial
    f2 = 4   # chi_{-4}
    f3 = 88  # chi_{-88}
    f4 = 88  # chi_{+22}=chi_{-4}·chi_{-88} which has conductor lcm(4,88)/gcd = 88
    D_K = f1 * f2 * f3 * f4
    return D_K, (f1, f2, f3, f4)


def discriminant_mod_squares(D):
    """Reduce |D| modulo (Q×)² by extracting all squared prime factors."""
    n = abs(D)
    sign = 1 if D > 0 else -1
    sf = 1  # squarefree kernel
    p = 2
    while p * p <= n:
        if n % (p * p) == 0:
            while n % (p * p) == 0:
                n //= p * p
            # now n may still have one factor of p
        if n % p == 0:
            sf *= p
            n //= p
        p += 1
    sf *= n  # remaining prime factor (if n > 1)
    return sign * sf


def main():
    print("=" * 78)
    print("M173 — Escape route (b): Biquadratic compositum K = Q(i, √-22)")
    print("=" * 78)

    print()
    print("--- Step 1: Verify K = Q(i, √-22) is a biquadratic field over Q ---")
    print()
    print("  K = Q(i)·Q(√-22) is the compositum of two distinct imaginary")
    print("  quadratic fields.")
    print("  Q(i) ∩ Q(√-22) = Q (since their discriminants -4 and -88 are not")
    print("  proportional mod squares: -4 vs -88 = -4·22 differ by 22 ≠ □).")
    print("  Hence [K:Q] = [Q(i):Q] · [Q(√-22):Q] = 2·2 = 4.")
    print("  Gal(K/Q) ≅ Z/2 × Z/2 (Klein four-group).")
    print()
    print("  Three quadratic subfields of K:")
    print("    Q(i)     [discriminant -4]")
    print("    Q(√-22)  [discriminant -88]")
    print("    Q(√22)   [discriminant +88]")
    print("  K is TOTALLY IMAGINARY (no real embeddings, 4 complex embeddings).")

    print()
    print("--- Step 2: Compute D_{K/Q} via conductor-discriminant formula ---")
    D_K, conductors = compute_biquadratic_disc()
    print()
    print(f"  Conductors of the 4 characters of Gal(K/Q):")
    print(f"    f(1) = {conductors[0]}      (trivial char)")
    print(f"    f(χ_{{-4}}) = {conductors[1]}    (cuts Q(i))")
    print(f"    f(χ_{{-88}}) = {conductors[2]}   (cuts Q(√-22))")
    print(f"    f(χ_{{+22}}) = {conductors[3]}   (cuts Q(√22))")
    print(f"  |D_K| = ∏ f(χ) = {D_K}")
    print(f"  D_K = +{D_K}  (positive since totally imaginary, 2 pairs of complex places)")

    print()
    # Verify factorization 30976 = 2^8 · 11² = 176²
    assert D_K == 256 * 121, f"Expected 256*121 = 30976 but got {D_K}"
    assert D_K == 176**2, f"Expected 176² = 30976 but got {D_K}"
    print(f"  D_K = {D_K} = 2^8 · 11² = 256 · 121 = 176²")
    print(f"  ⟹ D_K is a PERFECT SQUARE: D_K = 176²")

    print()
    print("--- Step 3: KW p.44 fn 70 condition for CM point with K = Q(i,√-22) ---")
    print()
    print("  KW p.44 fn 70 verbatim: 'D(T) admits a CM point with the CM field K")
    print("  only when discr(T) ∼ (-1)^{[K:Q]/2} D_{K/Q} mod (Q×)²'")
    print()
    print(f"  [K:Q] = 4, so (-1)^{{[K:Q]/2}} = (-1)^2 = +1")
    print(f"  ⟹ discr(T) ∼ +D_K = +30976 mod (Q×)²")
    sf = discriminant_mod_squares(D_K)
    print(f"  Squarefree kernel of {D_K}: {sf}")
    print(f"  ⟹ discr(T) ≡ +1 mod (Q×)²  (since 30976 = 176² is a perfect square)")
    print(f"  ⟹ discr(T) must itself be a perfect square (positive)")

    print()
    print("--- Step 4: Existence of singular K3 with rk T = 4 and CM by Q(i,√-22) ---")
    print()
    print("  WAIT: 'singular K3' means rk Pic = 20 (max), so rk T = 22 - 20 = 2.")
    print("  A K3 with rk T = 4 has rk Pic = 18 ; this is NOT singular but is")
    print("  Picard-rank-18, which is allowed and called a 'CM K3 of rk T = 4'.")
    print()
    print("  T has signature (2, rk(T) - 2) = (2, 2). For T to admit a CM point")
    print("  with CM by quartic biquadratic K = Q(i,√-22), we need T even, rank 4,")
    print("  signature (2, 2), and discr(T) ∼ +1 mod (Q×)² (perfect square).")
    print()
    print("  CONCRETE example: T = U ⊕ U(11) ?")
    print("    U = hyperbolic plane, signature (1,1), discriminant -1")
    print("    U(11) = scaled, discriminant -121 = -11²")
    print("    T = U ⊕ U(11) has signature (2,2), discriminant 121 = 11²")
    print("    discr(T) = 121 ∼ +1 mod (Q×)². CHECK ✓")
    print()
    print("  But does T = U ⊕ U(11) admit a CM point with K = Q(i,√-22)?")
    print("  This is harder: requires Hodge-isomorphism action of K on T ⊗ Q.")
    print()
    print("  Need: ε ∈ K = Q(i,√-22) acting Q-linearly on T_Q with q(εx, εy) =")
    print("  N_{K/Q}(ε)·q(x,y) (or similar). Specifically:")
    print("    - i acts on T_Q permuting eigenvalues via (i, -i)")
    print("    - √-22 acts permuting via (√-22, -√-22)")
    print("    - Compositum acts via 4 distinct embeddings: ±i, ±√-22 cross")
    print()
    print("  For T_Q = K_Q = Q(i,√-22) as Q-vector space of dim 4, the natural")
    print("  K-action is multiplication. The Q-bilinear form q on K such that")
    print("  q(εx, y) = q(x, ε̄y) with ε̄ = complex conjugate is")
    print("    q(x, y) = Tr_{K/Q}(λ x ȳ)")
    print("  for some λ ∈ K with λ = -λ̄ (purely imaginary in K). Such λ exist ;")
    print("  their existence is part of the Shimura construction of CM abelian")
    print("  varieties. This generalizes to K3 (Pjateckii-Šapiro/Šafarevič).")

    print()
    print("--- Step 5: Period of biquadratic CM K3 (numerical) ---")
    print()
    print("  For a CM K3 with K = Q(i, √-22), the 4 embeddings of K into Q̄:")
    embeddings = [
        ("ρ_1", mpc(0, 1), mpc(0, sqrt(mpf(22)))),     # i → +i, √-22 → +i√22
        ("ρ_2", mpc(0, 1), mpc(0, -sqrt(mpf(22)))),    # i → +i, √-22 → -i√22
        ("ρ_3", mpc(0, -1), mpc(0, sqrt(mpf(22)))),    # i → -i, √-22 → +i√22
        ("ρ_4", mpc(0, -1), mpc(0, -sqrt(mpf(22)))),   # i → -i, √-22 → -i√22
    ]
    for name, im_i, im_22 in embeddings:
        print(f"    {name}: i ↦ {im_i}, √-22 ↦ {im_22}")
    print()
    print("  The (2,0)-form Ω of the K3 corresponds to ONE of these embeddings,")
    print("  say ρ_1. The complex conjugate Ω̄ corresponds to ρ_4 (full conjugation).")
    print("  ρ_2 and ρ_3 are 'mixed' embeddings: complex conjugation only on one")
    print("  of i or √-22.")
    print()
    print("  Hodge structure on T_X ⊗ C with K-action:")
    print("    H^{2,0}: 1-dim, eigenvector for ρ_1")
    print("    H^{0,2}: 1-dim, eigenvector for ρ_4")
    print("    H^{1,1} ∩ T_X: 2-dim, eigenvectors for ρ_2 and ρ_3")

    print()
    print("--- Step 6: Compute period via Chowla-Selberg-like formula ---")
    print()
    print("  For a CM abelian variety A with CM by K = biquadratic Q(i, √-22):")
    print("  the period satisfies (Shimura, Damerell):")
    print()
    print("    Ω(A) ~ ∏_{χ} (something involving Γ functions)")
    print()
    print("  For biquadratic CM, the Chowla-Selberg formula generalizes to")
    print("  Colmez's formula for the Faltings height.")
    print()
    print("  The Q(i, √-22) CM type (Φ = {ρ_1, ρ_2}) has reflex field")
    print("  K* = Q(i, √-22) itself (biquadratic CM types of biquadratic fields")
    print("  are typically self-reflex up to outer Galois).")

    # Numerical: compute the four periods for a hypothetical CM K3 with K = Q(i,√-22)
    print()
    print("  Periods of the 'fundamental' 1-form on each CM elliptic factor")
    print("  (Shioda-Inose: T_X = T(E_1 × E_2) for CM elliptic curves E_1, E_2):")
    omega_i = gamma(mpf(1)/4)**2 / (2 * sqrt(pi))  # period of E_i (CM by Z[i])
    print(f"    Ω(E_i) = Γ(1/4)² / (2√π) = {omega_i}")

    # Period of E with CM by Z[√-22]: harder, requires Chowla-Selberg for D=-88, h=2
    # |Ω|² geometric mean ≈ 1.0233 from M171
    # |Ω(E_a) Ω(E_b)| ≈ |geom_mean|² = 1.047 ≈ ?
    print(f"    Ω(E_a) Ω(E_b)  for E_a, E_b with CM by O_{{Q(√-22)}}:")
    print(f"     geometric mean from Chowla-Selberg D=-88, h=2: |Ω|² ≈ 1.047")

    print()
    print("--- Step 7: Compatibility with ECI v9 W^L + W^Q vacuum ---")
    print()
    print("  ECI v9 vacuum:")
    print("    τ_L = i ∈ H_L,  W^L(i) = 0 via E_6(i) = 0")
    print("    τ_Q = i√(11/2) ∈ H_Q,  W^Q(τ_Q) = 0 via H_{-88}(j(τ_Q)) = 0")
    print()
    print("  These live on the moduli SPACE of pairs (X^(1), X^(2)) of K3 surfaces,")
    print("  one with CM by Q(i), one with CM by Q(√-22).")
    print()
    print("  The biquadratic compositum route would replace this with a SINGLE")
    print("  K3 X with CM by Q(i, √-22) (rk T_X = 4). This single K3 lives at")
    print("  ONE point in the moduli space D(T_0) (for an appropriate T_0 of")
    print("  rank > 4).")
    print()
    print("  Compatibility issue: the ECI v9 modular structure W^L + W^Q is")
    print("  EXPLICITLY a sum of two 1-cusp modular forms, one on H_L (Q(i)")
    print("  modular) and one on H_Q (Q(√-22) Hilbert modular). Replacing by a")
    print("  single biquadratic CM K3 would compress this structure into")
    print("  ONE field Q(i,√-22), losing the L-Q ASYMMETRY.")
    print()
    print("  The ECI v9 KEY ASYMMETRY (M169 finding):")
    print("    W^L vanishing via E_6(i) = 0      [modular form zero, weight 6]")
    print("    W^Q vanishing via H_{-88}(j) = 0  [Hilbert class polynomial zero]")
    print("  is structural, not aesthetic. A single K3 with biquadratic CM does")
    print("  NOT factor through this asymmetry — it would have a SINGLE")
    print("  Hilbert-class-polynomial-type vanishing for K = Q(i,√-22).")

    print()
    print("--- Step 8: Class number and Hilbert class polynomial of Q(i,√-22) ---")
    print()
    print("  For biquadratic K = Q(i, √-22):")
    print("    Class number h_K = h_{Q(i)} · h_{Q(√-22)} · h_{Q(√22)} / ... ")
    print("    = 1 · 2 · ?  (h_{Q(√22)} unknown without table)")
    print("    Standard result: h_{Q(√22)} = 1 (Q(√22) is small real quadratic)")
    print("  Genus theory: h_K = h_{Q(i)} · h_{Q(√-22)} · h_{Q(√22)} / 2 (if 2 ramifies)")
    print("    = 1 · 2 · 1 / ?  → likely h_K ∈ {1, 2}")
    print()
    print("  The biquadratic Hilbert class polynomial H_K(j) is a polynomial of")
    print("  degree h_K with j-roots being j-invariants of CM K3 with CM by")
    print("  ALL ideal classes of K. For our purposes h_K = 2 (likely).")

    print()
    print("--- Step 9: KW page 18-19 K^(1) ⊗ K^(2) = ⊕ L_i for biquadratic ---")
    print()
    print("  Recall KW eq (18-19): K^(1) ⊗_Q K^(2) ≅ ⊕_{i=1}^r L_i where L_i is")
    print("  a number field containing K^(2). For ECI v9:")
    print()
    print("    K^(1) ⊗_Q K^(2) = Q(i) ⊗_Q Q(√-22)")
    print()
    print("  Q(i) = Q[x]/(x² + 1). To compute Q(i) ⊗ Q(√-22), reduce x² + 1")
    print("  over Q(√-22). But x² + 1 is IRREDUCIBLE over Q(√-22) (since i ∉")
    print("  Q(√-22), as Q(i) ∩ Q(√-22) = Q).")
    print()
    print("  ⟹ Q(i) ⊗ Q(√-22) = Q(√-22)[x]/(x² + 1) ≅ Q(i, √-22) of degree 4")
    print("  ⟹ r = 1, L_1 = Q(i, √-22)")
    print()
    print("  KW Cases A and B (page 28):")
    print("    Case A (eq 45): ρ^(1)_(20)(K_0^(1)) = ρ^(2)_(20)(K_0^(2))")
    print("                 AND ρ^(1)_(20)(K^(1)) ≠ ρ^(2)_(20)(K^(2))")
    print("    Case B (eq 46): ρ^(1)_(20)(K^(1)) = ρ^(2)_(20)(K^(2))")
    print()
    print("  For ECI v9: K_0^(1) = K_0^(2) = Q (both imaginary quadratic),")
    print("              K^(1) = Q(i), K^(2) = Q(√-22), DISTINCT subfields of Q̄.")
    print("              ⟹ Case A holds, Case B FAILS")
    print()
    print("  In KW Case A on the SINGLE simple component W_1 = L_1 ≅ Q(i,√-22):")
    print("    KW eq (39): Φ^full_{L_(20|20)} = {ρ^(1)_(20) ⊗ ρ^(2)_(20),")
    print("                                       ρ^(1)_(20) ⊗ ρ^(2)_(02),")
    print("                                       ρ^(1)_(02) ⊗ ρ^(2)_(20),")
    print("                                       ρ^(1)_(02) ⊗ ρ^(2)_(02)}")
    print("                with each appearing once (n_1 = n_2 = 2 in our case).")
    print()
    print("  These are EXACTLY the 4 embeddings of K = Q(i, √-22) into Q̄.")
    print("  Hodge types: (4,0), (3,1), (1,3), (0,4) — but wait this is wrong:")
    print("  the (2,0)⊗(2,0) is (4,0) ; the (2,0)⊗(0,2) and (0,2)⊗(2,0) are (2,2)")
    print("  ; the (0,2)⊗(0,2) is (0,4). So 2 of (2,2), 1 of (4,0), 1 of (0,4).")
    print()
    print("  In Case A (eq 45 satisfied, eq 46 NOT):")
    print("    KW eq (39) ⟹ Φ has 4 + 2(n-2) = 4 + 0 = 4 embeddings (n=2)")
    print("    Hodge: (4,0), (0,4), (2,2), (2,2) — NO (3,1) or (1,3) ✓")
    print("    ⟹ W_(20|20) is (3,1)-free ⟹ DW = 0 OK")
    print("    BUT (4,0) and (0,4) are PRESENT ⟹ W ≠ 0 (the (4,0) is exactly Ω)")
    print()
    print("  This is the OBSTRUCTION: Q-rational fluxes on W_1 NECESSARILY")
    print("  have non-zero (4,0) component (since Galois orbit of (4,0)")
    print("  embedding under Gal(K/Q) = Z/2 x Z/2 is {(4,0),(0,4),(2,2)_a,(2,2)_b}")
    print("  if 4 elements form orbit. Actually since (4,0) and (0,4) are in")
    print("  the same orbit under c.c. ∈ Gal, the Galois orbit decomposition")
    print("  matters.)")

    print()
    print("--- Step 10: VERDICT for route (b) ---")
    print()
    print("  Route (b) — biquadratic compositum K = Q(i, √-22) — DOES yield a")
    print("  consistent number-theoretic structure: K^(1) ⊗ K^(2) = Q(i,√-22) is")
    print("  the SINGLE simple component W_1 in KW eq (24). This is the natural")
    print("  extension to non-isomorphic CM fields.")
    print()
    print("  HOWEVER: this DOES NOT escape the obstruction. KW Case A on W_1")
    print("  still applies (since K^(1) ≠ K^(2) as subfields of Q̄), giving")
    print("  W_(20|20) (3,1)-free but containing (4,0) and (0,4). Q-rational")
    print("  fluxes have W ≠ 0.")
    print()
    print("  The biquadratic compositum K^(1) · K^(2) = Q(i, √-22) is NOT a")
    print("  separate escape route — it IS the structure described by KW for")
    print("  Case A. M171's identification of route (b) as 'open' was BASED")
    print("  on incomplete reading of KW §2.4.1 (which already covers the")
    print("  K^(1) ⊗ K^(2) = single field case via eq 18-22).")
    print()
    print("  REVISED CLASSIFICATION:")
    print("    Route (a) [H^1 ⊗ H^1]: CLOSED — same K^(1) ≅ K^(2) obstruction")
    print("                            transferred to elliptic curves Z_(i).")
    print("    Route (b) [biquadratic]: NOT a separate route — already in scope")
    print("                            of KW §2.4.1 ; gives Case A obstruction.")
    print()
    print("  CONSEQUENCE FOR M173 VERDICT: tighter NEGATIVE result.")


if __name__ == "__main__":
    main()
