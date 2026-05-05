# Revision Notes: proposal_outline.md (v7.4) -> proposal_outline_v75.md

**Date:** 2026-05-05 night
**Author:** Sonnet sub-agent A66 (parent persisted)
**Hallu count entering / leaving:** 85 / 85 (held)
**Mistral large-latest:** STRICT-BANNED throughout
**Source draft:** `proposal_outline.md` (2026-05-03, 520 words, hallu count 77)
**Revised draft:** `proposal_outline_v75.md` (2026-05-05 night, ~1450 words, hallu count 85)

---

## Why this revision was needed

The original draft was written before Wave 11 (A56, A58, A60, A62, A48-A63, A65) and made claims now invalidated or weakened by sub-agent results from the night of 2026-05-05. Templeton OFI review demands the honest version; this revision implements the corrections required by the v7.5 epistemic state.

---

## Top changes (line-by-line by section)

### 1. Executive Summary
**Was**: "move from curve-fitting frameworks to first-principles parameter-free prediction" — implies a strong claim of derivation power from CM-anchoring.
**Now**: "consistency scaffold ... rigid enough to yield falsifiable downstream predictions" + explicit acknowledgement of A62 null test (315 vs 285±17 random hits, 1.7σ). Cite: A62 SUMMARY.md.

### 2. Background §1 (Problem)
**Was**: "CM-anchoring provides 1-2 additional structural constraints, reducing the lepton-sector DOF from ~6 to ~4, converting previously free-fitted observables into genuine predictions" — too strong post-A62.
**Now**: "the H7' Damerell ladder is well-posed; ... but its selection power on CKM observables is null (A62)" — honest demotion. The ladder remains mathematically rigorous (Hurwitz/Chowla-Selberg/Damerell), but the *selection* claim is retracted.

### 3. Background §2 (CM Anchor)
**Was**: "θ_13 Cabibbo angle from micro-locality bounds (H7-A Damerell ladder prediction)" — promotes A17 |V_us|=9/40 to "prediction".
**Now**: removed θ_13 prediction line; replaced with "(b) the lepton sector at τ in the τ_S=i vicinity (Im(τ)≈1.007 per A48 dMVP26 down-sector breaking — strict τ=i fails at y_d/y_s with 4500× suppression)". Cite: A48 SUMMARY.md.

### 4. Background §2 — τ=i strict pinning DROPPED
**Was**: "p→e⁺π⁰ proton decay B-ratio (first-principles, no fit)" presented at strict τ=i.
**Now**: phrasing "at τ in τ_S=i vicinity" everywhere strict τ=i would have appeared in a quark/down-sector context. Up-sector survives strict τ=i (<5% shift); down sector y_d/y_s drops 4500×; cite A48 + A63 fix. The proton-decay B-ratio (lepton-sector dominated) is preserved.

### 5. Background §2 — "two independent chains" RETRACTED
**Was**: implicit claim of two independent analytical derivations (P-NT Galois descent + BC×CM).
**Now**: "Three jointly H6-co-dependent witnesses (Galois descent + BC×CM at β=2π + KW dS-trap) provide *necessary-but-not-sufficient* mutual consistency for τ=i (A60); we do **not** claim two independent analytical chains." Cite: A60 SUMMARY.md.

### 6. Month 24 Deliverable — Wolf comparison REFRAMED
**Was**: "establishing ECI as foundationally incompatible with Wolf 2025 high-ξ claims" — reads as refutation.
**Now**: "Cassini-clean cosmology defensive result: ECI ξ≈0.001 is the only KG-physical regime; Wolf 2025 ξ=2.31 is CPL-effective only (A56), strengthening — not refuting — ECI's structural position." This matches A56's empirical ξ_crit_+≈+0.20 boundary finding (Wolf's ξ=2.31 is structurally infeasible for KG dynamics; must be interpreted as CPL effective). Cite: A56 SUMMARY.md.

### 7. NEW: Seven Falsifiers Table
Added explicit table of 7 falsifiers (NA62, KamLAND-Zen, JUNO, DUNE, CMB-S4, Belle II/LHCb-U2, Hyper-K) with year and "status if violated" column. The 11/210 NA62 first-row unitarity entry is explicitly labeled "consistency hint, not a derivation" per A62. The 6α₁²/(5π) Belle II entry is "consistency hit, *not* promoted to prediction" per A62 recommendation.

### 8. NEW: Eleven Formal Axioms section (replaces vague "rescue paths")
**Was**: brief "3 H7 rescue paths (H7-A primary, H7-B BDP, H7-C Rankin-Selberg)".
**Now**: full 11-axiom Lakatos table from A65, with explicit ESTABLISHED / WORKING-CONFIRMED / POSTULATE / CONJECTURED tags and arXiv provenance for each. Cite: A65 SUMMARY.md.

### 9. v7.5 Amendment status — UPDATED
**Was**: "v7.4 amendment (drafting now)" listed as Month 24 deliverable.
**Now**: v7.5 amendment **compiled** (15 pp PDF, `v75_amendment.tex`, 1454 lines, 2026-05-05 night) — listed as already-existing artifact. Includes A46 LYD20 retraction (99,061× χ² penalty) explicitly mentioned, since reviewers will want to see negative-result discipline.

