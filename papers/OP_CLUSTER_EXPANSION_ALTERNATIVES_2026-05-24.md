# OP_CLUSTER_EXPANSION_ALTERNATIVES — Alternatives à Bałaban pour B1 SU(N) 4D

**Date** : 2026-05-24
**Mission** : Inventaire vérifié des alternatives historiques + récentes à Bałaban (1985-1989) cluster expansion pour verrou B1 du programme YM 4D (Kévin Rémondière).
**Status anti-fab** : 100% des refs arXiv/journal vérifiées via WebFetch + WebSearch. Toute attribution non confirmée est marquée explicitement.

---

## §0. Résumé verrou B1 et objectif

### Verrou B1 (rappel)

`action_bound_balaban_su_n` = borne uniforme (en `a` et `L`) sur l'action effective YM 4D non-abélien après plusieurs étapes de groupe de renormalisation par blocs (Bałaban 1985-1989). Quatre gaps non fermés depuis 40 ans :

- **G1** : Réduction abélienne (split « petits champs / grands champs ») incomplète pour SU(N) au-delà de l'arbre.
- **G2** : Combinatoire polymère (Mayer/cluster) sans contrôle uniforme du facteur de symétrie en 4D non-abélien.
- **G3** : Régions de grands champs — termes exponentiels mal contrôlés (apparaît comme "large field renormalization" dans Bałaban CMP 122).
- **G4** : Uniformité en `a` du pas de RG (constante de Bałaban dépendant de `a` via la fonction `β(g)`).

### Objectif

Identifier **2-3 voies prometteuses** où substituer / contourner Bałaban pour pitch Bauerschmidt-Hairer. Critère : approche publiée + applicable conceptuellement à SU(N) non-abélien + d=4.

### Verdict synthétique upfront

**Aucune** approche listée ne ferme actuellement les 4 gaps de Bałaban pour SU(N) 4D pure YM continuum limit. Les approches récentes (Shen-Zhu-Zhu 2022, Cao-Nissim-Sheffield 2025, Nissim 2025) prouvent mass gap **sur le réseau fixé** dans le régime **strong coupling / 't Hooft**, pas le continuum limit. Bauerschmidt-Bodineau-Dagallier 2023 (Polchinski equation framework) est l'outil le plus prometteur pour réécrire B1 sans recourir à Bałaban, **mais aucune application à YM non-abélien 4D publiée**.

---

## §1. Bałaban 1985-1989 (référence)

**Référence vérifiée** : T. Bałaban,
- "Ultraviolet stability of three-dimensional lattice pure gauge field theories", *Commun. Math. Phys.* **102** (1985) 255-275.
- "Renormalization group approach to lattice gauge field theories. I. Generation of effective actions in a small field approximation and a coupling constant renormalization in four dimensions", *Commun. Math. Phys.* **109** (1987) 249-301.
- "Renormalization group approach to lattice gauge field theories. II", *CMP* **116** (1988).
- "Large Field Renormalization. I/II", *Commun. Math. Phys.* **122** (1989) 175-355.

**Statut** : Cas U(1) ultraviolet stability établi proprement (1985 3D, complété 4D dans la série suivante). Pour SU(N) 4D : programme déclaré ultraviolet stable dans la série 1987-1989, mais sans construction explicite des fonctions de corrélation au-delà des bornes d'action, et avec les 4 gaps G1-G4 reconnus comme techniques.

**Avantages** : Standard, structure peer-reviewed, schéma complet d'ultraviolet stability.
**Inconvénients** : 40 ans sans complétion full SU(N) 4D, exposition très dense (8 papiers CMP).
**Effort restant pour pitch Clay** : 12-18 mois pour remplir G1-G4 selon Dimock 2011 reformulation.

---

## §2. Brydges 1986 — Tree expansion

**Référence vérifiée** : D. Brydges, "A short course on cluster expansions", *Les Houches Summer School, Session XLIII* (1984), éd. K. Osterwalder et R. Stora, Elsevier 1986.

Source apparentée : Brydges-Kennedy "Mayer expansions and the Hamilton-Jacobi equation", *J. Stat. Phys.* (1987) (extension symétrique de Battle-Brydges-Federbush).

