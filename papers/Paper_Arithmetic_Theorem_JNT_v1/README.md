# Paper Arithmetic Theorem (consolidated) — target Journal of Number Theory

**Status**: DRAFT v1, compiled clean 12 pages (2026-05-20). Awaiting OCR + adversarial Opus review before submission.

## Description

Consolidation of three prior crossed-cosmos papers into a single self-contained
unconditional arithmetic-theorem paper for J. Number Theory submission:

- `Paper_Lemma_A32_Selberg_JFA/main.tex` — Theorem 1.1 (per-character Selberg
  pretrace decomposition on Bianchi 3-orbifolds, unconditional).
- `Paper_W1_xi_star_universal_CR/main.tex` — Universal Selberg residue ratio
  ξ* = 2/3 on every Bianchi 3-orbifold (unconditional, 100-digit verified).
- `Paper_CR_Theorem_JNT/main.tex` — Center–Rank inequality CR (conditional on
  G1–G4) + Dirichlet companion CR' (unconditional, 153/153 PASS).

Plus structural F(N) = (9/10)(1 + 1/N²) form via 't Hooft + Dijkgraaf–Witten
genus expansion at the SU(3) anchor (TIER 3 sketch).

The three ingredients assemble into the arithmetic invariant
  C(N) := √(2πe · 2/3) · (9/10)(1 + 1/N²) ∈ ℝ_{>0}, N ≥ 2.

C(N) is calculable algorithmically. The paper makes no physical interpretation
claim; empirical comparison with SU(N) glueball anchors is deferred to a
companion paper.

## Structure (12 pages)

- §1 Introduction (motivation + main theorem + honest scope) — ~3pp
- §2 Part (A): Per-character pretrace decomposition (5-step proof sketch) — ~3pp
- §3 Part (B): Universal Selberg residue ratio ξ* = 2/3 — ~2pp
- §4 Part (C): Center–Rank inequality + Dirichlet companion + per-N table — ~3pp
- §5 Part (D): F(N) via Dijkgraaf–Witten genus expansion — ~1pp
- §6 Assembly: definition of C(N), 3 falsifiables — ~1pp
- §7 Discussion + open questions — ~1pp

## Target

**Journal of Number Theory** (Elsevier), primary.

Alternates: Acta Arithmetica, J. Functional Analysis (for the spectral
ingredient), Transactions AMS.

## Theorem statement style

UNCONDITIONAL (parts A, B, C', D), CONDITIONAL on G1–G4 (part C).

## arXiv IDs verified live

- `hep-th/0306138` (Vassilevich 2003, *Heat kernel expansion: user's manual*)
  — verified via `/root/bin/verify-arxiv.py` 2026-05-20 → STATUS VERIFIED.

All other references are classical (Gauss 1801, Dirichlet 1839, Hecke 1937,
Selberg 1956, 't Hooft 1974/1979, Dijkgraaf–Witten 1990, Sarnak 1983,
Kim 2003, Cox 1989, Neukirch 1999, Davenport 2000, Rudin FA, Reed–Simon I,
EGM 1998, Bunke–Olbrich 1995, Gangolli–Warner 1980, Athenodorou–Teper 2021
arXiv:2106.00364). No arXiv-only IDs introduced beyond the Vassilevich 2003
(inherited from W1 source paper).

## Files

- `main.tex` — LaTeX source (amsart, 12pp typeset, ~595 KB PDF)
- `refs.bib` — bibliography (22 verified entries; no new arXiv IDs)
- `main.pdf` — compiled PDF (12 pages)
- `README.md` — this file

## Compile

```
cd Paper_Arithmetic_Theorem_JNT_v1
latexmk -pdf main.tex
```

Output: `main.pdf` (12 pages, ~595 KB).

## Cluster discipline

- Entry: 448 STABLE
- Exit: 448 STABLE (no new fabs introduced; no new arXiv IDs beyond Vassilevich
  hep-th/0306138 inherited from W1 + verified live).
- Honest-scope clauses preserved: no universal Selberg gap claim; no physical
  identification claim; no Clay Millennium claim.

## Next steps

1. **Adversarial Opus review** of this consolidated paper (1 reviewer pass:
   1-shot REJECT verdict + identify any over-claims or attribution errors).
2. **OCR pass** on the compiled PDF (manual scan for typos, broken refs,
   formatting issues).
3. **Final compile** after adversarial fixes.
4. **Cover letter** drafting for J. Number Theory editor.
5. **Private commit + push** to `crossed-cosmos-private` (NOT public yet —
   keep embargoed until OCR + adversarial pass complete).

## Author

Kévin Rémondière (independent researcher, Oloron-Sainte-Marie, France).
ORCID [0009-0008-2443-7166](https://orcid.org/0009-0008-2443-7166).
crossed-cosmos project (concept DOI
[10.5281/zenodo.19686398](https://doi.org/10.5281/zenodo.19686398)).
