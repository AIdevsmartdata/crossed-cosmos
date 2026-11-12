import Mathlib

/-! MUTANTS ET NON-VACUITE (rejeu non-auteur). Prélude recopié de PREUVES.lean jusqu à aux_diff.
  toute preuve) ; seuls les `sorry` sont remplacés, et des lemmes auxiliaires (préfixe `aux_`) sont ajoutés. -/

open BigOperators Finset

namespace CritereThooft

abbrev Sec := Fin 3 → ZMod 2

/-- χ_k(e) = (-1)^{k·e}. -/
def chi (k e : Sec) : ℝ := ∏ j : Fin 3, (if k j = 1 ∧ e j = 1 then (-1 : ℝ) else 1)

lemma aux_ne01 : (0 : ZMod 2) ≠ 1 := by decide

lemma aux_somme_facteur (b : ZMod 2) :
    ∑ a : ZMod 2, (if a = 1 ∧ b = 1 then (-1 : ℝ) else 1) = if b = 1 then 0 else 2 := by
  have hu : (Finset.univ : Finset (ZMod 2)) = {0, 1} := by decide
  rw [hu, Finset.sum_pair aux_ne01]
  by_cases hb : b = 1
  · subst hb
    have h0 : ¬ ((0 : ZMod 2) = 1 ∧ (1 : ZMod 2) = 1) := fun h => aux_ne01 h.1
    rw [if_neg h0, if_pos ⟨rfl, rfl⟩, if_pos rfl]
    norm_num
  · have h0 : ¬ ((0 : ZMod 2) = 1 ∧ b = 1) := fun h => aux_ne01 h.1
    have h1 : ¬ ((1 : ZMod 2) = 1 ∧ b = 1) := fun h => hb h.2
    rw [if_neg h0, if_neg h1, if_neg hb]
    norm_num

/-- Orthogonalité des caractères de ℤ₂³. -/
theorem chi_somme (e : Sec) : ∑ k : Sec, chi k e = if e = 0 then 8 else 0 := by
  have h1 : ∑ k : Sec, chi k e
      = ∏ j : Fin 3, ∑ a : ZMod 2, (if a = 1 ∧ e j = 1 then (-1 : ℝ) else 1) := by
    unfold chi
    rw [Fintype.prod_sum]
  rw [h1, Finset.prod_congr rfl (fun j _ => aux_somme_facteur (e j))]
  by_cases he : e = 0
  · subst he
    simp [aux_ne01]
    norm_num
  · have hex : ∃ j, e j = 1 := by
      by_contra hne
      push_neg at hne
      apply he
      funext j
      have hj := hne j
      generalize e j = b at hj ⊢
      fin_cases b
      · rfl
      · exact absurd rfl hj
    obtain ⟨j, hj⟩ := hex
    rw [if_neg he]
    apply Finset.prod_eq_zero (Finset.mem_univ j)
    simp [hj]

lemma aux_chi_zero_left (e : Sec) : chi 0 e = 1 := by
  unfold chi
  apply Finset.prod_eq_one
  intro j _
  simp [aux_ne01]

lemma aux_chi_zero_right (k : Sec) : chi k 0 = 1 := by
  unfold chi
  apply Finset.prod_eq_one
  intro j _
  simp [aux_ne01]

lemma aux_chi_abs (k e : Sec) : |chi k e| = 1 := by
  unfold chi
  rw [Finset.abs_prod]
  apply Finset.prod_eq_one
  intro j _
  split_ifs <;> simp

lemma aux_chi_bornes (k e : Sec) : 0 ≤ 1 - chi k e ∧ 1 - chi k e ≤ 2 := by
  have h := aux_chi_abs k e
  rw [abs_eq (by norm_num : (0:ℝ) ≤ 1)] at h
  rcases h with h | h <;> rw [h] <;> norm_num

variable {ι : Type*} [Fintype ι] [DecidableEq ι]

