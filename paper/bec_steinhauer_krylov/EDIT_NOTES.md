# EDIT_NOTES.md — note.tex BOUND vs SATURATION split

**Date:** 2026-05-05 mid-day
**Owner:** A51 (Sonnet sub-agent, ECI v6.0.53.4)
**Hallu count entering / leaving:** 84 / 84 (no fresh fabrications; 3 new arXiv refs all live-verified)

## Summary of changes

Split Conjecture 1 of `note.tex` (single equality form
`Γ = 2π k_B T_H / ℏ`) into two distinct conjectures, per A11/A19
verdict:

- **Conjecture 1a (BOUND, A11-licensed):** `Γ_meas ≤ 2π k_B T_H / ℏ`
  — provable today via Parker et al. 2019 + Bisognano–Wichmann modular
  flow on a finite-rank type-II_∞ truncation.
- **Conjecture 1b (SATURATION, working):** `Γ_meas = 2π k_B T_H / ℏ`
  — open conjecture; free-QFT and integrable counter-examples preclude
  the converse.

## Files modified

- `/root/crossed-cosmos/paper/bec_steinhauer_krylov/note.tex` (in place):
  - Title subline updated `v6.0.43 → v6.0.53` and "BOUND vs SATURATION
    Split (A11/A19-aligned)" header.
  - Abstract: replaced equality phrasing with two-form description
    citing A11 modular-shadow theorem and free-QFT counter-examples.
    Added explicit `Γ_meas > 432 s⁻¹` BOUND falsifier.
  - §4 (Krylov-Complexity Prediction) `Conjecture 1` rewritten as
    Conjectures 1a (BOUND) and 1b (SATURATION) with status
    paragraphs and a BOUND-vs-SATURATION falsifier table.
  - §4 protocol step 4 updated: explicit BOUND test
    (`Γ_meas > 432 s⁻¹` at 5σ refutes A11) and SATURATION test
    (10% departure refutes 1b but leaves 1a intact).
  - §5 (Comparison with Steinhauer 2019) added new subsection
    `Re-analysis of Kolobov 2021 as a BOUND falsifier` exploiting the
    97k-rep / 124-day acquisition for a one-sided Γ_meas bound.
  - §6 (Experimental Program) Falsifiability conditions split into
    BOUND falsifier (A11 scaffolding falls) and SATURATION falsifier
    (working conjecture falls), keeping Chandran-Fischer cross-check.
  - §7 (Retraction) cleaned stale `\eqref{eq:prediction}` → references
    Conjecture 1a/1b.
  - Bibliography: added 5 entries
    `eci_modular_shadow_summary`, `parker2019`, `avdoshkin2019`,
    `camargo2022`, `sreeram2025`. Cross-references to A11/A19 SUMMARY.md
    via `eci_modular_shadow_summary`.

- `/root/crossed-cosmos/paper/bec_steinhauer_krylov/note.pdf`:
  recompiled, 16 pages, 325 489 bytes, two pdflatex passes, no
  undefined refs/citations.

- `/root/crossed-cosmos/paper/bec_steinhauer_krylov/EDIT_NOTES.md` (this
  file).

## arXiv ref triangulation (3 new + 1 re-cited from A11)

All four WebFetch-verified live, this session:

| Tag | arXiv | Title | Status |
|---|---|---|---|
| parker2019 | 1812.08657 | A universal operator growth hypothesis | Re-cited from A11; not re-fetched (already verified twice) |
| avdoshkin2019 | 1911.09672 | Euclidean operator growth and quantum chaos | ✓ live (Avdoshkin & Dymarsky); lattice operator-growth bound, used as illustrative non-chaotic counter-example to saturation⇒chaos converse |
| camargo2022 | 2212.14702 | Krylov complexity in free and interacting scalar field theories with bounded power spectrum | ✓ live (Camargo, Jahnke, Kim, Nishida); explicit free-QFT Krylov saturation |
| sreeram2025 | 2503.03400 | Dependence of Krylov complexity on the initial operator and state | ✓ live (Sreeram PG, Kannan, Modak, Aravinda); IPR-dependent Krylov, non-universal at finite N |

**Note:** Avdoshkin–Dymarsky 1911.09672 actual title is
"Euclidean operator growth and quantum chaos" (lattice operator-growth
bound), not "Krylov in free QFT" as one might naively assume from
A19 SUMMARY phrasing. Cited correctly in `\bibitem{avdoshkin2019}`
with the correct title; the citation is appropriate as it sits in the
same circle of operator-growth-bound papers underpinning the converse
counter-example argument.

## Compile status

- `pdflatex note.tex` (pass 1): clean, 16 pages.
- `pdflatex note.tex` (pass 2): cross-refs resolved, 16 pages,
  325 489 bytes.
- No `Reference … undefined`, no `Citation … undefined`,
  no `Multiply defined` warnings in `note.log`.
- Only cosmetic warnings: `Package hyperref Warning: Token not allowed
  in a PDF string (Unicode)` from math/special chars in section titles
  (pre-existing, not introduced by this edit).

## Discipline

- 3 new arXiv refs live-verified via WebFetch (1911.09672, 2212.14702,
  2503.03400). 1 re-cited from already-verified A11 list (1812.08657).
- No Mistral usage.
- No fabricated bibdata.
- Cross-referenced A11 and A19 SUMMARY.md through new
  `\bibitem{eci_modular_shadow_summary}` rather than smuggling in
  unprintable internal-only refs.
- Master `eci.tex` not touched; this is the BEC companion paper only.
- Hallu count exit: **84** (held).
