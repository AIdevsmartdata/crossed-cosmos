# A62 — Systematic CKM extension of A17 K=Q(i) Damerell-ladder

**Date:** 2026-05-05 night
**Owner:** Sonnet sub-agent A62 (parent persisted; harness blocked SUMMARY write — content reproduced from agent output)
**Hallu count entering / leaving:** 85 / 85 (held; mp.dps=60 throughout, Mistral STRICT-BAN)

## Verdict

**WEAK / NULL-DOMINATED.** A62's central finding **REDUCES CONFIDENCE** in the entire K=Q(i) Damerell-ladder numerology framework (incl. A17's surviving |V_us|=9/40).

## Critical findings

### (1) A17 |V_cb|² = 1/600 is RETIRED

A17 used HFLAV-2024 |V_cb|=0.04085. PDG/HFLAV-2025 average shifted to **|V_cb|=0.04183(79)** ⇒ a₁·a₄=1/600 now sits at **1.26σ** (no longer <0.1σ).

Replacement: **|V_cb|² = (7/4)·α₁³ = 7/4000 = 0.00175** at 0.0038σ.

### (2) NULL TEST is decisive — Q(i) ladder ≈ random

Replacing the {1/10, 1/12, 1/24, 1/60} ladder with random small rationals of comparable magnitude (8 trials) yields **285 ± 17 sigma<0.1 hits**, vs Q(i)'s **315 hits — within 1.7σ of random expectation**.

**Q(i) is statistically indistinguishable from a random small-rational ladder.** The cross-K specificity test is a tautology (different K = different rationals = no transfer).

### (3) Top NEW headline candidates (all empirical, multiplicative coeffs un-derived)

| CKM | Formula | Closed | σ |
|---|---|---|---|
| \|V_ub\| | (6/5)·α₁²/π | 6/(500π) | **0.0014** |
| \|V_tb\|² | (5/4)·α₂·π² | 5π²/48 | **0.0019** |
| \|V_td/V_cb\| | (16/13)·α₄/α₁ | 8/39 | **0.0017** |
| \|V_us\|²+\|V_cb\|² | (22/7)·α₄ | 11/210 | **0.0054** |
| \|V_td/V_ts\| | (11/12)·α₁·√5 | 11√5/120 | **0.0039** |
| \|V_cb\|² | (7/4)·α₁³ | 7/4000 | **0.0038** |
| \|V_td\|² | 2·α₂²·α₄/π | 1/(4320π) | **0.015** |
| \|V_ub\|² | α₄³·π (q=1!) | π/216000 | **0.031** |
| J_CKM | (3/5)·α₁²·α₄/π | 1/(10⁵π) | **0.021** |
| \|V_ub/V_cb\| | (4/3)·α₂²·π² | π²/108 | **0.012** |

### (4) Most parsimonious survivor

|V_ub| = 6α₁²/(5π) — 0.0014σ, q=6/5, single π¹, structurally meaningful per Damerell-Beilinson L(f, 2m) algebraicity. This single hit deserves to be flagged but **CANNOT** be promoted to "prediction" given the null-test result.

## Honest framing

- All multiplicative coefficients (6/5, 7/4, 22/7, 16/13, 11/12, 5/4, 3/5, 19/6, ...) remain **EMPIRICAL** (per A17 caveat).
- A62's null test should **REDUCE confidence** in the entire K=Q(i) numerology framework — including A17's surviving |V_us|=9/40 (which is itself a small-q, small-denom hit and equally consistent with random expectation).
- The Damerell-CS theoretical foundation (H7') for the {1/10, 1/12, 1/24, 1/60} ladder remains intact (rigorous via Hurwitz/Chowla-Selberg/Damerell), but its **selection power** as a CKM-derivation tool is null.

## Falsifiers (sharp 2026-2030)

- **|V_us|² + |V_cb|² = 11/210**: NA62/CKM-LAT 2026-2027 (most sensitive — first-row unitarity at 0.001 precision)
- **|V_ub| = 6/(500π)**: Belle II + LHCb B→πℓν 2027-2030
- **|V_tb|² = 5π²/48**: LHC Run 4 single-top σ 2030+
- **J_CKM = 1/(10⁵π)**: Belle II + LHCb global UT fit 2028-2030

## Files written

- `ckm_pslq_search.py` (main systematic search)
- `ckm_hits.json` (1000s of hits, 328 Q(i)-specific)
- `analyze_hits.py` + `ckm_hits_dedup.json` (dedup by exact rational)
- `null_test.py` (random-ladder sanity check — load-bearing)
- `cleanest_q1.py` + `ckm_tiny_q.json` (tiny-q only)
- `verify_top_hits.py`, `headline_hits.py`, `ckm_headline.json`

## Recommended action

- **v7.5 framing**: explicitly demote the K=Q(i) Damerell ladder from "predictive" to "consistency tool". Cite null test in §3.
- **A17 amendment**: flag |V_us|=9/40 as a single-hit consistency, NOT a derivation. Keep the closed-form table as illustrative scaffold.
- **DO NOT** promote |V_ub|=6/(500π) as a "prediction" without theoretical motivation for the 6/5 coefficient.
- Hallu ledger: 85 unchanged (no fabrications).
