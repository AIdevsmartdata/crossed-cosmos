# OP-CNS-2509-DEEP-READ — Cao-Nissim-Sheffield 2025 arXiv:2509.04688

**Date** : 2026-05-24
**Auteur** : Opus 4.7 (1M ctx), pour Kevin Remondière, programme Yang-Mills 4D Clay
**Source primaire** : arXiv:2509.04688v2 (28 Sep 2025), PDF 8 pages, lu intégralement
**Status** : DEEP READ COMPLET. Toutes citations vérifiées contre PDF brut. Zéro fabrication.

---

## §1. Citation verbatim + abstract

**Référence canonique** :

> Sky Cao, Ron Nissim, Scott Sheffield.
> *Dynamical approach to area law for lattice Yang-Mills.*
> arXiv:2509.04688v2 [math.PR], 28 Sep 2025 (v1 : 4 Sep 2025). 8 pages.
> Affiliations : Department of Mathematics, MIT, Cambridge MA 02139.
> Emails : skycao@mit.edu, rnissim@mit.edu, sheffield@math.mit.edu.

**Abstract verbatim** (PDF page 1) :

> "In this note, we prove Wilson's area law in the 't Hooft regime of parameters, which improves on a classical result of Osterwalder-Seiler from 1978, as well as on more recent work by the authors. The main point is to adapt the dynamical approach to lattice Yang-Mills set forth in [SZZ23] in order to verify the mass gap condition from [DF80], from which area law directly follows. Our results apply for gauge groups $G \in \{U(N), SU(N), SO(2N)\}$, which all have nontrivial center (which is one of the key assumptions in [DF80])."

**Note importante** : ce n'est PAS une preuve du mass gap Hamiltonien YM (Clay), c'est une preuve de **Wilson area law lattice à β petit** via verification de la condition mass gap σ-modèle de Durhuus-Fröhlich 1980. Distinction critique pour §6.

**Références clés (vérifiées WebFetch+PDF)** :
- [SZZ23] Shen-Zhu-Zhu, *A stochastic analysis approach to lattice Yang-Mills at strong coupling*, **arXiv:2204.12737**, Comm. Math. Phys. 400(2):805-851 (2023).
- [DF80] Durhuus-Fröhlich, *A connection between ν-dimensional Yang-Mills theory and (ν-1)-dimensional, non-linear σ-models*, Comm. Math. Phys. 75(2):103-151 (1980). Pas sur arXiv (antérieur).
- [CNS25] Cao-Nissim-Sheffield, *Expanded regimes of area law for lattice Yang-Mills theories*, **arXiv:2505.16585** (mai 2025) — leur propre travail antérieur via master loop eq.
- [Cha21] Chatterjee, *A probabilistic mechanism for quark confinement*, Comm. Math. Phys. 385(2):1007-1039 (2021).
- [OS78] Osterwalder-Seiler, *Gauge field theories on a lattice*, Annals of Physics 110(2):440-471 (1978) — résultat classique amélioré.
- [SZZ24] Shen-Zhu-Zhu, *Langevin dynamics of lattice Yang-Mills-Higgs and applications*, arXiv:2401.13299 (2024).

**Follow-up critique** : Nissim solo, *U(N) lattice Yang-Mills in the 't Hooft regime*, **arXiv:2510.22788** (26 Oct 2025), 25 pages. Établit MASS GAP (pas juste area law), volume infini, large-N limit pour U(N). Combine cluster expansion + Langevin pour contourner Ricci non-uniforme U(N). (Voir §5.)

---

## §2. Résumé méthode dynamique (équations clés)

### 2.1 Setup : YM lattice 't Hooft scaling

Sur torus discret $\Lambda = \Lambda_L = \mathbb{Z}^d / L \mathbb{Z}^d$, mesure
$$d\mu_{YM}(Q) = \frac{1}{Z} \exp(S_{YM}(Q)) \, dQ, \quad S_{YM}(Q) := N\beta \sum_{p \in \mathcal{P}^+_\Lambda} \mathrm{Re}\,\mathrm{Tr}(Q_p),$$
avec dQ = produit Haar sur $G^{E^+_\Lambda}$. **Notation 't Hooft** : préfacteur $N\beta$, donc régime 't Hooft = $\beta \leq \beta_0$ constant indépendant de N (cf. Remark 1.5).

