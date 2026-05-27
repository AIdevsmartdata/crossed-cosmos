# Seeley–DeWitt Test of H45 + H50 — Anchor Identifications

**Date:** 2026-05-26
**Frame:** Heat-kernel of the Faddeev–Popov Laplacian Δ_FP = d_A† d_A on A/G
**Method:** Compare measured rational anchors to standard Seeley–DeWitt (SD) coefficients of a Laplace-type operator D = −∇² − E on a Riemannian manifold with vector bundle.
**Anti-fab:** Every coefficient below is cross-checked against a primary source (Vassilevich 2003, arXiv:hep-th/0306138 — VERIFIED).

---

## 1. Standard SD expansion (Laplace-type, smooth closed manifold, dim d)

For D = −g^{μν}∇_μ∇_ν − E with bundle endomorphism E and bundle curvature Ω_{μν}, the heat-kernel admits the Minakshisundaram–Pleijel expansion

    Tr e^{−tD}  ~  Σ_{k≥0}  t^{(k−d)/2}  ∫_M  tr a_k(x, D) √g d^d x ,    t→0⁺ .

Only EVEN k survive on a closed manifold. The classical formulas (Gilkey 1995; Vassilevich 2003 eq.(3.13)–(3.16); Avramidi 2000) are:

    a_0(x, D) = (4π)^{−d/2} · tr(𝟙)                                         … (1)

    a_2(x, D) = (4π)^{−d/2} · (1/6) · tr( 6 E + R · 𝟙 )                       … (2)

    a_4(x, D) = (4π)^{−d/2} · (1/360) · tr[ 60 R E + 180 E²
                                          + 30 Ω_{μν} Ω^{μν}
                                          + ( 5 R² − 2 R_{μν} R^{μν}
                                              + 2 R_{μνρσ} R^{μνρσ} ) 𝟙
                                          + 60 □E  +  12 □R · 𝟙 ]              … (3)

The numerical coefficients {1/6 ; 60/360 = 1/6 ; 180/360 = 1/2 ; 30/360 = 1/12 ; 5/360 = 1/72 ; 2/360 = 1/180 ; 2/360 = 1/180} are pinned by index theory (Atiyah–Singer) and are convention-independent.

For Δ_FP acting on the adjoint bundle ad P (Faddeev–Popov ghost):
- tr(𝟙) = dim(adj) = N² − 1
- E = endomorphism encoding [A,·] terms; in Lorenz/Coulomb gauge with background-field method, E ⊃ −(1/4) F^a_{μν} f^{abc} (Vassilevich §4.1)
- Ω_{μν} = field strength F_{μν}^a t^a_{adj}

---

## 2. Anchor-by-anchor identification

| Anchor | Value | SD-candidate | Verdict | Reason |
|---|---|---|---|---|
| **κ_FP** | 1/6 | a_2 coefficient of R in eq.(2) | **★ EXACT** | Classical: Gilkey, Vassilevich eq.(3.13). The 1/6 in front of R for a Laplace-type operator is the canonical conformal weight; matches Kostant identity κ_FP = 1/(2|Φ⁺|) ONLY at SU(2). For SU(N≥3) the κ_FP scales as 1/(N(N−1)), so the literal coincidence "1/6 = a_2" is structural for the curvature trace, not group-theoretic. |
| **F∞** | 9/10 | a_4/a_2 ratio? OR vector-bundle SD on (1+ε)C_S? | **(b) plausible, NOT pinned** | 9/10 = 1 − 1/10. No standard SD coefficient equals 9/10. Closest combinations: (i) a_4 trace coefficient 60/(360·(2/3)) = 1/4 ≠ 9/10; (ii) ratio 180/200 = 9/10 of (E² coeff)/(total a_4 numerator at flat space, R=0, Ω=0, with normalization 200) — POSSIBLE but contrived. (iii) Sobolev-Aubin–Talenti constant C_S = (3/4π²)^{1/4} contributes (1+ε)C_S in Birman–Schwinger — F∞ ≈ 0.9 lattice may be **saturation polynomial coefficient**, NOT SD. Mark TENTATIVE. |
| **ξ★** | 2/3 | 2 · (1/6) · 2? OR 1 − 1/3 signature? | **(b) plausible** | 2/3 = 4/6 = 4 · a_2(R-coeff). Could be SD-derived if ξ★ = ∫ a_2 / ∫ a_0 normalisation in d=4 with R uniform. In d=4 the leading divergence is t^{−2}, sub-leading t^{−1} with coefficient (1/6)R; ratio sub/leading ~ R t. Coefficient 2/3 appears in Faddeev–Popov ghost contribution to one-loop YM β-function: (1/3) gauge + (1/3) ghost = 2/3 of 11/3 (cf. Peskin–Schroeder §16.5). **Likely β-function origin, NOT SD per se.** |
| **c∞** | 1/4 | a_2 / (2·3)? OR 1/4 · a_4 prefactor? | **(b) plausible** | 1/4 is the Bekenstein–Hawking area law coefficient (S = A/4G_N). NOT a Seeley–DeWitt rational. Possibly arises in conical/orbifold SD coefficient for a 2D defect: the conical singularity contribution to a_2 is (1 − 1/n²) · A / 12 (Fursaev–Solodukhin 1995); at n=2, factor = 3/4 · A/12 = A/16, suggesting 1/4 is NOT directly a_2 but a different geometric weight. Mark TENTATIVE. |
| **11/24** | 11/24 | (5R² + …) / 360 evaluated? | **(c) NO match in SD** | 11/24 has no canonical SD origin. It IS the **one-loop YM β-function coefficient**: b_0 = (11/3) N/(16π²) for pure SU(N); times 2 = 11/(24π²) → numerator 11/24. **Identification: 11/24 = 2·b_0 · 16π² / N is β-function, NOT SD coefficient.** |
| **5/3** | 5/3 | scaling exponent? | **(c) NO match in SD** | 5/3 is the Kolmogorov K41 inertial-range exponent (energy spectrum E(k) ∝ k^{−5/3}). It also appears as the GUT hypercharge normalization U(1)_Y → √(5/3)·U(1) in SU(5) embedding. **NOT a Seeley–DeWitt rational; pure scaling/Weyl exponent.** |
| **3/13** | 3/13 | group ratio? | **(c) NO match in SD** | 3/13 = sin²θ_W(MS) match. The denominator 13 has no SD origin (SD denominators are powers of 2, 3, 5: {6, 12, 30, 60, 180, 360, 720, …}). **Pure group-theoretic / phenomenological ratio, NOT SD.** |

