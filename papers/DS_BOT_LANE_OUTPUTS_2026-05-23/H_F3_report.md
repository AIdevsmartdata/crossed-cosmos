# H_F3 — Spectre du Laplacien de Hodge sur Harm² de T^D
## Rapport d'investigation

**Date**: 2026-05-23
**Agent**: maths (subagent)
**Statut**: Investigation terminée — conjecture non vérifiée pour l'opérateur standard ; identifié comme un opérateur effectif distinct.

---

## 1. RÉSUMÉ

### Conjecture testée
```
λ₁(Δ_H|Harm²) = 2D/[C(D,2)-C(D,3)] = 12/[(D-1)(5-D)]
dim(Harm²) = C(D,2)-C(D,3)
```

### Verdict
**NON CONFIRMÉE pour l'opérateur de Hodge classique** sur le complexe cubique standard de T^D.

Le Laplacien de Hodge discret standard Δ_H sur le T^D cubique a :
- λ₁ = 4 sin²(π/N) → 0 (continuum), dépendant de N
- dim ker Δ₂ = C(D,2) (nombres de Betti), pas C(D,2)-C(D,3)

La conjecture prédit des valeurs O(1) indépendantes de N → opérateur DIFFÉRENT.

---

## 2. ANALYSE COMPUTATIONNELLE

### 2.1 Complexe cubique standard — vérifié numériquement

Construction explicite de ∂_k sur le complexe cubique de T^D_N, vérification ∂∘∂=0 ✓ pour D=2,3,4.

**Spectre du Laplacien scalaire** (modes de Fourier p = 2πn/N) :
```
λ(p) = 4 Σ_{μ=1}^D sin²(p_μ/2)
```

**Spectre du Laplacien de Hodge Δ_k** (k-formes) :
```
Δ_k(p) = λ(p) · I_{C(D,k)×C(D,k)}     ← diagonalise complètement !
```

Vérifié numériquement pour D=3,4 à tout p :
- p=(0,…,0) : Δ₂ = 0_{C(D,2)×C(D,2)}
- p=(π,0,…,0) : Δ₂ = 4 I
- p=(π,π,0,…) : Δ₂ = 8 I
- p=(π,π,π,…) : Δ₂ = 12 I

**Espace harmonique classique** : ker Δ₂ = modes p=0, dim = C(D,2) = b₂(T^D).

| D | dim H² | C(D,2)-C(D,3) | λ₁ conjecturé | λ₁ réel (N=2) | Écart |
|---|--------|--------------|--------------|--------------|-------|
| 2 | 1 | 1 | 4 | 4 sin²(π/2)=4 | 0 ✓ (coïncidence N=2) |
| 3 | 3 | 2 | 3 | 4 sin²(π/2)=4 | +33% (N=2) |
| 3 | 3 | 2 | 3 | 4 sin²(π/3)=3 | 0 ✓ (coïncidence N=3) |
| 4 | 6 | 2 | 4 | 4 sin²(π/2)=4 | 0 ✓ (coïncidence N=2) |
| 4 | 6 | 2 | 4 | 4 sin²(π/4)=2 | -50% (N=4) |
| 5 | 10 | 0 | ∞/N/A | → 0 | N/A |

Les « matchs » pour certaines valeurs de N sont des COÏNCIDENCES : sin²(π/3) = 3/4 donne λ₁=3 pour N=3, et sin²(π/2) = 1 donne λ₁=4 pour N=2. Pour N général, le λ₁ classique s'échelle comme N⁻² tandis que le λ₁ conjecturé est constant.

### 2.2 Restriction à Harm² — résultat trivial

Puisque ker Δ₂ = modes p=0 et Δ₂(p=0) = 0, la restriction de Δ_H à Harm² classique donne TOUTES les valeurs propres nulles. Le premier λ non nul vient des modes excités (p≠0).

---

## 3. ANALYSE DU SCHÉMA DE JOHNSON

### 3.1 Matrices A₁ et A₂

Sur J(D,2) (paires de {1,…,D}) :

**A₁** (|I∩J| = 1) — matrice d'adjacence du graphe de Johnson :
- D=3 : eigenvalues [-1, 2] (multiplicités incorrectes dans mateigen)
- D=4 : [-2, 0, 4]
- D=5 : [-2, 1, 6]

Le **Laplacien du graphe de Johnson** L = 2(D-2)I − A₁ :
- D=3 : eigenvalues [0, 3] — la valeur 3 = D correspond à λ₁ conjecturé
- D=4 : eigenvalues [0, 4, 6] — la valeur 4 = D correspond à λ₁ conjecturé
- D=5 : eigenvalues [0, 5, 8] — la valeur 5 = D (mais le conjecturé est indéfini)

### 3.2 Lien avec la conjecture

