noncomputable section

namespace CentreZN

lemma znb_pow_add {M : Type*} [Monoid M] {N : ℕ} [NeZero N]
    (z : M) (hzN : z ^ N = 1) (a b : ZMod N) :
    z ^ (a + b).val = z ^ a.val * z ^ b.val := by
  rw [ZMod.val_add, ← pow_eq_pow_mod (a.val + b.val) hzN, pow_add]

lemma znb_pow_mul {M : Type*} [Monoid M] {N : ℕ}
    (z : M) (hzN : z ^ N = 1) (a b : ZMod N) :
    (z ^ a.val) ^ b.val = z ^ (a * b).val := by
  rw [← pow_mul, ZMod.val_mul]
  exact pow_eq_pow_mod _ hzN

lemma znb_pow_neg {G : Type*} [Group G] {N : ℕ} [NeZero N]
    (z : G) (hzN : z ^ N = 1) (a : ZMod N) :
    z ^ (-a).val = (z ^ a.val)⁻¹ := by
  apply eq_inv_of_mul_eq_one_left
  rw [← znb_pow_add z hzN, neg_add_cancel, ZMod.val_zero, pow_zero]

lemma znb_pow_central {G : Type*} [Monoid G]
    (z : G) (hcentral : ∀ g : G, z * g = g * z) (k : ℕ) (g : G) :
    z ^ k * g = g * z ^ k := by
  exact ((show Commute z g from hcentral g).pow_left k).eq

