#!/usr/bin/env python3
"""PySR dédié QNM Schwarzschild + Kerr — test horizon = SU(2) régime.

Source : Berti, Cardoso, Starinets 2009 "Quasi-normal modes of black holes
and black branes" arXiv:0905.2975 (~120 values tabulated).
+ Berti-Cardoso 2006 perturbation theory + Berti's QNM webpage data.

Cible : ratios indépendants de la masse, indépendants de l'échelle.
        Seule géométrie de l'horizon.
Si tous matchent κ_SU(2) = 1/2 ↔ rationals, support horizon-SU(2).
"""
import math
import time
import json
import numpy as np
from scipy.spatial import cKDTree
from multiprocessing import Pool, cpu_count
from scipy.stats import norm

START = time.time()
print(f"START : {time.ctime()}")
print("=" * 78)
print(f"PySR QNM DEDICATED — horizon = SU(2) hypothesis")
print("=" * 78)

KAPPA_SU2 = 1/2
KAPPA_SU3 = 1/6
PI = math.pi
N_CPUS = cpu_count()
N_BOOTSTRAP = 1000

# Candidate library : favorise κ_SU(2)
a_set = np.array([-3, -2, -1.5, -1, -0.5, 0, 0.5, 1, 1.5, 2, 3])
b_set = np.array([-2, -1, -0.5, 0, 0.5, 1, 2])
d_set = np.array([-2, -1, -0.5, 0, 0.5, 1, 2])
n_set = np.arange(1, 25)
m_set = np.arange(1, 25)

print(f"\nBuilding candidates : κ_SU2^a · κ_SU3^b · π^d · (n/m), TW ≤ 2...")
t1 = time.time()
candidates_list = []
for a in a_set:
    for b in b_set:
        for d in d_set:
            tw = abs(a) + abs(b) + abs(d)
            if tw > 2:
                continue
            base = (KAPPA_SU2**a) * (KAPPA_SU3**b) * (PI**d)
            for n in n_set:
                for m in m_set:
                    if math.gcd(n, m) > 1:
                        continue
                    v = base * n / m
                    if v > 0 and 1e-4 < v < 1e3:  # narrow range = QNM ratios
                        candidates_list.append((v, a, b, d, n, m, tw))

candidates_arr = np.array([cd[0] for cd in candidates_list])
n_cand = len(candidates_arr)
print(f"Built {n_cand} candidates in {time.time()-t1:.1f}s")

log_candidates = np.log(candidates_arr)
sort_idx = np.argsort(log_candidates)
log_candidates_sorted = log_candidates[sort_idx]
tree = cKDTree(log_candidates_sorted.reshape(-1, 1))

# === QNM Schwarzschild (Berti-Cardoso-Starinets 2009 Table)===
# Mω_R, MωI for various ℓ, n=0 (fundamental) and n=1 (first overtone)
# Schwarzschild values: a=0
SCHW_QNM = {
    # ℓ, n, M*ω_R, M*ω_I (imaginary = damping)
    (2, 0): (0.37367, 0.08896),
    (2, 1): (0.34671, 0.27391),
    (2, 2): (0.30105, 0.47828),
    (3, 0): (0.59944, 0.09270),
    (3, 1): (0.58264, 0.28130),
    (3, 2): (0.55169, 0.47909),
    (4, 0): (0.80918, 0.09416),
    (4, 1): (0.79663, 0.28433),
    (4, 2): (0.77272, 0.48133),
    (5, 0): (1.01230, 0.09487),
    (5, 1): (1.00244, 0.28598),
    (6, 0): (1.21201, 0.09524),
}

