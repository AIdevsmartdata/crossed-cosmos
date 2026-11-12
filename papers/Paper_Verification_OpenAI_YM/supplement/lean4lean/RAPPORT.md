# Vérification par lean4lean (11/11/2026, machine louée Vast)

Autorisation de Kévin (11/11 soir) : « J'autorise l'installation de lean4lean sur la machine » (machine louée seulement). Rien de public.
Journaux : `journaux/` (copie de `/work/lean4lean_essai/` sur la machine louée, sans les sources ni les .olean des témoins compilés).

## Révision, licence, dépendances
- Dépôt `digama0/lean4lean`, SHA **408edad8930c1d9d974f93fcbe4a304a174b2b6f** (commit parent du bump vers 4.33.0-rc2 ; `lean-toolchain` = `leanprover/lean4:v4.32.2`).
- AUCUNE révision n'a de `lean-toolchain` = 4.32.0 (historique : 4.29.0, 4.30.0, 4.31.0, 4.32.2, 4.33.0-rc2). Plus proche = 4.32.2. Construite avec la chaîne **4.32.0** (celle des .olean) SANS aucune adaptation du code (aucun diff) : la construction a réussi telle quelle.
- Licence lean4lean : Apache-2.0. Dépendance unique : `batteries` v4.32.2 (cb3961288e99f02ee3d23aab55391aebb258fd0c), Apache-2.0. Pas de Mathlib.
- Construction : `lake build lean4lean` (cible exécutable seule, 59 tâches), 39 s, code 0. sha256 de `src/.lake/build/bin/lean4lean` :
  `f3adb28da674b22c2848671d3791b25356ec3d41d7204767ef7783d533eb3d38`.
- Commandes : `journaux/build.sh`, `build.log`, `clone.log`.
- Usage : `lean4lean -v <Module>` rejoue, avec le noyau de lean4lean, les déclarations du module dans l'environnement obtenu par les importations (lues depuis les .olean, NON revérifiées).

## Étalonnage (réussi)
Mini-projet `/work/lean4lean_essai/temoins/` (sources dans `journaux/temoins/`, scripts `temoins.sh`, `t2.sh`).
- `TemoinVrai` (2+2=4 par rfl ; add_comm) : lean4lean code 0, « checked 2 declarations ». ACCEPTÉ.
- `TemoinFaux1` (`theorem False := True.intro` ajouté via `addDecl` avec `debug.skipKernelTC true`) : le .olean se compile (le noyau de Lean est contourné) ; lean4lean code 1, « (kernel) declaration type mismatch ». REFUSÉ.
- `TemoinFaux2` (`1 = 2 := Eq.refl 1`, même méthode) : compile ; lean4lean code 1, « declaration type mismatch ». REFUSÉ.
- Contrôle : `theorem : False := True.intro` sans l'option est refusé par `lean` (rc 1).
- Remarque cosmétique : l'impression du message d'erreur panique (« invalid environment extension ») ; le refus et le code de retour 1 sont corrects.

## Résultats sur le projet (olean de `/work/travail_4320/OpenAI-YM-20261028`, lecture seule, `LEAN_PATH` par `lake env printenv LEAN_PATH`, aucune recompilation)
| Module | Déclaration visée | Code | Durée | Mémoire max | Déclarations |
|---|---|---|---|---|---|
| YM.FullVolume.Luna.Ocho | YM.PhysicalNext.Repeat.Luna.uniformE | 0 | 25 s | 7,2 Go | 172 |
| YM.Pert.Align.Cancel | YM.Pert.Align.orbit_eq | 0 | 45 s | 3,9 Go | 49 |
| YM.Pert.Align.Drivers | YM.Pert.Align.key_orb | 0 | 21 s | 3,3 Go | 31 |
| YM.Pert.Lattice.Symbol | YM.Pert.Full.whole_apply | 0 | 22 s | 3,1 Go | 64 |
Chaque déclaration visée apparaît dans la sortie verbeuse (`adding thmDecl …`), donc a été rejouée par le noyau de lean4lean. `uniformE` : acceptée (ligne 48 de `run_Ocho.out`). Seule déclaration lente : `orbit_eq` (23,7 s côté lean4lean ; `wide_avg` 1,6 s, `wide_cont` 1,3 s).
Statut : **accepté par lean4lean** (code 0 + étalonnage réussi) pour ces 4 modules ; version : révision 408edad conçue pour 4.32.2, utilisée avec la chaîne 4.32.0 sans modification.

