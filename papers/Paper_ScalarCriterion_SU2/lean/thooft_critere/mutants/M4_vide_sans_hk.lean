import Mathlib

/-! PREUVES (critere_thooft, 12/11/2026). Énoncés recopiés mot pour mot de ENONCES.lean (sha256 7dd1a95c…, figés avant
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

/-- T1(b),(e) : 0 ≤ 1 − Z_k/Z₀ ≤ 2 s(M). -/
theorem defaut_torsion (r : ι → ℝ) (lab : ι → Sec) (i0 : ι) (h0 : r i0 = 1) (hl : lab i0 = 0)
    (hr0 : ∀ i, 0 ≤ r i) (k : Sec) (M : ℕ) :
    0 ≤ 1 - Zt r lab k M / Zt r lab 0 M ∧ 1 - Zt r lab k M / Zt r lab 0 M ≤ 2 * sExc r i0 M := by
  have hS := aux_sExc_nonneg r i0 hr0 M
  have hZ := aux_Z0_split r lab i0 h0 M
  have hZpos : 0 < Zt r lab 0 M := by rw [hZ]; linarith
  have hZ1 : 1 ≤ Zt r lab 0 M := by rw [hZ]; linarith
  have hrew : 1 - Zt r lab k M / Zt r lab 0 M = (Zt r lab 0 M - Zt r lab k M) / Zt r lab 0 M := by
    field_simp
  have hD := aux_diff r lab i0 hl k M
  have hnum0 : 0 ≤ Zt r lab 0 M - Zt r lab k M := by
    rw [hD]
    exact Finset.sum_nonneg (fun i _ => mul_nonneg (aux_chi_bornes k (lab i)).1 (pow_nonneg (hr0 i) M))
  have hnum2 : Zt r lab 0 M - Zt r lab k M ≤ 2 * sExc r i0 M := by
    rw [hD]
    unfold sExc
    rw [Finset.mul_sum]
    apply Finset.sum_le_sum
    intro i _
    exact mul_le_mul_of_nonneg_right (aux_chi_bornes k (lab i)).2 (pow_nonneg (hr0 i) M)
  rw [hrew]
  constructor
  · exact div_nonneg hnum0 hZpos.le
  · calc (Zt r lab 0 M - Zt r lab k M) / Zt r lab 0 M ≤ Zt r lab 0 M - Zt r lab k M := by
          rw [div_le_iff₀ hZpos]
          nlinarith
      _ ≤ 2 * sExc r i0 M := hnum2

/-- T1(d) : décomposition exacte h = log(1 + s⁰) + log(8 Z₀ / Σ_k Z_k). -/
theorem decomposition (r : ι → ℝ) (lab : ι → Sec) (i0 : ι) (h0 : r i0 = 1) (hl : lab i0 = 0)
    (hr0 : ∀ i, 0 ≤ r i) (M : ℕ) :
    Real.log (Zt r lab 0 M) =
      Real.log (1 + (Tr0 r lab M - 1)) + Real.log (8 * Zt r lab 0 M / ∑ k : Sec, Zt r lab k M) := by
  have hT : 1 ≤ Tr0 r lab M := by
    unfold Tr0
    have hmem : i0 ∈ univ.filter (fun i => lab i = 0) := by simp [hl]
    rw [← Finset.add_sum_erase _ _ hmem, h0, one_pow]
    have : 0 ≤ ∑ i ∈ (univ.filter (fun i => lab i = 0)).erase i0, r i ^ M :=
      Finset.sum_nonneg (fun i _ => pow_nonneg (hr0 i) M)
    linarith
  have hZ := aux_Z0_split r lab i0 h0 M
  have hS := aux_sExc_nonneg r i0 hr0 M
  have hZpos : 0 < Zt r lab 0 M := by rw [hZ]; linarith
  have hTpos : 0 < Tr0 r lab M := by linarith
  rw [trace_neutre, add_sub_cancel]
  rw [show 8 * Zt r lab 0 M / (8 * Tr0 r lab M) = Zt r lab 0 M / Tr0 r lab M by
    field_simp]
  rw [Real.log_div hZpos.ne' hTpos.ne']
  ring

/-- T1(c), cœur : si toutes les limites G_k = Σ_e χ_k(e) g_e sont ≥ 0 et Σ g ≥ 1, le vide a une copie dans e = 0. -/
theorem vide_neutre (g : Sec → ℕ) (hpos : 1 ≤ ∑ e, g e) (hk : True) :
    1 ≤ g 0 := by
  by_contra hlt
  push_neg at hlt
  have hg0 : g 0 = 0 := by omega
  have htot : ∑ k : Sec, ∑ e, chi k e * (g e : ℝ) = 8 * (g 0 : ℝ) := by
    rw [Finset.sum_comm]
    simp_rw [← Finset.sum_mul, chi_somme]
    simp
  rw [hg0] at htot
  simp only [Nat.cast_zero, mul_zero] at htot
  have hall := (Finset.sum_eq_zero_iff_of_nonneg (fun k _ => hk k)).mp htot
  have h0 := hall 0 (Finset.mem_univ 0)
  simp only [aux_chi_zero_left, one_mul] at h0
  have : (1 : ℝ) ≤ ∑ e, (g e : ℝ) := by exact_mod_cast hpos
  linarith

/-- T2, cœur : si tout rapport excité vérifie r^n ≤ q et si s(m) ≤ A, alors 1 − Z_k/Z₀ ≤ 2 A q^l au temps m + n l. -/
theorem propagation (r : ι → ℝ) (lab : ι → Sec) (i0 : ι) (h0 : r i0 = 1) (hl : lab i0 = 0)
    (hr0 : ∀ i, 0 ≤ r i) (n m l : ℕ) (q A : ℝ) (hq : 0 ≤ q)
    (hexc : ∀ i, i ≠ i0 → r i ^ n ≤ q) (hA : sExc r i0 m ≤ A) (k : Sec) :
    1 - Zt r lab k (m + n * l) / Zt r lab 0 (m + n * l) ≤ 2 * A * q ^ l := by
  have hs : sExc r i0 (m + n * l) ≤ sExc r i0 m * q ^ l := by
    unfold sExc
    rw [Finset.sum_mul]
    apply Finset.sum_le_sum
    intro i hi
    have hne : i ≠ i0 := Finset.ne_of_mem_erase hi
    rw [pow_add, pow_mul]
    exact mul_le_mul_of_nonneg_left (pow_le_pow_left₀ (pow_nonneg (hr0 i) n) (hexc i hne) l)
      (pow_nonneg (hr0 i) m)
  have h1 := (defaut_torsion r lab i0 h0 hl hr0 k (m + n * l)).2
  have hql : 0 ≤ q ^ l := pow_nonneg hq l
  have h2 : sExc r i0 m * q ^ l ≤ A * q ^ l := mul_le_mul_of_nonneg_right hA hql
  nlinarith

/-- T3(a), partie réelle : h_j = log(1+s⁰_j) + φ_j, φ_j = −log(1 − D_j), D_j ≤ 7ε₁/8, s⁰_j ≤ ε₂, ε₁ ≤ 1/8,
    Δ ≤ 2 Σ_j 2^{3−j} h_j  ⟹  Δ ≤ 30 (ε₁ + ε₂). -/
theorem deux_sous_verrous (Δ e1 e2 : ℝ) (s0 D : Fin 4 → ℝ) (he1 : 0 ≤ e1) (he1' : e1 ≤ 1 / 8)
    (hs0 : ∀ j, 0 ≤ s0 j ∧ s0 j ≤ e2) (hD : ∀ j, 0 ≤ D j ∧ D j ≤ 7 * e1 / 8)
    (hΔ : Δ ≤ 2 * ∑ j : Fin 4, (2 : ℝ) ^ (3 - (j : ℕ)) * (Real.log (1 + s0 j) - Real.log (1 - D j))) :
    Δ ≤ 30 * (e1 + e2) := by
  have hterm : ∀ j, Real.log (1 + s0 j) - Real.log (1 - D j) ≤ e1 + e2 := by
    intro j
    obtain ⟨hs0a, hs0b⟩ := hs0 j
    obtain ⟨hDa, hDb⟩ := hD j
    have hlog1 : Real.log (1 + s0 j) ≤ s0 j := by
      have := Real.log_le_sub_one_of_pos (by linarith : (0:ℝ) < 1 + s0 j)
      linarith
    have hDlt : D j ≤ 7 / 64 := by linarith
    have hpos : 0 < 1 - D j := by linarith
    have hlog2 : -Real.log (1 - D j) ≤ D j / (1 - D j) := by
      have h := Real.one_sub_inv_le_log_of_pos hpos
      have heq : D j / (1 - D j) = (1 - D j)⁻¹ - 1 := by field_simp; ring
      linarith
    have hfrac : D j / (1 - D j) ≤ e1 := by
      rw [div_le_iff₀ hpos]
      nlinarith
    linarith
  have hw : ∀ j : Fin 4, (0 : ℝ) ≤ (2 : ℝ) ^ (3 - (j : ℕ)) := fun j => by positivity
  have hsum : ∑ j : Fin 4, (2 : ℝ) ^ (3 - (j : ℕ)) * (Real.log (1 + s0 j) - Real.log (1 - D j))
      ≤ ∑ j : Fin 4, (2 : ℝ) ^ (3 - (j : ℕ)) * (e1 + e2) :=
    Finset.sum_le_sum (fun j _ => mul_le_mul_of_nonneg_left (hterm j) (hw j))
  have hw15 : ∑ j : Fin 4, (2 : ℝ) ^ (3 - (j : ℕ)) * (e1 + e2) = 15 * (e1 + e2) := by
    simp [Fin.sum_univ_four]
    ring
  linarith

end CritereThooft

#print axioms CritereThooft.chi_somme
#print axioms CritereThooft.trace_neutre
#print axioms CritereThooft.defaut_torsion
#print axioms CritereThooft.decomposition
#print axioms CritereThooft.vide_neutre
#print axioms CritereThooft.propagation
#print axioms CritereThooft.deux_sous_verrous
