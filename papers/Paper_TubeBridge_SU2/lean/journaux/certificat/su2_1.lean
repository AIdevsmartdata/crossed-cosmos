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
/-
PART B (sharpness) and PART C (Wilson gauge theory) of the column-flip bound.  The harness compiles the concatenation
  PARTIE_A_gelee.lean (frozen, already proved: namespace TubeArea, theorem column_flip_bound)  ++  this file  ++  a footer.
So this file must NOT contain `import` lines and may use everything from PART A.
-/

open MeasureTheory Finset

namespace TubeArea

/-! ## PART B.  The bound is attained: one edge, one plaquette, the two-point space of signs. -/

/-- The only integer units are the two signs. -/
lemma cf_sign_cases (u : ℤˣ) : u = 1 ∨ u = -1 := by
  have hu := Finset.mem_univ u
  rw [UnitsInt.univ] at hu
  simpa using hu

/-- Sharpness of `column_flip_bound`.  On the two-point space `ℤˣ` there is a probability measure, invariant under
multiplication by any sign, for which the observable `sgn` (odd under the flip), with coupling `K = J · sgn` and
trivial remaining weight, satisfies the bound with EQUALITY (and the normalisation is positive).
STATEMENT FIXED BY THE PILOT: only the proof may be changed. -/
theorem sharp_one_edge (J : ℝ) :
    ∃ μ : Measure ℤˣ, IsProbabilityMeasure μ ∧
      (∀ u : ℤˣ, MeasurePreserving (fun ω : ℤˣ => u * ω) μ μ) ∧
      (∫ ω, sgn ω * Real.exp (J * sgn ω) ∂μ = Real.tanh J * ∫ ω, Real.exp (J * sgn ω) ∂μ) ∧
      0 < ∫ ω, Real.exp (J * sgn ω) ∂μ := by
  classical
  -- The existing measurable space on units is the comap along their value map.
  -- Supply measurable singletons locally; this does not change any measurable space.
  letI : MeasurableSingletonClass ℤˣ := by
    constructor
    intro u
    have hv : Measurable (fun v : ℤˣ => (v : ℤ)) := MeasurableSpace.le_map_comap
    have hs := hv (measurableSet_singleton (u : ℤ))
    convert hs using 1 <;> ext v <;> simp [Units.val_inj]
  let μ : Measure ℤˣ := (2 : ℝ≥0∞)⁻¹ • (Measure.dirac 1 + Measure.dirac (-1))
  have havg (f : ℤˣ → ℝ) : (∫ ω, f ω ∂μ) = (∑ u, f u) / 2 := by
    rw [cf_sum_sign]
    change (∫ ω, f ω ∂((2 : ℝ≥0∞)⁻¹ •
      (Measure.dirac 1 + Measure.dirac (-1)))) = _
    rw [integral_smul_measure,
      integral_add_measure (f := f) (integrable_dirac (by simp)) (integrable_dirac (by simp)),
      integral_dirac, integral_dirac]
    norm_num [smul_eq_mul, div_eq_mul_inv, mul_comm]
  refine ⟨μ, ?_, ?_, ?_, ?_⟩
  · constructor
    norm_num [μ]
  · intro u
    have hm : Measurable (fun ω : ℤˣ => u * ω) := measurable_of_finite _
    refine ⟨hm, ?_⟩
    dsimp only [μ]
    rw [Measure.map_smul, Measure.map_add _ _ hm,
      Measure.map_dirac' hm, Measure.map_dirac' hm]
    rcases cf_sign_cases u with rfl | rfl <;> simp [add_comm]
  · simp only [havg]
    have hw : (∑ ω : ℤˣ, sgn ω * Real.exp (J * sgn ω)) =
        Real.tanh J * (∑ ω : ℤˣ, Real.exp (J * sgn ω)) := by
      simpa only [mul_comm J, cf_exp_sum_sign] using cf_weighted_exp_sum_sign J
    rw [hw]
    ring
  · rw [havg, cf_sum_sign]
    exact div_pos (add_pos (Real.exp_pos _) (Real.exp_pos _)) (by norm_num)

/-! ## PART C.  Wilson theory for a measurable group with a central involution.

No topology is used.  Left invariance below is stated as preservation of the
measure by each left translation.  Jointly measurable multiplication and
measurable inversion suffice for all words, including negatively oriented links.
-/

