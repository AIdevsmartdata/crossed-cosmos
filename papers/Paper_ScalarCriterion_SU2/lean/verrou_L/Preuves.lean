import Mathlib

/-! PREUVES (verrou_2026-11-12 / lean_L, partie B). Énoncés recopiés à l'identique de Enonces.lean (sha256 dans
  ENONCES_GELES.md, version 1) ; seuls les `sorry` sont remplacés, et des lemmes auxiliaires (préfixe `aux_`) sont ajoutés. -/

open BigOperators

namespace VerrouL

abbrev SU2 := Matrix.specialUnitaryGroup (Fin 2) ℂ

lemma aux_det (U : SU2) : (U : Matrix (Fin 2) (Fin 2) ℂ).det = 1 :=
  (Matrix.mem_specialUnitaryGroup_iff.mp U.2).2

lemma aux_traces (A B : Matrix (Fin 2) (Fin 2) ℂ) (hA : A.det = 1) (hB : B.det = 1)
    (h : A * B = -(B * A)) : A.trace = 0 ∧ B.trace = 0 := by
  have e00 := congrFun (congrFun h 0) 0
  have e01 := congrFun (congrFun h 0) 1
  have e10 := congrFun (congrFun h 1) 0
  have e11 := congrFun (congrFun h 1) 1
  simp [Matrix.mul_apply, Fin.sum_univ_two] at e00 e01 e10 e11
  simp [Matrix.det_fin_two, Matrix.trace_fin_two] at hA hB ⊢
  constructor <;> grind

lemma aux_sq (A : Matrix (Fin 2) (Fin 2) ℂ) (hA : A.det = 1) (ht : A.trace = 0) : A ^ 2 = -1 := by
  have h1 := hA
  have h2 := ht
  simp [Matrix.det_fin_two, Matrix.trace_fin_two] at h1 h2
  ext i j
  fin_cases i <;> fin_cases j <;> simp [pow_two, Matrix.mul_apply, Fin.sum_univ_two] <;> grind

lemma aux_iσ1_mem : (!![0, Complex.I; Complex.I, 0] : Matrix (Fin 2) (Fin 2) ℂ) ∈ Matrix.specialUnitaryGroup (Fin 2) ℂ := by
  rw [Matrix.mem_specialUnitaryGroup_iff, Matrix.mem_unitaryGroup_iff]
  constructor
  · ext i j
    fin_cases i <;> fin_cases j <;> simp [Matrix.mul_apply, Fin.sum_univ_two, Matrix.star_apply]
  · simp [Matrix.det_fin_two]

lemma aux_iσ2_mem : (!![0, 1; -1, 0] : Matrix (Fin 2) (Fin 2) ℂ) ∈ Matrix.specialUnitaryGroup (Fin 2) ℂ := by
  rw [Matrix.mem_specialUnitaryGroup_iff, Matrix.mem_unitaryGroup_iff]
  constructor
  · ext i j
    fin_cases i <;> fin_cases j <;> simp [Matrix.mul_apply, Fin.sum_univ_two, Matrix.star_apply]
  · simp [Matrix.det_fin_two]

/-! ### (a) Le fait algébrique -/

/-- (a1) si U V = −(V U), alors tr U = 0, tr V = 0, U² = −1, V² = −1. -/
theorem a1_anticommute (U V : SU2)
    (h : (U : Matrix (Fin 2) (Fin 2) ℂ) * V = -((V : Matrix (Fin 2) (Fin 2) ℂ) * U)) :
    Matrix.trace (U : Matrix (Fin 2) (Fin 2) ℂ) = 0 ∧ Matrix.trace (V : Matrix (Fin 2) (Fin 2) ℂ) = 0 ∧
    (U : Matrix (Fin 2) (Fin 2) ℂ) ^ 2 = -1 ∧ (V : Matrix (Fin 2) (Fin 2) ℂ) ^ 2 = -1 := by
  obtain ⟨h1, h2⟩ := aux_traces _ _ (aux_det U) (aux_det V) h
  exact ⟨h1, h2, aux_sq _ (aux_det U) h1, aux_sq _ (aux_det V) h2⟩

