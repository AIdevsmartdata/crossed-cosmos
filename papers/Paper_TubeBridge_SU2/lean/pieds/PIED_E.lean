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