# === Kerr QNM ===
# (ℓ, m=ℓ, n, a/M, M*ω_R, M*ω_I)
KERR_QNM_LM_EQ_L_N0 = {
    (2, 0.0): (0.37367, 0.08896),
    (2, 0.1): (0.39264, 0.08884),
    (2, 0.3): (0.43653, 0.08763),
    (2, 0.5): (0.49093, 0.08358),
    (2, 0.7): (0.56787, 0.07475),
    (2, 0.9): (0.67165, 0.05641),
    (2, 0.99): (0.83217, 0.01793),
    (3, 0.0): (0.59944, 0.09270),
    (3, 0.5): (0.78073, 0.08698),
    (3, 0.7): (0.89934, 0.07736),
    (3, 0.9): (1.05483, 0.05804),
    (4, 0.0): (0.80918, 0.09416),
    (4, 0.5): (1.04795, 0.08817),
    (4, 0.7): (1.20316, 0.07810),
    (4, 0.9): (1.40432, 0.05828),
}

PRE_REGISTERED = []

# Schwarzschild absolute values + Q-factors
for (l, n), (wR, wI) in SCHW_QNM.items():
    PRE_REGISTERED.append((f"M·ω_R Schw ℓ={l}, n={n}", wR))
    PRE_REGISTERED.append((f"M·ω_I Schw ℓ={l}, n={n}", wI))
    Q = wR / (2 * wI)
    PRE_REGISTERED.append((f"Q Schw ℓ={l}, n={n}", Q))

# Schwarzschild RATIOS (most powerful — scale-free, mass-free)
schw_keys = list(SCHW_QNM.keys())
for i in range(len(schw_keys)):
    for j in range(i+1, len(schw_keys)):
        (l1, n1) = schw_keys[i]
        (l2, n2) = schw_keys[j]
        wR1, wI1 = SCHW_QNM[(l1, n1)]
        wR2, wI2 = SCHW_QNM[(l2, n2)]
        # Real frequency ratios
        if wR1 < wR2:
            r = wR2 / wR1
            PRE_REGISTERED.append((f"ω_R({l2},{n2})/ω_R({l1},{n1})", r))
        else:
            r = wR1 / wR2
            PRE_REGISTERED.append((f"ω_R({l1},{n1})/ω_R({l2},{n2})", r))

# Kerr ratios at different spins
for (l, a), (wR, wI) in KERR_QNM_LM_EQ_L_N0.items():
    PRE_REGISTERED.append((f"M·ω_R Kerr ℓ={l} a={a}", wR))
    if a > 0:  # spin-dependent ratio
        wR_0 = SCHW_QNM[(l, 0)][0] if (l, 0) in SCHW_QNM else None
        if wR_0:
            r_spin = wR / wR_0
            PRE_REGISTERED.append((f"ω_R(ℓ={l},a={a})/ω_R(ℓ={l},a=0)", r_spin))

# Cross-spin Kerr ratios (same ℓ)
kerr_keys_l2 = [(l, a) for (l, a) in KERR_QNM_LM_EQ_L_N0.keys() if l == 2 and a > 0]
for i, k1 in enumerate(kerr_keys_l2):
    for k2 in kerr_keys_l2[i+1:]:
        wR1 = KERR_QNM_LM_EQ_L_N0[k1][0]
        wR2 = KERR_QNM_LM_EQ_L_N0[k2][0]
        r = max(wR1, wR2) / min(wR1, wR2)
        PRE_REGISTERED.append((f"ω_R(ℓ=2, a={k2[1]})/ω_R(ℓ=2, a={k1[1]})", r))

# Real-LIGO ringdown events (dimensionless products f·T = M·ω)
LIGO_RINGDOWN = [
    ("GW150914 M·ω (62 M_sun, 250 Hz)", 62*1.989e30*9e16/(1.0545e-34) * 2*math.pi*250 / (62*1.989e30*9e16/(1.0545e-34))),  # just M·ω
    ("GW170817 NS-NS M·ω post-merger", 0.5),  # estimate
    ("GW190521 BBH M·ω peak (150 M_sun)", 0.45),  # estimate
]
# Simplified: focus on the ringdown frequency ratios across events
# These are dimensionless ratios

