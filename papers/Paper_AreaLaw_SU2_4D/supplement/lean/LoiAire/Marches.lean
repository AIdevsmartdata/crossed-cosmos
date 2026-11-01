import Mathlib
import LoiAire.Calcul

/-!
# Comptage des marches à mémoire `m` (lemmes 7.1 et 7.2 de PREUVE.md, partie combinatoire)

Représentation : un *historique* est la liste des pas déjà faits, le PLUS RÉCENT EN TÊTE :
`w = [d_{j-1}, d_{j-2}, …, d_1]`. Un *état* (mémoire `m`) est `w.take m`.

* `posList w = [P_1, …, P_len]` : `P_i` est la position du site visité `i` pas plus tôt, relativement au site
  courant (`P_i = -(d_{j-1} + ⋯ + d_{j-i})`, comme dans tm_cert/verif_cert).
* `Nglob w d = 1 + #{i ≥ 1 : P_i = d}` : nombre de visites (dans ℤ³) du nouveau site, nouveau passage compris.
* `Nwin m w d = 1 + #{1 ≤ i ≤ m : P_i = d}` : même nombre vu dans la fenêtre de mémoire `m` (`N_j^{(m)}`).
* `Ntor L w d` : nombre de visites du nouveau site sur le tore `(ℤ/Lℤ)³`.
* `Gsum wt n w` : somme, sur les `6ⁿ` prolongements de longueur `n` de l'historique `w`, du produit des poids de pas
  `wt (historique courant) (pas)`.
* `Tpow m f n s` : itérée `Tⁿ 𝟙` de l'opérateur de transfert `(T g)(s) = Σ_d f s d · g (shift m d s)` sur les états.

Théorème principal `borne_marches` (lemme 7.1) : si les poids de pas sont majorés par une fonction de l'état
`f (w.take m) d`, et si un certificat de Perron `T H ≤ ρ H` (H > 0 sur les états de longueur m) existe, alors
`Gsum wt (m + n) [] ≤ (6c)^m (H_max/H_min) ρⁿ`. Tout est démontré ici.
-/

namespace LoiAire

open Finset

/-- Nombre de visites dans ℤ³ (global). -/
def Nglob (w : List Dir) (d : Dir) : ℕ := 1 + (posList w).count (vec d)

/-- Projection ℤ³ → (ℤ/Lℤ)³. -/
def castT (L : ℕ) (p : ℤ × ℤ × ℤ) : ZMod L × ZMod L × ZMod L := ((p.1 : ZMod L), (p.2.1 : ZMod L), (p.2.2 : ZMod L))

/-- Nombre de visites sur le tore `(ℤ/Lℤ)³`. -/
def Ntor (L : ℕ) (w : List Dir) (d : Dir) : ℕ := 1 + ((posList w).map (castT L)).count (castT L (vec d))

theorem posList_length (w : List Dir) : (posList w).length = w.length := by
  induction w with
  | nil => rfl
  | cons d w ih => simp [posList, ih]

/-- Les `m` premières positions relatives ne dépendent que des `m` derniers pas. -/
theorem posList_take (w : List Dir) (m : ℕ) : posList (w.take m) = (posList w).take m := by
  induction w generalizing m with
  | nil => simp [posList]
  | cons d w ih =>
    cases m with
    | zero => simp [posList]
    | succ k => simp [posList, ih, List.map_take]

/-- La fenêtre ne dépend que de l'état. -/
theorem Nwin_take (m : ℕ) (w : List Dir) (d : Dir) : Nwin m (w.take m) d = Nwin m w d := by
  simp [Nwin, posList_take, List.take_take]

theorem count_le_count_map {α β : Type*} [BEq α] [LawfulBEq α] [BEq β] [LawfulBEq β] (f : α → β) (a : α) :
    ∀ l : List α, l.count a ≤ (l.map f).count (f a) := by
  intro l
  induction l with
  | nil => simp
  | cons x l ih =>
    simp only [List.count_cons, List.map_cons]
    by_cases hx : x = a
    · subst hx; simp; omega
    · have : (x == a) = false := by simpa using hx
      rw [this]
      split_ifs <;> simp_all <;> omega