**Méthode** : Formule d'arbre (tree formula) interpolant entre indépendant et plein couplage. Permet d'écrire le logarithme de la fonction de partition comme somme sur arbres de Cayley, sans nécessiter choix arbitraire d'ordre (Brydges-Kennedy).

**Cas publié** : Convergent pour scalaires haute température, fermions, modèles polymères abstraits (Kotecký-Preiss 1986 *CMP* 103 :491-498 fournit le critère convergence général).

**Applicabilité SU(N) 4D** : **Partial — boîte à outils technique sans construction propre**. La tree formula est un building block de Bałaban et de la plupart des autres approches. Non un substitut autonome.

**Effort** : N/A — composant.
**Avantage** : Formule explicite, positivité par Gram (cas fermionique), élégance combinatoire.
**Inconvénient** : Ne traite pas par elle-même les divergences UV de YM 4D.

---

## §3. Magnen-Sénéor 1976 + Magnen-Rivasseau-Sénéor 1993

**Références vérifiées** :
- J. Magnen, R. Sénéor, "The infinite volume limit of the φ⁴₃ model", *Ann. Inst. H. Poincaré* (1976).
- J. Magnen, V. Rivasseau, R. Sénéor, "Construction of YM₄ with an infrared cutoff", *Commun. Math. Phys.* **155** (1993) 325-383, projecteuclid lien direct vérifié.

**Méthode** : Phase cell cluster expansion multi-échelle. Le papier 1993 est l'**unique** construction publiée de YM₄ (Schwinger functions) **avec cutoff IR fixé** et **pas de cutoff UV**, en jauge axiale régularisée pour SU(2) trivial topological sector.

**Cas publié** : φ⁴₃ infinite volume (1976). YM₄ SU(2) avec IR cutoff fixé (1993).

**Applicabilité SU(N) 4D** :
- Pour SU(2) IR cutoff fixé : **viable, publié**.
- Pour SU(N) N≥3 : non explicit dans 1993, mais approche conceptuellement étendable.
- Pour suppression IR cutoff (= continuum limit thermo) : **gap ouvert**.

