---
name: M41 Sonnet papers submission finalization
description: 8-paper arXiv submission packages prepared. P5/P6 ready as first batch. P7 needs PRD revision (affiliation Hostinger→Tarbes APPLIED + ECI v7.4 collab co-author awaiting Kevin OK). Endorser plan + cover letters + packaging audit complete. Hallu 85→85
type: project
---

# M41 — Submission package finalization (Phase 4 prep, Sonnet)

**Date:** 2026-05-06
**Owner:** Sub-agent M41 (Sonnet, ~10min, $10-15)
**Hallu count:** 85 → 85 (held; 0 fabrications)

## Files

- `/root/crossed-cosmos/submission/M41_FINALIZE/`
  - `cover_letters.txt` — 8 cover letters (~200-280 words each)
  - `arxiv_strategy.txt` — endorser plan + outreach emails + sequence
  - `packaging_audit.txt` — per-paper [OK]/[FIX]/[WARN] checklist
- `/root/crossed-cosmos/submission/arxiv_submit/<paper_id>/` × 8 dirs
  - `arxiv_metadata.txt` + `submit.sh` per paper

## Per-paper status

| # | Paper | Ready? | Blocker |
|---|---|---|---|
| **P5** | Leptogenesis CSD(1+√6) hep-ph | **YES NOW** | none |
| **P6** | Cassini-Palatini gr-qc | **YES NOW** | 1-line ξ_χ note (trivial) |
| P1 | P-NT BLMS | minor fix | Cohen-Oesterlé dim formula 3 lines + remove A72 from abstract |
| P4 | Cardy LMP | minor fix | Theorem 2 Virasoro 2-para + polariton verify |
| P2 | ER=EPR LMP | minor fix | Prop 1 spectral-measure paragraph |
| P3 | Modular Shadow v2.5 | recompile + fix | Compile v2.5 PDF + App A.2 Mellin saddle |
| P7 | Proton-decay PRD | **MANDATORY REV** | ✅ affiliation Hostinger→Tarbes APPLIED 2026-05-06; ⏸ "ECI v7.4 collaboration" 2nd author (decision pending Kevin); ⏸ §6 honest disclosure of [0.98, 5.54] window already in abstract per M33 |
| P8 | Math.NT paper-2 | future Q3 2026 | 11 [TBD:prove] from M32; skeleton only |

## Endorser priorities (top picks)

| Cat | Endorser | Papers |
|---|---|---|
| math.NT | Tim Browning (IST Austria) | P1, P8 |
| hep-th | Nima Lashkari (Purdue) | P2, P3 |
| cond-mat | Pasquale Calabrese (SISSA) | P4 |
| hep-ph | Steve King (Southampton) | P5, P7 |
| gr-qc | Thomas Sotiriou (Nottingham) | P6 |

Outreach email drafts (~150 words each) for 7 active papers in `arxiv_strategy.txt`.

## Recommended first submission batch (low risk)

**P5 (leptogenesis hep-ph) + P6 (Cassini-Palatini gr-qc)** in parallel:
- Both PDFs present, both ready
- No endorser overlap (King vs Sotiriou) → independent paths
- P5: 3pp, hep-ph/2 (CSD(1+√6) leptogenesis structural fingerprint)
- P6: 3pp, gr-qc (real-data H_0 = 68.51 posterior + KSTD eqs)

## Global pre-submission gate

Re-verify 10 future-dated arXiv IDs flagged by M33 in single `curl` pass:
- 2602.02675, 2603.01664, 2604.02075, 2604.11277, 2604.01275
- 2604.16226, 2604.01422, 2604.13854, 2604.08449, 2603.18502
- Per-paper `submit.sh` gates with runtime warnings

## Discipline
- 0 new fabrications
- Mistral STRICT-BAN observed
- NO drift to settings.json (4th anti-stall iteration successful — pattern broken!)
- 200-line per-file Write protocol respected
