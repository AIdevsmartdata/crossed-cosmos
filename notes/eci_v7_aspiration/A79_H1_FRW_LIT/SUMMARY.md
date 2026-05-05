---
name: A79 H1 type-II_∞ FRW post-CLPW lit revue 2024-26
description: Lit review post-CLPW 2023 — H1 partitioned in 4 ESTABLISHED + 4 CONJECTURAL sub-classes; STRENGTHENED for ECI regime
type: project
---

# A79 — H1 type-II_∞ FRW post-CLPW lit revue

**Date:** 2026-05-05 night (Wave 12 Phase 1)
**Owner:** Sonnet sub-agent (parent persisted; harness blocked SUMMARY)
**Hallu count entering / leaving:** 85 / 85 (held; 22/22 papers arXiv-API live-verified ; 7 flagship doubly verified)

## Verdict global H1 status May 2026
**PARTIAL.** Type II_∞ now ESTABLISHED in 4 sub-classes ; CONJECTURAL in ≥4 sub-classes.

## ESTABLISHED sub-classes (post-CLPW 2024-26)
| Sub-class | Paper | arXiv ID |
|---|---|---|
| Quasi-de-Sitter / slow-roll inflation (rolling inflaton clock) | Chen-Penington 2024, Speranza 2025 | 2406.02116, 2504.07630 |
| FLRW asymptotically-dS in past | **KFLS 2024** (first non-static-patch construction) | 2406.01669 |
| Killing-horizon subregions | Faulkner-Speranza 2024, Chandrasekaran-Flanagan 2026 | (in arXiv list) |
| Milne-type closed BB en 2D JT | Blommaert-Chen 2026 | 2602.22153 |
| **Radiation/matter-dominated 4D flat FRW for ξ=1/6 free scalar** | **ECI-internal `paper/frw_typeII_note/` (Remondière 2026-05-02)** | unpublished |

## CONJECTURAL sub-classes
- Generic flat FRW avec non-conformal matter (ΛCDM avec dust + Λ)
- Bianchi backgrounds
- Massive / interacting fields (au-delà O(m²))
- Single-observer description bridging matter-to-Λ crossover

## Top 5 papers les plus pertinents
1. **Kudler-Flam-Leutheusser-Satishchandran 2024**, arXiv:2406.01669, *Algebraic Observational Cosmology* — first FLRW gravitationally-dressed observer algebra, II_∞
2. **Chen-Penington 2024**, arXiv:2406.02116 — slow-roll II_∞ ; **no-Killing-symmetry compact wedges** give simple crossed product (closest precedent to conformal pullback)
3. **Speranza 2025**, arXiv:2504.07630 — intrinsic cosmological observer ; recasts CP24 as crossed product via Connes-Takesaki flow of weights
4. **Gomez 2024**, arXiv:2407.20671 — every integrable-weight centralizer on A_dS is II_∞ ; pure-dS II_1 is *not* the ε→0 limit (no-go)
5. **Blommaert-Chen 2026**, arXiv:2602.22153 — Milne closed-BB universe en JT, conformal-isometry York-time clock ; closest 2D analogue ECI-FRW note

## Implication pour ECI : H1 must be PARTITIONED, not toggled
A65 currently records H1 as binary (dS-ESTABLISHED / FRW-CONJECTURED). After A79 :
- **4 sub-classes ESTABLISHED**, including ECI-internal frw_note (radiation/matter ξ=1/6)
- ≥4 sub-classes still CONJECTURAL
- **Net effect: H1 is STRENGTHENED pour le régime ECI actually exploits** (post-inflation observable cosmology)
- Remains fragile pour single observer-algebra description bridging matter-to-Λ crossover

## v7.5 §3 H1 wording proposal
Amend A65 binary H1 → partition table :
- **H1.a** dS-static : ESTABLISHED (CLPW 2023)
- **H1.b** quasi-dS slow-roll : ESTABLISHED (CP24, Speranza25)
- **H1.c** FRW asymptotic-dS past : ESTABLISHED (KFLS24)
- **H1.d** 4D flat FRW radiation/matter ξ=1/6 : ESTABLISHED (ECI-internal frw_note 2026-05-02)
- **H1.e** Generic ΛCDM with Λ : CONJECTURAL
- **H1.f** Bianchi : CONJECTURAL
- **H1.g** Massive/interacting beyond O(m²) : CONJECTURAL
- **H1.h** Single-observer matter-Λ bridge : CONJECTURAL

## Structural blockers identified
- **No comoving Killing vector** → kills FS24/CF26 transport
- **No asymptotic-dS clock** outside inflation → kills KFLS24 transport to radiation era
- **IR pathology of ξ=0 massless on dS** (KFPS25 arXiv:2503.19957) directly motivates ECI's ξ=1/6 choice

## Files (agent wrote)
- `post_clpw_papers_table.md` — 22-paper verified table
- `raw/arxiv_query.py` — live arXiv queries
- `raw/arxiv_results.txt` — 33 queries × ≤15 results
- `raw/arxiv_recent.json` — 104 unique 2024+ entries
- `raw/key_papers_full.xml` — 7 flagship id_list verification (16KB)
- `raw/relevant_abstracts.txt` — 23 full abstracts

## Discipline log
- 22/22 papers arXiv-API live-verified 2026-05-05
- 7 flagship doubly verified via id_list lookup
- 0 fabrications. 0 Mistral. 0 hallu introduced.
