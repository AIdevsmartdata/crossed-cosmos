import Mathlib

/-! CentreZN — base figée de la partie A (pilote, 12/11/2026) : en-tête seulement. -/

set_option autoImplicit false

open MeasureTheory Finset

noncomputable section

namespace CentreZN

lemma zn_norm_pow {N : ℕ} [NeZero N] (ζ : ℂ) (hζ : ζ ^ N = 1)
    (j : ZMod N) : ‖ζ ^ j.val‖ = 1 := by
  rw [norm_pow, Complex.norm_eq_one_of_pow_eq_one hζ (NeZero.ne N), one_pow]

lemma zn_pow_add {N : ℕ} [NeZero N] (ζ : ℂ) (hζ : ζ ^ N = 1)
    (a b : ZMod N) :
    ζ ^ (a + b).val = ζ ^ a.val * ζ ^ b.val := by
  exact (AddChar.zmodChar N hζ).map_add_eq_mul a b

lemma zn_phase_sum {I : Type*} [DecidableEq I]
    {N : ℕ} [NeZero N] (ζ : ℂ) (hζ : ζ ^ N = 1)
    (q : ZMod N) (A : Finset I) (t : I → ZMod N) :
    ζ ^ (q * ∑ p ∈ A, t p).val = ∏ p ∈ A, ζ ^ (q * t p).val := by
  induction A using Finset.induction_on with
  | empty => simp
  | @insert p A hp ih =>
      rw [Finset.sum_insert hp, Finset.prod_insert hp, mul_add,
        zn_pow_add ζ hζ, ih]

def zn_partition {P : Type*} [Fintype P] [DecidableEq P]
    (N : ℕ) [NeZero N] (ζ : ℂ) (x : P → ℂ) : ℝ :=
  ∑ t : P → ZMod N, Real.exp (∑ p, (ζ ^ (t p).val * x p).re)

def zn_charged {P : Type*} [Fintype P] [DecidableEq P]
    (N : ℕ) [NeZero N] (ζ : ℂ) (q : ZMod N)
    (A : Finset P) (x : P → ℂ) : ℂ :=
  ∑ t : P → ZMod N, ζ ^ (q * ∑ p ∈ A, t p).val *
    ((Real.exp (∑ p, (ζ ^ (t p).val * x p).re) : ℝ) : ℂ)

lemma zn_partition_eq {P : Type*} [Fintype P] [DecidableEq P]
    (N : ℕ) [NeZero N] (ζ : ℂ) (x : P → ℂ) :
    zn_partition N ζ x =
      ∏ p, ∑ j : ZMod N, Real.exp ((ζ ^ j.val * x p).re) := by
  classical
  calc
    zn_partition N ζ x =
        ∑ t : P → ZMod N, ∏ p, Real.exp ((ζ ^ (t p).val * x p).re) := by
      simp only [zn_partition, Real.exp_sum]
    _ = ∏ p, ∑ j : ZMod N, Real.exp ((ζ ^ j.val * x p).re) :=
      (Fintype.prod_sum
        (fun p (j : ZMod N) => Real.exp ((ζ ^ j.val * x p).re))).symm

lemma zn_charged_eq {P : Type*} [Fintype P] [DecidableEq P]
    (N : ℕ) [NeZero N] (ζ : ℂ) (hζ : ζ ^ N = 1)
    (q : ZMod N) (A : Finset P) (x : P → ℂ) :
    zn_charged N ζ q A x =
      ∏ p, ∑ j : ZMod N,
        (if p ∈ A then ζ ^ (q * j).val else 1) *
          ((Real.exp ((ζ ^ j.val * x p).re) : ℝ) : ℂ) := by
  classical
  have hterm (t : P → ZMod N) :
      ζ ^ (q * ∑ p ∈ A, t p).val *
          ((Real.exp (∑ p, (ζ ^ (t p).val * x p).re) : ℝ) : ℂ) =
        ∏ p, (if p ∈ A then ζ ^ (q * t p).val else 1) *
          ((Real.exp ((ζ ^ (t p).val * x p).re) : ℝ) : ℂ) := by
    simp only [zn_phase_sum ζ hζ, Real.exp_sum, Complex.ofReal_prod,
      Finset.prod_mul_distrib, Fintype.prod_ite_mem]
  calc
    zn_charged N ζ q A x =
        ∑ t : P → ZMod N,
          ∏ p, (if p ∈ A then ζ ^ (q * t p).val else 1) *
            ((Real.exp ((ζ ^ (t p).val * x p).re) : ℝ) : ℂ) := by
      exact Finset.sum_congr rfl (fun t _ => hterm t)
    _ = ∏ p, ∑ j : ZMod N,
        (if p ∈ A then ζ ^ (q * j).val else 1) *
          ((Real.exp ((ζ ^ j.val * x p).re) : ℝ) : ℂ) :=
      (Fintype.prod_sum (fun p (j : ZMod N) =>
        (if p ∈ A then ζ ^ (q * j).val else 1) *
          ((Real.exp ((ζ ^ j.val * x p).re) : ℝ) : ℂ))).symm

lemma zn_charged_bound {P : Type*} [Fintype P] [DecidableEq P]
    (N : ℕ) [NeZero N] (ζ : ℂ) (hζ : ζ ^ N = 1)
    (q : ZMod N) (A : Finset P) (x : P → ℂ)
    (κ : ℝ) (hx : ∀ p, ‖x p‖ ≤ κ) (ρ : ℝ)
    (hρ : ∀ t : ℂ, ‖t‖ ≤ κ →
      ‖∑ j : ZMod N, ζ ^ (q * j).val *
          ((Real.exp ((ζ ^ j.val * t).re) : ℝ) : ℂ)‖
        ≤ ρ * ∑ j : ZMod N, Real.exp ((ζ ^ j.val * t).re)) :
    ‖zn_charged N ζ q A x‖ ≤ ρ ^ A.card * zn_partition N ζ x := by
  classical
  rw [zn_charged_eq N ζ hζ, Complex.norm_prod]
  calc
    (∏ p, ‖∑ j : ZMod N,
        (if p ∈ A then ζ ^ (q * j).val else 1) *
          ((Real.exp ((ζ ^ j.val * x p).re) : ℝ) : ℂ)‖) ≤
        ∏ p, (if p ∈ A then ρ else 1) *
          ∑ j : ZMod N, Real.exp ((ζ ^ j.val * x p).re) := by
      apply Finset.prod_le_prod
      · intro p _
        exact norm_nonneg _
      · intro p _
        by_cases hp : p ∈ A
        · simpa only [if_pos hp] using hρ (x p) (hx p)
        · have hs : 0 ≤ ∑ j : ZMod N, Real.exp ((ζ ^ j.val * x p).re) :=
            Finset.sum_nonneg (fun j _ => (Real.exp_pos _).le)
          simp only [if_neg hp, one_mul, ← Complex.ofReal_sum,
            Complex.norm_real, Real.norm_eq_abs, abs_of_nonneg hs]
          exact le_rfl
    _ = ρ ^ A.card * zn_partition N ζ x := by
      rw [Finset.prod_mul_distrib, Fintype.prod_ite_mem,
        zn_partition_eq N ζ x]
      simp

lemma zn_integral_preserving
    {Ω 𝕜 : Type*} [MeasurableSpace Ω] [RCLike 𝕜]
    {μ : Measure Ω} {T : Ω → Ω}
    (hT : MeasurePreserving T μ μ) (f : Ω → 𝕜) (hf : Measurable f) :
    (∫ ω, f (T ω) ∂μ) = ∫ ω, f ω ∂μ := by
  have h := integral_map_of_stronglyMeasurable
    (μ := μ) hT.measurable hf.stronglyMeasurable
  rw [hT.map_eq] at h
  exact h.symm

lemma zn_integrable_change
    {Ω P : Type*} [MeasurableSpace Ω] [Fintype P]
    (μ : Measure Ω) (R : Ω → ℝ)
    (hRm : Measurable R) (hR0 : ∀ ω, 0 ≤ R ω)
    (K : P → Ω → ℝ) (κ : ℝ) (hK : ∀ p ω, |K p ω| ≤ κ)
    (hRint : Integrable (fun ω => R ω * Real.exp (∑ p, K p ω)) μ)
    (L : P → Ω → ℝ) (hLm : ∀ p, Measurable (L p))
    (hL : ∀ p ω, |L p ω| ≤ κ) :
    Integrable (fun ω => R ω * Real.exp (∑ p, L p ω)) μ := by
  classical
  let c : ℝ := Real.exp (∑ _p : P, 2 * κ)
  have hm : Measurable (fun ω => R ω * Real.exp (∑ p, L p ω)) :=
    hRm.mul (Finset.measurable_sum univ (fun p _ => hLm p)).exp
  apply (hRint.const_mul c).mono' hm.aestronglyMeasurable
  apply Filter.Eventually.of_forall
  intro ω
  have hs : (∑ p, L p ω) ≤ (∑ p, K p ω) + ∑ _p : P, 2 * κ := by
    calc
      (∑ p, L p ω) ≤ ∑ p, (K p ω + 2 * κ) := by
        apply Finset.sum_le_sum
        intro p _
        have hk := (abs_le.mp (hK p ω)).1
        have hl := (abs_le.mp (hL p ω)).2
        linarith
      _ = (∑ p, K p ω) + ∑ _p : P, 2 * κ := Finset.sum_add_distrib
  have he : Real.exp (∑ p, L p ω) ≤ c * Real.exp (∑ p, K p ω) := by
    calc
      Real.exp (∑ p, L p ω) ≤
          Real.exp ((∑ p, K p ω) + ∑ _p : P, 2 * κ) :=
        Real.exp_le_exp.mpr hs
      _ = c * Real.exp (∑ p, K p ω) := by
        dsimp only [c]
        rw [Real.exp_add]
        ring
  rw [Real.norm_eq_abs,
    abs_of_nonneg (mul_nonneg (hR0 ω) (Real.exp_pos _).le)]
  calc
    R ω * Real.exp (∑ p, L p ω) ≤
        R ω * (c * Real.exp (∑ p, K p ω)) :=
      mul_le_mul_of_nonneg_left he (hR0 ω)
    _ = c * (R ω * Real.exp (∑ p, K p ω)) := by ring

lemma zn_sum_total
    {P C : Type*} [Fintype P] [DecidableEq P] [CommSemiring C]
    {N : ℕ} [NeZero N] (p₀ : P) (f : ZMod N → C) :
    (N : C) * (∑ t : P → ZMod N, f (∑ p, t p)) =
      (Fintype.card (P → ZMod N) : C) * ∑ k : ZMod N, f k := by
  classical
  let v : ZMod N → P → ZMod N := fun k p => if p = p₀ then k else 0
  have hv (k : ZMod N) : ∑ p, v k p = k := by
    simp [v]
  have hshift (k : ZMod N) :
      (∑ t : P → ZMod N, f ((∑ p, t p) + k)) =
        ∑ t : P → ZMod N, f (∑ p, t p) := by
    calc
      (∑ t : P → ZMod N, f ((∑ p, t p) + k)) =
          ∑ t : P → ZMod N, f (∑ p, (t + v k) p) := by
        apply Finset.sum_congr rfl
        intro t _
        simp only [Pi.add_apply, Finset.sum_add_distrib, hv]
      _ = ∑ t : P → ZMod N, f (∑ p, t p) :=
        Equiv.sum_comp (Equiv.addRight (v k))
          (fun t : P → ZMod N => f (∑ p, t p))
  calc
    (N : C) * (∑ t : P → ZMod N, f (∑ p, t p)) =
        ∑ _k : ZMod N, ∑ t : P → ZMod N, f (∑ p, t p) := by
      simp [ZMod.card, nsmul_eq_mul]
    _ = ∑ k : ZMod N, ∑ t : P → ZMod N, f ((∑ p, t p) + k) := by
      exact Finset.sum_congr rfl (fun k _ => (hshift k).symm)
    _ = ∑ t : P → ZMod N, ∑ k : ZMod N, f ((∑ p, t p) + k) :=
      Finset.sum_comm
    _ = ∑ _t : P → ZMod N, ∑ k : ZMod N, f k := by
      apply Finset.sum_congr rfl
      intro t _
      exact Equiv.sum_comp (Equiv.addLeft (∑ p, t p)) f
    _ = (Fintype.card (P → ZMod N) : C) * ∑ k : ZMod N, f k := by
      simp [nsmul_eq_mul]

lemma zn_tanh_mono {x y : ℝ} (hxy : x ≤ y) :
    Real.tanh x ≤ Real.tanh y := by
  have hpos : Real.exp x ≤ Real.exp y := Real.exp_le_exp.mpr hxy
  have hneg : Real.exp (-y) ≤ Real.exp (-x) :=
    Real.exp_le_exp.mpr (by linarith)
  have hp : Real.exp x * Real.exp (-y) ≤ Real.exp y * Real.exp (-x) := by
    calc
      Real.exp x * Real.exp (-y) ≤ Real.exp y * Real.exp (-y) :=
        mul_le_mul_of_nonneg_right hpos (Real.exp_pos (-y)).le
      _ ≤ Real.exp y * Real.exp (-x) :=
        mul_le_mul_of_nonneg_left hneg (Real.exp_pos y).le
  rw [Real.tanh_eq, Real.tanh_eq]
  apply (div_le_div_iff₀
    (add_pos (Real.exp_pos x) (Real.exp_pos (-x)))
    (add_pos (Real.exp_pos y) (Real.exp_pos (-y)))).2
  nlinarith [hp]

lemma zn_abs_tanh_le {x κ : ℝ} (hx : |x| ≤ κ) :
    |Real.tanh x| ≤ Real.tanh κ := by
  obtain ⟨hl, hu⟩ := abs_le.mp hx
  apply abs_le.mpr
  constructor
  · have h := zn_tanh_mono hl
    rw [Real.tanh_neg] at h
    exact h
  · exact zn_tanh_mono hu

lemma zn_sum_two {F : Type*} [AddCommMonoid F] (f : ZMod 2 → F) :
    (∑ j : ZMod 2, f j) = f 0 + f 1 := by
  calc
    (∑ j : ZMod 2, f j) = ∑ j : Fin 2, f ((ZMod.finEquiv 2) j) :=
      ((ZMod.finEquiv 2).toEquiv.sum_comp f).symm
    _ = f 0 + f 1 := by
      rw [Fin.sum_univ_two]
      rfl

def zn_charge (u : ℤˣ) : ZMod 2 := if u = 1 then 0 else 1

def zn_sign (j : ZMod 2) : ℤˣ := if j = 0 then 1 else -1

lemma zn_units_cases (u : ℤˣ) : u = 1 ∨ u = -1 := by
  rcases Int.isUnit_eq_one_or u.isUnit with h | h
  · left
    apply Units.ext
    simpa using h
  · right
    apply Units.ext
    simpa using h

lemma zn_charge_sign (j : ZMod 2) : zn_charge (zn_sign j) = j := by
  fin_cases j <;> decide

lemma zn_sign_charge (u : ℤˣ) : zn_sign (zn_charge u) = u := by
  rcases zn_units_cases u with rfl | rfl <;> decide

lemma zn_charge_mul (u v : ℤˣ) :
    zn_charge (u * v) = zn_charge u + zn_charge v := by
  rcases zn_units_cases u with rfl | rfl <;>
    rcases zn_units_cases v with rfl | rfl <;> decide

lemma zn_charge_prod {I : Type*} [DecidableEq I]
    (A : Finset I) (t : I → ℤˣ) :
    zn_charge (∏ p ∈ A, t p) = ∑ p ∈ A, zn_charge (t p) := by
  induction A using Finset.induction_on with
  | empty => simp [zn_charge]
  | @insert p A hp ih => simp [hp, zn_charge_mul, ih]

lemma zn_sign_add (a b : ZMod 2) :
    zn_sign (a + b) = zn_sign a * zn_sign b := by
  fin_cases a <;> fin_cases b <;> decide

lemma zn_sign_sum {I : Type*} [DecidableEq I]
    (A : Finset I) (t : I → ZMod 2) :
    zn_sign (∑ p ∈ A, t p) = ∏ p ∈ A, zn_sign (t p) := by
  induction A using Finset.induction_on with
  | empty => simp [zn_sign]
  | @insert p A hp ih =>
      rw [Finset.sum_insert hp, Finset.prod_insert hp, zn_sign_add, ih]

lemma zn_cast_charge (u : ℤˣ) :
    ((((u : ℤ) : ℝ) : ℂ)) = (-1 : ℂ) ^ (zn_charge u).val := by
  have hn : (-1 : ℤˣ) ≠ 1 := by decide
  rcases zn_units_cases u with rfl | rfl <;>
    norm_num [zn_charge, hn, ZMod.val_one_eq_one_mod]

/-! ## Partie A : forme abstraite -/

