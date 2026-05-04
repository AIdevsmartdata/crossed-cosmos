# Appendix — Closed Pistes Re-Examination Worksheet

Companion to `STRATEGIC_SYNTHESIS.md` §2. Detailed per-piste re-examination with re-opening cost, expected yield, and recommendation.

---

## Re-examination matrix

Format: PISTE / CLOSURE-STATUS-IN-REPO / COULD-REFORMULATION-SAVE-IT / COST-TO-REOPEN / EXPECTED-YIELD / RECOMMENDATION

### v6.0.10 retracted pistes

| Piste | Closure rigour | Reformulation? | Cost | Yield | Recommendation |
|---|---|---|---|---|---|
| (b) firewall PBH C_jump | DEFINITIVE — 3 fatal issues + Bisognano-Wichmann universality | Need a non-trivial first-principles ε different from thermal time; none has emerged in 8 mo | 12+ mo R&D | LOW | **DO NOT REOPEN** |
| (c) Bell signed I_σ | DEFINITIVE — KRLP monotonicity argument is structural | Would require a non-physical I_σ definition; SGB target has no AQFT realisation | 6+ mo R&D | NIL | **DO NOT REOPEN** |

### v6.0.16 demotion of M1-C

| Piste | Closure rigour | Reformulation? | Cost | Yield | Recommendation |
|---|---|---|---|---|---|
| M1-C "conditional theorem" | demoted to Conjecture by editorial discipline (correct call) | Re-promotion needs Maass-form ↔ KMS bridge (3 gaps: chirality, σ_t-vs-Γ_N, explicit map) | 12-18 weeks | MODERATE if the bridge closes | **PARK as v7 R&D target M4 in main synthesis**; do not re-promote without bridge closure |

### v6.0.20-25 R-pistes (10-piste revolution wave)

| R-piste | Verdict | Re-open? | Cost | Recommendation |
|---|---|---|---|---|
| R1 (Cardy ρ=c/12) | CARVE-OUT, working conjecture | Already alive in eci.tex §3.9 | n/a | Status quo: working conjecture |
| R2 (Mixmaster invariant) | published as paper draft `paper/mixmaster_invariant/` | Already in repo | n/a | Submit when math-ph paper queue allows |
| R3-R7 | NEGATIVE | NO — adversarial review confirmed | n/a | Closed properly |
| R8 (FRW non-stationary) | CARVE-OUT, math.OA open question | Listed in §sec:limits item 8; natural target for §sec:bianchi extension paper | 4-6 weeks | **VIABLE — pursue jointly with Bianchi VIII closure (M1)** |
| R9-R10 | NEGATIVE | NO | n/a | Closed properly |

### v8 agent campaign (15 closed coupling attempts)

The 8 NEGATIVE-CLEAN verdicts deserve protective re-audit *only* because Mistral participated in some sub-checks. Concrete re-audit recommendation:

| Agent # | Original verdict | Mistral involved? | Re-audit priority |
|---|---|---|---|
| 01 (Legendre) | NEG-CLEAN | Yes (cross-check) | **Tier 2** — re-run with Gemini CLI cross-check only |
| 02 (MaxCaliber) | NEG-CLEAN | No | Tier 3 — passable |
| 03 (KW S-duality) | NEG-CLEAN | Yes | **Tier 2** — re-run |
| 04 (Wetterich) | NEG-CLEAN | No | Tier 3 |
| 05-08 (FRG/RG variants) | NEG-CLEAN | Mixed | Tier 2 — spot-check |
| 09 (Kashiwara-Schapira) | POSITIVE-REFORMULATION (DERIVED-UNDER-M2) | No | **VIABLE for math.AT paper M3 in main synthesis** |
| 10-11 | FRAMEWORK-INCOMPLETE | n/a | Park |
| 12 (Verlinde) | POSITIVE-REFORMULATION (compatibility w/ §mss-shadow) | No | Mention in §mss-shadow companion paper M4 |
| 13-15 | NEG-CLEAN | Mixed | Tier 2 — spot-check |