/-- (a2) si de plus W ∈ SU(2) commute avec U et avec V, alors W = 1 ou W = −1. -/
theorem a2_commutant (U V W : SU2)
    (h : (U : Matrix (Fin 2) (Fin 2) ℂ) * V = -((V : Matrix (Fin 2) (Fin 2) ℂ) * U))
    (hU : (W : Matrix (Fin 2) (Fin 2) ℂ) * U = (U : Matrix (Fin 2) (Fin 2) ℂ) * W)
    (hV : (W : Matrix (Fin 2) (Fin 2) ℂ) * V = (V : Matrix (Fin 2) (Fin 2) ℂ) * W) :
    (W : Matrix (Fin 2) (Fin 2) ℂ) = 1 ∨ (W : Matrix (Fin 2) (Fin 2) ℂ) = -1 := by
  obtain ⟨ht1, ht2, -, -⟩ := a1_anticommute U V h
  have dU := aux_det U
  have dV := aux_det V
  have dW := aux_det W
  have e00 := congrFun (congrFun h 0) 0
  have e01 := congrFun (congrFun h 0) 1
  have e10 := congrFun (congrFun h 1) 0
  have e11 := congrFun (congrFun h 1) 1
  have u00 := congrFun (congrFun hU 0) 0
  have u01 := congrFun (congrFun hU 0) 1
  have u10 := congrFun (congrFun hU 1) 0
  have u11 := congrFun (congrFun hU 1) 1
  have v00 := congrFun (congrFun hV 0) 0
  have v01 := congrFun (congrFun hV 0) 1
  have v10 := congrFun (congrFun hV 1) 0
  have v11 := congrFun (congrFun hV 1) 1
  simp [Matrix.mul_apply, Fin.sum_univ_two] at e00 e01 e10 e11 u00 u01 u10 u11 v00 v01 v10 v11
  simp [Matrix.det_fin_two, Matrix.trace_fin_two] at dU dV dW ht1 ht2
  have hq : (W : Matrix (Fin 2) (Fin 2) ℂ) 0 1 = 0 := by grind
  have hr : (W : Matrix (Fin 2) (Fin 2) ℂ) 1 0 = 0 := by grind
  have hd : (W : Matrix (Fin 2) (Fin 2) ℂ) 0 0 = (W : Matrix (Fin 2) (Fin 2) ℂ) 1 1 := by grind
  have hp : ((W : Matrix (Fin 2) (Fin 2) ℂ) 0 0 - 1) * ((W : Matrix (Fin 2) (Fin 2) ℂ) 0 0 + 1) = 0 := by
    grind
  rcases mul_eq_zero.mp hp with h1 | h1
  · left
    ext i j
    fin_cases i <;> fin_cases j <;> simp <;> grind
  · right
    ext i j
    fin_cases i <;> fin_cases j <;> simp <;> grind

/-- (a3) non-vacuité : i·σ₁ = !![0, I; I, 0] et i·σ₂ = !![0, 1; -1, 0] sont dans SU(2) et anticommutent. -/
theorem a3_existence : ∃ U V : SU2,
    (U : Matrix (Fin 2) (Fin 2) ℂ) = !![0, Complex.I; Complex.I, 0] ∧
    (V : Matrix (Fin 2) (Fin 2) ℂ) = !![0, 1; -1, 0] ∧
    (U : Matrix (Fin 2) (Fin 2) ℂ) * V = -((V : Matrix (Fin 2) (Fin 2) ℂ) * U) := by
  refine ⟨⟨_, aux_iσ1_mem⟩, ⟨_, aux_iσ2_mem⟩, rfl, rfl, ?_⟩
  ext i j
  fin_cases i <;> fin_cases j <;> simp [Matrix.mul_apply, Fin.sum_univ_two]

/-- (a4) mutant abélien, forme « 2 inversible » : dans un anneau commutatif non trivial où 2 est inversible,
    deux unités n'anticommutent jamais. -/
theorem a4_unites_commutatif {R : Type*} [CommRing R] [Nontrivial R] (h2 : IsUnit (2 : R)) (u v : Rˣ) :
    (u : R) * v ≠ -((v : R) * u) := by
  intro h
  have h' : (2 : R) * ((u : R) * v) = 0 := by linear_combination h
  have h'' : (u : R) * v = 0 := h2.mul_right_eq_zero.mp h'
  have : IsUnit ((u : R) * v) := (u * v).isUnit
  exact this.ne_zero h''

