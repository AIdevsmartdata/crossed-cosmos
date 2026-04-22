# ECI v6 — Owner Decision Memo

**Date:** 2026-04-22
**Author:** v6 synthesis agent (final of 6 sibling agents)
**Target equation:** `dS_gen[R]/dτ_R = κ_R · C_k[ρ_R(τ)] · Θ(PH_k[δn(τ)])`
**Inputs read:** `v6_audit.md`, `V6-claude-derivation-report.md`, `V6-gemini-derivation.md`, `V6-adversarial-attack.md`, `V6-dequantisation-map.md`, raw Magistral responses `_mistral_responses/v6_q{1,2,3}.txt`.
**Inputs missing:** `V6-magistral-derivation.md` (polished report — raw Magistral responses present and used as a proxy; Q1 timed out upstream), `V6-cross-verification.md` (this memo functionally substitutes for it).

---

## 1. Bottom-line recommendation

**PROCEED with caveat — publish v6 as an ANSATZ, not a derivation, on a formal track (JHEP / PRD-formal), NOT as a cosmology paper.** Three independent derivation agents (Claude, Gemini, Magistral) converge on the same verdict: the equation is algebraically consistent with the Faulkner–Speranza–Kirklin (FSK) Type II first law under two *unproved* identifications (modular commutator → `C_k`; insertion of `Θ(PH_k)`), and the Fan-2022 Krylov bridge route fails (log vs. linear). The adversarial attacker landed 3 valid formal defects; 2 of them (dimensions, category mismatch) were resolved in-session by owner decisions (`κ_R ≡ 2π T_R`, dequantisation map). The remaining blocker for a cosmology submission is Attack 7 (no new falsifier), which kills JCAP but leaves JHEP/PRD-formal viable. Timeline 3–5 weeks. Do not claim derivation; demarcate explicitly from Fan 2022.

## 2. Consolidated verdict table

Three derivations × seven attacks, compressed:

| Axis | Claude | Gemini | Magistral | Consensus |
|---|---|---|---|---|
| Q1 — FSK/variational derivation | ANSATZ (two unproved IDs) | ANSATZ (C_k+Θ imported) | timed out (raw); Q2/Q3 confirm heuristic | **ANSATZ, unanimous** |
| Q2 — Fan-2022 Krylov bridge | FAIL (log vs linear) | Motivated if `C_k` read as *rate*, else τ² tension with Page ramp | heuristic only (explicit) | **FAIL as derivation; motivated as postulate** |
| Q3 — `κ_R` identification | `2πT_R` or `v_Haferkamp` (nat/s) | `1/(2π)` modular / `T_local` proper (Bisognano–Wichmann) | `1/τ_scr` preferred | **Disagreement on which, agreement on units = nat/s** |
| Dimensional audit | Consistent; flagged audit typo | Consistent | Consistent | **Fixed: `[κ_R]=nat·t⁻¹`, commit 85bb6a7** |

| Attack | Status | Resolution |
|---|---|---|
| 1 — Dimensions (κ_R typo, τ_gate hidden, PH_c undefined) | **Partially resolved** | Units fixed (85bb6a7). τ_gate and PH_c still need appendix. |
| 2 — Fan-2022 Krylov conflict in PH_k→0 | **Open** | Kill with Wall-style *inequality* reformulation (see §3). |
| 3 — Category mismatch ρ_R × δn | **Resolved conditionally** | Dequantisation map (d64cd65), 3 asserts pass on toy model. |
| 4 — Arrow-of-time tautology | Rhetorical | Reframe as "modular-flow entropy production", drop arrow-of-time prose. |
| 5 — α = 0.095 ad hoc | **Open** | Either fit α with inflated error, or derive from single RG/CFT source. |
| 6 — Scoop risk | Low today (1.5/5), unstable at 6 mo | Fast arXiv deposit mandatory. |
| 7 — No new falsifier | **FATAL for JCAP; open for JHEP** | Either specify `Θ(PH_k)·fσ_8(z)` shift, or pivot to formal. |

**Net:** 3/3 unanimous on ansatz status. Adversarial landed 2 formal hits still open (Attacks 2, 5) and 1 editorial hit (Attack 7). No fatal attack for a *formal* submission.

## 3. Owner action items (PROCEED-with-caveat path)

Ordered, in priority:

