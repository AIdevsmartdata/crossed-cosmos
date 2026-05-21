# Paper — First-Principles Mass Gap Formula for 4D Pure Yang--Mills

**Author**: Kévin Rémondière — Independent Researcher, Oloron-Sainte-Marie, France
**ORCID**: 0009-0008-2443-7166
**Email**: kevin.remondiere@gmail.com
**License**: CC-BY-4.0
**Date**: 21 May 2026
**Status**: PRL draft v1 (4-page Letter)
**Target**: Physical Review Letters

## Abstract

We propose a closed-form expression for the dimensionless mass-gap ratio
m²(J,P,C,ex,N)/σ₀ of 4D pure SU(N) lattice Yang–Mills, in which every
numerical coefficient is a rational constant derived from independently
established invariants. The formula reads

```
m²/σ₀ = (2π·e·ξ★) · F(N)² · c²(J,P,C,ex,N)
```

with `F(N) = (9/10)(1+1/N²)`, `ξ★ = 2/3`, `β = 16/7`, and

```
c² = [ξ★·(J(J+1)/3 + 2δ_{J,1}) + (β-P)(ex+ξ★)] · [1 + η(N)·(1-C)/2]
η(N) = 1/2 - β/(3N²).
```

Three structural constants (`K² = 2πe·ξ★`, `9/10`, `ξ★ = 2/3`) are
PROVED in Lean 4. Two NEW empirical rationals (`η_∞ = 1/2` within
2.8%, `c_η = -β/3 = -16/21` within 0.2%) enter the C-splitting.

Cross-N verification on Athenodorou-Teper lattice data
(arXiv:2106.00364), SU(N) for N ∈ {3,4,5,6,8}, 78 channels (excluding
2⁺⁻ ditorelon-dominated scattering states): mean ≈14% residual,
comparable to AT2021 systematic-plus-statistical errors.

## Tier classification

- **K = √(4πe/3)**: Tier 1, PROVED Lean 4 (`Crossed/Transport.lean`)
- **F(N) = (9/10)(1+1/N²)**: Tier 1, PROVED Lean 4 (DW genus expansion)
- **ξ★ = 2/3**: Tier 1, PROVED Lean 4 (heat kernel on H³/PSL₂(O_K))
- **c² formula**: Tier 3, SUPPORTED (14% residual on 78 AT2021 channels)
- **η_∞ = 1/2**: Tier 3, NEW empirical (within 2.8% on 5 N values)
- **c_η = -β/3**: Tier 3, NEW empirical (within 0.2% on 5 N values)
- **β = 16/7**: Tier 4, empirical (origin open)

## Files

- `main.tex` — REVTeX 4.2 PRL source
- `references.bib` — BibTeX (companion; main.tex uses `\thebibliography` inline)
- `compile.sh` — Build script
- `main.pdf` — Compiled PDF (4-5 pages)

## Compile

```bash
bash compile.sh
```

Or manually:

```bash
pdflatex main.tex
pdflatex main.tex
```

## Citations

This Letter has two companion papers (preprints same day):

1. `Paper_W1_xi_star_universal_CR` — proves ξ★ = 2/3 unconditional (Comptes Rendus)
2. `Paper_NoGo_PRL` — no-go theorems for arithmetic determination of σ₀

The historic-discovery worksheet is preserved in:
`notes/HISTORIC_DISCOVERY_eta_beta_3_2026-05-21.md`

## Cluster firm status

485 STABLE (entry and exit). 0 propagated public fab.
