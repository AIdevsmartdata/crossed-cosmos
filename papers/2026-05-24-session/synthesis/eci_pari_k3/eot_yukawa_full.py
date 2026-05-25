"""
H3 RIGOROUS test using EOT 2010 (arXiv:1004.0956) data with proper coefficients.

EOT 2010 decomposition of K3 elliptic genus:
  chi_{K3}(tau, z) = 24 * mu(tau,z) + 2 sum_n A_n * theta_n(tau, z)

where A_n = number of times mu_n appears.
EOT observed: A_n for n=1,2,3,... are 90, 462, 1540, 4554, 11592, 27830, 61686, 131100, ...
(or equivalently divided by 2: 45, 231, 770, 2277, 5796, 13915, 30843, 65550, ...)

These A_n / 2 are non-negative integer combinations of M_24 IRREP DIMENSIONS:
  45 = 45 (single irrep)
  231 = 231 (single irrep)
  770 = 770 (single irrep)
  2277 = 2277 (single irrep)
  5796 = 5796 (single irrep)
  13915 = 1 + 23 + 252 + 990 + 1771 + 2024 + 2277 + 5796? Let me check:
        actually 13915 = 1771 + 990 + 252 + 5544 + 5358? Not directly identifiable
  30843 = ...

The Mathieu Moonshine "miracle" is that ALL these A_n are non-negative integer
combinations of dim of M_24 irreps.

For H3 ECI test:
  IF Yukawa fermions ~ 1/dim(M_24 irrep), then the 9 fermions
  should pick 9 specific irreps (with appropriate scale factor).
"""

import numpy as np
from itertools import combinations, permutations

# Standard PDG masses (running MS-bar)
masses_GeV = {
    'e':  0.000510999,
    'mu': 0.105658,
    'tau': 1.77686,
    'u':  0.00216,
    'd':  0.00467,
    's':  0.0935,
    'c':  1.273,
    'b':  4.183,
    't':  172.57,
}
v_higgs = 246.22
y = {f: float(np.sqrt(2) * m / v_higgs) for f, m in masses_GeV.items()}

# M_24 irrep dimensions
M24_unique = [1, 23, 45, 231, 252, 253, 483, 770, 990, 1035, 1265, 1771, 2024, 2277, 3312, 3520, 5313, 5544, 5796, 10395]

print("="*70)
print("H3 RIGOROUS TEST: 9 fermions vs 9 M_24 irrep dims")
print("="*70)
print()

# Best assignment: minimize sum of squared log-errors
# m_f = m_t * (d_t / d_f)^alpha
# Free parameters: alpha, {d_f}_{f != t}

# Try all 9-tuples of dimensions (with d_t fixed = ?)
# Actually let's not fix d_t. Try all assignments of 9 dims to 9 fermions.

# Compute log-ratios
log_m = {f: np.log(masses_GeV[f]) for f in masses_GeV}
log_m_ref = log_m['t']  # use top as reference

# For each candidate assignment, fit alpha to minimize sum of squared log errors
# alpha = - cov(log_m, log_d) / var(log_d)

from itertools import combinations
fermions = list(masses_GeV.keys())
log_m_arr = np.array([log_m[f] for f in fermions])

best_assignment = None
best_score = float('inf')

# Try all C(20, 9) = 167960 combinations of 9 dims
# For each, find best permutation: assign smallest dim to lightest fermion? No, vice versa
# Optimal: sort dims and sort fermions by mass, assign in correlated order
# Then fit alpha for best fit
fermions_by_mass = sorted(fermions, key=lambda f: -masses_GeV[f])  # heaviest first
log_m_sorted = np.array([log_m[f] for f in fermions_by_mass])

print("Fermions by mass (heaviest first):", fermions_by_mass)
print("log m_f:", log_m_sorted)
print()

# For each combination of 9 dims, sorted by dim, assign to fermions sorted by mass
# (heaviest fermion -> smallest dim, since y_f ~ 1/d_f)

n_tested = 0
for comb in combinations(M24_unique, 9):
    n_tested += 1
    dims_sorted = sorted(comb)  # smallest to largest
    log_d_arr = np.log(np.array(dims_sorted))
    # Heaviest fermion gets smallest dim
    # log_m_sorted is already heaviest-first
    # so log_m_sorted[0] (top) <-> log_d_arr[0] (smallest dim)
    # Linear fit: log m = a * log d + b
    # Then alpha = -a (since y ~ 1/d^alpha means m ~ 1/d^alpha => log m = -alpha log d + const)
    coeffs = np.polyfit(log_d_arr, log_m_sorted, 1)
    a, b = coeffs[0], coeffs[1]
    # Residuals
    pred = a * log_d_arr + b
    resid = log_m_sorted - pred
    score = np.sum(resid**2)
    if score < best_score:
        best_score = score
        best_assignment = (dims_sorted, a, b, resid)

