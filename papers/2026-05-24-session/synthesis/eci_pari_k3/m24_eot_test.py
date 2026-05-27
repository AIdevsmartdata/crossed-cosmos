"""
Refined H3 test using EOT 2010 (arXiv:1004.0956 VERIFIED) Mathieu moonshine.

EOT decomposition:
The elliptic genus of K3 is:
  EG_K3(tau, z) = 2*phi_{0,1}(tau, z) = sum of N=4 superconformal characters

The "massive" part decomposes as:
  H(tau) = sum_n a_n q^{n - 1/8}, q = exp(2pi i tau)

where the McKay-Mathieu observation is:
  H(tau) = 2 q^{-1/8} [-1 + sum_n A_n q^n]

with A_1 = 45 (dim of 45 irrep of M_24)
     A_2 = 231 = 1 + 23 + 23 + 45 + 45 + 94? -- actually 231 IS an irrep dim
     A_3 = 770 (irrep dim)
     A_4 = 2277 (irrep dim)
     A_5 = 5796 (irrep dim) -- but 5796 = irrep too
     A_6 = 13915 -- NOT an irrep dim of M_24 (so decomposes)
     A_7 = 30843 = ... (decomposes)

Refined hypothesis H3:
  Yukawa fermions y_f relate to LOW-LYING McKay-Mathieu coefficients A_n
  via y_f = c_f / A_n for some constant c_f.

Actually, ALTERNATIVE: dim of M_24 irrep = N_f where m_f = m_t / sqrt(N_f)
  (geometric mean style)

Let me test multiple formulations.
"""

import numpy as np
import sympy as sp
from mpmath import mp, mpf
mp.dps = 30

# Standard PDG masses (GeV)
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
v_higgs = 246.22  # GeV

# Yukawa values
y = {f: float(np.sqrt(2) * m / v_higgs) for f, m in masses_GeV.items()}

# McKay-Mathieu sequence (coefficients of H massive part in K3 EG):
# Following EOT 2010 Table 1
# A_n = "dimensions" of the n-th level
mckay_A = {
    1: 45,
    2: 231,
    3: 770,
    4: 2277,
    5: 5796,
    6: 13915,    # = 1 + 23 + 1265 + 990 + 5544 + 5796 + ... not single irrep
    7: 30843,
    8: 65550,
    9: 132825,
    10: 261800,
}

# All M_24 irreps (ATLAS standard)
M24_irreps = {
    'chi_1': 1, 'chi_23a': 23, 'chi_45a': 45, 'chi_45b': 45,
    'chi_231a': 231, 'chi_231b': 231, 'chi_252': 252, 'chi_253': 253,
    'chi_483': 483, 'chi_770a': 770, 'chi_770b': 770,
    'chi_990a': 990, 'chi_990b': 990,
    'chi_1035a': 1035, 'chi_1035b': 1035, 'chi_1035c': 1035,
    'chi_1265': 1265, 'chi_1771': 1771, 'chi_2024': 2024, 'chi_2277': 2277,
    'chi_3312': 3312, 'chi_3520': 3520, 'chi_5313': 5313,
    'chi_5544': 5544, 'chi_5796': 5796, 'chi_10395': 10395,
}
unique_dims = sorted(set(M24_irreps.values()))
print(f"Distinct M_24 irrep dimensions ({len(unique_dims)}):", unique_dims)
print(f"Number of irreducible reps: {len(M24_irreps)}")
print(f"Sum of squares = {sum(d**2 for d in M24_irreps.values())}, |M_24| = 244823040")
print()

# Test A: y_f = sqrt(2)/v * m_f, m_f = M / N^a for some N in dim set, some a
print("="*70)
print("TEST A: y_f vs 1/d^alpha for d in M_24 dim set, alpha integer")
print("="*70)
print()
print(f"Reference: y_top = {y['t']:.4f}, y_e = {y['e']:.4e}")
print(f"Ratio y_t/y_e = {y['t']/y['e']:.4e}")
print()
# If y_t = 1/d_t^a and y_e = 1/d_e^b, find a, b, d_t, d_e
# y_t/y_e ~ 3.4e5

# Find d^N close to y_t/y_e
target_top_e = y['t'] / y['e']
print(f"target y_t/y_e ratio: {target_top_e:.4e}")
print(f"Possible (d, n) with d^n ~ {target_top_e:.4e}:")
for d in unique_dims:
    if d <= 1: continue
    n = np.log(target_top_e) / np.log(d)
    if abs(n - round(n)) < 0.05:
        print(f"  d={d}, n={n:.3f} (close to integer {round(n)})")

print()
print("="*70)
print("TEST B: Yukawa = c / dim, find best 'c' that minimizes total error")
print("="*70)
# Optimal c such that y_f = c / d_f for assignment d_f -> y_f
# This is equivalent to: 1/y_f = d_f / c, so d_f / (c * y_f) should be ~1 if assignment correct
# Try c = 1 first (already done above) then test various scalings

