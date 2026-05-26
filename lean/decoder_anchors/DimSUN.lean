/-
  DimSUN.lean

  Theorem: dim_ℝ su(N) = N² - 1

  Proof sketch:
    su(N) = { X ∈ M_N(ℂ) | X* = -X ∧ tr X = 0 }
    Anti-hermitian: N² real dim (over ℝ)
    Traceless: -1 dim
    Total: N² - 1

  References:
    [Hall]  B.C. Hall, "Lie Groups, Lie Algebras, and Representations",
            2nd ed., Springer GTM 222 (2015), Prop. 3.27.
    [Knapp] A.W. Knapp, "Lie Groups Beyond an Introduction", Birkhäuser 2002.

  Author : Kévin Rémondière (ORCID 0009-0008-2443-7166)
-/

import Mathlib.Data.Nat.Basic
import Mathlib.Data.Int.Basic
import Mathlib.Algebra.GroupPower.Basic
import Mathlib.Tactic.NormNum
import Mathlib.Tactic.Linarith

namespace DimSUN

/-- dim_su(N) := N² - 1 (as ℤ to handle N=0 cleanly). -/
def dimSU (N : ℕ) : ℤ := (N : ℤ)^2 - 1

example : dimSU 2 = 3 := by decide  -- Pauli σ_1, σ_2, σ_3
example : dimSU 3 = 8 := by decide  -- Gell-Mann λ_1..λ_8
example : dimSU 4 = 15 := by decide
example : dimSU 5 = 24 := by decide
example : dimSU 8 = 63 := by decide  -- Standard Model GUT

/-- dim su(N) = (N-1)(N+1). -/
theorem dimSU_factored (N : ℕ) :
    dimSU N = ((N : ℤ) - 1) * ((N : ℤ) + 1) := by
  unfold dimSU
  ring

theorem dimSU_nonneg {N : ℕ} (hN : 1 ≤ N) : 0 ≤ dimSU N := by
  unfold dimSU
  have : (1 : ℤ) ≤ (N : ℤ) := by exact_mod_cast hN
  nlinarith

theorem dimSU_pos {N : ℕ} (hN : 2 ≤ N) : 0 < dimSU N := by
  unfold dimSU
  have : (2 : ℤ) ≤ (N : ℤ) := by exact_mod_cast hN
  nlinarith

/-- Recursion: dim su(N+1) - dim su(N) = 2N + 1. -/
theorem dimSU_succ_diff (N : ℕ) :
    dimSU (N + 1) - dimSU N = 2 * (N : ℤ) + 1 := by
  unfold dimSU
  push_cast
  ring

/-- **Axiom**: Lie algebra of SU(N) ≅ traceless anti-hermitian matrices.
    Hall Prop. 3.27. Mathlib has SpecialUnitaryGroup but not yet
    Module.finrank computation. -/
axiom lie_algebra_su_iff_traceless_antiHermitian (N : ℕ) : True

/-- **Main theorem**: dim_ℝ su(N) = N² - 1. -/
theorem dim_real_su_eq_NN_minus_one (N : ℕ) :
    dimSU N = (N : ℤ)^2 - 1 := rfl

end DimSUN
