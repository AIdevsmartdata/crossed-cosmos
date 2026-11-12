/-
Column-flip bound (abstract form).  Project: twisted tube, 11 November 2026.

Mathematical content.  A probability space carries, for every sign configuration `σ` on a finite set of "edges" `E`,
a measure-preserving map `τ σ` ("flip the columns where σ = -1").  Each "plaquette" `p` has a boundary `bd p ⊆ E`; its sign
is the product of the edge signs on its boundary.  The plaquette couplings `K p` are odd under the flips (they pick up the
plaquette sign), the remaining weight `R ≥ 0` is invariant, and the observable `W` (a Wilson loop bounding the set of
plaquettes `A`) picks up the product of the plaquette signs over `A`.  If the plaquette-sign map is surjective (plaquette signs
are independent, as on a planar patch with free boundary), then

    |∫ W · R · exp(∑ K)| ≤ tanh(κ)^{|A|} · ∫ R · exp(∑ K)        whenever |K p| ≤ κ.

For SU(2) Wilson theory on (planar patch) × (finite fibre with n_F sites), κ = β · n_F: this is the elementary area law.
The STATEMENT of `column_flip_bound` below is fixed by the pilot; only the proof may be changed.
-/
import Mathlib

open MeasureTheory Finset

namespace TubeArea

/-- Real value (+1 or -1) of a sign. -/
def sgn (u : ℤˣ) : ℝ := ((u : ℤ) : ℝ)

/-- Sign of a plaquette: the product of the edge signs over its boundary. -/
def plaq {E P : Type*} (bd : P → Finset E) (σ : E → ℤˣ) (p : P) : ℤˣ := ∏ e ∈ bd p, σ e

lemma cf_sgn_mul (u v : ℤˣ) : sgn (u * v) = sgn u * sgn v := by
  simp [sgn, Units.val_mul]

lemma cf_sgn_prod {I : Type*} [DecidableEq I] (B : Finset I) (t : I → ℤˣ) :
    sgn (∏ p ∈ B, t p) = ∏ p ∈ B, sgn (t p) := by
  induction B using Finset.induction_on with
  | empty => simp [sgn]
  | @insert p B hp ih => simp [hp, cf_sgn_mul, ih]

lemma cf_sum_sign (f : ℤˣ → ℝ) : (∑ u, f u) = f 1 + f (-1) := by
  have hne : (1 : ℤˣ) ≠ -1 := by
    intro h
    have hi := congrArg (fun u : ℤˣ => (u : ℤ)) h
    norm_num at hi
  rw [UnitsInt.univ]
  simp [hne]

lemma cf_exp_sum_sign (x : ℝ) :
    (∑ u : ℤˣ, Real.exp (sgn u * x)) = Real.exp x + Real.exp (-x) := by
  rw [cf_sum_sign]
  simp [sgn]

