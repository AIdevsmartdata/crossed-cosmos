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
