# Certificat de rejeu par un non-auteur — seize énoncés `CentreZN` (12/11/2026)

**Rejoueur** : Claude Sonnet 5.5 (session lancée par le pilote). Il n'est PAS l'auteur du théorème (Claude Opus 5.5), ni des preuves Lean (GPT-6.1 Sol), ni des outils de contrôle de l'auteur (`chantiers/centre_zn_2026-11-12/outils/`, que je n'ai pas utilisés : j'ai écrit les miens, dossier `outils/`). Le rejoueur est un modèle de la même famille que l'auteur du théorème : ce n'est pas un humain ni un laboratoire indépendant.
**Fichiers rejoués** : copie des fichiers de l'auteur (sha256 vérifiés ci-dessous) ; aucun fichier de l'auteur n'a été modifié.

## Résultat en une phrase
Les seize énoncés sont acceptés : Lean 4.32.0 (code 0, 0 erreur, trois axiomes standard seulement), Lean 4.32.2 (code 0, même résultat), noyau indépendant nanoda (« Checked 35154 declarations with no errors » sur l'export de la clôture des seize déclarations) ; leurs types sont égaux, terme à terme, à ceux des énoncés figés (16/16) ; six mutants échouent tous. Cela ne vérifie PAS le cas SU(N) 4D, la constante tanh, ni les formes closes (sur papier).

## 1. Empreintes des entrées
| fichier | sha256 |
|---|---|
| `ENONCES_GELES.lean` (énoncés figés) | `17f5a9116a371aa8ca0d4498be7da4f2499521b95ab0188d84449618908db863` (= valeur de `ENONCES_GELES.sha256`, `sha256sum -c` : OK) |
| `CentreZN_A_PROUVE_tour2.lean` (Sol, partie A, 991 lignes) | `e725fe1c9f017d68819128d562fdb26c20b0b2019e1d360a73a60a00154d0d89` |
| `CentreZN_B_PROUVE_tour2.lean` (Sol, partie B, 626 lignes) | `8093df18ffac42fd0759c88ee11966c29d0deaa6bdcecd1e7c648f6d82d1917c` |
| `GELE_A.lean` (en-tête figé) | `e0ac8f8a28f42a548f69a618cbd3d76b86f97f53446ec4bdeedb756a2be6345c` |
| `DEFS_B.lean` (définitions B figées) | `137e9dec4286eae6f2dba37a6c4967bf8edd2dea56437f25dafe629e69ebb6c7` (identique au texte des définitions de `ENONCES_GELES.lean`) |
| `build/main.lean` (mon assemblage : GELE_A + A + DEFS_B + B + fichier figé renommé `CentreZNFrozen` + comparaison des types + 16 `#print axioms`) | `fc11b8e1bfb1fcf74f6c39d5134b802e5c57fdba8ed7a8a97ab18c53b5d985d9` (100 538 octets) |
| `build/zn_sans_meta.lean` (même chose sans comparaison ni fichier figé : pour les essais en bac 4.34.0) | `815c26edb1828f303deb01046395aaf36c8e5c24abe625afdb3481eadfc8e94f` |
Le préfixe GELE_A + A + DEFS_B + B est octet pour octet le début du fichier complet de l'auteur (`certificat/final1/CentreZNComplet.lean`, `d69ca94a…15e6`) : seuls les pieds diffèrent (les miens ne réénoncent rien ; ils comparent les types et impriment les axiomes).

## 2. Contrôles de texte (`outils/verif_locale.py`, lecture seule, aucune compilation)
* Pour chacun des 16 théorèmes, le texte de `theorem NOM` à `:= by` est identique au caractère près entre le fichier figé et le fichier prouvé (et à espaces normalisés).
* Définitions de la partie B : figées = `DEFS_B.lean`.
* Mots interdits, hors commentaires et chaînes : `sorry`, `admit`, `axiom`, `native_decide`, `unsafe`, `implemented_by`, `opaque`, `extern`, `partial`, `macro`, `syntax`, `elab`, `notation`, `initialize`, `run_cmd`, `import`, `set_option`, `attribute`, `instance`, `local`, `scoped`, `variable`, `universe`, `@[`, lignes `#…`, `open` : **aucun** dans les fichiers de Sol (A, B) ni dans `DEFS_B`. (Les fichiers de Sol contiennent des lemmes et définitions auxiliaires `zn_*`, `znb_*` : aucun n'entre dans les énoncés.)
* Écart de procédure : ce script de lecture (Python écrit par un modèle) a été lancé directement sur l'acemagic, avant que la règle 9 amendée (bac sans droits) me soit communiquée ; il ne fait que lire quatre fichiers et ne produit aucune écriture ; son essai en bac n'était pas possible (le bac n'a pas accès à ces fichiers).

## 3. Lean 4.32.0 — machine louée `kvu-1112`, dossier neuf `/work/lean_zn_rejeu_1112/`, utilisateur `lean`
Environnement : chaîne `/work/tc/4.32.0` (commit `8c9756b2`), Mathlib compilé du projet d'OpenAI (v4.32.0), utilisé en lecture seule par `LEAN_PATH` (obtenu une fois par `lake env printenv LEAN_PATH`, puis `lean` appelé directement). Scripts : `outils/rejeu_4320.sh`, `outils/mutants_4320.sh`. Journaux : `journaux/main.log`, `main.out`.
| contrôle | résultat |
|---|---|
| compilation de `main.lean` (`lean -R … -o …olean`), 06:11:56–06:13:35 UTC (99 s) | **code de retour 0** (lu sur la ligne `RC=` écrite par le script après la commande, pas sur un `tail`) ; 0 erreur ; 2 avertissements de style (`hpar` inutilisé ; argument `simp` inutile) + 16 `declaration uses sorry` qui viennent du fichier FIGÉ renommé (voulu : ce sont les énoncés de comparaison) |
| axiomes des 16 théorèmes `CentreZN.*` | 16 lignes : 15 = `[propext, Classical.choice, Quot.sound]`, 1 (`mixed_word_neutral`) = `[propext, Quot.sound]` ; aucun autre axiome, pas de `sorryAx` |
| types contre énoncés figés (`#eval` de comparaison d'`Expr` : type de `CentreZNFrozen.NOM` avec préfixe remplacé = type de `CentreZN.NOM`) | **« BILAN types identiques : 16 sur 16 »** |
| export de la clôture des 16 déclarations (lean4export de la location, binaire de l'auteur de l'outil non modifié), 129 s | code 0 ; 3 394 007 lignes ; sha256 de l'export `54f81bf268aabd52dbdeebd0216eb21b773b3cce3f1d4342b3db30d6ca0ff106` |
| noyau indépendant nanoda (binaire non modifié, trois axiomes permis, erreur dure sinon), 35 s, 244 Mo | « **Checked 35154 declarations with no errors** », code 0 (`journaux/nanoda.log`, `zn.json`, `nanoda_pp.txt` : énoncés imprimés sans les preuves) |
(L'auteur annonce 35 170 déclarations : il exportait en plus les 16 réénoncés de ses pieds ; ici 16 déclarations de moins, cohérent.)

### Mutants (tous compilés par `lean` 4.32.0 sur la même base ; tous doivent échouer) — `journaux/mut_*.out`
| mutant | modification de l'énoncé seulement | résultat |
|---|---|---|
| M1a | constante de `rho_crude` : `exp(-2‖t‖)` → `exp(-‖t‖)` (1 − e^{−κ} au lieu de 1 − e^{−2κ}) | **échoue** (code 1) : « unsolved goals » dans la preuve de `rho_crude` ; les corollaires qui l'utilisent échouent aussi (`linarith failed`) |
| M1b | idem partout (`rho_crude`, `centre_flip_bound_crude`, `twist_ratio_bound_crude`) | **échoue** (code 1) : « unsolved goals », « `apply` failed: could not unify the conclusion of `centre_flip_bound` » |
| M2 | hypothèse `q ≠ 0` de `rho_crude` remplacée par `q = q` (donc retirée) | **échoue** (code 1) : erreurs d'application dans `rho_crude` et chez les utilisateurs (la preuve de Sol utilise réellement `hq`) |
| M3 | surjectivité des charges de `centre_flip_bound` remplacée par `surjective ∨ True` (donc inutilisable) | **échoue** (code 1) : « `rcases` failed » à l'endroit où la preuve exploite la surjectivité |
| M4 | image des charges de `twist_ratio_bound` remplacée par `… ∨ True` | **échoue** (code 1), même endroit |
| M5 | `2 ≤ m` de `torus_charge_image` → `0 ≤ m` | **échoue** (code 1) : `omega could not prove the goal` dans la construction (l'énoncé est faux pour m = 1) |
Limite : M3 et M4 échouent parce que la preuve utilise l'hypothèse, pas parce que j'ai exhibé un contre-exemple à l'énoncé affaibli ; M1, M2, M5 échouent à des étapes mathématiques (inégalités, construction).

## 4. Lean 4.32.2 — même machine, chaîne et Mathlib pris dans les archives locales du 11/11
Archives envoyées par `scp` dans mon dossier (`actif_lean_4322.tar.zst`, sha256 `0ef68786d8b386579b513cb1ea1d6e2aefd952ace2942091a164038956a6a555` ; `tc.tar.zst`, `f8f3768f5b46f517c8095c36636335ca4d8143b25fa94a006eeb130e7e0533cd` ; empreintes locales vérifiées par `sha256sum -c` avant l'envoi), extraites par l'utilisateur `lean` dans `/work/lean_zn_rejeu_1112/` (rien d'installé en root, rien touché ailleurs). Chaîne `Lean (version 4.32.2, commit f3b06c70)`, Mathlib recompilé sous 4.32.2 (`.lake/packages/*/.lake/build/lib/lean`). Script `outils/rejeu_4322.sh`, journaux `journaux/r4322.log`, `main4322.out`.
| contrôle | résultat |
|---|---|
| compilation du MÊME `main.lean` (sha256 `fc11b8e1…`), 104 s | **code 0** ; 0 erreur ; mêmes avertissements |
| axiomes | 16 lignes : 15 × `[propext, Classical.choice, Quot.sound]`, 1 × `[propext, Quot.sound]` |
| types contre énoncés figés | « BILAN types identiques : 16 sur 16 » |
| nanoda sur un export 4.32.2 | **NON FAIT** : le binaire `lean4export` de la location est celui de 4.32.0 et refuse les `.olean` 4.32.2 (« incompatible header ») ; je n'ai pas recompilé l'outil |

## 5. Lean 4.34.0 (bac sans droits de l'acemagic, `qlab_exec --ou acemagic --kind lean`) — essai sans adaptation
`build/zn_sans_meta.lean` : **ne compile pas** (3 erreurs, toutes dans les lemmes auxiliaires de Sol, aucune dans un énoncé) : `failed to synthesize MulLeftMono ℝ` (ligne 100) et deux `Decidable (zn_charge (zn_sign …) = …)` (ligne 254). Journal : `journaux/bac434.json`, `bac434_stdout.txt`. Les fichiers sont des fichiers Lean 4.32.0 ; aucune adaptation n'a été tentée.

## 6. Ce que ce rejeu ne couvre pas
* Reconstruction de Mathlib ou du projet d'OpenAI depuis les sources, et vérification de leur commit : non faites (comme pour la v1.1) ; la base est l'environnement compilé de la location.
* Un export nanoda sous 4.32.2 ; un rebâtissage sur une autre machine ; un humain.
* Les objets du réseau 4D (liens longs, plaquettes mixtes, SU(N)) : les énoncés Lean de la partie B portent sur un groupe abstrait et un tore × fibre abstraits ; l'instanciation à SU(N) est sur papier.
* Concordance énoncé par énoncé avec le texte : voir la partie II de `CONCORDANCE_TEXTE_LEAN.md` (seize lignes) ; aucun écart de fond.

## 7. Chaînes utilisées, par tâche
| tâche | chaîne |
|---|---|
| rejeu principal, mutants, export, nanoda | Lean 4.32.0 + Mathlib v4.32.0 (location `kvu-1112`, utilisateur `lean`) + lean4export/nanoda de la location |
| seconde version | Lean 4.32.2 + Mathlib recompilé 4.32.2 (archives locales du 11/11, extraites dans mon dossier de la location) |
| essai 4.34.0 | bac sans droits de l'acemagic, Lean 4.34.0 + Mathlib : échec |
| scripts de texte (comparaison d'énoncés, mots interdits) | Python 3 sur l'acemagic, lecture seule |
