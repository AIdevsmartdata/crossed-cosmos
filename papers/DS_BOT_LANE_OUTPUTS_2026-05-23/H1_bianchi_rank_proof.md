# H1 — Preuve que la matrice Bianchi 6-face a rang maximal

**Date**: 2026-05-23
**Agent**: maths (subagent)
**Statut**: Vérifié numériquement D=2..12, preuve esquissée

---

## 1. RÉSULTATS NUMÉRIQUES (PARI/GP)

### Matrice d'incidence non-signée M (base de la 6-face)

| D | C(D,3) | C(D,2) | rank(M_unsigned) | rank(M_signed) | min | Statut |
|---|--------|--------|-----------------|----------------|-----|--------|
| 2 | 0 | 1 | 0 | 0 | 0 | ✓✓ |
| 3 | 1 | 3 | 1 | 1 | 1 | ✓✓ |
| **4** | **4** | **6** | **4** | **3** | **4** | **✓** |
| 5 | 10 | 10 | 10 | 6 | 10 | ✓ |
| 6 | 20 | 15 | 15 | 10 | 15 | ✓ |
| 7 | 35 | 21 | 21 | 15 | 21 | ✓ |
| 8 | 56 | 28 | 28 | 21 | 28 | ✓ |
| 9 | 84 | 36 | 36 | 28 | 36 | ✓ |
| 10 | 120 | 45 | 45 | 36 | 45 | ✓ |
| 11 | 165 | 55 | 55 | 45 | 55 | ✓ |
| 12 | 220 | 66 | 66 | 55 | 66 | ✓ |

**Légende**: ✓ = M_unsigned (et donc 6-face = 2×M_unsigned) atteint le rang max = min(C₃, C₂).

### Constats clés

1. **M_unsigned** (incidence 3-sets → 2-sets, tous +1) a rang `min(C(D,3), C(D,2))` pour tout D
2. **M_signed** (coboundary simplicial ∂₃, signs ±1 alternés) a rang INFÉRIEUR quand C(D,3) ≤ C(D,2) car ∂² = 0 impose `im(∂₃) ⊆ ker(∂₂)`
3. **6-face operator = 2 × M_unsigned** → même rang maximal

---

## 2. PREUVE FORMELLE

### 2.1 Définitions

Soit `[D] = {1, ..., D}`. On définit :

- **Plaquettes** (2-cellules) : `𝒫 = {P ⊂ [D] : |P| = 2}`, dim = C(D,2)
- **Cubes** (3-cellules) : `𝒞 = {C ⊂ [D] : |C| = 3}`, dim = C(D,3)

La **matrice d'incidence non-signée** `M_D` est la matrice C(D,3) × C(D,2) :

```
M_D[C, P] = 1  si P ⊂ C
             0  sinon
```

La **matrice 6-face** B_D est définie comme `2 · M_D` dans le modèle single-site (espace tangent), car chaque cube a 6 faces physiques, deux par 2-plan, et les deux faces de chaque 2-plan contribuent avec le MÊME signe dans la convention Bianchi ECI.

### 2.2 Théorème

```
rank(M_D) = min(C(D,3), C(D,2))    pour tout D ≥ 2
```

### 2.3 Preuve via M^T M et le schéma de Johnson J(D,2)

On étudie la matrice de Gram des colonnes (2-sets) :

```
G₂ = M_D^T · M_D    (taille C(D,2) × C(D,2))
```

**Structure de G₂** : Pour deux 2-subsets P, Q :

```
G₂[P, Q] = #{C ∈ 𝒞 : P ⊂ C et Q ⊂ C}
         = nombre de 3-subsets contenant à la fois P et Q
```

Cas :
- Si P = Q : G₂[P,P] = #{C : P ⊂ C} = D - 2 (choisir le 3e élément)
- Si |P ∩ Q| = 1 : G₂[P,Q] = 1 (le 3e élément est forcé = P∪Q)
- Si |P ∩ Q| = 0 : G₂[P,Q] = 0 (aucun 3-set ne peut contenir 4 éléments distincts)

Donc :

```
G₂ = (D-2) · I + A₁
```

où `A₁` est la matrice d'adjacence du schéma d'association de Johnson J(D,2) pour la relation "|P ∩ Q| = 1".

