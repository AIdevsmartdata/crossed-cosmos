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
