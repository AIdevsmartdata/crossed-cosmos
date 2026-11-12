import Mathlib

/-! ENONCES FIGES (12/11/2026, avant toute preuve).  Aucun `sorry` ne doit rester dans RECIPROQUE.lean.
  Les définitions `sT`, `Delta` sont celles de CritereScalaire.lean (recopiées à l'identique, espace de noms séparé) ;
  `HypSpec` est `HypSpecTC` ; `HypRec` est la récurrence publiée `doublement_fin_4d` prise comme hypothèse nommée. -/
namespace Reciproque

noncomputable def sT (r : ℕ → ℝ) (n : ℕ) : ℝ := ∑' i, r i ^ n
def Delta (F : ℕ → ℕ → ℕ → ℕ → ℝ) (n : ℕ) : ℝ :=
  16 * F n n n n - F (2 * n) (2 * n) (2 * n) (2 * n)

/-- (W2) : représentation spectrale de la section (a,b,c), temps d>0. -/
def Rep (F : ℕ → ℕ → ℕ → ℕ → ℝ) (a b c : ℕ) (r : ℕ → ℝ) (L : ℝ) : Prop :=
  (∀ i, r i ≤ 1) ∧ (∀ d : ℕ, 0 < d → Summable (fun i => r i ^ d)) ∧
  ∀ d : ℕ, 0 < d → F a b c d = (d : ℝ) * L + Real.log (1 + sT r d)

def HypSpec (F : ℕ → ℕ → ℕ → ℕ → ℝ) : Prop :=
  ∀ a b c : ℕ, 0 < a → 0 < b → 0 < c → ∃ (r : ℕ → ℝ) (L : ℝ), Rep F a b c r L

/-- Récurrence de doublement (théorème publié, hypothèse nommée ici). -/
def HypRec (F : ℕ → ℕ → ℕ → ℕ → ℝ) : Prop :=
  ∀ m : ℕ, 0 < m → Delta F m ≤ 1 / 512 → Delta F (2 * m) ≤ 256 * Delta F m ^ 2


/-- pression par site -/
noncomputable def fp (F : ℕ → ℕ → ℕ → ℕ → ℝ) (a b c d : ℕ) : ℝ :=
  F a b c d / ((a : ℝ) * b * c * d)

lemma sT_nonneg (r : ℕ → ℝ) (h0 : ∀ i, 0 ≤ r i) (d : ℕ) : 0 ≤ sT r d :=
  tsum_nonneg (fun i => pow_nonneg (h0 i) d)

lemma sT_anti (r : ℕ → ℝ) (h0 : ∀ i, 0 ≤ r i) (h1 : ∀ i, r i ≤ 1)
    (hs : ∀ d : ℕ, 0 < d → Summable (fun i => r i ^ d)) {d d' : ℕ} (hd : 0 < d) (hdd : d ≤ d') :
    sT r d' ≤ sT r d :=
  Summable.tsum_le_tsum (fun i => pow_le_pow_of_le_one (h0 i) (h1 i) hdd)
    (hs d' (lt_of_lt_of_le hd hdd)) (hs d hd)

lemma h_nonneg (r : ℕ → ℝ) (h0 : ∀ i, 0 ≤ r i) (d : ℕ) : 0 ≤ Real.log (1 + sT r d) :=
  Real.log_nonneg (by linarith [sT_nonneg r h0 d])

lemma h_anti (r : ℕ → ℝ) (h0 : ∀ i, 0 ≤ r i) (h1 : ∀ i, r i ≤ 1)
    (hs : ∀ d : ℕ, 0 < d → Summable (fun i => r i ^ d)) {d d' : ℕ} (hd : 0 < d) (hdd : d ≤ d') :
    Real.log (1 + sT r d') ≤ Real.log (1 + sT r d) :=
  Real.log_le_log (by linarith [sT_nonneg r h0 d']) (by linarith [sT_anti r h0 h1 hs hd hdd])

lemma fp_rep {F : ℕ → ℕ → ℕ → ℕ → ℝ} {a b c : ℕ} {r : ℕ → ℝ} {L : ℝ} (hrep : Rep F a b c r L)
    (ha : 0 < a) (hb : 0 < b) (hc : 0 < c) {d : ℕ} (hd : 0 < d) :
    fp F a b c d = L / ((a : ℝ) * b * c) + Real.log (1 + sT r d) / ((a : ℝ) * b * c * d) := by
  unfold fp
  rw [hrep.2.2.2 d hd]
  have : (0 : ℝ) < a := by exact_mod_cast ha
  have : (0 : ℝ) < b := by exact_mod_cast hb
  have : (0 : ℝ) < c := by exact_mod_cast hc
  have : (0 : ℝ) < d := by exact_mod_cast hd
  field_simp

lemma mono4 {F : ℕ → ℕ → ℕ → ℕ → ℝ} (hS : HypSpec F) {a b c d d' : ℕ} (ha : 0 < a) (hb : 0 < b)
    (hc : 0 < c) (hd : 0 < d) (hdd : d ≤ d') : fp F a b c d' ≤ fp F a b c d := by
  obtain ⟨r, L, hrep⟩ := hS a b c ha hb hc
  have hd' : 0 < d' := lt_of_lt_of_le hd hdd
  rw [fp_rep hrep ha hb hc hd, fp_rep hrep ha hb hc hd']
  have hha := h_anti r hrep.1 hrep.2.1 hrep.2.2.1 hd hdd
  have hh0 := h_nonneg r hrep.1 d
  have pa : (0 : ℝ) < a := by exact_mod_cast ha
  have pb : (0 : ℝ) < b := by exact_mod_cast hb
  have pc : (0 : ℝ) < c := by exact_mod_cast hc
  have pd : (0 : ℝ) < d := by exact_mod_cast hd
  have pd' : (0 : ℝ) < d' := by exact_mod_cast hd'
  have hdd' : (d : ℝ) ≤ d' := by exact_mod_cast hdd
  have key : Real.log (1 + sT r d') / ((a : ℝ) * b * c * d') ≤
      Real.log (1 + sT r d) / ((a : ℝ) * b * c * d) := by
    rw [div_le_div_iff₀ (by positivity) (by positivity)]
    have e1 : Real.log (1 + sT r d') * ((a : ℝ) * b * c * d) ≤
        Real.log (1 + sT r d) * ((a : ℝ) * b * c * d) :=
      mul_le_mul_of_nonneg_right hha (by positivity)
    have e2 : Real.log (1 + sT r d) * ((a : ℝ) * b * c * d) ≤
        Real.log (1 + sT r d) * ((a : ℝ) * b * c * d') :=
      mul_le_mul_of_nonneg_left (by gcongr) hh0
    linarith
  linarith

section sym
variable {F : ℕ → ℕ → ℕ → ℕ → ℝ}

lemma fp_s12 (hs12 : ∀ a b c d, F a b c d = F b a c d) (a b c d : ℕ) : fp F a b c d = fp F b a c d := by
  unfold fp; rw [hs12 a b c d]; congr 1; ring
lemma fp_s23 (hs23 : ∀ a b c d, F a b c d = F a c b d) (a b c d : ℕ) : fp F a b c d = fp F a c b d := by
  unfold fp; rw [hs23 a b c d]; congr 1; ring
lemma fp_s34 (hs34 : ∀ a b c d, F a b c d = F a b d c) (a b c d : ℕ) : fp F a b c d = fp F a b d c := by
  unfold fp; rw [hs34 a b c d]; congr 1; ring

variable (hs12 : ∀ a b c d, F a b c d = F b a c d) (hs23 : ∀ a b c d, F a b c d = F a c b d)
  (hs34 : ∀ a b c d, F a b c d = F a b d c) (hS : HypSpec F)
include hs34 hS

lemma mono3 {a b c c' d : ℕ} (ha : 0 < a) (hb : 0 < b) (hc : 0 < c) (hd : 0 < d) (hcc : c ≤ c') :
    fp F a b c' d ≤ fp F a b c d := by
  rw [fp_s34 hs34 a b c' d, fp_s34 hs34 a b c d]
  exact mono4 hS ha hb hd hc hcc

include hs23 in
lemma mono2 {a b b' c d : ℕ} (ha : 0 < a) (hb : 0 < b) (hc : 0 < c) (hd : 0 < d) (hbb : b ≤ b') :
    fp F a b' c d ≤ fp F a b c d := by
  rw [fp_s23 hs23 a b' c d, fp_s23 hs23 a b c d]
  exact mono3 hs34 hS ha hc hb hd hbb

include hs23 hs12 in
lemma mono1 {a a' b c d : ℕ} (ha : 0 < a) (hb : 0 < b) (hc : 0 < c) (hd : 0 < d) (haa : a ≤ a') :
    fp F a' b c d ≤ fp F a b c d := by
  rw [fp_s12 hs12 a' b c d, fp_s12 hs12 a b c d]
  exact mono2 hs23 hs34 hS hb ha hc hd haa

include hs23 hs12 in
lemma mono_all {a b c d a' b' c' d' : ℕ} (ha : 0 < a) (hb : 0 < b) (hc : 0 < c) (hd : 0 < d)
    (haa : a ≤ a') (hbb : b ≤ b') (hcc : c ≤ c') (hdd : d ≤ d') :
    fp F a' b' c' d' ≤ fp F a b c d := by
  have ha' : 0 < a' := lt_of_lt_of_le ha haa
  have hb' : 0 < b' := lt_of_lt_of_le hb hbb
  have hc' : 0 < c' := lt_of_lt_of_le hc hcc
  calc fp F a' b' c' d' ≤ fp F a' b' c' d := mono4 hS ha' hb' hc' hd hdd
    _ ≤ fp F a' b' c d := mono3 hs34 hS ha' hb' hc hd hcc
    _ ≤ fp F a' b c d := mono2 hs23 hs34 hS ha' hb hc hd hbb
    _ ≤ fp F a b c d := mono1 hs12 hs23 hs34 hS ha hb hc hd haa
end sym

lemma fp_diff (F : ℕ → ℕ → ℕ → ℕ → ℝ) {m : ℕ} (hm : 0 < m) :
    fp F m m m m - fp F (2 * m) (2 * m) (2 * m) (2 * m) = Delta F m / (16 * (m : ℝ) ^ 4) := by
  unfold fp Delta
  have : (0 : ℝ) < m := by exact_mod_cast hm
  push_cast
  field_simp
  ring


section main
variable {F : ℕ → ℕ → ℕ → ℕ → ℝ}
variable (hs12 : ∀ a b c d, F a b c d = F b a c d) (hs23 : ∀ a b c d, F a b c d = F a c b d)
  (hs34 : ∀ a b c d, F a b c d = F a b d c) (hS : HypSpec F) (hR : HypRec F)

include hs12 hs23 hs34 hS in
lemma delta_nonneg {m : ℕ} (hm : 0 < m) : 0 ≤ Delta F m := by
  have h := mono_all hs12 hs23 hs34 hS hm hm hm hm (Nat.le_mul_of_pos_left m (by norm_num : 0 < 2))
    (Nat.le_mul_of_pos_left m (by norm_num : 0 < 2)) (Nat.le_mul_of_pos_left m (by norm_num : 0 < 2))
    (Nat.le_mul_of_pos_left m (by norm_num : 0 < 2))
  have h2 := fp_diff F hm
  have hmR : (0 : ℝ) < m := by exact_mod_cast hm
  by_contra hneg
  push Not at hneg
  have : Delta F m / (16 * (m : ℝ) ^ 4) < 0 := div_neg_of_neg_of_pos hneg (by positivity)
  linarith

include hs12 hs23 hs34 hS hR in
lemma step_bound {m : ℕ} (hm : 0 < m) {u : ℝ} (hu : Delta F m ≤ u) (hu2 : u ≤ 1 / 512) :
    Delta F (2 * m) ≤ 256 * u ^ 2 := by
  have h0 := delta_nonneg hs12 hs23 hs34 hS hm
  have := hR m hm (by linarith)
  have h3 : Delta F m ^ 2 ≤ u ^ 2 := pow_le_pow_left₀ h0 hu 2
  linarith

include hs12 hs23 hs34 hS hR in
lemma delta_seq {m : ℕ} (hm : 0 < m) (hD : Delta F m ≤ 1 / 512) :
    ∀ j : ℕ, 0 ≤ Delta F (2 ^ j * m) ∧ Delta F (2 ^ j * m) ≤ Delta F m / 2 ^ j := by
  intro j
  induction j with
  | zero => simp only [pow_zero, one_mul, div_one]; exact ⟨delta_nonneg hs12 hs23 hs34 hS hm, le_refl _⟩
  | succ j ih =>
    have hmj : 0 < 2 ^ j * m := by positivity
    have e : 2 ^ (j + 1) * m = 2 * (2 ^ j * m) := by ring
    rw [e]
    obtain ⟨h0, h1⟩ := ih
    have hD0 := delta_nonneg hs12 hs23 hs34 hS hm
    have hp : (1 : ℝ) ≤ 2 ^ j := one_le_pow₀ (by norm_num)
    have hpp : (0 : ℝ) < 2 ^ j := by positivity
    have hle : Delta F m / 2 ^ j ≤ Delta F m := div_le_self hD0 hp
    have hj : Delta F (2 ^ j * m) ≤ 1 / 512 := by linarith
    have := hR _ hmj hj
    refine ⟨delta_nonneg hs12 hs23 hs34 hS (by omega), ?_⟩
    have h5 : 256 * Delta F (2 ^ j * m) ^ 2 ≤ Delta F (2 ^ j * m) / 2 := by nlinarith
    have h6 : Delta F (2 ^ j * m) / 2 ≤ Delta F m / 2 ^ j / 2 := by linarith
    calc Delta F (2 * (2 ^ j * m)) ≤ _ := this
      _ ≤ Delta F m / 2 ^ j / 2 := by linarith
      _ = Delta F m / 2 ^ (j + 1) := by rw [pow_succ]; field_simp

include hs12 hs23 hs34 hS hR in
lemma telescope {m : ℕ} (hm : 0 < m) (hD : Delta F m ≤ 1 / 512) :
    ∀ J : ℕ, fp F m m m m - fp F (2 ^ J * m) (2 ^ J * m) (2 ^ J * m) (2 ^ J * m) ≤
      2 * Delta F m / (31 * (m : ℝ) ^ 4) * (1 - (1 / 32) ^ J) := by
  intro J
  have hmR : (0 : ℝ) < m := by exact_mod_cast hm
  induction J with
  | zero => simp
  | succ J ih =>
    have hmj : 0 < 2 ^ J * m := by positivity
    have e : 2 ^ (J + 1) * m = 2 * (2 ^ J * m) := by ring
    rw [e]
    have hdiff := fp_diff F hmj
    obtain ⟨h0, h1⟩ := delta_seq hs12 hs23 hs34 hS hR hm hD J
    have hD0 := delta_nonneg hs12 hs23 hs34 hS hm
    have hx : (0 : ℝ) < 2 ^ J := by positivity
    have step1 : Delta F (2 ^ J * m) / (16 * ((2 ^ J * m : ℕ) : ℝ) ^ 4) ≤
        (Delta F m / 2 ^ J) / (16 * ((2 ^ J * m : ℕ) : ℝ) ^ 4) :=
      div_le_div_of_nonneg_right h1 (by push_cast; positivity)
    have h32 : (1 / 32 : ℝ) ^ J = 1 / ((2 : ℝ) ^ J) ^ 5 := by
      rw [show (32 : ℝ) = 2 ^ 5 by norm_num, ← pow_mul, mul_comm, pow_mul, one_div_pow]
    have eq1 : (Delta F m / 2 ^ J) / (16 * ((2 ^ J * m : ℕ) : ℝ) ^ 4) =
        2 * Delta F m / (31 * (m : ℝ) ^ 4) * ((1 / 32) ^ J - (1 / 32) ^ (J + 1)) := by
      have h32' : (1 / 32 : ℝ) ^ (J + 1) = 1 / ((2 : ℝ) ^ J) ^ 5 / 32 := by rw [pow_succ, h32]; ring
      rw [h32', h32]
      push_cast
      field_simp
      ring
    have : fp F (2 ^ J * m) (2 ^ J * m) (2 ^ J * m) (2 ^ J * m) -
        fp F (2 * (2 ^ J * m)) (2 * (2 ^ J * m)) (2 * (2 ^ J * m)) (2 * (2 ^ J * m)) ≤
        2 * Delta F m / (31 * (m : ℝ) ^ 4) * ((1 / 32) ^ J - (1 / 32) ^ (J + 1)) := by
      rw [hdiff]; linarith
    have e2 : 2 * Delta F m / (31 * (m : ℝ) ^ 4) * (1 - (1 / 32) ^ (J + 1)) =
        2 * Delta F m / (31 * (m : ℝ) ^ 4) * (1 - (1 / 32) ^ J) +
        2 * Delta F m / (31 * (m : ℝ) ^ 4) * ((1 / 32) ^ J - (1 / 32) ^ (J + 1)) := by ring
    linarith

include hs12 hs23 hs34 hS hR in
theorem interpolation_pf (m : ℕ) (hm : 0 < m) (hD : Delta F m ≤ 1 / 512)
    (a b c : ℕ) (ha : m ≤ a) (hb : m ≤ b) (hc : m ≤ c) (r : ℕ → ℝ) (L : ℝ)
    (hrep : Rep F a b c r L) :
    Real.log (1 + sT r m) ≤ 2 * Delta F m * ((a : ℝ) * b * c) / (31 * (m : ℝ) ^ 3) := by
  have hmR : (0 : ℝ) < m := by exact_mod_cast hm
  have ha0 : 0 < a := lt_of_lt_of_le hm ha
  have hb0 : 0 < b := lt_of_lt_of_le hm hb
  have hc0 : 0 < c := lt_of_lt_of_le hm hc
  have haR : (0 : ℝ) < a := by exact_mod_cast ha0
  have hbR : (0 : ℝ) < b := by exact_mod_cast hb0
  have hcR : (0 : ℝ) < c := by exact_mod_cast hc0
  have hVpos : (0 : ℝ) < (a : ℝ) * b * c := by positivity
  have hD0 := delta_nonneg hs12 hs23 hs34 hS hm
  set c0 : ℝ := 2 * Delta F m / (31 * (m : ℝ) ^ 4) with hc0def
  have hc0nn : 0 ≤ c0 := by positivity
  have tele : ∀ J : ℕ, fp F m m m m - fp F (2 ^ J * m) (2 ^ J * m) (2 ^ J * m) (2 ^ J * m) ≤ c0 := by
    intro J
    have := telescope hs12 hs23 hs34 hS hR hm hD J
    have hq : (0 : ℝ) ≤ (1 / 32) ^ J := by positivity
    have hq1 : ((1 : ℝ) / 32) ^ J ≤ 1 := pow_le_one₀ (by norm_num) (by norm_num)
    nlinarith
  have hLge : fp F m m m m - c0 ≤ L / ((a : ℝ) * b * c) := by
    by_contra hlt
    push Not at hlt
    set ε : ℝ := fp F m m m m - c0 - L / ((a : ℝ) * b * c) with hε
    have hεpos : 0 < ε := by rw [hε]; linarith
    set h1 : ℝ := Real.log (1 + sT r 1) with hh1
    have hh1nn : 0 ≤ h1 := h_nonneg r hrep.1 1
    obtain ⟨M, hM⟩ := exists_nat_gt (h1 / (((a : ℝ) * b * c) * ε))
    have hMpos : 0 < M := by
      have : (0 : ℝ) < M := lt_of_le_of_lt (by positivity) hM
      exact_mod_cast this
    have hMR : (0 : ℝ) < M := by exact_mod_cast hMpos
    set J := a + b + c + M with hJ
    have hJlt : J < 2 ^ J := Nat.lt_two_pow_self
    have hbig : ∀ x : ℕ, x ≤ J → x ≤ 2 ^ J * m := fun x hx =>
      le_trans (le_trans hx hJlt.le) (Nat.le_mul_of_pos_right _ hm)
    have hmono := mono_all hs12 hs23 hs34 hS ha0 hb0 hc0 hMpos
      (hbig a (by omega)) (hbig b (by omega)) (hbig c (by omega)) (hbig M (by omega))
    have hJm : 0 < 2 ^ J * m := by positivity
    have hrepM := fp_rep hrep ha0 hb0 hc0 hMpos
    have hhM : Real.log (1 + sT r M) ≤ h1 :=
      h_anti r hrep.1 hrep.2.1 hrep.2.2.1 (by norm_num) (by omega)
    have hq : Real.log (1 + sT r M) / ((a : ℝ) * b * c * M) < ε := by
      have : Real.log (1 + sT r M) / ((a : ℝ) * b * c * M) ≤ h1 / (((a : ℝ) * b * c) * M) := by
        apply div_le_div_of_nonneg_right hhM (by positivity)
      have h2 : h1 / (((a : ℝ) * b * c) * ε) < M := hM
      have h3 : h1 < M * (((a : ℝ) * b * c) * ε) := by
        rwa [div_lt_iff₀ (by positivity)] at h2
      have h4 : h1 / (((a : ℝ) * b * c) * M) < ε := by
        rw [div_lt_iff₀ (by positivity)]; nlinarith
      linarith
    have := tele J
    rw [hrepM] at hmono
    linarith
  have hmono2 := mono_all hs12 hs23 hs34 hS hm hm hm hm ha hb hc (le_refl m)
  have hrepm := fp_rep hrep ha0 hb0 hc0 hm
  rw [hrepm] at hmono2
  have hq : Real.log (1 + sT r m) / ((a : ℝ) * b * c * m) ≤ c0 := by linarith
  rw [div_le_iff₀ (by positivity)] at hq
  have e : c0 * ((a : ℝ) * b * c * m) = 2 * Delta F m * ((a : ℝ) * b * c) / (31 * (m : ℝ) ^ 3) := by
    rw [hc0def]; field_simp
  linarith

end main

section final
variable {F : ℕ → ℕ → ℕ → ℕ → ℝ}
variable (hs12 : ∀ a b c d, F a b c d = F b a c d) (hs23 : ∀ a b c d, F a b c d = F a c b d)
  (hs34 : ∀ a b c d, F a b c d = F a b d c) (hS : HypSpec F) (hR : HypRec F)

include hs12 hs23 hs34 hS hR in
theorem reciproque_Bstar_pf (n : ℕ) (hn : 0 < n) (hD : Delta F n ≤ 1 / 512) :
    2 * (1 / (31 * 2 ^ 23 * ((16 * n : ℕ) : ℝ) ^ 3)) * (96 * ((16 * n : ℕ) : ℝ)) ^ 3 ≤ 1 / 20 ∧
    ∀ a b c : ℕ, 16 * n ≤ a → 16 * n ≤ b → 16 * n ≤ c → ∀ (r : ℕ → ℝ) (L : ℝ), Rep F a b c r L →
      Real.log (1 + sT r (16 * n)) ≤ (1 / (31 * 2 ^ 23 * ((16 * n : ℕ) : ℝ) ^ 3)) * ((a : ℝ) * b * c) := by
  have hnR : (0 : ℝ) < n := by exact_mod_cast hn
  have hT : (0 : ℝ) < ((16 * n : ℕ) : ℝ) := by push_cast; positivity
  refine ⟨?_, ?_⟩
  · have : 2 * (1 / (31 * 2 ^ 23 * ((16 * n : ℕ) : ℝ) ^ 3)) * (96 * ((16 * n : ℕ) : ℝ)) ^ 3 = 27 / 3968 := by
      field_simp; ring
    rw [this]; norm_num
  · intro a b c ha hb hc r L hrep
    have s1 := step_bound hs12 hs23 hs34 hS hR hn hD (le_refl _)
    have h1 : Delta F (2 * n) ≤ 1 / 1024 := by norm_num at s1; linarith
    have s2 := step_bound hs12 hs23 hs34 hS hR (by omega : 0 < 2 * n) h1 (by norm_num)
    have h2 : Delta F (2 * (2 * n)) ≤ 1 / 4096 := by norm_num at s2; linarith
    have s3 := step_bound hs12 hs23 hs34 hS hR (by omega : 0 < 2 * (2 * n)) h2 (by norm_num)
    have h3 : Delta F (2 * (2 * (2 * n))) ≤ 1 / 65536 := by norm_num at s3; linarith
    have s4 := step_bound hs12 hs23 hs34 hS hR (by omega : 0 < 2 * (2 * (2 * n))) h3 (by norm_num)
    have h4 : Delta F (16 * n) ≤ 1 / 16777216 := by
      have e : 16 * n = 2 * (2 * (2 * (2 * n))) := by ring
      rw [e]; norm_num at s4; linarith
    have hI := interpolation_pf hs12 hs23 hs34 hS hR (16 * n) (by omega)
      (by have : Delta F (16 * n) ≤ 1 / 16777216 := h4; linarith) a b c ha hb hc r L hrep
    have hV : (0 : ℝ) ≤ (a : ℝ) * b * c := by positivity
    have hstep : 2 * Delta F (16 * n) * ((a : ℝ) * b * c) / (31 * ((16 * n : ℕ) : ℝ) ^ 3) ≤
        2 * (1 / 16777216) * ((a : ℝ) * b * c) / (31 * ((16 * n : ℕ) : ℝ) ^ 3) := by
      apply div_le_div_of_nonneg_right _ (by positivity)
      have := mul_le_mul_of_nonneg_right h4 hV
      linarith
    have heq : 2 * (1 / 16777216 : ℝ) * ((a : ℝ) * b * c) / (31 * ((16 * n : ℕ) : ℝ) ^ 3) =
        (1 / (31 * 2 ^ 23 * ((16 * n : ℕ) : ℝ) ^ 3)) * ((a : ℝ) * b * c) := by
      field_simp; ring
    linarith

include hs12 hs23 hs34 hS hR in
lemma dexp (n : ℕ) (hn : 0 < n) (hD : Delta F n ≤ 1 / 512) :
    ∀ j : ℕ, 256 * Delta F (2 ^ j * n) ≤ (256 * Delta F n) ^ (2 ^ j) := by
  intro j
  induction j with
  | zero => simp
  | succ j ih =>
    have hmj : 0 < 2 ^ j * n := by positivity
    have e : 2 ^ (j + 1) * n = 2 * (2 ^ j * n) := by ring
    rw [e]
    obtain ⟨h0, h1⟩ := delta_seq hs12 hs23 hs34 hS hR hn hD j
    have hD0 := delta_nonneg hs12 hs23 hs34 hS hn
    have hp : (1 : ℝ) ≤ 2 ^ j := one_le_pow₀ (by norm_num)
    have hle : Delta F n / 2 ^ j ≤ Delta F n := div_le_self hD0 hp
    have hj : Delta F (2 ^ j * n) ≤ 1 / 512 := by linarith
    have := hR _ hmj hj
    calc 256 * Delta F (2 * (2 ^ j * n)) ≤ 256 * (256 * Delta F (2 ^ j * n) ^ 2) := by linarith
      _ = (256 * Delta F (2 ^ j * n)) ^ 2 := by ring
      _ ≤ ((256 * Delta F n) ^ (2 ^ j)) ^ 2 := pow_le_pow_left₀ (by linarith) ih 2
      _ = (256 * Delta F n) ^ (2 ^ (j + 1)) := by rw [← pow_mul, pow_succ]

include hs12 hs23 hs34 hS hR in
theorem trou_cubes_pf (n : ℕ) (hn : 0 < n) (hD : Delta F n ≤ 1 / 512)
    (N : ℕ) (hN : n ≤ N) (r : ℕ → ℝ) (L : ℝ) (hrep : Rep F N N N r L) :
    ∀ i, r i ^ n ≤ 256 * Delta F n := by
  intro i
  have hnR : (0 : ℝ) < n := by exact_mod_cast hn
  have hD0 := delta_nonneg hs12 hs23 hs34 hS hn
  set q : ℝ := 256 * Delta F n with hq
  have hq0 : 0 ≤ q := by rw [hq]; positivity
  have hq1 : q ≤ 1 / 2 := by rw [hq]; linarith
  -- choix de j
  have hdiv : 0 < N / n := Nat.div_pos hN hn
  set j := Nat.log 2 (N / n) with hj
  have hj1 : 2 ^ j ≤ N / n := Nat.pow_log_le_self 2 (by omega)
  have hj2 : N / n < 2 ^ (j + 1) := Nat.lt_pow_succ_log_self (by norm_num) (N / n)
  set p : ℕ := 2 ^ j with hp
  have hp0 : 0 < p := by positivity
  set m : ℕ := p * n with hm
  have hm0 : 0 < m := by positivity
  have hmN : m ≤ N := le_trans (Nat.mul_le_mul_right n hj1) (Nat.div_mul_le_self N n)
  have hNm : N < 2 * m := by
    have h1 : N < n * (N / n + 1) := Nat.lt_mul_div_succ N hn
    have h2 : N / n + 1 ≤ 2 * p := by rw [hp]; rw [pow_succ] at hj2; omega
    calc N < n * (N / n + 1) := h1
      _ ≤ n * (2 * p) := Nat.mul_le_mul_left n h2
      _ = 2 * m := by rw [hm]; ring
  have hmeq : m = 2 ^ j * n := by rw [hm, hp]
  have hdm := dexp hs12 hs23 hs34 hS hR n hn hD j
  rw [← hmeq] at hdm
  have hQ : q ^ p ≤ 1 / 2 := le_trans (pow_le_of_le_one hq0 (by linarith) (by omega)) hq1
  have hQ0 : 0 ≤ q ^ p := by positivity
  have hDm : Delta F m ≤ q ^ p / 256 := by
    have : 256 * Delta F m ≤ q ^ p := by rw [hp]; exact hdm
    linarith
  have hDm0 := delta_nonneg hs12 hs23 hs34 hS hm0
  have hI := interpolation_pf hs12 hs23 hs34 hS hR m hm0 (by linarith) N N N hmN hmN hmN r L hrep
  have hmR : (0 : ℝ) < m := by exact_mod_cast hm0
  have hNR : (N : ℝ) ≤ 2 * m := by exact_mod_cast hNm.le
  have hN0 : (0 : ℝ) ≤ N := by positivity
  have hN3 : (N : ℝ) * N * N ≤ 8 * (m : ℝ) ^ 3 := by
    have : (N : ℝ) * N * N ≤ (2 * m) * (2 * m) * (2 * m) := by gcongr
    nlinarith
  have hh : Real.log (1 + sT r m) ≤ q ^ p / 496 := by
    refine le_trans hI ?_
    rw [div_le_iff₀ (by positivity)]
    have h1 : 2 * Delta F m * ((N : ℝ) * N * N) ≤ 2 * Delta F m * (8 * (m : ℝ) ^ 3) :=
      mul_le_mul_of_nonneg_left hN3 (by positivity)
    have h2 : 2 * Delta F m * (8 * (m : ℝ) ^ 3) ≤ 2 * (q ^ p / 256) * (8 * (m : ℝ) ^ 3) := by
      apply mul_le_mul_of_nonneg_right _ (by positivity)
      linarith
    have h3 : 2 * (q ^ p / 256) * (8 * (m : ℝ) ^ 3) = q ^ p / 496 * (31 * (m : ℝ) ^ 3) := by
      ring
    linarith
  have hh0 := h_nonneg r hrep.1 m
  have hh1 : Real.log (1 + sT r m) ≤ 1 := by linarith
  -- sT = exp h - 1 ≤ 2h
  have hpos : 0 < 1 + sT r m := by linarith [sT_nonneg r hrep.1 m]
  have hexp : sT r m = Real.exp (Real.log (1 + sT r m)) - 1 := by
    rw [Real.exp_log hpos]; ring
  have hab := Real.abs_exp_sub_one_sub_id_le (x := Real.log (1 + sT r m))
    (by rw [abs_of_nonneg hh0]; exact hh1)
  have hsT : sT r m ≤ 2 * Real.log (1 + sT r m) := by
    have h5 := (abs_le.mp hab).2
    set x := Real.log (1 + sT r m)
    nlinarith
  have hri : r i ^ m ≤ sT r m := by
    have := Summable.le_tsum (hrep.2.2.1 m hm0) i (fun j _ => pow_nonneg (hrep.1 j) m)
    exact this
  have hfin : (r i ^ n) ^ p ≤ q ^ p := by
    rw [← pow_mul, mul_comm n p]
    have : r i ^ m ≤ q ^ p := by
      have : q ^ p / 496 * 2 ≤ q ^ p := by linarith
      linarith
    rw [hm] at this; exact this
  exact (pow_le_pow_iff_left₀ (pow_nonneg (hrep.1 i) n) hq0 (by omega)).mp hfin

end final

theorem facile (T0 : ℕ) (hT0 : 3 ≤ T0) (γ : ℝ) (hγ : 0 ≤ γ)
    (hg : 2 * γ * (96 * (T0 : ℝ)) ^ 3 ≤ 1 / 20) (n : ℝ) (hn : n = 2 * T0)
    (a0 a1 a2 a3 Δ : ℝ)
    (h0 : a0 ≤ γ * 2 ^ 0 * n ^ 3) (h1 : a1 ≤ γ * 2 ^ 1 * n ^ 3)
    (h2 : a2 ≤ γ * 2 ^ 2 * n ^ 3) (h3 : a3 ≤ γ * 2 ^ 3 * n ^ 3)
    (hΔ : Δ ≤ 16 * a0 + 8 * a1 + 4 * a2 + 2 * a3) :
    Δ ≤ 512 * γ * (T0 : ℝ) ^ 3 ∧ 512 * γ * (T0 : ℝ) ^ 3 ≤ 1 / 69120 ∧ (1 : ℝ) / 69120 < 1 / 512 := by
  subst hn
  have e1 : (96 * (T0 : ℝ)) ^ 3 = 884736 * (T0 : ℝ) ^ 3 := by ring
  have e2 : γ * (2 * (T0 : ℝ)) ^ 3 = 8 * (γ * (T0 : ℝ) ^ 3) := by ring
  rw [e1] at hg
  refine ⟨?_, ?_, by norm_num⟩
  · norm_num at h0 h1 h2 h3
    nlinarith [e2]
  · nlinarith

theorem interpolation (F : ℕ → ℕ → ℕ → ℕ → ℝ)
    (hs12 : ∀ a b c d, F a b c d = F b a c d) (hs23 : ∀ a b c d, F a b c d = F a c b d)
    (hs34 : ∀ a b c d, F a b c d = F a b d c)
    (hS : HypSpec F) (hR : HypRec F) (m : ℕ) (hm : 0 < m) (hD : Delta F m ≤ 1 / 512)
    (a b c : ℕ) (ha : m ≤ a) (hb : m ≤ b) (hc : m ≤ c) (r : ℕ → ℝ) (L : ℝ)
    (hrep : Rep F a b c r L) :
    Real.log (1 + sT r m) ≤ 2 * Delta F m * ((a : ℝ) * b * c) / (31 * (m : ℝ) ^ 3) :=
  interpolation_pf hs12 hs23 hs34 hS hR m hm hD a b c ha hb hc r L hrep

theorem reciproque_Bstar (F : ℕ → ℕ → ℕ → ℕ → ℝ)
    (hs12 : ∀ a b c d, F a b c d = F b a c d) (hs23 : ∀ a b c d, F a b c d = F a c b d)
    (hs34 : ∀ a b c d, F a b c d = F a b d c)
    (hS : HypSpec F) (hR : HypRec F) (n : ℕ) (hn : 0 < n) (hD : Delta F n ≤ 1 / 512) :
    2 * (1 / (31 * 2 ^ 23 * ((16 * n : ℕ) : ℝ) ^ 3)) * (96 * ((16 * n : ℕ) : ℝ)) ^ 3 ≤ 1 / 20 ∧
    ∀ a b c : ℕ, 16 * n ≤ a → 16 * n ≤ b → 16 * n ≤ c → ∀ (r : ℕ → ℝ) (L : ℝ), Rep F a b c r L →
      Real.log (1 + sT r (16 * n)) ≤ (1 / (31 * 2 ^ 23 * ((16 * n : ℕ) : ℝ) ^ 3)) * ((a : ℝ) * b * c) :=
  reciproque_Bstar_pf hs12 hs23 hs34 hS hR n hn hD

theorem trou_cubes (F : ℕ → ℕ → ℕ → ℕ → ℝ)
    (hs12 : ∀ a b c d, F a b c d = F b a c d) (hs23 : ∀ a b c d, F a b c d = F a c b d)
    (hs34 : ∀ a b c d, F a b c d = F a b d c)
    (hS : HypSpec F) (hR : HypRec F) (n : ℕ) (hn : 0 < n) (hD : Delta F n ≤ 1 / 512)
    (N : ℕ) (hN : n ≤ N) (r : ℕ → ℝ) (L : ℝ) (hrep : Rep F N N N r L) :
    ∀ i, r i ^ n ≤ 256 * Delta F n :=
  trou_cubes_pf hs12 hs23 hs34 hS hR n hn hD N hN r L hrep

end Reciproque

#print axioms Reciproque.facile
#print axioms Reciproque.interpolation
#print axioms Reciproque.reciproque_Bstar
#print axioms Reciproque.trou_cubes