lemma cf_weighted_exp_sum_sign (x : ℝ) :
    (∑ u : ℤˣ, sgn u * Real.exp (sgn u * x)) =
      Real.tanh x * (Real.exp x + Real.exp (-x)) := by
  calc
    (∑ u : ℤˣ, sgn u * Real.exp (sgn u * x)) =
        Real.exp x - Real.exp (-x) := by
      rw [cf_sum_sign]
      simp [sgn, sub_eq_add_neg]
    _ = Real.tanh x * (Real.exp x + Real.exp (-x)) := by
      rw [Real.tanh_eq]
      exact (div_mul_cancel₀ _ (add_pos (Real.exp_pos x) (Real.exp_pos (-x))).ne').symm

/-- Monotonicity obtained directly from the exponential formula. -/
lemma cf_tanh_mono {x y : ℝ} (hxy : x ≤ y) : Real.tanh x ≤ Real.tanh y := by
  have hpos : Real.exp x ≤ Real.exp y := Real.exp_le_exp.mpr hxy
  have hneg : Real.exp (-y) ≤ Real.exp (-x) := Real.exp_le_exp.mpr (by linarith)
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

lemma cf_abs_tanh_le {x κ : ℝ} (hx : |x| ≤ κ) : |Real.tanh x| ≤ Real.tanh κ := by
  obtain ⟨hl, hu⟩ := abs_le.mp hx
  apply abs_le.mpr
  constructor
  · have h := cf_tanh_mono hl
    rw [Real.tanh_neg] at h
    exact h
  · exact cf_tanh_mono hu

/-- The unnormalised sum over independent plaquette signs. -/
noncomputable def cf_partition {P : Type*} [Fintype P] [DecidableEq P]
    (x : P → ℝ) : ℝ :=
  ∑ t : P → ℤˣ, Real.exp (∑ p, sgn (t p) * x p)

/-- The same sum with the character belonging to the set `A`. -/
noncomputable def cf_charged {P : Type*} [Fintype P] [DecidableEq P]
    (A : Finset P) (x : P → ℝ) : ℝ :=
  ∑ t : P → ℤˣ, (∏ p ∈ A, sgn (t p)) * Real.exp (∑ p, sgn (t p) * x p)

lemma cf_partition_eq {P : Type*} [Fintype P] [DecidableEq P] (x : P → ℝ) :
    cf_partition x = ∏ p, (Real.exp (x p) + Real.exp (-(x p))) := by
  classical
  calc
    cf_partition x = ∑ t : P → ℤˣ, ∏ p, Real.exp (sgn (t p) * x p) := by
      simp only [cf_partition, Real.exp_sum]
    _ = ∏ p, ∑ u : ℤˣ, Real.exp (sgn u * x p) :=
      (Fintype.prod_sum (fun p (u : ℤˣ) => Real.exp (sgn u * x p))).symm
    _ = ∏ p, (Real.exp (x p) + Real.exp (-(x p))) := by
      apply Finset.prod_congr rfl
      intro p _
      exact cf_exp_sum_sign (x p)

lemma cf_partition_nonneg {P : Type*} [Fintype P] [DecidableEq P] (x : P → ℝ) :
    0 ≤ cf_partition x := by
  rw [cf_partition_eq]
  exact Finset.prod_nonneg (fun p _ =>
    (add_pos (Real.exp_pos (x p)) (Real.exp_pos (-(x p)))).le)

lemma cf_charged_eq {P : Type*} [Fintype P] [DecidableEq P]
    (A : Finset P) (x : P → ℝ) :
    cf_charged A x = (∏ p ∈ A, Real.tanh (x p)) * cf_partition x := by
  classical
  have hterm (t : P → ℤˣ) :
      (∏ p ∈ A, sgn (t p)) * Real.exp (∑ p, sgn (t p) * x p) =
        ∏ p, ((if p ∈ A then sgn (t p) else 1) * Real.exp (sgn (t p) * x p)) := by
    simp only [Finset.prod_mul_distrib, Fintype.prod_ite_mem, Real.exp_sum]
  calc
    cf_charged A x = ∑ t : P → ℤˣ,
        ∏ p, ((if p ∈ A then sgn (t p) else 1) * Real.exp (sgn (t p) * x p)) := by
      unfold cf_charged
      exact Finset.sum_congr rfl (fun t _ => hterm t)
    _ = ∏ p, ∑ u : ℤˣ,
        ((if p ∈ A then sgn u else 1) * Real.exp (sgn u * x p)) :=
      (Fintype.prod_sum (fun p (u : ℤˣ) =>
        (if p ∈ A then sgn u else 1) * Real.exp (sgn u * x p))).symm
    _ = ∏ p, ((if p ∈ A then Real.tanh (x p) else 1) *
        (Real.exp (x p) + Real.exp (-(x p)))) := by
      apply Finset.prod_congr rfl
      intro p _
      by_cases hp : p ∈ A
      · simpa only [if_pos hp] using cf_weighted_exp_sum_sign (x p)
      · simpa only [if_neg hp, one_mul] using cf_exp_sum_sign (x p)
    _ = (∏ p ∈ A, Real.tanh (x p)) * cf_partition x := by
      rw [Finset.prod_mul_distrib, Fintype.prod_ite_mem, cf_partition_eq]

lemma cf_charged_bound {P : Type*} [Fintype P] [DecidableEq P]
    (A : Finset P) (x : P → ℝ) (κ : ℝ) (hx : ∀ p, |x p| ≤ κ) :
    |cf_charged A x| ≤ Real.tanh κ ^ A.card * cf_partition x := by
  rw [cf_charged_eq, abs_mul, abs_of_nonneg (cf_partition_nonneg x)]
  apply mul_le_mul_of_nonneg_right _ (cf_partition_nonneg x)
  rw [Finset.abs_prod]
  calc
    (∏ p ∈ A, |Real.tanh (x p)|) ≤ ∏ _p ∈ A, Real.tanh κ :=
      Finset.prod_le_prod (fun p _ => abs_nonneg _) (fun p _ => cf_abs_tanh_le (hx p))
    _ = Real.tanh κ ^ A.card := by simp

/-- Change of variables needs no inverse for the measure preserving map. -/
lemma cf_integral_preserving {Ω : Type*} [MeasurableSpace Ω] {μ : Measure Ω}
    {T : Ω → Ω} (hT : MeasurePreserving T μ μ) (f : Ω → ℝ) (hf : Measurable f) :
    (∫ ω, f (T ω) ∂μ) = ∫ ω, f ω ∂μ := by
  have h := integral_map_of_stronglyMeasurable (μ := μ) hT.measurable hf.stronglyMeasurable
  rw [hT.map_eq] at h
  exact h.symm

theorem column_flip_bound
    {Ω E P : Type*} [MeasurableSpace Ω] [Fintype E] [DecidableEq E] [Fintype P] [DecidableEq P]
    (μ : Measure Ω) [IsProbabilityMeasure μ]
    (τ : (E → ℤˣ) → Ω → Ω) (hτ : ∀ σ, MeasurePreserving (τ σ) μ μ)
    (bd : P → Finset E)
    (hsurj : Function.Surjective (fun σ : E → ℤˣ => plaq bd σ))
    (K : P → Ω → ℝ) (hKm : ∀ p, Measurable (K p))
    (κ : ℝ) (hK : ∀ p ω, |K p ω| ≤ κ)
    (hKτ : ∀ σ p ω, K p (τ σ ω) = sgn (plaq bd σ p) * K p ω)
    (R : Ω → ℝ) (hRm : Measurable R) (hR0 : ∀ ω, 0 ≤ R ω) (hRτ : ∀ σ ω, R (τ σ ω) = R ω)
    (hRint : Integrable (fun ω => R ω * Real.exp (∑ p, K p ω)) μ)
    (W : Ω → ℝ) (hWm : Measurable W) (hW1 : ∀ ω, |W ω| ≤ 1)
    (A : Finset P)
    (hWτ : ∀ σ ω, W (τ σ ω) = sgn (∏ p ∈ A, plaq bd σ p) * W ω) :
    |∫ ω, W ω * (R ω * Real.exp (∑ p, K p ω)) ∂μ|
      ≤ Real.tanh κ ^ A.card * ∫ ω, R ω * Real.exp (∑ p, K p ω) ∂μ := by
  classical
  let D : Ω → ℝ := fun ω => R ω * Real.exp (∑ p, K p ω)
  let G : Ω → ℝ := fun ω => W ω * D ω
  let d : (P → ℤˣ) → Ω → ℝ :=
    fun t ω => R ω * Real.exp (∑ p, sgn (t p) * K p ω)
  let g : (P → ℤˣ) → Ω → ℝ :=
    fun t ω => (∏ p ∈ A, sgn (t p)) * W ω * d t ω
  let H : Ω → ℝ := fun ω => ∑ t, d t ω
  let J : Ω → ℝ := fun ω => ∑ t, g t ω
  let n : ℝ := Fintype.card (P → ℤˣ)
  let b : ℝ := Real.tanh κ ^ A.card
  have hn : 0 < n := by
    dsimp only [n]
    exact_mod_cast (Fintype.card_pos : 0 < Fintype.card (P → ℤˣ))
  have hDm : Measurable D :=
    hRm.mul (Finset.measurable_sum univ (fun p _ => hKm p)).exp
  have hGm : Measurable G := hWm.mul hDm
  have hDi : Integrable D μ := hRint
  have hD0 (ω : Ω) : 0 ≤ D ω := mul_nonneg (hR0 ω) (Real.exp_pos _).le
  have hGi : Integrable G μ := by
    apply hDi.mono' hGm.aestronglyMeasurable
    apply Filter.Eventually.of_forall
    intro ω
    change ‖W ω * D ω‖ ≤ D ω
    rw [Real.norm_eq_abs, abs_mul, abs_of_nonneg (hD0 ω)]
    simpa only [one_mul] using mul_le_mul_of_nonneg_right (hW1 ω) (hD0 ω)
  -- Pick one edge configuration for each plaquette configuration.  No uniform
  -- fibre count and no action law for the maps τ are required.
  have hprops (t : P → ℤˣ) :
      Integrable (d t) μ ∧ Integrable (g t) μ ∧
        (∫ ω, d t ω ∂μ) = (∫ ω, D ω ∂μ) ∧
        (∫ ω, g t ω ∂μ) = (∫ ω, G ω ∂μ) := by
    obtain ⟨σ, hσ⟩ := hsurj t
    have hsig (p : P) : plaq bd σ p = t p := congrFun hσ p
    have hdt : (fun ω => D (τ σ ω)) = d t := by
      funext ω
      dsimp only [D, d]
      simp only [hRτ σ, hKτ σ, hsig]
    have hgt : (fun ω => G (τ σ ω)) = g t := by
      funext ω
      change W (τ σ ω) * D (τ σ ω) =
        (∏ p ∈ A, sgn (t p)) * W ω * d t ω
      rw [hWτ σ ω, cf_sgn_prod, congrFun hdt ω]
      simp only [hsig]
    refine ⟨?_, ?_, ?_, ?_⟩
    · have h := (hτ σ).integrable_comp_of_integrable hDi
      change Integrable (fun ω => D (τ σ ω)) μ at h
      rw [hdt] at h
      exact h
    · have h := (hτ σ).integrable_comp_of_integrable hGi
      change Integrable (fun ω => G (τ σ ω)) μ at h
      rw [hgt] at h
      exact h
    · have h := cf_integral_preserving (hτ σ) D hDm
      rw [hdt] at h
      exact h
    · have h := cf_integral_preserving (hτ σ) G hGm
      rw [hgt] at h
      exact h
  have hHi : Integrable H μ :=
    integrable_finsetSum univ (fun t _ => (hprops t).1)
  have hHInt : (∫ ω, H ω ∂μ) = n * ∫ ω, D ω ∂μ := by
    calc
      (∫ ω, H ω ∂μ) = ∑ t, ∫ ω, d t ω ∂μ :=
        integral_finsetSum univ (fun t _ => (hprops t).1)
      _ = ∑ _t : P → ℤˣ, ∫ ω, D ω ∂μ :=
        Finset.sum_congr rfl (fun t _ => (hprops t).2.2.1)
      _ = n * ∫ ω, D ω ∂μ := by simp [n, nsmul_eq_mul]
  have hJInt : (∫ ω, J ω ∂μ) = n * ∫ ω, G ω ∂μ := by
    calc
      (∫ ω, J ω ∂μ) = ∑ t, ∫ ω, g t ω ∂μ :=
        integral_finsetSum univ (fun t _ => (hprops t).2.1)
      _ = ∑ _t : P → ℤˣ, ∫ ω, G ω ∂μ :=
        Finset.sum_congr rfl (fun t _ => (hprops t).2.2.2)
      _ = n * ∫ ω, G ω ∂μ := by simp [n, nsmul_eq_mul]
  have hH (ω : Ω) : H ω = R ω * cf_partition (fun p => K p ω) := by
    dsimp only [H, d, cf_partition]
    rw [Finset.mul_sum]
  have hJ (ω : Ω) : J ω = W ω * R ω * cf_charged A (fun p => K p ω) := by
    dsimp only [J, g, d, cf_charged]
    rw [Finset.mul_sum]
    apply Finset.sum_congr rfl
    intro t _
    ring
  have hpoint (ω : Ω) : |J ω| ≤ b * H ω := by
    rw [hJ ω, hH ω, abs_mul, abs_mul, abs_of_nonneg (hR0 ω)]
    have hwr : |W ω| * R ω ≤ R ω := by
      simpa only [one_mul] using mul_le_mul_of_nonneg_right (hW1 ω) (hR0 ω)
    have hc := cf_charged_bound A (fun p => K p ω) κ (fun p => hK p ω)
    calc
      |W ω| * R ω * |cf_charged A (fun p => K p ω)| ≤
          R ω * |cf_charged A (fun p => K p ω)| :=
        mul_le_mul_of_nonneg_right hwr (abs_nonneg _)
      _ ≤ R ω * (b * cf_partition (fun p => K p ω)) :=
        mul_le_mul_of_nonneg_left hc (hR0 ω)
      _ = b * (R ω * cf_partition (fun p => K p ω)) := by ring
  have hbound : |∫ ω, J ω ∂μ| ≤ b * ∫ ω, H ω ∂μ := by
    calc
      |∫ ω, J ω ∂μ| ≤ ∫ ω, b * H ω ∂μ := by
        have hp : ∀ᵐ ω ∂μ, ‖J ω‖ ≤ b * H ω :=
          Filter.Eventually.of_forall (fun ω => by
            simpa only [Real.norm_eq_abs] using hpoint ω)
        simpa only [Real.norm_eq_abs] using
          (norm_integral_le_of_norm_le (f := J) (hHi.const_mul b) hp)
      _ = b * ∫ ω, H ω ∂μ := integral_const_mul b H
  have hscaled : n * |∫ ω, G ω ∂μ| ≤ n * (b * ∫ ω, D ω ∂μ) := by
    calc
      n * |∫ ω, G ω ∂μ| = |∫ ω, J ω ∂μ| := by
        rw [hJInt, abs_mul, abs_of_pos hn]
      _ ≤ b * ∫ ω, H ω ∂μ := hbound
      _ = n * (b * ∫ ω, D ω ∂μ) := by rw [hHInt]; ring
  exact (mul_le_mul_iff_right₀ hn).mp hscaled

end TubeArea
