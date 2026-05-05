# A19 — BEC observable from A11 modular shadow BOUND theorem

**Date:** 2026-05-05 mid-day
**Owner:** Sonnet sub-agent A19 (parent persisted; harness blocked Sonnet's direct write)
**Hallu count entering / leaving:** 77 / 77 (no fresh fabrications; 4 new arXiv IDs live-verified)

## Verdict

**WEAK NEW MEASURABLE PREDICTION IDENTIFIED.** A11's BOUND theorem promotes the existing companion note's equality conjecture into a one-sided falsifier on Steinhauer/Kolobov data that is *robust* to integrability counter-examples (Avdoshkin-Dymarsky 1911.09672, Camargo 2212.14702, Sreeram 2503.03400) — these refute the saturation form but leave the bound form intact.

## The new prediction (BOUND form, distinct from saturation form)

For Steinhauer 2019 parameters T_H = 0.35 ± 0.10 nK:

**Γ_bound ≡ 2π k_B T_H / ℏ = (288 ± 82) s⁻¹**

A11's BOUND theorem (λ_K^mod ≤ 2π/β at finite-rank type-II_∞) implies Γ_meas ≤ Γ_bound for *any* exterior-phonon temporal correlator: g²(τ), G²(z₁,z₂,t) envelope, or Hawking ramp-up rate.

## Why this is genuinely new vs companion note

The existing `/root/crossed-cosmos/paper/bec_steinhauer_krylov/note.tex` Conjecture 1 predicts **equality** Γ = 2π k_B T_H / ℏ. Per A11, this equality is conjectural — free-QFT counter-examples saturate the bound without type-II_∞ chaoticity. The BOUND form (Γ ≤ Γ_bound) is what A11's finite-rank theorem actually proves and is robust to the integrability counter-examples that the saturation conjecture cannot survive.

- **Saturation falsifier (companion):** |Γ_meas − Γ_bound|/Γ_bound > 10% at 5σ.
- **BOUND falsifier (new, A19):** Γ_meas > Γ_bound at 5σ refutes type-II_∞ kinematic prefactor independently of any chaos hypothesis.

## Falsifier table

| Γ_meas regime | Verdict |
|---|---|
| < 0.5 × Γ_bound (=144 s⁻¹) | Bound CONSISTENT, saturation REFUTED |
| ∈ [0.8, 1.2] × Γ_bound | Bound + saturation both CONSISTENT |
| > 1.5 × Γ_bound (>432 s⁻¹) at 5σ | A11 finite-rank theorem REFUTED, type-II_∞ scaffolding falls |

## Experimental setup

**Primary: Kolobov-Golubkov-Munoz de Nova-Steinhauer 2021** (arXiv:1910.09363 ✓, Nat. Phys. 17 362). Already measured time evolution at six timepoints, 97,000 reps, 124-day acquisition. Re-analysis of the temporal envelope of G²(z₁,z₂,t) can extract Γ_meas directly.

**Secondary platforms** (independent substrates for cross-validation):
- Solnyshkov-Paquelier-Balmisse-Malpuech 2026 (arXiv:2603.01664 ✓): polariton condensate analog BH merger
- Weinfurtner Gravity Lab water-tank vortex (relocating Manchester 2026); Torres-Patrick et al. PRL 125 011301 measured QNM decay rates of surface waves
- Chandran-Fischer 2026 (arXiv:2604.02075 ✓): UV-finite volume-law entanglement negativity — entanglement growth rate also bounded by 2π T_H

## Live-verified arXiv refs (this session, 4/4 ✓)

| Tag | arXiv | Status |
|---|---|---|
| Steinhauer2019 | 1809.00913 | ✓ Nature 569 688; T_H = 0.35 ± 0.10 nK |
| Kolobov2021 | 1910.09363 | ✓ ramp-up + stationary phase, six timepoints |
| ChandranFischer2026 | 2604.02075 | ✓ UV-finite volume negativity |
| Solnyshkov2026 | 2603.01664 | ✓ polariton analog BH merger |

Re-cited from A11 (already verified, not re-fetched): Parker et al. 1812.08657, MSS 1503.01409, Caputa et al. 2306.14732.

## Recommended next step

Edit `/root/crossed-cosmos/paper/bec_steinhauer_krylov/note.tex` §4 to split Conjecture 1 into:
- **Conjecture 1a (BOUND, A11-licensed):** Γ_meas ≤ 2π k_B T_H / ℏ
- **Conjecture 1b (SATURATION, working):** Γ_meas = 2π k_B T_H / ℏ

Cross-reference `/root/crossed-cosmos/notes/eci_v7_aspiration/A11_MODULAR_SHADOW_THEOREM/SUMMARY.md`. The Kolobov 2021 re-analysis (Phase 1 of companion note) becomes a falsifier for Conjecture 1a directly, even if 1b stays open.

## Discipline log

- 4 arXiv refs WebFetch-verified, 1 WebFetch denied (Technion lab page) — worked around via arXiv PDF directly.
- No Mistral usage. No fabrications.
- A19 explicitly distinguishes the (provable) BOUND from the (conjectural) SATURATION — addressing A11's audit caveat that companion note's equality prediction is stronger than the modular shadow theorem licenses.
- Hallu count exit: **77** (held).
