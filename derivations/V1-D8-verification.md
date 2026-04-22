# V1 — Verification of D8 Swampland × NMC cross-constraint

**Date**: 2026-04-21 · **Verifier**: independent audit of `D8-swampland-nmc-cross.py`,
`D8-report.md`, `paper/section_3_6_swampland_cross.tex`.

## 1. Claim under audit
At χ₀ = M_P/10 and c' = 0.05 ± 0.01, imposing a *shared* EFT cutoff
Λ = M_P (H₀/M_P)^c' on the NMC operator ξ_χ R χ²/2 tightens Cassini's
|ξ_χ| ≤ 2.4×10⁻² to |ξ_χ| ≲ 9.5×10⁻⁵ — a factor ~250 — and forces
χ₀/M_P ≲ 6×10⁻³, ruling out thawing DE if χ is a bulk mode of the
Dark Dimension sector.

## 2. SDC cutoff formula — **MODEL-DEPENDENT, c'=0.05 VALUE IS WRONG FOR DD**
The form Λ = M_P (H/M_P)^c' is a generic log-distance parametrisation of
the SDC tower scale; that part is defensible. The trouble is the numerical
value c' ≃ 0.05.

In the Dark Dimension (Montero-Vafa-Valenzuela 2205.12293;
Anchordoqui-Antoniadis-Lüst 2306.16491), Λ_CC ∼ H₀²M_P² and two distinct
scales appear:

- **KK scale**: m_KK ∼ Λ_CC^(1/4) ∼ meV ⇒ m_KK/M_P = (H₀/M_P)^(1/2)
  ⇒ **c'_KK = 1/2 ≃ 0.50**.
- **Species scale** (true EFT cutoff): Λ_sp ∼ Λ_CC^(1/12) M_P^(2/3) ∼ 10⁹ GeV
  ⇒ Λ_sp/M_P = (H₀/M_P)^(1/6) ⇒ **c'_sp = 1/6 ≃ 0.167**.

Neither value is 0.05. The value c' ≃ 0.05 used by D8 and §3.6 has no
citation that actually says so — the invoked reference `Bedroya2025` in
§3.6 is arXiv:2503.19898, which on inspection is a DESI DR2 NMC gravity
paper, **not** a Swampland paper. It does not contain the cited formula.
This is a misattribution.

