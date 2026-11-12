/-- OpenAI's Wilson energy (`YangMills.wilsonEnergy`, file PublicWilson.lean) with a real sign on each plaquette term. -/
def signedWilsonEnergy {g : GaugeGroup} {l : ℕ+} (s : Site l × Directions → ℝ)
    (U : Configuration g l) : ℝ :=
  ∑ p : Site l × Directions,
    (1 - s p * ((plaquette U p.1 p.2.val.1 p.2.val.2).val.val.trace).re / ((g.n+1 : ℕ) : ℝ))

/-- I0. With all signs equal to one it is OpenAI's energy. -/
theorem signedWilsonEnergy_one {g : GaugeGroup} {l : ℕ+} (U : Configuration g l) :
    signedWilsonEnergy (fun _ => (1 : ℝ)) U = wilsonEnergy U := by
  PROOF_I0

/-- The 't Hooft twist in the plane of the axes 0 and 1: the sign is `-1` exactly on the plaquettes of that plane
whose base point has coordinates `(a, b)` along the axes 0 and 1, at every position along the axes 2 and 3. -/
def planeTwist {l : ℕ+} (a b : ZMod l.val) : Site l × Directions → ℝ :=
  fun p => if p.2.val = ((0 : Axis), (1 : Axis)) ∧ p.1 0 = a ∧ p.1 1 = b then -1 else 1

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
  PROOF_I1

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
  PROOF_I2

/-- I3. OpenAI's concrete SU(2) contains `-1`. -/
theorem su2_neg_one_mem : (-1 : UnitaryRepresentation su2.n) ∈ su2.image := by
  PROOF_I3

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
  PROOF_I4