/-- Lemme 7.2 (partie combinatoire) : fenêtre ≤ global ≤ tore. -/
theorem Nwin_le_Nglob (m : ℕ) (w : List Dir) (d : Dir) : Nwin m w d ≤ Nglob w d := by
  unfold Nwin Nglob
  have := (List.take_sublist m (posList w)).count_le (vec d)
  omega

theorem Nglob_le_Ntor (L : ℕ) (w : List Dir) (d : Dir) : Nglob w d ≤ Ntor L w d := by
  unfold Nglob Ntor
  have := count_le_count_map (castT L) (vec d) (posList w)
  omega

theorem Nwin_le_Ntor (L m : ℕ) (w : List Dir) (d : Dir) : Nwin m w d ≤ Ntor L w d :=
  (Nwin_le_Nglob m w d).trans (Nglob_le_Ntor L w d)

theorem one_le_Nwin (m : ℕ) (w : List Dir) (d : Dir) : 1 ≤ Nwin m w d := by unfold Nwin; omega

theorem take_cons_eq_shift (m : ℕ) (hm : 1 ≤ m) (d : Dir) (w : List Dir) :
    (d :: w).take m = shift m d (w.take m) := by
  obtain ⟨k, rfl⟩ : ∃ k, m = k + 1 := ⟨m - 1, by omega⟩
  simp [shift, List.take_take]

theorem shift_length (m : ℕ) (hm : 1 ≤ m) (d : Dir) (s : List Dir) (hs : s.length = m) :
    (shift m d s).length = m := by
  simp [shift, hs]

/-! ## Sommes sur les marches et opérateur de transfert -/

/-- Somme pondérée sur les `6ⁿ` prolongements de longueur `n` de l'historique `w`. -/
def Gsum (wt : List Dir → Dir → ℝ) : ℕ → List Dir → ℝ
  | 0, _ => 1
  | n + 1, w => ∑ d : Dir, wt w d * Gsum wt n (d :: w)

/-- Itérée `Tⁿ 𝟙` de l'opérateur de transfert à mémoire `m`. -/
def Tpow (m : ℕ) (f : List Dir → Dir → ℝ) : ℕ → List Dir → ℝ
  | 0, _ => 1
  | n + 1, s => ∑ d : Dir, f s d * Tpow m f n (shift m d s)

/-- Somme d'une fonction sur tous les historiques de longueur `len w + n` prolongeant `w`. -/
def sumHist (F : List Dir → ℝ) : ℕ → List Dir → ℝ
  | 0, w => F w
  | n + 1, w => ∑ d : Dir, sumHist F n (d :: w)

theorem Gsum_nonneg (wt : List Dir → Dir → ℝ) (hwt : ∀ w d, 0 ≤ wt w d) :
    ∀ n w, 0 ≤ Gsum wt n w := by
  intro n
  induction n with
  | zero => intro w; simp [Gsum]
  | succ n ih =>
    intro w; simp only [Gsum]
    exact Finset.sum_nonneg (fun d _ => mul_nonneg (hwt w d) (ih _))

theorem Tpow_nonneg (m : ℕ) (f : List Dir → Dir → ℝ) (hf : ∀ s d, 0 ≤ f s d) :
    ∀ n s, 0 ≤ Tpow m f n s := by
  intro n
  induction n with
  | zero => intro s; simp [Tpow]
  | succ n ih =>
    intro s; simp only [Tpow]
    exact Finset.sum_nonneg (fun d _ => mul_nonneg (hf s d) (ih _))

theorem Gsum_mono (wt₁ wt₂ : List Dir → Dir → ℝ) (h₁ : ∀ w d, 0 ≤ wt₁ w d)
    (h₁₂ : ∀ w d, wt₁ w d ≤ wt₂ w d) : ∀ n w, Gsum wt₁ n w ≤ Gsum wt₂ n w := by
  intro n
  induction n with
  | zero => intro w; simp [Gsum]
  | succ n ih =>
    intro w; simp only [Gsum]
    apply Finset.sum_le_sum
    intro d _
    exact mul_le_mul (h₁₂ w d) (ih _) (Gsum_nonneg wt₁ h₁ n _) ((h₁ w d).trans (h₁₂ w d))

