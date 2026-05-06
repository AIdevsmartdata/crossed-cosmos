---
name: M44 PISTES META — NEW interfaces + falsifiers + scope theorem-sketch
description: S1 DKSW23 Brumer-Stark p=2 VIABLE-FOOTNOTE (other 4 dead/defer); S2 7 falsifiers with explicit CPU-hr costs; S3 Meta-conjecture M44.1 ECI scope = (CM Q(d=1,3), N=p² ramified, k odd, Hecke Grössencharacter). Hallu 86→86
type: project
---

# M44 — PISTES META survey (Phase 3.G #3, Opus, ~6min)

**Date:** 2026-05-06
**Owner:** Sub-agent M44 (Opus 4.7, max-effort, ~6min)
**Hallu count:** 86 → 86 (held; 4 new arXiv WebFetch-verified)

## S1 — NEW interfaces beyond Phase 3.F

| # | Candidate | Verdict | Surviving content |
|---|---|---|---|
| 1 | Hilbert 12 / Kronecker Jugendtraum imag-quad | DEAD-END | Q(i) class field classical (Weber-Hasse-Deuring c.1900) |
| 2 | **Stark / Brumer-Stark (DKSW23, p=2 closure)** | **VIABLE-FOOTNOTE** | 50-word footnote in M13.1 paper-2 §6 |
| 3 | Langlands functoriality (CM lifts) | DEAD-END | Hecke 1936 + JL classical |
| 4 | Inverse Galois (S'_4 over Q) | DEAD-END | Klüners-Malle DBs cover S_4 / binary octahedral |
| 5 | Vojta heights (CM points) | DEFER | Categorical mismatch, no functor, no contradiction |

### S1 KEY DISCOVERY

**DKSW23** (arXiv:2310.16399, Dasgupta-Kakde-Silliman-Wang 2023) closes Brumer-Stark **over Z** at p=2 using Ribet's method + group-ring valued Hilbert modular forms with non-trivial nebentypus.

**DK20** (arXiv:2010.00657, *Inventiones* 2023) had proved away-from-p=2 only.

ECI's f=4.5.b.a sit at **p=2 ramified** — exact regime where DKSW23 invented new techniques. Suggested 50-word footnote for M13.1 paper-2 §6:

> *"The 2-adic distribution L_2^±(f) conjectured in M13.1, if constructed, would meet the Brumer-Stark-over-Z framework of Dasgupta-Kakde-Silliman-Wang (2023, arXiv:2310.16399) on the CM-character side via automorphic induction ψ → f. Whether the F1 renormalisation v_2 = {-3,-2,0,+1} admits an interpretation in their group-ring-valued Hilbert Eisenstein degeneracy at p=2 ramified is open."* [TBD: prove]

## S2 — 7 falsifier protocols (explicit CPU-hr costs)

| # | Conjecture | Cost | Falsifying outcome |
|---|---|---|---|
| **F2** | M13.1(c) F1 monotone v_2 (cheapest!) | **5 CPU-hr** | Monotone v_2 in non-Steinberg ⇒ F1 not Steinberg-specific |
| **F5** | M28 anticyclotomic IMC paragraph | **20 CPU-hr** | Hsieh 2014 hypothesis check fails for Q(i)/p=2 ramified |
| F1 | M13.1(a) FE-symmetric interp | 50 CPU-hr | Discrepancy v_2 ≥ 0 ⇒ symmetrisation wrong |
| F6 | M22 F1 v_2 ladder pattern | 100 CPU-hr | Non-(K=Q(i),N=p²,k odd) hit ⇒ M44.1 weakens |
| F3 | M13.1(d) θ-critical Bellaïche-Stevens | 200 CPU-hr | Off θ-critical ⇒ M13.1(d) wrong |
| F4 | M27.1 KLZ Beilinson regulator | 1000 CPU-hr | v_2(reg) ≠ {-3,-2,0,+1} ⇒ M27.1 wrong |
| F7 | H8' Cassini-wall ξ_χ (KSTD26) | observational free | BepiColombo Δγ outside wall ⇒ H8' false |

**Cheapest decisive: F2 + F5 within 25 CPU-hr ≈ 1 week local.**

## S3 — Meta-conjecture M44.1 (ECI scope theorem-sketch)

> *ECI's mathematical tools — CM Damerell ladder + F1-renormalised v_2 monotonicity + Modular Shadow type-II_∞ + anticyclotomic-IMC corollary + Beilinson companion M27.1 — form a tight package APPLICABLE PRECISELY when ALL of:*
>
> *(a) the relevant motive is M(f) for f a CM newform over an imaginary quadratic field K with class number 1 (K ∈ {Q(√-d) : d ∈ {1,2,3,7,11,19,43,67,163}}), realistically d ∈ {1,3};*
> *(b) the level N is a perfect prime square N = p² with p ramified in K (Q(i): p=2; Q(ω): p=3);*
> *(c) the weight k is ODD with k ≥ 3 (Steinberg-edge a_{p²} = ±p^((k-1)/2));*
> *(d) the Hodge infinity-type (k-1, 0) is realised by a Hecke Grössencharacter ψ on K with conductor EXACTLY N.*

**Outside this regime — explicit failures**: different K (Q(√-2): F1 motivation gone), non-square N (M22 v_2 undefined), even k (Damerell parity Shimura 1976), real quadratic K (DPV21 RM cocycle distinct), non-CM newforms (no Grössencharacter, framework empty).

**Falsifier of M44.1**: find any newform NOT satisfying (a)-(d) with F1-monotone v_2 ladder + p-adic L matching M13.1.

**Honesty bar**: M44.1 is a SCOPE claim, NOT a Clay claim. ECI's tight specificity = predictive power AND hard ceiling.

## Recommendations

1. **ADD** 50-word DKSW23 footnote to M13.1 paper-2 §6
2. **ADD** Meta-conjecture M44.1 as honest "scope statement" to v7.6 §10
3. **PERSIST** 7 falsifier protocols (separate falsifiers.md)
4. **DO NOT** approach DK/DKSW directly without paper-2 in hand
5. **DO NOT** inflate M44.1 to "uniqueness theorem"
6. **DO NOT** pursue Hilbert 12 / inverse-Galois / Langlands / Vojta sections

## Live-verified refs (4 new + 12 reused)

NEW (WebFetch 2026-05-06):
1. arXiv:2103.02490 — Darmon-Pozzi-Vonk 2021 RM cocycle (real-quad case)
2. arXiv:2010.00657 — Dasgupta-Kakde 2020 BS away-from-p=2
3. **arXiv:2310.16399** — DKSW 2023 BS-over-Z (closes p=2)
4. arXiv:2412.01803 — Charlton-Medvedovsky-Moree 2024 (S_3/S_4 background)

Reused: M27/M28/M37/M39/M40 set (KLZ2017, Kriz2021, etc.)

## [TBD: prove] markers (3 honest)
1. **TBD-M44-1**: F1 (1+p^{m-3}) ↔ DKSW23 group-ring Hilbert Eisenstein at p=2 ramified
2. **TBD-M44-2**: Hsieh 2014 anticycl-IMC admits Q(i)/p=2 ramified (book check)
3. **TBD-M44-3**: M44.1 (a)-(d) is SUFFICIENT (not just necessary)

## Discipline
- 0 fabrications
- Mistral STRICT-BAN observed
- 4 NEW arXiv WebFetch-verified (random-ID misses honestly reported)
- NO drift to settings.json (anti-stall ✅)
- Sub-agent return-as-text protocol used (parent saved)
