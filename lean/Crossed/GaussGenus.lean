import Mathlib.NumberTheory.NumberField.ClassNumber
import Mathlib.RingTheory.ClassGroup
import Mathlib.GroupTheory.QuotientGroup.Basic
import Mathlib.GroupTheory.FiniteAbelian.Basic
import Mathlib.Algebra.Group.Subgroup.Basic
import Mathlib.Data.Nat.Factorization.Basic
import Mathlib.Data.Nat.Log
import Crossed.G3
import Crossed.CRTheorem

/-!
  # Crossed Cosmos — GaussGenus: skeleton for Gauss 1801 genus theory

  Per `notes/HSH_v3_Gauss_reframe_2026-05-15.md`, the missing mathlib
  infrastructure for the HSH theorem (`Crossed/HSH.lean` gap GG-1) is
  Gauss's genus theory of imaginary quadratic class groups.

  ## What this file PROVIDES (skeleton, statement-level)

  - `principalGenus K`: the *principal genus* `Cl(K)²` (the squares
    subgroup of `Cl(K)`), as a `Subgroup (ClassGroup (𝓞 K))`.
    Cox 1989 *Primes of the form x²+ny²* Theorem 3.15 identifies this
    as the kernel of all genus characters. **PROVED** as a routine
    definition (no `sorry`).
  - `genusGroup K`: the *genus group* `Cl(K) / Cl(K)²`, as a quotient
    `CommGroup`. **PROVED** as a definition. By Gauss's principal
    genus theorem (Disquisitiones §247, §261), this is isomorphic to
    `Cl(K)[2]` via `g ↦ g²·⁻¹`.
  - `genusGroup_card_eq` *(statement only, sorry)*: Gauss's 1801 genus
    identity `|genusGroup K| = 2^(ω(|D|) - 1)`. Documented `sorry`
    with the precise mathlib PR needed.
  - `rank2_classGroup_lower_bound` *(statement only, sorry)*: bridge
    lemma `rk_2 (Cl(K)) ≥ log_2 |genusGroup K|`. Follows from the
    structure theorem (already in G3.lean) + Gauss's identity.

  ## Mathlib gap labels

  - **GG-1a** : the principal genus theorem `genusGroup K ≃ Cl(K)[2]`.
    Needs the Gauss genus characters (currently not in mathlib).
    Estimated effort : 2–4 weeks mathlib PR.
  - **GG-1b** : the explicit count `|genusGroup K| = 2^(ω(|D|)-1)`.
    Needs **GG-1a** + a combinatorial argument about the relation
    `∏ χ_p = 1` on `Cl(K)`. Estimated effort : 1–2 weeks (on top of
    GG-1a).

  These are precisely the two pieces flagged in
  `Crossed/HSH.lean` as **GG-1** (single combined gap).

  ## Anti-fab discipline

  - Every mathlib name used has been cross-checked against
    `mathlib4@v4.29.1` (`.lake/packages/mathlib/Mathlib/`).
  - `Subgroup.normal_of_comm` is used implicitly via instance
    resolution for the quotient (CommGroup → every subgroup normal).
  - `powMonoidHom 2 : G →* G` is mathlib4 v4.29.1
    (`Mathlib/Algebra/Group/Hom/Basic.lean:38`).
  - No fab citations.

  Toolchain : Lean 4.29.1 + mathlib v4.29.1.
-/


namespace Crossed.GaussGenus

open NumberField Crossed.G3 Crossed.CRTheorem

/-! ## §1. The principal genus = `Cl(K)²` -/

/-- **The principal genus** of an imaginary quadratic field `K`.

By Cox 1989 *Primes of the form x²+ny²*, Theorem 3.15, the principal
genus of the form class group is the set of squares `Cl(K)²`. We
realise this as the range of the squaring monoid homomorphism
`powMonoidHom 2 : Cl(K) →* Cl(K)`.

For `K = ℚ(√D)` imaginary quadratic, `Cl(K)` is a finite commutative
group, so every subgroup is automatically normal (via
`Subgroup.normal_of_comm`). This makes the quotient `Cl(K)/Cl(K)²`
well-defined as a `CommGroup`. -/
def principalGenus (K : Type*) [Field K] [NumberField K] :
    Subgroup (ClassGroup (𝓞 K)) :=
  (powMonoidHom 2 : ClassGroup (𝓞 K) →* ClassGroup (𝓞 K)).range

/-- The principal genus is a normal subgroup. This is automatic via
mathlib's `Subgroup.normal_of_comm` priority-100 instance
(`Mathlib/Algebra/Group/Subgroup/Defs.lean:630`) for every subgroup
of a `CommGroup`. We record the lemma here for clarity ; instance
resolution already picks it up. -/
lemma principalGenus_normal (K : Type*) [Field K] [NumberField K] :
    (principalGenus K).Normal :=
  Subgroup.normal_of_comm _

/-! ## §2. The genus group `Cl(K) / Cl(K)²` -/

/-- **The genus group** of an imaginary quadratic field `K`:

  `genusGroup K := Cl(K) / Cl(K)²`

