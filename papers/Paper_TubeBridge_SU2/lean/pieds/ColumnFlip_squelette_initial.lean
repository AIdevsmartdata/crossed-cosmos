/-
Column-flip bound (abstract form).  Project: twisted tube, 11 November 2026.

Mathematical content.  A probability space carries, for every sign configuration `σ` on a finite set of "edges" `E`,
a measure-preserving map `τ σ` ("flip the columns where σ = -1").  Each "plaquette" `p` has a boundary `bd p ⊆ E`; its sign
is the product of the edge signs on its boundary.  The plaquette couplings `K p` are odd under the flips (they pick up the
plaquette sign), the remaining weight `R ≥ 0` is invariant, and the observable `W` (a Wilson loop bounding the set of
plaquettes `A`) picks up the product of the plaquette signs over `A`.  If the plaquette-sign map is surjective (plaquette signs
are independent, as on a planar patch with free boundary), then

    |∫ W · R · exp(∑ K)| ≤ tanh(κ)^{|A|} · ∫ R · exp(∑ K)        whenever |K p| ≤ κ.

For SU(2) Wilson theory on (planar patch) × (finite fibre with n_F sites), κ = β · n_F: this is the elementary area law.
The STATEMENT of `column_flip_bound` below is fixed by the pilot; only the proof may be changed.
-/
import Mathlib

open MeasureTheory Finset

namespace TubeArea

/-- Real value (+1 or -1) of a sign. -/
def sgn (u : ℤˣ) : ℝ := ((u : ℤ) : ℝ)

/-- Sign of a plaquette: the product of the edge signs over its boundary. -/
def plaq {E P : Type*} (bd : P → Finset E) (σ : E → ℤˣ) (p : P) : ℤˣ := ∏ e ∈ bd p, σ e

theorem column_flip_bound
    {Ω E P : Type*} [MeasurableSpace Ω] [Fintype E] [DecidableEq E] [Fintype P] [DecidableEq P]
    (μ : Measure Ω) [IsProbabilityMeasure μ]
    (τ : (E → ℤˣ) → Ω → Ω) (hτ : ∀ σ, MeasurePreserving (τ σ) μ μ)
    (bd : P → Finset E)
    (hsurj : Function.Surjective (fun σ : E → ℤˣ => plaq bd σ))
    (K : P → Ω → ℝ) (hKm : ∀ p, Measurable (K p))
    (κ : ℝ) (hK : ∀ p ω, |K p ω| ≤ κ)
    (hKτ : ∀ σ p ω, K p (τ σ ω) = sgn (plaq bd σ p) * K p ω)
    (R : Ω → ℝ) (hRm : Measurable R) (hR0 : ∀ ω, 0 ≤ R ω) (hRτ : ∀ σ ω, R (τ σ ω) = R ω)
    (hRint : Integrable (fun ω => R ω * Real.exp (∑ p, K p ω)) μ)
    (W : Ω → ℝ) (hWm : Measurable W) (hW1 : ∀ ω, |W ω| ≤ 1)
    (A : Finset P)
    (hWτ : ∀ σ ω, W (τ σ ω) = sgn (∏ p ∈ A, plaq bd σ p) * W ω) :
    |∫ ω, W ω * (R ω * Real.exp (∑ p, K p ω)) ∂μ|
      ≤ Real.tanh κ ^ A.card * ∫ ω, R ω * Real.exp (∑ p, K p ω) ∂μ := by
  sorry

end TubeArea
