# Rejeu de l'angle A par un non-auteur (12/11/2026, 11h04, rien de public)

Source : `chantiers/critere_thooft_2026-11-12/lean/PREUVES.lean` (sha256 58a549d7…, copié dans `A_copie/`, source non modifiée), prose : `THEOREMES.md`
§3, §4, §7. Rejoueur : agent Sonnet 5.5, non auteur. Lean 4.34.0 + Mathlib. Sorties : `sorties/A_preuves_{sandbox1,sandbox2}.json`, `sorties/A_mutants_{sandbox1,sandbox2}.json`.
Les deux bacs : rc 0, 0 erreur, pas de sorry, `#print axioms` = propext, Classical.choice, Quot.sound pour les sept (et pour les lemmes `aux_*`).
Les mutants sont dans `MutantsA.lean` : chaque mutant est un énoncé MUTÉ dont on PROUVE LA NÉGATION par un contre-exemple chiffré
(famille à deux états r = (1, 1/2), étiquettes (0, e₁), etc.) ; compile rc 0 dans les deux bacs. Un mutant « rouge » veut dire : l'énoncé muté est faux, donc aucune preuve ne peut passer.
Non-vacuité : `nv_spectre`, `nv_vide_neutre`, `nv_deux_sous_verrous` exhibent des instances où toutes les hypothèses sont vraies ; les hypothèses
ne sont donc pas contradictoires (on ne peut pas dériver False d'elles) ; de plus les contre-exemples des mutants (hl, hr0, hq tenus sauf le muté) vérifient les hypothèses restantes.

| énoncé | fichier | compile sandbox1 / sandbox2 | axiomes | fidélité à la prose | mutants (négation prouvée) |
|---|---|---|---|---|---|
| `chi_somme` (T1a) | PREUVES.lean | rc 0 / rc 0 | standard | oui : Σ_k χ_k(e) = 8 si e = 0, 0 sinon | 8 → 7 : faux (e = 0 donne 8) |
| `trace_neutre` (T1a) | idem | rc 0 / rc 0 | standard | oui : Σ_k Z_k = 8 Tr₀ (finie, abstraite) | 8 → 4 : faux (Tr₀ = 1, somme = 8 à M = 0) |
| `defaut_torsion` (T1b,e) | idem | rc 0 / rc 0 | standard | écart de force seulement : prose (b) donne aussi ≤ min(2D, 1) et (e) la forme fine 2 s^flux/(1+s) ; Lean prouve la forme grossière 0 ≤ 1 − Z_k/Z₀ ≤ 2 s(M) (celle que T2 utilise). Positivité Z_k ≥ 0 (pour le « 1 ») non formalisée | sans `hl` : faux (r = (1, 1/2), tout en e₁ : 2 ≤ 1) ; sans `hr0` : faux (r = (1, −1)) ; 2 s → s : faux (2/3 ≤ 1/2) |
| `decomposition` (T1d) | idem | rc 0 / rc 0 | standard | oui : log Z₀ = log(1+s⁰) + log(8Z₀/Σ_k Z_k), s⁰ = Tr₀ − 1 | sans `hl` : faux (Tr₀ = 0, les log 0 valent 0 en Lean : log 2 ≠ 0) |
| `vide_neutre` (T1c cœur) | idem | rc 0 / rc 0 | standard | cœur combinatoire seulement, comme annoncé : les G_k sont pris en hypothèse (le passage à la limite M → ∞ avec trace finie n'est pas formalisé) | sans `hk` : faux (g = indicatrice de e₁) ; 1 → 2 : faux (g = indicatrice de 0) |
| `propagation` (T2 étape finale) | idem | rc 0 / rc 0 | standard | oui pour l'étape finale, forme générale (q, A quelconques, r^n ≤ q) ; les valeurs q = 256Δ, A = q^p/248 ne sont pas dans l'énoncé | sans `hq` : faux (ι = point, q = −1, l = 1) ; 2Aq^l → Aq^l : faux (2/3 ≤ 1/2) |
| `deux_sous_verrous` (T3a) | idem | rc 0 / rc 0 | standard | oui, avec l'encadrement publié pris en hypothèse `hΔ` (dit dans la prose et le certificat) ; conclusion = dernier maillon 30(ε₁+ε₂), plus faible que le maillon fin 30[ε₂ + (7ε₁/8)/(1−7ε₁/8)] ; D_j ≤ 7ε₁/8 pris en hypothèse (T1b) | 30 → 29 : faux (e₁ = 0, ε₂ = 0,01, Δ = 30 log 1,01) ; sans `e1 ≤ 1/8` : faux (e₁ = 1, D = 7/8, Δ = 30 log 8 > 30) |

Verdict : 7/7 compilent dans les deux bacs avec axiomes standard ; aucune hypothèse en trop ni contradictoire ; seules différences avec la prose : `defaut_torsion` (forme grossière
seulement) et `deux_sous_verrous` (dernier maillon seulement), plus les restrictions déjà déclarées (spectre fini, cœur combinatoire de T1c, encadrement en hypothèse). Les 12 mutants sont réfutés.
Remarque : un premier lancement de MutantsA sur le bac du sandbox1 a fini en rc 139 (segfault) sans erreur Lean, non reproduit aux trois relances ; à signaler comme aléa du bac, pas du fichier.
Limite : fidélité jugée par lecture de la prose, non par un second noyau (nanoda non lancé) ; l'identification Z_k = Tr(C^k K^M) n'est pas dans ces énoncés.