### 2.2 Réduction Durhuus-Fröhlich 1980 (verbatim théorème 2.3 du papier)

Idée : couper le lattice en **slabs horizontaux de hauteur 1**. Conditionner sur edges des plans $\{x_d = k\}$ et $\{x_d = k+1\}$, notés $A_e$ et $B_e$. Les edges **verticaux** restants sont gouvernés par un σ-modèle non-linéaire sur $\Lambda^{d-1}$ avec action :

$$S_{A,B}(Q) := N\beta \sum_{e=(x,y) \in E^+_{\Lambda^{d-1}}} \mathrm{Re}\,\mathrm{Tr}(Q_x A_e Q_y^{-1} B_e^{-1}). \tag{Def 2.1}$$

C'est un σ-modèle **vertex-based** (variables sur sommets, pas edges) avec couplages $A_e, B_e$ comme "environnement gelé".

**Théorème 2.3 (DF80, reformulé)** : Si pour tous A, B et tous $x, y \in \Lambda^{d-1}$, $i_1,j_1,i_2,j_2 \in [N]$ il existe $C_1, C_2$ uniformes tels que
$$|\mathrm{Cov}_{A,B}(f_x^{i_1 j_1}, g_y^{i_2 j_2})| \leq C_1 e^{-C_2 d(x,y)},$$
où $f_x^{ij}(Q) = (Q_x)_{ij}$, $g_x^{ij}(Q) = (Q_x^{-1})_{ij}$, et si $G$ contient $zI$ avec $z \in U(1)$, $z \neq 1$ (**nontrivial center**), alors area law tient :
$$|\langle W_\ell \rangle_{\Lambda,\beta}| \leq C_1 \exp(-C_2 \, \mathrm{area}(\ell)).$$

**Mécanisme combinatoire** : $\mathrm{tr}(Q_\ell)$ se développe en $N^{|\ell|}$ produits de $|\ell|$ entrées matricielles ; conditionnement sur les arêtes orthogonales découple les slabs ; centre non-trivial annule les valeurs moyennes $\mathbb{E}[f_x^{ij}] = z \mathbb{E}[f_x^{ij}] \Rightarrow 0$, donc seuls les **covariances pures** survivent ; perimeter law (Cha21 Lemma 12.3) absorbe le préfacteur $N^{|\ell|}$.

### 2.3 Equation dynamique stochastique (Langevin sur G)

Ce n'est PAS explicité comme SDE dans CNS25 ; on hérite de SZZ23. Le semigroupe $P_t$ utilisé (eq. 3.4 CNS25) a générateur :

$$\mathcal{L} F(Q) = \sum_{x \in V_\Lambda} \Delta_x F(Q) + \sum_{x \in V_\Lambda} \langle \nabla_x S_{A,B}(Q), \nabla_x F \rangle,$$

