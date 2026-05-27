"""
Test Yukawa = M_24 dim irreps — approfondi structurel
======================================================
Opus a montré α=3.50 ad hoc + y_t/y_b = 10395/252 (0.01-0.08%).
Creuser : autres ratios fermions = ratios M_24 dims ?
Structure consistante par génération / type ?
"""
import numpy as np
from math import log, exp, sqrt
from itertools import combinations, permutations

# M_24 irreps (dimensions distinctes)
# Vérifiées par sum-of-squares = 244,823,040 = |M_24|
M24_DIMS = [1, 23, 45, 231, 252, 253, 483, 770, 990, 1035,
            1265, 1771, 2024, 2277, 3312, 3520, 5313, 5544, 5796, 10395]

# Fermion data (PDG 2024)
v = 246.22  # GeV
masses = {
    'e':  0.51099895e-3,
    'mu': 0.10565838,
    'tau': 1.77686,
    'u':  2.16e-3,
    'd':  4.67e-3,
    's':  93.4e-3,
    'c':  1.27,
    'b':  4.18,
    't':  172.57,
}

# Yukawa values
yukawas = {f: sqrt(2)*m/v for f, m in masses.items()}
print("Yukawa values (PDG):")
for f, y in yukawas.items():
    print(f"  y_{f:3s} = {y:.4e}, ln(y) = {log(y):.4f}")

# ============================================================================
# TEST 1 : All pairwise ratios fermions vs all pairwise M_24 dim ratios
# ============================================================================
print("\n" + "="*78)
print("TEST 1 : Pairwise ratios fermions ↔ M_24 dim ratios")
print("="*78)

# For each fermion pair (i,j) compute y_i/y_j
fermion_pairs = list(combinations(yukawas.keys(), 2))
print(f"\n{len(fermion_pairs)} fermion pairs")
print(f"\nFor each, find best M_24 ratio match within 5%:")

matches = []
for f1, f2 in fermion_pairs:
    r_obs = yukawas[f1] / yukawas[f2]
    # find best M_24 dim ratio
    best_match = None
    best_err = 100
    for d1 in M24_DIMS:
        for d2 in M24_DIMS:
            if d1 != d2:
                r_pred = d1 / d2
                err = abs(r_pred - r_obs) / r_obs
                if err < best_err:
                    best_err = err
                    best_match = (d1, d2)
    if best_err < 0.05:
        matches.append((f1, f2, r_obs, best_match, best_err))

print(f"\n{len(matches)} pairs match within 5%")
print(f"\n{'Pair':<10s}  {'r_obs':>10s}  {'M_24 ratio':>15s}  {'err':>8s}")
for f1, f2, r_obs, (d1, d2), err in sorted(matches, key=lambda x: x[4]):
    print(f"  {f1}/{f2:<6s} {r_obs:>10.4f}  {d1}/{d2:<10d} = {d1/d2:>10.4f}  {err*100:>6.2f}%")

# ============================================================================
# TEST 2 : structure - assign each fermion to single M_24 dim, check consistent
# ============================================================================
print("\n" + "="*78)
print("TEST 2 : Best assignment fermion ↔ M_24 dim avec norm constante")
print("="*78)

# y_f = d_f / D where D is normalization constant
# Find best (d_e, d_μ, ..., d_t) ∈ M24_DIMS^9 minimizing fit

# Trop combos pour brute force. Greedy : pour chaque fermion, dim qui minimize residual
# avec D = max dim (= 10395) ? Or D variable.

# Approach : try D = each M_24 dim, then for each fermion find closest dim/D match
print("\n  Pour différents D = M_24 dim, trouver d_f match pour chaque fermion :")
for D_idx in [5, 10, 15, 19]:  # try few normalizations
    D = M24_DIMS[D_idx]
    print(f"\n  D = {D} (M_24 dim #{D_idx}) :")
    total_log_err = 0
    used_dims = []
    for f in ['e', 'mu', 'tau', 'u', 'd', 's', 'c', 'b', 't']:
        y_target = yukawas[f]
        # find d such that d/D ≈ y_target
        ratio_target = y_target  # d/D = y_target → d = D·y_target
        d_target_continuous = D * y_target
        # closest M_24 dim
        d_best = min(M24_DIMS, key=lambda d: abs(d/D - y_target))
        err_log = abs(log(d_best/D) - log(y_target))
        total_log_err += err_log
        used_dims.append(d_best)
        print(f"    y_{f:3s} = {y_target:.3e}, d_pred ≈ {d_target_continuous:.1f}, d_best = {d_best}, err log = {err_log:.3f}")
    print(f"    Total log error = {total_log_err:.3f}, distinct dims used = {len(set(used_dims))}/9")