**Total Tier-2 re-audit cost**: ~1 week of Sonnet sub-agent work. Expected catches: 0-1 false negatives. Worth doing pre-v6.0.50.

### v7 manifesto (∞,2)-functor U conjecture

| Element | Status | Save-it reformulation? | Cost | Recommendation |
|---|---|---|---|---|
| (∞,2)-functor U existence | REFUTED in current form (Krylov 2π × rational MTC incompatible) | YES — replace rational MTC with non-semisimple (Hopf, quasi-Hopf, Lyubashenko) target | 6-9 mo + categorical algebra co-PI | **Do not pursue from this project's resources**; suggest Schäfer-Nameki-style outreach via SymTFT bridge X2 |
| Q_arith schematic placeholder | UNDEFINED, 4 obstructions | Probably not — see B2 in `project_mcc_v7_aspiration.md` | n/a | Drop; do not publish brand "MCC/CCF" |
| λ_arith ≈ 0.06 numerology | RETIRED to "implied scale not prediction" | n/a | n/a | Closed properly |
| BMV formula §VII.3 | DIMENSIONALLY INCORRECT in v1.0; FIXED in v0.2 | Use BMV 2017 canonical `m² ≥ πℏd/(2Gt)` | n/a | Use canonical form only |

### G2 Maass/KMS τ-fixing (G2 evening: closure blocked)

| Element | Status | Save-it? | Cost | Recommendation |
|---|---|---|---|---|
| KMS at β=2π → τ value | NO published bridge in DEHK/Qu-Ding/Faulkner-Speranza | Two-τ picture (M5 in main synthesis) bypasses but introduces 2 free moduli | 2-4 weeks | **Pursue M5 to verify the no-go is τ-pair-independent** |
| Polyharmonic Maass form Δ_k^r Y = 0 for r ≥ 2 | UNADDRESSED in published lit (H4 confirmed) | Genuinely open math.NT problem | indefinite | Park as open problem in math.NT companion to S1 |
| CM-point alternative (4.5.b.a → τ=i) | REFUTED tonight by V2 group-theoretic no-go | Two-τ picture or τ near i but not at i | 2-4 weeks | Same as above; M5 pursuit |

### Bianchi VIII, IX

| Type | Current label in AWCH paper | Closure path | Cost | Recommendation |
|---|---|---|---|---|
| IX | pathwise on BKL attractor (Heinzle-Uggla 2009 + Peter-Weyl SU(2) SLE) | Full unconditional Hadamard SLE | 12+ weeks | **Park** — pathwise is publishable as is |
| VIII | rigorous-pending-Hadamard | Explicit SLE construction, template = Banerjee-Niedermaier I + WKB lemma for V | **4-6 weeks** | **VIABLE — M1 in main synthesis**, closes 9-type table cleanly |

---

## Summary: pistes recommended for re-opening

In priority order for the next 1-3 months:

1. **Bianchi VIII Hadamard SLE** (M1) — 4-6 weeks, high yield, closes a cleanly-defined paper
2. **R8 FRW non-stationary classification** — 4-6 weeks, joint with M1, math.OA open question
3. **v8 agents Tier-2 re-audit** — ~1 week, protective, expected catches 0-1
4. **M5 two-τ picture for modular flavour** — 2-4 weeks, verifies V2 no-go is τ-pair-independent
5. **R2 Mixmaster invariant paper** — already in repo, just submit when queue allows

Pistes recommended for **definitive closure** (do not re-open):
- v6.0.10 (b) firewall — STRUCTURALLY CLOSED
- v6.0.10 (c) Bell I_σ — STRUCTURALLY CLOSED via KRLP monotonicity
- 7 of 10 R-pistes that returned NEGATIVE — properly adversarially reviewed
- v7 (∞,2)-functor U conjecture — REFUTED; needs categorical algebra co-PI to revive
- MCC/CCF brand — RETIRED (do not publish)