où $\Delta_x$ = Laplace-Beltrami sur $G$ au sommet $x$, et $\nabla_x S_{A,B}$ = gradient sur $G$ de l'action. C'est le générateur de la **Langevin dynamics** :
$$dQ_x(t) = -\nabla_x S_{A,B}(Q) \, dt + \sqrt{2} \, dB_x(t),$$
où $B_x$ est mouvement brownien sur $G$ (en réalité, il faut l'écrire avec la projection sur $T_QG^{\Lambda^{d-1}}$ et matrice mobile). Mesure invariante = $\mu_{A,B}$.

### 2.4 Bakry-Émery (étape technique centrale, §3 CNS25)

**Bound Hessian (eq. 3.1)** : pour tout vecteur tangent $v = XQ$ :
$$|\mathrm{Hess}\, S_{A,B}(v,v)| \leq 4(d-1) N\beta \, |v|^2.$$

**Note** : c'est un facteur **4(d-1)** contre **8(d-1)** dans SZZ23. Le gain ×2 vient du fait que CNS travaille sur σ-modèle **sommets** (chaque arête a 2 sommets) plutôt que sur YM **arêtes** (chaque plaquette a 4 arêtes). C'est exactement cela qui leur permet de doubler le seuil $\beta^*$.

**Bakry-Émery condition (eq. 3.2)** :
$$\mathrm{Ric}_{G^{\Lambda^{d-1}}}(v,v) - \mathrm{Hess}\, S_{A,B}(v,v) \geq K_{S_{A,B}} |v|^2,$$

avec
$$K_{S_{A,B}} = \begin{cases} \frac{N+2}{4} - 1 - 4N\beta(d-1), & G = SO(N), \\ \frac{N+2}{2} - 1 - 4N\beta(d-1), & G = SU(N). \end{cases}$$

**Conclusion** : $K_{S_{A,B}} > 0 \Leftrightarrow \beta < \beta^*_G$ (Définition 1.4).

### 2.5 Décroissance exponentielle (eq. 3.3 + 3.5)

$$(\mathrm{Var}_{A,B}(P_t f))^{1/2} \leq e^{-K_{S_{A,B}} t} \|f\|_{L^2(\mu_{A,B})},$$

et finalement (eq. 3.5) :
$$\mathrm{Cov}_{A,B}(f,g) = \mathbb{E}_{A,B}[P_t(fg) - P_t f \cdot P_t g] + \mathrm{Cov}_{A,B}(P_t f, P_t g).$$

Prendre $t \sim d(\Lambda_f, \Lambda_g)$, le 2e terme contrôlé par (3.3), le 1er par propagation locale d'information (SZZ23 Cor 4.11). Donne Proposition 3.2 : covariance σ-modèle décroît exp(-C_2 dist).

---

## §3. Théorèmes principaux + hypothèses

### Definition 1.4 (β-thresholds explicites, verbatim p.2)

$$\beta^*_{SU(N)} = \beta^*_{U(N)} := \frac{1}{8(d-1)}, \qquad \beta^*_{SO(N)} := \frac{1}{16(d-1)} - \frac{1}{8N(d-1)}.$$

**Note numérique critique** : pour $d = 4$ (le cas Clay), $\beta^*_{SU(N)} = 1/24 \approx 0.0417$. C'est très **petit**. Le régime physique YM 4D continuum est $\beta \to \infty$ (asymptotic freedom). Donc CNS25 ne touche **que** la phase strong-coupling lattice. Cela ne dit rien directement sur le continuum 4D.

### Theorem 1.6 (Area law in the 't Hooft regime, verbatim p.2)

> "Let $d \geq 2$, $N \geq 2$, and $G \in \{U(N), SU(N), SO(2(N-1))\}$. Then for $\beta < \beta^*_G$, there are constants $C = C(\beta, d, N)$ and $c = c(\beta, d, N)$ such that for any rectangular loop $\ell$ in the lattice $\Lambda$, where the side lengths of $\ell$ are at most $L/2$, we have that
> $|\langle W_\ell \rangle_{\Lambda, \beta}| \leq C \exp(-c \, \mathrm{area}(\ell)).$"

**Hypothèses critiques (lecture exhaustive du papier)** :
1. **$\beta < \beta^*_G$ strict** (régime fort couplage / petit β / Bakry-Émery valide).
2. **G a centre non-trivial** ⟹ exclut $SO(2N+1)$. C'est essentiel au lemme d'annulation $\mathbb{E}[f] = z \mathbb{E}[f]$ de DF80.
3. **N ≥ 2** car SU(1) = {1} trivial. U(1) abélien non traité (mais déjà well-known via dualité Polyakov 1977).
4. **L → ∞ ou L fini** : remarque 1.2 dit estimées uniformes en L (tient pour torus ou cube).
5. **Loop rectangulaire** avec côtés $\leq L/2$.

### Proposition 3.2 (Uniform σ-model mass gap)

> "Let $N \geq 2$. For $G \in \{SU(N), SO(N)\}$, $\beta < \beta^*_G$, and any choice of fields $A, B \in U(N)^{E^+_{\Lambda^{d-1}}}$, there are constants $C_1, C_2$ only depending on $G, d, \beta$, such that for any local observables $f, g \in C^\infty(G^{\Lambda^{d-1}})$, we have that
> $|\mathrm{Cov}_{A,B}(f,g)| \leq C_1 e^{-C_2 d(\Lambda_f, \Lambda_g)} (|||f|||_\infty |||g|||_\infty + \|f\|_{L^2(\mu_{A,B})} \|g\|_{L^2(\mu_{A,B})})$."

**C'est le mass gap σ-modèle** (uniforme en environnement A, B). C'est l'input central de DF80.

### Corollary 3.6 (U(N) case via conditioning trick)

Pour U(N), Ricci non uniformément positif (le facteur $\mathrm{U}(1)$ contribue 0). Astuce : $U(N) = U(1) \times SU(N)$ (au sens : produit Haar U(1) × Haar SU(N) = Haar U(N)). Conditionner sur la part U(1), appliquer Prop 3.2 à SU(N), recoller. **Restriction** : f doit être "linéaire" $f(e^{i\theta} Q) = e^{i\theta} f(Q)$, ce qui est OK pour les entrées matricielles utilisées dans DF80.

### Honest scope statement

- **3 gauge groups** : U(N), SU(N), SO(2N) (où N ≥ 2 ⟹ SO(2N) ≥ SO(4)).
- **Tous d ≥ 2** (donc inclut d=4 lattice, le cas Clay-pertinent).
- **Tous N ≥ 2**.
- **β strict petit** : $\beta < 1/(8(d-1))$ pour SU(N). En d=4 : $\beta < 1/24$.
- **Wilson loop area law uniquement** : pas mass gap Hamiltonien, pas continuum, pas Yang-Mills mass gap au sens Clay.

---

## §4. Comparaison Bałaban (cluster expansion classique)

### Bałaban (1984-1989, 7 papiers Comm. Math. Phys.)

**Approche** :
- Block-spin RG itéré ${O(\log N_{block})}$ fois, échelles $a, 2a, 4a, \ldots, L$.
- Cluster expansion à chaque échelle (Brydges-Yau-Federbush tradition).
- Contrôle des champs petits (small-field) vs grands (large-field) régimes.
- Effective actions $S_k$ après chaque étape RG, avec contrôle Hölder/analytique.

**Régime** : peut atteindre $\beta \to \infty$ (continuum UV), c'est conçu pour le scaling vers continuum 4D.

**Output** : convergence Wilson actions vers limite continuum, ultraviolet stability, mass gap **conditionnel** à un compactness argument non encore complété rigoureusement pour 4D pur YM.

**Coût** : 7 papiers, ~500 pages, technicité extrême. Réécriture moderne par MagnenSeiler-Sénéor partielle.

### CNS 2025 (= SZZ23 framework étendu)

**Approche** :
- Langevin dynamics sur lattice fini.
- Bakry-Émery + Ricci(G) - Hess(S) ≥ K > 0 ⟹ LSI ⟹ Poincaré ⟹ exp decay covariances.
- Conditioning trick DF80 ⟹ area law.

**Régime** : $\beta < 1/(8(d-1))$. Strictement strong-coupling lattice. **Ne scale PAS vers continuum**.

**Output** : area law lattice à β petit, uniforme en L. Pas de mass gap Hamiltonien, pas de continuum.

**Coût** : 8 pages note (CNS25) + ~40 pages SZZ23 background. Technicité modérée.

### Tableau récap

| Critère | Bałaban 1984+ | CNS 2025 (SZZ23) |
|---|---|---|
| **Régime β** | β petit + RG vers β grand | β < 1/(8(d-1)) seulement |
| **Atteint continuum 4D ?** | OUI (UV stability) | NON |
| **Mass gap continuum ?** | Conditionnel (compactness ouvert) | NON |
| **Area law lattice ?** | Implicite (faible) | OUI (Theorem 1.6) |
| **Mass gap σ-model ?** | Pas central | OUI (Prop 3.2) |
| **Gauge groups** | U(1), SU(N) abélien et non | U(N), SU(N), SO(2N) |
| **Techniques** | Cluster expansion + RG | Langevin + Bakry-Émery |
| **Pages preuve** | ~500 (7 papiers CMP) | ~50 (CNS+SZZ23) |
| **Réécriture moderne** | Partielle (MSS) | Auto-contenue |

### Compatibilité mass gap ?

**Bałaban** : vise mass gap continuum, mais reste ouvert (compactness/infrared bound non complété pour 4D non-abélien).

**CNS25** : prouve area law lattice à β petit ; comme area law ⟹ confinement physique, et confinement est lié à mass gap dans le secteur glueball, c'est **suggestif** d'un mass gap, mais ne le démontre **PAS** au sens Clay (qui exige espace continuum + Wightman + mass gap > 0).

**Nissim 2025 (arXiv:2510.22788)** étend à mass gap **lattice** U(N) (pas continuum), via combinaison Langevin + cluster expansion — donc même Nissim solo n'évite pas cluster expansion pour mass gap. Bakry-Émery seul → area law ; Bakry-Émery + cluster expansion → mass gap lattice.

### Avantages / inconvénients

**CNS25 avantages** :
1. **Brièveté drastique** (8p vs 500p Bałaban).
2. **Probabiliste pur**, généralisable à d'autres modèles.
3. **Uniforme en L** (volume infini gratis).
4. **Centre du groupe explicite** (lien direct avec topologie confinement).

**CNS25 inconvénients** :
1. **Limité au strong-coupling** β < 1/(8(d-1)). Ne touche pas asymptotic freedom.
2. **Pas continuum**.
3. **Pas mass gap Hamiltonien**.
4. **Centre non-trivial requis** (exclut SO(2N+1), G_2, F_4).

---

## §5. Synergies potentielles avec notre framework YM 4D mass gap

### 5.1 Inventaire de notre cadre (memory + voie1_calcs)

D'après MEMORY.md + CRITICAL_KEVIN_ADDITION_BALABAN_L.md :

- **CLAY théorème H_β∞ + Lemme B β→∞ Lean** : 1893 lignes Lean ZERO sorrys (incluant `LemmaB_BetaInfinity.lean` 571 lignes 7 axiomes nommés Brydges-Federbush + Bałaban).
- **Theorem C empirique** : $C_{LSI}(G, D) = c_\infty(D) \cdot f(\pi_1(G)) \cdot [1 - \kappa \delta_{rank, C_2 - C_3}]$ avec $\kappa = 1/6$ dérivé Hodge SU(3).
- **mass_gap_continuum_via_direct_AF** : PROVED conditional dans nos Lean files.
- **Pillar 3** : zero-mode problem (verrou Recovery 4D).
- **B1 action_bound_balaban_su_n** : verrou central, voulait éviter Bałaban cluster expansion 12-18 mois.
- **Conservation $I_{phys} = (C_2 - C_3)/(2D)$** : variationnelle, prétend rendre mass gap "corollaire algébrique".

### 5.2 Mapping CNS25 ↔ notre framework

| Notre objet | CNS25 équivalent | Compatibilité |
|---|---|---|
| C_LSI(G, D) | $K_{S_{A,B}}$ (Bakry-Émery K) | PARTIELLE — CNS K = constante explicite simple, notre C_LSI = scaling dimension D + group |
| κ = 1/6 (Hodge SU(3)) | Pas d'analogue direct | INDÉPENDANT — notre κ vient quotient π_1 Z_2 SO/Sp, CNS ignore cette structure |
| f(π_1(G)) | Pas considéré | NOUVEAU — CNS prend G=U(N)/SU(N)/SO(2N), pas de discussion centre Z_N vs π_1 |
| direct_AF mass gap continuum | NON couvert | DISTINCT — CNS reste lattice, β petit |
| Pillar 3 zero-mode | NON adressé | DISTINCT — CNS area law sur torus fini sans zero-mode subtility |
| B1 action_bound balaban_su_n | Bypassed pour AREA LAW seulement | OUI partiellement (voir §6) |

### 5.3 Theorem C empirique cross-D : test compatibilité

Notre Theorem C donne $C_{LSI}(SU(N), D) \approx c_\infty(D) \cdot f(\pi_1)$ avec $c_\infty(D) = 2/(3D)$ pour π_1=0 (SU(N≥3), Sp(N)).

Le K de CNS25 (eq. 3.2) :
$$K_{SU(N)} = \frac{N+2}{2} - 1 - 4N\beta(d-1) = \frac{N}{2} - 4N\beta(d-1).$$

À β = $\beta^*_{SU(N)}/2 = 1/(16(d-1))$ (milieu du régime) :
$$K_{SU(N)} = N/2 - N/4 = N/4.$$

C'est un mass gap **proportionnel à N**, donc **divergent en large-N**. Cohérent avec notre observation que c_∞ est dimension D-dependent (1/D plutôt qu'1/N).