/-- (a4') mutant abélien, forme « intègre de caractéristique ≠ 2 » : deux éléments non nuls n'anticommutent pas
    (couvre U(1) ⊂ ℂ et ℤ₂ = {±1} ⊂ ℤ). -/
theorem a4_integre {R : Type*} [CommRing R] [IsDomain R] (h2 : (2 : R) ≠ 0) (u v : R)
    (hu : u ≠ 0) (hv : v ≠ 0) : u * v ≠ -(v * u) := by
  intro h
  have h' : (2 : R) * (u * v) = 0 := by linear_combination h
  rcases mul_eq_zero.mp h' with h1 | h1
  · exact h2 h1
  · exact mul_ne_zero hu hv h1

/-- (a4'') cas U(1) et ℤ₂ : deux éléments du cercle (resp. de ℤˣ = {±1}) n'anticommutent pas. -/
theorem a4_cercle_et_Z2 :
    (∀ u v : Circle, (u : ℂ) * v ≠ -((v : ℂ) * u)) ∧ (∀ u v : ℤˣ, (u : ℤ) * v ≠ -((v : ℤ) * u)) := by
  constructor
  · intro u v
    exact a4_integre (by norm_num) _ _ (Circle.coe_ne_zero u) (Circle.coe_ne_zero v)
  · intro u v
    exact a4_integre (by norm_num) _ _ u.ne_zero v.ne_zero

/-- (a5) mutant de (a2) : commuter avec U SEUL ne force pas W = ±1 (W = U convient). -/
theorem a5_mutant_commuter_avec_U_seul : ∃ U V W : SU2,
    (U : Matrix (Fin 2) (Fin 2) ℂ) * V = -((V : Matrix (Fin 2) (Fin 2) ℂ) * U) ∧
    (W : Matrix (Fin 2) (Fin 2) ℂ) * U = (U : Matrix (Fin 2) (Fin 2) ℂ) * W ∧
    ¬ ((W : Matrix (Fin 2) (Fin 2) ℂ) = 1 ∨ (W : Matrix (Fin 2) (Fin 2) ℂ) = -1) := by
  obtain ⟨U, V, hU, hV, h⟩ := a3_existence
  refine ⟨U, V, U, h, rfl, ?_⟩
  rintro (h1 | h1)
  · have := congrFun (congrFun h1 0) 1
    rw [hU] at this
    simp at this
  · have := congrFun (congrFun h1 0) 1
    rw [hU] at this
    simp at this

/-! ### (b) Algèbre réelle du Corollaire L1 -/

/-- (b1) 0 ≤ R ≤ 1, D ≥ (3/8)(1 − R), D < 1, 8(−log(1 − D)) ≤ Δ  ⟹  Δ ≥ 8 log(8/(5 + 3R)). -/
theorem b1_cube (R D Δ : ℝ) (hR0 : 0 ≤ R) (hR1 : R ≤ 1) (hD : 3 / 8 * (1 - R) ≤ D) (hD1 : D < 1)
    (hΔ : 8 * (-Real.log (1 - D)) ≤ Δ) : 8 * Real.log (8 / (5 + 3 * R)) ≤ Δ := by
  have hx : 0 < 1 - D := by linarith
  have hy : 1 - D ≤ (5 + 3 * R) / 8 := by linarith
  have hl := Real.log_le_log hx hy
  have heq : Real.log (8 / (5 + 3 * R)) = - Real.log ((5 + 3 * R) / 8) := by
    rw [← Real.log_inv, inv_div]
  linarith

lemma aux_sept (r D : ℝ) (R : Fin 7 → ℝ) (hR : ∀ k, 0 ≤ R k ∧ R k ≤ r)
    (hD : 1 - D = (1 + ∑ k, R k) / 8) : 0 < 1 - D ∧ 1 - D ≤ (1 + 7 * r) / 8 := by
  have h0 : 0 ≤ ∑ k, R k := Finset.sum_nonneg (fun k _ => (hR k).1)
  have h1 : ∑ k, R k ≤ ∑ _k : Fin 7, r := Finset.sum_le_sum (fun k _ => (hR k).2)
  have h2 : ∑ _k : Fin 7, r = 7 * r := by simp
  constructor <;> linarith

/-- (b2) sept rapports 0 ≤ R_k ≤ r, 1 − D = (1 + Σ R_k)/8  ⟹  −log(1 − D) ≥ log(8/(1 + 7r)). -/
theorem b2_sept_rapports (r D : ℝ) (R : Fin 7 → ℝ) (hR : ∀ k, 0 ≤ R k ∧ R k ≤ r)
    (hD : 1 - D = (1 + ∑ k, R k) / 8) : Real.log (8 / (1 + 7 * r)) ≤ -Real.log (1 - D) := by
  obtain ⟨hx, hy⟩ := aux_sept r D R hR hD
  have hl := Real.log_le_log hx hy
  have heq : Real.log (8 / (1 + 7 * r)) = - Real.log ((1 + 7 * r) / 8) := by
    rw [← Real.log_inv, inv_div]
  linarith

/-- (b2') et si r ≤ 1/7 : −log(1 − D) ≥ log 4. -/
theorem b2_log4 (r D : ℝ) (R : Fin 7 → ℝ) (hR : ∀ k, 0 ≤ R k ∧ R k ≤ r) (hr : r ≤ 1 / 7)
    (hD : 1 - D = (1 + ∑ k, R k) / 8) : Real.log 4 ≤ -Real.log (1 - D) := by
  have hr0 : 0 ≤ r := le_trans (hR 0).1 (hR 0).2
  have hpos : 0 < 1 + 7 * r := by linarith
  have h4 : (4 : ℝ) ≤ 8 / (1 + 7 * r) := by
    rw [le_div_iff₀ hpos]; linarith
  have := Real.log_le_log (by norm_num) h4
  have h2 := b2_sept_rapports r D R hR hD
  linarith

/-- (b3) somme des poids 8 + 4 + 2 + 1 = 15 (aussi Σ_{j<4} 2^{3−j}) et 15 log 8 = 45 log 2. -/
theorem b3_poids : (8 + 4 + 2 + 1 : ℕ) = 15 ∧ ∑ j : Fin 4, (2 : ℕ) ^ (3 - (j : ℕ)) = 15 ∧
    (15 : ℝ) * Real.log 8 = 45 * Real.log 2 := by
  refine ⟨by norm_num, by simp [Fin.sum_univ_four], ?_⟩
  have : (8 : ℝ) = 2 ^ 3 := by norm_num
  rw [this, Real.log_pow]
  push_cast
  ring

/-! ### (c) Comptages de dimension -/

/-- (c1) dans ℕ (soustractions tronquées) : pour V ≥ 1 et d ≥ 2, (3dV − 3V) − (3dV − 3V + 1 − d) = d − 1. -/
theorem c1_nat (V d : ℕ) (hV : 1 ≤ V) (hd : 2 ≤ d) :
    (3 * d * V - 3 * V) - (3 * d * V - 3 * V + 1 - d) = d - 1 := by
  have h1 : V + d ≤ d * V + 1 := by nlinarith
  have h2 : V ≤ d * V := Nat.le_mul_of_pos_left V (by omega)
  have h3 : 3 * d * V = 3 * (d * V) := by ring
  rw [h3]
  generalize d * V = t at h1 h2 ⊢
  omega

/-- (c1) dans ℤ, sans hypothèse. -/
theorem c1_int (V d : ℤ) : (3 * d * V - 3 * V) - (3 * d * V - 3 * V + 1 - d) = d - 1 := by
  ring

/-- (c2) en dimension 4 : 6 + 9(V − 1) = 9V − 3 (V ≥ 1, dans ℕ). -/
theorem c2_nat (V : ℕ) (hV : 1 ≤ V) : 6 + 9 * (V - 1) = 9 * V - 3 := by
  omega

/-- (c2) dans ℤ, sans hypothèse. -/
theorem c2_int (V : ℤ) : 6 + 9 * (V - 1) = 9 * V - 3 := by
  ring

end VerrouL

#print axioms VerrouL.a1_anticommute
#print axioms VerrouL.a2_commutant
#print axioms VerrouL.a3_existence
#print axioms VerrouL.a4_unites_commutatif
#print axioms VerrouL.a4_integre
#print axioms VerrouL.a4_cercle_et_Z2
#print axioms VerrouL.a5_mutant_commuter_avec_U_seul
#print axioms VerrouL.b1_cube
#print axioms VerrouL.b2_sept_rapports
#print axioms VerrouL.b2_log4
#print axioms VerrouL.b3_poids
#print axioms VerrouL.c1_nat
#print axioms VerrouL.c1_int
#print axioms VerrouL.c2_nat
#print axioms VerrouL.c2_int