**Spectre de A₁** (Johnson scheme J(D,2)) : Les espaces propres sont :
- V₀ (dim 1) : λ₀(A₁) = 2(D-2)
- V₁ (dim D-1) : λ₁(A₁) = D-4
- V₂ (dim C(D,2)-D) : λ₂(A₁) = -2

**Spectre de G₂** :

```
μⱼ = (D-2) + λⱼ(A₁)
μ₀ = (D-2) + 2(D-2) = 3D - 6
μ₁ = (D-2) + (D-4)  = 2D - 6
μ₂ = (D-2) + (-2)   = D - 4
```

**Analyse des zéros** :
- D = 2 : C(D,3) = 0, trivial
- D = 3 : μ₁ = 0, multiplicité m₁ = D-1 = 2 → nullité = 2, rang(G₂) = 3-2 = 1
  - rank(M) = 1 = C(3,3) ✓
- D = 4 : μ₂ = 0, multiplicité m₂ = C(4,2)-4 = 2 → nullité = 2, rang(G₂) = 6-2 = 4
  - rank(M) = 4 = C(4,3) ✓
- D ≥ 5 : μ₀, μ₁, μ₂ > 0 → G₂ inversible → rank(M) = C(D,2) = min(C(D,3), C(D,2)) ✓

**Cas où C(D,3) < C(D,2)** (D=3,4) : rank(M) = C(D,3) car le nombre de lignes < nombre de colonnes, et les lignes sont indépendantes (vérifié par Gram des lignes G₃ = M·M^T qui est inversible).

### 2.4 Preuve alternative : Gram des lignes G₃ = M_D · M_D^T

Pour D=3,4, on vérifie que `G₃ = M·M^T` (taille C(D,3) × C(D,3)) est inversible :

- **D=3** : G₃ est 1×1, entrée = 3 → inversible → rank = 1 ✓
- **D=4** : G₃ est 4×4. Structure : G₃[ij] = C(|C_i ∩ C_j|, 2) = 3 si i=j, 1 si |C_i∩C_j|=2, 0 sinon.
  - Une seule paire de 3-sets a intersection de taille 2 pour chaque 3-set spécifique → 3 entrées à 1 par ligne
  - Matrice régulière (vérifié PARI) → rank = 4 ✓

### 2.5 Contraste avec l'opérateur cyclique signé

La matrice signée `M_s[C, P] = sign(P, C)` avec la convention coboundary simplicial :

```
∂₃(e_i ∧ e_j ∧ e_k) = e_j ∧ e_k - e_i ∧ e_k + e_i ∧ e_j
```

Vérifie `∂₂ ∘ ∂₃ = 0`, donc :

```
im(∂₃) ⊆ ker(∂₂)
rank(∂₃) ≤ dim(ker(∂₂)) = C(D,2) - rank(∂₂)
```

