# A41 — TOP-5 cosmology models vs ECI v7.4

**Date:** 2026-05-05 evening
**Owner:** Sonnet sub-agent A41 (parent persisted)
**Hallu count entering / leaving:** 84 / 84 (held; brief-internal mis-attribution caught for Bella et al., not propagated)

## Verification ledger (corrections to mission tags)

| # | Mission ID | Verified status |
|---|---|---|
| 1 | Planck PR4 + DESI DR2 (baseline) | OK |
| 2 | arXiv:2504.07679 — Wolf, García-García, Anton, Ferreira, "Assessing cosmological evidence for non-minimal coupling", PRL 135, 081001 (2025) | VERIFIED |
| 3 | arXiv:2604.16226 — Karam, Sánchez López, Terente Díaz, "Post-Newtonian Constraints on Scalar-Tensor Gravity" (17 Apr 2026) | VERIFIED — covers metric AND Palatini, not Palatini-exclusive |
| 4 | arXiv:2404.03002 — DESI Collab., "DESI 2024 VI: BAO Constraints" (JCAP 2025) | VERIFIED — w0wa CPL, 2.5σ to 3.9σ vs ΛCDM (SN combo dependent) |
| 5 | arXiv:2604.13535 — Bella, Poulin, Vagnozzi, Knox, "Double the axions, half the tension" (15 Apr 2026) | VERIFIED ID — but mission tag "EDE+late-NMC" INCORRECT: paper is 2-field axion EDE, NO non-minimal coupling. Tag corrected. |

## ECI v7.4 reference

ξ_χ = −0.017±0.053 (Levier #1B mean ≈ −3×10⁻⁵, σ ≈ 0.016); H₀ = 70.20±5.74; log B = −1.37 vs ΛCDM (Savage-Dickey); Cassini wall |ξ_χ|(χ₀/M_P)² ≲ 6×10⁻⁶; Jordan frame Faraoni convention −½ ξ_χ R χ².

## 5 × 9 comparison table

(See full table in returned text — 9 columns: Signal / Foundation / H₀,S₈,w(z),σ₈ / Cassini compliance / ECI BETTER / Model BETTER / Graft INTO ECI / Graft FROM ECI / Recommendation)

## Strategic position of ECI's "Cassini-clean wedge"

ECI v7.4 sits in a **structurally distinct corner**: small ξ, Cassini-clean by construction, with arithmetic-modular anchors. It is orthogonal to:
- **Wolf 2025**: algebraically identical −½ξφ²R Lagrangian but ξ ≈ 2.31 (~77,000× larger), relies on Vainshtein fine-tuning
- **Bella et al.**: completely different sector (axion EDE), no NMC
- **DESI CPL**: phenomenological w(z) ansatz, agnostic to field theory
- **Karam et al.**: analytical PPN reference, not a cosmological model

**Honest tension:** ECI's null (log B = −1.37) and Wolf's detection (log B = +7.34) under the algebraically-identical operator cannot both describe the same Universe. The Cassini-clean wedge is defensible iff: (i) ECI reproduces DESI 2.5σ CPL signal at ξ_χ ≈ 0; (ii) Wolf's signal is shown to be screening-fragile; (iii) ECI's arithmetic predictions get external corroboration (DUNE 2030+, Belle-II 2030+).

## Three concrete recommendations

### R1 — GRAFT (low-cost, high-upside): Karam-Palatini analytical PPN as Cassini-wall reference
Cite arXiv:2604.16226 explicit γ(ξ, m_eff, λ_φ) and β analytical expressions to anchor ECI's Cassini bound. Open optional Palatini sub-branch ECI v7.5-P which relaxes the wall and reopens large-ξ contest with Wolf.

### R2 — REFORMULATE (medium-cost, very-high-upside): dual-branch ECI for direct Wolf contest
Add J(φ)X² Galileon kinetic term as optional "ECI-V" sector. Run head-to-head Bayes: ECI-main (ξ_χ ≈ 0, no J) vs ECI-V (ξ_χ free, J(φ)X² active) on Planck PR4 + DESI DR2 + Pantheon+. Decisive in either direction (recovers Wolf → win; fails to recover → falsifies Wolf as Lagrangian-fragile). ~3-4 weeks dev.

### R3 — SKIP (with conditional re-eval): Bella 2-field EDE
Do NOT graft unless the mass ratio φ₂/φ₁ can be predicted from ECI's modular ladder (A14 K=Q(i) / A24 √6-structure). Adding free 2-field EDE without arithmetic anchor re-imports the parameter-explosion critique. Re-evaluate to GRAFT only if A14/A24 ladder predicts mass ratio in (3, 30).

## Key file paths

- /root/crossed-cosmos/notes/eci_v7_aspiration/A4_wolf_eci_structural.md — verified Wolf vs ECI structural comparison
- /root/crossed-cosmos/notes/eci_v7_aspiration/A25_NMC_JAX_ADAPTER/SUMMARY.md — verified ECI v7.4 numerics
- /root/crossed-cosmos/notes/eci_v7_aspiration/V74_AMENDMENT/A28_SUMMARY.md — v7.4 amendment paper context
