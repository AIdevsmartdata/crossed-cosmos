---
name: M17 integration log
description: Detailed log of label renames, bibitem additions, paragraph insertions in modular_shadow_LMP_v2.tex
type: project
---

# M17 Integration Log

**Date:** 2026-05-06
**File audited:** `/root/crossed-cosmos/notes/eci_v7_aspiration/MODULAR_SHADOW/modular_shadow_LMP_v2.tex`

## A61 label renames applied (all prefixed A61-)

| Original label (in proof_draft.tex) | Renamed label (in v2.5 appendix) | Line in v2.tex |
|---|---|---|
| eq:crossed | eq:A61-crossed | 803 |
| eq:modflow | eq:A61-modflow | 819 |
| eq:trunc | eq:A61-trunc | 833 |
| lem:bw-trunc | lem:A61-bw-trunc | 845 |
| eq:gns | eq:A61-gns | 880 |
| eq:liouv | eq:A61-liouv | 886 |
| eq:lanczos | eq:A61-lanczos | 907 |
| eq:CKmod | eq:A61-CKmod | 919 |
| eq:schrod-discrete | eq:A61-schrod | 950 |
| eq:parker-cosh | eq:A61-parker-cosh | 971 |
| eq:moments | eq:A61-moments | 1003 |
| eq:hankel | eq:A61-hankel | 1014 |
| eq:bw-spectral | eq:A61-bw-spectral | 1031 |
| eq:moment-asymp | eq:A61-moment-asymp | 1056 |
| eq:total-moment | eq:A61-total-moment | 1071 |
| eq:bw-twopt-sat | eq:A61-bw-twopt-sat | 1107 |
| sec:setup | ssec:A61-setup | 784 |
| ssec:crossed | sssec:A61-crossed | 795 |
| ssec:trunc | sssec:A61-trunc | 823 |
| ssec:krylov | sssec:A61-krylov | 873 |
| sec:proof | ssec:A61-proof | 924 |
| sec:vardian | ssec:A61-vardian | 1135 |
| sec:open | ssec:A61-open | 1155 |

## Sections removed from A61 body during integration

- `\maketitle` (A61 title/author/date block stripped)
- `\begin{abstract}...\end{abstract}` (stripped — paper has its own abstract)
- `\begin{thebibliography}...\end{thebibliography}` (stripped — merged into v2 bib)
- `\end{document}` (stripped)
- `\section{Setup...}` → converted to `\subsection{Setup...}` (and sub-sections to subsubsection)
- `\section{Bound theorem...}` → converted to `\subsection{Full proof...}`
- `\section{Comparison...}` → converted to `\subsection{Comparison...}`
- `\section{Open problems}` → converted to `\subsection{Open problems...}`

## Bibitem additions to v2.5 bibliography (from A61)

| Bibkey | Added? | Note |
|---|---|---|
| Parker2019 | Already present (line 1193) | v2 already cited it |
| BisognanoWichmann1976 | Already present (line 1245) | v2 already cited it |
| Haag1996 | ADDED (line 1250) | New addition for A61 Step 2 |
| Witten2022 | Already present (line 1205) | v2 already cited it |
| CLPW2023 | Already present (line 1211) | v2 already cited it |
| FaulknerSperanza2024 | Already present (line 1217) | v2 already cited it |
| Caputa2024 | Already present (line 1199) | v2 already cited it |
| Vardian2026 | Already present (line 1263) | v2 already cited it |
| AvdoshkinDymarsky2019 | Already present (line 1272) | v2 already cited it |
| Camargo2023 | Already present (line 1278) | v2 already cited it |
| Sreeram2025 | Already present (line 1285) | v2 already cited it |

**Net new bibitems added: 1 (Haag1996)**

## §1 paragraph additions

**"Literature status as of 2026-05-06" paragraph** (lines 163–183):
- Inserted as a new `\paragraph{}` in §1 (Introduction) before `\paragraph{Organization.}`
- Content: confirms no 2026 challenger from M5 search, identifies adjacent papers
  (Govindarajan-Sadanandan 2604.11277, Benjamin-Fitzpatrick-Li-Thaler 2604.01275)
- Confirms A77 finding: g≥2 bootstrap in different functor category, 0 of 4 A61 pillars
  have off-the-shelf g≥2 analogs
- Correctly refers to `Appendix~\ref{app:A61-proof}` for full proof

**Pointer in `\paragraph{Organization.}`** (line 188):
- "full details in Appendix~\ref{app:A61-proof}" inserted into §3 description

## Preamble changes

**No changes needed.** A61 declared `\newtheorem{definition}[theorem]{Definition}`
but `\begin{definition}` is never used in the integrated appendix content.
All other A61 theorem environments (theorem, proposition, lemma, conjecture,
remark, corollary) were already present in v2.tex preamble.

## Hallu discipline

All references in Appendix A come from A61's live-verified list (2026-05-05).
No new bibliographic claims introduced by M17.
Hallu count: 85 in → 85 out.