print(f"Tested {n_tested} combinations of 9 dims out of {len(M24_unique)} M_24 irreps")
print()
print("BEST ASSIGNMENT:")
dims_b, a_b, b_b, resid_b = best_assignment
print(f"  Slope (alpha) = {-a_b:.4f}")
print(f"  Intercept = {b_b:.4f}")
print(f"  Sum sq log residuals: {best_score:.6f}")
print(f"  Max |residual|: {max(abs(resid_b)):.4f}")
print(f"  Mean |residual|: {np.mean(abs(resid_b)):.4f}")
print()
print(f"{'fermion':<8} {'m_obs':<14} {'d (best)':<10} {'m_pred':<14} {'rel err':<10}")
for i, f in enumerate(fermions_by_mass):
    d = dims_b[i]
    m_pred = np.exp(a_b * np.log(d) + b_b)
    rel = abs(m_pred - masses_GeV[f]) / masses_GeV[f]
    print(f"{f:<8} {masses_GeV[f]:<14.6f} {d:<10} {m_pred:<14.6e} {rel*100:.2f}%")
print()

# Adversarial null: random dim list with same size
print("="*70)
print("Adversarial null: random dim list (size 9, same range)")
print("="*70)
np.random.seed(42)
null_scores = []
n_trials = 2000
log_m_sorted_arr = log_m_sorted
for trial in range(n_trials):
    rand_dims = sorted(np.random.choice(range(2, 11000), 9, replace=False))
    log_d = np.log(np.array(rand_dims))
    coeffs = np.polyfit(log_d, log_m_sorted_arr, 1)
    pred = coeffs[0] * log_d + coeffs[1]
    score = np.sum((log_m_sorted_arr - pred)**2)
    null_scores.append(score)

null_scores = np.array(null_scores)
print(f"Null distribution: mean={null_scores.mean():.4f}, std={null_scores.std():.4f}")
print(f"  Min: {null_scores.min():.4f}")
print(f"  Real best (M_24 dims): {best_score:.4f}")
print(f"  Fraction of null trials with score <= real: {np.mean(null_scores <= best_score)*100:.2f}%")
print()

# Now test: what if we restrict to McKay-Mathieu coefficients ONLY (low n)
print("="*70)
print("RESTRICTED: only McKay-Mathieu coefficients (first 9 levels)")
print("="*70)
mckay_dims = [1, 23, 45, 231, 770, 2277, 5796, 10395, 13915]
print(f"McKay candidates: {mckay_dims}")
log_d_mckay = np.log(np.array(mckay_dims))
coeffs = np.polyfit(log_d_mckay, log_m_sorted_arr, 1)
print(f"  Alpha (slope): {-coeffs[0]:.4f}")
print(f"  Intercept: {coeffs[1]:.4f}")
pred = coeffs[0] * log_d_mckay + coeffs[1]
resid = log_m_sorted_arr - pred
print(f"  Sum sq residuals: {np.sum(resid**2):.4f}")
print(f"  Max |residual|: {max(abs(resid)):.4f}")
print()
print(f"{'fermion':<8} {'m_obs':<14} {'d McKay':<10} {'m_pred':<14} {'rel err':<10}")
for i, f in enumerate(fermions_by_mass):
    d = mckay_dims[i]
    m_pred = np.exp(coeffs[0] * np.log(d) + coeffs[1])
    rel = abs(m_pred - masses_GeV[f]) / masses_GeV[f]
    print(f"{f:<8} {masses_GeV[f]:<14.6f} {d:<10} {m_pred:<14.6e} {rel*100:.2f}%")
print()
print()

# What is alpha for the best case?
print("="*70)
print("CRITICAL: what physical meaning does best-fit alpha have?")
print("="*70)
print(f"Best alpha (M_24 free choice): {-best_assignment[1]:.4f}")
print(f"Hypothesis: alpha = 2 (Yukawa from instanton action scaling) ?")
print(f"           alpha = 1 (Yukawa from rep dim direct) ?")
print(f"           alpha = 1/2 (BPS spectrum overlap) ?")
print()
print("The MEAN slope of log(m_f) vs log(d_f) for masses (rounded log scale):")
print(f"  log(m_t) = {np.log(masses_GeV['t']):.3f}")
print(f"  log(m_e) = {np.log(masses_GeV['e']):.3f}")
print(f"  log slope per decade of mass: depends on dim choice")