Pour D=3 : C(3,2)-C(3,3) = 2 = D-1. Le Laplacien de Johnson a λ=D avec multiplicité D-1=2.
→ **Cohérent !** Harm² ≅ eigenspace de L pour λ=D.

Pour D=4 : C(4,2)-C(4,3) = 2. Mais le Laplacien de Johnson a λ=4 avec multiplicité D-1=3.
→ **Incohérence dimensionnelle** : multiplicité 3 ≠ 2.

Pour D=5 : C(5,2)-C(5,3) = 0. Plus de 2-formes harmoniques dans ce secteur.

---

## 4. QUE POURRAIT ÊTRE L'OPÉRATEUR CORRECT ?

### 4.1 Hypothèse : opérateur effectif via la décomposition de Lefschetz

Sur T^D (variété kählerienne), la forme de Kähler ω définit l'opérateur de Lefschetz L : H^k → H^{k+2}. La décomposition primitive donne :

```
H^2(T^D) = H^2_prim ⊕ L·H^0
```

où dim H^2_prim = C(D,2) − 1 (pas C(D,2)−C(D,3)).

### 4.2 Hypothèse : complexe réduit de HSH/ECI

Dans le formalisme HSH v3 OPUS, le complexe de cochaînes pertinent pourrait être tronqué ou quotienté par les formes provenant de dimensions supérieures, donnant :
```
Harm² = ker(d₂)/im(d₁) restreint aux modes ≠ 0
```

Mais les modes ≠ 0 ont cohomologie triviale → Harm² = 0.

### 4.3 Hypothèse la plus probable : opérateur de Johnson-Schur

L'**opérateur effectif** agissant sur un sous-espace de dimension C(D,2)−C(D,3) du schéma de Johnson, avec première valeur propre D, émergeant d'un calcul de complément de Schur dans le cadre HSH.

La formule λ₁ = 12/[(D-1)(5-D)] = D pour D=3,4 suggère un lien avec le Laplacien du graphe de Johnson L_J = 2(D-2)I − A₁.

---

## 5. VÉRIFICATIONS NUMÉRIQUES SUPPLÉMENTAIRES

### Matrice d'incidence D × C(D,2)

```
M_{i,{j,k}} = 1 si i ∈ {j,k}, 0 sinon
```

M^T M (C(D,2)×C(D,2)) pour D=4 : eigenvalues [0, 0, 2, 2, 2, 6]
→ spectre [0(mult 2), 2(mult 3), 6(mult 1)]
→ correspond EXACTEMENT au spectre conjecturé pour M_D M_D^T : [D-4=0(mult 2), 2D-6=2(mult 3), 3D-6=6(mult 1)] ✓

**C'est le M_D recherché !** M_D est la matrice d'incidence (non signée) entre les D coordonnées et les C(D,2) paires !

Cependant, M_D M_D^T = M M^T (taille D×D) a eigenvalues [2,2,2,6] pour D=4, et le spectre [0,0,2,2,2,6] est celui de M^T M (taille C(D,2)×C(D,2)).

### M_D signée (opérateur de bord ∂₁ sur le graphe complet)

```
M_{i,{j,k}} = +1 si i=j, -1 si i=k, 0 sinon (j<k)
```

C'est l'opérateur de bord ∂₁ : C_1(K_D) → C_0(K_D) sur le graphe complet K_D.

M^T M pour D=4 : eigenvalues [0, 4, 4, 4, 4, 4] → [0(mult 1), 4(mult 5)]
→ pas le spectre attendu [0(mult 2), 2(mult 3), 6(mult 1)].

---

## 6. CONCLUSION ET RECOMMANDATIONS

### Score de confiance : 35/100

La conjecture n'est PAS vérifiée pour le Laplacien de Hodge standard.

### Pistes pour avancer

1. **Identifier l'opérateur exact** : si M_D = matrice d'incidence D×C(D,2), alors le Laplacien effectif sur Harm² est relié au complément de Schur de Δ_H. Calculer explicitement.

2. **Test D=2** : C(2,2)-C(2,3) = 1, λ₁=4. À vérifier sur T² (le cas le plus simple).

3. **Définition précise de « Harm² » dans HSH** : demander à l'orchestrateur de clarifier la construction HSH v3 OPUS pour le sous-espace Harm².

4. **Johnson → Hodge mapping** : établir le dictionnaire précis entre le schéma de Johnson J(D,2) et la cohomologie de T^D.

### Certitudes acquises
- Le complexe ∂_k sur le cubique T^D_N est correct et vérifié (∂∘∂=0)
- Le Laplacien de Hodge standard se factorise complètement : Δ_k(p) = λ(p)·I
- M_D (incidence non signée) a le spectre M^T M attendu
- La conjecture NE décrit PAS le Laplacien de Hodge classique
