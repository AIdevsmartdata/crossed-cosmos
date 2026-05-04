# Literature Check — Gate G1 (S'_4 hatted multiplet Hecke closure)

**Date:** 2026-05-04 (evening)  •  **Author:** G1 agent  •  **ORCID:** 0009-0008-2443-7166

All references verified at runtime by `gate_g1_hatted.py` via the live arXiv API endpoint
`https://export.arxiv.org/api/query?id_list=<id>`. Anti-hallucination tag: every metadata
field below was returned by the public API and is reproducible.

---

## Primary references (load-bearing)

| Tag      | arXiv ID    | Status     | Title (verified)                                                                | Authors (verified)                          | Journal                                |
|----------|-------------|------------|---------------------------------------------------------------------------------|---------------------------------------------|----------------------------------------|
| [NPP20]  | 2006.03058  | VERIFIED   | "Double Cover of Modular S_4 for Flavour Model Building"                         | P. P. Novichkov, J. T. Penedo, S. T. Petcov | Nucl. Phys. B 963 (2021) 115301        |
| [LYD20]  | 2006.10722  | VERIFIED   | "Modular Invariant Quark and Lepton Models in Double Covering of S_4 Modular Group" | X.-G. Liu, C.-Y. Yao, G.-J. Ding         | Phys. Rev. D 103, 056013 (2021)        |
| [dMVP26] | 2604.01422  | INHERITED  | "Quark masses and mixing from Modular S'_4 with Canonical Kähler Effects"        | de Medeiros Varzielas, Paiva                | (no journal-ref as of 2026-05-04)      |

DOIs (verified via arXiv API):
- [NPP20] DOI: 10.1016/j.nuclphysb.2020.115301
- [LYD20] DOI: 10.1103/PhysRevD.103.056013

The [dMVP26] entry is INHERITED from E2/B3 morning verification (2026-05-04 forenoon) as
described in `/tmp/agents_v647_evening/E2/numerical_closure.md` §1; it was not re-verified
here because it is not load-bearing for G1 (no formula extracted from it). Tag: still
"no journal-ref" as of today.

## Equations transcribed from the NPP20 PDF

**Eq. (3.3)** [NPP20 page 8]:
- θ(τ) = Θ_3(2τ) = Σ_{k ∈ Z} q_4^{(2k)²} where q_4 = exp(iπτ/2)
- ε(τ) = Θ_2(2τ) = Σ_{k ∈ Z} q_4^{(2k-1)²} = 2 Σ_{k≥1} q_4^{(2k-1)²}

**Eq. (3.13)** [NPP20 page 9]: q_4-expansions of unhatted weight-2 doublet 2 and triplet 3'
(used as sanity benchmark; reproduced exactly by E2 last evening).

**Eq. (3.14)** [NPP20 page 9]: hatted multiplets at weight k=3:
- Y_1̂'^(3)(τ)  = √3 (ε θ⁵ − ε⁵ θ)
- Y_3̂^(3)(τ)  = ( ε⁵ θ + ε θ⁵ ;  (5 ε² θ⁴ − ε⁶) / (2 √2) ;  (θ⁶ − 5 ε⁴ θ²) / (2 √2) )ᵀ
- Y_3̂'^(3)(τ) = (1/2) ( −4 √2 ε³ θ³ ;  θ⁶ + 3 ε⁴ θ² ;  −3 ε² θ⁴ − ε⁶ )ᵀ

**App. D, page 36** [NPP20]: hatted doublet 2̂ first appears at k=5:
- Y_2̂^(5)(τ) = ( (3/2)(ε³ θ⁷ − ε⁷ θ³) ;  (√3/4)(ε θ⁹ − ε⁹ θ) )ᵀ

**Note** [NPP20 page 9, end of §3.4]:
> "odd(even)-weighted modular forms always furnish (un)hatted representations,
> since in our notation hatted representations are exactly the ones for which ρ(R) = −1."

This tells us that the doublet 2̂ cannot exist at weight k=3 (only 1̂', 3̂, 3̂' do).
**The smallest odd weight where 2̂ appears is k=5**, as confirmed by NPP20 App. D.

## Hecke operator formula

Standard Hecke operator T(p) on Γ(N)-modular forms, gcd(p, N) = 1, weight k, in
q_N-coefficient form (Diamond-Shurman §5.5):
$$ (T_p f)(m) = a_f(p\,m) + p^{k-1}\,a_f(m / p) $$
with the convention a(m/p) = 0 unless p | m.

This formula was used and validated by E2 yesterday on the unhatted weight-2 doublet
2 (NPP20 eq. 3.12), which closed cleanly with λ(p) = 1 + p for p ∈ {3, 5, 7, 11, 13}.

## Anti-hallucination flags

- All q_4-coefficients are computed FROM FIRST PRINCIPLES from the NPP20 eq. (3.3)
  definition of θ, ε using `sympy.Rational` and `fractions.Fraction`. No coefficient
  was copied from the paper or any other source.
- The candidate formula λ(p) = χ_4(p) + p^(k-1) is treated as a HYPOTHESIS to be
  TESTED, exactly as the morning B3 prediction λ(p) = χ_4(p) + p was treated by
  E2 (and refuted for the unhatted case).
- The "metaplectic T(p²)" alternative was added as a fall-back to test whether
  the standard Hecke operator was the wrong tool; it produced even less closure
  than T(p), so the analysis ruled it out as a uniformly correct alternative.
