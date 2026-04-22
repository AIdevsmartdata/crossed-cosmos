# v6 — JHEP formal-track companion (draft skeleton)

**Status:** `v6:draft:skeleton` — 2026-04-22.
Companion to v5.0 (EPJ C phenomenological track). v6 targets JHEP.

## Title candidates (owner to choose one)

1. An information-theoretic upper bound on observer-dependent entropy growth in
   type-II algebras.
2. Modular-time refinement of the generalised second law: a dequantisation
   bridge.
3. From Faulkner--Speranza to a complexity-bounded GSL in crossed-product
   algebras. **(current tentative default, set in `\title{}`)**

## Files

- `v6_jhep.tex` — §1--§7 + Appendix A skeleton, compiles clean
  (4 pages, RevTeX 4-2 fallback class).
- `v6_jhep.pdf` — latest compile.

## Class status

`jheppub.cls` is **not** available on this build host; SISSA download link
`https://jhep.sissa.it/jhep/help/JHEP/TeXclass/JHEP3.zip` returned HTTP 404 on
2026-04-22. The skeleton compiles against `revtex4-2` (PRD-style) as a
fallback. Swap to `jheppub` before submission; the class change is a
one-line edit of `\documentclass{...}` and a move of `\author/\affiliation`
macros to the JHEP forms. No structural changes.

## Rules applied

- **V6-1.** Main result is an inequality, boxed as Eq.~(1).
- **V6-2.** Assumptions M1, M2, M3 explicitly labelled with
  POSTULATE / ANSATZ / CONJECTURAL tags and anchored in the literature.
- **V6-3.** No "arrow of time" rhetoric; §7 explicitly declines to explain
  the cosmological arrow.
- **V6-4.** No cosmological prediction; no falsifier table; §7 defers to the
  v5.0 companion.

## Section word counts (skeleton, approximate)

| §   | Section                                   | Words |
|-----|-------------------------------------------|-------|
| 1   | Introduction                              | ~260  |
| 2   | Setup                                     | ~220  |
| 3   | Main inequality                           | ~430  |
| 4   | Dequantisation map                        | ~200  |
| 5   | Relation to existing GSL statements       | ~200  |
| 6   | Explicit assumptions summary              | ~110  |
| 7   | Conclusion                                | ~190  |
| App A | Computational realisation               | ~130  |

All seven sections are below the ≤200-word prose-cap directive only for
§3 and §1 (which the outline explicitly permits to be longer). Subsequent
drafting agents will expand §3 and §4 after the formal checks.

## Bibliography

- Reuses `../eci.bib` via `\bibliography{../eci}`. **Not** duplicated.
- Currently cited keys (all present in `eci.bib`): CLPW2023, DEHK2025a,
  DEHK2025b, FaulknerSperanza2024, Kirklin2025, MaHuang2025, Haferkamp2022,
  CryptoCensorship, Yip2024, Jacobson1995, KhouryWeltman2004.
- **Missing keys required for full referencing** (to be added by the
  bib-consolidation agent; see `_internal_rag/v6_audit.md §5`):
    - Wall 2011 (`1105.3445`)
    - Eling--Guedens--Jacobson 2006 (`gr-qc/0602001`)
    - Fan 2022 (`JHEP 08 232`) --- currently one claim routes through
      `\cite{Kirklin2025}` as a placeholder; fix once `Fan2022` added.
    - Brown--Susskind 2018 (`1701.01107`)
    - Caputa--Mag\'an--Patramanis--Tonni 2024 (`2306.14732`)
    - Connes--Rovelli 1994 (`CQG 11 2899`)
    - Witten 2023
    - Jacobson 2016 (`1505.04753`)
    - Barrow 2020 (`PLB 808 135643`)
    - Pedraza et al.\ 2022 / Carrasco et al.\ 2023
    - Bianconi 2025 (`2408.14391`)
    - Schuster--Haferkamp--Huang 2025 / Ma--Huang STOC (if not subsumed in
      `MaHuang2025`).
- One inline temporary prose note in §5 L4 labels the EGJ 2006 citation as
  pending; remove once `EGJ2006` key is added.

## What the next two agents need to complete before §3 is reviewer-ready

1. **bib-consolidation agent.** Add the 12 missing keys above to
   `eci.bib`, verify arXiv IDs against the wet-floor-signs list (rule #10
   in `_internal_rag/PRINCIPLES.md`), and swap in the corrected
   `\cite{}` calls in §3, §4, §5. Run `bib_audit.md` after.
2. **sympy-formal-check agent.** Expand the proof sketch of
   Theorem~1: (a) explicit type-II spectral decomposition of the RHS in
   Faulkner--Speranza; (b) operator-growth bound under M1 with a clear
   statement of \emph{what} the non-negative correction is; (c) a
   worked miniature of the $\Theta\to 1$ limit showing numerical
   recovery of the Wall bound within $<1\%$ on the toy
   \texttt{V6-dequantisation-map.py} factor. Log results in
   `derivations/V6-formal-check.md`.

Only after those two passes can §3 be handed to the external adversarial
reviewer.

## Compile

```sh
cd paper/v6
latexmk -pdf v6_jhep.tex
```

Clean compile, no bib warnings for the 11 keys used; undefined reference
to `EGJ2006` is explicitly avoided (handled as prose).
