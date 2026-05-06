# M176 sub-task 1 — Schütt 2008 verbatim Shioda-Inose recipe extraction

PDF Read pages 1-19 of arXiv:0804.1558v3 ("K3 surfaces with Picard rank 20", M. Schütt, Hannover, 2010 final form).

## Theorem 3 (Pjateckii-Šapiro / Šafarevič / Shioda-Inose) — page 2 verbatim

> "The map X → T(X) gives a bijection
> {Singular K3 surfaces}_{/≅} ↔1:1 {positive-definite oriented even lattices of rank two}_{/≅}.
> The injectivity of this map follows from the Torelli theorem for singular K3 surfaces [16]. For the surjectivity, Shioda-Inose exhibited an explicit construction involving isogenous CM-elliptic curves E, E' [32]. This is often referred to as Shioda-Inose structure:"

Then on page 3 verbatim:

>          E × E'             X
>              \\           //
>           Km(E × E')
> 
> "Here both rational maps are 2:1, and T(X) ≅ T(E × E'). Shioda-Inose exhibited the rational map X --> Km(E × E') through base change of elliptic fibrations. Explicit equations were subsequently given by Inose in [10]. In [21], Inose's results were improved to derive a model over the ring class field H(d) associated to the discriminant d = disc(T(X)) of the transcendental lattice (cf. Lemma 33). Over some extension, one can moreover determine the ζ-function of X (Theorem 29)."

## Theorem 2 (field of definition obstruction) — page 2 verbatim

> "Let L be a number field and X a K3 surface of Picard rank 20 over L. Denote the discriminant of X by d < 0. Then L(√d) contains the ring class field H(d)."

## Lemma 33 (page 15, M176 PDF Read p.15 verbatim)

> "Let X be a singular K3 surface of discriminant d. Then X has a model over the ring class field H(d)."

## Theorem 29 (Shioda-Inose [32, Theorem 6]) — page 14 verbatim

> "Upon increasing the base field, the ζ-function of a singular K3 surface X splits into one-dimensional factors. Then the L-function of the transcendental lattice factors as
> 
>   L(T(X), s) = L(ψ², s) L(ψ̄², s)
> 
> where ψ is the Hecke character associated to an elliptic curve with CM in K. Here one can choose the elliptic curve E identified with the transcendental lattice T(S) under the map
> 
>   ⎛ 2a   b  ⎞      -b + √(b² - 4ac)
>   ⎜       ⎟  →  τ = ──────────────  →  E = ℂ/(ℤ + τℤ)."
>   ⎝ b   2c  ⎠            2a

## Proposition 28 (page 14 verbatim)

> "Let L be a quadratic extension of ℚ and X be a K3 surface with Picard rank 20 over L. As before, let T(X) denote the transcendental lattice, d its discriminant and K = ℚ(√d). Then:
>   (i) If L = K, then d has class number one.
>   (ii) If L ≠ K, then d has class number one or two. In the latter case, the compositum LK agrees with the ring class field H(d)."

## Page 15 conclusion verbatim

> "If L ≠ K, then Proposition 14 tells us that all the primes that split in both K and L are principal. Hence K has class number one or two. By the argumentation of section 8, all these p are principal in Cl(d) as well (as mentioned in Remark 31). Hence, d has class number one or two. In the latter case, LK = H(d) by class field theory."

## Page 16 Lemma 34 (genus condition) verbatim

> "Let X be a singular K3 surface over some number field L. In the above notation, M ⊂ KL."
> 
> where M is "the fixed field of G in the abelian Galois extension H(d')/K", with G = Cl(d')[2], the two-torsion subgroup of Cl(d').

## EXTRACTED RECIPE for ECI v9 / Q(√-22), d = -88, h(d) = 2

By **Shioda-Inose Theorem 3** + **Theorem 29**:

For each transcendental lattice T(X) of rank 2, even, positive-definite, with disc(T(X)) = -88 and Cl(T(X)) ≅ ℤ/2 (a quadratic form class), the singular K3 X is constructed as follows:

**Step (a)** — Pick the binary form (a, b, c) ↔ Gram matrix (2a, b; b, 2c) representing T(X). For class [1] of D = -88: form (1, 0, 22), Gram (2, 0, 0, 44). For class [2]: form (2, 0, 11), Gram (4, 0, 0, 22).

**Step (b)** — Compute τ_α = (-b + √(b² - 4ac))/(2a):
  - τ_a = i√22 (for class [1])
  - τ_b = i√(11/2) = i√22/2 (for class [2])

**Step (c)** — Identify CM elliptic curve E_α with j-invariant equal to one of the two roots of H_{-88}(X):
  - j(E_a) = 3,147,421,320,000 + 2,225,561,184,000·√2
  - j(E_b) = 3,147,421,320,000 − 2,225,561,184,000·√2
  Both ∈ ℚ(√2) = HCF intersection ℚ̄.
  Hilbert class field H(-88) = K(j(E_a)) = ℚ(√-22, √2) — a biquadratic extension of ℚ of degree 4, abelian over ℚ.

**Step (d)** — Form the product abelian surface E_a × E_a (or E_b × E_b for class [2]). Take the Kummer surface Km(E_a × E_a) — desingularization of (E_a × E_a)/⟨−1⟩.

**Step (e)** — Construct the singular K3 X as the unique double cover of Km(E_a × E_a) ramified along the appropriate divisor (Shioda-Inose [32], explicit equations Inose [10]).

**Step (f)** — Schütt Theorem 29 then gives:
  L(T(X_a), s) = L(ψ_a², s) · L(ψ̄_a², s)
where ψ_a is the Hecke character of E_a, of ∞-type 1 with CM by K = ℚ(√-22). Squaring gives ∞-type 2.

## Critical structural fact for ECI v9

The transcendental lattice T(X_b) of singular K3 X_b for class [2] (form (2,0,11), τ_b = i√(11/2)) is the ECI v9 anchor. Its Gram matrix is

  G_b = [[ 4   0 ]
         [ 0  22 ]]

with determinant det(G_b) = 88 and discriminant disc(T(X_b)) = -88.

Since X_b has Picard rank 20 over a number field L, by Theorem 2: L(√−88) = L·ℚ(√−22) ⊃ H(−88) = ℚ(√−22, √2). Hence L ⊃ ℚ(√2) at minimum.

In particular, **X_b is not defined over ℚ** (this would require disc class number 1 by Corollary 15 of Schütt; we have h(d) = 2).

## Field of moduli analysis

For class group action: Cl(d=−88) ≅ ℤ/2ℤ (two-torsion only), so by Schütt's Lemma 34 setup, the field M = H(d')/K^{Cl(d')[2]} fixed field, here d' = d = −88 (since d is fundamental), so Cl(d')[2] = full Cl(d') = ℤ/2ℤ, hence M = K. Thus M ⊂ KL imposes K ⊂ KL, trivially satisfied. The genuine obstruction is

  L · K ⊃ H(-88) = ℚ(√-22, √2)

so L must contain the ring class field H(-88) = ℚ(√-22, √2) over ℚ as soon as one wants both K3 surfaces (X_a, X_b) defined over L.

If we want X_b alone (class [2]), then by Lemma 33 it has a model over H(-88) = ℚ(√-22, √2).

**Minimal field of definition for X_b: ℚ(√-22, √2) of degree 4 over ℚ, biquadratic, Galois group V_4 = ℤ/2 × ℤ/2.**

## Conclusion for sub-task 1

Schütt 2008 furnishes a COMPLETE EXPLICIT recipe at the level of:
- (1) bijection rank-2 lattice ↔ singular K3 (Theorem 3, by Shioda-Inose [32]);
- (2) explicit Inose fibration model over H(d) (Lemma 33, refines Shioda-Inose [32]);
- (3) ζ-function as L(ψ²) · L(ψ̄²) (Theorem 29).

The MISSING explicit input is Inose's [10] explicit Weierstrass equations of the singular K3 X (1977 Symposium proceedings, hard to obtain in 2026). However the construction method (E × E' → Km(E × E') → X via 2:1 base-change of elliptic fibrations) is fully specified.

For Q(√-22) class [2] anchor, Schütt page 12 TABLE shows discriminants up through −163 with class number one; d = −88 is explicitly NOT in that table (h(d) = 2), but Section 12 (Proposition 28) covers exactly the h(d) = 2 case via biquadratic descent.
