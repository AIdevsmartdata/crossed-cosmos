---
name: R3 Geometric Langlands — live-verified arXiv refs
description: Gaitsgory et al. 2024-2025 GLC series I-V + Braverman-Gaitsgory geometric Eisenstein + Xinwen Zhu arithmetic interface
type: project
---

# Live-verified Gaitsgory et al. proof of GLC (5 papers)

All five papers verified via WebFetch against arXiv 2026-05-06.

| # | arXiv | Title | Authors | Verified |
|---|-------|-------|---------|----------|
| **I** | 2405.03599 | Proof of the GLC I: construction of the functor | Gaitsgory, Raskin | ✅ direct fetch |
| **II** | 2405.03648 | Proof of the GLC II: Kac-Moody localization and the FLE | Arinkin, Beraldo, Campbell, Chen, Faergeman, Gaitsgory, Lin, Raskin, Rozenblyum | ✅ direct fetch |
| **III** | 2409.07051 | Proof of the GLC III: compatibility with parabolic induction | Campbell, Chen, Faergeman, Gaitsgory, Lin, Raskin, Rozenblyum | ✅ direct fetch |
| **IV** | 2409.08670 | Proof of the GLC IV: ambidexterity | Arinkin, Beraldo, Chen, Faergeman, Gaitsgory, Lin, Raskin, Rozenblyum | ✅ direct fetch |
| **V** | 2409.09856 | Proof of the GLC V: the multiplicity one theorem | Gaitsgory, Raskin | ✅ direct fetch |

## What each paper does (relevant to ECI angles)

- **I (2405.03599)**: constructs the functor L_G : D-mod(Bun_G)^{ren} → IndCoh_{Nilp}(LocSys_{G^∨}) in characteristic 0 (de Rham + Betti). Establishes equivalence among de Rham/Betti/restricted/non-restricted variants. Setup paper.

- **II (2405.03648)**: Fundamental Local Equivalence (FLE) at critical level + Kac-Moody localization. Local-to-global ingredient.

- **III (2409.07051)**: Compatibility with parabolic induction = constant-term + Eisenstein. Shows L_G induces equivalence on Eisenstein-generated sub-categories. **This is the relevant paper for ECI Angle B (Eisenstein).**

- **IV (2409.08670)**: Ambidexterity Theorem — left adjoint = right adjoint of L_G on cuspidal category. Technical bridge to V.

- **V (2409.09856)**: Multiplicity-one — for an irreducible local system σ on X, the Hecke eigensheaf with parameter σ is unique up to a vector space twist. **CONCLUDES the proof of GLC.**

## Important caveat for ECI

**GLC is over a smooth projective curve X over a field of characteristic 0** (typically X complex, function field K(X) = C(X)). The "automorphic side" is D-modules on Bun_G(X), i.e., the function-field version. For ECI's f = 4.5.b.a (over Q) we are in **arithmetic Langlands**, not geometric per se.

The bridge is via Xinwen Zhu **arXiv:2504.07502** ("Arithmetic and Geometric Langlands Program", 2025): how geometric Langlands inspires new perspectives on classical arithmetic Langlands. ✅ verified abstract via WebFetch — connects categorical methods to arithmetic results.

## Geometric Eisenstein series — Braverman-Gaitsgory

- **arXiv:math/9912097** — "Geometric Eisenstein series" (Braverman-Gaitsgory 1999/2000). ✅ verified via WebFetch.
- Develops Eisenstein in geometric Langlands via relative compactification of moduli of parabolic bundles.
- General reductive G; positive-characteristic global fields; **does NOT specifically cover GL_2 over Q at level 4**.

## Note on original brief arXiv IDs

The original brief listed `arXiv:2405.03600/01/02/03` — these are NOT Gaitsgory papers (verified directly: terahertz metasurfaces, brain rhythm models, etc.). The actual sequence is **2405.03599 (I), 2405.03648 (II), 2409.07051 (III), 2409.08670 (IV), 2409.09856 (V)**. Brief was off by ~50 in the ID and the III-V batch is from Sep 2024 (not contiguous May 2024 IDs).

This is a documentation correction; no hallu attribution to ECI project.

## Other refs touched

- **arXiv:math/9801109** — Lysenko 1998 "Preuve d'une conjecture de Frenkel-Gaitsgory-Kazhdan-Vilonen" (verified search hit, not WebFetched).
- **arXiv:math/0207078** — Laumon 2001/2002 Bourbaki seminar exposé on Frenkel-Gaitsgory-Vilonen (verified search hit).
- Frenkel-Gaitsgory-Vilonen "On the geometric Langlands conjecture" J. Amer. Math. Soc. 15 (2002) 367-417 (cited as the FGV foundational paper, not directly fetched in this session).

## Honest scope

Not fetched directly this session: Beilinson-Drinfeld "Quantization of Hitchin's integrable system and Hecke eigensheaves" (cited via search results), 2010.01906 Arinkin-Gaitsgory restricted-variation paper, 2102.13459 Fargues-Scholze geometrization. These are background not load-bearing on the verdict.

**Hallu count**: 87 → 87 (held; original brief ID-miss is a brief-author typo not a hallu, ECI memory unchanged).
