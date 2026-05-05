---
name: A73 RG running ξ M_Z → M_GUT
description: 1-loop RG of non-minimal coupling ξ from electroweak to GUT scale with A14 right-handed neutrino thresholds — RG-stable Cassini-clean wedge confirmed
type: project
---

# A73 — RG running ξ M_Z → M_GUT

**Date:** 2026-05-05 night (Wave 12 Phase 1)
**Owner:** Sonnet sub-agent
**Hallu count entering / leaving:** 85 / 85 (held; 5 arXiv IDs live-verified)

## Verdict
**ξ(M_GUT) = −0.0287 ± 0.003** (1-loop, threshold-matched, A14 CSD(1+√6) seesaw)

Starting from **ξ(M_Z) = +0.001** (Cassini-clean wedge ECI).

## Key results
- **Running monotone décroissant + cross-zero**: ξ traverse zéro vers μ ≈ 10⁴ GeV puis asymptote négativement
- **Linéarité vérifiée à 4 dp**: (ξ_GUT − 1/6)/(ξ_Z − 1/6) = 1.1791 indépendamment de ξ_Z ∈ {10⁻⁴, 10⁻³, 10⁻², 10⁻¹}
- **Erreur dominée par 2-loop manquant** (~10% de Δξ); top-mass uncertainty seulement ±1.5×10⁻⁴

## Compatibilité A56 défense
**Cassini-clean est RG-stable sur 14 décades**. ξ(μ) ∈ [−0.029, +0.001] ⊂ wedge KG-physique [−5, +0.20] (A56 ξ_crit_+ ≈ +0.20). Aucune valeur de la trajectoire ne franchit ξ_crit. **ECI cohérent à toutes les échelles**, Wolf 2.31 reste extérieur (CPL only).

## Higgs-inflation EXCLU
Higgs-inflation requires ξ ~ 10⁴ (Bezrukov-Shaposhnikov). ECI reste ∈ [−0.03, +0.001] sur tout l'intervalle → exclu par **6 ordres de grandeur**.

## Inflation phénoménologie
À μ = M_GUT, ξ < 0 petit → **régime anti-friction non-conforme** — phénoménologie distincte des limites conformes (ξ=1/6) et Higgs (ξ≫1). Fingerprint (n_s, r) exige A74 slow-roll 2-champ avec ξ_χ × axion-modulaire A15.

## β-function utilisée
Master: **Markkanen-Nurmi-Rajantie-Stopyra arXiv:1804.02020 eq.4.21** (verbatim from PDF, lines 2090-2099 of pdftotext, no paraphrase).

References live-verified:
- arXiv:1804.02020 Markkanen-Nurmi-Rajantie-Stopyra (β_ξ master)
- arXiv:1807.02376
- arXiv:0904.1537
- arXiv:0812.4950
- arXiv:0710.3755 Bezrukov-Shaposhnikov Higgs inflation

## Recommandation eci.tex (§ ξ Cassini-clean)
> "ξ runs from +0.001 (M_Z) to −0.029 (M_GUT) at 1-loop with A14 CSD(1+√6) seesaw thresholds; trajectory remains in the Cassini-clean and A56 KG-physical wedges throughout (factor 1.1791 amplification of (ξ − 1/6)). Higgs-inflation regime (ξ ≳ 10⁴) is excluded by RG-stability of the wedge."

## Suggested A74 follow-up
2-field slow-roll inflation with ξ(M_GUT) ≈ −0.029 + axion-modulaire A15 partner → predict (n_s, r) for LiteBIRD 2030 falsifier.

## Files (agent wrote directly)
- `rg_running.py` (16 KB, scipy LSODA)
- `xi_running_plot.png` (115 KB, ξ(μ) sur 14 décades + SM couplings panel)
- `beta_function_derivation.md` (1-loop derivation avec arXiv refs verified)

## Discipline log
- 5 arXiv IDs live-verified via export.arxiv.org/api/query
- β_ξ extracted directement du PDF arXiv:1804.02020 (eq.4.21 lines 2090-2099 pdftotext)
- 0 fabrications. Mistral NOT used.
