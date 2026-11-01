import Mathlib

/-!
# (a) Lemme de Perron abstrait : un certificat borne le nombre (pondéré) de marches

Énoncé : `A` matrice à coefficients ≥ 0 sur un ensemble fini d'états, `v > 0`, `A v ≤ ρ v` composante par
composante. Alors la somme pondérée des marches de longueur `n` issues de `s` (c'est-à-dire `(Aⁿ 𝟙)(s)`)
est majorée par `ρⁿ · v(s) / min v`, donc par `C ρⁿ` avec `C = max v / min v`.

Tout est démontré ici (aucune hypothèse supplémentaire).
-/

namespace LoiAire

open Finset

variable {S : Type*} [Fintype S]

/-- Somme pondérée des marches de longueur `n` issues de `s` :
`marches A n s = Σ_{t₁,…,tₙ} A s t₁ · A t₁ t₂ ⋯ A tₙ₋₁ tₙ` (définition par récurrence). -/
def marches (A : S → S → ℝ) : ℕ → S → ℝ
  | 0, _ => 1
  | n + 1, s => ∑ t, A s t * marches A n t

theorem marches_nonneg (A : S → S → ℝ) (hA : ∀ s t, 0 ≤ A s t) : ∀ n s, 0 ≤ marches A n s := by
  intro n
  induction n with
  | zero => intro s; simp [marches]
  | succ n ih =>
    intro s
    simp only [marches]
    exact Finset.sum_nonneg (fun t _ => mul_nonneg (hA s t) (ih t))

/-- **Lemme (a).** Certificat de Perron ⟹ borne exponentielle des marches. -/
theorem marches_le_certificat (A : S → S → ℝ) (hA : ∀ s t, 0 ≤ A s t)
    (v : S → ℝ) (ρ c : ℝ) (hc : 0 < c) (hvc : ∀ s, c ≤ v s) (hρ : 0 ≤ ρ)
    (hAv : ∀ s, ∑ t, A s t * v t ≤ ρ * v s) :
    ∀ n s, marches A n s ≤ ρ ^ n * v s / c := by
  intro n
  induction n with
  | zero =>
    intro s
    simp only [marches, pow_zero, one_mul]
    rw [le_div_iff₀ hc, one_mul]
    exact hvc s
  | succ n ih =>
    intro s
    simp only [marches]
    calc ∑ t, A s t * marches A n t ≤ ∑ t, A s t * (ρ ^ n * v t / c) := by
          apply Finset.sum_le_sum
          intro t _
          exact mul_le_mul_of_nonneg_left (ih t) (hA s t)
      _ = ρ ^ n / c * ∑ t, A s t * v t := by
          rw [Finset.mul_sum]
          refine Finset.sum_congr rfl (fun t _ => ?_)
          ring
      _ ≤ ρ ^ n / c * (ρ * v s) := by
          apply mul_le_mul_of_nonneg_left (hAv s)
          exact div_nonneg (pow_nonneg hρ n) hc.le
      _ = ρ ^ (n + 1) * v s / c := by ring

/-- Forme « constante » : `marches A n s ≤ (V / c) ρⁿ` si `c ≤ v ≤ V`. -/
theorem marches_le_C_rho_pow (A : S → S → ℝ) (hA : ∀ s t, 0 ≤ A s t)
    (v : S → ℝ) (ρ c V : ℝ) (hc : 0 < c) (hvc : ∀ s, c ≤ v s) (hvV : ∀ s, v s ≤ V) (hρ : 0 ≤ ρ)
    (hAv : ∀ s, ∑ t, A s t * v t ≤ ρ * v s) (n : ℕ) (s : S) :
    marches A n s ≤ (V / c) * ρ ^ n := by
  have h := marches_le_certificat A hA v ρ c hc hvc hρ hAv n s
  calc marches A n s ≤ ρ ^ n * v s / c := h
    _ ≤ ρ ^ n * V / c := by
        apply div_le_div_of_nonneg_right _ hc.le
        exact mul_le_mul_of_nonneg_left (hvV s) (pow_nonneg hρ n)
    _ = (V / c) * ρ ^ n := by ring

/-- Lien avec les puissances de matrices : `marches A n s = Σ_t (Aⁿ)_{s t}`. -/
theorem marches_eq_pow [DecidableEq S] (A : S → S → ℝ) :
    ∀ n s, marches A n s = ∑ t, ((Matrix.of A) ^ n) s t := by
  intro n
  induction n with
  | zero =>
    intro s
    simp [marches, Matrix.one_apply]
  | succ n ih =>
    intro s
    simp only [marches, ih, pow_succ', Matrix.mul_apply, Matrix.of_apply]
    rw [Finset.sum_comm]
    refine Finset.sum_congr rfl (fun t _ => ?_)
    rw [Finset.mul_sum]

/-- Lien avec le comptage explicite des chemins : `marches A n s` est la somme, sur les suites
`p : Fin n → S`, du produit des poids `A p₀ p₁ ⋯` le long du chemin `s, p 0, …, p (n-1)`. -/
def poidsChemin (A : S → S → ℝ) : (n : ℕ) → S → (Fin n → S) → ℝ
  | 0, _, _ => 1
  | n + 1, s, p => A s (p 0) * poidsChemin A n (p 0) (fun i => p i.succ)

theorem marches_eq_sum_chemins (A : S → S → ℝ) :
    ∀ n s, marches A n s = ∑ p : Fin n → S, poidsChemin A n s p := by
  intro n
  induction n with
  | zero => intro s; simp [marches, poidsChemin]
  | succ n ih =>
    intro s
    simp only [marches, poidsChemin, ih]
    rw [← (Fin.consEquiv (fun _ : Fin (n + 1) => S)).sum_comp]
    rw [Fintype.sum_prod_type]
    refine Finset.sum_congr rfl (fun t _ => ?_)
    rw [Finset.mul_sum]
    refine Finset.sum_congr rfl (fun q _ => ?_)
    simp [Fin.consEquiv]

/-- Cas d'un graphe (matrice 0/1) : le NOMBRE de chemins de longueur `n` issus de `s` est `≤ (V/c) ρⁿ`. -/
theorem nombre_chemins_le (adj : S → S → Prop) [DecidableRel adj]
    (v : S → ℝ) (ρ c V : ℝ) (hc : 0 < c) (hvc : ∀ s, c ≤ v s) (hvV : ∀ s, v s ≤ V) (hρ : 0 ≤ ρ)
    (hAv : ∀ s, ∑ t, (if adj s t then (1 : ℝ) else 0) * v t ≤ ρ * v s) (n : ℕ) (s : S) :
    marches (fun a b => if adj a b then (1 : ℝ) else 0) n s ≤ (V / c) * ρ ^ n :=
  marches_le_C_rho_pow _ (fun a b => by split_ifs <;> norm_num) v ρ c V hc hvc hvV hρ hAv n s

end LoiAire
