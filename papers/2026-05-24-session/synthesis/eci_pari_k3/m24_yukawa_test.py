"""
H3 test: Yukawa fermions = 1/dim(reps) of M_24 (Mathieu Moonshine).

References to verify:
- Eguchi-Ooguri-Tachikawa 2010 arXiv:1004.0956 (NOT yet verified, TODO WebFetch)
- M_24 has 26 conjugacy classes and 26 irreducible representations.

Dimensions of irreducible reps of M_24 (from ATLAS of finite groups):
1, 23, 45, 45, 231, 231, 252, 253, 483, 770, 770, 990, 990, 1035, 1035, 1035,
1265, 1771, 2024, 2277, 3312, 3520, 5313, 5544, 5796, 10395

Total: 26 reps.
Sum of squares = |M_24| = 244823040 = 2^10 * 3^3 * 5 * 7 * 11 * 23

Yukawa fermions (PDG 2024, m_f * sqrt(2) / v with v = 246.22 GeV):
"""

import sympy as sp
from mpmath import mp, mpf
import numpy as np
from itertools import combinations

mp.dps = 30

# Standard PDG masses in GeV (running MS-bar at appropriate scale)
masses_GeV = {
    'e':  0.000510999,
    'mu': 0.105658,
    'tau': 1.77686,
    'u':  0.00216,   # MS-bar at 2 GeV
    'd':  0.00467,   # MS-bar at 2 GeV
    's':  0.0935,    # MS-bar at 2 GeV
    'c':  1.273,     # MS-bar at MC
    'b':  4.183,     # MS-bar at Mb
    't':  172.57,    # PDG 2024 pole
}

v_higgs = 246.22  # GeV

# Yukawa = sqrt(2) * m / v
yukawas = {f: float(mpf(2).sqrt() * m / v_higgs) for f, m in masses_GeV.items()}

print("== H3 Test: Yukawa fermions vs 1/dim(reps M_24) ==\n")
print("Yukawa couplings (y_f = sqrt(2) * m_f / v):")
for f, y in sorted(yukawas.items(), key=lambda kv: kv[1]):
    print(f"  y_{f:3s} = {y:.4e}  =>  1/y = {1/y:.4f}")
print()

# M_24 irrep dimensions (ATLAS, verified standard)
M24_dims = [
    1, 23, 45, 45, 231, 231, 252, 253, 483, 770, 770,
    990, 990, 1035, 1035, 1035, 1265, 1771, 2024, 2277,
    3312, 3520, 5313, 5544, 5796, 10395
]
print(f"M_24 has {len(M24_dims)} irreducible representations.")
print(f"Sum of squares = {sum(d**2 for d in M24_dims)}  (should = |M_24| = 244823040)")
print(f"Match |M_24|: {sum(d**2 for d in M24_dims) == 244823040}\n")

# Distinct dimensions for matching
unique_dims = sorted(set(M24_dims))
print(f"Distinct dimensions: {unique_dims}\n")

print("== Test 1: y_f vs 1/d for each d in M_24 dims ==\n")
print(f"{'fermion':<8} {'y_f':<14} {'1/y_f':<14} {'closest d in M24':<20} {'1/d':<14} {'rel err':<10}")
for f, y in sorted(yukawas.items(), key=lambda kv: kv[1]):
    target = 1 / y
    best_d = min(unique_dims, key=lambda d: abs(d - target) / target)
    err = abs(best_d - target) / target
    print(f"{f:<8} {y:.4e}    {target:<14.4f} {best_d:<20} {1/best_d:.4e}    {err*100:.2f}%")
print()

# Also test inverse logic: which 1/d matches y_f?
print("== Test 2: Best Matchings - closest 1/d for each y_f ==\n")
print(f"{'fermion':<8} {'y_f':<14} {'best 1/d':<14} {'d':<8} {'err':<10}")
for f, y in sorted(yukawas.items(), key=lambda kv: kv[1]):
    best_d = min(unique_dims, key=lambda d: abs(1/d - y) / y if y > 0 else float('inf'))
    err = abs(1/best_d - y) / y
    print(f"{f:<8} {y:.4e}    {1/best_d:.4e}   {best_d:<8} {err*100:.3f}%")
print()

# Test 3: Yukawa RATIOS vs ratios of dim
print("== Test 3: Yukawa Ratios vs Dim Ratios ==\n")
print("If y_f / y_{f'} = d_{f'} / d_f exact, look for the dim pair matching observed ratio.")
print()
fermions = sorted(yukawas.items(), key=lambda kv: kv[1])
for (f1, y1), (f2, y2) in combinations(fermions, 2):
    ratio = y2 / y1  # y2 > y1
    # Look for d1 / d2 = ratio (d1 > d2)
    best = (None, None, float('inf'))
    for d1 in unique_dims:
        for d2 in unique_dims:
            if d2 == 0: continue
            test_ratio = d1 / d2
            rel = abs(test_ratio - ratio) / ratio
            if rel < best[2]:
                best = (d1, d2, rel)
    if best[2] < 0.02:  # less than 2%
        print(f"  y_{f2}/y_{f1} = {ratio:.4e} ≈ {best[0]}/{best[1]} = {best[0]/best[1]:.4e}  ({best[2]*100:.2f}%)")
print()

# Test 4: y_top special, dim_max = 10395
print(f"== Test 4: Top Yukawa anchor ==")
print(f"y_top = {yukawas['t']:.4f}")
print(f"1/y_top = {1/yukawas['t']:.4f}")
print(f"sqrt(2)/v = {float(mpf(2).sqrt() / v_higgs):.4e}")
print()

# Adversarial null: how many spurious matches if I picked RANDOM integers ?
import random
random.seed(42)
print("== Test 5: Adversarial null (random dim list with same size) ==\n")
n_trials = 50
match_count_real = 0
for f, y in yukawas.items():
    target = 1/y
    best_d = min(unique_dims, key=lambda d: abs(d - target)/target)
    if abs(best_d - target)/target < 0.05:
        match_count_real += 1

print(f"Real M_24 dims, matches with <5% err: {match_count_real} / {len(yukawas)}")

null_match_counts = []
for trial in range(n_trials):
    random_dims = sorted(set(random.randint(1, 11000) for _ in range(len(unique_dims))))
    count = 0
    for f, y in yukawas.items():
        target = 1/y
        best_d = min(random_dims, key=lambda d: abs(d - target)/target if target > 0 else float('inf'))
        if abs(best_d - target)/target < 0.05:
            count += 1
    null_match_counts.append(count)

null_match_counts = np.array(null_match_counts)
print(f"Null distribution (random dims sized like M_24): mean={null_match_counts.mean():.1f}, std={null_match_counts.std():.1f}")
print(f"Z-score of real: {(match_count_real - null_match_counts.mean())/null_match_counts.std():.2f}")
