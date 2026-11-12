# Théorème `TubeArea.column_flip_bound` (borne par retournement de colonne, forme abstraite) : certificat du 11/11/2026

**Énoncé (français).** Soit un espace de probabilité (Ω, μ) et deux ensembles finis, les arêtes E et les plaquettes P ; chaque
plaquette p a un bord `bd p ⊆ E`, et son signe sous une configuration de signes σ : E → {±1} est le produit des σ(e) sur son
bord. On suppose : pour chaque σ, une application τ_σ : Ω → Ω qui préserve μ ; des couplages mesurables K_p, bornés par κ en
valeur absolue, IMPAIRS sous les retournements (K_p ∘ τ_σ = signe_p(σ) · K_p) ; un poids R ≥ 0 mesurable et invariant, avec
R·exp(Σ_p K_p) intégrable ; une observable mesurable W, |W| ≤ 1, qui prend sous τ_σ le produit des signes des plaquettes d'un
ensemble A ; et l'indépendance des signes de plaquettes (l'application σ ↦ (signe_p(σ))_p est surjective). Alors
|∫ W · R · exp(Σ K) dμ| ≤ tanh(κ)^|A| · ∫ R · exp(Σ K) dμ.
Pour SU(2) avec l'action de Wilson sur (plaque du plan long) × (fibre finie à n sites), κ = β·n : c'est la loi d'aire
élémentaire du tube, |⟨W_C⟩| ≤ tanh(β n)^(aire), à tout couplage.

**Qui a fait quoi.** Énoncé écrit et FIGÉ par le pilote (Claude) avant toute preuve ; preuve écrite par GPT-6.1 Sol en un tour
(291 lignes, `ColumnFlip_PROUVE_tour1.lean`, sha256 6fb9a5ee…ad2f) ; le modèle ne pouvait ni compiler ni modifier le pied de
vérification (`../lean_protege/PIED_VERIFICATION.lean`), qui réénonce le théorème sans les définitions auxiliaires et l'obtient
par application directe.

**Contrôles (machine louée, 11/11/2026, 20h12 à 20h16 ; journaux dans `certificat/`).**
| contrôle | résultat |
|---|---|
| Lean 4.32.0 + Mathlib v4.32.0 (81a5d257) | code 0, 0 erreur ; `enonce_canonique` dépend de [propext, Classical.choice, Quot.sound] |
| Lean 4.32.2 (même Mathlib recompilé) | code 0 ; mêmes trois axiomes |
| noyau indépendant nanoda 0.4.32 (binaire non modifié) sur la clôture exportée (2 368 714 lignes, sha256 5ff798af…e51c) | « Checked 26868 declarations with no errors », code 0, axiomes permis : les trois standard seulement |
| mots interdits (`sorry`, `axiom`, `native_decide`, `unsafe`…) | aucun |
| énoncé du fichier prouvé contre le squelette du pilote | identique (diff vide) |
| lecture du fichier par le pilote | aucune notation, macro, instance ni option hors de l'espace de noms ; deux définitions auxiliaires et douze lemmes |

**Ce que ce théorème est, et n'est pas.** C'est le cœur mathématique de la loi d'aire élémentaire du tube, sous forme abstraite ;
il est élémentaire (pas de développement en amas, pas de couplage faible). Il ne dit rien du trou de masse ni du verrou en
dimension 4. L'outil (multiplier des liens par un élément du centre) est classique (Tomboulis–Yaffe 1985) ; l'article voisin de
Borgs (1985) n'a pas pu être lu : ne pas écrire « nouveau ». La non-vacuité (exemple où la borne est atteinte) et l'instance
« théorie de jauge de type Wilson » sont en cours de formalisation (`../lean2/`).

---

# Suite du 11/11/2026, 20h35 à 20h40 : deux théorèmes de plus (fichier `../lean2/TubeSu2_PROUVE_tour3.lean`, sha256 985d5921…c10b)

**`TubeArea.sharp_one_edge` (la borne est atteinte).** Énoncé figé par le pilote : sur l'espace à deux points des signes, il existe
une mesure de probabilité invariante par multiplication par tout signe pour laquelle, avec le couplage K = J·signe et
l'observable « signe », on a ÉGALITÉ : ∫ signe·exp(J·signe) = tanh(J)·∫ exp(J·signe), avec une normalisation strictement
positive. Donc les hypothèses de `column_flip_bound` ne sont pas vides et sa constante tanh(κ) est optimale.

