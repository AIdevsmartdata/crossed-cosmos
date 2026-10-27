import Mathlib

/-!
# CH (28/09/2026) — Dobrushin W1 à un lien, métrique CORDALE : partie rationnelle

Ce fichier ne contient AUCUNE physique. Il vérifie :

1. `chaine_couvre` : une liste de boîtes `[k0, k1]` chaînées de `a` à `c` couvre tout `κ ∈ [a, c]`.
2. `sound` : si, sur chaque boîte, `lb ≤ Nt κ`, `J0 κ ≤ h0`, `J1 κ ≤ h1` (bornes produites par Arb, voir
   `RAPPORT_CH.md`), et si chaque boîte passe le test rationnel `h0 < lb ∧ h1 < lb`, alors
   `max (J0 κ) (J1 κ) < Nt κ` pour tout `κ ∈ [a, c]`.
3. L'algèbre de la réduction en α et en κ², et l'arithmétique du seuil : `18 · β · (1/4) < 1 ⟺ β < 2/9`,
   l'égalité au bord, `6 · (2/9) = 4/3`, et `π/16 < 2/9`.

Le lien entre `Nt, J0, J1` et la physique (champ de Beckmann, séries en κ, restes de Cauchy) est certifié
par Arb (python-flint), PAS par Lean.
-/

namespace KevYM.Certif.DobrushinCordale

/-- Une boîte `κ ∈ [k0, k1]` avec un minorant `lb` de `Nt` et des majorants `h0, h1` de `J0, J1`. -/
structure Boite where
  k0 : ℚ
  k1 : ℚ
  lb : ℚ
  h0 : ℚ
  h1 : ℚ

/-- Test rationnel d'une boîte. -/
def Boite.ok (b : Boite) : Bool :=
  decide (b.h0 < b.lb) && decide (b.h1 < b.lb) && decide (b.k0 ≤ b.k1)

/-- `chaine L a c` : les boîtes de `L` se suivent, la première commence en `a`, une boîte finit en `c`. -/
def chaine : List Boite → ℚ → ℚ → Bool
  | [], _, _ => false
  | b :: r, a, c => decide (b.k0 = a) && decide (b.k0 ≤ b.k1) && (decide (b.k1 = c) || chaine r b.k1 c)

theorem chaine_couvre : ∀ (L : List Boite) (a c : ℚ), chaine L a c = true →
    ∀ κ : ℝ, (a : ℝ) ≤ κ → κ ≤ (c : ℝ) → ∃ b ∈ L, (b.k0 : ℝ) ≤ κ ∧ κ ≤ (b.k1 : ℝ) := by
  intro L
  induction L with
  | nil => intro a c h; simp [chaine] at h
  | cons b r ih =>
    intro a c h κ ha hc
    simp only [chaine, Bool.and_eq_true, decide_eq_true_eq, Bool.or_eq_true] at h
    obtain ⟨⟨h0, _⟩, h2⟩ := h
    by_cases hk : κ ≤ (b.k1 : ℝ)
    · refine ⟨b, by simp, ?_, hk⟩
      rw [h0]; exact ha
    · rw [not_le] at hk
      rcases h2 with h2 | h2
      · exfalso
        rw [h2] at hk
        linarith
      · obtain ⟨b', hb', h'⟩ := ih b.k1 c h2 κ hk.le hc
        exact ⟨b', by simp [hb'], h'⟩

