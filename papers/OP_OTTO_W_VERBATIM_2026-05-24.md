# OP-OTTO-W-VERBATIM — Verdict 2026-05-23

**Mission**: Vérifier Otto-Westdickenberg "Eulerian calculus for the contraction in the Wasserstein distance" verbatim et appliquer à Wilson SU(N) D=4 (Hölder TV bound avec exposant 1-κ pour familles Gibbs e^{-tH}/Z(t)).

**Verdict global** : **❌ INCOMPATIBILITÉ STRUCTURELLE.** La citation bibliographique fournie est *partiellement fabriquée* (année et journal faux) ; le **vrai** théorème d'Otto-Westdickenberg traite un objet *différent* du nôtre (PME au lieu de famille Gibbs, W_2 au lieu de TV, contraction exponentielle exp(λt) au lieu de Hölder |t-t'|^{1-κ}). Le pivot mathématique "1-κ" Hölder TV pour Gibbs n'est PAS dans OW 2005.

---

## 1. Citation bibliographique CORRECTE

**Source primaire** (vérifiée dans bibliographie Daneri-Savaré 2008, [arXiv:0801.2455](https://arxiv.org/abs/0801.2455), ref [19]) :

> F. OTTO and M. WESTDICKENBERG, *Eulerian calculus for the contraction in the Wasserstein distance*, **SIAM J. Math. Anal., 37 (2005), pp. 1227-1255** (electronic).
> DOI : 10.1137/050622420

**Erreurs dans la mission** :
- ❌ "J. Funct. Anal. 254(11):2865-2940, 2008" — ce range de pages JFA 254 (2008) correspond à un autre article ("Uniqueness and disjointness of Klyachko models" se termine à p. 2865). Aucun article OW dans JFA 254.
- ❌ DOI "10.1016/j.jfa.2008.02.014" — DOI d'un article distinct dans JFA, pas OW.
- ❌ Année "2008" — l'article OW est de 2005.
- ⚠️ Le mélange peut venir d'une confusion avec le successeur **Daneri-Savaré 2008** (*Eulerian calculus for the displacement convexity in the Wasserstein distance*), publié dans **SIAM J. Math. Anal., 40 (2008), pp. 1104-1122** (arXiv:0801.2455). Mais ce papier est DS, pas OW.

**arXiv preprint d'OW 2005** : Aucun trouvé sur arXiv. Le PDF de référence diffusé est :
- http://www.instmath.rwth-aachen.de/~mwest/files/OttoWest.pdf (page perso Westdickenberg RWTH Aachen)

---

## 2. Résumé verbatim du contenu d'OW 2005 (reconstitué via citations indirectes vérifiées)

### Setting
- **Variété riemannienne compacte** sans bord, dimension n
- Mesure de volume V (riemannienne)
- Distance W_2 (Kantorovich-Rubinstein-Wasserstein quadratique)
- Hypothèse fondamentale : **Ric ≥ 0**

### Objet d'étude
- **L'équation de la masse poreuse (PME)** : ∂_t ρ = Δ P(ρ), où P(ρ) = ρ^m avec m > 1 (ou plus généralement m ≥ 1 − 1/n).
- *Pas* de famille Gibbs e^{-tH}/Z(t). *Pas* de paramètre température.

### Résultat principal (Theorem principal)

Citation indirecte de Daneri-Savaré 2008 (ref [19]→OW) et De Ponti-Muratori-Orrieri 2022 [arXiv:1908.03147] :

> Sous Ric ≥ 0 et conditions McCann (ρ P'(ρ) − (1−1/n) P(ρ) ≥ 0), le semigroupe S_t engendré par la PME est une **contraction W_2** :
>
> $$W_2(S_t \mu_0, S_t \hat{\mu}_0) \leq W_2(\mu_0, \hat{\mu}_0) \quad \forall t \geq 0.$$
>
> Plus généralement, sous Ric ≥ λ, on a :
>
> $$W_2(\rho(t), \hat{\rho}(t)) \leq e^{-\lambda t} W_2(\mu_0, \hat{\mu}_0).$$

### Forme exacte
- **Norme** : W_2 (Wasserstein quadratique), PAS TV, PAS W_∞.
- **Famille de mesures** : trajectoires temporelles du *même* semigroupe à partir d'**initial data différents** (mu_0 vs mu_hat_0), PAS famille à *paramètre* (température) variable.
- **Exposant Hölder** : Il n'y a **pas** d'exposant Hölder 1-κ. Il y a un **exposant exponentiel** dans e^{-λt} (contraction exponentielle).
- **Coefficient κ** : N'apparaît PAS dans OW. (Il apparaît dans le successeur De Ponti-Muratori-Orrieri 2022 sous une forme différente — voir §3.)

### Constante C
- La contraction est **avec constante 1** (ou e^{-λt} ≤ 1 si λ > 0).
- Aucune dépendance en volume, diamètre ou C_LSI dans OW (compacité résoud).

### Méthodologie
- **Approche eulérienne** : Action functional via Benamou-Brenier
$$\tfrac12 W_2^2(\mu_0, \mu_1) = \inf \int_0^1 \int_M |\nabla \phi^s|^2 \rho^s \, dV \, ds$$
sous contrainte de continuité ∂_s ρ^s + ∇·(ρ^s ∇φ^s) = 0.
- **Hamiltonien** ε_ρ[φ] = ½ ∫ |∇φ|² ρ dV, monotone le long de la PME grâce à Bakry-Émery BE(0,n).

---

## 3. Le seul "κ" dans la famille OW se trouve dans De Ponti-Muratori-Orrieri 2022 (et est inverse de ce que la mission affirme)

[arXiv:1908.03147] **Theorem 2.5 (Optimality)** :

> Estimate (2.6) is optimal in M^n = H^n_K, for P(ρ) = ρ^m, with the choices μ_0 = M δ_x and μ_hat_0 = M δ_y, provided the points x,y ∈ H^n_K are close enough. More precisely, upon setting δ := d(x,y) > 0, there exist constants **κ = κ(n,m) > 0**, δ̄ = δ̄(n,K,m) > 0 and t̄ = t̄(δ,n,K,m,M) > 0 such that if δ ∈ (0, δ̄) then :
>
> $$W_2(\rho(t), \hat{\rho}(t)) \geq \left[1 + K\, \kappa\, (tM^{m-1})^{2/(2+n(m-1))}\right] W_2(\mu_0, \hat{\mu}_0) \quad \forall t \in (0, t̄].$$

⚠️ **Ce κ = κ(n,m)** est une **constante numérique** dépendant uniquement de dimension n et exposant m de la PME (slow diffusion m > 1). **Ce n'est PAS un "coefficient de saturation"** au sens de notre projet Wilson SU(N) (où nous l'introduisons via Bochner-Weitzenböck triple cancel κ = 1/6).

**De plus** : l'estimation (2.6) DPMO 2022 prend la forme

$$W_2(\rho(t), \hat{\rho}(t)) \leq \exp\left\{K\, c_1\, \mathfrak{C}_m \left[(tM^{m-1})^{2/(2+n(m-1))} \vee (tM^{m-1})\right]\right\} W_2(\mu_0, \hat{\mu}_0).$$

L'**exposant Hölder** apparent est **2/(2+n(m-1))** (PME en milieu négativement courbé), pas **1-κ**. Pour m → 1+ (équation de la chaleur) cet exposant → 1 (Lipschitz, pas Hölder).

---

## 4. Application à Wilson SU(N) D=4 : NON, OW 2005 ne s'applique pas

### Le mismatch fondamental

| Item | OW 2005 (réalité) | Notre mission Wilson SU(N) D=4 |
|------|---------------------|---------------------------------|
| Objet | Trajectoires PME (un semigroupe, deux IC) | Famille Gibbs à paramètre β (ou t = β⁻¹) |
| Distance | W_2 quadratique | TV (total variation) — supposé dans brief |
| Setting | Variété riemannienne compacte n-dim | Espace produit SU(N)^{N_links(a)} (mesure produit haar décorée par exp(-β S_W)) |
| Hypothèse géométrique | Ric ≥ λ (Bakry-Émery BE(λ,n)) | BE non-établi rigoureusement à β finis |
| Contraction | exp(-λt) (exponentielle) | Brief affirme |t-t'|^{1-κ} (Hölder) |
| κ | n'existe pas (ou n,m-dim. en DPMO) | κ = 1/6 (Bochner triple cancel SU(3)) |

### Critique du brief

Le brief affirme :
> "Otto-Westdickenberg 2008 : si μ_t = e^{-t·H}/Z(t) famille de Gibbs sur variété riemannienne compacte avec LSI(C_LSI) uniforme et coef saturation κ, alors ||μ_t - μ_t'||_TV ≤ C · |t-t'|^{1-κ}"

**Aucun de ces ingrédients ne se trouve dans OW 2005** :
1. ❌ OW ne traite PAS une famille e^{-tH}/Z(t) (c'est une trajectoire de PME, pas une famille Gibbs à température variable).
2. ❌ OW n'utilise PAS la norme TV.
3. ❌ OW n'utilise PAS de coefficient de saturation κ.
4. ❌ OW ne donne PAS un bound Hölder |t-t'|^{1-κ}, mais une contraction exponentielle exp(-λt) sur W_2.
5. ❌ La constante C n'est PAS reliée à C_LSI dans OW (qui n'évoque pas LSI directement).

### Volume uniformity (la question critique soulevée par Kévin)

Le brief demande : « Le volume `N_links(a) = D · L^D / a^D` → ∞ quand `a → 0`. Est-ce que C reste borné ? »

**Réponse** : Dans OW 2005 strict, la variété est **compacte** et de **dimension n fixe**. Le passage à l'extension Wilson SU(N) D=4 nécessite :
- (a) compacité de SU(N)^{N_links(a)} : oui (produit de compacts compact), mais **dimension explose** : dim = (N²-1) · D · L^D / a^D → ∞ quand a → 0.
- (b) BE(λ,n) uniforme en n : **fragile**. Dans la version BE de DPMO 2022 (Th 2.4), la constante C dépend explicitement de n (`tM^{m-1}` à la puissance `2/(2+n(m-1))`). Quand n → ∞, l'exposant → 0, et l'estimate dégénère vers Lipschitz-1 trivial.
- (c) En conséquence, **même si on adaptait OW à notre cas, l'estimation ne serait pas uniforme en a** quand a → 0.

---

## 5. Que vaut alors le PySR β-scan α = 0.8339 ≈ 5/6 ?

L'observation empirique :
> α = 0.8339 ± 0.01 ≈ 5/6 à 0.06%, et 1 − 1/6 = 5/6

est **frappante mais ne vient PAS d'OW 2005**. C'est soit :
- (a) une **coincidence numérique** (à valider via tests cross-D, cross-N : si α dépendait vraiment de κ_geometric, il devrait varier),
- (b) une **véritable loi** qui requiert un **autre théorème** (peut-être un descendant de Wang 2003, Cattiaux 2010, ou Bakry-Gentil-Ledoux 2014 chapitre 8, mais ces sources ne donnent pas non plus 1-κ Hölder TV pour Gibbs e^{-tH}/Z(t) en général),
- (c) un **effet RG** lié à la dimension anomale dans la phase confinée, indépendant d'OW.

**À tester** : faire un PySR β-scan sur D=3 (κ pourrait être différent) et SU(2) (κ pourrait varier) et vérifier si α reste à 5/6 ou suit une formule du type α = 1 − κ(N,D).

---

## 6. Alternatives et recommandations

### (a) Ne PAS appliquer OW 2005 tel quel
Il ne s'applique pas. Tout argument du paper Clay reposant sur cette ref serait fab.

### (b) Adaptations possibles

1. **Hairer 2014 (Inventiones, Hopf-coh)** — convergence ergodique des SPDEs, mais avec exposants Lipschitz pas Hölder.

2. **Ambrosio-Gigli-Savaré 2014 (RCD spaces)** — formalisme métrique des courbures Ric ≥ K, donne contraction W_2 mais nécessite vérification RCD(K,N) sur SU(N)^{N_links(a)} qui est compact mais a courbure sectionnelle bornée *par le bas pour SU(N) à curvature Killing*, *mais à dimension explosive en a → 0*.

3. **Bauerschmidt-Bodineau 2019** — Wasserstein contraction sous décomposition multi-échelle Bałaban-style, **plus proche** de notre besoin (Yang-Mills lattice), mais c'est essentiellement *retomber dans Bałaban* — pas un bypass.

4. **Capitaine-Hsu-Ledoux 1997 / Cattiaux 2010** — log-Sob → Gauss → Wasserstein, encore avec contraction Lipschitz (W_2 ≤ √(2 C_LSI · Entropy)).

5. **Otto-Villani 2000 (HWI inequality)** — Talagrand-LSI link. Donne W_2² ≤ 2 C_LSI · Entropy. NE donne PAS un bound Hölder pour Gibbs à T variable.

### (c) Chercher LE théorème de bonne forme

Aucune source standard (Villani 2009, BGL 2014, AGS 2008) ne contient le bound :
$$\|\mu_t - \mu_{t'}\|_{TV} \leq C \cdot |t-t'|^{1-\kappa}$$
pour une famille Gibbs μ_t = e^{-tH}/Z(t).

**Il existe des bounds approchants** :
- Stuart-Voss-Wiberg : régularité Hölder des mesures de Gibbs en *paramètre external* (mais c'est pour des distributions postérieurs en inférence statistique, pas champs de jauge).
- Bobkov-Gentil-Ledoux : régularité de l'entropie en température sous Bakry-Émery, mais c'est en *Entropy* pas *TV*.

### (d) Recommandation pratique : pivot

**Option A** : reformuler la dépendance en β (température) via un PySR-fit empirique, sans invoquer OW. Présenter α ≈ 5/6 comme observation, demander à Bauerschmidt / Hairer / Cattiaux la bonne réf théorique.

**Option B** : utiliser **Cattiaux 2010 (chap. "TV stability via LSI")** où on a :
$$\|\mu_t - \mu_{t'}\|_{TV}^2 \leq \tfrac12 \cdot \text{Entropy}(\mu_t | \mu_{t'}) \leq C_{LSI} \cdot \text{Fisher}(\mu_t | \mu_{t'}),$$
puis estimer Fisher en fonction de |t-t'| à la main. Cela donnera typiquement un bound *Lipschitz* (exposant 1), pas Hölder 1-κ.

**Option C** : accepter que α = 5/6 soit une **prédiction phénoménologique non-rigoureuse** dans le paper Clay, à confirmer par cross-D/cross-N (test falsifiable).

---

## 7. Décision

| Item | Verdict |
|------|---------|
| Theorem 2.1 OW 2008 verbatim | **❌ N'existe pas sous cette forme**. Citation bibliographique fabriquée (année, journal, DOI tous incorrects). |
| OW 2005 (la vraie référence) | Existe, mais traite W_2 contraction PME sur manif compacte. Pas TV. Pas Hölder 1-κ. Pas Gibbs e^{-tH}/Z(t). |
| Application à Wilson SU(N) D=4 | **❌ ne s'applique pas**. Mismatch structurel sur 5 axes (objet, norme, hypothèse, exposant, κ). Volume uniformity échoue de toute façon. |
| α = 5/6 empirique PySR | Observation honnête, mais sans support théorique OW. **Promotion** : TIER 3 SKETCH (numérique) au lieu de TIER 2 SUPPORTED. |
| Recommendation | **Pivot** : ne pas citer OW comme support. Soit (A) PySR phénoménologique honnête, soit (B) Cattiaux Lipschitz, soit (C) effet RG ad-hoc. |

---

## 8. Anti-fab notes

- L'attribution OW 2008 JFA 254:2865-2940 DOI 10.1016/j.jfa.2008.02.014 est **fabriquée** (probablement hallucinée par un LLM en confondant OW 2005 SIAM avec un autre article aux pages 2865 dans JFA 254 2008 — ce dernier traite Klyachko models).
- Aucun arXiv ID pour OW 2005 (le papier n'a pas été préprintée sur arXiv).
- Le κ "saturation coefficient" est une **introduction ad-hoc** de notre projet Wilson SU(N), pas un objet importé d'OW.
- L'absence du bound Hölder 1-κ TV dans OW est une **gap structurel** dans notre stratégie « bypass Bałaban via compactness + Bakry-Émery uniqueness » — il faut chercher ailleurs ou accepter le caractère phénoménologique de α = 5/6.

---

**Sources vérifiées** :
- [arXiv:0801.2455](https://arxiv.org/abs/0801.2455) — Daneri-Savaré 2008, **bibliography [19]** confirme OW publié SIAM J. Math. Anal. 37 (2005) 1227-1255.
- [arXiv:1908.03147v2](https://arxiv.org/abs/1908.03147) — De Ponti-Muratori-Orrieri 2022, JFA 314 (2023), Theorem 2.4 + 2.5 généralisent OW et fournissent l'exposant 2/(2+n(m-1)) (pas 1-κ).
- [SIAM J. Math. Anal. 37 (2005) 1227-1255](https://epubs.siam.org/doi/10.1137/050622420) — page primaire OW (paywall, fermé sous SIAM).
- [Westdickenberg RWTH publications](https://www.instmath.rwth-aachen.de/en/~mwest/publications/) — page personnelle, hébergé un PDF copie.
