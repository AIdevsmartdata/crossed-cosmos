---
name: A72 Damerell ladder extension — INTERRUPTED, retry pending
description: Algebraic invariants K=Q(i) extension to lepton sector + null test. Script saved, run timed out
type: project
---

# A72 — Damerell ladder extension (INTERRUPTED)

**Date:** 2026-05-05 night
**Owner:** Sonnet sub-agent (killed by SSH déco mid-flight 19:55 UTC)
+ parent local re-run attempt (killed at 17.5 min, mp.dps=60 too slow)
**Hallu count entering / leaving:** 85 / 85 (no fabrications)

---

## Verdict

**INTERRUPTED — no result.** Script `null_test.py` (16.8 KB) saved in this
directory. Sub-agent was killed by SSH disconnection before writing
SUMMARY; parent's local re-run (`python3 null_test.py`) hit harness timeout
at ~17.5 min wall-clock without output.

Diagnosis: mp.dps=60 × 512 trials × multiple observables (PMNS angles,
Jarlskog leptonic + CKM, Σm_ν, quark mass ratios) = O(10⁵+) high-precision
arithmetic ops. Script is correct but inefficient on a single core.

## Retry plan (Wave 12 Phase 1.5 or Phase 2)

Either:
1. **Optimize**: drop mp.dps=60 → 40 for the null test (4x faster per op);
   parallelize 512 trials over multiprocessing pool (8x more on 8-core VPS);
   total ~30s expected vs hours.
2. **Reduce scope**: 256 trials instead of 512; PMNS-only first, then
   extend to CKM if interesting; mp.dps=30.
3. **Run on PC**: cores=12 vs VPS cores=2; 6x speedup just from cores.

## Context (from script header, verified)

A62 already established that K=Q(i) Damerell ladder hits ≈ random
(1.7σ vs 285±17 expected). A72 was meant to extend the algebraic invariant
set to:
- Lepton-sector observables (PMNS angles, J_PMNS)
- Σm_ν (A14 prediction 65-69 meV, testable CMB-S4 2032+)
- Quark mass ratios MS-bar at μ=2 GeV

And test whether NEW invariants (Petersson inner product, Hecke
eigenvalue rationals, χ_4 phases) survive a STRICTER null test
(512 trials, max_q=15) than A62's original.

**No fabrication:** script is honest scaffold only. No claim made.

## Files
- `null_test.py` — 16.8 KB script, ready for optimized retry
- `SUMMARY.md` — this file

## Discipline
- Hallu count: 85 → 85 (script writes only candidate observables, no claims)
- Mistral STRICT-BAN observed