/-- Majoration par la fenêtre : si `wt w d ≤ f (w.take m) d` pour les historiques de longueur ≥ m,
la somme sur les prolongements est majorée par l'itérée de l'opérateur de transfert sur l'état. -/
theorem Gsum_le_Tpow (m : ℕ) (hm : 1 ≤ m) (wt f : List Dir → Dir → ℝ) (hwt : ∀ w d, 0 ≤ wt w d)
    (hf : ∀ s d, 0 ≤ f s d) (hwin : ∀ w, m ≤ w.length → ∀ d, wt w d ≤ f (w.take m) d) :
    ∀ n w, m ≤ w.length → Gsum wt n w ≤ Tpow m f n (w.take m) := by
  intro n
  induction n with
  | zero => intro w _; simp [Gsum, Tpow]
  | succ n ih =>
    intro w hw
    simp only [Gsum, Tpow]
    apply Finset.sum_le_sum
    intro d _
    have h1 := ih (d :: w) (by simp; omega)
    rw [take_cons_eq_shift m hm d w] at h1
    exact mul_le_mul (hwin w hw d) h1 (Gsum_nonneg wt hwt n _) (hf _ d)

/-- Certificat de Perron sur les états de longueur `m` ⟹ croissance au plus `ρⁿ` (version états du lemme (a)). -/
theorem Tpow_le (m : ℕ) (hm : 1 ≤ m) (f : List Dir → Dir → ℝ) (hf : ∀ s d, 0 ≤ f s d)
    (H : List Dir → ℝ) (Hmin ρ : ℝ) (hHmin : 0 < Hmin) (hH : ∀ s, s.length = m → Hmin ≤ H s) (hρ : 0 ≤ ρ)
    (hcert : ∀ s, s.length = m → ∑ d, f s d * H (shift m d s) ≤ ρ * H s) :
    ∀ n s, s.length = m → Tpow m f n s ≤ ρ ^ n * H s / Hmin := by
  intro n
  induction n with
  | zero =>
    intro s hs
    simp only [Tpow, pow_zero, one_mul]
    rw [le_div_iff₀ hHmin, one_mul]
    exact hH s hs
  | succ n ih =>
    intro s hs
    simp only [Tpow]
    calc ∑ d, f s d * Tpow m f n (shift m d s)
        ≤ ∑ d, f s d * (ρ ^ n * H (shift m d s) / Hmin) := by
          apply Finset.sum_le_sum
          intro d _
          exact mul_le_mul_of_nonneg_left (ih _ (shift_length m hm d s hs)) (hf s d)
      _ = ρ ^ n / Hmin * ∑ d, f s d * H (shift m d s) := by
          rw [Finset.mul_sum]
          refine Finset.sum_congr rfl (fun d _ => ?_)
          ring
      _ ≤ ρ ^ n / Hmin * (ρ * H s) := by
          apply mul_le_mul_of_nonneg_left (hcert s hs)
          exact div_nonneg (pow_nonneg hρ n) hHmin.le
      _ = ρ ^ (n + 1) * H s / Hmin := by ring

theorem sumHist_le (F : List Dir → ℝ) (B : ℝ) :
    ∀ n w, (∀ u : List Dir, u.length = w.length + n → F u ≤ B) → sumHist F n w ≤ 6 ^ n * B := by
  intro n
  induction n with
  | zero => intro w hF; simpa [sumHist] using hF w (by simp)
  | succ n ih =>
    intro w hF
    simp only [sumHist]
    calc ∑ d : Dir, sumHist F n (d :: w) ≤ ∑ _d : Dir, 6 ^ n * B := by
          apply Finset.sum_le_sum
          intro d _
          exact ih (d :: w) (fun u hu => hF u (by simp at hu; omega))
      _ = 6 ^ (n + 1) * B := by simp [Finset.sum_const, Finset.card_univ]; ring

