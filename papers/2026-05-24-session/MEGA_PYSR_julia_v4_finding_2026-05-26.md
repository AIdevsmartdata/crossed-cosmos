---
name: mega-pysr-julia-v4-finding-2026-05-26
description: "🎯 PySR Julia v4 finding 2026-05-26 nuit : κ_EE(N)/dim(G) = 0.4012/N^{9/5} + 0.0071 (loss 7.5e-9). 9/5 = correction finite-N, PAS scaling principal. Asymptote N² avec prefactor 0.0071. Coefficient 0.4012 ≈ 4/π² (1% off — suggestif). β_residual PySR run aussi trouve 4/π². Decoder finding : pas K41 5/3 leading mais N² + N^{-9/5} finite-N correction. Méthodologie DS Bot : inject features, parsimony=0.003, maxsize=25, dimensionless."
metadata: 
  node_type: memory
  type: project
  originSessionId: 74bad51b-2b92-48e2-ba55-e4534c5565f3
---

# MEGA PySR Julia v4 finding 2026-05-26 nuit

## Methodology (per DS Bot guide)

PySR avec Julia backend (fix venv frais /tmp/pysr_fresh), suit guide rigoureux :
- Variables nommées Nv, kv (pas N, k — réservés Julia)
- FEATURES = formes analytiques candidates INJECTÉES (N^{5/3}, N^{9/5}, N^{4/3}, etc.)
- parsimony = 0.003-0.005
- maxsize = 25
- model_selection = 'best'
- Targets DIMENSIONNÉS proprement : κ/dim(G) (per DOF, dimensionless)
- Weights = 1/σ² (passed via fit, not constructor)

## Best find : κ_EE per-DOF decomposition

Run 4 (target = κ/dim(G)) :

```
κ_EE(N) / (N²-1) = 0.40115/N^{9/5} + 0.00707

loss = 7.5e-9 (excellent, complexity 5)
```

Donc :
```
κ_EE(N) = (N²-1) × [0.00707 + 0.40115/N^{9/5}]
        = 0.00707·N² - 0.00707 + 0.40115·(N²-1)/N^{1.8}
```

**Pour N → ∞ : leading = 0.00707·N²** (PAS N^{5/3} ou N^{9/5})

**Le 9/5 apparaît seulement dans la CORRECTION finite-N** subleading.

## Interprétation numerical

| Coefficient | Valeur | Candidate structural |
|-------------|--------|---------------------|
| 0.00707 | asymptote/dof | 1/144 = 1/12² = 0.00694 (diff 2%)<br>1/141 = 0.00709 ★ |
| 0.40115 | finite-N prefactor | **4/π² = 0.4053** (diff 1%) ★<br>or empirical |
| exposant 9/5 | finite-N correction | 9/5 = 1.8 (wave turbulence?) |

## Run 1 (κ_EE direct, simple expressions)

Top complexity 5 : `κ = 0.0139·N^{9/5} + 0.452` (loss 1.5e-5)

Run 1 et Run 4 DIFFÈRENT par target normalization :
- Run 1 (κ direct) trouve N^{9/5} comme leading
- Run 4 (κ/dim_G) trouve N² leading + N^{9/5} correction

**Insight** : N²·constant ≡ scaling 't Hooft large-N counting (κ_EE proportional to # gluons in adjoint), avec correction 9/5 sub-leading.

## Run 2 (residual β = κ - α·N^{5/3})

PySR failed sympy parsing, mais expression suggérée :
```
β ≈ 4/π² - (0.0038)/((log N - 1.88)·√dim_G)
```

Donc β ≈ 4/π² avec correction logarithmique en √dim_G. **Indépendant et cohérent avec Run 4 finding** (4/π² apparaît deux fois !).

## Run 3 (Σ_k premiers)

Pattern PySR : Σ_k ≈ k²·(0.52·log k) avec correction sqrt(k)·0.38.

Mertens-type asymptotic : Σ_k ~ k²/(2 log k) (textbook). PySR récupère cette structure approximativement.

## Implications

### Pour le decoder

1. **Le N^{9/5} n'est PAS le scaling principal** — c'est une correction.
2. **Leading est N²** (free-counting 't Hooft).
3. **Constante 4/π²** apparaît deux fois indépendamment.
4. **Asymptote 0.0071 ≈ 1/144** — à investiguer (1/12² ?)

### Pour SU(15) v2 (en cours)

Prédictions selon PySR formule :
- κ(SU(15)) = 224 · [0.00707 + 0.40115/15^{1.8}] = 224·[0.00707 + 0.00310] = 224·0.01017 = **2.279**
- vs free p=9/5 fit : κ(SU(15)) = 2.277
- vs K41 5/3 : κ(SU(15)) = 2.234

SU(15) discriminera proprement.

## Anti-fab caveats

- Loss 7.5e-9 est très bas mais sur 8 points avec ~3 paramètres effectifs. Risque overfitting.
- 4/π² ≈ 0.4053 vs PySR 0.40115 diff 1%. Could be coincidence.
- 0.0071 reste sans home structural clair.
- Run 3 Mertens recovery confirme PySR fonctionne, mais doesn't prove other findings.

## Action items

1. Verify κ scaling N² au large N — attendre SU(15) v2
2. Test si 0.4012 EST 4/π² avec scan plus large
3. Identifier 0.0071 structurale (1/144 ou autre)
4. Update Paper d_s=3 PRL avec finding "κ → N² leading at large N, with N^{-9/5} correction"

## Author

Kévin Rémondière (ORCID 0009-0008-2443-7166)

## Files

- /tmp/MEGA_PYSR_julia_v4_2026-05-26.py
- /tmp/MEGA_PYSR_v4_results.json
- /tmp/MEGA_v3_results.json (brute force complementary)

## Links

[[CRITICAL_anti_fab_beta_11over24_spurious_2026-05-26]]
[[decoder_BG_HL_fixed_point_2026-05-26]]
[[SESSION_MASTER_FINAL_2026-05-26]]
