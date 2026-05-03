# `paper/frw_typeII_curved/` --- spatially curved FRW companion note

Standalone math.OA companion note extending the FRW conformal-pullback type
II_infty classification of `paper/frw_typeII_note/frw_note.tex` (Theorems
3.5/3.6, spatially flat k=0 case) to spatially curved (k = +/- 1)
Friedmann-Robertson-Walker spacetimes.

## Files

- `note.tex` -- main document (9 pages compiled).
- `note.bib` -- bibliography (all arXiv-indexed entries triangulated
  2026-05-02 against arxiv.org abstract pages; 16 references).
- `note.pdf` -- compiled PDF (requires `pdflatex`, `bibtex`).
- `note.{aux,bbl,blg,log,out}` -- LaTeX auxiliary outputs from the
  build (regenerable by re-running the build pipeline below).
- `README.md` -- this file.

## Build

```
pdflatex note
bibtex   note
pdflatex note
pdflatex note
```

This produces `note.pdf` with no undefined references and no undefined
citations (verified 2026-05-02).

## Result summary

- **Theorem 2 (open FRW, k = -1, Section 4) -- UNCONDITIONAL.** For the
  conformally coupled massless scalar on open FRW with smooth strictly
  positive a(eta) on a closed conformal-time interval bounded away from
  the Big Bang, the modular crossed product A(D_O)_FRW \rtimes_sigma R
  of a doubly-bounded comoving causal diamond is a type II_infty factor.
  Proof factors through the classical isometry Milne ~ I^+(0) \subset
  Mink and reduces to the k=0 Theorem 3.5/3.6 of the companion note via
  Hislop-Longo on the lifted Minkowski diamond.

- **Theorem 9 (closed FRW, k = +1, Section 5) -- CONDITIONAL on
  H1_{+1}.** Items (1)-(2) (geometric modular action, modular stability,
  SO(4,1) covariance, cyclic-separating ground state on wedges;
  cyclicity on diamonds of conformal-time extent > pi/2 (1 - alpha)) are
  unconditional via Buchholz-Mund-Summers 2000 (arXiv:hep-th/0011237),
  Theorem 3.1 + Cor 3.2 + Cor 3.3 (quoted verbatim as Theorem 5, Cor 6,
  Cor 7 in our note). Item (3) (type II_infty crossed product) is
  conditional on the residual hypothesis H1_{+1}: the wedge net of the
  conformally coupled massless scalar on the Einstein static universe in
  its conformally invariant ground state has type III_1 factors with
  full Connes spectrum on its spherical-diamond subalgebras. BMS p.16
  (last paragraph before References) is quoted verbatim and explicitly
  flags the conformally coupled scalar question on RW (and a fortiori on
  ESU) as open.

- **Sympy identity (Section 3).** The curvature-corrected
  conformal-covariance identity (Wald 1984 App. D, eq. D.9)
  (Box_g~ - R[g~]/6)(a phi) = a^3 (Box_g - R[g]/6) phi
  is verified for k = -1, 0, +1 by `piste_spatially_curved.py` (in
  `/tmp/`, bundled with source). The Ricci scalars
  R[g~_k] = 6k and R[g_FRW] = 6 (a''/a + k) / a^2 are sympy-rederived
  from the Christoffel symbols.

## Reference triangulation log (2026-05-02)

All arXiv-indexed entries were triangulated against the corresponding
arxiv.org abstract pages via the OpenSearch `<meta name="citation_*">`
metadata. All confirmed:

| Reference | arXiv ID | Status |
|---|---|---|
| Buchholz-Mund-Summers 2000 | hep-th/0011237 | Confirmed: title + authors + abstract match |
| Brunetti-Guido-Longo 1993 | funct-an/9302008 | Confirmed: title + authors match |
| Hollands-Wald 2001 | gr-qc/0103074 | Confirmed: title + authors match |
| Iihoshi-Ketov-Morishita 2007 | hep-th/0702139 | Confirmed: title + authors match (note: 3 authors, not 2 as in some preliminary notes) |
| Verch 1997 | funct-an/9609004 | Confirmed: title + author match |
| Frob 2023 (JHEP 12 (2023) 074) | 2308.14797 | Confirmed: title + author + DOI match |
| Chandrasekaran-Longo-Penington-Witten 2023 | 2206.10780 | Confirmed (carry-over from companion note) |
| Witten 2022 | 2112.12828 | Confirmed (carry-over from companion note) |

Pre-arXiv journal references (Hislop-Longo 1982 CMP 84, 71; Connes 1973
Ann. Sci. ENS 6, 133; Wald 1984/1994 books; Penrose-Rindler 1986 book;
Dimock 1980 CMP 77, 219; Luders-Roberts 1990 CMP 134, 29) cite their
journal entries with DOIs where available.

## Recommended publication target

Letters in Mathematical Physics (LMP) or Communications in Mathematical
Physics (CMP). The note is short (9 pages) and naturally fits LMP; CMP
fits if the spatially-flat companion note is bundled / submitted in
parallel. arXiv primary class: math.OA (cross-list to math-ph and
gr-qc).

## Status

- Verified clean compile (0 undefined references, 0 undefined citations).
- All references arXiv-triangulated (2026-05-02).
- NOT pushed to remote.
