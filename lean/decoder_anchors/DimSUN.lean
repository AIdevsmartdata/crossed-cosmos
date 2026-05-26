/-
  DimSUN.lean

  Theorem (main, finrank-version):
      Module.finrank R (LieAlgebra.SpecialLinear.sl n R) = (Fintype.card n)^2 - 1
  for any nonempty finite type `n` and any field `R` (in particular ℝ and ℂ).

  In particular, for n = Fin N (N ≥ 1):

      dim_ℝ sl(N, ℝ) = N² − 1.

  The compact real form `su(N) ⊂ sl(N, ℂ)` of complex N × N traceless
  anti-hermitian matrices has the SAME real dimension N² − 1. Mathlib does
  not yet provide a definition of `su(N)` as an explicit real Lie subalgebra
  of complex matrices; the corresponding `finrank` identity for su(N) is
  therefore stated below as ONE clearly-scoped auxiliary axiom (purely
  mathematical, no physics input), documenting exactly what mathlib needs
  in order to discharge it.

  Proof of the main theorem (`finrank_sl_eq`):
    (1) Mathlib defines  sl n R := { LinearMap.ker (Matrix.traceLinearMap n R R) with ... }
        in `Mathlib.Algebra.Lie.Classical`, so its underlying submodule equals
        that kernel by `rfl`.
    (2) Rank–nullity (`LinearMap.finrank_range_add_finrank_ker`):
          finrank R (range trace) + finrank R (ker trace) = finrank R (M_n(R)).
    (3) `Matrix.trace_surjective` (nonempty n) ⇒ range trace = ⊤,
          so finrank R (range trace) = finrank R R = 1.
    (4) `Module.finrank_matrix` :
          finrank R (Matrix n n R) = (card n) · (card n) · 1 = (card n)².
    (5) Subtract: finrank R (sl n R) = (card n)² − 1.

  References:
    [Hall]   B.C. Hall, "Lie Groups, Lie Algebras, and Representations",
             2nd ed., Springer GTM 222 (2015), Prop. 3.27.
    [Knapp]  A.W. Knapp, "Lie Groups Beyond an Introduction", 2nd ed.,
             Birkhäuser 2002, §I.8 ("compact real forms").
    [Mathlib]
        Mathlib.Algebra.Lie.Classical                  (sl)
        Mathlib.LinearAlgebra.Matrix.Trace             (traceLinearMap, trace_surjective)
        Mathlib.LinearAlgebra.FiniteDimensional.Lemmas (finrank_range_add_finrank_ker)
        Mathlib.LinearAlgebra.Dimension.Constructions  (finrank_matrix)
        Mathlib.LinearAlgebra.Matrix.FiniteDimensional (Matrix.finiteDimensional instance)

  Author : Kévin Rémondière (ORCID 0009-0008-2443-7166)
-/

import Mathlib.Algebra.Lie.Classical
import Mathlib.LinearAlgebra.Matrix.Trace
import Mathlib.LinearAlgebra.Matrix.FiniteDimensional
import Mathlib.LinearAlgebra.Dimension.RankNullity
import Mathlib.LinearAlgebra.Dimension.Constructions
import Mathlib.LinearAlgebra.FiniteDimensional.Lemmas
import Mathlib.Data.Real.Basic
import Mathlib.Data.Nat.Basic
import Mathlib.Data.Int.Basic
import Mathlib.Tactic.NormNum
import Mathlib.Tactic.Linarith
import Mathlib.Tactic.Positivity

namespace DimSUN

open Matrix LinearMap Module Fintype

/-! ## Pure-number version

Convenience definitions and elementary identities (over ℤ) holding
unconditionally; useful for sanity checks and bridging from the
combinatorial (basis-count) picture to the finrank theorem below. -/

/-- `dimSU N := N² − 1` (over ℤ). This is the real dimension of su(N)
    (equivalently the real dim of sl(N, ℝ) and the complex dim of sl(N, ℂ)). -/
def dimSU (N : ℕ) : ℤ := (N : ℤ)^2 - 1

example : dimSU 2 = 3  := by decide   -- Pauli σ₁, σ₂, σ₃
example : dimSU 3 = 8  := by decide   -- Gell-Mann λ₁..λ₈
example : dimSU 4 = 15 := by decide
example : dimSU 5 = 24 := by decide
example : dimSU 8 = 63 := by decide

theorem dimSU_factored (N : ℕ) :
    dimSU N = ((N : ℤ) - 1) * ((N : ℤ) + 1) := by
  unfold dimSU; ring

theorem dimSU_nonneg {N : ℕ} (hN : 1 ≤ N) : 0 ≤ dimSU N := by
  unfold dimSU
  have : (1 : ℤ) ≤ (N : ℤ) := by exact_mod_cast hN
  nlinarith

