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
