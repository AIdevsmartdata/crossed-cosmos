---
name: M159 Sonnet Williams 2013 thesis Ch 10-11 full survey — (D) PARTIAL — Ch 9 p.81 k=2 algebraicity NEW + Ch 10 Katz measure Thm 10.0.1 verbatim documented
description: Williams 2013 Heidelberg M.Sc. supervisor Venjakob "On elliptic curves with complex multiplication, L-functions, and p-adic interpolation" full 89pp survey. Ch 1-5 prerequisites (no ECI value). Ch 6-7 CM L-functions (background). Ch 8 p-adic interpolation Mahler/Amice + Kummer congruences. Ch 9 Damerell theorem (M135 used) + NEW finding Williams p.81 k=2 algebraicity via G_2*=G_2-π/A regularization. Ch 10 Katz measure Thm 10.0.1 BIVARIATE verbatim — directly citable for R-2 paper IMC. Ch 11 Legendre family illustrative. Hallu 100 held
type: project
---

# M159 — Sonnet Williams 2013 thesis full survey

**Date:** 2026-05-06 | **Hallu count: 100 → 100** held (M159: 0 fabs) | **Mistral STRICT-BAN** | Time ~50min

## Thesis Identity (verbatim verified)

**Title**: "On elliptic curves with complex multiplication, L-functions, and p-adic interpolation"
**Author**: Brandon Williams, Ruprecht-Karls-Universitat Heidelberg, 25 Juli 2013
**Supervisor**: Prof. Dr. Otmar Venjakob

(Note: the title is more precise than what M135 had cached.)

## VERDICT (D) PARTIAL with 2 new findings

**D1 NEW**: Ch 9 p.81 contains a k=2 algebraicity result via G_2* regularization that M135 did NOT use.

**D2 CONFIRMED**: Ch 10 Theorem 10.0.1 gives complete bivariate Katz measure interpolation formula. Directly citable for R-2 paper IMC/Katz measure discussion.

**C1 NEGATIVE**: Ch 11 Legendre family illustrative only.
**C2 NEGATIVE**: Ch 2-5 standard prerequisites.
**C3 NEGATIVE**: Ch 7-8 nothing beyond Silverman/de Shalit.

## Table of Contents (verbatim)

| Ch | Title | Pages |
|----|-------|-------|
| 1 | Introduction | 3-4 |
| 2 | Review of algebraic geometry | 5-14 |
| 3 | Elliptic Curves | 15-27 |
| 4 | Differentials and de Rham cohomology | 28-35 |
| 5 | Formal groups | 36-44 |
| 6 | Complex multiplication | 45-54 |
| 7 | The L-function | 55-64 |
| 8 | p-adic interpolation | 65-71 |
| 9 | Damerell's theorem | 72-81 |
| 10 | Katz's measure | 82-84 |
| 11 | Example: the Legendre family | 85-87 |
| — | Bibliography | 88-89 |

## Ch 9 NEW finding (p.81)

Williams proves B_{2,r} is also algebraic. The formula uses:
$$G_2^* = \frac{1}{\alpha(\alpha - \bar\alpha)} \sum_{s \neq 0} \wp(s/\alpha)$$
with regularized E_2* = E_2 + (π/A)·z̄ - π/A. The argument that wp(s/α) is algebraic over Q(G_4, G_6) uses "the same argument as in 9.3.1."

**M135 did not use or note this k=2 result.** This is the main NEW finding of M159.

## Ch 10 Katz Measure Theorem 10.0.1 (verbatim, pp.82-84)

**Theorem 10.0.1**: There exists a unit c in W^× and for any b in Z coprime to p, a W-valued p-adic measure μ(c,b) on Z_p × Z_p such that:
$$\int_{Z_p \times Z_p} x^{k-3} y^r d\mu(c,b) = 2 c^{k+2r} (b^k - 1) B(k,r)$$

Proof structure:
1. p splits in K → ordinary reduction → Ê ≅ Ĝ_m over W (Lazard + Hensel). Fix φ: Ê → Ĝ_m, get c ∈ W^× from φ_*(c^{-1}ω) = 1/(1+X)dX
2. Universal formal W-deformation E^{univ} over W[a_1,...,a_6]; M̂ = formal completion. φ extends to φ : Ê^{univ} → M̂ × Ĝ_m
3. M̂ ≅ Ĝ_m (Serre-Tate): T = 1+X, L = log(1+X), d/dL = T d/dT
4. Power series f(Z) = b³ ℘'(bZ) - ℘'(Z) in W[[Z]]
5. **Key identity**: (d/dL)^r (D^{k-3}(f))|_{0,0} = 2 c^{k+2r} (b^k - 1) B(k,r)
6. Weil operator W = (-π/A)(ω₁ d/dω₁ + ω̄₂ d/dω₂) corresponds to d/dL via Serre-Tate; A(ω₁, ω₂) = Im(ω̄₁ ω₂)

**Hard constraint**: requires k ≥ 3. The k=1, 2 cases are NOT handled here.

## Recommended Actions for ECI v8.2

1. **Cite Williams Thm 10.0.1** (Ch 10, pp.82-84) in R-2 paper for bivariate Katz measure moments formula
2. **Note Williams p.81 k=2 result** in A72_DAMERELL_EXTENSION or M150_YAGER context — algebraicity of B_{2,r} via G_2* regularization
3. **Primary Katz citation** remains Katz [9] = Invent. Math. 49 (1978), 199-297. Williams is secondary exposition
4. **IMC proper**: requires de Shalit [17] "Iwasawa theory of elliptic curves with complex multiplication: p-adic L-functions" (Academic Press, 1987) — not in Williams scope

## Discipline log

- 0 fabrications
- All theorems / page numbers / bibliography verbatim from /tmp/williams_diplom.pdf via multimodal vision Read
- No Mistral used
- Hallu count: 100 → 100 held
- Time ~50min within 60-min budget