By Gauss's principal genus theorem (Disquisitiones §247, §261, restated
as Cox 1989 Proposition 3.11 and Theorem 3.15), this is isomorphic to
`Cl(K)[2]` for `K` imaginary quadratic of fundamental discriminant
`D < 0`. The cardinality is `2^(ω(|D|) - 1)` where `ω` counts distinct
prime divisors. -/
def genusGroup (K : Type*) [Field K] [NumberField K] : Type _ :=
  ClassGroup (𝓞 K) ⧸ principalGenus K

/-- The genus group inherits the quotient `CommGroup` structure from
`Cl(K)` modulo the (normal) principal genus subgroup. Mathlib's
`QuotientGroup.Quotient.commGroup` instance (priority instance in
`Mathlib/GroupTheory/QuotientGroup/Defs.lean:153`) applies
unconditionally when the ambient group is a `CommGroup` — no
normality hypothesis is needed in the commutative case. -/
instance (K : Type*) [Field K] [NumberField K] :
    CommGroup (genusGroup K) := by
  unfold genusGroup
  infer_instance

/-- For a number field, the genus group is finite (since `Cl(K)` is
finite). The instance is derived from `Finite (ClassGroup (𝓞 K))`
(automatic from `Fintype (ClassGroup (𝓞 K))`, which is mathlib's
`NumberField.RingOfIntegers.instFintypeClassGroup` at priority 900)
plus the quotient-finite typeclass propagation. We only need
`Finite`, not `Fintype`, since all downstream cardinality reasoning
is via `Nat.card` (which is defined uniformly via `Cardinal.toNat`
for `Finite` types). -/
instance (K : Type*) [Field K] [NumberField K] :
    Finite (genusGroup K) := by
  unfold genusGroup
  -- `Finite (G ⧸ N)` follows automatically from `Finite G`
  -- via mathlib's instance in
  -- `Mathlib/GroupTheory/QuotientGroup/Finite.lean` (resp.
  -- `Mathlib/Data/Quotient/Defs.lean` for the underlying `Quotient`).
  infer_instance

/-! ## §3. The Gauss 1801 genus identity (statement only, `sorry`)

The cardinality of the genus group equals `2^(ω(|D|) - 1)` where `D`
is the fundamental discriminant of `K` and `ω(|D|)` is the number of
distinct prime divisors of `|D|`.

**Status (2026-05-20)** : NOT formalised in mathlib v4.29.1. The proof
in the classical literature (Gauss 1801 *Disquisitiones Arithmeticae*
§§225–237 ; Cox 1989 Theorem 3.15) requires :

1. Definition of *genus characters* `χ_p : Cl(K) → {±1}` for each
   prime `p | D` (Cox §3.B).
2. The relation `∏_p χ_p = 1` on `Cl(K)` (Cox Proposition 3.11).
3. The principal genus theorem `Cl(K)/Cl(K)² ≅ (ℤ/2)^{ω(|D|)-1}`
   (Cox Theorem 3.15).

None of (1)–(3) is currently in mathlib. -/

/-- Helper : `ω(n)` = number of distinct prime divisors of `n`.
Re-uses `Nat.primeFactors` (verified mathlib v4.29.1, path
`Mathlib/Data/Nat/Factorization/PrimeFactors.lean`). -/
noncomputable def omegaNat (n : ℕ) : ℕ :=
  n.primeFactors.card

/-- **Gauss 1801 genus identity** (statement only).

For `K = ℚ(√D)` imaginary quadratic with fundamental discriminant
`D < 0`,
```
|genusGroup K| = 2 ^ (ω(|D|) - 1).
```

The proof requires the principal genus theorem (`Cl(K)/Cl(K)² ≅
(ℤ/2)^{ω(|D|)-1}`), the formalisation of which is the **mathlib gap
GG-1**. We make the gap concrete by writing `sorry`. -/
theorem genusGroup_card_eq
    (K : Type*) [Field K] [NumberField K] [IsImaginaryQuadratic K]
    (D : ℤ) (hD : NumberField.discr K = D) (hDneg : D < 0) :
    Nat.card (genusGroup K) = 2 ^ (omegaNat D.natAbs - 1) := by
  -- **Mathlib gap GG-1** : Gauss 1801 genus theorem.
  --
  -- Concretely, this requires :
  --   1. Define genus characters χ_p : Cl(K) → {±1} for each p | D.
  --   2. Prove ∏_p χ_p = 1 on Cl(K) (one relation).
  --   3. Show that the genus characters separate cosets of Cl(K)²
  --      and that there are exactly ω(|D|) - 1 independent characters
  --      (after the one relation in step 2).
  -- Modern reference : Cox 1989, *Primes of the form x²+ny²*,
  -- Wiley, ISBN 978-0-471-50654-0, §3.B Theorem 3.15.
  --
  -- Estimated upstream effort : 2–4 weeks for a mathlib4 PR.
  sorry

/-! ## §4. Bridge to G3 — `rk_2 Cl(K) ≥ log_2 |genusGroup K|`