# Bekenstein-Hawking related
BH_OTHER = [
    ("BH spin a_max/M = 1", 1.0),
    ("BH r_ISCO/M Schwarz", 6.0),
    ("BH r_horizon/M Schwarz", 2.0),
    ("BH r_ISCO/r_horizon Schwarz", 3.0),
    ("Hawking T·M Schwarz", 1/(8*math.pi)),
    ("S_BH/πr_S² (Bekenstein)", 1/(4*1.0)),  # =1/4 dimensionless if ℓ_P=1
    ("BH photon sphere r/M", 3.0),
]
PRE_REGISTERED.extend(BH_OTHER)

print(f"\nTotal observables : {len(PRE_REGISTERED)}")

target_vals = np.array([abs(v) for _, v in PRE_REGISTERED])
target_logs = np.log(target_vals)

real_distances, real_indices = tree.query(target_logs.reshape(-1, 1), k=1)
real_rel = np.exp(real_distances.flatten()) - 1

tolerance_levels = [1e-5, 1e-4, 1e-3, 5e-3, 0.01, 0.02, 0.05]
real_hits = {tol: int(np.sum(real_rel < tol)) for tol in tolerance_levels}

val_min, val_max = target_vals.min(), target_vals.max()
log_min, log_max = math.log(val_min), math.log(val_max)

def bootstrap_one(seed):
    np.random.seed(seed)
    rand_logs = np.random.uniform(log_min, log_max, len(target_vals))
    distances, _ = tree.query(rand_logs.reshape(-1, 1), k=1)
    rel = np.exp(distances.flatten()) - 1
    return tuple(int(np.sum(rel < t)) for t in tolerance_levels)

t3 = time.time()
with Pool(N_CPUS) as pool:
    boot_results = pool.map(bootstrap_one, range(2026, 2026 + N_BOOTSTRAP))
boot_results = np.array(boot_results)

print(f"\n{'='*78}\nRESULTS — QNM DEDICATED ({len(PRE_REGISTERED)} obs)\n{'='*78}\n")
print(f"{'Tol':>10} {'Real':>6} {'Random μ±σ':>18} {'Z':>10}")
print("-"*70)

z_scores = {}
for i, tol in enumerate(tolerance_levels):
    real = real_hits[tol]
    rand_mean = boot_results[:, i].mean()
    rand_std = boot_results[:, i].std()
    z = (real - rand_mean) / max(rand_std, 0.01)
    sig = "✓✓" if z > 4 else "✓" if z > 3 else "🟡" if z > 2 else ""
    print(f"  <{tol*100:.4f}% {real:>6} {rand_mean:>8.1f}±{rand_std:>6.2f} {z:>+9.2f}σ {sig}")
    z_scores[tol] = {"real": int(real), "random_mean": float(rand_mean),
                     "random_std": float(rand_std), "z": float(z)}

print(f"\nTop 40 matches (sorted by rel diff):")
sort_real = np.argsort(real_rel)
top_hits = []
for k in range(min(40, len(PRE_REGISTERED))):
    i = sort_real[k]
    name = PRE_REGISTERED[i][0]
    val = PRE_REGISTERED[i][1]
    cand_idx = sort_idx[real_indices[i]]
    cand_meta = candidates_list[cand_idx]
    cand_v = cand_meta[0]
    a, b, d, n, m, tw = cand_meta[1:]
    rel = real_rel[i] * 100
    formula = f"κ_SU2^{a}·κ_SU3^{b}·π^{d}·({n}/{m})"
    print(f"  {name:>50} obs={val:.5e} pred={cand_v:.5e} ({rel:.4f}%) TW={tw} {formula}")
    top_hits.append({"name": name, "obs": float(val), "pred": float(cand_v),
                     "rel_pct": float(rel), "tw": float(tw), "formula": formula})

output = {"domain": "QNM_dedicated", "n_obs": len(PRE_REGISTERED),
          "n_candidates": n_cand, "z_scores": z_scores, "top_hits": top_hits}
with open("/tmp/pysr_qnm_dedicated_results.json", "w") as f:
    json.dump(output, f, indent=2)
print(f"\nElapsed : {time.time()-START:.1f}s")
print(f"Saved : /tmp/pysr_qnm_dedicated_results.json")
print(f"DONE.")
