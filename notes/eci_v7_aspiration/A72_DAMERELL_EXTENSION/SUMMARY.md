---
name: A72 Damerell ladder extension — DEAD-END finding (definitive)
description: K=Q(i) numerology indistinguishable from random rationals on PMNS+lepton+quark observables (-0.33σ, P=0.63)
type: project
---

# A72 — Damerell ladder extension: DEAD-END finding

**Date:** 2026-05-05 night → 2026-05-06 (replaced INTERRUPTED status with definitive result)
**Owner:** Parent agent (Sonnet sub-agent and original local re-run both timed out;
parent-written `null_test_optimized.py` finished in 0.8s after vectorization)
**Hallu count entering / leaving:** 85 / 85

---

## Verdict

**STRONG DEAD-END.** K=Q(i) Damerell-ladder numerology is **statistically
indistinguishable from random rational ladders** when extended to the
PMNS + lepton + quark observable space (PDG 2024, NuFit-5.3, HFLAV 2025).

This is a clean, definitive negative result — stronger than A62's 1.7σ —
because the test domain is broader (19 observables vs A62's 2) and the
optimization is faster (0.8s vs minutes), enabling full 512-trial null
distributions with both lax and strict cuts.

---

## Headline numbers

| Cut             | Threshold              | Q(i) hits | Null mean ± sd  | σ vs mean | Tail prob |
|-----------------|------------------------|-----------|-----------------|-----------|-----------|
| Lax             | σ<0.5, \|q\|≤5/4       | 718       | 698.5 ± 42.9    | **+0.46** | 0.32      |
| **Strict**      | σ<0.3, \|q\|≤1         | 358       | 366.2 ± 25.0    | **−0.33** | **0.63**  |

**Strict cut is DOMINANT** for evidence: Q(i) is **below** the random mean.
Tail probability 63.3% — totally consistent with chance.

---

## What this kills

A62 already retired |V_cb|² = 1/600 (HFLAV-2025 → 1.26σ) and reported the
remaining V_us = 9/40 + V_cb candidates at only 1.7σ vs random.

A72 extends the test to the FULL Damerell-derivable invariant space (150
candidates: products α_i·α_j, α·π^k, α·√n, α·|λ_p|, w_K factors, ...) and
the FULL low-energy observable space (PMNS angles, J_PMNS, J_CKM,
Σm_ν, ratio Δm²₂₁/Δm²₃₁, mu_md, ms_md, mc_ms, mb_mc, mt_mb, yu_yt,
yc_yt, yd_yb, ys_yb).

Result: **Q(i) is BELOW random mean** under the structural-tightness cut
(σ<0.3, |q|≤1). The K=Q(i) ladder has no detectable structural signal
on any of these observables.

## Implications for v7.5+ amendment

Sections claiming "K=Q(i) Damerell-ladder structural fingerprint" must be
**REMOVED or downgraded**. Specifically:
- v7.5 §X.Y on V_us = 9/40 etc. must be reframed as "speculative
  numerical observation, P_null > 30%" rather than structural prediction
- Eq. block referring to α_m ladder "anchoring" the PMNS sector should
  be flagged with "no statistical preference vs random", citing this A72
- The H7' axiom (integer Damerell ladder as structural input) is
  **further weakened** beyond A78's reformulation — it's now a notation
  convention, not a falsifiable structural claim.

This is a healthy scientific outcome: the framework's CM/Damerell
backbone is valid as an arithmetic anchor (LMFDB 4.5.b.a, Hecke H_1)
but does NOT encode predictions of low-energy fermion observables
beyond what numerology with random rationals would also produce.

## Optimization story (script-level)

The original `null_test.py` (mp.dps=60, 512 trials) timed out at >17min
without producing output. `null_test_optimized.py`:

1. Build invariants ONCE using mpmath at mp.dps=30, immediately convert
   to float64 (sufficient for σ<0.3 cuts; high-precision only needed
   for the L-value rationals which are exact)
2. Hit-counting via numpy broadcasting: 150 inv × 90 quotients × 19 obs
   = 256k simultaneous comparisons per call
3. multiprocessing.Pool over 512 trials on 4 CPU cores

Total: **0.8 seconds** vs original >17min → **>1000× speedup**.

---

## Files

- `null_test.py` (16.8 KB) — original sub-agent draft, kept for record
- `null_test_optimized.py` (10 KB) — production script, this result
- `null_test_results.json` — full posterior (counts, percentiles, etc.)
- `SUMMARY.md` — this file

## Discipline

- Hallu count: 85 entering → 85 leaving
- Mistral STRICT-BAN observed
- Result computed locally on VPS, verifiable: re-run `python3 null_test_optimized.py` → same numbers (deterministic seed 20260505).
- No fabrication; all 19 observables have PDG/NuFit citations in code header.
