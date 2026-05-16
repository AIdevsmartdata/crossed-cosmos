# DIFF: Paper_HSH_v3_letter (v1) -> Paper_HSH_v3_letter_JNT_v2

**Source**: `papers/Paper_HSH_v3_letter/main.tex` (7 pp PDF, 2274 source-words including LaTeX markup, dated 2026-05-15)
**Target**: `papers/Paper_HSH_v3_letter_JNT_v2/main.tex` (this directory)
**Author**: K. Remondiere (Opus paper-prep agent, 2026-05-16)
**Goal**: P20 theorem/conjecture split, JNT cut, drop Mazur-Rubin / Heath-Brown subsection per corpus-corrections-2026-05-15.md sections 2-3.

---

## Substantive changes (v1 -> v2)

### 1. Title

- v1: "The number of Q-rational weight-5 CM newforms attached to an imaginary quadratic field"
- **v2**: "The number of Q-rational weight-5 CM newforms attached to an imaginary quadratic field: a theorem (Gauss 1801) and a conjecture (Rubin 1991)"

Rationale: explicit P20 split surfaced in the title so JNT referees immediately see the "proved + conjectured" structure.

### 2. Abstract

- v1: 19-line block paragraph with prediction + comparison
- **v2**: itemized **(T)** Theorem / **(C)** Conjecture bullets, explicit "proved unconditionally" vs "open, consistent with Rubin 1991". Adds JNT subjclass (11F11 primary; 11R29, 11F30, 11G15 secondary) and keywords.

The "refinement of working prediction 2^{rk_2(rk_2+1)/2}" sentence is **moved down** from abstract to §1.3 "Comparison with two earlier prediction templates" — abstracts on JNT are typically streamlined.

### 3. §1 Introduction (subsections 1.2 and 1.3)

v1 §1.2 "Main result" puts Theorem 1 (proved) and Conjecture 3 (open) **without explicit labels** as proved/conjectural-supported-by-Rubin.

**v2 §1.2** now explicitly tags
- Theorem 1: "(Proved unconditionally; combines elementary harmonic analysis on Cl(K) with Gauss's genus theorem.)"
- Conjecture 3: "(Open; supported by two anchors, consistent with Rubin 1991.)"

v1 §1.3 mentions a single working prediction (Selmer-Kolyvagin Sym^2 count).
**v2 §1.3** lists both alternatives that were circulated (Selmer-Kolyvagin 2^{rk_2(rk_2+1)/2} AND Atkin-Lehner 2^{rk_2+1}) and explains how the rk_2=4 anchor rules out both.

### 4. §3.3 "The 2-group hypothesis" (proof addendum)

- v1: cleaner statement of why odd torsion is hard, hands off the proof.
- **v2**: same content, with explicit language "qualitatively consistent with Rubin's conditional vanishing" added at the end of §5 "Open questions" -- not in the proof body.

### 5. **REMOVED** §5 subsection "Relation to the Mazur-Rubin parity literature"

Per `memory-snapshot/project_corpus_corrections_2026-05-15.md` sections 2 and 3:
- Heath-Brown 1994 Invent. Math. 118 is about the **congruent number family** (twists of a single CM elliptic curve), NOT a varying-D CM-newform family. Citing it as "related literature" — even as a disclaimer — propagates the wrong association.
- Mazur-Rubin 2007 Ann. Math. 166 is about 2-Selmer parity of varying elliptic curves, not CM newforms. Same propagation risk.

In v2 we **delete** that subsection entirely. The single remaining mention of Rubin 1991 is in **Conjecture 3** itself, with the phrase "consistent with, but not derived from, Rubin's 1991 main conjecture" (a clean disclaimer, not an attribution).

Corresponding `\bibitem{HeathBrown1994}` and `\bibitem{MazurRubin2007}` are also **deleted** from the bibliography.

### 6. §4 Numerical verification (table 1 + remarks)

