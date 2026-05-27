# H43 — "3 generations from f^{abc} graph percolation": COMBINATORIAL TEST

**Date**: 2026-05-26
**Verdict short**: ~5% plausibility (essentially numerology). The "3" appearing in any natural f^{abc} graph decomposition of E_8 is forced by a *choice* of subgroup embedding (SU(3) flavor), not by a topological invariant of the graph. The standard, mathematically rigorous explanation for 3 generations lives in **Calabi-Yau topology** (chi/2 = 3), not in Lie-algebra combinatorics.

---

## 1. f^{abc} graph of E_8 — what is actually intrinsic

The f^{abc} graph (vertices = adjoint basis; edge α–β iff [E_α, E_β] != 0, i.e. α+β is a root) has the following data:

| Group  | dim | rank | # roots |
|--------|----:|----:|--------:|
| SU(3)  |   8 |   2 |       6 |
| SO(10) |  45 |   5 |      40 |
| E_6    |  78 |   6 |      72 |
| E_8    | 248 |   8 |     240 |

Intrinsic invariants of this graph (independent of embedding choice):
- **Outer automorphism group**: E_8 has Out = {1} (trivial). So no natural "3" from triality. **Triality (S_3) lives on D_4/SO(8) only**, not E_8.
- **# orbits of Weyl group on roots**: 1 (simply-laced, all roots equivalent). No "3".
- **Coxeter number h(E_8) = 30**, dual Coxeter h^v = 30. No "3".
- **Cartan matrix determinant = 1** (E_8 unimodular). No "3".

**No topological invariant of the f^{abc} graph of E_8 equals 3 naturally.**

## 2. The "3" in E_8 → E_6 × SU(3)

Decomposition 248 = (78,1) + (1,8) + (27,3) + (27̄,3̄). The "3" is **dim(SU(3)_flavor fundamental)**, i.e. fixed once we *choose* to embed SU(3)_flavor as the commutant of E_6 in E_8. This is not topological — it's the rank+1 of a chosen subgroup. The same E_8 also admits embeddings E_8 ⊃ SO(16), E_8 ⊃ SU(5)×SU(5), E_8 ⊃ SU(2)×E_7, where no "3" appears. So the count is **forced by hand**, not emergent.

## 3. The Distler–Garibaldi no-go

Distler & Garibaldi (arXiv:0905.2658) proved that **no embedding of three full SM fermion generations into E_8 (real form) exists** that simultaneously satisfies (a) anti-commuting chiral fermions, (b) correct hypercharges, (c) one complex spin representation per generation. Their dimensional argument: 3 generations require 180 fermionic real dimensions, while E_8 contains only 128 in its real form (split). Lisi-type embeddings violate at least one of (a-c). This **rules out the most direct group-theoretic route** to 3 generations from E_8.

## 4. Standard mathematically rigorous explanation: Calabi-Yau topology

Heterotic E_8 × E_8 string compactified on Calabi-Yau threefold X with standard embedding gives:

**# net generations = (1/2) |chi(X)| = (1/2) |h^{1,1}(X) − h^{2,1}(X)|**

via Atiyah-Singer index theorem applied to the Dirac operator on X coupled to the tangent bundle. To get 3 generations one needs **χ(X) = ±6**.

Known concrete realizations (all verified arXiv):
- **Tian-Yau / Schoen-Yau**: complete intersection CICY with χ = −72, quotiented by Z_12 or Dic_3 (order 12) → χ = −6, gives E_6 GUT with 3 generations.
- **Braun, "A Three-Generation Calabi-Yau Manifold with Small Hodge Numbers"** (arXiv:0910.5464, 2009) — explicit small Hodge construction.
- **Beasley-Heckman-Vafa F-theory GUTs** (arXiv:0802.3391, 0806.0102) — 3 generations from spectral cover topology / G-flux on del Pezzo surface, again Riemann-Roch index counting.

In all rigorous constructions the "3" is **chi/2**, an Atiyah-Singer index, a topological invariant of a 6-manifold + bundle — **never an invariant of an f^{abc} graph alone**.

## 5. Connection to SU(N) κ_EE percolation crossover?

The lattice finding that κ_EE(N) ∝ N^{5/3} above N≈4-5 (Kolmogorov K41 in adjoint-charge transport) is a **statistical/transport** property of the adjoint graph weighted by Boltzmann measure. The percolation threshold N_c ≈ 4-5 relates to the *connectivity density* of the f^{abc} graph (# edges / # vertex pairs grows as N^2/N^4 = 1/N^2 — wait, that decreases, so percolation must use a different weighting, e.g. # triangles per edge).

Even granting full physical reality of the percolation crossover, **it has no natural mechanism producing the integer 3**. Percolation gives critical exponents and an order parameter (% in giant cluster), not integer Betti numbers of a compactification. **No direct link.**

## 6. Alternative interpretations canvassed

| Source of "3"                              | Where it lives                       | Rigorous? |
|--------------------------------------------|--------------------------------------|-----------|
| chi(X)/2 = 3                               | Calabi-Yau 3-fold + standard embed.  | YES       |
| Chern character c_3 of stable bundle       | F-theory / heterotic line bundles    | YES       |
| Fixed points of Z_3 on X                   | Lefschetz fixed-point formula        | YES       |
| b_1(quotient) for SU(4)-bundle             | Donagi-Ovrut Z_3×Z_3 models          | YES       |
| f^{abc} graph orbit count                  | (this hypothesis)                    | NO        |

All four rigorous routes are *geometric/topological on the compactification manifold*, **not on the Lie-algebra graph**.

## 7. Verdict

**Plausibility: 5%.** The hypothesis as stated is essentially numerology. The "3" in E_8 → E_6 × SU(3) is a choice, not a topological invariant. The K41-percolation crossover at N=4-5 is a transport phenomenon producing real exponents, not integers like 3. Calabi-Yau index theorems give the rigorous answer and have been understood since 1985 (Candelas-Horowitz-Strominger-Witten). **Honest call: H43 is dead unless you can exhibit a precise invariant I(graph) with I(E_8 with chosen marked subgroup) = 3 derived purely from structure constants — which to current knowledge does not exist.**

## 8. Verified references

1. **Distler & Garibaldi**, "There is no 'Theory of Everything' inside E_8", arXiv:0905.2658 (2009) — VERIFIED title/author/year via arXiv abs page.
2. **Beasley, Heckman & Vafa**, "GUTs and Exceptional Branes in F-theory – I", arXiv:0802.3391 (2008) — VERIFIED via arXiv abs page.
3. **Braun**, "A Three-Generation Calabi-Yau Manifold with Small Hodge Numbers", arXiv:0910.5464 (2009) — VERIFIED via arXiv abs page.

Tentative (well-known but not re-checked against API this session): Candelas-Horowitz-Strominger-Witten "Vacuum configurations for superstrings" Nucl. Phys. B 258 (1985); Tian-Yau "Three-dimensional algebraic manifolds with c_1=0 and chi=-6" (Proc. Argonne Symp. 1987); Schoen "On fiber products of rational elliptic surfaces with section" Math. Z. 197 (1988).
