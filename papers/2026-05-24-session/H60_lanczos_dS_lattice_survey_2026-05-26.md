# H60 — Lanczos d_s lattice FP eigenvalue density survey

**Verdict** : d_s partially measured, **best fit ≈ 2.3-2.5** (not 2 strict, not 10/3 strict). Discriminate via heat-trace measurement (6-10 weeks).

## 1-line synthesis

ρ(λ) ~ λ^α with α = 0.15-0.25, giving **d_s = 2(α+1) ≈ 2.3-2.5** with uncertainty spanning [2.0, 3.0]. No clean discrimination yet.

## Top 5 verified lattice papers

1. **hep-lat/0509054** Greensite-Olejnik-Zwanziger "Gribov horizon under microscope" — SU(2) Coulomb, ρ(λ) ~ λ^0.25 (full configs Sec. 5)
2. **hep-lat/0702002** Nakagawa-Nakamura-Saito-Toki — quenched SU(3) Coulomb 24⁴, fit p=0.15(10), χ²/ndf=1.60
3. **hep-lat/0510109** Sternbeck-Ilgenfritz-Müller-Preussker — SU(3) Landau (cross-check), ε=0.16(4) λ₁, 0.24(5) λ₂, 0.45(4) λ₅
4. **arXiv:1204.6591** Iritani-Suganuma — SU(3) Coulomb, confirms ρ(λ) → λ^(1/2) free-field. References SU(2) GOZ
5. **arXiv:1001.0784** Greensite "FP spectra at Gribov horizon" — continuum perturbative, predicts ~λ^(0.2-0.25) in 3D

## Discrimination vs 3 candidates

| d_s | α expected | vs lattice α≈0.15-0.25 |
|-----|-----------|------------------------|
| 2 (Greensite implicit) | 0 | marginal compat ~1σ in Nakagawa |
| **10/3 (Gribov fractal H46)** | **2/3 ≈ 0.667** | **DISFAVORED 4-5σ below** |
| 4 (naive 4D) | 1 | excluded >>5σ |

**Verdict** : d_s = 10/3 hypothesis (which would make {ξ★=2/3, κ_FP=1/6} ζ-pole residues per H58) is DISFAVORED by current data.

**Note** : d_s ≈ 2.3 is NEW intermediate value. Could correspond to s_k poles at 1.15, 0.65, 0.15, -0.35, ... — closer to {κ_FP=1/6 ≈ 0.167} weakly compatible.

## Honest gap

- All published fits = single power law at fixed volume, NO heat-trace Tr(e^{-tΔ_FP}) extraction
- α sensitive to lower-cutoff in λ + vortex content (GOZ vortex-only ρ(0+)=0.06, vortex-removed ~0)
- NO continuum extrapolation
- NO SU(2) vs SU(3) matched physical volume comparison

## ETA new measurement

- Config gen SU(2) β=2.4 32⁴ + SU(3) β=6.0 24⁴×32, 50 configs each : 1-2 weeks 4-GPU
- Lanczos 500 modes per config : ~1 week
- Continuum extrap (3 spacings) : **6-10 weeks total for d_s ± 0.1**
- Fast-path single-spacing : ~2 weeks for α ± 0.2

## ANTI-FAB CATCHES

- **arXiv:0901.0736 author list ERROR** : task referenced "Bogolubsky-Sternbeck-Maltman-von Smekal-Williams" but actual paper = Bogolubsky-Ilgenfritz-Müller-Preussker-Sternbeck in Landau (not Coulomb) gauge. No FP spectrum measurement.
- Author list as given was INCORRECT.

## Author

Kévin Rémondière (ORCID 0009-0008-2443-7166)

## Links

[[H58_zeta_FP_poles_meromorphic_2026-05-26]]
[[spectral_decoder_validated_2026-05-26]]