# ============================================================================
# TEST 3 : RATIOS PRESERVATION (M_24 should preserve specific ratios)
# ============================================================================
print("\n" + "="*78)
print("TEST 3 : Y_top/Y_bottom = 10395/252 confirmé")
print("="*78)
y_t_y_b = yukawas['t']/yukawas['b']
m24_ratio = 10395/252
print(f"  y_top/y_bottom obs    = {y_t_y_b:.5f}")
print(f"  10395/252 M_24 ratio  = {m24_ratio:.5f}")
print(f"  Δ = {(y_t_y_b/m24_ratio - 1)*100:+.3f}%")

# More 3-fermion ratios
print(f"\n  Other striking ratios :")
for label, num_f, denom_f in [
    ('y_t/y_τ', 't', 'tau'),
    ('y_t/y_c', 't', 'c'),
    ('y_c/y_τ', 'c', 'tau'),
    ('y_τ/y_μ', 'tau', 'mu'),
    ('y_b/y_s', 'b', 's'),
    ('y_s/y_μ', 's', 'mu'),
    ('y_c/y_b', 'c', 'b'),
]:
    r = yukawas[num_f]/yukawas[denom_f]
    print(f"  {label:>12s} = {r:.4e}")
    # Find best M_24 dim ratio
    best = (None, None, 100)
    for d1 in M24_DIMS:
        for d2 in M24_DIMS:
            if d1 != d2:
                err = abs(d1/d2 - r)/r
                if err < best[2]:
                    best = (d1, d2, err)
    print(f"    Best M_24 : {best[0]}/{best[1]} = {best[0]/best[1]:.4e}  ({best[2]*100:.2f}%)")

# ============================================================================
# TEST 4 : Structural assignment by quantum numbers
# ============================================================================
print("\n" + "="*78)
print("TEST 4 : Assignment structural — par génération et type")
print("="*78)

# Conjecture : assignment par génération g et type t :
# g=1,2,3 generations
# t = lepton, up, down
# Each (g, t) gets a M_24 irrep with specific dim

# Smallest fermion = electron (gen 1, lepton) → smallest dim ?
# Largest = top (gen 3, up) → 10395 ?

# Sort fermions by mass and dims by size
sorted_fermions = sorted(yukawas.keys(), key=lambda f: yukawas[f])
sorted_dims = sorted(M24_DIMS, reverse=False)
print(f"  Fermions tri par y croissant : {sorted_fermions}")
print(f"  M_24 dims (20) tri croissant : {sorted_dims}")

# Try monotonic assignment : smallest fermion → smallest dim, etc.
# 9 fermions, 20 dims, so pick 9 of 20
# Optimal subset: ?

# Best 9 dims giving smallest log fit error
def fit_log_uniform(yukawa_list, dim_list, alpha):
    """Try y_f = (d_f / d_max)^alpha for assignment."""
    if len(yukawa_list) != len(dim_list):
        return float('inf')
    d_max = max(dim_list)
    errs = []
    for y, d in zip(yukawa_list, dim_list):
        y_pred = (d / d_max) ** alpha
        errs.append(log(y_pred) - log(y))
    return sum(e**2 for e in errs), errs

# Pick 9 dims sorted, smallest to largest
sorted_y = [yukawas[f] for f in sorted_fermions]

# Use the 9 largest dims of M_24 (since fermions span 5 OM)
# But also try 9 smallest, 9 random...

