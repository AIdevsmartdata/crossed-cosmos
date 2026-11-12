import Mathlib

/-! # CentreZN : énoncés figés par le pilote (12/11/2026), avant toute preuve.

Généralisation au centre cyclique `ZMod N` de la borne de retournement de colonne et du rapport de torsion
(cas `N = 2` : `TubeArea.column_flip_bound`, `TubeArea.twist_ratio_bound`, publiés le 12/11/2026).
Partie A : forme abstraite. Partie B : théorie de type Wilson, tore discret. Toutes les preuves sont `sorry`. -/

set_option autoImplicit false

open MeasureTheory Finset

noncomputable section

namespace CentreZN

/-! ## Partie A : forme abstraite -/

/-- A1. Abstract centre-twist bound (open surface). Twists `τ s` preserve `μ`; the charge map `chg` onto
`P → ZMod N` is surjective; the complex couplings rotate, `T p ∘ τ s = ζ ^ (chg s p) • T p`; the weight `R` is
invariant; the observable `W` takes the phase `ζ ^ (q • Σ_{p ∈ A} chg s p)`; `ρ` dominates the one-plaquette
Fourier ratio on the disc of radius `κ`. -/
theorem centre_flip_bound
    {Ω S P : Type*} [MeasurableSpace Ω] [Fintype P] [DecidableEq P]
    (N : ℕ) [NeZero N] (ζ : ℂ) (hζ : ζ ^ N = 1)
    (μ : Measure Ω) [IsProbabilityMeasure μ]
    (τ : S → Ω → Ω) (hτ : ∀ s, MeasurePreserving (τ s) μ μ)
    (chg : S → P → ZMod N) (hsurj : Function.Surjective chg)
    (T : P → Ω → ℂ) (hTm : ∀ p, Measurable (T p))
    (κ : ℝ) (hT : ∀ p ω, ‖T p ω‖ ≤ κ)
    (hTτ : ∀ s p ω, T p (τ s ω) = ζ ^ (chg s p).val * T p ω)
    (R : Ω → ℝ) (hRm : Measurable R) (hR0 : ∀ ω, 0 ≤ R ω) (hRτ : ∀ s ω, R (τ s ω) = R ω)
    (hRint : Integrable (fun ω => R ω * Real.exp (∑ p, (T p ω).re)) μ)
    (W : Ω → ℂ) (hWm : Measurable W) (hW1 : ∀ ω, ‖W ω‖ ≤ 1)
    (q : ZMod N) (A : Finset P)
    (hWτ : ∀ s ω, W (τ s ω) = ζ ^ (q * ∑ p ∈ A, chg s p).val * W ω)
    (ρ : ℝ)
    (hρ : ∀ t : ℂ, ‖t‖ ≤ κ →
      ‖∑ j : ZMod N, ζ ^ (q * j).val * ((Real.exp ((ζ ^ j.val * t).re) : ℝ) : ℂ)‖
        ≤ ρ * ∑ j : ZMod N, Real.exp ((ζ ^ j.val * t).re)) :
    ‖∫ ω, W ω * ((R ω * Real.exp (∑ p, (T p ω).re) : ℝ) : ℂ) ∂μ‖
      ≤ ρ ^ A.card * ∫ ω, R ω * Real.exp (∑ p, (T p ω).re) ∂μ := by
  sorry

