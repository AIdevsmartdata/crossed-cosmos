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
  (∀ i, 0 ≤ r i) ∧ (∀ i, r i ≤ 1) ∧ (∀ d : ℕ, 0 < d → Summable (fun i => r i ^ d)) ∧
  ∀ d : ℕ, 0 < d → F a b c d = (d : ℝ) * L + Real.log (1 + sT r d)

def HypSpec (F : ℕ → ℕ → ℕ → ℕ → ℝ) : Prop :=
  ∀ a b c : ℕ, 0 < a → 0 < b → 0 < c → ∃ (r : ℕ → ℝ) (L : ℝ), Rep F a b c r L

/-- Récurrence de doublement (théorème publié, hypothèse nommée ici). -/
def HypRec (F : ℕ → ℕ → ℕ → ℕ → ℝ) : Prop :=
  ∀ m : ℕ, 0 < m → Delta F m ≤ 1 / 512 → Delta F (2 * m) ≤ 256 * Delta F m ^ 2

/-- (a) Le sens facile publié : (B*) ⟹ Δ(2T0) ≤ 2⁻⁹, forme abstraite. -/
theorem facile (T0 : ℕ) (hT0 : 3 ≤ T0) (γ : ℝ) (hγ : 0 ≤ γ)
    (hg : 2 * γ * (96 * (T0 : ℝ)) ^ 3 ≤ 1 / 20) (n : ℝ) (hn : n = 2 * T0)
    (a0 a1 a2 a3 Δ : ℝ)
    (h0 : a0 ≤ γ * 2 ^ 0 * n ^ 3) (h1 : a1 ≤ γ * 2 ^ 1 * n ^ 3)
    (h2 : a2 ≤ γ * 2 ^ 2 * n ^ 3) (h3 : a3 ≤ γ * 2 ^ 3 * n ^ 3)
    (hΔ : Δ ≤ 16 * a0 + 8 * a1 + 4 * a2 + 2 * a3) :
    Δ ≤ 512 * γ * (T0 : ℝ) ^ 3 ∧ 512 * γ * (T0 : ℝ) ^ 3 ≤ 1 / 69120 ∧ (1 : ℝ) / 69120 < 1 / 512 := by
  sorry

/-- (b1) Interpolation : h_t(m) ≤ 2 Δ(m) V /(31 m³) pour tout tore de côtés ≥ m. -/
theorem interpolation (F : ℕ → ℕ → ℕ → ℕ → ℝ)
    (hs12 : ∀ a b c d, F a b c d = F b a c d) (hs23 : ∀ a b c d, F a b c d = F a c b d)
    (hs34 : ∀ a b c d, F a b c d = F a b d c)
    (hS : HypSpec F) (hR : HypRec F) (m : ℕ) (hm : 0 < m) (hD : Delta F m ≤ 1 / 512)
    (a b c : ℕ) (ha : m ≤ a) (hb : m ≤ b) (hc : m ≤ c) (r : ℕ → ℝ) (L : ℝ)
    (hrep : Rep F a b c r L) :
    Real.log (1 + sT r m) ≤ 2 * Delta F m * ((a : ℝ) * b * c) / (31 * (m : ℝ) ^ 3) := by
  sorry

/-- (b2) LA RÉCIPROQUE : Δ(n) ≤ 2⁻⁹ ⟹ (B*) à T0 = 16 n, avec γ = 1/(31·2²³·T0³) et 2γ(96T0)³ ≤ 1/20. -/
theorem reciproque_Bstar (F : ℕ → ℕ → ℕ → ℕ → ℝ)
    (hs12 : ∀ a b c d, F a b c d = F b a c d) (hs23 : ∀ a b c d, F a b c d = F a c b d)
    (hs34 : ∀ a b c d, F a b c d = F a b d c)
    (hS : HypSpec F) (hR : HypRec F) (n : ℕ) (hn : 0 < n) (hD : Delta F n ≤ 1 / 512) :
    2 * (1 / (31 * 2 ^ 23 * ((16 * n : ℕ) : ℝ) ^ 3)) * (96 * ((16 * n : ℕ) : ℝ)) ^ 3 ≤ 1 / 20 ∧
    ∀ a b c : ℕ, 16 * n ≤ a → 16 * n ≤ b → 16 * n ≤ c → ∀ (r : ℕ → ℝ) (L : ℝ), Rep F a b c r L →
      Real.log (1 + sT r (16 * n)) ≤ (1 / (31 * 2 ^ 23 * ((16 * n : ℕ) : ℝ) ^ 3)) * ((a : ℝ) * b * c) := by
  sorry

/-- (b3) Trou sur TOUS les cubes entiers N ≥ n (non dyadiques compris) : r_i^n ≤ 256 Δ(n) ≤ 1/2. -/
theorem trou_cubes (F : ℕ → ℕ → ℕ → ℕ → ℝ)
    (hs12 : ∀ a b c d, F a b c d = F b a c d) (hs23 : ∀ a b c d, F a b c d = F a c b d)
    (hs34 : ∀ a b c d, F a b c d = F a b d c)
    (hS : HypSpec F) (hR : HypRec F) (n : ℕ) (hn : 0 < n) (hD : Delta F n ≤ 1 / 512)
    (N : ℕ) (hN : n ≤ N) (r : ℕ → ℝ) (L : ℝ) (hrep : Rep F N N N r L) :
    ∀ i, r i ^ n ≤ 256 * Delta F n := by
  sorry

end Reciproque