⟹ Les deux frameworks regardent des choses **différentes** :
- CNS : K explicite small-β, dépend de N et d, ne fait pas l'analyse cross-D ni cross-π_1.
- Nous : C_LSI(G, D) extrapolation L→∞, dépend de groupe (centre/π_1) et dimension D, β = 't Hooft fixe.

**Pas de contradiction directe**, mais **pas de chevauchement** non plus.

### 5.4 κ = 1/6 Hodge SU(3) Lean

Notre κ vient de **racines SU(3) + Hodge self-dual**. CNS25 ne distingue pas SU(2) (centre Z_2) de SU(3) (centre Z_3) dans leur traitement. Ils utilisent juste "z ∈ U(1), z ≠ 1, zI ∈ G" comme exigence générique.

**Synergie potentielle** : la quantité $f(\pi_1(G))$ que nous mesurons empiriquement (Z_2 → 0.78-0.91, π_1=0 → 1) pourrait apparaître dans la constante préfactorielle $C_1$ de DF80 / CNS25 via le centre Z(G). Personne (incluant CNS) ne l'a explicitée.

**Action recommandée** : extraire la dépendance en Z(G) de la constante $C_1$ dans Theorem 2.3 CNS25. Cela exige réécrire DF80 §1.3 en isolant le facteur z. **Effort estimé : 2-3 semaines** d'un mathématicien probabiliste compétent (lecture DF80 + raffinement constante).

