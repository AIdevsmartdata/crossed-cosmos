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
