# crossed-cosmos

**ECI — Entanglement, Complexity, Information.** Two companion papers on orthogonal tracks: (v5) a phenomenological framework with MCMC on DESI DR2 + Pantheon+ targeting EPJ C, and (v6) a formal differential GSL on type-II crossed-product algebras targeting JHEP.

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.19686399.svg)](https://doi.org/10.5281/zenodo.19686399)
[![License: CC BY 4.0](https://img.shields.io/badge/License-CC_BY_4.0-lightgrey.svg)](https://creativecommons.org/licenses/by/4.0/)
[![ORCID](https://img.shields.io/badge/ORCID-0009--0008--2443--7166-a6ce39)](https://orcid.org/0009-0008-2443-7166)

> *"Le Big Bang n'est pas un instant, c'est une frontière de décodabilité."*

---

## The two companion papers

| | **v5.0** phenomenological | **v6.0** formal |
|---|---|---|
| Track | EPJ C / astro-ph.CO | JHEP / hep-th |
| Pages | 14 | 7 |
| Source | `paper/eci.tex` | `paper/v6/v6_jhep.tex` |
| Data | DESI DR2 + Pantheon+ MCMC (19700 samples, R-1=0.036) | None — pure formalism |
| Main result | ξ_χ = 0.003 +0.065/−0.070 (68% CL), BF_01 ≈ 1 | dS_gen/dτ_R ≤ κ_R · C_k · Θ(PH_k) + logistic envelope (Prop. 1) |
| Second result | — | Dequantisation map (type-II → classical PH) |
| Falsifier | NMC deviations from ΛCDM at DR3+Euclid | None (D18 / D18b killed fσ_8 × Θ(PH_2)) |
| Zenodo | [10.5281/zenodo.19686399](https://doi.org/10.5281/zenodo.19686399) | (fresh DOI on tag `v6.0.0`) |

The two papers are **complementary, not hierarchical**: v6 does not subsume or supersede v5; it operates on an orthogonal axis (formal-algebraic vs empirical-fit).

## What is this

A **framework paper** — not a derivation, not a fit on DESI DR2. It assembles six programs into one architecture and lists seven falsifiable predictions (DESI DR3, Euclid DR1, CMB-S4, SO, Eöt-Wash, optical clocks, KM3NeT).

- **A1 — Observer-dependent algebra** (type II via QRF crossed product)
- **A2 — Emergent geometry** (Jacobson, non-perturbative GSL)
- **A3 — Cryptographic Censorship** as bulk selection rule
- **A4 — Two-field scalar sector** (EDE axion + NMC thawing quintessence)
- **A5 — Dark Dimension** (mesoscopic extra dimension, KK DM)
- **A6 — Persistent-homology complexity** (primordial non-Gaussianity diagnostics)

## What this is *not*

- Not peer-reviewed. Not yet.
- Not a new derivation — an architectural synthesis.
- Not quantitative at the level a PRD / JCAP referee would demand. EPJ C or Foundations of Physics are the realistic editorial targets.

## Read it

- `paper/eci.tex` — v5 RevTeX source (phenomenological)
- `paper/v6/v6_jhep.tex` — v6 RevTeX source (formal)
- `paper/v6/RELEASE_NOTES.md` — v6 release notes and audit trail
- `paper/v6/CITATION.cff` — v6-specific citation metadata
- `paper/eci.bib` — verified bibliography (DOIs cross-checked via Crossref, 2026-04-22)
- `derivations/V6-claims-audit-pipeline.py` — pre-write rigour pipeline (18/18 PASS on v6.2)
- `paper/_internal_rag/PRINCIPLES.md` — project-wide editing rules
- `CHANGELOG.md` — version log

## Build

```bash
cd paper && latexmk -pdf eci.tex
```

## Cite this preprint

```bibtex
@misc{Remondiere2026ECI,
  author  = {Remondi\`ere, Kevin},
  title   = {ECI --- Entanglement, Complexity, Information: a framework paper},
  year    = {2026},
  doi     = {10.5281/zenodo.19686399},
  url     = {https://github.com/AIdevsmartdata/crossed-cosmos}
}
```

Or use `CITATION.cff` (GitHub "Cite this repository" button picks it up automatically).

## Releases → Zenodo DOI

Each `git tag v*` creates a GitHub Release which Zenodo auto-archives under a fresh DOI. Toggle the repo on https://zenodo.org/account/settings/github/ to enable.

## License

- Text: [CC BY 4.0](LICENSE)
- Code (if any added later): MIT

## Author

**Kevin Remondière** — Independent Researcher · ORCID [0009-0008-2443-7166](https://orcid.org/0009-0008-2443-7166) · arXiv `AIdevsmartdata`

## Roadmap

- [ ] v4.0 — corrections bibliographiques + N_eff ACT DR6 + Ġ/G Biskupek
- [ ] Zenodo DOI (first release)
- [ ] HAL deposit (CNRS timestamp)
- [ ] arXiv gr-qc endorsement request
- [ ] MCMC on DESI DR2 with (ξ_χ, α, φ_c) — needs Boltzmann code collaborator
- [ ] Submit to EPJ C (SCOAP3 OA)
