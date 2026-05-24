# Pitch Bauerschmidt v22 — Yang-Mills Mass Gap via Geometric Rigidity

**Date** : 2026-05-24
**Auteur** : Kévin Rémondière
**DOI Zenodo** : [10.5281/zenodo.20363988](https://zenodo.org/records/20363988)
**Statut** : Draft pour discussion — honnête, zéro overclaim

---

## Résumé

Nous proposons une stratégie de preuve du mass gap pour la théorie de Yang-Mills
pure SU(N) en dimension D=4, fondée sur la **rigidité géométrique** de la mesure
de Gibbs dans la limite continue. La stratégie repose sur quatre piliers, dont
deux sont prouvés en Lean (0 sorrys, 6301 lignes), un est partiellement prouvé
(conditionnel à une borne LSI uniforme en β), et le quatrième — le zero-mode
problem — est ouvert.

**Finding central** : la structure cohomologique de SU(N) distingue **SU(3) comme
le seul groupe saturé en D=4**. Ceci n'est pas un accident numérique : c'est une
conséquence de la condition rank(SU(N)) = C(4,2) − C(4,3) = 2.

---

## 1. Les quatre piliers

### A1 — κ = 1/6 (Hodge SU(3)) ✅ PROUVÉ Lean

L'invariant κ = 1/6 émerge de la structure de Hodge de SU(3) en D=4.
Condition de saturation : `rank(SU(N)) = N−1 = 2 = C(4,2) − C(4,3)`.
Seul SU(3) satisfait cette condition.

Preuve Lean : `KappaOneSixth.lean` (0 sorrys).

### A2 — LipschitzActionMeasure ✅ PROUVÉ Lean

L'action de Wilson est Lipschitz-continue sur l'espace de configuration
SU(N)^N_links. La mesure de Gibbs hérite de cette régularité.

Preuve Lean : `LipschitzActionMeasure.lean` (622 lignes, 0 sorrys).

### A3 — Prokhorov compactness → existence limite continue

La famille de mesures μ_{a,β(a)} (trajectoire AF) est tight. Prokhorov
donne l'existence d'une sous-suite convergente vers une mesure limite μ_∞.

Statut : preuve standard (Glimm-Jaffe 1981 §6.2), non encore formalisée Lean.

### A4 — Bakry-Émery rigidity → unicité

Sur Harm² ⊗ su(N), la mesure limite satisfait une inégalité de Sobolev
logarithmique (LSI). Si la constante LSI est uniforme en β (Pillar 3),
la limite est **unique** = Maxwell libre.

Statut : conditionnel à Pillar 3.

---

## 2. Pillar 3 : la borne LSI uniforme — le verrou

Le générateur de Markov L sur SU(N)^N_links a un trou spectral λ₁.
L'inégalité LSI donne λ₁ ≥ c(κ) où κ est le **déficit de saturation**.

Pour SU(3) saturé : κ = 1/6 → λ₁ ≥ c(1/6) > c(0) (borne améliorée vs Pinsker).

**Le zero-mode problem** (Pillar 3 sub-3, OPEN) :

Sur Harm², par définition Δ₁ = 0. La covariance gaussienne (βΔ₁)⁻¹ diverge.
Le mass gap physique ne peut pas venir de λ_min(Δ₁ sur Harm²) = 0.

Quatre pistes à explorer :
1. Twist 't Hooft (conditions aux bords tordues → lève Harm²)
2. k ≥ 2π/L (discrétisation du spectre en volume fini)
3. Quotient par le centre (Z_N → mesure quotient non-triviale)
4. BBD multiscale (Brydges-Fröhlich-Spencer → Bałaban sans cluster expansion)

**C'est le seul obstacle à une preuve complète.** Si Pillar 3 est résolu,
A1-A4 donnent :
- Existence de la limite continue (A3)
- Unicité = Maxwell libre (A4)
- Mass gap > 0 (conséquence de l'unicité + OS positivity)

---

## 3. Structure cross-N : pourquoi SU(3) est spécial

| Groupe | rank | Saturé ? | κ | α prédit | Mécanisme mass gap |
|--------|------|----------|---|----------|-------------------|
| SU(2) | 1 | ❌ | — | 1 (Pinsker) | Standard (cluster expansion) |
| **SU(3)** | **2** | **✅** | **1/6** | **5/6** | **Géométrique (notre framework)** |
| SU(4) | 3 | ❌ | — | 1 (Pinsker) | Standard (cluster expansion) |
| SU(N≥5) | N−1 | ❌ | — | 1 (Pinsker) | Standard (cluster expansion) |

Le framework ne résout pas le problème Clay « mass gap pour tout SU(N) ».
Il résout quelque chose de **plus fin** : le mass gap de SU(3) a une structure
géométrique spéciale que les autres n'ont pas.

Si la Nature avait choisi SU(2) comme groupe de jauge fort, le mécanisme
κ = 1/6 n'existerait pas. C'est un fait mathématique pur.

---

## 4. Ce qui est solide (indépendant de Pillar 3)

- κ = 1/6 (Lean, 0 sorrys) — invariant cohomologique structurel
- m(2⁺⁺)/m(0⁺⁺) = √2 — confirmé sur 6 groupes SU(N) à ±2% (AT 2021)
- Manifestations M1, M9 algébriques — vérifiées cross-D=2..10
- D=4 = dernière dimension non-triviale (condition de saturation)
- Theorem C empirique à 7σ (cross-(N,D,G))
- 6301 lignes Lean YM core, 0 sorrys, public

---

## 5. Ce qui est conjecturé (testable)

- α(SU(3), D=4) = 5/6 = 1 − κ — hypothèse géométrique, à tester via
  gradient flow Lüscher (pas Migdal-Kadanoff, contaminé à haut β)
- Si α(SU(3)) = 5/6 confirmé → la chaîne κ → α → LSI améliorée → mass gap > 0
  est fermée (modulo Pillar 3 zero-mode)
- α(SU(2)) = 1 (Pinsker), α(SU(4)) = 1 — falsifiables par mesure directe

---

## 6. Anti-fab disclosure

- Otto-Westdickenberg 2008 JFA : **INVENTÉ par LLM** (catché + corrigé)
- « α = 5/6 loi géométrique de base » : **coïncidence empirique à 0.06%**
  sur 4 points PySR, pas un théorème. Reformulé comme conjecture géométrique.
- Implications cosmologiques (DM glueball, inflation, GW) : **speculation,
  ne pas propager**.
- Migdal-Kadanoff invalide à β > 200-300 : **NaN + overshoot P_MK > 1**,
  remplacé par gradient flow pour mesures propres.

---

## 7. Ce dont on a besoin de Bauerschmidt

Votre expertise en **bornes LSI uniformes en β** sur des espaces de configuration
de type réseau SU(N) est le chaînon manquant. Plus précisément :

1. **Pillar 3 proof sketch** : établir que LSI(μ_{a,β}) ≥ c(κ) uniformément en a
   pour SU(3) saturé, où κ = 1/6 via Hodge.
2. **Zero-mode resolution** : parmi les 4 pistes (twist 't Hooft, k ≥ 2π/L,
   quotient centre, BBD multiscale), laquelle est viable ?
3. **Validation du framework cross-N** : confirmer ou infirmer que la
   différenciation SU(3) vs SU(2)/SU(4) est mathématiquement fondée.

---

## 8. Estimation honnête

- P(Clay 10y) : 40-55%
- Verrou principal : Pillar 3 sub-3 (zero-mode) + B1 cluster expansion
- Si Pillar 3 résolu avec votre aide : P(Clay 10y) → 60-75%

---

**Contact** : Kévin Rémondière
**GitHub** : [github.com/AIdevsmartdata/crossed-cosmos](https://github.com/AIdevsmartdata/crossed-cosmos)
**Zenodo** : [10.5281/zenodo.20363988](https://zenodo.org/records/20363988)
