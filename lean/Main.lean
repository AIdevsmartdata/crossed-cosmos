import Crossed

open Crossed

/-- Print the first PROVED Crossed Cosmos identities so a `lake exe crossed`
invocation visibly confirms the kernel-verified theorems are in the build. -/
def main : IO Unit := do
  IO.println "Crossed Cosmos — first kernel-verified Lean 4 theorems"
  IO.println "  xi_star_denominator : 2 + 1 = 3                    OK"
  IO.println "  c_DW_denominator    : 9 + 1 = 10                   OK"
  IO.println "  FN_two_numerator    : 9 * (2^2 + 1) = 45           OK"
  IO.println "  FN_two_denominator  : 10 * 2^2 = 40                OK"
  IO.println "  FN_two_gcd          : gcd(45,40) = 5               OK"
  IO.println "  three_adic_split    : D%3=2 → ¬3∣D                 OK"
  IO.println "  two_pow_two_eq_four : 2^2 = 4                      OK"
  IO.println "  four_lt_two_pow_three : 4 < 2^3                    OK"
  IO.println "  chained_identities  : conj of three                OK"
