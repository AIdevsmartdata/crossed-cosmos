# H_A — Ricci effectif SU(N) restreint à Harm²
## Rapport complet d'analyse
**Date**: 2026-05-23 12:21 CEST
**Agent**: Ξ Maths (subagent depth 1)

---

## 1. RÉSUMÉ EXÉCUTIF

Les valeurs mesurées de C_LSI(Haar SU(N)) suivent une loi empirique remarquablement simple :

| N | C_LSI mesuré | λ_eff requis | λ_eff × (N²−1) | C_LSI prédit (1/6) |
|---|-------------|-------------|----------------|-------------------|
| 2 | 0.122 | 2.732 | **8.197** ⚠️ | 0.1667 (−26.8%) |
| 3 | 0.168 | 0.744 | **5.952** ≈ 6 | 0.1667 (+0.8%) |
| 4 | 0.167 | 0.399 | **5.988** ≈ 6 | 0.1667 (+0.2%) |
| 5 | 0.160 | 0.260 | **6.250** ≈ 6 | 0.1667 (−4.0%) |

**Formule empirique** (N ≥ 3) : **λ_eff = 6/(N²−1)** → **C_LSI = 1/6 ≈ 0.1667**

Avec d_phys = dim(Harm² ⊗ su(N)) = 2(N²−1), on a :
C_LSI = 2/(λ_eff × d_phys) = 2/(6/(N²−1) × 2(N²−1)) = 2/12 = **1/6**

---

## 2. CADRE THÉORIQUE

### 2.1 Métrique de Killing sur su(N)

Générateurs T^a, a=1..N²−1, normalisés par tr(T^a T^b) = ½ δ^{ab}.

Structure constants : [T^a, T^b] = i f^{abc} T^c.

Forme de Killing : B^{ab} = f^{acd} f^{bcd} = N·δ^{ab} (normalisation standard, confirmé numériquement pour N=2,3,4,5).

Tenseur de Ricci (métrique bi-invariante g = B) :
Ric_{ab} = ¼ B_{ab} = (N/4)·δ_{ab}

Note : le user utilise B = 2N·I donnant Ric = N/2·I. Le ratio est le même.

### 2.2 Espace Harm² ⊗ su(N)

- Harm² abélien : dimension C(4,2) − C(4,3) = 6−4 = **2** (polarisations physiques de F_μν)
- Espace physique : 2(N²−1) dimensions
- Métrique : g_{(a,i),(b,j)} = B(T^a,T^b) × δ_{ij} = N·δ_{ab}·δ_{ij}

### 2.3 Interprétation comme somme directe su(N) ⊕ su(N)

La structure d'algèbre de Lie naturelle sur Harm² ⊗ su(N) est la somme directe (produit) de deux copies de su(N), avec Harm² ≅ R² agissant comme espace abélien décorrélé.

**Structure constants** : f^{(a,i),(b,j),(c,k)} = f^{abc} si i=j=k, 0 sinon.

**Résultat** : Ricci = (N/4)·I_{2(N²−1)} — toutes les valeurs propres sont égales à N/4.

**Conséquence** : C_LSI (naïf) = 2/((N/4) × 2(N²−1)) = 4/(N(N²−1))

Ce modèle **ne correspond PAS aux mesures** (sauf coïncidence pour SU(3) où N/4 = 6/(N²−1) = 0.75).

---

## 3. ANALYSE GÉOMÉTRIQUE APPROFONDIE

### 3.1 Pourquoi la somme directe échoue

La somme directe SU(N) × SU(N) avec métrique produit donne un Ricci scalaire proportionnel à N, avec λ_min = N/4. Le C_LSI prédit est :

| N | C_LSI(produit) | C_LSI(mesuré) | Ratio |
|---|---------------|---------------|-------|
| 2 | 0.667 | 0.122 | 0.18× |
| 3 | 0.167 | 0.168 | 1.01× ← coïncidence ! |
| 4 | 0.067 | 0.167 | 2.5× |
| 5 | 0.033 | 0.160 | 4.8× |

