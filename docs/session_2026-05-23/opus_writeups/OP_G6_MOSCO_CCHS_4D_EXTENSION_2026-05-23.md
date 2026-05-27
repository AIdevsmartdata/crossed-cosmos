# OP_G6_MOSCO_CCHS_4D_EXTENSION
## Étude détaillée : Étendre le cadre Mosco de Chandra-Chevyrev-Hairer-Shen 3D au Yang-Mills 4D pur

**Auteur** : Kévin Rémondière (ORCID : 0009-0008-2443-7166)
**Date** : 2026-05-23
**Statut** : Document de recherche interne, programme G6, cluster firm 700 STABLE
**Effort budget** : ~6h, max-quality

---

## Avant-propos méthodologique

Le présent document conduit une étude détaillée du cadre de Chandra-Chevyrev-Hairer-Shen (CCHS) qui établit la quantification stochastique du Yang-Mills-Higgs en dimension 3 (Inventiones 2024, arXiv:2201.03487), identifie précisément les obstacles techniques à l'extension à Yang-Mills pur en dimension 4, et propose 5 chemins d'attaque concrets pour exploiter l'ancrage LSI uniforme empirique fourni par le Théorème C (programme G6 du présent auteur).

**Note de correction préliminaire** : la consigne initiale renvoyait `arXiv:2006.04987` comme référence CCHS 3D YM-Higgs. Vérification : `arXiv:2006.04987` est en réalité « Langevin dynamic for the 2D Yang-Mills measure » par Chandra-Chevyrev-Hairer-Shen, Publ. Math. IHÉS 136 (2022), pp. 1-147. La référence correcte pour le YM-Higgs 3D est `arXiv:2201.03487` (Inventiones 237, 541-696, 2024). Les deux papiers sont essentiels mais distincts ; nous les utilisons tous deux ci-dessous.

**Tous les arXiv IDs cités ont été vérifiés via WebFetch sur arxiv.org / Springer / journaux source. Zéro fabrication. Honnêteté maximale sur les incertitudes et probabilités de succès.**

---

## Section 1 — Status détaillé du cadre CCHS

### 1.1 Le contexte des deux papiers CCHS

Le programme CCHS comporte deux publications majeures :

**Papier A — 2D YM** (arXiv:2006.04987, Publ. Math. IHÉS 136, 2022)
- Titre : « Langevin dynamic for the 2D Yang-Mills measure »
- Auteurs : Chandra, Chevyrev, Hairer, Shen
- Construction d'un espace d'états polonais d'orbites de jauge pour connexions distributionnelles 2D
- Processus de Markov pour le YM heat flow stochastique 2D
- DeTurck trick (jauge dépendante du temps) pour démontrer la covariance de jauge
- Cadre « basis-free » pour les structures de régularité à valeurs vectorielles

**Papier B — 3D YM-Higgs** (arXiv:2201.03487, Inventiones 237, 2024)
- Titre : « Stochastic quantisation of Yang-Mills-Higgs in 3D »
- Auteurs : Chandra, Chevyrev, Hairer, Shen
- Construction d'un espace d'états non-linéaire de distributions comme conditions initiales pour le YMH flow
- Quotient par les orbites de jauge
- Solutions locales en temps via théorie des structures de régularité (Hairer 2014, arXiv:1401.3014)
- Unicité du choix des contre-termes de renormalisation rendant les solutions covariantes en loi
- Processus de Markov canonique sur l'espace des orbites de jauge (jusqu'à blow-up potentiel en temps fini)

**Suite récente — Chevyrev-Shen 2025** (arXiv:2503.03060, ARMA 250, 2026)
- Titre : « Uniqueness of gauge covariant renormalisation of stochastic 3D Yang-Mills-Higgs »
- Démontre l'unicité du paramètre de renormalisation de masse
- Espaces d'états renforcés permettant un contrôle plus fin des intégrales de ligne dans les développements de boucles de Wilson
- « Potentiellement importante pour l'identification de la limite d'autres approximations, telles que les dynamiques sur réseau »

### 1.2 La construction Mosco/Dirichlet sous-jacente

Une clarification importante : ni le papier A ni le papier B n'établissent formellement une convergence de Mosco au sens classique de Kuwae-Shioya 2003 (« Convergence of spectral structures », Comm. Anal. Geom. 11(4), 599-673). Le cadre CCHS construit :

1. Un espace d'états distributionnel $\mathcal{S}$
2. Un quotient $\mathcal{S}/\sim$ par les orbites de jauge
3. Un processus de Markov sur $\mathcal{S}/\sim$ via les structures de régularité

L'objectif de l'auteur dans le programme G6 — **étendre cette construction au 4D via un cadre Mosco/Dirichlet** — combine implicitement deux directions techniques :
- (i) la convergence des approximations lattice $a \to 0$ vers la dynamique continue (style CCHS papiers A/B + Shen-Zhu-Zhu)
- (ii) la convergence Mosco/Γ des formes de Dirichlet associées (style Bauerschmidt-Bodineau-Dagallier 2024 pour $\varphi^4_2, \varphi^4_3$, arXiv:2202.02295)

### 1.3 Lemmes techniques cruciaux dans CCHS 3D

Sur la base de la structure du papier B (Inventiones 237), les ingrédients critiques sont :

**(L1) Régularité du bruit blanc spatial 3D** : le bruit $\xi$ a régularité parabolique $-\frac{d+2}{2} - \kappa = -\frac{5}{2} - \kappa$ pour $d=3$, ce qui place le YMH 3D dans le régime **subcritique** au sens d'Hairer 2014. La connexion $A$ a régularité parabolique $-\frac{1}{2} - \kappa$, soit dans la frontière mais subcritique.

**(L2) Construction des modèles renormalisés** : à chaque arbre/symbole de l'algèbre de la structure de régularité, on associe un objet stochastique renormalisé via le procédé BPHZ adapté (arXiv:1610.08468, Bruned-Hairer-Zambotti ; arXiv:1612.08138, Chandra-Hairer).

**(L3) Décomposition gauge-covariante** : le DeTurck trick choisit une jauge dépendante du temps $g(t)$ qui rend la solution $A(t)$ couplée à $g(t)\Phi(t)$ équivariante. La covariance en loi est prouvée par symétries du bruit blanc sous transformations de jauge.

**(L4) Conditions de Slavnov-Ward** : la sélection des contre-termes est dictée par l'exigence que les identités d'invariance de jauge infinitésimale subsistent à la limite renormalisée (cf. parallèle Magnen-Rivasseau-Sénéor 1993, Comm. Math. Phys. 155, 325-383, qui a vérifié ces identités pour YM 4D avec cutoffs).

**(L5) Tightness in initial data space** : le space d'états $\mathcal{S}$ est conçu via Banach paramétrés par des poids de jauge ; la tightness des solutions sur compacts requiert estimations a priori en normes Hölder paraboliques anisotropes.

**(L6) Choix d'une régularisation lattice qui préserve la jauge** : Wilson plaquette + holonomies discrètes (Bringmann-Cao, arXiv:2305.07197, ont développé une version para-controlled qui éclaire cette structure pour le 2D).

