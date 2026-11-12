# Certificat Lean — critere_thooft (12/11/2026, rien de public)

- Énoncés figés AVANT toute preuve : `ENONCES.lean`, sha256 7dd1a95c1e46d900b9ab4cd100627a0e50a8d66596f8a27a52c22ca95dc1730f
  (compilé avec `sorry` à 08h11 : 0 erreur, les sept énoncés s'élaborent).
- Preuves : `PREUVES.lean`, sha256 58a549d7b6bab4915fee9bc40cc7d858ecb1541eb54b9c161fbbae4d93f7e5e1. Contrôle mécanique : les
  énoncés et définitions (hors lemmes `aux_*`) sont identiques à ceux de `ENONCES.lean` (comparaison de texte normalisé).
- Compilation : bac de l'sandbox2 (`qlab_exec.py --ou sandbox2 --kind lean`), Lean v4.34.0 (`/srv/qlab/.elan/toolchains/
  leanprover--lean4---v4.34.0`) + Mathlib du projet `/srv/qlab/lean`, travail 20261112-081444-13ce85 : rc 0, 0 erreur,
  aucun `sorry` (le seul mot « sorry » du fichier est dans le commentaire d'en-tête), `#print axioms` : propext,
  Classical.choice, Quot.sound pour les sept théorèmes.
- Mutants (doivent échouer, ont échoué, rc 1) : M1 `defaut_torsion` sans « le vide est dans e = 0 » ; M2 constante 30 → 29 dans
  `deux_sous_verrous` ; M3 facteur 8 → 7 dans `trace_neutre` ; M4 `vide_neutre` sans la positivité des G_k.
- Non fait : reconstruction par un non-auteur ; second noyau (nanoda) ; chaîne 4.32.x.

## Ce qui est formalisé (forme abstraite FINIE)
| déclaration | contenu | papier |
|---|---|---|
| `chi_somme` | Σ_k χ_k(e) = 8 si e = 0, 0 sinon (caractères de ℤ₂³) | T1(a) |
| `trace_neutre` | Σ_k Z_k = 8 Tr₀ | T1(a) |
| `defaut_torsion` | 0 ≤ 1 − Z_k/Z₀ ≤ 2 s(M) si le vide (r = 1) est dans e = 0 | T1(b),(e) |
| `decomposition` | log Z₀ = log(1 + s⁰) + log(8Z₀/Σ_k Z_k) | T1(d) |
| `vide_neutre` | G_k ≥ 0 ∀k et Σ g ≥ 1 ⇒ g₀ ≥ 1 (cœur combinatoire du lemme du vide) | T1(c) |
| `propagation` | r^n ≤ q pour les excités et s(m) ≤ A ⇒ 1 − Z_k/Z₀ ≤ 2A q^l au temps m + nl | T2, étape finale |
| `deux_sous_verrous` | Δ ≤ 2Σ 2^{3−j}(log(1+s⁰_j) − log(1−D_j)), D_j ≤ 7ε₁/8, s⁰_j ≤ ε₂, ε₁ ≤ 1/8 ⇒ Δ ≤ 30(ε₁+ε₂) | T3(a) |

## Ce qui n'est PAS formalisé
Le passage des opérateurs à trace (spectre infini) au spectre fini ; le passage à la limite M → ∞ de T1(c) (seul le cœur
combinatoire est formalisé) ; l'identification Z_k = Tr(C^k K^M) pour Wilson SU(2) (§2) ; l'application du Théorème R (déjà
formalisé dans `reciproque_critere_2026-11-12/lean/`, non relié ici) ; T2(b),(c), T4, T5 ; l'encadrement publié (pris comme
hypothèse hΔ de `deux_sous_verrous`).
