/-!
  # Crossed Cosmos — Basic theorems (Lean 4, no mathlib)

  First fully-PROVED theorems for the Crossed Cosmos formalization
  program. These are intentionally simple identities that underpin the
  larger theorems (CR', M142, F(N), xi_star). Closing them in Lean 4
  establishes the project's first non-`sorry` lemmas.

  Session : 2026-05-20
  Toolchain : Lean 4.29.1, no external dependencies (core Lean only).
-/

namespace Crossed

/-! ## §1. ξ* fixed-point Nat identities

The Crossed Cosmos universal Cosmological Ratio fixed point ξ* = 2/3
reduces algebraically to identities on numerators and denominators.
For a "ξ* = 2/3" rational identity over ℚ we'd need mathlib's `norm_num`,
so here we close the underlying ℕ identities that any subsequent
mathlib-based proof of `ξ* = 2/3` will need.

  ξ*    = 1 / (1 + 1/2)
        = 1 / (3/2)
        = 2 / 3

Key ℕ facts : (i) 2 + 1 = 3, (ii) 1 · 2 = 2, (iii) 1 · 3 = 3.
-/

/-- The denominator identity for `ξ* = 2/3`: `1 + 1/2 = 3/2`. In ℕ-form:
the common denominator yields `2 + 1 = 3`. Pure closed-form ℕ. -/
theorem xi_star_denominator : (2 : Nat) + 1 = 3 := by
  decide

/-- The numerator identity for `ξ* = 2/3` after cross-multiplication:
the reciprocal of `3/2` is `2/3`, so `1 · 2 = 2` (numerator) and
`1 · 3 = 3` (denominator). Pure closed-form ℕ. -/
theorem xi_star_numerator : (1 : Nat) * 2 = 2 ∧ (1 : Nat) * 3 = 3 := by
  decide

/-! ## §2. Dijkgraaf–Witten c = 9/10 (genus expansion ratio)

't Hooft genus expansion gives `Z_0 / (Z_0 + Z_1) = 9 / (9 + 1) = 9/10`.
The underlying ℕ identity `9 + 1 = 10` is the load-bearing fact. -/

/-- Denominator identity for the Dijkgraaf–Witten genus-expansion ratio
`9 / (9 + 1) = 9 / 10`: namely `9 + 1 = 10`. -/
theorem c_DW_denominator : (9 : Nat) + 1 = 10 := by
  decide

/-! ## §3. F(N) ratio identity (concrete instance)

The genus-expansion combination `(9/10) · (N²+1)/N²` for `N = 2` (the
smallest interesting case) equals `45/40 = 9/8`. We verify the integer
identity `9 · (4 + 1) = 45` and `10 · 4 = 40` and `45 / 5 = 9`, `40 / 5 = 8`. -/

/-- Numerator identity for `F(N=2)` ratio: `9 · (2² + 1) = 45`. -/
theorem FN_two_numerator : (9 : Nat) * (2 ^ 2 + 1) = 45 := by
  decide

/-- Denominator identity for `F(N=2)` ratio: `10 · 2² = 40`. -/
theorem FN_two_denominator : (10 : Nat) * 2 ^ 2 = 40 := by
  decide

/-- The reduced form of `F(N=2)`: `45 / gcd(45,40) = 9` and
`40 / gcd(45,40) = 8`. We verify the gcd is 5. -/
theorem FN_two_gcd : Nat.gcd 45 40 = 5 := by
  decide

/-! ## §4. 3-adic split rule (negative direction)

If `D ≡ 2 (mod 3)` then `3 ∤ D`. Pure integer arithmetic, omega-closable. -/

/-- Negative side of the 3-adic anchor split: `D % 3 = 2` precludes
`3 ∣ D`. -/
theorem three_adic_split (D : Int) (hD : D % 3 = 2) :
    ¬ (3 : Int) ∣ D := by
  intro h
  obtain ⟨k, hk⟩ := h
  -- `D = 3 * k`, so `D % 3 = 0`. Combined with `hD : D % 3 = 2`, omega closes.
  subst hk
  omega

/-! ## §5. `Nat.log 2 4 = 2` building block

Used in `CR_prime_N4` of the Theorem CR' formalisation. The underlying
closed-form fact is `2 ^ 2 = 4`. -/

/-- The closed-form identity `2 ^ 2 = 4`, which is the witness for
`Nat.log 2 4 = 2` (i.e. `2^2 ≤ 4 < 2^3`). -/
theorem two_pow_two_eq_four : (2 : Nat) ^ 2 = 4 := by
  decide

/-- The upper-bound witness for `Nat.log 2 4 = 2`: `4 < 2 ^ 3 = 8`. -/
theorem four_lt_two_pow_three : (4 : Nat) < 2 ^ 3 := by
  decide

/-! ## §6. Sanity check : composed identity

A non-trivial combination demonstrating the closed-form proofs above
chain together cleanly. -/

/-- Composition: `(2 + 1) = 3` AND `9 + 1 = 10` AND `2 ^ 2 = 4` simultaneously,
showing the proof toolkit (`decide`) extends to conjunctions of arithmetic
facts. -/
theorem chained_identities :
    (2 : Nat) + 1 = 3 ∧ (9 : Nat) + 1 = 10 ∧ (2 : Nat) ^ 2 = 4 := by
  decide

end Crossed