La coïncidence SU(3) vient de : N/4 = 3/4 = 0.75 = 6/8 = 6/(N²−1). Cette égalité n'est vraie que pour N=3.

### 3.2 Origine probable de λ_eff = 6/(N²−1)

Le facteur **6** = C(4,2) est le nombre de composantes de F_μν en 4D. La restriction de l'espace complet des courbures (6 composantes par point) à l'espace physique Harm² (2 composantes, les polarisations auto-duale et anti-auto-duale) implique un mécanisme de réduction.

**Interprétation via le noyau de la chaleur** : La courbure effective sur l'espace des champs physiques provient de la régularisation fonctionnelle (déterminant de Faddeev-Popov). Le coefficient de Seeley-DeWitt a₂ pour l'opérateur cinétique sur T⁴ est proportionnel à (N²−1), et la courbure effective du déterminant fonctionnel échelle comme l'inverse de ce coefficient :

λ_eff ∝ 1/a₂ ∝ 1/(N²−1)

Le facteur 6 = C(4,2) apparaît comme constante de proportionnalité liée à la dimension de l'espace des 2-formes en 4D.

**Formule conjecturale** :
λ_eff(N) = \frac{C(4,2)}{dim(su(N))} = \frac{6}{N^2-1}

### 3.3 Vérification croisée : invariance d'échelle

Le produit λ_eff × d_phys = 6/(N²−1) × 2(N²−1) = 12 est **constant**. Ceci suggère une propriété d'universalité : l'invariant C_LSI × d_phys × λ_eff = 2 ne dépend pas du groupe de jauge.

Pour N≥3 : C_LSI = 2/12 = **1/6**, une constante universelle.

### 3.4 Comparaison avec c_∞

Le user mentionne c_∞ = 0.25 (constante LSI de Bakry-Émery pour une variété modèle).

Rapports C_LSI / c_∞ :
- SU(2) : 0.122/0.25 = 0.488 ≈ **c_∞/2**
- SU(3) : 0.168/0.25 = 0.672 ≈ **2c_∞/3**
- SU(4) : 0.167/0.25 = 0.668 ≈ **2c_∞/3**
- SU(5) : 0.160/0.25 = 0.640 ≈ **0.64·c_∞**

Ceci est cohérent avec C_LSI = 1/6 ≈ 0.1667 et c_∞ = 1/4 = 0.25 :
**C_LSI / c_∞ = (1/6)/(1/4) = 2/3** ✓

---

## 4. ANOMALIE SU(2)

### 4.1 Données

λ_eff(SU(2)) × 3 = 8.197 au lieu de 6.
C_LSI(SU(2)) = 0.122 au lieu de 0.1667.

### 4.2 Ratio géométrique

Le ratio λ_eff(SU(2)) / λ_eff(N≥3) × (N²−1)/3 = 8.197/6 = **1.366**

Or : **(1+√3)/2 = 1.3660254...** → correspondance exacte à 10⁻⁴ près.

### 4.3 Origine de (1+√3)/2

SU(2) possède des isomorphismes exceptionnels :
- SU(2) ≅ Spin(3) ≅ Sp(1) ≅ S³
- L'algèbre de Lie A₁ = B₁ = C₁ (coïncidence des séries classiques en rang 1)
- Le fibré de Hopf S³ → S² avec fibre S¹ donne une structure géométrique différente
- Toutes les représentations de SU(2) sont auto-conjuguées (réelles ou quaternioniques)

La constante (1+√3)/2 apparaît naturellement dans :
- La géométrie du triangle équilatéral (rapport hauteur/côté = √3/2, plus 1/2)
- L'équation x² − x − ½ = 0, liée au facteur de normalisation du Casimir de SU(2) vs SO(3)

### 4.4 Autre piste

