---
name: correction-h51-anti-fab-vassilevich-2026-05-26
description: "🚨 ANTI-FAB CATCH H51 : Vassilevich hep-th/0306138 Eq. 4.34 EXPLICIT donne a_4^[tot] = (11/96π²)·∫F·F·K = (1/16π²)·(11/6). Coefficient REEL = 11/6, PAS 11/24. H51 agent's claim 'exact -11/24 = a_4 SD coefficient' était INCORRECT. Lattice β = -11/24 reste numériquement intéressant mais identification structurale NON résolu. P(H51) 65-75% → 25-40%."
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 74bad51b-2b92-48e2-ba55-e4534c5565f3
---

# Correction H51 anti-fab : Vassilevich Eq. 4.34 réelle

## Le fait

Vassilevich hep-th/0306138 §4.2.1 Eq. 4.34 (vérifié texte PDF direct 2026-05-26) :

$$a_4^{[\text{tot}]} = a_4^{[\text{vec}]} - 2 \cdot a_4^{[\text{gh}]} = \frac{11}{96\pi^2} \int_M d^4x \sqrt{g} \, F^{\delta}_{\rho\nu} F^{\gamma}_{\rho\nu} K_{\delta\gamma}$$

Donc per (16π²)⁻¹ normalization : **coefficient = 11/6** (= 11·16/96 = 11/6 ≈ 1.833).

Le ratio 11/6 reproduit la convention textbook **b_0 = 11N/(48π²) = (1/16π²)·(11N/3)·(1/2)** — facteur 2 de Z_g.

## L'erreur H51 agent

L'agent H51 affirmait :

> "After incorporating background-Lorenz spin-projection (DeWitt-Christensen 1976, Vassilevich Eq. 4.41), the universal F² coefficient is Γ_∞^YM|_{F²} = -(1/ε)·(1/16π²)·(11N/24)·∫ tr(F_μν F^μν)"

Le **(11N/24)** était INCORRECT. Le calcul direct de Vassilevich Eq. 4.34 donne **(11/6)·K_δγ** (Killing form, qui pour SU(N) gives K = -2N·δ_ab dans normalization standard).

## Quelle convention donne 11/24 ?

Plausibles :
1. **/4 du replica trick** : EE = (1/4)·a_4 type contribution
2. **/4 dimensional reduction** slab 4D → 3-area
3. **/4 de degeneracy** spinor-vector
4. Confusion entre conventions Euclidean/Lorentz

**Aucun de ces facteurs n'est explicité dans Vassilevich.** L'identification "lattice β = -11/24 = SD a_4 coefficient" reste **NON résolu structurellement**.

## Implications

- H51 STRUCTURAL claim **BRUT** : RÉTROGRADÉ 65-75% → 25-40%
- H51 STRUCTURAL **AFFINÉ** (Kévin 2026-05-26 nuit) : `β = -a_4/4 = -11/24` avec **facteur 1/4 = bulk 4D / surface 2D codim** (réduction dimensionnelle + sign vacuum subtraction)
- Reformulé P(H51 refiné) : **50-65%** sans dérivation 1/4, **70-85%** si Solodukhin uplift dérive le 1/4 explicitement
- Le décodeur reste valide POUR κ_FP = 1/6 (Kostant, vérifié, EXACT) et b_0 = 11N/48π² (Vassilevich 4.34, EXACT)
- Pour β = -11/24 : maintenant **conjecture testable** `β = -a_4_total/4`, pas identité brute

## Pour H58 ancres hétérogènes

| Anchor | Mechanism | Verified |
|--------|-----------|----------|
| κ_FP = 1/6 | Kostant : a_2 SD pour FP vac | ✓ TIER 1 |
| β_YM = -11/24 | ??? (PAS Vassilevich Eq 4.34 brut) | ❌ TIER 3 |
| ξ★ = 2/3 | pôle ζ_Δ pour d_s=10/3 | ❌ d_s mesuré ≈ 2.3-2.5 H60 |
| F∞ = 9/10 | K41 intermittency 1-1/10 | TIER 3 |
| c∞ = 1/4 | Bekenstein area-law | TIER 1 |
| sin²θ_W = 3/13 | empirical / AdS_5/Γ | TIER 4 |

## Why : pour rétention

Anti-fab catch important : NE PAS faire confiance à un agent qui cite une équation sans vérification source. **TOUJOURS** vérifier numérique du coefficient en PDF direct.

L'erreur H51 type "confusion factor 4" est commune en heat kernel literature (différentes conventions /8π², /16π², /96π²). 

Le décodeur spectral REPOSE sur Kostant (κ_FP=1/6 verified) et SU(N) Casimirs (factual). Il NE REPOSE PAS sur Vassilevich Eq 4.34 → -11/24 (faux).

## How to apply

Si un agent prochain claim "exact coefficient X = SD coefficient Y", **TOUJOURS** :
1. WebFetch ou wget arXiv PDF
2. pdftotext + grep numerical value
3. Verifier convention de normalization (16π² ou 4π² ou 96π²)
4. Si pas concordance EXACT, DEMOTE le claim au statut "intéressant numérique mais non structural"

## Author

Kévin Rémondière (ORCID 0009-0008-2443-7166)

## Links

[[H51_seeley_dewitt_minus_11_over_24_2026-05-26]]
[[spectral_decoder_validated_2026-05-26]]