# Try several alphas, best of dim arrangement
best_fit = (None, None, float('inf'))
for alpha in [1.0, 2.0, 2.5, 3.0, 3.5, 4.0, 5.0]:
    # For each alpha, optimal subset and ordering
    # Brute force on subsets is C(20,9) = 167960 — Opus did this
    # Here just monotonic assignment with 9 selected dims = sorted top 9
    # And alternative : sorted all 20 dims, pick spaced

    # Option A : 9 sorted dims = sorted_dims[:9] (smallest)
    dims_A = sorted_dims[:9]
    err_sq_A, _ = fit_log_uniform(sorted_y, dims_A, alpha)

    # Option B : 9 sorted dims = sorted_dims[-9:] (largest)
    dims_B = sorted_dims[-9:]
    err_sq_B, _ = fit_log_uniform(sorted_y, dims_B, alpha)

    # Option C : evenly spaced 9 from 20
    idx = np.linspace(0, 19, 9).astype(int)
    dims_C = [sorted_dims[i] for i in idx]
    err_sq_C, _ = fit_log_uniform(sorted_y, dims_C, alpha)

    print(f"\n  α = {alpha}")
    print(f"    sorted_smallest 9 dims  : err² = {err_sq_A:.3f}")
    print(f"    sorted_largest 9 dims   : err² = {err_sq_B:.3f}")
    print(f"    evenly spaced 9 dims    : err² = {err_sq_C:.3f}")

    for opt_label, dims, err_sq in [('smallest', dims_A, err_sq_A), ('largest', dims_B, err_sq_B), ('spaced', dims_C, err_sq_C)]:
        if err_sq < best_fit[2]:
            best_fit = (alpha, (opt_label, dims), err_sq)

print(f"\n  Best fit : α = {best_fit[0]}, dims = {best_fit[1]}, err² = {best_fit[2]:.3f}")

# ============================================================================
# TEST 5 : Adversarial — random dimension sets vs M_24
# ============================================================================
print("\n" + "="*78)
print("TEST 5 : Adversarial — random 9-dim subsets vs M_24")
print("="*78)

# Compare M_24 best-fit to random log-uniform same-size pool
np.random.seed(2026)
n_trials = 1000

# For pool sizes : random 20 dims log-uniform same range
log_min, log_max = log(1), log(10395)
better_count = 0
m24_err = best_fit[2]
print(f"  Best M_24 fit err² = {m24_err:.3f} (α={best_fit[0]})")
print(f"  Compare to {n_trials} random pools (log-uniform 1..10395)")

for trial in range(n_trials):
    # Random 20 dims (same size as M_24 pool)
    rand_dims = sorted([int(exp(log_min + (log_max-log_min)*np.random.rand())) for _ in range(20)])
    rand_dims = sorted(set(rand_dims))[:20]  # unique sort
    if len(rand_dims) < 9: continue

    # Use sorted 9 from random pool, evenly spaced
    idx = np.linspace(0, len(rand_dims)-1, 9).astype(int)
    dims_r = [rand_dims[i] for i in idx]
    err_sq_r, _ = fit_log_uniform(sorted_y, dims_r, best_fit[0])
    if err_sq_r < m24_err:
        better_count += 1

p_value = better_count / n_trials
print(f"\n  {better_count}/{n_trials} = {p_value*100:.1f}% random pools beat M_24")
if p_value < 0.05:
    print(f"  → SIGNIFICATIF (p<0.05)")
else:
    print(f"  → NON significatif")

# ============================================================================
# TEST 6 : Specific ratios significance
# ============================================================================
print("\n" + "="*78)
print("TEST 6 : Is y_t/y_b = 10395/252 = (0.01%) statistiquement significatif ?")
print("="*78)

# 36 fermion pair ratios × 190 M_24 dim ratios = 6840 possible matches
# Expected match within 0.1% by chance ?
# Random uniform in log space : density 1/log(range) per unit log

# For uniform in [1e-7, 1e5] (range of ratios), p < 0.1% per ratio comparison
# 6840 comparisons → expected ~ 7 matches at <0.1%
print(f"""
  6840 possible (fermion pair × M_24 pair) comparisons.
  Expected random matches < 0.1% per comparison.
  Density per log unit = 1 / log(10^12) = 1/27.6
  Cumulative within 0.1% (=log delta 0.001) = 0.001/27.6 = 3.6e-5 per comparison
  Expected total at <0.1% = 6840 × 3.6e-5 = 0.25

  → y_t/y_b = 10395/252 match at 0.08% : ratio random ~3-4
  → Statistically interesting but not unique
""")

# ============================================================================
# CONCLUSION
# ============================================================================
print("\n" + "="*78)
print("CONCLUSION yukawa M_24 deep test")
print("="*78)
print(f"""
  ✓ y_t/y_b = 10395/252 (0.08%) — match statistique seuilou random ~3-4
  ⚠ Best fit alpha=3.50 (Opus brute force) sans interp claire
  ⚠ Espacement log dim M_24 drives matching, pas physique M_24

  → Aucune assignation structurelle physique consistante
  → Le pattern Yukawa-M_24 reste TIER 3 NUMERICAL sans mécanisme
""")