/-- A2. Abstract twist-ratio bound (closed surface). Every charge assignment of total charge zero is realised by a
twist. `Z k` is the partition function in which the coupling of the plaquette `p₀` is multiplied by `ζ ^ k`; the
left side is the norm of its Fourier transform at `q`, the right side involves the sum of all `Z k`. -/
theorem twist_ratio_bound
    {Ω S P : Type*} [MeasurableSpace Ω] [Fintype P] [DecidableEq P]
    (N : ℕ) [NeZero N] (ζ : ℂ) (hζ : ζ ^ N = 1)
    (μ : Measure Ω) [IsProbabilityMeasure μ]
    (τ : S → Ω → Ω) (hτ : ∀ s, MeasurePreserving (τ s) μ μ)
    (chg : S → P → ZMod N)
    (himg : ∀ t : P → ZMod N, ∑ p, t p = 0 → ∃ s, chg s = t)
    (T : P → Ω → ℂ) (hTm : ∀ p, Measurable (T p))
    (κ : ℝ) (hT : ∀ p ω, ‖T p ω‖ ≤ κ)
    (hTτ : ∀ s p ω, T p (τ s ω) = ζ ^ (chg s p).val * T p ω)
    (R : Ω → ℝ) (hRm : Measurable R) (hR0 : ∀ ω, 0 ≤ R ω) (hRτ : ∀ s ω, R (τ s ω) = R ω)
    (hRint : Integrable (fun ω => R ω * Real.exp (∑ p, (T p ω).re)) μ)
    (q : ZMod N) (ρ : ℝ)
    (hρ : ∀ t : ℂ, ‖t‖ ≤ κ →
      ‖∑ j : ZMod N, ζ ^ (q * j).val * ((Real.exp ((ζ ^ j.val * t).re) : ℝ) : ℂ)‖
        ≤ ρ * ∑ j : ZMod N, Real.exp ((ζ ^ j.val * t).re))
    (p₀ : P) :
    ‖∑ k : ZMod N, ζ ^ (q * k).val *
        ((∫ ω, R ω * Real.exp (∑ p, ((if p = p₀ then ζ ^ k.val else 1) * T p ω).re) ∂μ : ℝ) : ℂ)‖
      ≤ ρ ^ Fintype.card P *
        ∑ k : ZMod N, ∫ ω, R ω * Real.exp (∑ p, ((if p = p₀ then ζ ^ k.val else 1) * T p ω).re) ∂μ := by
  sorry

/-- A3. Crude constant: for a primitive `N`-th root of unity and a non-zero charge `q`, the one-plaquette Fourier
ratio is at most `1 - exp (-2 ‖t‖)`. -/
theorem rho_crude (N : ℕ) [NeZero N] (ζ : ℂ) (hζ : IsPrimitiveRoot ζ N) (q : ZMod N) (hq : q ≠ 0)
    (t : ℂ) :
    ‖∑ j : ZMod N, ζ ^ (q * j).val * ((Real.exp ((ζ ^ j.val * t).re) : ℝ) : ℂ)‖
      ≤ (1 - Real.exp (-2 * ‖t‖)) * ∑ j : ZMod N, Real.exp ((ζ ^ j.val * t).re) := by
  sorry

/-- A4. The case `N = 2`, `ζ = -1`, `q = 1`: the constant is `tanh ‖t‖`. -/
theorem rho_two (t : ℂ) :
    ‖∑ j : ZMod 2, (-1 : ℂ) ^ ((1 : ZMod 2) * j).val * ((Real.exp (((-1 : ℂ) ^ j.val * t).re) : ℝ) : ℂ)‖
      ≤ Real.tanh ‖t‖ * ∑ j : ZMod 2, Real.exp (((-1 : ℂ) ^ j.val * t).re) := by
  sorry

/-- A5. Sharpness: on `ZMod N` with the uniform probability measure, translations preserve the measure, the coupling
`j ↦ ζ ^ j * t` and the observable `j ↦ ζ ^ (q * j)` have the covariances required by A1 (one plaquette, charge of a
translation by `s` equal to `s`, coupling of norm `‖t‖`, observable of norm one), and the two integrals are exactly
the normalised Fourier sums of A1's hypothesis: A1 is an equality here with `ρ` the ratio at `t`. -/
theorem sharp_one_plaquette (N : ℕ) [NeZero N] (ζ : ℂ) (hζ : ζ ^ N = 1) (q : ZMod N) (t : ℂ) :
    ∃ μ : Measure (ZMod N), IsProbabilityMeasure μ ∧
      (∀ s : ZMod N, MeasurePreserving (fun j : ZMod N => s + j) μ μ) ∧
      (∀ j : ZMod N, ‖ζ ^ j.val * t‖ = ‖t‖) ∧ (∀ j : ZMod N, ‖ζ ^ (q * j).val‖ = 1) ∧
      (∀ s j : ZMod N, ζ ^ (s + j).val * t = ζ ^ s.val * (ζ ^ j.val * t)) ∧
      (∀ s j : ZMod N, ζ ^ (q * (s + j)).val = ζ ^ (q * s).val * ζ ^ (q * j).val) ∧
      (∫ j, ζ ^ (q * j).val * ((Real.exp ((ζ ^ j.val * t).re) : ℝ) : ℂ) ∂μ)
          = (N : ℂ)⁻¹ * ∑ j : ZMod N, ζ ^ (q * j).val * ((Real.exp ((ζ ^ j.val * t).re) : ℝ) : ℂ) ∧
      (∫ j, Real.exp ((ζ ^ j.val * t).re) ∂μ) = (N : ℝ)⁻¹ * ∑ j : ZMod N, Real.exp ((ζ ^ j.val * t).re) := by
  sorry

