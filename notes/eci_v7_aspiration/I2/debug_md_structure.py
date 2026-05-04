"""
Debug: Verify M_d structure against LYD20's reported mass ratios.

LYD20 reports for Model VI at best-fit:
  m_u/m_c = 0.00204, m_c/m_t = 0.00268  → m_u/m_t ≈ 5.5e-6
  m_d/m_s = 0.05182, m_s/m_b = 0.01309  → m_d/m_b ≈ 6.8e-4

Our M_u gives m_u/m_t = 4.9e-4, m_c/m_t = 2.67e-3 → m_u/m_c = 0.184 (NOT 0.00204!)

So there's a parameter mismatch. The rep_assignment.md says:
  LYD20 best-fit: β_u/α_u = 62.2142, γ_u/α_u = 0.00104

But these give m_u/m_c = 0.184 not 0.00204. Let's check:
  LYD20's Table gives θ_12 = 0.22731 at τ = -0.4999 + 0.8958i.

This suggests the parameters in rep_assignment.md may NOT be the exact LYD20 values,
or the modular forms are normalized differently.

Let me check what beta_u/alpha_u values give the correct mass ratios.
"""

import numpy as np
from numpy import pi, sqrt, exp
from scipy.optimize import minimize
import sys
sys.path.insert(0, '/root/crossed-cosmos/notes/eci_v7_aspiration/H3')
from mass_matrix import M_u, M_d, modular_forms_weight1, modular_forms_all

TAU_LYD20 = -0.4999 + 0.8958j

def mass_ratios_u(tau, beta_over_alpha, gamma_over_alpha):
    """Compute up quark mass ratios given coupling ratios."""
    Mu = M_u(tau, 1.0, beta_over_alpha, gamma_over_alpha)
    from scipy.linalg import svd
    _, s, _ = svd(Mu)
    s = np.sort(s)
    if s[2] == 0 or s[1] == 0:
        return None, None, None
    return s[0]/s[2], s[1]/s[2], s[0]/s[1]

# Check current best-fit values
br, gr = 62.2142, 0.00104
r_ut, r_ct, r_uc = mass_ratios_u(TAU_LYD20, br, gr)
print(f"At LYD20 best-fit τ, β/α={br}, γ/α={gr}:")
print(f"  m_u/m_t = {r_ut:.5e}  (LYD20: ~5.5e-6)")
print(f"  m_c/m_t = {r_ct:.5e}  (LYD20: 2.68e-3)")
print(f"  m_u/m_c = {r_uc:.5e}  (LYD20: 2.04e-3)")

# The issue: β/α=62.2142 clearly sets the c-quark dominantly.
# But the weight-2 forms dominate row 1, and weight-5 forms dominate row 2.
# Let me check what singuar values are at the CM point vs LYD20 τ

print("\n\nLet me examine the modular forms at LYD20 τ:")
Y1, Y2, Y3 = modular_forms_weight1(TAU_LYD20)
f = modular_forms_all(Y1, Y2, Y3)
print(f"  |Y1_1|={abs(f['Y1_1']):.4f}, |Y1_2|={abs(f['Y1_2']):.4f}, |Y1_3|={abs(f['Y1_3']):.4f}")
print(f"  |Y2_3|={abs(f['Y2_3']):.4f}, |Y2_4|={abs(f['Y2_4']):.4f}, |Y2_5|={abs(f['Y2_5']):.4f}")
print(f"  |Y5_3|={abs(f['Y5_3']):.4f}, |Y5_4|={abs(f['Y5_4']):.4f}, |Y5_5|={abs(f['Y5_5']):.4f}")
print(f"  |Y5_6|={abs(f['Y5_6']):.4f}, |Y5_7|={abs(f['Y5_7']):.4f}, |Y5_8|={abs(f['Y5_8']):.4f}")
print(f"  |Y5_9|={abs(f['Y5_9']):.4f}, |Y5_10|={abs(f['Y5_10']):.4f}, |Y5_11|={abs(f['Y5_11']):.4f}")

