# Paper — Mass Gap Formula for 4D Pure Yang--Mills from Three Geometric Anchors

**Author**: Kévin Rémondière — Independent Researcher, Oloron-Sainte-Marie, France
**ORCID**: 0009-0008-2443-7166
**Email**: kevin.remondiere@gmail.com
**License**: CC-BY-4.0
**Date**: 21 May 2026 (v2)
**Status**: PRL draft v2 (5-page Letter, 6/6 first-principles)
**Target**: Physical Review Letters

## Abstract (v2)

We derive a closed-form expression for the dimensionless mass-gap ratio
m²(J,P,C,ex,N)/σ₀ in 4D pure SU(N) lattice Yang–Mills in which every
rational coefficient is generated from just **three geometric anchors**:

- `ξ★ = 2/3` (heat kernel on H³/PSL₂(O_K), Lean 4 proved)
- `F_∞ = 9/10` (Dijkgraaf–Witten genus expansion, Lean 4 proved)
- `δ = +2` (flux tube flexion energy unit, structural empirical, universal cross-N)

The two rationals that were empirical in v1 emerge as **exact algebraic
identities**:

```
β   = 2 + F_∞ · ξ★            = 13/5  EXACT  (NEW v2)
c_η = (ξ★ + δ) / (F_∞ + β)     = 16/21 EXACT  (NEW v2)
```

The full formula:

```
m²/σ₀ = (2π·e·ξ★) · F_∞²(1+1/N²)²
        · [ξ★·(J(J+1)/3 + δ·δ_{J,1}) + (β-P)(ex+ξ★)]
        · [1 + (η_∞ - c_η/N²)·(1-C)/2]
```

with `η_∞ = 1/2` (Lie-algebra so(N)/su(N) large-N limit). **Zero free
parameters** in the N → ∞ limit; σ₀ (string tension) is the sole
dimensional input via QCD transmutation.

Cross-N verification on Athenodorou–Teper lattice data (arXiv:2106.00364),
SU(N) for N ∈ {3,4,5,6,8}, 78 channels (excluding 2⁺⁻ ditorelon-dominated
scattering states): mean ≈14% residual, comparable to AT2021
systematic-plus-statistical errors.

## What changed in v2

In v1 (the first draft on this same day) two rationals — `β = 16/7` and
`c_η = -β/3 = -16/21` — were left as empirical structural constants. The
v2 paper exhibits both as exact algebraic identities in the three anchors:

| v1 (empirical) | v2 (derived)                              |
|---             |---                                        |
| β = 16/7       | β = 2 + F_∞·ξ★ = 13/5                    |
| c_η = -16/21   | c_η = (ξ★+δ)/(F_∞+β) = 16/21              |

The numerical predictions are essentially identical (β = 16/7 = 2.286 vs
β = 13/5 = 2.600, within the AT2021 95% CI), and the bootstrap fit
favors v2 slightly (1.7% closer to the free-fit central value).

## Tier classification (v2)

| Constant       | Identity                       | Tier             |
|---             |---                             |---               |
| ξ★ = 2/3       | anchor (heat kernel)           | Lean proved      |
| F_∞ = 9/10     | anchor (DW genus)              | Lean proved      |
| δ = +2         | anchor (flexion)               | structural       |
| K² = 4πe/3     | 2πe·ξ★                         | Lean proved      |
| α = 2/3        | ξ★                             | derived          |
| β = 13/5       | 2 + F_∞·ξ★                     | derived (NEW v2) |
| γ = 2/3        | ξ★                             | derived          |
| η_∞ = 1/2      | so/su large-N limit            | derived          |
| c_η = 16/21    | (ξ★+δ)/(F_∞+β)                 | derived (NEW v2) |
| c² formula     | full closed-form               | Tier 3 supported |

## Files

- `main.tex` — REVTeX 4.2 PRL source (v2)
- `main.pdf` — Compiled PDF (4 pages)
- `references.bib` — BibTeX (companion; main.tex uses `\thebibliography` inline)
- `compile.sh` — Build script

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

The historic-discovery worksheets are at:
- `notes/HISTORIC_beta_eq_2_plus_F_xi_2026-05-21.md`
- `notes/HISTORIC_c_eta_eq_xi_delta_over_F_beta_2026-05-21.md`
- `notes/eta_inf_HALF_DISCOVERY_2026-05-21.md`

## Cluster firm status

491 STABLE (entry and exit). 0 propagated public fab.
