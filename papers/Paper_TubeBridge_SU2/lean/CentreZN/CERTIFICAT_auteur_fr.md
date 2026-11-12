# CentreZN : borne de torsion centrale Z_N, vérifiée par le noyau Lean — certificat du 12/11/2026

**En une phrase.** Seize énoncés de l'espace de noms `CentreZN` (généralisation au centre cyclique Z_N de nos bornes de
retournement de colonne et de rapport de torsion publiées ce matin pour Z_2), figés avant toute preuve, sont prouvés par
GPT-6.1 Sol et acceptés par le noyau de Lean 4.32.0 (Mathlib v4.32.0) et par le noyau indépendant nanoda, avec les trois
axiomes standard seulement. Statut : VÉRIFIÉ PAR LE NOYAU (une seule chaîne Lean ; pas encore rebâti par un non-auteur).

## Énoncés (français), espace de noms `CentreZN`
Notations : N ≥ 1, ζ ∈ ℂ avec ζ^N = 1 ; pour j ∈ Z/NZ, ζ^j := ζ^{j.val} ; pour t ∈ ℂ, f_j(t) = exp(Re(ζ^j t)),
S(t) = Σ_j f_j(t), A_q(t) = Σ_j ζ^{qj} f_j(t). Hypothèse (H_ρ) : |A_q(t)| ≤ ρ S(t) pour tout |t| ≤ κ.

**Partie A (forme abstraite).**
* `centre_flip_bound` (A1). (Ω, μ) probabilité ; des transformations τ_s qui préservent μ ; une application « charges »
  s ↦ chg(s) ∈ (Z/N)^P SURJECTIVE ; des couplages complexes mesurables T_p, |T_p| ≤ κ, T_p∘τ_s = ζ^{chg(s)_p} T_p ; un poids
  R ≥ 0 mesurable invariant avec R·exp(Σ_p Re T_p) intégrable ; une observable W complexe mesurable, |W| ≤ 1,
  W∘τ_s = ζ^{q·Σ_{p∈A} chg(s)_p} W ; ρ vérifiant (H_ρ). Alors |∫ W R e^{Σ Re T}| ≤ ρ^{|A|} ∫ R e^{Σ Re T}.
* `twist_ratio_bound` (A2). Mêmes données sans W ni A ; toute affectation de charges de somme nulle est réalisée ;
  Z_k = ∫ R exp(Σ_p Re(ε_{k,p} T_p)), ε_{k,p} = ζ^k si p = p₀, 1 sinon. Alors |Σ_k ζ^{qk} Z_k| ≤ ρ^{|P|} Σ_k Z_k.
* `rho_crude` (A3). ζ racine primitive N-ième, q ≢ 0 : |A_q(t)| ≤ (1 − e^{−2|t|}) S(t).
* `rho_two` (A4). N = 2, ζ = −1, q = 1 : |A_1(t)| ≤ tanh|t| · S(t).
* `sharp_one_plaquette` (A5). Sur Z/N avec la mesure uniforme, les translations préservent la mesure, T(j) = ζ^j t et
  W(j) = ζ^{qj} ont les covariances de A1 (une plaquette), |T| = |t|, |W| = 1, et ∫ W e^{Re T} = A_q(t)/N,
  ∫ e^{Re T} = S(t)/N : A1 est une égalité pour ρ = |A_q(t)|/S(t). La constante optimale de A1 est donc
  ρ_{N,q}(κ) = sup_{|t|≤κ} |A_q(t)|/S(t).
* `centre_flip_bound_crude`, `twist_ratio_bound_crude` (A6). A1, A2 avec la constante 1 − e^{−2κ} (ζ primitive, q ≢ 0).
* `recover_column_flip_bound`, `recover_twist_ratio_bound` (A7). Les énoncés publiés L01 (`TubeArea.column_flip_bound`) et
  L14 (`TubeArea.twist_ratio_bound`), texte identique à leur réénoncé du pied d'hier, DÉDUITS de A1, A2 et A4 (N = 2).

