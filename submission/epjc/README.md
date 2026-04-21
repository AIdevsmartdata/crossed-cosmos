# EPJ C Submission Dossier — ECI v4

Target: **European Physical Journal C** (Springer, SCOAP3 open access, IF 4.3).
Manuscript: `paper/eci.tex` (currently RevTeX 4-2, `aps,prd`).

## (a) Adapt `eci.tex` to svjour3

Replace preamble:

```latex
\documentclass[epj,twocolumn]{svjour3}
\usepackage{graphicx,hyperref,physics,xcolor}
\usepackage[utf8]{inputenc}
\usepackage[T1]{fontenc}
\smartqed
```

Main adaptations (not 1-click — do by hand, use `eci_svjour3_skeleton.tex` as scaffold):

1. **Author block**: RevTeX `\author{...}\affiliation{...}\email{...}` → svjour3
   `\author{Kevin Remondi\`ere\thanks{\email{kevin.remondiere@gmail.com}}}`
   followed by `\institute{Independent Researcher \at ORCID 0009-0008-2443-7166}`.
2. **`\thanks{}`**: RevTeX free-floating `\thanks` → move inside `\title[short]{...}\thanks{...}` or first author footnote.
3. **Abstract**: svjour3 uses `\abstract{...}` **before** `\maketitle` (not `\begin{abstract}...\end{abstract}` after title as in RevTeX).
4. **Keywords**: add `\keywords{dark energy \and non-minimal coupling \and von Neumann algebras \and early dark energy \and persistent homology}` before `\maketitle`.
5. **PACS/MSC (optional)**: `\PACS{98.80.-k \and 04.62.+v}`.
6. **Bibliography**: RevTeX `apsrev4-2.bst` → Springer `spphys.bst` (physics) or `spmpsci.bst` (math/phys). Run:
   `\bibliographystyle{spphys}\bibliography{eci}`.
   Some `@article` entries may need a `doi =` field — `spphys` prints DOIs.
7. **Equations, sections, labels**: unchanged.
8. **Figures**: svjour3 prefers `\begin{figure}...\end{figure}` with `\caption` *below* `\includegraphics`; already compatible.
9. **`\maketitle`**: keep; svjour3 honours it.

Compile test: `latexmk -pdf eci_svjour3.tex` with `svjour3.cls` + `spphys.bst` from the EPJ template bundle (`https://www.springernature.com/gp/authors/campaigns/latex-author-support`).

## (b) Cover letter

See `cover_letter.tex`. Compile standalone (`\documentclass{article}`) → PDF upload at submission step "Cover Letter".

## (c) Suggested referees

See `suggested_referees.md` — 5 names with rationale tied to `eci.bib` entries.

## (d) Submission URL

<https://www.editorialmanager.com/epjc/>

Steps:
1. Register / log in (ORCID SSO supported).
2. "Submit New Manuscript" → Article Type: **Regular Article — Theoretical Physics**.
3. Section/Category: **Astroparticle Physics and Cosmology**.
4. Upload: main PDF, `eci.tex` source + `eci.bib` + figures (zipped), cover letter PDF.
5. Suggested / opposed reviewers: paste from `suggested_referees.md`.
6. Funding: none (independent researcher). SCOAP3 open-access fee waived for theoretical HEP papers covered by the SCOAP3 consortium — confirm eligibility on the submission form.

## (e) Expected turnaround

EPJ C typical timeline (2024–2026 data):
- Editor assignment: 1–2 weeks
- First referee report: **6–12 weeks**
- First decision: **2–4 months**
- If accepted with minor revision: ~1 additional month to production.
- SCOAP3 publication: open access, no APC for the author.