/-- Configurations: long links indexed by `E × F`, and other links indexed by `X`. -/
abbrev WilsonConfig (G E F X : Type*) := ((E × F) → G) × (X → G)

/-- The independent product of the given single-link measure over all links. -/
noncomputable def wilsonMeasure {G E F X : Type*} [MeasurableSpace G]
    [Fintype E] [Fintype F] [Fintype X] (haarG : Measure G) :
    Measure (WilsonConfig G E F X) :=
  (Measure.pi fun _ : E × F => haarG).prod (Measure.pi fun _ : X => haarG)

/-- The central multiplier encoded by a sign: `1 ↦ 1`, `-1 ↦ z`. -/
def centralSign {G : Type*} [One G] (z : G) (u : ℤˣ) : G :=
  if u = 1 then 1 else z

/-- Flip every fibre link in each selected column; leave all other links fixed. -/
def columnFlip {G E F X : Type*} [Mul G] [One G]
    (z : G) (σ : E → ℤˣ) (ω : WilsonConfig G E F X) : WilsonConfig G E F X :=
  ((fun ey => centralSign z (σ ey.1) * ω.1 ey), ω.2)

/-- Positive orientation is the link itself; negative orientation is its inverse. -/
def orientedLink {G : Type*} [Inv G] : Bool → G → G
  | true, g => g
  | false, g => g⁻¹

/-- Ordered holonomy of a word, all at the same fibre site `y`.
The empty word has holonomy `1`; order is retained in this noncommutative product. -/
def wordHolonomy {G E F : Type*} [Group G] :
    List (E × Bool) → ((E × F) → G) → F → G
  | [], _, _ => 1
  | a :: w, U, y => orientedLink a.2 (U (a.1, y)) * wordHolonomy w U y

/-- Product of column signs along a word, with multiplicity and independent of orientation. -/
def wordSign {E : Type*} : List (E × Bool) → (E → ℤˣ) → ℤˣ
  | [], _ => 1
  | a :: w, σ => σ a.1 * wordSign w σ

/-- Boundary edge set.  The theorems require `Nodup` of the edge list, so passing
from the list to this finset loses no multiplicities in the sign product. -/
def wordBoundary {E : Type*} [DecidableEq E] (w : List (E × Bool)) : Finset E :=
  (w.map Prod.fst).toFinset

/-- Wilson plaquette coupling, summed over the finite fibre, with bounded real weights. -/
noncomputable def wilsonCoupling {G E F X P : Type*} [Group G] [Fintype F]
    (β : ℝ) (c : P → F → ℝ) (chi : G → ℝ) (w : P → List (E × Bool))
    (p : P) (ω : WilsonConfig G E F X) : ℝ :=
  β * ∑ y, c p y * chi (wordHolonomy (w p) ω.1 y)

/-- Wilson loop observable at the specified fibre site. -/
def wilsonLoop {G E F X : Type*} [Group G] (chi : G → ℝ)
    (wC : List (E × Bool)) (y0 : F) (ω : WilsonConfig G E F X) : ℝ :=
  chi (wordHolonomy wC ω.1 y0)

lemma cf_neg_sign_ne_one : (-1 : ℤˣ) ≠ 1 := by decide

lemma cf_centralSign_mul {G : Type*} [Group G] {z : G} (hz : z * z = 1)
    (u v : ℤˣ) : centralSign z (u * v) = centralSign z u * centralSign z v := by
  rcases cf_sign_cases u with rfl | rfl <;>
    rcases cf_sign_cases v with rfl | rfl <;>
    simp [centralSign, cf_neg_sign_ne_one, hz]

lemma cf_centralSign_central {G : Type*} [Group G] {z : G}
    (hcentral : ∀ g : G, z * g = g * z) (u : ℤˣ) (g : G) :
    centralSign z u * g = g * centralSign z u := by
  rcases cf_sign_cases u with rfl | rfl <;>
    simp [centralSign, cf_neg_sign_ne_one, hcentral]

lemma cf_centralSign_inv {G : Type*} [Group G] {z : G} (hz : z * z = 1)
    (u : ℤˣ) : (centralSign z u)⁻¹ = centralSign z u := by
  rcases cf_sign_cases u with rfl | rfl
  · simp [centralSign]
  · simpa [centralSign, cf_neg_sign_ne_one] using inv_eq_of_mul_eq_one_right hz