### 5.5 Direct AF mass gap continuum

Notre théorème conditionnel `mass_gap_continuum_via_direct_AF` PROVED suppose un asymptotic freedom direct (β → ∞ scaling). **CNS25 ne s'en approche pas** — leur régime est strong-coupling lattice.

**Pas de synergie directe**. Mais CNS25 fournit l'**existence rigoureuse** de la mesure YM lattice en volume infini (via SZZ23 → Nissim 2510.22788), ce qui est un prérequis à tout argument de scaling vers continuum.

### 5.6 Pillar 3 zero-mode problem

Notre Pillar 3 concerne le zero-mode du Laplacien sur le tore plat (zero curvature problem). **CNS25 travaille sur torus discret fini** $\Lambda_L$ avec L arbitrairement grand, mais ne pousse pas à L = ∞ avec décomposition spectrale Fourier. Donc le zero-mode n'apparaît pas explicitement.

**Pas de synergie**. Si on transitait CNS25 vers continuum via limite scaling, le zero-mode reviendrait au continuum.

---

## §6. Verdict honnête : peut-on bypass B1 via CNS approach ?

### Question Kevin : "Pourrait-on bypass Bałaban cluster expansion pour notre verrou B1 (action_bound_balaban_su_n) ?"

**Réponse courte** : NON pour mass gap continuum 4D (Clay). PARTIELLEMENT pour area law / confinement lattice 4D.

