/-!
  # Crossed Cosmos — BasicMathlib (Lean 4 + Mathlib)

  Mathlib-backed counterparts of the Rat-level theorems already PROVED
  in `Crossed/Basic.lean` via `native_decide`. Here we re-prove the same
  numerical identities (ξ* = 2/3, c_DW = 9/10, F(N=3) = 1, F(N=2) = 9/8,
  etc.) using mathlib's `norm_num` decision procedure, which is the
  idiomatic mathlib4 tactic for rational arithmetic.

  Why two parallel files :
  * `Basic.lean` (no mathlib) uses `native_decide`, which compiles a
    decision procedure to native code and is the official trusted
    fallback for kernel-verified `Rat` numerics. Build is fast, no
    external deps.
  * `BasicMathlib.lean` (this file) imports mathlib's `norm_num` extension
    and uses it for the same statements, demonstrating that the Crossed
    Cosmos numerical identities hold in the mathlib-native `ℚ` (which
    coincides with core `Rat`).

  Equivalence claim. Lean's core `Rat` IS the mathlib `ℚ`: mathlib4
  provides instances `Field ℚ`, `LinearOrderedField ℚ` for the core
  `Rat` type rather than redefining it. Hence every theorem
  proved with `native_decide` on `Rat` is *definitionally* the same
  statement as the corresponding `norm_num` proof on `ℚ`.

  Session : 2026-05-20 step 3 (continuation).
  Toolchain : Lean 4.29.1 + mathlib v4.29.1 (pinned in lakefile.toml).
-/

import Mathlib.Tactic.NormNum
import Mathlib.Data.Rat.Defs

namespace Crossed

/-! ## §1. ξ* = 2/3 via norm_num -/

/-- **ξ* = 2/3** proved using mathlib's `norm_num`. Companion to
`Crossed.xi_star_eq_two_thirds` from `Basic.lean` (proved by
`native_decide`). Both statements are about the same `ℚ`. -/
theorem xi_star_eq_two_thirds_mathlib :
    (1 : ℚ) / (1 + 1 / 2) = 2 / 3 := by
  norm_num

/-- Reciprocal form: `1 / (3/2) = 2/3`. -/
theorem inv_three_halves_mathlib :
    (1 : ℚ) / (3 / 2) = 2 / 3 := by
  norm_num

/-- `1 + 1/2 = 3/2`. -/
theorem one_plus_half_mathlib :
    (1 : ℚ) + 1 / 2 = 3 / 2 := by
  norm_num

/-! ## §2. c_DW = 9/10 via norm_num -/

/-- **c_DW = 9/10** proved using mathlib's `norm_num`. Companion to
`Crossed.c_DW_eq_nine_tenths` from `Basic.lean`. -/
theorem c_DW_eq_nine_tenths_mathlib :
    (9 : ℚ) / (9 + 1) = 9 / 10 := by
  norm_num

/-! ## §3. F(N) DW formula at N = 2, N = 3 via norm_num -/

/-- **F(N=3) = 1** via `norm_num`: `(9/10) · (3² + 1)/3² = 1`. -/
theorem c_DW_FN_three_mathlib :
    (9 / 10 : ℚ) * ((3^2 + 1) / 3^2) = 1 := by
  norm_num

/-- **F(N=2) = 9/8** via `norm_num`: `(9/10) · (2² + 1)/2² = 9/8`. -/
theorem c_DW_FN_two_mathlib :
    (9 / 10 : ℚ) * ((2^2 + 1) / 2^2) = 9 / 8 := by
  norm_num

/-- **F(N=4) = 17·9/(10·16) = 153/160** via `norm_num`. -/
theorem c_DW_FN_four_mathlib :
    (9 / 10 : ℚ) * ((4^2 + 1) / 4^2) = 153 / 160 := by
  norm_num

/-- **F(N=5) = 234/250 = 117/125** via `norm_num`. -/
theorem c_DW_FN_five_mathlib :
    (9 / 10 : ℚ) * ((5^2 + 1) / 5^2) = 117 / 125 := by
  norm_num

/-! ## §4. Cross-check: native_decide and norm_num agree

These should be definitionally trivial since `(ℚ : Type) = (Rat : Type)`
in Lean 4 + mathlib (mathlib's `ℚ` is core `Rat`, with mathlib supplying
the algebraic structure instances). We record this as a sanity-check
identity. The two right-hand sides are by definition the same value. -/

/-- Sanity: the `ℚ`-value `2/3` is the same as the `Rat`-value `2/3`. -/
theorem rat_two_thirds_unique : (2 / 3 : ℚ) = (2 / 3 : Rat) := rfl

/-- Sanity: the `ℚ`-value `9/10` matches the `Rat`-value `9/10`. -/
theorem rat_nine_tenths_unique : (9 / 10 : ℚ) = (9 / 10 : Rat) := rfl

/-! ## §5. Lifted Nat identities (using `Nat.log` from mathlib)

Mathlib defines `Nat.log b n` (general base-`b` log) extending the
core `Nat.log2`. The values agree on powers of `2`. -/

/-- `Nat.log 2 4 = 2` via mathlib's `Nat.log`. Concrete kernel
reduction by `decide` (`Nat.log` is computable). -/
theorem nat_log_two_four_mathlib : Nat.log 2 4 = 2 := by
  decide

/-- `Nat.log 2 8 = 3`. -/
theorem nat_log_two_eight_mathlib : Nat.log 2 8 = 3 := by
  decide

/-- `Nat.log 2 16 = 4`. -/
theorem nat_log_two_sixteen_mathlib : Nat.log 2 16 = 4 := by
  decide

/-- `Nat.log 2 32 = 5`. -/
theorem nat_log_two_thirtytwo_mathlib : Nat.log 2 32 = 5 := by
  decide

/-! ## §6. Bridge: `Nat.log2` (core) and `Nat.log 2` (mathlib) agree on
    powers of 2.

Mathlib provides the lemma `Nat.log_eq_log2` (or similar) but the
agreement on concrete values is decidable. -/

/-- `Nat.log2 4 = Nat.log 2 4` (both reduce to 2). -/
theorem log2_eq_log_two_four : Nat.log2 4 = Nat.log 2 4 := by
  decide

/-- `Nat.log2 16 = Nat.log 2 16` (both reduce to 4). -/
theorem log2_eq_log_two_sixteen : Nat.log2 16 = Nat.log 2 16 := by
  decide

end Crossed
