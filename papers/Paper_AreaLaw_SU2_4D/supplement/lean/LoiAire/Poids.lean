import Mathlib

/-!
# Propriétés élémentaires des poids par site (PREUVE.md §5), démontrées

`Mser J s = Σ_k (J² s)^k / (k!(k+1)!)`, `ρ_J(s) = M_J(s)/M_J(1)`, `h_J(λ) = ρ_J((1−λ)²)³`,
`Ã_n(J) = ∫₀¹ λ^{n−1}(1−λ)/(n−1)! · h_J(λ) dλ`.
Démontré ici : 0 < h_J ≤ 1 sur [0,1], `Ã_n(J) > 0` et `Ã₁(J) ≤ 1/2` (pour tout J réel).
Les définitions sont celles de `Enonce.lean` (recopiées à l'identique pour garder ce fichier autonome).
-/

namespace LoiAire.Poids

open Finset

noncomputable section

def Mser (J s : ℝ) : ℝ := ∑' k : ℕ, (J ^ 2 * s) ^ k / ((k.factorial : ℝ) * ((k + 1).factorial : ℝ))
def rhoJ (J s : ℝ) : ℝ := Mser J s / Mser J 1
def hJ (J t : ℝ) : ℝ := rhoJ J ((1 - t) ^ 2) ^ 3
def fpoids (n : ℕ) (t : ℝ) : ℝ := t ^ (n - 1) * (1 - t) / ((n - 1).factorial : ℝ)
def Atilde (J : ℝ) (n : ℕ) : ℝ := ∫ t in (0 : ℝ)..1, fpoids n t * hJ J t

theorem terme_le (x : ℝ) (hx : 0 ≤ x) (k : ℕ) :
    x ^ k / ((k.factorial : ℝ) * ((k + 1).factorial : ℝ)) ≤ x ^ k / (k.factorial : ℝ) := by
  apply div_le_div_of_nonneg_left (pow_nonneg hx k) (by positivity)
  have h1 : (1 : ℝ) ≤ ((k + 1).factorial : ℝ) := by exact_mod_cast Nat.one_le_iff_ne_zero.mpr (Nat.factorial_ne_zero _)
  nlinarith [show (0 : ℝ) < (k.factorial : ℝ) by positivity]

theorem summable_terme (x : ℝ) (hx : 0 ≤ x) :
    Summable (fun k : ℕ => x ^ k / ((k.factorial : ℝ) * ((k + 1).factorial : ℝ))) := by
  refine Summable.of_nonneg_of_le (fun k => by positivity) (fun k => terme_le x hx k) ?_
  exact Real.summable_pow_div_factorial x

theorem Mser_ge_one (J s : ℝ) (hs : 0 ≤ s) : 1 ≤ Mser J s := by
  have hx : 0 ≤ J ^ 2 * s := by positivity
  unfold Mser
  have h := (summable_terme _ hx).le_tsum 0 (fun k _ => by positivity)
  simpa using h

theorem Mser_mono (J : ℝ) {s s' : ℝ} (hs : 0 ≤ s) (hss' : s ≤ s') : Mser J s ≤ Mser J s' := by
  have hx : 0 ≤ J ^ 2 * s := by positivity
  have hx' : 0 ≤ J ^ 2 * s' := by nlinarith [sq_nonneg J]
  unfold Mser
  apply (summable_terme _ hx).tsum_le_tsum _ (summable_terme _ hx')
  intro k
  apply div_le_div_of_nonneg_right _ (by positivity)
  apply pow_le_pow_left₀ hx
  nlinarith [sq_nonneg J]

theorem rhoJ_pos (J s : ℝ) (hs : 0 ≤ s) : 0 < rhoJ J s := by
  unfold rhoJ
  have := Mser_ge_one J s hs
  have := Mser_ge_one J 1 zero_le_one
  positivity

theorem rhoJ_le_one (J s : ℝ) (hs : 0 ≤ s) (hs1 : s ≤ 1) : rhoJ J s ≤ 1 := by
  unfold rhoJ
  have h1 := Mser_ge_one J 1 zero_le_one
  rw [div_le_one (by linarith)]
  exact Mser_mono J hs hs1

theorem hJ_pos (J t : ℝ) : 0 < hJ J t := by
  unfold hJ
  exact pow_pos (rhoJ_pos J _ (sq_nonneg _)) 3

theorem hJ_le_one (J t : ℝ) (ht0 : 0 ≤ t) (ht1 : t ≤ 1) : hJ J t ≤ 1 := by
  unfold hJ
  have hs : (1 - t) ^ 2 ≤ 1 := by nlinarith
  exact pow_le_one₀ (rhoJ_pos J _ (sq_nonneg _)).le (rhoJ_le_one J _ (sq_nonneg _) hs)

/-- Terme général de la série M_J. -/
def terme (J : ℝ) (k : ℕ) (s : ℝ) : ℝ := (J ^ 2 * s) ^ k / ((k.factorial : ℝ) * ((k + 1).factorial : ℝ))

theorem terme_continuous (J : ℝ) (k : ℕ) : Continuous (terme J k) := by
  unfold terme
  exact ((continuous_const.mul continuous_id).pow k).div_const _

/-- Continuité de s ↦ M_J(s) sur [0, 1] (test de Weierstrass). -/
theorem Mser_continuousOn (J : ℝ) : ContinuousOn (fun s => Mser J s) (Set.Icc 0 1) := by
  have hx : 0 ≤ J ^ 2 := sq_nonneg J
  have hbound : ∀ (k : ℕ) (s : ℝ), s ∈ Set.Icc (0 : ℝ) 1 → ‖terme J k s‖ ≤ terme J k 1 := by
    intro k s hs
    have h0 : 0 ≤ J ^ 2 * s := mul_nonneg hx hs.1
    unfold terme
    rw [Real.norm_eq_abs, abs_of_nonneg (by positivity)]
    apply div_le_div_of_nonneg_right _ (by positivity)
    apply pow_le_pow_left₀ h0
    nlinarith [hs.2]
  have hsum : Summable (fun k => terme J k 1) := summable_terme (J ^ 2 * 1) (by positivity)
  have h := continuousOn_tsum (f := fun k s => terme J k s) (s := Set.Icc (0 : ℝ) 1)
    (fun k => (terme_continuous J k).continuousOn) hsum hbound
  have e : (fun s => Mser J s) = (fun s => ∑' k, terme J k s) := rfl
  rw [e]
  exact h

theorem hJ_continuousOn (J : ℝ) : ContinuousOn (fun t => hJ J t) (Set.Icc 0 1) := by
  unfold hJ rhoJ
  have hM1 : Mser J 1 ≠ 0 := by have := Mser_ge_one J 1 zero_le_one; positivity
  have hmap : Set.MapsTo (fun t : ℝ => (1 - t) ^ 2) (Set.Icc 0 1) (Set.Icc 0 1) := by
    intro t ht
    exact ⟨sq_nonneg _, by nlinarith [ht.1, ht.2]⟩
  have hc : ContinuousOn (fun t : ℝ => Mser J ((1 - t) ^ 2)) (Set.Icc 0 1) :=
    (Mser_continuousOn J).comp (by fun_prop) hmap
  exact ((hc.div_const _)).pow 3

theorem integrand_continuousOn (J : ℝ) (n : ℕ) :
    ContinuousOn (fun t => fpoids n t * hJ J t) (Set.Icc 0 1) := by
  unfold fpoids
  exact ContinuousOn.mul (by fun_prop) (hJ_continuousOn J)

theorem Atilde_pos (J : ℝ) (n : ℕ) : 0 < Atilde J n := by
  unfold Atilde
  have hcont : ContinuousOn (fun t => fpoids n t * hJ J t) (Set.uIcc 0 1) := by
    rw [Set.uIcc_of_le zero_le_one]; exact integrand_continuousOn J n
  apply intervalIntegral.intervalIntegral_pos_of_pos_on (hcont.intervalIntegrable) _ zero_lt_one
  intro t ht
  unfold fpoids
  have h1 : 0 < 1 - t := by linarith [ht.2]
  have h2 : 0 < t ^ (n - 1) := pow_pos ht.1 _
  have h3 := hJ_pos J t
  positivity

theorem Atilde_one_le (J : ℝ) : Atilde J 1 ≤ 1 / 2 := by
  unfold Atilde
  have hcont : ContinuousOn (fun t => fpoids 1 t * hJ J t) (Set.uIcc 0 1) := by
    rw [Set.uIcc_of_le zero_le_one]; exact integrand_continuousOn J 1
  have h : ∫ t in (0 : ℝ)..1, fpoids 1 t * hJ J t ≤ ∫ t in (0 : ℝ)..1, (1 - t) := by
    apply intervalIntegral.integral_mono_on zero_le_one hcont.intervalIntegrable
    · exact (by fun_prop : Continuous fun t : ℝ => 1 - t).intervalIntegrable _ _
    · intro t ht
      simp only [fpoids, Nat.sub_self, pow_zero, Nat.factorial_zero, Nat.cast_one, div_one, one_mul]
      have h1 : 0 ≤ 1 - t := by linarith [ht.2]
      have := hJ_le_one J t ht.1 ht.2
      nlinarith
  calc ∫ t in (0 : ℝ)..1, fpoids 1 t * hJ J t ≤ ∫ t in (0 : ℝ)..1, (1 - t) := h
    _ = 1 / 2 := by
        rw [intervalIntegral.integral_sub intervalIntegrable_const intervalIntegral.intervalIntegrable_id, integral_id,
          intervalIntegral.integral_const]
        norm_num

end

end LoiAire.Poids