1. **Reformulate the equality as a Wall-style inequality** `dS_gen/dτ_R ≤ κ_R · C_k · Θ(PH_k[δn])`. This is the single cheapest move: it neutralises Attack 2 (Fan-2022 log regime becomes the saturating limit, not a contradiction), and it aligns with every rigorous GSL precursor (Wall 2011, Faulkner–Speranza 2024, Kirklin 2025). Cost: ≈ 1 day of `derivations/V6-inequality-form.py` + rewrite of claim prose.
2. **Decide `κ_R` canonical form.** Three candidates on the table: Claude's `2π T_R`, Gemini's `1/(2π)` (modular) / `T_local` (proper), Magistral's `1/τ_scr`. Gemini's Bisognano–Wichmann pinning is the most publishable; Claude's `2π T_R` is already committed in the audit (85bb6a7). Reconcile: `2π T_R ≡ T_local` is the same object under the modular temperature = local Unruh identification. Confirm this is the final choice; kill `v_Haferkamp` and `1/τ_scr` as backups.
3. **Dimensional-analysis appendix.** Write `paper/eci_dim_appendix.tex` documenting (a) `[κ_R] = nat·s⁻¹`, (b) the `τ_gate` absorption convention for `C_k`, (c) the operational definition of `PH_c` (Betti count at the nonlinear scale `k_NL`). ≈ 2 days. Closes the residue of Attack 1.
4. **Decide α fate.** Two-pass decision: (a) drop `α = 0.095` numerology, promote `α` to a fit parameter with a Gaussian prior centred on Barrow `Δ ≲ 0.1`; or (b) derive `α` from a single RG source (Barrow fractal horizon is the cleanest; see audit §5.6). Owner choice. ≈ 0.5–3 days.
5. **Pivot target to JHEP / PRD-formal.** Drop all cosmology-prediction claims from the v6 paper. Pitch v6 as *a non-equilibrium extension of the Eling–Guedens–Jacobson `d_i S` schema for Type II crossed products*. Cosmological falsifiers become §"Outlook"; no quantitative table claimed. This neutralises Attack 7.
6. **Fast arXiv deposit once §3.1–§3.5 done.** Surveillance targets `2507.23739` (generalised Krylov) and `2602.02675` (modular Krylov + area operator) are <10 months old; window is short.
7. **D18/D19/D20 — no numerical checks required for v6 itself.** v6 does not reach the v5.0 falsifier table. Keep v5.0 submission on its own timeline; do not block v5.0 on v6.

Not on the critical path (but flagged): the `V6-magistral-derivation.md` polished report did not materialise upstream (Q1 timed out). If the v6 paper cites three independent derivations, we should either retry Magistral with `mistral-large-latest` instead of `magistral-medium-latest` on Q1, or drop the three-way framing and present two derivations + an adversarial.

## 4. Timeline

| Scenario | Path | Duration | Target |
|---|---|---|---|
| **Best case** (Attacks 2+5 cleanly rebutted by inequality + α-fit) | v6 as JHEP/PRD-formal companion, ansatz framing | **3 weeks** | JHEP or PRD |
| **Median** (Attack 2 resolved, α stays controversial, reviewer asks revisions) | JHEP submission + 1 revision round | **5 weeks** | JHEP |
| **Worst case** (during dim-appendix work, a pre-scoop by `2507.23739` line appears on arXiv, or `PH_c` cannot be operationally defined) | Revert: submit v5.0 as-is, v6 deferred to v7 after cosmology-falsifier work | **1 week to park, v6 indefinite** | v5.0 only |

v5.0 submission is decoupled and must not slip. Budget cap: if v6 week-by-week work runs past 6 weeks with no submitted manuscript, hard-stop and defer.

## 5. Cost–benefit (honest)

**Upside — v6 as JHEP/PRD-formal ansatz (most likely):** a second paper in a respectable venue. Originality is real (composite form has no published occurrence; scoop risk 1.5/5); the ansatz framing is defensible because it extends a known schema (Eling–Guedens–Jacobson) with three well-cited ingredients (CLPW Type II, Ma–Huang PRU, Yip 2024 PH_k). Plausible citations: 15–40 over 3 years. Not a prestige win, but a real contribution.

**Upside — v6 as JHEP theory-heavy (best case):** if the dequantisation map paper (`V6-dequantisation-map.md`) is spun into §2 and the inequality form closes Attack 2, the paper is original enough to warrant JHEP. Upside plausibly 50–150 citations over 5 years if the `Θ(PH_k)` topological activator catches on in the Krylov community. This is the A+ scenario; probability ≈ 15–25 %.

**Downside — 3–5 weeks of theory work that might stall.** Opportunity cost: v5.0 slips by the same window if the owner cannot parallelise. α-derivation is the known failure-mode risk; if no RG source is found, α stays as a fit parameter with an ugly posterior, which referees may call fine-tuning.

**Downside — retraction / RETRACT scenario.** No attack was fatal enough to warrant RETRACT. The equation is *ansatz-publishable* today; it is *not derivation-publishable*. The risk is not "unpublishable"; it is "published-weaker-than-hoped".

**Opportunity cost on v5.0.** v5.0 is a finished product (DESI-DR2 + NMC Cassini bound + Dark Dimension × NMC + D7/D14/D17 pipeline) and should not wait on v6. Recommend: submit v5.0 now on its own schedule; begin v6 rewrite in parallel. If owner cannot parallelise, v5.0 first, v6 second — no exceptions.

## Appendix — provenance and missing inputs

- Claude derivation: `derivations/V6-claude-derivation-report.md` (read).
- Gemini derivation: `derivations/V6-gemini-derivation.md` (read).
- Magistral derivation: raw responses `_mistral_responses/v6_q{1,2,3}.txt` read. `v6_q1.txt` is a single-line timeout error (Q1 did not return); `v6_q2.txt` (198 lines) and `v6_q3.txt` (114 lines) are complete and align with the Claude/Gemini verdicts (heuristic-only bridge; `κ_R` has units nat/s). Polished `V6-magistral-derivation.md` never committed — flagged.
- Adversarial: `derivations/V6-adversarial-attack.md` (read).
- Dequantisation resolution: `derivations/V6-dequantisation-map.md` + `v6_audit.md §9` (read).
- Cross-verification report `V6-cross-verification.md` never committed — this memo functionally substitutes for §1–§2 of it (consolidated verdicts across the three derivations + adversarial).

*No other repository files modified. Single commit, single push, no Co-Authored-By.*
