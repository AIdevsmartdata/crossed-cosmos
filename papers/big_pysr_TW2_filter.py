#!/usr/bin/env python3
"""BIG PySR — filter TW ≤ 2 only (structurels solides uniquement).

Test : avec espace candidat RESTREINT (formules simples seulement),
quelle est la Z-score significance ?

Si Z reste > 3σ → 21 patterns sont vraiment STRUCTURELS solides
Si Z chute < 1σ → tout signal était dû à model space riche (TW=3-5)
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
print(f"PySR TW≤2 FILTER — test structural solidity")
print(f"="*78)

KAPPA = 1/6
PI = math.pi
N_CPUS = cpu_count()
N_BOOTSTRAP = 1000

# Same exposants raffinés but TW filter strict
a_set = np.array([-3, -2, -1, -0.5, 0, 0.5, 1, 1.5, 2, 3])
b_set = np.array([-2, -1, -0.5, 0, 0.5, 1, 2])
c_set = np.array([-1, -0.5, 0, 0.5, 1])
d_set = np.array([-1, -0.5, 0, 0.5, 1])
n_set = np.arange(1, 21)
m_set = np.arange(1, 21)

TW_MAX = 2  # FILTRE STRICT

print(f"\nBuilding candidates (TW ≤ {TW_MAX})...")
t1 = time.time()
candidates_list = []
for a in a_set:
    for b in b_set:
        for c in c_set:
            for d in d_set:
                tw = abs(a) + abs(b) + abs(c) + abs(d)
                if tw > TW_MAX:
                    continue
                base = (KAPPA**a) * ((1-KAPPA)**b) * ((1+KAPPA)**c) * (PI**d)
                for n in n_set:
                    for m in m_set:
                        if math.gcd(n, m) > 1:
                            continue
                        v = base * n / m
                        if v > 0 and 1e-6 < v < 1e8:
                            candidates_list.append((v, a, b, c, d, n, m, tw))

candidates_arr = np.array([c[0] for c in candidates_list])
n_cand = len(candidates_arr)
elapsed = time.time() - t1
print(f"Built {n_cand} candidates in {elapsed:.1f}s (FILTRÉ vs 391170 sans filter)")

# Log-space + KDTree
log_candidates = np.log(candidates_arr)
sort_idx = np.argsort(log_candidates)
log_candidates_sorted = log_candidates[sort_idx]
tree = cKDTree(log_candidates_sorted.reshape(-1, 1))

# Targets pre-registered
PRE_REGISTERED = [
    ("V_td_CKM",          0.00876),
    ("V_cd_CKM",          0.22487),
    ("V_ts_CKM",          0.04117),
    ("sin²θ12_PMNS",      0.307),
    ("δ_CP/(2π)_PMNS",    0.2160),
    ("sin²2θ12_PMNS",     0.851),
    ("sin²2θ23_PMNS",     0.985),
    ("m_τ/m_μ",           1776.86/105.66),
    ("m_τ/m_e",           1776.86/0.511),
    ("m_μ/m_e",           105.66/0.511),
    ("m_d/m_u",           4.67/2.16),
    ("m_s/m_d",           93.4/4.67),
    ("m_c/m_s",           1270/93.4),
    ("m_b/m_c",           4180/1270),
    ("m_t/m_b",           172570/4180),
    ("m_K/m_π",           493.677/139.570),
    ("m_η/m_π",           547.862/139.570),
    ("m_ρ/m_π",           775.26/139.570),
    ("m_K*/m_K",          891.66/493.677),
    ("m_ω/m_ρ",           782.65/775.26),
    ("m_φ/m_ω",           1019.461/782.65),
    ("m_η'/m_η",          957.78/547.862),
    ("m_n/m_p",           939.565/938.272),
    ("m_Λ/m_p",           1115.683/938.272),
    ("m_Σ+/m_p",          1189.37/938.272),
    ("m_Ξ0/m_p",          1314.86/938.272),
    ("m_Ω/m_p",           1672.45/938.272),
    ("m_Δ/m_p",           1232.0/938.272),
    ("m_Λ_c/m_p",         2286.46/938.272),
    ("m_Λ_b/m_p",         5619.6/938.272),
    ("m_ψ(2S)/m_J/ψ",     3686.097/3096.9),
    ("m_χc0/m_J/ψ",       3414.71/3096.9),
    ("m_Υ(2S)/m_Υ(1S)",   10023.26/9460.4),
    ("m_J/ψ/m_p",         3096.9/938.272),
    ("m_W/m_Z",           80.377/91.188),
    ("m_H/m_Z",           125.25/91.188),
    ("m_H/m_W",           125.25/80.377),
    ("m_H/v",             125.25/246.22),
    ("sin²θ_W_eff",       0.23857),
    ("sin²θ_W_MSbar_MZ",  0.23121),  # Standard PDG
    ("α_s(M_Z)",          0.1179),
    ("g_A_axial",         1.2754),
    ("f_K/f_π",           110.4/92.4),
    ("Ω_b/Ω_m",           0.049/0.315),
    ("Ω_DM/Ω_b",          5.4),
    ("Ω_Λ_h²",            0.6847*0.674**2),
    ("n_s",               0.9649),
    ("Γ_Υ/m_Υ",           5.4e-5/9.46),
    ("τ_n_per_m_p",       880.2/939.565),
    ("|μ_p|",             2.7928),
    ("|μ_n|/|μ_p|",       1.91304/2.7928),
]

target_vals = np.array([v for _, v in PRE_REGISTERED])
target_logs = np.log(target_vals)

# Match
real_distances, real_indices = tree.query(target_logs.reshape(-1, 1), k=1)
real_rel = np.exp(real_distances.flatten()) - 1

# Multi tolerance
tolerance_levels = [1e-5, 1e-4, 1e-3, 5e-3, 0.01, 0.02, 0.05]

real_hits = {}
for tol in tolerance_levels:
    real_hits[tol] = int(np.sum(real_rel < tol))

# Bootstrap baseline
val_min, val_max = target_vals.min(), target_vals.max()
log_min, log_max = math.log(val_min), math.log(val_max)

def bootstrap_one(seed):
    np.random.seed(seed)
    rand_logs = np.random.uniform(log_min, log_max, len(target_vals))
    distances, _ = tree.query(rand_logs.reshape(-1, 1), k=1)
    rel = np.exp(distances.flatten()) - 1
    return tuple(int(np.sum(rel < t)) for t in tolerance_levels)

with Pool(N_CPUS) as pool:
    boot_results = pool.map(bootstrap_one, range(2026, 2026 + N_BOOTSTRAP))
boot_results = np.array(boot_results)

# Z-scores
print(f"\n{'='*78}")
print(f"RESULTS — TW ≤ {TW_MAX} filter")
print(f"{'='*78}")
print(f"\n{'Tol':>10} {'Real':>6} {'Random μ±σ':>18} {'Z':>10} {'p-value':>15}")
print("-"*70)
from scipy.stats import norm
verdict = {}
for i, tol in enumerate(tolerance_levels):
    real = real_hits[tol]
    rand_mean = boot_results[:, i].mean()
    rand_std = boot_results[:, i].std()
    z = (real - rand_mean) / max(rand_std, 0.01)
    p_value = 1 - norm.cdf(z)
    sig = "✓✓" if z > 4 else "✓" if z > 3 else "🟡" if z > 2 else ""
    print(f"  <{tol*100:.4f}% {real:>6} {rand_mean:>8.1f}±{rand_std:>6.2f} {z:>+9.2f}σ {p_value:>15.3e} {sig}")
    verdict[tol] = (real, rand_mean, rand_std, z)

# Top matches sorted
print(f"\nTop 20 matches sorted by rel diff (TW ≤ {TW_MAX}) :")
sort_real = np.argsort(real_rel)
for k in range(min(20, len(PRE_REGISTERED))):
    i = sort_real[k]
    name = PRE_REGISTERED[i][0]
    val = PRE_REGISTERED[i][1]
    cand_idx = sort_idx[real_indices[i]]
    cand_meta = candidates_list[cand_idx]
    cand_v = cand_meta[0]
    a, b, c, d, n, m, tw = cand_meta[1:]
    rel = real_rel[i] * 100
    formula = f"κ^{a}·(1-κ)^{b}·(1+κ)^{c}·π^{d}·({n}/{m})"
    print(f"  {name:>25} obs={val:.6f} pred={cand_v:.6f} ({rel:.4f}%) TW={tw} {formula}")

# Save
output = {
    "filter": f"TW <= {TW_MAX}",
    "n_candidates": n_cand,
    "n_pre_registered": len(PRE_REGISTERED),
    "n_bootstrap": N_BOOTSTRAP,
    "z_scores": {f"{t*100:.4f}%": {
        "real": int(verdict[t][0]),
        "random_mean": float(verdict[t][1]),
        "random_std": float(verdict[t][2]),
        "z": float(verdict[t][3]),
    } for t in tolerance_levels},
}
with open("/tmp/big_pysr_TW2_results.json", "w") as f:
    json.dump(output, f, indent=2)

print(f"\nElapsed : {time.time()-START:.1f}s")
print(f"Saved : /tmp/big_pysr_TW2_results.json")
print(f"END : {time.ctime()}")
print(f"DONE.")