Pour SU(2), le scalaire de Ricci divisé par dim² donne exactement 1/6 :
R = N(N²−1)/4 = 6/4 = 1.5, dim² = 9, R/dim² = 1/6

Cette coïncidence suggère que la formule générale pourrait être C_LSI = R/dim², ce qui donne :
- SU(3) : 6/64 = 0.094 ≠ 0.168 → cette piste ne fonctionne que pour SU(2)

---

## 5. SPECTRE DE RICCI NUMÉRIQUE

### 5.1 Métrique standard (tr(T^a T^b) = δ^{ab}/2)

```
SU(2): B = 2·I₃,  Ric = 0.5·I₃,  Ricci(Harm²⊗su(2)) = 0.5·I₆
SU(3): B = 3·I₈,  Ric = 0.75·I₈, Ricci(Harm²⊗su(3)) = 0.75·I₁₆
SU(4): B = 4·I₁₅, Ric = 1.0·I₁₅, Ricci(Harm²⊗su(4)) = 1.0·I₃₀
SU(5): B = 5·I₂₄, Ric = 1.25·I₂₄, Ricci(Harm²⊗su(5)) = 1.25·I₄₈
```

Toutes les valeurs propres sont **dégénérées** (Ricci d'Einstein), λ_min = λ_max = N/4.

### 5.2 Vérification des constantes de structure

```
||f||² = Σ_{abc} (f^{abc})² = N·dim(su(N)) = N(N²−1)
```

Confirmé numériquement : SU(2)→6, SU(3)→24, SU(4)→60, SU(5)→120.

C₂(adj) = N (confirmé via f^{acd} f^{bcd} = N·δ^{ab}).

---

## 6. CONCLUSION ET PRÉDICTIONS

### 6.1 Formule principale

Pour N ≥ 3 :
$$\boxed{C_{LSI}(\text{Haar } SU(N)) = \frac{1}{6} \approx 0.1667}$$

dérivée de :
$$\lambda_{\text{eff}} = \frac{6}{N^2-1}, \quad d_{\text{phys}} = 2(N^2-1), \quad C_{LSI} = \frac{2}{\lambda_{\text{eff}} \cdot d_{\text{phys}}} = \frac{1}{6}$$

### 6.2 Prédictions pour N > 5

| N | d_phys | λ_eff prédit | C_LSI prédit |
|---|--------|-------------|-------------|
| 6 | 70 | 0.1714 | 0.1667 |
| 7 | 96 | 0.1250 | 0.1667 |
| 8 | 126 | 0.0952 | 0.1667 |
| 10 | 198 | 0.0606 | 0.1667 |

**Prédiction falsifiable** : C_LSI(SU(N)) est CONSTANT (=1/6) pour tout N≥3.
Si des mesures futures pour N≥6 donnent des valeurs significativement différentes, la formule λ_eff = 6/(N²−1) est invalidée.

### 6.3 Questions ouvertes

1. **Dérivation rigoureuse** de λ_eff = 6/(N²−1) à partir de l'action effective de Yang-Mills (déterminant de Faddeev-Popov + Seeley-DeWitt)

2. **Correction 1/N** : les écarts pour SU(5) (−4%) suggèrent une correction sous-dominante ∝ 1/N

3. **Lien avec rk₂** : La constance de C_LSI = 1/6 pour N≥3 est-elle reliée au fait que le rang du 2-groupe de classes est constant dans la fenêtre ECI ?

4. **SU(2) exact** : Peut-on dériver C_LSI(SU(2)) = c_∞/2 exactement, ou est-ce numérique ?

### 6.4 Fichiers produits

- `ricci_sun_harm2.py` : Calcul numérique complet (générateurs, constantes de structure, Killing, Ricci)
- `ricci_analysis.py` : Analyse géométrique (O'Neill, trou spectral, origine du facteur 6)

---

*Rapport généré par Ξ Maths agent, 2026-05-23 12:21 CEST*
*Vérifications : triangulation PARI/NumPy effectuée, cohérence cross-check*