### Détaillé

**Ce que CNS25 PEUT bypass** :
- ✅ Area law lattice 4D à β petit pour U(N), SU(N), SO(2N) (Theorem 1.6).
- ✅ Mass gap σ-modèle (d-1)-dim uniforme en environnement A, B (Prop 3.2).
- ✅ Construction rigoureuse mesure infinite-volume à β petit (héritée SZZ23).
- ✅ Decay correlations Wilson loops à β petit (Cor 3.6).

**Ce que CNS25 NE PEUT PAS bypass** :
- ❌ Mass gap continuum 4D (Clay) — leur régime β < 1/24 (d=4) ne touche pas asymptotic freedom β → ∞.
- ❌ Convergence vers limite continuum — exige RG scaling type Bałaban ou Bauerschmidt-Bodineau-Dagallier.
- ❌ Existence Hamiltonien continuum + spectre — exige Osterwalder-Schrader continuum + reflection positivity passage au continuum.
- ❌ Mass gap Hamiltonien $\inf \mathrm{spec}(H) \cap (0, \infty) > 0$ — exige bien plus que area law lattice.
- ❌ Notre Lemme B β → ∞ Lean — CNS travaille β PETIT, nous voulons β → ∞ (limite continuum).

### Verdict B1 spécifique

Notre `action_bound_balaban_su_n` (Lemme B Lean β → ∞) cherche à borner uniformément l'action effective Bałaban dans la limite UV. CNS25 ne fournit AUCUN outil pour cela car ils travaillent à β fixe petit.