/-- Reversing orientation leaves the central involution factor unchanged. -/
lemma cf_orientedLink_flip {G : Type*} [Group G] {z : G} (hz : z * z = 1)
    (hcentral : ∀ g : G, z * g = g * z) (b : Bool) (u : ℤˣ) (g : G) :
    orientedLink b (centralSign z u * g) = centralSign z u * orientedLink b g := by
  cases b with
  | false =>
    change (centralSign z u * g)⁻¹ = centralSign z u * g⁻¹
    rw [mul_inv_rev, cf_centralSign_inv hz]
    exact (cf_centralSign_central hcentral u g⁻¹).symm
  | true => rfl

/-- Exact holonomy transformation.  The product of signs records the parity of
the number of flipped letters: the multiplier is `1` or `z` accordingly.
This identity itself allows repetitions; only the finset conversion needs `Nodup`. -/
lemma cf_wordHolonomy_flip {G E F : Type*} [Group G] {z : G} (hz : z * z = 1)
    (hcentral : ∀ g : G, z * g = g * z) (w : List (E × Bool))
    (σ : E → ℤˣ) (U : (E × F) → G) (y : F) :
    wordHolonomy w (fun ey => centralSign z (σ ey.1) * U ey) y =
      centralSign z (wordSign w σ) * wordHolonomy w U y := by
  induction w with
  | nil => simp [wordHolonomy, wordSign, centralSign]
  | cons a w ih =>
    change orientedLink a.2 (centralSign z (σ a.1) * U (a.1, y)) *
        wordHolonomy w (fun ey => centralSign z (σ ey.1) * U ey) y =
      centralSign z (σ a.1 * wordSign w σ) *
        (orientedLink a.2 (U (a.1, y)) * wordHolonomy w U y)
    rw [cf_orientedLink_flip hz hcentral, ih, cf_centralSign_mul hz]
    calc
      (centralSign z (σ a.1) * orientedLink a.2 (U (a.1, y))) *
          (centralSign z (wordSign w σ) * wordHolonomy w U y) =
        centralSign z (σ a.1) *
          ((orientedLink a.2 (U (a.1, y)) * centralSign z (wordSign w σ)) *
            wordHolonomy w U y) := by simp only [mul_assoc]
      _ = centralSign z (σ a.1) *
          ((centralSign z (wordSign w σ) * orientedLink a.2 (U (a.1, y))) *
            wordHolonomy w U y) := by
        rw [← cf_centralSign_central hcentral (wordSign w σ)
          (orientedLink a.2 (U (a.1, y)))]
      _ = (centralSign z (σ a.1) * centralSign z (wordSign w σ)) *
          (orientedLink a.2 (U (a.1, y)) * wordHolonomy w U y) := by
        simp only [mul_assoc]

lemma cf_wordSign_boundary {E : Type*} [DecidableEq E] (w : List (E × Bool))
    (σ : E → ℤˣ) (hw : (w.map Prod.fst).Nodup) :
    wordSign w σ = ∏ e ∈ wordBoundary w, σ e := by
  revert hw
  induction w with
  | nil =>
    intro _
    simp [wordSign, wordBoundary]
  | cons a w ih =>
    intro hw
    have hh : a.1 ∉ w.map Prod.fst ∧ (w.map Prod.fst).Nodup := by
      simpa only [List.map_cons, List.nodup_cons] using hw
    have hn : a.1 ∉ wordBoundary w := by
      simpa only [wordBoundary, List.mem_toFinset] using hh.1
    have hb : wordBoundary (a :: w) = insert a.1 (wordBoundary w) := by
      simp only [wordBoundary, List.map_cons, List.toFinset_cons]
    rw [hb, Finset.prod_insert hn]
    exact congrArg (fun u : ℤˣ => σ a.1 * u) (ih hh.2)

lemma cf_chi_centralSign {G : Type*} [Group G] {z : G} {chi : G → ℝ}
    (hodd : ∀ g, chi (z * g) = -chi g) (u : ℤˣ) (g : G) :
    chi (centralSign z u * g) = sgn u * chi g := by
  rcases cf_sign_cases u with rfl | rfl <;>
    simp [centralSign, cf_neg_sign_ne_one, sgn, hodd]

