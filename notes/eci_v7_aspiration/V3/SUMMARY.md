# V3 — Independent Re-Verification of I1.5 Lepton Sector Claims

**Date**: 2026-05-04  
**Script**: `/tmp/agents_v647_evening/V3/v3_lepton_verify.py` (fresh; NOT reusing I1.5/lepton_unified.py)

---

## VERDICT: [I1.5 NUANCED — lepton sector at τ=i works with correct rep + re-fitted params, but is a 0-DOF fit, not a structural prediction]

---

## V3.A — LYD20 unified-model lepton assignment (TeX lines 1483–1495, direct)

Field assignments (TeX line 1483):
  L ~ 3, k=2; E1^c ~ 1, k=2 → Y^(4)_3; E2^c ~ 1, k=0 → Y^(2)_3; E3^c ~ 1̂', k=1 → Y^(3)_hat3

Charged-lepton matrix eq:Ml (TeX lines 1491–1495): Row 0 uses weight-4 Y^(4)_3 — distinct from all four C1–C4 cases which use weight ≤3 for row 0.

LYD20 unified best-fit (TeX lines 1531–1538): τ=−0.2123+1.5201i (quark-driven), β_e/α_e=0.0187, γ_e/α_e=0.1466, α_e v_d=16.888 MeV. LYD20 lepton targets (TeX line 928–930): m_e/m_μ=0.0048±0.0002, m_μ/m_τ=0.0565±0.0045.

---

## V3.B — Fresh computation results

**Weight-4 forms at τ=i** (non-zero — this is the structural key):
  Y4_4(i)=−128.37 (real), Y4_5(i)=Y4_6(i)=+64.19 (real). Constraint Y1²+2Y2Y3=1.6×10⁻¹⁵ ✓

**LYD20's quoted params (β/α=0.0187, γ/α=0.1466) applied at τ=i:**
  m_e/m_μ=2.160×10⁻² (+347% off PDG 4.836×10⁻³) — FAILS BADLY

**Same quoted params at LYD20's fitted τ=−0.2123+1.5201i:**
  m_e/m_μ=4.946×10⁻³ (+2.3% off PDG) ✓  m_μ/m_τ=5.577×10⁻² (−6.2% off) ✓

**Re-fitted (β/α, γ/α) optimized at τ=i:**
  β_e/α_e=0.5775, γ_e/α_e=1.32×10⁻³ (factor ~31× and ~111× from LYD20's values)
  m_e/m_μ=4.836×10⁻³ (0.0% off PDG) ✓  m_μ/m_τ=5.946×10⁻² (0.0% off) ✓  χ²=0.000

I1.5's numbers (m_e/m_μ≈4.80×10⁻³, 0.8% off; m_μ/m_τ≈5.65×10⁻², 5.0% off) are confirmed achievable at τ=i. But the parameters used differ completely from LYD20's quoted values.

---

## V3.C — DOF analysis

At fixed τ=i: 2 free Yukawa ratios (β/α, γ/α) fit 2 mass-ratio observables → DOF=0.

Critical V3.D sweep: chi²=0 achievable at EVERY tested τ value (τ=1.2i, 1.5i, 2.0i, −0.2+1.5i, 0.3+i — all give min χ²=0.000). τ=i is not singled out. The LYD20 unified model generically admits an exact solution for any target (r1, r2) at any τ where the matrix is non-degenerate. This is a property of having 2 free parameters to fit 2 observables.

---

## V3.D — Root cause of I1's failure

I1 used Case C1 (TeX lines 605–614): row 0 uses weight-1 Y^(1)_hat3'. At τ=i (CM-point fixed by S), weight-1 forms vanish → row 0 is zero → m_e/m_μ~10⁻¹⁵. This is C1-specific, not a universal CM-point pathology.

LYD20's unified model uses weight-4 Y^(4)_3 for row 0, which is non-zero at τ=i. I1.5's structural correction is verified correct.

---

## What I1.5's "victory" actually means physically

**Confirmed**: The LYD20 unified model's lepton matrix is non-degenerate at τ=i; a solution exists and I1's catastrophe was a rep-assignment bug. This is a real correction.

**Nuanced**: "v7 LEPTON CLOSURE OK" is a viability statement, not a prediction. With τ fixed externally (by v7's KMS/Maass-form mechanism), the 2 free Yukawa ratios absorb 2 lepton mass observables exactly — predictive content for the lepton sector = 0, given τ. The same closure works at any generic τ. The v7 case rests entirely on whether the KMS/Maass mechanism independently fixes τ=i; the lepton computation provides no independent evidence for or against it.
