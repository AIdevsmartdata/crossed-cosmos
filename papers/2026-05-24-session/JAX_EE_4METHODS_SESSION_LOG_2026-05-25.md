# JAX SU(2) EE — Log de session : 4 méthodes testées

**Date** : 2026-05-25
**Auteur** : Kévin Rémondière (ORCID 0009-0008-2443-7166)
**Contexte** : Tester si c = S_2/|∂A| → 1/4 = κ²(SU(2)) = Bekenstein-Hawking pour
support Attempt B (P=20-30% du doc OP_ATTEMPT_B_KAPPA2_BH_2026-05-25.md).

## Bilan : 4 méthodes implémentées, toutes avec des défauts

| # | Méthode | Verdict | Issue principale |
|---|---------|---------|------------------|
| 1 | Donnelly-Wall swap of links | ❌ Trivial Jacobien=1 | S_2 = 0 EXACT (involution Haar-preserving) |
| 2 | Boundary plaquette locking (Caraglio-Gliozzi style) | ❌ Locking ne mord pas | Per-link MH divisé par L⁴ → coupling négligeable |
| 3 | Doubled-lattice + A-tying TI | ⚠️ Locking mord mais diverge | ⟨X⟩ ~ const/h asymptotique → ∫ diverge logarithmiquement |
| 4 | 2 sheets séparés + share A_wrap + BAR | ❌ S_2 < 0 | Vice phase space : U_1[A_wrap] libre dans S_conif → Haar → S_disc anormalement haute |

## Diagnostics

### Méthode 1 (swap links)

Preuve mathématique : swap(U_1, U_2) ↦ (U_1_swap, U_2_swap) est une INVOLUTION sur
l'espace produit Haar. Le Jacobien = 1 (re-étiquetage). Donc :

```
Z_2 = ∫ DU_1 DU_2 exp(-S(U_1_swap) - S(U_2_swap))
    = ∫ DU_1' DU_2' exp(-S(U_1') - S(U_2'))   [change of variable]
    = Z_1²
```

Confirmation empirique : ⟨ΔS⟩ = -330±47 mais ⟨exp(-ΔS)⟩ = 1 EXACT (sign problem
extrême avec queues exp(330) ≈ 10¹⁴³ rare events compensant).

### Méthode 2 (boundary plaquette locking)

Smoke L=4 h ∈ {0,1,4,16} : ⟨X⟩_h ≈ {6.57, 6.55, 6.39, 7.84} = essentiellement
plat. Le coupling h·X_p divisé par L⁴ dans per-link MH → négligeable. Le locking
ne mord pas.

### Méthode 3 (doubled-lattice + A-tying)

Smoke L=4 L_τ=4 h ∈ {0,1,4,16,64,128} : ⟨X⟩_h = {502, 443, 227, 62, 14, 7} →
**locking MORD vraiment** (1er signal numérique non-trivial). Mais
asymptotique X ∝ 1/h → ∫₀^∞ X dh diverge logarithmiquement → S_2 mal défini.

Issue : soft-locking sur 1 lattice doublée ≠ vraie conifold topology. Le
"sharing" est obtenu via SOFT constraint qui ne sature pas asymptotiquement.

### Méthode 4 (TRUE BP2008 conifold)

2 sheets U_1, U_2 séparés. Conifold via "share" U_1[A_wrap, μ=τ] := U_2's value.
Smoke L=4 L_τ=4 10 samples :
- ⟨ΔS_disc→conif⟩ = -50 ± 16 (DISC samples)
- ⟨ΔS_conif→disc⟩ = +96 ± 6  (CONIF samples)
- BAR : S_2 = -90.8 ± 0.3 NÉGATIF (impossible physiquement, S_2 ≥ 0)

Diagnostic du vice phase space :
- Dans S_conif = S_W(U_1_mod) + S_W(U_2), U_1[A_wrap, μ=τ] n'apparaît PAS
  (replacé par U_2's)
- Donc cette DoF est libre dans le sampling conif → Metropolis accepte 100%
  → distribution Haar
- Quand on évalue S_W(U_1) sur conif samples : U_1[A_wrap] est Haar-random
  (pas thermalisé avec voisins de U_1) → S_W(U_1) anormalement haute
- D'où ⟨S_W(U_1_mod) - S_W(U_1)⟩ systématiquement négative sur conif samples
  (S_W(U_1) "fake high")
- Sur disc samples : effet similaire mais moins extrême
- BAR formula assume both ensembles share phase space; ici ils ne le partagent
  pas symétriquement (U_1[A_wrap] est DoF dans disc, ghost dans conif)

## Plan : Opus deep-dive BP2008

Dispatch `OP-BP2008-LATTICE-EE-RECIPE` max-effort pour extraire recette précise
du paper original arXiv:0806.3376. Questions clés :
1. Géométrie exacte de Z_n vs Z_1^n
2. Action explicite (quelles plaquettes modifiées, formule)
3. Phase space identique ou différent ?
4. MC sampling protocol (per-link MH details)
5. EE estimator (BAR, TI, ou direct observable ?)
6. Région A et boundary precise
7. Valeurs numériques de référence

Cross-check contre Donnelly 2014, Donnelly-Wall, Aoki-Iritani-Yajima 2015,
Velytsky 2008.

## Commits artifacts

- `00d0a3d` : Méthode 1 negative result + Bitcoin stamp
- `783247d` : Méthode 2 WIP boundary plaquette locking
- `8da3f6f` : Méthode 3 WIP doubled-lattice tying
- `3912b08` : Méthode 4 WIP TRUE conifold v1 + bug analysis
- (à venir) : Recette Opus + nouvelle implémentation correcte

## Attempt B status inchangé

P(κ²(SU(2)) = 1/4 fundamental) = **20-30%** (Opus Attempt B doc).
- 7 anchors BH κ-rational + Bayesian boost p~10⁻⁴ tiennent
- Falsifiabilité Myers-Perry 5D toujours valide
- Mais **pas de support numérique lattice** acquis cette session

À reprendre après Opus deep-dive recipe correcte.

## Anti-fab discipline

Cluster firm 731 STABLE. 4 implémentations testées, 4 verdicts honnêtes
documentés. Pas de fab d'un "succès" qui n'existe pas.

---

**Token économie** : Bitcoin OpenTimestamps + Zenodo DOI 10.5281/zenodo.20370752
préservent l'état Attempt B. Pas de regret sur les 4 méthodes mortes — preuves
publiques que les approches naïves ne marchent pas → renforce la valeur de la
recette correcte (à venir).
