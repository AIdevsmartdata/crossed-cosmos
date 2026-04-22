# V6 Adversarial v3 — pre-arXiv final sweep

Date: 2026-04-22
Target: `paper/v6/v6_jhep.tex` @ commit 57726d1 (7 pages, RevTeX 4-2)
Reviewer: hostile JHEP referee simulation
Pipeline: `derivations/V6-claims-audit-pipeline.py` = 18/18 PASS (pre- and post-fix)
Build: `latexmk -pdf` → 7 pages, 0 undefined refs, 0 errors (only cosmetic
hyperref Unicode-token warnings for accented names in cite keys, harmless)
TODO/FIXME/XXX/BUG/HACK grep: EMPTY

## Section-by-section verdict

| § | Topic | Verdict |
|---|---|---|
| Abstract | Statement of bound + logistic envelope + dequant | SHIP |
| §1 Intro | Positioning vs CLPW/DEHK/Faulkner--Speranza | SHIP |
| §2 Setup | TikZ diagram, $\kappa_R=2\pi T_R$, M1' spread-complexity | SHIP |
| §3 Main | Eq.(1), M1/M2/M3, Thm 1, Lemma 1 submult | MINOR-FIX (cite bug) |
| §4 Dequant | Def 1, sympy checks, CPTP | SHIP |
| §5 Relation | 4-way limits, Prop 1 logistic, comparative table | MINOR-FIX (orphan "bib-consolidation agent" note) |
| §6 Assumptions | M1/M2/M3 summary table | MINOR-FIX (internal "v5.0" tag) |
| §7 Outlook | MOTIVATION-tagged Einstein analogy, κ UV/IR, Λ/M_P⁴ coincidence | SHIP |
| §8 Conclusion | "no cosmological claim" honesty gate | MINOR-FIX (internal "v5.0" tag) |

## Referee-flaggable issues found

1. **[CITATION BUG, §3 L285]** `Fan~(2022)~\cite{Kirklin2025}`: wrong bib key
   — points to Kirklin2025 but the sentence is about Fan 2022.
   `Fan2022` key DOES exist in `eci.bib` line 634. Classic copy-paste flag
   that a referee would immediately catch.
   **FIX APPLIED**: `\cite{Kirklin2025}` → `\cite{Fan2022}`.

2. **[ORPHAN INTERNAL NOTE, §5 L450]** Parenthetical
   "Eling--Guedens--Jacobson 2006; bib key to be added by the
   bib-consolidation agent" — this is internal tooling language that
   must not ship. Referee would flag as "unprofessional" or "incomplete".
   **FIX APPLIED**: stripped to "(Eling--Guedens--Jacobson 2006)".
   (Adding the actual EGJ 2006 bib entry is deferred; citation via author
   names only is acceptable at this stage since Jacobson1995 already
   anchors the programme.)

3. **[INTERNAL VERSIONING, 4 occurrences]** "v5.0 phenomenological
   companion" / "companion paper (v5.0, arXiv: to be assigned)" — the
   "v5.0" tag is internal crossed-cosmos versioning, meaningless to a
   JHEP reader. **FIX APPLIED**: "v5.0" dropped; now reads
   "(companion, arXiv: to be assigned)" and "phenomenological companion".

## Honesty-gate cross-check

- Every numerical value in §6.3 (`log ρ_Λ/ρ_P ≈ -122.95`,
  `log (H_0/ω_P)² ≈ -121.86`, 1-dex gap) is explicitly flagged as
  order-of-magnitude coincidence, not identity. PASS.
- ω_P = 1.85e43 rad/s: matches standard Planck angular freq √(c⁵/Gℏ). PASS.
- κ_R^UV = 2π ω_P and κ_R^IR = H_0: explicitly stated as definitional,
  with the 2π factor called out. PASS.
- Every "we prove"/"we establish"/"we show": all four scripts in
  `derivations/` exist; pipeline Section 3 (forbidden-pattern scan) PASS.
- 18/18 audit gates still PASS post-fix.

## Consistency check

- §6 (outlook) does NOT contradict §5 positioning: both repeatedly state
  orthogonal/complementary to Pedraza et al., and Motivation 1 is
  explicitly tagged MOTIVATION. PASS.
- Lemma 1 wording matches Eq.(1): uses `\Ck`, `\PHk`, `\dn`, `\kR`
  notation identically. PASS.
- Bib: all 14 cite keys in draft (`Caputa2024`, `Pedraza2022Threads`,
  `Carrasco2023`, `Fan2022`, `Kirklin2025`, `DEHK2025a`, `DEHK2025b`,
  `MaHuang2025`, `Haferkamp2022`, `Yip2024`, `Longo2019`,
  `CeyhanFaulkner2020`, `Bianconi2025`, `CryptoCensorship`) present in
  `eci.bib`. No orphans introduced. PASS.

## Scope / undefined symbols

- All symbols defined at first use: `\Sgen`, `\tauR`, `\kR`, `\Ck`,
  `\PHk`, `\dn`, `\AR`, `\sigma^R_{\tauR}`, `\rho_R`, `K_R`, `\Delta_R`,
  `\PHk^c`, `\alpha`, `\Ck^{\max}`, `T_R`, `T_P`, `T_{dS}`, `\omega_P`,
  `\Omega_\Lambda`, `H_0`. PASS.
- All `\ref{...}` resolve (latexmk clean). PASS.
- No remaining overclaim: "we propose"/"we prove" verbs all bracketed by
  M1-M3 postulate labels. The only hard "we prove" is for the bound
  UNDER M1-M3, consistent with Thm 1 phrasing. PASS.

## PRINCIPLES.md cross-check

- V6-1 (Type-II formal track, no cosmological claim): explicit abstract
  + §8 conclusion statement. PASS.
- V6-4 (no falsifier required for formal paper): pipeline Section 4 PASS.
- Rule 1 (honesty-gate): all numerics tagged coincidence/definitional. PASS.
- Rule 3 (reversibility): fixes applied are one-line textual edits; git
  tracked. PASS.
- Rule 12 (no fabricated citations): all bib keys verified present. PASS.
- Rule 16 (no internal language shipped): three instances removed above. PASS.

## Mistral cross-check on rigour framing

`mistral-large-latest` (magistral-medium returned only thinking block,
truncated) on the bound + 3-postulate + limit-recovery framing:

> **YES** — "rigorous, well-structured upper bound with clear postulates,
> technical lemmas, and precise limiting cases, making it suitable for
> JHEP while transparently flagging conjectural elements."

## Applied edits (v6.2:adv-v3)

1. `v6_jhep.tex:285` — `\cite{Kirklin2025}` → `\cite{Fan2022}` on Fan 2022 demarcation paragraph.
2. `v6_jhep.tex:450-451` — stripped "bib key to be added by the bib-consolidation agent".
3. `v6_jhep.tex:107,249,528,684` — four "v5.0" internal tags replaced by "companion"/"phenomenological companion".

Total: 6 edit sites, all cosmetic / single-token; no structural change.
Post-fix: pipeline 18/18 PASS, latexmk 7 pages clean, 0 undef.

## Final verdict

**GO for arXiv** (SHIP after 6 one-line MINOR-FIX edits applied and verified).
