---
name: A69 Wolf 2025 lit-extract
description: Identification + Lagrangian extraction of Wolf 2025 NMC cosmology paper (arXiv:2504.07679) for A70/A71 Bayes contest design
type: project
---

# A69 — Wolf 2025 lit-extract for ECI-vs-Wolf Bayes contest

**Date:** 2026-05-05 night (Wave 12 Phase 1)
**Owner:** Sonnet sub-agent (parent persisted; harness blocked sub-agent file writes)
**Hallu count entering / leaving:** 85 / 85 (held; live arXiv API verification)

## Verdict
**Wolf 2025 = generic scalar-tensor / Brans-Dicke / Horndeski-G4 ONLY.** Not Galileon, not chameleon, not k-mouflage.

## Identity (live arXiv-verified)
- **arXiv:** 2504.07679v3
- **Title:** "Assessing cosmological evidence for non-minimal coupling"
- **Authors:** Wolf, García-García, Anton, Ferreira
- **Journal:** PRL 135, 081001 (2025), DOI 10.1103/jysf-k72m
- **Categories:** astro-ph.CO + gr-qc + hep-ph + hep-th

## Lagrangian (verbatim Eq.1-2)
```
S = ∫d⁴x √(-g) [ M²_Pl/2 · F(φ) R  −  ½ G(φ) X  −  V(φ)  −  J(φ) X²  +  L_m ]
X ≡ ∂_μ φ ∂^μ φ
F(φ) ≃ 1 − ξ (φ²/M²_Pl)
V(φ) ≃ V₀ + β φ + ½ m² φ²
G(φ) = 1   (k-essence neutralisé)
J(φ) = 0   (Galileon X² neutralisé)
```
V₀ tuned (NOT sampled) to close Friedmann today. NMC enters exclusively via Brans-Dicke / Horndeski-G4 branch.

## Best-fit Wolf (BAO+CMB+DES-Y5)
- **ξ = 2.31 ⁺⁰·⁷⁵ ⁻⁰·³⁴**
- **log B = 7.34 ± 0.6** vs minimally-coupled scalar quintessence (NB: NOT vs strict ΛCDM)
- G_eff(0)/G_N = 1.77, 4.3σ from GR
- Concave potential (m² < 0) favoured

## A4 / A64 corrections caught
- **Planck 2018 NOT PR4 NPIPE** (A4 was wrong)
- **PolyChord NOT MultiNest** (A4 was wrong)
- Σm_ν = 0.06 eV fixed (matches Wolf)
- Datasets: DESI DR2 BAO + Planck 2018 T+E+EE + ACT DR6 lensing + DES-Y5 SN-Ia (rotated, not stacked)

## Wolf's KG-physical posture
- **HONEST about Cassini**: explicit abstract statement "additional new physics must be invoked to screen ... or quintessence is an unlikely explanation"
- **DOES NOT report homogeneous KG-stability diagnostics at ξ=2.31**
- A56's ξ_crit ≈ +0.20 was for V₀exp(−λφ) (ECI exponential potential) — Wolf's quadratic V is different, A56 bound does NOT transfer exactly. Generic mechanism (F(φ)R sources effective mass ~6ξH²) remains.
- Concave V₀+βφ+½m²φ² with m²<0 is flat-space-unstable; only Hubble friction stabilises during slow-roll.

## A70 must implement
1. **KG-stability gate** (CRITICAL): integrate homogeneous KG eq, reject samples with logL=−∞ if φ runaway / F(φ)<0 / a_today<0.95.
2. **Wolf-side params**: ξ ∈ [0,4.0], β ∈ [0,10] M_Pl·M_H², m² ∈ [−10,10] M_H² + 6 ΛCDM.
3. **ECI-side**: Cassini-clean wedge |ξ_χ|<0.024, exponential V₀exp(−λχ/M_P) (existing A25 emulator).
4. **Sampler**: PolyChord (matches Wolf, gives evidence directly) + NUTS cross-check.
5. **Boltzmann**: hi_class native; cosmopower-jax emulator if PolyChord too slow on RTX 5060 Ti.
6. **Sanity gate**: must reproduce Wolf log B = 7.34 ± 2σ on Wolf-side branch before publishing.

## Pre-registered hypotheses (frozen for A71)
- H0: log B(ECI vs Wolf) > +1 → Cassini-clean wedge wins
- H1: log B(Wolf vs ECI) > +1 → Wolf large-ξ recovered (forces ECI v7.5 reformulation)
- H2: log B ∈ [−1,+1] → tie

## Discipline log
- arXiv 2504.07679 RE-VERIFIED via live arXiv API
- Lagrangian extracted via WebFetch on arxiv.org/html/2504.07679v3 verbatim
- 0 fabrications. Mistral NOT used.

## Files
- `lagrangian.tex` — verbatim Eq.1-2 ready to import into eci.tex
- `likelihood_design_notes.md` — full A70 spec