/-- Oddness of `chi` turns the holonomy multiplier into the real boundary sign. -/
lemma cf_wordCharacter_flip {G E F X : Type*} [Group G] [DecidableEq E]
    {z : G} (hz : z * z = 1) (hcentral : ∀ g : G, z * g = g * z)
    {chi : G → ℝ} (hodd : ∀ g, chi (z * g) = -chi g)
    (w : List (E × Bool)) (hw : (w.map Prod.fst).Nodup)
    (σ : E → ℤˣ) (ω : WilsonConfig G E F X) (y : F) :
    chi (wordHolonomy w (columnFlip z σ ω).1 y) =
      sgn (∏ e ∈ wordBoundary w, σ e) * chi (wordHolonomy w ω.1 y) := by
  change chi (wordHolonomy w (fun ey => centralSign z (σ ey.1) * ω.1 ey) y) = _
  rw [cf_wordHolonomy_flip hz hcentral, cf_chi_centralSign hodd,
    cf_wordSign_boundary w σ hw]

/-- Preservation of the configuration measure follows coordinate by coordinate
from left invariance.  No action law or topological Haar construction is needed. -/
lemma cf_columnFlip_preserving {G E F X : Type*} [Group G] [MeasurableSpace G]
    [Fintype E] [Fintype F] [Fintype X]
    (haarG : Measure G) [IsProbabilityMeasure haarG]
    (hleft : ∀ g : G, MeasurePreserving (fun h : G => g * h) haarG haarG)
    (z : G) (σ : E → ℤˣ) :
    MeasurePreserving (columnFlip z σ : WilsonConfig G E F X → WilsonConfig G E F X)
      (wilsonMeasure haarG) (wilsonMeasure haarG) := by
  have hU := measurePreserving_pi
    (fun _ : E × F => haarG) (fun _ : E × F => haarG)
    (fun ey => hleft (centralSign z (σ ey.1)))
  have hV := MeasurePreserving.id (Measure.pi fun _ : X => haarG)
  simpa only [columnFlip, wilsonMeasure, Prod.map] using hU.prod hV

lemma cf_measurable_orientedLink {G : Type*} [Group G] [MeasurableSpace G]
    [MeasurableInv G] (b : Bool) : Measurable (orientedLink b : G → G) := by
  cases b with
  | false => exact measurable_inv
  | true => exact measurable_id

/-- Measurability of holonomy uses evaluations, inversion, and ordered multiplication. -/
lemma cf_measurable_wordHolonomy {G E F X : Type*} [Group G] [MeasurableSpace G]
    [MeasurableMul₂ G] [MeasurableInv G] (w : List (E × Bool)) (y : F) :
    Measurable (fun ω : WilsonConfig G E F X => wordHolonomy w ω.1 y) := by
  induction w with
  | nil => exact measurable_const
  | cons a w ih =>
    exact ((cf_measurable_orientedLink a.2).comp
      ((measurable_pi_apply (a.1, y)).comp measurable_fst)).mul ih

lemma cf_measurable_wilsonCoupling {G E F X P : Type*} [Group G] [MeasurableSpace G]
    [MeasurableMul₂ G] [MeasurableInv G] [Fintype F]
    (β : ℝ) (c : P → F → ℝ) (chi : G → ℝ) (hchi : Measurable chi)
    (w : P → List (E × Bool)) (p : P) :
    Measurable (wilsonCoupling β c chi w p : WilsonConfig G E F X → ℝ) := by
  exact (Finset.measurable_sum univ (fun y _ =>
    (hchi.comp (cf_measurable_wordHolonomy (w p) y)).const_mul (c p y))).const_mul β

