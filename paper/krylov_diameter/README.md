# krylov_diameter — A Krylov-Diameter Correspondence on Type II_infty FRW Crossed Product Algebras

Standalone math.OA note, May 2026. Author: Kevin Remondiere.

## Files

- `krylov_diameter.tex` — main note, 7 sections (Introduction, Setup,
  Block A definition, Main theorem, Era-by-era, CMPT comparison,
  Open problems).
- `krylov_diameter.bib` — bibliography (8 entries; arXiv IDs
  verified 2026-05-02 via `https://export.arxiv.org/api/query`).
- `krylov_diameter.pdf` — compiled output (7 pages, ~500 KB).

## Subject

Honest reframing of "Piste 1" (`/tmp/piste1_hubble_kc.md`,
`/tmp/piste1_gauge_audit.md`) following the Mistral large-latest
counter-review (2026-05-02) and a sympy-verified gauge audit:

> The substantive content is the geometric identity
> `(1/C_k) dC_k/dt = 1/R_proper(eta_c)`, not a universal
> Hubble-Krylov claim. The Hubble identity `H = 1/R_proper` is
> era- and diamond-convention-conditional and is recovered as
> Friedmann arithmetic in two of the four era/diamond combinations
> tabulated in §5.

## Companion paper

`paper/frw_typeII_note/frw_note.tex` — the type II_infty
classification of the FRW crossed product (Theorem 3.5/3.6, Cor 3.7
in this README; theorem.5/theorem.6/theorem.7 in the compiled
frw_note PDF) is taken as input for the present Theorem 1
(Theorem 4 in the compiled krylov_diameter PDF).

## Compile

```
pdflatex krylov_diameter
bibtex   krylov_diameter
pdflatex krylov_diameter
pdflatex krylov_diameter
```

Last clean compile (2026-05-02): 7 pages, 2 trivial overfull-hbox
warnings (max 2.65 pt), 2 BibTeX warnings about the empty `journal`
field in arXiv-only entries (intentional and correct), no errors,
no undefined references.

## Bibliography (verified arXiv API, 2026-05-02)

- CMPT24 — Caputa, Magán, Patramanis, Tonni (2024), arXiv:2306.14732,
  PRD 109, 086004
- ParkerEtAl2019 — Parker, Cao, Avdoshkin, Scaffidi, Altman, Khemani
  (2019), arXiv:1812.08657, PRX 9, 041017
- AguilarGutierrez2025 — Aguilar-Gutiérrez (2025), arXiv:2511.03779
- CLPW2023 — Chandrasekaran, Longo, Penington, Witten (2023),
  arXiv:2206.10780, JHEP 02, 082
- Witten2022 — Witten (2022), arXiv:2112.12828, JHEP 10, 008
- HislopLongo1982 — Hislop, Longo (1982), CMP 84, 71
- CHM2008 — Casini, Huerta, Myers, JHEP 0805:012 (used for
  modular/proper-time Jacobian at the diamond center, eq. 3.16)
- Remondiere2026 — companion frw_typeII_note (this repo)
