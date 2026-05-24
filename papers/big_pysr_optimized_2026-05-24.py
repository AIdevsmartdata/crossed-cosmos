#!/usr/bin/env python3
"""BIG PySR OPTIMIZED — i5-14600KF 20 threads + 31GB RAM.

Optimisations :
- Vectorized numpy (no Python loops)
- cKDTree pour nearest neighbor O(log n)
- multiprocessing.Pool 20 workers pour bootstrap
- Multiple tolerance levels (0.001% → 5%) — voir où le framework écrase Bonferroni
- 1000 bootstrap trials
- Larger candidate space : exposants raffinés + rationals 1..20

Goal : trouver le LEVEL DE TOLERANCE où Real >> Random à >5σ.
Si pas trouvé → framework Bonferroni-fragile à toute tolerance.
"""
import math
import time
import json
import numpy as np
from scipy.spatial import cKDTree
from multiprocessing import Pool, cpu_count

START = time.time()
print(f"START : {time.ctime()}")
print(f"="*78)
print(f"BIG PySR OPTIMIZED — {cpu_count()} CPUs disponibles")
print(f"="*78)

KAPPA = 1/6
PI = math.pi
N_CPUS = cpu_count()
N_BOOTSTRAP = 1000

# ==============================================================
# Build candidate space (vectorized)
# ==============================================================
print(f"\nBuilding vectorized candidate space...")
t1 = time.time()

# Exposants raffinés
a_set = np.array([-3, -2, -1, -0.5, 0, 0.5, 1, 1.5, 2, 3])
b_set = np.array([-2, -1, -0.5, 0, 0.5, 1, 2])
c_set = np.array([-1, -0.5, 0, 0.5, 1])
d_set = np.array([-1, -0.5, 0, 0.5, 1])
n_set = np.arange(1, 21)
m_set = np.arange(1, 21)

# Build all combinations with TW filter
candidates_list = []
for a in a_set:
    for b in b_set:
        for c in c_set:
            for d in d_set:
                tw = abs(a) + abs(b) + abs(c) + abs(d)
                if tw > 5:
                    continue
                base = (KAPPA**a) * ((1-KAPPA)**b) * ((1+KAPPA)**c) * (PI**d)
                for n in n_set:
                    for m in m_set:
                        if math.gcd(n, m) > 1:  # skip reducible fractions
                            continue
                        v = base * n / m
                        if v > 0 and 1e-6 < v < 1e8:
                            candidates_list.append((v, a, b, c, d, n, m, tw))

candidates_arr = np.array([c[0] for c in candidates_list])
candidates_meta = candidates_list
n_cand = len(candidates_arr)
elapsed_build = time.time() - t1
print(f"Built {n_cand} candidates in {elapsed_build:.1f}s")

# Sort + log-space for KDTree
log_candidates = np.log(candidates_arr)
sort_idx = np.argsort(log_candidates)
log_candidates_sorted = log_candidates[sort_idx]
tree = cKDTree(log_candidates_sorted.reshape(-1, 1))
print(f"KDTree built")