lemma cf_wilsonCoupling_bound {G E F X P : Type*} [Group G] [Fintype F]
    (β : ℝ) (hβ : 0 ≤ β) (c : P → F → ℝ) (hc : ∀ p y, |c p y| ≤ 1)
    (chi : G → ℝ) (hchi : ∀ g, |chi g| ≤ 1) (w : P → List (E × Bool))
    (p : P) (ω : WilsonConfig G E F X) :
    |wilsonCoupling β c chi w p ω| ≤ β * (Fintype.card F : ℝ) := by
  unfold wilsonCoupling
  rw [abs_mul, abs_of_nonneg hβ]
  apply mul_le_mul_of_nonneg_left _ hβ
  calc
    |∑ y, c p y * chi (wordHolonomy (w p) ω.1 y)| ≤
        ∑ y, |c p y * chi (wordHolonomy (w p) ω.1 y)| :=
      Finset.abs_sum_le_sum_abs _ _
    _ ≤ ∑ _y : F, (1 : ℝ) := by
      apply Finset.sum_le_sum
      intro y _
      rw [abs_mul]
      calc
        |c p y| * |chi (wordHolonomy (w p) ω.1 y)| ≤
            1 * |chi (wordHolonomy (w p) ω.1 y)| :=
          mul_le_mul_of_nonneg_right (hc p y) (abs_nonneg _)
        _ ≤ 1 := by simpa using hchi (wordHolonomy (w p) ω.1 y)
    _ = (Fintype.card F : ℝ) := by simp

lemma cf_wilsonCoupling_flip {G E F X P : Type*} [Group G] [Fintype F] [DecidableEq E]
    {z : G} (hz : z * z = 1) (hcentral : ∀ g : G, z * g = g * z)
    (β : ℝ) (c : P → F → ℝ) (chi : G → ℝ)
    (hodd : ∀ g, chi (z * g) = -chi g)
    (w : P → List (E × Bool)) (hw : ∀ p, ((w p).map Prod.fst).Nodup)
    (σ : E → ℤˣ) (p : P) (ω : WilsonConfig G E F X) :
    wilsonCoupling β c chi w p (columnFlip z σ ω) =
      sgn (plaq (fun p => wordBoundary (w p)) σ p) * wilsonCoupling β c chi w p ω := by
  have hchar (y : F) : chi (wordHolonomy (w p) (columnFlip z σ ω).1 y) =
      sgn (plaq (fun p => wordBoundary (w p)) σ p) *
        chi (wordHolonomy (w p) ω.1 y) :=
    cf_wordCharacter_flip hz hcentral hodd (w p) (hw p) σ ω y
  calc
    wilsonCoupling β c chi w p (columnFlip z σ ω) =
        β * ∑ y, c p y *
          (sgn (plaq (fun p => wordBoundary (w p)) σ p) *
            chi (wordHolonomy (w p) ω.1 y)) := by
      simp only [wilsonCoupling, hchar]
    _ = sgn (plaq (fun p => wordBoundary (w p)) σ p) *
        wilsonCoupling β c chi w p ω := by
      simp only [wilsonCoupling, Finset.mul_sum]
      apply Finset.sum_congr rfl
      intro y _
      ring

/-- Column-flip bound for a Wilson theory on `E × F` plus other links `X`.

