import Mathlib

-- ===== ClayYM/Basic.lean (verbatim, sha256 049ed8173ebf03b4…, imports retirés) =====
section  -- enveloppe : borne la portée des 'open' (open scoped ContDiff définit la notation ω)
/-
ClayYM/Basic.lean
=================
Basic geometric objects for the Euclidean (Osterwalder–Schrader) statement:
Euclidean space-time `ℝ^d`, orthogonal group `O(d)`, time reflection `θ`,
configurations of `n` points, test functions with ordered positive times (the space `°S₊`
of Osterwalder–Schrader 1973), families of test functions (vectors of the pre-Hilbert space
of the OS reconstruction).

No hypothesis, no axiom, no `sorry` in this file: only concrete definitions built from
Mathlib.
-/

open scoped ContDiff
open MeasureTheory

noncomputable section

namespace ClayYM

/-- Euclidean space-time `ℝ^d` (Mathlib's ℓ² norm and inner product). -/
abbrev Spacetime (d : ℕ) : Type := EuclideanSpace ℝ (Fin d)

/-- The orthogonal group `O(d)`: bijective linear isometries of `ℝ^d`
(rotations AND reflections: the full group, not only `SO(d)`). -/
abbrev Orth (d : ℕ) : Type := Spacetime d ≃ₗᵢ[ℝ] Spacetime d

variable {d : ℕ}

/-- Euclidean time coordinate: the coordinate with index `0`. -/
def time [NeZero d] (x : Spacetime d) : ℝ := x 0

/-- Unit vector of the time direction. -/
def e₀ (d : ℕ) [NeZero d] : Spacetime d := EuclideanSpace.single 0 1

/-! ### Time reflection -/

/-- Sign of the time reflection on coordinate `i`: `-1` for time, `+1` otherwise. -/
def θsign [NeZero d] (i : Fin d) : ℝ := if i = 0 then -1 else 1

lemma θsign_mul_self [NeZero d] (i : Fin d) : θsign i * θsign i = 1 := by
  unfold θsign; split_ifs <;> norm_num

/-- Time reflection as the linear map `(t, x⃗) ↦ (-t, x⃗)`. -/
def θlin [NeZero d] : Spacetime d →ₗ[ℝ] Spacetime d where
  toFun x := WithLp.toLp 2 (fun i => θsign i * x i)
  map_add' x y := by
    ext i; simp [mul_add]
  map_smul' c x := by
    ext i; simp; ring

lemma θlin_apply [NeZero d] (x : Spacetime d) (i : Fin d) : θlin x i = θsign i * x i := rfl

lemma θlin_θlin [NeZero d] (x : Spacetime d) : θlin (θlin x) = x := by
  ext i; simp only [θlin_apply, ← mul_assoc, θsign_mul_self, one_mul]

lemma norm_θlin [NeZero d] (x : Spacetime d) : ‖θlin x‖ = ‖x‖ := by
  rw [EuclideanSpace.norm_eq, EuclideanSpace.norm_eq]
  congr 1
  refine Finset.sum_congr rfl (fun i _ => ?_)
  rw [θlin_apply, Real.norm_eq_abs, Real.norm_eq_abs, sq_abs, sq_abs, mul_pow]
  have : θsign i ^ 2 = 1 := by rw [sq]; exact θsign_mul_self i
  rw [this, one_mul]

/-- The time reflection `θ ∈ O(d)`. -/
def θ (d : ℕ) [NeZero d] : Orth d where
  toLinearEquiv :=
    { θlin with
      invFun := θlin
      left_inv := fun x => θlin_θlin x
      right_inv := fun x => θlin_θlin x }
  norm_map' := norm_θlin

lemma θ_apply [NeZero d] (x : Spacetime d) (i : Fin d) : θ d x i = θsign i * x i := rfl

lemma time_θ [NeZero d] (x : Spacetime d) : time (θ d x) = - time x := by
  simp [time, θ_apply, θsign]

/-! ### Configurations -/

/-- Configurations of `n` points of `ℝ^d`. -/
abbrev Config (d n : ℕ) : Type := Fin n → Spacetime d

/-- The `n` points are pairwise distinct (non-coincident configuration). -/
def NonCoincident {n : ℕ} (x : Config d n) : Prop := Function.Injective x

/-- Smallest distance between two distinct points (distinct indices) of a configuration;
equals `0` (Mathlib's convention `sInf ∅ = 0`) if `n ≤ 1`. -/
def minDist {n : ℕ} (x : Config d n) : ℝ :=
  ⨅ p : {p : Fin n × Fin n // p.1 ≠ p.2}, dist (x p.1.1) (x p.1.2)

/-- Region of strictly positive, strictly ordered times: `0 < t₁ < t₂ < … < tₙ`. -/
def OrderedPositive [NeZero d] (n : ℕ) : Set (Config d n) :=
  {x | (∀ k, 0 < time (x k)) ∧ StrictMono (fun k => time (x k))}

/-- Test functions of `°S₊`: smooth (`C^∞`, as opposed to analytic: we fix `∞ = ((⊤ : ℕ∞) : ℕ∞ω)`),
with compact support contained in the region of ordered positive times. -/
structure PosTest (d n : ℕ) [NeZero d] where
  toFun : Config d n → ℝ
  smooth : ContDiff ℝ ∞ toFun
  compact : HasCompactSupport toFun
  supp : tsupport toFun ⊆ OrderedPositive n

instance [NeZero d] {n : ℕ} : CoeFun (PosTest d n) (fun _ => Config d n → ℝ) :=
  ⟨PosTest.toFun⟩

/-! ### Lists of labelled points -/

/-- List of labelled points `(field index, point)`, the argument of the Schwinger functions. -/
abbrev LList (ι : Type) (d : ℕ) : Type := List (ι × Spacetime d)

/-- The list `[(i₀, x₀), …, (iₙ₋₁, xₙ₋₁)]`. -/
def mkList {ι : Type} {n : ℕ} (i : Fin n → ι) (x : Config d n) : LList ι d :=
  List.ofFn (fun k => (i k, x k))

/-- Pairwise distinct points in a labelled list. -/
def NonCoinc {ι : Type} (l : LList ι d) : Prop := (l.map Prod.snd).Nodup

/-- Translation of a labelled list by a vector `a`. -/
def shiftList {ι : Type} (a : Spacetime d) (l : LList ι d) : LList ι d :=
  l.map (fun p => (p.1, p.2 + a))

/-! ### Families of test functions (vectors of the OS reconstruction) -/

/-- A term `f(x₁,…,xₙ)` carrying the field indices `labels`. -/
structure Term (ι : Type) (d : ℕ) [NeZero d] where
  n : ℕ
  labels : Fin n → ι
  f : PosTest d n

/-- A finite family of terms (the finite sequence `(f₀, f₁, …)` of Osterwalder–Schrader). -/
abbrev Family (ι : Type) (d : ℕ) [NeZero d] : Type := List (Term ι d)

/-- The constant function `1` on the one-point space `Config d 0`: the vacuum vector. -/
def vacTest [NeZero d] : PosTest d 0 where
  toFun := fun _ => 1
  smooth := contDiff_const
  compact := by
    have : CompactSpace (Config d 0) := Finite.compactSpace
    exact HasCompactSupport.of_compactSpace _
  supp := by
    intro x _
    refine ⟨fun k => k.elim0, fun a _ _ => a.elim0⟩

/-- The vacuum term (no point, function `1`). -/
def vacTerm (ι : Type) [NeZero d] : Term ι d := ⟨0, Fin.elim0, vacTest⟩

/-- The vacuum family `Ω = (1, 0, 0, …)`. -/
def vac (ι : Type) [NeZero d] : Family ι d := [vacTerm ι]

end ClayYM

end  -- ferme le 'noncomputable section' de ClayYM/Basic.lean
end  -- ferme l'enveloppe

-- ===== ClayYM/OS.lean (verbatim, sha256 a89e78949376871a…, imports retirés) =====
section  -- enveloppe : borne la portée des 'open' (open scoped ContDiff définit la notation ω)
/-
ClayYM/OS.lean
==============
Euclidean quantum theory in the form of Schwinger KERNELS at non-coincident points,
and Osterwalder–Schrader axioms (OS 1973: E1–E4; OS 1975: linear growth condition E0').

Design choices (see STATEMENT.md, §3.1):
* The local gauge-invariant fields of YM₄ (canonical dimension ≥ 4 > d/2) are not random
  distributions (even `:φ²:` of the free field in dimension 4 has infinite variance):
  the framework "probability measure on S'(ℝ⁴)" (Glimm–Jaffe OS0–OS4) does not suit them.
  We therefore use the Schwinger functions of OS 1973, defined off the diagonals.
* For a reconstructible theory, these functions are real analytic off the diagonals;
  we handle them as functions (kernels) `S : list of (index, point) → ℝ`. The values at
  coincident points are arbitrary and enter no axiom.
* The fields have components (indices `ι`) on which `O(d)` acts through a given matrix
  representation `R` (for Yang–Mills: the rank-4 tensor representation).
-/

open scoped ContDiff BigOperators
open MeasureTheory Filter Topology

noncomputable section

namespace ClayYM

variable {ι : Type} {d : ℕ}

/-- Schwinger functions in kernel form: `S [(i₁,x₁), …, (iₙ,xₙ)]`. -/
abbrev Schwinger (ι : Type) (d : ℕ) : Type := LList ι d → ℝ

/-- Matrix representation of `O(d)` on the field components. -/
abbrev CompRep (ι : Type) (d : ℕ) : Type := Orth d → Matrix ι ι ℝ

/-! ### Reflection-positivity form -/

/-- Kernel of the reflection form between two terms `a` (reflected) and `b` (translated by `t`
in time): `Σ_j Π_k R(θ)_{i_{n-1-k}, j_k} · S((j, θ x_rev) ++ (labels_b, y + t e₀))`.
This is `S_{n+m}(Θ f* ⊗ τ_t g)` of OS 1973 written with kernels (Θf*(x₁…xₙ) = f(θxₙ,…,θx₁), real
functions), with the action of `θ` on the tensor components. -/
def rpKernel [Fintype ι] [NeZero d] (R : CompRep ι d) (S : Schwinger ι d) (a b : Term ι d)
    (t : ℝ) (x : Config d a.n) (y : Config d b.n) : ℝ :=
  ∑ j : Fin a.n → ι, (∏ k, R (θ d) (a.labels (Fin.rev k)) (j k)) *
    S (mkList j (fun k => θ d (x (Fin.rev k))) ++ mkList b.labels (fun k => y k + t • e₀ d))

/-- The Osterwalder–Schrader bilinear form `⟪F, τ_t G⟫ = Σ_{a∈F} Σ_{b∈G} ∫∫ f_a(x) g_b(y) K(x,y)`.
For `t = 0` it is the (pre-Hilbert) inner product of the reconstruction; `τ_t` acts there
as `e^{-tH}`. -/
def rpForm [Fintype ι] [NeZero d] (R : CompRep ι d) (S : Schwinger ι d)
    (F G : Family ι d) (t : ℝ) : ℝ :=
  (F.map fun a => (G.map fun b =>
      ∫ x, ∫ y, a.f x * b.f y * rpKernel R S a b t x y).sum).sum

/-! ### Osterwalder–Schrader axioms (kernel form) -/

/-- The Osterwalder–Schrader axioms for real Schwinger kernels:
* `normalized`            : `S(∅) = 1` (normalised vacuum);
* `smooth`                : E0 — `C^∞` regularity off the diagonals;
* `linear_growth`         : E0' (OS 1975) in the form of a sufficient pointwise bound, of order
                            linear in `n` and with at most factorial constants;
* `translation_invariant`, `rotation_covariant` : E1 — Euclidean covariance under the FULL
                            group `ℝ^d ⋊ O(d)` (reflections included);
* `symmetric`             : E3 — symmetry under permutations (Bose statistics, locality);
* `reflection_positive`   : E2 — reflection positivity;
* `cluster`               : E4 — cluster property (factorisation at large separation). -/
structure OSAxioms [Fintype ι] [NeZero d] (R : CompRep ι d) (S : Schwinger ι d) : Prop where
  normalized : S [] = 1
  smooth : ∀ (n : ℕ) (i : Fin n → ι),
    ContDiffOn ℝ ∞ (fun x : Config d n => S (mkList i x)) {x | NonCoincident x}
  linear_growth : ∃ α β c : ℝ, 0 < α ∧ 0 ≤ β ∧ 0 ≤ c ∧
    ∀ (n : ℕ) (i : Fin n → ι) (x : Config d n), NonCoincident x →
      |S (mkList i x)| ≤
        α * (n.factorial : ℝ) ^ β * ((1 + ∑ k, ‖x k‖) * (1 + (minDist x)⁻¹)) ^ (c * n)
  translation_invariant : ∀ (a : Spacetime d) (l : LList ι d), NonCoinc l →
    S (shiftList a l) = S l
  rotation_covariant : ∀ (g : Orth d) (n : ℕ) (i : Fin n → ι) (x : Config d n),
    NonCoincident x →
      S (mkList i (fun k => g (x k))) = ∑ j : Fin n → ι, (∏ k, R g (i k) (j k)) * S (mkList j x)
  symmetric : ∀ l l' : LList ι d, l.Perm l' → S l = S l'
  reflection_positive : ∀ F : Family ι d, 0 ≤ rpForm R S F F 0
  cluster : ∀ (l l' : LList ι d) (a : Spacetime d), NonCoinc l → NonCoinc l' →
    time a = 0 → a ≠ 0 →
      Tendsto (fun s : ℝ => S (l ++ shiftList (s • a) l')) atTop (𝓝 (S l * S l'))

end ClayYM

end  -- ferme le 'noncomputable section' de ClayYM/OS.lean
end  -- ferme l'enveloppe

-- ===== ClayYM/Gap.lean (verbatim, sha256 b7a879ea1aabd38b…, imports retirés) =====
section  -- enveloppe : borne la portée des 'open' (open scoped ContDiff définit la notation ω)
/-
ClayYM/Gap.lean
===============
Mass gap in Euclidean form, and finite mass.

Jaffe–Witten §4: "A quantum field theory has a mass gap Δ if H has no spectrum in the interval
(0, Δ) for some Δ > 0. The supremum of such Δ is the mass m, and we require m < ∞."

Euclidean form used (equivalent through the Osterwalder–Schrader reconstruction, where
`⟪F, τ_t G⟫ = ⟨F, e^{-tH} G⟩` and `Ω` is the class of the family `vac`):
  `|⟪F, τ_t G⟫ − ⟪F, Ω⟫⟪Ω, G⟫| ≤ e^{−Δ t} ‖F‖ ‖G‖`  for every `t ≥ 0` and all families `F, G`,
which is equivalent to `‖e^{−tH}(1 − P_Ω)‖ ≤ e^{−Δt}`, i.e. `spec(H) ⊂ {0} ∪ [Δ, ∞)` AND `ker H = ℂΩ`
(unique vacuum). This equivalence relies on the OS reconstruction theorem (not formalised here).
-/

open MeasureTheory Filter Topology

noncomputable section

namespace ClayYM

variable {ι : Type} {d : ℕ}

/-- `Δ` is a mass gap: exponential decay at rate `Δ` of all truncated correlations
(reflection form), uniformly over the families of test functions. -/
def HasMassGap [Fintype ι] [NeZero d] (R : CompRep ι d) (S : Schwinger ι d) (Δ : ℝ) : Prop :=
  0 < Δ ∧ ∀ (F G : Family ι d) (t : ℝ), 0 ≤ t →
    |rpForm R S F G t - rpForm R S F (vac ι) 0 * rpForm R S (vac ι) G 0| ≤
      Real.exp (-(Δ * t)) * Real.sqrt (rpForm R S F F 0) * Real.sqrt (rpForm R S G G 0)

/-- The mass `m = sup {Δ | Δ mass gap}` (equal to `0` by Mathlib's convention if the set is not
bounded above or is empty; used for documentation only). -/
def mass [Fintype ι] [NeZero d] (R : CompRep ι d) (S : Schwinger ι d) : ℝ :=
  sSup {Δ : ℝ | HasMassGap R S Δ}

/-- "we require m < ∞": the set of mass gaps is bounded above. -/
def FiniteMass [Fintype ι] [NeZero d] (R : CompRep ι d) (S : Schwinger ι d) : Prop :=
  BddAbove {Δ : ℝ | HasMassGap R S Δ}

/-- Mass gap in the Clay sense: some `Δ > 0` exists, and the mass is finite. -/
def ClayMassGap [Fintype ι] [NeZero d] (R : CompRep ι d) (S : Schwinger ι d) : Prop :=
  (∃ Δ, HasMassGap R S Δ) ∧ FiniteMass R S

/-- Consistency check: a smaller gap is still a gap (the set of gaps is an interval
`]0, m]` or `]0, m[`). -/
theorem HasMassGap.mono [Fintype ι] [NeZero d] {R : CompRep ι d} {S : Schwinger ι d}
    {Δ Δ' : ℝ} (h : HasMassGap R S Δ) (h0 : 0 < Δ') (hle : Δ' ≤ Δ) : HasMassGap R S Δ' := by
  refine ⟨h0, fun F G t ht => (h.2 F G t ht).trans ?_⟩
  have hexp : Real.exp (-(Δ * t)) ≤ Real.exp (-(Δ' * t)) := by
    apply Real.exp_le_exp.mpr
    have := mul_le_mul_of_nonneg_right hle ht
    linarith
  have hs : 0 ≤ Real.sqrt (rpForm R S F F 0) * Real.sqrt (rpForm R S G G 0) :=
    mul_nonneg (Real.sqrt_nonneg _) (Real.sqrt_nonneg _)
  calc Real.exp (-(Δ * t)) * Real.sqrt (rpForm R S F F 0) * Real.sqrt (rpForm R S G G 0)
      = Real.exp (-(Δ * t)) * (Real.sqrt (rpForm R S F F 0) * Real.sqrt (rpForm R S G G 0)) := by
        ring
    _ ≤ Real.exp (-(Δ' * t)) * (Real.sqrt (rpForm R S F F 0) * Real.sqrt (rpForm R S G G 0)) :=
        mul_le_mul_of_nonneg_right hexp hs
    _ = Real.exp (-(Δ' * t)) * Real.sqrt (rpForm R S F F 0) * Real.sqrt (rpForm R S G G 0) := by
        ring

end ClayYM

end  -- ferme le 'noncomputable section' de ClayYM/Gap.lean
end  -- ferme l'enveloppe

-- ===== ClayYM/Fake/Trivial.lean (verbatim, sha256 a5fc2db5307a739b…, imports retirés) =====
section  -- enveloppe : borne la portée des 'open' (open scoped ContDiff définit la notation ω)
/-
ClayYM/Fake/Trivial.lean
========================
FAKE MODEL no. 1: the trivial theory `S(∅) = 1`, `S(l) = 0` otherwise (reconstructed Hilbert space
`= ℂΩ`). Proved results (no `sorry`):

* `trivS_OSAxioms`      : it satisfies ALL the Osterwalder–Schrader axioms, for every
                          representation `R` — so the axiom system `OSAxioms` is not
                          contradictory (unlike the pre-09/2026 vacuum axiom of the lean-dojo
                          repository, which made the structure empty);
* `trivS_hasMassGap`    : EVERY `Δ > 0` is a mass gap;
* `trivS_not_finiteMass`: it violates "m < ∞" (Jaffe–Witten §4).

Conclusion (mutation test): the clause `FiniteMass` is NECESSARY; without it, the
"OS + mass gap" part of the statement would be satisfied by the trivial theory.
-/

open scoped ContDiff BigOperators
open MeasureTheory Filter Topology

noncomputable section

namespace ClayYM

variable {ι : Type} {d : ℕ}

/-- The trivial theory. -/
def trivS (ι : Type) (d : ℕ) : Schwinger ι d := fun l => if l = [] then 1 else 0

lemma trivS_append (l l' : LList ι d) :
    trivS ι d (l ++ l') = trivS ι d l * trivS ι d l' := by
  unfold trivS
  by_cases h : l = [] <;> by_cases h' : l' = [] <;> simp [h, h']

lemma trivS_mkList {n : ℕ} (i : Fin n → ι) (x : Config d n) :
    trivS ι d (mkList i x) = if n = 0 then 1 else 0 := by
  unfold trivS mkList
  simp [List.ofFn_eq_nil_iff]

lemma trivS_shiftList (a : Spacetime d) (l : LList ι d) :
    trivS ι d (shiftList a l) = trivS ι d l := by
  unfold trivS shiftList
  simp

/-- Indicator of "term without points". -/
def c0 {n : ℕ} : ℝ := if n = 0 then 1 else 0

lemma sum_reflect_c0 [Fintype ι] {n : ℕ} (M : Matrix ι ι ℝ) (lab : Fin n → ι) (c : ℝ) :
    (∑ j : Fin n → ι, (∏ k, M (lab (Fin.rev k)) (j k)) * ((if n = 0 then (1:ℝ) else 0) * c)) =
      (if n = 0 then (1:ℝ) else 0) * c := by
  cases n with
  | zero => simp
  | succ n => simp

lemma rpKernel_trivS [Fintype ι] [NeZero d] (R : CompRep ι d) (a b : Term ι d) (t : ℝ)
    (x : Config d a.n) (y : Config d b.n) :
    rpKernel R (trivS ι d) a b t x y =
      (if a.n = 0 then (1:ℝ) else 0) * (if b.n = 0 then (1:ℝ) else 0) := by
  obtain ⟨n, la, fa⟩ := a
  obtain ⟨m, lb, fb⟩ := b
  simp only [rpKernel, trivS_append, trivS_mkList]
  exact sum_reflect_c0 (R (θ d)) la _

/-- "Amplitude" of a family in the trivial theory: the component along `Ω`. -/
def trivAmp [NeZero d] (F : Family ι d) : ℝ :=
  (F.map fun a => (if a.n = 0 then (1:ℝ) else 0) * ∫ x, a.f x).sum

lemma integral_prod_const {n m : ℕ} (f : Config d n → ℝ) (g : Config d m → ℝ) (k : ℝ) :
    (∫ x, ∫ y, f x * g y * k) = (∫ x, f x) * (∫ y, g y) * k := by
  have h1 : ∀ x, (∫ y, f x * g y * k) = (f x * k) * ∫ y, g y := by
    intro x
    rw [← integral_const_mul]
    congr 1; ext y; ring
  simp_rw [h1]
  rw [integral_mul_const, integral_mul_const]
  ring

lemma rpForm_trivS [Fintype ι] [NeZero d] (R : CompRep ι d) (F G : Family ι d) (t : ℝ) :
    rpForm R (trivS ι d) F G t = trivAmp F * trivAmp G := by
  unfold rpForm trivAmp
  simp only [rpKernel_trivS]
  have key : ∀ a b : Term ι d,
      (∫ x, ∫ y, a.f x * b.f y *
        ((if a.n = 0 then (1:ℝ) else 0) * (if b.n = 0 then (1:ℝ) else 0))) =
      ((if a.n = 0 then (1:ℝ) else 0) * ∫ x, a.f x) *
        ((if b.n = 0 then (1:ℝ) else 0) * ∫ y, b.f y) := by
    intro a b
    rw [integral_prod_const]
    ring
  simp_rw [key, List.sum_map_mul_left, List.sum_map_mul_right]

lemma volume_config_zero_univ : (volume : Measure (Config d 0)) Set.univ = 1 := by
  rw [volume_pi, Measure.pi_univ]
  simp

lemma volume_real_config_zero_univ : (volume : Measure (Config d 0)).real Set.univ = 1 := by
  rw [measureReal_def, volume_config_zero_univ]
  simp

lemma trivAmp_vac [NeZero d] : trivAmp (vac ι : Family ι d) = 1 := by
  simp only [trivAmp, vac, vacTerm, List.map_cons, List.map_nil, List.sum_cons, List.sum_nil,
    add_zero]
  simp [vacTest, volume_real_config_zero_univ]

/-- The trivial theory satisfies all the OS axioms (for every representation `R`). -/
theorem trivS_OSAxioms [Fintype ι] [NeZero d] (R : CompRep ι d) :
    OSAxioms R (trivS ι d) where
  normalized := by simp [trivS]
  smooth := by
    intro n i
    simp only [trivS_mkList]
    exact contDiffOn_const
  linear_growth := by
    refine ⟨1, 0, 0, one_pos, le_rfl, le_rfl, ?_⟩
    intro n i x _
    rw [trivS_mkList, zero_mul, Real.rpow_zero, Real.rpow_zero, mul_one, mul_one]
    split_ifs <;> norm_num
  translation_invariant := by
    intro a l _
    exact trivS_shiftList a l
  rotation_covariant := by
    intro g n i x _
    simp only [trivS_mkList]
    cases n with
    | zero => simp
    | succ n => simp
  symmetric := by
    intro l l' h
    unfold trivS
    by_cases hl : l = []
    · subst hl
      have : l' = [] := List.Perm.eq_nil h.symm
      simp [this]
    · have : l' ≠ [] := fun h' => hl (List.Perm.eq_nil (h' ▸ h))
      simp [hl, this]
  reflection_positive := by
    intro F
    rw [rpForm_trivS]
    exact mul_self_nonneg _
  cluster := by
    intro l l' a _ _ _ _
    simp only [trivS_append, trivS_shiftList]
    exact tendsto_const_nhds

/-- Every `Δ > 0` is a mass gap of the trivial theory. -/
theorem trivS_hasMassGap [Fintype ι] [NeZero d] (R : CompRep ι d) {Δ : ℝ} (hΔ : 0 < Δ) :
    HasMassGap R (trivS ι d) Δ := by
  refine ⟨hΔ, fun F G t _ => ?_⟩
  simp only [rpForm_trivS, trivAmp_vac, mul_one, one_mul, sub_self, abs_zero]
  exact mul_nonneg (mul_nonneg (Real.exp_pos _).le (Real.sqrt_nonneg _)) (Real.sqrt_nonneg _)

/-- The trivial theory violates "m < ∞". -/
theorem trivS_not_finiteMass [Fintype ι] [NeZero d] (R : CompRep ι d) :
    ¬ FiniteMass R (trivS ι d) := by
  rintro ⟨M, hM⟩
  have hpos : 0 < max M 0 + 1 := by positivity
  have := hM (trivS_hasMassGap R hpos)
  linarith [le_max_left M 0]

/-- … hence it violates the mass gap in the Clay sense. -/
theorem trivS_not_clayMassGap [Fintype ι] [NeZero d] (R : CompRep ι d) :
    ¬ ClayMassGap R (trivS ι d) := fun h => trivS_not_finiteMass R h.2

end ClayYM

end  -- ferme le 'noncomputable section' de ClayYM/Fake/Trivial.lean
end  -- ferme l'enveloppe

-- ===== ClayYM/Transfer.lean (verbatim, sha256 4e9a2e0212cc23f3…, imports retirés) =====
section  -- enveloppe : borne la portée des 'open' (open scoped ContDiff définit la notation ω)
/-
ClayYM/Transfer.lean  (v1.1)
============================
Abstract layer of the mass gap: the gap as a uniform bound on the transfer form, its closure under
limits, and its relation with the operator form `‖e^{-tH}(1 − P_Ω)‖ ≤ e^{-Δt}`.

No axiom, no `sorry`. The Osterwalder–Schrader reconstruction is NOT proved here: it enters only as
the NAMED HYPOTHESIS `Recon` (a structure passed as an explicit argument, never asserted).

* `VecOps`, `IsBilin` : formal operations on the vectors of the OS pre-Hilbert space (for families of
  test functions: concatenation, scaling, vacuum) and bilinearity of the OS form
  `B F G t = ⟪F, τ_t G⟫` for these operations;
* `MassGapOn`         : the mass gap of `ClayYM.HasMassGap`, restricted to a set of vectors;
* `QGapOn`            : the q-form `0 < q < 1 ∧ ∀ A ∈ 𝒜₀, ⟨v_A, e^{-ℓH} v_A⟩ ≤ q ‖v_A‖²`, with the
                        truncated vector `v_A = A − ⟨Ω, A⟩ Ω`;
* `QGapOn.of_tendsto` : CLOSURE LEMMA (pointwise limits, along any filter, with the SAME `q`);
* `decay_of_qbound`   : elementary semigroup estimate (bound at one time `ℓ` ⟹ bound `q^{t/ℓ}` at every
                        time `t ≥ 0`; no spectral theorem);
* `Recon`             : reconstruction data (real Hilbert space, class map, strongly continuous
                        transfer semigroup of self-adjoint contractions);
* `Recon.massGapOn_of_qGapOn`     : q-form + density ⟹ mass gap `Δ = −log q / ℓ`;
* `MassGapOn.qGapOn`              : mass gap `Δ` ⟹ q-form with `q = e^{−Δℓ}` (no reconstruction);
* `Recon.vacuum_unique`           : q-form + density ⟹ every vector fixed by `e^{-ℓH}` is a multiple
                                    of `Ω` (uniqueness of the vacuum is a CONSEQUENCE, not a hypothesis);
* `Recon.massGapOn_univ_iff_opNorm` : mass gap ⟺ `‖e^{-tH}(1 − P_Ω)‖ ≤ e^{-Δt}` for all `t ≥ 0`.
-/

open Filter Topology
open scoped RealInnerProductSpace

noncomputable section

namespace ClayYM.Transfer

universe u

variable {V : Type u}

/-! ### Formal operations and the two forms of the gap -/

/-- Formal operations on the vectors of the OS pre-Hilbert space: formal sum, scaling, vacuum.
No law is assumed; the laws used are stated separately (`IsBilin`). -/
structure VecOps (V : Type u) where
  add : V → V → V
  smul : ℝ → V → V
  Ω : V

/-- Bilinearity of the OS form `B F G t = ⟪F, τ_t G⟫` for the formal operations. -/
structure IsBilin (o : VecOps V) (B : V → V → ℝ → ℝ) : Prop where
  add_left : ∀ F F' G t, B (o.add F F') G t = B F G t + B F' G t
  add_right : ∀ F G G' t, B F (o.add G G') t = B F G t + B F G' t
  smul_left : ∀ c F G t, B (o.smul c F) G t = c * B F G t
  smul_right : ∀ c F G t, B F (o.smul c G) t = c * B F G t

/-- Truncated vector `v_A = A − ⟨Ω, A⟩ Ω`, with `⟨Ω, A⟩ = B Ω A 0`. -/
def VecOps.trunc (o : VecOps V) (B : V → V → ℝ → ℝ) (A : V) : V :=
  o.add A (o.smul (-(B o.Ω A 0)) o.Ω)

/-- Mass gap `Δ` restricted to a set `D` of vectors. With `D = univ` and the OS form of a Schwinger
function this is exactly `ClayYM.HasMassGap` (see `ClayYM.hasMassGap_iff_massGapOn`). -/
def MassGapOn (o : VecOps V) (B : V → V → ℝ → ℝ) (D : Set V) (Δ : ℝ) : Prop :=
  0 < Δ ∧ ∀ F ∈ D, ∀ G ∈ D, ∀ t : ℝ, 0 ≤ t →
    |B F G t - B F o.Ω 0 * B o.Ω G 0| ≤
      Real.exp (-(Δ * t)) * Real.sqrt (B F F 0) * Real.sqrt (B G G 0)

/-- **q-form of the gap** on a set `𝒜₀`, at the physical time `ℓ`:
`0 < q < 1` and `⟨v_A, e^{-ℓH} v_A⟩ ≤ q ‖v_A‖²` for every `A ∈ 𝒜₀`. The SAME `q` serves every `A`
(the statement `∃ q, QGapOn o B 𝒜₀ ℓ q` is `∃ q < 1, ∀ A ∈ 𝒜₀, …`). -/
def QGapOn (o : VecOps V) (B : V → V → ℝ → ℝ) (𝒜₀ : Set V) (ℓ q : ℝ) : Prop :=
  0 < ℓ ∧ 0 < q ∧ q < 1 ∧
    ∀ A ∈ 𝒜₀, B (o.trunc B A) (o.trunc B A) ℓ ≤ q * B (o.trunc B A) (o.trunc B A) 0

lemma QGapOn.mono {o : VecOps V} {B : V → V → ℝ → ℝ} {𝒜₀ 𝒜₁ : Set V} {ℓ q : ℝ}
    (h : QGapOn o B 𝒜₁ ℓ q) (hsub : 𝒜₀ ⊆ 𝒜₁) : QGapOn o B 𝒜₀ ℓ q :=
  ⟨h.1, h.2.1, h.2.2.1, fun A hA => h.2.2.2 A (hsub hA)⟩

lemma MassGapOn.mono {o : VecOps V} {B : V → V → ℝ → ℝ} {D D' : Set V} {Δ : ℝ}
    (h : MassGapOn o B D' Δ) (hsub : D ⊆ D') : MassGapOn o B D Δ :=
  ⟨h.1, fun F hF G hG t ht => h.2 F (hsub hF) G (hsub hG) t ht⟩

/-- Expanded truncated correlation (a polynomial in finitely many values of `B`). -/
def truncCorr (o : VecOps V) (B : V → V → ℝ → ℝ) (A : V) (t : ℝ) : ℝ :=
  B A A t - B o.Ω A 0 * B A o.Ω t - B o.Ω A 0 * B o.Ω A t + B o.Ω A 0 ^ 2 * B o.Ω o.Ω t

lemma IsBilin.trunc_trunc {o : VecOps V} {B : V → V → ℝ → ℝ} (h : IsBilin o B) (A : V) (t : ℝ) :
    B (o.trunc B A) (o.trunc B A) t = truncCorr o B A t := by
  simp only [VecOps.trunc, truncCorr, h.add_left, h.add_right, h.smul_left, h.smul_right]
  ring

lemma IsBilin.vac_trunc {o : VecOps V} {B : V → V → ℝ → ℝ} (h : IsBilin o B)
    (hΩ : B o.Ω o.Ω 0 = 1) (A : V) : B o.Ω (o.trunc B A) 0 = 0 := by
  simp only [VecOps.trunc, h.add_right, h.smul_right, hΩ]
  ring

/-! ### Closure lemma -/

/-- Pointwise convergence of the transfer form on `𝒜₀ ∪ {Ω}`, at the two times `0` and `ℓ`
(the weakest convergence used by the closure lemma). -/
def ConvergesOn {α : Type*} (L : Filter α) (o : VecOps V) (Bk : α → V → V → ℝ → ℝ)
    (B : V → V → ℝ → ℝ) (𝒜₀ : Set V) (ℓ : ℝ) : Prop :=
  ∀ F ∈ insert o.Ω 𝒜₀, ∀ G ∈ insert o.Ω 𝒜₀, ∀ t ∈ ({0, ℓ} : Set ℝ),
    Tendsto (fun k => Bk k F G t) L (𝓝 (B F G t))

/-- **Closure lemma.** If the forms `Bk k` converge pointwise on `𝒜₀ ∪ {Ω}` (times `0` and `ℓ`) and
eventually satisfy the q-form with the SAME `q`, the limit satisfies it. Any filter: sequences,
subsequences, nets (no choice of subsequence is needed). -/
theorem QGapOn.of_tendsto {α : Type*} {L : Filter α} [L.NeBot] {o : VecOps V}
    {Bk : α → V → V → ℝ → ℝ} {B : V → V → ℝ → ℝ} {𝒜₀ : Set V} {ℓ q : ℝ}
    (hbk : ∀ k, IsBilin o (Bk k)) (hb : IsBilin o B) (hconv : ConvergesOn L o Bk B 𝒜₀ ℓ)
    (h : ∀ᶠ k in L, QGapOn o (Bk k) 𝒜₀ ℓ q) : QGapOn o B 𝒜₀ ℓ q := by
  obtain ⟨k₀, hk₀⟩ := h.exists
  refine ⟨hk₀.1, hk₀.2.1, hk₀.2.2.1, fun A hA => ?_⟩
  have hA' : A ∈ insert o.Ω 𝒜₀ := Set.mem_insert_of_mem _ hA
  have hΩ' : o.Ω ∈ insert o.Ω 𝒜₀ := Set.mem_insert _ _
  have h0 : (0 : ℝ) ∈ ({0, ℓ} : Set ℝ) := by simp
  have hℓ : ℓ ∈ ({0, ℓ} : Set ℝ) := by simp
  have tc : ∀ t ∈ ({0, ℓ} : Set ℝ),
      Tendsto (fun k => truncCorr o (Bk k) A t) L (𝓝 (truncCorr o B A t)) := by
    intro t ht
    unfold truncCorr
    have e1 := hconv A hA' A hA' t ht
    have e2 := hconv o.Ω hΩ' A hA' 0 h0
    have e3 := hconv A hA' o.Ω hΩ' t ht
    have e4 := hconv o.Ω hΩ' A hA' t ht
    have e5 := hconv o.Ω hΩ' o.Ω hΩ' t ht
    exact ((e1.sub (e2.mul e3)).sub (e2.mul e4)).add ((e2.pow 2).mul e5)
  rw [hb.trunc_trunc, hb.trunc_trunc]
  have hev : ∀ᶠ k in L, truncCorr o (Bk k) A ℓ ≤ q * truncCorr o (Bk k) A 0 := by
    filter_upwards [h] with k hk
    rw [← (hbk k).trunc_trunc, ← (hbk k).trunc_trunc]
    exact hk.2.2.2 A hA
  exact le_of_tendsto_of_tendsto (tc ℓ hℓ) ((tc 0 h0).const_mul q) hev

/-! ### From the gap to the q-form (no reconstruction needed) -/

/-- Mass gap `Δ` ⟹ q-form with `q = e^{−Δℓ}`, for any `𝒜₀` and any `ℓ > 0`. Uses only bilinearity,
the normalisation `⟨Ω, Ω⟩ = 1` and reflection positivity `0 ≤ ⟨F, F⟩`. -/
theorem MassGapOn.qGapOn {o : VecOps V} {B : V → V → ℝ → ℝ} {Δ ℓ : ℝ} (hb : IsBilin o B)
    (hΩ : B o.Ω o.Ω 0 = 1) (hpos : ∀ F, 0 ≤ B F F 0) (h : MassGapOn o B Set.univ Δ)
    (hℓ : 0 < ℓ) (𝒜₀ : Set V) : QGapOn o B 𝒜₀ ℓ (Real.exp (-(Δ * ℓ))) := by
  refine ⟨hℓ, Real.exp_pos _, Real.exp_lt_one_iff.2 (neg_neg_of_pos (mul_pos h.1 hℓ)), fun A _ => ?_⟩
  have h0 : B o.Ω (o.trunc B A) 0 = 0 := hb.vac_trunc hΩ A
  have h1 := h.2 (o.trunc B A) (Set.mem_univ _) (o.trunc B A) (Set.mem_univ _) ℓ hℓ.le
  rw [h0, mul_zero, sub_zero, mul_assoc, Real.mul_self_sqrt (hpos _)] at h1
  exact (le_abs_self _).trans h1

/-! ### Elementary semigroup estimate -/

section Decay

variable {E : Type*} [NormedAddCommGroup E] [InnerProductSpace ℝ E]

/-- **Semigroup estimate.** Let `T` be a semigroup of self-adjoint contractions fixing `ω`. If
`⟨w, T ℓ w⟩ ≤ q ‖w‖²` for every `w ⊥ ω`, then `‖T t w‖ ≤ q^{t/ℓ} ‖w‖` for every `t ≥ 0` and `w ⊥ ω`.
Proof: halving (`‖T(s/2) w‖² = ⟨w, T s w⟩`), dyadic times, then a limit. No spectral theorem. -/
theorem decay_of_qbound (T : ℝ → E →L[ℝ] E) (ω : E) {ℓ q : ℝ}
    (hadd : ∀ s t, 0 ≤ s → 0 ≤ t → T (s + t) = (T s).comp (T t))
    (hsymm : ∀ t, 0 ≤ t → ∀ x y, ⟪T t x, y⟫ = ⟪x, T t y⟫)
    (hcontr : ∀ t, 0 ≤ t → ‖T t‖ ≤ 1)
    (hvac : ∀ t, 0 ≤ t → T t ω = ω)
    (hℓ : 0 < ℓ) (hq : 0 < q) (hq1 : q ≤ 1)
    (hb : ∀ w, ⟪ω, w⟫ = 0 → ⟪w, T ℓ w⟫ ≤ q * ‖w‖ ^ 2) :
    ∀ t, 0 ≤ t → ∀ w, ⟪ω, w⟫ = 0 → ‖T t w‖ ≤ q ^ (t / ℓ) * ‖w‖ := by
  have hinv : ∀ t, 0 ≤ t → ∀ w, ⟪ω, w⟫ = 0 → ⟪ω, T t w⟫ = 0 := by
    intro t ht w hw
    rw [← hsymm t ht, hvac t ht, hw]
  have hc : ∀ t, 0 ≤ t → ∀ w, ‖T t w‖ ≤ ‖w‖ := by
    intro t ht w
    calc ‖T t w‖ ≤ ‖T t‖ * ‖w‖ := (T t).le_opNorm w
      _ ≤ 1 * ‖w‖ := mul_le_mul_of_nonneg_right (hcontr t ht) (norm_nonneg w)
      _ = ‖w‖ := one_mul _
  have hsq : ∀ s, 0 ≤ s → ∀ w, ‖T (s / 2) w‖ ^ 2 = ⟪w, T s w⟫ := by
    intro s hs w
    have hs2 : 0 ≤ s / 2 := by linarith
    rw [← real_inner_self_eq_norm_sq, hsymm (s / 2) hs2, ← ContinuousLinearMap.comp_apply,
      ← hadd _ _ hs2 hs2, add_halves]
  have hhalf : ∀ s, 0 ≤ s → ∀ c, 0 ≤ c →
      (∀ w, ⟪ω, w⟫ = 0 → ‖T s w‖ ≤ c * ‖w‖) →
      ∀ w, ⟪ω, w⟫ = 0 → ‖T (s / 2) w‖ ≤ Real.sqrt c * ‖w‖ := by
    intro s hs c hc0 hcs w hw
    have h1 : ‖T (s / 2) w‖ ^ 2 ≤ (Real.sqrt c * ‖w‖) ^ 2 := by
      rw [hsq s hs w, mul_pow, Real.sq_sqrt hc0]
      calc ⟪w, T s w⟫ ≤ ‖w‖ * ‖T s w‖ := real_inner_le_norm _ _
        _ ≤ ‖w‖ * (c * ‖w‖) := mul_le_mul_of_nonneg_left (hcs w hw) (norm_nonneg w)
        _ = c * ‖w‖ ^ 2 := by ring
    exact (sq_le_sq₀ (norm_nonneg _) (by positivity)).1 h1
  have hℓ2 : 0 ≤ ℓ / 2 := by linarith
  have hbase : ∀ w, ⟪ω, w⟫ = 0 → ‖T (ℓ / 2) w‖ ≤ Real.sqrt q * ‖w‖ := by
    intro w hw
    have h1 : ‖T (ℓ / 2) w‖ ^ 2 ≤ (Real.sqrt q * ‖w‖) ^ 2 := by
      rw [hsq ℓ hℓ.le w, mul_pow, Real.sq_sqrt hq.le]
      exact hb w hw
    exact (sq_le_sq₀ (norm_nonneg _) (by positivity)).1 h1
  have hP0 : ∀ w, ⟪ω, w⟫ = 0 → ‖T ℓ w‖ ≤ q * ‖w‖ := by
    intro w hw
    have e : T ℓ w = T (ℓ / 2) (T (ℓ / 2) w) := by
      rw [← ContinuousLinearMap.comp_apply, ← hadd _ _ hℓ2 hℓ2, add_halves]
    rw [e]
    calc ‖T (ℓ / 2) (T (ℓ / 2) w)‖ ≤ Real.sqrt q * ‖T (ℓ / 2) w‖ :=
          hbase _ (hinv _ hℓ2 w hw)
      _ ≤ Real.sqrt q * (Real.sqrt q * ‖w‖) :=
          mul_le_mul_of_nonneg_left (hbase w hw) (Real.sqrt_nonneg q)
      _ = q * ‖w‖ := by rw [← mul_assoc, Real.mul_self_sqrt hq.le]
  have hdy : ∀ m : ℕ, ∀ w, ⟪ω, w⟫ = 0 →
      ‖T (ℓ / 2 ^ m) w‖ ≤ q ^ ((1 / 2 : ℝ) ^ m) * ‖w‖ := by
    intro m
    induction m with
    | zero => simpa using hP0
    | succ m ih =>
      intro w hw
      have hs : 0 ≤ ℓ / 2 ^ m := by positivity
      have h := hhalf (ℓ / 2 ^ m) hs (q ^ ((1 / 2 : ℝ) ^ m)) (by positivity) ih w hw
      have e1 : ℓ / 2 ^ m / 2 = ℓ / 2 ^ (m + 1) := by rw [pow_succ, div_div]
      have e2 : Real.sqrt (q ^ ((1 / 2 : ℝ) ^ m)) = q ^ ((1 / 2 : ℝ) ^ (m + 1)) := by
        rw [Real.sqrt_eq_rpow, ← Real.rpow_mul hq.le, pow_succ]
      rw [e1, e2] at h
      exact h
  have hmul : ∀ s, 0 ≤ s → ∀ c, 0 ≤ c → (∀ w, ⟪ω, w⟫ = 0 → ‖T s w‖ ≤ c * ‖w‖) →
      ∀ k : ℕ, ∀ w, ⟪ω, w⟫ = 0 → ‖T (k * s) w‖ ≤ c ^ k * ‖w‖ := by
    intro s hs c hc0 hcs k
    induction k with
    | zero => intro w _; simpa using hc 0 le_rfl w
    | succ k ih =>
      intro w hw
      have hks : 0 ≤ (k : ℝ) * s := by positivity
      have e : T (((k + 1 : ℕ) : ℝ) * s) w = T s (T (k * s) w) := by
        rw [← ContinuousLinearMap.comp_apply, ← hadd _ _ hs hks]
        congr 2
        push_cast
        ring
      rw [e]
      calc ‖T s (T (k * s) w)‖ ≤ c * ‖T (k * s) w‖ := hcs _ (hinv _ hks w hw)
        _ ≤ c * (c ^ k * ‖w‖) := mul_le_mul_of_nonneg_left (ih w hw) hc0
        _ = c ^ (k + 1) * ‖w‖ := by ring
  intro t ht w hw
  have hbound : ∀ m : ℕ, ‖T t w‖ ≤ q ^ (t / ℓ - (1 / 2 : ℝ) ^ m) * ‖w‖ := by
    intro m
    have hs : 0 < ℓ / 2 ^ m := by positivity
    have hfl := Nat.floor_le (div_nonneg ht hs.le)
    have hlt := Nat.lt_floor_add_one (t / (ℓ / 2 ^ m))
    set s : ℝ := ℓ / 2 ^ m with hs_def
    set k : ℕ := ⌊t / s⌋₊ with hk_def
    have hks : (k : ℝ) * s ≤ t := by
      calc (k : ℝ) * s ≤ t / s * s := mul_le_mul_of_nonneg_right hfl hs.le
        _ = t := div_mul_cancel₀ t hs.ne'
    have hr : 0 ≤ t - k * s := by linarith
    have hks0 : 0 ≤ (k : ℝ) * s := by positivity
    have e : T t w = T (t - k * s) (T (k * s) w) := by
      rw [← ContinuousLinearMap.comp_apply, ← hadd _ _ hr hks0]
      congr 2
      ring
    have h1 : ‖T t w‖ ≤ (q ^ ((1 / 2 : ℝ) ^ m)) ^ k * ‖w‖ := by
      rw [e]
      exact (hc _ hr _).trans (hmul s hs.le _ (by positivity) (hdy m) k w hw)
    have h2 : (q ^ ((1 / 2 : ℝ) ^ m)) ^ k = q ^ ((1 / 2 : ℝ) ^ m * k) := by
      rw [← Real.rpow_natCast, ← Real.rpow_mul hq.le]
    have hsℓ : (1 / 2 : ℝ) ^ m = s / ℓ := by
      rw [hs_def, one_div_pow]
      field_simp
    have key : t - s ≤ s * k := by
      have := (div_lt_iff₀ hs).1 hlt
      nlinarith
    have h3 : t / ℓ - (1 / 2 : ℝ) ^ m ≤ (1 / 2 : ℝ) ^ m * k := by
      rw [hsℓ]
      calc t / ℓ - s / ℓ = (t - s) / ℓ := (sub_div t s ℓ).symm
        _ ≤ (s * k) / ℓ := by gcongr
        _ = s / ℓ * k := by ring
    calc ‖T t w‖ ≤ q ^ ((1 / 2 : ℝ) ^ m * k) * ‖w‖ := by rw [← h2]; exact h1
      _ ≤ q ^ (t / ℓ - (1 / 2 : ℝ) ^ m) * ‖w‖ :=
          mul_le_mul_of_nonneg_right (Real.rpow_le_rpow_of_exponent_ge hq hq1 h3) (norm_nonneg w)
  have hlim : Tendsto (fun m : ℕ => q ^ (t / ℓ - (1 / 2 : ℝ) ^ m) * ‖w‖) atTop
      (𝓝 (q ^ (t / ℓ) * ‖w‖)) := by
    have h1 : Tendsto (fun m : ℕ => t / ℓ - (1 / 2 : ℝ) ^ m) atTop (𝓝 (t / ℓ - 0)) :=
      tendsto_const_nhds.sub (tendsto_pow_atTop_nhds_zero_of_lt_one (by norm_num) (by norm_num))
    rw [sub_zero] at h1
    have h2 := ((Real.continuousAt_const_rpow hq.ne').tendsto).comp h1
    exact h2.mul_const _
  exact ge_of_tendsto' hlim hbound

end Decay

/-! ### Reconstruction data (NAMED HYPOTHESIS) -/

/-- **Reconstruction data** for the OS form `B` (the conclusion of the Osterwalder–Schrader
reconstruction theorem for the Hilbert space and the transfer semigroup — NOT proved here, used
only as an explicit hypothesis): a real Hilbert space `H`, the class map `cls : V → H`, and a
STRONGLY CONTINUOUS semigroup `T t` (`t ≥ 0`) of self-adjoint contractions fixing the vacuum, with
`⟨[F], T t [G]⟩ = B F G t`; the classes are dense (the reconstructed space is the completion of the
classes, so the vacuum is cyclic for `V` by construction). Such a semigroup is `T t = e^{-tH}` for a
self-adjoint `H ≥ 0` (standard semigroup theory, not formalised). Completeness and strong
continuity are required for this identification only: no theorem of this file uses them. -/
structure Recon (o : VecOps V) (B : V → V → ℝ → ℝ) where
  /-- The physical Hilbert space. -/
  H : Type
  [instNormed : NormedAddCommGroup H]
  [instInner : InnerProductSpace ℝ H]
  [instComplete : CompleteSpace H]
  /-- Class map `F ↦ [F]`. -/
  cls : V → H
  /-- Transfer semigroup `T t = e^{-tH}`. -/
  T : ℝ → H →L[ℝ] H
  inner_cls : ∀ F G, ⟪cls F, cls G⟫ = B F G 0
  inner_T : ∀ F G t, 0 ≤ t → ⟪cls F, T t (cls G)⟫ = B F G t
  T_add : ∀ s t, 0 ≤ s → 0 ≤ t → T (s + t) = (T s).comp (T t)
  T_symm : ∀ t, 0 ≤ t → ∀ x y, ⟪T t x, y⟫ = ⟪x, T t y⟫
  T_contr : ∀ t, 0 ≤ t → ‖T t‖ ≤ 1
  T_vac : ∀ t, 0 ≤ t → T t (cls o.Ω) = cls o.Ω
  /-- Strong continuity at `0⁺` (with the semigroup law: a C₀-semigroup). -/
  T_cont : ∀ x, Tendsto (fun t => T t x) (𝓝[≥] 0) (𝓝 x)
  dense : DenseRange cls

attribute [instance] Recon.instNormed Recon.instInner Recon.instComplete

namespace Recon

variable {o : VecOps V} {B : V → V → ℝ → ℝ} (r : Recon o B)

/-- The vacuum vector `Ω = [vac]`. -/
def ω : r.H := r.cls o.Ω

lemma inner_ω_self (hΩ : B o.Ω o.Ω 0 = 1) : ⟪r.ω, r.ω⟫ = 1 := by
  rw [ω, r.inner_cls, hΩ]

lemma norm_cls (F : V) : ‖r.cls F‖ = Real.sqrt (B F F 0) := by
  rw [norm_eq_sqrt_real_inner, r.inner_cls]

lemma T_ω (t : ℝ) (ht : 0 ≤ t) : r.T t r.ω = r.ω := r.T_vac t ht

lemma inner_ω_T (t : ℝ) (ht : 0 ≤ t) (x : r.H) : ⟪r.ω, r.T t x⟫ = ⟪r.ω, x⟫ := by
  rw [← r.T_symm t ht, r.T_ω t ht]

lemma inner_ω_perp (hΩ : B o.Ω o.Ω 0 = 1) (x : r.H) : ⟪r.ω, x - ⟪r.ω, x⟫ • r.ω⟫ = 0 := by
  rw [inner_sub_right, real_inner_smul_right, r.inner_ω_self hΩ]
  ring

lemma norm_perp_le (hΩ : B o.Ω o.Ω 0 = 1) (x : r.H) : ‖x - ⟪r.ω, x⟫ • r.ω‖ ≤ ‖x‖ := by
  have h : ‖x - ⟪r.ω, x⟫ • r.ω‖ ^ 2 = ‖x‖ ^ 2 - ⟪r.ω, x⟫ ^ 2 := by
    rw [norm_sub_sq_real, norm_smul, mul_pow, real_inner_smul_right, Real.norm_eq_abs, sq_abs,
      ← real_inner_self_eq_norm_sq r.ω, r.inner_ω_self hΩ, real_inner_comm r.ω x]
    ring
  have h2 : ‖x - ⟪r.ω, x⟫ • r.ω‖ ^ 2 ≤ ‖x‖ ^ 2 := by
    rw [h]
    nlinarith [sq_nonneg ⟪r.ω, x⟫]
  exact (sq_le_sq₀ (norm_nonneg _) (norm_nonneg _)).1 h2

/-- Truncated correlation = matrix element of `e^{-tH}` between truncated vectors. -/
lemma corr_eq (hΩ : B o.Ω o.Ω 0 = 1) (F G : V) (t : ℝ) (ht : 0 ≤ t) :
    B F G t - B F o.Ω 0 * B o.Ω G 0 =
      ⟪r.cls F - ⟪r.ω, r.cls F⟫ • r.ω, r.T t (r.cls G - ⟪r.ω, r.cls G⟫ • r.ω)⟫ := by
  have h1 : B F G t = ⟪r.cls F, r.T t (r.cls G)⟫ := (r.inner_T F G t ht).symm
  have h2 : B F o.Ω 0 = ⟪r.cls F, r.ω⟫ := (r.inner_cls F o.Ω).symm
  have h3 : B o.Ω G 0 = ⟪r.ω, r.cls G⟫ := (r.inner_cls o.Ω G).symm
  rw [h1, h2, h3, map_sub, map_smul, r.T_ω t ht]
  simp only [inner_sub_left, inner_sub_right, real_inner_smul_left, real_inner_smul_right,
    r.inner_ω_T t ht, r.inner_ω_self hΩ]
  ring

/-- The q-bound, extended by density from the truncated classes to the whole of `Ω^⊥`. -/
lemma qbound {𝒜₀ : Set V} {ℓ q : ℝ} (hq : QGapOn o B 𝒜₀ ℓ q)
    (hd : ∀ w : r.H, ⟪r.ω, w⟫ = 0 → w ∈ closure (r.cls '' (o.trunc B '' 𝒜₀))) :
    ∀ w : r.H, ⟪r.ω, w⟫ = 0 → ⟪w, r.T ℓ w⟫ ≤ q * ‖w‖ ^ 2 := by
  intro w hw
  have hcl : IsClosed {x : r.H | ⟪x, r.T ℓ x⟫ ≤ q * ‖x‖ ^ 2} :=
    isClosed_le (continuous_id.inner (r.T ℓ).continuous)
      (continuous_const.mul (continuous_norm.pow 2))
  have hsub : r.cls '' (o.trunc B '' 𝒜₀) ⊆ {x : r.H | ⟪x, r.T ℓ x⟫ ≤ q * ‖x‖ ^ 2} := by
    rintro _ ⟨_, ⟨A, hA, rfl⟩, rfl⟩
    show ⟪r.cls (o.trunc B A), r.T ℓ (r.cls (o.trunc B A))⟫ ≤ q * ‖r.cls (o.trunc B A)‖ ^ 2
    rw [r.inner_T _ _ ℓ hq.1.le, ← real_inner_self_eq_norm_sq, r.inner_cls]
    exact hq.2.2.2 A hA
  exact closure_minimal hsub hcl (hd w hw)

/-- **q-form ⟹ mass gap.** With the reconstruction (named hypothesis) and the density of the
truncated classes of `𝒜₀` in `Ω^⊥`, the q-form gives the mass gap `Δ = −log q / ℓ`. -/
theorem massGapOn_of_qGapOn (hΩ : B o.Ω o.Ω 0 = 1) {𝒜₀ : Set V} {ℓ q : ℝ}
    (hq : QGapOn o B 𝒜₀ ℓ q)
    (hd : ∀ w : r.H, ⟪r.ω, w⟫ = 0 → w ∈ closure (r.cls '' (o.trunc B '' 𝒜₀))) :
    MassGapOn o B Set.univ (-Real.log q / ℓ) := by
  have hb := r.qbound hq hd
  obtain ⟨hℓ, hq0, hq1, -⟩ := hq
  have hdec := decay_of_qbound r.T r.ω r.T_add r.T_symm r.T_contr (fun t ht => r.T_ω t ht)
    hℓ hq0 hq1.le hb
  refine ⟨div_pos (neg_pos.2 (Real.log_neg hq0 hq1)) hℓ, fun F _ G _ t ht => ?_⟩
  rw [r.corr_eq hΩ F G t ht]
  have hexp : Real.exp (-(-Real.log q / ℓ * t)) = q ^ (t / ℓ) := by
    rw [Real.rpow_def_of_pos hq0]
    congr 1
    field_simp
  rw [hexp, ← r.norm_cls F, ← r.norm_cls G]
  calc |⟪r.cls F - ⟪r.ω, r.cls F⟫ • r.ω, r.T t (r.cls G - ⟪r.ω, r.cls G⟫ • r.ω)⟫|
      ≤ ‖r.cls F - ⟪r.ω, r.cls F⟫ • r.ω‖ * ‖r.T t (r.cls G - ⟪r.ω, r.cls G⟫ • r.ω)‖ :=
        abs_real_inner_le_norm _ _
    _ ≤ ‖r.cls F - ⟪r.ω, r.cls F⟫ • r.ω‖ * (q ^ (t / ℓ) * ‖r.cls G - ⟪r.ω, r.cls G⟫ • r.ω‖) :=
        mul_le_mul_of_nonneg_left (hdec t ht _ (r.inner_ω_perp hΩ _)) (norm_nonneg _)
    _ ≤ ‖r.cls F‖ * (q ^ (t / ℓ) * ‖r.cls G‖) := by
        gcongr
        · exact r.norm_perp_le hΩ _
        · exact r.norm_perp_le hΩ _
    _ = q ^ (t / ℓ) * ‖r.cls F‖ * ‖r.cls G‖ := by ring

/-- **Uniqueness of the vacuum is a consequence.** With the reconstruction and the density of the
truncated classes of `𝒜₀` in `Ω^⊥`, every vector fixed by `e^{-ℓH}` is a multiple of `Ω`. -/
theorem vacuum_unique (hΩ : B o.Ω o.Ω 0 = 1) {𝒜₀ : Set V} {ℓ q : ℝ} (hq : QGapOn o B 𝒜₀ ℓ q)
    (hd : ∀ w : r.H, ⟪r.ω, w⟫ = 0 → w ∈ closure (r.cls '' (o.trunc B '' 𝒜₀)))
    (w : r.H) (hw : r.T ℓ w = w) : w = ⟪r.ω, w⟫ • r.ω := by
  have hb := r.qbound hq hd
  have hperp : ⟪r.ω, w - ⟪r.ω, w⟫ • r.ω⟫ = 0 := r.inner_ω_perp hΩ w
  have hT : r.T ℓ (w - ⟪r.ω, w⟫ • r.ω) = w - ⟪r.ω, w⟫ • r.ω := by
    rw [map_sub, map_smul, hw, r.T_ω ℓ hq.1.le]
  have h1 := hb _ hperp
  rw [hT, real_inner_self_eq_norm_sq] at h1
  have h2 : ‖w - ⟪r.ω, w⟫ • r.ω‖ ^ 2 ≤ 0 := by
    have hq1 := hq.2.2.1
    nlinarith [sq_nonneg ‖w - ⟪r.ω, w⟫ • r.ω‖]
  have h3 : ‖w - ⟪r.ω, w⟫ • r.ω‖ = 0 :=
    pow_eq_zero_iff (n := 2) (by norm_num) |>.1 (le_antisymm h2 (sq_nonneg _))
  exact sub_eq_zero.1 (norm_eq_zero.1 h3)

/-! #### Linearity of the class map and density of the truncated classes -/

lemma eq_of_inner_cls {x y : r.H} (h : ∀ F, ⟪r.cls F, x⟫ = ⟪r.cls F, y⟫) : x = y := by
  have hall : ∀ z : r.H, ⟪z, x - y⟫ = 0 := by
    intro z
    refine r.dense.induction_on (p := fun z => ⟪z, x - y⟫ = 0) z ?_ ?_
    · exact isClosed_eq (continuous_id.inner continuous_const) continuous_const
    · intro F
      rw [inner_sub_right, h F, sub_self]
  have h0 := hall (x - y)
  rw [real_inner_self_eq_norm_sq] at h0
  have : ‖x - y‖ = 0 := pow_eq_zero_iff (n := 2) (by norm_num) |>.1 h0
  exact sub_eq_zero.1 (norm_eq_zero.1 this)

lemma cls_add (hb : IsBilin o B) (F G : V) : r.cls (o.add F G) = r.cls F + r.cls G :=
  r.eq_of_inner_cls fun K => by
    rw [inner_add_right, r.inner_cls, r.inner_cls, r.inner_cls, hb.add_right]

lemma cls_smul (hb : IsBilin o B) (c : ℝ) (F : V) : r.cls (o.smul c F) = c • r.cls F :=
  r.eq_of_inner_cls fun K => by
    rw [real_inner_smul_right, r.inner_cls, r.inner_cls, hb.smul_right]

lemma cls_trunc (hb : IsBilin o B) (A : V) :
    r.cls (o.trunc B A) = r.cls A - ⟪r.ω, r.cls A⟫ • r.ω := by
  rw [VecOps.trunc, r.cls_add hb, r.cls_smul hb, ω, r.inner_cls, neg_smul, ← sub_eq_add_neg]

/-- For `𝒜₀ = univ` the density hypothesis is automatic (cyclicity of the vacuum is built into
the reconstruction). -/
lemma truncDense_univ (hb : IsBilin o B) :
    ∀ w : r.H, ⟪r.ω, w⟫ = 0 → w ∈ closure (r.cls '' (o.trunc B '' Set.univ)) := by
  intro w hw
  have hP : Continuous fun x : r.H => x - ⟪r.ω, x⟫ • r.ω :=
    continuous_id.sub ((continuous_const.inner continuous_id).smul continuous_const)
  have hPw : w - ⟪r.ω, w⟫ • r.ω = w := by rw [hw, zero_smul, sub_zero]
  have himg : (fun x : r.H => x - ⟪r.ω, x⟫ • r.ω) '' Set.range r.cls =
      r.cls '' (o.trunc B '' Set.univ) := by
    ext x
    constructor
    · rintro ⟨_, ⟨A, rfl⟩, rfl⟩
      exact ⟨o.trunc B A, ⟨A, Set.mem_univ _, rfl⟩, r.cls_trunc hb A⟩
    · rintro ⟨_, ⟨A, -, rfl⟩, rfl⟩
      exact ⟨r.cls A, ⟨A, rfl⟩, (r.cls_trunc hb A).symm⟩
  rw [← himg, ← hPw]
  apply image_closure_subset_closure_image hP
  refine ⟨w, ?_, rfl⟩
  rw [r.dense.closure_range]
  exact Set.mem_univ _

/-! #### Operator form `‖e^{-tH}(1 − P_Ω)‖ ≤ e^{-Δt}` -/

/-- `1 − P_Ω`, with `P_Ω x = ⟨Ω, x⟩ Ω`. -/
def perp : r.H →L[ℝ] r.H := ContinuousLinearMap.id ℝ r.H - (innerSL ℝ r.ω).smulRight r.ω

lemma perp_apply (x : r.H) : r.perp x = x - ⟪r.ω, x⟫ • r.ω := by
  simp [perp, ContinuousLinearMap.smulRight_apply, innerSL_apply_apply]

lemma corr_eq_perp (F G : V) (t : ℝ) (ht : 0 ≤ t) :
    B F G t - B F o.Ω 0 * B o.Ω G 0 = ⟪r.cls F, ((r.T t).comp r.perp) (r.cls G)⟫ := by
  rw [ContinuousLinearMap.comp_apply, r.perp_apply, map_sub, map_smul, r.T_ω t ht,
    inner_sub_right, real_inner_smul_right, r.inner_T F G t ht, ω, r.inner_cls, r.inner_cls]
  ring

/-- **Operator form.** With the reconstruction, `HasMassGap`-type decay of the truncated
correlations is equivalent to `‖e^{-tH}(1 − P_Ω)‖ ≤ e^{-Δt}` for every `t ≥ 0`. -/
theorem massGapOn_univ_iff_opNorm (hΩ : B o.Ω o.Ω 0 = 1) (Δ : ℝ) :
    MassGapOn o B Set.univ Δ ↔
      0 < Δ ∧ ∀ t, 0 ≤ t → ‖(r.T t).comp r.perp‖ ≤ Real.exp (-(Δ * t)) := by
  constructor
  · rintro ⟨hΔ, h⟩
    refine ⟨hΔ, fun t ht => ?_⟩
    have hc : 0 ≤ Real.exp (-(Δ * t)) := (Real.exp_pos _).le
    have hcls : ∀ F G : V, |⟪r.cls F, ((r.T t).comp r.perp) (r.cls G)⟫| ≤
        Real.exp (-(Δ * t)) * ‖r.cls F‖ * ‖r.cls G‖ := by
      intro F G
      rw [← r.corr_eq_perp F G t ht, r.norm_cls, r.norm_cls]
      exact h F (Set.mem_univ _) G (Set.mem_univ _) t ht
    have hall : ∀ x y : r.H, |⟪x, ((r.T t).comp r.perp) y⟫| ≤
        Real.exp (-(Δ * t)) * ‖x‖ * ‖y‖ := by
      intro x y
      refine r.dense.induction_on
        (p := fun y => |⟪x, ((r.T t).comp r.perp) y⟫| ≤ Real.exp (-(Δ * t)) * ‖x‖ * ‖y‖) y ?_ ?_
      · exact isClosed_le (continuous_const.inner ((r.T t).comp r.perp).continuous).abs
          (continuous_const.mul continuous_norm)
      · intro G
        refine r.dense.induction_on (p := fun x => |⟪x, ((r.T t).comp r.perp) (r.cls G)⟫| ≤
          Real.exp (-(Δ * t)) * ‖x‖ * ‖r.cls G‖) x ?_ ?_
        · exact isClosed_le (continuous_id.inner continuous_const).abs
            ((continuous_const.mul continuous_norm).mul continuous_const)
        · intro F
          exact hcls F G
    refine ContinuousLinearMap.opNorm_le_bound _ hc fun y => ?_
    have h1 := hall (((r.T t).comp r.perp) y) y
    rw [real_inner_self_eq_norm_sq, abs_of_nonneg (sq_nonneg _)] at h1
    by_contra hcon
    push Not at hcon
    nlinarith [norm_nonneg (((r.T t).comp r.perp) y), mul_nonneg hc (norm_nonneg y)]
  · rintro ⟨hΔ, h⟩
    refine ⟨hΔ, fun F _ G _ t ht => ?_⟩
    rw [r.corr_eq_perp F G t ht, ← r.norm_cls F, ← r.norm_cls G]
    calc |⟪r.cls F, ((r.T t).comp r.perp) (r.cls G)⟫|
        ≤ ‖r.cls F‖ * ‖((r.T t).comp r.perp) (r.cls G)‖ := abs_real_inner_le_norm _ _
      _ ≤ ‖r.cls F‖ * (‖(r.T t).comp r.perp‖ * ‖r.cls G‖) :=
          mul_le_mul_of_nonneg_left (ContinuousLinearMap.le_opNorm _ _) (norm_nonneg _)
      _ ≤ ‖r.cls F‖ * (Real.exp (-(Δ * t)) * ‖r.cls G‖) := by
          gcongr
          exact h t ht
      _ = Real.exp (-(Δ * t)) * ‖r.cls F‖ * ‖r.cls G‖ := by ring

end Recon

end ClayYM.Transfer

end  -- ferme le 'noncomputable section' de ClayYM/Transfer.lean
end  -- ferme l'enveloppe

-- ===== ClayYM/GapQ.lean (verbatim, sha256 46a2b4217209941b…, imports retirés) =====
section  -- enveloppe : borne la portée des 'open' (open scoped ContDiff définit la notation ω)
/-
ClayYM/GapQ.lean  (v1.1)
========================
The q-form of the mass gap for the Schwinger kernels of `ClayYM`, its equivalence with `HasMassGap`
(and with the operator form `‖e^{-tH}(1 − P_Ω)‖ ≤ e^{-Δt}`), the CLOSURE LEMMA, and the uniqueness
of the vacuum. Abstract proofs: `ClayYM/Transfer.lean`.

No axiom, no `sorry`. The Osterwalder–Schrader reconstruction is the NAMED HYPOTHESIS
`OSReconstruction R S` (= `Transfer.Recon (famOps ι d) (rpForm R S)`): an explicit argument of the
conditional theorems, never asserted. Its satisfiability is checked on the trivial theory
(`trivRecon`); for a genuine OS theory it is the content of the OS reconstruction theorem
(OS 1973/1975), which is NOT formalised.

* `QGap R S 𝒜₀ ℓ q` : `0 < ℓ`, `0 < q < 1` and `⟨v_A, e^{-ℓH} v_A⟩ ≤ q ‖v_A‖²` for every `A ∈ 𝒜₀`,
  with `v_A = A − ⟨Ω, A⟩ Ω` the family `truncFam R S A`; the gap statement is `∃ q, QGap R S 𝒜₀ ℓ q`.
* `HasMassGap.qGap`          : `HasMassGap R S Δ` ⟹ `QGap R S 𝒜₀ ℓ (e^{−Δℓ})`  (OS axioms only);
* `QGap.hasMassGap`          : `QGap R S 𝒜₀ ℓ q` + density ⟹ `HasMassGap R S (−log q / ℓ)`
                               (named hypothesis `OSReconstruction`);
* `exists_hasMassGap_iff_exists_qGap` : the equivalence, for every fixed `ℓ > 0`;
* `hasMassGap_iff_opNorm`    : `HasMassGap R S Δ` ⟺ `0 < Δ ∧ ∀ t ≥ 0, ‖e^{-tH}(1 − P_Ω)‖ ≤ e^{-Δt}`;
* `QGap.of_tendsto`          : CLOSURE LEMMA (no hypothesis beyond pointwise convergence on
                               `𝒜₀ ∪ {Ω}` and the SAME `q`);
* `hasMassGap_of_tendsto`, `vacuum_unique_of_tendsto` : gap and unique vacuum of the limit, under
                               the named hypothesis for the LIMIT theory only;
* `QGap.vacuum_unique`       : the uniqueness of the vacuum is a CONSEQUENCE of the q-form plus
                               density, not an extra hypothesis.
-/

open MeasureTheory Filter Topology
open scoped ContDiff RealInnerProductSpace

noncomputable section

namespace ClayYM

variable {ι : Type} {d : ℕ}

/-! ### Formal operations on families -/

/-- Scaling of a test function by `c`. -/
def PosTest.smul [NeZero d] {n : ℕ} (c : ℝ) (f : PosTest d n) : PosTest d n where
  toFun := fun x => c * f x
  smooth := contDiff_const.mul f.smooth
  compact := HasCompactSupport.mul_left (f := fun _ => c) f.compact
  supp := tsupport_mul_subset_right.trans f.supp

/-- Scaling of a term (same number of points, same labels). -/
def Term.smul [NeZero d] (c : ℝ) (a : Term ι d) : Term ι d := ⟨a.n, a.labels, a.f.smul c⟩

/-- Scaling of a family (every term is scaled). -/
def Family.smul [NeZero d] (c : ℝ) (F : Family ι d) : Family ι d := F.map (Term.smul c)

/-- Formal operations on families: concatenation (formal sum), scaling, vacuum `vac`. -/
def famOps (ι : Type) (d : ℕ) [NeZero d] : Transfer.VecOps (Family ι d) where
  add := fun F G => F ++ G
  smul := Family.smul
  Ω := vac ι

variable [Fintype ι] [NeZero d]

lemma rpForm_append_left (R : CompRep ι d) (S : Schwinger ι d) (F F' G : Family ι d) (t : ℝ) :
    rpForm R S (F ++ F') G t = rpForm R S F G t + rpForm R S F' G t := by
  unfold rpForm
  rw [List.map_append, List.sum_append]

lemma rpForm_append_right (R : CompRep ι d) (S : Schwinger ι d) (F G G' : Family ι d) (t : ℝ) :
    rpForm R S F (G ++ G') t = rpForm R S F G t + rpForm R S F G' t := by
  unfold rpForm
  simp only [List.map_append, List.sum_append]
  exact List.sum_map_add

lemma term_integral_smul_left (R : CompRep ι d) (S : Schwinger ι d) (c : ℝ) (a b : Term ι d)
    (t : ℝ) :
    (∫ x, ∫ y, (Term.smul c a).f x * b.f y * rpKernel R S (Term.smul c a) b t x y) =
      c * ∫ x, ∫ y, a.f x * b.f y * rpKernel R S a b t x y := by
  rw [← integral_const_mul]
  congr 1
  ext x
  rw [← integral_const_mul]
  congr 1
  ext y
  show c * a.f x * b.f y * rpKernel R S a b t x y = c * (a.f x * b.f y * rpKernel R S a b t x y)
  ring

lemma term_integral_smul_right (R : CompRep ι d) (S : Schwinger ι d) (c : ℝ) (a b : Term ι d)
    (t : ℝ) :
    (∫ x, ∫ y, a.f x * (Term.smul c b).f y * rpKernel R S a (Term.smul c b) t x y) =
      c * ∫ x, ∫ y, a.f x * b.f y * rpKernel R S a b t x y := by
  rw [← integral_const_mul]
  congr 1
  ext x
  rw [← integral_const_mul]
  congr 1
  ext y
  show a.f x * (c * b.f y) * rpKernel R S a b t x y = c * (a.f x * b.f y * rpKernel R S a b t x y)
  ring

lemma rpForm_smul_left (R : CompRep ι d) (S : Schwinger ι d) (c : ℝ) (F G : Family ι d) (t : ℝ) :
    rpForm R S (Family.smul c F) G t = c * rpForm R S F G t := by
  unfold rpForm Family.smul
  rw [List.map_map, ← List.sum_map_mul_left]
  congr 1
  refine List.map_congr_left fun a _ => ?_
  simp only [Function.comp_apply]
  rw [← List.sum_map_mul_left]
  congr 1
  exact List.map_congr_left fun b _ => term_integral_smul_left R S c a b t

lemma rpForm_smul_right (R : CompRep ι d) (S : Schwinger ι d) (c : ℝ) (F G : Family ι d) (t : ℝ) :
    rpForm R S F (Family.smul c G) t = c * rpForm R S F G t := by
  unfold rpForm Family.smul
  rw [← List.sum_map_mul_left]
  congr 1
  refine List.map_congr_left fun a _ => ?_
  rw [List.map_map, ← List.sum_map_mul_left]
  congr 1
  exact List.map_congr_left fun b _ => term_integral_smul_right R S c a b t

/-- The OS form is bilinear for concatenation and scaling (no hypothesis on `S`). -/
theorem rpForm_isBilin (R : CompRep ι d) (S : Schwinger ι d) :
    Transfer.IsBilin (famOps ι d) (rpForm R S) where
  add_left := rpForm_append_left R S
  add_right := rpForm_append_right R S
  smul_left := rpForm_smul_left R S
  smul_right := rpForm_smul_right R S

/-- `⟨Ω, e^{-tH} Ω⟩ = S(∅)` for every `t`. -/
lemma rpForm_vac_vac (R : CompRep ι d) (S : Schwinger ι d) (t : ℝ) :
    rpForm R S (vac ι) (vac ι) t = S [] := by
  simp [rpForm, vac, vacTerm, vacTest, rpKernel, mkList, integral_const,
    volume_real_config_zero_univ]

lemma famOps_vac_vac (R : CompRep ι d) (S : Schwinger ι d) (hnorm : S [] = 1) :
    rpForm R S (famOps ι d).Ω (famOps ι d).Ω 0 = 1 := by
  show rpForm R S (vac ι) (vac ι) 0 = 1
  rw [rpForm_vac_vac, hnorm]

/-- `HasMassGap` is the abstract mass gap of the OS form. -/
theorem hasMassGap_iff_massGapOn (R : CompRep ι d) (S : Schwinger ι d) (Δ : ℝ) :
    HasMassGap R S Δ ↔ Transfer.MassGapOn (famOps ι d) (rpForm R S) Set.univ Δ :=
  ⟨fun h => ⟨h.1, fun F _ G _ t ht => h.2 F G t ht⟩,
   fun h => ⟨h.1, fun F G t ht => h.2 F (Set.mem_univ _) G (Set.mem_univ _) t ht⟩⟩

/-! ### The q-form of the gap -/

/-- Truncated family `v_A = A − ⟨Ω, A⟩ Ω`: the family `A` followed by the vacuum term scaled by
`−⟨Ω, A⟩ = −rpForm R S (vac ι) A 0`. -/
def truncFam (R : CompRep ι d) (S : Schwinger ι d) (A : Family ι d) : Family ι d :=
  A ++ Family.smul (-(rpForm R S (vac ι) A 0)) (vac ι)

/-- **Mass gap, q-form.** At the physical time `ℓ > 0`, with `0 < q < 1`:
`⟨v_A, e^{-ℓH} v_A⟩ ≤ q ‖v_A‖²` for every `A ∈ 𝒜₀`, i.e.
`rpForm R S (truncFam R S A) (truncFam R S A) ℓ ≤ q * rpForm R S (truncFam R S A) (truncFam R S A) 0`.
The gap statement is `∃ q, QGap R S 𝒜₀ ℓ q` (one `q` for all `A`). -/
def QGap (R : CompRep ι d) (S : Schwinger ι d) (𝒜₀ : Set (Family ι d)) (ℓ q : ℝ) : Prop :=
  0 < ℓ ∧ 0 < q ∧ q < 1 ∧ ∀ A ∈ 𝒜₀,
    rpForm R S (truncFam R S A) (truncFam R S A) ℓ ≤
      q * rpForm R S (truncFam R S A) (truncFam R S A) 0

/-- `QGap` is the abstract q-form of the OS form (definitional bridge; tripwire for mutations). -/
theorem qGap_iff_qGapOn (R : CompRep ι d) (S : Schwinger ι d) (𝒜₀ : Set (Family ι d)) (ℓ q : ℝ) :
    QGap R S 𝒜₀ ℓ q ↔ Transfer.QGapOn (famOps ι d) (rpForm R S) 𝒜₀ ℓ q :=
  Iff.rfl

/-- **Gap ⟹ q-form** (OS axioms only: normalisation and reflection positivity). -/
theorem HasMassGap.qGap {R : CompRep ι d} {S : Schwinger ι d} {Δ ℓ : ℝ} (hOS : OSAxioms R S)
    (h : HasMassGap R S Δ) (hℓ : 0 < ℓ) (𝒜₀ : Set (Family ι d)) :
    QGap R S 𝒜₀ ℓ (Real.exp (-(Δ * ℓ))) :=
  Transfer.MassGapOn.qGapOn (rpForm_isBilin R S) (famOps_vac_vac R S hOS.normalized)
    hOS.reflection_positive ((hasMassGap_iff_massGapOn R S Δ).1 h) hℓ 𝒜₀

/-! ### The named hypothesis -/

/-- **NAMED HYPOTHESIS: Osterwalder–Schrader reconstruction of the theory `(R, S)`** (Hilbert space
and transfer semigroup). NOT proved; used only as an explicit argument. -/
abbrev OSReconstruction (R : CompRep ι d) (S : Schwinger ι d) : Type 1 :=
  Transfer.Recon (famOps ι d) (rpForm R S)

/-- Density of the truncated classes of `𝒜₀` in `Ω^⊥` (cyclicity of the vacuum for `𝒜₀`). -/
def TruncDense {R : CompRep ι d} {S : Schwinger ι d} (rec : OSReconstruction R S)
    (𝒜₀ : Set (Family ι d)) : Prop :=
  ∀ w : rec.H, ⟪rec.ω, w⟫ = 0 → w ∈ closure (rec.cls '' (truncFam R S '' 𝒜₀))

/-- For `𝒜₀ = univ` (all families) the density is automatic. -/
theorem truncDense_univ {R : CompRep ι d} {S : Schwinger ι d} (rec : OSReconstruction R S) :
    TruncDense rec Set.univ :=
  rec.truncDense_univ (rpForm_isBilin R S)

/-- **q-form ⟹ gap** `Δ = −log q / ℓ` (named hypothesis `OSReconstruction`, plus density). -/
theorem QGap.hasMassGap {R : CompRep ι d} {S : Schwinger ι d} {𝒜₀ : Set (Family ι d)} {ℓ q : ℝ}
    (rec : OSReconstruction R S) (hnorm : S [] = 1) (h : QGap R S 𝒜₀ ℓ q)
    (hd : TruncDense rec 𝒜₀) : HasMassGap R S (-Real.log q / ℓ) :=
  (hasMassGap_iff_massGapOn R S _).2 (rec.massGapOn_of_qGapOn (famOps_vac_vac R S hnorm) h hd)

theorem QGap.hasMassGap_univ {R : CompRep ι d} {S : Schwinger ι d} {ℓ q : ℝ}
    (rec : OSReconstruction R S) (hnorm : S [] = 1) (h : QGap R S Set.univ ℓ q) :
    HasMassGap R S (-Real.log q / ℓ) :=
  h.hasMassGap rec hnorm (truncDense_univ rec)

/-- **Equivalence** of the two forms of the gap, for every fixed `ℓ > 0`. -/
theorem exists_hasMassGap_iff_exists_qGap {R : CompRep ι d} {S : Schwinger ι d}
    (hOS : OSAxioms R S) (rec : OSReconstruction R S) {ℓ : ℝ} (hℓ : 0 < ℓ) :
    (∃ Δ, HasMassGap R S Δ) ↔ ∃ q, QGap R S Set.univ ℓ q :=
  ⟨fun ⟨_, h⟩ => ⟨_, h.qGap hOS hℓ Set.univ⟩,
   fun ⟨_, h⟩ => ⟨_, h.hasMassGap_univ rec hOS.normalized⟩⟩

/-- The two constructions are inverse to each other: `Δ ↦ q = e^{−Δℓ} ↦ −log q / ℓ = Δ`. -/
lemma neg_log_exp_div {Δ ℓ : ℝ} (hℓ : 0 < ℓ) : -Real.log (Real.exp (-(Δ * ℓ))) / ℓ = Δ := by
  rw [Real.log_exp, neg_neg, mul_div_assoc, div_self hℓ.ne', mul_one]

/-- **Operator form** (named hypothesis): `HasMassGap R S Δ` ⟺
`0 < Δ ∧ ∀ t ≥ 0, ‖e^{-tH}(1 − P_Ω)‖ ≤ e^{-Δt}`. -/
theorem hasMassGap_iff_opNorm {R : CompRep ι d} {S : Schwinger ι d} (rec : OSReconstruction R S)
    (hnorm : S [] = 1) (Δ : ℝ) :
    HasMassGap R S Δ ↔ 0 < Δ ∧ ∀ t, 0 ≤ t → ‖(rec.T t).comp rec.perp‖ ≤ Real.exp (-(Δ * t)) :=
  (hasMassGap_iff_massGapOn R S Δ).trans (rec.massGapOn_univ_iff_opNorm (famOps_vac_vac R S hnorm) Δ)

/-- **Uniqueness of the vacuum** follows from the q-form and density (no extra hypothesis):
every vector fixed by `e^{-ℓH}` is a multiple of `Ω`. -/
theorem QGap.vacuum_unique {R : CompRep ι d} {S : Schwinger ι d} {𝒜₀ : Set (Family ι d)}
    {ℓ q : ℝ} (rec : OSReconstruction R S) (hnorm : S [] = 1) (h : QGap R S 𝒜₀ ℓ q)
    (hd : TruncDense rec 𝒜₀) (w : rec.H) (hw : rec.T ℓ w = w) : w = ⟪rec.ω, w⟫ • rec.ω :=
  rec.vacuum_unique (famOps_vac_vac R S hnorm) h hd w hw

/-! ### Closure lemma -/

/-- Pointwise ("simple") convergence of the Schwinger functions on `𝒜₀`: convergence of the
smeared values `⟪F, τ_t G⟫ = rpForm R (Sk k) F G t` for `F, G ∈ 𝒜₀ ∪ {Ω}` and `t ∈ {0, ℓ}`. -/
def SchwingerConvergesOn {α : Type*} (L : Filter α) (R : CompRep ι d) (Sk : α → Schwinger ι d)
    (S : Schwinger ι d) (𝒜₀ : Set (Family ι d)) (ℓ : ℝ) : Prop :=
  ∀ F ∈ insert (vac ι) 𝒜₀, ∀ G ∈ insert (vac ι) 𝒜₀, ∀ t ∈ ({0, ℓ} : Set ℝ),
    Tendsto (fun k => rpForm R (Sk k) F G t) L (𝓝 (rpForm R S F G t))

/-- **CLOSURE LEMMA.** If Schwinger functions converge pointwise on `𝒜₀` and (eventually) satisfy
the truncated inequality with the SAME `q`, their limit satisfies it. Any filter: sequences,
subsequences, nets. No OS axiom and no reconstruction is used. -/
theorem QGap.of_tendsto {α : Type*} {L : Filter α} [L.NeBot] {R : CompRep ι d}
    {Sk : α → Schwinger ι d} {S : Schwinger ι d} {𝒜₀ : Set (Family ι d)} {ℓ q : ℝ}
    (hconv : SchwingerConvergesOn L R Sk S 𝒜₀ ℓ) (h : ∀ᶠ k in L, QGap R (Sk k) 𝒜₀ ℓ q) :
    QGap R S 𝒜₀ ℓ q :=
  Transfer.QGapOn.of_tendsto (fun k => rpForm_isBilin R (Sk k)) (rpForm_isBilin R S) hconv h

/-- The normalisation `S(∅) = 1` passes to the limit. -/
theorem normalized_of_tendsto {α : Type*} {L : Filter α} [L.NeBot] {R : CompRep ι d}
    {Sk : α → Schwinger ι d} {S : Schwinger ι d} {𝒜₀ : Set (Family ι d)} {ℓ : ℝ}
    (hconv : SchwingerConvergesOn L R Sk S 𝒜₀ ℓ) (hn : ∀ᶠ k in L, Sk k [] = 1) : S [] = 1 := by
  have h := hconv (vac ι) (Set.mem_insert _ _) (vac ι) (Set.mem_insert _ _) 0 (by simp)
  simp only [rpForm_vac_vac] at h
  exact tendsto_nhds_unique h (tendsto_const_nhds.congr' (hn.mono fun k hk => hk.symm))

/-- **Closure + gap.** Approximants with the SAME `q`, converging pointwise on `𝒜₀`: the limit has
the mass gap `−log q / ℓ`, under the named hypothesis for the LIMIT theory and the density of the
truncated classes of `𝒜₀` (automatic for `𝒜₀ = univ`). -/
theorem hasMassGap_of_tendsto {α : Type*} {L : Filter α} [L.NeBot] {R : CompRep ι d}
    {Sk : α → Schwinger ι d} {S : Schwinger ι d} {𝒜₀ : Set (Family ι d)} {ℓ q : ℝ}
    (hconv : SchwingerConvergesOn L R Sk S 𝒜₀ ℓ) (hq : ∀ᶠ k in L, QGap R (Sk k) 𝒜₀ ℓ q)
    (hn : ∀ᶠ k in L, Sk k [] = 1) (rec : OSReconstruction R S) (hd : TruncDense rec 𝒜₀) :
    HasMassGap R S (-Real.log q / ℓ) :=
  (QGap.of_tendsto hconv hq).hasMassGap rec (normalized_of_tendsto hconv hn) hd

/-- **Closure + unique vacuum.** Same hypotheses: every vector of the limit theory fixed by
`e^{-ℓH}` is a multiple of `Ω`. No uniqueness of the vacuum is assumed. -/
theorem vacuum_unique_of_tendsto {α : Type*} {L : Filter α} [L.NeBot] {R : CompRep ι d}
    {Sk : α → Schwinger ι d} {S : Schwinger ι d} {𝒜₀ : Set (Family ι d)} {ℓ q : ℝ}
    (hconv : SchwingerConvergesOn L R Sk S 𝒜₀ ℓ) (hq : ∀ᶠ k in L, QGap R (Sk k) 𝒜₀ ℓ q)
    (hn : ∀ᶠ k in L, Sk k [] = 1) (rec : OSReconstruction R S) (hd : TruncDense rec 𝒜₀)
    (w : rec.H) (hw : rec.T ℓ w = w) : w = ⟪rec.ω, w⟫ • rec.ω :=
  (QGap.of_tendsto hconv hq).vacuum_unique rec (normalized_of_tendsto hconv hn) hd w hw

/-! ### Non-vacuity of the named hypothesis (trivial theory) -/

/-- The trivial theory has an OS reconstruction (`H = ℝ`, `e^{-tH} = 1`): the named hypothesis is
satisfiable (all its fields, completeness and strong continuity included). -/
def trivRecon (R : CompRep ι d) : OSReconstruction R (trivS ι d) where
  H := ℝ
  cls := trivAmp
  T := fun _ => ContinuousLinearMap.id ℝ ℝ
  inner_cls := by
    intro F G
    rw [rpForm_trivS]
    simp [mul_comm]
  inner_T := by
    intro F G t _
    rw [rpForm_trivS]
    simp [mul_comm]
  T_add := by
    intro s t _ _
    exact (ContinuousLinearMap.id_comp _).symm
  T_symm := by
    intro t _ x y
    simp
  T_contr := by
    intro t _
    exact ContinuousLinearMap.norm_id_le
  T_vac := by
    intro t _
    simp
  T_cont := by
    intro x
    exact tendsto_const_nhds
  dense := by
    apply Function.Surjective.denseRange
    intro r
    refine ⟨Family.smul r (vac ι), ?_⟩
    simp [trivAmp, Family.smul, vac, vacTerm, Term.smul, PosTest.smul, vacTest, integral_const,
      volume_real_config_zero_univ]

/-- The trivial theory satisfies the q-form for every `q ∈ (0,1)` (its truncated vectors vanish). -/
theorem trivS_qGap (R : CompRep ι d) {ℓ q : ℝ} (hℓ : 0 < ℓ) (hq : 0 < q) (hq1 : q < 1) :
    QGap R (trivS ι d) Set.univ ℓ q := by
  refine ⟨hℓ, hq, hq1, fun A _ => ?_⟩
  show rpForm R (trivS ι d) ((famOps ι d).trunc _ A) ((famOps ι d).trunc _ A) ℓ ≤
    q * rpForm R (trivS ι d) ((famOps ι d).trunc _ A) ((famOps ι d).trunc _ A) 0
  rw [(rpForm_isBilin R _).trunc_trunc, (rpForm_isBilin R _).trunc_trunc]
  simp only [Transfer.truncCorr, famOps, rpForm_trivS, trivAmp_vac]
  ring_nf
  exact le_refl _

/-- Sanity check of the whole conditional chain on the trivial theory: every hypothesis of
`QGap.hasMassGap_univ` is satisfiable simultaneously, and its conclusion agrees with
`trivS_hasMassGap`. -/
theorem trivS_conditional_chain (R : CompRep ι d) {ℓ q : ℝ} (hℓ : 0 < ℓ) (hq : 0 < q)
    (hq1 : q < 1) : HasMassGap R (trivS ι d) (-Real.log q / ℓ) :=
  (trivS_qGap R hℓ hq hq1).hasMassGap_univ (trivRecon R) (trivS_OSAxioms R).normalized

end ClayYM

end  -- ferme le 'noncomputable section' de ClayYM/GapQ.lean
end  -- ferme l'enveloppe

-- ===== CritereScalaire.lean (ce chantier) =====
noncomputable section
/-!
# Critère scalaire uniforme ⟹ forme q du trou de ClayYM (piste 1, chantier critere_scalaire_2026-11-11)

Ce fichier est compilé APRÈS les sources ClayYM v1.1 (Basic, OS, Gap, Fake/Trivial, Transfer, GapQ), recopiées
verbatim (imports retirés) en tête de `main.lean` par `assembler.sh`.

Contenu :
* §1  lemme scalaire FIN (p(2n) ≤ 2(eᵖ − 1)²) pour un spectre DÉNOMBRABLE (T-A ne l'avait qu'en spectre fini) ;
* §2  chaîne 4D fine : Δ₄(n) ≤ 2⁻⁹ ⟹ Δ₄(2n) ≤ 256 Δ₄(n)² (T-A : C₄(2⁻⁹) ≤ 247,3 sur papier ; ici 256, en Lean) ;
* §3  itération et trou de transfert : (λ_i/λ₀)ⁿ ≤ 256 Δ₄(n) ≤ 1/2 sur TOUTES les sections (2ᵏn)³ ;
* §4  la même chose en dimension 3 : Δ₃(n) ≤ 2⁻⁷ ⟹ Δ₃(2n) ≤ 64 Δ₃(n)² et (λ_i/λ₀)ⁿ ≤ 64 Δ₃(n) ≤ 1/2 ;
* §5  représentation spectrale de la forme OS (HYPOTHÈSE NOMMÉE `SpecLink`) ⟹ forme q ;
* §6  ASSEMBLAGE : critère uniforme le long d'une suite (filtre) + lien spectral + convergence des formes OS
      ⟹ la limite vérifie `QGapOn … ℓ (256 η)` (même q) ; variante tores carrés ; en termes ClayYM :
      `QGap R S univ ℓ (256 η)` et `HasMassGap R S (−log(256 η)/ℓ)` avec −log(256η)/ℓ ≥ (log 2)/ℓ.

Hypothèses nommées (aucun axiome) : symétrie de log Z (hs12, hs23, hs34) ; `HypSpecTC` (transfert positif à trace) ;
`SpecLink` / `LienTransfert4` (forme OS du cylindre = même transfert) ; `ConvergesOn` (sens exact de « limite ») ;
`OSReconstruction` de ClayYM pour la limite. Rien sur l'unicité de l'état de Gibbs ni de la limite.
-/

namespace CritereScalaire

open Real Filter Topology

/-! ## §1 Lemme scalaire fin, spectre dénombrable -/

/-- Queue excitée `s_n = Σ' r_i^n` (rapports λ_i/λ₀ des états excités). -/
noncomputable def sT (r : ℕ → ℝ) (n : ℕ) : ℝ := ∑' i, r i ^ n

/-- `p(n) = 2 log(1 + s_n) − log(1 + s_{2n})` (λ₀ se simplifie). -/
noncomputable def pT (r : ℕ → ℝ) (n : ℕ) : ℝ :=
  2 * Real.log (1 + sT r n) - Real.log (1 + sT r (2 * n))

lemma summable_pow_mono (r : ℕ → ℝ) (h0 : ∀ i, 0 ≤ r i) (h1 : ∀ i, r i ≤ 1) {n m : ℕ}
    (hnm : n ≤ m) (hs : Summable (fun i => r i ^ n)) : Summable (fun i => r i ^ m) :=
  Summable.of_nonneg_of_le (fun i => pow_nonneg (h0 i) m)
    (fun i => pow_le_pow_of_le_one (h0 i) (h1 i) hnm) hs

/-- **Lemme fin (spectre dénombrable).** p ≥ 0, chaque r_i^n ≤ s_n ≤ eᵖ − 1, et p(2n) ≤ 2(e^{p(n)} − 1)²,
SANS condition de petitesse. -/
theorem lemme_fin_tc (r : ℕ → ℝ) (h0 : ∀ i, 0 ≤ r i) (h1 : ∀ i, r i ≤ 1) (n : ℕ)
    (hsum : Summable (fun i => r i ^ n)) :
    0 ≤ pT r n ∧ sT r n ≤ Real.exp (pT r n) - 1 ∧ (∀ i, r i ^ n ≤ sT r n) ∧
      pT r (2 * n) ≤ 2 * (Real.exp (pT r n) - 1) ^ 2 := by
  have hsum2 : Summable (fun i => r i ^ (2 * n)) := summable_pow_mono r h0 h1 (by omega) hsum
  have hs : 0 ≤ sT r n := tsum_nonneg (fun i => pow_nonneg (h0 i) n)
  have hs2 : 0 ≤ sT r (2 * n) := tsum_nonneg (fun i => pow_nonneg (h0 i) (2 * n))
  have hs4 : 0 ≤ sT r (2 * (2 * n)) := tsum_nonneg (fun i => pow_nonneg (h0 i) (2 * (2 * n)))
  have h21 : sT r (2 * n) ≤ sT r n :=
    Summable.tsum_le_tsum (fun i => pow_le_pow_of_le_one (h0 i) (h1 i) (by omega)) hsum2 hsum
  have hterm : ∀ j, r j ^ n ≤ sT r n := fun j =>
    hsum.le_tsum j (fun i _ => pow_nonneg (h0 i) n)
  have h2sq : sT r (2 * n) ≤ (sT r n) ^ 2 := by
    calc sT r (2 * n) = ∑' i, r i ^ n * r i ^ n := by
          unfold sT; congr 1; funext i; rw [two_mul, pow_add]
      _ ≤ ∑' i, r i ^ n * sT r n := by
          apply Summable.tsum_le_tsum
          · intro i; exact mul_le_mul_of_nonneg_left (hterm i) (pow_nonneg (h0 i) n)
          · refine hsum2.congr (fun i => ?_); rw [two_mul, pow_add]
          · exact hsum.mul_right _
      _ = (sT r n) ^ 2 := by rw [tsum_mul_right]; unfold sT; ring
  have hpdef : pT r n = 2 * Real.log (1 + sT r n) - Real.log (1 + sT r (2 * n)) := rfl
  have hp2def : pT r (2 * n) =
      2 * Real.log (1 + sT r (2 * n)) - Real.log (1 + sT r (2 * (2 * n))) := rfl
  have hlog1 : Real.log (1 + sT r (2 * n)) ≤ Real.log (1 + sT r n) :=
    Real.log_le_log (by linarith) (by linarith)
  have hl0 : 0 ≤ Real.log (1 + sT r n) := Real.log_nonneg (by linarith)
  have hp_ge : Real.log (1 + sT r n) ≤ pT r n := by rw [hpdef]; linarith
  have hsE : sT r n ≤ Real.exp (pT r n) - 1 := by
    have : 1 + sT r n ≤ Real.exp (pT r n) := by
      calc 1 + sT r n = Real.exp (Real.log (1 + sT r n)) := (Real.exp_log (by linarith)).symm
        _ ≤ Real.exp (pT r n) := Real.exp_le_exp.mpr hp_ge
    linarith
  refine ⟨by linarith, hsE, hterm, ?_⟩
  have e1 : Real.log (1 + sT r (2 * n)) ≤ sT r (2 * n) := by
    have := Real.log_le_sub_one_of_pos (show 0 < 1 + sT r (2 * n) by linarith); linarith
  have e2 : 0 ≤ Real.log (1 + sT r (2 * (2 * n))) := Real.log_nonneg (by linarith)
  have hsq : (sT r n) ^ 2 ≤ (Real.exp (pT r n) - 1) ^ 2 := pow_le_pow_left₀ hs hsE 2
  rw [hp2def]
  nlinarith

/-- Majoration polynomiale : e^x − 1 ≤ x + x² sur [0,1]. -/
lemma expm1_le (x : ℝ) (h0 : 0 ≤ x) (h1 : x ≤ 1) : Real.exp x - 1 ≤ x + x ^ 2 := by
  have h := Real.abs_exp_sub_one_sub_id_le (x := x) (by rw [abs_of_nonneg h0]; exact h1)
  have := (abs_le.mp h).2
  linarith

lemma expm1_nonneg (x : ℝ) (h0 : 0 ≤ x) : 0 ≤ Real.exp x - 1 := by
  have := Real.add_one_le_exp x; linarith

lemma f_le (x : ℝ) (h0 : 0 ≤ x) (h1 : x ≤ 1) :
    2 * (Real.exp x - 1) ^ 2 ≤ 2 * (x + x ^ 2) ^ 2 := by
  have := pow_le_pow_left₀ (expm1_nonneg x h0) (expm1_le x h0 h1) 2
  linarith

/-- Pas élémentaire de la chaîne : si `0 ≤ B ≤ c·D`, `D ≤ δ`, `c·δ ≤ 1` et `A ≤ 2(e^B − 1)²`, alors
`A ≤ 2 c²(1 + cδ)² D²`. -/
lemma pas_chaine (A B D c δ : ℝ) (hD0 : 0 ≤ D) (hDδ : D ≤ δ) (hc0 : 0 ≤ c) (hcδ : c * δ ≤ 1)
    (hB0 : 0 ≤ B) (hB : B ≤ c * D) (hA : A ≤ 2 * (Real.exp B - 1) ^ 2) :
    A ≤ 2 * (c * (1 + c * δ)) ^ 2 * D ^ 2 := by
  have hcD : c * D ≤ 1 := le_trans (mul_le_mul_of_nonneg_left hDδ hc0) hcδ
  have hf := f_le B hB0 (le_trans hB hcD)
  have hBB : B ^ 2 ≤ (c * D) * (c * δ) := by
    have h1 : B * B ≤ (c * D) * (c * D) := mul_le_mul hB hB hB0 (by positivity)
    have h2 : (c * D) * (c * D) ≤ (c * D) * (c * δ) :=
      mul_le_mul_of_nonneg_left (mul_le_mul_of_nonneg_left hDδ hc0) (by positivity)
    nlinarith
  have hsum : B + B ^ 2 ≤ c * (1 + c * δ) * D := by nlinarith
  have hsq : (B + B ^ 2) ^ 2 ≤ (c * (1 + c * δ) * D) ^ 2 :=
    pow_le_pow_left₀ (by positivity) hsum 2
  have e : (c * (1 + c * δ) * D) ^ 2 = (c * (1 + c * δ)) ^ 2 * D ^ 2 := by ring
  nlinarith

/-! ## §2 Chaîne 4D fine -/

/-- Défaut de doublement dans la 4ᵉ direction. -/
def Q (F : ℕ → ℕ → ℕ → ℕ → ℝ) (a b c d : ℕ) : ℝ := 2 * F a b c d - F a b c (2 * d)

/-- Δ₄(n) = 16 log Z(n⁴) − log Z((2n)⁴). -/
def Delta (F : ℕ → ℕ → ℕ → ℕ → ℝ) (n : ℕ) : ℝ :=
  16 * F n n n n - F (2 * n) (2 * n) (2 * n) (2 * n)

/-- Partie numérique de la chaîne fine 4D : seuil 2⁻⁹, constante 256. -/
lemma chaine_num_fin4 (D B0 B1 B2 B3 A0 A1 A2 A3 : ℝ) (hD0 : 0 ≤ D) (hD : D ≤ 1 / 512)
    (hB0n : 0 ≤ B0) (hB1n : 0 ≤ B1) (hB2n : 0 ≤ B2) (hB3n : 0 ≤ B3)
    (hB0 : B0 ≤ D)
    (hA0 : A0 ≤ 2 * (Real.exp B0 - 1) ^ 2) (hB1 : B1 ≤ 2 * B0 + A0)
    (hA1 : A1 ≤ 2 * (Real.exp B1 - 1) ^ 2) (hB2 : B2 ≤ 2 * B1 + A1)
    (hA2 : A2 ≤ 2 * (Real.exp B2 - 1) ^ 2) (hB3 : B3 ≤ 2 * B2 + A2)
    (hA3 : A3 ≤ 2 * (Real.exp B3 - 1) ^ 2) :
    8 * A0 + 4 * A1 + 2 * A2 + A3 ≤ 256 * D ^ 2 := by
  have hDD : D ^ 2 ≤ D / 512 := by nlinarith
  have a0 := pas_chaine A0 B0 D 1 (1 / 512) hD0 hD (by norm_num) (by norm_num) hB0n (by linarith) hA0
  have a0' : A0 ≤ 2008 / 1000 * D ^ 2 := by
    norm_num at a0
    nlinarith [sq_nonneg D]
  have b1 : B1 ≤ 2004 / 1000 * D := by nlinarith
  have a1 := pas_chaine A1 B1 D (2004 / 1000) (1 / 512) hD0 hD (by norm_num) (by norm_num) hB1n b1 hA1
  have a1' : A1 ≤ 8096 / 1000 * D ^ 2 := by
    norm_num at a1
    nlinarith [sq_nonneg D]
  have b2 : B2 ≤ 4024 / 1000 * D := by nlinarith
  have a2 := pas_chaine A2 B2 D (4024 / 1000) (1 / 512) hD0 hD (by norm_num) (by norm_num) hB2n b2 hA2
  have a2' : A2 ≤ 329 / 10 * D ^ 2 := by
    norm_num at a2
    nlinarith [sq_nonneg D]
  have b3 : B3 ≤ 8113 / 1000 * D := by nlinarith
  have a3 := pas_chaine A3 B3 D (8113 / 1000) (1 / 512) hD0 hD (by norm_num) (by norm_num) hB3n b3 hA3
  have a3' : A3 ≤ 1359 / 10 * D ^ 2 := by
    norm_num at a3
    nlinarith [sq_nonneg D]
  nlinarith

/-- Décomposition (D) et positivité : Δ₄(n) ≥ 0, Q(n⁴) ≤ Δ₄(n)/8, Q(2n,2n,2n | n) ≤ Δ₄(n). -/
theorem decomp_4d (F : ℕ → ℕ → ℕ → ℕ → ℝ)
    (hs12 : ∀ a b c d, F a b c d = F b a c d)
    (hs23 : ∀ a b c d, F a b c d = F a c b d)
    (hs34 : ∀ a b c d, F a b c d = F a b d c)
    (hpos : ∀ a b c d, 0 < a → 0 < b → 0 < c → 0 < d → 0 ≤ Q F a b c d)
    (n : ℕ) (hn : 0 < n) :
    0 ≤ Delta F n ∧ Q F n n n n ≤ Delta F n / 8 ∧ Q F (2 * n) (2 * n) (2 * n) n ≤ Delta F n := by
  have h2 : 0 < 2 * n := by omega
  unfold Q at hpos ⊢
  unfold Delta
  have e1 : F (2 * n) n n n = F n n n (2 * n) := (hs12 (2 * n) n n n).trans ((hs23 n (2 * n) n n).trans ((hs34 n n (2 * n) n)))
  have e2 : F (2 * n) n n (2 * n) = F n n (2 * n) (2 * n) := (hs12 (2 * n) n n (2 * n)).trans ((hs23 n (2 * n) n (2 * n)))
  have e3 : F (2 * n) (2 * n) n n = F n n (2 * n) (2 * n) := (hs23 (2 * n) (2 * n) n n).trans ((hs12 (2 * n) n (2 * n) n).trans ((hs34 n (2 * n) (2 * n) n).trans ((hs23 n (2 * n) n (2 * n)))))
  have e4 : F (2 * n) (2 * n) n (2 * n) = F n (2 * n) (2 * n) (2 * n) := (hs23 (2 * n) (2 * n) n (2 * n)).trans ((hs12 (2 * n) n (2 * n) (2 * n)))
  have e5 : F (2 * n) (2 * n) (2 * n) n = F n (2 * n) (2 * n) (2 * n) := (hs34 (2 * n) (2 * n) (2 * n) n).trans ((hs23 (2 * n) (2 * n) n (2 * n)).trans ((hs12 (2 * n) n (2 * n) (2 * n))))
  have q1 := hpos n n n n hn hn hn hn
  have q2 := hpos (2 * n) n n n h2 hn hn hn
  have q3 := hpos (2 * n) (2 * n) n n h2 h2 hn hn
  have q4 := hpos (2 * n) (2 * n) (2 * n) n h2 h2 h2 hn
  have hdec : 16 * F n n n n - F (2 * n) (2 * n) (2 * n) (2 * n) =
      8 * (2 * F n n n n - F n n n (2 * n)) + 4 * (2 * F (2 * n) n n n - F (2 * n) n n (2 * n)) +
      2 * (2 * F (2 * n) (2 * n) n n - F (2 * n) (2 * n) n (2 * n)) + (2 * F (2 * n) (2 * n) (2 * n) n - F (2 * n) (2 * n) (2 * n) (2 * n)) := by
    rw [e1, e2, e3, e4, e5]; ring
  refine ⟨?_, ?_, ?_⟩
  · rw [hdec]; linarith
  · rw [hdec]; linarith
  · rw [hdec]; linarith

/-- **Doublement 4D fin** : Δ₄(n) ≤ 2⁻⁹ ⟹ Δ₄(2n) ≤ 256 Δ₄(n)². Hypothèses : symétrie de F = log Z, positivité
du défaut et lemme fin dans la 4ᵉ direction (fournis par `HypSpecTC`). -/
theorem doublement_fin_4d (F : ℕ → ℕ → ℕ → ℕ → ℝ)
    (hs12 : ∀ a b c d, F a b c d = F b a c d)
    (hs23 : ∀ a b c d, F a b c d = F a c b d)
    (hs34 : ∀ a b c d, F a b c d = F a b d c)
    (hpos : ∀ a b c d, 0 < a → 0 < b → 0 < c → 0 < d → 0 ≤ Q F a b c d)
    (hsq : ∀ a b c d, 0 < a → 0 < b → 0 < c → 0 < d →
      Q F a b c (2 * d) ≤ 2 * (Real.exp (Q F a b c d) - 1) ^ 2)
    (n : ℕ) (hn : 0 < n) (hD : Delta F n ≤ 1 / 512) :
    Delta F (2 * n) ≤ 256 * (Delta F n) ^ 2 := by
  obtain ⟨hD0, -, hB0⟩ := decomp_4d F hs12 hs23 hs34 hpos n hn
  have h2 : 0 < 2 * n := by omega
  have h4 : 0 < 2 * (2 * n) := by omega
  unfold Q at hpos hsq hB0
  unfold Delta at hD hD0 hB0 ⊢
  have e5 : F (2 * n) (2 * n) (2 * n) n = F n (2 * n) (2 * n) (2 * n) := (hs34 (2 * n) (2 * n) (2 * n) n).trans ((hs23 (2 * n) (2 * n) n (2 * n)).trans ((hs12 (2 * n) n (2 * n) (2 * n))))
  have e6 : F (2 * (2 * n)) (2 * n) (2 * n) n = F n (2 * n) (2 * n) (2 * (2 * n)) := (hs12 (2 * (2 * n)) (2 * n) (2 * n) n).trans ((hs23 (2 * n) (2 * (2 * n)) (2 * n) n).trans ((hs34 (2 * n) (2 * n) (2 * (2 * n)) n).trans ((hs23 (2 * n) (2 * n) n (2 * (2 * n))).trans ((hs12 (2 * n) n (2 * n) (2 * (2 * n)))))))
  have e7 : F (2 * n) (2 * n) (2 * n) (2 * (2 * n)) = F (2 * (2 * n)) (2 * n) (2 * n) (2 * n) := (hs34 (2 * n) (2 * n) (2 * n) (2 * (2 * n))).trans ((hs23 (2 * n) (2 * n) (2 * (2 * n)) (2 * n)).trans ((hs12 (2 * n) (2 * (2 * n)) (2 * n) (2 * n))))
  have e8 : F (2 * (2 * n)) (2 * n) (2 * n) n = F (2 * (2 * n)) n (2 * n) (2 * n) := (hs34 (2 * (2 * n)) (2 * n) (2 * n) n).trans ((hs23 (2 * (2 * n)) (2 * n) n (2 * n)))
  have e9 : F (2 * (2 * n)) (2 * (2 * n)) (2 * n) n = F (2 * (2 * n)) n (2 * n) (2 * (2 * n)) := (hs23 (2 * (2 * n)) (2 * (2 * n)) (2 * n) n).trans ((hs34 (2 * (2 * n)) (2 * n) (2 * (2 * n)) n).trans ((hs23 (2 * (2 * n)) (2 * n) n (2 * (2 * n)))))
  have e10 : F (2 * (2 * n)) (2 * n) (2 * n) (2 * (2 * n)) = F (2 * (2 * n)) (2 * (2 * n)) (2 * n) (2 * n) := (hs34 (2 * (2 * n)) (2 * n) (2 * n) (2 * (2 * n))).trans ((hs23 (2 * (2 * n)) (2 * n) (2 * (2 * n)) (2 * n)))
  have e11 : F (2 * (2 * n)) (2 * (2 * n)) (2 * n) n = F (2 * (2 * n)) (2 * (2 * n)) n (2 * n) := (hs34 (2 * (2 * n)) (2 * (2 * n)) (2 * n) n)
  have e12 : F (2 * (2 * n)) (2 * (2 * n)) n (2 * (2 * n)) = F (2 * (2 * n)) (2 * (2 * n)) (2 * (2 * n)) n := (hs34 (2 * (2 * n)) (2 * (2 * n)) n (2 * (2 * n)))
  have e13 : F (2 * (2 * n)) (2 * (2 * n)) (2 * n) (2 * (2 * n)) = F (2 * (2 * n)) (2 * (2 * n)) (2 * (2 * n)) (2 * n) := (hs34 (2 * (2 * n)) (2 * (2 * n)) (2 * n) (2 * (2 * n)))
  have xA := hpos n (2 * n) (2 * n) (2 * n) hn h2 h2 h2
  have xB := hpos (2 * (2 * n)) n (2 * n) (2 * n) h4 hn h2 h2
  have xC := hpos (2 * (2 * n)) (2 * (2 * n)) n (2 * n) h4 h4 hn h2
  have hB0n := hpos (2 * n) (2 * n) (2 * n) n h2 h2 h2 hn
  have hB1n := hpos (2 * (2 * n)) (2 * n) (2 * n) n h4 h2 h2 hn
  have hB2n := hpos (2 * (2 * n)) (2 * (2 * n)) (2 * n) n h4 h4 h2 hn
  have hB3n := hpos (2 * (2 * n)) (2 * (2 * n)) (2 * (2 * n)) n h4 h4 h4 hn
  have hA0 := hsq (2 * n) (2 * n) (2 * n) n h2 h2 h2 hn
  have hA1 := hsq (2 * (2 * n)) (2 * n) (2 * n) n h4 h2 h2 hn
  have hA2 := hsq (2 * (2 * n)) (2 * (2 * n)) (2 * n) n h4 h4 h2 hn
  have hA3 := hsq (2 * (2 * n)) (2 * (2 * n)) (2 * (2 * n)) n h4 h4 h4 hn
  have hD2 : 16 * F (2 * n) (2 * n) (2 * n) (2 * n) - F (2 * (2 * n)) (2 * (2 * n)) (2 * (2 * n)) (2 * (2 * n)) =
      8 * (2 * F (2 * n) (2 * n) (2 * n) (2 * n) - F (2 * n) (2 * n) (2 * n) (2 * (2 * n))) + 4 * (2 * F (2 * (2 * n)) (2 * n) (2 * n) (2 * n) - F (2 * (2 * n)) (2 * n) (2 * n) (2 * (2 * n))) +
      2 * (2 * F (2 * (2 * n)) (2 * (2 * n)) (2 * n) (2 * n) - F (2 * (2 * n)) (2 * (2 * n)) (2 * n) (2 * (2 * n))) + (2 * F (2 * (2 * n)) (2 * (2 * n)) (2 * (2 * n)) (2 * n) - F (2 * (2 * n)) (2 * (2 * n)) (2 * (2 * n)) (2 * (2 * n))) := by
    rw [e7, e10, e13]; ring
  have hB1 : 2 * F (2 * (2 * n)) (2 * n) (2 * n) n - F (2 * (2 * n)) (2 * n) (2 * n) (2 * n) ≤
      2 * (2 * F (2 * n) (2 * n) (2 * n) n - F (2 * n) (2 * n) (2 * n) (2 * n)) + (2 * F (2 * n) (2 * n) (2 * n) (2 * n) - F (2 * n) (2 * n) (2 * n) (2 * (2 * n))) := by
    have r : 2 * F (2 * (2 * n)) (2 * n) (2 * n) n - F (2 * (2 * n)) (2 * n) (2 * n) (2 * n) = 2 * (2 * F (2 * n) (2 * n) (2 * n) n - F (2 * n) (2 * n) (2 * n) (2 * n))
        - 2 * (2 * F n (2 * n) (2 * n) (2 * n) - F n (2 * n) (2 * n) (2 * (2 * n))) + (2 * F (2 * n) (2 * n) (2 * n) (2 * n) - F (2 * n) (2 * n) (2 * n) (2 * (2 * n))) := by
      rw [e5, e6, e7]; ring
    linarith
  have hB2 : 2 * F (2 * (2 * n)) (2 * (2 * n)) (2 * n) n - F (2 * (2 * n)) (2 * (2 * n)) (2 * n) (2 * n) ≤
      2 * (2 * F (2 * (2 * n)) (2 * n) (2 * n) n - F (2 * (2 * n)) (2 * n) (2 * n) (2 * n)) + (2 * F (2 * (2 * n)) (2 * n) (2 * n) (2 * n) - F (2 * (2 * n)) (2 * n) (2 * n) (2 * (2 * n))) := by
    have r : 2 * F (2 * (2 * n)) (2 * (2 * n)) (2 * n) n - F (2 * (2 * n)) (2 * (2 * n)) (2 * n) (2 * n) = 2 * (2 * F (2 * (2 * n)) (2 * n) (2 * n) n - F (2 * (2 * n)) (2 * n) (2 * n) (2 * n))
        - 2 * (2 * F (2 * (2 * n)) n (2 * n) (2 * n) - F (2 * (2 * n)) n (2 * n) (2 * (2 * n))) + (2 * F (2 * (2 * n)) (2 * n) (2 * n) (2 * n) - F (2 * (2 * n)) (2 * n) (2 * n) (2 * (2 * n))) := by
      rw [e8, e9, e10]; ring
    linarith
  have hB3 : 2 * F (2 * (2 * n)) (2 * (2 * n)) (2 * (2 * n)) n - F (2 * (2 * n)) (2 * (2 * n)) (2 * (2 * n)) (2 * n) ≤
      2 * (2 * F (2 * (2 * n)) (2 * (2 * n)) (2 * n) n - F (2 * (2 * n)) (2 * (2 * n)) (2 * n) (2 * n)) + (2 * F (2 * (2 * n)) (2 * (2 * n)) (2 * n) (2 * n) - F (2 * (2 * n)) (2 * (2 * n)) (2 * n) (2 * (2 * n))) := by
    have r : 2 * F (2 * (2 * n)) (2 * (2 * n)) (2 * (2 * n)) n - F (2 * (2 * n)) (2 * (2 * n)) (2 * (2 * n)) (2 * n) = 2 * (2 * F (2 * (2 * n)) (2 * (2 * n)) (2 * n) n - F (2 * (2 * n)) (2 * (2 * n)) (2 * n) (2 * n))
        - 2 * (2 * F (2 * (2 * n)) (2 * (2 * n)) n (2 * n) - F (2 * (2 * n)) (2 * (2 * n)) n (2 * (2 * n))) + (2 * F (2 * (2 * n)) (2 * (2 * n)) (2 * n) (2 * n) - F (2 * (2 * n)) (2 * (2 * n)) (2 * n) (2 * (2 * n))) := by
      rw [e11, e12, e13]; ring
    linarith
  rw [hD2]
  exact chaine_num_fin4 _ _ _ _ _ _ _ _ _ hD0 hD hB0n hB1n hB2n hB3n hB0 hA0 hB1 hA1 hB2 hA2 hB3 hA3

/-! ## §3 Itération et trou de transfert (4D) -/

/-- Itération : si d_{k+1} ≤ 256 d_k² dès que d_k ≤ 2⁻⁹, alors 256 d_k ≤ (256 d₀)^(2^k). -/
theorem iteration256 (d : ℕ → ℝ) (hnn : ∀ k, 0 ≤ d k)
    (hstep : ∀ k, d k ≤ 1 / 512 → d (k + 1) ≤ 256 * d k ^ 2) (h0 : d 0 ≤ 1 / 512) :
    ∀ k, 256 * d k ≤ (256 * d 0) ^ (2 ^ k) := by
  intro k
  induction k with
  | zero => simp
  | succ k ih =>
    have hq : 256 * d 0 ≤ 1 / 2 := by linarith
    have hq0 : 0 ≤ 256 * d 0 := by linarith [hnn 0]
    have hpow : (256 * d 0) ^ (2 ^ k) ≤ 256 * d 0 :=
      pow_le_of_le_one hq0 (by linarith) (by positivity)
    have hdk : d k ≤ 1 / 512 := by linarith
    have h1 := hstep k hdk
    have h2 : (256 * d k) ^ 2 ≤ ((256 * d 0) ^ (2 ^ k)) ^ 2 :=
      pow_le_pow_left₀ (by linarith [hnn k]) ih 2
    calc 256 * d (k + 1) ≤ 256 * (256 * d k ^ 2) := by linarith
      _ = (256 * d k) ^ 2 := by ring
      _ ≤ ((256 * d 0) ^ (2 ^ k)) ^ 2 := h2
      _ = (256 * d 0) ^ (2 ^ (k + 1)) := by rw [← pow_mul, pow_succ]

/-- Structure de transfert à trace dans la 4ᵉ direction, tailles > 0 (identique à P2 `HypSpecTC`). -/
def HypSpecTC (F : ℕ → ℕ → ℕ → ℕ → ℝ) : Prop :=
  ∀ a b c : ℕ, 0 < a → 0 < b → 0 < c →
    ∃ (r : ℕ → ℝ) (L : ℝ), (∀ i, 0 ≤ r i) ∧ (∀ i, r i ≤ 1) ∧
      (∀ d : ℕ, 0 < d → Summable (fun i => r i ^ d)) ∧
      ∀ d : ℕ, 0 < d → F a b c d = (d : ℝ) * L + Real.log (1 + sT r d)

lemma Q_eq_pT (F : ℕ → ℕ → ℕ → ℕ → ℝ) (a b c : ℕ) (r : ℕ → ℝ) (L : ℝ)
    (hF : ∀ d : ℕ, 0 < d → F a b c d = (d : ℝ) * L + Real.log (1 + sT r d)) (d : ℕ)
    (hd : 0 < d) : Q F a b c d = pT r d := by
  unfold Q pT
  rw [hF d hd, hF (2 * d) (by omega)]
  push_cast
  ring

lemma hyp_of_specTC (F : ℕ → ℕ → ℕ → ℕ → ℝ) (hF : HypSpecTC F) :
    (∀ a b c d, 0 < a → 0 < b → 0 < c → 0 < d → 0 ≤ Q F a b c d) ∧
    (∀ a b c d, 0 < a → 0 < b → 0 < c → 0 < d →
      Q F a b c (2 * d) ≤ 2 * (Real.exp (Q F a b c d) - 1) ^ 2) := by
  constructor
  · intro a b c d ha hb hc hd
    obtain ⟨r, L, h0, h1, hs, hF⟩ := hF a b c ha hb hc
    rw [Q_eq_pT F a b c r L hF d hd]
    exact (lemme_fin_tc r h0 h1 d (hs d hd)).1
  · intro a b c d ha hb hc hd
    obtain ⟨r, L, h0, h1, hs, hF⟩ := hF a b c ha hb hc
    rw [Q_eq_pT F a b c r L hF (2 * d) (by omega), Q_eq_pT F a b c r L hF d hd]
    exact (lemme_fin_tc r h0 h1 d (hs d hd)).2.2.2

/-- **Trou de transfert 4D (constantes fines).** Si Δ₄(n) ≤ 2⁻⁹, alors pour tout k, sur la section (2ᵏn)³,
tout rapport excité r_i = λ_i/λ₀ du transfert vérifie r_iⁿ ≤ 256 Δ₄(n) (≤ 1/2), soit un trou ≥ −log(256Δ₄(n))/n. -/
theorem gap_4d_fin (F : ℕ → ℕ → ℕ → ℕ → ℝ)
    (hs12 : ∀ a b c d, F a b c d = F b a c d)
    (hs23 : ∀ a b c d, F a b c d = F a c b d)
    (hs34 : ∀ a b c d, F a b c d = F a b d c)
    (hF : HypSpecTC F) (n : ℕ) (hn : 0 < n) (hD : Delta F n ≤ 1 / 512) (k : ℕ)
    (r : ℕ → ℝ) (L : ℝ) (h0 : ∀ i, 0 ≤ r i) (h1 : ∀ i, r i ≤ 1)
    (hs : ∀ d : ℕ, 0 < d → Summable (fun i => r i ^ d))
    (hFm : ∀ d : ℕ, 0 < d →
      F (2 ^ k * n) (2 ^ k * n) (2 ^ k * n) d = (d : ℝ) * L + Real.log (1 + sT r d)) :
    ∀ i, r i ^ n ≤ 256 * Delta F n := by
  obtain ⟨hpos, hsq⟩ := hyp_of_specTC F hF
  have hnn : ∀ k, 0 ≤ Delta F (2 ^ k * n) := fun k =>
    (decomp_4d F hs12 hs23 hs34 hpos _ (by positivity)).1
  have hit : ∀ k, 256 * Delta F (2 ^ k * n) ≤ (256 * Delta F (2 ^ 0 * n)) ^ (2 ^ k) := by
    apply iteration256 (fun k => Delta F (2 ^ k * n)) hnn
    · intro k hk
      have := doublement_fin_4d F hs12 hs23 hs34 hpos hsq _ (by positivity) hk
      have e : 2 ^ (k + 1) * n = 2 * (2 ^ k * n) := by ring
      simp only [e]
      exact this
    · simpa using hD
  have e0 : 2 ^ 0 * n = n := by simp
  rw [e0] at hit
  intro i
  set m := 2 ^ k * n with hm
  have hm0 : 0 < m := by positivity
  have hD0 : 0 ≤ Delta F n := (decomp_4d F hs12 hs23 hs34 hpos n hn).1
  have hq : 256 * Delta F n ≤ 1 / 2 := by linarith
  have hk := hit k
  have hpowle : (256 * Delta F n) ^ (2 ^ k) ≤ 256 * Delta F n :=
    pow_le_of_le_one (by linarith) (by linarith) (by positivity)
  have hDm0 : 0 ≤ Delta F m := hnn k
  have hDm : Delta F m ≤ 1 / 512 := by linarith
  obtain ⟨-, hq8, -⟩ := decomp_4d F hs12 hs23 hs34 hpos m hm0
  have hQ : Q F m m m m = pT r m := Q_eq_pT F m m m r L hFm m hm0
  obtain ⟨hp0, hsE, hterm, -⟩ := lemme_fin_tc r h0 h1 m (hs m hm0)
  have hp : pT r m ≤ Delta F m / 8 := by rw [← hQ]; exact hq8
  have hp1 : pT r m ≤ 1 := by linarith
  have hexp := expm1_le (pT r m) hp0 hp1
  have hpp : pT r m ^ 2 ≤ pT r m := by nlinarith
  have hri : r i ^ m ≤ Delta F m / 4 := by
    have := hterm i; linarith
  have hri' : (r i ^ n) ^ (2 ^ k) ≤ (256 * Delta F n) ^ (2 ^ k) := by
    rw [← pow_mul, mul_comm n (2 ^ k), ← hm]
    linarith
  exact (pow_le_pow_iff_left₀ (pow_nonneg (h0 i) n) (by linarith) (by positivity)).mp hri'

/-! ## §4 Dimension 3 -/

/-- Défaut de doublement dans la 3ᵉ direction. -/
def Q3 (F : ℕ → ℕ → ℕ → ℝ) (a b c : ℕ) : ℝ := 2 * F a b c - F a b (2 * c)

/-- Δ₃(n) = 8 log Z(n³) − log Z((2n)³). -/
def Delta3 (F : ℕ → ℕ → ℕ → ℝ) (n : ℕ) : ℝ := 8 * F n n n - F (2 * n) (2 * n) (2 * n)

lemma chaine_num_fin3 (D B0 B1 B2 A0 A1 A2 : ℝ) (hD0 : 0 ≤ D) (hD : D ≤ 1 / 128)
    (hB0n : 0 ≤ B0) (hB1n : 0 ≤ B1) (hB2n : 0 ≤ B2)
    (hB0 : B0 ≤ D)
    (hA0 : A0 ≤ 2 * (Real.exp B0 - 1) ^ 2) (hB1 : B1 ≤ 2 * B0 + A0)
    (hA1 : A1 ≤ 2 * (Real.exp B1 - 1) ^ 2) (hB2 : B2 ≤ 2 * B1 + A1)
    (hA2 : A2 ≤ 2 * (Real.exp B2 - 1) ^ 2) :
    4 * A0 + 2 * A1 + A2 ≤ 64 * D ^ 2 := by
  have hDD : D ^ 2 ≤ D / 128 := by nlinarith
  have a0 := pas_chaine A0 B0 D 1 (1 / 128) hD0 hD (by norm_num) (by norm_num) hB0n (by linarith) hA0
  have a0' : A0 ≤ 2032 / 1000 * D ^ 2 := by
    norm_num at a0
    nlinarith [sq_nonneg D]
  have b1 : B1 ≤ 2016 / 1000 * D := by nlinarith
  have a1 := pas_chaine A1 B1 D (2016 / 1000) (1 / 128) hD0 hD (by norm_num) (by norm_num) hB1n b1 hA1
  have a1' : A1 ≤ 8387 / 1000 * D ^ 2 := by
    norm_num at a1
    nlinarith [sq_nonneg D]
  have b2 : B2 ≤ 4098 / 1000 * D := by nlinarith
  have a2 := pas_chaine A2 B2 D (4098 / 1000) (1 / 128) hD0 hD (by norm_num) (by norm_num) hB2n b2 hA2
  have a2' : A2 ≤ 3578 / 100 * D ^ 2 := by
    norm_num at a2
    nlinarith [sq_nonneg D]
  nlinarith

theorem decomp_3d (F : ℕ → ℕ → ℕ → ℝ)
    (hs12 : ∀ a b c, F a b c = F b a c) (hs23 : ∀ a b c, F a b c = F a c b)
    (hpos : ∀ a b c, 0 < a → 0 < b → 0 < c → 0 ≤ Q3 F a b c) (n : ℕ) (hn : 0 < n) :
    0 ≤ Delta3 F n ∧ Q3 F n n n ≤ Delta3 F n / 4 ∧ Q3 F (2 * n) (2 * n) n ≤ Delta3 F n := by
  have h2 : 0 < 2 * n := by omega
  unfold Q3 at hpos ⊢
  unfold Delta3
  have e1 : F n n (2 * n) = F n (2 * n) n := hs23 n n (2 * n)
  have e2 : F n (2 * n) (2 * n) = F (2 * n) (2 * n) n :=
    ((hs12 n (2 * n) (2 * n)).trans (hs23 (2 * n) n (2 * n)))
  have q1 := hpos n n n hn hn hn
  have q2 := hpos n (2 * n) n hn h2 hn
  have q3 := hpos (2 * n) (2 * n) n h2 h2 hn
  have hdec : 8 * F n n n - F (2 * n) (2 * n) (2 * n) =
      4 * (2 * F n n n - F n n (2 * n)) + 2 * (2 * F n (2 * n) n - F n (2 * n) (2 * n)) +
      (2 * F (2 * n) (2 * n) n - F (2 * n) (2 * n) (2 * n)) := by
    rw [e1, e2]; ring
  refine ⟨?_, ?_, ?_⟩
  · rw [hdec]; linarith
  · rw [hdec]; linarith
  · rw [hdec]; linarith


/-- Identité de décomposition 3D : Δ₃(n) = 4 Q₃(n,n,n) + 2 Q₃(n,2n,n) + Q₃(2n,2n,n). -/
lemma dec3_eq (F : ℕ → ℕ → ℕ → ℝ)
    (hs12 : ∀ a b c, F a b c = F b a c) (hs23 : ∀ a b c, F a b c = F a c b) (n : ℕ) :
    Delta3 F n = 4 * Q3 F n n n + 2 * Q3 F n (2 * n) n + Q3 F (2 * n) (2 * n) n := by
  unfold Delta3 Q3
  have e1 : F n n (2 * n) = F n (2 * n) n := hs23 n n (2 * n)
  have e2 : F n (2 * n) (2 * n) = F (2 * n) (2 * n) n :=
    ((hs12 n (2 * n) (2 * n)).trans (hs23 (2 * n) n (2 * n)))
  rw [e1, e2]; ring

/-- Transposition (1 3) à partir des transpositions adjacentes. -/
lemma t13 (F : ℕ → ℕ → ℕ → ℝ)
    (hs12 : ∀ a b c, F a b c = F b a c) (hs23 : ∀ a b c, F a b c = F a c b) (a b c : ℕ) :
    F a b c = F c b a :=
  (hs23 a b c).trans ((hs12 a c b).trans (hs23 c a b))

/-- **Doublement 3D fin** : Δ₃(n) ≤ 2⁻⁷ ⟹ Δ₃(2n) ≤ 64 Δ₃(n)². -/
theorem doublement_fin_3d (F : ℕ → ℕ → ℕ → ℝ)
    (hs12 : ∀ a b c, F a b c = F b a c) (hs23 : ∀ a b c, F a b c = F a c b)
    (hpos : ∀ a b c, 0 < a → 0 < b → 0 < c → 0 ≤ Q3 F a b c)
    (hsq : ∀ a b c, 0 < a → 0 < b → 0 < c →
      Q3 F a b (2 * c) ≤ 2 * (Real.exp (Q3 F a b c) - 1) ^ 2)
    (n : ℕ) (hn : 0 < n) (hD : Delta3 F n ≤ 1 / 128) :
    Delta3 F (2 * n) ≤ 64 * (Delta3 F n) ^ 2 := by
  obtain ⟨hD0, -, hB0⟩ := decomp_3d F hs12 hs23 hpos n hn
  have h2 : 0 < 2 * n := by omega
  have h4 : 0 < 2 * (2 * n) := by omega
  have hB0n := hpos (2 * n) (2 * n) n h2 h2 hn
  have hB1n := hpos (2 * (2 * n)) (2 * n) n h4 h2 hn
  have hB2n := hpos (2 * (2 * n)) (2 * (2 * n)) n h4 h4 hn
  have hX := hpos n (2 * n) (2 * n) hn h2 h2
  have hY := hpos (2 * (2 * n)) n (2 * n) h4 hn h2
  have hA0 := hsq (2 * n) (2 * n) n h2 h2 hn
  have hA1 := hsq (2 * (2 * n)) (2 * n) n h4 h2 hn
  have hA2 := hsq (2 * (2 * n)) (2 * (2 * n)) n h4 h4 hn
  have s1 : F (2 * n) (2 * n) n = F n (2 * n) (2 * n) :=
    ((hs12 n (2 * n) (2 * n)).trans (hs23 (2 * n) n (2 * n))).symm
  have hB1 : Q3 F (2 * (2 * n)) (2 * n) n ≤
      2 * Q3 F (2 * n) (2 * n) n + Q3 F (2 * n) (2 * n) (2 * n) := by
    have r : Q3 F (2 * (2 * n)) (2 * n) n =
        2 * Q3 F (2 * n) (2 * n) n - 2 * Q3 F n (2 * n) (2 * n) + Q3 F (2 * n) (2 * n) (2 * n) := by
      unfold Q3
      rw [s1, t13 F hs12 hs23 n (2 * n) (2 * (2 * n)), t13 F hs12 hs23 (2 * n) (2 * n) (2 * (2 * n))]
      ring
    linarith
  have hB2 : Q3 F (2 * (2 * n)) (2 * (2 * n)) n ≤
      2 * Q3 F (2 * (2 * n)) (2 * n) n + Q3 F (2 * (2 * n)) (2 * n) (2 * n) := by
    have r : Q3 F (2 * (2 * n)) (2 * (2 * n)) n =
        2 * Q3 F (2 * (2 * n)) (2 * n) n - 2 * Q3 F (2 * (2 * n)) n (2 * n) +
          Q3 F (2 * (2 * n)) (2 * n) (2 * n) := by
      unfold Q3
      rw [hs23 (2 * (2 * n)) (2 * n) n, hs23 (2 * (2 * n)) n (2 * (2 * n)),
        hs23 (2 * (2 * n)) (2 * n) (2 * (2 * n))]
      ring
    linarith
  have hdec2 := dec3_eq F hs12 hs23 (2 * n)
  have hA1eq : Q3 F (2 * n) (2 * (2 * n)) (2 * n) = Q3 F (2 * (2 * n)) (2 * n) (2 * n) := by
    unfold Q3
    rw [hs12 (2 * n) (2 * (2 * n)) (2 * n), hs12 (2 * n) (2 * (2 * n)) (2 * (2 * n))]
  rw [hdec2, hA1eq]
  exact chaine_num_fin3 _ _ _ _ _ _ _ hD0 hD hB0n hB1n hB2n hB0 hA0 hB1 hA1 hB2 hA2

theorem iteration64 (d : ℕ → ℝ) (hnn : ∀ k, 0 ≤ d k)
    (hstep : ∀ k, d k ≤ 1 / 128 → d (k + 1) ≤ 64 * d k ^ 2) (h0 : d 0 ≤ 1 / 128) :
    ∀ k, 64 * d k ≤ (64 * d 0) ^ (2 ^ k) := by
  intro k
  induction k with
  | zero => simp
  | succ k ih =>
    have hq : 64 * d 0 ≤ 1 / 2 := by linarith
    have hq0 : 0 ≤ 64 * d 0 := by linarith [hnn 0]
    have hpow : (64 * d 0) ^ (2 ^ k) ≤ 64 * d 0 :=
      pow_le_of_le_one hq0 (by linarith) (by positivity)
    have hdk : d k ≤ 1 / 128 := by linarith
    have h1 := hstep k hdk
    have h2 : (64 * d k) ^ 2 ≤ ((64 * d 0) ^ (2 ^ k)) ^ 2 :=
      pow_le_pow_left₀ (by linarith [hnn k]) ih 2
    calc 64 * d (k + 1) ≤ 64 * (64 * d k ^ 2) := by linarith
      _ = (64 * d k) ^ 2 := by ring
      _ ≤ ((64 * d 0) ^ (2 ^ k)) ^ 2 := h2
      _ = (64 * d 0) ^ (2 ^ (k + 1)) := by rw [← pow_mul, pow_succ]

/-- Structure de transfert à trace dans la 3ᵉ direction (sections a × b). -/
def HypSpecTC3 (F : ℕ → ℕ → ℕ → ℝ) : Prop :=
  ∀ a b : ℕ, 0 < a → 0 < b →
    ∃ (r : ℕ → ℝ) (L : ℝ), (∀ i, 0 ≤ r i) ∧ (∀ i, r i ≤ 1) ∧
      (∀ c : ℕ, 0 < c → Summable (fun i => r i ^ c)) ∧
      ∀ c : ℕ, 0 < c → F a b c = (c : ℝ) * L + Real.log (1 + sT r c)

lemma Q3_eq_pT (F : ℕ → ℕ → ℕ → ℝ) (a b : ℕ) (r : ℕ → ℝ) (L : ℝ)
    (hF : ∀ c : ℕ, 0 < c → F a b c = (c : ℝ) * L + Real.log (1 + sT r c)) (c : ℕ)
    (hc : 0 < c) : Q3 F a b c = pT r c := by
  unfold Q3 pT
  rw [hF c hc, hF (2 * c) (by omega)]
  push_cast
  ring

lemma hyp_of_specTC3 (F : ℕ → ℕ → ℕ → ℝ) (hF : HypSpecTC3 F) :
    (∀ a b c, 0 < a → 0 < b → 0 < c → 0 ≤ Q3 F a b c) ∧
    (∀ a b c, 0 < a → 0 < b → 0 < c →
      Q3 F a b (2 * c) ≤ 2 * (Real.exp (Q3 F a b c) - 1) ^ 2) := by
  constructor
  · intro a b c ha hb hc
    obtain ⟨r, L, h0, h1, hs, hF⟩ := hF a b ha hb
    rw [Q3_eq_pT F a b r L hF c hc]
    exact (lemme_fin_tc r h0 h1 c (hs c hc)).1
  · intro a b c ha hb hc
    obtain ⟨r, L, h0, h1, hs, hF⟩ := hF a b ha hb
    rw [Q3_eq_pT F a b r L hF (2 * c) (by omega), Q3_eq_pT F a b r L hF c hc]
    exact (lemme_fin_tc r h0 h1 c (hs c hc)).2.2.2

/-- **Trou de transfert 3D.** Δ₃(n) ≤ 2⁻⁷ ⟹ sur toute section (2ᵏn)², r_iⁿ ≤ 64 Δ₃(n) ≤ 1/2. -/
theorem gap_3d_fin (F : ℕ → ℕ → ℕ → ℝ)
    (hs12 : ∀ a b c, F a b c = F b a c) (hs23 : ∀ a b c, F a b c = F a c b)
    (hF : HypSpecTC3 F) (n : ℕ) (hn : 0 < n) (hD : Delta3 F n ≤ 1 / 128) (k : ℕ)
    (r : ℕ → ℝ) (L : ℝ) (h0 : ∀ i, 0 ≤ r i) (h1 : ∀ i, r i ≤ 1)
    (hs : ∀ c : ℕ, 0 < c → Summable (fun i => r i ^ c))
    (hFm : ∀ c : ℕ, 0 < c →
      F (2 ^ k * n) (2 ^ k * n) c = (c : ℝ) * L + Real.log (1 + sT r c)) :
    ∀ i, r i ^ n ≤ 64 * Delta3 F n := by
  obtain ⟨hpos, hsq⟩ := hyp_of_specTC3 F hF
  have hnn : ∀ k, 0 ≤ Delta3 F (2 ^ k * n) := fun k =>
    (decomp_3d F hs12 hs23 hpos _ (by positivity)).1
  have hit : ∀ k, 64 * Delta3 F (2 ^ k * n) ≤ (64 * Delta3 F (2 ^ 0 * n)) ^ (2 ^ k) := by
    apply iteration64 (fun k => Delta3 F (2 ^ k * n)) hnn
    · intro k hk
      have := doublement_fin_3d F hs12 hs23 hpos hsq _ (by positivity) hk
      have e : 2 ^ (k + 1) * n = 2 * (2 ^ k * n) := by ring
      simp only [e]
      exact this
    · simpa using hD
  have e0 : 2 ^ 0 * n = n := by simp
  rw [e0] at hit
  intro i
  set m := 2 ^ k * n with hm
  have hm0 : 0 < m := by positivity
  have hD0 : 0 ≤ Delta3 F n := (decomp_3d F hs12 hs23 hpos n hn).1
  have hk := hit k
  have hpowle : (64 * Delta3 F n) ^ (2 ^ k) ≤ 64 * Delta3 F n :=
    pow_le_of_le_one (by linarith) (by linarith) (by positivity)
  have hDm0 : 0 ≤ Delta3 F m := hnn k
  have hDm : Delta3 F m ≤ 1 / 128 := by linarith
  obtain ⟨-, hq4, -⟩ := decomp_3d F hs12 hs23 hpos m hm0
  have hQ : Q3 F m m m = pT r m := Q3_eq_pT F m m r L hFm m hm0
  obtain ⟨hp0, hsE, hterm, -⟩ := lemme_fin_tc r h0 h1 m (hs m hm0)
  have hp : pT r m ≤ Delta3 F m / 4 := by rw [← hQ]; exact hq4
  have hp1 : pT r m ≤ 1 := by linarith
  have hexp := expm1_le (pT r m) hp0 hp1
  have hpp : pT r m ^ 2 ≤ pT r m := by nlinarith
  have hri : r i ^ m ≤ Delta3 F m / 2 := by
    have := hterm i; linarith
  have hri' : (r i ^ n) ^ (2 ^ k) ≤ (64 * Delta3 F n) ^ (2 ^ k) := by
    rw [← pow_mul, mul_comm n (2 ^ k), ← hm]
    linarith
  exact (pow_le_pow_iff_left₀ (pow_nonneg (h0 i) n) (by linarith) (by positivity)).mp hri'

/-! ## §5 Lien spectral (HYPOTHÈSE NOMMÉE) ⟹ forme q -/

section Spectral

open ClayYM.Transfer

variable {V : Type}

/-- **Hypothèse nommée (W3) : représentation spectrale de la forme OS de réseau** au temps physique `ℓ`
(= `n` pas de réseau). `c F i` = coordonnée du vecteur OS de `F` sur le i-ième vecteur d'une base orthonormée
de vecteurs propres du transfert normalisé `K̂ = K/λ₀` (indice 0 = vide de Perron, indices i+1 = états excités,
de valeurs propres `r i`). Justification : théorème spectral de Hilbert–Schmidt pour `K̂` compact autoadjoint
positif sur `H_inv`, et formule de transfert de la forme OS du cylindre (Lüscher 1977 ; Osterwalder–Seiler 1978). -/
def SpecLink (o : VecOps V) (B : V → V → ℝ → ℝ) (ℓ : ℝ) (r : ℕ → ℝ) (n : ℕ) : Prop :=
  ∃ c : V → ℕ → ℝ,
    (∀ F G i, c (o.add F G) i = c F i + c G i) ∧
    (∀ a F i, c (o.smul a F) i = a * c F i) ∧
    (∀ i, c o.Ω i = if i = 0 then 1 else 0) ∧
    (∀ F, Summable (fun i => (c F i) ^ 2)) ∧
    (∀ F, B o.Ω F 0 = c F 0) ∧
    (∀ F, B F F 0 = ∑' i, (c F i) ^ 2) ∧
    (∀ F, B F F ℓ = (c F 0) ^ 2 + ∑' i, r i ^ n * (c F (i + 1)) ^ 2)

/-- Lien spectral + rapports excités `r_iⁿ ≤ q` ⟹ forme q de la forme OS, sur tout `𝒜₀`. -/
theorem qGapOn_of_specLink (o : VecOps V) (B : V → V → ℝ → ℝ) {ℓ q : ℝ} (r : ℕ → ℝ) (n : ℕ)
    (hℓ : 0 < ℓ) (hq0 : 0 < q) (hq1 : q < 1) (hr0 : ∀ i, 0 ≤ r i) (hrq : ∀ i, r i ^ n ≤ q)
    (h : SpecLink o B ℓ r n) (𝒜₀ : Set V) : QGapOn o B 𝒜₀ ℓ q := by
  obtain ⟨c, cadd, csmul, cvac, csum, cB0, cdiag0, cdiagℓ⟩ := h
  refine ⟨hℓ, hq0, hq1, fun A _ => ?_⟩
  have hc : ∀ i, c (o.trunc B A) i = c A i + (-(B o.Ω A 0)) * (if i = 0 then 1 else 0) := by
    intro i
    show c (o.add A (o.smul (-(B o.Ω A 0)) o.Ω)) i = _
    rw [cadd, csmul, cvac]
  have hc0 : c (o.trunc B A) 0 = 0 := by rw [hc 0, cB0]; simp
  have hs : Summable (fun i => (c (o.trunc B A) (i + 1)) ^ 2) :=
    (summable_nat_add_iff 1).mpr (csum (o.trunc B A))
  have hle : ∀ i, r i ^ n * (c (o.trunc B A) (i + 1)) ^ 2 ≤ q * (c (o.trunc B A) (i + 1)) ^ 2 :=
    fun i => mul_le_mul_of_nonneg_right (hrq i) (sq_nonneg _)
  have hs' : Summable (fun i => r i ^ n * (c (o.trunc B A) (i + 1)) ^ 2) :=
    Summable.of_nonneg_of_le (fun i => mul_nonneg (pow_nonneg (hr0 i) n) (sq_nonneg _)) hle
      (hs.mul_left q)
  have h0 : B (o.trunc B A) (o.trunc B A) 0 = ∑' i, (c (o.trunc B A) (i + 1)) ^ 2 := by
    rw [cdiag0, (csum (o.trunc B A)).tsum_eq_zero_add, hc0]; simp
  rw [cdiagℓ, hc0, h0]
  calc (0 : ℝ) ^ 2 + ∑' i, r i ^ n * (c (o.trunc B A) (i + 1)) ^ 2
      = ∑' i, r i ^ n * (c (o.trunc B A) (i + 1)) ^ 2 := by simp
    _ ≤ ∑' i, q * (c (o.trunc B A) (i + 1)) ^ 2 := Summable.tsum_le_tsum hle hs' (hs.mul_left q)
    _ = q * ∑' i, (c (o.trunc B A) (i + 1)) ^ 2 := tsum_mul_left

/-! ## §6 Assemblage -/

/-- **Hypothèse nommée (W2)+(W3) au rang k, 4D** : sur la section (2^j n)³, le spectre excité `r` du transfert
qui apparaît dans log Z (forme `HypSpecTC`) est celui de la représentation spectrale de la forme OS `B` au temps ℓ
(= n pas). -/
def LienTransfert4 (o : VecOps V) (F : ℕ → ℕ → ℕ → ℕ → ℝ) (n j : ℕ) (B : V → V → ℝ → ℝ) (ℓ : ℝ) : Prop :=
  ∃ (r : ℕ → ℝ) (L : ℝ), (∀ i, 0 ≤ r i) ∧ (∀ i, r i ≤ 1) ∧
    (∀ d : ℕ, 0 < d → Summable (fun i => r i ^ d)) ∧
    (∀ d : ℕ, 0 < d → F (2 ^ j * n) (2 ^ j * n) (2 ^ j * n) d = (d : ℝ) * L + Real.log (1 + sT r d)) ∧
    SpecLink o B ℓ r n

/-- Version 3D (sections (2^j n)²). -/
def LienTransfert3 (o : VecOps V) (F : ℕ → ℕ → ℕ → ℝ) (n j : ℕ) (B : V → V → ℝ → ℝ) (ℓ : ℝ) : Prop :=
  ∃ (r : ℕ → ℝ) (L : ℝ), (∀ i, 0 ≤ r i) ∧ (∀ i, r i ≤ 1) ∧
    (∀ c : ℕ, 0 < c → Summable (fun i => r i ^ c)) ∧
    (∀ c : ℕ, 0 < c → F (2 ^ j * n) (2 ^ j * n) c = (c : ℝ) * L + Real.log (1 + sT r c)) ∧
    SpecLink o B ℓ r n

/-- **Théorème (b), forme abstraite, 4D.** Le long d'un filtre non trivial (suite, sous-suite, double limite
volume puis maille), si `sup_k Δ₄^{(k)}(n_k) ≤ η ≤ 2⁻⁹`, si chaque forme OS de réseau `B k` est reliée au
transfert de la section (2^{j_k} n_k)³ (hypothèse nommée) et si les `B k` convergent vers `Blim` sur
𝒜₀ ∪ {Ω} aux temps 0 et ℓ, alors `Blim` vérifie la forme q au temps ℓ avec q = 256η (≤ 1/2), le MÊME pour tous. -/
theorem qGapOn_limite_4d (o : VecOps V) {α : Type} {L : Filter α} [L.NeBot]
    (F : α → ℕ → ℕ → ℕ → ℕ → ℝ) (n j : α → ℕ) (hn : ∀ k, 0 < n k)
    (hs12 : ∀ k a b c d, F k a b c d = F k b a c d)
    (hs23 : ∀ k a b c d, F k a b c d = F k a c b d)
    (hs34 : ∀ k a b c d, F k a b c d = F k a b d c)
    (hF : ∀ k, HypSpecTC (F k))
    {η : ℝ} (hη0 : 0 < η) (hη : η ≤ 1 / 512) (hΔ : ∀ k, Delta (F k) (n k) ≤ η)
    (B : α → V → V → ℝ → ℝ) (hB : ∀ k, IsBilin o (B k)) {ℓ : ℝ} (hℓ : 0 < ℓ)
    (hlink : ∀ k, LienTransfert4 o (F k) (n k) (j k) (B k) ℓ)
    (Blim : V → V → ℝ → ℝ) (hBlim : IsBilin o Blim) (𝒜₀ : Set V)
    (hconv : ConvergesOn L o B Blim 𝒜₀ ℓ) :
    QGapOn o Blim 𝒜₀ ℓ (256 * η) := by
  have hk : ∀ k, QGapOn o (B k) 𝒜₀ ℓ (256 * η) := by
    intro k
    obtain ⟨r, Lk, h0, h1, hs, hFm, hsl⟩ := hlink k
    have hD : Delta (F k) (n k) ≤ 1 / 512 := le_trans (hΔ k) hη
    have hr := gap_4d_fin (F k) (hs12 k) (hs23 k) (hs34 k) (hF k) (n k) (hn k) hD (j k) r Lk h0 h1 hs hFm
    have hrq : ∀ i, r i ^ n k ≤ 256 * η := fun i => le_trans (hr i) (by linarith [hΔ k])
    exact qGapOn_of_specLink o (B k) r (n k) hℓ (by linarith) (by linarith) h0 hrq hsl 𝒜₀
  exact QGapOn.of_tendsto hB hBlim hconv (Eventually.of_forall hk)

/-- **Théorème (b), version 3D** : seuil 2⁻⁷, q = 64η. -/
theorem qGapOn_limite_3d (o : VecOps V) {α : Type} {L : Filter α} [L.NeBot]
    (F : α → ℕ → ℕ → ℕ → ℝ) (n j : α → ℕ) (hn : ∀ k, 0 < n k)
    (hs12 : ∀ k a b c, F k a b c = F k b a c) (hs23 : ∀ k a b c, F k a b c = F k a c b)
    (hF : ∀ k, HypSpecTC3 (F k))
    {η : ℝ} (hη0 : 0 < η) (hη : η ≤ 1 / 128) (hΔ : ∀ k, Delta3 (F k) (n k) ≤ η)
    (B : α → V → V → ℝ → ℝ) (hB : ∀ k, IsBilin o (B k)) {ℓ : ℝ} (hℓ : 0 < ℓ)
    (hlink : ∀ k, LienTransfert3 o (F k) (n k) (j k) (B k) ℓ)
    (Blim : V → V → ℝ → ℝ) (hBlim : IsBilin o Blim) (𝒜₀ : Set V)
    (hconv : ConvergesOn L o B Blim 𝒜₀ ℓ) :
    QGapOn o Blim 𝒜₀ ℓ (64 * η) := by
  have hk : ∀ k, QGapOn o (B k) 𝒜₀ ℓ (64 * η) := by
    intro k
    obtain ⟨r, Lk, h0, h1, hs, hFm, hsl⟩ := hlink k
    have hD : Delta3 (F k) (n k) ≤ 1 / 128 := le_trans (hΔ k) hη
    have hr := gap_3d_fin (F k) (hs12 k) (hs23 k) (hF k) (n k) (hn k) hD (j k) r Lk h0 h1 hs hFm
    have hrq : ∀ i, r i ^ n k ≤ 64 * η := fun i => le_trans (hr i) (by linarith [hΔ k])
    exact qGapOn_of_specLink o (B k) r (n k) hℓ (by linarith) (by linarith) h0 hrq hsl 𝒜₀
  exact QGapOn.of_tendsto hB hBlim hconv (Eventually.of_forall hk)

/-- **Variante tores (hypothèse W5)** : si les formes des tores `Btor k` convergent vers `Blim` et ne diffèrent
de celles des cylindres `B k` que par un terme qui tend vers 0 (sur 𝒜₀ ∪ {Ω}, temps 0 et ℓ), alors les
formes des cylindres convergent aussi vers `Blim` : on se ramène au cas précédent. -/
theorem convergesOn_of_proche (o : VecOps V) {α : Type} {L : Filter α}
    (B Btor : α → V → V → ℝ → ℝ) (Blim : V → V → ℝ → ℝ) (𝒜₀ : Set V) {ℓ : ℝ}
    (hproche : ∀ F ∈ insert o.Ω 𝒜₀, ∀ G ∈ insert o.Ω 𝒜₀, ∀ t ∈ ({0, ℓ} : Set ℝ),
      Tendsto (fun k => Btor k F G t - B k F G t) L (𝓝 0))
    (hconv : ConvergesOn L o Btor Blim 𝒜₀ ℓ) : ConvergesOn L o B Blim 𝒜₀ ℓ := by
  intro F hF G hG t ht
  have h := (hconv F hF G hG t ht).sub (hproche F hF G hG t ht)
  simp only [sub_zero, sub_sub_cancel] at h
  exact h

end Spectral

/-! ## §7 En termes ClayYM -/

section Clay

open ClayYM ClayYM.Transfer

lemma log_deux_le {η ℓ : ℝ} (hℓ : 0 < ℓ) (hη0 : 0 < η) (hq : 256 * η ≤ 1 / 2) :
    Real.log 2 / ℓ ≤ -Real.log (256 * η) / ℓ := by
  have h1 : Real.log (256 * η) ≤ Real.log (1 / 2) := Real.log_le_log (by linarith) hq
  have h2 : Real.log (1 / 2) = -Real.log 2 := by rw [one_div, Real.log_inv]
  apply div_le_div_of_nonneg_right _ hℓ.le
  linarith

/-- **Théorème (b) en termes de ClayYM (4D)** : la limite `S` (noyaux de Schwinger de ClayYM sur ℝ⁴) des formes
OS de réseau vérifie `QGap R S univ ℓ (256η)` ; avec l'hypothèse nommée `OSReconstruction R S` et `S [] = 1`,
elle a le trou `HasMassGap R S (−log(256η)/ℓ)`, et −log(256η)/ℓ ≥ (log 2)/ℓ. -/
theorem clay_trou_de_critere_4d {ι : Type} [Fintype ι] (R : CompRep ι 4) (S : Schwinger ι 4)
    {α : Type} {L : Filter α} [L.NeBot]
    (F : α → ℕ → ℕ → ℕ → ℕ → ℝ) (n j : α → ℕ) (hn : ∀ k, 0 < n k)
    (hs12 : ∀ k a b c d, F k a b c d = F k b a c d)
    (hs23 : ∀ k a b c d, F k a b c d = F k a c b d)
    (hs34 : ∀ k a b c d, F k a b c d = F k a b d c)
    (hF : ∀ k, HypSpecTC (F k))
    {η : ℝ} (hη0 : 0 < η) (hη : η ≤ 1 / 512) (hΔ : ∀ k, Delta (F k) (n k) ≤ η)
    (B : α → Family ι 4 → Family ι 4 → ℝ → ℝ) (hB : ∀ k, IsBilin (famOps ι 4) (B k))
    {ℓ : ℝ} (hℓ : 0 < ℓ)
    (hlink : ∀ k, LienTransfert4 (famOps ι 4) (F k) (n k) (j k) (B k) ℓ)
    (hconv : ConvergesOn L (famOps ι 4) B (rpForm R S) Set.univ ℓ)
    (rec : OSReconstruction R S) (hnorm : S [] = 1) :
    QGap R S Set.univ ℓ (256 * η) ∧ HasMassGap R S (-Real.log (256 * η) / ℓ) ∧
      Real.log 2 / ℓ ≤ -Real.log (256 * η) / ℓ := by
  have hq : QGap R S Set.univ ℓ (256 * η) :=
    (qGap_iff_qGapOn R S Set.univ ℓ _).2
      (qGapOn_limite_4d (famOps ι 4) F n j hn hs12 hs23 hs34 hF hη0 hη hΔ B hB hℓ hlink
        (rpForm R S) (rpForm_isBilin R S) Set.univ hconv)
  exact ⟨hq, hq.hasMassGap_univ rec hnorm, log_deux_le hℓ hη0 (by linarith)⟩

/-- **Théorème (b) en termes de ClayYM (3D)** : q = 64η, seuil 2⁻⁷. -/
theorem clay_trou_de_critere_3d {ι : Type} [Fintype ι] (R : CompRep ι 3) (S : Schwinger ι 3)
    {α : Type} {L : Filter α} [L.NeBot]
    (F : α → ℕ → ℕ → ℕ → ℝ) (n j : α → ℕ) (hn : ∀ k, 0 < n k)
    (hs12 : ∀ k a b c, F k a b c = F k b a c) (hs23 : ∀ k a b c, F k a b c = F k a c b)
    (hF : ∀ k, HypSpecTC3 (F k))
    {η : ℝ} (hη0 : 0 < η) (hη : η ≤ 1 / 128) (hΔ : ∀ k, Delta3 (F k) (n k) ≤ η)
    (B : α → Family ι 3 → Family ι 3 → ℝ → ℝ) (hB : ∀ k, IsBilin (famOps ι 3) (B k))
    {ℓ : ℝ} (hℓ : 0 < ℓ)
    (hlink : ∀ k, LienTransfert3 (famOps ι 3) (F k) (n k) (j k) (B k) ℓ)
    (hconv : ConvergesOn L (famOps ι 3) B (rpForm R S) Set.univ ℓ)
    (rec : OSReconstruction R S) (hnorm : S [] = 1) :
    QGap R S Set.univ ℓ (64 * η) ∧ HasMassGap R S (-Real.log (64 * η) / ℓ) := by
  have hq : QGap R S Set.univ ℓ (64 * η) :=
    (qGap_iff_qGapOn R S Set.univ ℓ _).2
      (qGapOn_limite_3d (famOps ι 3) F n j hn hs12 hs23 hF hη0 hη hΔ B hB hℓ hlink
        (rpForm R S) (rpForm_isBilin R S) Set.univ hconv)
  exact ⟨hq, hq.hasMassGap_univ rec hnorm⟩

end Clay

/-! ## §8 Non-vacuité : les hypothèses du théorème (b) sont simultanément satisfiables (modèle trivial) -/

section NonVacuite

open ClayYM.Transfer

/-- Opérations de ℝ (V = ℝ, Ω = 1). -/
def opsR : VecOps ℝ where
  add := fun a b => a + b
  smul := fun c a => c * a
  Ω := 1

/-- Forme triviale B(F, G, t) = F·G (théorie triviale : un seul état). -/
def BR : ℝ → ℝ → ℝ → ℝ := fun a b _ => a * b

lemma BR_bilin : IsBilin opsR BR where
  add_left := fun F F' G t => by simp only [BR, opsR]; ring
  add_right := fun F G G' t => by simp only [BR, opsR]; ring
  smul_left := fun c F G t => by simp only [BR, opsR]; ring
  smul_right := fun c F G t => by simp only [BR, opsR]; ring

lemma zero_pow_fun (d : ℕ) (hd : 0 < d) : (fun _ : ℕ => (0 : ℝ) ^ d) = fun _ => 0 := by
  funext i; exact zero_pow (Nat.pos_iff_ne_zero.mp hd)

lemma sT_zero (d : ℕ) (hd : 0 < d) : sT (fun _ => 0) d = 0 := by
  unfold sT; rw [zero_pow_fun d hd]; exact tsum_zero

lemma hypSpec_zero : HypSpecTC (fun _ _ _ _ => (0 : ℝ)) := by
  intro a b c _ _ _
  refine ⟨fun _ => 0, 0, fun _ => le_refl _, fun _ => zero_le_one, ?_, ?_⟩
  · intro d hd
    show Summable (fun _ : ℕ => (0 : ℝ) ^ d)
    rw [zero_pow_fun d hd]; exact summable_zero
  · intro d hd
    rw [sT_zero d hd]; simp

lemma specLink_zero (n : ℕ) (hn : 0 < n) (ℓ : ℝ) : SpecLink opsR BR ℓ (fun _ => 0) n := by
  refine ⟨fun F i => if i = 0 then F else 0, ?_, ?_, ?_, ?_, ?_, ?_, ?_⟩
  · intro F G i; simp only [opsR]; split_ifs <;> ring
  · intro a F i; simp only [opsR]; split_ifs <;> ring
  · intro i; rfl
  · intro F
    have e : (fun i : ℕ => (if i = 0 then F else 0) ^ 2) = fun i => if i = 0 then F ^ 2 else 0 := by
      funext i; split_ifs <;> ring
    rw [e]; exact (hasSum_ite_eq 0 (F ^ 2)).summable
  · intro F; simp [BR, opsR]
  · intro F
    have e : (fun i : ℕ => (if i = 0 then F else 0) ^ 2) = fun i => if i = 0 then F ^ 2 else 0 := by
      funext i; split_ifs <;> ring
    show F * F = ∑' i, (if i = 0 then F else 0) ^ 2
    rw [e, tsum_ite_eq]; ring
  · intro F
    have e : (fun i : ℕ => (0 : ℝ) ^ n * (if i + 1 = 0 then F else 0) ^ 2) = fun _ => 0 := by
      funext i; simp
    show F * F = (if (0 : ℕ) = 0 then F else 0) ^ 2 + ∑' i, (0 : ℝ) ^ n * (if i + 1 = 0 then F else 0) ^ 2
    rw [e, tsum_zero]; simp; ring

/-- **Non-vacuité** : toutes les hypothèses de `qGapOn_limite_4d` sont satisfaites par la théorie triviale
(log Z ≡ 0, un seul état) ; la conclusion est alors la forme q avec q = 1/4. Garde contre une hypothèse contradictoire
cachée (piège de P2 v1 : structure spectrale imposée aux tailles nulles). -/
theorem non_vacuite_4d : QGapOn opsR BR Set.univ 1 (256 * (1 / 1024)) :=
  qGapOn_limite_4d opsR (L := (Filter.atTop : Filter ℕ)) (fun _ => fun _ _ _ _ => (0 : ℝ))
    (fun _ => 1) (fun _ => 0) (fun _ => one_pos)
    (fun _ _ _ _ _ => rfl) (fun _ _ _ _ _ => rfl) (fun _ _ _ _ _ => rfl)
    (fun _ => hypSpec_zero) (by norm_num) (by norm_num)
    (fun _ => by simp [Delta])
    (fun _ => BR) (fun _ => BR_bilin) one_pos
    (fun _ => ⟨fun _ => 0, 0, fun _ => le_refl _, fun _ => zero_le_one,
      (fun d hd => by show Summable (fun _ : ℕ => (0 : ℝ) ^ d); rw [zero_pow_fun d hd]; exact summable_zero),
      (fun d hd => by rw [sT_zero d hd]; simp), specLink_zero 1 one_pos 1⟩)
    BR BR_bilin Set.univ (fun _ _ _ _ _ _ => tendsto_const_nhds)

end NonVacuite

end CritereScalaire

end
