# Antériorité de la section « Centre Z_N » (candidat v1.2) — contrôle du jour, 12/11/2026

Par Claude Sonnet 5.5 (non auteur du théorème). Le mot « nouveau » n'est pas employé. « Non trouvé dans ce qui a été lu » n'est pas une preuve d'absence.

## 1. Ce que j'ai fait aujourd'hui
* Relu `chantiers/centre_zn_2026-11-12/ANTERIORITE.md` (pilote Opus, 06h30) et `chantiers/biblio_2026-11-12/` (BIBLIOGRAPHIE, VERDICT_PAR_NOTE). Je n'ai pas refait leur lecture des pages ; je les prends pour établies sauf là où je l'indique.
* Corpus local : `outils/rag_gamer/ragh-lit` sur quatre questions (« center vortex free energy bound valid at all couplings lattice gauge theory finite volume », « 't Hooft loop Z_N lattice inequality twisted partition function ratio bound », « Münster character coefficients vortex free energy strong coupling Z(N) », « electric flux free energy lower bound rigorous Z_N gauge theory »), sorties conservées dans le dossier de travail (non publiées). Résultats : Greensite 2003, Kovács–Tomboulis 2000/2002, Tomboulis 2007, Kanazawa 0808.3442 et 0805.2742 ; aucun texte nouveau par rapport à la liste du pilote.
* Web GÉNÉRIQUE (six requêtes, jamais nos textes) : « explicit bound center vortex free energy twisted partition function ratio … all couplings rigorous Z_N » ; « Münster 1981 high temperature expansions for the free energy of vortices… » ; « 't Hooft loop lattice Z_N … character expansion rigorous inequality electric flux Fourier transform center » ; « Fourier coefficient bound tanh per plaquette twisted partition function ratio Z(2)… » ; « Mack Petkova sufficient condition for confinement… » (et deux lectures de pages arXiv : 2605.02156, 2505.16546). Aucune borne explicite « rapport de torsion Z_N ≤ constante^{aire} à tout couplage » n'est apparue.
* Texte local relu pour cette version : Kanazawa 0808.3442v3, pp. 4–9 (définitions (5)–(9), Lemmes 1–2, Théorèmes 1–2, preuve du Théorème 2 jusqu'à (41)), pour recopier exactement les hypothèses de son Théorème 2 ; Kanazawa 0805.2742v3 : résumé, introduction et §2 (Théorème 1 : égalité entre les rapports sur deux réseaux de tailles différentes, avec écart de couplage), énoncés des Théorèmes 2–4 repérés.

## 2. Ce qui a été lu, en entier, en partie, pas du tout
| texte | statut | contenu utile pour la question |
|---|---|---|
| Kanazawa, arXiv:0808.3442v3 | PARTIE (pp. 4–10 : définitions, Lemmes 1–2, Théorèmes 1–2, preuve du Théorème 2) ; §3 (spins) non lu en détail | Théorème 2 : borne de la boucle de Wilson de N-alité non nulle par les projecteurs de flux ; version Z_N annoncée par TY85 et rendue explicite ici ; **aucune borne explicite de ⟨F^[q]⟩** ; il cite Münster (couplage fort) pour la décroissance de l'énergie libre de vortex. |
| Kanazawa, arXiv:0805.2742v3 | PARTIE (résumé, introduction, §2 début ; Théorèmes 2–4 repérés par recherche de mots) | Théorème 1 : égalité exacte, à tout couplage, entre une combinaison linéaire des fonctions de partition tordues sur un réseau et la même sur un réseau plus petit, avec un petit écart de couplage qui disparaît en volume infini ; ce n'est pas une borne à constante explicite ; non comparable à la nôtre (autre type de résultat). |
| Tomboulis–Yaffe 1985 (CMP 100, 313) | PARTIE (pp. 317, 332–333, couche OCR) | ouvrage de référence de l'outil et de l'identité Z_2 ; p. 333 : extension aux autres groupes à centre non trivial annoncée sans construction. |
| Kovács–Tomboulis 2002 (hep-lat/0108017) | PARTIE (éq. (3), (8), (11)) | outil et inégalité boucle ≤ flux pour SU(2). |
| Münster 1981, NPB 180 [FS2] 23 | PARTIE (résumé, introduction, mots-clés « vortex », « bound », « converge » avec les passages autour des lignes 306–420 et 500–545 sur 716) | développement en amas de l'énergie libre de vortex pour SU(2) et Z_2, à couplage fort (β petit), 3 et 4 dimensions ; coefficient = tension de corde ; **pas** une borne à tout couplage ni un traitement de Z_N général. |
| Mihajlovic 2611.11534 | EXTRAITS seulement (§79.7) | reprise de Kanazawa. |
| Borgs–Seiler 1983 | PARTIE (p. 339, (11.32), Lemme II.6) | flux électrique central à température non nulle. |
| Tomboulis 2007 (0707.2179) ; Kovács–Tomboulis 1998–2000 ; Greensite 2003 ; de Forcrand–von Smekal ; Anshu ; Chatterjee ; Lemm | RÉSUMÉS / passages cités par le RAG | numérique ou autres résultats rigoureux (décimation pour SU(2)) ; rien d'une borne de Fourier explicite à tout couplage. |
| Mack–Petkova (Ann. Phys. 125 (1980) 117, « Sufficient condition for confinement of static quarks by a vortex condensation mechanism » ; préprint 1979) | RÉSUMÉ/NOTICE seulement (recherche web ; le préprint a été lu par le pilote, pas par moi) | condition suffisante de confinement par condensation de vortex ; je n'ai pas vérifié son contenu. |
| 't Hooft, NPB 153 (1979) 141 ; Borgs NPB 261 (1985) 455 ; Seiler PRD 18 (1978), LNP 159 (1982) ; Migdal 1975 | PAS LU | origine du cadre ; solution exacte 2D par caractères ; la forme de l'identité centrale du théorème B (Ẑ_q ∝ ∫ R Π_p A_q(T_p)) est très probablement classique dans son principe. |
| arXiv:2605.02156 (« Lattice Gauge Theory and Wilson-Loop Confinement: A Statistical-Mechanical Survey ») | PAGE arXiv (résumé) ; l'avis de retrait de la v3 est sur la page | retiré pour « unverifiable authorship and affiliation » ; texte indisponible ; AUCUNE valeur de source. |
| arXiv:2505.16546 (Maeda–Tanizaki, JHEP 08 (2025) 128) | RÉSUMÉ | fonctions de partition tordues comme paramètres d'ordre ; cadre qualitatif, aucune inégalité. |
| BB26 v5.0.0 (Zenodo 24147967) | PARTIES (comme dans la v1.1) | rien de ce type. **Le contrôle du jour de publication de la dernière archive de BB26 reste à faire par le pilote.** |

## 3. Ce qui est classique (avec la page, repris de la recherche du pilote et recoupé)
1. L'objet : Ẑ_q = Σ_k ζ^{qk} Z_k = N·Z_0·⟨F^[q][V]⟩, projecteur de flux électrique (Kanazawa 0808.3442 (8)–(9), p. 5 ; signe vérifié sur le texte : z^{+mk}) ; pour N = 2, TY85 (2.8)–(2.9) p. 317.
2. L'outil : changement de variables U → z^k U sur un ensemble de liens (Kanazawa p. 6, preuve du Lemme 1 ; TY85 App. I.C p. 332 ; KT02 (8)).
3. La version Z_N de la boucle ≤ flux : annoncée TY85 p. 333, explicitée Kanazawa Théorème 2 p. 7.
4. Le facteur par plaquette : coefficients de caractère de Z_N de j ↦ e^{Re(ζ^j t)} ; pour Z_2, tanh (Münster, exp L_p = cosh β (1 + tanh β δ(p))).

## 4. Ce qui n'a pas été trouvé dans les textes lus
Une borne EXPLICITE, élémentaire, valable à TOUT couplage et en volume fini, de ⟨F^[q]⟩ (ou de |Σ_k ζ^{qk} Z_k| / Σ_k Z_k) par ρ^{aire}, obtenue en moyennant sur les torsions de toutes les colonnes ; la constante abstraite atteinte ρ_{N,q}(κ) = sup |A_q|/S ; la formalisation par le noyau. Ni les recherches web du jour, ni le corpus local, ni les passages lus ne contiennent un énoncé de cette forme. Absence NON prouvée : 't Hooft 1979, Mack–Petkova, Borgs, Seiler, Migdal et la plus grande partie de Münster n'ont pas été lus ; si l'un d'eux contient la borne, l'apport se réduit à la formalisation et à l'énoncé de la constante optimale.

## 5. Mots employés dans la note
« not found in the texts we read », « elementary », « probably folklore in principle », « we claim no priority » ; jamais « new ».

## 6. Restes à faire le jour de la publication
Rouvrir les dernières archives de BB26 (24147967) et de Mihajlovic (arXiv:2611.11534) ; une requête arXiv/INSPIRE sur « twist Fourier flux bound » ; si possible lire Münster en entier et Mack–Petkova 1980.
