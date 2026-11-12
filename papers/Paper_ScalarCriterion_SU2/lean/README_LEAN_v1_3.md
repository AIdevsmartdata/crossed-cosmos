# Lean files added in version 1.3 (12 November 2026)

Two groups of abstract, finite statements. They check small algebraic pieces of Sections 7 and 8 of the note and **nothing analytic**. No file of versions 1.0 to 1.2 is changed (`CritereScalaire.lean`, `main.lean`, `Reciproque.lean`, `main_v1_2.lean` are byte for byte those of version 1.2).

## `thooft_critere/` (7 statements, namespace `CritereThooft`)
`ENONCES.lean` (statements with `sorry`, frozen before any proof, sha256 `7dd1a95c1e46d900b9ab4cd100627a0e50a8d66596f8a27a52c22ca95dc1730f`), `PREUVES.lean` (sha256 `58a549d7b6bab4915fee9bc40cc7d858ecb1541eb54b9c161fbbae4d93f7e5e1`). Data: a **finite** family `r_i >= 0`, a vacuum index `i0` with `r_i0 = 1`, a label `e_i` in `Z_2^3`, `Z_k(M) = sum_i (-1)^{k.e_i} r_i^M`.

| declaration | formalised | NOT formalised / difference from the text |
|---|---|---|
| `chi_somme` | sum over k of the character = 8 if e = 0, else 0 | -- |
| `trace_neutre` | sum_k Z_k = 8 Tr_0 | finite spectrum instead of a trace-class operator |
| `defaut_torsion` | if the vacuum is in the sector 0 and r_i >= 0: 0 <= 1 - Z_k/Z_0 <= 2 s(M) | **coarse form only**: not min(2D,1), not 2 s^fl/(1+s); positivity Z_k >= 0 not used |
| `decomposition` | log Z_0 = log(1+s^0) + log(8 Z_0 / sum_k Z_k) | finite spectrum |
| `vide_neutre` | G_k >= 0 for all k and sum g >= 1 imply g_0 >= 1 | **combinatorial core only**: the G_k are hypotheses; the limit M -> infinity for a trace-class operator is not formalised |
| `propagation` | r_i^n <= q (i != i0), s(m) <= A imply 1 - Z_k/Z_0 <= 2 A q^l at time m + n l | last step of Theorem 7.3(a) only (q = 256 Delta and A = q^p/248 are not in the statement) |
| `deux_sous_verrous` | D_j <= 7 e1/8, s^0_j <= e2, e1 <= 1/8 and Delta <= 2 sum_j 2^{3-j}(log(1+s^0_j) - log(1-D_j)) imply Delta <= 30 (e1+e2) | **last link only**: the bracket (Proposition 6.1) and D_j <= 7 e1/8 are hypotheses; the conclusion is the coarse 30(e1+e2), weaker than the fine form of Theorem 7.5(a) |

## `verrou_L/` (15 statements, namespace `VerrouL`)
`Enonces.lean` (frozen, sha256 `06c735775d3a0f56b9450987f4ffa7f64c2f0fa4d508e4a2bb61039dd9983353`), `Preuves.lean` (sha256 `07ee1c56d40ffa8167bd8c22aca1b106278dc1df40860cd038f4a135d4691b8a`).

* `a1_anticommute`, `a2_commutant`, `a3_existence`, `a5_mutant_commuter_avec_U_seul`: the algebraic fact on `Matrix.specialUnitaryGroup (Fin 2) Complex` (anticommuting U, V: traces 0 and squares -1; the commutant of such a pair is {+1, -1}; an explicit pair; commuting with U alone does not suffice).
* `a4_unites_commutatif`, `a4_integre`, `a4_cercle_et_Z2`: anticommutation is impossible for the abelian cases (commutative ring with 2 invertible; integral domain with 2 != 0; `Circle` and the units of Z).
* `b1_cube`, `b2_sept_rapports`, `b2_log4`, `b3_poids`: the real algebra of Corollary 8.7, **from the inequalities taken as hypotheses** (`b1_cube` declares hypotheses on R that are not all used).
* `c1_*`, `c2_*`: the dimension counts as natural-number / integer arithmetic.

**Not formalised:** the whole analytic part of Theorem 8.1 (zero sets and gauge orbits, Morse-Bott, Laplace exponents, the U(1) and Z_2 bounds); the link between the algebraic fact and lattice configurations (cut gauge, transitivity of SO(3) on orthonormal pairs); D_j -> 7/8 on the tori sigma_j x n; (W1), (W2), (C); the bracket of Proposition 6.1.

## Replays
* Lean 4.34.0 + Mathlib; both proof files compiled with return code 0, 0 errors, no `sorry`, no axiom outside `propext`, `Classical.choice`, `Quot.sound` (a subset of these for some declarations of the second file), in two sandboxes: `sorties_rejeu_v1_3/` (12 November 2026, 11h17-11h18 CET, by the preparer of version 1.3), and, for the earlier runs by the authors of the files, `thooft_critere/sorties/`, `verrou_L/sorties/`.
* Statements vs proofs: `../calculs/comparer_enonces.py` extracts every `theorem ... := by` statement of the frozen file and of the proof file and compares them (7 = 7 and 15 = 15 identical).
* Mutants: four for the first file (`thooft_critere/mutants/`, each fails to compile); for the first file a replayer proved the negation of twelve mutated statements by explicit counter-examples (`verrou_L/MutantsA.lean`, `verrou_L/REJEU_ANGLE_A.md`); **no mutation campaign for the second file** beyond its own abelian cases `a4`, `a5`.
* **Not done:** independent second kernel (nanoda), build on Lean 4.32.x, rebuild from a git archive, rebuild by a human.