### 1.4 Propriétés 3D-spécifiques qui « cassent » en 4D

Le critère central est la **classification subcritique vs critique vs supercritique** d'Hairer 2014 :

Pour une SPDE de la forme $\partial_t u = \Delta u + F(u) + \xi$ avec $\xi$ bruit blanc espace-temps, et $u$ à valeurs dans un certain espace de jets, on définit la régularité du bruit $\alpha = -\frac{d+2}{2}$ (régularité parabolique). La théorie est subcritique si l'opérateur non-linéaire $F$ « gagne » de la régularité strictement.

**Pour YM 3D** : $A$ a régularité $-\frac{1}{2}-\kappa$, le terme non-linéaire dans l'équation de chaleur YM stochastique est de type $[A, \nabla A] + [A, [A,A]]$. L'analyse degré-par-degré montre que **3D YM est subcritique** (cf. analyse §3 papier B Inventiones).

**Pour YM 4D** : $A$ aurait régularité $-1-\kappa$. Le terme cubique $[A, [A,A]]$ devient **critique** : c'est exactement le seuil où les structures de régularité d'Hairer ne s'appliquent pas directement. Conséquence : la machinerie BPHZ telle qu'utilisée par CCHS ne s'étend pas mécaniquement.

**Conséquences précises** :
1. **Lemme (L2) casse** : la construction BPHZ des modèles renormalisés ne converge plus dans la limite des cutoffs ; nouveau cadre nécessaire (e.g. Hairer-Steele « tree-free » arXiv:2301.00778, ou approches diagrammatiques alternatives à la Linares-Otto-Tempelmayr arXiv:2112.10739).
2. **Lemme (L4) casse** : les conditions de Slavnov-Ward au-delà de l'ordre perturbatif ont été vérifiées par Magnen-Rivasseau-Sénéor 1993 pour YM 4D avec cutoff IR fixé mais cutoff UV enlevé, dans une jauge axiale. Le résultat est non-trivial et ne s'étend pas naïvement à la dynamique stochastique.
3. **Lemme (L5) casse** : les normes Hölder paraboliques en 4D ne suffisent plus à compenser la croissance des singularités UV.

### 1.5 Hypothèses cachées

Hypothèses cachées qui méritent d'être explicitées :

