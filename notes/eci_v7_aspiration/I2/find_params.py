"""
Find the correct LYD20 Model VI parameters by fitting to:
  m_c/m_t = 0.00268  (LYD20 reported)
  m_u/m_c = 0.00204  (LYD20 reported, equivalently m_u/m_t = 5.47e-6)

at τ = -0.4999 + 0.8958i.

Also independently: scan (β/α, γ/α) space to find the unique solution.

This will determine the correct parameter assignment.
"""

import numpy as np
from numpy import pi
from scipy.linalg import svd
from scipy.optimize import minimize
import sys
sys.path.insert(0, '/root/crossed-cosmos/notes/eci_v7_aspiration/H3')
from mass_matrix import M_u

TAU_LYD20 = -0.4999 + 0.8958j

LYD20_MC_MT = 0.00268
LYD20_MU_MC = 0.00204
LYD20_MU_MT = LYD20_MU_MC * LYD20_MC_MT

def get_mass_ratios(tau, beta_over_alpha, gamma_over_alpha):
    Mu = M_u(tau, 1.0, beta_over_alpha, gamma_over_alpha)
    _, s, _ = svd(Mu)
    s = np.sort(s)   # ascending: u < c < t
    if s[2] == 0:
        return np.inf, np.inf
    return s[1]/s[2], s[0]/s[2]  # (m_c/m_t, m_u/m_t)

def chi2(log_params, tau=TAU_LYD20):
    beta_over_alpha  = np.exp(log_params[0])
    gamma_over_alpha = np.exp(log_params[1])
    mc_mt, mu_mt = get_mass_ratios(tau, beta_over_alpha, gamma_over_alpha)

    r1 = (np.log(mc_mt) - np.log(LYD20_MC_MT))**2 / (0.05)**2
    r2 = (np.log(mu_mt) - np.log(LYD20_MU_MT))**2 / (0.05)**2
    return r1 + r2

print("Scanning (log β/α, log γ/α) space to find LYD20 best-fit masses:")
print(f"Target: m_c/m_t = {LYD20_MC_MT:.5e}, m_u/m_t = {LYD20_MU_MT:.5e}")
print()

# Scan a grid
best_chi2 = np.inf
best_params = None
best_ratios = None

for log_b in np.linspace(-6, 6, 25):
    for log_g in np.linspace(-6, 6, 25):
        c2 = chi2([log_b, log_g])
        if c2 < best_chi2:
            best_chi2 = c2
            best_params = (np.exp(log_b), np.exp(log_g))
            best_ratios = get_mass_ratios(TAU_LYD20, best_params[0], best_params[1])

print(f"Grid best: β/α = {best_params[0]:.4f}, γ/α = {best_params[1]:.4f}")
print(f"  m_c/m_t = {best_ratios[0]:.5e}, m_u/m_t = {best_ratios[1]:.5e}")

# Refine with optimizer
from scipy.optimize import differential_evolution
bounds = [(-6, 6), (-6, 6)]
result = differential_evolution(chi2, bounds, maxiter=2000, tol=1e-12, seed=0,
                                 workers=1, mutation=(0.5, 1.5), popsize=20, disp=False)
print(f"\nDE result: chi2 = {result.fun:.6e}")

result2 = minimize(chi2, result.x, method='Nelder-Mead',
                   options={'xatol': 1e-12, 'fatol': 1e-12, 'maxiter': 50000})
print(f"NM refined: chi2 = {result2.fun:.6e}")

beta_opt  = np.exp(result2.x[0])
gamma_opt = np.exp(result2.x[1])
mc_mt_opt, mu_mt_opt = get_mass_ratios(TAU_LYD20, beta_opt, gamma_opt)

print(f"\nOptimal parameters at LYD20 τ:")
print(f"  β/α = {beta_opt:.8f}")
print(f"  γ/α = {gamma_opt:.8e}")
print(f"  m_c/m_t = {mc_mt_opt:.6e}  (target: {LYD20_MC_MT:.6e})")
print(f"  m_u/m_t = {mu_mt_opt:.6e}  (target: {LYD20_MU_MT:.6e})")
print(f"  m_u/m_c = {mu_mt_opt/mc_mt_opt:.6e}  (target: {LYD20_MU_MC:.6e})")

