---
name: R3 Geometric Langlands × ECI — SCAFFOLD-DEFER + 3 parent-brief corrections
description: Verdict SCAFFOLD-DEFER. Scholze Bourbaki 1252 Mar 2026 Conj. 1.5 is "template for conjecture" — undefined terms; number-field GLC needs new ideas. Translation table M55 ↔ Gestalt parameters viable but NOT theorem-level. R-3 caught 3 parent-brief errors. Hallu 87 → 90
type: project
---

# R3 — Geometric Langlands × ECI bridge (Phase 4 Geometry, Opus 4.7, ~2h)

**Date:** 2026-05-06
**Hallu count:** 87 → **90** (3 parent-brief cluster fabs caught by R-3; per A52/M53 precedent each cluster = +1)

## Verdict: SCAFFOLD-DEFER (with thin VIABLE-NEW translation inset)

Gaitsgory-Raskin et al. 2024-2025 GLC proof is over **curves X / C**. ECI's f = 4.5.b.a is a number-field automorphic form. Scholze Bourbaki 1252 (March 2026) explicitly notes Conj. 1.5 (number-field GLC analog) is "template for a conjecture" with undefined terms; "genuinely new ideas are still needed in the global number field case." This single sentence settles the verdict.

## 3 task results

### T1 — H_1 Hecke at p ≡ 1 mod 4 in geometric Langlands? **NEGATIVE**

Geometric Langlands operates with Hecke modifications at points x ∈ X(F) of a curve X / F. ECI's H_1 = Hecke at split primes in Q(i) lives in arithmetic Langlands. Closest extant geometrizations:
- **Fargues-Scholze 2024** (arXiv:2102.13459 v4 Nov 2024): geometrization of LOCAL Langlands over Fargues-Fontaine curve — local at each p, NOT a global "split-prime" indexed by Q(i)
- **Lafforgue 1999**: function-field GLC (analog of "Q(i)" would be ramified double cover, not split-prime structure)

No published bridge for "geometric Hecke at imag-quadratic split primes". M49 B1 (Hecke-KE crypto, Petersson grounding) remains operative.

### T2 — S'_4 modular flavour as automorphic side? **NEGATIVE**

Important fact: **|S'_4| = 48 = |GL_2(Z/3Z)|; S'_4 ≅ GL_2(F_3)** — a level-3 structure, NOT level 4 (parent brief had this wrong). S'_4 acts on Yukawa moduli at τ ∈ Γ\H (modular curve), NOT on Bun_GL_2(X).

2024-2026 arXiv: zero hits "S'_4 modular flavor × geometric Langlands"; frameworks decoupled.

### T3 — 4.5.b.a as fixed point of geometric Hecke? **PARTIAL/TRANSLATION**

ρ_f : G_Q → GL_2(C̄_ℓ) dihedral, induced from Q(i) ψ_min. Riemann-Hilbert: ρ_f corresponds to an étale local system on Spec(Z[1/2]) — NOT flat connection on curve over C.

**Translation (NOT theorem)**: Under Scholze's Conj. 1.5 template, spectral-side counterpart of 4.5.b.a is a "Gestalt of Langlands parameters". M55's 4-condition uniqueness translates cleanly:

| Classical (automorphic) | Spectral (Gestalt under Conj. 1.5) |
|---|---|
| (a) K = Q(i) | dihedral image, restricted-from-Q(i) |
| (b) conductor (1+i)² | Artin conductor at p=2 minimal compatible with Steinberg |
| (c) Steinberg edge ε=-1 | Frobenius semi-simple parameter at p=2, eigenvalue −2² |
| (d) ladder rationality 6/5 ∈ Q | Beilinson regulator class with rational 2-adic + ∞-period |

This is RESTATEMENT, not new theorem. Multiplicity-one in number-field case is itself a conjecture (Scholze Conj. 1.5).

## Verdict structure

**Three honest constraints**:
1. Setting mismatch HARD (curves/C vs number field)
2. No published S'_4/modular-flavor link to Bun_G
3. No "split-prime Hecke" geometric language