/-- A1. Abstract centre-twist bound (open surface). Twists `τ s` preserve `μ`; the charge map `chg` onto
`P → ZMod N` is surjective; the complex couplings rotate, `T p ∘ τ s = ζ ^ (chg s p) • T p`; the weight `R` is
invariant; the observable `W` takes the phase `ζ ^ (q • Σ_{p ∈ A} chg s p)`; `ρ` dominates the one-plaquette
Fourier ratio on the disc of radius `κ`. -/
theorem centre_flip_bound
    {Ω S P : Type*} [MeasurableSpace Ω] [Fintype P] [DecidableEq P]
    (N : ℕ) [NeZero N] (ζ : ℂ) (hζ : ζ ^ N = 1)
    (μ : Measure Ω) [IsProbabilityMeasure μ]
    (τ : S → Ω → Ω) (hτ : ∀ s, MeasurePreserving (τ s) μ μ)
    (chg : S → P → ZMod N) (hsurj : Function.Surjective chg)
    (T : P → Ω → ℂ) (hTm : ∀ p, Measurable (T p))
    (κ : ℝ) (hT : ∀ p ω, ‖T p ω‖ ≤ κ)
    (hTτ : ∀ s p ω, T p (τ s ω) = ζ ^ (chg s p).val * T p ω)
    (R : Ω → ℝ) (hRm : Measurable R) (hR0 : ∀ ω, 0 ≤ R ω) (hRτ : ∀ s ω, R (τ s ω) = R ω)
    (hRint : Integrable (fun ω => R ω * Real.exp (∑ p, (T p ω).re)) μ)
    (W : Ω → ℂ) (hWm : Measurable W) (hW1 : ∀ ω, ‖W ω‖ ≤ 1)
    (q : ZMod N) (A : Finset P)
    (hWτ : ∀ s ω, W (τ s ω) = ζ ^ (q * ∑ p ∈ A, chg s p).val * W ω)
    (ρ : ℝ)
    (hρ : ∀ t : ℂ, ‖t‖ ≤ κ →
      ‖∑ j : ZMod N, ζ ^ (q * j).val * ((Real.exp ((ζ ^ j.val * t).re) : ℝ) : ℂ)‖
        ≤ ρ * ∑ j : ZMod N, Real.exp ((ζ ^ j.val * t).re)) :
    ‖∫ ω, W ω * ((R ω * Real.exp (∑ p, (T p ω).re) : ℝ) : ℂ) ∂μ‖
      ≤ ρ ^ A.card * ∫ ω, R ω * Real.exp (∑ p, (T p ω).re) ∂μ := by
  classical
  let D : Ω → ℝ := fun ω => R ω * Real.exp (∑ p, (T p ω).re)
  let G : Ω → ℂ := fun ω => W ω * (D ω : ℂ)
  let d : (P → ZMod N) → Ω → ℝ :=
    fun t ω => R ω * Real.exp (∑ p, (ζ ^ (t p).val * T p ω).re)
  let g : (P → ZMod N) → Ω → ℂ :=
    fun t ω => ζ ^ (q * ∑ p ∈ A, t p).val * W ω * (d t ω : ℂ)
  let H : Ω → ℝ := fun ω => ∑ t, d t ω
  let J : Ω → ℂ := fun ω => ∑ t, g t ω
  let n : ℕ := Fintype.card (P → ZMod N)
  let b : ℝ := ρ ^ A.card
  have hn : 0 < (n : ℝ) := by
    dsimp only [n]
    exact_mod_cast (Fintype.card_pos : 0 < Fintype.card (P → ZMod N))
  have hDm : Measurable D := by
    dsimp only [D]
    fun_prop
  have hGm : Measurable G := by
    dsimp only [G]
    fun_prop
  have hDi : Integrable D μ := hRint
  have hD0 (ω : Ω) : 0 ≤ D ω :=
    mul_nonneg (hR0 ω) (Real.exp_pos _).le
  have hGi : Integrable G μ := by
    apply hDi.mono' hGm.aestronglyMeasurable
    apply Filter.Eventually.of_forall
    intro ω
    change ‖W ω * (D ω : ℂ)‖ ≤ D ω
    rw [norm_mul, Complex.norm_real, Real.norm_eq_abs, abs_of_nonneg (hD0 ω)]
    simpa only [one_mul] using
      mul_le_mul_of_nonneg_right (hW1 ω) (hD0 ω)
  have hprops (t : P → ZMod N) :
      Integrable (d t) μ ∧ Integrable (g t) μ ∧
        (∫ ω, d t ω ∂μ) = (∫ ω, D ω ∂μ) ∧
        (∫ ω, g t ω ∂μ) = (∫ ω, G ω ∂μ) := by
    obtain ⟨s, hs⟩ := hsurj t
    have hsig (p : P) : chg s p = t p := congrFun hs p
    have hdt : (fun ω => D (τ s ω)) = d t := by
      funext ω
      dsimp only [D, d]
      simp only [hRτ s, hTτ s, hsig]
    have hgt : (fun ω => G (τ s ω)) = g t := by
      funext ω
      change W (τ s ω) * (D (τ s ω) : ℂ) =
        ζ ^ (q * ∑ p ∈ A, t p).val * W ω * (d t ω : ℂ)
      rw [hWτ s ω, congrFun hdt ω]
      simp only [hsig]
    refine ⟨?_, ?_, ?_, ?_⟩
    · have h := (hτ s).integrable_comp_of_integrable hDi
      change Integrable (fun ω => D (τ s ω)) μ at h
      rw [hdt] at h
      exact h
    · have h := (hτ s).integrable_comp_of_integrable hGi
      change Integrable (fun ω => G (τ s ω)) μ at h
      rw [hgt] at h
      exact h
    · have h := zn_integral_preserving (hτ s) D hDm
      rw [hdt] at h
      exact h
    · have h := zn_integral_preserving (hτ s) G hGm
      rw [hgt] at h
      exact h
  have hHi : Integrable H μ :=
    integrable_finsetSum univ (fun t _ => (hprops t).1)
  have hHInt : (∫ ω, H ω ∂μ) = (n : ℝ) * ∫ ω, D ω ∂μ := by
    calc
      (∫ ω, H ω ∂μ) = ∑ t, ∫ ω, d t ω ∂μ :=
        integral_finsetSum univ (fun t _ => (hprops t).1)
      _ = ∑ _t : P → ZMod N, ∫ ω, D ω ∂μ :=
        Finset.sum_congr rfl (fun t _ => (hprops t).2.2.1)
      _ = (n : ℝ) * ∫ ω, D ω ∂μ := by simp [n, nsmul_eq_mul]
  have hJInt : (∫ ω, J ω ∂μ) = (n : ℂ) * ∫ ω, G ω ∂μ := by
    calc
      (∫ ω, J ω ∂μ) = ∑ t, ∫ ω, g t ω ∂μ :=
        integral_finsetSum univ (fun t _ => (hprops t).2.1)
      _ = ∑ _t : P → ZMod N, ∫ ω, G ω ∂μ :=
        Finset.sum_congr rfl (fun t _ => (hprops t).2.2.2)
      _ = (n : ℂ) * ∫ ω, G ω ∂μ := by simp [n, nsmul_eq_mul]
  have hH (ω : Ω) : H ω = R ω * zn_partition N ζ (fun p => T p ω) := by
    dsimp only [H, d, zn_partition]
    rw [Finset.mul_sum]
  have hJ (ω : Ω) :
      J ω = W ω * (R ω : ℂ) * zn_charged N ζ q A (fun p => T p ω) := by
    dsimp only [J, g, d, zn_charged]
    rw [Finset.mul_sum]
    apply Finset.sum_congr rfl
    intro t _
    simp only [Complex.ofReal_mul]
    ring
  have hpoint (ω : Ω) : ‖J ω‖ ≤ b * H ω := by
    rw [hJ ω, hH ω, norm_mul, norm_mul, Complex.norm_real,
      Real.norm_eq_abs, abs_of_nonneg (hR0 ω)]
    have hwr : ‖W ω‖ * R ω ≤ R ω := by
      simpa only [one_mul] using
        mul_le_mul_of_nonneg_right (hW1 ω) (hR0 ω)
    have hc := zn_charged_bound N ζ hζ q A (fun p => T p ω)
      κ (fun p => hT p ω) ρ hρ
    calc
      ‖W ω‖ * R ω * ‖zn_charged N ζ q A (fun p => T p ω)‖ ≤
          R ω * ‖zn_charged N ζ q A (fun p => T p ω)‖ :=
        mul_le_mul_of_nonneg_right hwr (norm_nonneg _)
      _ ≤ R ω * (b * zn_partition N ζ (fun p => T p ω)) :=
        mul_le_mul_of_nonneg_left hc (hR0 ω)
      _ = b * (R ω * zn_partition N ζ (fun p => T p ω)) := by ring
  have hbound : ‖∫ ω, J ω ∂μ‖ ≤ b * ∫ ω, H ω ∂μ := by
    calc
      ‖∫ ω, J ω ∂μ‖ ≤ ∫ ω, b * H ω ∂μ :=
        norm_integral_le_of_norm_le (hHi.const_mul b)
          (Filter.Eventually.of_forall hpoint)
      _ = b * ∫ ω, H ω ∂μ := integral_const_mul b H
  have hscaled :
      (n : ℝ) * ‖∫ ω, G ω ∂μ‖ ≤
        (n : ℝ) * (b * ∫ ω, D ω ∂μ) := by
    calc
      (n : ℝ) * ‖∫ ω, G ω ∂μ‖ = ‖∫ ω, J ω ∂μ‖ := by
        rw [hJInt, norm_mul, Complex.norm_natCast]
      _ ≤ b * ∫ ω, H ω ∂μ := hbound
      _ = (n : ℝ) * (b * ∫ ω, D ω ∂μ) := by
        rw [hHInt]
        ring
  exact (mul_le_mul_iff_right₀ hn).mp hscaled

/-- A2. Abstract twist-ratio bound (closed surface). Every charge assignment of total charge zero is realised by a
twist. `Z k` is the partition function in which the coupling of the plaquette `p₀` is multiplied by `ζ ^ k`; the
left side is the norm of its Fourier transform at `q`, the right side involves the sum of all `Z k`. -/
theorem twist_ratio_bound
    {Ω S P : Type*} [MeasurableSpace Ω] [Fintype P] [DecidableEq P]
    (N : ℕ) [NeZero N] (ζ : ℂ) (hζ : ζ ^ N = 1)
    (μ : Measure Ω) [IsProbabilityMeasure μ]
    (τ : S → Ω → Ω) (hτ : ∀ s, MeasurePreserving (τ s) μ μ)
    (chg : S → P → ZMod N)
    (himg : ∀ t : P → ZMod N, ∑ p, t p = 0 → ∃ s, chg s = t)
    (T : P → Ω → ℂ) (hTm : ∀ p, Measurable (T p))
    (κ : ℝ) (hT : ∀ p ω, ‖T p ω‖ ≤ κ)
    (hTτ : ∀ s p ω, T p (τ s ω) = ζ ^ (chg s p).val * T p ω)
    (R : Ω → ℝ) (hRm : Measurable R) (hR0 : ∀ ω, 0 ≤ R ω) (hRτ : ∀ s ω, R (τ s ω) = R ω)
    (hRint : Integrable (fun ω => R ω * Real.exp (∑ p, (T p ω).re)) μ)
    (q : ZMod N) (ρ : ℝ)
    (hρ : ∀ t : ℂ, ‖t‖ ≤ κ →
      ‖∑ j : ZMod N, ζ ^ (q * j).val * ((Real.exp ((ζ ^ j.val * t).re) : ℝ) : ℂ)‖
        ≤ ρ * ∑ j : ZMod N, Real.exp ((ζ ^ j.val * t).re))
    (p₀ : P) :
    ‖∑ k : ZMod N, ζ ^ (q * k).val *
        ((∫ ω, R ω * Real.exp (∑ p, ((if p = p₀ then ζ ^ k.val else 1) * T p ω).re) ∂μ : ℝ) : ℂ)‖
      ≤ ρ ^ Fintype.card P *
        ∑ k : ZMod N, ∫ ω, R ω * Real.exp (∑ p, ((if p = p₀ then ζ ^ k.val else 1) * T p ω).re) ∂μ := by
  classical
  let v : ZMod N → P → ZMod N := fun k p => if p = p₀ then k else 0
  let d : (P → ZMod N) → Ω → ℝ :=
    fun t ω => R ω * Real.exp (∑ p, (ζ ^ (t p).val * T p ω).re)
  let Z : ZMod N → ℝ := fun k => ∫ ω, d (v k) ω ∂μ
  let H : Ω → ℝ := fun ω => ∑ t : P → ZMod N, d t ω
  let J : Ω → ℂ := fun ω => ∑ t : P → ZMod N,
    ζ ^ (q * ∑ p, t p).val * (d t ω : ℂ)
  let m : ℕ := Fintype.card (P → ZMod N)
  let b : ℝ := ρ ^ Fintype.card P
  have hm : 0 < (m : ℝ) := by
    dsimp only [m]
    exact_mod_cast (Fintype.card_pos : 0 < Fintype.card (P → ZMod N))
  have hv (k : ZMod N) : ∑ p, v k p = k := by
    simp [v]
  have hdm (t : P → ZMod N) : Measurable (d t) := by
    dsimp only [d]
    fun_prop
  have hdi (t : P → ZMod N) : Integrable (d t) μ := by
    apply zn_integrable_change μ R hRm hR0
      (fun p ω => (T p ω).re) κ
      (fun p ω => (Complex.abs_re_le_norm (T p ω)).trans (hT p ω))
      hRint
      (fun p ω => (ζ ^ (t p).val * T p ω).re)
    · intro p
      fun_prop
    · intro p ω
      calc
        |(ζ ^ (t p).val * T p ω).re| ≤ ‖ζ ^ (t p).val * T p ω‖ :=
          Complex.abs_re_le_norm _
        _ = ‖T p ω‖ := by
          rw [norm_mul, zn_norm_pow ζ hζ, one_mul]
        _ ≤ κ := hT p ω
  have hprops (t : P → ZMod N) :
      (∫ ω, d t ω ∂μ) = Z (∑ p, t p) := by
    let k : ZMod N := ∑ p, t p
    let a : P → ZMod N := fun p => t p - v k p
    have ha : ∑ p, a p = 0 := by
      dsimp only [a]
      rw [Finset.sum_sub_distrib, hv]
      exact sub_self _
    obtain ⟨s, hs⟩ := himg a ha
    have hkey (p : P) : v k p + a p = t p := by
      dsimp only [a]
      abel
    have hdt : (fun ω => d (v k) (τ s ω)) = d t := by
      funext ω
      dsimp only [d]
      rw [hRτ s ω]
      congr 1
      apply congrArg Real.exp
      apply Finset.sum_congr rfl
      intro p _
      rw [hTτ s p ω, congrFun hs p, ← mul_assoc,
        ← zn_pow_add ζ hζ, hkey p]
    have h := zn_integral_preserving (hτ s) (d (v k)) (hdm (v k))
    rw [hdt] at h
    exact h
  have hHi : Integrable H μ :=
    integrable_finsetSum univ (fun t _ => hdi t)
  have hHint :
      (∫ ω, H ω ∂μ) = ∑ t : P → ZMod N, Z (∑ p, t p) := by
    calc
      (∫ ω, H ω ∂μ) = ∑ t : P → ZMod N, ∫ ω, d t ω ∂μ :=
        integral_finsetSum univ (fun t _ => hdi t)
      _ = ∑ t : P → ZMod N, Z (∑ p, t p) :=
        Finset.sum_congr rfl (fun t _ => hprops t)
  have hJint :
      (∫ ω, J ω ∂μ) =
        ∑ t : P → ZMod N, ζ ^ (q * ∑ p, t p).val *
          (Z (∑ p, t p) : ℂ) := by
    calc
      (∫ ω, J ω ∂μ) =
          ∑ t : P → ZMod N,
            ∫ ω, ζ ^ (q * ∑ p, t p).val * (d t ω : ℂ) ∂μ :=
        integral_finsetSum univ (fun t _ => (hdi t).ofReal.const_mul _)
      _ = ∑ t : P → ZMod N, ζ ^ (q * ∑ p, t p).val *
          (Z (∑ p, t p) : ℂ) := by
        apply Finset.sum_congr rfl
        intro t _
        rw [integral_const_mul, integral_complex_ofReal, hprops t]
  have hHI :
      (N : ℝ) * (∫ ω, H ω ∂μ) = (m : ℝ) * ∑ k : ZMod N, Z k := by
    rw [hHint]
    exact zn_sum_total p₀ Z
  have hJI :
      (N : ℂ) * (∫ ω, J ω ∂μ) =
        (m : ℂ) * ∑ k : ZMod N, ζ ^ (q * k).val * (Z k : ℂ) := by
    rw [hJint]
    exact zn_sum_total p₀ (fun k : ZMod N => ζ ^ (q * k).val * (Z k : ℂ))
  have hH (ω : Ω) : H ω = R ω * zn_partition N ζ (fun p => T p ω) := by
    dsimp only [H, d, zn_partition]
    rw [Finset.mul_sum]
  have hJ (ω : Ω) :
      J ω = (R ω : ℂ) *
        zn_charged N ζ q (univ : Finset P) (fun p => T p ω) := by
    dsimp only [J, d, zn_charged]
    rw [Finset.mul_sum]
    apply Finset.sum_congr rfl
    intro t _
    simp only [Complex.ofReal_mul]
    ring
  have hpoint (ω : Ω) : ‖J ω‖ ≤ b * H ω := by
    rw [hJ ω, hH ω, norm_mul, Complex.norm_real,
      Real.norm_eq_abs, abs_of_nonneg (hR0 ω)]
    have hc := zn_charged_bound N ζ hζ q (univ : Finset P)
      (fun p => T p ω) κ (fun p => hT p ω) ρ hρ
    simp only [Finset.card_univ] at hc
    calc
      R ω * ‖zn_charged N ζ q univ (fun p => T p ω)‖ ≤
          R ω * (b * zn_partition N ζ (fun p => T p ω)) :=
        mul_le_mul_of_nonneg_left hc (hR0 ω)
      _ = b * (R ω * zn_partition N ζ (fun p => T p ω)) := by ring
  have hbound : ‖∫ ω, J ω ∂μ‖ ≤ b * ∫ ω, H ω ∂μ := by
    calc
      ‖∫ ω, J ω ∂μ‖ ≤ ∫ ω, b * H ω ∂μ :=
        norm_integral_le_of_norm_le (hHi.const_mul b)
          (Filter.Eventually.of_forall hpoint)
      _ = b * ∫ ω, H ω ∂μ := integral_const_mul b H
  have hscaled :
      (m : ℝ) * ‖∑ k : ZMod N, ζ ^ (q * k).val * (Z k : ℂ)‖ ≤
        (m : ℝ) * (b * ∑ k : ZMod N, Z k) := by
    calc
      (m : ℝ) * ‖∑ k : ZMod N, ζ ^ (q * k).val * (Z k : ℂ)‖ =
          ‖(m : ℂ) * ∑ k : ZMod N, ζ ^ (q * k).val * (Z k : ℂ)‖ := by
        rw [norm_mul, Complex.norm_natCast]
      _ = ‖(N : ℂ) * ∫ ω, J ω ∂μ‖ := by rw [hJI]
      _ = (N : ℝ) * ‖∫ ω, J ω ∂μ‖ := by
        rw [norm_mul, Complex.norm_natCast]
      _ ≤ (N : ℝ) * (b * ∫ ω, H ω ∂μ) :=
        mul_le_mul_of_nonneg_left hbound (Nat.cast_nonneg N)
      _ = b * ((N : ℝ) * ∫ ω, H ω ∂μ) := by ring
      _ = (m : ℝ) * (b * ∑ k : ZMod N, Z k) := by
        rw [hHI]
        ring
  have hres := (mul_le_mul_iff_right₀ hm).mp hscaled
  have hZraw (k : ZMod N) :
      Z k =
        ∫ ω, R ω * Real.exp
          (∑ p, ((if p = p₀ then ζ ^ k.val else 1) * T p ω).re) ∂μ := by
    dsimp only [Z, d]
    apply integral_congr_ae
    apply Filter.Eventually.of_forall
    intro ω
    apply congrArg (fun y : ℝ => R ω * Real.exp y)
    apply Finset.sum_congr rfl
    intro p _
    by_cases hp : p = p₀ <;> simp [v, hp]
  simpa only [hZraw] using hres

