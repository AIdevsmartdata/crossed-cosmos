import KevYM.Certif.DobrushinLien.Donnees

/-!
# C2 — énoncé final (partie rationnelle)

Pour chacune des 160 boîtes en α ∈ [0, π] : tout polynôme réel en `w = κ²` dont les coefficients sont majorés
par les bornes Arb exportées est strictement négatif sur `[0, (59/50)²]`. Combiné (hors Lean) à la chaîne
Arb de `RAPPORT_C2.md`, cela donne `sup_{0<κ≤59/50, v} D(κ, v) < 8/(9π)`, puis le seuil via
`somme_dobrushin_lt_one`.
-/

namespace KevYM.Certif.DobrushinLien

theorem certs_neg : ∀ cs ∈ certs, bP cs 0 0 KW < 0 := by
  intro cs hcs
  have h := List.all_eq_true.mp certs_ok cs hcs
  simpa using h

theorem certificat_boites (cs : List ℚ) (hcs : cs ∈ certs) (es : List ℝ)
    (hes : List.Forall₂ (fun (e : ℝ) (c : ℚ) => e ≤ (c : ℝ)) es cs)
    (w : ℝ) (hw0 : 0 ≤ w) (hw : w ≤ (KW : ℝ)) : pR es 0 w < 0 :=
  sound cs 0 KW le_rfl (certs_neg cs hcs) es hes w (by simpa using hw0) hw

/-- `K² = (59/50)²` et `6·(π/16) < 59/50` : la boîte couvre tous les κ = β|s| ≤ 6β, β < π/16. -/
theorem KW_eq : (KW : ℝ) = ((59 : ℝ) / 50) ^ 2 := by
  simp [KW]; norm_num

end KevYM.Certif.DobrushinLien
