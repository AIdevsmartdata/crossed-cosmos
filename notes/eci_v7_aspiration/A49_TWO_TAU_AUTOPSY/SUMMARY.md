# A49 — Two-τ Autopsy of Du-Wang arXiv:2209.08796

**Date:** 2026-05-05 evening
**Owner:** Sonnet sub-agent A49 (parent persisted)
**Hallu count entering / leaving:** 84 / 84 (held; 1 framing correction logged against A42)

**Source verified live**: Du, X. K. & Wang, F., *"Flavor Structures of Quarks and Leptons from Flipped SU(5) GUT with A_4 Modular Flavor Symmetry"*, arXiv:2209.08796v2, JHEP 01 (2023) 036. PDF (632 KB) read directly via `Read` tool — pages 1–9 and 29–36. No Mistral.

## 1. CRITICAL CORRECTION TO A42 FRAMING

A42 row 5 said *"single-τ Model IX' = 1.558; dual-τ = 95 (60× WORSE)"*. **This is a category error.** The two numbers compare DIFFERENT objects:

| Object | Single τ | Two τ |
|---|---|---|
| **Sample IX' of Scenario III** | **χ²_total = 1.58** (q:1.221, l:0.358) — Table 5 | not reported (already at data floor) |
| **Scenario III generic** (worst sub-scenarios) | ~282.4 | ~95 |
| Sub-scenario IX (Scenario II), lepton only | χ²_l = 486.0 | χ²_l = 30.2 |
| Sub-scenario X' (Scenario III), lepton only | χ²_l = 233.0 | χ²_l = 58.9 |
| Scenario I, lepton only | χ²_l = 236.3 | χ²_l = 48.8 |

Du-Wang explicitly state two-τ migration **improves** the lepton fit by 4–16× in every sub-scenario where they tabulate both. The "60×" arises from comparing Sample IX' single-τ (a sweet spot) against Scenario III's generic-bad dual-τ (different sub-models).

## 2. Mechanism

Sample IX' wins because (a) flipped SU(5) GUT-locks $Y^D = (Y^E)^T$ (one Yukawa makes both down-quark and charged-lepton matrices), so the lepton sector inherits any tuning that succeeds for quarks; (b) the (1', 1'', 1'') singlet assignments with weights (2, 4, 2) for $\bar{F}_{1,2,3}$ provide just enough freedom for one τ in fundamental domain to satisfy quark hierarchy AND PMNS angles simultaneously. **Mechanism is GUT-locked structure + lucky weight assignment**, NOT cancellation.

## 3. Verdict — GENERIC or SPECIFIC?

**Two-τ is generically HELPFUL empirically**, not harmful. A42's empirical case collapses. **However**, Du-Wang themselves argue (§4, conclusions) that two-τ is **theoretically problematic**: GUT reps (flipped SU(5) $\bar{10}$, SO(10) 16) contain BOTH quarks and leptons, so independent τ_q, τ_l "spoils unification of matter contents". They propose a 5D $M_4 \times S^1/Z_2$ orbifold that breaks $A_4^Q \times A_4^L \to$ diagonal $A_4^D$ via boundary conditions (eqs. 4.13–4.16), restoring single low-energy modular symmetry.

## 4. Implications for ECI v7.5

1. **Drop A42's "60× worse" claim** — re-tag row 5 of A42_TOP5_BSM_COMPARISON.
2. **Keep single-τ as math-anchor on STRUCTURAL grounds, not numerical**: the genuine argument is GUT matter-unification, not empirical χ².
3. **CM-anchored ATTRACTOR (v7.4) survives**: ECI's selected τ* (W1: τ ≈ -0.19+1.00i) plays Sample IX' role — a special high-symmetry point where ONE modulus suffices.
4. **If v7.5 wants UV two-τ, inherit Du-Wang's orbifold-BC reduction** to a single IR τ — this becomes a *predicted constraint*, not freedom.
5. **Re-frame the "two-τ harmful" thesis** as unification-violation, not χ²-degradation.