**Partie B (type Wilson).** Groupe G mesurable à mesure de probabilité invariante à gauche, z central avec z^N = 1,
χ : G → ℂ mesurable, |χ| ≤ 1, χ(zg) = ζχ(g) ; liens longs (e, y) (arête de base, site de fibre) et autres liens ; torsion
de colonne σ : E → Z/N (lien (e,y) multiplié à gauche par z^{σ(e)}) ; charge d'un mot = somme signée (orientation, avec
multiplicité) des σ de ses lettres longues.
* `mixed_word_neutral` (B0). Une plaquette mixte (lien long en y, autre lien, même colonne en y' à l'envers, autre lien à
  l'envers) est neutre pour tout N.
* `wilson_centre_flip_bound` (B1). Couplages T_p = β Σ_y c_{p,y} χ(holonomie de p en y), |c| ≤ 1, β ≥ 0 ; observable ψ de
  N-alité q sur la boucle w_C au site y₀ ; Stokes sur les charges et surjectivité des charges de plaquettes en hypothèses :
  |∫ ψ(hol_C) R e^{Σ Re T}| ≤ ρ^{|A|} ∫ R e^{Σ Re T}, pour ρ vérifiant (H_ρ) à κ = β|F|.
* `torus_charge_explicit`, `torus_charge_sum`, `torus_charge_image` (B2). Sur le tore discret (Z/m)×(Z/n) : charge d'une
  plaquette = rotationnel discret ; somme des charges nulle ; si m, n ≥ 2, toute affectation de somme nulle est réalisée.
* `wilson_twist_ratio_torus` (B3) et `_crude`. Action de type Wilson complète sur (tore m × n) × (fibre F) avec termes neutres
  à coefficients complexes ; Z_k = poids des plaquettes de base p₀ multipliés par ζ^k à tout site de fibre :
  |Σ_k ζ^{qk} Z_k| ≤ ρ^{mn} Σ_k Z_k, et ≤ (1 − e^{−2β|F|})^{mn} Σ_k Z_k (ζ primitive, q ≢ 0).

## Qui a fait quoi
* **Pilote (Claude Opus 5.5)** : dérivation et preuve sur papier (`PREUVE_PAPIER.md`) ; énoncés et définitions de la partie B
  écrits et FIGÉS avant toute preuve (`ENONCES_GELES.lean`, sha256 17f5a911…b863, contrôlé par `SHA256_ENONCES.txt`) ;
  élaboration des énoncés vérifiée avec `sorry` sur la machine louée (16 « declaration uses sorry », code 0) ; pieds de
  vérification fabriqués mécaniquement à partir des énoncés figés (`outils/faire_pied.py`) ; boucle, compilations, contrôles,
  nanoda. Le pilote n'a écrit aucune preuve Lean.
* **GPT-6.1 Sol** (`codex exec -m gpt-6.1-sol -s read-only`) : toutes les preuves Lean (A : 991 lignes ; B : 626 lignes),
  sans pouvoir compiler ni écrire de fichier : il rendait le fichier complet dans sa réponse, le harnais l'extrayait. Les
  consignes (`leanA/CONSIGNE_SOL.txt`, `leanB/CONSIGNE_SOL.txt`) portaient en fin les règles des modèles externes et la palette.
* **DeepSeek V4 Pro** (sans outils) : relecture adverse de la preuve sur papier (`relecture/relecture_papier_ds_1.md` :
  « no fatal errors », une remarque de rédaction corrigée) ; retraduction à l'aveugle des énoncés sans commentaires
  (`retraduction/retraduction_ds_1.md`, comparaison `retraduction/BILAN_PILOTE.md` : aucun écart, aucune correction avant
  Sol) ; seconde relecture adverse (§5 bis, représentation de Bessel, conjecture de la constante optimale) avec la palette :
  voir `relecture/relecture_papier_ds_2.md`. Écart de procédure : la première relecture (05h50) a été lancée SANS la palette
  (règle de CLAUDE.md : champ `"palette": true` pour DeepSeek) ; la seconde la porte. La retraduction (vérification
  mécanique) est hors du champ de la règle.

## Méthode (celle d'hier, adaptée)
* Base figée + fichier de Sol + pied : la machine louée compile `GELE ++ FICHIER ++ PIED`. Le pied (`leanA_protege/PIED_A.lean`,
  `leanB_protege/PIED_B.lean`) RÉÉNONCE chacun des seize théorèmes dans l'espace de noms `CentreZNVerif` (texte copié des
  énoncés figés) et l'obtient par application directe du théorème de Sol à tous ses arguments explicites ; puis
  `#print axioms` sur les 16 réénoncés et les 16 originaux (32 lignes attendues).
