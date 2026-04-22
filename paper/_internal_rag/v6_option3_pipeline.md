# v6 option-3 pipeline — ambitious refounded document

**Date.** 2026-04-22.
**Trigger.** Owner requested option-3 refounded v2 of Claude-app "loi ECI
finale" document, with "tous calculs vérifiés sympy+numpy d'abord,
citations Crossref vérifiées une par une, et respect strict V6-1".

**Enforcement.** `derivations/V6-claims-audit-pipeline.py` — MUST pass
(exit 0) before any new text enters `paper/v6/` or any companion .tex.

## Hard gates (exit non-zero on fail)

### Numerical
- ω_P = 1.854859×10⁴³ rad/s (within 0.1%)
- T_Planck = 1.4168×10³² K (within 0.1%)
- **2π k_B T_P/ℏ = 2π · ω_P, NOT ω_P** (documented false in Claude-app doc)
- H_0(67.4 km/s/Mpc) = 2.184×10⁻¹⁸ s⁻¹ (within 0.1%)
- T_dS(67.4) = 2.655×10⁻³⁰ K
- **Λ/M_P⁴ ≠ (H_0/ω_P)² exactly** — differ by ~1 dex; any "exact" claim is
  rejected
- **S_BH(5.1×10¹⁴ g) = 6.9×10³⁹, NOT 10²⁵** — 15 orders off from
  Claude-app doc
- With correct S_BH, burst "extension factor" S⁻⁰·⁰⁵ · ln S = 0.93,
  **not 3** — flagship prediction numerically fails

### Citation
- All mandatory anchors (v6.1 HEAD a09bbce) present in `eci.bib`:
  Haferkamp2022, CLPW2023, FaulknerSperanza2024, Jacobson1995, Wall2011,
  BrownSusskind2018, ConnesRovelli1994, KhouryWeltman2004
- **Lange2021 (PRL 126 011102) red-flag**: real value 1.0(1.1)×10⁻¹⁸/yr,
  NOT -8.0±3.6×10⁻¹⁸/yr. Any doc citing Lange must quote correct value.
- Wishlist (warn): Jacobson2016 arXiv:1505.04753, CaputaMagan2024
  arXiv:2205.05688, GibbonsHawking1977 PRD 15 2738. Add verified entries
  before citing.

### Theoretical status (V6-1, rule 12)
Every load-bearing claim in the draft must carry one tag:
THEOREM / POSTULATE / ANSATZ / HEURISTIC / MOTIVATION. The pipeline
grep-rejects:
- Equality form of main inequality (V6-1)
- "PBH burst ×3" patterns (V6-4)
- "LISA Ω_gw h²" without D18-equivalent tag (V6-4)
- "-8.0 ± 3.6 × 10⁻¹⁸/yr" Lange value (rule 1)
- "Λ/M_P⁴ = (H_0/ω_P)²" exact-identity claim (rule 12)
- "aucune publication entre YYYY et YYYY" sweep (rule 16)

### Falsifier (V6-4)
- No cosmological falsifier proposed in v6 without a D18-equivalent
  artefact (Fisher forecast + nuisance marginalisation + cross-model
  verdict). Registry currently empty. D18 killed fσ_8 × Θ(PH_2); any
  new entry requires a new `derivations/D19+` commit.

## Soft gates (warn-only)

- Negative-literature claims require a specific scope.
- Einstein-analogy framings are MOTIVATION, not THEOREM.
- Any promotion of a quantity to "fundamental constant" is PROGRAMMATIC,
  not metrological, for the next decade.

## How to use

1. Write the proposed section of the new document as a .tex fragment at
   `paper/v6/v6_option3_draft.tex`.
2. Run `python3 derivations/V6-claims-audit-pipeline.py`.
3. If exit 0 → safe to integrate. If exit 1 → fix, rerun.
4. Before any git-tag, pipeline must pass + `latexmk` must compile with 0
   undef refs/cites + cross-model adversarial verdict must be SHIP or
   MINOR-FIX.

## Option-3 document scope (draft)

The refounded document, when written, must:

- Preserve v6.1 Eq.(1) as **inequality** (V6-1).
- Keep Prop. 1 (logistic envelope, Prop:logistic) as tightened bound
  under explicit Brown-Susskind + Haferkamp postulate.
- Add a §6 "programmatic outlook" that:
  - Frames the entropy/complexity equivalence as a **conceptual motivation**
    (MOTIVATION tag), explicitly NOT a theorem of B5.
  - Discusses κ_R = 2π k_B T_R/ℏ as an observer-dependent modular
    conductance, with correct 2π factor; mentions ω_P and H_0 as the
    two extremal values *without* claiming κ is a CODATA-candidate.
  - Discusses Λ/M_P⁴ ~ (H_0/ω_P)² as an order-of-magnitude coincidence,
    explicitly *not* an exact identity (softening on the dex-level gap).
- Add a new §7 "comparative context" covering Verlinde 2017, Rovelli
  relational QM, LQG, strings — material from Claude-app doc.
- **Optionally** open a future companion paper (v7) for phenomenology,
  requiring D19+ pipeline artefacts for each falsifier.

## What the refounded document must NOT contain

- Main equation as equality (V6-1).
- PBH burst ×3, LISA plateau, α̇/α ~ H_0 as v6-level falsifiers.
- Claim of "5th fundamental constant" with CODATA implication.
- Claim of "theorem" for any of A1-A6 derived from B5.
- "2π k_B T_P/ℏ = ω_P" identity.
- "S_BH = 10²⁵" or any derived Δt/τ = 3.
- "Λ/M_P⁴ = (H_0/ω_P)² exactly".
- Lange 2021 value -8.0 ± 3.6 × 10⁻¹⁸/yr.
- "Aucune publication entre 2015 et 2026" sweep.