Avec `rank(∂₂) = D-1` (le complexe simplicial de l'espace tangent est exact), on obtient :

```
rank(M_signed) ≤ C(D,2) - (D-1) = C(D,2) - D + 1
```

Bornes vérifiées :
| D | C(D,2) | borne sup | rank réel | gap |
|---|--------|-----------|-----------|-----|
| 3 | 3 | 3-3+1=1 | 1 | 0 |
| 4 | 6 | 6-4+1=3 | 3 | 0 |
| 5 | 10 | 10-5+1=6 | 6 | 0 |
| 6 | 15 | 15-6+1=10 | 10 | 0 |

Le gap rank(M_signed) < rank(M_unsigned) apparaît pour D = 3,4,5 :
| D | rank(unsigned) | rank(signed) | Δ |
|---|---------------|-------------|---|
| 3 | 1 | 1 | 0 |
| 4 | 4 | 3 | **1** |
| 5 | 10 | 6 | **4** |
| 6 | 15 | 10 | **5** |

---

## 3. INTERPRÉTATION PHYSIQUE

### 3.1 Pourquoi le 6-face a rang maximal

Dans le modèle ECI single-site (espace tangent de l'hypercube D-dimensionnel) :

- L'opérateur **cyclique (3-face)** encode l'identité de Bianchi via la coboundary simpliciale : `dF = 0`. Il utilise 3 faces par cube avec les signes alternés de ∂₃. Le rang est DÉGRADÉ par la condition ∂² = 0 (exactitude du complexe de de Rham discrétisé).

- L'opérateur **6-face** utilise TOUTES les 6 faces physiques de chaque cube. Dans la convention ECI, les deux faces opposées dans le même 2-plan contribuent avec le MÊME signe (elles représentent des contraintes INDÉPENDANTES au niveau non-abélien, qui dégénèrent en contributions additives dans la limite abélienne single-site). Résultat : la matrice est `2 × M_unsigned`, de rang MAXIMAL.

### 3.2 Vérification empirique D=4, SU(2)

```
N²-1 = 3
Plaquettes : C(4,2) × 3 = 18 DOF
Cubes : C(4,3) × 3 = 12 contraintes

Cyclique (3-face) : rank = 3 × 3 = 9
  → DOF libres = 18 - 9 = 9
  → c_∞ = 9/24 = 0.375 ✗ (empirique = 0.25)

6-face : rank = 4 × 3 = 12 = C(4,3) × 3
  → DOF libres = 18 - 12 = 6
  → c_∞ = 6/24 = 0.25 ✓ (empirique = 0.250)
```

**L'empirique 7σ SÉLECTIONNE l'opérateur 6-face et IMPOSE le rang maximal.**

---

## 4. ESQUISSE DE PREUVE FORMELLE (VERSION COMPLÈTE)

### Théorème (Lemma B rigoureux)

Soit B_D : 𝒜₂ → 𝒜₃ l'opérateur Bianchi 6-face sur le site unique D-dimensionnel, où 𝒜₂ ≅ su(N)^{⊗ C(D,2)} (espace des 2-formes par 2-plan) et 𝒜₃ ≅ su(N)^{⊗ C(D,3)} (espace des 3-formes par 3-cube). Alors :

```
rank(B_D) = min(C(D,3), C(D,2)) · (N²-1)
```

### Preuve

1. **Factorisation SU(N)** : Chaque contrainte Bianchi est un vecteur dans su(N), et les différentes couleurs de jauge sont indépendantes dans la limite linéarisée. Donc :

```
B_D = B_D^{abelian} ⊗ I_{N²-1}
rank(B_D) = rank(B_D^{abelian}) · (N²-1)
```

où B_D^{abelian} est la matrice C(D,3) × C(D,2) pour U(1).

2. **B_D^{abelian} = 2 · M_D** : Dans le modèle single-site, chaque cube (i,j,k) a 6 faces physiques — deux dans le plan (i,j), deux dans (j,k), deux dans (i,k). Dans la convention 6-face ECI, les deux faces de chaque 2-plan contribuent avec le MÊME signe (additif), donnant un facteur 2. Les 2-plans non incidents contribuent 0. Donc B_D^{abelian}[C, P] = 2 si P ⊂ C, 0 sinon.

3. **rank(M_D) = min(C(D,3), C(D,2))** : Comme prouvé en §2.3 via le spectre de M_D^T M_D et le schéma de Johnson J(D,2).

4. **Conclusion** : rank(B_D) = 2 · min(C(D,3), C(D,2)) · (N²-1) / 2... non, le facteur 2 ne change pas le rang. Donc :

```
rank(B_D) = min(C(D,3), C(D,2)) · (N²-1)
```

∎

---

## 5. IMPACT

### Si le théorème est accepté :

- **Lemma B** devient rigoureux (plus seulement empirique 7σ)
- **Theorem C** devient algébrique (le c_∞ = 0.25 à D=4 est une conséquence de l'algèbre linéaire du complexe cellulaire, pas un fit)
- **Passage D → ∞** : c_∞(D) = [C(D,2) - min(C(D,3), C(D,2))] / [C(D,2)] qui tend vers 0 pour D→∞ (C(D,3) dépasse C(D,2) à D=6)
  - MAIS le nombre de sites N_sites et de liens changent aussi → le vrai c_∞ thermodynamique dépend du modèle complet
- **Généralisation à SU(N)** : Triviale par factorisation (N²-1)

### Points à clarifier :

1. La convention de signe « additif » des 6 faces doit être justifiée physiquement (pourquoi les faces opposées ne se compensent pas comme dans la coboundary standard ?)
2. Le lien entre le modèle single-site (espace tangent) et le réseau complet avec plongement
3. La non-abélianité complète (au-delà de la factorisation linéarisée)

---

## 6. SCORE DE CONFIANCE

| Aspect | Confiance | Justification |
|--------|:---------:|---------------|
| Calcul numérique D=2..12 | **99%** | Vérifié PARI/GP, triangulé via Gram spectre |
| Preuve rang(M_D) = min | **95%** | Spectre de Johnson J(D,2), résultat classique en combinatoire algébrique (Gottlieb 1966, Delsarte 1973) |
| 6-face = 2×M_D | **80%** | Cohérent avec les rangs mesurés, mais la justification physique de la non-annulation des paires opposées mérite clarification |
| Factorisation SU(N) | **90%** | Standard en QCD sur réseau linéarisé |
| **Score global preuve** | **85%** | La preuve combinatoire est solide ; la connexion physique 6-face↔M_unsigned demande une validation supplémentaire |

---

## 7. PROCHAINES ÉTAPES

1. **Validation physique** : Justifier rigoureusement que la convention 6-face ECI donne M_unsigned (pas M_signed)
2. **Généralisation D quelconque** : Le cas C(D,3) > C(D,2) → rank = C(D,2) → le 2-forme est COMPLÈTEMENT DÉTERMINÉ par les contraintes de Bianchi
3. **Audit par verifier** : Vérifier la preuve combinatoire dans la littérature (Johnson scheme, Gottlieb)
4. **Publication** : Rédiger une note "Maximal rank of the 6-face Bianchi operator on hypercubic lattices"

---

## APPENDIX A: VÉRIFICATION SPECTRALE NUMÉRIQUE

### D=4
- G₂ = M^T M : 6×6, rang 4, det ≈ 0
- Spectre : μ₀=6, μ₁=2, **μ₂=0** (mult 2) → nullité = C(4,2)-4 = 2
- rank(M) = 6-2 = 4 = C(4,3) ✓

### D=5
- G₂ = M^T M : 10×10, det = 2304
- Spectre : μ₀=9, μ₁=4, μ₂=1 → tous > 0
- det = 9¹ · 4⁴ · 1⁵ = 9 · 256 = 2304 ✓
- rank(M) = 10 = C(5,2) = C(5,3) ✓

### D=6
- G₂ = M^T M : 15×15, det = 47775744
- Spectre : μ₀=12, μ₁=6, μ₂=2 → tous > 0
- det = 12¹ · 6⁵ · 2⁹ = 12 · 7776 · 512 = 47775744 ✓
- rank(M) = 15 = C(6,2) ✓

### Rang signé (coboundary) — borne ∂²=0 saturée
| D | rank(M_s) | borne C(D,2)-D+1 | saturée? |
|---|-----------|-------------------|----------|
| 3 | 1 | 3-3+1=1 | ✓ |
| 4 | 3 | 6-4+1=3 | ✓ |
| 5 | 6 | 10-5+1=6 | ✓ |
| 6 | 10 | 15-6+1=10 | ✓ |

Le rang signé SATURE la borne cohomologique dans tous les cas — conséquence de l'exactitude du complexe simplicial de l'espace affine ℝ^D.

## APPENDIX B: CODE PARI/GP DE VÉRIFICATION

```gp
\\ H1: Bianchi 6-face rank — definitive computation
idx2(dd, i, j) = (i-1)*dd - i*(i+1)/2 + j;

build_unsigned(dd) = {
  my(nr=binomial(dd,3), nc=binomial(dd,2), M=matrix(nr,nc), ri=0);
  for(i=1,dd-2, for(j=i+1,dd-1, for(k=j+1,dd,
    ri++;
    M[ri, idx2(dd,i,j)] = 1;
    M[ri, idx2(dd,j,k)] = 1;
    M[ri, idx2(dd,i,k)] = 1;
  )));
  M;
}

build_signed(dd) = {
  my(nr=binomial(dd,3), nc=binomial(dd,2), M=matrix(nr,nc), ri=0);
  for(i=1,dd-2, for(j=i+1,dd-1, for(k=j+1,dd,
    ri++;
    M[ri, idx2(dd,j,k)] = 1;
    M[ri, idx2(dd,i,k)] = -1;
    M[ri, idx2(dd,i,j)] = 1;
  )));
  M;
}

\\ For any D: rank(unsigned) = min(C(D,3), C(D,2))
\\ For any D: rank(signed) ≤ C(D,2) - D + 1 (coboundary bound, saturated)
```