/-- A3. Crude constant: for a primitive `N`-th root of unity and a non-zero charge `q`, the one-plaquette Fourier
ratio is at most `1 - exp (-2 ‖t‖)`. -/
theorem rho_crude (N : ℕ) [NeZero N] (ζ : ℂ) (hζ : IsPrimitiveRoot ζ N) (q : ZMod N) (hq : q ≠ 0)
    (t : ℂ) :
    ‖∑ j : ZMod N, ζ ^ (q * j).val * ((Real.exp ((ζ ^ j.val * t).re) : ℝ) : ℂ)‖
      ≤ (1 - Real.exp (-2 * ‖t‖)) * ∑ j : ZMod N, Real.exp ((ζ ^ j.val * t).re) := by
  classical
  have hqval : q.val ≠ 0 := by
    intro h
    exact hq ((ZMod.val_eq_zero q).mp h)
  have hzero : (∑ j : ZMod N, ζ ^ (q * j).val) = 0 := by
    let χ : AddChar (ZMod N) ℂ :=
      (AddChar.zmodChar N hζ.pow_eq_one).mulShift q
    have hχ : χ ≠ 1 := by
      apply AddChar.ne_one_iff.mpr
      refine ⟨1, ?_⟩
      change ζ ^ (q * 1).val ≠ 1
      simpa only [mul_one] using
        hζ.pow_ne_one_of_pos_of_lt hqval (ZMod.val_lt q)
    simpa only [χ, AddChar.mulShift_apply, AddChar.zmodChar_apply] using
      AddChar.sum_eq_zero_of_ne_one hχ
  have hnorm (j : ZMod N) : ‖ζ ^ j.val * t‖ = ‖t‖ := by
    rw [norm_mul, zn_norm_pow ζ hζ.pow_eq_one, one_mul]
  have hlo (j : ZMod N) :
      Real.exp (-‖t‖) ≤ Real.exp ((ζ ^ j.val * t).re) := by
    apply Real.exp_le_exp.mpr
    have h := (abs_le.mp (Complex.abs_re_le_norm (ζ ^ j.val * t))).1
    rwa [hnorm j] at h
  have hhi (j : ZMod N) :
      Real.exp ((ζ ^ j.val * t).re) ≤ Real.exp ‖t‖ := by
    apply Real.exp_le_exp.mpr
    have h := Complex.re_le_norm (ζ ^ j.val * t)
    rwa [hnorm j] at h
  have hshift :
      (∑ j : ZMod N, ζ ^ (q * j).val *
          ((Real.exp ((ζ ^ j.val * t).re) : ℝ) : ℂ)) =
        ∑ j : ZMod N, ζ ^ (q * j).val *
          ((Real.exp ((ζ ^ j.val * t).re) - Real.exp (-‖t‖) : ℝ) : ℂ) := by
    simp only [Complex.ofReal_sub, mul_sub, Finset.sum_sub_distrib,
      ← Finset.sum_mul, hzero, zero_mul, sub_zero]
  have hsum :
      (∑ j : ZMod N, Real.exp ((ζ ^ j.val * t).re)) ≤
        (N : ℝ) * Real.exp ‖t‖ := by
    calc
      (∑ j : ZMod N, Real.exp ((ζ ^ j.val * t).re)) ≤
          ∑ _j : ZMod N, Real.exp ‖t‖ :=
        Finset.sum_le_sum (fun j _ => hhi j)
      _ = (N : ℝ) * Real.exp ‖t‖ := by
        simp [ZMod.card, nsmul_eq_mul]
  have hexp :
      Real.exp (-2 * ‖t‖) * Real.exp ‖t‖ = Real.exp (-‖t‖) := by
    rw [← Real.exp_add]
    congr 1
    ring
  have hsub :
      Real.exp (-2 * ‖t‖) *
          (∑ j : ZMod N, Real.exp ((ζ ^ j.val * t).re)) ≤
        (N : ℝ) * Real.exp (-‖t‖) := by
    calc
      Real.exp (-2 * ‖t‖) *
          (∑ j : ZMod N, Real.exp ((ζ ^ j.val * t).re)) ≤
          Real.exp (-2 * ‖t‖) * ((N : ℝ) * Real.exp ‖t‖) :=
        mul_le_mul_of_nonneg_left hsum (Real.exp_pos _).le
      _ = (N : ℝ) * (Real.exp (-2 * ‖t‖) * Real.exp ‖t‖) := by ring
      _ = (N : ℝ) * Real.exp (-‖t‖) := by rw [hexp]
  calc
    ‖∑ j : ZMod N, ζ ^ (q * j).val *
        ((Real.exp ((ζ ^ j.val * t).re) : ℝ) : ℂ)‖ =
        ‖∑ j : ZMod N, ζ ^ (q * j).val *
          ((Real.exp ((ζ ^ j.val * t).re) - Real.exp (-‖t‖) : ℝ) : ℂ)‖ :=
      congrArg norm hshift
    _ ≤ ∑ j : ZMod N, ‖ζ ^ (q * j).val *
        ((Real.exp ((ζ ^ j.val * t).re) - Real.exp (-‖t‖) : ℝ) : ℂ)‖ :=
      norm_sum_le _ _
    _ = ∑ j : ZMod N,
        (Real.exp ((ζ ^ j.val * t).re) - Real.exp (-‖t‖)) := by
      apply Finset.sum_congr rfl
      intro j _
      rw [norm_mul, zn_norm_pow ζ hζ.pow_eq_one, one_mul,
        Complex.norm_real, Real.norm_eq_abs]
      exact abs_of_nonneg (sub_nonneg.mpr (hlo j))
    _ = (∑ j : ZMod N, Real.exp ((ζ ^ j.val * t).re)) -
        (N : ℝ) * Real.exp (-‖t‖) := by
      rw [Finset.sum_sub_distrib]
      simp [ZMod.card, nsmul_eq_mul]
    _ ≤ (1 - Real.exp (-2 * ‖t‖)) *
        ∑ j : ZMod N, Real.exp ((ζ ^ j.val * t).re) := by
      nlinarith [hsub]

