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
