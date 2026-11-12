# Certificat de rejeu de la réciproque (Théorème R) — 12/11/2026, par un non-auteur

Rejoueur : Claude Sonnet 5.5 (agent du pilote), qui n'a écrit ni la preuve papier (GPT-6 Astra), ni les preuves Lean. Rien de public.
Statut obtenu : **VÉRIFIÉ PAR LE NOYAU (deux chaînes Lean + noyau indépendant nanoda), en forme ABSTRAITE** ; non formalisés : (d) rapport d'aspect ≤ 24, forme logarithmique de (c), formule de Casimir, passage côtés ≥ 3 → ≥ 1, corollaire pont.

## Fichiers rejoués (copies dans `lean_rejeu/` ; mêmes octets que ceux du dossier de l'agent auteur, `chantiers/reciproque_critere_2026-11-12/lean/`)
| fichier | sha256 |
|---|---|
| `ENONCES.lean` (énoncés figés avant les preuves) | 6a2c0e9f73c062a0009198aaf2829b324bc38e844b13a43d3a06ceec66120af8 (identique à `ENONCES.sha256`) |
| `RECIPROQUE_full.lean` (= `lean/Reciproque.lean` du paquet), 474 lignes | efa8870dc236ef5d5a35d92e45e7cd7408573b2229e18d633404c017ab9d4dbb |
| `COMBINE.lean` + une ligne `#print axioms Reciproque.interpolation` (= `lean/main_v1_2.lean` du paquet) | 78cecaa42cc1ea48197908718afeb23f3017ffab6cb3fb48ecc4749c6c838b2e |
| `main.lean` publié (v1.0/v1.1) | 944a99f6fc10f1696e6dfa5bc231b73dd9c57a101b48518c52e3e4ca944ef2c6 (inchangé) |
| `CritereScalaire.lean` publié | 0c4264a7c3f665346d1e479f6ed99e8b531b3b23960efcc718095d4ed4fe8496 (inchangé) |