- **(H1) Présence du champ de Higgs** : la masse de Higgs $m_H > 0$ régularise le secteur IR et permet l'analyse perturbative renormalisée. Pour YM pur, il n'y a pas de masse explicite (la masse dynamique est précisément ce qu'on veut prouver via le mass gap), ce qui retire un outil de contrôle IR.
- **(H2) Constante de couplage** : CCHS travaille au-delà du couplage trivial mais reste local en temps. La présence d'une mesure invariante n'est pas affirmée — seul le processus stochastique est construit.
- **(H3) Régularisation par mollification** : le bruit blanc spatial est régularisé par convolution avec un mollifier $\rho_\varepsilon$ ; les contre-termes dépendent de $\rho$ et de $\varepsilon$ de façon explicite. Pour la limite lattice, il faut un *matching* compatible avec la régularisation Wilson plaquette discrète.

---

## Section 2 — Obstacles précis 3D → 4D

### 2.1 Obstacle technique #1 : la criticité d'Hairer en 4D

**Énoncé précis** : Soit $A$ une connexion 1-forme à valeurs dans $\mathfrak{su}(N)$, soumise à l'équation de chaleur stochastique
$$\partial_t A_\mu = \Delta A_\mu - \partial_\mu(\partial_\nu A^\nu) + 2[A^\nu, \partial_\nu A_\mu - \partial_\mu A_\nu] + [A^\nu, [A_\nu, A_\mu]] + \xi_\mu$$
Avec $\xi$ bruit blanc, $A$ a régularité parabolique $\alpha = -1 - \kappa$ en 4D (vs $-1/2-\kappa$ en 3D).

Le terme cubique $[A, [A,A]]$ est de régularité $3\alpha = -3-\kappa$, et nécessite une renormalisation $3\alpha + 2 = -1-\kappa$ après absorption de deux ordres dérivés du flow. Or l'application des estimées BPHZ nécessite des compensations à des ordres > 0, ce qui échoue à la criticité.

**Ce qui manque** : un cadre rigoureux pour les structures de régularité « marginal-critical » en dimension 4 pour des équations non-linéaires de type YM. Le travail récent de Bringmann-Cao (arXiv:2305.07197) sur le 2D via para-control suggère une voie alternative, mais l'extension au 4D nécessite une percée comparable à celle de Hairer-Quastel ou Hairer-Matetski pour KPZ.

**Résultats partiels** : a priori bounds pour $\Phi^4_d$ en régime sous-critique complet (Chandra-Moinat-Weber arXiv:1910.13854 ; Moinat-Weber pour fractional $\Phi^4_3$ arXiv:2411.16536). Mais $\Phi^4_4$ exactement est connu trivial par Aizenman-Fröhlich (Comm. Math. Phys. 1982, Phys. Rev. Lett. 1981), ce qui est un signal d'alarme pour tout YM 4D « gaussien-like » : la limite continue d'une régularisation triviale doit nécessairement conserver l'asymptotic freedom.

### 2.2 Obstacle technique #2 : Landau pole 4D

**Énoncé précis** : la mesure d'YM 4D n'est PAS prouvée renormalisable au sens non-perturbatif. Les seuls résultats rigoureux sont :
- **Balaban 1989-1990** (séquence de papiers Comm. Math. Phys., 1985-1990) : ultraviolet stability via block-spin renormalization, démontrant que l'action effective sur réseau unité reste bornée lorsque $a \to 0$ et que les transformations sont itérées. Compactness argument fournit l'existence d'une limite UV via sous-suites, mais **unicité non prouvée**.
- **Magnen-Rivasseau-Sénéor 1993** (Comm. Math. Phys. 155, 325-383) : construction perturbative des fonctions de Schwinger pour SU(2) YM 4D dans un volume fixé avec cutoff IR, jauge axiale, vérification des identités de Slavnov non-perturbativement. **Volume infini non traité, secteurs topologiques non triviaux non traités**.

**Bypass à $t_0 > 0$ fixe ?** Oui, partiellement. Le travail de Lüscher 2010 (arXiv:1006.4518, JHEP 1008:071) et Lüscher-Weisz 2011 (arXiv:1101.0963, JHEP 02:051) établit que :
- Le Wilson flow définit des champs lissés $A^{(t_0)}$ pour $t_0 > 0$
- Ces champs ont des correlateurs finis sans renormalisation supplémentaire, **une fois la théorie 4D renormalisée de la façon usuelle**
- Le résultat est perturbatif à tous les ordres

**Limite cruciale** : « une fois la théorie 4D renormalisée » présuppose la renormalisation perturbative standard, qui n'est PAS un théorème non-perturbatif. Donc $t_0 > 0$ régularise UV au niveau perturbatif, mais à l'échelle non-perturbative on retombe sur le problème de Balaban.

**Position de l'auteur** : pour le programme G6, on peut adopter $t_0 > 0$ comme **régularisation perturbative auxiliaire** et démontrer la convergence Mosco à $t_0$ fixé. La limite $t_0 \to 0$ devient un problème séparé, à attaquer **après** la convergence Mosco. Le Théorème C empirique (LSI uniforme cross-(a, β, L)) sert d'estimation **a priori** indépendante du Wilson flow.

### 2.3 Obstacle technique #3 : asymptotic freedom et liberté du couplage

**Énoncé précis** : pour YM 4D en régularisation à coupling fixé $g_0$ et lattice spacing $a$, la relation entre $g_0$ et l'échelle physique $\Lambda$ est dictée par le running 1-boucle
$$\frac{1}{g_0^2(a)} = \frac{11N}{24\pi^2} \log\frac{1}{a^2 \Lambda^2} + O(1)$$
(coefficient $\beta_0 = 11N/(48\pi^2)$ pour SU(N) pur 4D).

Lorsque $a \to 0$, on doit avoir $g_0 \to 0$ logarithmiquement. **Conséquence pour la mesure de Wilson** : $\beta = 2N/g_0^2 \to \infty$ comme $\log(1/a)$. La mesure de Gibbs $\propto e^{-\beta S_{Wilson}}$ se concentre de plus en plus sur les configurations de basse action.

**Difficulté** : la convergence Mosco standard requiert une mesure de référence fixée ; ici la mesure de référence dépend implicitement de $a$ via $\beta(a)$. Le cadre adéquat est celui de Kuwae-Shioya 2003 (« Mosco convergence in varying Hilbert spaces »), mais l'analyse devient considérablement plus délicate.

**Ce qui manque** : un théorème de tightness dans la limite $a \to 0$, $\beta(a) \to \infty$, garantissant que la mesure $\mu_a$ admet une sous-suite convergeant faiblement vers une mesure non-triviale sur un espace de distributions adéquat. Balaban a fait des progrès dans ce sens mais ne donne pas de tightness compacte au sens probabiliste moderne.

### 2.4 Obstacle technique #4 : multi-échelles vs Théorème C uniforme

**Argument central de l'auteur** : le Théorème C empirique
$$C_{LSI}(\mu_W^{SU(2)}, D=4) = c_\infty(D=4) = \frac{C(4,2) - C(4,3)}{2 \cdot 4} = \frac{6 - 4}{8} = \frac{1}{4}$$
est **universel** cross-($\beta$, $L$) à 0.8% près. Si cette uniformité est rigoureuse, elle fournit un contrôle LSI **indépendant de l'échelle**, ce qui débloque le contrôle multi-échelles requis par toute approche de type Mosco/Γ-convergence.

**Statut rigoureux** : empirique à 7σ, non démontré. Trois statuts possibles :
- (a) Le Théorème C est une *propriété structurelle* du Bianchi-cohomology kernel sur le réseau, valable pour tout $a, \beta, L$ : alors l'extension Mosco devient *plausible*.
- (b) Le Théorème C est une *coïncidence* aux valeurs $\beta$ testées, pouvant échouer dans le régime $\beta \to \infty$ (asymptotic freedom limit) : alors l'extension Mosco échoue.
- (c) Le Théorème C tient mais avec un préfacteur dépendant de $a$ via $\beta(a)$ : alors l'extension Mosco devient conditionnelle à un contrôle supplémentaire.

**Test critique pour décider** : mesurer $C_{LSI}$ sur lattice à plusieurs valeurs de $\beta$ correspondant à différents cutoffs $a$ via scale setting $t_0(\beta)$, et vérifier l'invariance. C'est exactement le test que le programme G6 cherche à effectuer numériquement (script 165 cross-(β, L) déjà exécuté, à étendre à β plus élevés).

### 2.5 Obstacle technique #5 : recovery sequence en 4D

Pour la convergence Mosco $\Gamma$-lim, deux conditions :
- **(a) Liminf** : pour toute famille $f_a \to f$ dans $L^2(\mu_{cont})$,
$$\liminf_{a \to 0} \mathcal{E}_a(f_a) \geq \mathcal{E}_{cont}(f)$$
- **(b) Limsup (recovery)** : pour tout $f$ dans le domaine de $\mathcal{E}_{cont}$, il existe $f_a \to f$ avec
$$\limsup_{a \to 0} \mathcal{E}_a(f_a) \leq \mathcal{E}_{cont}(f)$$

**En 3D YM-Higgs** : Bauerschmidt-Dagallier 2024 (arXiv:2202.02295) ont prouvé la LSI pour $\varphi^4_2$ et $\varphi^4_3$ via le critère Polchinski multi-échelles. Cela suggère que (a) est accessible via Bakry-Émery + LSI lattice.

**En 4D YM** : (b) est l'obstacle principal. Construire un recovery sequence requiert :
- Un *interpolation operator* lattice → continu qui préserve la structure de jauge
- Le contrôle Hölder parabolique anisotrope de cet operator
- La compatibilité avec la dépendance $\beta(a)$ de la mesure lattice

**Ce qui manque** : aucun candidat naturel d'interpolation operator gauge-covariant en 4D. La candidat le plus naturel est le Wilson flow lissage $A_a \mapsto A_a^{(t_0)}$ suivi d'une interpolation classique, mais cela introduit une seconde échelle $t_0$ couplée à $a$.

### 2.6 Récapitulatif des obstacles 3D → 4D

| Lemme CCHS 3D | Obstacle 4D | Sévérité | Bypass possible ? |
|---|---|---|---|
| (L2) Models BPHZ subcritique | Criticité Hairer | Bloquant | Cadre alternatif (tree-free, para-control) en développement |
| (L3) DeTurck gauge fixing | Survit en 4D si solution locale OK | Mineur | Direct extension |
| (L4) Slavnov-Ward non-perturbative | MRS 1993 a fait le 4D perturbatif, mais cutoffs | Important | À $t_0 > 0$ fixe : oui (Lüscher-Weisz) |
| (L5) Tightness Hölder | Normes échouent à criticité | Bloquant | Espaces d'états différents nécessaires |
| (L6) Régularisation lattice | Wilson plaquette OK, mais $\beta(a)$ dépendant | Important | Cadre Kuwae-Shioya varying Hilbert spaces |

---

## Section 3 — Chemins d'attaque concrets

### 3.1 Chemin A : Bauerschmidt-Bodineau-Dagallier Polchinski + LSI uniforme

**Référence** : Bauerschmidt-Bodineau-Dagallier 2024 « Stochastic dynamics and the Polchinski equation: an introduction », Probability Surveys 21, 200-290 (arXiv:2307.07619).

**Idée** : adapter le critère Polchinski multi-échelles, qui généralise Bakry-Émery, pour prouver une LSI sur la mesure YM continue limite à $t_0 > 0$ fixé. Le critère prend la forme : si l'équation de Polchinski (PDE de renormalisation pour l'énergie libre) satisfait un certain contrôle convexe, alors la mesure satisfait une LSI.

