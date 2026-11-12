# Certificat Lean, partie B (lean_L), 12/11/2026 11h04, rien de public

- Lean 4.34.0 + Mathlib (même projet `/srv/qlab/lean` dans les deux bacs). Compilation par `qlab_exec.py --kind lean` : bac du sandbox1 (`sorties/B_preuves_sandbox1.json`) et bac de l'sandbox2, 8 cœurs (`sorties/B_preuves_sandbox2.json`) : rc 0, 0 erreur, pas de sorry, `lean.axioms_hors_standard` vide.
- Énoncés gelés : `Enonces.lean`, sha256 06c735775d3a0f56b9450987f4ffa7f64c2f0fa4d508e4a2bb61039dd9983353, gel 2026-11-12 10:57:40 CET, version 1, jamais modifiée (voir `ENONCES_GELES.md`). Compilé avec sorry : rc 0, 0 erreur.
- Preuves : `Preuves.lean`, sha256 07ee1c56d40ffa8167bd8c22aca1b106278dc1df40860cd038f4a135d4691b8a. Contrôle : extraction des 15 énoncés (de `theorem` à `:= by`) dans les deux fichiers puis diff : identiques (40 lignes chacun). Lemmes ajoutés : préfixe `aux_` seulement.
- Axiomes de chacun des 15 théorèmes : propext, Classical.choice, Quot.sound (sauf c1_int : propext ; c2_nat, c2_int : propext, Quot.sound ; a4_unites_commutatif : propext), tous dans la liste autorisée.

## Prouvé (15 théorèmes, `namespace VerrouL`)
| théorème | contenu |
|---|---|
| `a1_anticommute` | SU(2) matrices : UV = −VU ⇒ tr U = tr V = 0, U² = V² = −1 (n'utilise que det = 1) |
| `a2_commutant` | W ∈ SU(2) commute avec U et V (anticommutants) ⇒ W = 1 ou W = −1 |
| `a3_existence` | iσ₁ = !![0,I;I,0] et iσ₂ = !![0,1;−1,0] sont dans SU(2) et anticommutent |
| `a4_unites_commutatif` | anneau commutatif non trivial, 2 inversible : deux unités n'anticommutent pas |
| `a4_integre` | anneau intègre, 2 ≠ 0 : deux éléments non nuls n'anticommutent pas |
| `a4_cercle_et_Z2` | idem pour Circle (U(1)) et ℤˣ (ℤ₂) |
| `a5_mutant_commuter_avec_U_seul` | U, V anticommutants, W = U commute avec U et n'est pas ±1 |
| `b1_cube` | Δ ≥ 8 log(8/(5+3R)) (les hypothèses 0 ≤ R ≤ 1 sont déclarées mais inutilisées par la preuve : R > −5/3 suffirait) |
| `b2_sept_rapports`, `b2_log4` | −log(1−D) ≥ log(8/(1+7r)) ; ≥ log 4 si r ≤ 1/7 |
| `b3_poids` | 8+4+2+1 = 15, Σ_{j<4} 2^{3−j} = 15, 15 log 8 = 45 log 2 |
| `c1_nat`, `c1_int`, `c2_nat`, `c2_int` | comptages de dimension (ℕ avec hypothèses V ≥ 1, d ≥ 2 ; ℤ sans) |

Les quaternions unitaires n'ont pas été utilisés : (a) est prouvé directement sur `Matrix.specialUnitaryGroup (Fin 2) ℂ`. Preuve de (a2) : calcul en coordonnées, fermé par `grind` (anneau de polynômes) ; la preuve n'utilise ni l'unitarité ni le produit scalaire : seulement det = 1 (valable sur SL₂(ℂ)).

## Non formalisé
- Toute la partie analytique du Théorème L : Lemme A (orbites de jauge, dimension des zéros), Lemme B (Morse–Bott), Lemme C (Laplace, exposants), Lemme D (U(1), ℤ₂ par Cauchy–Schwarz) : restent sur papier.
- Le lien entre le fait algébrique et les configurations de réseau (jauge du tore découpé, transitivité de SO(3) sur les couples orthonormés), l'identification D_j → 7/8 pour les tores σ_j × n, (W1)–(W2)–(C), T3(b) : non formalisés ; (b) formalise seulement l'algèbre réelle à partir de D ≥ (3/8)(1−R) et de l'inégalité de départ.
- Aucun second noyau (nanoda) lancé ; pas de vérification des versions 4.32.x.