/-- A6a. A1 with the crude constant (primitive root, non-zero charge). -/
theorem centre_flip_bound_crude
    {Ω S P : Type*} [MeasurableSpace Ω] [Fintype P] [DecidableEq P]
    (N : ℕ) [NeZero N] (ζ : ℂ) (hζ : IsPrimitiveRoot ζ N)
    (μ : Measure Ω) [IsProbabilityMeasure μ]
    (τ : S → Ω → Ω) (hτ : ∀ s, MeasurePreserving (τ s) μ μ)
    (chg : S → P → ZMod N) (hsurj : Function.Surjective chg)
    (T : P → Ω → ℂ) (hTm : ∀ p, Measurable (T p))
    (κ : ℝ) (hT : ∀ p ω, ‖T p ω‖ ≤ κ)
    (hTτ : ∀ s p ω, T p (τ s ω) = ζ ^ (chg s p).val * T p ω)
    (R : Ω → ℝ) (hRm : Measurable R) (hR0 : ∀ ω, 0 ≤ R ω) (hRτ : ∀ s ω, R (τ s ω) = R ω)
    (hRint : Integrable (fun ω => R ω * Real.exp (∑ p, (T p ω).re)) μ)
    (W : Ω → ℂ) (hWm : Measurable W) (hW1 : ∀ ω, ‖W ω‖ ≤ 1)
    (q : ZMod N) (hq : q ≠ 0) (A : Finset P)
    (hWτ : ∀ s ω, W (τ s ω) = ζ ^ (q * ∑ p ∈ A, chg s p).val * W ω) :
    ‖∫ ω, W ω * ((R ω * Real.exp (∑ p, (T p ω).re) : ℝ) : ℂ) ∂μ‖
      ≤ (1 - Real.exp (-2 * κ)) ^ A.card * ∫ ω, R ω * Real.exp (∑ p, (T p ω).re) ∂μ := by
  sorry

/-- A6b. A2 with the crude constant (primitive root, non-zero charge). -/
theorem twist_ratio_bound_crude
    {Ω S P : Type*} [MeasurableSpace Ω] [Fintype P] [DecidableEq P]
    (N : ℕ) [NeZero N] (ζ : ℂ) (hζ : IsPrimitiveRoot ζ N)
    (μ : Measure Ω) [IsProbabilityMeasure μ]
    (τ : S → Ω → Ω) (hτ : ∀ s, MeasurePreserving (τ s) μ μ)
    (chg : S → P → ZMod N)
    (himg : ∀ t : P → ZMod N, ∑ p, t p = 0 → ∃ s, chg s = t)
    (T : P → Ω → ℂ) (hTm : ∀ p, Measurable (T p))
    (κ : ℝ) (hT : ∀ p ω, ‖T p ω‖ ≤ κ)
    (hTτ : ∀ s p ω, T p (τ s ω) = ζ ^ (chg s p).val * T p ω)
    (R : Ω → ℝ) (hRm : Measurable R) (hR0 : ∀ ω, 0 ≤ R ω) (hRτ : ∀ s ω, R (τ s ω) = R ω)
    (hRint : Integrable (fun ω => R ω * Real.exp (∑ p, (T p ω).re)) μ)
    (q : ZMod N) (hq : q ≠ 0) (p₀ : P) :
    ‖∑ k : ZMod N, ζ ^ (q * k).val *
        ((∫ ω, R ω * Real.exp (∑ p, ((if p = p₀ then ζ ^ k.val else 1) * T p ω).re) ∂μ : ℝ) : ℂ)‖
      ≤ (1 - Real.exp (-2 * κ)) ^ Fintype.card P *
        ∑ k : ZMod N, ∫ ω, R ω * Real.exp (∑ p, ((if p = p₀ then ζ ^ k.val else 1) * T p ω).re) ∂μ := by
  sorry

