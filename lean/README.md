# Crossed Cosmos — Lean 4 formalization

**Toolchain** : Lean 4.29.1 + lake 5.0.0 (`leanprover/lean4:v4.29.1`).
**Status** : first PROVED theorems landed 2026-05-20 (no mathlib dependency).

## Build

```bash
cd /root/cc-private/lean
lake build              # build library + executable
lake exe crossed        # run the demo executable
```

## Layout

- `lakefile.toml` — Lake project (library `Crossed`, executable `crossed`).
- `lean-toolchain` — pinned to `leanprover/lean4:v4.29.1`.
- `Crossed.lean` — library root (imports `Crossed.Basic`).
- `Crossed/Basic.lean` — **9 PROVED theorems, 0 sorry**.
- `Main.lean` — demo executable that prints the verified identities.
- `EciM142.lean` — STUB for M142 (`α₂ = 1/12` for LMFDB 4.5.b.a). NOT in
  the Lake build yet (requires mathlib + heavy CM-modular-form theory).
  6 `sorry`s remain.

## First PROVED theorems (`Crossed/Basic.lean`)

All closed by `decide` or `omega` — no axioms, no `sorry`, kernel-checked.

| Theorem                  | Statement                                  | Tactic   |
|--------------------------|--------------------------------------------|----------|
| `xi_star_denominator`    | `(2 : ℕ) + 1 = 3`                          | `decide` |
| `xi_star_numerator`      | `1 * 2 = 2 ∧ 1 * 3 = 3`                    | `decide` |
| `c_DW_denominator`       | `(9 : ℕ) + 1 = 10`                         | `decide` |
| `FN_two_numerator`       | `9 * (2² + 1) = 45`                        | `decide` |
| `FN_two_denominator`     | `10 * 2² = 40`                             | `decide` |
| `FN_two_gcd`             | `Nat.gcd 45 40 = 5`                        | `decide` |
| `three_adic_split`       | `D % 3 = 2 → ¬ 3 ∣ D` (over ℤ)             | `omega`  |
| `two_pow_two_eq_four`    | `2 ^ 2 = 4`                                | `decide` |
| `four_lt_two_pow_three`  | `4 < 2 ^ 3`                                | `decide` |
| `chained_identities`     | conj of three                              | `decide` |

These are the algebraic substrates of the Crossed Cosmos universal
ratios `ξ* = 2/3`, `c_DW = 9/10`, the F(N) genus-expansion identity,
the 3-adic split rule, and the `Nat.log 2 4 = 2` building block used in
`CR_prime_N4` of the Theorem CR' formalisation.

## Next steps

1. Add mathlib dependency to lift the Nat identities into the actual
   ℚ statements (`(1 : ℚ) / (1 + 1/2) = 2/3`, `(9 : ℚ) / 10 = 9/10`,
   `Nat.log 2 4 = 2`, etc.). Adds ~30 min initial mathlib download.
2. Move `EciM142.lean` into the mathlib-enabled Lake project, then
   address the 6 remaining `sorry`s in order of decreasing tractability.
3. Bring in `CRtheorem.lean` + `CRtheorem_helpers.lean` from
   `/root/notes/lean/` (16 `sorry`s combined, 4 mathlib gaps documented).

See `/root/cc-private/notes/LEAN_FORMALIZATION_STATUS_2026-05-20.md`
for the full roadmap and DS V4 Pro dispatch report.