/-- A4. The case `N = 2`, `ζ = -1`, `q = 1`: the constant is `tanh ‖t‖`. -/
theorem rho_two (t : ℂ) :
    ‖∑ j : ZMod 2, (-1 : ℂ) ^ ((1 : ZMod 2) * j).val * ((Real.exp (((-1 : ℂ) ^ j.val * t).re) : ℝ) : ℂ)‖
      ≤ Real.tanh ‖t‖ * ∑ j : ZMod 2, Real.exp (((-1 : ℂ) ^ j.val * t).re) := by
  have hc :
      (∑ j : ZMod 2, (-1 : ℂ) ^ ((1 : ZMod 2) * j).val *
          ((Real.exp (((-1 : ℂ) ^ j.val * t).re) : ℝ) : ℂ)) =
        ((Real.exp t.re - Real.exp (-t.re) : ℝ) : ℂ) := by
    rw [zn_sum_two]
    norm_num [sub_eq_add_neg, ZMod.val_one_eq_one_mod]
  have hd :
      (∑ j : ZMod 2, Real.exp (((-1 : ℂ) ^ j.val * t).re)) =
        Real.exp t.re + Real.exp (-t.re) := by
    rw [zn_sum_two]
    norm_num [ZMod.val_one_eq_one_mod]
  have he :
      Real.exp t.re - Real.exp (-t.re) =
        Real.tanh t.re * (Real.exp t.re + Real.exp (-t.re)) := by
    rw [Real.tanh_eq]
    exact (div_mul_cancel₀ _
      (add_pos (Real.exp_pos t.re) (Real.exp_pos (-t.re))).ne').symm
  rw [hc, hd, Complex.norm_real, Real.norm_eq_abs, he, abs_mul,
    abs_of_pos (add_pos (Real.exp_pos t.re) (Real.exp_pos (-t.re)))]
  exact mul_le_mul_of_nonneg_right
    (zn_abs_tanh_le (Complex.abs_re_le_norm t))
    (add_pos (Real.exp_pos t.re) (Real.exp_pos (-t.re))).le

/-- A5. Sharpness: on `ZMod N` with the uniform probability measure, translations preserve the measure, the coupling
`j ↦ ζ ^ j * t` and the observable `j ↦ ζ ^ (q * j)` have the covariances required by A1 (one plaquette, charge of a
translation by `s` equal to `s`, coupling of norm `‖t‖`, observable of norm one), and the two integrals are exactly
the normalised Fourier sums of A1's hypothesis: A1 is an equality here with `ρ` the ratio at `t`. -/
theorem sharp_one_plaquette (N : ℕ) [NeZero N] (ζ : ℂ) (hζ : ζ ^ N = 1) (q : ZMod N) (t : ℂ) :
    ∃ μ : Measure (ZMod N), IsProbabilityMeasure μ ∧
      (∀ s : ZMod N, MeasurePreserving (fun j : ZMod N => s + j) μ μ) ∧
      (∀ j : ZMod N, ‖ζ ^ j.val * t‖ = ‖t‖) ∧ (∀ j : ZMod N, ‖ζ ^ (q * j).val‖ = 1) ∧
      (∀ s j : ZMod N, ζ ^ (s + j).val * t = ζ ^ s.val * (ζ ^ j.val * t)) ∧
      (∀ s j : ZMod N, ζ ^ (q * (s + j)).val = ζ ^ (q * s).val * ζ ^ (q * j).val) ∧
      (∫ j, ζ ^ (q * j).val * ((Real.exp ((ζ ^ j.val * t).re) : ℝ) : ℂ) ∂μ)
          = (N : ℂ)⁻¹ * ∑ j : ZMod N, ζ ^ (q * j).val * ((Real.exp ((ζ ^ j.val * t).re) : ℝ) : ℂ) ∧
      (∫ j, Real.exp ((ζ ^ j.val * t).re) ∂μ) = (N : ℝ)⁻¹ * ∑ j : ZMod N, Real.exp ((ζ ^ j.val * t).re) := by
  classical
  let u : PMF (ZMod N) := PMF.uniformOfFintype (ZMod N)
  refine ⟨u.toMeasure, inferInstance, ?_, ?_, ?_, ?_, ?_, ?_, ?_⟩
  · intro s
    have hm : Measurable (fun j : ZMod N => s + j) :=
      measurable_of_countable _
    have hu : u.map (fun j : ZMod N => s + j) = u := by
      ext j
      rw [PMF.map_apply]
      rw [tsum_eq_single (-s + j)]
      · simp [u, ← add_assoc]
      · intro a ha
        have hne : j ≠ s + a := by
          intro h
          apply ha
          rw [h]
          abel
        simp [hne]
    refine ⟨hm, ?_⟩
    rw [PMF.toMeasure_map (fun j : ZMod N => s + j) u hm, hu]
  · intro j
    rw [norm_mul, zn_norm_pow ζ hζ, one_mul]
  · intro j
    exact zn_norm_pow ζ hζ (q * j)
  · intro s j
    rw [zn_pow_add ζ hζ, mul_assoc]
  · intro s j
    rw [mul_add, zn_pow_add ζ hζ]
  · simp only [PMF.integral_eq_sum, u, PMF.uniformOfFintype_apply,
      ZMod.card, ENNReal.toReal_inv, ENNReal.toReal_natCast,
      Complex.real_smul, Complex.ofReal_inv, Complex.ofReal_natCast]
    rw [← Finset.mul_sum]
  · simp only [PMF.integral_eq_sum, u, PMF.uniformOfFintype_apply,
      ZMod.card, ENNReal.toReal_inv, ENNReal.toReal_natCast, smul_eq_mul]
    rw [← Finset.mul_sum]

/-- A6a. A1 with the crude constant (primitive root, non-zero charge). -/
theorem centre_flip_bound_crude
    {Ω S P : Type*} [MeasurableSpace Ω] [Fintype P] [DecidableEq P]
    (N : ℕ) [NeZero N] (ζ : ℂ) (hζ : IsPrimitiveRoot ζ N)
    (μ : Measure Ω) [IsProbabilityMeasure μ]
    (τ : S → Ω → Ω) (hτ : ∀ s, MeasurePreserving (τ s) μ μ)
    (chg : S → P → ZMod N) (hsurj : Function.Surjective chg)
    (T : P → Ω → ℂ) (hTm : ∀ p, Measurable (T p))
    (κ : ℝ) (hT : ∀ p ω, ‖T p ω‖ ≤ κ)
    (hTτ : ∀ s p ω, T p (τ s ω) = ζ ^ (chg s p).val * T p ω)
    (R : Ω → ℝ) (hRm : Measurable R) (hR0 : ∀ ω, 0 ≤ R ω) (hRτ : ∀ s ω, R (τ s ω) = R ω)
    (hRint : Integrable (fun ω => R ω * Real.exp (∑ p, (T p ω).re)) μ)
    (W : Ω → ℂ) (hWm : Measurable W) (hW1 : ∀ ω, ‖W ω‖ ≤ 1)
    (q : ZMod N) (hq : q ≠ 0) (A : Finset P)
    (hWτ : ∀ s ω, W (τ s ω) = ζ ^ (q * ∑ p ∈ A, chg s p).val * W ω) :
    ‖∫ ω, W ω * ((R ω * Real.exp (∑ p, (T p ω).re) : ℝ) : ℂ) ∂μ‖
      ≤ (1 - Real.exp (-2 * κ)) ^ A.card * ∫ ω, R ω * Real.exp (∑ p, (T p ω).re) ∂μ := by
  apply centre_flip_bound N ζ hζ.pow_eq_one μ τ hτ chg hsurj
    T hTm κ hT hTτ R hRm hR0 hRτ hRint W hWm hW1 q A hWτ
    (1 - Real.exp (-2 * κ))
  intro t ht
  apply (rho_crude N ζ hζ q hq t).trans
  apply mul_le_mul_of_nonneg_right
    _ (Finset.sum_nonneg (fun j _ => (Real.exp_pos _).le))
  have he : Real.exp (-2 * κ) ≤ Real.exp (-2 * ‖t‖) :=
    Real.exp_le_exp.mpr (by linarith)
  linarith

/-- A6b. A2 with the crude constant (primitive root, non-zero charge). -/
theorem twist_ratio_bound_crude
    {Ω S P : Type*} [MeasurableSpace Ω] [Fintype P] [DecidableEq P]
    (N : ℕ) [NeZero N] (ζ : ℂ) (hζ : IsPrimitiveRoot ζ N)
    (μ : Measure Ω) [IsProbabilityMeasure μ]
    (τ : S → Ω → Ω) (hτ : ∀ s, MeasurePreserving (τ s) μ μ)
    (chg : S → P → ZMod N)
    (himg : ∀ t : P → ZMod N, ∑ p, t p = 0 → ∃ s, chg s = t)
    (T : P → Ω → ℂ) (hTm : ∀ p, Measurable (T p))
    (κ : ℝ) (hT : ∀ p ω, ‖T p ω‖ ≤ κ)
    (hTτ : ∀ s p ω, T p (τ s ω) = ζ ^ (chg s p).val * T p ω)
    (R : Ω → ℝ) (hRm : Measurable R) (hR0 : ∀ ω, 0 ≤ R ω) (hRτ : ∀ s ω, R (τ s ω) = R ω)
    (hRint : Integrable (fun ω => R ω * Real.exp (∑ p, (T p ω).re)) μ)
    (q : ZMod N) (hq : q ≠ 0) (p₀ : P) :
    ‖∑ k : ZMod N, ζ ^ (q * k).val *
        ((∫ ω, R ω * Real.exp (∑ p, ((if p = p₀ then ζ ^ k.val else 1) * T p ω).re) ∂μ : ℝ) : ℂ)‖
      ≤ (1 - Real.exp (-2 * κ)) ^ Fintype.card P *
        ∑ k : ZMod N, ∫ ω, R ω * Real.exp (∑ p, ((if p = p₀ then ζ ^ k.val else 1) * T p ω).re) ∂μ := by
  apply twist_ratio_bound N ζ hζ.pow_eq_one μ τ hτ chg himg
    T hTm κ hT hTτ R hRm hR0 hRτ hRint q
    (1 - Real.exp (-2 * κ)) _ p₀
  intro t ht
  apply (rho_crude N ζ hζ q hq t).trans
  apply mul_le_mul_of_nonneg_right
    _ (Finset.sum_nonneg (fun j _ => (Real.exp_pos _).le))
  have he : Real.exp (-2 * κ) ≤ Real.exp (-2 * ‖t‖) :=
    Real.exp_le_exp.mpr (by linarith)
  linarith

/-- A7a. `N = 2` recovers the published column-flip bound (statement of `TubeArea.column_flip_bound`, verbatim, as
restated in its verification footer); to be derived from A1 and A4. -/
theorem recover_column_flip_bound
    {Ω E P : Type*} [MeasurableSpace Ω] [Fintype E] [DecidableEq E] [Fintype P] [DecidableEq P]
    (μ : Measure Ω) [IsProbabilityMeasure μ]
    (τ : (E → ℤˣ) → Ω → Ω) (hτ : ∀ σ, MeasurePreserving (τ σ) μ μ)
    (bd : P → Finset E)
    (hsurj : Function.Surjective (fun σ : E → ℤˣ => ((fun p => ∏ e ∈ bd p, σ e) : P → ℤˣ)))
    (K : P → Ω → ℝ) (hKm : ∀ p, Measurable (K p))
    (κ : ℝ) (hK : ∀ p ω, |K p ω| ≤ κ)
    (hKτ : ∀ σ p ω, K p (τ σ ω) = (((∏ e ∈ bd p, σ e : ℤˣ) : ℤ) : ℝ) * K p ω)
    (R : Ω → ℝ) (hRm : Measurable R) (hR0 : ∀ ω, 0 ≤ R ω) (hRτ : ∀ σ ω, R (τ σ ω) = R ω)
    (hRint : Integrable (fun ω => R ω * Real.exp (∑ p, K p ω)) μ)
    (W : Ω → ℝ) (hWm : Measurable W) (hW1 : ∀ ω, |W ω| ≤ 1)
    (A : Finset P)
    (hWτ : ∀ σ ω, W (τ σ ω) = (((∏ p ∈ A, ∏ e ∈ bd p, σ e : ℤˣ) : ℤ) : ℝ) * W ω) :
    |∫ ω, W ω * (R ω * Real.exp (∑ p, K p ω)) ∂μ|
      ≤ Real.tanh κ ^ A.card * ∫ ω, R ω * Real.exp (∑ p, K p ω) ∂μ := by
  classical
  let chg : (E → ℤˣ) → P → ZMod 2 :=
    fun σ p => zn_charge (∏ e ∈ bd p, σ e)
  let T : P → Ω → ℂ := fun p ω => (K p ω : ℂ)
  have hcs : Function.Surjective chg := by
    intro t
    obtain ⟨σ, hσ⟩ := hsurj (fun p => zn_sign (t p))
    refine ⟨σ, ?_⟩
    funext p
    change zn_charge (∏ e ∈ bd p, σ e) = t p
    have hσp : (∏ e ∈ bd p, σ e) = zn_sign (t p) := congrFun hσ p
    rw [hσp]
    exact zn_charge_sign (t p)
  have hTm (p : P) : Measurable (T p) := by
    dsimp only [T]
    fun_prop
  have hT (p : P) (ω : Ω) : ‖T p ω‖ ≤ κ := by
    simpa only [T, Complex.norm_real, Real.norm_eq_abs] using hK p ω
  have hTτ (σ : E → ℤˣ) (p : P) (ω : Ω) :
      T p (τ σ ω) = (-1 : ℂ) ^ (chg σ p).val * T p ω := by
    dsimp only [T, chg]
    rw [hKτ σ p ω, Complex.ofReal_mul, zn_cast_charge]
  have hRi :
      Integrable (fun ω => R ω * Real.exp (∑ p, (T p ω).re)) μ := by
    simpa only [T, Complex.ofReal_re] using hRint
  have hWmc : Measurable (fun ω => (W ω : ℂ)) := by
    fun_prop
  have hW1c (ω : Ω) : ‖(W ω : ℂ)‖ ≤ 1 := by
    simpa only [Complex.norm_real, Real.norm_eq_abs] using hW1 ω
  have hWτc (σ : E → ℤˣ) (ω : Ω) :
      (W (τ σ ω) : ℂ) =
        (-1 : ℂ) ^ ((1 : ZMod 2) * ∑ p ∈ A, chg σ p).val *
          (W ω : ℂ) := by
    dsimp only [chg]
    rw [hWτ σ ω, Complex.ofReal_mul]
    simp only [one_mul]
    rw [← zn_charge_prod A (fun p => ∏ e ∈ bd p, σ e),
      ← zn_cast_charge]
  have hρ :
      ∀ t : ℂ, ‖t‖ ≤ κ →
        ‖∑ j : ZMod 2, (-1 : ℂ) ^ ((1 : ZMod 2) * j).val *
            ((Real.exp (((-1 : ℂ) ^ j.val * t).re) : ℝ) : ℂ)‖ ≤
          Real.tanh κ *
            ∑ j : ZMod 2, Real.exp (((-1 : ℂ) ^ j.val * t).re) := by
    intro t ht
    exact (rho_two t).trans
      (mul_le_mul_of_nonneg_right (zn_tanh_mono ht)
        (Finset.sum_nonneg (fun j _ => (Real.exp_pos _).le)))
  have h := centre_flip_bound 2 (-1 : ℂ) (by norm_num)
    μ τ hτ chg hcs T hTm κ hT hTτ R hRm hR0 hRτ hRi
    (fun ω => (W ω : ℂ)) hWmc hW1c (1 : ZMod 2) A hWτc
    (Real.tanh κ) hρ
  simpa only [T, Complex.ofReal_re, ← Complex.ofReal_mul,
    integral_complex_ofReal, Complex.norm_real, Real.norm_eq_abs] using h

/-- A7b. `N = 2` recovers the published twist-ratio bound (statement of `TubeArea.twist_ratio_bound`, verbatim, as
restated in its verification footer); to be derived from A2 and A4. -/
theorem recover_twist_ratio_bound
    {Ω E P : Type*} [MeasurableSpace Ω] [Fintype E] [DecidableEq E] [Fintype P] [DecidableEq P]
    (μ : Measure Ω) [IsProbabilityMeasure μ]
    (τ : (E → ℤˣ) → Ω → Ω) (hτ : ∀ σ, MeasurePreserving (τ σ) μ μ)
    (bd : P → Finset E)
    (hpar : ∀ σ : E → ℤˣ, ∏ p, (∏ e ∈ bd p, σ e) = 1)
    (himg : ∀ t : P → ℤˣ, ∏ p, t p = 1 → ∃ σ : E → ℤˣ, ∀ p, ∏ e ∈ bd p, σ e = t p)
    (K : P → Ω → ℝ) (hKm : ∀ p, Measurable (K p))
    (κ : ℝ) (hK : ∀ p ω, |K p ω| ≤ κ)
    (hKτ : ∀ σ p ω, K p (τ σ ω) = (((∏ e ∈ bd p, σ e : ℤˣ) : ℤ) : ℝ) * K p ω)
    (R : Ω → ℝ) (hRm : Measurable R) (hR0 : ∀ ω, 0 ≤ R ω) (hRτ : ∀ σ ω, R (τ σ ω) = R ω)
    (hRint : Integrable (fun ω => R ω * Real.exp (∑ p, K p ω)) μ)
    (p₀ : P) :
    |(∫ ω, R ω * Real.exp (∑ p, K p ω) ∂μ)
        - ∫ ω, R ω * Real.exp (∑ p, (if p = p₀ then -(K p ω) else K p ω)) ∂μ|
      ≤ Real.tanh κ ^ Fintype.card P *
        ((∫ ω, R ω * Real.exp (∑ p, K p ω) ∂μ)
          + ∫ ω, R ω * Real.exp (∑ p, (if p = p₀ then -(K p ω) else K p ω)) ∂μ) := by
  classical
  let chg : (E → ℤˣ) → P → ZMod 2 :=
    fun σ p => zn_charge (∏ e ∈ bd p, σ e)
  let T : P → Ω → ℂ := fun p ω => (K p ω : ℂ)
  have hci :
      ∀ t : P → ZMod 2, ∑ p, t p = 0 → ∃ σ, chg σ = t := by
    intro t ht
    have hp : ∏ p, zn_sign (t p) = 1 := by
      rw [← zn_sign_sum (univ : Finset P) t, ht]
      simp [zn_sign]
    obtain ⟨σ, hσ⟩ := himg (fun p => zn_sign (t p)) hp
    refine ⟨σ, ?_⟩
    funext p
    change zn_charge (∏ e ∈ bd p, σ e) = t p
    rw [hσ p]
    exact zn_charge_sign (t p)
  have hTm (p : P) : Measurable (T p) := by
    dsimp only [T]
    fun_prop
  have hT (p : P) (ω : Ω) : ‖T p ω‖ ≤ κ := by
    simpa only [T, Complex.norm_real, Real.norm_eq_abs] using hK p ω
  have hTτ (σ : E → ℤˣ) (p : P) (ω : Ω) :
      T p (τ σ ω) = (-1 : ℂ) ^ (chg σ p).val * T p ω := by
    dsimp only [T, chg]
    rw [hKτ σ p ω, Complex.ofReal_mul, zn_cast_charge]
  have hRi :
      Integrable (fun ω => R ω * Real.exp (∑ p, (T p ω).re)) μ := by
    simpa only [T, Complex.ofReal_re] using hRint
  have hρ :
      ∀ t : ℂ, ‖t‖ ≤ κ →
        ‖∑ j : ZMod 2, (-1 : ℂ) ^ ((1 : ZMod 2) * j).val *
            ((Real.exp (((-1 : ℂ) ^ j.val * t).re) : ℝ) : ℂ)‖ ≤
          Real.tanh κ *
            ∑ j : ZMod 2, Real.exp (((-1 : ℂ) ^ j.val * t).re) := by
    intro t ht
    exact (rho_two t).trans
      (mul_le_mul_of_nonneg_right (zn_tanh_mono ht)
        (Finset.sum_nonneg (fun j _ => (Real.exp_pos _).le)))
  have h := twist_ratio_bound 2 (-1 : ℂ) (by norm_num)
    μ τ hτ chg hci T hTm κ hT hTτ R hRm hR0 hRτ hRi
    (1 : ZMod 2) (Real.tanh κ) hρ p₀
  let Z : ZMod 2 → ℝ := fun k =>
    ∫ ω, R ω * Real.exp
      (∑ p, ((if p = p₀ then (-1 : ℂ) ^ k.val else 1) * T p ω).re) ∂μ
  change
    ‖∑ k : ZMod 2, (-1 : ℂ) ^ ((1 : ZMod 2) * k).val * (Z k : ℂ)‖ ≤
      Real.tanh κ ^ Fintype.card P * ∑ k : ZMod 2, Z k at h
  have hF :
      (∑ k : ZMod 2, (-1 : ℂ) ^ ((1 : ZMod 2) * k).val * (Z k : ℂ)) =
        ((Z 0 - Z 1 : ℝ) : ℂ) := by
    rw [zn_sum_two]
    norm_num [Complex.ofReal_sub, sub_eq_add_neg, ZMod.val_one_eq_one_mod]
  have hS : (∑ k : ZMod 2, Z k) = Z 0 + Z 1 := zn_sum_two Z
  have hz0 :
      Z 0 = ∫ ω, R ω * Real.exp (∑ p, K p ω) ∂μ := by
    dsimp only [Z, T]
    simp
  have hz1 :
      Z 1 = ∫ ω, R ω * Real.exp
        (∑ p, if p = p₀ then -(K p ω) else K p ω) ∂μ := by
    dsimp only [Z, T]
    apply integral_congr_ae
    apply Filter.Eventually.of_forall
    intro ω
    apply congrArg (fun y : ℝ => R ω * Real.exp y)
    apply Finset.sum_congr rfl
    intro p _
    by_cases hp : p = p₀ <;> simp [hp, ZMod.val_one_eq_one_mod]
  rw [hF, hS, Complex.norm_real, Real.norm_eq_abs] at h
  simpa only [hz0, hz1] using h

end CentreZN

end

noncomputable section

namespace CentreZN

/-! ## Partie B : théorie de type Wilson à élément central d'ordre `N` (définitions figées) -/

/-- Configurations: long links `(e, y)` (base edge `e`, fibre site `y`) and other links `x`. -/
abbrev Config (G E F X : Type*) := ((E × F) → G) × (X → G)

/-- The product of the single-link measure over all links. -/
def configMeasure {G E F X : Type*} [MeasurableSpace G] [Fintype E] [Fintype F] [Fintype X]
    (haarG : Measure G) : Measure (Config G E F X) :=
  (Measure.pi fun _ : E × F => haarG).prod (Measure.pi fun _ : X => haarG)

/-- Column twist: every long link `(e, y)` is left-multiplied by `z ^ (σ e).val`; other links are unchanged. -/
def columnTwist {G E F X : Type*} [Monoid G] {N : ℕ} (z : G) (σ : E → ZMod N)
    (ω : Config G E F X) : Config G E F X :=
  (fun ey => z ^ (σ ey.1).val * ω.1 ey, ω.2)

/-- Positive orientation: the link itself; negative orientation: its inverse. -/
def orientedLink {G : Type*} [Inv G] : Bool → G → G
  | true, g => g
  | false, g => g⁻¹

/-- A word: a list of oriented letters, each a long link `Sum.inl (e, y)` or another link `Sum.inr x`. -/
abbrev Word (E F X : Type*) := List (((E × F) ⊕ X) × Bool)

/-- Ordered holonomy of a word (empty word: `1`). -/
def holonomy {G E F X : Type*} [Group G] : Word E F X → Config G E F X → G
  | [], _ => 1
  | (Sum.inl ey, b) :: w, ω => orientedLink b (ω.1 ey) * holonomy w ω
  | (Sum.inr x, b) :: w, ω => orientedLink b (ω.2 x) * holonomy w ω

/-- Charge of a word: signed sum (with multiplicity) of the column variables of its long letters. -/
def charge {E F X : Type*} {N : ℕ} : Word E F X → (E → ZMod N) → ZMod N
  | [], _ => 0
  | (Sum.inl ey, b) :: w, σ => (if b then σ ey.1 else -σ ey.1) + charge w σ
  | (Sum.inr _, _) :: w, σ => charge w σ

/-- A word is neutral for `ZMod N` when its charge vanishes for all column variables. -/
def Neutral {E F X : Type*} (N : ℕ) (w : Word E F X) : Prop :=
  ∀ σ : E → ZMod N, charge w σ = 0

/-- The word of a base path (list of oriented base edges) at the fibre site `y`. -/
def baseWord {E F X : Type*} (w : List (E × Bool)) (y : F) : Word E F X :=
  w.map fun a => (Sum.inl (a.1, y), a.2)

/-- Charge of a base path: signed sum (with multiplicity) of the column variables along it. -/
def baseCharge {E : Type*} {N : ℕ} : List (E × Bool) → (E → ZMod N) → ZMod N
  | [], _ => 0
  | a :: w, σ => (if a.2 then σ a.1 else -σ a.1) + baseCharge w σ

/-- Complex Wilson coupling of the base plaquette `p`: `β Σ_y c p y χ(holonomy of its word at y)`.
The action uses its real part. -/
def coupling {G E F X P : Type*} [Group G] [Fintype F]
    (β : ℝ) (c : P → F → ℂ) (chi : G → ℂ) (w : P → List (E × Bool)) (p : P)
    (ω : Config G E F X) : ℂ :=
  (β : ℂ) * ∑ y, c p y * chi (holonomy (baseWord (w p) y) ω)

/-- Weight of a finite family of extra terms: `exp (Σ_k Re (coef k · χ(holonomy of the word k)))`. -/
def termsWeight {G E F X Q : Type*} [Group G] [Fintype Q]
    (chi : G → ℂ) (wq : Q → Word E F X) (coef : Q → ℂ) (ω : Config G E F X) : ℝ :=
  Real.exp (∑ k, (coef k * chi (holonomy (wq k) ω)).re)

/-- Edges of the discrete torus `(ℤ/m) × (ℤ/n)`: `Sum.inl (i,j)` is the horizontal edge from `(i,j)` to `(i+1,j)`,
`Sum.inr (i,j)` the vertical edge from `(i,j)` to `(i,j+1)`; indices are cyclic (`finRotate`). -/
abbrev TorusEdge (m n : ℕ) := (Fin m × Fin n) ⊕ (Fin m × Fin n)

/-- Counterclockwise plaquette path from the corner `p = (i,j)`: bottom `H(i,j)` forwards, right `V(i+1,j)`
forwards, top `H(i,j+1)` backwards, left `V(i,j)` backwards. -/
def torusWord {m n : ℕ} (p : Fin m × Fin n) : List (TorusEdge m n × Bool) :=
  [(Sum.inl (p.1, p.2), true), (Sum.inr (finRotate m p.1, p.2), true),
    (Sum.inl (p.1, finRotate n p.2), false), (Sum.inr (p.1, p.2), false)]

end CentreZN

end

noncomputable section

namespace CentreZN

lemma znb_pow_add {M : Type*} [Monoid M] {N : ℕ} [NeZero N]
    (z : M) (hzN : z ^ N = 1) (a b : ZMod N) :
    z ^ (a + b).val = z ^ a.val * z ^ b.val := by
  rw [ZMod.val_add, ← pow_eq_pow_mod (a.val + b.val) hzN, pow_add]

lemma znb_pow_mul {M : Type*} [Monoid M] {N : ℕ}
    (z : M) (hzN : z ^ N = 1) (a b : ZMod N) :
    (z ^ a.val) ^ b.val = z ^ (a * b).val := by
  rw [← pow_mul, ZMod.val_mul]
  exact pow_eq_pow_mod _ hzN

lemma znb_pow_neg {G : Type*} [Group G] {N : ℕ} [NeZero N]
    (z : G) (hzN : z ^ N = 1) (a : ZMod N) :
    z ^ (-a).val = (z ^ a.val)⁻¹ := by
  apply eq_inv_of_mul_eq_one_left
  rw [← znb_pow_add z hzN, neg_add_cancel, ZMod.val_zero, pow_zero]

lemma znb_pow_central {G : Type*} [Monoid G]
    (z : G) (hcentral : ∀ g : G, z * g = g * z) (k : ℕ) (g : G) :
    z ^ k * g = g * z ^ k := by
  exact ((show Commute z g from hcentral g).pow_left k).eq

lemma znb_character_pow {G : Type*} [Group G]
    (z : G) (chi : G → ℂ) (η : ℂ)
    (hchi : ∀ g, chi (z * g) = η * chi g) (k : ℕ) (g : G) :
    chi (z ^ k * g) = η ^ k * chi g := by
  induction k with
  | zero => simp
  | succ k ih =>
    calc
      chi (z ^ (k + 1) * g) = η * chi (z ^ k * g) := by
        rw [pow_succ', mul_assoc, hchi]
      _ = η ^ (k + 1) * chi g := by
        rw [ih, pow_succ', mul_assoc]

lemma znb_oriented_twist {G : Type*} [Group G] {N : ℕ} [NeZero N]
    (z : G) (hzN : z ^ N = 1) (hcentral : ∀ g : G, z * g = g * z)
    (b : Bool) (a : ZMod N) (g : G) :
    orientedLink b (z ^ a.val * g) =
      z ^ (if b then a else -a).val * orientedLink b g := by
  cases b with
  | false =>
    change (z ^ a.val * g)⁻¹ = z ^ (-a).val * g⁻¹
    rw [mul_inv_rev, ← znb_pow_neg z hzN a]
    exact (znb_pow_central z hcentral (-a).val g⁻¹).symm
  | true => rfl

lemma znb_holonomy_twist {G E F X : Type*} [Group G] {N : ℕ} [NeZero N]
    (z : G) (hzN : z ^ N = 1) (hcentral : ∀ g : G, z * g = g * z)
    (w : Word E F X) (σ : E → ZMod N) (ω : Config G E F X) :
    holonomy w (columnTwist z σ ω) =
      z ^ (charge w σ).val * holonomy w ω := by
  induction w with
  | nil => simp [holonomy, charge]
  | cons a w ih =>
    rcases a with ⟨l, b⟩
    cases l with
    | inl ey =>
      change orientedLink b (z ^ (σ ey.1).val * ω.1 ey) *
          holonomy w (columnTwist z σ ω) =
        z ^ ((if b then σ ey.1 else -σ ey.1) + charge w σ).val *
          (orientedLink b (ω.1 ey) * holonomy w ω)
      rw [znb_oriented_twist z hzN hcentral, ih, znb_pow_add z hzN]
      calc
        (z ^ (if b then σ ey.1 else -σ ey.1).val * orientedLink b (ω.1 ey)) *
            (z ^ (charge w σ).val * holonomy w ω) =
          z ^ (if b then σ ey.1 else -σ ey.1).val *
            ((orientedLink b (ω.1 ey) * z ^ (charge w σ).val) *
              holonomy w ω) := by
                simp only [mul_assoc]
        _ = z ^ (if b then σ ey.1 else -σ ey.1).val *
            ((z ^ (charge w σ).val * orientedLink b (ω.1 ey)) *
              holonomy w ω) := by
                rw [← znb_pow_central z hcentral (charge w σ).val
                  (orientedLink b (ω.1 ey))]
        _ = (z ^ (if b then σ ey.1 else -σ ey.1).val *
              z ^ (charge w σ).val) *
            (orientedLink b (ω.1 ey) * holonomy w ω) := by
                simp only [mul_assoc]
    | inr x =>
      change orientedLink b (ω.2 x) * holonomy w (columnTwist z σ ω) =
        z ^ (charge w σ).val * (orientedLink b (ω.2 x) * holonomy w ω)
      rw [ih]
      calc
        orientedLink b (ω.2 x) * (z ^ (charge w σ).val * holonomy w ω) =
          (orientedLink b (ω.2 x) * z ^ (charge w σ).val) *
            holonomy w ω := by
              simp only [mul_assoc]
        _ = (z ^ (charge w σ).val * orientedLink b (ω.2 x)) *
            holonomy w ω := by
              rw [← znb_pow_central z hcentral (charge w σ).val
                (orientedLink b (ω.2 x))]
        _ = z ^ (charge w σ).val *
            (orientedLink b (ω.2 x) * holonomy w ω) := by
              simp only [mul_assoc]

lemma znb_charge_base {E F X : Type*} {N : ℕ}
    (w : List (E × Bool)) (y : F) (σ : E → ZMod N) :
    charge (baseWord w y : Word E F X) σ = baseCharge w σ := by
  induction w with
  | nil => rfl
  | cons a w ih =>
    change (if a.2 then σ a.1 else -σ a.1) + charge (baseWord w y : Word E F X) σ =
      (if a.2 then σ a.1 else -σ a.1) + baseCharge w σ
    rw [ih]

lemma znb_columnTwist_preserving {G E F X : Type*} [Group G] [MeasurableSpace G]
    [Fintype E] [Fintype F] [Fintype X] {N : ℕ}
    (haarG : Measure G) [IsProbabilityMeasure haarG]
    (hleft : ∀ g : G, MeasurePreserving (fun h : G => g * h) haarG haarG)
    (z : G) (σ : E → ZMod N) :
    MeasurePreserving (columnTwist z σ : Config G E F X → Config G E F X)
      (configMeasure haarG) (configMeasure haarG) := by
  have hU := measurePreserving_pi
    (fun _ : E × F => haarG) (fun _ : E × F => haarG)
    (fun ey => hleft (z ^ (σ ey.1).val))
  have hV := MeasurePreserving.id (Measure.pi fun _ : X => haarG)
  have hmap : (columnTwist z σ : Config G E F X → Config G E F X) =
      Prod.map (fun U : E × F → G => fun ey => z ^ (σ ey.1).val * U ey)
        (id : (X → G) → (X → G)) := by
    funext ω
    rcases ω with ⟨U, V⟩
    rfl
  rw [hmap]
  exact hU.prod hV

lemma znb_measurable_orientedLink {G : Type*} [Group G] [MeasurableSpace G]
    [MeasurableInv G] (b : Bool) :
    Measurable (orientedLink b : G → G) := by
  cases b with
  | false => exact measurable_inv
  | true => exact measurable_id

lemma znb_measurable_holonomy {G E F X : Type*} [Group G] [MeasurableSpace G]
    [MeasurableMul₂ G] [MeasurableInv G] (w : Word E F X) :
    Measurable (holonomy w : Config G E F X → G) := by
  induction w with
  | nil => exact measurable_const
  | cons a w ih =>
    rcases a with ⟨l, b⟩
    cases l with
    | inl ey =>
      exact ((znb_measurable_orientedLink b).comp
        ((measurable_pi_apply ey).comp measurable_fst)).mul ih
    | inr x =>
      exact ((znb_measurable_orientedLink b).comp
        ((measurable_pi_apply x).comp measurable_snd)).mul ih

lemma znb_measurable_coupling {G E F X P : Type*} [Group G] [MeasurableSpace G]
    [MeasurableMul₂ G] [MeasurableInv G] [Fintype F]
    (β : ℝ) (c : P → F → ℂ) (chi : G → ℂ) (hchim : Measurable chi)
    (w : P → List (E × Bool)) (p : P) :
    Measurable (coupling β c chi w p : Config G E F X → ℂ) := by
  exact (Finset.measurable_sum univ (fun y _ =>
    (hchim.comp (znb_measurable_holonomy (baseWord (w p) y))).const_mul
      (c p y))).const_mul (β : ℂ)

lemma znb_coupling_bound {G E F X P : Type*} [Group G] [Fintype F]
    (β : ℝ) (hβ : 0 ≤ β) (c : P → F → ℂ) (hc : ∀ p y, ‖c p y‖ ≤ 1)
    (chi : G → ℂ) (hchi1 : ∀ g, ‖chi g‖ ≤ 1) (w : P → List (E × Bool))
    (p : P) (ω : Config G E F X) :
    ‖coupling β c chi w p ω‖ ≤ β * (Fintype.card F : ℝ) := by
  unfold coupling
  rw [norm_mul, Complex.norm_real, Real.norm_of_nonneg hβ]
  apply mul_le_mul_of_nonneg_left _ hβ
  calc
    ‖∑ y, c p y * chi (holonomy (baseWord (w p) y) ω)‖ ≤
        ∑ y, ‖c p y * chi (holonomy (baseWord (w p) y) ω)‖ :=
      norm_sum_le _ _
    _ ≤ ∑ _y : F, (1 : ℝ) := by
      apply Finset.sum_le_sum
      intro y _
      rw [norm_mul]
      calc
        ‖c p y‖ * ‖chi (holonomy (baseWord (w p) y) ω)‖ ≤
            1 * ‖chi (holonomy (baseWord (w p) y) ω)‖ :=
          mul_le_mul_of_nonneg_right (hc p y) (norm_nonneg _)
        _ ≤ 1 := by
          simpa using hchi1 (holonomy (baseWord (w p) y) ω)
    _ = (Fintype.card F : ℝ) := by simp

lemma znb_coupling_twist {G E F X P : Type*} [Group G] [Fintype F]
    {N : ℕ} [NeZero N]
    (z : G) (hzN : z ^ N = 1) (hcentral : ∀ g : G, z * g = g * z)
    (β : ℝ) (c : P → F → ℂ) (chi : G → ℂ) (ζ : ℂ)
    (hchiz : ∀ g, chi (z * g) = ζ * chi g)
    (w : P → List (E × Bool)) (σ : E → ZMod N) (p : P)
    (ω : Config G E F X) :
    coupling β c chi w p (columnTwist z σ ω) =
      ζ ^ (baseCharge (w p) σ).val * coupling β c chi w p ω := by
  have hchar (y : F) :
      chi (holonomy (baseWord (w p) y) (columnTwist z σ ω)) =
        ζ ^ (baseCharge (w p) σ).val *
          chi (holonomy (baseWord (w p) y) ω) := by
    rw [znb_holonomy_twist z hzN hcentral, znb_charge_base,
      znb_character_pow z chi ζ hchiz]
  calc
    coupling β c chi w p (columnTwist z σ ω) =
        (β : ℂ) * ∑ y, c p y *
          (ζ ^ (baseCharge (w p) σ).val *
            chi (holonomy (baseWord (w p) y) ω)) := by
      simp only [coupling, hchar]
    _ = ζ ^ (baseCharge (w p) σ).val * coupling β c chi w p ω := by
      simp only [coupling, Finset.mul_sum]
      apply Finset.sum_congr rfl
      intro y _
      ring

lemma znb_measurable_termsWeight {G E F X Q : Type*}
    [Group G] [MeasurableSpace G] [MeasurableMul₂ G] [MeasurableInv G] [Fintype Q]
    (chi : G → ℂ) (hchim : Measurable chi)
    (wq : Q → Word E F X) (coef : Q → ℂ) :
    Measurable (termsWeight chi wq coef : Config G E F X → ℝ) := by
  exact (Finset.measurable_sum univ (fun k _ =>
    Complex.measurable_re.comp
      ((hchim.comp (znb_measurable_holonomy (wq k))).const_mul (coef k)))).exp

lemma znb_termsWeight_twist {G E F X Q : Type*} [Group G] [Fintype Q]
    {N : ℕ} [NeZero N]
    (z : G) (hzN : z ^ N = 1) (hcentral : ∀ g : G, z * g = g * z)
    (chi : G → ℂ) (wq : Q → Word E F X)
    (hneutral : ∀ k, Neutral N (wq k)) (coef : Q → ℂ)
    (σ : E → ZMod N) (ω : Config G E F X) :
    termsWeight chi wq coef (columnTwist z σ ω) = termsWeight chi wq coef ω := by
  unfold termsWeight
  apply congrArg Real.exp
  apply Finset.sum_congr rfl
  intro k _
  rw [znb_holonomy_twist z hzN hcentral, hneutral k σ]
  simp

lemma znb_termsWeight_bound {G E F X Q : Type*} [Group G] [Fintype Q]
    (chi : G → ℂ) (hchi1 : ∀ g, ‖chi g‖ ≤ 1)
    (wq : Q → Word E F X) (coef : Q → ℂ) (ω : Config G E F X) :
    termsWeight chi wq coef ω ≤ Real.exp (∑ k, ‖coef k‖) := by
  unfold termsWeight
  apply Real.exp_le_exp.mpr
  apply Finset.sum_le_sum
  intro k _
  calc
    (coef k * chi (holonomy (wq k) ω)).re ≤
        ‖coef k * chi (holonomy (wq k) ω)‖ := Complex.re_le_norm _
    _ = ‖coef k‖ * ‖chi (holonomy (wq k) ω)‖ := norm_mul _ _
    _ ≤ ‖coef k‖ * 1 :=
      mul_le_mul_of_nonneg_left (hchi1 _) (norm_nonneg _)
    _ = ‖coef k‖ := mul_one _

lemma znb_integrable_density {G E F X P Q : Type*}
    [Group G] [MeasurableSpace G] [MeasurableMul₂ G] [MeasurableInv G]
    [Fintype E] [Fintype F] [Fintype X] [Fintype P] [Fintype Q]
    (haarG : Measure G) [IsProbabilityMeasure haarG]
    (chi : G → ℂ) (hchim : Measurable chi) (hchi1 : ∀ g, ‖chi g‖ ≤ 1)
    (wq : Q → Word E F X) (coef : Q → ℂ)
    (β : ℝ) (hβ : 0 ≤ β) (weights : P → F → ℂ)
    (hweights : ∀ p y, ‖weights p y‖ ≤ 1) (w : P → List (E × Bool)) :
    Integrable
      (fun ω : Config G E F X => termsWeight chi wq coef ω *
        Real.exp (∑ p, (coupling β weights chi w p ω).re))
      (configMeasure haarG) := by
  classical
  letI : IsProbabilityMeasure
      (configMeasure (E := E) (F := F) (X := X) haarG) := by
    unfold configMeasure
    infer_instance
  let C : ℝ := Real.exp (∑ k, ‖coef k‖) *
    Real.exp (∑ _p : P, β * (Fintype.card F : ℝ))
  have hDm : Measurable (fun ω : Config G E F X =>
      termsWeight chi wq coef ω *
        Real.exp (∑ p, (coupling β weights chi w p ω).re)) :=
    (znb_measurable_termsWeight chi hchim wq coef).mul
      (Finset.measurable_sum univ (fun p _ =>
        Complex.measurable_re.comp
          (znb_measurable_coupling β weights chi hchim w p))).exp
  have hKbound (ω : Config G E F X) :
      Real.exp (∑ p, (coupling β weights chi w p ω).re) ≤
        Real.exp (∑ _p : P, β * (Fintype.card F : ℝ)) := by
    apply Real.exp_le_exp.mpr
    apply Finset.sum_le_sum
    intro p _
    exact (Complex.re_le_norm _).trans
      (znb_coupling_bound β hβ weights hweights chi hchi1 w p ω)
  refine (integrable_const (μ := configMeasure haarG) C).mono'
    hDm.aestronglyMeasurable ?_
  apply Filter.Eventually.of_forall
  intro ω
  have hRpos : 0 < termsWeight chi wq coef ω := by
    unfold termsWeight
    exact Real.exp_pos _
  rw [Real.norm_eq_abs,
    abs_of_pos (mul_pos hRpos (Real.exp_pos _))]
  exact mul_le_mul (znb_termsWeight_bound chi hchi1 wq coef ω) (hKbound ω)
    (Real.exp_pos _).le (Real.exp_pos _).le

def znb_prefix {A : Type*} [AddCommGroup A] {k : ℕ}
    (g : Fin k → A) (r : ℕ) : A :=
  ∑ j ∈ Finset.univ.filter (fun j : Fin k => j.val < r), g j

lemma znb_prefix_zero {A : Type*} [AddCommGroup A] {k : ℕ}
    (g : Fin k → A) :
    znb_prefix g 0 = 0 := by
  simp [znb_prefix]

lemma znb_prefix_total {A : Type*} [AddCommGroup A] {k : ℕ}
    (g : Fin k → A) :
    znb_prefix g k = ∑ j, g j := by
  have hs : Finset.univ.filter (fun j : Fin k => j.val < k) = Finset.univ := by
    ext j
    simp [j.isLt]
  unfold znb_prefix
  rw [hs]

lemma znb_prefix_succ {A : Type*} [AddCommGroup A] {k : ℕ}
    (g : Fin k → A) (i : Fin k) :
    znb_prefix g (i.val + 1) = znb_prefix g i.val + g i := by
  classical
  have hs : Finset.univ.filter (fun j : Fin k => j.val < i.val + 1) =
      insert i (Finset.univ.filter (fun j : Fin k => j.val < i.val)) := by
    ext j
    simp only [Finset.mem_filter, Finset.mem_univ, true_and, Finset.mem_insert]
    constructor
    · intro hj
      by_cases he : j = i
      · exact Or.inl he
      · right
        have hne : j.val ≠ i.val := by
          intro h
          exact he (Fin.ext h)
        omega
    · intro hj
      rcases hj with rfl | hj
      · omega
      · omega
  have hi : i ∉ Finset.univ.filter (fun j : Fin k => j.val < i.val) := by
    simp
  unfold znb_prefix
  rw [hs, Finset.sum_insert hi]
  exact add_comm _ _

lemma znb_cycle {A : Type*} [AddCommGroup A] {k : ℕ}
    (g : Fin (k + 1) → A) (hg : ∑ j, g j = 0) (i : Fin (k + 1)) :
    znb_prefix g (finRotate (k + 1) i).val - znb_prefix g i.val = g i := by
  by_cases hi : i = Fin.last k
  · subst i
    rw [finRotate_last]
    change znb_prefix g 0 - znb_prefix g k = g (Fin.last k)
    rw [znb_prefix_zero]
    have hs : znb_prefix g k + g (Fin.last k) = 0 := by
      calc
        znb_prefix g k + g (Fin.last k) = znb_prefix g (k + 1) :=
          (znb_prefix_succ g (Fin.last k)).symm
        _ = 0 := by rw [znb_prefix_total, hg]
    calc
      0 - znb_prefix g k =
          (znb_prefix g k + g (Fin.last k)) - znb_prefix g k := by
        rw [hs]
      _ = g (Fin.last k) := by abel
  · rw [coe_finRotate_of_ne_last hi, znb_prefix_succ]
    abel

/-! ## Partie B : énoncés -/

/-- B0. A mixed plaquette (long link at `y`, other link, the same column at `y'` backwards, other link backwards)
is neutral for every `N`. -/
theorem mixed_word_neutral {E F X : Type*} (N : ℕ) (e : E) (y y' : F) (x x' : X) :
    Neutral N ([(Sum.inl (e, y), true), (Sum.inr x, true), (Sum.inl (e, y'), false), (Sum.inr x', false)] :
      Word E F X) := by
  intro σ
  simp [charge]

/-- B1. Wilson-type centre-twist bound (open surface): group with a left-invariant probability measure, central `z`
with `z ^ N = 1`, `χ (z g) = ζ χ g`; observable `ψ` of `N`-ality `q`; Stokes relation and independence of the
plaquette charges are hypotheses. -/
theorem wilson_centre_flip_bound
    {G E F X P : Type*} [Group G] [MeasurableSpace G] [MeasurableMul₂ G] [MeasurableInv G]
    [Fintype E] [DecidableEq E] [Fintype F] [Fintype X] [Fintype P] [DecidableEq P]
    (N : ℕ) [NeZero N] (ζ : ℂ) (hζ : ζ ^ N = 1)
    (haarG : Measure G) [IsProbabilityMeasure haarG]
    (hleft : ∀ g : G, MeasurePreserving (fun h : G => g * h) haarG haarG)
    (z : G) (hzN : z ^ N = 1) (hcentral : ∀ g : G, z * g = g * z)
    (chi : G → ℂ) (hchim : Measurable chi) (hchi1 : ∀ g, ‖chi g‖ ≤ 1)
    (hchiz : ∀ g, chi (z * g) = ζ * chi g)
    (w : P → List (E × Bool)) (c : P → F → ℂ) (hc : ∀ p y, ‖c p y‖ ≤ 1)
    (β : ℝ) (hβ : 0 ≤ β)
    (R : Config G E F X → ℝ) (hRm : Measurable R) (hR0 : ∀ ω, 0 ≤ R ω)
    (hRtw : ∀ (σ : E → ZMod N) ω, R (columnTwist z σ ω) = R ω)
    (hRint : Integrable (fun ω => R ω * Real.exp (∑ p, (coupling β c chi w p ω).re))
      (configMeasure haarG))
    (q : ZMod N) (psi : G → ℂ) (hpsim : Measurable psi) (hpsi1 : ∀ g, ‖psi g‖ ≤ 1)
    (hpsiz : ∀ g, psi (z * g) = ζ ^ q.val * psi g)
    (wC : List (E × Bool)) (y0 : F) (A : Finset P)
    (hStokes : ∀ σ : E → ZMod N, baseCharge wC σ = ∑ p ∈ A, baseCharge (w p) σ)
    (hsurj : Function.Surjective (fun σ : E → ZMod N => fun p => baseCharge (w p) σ))
    (ρ : ℝ)
    (hρ : ∀ t : ℂ, ‖t‖ ≤ β * (Fintype.card F : ℝ) →
      ‖∑ j : ZMod N, ζ ^ (q * j).val * ((Real.exp ((ζ ^ j.val * t).re) : ℝ) : ℂ)‖
        ≤ ρ * ∑ j : ZMod N, Real.exp ((ζ ^ j.val * t).re)) :
    ‖∫ ω, psi (holonomy (baseWord wC y0) ω) *
        ((R ω * Real.exp (∑ p, (coupling β c chi w p ω).re) : ℝ) : ℂ) ∂configMeasure haarG‖
      ≤ ρ ^ A.card *
        ∫ ω, R ω * Real.exp (∑ p, (coupling β c chi w p ω).re) ∂configMeasure haarG := by
  classical
  letI : IsProbabilityMeasure
      (configMeasure (E := E) (F := F) (X := X) haarG) := by
    unfold configMeasure
    infer_instance
  have hWtw (σ : E → ZMod N) (ω : Config G E F X) :
      psi (holonomy (baseWord wC y0) (columnTwist z σ ω)) =
        ζ ^ (q * ∑ p ∈ A, baseCharge (w p) σ).val *
          psi (holonomy (baseWord wC y0) ω) := by
    rw [znb_holonomy_twist z hzN hcentral, znb_charge_base,
      znb_character_pow z psi (ζ ^ q.val) hpsiz,
      znb_pow_mul ζ hζ, hStokes σ]
  exact centre_flip_bound (Ω := Config G E F X) (S := E → ZMod N)
    N ζ hζ
    (configMeasure haarG) (columnTwist z)
    (znb_columnTwist_preserving haarG hleft z)
    (fun σ p => baseCharge (w p) σ) hsurj
    (coupling β c chi w) (znb_measurable_coupling β c chi hchim w)
    (β * (Fintype.card F : ℝ)) (znb_coupling_bound β hβ c hc chi hchi1 w)
    (znb_coupling_twist z hzN hcentral β c chi ζ hchiz w)
    R hRm hR0 hRtw hRint
    (fun ω => psi (holonomy (baseWord wC y0) ω))
    (hpsim.comp (znb_measurable_holonomy (baseWord wC y0)))
    (fun ω => hpsi1 (holonomy (baseWord wC y0) ω))
    q A hWtw ρ hρ

/-- B2a. Explicit charge of a torus plaquette (discrete curl). -/
theorem torus_charge_explicit {m n N : ℕ} (σ : TorusEdge m n → ZMod N) (p : Fin m × Fin n) :
    baseCharge (torusWord p) σ =
      σ (Sum.inl (p.1, p.2)) + σ (Sum.inr (finRotate m p.1, p.2))
        - σ (Sum.inl (p.1, finRotate n p.2)) - σ (Sum.inr (p.1, p.2)) := by
  simp [torusWord, baseCharge, sub_eq_add_neg, add_assoc]

/-- B2b. On the torus the plaquette charges always sum to zero. -/
theorem torus_charge_sum {m n N : ℕ} (σ : TorusEdge m n → ZMod N) :
    ∑ p : Fin m × Fin n, baseCharge (torusWord p) σ = 0 := by
  classical
  have hH : (∑ p : Fin m × Fin n, σ (Sum.inl (p.1, finRotate n p.2))) =
      ∑ p : Fin m × Fin n, σ (Sum.inl p) := by
    exact Equiv.sum_comp (Equiv.prodCongr (Equiv.refl (Fin m)) (finRotate n))
      (fun p : Fin m × Fin n => σ (Sum.inl p))
  have hV : (∑ p : Fin m × Fin n, σ (Sum.inr (finRotate m p.1, p.2))) =
      ∑ p : Fin m × Fin n, σ (Sum.inr p) := by
    exact Equiv.sum_comp (Equiv.prodCongr (finRotate m) (Equiv.refl (Fin n)))
      (fun p : Fin m × Fin n => σ (Sum.inr p))
  simp only [torus_charge_explicit, Finset.sum_sub_distrib, Finset.sum_add_distrib]
  rw [hH, hV]
  abel

/-- B2c. On the torus (periods at least two) every plaquette charge assignment of total charge zero is realised by
column variables. -/
theorem torus_charge_image {m n N : ℕ} (hm : 2 ≤ m) (hn : 2 ≤ n) (t : Fin m × Fin n → ZMod N)
    (ht : ∑ p, t p = 0) :
    ∃ σ : TorusEdge m n → ZMod N, ∀ p, baseCharge (torusWord p) σ = t p := by
  classical
  obtain ⟨m', rfl⟩ : ∃ m', m = m' + 1 := ⟨m - 1, by omega⟩
  obtain ⟨n', rfl⟩ : ∃ n', n = n' + 1 := ⟨n - 1, by omega⟩
  let c : Fin (m' + 1) → ZMod N :=
    fun i => ∑ j : Fin (n' + 1), t (i, j)
  have hc : (∑ i, c i) = 0 := by
    dsimp only [c]
    exact (Fintype.sum_prod_type t).symm.trans ht
  let d : Fin (m' + 1) → Fin (n' + 1) → ZMod N :=
    fun i j => (if j = 0 then c i else 0) - t (i, j)
  have hd (i : Fin (m' + 1)) : (∑ j, d i j) = 0 := by
    dsimp only [d]
    rw [Finset.sum_sub_distrib]
    have hcorr : (∑ j : Fin (n' + 1), if j = 0 then c i else (0 : ZMod N)) =
        c i := by
      simpa only [Finset.mem_univ, if_true] using
        (Finset.sum_ite_eq' (Finset.univ : Finset (Fin (n' + 1)))
          (0 : Fin (n' + 1)) (fun _ => c i))
    rw [hcorr]
    change c i - c i = 0
    exact sub_self _
  let v : Fin (m' + 1) → Fin (n' + 1) → ZMod N :=
    fun i j => if j = 0 then znb_prefix c i.val else 0
  let h : Fin (m' + 1) → Fin (n' + 1) → ZMod N :=
    fun i j => znb_prefix (d i) j.val
  have hv (i : Fin (m' + 1)) (j : Fin (n' + 1)) :
      v (finRotate (m' + 1) i) j - v i j =
        (if j = 0 then c i else 0) := by
    by_cases hj : j = 0
    · simp only [v, if_pos hj]
      exact znb_cycle c hc i
    · simp only [v, if_neg hj, sub_self]
  have hh (i : Fin (m' + 1)) (j : Fin (n' + 1)) :
      h i (finRotate (n' + 1) j) - h i j = d i j :=
    znb_cycle (d i) (hd i) j
  let σ : TorusEdge (m' + 1) (n' + 1) → ZMod N := fun e =>
    match e with
    | Sum.inl p => h p.1 p.2
    | Sum.inr p => v p.1 p.2
  refine ⟨σ, ?_⟩
  intro p
  rcases p with ⟨i, j⟩
  rw [torus_charge_explicit]
  change h i j + v (finRotate (m' + 1) i) j -
      h i (finRotate (n' + 1) j) - v i j = t (i, j)
  calc
    h i j + v (finRotate (m' + 1) i) j -
        h i (finRotate (n' + 1) j) - v i j =
      (v (finRotate (m' + 1) i) j - v i j) -
        (h i (finRotate (n' + 1) j) - h i j) := by abel
    _ = (if j = 0 then c i else 0) - d i j := by rw [hv, hh]
    _ = t (i, j) := by
      dsimp only [d]
      abel

/-- B3. Wilson-type twist ratio on (torus `m × n`) × (finite fibre `F`), with a finite family of neutral extra terms
(complex coefficients): `Z k` multiplies the weights of the base plaquette `p₀` by `ζ ^ k` at every fibre site. -/
theorem wilson_twist_ratio_torus
    {G F X Q : Type*} [Group G] [MeasurableSpace G] [MeasurableMul₂ G] [MeasurableInv G]
    [Fintype F] [Fintype X] [Fintype Q]
    (N : ℕ) [NeZero N] (ζ : ℂ) (hζ : ζ ^ N = 1)
    (m n : ℕ) (hm : 2 ≤ m) (hn : 2 ≤ n)
    (haarG : Measure G) [IsProbabilityMeasure haarG]
    (hleft : ∀ g : G, MeasurePreserving (fun h : G => g * h) haarG haarG)
    (z : G) (hzN : z ^ N = 1) (hcentral : ∀ g : G, z * g = g * z)
    (chi : G → ℂ) (hchim : Measurable chi) (hchi1 : ∀ g, ‖chi g‖ ≤ 1)
    (hchiz : ∀ g, chi (z * g) = ζ * chi g)
    (weights : (Fin m × Fin n) → F → ℂ) (hweights : ∀ p y, ‖weights p y‖ ≤ 1)
    (β : ℝ) (hβ : 0 ≤ β)
    (wq : Q → Word (TorusEdge m n) F X) (hneutral : ∀ k, Neutral N (wq k)) (coef : Q → ℂ)
    (q : ZMod N) (ρ : ℝ)
    (hρ : ∀ t : ℂ, ‖t‖ ≤ β * (Fintype.card F : ℝ) →
      ‖∑ j : ZMod N, ζ ^ (q * j).val * ((Real.exp ((ζ ^ j.val * t).re) : ℝ) : ℂ)‖
        ≤ ρ * ∑ j : ZMod N, Real.exp ((ζ ^ j.val * t).re))
    (p₀ : Fin m × Fin n) :
    ‖∑ k : ZMod N, ζ ^ (q * k).val *
        ((∫ ω, termsWeight chi wq coef ω * Real.exp (∑ p, (coupling β
            (fun p y => if p = p₀ then ζ ^ k.val * weights p y else weights p y) chi torusWord p ω).re)
            ∂configMeasure haarG : ℝ) : ℂ)‖
      ≤ ρ ^ (m * n) *
        ∑ k : ZMod N, ∫ ω, termsWeight chi wq coef ω * Real.exp (∑ p, (coupling β
            (fun p y => if p = p₀ then ζ ^ k.val * weights p y else weights p y) chi torusWord p ω).re)
            ∂configMeasure haarG := by
  classical
  letI : IsProbabilityMeasure
      (configMeasure (E := TorusEdge m n) (F := F) (X := X) haarG) := by
    unfold configMeasure
    infer_instance
  have himg :
      ∀ t : (Fin m × Fin n) → ZMod N, ∑ p, t p = 0 →
        ∃ σ : TorusEdge m n → ZMod N,
          (fun p => baseCharge (torusWord p) σ) = t := by
    intro t ht
    obtain ⟨σ, hσ⟩ := torus_charge_image hm hn t ht
    exact ⟨σ, funext hσ⟩
  have htwisted (k : ZMod N) (p : Fin m × Fin n)
      (ω : Config G (TorusEdge m n) F X) :
      coupling β
          (fun p y => if p = p₀ then ζ ^ k.val * weights p y else weights p y)
          chi torusWord p ω =
        (if p = p₀ then ζ ^ k.val else 1) *
          coupling β weights chi torusWord p ω := by
    by_cases hp : p = p₀
    · simp only [coupling, if_pos hp, Finset.mul_sum]
      apply Finset.sum_congr rfl
      intro y _
      ring
    · simp only [coupling, if_neg hp, one_mul]
  have hmain := twist_ratio_bound
    (Ω := Config G (TorusEdge m n) F X) (S := TorusEdge m n → ZMod N)
    N ζ hζ
    (configMeasure haarG) (columnTwist z)
    (znb_columnTwist_preserving haarG hleft z)
    (fun σ p => baseCharge (torusWord p) σ) himg
    (coupling β weights chi torusWord)
    (znb_measurable_coupling β weights chi hchim torusWord)
    (β * (Fintype.card F : ℝ))
    (znb_coupling_bound β hβ weights hweights chi hchi1 torusWord)
    (znb_coupling_twist z hzN hcentral β weights chi ζ hchiz torusWord)
    (termsWeight chi wq coef)
    (znb_measurable_termsWeight chi hchim wq coef)
    (fun ω => (Real.exp_pos _).le)
    (znb_termsWeight_twist z hzN hcentral chi wq hneutral coef)
    (znb_integrable_density haarG chi hchim hchi1 wq coef
      β hβ weights hweights torusWord)
    q ρ hρ p₀
  simpa only [htwisted, Fintype.card_prod, Fintype.card_fin] using hmain

/-- B3c. B3 with the crude constant `1 - exp (-2 β |F|)` (primitive root, non-zero charge). -/
theorem wilson_twist_ratio_torus_crude
    {G F X Q : Type*} [Group G] [MeasurableSpace G] [MeasurableMul₂ G] [MeasurableInv G]
    [Fintype F] [Fintype X] [Fintype Q]
    (N : ℕ) [NeZero N] (ζ : ℂ) (hζ : IsPrimitiveRoot ζ N)
    (m n : ℕ) (hm : 2 ≤ m) (hn : 2 ≤ n)
    (haarG : Measure G) [IsProbabilityMeasure haarG]
    (hleft : ∀ g : G, MeasurePreserving (fun h : G => g * h) haarG haarG)
    (z : G) (hzN : z ^ N = 1) (hcentral : ∀ g : G, z * g = g * z)
    (chi : G → ℂ) (hchim : Measurable chi) (hchi1 : ∀ g, ‖chi g‖ ≤ 1)
    (hchiz : ∀ g, chi (z * g) = ζ * chi g)
    (weights : (Fin m × Fin n) → F → ℂ) (hweights : ∀ p y, ‖weights p y‖ ≤ 1)
    (β : ℝ) (hβ : 0 ≤ β)
    (wq : Q → Word (TorusEdge m n) F X) (hneutral : ∀ k, Neutral N (wq k)) (coef : Q → ℂ)
    (q : ZMod N) (hq : q ≠ 0) (p₀ : Fin m × Fin n) :
    ‖∑ k : ZMod N, ζ ^ (q * k).val *
        ((∫ ω, termsWeight chi wq coef ω * Real.exp (∑ p, (coupling β
            (fun p y => if p = p₀ then ζ ^ k.val * weights p y else weights p y) chi torusWord p ω).re)
            ∂configMeasure haarG : ℝ) : ℂ)‖
      ≤ (1 - Real.exp (-2 * (β * (Fintype.card F : ℝ)))) ^ (m * n) *
        ∑ k : ZMod N, ∫ ω, termsWeight chi wq coef ω * Real.exp (∑ p, (coupling β
            (fun p y => if p = p₀ then ζ ^ k.val * weights p y else weights p y) chi torusWord p ω).re)
            ∂configMeasure haarG := by
  classical
  refine wilson_twist_ratio_torus N ζ hζ.pow_eq_one m n hm hn
    haarG hleft z hzN hcentral chi hchim hchi1 hchiz
    weights hweights β hβ wq hneutral coef q
    (1 - Real.exp (-2 * (β * (Fintype.card F : ℝ)))) ?_ p₀
  intro t ht
  refine (rho_crude N ζ hζ q hq t).trans ?_
  apply mul_le_mul_of_nonneg_right ?_
    (Finset.sum_nonneg (fun j _ => (Real.exp_pos _).le))
  have he :
      Real.exp (-2 * (β * (Fintype.card F : ℝ))) ≤ Real.exp (-2 * ‖t‖) :=
    Real.exp_le_exp.mpr (by linarith)
  linarith

end CentreZN

end


noncomputable section

namespace CentreZNFrozen

/-! ## Partie A : forme abstraite -/

/-- A1. Abstract centre-twist bound (open surface). Twists `τ s` preserve `μ`; the charge map `chg` onto
`P → ZMod N` is surjective; the complex couplings rotate, `T p ∘ τ s = ζ ^ (chg s p) • T p`; the weight `R` is
invariant; the observable `W` takes the phase `ζ ^ (q • Σ_{p ∈ A} chg s p)`; `ρ` dominates the one-plaquette
Fourier ratio on the disc of radius `κ`. -/
theorem centre_flip_bound
    {Ω S P : Type*} [MeasurableSpace Ω] [Fintype P] [DecidableEq P]
    (N : ℕ) [NeZero N] (ζ : ℂ) (hζ : ζ ^ N = 1)
    (μ : Measure Ω) [IsProbabilityMeasure μ]
    (τ : S → Ω → Ω) (hτ : ∀ s, MeasurePreserving (τ s) μ μ)
    (chg : S → P → ZMod N) (hsurj : Function.Surjective chg)
    (T : P → Ω → ℂ) (hTm : ∀ p, Measurable (T p))
    (κ : ℝ) (hT : ∀ p ω, ‖T p ω‖ ≤ κ)
    (hTτ : ∀ s p ω, T p (τ s ω) = ζ ^ (chg s p).val * T p ω)
    (R : Ω → ℝ) (hRm : Measurable R) (hR0 : ∀ ω, 0 ≤ R ω) (hRτ : ∀ s ω, R (τ s ω) = R ω)
    (hRint : Integrable (fun ω => R ω * Real.exp (∑ p, (T p ω).re)) μ)
    (W : Ω → ℂ) (hWm : Measurable W) (hW1 : ∀ ω, ‖W ω‖ ≤ 1)
    (q : ZMod N) (A : Finset P)
    (hWτ : ∀ s ω, W (τ s ω) = ζ ^ (q * ∑ p ∈ A, chg s p).val * W ω)
    (ρ : ℝ)
    (hρ : ∀ t : ℂ, ‖t‖ ≤ κ →
      ‖∑ j : ZMod N, ζ ^ (q * j).val * ((Real.exp ((ζ ^ j.val * t).re) : ℝ) : ℂ)‖
        ≤ ρ * ∑ j : ZMod N, Real.exp ((ζ ^ j.val * t).re)) :
    ‖∫ ω, W ω * ((R ω * Real.exp (∑ p, (T p ω).re) : ℝ) : ℂ) ∂μ‖
      ≤ ρ ^ A.card * ∫ ω, R ω * Real.exp (∑ p, (T p ω).re) ∂μ := by
  sorry

/-- A2. Abstract twist-ratio bound (closed surface). Every charge assignment of total charge zero is realised by a
twist. `Z k` is the partition function in which the coupling of the plaquette `p₀` is multiplied by `ζ ^ k`; the
left side is the norm of its Fourier transform at `q`, the right side involves the sum of all `Z k`. -/
theorem twist_ratio_bound
    {Ω S P : Type*} [MeasurableSpace Ω] [Fintype P] [DecidableEq P]
    (N : ℕ) [NeZero N] (ζ : ℂ) (hζ : ζ ^ N = 1)
    (μ : Measure Ω) [IsProbabilityMeasure μ]
    (τ : S → Ω → Ω) (hτ : ∀ s, MeasurePreserving (τ s) μ μ)
    (chg : S → P → ZMod N)
    (himg : ∀ t : P → ZMod N, ∑ p, t p = 0 → ∃ s, chg s = t)
    (T : P → Ω → ℂ) (hTm : ∀ p, Measurable (T p))
    (κ : ℝ) (hT : ∀ p ω, ‖T p ω‖ ≤ κ)
    (hTτ : ∀ s p ω, T p (τ s ω) = ζ ^ (chg s p).val * T p ω)
    (R : Ω → ℝ) (hRm : Measurable R) (hR0 : ∀ ω, 0 ≤ R ω) (hRτ : ∀ s ω, R (τ s ω) = R ω)
    (hRint : Integrable (fun ω => R ω * Real.exp (∑ p, (T p ω).re)) μ)
    (q : ZMod N) (ρ : ℝ)
    (hρ : ∀ t : ℂ, ‖t‖ ≤ κ →
      ‖∑ j : ZMod N, ζ ^ (q * j).val * ((Real.exp ((ζ ^ j.val * t).re) : ℝ) : ℂ)‖
        ≤ ρ * ∑ j : ZMod N, Real.exp ((ζ ^ j.val * t).re))
    (p₀ : P) :
    ‖∑ k : ZMod N, ζ ^ (q * k).val *
        ((∫ ω, R ω * Real.exp (∑ p, ((if p = p₀ then ζ ^ k.val else 1) * T p ω).re) ∂μ : ℝ) : ℂ)‖
      ≤ ρ ^ Fintype.card P *
        ∑ k : ZMod N, ∫ ω, R ω * Real.exp (∑ p, ((if p = p₀ then ζ ^ k.val else 1) * T p ω).re) ∂μ := by
  sorry

/-- A3. Crude constant: for a primitive `N`-th root of unity and a non-zero charge `q`, the one-plaquette Fourier
ratio is at most `1 - exp (-2 ‖t‖)`. -/
theorem rho_crude (N : ℕ) [NeZero N] (ζ : ℂ) (hζ : IsPrimitiveRoot ζ N) (q : ZMod N) (hq : q ≠ 0)
    (t : ℂ) :
    ‖∑ j : ZMod N, ζ ^ (q * j).val * ((Real.exp ((ζ ^ j.val * t).re) : ℝ) : ℂ)‖
      ≤ (1 - Real.exp (-2 * ‖t‖)) * ∑ j : ZMod N, Real.exp ((ζ ^ j.val * t).re) := by
  sorry

/-- A4. The case `N = 2`, `ζ = -1`, `q = 1`: the constant is `tanh ‖t‖`. -/
theorem rho_two (t : ℂ) :
    ‖∑ j : ZMod 2, (-1 : ℂ) ^ ((1 : ZMod 2) * j).val * ((Real.exp (((-1 : ℂ) ^ j.val * t).re) : ℝ) : ℂ)‖
      ≤ Real.tanh ‖t‖ * ∑ j : ZMod 2, Real.exp (((-1 : ℂ) ^ j.val * t).re) := by
  sorry

/-- A5. Sharpness: on `ZMod N` with the uniform probability measure, translations preserve the measure, the coupling
`j ↦ ζ ^ j * t` and the observable `j ↦ ζ ^ (q * j)` have the covariances required by A1 (one plaquette, charge of a
translation by `s` equal to `s`, coupling of norm `‖t‖`, observable of norm one), and the two integrals are exactly
the normalised Fourier sums of A1's hypothesis: A1 is an equality here with `ρ` the ratio at `t`. -/
theorem sharp_one_plaquette (N : ℕ) [NeZero N] (ζ : ℂ) (hζ : ζ ^ N = 1) (q : ZMod N) (t : ℂ) :
    ∃ μ : Measure (ZMod N), IsProbabilityMeasure μ ∧
      (∀ s : ZMod N, MeasurePreserving (fun j : ZMod N => s + j) μ μ) ∧
      (∀ j : ZMod N, ‖ζ ^ j.val * t‖ = ‖t‖) ∧ (∀ j : ZMod N, ‖ζ ^ (q * j).val‖ = 1) ∧
      (∀ s j : ZMod N, ζ ^ (s + j).val * t = ζ ^ s.val * (ζ ^ j.val * t)) ∧
      (∀ s j : ZMod N, ζ ^ (q * (s + j)).val = ζ ^ (q * s).val * ζ ^ (q * j).val) ∧
      (∫ j, ζ ^ (q * j).val * ((Real.exp ((ζ ^ j.val * t).re) : ℝ) : ℂ) ∂μ)
          = (N : ℂ)⁻¹ * ∑ j : ZMod N, ζ ^ (q * j).val * ((Real.exp ((ζ ^ j.val * t).re) : ℝ) : ℂ) ∧
      (∫ j, Real.exp ((ζ ^ j.val * t).re) ∂μ) = (N : ℝ)⁻¹ * ∑ j : ZMod N, Real.exp ((ζ ^ j.val * t).re) := by
  sorry

/-- A6a. A1 with the crude constant (primitive root, non-zero charge). -/
theorem centre_flip_bound_crude
    {Ω S P : Type*} [MeasurableSpace Ω] [Fintype P] [DecidableEq P]
    (N : ℕ) [NeZero N] (ζ : ℂ) (hζ : IsPrimitiveRoot ζ N)
    (μ : Measure Ω) [IsProbabilityMeasure μ]
    (τ : S → Ω → Ω) (hτ : ∀ s, MeasurePreserving (τ s) μ μ)
    (chg : S → P → ZMod N) (hsurj : Function.Surjective chg)
    (T : P → Ω → ℂ) (hTm : ∀ p, Measurable (T p))
    (κ : ℝ) (hT : ∀ p ω, ‖T p ω‖ ≤ κ)
    (hTτ : ∀ s p ω, T p (τ s ω) = ζ ^ (chg s p).val * T p ω)
    (R : Ω → ℝ) (hRm : Measurable R) (hR0 : ∀ ω, 0 ≤ R ω) (hRτ : ∀ s ω, R (τ s ω) = R ω)
    (hRint : Integrable (fun ω => R ω * Real.exp (∑ p, (T p ω).re)) μ)
    (W : Ω → ℂ) (hWm : Measurable W) (hW1 : ∀ ω, ‖W ω‖ ≤ 1)
    (q : ZMod N) (hq : q ≠ 0) (A : Finset P)
    (hWτ : ∀ s ω, W (τ s ω) = ζ ^ (q * ∑ p ∈ A, chg s p).val * W ω) :
    ‖∫ ω, W ω * ((R ω * Real.exp (∑ p, (T p ω).re) : ℝ) : ℂ) ∂μ‖
      ≤ (1 - Real.exp (-2 * κ)) ^ A.card * ∫ ω, R ω * Real.exp (∑ p, (T p ω).re) ∂μ := by
  sorry

/-- A6b. A2 with the crude constant (primitive root, non-zero charge). -/
theorem twist_ratio_bound_crude
    {Ω S P : Type*} [MeasurableSpace Ω] [Fintype P] [DecidableEq P]
    (N : ℕ) [NeZero N] (ζ : ℂ) (hζ : IsPrimitiveRoot ζ N)
    (μ : Measure Ω) [IsProbabilityMeasure μ]
    (τ : S → Ω → Ω) (hτ : ∀ s, MeasurePreserving (τ s) μ μ)
    (chg : S → P → ZMod N)
    (himg : ∀ t : P → ZMod N, ∑ p, t p = 0 → ∃ s, chg s = t)
    (T : P → Ω → ℂ) (hTm : ∀ p, Measurable (T p))
    (κ : ℝ) (hT : ∀ p ω, ‖T p ω‖ ≤ κ)
    (hTτ : ∀ s p ω, T p (τ s ω) = ζ ^ (chg s p).val * T p ω)
    (R : Ω → ℝ) (hRm : Measurable R) (hR0 : ∀ ω, 0 ≤ R ω) (hRτ : ∀ s ω, R (τ s ω) = R ω)
    (hRint : Integrable (fun ω => R ω * Real.exp (∑ p, (T p ω).re)) μ)
    (q : ZMod N) (hq : q ≠ 0) (p₀ : P) :
    ‖∑ k : ZMod N, ζ ^ (q * k).val *
        ((∫ ω, R ω * Real.exp (∑ p, ((if p = p₀ then ζ ^ k.val else 1) * T p ω).re) ∂μ : ℝ) : ℂ)‖
      ≤ (1 - Real.exp (-2 * κ)) ^ Fintype.card P *
        ∑ k : ZMod N, ∫ ω, R ω * Real.exp (∑ p, ((if p = p₀ then ζ ^ k.val else 1) * T p ω).re) ∂μ := by
  sorry

/-- A7a. `N = 2` recovers the published column-flip bound (statement of `TubeArea.column_flip_bound`, verbatim, as
restated in its verification footer); to be derived from A1 and A4. -/
theorem recover_column_flip_bound
    {Ω E P : Type*} [MeasurableSpace Ω] [Fintype E] [DecidableEq E] [Fintype P] [DecidableEq P]
    (μ : Measure Ω) [IsProbabilityMeasure μ]
    (τ : (E → ℤˣ) → Ω → Ω) (hτ : ∀ σ, MeasurePreserving (τ σ) μ μ)
    (bd : P → Finset E)
    (hsurj : Function.Surjective (fun σ : E → ℤˣ => ((fun p => ∏ e ∈ bd p, σ e) : P → ℤˣ)))
    (K : P → Ω → ℝ) (hKm : ∀ p, Measurable (K p))
    (κ : ℝ) (hK : ∀ p ω, |K p ω| ≤ κ)
    (hKτ : ∀ σ p ω, K p (τ σ ω) = (((∏ e ∈ bd p, σ e : ℤˣ) : ℤ) : ℝ) * K p ω)
    (R : Ω → ℝ) (hRm : Measurable R) (hR0 : ∀ ω, 0 ≤ R ω) (hRτ : ∀ σ ω, R (τ σ ω) = R ω)
    (hRint : Integrable (fun ω => R ω * Real.exp (∑ p, K p ω)) μ)
    (W : Ω → ℝ) (hWm : Measurable W) (hW1 : ∀ ω, |W ω| ≤ 1)
    (A : Finset P)
    (hWτ : ∀ σ ω, W (τ σ ω) = (((∏ p ∈ A, ∏ e ∈ bd p, σ e : ℤˣ) : ℤ) : ℝ) * W ω) :
    |∫ ω, W ω * (R ω * Real.exp (∑ p, K p ω)) ∂μ|
      ≤ Real.tanh κ ^ A.card * ∫ ω, R ω * Real.exp (∑ p, K p ω) ∂μ := by
  sorry

/-- A7b. `N = 2` recovers the published twist-ratio bound (statement of `TubeArea.twist_ratio_bound`, verbatim, as
restated in its verification footer); to be derived from A2 and A4. -/
theorem recover_twist_ratio_bound
    {Ω E P : Type*} [MeasurableSpace Ω] [Fintype E] [DecidableEq E] [Fintype P] [DecidableEq P]
    (μ : Measure Ω) [IsProbabilityMeasure μ]
    (τ : (E → ℤˣ) → Ω → Ω) (hτ : ∀ σ, MeasurePreserving (τ σ) μ μ)
    (bd : P → Finset E)
    (hpar : ∀ σ : E → ℤˣ, ∏ p, (∏ e ∈ bd p, σ e) = 1)
    (himg : ∀ t : P → ℤˣ, ∏ p, t p = 1 → ∃ σ : E → ℤˣ, ∀ p, ∏ e ∈ bd p, σ e = t p)
    (K : P → Ω → ℝ) (hKm : ∀ p, Measurable (K p))
    (κ : ℝ) (hK : ∀ p ω, |K p ω| ≤ κ)
    (hKτ : ∀ σ p ω, K p (τ σ ω) = (((∏ e ∈ bd p, σ e : ℤˣ) : ℤ) : ℝ) * K p ω)
    (R : Ω → ℝ) (hRm : Measurable R) (hR0 : ∀ ω, 0 ≤ R ω) (hRτ : ∀ σ ω, R (τ σ ω) = R ω)
    (hRint : Integrable (fun ω => R ω * Real.exp (∑ p, K p ω)) μ)
    (p₀ : P) :
    |(∫ ω, R ω * Real.exp (∑ p, K p ω) ∂μ)
        - ∫ ω, R ω * Real.exp (∑ p, (if p = p₀ then -(K p ω) else K p ω)) ∂μ|
      ≤ Real.tanh κ ^ Fintype.card P *
        ((∫ ω, R ω * Real.exp (∑ p, K p ω) ∂μ)
          + ∫ ω, R ω * Real.exp (∑ p, (if p = p₀ then -(K p ω) else K p ω)) ∂μ) := by
  sorry

/-! ## Partie B : théorie de type Wilson à élément central d'ordre `N` (définitions figées) -/

/-- Configurations: long links `(e, y)` (base edge `e`, fibre site `y`) and other links `x`. -/
abbrev Config (G E F X : Type*) := ((E × F) → G) × (X → G)

/-- The product of the single-link measure over all links. -/
def configMeasure {G E F X : Type*} [MeasurableSpace G] [Fintype E] [Fintype F] [Fintype X]
    (haarG : Measure G) : Measure (Config G E F X) :=
  (Measure.pi fun _ : E × F => haarG).prod (Measure.pi fun _ : X => haarG)

/-- Column twist: every long link `(e, y)` is left-multiplied by `z ^ (σ e).val`; other links are unchanged. -/
def columnTwist {G E F X : Type*} [Monoid G] {N : ℕ} (z : G) (σ : E → ZMod N)
    (ω : Config G E F X) : Config G E F X :=
  (fun ey => z ^ (σ ey.1).val * ω.1 ey, ω.2)

/-- Positive orientation: the link itself; negative orientation: its inverse. -/
def orientedLink {G : Type*} [Inv G] : Bool → G → G
  | true, g => g
  | false, g => g⁻¹

/-- A word: a list of oriented letters, each a long link `Sum.inl (e, y)` or another link `Sum.inr x`. -/
abbrev Word (E F X : Type*) := List (((E × F) ⊕ X) × Bool)

/-- Ordered holonomy of a word (empty word: `1`). -/
def holonomy {G E F X : Type*} [Group G] : Word E F X → Config G E F X → G
  | [], _ => 1
  | (Sum.inl ey, b) :: w, ω => orientedLink b (ω.1 ey) * holonomy w ω
  | (Sum.inr x, b) :: w, ω => orientedLink b (ω.2 x) * holonomy w ω

/-- Charge of a word: signed sum (with multiplicity) of the column variables of its long letters. -/
def charge {E F X : Type*} {N : ℕ} : Word E F X → (E → ZMod N) → ZMod N
  | [], _ => 0
  | (Sum.inl ey, b) :: w, σ => (if b then σ ey.1 else -σ ey.1) + charge w σ
  | (Sum.inr _, _) :: w, σ => charge w σ

/-- A word is neutral for `ZMod N` when its charge vanishes for all column variables. -/
def Neutral {E F X : Type*} (N : ℕ) (w : Word E F X) : Prop :=
  ∀ σ : E → ZMod N, charge w σ = 0

/-- The word of a base path (list of oriented base edges) at the fibre site `y`. -/
def baseWord {E F X : Type*} (w : List (E × Bool)) (y : F) : Word E F X :=
  w.map fun a => (Sum.inl (a.1, y), a.2)

/-- Charge of a base path: signed sum (with multiplicity) of the column variables along it. -/
def baseCharge {E : Type*} {N : ℕ} : List (E × Bool) → (E → ZMod N) → ZMod N
  | [], _ => 0
  | a :: w, σ => (if a.2 then σ a.1 else -σ a.1) + baseCharge w σ

/-- Complex Wilson coupling of the base plaquette `p`: `β Σ_y c p y χ(holonomy of its word at y)`.
The action uses its real part. -/
def coupling {G E F X P : Type*} [Group G] [Fintype F]
    (β : ℝ) (c : P → F → ℂ) (chi : G → ℂ) (w : P → List (E × Bool)) (p : P)
    (ω : Config G E F X) : ℂ :=
  (β : ℂ) * ∑ y, c p y * chi (holonomy (baseWord (w p) y) ω)

/-- Weight of a finite family of extra terms: `exp (Σ_k Re (coef k · χ(holonomy of the word k)))`. -/
def termsWeight {G E F X Q : Type*} [Group G] [Fintype Q]
    (chi : G → ℂ) (wq : Q → Word E F X) (coef : Q → ℂ) (ω : Config G E F X) : ℝ :=
  Real.exp (∑ k, (coef k * chi (holonomy (wq k) ω)).re)

/-- Edges of the discrete torus `(ℤ/m) × (ℤ/n)`: `Sum.inl (i,j)` is the horizontal edge from `(i,j)` to `(i+1,j)`,
`Sum.inr (i,j)` the vertical edge from `(i,j)` to `(i,j+1)`; indices are cyclic (`finRotate`). -/
abbrev TorusEdge (m n : ℕ) := (Fin m × Fin n) ⊕ (Fin m × Fin n)

/-- Counterclockwise plaquette path from the corner `p = (i,j)`: bottom `H(i,j)` forwards, right `V(i+1,j)`
forwards, top `H(i,j+1)` backwards, left `V(i,j)` backwards. -/
def torusWord {m n : ℕ} (p : Fin m × Fin n) : List (TorusEdge m n × Bool) :=
  [(Sum.inl (p.1, p.2), true), (Sum.inr (finRotate m p.1, p.2), true),
    (Sum.inl (p.1, finRotate n p.2), false), (Sum.inr (p.1, p.2), false)]

/-! ## Partie B : énoncés -/

/-- B0. A mixed plaquette (long link at `y`, other link, the same column at `y'` backwards, other link backwards)
is neutral for every `N`. -/
theorem mixed_word_neutral {E F X : Type*} (N : ℕ) (e : E) (y y' : F) (x x' : X) :
    Neutral N ([(Sum.inl (e, y), true), (Sum.inr x, true), (Sum.inl (e, y'), false), (Sum.inr x', false)] :
      Word E F X) := by
  sorry

/-- B1. Wilson-type centre-twist bound (open surface): group with a left-invariant probability measure, central `z`
with `z ^ N = 1`, `χ (z g) = ζ χ g`; observable `ψ` of `N`-ality `q`; Stokes relation and independence of the
plaquette charges are hypotheses. -/
theorem wilson_centre_flip_bound
    {G E F X P : Type*} [Group G] [MeasurableSpace G] [MeasurableMul₂ G] [MeasurableInv G]
    [Fintype E] [DecidableEq E] [Fintype F] [Fintype X] [Fintype P] [DecidableEq P]
    (N : ℕ) [NeZero N] (ζ : ℂ) (hζ : ζ ^ N = 1)
    (haarG : Measure G) [IsProbabilityMeasure haarG]
    (hleft : ∀ g : G, MeasurePreserving (fun h : G => g * h) haarG haarG)
    (z : G) (hzN : z ^ N = 1) (hcentral : ∀ g : G, z * g = g * z)
    (chi : G → ℂ) (hchim : Measurable chi) (hchi1 : ∀ g, ‖chi g‖ ≤ 1)
    (hchiz : ∀ g, chi (z * g) = ζ * chi g)
    (w : P → List (E × Bool)) (c : P → F → ℂ) (hc : ∀ p y, ‖c p y‖ ≤ 1)
    (β : ℝ) (hβ : 0 ≤ β)
    (R : Config G E F X → ℝ) (hRm : Measurable R) (hR0 : ∀ ω, 0 ≤ R ω)
    (hRtw : ∀ (σ : E → ZMod N) ω, R (columnTwist z σ ω) = R ω)
    (hRint : Integrable (fun ω => R ω * Real.exp (∑ p, (coupling β c chi w p ω).re))
      (configMeasure haarG))
    (q : ZMod N) (psi : G → ℂ) (hpsim : Measurable psi) (hpsi1 : ∀ g, ‖psi g‖ ≤ 1)
    (hpsiz : ∀ g, psi (z * g) = ζ ^ q.val * psi g)
    (wC : List (E × Bool)) (y0 : F) (A : Finset P)
    (hStokes : ∀ σ : E → ZMod N, baseCharge wC σ = ∑ p ∈ A, baseCharge (w p) σ)
    (hsurj : Function.Surjective (fun σ : E → ZMod N => fun p => baseCharge (w p) σ))
    (ρ : ℝ)
    (hρ : ∀ t : ℂ, ‖t‖ ≤ β * (Fintype.card F : ℝ) →
      ‖∑ j : ZMod N, ζ ^ (q * j).val * ((Real.exp ((ζ ^ j.val * t).re) : ℝ) : ℂ)‖
        ≤ ρ * ∑ j : ZMod N, Real.exp ((ζ ^ j.val * t).re)) :
    ‖∫ ω, psi (holonomy (baseWord wC y0) ω) *
        ((R ω * Real.exp (∑ p, (coupling β c chi w p ω).re) : ℝ) : ℂ) ∂configMeasure haarG‖
      ≤ ρ ^ A.card *
        ∫ ω, R ω * Real.exp (∑ p, (coupling β c chi w p ω).re) ∂configMeasure haarG := by
  sorry

/-- B2a. Explicit charge of a torus plaquette (discrete curl). -/
theorem torus_charge_explicit {m n N : ℕ} (σ : TorusEdge m n → ZMod N) (p : Fin m × Fin n) :
    baseCharge (torusWord p) σ =
      σ (Sum.inl (p.1, p.2)) + σ (Sum.inr (finRotate m p.1, p.2))
        - σ (Sum.inl (p.1, finRotate n p.2)) - σ (Sum.inr (p.1, p.2)) := by
  sorry

/-- B2b. On the torus the plaquette charges always sum to zero. -/
theorem torus_charge_sum {m n N : ℕ} (σ : TorusEdge m n → ZMod N) :
    ∑ p : Fin m × Fin n, baseCharge (torusWord p) σ = 0 := by
  sorry

/-- B2c. On the torus (periods at least two) every plaquette charge assignment of total charge zero is realised by
column variables. -/
theorem torus_charge_image {m n N : ℕ} (hm : 2 ≤ m) (hn : 2 ≤ n) (t : Fin m × Fin n → ZMod N)
    (ht : ∑ p, t p = 0) :
    ∃ σ : TorusEdge m n → ZMod N, ∀ p, baseCharge (torusWord p) σ = t p := by
  sorry

/-- B3. Wilson-type twist ratio on (torus `m × n`) × (finite fibre `F`), with a finite family of neutral extra terms
(complex coefficients): `Z k` multiplies the weights of the base plaquette `p₀` by `ζ ^ k` at every fibre site. -/
theorem wilson_twist_ratio_torus
    {G F X Q : Type*} [Group G] [MeasurableSpace G] [MeasurableMul₂ G] [MeasurableInv G]
    [Fintype F] [Fintype X] [Fintype Q]
    (N : ℕ) [NeZero N] (ζ : ℂ) (hζ : ζ ^ N = 1)
    (m n : ℕ) (hm : 2 ≤ m) (hn : 2 ≤ n)
    (haarG : Measure G) [IsProbabilityMeasure haarG]
    (hleft : ∀ g : G, MeasurePreserving (fun h : G => g * h) haarG haarG)
    (z : G) (hzN : z ^ N = 1) (hcentral : ∀ g : G, z * g = g * z)
    (chi : G → ℂ) (hchim : Measurable chi) (hchi1 : ∀ g, ‖chi g‖ ≤ 1)
    (hchiz : ∀ g, chi (z * g) = ζ * chi g)
    (weights : (Fin m × Fin n) → F → ℂ) (hweights : ∀ p y, ‖weights p y‖ ≤ 1)
    (β : ℝ) (hβ : 0 ≤ β)
    (wq : Q → Word (TorusEdge m n) F X) (hneutral : ∀ k, Neutral N (wq k)) (coef : Q → ℂ)
    (q : ZMod N) (ρ : ℝ)
    (hρ : ∀ t : ℂ, ‖t‖ ≤ β * (Fintype.card F : ℝ) →
      ‖∑ j : ZMod N, ζ ^ (q * j).val * ((Real.exp ((ζ ^ j.val * t).re) : ℝ) : ℂ)‖
        ≤ ρ * ∑ j : ZMod N, Real.exp ((ζ ^ j.val * t).re))
    (p₀ : Fin m × Fin n) :
    ‖∑ k : ZMod N, ζ ^ (q * k).val *
        ((∫ ω, termsWeight chi wq coef ω * Real.exp (∑ p, (coupling β
            (fun p y => if p = p₀ then ζ ^ k.val * weights p y else weights p y) chi torusWord p ω).re)
            ∂configMeasure haarG : ℝ) : ℂ)‖
      ≤ ρ ^ (m * n) *
        ∑ k : ZMod N, ∫ ω, termsWeight chi wq coef ω * Real.exp (∑ p, (coupling β
            (fun p y => if p = p₀ then ζ ^ k.val * weights p y else weights p y) chi torusWord p ω).re)
            ∂configMeasure haarG := by
  sorry

/-- B3c. B3 with the crude constant `1 - exp (-2 β |F|)` (primitive root, non-zero charge). -/
theorem wilson_twist_ratio_torus_crude
    {G F X Q : Type*} [Group G] [MeasurableSpace G] [MeasurableMul₂ G] [MeasurableInv G]
    [Fintype F] [Fintype X] [Fintype Q]
    (N : ℕ) [NeZero N] (ζ : ℂ) (hζ : IsPrimitiveRoot ζ N)
    (m n : ℕ) (hm : 2 ≤ m) (hn : 2 ≤ n)
    (haarG : Measure G) [IsProbabilityMeasure haarG]
    (hleft : ∀ g : G, MeasurePreserving (fun h : G => g * h) haarG haarG)
    (z : G) (hzN : z ^ N = 1) (hcentral : ∀ g : G, z * g = g * z)
    (chi : G → ℂ) (hchim : Measurable chi) (hchi1 : ∀ g, ‖chi g‖ ≤ 1)
    (hchiz : ∀ g, chi (z * g) = ζ * chi g)
    (weights : (Fin m × Fin n) → F → ℂ) (hweights : ∀ p y, ‖weights p y‖ ≤ 1)
    (β : ℝ) (hβ : 0 ≤ β)
    (wq : Q → Word (TorusEdge m n) F X) (hneutral : ∀ k, Neutral N (wq k)) (coef : Q → ℂ)
    (q : ZMod N) (hq : q ≠ 0) (p₀ : Fin m × Fin n) :
    ‖∑ k : ZMod N, ζ ^ (q * k).val *
        ((∫ ω, termsWeight chi wq coef ω * Real.exp (∑ p, (coupling β
            (fun p y => if p = p₀ then ζ ^ k.val * weights p y else weights p y) chi torusWord p ω).re)
            ∂configMeasure haarG : ℝ) : ℂ)‖
      ≤ (1 - Real.exp (-2 * (β * (Fintype.card F : ℝ)))) ^ (m * n) *
        ∑ k : ZMod N, ∫ ω, termsWeight chi wq coef ω * Real.exp (∑ p, (coupling β
            (fun p y => if p = p₀ then ζ ^ k.val * weights p y else weights p y) chi torusWord p ω).re)
            ∂configMeasure haarG := by
  sorry

end CentreZNFrozen

end


open Lean Elab Command Meta in
#eval show CommandElabM Unit from do
  let env ← getEnv
  let noms : List String := ["centre_flip_bound", "twist_ratio_bound", "rho_crude", "rho_two", "sharp_one_plaquette", "centre_flip_bound_crude", "twist_ratio_bound_crude", "recover_column_flip_bound", "recover_twist_ratio_bound", "mixed_word_neutral", "wilson_centre_flip_bound", "torus_charge_explicit", "torus_charge_sum", "torus_charge_image", "wilson_twist_ratio_torus", "wilson_twist_ratio_torus_crude"]
  let ren (e : Expr) : Expr := e.replace fun x => match x with
    | .const c ls => if `CentreZNFrozen |>.isPrefixOf c then some (.const (c.replacePrefix `CentreZNFrozen `CentreZN) ls) else none
    | _ => none
  let mut bons : Nat := 0
  for n in noms do
    let nf := `CentreZNFrozen ++ Name.mkSimple n
    let np := `CentreZN ++ Name.mkSimple n
    match env.find? nf, env.find? np with
    | some a, some b =>
      if ren a.type == b.type then
        bons := bons + 1
        logInfo m!"TYPE-IDENTIQUE {n}"
      else logInfo m!"TYPE-DIFFERENT {n}"
    | _, _ => logInfo m!"ABSENT {n}"
  logInfo m!"BILAN types identiques : {bons} sur {noms.length}"

#print axioms CentreZN.centre_flip_bound
#print axioms CentreZN.twist_ratio_bound
#print axioms CentreZN.rho_crude
#print axioms CentreZN.rho_two
#print axioms CentreZN.sharp_one_plaquette
#print axioms CentreZN.centre_flip_bound_crude
#print axioms CentreZN.twist_ratio_bound_crude
#print axioms CentreZN.recover_column_flip_bound
#print axioms CentreZN.recover_twist_ratio_bound
#print axioms CentreZN.mixed_word_neutral
#print axioms CentreZN.wilson_centre_flip_bound
#print axioms CentreZN.torus_charge_explicit
#print axioms CentreZN.torus_charge_sum
#print axioms CentreZN.torus_charge_image
#print axioms CentreZN.wilson_twist_ratio_torus
#print axioms CentreZN.wilson_twist_ratio_torus_crude