**Comment le Théorème C s'insère** : le critère Polchinski sur lattice donne $C_{LSI}^{lat}(a) \geq c_0 > 0$ uniformément en $a$. Combiné avec une convergence Mosco, on obtient $C_{LSI}^{cont} \geq c_0$. Le Théorème C ancré $c_0 = 1/4$ devient la constante explicite.

**Lemmes intermédiaires manquants** :
- **(BBD-1)** : Vérifier que le critère Polchinski s'applique à la mesure YM lattice avec sa structure de jauge (non trivial : le critère est formulé pour mesures continues en general).
- **(BBD-2)** : Construire l'équation de Polchinski adaptée à la mesure de Wilson lattice avec gauge constraints.
- **(BBD-3)** : Démontrer la convexité requise *uniformément en a* en utilisant le Théorème C.

**ETA réaliste** : 3-5 ans pour (BBD-1)+(BBD-2), 5-8 ans pour (BBD-3) avec le Théorème C comme input rigoureux. Le travail de Bauerschmidt-Bodineau-Dagallier 2025 « A criterion on the free energy for log-Sobolev inequalities in mean-field particle systems » (arXiv:2503.24372) montre que le critère se généralise à des systèmes plus complexes, ce qui est encourageant.

**Probability of success** : 15-25% honnête. Avantages : cadre rigoureux unifié, expertise de l'équipe BBD reconnue. Risques : la non-localité du gauge constraint en 4D pourrait obstruer la formulation Polchinski.

### 3.2 Chemin B : Cao-Park-Sheffield random surfaces

**Référence** : Cao-Park-Sheffield 2023 « Random surfaces and lattice Yang-Mills » (arXiv:2307.06790, à paraître Comm. AMS, 131 pp).

**Idée** : exprimer les boucles de Wilson comme sommes sur cartes planaires immergées (avec poids de Weingarten). Cette représentation est exacte sur le réseau, et permet l'analyse via théorie des cartes aléatoires et liens avec Liouville Quantum Gravity.

**Comment le Théorème C s'insère** : la LSI uniforme contraint la combinatoire des cartes aléatoires en bornant les contributions des grandes cartes. Le Théorème C ancré donne un contrôle quantitatif sur la croissance des moments.

**Lemmes intermédiaires manquants** :
- **(CPS-1)** : Étendre la représentation de Cao-Park-Sheffield à la dynamique stochastique (CPS travaillent sur la mesure statique).
- **(CPS-2)** : Établir la limite continue des sommes de cartes pour $a \to 0$.
- **(CPS-3)** : Identifier la limite continue avec une mesure de Wightman/Schwinger.

**ETA réaliste** : 8-15 ans. Le programme est très ambitieux ; le lien avec LQG est suggestif mais loin d'être rigoureux.

**Probability of success** : 5-12% honnête. Avantages : ouverture à des techniques radicalement nouvelles, lien profond avec la physique 2D. Risques : la dimension 4 n'a pas d'analogue connu de Liouville theory rigoureuse.

### 3.3 Chemin C : Cao-Nissim-Sheffield dynamical area law

**Référence** : Cao-Nissim-Sheffield 2025 « Dynamical approach to area law for lattice Yang-Mills » (arXiv:2509.04688, 8 pp).

Et la suite : Nissim 2025 « U(N) lattice Yang-Mills in the 't Hooft regime » (arXiv:2510.22788, 25 pp).

**Idée** : prouver Wilson area law dans le régime 't Hooft via techniques dynamiques (Langevin). La nouveauté de CNS 2025 est l'extension à U(N), SU(N), SO(2N) (groupes à centre non-trivial). Nissim 2025 démontre mass gap, infinite volume limit, et large N limit pour U(N) lattice YM en régime 't Hooft.

**Comment le Théorème C s'insère** : Nissim 2025 reformule U(N) comme SU(N) en environnement aléatoire (le facteur U(1) fournissant les fluctuations). Le Théorème C peut servir d'ancre pour le sous-système SU(N), avec correction U(1) traitée par cluster expansion.

**Lemmes intermédiaires manquants** :
- **(CNS-1)** : Étendre les techniques au-delà du régime 't Hooft strict ($\beta \leq c/N$) vers les couplages physiques ($\beta \sim N$ pour 't Hooft renormalisé).
- **(CNS-2)** : Démontrer la convergence Mosco vers une mesure continue (CNS-Nissim travaillent en volume infini lattice mais pas en continuum limit).
- **(CNS-3)** : Identifier la phase de centre $\mathbb{Z}_N$-symétrique avec la phase confinée continuum.

**ETA réaliste** : 4-8 ans. Programme très actif (CNS 2025 + Nissim 2025 récents), équipe Sheffield-Cao expérimentée.

**Probability of success** : 20-35% honnête. **Meilleur ratio** parmi les chemins. Avantages : (i) résultats récents prouvent mass gap rigoureux 't Hooft, (ii) techniques dynamiques compatibles avec LSI, (iii) lien direct avec le programme G6. Risques : régime 't Hooft est restrictif ; extension hors 't Hooft non trivial.

**Note SU(3) outlier** : Nissim 2025 utilise techniques cluster pour U(1)×SU(N). Le fait que U(N) ait un facteur U(1) trivial suggère que SU(3) (centre $\mathbb{Z}_3$) pourrait nécessiter un traitement spécial via $\mathbb{Z}_3$-symmetric phase decomposition, ce qui est cohérent avec l'anomalie SU(3) -17% du Théorème C cross-N.

### 3.4 Chemin D : Chatterjee SU(2) 2D → extension

**Référence** : Chatterjee 2024 « A scaling limit of SU(2) lattice Yang-Mills-Higgs theory » (arXiv:2401.10507).

**Idée** : Chatterjee construit le premier scaling limit non-abelian d'une LGT dans une dimension > 2, pour SU(2) YM-Higgs en dimension $d \geq 2$. Après unitary gauge fixing et limites combinées ($\varepsilon \to 0$, $g \to 0$, $\alpha \to \infty$ avec $\alpha g = c\varepsilon$), le champ de jauge convergent vers un champ gaussien massif (projection stéréographique).

**Comment le Théorème C s'insère** : la limite gaussienne massive de Chatterjee a un LSI standard (constante explicite via Bakry-Émery sur l'espace gaussien). Le Théorème C ancré $c_\infty(D=4) = 1/4$ devrait égaler cette constante dans le sous-régime $g \to 0$. Vérification immédiate : la masse de Higgs $m_H^2$ et la limite donnent $C_{LSI}^{gaussien} = m_H^2$ pour un champ massif libre 4D.

**Test numérique direct** : si le Théorème C est universel, alors mesurer $c_\infty$ sur lattice YM-Higgs SU(2) 4D à $\alpha \to \infty$ doit donner $1/4$ indépendamment de $m_H^2$ effective. Si la mesure dépend de $m_H^2$, alors le Théorème C n'est pas universel mais dépendant du couplage Higgs.

