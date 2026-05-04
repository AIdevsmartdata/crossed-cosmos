# H2 Gate Summary

ECI v7-R&D | 2026-05-04

## Anti-Hallucination Alert (Critical)

The task prompt's formulas for `Y_2̂'^(5)` and `Y_4̂^(5)` are **fabricated**. After
fetching the NPP20 PDF (arXiv:2006.03058) and extracting Appendix D via pdftotext:
S'_4 (order 48) has irreps of dimensions 1,1,1,1,2,2,3,3,3,3 only (sum of sq. = 48).
There is no 4̂ and no 2̂'. The full weight-5 hatted sector is 2̂⊕3̂⊕3̂⊕3̂' (11 components).

## Substituted Multiplets Tested

Actual NPP20 weight-5 hatted forms used in place of the fabricated ones:
- `Y_3̂,2^(5)`: 2nd independent 3̂ triplet at weight 5 (reconstructed from App D pdftotext)
- `Y_3̂'^(5)`: 3̂' triplet via CG construction 2⊗3̂→3̂' (NPP20 Table 10)

## Gate Results

**Sub-algebra closure on H_1 = {T(p): p ≡ 1 mod 4}:**

| Multiplet | Closed? | λ(5) | λ(13) | λ(17) | λ(29) | λ(37) |
| --- | --- | --- | --- | --- | --- | --- |
| 3̂(3) [G1.5] | YES | 26 | 170 | 290 | 842 | 1370 |
| 2̂(5) [G1.5] | YES | 18 | 178 | −126 | −1422 | 530 |
| 3̂,2(5) [new] | YES | −14 | −238 | 322 | 82 | 2162 |
| 3̂'(5) CG | NO | — | — | — | — | — |

Note: G1.5's deliverable B had a bug (used 3̂(3) Eisenstein values 290,842,1370 for 2̂(5) at
p=17,29,37 instead of the correct cuspidal values −126, −1422, 530). Corrected here.

**Commutativity T(5)·T(13) = T(13)·T(5):** All multiplets commute (verified, cap=5).

**Obstruction at p ≡ 3 mod 4:** All four hatted multiplets fail the eigenform test —
confirmed obstructed at p=3, 7, 11. H_1 sub-algebra closure is restricted to p ≡ 1 mod 4.

## Prime-Stability of Ratios

All ratios tested are prime-DEPENDENT (spread >> 1%):

| Ratio | At p = {5, 13, 17, 29, 37} | Stable? |
| --- | --- | --- |
| λ_3̂,2(5)/λ_3̂(3) | −0.54, −1.40, +1.11, +0.10, +1.58 | NO |
| λ_3̂,2(5)/λ_2̂(5) | −0.78, −1.34, −2.56, −0.06, +4.08 | NO |
| λ_2̂(5)/λ_3̂(3) | +0.69, +1.05, −0.43, −1.69, +0.39 | NO |

## Verdict

1. **Sub-algebra H_1 extends to 3̂,2(5)?** YES — closes on all 5 tested primes.
   (The prompt's 2̂' and 4̂ do not exist and cannot be tested.)
2. **Any prime-stable ratio identified?** NO — every cross-weight ratio between
   weight-5 cuspidal forms and the weight-3 Eisenstein triplet is wildly prime-dependent,
   with sign changes across the prime set {5,13,17,29,37}.
3. **Implication for v7 m_c/m_t:** This extends and confirms the G1.5 finding.
   No single-eigenvalue ratio is a structural constant. The prediction λ_2̂(5)/λ_3̂(3) ≈ m_c/m_t
   is prime-dependent even within the closed sub-algebra H_1. A genuine v7 mass-ratio formula
   requires the full Clebsch-Gordan Yukawa matrix — the ratio of two individual Hecke
   eigenvalues is always a fit parameter, not a derivable quantity.