# At LYD20 τ, let me manually compute singular values of M_u
Mu = M_u(TAU_LYD20, 1.0, 62.2142, 0.00104)
print(f"\nM_u rows at LYD20 τ:")
print(f"  Row 0 (u^c, α=1):   {np.abs(Mu[0,:])}")
print(f"  Row 1 (c^c, β=62.2): {np.abs(Mu[1,:])}")
print(f"  Row 2 (t^c, γ=1e-3): {np.abs(Mu[2,:])}")

# Clearly row 1 (c^c) dominates with β=62, row 2 (t^c) with γ=1e-3 is tiny!
# This seems wrong - t^c should be heavy.
# Unless the coupling assignment is: LARGER index = heavier quark, but the coupling
# RATIO gamma_u/alpha_u = 0.00104 makes t^c the LIGHTEST, not the heaviest!
#
# Hypothesis: the coupling ratios are α_u/γ_u = 0.00104 and β_u/γ_u = 62.2142
# (i.e., α_u is the SMALLEST, γ_u is the LARGEST)
# This would make t^c (row 2, coupling γ_u) the HEAVIEST.

print("\n\nHypothesis: LYD20 best-fit parameterises γ_u as the LARGEST coupling")
print("Testing: α_u=0.00104, β_u=62.2142*0.00104, γ_u=1.0")
alt_alpha = 0.00104
alt_beta  = 62.2142 * 0.00104
alt_gamma = 1.0
Mu_alt = M_u(TAU_LYD20, alt_alpha, alt_beta, alt_gamma)
from scipy.linalg import svd as lsvd
_, s_alt, _ = lsvd(Mu_alt)
s_alt = np.sort(s_alt)
print(f"  Singular values: {s_alt}")
print(f"  m_u/m_t = {s_alt[0]/s_alt[2]:.5e}")
print(f"  m_c/m_t = {s_alt[1]/s_alt[2]:.5e}")
print(f"  m_u/m_c = {s_alt[0]/s_alt[1]:.5e}")

# Try: α_u is smallest (sets u quark), γ_u is largest (sets t quark)
# β_u/α_u = 62.2142 means β_u is intermediate
# γ_u/α_u = 0.00104 means γ_u << α_u << β_u  → β_u dominates → c^c heaviest??

# Actually, maybe the issue is the WEIGHT order:
# If t^c has modular weight 5, the Y^(5) forms are polynomials in Y_i
# At τ=i, Y^(5) forms might be very small due to the fixed-point structure!

print("\n\nAt τ=i, comparing form magnitudes:")
Y1i, Y2i, Y3i = modular_forms_weight1(1j)
fi = modular_forms_all(Y1i, Y2i, Y3i)
print(f"  |Y1_1|={abs(fi['Y1_1']):.4f}, |Y2_3|={abs(fi['Y2_3']):.6f}, |Y5_3|={abs(fi['Y5_3']):.6f}")
print(f"  Ratio |Y5|/|Y1| ~ {abs(fi['Y5_3'])/abs(fi['Y1_1']):.4f}")
print(f"  Ratio |Y2|/|Y1| ~ {abs(fi['Y2_3'])/abs(fi['Y1_1']):.4f}")

# At LYD20 best-fit τ:
print(f"\nAt LYD20 τ={TAU_LYD20}:")
print(f"  |Y1_1|={abs(f['Y1_1']):.4f}, |Y2_3|={abs(f['Y2_3']):.4f}, |Y5_3|={abs(f['Y5_3']):.4f}")
print(f"  Ratio |Y5|/|Y1| ~ {abs(f['Y5_3'])/abs(f['Y1_1']):.4f}")
print(f"  Ratio |Y2|/|Y1| ~ {abs(f['Y2_3'])/abs(f['Y1_1']):.4f}")

