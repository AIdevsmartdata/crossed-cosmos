# Reconstructions Lean depuis l'archive git, 11/11/2026 (machine louée Vast, utilisateur `lean`, /work/lean_nous/)

Rien n'a été publié, poussé, étiqueté ni envoyé. Journaux complets (horodatés UTC, chaque commande et son code de retour) :
`/root/physique/publication/reconstructions_lean_2026-11-11/journaux/{D7,aire,crit,p2}.log` ; archives, scripts distants et
fichiers copiés sont dans le même dossier. Mémoire consultée : lecture de la liste de contrôle, des procédures, de `RESULTAT.md`,
`VERDICT.md`, `MANIFEST.txt` (pas de requête `ragh`).

## Quelle révision, quel dossier
- Dépôt public `AIdevsmartdata/crossed-cosmos`, clone `publication/D7_dobrushin/_push_clone`, `origin/master` = `10d511b3e88d3389821016542e588809e5ecd688`
  (tag v7.9.0, loi d'aire v1.1). Aucun paquet v1.6 / v1.2 n'existe encore (seuls les brouillons TeX) : la « révision publiée »
  est donc la dernière du dépôt public.
- D7 : `papers/Paper_Dobrushin_SU2_Wilson/lean` (arbre git `ec9f79c`). Loi d'aire : `papers/Paper_AreaLaw_SU2_4D/supplement/lean`
  (arbre `806a54a`) plus `.../supplement/data` (arbre `8716469`, pour le certificat m = 11).
- Le Lean n'a pas changé : `git diff v7.7.0 10d511b` sur le dossier D7 est vide ; `git diff v7.8.0 10d511b` sur le dossier loi d'aire est vide.
- Ces deux dossiers sont la source du futur paquet ; si le paquet v1.6 / v1.2 est régénéré, ses dossiers `lean/` doivent être comparés
  octet pour octet à ces arbres (non fait, le paquet n'existe pas).

## Résultats

| Projet | Révision / source | Empreinte de l'archive (sha256) | Lean | Mathlib | Build | Axiomes | Durée | Verdict |
|---|---|---|---|---|---|---|---|---|
| D7 (Dobrushin, 6 modules) | 10d511b, `git archive` tar.gz | 708c01ea93d67a5fc2dbc91e961bb9ebd92d662150106258f0865bdf32785f50 | 4.34.0 | v4.34.0 = 5ed2965256430c3649e86755f9576b54eca72435 | `lake build` RC 0 (8930 jobs) | 29 théorèmes, tous ⊆ {propext, Classical.choice, Quot.sound}, identiques au log livré (29) | build 233 s ; total 254 s | VERT |
| Loi d'aire (LoiAire, 12 modules) | 10d511b, `git archive` (lean : fca90026016b86d25fb58127c15f7f1d3842a25b0b09ab205ae5d5b0ef5ff258 ; data : 5585bc36b9e6c21bd194a6f7f55a397e96e2304996407e08b802c01025075c8e) | idem | 4.34.0 | idem 5ed2965 | `lake build` RC 0 (8936 jobs, CertPetits 478 s) ; `lake build verifcert` RC 0 | 52 constantes, aucune hors standard, liste identique mot pour mot à `logs/print_axioms.log` livré ; `verifcert` sur le certificat m = 11 (sha256 du .bin décompressé b50d3769…cf142 conforme) : `verifiePar … = true`, « CertificatPerron 11 … : ETABLI (par exécution compilée) », RC 0 | build 715 s ; verifcert 2 598 s ; total 3 356 s | VERT |
| Critère scalaire (`critere_scalaire_2026-11-11/lean/main.lean`) | PAS dans un dépôt git : copie avec empreintes, sha256 main.lean 944a99f6fc10f1696e6dfa5bc231b73dd9c57a101b48518c52e3e4ca944ef2c6 (= MANIFEST) | sans objet | 4.34.0 | 5ed2965 (manifeste de D7 recopié) | `lake build` RC 0 (8925 jobs) | 35 déclarations, toutes {propext, Classical.choice, Quot.sound} | build 212 s ; total 243 s | VERT |
| P2 doublement 4D (`vision_20261025/calculs/P2_doublement_4d/lean/KevDoublement4D.lean`) | PAS dans un dépôt git : copie, sha256 5ef59bc05900c16e455d4b1698d33cf235483af20355ddcead2e0c99030d2f37 | sans objet | 4.29.1 (comme l'original) | 5e932f97dd25535344f80f9dd8da3aab83df0fe6 (rev du manifeste lean06, `lake update`) | `lake build` RC 0 (8249 jobs) | 8 théorèmes imprimés (les 6 du VERDICT + `iteration`, `racine`), tous standard | build 230 s ; total 257 s | VERT |

Lecture de « aucun sorry » : `grep -E '\b(sorry|admit|native_decide)\b|^\s*axiom\b'` sur tous les .lean (hors `.lake`) : rien pour D7, loi d'aire, P2 (rc 1).
Critère scalaire : 4 lignes trouvées dans `main.lean`, toutes des phrases de docstring/commentaire (« No axiom, no `sorry` »), aucune occurrence en code ;
la compilation sans `sorry` est confirmée par l'absence d'avertissement « declaration uses sorry » (le build ne contient que des avertissements de linter).

## Commandes (communes, détail dans les journaux)
`curl` des toolchains officielles `lean-4.34.0-linux.tar.zst` et `lean-4.29.1-linux.tar.zst` (sha256 contrôlés contre le champ `digest` de
`gh api repos/leanprover/lean4/releases/tags/vX` : caaa9835…b646b et bf062d29…aec1, concordants) ; `tar xzf` de l'archive git dans un dossier
neuf ; `ulimit -n 1048576` ; `taskset -c 0-31 nice -n 10 lake exe cache get` (cache officiel, 5 980 / 8 908 / 8 232 fichiers décompressés) ;
`lake build` ; `lake env lean PrintAxioms.lean`. Pour le critère scalaire et P2, j'ai écrit un `lakefile.toml` minimal (et un `PrintAxioms.lean`
généré à partir de `build4_axiomes.txt` pour le critère) : fichiers dans `reconstructions_lean_2026-11-11/nous/`. Plafonds respectés : 32 cœurs
(`taskset`), nice 10, disque ≈ 25 Go.

## Écarts avec la procédure / incidents
1. Procédure D7 et liste de contrôle : le « rejeu depuis `git archive` » n'est pas encore faisable sur un paquet v1.6 / v1.2 qui n'existe pas ; fait sur le tag publié (le Lean est identique, voir plus haut).
2. Nanoda NON exécuté : les binaires de `/work/outils/bin` sont construits pour Lean 4.32.0, ces projets sont en 4.34.0 (et P2 en 4.29.1). Non réutilisables sans improviser ; le journal nanoda livré (`nanoda_pipeline.log`, 43 458 déclarations) n'est donc pas rejoué. Pour le faire : construire `lean4export` pour v4.34.0 et un nanoda 0.4.19, à décider.
3. Première tentative : échec bête de ma part (`lake build -j` n'existe pas dans Lake 5.0.0) ; logs conservés `*_essai1_ECHEC_option_-j.log`, relance corrigée. Un compteur de code retour du `grep` était aussi faux dans le script v1 (corrigé en v2).
4. Le piège de la limite de fichiers est confirmé : sous `runuser`, soft 1024 / hard 1048576 ; `ulimit -n 1048576` dans le script a suffi.
5. Machine chargée (load ≈ 170 sur 192) : `verifcert` a pris 2 598 s au lieu de ~6 100 s annoncés par le README (1 h 42), avec 32 cœurs.
6. Pour P2 et le critère, ce n'est pas « depuis git » : copies avec empreintes. P2 : le VERDICT parle de `chantiers/lean06/lean` (Lean 4.29.1) ; reconstruit ici dans un projet isolé avec la même révision Mathlib, mêmes six théorèmes, mêmes axiomes. Les dépendances de P2 ont été résolues par `lake update` (manifeste produit : `journaux/p2_lake-manifest.json`) et non reprises de lean06.

## Reste à faire à la main pour le paquet (rien de fait)
- Régénérer les paquets v1.6 (D7) et v1.2 (loi d'aire) ; vérifier que leur dossier `lean/` est octet pour octet l'arbre git ci-dessus (`git diff --no-index` ou `sha256sum`), puis copier ce rapport et les journaux dans le dossier de justification si voulu.
- Décider pour nanoda (voir écart 2) ; la procédure D7 ne l'exige pas explicitement, le README loi d'aire le mentionne.
- Pour le critère scalaire et P2 : les mettre dans un dépôt git si on veut une vraie reconstruction « depuis l'archive ».
- Les étapes de la procédure qui restent publiques ou irréversibles (push, tag, dépôt Zenodo) sont intactes, non lancées : attendre le délai du 12/11 18h40 et le GO de Kévin.