/-- **Correction du vérificateur.** -/
theorem sound (L : List Boite) (a c : ℚ) (hch : chaine L a c = true) (hok : L.all Boite.ok = true)
    (Nt J0 J1 : ℝ → ℝ)
    (hN : ∀ b ∈ L, ∀ κ : ℝ, (b.k0 : ℝ) ≤ κ → κ ≤ (b.k1 : ℝ) → (b.lb : ℝ) ≤ Nt κ)
    (hJ0 : ∀ b ∈ L, ∀ κ : ℝ, (b.k0 : ℝ) ≤ κ → κ ≤ (b.k1 : ℝ) → J0 κ ≤ (b.h0 : ℝ))
    (hJ1 : ∀ b ∈ L, ∀ κ : ℝ, (b.k0 : ℝ) ≤ κ → κ ≤ (b.k1 : ℝ) → J1 κ ≤ (b.h1 : ℝ))
    (κ : ℝ) (ha : (a : ℝ) ≤ κ) (hc : κ ≤ (c : ℝ)) : max (J0 κ) (J1 κ) < Nt κ := by
  obtain ⟨b, hb, h1, h2⟩ := chaine_couvre L a c hch κ ha hc
  have hbok := List.all_eq_true.mp hok b hb
  simp only [Boite.ok, Bool.and_eq_true, decide_eq_true_eq] at hbok
  obtain ⟨⟨hh0, hh1⟩, _⟩ := hbok
  have e0 : (b.h0 : ℝ) < (b.lb : ℝ) := by exact_mod_cast hh0
  have e1 : (b.h1 : ℝ) < (b.lb : ℝ) := by exact_mod_cast hh1
  have n := hN b hb κ h1 h2
  have j0 := hJ0 b hb κ h1 h2
  have j1 := hJ1 b hb κ h1 h2
  rw [max_lt_iff]
  exact ⟨by linarith, by linarith⟩

/-! ## Algèbre de la réduction (hors Arb) -/

/-- Réduction κ² : si `E₂ − V₁ = κ² Ñ` et `J̃ < Ñ`, alors `V₁ + κ² J̃ ≤ E₂`. -/
theorem etape_kappa2 (k Nt Jt V1 E2 : ℝ) (hE : E2 - V1 = k ^ 2 * Nt) (h : Jt < Nt) :
    V1 + k ^ 2 * Jt ≤ E2 := by
  nlinarith [mul_le_mul_of_nonneg_left h.le (sq_nonneg k)]

/-- Réduction en α : pour `c² + s² = 1`, `Var_κ(u) + c²·J = c²(V₁ + J) + s² E₂ ≤ E₂` dès que `V₁ + J ≤ E₂`. -/
theorem etape_alpha (V1 E2 J c s : ℝ) (hcs : c ^ 2 + s ^ 2 = 1) (h : V1 + J ≤ E2) :
    c ^ 2 * (V1 + J) + s ^ 2 * E2 ≤ E2 := by
  have hs : s ^ 2 = 1 - c ^ 2 := by linarith
  have hneg : c ^ 2 * (V1 + J - E2) ≤ 0 := mul_nonpos_of_nonneg_of_nonpos (sq_nonneg c) (by linarith)
  rw [hs]
  nlinarith [hneg]

/-- Tchebychev (hors Lean : `E_κ[x₁²] ≥ 1/4`) ⟹ `E_κ[x₂²] = (1 − E_κ[x₁²])/3 ≤ 1/4`. -/
theorem Ex2_le_quart (m2 : ℝ) (h : 1 / 4 ≤ m2) : (1 - m2) / 3 ≤ 1 / 4 := by linarith

/-! ## Arithmétique du seuil -/

/-- Somme de Dobrushin cordale à un lien : `18 · β · (1/4) < 1` pour `β < 2/9`. -/
theorem somme_dobrushin_lt_one (β : ℝ) (hβ : β < 2 / 9) : 18 * β * (1 / 4) < 1 := by linarith

/-- Au bord, la somme vaut exactement 1. -/
theorem somme_dobrushin_bord : (18 : ℝ) * (2 / 9) * (1 / 4) = 1 := by norm_num

/-- Réciproque : pour `β ≥ 2/9`, la somme est `≥ 1`. -/
theorem somme_dobrushin_ge_one (β : ℝ) (hβ : 2 / 9 ≤ β) : 1 ≤ 18 * β * (1 / 4) := by linarith

/-- `κ = β|s| ≤ 6β < 4/3` pour `β < 2/9` : le domaine certifié `[0, 4/3]` suffit. -/
theorem kappa_max_lt (β : ℝ) (hβ : β < 2 / 9) : 6 * β < 4 / 3 := by linarith

theorem kappa_max_bord : (6 : ℝ) * (2 / 9) = 4 / 3 := by norm_num

/-- Le seuil cordal 2/9 dépasse le seuil géodésique π/16. -/
theorem pi_div_16_lt : Real.pi / 16 < 2 / 9 := by
  have := Real.pi_lt_d4
  norm_num at this ⊢
  linarith

end KevYM.Certif.DobrushinCordale