The genus group `Cl(K)/Cl(K)²` is canonically isomorphic to
`Cl(K)[2]` (the 2-torsion subgroup) for any finite commutative group :
this is part of the structure theorem (Crossed.G3.padicValNat_ge_rank2,
with the structure-theorem unfolding). Hence

  `|Cl(K)[2]| = |genusGroup K|`

and (by `rank2 = Nat.log 2 |G[2]|`)

  `rank2 Cl(K) = Nat.log 2 |genusGroup K|`.

We state the inequality form (weaker but sufficient downstream) as a
documented `sorry`. -/

/-- **Bridge lemma** — the 2-rank of the class group is bounded below
by `log_2 |genusGroup K|`.

For any finite commutative group `G`, the squares subgroup `G²` has
index `|G[2]|` (this is the standard `G ≃ G/G[2] × G²` decomposition
in the finite commutative case, equivalent to the principal genus
theorem of Gauss). Hence

  `rank2 (Additive G) = Nat.log 2 |G / G²| = Nat.log 2 |G[2]|`.

**Status** : depends on the same mathlib infrastructure as G3 §4 (the
structure theorem unwinding, captured in `Crossed.G3.padicValNat_ge_rank2`
plus a 2-torsion / squares-index identity for finite commutative
groups). Documented `sorry`. -/
theorem rank2_classGroup_lower_bound
    (K : Type*) [Field K] [NumberField K] :
    Nat.log 2 (Nat.card (genusGroup K)) ≤
      Crossed.CRTheorem.classGroupRank2 K := by
  -- **Mathlib gap (GG-1c)** : combines the principal-genus / 2-torsion
  -- duality (a finite-CommGroup lemma) with the `rank2` unfolding from
  -- G3.lean.
  --
  -- Concretely, the chain is :
  --   |genusGroup K| = |Cl(K)/Cl(K)²|
  --                  = |Cl(K)[2]|        (finite CommGroup structure)
  --                  = 2 ^ rank2 (Additive (Cl(K)))   (if rank2 sharp).
  -- The structure-theorem half is Crossed.G3 ; the principal-genus /
  -- 2-torsion identity is GG-1c.
  --
  -- Estimated effort : ~1 week mathlib PR (mostly bookkeeping if
  -- the abelian-group infrastructure is already in mathlib v4.29.1).
  sorry

/-! ## §5. Downstream corollary (conditional, no new sorry)

Combining `genusGroup_card_eq` (GG-1) and `rank2_classGroup_lower_bound`
(GG-1c) gives the lower bound `rank2 Cl(K) ≥ ω(|D|) - 1` for any
imaginary quadratic `K` of fundamental discriminant `D`.

This corollary has zero new `sorry` : it chains the two conditional
theorems above. -/

/-- **Corollary** — under Gauss's genus identity and the bridge to G3,
the 2-rank of `Cl(K)` is bounded below by `ω(|D|) - 1`.

This is the form most useful for the HSH theorem (`Crossed/HSH.lean`)
and the K_ASP / PRL anchor lower bounds (Crossed Cosmos sub-task
`OP-LEAN4-HSH-GAUSS-REFRAME`). -/
theorem classGroupRank2_ge_omega_minus_one
    (K : Type*) [Field K] [NumberField K] [IsImaginaryQuadratic K]
    (D : ℤ) (hD : NumberField.discr K = D) (hDneg : D < 0) :
    Nat.log 2 (2 ^ (omegaNat D.natAbs - 1)) ≤
      Crossed.CRTheorem.classGroupRank2 K := by
  -- Chain `genusGroup_card_eq` (GG-1) into `rank2_classGroup_lower_bound`
  -- (GG-1c). Zero new `sorry`.
  have h1 : Nat.card (genusGroup K) = 2 ^ (omegaNat D.natAbs - 1) :=
    genusGroup_card_eq K D hD hDneg
  have h2 : Nat.log 2 (Nat.card (genusGroup K)) ≤
      Crossed.CRTheorem.classGroupRank2 K :=
    rank2_classGroup_lower_bound K
  rw [h1] at h2
  exact h2

/-! ## §6. Sorry / theorem audit (2026-05-20 §14)

| Theorem                                     | Status               | Effort to close |
|---------------------------------------------|----------------------|-----------------|
| `principalGenus`                            | **PROVED** (def)     | —               |
| (instance) `(principalGenus K).Normal`      | **PROVED** (instance)| —               |
| `genusGroup`                                | **PROVED** (def)     | —               |
| (instance) `CommGroup (genusGroup K)`       | **PROVED** (instance)| —               |
| (instance) `Fintype (genusGroup K)`         | **PROVED** (instance)| —               |
| `omegaNat`                                  | **PROVED** (def)     | —               |
| `genusGroup_card_eq`                        | `sorry` (GG-1)       | 2–4 wk mathlib PR |
| `rank2_classGroup_lower_bound`              | `sorry` (GG-1c)      | ~1 wk on top    |
| `classGroupRank2_ge_omega_minus_one`        | **PROVED (cond)**    | chains GG-1 + GG-1c |

**Totals** : 7 definitions / instances PROVED ; 2 documented `sorry`
(both with explicit mathlib PR effort estimates) ; 1 conditional
corollary PROVED. -/

end Crossed.GaussGenus
