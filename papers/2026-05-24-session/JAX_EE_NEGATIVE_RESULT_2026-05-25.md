# JAX SU(2) Donnelly-Wall — résultat négatif honnête

**Date** : 2026-05-25 (nuit)
**Contexte** : Attempt B (κ²(SU(2)) = 1/4 = Bekenstein-Hawking) — test lattice EE

## Méthode tentée

Swap-operator Renyi-2 entropy via Metropolis sweep + estimation directe
`⟨exp(-ΔS_swap)⟩` sur 2 réplicas indépendantes.

## Résultat

**Méthode mathématiquement triviale.**

### Preuve

Soit `swap` la bijection (U₁, U₂) ↦ (U₁_swap, U₂_swap) où U₁_swap a les links
de U₂ dans région A et de U₁ dans région B, et inversement pour U₂_swap.

`swap` est une INVOLUTION sur l'espace produit Haar (juste un re-étiquetage de
quels links appartiennent à quel config). Le Jacobien de la mesure de Haar
sous swap = 1.

Donc :
```
Z₂ = ∫ DU₁ DU₂ exp(−S(U₁_swap) − S(U₂_swap))
   = ∫ DU₁' DU₂' exp(−S(U₁') − S(U₂'))    [change of variable]
   = Z₁²
```

Donc S₂(A) = −log(Z₂/Z₁²) = −log(1) = **0**.

### Confirmation empirique

Smoke L=4, β=2.4, 200 samples :
- ⟨ΔS⟩ = −330 ± 47 (std)
- Naïvement ⟨exp(−ΔS)⟩ ≈ exp(+330) ≈ 10¹⁴³ → S₂ ≈ −330 (négatif = absurde)
- Mais en réalité par Jacobien ⟨exp(−ΔS)⟩ = 1 EXACT
- Donc la variance est telle que les events rares (ΔS très positifs) compensent
  exactement les events typiques (ΔS très négatifs)
- C'est le sign/overlap problem dans sa forme la plus violente

## Pourquoi Buividovich-Polikarpov 2008 marche

Leur méthode **n'est PAS le swap de links que j'ai implémenté**.

Ils calculent Z_n sur une géométrie **conifold** où le lattice a une topologie
modifiée (2 sheets gluées le long du plan-frontière). C'est une MODIFICATION
de la topologie du lattice, pas un re-étiquetage de variables.

Concrètement :
- Original : L_x × L_y × L_z × L_t periodic
- Replica n=2 : L_x × L_y × L_z × 2L_t avec identification spéciale au plan
  x = L_x/2 entre les 2 sheets

Cette géométrie n'est pas un quadri-array numpy standard ; elle requiert un
custom lattice topology avec links boundary partagés.

## Alternative : Calabrese-Cardy / Velytsky boundary-condition method

Velytsky 2008 (arXiv:0809.4502) calcule S_n via :
`S_n = (1/(1−n)) log[Z_n / Z_1^n]`

où Z_n est calculé par un **twist** sur les plaquettes boundary entre les n
sheets, pas un swap de configs.

Implementable mais demande modification de l'action sur les plaquettes
boundary — plusieurs heures de coding propre.

## Conclusion

L'overnight JAX que j'ai dispatché ne donnera **pas** le coefficient c
prédit (1/4 si Bekenstein-Hawking). Le job a été **annulé avant launch**
pour éviter de gaspiller 8h GPU sur un estimateur trivialisé.

## Plan pour demain (rested)

1. **Implementer le vrai Donnelly-Wall** via geometry conifold 2-sheets
   (modification de la topologie du lattice)
   OU
2. **Implementer Velytsky boundary-condition method** via twist sur plaquettes
   boundary (plus simple, ~half-day coding)

Les deux nécessitent ~½-1 jour de coding propre + 8-12h compute.

## Attempt B status inchangé

- P(κ²(SU(2)) = 1/4 fondamental) reste **20-30%**
- 7 anchors BH κ-rational + Bayesian boost p~10⁻⁴ inchangés
- Mais **pas de support numérique lattice pour l'instant** (1/4 non testé)
- Falsifiabilité Myers-Perry 5D toujours valide

## Token économie

GPU 8h non gaspillé. Bitcoin/Zenodo/GH déjà persistés (DOI 10.5281/zenodo.20370752).
Pas de regret.

---

**Author** : Kévin Rémondière (ORCID 0009-0008-2443-7166)
**Discipline anti-fab** : reconnaître quand une approche est triviale plutôt
que produire des données qui mèneraient à conclusions fausses.