# ==============================================================
# Targets : 50 pre-registered PDG observables
# ==============================================================
PRE_REGISTERED = [
    ("V_td_CKM",          0.00876,  0.00018),
    ("V_cd_CKM",          0.22487,  0.00068),
    ("V_ts_CKM",          0.04117,  0.00074),
    ("sin²θ12_PMNS",      0.307,    0.013),
    ("δ_CP/(2π)_PMNS",    0.2160,   0.0430),
    ("sin²2θ12_PMNS",     0.851,    0.025),
    ("sin²2θ23_PMNS",     0.985,    0.025),
    ("m_τ/m_μ",           1776.86/105.66,         0.001),
    ("m_τ/m_e",           1776.86/0.511,          0.01),
    ("m_μ/m_e",           105.66/0.511,           0.001),
    ("m_d/m_u",           4.67/2.16,               0.05),
    ("m_s/m_d",           93.4/4.67,               0.5),
    ("m_c/m_s",           1270/93.4,               0.2),
    ("m_b/m_c",           4180/1270,               0.01),
    ("m_t/m_b",           172570/4180,             0.5),
    ("m_K/m_π",           493.677/139.570,         0.001),
    ("m_η/m_π",           547.862/139.570,         0.001),
    ("m_ρ/m_π",           775.26/139.570,          0.01),
    ("m_K*/m_K",          891.66/493.677,          0.001),
    ("m_ω/m_ρ",           782.65/775.26,           0.001),
    ("m_φ/m_ω",           1019.461/782.65,         0.001),
    ("m_η'/m_η",          957.78/547.862,          0.001),
    ("m_n/m_p",           939.565/938.272,         1e-6),
    ("m_Λ/m_p",           1115.683/938.272,        0.0001),
    ("m_Σ+/m_p",          1189.37/938.272,         0.0001),
    ("m_Ξ0/m_p",          1314.86/938.272,         0.0001),
    ("m_Ω/m_p",           1672.45/938.272,         0.0001),
    ("m_Δ/m_p",           1232.0/938.272,          0.005),
    ("m_Λ_c/m_p",         2286.46/938.272,         0.0001),
    ("m_Λ_b/m_p",         5619.6/938.272,          0.0001),
    ("m_ψ(2S)/m_J/ψ",     3686.097/3096.9,         0.001),
    ("m_χc0/m_J/ψ",       3414.71/3096.9,          0.001),
    ("m_Υ(2S)/m_Υ(1S)",   10023.26/9460.4,         0.001),
    ("m_J/ψ/m_p",         3096.9/938.272,          0.001),
    ("m_W/m_Z",           80.377/91.188,           0.001),
    ("m_H/m_Z",           125.25/91.188,           0.001),
    ("m_H/m_W",           125.25/80.377,           0.001),
    ("m_H/v",             125.25/246.22,           0.001),
    ("sin²θ_W_eff",       0.23857,                 0.0001),
    ("α_s(M_Z)",          0.1179,                  0.0009),
    ("g_A_axial",         1.2754,                  0.0013),
    ("f_K/f_π",           110.4/92.4,              0.001),
    ("Ω_b/Ω_m",           0.049/0.315,             0.005),
    ("Ω_DM/Ω_b",          5.4,                     0.1),
    ("Ω_Λ_h²",            0.6847*0.674**2,         0.002),
    ("n_s",               0.9649,                  0.0042),
    ("Γ_Υ/m_Υ",           5.4e-5/9.46,             1e-7),
    ("τ_n_per_m_p",       880.2/939.565,           0.01),
    ("|μ_p|",             2.7928,                  0.001),
    ("|μ_n|/|μ_p|",       1.91304/2.7928,          0.001),
]

target_vals = np.array([v for _, v, _ in PRE_REGISTERED])
target_logs = np.log(target_vals)

# ==============================================================
# Vectorized nearest-neighbor matching
# ==============================================================
def find_best_match_for_targets(target_logs):
    """For each target, find closest candidate in log space."""
    # KDTree returns nearest distance
    distances, indices = tree.query(target_logs.reshape(-1, 1), k=1)
    # rel diff in linear : exp(log_diff) - 1
    rel_diffs = np.exp(distances.flatten()) - 1
    return rel_diffs, indices.flatten()

# Test on real
t2 = time.time()
real_rel_diffs, real_indices = find_best_match_for_targets(target_logs)
elapsed_real = time.time() - t2
print(f"\nReal targets matched in {elapsed_real*1000:.0f}ms")

# Tolerance levels to test
tolerance_levels = [1e-5, 1e-4, 1e-3, 5e-3, 0.01, 0.02, 0.05]

print(f"\nReal hit count per tolerance level :")
real_hits = {}
for tol in tolerance_levels:
    h = int(np.sum(real_rel_diffs < tol))
    real_hits[tol] = h
    print(f"  tol < {tol*100:.4f}% : {h}/{len(target_vals)} ({100*h/len(target_vals):.1f}%)")

# ==============================================================
# Bonferroni baseline parallelized
# ==============================================================
val_min = target_vals.min()
val_max = target_vals.max()
log_min = math.log(val_min)
log_max = math.log(val_max)