# The real issue: at LYD20 τ, are the form MAGNITUDES such that row2 (β=62.2, Y^(2))
# is LARGER than row0 (α=1, Y^(1))?
print("\nEffective coupling × form magnitude at LYD20 τ:")
print(f"  Row 0 (u^c): α * |Y1| = {1.0 * abs(f['Y1_1']):.4f}")
print(f"  Row 1 (c^c): β * |Y2| = {62.2142 * abs(f['Y2_3']):.4f}")
print(f"  Row 2 (t^c): γ * |Y5| = {0.00104 * abs(f['Y5_3']):.6f}")

# This clearly shows: row 2 (t^c) is SMALLEST, not heaviest. Bug confirmed.
# The coupling γ_u/α_u = 0.00104 makes t^c the LIGHTEST quark.
# But LYD20 reports m_c/m_t = 0.00268 → top is heaviest → t^c should have LARGEST coupling.
#
# CONCLUSION: The transcribed coupling ratios in rep_assignment.md are INVERTED.
# LYD20 best-fit should be:
#   γ_u/α_u = 62.2142  (t^c has LARGE coupling → heaviest)
#   β_u/α_u = 0.00104  (c^c has intermediate coupling)
# OR perhaps:
#   β_u is for t^c and γ_u is for c^c (row labeling swapped)

print("\n\nTesting corrected assignment: γ_u/α_u=62.2142, β_u/α_u=0.00104 (SWAPPED):")
Mu_swap = M_u(TAU_LYD20, 1.0, 0.00104, 62.2142)
_, s_swap, _ = lsvd(Mu_swap)
s_swap = np.sort(s_swap)
print(f"  Singular values: {s_swap}")
print(f"  m_u/m_t = {s_swap[0]/s_swap[2]:.5e}  (LYD20: ~5.5e-6)")
print(f"  m_c/m_t = {s_swap[1]/s_swap[2]:.5e}  (LYD20: 2.68e-3)")
print(f"  m_u/m_c = {s_swap[0]/s_swap[1]:.5e}  (LYD20: 2.04e-3)")

# The issue with (β=0.00104, γ=62.2142): which row is c^c and which is t^c?
# Row 1 (labeled c^c in code): β_u * [Y^(2)_3, Y^(2)_5, Y^(2)_4]
# Row 2 (labeled t^c in code): γ_u * [Y^(5)_3, Y^(5)_5, Y^(5)_4]
# If γ_u >> β_u, then row 2 (Y^(5)) dominates → that's the TOP quark row → correct!
# So β_u/α_u = 0.00104 and γ_u/α_u = 62.2142 might be the correct interpretation.

# But wait - in LYD20, the notation might be:
# they report β_u/α_u and γ_u/α_u where α_u is the TOP coupling and β_u, γ_u are smaller
# So the rows might be labeled differently.

# Let me try: what if row assignment is t^c=row0, c^c=row1, u^c=row2?
# Then: α_u ~ 62.2142 (top), β_u ~ 1.0 (charm), γ_u ~ 0.00104 (up)
# But LYD20 Table I says: u^c ~ 1̂ (weight 1), c^c ~ 1 (weight 2), t^c ~ 1̂' (weight 5)
# Row 0 = u^c (weight-1 forms), Row 1 = c^c (weight-2 forms), Row 2 = t^c (weight-5 forms)

# ANOTHER HYPOTHESIS: LYD20 normalises the forms differently.
# The forms Y^(k) in LYD20 may be normalised such that |Y^(1)|~1 but |Y^(5)| >> |Y^(1)|.
# Let's check the actual Y^(5) forms numerically.

print("\n\nNumerical values at LYD20 best-fit τ:")
print(f"  Y1_1 = {f['Y1_1']:.6f}")
print(f"  Y2_3 = {f['Y2_3']:.6f}")
print(f"  Y5_3 = {f['Y5_3']:.6f}")
print(f"  Y5_4 = {f['Y5_4']:.6f}")
print(f"  Y5_5 = {f['Y5_5']:.6f}")
