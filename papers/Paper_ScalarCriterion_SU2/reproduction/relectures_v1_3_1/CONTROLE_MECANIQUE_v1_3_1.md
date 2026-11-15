# Contrôle mécanique v1.3 → v1.3.1 (15/11/2026)

- `diff redaction/v1_3_publiee.tex note/scalar_criterion_su2_v1_3_1.tex` (copie de la v1.3 publiée, sha256 513d388e…, identique à celle du paquet v1.3) : 7 blocs.
  Lignes supprimées : 2 seulement : `\date{12 November 2026 (version 1.3)}` et la phrase finale « The human author read the final text of this note … » (remplacée comme décidé).
  Blocs ajoutés : (1a2) ligne de commentaire de version ; (57c58) date ; (103a105,106) paragraphe « Version 1.3.1 » du résumé (renvoi à la notice) ; (105a109,159) la notice ; (1377a1432) entrée « Version 1.3.1 » dans la déclaration sur l'usage de l'IA ; (1384c1439) phrase sur l'auteur humain ; (1440a1496,1508) douze entrées de bibliographie. AUCUN autre changement : pas une phrase du corps, pas un énoncé, pas une preuve.
- Numérotation : `\newlabel` des .aux (80 étiquettes de sections, équations, théorèmes) comparés : écart unique = la nouvelle étiquette `sec:notice` (section non numérotée, valeur vide). Aucun numéro n'a bougé.
- Compilation (pdflatex, trois passes) : RC 0, zéro référence indéfinie, 5 boîtes « Underfull » comme dans la v1.3 (0 nouvelle, mêmes lignes de code hors notice) ; 46 pages (v1.3 : 42 ; la notice occupe environ 3,3 pages en `\footnotesize`) ; texte du PDF reproductible (recompilation dans une compilation séparée, `pdftotext` identique).
- `pdftotext` comparé mot à mot v1.3 / v1.3.1 : les différences sont des numéros de page et la table des matières ; comparaison non concluante en soi, le diff du .tex fait foi.
- Mots interdits dans les lignes ajoutées : aucun nom de machine, d'outil, de dossier ni prénom ; « independent », « new », « first » n'apparaissent que dans des CITATIONS de nos propres phrases (« What we believe is new here… », « was first written… ») et dans la phrase qui dit à quoi se rapportent « independent derivation » / « obtained independently » ; aucun mot de copie.
- Dates : voir la table des faits (fournie à l'auteur humain) ; réponses d'API du 15/11 dans les réponses publiques d'API du 15 novembre 2026.

## Refait le 15/11 au soir (après les trois ajouts)
- Mêmes 7 blocs ajoutés, 2 lignes supprimées (la date, la phrase de l'auteur humain) ; nouveaux numéros de lignes : 1a2, 57c58, 103a105,106, 105a109,159, 1377a1432, 1384c1439, 1440a1496,1508 (douze entrées de bibliographie : les onze du premier jet, plus Asano–Nishimura et le brouillon « Thermal Purity Bounds », moins aucune).
- Étiquettes : 80 comparées, écart unique `sec:notice`. RC pdflatex 0 ×3, zéro référence indéfinie, 5 « Underfull » (comme la v1.3), 46 pages, texte du PDF reproductible par recompilation séparée.
- PDF sha256 acfe8070…, .tex sha256 30483061….

## Refait le 15/11 à la fin de la soirée (classiques lus : 't Hooft, van Baal–Koller, Koller–van Baal, Tomboulis–Yaffe)
- Mêmes 7 blocs ajoutés, 2 lignes supprimées (la date, la phrase de l'auteur humain) ; lignes : 1a2, 57c58, 103a105,106, 105a109,161, 1377a1434, 1384c1441, 1440a1498,1512 : QUINZE entrées de bibliographie (onze travaux de la notice, Asano–Nishimura, le brouillon BB26, van Baal–Koller, Koller–van Baal ; « douze » dans la section précédente était un décompte erroné, corrigé ici).
- 80 étiquettes comparées, écart unique `sec:notice`. RC pdflatex 0 ×3, zéro référence indéfinie, 5 « Underfull » (comme la v1.3), 47 pages, texte du PDF reproductible. Aucun mot interne ni mot de copie dans les lignes ajoutées.
- PDF sha256 7383f5cd…, .tex 10bd3aa4….

## Refait le 16/11 (décision de l'auteur : erratum inséré, date 16 novembre 2026)
- Ajouts par rapport au 15/11 : l'erratum « Erratum to Section 8 of version 1.3 » (fin de la notice), une phrase de renvoi (paragraphe sur le Théorème L), la date 16 November 2026 (titre de la notice, \date, ligne de version, paragraphe du résumé, entrée « usage de l'IA »).
- Diff v1.3 → v1.3.1 : 7 blocs ajoutés, 2 lignes supprimées (la date, la phrase de l'auteur humain) ; lignes : 1a2, 57c58, 103a105,106, 105a109,162, 1377a1435, 1384c1442, 1440a1499,1513. Rien hors des catégories permises ; l'erratum est DANS le bloc de la notice.
- 80 étiquettes comparées : écart unique `sec:notice`. pdflatex RC 0 ×3, zéro référence indéfinie, 5 « Underfull » comme la v1.3, 47 pages, texte du PDF reproductible par recompilation séparée. Aucun mot interne ni mot de copie dans les lignes ajoutées.
- PDF sha256 26e41481…, .tex sha256 1b9b9323….
