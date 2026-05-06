---
name: M12 v7.5 strategic patches per O1 D3.4
description: 2 patches APPLIED (P-NT abstract + Cardy footnote, compile clean), 2 SKIPPED (already in place), 2 UNCHANGED, PRD verified
type: project
---

# M12 — v7.5 strategic patches (Phase 3.B)

**Date:** 2026-05-06
**Owner:** Sub-agent M12 (Sonnet) + parent triple-pass compile
**Hallu count entering / leaving:** 85 / 85

## Patches applied (2)

### Patch 1 — P-NT BLMS abstract ✅
File: `notes/eci_v7_aspiration/PNT/paper_lmfdb_s4prime.tex`
Compiled: 11 pages, clean.

3-sentence A72 demotion paragraph at end of abstract:
- K=Q(i) Damerell ladder = math-internal anchor only
- A72 (2026-05-06): Q(i)=358 vs null 366±25, σ=−0.33, P_null=0.63 → indistinguishable from random
- V_us=9/40 and V_cb²=1/600 demoted to speculative (P_null > 30%)
- Hecke H_1 + χ_4 nebentypus + Galois descent **unaffected**

### Patch 4 — Cardy LMP footnote ✅
File: `notes/eci_v7_aspiration/CARDY_PAPER/cardy_rho_paper.tex`
Compiled: 10 pages, clean.

`\begin{remark}` after D-series corollary:
- ρ(c=1) = 1/12 = α_2 survives A72 as math identity
- A72 demotes predictive use of {1/10, 1/12, 1/24, 1/60} on fermion observables but NOT mathematical Cardy ladder

## Patches skipped (already in place from previous waves)

- **Patch 2 v75_amendment.tex §6**: §A72 already at lines 1375-1450, §H1ladder at 1114-1210 with all numbers
- **Patch 3 Modular Shadow**: A77 g≥2 footnote already at lines 176-182

## Patches unchanged per O1 (no edit)

- **Patch 5 ER=EPR LMP**: operator algebra, not modular-flavor
- **Patch 7 BEC LMP**: UNCHANGED per O1

## Patch verified (no edit needed)

- **Patch 6 Proton-decay PRD**: B-ratio = 2.06⁺⁰·⁸³₋₀.₁₃, τ(e⁺π⁰)=6.6×10³⁴, τ(K⁺ν̄)=1.4×10³⁵ confirmed at lines 271-275 (M6 verdict.json consistency)

## Compilation result

| Paper | Pages | Status |
|---|---|---|
| P-NT BLMS | 11 | ✅ clean |
| Cardy LMP | 10 | ✅ clean |

## Files
- `SUMMARY.md` — this file
- `patch_log.md` — exact diffs per paper

## Discipline
- Hallu count: 85 → 85
- Mistral STRICT-BAN observed
- Surgical 1-3 sentence additions, no fabrication