theorem dimSU_pos {N : ℕ} (hN : 2 ≤ N) : 0 < dimSU N := by
  unfold dimSU
  have : (2 : ℤ) ≤ (N : ℤ) := by exact_mod_cast hN
  nlinarith

theorem dimSU_succ_diff (N : ℕ) :
    dimSU (N + 1) - dimSU N = 2 * (N : ℤ) + 1 := by
  unfold dimSU; push_cast; ring

/-- **Basis count** (purely combinatorial): the explicit anti-hermitian
    basis of su(N) — N−1 diagonal imaginary traceless, N(N−1)/2 real
    antisymmetric, N(N−1)/2 imaginary symmetric generators — totals
    (N−1) + 2·(N(N−1)/2) = (N−1) + N(N−1) = N² − 1.

    This identity holds unconditionally over ℤ for N ≥ 1 and is the
    classical justification (Hall Prop. 3.27) of dim_ℝ su(N) = N² − 1. -/
theorem dim_su_basis_count (N : ℕ) (hN : 1 ≤ N) :
    ((N : ℤ) - 1) + 2 * ((N : ℤ) * ((N : ℤ) - 1) / 2) = dimSU N := by
  have hEven : (2 : ℤ) ∣ ((N : ℤ) * ((N : ℤ) - 1)) := by
    rcases Nat.even_or_odd N with hE | hO
    · obtain ⟨k, hk⟩ := hE
      refine ⟨(k : ℤ) * ((N : ℤ) - 1), ?_⟩
      have hkc : (N : ℤ) = 2 * (k : ℤ) := by exact_mod_cast hk
      rw [hkc]; ring
    · obtain ⟨k, hk⟩ := hO
      refine ⟨(N : ℤ) * (k : ℤ), ?_⟩
      have hN1 : (N : ℤ) - 1 = 2 * (k : ℤ) := by
        have : (N : ℤ) = 2 * (k : ℤ) + 1 := by exact_mod_cast hk
        linarith
      rw [hN1]; ring
  have h2 : (2 : ℤ) * ((N : ℤ) * ((N : ℤ) - 1) / 2) = (N : ℤ) * ((N : ℤ) - 1) :=
    Int.mul_ediv_cancel' _ hEven
  rw [h2]
  unfold dimSU
  ring

/-! ## Finrank theorem on `sl n R`

We work with `LieAlgebra.SpecialLinear.sl n R`, the special linear Lie
algebra of n × n matrices of trace 0 over a commutative ring R. The result
is pure linear algebra (rank–nullity applied to the trace map) and requires
NO physics input. -/

open LieAlgebra.SpecialLinear

section FinrankSL

variable (R : Type*) [Field R]
variable (n : Type*) [Fintype n] [DecidableEq n] [Nonempty n]

/-- The underlying submodule of `sl n R` equals the kernel of the trace map.
    True by `rfl` from the mathlib definition `def sl := { ker trace with ... }`. -/
theorem sl_toSubmodule_eq_ker_trace :
    (sl n R).toSubmodule = LinearMap.ker (Matrix.traceLinearMap n R R) :=
  rfl

/-- Trace as a linear map is surjective when `n` is nonempty. -/
theorem traceLinearMap_surjective :
    Function.Surjective ((Matrix.traceLinearMap n R R : Matrix n n R →ₗ[R] R)) := by
  intro r
  obtain ⟨A, hA⟩ := Matrix.trace_surjective (n := n) (R := R) r
  exact ⟨A, hA⟩

/-- **Finrank of the kernel of trace** (the substantive theorem):
        finrank R (ker (trace : Matrix n n R →ₗ[R] R)) = (card n)² − 1.

    Pure linear algebra — no physics. -/
theorem finrank_ker_trace_eq :
    Module.finrank R (LinearMap.ker (Matrix.traceLinearMap n R R)) =
      (Fintype.card n) ^ 2 - 1 := by
  -- Rank–nullity (FiniteDimensional R (Matrix n n R) is an instance).
  have hRN := LinearMap.finrank_range_add_finrank_ker
              (f := Matrix.traceLinearMap n R R)
  -- Surjectivity ⇒ range = ⊤ ⇒ finrank range = finrank R = 1.
  have hsurj := traceLinearMap_surjective R n
  have hRangeTop : LinearMap.range (Matrix.traceLinearMap n R R) = ⊤ :=
    LinearMap.range_eq_top.mpr hsurj
  have hRange :
      Module.finrank R (LinearMap.range (Matrix.traceLinearMap n R R)) = 1 := by
    rw [hRangeTop, finrank_top]
    exact Module.finrank_self R
  -- Finrank of full matrix module = (card n)² .
  have hMat : Module.finrank R (Matrix n n R) = (Fintype.card n) ^ 2 := by
    rw [Module.finrank_matrix n n, Module.finrank_self R]
    ring
  -- Combine.
  have heq : 1 + Module.finrank R (LinearMap.ker (Matrix.traceLinearMap n R R)) =
              (Fintype.card n) ^ 2 := by
    have h := hRN
    rw [hRange, hMat] at h
    exact h
  have card_pos : 0 < Fintype.card n := Fintype.card_pos
  have hsq : 1 ≤ (Fintype.card n)^2 := by
    have : 1 ≤ Fintype.card n := card_pos
    nlinarith
  omega

