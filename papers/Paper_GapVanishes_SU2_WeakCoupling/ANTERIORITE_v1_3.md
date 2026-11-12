# Antériorité du taux (note v1.3), 12/11/2026, faite par l'agent de montage (Sonnet 5.5). Rien de public.

Limites : recherche web GÉNÉRIQUE (aucun de nos textes envoyé), corpus local (`ragh-lit`), texte du concurrent. Ce n'est pas une recherche
exhaustive. Je n'ai LU aucun des articles cités ci-dessous (titres, résumés et métadonnées Crossref seulement) : ce que je dis de leur contenu est
« abstract read » ou « de mémoire, non vérifié ».

## (a) Dernière version du concurrent (BB26)
`curl -sL https://zenodo.org/api/records/23444338/versions/latest` (12/11/2026, ~08h20) : enregistrement 24147967, version 5.0.0, créé 2026-11-11T23:29:13 UTC,
titre « The Yang-Mills Mass Gap from One Bound at One Scale », un fichier zip (3 042 889 octets), DOI 10.5281/zenodo.24147967. Aucune version postérieure à celle lue.
Réponse sauvegardée : `anteriorite/latest.json`.

## (b) Leur texte (papier.txt de la v5.0.0, lu en entier le 12/11 par un agent précédent : `chantiers/concurrents_2026-11-12/LECTURE_COMPLETE_BB26_v5.md`)
- Volume infini : NON (Q3 de cette lecture : Prop. 7.26, l. 2302-2311, ne demande qu'un taux ~1/N pour (Z) ; l. 3809-3821 : (W) et (B**) restent ouverts). Mes recherches par mots-clés
  de ce matin dans le texte (infinite volume, translation invariant, Gibbs state, Stein, polynomial, weak coupling, closes, vanish) : aucune apparition d'un majorant du trou d'un état
  de Gibbs invariant par translation à couplage faible, avec ou sans taux. Les seules occurrences d'« infinite-volume Gibbs state » sont l. 372 (formalisation Lean d'un état limite de tores, régime de couplage FORT) et l. 4376 (limites de tores, βW ≤ 9/25, couplage fort).
- Leur seul taux est le Thm 7.59 (l. 3699-3785), à taille de tore fixée ; voir la conversion de β dans la note (c = 2β_BB = β/2).
- Conclusion : aucun taux ni énoncé en volume infini chez eux. Réserve : lecture de passages + mots-clés, pas d'une lecture ligne à ligne des 157 pages.