/-- A7a. `N = 2` recovers the published column-flip bound (statement of `TubeArea.column_flip_bound`, verbatim, as
restated in its verification footer); to be derived from A1 and A4. -/
theorem recover_column_flip_bound
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
      ≤ Real.tanh κ ^ A.card * ∫ ω, R ω * Real.exp (∑ p, K p ω) ∂μ := by
  sorry

/-- A7b. `N = 2` recovers the published twist-ratio bound (statement of `TubeArea.twist_ratio_bound`, verbatim, as
restated in its verification footer); to be derived from A2 and A4. -/
theorem recover_twist_ratio_bound
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
          + ∫ ω, R ω * Real.exp (∑ p, (if p = p₀ then -(K p ω) else K p ω)) ∂μ) := by
  sorry

/-! ## Partie B : théorie de type Wilson à élément central d'ordre `N` (définitions figées) -/

/-- Configurations: long links `(e, y)` (base edge `e`, fibre site `y`) and other links `x`. -/
abbrev Config (G E F X : Type*) := ((E × F) → G) × (X → G)

/-- The product of the single-link measure over all links. -/
def configMeasure {G E F X : Type*} [MeasurableSpace G] [Fintype E] [Fintype F] [Fintype X]
    (haarG : Measure G) : Measure (Config G E F X) :=
  (Measure.pi fun _ : E × F => haarG).prod (Measure.pi fun _ : X => haarG)

/-- Column twist: every long link `(e, y)` is left-multiplied by `z ^ (σ e).val`; other links are unchanged. -/
def columnTwist {G E F X : Type*} [Monoid G] {N : ℕ} (z : G) (σ : E → ZMod N)
    (ω : Config G E F X) : Config G E F X :=
  (fun ey => z ^ (σ ey.1).val * ω.1 ey, ω.2)

/-- Positive orientation: the link itself; negative orientation: its inverse. -/
def orientedLink {G : Type*} [Inv G] : Bool → G → G
  | true, g => g
  | false, g => g⁻¹

/-- A word: a list of oriented letters, each a long link `Sum.inl (e, y)` or another link `Sum.inr x`. -/
abbrev Word (E F X : Type*) := List (((E × F) ⊕ X) × Bool)

/-- Ordered holonomy of a word (empty word: `1`). -/
def holonomy {G E F X : Type*} [Group G] : Word E F X → Config G E F X → G
  | [], _ => 1
  | (Sum.inl ey, b) :: w, ω => orientedLink b (ω.1 ey) * holonomy w ω
  | (Sum.inr x, b) :: w, ω => orientedLink b (ω.2 x) * holonomy w ω

/-- Charge of a word: signed sum (with multiplicity) of the column variables of its long letters. -/
def charge {E F X : Type*} {N : ℕ} : Word E F X → (E → ZMod N) → ZMod N
  | [], _ => 0
  | (Sum.inl ey, b) :: w, σ => (if b then σ ey.1 else -σ ey.1) + charge w σ
  | (Sum.inr _, _) :: w, σ => charge w σ

/-- A word is neutral for `ZMod N` when its charge vanishes for all column variables. -/
def Neutral {E F X : Type*} (N : ℕ) (w : Word E F X) : Prop :=
  ∀ σ : E → ZMod N, charge w σ = 0

/-- The word of a base path (list of oriented base edges) at the fibre site `y`. -/
def baseWord {E F X : Type*} (w : List (E × Bool)) (y : F) : Word E F X :=
  w.map fun a => (Sum.inl (a.1, y), a.2)