`haarG` is a left-invariant probability measure on the measurable group `G`.
`z` is a central involution and `chi` is measurable, bounded by one, and odd under `z`.
Each plaquette word and the loop word has distinct underlying edges.
The bounded weights `c` and nonnegative coupling `β` give `κ = β * card F`.
The remaining nonnegative measurable weight `R` is flip invariant, and the full
weight is integrable.  `hStokes` specifies the loop's boundary character, and
`hsurj` says that all plaquette sign assignments can be realised by column signs.
The conclusion is an unnormalised integral inequality, so it also covers zero weight.
-/
theorem wilson_column_flip_bound
    {G E F X P : Type*} [Group G] [MeasurableSpace G]
    [MeasurableMul₂ G] [MeasurableInv G]
    [Fintype E] [DecidableEq E] [Fintype F] [Fintype X]
    [Fintype P] [DecidableEq P]
    (haarG : Measure G) [IsProbabilityMeasure haarG]
    (hleft : ∀ g : G, MeasurePreserving (fun h : G => g * h) haarG haarG)
    (z : G) (hz : z * z = 1) (hcentral : ∀ g : G, z * g = g * z)
    (chi : G → ℝ) (hchim : Measurable chi) (hchi1 : ∀ g, |chi g| ≤ 1)
    (hodd : ∀ g, chi (z * g) = -chi g)
    (w : P → List (E × Bool)) (hw : ∀ p, ((w p).map Prod.fst).Nodup)
    (c : P → F → ℝ) (hc : ∀ p y, |c p y| ≤ 1)
    (β : ℝ) (hβ : 0 ≤ β)
    (R : WilsonConfig G E F X → ℝ) (hRm : Measurable R) (hR0 : ∀ ω, 0 ≤ R ω)
    (hRflip : ∀ σ ω, R (columnFlip z σ ω) = R ω)
    (hRint : Integrable (fun ω => R ω * Real.exp (∑ p, wilsonCoupling β c chi w p ω))
      (wilsonMeasure haarG))
    (wC : List (E × Bool)) (hwC : (wC.map Prod.fst).Nodup) (y0 : F)
    (A : Finset P)
    (hStokes : ∀ σ : E → ℤˣ,
      (∏ e ∈ wordBoundary wC, σ e) = ∏ p ∈ A, plaq (fun p => wordBoundary (w p)) σ p)
    (hsurj : Function.Surjective
      (fun σ : E → ℤˣ => plaq (fun p => wordBoundary (w p)) σ)) :
    |∫ ω, wilsonLoop chi wC y0 ω *
        (R ω * Real.exp (∑ p, wilsonCoupling β c chi w p ω)) ∂wilsonMeasure haarG|
      ≤ Real.tanh (β * (Fintype.card F : ℝ)) ^ A.card *
        ∫ ω, R ω * Real.exp (∑ p, wilsonCoupling β c chi w p ω) ∂wilsonMeasure haarG := by
  letI : IsProbabilityMeasure (wilsonMeasure (E := E) (F := F) (X := X) haarG) := by
    unfold wilsonMeasure
    infer_instance
  have hWflip (σ : E → ℤˣ) (ω : WilsonConfig G E F X) :
      wilsonLoop chi wC y0 (columnFlip z σ ω) =
        sgn (∏ p ∈ A, plaq (fun p => wordBoundary (w p)) σ p) *
          wilsonLoop chi wC y0 ω := by
    unfold wilsonLoop
    rw [cf_wordCharacter_flip hz hcentral hodd wC hwC σ ω y0, hStokes σ]
  exact column_flip_bound (wilsonMeasure haarG) (columnFlip z)
    (cf_columnFlip_preserving haarG hleft z)
    (fun p => wordBoundary (w p)) hsurj
    (wilsonCoupling β c chi w) (cf_measurable_wilsonCoupling β c chi hchim w)
    (β * (Fintype.card F : ℝ)) (cf_wilsonCoupling_bound β hβ c hc chi hchi1 w)
    (cf_wilsonCoupling_flip hz hcentral β c chi hodd w hw)
    R hRm hR0 hRflip hRint
    (wilsonLoop chi wC y0) (hchim.comp (cf_measurable_wordHolonomy wC y0))
    (fun ω => hchi1 (wordHolonomy wC ω.1 y0)) A hWflip

end TubeArea

-- ===== PIED DE VÉRIFICATION, PARTIES A et B (harnais du pilote ; jamais écrit par le modèle) =====
namespace TubeAreaVerif
open MeasureTheory Finset
theorem enonce_canonique_A
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
      ≤ Real.tanh κ ^ A.card * ∫ ω, R ω * Real.exp (∑ p, K p ω) ∂μ :=
  TubeArea.column_flip_bound μ τ hτ bd hsurj K hKm κ hK hKτ R hRm hR0 hRτ hRint W hWm hW1 A hWτ
theorem enonce_canonique_B (J : ℝ) :
    ∃ μ : Measure ℤˣ, IsProbabilityMeasure μ ∧
      (∀ u : ℤˣ, MeasurePreserving (fun ω : ℤˣ => u * ω) μ μ) ∧
      (∫ ω, (((ω : ℤˣ) : ℤ) : ℝ) * Real.exp (J * (((ω : ℤˣ) : ℤ) : ℝ)) ∂μ
          = Real.tanh J * ∫ ω, Real.exp (J * (((ω : ℤˣ) : ℤ) : ℝ)) ∂μ) ∧
      0 < ∫ ω, Real.exp (J * (((ω : ℤˣ) : ℤ) : ℝ)) ∂μ :=
  TubeArea.sharp_one_edge J
end TubeAreaVerif
#print axioms TubeAreaVerif.enonce_canonique_A
#print axioms TubeAreaVerif.enonce_canonique_B
-- PARTIE C : le théorème doit exister et ne dépendre que des axiomes standard (son énoncé est relu à la main par le pilote).
#print axioms TubeArea.wilson_column_flip_bound
#check @TubeArea.wilson_column_flip_bound
