---
name: F2 v2 sweep partial result + interpretation note
description: F2 ran but at HECKE-level (a_{p^m}×F1), NOT Damerell-L-value-level (α_m^L×F1) which is the actual M13.1(c) conjecture. Anchor sanity FAILED in original sense, but Hecke-level pattern is interesting. True F2 needs PARI/Sage. Hallu 86 unchanged
type: project
---

# F2 v2.1 — partial result, honest interpretation

**Date:** 2026-05-06 14:02 CEST
**Runtime:** 1.8s (10 newforms, LMFDB beta+cookie patch worked)
**Status:** PARTIAL — Hecke-level computed; Damerell-L-value level untested

## CSV results (10 rows)

| Label | CM disc | Steinberg | a_p² | v_2 (m=1,2,3,4) | Notes |
|---|---|---|---|---|---|
| **4.5.b.a** (anchor) | -4 (Q(i)) | NON-ST | 16 | **[0, 4, 9, 11]** | classification flag wrong (is Steinberg at p=2!) |
| 9.5.b.a | none | ST | -4 | [∞, 2, ∞, 6] | non-CM |
| 12.5.b.a | LMFDB miss | — | — | — | label may not exist |
| 16.5.b.a | LMFDB miss | — | — | — | label may not exist |
| 16.5.c.a | none | NON-ST | 0 | [∞, ∞, ∞, ∞] | non-CM, a_2=0 |
| 25.5.b.a | LMFDB miss | — | — | — | label may not exist |
| 27.5.b.a | -3 (Q(ω)) | NON-ST | 16 | [∞, 4, ∞, 11] | partial pattern hit |
| 36.5.b.a | LMFDB miss | — | — | — | label may not exist |
| 49.5.b.a | none | NON-ST | 40 | [1, 3, 7, 7] | non-CM, different |
| **100.5.b.a** | -4 (Q(i)) | NON-ST | 16 | **[0, 4, 9, 11]** | ⚡ IDENTICAL to anchor |

## Interpretation

### Critical issue
The script computes **v_2(a_{p^m} × F1_factor)** where:
- F1_factor = (-2)^{m-1} × (1 + 2^{m-3})
- a_{p^m} is the Hecke eigenvalue (= traces[2^m - 1])

But the **M13.1(c) conjecture is about α_m^F1 = α_m × F1_factor** where:
- **α_m = L(f, m) × π^(k-2m) / Ω_K^(2m)** (Damerell-renormalized critical L-value)
- The conjecture predicts **v_2(α_m^F1) = {-3, -2, 0, +1}** monotone

These are DIFFERENT quantities. The script's "anchor sanity FAIL" is not actually a refutation of M13.1(c) — it's a category mismatch in the implementation.

### Hecke-level finding (what was actually computed)

At the Hecke level (a_{p^m} × F1):
- **Q(i) CM newforms** (4.5.b.a level 4=2² ramified, 100.5.b.a level 100=2²·5² ramified-at-2):
  - **IDENTICAL F1 pattern [0, 4, 9, 11]** — strong consistency check
  - Both share the same multiplicative Q(i) structure at p=2
- **Q(ω) CM newforms** (27.5.b.a level 27=3³): partial pattern [∞, 4, ∞, 11] — m=2, m=4 match Q(i) Hecke values, m=1, m=3 are zero (a_p=0 expected for half the primes)
- **Non-CM newforms**: completely different patterns

### What this MEANS (honest)

1. ✅ **Hecke-level F1 fingerprint of CM-by-Q(i) newforms is consistent** — 4.5.b.a and 100.5.b.a give same pattern. NEW sanity check passed.
2. ⚠ **M13.1(c) conjecture not yet tested** — needs L-value computation, not Hecke computation
3. ⚠ **Steinberg classification flag in script is buggy** — 4.5.b.a IS Steinberg at p=2 (a_2 = -4 = -2^((k-1)/2)) but flagged "NON-ST"; needs fix for proper sweep interpretation

## Required for true F2 falsifier (M13.1(c) Damerell-level)

Need to compute α_m = L(f, m) × π^(k-2m) / Ω_K^(2m) for m ∈ {1,2,3,4}.

Tools needed (any one):
- **PARI/GP**: `mfinit + lfun + lfunmf` — Kevin can install: `sudo apt install pari-gp` (~50 MB)
- **SageMath**: `f.lseries().value(m)` — heavier install (~2 GB)
- Manual: compute Hecke Grössencharacter ψ on Q(i), use Damerell theorem with Eisenstein series — requires expert implementation

## Action items

1. **Install PARI/GP on PC** : `sudo apt install pari-gp` (Kevin only, sudo needed)
2. **F2 v3 script** : rewrite using PARI subprocess to compute true α_m^F1
3. **Steinberg classifier fix** : current logic incorrectly flags 4.5.b.a as NON-STEINBERG; should detect a_p = ±p^((k-1)/2) per LMFDB Steinberg field

## Discipline
- 0 fabrications by parent
- LMFDB beta+cookie patch documented (working endpoint identified)
- Hecke-level finding (Q(i) consistency [0,4,9,11]) is genuine but NOT the M13.1(c) conjecture test
- Hallu 86 → 86 (Damerell-level test deferred to F2 v3 with PARI)