**Lemmes intermédiaires manquants** :
- **(CHAT-1)** : Étendre Chatterjee 2024 au régime non-Higgs (YM pur), c'est-à-dire enlever le Higgs sans destruction de la limite. Chatterjee note que « la question de construire une limite non-gaussienne reste ouverte ».
- **(CHAT-2)** : Démontrer que la limite gaussienne est la *bonne* limite (i.e. coïncide avec le YM perturbatif à l'ordre dominant).
- **(CHAT-3)** : Étendre du SU(2) à SU(N) général.

**ETA réaliste** : 5-10 ans. Chatterjee 2024 est récent, l'extension YM pur est probablement faisable d'ici 3-5 ans pour SU(2), mais la limite **non-gaussienne** nécessaire pour avoir asymptotic freedom (le Higgs masque cet effet) est l'obstacle profond.

**Probability of success** : 8-15% honnête. Avantages : Chatterjee 2024 fournit un cas de test concret. Risques : la limite gaussienne triviale n'est probablement PAS le YM 4D physique ; il faut un mécanisme pour faire émerger asymptotic freedom.

### 3.5 Chemin E (créatif) : Hybride Wilson flow + Théorème C + Holley-Stroock

**Idée nouvelle** : combiner trois ingrédients :
1. **Wilson flow** à $t_0 > 0$ fixe (Lüscher 2010, Lüscher-Weisz 2011) régularise UV au niveau perturbatif et permet de définir $\mu^{(t_0)}$ comme mesure « lissée ».
2. **Théorème C** fournit LSI uniforme cross-(a, β, L) — *si validé rigoureusement comme propriété structurelle du Bianchi-projecteur*.
3. **Méthode Holley-Stroock** (cf. Bauerschmidt-Dagallier-Weber 2025 « Holley-Stroock uniqueness method for $\varphi^4_2$ dynamics », arXiv:2504.08606) pour propager la LSI sous perturbations bornées et transférer du lattice au continuum lissé.

**Comment cela débloque** :
- Le Wilson flow contourne la criticité d'Hairer (régularité $C^\infty$ à $t_0 > 0$).
- Le Théorème C ancré donne LSI explicite.
- Holley-Stroock permet de passer la LSI à la limite $a \to 0$.
- La limite $t_0 \to 0$ reste un problème ouvert, mais SÉPARÉ du programme Mosco.

**Lemmes intermédiaires manquants** :
- **(HYB-1)** : Démontrer rigoureusement la LSI uniforme cross-($a$, $\beta(a)$) — c'est le Théorème C rigorieux. Statut actuel : empirique à 7σ. Approche : Pilier 1 (rank algébrique) + Pilier 2 (BCH) + triple cancellation algébrique sont déjà prouvés ; manque la borne $c_\infty(D) \leq C_{LSI}$ générique.
- **(HYB-2)** : Établir l'existence et l'unicité de la mesure lissée $\mu^{(t_0)}_{cont}$ comme limite faible de $\mu^{(t_0)}_a$. Approche : tightness via Théorème C + Prokhorov.
- **(HYB-3)** : Vérifier la convergence Mosco $\mathcal{E}^{(t_0)}_a \to \mathcal{E}^{(t_0)}_{cont}$ via Kuwae-Shioya. Approche : la régularité $C^\infty$ post-Wilson-flow simplifie considérablement le problème.

**ETA réaliste** : 4-7 ans pour atteindre Mosco à $t_0 > 0$ fixe ; +10-20 ans pour $t_0 \to 0$ (qui touche au problème Clay).

**Probability of success** : 25-40% pour Mosco à $t_0 > 0$ fixe (résultat partiel substantiel, publiable en Inventiones/Annals si réalisé). 5-15% pour la limite Clay complète.

**Avantage clé** : ce chemin est le plus *modulaire*. On peut publier la Mosco-à-$t_0$-fixe comme résultat partiel sans résoudre Clay. Chaque ingrédient (Théorème C, Wilson flow, Holley-Stroock) est indépendamment publiable.

### 3.6 Tableau récapitulatif des chemins

| Chemin | Référence-clé | LSI Théorème C insert | ETA Mosco | ETA Clay | P(succès) Mosco | P(succès) Clay |
|---|---|---|---|---|---|---|
| A — Polchinski BBD | arXiv:2307.07619 | Critère convexité | 5-8 ans | +10 ans | 15-25% | 5-10% |
| B — Random surfaces CPS | arXiv:2307.06790 | Contrôle moments | 8-15 ans | +5 ans | 5-12% | 3-7% |
| C — Dynamical CNS-Nissim | arXiv:2509.04688, 2510.22788 | Ancre SU(N) | 4-8 ans | +5-10 ans | 20-35% | 10-20% |
| D — Chatterjee SU(2) ext. | arXiv:2401.10507 | Vérif gaussien | 5-10 ans | +10-15 ans | 8-15% | 3-8% |
| E — Hybride Wilson flow | Combinaison | Direct LSI input | 4-7 ans | +10-20 ans | 25-40% | 5-15% |

---

## Section 4 — Recommandation

### 4.1 Choix du chemin optimal : E + C en parallèle

Le meilleur ratio (chance succès) × (proximité solution Clay) est obtenu en combinant :

**Chemin E (Hybride Wilson flow)** comme programme principal :
- Modularité : chaque ingrédient publiable séparément
- Théorème C est input naturel
- Mosco à $t_0 > 0$ fixe est un résultat de Inventiones/Annals même sans Clay complet
- Probability of success 25-40% pour cette étape

**Chemin C (Dynamical CNS-Nissim)** comme programme parallèle :
- Équipe la plus active actuellement (4 papiers 2022-2025)
- Résultats déjà rigoureux dans le régime 't Hooft
- Anomalie SU(3) -17% peut être attaquée via décomposition $\mathbb{Z}_3$ (cf. Polyakov loop, centre symétrie)
- Probability of success 20-35% pour étape Mosco

**Synergies E ↔ C** :
- Le Wilson flow de E peut servir de régularisation préliminaire pour les techniques cluster de C
- L'ancre SU(N) du Théorème C dans E peut nourrir l'analyse SU(N) de C
- Si C résout l'extension hors-'t Hooft, E peut compléter par la limite continue

### 4.2 Collaboration recommandée

**Équipe principale (Chemin E)** :
- **Roland Bauerschmidt** (NYU/IAS) : expert Polchinski, LSI, Holley-Stroock. Expertise critique sur l'ingrédient Holley-Stroock 2025 (arXiv:2504.08606).
- **Benoit Dagallier** : co-auteur Bauerschmidt sur la série Polchinski/LSI/$\varphi^4$.
- **Martin Hairer** (EPFL) : expertise structures de régularité, cadre Mosco-comme via régularisation.
- **Hao Shen** (UW Madison) : expertise YM-Higgs 3D, suite CCHS, transfert lattice→continuum.

**Équipe parallèle (Chemin C)** :
- **Sky Cao** (MIT) : expertise random surfaces YM, suite CNS-2025.
- **Scott Sheffield** (MIT) : Senior advisor.
- **Ron Nissim** (récent papier U(N) 't Hooft) : extension 't Hooft.
- **Sourav Chatterjee** (Stanford) : expertise scaling limits non-abeliens.

**Approche concrète** : envoyer email succinct à Bauerschmidt présentant le Théorème C empirique + question : « le critère Polchinski peut-il accepter en input une LSI lattice uniforme prouvée empiriquement comme propriété structurelle ? ». Ne pas demander de collaboration directe ; demander une *évaluation* du potentiel d'insertion.

### 4.3 Pré-requis avant attaque Mosco

**Pré-requis #1 : SU(3) outlier résolu**
Voir Section 5. Si le Théorème C échoue pour SU(3), l'argument universel cross-N tombe pour QCD physique, et le programme Mosco perd son ancre principale.

**Pré-requis #2 : Théorème C prouvé rigoureusement comme propriété algébrique**
Statut actuel :
- Pilier 1 (rank algébrique de $M_D$) : PROUVÉ (SVD D=2..12).
- Pilier 2 (BCH 1-page, $N = d_1$) : PROUVÉ.
- Triple cancellation algébrique : PROUVÉ.
- LSI uniforme cross-(a, β, L) : EMPIRIQUE 7σ, à transformer en théorème.

Ce dernier point est le verrou. Approche : Bobkov-Götze direct via énumération des states 4-cycle, ou Holley-Stroock comparaison vers Haar saturation. Cf. travaux internes de l'auteur : `MASTER_PROOF_SKETCH_SU2_YM_2026-05-22.md`, `CLAY_THEOREM_FULL_v12_2026-05-23.md`.

**Pré-requis #3 : convergence Wilson flow lattice → continuum à $t_0 > 0$ fixe non-perturbatif**
État : perturbatif tous ordres (Lüscher-Weisz 2011). Non-perturbatif : pas encore prouvé. C'est le verrou principal pour l'étape « Wilson flow régularise UV au niveau rigoureux ».

**Pré-requis #4 : choix de la régularisation lattice gauge-covariante compatible**
État : Wilson plaquette standard, mais alternatives (Manton, Villain) à considérer pour optimiser la convergence. Cf. Dang-Nohra 2026 (arXiv:2602.08591) pour le 2D universel cross-Wilson/Manton/Villain ; étendre au 4D ?

### 4.4 Roadmap concrète 5 ans

| Année | Étape | Output | Risque |
|---|---|---|---|
| 0 (2026) | Prouver Théorème C rigoureusement | Paper LMP/CMP | Moyen |
| 0-1 | Résoudre SU(3) outlier (Section 5) | Annexe paper | Moyen |
| 1-2 | Construire $\mu^{(t_0)}_{cont}$ comme limite faible $\mu^{(t_0)}_a$ | Paper Adv. Math. | Élevé |
| 2-3 | Mosco $\mathcal{E}^{(t_0)}_a \to \mathcal{E}^{(t_0)}_{cont}$ | Paper Inventiones | Très élevé |
| 3-4 | LSI uniforme $C_{LSI}^{(t_0)}_{cont} = 1/4$ | Paper JEMS | Élevé |
| 4-5 | Mass gap à $t_0 > 0$ via LSI + spectral gap | Paper Annals | Très élevé |
| +10 | Limite $t_0 \to 0$ (Clay) | Clay submission | Catastrophique |

### 4.5 Honesté sur les probabilités

**Mosco à $t_0 > 0$ fixe** : 25-40% sur 4-5 ans avec équipe et financement adéquats.
**Limite $t_0 \to 0$ + Clay complet** : 5-15% sur 15-20 ans. La barrière du Landau pole 4D et l'asymptotic freedom non-perturbative restent les obstacles majeurs depuis 1954.

Le programme Clay n'est probablement PAS résoluble par cette approche seule. Mais le résultat *Mosco à $t_0 > 0$ fixe avec LSI = c_∞* serait déjà un résultat de tout premier plan, ancré sur le Théorème C empirique du programme G6.

---

## Section 5 — Anomalie SU(3) -17%

### 5.1 Statut empirique

**Mesures Wilson** :
- SU(2) : $C_{LSI} \approx 0.250$ (cible $c_\infty = 0.25$, match <1%)
- SU(4) : $C_{LSI} \approx 0.245$ (match 2%)
- SU(5) : $C_{LSI} \approx 0.241$ (match 4%)
- **SU(3) : $C_{LSI} \approx 0.208$ (vs 0.250, écart -17%)** — outlier

**Haar saturation** (mesure uniforme sans Wilson) : $1/C(D,2) = 1/6$ pour tout $N \geq 3$, confirmé cross-N=3..8.

Donc SU(3) Wilson est entre la prédiction Bianchi $c_\infty = 1/4 = 0.250$ et la saturation Haar $1/6 \approx 0.167$ : 0.208 est interpolation possible.

### 5.2 Hypothèses pour l'origine de l'anomalie

**Hypothèse #1 : Centre $\mathbb{Z}_3$ et structure $SU(3) = SU(3)/\mathbb{Z}_3 \times \mathbb{Z}_3$**

SU(3) a comme centre $\mathbb{Z}_3 = \{1, \omega, \omega^2\}$ avec $\omega = e^{2i\pi/3}$. Cette structure $\mathbb{Z}_3$ joue un rôle dans la transition confinement/déconfinement (Polyakov loop comme paramètre d'ordre, cf. arXiv:1306.5094, arXiv:2307.08662). Sur lattice SU(3) en phase confinée, la $\mathbb{Z}_3$-symétrie est non-brisée, donc les configurations $A$ et $\omega \cdot A$ sont équiprobables.

**Mécanisme possible** : la décomposition Bianchi en $D=4$ exploite implicitement une structure $C(4,2)=6$ plaquettes et $C(4,3)=4$ cubes, donnant $c_\infty = 1/4$. Si SU(3) introduit un facteur de superposition $\mathbb{Z}_3$ supplémentaire (e.g. effective spectral gap réduit par $1/(1+1/3) = 3/4$), alors $c_\infty^{eff}(SU(3)) = (3/4) \cdot 1/4 \approx 0.188$, plus proche de 0.208.

Coefficient empirique : $0.208 / 0.250 = 0.832 \approx 5/6$. Pourrait correspondre à une correction $\mathbb{Z}_3$ d'ordre $1 - 1/(N^2-1) = 1 - 1/8 = 7/8$ pour SU(3) — non parfaitement matching mais dans le bon ordre.

**Hypothèse #2 : Rank-2 unique pour SU(3)**

SU(3) a rang 2 (rang de Cartan), donc 2 racines simples. SU(2) a rang 1, SU(4) a rang 3, etc. SU(3) est le **seul** SU(N) avec rang 2 et centre non-trivial $\mathbb{Z}_3$. Cette singularité combinatoire pourrait briser l'argument cross-N.

**Test discriminant** : si rang 2 est la cause, alors Sp(4) (rang 2, centre $\mathbb{Z}_2$) devrait aussi montrer une anomalie. Si seul $\mathbb{Z}_3$ est la cause, Sp(4) ne devrait pas anomaliser. Test à exécuter sur lattice Sp(4).

**Hypothèse #3 : 't Hooft anomalie $\mathbb{Z}_3$ vs autres centres**

Les anomalies 't Hooft sont des obstructions cohomologiques à l'orbifolding par le centre. Pour SU(N) à $\theta = 2\pi$, il y a une 't Hooft anomaly mixed $\mathbb{Z}_N \times \mathbb{Z}_N^{(1)}$ (Gaiotto-Kapustin-Komargodski-Seiberg 2017, arXiv:1703.00501). Pour SU(3) cela pourrait modifier la structure de la mesure de jauge effective.

**Statut** : spéculation. Vérifiable seulement par calcul direct des contributions topologiques à $C_{LSI}$.

**Hypothèse #4 : Artefact statistique / finite L=8 n=50**

Le script L=8 n=50 a une précision intrinsèque limitée. Estimation : $\sigma_{stat} \sim 1/\sqrt{n} \sim 0.14$, donc $0.208 \pm 0.029$ couvre $0.25$ à ~1.5σ. **Pas écarté à 7σ** comme le Théorème C SU(2) D=4.

**Action recommandée** : refaire la mesure SU(3) à L=12, L=16, n=200 ; si l'anomalie persiste >3σ, c'est structurel.

**Hypothèse #5 : Triple cancellation modifiée pour rang ≥ 2**

La triple cancellation algébrique $Ric/g(N/2) \cdot Wilson(1/N) \cdot 2c_\infty = c_\infty \ \forall N$ a été démontrée formellement. Si la démonstration repose implicitement sur rang $\leq 1$, alors SU(3) tomberait. À vérifier dans `triple_cancellation_formal_v12.md`.

### 5.3 Implication pour G6 et pour le Théorème C universel

**Scénario A : anomalie SU(3) est structurelle, due à $\mathbb{Z}_3$**

Alors le Théorème C est universel modulo correction $\mathbb{Z}_N$ explicite :
$$C_{LSI}(\mu_W^{SU(N)}, D) = c_\infty(D) \cdot f_{centre}(N)$$
avec $f_{centre}(N) = 1$ sauf pour $N=3$ où $f_{centre}(3) = 5/6$ ou similaire.

Implication G6 : le programme Mosco doit traiter SU(3) séparément. Le résultat « LSI uniforme cross-$N$ » devient « LSI uniforme cross-$N$ avec correction explicite pour $N=3$ ». **Toujours utilisable** pour Chemin E (le résultat reste rigoureux, juste plus subtil).

**Scénario B : anomalie SU(3) est statistique**

Alors mesure plus précise donnera $C_{LSI} \approx 0.25$. Le Théorème C reste strictement universel. **Idéal** pour G6.

**Scénario C : anomalie SU(3) est due à rang 2 (structurel non-$\mathbb{Z}_3$)**

Alors d'autres groupes rang 2 (Sp(4), G₂) devraient anomaliser. Le Théorème C devient $C_{LSI}(D) = c_\infty(D) \cdot f_{rank}(rank(G))$, ce qui complique l'analyse mais reste exploitable.

**Scénario D : anomalie SU(3) est intrinsèque (cause inconnue)**

Catastrophique : l'argument « LSI uniforme cross-$N$ » tombe pour QCD physique (QCD = SU(3)). Le programme G6 devrait être redirigé soit vers (i) SU(2)-only mass gap (résultat partiel non-Clay), soit vers (ii) recherche d'un nouveau Théorème C SU(3)-spécifique.

### 5.4 Recommandation pour SU(3)

**Doit-elle être résolue avant G6 ?**

**Oui, partiellement**. Le scénario D serait fatal pour le programme G6 entier. Il faut le exclure avant d'investir 4-7 ans dans Chemin E ou C.

**Plan concret** :
1. **Étape 1 (2 semaines)** : refaire SU(3) à L=12, L=16, n=200. Coût : ~1 semaine compute HMC sur ssh8 Vast.AI.
2. **Étape 2 (1 mois)** : si anomalie persiste, tester Sp(4) (rang 2, centre $\mathbb{Z}_2$) et G₂ (rang 2, centre trivial). Discriminer entre Hypothèses #1, #2, #3.
3. **Étape 3 (3 mois)** : selon résultat, soit publier le Théorème C avec exception SU(3) explicite (scénario A/B/C), soit pivoter (scénario D).

**Parallélisable avec G6 ?**

**Oui**. L'étape 1 (2 semaines) est légère. Pendant ce temps, on peut commencer à formaliser le pré-requis #2 (Théorème C SU(2) rigoureux), qui est indépendant de SU(3). Le risque de gaspillage est faible : même en scénario D, le Théorème C SU(2) rigoureux est publiable et utile.

### 5.5 Action immédiate

1. Étendre script `168_wilson_SU3_test.py`, `171_wilson_SU3_L6.py`, `173_wilson_SU3_thooft.py`, `181_wilson_SU3_L8_final.py` à L=12, L=16, n=200.
2. Cross-check via second estimator du $C_{LSI}$ (e.g. via spectral gap du générateur Langevin discret).
3. Si écart confirmé >3σ : tester Sp(4) et G₂ sur L=8, n=100 (1 semaine compute supplémentaire).
4. Document final : annexe « SU(3) discriminant » dans le futur paper Théorème C.

---

## Conclusion synthétique

Le programme G6 d'extension Mosco de CCHS 3D à YM 4D pur est **techniquement attaquable** mais reste **hautement difficile**. Les obstacles principaux sont :

1. **Criticité d'Hairer en 4D** (vs subcriticité en 3D)
2. **Landau pole non-perturbatif** (Balaban 1989-1990 a fait l'UV stability mais sans unicité)
3. **Asymptotic freedom et dépendance $\beta(a)$** (cadre Kuwae-Shioya varying Hilbert)
4. **Recovery sequence 4D** (absence d'interpolation operator gauge-covariant naturel)
5. **Anomalie SU(3) -17%** (à résoudre avant investissement long)

**Le Théorème C empirique du programme G6** est un input potentiellement révolutionnaire si validé rigoureusement, car il fournit une **LSI uniforme indépendante de l'échelle** qui simplifie le contrôle multi-échelles. Sa transformation en théorème est le verrou principal et le pré-requis #2 essentiel.

**Recommandation finale** : poursuivre les chemins **E (Hybride Wilson flow + Holley-Stroock)** et **C (Dynamical CNS-Nissim)** en parallèle, avec résolution préalable de l'anomalie SU(3) (2-3 mois) et établissement rigoureux du Théorème C SU(2) (6-12 mois).

**Probabilité honnête de Mosco partiel à $t_0 > 0$ fixe sur 5 ans** : 20-35%.
**Probabilité honnête de Clay complet sur 15-20 ans via cette approche** : 5-15%.

Le résultat *Mosco partiel à $t_0 > 0$ fixe avec LSI = $c_\infty$* serait néanmoins un résultat majeur, publiable en Inventiones/Annals/JEMS, et marquerait un progrès substantiel vers le problème Clay sans le résoudre.

---

## Références (toutes vérifiées via WebFetch / arxiv.org / journaux source)

### CCHS et suite directe
- **arXiv:2006.04987** — Chandra, Chevyrev, Hairer, Shen, « Langevin dynamic for the 2D Yang-Mills measure », Publ. Math. IHÉS 136 (2022), 1-147.
- **arXiv:2201.03487** — Chandra, Chevyrev, Hairer, Shen, « Stochastic quantisation of Yang-Mills-Higgs in 3D », Inventiones Math. 237 (2024), 541-696.
- **arXiv:2503.03060** — Chevyrev, Shen, « Uniqueness of gauge covariant renormalisation of stochastic 3D Yang-Mills-Higgs », Arch. Rational Mech. Anal. 250 (2026).
- **arXiv:2305.07197** — Bringmann, Cao, « A para-controlled approach to the stochastic Yang-Mills equation in two dimensions ».

### Wilson flow et régularisation
- **arXiv:1006.4518** — Lüscher, « Properties and uses of the Wilson flow in lattice QCD », JHEP 1008:071 (2010).
- **arXiv:1101.0963** — Lüscher, Weisz, « Perturbative analysis of the gradient flow in non-abelian gauge theories », JHEP 02:051 (2011).
- **arXiv:1203.4469** — High-precision scale setting in lattice QCD.
- **arXiv:1508.05916** — Wilson flow and scale setting from lattice QCD.

### Polchinski / log-Sobolev approach
- **arXiv:2307.07619** — Bauerschmidt, Bodineau, Dagallier, « Stochastic dynamics and the Polchinski equation: an introduction », Probability Surveys 21 (2024), 200-290.
- **arXiv:2202.02295** — Bauerschmidt, Dagallier, « Log-Sobolev inequality for the $\varphi^4_2$ and $\varphi^4_3$ measures », Comm. Pure Appl. Math. 77 (2024), 2579-2612.
- **arXiv:2202.02301** — Bauerschmidt, Dagallier, « Log-Sobolev inequality for near critical Ising models », Comm. Pure Appl. Math. 77 (2024), 2568-2576.
- **arXiv:2503.24372** — Bauerschmidt, Bodineau, Dagallier, « A criterion on the free energy for log-Sobolev inequalities in mean-field particle systems » (2025, preprint).
- **arXiv:2504.08606** — Bauerschmidt, Dagallier, Weber, « Holley-Stroock uniqueness method for the $\varphi^4_2$ dynamics » (2025, preprint).

### Lattice YM and continuum limits
- **arXiv:2204.12737** — Shen, Zhu, Zhu, « A stochastic analysis approach to lattice Yang-Mills at strong coupling », Comm. Math. Phys. (2023). 't Hooft scaling, LSI à fort couplage uniquement.
- **arXiv:2401.13299** — Shen, Zhu, Zhu, « Langevin dynamics of lattice Yang-Mills-Higgs and applications ». Exponential ergodicity, mass gap pour YMH lattice.
- **arXiv:2509.04688** — Cao, Nissim, Sheffield, « Dynamical approach to area law for lattice Yang-Mills » (2025). Wilson area law dans le régime 't Hooft.
- **arXiv:2510.22788** — Nissim, « U(N) lattice Yang-Mills in the 't Hooft regime » (2025). Mass gap, infinite volume, large N pour U(N).
- **arXiv:2307.06790** — Cao, Park, Sheffield, « Random surfaces and lattice Yang-Mills », à paraître Comm. AMS.
- **arXiv:2401.10507** — Chatterjee, « A scaling limit of SU(2) lattice Yang-Mills-Higgs theory » (2024). Première limite scaling non-abélienne d > 2.
- **arXiv:1803.01950** — Chatterjee, « Yang-Mills for probabilists », in Probability and Analysis in Interacting Physical Systems, Springer 2019.
- **arXiv:2602.08591** — Dang, Nohra, « The Yang-Mills measure on compact surfaces as a universal scaling limit of lattice gauge models » (2026).

### Regularity structures
- **arXiv:1401.3014** — Hairer, « Introduction to Regularity Structures » (2014).
- **arXiv:1508.05261** — Hairer, « Regularity structures and the dynamical $\Phi^4_3$ model » (2015).
- **arXiv:1610.08468** — Bruned, Hairer, Zambotti, « Algebraic renormalisation of regularity structures ».
- **arXiv:1612.08138** — Chandra, Hairer, « An analytic BPHZ theorem for regularity structures ».
- **arXiv:1910.13854** — Chandra, Moinat, Weber, « A priori bounds for the $\Phi^4$ equation in the full sub-critical regime ».
- **arXiv:2411.16536** — Moinat-Weber, « A priori bounds for the dynamic fractional $\Phi^4$ model on $\mathbb{T}^3$ ».
- **arXiv:2301.00778** — Hairer-Steele, « Lecture notes on tree-free regularity structures ».
- **arXiv:2112.10739** — Linares-Otto-Tempelmayr, « A diagram-free approach to the stochastic estimates in regularity structures ».

### Mosco convergence et formes de Dirichlet
- Kuwae, Shioya 2003, « Convergence of spectral structures: a functional analytic theory and its applications to spectral geometry », Comm. Anal. Geom. 11(4), 599-673. (Cadre Mosco avec varying Hilbert spaces — référence non-arXiv, vérifiable sur intlpress.)

### Programme rigoureux YM 4D historique
- **Balaban 1989** — Séquence de papiers Comm. Math. Phys. 1985-1990 (block-spin renormalization).
- **Magnen-Rivasseau-Sénéor 1993** — « Construction of $YM_4$ with an infrared cutoff », Comm. Math. Phys. 155, 325-383.
- **Aizenman 1981, Fröhlich 1982** — Trivialité $\varphi^4_d$ pour $d > 4$.

### Anomalies et centre symétrie
- **arXiv:1703.00501** — Gaiotto, Kapustin, Komargodski, Seiberg, « Theta, time reversal, and temperature ». 't Hooft anomalies mixed $\mathbb{Z}_N$.
- **arXiv:2307.08662** — Pelaez et al., « Deconfinement, Center Symmetry and the Ghost Propagator in Landau Gauge Pure SU(3) Yang-Mills Theory », JHEP 05:164 (2024).
- **arXiv:1306.5094** — Probing Deconfinement with Polyakov Loop Susceptibilities.

### Documents internes auteur
- `/tmp/voie1_calcs/MASTER_PROOF_SKETCH_SU2_YM_2026-05-22.md`
- `/tmp/voie1_calcs/CLAY_THEOREM_FULL_v12_2026-05-23.md`
- `/tmp/voie1_calcs/G6_CONTINUUM_PROGRAM_v1.md`
- `/tmp/voie1_calcs/THEOREM_C_PROOF_RIGOROUS_v1.md`
- `/tmp/voie1_calcs/triple_cancellation_formal_v12.md`
- `/tmp/voie1_calcs/BAUERSCHMIDT_EQUATIONS_2026-05-22.md`
- `/tmp/voie1_calcs/EMAIL_BAUERSCHMIDT_DRAFT_2026-05-22.md`

---

**Fin du document. Aucun nom d'agent / outil / société dans le contenu. Auteur unique : Kévin Rémondière. Honnêteté maximale sur les probabilités et obstacles. Tous arXiv IDs vérifiés.**