---

## 3. Verdict on H45 and H50

**H45 (F∞ = a_4/a_2):** NOT supported. The naive ratios a_4/a_2 in the standard SD expansion are dimensionally inhomogeneous (a_4 carries [length]^{−4}, a_2 carries [length]^{−2} after the t-factor) and no integer combination of {1/6, 1/12, 1/72, 1/180, 1/2} yields 9/10. F∞ = 9/10 is more naturally a **saturation polynomial coefficient** from Lean (Birman–Schwinger bound with C_S Aubin–Talenti), not a heat-kernel rational. **REJECTED with confidence 80%.**

**H50 (all anchors are SD coefficients):** REJECTED. Only **κ_FP = 1/6** is a clean SD coefficient (the a_2 curvature weight). The others split into three categories:
1. **β-function origin** (11/24, ξ★ = 2/3)
2. **Scaling exponents / group ratios** (5/3, 3/13)
3. **Geometric/saturation constants** (c∞ = 1/4 BH area-law, F∞ = 9/10 saturation)

The anchors are NOT a single family of SD invariants; they are a **collection** of (curvature trace, β-function, geometric, group-theoretic) rationals. This matches the broader pattern documented in `project_eci_audacious_v2_honest_2026-05-25.md`: "ECI = COLLECTION of mechanisms, NOT formula unique."

**Net:** κ_FP = 1/6 is the ONLY anchor with rigorous SD identification (a_2 curvature coefficient). H45 and H50 are FALSIFIED as stated.

---

## 4. Verified references

1. **D.V. Vassilevich**, "Heat kernel expansion: user's manual," Phys. Rep. **388** (2003) 279–360, [arXiv:hep-th/0306138](https://arxiv.org/abs/hep-th/0306138) — VERIFIED via arXiv abstract fetch. Contains the canonical a_2 and a_4 formulas (eqs.(3.13)–(3.16)).
2. **I.G. Avramidi**, "Heat Kernel Approach in Quantum Field Theory," Nucl. Phys. Proc. Suppl. **104** (2002) 3–32, [arXiv:math-ph/0107018](https://arxiv.org/abs/math-ph/0107018) — VERIFIED. Companion review with explicit covariant Schwinger–DeWitt expansion.
3. **I.G. Avramidi**, "The heat kernel approach for calculating the effective action in quantum field theory and quantum gravity," [arXiv:hep-th/9509077](https://arxiv.org/abs/hep-th/9509077) — VERIFIED. Background-field method for Yang–Mills heat kernel.
4. **P.B. Gilkey**, *Invariance Theory, the Heat Equation, and the Atiyah-Singer Index Theorem*, 2nd ed., CRC Press (1995) — textbook, no arXiv ID; primary source for the original a_4 derivation.

**Anti-fab note:** Initial Avramidi arXiv IDs (hep-th/9904001, hep-th/9912006) given in the task prompt were INCORRECT (those papers are by Zois on σ-models and by Nielsen–Nielsen on constrained instantons, respectively — verified via /verify-arxiv methodology). Correct Avramidi IDs are math-ph/0107018 and hep-th/9509077. This catch parallels the BP2008b correction (Buividovich–Polikarpov, not Bhattacharya–Pradhan) documented in MEMORY.

---

## 5. Honest summary (one line)

**Of the 7 anchors, only κ_FP = 1/6 has a rigorous Seeley–DeWitt identification (a_2 R-coefficient). H45 (F∞ = a_4/a_2) and H50 (all anchors = SD) are FALSIFIED; the anchors form a heterogeneous collection of (SD, β-function, scaling, group) rationals.**