/-- Les `k` premiers pas majorés par une constante `c`. -/
theorem Gsum_split (wt : List Dir → Dir → ℝ) (c : ℝ) (hwt : ∀ w d, 0 ≤ wt w d ∧ wt w d ≤ c) (n : ℕ) :
    ∀ k w, Gsum wt (k + n) w ≤ c ^ k * sumHist (Gsum wt n) k w := by
  have hc : 0 ≤ c := (hwt [] 0).1.trans (hwt [] 0).2
  intro k
  induction k with
  | zero => intro w; simp [sumHist]
  | succ k ih =>
    intro w
    have e : k + 1 + n = (k + n) + 1 := by omega
    rw [e]
    simp only [Gsum, sumHist]
    calc ∑ d : Dir, wt w d * Gsum wt (k + n) (d :: w)
        ≤ ∑ d : Dir, c * (c ^ k * sumHist (Gsum wt n) k (d :: w)) := by
          apply Finset.sum_le_sum
          intro d _
          apply mul_le_mul (hwt w d).2 (ih _) (Gsum_nonneg wt (fun w d => (hwt w d).1) _ _) hc
      _ = c ^ (k + 1) * ∑ d : Dir, sumHist (Gsum wt n) k (d :: w) := by
          rw [Finset.mul_sum]
          refine Finset.sum_congr rfl (fun d _ => ?_)
          ring

theorem Gsum_le_pow (wt : List Dir → Dir → ℝ) (c : ℝ) (hwt : ∀ w d, 0 ≤ wt w d ∧ wt w d ≤ c) :
    ∀ n w, Gsum wt n w ≤ (6 * c) ^ n := by
  intro n
  induction n with
  | zero => intro w; simp [Gsum]
  | succ n ih =>
    intro w
    have hc : 0 ≤ c := (hwt [] 0).1.trans (hwt [] 0).2
    simp only [Gsum]
    calc ∑ d : Dir, wt w d * Gsum wt n (d :: w) ≤ ∑ _d : Dir, c * (6 * c) ^ n := by
          apply Finset.sum_le_sum
          intro d _
          exact mul_le_mul (hwt w d).2 (ih _) (Gsum_nonneg wt (fun w d => (hwt w d).1) _ _) hc
      _ = (6 * c) ^ (n + 1) := by simp [Finset.sum_const, Finset.card_univ]; ring

/-- **Lemme 7.1 (forme abstraite, démontrée).** Poids de pas `0 ≤ wt ≤ c`, majorés par une fonction de l'état
`f (w.take m) d` dès que l'historique a au moins `m` pas, et certificat de Perron `T_f H ≤ ρ H`,
`H_min ≤ H ≤ H_max` sur les états de longueur `m`. Alors
`Σ_{marches de longueur m+n} Π poids ≤ (6c)^m (H_max/H_min) ρⁿ`. -/
theorem borne_marches (m : ℕ) (hm : 1 ≤ m) (wt f : List Dir → Dir → ℝ) (c ρ Hmin Hmax : ℝ)
    (H : List Dir → ℝ) (hwt : ∀ w d, 0 ≤ wt w d ∧ wt w d ≤ c) (hf : ∀ s d, 0 ≤ f s d)
    (hwin : ∀ w, m ≤ w.length → ∀ d, wt w d ≤ f (w.take m) d)
    (hHmin : 0 < Hmin) (hH : ∀ s, s.length = m → Hmin ≤ H s ∧ H s ≤ Hmax) (hρ : 0 ≤ ρ)
    (hcert : ∀ s, s.length = m → ∑ d, f s d * H (shift m d s) ≤ ρ * H s) (n : ℕ) :
    Gsum wt (m + n) [] ≤ (6 * c) ^ m * (Hmax / Hmin) * ρ ^ n := by
  have hc : 0 ≤ c := (hwt [] 0).1.trans (hwt [] 0).2
  have h1 := Gsum_split wt c hwt n m []
  have h2 : sumHist (Gsum wt n) m [] ≤ 6 ^ m * (ρ ^ n * Hmax / Hmin) := by
    apply sumHist_le
    intro u hu
    simp at hu
    have hu' : m ≤ u.length := by omega
    have a := Gsum_le_Tpow m hm wt f (fun w d => (hwt w d).1) hf hwin n u hu'
    rw [List.take_of_length_le (by omega)] at a
    have b := Tpow_le m hm f hf H Hmin ρ hHmin (fun s hs => (hH s hs).1) hρ hcert n u hu
    calc Gsum wt n u ≤ Tpow m f n u := a
      _ ≤ ρ ^ n * H u / Hmin := b
      _ ≤ ρ ^ n * Hmax / Hmin := by
          apply div_le_div_of_nonneg_right _ hHmin.le
          exact mul_le_mul_of_nonneg_left (hH u hu).2 (pow_nonneg hρ n)
  calc Gsum wt (m + n) [] ≤ c ^ m * sumHist (Gsum wt n) m [] := h1
    _ ≤ c ^ m * (6 ^ m * (ρ ^ n * Hmax / Hmin)) := mul_le_mul_of_nonneg_left h2 (pow_nonneg hc m)
    _ = (6 * c) ^ m * (Hmax / Hmin) * ρ ^ n := by rw [mul_pow]; ring