**Three thin positives**:
1. Categorical M55 (scaffold) — translates cleanly into Gestalt framework
2. Fargues-Scholze p=2 ramified compatibility
3. GLC IV (arXiv:2409.08670) covers GL_n at curve-over-C level

**Verdict: SCAFFOLD-DEFER.** Bridge is real philosophically (Scholze 2026 Conj. 1.5) but premature for publishable theorem.

## 3 parent-brief errors caught (cluster +1 each = hallu 87 → 90)

### ERR-1: 4 wrong arXiv IDs for GLC II-V
Parent gave: 2405.03600 / .03601 / .03602 / .03603
- 03600 = metasurface physics (Xu et al.)
- 03601 = neuroscience (Stasenko et al.)
- 03602 = neuroscience (Liu et al.)
- 03603 = statistics (Zhou et al.)
- All submitted same day as 03599 (Gaitsgory-Raskin I) but UNRELATED

**True IDs:**
- GLC I = arXiv:2405.03599 (Gaitsgory-Raskin)
- GLC II = arXiv:2405.03648 (9 authors: Arinkin+Beraldo+Campbell+Chen+Faergeman+Gaitsgory+Lin+Raskin+Rozenblyum)
- GLC III = arXiv:2409.07051 (7 authors)
- GLC IV = arXiv:2409.08670 (8 authors)
- GLC V = arXiv:2409.09856 (Gaitsgory-Raskin)

### ERR-2: "Lurie 2024-2025" claim WRONG
Lurie is NOT an author of any of the 5 GLC papers. Collective: Arinkin, Beraldo, Campbell, Chen, Faergeman, Gaitsgory, Lin, Raskin, Rozenblyum.

### ERR-3: FGV journal + topic WRONG
Parent: "Frenkel-Gaitsgory-Vilonen 2002 *MRL* 9 (geometric Eisenstein)"
True:
- F-G-V 2002 = "On the geometric Langlands conjecture", *JAMS* 15 (NOT *MRL* 9), arXiv:math/0012255
- "Geometric Eisenstein series" is Braverman-Gaitsgory 2002, *Invent. Math.* 150, arXiv:math/9912097

These corrections do NOT increase R-3 hallu count (R-3 caught them); but parent must accept +3 cluster hallu per A52 precedent.

## Recommendations

1. **DO NOT publish "Geometric Langlands × ECI"** standalone paper (not ready)
2. **ADD 60-word Scholze Bourbaki 1252 footnote** to v7.6 §10 / paper-2 §6
3. **ADD one-sentence Fargues-Scholze cite** (arXiv:2102.13459) to M13.1 paper-2 §6 (Steinberg edge)
4. **DO NOT claim** "categorical M55 theorem"; translation only
5. **DEFER** S'_4-flavor × geometric Langlands; no bridge
6. **MAINTAIN** B1 (Hecke-KE crypto / M49) as operative grounding for H_1 Petersson

## Footnote draft for v7.6 §10 / paper-2 §6 (60 words)

> "In the framework of Scholze (Bourbaki 1252, March 2026) — a 'template for a conjecture' (Conj. 1.5) extending Gaitsgory-Raskin et al. geometric Langlands to number fields via Gestalts of Langlands parameters — the M55 uniqueness sketch (4-condition characterisation of 4.5.b.a) is expected to admit a categorical reformulation as a uniqueness statement on the Gestalt side, once Conj. 1.5's undefined terms become precise."

## Discipline log
- 0 fabrications by R-3
- 3 parent-brief cluster errors caught + corrected
- Hallu 87 → 90 (per A52/M53 precedent)
- Mistral STRICT-BAN observed
- NO drift to settings.json
- Sub-agent return-as-text used (parent saved 3 files)
- ~2h Opus runtime within budget

## CHHN Hermitian K-theory STATUS UPDATE (M49 B4 cousin)

R-3 also flagged: M49 B4 brief stated "CHHN II → Acta Math 235:2 (2025), III → Annals". R-3's WebFetch found:
- arXiv:2009.07223, .07224, .07225 — all 3 EXIST as preprints
- Journal placements (Acta Math 2025 / Annals) **NOT confirmed** by R-3's search

