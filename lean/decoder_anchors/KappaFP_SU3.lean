/-
  KappaFP_SU3.lean
  (renamed 2026-05-27 from KostantKappaFP.lean — see audit
   decoder_BRIDGES_REJECTED_2026-05-27: the "Kostant 1959" attribution for
   κ_FP = 1/(2|Φ⁺|) was project-internal and not in Kostant's paper.)

  Theorem: κ_FP(SU(3)) = 1/6 under the project convention

      κ_FP(N) := 1 / (2 · |Φ⁺(SU(N))|),     |Φ⁺(SU(N))| = N(N−1)/2.

  ## Provenance of κ_FP — explicit disclaimer

  The formula 1/(2|Φ⁺|) is a PROJECT CONVENTION arising in the Faddeev–Popov
  determinant analysis of the SU(N) Yang–Mills measure (project's KR_FP_3
  / Mass-Gap papers). It is NOT a result of Kostant's 1959 paper, which
  discusses Betti numbers and principal sl₂-triples but does not define
  a constant 1/(2|Φ⁺|).

  The Weyl-group convention is DIFFERENT:

      κ_Weyl(N) := 1 / |W(SU(N))| = 1 / N!

  These two conventions COINCIDE only at N = 3:
        |Φ⁺(SU(3))| · 2 = 3 · 2 = 6 = 3! = |W(SU(3))|.

  They DIVERGE for all N ≥ 4 because |Φ⁺| grows polynomially while
  |W| = N! grows factorially:
        N = 4 :  2|Φ⁺| = 12 ,  N! = 24  →  κ_FP = 1/12 ≠ 1/24 = κ_Weyl.

  Both equalities (coincidence at N = 3, divergence at N = 4 and N = 5)
  are proved below as standalone Lean theorems, so the distinction is
  UNAMBIGUOUS in the formalisation. No Kostant attribution.

  References:
    [Bourbaki]    N. Bourbaki, Groupes et algèbres de Lie, Ch. IV–VI,
                  Plate I (root systems of classical types A_{N−1}).
    [Vassilevich] D.V. Vassilevich, "Heat kernel expansion: user's manual",
                  Phys. Rept. 388 (2003) 279, hep-th/0306138, Eq. 3.13.
    [Project]     KR_FP_3, Mass-Gap PRL v5 (Kevin Rémondière, 2026-05).

  Author : Kévin Rémondière (ORCID 0009-0008-2443-7166)
-/

import Mathlib.Data.Nat.Basic
import Mathlib.Data.Nat.Choose.Basic
import Mathlib.Data.Nat.Factorial.Basic
import Mathlib.Data.Rat.Defs
import Mathlib.Data.Rat.Order
import Mathlib.Algebra.Order.Ring.Defs
import Mathlib.Tactic.NormNum
import Mathlib.Tactic.Linarith

namespace KappaFP_SU3

/-! ## Number of positive roots of A_{N−1} = su(N) -/

/-- Number of positive roots of the root system A_{N−1} (= su(N)).
    For SU(N), |Φ⁺| = N(N−1)/2 (the binomial coefficient C(N, 2)).
    Reference: Bourbaki, Groupes et algèbres de Lie, Ch. VI, Planche I. -/
def numPositiveRoots (N : ℕ) : ℕ := N * (N - 1) / 2

example : numPositiveRoots 2 = 1  := by decide
example : numPositiveRoots 3 = 3  := by decide
example : numPositiveRoots 4 = 6  := by decide
example : numPositiveRoots 5 = 10 := by decide
example : numPositiveRoots 8 = 28 := by decide

/-- |Φ⁺(SU(N))| equals the binomial coefficient C(N, 2). -/
theorem numPositiveRoots_eq_choose (N : ℕ) :
    numPositiveRoots N = Nat.choose N 2 := by
  unfold numPositiveRoots
  rw [Nat.choose_two_right]

/-! ## Project convention: κ_FP(N) := 1/(2|Φ⁺(SU(N))|) -/

/-- The Faddeev–Popov κ constant for SU(N), in the project convention:
        κ_FP(N) := 1 / (2 · |Φ⁺(SU(N))|).

    For N ≥ 2 this equals 1 / (N(N−1)). For N = 1 the formula gives 1/0
    which the ℚ-conventions render as 0; this corner case is irrelevant. -/
noncomputable def kappaFP (N : ℕ) : ℚ :=
  1 / (2 * (numPositiveRoots N : ℚ))

/-- **Main theorem**: κ_FP(SU(3)) = 1/6. -/
theorem kappaFP_SU3 : kappaFP 3 = 1 / 6 := by
  unfold kappaFP numPositiveRoots
  norm_num

theorem kappaFP_SU2 : kappaFP 2 = 1 / 2 := by
  unfold kappaFP numPositiveRoots
  norm_num

theorem kappaFP_SU4 : kappaFP 4 = 1 / 12 := by
  unfold kappaFP numPositiveRoots
  norm_num

theorem kappaFP_SU5 : kappaFP 5 = 1 / 20 := by
  unfold kappaFP numPositiveRoots
  norm_num

theorem kappaFP_SU8 : kappaFP 8 = 1 / 56 := by
  unfold kappaFP numPositiveRoots
  norm_num

/-- Closed form for N ≥ 2: κ_FP(N) = 1 / (N · (N−1)). -/
theorem kappaFP_closed_form (N : ℕ) (hN : 2 ≤ N) :
    kappaFP N = 1 / ((N : ℚ) * ((N : ℚ) - 1)) := by
  unfold kappaFP numPositiveRoots
  have hN1 : 1 ≤ N := by omega
  -- 2 ∣ N(N-1) because one of N, N-1 is even.
  have h2div : 2 ∣ (N * (N - 1)) := by
    rcases Nat.even_or_odd N with hE | hO
    · obtain ⟨k, hk⟩ := hE
      refine ⟨k * (N - 1), ?_⟩; rw [hk]; ring
    · obtain ⟨k, hk⟩ := hO
      have hNk : N - 1 = 2 * k := by omega
      refine ⟨N * k, ?_⟩; rw [hNk]; ring
  -- Push the ℕ-division through the cast to ℚ.
  have hcast : ((N * (N - 1) / 2 : ℕ) : ℚ) = (N : ℚ) * ((N : ℚ) - 1) / 2 := by
    rw [Nat.cast_div h2div (by norm_num : (2 : ℚ) ≠ 0)]
    push_cast [Nat.cast_sub hN1]
    ring
  rw [hcast]
  -- Now simplify the 2's: 2 * (X / 2) = X.
  congr 1
  ring

/-- Positivity of κ_FP for N ≥ 2. -/
theorem kappaFP_pos (N : ℕ) (hN : 2 ≤ N) : 0 < kappaFP N := by
  rw [kappaFP_closed_form N hN]
  have hN_pos : (0 : ℚ) < (N : ℚ) := by exact_mod_cast (by omega : 0 < N)
  have hN_minus_1_pos : (0 : ℚ) < ((N : ℚ) - 1) := by
    have h1 : (1 : ℚ) ≤ (N : ℚ) := by exact_mod_cast (by omega : 1 ≤ N)
    linarith
  positivity

/-! ## Comparison to the Weyl-group convention κ_Weyl(N) := 1/N!

These conventions COINCIDE only at N = 3 by the numerical coincidence
      2 · |Φ⁺(SU(3))| = 2 · 3 = 6 = 3!
and DIVERGE for all N ≥ 4. -/

/-- The Weyl-group convention: κ_Weyl(N) := 1/N!. -/
noncomputable def kappaWeyl (N : ℕ) : ℚ := 1 / (Nat.factorial N : ℚ)

example : kappaWeyl 3 = 1 / 6  := by unfold kappaWeyl; norm_num [Nat.factorial]
example : kappaWeyl 4 = 1 / 24 := by unfold kappaWeyl; norm_num [Nat.factorial]

/-- **Coincidence theorem (N = 3)**: the two conventions agree. This is a
    purely numerical coincidence (2·|Φ⁺(SU(3))| = 6 = 3!). It does NOT
    generalise. -/
theorem kappaFP_3_equals_weyl : kappaFP 3 = kappaWeyl 3 := by
  rw [kappaFP_SU3]
  unfold kappaWeyl
  norm_num [Nat.factorial]

/-- **Divergence theorem (N = 4)**: the conventions disagree starting at N = 4.
    κ_FP(4) = 1/12, while κ_Weyl(4) = 1/24. -/
theorem kappaFP_diverges_from_weyl_for_N_eq_4 :
    kappaFP 4 ≠ kappaWeyl 4 := by
  rw [kappaFP_SU4]
  unfold kappaWeyl
  norm_num [Nat.factorial]

/-- **Divergence theorem (N = 5)**: also disagree at N = 5 (κ_FP = 1/20 vs
    κ_Weyl = 1/120). -/
theorem kappaFP_diverges_from_weyl_for_N_eq_5 :
    kappaFP 5 ≠ kappaWeyl 5 := by
  rw [kappaFP_SU5]
  unfold kappaWeyl
  norm_num [Nat.factorial]

/-- **Divergence theorem (N = 8)**: divergence persists at the SM/GUT scale.
    κ_FP(8) = 1/56, κ_Weyl(8) = 1/40320. -/
theorem kappaFP_diverges_from_weyl_for_N_eq_8 :
    kappaFP 8 ≠ kappaWeyl 8 := by
  rw [kappaFP_SU8]
  unfold kappaWeyl
  norm_num [Nat.factorial]

/-! ## Physics-bridge axiom (the link to the Seeley–DeWitt heat-kernel coefficient)

The geometric interpretation of κ_FP via the Seeley–DeWitt coefficient
a₂ = R/6 of the scalar Laplacian (Vassilevich Eq. 3.13) is a PHYSICS
statement requiring heat-kernel asymptotic-expansion machinery (Gilkey 1995,
BRST cohomology of Henneaux–Teitelboim 1992). None of this is in mathlib.

We do NOT pretend the project formula 1/(2|Φ⁺|) is derived from a₂ = R/6
inside Lean — that derivation is in the project's KR_FP_3 paper (informal).

We introduce an OPAQUE κ_FP-from-physics function and assert by axiom its
equality with the combinatorial `kappaFP`. This makes the bridge
non-vacuous: the opaque physics constant could a priori be anything; the
axiom fixes it to the combinatorial definition. -/

/-- Opaque κ_FP function as derived from the BRST/Seeley–DeWitt computation
    (NOT defined in Lean; the value is fixed only by the bridge axiom below). -/
opaque kappaFP_physical : ℕ → ℚ

/-- **Physics-bridge axiom** (UNPROVED in Lean, project-internal):

    For N ≥ 2, the BRST-derived Faddeev–Popov κ constant equals the
    combinatorial expression 1/(2|Φ⁺|).

    What needs to be added (and is NOT in mathlib) to discharge it:
      • Heat-kernel asymptotic expansion (Gilkey 1995).
      • BRST cohomology and the Faddeev–Popov determinant for SU(N) on a
        compact 4-manifold (Henneaux–Teitelboim 1992).
      • The actual computation that the BRST measure yields 1/(N(N−1)).

    The project's KR_FP_3 paper provides the informal derivation. -/
axiom kappaFP_physical_eq_combinatorial :
  ∀ (N : ℕ), 2 ≤ N → kappaFP_physical N = kappaFP N

/-- **Corollary**: the BRST-derived κ_FP at SU(3) equals 1/6. -/
theorem kappaFP_physical_SU3 : kappaFP_physical 3 = 1 / 6 := by
  rw [kappaFP_physical_eq_combinatorial 3 (by decide)]
  exact kappaFP_SU3

/-- **Corollary**: the BRST-derived κ_FP at SU(N) equals 1/(N(N−1)) for N ≥ 2. -/
theorem kappaFP_physical_closed_form (N : ℕ) (hN : 2 ≤ N) :
    kappaFP_physical N = 1 / ((N : ℚ) * ((N : ℚ) - 1)) := by
  rw [kappaFP_physical_eq_combinatorial N hN]
  exact kappaFP_closed_form N hN

end KappaFP_SU3