### 10. Hallu count + Zenodo DOI updated
- 77 → **85** (8 new catches in Wave 9-11, including A52 BuntingNicolini→BanerjeeNiedermaier authorship fix, A34 Cardy 78→81, A37 v7.4 bibitem, A36 Mistral Babu-Mohapatra fabrication, A52 second pass through eci.tex line 675).
- Zenodo v6.0.53.1 → **v6.0.53.3 = `10.5281/zenodo.20036808`** (per MEMORY.md current state).
- Concept DOI unchanged: `10.5281/zenodo.19686398`.

### 11. 9 papers status + v7.5 amendment
**Was**: "8 papers" or sometimes "9 papers" inconsistent.
**Now**: "9 submission-ready papers (P-NT BLMS, v7.4 LMP, ER=EPR LMP, Modular Shadow LMP, Cardy LMP, BEC, P-KS, P-DSSYK, AWCH BIX) + v7.5 amendment compiled" — matches MEMORY.md current state.

### 12. Risk Mitigation section — HONEST
**Was**: "If H7 Damerell-CS refuted (≤15% chance): H7-A, H7-B, H7-C rescue paths all preserve 4.5.b.a anchor. Portfolio remains 85% viable."
**Now**: Three concrete branches:
- "If Hyper-K B-ratio differs >1σ from 2.06: G1.12.B falsified; H11' demoted; ~50% portfolio remains."
- "If Damerell ladder fails further consistency tests: A62 null already documents weak selection power; portfolio reframes as pure consistency scaffold."
- "If KW dS-trap (H9') is refuted: triple-witness heuristic collapses; CM-anchor narrative weakens but P-NT theorem-content unaffected."

No phantom probabilities ("≤15% chance") — these were unfounded.

### 13. Title change
**Was**: "Bridging Mathematical Structures and Fundamental Physics".
**Now**: "Number-Theoretic Consistency Scaffolds for Particle Physics and Cosmology" — matches the honest framing (consistency, not derivation).

### 14. Word count adjustment
**Was**: ~520 words.
**Now**: ~1450 words (matches mission spec "target ~1500 words / 1 page A4 packed").

---

## What was KEPT from v7.4 draft

- Hyper-K B(p→e⁺π⁰)/B(p→K⁺ν̄) = 2.06 ± 0.15 — the strongest surviving claim, kept as primary falsification gate.
- LMFDB 4.5.b.a 4-path verification — solid; retained.
- Independent researcher framing (no institutional host).
- Audit trail (GitHub + Zenodo + Mistral STRICT-BAN).
- Reference letter targets (Marcolli, Schäfer-Nameki, Booker) — unchanged.
- Budget breakdown structure (postdoc + compute + travel + author time + publication) — unchanged in totals; minor adjustments to compute justification per A56-revised (separate CPL emulator for Wolf comparison, not extension of KG emulator).

---

## What was REMOVED

- The phrase "first-principles parameter-free prediction" (oversells post-A62).
- The phrase "two independent analytical chains" (refuted by A60).
- The strict-τ=i pinning for quark sector (refuted by A48 down-sector breaking).
- The "Wolf foundationally incompatible" framing (A56 reframes as defensive strengthening).
- The "≤15% chance H7 refuted" phantom probability.

---

## New hallu catches (none from this revision pass)

This revision did not consult any external sources beyond the 8 SUMMARY.md files already in the repo (A48, A56, A58, A60, A62, A65, V75_DRAFT_NOTES, README of H7_TEMPLETON_DRAFT) and the v7.5 amendment LaTeX header. All claims trace to those internal documents which themselves carry verified provenance per A65 (all 11 axioms have arXiv-verifiable provenance). **Hallu ledger 85 → 85 (held).**

---

## Confidence assessment for Templeton submission

The revised draft is **honest enough for Templeton review**. Specifically:
1. No claim of derivation that A62 contradicts.
2. No strict-τ=i pinning where A48 shows breaking.
3. No "two independent chains" where A60 shows H6-co-dependence.
4. No "Wolf refutation" framing where A56 actually shows structural strengthening.
5. All 11 axioms are tagged with explicit Lakatos status; reviewer can verify each provenance.
6. Negative results (A62 null, A46 LYD20 retraction, A48 down-sector breaking) are stated openly, not buried.

The remaining tension is that the proposal still asks for $234.8K — Templeton reviewers will assess whether the *consistency-scaffold* framing (weaker than the original "derivation engine" framing) is fundable as "Big Questions". The Hyper-K B-ratio = 2.06 ± 0.15 prediction (G1.12.B M1-M5 PASS, M6 in progress) remains the load-bearing falsifiable claim.

**Verdict:** READY for Kévin review and edit. Recommend: keep this v7.5 draft as the primary submission; archive the v7.4 draft as `proposal_outline_v74_superseded.md` for the audit trail.

---

## File map

- `proposal_outline.md` (v7.4, original, 520 words) — KEEP unchanged for audit trail.
- `proposal_outline_v75.md` (v7.5, NEW, ~1450 words) — PRIMARY submission candidate.
- `REVISION_NOTES_v75.md` (this file) — changelog with full citations.
- `submission_protocol.md` (v7.4) — minor updates needed (P-NT timeline still valid; v7.4 amendment line should be updated to v7.5 amendment compiled).
- `reference_letter_targets.md` (v7.4) — unchanged; outreach plan still valid.

---

*Prepared by H7/A66 sub-agent 2026-05-05 night, post Wave 11 completion.*
*All claims trace to: A48, A56, A58, A60, A62, A65 SUMMARY.md + V75_DRAFT_NOTES.md + v75_amendment.tex header.*