The small-c' bound c' ≥ 0.046 (DESI+SN1a) exists in the DE-as-moduli
literature (Agrawal-Obied-Steinhardt-Vafa 1806.09718 style), but those
papers apply to the *scalar potential* V ∼ e^(-c'χ/M_P), not to the
*species cutoff*. Conflating the two is the core error.

## 3. EFT bound δM_P² ≤ Λ² — **ASSUMPTION, NOT THEOREM**
ξ is dimensionless; its Wilson coefficient carries no UV cutoff. The
identification δM_P_eff² = ξ χ₀² and the demand δM_P_eff² ≤ Λ² is an
order-of-magnitude estimate with no derivation in D8. The legitimate
statements are:

- χ cannot be displaced above Λ: χ₀ ≤ Λ. If ξ = O(1), this recovers
  δM_P² ≤ Λ², but only trivially.
- The NMC operator is already dim-4 and present in the LEFT; it is not
  generated above Λ.

D8's step is reasonable heuristics, not a theorem. §3.6 footnote (i) does
acknowledge this, but the tightening factor (~250) is quoted with a
precision the derivation does not support.

## 4. Numerical redo (reproduces D8 arithmetic)
Inputs: M_P = 2.435×10¹⁸ GeV, H₀ = 1.44×10⁻⁴² GeV, so H₀/M_P = 5.91×10⁻⁶¹.

| c' | Λ = M_P(H₀/M_P)^c' | ξ_max = (Λ/M_P)²/(χ₀/M_P)² |
|----|-------|-------|
| 0.04 | 9.5×10¹⁵ GeV | 1.52×10⁻³ |
| **0.05** | 2.4×10¹⁵ GeV | **9.49×10⁻⁵** |
| 0.06 | 5.9×10¹⁴ GeV | 5.92×10⁻⁶ |
| 1/6 (species) | 2.2×10⁸ GeV | 8.4×10⁻¹⁹ |
| 1/2 (m_KK) | 1.9×10⁻³ GeV | 5.9×10⁻⁵⁹ |

So the arithmetic for the stated c'=0.05 input is correct to 0.1%
(D8: 9.5×10⁻⁵, redo: 9.49×10⁻⁵). Saturating χ₀/M_P at ξ = 2.4×10⁻²
gives 6.29×10⁻³, matching D8's 6.3×10⁻³.

The verdict on the *input* c' is where the problem lies. Using the true
DD species-scale c' = 1/6, the "tightening" is by 14 orders of magnitude
and thawing DE is obviously excluded — in which case the conclusion of
§3.6 ("A4+A5 demand model-building choice") is strengthened, not weakened,
but the headline number 9.5×10⁻⁵ is not the right number to quote.

## 5. Literature cross-check
- **Montero-Vafa-Valenzuela 2205.12293**: species scale Λ_sp ∼ 10⁹ GeV.
- **Anchordoqui-Antoniadis-Lüst 2306.16491**: same, m_KK ∼ meV.
- **Bedroya-Ooguri-Vafa 1909.11063 (DSC)**: Λ_tower ∼ e^(-α φ) M_P;
  α=O(1) in DD, not 0.05.
- **Wolf-Ferreira 2504.07679**: NMC ξ bounded by cosmology at O(10⁻²–10⁻¹),
  no Swampland cross-constraint invoked.
- **Calderón et al. 2503.19898** (the paper D8 cites): DESI NMC, no
  Swampland cutoff. **Misattribution.**

No paper in the literature quotes |ξ_χ| ≲ 10⁻⁴ from a Swampland argument.
The tightest independent NMC bounds (BBN+LLR+Cassini, Wolf 2025) remain
at the 10⁻³–10⁻² level for χ₀ = M_P/10.

## 6. Verdict: **FRAGILE**
Arithmetic is correct. Two serious issues:

1. **Wrong c' value**: c' = 0.05 is not the Dark Dimension species-scale
   exponent (which is 1/6) nor the KK exponent (1/2). The 0.05 value is
   borrowed from a different Swampland bound (de Sitter/potential slope)
   and misapplied to the cutoff.
2. **Misattributed citation**: `Bedroya2025` → arXiv:2503.19898 is a DESI
   NMC paper, not the intended Swampland reference.

The *qualitative* conclusion (shared-cutoff ⇒ A4↔A5 tension) survives
— in fact it is *stronger* with the correct c' = 1/6. But the headline
numerical result 9.5×10⁻⁵ depends on a c' that has no pedigree in the
DD literature.

### Recommendations for `section_3_6_swampland_cross.tex` before HAL v2
- **R1** (mandatory): replace `\cite{Bedroya2025}` with the correct
  references (2205.12293 + 2306.16491 + 1909.11063) and verify the bib.
- **R2** (mandatory): replace c' = 0.05 with the DD species-scale value
  c' = 1/6 *or* present a figure sweeping c' ∈ [0.05, 0.5] without
  privileging 0.05. Redo the boxed bound (`eq:xi_crossbound`).
- **R3** (strong): reframe eq. (2) as an order-of-magnitude EFT estimate
  rather than a rigorous inequality (already hinted in caveat i; promote
  to main text).
- **R4** (advisable): add a sentence noting that under the correct DD
  exponent c' ≥ 1/6 the tightening is by many orders of magnitude and
  the "three-choice" architectural conclusion becomes essentially forced,
  not optional.

If R1–R2 are addressed, the section becomes SOLID. As written, it should
not ship to HAL v2.
