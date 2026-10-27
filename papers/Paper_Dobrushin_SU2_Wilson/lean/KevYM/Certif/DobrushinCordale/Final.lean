import KevYM.Certif.DobrushinCordale.Donnees

/-!
# CH — énoncé final (partie rationnelle)

Pour toutes fonctions réelles `Nt, J0, J1` majorées/minorées boîte par boîte par les bornes Arb exportées,
`max (J0 κ) (J1 κ) < Nt κ` pour tout `κ ∈ [0, 4/3]`. Combiné (hors Lean) à la chaîne Arb et aux preuves
de `RAPPORT_CH.md` (Beckmann, réduction en α, Tchebychev), cela donne `D_ch(κ) = E_κ[x₂²] ≤ 1/4` sur
`[0, 4/3]`, puis le seuil `β < 2/9` via `somme_dobrushin_lt_one` et `kappa_max_lt`.
-/

namespace KevYM.Certif.DobrushinCordale

theorem KC_eq : (KC : ℝ) = 4 / 3 := by
  simp [KC]

theorem certificat_cordal (Nt J0 J1 : ℝ → ℝ)
    (hN : ∀ b ∈ boites, ∀ κ : ℝ, (b.k0 : ℝ) ≤ κ → κ ≤ (b.k1 : ℝ) → (b.lb : ℝ) ≤ Nt κ)
    (hJ0 : ∀ b ∈ boites, ∀ κ : ℝ, (b.k0 : ℝ) ≤ κ → κ ≤ (b.k1 : ℝ) → J0 κ ≤ (b.h0 : ℝ))
    (hJ1 : ∀ b ∈ boites, ∀ κ : ℝ, (b.k0 : ℝ) ≤ κ → κ ≤ (b.k1 : ℝ) → J1 κ ≤ (b.h1 : ℝ))
    (κ : ℝ) (h0 : 0 ≤ κ) (hK : κ ≤ 4 / 3) : max (J0 κ) (J1 κ) < Nt κ :=
  sound boites 0 KC boites_chaine boites_ok Nt J0 J1 hN hJ0 hJ1 κ (by simpa using h0)
    (by rw [KC_eq]; exact hK)

end KevYM.Certif.DobrushinCordale