# A more elegant formulation: y_f = sqrt(2) m_f / v
# If m_f = (v/sqrt(2)) * (d_min / d_f), then y_f = d_min/d_f
# So with d_min = d of top (d=1 ideally), y_t = 1/d_t  =>  y_t = 1, m_t = v/sqrt(2) = 174.1 GeV
# Observed m_t = 172.57, ratio = 0.991. Off by 0.9% (assigning d_t = 1 + 1/v correction)
# Then m_f = m_t / d_f for d_f > 1.
print("Hypothesis B: m_f = m_t / d_f for some d_f in M_24 dim set")
print(f"  m_t = {masses_GeV['t']} GeV (assigned d_t = 1)")
print()
print(f"{'fermion':<8} {'m_f (GeV)':<14} {'m_t/m_f':<14} {'closest d':<10} {'rel err':<10}")
for f in sorted(masses_GeV.keys(), key=lambda x: -masses_GeV[x]):
    if f == 't': continue
    mf = masses_GeV[f]
    target_d = masses_GeV['t'] / mf
    best_d = min(unique_dims, key=lambda d: abs(d - target_d)/target_d)
    err = abs(best_d - target_d)/target_d
    print(f"{f:<8} {mf:<14.6f} {target_d:<14.2f} {best_d:<10} {err*100:.2f}%")
print()

# Better: use 1, 23, 45, 252, 253, 483, etc. and find OPTIMAL assignment
print("="*70)
print("TEST C: Best assignment of M_24 dims to fermions minimizing max error")
print("="*70)
# We have 9 fermions to assign 9 dims to. Test greedy: for each fermion,
# find closest unused dim such that m_t/d = m_f
fermions_sorted = sorted(masses_GeV.keys(), key=lambda x: -masses_GeV[x])
assignment = {}
used = set()
errors = {}
for f in fermions_sorted:
    if f == 't':
        assignment['t'] = 1
        used.add(1)
        errors['t'] = 0.0
        continue
    target_d = masses_GeV['t'] / masses_GeV[f]
    # find closest unused
    available = [d for d in unique_dims if d not in used]
    best_d = min(available, key=lambda d: abs(d - target_d)/target_d)
    assignment[f] = best_d
    used.add(best_d)
    errors[f] = abs(best_d - target_d)/target_d

print(f"{'fermion':<8} {'m_obs':<14} {'d':<8} {'m_pred = m_t/d':<14} {'rel err':<10}")
for f in fermions_sorted:
    d = assignment[f]
    m_pred = masses_GeV['t'] / d
    print(f"{f:<8} {masses_GeV[f]:<14.6f} {d:<8} {m_pred:<14.6f} {errors[f]*100:.2f}%")

print()
print(f"Max error: {max(errors.values())*100:.2f}%")
print(f"Mean error: {np.mean(list(errors.values()))*100:.2f}%")
print()

# Test C2: m_f = m_t / d_f^alpha for varying alpha
print("="*70)
print("TEST D: m_f = m_t / d_f^alpha (fit alpha)")
print("="*70)
# y_f ratios should match d^alpha ratios

# Same logic: log(m_t/m_f) = alpha * log(d_f)
# Take 'best alpha' over assignments
for alpha in [0.5, 1.0, 1.5, 2.0]:
    print(f"\n  alpha = {alpha}:")
    used = set()
    errs = []
    for f in fermions_sorted:
        if f == 't': continue
        target = (masses_GeV['t'] / masses_GeV[f]) ** (1/alpha)
        avail = [d for d in unique_dims if d not in used and d > 1]
        if not avail: break
        best_d = min(avail, key=lambda d: abs(d - target)/target if target > 0 else float('inf'))
        used.add(best_d)
        m_pred = masses_GeV['t'] / (best_d ** alpha)
        err = abs(m_pred - masses_GeV[f]) / masses_GeV[f]
        errs.append(err)
        print(f"    {f}: target d={target:.2f}, best d={best_d}, m_pred={m_pred:.4e}, err={err*100:.1f}%")
    if errs:
        print(f"    Max err: {max(errs)*100:.1f}%, Mean err: {np.mean(errs)*100:.1f}%")
print()

# === McKay-Mathieu CONNECTION ===
print("="*70)
print("TEST E: Using only McKay-Mathieu coefficients (low-lying A_n)")
print("="*70)
# A_n are: 45, 231, 770, 2277, 5796, 13915, 30843, ...
mckay_seq = [45, 231, 770, 2277, 5796, 13915, 30843, 65550, 132825, 261800]
print(f"McKay-Mathieu sequence (EOT 2010): {mckay_seq[:6]}...")
print()
for f in fermions_sorted:
    if f == 't': continue
    target_d = masses_GeV['t'] / masses_GeV[f]
    best_d = min(mckay_seq, key=lambda d: abs(d - target_d)/target_d)
    err = abs(best_d - target_d)/target_d
    print(f"  {f}: target d={target_d:.2f}, best McKay d={best_d}, err={err*100:.1f}%")

print()

# === SANITY: Compare with Koide and y_top G_2 ===
print("="*70)
print("Sanity check against known TIER 1 results:")
print("="*70)
# y_top^2 = 48/49 expected from G_2
y_top_pred_G2 = np.sqrt(48/49)
print(f"y_top (obs) = {y['t']:.5f}")
print(f"y_top (G_2 pred) = sqrt(48/49) = {y_top_pred_G2:.5f}")
print(f"Error: {abs(y['t'] - y_top_pred_G2)/y['t']*100:.3f}%")
print()
print(f"For Koide: m_e + m_mu + m_tau = {masses_GeV['e'] + masses_GeV['mu'] + masses_GeV['tau']:.5f}")
print(f"K = (sum sqrt(m))^2 / (3*sum m) = ?")
sum_sqrt_m = sum(np.sqrt(masses_GeV[f]) for f in ['e','mu','tau'])
sum_m = sum(masses_GeV[f] for f in ['e','mu','tau'])
K = sum_sqrt_m**2 / (3*sum_m)
print(f"K = {K:.6f}, 2/3 = {2/3:.6f}, |K - 2/3| = {abs(K - 2/3):.6f}")
