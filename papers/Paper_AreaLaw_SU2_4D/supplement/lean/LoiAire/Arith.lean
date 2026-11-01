import Mathlib
import LoiAire.DonneesM11Calcul

/-!
# (c) Arithmétique finale en rationnels exacts (`norm_num`)

* θ* = J* ρ'* < 1 pour m = 11 (théorème 1), valeur exacte 53686712485971/53687091200000 ;
* idem pour m = 13 (théorème 1′) et pour les certificats à petite mémoire (m = 3, 4, 5) ;
* constantes : 6 r̄*(1)/ρ'* > 1, H_max/H_min ≥ 1, K₀ ≈ 3,978, C* = K₀/(1 − θ*) ∈ (563935, 563936) ;
* décroissance des 13 poids p_n (nécessaire au comptage, lemme 7.1).
Tout est démontré (noyau).
-/

namespace LoiAire

/-- θ* (m = 11). -/
def theta11 : ℚ := (40674 / 100000) * (2639854083 / 2 ^ 30)

theorem theta11_eq : theta11 = 53686712485971 / 53687091200000 := by norm_num [theta11]

theorem theta11_lt_one : theta11 < 1 := by norm_num [theta11]

theorem theta11_pos : 0 < theta11 := by norm_num [theta11]

/-- β* = 2 J* = 0,81348 et J* ≤ 0,44 (domaine du lemme 6.1). -/
theorem beta11_eq : (2 : ℚ) * (40674 / 100000) = 81348 / 100000 := by norm_num

theorem J11_le : (40674 / 100000 : ℚ) ≤ 44 / 100 := by norm_num

/-- θ*₁₃ (m = 13, théorème 1′). -/
theorem theta13_eq : (40749 / 100000 : ℚ) * (2635005744 / 2 ^ 30) = 6710865566391 / 6710886400000 := by norm_num

theorem theta13_lt_one : (40749 / 100000 : ℚ) * (2635005744 / 2 ^ 30) < 1 := by norm_num

/-- Petites mémoires (certificats vérifiés par le noyau dans `CertPetits.lean`). -/
theorem theta3_lt_one : (39859 / 100000 : ℚ) * (2693834779 / 2 ^ 30) < 1 := by norm_num
theorem theta5_lt_one : (40219 / 100000 : ℚ) * (2669713701 / 2 ^ 30) < 1 := by norm_num

/-- Rapport 6 r̄*(1)/ρ'* (> 1 : nécessaire pour le cas n < m du §8). -/
def q11 : ℚ := 6 * (487896913543 / 2 ^ 40) / (2639854083 / 2 ^ 30)

theorem q11_gt_one : 1 < q11 := by norm_num [q11]

/-- K₀ = (6 r̄*(1)/ρ'*)^11 · H_max/H_min. -/
def K11 : ℚ := q11 ^ 11 * (1099511627776 / 663930282413)

theorem K11_bornes : 3978 / 1000 < K11 ∧ K11 < 3979 / 1000 := by
  constructor <;> norm_num [K11, q11]

/-- C* = K₀ / (1 − θ*). -/
def C11 : ℚ := K11 / (1 - theta11)

theorem C11_bornes : 563935 < C11 ∧ C11 < 563936 := by
  constructor <;> norm_num [C11, K11, q11, theta11]

/-- Les 13 poids sont décroissants (r̄ non croissant). -/
theorem p_m11_decroissants : ∀ i j : Fin 13, j ≤ i → p_m11.getD i.val 0 ≤ p_m11.getD j.val 0 := by
  decide

end LoiAire