**`TubeArea.wilson_column_flip_bound` (théorie de jauge de type Wilson).** Énoncé rédigé par Sol selon la spécification du pilote,
RELU par le pilote avant d'être gelé (définitions `WilsonConfig`, `wilsonMeasure`, `columnFlip`, `wordHolonomy`, `wilsonCoupling`,
`wilsonLoop`, l. 74 à 122 ; énoncé l. 328 à 349). Données : un groupe mesurable G avec une mesure de probabilité invariante à
gauche, une involution centrale z, une fonction χ mesurable, bornée par 1, impaire sous z (pour SU(2) : z = −1, χ = demi-trace) ;
des liens longs indexés par (arête, site de fibre) et d'autres liens ; pour chaque plaquette longue un mot à arêtes distinctes ;
des poids |c| ≤ 1 (signes de torsion compris) et β ≥ 0 ; le couplage K_p = β Σ_y c_{p,y} χ(holonomie de p en y) ; un poids
restant R ≥ 0 invariant par retournement (hypothèse) ; une boucle de Wilson à arêtes distinctes en un site de fibre, bord d'un
ensemble A de plaquettes (hypothèse de Stokes sur les signes) ; signes de plaquettes indépendants (hypothèse de surjectivité).
Conclusion : |∫ W·R·exp(ΣK)| ≤ tanh(β·card F)^(card A) · ∫ R·exp(ΣK).
Ce qui reste HYPOTHÈSE dans cet énoncé (à décharger par l'étape suivante sur un réseau explicite) : l'invariance de R, la
relation de Stokes, la surjectivité. Le corollaire SU(2) proprement dit (mesure de Haar de SU(2)) n'est pas écrit.

**Contrôles** (journaux `certificat/`, fichier complet `su2_3.lean`, sha256 0bb00445…9a4f) :
| contrôle | résultat |
|---|---|
| Lean 4.32.0 + Mathlib v4.32.0 | code 0 ; les trois théorèmes dépendent de [propext, Classical.choice, Quot.sound] |
| Lean 4.32.2 | code 0 ; mêmes axiomes |
| nanoda 0.4.32 (binaire non modifié), clôture exportée (2 542 326 lignes, sha256 2a53edca…66f0) | « Checked 28343 declarations with no errors », code 0 |
| mots interdits, importations, notations ou instances au niveau du fichier | aucun |
| tours de la boucle | 3 (5 erreurs, puis 1, puis 0) ; énoncés A et B inchangés (pied de vérification) |

---

# Suite du 11/11/2026, 20h52 à 20h58 : le réseau rectangulaire explicite (fichier `../lean3/TubeGrid_PROUVE_tour2.lean`, sha256 7b36e072…3ccf)

Définitions relues par le pilote (littérales) : arêtes `GridEdge m n` (horizontales et verticales d'une grille de m × n
plaquettes), bord d'une plaquette `gridBd` (ses quatre arêtes), rectangles `rectPlaquettes a b c d` (a ≤ i < b, c ≤ j < d) et
leur bord `rectBoundary`, mot d'une plaquette `gridWord` et mot du contour d'un rectangle `rectWord` (sens trigonométrique).
- **`grid_plaq_surjective`** : sur la grille à bord libre, toute affectation de signes aux plaquettes est réalisée par des signes
  d'arêtes (les signes de plaquettes sont indépendants).
- **`grid_stokes_rectangle`** (a < b, c < d) : le produit des signes sur le contour du rectangle égale le produit des signes des
  plaquettes qu'il entoure.
- **`tube_area_law_rectangle`** : loi d'aire élémentaire sur (plaque rectangulaire) × (fibre finie F), pour tout groupe mesurable
  à mesure de probabilité invariante à gauche, involution centrale z et fonction χ mesurable, bornée par 1, impaire sous z :
  |∫ W_rectangle · R · exp(ΣK)| ≤ tanh(β·card F)^((b−a)(d−c)) · ∫ R · exp(ΣK). Les hypothèses de Stokes et d'indépendance sont
  maintenant DÉMONTRÉES ; reste supposée l'invariance par retournement du poids R des autres plaquettes (étape suivante).
**Contrôles** (fichier complet `grid_2.lean`, sha256 4e3ab68e…07dd) : Lean 4.32.0 et 4.32.2, code 0, les six théorèmes avec les
trois axiomes standard ; nanoda : « Checked 31363 declarations with no errors » (export de 2 822 331 lignes, sha256
7dab5b15…0a0f). Deux tours de boucle (5 erreurs, puis 0).

---

# Suite du 11/11/2026, 21h02 à 21h10 : l'action de type Wilson complète (fichier `../lean4/TubeAction_PROUVE_tour1.lean`, sha256 7150582b…4c68)

Définitions relues par le pilote : `GeneralWord` (mot de liens : lien long `(e, y)` ou autre lien `x`, avec orientation),
`generalHolonomy` (produit ordonné, inverses pour les orientations négatives), `generalWordSign` (produit des signes de colonne
aux entrées longues, avec multiplicité), `NeutralWord` (ce produit vaut 1 pour tout choix de signes), `mixedWord e y y' x x'`
(plaquette mixte : lien long en y, lien de fibre, même lien long en y' à rebours, lien de fibre à rebours),
`neutralActionWeight` = exp(Σ_q coef_q · χ(holonomie du mot q)).
- **`neutral_word_flip_invariant`** : pour un groupe quelconque et une involution centrale z, l'holonomie d'un mot neutre est
  invariante par tout retournement de colonne (aucune hypothèse sur χ).
- **`mixedWord_neutral`** : toute plaquette mixte est neutre (et, lemme `no_long_word_neutral`, tout mot sans lien long).
- **`wilson_action_area_law_rectangle`** : loi d'aire élémentaire pour l'action de type Wilson COMPLÈTE sur
  (plaque rectangulaire à bord libre) × (fibre finie quelconque) : plaquettes de la base à poids bornés par 1 (signes de torsion
  compris), plus une famille finie quelconque de termes neutres (plaquettes mixtes, plaquettes de fibre) à coefficients réels
  quelconques : |∫ W_rectangle · e^{−S}| ≤ tanh(β·card F)^((b−a)(d−c)) · ∫ e^{−S}. Plus AUCUNE hypothèse sur le poids
  (mesurabilité, positivité, invariance et intégrabilité sont démontrées). Hypothèses restantes : celles du groupe (mesure de
  probabilité invariante à gauche, involution centrale z, χ mesurable, bornée par 1, impaire sous z), 0 ≤ β, a < b, c < d.
**Contrôles** (fichier complet `action_1.lean`, sha256 34ae468b…8531) : Lean 4.32.0 et 4.32.2, code 0, neuf théorèmes aux trois
axiomes standard ; nanoda : « Checked 31384 declarations with no errors » (export de 2 826 221 lignes, sha256 33925e23…5c1b).
Un seul tour de boucle. Journaux : `certificat/etape4/`.
**Ce que ces neuf théorèmes ne disent pas** : rien sur le trou de masse ni sur une tension de corde uniforme en la taille de la
fibre (la borne tend vers 1 quand card F grandit à β fixé) ; pas encore de corollaire nommé pour SU(2) avec sa mesure de Haar
(instances de compacité absentes de Mathlib v4.32.0 ; cible : les objets `YangMills.su2` et `wilsonLaw` du développement
d'OpenAI) ; le bord de la plaque est libre (le tore : étapes F et G en cours).

---

# Suite du 11/11/2026, 21h26 à 21h28 : géométrie du tore discret (fichier `../lean6/TubeTorusGeom_PROUVE_tour1.lean`, sha256 130e414f…dc90)

Énoncés et définitions FIGÉS PAR LE PILOTE avant la boucle (`../lean6_protege/ENONCES_G.lean`), repris mot pour mot (contrôle par
`diff` : aucune ligne différente), et réénoncés indépendamment dans le pied sans les définitions du modèle.
`TorusEdge m n` : arêtes du tore (ℤ/m) × (ℤ/n) (horizontales et verticales, indices cycliques par `finRotate`) ; `torusBd p` : les
quatre arêtes du bord de la plaquette de coin p.
- **`torus_plaq_explicit`** (m, n ≥ 2) : le signe d'une plaquette est le produit des signes de ses quatre arêtes (distinctes).
- **`torus_plaq_parity`** (m, n ≥ 2) : sur le tore, le produit de tous les signes de plaquettes vaut 1.
- **`torus_plaq_image`** (m, n ≥ 2) : toute affectation de signes de plaquettes de produit 1 est réalisée par des signes d'arêtes.
Autrement dit : sur le tore, l'image de l'application « signes d'arêtes ↦ signes de plaquettes » est exactement l'ensemble des
configurations paires. Ce sont les deux hypothèses de la version « surface fermée » de la moyenne des signes (étape F).
**Contrôles** (fichier complet `torusgeom_1.lean`, sha256 aa8c9adc…5623) : Lean 4.32.0 et 4.32.2, code 0, douze lignes d'axiomes
toutes standard ; nanoda : « Checked 31116 declarations with no errors » (export de 2 784 550 lignes, sha256 1e712c05…86d4).
Un seul tour de boucle. Journaux : `certificat/etape6/`.

---

# Suite du 11/11/2026, 21h34 à 21h37 : moyenne des signes sur une surface fermée, rapport de torsion (fichier `../lean5/TubeTorus_PROUVE_tour2.lean`, sha256 70fc5baf…a220)

Énoncés FIGÉS PAR LE PILOTE avant la boucle (`../lean5_protege/ENONCES_F.lean`, dérivation à la main consignée dans la consigne),
repris mot pour mot (diff vide), réénoncés indépendamment dans le pied. Cadre abstrait de la partie A, où l'hypothèse de
surjectivité est remplacée par : (parité) le produit de tous les signes de plaquettes vaut 1 ; (image) toute affectation de
produit 1 est réalisée. Notations : q = tanh κ, N = nombre de plaquettes.
- **`torus_flip_bound`** : (1 − q^N) · |∫ W · R · exp(ΣK)| ≤ (q^|A| + q^(N−|A|)) · ∫ R · exp(ΣK).
- **`twist_ratio_bound`** : si Z₀ = ∫ R exp(ΣK) et Z₁ est la même intégrale après changement de signe du couplage d'UNE plaquette,
  alors |Z₀ − Z₁| ≤ q^N · (Z₀ + Z₁). C'est la borne sur l'énergie libre de flux électrique (au sens de 't Hooft) du tube.
- **`le_of_forall_pow_le_const_mul_pow`** : si aⁿ ≤ M·bⁿ pour tout n ≥ 1 (a, b ≥ 0, M > 0), alors a ≤ b.
- **`flux_gap_of_traces`** : si λ₁ⁿ ≤ Od(n), Ev(n) ≤ D·λ₀ⁿ et Od(n) ≤ q^(nℓ)·Ev(n) pour tout n ≥ 1, alors λ₁ ≤ q^ℓ·λ₀.
Lecture : le théorème du trou dans le secteur de flux (dérivation T19 d'Astra, relue par un Opus non-auteur) = `twist_ratio_bound`
(formalisé) + `flux_gap_of_traces` (formalisé) + les identités de traces de la matrice de transfert, Z₀ = Tr Tⁿ et Z₁ = Tr(ΩTⁿ),
qui ne sont PAS formalisées (papier seulement).
**Contrôles** (fichier complet `torusavg_2.lean`, sha256 aefbe076…cfcc) : Lean 4.32.0 et 4.32.2, code 0, treize lignes d'axiomes
toutes standard ; nanoda : « Checked 27006 declarations with no errors » (export de 2 397 150 lignes, sha256 e0bd8495…9521).
Deux tours de boucle (6 erreurs, puis 0). Journaux : `certificat/etape5/`.

---

# Suite du 11/11/2026, 21h47 à 21h53 : l'action de type Wilson sur le tore (fichier `../lean7/TubeTorusWilson_PROUVE_tour2.lean`, sha256 b9e2da60…34d8)

Énoncés et définition `torusWord` FIGÉS PAR LE PILOTE (`../lean7_protege/ENONCES_H.lean`), repris mot pour mot (diff vide).
- **`wilson_twist_ratio_bound`** : pour une théorie de jauge de type Wilson dont les signes de plaquettes vérifient la contrainte
  de parité et réalisent toute affectation paire : si Z₁ est obtenue de Z₀ en changeant le signe de toutes les copies de fibre
  d'UNE plaquette de base, alors |Z₀ − Z₁| ≤ tanh(β·card F)^(nombre de plaquettes de base) · (Z₀ + Z₁).
- **`wilson_electric_flux_torus`** : le même énoncé pour l'action de type Wilson COMPLÈTE sur (tore m × n, m, n ≥ 2) × (fibre
  finie F) : plaquettes de base à poids bornés, plus toute famille finie de termes neutres (plaquettes mixtes et de fibre) à
  coefficients réels quelconques : |Z₀ − Z₁| ≤ tanh(β·card F)^(mn) · (Z₀ + Z₁). C'est un « rapport de torsion » : il borne par le
  bas l'énergie libre de flux électrique au sens de 't Hooft (e^(−F) = (Z₀ − Z₁)/(Z₀ + Z₁)) par mn·|log tanh(β·card F)|.
**Contrôles** (fichier complet `toruswilson_2.lean`) : Lean 4.32.0 et 4.32.2, code 0, dix-huit lignes d'axiomes toutes standard ;
nanoda : « Checked 31158 declarations with no errors » (export de 2 801 978 lignes, sha256 8331f5f6…6563). Deux tours de boucle.
Journaux : `certificat/etape7/`.

**Bilan au 11/11/2026, 22h : DIX-HUIT théorèmes vérifiés** (parties A à H ; base gelée complète :
`../lean8_protege/PARTIE_ABCDEFGH_pont_gelee.lean`). Lecture à l'aveugle par une troisième famille (DeepSeek V4 Pro) :
`../retraduction/BILAN_PILOTE.md` (aucun énoncé jugé vide ; dix clarifications de rédaction demandées).
Ce que ces théorèmes ne disent pas : rien sur le trou de masse ; rien d'uniforme en la taille de la fibre ; les identités de traces
de la matrice de transfert (Z₀ = Tr Tⁿ, Z₁ = Tr(ΩTⁿ)) ne sont pas formalisées ; pas de corollaire SU(2) autonome (étape I en cours :
énoncé sur les objets publics du développement d'OpenAI).

---

# Suite du 11/11/2026, 22h38 à 22h41 : PONT vers les objets publics du développement d'OpenAI (fichier `../lean8/TubeBridge_PROUVE_tour6.lean`, sha256 2a8f32f8…30dd)

Ce fichier se compile DANS le projet Lean d'OpenAI (`yang-mills-group/OpenAI-YM-20261028`, HEAD 3456e5e7, Lean 4.32.0) : la base
gelée importe `PublicWilson` et `ConcreteSU2`. Énoncés et les deux définitions FIGÉS PAR LE PILOTE avant la boucle
(`../lean8_protege/ENONCES_I.lean`), repris mot pour mot (diff vide). Espace de noms `TubeBridge`.
Objets d'OpenAI utilisés tels quels : `YangMills.GaugeGroup` (sous-groupe fermé du groupe unitaire), `Site l = Axis → ZMod l`
(réseau périodique à quatre dimensions), `Configuration g l`, `plaquette`, `wilsonEnergy`, `WilsonFamily` (avec sa mesure `haar`),
`su2`. Définitions ajoutées : `signedWilsonEnergy s U` (leur énergie avec un signe par terme de plaquette ; `signedWilsonEnergy_one`
prouve qu'avec des signes 1 c'est `wilsonEnergy`) ; `planeTwist a b` (signe −1 sur les plaquettes du plan des axes 0 et 1 dont le
point de base a les coordonnées (a, b), à toute position le long des axes 2 et 3 : torsion de 't Hooft dans ce plan).
- **`openai_wilson_twist_ratio`** : pour tout groupe de jauge g contenant −1, toute période l ≥ 2, tout β ≥ 0, toute mesure de
  probabilité sur g invariante à gauche, tous a, b : avec Z₀ = ∫ exp(−β·wilsonEnergy U) et Z₁ = ∫ exp(−β·signedWilsonEnergy
  (planeTwist a b) U), intégrales sur toutes les configurations pour la mesure produit,
  |Z₀ − Z₁| ≤ tanh(β·l²)^(l²) · (Z₀ + Z₁).
- **`openai_wilson_twist_ratio_family`** : le même énoncé pour la mesure `C.haar` de toute `WilsonFamily C`.
- **`su2_neg_one_mem`** : le SU(2) concret d'OpenAI contient −1.
- **`openai_su2_twist_ratio`** : l'énoncé pour `su2` et toute `WilsonFamily su2`, sans autre hypothèse que l ≥ 2 et β ≥ 0.
**Contrôles** (fichier complet `pont_6.lean`, sha256 e0a70f80…8bb6) : Lean 4.32.0 et 4.32.2, code 0, vingt-quatre lignes d'axiomes
toutes standard (dont celle du théorème `YangMills.su2Theory` d'OpenAI, réaffichée comme témoin) ; nanoda : « Checked 40099
declarations with no errors » (export de 4 090 351 lignes, sha256 4d9c751e…9f49). Six tours de boucle (11, 14, 3, 3, 1, 0 erreurs).
Journaux : `certificat/etape8/`.
**Portée, à dire telle quelle** : c'est une inégalité exacte en volume fini sur la mesure de réseau dont part la construction
d'OpenAI ; elle dépend du volume (tanh(βl²)^(l²) tend vers 1 quand l grandit à β fixé) et ne dit RIEN du trou de masse ni de la
limite continue. Son intérêt : un théorème à nous, vérifié par trois vérificateurs, énoncé sur leurs définitions sans les modifier.
