import Mathlib

theorem L1 (a0 a1 a2 a3 : ℝ) (h : a0^2 + a1^2 + a2^2 + a3^2 = 1) :
    1 - a0 = ((a0 - 1)^2 + a1^2 + a2^2 + a3^2) / 2 := by
  have : (a0 - 1)^2 = a0^2 - 2*a0 + 1 := by ring
  rw [this]; nlinarith

theorem L2a (s1 s2 al be w : ℝ) (h1 : |s1| ≤ |al|) (h2 : |s2| ≤ |be|) (hw : 0 ≤ w) :
    |s1 * s2| * w ≤ |al * be| * w := by
  have hprod : |s1 * s2| ≤ |al * be| := by
    rw [abs_mul, abs_mul]
    exact mul_le_mul h1 h2 (abs_nonneg _) (abs_nonneg _)
  exact mul_le_mul_of_nonneg_right hprod hw

theorem L2b (x : ℝ) : |Real.sin x| ≤ |x| := by
  have := Real.lipschitzWith_sin.dist_le_mul x 0
  simpa [Real.sin_zero, Real.dist_eq] using this

theorem L3 (beta r t1 t2 z1 z2 : ℝ) (hb : 0 < beta) (hr : 0 < r)
    (hreg : r^2 * Real.sqrt beta ≥ 1)
    (ht1 : |t1| ≤ r) (ht2 : |t2| ≤ r)
    (hz1 : 0 ≤ z1) (hz1' : z1 ≤ 1 / (r * Real.sqrt beta))
    (hz2 : 0 ≤ z2) (hz2' : z2 ≤ 1 / (r * Real.sqrt beta)) :
    |t1| * z2 + |t2| * z1 + z1 * z2 ≤ 3 / Real.sqrt beta := by
  have hsb : 0 < Real.sqrt beta := Real.sqrt_pos.mpr hb
  have hs2 : Real.sqrt beta ^ 2 = beta := Real.sq_sqrt (le_of_lt hb)
  have h1 : |t1| * z2 ≤ 1 / Real.sqrt beta := by
    calc |t1| * z2 ≤ r * (1 / (r * Real.sqrt beta)) :=
        mul_le_mul ht1 hz2' hz2 (le_of_lt hr)
      _ = 1 / Real.sqrt beta := by field_simp
  have h2 : |t2| * z1 ≤ 1 / Real.sqrt beta := by
    calc |t2| * z1 ≤ r * (1 / (r * Real.sqrt beta)) :=
        mul_le_mul ht2 hz1' hz1 (le_of_lt hr)
      _ = 1 / Real.sqrt beta := by field_simp
  have hprod : (1 / (r * Real.sqrt beta)) * (1 / (r * Real.sqrt beta)) = 1 / (r^2 * beta) := by
    rw [div_mul_div_comm, one_mul]
    have hsq : (r * Real.sqrt beta) * (r * Real.sqrt beta) = r^2 * (Real.sqrt beta)^2 := by ring
    rw [hsq, hs2]
  have hz1z2 : z1 * z2 ≤ 1 / (r^2 * beta) := by
    calc z1 * z2 ≤ (1 / (r * Real.sqrt beta)) * (1 / (r * Real.sqrt beta)) :=
        mul_le_mul hz1' hz2' hz2 (by positivity)
      _ = 1 / (r^2 * beta) := hprod
  have hassoc : (r^2 * Real.sqrt beta) * Real.sqrt beta = r^2 * beta := by
    have h : (r^2 * Real.sqrt beta) * Real.sqrt beta = r^2 * (Real.sqrt beta)^2 := by ring
    rw [h, hs2]
  have hle : Real.sqrt beta ≤ r^2 * beta := by
    calc Real.sqrt beta = 1 * Real.sqrt beta := by ring
      _ ≤ (r^2 * Real.sqrt beta) * Real.sqrt beta :=
        mul_le_mul_of_nonneg_right hreg (le_of_lt hsb)
      _ = r^2 * beta := hassoc
  have h3 : z1 * z2 ≤ 1 / Real.sqrt beta := by
    have := one_div_le_one_div_of_le hsb hle
    linarith
  have hsum : |t1| * z2 + |t2| * z1 + z1 * z2
      ≤ 1/Real.sqrt beta + 1/Real.sqrt beta + 1/Real.sqrt beta := by linarith
  have : 1/Real.sqrt beta + 1/Real.sqrt beta + 1/Real.sqrt beta = 3 / Real.sqrt beta := by ring
  linarith

theorem L4a (V : ℕ) (hV : 1 ≤ V) : 3 * (3 * V + 1) - 12 = 9 * V - 9 := by
  have : 3 * (3 * V + 1) = 9 * V + 3 := by ring
  omega

theorem L4b (V : ℚ) : (9 * V - 9) / 2 + 3 = (9 * V - 3) / 2 := by ring

theorem L4c (V : ℚ) : 9 * V / 2 - (9 * V - 3) / 2 = 3 / 2 := by ring

-- F2 in the exact form used: sin product bound feeding the commutator estimate
theorem F2scalar (al be : ℝ) : |Real.sin al * Real.sin be| ≤ |al * be| := by
  rw [abs_mul, abs_mul]
  exact mul_le_mul (L2b al) (L2b be) (abs_nonneg _) (abs_nonneg _)

#print axioms L1
#print axioms L2a
#print axioms L2b
#print axioms L3
#print axioms L4a
#print axioms L4b
#print axioms L4c
#print axioms F2scalar#print axioms L1
#print axioms L2a
#print axioms L2b
#print axioms L3
#print axioms L4a
#print axioms L4b
#print axioms L4c
#print axioms F2scalar