# Now check: which row IS the heavy one?
Mu_opt = M_u(TAU_LYD20, 1.0, beta_opt, gamma_opt)
_, s_opt, _ = svd(Mu_opt)
s_opt = np.sort(s_opt)
print(f"\nSingular values (sorted): {s_opt}")

# Row magnitudes
print(f"\nRow norms:")
for i, label in enumerate(['u^c (α, Y^1)', 'c^c (β, Y^2)', 't^c (γ, Y^5)']):
    print(f"  Row {i} ({label}): |row| = {np.linalg.norm(Mu_opt[i,:]):.4f}")

# Compare with LYD20 claim: β/α = 62.2142, γ/α = 0.00104
print(f"\nLYD20 claim: β/α = 62.2142, γ/α = 0.00104")
print(f"Our fit:     β/α = {beta_opt:.4f}, γ/α = {gamma_opt:.8f}")
print()

# What if the forms are NOT normalized as we think?
# Let me check: maybe LYD20 uses a different normalization of Y^(k)
# such that |Y^(5)_{3̂}| ~ O(1) at their best-fit τ.
# Their Y^(5) = (18 Y1^2 (Y3^3 - Y2^3), ...)
# At |Y1|~0.87, this gives |Y5_3| = 18 * 0.87^2 * |Y3^3 - Y2^3| ~ 18*0.76*(...)
# Let's compute the actual LYD20-normalized values

from mass_matrix import modular_forms_weight1, modular_forms_all
Y1, Y2, Y3 = modular_forms_weight1(TAU_LYD20)
f = modular_forms_all(Y1, Y2, Y3)
print(f"Form magnitudes at LYD20 τ:")
print(f"  |Y1|~{abs(Y1):.4f}, |Y2|~{abs(Y2):.4f}, |Y3|~{abs(Y3):.4f}")
print(f"  Row0 entries: {[abs(f['Y1_1']), abs(f['Y1_3']), abs(f['Y1_2'])]}")
print(f"  Row1 entries: {[abs(f['Y2_3']), abs(f['Y2_5']), abs(f['Y2_4'])]}")
print(f"  Row2 entries: {[abs(f['Y5_3']), abs(f['Y5_5']), abs(f['Y5_4'])]}")
print(f"  (Y5 are polynomials in Y1,Y2,Y3 — they're larger by ~O(Y^4) factor)")
print(f"  Row2/Row0 form ratio: {abs(f['Y5_3'])/abs(f['Y1_1']):.1f}x")
print(f"  So γ_u must be ~100x smaller than α_u to compensate")
print(f"  Fitted γ/α = {gamma_opt:.4e} vs 100x = 0.01")
print(f"  LYD20 claim γ/α = 0.00104 → this is ~385x suppression (|Y5|/|Y1|)")
print()

# KEY INSIGHT: if LYD20's γ/α = 0.00104 and |Y5_3/Y1_1| ≈ 370
# then γ*|Y5| / α*|Y1| ≈ 0.00104 * 370 ≈ 0.38
# And β/α = 62.2142, |Y2_3/Y1_1| ≈ 2.6
# Then β*|Y2| / α*|Y1| ≈ 62.2 * 2.6 ≈ 162
# So c^c (row1) still dominates → c^c is heaviest, t^c second, u^c lightest??
# That contradicts quark physics. Something is fundamentally wrong with M_u.

print("CONCLUSION: With standard labeling, c^c is the heaviest quark.")
print("Either: (a) the row labeling in LYD20 is different from what we have,")
print("        (b) the coupling ratios are inverted (α_u is the t coupling),")
print("        (c) our weight-5 forms Y^(5)_3, etc. are wrong by a large factor.")
print()
print(f"Our fit gives β/α = {beta_opt:.4f}, γ/α = {gamma_opt:.4e}")
print(f"This is very different from LYD20 claim of 62.2142 and 0.00104")