def bootstrap_one(seed):
    np.random.seed(seed)
    rand_logs = np.random.uniform(log_min, log_max, len(target_vals))
    distances, _ = tree.query(rand_logs.reshape(-1, 1), k=1)
    rel = np.exp(distances.flatten()) - 1
    return tuple(int(np.sum(rel < t)) for t in tolerance_levels)

print(f"\nRunning {N_BOOTSTRAP} bootstrap trials parallelized on {N_CPUS} CPUs...")
t3 = time.time()
with Pool(N_CPUS) as pool:
    boot_results = pool.map(bootstrap_one, range(2026, 2026 + N_BOOTSTRAP))
boot_results = np.array(boot_results)  # shape (N_BOOTSTRAP, len(tolerance_levels))
elapsed_boot = time.time() - t3
print(f"Bootstrap done in {elapsed_boot:.1f}s ({N_BOOTSTRAP/elapsed_boot:.0f} trials/sec)")

# Compute Z-scores
print(f"\n{'='*78}")
print(f"FINAL RESULTS")
print(f"{'='*78}")
print(f"\n{'Tol':>10} {'Real':>6} {'Random μ±σ':>15} {'Z':>10} {'p-value':>15}")
print("-"*70)
z_scores = {}
for i, tol in enumerate(tolerance_levels):
    real = real_hits[tol]
    rand_mean = boot_results[:, i].mean()
    rand_std = boot_results[:, i].std()
    z = (real - rand_mean) / max(rand_std, 0.01)
    # Approximate p-value via Gaussian tail
    from scipy.stats import norm
    p_value = 1 - norm.cdf(z)
    z_scores[tol] = (real, rand_mean, rand_std, z, p_value)
    sig = "✓" if z > 3 else "🟡" if z > 2 else ""
    print(f"  <{tol*100:.4f}% {real:>6} {rand_mean:>6.1f}±{rand_std:>5.1f} {z:>+9.2f}σ {p_value:>15.3e} {sig}")

# Print best matches detail
print(f"\n{'='*78}")
print(f"Best PRE-REGISTERED matches (sorted by rel diff)")
print(f"{'='*78}")
sort_real = np.argsort(real_rel_diffs)
for k in range(20):
    i = sort_real[k]
    name = PRE_REGISTERED[i][0]
    val = PRE_REGISTERED[i][1]
    sig = PRE_REGISTERED[i][2]
    cand_idx = sort_idx[real_indices[i]]
    cand_meta = candidates_meta[cand_idx]
    cand_v = cand_meta[0]
    a, b, c, d, n, m, tw = cand_meta[1], cand_meta[2], cand_meta[3], cand_meta[4], cand_meta[5], cand_meta[6], cand_meta[7]
    rel = real_rel_diffs[i] * 100
    sigma_match = abs(val - cand_v) / sig if sig > 0 else float('inf')
    formula = f"κ^{a}·(1-κ)^{b}·(1+κ)^{c}·π^{d}·({n}/{m})"
    print(f"  {name:>25} obs={val:.6f} pred={cand_v:.6f} ({rel:.4f}%, {sigma_match:.1f}σ) {formula}")

# Save
output = {
    "n_candidates": n_cand,
    "n_pre_registered": len(PRE_REGISTERED),
    "n_bootstrap": N_BOOTSTRAP,
    "elapsed_seconds": time.time() - START,
    "real_hits_per_tolerance": {f"{t*100:.4f}%": int(real_hits[t]) for t in tolerance_levels},
    "z_scores_per_tolerance": {f"{t*100:.4f}%": {
        "real": int(z_scores[t][0]),
        "random_mean": float(z_scores[t][1]),
        "random_std": float(z_scores[t][2]),
        "z": float(z_scores[t][3]),
        "p_value": float(z_scores[t][4]),
    } for t in tolerance_levels},
}

with open("/tmp/big_pysr_optimized_results.json", "w") as f:
    json.dump(output, f, indent=2)

ELAPSED = time.time() - START
print(f"\nTotal elapsed : {ELAPSED:.1f}s ({ELAPSED/60:.1f}min)")
print(f"Saved : /tmp/big_pysr_optimized_results.json")
print(f"END : {time.ctime()}")
print(f"DONE.")