## 1. Contrôles statiques (script `lean_rejeu/verif_statique.py`, sortie `verif_statique.out`) : VERDICT_STATIQUE OK
* les quatre énoncés (`facile`, `interpolation`, `reciproque_Bstar`, `trou_cubes`) de `RECIPROQUE_full.lean` et de `COMBINE.lean` sont identiques à ceux de `ENONCES.lean` (texte de la déclaration jusqu'à `:=`, blancs normalisés, commentaires retirés) ; idem pour le corps des définitions `sT`, `Delta`, `Rep`, `HypSpec`, `HypRec` ;
* `COMBINE.lean` commence par les 114 899 octets de `main.lean` publié, octet pour octet ; il AJOUTE 25 446 octets / 499 lignes : un `section / noncomputable section`, le corps de `namespace Reciproque` de `RECIPROQUE_full.lean` recopié tel quel (vérifié), le théorème `Reciproque.reciproque_publie` (qui déduit `HypRec` de `CritereScalaire.doublement_fin_4d` via `hyp_of_specTC`) et des `#print axioms` ;
* aucun `sorry`, `admit`, `axiom`, `native_decide`, `unsafe`, `implemented_by`, `@[extern]`, `opaque`, `extern` hors commentaires, dans les deux fichiers.
Remarque (honnête) sur l'énoncé : `interpolation` et `reciproque_Bstar` supposent `HypSpec` (représentation à tous temps d ≥ 1 et tous côtés ≥ 1, c.-à-d. `HypSpecTC` publié) ; le papier n'utilise que d, côtés ≥ 3. L'hypothèse Lean est plus forte : la formalisation couvre donc un énoncé un peu plus faible que le papier. Dit dans la note.

## 2. Chaîne A : bac à sable du gamer (`qlab_exec.py --kind lean`), Lean 4.34.0, Mathlib 5ed2965
* `RECIPROQUE_full.lean` : rc 0, 0 erreur, pas de sorry, axiomes hors standard : aucun ; job 20261112-070619-0a612c ; durée 12,5 s ; les quatre `#print axioms` et ceux des lemmes : propext, Classical.choice, Quot.sound (lu dans le JSON, `lean_rejeu/sandbox/R_pied.json`).
* `COMBINE.lean` + pied : rc 0, 0 erreur ; job 20261112-070619-f382b1 ; 24,7 s ; `Reciproque.reciproque_publie`, `facile`, `interpolation`, `reciproque_Bstar`, `trou_cubes` : axiomes standard (`sandbox/C_pied.json`).

### 2 bis. Même chaîne (Lean 4.34.0, même Mathlib), second bac à sable sans droits sur l'acemagic (`qlab_exec.py --ou acemagic --coeurs 16 --mem 32`)
`R_pied` : job 20261112-072756-20ad77, rc 0, 0 erreur, 6,7 s, 30 lignes d'axiomes tous standard ; `C_pied` : job 20261112-072756-55f333, rc 0, 0 erreur, 12,5 s, 138 lignes tous standard (`lean_rejeu/ace/*.json`). Machine différente, mêmes versions : sert de contrôle de reproductibilité, pas de chaîne indépendante.

## 3. Chaîne B : machine louée `kvu-1112`, Lean 4.32.0 (commit 8c9756b2) + Mathlib v4.32.0, utilisateur `lean`, dossier neuf `/work/lean_reciproque_1112/` (créé par root puis rendu à `lean`), `lake env lean`, `nice 10`
Les fichiers n'ont PAS été adaptés (mêmes sha256 sur la machine : vérifié, `lean/reciproque/distant/versions_et_empreintes.txt`).
* `Reciproque_full.lean` : compile, RC=0, aucun message d'erreur (deux avertissements de style), quatre axiomes standard ; olean produit.
* `Combine.lean` : compile, RC=0 (≈ 6 min, la machine était chargée par d'autres travaux), axiomes standard.
* Export de la clôture par `lean4export` (sha256 du binaire e57369980b0b…b0), puis **nanoda** (binaire non modifié, sha256 ce46eafff2c4…2c1, axiomes permis : les trois, erreur dure sinon) :
  `Reciproque_full` : 4 déclarations racines, 1 377 205 lignes d'export (sha256 7eebf3b7…b27715), « Checked 16949 declarations with no errors », RC=0, 12,7 s, 123 Mo ;
  `Combine` : 6 racines (`reciproque_publie`, les quatre théorèmes, `CritereScalaire.doublement_fin_4d`), 1 433 069 lignes (sha256 720a7b42…c68), « Checked 17156 declarations with no errors », RC=0.
  Journaux dans `CRITERE_SCALAIRE_v1_2/.../lean/reciproque/distant/{R,C}/`.
Rôles des chaînes : A (bac du gamer, 4.34.0) = compilation de référence et mutants ; 2 bis (bac sans droits de l'acemagic, 4.34.0) = reproduction ; B (machine louée, 4.32.0) = seconde version de Lean + export + noyau indépendant nanoda. `calc_borne` en root (nanoda/comparateur local) : non utilisé, nanoda ayant tourné sur la machine louée.
Écart : nanoda n'a PAS rejoué `main.lean` publié seul ; il a rejoué la clôture de `doublement_fin_4d`, qui est dans l'export de `Combine`.

## 4. Mutants (sur `RECIPROQUE_full.lean`, bac à sable ; `lean/reciproque/mutants/`, `RESULTATS.txt`) : 4/4 ÉCHOUENT
| mutant | résultat |
|---|---|
| M1 : constante 31 → 30 dans l'énoncé de `reciproque_Bstar` | rc 1, 2 erreurs, 1ʳᵉ : ligne 303, `rewrite` ne trouve plus le motif (dans la preuve de `reciproque_Bstar`) |
| M2 : facteur 16 → 8 (fenêtre `8 * n ≤ a`) | rc 1, 2 erreurs, 1ʳᵉ : ligne 316, « Application type mismatch » |
| M3 : positivité `0 ≤ r i` retirée de `Rep` | rc 1, 13 erreurs, 1ʳᵉ : ligne 50 (`sT_nonneg` et lemmes de monotonie) |
| M4 : seuil `1/512` → `1/256` dans l'hypothèse de `reciproque_Bstar` | rc 1, 2 erreurs, 1ʳᵉ : ligne 305, « Application type mismatch » |
Limite : les mutants ont été exécutés sur la chaîne A seule ; la position de l'erreur est dans le théorème visé (M1, M2, M4) ou dans les lemmes qui utilisent la positivité (M3).

## 5. Contrôle du pilote consigné (fait ce matin avant ma mission, d'après la consigne)
La preuve papier (étapes 1 à 4, puis (b), (c), (d)) a été refaite ligne à ligne par le pilote et tient ; constantes revérifiées : 2/31 ; Δ(16n) ≤ 2⁻²⁴ ; γ = 1/(31·2²³T0³) ; y0 = 27/3968 ; avec T0 = 8n on aurait y0 = 54/31 > 1/20 (16 est le premier facteur dyadique que CETTE preuve permet) ; (c) r^m ≤ q^p/248 ; (d) 4608 = 2·48·48 (mon calcul : 576·8), θ = e^{18/31} − 1 ≈ 0,787, 0,2393/n. Les énoncés Lean figés correspondent au théorème papier.
Je les ai aussi refaites (voir `verif_pilote_constantes/` et `RELECTURES.md`).

## 6. Ce que ce certificat NE dit PAS
Pas de vérification que (W2) vaut pour Wilson SU(2) (positivité aux côtés impairs : BB26 Lemme 7.3(vii) affirme T ≥ 0, lu, non revérifié) ; pas de vérification du Théorème F de BB26 ni de (W) (corollaire pont conditionnel) ; (d) et Casimir sur papier seulement ; aucun humain n'a lu les preuves.