lemma znb_character_pow {G : Type*} [Group G]
    (z : G) (chi : G → ℂ) (η : ℂ)
    (hchi : ∀ g, chi (z * g) = η * chi g) (k : ℕ) (g : G) :
    chi (z ^ k * g) = η ^ k * chi g := by
  induction k with
  | zero => simp
  | succ k ih =>
    calc
      chi (z ^ (k + 1) * g) = η * chi (z ^ k * g) := by
        rw [pow_succ', mul_assoc, hchi]
      _ = η ^ (k + 1) * chi g := by
        rw [ih, pow_succ', mul_assoc]

lemma znb_oriented_twist {G : Type*} [Group G] {N : ℕ} [NeZero N]
    (z : G) (hzN : z ^ N = 1) (hcentral : ∀ g : G, z * g = g * z)
    (b : Bool) (a : ZMod N) (g : G) :
    orientedLink b (z ^ a.val * g) =
      z ^ (if b then a else -a).val * orientedLink b g := by
  cases b with
  | false =>
    change (z ^ a.val * g)⁻¹ = z ^ (-a).val * g⁻¹
    rw [mul_inv_rev, ← znb_pow_neg z hzN a]
    exact (znb_pow_central z hcentral (-a).val g⁻¹).symm
  | true => rfl

lemma znb_holonomy_twist {G E F X : Type*} [Group G] {N : ℕ} [NeZero N]
    (z : G) (hzN : z ^ N = 1) (hcentral : ∀ g : G, z * g = g * z)
    (w : Word E F X) (σ : E → ZMod N) (ω : Config G E F X) :
    holonomy w (columnTwist z σ ω) =
      z ^ (charge w σ).val * holonomy w ω := by
  induction w with
  | nil => simp [holonomy, charge]
  | cons a w ih =>
    rcases a with ⟨l, b⟩
    cases l with
    | inl ey =>
      change orientedLink b (z ^ (σ ey.1).val * ω.1 ey) *
          holonomy w (columnTwist z σ ω) =
        z ^ ((if b then σ ey.1 else -σ ey.1) + charge w σ).val *
          (orientedLink b (ω.1 ey) * holonomy w ω)
      rw [znb_oriented_twist z hzN hcentral, ih, znb_pow_add z hzN]
      calc
        (z ^ (if b then σ ey.1 else -σ ey.1).val * orientedLink b (ω.1 ey)) *
            (z ^ (charge w σ).val * holonomy w ω) =
          z ^ (if b then σ ey.1 else -σ ey.1).val *
            ((orientedLink b (ω.1 ey) * z ^ (charge w σ).val) *
              holonomy w ω) := by
                simp only [mul_assoc]
        _ = z ^ (if b then σ ey.1 else -σ ey.1).val *
            ((z ^ (charge w σ).val * orientedLink b (ω.1 ey)) *
              holonomy w ω) := by
                rw [← znb_pow_central z hcentral (charge w σ).val
                  (orientedLink b (ω.1 ey))]
        _ = (z ^ (if b then σ ey.1 else -σ ey.1).val *
              z ^ (charge w σ).val) *
            (orientedLink b (ω.1 ey) * holonomy w ω) := by
                simp only [mul_assoc]
    | inr x =>
      change orientedLink b (ω.2 x) * holonomy w (columnTwist z σ ω) =
        z ^ (charge w σ).val * (orientedLink b (ω.2 x) * holonomy w ω)
      rw [ih]
      calc
        orientedLink b (ω.2 x) * (z ^ (charge w σ).val * holonomy w ω) =
          (orientedLink b (ω.2 x) * z ^ (charge w σ).val) *
            holonomy w ω := by
              simp only [mul_assoc]
        _ = (z ^ (charge w σ).val * orientedLink b (ω.2 x)) *
            holonomy w ω := by
              rw [← znb_pow_central z hcentral (charge w σ).val
                (orientedLink b (ω.2 x))]
        _ = z ^ (charge w σ).val *
            (orientedLink b (ω.2 x) * holonomy w ω) := by
              simp only [mul_assoc]

lemma znb_charge_base {E F X : Type*} {N : ℕ}
    (w : List (E × Bool)) (y : F) (σ : E → ZMod N) :
    charge (baseWord w y : Word E F X) σ = baseCharge w σ := by
  induction w with
  | nil => rfl
  | cons a w ih =>
    change (if a.2 then σ a.1 else -σ a.1) + charge (baseWord w y : Word E F X) σ =
      (if a.2 then σ a.1 else -σ a.1) + baseCharge w σ
    rw [ih]

lemma znb_columnTwist_preserving {G E F X : Type*} [Group G] [MeasurableSpace G]
    [Fintype E] [Fintype F] [Fintype X] {N : ℕ}
    (haarG : Measure G) [IsProbabilityMeasure haarG]
    (hleft : ∀ g : G, MeasurePreserving (fun h : G => g * h) haarG haarG)
    (z : G) (σ : E → ZMod N) :
    MeasurePreserving (columnTwist z σ : Config G E F X → Config G E F X)
      (configMeasure haarG) (configMeasure haarG) := by
  have hU := measurePreserving_pi
    (fun _ : E × F => haarG) (fun _ : E × F => haarG)
    (fun ey => hleft (z ^ (σ ey.1).val))
  have hV := MeasurePreserving.id (Measure.pi fun _ : X => haarG)
  have hmap : (columnTwist z σ : Config G E F X → Config G E F X) =
      Prod.map (fun U : E × F → G => fun ey => z ^ (σ ey.1).val * U ey)
        (id : (X → G) → (X → G)) := by
    funext ω
    rcases ω with ⟨U, V⟩
    rfl
  rw [hmap]
  exact hU.prod hV

lemma znb_measurable_orientedLink {G : Type*} [Group G] [MeasurableSpace G]
    [MeasurableInv G] (b : Bool) :
    Measurable (orientedLink b : G → G) := by
  cases b with
  | false => exact measurable_inv
  | true => exact measurable_id

lemma znb_measurable_holonomy {G E F X : Type*} [Group G] [MeasurableSpace G]
    [MeasurableMul₂ G] [MeasurableInv G] (w : Word E F X) :
    Measurable (holonomy w : Config G E F X → G) := by
  induction w with
  | nil => exact measurable_const
  | cons a w ih =>
    rcases a with ⟨l, b⟩
    cases l with
    | inl ey =>
      exact ((znb_measurable_orientedLink b).comp
        ((measurable_pi_apply ey).comp measurable_fst)).mul ih
    | inr x =>
      exact ((znb_measurable_orientedLink b).comp
        ((measurable_pi_apply x).comp measurable_snd)).mul ih

lemma znb_measurable_coupling {G E F X P : Type*} [Group G] [MeasurableSpace G]
    [MeasurableMul₂ G] [MeasurableInv G] [Fintype F]
    (β : ℝ) (c : P → F → ℂ) (chi : G → ℂ) (hchim : Measurable chi)
    (w : P → List (E × Bool)) (p : P) :
    Measurable (coupling β c chi w p : Config G E F X → ℂ) := by
  exact (Finset.measurable_sum univ (fun y _ =>
    (hchim.comp (znb_measurable_holonomy (baseWord (w p) y))).const_mul
      (c p y))).const_mul (β : ℂ)

lemma znb_coupling_bound {G E F X P : Type*} [Group G] [Fintype F]
    (β : ℝ) (hβ : 0 ≤ β) (c : P → F → ℂ) (hc : ∀ p y, ‖c p y‖ ≤ 1)
    (chi : G → ℂ) (hchi1 : ∀ g, ‖chi g‖ ≤ 1) (w : P → List (E × Bool))
    (p : P) (ω : Config G E F X) :
    ‖coupling β c chi w p ω‖ ≤ β * (Fintype.card F : ℝ) := by
  unfold coupling
  rw [norm_mul, Complex.norm_real, Real.norm_of_nonneg hβ]
  apply mul_le_mul_of_nonneg_left _ hβ
  calc
    ‖∑ y, c p y * chi (holonomy (baseWord (w p) y) ω)‖ ≤
        ∑ y, ‖c p y * chi (holonomy (baseWord (w p) y) ω)‖ :=
      norm_sum_le _ _
    _ ≤ ∑ _y : F, (1 : ℝ) := by
      apply Finset.sum_le_sum
      intro y _
      rw [norm_mul]
      calc
        ‖c p y‖ * ‖chi (holonomy (baseWord (w p) y) ω)‖ ≤
            1 * ‖chi (holonomy (baseWord (w p) y) ω)‖ :=
          mul_le_mul_of_nonneg_right (hc p y) (norm_nonneg _)
        _ ≤ 1 := by
          simpa using hchi1 (holonomy (baseWord (w p) y) ω)
    _ = (Fintype.card F : ℝ) := by simp

lemma znb_coupling_twist {G E F X P : Type*} [Group G] [Fintype F]
    {N : ℕ} [NeZero N]
    (z : G) (hzN : z ^ N = 1) (hcentral : ∀ g : G, z * g = g * z)
    (β : ℝ) (c : P → F → ℂ) (chi : G → ℂ) (ζ : ℂ)
    (hchiz : ∀ g, chi (z * g) = ζ * chi g)
    (w : P → List (E × Bool)) (σ : E → ZMod N) (p : P)
    (ω : Config G E F X) :
    coupling β c chi w p (columnTwist z σ ω) =
      ζ ^ (baseCharge (w p) σ).val * coupling β c chi w p ω := by
  have hchar (y : F) :
      chi (holonomy (baseWord (w p) y) (columnTwist z σ ω)) =
        ζ ^ (baseCharge (w p) σ).val *
          chi (holonomy (baseWord (w p) y) ω) := by
    rw [znb_holonomy_twist z hzN hcentral, znb_charge_base,
      znb_character_pow z chi ζ hchiz]
  calc
    coupling β c chi w p (columnTwist z σ ω) =
        (β : ℂ) * ∑ y, c p y *
          (ζ ^ (baseCharge (w p) σ).val *
            chi (holonomy (baseWord (w p) y) ω)) := by
      simp only [coupling, hchar]
    _ = ζ ^ (baseCharge (w p) σ).val * coupling β c chi w p ω := by
      simp only [coupling, Finset.mul_sum]
      apply Finset.sum_congr rfl
      intro y _
      ring

lemma znb_measurable_termsWeight {G E F X Q : Type*}
    [Group G] [MeasurableSpace G] [MeasurableMul₂ G] [MeasurableInv G] [Fintype Q]
    (chi : G → ℂ) (hchim : Measurable chi)
    (wq : Q → Word E F X) (coef : Q → ℂ) :
    Measurable (termsWeight chi wq coef : Config G E F X → ℝ) := by
  exact (Finset.measurable_sum univ (fun k _ =>
    Complex.measurable_re.comp
      ((hchim.comp (znb_measurable_holonomy (wq k))).const_mul (coef k)))).exp

lemma znb_termsWeight_twist {G E F X Q : Type*} [Group G] [Fintype Q]
    {N : ℕ} [NeZero N]
    (z : G) (hzN : z ^ N = 1) (hcentral : ∀ g : G, z * g = g * z)
    (chi : G → ℂ) (wq : Q → Word E F X)
    (hneutral : ∀ k, Neutral N (wq k)) (coef : Q → ℂ)
    (σ : E → ZMod N) (ω : Config G E F X) :
    termsWeight chi wq coef (columnTwist z σ ω) = termsWeight chi wq coef ω := by
  unfold termsWeight
  apply congrArg Real.exp
  apply Finset.sum_congr rfl
  intro k _
  rw [znb_holonomy_twist z hzN hcentral, hneutral k σ]
  simp

lemma znb_termsWeight_bound {G E F X Q : Type*} [Group G] [Fintype Q]
    (chi : G → ℂ) (hchi1 : ∀ g, ‖chi g‖ ≤ 1)
    (wq : Q → Word E F X) (coef : Q → ℂ) (ω : Config G E F X) :
    termsWeight chi wq coef ω ≤ Real.exp (∑ k, ‖coef k‖) := by
  unfold termsWeight
  apply Real.exp_le_exp.mpr
  apply Finset.sum_le_sum
  intro k _
  calc
    (coef k * chi (holonomy (wq k) ω)).re ≤
        ‖coef k * chi (holonomy (wq k) ω)‖ := Complex.re_le_norm _
    _ = ‖coef k‖ * ‖chi (holonomy (wq k) ω)‖ := norm_mul _ _
    _ ≤ ‖coef k‖ * 1 :=
      mul_le_mul_of_nonneg_left (hchi1 _) (norm_nonneg _)
    _ = ‖coef k‖ := mul_one _

lemma znb_integrable_density {G E F X P Q : Type*}
    [Group G] [MeasurableSpace G] [MeasurableMul₂ G] [MeasurableInv G]
    [Fintype E] [Fintype F] [Fintype X] [Fintype P] [Fintype Q]
    (haarG : Measure G) [IsProbabilityMeasure haarG]
    (chi : G → ℂ) (hchim : Measurable chi) (hchi1 : ∀ g, ‖chi g‖ ≤ 1)
    (wq : Q → Word E F X) (coef : Q → ℂ)
    (β : ℝ) (hβ : 0 ≤ β) (weights : P → F → ℂ)
    (hweights : ∀ p y, ‖weights p y‖ ≤ 1) (w : P → List (E × Bool)) :
    Integrable
      (fun ω : Config G E F X => termsWeight chi wq coef ω *
        Real.exp (∑ p, (coupling β weights chi w p ω).re))
      (configMeasure haarG) := by
  classical
  letI : IsProbabilityMeasure
      (configMeasure (E := E) (F := F) (X := X) haarG) := by
    unfold configMeasure
    infer_instance
  let C : ℝ := Real.exp (∑ k, ‖coef k‖) *
    Real.exp (∑ _p : P, β * (Fintype.card F : ℝ))
  have hDm : Measurable (fun ω : Config G E F X =>
      termsWeight chi wq coef ω *
        Real.exp (∑ p, (coupling β weights chi w p ω).re)) :=
    (znb_measurable_termsWeight chi hchim wq coef).mul
      (Finset.measurable_sum univ (fun p _ =>
        Complex.measurable_re.comp
          (znb_measurable_coupling β weights chi hchim w p))).exp
  have hKbound (ω : Config G E F X) :
      Real.exp (∑ p, (coupling β weights chi w p ω).re) ≤
        Real.exp (∑ _p : P, β * (Fintype.card F : ℝ)) := by
    apply Real.exp_le_exp.mpr
    apply Finset.sum_le_sum
    intro p _
    exact (Complex.re_le_norm _).trans
      (znb_coupling_bound β hβ weights hweights chi hchi1 w p ω)
  refine (integrable_const (μ := configMeasure haarG) C).mono'
    hDm.aestronglyMeasurable ?_
  apply Filter.Eventually.of_forall
  intro ω
  have hRpos : 0 < termsWeight chi wq coef ω := by
    unfold termsWeight
    exact Real.exp_pos _
  rw [Real.norm_eq_abs,
    abs_of_pos (mul_pos hRpos (Real.exp_pos _))]
  exact mul_le_mul (znb_termsWeight_bound chi hchi1 wq coef ω) (hKbound ω)
    (Real.exp_pos _).le (Real.exp_pos _).le

def znb_prefix {A : Type*} [AddCommGroup A] {k : ℕ}
    (g : Fin k → A) (r : ℕ) : A :=
  ∑ j ∈ Finset.univ.filter (fun j : Fin k => j.val < r), g j

lemma znb_prefix_zero {A : Type*} [AddCommGroup A] {k : ℕ}
    (g : Fin k → A) :
    znb_prefix g 0 = 0 := by
  simp [znb_prefix]

lemma znb_prefix_total {A : Type*} [AddCommGroup A] {k : ℕ}
    (g : Fin k → A) :
    znb_prefix g k = ∑ j, g j := by
  have hs : Finset.univ.filter (fun j : Fin k => j.val < k) = Finset.univ := by
    ext j
    simp [j.isLt]
  unfold znb_prefix
  rw [hs]

lemma znb_prefix_succ {A : Type*} [AddCommGroup A] {k : ℕ}
    (g : Fin k → A) (i : Fin k) :
    znb_prefix g (i.val + 1) = znb_prefix g i.val + g i := by
  classical
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
  unfold znb_prefix
  rw [hs, Finset.sum_insert hi]
  exact add_comm _ _

lemma znb_cycle {A : Type*} [AddCommGroup A] {k : ℕ}
    (g : Fin (k + 1) → A) (hg : ∑ j, g j = 0) (i : Fin (k + 1)) :
    znb_prefix g (finRotate (k + 1) i).val - znb_prefix g i.val = g i := by
  by_cases hi : i = Fin.last k
  · subst i
    rw [finRotate_last]
    change znb_prefix g 0 - znb_prefix g k = g (Fin.last k)
    rw [znb_prefix_zero]
    have hs : znb_prefix g k + g (Fin.last k) = 0 := by
      calc
        znb_prefix g k + g (Fin.last k) = znb_prefix g (k + 1) :=
          (znb_prefix_succ g (Fin.last k)).symm
        _ = 0 := by rw [znb_prefix_total, hg]
    calc
      0 - znb_prefix g k =
          (znb_prefix g k + g (Fin.last k)) - znb_prefix g k := by
        rw [hs]
      _ = g (Fin.last k) := by abel
  · rw [coe_finRotate_of_ne_last hi, znb_prefix_succ]
    abel

/-! ## Partie B : énoncés -/

/-- B0. A mixed plaquette (long link at `y`, other link, the same column at `y'` backwards, other link backwards)
is neutral for every `N`. -/
theorem mixed_word_neutral {E F X : Type*} (N : ℕ) (e : E) (y y' : F) (x x' : X) :
    Neutral N ([(Sum.inl (e, y), true), (Sum.inr x, true), (Sum.inl (e, y'), false), (Sum.inr x', false)] :
      Word E F X) := by
  intro σ
  simp [charge]

/-- B1. Wilson-type centre-twist bound (open surface): group with a left-invariant probability measure, central `z`
with `z ^ N = 1`, `χ (z g) = ζ χ g`; observable `ψ` of `N`-ality `q`; Stokes relation and independence of the
plaquette charges are hypotheses. -/
theorem wilson_centre_flip_bound
    {G E F X P : Type*} [Group G] [MeasurableSpace G] [MeasurableMul₂ G] [MeasurableInv G]
    [Fintype E] [DecidableEq E] [Fintype F] [Fintype X] [Fintype P] [DecidableEq P]
    (N : ℕ) [NeZero N] (ζ : ℂ) (hζ : ζ ^ N = 1)
    (haarG : Measure G) [IsProbabilityMeasure haarG]
    (hleft : ∀ g : G, MeasurePreserving (fun h : G => g * h) haarG haarG)
    (z : G) (hzN : z ^ N = 1) (hcentral : ∀ g : G, z * g = g * z)
    (chi : G → ℂ) (hchim : Measurable chi) (hchi1 : ∀ g, ‖chi g‖ ≤ 1)
    (hchiz : ∀ g, chi (z * g) = ζ * chi g)
    (w : P → List (E × Bool)) (c : P → F → ℂ) (hc : ∀ p y, ‖c p y‖ ≤ 1)
    (β : ℝ) (hβ : 0 ≤ β)
    (R : Config G E F X → ℝ) (hRm : Measurable R) (hR0 : ∀ ω, 0 ≤ R ω)
    (hRtw : ∀ (σ : E → ZMod N) ω, R (columnTwist z σ ω) = R ω)
    (hRint : Integrable (fun ω => R ω * Real.exp (∑ p, (coupling β c chi w p ω).re))
      (configMeasure haarG))
    (q : ZMod N) (psi : G → ℂ) (hpsim : Measurable psi) (hpsi1 : ∀ g, ‖psi g‖ ≤ 1)
    (hpsiz : ∀ g, psi (z * g) = ζ ^ q.val * psi g)
    (wC : List (E × Bool)) (y0 : F) (A : Finset P)
    (hStokes : ∀ σ : E → ZMod N, baseCharge wC σ = ∑ p ∈ A, baseCharge (w p) σ)
    (hsurj : Function.Surjective (fun σ : E → ZMod N => fun p => baseCharge (w p) σ))
    (ρ : ℝ)
    (hρ : ∀ t : ℂ, ‖t‖ ≤ β * (Fintype.card F : ℝ) →
      ‖∑ j : ZMod N, ζ ^ (q * j).val * ((Real.exp ((ζ ^ j.val * t).re) : ℝ) : ℂ)‖
        ≤ ρ * ∑ j : ZMod N, Real.exp ((ζ ^ j.val * t).re)) :
    ‖∫ ω, psi (holonomy (baseWord wC y0) ω) *
        ((R ω * Real.exp (∑ p, (coupling β c chi w p ω).re) : ℝ) : ℂ) ∂configMeasure haarG‖
      ≤ ρ ^ A.card *
        ∫ ω, R ω * Real.exp (∑ p, (coupling β c chi w p ω).re) ∂configMeasure haarG := by
  classical
  letI : IsProbabilityMeasure
      (configMeasure (E := E) (F := F) (X := X) haarG) := by
    unfold configMeasure
    infer_instance
  have hWtw (σ : E → ZMod N) (ω : Config G E F X) :
      psi (holonomy (baseWord wC y0) (columnTwist z σ ω)) =
        ζ ^ (q * ∑ p ∈ A, baseCharge (w p) σ).val *
          psi (holonomy (baseWord wC y0) ω) := by
    rw [znb_holonomy_twist z hzN hcentral, znb_charge_base,
      znb_character_pow z psi (ζ ^ q.val) hpsiz,
      znb_pow_mul ζ hζ, hStokes σ]
  exact centre_flip_bound (Ω := Config G E F X) (S := E → ZMod N)
    N ζ hζ
    (configMeasure haarG) (columnTwist z)
    (znb_columnTwist_preserving haarG hleft z)
    (fun σ p => baseCharge (w p) σ) hsurj
    (coupling β c chi w) (znb_measurable_coupling β c chi hchim w)
    (β * (Fintype.card F : ℝ)) (znb_coupling_bound β hβ c hc chi hchi1 w)
    (znb_coupling_twist z hzN hcentral β c chi ζ hchiz w)
    R hRm hR0 hRtw hRint
    (fun ω => psi (holonomy (baseWord wC y0) ω))
    (hpsim.comp (znb_measurable_holonomy (baseWord wC y0)))
    (fun ω => hpsi1 (holonomy (baseWord wC y0) ω))
    q A hWtw ρ hρ

/-- B2a. Explicit charge of a torus plaquette (discrete curl). -/
theorem torus_charge_explicit {m n N : ℕ} (σ : TorusEdge m n → ZMod N) (p : Fin m × Fin n) :
    baseCharge (torusWord p) σ =
      σ (Sum.inl (p.1, p.2)) + σ (Sum.inr (finRotate m p.1, p.2))
        - σ (Sum.inl (p.1, finRotate n p.2)) - σ (Sum.inr (p.1, p.2)) := by
  simp [torusWord, baseCharge, sub_eq_add_neg, add_assoc]

/-- B2b. On the torus the plaquette charges always sum to zero. -/
theorem torus_charge_sum {m n N : ℕ} (σ : TorusEdge m n → ZMod N) :
    ∑ p : Fin m × Fin n, baseCharge (torusWord p) σ = 0 := by
  classical
  have hH : (∑ p : Fin m × Fin n, σ (Sum.inl (p.1, finRotate n p.2))) =
      ∑ p : Fin m × Fin n, σ (Sum.inl p) := by
    exact Equiv.sum_comp (Equiv.prodCongr (Equiv.refl (Fin m)) (finRotate n))
      (fun p : Fin m × Fin n => σ (Sum.inl p))
  have hV : (∑ p : Fin m × Fin n, σ (Sum.inr (finRotate m p.1, p.2))) =
      ∑ p : Fin m × Fin n, σ (Sum.inr p) := by
    exact Equiv.sum_comp (Equiv.prodCongr (finRotate m) (Equiv.refl (Fin n)))
      (fun p : Fin m × Fin n => σ (Sum.inr p))
  simp only [torus_charge_explicit, Finset.sum_sub_distrib, Finset.sum_add_distrib]
  rw [hH, hV]
  abel

/-- B2c. On the torus (periods at least two) every plaquette charge assignment of total charge zero is realised by
column variables. -/
theorem torus_charge_image {m n N : ℕ} (hm : 2 ≤ m) (hn : 2 ≤ n) (t : Fin m × Fin n → ZMod N)
    (ht : ∑ p, t p = 0) :
    ∃ σ : TorusEdge m n → ZMod N, ∀ p, baseCharge (torusWord p) σ = t p := by
  classical
  obtain ⟨m', rfl⟩ : ∃ m', m = m' + 1 := ⟨m - 1, by omega⟩
  obtain ⟨n', rfl⟩ : ∃ n', n = n' + 1 := ⟨n - 1, by omega⟩
  let c : Fin (m' + 1) → ZMod N :=
    fun i => ∑ j : Fin (n' + 1), t (i, j)
  have hc : (∑ i, c i) = 0 := by
    dsimp only [c]
    exact (Fintype.sum_prod_type t).symm.trans ht
  let d : Fin (m' + 1) → Fin (n' + 1) → ZMod N :=
    fun i j => (if j = 0 then c i else 0) - t (i, j)
  have hd (i : Fin (m' + 1)) : (∑ j, d i j) = 0 := by
    dsimp only [d]
    rw [Finset.sum_sub_distrib]
    have hcorr : (∑ j : Fin (n' + 1), if j = 0 then c i else (0 : ZMod N)) =
        c i := by
      simpa only [Finset.mem_univ, if_true] using
        (Finset.sum_ite_eq' (Finset.univ : Finset (Fin (n' + 1)))
          (0 : Fin (n' + 1)) (fun _ => c i))
    rw [hcorr]
    change c i - c i = 0
    exact sub_self _
  let v : Fin (m' + 1) → Fin (n' + 1) → ZMod N :=
    fun i j => if j = 0 then znb_prefix c i.val else 0
  let h : Fin (m' + 1) → Fin (n' + 1) → ZMod N :=
    fun i j => znb_prefix (d i) j.val
  have hv (i : Fin (m' + 1)) (j : Fin (n' + 1)) :
      v (finRotate (m' + 1) i) j - v i j =
        (if j = 0 then c i else 0) := by
    by_cases hj : j = 0
    · simp only [v, if_pos hj]
      exact znb_cycle c hc i
    · simp only [v, if_neg hj, sub_self]
  have hh (i : Fin (m' + 1)) (j : Fin (n' + 1)) :
      h i (finRotate (n' + 1) j) - h i j = d i j :=
    znb_cycle (d i) (hd i) j
  let σ : TorusEdge (m' + 1) (n' + 1) → ZMod N := fun e =>
    match e with
    | Sum.inl p => h p.1 p.2
    | Sum.inr p => v p.1 p.2
  refine ⟨σ, ?_⟩
  intro p
  rcases p with ⟨i, j⟩
  rw [torus_charge_explicit]
  change h i j + v (finRotate (m' + 1) i) j -
      h i (finRotate (n' + 1) j) - v i j = t (i, j)
  calc
    h i j + v (finRotate (m' + 1) i) j -
        h i (finRotate (n' + 1) j) - v i j =
      (v (finRotate (m' + 1) i) j - v i j) -
        (h i (finRotate (n' + 1) j) - h i j) := by abel
    _ = (if j = 0 then c i else 0) - d i j := by rw [hv, hh]
    _ = t (i, j) := by
      dsimp only [d]
      abel

/-- B3. Wilson-type twist ratio on (torus `m × n`) × (finite fibre `F`), with a finite family of neutral extra terms
(complex coefficients): `Z k` multiplies the weights of the base plaquette `p₀` by `ζ ^ k` at every fibre site. -/
theorem wilson_twist_ratio_torus
    {G F X Q : Type*} [Group G] [MeasurableSpace G] [MeasurableMul₂ G] [MeasurableInv G]
    [Fintype F] [Fintype X] [Fintype Q]
    (N : ℕ) [NeZero N] (ζ : ℂ) (hζ : ζ ^ N = 1)
    (m n : ℕ) (hm : 2 ≤ m) (hn : 2 ≤ n)
    (haarG : Measure G) [IsProbabilityMeasure haarG]
    (hleft : ∀ g : G, MeasurePreserving (fun h : G => g * h) haarG haarG)
    (z : G) (hzN : z ^ N = 1) (hcentral : ∀ g : G, z * g = g * z)
    (chi : G → ℂ) (hchim : Measurable chi) (hchi1 : ∀ g, ‖chi g‖ ≤ 1)
    (hchiz : ∀ g, chi (z * g) = ζ * chi g)
    (weights : (Fin m × Fin n) → F → ℂ) (hweights : ∀ p y, ‖weights p y‖ ≤ 1)
    (β : ℝ) (hβ : 0 ≤ β)
    (wq : Q → Word (TorusEdge m n) F X) (hneutral : ∀ k, Neutral N (wq k)) (coef : Q → ℂ)
    (q : ZMod N) (ρ : ℝ)
    (hρ : ∀ t : ℂ, ‖t‖ ≤ β * (Fintype.card F : ℝ) →
      ‖∑ j : ZMod N, ζ ^ (q * j).val * ((Real.exp ((ζ ^ j.val * t).re) : ℝ) : ℂ)‖
        ≤ ρ * ∑ j : ZMod N, Real.exp ((ζ ^ j.val * t).re))
    (p₀ : Fin m × Fin n) :
    ‖∑ k : ZMod N, ζ ^ (q * k).val *
        ((∫ ω, termsWeight chi wq coef ω * Real.exp (∑ p, (coupling β
            (fun p y => if p = p₀ then ζ ^ k.val * weights p y else weights p y) chi torusWord p ω).re)
            ∂configMeasure haarG : ℝ) : ℂ)‖
      ≤ ρ ^ (m * n) *
        ∑ k : ZMod N, ∫ ω, termsWeight chi wq coef ω * Real.exp (∑ p, (coupling β
            (fun p y => if p = p₀ then ζ ^ k.val * weights p y else weights p y) chi torusWord p ω).re)
            ∂configMeasure haarG := by
  classical
  letI : IsProbabilityMeasure
      (configMeasure (E := TorusEdge m n) (F := F) (X := X) haarG) := by
    unfold configMeasure
    infer_instance
  have himg :
      ∀ t : (Fin m × Fin n) → ZMod N, ∑ p, t p = 0 →
        ∃ σ : TorusEdge m n → ZMod N,
          (fun p => baseCharge (torusWord p) σ) = t := by
    intro t ht
    obtain ⟨σ, hσ⟩ := torus_charge_image hm hn t ht
    exact ⟨σ, funext hσ⟩
  have htwisted (k : ZMod N) (p : Fin m × Fin n)
      (ω : Config G (TorusEdge m n) F X) :
      coupling β
          (fun p y => if p = p₀ then ζ ^ k.val * weights p y else weights p y)
          chi torusWord p ω =
        (if p = p₀ then ζ ^ k.val else 1) *
          coupling β weights chi torusWord p ω := by
    by_cases hp : p = p₀
    · simp only [coupling, if_pos hp, Finset.mul_sum]
      apply Finset.sum_congr rfl
      intro y _
      ring
    · simp only [coupling, if_neg hp, one_mul]
  have hmain := twist_ratio_bound
    (Ω := Config G (TorusEdge m n) F X) (S := TorusEdge m n → ZMod N)
    N ζ hζ
    (configMeasure haarG) (columnTwist z)
    (znb_columnTwist_preserving haarG hleft z)
    (fun σ p => baseCharge (torusWord p) σ) himg
    (coupling β weights chi torusWord)
    (znb_measurable_coupling β weights chi hchim torusWord)
    (β * (Fintype.card F : ℝ))
    (znb_coupling_bound β hβ weights hweights chi hchi1 torusWord)
    (znb_coupling_twist z hzN hcentral β weights chi ζ hchiz torusWord)
    (termsWeight chi wq coef)
    (znb_measurable_termsWeight chi hchim wq coef)
    (fun ω => (Real.exp_pos _).le)
    (znb_termsWeight_twist z hzN hcentral chi wq hneutral coef)
    (znb_integrable_density haarG chi hchim hchi1 wq coef
      β hβ weights hweights torusWord)
    q ρ hρ p₀
  simpa only [htwisted, Fintype.card_prod, Fintype.card_fin] using hmain

/-- B3c. B3 with the crude constant `1 - exp (-2 β |F|)` (primitive root, non-zero charge). -/
theorem wilson_twist_ratio_torus_crude
    {G F X Q : Type*} [Group G] [MeasurableSpace G] [MeasurableMul₂ G] [MeasurableInv G]
    [Fintype F] [Fintype X] [Fintype Q]
    (N : ℕ) [NeZero N] (ζ : ℂ) (hζ : IsPrimitiveRoot ζ N)
    (m n : ℕ) (hm : 2 ≤ m) (hn : 2 ≤ n)
    (haarG : Measure G) [IsProbabilityMeasure haarG]
    (hleft : ∀ g : G, MeasurePreserving (fun h : G => g * h) haarG haarG)
    (z : G) (hzN : z ^ N = 1) (hcentral : ∀ g : G, z * g = g * z)
    (chi : G → ℂ) (hchim : Measurable chi) (hchi1 : ∀ g, ‖chi g‖ ≤ 1)
    (hchiz : ∀ g, chi (z * g) = ζ * chi g)
    (weights : (Fin m × Fin n) → F → ℂ) (hweights : ∀ p y, ‖weights p y‖ ≤ 1)
    (β : ℝ) (hβ : 0 ≤ β)
    (wq : Q → Word (TorusEdge m n) F X) (hneutral : ∀ k, Neutral N (wq k)) (coef : Q → ℂ)
    (q : ZMod N) (hq : q ≠ 0) (p₀ : Fin m × Fin n) :
    ‖∑ k : ZMod N, ζ ^ (q * k).val *
        ((∫ ω, termsWeight chi wq coef ω * Real.exp (∑ p, (coupling β
            (fun p y => if p = p₀ then ζ ^ k.val * weights p y else weights p y) chi torusWord p ω).re)
            ∂configMeasure haarG : ℝ) : ℂ)‖
      ≤ (1 - Real.exp (-2 * (β * (Fintype.card F : ℝ)))) ^ (m * n) *
        ∑ k : ZMod N, ∫ ω, termsWeight chi wq coef ω * Real.exp (∑ p, (coupling β
            (fun p y => if p = p₀ then ζ ^ k.val * weights p y else weights p y) chi torusWord p ω).re)
            ∂configMeasure haarG := by
  classical
  refine wilson_twist_ratio_torus N ζ hζ.pow_eq_one m n hm hn
    haarG hleft z hzN hcentral chi hchim hchi1 hchiz
    weights hweights β hβ wq hneutral coef q
    (1 - Real.exp (-2 * (β * (Fintype.card F : ℝ)))) ?_ p₀
  intro t ht
  refine (rho_crude N ζ hζ q hq t).trans ?_
  apply mul_le_mul_of_nonneg_right ?_
    (Finset.sum_nonneg (fun j _ => (Real.exp_pos _).le))
  have he :
      Real.exp (-2 * (β * (Fintype.card F : ℝ))) ≤ Real.exp (-2 * ‖t‖) :=
    Real.exp_le_exp.mpr (by linarith)
  linarith

end CentreZN

end