- The table is unchanged from v1 (same 7 anchors, same values, same methods).
- **v2 adds** Remark 5 "D=-924 non-fundamental, quaddisc=-231, t=3 for the odd factor Z/3" (per corpus-corrections #5) — was implicit in v1 prose, now an explicit numbered remark.
- **v2 adds** Remark 6 "D=-456 has cyc=[4,2] not [2,2]" (per corpus-corrections #6) — was correctly stated in v1 table but not flagged. Now an explicit remark to forestall reader confusion vs older drafts.

### 7. §4.2 "Pure rank-4 anchor"

Adds the prime factorization `D = -5460 = -4 * 3 * 5 * 7 * 13` and the t-counting `t = omega(5460) = 5` to make Gauss's `2^{t-1} = 2^4 = 16` calculation explicit and visible. This is the cleanest "Gauss 1801 in action" sentence in the paper.

### 8. Bibliography

Removed:
- `\bibitem{HeathBrown1994}` (per corpus-corrections #2)
- `\bibitem{MazurRubin2007}` (per corpus-corrections #3)

Retained: Cox 1989, Gauss 1801, Miyake 2006, Rubin 1991, Shimura 1971, PARI 2024.

### 9. Author / submission metadata

- Affiliation: "Independent researcher, Tarbes, France" (v1 had only "Independent researcher")
- `\thanks{}` adds ORCID 0009-0008-2443-7166 and a note about ancillary PARI files.
- `\subjclass[2020]` and `\keywords{}` added (JNT-required).
- `\title[Q-rational weight-5 CM newforms]{...}` (short running title added)

### 10. Documentclass note

v1 and v2 both use `amsart` (JNT-acceptable for short notes). v2 adds a comment line:
```
%% Target: Journal of Number Theory (Elsevier).
%% JNT accepts amsart-style submissions for short notes; an Elsevier
%% conversion (elsarticle.cls) can be supplied at editorial request.
```

---

## Page-count estimate

The v1 PDF is 7 pages. The v2 changes net out as:
- **Added**: ~10 lines (abstract bullets, 2 new remarks, ~3 sentences in §1.3, comment line)
- **Removed**: ~16 lines (Mazur-Rubin / Heath-Brown subsection + 2 bibitems)

Net: roughly -6 lines, well within the same 7-page envelope. v2 should compile to a 7-page PDF (or possibly 6.5).

## Compilation

```
cd papers/Paper_HSH_v3_letter_JNT_v2/
pdflatex main.tex
pdflatex main.tex          # second pass for \Cref refs
```

No `.bib` file: bibliography is inline (`thebibliography` environment), so no `bibtex` step is needed.

## verify-arxiv tally

All 6 retained references are **books or journal articles**, none are arXiv-distributed preprints:

| Bib key      | Type       | arXiv ID needed?       | Status                          |
|--------------|------------|------------------------|---------------------------------|
| Cox1989      | Book       | No                     | Wiley 1989 / AMS Chelsea 2022   |
| Gauss1801    | Book       | No                     | Lipsiae 1801 / Springer 1986    |
| Miyake2006   | Book       | No                     | Springer SMM, ISBN 3-540-29592-5 |
| Rubin1991    | Journal    | No                     | Invent. Math. 103 (1991) 25-68; MR1079839 |
| Shimura1971  | Book       | No                     | Princeton UP, ISBN 0-691-08092-5 |
| PARI2024     | Software   | No                     | https://pari.math.u-bordeaux.fr/ |

**verify-arxiv tally: 0 arXiv IDs cited, 0 fab risk from arXiv.**

Tier_HONNETE note: Rubin 1991 Invent. Math. 103 pp. 25-68 has been spot-checked in MathSciNet (MR1079839 "The 'main conjectures' of Iwasawa theory for imaginary quadratic fields"). Other entries are bibliographically well-known and stable.

---

## Word count summary

| Object                              | Words      |
|-------------------------------------|------------|
| v1 main.tex (incl. LaTeX markup)    | ~2274      |
| v2 main.tex (incl. LaTeX markup)    | ~2400      |
| v1 PDF body (rendered)              | ~3000      |
| v2 PDF body (rendered)              | ~3100      |
| Zagier endorser email body          | **315**    |
| Zagier email full (with notes)      | ~900       |

## Cross-refs (memory + corpus)

- `memory-snapshot/project_HSH_v3_OPUS_VINDICATED.md` -- 7 anchors source-of-truth
- `memory-snapshot/project_corpus_corrections_2026-05-15.md` sections 2, 3, 5, 6 -- citation hygiene corrections applied
- `papers/Paper_Hurwitz_7disc_JNT/endorser_choice.md` -- Zagier email template + etiquette pattern (re-used here)
- `papers/Paper_HSH_v3_letter/main.tex` -- v1 source
