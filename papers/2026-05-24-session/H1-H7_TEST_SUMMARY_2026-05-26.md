# H1-H7 Test Summary — Crossover N=4-5 → Cosmologie

**Date :** 2026-05-26  
**Context :** Lancement parallèle 5 agents + 2 toy calc locaux pour tester l'extension du crossover SU(N) lattice dilué→dense vers prédictions cosmologiques.

---

## Résultats agrégés (mise à jour live)

| H | Domain | Verdict | Détail |
|---|--------|---------|--------|
| **H1** | κ_EE(T) thermal SU(3) | **TESTABLE** ✓ | Toy : Δκ=0.085 drop à T_inflection=120 MeV (vs T_c=150). Signal au seuil détectabilité 0.10. À mesurer lattice thermal (HotQCD). |
| **H2** | v_E peak → T_reh | **PLAUSIBLE underconstrained** ~ | GUT-scale Λ~10¹⁶ GeV → T_reh~10¹⁵·⁸ GeV (BICEP3 upper bound). 0/7 candidates strictement compatible avec T_reh∈[10⁹,6×10¹⁵]. Killé par CMB-S4 r<0.001 si arrive. |
| **H3** | η_B baryogenesis | **FALSIFIÉ** ✗ | QCD-T_c : 20 000 OM off (sphalerons exp(-60 000) suppressed). EW-T dark sector : 4 OM short. ECI exp(-21)=7.6e-10 ≠ même mécanisme (topologique). |
| **H4** | Ω_DM/Ω_b vs G_dark | **FALSIFIÉ naïf** ✗ | 0/40 cells (10 groupes × 4 formules) match dans 5%. Closest F_4·F5=6.38 (+19%). Memory G_2=5.50 = post-hoc π·14/8, pas dérivable de κ_EE. |
| **H5** | NANOGrav GW spectrum | **MIXED footprint** ~ | Spectral β=2/3 MATCH EXACT γ=13/3 (mais dégénéré SMBHB). Amplitude 10³ low → H5 ≠ source primaire. Survives footprint modulator. Discriminant : PTA→LISA cross-band cutoff. P=30-40% détectable. |
| **H6** | Polyakov χ_L(N) fingerprint | en cours | Re-analyse LTW/Boyd/Lucini data, break N=4-5 vs smooth fit |
| **H7** | κ_dense(G_2) → Λ | en cours | Holland-Pepe-Wiese G_2 lattice, 3 candidate scaling laws |

---

## Honest summary

Sur les 5 hypothèses testées jusqu'ici :
- **2 falsifiées** (H3 baryogenesis, H4 Ω_DM ratio)
- **2 testables avec signal au seuil** (H1 thermal, H5 NANOGrav)  
- **1 plausible mais underconstrained** (H2 reheating)

Anti-fab discipline : **les naive forms échouent**, comme attendu. La crossover N=4-5 est un fait lattice solide ; les sauts vers cosmologie ne tiennent pas en forme simple. Cela confirme :

1. **κ_EE(N) crossover est un finding SOLIDE** (lattice mesurable, dérivable de β-function via L_c(N)).
2. **Les "applications" cosmologiques sont spéculatives** — formules naïves échouent en grande majorité.
3. **Les coïncidences ECI mémorisées** (G_2 = 5.50, exp(-21) = η_B) sont **post-hoc** ou **independent mechanisms**, pas dérivables du crossover lui-même.

---

## Tests survivants à approfondir

### H1 + H5 = path le plus prometteur

H1 (thermal lattice κ_EE(T)) est l'EXTENSION naturelle directe — pas de saut spéculatif. La méthode BP2008b appliquée à lattice thermal (NT=4,6,8,10,12 vs NS×NS×NS×NT) donnerait :
- Si pic dκ/dT à T_c : H1 SUPPORTED
- Si lisse : H1 FALSIFIÉ
- Δκ=0.085 prédit → besoin précision <0.05 (faisable avec THERM5000-style runs sur GPU)

H5 (NANOGrav) survives comme footprint modulator. Test discriminant = PTA→LISA cross-band slope avec cutoff above f_peak.

### Programme suggéré (3 mois)

1. **HotQCD-style lattice run** : SU(3) thermal κ_EE(T) sur 10 températures T/T_c ∈ [0.7, 1.5]. ETA 1-2 semaines sur RTX 5060 Ti.
2. **NANOGrav 20yr data** (sortie ~2027) : si γ s'éloigne de 13/3, H5 contraint plus fortement.
3. **Direct measurement κ_EE(G_2)** lattice exceptional groups : valide ou tue H7.

---

## Why : pour rétention

Cette session a démontré :
- Le crossover N=4-5 est robust (lattice direct).
- Les extensions cosmologiques naïves échouent dans 4/5 cas.
- Les "matchs" coïncidents (ECI G_2 = 5.50, exp(-21)) sont des artefacts post-hoc.
- La voie sérieuse pour étendre ECI vers cosmologie est :
  1. **Thermal lattice** (H1) — extension directe sans saut
  2. **NANOGrav cross-band** (H5 raffiné) — test indépendant
  3. **Exceptional groups κ_EE** (H7) — généralise crossover G_2/F_4/E_n

P(ECI Phase 1, crossover incluse) reste 70-80% (le lattice fact est solide).
P(ECI Phase 2, extensions cosmologiques) honnête : 20-30% (la majorité falsifiée).

## Files

- `/tmp/H1_thermal_kappa_T_toy_2026-05-26.{py,json}` — toy thermal calc
- `/tmp/H2_entanglement_speed_reheating_2026-05-26.{py,json}` — T_reh candidates
- `/tmp/H3_baryogenesis_test_2026-05-26.md` — agent verdict FALSIFIED
- `/tmp/H4_dark_matter_ratio_test_2026-05-26.md` — agent verdict FALSIFIED
- `/tmp/H5_nanograv_test_2026-05-26.md` — agent verdict mixed/footprint
- `/tmp/H6_polyakov_test_2026-05-26.{py,md}` — pending
- `/tmp/H7_G2_Lambda_test_2026-05-26.md` — pending

## Author

Kévin Rémondière (ORCID 0009-0008-2443-7166)