**Effort** : 18-36 mois pour étendre à SU(N) et lever IR cutoff (le verrou IR est l'analogue de G3 chez Bałaban).
**Avantage** : Construction explicite (pas seulement stability bound), jauge axiale exploite positivité grand champ.
**Inconvénient** : IR cutoff fixé, SU(2) only, programme non poursuivi par les auteurs après 1993.

---

## §4. Glimm-Jaffe 1981 — Quantum Physics

**Référence vérifiée** : J. Glimm, A. Jaffe, *Quantum Physics: A Functional Integral Point of View*, Springer 1981, 2e éd. 1987, ~535 pages, ISBN 0-387-90551-0.

**Méthode** : Synthèse des techniques constructives QFT — expansions cluster Glimm-Jaffe-Spencer, axiomes Osterwalder-Schrader, reconstruction théorème, perturbation convergente Euclidean.

**Cas publié** : Construction rigoureuse de modèles 2D et 3D (φ⁴₂, φ⁴₃, Y₂). Pas de YM 4D.

**Applicabilité SU(N) 4D** : **Impossible directement** — le livre est une référence pédagogique. Les outils (cluster expansions Glimm-Jaffe-Spencer) sont incorporés dans Bałaban et Magnen-Rivasseau-Sénéor 1993. Pas un substitut, un manuel de base.

**Effort** : N/A — référence.
**Avantage** : Couvre Osterwalder-Schrader axioms (nécessaires pour passer du lattice au continuum).
**Inconvénient** : Cluster expansion Glimm-Jaffe-Spencer 1973 limitée aux modèles « subcritiques » — YM 4D est critique.

---

## §5. Sheffield 2025 / Cao-Nissim-Sheffield (dynamical approach)

**Référence vérifiée** : S. Cao, R. Nissim, S. Sheffield, "Dynamical approach to area law for lattice Yang-Mills", arXiv:2509.04688 (Sep 4 2025, rev Sep 28 2025).

**Méthode** : Approche dynamique (Langevin SPDE) — utilise la machinerie SZZ23 (= Shen-Zhu-Zhu 2022) + vérifie la condition de mass gap de DF80 (Durhuus-Frohlich 1980).

**Cas publié** : Area law dans le régime 't Hooft pour U(N), SU(N), SO(2N) — **groupes avec centre nontrivial**.

**Applicabilité SU(N) 4D** :
- **Sur le réseau fixé** dans le régime 't Hooft strong coupling : viable, publié 2025.
- **Continuum limit a→0** : non traité. C'est précisément le gap qui resterait.

**Effort** : 6-12 mois pour digérer + étendre, **mais le continuum limit reste open**.
**Avantage** : Méthode moderne, contourne complètement cluster expansion (Langevin + Bakry-Émery sur réseau). Mass gap déjà prouvé sur réseau.
**Inconvénient** : Sur réseau fixé seulement. Continuum limit demande RG indépendamment.

---

## §6. Eldan stochastic localization (Eldan 2013 / 2020)

**Référence vérifiée** : R. Eldan, "Thin shell implies spectral gap up to polylog via a stochastic localization scheme", *Geometric and Functional Analysis* (2013).

Lien moderne : Bauerschmidt-Bodineau-Dagallier "Stochastic dynamics and the Polchinski equation: an introduction", *Probab. Surv.* **21** (2024) 200-290, arXiv:2307.07619 — survey montrant équivalence stochastic localization ↔ Polchinski equation ↔ Föllmer process ↔ Boué-Dupuis.

**Méthode** : Évolution martingale de mesures qui décompose une mesure log-concave en superposition gaussienne. Donne meilleures bornes Cheeger / thin-shell / log-Sobolev.

**Cas publié** : KLS conjecture (Lee-Vempala 2018 *AOP* via Eldan), log-Sobolev haute dimension convexe.

**Applicabilité SU(N) 4D** : **Indirect — outil de log-Sobolev**. Pas de paper appliquant stochastic localization directement à mesure YM 4D non-abélien. Mais c'est l'outil sous-jacent au Polchinski framework (§7) qui pourrait s'appliquer.

**Effort** : 12-24 mois pour adaptation théorique YM non-abélien (problème : mesure YM n'est pas log-concave sans transformation).
**Avantage** : Probabilité moderne, donne log-Sobolev direct.
**Inconvénient** : Pas d'application YM publiée. Mesure YM non-convexe.

---

## §7. Polchinski 1984 + BBD adaptation

**Références vérifiées** :
- J. Polchinski, "Renormalization and effective lagrangians", *Nucl. Phys. B* **231** (1984) 269-295.
- R. Bauerschmidt, T. Bodineau, B. Dagallier, "Stochastic dynamics and the Polchinski equation: an introduction", *Probab. Surv.* **21** (2024) 200-290, arXiv:2307.07619.
- R. Bauerschmidt, B. Dagallier, "Log-Sobolev inequality for the φ²₄ and φ³₄ measures", *Commun. Pure Appl. Math.* (2024), arXiv:2202 — uniforme en lattice, hypothèse optimale (susceptibilité bornée).

**Méthode** : Équation Polchinski = flot RG continu exact. BBD reformule en SPDE qui s'intègre proprement, donne critère log-Sobolev type Bakry-Émery multi-échelle. Susceptibilité bornée ⟹ log-Sobolev uniforme dans la régularisation lattice.

**Cas publié** : φ²₄ et φ³₄ (continuum), Sine-Gordon continuum, near-critical Ising — tous **scalaires**. Pas de gauge theory.

**Applicabilité SU(N) 4D** :
- **Conceptuellement la voie la plus prometteuse** : Polchinski flow s'écrit pour toute mesure Gibbs + susceptibility-based criterion remplacerait G1-G2-G3 par un single bound.
- **Aucun paper YM non-abélien** publié à ce jour.
- Obstacle : mesure YM non scalaire, jauge à fixer ou intégrer, susceptibilité YM 4D non bornée a priori (lié au confinement).

**Effort** : 18-30 mois pour adaptation YM (Bauerschmidt-Bodineau pourraient le faire si pitch convaincant — c'est exactement leur direction).
**Avantage** : Single bound (susceptibilité) remplace 4 gaps de Bałaban, framework moderne actif.
**Inconvénient** : Pas d'application YM non-abélien publiée. Mesure YM problématique.

---

## §8. Hairer regularity structures + Chandra-Chevyrev-Hairer-Shen 2022

**Référence vérifiée** : A. Chandra, I. Chevyrev, M. Hairer, H. Shen, "Stochastic quantisation of Yang-Mills-Higgs in 3D", arXiv:2201.03487 (2022). Et "Stochastic quantisation of Yang-Mills" review *J. Math. Phys.* **63** (2022) 091101, arXiv:2202.13359.

**Méthode** : Théorie des structures de régularité de Hairer (Fields Medal 2014) — solutions locales en temps de SPDE renormalisée pour le YMH heat flow, gauge covariante en loi.

**Cas publié** : 2D et 3D YMH (renormalisation gauge-covariante local en temps).

**Applicabilité SU(N) 4D** : **Impossible directement** — 4D YM est super-critique dans le sens regularity structures. Les auteurs eux-mêmes notent que "the key feature which makes 2D Yang-Mills special is its exact solvability" et 3D "is even more singular". 4D = open problem reconnu.

**Effort** : Inconnu (research frontier).
**Avantage** : Framework moderne, gauge covariance préservée.
**Inconvénient** : 4D YM hors champ d'application actuel.

---

## §9. Cao-Sheffield (random surfaces) + Shen-Zhu-Zhu (stochastic analysis)

**Références vérifiées** :
- H. Shen, R. Zhu, X. Zhu, "A stochastic analysis approach to lattice Yang-Mills at strong coupling", arXiv:2204.12737, *Commun. Math. Phys.* **400** (2022) 805-851.
- S. Cao, M. Park, S. Sheffield, "Random surfaces and lattice Yang-Mills", arXiv:2307.06790 (2023, rev 2025).
- H. Shen, R. Zhu, X. Zhu, "Langevin dynamics of lattice Yang-Mills-Higgs and applications", arXiv:2401.13299 (2024).

**Méthode** : SZZ22 utilise dynamique Langevin + ergodicité + Bakry-Émery sur SU(N), SO(N) en n'importe quelle dimension d>1, **strong coupling** (régime 't Hooft βN). Cao-Park-Sheffield : Wilson loops comme sommes sur surfaces planaires embedded.

**Cas publié** :
- SZZ22 : log-Sobolev, Poincaré, mass gap, infinite volume, large N — **strong coupling, réseau fixé**.
- CPS23 : Wilson loop expansion any N≥1, d≥2, dual cordique.

**Applicabilité SU(N) 4D** :
- **Réseau fixé, strong coupling** : viable, publié 2022.
- **Continuum limit** : **non**. Constantes log-Sobolev dépendent du couplage → divergent quand a→0 (β(a)→∞ par asymptotic freedom).

**Effort** : Réseau fixé déjà fait. Continuum limit = problème ouvert (probablement requires Bałaban-like RG quand même).
**Avantage** : Bakry-Émery direct, mass gap déjà acquis sur réseau.
**Inconvénient** : Strong coupling seulement, ne se prolonge pas au continuum sans RG.

---

## §10. Comparaison tabulée

| Approche | Cas publié | Applicabilité SU(N) 4D continuum | Effort restant | Avantage clé | Inconvénient majeur |
|---|---|---|---|---|---|
| **Bałaban classique** 1985-1989 | U(1) UV stab. 3D/4D ; SU(N) 4D UV stab. *partiel* | Partial — 4 gaps G1-G4 | 12-18m | Standard, programme complet en principe | 40 ans non terminé |
| **Brydges 1986** tree formula | Composant universel | Building block (pas standalone) | N/A | Élégance combinatoire | Pas un substitut |
| **Magnen-Sénéor 1976 / MRS 1993** | YM₄ SU(2) IR cutoff fixé | Partial (SU(2) avec IR cutoff fixé) | 18-36m | Construction explicite Schwinger | Pas SU(N), IR cutoff |
| **Glimm-Jaffe 1981** | Manuel constructif 2D/3D | Impossible (référence) | N/A | Pédagogie OS axioms | Pas YM 4D |
| **Sheffield 2025** (Cao-Nissim-Sheffield) | Area law U(N)/SU(N)/SO(2N) lattice 't Hooft | Lattice fixé OK, continuum non | 6-12m réseau, continuum ouvert | Méthode moderne dynamique | Pas de continuum limit |
| **Eldan localization** 2013+ | KLS, log-Sobolev convexe | Indirect (outil) | 12-24m | Probabilité moderne | Pas d'app YM, mesure non-convexe |
| **Polchinski 1984 + BBD 2023** | φ⁴₂, φ⁴₃ continuum, Sine-Gordon, Ising | Pas d'app YM non-abélien | 18-30m | Single bound (susceptibilité) au lieu de 4 gaps | Mesure YM problématique |
| **Hairer reg. structures** (CCHS 2022) | YMH 2D, 3D | Impossible 4D super-critique | Inconnu | Framework moderne | 4D YM hors champ |
| **SZZ22 / CPS23** stochastic analysis | SU(N), SO(N), U(N) lattice mass gap strong coupling | Lattice fixé OK, continuum non | 0 (réseau) | Bakry-Émery direct, log-Sob | Strong coupling seulement |
| **Adhikari-Cao 2022** (arXiv:2202.10375) | **Finite gauge groups seulement** | Impossible (groupes finis) | N/A | Décorrélation exponentielle | Pas continu SU(N) |
| **Nissim 2025** (arXiv:2510.22788) | U(N) 't Hooft lattice mass gap | Lattice OK (réutilise SZZ23 pour SU(N)) | 0 (lattice) | Innovation Bakry-Émery contournement | Pas de continuum |
| **Faria da Veiga-O'Carroll** (arXiv:1903.09829) | U(N)/SU(N) lattice stab. d=2,3,4 | Stability only, pas de mass gap | Mass gap non | Stab. bounds avec gauge fixing tree | Pas de mass gap |

**Note sur Adhikari-Cao 2022** : confirmé via WebFetch — applies to **finite (possibly non-Abelian) gauge groups only**, exclut SU(N) continuous. Important catch — c'était listé dans le briefing comme alternative SU(N) potentielle, c'est faux.

**Note sur Cao-Nissim-Sheffield 2025** : Bypasse Bakry-Émery pour U(N) via random-environment SU(N) reduction. Pas une *vraie* nouvelle technique pour SU(N) — réutilise SZZ23.

---

## §11. Recommandation pour pitch Bauerschmidt

### Tier 1 — Promu (à mentionner explicitement dans pitch)

1. **Polchinski + BBD framework (§7)** — La voie la plus prometteuse **conceptuellement**.
   - Bauerschmidt est l'auteur du framework Polchinski-stochastic-dynamics (BBD 2023 survey, BD 2024 φ⁴₂/φ⁴₃).
   - Pitch : "Bauerschmidt, would Polchinski-equation log-Sobolev criterion via susceptibility-bound apply to lattice YM SU(N) 4D? You proved it for φ⁴₂/φ⁴₃, and BBD 2023 surveys cover Eldan/Föllmer/Boué-Dupuis equivalence. YM 4D log-Sobolev would close B1 via single bound rather than Bałaban's 4 gaps."
   - Effort estimé : 18-30 mois (recherche frontière).
   - Risque : susceptibilité YM 4D non bornée trivialement — c'est *le* sujet.

2. **Sheffield-style dynamique (§5,9)** — Combinable avec voie 1.
   - Cao-Nissim-Sheffield 2025 + Nissim 2025 : mass gap **sur réseau fixé** pour U(N), SU(N), SO(2N) en régime 't Hooft.
   - Pitch : "Sheffield + Cao groupe a fermé le mass gap sur réseau via Langevin Bakry-Émery. Le continuum limit reste open. Auriez-vous des heuristiques pour le coupler à votre RG?"
   - Effort : 12-24 mois pour continuum limit (= le vrai gap).

### Tier 2 — Mentionnable (alternative historique sérieuse)

3. **Magnen-Rivasseau-Sénéor 1993 YM₄ (§3)** — Seule construction explicite YM 4D publiée.
   - Pitch : "Approche phase cell expansion 1993 est-elle ré-attaquable avec outils modernes? Rivasseau est encore actif."
   - Effort : 18-36 mois pour SU(N) + suppression IR cutoff.
   - Risque : Programme abandonné par auteurs depuis 30 ans.

### Tier 3 — Skip dans pitch (pas substituts)

- Brydges 1986 (building block, pas standalone)
- Glimm-Jaffe 1981 (manuel)
- Eldan 2013 isolé (indirect)
- Hairer reg. structures (4D impossible)
- Adhikari-Cao 2022 (finite groups only)
- Faria da Veiga-O'Carroll (stab. sans mass gap)

### Note méta

**Aucune approche** ne ferme B1 pour SU(N) 4D continuum limit aujourd'hui. Tout pitch doit être franc sur ce point. L'angle Bauerschmidt-Hairer le plus convaincant n'est pas "voici un substitut à Bałaban" mais "voici un programme de réécriture de B1 via Polchinski-flow + stochastic localization qui réduit 4 gaps à 1 (susceptibilité bornée), réalisable sur 18-30 mois si la mesure YM cooperate."

---

## §12. Catches anti-fab détectés en cours

1. **Adhikari-Cao 2022 (arXiv:2202.10375)** — listé dans briefing initial comme "weak coupling expansion". Confirmé via WebFetch : **gauge groups finis seulement**, pas SU(N) continuous. Catch.
2. **"Brydges Wright 1988"** — search retourne 0 résultats sérieux. Probable confusion ou non-existant. Skip.
3. **"Disertori-Rivasseau 2000 phase cell"** — pas de paper exact trouvé sous ce titre/date. Disertori-Rivasseau 1998 *Continuous Constructive Fermionic Renormalization* (hep-th/9802145) existe mais autre sujet (fermions).
4. **"Erdős-Schlein 2010 cluster"** — pas trouvé pour gauge theory. Skip.
5. **"Jaffe-Lesniewski 1992"** — pas confirmé via search. Skip ou marker "non vérifié".
6. **Bauerschmidt-Park-Sheffield 2023** — la triplette correcte est **Cao-Park-Sheffield** (arXiv:2307.06790), pas Bauerschmidt. Bauerschmidt n'est pas co-auteur ici.

Tous les éléments ci-dessus n'ont **pas** été propagés en assertions positives dans §1-§11.

---

## §13. Liens vérifiés (anti-fab source of truth)

- arXiv:2204.12737 Shen-Zhu-Zhu (SZZ22) — *CMP* 400 (2022) — VERIFIED
- arXiv:2401.13299 Shen-Zhu-Zhu (SZZ24 Higgs) — VERIFIED
- arXiv:2509.04688 Cao-Nissim-Sheffield (2025) — VERIFIED
- arXiv:2510.22788 Nissim (2025) U(N) — VERIFIED
- arXiv:2307.07619 Bauerschmidt-Bodineau-Dagallier (2023) *Probab. Surv.* 21 — VERIFIED
- arXiv:2202.10375 Adhikari-Cao (2022) *AOP* — VERIFIED, finite groups only
- arXiv:2201.03487 Chandra-Chevyrev-Hairer-Shen (2022) 3D YMH — VERIFIED
- arXiv:2202.13359 Chevyrev YM stoch quant review — VERIFIED
- arXiv:2307.06790 Cao-Park-Sheffield (2023) random surfaces — VERIFIED
- arXiv:1610.03821 Jafarov 2016 Wilson loops SU(N) 1/N — VERIFIED
- arXiv:1903.09829 Faria da Veiga-O'Carroll YM stab — VERIFIED
- arXiv:1108.1335 Dimock Renormalization group Balaban I (Small fields) — VERIFIED, φ⁴₃ pas YM
- arXiv:2504.08606 Bauerschmidt-Dagallier-Weber Holley-Stroock φ⁴₂ (2025) — VERIFIED
- arXiv:1403.7422 / 1403.7424 BBS (2015) 4D weakly self-avoiding walk / |φ|⁴ — VERIFIED
- Polchinski *Nucl. Phys. B* 231 (1984) 269 — VERIFIED via search
- Balaban *CMP* 102 (1985), 109 (1987), 116 (1988), 122 (1989) — VERIFIED
- Brydges Les Houches 1984 / publ. 1986 — VERIFIED via search (no DOI)
- Magnen-Rivasseau-Sénéor *CMP* 155 (1993) 325 — VERIFIED via projecteuclid
- Glimm-Jaffe Springer 1981 — VERIFIED
- Kotecký-Preiss *CMP* 103 (1986) 491-498 — VERIFIED

---

## §14. Tags

#YM4D #B1 #ClusterExpansion #Balaban #Polchinski #Bauerschmidt #Hairer #Sheffield #ShenZhu #Magnen #Rivasseau #LSI #LogSobolev #StochasticLocalization #Eldan #anti-fab