## (c) Littérature (Crossref vérifié ; contenu NON lu)
| Référence (vérifiée Crossref) | Ce que c'est (degré de certitude) | Un taux pour le trou en découle ? |
|---|---|---|
| S. Chatterjee, *The leading term of the Yang–Mills free energy*, J. Funct. Anal. 271 (2016) 2944–3005, doi:10.1016/j.jfa.2016.04.032 | terme dominant de l'énergie libre U(N), 3D quand a→0 ; en 4D seulement à couplage faible ; boîtes à bord libre (résumé lu, déjà cité dans la note comme [Cha16]) | non : énergie libre, pas de trou |
| S. Cao, *Wilson Loop Expectations in Lattice Gauge Theories with Finite Gauge Groups*, Commun. Math. Phys. 380 (2020) 1439–1505, doi:10.1007/s00220-020-03912-z | groupes de jauge FINIS, couplage faible, boucles de Wilson au premier ordre ; la recherche web dit : réduction à une approximation de Poisson traitée par la méthode de Stein (résumé de la recherche, non lu) | non : groupes finis, pas de limite gaussienne, pas de trou |
| A. Adhikari, S. Cao, *Correlation decay for finite lattice gauge theories at weak coupling*, Ann. Probab. 53 (2025) 140–174, doi:10.1214/24-AOP1702 | décroissance des corrélations à couplage faible, groupes FINIS (titre vérifié ; contenu de mémoire) | non pour SU(2) : groupe fini seulement. Elle va dans le sens CONTRAIRE (décroissance, trou positif) pour les groupes finis, ce qui n'est pas en contradiction : le mécanisme de notre note vit dans le groupe continu (modes de Goldstone / photon libre) |
| S. Chatterjee, *A scaling limit of SU(2) lattice Yang–Mills–Higgs theory*, Probab. Math. Phys. 7 (2026) 339–381, doi:10.2140/pmp.2026.7.339 (arXiv:2401.10507, titre vérifié) | limite d'échelle GAUSSIENNE MASSIVE (champ de Proca) avec champ de Higgs en brisure complète de symétrie | non : avec Higgs la limite est massive ; ce n'est pas Yang–Mills pur. Mentionné dans la note [Cha24] |
| Rajasekaran–Yakir–Zhou, *Gaussian limits of lattice Higgs models with complete symmetry breaking*, arXiv:2603.24555 (titre vérifié sur arxiv.org/abs, non publié en revue à ma connaissance) | idem pour tout groupe compact connexe, d≥2 | non (idem). Mentionné dans la note [RYZ26] |
| S. Chatterjee, *Yang–Mills for probabilists*, Springer Proceedings in Mathematics & Statistics (2019), 1–16, doi:10.1007/978-3-030-15338-0_1 | le Problème 5.1 (déjà traité dans la note) | non |
| A. Guth, Phys. Rev. D 21 (1980) 2291–2307, doi:10.1103/physrevd.21.2291 ; J. Fröhlich, T. Spencer, Commun. Math. Phys. 83 (1982) 411–454, doi:10.1007/bf01213610 | U(1) 4D à couplage faible : phase non confinante / sans masse (photon sans masse) | non pour le taux ; c'est le filtre F1 : notre majorant vaut aussi pour U(1) en phase de Coulomb où m = 0 |
Recherche web (deux requêtes génériques) : « Gaussian limit lattice Yang–Mills weak coupling Stein's method » → articles ci-dessus ; « upper bound mass gap lattice gauge theory weak coupling … » → aucun majorant rigoureux du trou, quelques préprints 2025-26 sur le couplage FORT (non lus, non cités). Corpus local `ragh-lit` (deux questions) : trouve Guth 1980, des notes internes, un préprint arXiv:2606.19362 (couplage fort) ; rien sur un majorant du trou à couplage faible.

## (d) Classique / chez d'autres / à nous
- **Classique** : méthode de Stein par l'équation d'Ornstein–Uhlenbeck, solution de Stein à gradient borné indépendamment de la dimension (constante √(π/8) pour la loi gaussienne et une fonction test à valeurs dans [0,1] : c'est la borne de type Barbour / Götze / Chatterjee–Meckes pour le sup du gradient de u, certitude MOYENNE sur l'attribution, rédigée entièrement dans la note donc invérifiée par citation ; [MEMORY, UNVERIFIED : Stein 1972, Barbour 1990, Götze 1991]) ; principe variationnel pour l'opérateur de transfert ; positivité par réflexion de l'action de Wilson (OS78, Lüscher) ; le fait que le champ de Yang–Mills sur réseau est gaussien à petite échelle à couplage faible (idée citée par Chatterjee).
- **Chez d'autres** : la limite gaussienne (sans taux) avec Higgs [Cha24, RYZ26] ; Stein pour des boucles de Wilson de groupes finis [Cao] ; le trou à taille de tore FIXÉE avec taux (log β)/β [BB26 Thm 7.59].
- **À nous (sous réserve de la recherche ci-dessus)** : le théorème en volume infini sans unicité (v1.0–1.2) ; la comparaison de Stein de la loi conditionnelle dans une boîte qui grandit avec β ; le taux β^{-1/120} log β. Certitude : MOYENNE-FAIBLE sur la nouveauté (recherche bornée, pas de spécialiste humain). Aucun énoncé trouvé qui implique le nôtre ou donne un taux en volume infini. Aucun texte lu en entier hors BB26.
- Antériorité interne : `chantiers/pistes_2026-11-12/PISTES.md` P4 (12/11, 06h27) posait le but ; `chantiers/majorant_trou_2026-11-11/RESULTAT.md` §6.1 (conjecture, sans exposant).
