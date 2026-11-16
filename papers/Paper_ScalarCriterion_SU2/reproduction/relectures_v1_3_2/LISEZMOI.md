# Version 1.3.2 : pièces de la preuve de remplacement du Lemme C(c)

- `C3_preuve_maitre_en.md` : texte maître (anglais) de la preuve de remplacement ; le paragraphe de la note en est la rédaction condensée.
- `C3_algebre_qwen4.lean` : huit inégalités élémentaires (L1, L2a, L2b, L3, L4a, L4b, L4c, F2scalar) : identité (F1) sur les composantes d'un quaternion unité, produit des majorations |sin|, arithmétique de la région d'intégration, comptes de dimensions. Le fichier imprime trois fois la liste des axiomes (sans effet). Aucun `sorry`.
- `C3_algebre_sortie_bac.json` : sortie de la compilation au bac à sable (code 0, 0 erreur, pas de `sorry`, axiomes `propext`, `Classical.choice`, `Quot.sound`).
- `CONTROLE_MECANIQUE_v1_3_2.md` : contrôles mécaniques de la version.
- Ce que ces pièces ne contiennent pas : la partie analytique (carte, densité de Haar, intégration) n'est pas formalisée ; aucun humain n'a relu la preuve.