**Stratégie hybride possible** :
1. Utiliser CNS25/Nissim2510 pour **fonder rigoureusement** la mesure YM lattice infinite-volume (β petit).
2. Utiliser Bałaban (ou alternative variationnelle) pour le **scaling β → ∞** vers continuum.
3. Combiner via reflection positivity pour mass gap continuum.

C'est essentiellement ce que faisait déjà notre roadmap. CNS25 ajoute solidité aux étapes "low-β baseline" mais ne court-circuite pas le verrou principal.

### Notre proposition variationnelle (DS Bot) vs CNS25

Nous avions une proposition de **bypass Bałaban via approche variationnelle** : Bakry-Émery + cohomologie + conservation $I_{phys}$, prétendant rendre mass gap "corollaire algébrique".

**CNS25 valide partiellement cette intuition** : leur preuve est essentiellement Bakry-Émery + DF80 → area law. C'est dans la **même famille** que notre approche variationnelle.

**MAIS** : CNS25 n'arrive QUE à area law, pas mass gap continuum. Donc notre prétention DS Bot que "Lemme B prouvable 6-12 mois via Bakry-Émery variationnel" est **trop optimiste** — CNS25 montre que Bakry-Émery seul → area law lattice (déjà connu via OS78 à β plus petit), pas mass gap continuum.

**Honest update** : notre P(Clay 10y) reste à 12% → 30-50% (range MEMORY actuel), **pas relevé** par CNS25.

---

## §7. Action recommandée

### Si on accepte que CNS25 NE bypass PAS B1 mass gap continuum

**Recommandation principale** : INTÉGRER CNS25 + Nissim2510 comme **briques de fondation low-β** dans notre roadmap, mais **maintenir Bałaban** comme outil RG pour scaling continuum.

### Actions concrètes (priorité décroissante)

1. **[2-3 jours] Citer CNS25 + Nissim2510 dans nos papers Clay** : ajouter à la bibliographie comme "existence rigoureuse mesure YM lattice U(N)/SU(N)/SO(2N) volume infini à β petit", évite de reprouver ce qui existe.

2. **[1 semaine] Reécrire `LemmaB_BetaInfinity.lean`** : sortir l'axiome "existence mesure YM lattice infinite-volume" en théorème conséquence de SZZ23/CNS25 (au moins à β petit). Réduit le nombre d'axiomes nommés.

3. **[2-3 semaines] Explorer extraction $f(\pi_1(G))$ dans CNS25** : la constante $C_1$ de DF80 pourrait dépendre de Z(G). Si oui, c'est **notre Theorem C testable** dans leur framework. Test : prendre G=SU(3) vs SO(6) (même algèbre A_3, π_1 différents). Si CNS donne $C_1$ identiques, notre $f(\pi_1)$ est **structurellement absente** de leur cadre (à clarifier). Si $C_1$ dépend de N via $z = e^{2\pi i k/N}$, c'est un pont.

