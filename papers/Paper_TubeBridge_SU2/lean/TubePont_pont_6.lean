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
import PublicWilson
import ConcreteSU2

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
  let μ : Measure ℤˣ := (2 : ENNReal)⁻¹ • (Measure.dirac 1 + Measure.dirac (-1))
  have havg (f : ℤˣ → ℝ) : (∫ ω, f ω ∂μ) = (∑ u, f u) / 2 := by
    rw [cf_sum_sign]
    change (∫ ω, f ω ∂((2 : ENNReal)⁻¹ •
      (Measure.dirac 1 + Measure.dirac (-1)))) = _
    rw [integral_smul_measure,
      integral_add_measure (f := f) (integrable_dirac (by simp)) (integrable_dirac (by simp)),
      integral_dirac, integral_dirac]
    norm_num [smul_eq_mul, div_eq_mul_inv, mul_comm]
  refine ⟨μ, ?_, ?_, ?_, ?_⟩
  · constructor
    norm_num [μ]
    exact ENNReal.inv_two_add_inv_two
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
  have hmap : (columnFlip z σ : WilsonConfig G E F X → WilsonConfig G E F X) =
      Prod.map (fun U : E × F → G => fun ey => centralSign z (σ ey.1) * U ey)
        (id : (X → G) → (X → G)) := by
    funext ω
    rcases ω with ⟨U, V⟩
    rfl
  rw [hmap]
  exact hU.prod hV

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
/-
PART D: the explicit rectangular patch.  The harness compiles the concatenation
  PARTIE_ABC_gelee.lean (frozen: column_flip_bound, sharp_one_edge, wilson_column_flip_bound)  ++  this file  ++  a footer.
So this file must NOT contain `import` lines and may use everything from the frozen parts.
-/

open MeasureTheory Finset

namespace TubeArea

/-- Vertices `(i,j)` with `0 ≤ i ≤ m` and `0 ≤ j ≤ n`. -/
abbrev GridVertex (m n : ℕ) := Fin (m + 1) × Fin (n + 1)

/-- Unoriented edges of the free rectangular grid.  The left summand is
horizontal, the right summand vertical. -/
abbrev GridEdge (m n : ℕ) :=
  (Fin m × Fin (n + 1)) ⊕ (Fin (m + 1) × Fin n)

/-- The horizontal edge from `(i,j)` to `(i+1,j)`. -/
def gridH {m n : ℕ} (i : Fin m) (j : Fin (n + 1)) : GridEdge m n :=
  Sum.inl (i, j)

/-- The vertical edge from `(i,j)` to `(i,j+1)`. -/
def gridV {m n : ℕ} (i : Fin (m + 1)) (j : Fin n) : GridEdge m n :=
  Sum.inr (i, j)

/-- The four literal boundary edges of the plaquette with lower-left corner `p`.
`castSucc` keeps a coordinate; `succ` adds one to it. -/
def gridBd {m n : ℕ} (p : Fin m × Fin n) : Finset (GridEdge m n) :=
  {gridH p.1 p.2.castSucc, gridH p.1 p.2.succ,
    gridV p.1.castSucc p.2, gridV p.1.succ p.2}

lemma grid_castSucc_ne_succ {k : ℕ} (i : Fin k) : i.castSucc ≠ i.succ := by
  intro h
  have hv := congrArg Fin.val h
  change i.val = i.val + 1 at hv
  omega

lemma grid_sign_square (u : ℤˣ) : u * u = 1 := by
  rcases cf_sign_cases u with rfl | rfl <;> simp

lemma grid_sign_inv (u : ℤˣ) : u⁻¹ = u := by
  rcases cf_sign_cases u with rfl | rfl <;> simp

lemma grid_plaq_eq {m n : ℕ} (σ : GridEdge m n → ℤˣ) (i : Fin m) (j : Fin n) :
    plaq gridBd σ (i, j) =
      (σ (gridH i j.castSucc) * σ (gridH i j.succ)) *
        (σ (gridV i.castSucc j) * σ (gridV i.succ j)) := by
  have hi := grid_castSucc_ne_succ i
  have hj := grid_castSucc_ne_succ j
  have hi' : i.succ ≠ i.castSucc := fun h => hi h.symm
  have hj' : j.succ ≠ j.castSucc := fun h => hj h.symm
  simp [plaq, gridBd, gridH, gridV, hi, hj, hi', hj', mul_assoc]

/-- Product of the target signs below height `r` in column `i`.
The extra `if` merely makes this a function of every natural `r`; all its uses
on grid edges have `r ≤ n`. -/
def gridPrefix {m n : ℕ} (t : Fin m × Fin n → ℤˣ) (i : Fin m) (r : ℕ) : ℤˣ :=
  ∏ k ∈ Finset.range r, if hk : k < n then t (i, ⟨k, hk⟩) else 1

lemma gridPrefix_succ {m n : ℕ} (t : Fin m × Fin n → ℤˣ)
    (i : Fin m) (j : Fin n) :
    gridPrefix t i (j.val + 1) = gridPrefix t i j.val * t (i, j) := by
  unfold gridPrefix
  rw [Finset.prod_range_succ]
  simp [j.isLt]

/-- Every assignment of plaquette signs is realised by edge signs.
Vertical edges are `1`; a horizontal edge receives the prefix product below it.
This includes grids with zero rows or zero columns. -/
theorem grid_plaq_surjective (m n : ℕ) :
    Function.Surjective (fun σ : GridEdge m n → ℤˣ => plaq gridBd σ) := by
  intro t
  let σ : GridEdge m n → ℤˣ := fun e =>
    match e with
    | Sum.inl ij => gridPrefix t ij.1 ij.2.val
    | Sum.inr _ => 1
  refine ⟨σ, ?_⟩
  funext p
  rcases p with ⟨i, j⟩
  change plaq gridBd σ (i, j) = t (i, j)
  rw [grid_plaq_eq]
  change (gridPrefix t i j.val * gridPrefix t i (j.val + 1)) * (1 * 1) = t (i, j)
  rw [gridPrefix_succ]
  simp only [mul_one, ← mul_assoc, grid_sign_square, one_mul]

/-- Grid indices in the half-open natural interval `[a,b)`.
Using a filter makes its membership condition literal, even for an empty interval. -/
def gridInterval (k a b : ℕ) : Finset (Fin k) :=
  Finset.univ.filter (fun i => a ≤ i.val ∧ i.val < b)

lemma mem_gridInterval {k a b : ℕ} (i : Fin k) :
    i ∈ gridInterval k a b ↔ a ≤ i.val ∧ i.val < b := by
  simp [gridInterval]

lemma gridInterval_card (k a b : ℕ) (hb : b ≤ k) :
    (gridInterval k a b).card = b - a := by
  have hcard : (gridInterval k a b).card = (Finset.Ico a b).card := by
    apply Finset.card_bij (fun i _ => i.val)
    · intro i hi
      exact Finset.mem_Ico.mpr ((mem_gridInterval i).mp hi)
    · intro i _ j _ hij
      exact Fin.ext hij
    · intro r hr
      have hr' := Finset.mem_Ico.mp hr
      have hrk : r < k := by omega
      refine ⟨⟨r, hrk⟩, ?_, rfl⟩
      exact (mem_gridInterval ⟨r, hrk⟩).mpr hr'
  simpa only [Nat.card_Ico] using hcard

lemma gridInterval_prod {M : Type*} [CommMonoid M]
    (k a b : ℕ) (hb : b ≤ k) (f : ℕ → M) :
    (∏ i ∈ gridInterval k a b, f i.val) = ∏ r ∈ Finset.Ico a b, f r := by
  apply Finset.prod_bij (fun i _ => i.val)
  · intro i hi
    exact Finset.mem_Ico.mpr ((mem_gridInterval i).mp hi)
  · intro i _ j _ hij
    exact Fin.ext hij
  · intro r hr
    have hr' := Finset.mem_Ico.mp hr
    have hrk : r < k := by omega
    refine ⟨⟨r, hrk⟩, ?_, rfl⟩
    exact (mem_gridInterval ⟨r, hrk⟩).mpr hr'
  · intro _ _
    rfl

lemma grid_sign_telescope (f : ℕ → ℤˣ) {a b : ℕ} (hab : a ≤ b) :
    (∏ r ∈ Finset.Ico a b, f r * f (r + 1)) = f a * f b := by
  calc
    (∏ r ∈ Finset.Ico a b, f r * f (r + 1)) =
        ∏ r ∈ Finset.Ico a b, f (r + 1) / f r := by
      apply Finset.prod_congr rfl
      intro r _
      simp only [div_eq_mul_inv, grid_sign_inv, mul_comm]
    _ = f b / f a := Finset.prod_Ico_div f hab
    _ = f a * f b := by simp only [div_eq_mul_inv, grid_sign_inv, mul_comm]

/-- Extend a finite sequence of vertex signs to natural indices, using `1`
outside its domain.  Only values inside the domain enter the telescope. -/
def gridExtend {k : ℕ} (f : Fin (k + 1) → ℤˣ) (r : ℕ) : ℤˣ :=
  if hr : r < k + 1 then f ⟨r, hr⟩ else 1

lemma gridExtend_at {k : ℕ} (f : Fin (k + 1) → ℤˣ) (i : Fin (k + 1)) :
    gridExtend f i.val = f i := by
  simp [gridExtend, i.isLt]

lemma grid_interval_telescope {k : ℕ} (f : Fin (k + 1) → ℤˣ)
    (a b : Fin (k + 1)) (hab : a.val ≤ b.val) :
    (∏ i ∈ gridInterval k a.val b.val, f i.castSucc * f i.succ) = f a * f b := by
  have hb : b.val ≤ k := by have h := b.isLt; omega
  have hl (i : Fin k) : gridExtend f i.val = f i.castSucc :=
    gridExtend_at f i.castSucc
  have hr (i : Fin k) : gridExtend f (i.val + 1) = f i.succ :=
    gridExtend_at f i.succ
  calc
    (∏ i ∈ gridInterval k a.val b.val, f i.castSucc * f i.succ) =
        ∏ i ∈ gridInterval k a.val b.val,
          gridExtend f i.val * gridExtend f (i.val + 1) := by
      apply Finset.prod_congr rfl
      intro i _
      rw [hl, hr]
    _ = ∏ r ∈ Finset.Ico a.val b.val,
          gridExtend f r * gridExtend f (r + 1) :=
      gridInterval_prod k a.val b.val hb
        (fun r => gridExtend f r * gridExtend f (r + 1))
    _ = gridExtend f a.val * gridExtend f b.val := grid_sign_telescope _ hab
    _ = f a * f b := by rw [gridExtend_at, gridExtend_at]

/-- Plaquettes of `[a,b] × [c,d]`: precisely `a ≤ i < b` and `c ≤ j < d`.
Endpoints are vertex indices, so their upper bounds by `m` and `n` are in their
`Fin` types rather than supplied as extra proof arguments. -/
def rectPlaquettes {m n : ℕ} (a b : Fin (m + 1)) (c d : Fin (n + 1)) :
    Finset (Fin m × Fin n) :=
  (gridInterval m a.val b.val) ×ˢ (gridInterval n c.val d.val)

lemma mem_rectPlaquettes {m n : ℕ} (a b : Fin (m + 1)) (c d : Fin (n + 1))
    (p : Fin m × Fin n) :
    p ∈ rectPlaquettes a b c d ↔
      (a.val ≤ p.1.val ∧ p.1.val < b.val) ∧ (c.val ≤ p.2.val ∧ p.2.val < d.val) := by
  simp [rectPlaquettes, mem_gridInterval]

lemma rectPlaquettes_card {m n : ℕ} (a b : Fin (m + 1)) (c d : Fin (n + 1)) :
    (rectPlaquettes a b c d).card = (b.val - a.val) * (d.val - c.val) := by
  have hb : b.val ≤ m := by have h := b.isLt; omega
  have hd : d.val ≤ n := by have h := d.isLt; omega
  unfold rectPlaquettes
  rw [Finset.card_product, gridInterval_card m a.val b.val hb,
    gridInterval_card n c.val d.val hd]

/-- Literal union of bottom, right, top, and left edge sets.
Stokes for this set requires positive width and height: coincident sides in a
degenerate rectangle would occur only once in a finset. -/
def rectBoundary {m n : ℕ} (a b : Fin (m + 1)) (c d : Fin (n + 1)) :
    Finset (GridEdge m n) :=
  (((gridInterval m a.val b.val).image (fun i => gridH i c) ∪
    (gridInterval n c.val d.val).image (fun j => gridV b j)) ∪
    (gridInterval m a.val b.val).image (fun i => gridH i d)) ∪
    (gridInterval n c.val d.val).image (fun j => gridV a j)

/-- Counterclockwise plaquette word, starting at the lower-left corner:
bottom forwards, right forwards, top backwards, left backwards. -/
def gridWord {m n : ℕ} (p : Fin m × Fin n) : List (GridEdge m n × Bool) :=
  [(gridH p.1 p.2.castSucc, true), (gridV p.1.succ p.2, true),
    (gridH p.1 p.2.succ, false), (gridV p.1.castSucc p.2, false)]

lemma gridWord_nodup {m n : ℕ} (p : Fin m × Fin n) :
    ((gridWord p).map Prod.fst).Nodup := by
  rcases p with ⟨i, j⟩
  have hi := grid_castSucc_ne_succ i
  have hj := grid_castSucc_ne_succ j
  have hi' : i.succ ≠ i.castSucc := fun h => hi h.symm
  have hj' : j.succ ≠ j.castSucc := fun h => hj h.symm
  simp [gridWord, gridH, gridV, hi, hj, hi', hj']

lemma gridWord_boundary {m n : ℕ} (p : Fin m × Fin n) :
    wordBoundary (gridWord p) = gridBd p := by
  ext e
  simp [wordBoundary, gridWord, gridBd, or_assoc, or_left_comm, or_comm]

/-- Increasing list of grid indices in `[a,b)`.  Filtering `finRange` keeps
the natural order; its underlying finset is `gridInterval`. -/
def gridIndexList (k a b : ℕ) : List (Fin k) :=
  (List.finRange k).filter (fun i => decide (a ≤ i.val ∧ i.val < b))

lemma gridIndexList_nodup (k a b : ℕ) : (gridIndexList k a b).Nodup := by
  exact List.Nodup.filter _ (List.nodup_finRange k)

lemma gridIndexList_toFinset (k a b : ℕ) :
    (gridIndexList k a b).toFinset = gridInterval k a b := by
  ext i
  simp [gridIndexList, gridInterval]

/-- Horizontal edges at a fixed row, in the order supplied by the index list. -/
def gridHSide {m n : ℕ} (l : List (Fin m)) (r : Fin (n + 1)) :
    List (GridEdge m n) := l.map (fun i => gridH i r)

/-- Vertical edges at a fixed column, in the order supplied by the index list. -/
def gridVSide {m n : ℕ} (l : List (Fin n)) (r : Fin (m + 1)) :
    List (GridEdge m n) := l.map (fun j => gridV r j)

lemma gridHSide_nodup {m n : ℕ} (l : List (Fin m)) (r : Fin (n + 1))
    (hl : l.Nodup) : (gridHSide l r).Nodup := by
  unfold gridHSide
  apply List.Nodup.map ?_ hl
  intro i j hij
  simpa [gridH] using hij

lemma gridVSide_nodup {m n : ℕ} (l : List (Fin n)) (r : Fin (m + 1))
    (hl : l.Nodup) : (gridVSide l r).Nodup := by
  unfold gridVSide
  apply List.Nodup.map ?_ hl
  intro i j hij
  simpa [gridV] using hij