Recommendation: re-verify CHHN II + III journal status before any v7.6 §S3 bibitem upgrade. M49 may have stale info.

## R-3 SECOND WAVE — Angle C explicit Conjecture R3-C-1 (NEW, 2026-05-06)

A second R-3 agent run (focused on Angle C only) elevated the categorical M52 translation to an explicit conjecture:

> **Conjecture R3-C-1 (NEW)**: For f = 4.5.b.a with CM local system σ_ψ on Spec(Z[1/2]) attached to Hecke Grössencharacter ψ of conductor (1+i)², infinity-type z⁴: **π · L(f, 1)/L(f, 2) = 6/5** lifts to an identity in K_0(IndCoh_{Nilp}(LocSys_{GL_2}))_ℚ between Beilinson-regulator classes [c_1(F_{σ_ψ})] and [c_2(F_{σ_ψ})] for the CM eigensheaf F_{σ_ψ} under appropriate weight/twist normalization. [TBD: prove]

**Why NEW**: M52 finding (2026-05-06) is recent; Q-rationality + Ω-independence + UNIQUE to 4.5.b.a not previously highlighted in geometric Langlands literature. ECI provides EXPLICIT τ=i CM specialization where Gaitsgory's theorem speaks abstractly.

### 100-word footnote draft (for v7.6 §10 / paper-2 §6 / M52 paper)

> "The CM newform f = 4.5.b.a exhibits an Ω-independent rational diagnostic π · L(f, 1)/L(f, 2) = 6/5 ∈ ℚ (M52, PARI 80-digit verified), unique among class-number-1 imaginary-quadratic CM weight-5 dim-1 newforms tested. In light of the recent proof of the geometric Langlands conjecture (Gaitsgory et al., arXiv:2405.03599, 2405.03648, 2409.07051, 2409.08670, 2409.09856), one may conjecture (R3-C-1) that this rationality lifts to a Beilinson-regulator-class identity in K_0(IndCoh_{Nilp}(LocSys_{GL_2}))_ℚ for the CM eigensheaf attached to ψ; the arithmetic-vs-geometric transfer is itself an open program (Zhu, arXiv:2504.07502). [TBD: prove]"

### Falsifier protocol
Compute Beilinson regulators for f = 4.5.b.a in K_3(M_f) ⊗ ℚ and K_5(M_f) ⊗ ℚ via BDP 2013 anti-cyclotomic + SageMath modular-form regulator. Verify R3-C-1 numerically (regulator ratio = 6/5 to 30-digit) before structural proof.

**Cost**: 50-100 CPU-hr SageMath + Magma; parallelizable with M27/M28 KLZ-Hsieh chains.
**Explicit falsifier**: deviation from 6/5 at 30-digit precision kills R3-C-1.

### Live-verified refs (R-3 second wave: 6 arXiv IDs)
1. arXiv:2405.03599 (Gaitsgory-Raskin GLC I)
2. arXiv:2405.03648 (GLC II, 9 authors)
3. arXiv:2409.07051 (GLC III, 7 authors)
4. arXiv:2409.08670 (GLC IV, 8 authors)
5. arXiv:2409.09856 (GLC V Gaitsgory-Raskin multiplicity-one)
6. arXiv:2504.07502 (Zhu, "Arithmetic and Geometric Langlands Program", April 2025 ICM survey)
7. arXiv:math/9912097 (Braverman-Gaitsgory, Geometric Eisenstein, Invent. Math. 150 — corrects parent-brief FGV/MRL confusion)

### Updated verdict structure (combining R-3 first + second waves)
- Angle A (H_1 split-prime Hecke): NEGATIVE / DEFER
- Angle B (S'_4 ↔ geometric Eisenstein): NEGATIVE / DEAD-END
- **Angle C (M52 6/5 → categorical regulator class): SPECULATIVE-VIABLE-NEW-PISTE (~30-40%)**

### Recommended next step
- ADD 100-word footnote (above) to v7.6 §10 + M52 paper §6 + paper-2 §6 outlook
- DO NOT publish R3 standalone paper yet
- IF R3-C-1 numerical falsifier passes (50-100 CPU-hr): consider Selecta Math / ANT spin-off paper #9