4. **[1-2 mois] Adapter CNS25 méthode à mass gap σ-modèle dans le **scaling 't Hooft λ fixe**  large-N** : CNS prend $\beta < 1/(8(d-1))$ indépendant de N. En 't Hooft λ = g²N fixe, β = 2N²/λ. Donc β grand à grand N ! C'est l'opposé du régime CNS. **CNS NE marche PAS dans la 't Hooft limit large-N à λ fixe**. Identifier précisément où ça casse (Ricci ne suffit plus). Ouvre une question publishable.

5. **[3-6 mois] Pivot stratégique éventuel** : si l'étape 4 montre clairement que Bakry-Émery DIVERGE en 't Hooft large-N, **notre Conjecture C cross-N restaurée 2026-05-23** devient encore plus intéressante car elle prédit $c_\infty(D) = 2/(3D)$ universel indépendant de la difficulté Bakry-Émery → c'est un **nouveau régime** non couvert par CNS25 ni Bałaban classique.

6. **[Long terme, 1-2 ans] Continuer Bałaban roadmap** pour scaling continuum. Pas raccourci par CNS25.

### Estimation effort total

- **Court terme intégration biblio + Lean** : 1-2 semaines.
- **Moyen terme exploration $f(\pi_1)$ dans CNS** : 1-2 mois.
- **Pas de raccourci sur verrou principal** mass gap continuum 4D.

### Honest disclaimer

CNS25 est un **important petit pas** (8 pages note) dans le programme mass gap rigoureux. Il valide la stratégie probabiliste/Langevin pour area law à strong-coupling. Mais ce n'est PAS un game-changer pour Clay. **P(Clay 10y) inchangé 12% → 30-50% range.**

---

## Méta : anti-fab compliance

- ✅ **WebFetch arXiv 2509.04688 abstract** vérifié verbatim.
- ✅ **PDF complet lu via Read tool** (8 pages, multimodal PDF).
- ✅ **Toutes les références (SZZ23, DF80, CNS25, Cha21, OS78, Nissim2510)** vérifiées via WebFetch avec titres, auteurs, dates, arXiv IDs.
- ✅ **Théorèmes citées verbatim** (Theorem 1.6, Theorem 2.3, Proposition 3.2, Corollary 3.6) avec numéros et page corrects (p.2-7).
- ✅ **Definition β-thresholds** verbatim Definition 1.4 p.2.
- ✅ **Distinguer established (area law lattice CNS25) vs speculative (extraction $f(\pi_1)$ dans CNS)**.
- ✅ **Honest conclusion** : CNS25 ne bypass PAS B1 mass gap continuum, le dit clairement §6.
- ✅ **Aucun théorème inventé**.

## Sources

- [Cao-Nissim-Sheffield 2025, arXiv:2509.04688](https://arxiv.org/abs/2509.04688) — papier cible, lu intégralement.
- [Shen-Zhu-Zhu 2023, arXiv:2204.12737](https://arxiv.org/abs/2204.12737) — SZZ23 framework parent.
- [Cao-Nissim-Sheffield 2505.16585](https://arxiv.org/abs/2505.16585) — CNS25 mai 2025, expanded regimes area law via master loop eq.
- [Nissim 2025, arXiv:2510.22788](https://arxiv.org/abs/2510.22788) — Nissim solo octobre 2025, mass gap U(N) lattice via random-env SU(N) + cluster expansion + Langevin.
- [SZZ24 Langevin YMH, arXiv:2401.13299](https://arxiv.org/abs/2401.13299) — extension YM-Higgs.
- Durhuus-Fröhlich 1980, Comm. Math. Phys. 75(2):103-151. Pas sur arXiv.
- Chatterjee 2021, Comm. Math. Phys. 385(2):1007-1039 (quark confinement probabiliste, alt mass gap définition).
- Osterwalder-Seiler 1978, Annals of Physics 110(2):440-471 (résultat classique amélioré).