lemma gridHSide_disjoint {m n : ℕ} (l l' : List (Fin m))
    (r s : Fin (n + 1)) (hrs : r ≠ s) :
    List.Disjoint (gridHSide l r) (gridHSide l' s) := by
  apply List.disjoint_left.mpr
  intro e he he'
  obtain ⟨i, _, hi⟩ := List.mem_map.mp he
  obtain ⟨j, _, hj⟩ := List.mem_map.mp he'
  have hp : i = j ∧ r = s := by simpa [gridH] using hi.trans hj.symm
  exact hrs hp.2

lemma gridVSide_disjoint {m n : ℕ} (l l' : List (Fin n))
    (r s : Fin (m + 1)) (hrs : r ≠ s) :
    List.Disjoint (gridVSide l r) (gridVSide l' s) := by
  apply List.disjoint_left.mpr
  intro e he he'
  obtain ⟨i, _, hi⟩ := List.mem_map.mp he
  obtain ⟨j, _, hj⟩ := List.mem_map.mp he'
  have hp : r = s ∧ i = j := by simpa [gridV] using hi.trans hj.symm
  exact hrs hp.1

lemma gridHVSide_disjoint {m n : ℕ} (l : List (Fin m)) (l' : List (Fin n))
    (r : Fin (n + 1)) (s : Fin (m + 1)) :
    List.Disjoint (gridHSide l r) (gridVSide l' s) := by
  apply List.disjoint_left.mpr
  intro e he he'
  obtain ⟨i, _, hi⟩ := List.mem_map.mp he
  obtain ⟨j, _, hj⟩ := List.mem_map.mp he'
  simpa [gridH, gridV] using hi.trans hj.symm

lemma gridVHSide_disjoint {m n : ℕ} (l : List (Fin n)) (l' : List (Fin m))
    (r : Fin (m + 1)) (s : Fin (n + 1)) :
    List.Disjoint (gridVSide l r) (gridHSide l' s) := by
  apply List.disjoint_left.mpr
  intro e he he'
  exact (List.disjoint_left.mp (gridHVSide_disjoint l' l s r)) he' he

lemma grid_four_lists_nodup {E : Type*} (B R T L : List E)
    (hB : B.Nodup) (hR : R.Nodup) (hT : T.Nodup) (hL : L.Nodup)
    (hBR : List.Disjoint B R) (hBT : List.Disjoint B T) (hBL : List.Disjoint B L)
    (hRT : List.Disjoint R T) (hRL : List.Disjoint R L) (hTL : List.Disjoint T L) :
    (((B ++ R) ++ T.reverse) ++ L.reverse).Nodup := by
  simp only [List.nodup_append', List.nodup_reverse, List.disjoint_left,
    List.mem_append, List.mem_reverse] at *
  aesop

/-- Counterclockwise rectangle word starting at `(a,c)`: bottom and right
in increasing order and with positive orientation, then top and left in
decreasing order and with negative orientation. -/
def rectWord {m n : ℕ} (a b : Fin (m + 1)) (c d : Fin (n + 1)) :
    List (GridEdge m n × Bool) :=
  (((gridHSide (gridIndexList m a.val b.val) c).map (fun e => (e, true)) ++
    (gridVSide (gridIndexList n c.val d.val) b).map (fun e => (e, true))) ++
    (gridHSide (gridIndexList m a.val b.val) d).reverse.map (fun e => (e, false))) ++
    (gridVSide (gridIndexList n c.val d.val) a).reverse.map (fun e => (e, false))

lemma rectWord_edges {m n : ℕ} (a b : Fin (m + 1)) (c d : Fin (n + 1)) :
    (rectWord a b c d).map Prod.fst =
      (((gridHSide (gridIndexList m a.val b.val) c ++
        gridVSide (gridIndexList n c.val d.val) b) ++
        (gridHSide (gridIndexList m a.val b.val) d).reverse) ++
        (gridVSide (gridIndexList n c.val d.val) a).reverse) := by
  simp [rectWord, List.map_append, List.map_map, Function.comp_def]

lemma rectWord_nodup {m n : ℕ} (a b : Fin (m + 1)) (c d : Fin (n + 1))
    (hab : a.val < b.val) (hcd : c.val < d.val) :
    ((rectWord a b c d).map Prod.fst).Nodup := by
  have hab' : a ≠ b := by
    intro h
    have hv := congrArg Fin.val h
    omega
  have hcd' : c ≠ d := by
    intro h
    have hv := congrArg Fin.val h
    omega
  rw [rectWord_edges]
  apply grid_four_lists_nodup
  · exact gridHSide_nodup _ _ (gridIndexList_nodup _ _ _)
  · exact gridVSide_nodup _ _ (gridIndexList_nodup _ _ _)
  · exact gridHSide_nodup _ _ (gridIndexList_nodup _ _ _)
  · exact gridVSide_nodup _ _ (gridIndexList_nodup _ _ _)
  · exact gridHVSide_disjoint _ _ _ _
  · exact gridHSide_disjoint _ _ _ _ hcd'
  · exact gridHVSide_disjoint _ _ _ _
  · exact gridVHSide_disjoint _ _ _ _
  · exact gridVSide_disjoint _ _ _ _ (fun h => hab' h.symm)
  · exact gridHVSide_disjoint _ _ _ _

lemma gridHSide_toFinset {m n : ℕ} (l : List (Fin m)) (r : Fin (n + 1)) :
    (gridHSide l r).toFinset = l.toFinset.image (fun i => gridH i r) := by
  ext e
  simp [gridHSide]

lemma gridVSide_toFinset {m n : ℕ} (l : List (Fin n)) (r : Fin (m + 1)) :
    (gridVSide l r).toFinset = l.toFinset.image (fun j => gridV r j) := by
  ext e
  simp [gridVSide]

lemma rectWord_boundary {m n : ℕ} (a b : Fin (m + 1)) (c d : Fin (n + 1)) :
    wordBoundary (rectWord a b c d) = rectBoundary a b c d := by
  unfold wordBoundary
  rw [rectWord_edges]
  simp only [List.toFinset_append, List.toFinset_reverse, gridHSide_toFinset,
    gridVSide_toFinset, gridIndexList_toFinset, rectBoundary]

lemma gridHSide_prod {m n : ℕ} (σ : GridEdge m n → ℤˣ) (a b : ℕ)
    (r : Fin (n + 1)) :
    ((gridHSide (gridIndexList m a b) r).map σ).prod =
      ∏ i ∈ gridInterval m a b, σ (gridH i r) := by
  simp only [gridHSide, List.map_map, Function.comp_def]
  simpa only [gridIndexList_toFinset] using
    (List.prod_toFinset (fun i : Fin m => σ (gridH i r)) (gridIndexList_nodup m a b)).symm

lemma gridVSide_prod {m n : ℕ} (σ : GridEdge m n → ℤˣ) (a b : ℕ)
    (r : Fin (m + 1)) :
    ((gridVSide (gridIndexList n a b) r).map σ).prod =
      ∏ j ∈ gridInterval n a b, σ (gridV r j) := by
  simp only [gridVSide, List.map_map, Function.comp_def]
  simpa only [gridIndexList_toFinset] using
    (List.prod_toFinset (fun j : Fin n => σ (gridV r j)) (gridIndexList_nodup n a b)).symm

lemma rectBoundary_prod {m n : ℕ} (a b : Fin (m + 1)) (c d : Fin (n + 1))
    (hab : a.val < b.val) (hcd : c.val < d.val) (σ : GridEdge m n → ℤˣ) :
    (∏ e ∈ rectBoundary a b c d, σ e) =
      ((∏ i ∈ gridInterval m a.val b.val, σ (gridH i c)) *
        (∏ j ∈ gridInterval n c.val d.val, σ (gridV b j))) *
        (∏ i ∈ gridInterval m a.val b.val, σ (gridH i d)) *
        (∏ j ∈ gridInterval n c.val d.val, σ (gridV a j)) := by
  calc
    (∏ e ∈ rectBoundary a b c d, σ e) =
        (((rectWord a b c d).map Prod.fst).map σ).prod := by
      rw [← rectWord_boundary]
      exact List.prod_toFinset σ (rectWord_nodup a b c d hab hcd)
    _ = _ := by
      rw [rectWord_edges]
      simp only [List.map_append, List.prod_append, List.map_reverse,
        List.prod_reverse, gridHSide_prod, gridVSide_prod]

lemma grid_column_plaq_prod {m n : ℕ} (σ : GridEdge m n → ℤˣ) (i : Fin m)
    (c d : Fin (n + 1)) (hcd : c.val ≤ d.val) :
    (∏ j ∈ gridInterval n c.val d.val, plaq gridBd σ (i, j)) =
      (σ (gridH i c) * σ (gridH i d)) *
        ((∏ j ∈ gridInterval n c.val d.val, σ (gridV i.castSucc j)) *
          (∏ j ∈ gridInterval n c.val d.val, σ (gridV i.succ j))) := by
  calc
    (∏ j ∈ gridInterval n c.val d.val, plaq gridBd σ (i, j)) =
        (∏ j ∈ gridInterval n c.val d.val,
          σ (gridH i j.castSucc) * σ (gridH i j.succ)) *
        (∏ j ∈ gridInterval n c.val d.val,
          σ (gridV i.castSucc j) * σ (gridV i.succ j)) := by
      simp only [grid_plaq_eq, Finset.prod_mul_distrib]
    _ = _ := by
      rw [grid_interval_telescope (fun r => σ (gridH i r)) c d hcd,
        Finset.prod_mul_distrib]

lemma rectPlaquettes_prod {m n : ℕ} (a b : Fin (m + 1)) (c d : Fin (n + 1))
    (hab : a.val ≤ b.val) (hcd : c.val ≤ d.val) (σ : GridEdge m n → ℤˣ) :
    (∏ p ∈ rectPlaquettes a b c d, plaq gridBd σ p) =
      ((∏ i ∈ gridInterval m a.val b.val, σ (gridH i c)) *
        (∏ i ∈ gridInterval m a.val b.val, σ (gridH i d))) *
        ((∏ j ∈ gridInterval n c.val d.val, σ (gridV a j)) *
          (∏ j ∈ gridInterval n c.val d.val, σ (gridV b j))) := by
  calc
    (∏ p ∈ rectPlaquettes a b c d, plaq gridBd σ p) =
        ∏ i ∈ gridInterval m a.val b.val,
          ∏ j ∈ gridInterval n c.val d.val, plaq gridBd σ (i, j) :=
      Finset.prod_product _ _ _
    _ = ∏ i ∈ gridInterval m a.val b.val,
        (σ (gridH i c) * σ (gridH i d)) *
          ((∏ j ∈ gridInterval n c.val d.val, σ (gridV i.castSucc j)) *
            (∏ j ∈ gridInterval n c.val d.val, σ (gridV i.succ j))) := by
      apply Finset.prod_congr rfl
      intro i _
      exact grid_column_plaq_prod σ i c d hcd
    _ = (∏ i ∈ gridInterval m a.val b.val, σ (gridH i c) * σ (gridH i d)) *
        (∏ i ∈ gridInterval m a.val b.val,
          (∏ j ∈ gridInterval n c.val d.val, σ (gridV i.castSucc j)) *
            (∏ j ∈ gridInterval n c.val d.val, σ (gridV i.succ j))) :=
      Finset.prod_mul_distrib
    _ = _ := by
      rw [Finset.prod_mul_distrib,
        grid_interval_telescope
          (fun r => ∏ j ∈ gridInterval n c.val d.val, σ (gridV r j)) a b hab]

/-- Stokes for a nondegenerate literal rectangle: each interior edge cancels
twice and each boundary edge occurs once.  Positive side lengths are necessary
for the literal set-union definition of `rectBoundary`. -/
theorem grid_stokes_rectangle {m n : ℕ} (a b : Fin (m + 1)) (c d : Fin (n + 1))
    (hab : a.val < b.val) (hcd : c.val < d.val) (σ : GridEdge m n → ℤˣ) :
    (∏ e ∈ rectBoundary a b c d, σ e) =
      ∏ p ∈ rectPlaquettes a b c d, plaq gridBd σ p := by
  rw [rectBoundary_prod a b c d hab hcd σ,
    rectPlaquettes_prod a b c d (by omega) (by omega) σ]
  ac_rfl

/-- The elementary area law on the explicit free rectangular patch times a
finite fibre.  The geometry, sign surjectivity, and absence of repeated edges
are proved above.  The analytic and group hypotheses are precisely those of
the frozen Wilson column-flip bound; the exponent is the literal rectangle area.
The endpoint types encode `b ≤ m` and `d ≤ n`. -/
theorem tube_area_law_rectangle
    {G F X : Type*} [Group G] [MeasurableSpace G]
    [MeasurableMul₂ G] [MeasurableInv G] [Fintype F] [Fintype X]
    (m n : ℕ) (a b : Fin (m + 1)) (c d : Fin (n + 1))
    (hab : a.val < b.val) (hcd : c.val < d.val)
    (haarG : Measure G) [IsProbabilityMeasure haarG]
    (hleft : ∀ g : G, MeasurePreserving (fun h : G => g * h) haarG haarG)
    (z : G) (hz : z * z = 1) (hcentral : ∀ g : G, z * g = g * z)
    (chi : G → ℝ) (hchim : Measurable chi) (hchi1 : ∀ g, |chi g| ≤ 1)
    (hodd : ∀ g, chi (z * g) = -chi g)
    (weights : (Fin m × Fin n) → F → ℝ) (hweights : ∀ p y, |weights p y| ≤ 1)
    (β : ℝ) (hβ : 0 ≤ β)
    (R : WilsonConfig G (GridEdge m n) F X → ℝ)
    (hRm : Measurable R) (hR0 : ∀ ω, 0 ≤ R ω)
    (hRflip : ∀ σ ω, R (columnFlip z σ ω) = R ω)
    (hRint : Integrable
      (fun ω => R ω * Real.exp (∑ p, wilsonCoupling β weights chi gridWord p ω))
      (wilsonMeasure haarG))
    (y0 : F) :
    |∫ ω, wilsonLoop chi (rectWord a b c d) y0 ω *
        (R ω * Real.exp (∑ p, wilsonCoupling β weights chi gridWord p ω))
        ∂wilsonMeasure haarG| ≤
      Real.tanh (β * (Fintype.card F : ℝ)) ^ ((b.val - a.val) * (d.val - c.val)) *
        ∫ ω, R ω * Real.exp (∑ p, wilsonCoupling β weights chi gridWord p ω)
          ∂wilsonMeasure haarG := by
  have hStokes (σ : GridEdge m n → ℤˣ) :
      (∏ e ∈ wordBoundary (rectWord a b c d), σ e) =
        ∏ p ∈ rectPlaquettes a b c d,
          plaq (fun p : Fin m × Fin n => wordBoundary (gridWord p)) σ p := by
    simpa only [rectWord_boundary, gridWord_boundary] using
      grid_stokes_rectangle a b c d hab hcd σ
  have hsurj : Function.Surjective
      (fun σ : GridEdge m n → ℤˣ =>
        plaq (fun p : Fin m × Fin n => wordBoundary (gridWord p)) σ) := by
    simpa only [gridWord_boundary] using grid_plaq_surjective m n
  have h := wilson_column_flip_bound (E := GridEdge m n) (P := Fin m × Fin n)
    (F := F) (X := X)
    haarG hleft z hz hcentral chi hchim hchi1 hodd
    gridWord gridWord_nodup weights hweights β hβ R hRm hR0 hRflip hRint
    (rectWord a b c d) (rectWord_nodup a b c d hab hcd) y0
    (rectPlaquettes a b c d) hStokes hsurj
  simpa only [rectPlaquettes_card] using h

end TubeArea
/-
PART E.  General words and the full Wilson-type action.
The additional action terms are literal finite words in long and other links.
Their neutrality, rather than any assumption about a remaining weight, gives
column-flip invariance.  Boundedness of chi gives integrability of the density.
-/

open MeasureTheory Finset

namespace TubeArea

/-- A general word is a list of oriented links.  A link is either a long link
`(e,y)`, in the left summand, or an other link `x`, in the right summand.
The Boolean orientation has exactly the meaning fixed by `orientedLink`. -/
abbrev GeneralWord (E F X : Type*) := List (((E × F) ⊕ X) × Bool)

/-- Ordered product of the configured links in a general word, with inverses
for negative orientations.  The empty word has holonomy one. -/
def generalHolonomy {G E F X : Type*} [Group G] :
    GeneralWord E F X → WilsonConfig G E F X → G
  | [], _ => 1
  | (Sum.inl ey, b) :: q, ω =>
      orientedLink b (ω.1 ey) * generalHolonomy q ω
  | (Sum.inr x, b) :: q, ω =>
      orientedLink b (ω.2 x) * generalHolonomy q ω

/-- Product, with multiplicity, of the column signs at the long entries.
Other entries contribute one.  Orientation does not change an integer unit
sign, since each such sign is its own inverse. -/
def generalWordSign {E F X : Type*} :
    GeneralWord E F X → (E → ℤˣ) → ℤˣ
  | [], _ => 1
  | (Sum.inl ey, _) :: q, σ => σ ey.1 * generalWordSign q σ
  | (Sum.inr _, _) :: q, σ => generalWordSign q σ

/-- A word is neutral if its sign product is one for every assignment of
column signs.  This condition involves only the word, not the configuration. -/
def NeutralWord {E F X : Type*} (q : GeneralWord E F X) : Prop :=
  ∀ σ : E → ℤˣ, generalWordSign q σ = 1

/-- Exact transformation of a general word, including repeated links and
either orientation, under a column flip. -/
lemma generalHolonomy_flip {G E F X : Type*} [Group G] {z : G}
    (hz : z * z = 1) (hcentral : ∀ g : G, z * g = g * z)
    (q : GeneralWord E F X) (σ : E → ℤˣ) (ω : WilsonConfig G E F X) :
    generalHolonomy q (columnFlip z σ ω) =
      centralSign z (generalWordSign q σ) * generalHolonomy q ω := by
  induction q with
  | nil => simp [generalHolonomy, generalWordSign, centralSign]
  | cons a q ih =>
    rcases a with ⟨l, b⟩
    cases l with
    | inl ey =>
      change orientedLink b (centralSign z (σ ey.1) * ω.1 ey) *
          generalHolonomy q (columnFlip z σ ω) =
        centralSign z (σ ey.1 * generalWordSign q σ) *
          (orientedLink b (ω.1 ey) * generalHolonomy q ω)
      rw [cf_orientedLink_flip hz hcentral, ih, cf_centralSign_mul hz]
      calc
        (centralSign z (σ ey.1) * orientedLink b (ω.1 ey)) *
            (centralSign z (generalWordSign q σ) * generalHolonomy q ω) =
          centralSign z (σ ey.1) *
            ((orientedLink b (ω.1 ey) * centralSign z (generalWordSign q σ)) *
              generalHolonomy q ω) := by simp only [mul_assoc]
        _ = centralSign z (σ ey.1) *
            ((centralSign z (generalWordSign q σ) * orientedLink b (ω.1 ey)) *
              generalHolonomy q ω) := by
          rw [← cf_centralSign_central hcentral (generalWordSign q σ)
            (orientedLink b (ω.1 ey))]
        _ = (centralSign z (σ ey.1) * centralSign z (generalWordSign q σ)) *
            (orientedLink b (ω.1 ey) * generalHolonomy q ω) := by
          simp only [mul_assoc]
    | inr x =>
      change orientedLink b (ω.2 x) * generalHolonomy q (columnFlip z σ ω) =
        centralSign z (generalWordSign q σ) *
          (orientedLink b (ω.2 x) * generalHolonomy q ω)
      rw [ih]
      calc
        orientedLink b (ω.2 x) *
            (centralSign z (generalWordSign q σ) * generalHolonomy q ω) =
          (orientedLink b (ω.2 x) * centralSign z (generalWordSign q σ)) *
            generalHolonomy q ω := by simp only [mul_assoc]
        _ = (centralSign z (generalWordSign q σ) * orientedLink b (ω.2 x)) *
            generalHolonomy q ω := by
          rw [← cf_centralSign_central hcentral (generalWordSign q σ)
            (orientedLink b (ω.2 x))]
        _ = centralSign z (generalWordSign q σ) *
            (orientedLink b (ω.2 x) * generalHolonomy q ω) := by
          simp only [mul_assoc]

/-- Every neutral word has unchanged holonomy under every column flip.
No observable or oddness assumption is used in this group identity. -/
theorem neutral_word_flip_invariant {G E F X : Type*} [Group G] {z : G}
    (hz : z * z = 1) (hcentral : ∀ g : G, z * g = g * z)
    (q : GeneralWord E F X) (hq : NeutralWord q)
    (σ : E → ℤˣ) (ω : WilsonConfig G E F X) :
    generalHolonomy q (columnFlip z σ ω) = generalHolonomy q ω := by
  rw [generalHolonomy_flip hz hcentral, hq σ]
  simp [centralSign]

/-- Consequently every function of a neutral holonomy is flip invariant. -/
lemma neutral_word_function_flip_invariant {G E F X Y : Type*} [Group G] {z : G}
    (hz : z * z = 1) (hcentral : ∀ g : G, z * g = g * z)
    (q : GeneralWord E F X) (hq : NeutralWord q) (chi : G → Y)
    (σ : E → ℤˣ) (ω : WilsonConfig G E F X) :
    chi (generalHolonomy q (columnFlip z σ ω)) = chi (generalHolonomy q ω) := by
  rw [neutral_word_flip_invariant hz hcentral q hq σ ω]

/-- The mixed plaquette: long link at `y`, other link `x`, reversed long
link in the same column at `y'`, then reversed other link `x'`. -/
def mixedWord {E F X : Type*} (e : E) (y y' : F) (x x' : X) :
    GeneralWord E F X :=
  [(Sum.inl (e, y), true), (Sum.inr x, true),
    (Sum.inl (e, y'), false), (Sum.inr x', false)]

/-- The two long entries of a mixed plaquette have the same column sign,
so their product is one, including when sites or other links coincide. -/
theorem mixedWord_neutral {E F X : Type*} (e : E) (y y' : F) (x x' : X) :
    NeutralWord (mixedWord e y y' x x') := by
  intro σ
  change σ e * (σ e * 1) = 1
  simpa only [mul_one] using grid_sign_square (σ e)

/-- Every word containing no long entry is neutral; orientations and
repetitions of its other links are unrestricted. -/
lemma no_long_word_neutral {E F X : Type*} (q : GeneralWord E F X)
    (hq : ∀ (ey : E × F) (b : Bool), (Sum.inl ey, b) ∉ q) :
    NeutralWord q := by
  revert hq
  induction q with
  | nil => intro _ σ; rfl
  | cons a q ih =>
    intro hq
    rcases a with ⟨l, b⟩
    cases l with
    | inl ey => exact False.elim (hq ey b (by simp))
    | inr x =>
      have ht : ∀ (ey : E × F) (b' : Bool), (Sum.inl ey, b') ∉ q := by
        intro ey b' hmem
        exact hq ey b' (List.mem_cons.mpr (Or.inr hmem))
      exact ih ht

/-- General holonomy is measurable by coordinate evaluation, inversion,
and multiplication.  The indexing types need not be finite here. -/
lemma measurable_generalHolonomy {G E F X : Type*} [Group G] [MeasurableSpace G]
    [MeasurableMul₂ G] [MeasurableInv G] (q : GeneralWord E F X) :
    Measurable (generalHolonomy q : WilsonConfig G E F X → G) := by
  induction q with
  | nil => exact measurable_const
  | cons a q ih =>
    rcases a with ⟨l, b⟩
    cases l with
    | inl ey =>
      exact ((cf_measurable_orientedLink b).comp
        ((measurable_pi_apply ey).comp measurable_fst)).mul ih
    | inr x =>
      exact ((cf_measurable_orientedLink b).comp
        ((measurable_pi_apply x).comp measurable_snd)).mul ih

/-- The extra action weight is exactly the exponential of the finite sum
`coef q * chi (generalHolonomy (wq q) ω)`.  Its definition imposes no bound
on the real coefficients, and no neutrality condition is built into it. -/
noncomputable def neutralActionWeight {G E F X Q : Type*} [Group G] [Fintype Q]
    (chi : G → ℝ) (wq : Q → GeneralWord E F X) (coef : Q → ℝ)
    (ω : WilsonConfig G E F X) : ℝ :=
  Real.exp (∑ q, coef q * chi (generalHolonomy (wq q) ω))

lemma measurable_neutralActionWeight {G E F X Q : Type*}
    [Group G] [MeasurableSpace G] [MeasurableMul₂ G] [MeasurableInv G] [Fintype Q]
    (chi : G → ℝ) (hchim : Measurable chi)
    (wq : Q → GeneralWord E F X) (coef : Q → ℝ) :
    Measurable (neutralActionWeight chi wq coef : WilsonConfig G E F X → ℝ) := by
  exact (Finset.measurable_sum univ (fun q _ =>
    (hchim.comp (measurable_generalHolonomy (wq q))).const_mul (coef q))).exp

lemma neutralActionWeight_pos {G E F X Q : Type*} [Group G] [Fintype Q]
    (chi : G → ℝ) (wq : Q → GeneralWord E F X) (coef : Q → ℝ)
    (ω : WilsonConfig G E F X) :
    0 < neutralActionWeight chi wq coef ω := Real.exp_pos _

lemma neutralActionWeight_flip {G E F X Q : Type*} [Group G] [Fintype Q] {z : G}
    (hz : z * z = 1) (hcentral : ∀ g : G, z * g = g * z)
    (chi : G → ℝ) (wq : Q → GeneralWord E F X)
    (hq : ∀ q, NeutralWord (wq q)) (coef : Q → ℝ)
    (σ : E → ℤˣ) (ω : WilsonConfig G E F X) :
    neutralActionWeight chi wq coef (columnFlip z σ ω) =
      neutralActionWeight chi wq coef ω := by
  unfold neutralActionWeight
  apply congrArg Real.exp
  apply Finset.sum_congr rfl
  intro q _
  rw [neutral_word_flip_invariant hz hcentral (wq q) (hq q) σ ω]

/-- A uniform finite upper bound on the extra action weight. -/
lemma neutralActionWeight_le {G E F X Q : Type*} [Group G] [Fintype Q]
    (chi : G → ℝ) (hchi1 : ∀ g, |chi g| ≤ 1)
    (wq : Q → GeneralWord E F X) (coef : Q → ℝ)
    (ω : WilsonConfig G E F X) :
    neutralActionWeight chi wq coef ω ≤ Real.exp (∑ q, |coef q|) := by
  unfold neutralActionWeight
  apply Real.exp_le_exp.mpr
  apply Finset.sum_le_sum
  intro q _
  calc
    coef q * chi (generalHolonomy (wq q) ω) ≤
        |coef q * chi (generalHolonomy (wq q) ω)| := le_abs_self _
    _ = |coef q| * |chi (generalHolonomy (wq q) ω)| := abs_mul _ _
    _ ≤ |coef q| * 1 :=
      mul_le_mul_of_nonneg_left (hchi1 _) (abs_nonneg _)
    _ = |coef q| := mul_one _

/-- The extra weight itself is integrable for every finite configuration
measure.  Neither neutrality nor oddness is needed for this assertion. -/
lemma integrable_neutralActionWeight {G E F X Q : Type*}
    [Group G] [MeasurableSpace G] [MeasurableMul₂ G] [MeasurableInv G] [Fintype Q]
    (μ : Measure (WilsonConfig G E F X)) [IsFiniteMeasure μ]
    (chi : G → ℝ) (hchim : Measurable chi) (hchi1 : ∀ g, |chi g| ≤ 1)
    (wq : Q → GeneralWord E F X) (coef : Q → ℝ) :
    Integrable (neutralActionWeight chi wq coef) μ := by
  refine (integrable_const (μ := μ) (Real.exp (∑ q, |coef q|))).mono'
    (measurable_neutralActionWeight chi hchim wq coef).aestronglyMeasurable ?_
  apply Filter.Eventually.of_forall
  intro ω
  rw [Real.norm_eq_abs, abs_of_pos (neutralActionWeight_pos chi wq coef ω)]
  exact neutralActionWeight_le chi hchi1 wq coef ω

/-- Integrability of the complete density.  The extra exponent is bounded
by `∑ q, |coef q|`; the long-plaquette exponent is bounded by the sum of
`β * card F` over all plaquettes.  Both bounds are constants. -/
lemma integrable_wilsonActionWeight {G E F X P Q : Type*}
    [Group G] [MeasurableSpace G] [MeasurableMul₂ G] [MeasurableInv G]
    [Fintype E] [Fintype F] [Fintype X] [Fintype P] [Fintype Q]
    (haarG : Measure G) [IsProbabilityMeasure haarG]
    (chi : G → ℝ) (hchim : Measurable chi) (hchi1 : ∀ g, |chi g| ≤ 1)
    (wq : Q → GeneralWord E F X) (coef : Q → ℝ)
    (β : ℝ) (hβ : 0 ≤ β) (weights : P → F → ℝ)
    (hweights : ∀ p y, |weights p y| ≤ 1) (w : P → List (E × Bool)) :
    Integrable
      (fun ω : WilsonConfig G E F X => neutralActionWeight chi wq coef ω *
        Real.exp (∑ p, wilsonCoupling β weights chi w p ω))
      (wilsonMeasure haarG) := by
  classical
  letI : IsProbabilityMeasure (wilsonMeasure (E := E) (F := F) (X := X) haarG) := by
    unfold wilsonMeasure
    infer_instance
  let C : ℝ := Real.exp (∑ q, |coef q|) *
    Real.exp (∑ _p : P, β * (Fintype.card F : ℝ))
  have hDm : Measurable (fun ω : WilsonConfig G E F X =>
      neutralActionWeight chi wq coef ω *
        Real.exp (∑ p, wilsonCoupling β weights chi w p ω)) :=
    (measurable_neutralActionWeight chi hchim wq coef).mul
      (Finset.measurable_sum univ (fun p _ =>
        cf_measurable_wilsonCoupling β weights chi hchim w p)).exp
  have hKbound (ω : WilsonConfig G E F X) :
      Real.exp (∑ p, wilsonCoupling β weights chi w p ω) ≤
        Real.exp (∑ _p : P, β * (Fintype.card F : ℝ)) := by
    apply Real.exp_le_exp.mpr
    apply Finset.sum_le_sum
    intro p _
    exact (le_abs_self _).trans
      (cf_wilsonCoupling_bound β hβ weights hweights chi hchi1 w p ω)
  refine (integrable_const (μ := wilsonMeasure haarG) C).mono'
    hDm.aestronglyMeasurable ?_
  apply Filter.Eventually.of_forall
  intro ω
  rw [Real.norm_eq_abs,
    abs_of_pos (mul_pos (neutralActionWeight_pos chi wq coef ω) (Real.exp_pos _))]
  exact mul_le_mul (neutralActionWeight_le chi hchi1 wq coef ω) (hKbound ω)
    (Real.exp_pos _).le (Real.exp_pos _).le

/-- Elementary rectangle area law for the full Wilson-type action on a
free rectangular patch times a finite fibre.  The additional terms have
arbitrary real coefficients and neutral general words.  Their explicit
exponential weight is measurable, strictly positive, flip invariant and
bounded, and the complete density is integrable, as proved above.
No hypothesis about a separate remaining weight or its integrability occurs. -/
theorem wilson_action_area_law_rectangle
    {G F X Q : Type*} [Group G] [MeasurableSpace G]
    [MeasurableMul₂ G] [MeasurableInv G] [Fintype F] [Fintype X] [Fintype Q]
    (m n : ℕ) (a b : Fin (m + 1)) (c d : Fin (n + 1))
    (hab : a.val < b.val) (hcd : c.val < d.val)
    (haarG : Measure G) [IsProbabilityMeasure haarG]
    (hleft : ∀ g : G, MeasurePreserving (fun h : G => g * h) haarG haarG)
    (z : G) (hz : z * z = 1) (hcentral : ∀ g : G, z * g = g * z)
    (chi : G → ℝ) (hchim : Measurable chi) (hchi1 : ∀ g, |chi g| ≤ 1)
    (hodd : ∀ g, chi (z * g) = -chi g)
    (weights : (Fin m × Fin n) → F → ℝ) (hweights : ∀ p y, |weights p y| ≤ 1)
    (β : ℝ) (hβ : 0 ≤ β)
    (wq : Q → GeneralWord (GridEdge m n) F X)
    (hq : ∀ q, NeutralWord (wq q)) (coef : Q → ℝ) (y0 : F) :
    |∫ ω, wilsonLoop chi (rectWord a b c d) y0 ω *
        (neutralActionWeight chi wq coef ω *
          Real.exp (∑ p, wilsonCoupling β weights chi gridWord p ω))
        ∂wilsonMeasure haarG| ≤
      Real.tanh (β * (Fintype.card F : ℝ)) ^ ((b.val - a.val) * (d.val - c.val)) *
        ∫ ω, neutralActionWeight chi wq coef ω *
          Real.exp (∑ p, wilsonCoupling β weights chi gridWord p ω)
          ∂wilsonMeasure haarG := by
  exact tube_area_law_rectangle m n a b c d hab hcd haarG hleft z hz hcentral
    chi hchim hchi1 hodd weights hweights β hβ
    (neutralActionWeight chi wq coef)
    (measurable_neutralActionWeight chi hchim wq coef)
    (fun ω => (neutralActionWeight_pos chi wq coef ω).le)
    (neutralActionWeight_flip hz hcentral chi wq hq coef)
    (integrable_wilsonActionWeight haarG chi hchim hchi1 wq coef
      β hβ weights hweights gridWord) y0

end TubeArea
/- Part F. Appended by the harness to the frozen parts A--E. -/

open MeasureTheory Finset

namespace TubeArea

/- The parity projection is used on the full sign cube.  Only its even
   summands need a change of variables; the other summands vanish. -/

lemma torusAvg_sgn_sq (u : ℤˣ) : sgn u * sgn u = 1 := by
  rcases cf_sign_cases u with rfl | rfl <;> norm_num [sgn]

lemma torusAvg_abs_sgn (u : ℤˣ) : |sgn u| = 1 := by
  rcases cf_sign_cases u with rfl | rfl <;> norm_num [sgn]

lemma torusAvg_char_compl {P : Type*} [Fintype P] [DecidableEq P]
    (A : Finset P) (t : P → ℤˣ) :
    (∏ p ∈ A, sgn (t p)) * sgn (∏ p, t p) = ∏ p ∈ Aᶜ, sgn (t p) := by
  have hs : (∏ p ∈ A, sgn (t p)) * (∏ p ∈ A, sgn (t p)) = 1 := by
    simp only [← cf_sgn_prod A t]
    exact torusAvg_sgn_sq _
  rw [cf_sgn_prod, ← Finset.prod_mul_prod_compl A (fun p => sgn (t p)),
    ← mul_assoc, hs, one_mul]

lemma torusAvg_parity_sum {P : Type*} [Fintype P] [DecidableEq P] [Nonempty P] :
    (∑ t : P → ℤˣ, sgn (∏ p, t p)) = 0 := by
  classical
  obtain ⟨p₀⟩ := ‹Nonempty P›
  have hz : (∏ p : P, Real.tanh (0 : ℝ)) = 0 :=
    Finset.prod_eq_zero (Finset.mem_univ p₀) (by simp)
  have h := cf_charged_eq (Finset.univ : Finset P) (fun _ => (0 : ℝ))
  rw [hz, zero_mul] at h
  simpa [cf_charged, ← cf_sgn_prod] using h

lemma torusAvg_integral_average
    {Ω E P : Type*} [MeasurableSpace Ω] [Fintype E] [DecidableEq E]
    [Fintype P] [DecidableEq P] [Nonempty P]
    (μ : Measure Ω)
    (τ : (E → ℤˣ) → Ω → Ω) (hτ : ∀ σ, MeasurePreserving (τ σ) μ μ)
    (bd : P → Finset E)
    (himg : ∀ t : P → ℤˣ, ∏ p, t p = 1 → ∃ σ : E → ℤˣ, ∀ p, plaq bd σ p = t p)
    (K : P → Ω → ℝ) (hKm : ∀ p, Measurable (K p))
    (hKτ : ∀ σ p ω, K p (τ σ ω) = sgn (plaq bd σ p) * K p ω)
    (R : Ω → ℝ) (hRm : Measurable R) (hR0 : ∀ ω, 0 ≤ R ω)
    (hRτ : ∀ σ ω, R (τ σ ω) = R ω)
    (hRint : Integrable (fun ω => R ω * Real.exp (∑ p, K p ω)) μ)
    (W : Ω → ℝ) (hWm : Measurable W) (hW1 : ∀ ω, |W ω| ≤ 1)
    (A : Finset P)
    (hWτ : ∀ σ ω, W (τ σ ω) = sgn (∏ p ∈ A, plaq bd σ p) * W ω) :
    Integrable (fun ω => W ω * R ω *
      (cf_charged A (fun p => K p ω) + cf_charged Aᶜ (fun p => K p ω))) μ ∧
    (Fintype.card (P → ℤˣ) : ℝ) *
      (∫ ω, W ω * (R ω * Real.exp (∑ p, K p ω)) ∂μ) =
      ∫ ω, W ω * R ω *
        (cf_charged A (fun p => K p ω) + cf_charged Aᶜ (fun p => K p ω)) ∂μ := by
  classical
  let D : Ω → ℝ := fun ω => R ω * Real.exp (∑ p, K p ω)
  let G : Ω → ℝ := fun ω => W ω * D ω
  let g : (P → ℤˣ) → Ω → ℝ := fun t ω =>
    (∏ p ∈ A, sgn (t p)) * W ω *
      (R ω * Real.exp (∑ p, sgn (t p) * K p ω))
  let F : (P → ℤˣ) → Ω → ℝ := fun t ω => (1 + sgn (∏ p, t p)) * g t ω
  have hDm : Measurable D :=
    hRm.mul (Finset.measurable_sum univ (fun p _ => hKm p)).exp
  have hGm : Measurable G := hWm.mul hDm
  have hD0 (ω : Ω) : 0 ≤ D ω := mul_nonneg (hR0 ω) (Real.exp_pos _).le
  have hGi : Integrable G μ := by
    apply hRint.mono' hGm.aestronglyMeasurable
    apply Filter.Eventually.of_forall
    intro ω
    change ‖W ω * D ω‖ ≤ D ω
    rw [Real.norm_eq_abs, abs_mul, abs_of_nonneg (hD0 ω)]
    simpa only [one_mul] using mul_le_mul_of_nonneg_right (hW1 ω) (hD0 ω)
  have hprops (t : P → ℤˣ) : Integrable (F t) μ ∧
      (∫ ω, F t ω ∂μ) = (1 + sgn (∏ p, t p)) * ∫ ω, G ω ∂μ := by
    by_cases he : ∏ p, t p = 1
    · obtain ⟨σ, hσ⟩ := himg t he
      have hgt : (fun ω => G (τ σ ω)) = g t := by
        funext ω
        dsimp only [G, D, g]
        rw [hWτ σ ω, cf_sgn_prod, hRτ σ ω]
        simp only [hKτ σ, hσ]
      have hgi : Integrable (g t) μ := by
        have hi := (hτ σ).integrable_comp_of_integrable hGi
        change Integrable (fun ω => G (τ σ ω)) μ at hi
        rw [hgt] at hi
        exact hi
      have hge : (∫ ω, g t ω ∂μ) = ∫ ω, G ω ∂μ := by
        have hi := cf_integral_preserving (hτ σ) G hGm
        rw [hgt] at hi
        exact hi
      refine ⟨hgi.const_mul _, ?_⟩
      change (∫ ω, (1 + sgn (∏ p, t p)) * g t ω ∂μ) = _
      rw [integral_const_mul, hge]
    · have ho : ∏ p, t p = -1 := (cf_sign_cases _).resolve_left he
      have hc : (1 : ℝ) + sgn (∏ p, t p) = 0 := by
        rw [ho]
        norm_num [sgn]
      constructor <;> simp only [F, hc, zero_mul, integrable_fun_zero, integral_zero]
  have hw : (∑ t : P → ℤˣ, (1 + sgn (∏ p, t p))) =
      (Fintype.card (P → ℤˣ) : ℝ) := by
    rw [Finset.sum_add_distrib, torusAvg_parity_sum]
    simp
  have hfun : (fun ω => ∑ t, F t ω) =
      (fun ω => W ω * R ω *
        (cf_charged A (fun p => K p ω) + cf_charged Aᶜ (fun p => K p ω))) := by
    funext ω
    dsimp only [F, g, cf_charged]
    rw [mul_add, Finset.mul_sum, Finset.mul_sum, ← Finset.sum_add_distrib]
    apply Finset.sum_congr rfl
    intro t _
    calc
      (1 + sgn (∏ p, t p)) * ((∏ p ∈ A, sgn (t p)) * W ω *
          (R ω * Real.exp (∑ p, sgn (t p) * K p ω))) =
          W ω * R ω * (((∏ p ∈ A, sgn (t p)) +
            (∏ p ∈ A, sgn (t p)) * sgn (∏ p, t p)) *
              Real.exp (∑ p, sgn (t p) * K p ω)) := by ring
      _ = W ω * R ω * ((∏ p ∈ A, sgn (t p)) *
            Real.exp (∑ p, sgn (t p) * K p ω)) +
          W ω * R ω * ((∏ p ∈ Aᶜ, sgn (t p)) *
            Real.exp (∑ p, sgn (t p) * K p ω)) := by
        rw [torusAvg_char_compl]
        ring
  have hfi : Integrable (fun ω => ∑ t, F t ω) μ :=
    integrable_finsetSum univ (fun t _ => (hprops t).1)
  have hint : (∫ ω, ∑ t, F t ω ∂μ) =
      (Fintype.card (P → ℤˣ) : ℝ) * ∫ ω, G ω ∂μ := by
    calc
      (∫ ω, ∑ t, F t ω ∂μ) = ∑ t, ∫ ω, F t ω ∂μ :=
        integral_finsetSum univ (fun t _ => (hprops t).1)
      _ = ∑ t : P → ℤˣ, (1 + sgn (∏ p, t p)) * ∫ ω, G ω ∂μ :=
        Finset.sum_congr rfl (fun t _ => (hprops t).2)
      _ = (∑ t : P → ℤˣ, (1 + sgn (∏ p, t p))) * ∫ ω, G ω ∂μ :=
        (Finset.sum_mul _ _ _).symm
      _ = (Fintype.card (P → ℤˣ) : ℝ) * ∫ ω, G ω ∂μ := by rw [hw]
  rw [hfun] at hfi hint
  exact ⟨hfi, hint.symm⟩

/- A bounded change of all couplings preserves integrability.  This also
   covers odd sign assignments, which need not be realised by a column flip. -/
lemma torusAvg_integrable_change
    {Ω P : Type*} [MeasurableSpace Ω] [Fintype P]
    (μ : Measure Ω) (R : Ω → ℝ) (hRm : Measurable R) (hR0 : ∀ ω, 0 ≤ R ω)
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
      Real.exp (∑ p, L p ω) ≤ Real.exp ((∑ p, K p ω) + ∑ _p : P, 2 * κ) :=
        Real.exp_le_exp.mpr hs
      _ = c * Real.exp (∑ p, K p ω) := by
        dsimp only [c]
        rw [Real.exp_add]
        ring
  rw [Real.norm_eq_abs, abs_of_nonneg (mul_nonneg (hR0 ω) (Real.exp_pos _).le)]
  calc
    R ω * Real.exp (∑ p, L p ω) ≤ R ω * (c * Real.exp (∑ p, K p ω)) :=
      mul_le_mul_of_nonneg_left he (hR0 ω)
    _ = c * (R ω * Real.exp (∑ p, K p ω)) := by ring

lemma torusAvg_full_integrable
    {Ω P : Type*} [MeasurableSpace Ω] [Fintype P] [DecidableEq P]
    (μ : Measure Ω) (R : Ω → ℝ) (hRm : Measurable R) (hR0 : ∀ ω, 0 ≤ R ω)
    (K : P → Ω → ℝ) (hKm : ∀ p, Measurable (K p))
    (κ : ℝ) (hK : ∀ p ω, |K p ω| ≤ κ)
    (hRint : Integrable (fun ω => R ω * Real.exp (∑ p, K p ω)) μ) :
    Integrable (fun ω => R ω * cf_partition (fun p => K p ω)) μ := by
  classical
  have hi (t : P → ℤˣ) :
      Integrable (fun ω => R ω * Real.exp (∑ p, sgn (t p) * K p ω)) μ := by
    apply torusAvg_integrable_change μ R hRm hR0 K κ hK hRint
      (fun p ω => sgn (t p) * K p ω)
    · intro p
      exact (hKm p).const_mul _
    · intro p ω
      simpa only [abs_mul, torusAvg_abs_sgn, one_mul] using hK p ω
  simpa only [cf_partition, Finset.mul_sum] using
    (integrable_finsetSum univ (fun t _ => hi t))

lemma torusAvg_partition_identity
    {Ω E P : Type*} [MeasurableSpace Ω] [Fintype E] [DecidableEq E]
    [Fintype P] [DecidableEq P] [Nonempty P]
    (μ : Measure Ω)
    (τ : (E → ℤˣ) → Ω → Ω) (hτ : ∀ σ, MeasurePreserving (τ σ) μ μ)
    (bd : P → Finset E)
    (himg : ∀ t : P → ℤˣ, ∏ p, t p = 1 → ∃ σ : E → ℤˣ, ∀ p, plaq bd σ p = t p)
    (K : P → Ω → ℝ) (hKm : ∀ p, Measurable (K p))
    (hKτ : ∀ σ p ω, K p (τ σ ω) = sgn (plaq bd σ p) * K p ω)
    (R : Ω → ℝ) (hRm : Measurable R) (hR0 : ∀ ω, 0 ≤ R ω)
    (hRτ : ∀ σ ω, R (τ σ ω) = R ω)
    (hRint : Integrable (fun ω => R ω * Real.exp (∑ p, K p ω)) μ) :
    Integrable (fun ω => R ω * cf_partition (fun p => K p ω) *
      (1 + ∏ p, Real.tanh (K p ω))) μ ∧
    (Fintype.card (P → ℤˣ) : ℝ) * (∫ ω, R ω * Real.exp (∑ p, K p ω) ∂μ) =
      ∫ ω, R ω * cf_partition (fun p => K p ω) * (1 + ∏ p, Real.tanh (K p ω)) ∂μ := by
  classical
  have h := torusAvg_integral_average μ τ hτ bd himg K hKm hKτ R hRm hR0 hRτ hRint
    (fun _ => 1) measurable_const (by intro ω; norm_num) ∅ (by intro σ ω; simp [sgn])
  have hf : (fun ω => (1 : ℝ) * R ω *
      (cf_charged ∅ (fun p => K p ω) + cf_charged (∅ : Finset P)ᶜ (fun p => K p ω))) =
      (fun ω => R ω * cf_partition (fun p => K p ω) * (1 + ∏ p, Real.tanh (K p ω))) := by
    funext ω
    rw [cf_charged_eq, cf_charged_eq]
    simp only [Finset.prod_empty, Finset.compl_empty, one_mul]
    ring
  simp only [hf] at h
  simpa only [one_mul] using h

lemma torusAvg_tanh_prod_bound {P : Type*} [Fintype P] [DecidableEq P]
    (A : Finset P) (x : P → ℝ) (κ : ℝ) (hx : ∀ p, |x p| ≤ κ) :
    |∏ p ∈ A, Real.tanh (x p)| ≤ Real.tanh κ ^ A.card := by
  rw [Finset.abs_prod]
  calc
    (∏ p ∈ A, |Real.tanh (x p)|) ≤ ∏ _p ∈ A, Real.tanh κ :=
      Finset.prod_le_prod (fun p _ => abs_nonneg _) (fun p _ => cf_abs_tanh_le (hx p))
    _ = Real.tanh κ ^ A.card := by simp

lemma torusAvg_card_signs {P : Type*} [Fintype P] [DecidableEq P] :
    (Fintype.card (P → ℤˣ) : ℝ) = ∏ _p : P, (2 : ℝ) := by
  calc
    (Fintype.card (P → ℤˣ) : ℝ) = cf_partition (fun _ : P => (0 : ℝ)) := by
      simp [cf_partition]
    _ = ∏ _p : P, (2 : ℝ) := by rw [cf_partition_eq]; norm_num

lemma torusAvg_partition_cosh {P : Type*} [Fintype P] [DecidableEq P] (x : P → ℝ) :
    cf_partition x = (Fintype.card (P → ℤˣ) : ℝ) * ∏ p, Real.cosh (x p) := by
  rw [cf_partition_eq, torusAvg_card_signs, ← Finset.prod_mul_distrib]
  apply Finset.prod_congr rfl
  intro p _
  rw [Real.cosh_eq]
  ring

lemma torusAvg_charged_cosh {P : Type*} [Fintype P] [DecidableEq P]
    (A : Finset P) (x : P → ℝ) :
    cf_charged A x = (Fintype.card (P → ℤˣ) : ℝ) *
      ((∏ p ∈ A, Real.sinh (x p)) * ∏ p ∈ Aᶜ, Real.cosh (x p)) := by
  rw [cf_charged_eq, torusAvg_partition_cosh,
    ← Finset.prod_mul_prod_compl A (fun p => Real.cosh (x p))]
  have hs : (∏ p ∈ A, Real.tanh (x p)) * (∏ p ∈ A, Real.cosh (x p)) =
      ∏ p ∈ A, Real.sinh (x p) := by
    rw [← Finset.prod_mul_distrib]
    apply Finset.prod_congr rfl
    intro p _
    rw [Real.tanh_eq_sinh_div_cosh]
    exact div_mul_cancel₀ _ (Real.cosh_pos _).ne'
  calc
    (∏ p ∈ A, Real.tanh (x p)) *
        ((Fintype.card (P → ℤˣ) : ℝ) *
          ((∏ p ∈ A, Real.cosh (x p)) * ∏ p ∈ Aᶜ, Real.cosh (x p))) =
        (Fintype.card (P → ℤˣ) : ℝ) *
          (((∏ p ∈ A, Real.tanh (x p)) * (∏ p ∈ A, Real.cosh (x p))) *
            ∏ p ∈ Aᶜ, Real.cosh (x p)) := by ring
    _ = _ := by rw [hs]

/-- The unscaled exact identity, with the two complementary hyperbolic terms. -/
lemma torusAvg_exact_identity
    {Ω E P : Type*} [MeasurableSpace Ω] [Fintype E] [DecidableEq E]
    [Fintype P] [DecidableEq P] [Nonempty P]
    (μ : Measure Ω)
    (τ : (E → ℤˣ) → Ω → Ω) (hτ : ∀ σ, MeasurePreserving (τ σ) μ μ)
    (bd : P → Finset E)
    (himg : ∀ t : P → ℤˣ, ∏ p, t p = 1 → ∃ σ : E → ℤˣ, ∀ p, plaq bd σ p = t p)
    (K : P → Ω → ℝ) (hKm : ∀ p, Measurable (K p))
    (hKτ : ∀ σ p ω, K p (τ σ ω) = sgn (plaq bd σ p) * K p ω)
    (R : Ω → ℝ) (hRm : Measurable R) (hR0 : ∀ ω, 0 ≤ R ω)
    (hRτ : ∀ σ ω, R (τ σ ω) = R ω)
    (hRint : Integrable (fun ω => R ω * Real.exp (∑ p, K p ω)) μ)
    (W : Ω → ℝ) (hWm : Measurable W) (hW1 : ∀ ω, |W ω| ≤ 1)
    (A : Finset P)
    (hWτ : ∀ σ ω, W (τ σ ω) = sgn (∏ p ∈ A, plaq bd σ p) * W ω) :
    (∫ ω, W ω * (R ω * Real.exp (∑ p, K p ω)) ∂μ) =
      ∫ ω, W ω * R ω *
        (((∏ p ∈ A, Real.sinh (K p ω)) * ∏ p ∈ Aᶜ, Real.cosh (K p ω)) +
          ((∏ p ∈ Aᶜ, Real.sinh (K p ω)) * ∏ p ∈ A, Real.cosh (K p ω))) ∂μ := by
  classical
  let n : ℝ := Fintype.card (P → ℤˣ)
  have hn : 0 < n := by
    dsimp only [n]
    exact_mod_cast (Fintype.card_pos : 0 < Fintype.card (P → ℤˣ))
  have hi := (torusAvg_integral_average μ τ hτ bd himg K hKm hKτ R hRm hR0 hRτ
    hRint W hWm hW1 A hWτ).2
  have hf : (fun ω => W ω * R ω *
      (cf_charged A (fun p => K p ω) + cf_charged Aᶜ (fun p => K p ω))) =
      (fun ω => n * (W ω * R ω *
        (((∏ p ∈ A, Real.sinh (K p ω)) * ∏ p ∈ Aᶜ, Real.cosh (K p ω)) +
          ((∏ p ∈ Aᶜ, Real.sinh (K p ω)) * ∏ p ∈ A, Real.cosh (K p ω))))) := by
    funext ω
    rw [torusAvg_charged_cosh, torusAvg_charged_cosh]
    simp only [compl_compl]
    dsimp only [n]
    ring
  rw [hf, integral_const_mul] at hi
  exact mul_left_cancel₀ hn.ne' hi

/-- F1. Sign averaging on a closed surface: plaquette signs have even parity and every even assignment is realised. -/
theorem torus_flip_bound
    {Ω E P : Type*} [MeasurableSpace Ω] [Fintype E] [DecidableEq E] [Fintype P] [DecidableEq P]
    (μ : Measure Ω) [IsProbabilityMeasure μ]
    (τ : (E → ℤˣ) → Ω → Ω) (hτ : ∀ σ, MeasurePreserving (τ σ) μ μ)
    (bd : P → Finset E)
    (hpar : ∀ σ : E → ℤˣ, ∏ p, plaq bd σ p = 1)
    (himg : ∀ t : P → ℤˣ, ∏ p, t p = 1 → ∃ σ : E → ℤˣ, ∀ p, plaq bd σ p = t p)
    (K : P → Ω → ℝ) (hKm : ∀ p, Measurable (K p))
    (κ : ℝ) (hK : ∀ p ω, |K p ω| ≤ κ)
    (hKτ : ∀ σ p ω, K p (τ σ ω) = sgn (plaq bd σ p) * K p ω)
    (R : Ω → ℝ) (hRm : Measurable R) (hR0 : ∀ ω, 0 ≤ R ω) (hRτ : ∀ σ ω, R (τ σ ω) = R ω)
    (hRint : Integrable (fun ω => R ω * Real.exp (∑ p, K p ω)) μ)
    (W : Ω → ℝ) (hWm : Measurable W) (hW1 : ∀ ω, |W ω| ≤ 1)
    (A : Finset P)
    (hWτ : ∀ σ ω, W (τ σ ω) = sgn (∏ p ∈ A, plaq bd σ p) * W ω) :
    (1 - Real.tanh κ ^ Fintype.card P) * |∫ ω, W ω * (R ω * Real.exp (∑ p, K p ω)) ∂μ|
      ≤ (Real.tanh κ ^ A.card + Real.tanh κ ^ (Fintype.card P - A.card)) *
          ∫ ω, R ω * Real.exp (∑ p, K p ω) ∂μ := by
  classical
  have hZ0 : 0 ≤ ∫ ω, R ω * Real.exp (∑ p, K p ω) ∂μ :=
    integral_nonneg (fun ω => mul_nonneg (hR0 ω) (Real.exp_pos _).le)
  by_cases hP : Nonempty P
  · letI : Nonempty P := hP
    obtain ⟨p₀⟩ := hP
    let ω₀ : Ω := Classical.choice (nonempty_of_isProbabilityMeasure μ)
    have hκ : 0 ≤ κ := (abs_nonneg (K p₀ ω₀)).trans (hK p₀ ω₀)
    have hq : 0 ≤ Real.tanh κ := by
      simpa only [Real.tanh_zero] using (cf_tanh_mono hκ)
    let n : ℝ := Fintype.card (P → ℤˣ)
    let b : ℝ := Real.tanh κ ^ A.card + Real.tanh κ ^ (Fintype.card P - A.card)
    let c : ℝ := 1 - Real.tanh κ ^ Fintype.card P
    let U : Ω → ℝ := fun ω => R ω * cf_partition (fun p => K p ω)
    let J : Ω → ℝ := fun ω => W ω * R ω *
      (cf_charged A (fun p => K p ω) + cf_charged Aᶜ (fun p => K p ω))
    let H : Ω → ℝ := fun ω => U ω * (1 + ∏ p, Real.tanh (K p ω))
    have hn : 0 < n := by
      dsimp only [n]
      exact_mod_cast (Fintype.card_pos : 0 < Fintype.card (P → ℤˣ))
    have hb : 0 ≤ b := add_nonneg (pow_nonneg hq _) (pow_nonneg hq _)
    have hc : 0 ≤ c := sub_nonneg.mpr (pow_le_one₀ hq (Real.tanh_lt_one κ).le)
    have hUi : Integrable U μ := torusAvg_full_integrable μ R hRm hR0 K hKm κ hK hRint
    have hU0 (ω : Ω) : 0 ≤ U ω := mul_nonneg (hR0 ω) (cf_partition_nonneg _)
    have hIA := torusAvg_integral_average μ τ hτ bd himg K hKm hKτ R hRm hR0 hRτ
      hRint W hWm hW1 A hWτ
    have hIZ := torusAvg_partition_identity μ τ hτ bd himg K hKm hKτ R hRm hR0 hRτ hRint
    have hpoint (ω : Ω) : |J ω| ≤ b * U ω := by
      have ht : |cf_charged A (fun p => K p ω) + cf_charged Aᶜ (fun p => K p ω)| ≤
          b * cf_partition (fun p => K p ω) := by
        calc
          |cf_charged A (fun p => K p ω) + cf_charged Aᶜ (fun p => K p ω)| ≤
              |cf_charged A (fun p => K p ω)| + |cf_charged Aᶜ (fun p => K p ω)| :=
            abs_add_le _ _
          _ ≤ Real.tanh κ ^ A.card * cf_partition (fun p => K p ω) +
              Real.tanh κ ^ (Aᶜ).card * cf_partition (fun p => K p ω) :=
            add_le_add (cf_charged_bound A _ κ (fun p => hK p ω))
              (cf_charged_bound Aᶜ _ κ (fun p => hK p ω))
          _ = b * cf_partition (fun p => K p ω) := by
            rw [Finset.card_compl]
            dsimp only [b]
            ring
      have hwr : |W ω| * R ω ≤ R ω := by
        simpa only [one_mul] using mul_le_mul_of_nonneg_right (hW1 ω) (hR0 ω)
      change |W ω * R ω * _| ≤ b * (R ω * cf_partition (fun p => K p ω))
      rw [abs_mul, abs_mul, abs_of_nonneg (hR0 ω)]
      calc
        |W ω| * R ω * |cf_charged A (fun p => K p ω) + cf_charged Aᶜ (fun p => K p ω)| ≤
            R ω * |cf_charged A (fun p => K p ω) + cf_charged Aᶜ (fun p => K p ω)| :=
          mul_le_mul_of_nonneg_right hwr (abs_nonneg _)
        _ ≤ R ω * (b * cf_partition (fun p => K p ω)) :=
          mul_le_mul_of_nonneg_left ht (hR0 ω)
        _ = b * (R ω * cf_partition (fun p => K p ω)) := by ring
    have hJbound : |∫ ω, J ω ∂μ| ≤ b * ∫ ω, U ω ∂μ := by
      calc
        |∫ ω, J ω ∂μ| ≤ ∫ ω, b * U ω ∂μ := by
          simpa only [Real.norm_eq_abs] using
            (norm_integral_le_of_norm_le (f := J) (hUi.const_mul b)
              (Filter.Eventually.of_forall (fun ω => by
                simpa only [Real.norm_eq_abs] using hpoint ω)))
        _ = b * ∫ ω, U ω ∂μ := integral_const_mul b U
    have hlower : c * (∫ ω, U ω ∂μ) ≤
        n * ∫ ω, R ω * Real.exp (∑ p, K p ω) ∂μ := by
      calc
        c * (∫ ω, U ω ∂μ) = ∫ ω, c * U ω ∂μ := (integral_const_mul c U).symm
        _ ≤ ∫ ω, H ω ∂μ := by
          apply integral_mono (hUi.const_mul c) hIZ.1
          intro ω
          have ht := (abs_le.mp (torusAvg_tanh_prod_bound univ
            (fun p => K p ω) κ (fun p => hK p ω))).1
          simp only [Finset.card_univ] at ht
          change c * U ω ≤ U ω * (1 + ∏ p, Real.tanh (K p ω))
          calc
            c * U ω = U ω * c := mul_comm _ _
            _ ≤ U ω * (1 + ∏ p, Real.tanh (K p ω)) := by
              apply mul_le_mul_of_nonneg_left _ (hU0 ω)
              dsimp only [c]
              linarith
        _ = n * ∫ ω, R ω * Real.exp (∑ p, K p ω) ∂μ := hIZ.2.symm
    have hscaled : n * |∫ ω, W ω * (R ω * Real.exp (∑ p, K p ω)) ∂μ| ≤
        b * ∫ ω, U ω ∂μ := by
      calc
        n * |∫ ω, W ω * (R ω * Real.exp (∑ p, K p ω)) ∂μ| =
            |n * ∫ ω, W ω * (R ω * Real.exp (∑ p, K p ω)) ∂μ| := by
          rw [abs_mul, abs_of_pos hn]
        _ = |∫ ω, J ω ∂μ| := congrArg abs hIA.2
        _ ≤ b * ∫ ω, U ω ∂μ := hJbound
    have hf : n * (c * |∫ ω, W ω * (R ω * Real.exp (∑ p, K p ω)) ∂μ|) ≤
        n * (b * ∫ ω, R ω * Real.exp (∑ p, K p ω) ∂μ) := by
      calc
        n * (c * |∫ ω, W ω * (R ω * Real.exp (∑ p, K p ω)) ∂μ|) =
            c * (n * |∫ ω, W ω * (R ω * Real.exp (∑ p, K p ω)) ∂μ|) := by ring
        _ ≤ c * (b * ∫ ω, U ω ∂μ) := mul_le_mul_of_nonneg_left hscaled hc
        _ = b * (c * ∫ ω, U ω ∂μ) := by ring
        _ ≤ b * (n * ∫ ω, R ω * Real.exp (∑ p, K p ω) ∂μ) :=
          mul_le_mul_of_nonneg_left hlower hb
        _ = n * (b * ∫ ω, R ω * Real.exp (∑ p, K p ω) ∂μ) := by ring
    exact (mul_le_mul_iff_right₀ hn).mp hf
  · letI : IsEmpty P := ⟨fun p => hP ⟨p⟩⟩
    have hA : A = ∅ := Finset.eq_empty_of_isEmpty A
    simpa [hA] using mul_nonneg (by norm_num : (0 : ℝ) ≤ 2) hZ0

lemma torusAvg_twist_partition {P : Type*} [Fintype P] [DecidableEq P]
    (p₀ : P) (x : P → ℝ) :
    cf_partition (fun p => if p = p₀ then -(x p) else x p) = cf_partition x := by
  rw [cf_partition_eq, cf_partition_eq]
  apply Finset.prod_congr rfl
  intro p _
  by_cases hp : p = p₀
  · simp only [if_pos hp, neg_neg]
    ring
  · simp only [if_neg hp]

lemma torusAvg_twist_product {P : Type*} [Fintype P] [DecidableEq P]
    (p₀ : P) (x : P → ℝ) :
    (∏ p, Real.tanh (if p = p₀ then -(x p) else x p)) = -∏ p, Real.tanh (x p) := by
  classical
  let f : P → ℝ := fun p => Real.tanh (if p = p₀ then -(x p) else x p)
  have he : (∏ p ∈ (univ : Finset P).erase p₀, f p) =
      ∏ p ∈ (univ : Finset P).erase p₀, Real.tanh (x p) := by
    apply Finset.prod_congr rfl
    intro p hp
    have hne : p ≠ p₀ := (Finset.mem_erase.mp hp).1
    simp only [f, if_neg hne]
  change (∏ p, f p) = -∏ p, Real.tanh (x p)
  rw [← Finset.mul_prod_erase univ f (Finset.mem_univ p₀), he,
    ← Finset.mul_prod_erase univ (fun p => Real.tanh (x p)) (Finset.mem_univ p₀)]
  simp [f, Real.tanh_neg]

/-- F2. Twist ratio (electric-flux free energy): flipping the sign of the coupling of ONE plaquette `p₀`. -/
theorem twist_ratio_bound
    {Ω E P : Type*} [MeasurableSpace Ω] [Fintype E] [DecidableEq E] [Fintype P] [DecidableEq P]
    (μ : Measure Ω) [IsProbabilityMeasure μ]
    (τ : (E → ℤˣ) → Ω → Ω) (hτ : ∀ σ, MeasurePreserving (τ σ) μ μ)
    (bd : P → Finset E)
    (hpar : ∀ σ : E → ℤˣ, ∏ p, plaq bd σ p = 1)
    (himg : ∀ t : P → ℤˣ, ∏ p, t p = 1 → ∃ σ : E → ℤˣ, ∀ p, plaq bd σ p = t p)
    (K : P → Ω → ℝ) (hKm : ∀ p, Measurable (K p))
    (κ : ℝ) (hK : ∀ p ω, |K p ω| ≤ κ)
    (hKτ : ∀ σ p ω, K p (τ σ ω) = sgn (plaq bd σ p) * K p ω)
    (R : Ω → ℝ) (hRm : Measurable R) (hR0 : ∀ ω, 0 ≤ R ω) (hRτ : ∀ σ ω, R (τ σ ω) = R ω)
    (hRint : Integrable (fun ω => R ω * Real.exp (∑ p, K p ω)) μ)
    (p₀ : P) :
    |(∫ ω, R ω * Real.exp (∑ p, K p ω) ∂μ)
        - ∫ ω, R ω * Real.exp (∑ p, (if p = p₀ then -(K p ω) else K p ω)) ∂μ|
      ≤ Real.tanh κ ^ Fintype.card P *
        ((∫ ω, R ω * Real.exp (∑ p, K p ω) ∂μ)
          + ∫ ω, R ω * Real.exp (∑ p, (if p = p₀ then -(K p ω) else K p ω)) ∂μ) := by
  classical
  letI : Nonempty P := ⟨p₀⟩
  let L : P → Ω → ℝ := fun p ω => if p = p₀ then -(K p ω) else K p ω
  have hLm (p : P) : Measurable (L p) := by
    by_cases hp : p = p₀
    · simpa only [L, if_pos hp] using (hKm p).fun_neg
    · simpa only [L, if_neg hp] using hKm p
  have hL (p : P) (ω : Ω) : |L p ω| ≤ κ := by
    by_cases hp : p = p₀
    · simpa only [L, if_pos hp, abs_neg] using hK p ω
    · simpa only [L, if_neg hp] using hK p ω
  have hLτ (σ : E → ℤˣ) (p : P) (ω : Ω) :
      L p (τ σ ω) = sgn (plaq bd σ p) * L p ω := by
    dsimp only [L]
    by_cases hp : p = p₀
    · simp only [if_pos hp, hKτ σ p ω]
      ring
    · simp only [if_neg hp, hKτ σ p ω]
  have hLi : Integrable (fun ω => R ω * Real.exp (∑ p, L p ω)) μ :=
    torusAvg_integrable_change μ R hRm hR0 K κ hK hRint L hLm hL
  let n : ℝ := Fintype.card (P → ℤˣ)
  let Z : ℝ := ∫ ω, R ω * Real.exp (∑ p, K p ω) ∂μ
  let Z' : ℝ := ∫ ω, R ω * Real.exp (∑ p, L p ω) ∂μ
  let U : Ω → ℝ := fun ω => R ω * cf_partition (fun p => K p ω)
  let T : Ω → ℝ := fun ω => ∏ p, Real.tanh (K p ω)
  let Hp : Ω → ℝ := fun ω => U ω * (1 + T ω)
  let Hm : Ω → ℝ := fun ω => U ω * (1 - T ω)
  have hn : 0 < n := by
    dsimp only [n]
    exact_mod_cast (Fintype.card_pos : 0 < Fintype.card (P → ℤˣ))
  have hUi : Integrable U μ := torusAvg_full_integrable μ R hRm hR0 K hKm κ hK hRint
  have hU0 (ω : Ω) : 0 ≤ U ω := mul_nonneg (hR0 ω) (cf_partition_nonneg _)
  have hp := torusAvg_partition_identity μ τ hτ bd himg K hKm hKτ R hRm hR0 hRτ hRint
  have hm := torusAvg_partition_identity μ τ hτ bd himg L hLm hLτ R hRm hR0 hRτ hLi
  have hfun : (fun ω => R ω * cf_partition (fun p => L p ω) *
      (1 + ∏ p, Real.tanh (L p ω))) = Hm := by
    funext ω
    dsimp only [L, Hm, U, T]
    rw [torusAvg_twist_partition, torusAvg_twist_product]
    ring
  simp only [hfun] at hm
  have hpi : Integrable Hp μ := hp.1
  have hmi : Integrable Hm μ := hm.1
  have hep : n * Z = ∫ ω, Hp ω ∂μ := hp.2
  have hem : n * Z' = ∫ ω, Hm ω ∂μ := hm.2
  have hsum : n * (Z + Z') = 2 * ∫ ω, U ω ∂μ := by
    calc
      n * (Z + Z') = n * Z + n * Z' := by ring
      _ = (∫ ω, Hp ω ∂μ) + ∫ ω, Hm ω ∂μ := by rw [hep, hem]
      _ = ∫ ω, Hp ω + Hm ω ∂μ := (integral_add hpi hmi).symm
      _ = ∫ ω, 2 * U ω ∂μ := by
        apply integral_congr_ae
        apply Filter.Eventually.of_forall
        intro ω
        dsimp only [Hp, Hm]
        ring
      _ = 2 * ∫ ω, U ω ∂μ := integral_const_mul 2 U
  have hdiff : n * (Z - Z') = ∫ ω, Hp ω - Hm ω ∂μ := by
    calc
      n * (Z - Z') = n * Z - n * Z' := by ring
      _ = (∫ ω, Hp ω ∂μ) - ∫ ω, Hm ω ∂μ := by rw [hep, hem]
      _ = ∫ ω, Hp ω - Hm ω ∂μ := (integral_sub hpi hmi).symm
  have hpoint (ω : Ω) : ‖Hp ω - Hm ω‖ ≤
      (2 * Real.tanh κ ^ Fintype.card P) * U ω := by
    have ht : |T ω| ≤ Real.tanh κ ^ Fintype.card P := by
      simpa only [T, Finset.card_univ] using
        torusAvg_tanh_prod_bound univ (fun p => K p ω) κ (fun p => hK p ω)
    have he : Hp ω - Hm ω = 2 * U ω * T ω := by
      dsimp only [Hp, Hm]
      ring
    rw [he, Real.norm_eq_abs, abs_mul, abs_mul,
      abs_of_nonneg (by norm_num : (0 : ℝ) ≤ 2), abs_of_nonneg (hU0 ω)]
    calc
      2 * U ω * |T ω| ≤ 2 * U ω * Real.tanh κ ^ Fintype.card P :=
        mul_le_mul_of_nonneg_left ht (mul_nonneg (by norm_num) (hU0 ω))
      _ = (2 * Real.tanh κ ^ Fintype.card P) * U ω := by ring
  have hbound : |∫ ω, Hp ω - Hm ω ∂μ| ≤
      (2 * Real.tanh κ ^ Fintype.card P) * ∫ ω, U ω ∂μ := by
    calc
      |∫ ω, Hp ω - Hm ω ∂μ| ≤ ∫ ω, (2 * Real.tanh κ ^ Fintype.card P) * U ω ∂μ := by
        simpa only [Real.norm_eq_abs] using
          (norm_integral_le_of_norm_le (f := fun ω => Hp ω - Hm ω)
            (hUi.const_mul (2 * Real.tanh κ ^ Fintype.card P))
            (Filter.Eventually.of_forall hpoint))
      _ = (2 * Real.tanh κ ^ Fintype.card P) * ∫ ω, U ω ∂μ := integral_const_mul _ U
  have hs : n * |Z - Z'| ≤ n * (Real.tanh κ ^ Fintype.card P * (Z + Z')) := by
    calc
      n * |Z - Z'| = |n * (Z - Z')| := by rw [abs_mul, abs_of_pos hn]
      _ = |∫ ω, Hp ω - Hm ω ∂μ| := congrArg abs hdiff
      _ ≤ (2 * Real.tanh κ ^ Fintype.card P) * ∫ ω, U ω ∂μ := hbound
      _ = Real.tanh κ ^ Fintype.card P * (n * (Z + Z')) := by rw [hsum]; ring
      _ = n * (Real.tanh κ ^ Fintype.card P * (Z + Z')) := by ring
  exact (mul_le_mul_iff_right₀ hn).mp hs

/-- F3. Taking n-th roots. -/
theorem le_of_forall_pow_le_const_mul_pow (a b M : ℝ) (ha : 0 ≤ a) (hb : 0 ≤ b) (hM : 0 < M)
    (h : ∀ n : ℕ, 0 < n → a ^ n ≤ M * b ^ n) : a ≤ b := by
  by_cases hbz : b = 0
  · subst b
    simpa using h 1 (by norm_num)
  have hbp : 0 < b := lt_of_le_of_ne hb (Ne.symm hbz)
  by_contra hab
  have hba : b < a := lt_of_not_ge hab
  have hr : 1 < a / b := (one_lt_div hbp).mpr hba
  obtain ⟨n, hn⟩ := pow_unbounded_of_one_lt (M + 1) hr
  have hnpos : 0 < n := by
    by_contra hnp
    have hnz : n = 0 := by omega
    rw [hnz, pow_zero] at hn
    linarith
  have hle : (a / b) ^ n ≤ M := by
    rw [div_pow]
    exact (div_le_iff₀ (pow_pos hbp n)).mpr (h n hnpos)
  linarith

/-- F4. From trace ratios to the ratio of the top eigenvalues of the two sectors. -/
theorem flux_gap_of_traces (ℓ : ℕ) (q lam0 lam1 D : ℝ)
    (hq : 0 ≤ q) (h0 : 0 ≤ lam0) (h1 : 0 ≤ lam1) (hD : 0 < D)
    (Ev Od : ℕ → ℝ)
    (hOd : ∀ n : ℕ, 0 < n → lam1 ^ n ≤ Od n)
    (hEv : ∀ n : ℕ, 0 < n → Ev n ≤ D * lam0 ^ n)
    (hratio : ∀ n : ℕ, 0 < n → Od n ≤ q ^ (n * ℓ) * Ev n) :
    lam1 ≤ q ^ ℓ * lam0 := by
  apply le_of_forall_pow_le_const_mul_pow lam1 (q ^ ℓ * lam0) D h1
    (mul_nonneg (pow_nonneg hq _) h0) hD
  intro n hn
  calc
    lam1 ^ n ≤ Od n := hOd n hn
    _ ≤ q ^ (n * ℓ) * Ev n := hratio n hn
    _ ≤ q ^ (n * ℓ) * (D * lam0 ^ n) :=
      mul_le_mul_of_nonneg_left (hEv n hn) (pow_nonneg hq _)
    _ = D * (q ^ ℓ * lam0) ^ n := by rw [pow_mul', mul_pow]; ring

end TubeArea
open MeasureTheory Finset

namespace TubeArea

/-- A cyclic successor has no fixed point when the period is at least two. -/
lemma torusGeom_rotate_ne {k : ℕ} (hk : 2 ≤ k) (i : Fin k) :
    finRotate k i ≠ i := by
  obtain ⟨l, rfl⟩ : ∃ l, k = l + 1 := ⟨k - 1, by omega⟩
  intro h
  have hv := congrArg Fin.val h
  rw [coe_finRotate] at hv
  split_ifs at hv with hi
  · have hi' := congrArg Fin.val hi
    change i.val = l at hi'
    omega
  · omega

/-- Product of the entries whose natural index is strictly smaller than `r`. -/
def torusGeom_prefix {k : ℕ} (g : Fin k → ℤˣ) (r : ℕ) : ℤˣ :=
  ∏ j ∈ Finset.univ.filter (fun j : Fin k => j.val < r), g j

lemma torusGeom_prefix_zero {k : ℕ} (g : Fin k → ℤˣ) :
    torusGeom_prefix g 0 = 1 := by
  simp [torusGeom_prefix]

lemma torusGeom_prefix_total {k : ℕ} (g : Fin k → ℤˣ) :
    torusGeom_prefix g k = ∏ j, g j := by
  have hs : Finset.univ.filter (fun j : Fin k => j.val < k) = Finset.univ := by
    ext j
    simp [j.isLt]
  unfold torusGeom_prefix
  rw [hs]

lemma torusGeom_prefix_succ {k : ℕ} (g : Fin k → ℤˣ) (i : Fin k) :
    torusGeom_prefix g (i.val + 1) = torusGeom_prefix g i.val * g i := by
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
  unfold torusGeom_prefix
  rw [hs, Finset.prod_insert hi]
  exact mul_comm _ _

/-- Prefix products solve the cyclic sign equation when the total is one. -/
lemma torusGeom_cycle {k : ℕ} (g : Fin (k + 1) → ℤˣ)
    (hg : ∏ j, g j = 1) (i : Fin (k + 1)) :
    torusGeom_prefix g i.val *
        torusGeom_prefix g (finRotate (k + 1) i).val = g i := by
  by_cases hi : i = Fin.last k
  · subst i
    rw [finRotate_last]
    change torusGeom_prefix g k * torusGeom_prefix g 0 = g (Fin.last k)
    rw [torusGeom_prefix_zero, mul_one]
    have hs : 1 = torusGeom_prefix g k * g (Fin.last k) := by
      calc
        1 = torusGeom_prefix g (k + 1) := by
          rw [torusGeom_prefix_total, hg]
        _ = torusGeom_prefix g k * g (Fin.last k) :=
          torusGeom_prefix_succ g (Fin.last k)
    calc
      torusGeom_prefix g k =
          (torusGeom_prefix g k * g (Fin.last k)) * g (Fin.last k) := by
        rw [mul_assoc, grid_sign_square, mul_one]
      _ = g (Fin.last k) := by rw [← hs, one_mul]
  · rw [coe_finRotate_of_ne_last hi, torusGeom_prefix_succ]
    rw [← mul_assoc, grid_sign_square, one_mul]

/-- Edges of the discrete torus `(ℤ/m) × (ℤ/n)`: `Sum.inl (i,j)` is the horizontal edge from `(i,j)` to `(i+1,j)`,
`Sum.inr (i,j)` the vertical edge from `(i,j)` to `(i,j+1)`; indices are cyclic. -/
abbrev TorusEdge (m n : ℕ) := (Fin m × Fin n) ⊕ (Fin m × Fin n)

/-- The four boundary edges of the plaquette with lower-left corner `p = (i,j)`: bottom `H(i,j)`, top `H(i,j+1)`,
left `V(i,j)`, right `V(i+1,j)`; the cyclic successor is `finRotate`. -/
def torusBd {m n : ℕ} (p : Fin m × Fin n) : Finset (TorusEdge m n) :=
  {Sum.inl (p.1, p.2), Sum.inl (p.1, finRotate n p.2), Sum.inr (p.1, p.2), Sum.inr (finRotate m p.1, p.2)}

/-- G3. For periods at least two the four boundary edges are distinct. -/
theorem torus_plaq_explicit {m n : ℕ} (hm : 2 ≤ m) (hn : 2 ≤ n)
    (σ : TorusEdge m n → ℤˣ) (p : Fin m × Fin n) :
    plaq torusBd σ p =
      σ (Sum.inl (p.1, p.2)) * σ (Sum.inl (p.1, finRotate n p.2)) *
        σ (Sum.inr (p.1, p.2)) * σ (Sum.inr (finRotate m p.1, p.2)) := by
  classical
  have hi := torusGeom_rotate_ne hm p.1
  have hj := torusGeom_rotate_ne hn p.2
  have hA : (Sum.inl (p.1, p.2) : TorusEdge m n) ∉
      ({Sum.inl (p.1, finRotate n p.2), Sum.inr (p.1, p.2),
        Sum.inr (finRotate m p.1, p.2)} : Finset (TorusEdge m n)) := by
    intro he
    simp only [Finset.mem_insert, Finset.mem_singleton] at he
    rcases he with he | he | he
    · exact hj (congrArg Prod.snd (Sum.inl.inj he)).symm
    · cases he
    · cases he
  have hB : (Sum.inl (p.1, finRotate n p.2) : TorusEdge m n) ∉
      ({Sum.inr (p.1, p.2), Sum.inr (finRotate m p.1, p.2)} :
        Finset (TorusEdge m n)) := by
    intro he
    simp only [Finset.mem_insert, Finset.mem_singleton] at he
    rcases he with he | he <;> cases he
  have hC : (Sum.inr (p.1, p.2) : TorusEdge m n) ∉
      ({Sum.inr (finRotate m p.1, p.2)} : Finset (TorusEdge m n)) := by
    intro he
    exact hi (congrArg Prod.fst (Sum.inr.inj (Finset.mem_singleton.mp he))).symm
  unfold plaq torusBd
  rw [Finset.prod_insert hA, Finset.prod_insert hB, Finset.prod_insert hC,
    Finset.prod_singleton]
  simp only [mul_assoc]

/-- G1. Parity: on the torus the product of all plaquette signs is one. -/
theorem torus_plaq_parity {m n : ℕ} (hm : 2 ≤ m) (hn : 2 ≤ n) (σ : TorusEdge m n → ℤˣ) :
    ∏ p : Fin m × Fin n, plaq torusBd σ p = 1 := by
  classical
  have hH : (∏ p : Fin m × Fin n, σ (Sum.inl (p.1, finRotate n p.2))) =
      ∏ p : Fin m × Fin n, σ (Sum.inl p) := by
    exact Equiv.prod_comp (Equiv.prodCongr (Equiv.refl (Fin m)) (finRotate n))
      (fun p : Fin m × Fin n => σ (Sum.inl p))
  have hV : (∏ p : Fin m × Fin n, σ (Sum.inr (finRotate m p.1, p.2))) =
      ∏ p : Fin m × Fin n, σ (Sum.inr p) := by
    exact Equiv.prod_comp (Equiv.prodCongr (finRotate m) (Equiv.refl (Fin n)))
      (fun p : Fin m × Fin n => σ (Sum.inr p))
  simp only [torus_plaq_explicit hm hn, Finset.prod_mul_distrib]
  rw [hH, hV]
  simp only [grid_sign_square, one_mul]

/-- G2. Image: every assignment of plaquette signs with product one is realised by edge signs. -/
theorem torus_plaq_image {m n : ℕ} (hm : 2 ≤ m) (hn : 2 ≤ n) (t : Fin m × Fin n → ℤˣ)
    (ht : ∏ p, t p = 1) : ∃ σ : TorusEdge m n → ℤˣ, ∀ p, plaq torusBd σ p = t p := by
  classical
  obtain ⟨m', rfl⟩ : ∃ m', m = m' + 1 := ⟨m - 1, by omega⟩
  obtain ⟨n', rfl⟩ : ∃ n', n = n' + 1 := ⟨n - 1, by omega⟩
  let torusGeom_c : Fin (m' + 1) → ℤˣ :=
    fun i => ∏ j : Fin (n' + 1), t (i, j)
  have hc : (∏ i, torusGeom_c i) = 1 := by
    dsimp only [torusGeom_c]
    exact (Fintype.prod_prod_type t).symm.trans ht
  let torusGeom_d : Fin (m' + 1) → Fin (n' + 1) → ℤˣ :=
    fun i j => t (i, j) * (if j = 0 then torusGeom_c i else 1)
  have hd (i : Fin (m' + 1)) : (∏ j, torusGeom_d i j) = 1 := by
    dsimp only [torusGeom_d]
    rw [Finset.prod_mul_distrib]
    have hcorr : (∏ j : Fin (n' + 1),
        if j = 0 then torusGeom_c i else (1 : ℤˣ)) = torusGeom_c i := by
      simpa only [Finset.mem_univ, if_true] using
        (Finset.prod_ite_eq' (Finset.univ : Finset (Fin (n' + 1)))
          (0 : Fin (n' + 1)) (fun _ => torusGeom_c i))
    rw [hcorr]
    exact grid_sign_square (torusGeom_c i)
  let torusGeom_v : Fin (m' + 1) → Fin (n' + 1) → ℤˣ :=
    fun i j => if j = 0 then torusGeom_prefix torusGeom_c i.val else 1
  let torusGeom_h : Fin (m' + 1) → Fin (n' + 1) → ℤˣ :=
    fun i j => torusGeom_prefix (torusGeom_d i) j.val
  have hv (i : Fin (m' + 1)) (j : Fin (n' + 1)) :
      torusGeom_v i j * torusGeom_v (finRotate (m' + 1) i) j =
        (if j = 0 then torusGeom_c i else 1) := by
    by_cases hj : j = 0
    · simp only [torusGeom_v, if_pos hj]
      exact torusGeom_cycle torusGeom_c hc i
    · simp only [torusGeom_v, if_neg hj, one_mul]
  have hh (i : Fin (m' + 1)) (j : Fin (n' + 1)) :
      torusGeom_h i j * torusGeom_h i (finRotate (n' + 1) j) =
        torusGeom_d i j :=
    torusGeom_cycle (torusGeom_d i) (hd i) j
  let torusGeom_σ : TorusEdge (m' + 1) (n' + 1) → ℤˣ := fun e =>
    match e with
    | Sum.inl p => torusGeom_h p.1 p.2
    | Sum.inr p => torusGeom_v p.1 p.2
  refine ⟨torusGeom_σ, ?_⟩
  intro p
  rcases p with ⟨i, j⟩
  rw [torus_plaq_explicit hm hn]
  change torusGeom_h i j * torusGeom_h i (finRotate (n' + 1) j) *
      torusGeom_v i j * torusGeom_v (finRotate (m' + 1) i) j = t (i, j)
  calc
    torusGeom_h i j * torusGeom_h i (finRotate (n' + 1) j) *
        torusGeom_v i j * torusGeom_v (finRotate (m' + 1) i) j =
        (torusGeom_h i j * torusGeom_h i (finRotate (n' + 1) j)) *
          (torusGeom_v i j * torusGeom_v (finRotate (m' + 1) i) j) := by
      rw [mul_assoc]
    _ = torusGeom_d i j * (if j = 0 then torusGeom_c i else 1) := by
      rw [hh, hv]
    _ = t (i, j) := by
      dsimp only [torusGeom_d]
      rw [mul_assoc, grid_sign_square, mul_one]

end TubeArea

open MeasureTheory Finset

namespace TubeArea

/-- H1. Electric-flux (twist) bound for a Wilson-type gauge theory whose plaquette signs satisfy the parity
constraint and realise every even assignment (closed surface).  The twisted weights flip the sign of ALL fibre
copies of the plaquette `p₀`. -/
theorem wilson_twist_ratio_bound
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
    (hpar : ∀ σ : E → ℤˣ, ∏ p, plaq (fun p => wordBoundary (w p)) σ p = 1)
    (himg : ∀ t : P → ℤˣ, ∏ p, t p = 1 →
      ∃ σ : E → ℤˣ, ∀ p, plaq (fun p => wordBoundary (w p)) σ p = t p)
    (p₀ : P) :
    |(∫ ω, R ω * Real.exp (∑ p, wilsonCoupling β c chi w p ω) ∂wilsonMeasure haarG)
        - ∫ ω, R ω * Real.exp (∑ p, wilsonCoupling β
              (fun p y => if p = p₀ then -(c p y) else c p y) chi w p ω) ∂wilsonMeasure haarG|
      ≤ Real.tanh (β * (Fintype.card F : ℝ)) ^ Fintype.card P *
        ((∫ ω, R ω * Real.exp (∑ p, wilsonCoupling β c chi w p ω) ∂wilsonMeasure haarG)
          + ∫ ω, R ω * Real.exp (∑ p, wilsonCoupling β
              (fun p y => if p = p₀ then -(c p y) else c p y) chi w p ω) ∂wilsonMeasure haarG) := by
  classical
  letI : IsProbabilityMeasure (wilsonMeasure (E := E) (F := F) (X := X) haarG) := by
    unfold wilsonMeasure
    infer_instance
  have torusWilson_twist (p : P) (ω : WilsonConfig G E F X) :
      wilsonCoupling β (fun p y => if p = p₀ then -(c p y) else c p y) chi w p ω =
        if p = p₀ then -(wilsonCoupling β c chi w p ω) else wilsonCoupling β c chi w p ω := by
    by_cases hp : p = p₀
    · simp only [wilsonCoupling, if_pos hp, neg_mul, Finset.sum_neg_distrib, mul_neg]
    · simp only [wilsonCoupling, if_neg hp]
  have torusWilson_bound := twist_ratio_bound (wilsonMeasure haarG) (columnFlip z)
    (cf_columnFlip_preserving haarG hleft z)
    (fun p => wordBoundary (w p)) hpar himg
    (wilsonCoupling β c chi w) (cf_measurable_wilsonCoupling β c chi hchim w)
    (β * (Fintype.card F : ℝ)) (cf_wilsonCoupling_bound β hβ c hc chi hchi1 w)
    (cf_wilsonCoupling_flip hz hcentral β c chi hodd w hw)
    R hRm hR0 hRflip hRint p₀
  simpa only [torusWilson_twist] using torusWilson_bound

/-- Counterclockwise plaquette word on the torus, from the lower-left corner `p = (i,j)`:
bottom `H(i,j)` forwards, right `V(i+1,j)` forwards, top `H(i,j+1)` backwards, left `V(i,j)` backwards. -/
def torusWord {m n : ℕ} (p : Fin m × Fin n) : List (TorusEdge m n × Bool) :=
  [(Sum.inl (p.1, p.2), true), (Sum.inr (finRotate m p.1, p.2), true),
    (Sum.inl (p.1, finRotate n p.2), false), (Sum.inr (p.1, p.2), false)]

lemma torusWilson_word_nodup {m n : ℕ} (hm : 2 ≤ m) (hn : 2 ≤ n)
    (p : Fin m × Fin n) : ((torusWord p).map Prod.fst).Nodup := by
  have torusWilson_hi : finRotate m p.1 ≠ p.1 := torusGeom_rotate_ne hm p.1
  have torusWilson_hj : finRotate n p.2 ≠ p.2 := torusGeom_rotate_ne hn p.2
  have torusWilson_distinct :
      p ≠ (p.1, finRotate n p.2) ∧ (finRotate m p.1, p.2) ≠ p := by
    constructor
    · intro h
      exact torusWilson_hj (congrArg Prod.snd h).symm
    · intro h
      exact torusWilson_hi (congrArg Prod.fst h)
  simpa [torusWord] using torusWilson_distinct

lemma torusWilson_word_boundary {m n : ℕ} (p : Fin m × Fin n) :
    wordBoundary (torusWord p) = torusBd p := by
  apply Finset.ext
  intro e
  simp [wordBoundary, torusWord, torusBd, or_assoc, or_left_comm, or_comm]

/-- H2. Electric-flux free-energy bound for the full Wilson-type action on (torus `m × n`) × (finite fibre `F`):
base plaquettes with weights bounded by one, plus any finite family of neutral terms (mixed and fibre plaquettes)
with arbitrary real coefficients.  `Z₁` is obtained from `Z₀` by flipping the sign of all fibre copies of the
base plaquette `p₀` ('t Hooft twist in the base plane). -/
theorem wilson_electric_flux_torus
    {G F X Q : Type*} [Group G] [MeasurableSpace G]
    [MeasurableMul₂ G] [MeasurableInv G] [Fintype F] [Fintype X] [Fintype Q]
    (m n : ℕ) (hm : 2 ≤ m) (hn : 2 ≤ n)
    (haarG : Measure G) [IsProbabilityMeasure haarG]
    (hleft : ∀ g : G, MeasurePreserving (fun h : G => g * h) haarG haarG)
    (z : G) (hz : z * z = 1) (hcentral : ∀ g : G, z * g = g * z)
    (chi : G → ℝ) (hchim : Measurable chi) (hchi1 : ∀ g, |chi g| ≤ 1)
    (hodd : ∀ g, chi (z * g) = -chi g)
    (weights : (Fin m × Fin n) → F → ℝ) (hweights : ∀ p y, |weights p y| ≤ 1)
    (β : ℝ) (hβ : 0 ≤ β)
    (wq : Q → GeneralWord (TorusEdge m n) F X)
    (hq : ∀ q, NeutralWord (wq q)) (coef : Q → ℝ)
    (p₀ : Fin m × Fin n) :
    |(∫ ω, neutralActionWeight chi wq coef ω *
          Real.exp (∑ p, wilsonCoupling β weights chi torusWord p ω) ∂wilsonMeasure haarG)
        - ∫ ω, neutralActionWeight chi wq coef ω *
          Real.exp (∑ p, wilsonCoupling β
            (fun p y => if p = p₀ then -(weights p y) else weights p y) chi torusWord p ω)
            ∂wilsonMeasure haarG|
      ≤ Real.tanh (β * (Fintype.card F : ℝ)) ^ (m * n) *
        ((∫ ω, neutralActionWeight chi wq coef ω *
          Real.exp (∑ p, wilsonCoupling β weights chi torusWord p ω) ∂wilsonMeasure haarG)
          + ∫ ω, neutralActionWeight chi wq coef ω *
          Real.exp (∑ p, wilsonCoupling β
            (fun p y => if p = p₀ then -(weights p y) else weights p y) chi torusWord p ω)
            ∂wilsonMeasure haarG) := by
  classical
  have torusWilson_hpar (σ : TorusEdge m n → ℤˣ) :
      ∏ p : Fin m × Fin n, plaq (fun p => wordBoundary (torusWord p)) σ p = 1 := by
    simpa only [torusWilson_word_boundary] using torus_plaq_parity hm hn σ
  have torusWilson_himg (t : Fin m × Fin n → ℤˣ) (ht : ∏ p, t p = 1) :
      ∃ σ : TorusEdge m n → ℤˣ,
        ∀ p, plaq (fun p => wordBoundary (torusWord p)) σ p = t p := by
    simpa only [torusWilson_word_boundary] using torus_plaq_image hm hn t ht
  have torusWilson_bound := wilson_twist_ratio_bound (E := TorusEdge m n) (P := Fin m × Fin n)
    haarG hleft z hz hcentral chi hchim hchi1 hodd
    torusWord (torusWilson_word_nodup hm hn) weights hweights β hβ
    (neutralActionWeight chi wq coef)
    (measurable_neutralActionWeight chi hchim wq coef)
    (fun ω => (neutralActionWeight_pos chi wq coef ω).le)
    (neutralActionWeight_flip hz hcentral chi wq hq coef)
    (integrable_wilsonActionWeight haarG chi hchim hchi1 wq coef
      β hβ weights hweights torusWord)
    torusWilson_hpar torusWilson_himg p₀
  simpa only [Fintype.card_prod, Fintype.card_fin] using torusWilson_bound

end TubeArea
noncomputable section
namespace TubeBridge
open YangMills MeasureTheory Finset TubeArea

/-- OpenAI's Wilson energy (`YangMills.wilsonEnergy`, file PublicWilson.lean) with a real sign on each plaquette term. -/
def signedWilsonEnergy {g : GaugeGroup} {l : ℕ+} (s : Site l × Directions → ℝ)
    (U : Configuration g l) : ℝ :=
  ∑ p : Site l × Directions,
    (1 - s p * ((plaquette U p.1 p.2.val.1 p.2.val.2).val.val.trace).re / ((g.n+1 : ℕ) : ℝ))

/-- I0. With all signs equal to one it is OpenAI's energy. -/
theorem signedWilsonEnergy_one {g : GaugeGroup} {l : ℕ+} (U : Configuration g l) :
    signedWilsonEnergy (fun _ => (1 : ℝ)) U = wilsonEnergy U := by
  simp only [signedWilsonEnergy, wilsonEnergy, one_mul]

/-- The 't Hooft twist in the plane of the axes 0 and 1: the sign is `-1` exactly on the plaquettes of that plane
whose base point has coordinates `(a, b)` along the axes 0 and 1, at every position along the axes 2 and 3. -/
def planeTwist {l : ℕ+} (a b : ZMod l.val) : Site l × Directions → ℝ :=
  fun p => if p.2.val = ((0 : Axis), (1 : Axis)) ∧ p.1 0 = a ∧ p.1 1 = b then -1 else 1

lemma bridge_secondCountable_image (g : GaugeGroup) : SecondCountableTopology g.image := by
  haveI : SecondCountableTopology (Matrix (Fin (g.n + 1)) (Fin (g.n + 1)) ℂ) :=
    inferInstanceAs (SecondCountableTopology (Fin (g.n + 1) → Fin (g.n + 1) → ℂ))
  haveI : SecondCountableTopology (UnitaryRepresentation g.n) :=
    inferInstanceAs (SecondCountableTopology
      ↥((UnitaryRepresentation g.n : Set (Matrix (Fin (g.n + 1)) (Fin (g.n + 1)) ℂ))))
  exact inferInstanceAs (SecondCountableTopology ↥(g.image : Set (UnitaryRepresentation g.n)))

/-- The normalized real trace in the public faithful representation. -/
def bridge_chi {g : GaugeGroup} (V : g.image) : ℝ :=
  V.val.val.trace.re / ((g.n + 1 : ℕ) : ℝ)

lemma bridge_continuous_chi {g : GaugeGroup} : Continuous (bridge_chi : g.image → ℝ) := by
  have hv : Continuous (fun V : g.image => V.val.val) :=
    continuous_subtype_val.comp continuous_subtype_val
  exact (Complex.continuous_re.comp hv.matrix_trace).div_const _

lemma bridge_chi_bound {g : GaugeGroup} (V : g.image) : |bridge_chi V| ≤ 1 := by
  have hn : (0 : ℝ) < ((g.n + 1 : ℕ) : ℝ) := by positivity
  have he (i : Fin (g.n + 1)) : |(V.val.val i i).re| ≤ 1 :=
    (Complex.abs_re_le_norm _).trans (entry_norm_bound_of_unitary V.val.property i i)
  have ht : |V.val.val.trace.re| ≤ ((g.n + 1 : ℕ) : ℝ) := by
    calc
      |V.val.val.trace.re| = |∑ i : Fin (g.n + 1), (V.val.val i i).re| := by
        simp [Matrix.trace]
      _ ≤ ∑ i : Fin (g.n + 1), |(V.val.val i i).re| := Finset.abs_sum_le_sum_abs _ _
      _ ≤ ∑ _i : Fin (g.n + 1), (1 : ℝ) := Finset.sum_le_sum (fun i _ => he i)
      _ = ((g.n + 1 : ℕ) : ℝ) := by simp
  rw [bridge_chi, abs_div, abs_of_pos hn]
  exact (div_le_iff₀ hn).mpr (by simpa only [one_mul] using ht)

/-- The element of the public gauge image furnished by the hypothesis on `-1`. -/
def bridge_z (g : GaugeGroup) (hneg : (-1 : UnitaryRepresentation g.n) ∈ g.image) :
    g.image := ⟨-1, hneg⟩

lemma bridge_z_square (g : GaugeGroup)
    (hneg : (-1 : UnitaryRepresentation g.n) ∈ g.image) :
    bridge_z g hneg * bridge_z g hneg = 1 := by
  apply Subtype.ext
  change (-1 : UnitaryRepresentation g.n) * (-1) = 1
  simp

lemma bridge_z_central (g : GaugeGroup)
    (hneg : (-1 : UnitaryRepresentation g.n) ∈ g.image) (V : g.image) :
    bridge_z g hneg * V = V * bridge_z g hneg := by
  apply Subtype.ext
  change (-1 : UnitaryRepresentation g.n) * V.val = V.val * (-1)
  simp

lemma bridge_chi_odd (g : GaugeGroup)
    (hneg : (-1 : UnitaryRepresentation g.n) ∈ g.image) (V : g.image) :
    bridge_chi (bridge_z g hneg * V) = -bridge_chi V := by
  have hv : (bridge_z g hneg * V).val.val = -V.val.val := by
    change (-(1 : Matrix (Fin (g.n + 1)) (Fin (g.n + 1)) ℂ)) * V.val.val = _
    simp only [neg_mul, one_mul]
  simp only [bridge_chi, hv, Matrix.trace_neg, Complex.neg_re, neg_div]

lemma bridge_continuous_plaquette {g : GaugeGroup} {l : ℕ+}
    (x : Site l) (i j : Axis) :
    Continuous (fun U : Configuration g l => plaquette U x i j) := by
  unfold plaquette
  exact (continuous_apply (x, i)).mul
    ((continuous_apply (x + Pi.single i 1, j)).mul
      ((continuous_apply (x + Pi.single j 1, i)).inv.mul (continuous_apply (x, j)).inv))

/-- A single normalized trace term, indexed exactly as in the public energy. -/
def bridge_term {g : GaugeGroup} {l : ℕ+} (U : Configuration g l)
    (q : Site l × Directions) : ℝ :=
  bridge_chi (plaquette U q.1 q.2.val.1 q.2.val.2)

lemma bridge_measurable_term {g : GaugeGroup} {l : ℕ+} (q : Site l × Directions) :
    Measurable (fun U : Configuration g l => bridge_term U q) := by
  letI : SecondCountableTopology g.image := bridge_secondCountable_image g
  exact (bridge_continuous_chi.comp
    (bridge_continuous_plaquette q.1 q.2.val.1 q.2.val.2)).measurable

lemma bridge_measurable_energy {g : GaugeGroup} {l : ℕ+} :
    Measurable (wilsonEnergy : Configuration g l → ℝ) := by
  change Measurable (fun U : Configuration g l => ∑ q : Site l × Directions,
    ((1 : ℝ) - bridge_term U q))
  exact Finset.measurable_sum univ (fun q _ => measurable_const.sub (bridge_measurable_term q))

lemma bridge_energy_nonneg {g : GaugeGroup} {l : ℕ+} (U : Configuration g l) :
    0 ≤ wilsonEnergy U := by
  unfold wilsonEnergy
  apply Finset.sum_nonneg
  intro q _
  change 0 ≤ 1 - bridge_chi (plaquette U q.1 q.2.val.1 q.2.val.2)
  exact sub_nonneg.mpr (abs_le.mp (bridge_chi_bound _)).2

lemma bridge_integrable_density {g : GaugeGroup} {l : ℕ+}
    (haar : Measure g.image) [IsProbabilityMeasure haar] (β : ℝ) (hβ : 0 ≤ β) :
    Integrable (fun U : Configuration g l => Real.exp (-β * wilsonEnergy U))
      (Measure.pi fun _ : Site l × Axis => haar) := by
  have hm : Measurable (fun U : Configuration g l => Real.exp (-β * wilsonEnergy U)) :=
    (bridge_measurable_energy.const_mul (-β)).exp
  apply (integrable_const (μ := Measure.pi fun _ : Site l × Axis => haar) (1 : ℝ)).mono'
    hm.aestronglyMeasurable
  filter_upwards [] with U
  rw [Real.norm_eq_abs, abs_of_nonneg (Real.exp_nonneg _)]
  exact Real.exp_le_one_iff.mpr
    (mul_nonpos_of_nonpos_of_nonneg (neg_nonpos.mpr hβ) (bridge_energy_nonneg U))

/-- Positive periods are written as `k + 2` before using definitional `ZMod = Fin`. -/
def bridge_period (k : ℕ) : ℕ+ := ⟨k + 2, by omega⟩

/-- Both a base plaquette index and a transverse fibre index have two coordinates. -/
abbrev bridge_point (k : ℕ) := Fin (k + 2) × Fin (k + 2)

/-- Assemble the base coordinates and the two transverse coordinates into a public site. -/
def bridge_site (k : ℕ) (p y : bridge_point k) : Site (bridge_period k) :=
  fun i => if i = 0 then p.1 else if i = 1 then p.2 else if i = 2 then y.1 else y.2

/-- The explicit change of finite indices used only for sums, never for configuration measures. -/
def bridge_siteEquiv (k : ℕ) : (bridge_point k × bridge_point k) ≃ Site (bridge_period k) where
  toFun q := bridge_site k q.1 q.2
  invFun x := ((x 0, x 1), (x 2, x 3))
  left_inv q := by
    rcases q with ⟨⟨a, b⟩, ⟨c, d⟩⟩
    simp [bridge_site]
  right_inv x := by
    funext i
    fin_cases i <;> simp [bridge_site]

lemma bridge_sum_sites (k : ℕ) (f : Site (bridge_period k) → ℝ) :
    (∑ x, f x) = ∑ p : bridge_point k, ∑ y : bridge_point k, f (bridge_site k p y) := by
  simpa only [Fintype.sum_prod_type] using
    (Fintype.sum_equiv (bridge_siteEquiv k)
      (fun q => f (bridge_site k q.1 q.2)) f (fun _ => rfl)).symm

/-- The public orientation `(0,1)`, with its strict-order witness. -/
def bridge_dir01 : Directions := ⟨(0, 1), by decide⟩

lemma bridge_sum_direction (f : Directions → ℝ) :
    (∑ d : Directions, if d.val = ((0 : Axis), (1 : Axis)) then f d else 0) =
      f bridge_dir01 := by
  classical
  have hd (d : Directions) : d.val = ((0 : Axis), (1 : Axis)) ↔ d = bridge_dir01 := by
    constructor
    · exact fun h => Subtype.ext h
    · rintro rfl
      rfl
  simp only [hd]
  exact Fintype.sum_ite_eq' bridge_dir01 f

lemma bridge_split_sum (k : ℕ) (f : Site (bridge_period k) × Directions → ℝ) :
    (∑ q, f q) =
      (∑ q, if q.2.val = ((0 : Axis), (1 : Axis)) then 0 else f q) +
        ∑ x : Site (bridge_period k), f (x, bridge_dir01) := by
  classical
  calc
    (∑ q, f q) = ∑ q, ((if q.2.val = ((0 : Axis), (1 : Axis)) then 0 else f q) +
        (if q.2.val = ((0 : Axis), (1 : Axis)) then f q else 0)) := by
      apply Finset.sum_congr rfl
      intro q _
      split_ifs <;> simp
    _ = (∑ q, if q.2.val = ((0 : Axis), (1 : Axis)) then 0 else f q) +
        ∑ q, if q.2.val = ((0 : Axis), (1 : Axis)) then f q else 0 :=
      Finset.sum_add_distrib
    _ = _ := by
      congr 1
      rw [Fintype.sum_prod_type]
      apply Finset.sum_congr rfl
      intro x _
      exact bridge_sum_direction (fun d => f (x, d))

/-- A link gets its base-edge sign on axes 0 and 1 and gets the identity sign on axes 2 and 3. -/
def bridge_edgeSign {k : ℕ} (σ : TorusEdge (k + 2) (k + 2) → ℤˣ)
    (e : Site (bridge_period k) × Axis) : ℤˣ :=
  if e.2 = 0 then σ (Sum.inl (e.1 0, e.1 1))
  else if e.2 = 1 then σ (Sum.inr (e.1 0, e.1 1)) else 1

/-- The coordinatewise left multiplication acting on the public configuration space itself. -/
def bridge_tau {g : GaugeGroup} {k : ℕ} (z : g.image)
    (σ : TorusEdge (k + 2) (k + 2) → ℤˣ)
    (U : Configuration g (bridge_period k)) : Configuration g (bridge_period k) :=
  fun e => centralSign z (bridge_edgeSign σ e) * U e

lemma bridge_tau_preserving {g : GaugeGroup} {k : ℕ}
    (haar : Measure g.image) [IsProbabilityMeasure haar]
    (hleft : ∀ u : g.image, MeasurePreserving (fun v : g.image => u * v) haar haar)
    (z : g.image) (σ : TorusEdge (k + 2) (k + 2) → ℤˣ) :
    MeasurePreserving (bridge_tau z σ)
      (Measure.pi fun _ : Site (bridge_period k) × Axis => haar)
      (Measure.pi fun _ : Site (bridge_period k) × Axis => haar) := by
  exact measurePreserving_pi _ _ (fun e => hleft (centralSign z (bridge_edgeSign σ e)))

/-- Product of the four link signs, in the order of the public plaquette. -/
def bridge_plaquetteSign {k : ℕ} (σ : TorusEdge (k + 2) (k + 2) → ℤˣ)
    (x : Site (bridge_period k)) (i j : Axis) : ℤˣ :=
  bridge_edgeSign σ (x, i) * bridge_edgeSign σ (x + Pi.single i 1, j) *
    bridge_edgeSign σ (x + Pi.single j 1, i) * bridge_edgeSign σ (x, j)

lemma bridge_plaquette_flip {g : GaugeGroup} {k : ℕ} (z : g.image)
    (hz : z * z = 1) (hc : ∀ V : g.image, z * V = V * z)
    (σ : TorusEdge (k + 2) (k + 2) → ℤˣ) (U : Configuration g (bridge_period k))
    (x : Site (bridge_period k)) (i j : Axis) :
    plaquette (bridge_tau z σ U) x i j =
      centralSign z (bridge_plaquetteSign σ x i j) * plaquette U x i j := by
  have h := cf_wordHolonomy_flip (G := g.image)
    (E := Site (bridge_period k) × Axis) (F := Unit) hz hc
    [((x, i), true), ((x + Pi.single i 1, j), true),
      ((x + Pi.single j 1, i), false), ((x, j), false)]
    (bridge_edgeSign σ) (fun ey => U ey.1) ()
  simpa only [wordHolonomy, wordSign, orientedLink, mul_one, mul_assoc,
    bridge_tau, plaquette, bridge_plaquetteSign] using h

lemma bridge_plane_sign {k : ℕ} (σ : TorusEdge (k + 2) (k + 2) → ℤˣ)
    (x : Site (bridge_period k)) :
    bridge_plaquetteSign σ x 0 1 = plaq torusBd σ (x 0, x 1) := by
  rw [torus_plaq_explicit (by omega : 2 ≤ k + 2) (by omega : 2 ≤ k + 2)]
  simp [bridge_plaquetteSign, bridge_edgeSign, Pi.add_apply,
    finRotate_apply] <;> ac_rfl

lemma bridge_neutral_sign {k : ℕ} (σ : TorusEdge (k + 2) (k + 2) → ℤˣ)
    (x : Site (bridge_period k)) (d : Directions)
    (hd : d.val ≠ ((0 : Axis), (1 : Axis))) :
    bridge_plaquetteSign σ x d.val.1 d.val.2 = 1 := by
  rcases d with ⟨⟨i, j⟩, hij⟩
  change i.val < j.val at hij
  change (i, j) ≠ ((0 : Axis), (1 : Axis)) at hd
  fin_cases i <;> fin_cases j <;>
    simp_all [bridge_plaquetteSign, bridge_edgeSign, Pi.add_apply,
      mul_assoc, grid_sign_square] <;> norm_num at hij

lemma bridge_neutral_plaquette {g : GaugeGroup} {k : ℕ} (z : g.image)
    (hz : z * z = 1) (hc : ∀ V : g.image, z * V = V * z)
    (σ : TorusEdge (k + 2) (k + 2) → ℤˣ) (U : Configuration g (bridge_period k))
    (x : Site (bridge_period k)) (d : Directions)
    (hd : d.val ≠ ((0 : Axis), (1 : Axis))) :
    plaquette (bridge_tau z σ U) x d.val.1 d.val.2 = plaquette U x d.val.1 d.val.2 := by
  rw [bridge_plaquette_flip z hz hc, bridge_neutral_sign σ x d hd]
  simp [centralSign]

/-- The coupling of a base plaquette is the sum of all its transverse copies, multiplied by beta. -/
def bridge_K {g : GaugeGroup} {k : ℕ} (β : ℝ) (p : bridge_point k)
    (U : Configuration g (bridge_period k)) : ℝ :=
  β * ∑ y : bridge_point k, bridge_chi (plaquette U (bridge_site k p y) 0 1)

lemma bridge_measurable_K {g : GaugeGroup} {k : ℕ} (β : ℝ) (p : bridge_point k) :
    Measurable (bridge_K (g := g) β p) := by
  letI : SecondCountableTopology g.image := bridge_secondCountable_image g
  unfold bridge_K
  exact (Finset.measurable_sum univ (fun y _ =>
    (bridge_continuous_chi.comp (bridge_continuous_plaquette (bridge_site k p y) 0 1)).measurable)).const_mul β

lemma bridge_K_bound {g : GaugeGroup} {k : ℕ} (β : ℝ) (hβ : 0 ≤ β)
    (p : bridge_point k) (U : Configuration g (bridge_period k)) :
    |bridge_K β p U| ≤ β * (Fintype.card (bridge_point k) : ℝ) := by
  rw [bridge_K, abs_mul, abs_of_nonneg hβ]
  apply mul_le_mul_of_nonneg_left _ hβ
  calc
    |∑ y : bridge_point k, bridge_chi (plaquette U (bridge_site k p y) 0 1)| ≤
        ∑ y : bridge_point k, |bridge_chi (plaquette U (bridge_site k p y) 0 1)| :=
      Finset.abs_sum_le_sum_abs _ _
    _ ≤ ∑ _y : bridge_point k, (1 : ℝ) :=
      Finset.sum_le_sum (fun y _ => bridge_chi_bound _)
    _ = (Fintype.card (bridge_point k) : ℝ) := by simp

lemma bridge_K_flip {g : GaugeGroup} {k : ℕ} (z : g.image)
    (hz : z * z = 1) (hc : ∀ V : g.image, z * V = V * z)
    (ho : ∀ V : g.image, bridge_chi (z * V) = -bridge_chi V)
    (β : ℝ) (σ : TorusEdge (k + 2) (k + 2) → ℤˣ)
    (p : bridge_point k) (U : Configuration g (bridge_period k)) :
    bridge_K β p (bridge_tau z σ U) = sgn (plaq torusBd σ p) * bridge_K β p U := by
  have h (y : bridge_point k) :
      bridge_chi (plaquette (bridge_tau z σ U) (bridge_site k p y) 0 1) =
        sgn (plaq torusBd σ p) * bridge_chi (plaquette U (bridge_site k p y) 0 1) := by
    rw [bridge_plaquette_flip z hz hc, cf_chi_centralSign ho, bridge_plane_sign]
    simp [bridge_site]
  unfold bridge_K
  simp_rw [h]
  rw [← Finset.mul_sum]
  ring

/-- The trace sum of the other five public orientations, before multiplication by beta. -/
def bridge_other {g : GaugeGroup} {k : ℕ} (U : Configuration g (bridge_period k)) : ℝ :=
  ∑ q : Site (bridge_period k) × Directions,
    if q.2.val = ((0 : Axis), (1 : Axis)) then 0 else bridge_term U q

lemma bridge_measurable_other {g : GaugeGroup} {k : ℕ} :
    Measurable (bridge_other : Configuration g (bridge_period k) → ℝ) := by
  classical
  unfold bridge_other
  exact Finset.measurable_sum univ (fun q _ => by
    by_cases hd : q.2.val = ((0 : Axis), (1 : Axis))
    · simp only [if_pos hd]
      exact measurable_const
    · simp only [if_neg hd]
      exact bridge_measurable_term q)

lemma bridge_other_flip {g : GaugeGroup} {k : ℕ} (z : g.image)
    (hz : z * z = 1) (hc : ∀ V : g.image, z * V = V * z)
    (σ : TorusEdge (k + 2) (k + 2) → ℤˣ) (U : Configuration g (bridge_period k)) :
    bridge_other (bridge_tau z σ U) = bridge_other U := by
  classical
  unfold bridge_other
  apply Finset.sum_congr rfl
  intro q _
  by_cases hd : q.2.val = ((0 : Axis), (1 : Axis))
  · simp only [if_pos hd]
  · simp only [if_neg hd, bridge_term, bridge_neutral_plaquette z hz hc σ U q.1 q.2 hd]

/-- The invariant residual weight, including the constant part of the Wilson energy. -/
def bridge_R {g : GaugeGroup} {k : ℕ} (β : ℝ)
    (U : Configuration g (bridge_period k)) : ℝ :=
  Real.exp (-β * (Fintype.card (Site (bridge_period k) × Directions) : ℝ) + β * bridge_other U)

lemma bridge_measurable_R {g : GaugeGroup} {k : ℕ} (β : ℝ) :
    Measurable (bridge_R (g := g) (k := k) β) := by
  unfold bridge_R
  exact (measurable_const.add (bridge_measurable_other.const_mul β)).exp

lemma bridge_R_nonneg {g : GaugeGroup} {k : ℕ} (β : ℝ)
    (U : Configuration g (bridge_period k)) : 0 ≤ bridge_R β U :=
  Real.exp_nonneg _

lemma bridge_R_flip {g : GaugeGroup} {k : ℕ} (z : g.image)
    (hz : z * z = 1) (hc : ∀ V : g.image, z * V = V * z)
    (β : ℝ) (σ : TorusEdge (k + 2) (k + 2) → ℤˣ)
    (U : Configuration g (bridge_period k)) :
    bridge_R β (bridge_tau z σ U) = bridge_R β U := by
  unfold bridge_R
  rw [bridge_other_flip z hz hc]

lemma bridge_energy_eq {g : GaugeGroup} {l : ℕ+} (U : Configuration g l) :
    wilsonEnergy U = (Fintype.card (Site l × Directions) : ℝ) - ∑ q, bridge_term U q := by
  simp [wilsonEnergy, bridge_term, bridge_chi, Finset.sum_sub_distrib]

lemma bridge_signed_energy_eq {g : GaugeGroup} {l : ℕ+}
    (s : Site l × Directions → ℝ) (U : Configuration g l) :
    signedWilsonEnergy s U = (Fintype.card (Site l × Directions) : ℝ) -
      ∑ q, s q * bridge_term U q := by
  simp [signedWilsonEnergy, bridge_term, bridge_chi, mul_div_assoc, Finset.sum_sub_distrib]

lemma bridge_K_sum {g : GaugeGroup} {k : ℕ} (β : ℝ)
    (U : Configuration g (bridge_period k)) :
    (∑ p : bridge_point k, bridge_K β p U) =
      β * ∑ x : Site (bridge_period k), bridge_chi (plaquette U x 0 1) := by
  rw [bridge_sum_sites k]
  simp only [bridge_K, Finset.mul_sum]

lemma bridge_exponent {g : GaugeGroup} {k : ℕ} (β : ℝ)
    (U : Configuration g (bridge_period k)) :
    (-β * (Fintype.card (Site (bridge_period k) × Directions) : ℝ) + β * bridge_other U) +
      (∑ p : bridge_point k, bridge_K β p U) = -β * wilsonEnergy U := by
  rw [bridge_energy_eq, bridge_split_sum k (bridge_term U), bridge_K_sum]
  change (-β * (Fintype.card (Site (bridge_period k) × Directions) : ℝ) + β * bridge_other U) +
    β * (∑ x : Site (bridge_period k), bridge_chi (plaquette U x 0 1)) =
      -β * ((Fintype.card (Site (bridge_period k) × Directions) : ℝ) -
        (bridge_other U + ∑ x : Site (bridge_period k), bridge_chi (plaquette U x 0 1)))
  ring

lemma bridge_density_factor {g : GaugeGroup} {k : ℕ} (β : ℝ)
    (U : Configuration g (bridge_period k)) :
    bridge_R β U * Real.exp (∑ p : bridge_point k, bridge_K β p U) =
      Real.exp (-β * wilsonEnergy U) := by
  rw [bridge_R, ← Real.exp_add, bridge_exponent]

lemma bridge_planeTwist_site {k : ℕ} (a b : Fin (k + 2)) (p y : bridge_point k) :
    planeTwist (l := bridge_period k) a b (bridge_site k p y, bridge_dir01) =
      if p = (a, b) then -1 else 1 := by
  classical
  by_cases hp : p = (a, b)
  · subst p
    simp [planeTwist, bridge_site, bridge_dir01]
  · have hcoord : ¬(p.1 = a ∧ p.2 = b) := by
      intro h
      exact hp (Prod.ext h.1 h.2)
    simp [planeTwist, bridge_site, bridge_dir01, hp]
    intro ha hb
    exact (hcoord ⟨ha, hb⟩).elim

lemma bridge_twisted_K_sum {g : GaugeGroup} {k : ℕ} (β : ℝ)
    (a b : Fin (k + 2)) (U : Configuration g (bridge_period k)) :
    (∑ p : bridge_point k, if p = (a, b) then -(bridge_K β p U) else bridge_K β p U) =
      β * ∑ x : Site (bridge_period k),
        planeTwist (l := bridge_period k) a b (x, bridge_dir01) * bridge_chi (plaquette U x 0 1) := by
  classical
  rw [bridge_sum_sites k, Finset.mul_sum]
  apply Finset.sum_congr rfl
  intro p _
  simp only [bridge_planeTwist_site]
  by_cases hp : p = (a, b)
  · simp [hp, bridge_K, Finset.sum_neg_distrib]
  · simp [hp, bridge_K]

lemma bridge_twisted_other {g : GaugeGroup} {k : ℕ} (a b : Fin (k + 2))
    (U : Configuration g (bridge_period k)) :
    (∑ q : Site (bridge_period k) × Directions,
      if q.2.val = ((0 : Axis), (1 : Axis)) then 0
      else planeTwist (l := bridge_period k) a b q * bridge_term U q) = bridge_other U := by
  classical
  unfold bridge_other
  apply Finset.sum_congr rfl
  intro q _
  by_cases hd : q.2.val = ((0 : Axis), (1 : Axis)) <;>
    simp [hd, planeTwist]

lemma bridge_twisted_exponent {g : GaugeGroup} {k : ℕ} (β : ℝ)
    (a b : Fin (k + 2)) (U : Configuration g (bridge_period k)) :
    (-β * (Fintype.card (Site (bridge_period k) × Directions) : ℝ) + β * bridge_other U) +
      (∑ p : bridge_point k, if p = (a, b) then -(bridge_K β p U) else bridge_K β p U) =
        -β * signedWilsonEnergy (planeTwist (l := bridge_period k) a b) U := by
  rw [bridge_signed_energy_eq,
    bridge_split_sum k (fun q => planeTwist (l := bridge_period k) a b q * bridge_term U q),
    bridge_twisted_other, bridge_twisted_K_sum]
  change (-β * (Fintype.card (Site (bridge_period k) × Directions) : ℝ) + β * bridge_other U) +
    β * (∑ x : Site (bridge_period k),
      planeTwist (l := bridge_period k) a b (x, bridge_dir01) * bridge_chi (plaquette U x 0 1)) =
      -β * ((Fintype.card (Site (bridge_period k) × Directions) : ℝ) -
        (bridge_other U + ∑ x : Site (bridge_period k),
          planeTwist (l := bridge_period k) a b (x, bridge_dir01) * bridge_chi (plaquette U x 0 1)))
  ring

lemma bridge_twisted_density_factor {g : GaugeGroup} {k : ℕ} (β : ℝ)
    (a b : Fin (k + 2)) (U : Configuration g (bridge_period k)) :
    bridge_R β U * Real.exp
      (∑ p : bridge_point k, if p = (a, b) then -(bridge_K β p U) else bridge_K β p U) =
        Real.exp (-β * signedWilsonEnergy (planeTwist (l := bridge_period k) a b) U) := by
  rw [bridge_R, ← Real.exp_add, bridge_twisted_exponent]

/-- I1. Twist-ratio bound for OpenAI's four-dimensional periodic Wilson lattice (period `l ≥ 2` in every direction),
for every gauge group containing `-1`, every left-invariant probability measure on it, every `β ≥ 0`. -/
theorem openai_wilson_twist_ratio (g : GaugeGroup)
    (hneg : (-1 : UnitaryRepresentation g.n) ∈ g.image)
    (l : ℕ+) (hl : 2 ≤ l.val) (β : ℝ) (hβ : 0 ≤ β)
    (haar : Measure g.image) [IsProbabilityMeasure haar]
    (hleft : ∀ u : g.image, MeasurePreserving (fun v : g.image => u * v) haar haar)
    (a b : ZMod l.val) :
    |(∫ U : Configuration g l, Real.exp (-β * wilsonEnergy U) ∂(Measure.pi fun _ : Site l × Axis => haar))
        - ∫ U : Configuration g l, Real.exp (-β * signedWilsonEnergy (planeTwist a b) U)
            ∂(Measure.pi fun _ : Site l × Axis => haar)|
      ≤ Real.tanh (β * (l.val : ℝ) ^ 2) ^ (l.val ^ 2) *
        ((∫ U : Configuration g l, Real.exp (-β * wilsonEnergy U) ∂(Measure.pi fun _ : Site l × Axis => haar))
          + ∫ U : Configuration g l, Real.exp (-β * signedWilsonEnergy (planeTwist a b) U)
              ∂(Measure.pi fun _ : Site l × Axis => haar)) := by
  classical
  obtain ⟨m, hm⟩ := l
  change 2 ≤ m at hl
  obtain ⟨k, rfl⟩ : ∃ k : ℕ, m = k + 2 := ⟨m - 2, by omega⟩
  let μ : Measure (Configuration g (bridge_period k)) :=
    Measure.pi fun _ : Site (bridge_period k) × Axis => haar
  haveI : IsProbabilityMeasure μ := by
    dsimp only [μ]
    infer_instance
  have hpar (σ : TorusEdge (k + 2) (k + 2) → ℤˣ) :
      ∏ p : bridge_point k, plaq torusBd σ p = 1 :=
    torus_plaq_parity (by omega) (by omega) σ
  have himg (t : bridge_point k → ℤˣ) (ht : ∏ p, t p = 1) :
      ∃ σ : TorusEdge (k + 2) (k + 2) → ℤˣ, ∀ p, plaq torusBd σ p = t p :=
    torus_plaq_image (by omega) (by omega) t ht
  have hint : Integrable (fun U : Configuration g (bridge_period k) =>
      bridge_R β U * Real.exp (∑ p : bridge_point k, bridge_K β p U)) μ := by
    simpa only [bridge_density_factor, μ] using
      (bridge_integrable_density (l := bridge_period k) haar β hβ)
  have h := TubeArea.twist_ratio_bound
    (Ω := Configuration g (bridge_period k))
    (E := TorusEdge (k + 2) (k + 2)) (P := bridge_point k)
    μ (bridge_tau (bridge_z g hneg))
    (bridge_tau_preserving haar hleft (bridge_z g hneg))
    torusBd hpar himg (bridge_K β) (bridge_measurable_K β)
    (β * (Fintype.card (bridge_point k) : ℝ)) (bridge_K_bound β hβ)
    (bridge_K_flip (bridge_z g hneg) (bridge_z_square g hneg)
      (bridge_z_central g hneg) (bridge_chi_odd g hneg) β)
    (bridge_R β) (bridge_measurable_R β) (bridge_R_nonneg β)
    (bridge_R_flip (bridge_z g hneg) (bridge_z_square g hneg) (bridge_z_central g hneg) β)
    hint (a, b)
  convert h using 1 <;>
    simp only [bridge_density_factor, bridge_twisted_density_factor, bridge_point,
      Fintype.card_prod, Fintype.card_fin, PNat.mk_coe, Nat.cast_mul, pow_two, μ,
      bridge_period] <;>
    congr! (transparency := .default)

/-- I2. The same for the Haar measure carried by any of OpenAI's Wilson families. -/
theorem openai_wilson_twist_ratio_family (g : GaugeGroup)
    (hneg : (-1 : UnitaryRepresentation g.n) ∈ g.image) (C : WilsonFamily g)
    (l : ℕ+) (hl : 2 ≤ l.val) (β : ℝ) (hβ : 0 ≤ β) (a b : ZMod l.val) :
    |(∫ U : Configuration g l, Real.exp (-β * wilsonEnergy U) ∂(Measure.pi fun _ : Site l × Axis => C.haar))
        - ∫ U : Configuration g l, Real.exp (-β * signedWilsonEnergy (planeTwist a b) U)
            ∂(Measure.pi fun _ : Site l × Axis => C.haar)|
      ≤ Real.tanh (β * (l.val : ℝ) ^ 2) ^ (l.val ^ 2) *
        ((∫ U : Configuration g l, Real.exp (-β * wilsonEnergy U) ∂(Measure.pi fun _ : Site l × Axis => C.haar))
          + ∫ U : Configuration g l, Real.exp (-β * signedWilsonEnergy (planeTwist a b) U)
              ∂(Measure.pi fun _ : Site l × Axis => C.haar)) := by
  letI : SecondCountableTopology g.image := bridge_secondCountable_image g
  letI : IsProbabilityMeasure C.haar := C.probability
  letI : C.haar.IsHaarMeasure := C.invariantHaar
  exact openai_wilson_twist_ratio g hneg l hl β hβ C.haar
    (fun u => measurePreserving_mul_left C.haar u) a b

/-- I3. OpenAI's concrete SU(2) contains `-1`. -/
theorem su2_neg_one_mem : (-1 : UnitaryRepresentation su2.n) ∈ su2.image := by
  change Matrix.det (-(1 : Matrix (Fin 2) (Fin 2) ℂ)) = 1
  norm_num [Matrix.det_neg, Matrix.det_one, Fintype.card_fin]

/-- I4. The twist-ratio bound for OpenAI's concrete SU(2) and any of its Wilson families. -/
theorem openai_su2_twist_ratio (C : WilsonFamily su2)
    (l : ℕ+) (hl : 2 ≤ l.val) (β : ℝ) (hβ : 0 ≤ β) (a b : ZMod l.val) :
    |(∫ U : Configuration su2 l, Real.exp (-β * wilsonEnergy U) ∂(Measure.pi fun _ : Site l × Axis => C.haar))
        - ∫ U : Configuration su2 l, Real.exp (-β * signedWilsonEnergy (planeTwist a b) U)
            ∂(Measure.pi fun _ : Site l × Axis => C.haar)|
      ≤ Real.tanh (β * (l.val : ℝ) ^ 2) ^ (l.val ^ 2) *
        ((∫ U : Configuration su2 l, Real.exp (-β * wilsonEnergy U) ∂(Measure.pi fun _ : Site l × Axis => C.haar))
          + ∫ U : Configuration su2 l, Real.exp (-β * signedWilsonEnergy (planeTwist a b) U)
              ∂(Measure.pi fun _ : Site l × Axis => C.haar)) := by
  exact openai_wilson_twist_ratio_family su2 su2_neg_one_mem C l hl β hβ a b

end TubeBridge
end
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
#print axioms TubeArea.wilson_column_flip_bound
-- PARTIE D : les trois théorèmes doivent exister et ne dépendre que des axiomes standard (énoncés relus à la main par le pilote).
#print axioms TubeArea.grid_plaq_surjective
#print axioms TubeArea.grid_stokes_rectangle
#print axioms TubeArea.tube_area_law_rectangle
#check @TubeArea.grid_plaq_surjective
#check @TubeArea.grid_stokes_rectangle
#check @TubeArea.tube_area_law_rectangle
-- PARTIE E : énoncés relus à la main par le pilote.
#print axioms TubeArea.neutral_word_flip_invariant
#print axioms TubeArea.mixedWord_neutral
#print axioms TubeArea.wilson_action_area_law_rectangle
#check @TubeArea.neutral_word_flip_invariant
#check @TubeArea.mixedWord_neutral
#check @TubeArea.wilson_action_area_law_rectangle
-- ===== PARTIE F (tore abstrait, rapport de torsion, racines) : énoncés canoniques réécrits par le pilote =====
namespace TubeAreaVerif
open MeasureTheory Finset
theorem enonce_canonique_F1
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
    (W : Ω → ℝ) (hWm : Measurable W) (hW1 : ∀ ω, |W ω| ≤ 1)
    (A : Finset P)
    (hWτ : ∀ σ ω, W (τ σ ω) = (((∏ p ∈ A, ∏ e ∈ bd p, σ e : ℤˣ) : ℤ) : ℝ) * W ω) :
    (1 - Real.tanh κ ^ Fintype.card P) * |∫ ω, W ω * (R ω * Real.exp (∑ p, K p ω)) ∂μ|
      ≤ (Real.tanh κ ^ A.card + Real.tanh κ ^ (Fintype.card P - A.card)) *
          ∫ ω, R ω * Real.exp (∑ p, K p ω) ∂μ :=
  TubeArea.torus_flip_bound μ τ hτ bd hpar himg K hKm κ hK hKτ R hRm hR0 hRτ hRint W hWm hW1 A hWτ
theorem enonce_canonique_F2
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
          + ∫ ω, R ω * Real.exp (∑ p, (if p = p₀ then -(K p ω) else K p ω)) ∂μ) :=
  TubeArea.twist_ratio_bound μ τ hτ bd hpar himg K hKm κ hK hKτ R hRm hR0 hRτ hRint p₀
theorem enonce_canonique_F3 (a b M : ℝ) (ha : 0 ≤ a) (hb : 0 ≤ b) (hM : 0 < M)
    (h : ∀ n : ℕ, 0 < n → a ^ n ≤ M * b ^ n) : a ≤ b :=
  TubeArea.le_of_forall_pow_le_const_mul_pow a b M ha hb hM h
theorem enonce_canonique_F4 (ℓ : ℕ) (q lam0 lam1 D : ℝ)
    (hq : 0 ≤ q) (h0 : 0 ≤ lam0) (h1 : 0 ≤ lam1) (hD : 0 < D)
    (Ev Od : ℕ → ℝ)
    (hOd : ∀ n : ℕ, 0 < n → lam1 ^ n ≤ Od n)
    (hEv : ∀ n : ℕ, 0 < n → Ev n ≤ D * lam0 ^ n)
    (hratio : ∀ n : ℕ, 0 < n → Od n ≤ q ^ (n * ℓ) * Ev n) :
    lam1 ≤ q ^ ℓ * lam0 :=
  TubeArea.flux_gap_of_traces ℓ q lam0 lam1 D hq h0 h1 hD Ev Od hOd hEv hratio
end TubeAreaVerif
#print axioms TubeAreaVerif.enonce_canonique_F1
#print axioms TubeAreaVerif.enonce_canonique_F2
#print axioms TubeAreaVerif.enonce_canonique_F3
#print axioms TubeAreaVerif.enonce_canonique_F4
-- ===== PARTIE G (géométrie du tore discret) : énoncés canoniques réécrits par le pilote, sans les définitions du modèle =====
namespace TubeAreaVerif
open Finset
theorem enonce_canonique_G3 {m n : ℕ} (hm : 2 ≤ m) (hn : 2 ≤ n)
    (σ : ((Fin m × Fin n) ⊕ (Fin m × Fin n)) → ℤˣ) (p : Fin m × Fin n) :
    (∏ e ∈ ({Sum.inl (p.1, p.2), Sum.inl (p.1, finRotate n p.2), Sum.inr (p.1, p.2),
        Sum.inr (finRotate m p.1, p.2)} : Finset ((Fin m × Fin n) ⊕ (Fin m × Fin n))), σ e)
      = σ (Sum.inl (p.1, p.2)) * σ (Sum.inl (p.1, finRotate n p.2)) *
          σ (Sum.inr (p.1, p.2)) * σ (Sum.inr (finRotate m p.1, p.2)) :=
  TubeArea.torus_plaq_explicit hm hn σ p
theorem enonce_canonique_G1 {m n : ℕ} (hm : 2 ≤ m) (hn : 2 ≤ n)
    (σ : ((Fin m × Fin n) ⊕ (Fin m × Fin n)) → ℤˣ) :
    ∏ p : Fin m × Fin n,
      (∏ e ∈ ({Sum.inl (p.1, p.2), Sum.inl (p.1, finRotate n p.2), Sum.inr (p.1, p.2),
        Sum.inr (finRotate m p.1, p.2)} : Finset ((Fin m × Fin n) ⊕ (Fin m × Fin n))), σ e) = 1 :=
  TubeArea.torus_plaq_parity hm hn σ
theorem enonce_canonique_G2 {m n : ℕ} (hm : 2 ≤ m) (hn : 2 ≤ n) (t : Fin m × Fin n → ℤˣ)
    (ht : ∏ p, t p = 1) :
    ∃ σ : ((Fin m × Fin n) ⊕ (Fin m × Fin n)) → ℤˣ, ∀ p : Fin m × Fin n,
      (∏ e ∈ ({Sum.inl (p.1, p.2), Sum.inl (p.1, finRotate n p.2), Sum.inr (p.1, p.2),
        Sum.inr (finRotate m p.1, p.2)} : Finset ((Fin m × Fin n) ⊕ (Fin m × Fin n))), σ e) = t p :=
  TubeArea.torus_plaq_image hm hn t ht
end TubeAreaVerif
#print axioms TubeAreaVerif.enonce_canonique_G1
#print axioms TubeAreaVerif.enonce_canonique_G2
#print axioms TubeAreaVerif.enonce_canonique_G3
-- ===== PARTIE H (instance Wilson sur le tore) : énoncés figés par le pilote (ENONCES_H.lean), contrôlés par diff =====
#print axioms TubeArea.wilson_twist_ratio_bound
#print axioms TubeArea.wilson_electric_flux_torus
#check @TubeArea.wilson_twist_ratio_bound
#check @TubeArea.wilson_electric_flux_torus
#check @TubeArea.torusWord
-- ===== PARTIE I (pont vers les objets publics d'OpenAI) : énoncés figés par le pilote (ENONCES_I.lean), contrôlés par diff =====
#print axioms TubeBridge.signedWilsonEnergy_one
#print axioms TubeBridge.openai_wilson_twist_ratio
#print axioms TubeBridge.openai_wilson_twist_ratio_family
#print axioms TubeBridge.su2_neg_one_mem
#print axioms TubeBridge.openai_su2_twist_ratio
#check @TubeBridge.openai_wilson_twist_ratio
#check @TubeBridge.openai_su2_twist_ratio
#print axioms YangMills.su2Theory
