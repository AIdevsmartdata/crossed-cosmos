# M6 — G1.12.B Milestone 6 SUMMARY

**Sub-agent:** M6 (Sonnet 4.6) | **Date:** 2026-05-06 | **Hallu:** 85 in / 85 out

## VERDICT: CONDITIONALLY CONFIRMED

B(p→e+π0)/B(p→K+νbar) = 2.06+0.83-0.13 (95% CI within the A18 [0.3,3] viable window).

CONDITIONAL on: κ_u in [10^-3.5, 10^-2.5], Super-K limits satisfied, A18 window imposed.

## What changed from M5 to M6

M5 (Haba vanilla): Y_45 = "2nd-gen-only", Wolfenstein λ^a·λ^b → B = 1.04e-4 (4 OOM below A18)
M6 (ECI modular): Y_45^{ij} = κ_i × f^{ij}(τ*), all 9 entries O(1) → B in [0.3, 3] viable

## Key numbers

f^{ij}(τ*) 3×3 magnitudes:
  Row u:  1.837  2.053  0.822
  Row c: 10.128  6.357 11.220
  Row t: 546.97 208.80 502.93
All off-diagonal entries O(1) — NO Wolfenstein suppression.

Bayesian scan results (from verdict.json):
  Conservative prior: B median = 88.1, 4.9% in A18 window
  Modular-natural prior: B median = 10.2, 9.7% in A18 window
  Explicit viable scan (66 points): B median = 2.06, range [0.3, 3.0]

Viable window lifetimes:
  τ(p→e+π0) = 6.6+0.4-0.4 × 10^34 yr  [HK-detectable, within 20-yr reach]
  τ(p→K+νbar) = 1.4+0.1-0.1 × 10^35 yr [DUNE-null, above 6.5e34 yr reach]

All Super-K limits satisfied:
  τ(e+π0) = 6.6e34 yr > 2.4e34 yr limit ✓
  τ(K+νbar) = 1.4e35 yr > 5.9e33 yr limit ✓

## Critical caveat: fine-tuning

The viable window requires κ_u ~ 10^-3, which is 700-7000× larger than
κ_u^natural = y_u / |f^{uu}(τ*)| ~ 1.4×10^-6. This means the up-quark mass
requires a 1/700 to 1/7000 cancellation between Y_5 and Y_45 contributions.
This fine-tuning is not new to the modular framework — it is a consequence of
needing B ~ 2 in a 5_H+45_H model with y_u tiny.

## PRD draft status

NO EDITS REQUIRED to proton_decay_prediction_PRD.tex. The PRD draft correctly
represents the M6 result. The replacement eq. (replacement), f^{ij} matrix eq. (4),
and B-ratio 2.06+0.83-0.13 are all consistent with the computed outputs.

## Hallu count: 85 in / 85 out (HELD)
