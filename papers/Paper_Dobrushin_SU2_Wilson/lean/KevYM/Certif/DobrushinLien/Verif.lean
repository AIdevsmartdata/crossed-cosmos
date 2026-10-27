import Mathlib

/-!
# C2 (27/09/2026) — Dobrushin W1 à un lien : l'inégalité finale sur des rationnels

Ce fichier ne contient AUCUNE physique. Il vérifie :

1. `sound` : un vérificateur `bP` de négativité d'un polynôme `Σ_j e_j w^j` sur `w ∈ [a, b]`, `a ≥ 0`,
   quand on ne connaît des coefficients (réels) `e_j` que des bornes supérieures rationnelles `c_j`
   (bornes produites par Arb, voir `RAPPORT_C2.md`) : `Σ_j max (c_j a^j) (c_j b^j) < 0 ⟹ Σ_j e_j w^j < 0`.
2. L'arithmétique du seuil : `18·β·(8/(9π)) < 1 ⟺ β < π/16`, l'égalité au bord, et `6·(π/16) < 59/50`.

Le lien entre les `e_j` et les intégrales de la physique (série de perturbation, Gauss–Legendre, restes)
est certifié par Arb (python-flint), PAS par Lean.
-/

namespace KevYM.Certif.DobrushinLien

/-- `bP cs k a b = Σ_j max (c_j a^(k+j)) (c_j b^(k+j))` (rationnels exacts, calculable par le noyau). -/
def bP : List ℚ → ℕ → ℚ → ℚ → ℚ
  | [], _, _, _ => 0
  | c :: cs, k, a, b => max (c * a ^ k) (c * b ^ k) + bP cs (k + 1) a b

/-- `pR es k w = Σ_j e_j w^(k+j)` (réels). -/
noncomputable def pR : List ℝ → ℕ → ℝ → ℝ
  | [], _, _ => 0
  | e :: es, k, w => e * w ^ k + pR es (k + 1) w

lemma term_le (c : ℚ) (e w : ℝ) (a b : ℚ) (k : ℕ) (ha : 0 ≤ (a : ℝ)) (haw : (a : ℝ) ≤ w)
    (hwb : w ≤ b) (he : e ≤ c) :
    e * w ^ k ≤ ((max (c * a ^ k) (c * b ^ k) : ℚ) : ℝ) := by
  have hw0 : 0 ≤ w := le_trans ha haw
  have hwk : 0 ≤ w ^ k := pow_nonneg hw0 k
  have h1 : e * w ^ k ≤ (c : ℝ) * w ^ k := mul_le_mul_of_nonneg_right he hwk
  push_cast
  rcases le_total 0 (c : ℝ) with hc | hc
  · have h2 : (c : ℝ) * w ^ k ≤ (c : ℝ) * (b : ℝ) ^ k :=
      mul_le_mul_of_nonneg_left (pow_le_pow_left₀ hw0 hwb k) hc
    exact le_trans h1 (le_trans h2 (le_max_right _ _))
  · have h2 : (c : ℝ) * w ^ k ≤ (c : ℝ) * (a : ℝ) ^ k :=
      mul_le_mul_of_nonpos_left (pow_le_pow_left₀ ha haw k) hc
    exact le_trans h1 (le_trans h2 (le_max_left _ _))

theorem pR_le_bP (a b : ℚ) (w : ℝ) (ha : 0 ≤ (a : ℝ)) (haw : (a : ℝ) ≤ w) (hwb : w ≤ b) :
    ∀ (es : List ℝ) (cs : List ℚ), List.Forall₂ (fun (e : ℝ) (c : ℚ) => e ≤ (c : ℝ)) es cs →
      ∀ k, pR es k w ≤ (bP cs k a b : ℝ) := by
  intro es cs h
  induction h with
  | nil => intro k; simp [pR, bP]
  | cons hec _ ih =>
    intro k
    simp only [pR, bP, Rat.cast_add]
    exact add_le_add (term_le _ _ _ _ _ _ ha haw hwb hec) (ih (k + 1))

/-- **Correction du vérificateur** : si `bP cs 0 a b < 0` (calcul rationnel exact), alors tout polynôme
réel dont les coefficients sont majorés par `cs` est `< 0` sur `[a, b]`. -/
theorem sound (cs : List ℚ) (a b : ℚ) (ha : 0 ≤ a) (hneg : bP cs 0 a b < 0)
    (es : List ℝ) (hes : List.Forall₂ (fun (e : ℝ) (c : ℚ) => e ≤ (c : ℝ)) es cs)
    (w : ℝ) (haw : (a : ℝ) ≤ w) (hwb : w ≤ b) : pR es 0 w < 0 := by
  have h := pR_le_bP a b w (by exact_mod_cast ha) haw hwb es cs hes 0
  have h' : ((bP cs 0 a b : ℚ) : ℝ) < 0 := by exact_mod_cast hneg
  linarith

/-- `pR es 0 w` est bien le polynôme `Σ_{j < |es|} e_j w^j`. -/
theorem pR_eq_sum (es : List ℝ) (w : ℝ) :
    ∀ k, pR es k w = ∑ j ∈ Finset.range es.length, es.getD j 0 * w ^ (k + j) := by
  induction es with
  | nil => intro k; simp [pR]
  | cons e es ih =>
    intro k
    rw [pR, ih (k + 1), List.length_cons, Finset.sum_range_succ']
    simp only [List.getD_cons_succ, List.getD_cons_zero, add_zero]
    rw [add_comm]
    congr 1
    refine Finset.sum_congr rfl (fun j _ => ?_)
    ring_nf

/-! ## Arithmétique du seuil -/

/-- κ_max = 6·(π/16) = 3π/8 < 59/50 = K (borne de la boîte certifiée). -/
theorem kappa_max_lt : 6 * (Real.pi / 16) < (59 : ℝ) / 50 := by
  have := Real.pi_lt_d4
  norm_num at this ⊢
  linarith

/-- Somme de Dobrushin à un lien : `18 · β · (8/(9π)) = 16β/π < 1` pour `0 ≤ β < π/16`. -/
theorem somme_dobrushin_lt_one (β : ℝ) (hβ : β < Real.pi / 16) :
    18 * β * (8 / (9 * Real.pi)) < 1 := by
  have hpi := Real.pi_pos
  have e : 18 * β * (8 / (9 * Real.pi)) = 16 * β / Real.pi := by
    field_simp; ring
  rw [e, div_lt_one hpi]
  linarith

/-- Au bord, la somme vaut exactement 1 : le seuil π/16 est exactement marginal. -/
theorem somme_dobrushin_bord : 18 * (Real.pi / 16) * (8 / (9 * Real.pi)) = 1 := by
  have hpi := Real.pi_pos.ne'
  field_simp; ring

/-- Réciproque : pour `β ≥ π/16`, la somme `18 · β · (8/(9π))` est `≥ 1`. -/
theorem somme_dobrushin_ge_one (β : ℝ) (hβ : Real.pi / 16 ≤ β) :
    1 ≤ 18 * β * (8 / (9 * Real.pi)) := by
  have hpi := Real.pi_pos
  have e : 18 * β * (8 / (9 * Real.pi)) = 16 * β / Real.pi := by
    field_simp; ring
  rw [e, le_div_iff₀ hpi]
  linarith

end KevYM.Certif.DobrushinLien