/-- **Forme « pour tout n »** (fin du §8) : avec `K₀ := (6c/ρ)^m (H_max/H_min)`, si `6c ≥ ρ > 0` et
`H_max ≥ H_min`, alors `Σ_{|ω| = n} Π poids ≤ K₀ ρⁿ` pour TOUT `n ≥ 0` (y compris `n < m`). -/
theorem borne_marches_tout_n (m : ℕ) (hm : 1 ≤ m) (wt f : List Dir → Dir → ℝ) (c ρ Hmin Hmax : ℝ)
    (H : List Dir → ℝ) (hwt : ∀ w d, 0 ≤ wt w d ∧ wt w d ≤ c) (hf : ∀ s d, 0 ≤ f s d)
    (hwin : ∀ w, m ≤ w.length → ∀ d, wt w d ≤ f (w.take m) d)
    (hHmin : 0 < Hmin) (hH : ∀ s, s.length = m → Hmin ≤ H s ∧ H s ≤ Hmax) (hρ : 0 < ρ)
    (hcρ : ρ ≤ 6 * c) (hHH : Hmin ≤ Hmax)
    (hcert : ∀ s, s.length = m → ∑ d, f s d * H (shift m d s) ≤ ρ * H s) (n : ℕ) :
    Gsum wt n [] ≤ ((6 * c) / ρ) ^ m * (Hmax / Hmin) * ρ ^ n := by
  have hq : 1 ≤ (6 * c) / ρ := by rw [le_div_iff₀ hρ]; linarith
  have hHq : 1 ≤ Hmax / Hmin := by rw [le_div_iff₀ hHmin]; linarith
  by_cases hn : m ≤ n
  · obtain ⟨k, rfl⟩ : ∃ k, n = m + k := ⟨n - m, by omega⟩
    have := borne_marches m hm wt f c ρ Hmin Hmax H hwt hf hwin hHmin hH hρ.le hcert k
    calc Gsum wt (m + k) [] ≤ (6 * c) ^ m * (Hmax / Hmin) * ρ ^ k := this
      _ = ((6 * c) / ρ) ^ m * (Hmax / Hmin) * ρ ^ (m + k) := by
          rw [div_pow, pow_add]; field_simp
  · push Not at hn
    have h := Gsum_le_pow wt c hwt n []
    calc Gsum wt n [] ≤ (6 * c) ^ n := h
      _ = ((6 * c) / ρ) ^ n * ρ ^ n := by rw [div_pow]; field_simp
      _ ≤ ((6 * c) / ρ) ^ m * ρ ^ n := by
          apply mul_le_mul_of_nonneg_right _ (pow_nonneg hρ.le n)
          exact pow_le_pow_right₀ hq hn.le
      _ ≤ ((6 * c) / ρ) ^ m * (Hmax / Hmin) * ρ ^ n := by
          rw [mul_assoc]
          apply mul_le_mul_of_nonneg_left _ (pow_nonneg (by linarith) m)
          nlinarith [pow_nonneg hρ.le n]

end LoiAire