## Coût d'un élargissement (estimé, non lancé)
Échantillon de 20 modules (graine 42, `echantillon20.txt`) en un seul appel : code 0, 696 déclarations, 373 s, 92,7 Go de mémoire (chaque module ré-importe son propre environnement, ~4,6 Go ; temps surtout système). Le coût est dominé par le chargement des importations (~20 s et 3-7 Go par module, même pour 31 déclarations), pas par la vérification (35 déclarations par module en moyenne).
Estimation pour 9 470 modules : ≈ 9 470 × 22 s ≈ 58 h-processeur ; avec 16 processus séquentiels indépendants (un module à la fois chacun, ~16 × 5 Go) ≈ 3,5 à 5 h ; un appel unique avec le préfixe `YM` lancerait des milliers de tâches parallèles en mémoire : à NE PAS faire (extrapolation 4,6 Go × tâches). Machine chargée (charge ~135 sur 192 cœurs) : les durées sont pessimistes. Aussi : l'outil rescanne tous les .olean du chemin à chaque cible (coût fixe notable).

## Limites (ce que cela apporte et n'apporte pas)
- lean4lean est une AUTRE implémentation du noyau (code distinct de celui de Lean, auteur distinct), qui lève la limite de capacité rencontrée par nanoda sur `uniformE`. Il suit de près l'algorithme du noyau officiel (mêmes réductions, même ordre de vérification) : son accord est moins indépendant qu'un noyau d'une autre conception.
- Il est écrit en Lean et exécuté par le compilateur, l'environnement d'exécution et les bibliothèques de Lean 4.32.0 : une faille de ce socle (ou des structures de données `Environment`/`readModuleData`) n'est pas indépendante.
- Les importations de chaque module sont prises telles quelles des .olean ; elles ne sont pas revérifiées par lean4lean à ces étapes (leur validité repose sur la vérification de leurs propres modules : nanoda a déjà accepté 187 924 éléments sur 187 925, la dernière étant `uniformE`, maintenant acceptée par lean4lean).
- Les .olean utilisés sont ceux de la compilation de référence ; le lien avec l'export vérifié par nanoda est supposé (même compilation), non revérifié ici.
- Version : lean4lean 408edad (cible 4.32.2) avec chaîne 4.32.0, sans adaptation ; l'étalonnage valide la chaîne mais n'est pas une preuve de correction de lean4lean.
- Échantillon de 20 modules : exécuté pour le débit, accepté (code 0), mais ne constitue pas une vérification du projet entier.

## Vérification complète (lancée le 11/11 au soir, 19:25 UTC)
- Liste : 9 470 modules (9 457 `YM.*` + 13 racines : Challenge, ChallengeSpec, ConcreteSU2, Construction, ContactBridge, ContactSpec, HierarchyBridge, PublicTheory, PublicView, PublicWilson, Solution, TraceBridge, WilsonBridge), tirés des .olean de `/work/travail_4320` (lecture seule) : `modules.txt`. Écart : aucun. Réserve : lean4lean prend le nom de module comme PRÉFIXE ; 20 modules qui sont préfixes d'autres (ex. `YM.Work.A01`, `YM.Next.ROTATIONS`) revérifient aussi leurs sous-modules (redondance, pas d'erreur).
- Pilote `/work/lean4lean_essai/complet/lancer.sh` (lancé par `setsid nohup runuser -u lean -- env -i … bash -c "ulimit -n 1048576; nice -n 10 bash …/lancer.sh"`), un module par appel (`worker.sh`, `lean4lean <Module>`, chaîne 4.32.0, mêmes .olean), phase 1 : 8 modules à 4 processus, puis `xargs -P 20`. Reprise : un module dont le `.rc` existe est sauté (relancer la même commande).
- Résultats sur la machine louée, dans `/work/lean4lean_essai/complet/` : `rc/<module>.rc` (« code durée_s »), `echecs/<module>.log` (échecs seulement), `suivi.log` (une ligne par minute), `modules.txt`, `attendus.txt`, `pilote.log`, `FIN` (à la fin), bilan par `bash bilan.sh` (lecture seule). À rapatrier : tout ce dossier sauf `tmp/` (et `/work/lean4lean_essai/{build.log,clone.log}`) ; l'exécutable (sha256 f3adb28d…d38) n'est pas à rapatrier.
- Mesure à 19:29 : 125/9470 faits, 125 codes 0, 0 échec, ≈ 55 modules/min, mémoire disponible stable ≈ 220 Go (pic par processus ≈ 11 Go). Fin estimée ≈ 22:20 UTC (si les modules lourds ne ralentissent pas).
