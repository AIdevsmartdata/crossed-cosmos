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
