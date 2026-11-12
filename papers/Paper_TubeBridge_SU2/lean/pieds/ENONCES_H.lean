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
  PROOF_H1

/-- Counterclockwise plaquette word on the torus, from the lower-left corner `p = (i,j)`:
bottom `H(i,j)` forwards, right `V(i+1,j)` forwards, top `H(i,j+1)` backwards, left `V(i,j)` backwards. -/
def torusWord {m n : ℕ} (p : Fin m × Fin n) : List (TorusEdge m n × Bool) :=
  [(Sum.inl (p.1, p.2), true), (Sum.inr (finRotate m p.1, p.2), true),
    (Sum.inl (p.1, finRotate n p.2), false), (Sum.inr (p.1, p.2), false)]

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
  PROOF_H2