def Zt (r : ι → ℝ) (lab : ι → Sec) (k : Sec) (M : ℕ) : ℝ := ∑ i, chi k (lab i) * r i ^ M
def Tr0 (r : ι → ℝ) (lab : ι → Sec) (M : ℕ) : ℝ := ∑ i ∈ univ.filter (fun i => lab i = 0), r i ^ M
def sExc (r : ι → ℝ) (i0 : ι) (M : ℕ) : ℝ := ∑ i ∈ univ.erase i0, r i ^ M

/-- T1(a) : trace du secteur neutre = (1/8) Σ_k Z_k. -/
theorem trace_neutre (r : ι → ℝ) (lab : ι → Sec) (M : ℕ) :
    ∑ k : Sec, Zt r lab k M = 8 * Tr0 r lab M := by
  unfold Zt Tr0
  rw [Finset.sum_comm]
  simp_rw [← Finset.sum_mul, chi_somme]
  rw [Finset.sum_filter, Finset.mul_sum]
  apply Finset.sum_congr rfl
  intro i _
  split_ifs <;> ring

lemma aux_Z0 (r : ι → ℝ) (lab : ι → Sec) (M : ℕ) : Zt r lab 0 M = ∑ i, r i ^ M := by
  unfold Zt
  simp [aux_chi_zero_left]

lemma aux_Z0_split (r : ι → ℝ) (lab : ι → Sec) (i0 : ι) (h0 : r i0 = 1) (M : ℕ) :
    Zt r lab 0 M = 1 + sExc r i0 M := by
  rw [aux_Z0, ← Finset.add_sum_erase _ _ (Finset.mem_univ i0), h0, one_pow]
  rfl

lemma aux_sExc_nonneg (r : ι → ℝ) (i0 : ι) (hr0 : ∀ i, 0 ≤ r i) (M : ℕ) : 0 ≤ sExc r i0 M := by
  unfold sExc
  exact Finset.sum_nonneg (fun i _ => pow_nonneg (hr0 i) M)

lemma aux_diff (r : ι → ℝ) (lab : ι → Sec) (i0 : ι) (hl : lab i0 = 0) (k : Sec) (M : ℕ) :
    Zt r lab 0 M - Zt r lab k M = ∑ i ∈ univ.erase i0, (1 - chi k (lab i)) * r i ^ M := by
  have hs : Zt r lab 0 M - Zt r lab k M = ∑ i, (1 - chi k (lab i)) * r i ^ M := by
    rw [aux_Z0]
    unfold Zt
    rw [← Finset.sum_sub_distrib]
    apply Finset.sum_congr rfl
    intro i _
    ring
  rw [hs, ← Finset.add_sum_erase _ _ (Finset.mem_univ i0), hl, aux_chi_zero_right]
  simp

/-! ## Prélude chiffré -/
def e1 : Sec := ![1, 0, 0]

lemma e1_ne : e1 ≠ 0 := by
  intro h
  have := congrFun h 0
  simp [e1] at this

lemma chi_zero_left_ex : chi 0 e1 = 1 := aux_chi_zero_left e1

lemma chi_e1_e1 : chi e1 e1 = -1 := by
  unfold chi e1
  simp [Fin.prod_univ_three]

lemma chi_e1_0 : chi e1 0 = 1 := aux_chi_zero_right e1

noncomputable def r1 : Fin 2 → ℝ := ![1, 1/2]
def lab1 : Fin 2 → Sec := ![0, e1]

lemma Zt_r1_0 (M : ℕ) : Zt r1 lab1 0 M = 1 + (1/2) ^ M := by
  simp [Zt, r1, lab1, Fin.sum_univ_two, aux_chi_zero_left]

lemma Zt_r1_e1 (M : ℕ) : Zt r1 lab1 e1 M = 1 - (1/2) ^ M := by
  simp [Zt, r1, lab1, Fin.sum_univ_two, chi_e1_0, chi_e1_e1]
  ring

lemma sExc_r1 (M : ℕ) : sExc r1 0 M = (1/2) ^ M := by
  simp [sExc, r1, Fin.sum_univ_two]

