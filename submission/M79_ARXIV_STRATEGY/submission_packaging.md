---
name: M79 arXiv submission packaging workflow
description: tar.gz archive structure, portal walkthrough, endorser code workflow.
type: project
---

# M79 — arXiv Submission Packaging (2026-05-06)

---

## 1. Per-paper tar.gz archive structure

Each paper should produce a single .tar.gz:

  <paper_id>/
    <main>.tex          (UTF-8, no absolute paths)
    <main>.bbl          (pre-built bibliography)
    figures/            (EPS or PDF figures only; no PNG/JPG unless essential)
    README              (optional; 2-3 lines: title, author, date)

Build command (from paper directory):
  pdflatex <main>.tex && pdflatex <main>.tex && pdflatex <main>.tex
  bibtex <main>  (if using .bib; else .bbl already present)
  pdflatex <main>.tex && pdflatex <main>.tex
  # verify no "undefined reference" or "undefined citation" warnings
  tar czf <paper_id>_arxiv.tar.gz <main>.tex <main>.bbl figures/ README

NO .pdf, .aux, .log, .out, .synctex.gz in the archive.

Per-paper archive map:
  P5  leptogenesis_csd_LMP.tar.gz      -> submission/lmp_leptogenesis_csd1sqrt6/
  P6  cassini_palatini_prd.tar.gz      -> submission/prd_cassini_palatini/
  P1  paper_lmfdb_s4prime.tar.gz       -> notes/eci_v7_aspiration/PNT/
  P2  erepr_araki_LMP.tar.gz           -> notes/eci_v7_aspiration/EREPR_REOPEN/
  P4  cardy_rho_LMP.tar.gz             -> notes/eci_v7_aspiration/CARDY_PAPER/
  P3  modular_shadow_v25.tar.gz        -> notes/eci_v7_aspiration/MODULAR_SHADOW/
  P7  proton_decay_prd.tar.gz          -> notes/eci_v7_aspiration/OPUS_G112B_M6/
  R-2 r2_blochkato.tar.gz             -> notes/eci_v7_aspiration/M70_R2_PAPER/
  R3  r3c1_short_note.tar.gz          -> notes/eci_v7_aspiration/M71_R3C1_PAPER/
  M45 bianchi_ix_ms.tar.gz            -> notes/eci_v7_aspiration/M45_BIANCHI_IX_PAPER/
  R-6 lemniscate_note.tar.gz          -> notes/eci_v7_aspiration/R6_LEMNISCATE_NOTE/

---

## 2. arXiv submission portal walkthrough (arxiv.org/submit)

Step 1: Login / account
  arxiv.org -> Log In (or register if first time)
  If first submission: you will be asked to supply an endorser code (see Section 3).

Step 2: Start submission
  "Submit" -> "Start New Submission"
  Select primary archive + category (e.g., hep-ph, gr-qc, math.NT).

Step 3: Upload files
  Upload .tar.gz archive. arXiv auto-compiles with pdflatex.
  If compilation fails: check for missing packages, encoding issues, \input paths.

Step 4: Metadata form
  Title: exact match to \title{} in .tex
  Authors: "K. Remond\`{i}ere" — use consistent UTF-8 form or LaTeX accent macros
  Abstract: paste from .tex \begin{abstract}...\end{abstract} (plain text, no LaTeX)
  Comments: "X pages, Y figures; submitted to <Journal>"
  MSC / ACM codes: fill for math papers (e.g., 11F67, 11G40 for math.NT)
  Journal-ref: leave blank until accepted

Step 5: Category selection
  Primary: as planned (hep-ph, gr-qc, math.NT, hep-th, cond-mat.stat-mech, math-ph)
  Cross-list: e.g., math-ph for Bianchi IX (primary math-ph, cross gr-qc)
  DO NOT cross-list excessively: 1-2 categories maximum.

Step 6: Review + submit
  Preview PDF carefully (check title page, references, figures).
  Confirm author name consistency with all prior papers ("K. Remondiere").
  Submit. Confirmation email with arXiv ID arrives within 1 business day.

---

## 3. Endorser code request workflow (first arXiv submission)

arXiv requires endorsement for first submissions in most categories.

Process:
  a) Contact endorser via email (see endorser_emails.md).
  b) Endorser logs into arXiv -> "Endorse a Submitter" -> enters your email.
  c) You receive an email with endorsement code (6-character alphanumeric).
  d) During submission Step 2, enter code when prompted.

Notes:
  - One endorser per category; same person can endorse multiple papers in same category.
  - If endorser is unavailable: arXiv has a "find an endorser" tool at
    arxiv.org/auth/endorse — search for active submitters in target category.
  - Endorsement is permanent: once endorsed in hep-ph, future hep-ph submissions
    need no additional endorser (codes are category-specific).

Category-by-category first-submission priority:
  hep-ph first: P5 (King endorsement) -> unlocks P7, M58
  gr-qc first: P6 (Sotiriou) -> one-time
  math.NT first: P1 (Booker) -> unlocks R-2, R-6, #9
  hep-th first: P2 (Lashkari) -> unlocks P3
  cond-mat first: P4 (Calabrese) -> one-time
  math-ph: Bianchi IX (Marcolli, gated W3)

Hallu 91 held. 0 fabrications.
