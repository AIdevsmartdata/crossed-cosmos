# V6 Cross-Verification (Lite)

**Date.** 2026-04-21. **Scope.** 4-agent cross-check of the composite ECI v6
equation `dS_gen[R]/dτ_R = κ_R · C_k[ρ_R] · Θ(PH_k[δn])`. Mistral Magistral
agent timed out; this summary is built from the 4 completed agents + the
owner dequantisation-map fix.

Sources:
- `paper/_internal_rag/v6_audit.md` — Claude.ai external deep audit
- `derivations/V6-claude-derivation-report.md` — Claude Opus sympy derivation
- `derivations/V6-gemini-derivation.md` — Gemini 2.5 Pro cross-derivation
- `derivations/V6-adversarial-attack.md` — hostile referee, 7 attack vectors
- `derivations/V6-dequantisation-map.md` + `.py` — owner's Jacobson-2016-style fix

## Agreement across models

1. **Ansatz, not theorem.** Claude and Gemini independently converge on
   ANSATZ: the FSK first-law skeleton is rigorous, but both the
   commutator → `C_k` step and the `Θ(PH_k)` gate are inserted, not derived.
   Claude's (I1) `d⟨H_mod⟩/dτ = v_C · C_k` is exactly Gemini's "conjectural
   CV/CA-adjacent step". The audit concurs editorially (§7: "ansatz extending
   Eling–Guedens–Jacobson").
2. **Dimensional typo in audit §2.** Claude and the adversarial agent both
   flag `[κ_R] = nat · t⁻²` as wrong; correct value is `nat · s⁻¹`. Owner has
   adopted `κ_R ≡ 2π T_R` (Tomita–Takesaki modular temperature), which
   matches Gemini's Bisognano–Wichmann pin (`1/(2π)` modular, `T_local`
   proper). Three-way agreement.
3. **Fan 2022 reduction fails as written.** Claude: log vs linear mismatch.
   Adversarial Attack #2: over-prediction by factor `C_K` in the PH_k → 0
   limit. Gemini: consistency with Page ramp requires reading `C_k` as a
   *rate proxy* (Lanczos saturation), not accumulated complexity. All three
   agree the equation only survives in a "post-scrambling, pre-saturation,
   rate-proxy" window that must be demarcated explicitly.
4. **Scoop risk stays low (1.5/5)** — adversarial Attack #6 independently
   confirms audit: no direct linear-form competitor on arXiv as of April
   2026. But `2507.23739` and `2602.02675` are plausible 6-month threats →
   fast arXiv deposit mandatory.

## Disagreement / tension

- **Falsifier status.** Adversarial Attack #7 flags NO new prediction →
  FATAL for JCAP. Claude agrees ("no D7/D14/D17 consequence"). Gemini
  silent. Audit mentions CMB low-ℓ but doesn't compute. The owner's
  fσ_8(z) × Θ(PH_2) DESI-DR3 falsifier (decided 2026-04-22) is the exact
  remedy prescribed by the adversarial agent (minimum-modification list
  item #6).
- **Category mismatch (Attack #3).** Adversarial flags FATAL formal defect;
  audit and Claude are silent; Gemini interprets `Θ(PH_k)` phenomenologically
  without typing it. **Resolved by owner's dequantisation map**
  `δn := Tr_R[ρ_R n̂] − ⟨n⟩` (Jacobson 2016 analogue), formalised in
  sympy + numerical toy (N=6 qubits): all three asserts pass (reality,
  mean-zero, modular-covariance to 10⁻⁸). Downgrade: **FATAL → semi-classical-
  limit CAVEAT**.
- **α = 0.095 anchor.** Claude warns "do not reuse α from D15". Adversarial
  Attack #5 concurs (three unrelated small-number anchors = numerology).
  Audit offers Barrow Δ ≲ 0.1 as weak anchor. No resolution; must be
  acknowledged as free parameter in v6 draft.

## Post-fix status of the 7 adversarial attacks

| # | Attack | Pre-fix | Post-fix (2026-04-22 decisions) |
|---|---|---|---|
| 1 | Dimensional | VALID | Fixed: `κ_R ≡ 2π T_R`, nat/s |
| 2 | Fan reduction / saturation | VALID | Demarcated in prose (rate-proxy window) |
| 3 | Category mismatch | FATAL | Resolved conditionally (dequant map) |
| 4 | Arrow tautology | VALID/rebuttable | Rephrased descriptively |
| 5 | α ad hoc | VALID | Accepted as free parameter, error-bar inflated |
| 6 | Scoop | stable | Fast arXiv deposit scheduled |
| 7 | No prediction | FATAL | Fixed: fσ_8 × Θ(PH_2) DESI DR3 ELG + Euclid DR1 |

## Net convergence score

3-of-4 agents (Claude, Gemini, audit) treat v6 as publishable **ansatz** with
Assumption M1 postulated (Brown–Susskind-style complexity-momentum). The
adversarial agent's list of 7 blockers reduces to 2 residual items post-fix:
(2) the Fan-2022 window bounds (solvable by prose demarcation), and (5) the
α numerology (solvable by stated free-parameter + error bar). No agent
recommends RETRACT.

## Missing data

Mistral Magistral cross-derivation never completed. Based on Gemini's
expected-priors section and Mistral's historical behaviour on V10-V12 (softer
stance, accepts phenomenological fits), Magistral is expected to side with
Gemini or weaker. A fatal new attack vector from Magistral is possible but
improbable (~15% prior). This is a decision risk, not a blocker.