/-! ## Non-vacuité : les hypothèses sont satisfaites par une instance explicite -/
theorem nv_spectre : r1 0 = 1 ∧ lab1 0 = 0 ∧ ∀ i, 0 ≤ r1 i := by
  refine ⟨by simp [r1], by simp [lab1], ?_⟩
  intro i; fin_cases i <;> simp [r1]

theorem nv_vide_neutre : ∃ g : Sec → ℕ, 1 ≤ ∑ e, g e ∧ ∀ k, 0 ≤ ∑ e, chi k e * (g e : ℝ) := by
  refine ⟨fun e => if e = 0 then 1 else 0, ?_, ?_⟩
  · simp
  · intro k; simp [aux_chi_zero_right]

theorem nv_deux_sous_verrous :
    ∃ (Δ e1' e2 : ℝ) (s0 D : Fin 4 → ℝ), 0 ≤ e1' ∧ e1' ≤ 1 / 8 ∧ (∀ j, 0 ≤ s0 j ∧ s0 j ≤ e2) ∧
      (∀ j, 0 ≤ D j ∧ D j ≤ 7 * e1' / 8) ∧
      Δ ≤ 2 * ∑ j : Fin 4, (2 : ℝ) ^ (3 - (j : ℕ)) * (Real.log (1 + s0 j) - Real.log (1 - D j)) := by
  refine ⟨0, 0, 0, fun _ => 0, fun _ => 0, le_rfl, by norm_num, ?_, ?_, ?_⟩ <;> simp

/-! ## Mutants : l'énoncé muté est FAUX (contre-exemple chiffré) -/

/-- M-A : chi_somme avec 8 -> 7. -/
theorem mut_chi_somme_7 : ¬ (∀ e : Sec, ∑ k : Sec, chi k e = if e = 0 then 7 else 0) := by
  intro H
  have h := H 0
  have h8 := chi_somme 0
  simp at h h8
  linarith

/-- M-B : trace_neutre avec 8 -> 4. -/
theorem mut_trace_neutre_4 : ¬ (∀ (r : Fin 2 → ℝ) (lab : Fin 2 → Sec) (M : ℕ),
    ∑ k : Sec, Zt r lab k M = 4 * Tr0 r lab M) := by
  intro H
  have h := H r1 lab1 0
  rw [trace_neutre] at h
  have hT : Tr0 r1 lab1 0 = 1 := by
    rw [Tr0, Finset.sum_filter, Fin.sum_univ_two]
    simp [r1, lab1, e1_ne]
  rw [hT] at h
  simp [Zt] at h

/-- M-C1 : defaut_torsion sans « le vide est dans e = 0 » (hl). -/
theorem mut_defaut_sans_hl : ¬ (∀ (r : Fin 2 → ℝ) (lab : Fin 2 → Sec) (i0 : Fin 2) (h0 : r i0 = 1)
    (hr0 : ∀ i, 0 ≤ r i) (k : Sec) (M : ℕ),
    0 ≤ 1 - Zt r lab k M / Zt r lab 0 M ∧ 1 - Zt r lab k M / Zt r lab 0 M ≤ 2 * sExc r i0 M) := by
  intro H
  have h := (H r1 (fun _ => e1) 0 (by simp [r1]) (by intro i; fin_cases i <;> simp [r1]) e1 1).2
  simp [Zt, sExc, r1, Fin.sum_univ_two, chi_e1_e1, chi_zero_left_ex] at h
  norm_num at h

/-- M-C2 : defaut_torsion sans positivité des r_i (hr0). -/
theorem mut_defaut_sans_hr0 : ¬ (∀ (r : Fin 2 → ℝ) (lab : Fin 2 → Sec) (i0 : Fin 2) (h0 : r i0 = 1)
    (hl : lab i0 = 0) (k : Sec) (M : ℕ),
    0 ≤ 1 - Zt r lab k M / Zt r lab 0 M ∧ 1 - Zt r lab k M / Zt r lab 0 M ≤ 2 * sExc r i0 M) := by
  intro H
  have h := (H ![1, -1] lab1 0 (by simp) (by simp [lab1]) e1 1).2
  simp [Zt, sExc, lab1, Fin.sum_univ_two, chi_e1_e1, aux_chi_zero_left, chi_e1_0, chi_zero_left_ex] at h
  norm_num at h

/-- M-C3 : defaut_torsion durci : 2 s -> s. -/
theorem mut_defaut_durci : ¬ (∀ (r : Fin 2 → ℝ) (lab : Fin 2 → Sec) (i0 : Fin 2) (h0 : r i0 = 1)
    (hl : lab i0 = 0) (hr0 : ∀ i, 0 ≤ r i) (k : Sec) (M : ℕ),
    0 ≤ 1 - Zt r lab k M / Zt r lab 0 M ∧ 1 - Zt r lab k M / Zt r lab 0 M ≤ sExc r i0 M) := by
  intro H
  have h := (H r1 lab1 0 nv_spectre.1 nv_spectre.2.1 nv_spectre.2.2 e1 1).2
  rw [Zt_r1_0, Zt_r1_e1, sExc_r1] at h
  norm_num at h


/-- M-D : decomposition sans « le vide est dans e = 0 » (hl) : faux (Tr0 = 0, log 0 = 0 dans Lean). -/
theorem mut_decomposition_sans_hl : ¬ (∀ (r : Fin 2 → ℝ) (lab : Fin 2 → Sec) (i0 : Fin 2) (h0 : r i0 = 1)
    (hr0 : ∀ i, 0 ≤ r i) (M : ℕ),
    Real.log (Zt r lab 0 M) =
      Real.log (1 + (Tr0 r lab M - 1)) + Real.log (8 * Zt r lab 0 M / ∑ k : Sec, Zt r lab k M)) := by
  intro H
  have h := H ![1, 1] (fun _ => e1) 0 (by simp) (by intro i; fin_cases i <;> simp) 1
  have hT : Tr0 ![1, 1] (fun _ : Fin 2 => e1) 1 = 0 := by
    rw [Tr0, Finset.sum_filter]
    simp [e1_ne]
  have hS : ∑ k : Sec, Zt ![1, 1] (fun _ : Fin 2 => e1) k 1 = 0 := by
    rw [trace_neutre, hT]; simp
  rw [hS, hT] at h
  simp [Zt, chi_zero_left_ex, Fin.sum_univ_two] at h
  norm_num at h

/-- M-E1 : vide_neutre sans la positivité des G_k (hk). -/
theorem mut_vide_sans_hk : ¬ (∀ g : Sec → ℕ, 1 ≤ ∑ e, g e → 1 ≤ g 0) := by
  intro H
  have h := H (fun e => if e = e1 then 1 else 0) (by simp)
  simp [e1_ne.symm] at h

/-- M-E2 : vide_neutre durci : 1 <= g 0 -> 2 <= g 0. -/
theorem mut_vide_durci : ¬ (∀ g : Sec → ℕ, 1 ≤ ∑ e, g e → (∀ k, 0 ≤ ∑ e, chi k e * (g e : ℝ)) → 2 ≤ g 0) := by
  intro H
  have h := H (fun e => if e = 0 then 1 else 0) (by simp) (by intro k; simp [aux_chi_zero_right])
  simp at h

/-- M-F1 : propagation sans hq (0 <= q). -/
theorem mut_propagation_sans_hq : ¬ (∀ (r : Unit → ℝ) (lab : Unit → Sec) (i0 : Unit) (h0 : r i0 = 1)
    (hl : lab i0 = 0) (hr0 : ∀ i, 0 ≤ r i) (n m l : ℕ) (q A : ℝ)
    (hexc : ∀ i, i ≠ i0 → r i ^ n ≤ q) (hA : sExc r i0 m ≤ A) (k : Sec),
    1 - Zt r lab k (m + n * l) / Zt r lab 0 (m + n * l) ≤ 2 * A * q ^ l) := by
  intro H
  have h := H (fun _ => 1) (fun _ => 0) () (by simp) (by simp) (by intro i; simp) 0 0 1 (-1) 1
    (by intro i hi; exact absurd rfl hi) (by simp [sExc]) 0
  simp [Zt, aux_chi_zero_left] at h
  norm_num at h

/-- M-F2 : propagation durcie : 2 A q^l -> A q^l. -/
theorem mut_propagation_durci : ¬ (∀ (n m l : ℕ) (q A : ℝ) (hq : 0 ≤ q)
    (hexc : ∀ i : Fin 2, i ≠ 0 → r1 i ^ n ≤ q) (hA : sExc r1 0 m ≤ A) (k : Sec),
    1 - Zt r1 lab1 k (m + n * l) / Zt r1 lab1 0 (m + n * l) ≤ A * q ^ l) := by
  intro H
  have h := H 1 1 0 (1/2) (1/2) (by norm_num)
    (by intro i hi; fin_cases i
        · exact absurd rfl hi
        · simp [r1]) (by rw [sExc_r1]; norm_num) e1
  simp only [mul_zero, add_zero, pow_zero, mul_one] at h
  rw [Zt_r1_0, Zt_r1_e1] at h
  norm_num at h

/-- M-G1 : deux_sous_verrous avec 29 au lieu de 30. -/
theorem mut_verrous_29 : ¬ (∀ (Δ e1' e2 : ℝ) (s0 D : Fin 4 → ℝ) (he1 : 0 ≤ e1') (he1' : e1' ≤ 1 / 8)
    (hs0 : ∀ j, 0 ≤ s0 j ∧ s0 j ≤ e2) (hD : ∀ j, 0 ≤ D j ∧ D j ≤ 7 * e1' / 8)
    (hΔ : Δ ≤ 2 * ∑ j : Fin 4, (2 : ℝ) ^ (3 - (j : ℕ)) * (Real.log (1 + s0 j) - Real.log (1 - D j))),
    Δ ≤ 29 * (e1' + e2)) := by
  intro H
  have h := H (30 * Real.log (1 + 1/100)) 0 (1/100) (fun _ => 1/100) (fun _ => 0) le_rfl (by norm_num)
    (by intro j; norm_num) (by intro j; simp) (by simp [Fin.sum_univ_four]; linarith)
  have hl := Real.one_sub_inv_le_log_of_pos (by norm_num : (0:ℝ) < 1 + 1/100)
  norm_num at h hl
  linarith

/-- M-G2 : deux_sous_verrous sans e1 <= 1/8. -/
theorem mut_verrous_sans_borne : ¬ (∀ (Δ e1' e2 : ℝ) (s0 D : Fin 4 → ℝ) (he1 : 0 ≤ e1')
    (hs0 : ∀ j, 0 ≤ s0 j ∧ s0 j ≤ e2) (hD : ∀ j, 0 ≤ D j ∧ D j ≤ 7 * e1' / 8)
    (hΔ : Δ ≤ 2 * ∑ j : Fin 4, (2 : ℝ) ^ (3 - (j : ℕ)) * (Real.log (1 + s0 j) - Real.log (1 - D j))),
    Δ ≤ 30 * (e1' + e2)) := by
  intro H
  have h := H (30 * Real.log 8) 1 0 (fun _ => 0) (fun _ => 7/8) (by norm_num)
    (by intro j; simp) (by intro j; norm_num)
    (by
      have hlog : Real.log (1 - 7/8 : ℝ) = - Real.log 8 := by
        rw [show (1 - 7/8 : ℝ) = (8:ℝ)⁻¹ by norm_num, Real.log_inv]
      simp [Fin.sum_univ_four, hlog]
      linarith)
  have h2 := Real.log_two_gt_d9
  have h3 : Real.log 8 = 3 * Real.log 2 := by
    rw [show (8:ℝ) = 2^3 by norm_num, Real.log_pow]; norm_num
  linarith

end CritereThooft

#print axioms CritereThooft.mut_chi_somme_7
