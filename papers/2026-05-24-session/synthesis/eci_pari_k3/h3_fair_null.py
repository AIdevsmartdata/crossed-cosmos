"""
FAIR null test for H3.

The previous null used 9 random dims out of (2, 11000) — that's TOO restrictive.
The fair null should:
1. Generate 20 random "fake M_24 dims" with same statistics (range, distribution)
2. Select the BEST 9-subset from those 20 (167960 choices, same combinatorics as real)
3. Compare best-fit score to real M_24 best 9-subset score
"""

import numpy as np
from itertools import combinations

masses_GeV = {
    'e':  0.000510999, 'mu': 0.105658, 'tau': 1.77686,
    'u':  0.00216, 'd':  0.00467, 's':  0.0935,
    'c':  1.273, 'b':  4.183, 't':  172.57,
}
fermions_by_mass = sorted(masses_GeV.keys(), key=lambda f: -masses_GeV[f])
log_m_sorted = np.array([np.log(masses_GeV[f]) for f in fermions_by_mass])

# Real M_24 dims
M24_unique = [1, 23, 45, 231, 252, 253, 483, 770, 990, 1035, 1265, 1771, 2024, 2277, 3312, 3520, 5313, 5544, 5796, 10395]

def best_fit_score(dim_pool):
    """Best fit log(m_f) = a*log(d) + b over all 9-subsets of dim_pool."""
    if len(dim_pool) < 9: return float('inf')
    best = float('inf')
    for comb in combinations(dim_pool, 9):
        dims_sorted = sorted(comb)
        log_d = np.log(np.array(dims_sorted, dtype=float))
        coeffs = np.polyfit(log_d, log_m_sorted, 1)
        pred = coeffs[0] * log_d + coeffs[1]
        score = np.sum((log_m_sorted - pred)**2)
        if score < best:
            best = score
    return best

# Real M_24
real_score = best_fit_score(M24_unique)
print(f"REAL M_24 (20 dims, best 9-subset): score = {real_score:.4f}")
print()

print("="*70)
print("FAIR Null A: 20 uniformly random integers in [1, 11000]")
print("="*70)
np.random.seed(42)
null_A_scores = []
for trial in range(100):
    fake_pool = sorted(set(np.random.choice(range(1, 11000), 20, replace=False).astype(int)))
    if len(fake_pool) < 9: continue
    score = best_fit_score(fake_pool)
    null_A_scores.append(score)
    if trial < 5:
        print(f"  Trial {trial}: score = {score:.4f}")

null_A_scores = np.array(null_A_scores)
print(f"  Null A (100 trials): mean={null_A_scores.mean():.4f}, std={null_A_scores.std():.4f}, min={null_A_scores.min():.4f}")
print(f"  Real <= null: {np.mean(null_A_scores <= real_score)*100:.1f}%")
print()

print("="*70)
print("FAIR Null B: 20 log-uniform random integers in [1, 11000]")
print("(matching M_24 logarithmic density)")
print("="*70)
np.random.seed(42)
null_B_scores = []
for trial in range(100):
    log_min = 0
    log_max = np.log(11000)
    fake_pool_floats = np.exp(np.random.uniform(log_min, log_max, 25))
    fake_pool = sorted(set(np.round(fake_pool_floats).astype(int)))
    fake_pool = [d for d in fake_pool if d >= 1][:20]
    if len(fake_pool) < 9: continue
    score = best_fit_score(fake_pool)
    null_B_scores.append(score)

null_B_scores = np.array(null_B_scores)
print(f"  Null B (100 trials): mean={null_B_scores.mean():.4f}, std={null_B_scores.std():.4f}, min={null_B_scores.min():.4f}")
print(f"  Real <= null: {np.mean(null_B_scores <= real_score)*100:.1f}%")
print()

print("="*70)
print("FAIR Null C: 20 dims matching M_24 statistical distribution")
print("(log-spaced from min to max of real M_24)")
print("="*70)
np.random.seed(42)
log_min = np.log(min(M24_unique))
log_max = np.log(max(M24_unique))
null_C_scores = []
for trial in range(100):
    fake_pool_floats = np.exp(np.random.uniform(log_min, log_max, 25))
    fake_pool = sorted(set(np.round(fake_pool_floats).astype(int)))
    fake_pool = [d for d in fake_pool if d >= 1][:20]
    if len(fake_pool) < 9: continue
    score = best_fit_score(fake_pool)
    null_C_scores.append(score)

null_C_scores = np.array(null_C_scores)
print(f"  Null C (100 trials): mean={null_C_scores.mean():.4f}, std={null_C_scores.std():.4f}, min={null_C_scores.min():.4f}")
print(f"  Real <= null: {np.mean(null_C_scores <= real_score)*100:.1f}%")
print()

# Interpret: if real M_24 score is comparable to nulls B/C (log-spaced random),
# then there's NOTHING SPECIAL about M_24 dims for fitting Yukawa.
# It's just a log-spaced collection that we can fit any 9-tuple of log-spaced reals to.

print("="*70)
print("VERDICT INTERPRETATION:")
print("="*70)
print(f"Real M_24 best score: {real_score:.4f}")
print(f"  vs uniform random pool: {null_A_scores.mean():.4f} (Real is MUCH better, but pool not log-spaced)")
print(f"  vs log-uniform pool: {null_B_scores.mean():.4f} (FAIR comparison)")
print(f"  vs log-uniform within M_24 range: {null_C_scores.mean():.4f}")
print()
print("If null_B,C means are COMPARABLE to real, then M_24 has NO special structure")
print("for Yukawa fit -- it's just providing 'a list of log-spaced numbers'.")
print()
print("Statistical conclusion:")
if real_score < null_C_scores.mean() * 0.5:
    print("M_24 STRONGLY out-performs random log-spaced (real factor 2+ better)")
elif real_score < null_C_scores.mean():
    print("M_24 marginally outperforms (real better than mean)")
else:
    print("M_24 NOT significantly better than random log-spaced -- LIKELY COINCIDENCE")