* Les définitions de la partie B (`Config`, `configMeasure`, `columnTwist`, `orientedLink`, `Word`, `holonomy`, `charge`,
  `Neutral`, `baseWord`, `baseCharge`, `coupling`, `termsWeight`, `TorusEdge`, `torusWord`) sont dans la base figée
  (`leanB_protege/DEFS_B.lean`, sha256 137e9dec…98d8) : Sol ne pouvait pas les modifier.
* Les deux boucles ont tourné en parallèle : la partie B a été prouvée sur une base où les énoncés de A étaient encore en
  `sorry` (le `sorryAx` hérité n'était toléré que dans cette boucle) ; l'assemblage final a tout recompilé ensemble avec les
  preuves de A, sans aucun `sorry`.

## Tours de boucle
| partie | tour | heure | résultat |
|---|---|---|---|
| A (9 théorèmes) | 1 | 06:20 | code 1, 17 erreurs (instances, buts non résolus, réécritures) |
| A | 2 | 06:29 | code 0, 0 erreur, 18/18 lignes d'axiomes standard : SUCCÈS (`leanA/CentreZN_A_PROUVE_tour2.lean`, sha256 e725fe1c…0d89) |
| B (7 théorèmes) | 1 | 06:17 | code 1, 1 erreur (une réécriture dont le motif |exp a · exp b| n'apparaissait pas dans le but) |
| B | 2 | 06:23 | code 0, 0 erreur : SUCCÈS (`leanB/CentreZN_B_PROUVE_tour2.lean`, sha256 8093df18…917c) |
Aucun énoncé n'a été jugé faux ou improuvable ; aucun énoncé n'a été refigé.

## Contrôles (machine louée kvu-1112, 12/11/2026 ; journaux dans `certificat/final1/`)
| contrôle | résultat |
|---|---|
| fichier complet `certificat/final1/CentreZNComplet.lean` (1 990 lignes : base A + preuve A + définitions B + preuve B + pieds A et B), sha256 d69ca94a…15e6 | — |
| Lean 4.32.0 (commit 8c9756b2), Mathlib v4.32.0 (81a5d257c8e4, celle du projet d'OpenAI sur la location), `lake env lean`, nice 10 | code 0, 0 erreur ; 2 avertissements de style (`hpar` non utilisé dans `recover_twist_ratio_bound`, argument `simp` inutile) |
| axiomes (`outils/lire_axiomes.py`, qui recolle les messages coupés) | 32 lignes ; 30 = [propext, Classical.choice, Quot.sound], 2 = [propext, Quot.sound] (`mixed_word_neutral` et son réénoncé) ; aucun autre axiome |
| compilation en module (`lean -R … -o CentreZNComplet.olean`) | code 0 |
| export de la clôture (lean4export, sha256 du binaire e5736998…66b0) des 32 déclarations | code 0 ; 3 394 846 lignes ; sha256 34a02898…d395 (copie compressée `certificat/final1/nanoda/zn.ndjson.gz`, sha256 9bf1bc32…3700) |
| noyau indépendant nanoda (binaire non modifié de la location, sha256 ce46eaff…d2c1), axiomes permis : les trois, erreur dure sinon | « Checked 35170 declarations with no errors », code 0 ; 4,3 s, 245 Mo |
| énoncés prouvés contre énoncés figés (`outils/comparer_enonces.py`) | les 16 textes d'énoncé identiques au caractère près ; et les 16 réénoncés du pied passent |
| mots interdits (`sorry`, `admit`, `axiom`, `native_decide`, `unsafe`, `implemented_by`, `set_option`, `#…`, `import`, notations, instances, attributs au niveau du fichier) dans les deux fichiers de Sol | aucun |
| bases et pieds non modifiés pendant les boucles | sha256 vérifiés (`sha256sum -c SHA256_ENONCES.txt` : tous OK) |
| les deux énoncés « retour au cas N = 2 » (A7) sont DÉDUITS des théorèmes Z_N | oui (lecture du fichier : `recover_column_flip_bound` applique `centre_flip_bound 2 (-1)` et `rho_two` ; `recover_twist_ratio_bound` applique `twist_ratio_bound 2 (-1)` et `rho_two`) |
| mémoire et disque de la location avant chaque compilation | ≥ 300 Go disponibles, ≈ 127 Gio libres (seuils 25 Go et 90 Gio) |
Non fait : recompilation sous Lean 4.32.2 (cette location ne porte que 4.32.0) ; reconstruction par un non-auteur ; lecture
ligne à ligne des preuves de Sol par le pilote (seulement leur structure et l'usage des théorèmes A dans A7, B1, B3).

## Ce que ces théorèmes sont
* Une généralisation EXACTE, en volume fini et à tout couplage, de nos énoncés Z_2 : pour un centre cyclique d'ordre N, la
  moyenne de Fourier sur les torsions de colonnes remplace la moyenne des signes, et le facteur par plaquette est le rapport de
  Fourier d'une plaquette r_{N,q}(t) = |A_q(t)|/S(t), au lieu de tanh. Pour N = 2 on retrouve exactement L01 et L14 (A7, en Lean).
* Une constante prouvée, grossière : 1 − e^{−2κ} (A3) ; la constante optimale de la forme abstraite est exactement
  ρ_{N,q}(κ) = sup_{|t|≤κ} r_{N,q}(t) (A1 + A5) ; sa forme close r_{N,q}(κ) (valeur en t = κ réel) est PROUVÉE SUR PAPIER pour N = 2 (tanh κ) et N = 4
  (tanh(κ/2), tanh²(κ/2)), et reste une CONJECTURE pour les autres N (calcul : N ≤ 8, écart ≤ 5·10⁻¹⁶). Seule la constante
  grossière et le cas N = 2 sont en Lean.
* Dans le langage de Kanazawa (arXiv:0808.3442) : une borne explicite des projecteurs de flux électrique,
  ⟨F^{[q]}⟩ ≤ ρ_{N,q}(βL_⊥)^{L_µL_ν} ⟨F^{[0]}⟩ (sur papier pour le réseau 4D ; en Lean pour (tore) × (fibre abstraite)).

## Ce que ces théorèmes ne sont pas
* Rien sur le trou de masse, rien d'uniforme : ρ_{N,q}(βl²)^{l²} → 1 quand l grandit à β fixé (section transverse l²).
* Rien sur le secteur neutre (q ≡ 0) ; rien en volume infini ni dans la limite continue.
* Le corollaire SU(N) sur le réseau périodique 4D n'est PAS formalisé : le développement d'OpenAI ne fournit que `su2`
  (`YangMills.GaugeGroup` est général, mais aucun SU(N) concret pour N > 2 n'y est défini) ; aucun pont n'a été écrit, et rien
  n'a été inventé. d'après le certificat d'hier, les instances (compacité, structure borélienne) qui donneraient une mesure de Haar sur SU(N) ne sont pas prêtes dans Mathlib v4.32.0 (non revérifié aujourd'hui) ; les énoncés B supposent une mesure de
  probabilité invariante à gauche quelconque.
* L'outil (torsion par le centre), les quantités (fonctions de partition tordues, projecteurs de flux) et la borne « boucle ≤
  flux » sont classiques (`ANTERIORITE.md`) ; ce qui peut rester à nous est la borne explicite élémentaire et sa vérification.