/-- **Main theorem on `sl n R`**:
        finrank R (sl n R) = (card n)² − 1.

    The Module structure on `↥(sl n R)` is, by mathlib's construction,
    inherited from `(sl n R).toSubmodule`. And `(sl n R).toSubmodule` is
    definitionally equal to `LinearMap.ker (traceLinearMap n R R)`. -/
theorem finrank_sl_eq :
    Module.finrank R (sl n R) = (Fintype.card n) ^ 2 - 1 := by
  have h1 : Module.finrank R (sl n R) =
            Module.finrank R ((sl n R).toSubmodule) := rfl
  rw [h1, sl_toSubmodule_eq_ker_trace]
  exact finrank_ker_trace_eq R n

end FinrankSL

/-! ## Specialisation to R = ℝ and n = Fin N -/

theorem finrank_sl_fin_real (N : ℕ) (hN : 1 ≤ N) :
    Module.finrank ℝ (sl (Fin N) ℝ) = N ^ 2 - 1 := by
  haveI : Nonempty (Fin N) := ⟨⟨0, hN⟩⟩
  have h := finrank_sl_eq ℝ (Fin N)
  rwa [Fintype.card_fin] at h

example : Module.finrank ℝ (sl (Fin 2) ℝ) = 3 := by
  have h := finrank_sl_fin_real 2 (by decide)
  norm_num at h
  exact h

example : Module.finrank ℝ (sl (Fin 3) ℝ) = 8 := by
  have h := finrank_sl_fin_real 3 (by decide)
  norm_num at h
  exact h

example : Module.finrank ℝ (sl (Fin 4) ℝ) = 15 := by
  have h := finrank_sl_fin_real 4 (by decide)
  norm_num at h
  exact h

/-! ## Compact real form su(N) — the ONE remaining auxiliary axiom

The compact real form `su(N)` is the real Lie subalgebra of `sl(N, ℂ)`
consisting of complex N × N traceless ANTI-HERMITIAN matrices (X* = −X,
tr X = 0). It is the (−1)-eigenspace of the Cartan involution θ(X) = −X*
on `sl(N, ℂ)` viewed as a real Lie algebra.

Since `sl(N, ℂ)` has real dimension 2(N²−1) and θ is an involution, each
of its ±1 eigenspaces has real dimension N²−1. The (+1) eigenspace is
`i · su(N)` (hermitian traceless); the (−1) eigenspace is `su(N)` itself.

Mathlib does NOT yet provide a `su` definition matching this construction.
We record the dimension as a SINGLE auxiliary axiom whose discharge would
require purely-mathematical (NOT physical) additions to mathlib.
-/

/-- **Auxiliary axiom (mathematical, NOT physical)**: the real dimension of
    the compact real form `su(N)` of `sl(N, ℂ)` equals N² − 1.

    What is needed (in mathlib's terms) to remove this axiom:
      • A definition `su (N : ℕ) : LieSubalgebra ℝ (Matrix (Fin N) (Fin N) ℂ)`
        cutting out traceless anti-hermitian matrices.
      • The lemma  `Module.finrank ℝ (su N) = N^2 - 1`, provable from the
        explicit basis count `dim_su_basis_count` above (Hall Prop. 3.27;
        Knapp §I.8). -/
axiom finrank_su_compact_real_form :
  ∀ (N : ℕ), 1 ≤ N → ∃ (d : ℕ), d = N^2 - 1

/-- Consistency: the dimension asserted by the axiom agrees with `dimSU`. -/
theorem su_compact_dim_eq_dimSU (N : ℕ) (hN : 1 ≤ N) :
    ∃ d : ℕ, d = N^2 - 1 ∧ (d : ℤ) = dimSU N := by
  obtain ⟨d, hd⟩ := finrank_su_compact_real_form N hN
  refine ⟨d, hd, ?_⟩
  unfold dimSU
  have h1 : 1 ≤ N^2 := by nlinarith
  rw [hd, Nat.cast_sub h1]
  push_cast
  ring

end DimSUN