/-- Charge of a base path: signed sum (with multiplicity) of the column variables along it. -/
def baseCharge {E : Type*} {N : ℕ} : List (E × Bool) → (E → ZMod N) → ZMod N
  | [], _ => 0
  | a :: w, σ => (if a.2 then σ a.1 else -σ a.1) + baseCharge w σ

/-- Complex Wilson coupling of the base plaquette `p`: `β Σ_y c p y χ(holonomy of its word at y)`.
The action uses its real part. -/
def coupling {G E F X P : Type*} [Group G] [Fintype F]
    (β : ℝ) (c : P → F → ℂ) (chi : G → ℂ) (w : P → List (E × Bool)) (p : P)
    (ω : Config G E F X) : ℂ :=
  (β : ℂ) * ∑ y, c p y * chi (holonomy (baseWord (w p) y) ω)

/-- Weight of a finite family of extra terms: `exp (Σ_k Re (coef k · χ(holonomy of the word k)))`. -/
def termsWeight {G E F X Q : Type*} [Group G] [Fintype Q]
    (chi : G → ℂ) (wq : Q → Word E F X) (coef : Q → ℂ) (ω : Config G E F X) : ℝ :=
  Real.exp (∑ k, (coef k * chi (holonomy (wq k) ω)).re)

/-- Edges of the discrete torus `(ℤ/m) × (ℤ/n)`: `Sum.inl (i,j)` is the horizontal edge from `(i,j)` to `(i+1,j)`,
`Sum.inr (i,j)` the vertical edge from `(i,j)` to `(i,j+1)`; indices are cyclic (`finRotate`). -/
abbrev TorusEdge (m n : ℕ) := (Fin m × Fin n) ⊕ (Fin m × Fin n)

/-- Counterclockwise plaquette path from the corner `p = (i,j)`: bottom `H(i,j)` forwards, right `V(i+1,j)`
forwards, top `H(i,j+1)` backwards, left `V(i,j)` backwards. -/
def torusWord {m n : ℕ} (p : Fin m × Fin n) : List (TorusEdge m n × Bool) :=
  [(Sum.inl (p.1, p.2), true), (Sum.inr (finRotate m p.1, p.2), true),
    (Sum.inl (p.1, finRotate n p.2), false), (Sum.inr (p.1, p.2), false)]

/-! ## Partie B : énoncés -/

/-- B0. A mixed plaquette (long link at `y`, other link, the same column at `y'` backwards, other link backwards)
is neutral for every `N`. -/
theorem mixed_word_neutral {E F X : Type*} (N : ℕ) (e : E) (y y' : F) (x x' : X) :
    Neutral N ([(Sum.inl (e, y), true), (Sum.inr x, true), (Sum.inl (e, y'), false), (Sum.inr x', false)] :
      Word E F X) := by
  sorry

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
  sorry

/-- B2a. Explicit charge of a torus plaquette (discrete curl). -/
theorem torus_charge_explicit {m n N : ℕ} (σ : TorusEdge m n → ZMod N) (p : Fin m × Fin n) :
    baseCharge (torusWord p) σ =
      σ (Sum.inl (p.1, p.2)) + σ (Sum.inr (finRotate m p.1, p.2))
        - σ (Sum.inl (p.1, finRotate n p.2)) - σ (Sum.inr (p.1, p.2)) := by
  sorry

/-- B2b. On the torus the plaquette charges always sum to zero. -/
theorem torus_charge_sum {m n N : ℕ} (σ : TorusEdge m n → ZMod N) :
    ∑ p : Fin m × Fin n, baseCharge (torusWord p) σ = 0 := by
  sorry

/-- B2c. On the torus (periods at least two) every plaquette charge assignment of total charge zero is realised by
column variables. -/
theorem torus_charge_image {m n N : ℕ} (hm : 2 ≤ m) (hn : 2 ≤ n) (t : Fin m × Fin n → ZMod N)
    (ht : ∑ p, t p = 0) :
    ∃ σ : TorusEdge m n → ZMod N, ∀ p, baseCharge (torusWord p) σ = t p := by
  sorry

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
  sorry

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
  sorry

end CentreZN

end
