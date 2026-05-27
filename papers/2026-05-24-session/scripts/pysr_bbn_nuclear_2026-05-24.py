#!/usr/bin/env python3
"""PySR BBN + Nuclear binding + Phase shifts — domaines variés."""
import math
import time
import json
import numpy as np
from scipy.spatial import cKDTree
from multiprocessing import Pool, cpu_count
from scipy.stats import norm

START = time.time()
print(f"START : {time.ctime()}\n" + "="*78 + f"\nPySR BBN + Nuclear + Phase shifts\n" + "="*78)

KAPPA = 1/6
PI = math.pi
N_CPUS = cpu_count()
N_BOOTSTRAP = 1000
TW_MAX = 2

a_set = np.array([-3, -2, -1, -0.5, 0, 0.5, 1, 1.5, 2, 3])
b_set = np.array([-2, -1, -0.5, 0, 0.5, 1, 2])
c_set = np.array([-1, -0.5, 0, 0.5, 1])
d_set = np.array([-1, -0.5, 0, 0.5, 1])
n_set = np.arange(1, 21)
m_set = np.arange(1, 21)

t1 = time.time()
candidates_list = []
for a in a_set:
    for b in b_set:
        for c in c_set:
            for d in d_set:
                tw = abs(a) + abs(b) + abs(c) + abs(d)
                if tw > TW_MAX: continue
                base = (KAPPA**a) * ((1-KAPPA)**b) * ((1+KAPPA)**c) * (PI**d)
                for n in n_set:
                    for m in m_set:
                        if math.gcd(n, m) > 1: continue
                        v = base * n / m
                        if v > 0 and 1e-6 < v < 1e8:
                            candidates_list.append((v, a, b, c, d, n, m, tw))
candidates_arr = np.array([c[0] for c in candidates_list])
n_cand = len(candidates_arr)
print(f"Built {n_cand} candidates in {time.time()-t1:.1f}s")

log_candidates = np.log(candidates_arr)
sort_idx = np.argsort(log_candidates)
log_candidates_sorted = log_candidates[sort_idx]
tree = cKDTree(log_candidates_sorted.reshape(-1, 1))

# === BBN abundances PDG 2024 ===
PRE_REGISTERED = [
    # Primordial abundances (number ratios to H)
    ("Y_p (He-4 mass fraction)",  0.2453),
    ("D/H × 10⁵",                  2.527),
    ("He³/H × 10⁵",                1.1),
    ("Li⁷/H × 10¹⁰",               1.6),
    ("η_B × 10¹⁰ (baryon/photon)", 6.10),
    ("Y_p · η⁻¹·10¹⁰",             0.2453/6.10*10),
    # Cross-ratios
    ("D/H / Li⁷",                  2.527e-5/1.6e-10),  # large number
    ("Y_p · (η/6.10)⁰·⁰⁵",         0.2453),  # near-flat scaling
    # Λ_QCD / quark masses (BBN sensitive to these)
    ("m_n - m_p [MeV]",            1.2933),  # nucleon mass diff
    ("(m_n-m_p)/m_e",              1.2933/0.511),
    ("(m_n-m_p)/(m_d-m_u)",        1.2933/(4.67-2.16)),
]

# === Nuclear binding energies per nucleon (AME 2020) ===
NUCLEAR_BINDING = [
    ("D (²H) B/A [MeV]",    1.11),
    ("T (³H) B/A",          2.83),
    ("³He B/A",             2.57),
    ("⁴He B/A",             7.07),
    ("⁶Li B/A",             5.33),
    ("⁸Be B/A",             7.06),
    ("¹²C B/A",             7.68),
    ("¹⁶O B/A",             7.98),
    ("²⁰Ne B/A",            8.03),
    ("²⁸Si B/A",            8.45),
    ("³²S B/A",             8.49),
    ("⁴⁰Ca B/A",            8.55),
    ("⁵⁶Fe B/A",            8.79),  # max stable
    ("⁵⁸Ni B/A",            8.73),
    ("⁹⁰Zr B/A",            8.71),
    ("¹⁰⁸Pd B/A",           8.55),
    ("²⁰⁸Pb B/A",           7.87),
    ("²³⁸U B/A",            7.57),
    # Ratios
    ("⁵⁶Fe/⁴He B/A",        8.79/7.07),
    ("¹⁶O/¹²C B/A",         7.98/7.68),
    ("²⁰⁸Pb/⁵⁶Fe B/A",      7.87/8.79),
]

# === Magic numbers structure ===
MAGIC_NUMBERS_RATIOS = [
    ("magic_2/magic_8",     2/8),
    ("magic_8/magic_20",    8/20),
    ("magic_20/magic_28",   20/28),
    ("magic_28/magic_50",   28/50),
    ("magic_50/magic_82",   50/82),
    ("magic_82/magic_126",  82/126),
]

# === ππ phase shifts (Roy equations, Garcia-Martin 2011) ===
PHASE_SHIFTS = [
    ("δ₀⁰(√s=600MeV)_ππ [deg]",  43.0),  # approx
    ("δ₀⁰(800MeV)_ππ",            72.0),
    ("δ₀⁰(1000MeV)_ππ",           108.0),
    ("δ₁¹(770MeV)_ππ",            90.0),  # ρ resonance
    ("a₀⁰ (S-wave scattering length)", 0.220),  # m_π units
    ("a₂⁰",                       -0.0444),
    ("a₁¹ (P-wave)",              0.0382),
    # Roy bridges
    ("a₀⁰ - a₂⁰",                 0.220 - (-0.0444)),
    ("a₀⁰ / (-a₂⁰)",              0.220/0.0444),
]

# === Effective ranges / scattering lengths ===
SCATTERING_LENGTHS = [
    ("a_NN(¹S₀) [fm]",     -23.748),
    ("a_NN(³S₁) [fm]",     5.4194),
    ("r_NN(¹S₀)",          2.75),
    ("r_NN(³S₁)",          1.749),
    ("a_NN(³S₁)/|a_NN(¹S₀)|", 5.4194/23.748),
]

# Combine all
for name, val in NUCLEAR_BINDING + MAGIC_NUMBERS_RATIOS + PHASE_SHIFTS + SCATTERING_LENGTHS:
    PRE_REGISTERED.append((name, val))

print(f"\nTotal observables : {len(PRE_REGISTERED)}")

target_vals = np.array([abs(v) if v != 0 else 1e-10 for _, v in PRE_REGISTERED])
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

print(f"\nResults BBN+NUCLEAR ({len(PRE_REGISTERED)} obs):\n")
print(f"{'Tol':>10} {'Real':>6} {'μ±σ':>14} {'Z':>10}")
print("-"*55)
z_scores = {}
for i, tol in enumerate(tolerance_levels):
    real = real_hits[tol]
    rand_mean = boot_results[:, i].mean()
    rand_std = boot_results[:, i].std()
    z = (real - rand_mean) / max(rand_std, 0.01)
    sig = "✓✓" if z > 4 else "✓" if z > 3 else "🟡" if z > 2 else ""
    print(f"  <{tol*100:.4f}% {real:>6} {rand_mean:>6.1f}±{rand_std:>5.2f} {z:>+9.2f}σ {sig}")
    z_scores[tol] = {"real": int(real), "random_mean": float(rand_mean),
                     "random_std": float(rand_std), "z": float(z)}

print(f"\nTop 25 :")
sort_real = np.argsort(real_rel)
top_hits = []
for k in range(min(25, len(PRE_REGISTERED))):
    i = sort_real[k]
    name = PRE_REGISTERED[i][0]
    val = PRE_REGISTERED[i][1]
    cand_idx = sort_idx[real_indices[i]]
    cand_meta = candidates_list[cand_idx]
    cand_v = cand_meta[0]
    a, b, c, d, n, m, tw = cand_meta[1:]
    rel = real_rel[i] * 100
    formula = f"κ^{a}·(1-κ)^{b}·(1+κ)^{c}·π^{d}·({n}/{m})"
    print(f"  {name:>40} obs={val:.5f} pred={cand_v:.5f} ({rel:.4f}%) TW={tw} {formula}")
    top_hits.append({"name": name, "obs": float(val), "pred": float(cand_v),
                     "rel_pct": float(rel), "tw": float(tw), "formula": formula})

with open("/tmp/pysr_bbn_nuclear_results.json", "w") as f:
    json.dump({"domain": "bbn_nuclear", "n_obs": len(PRE_REGISTERED),
               "n_candidates": n_cand, "z_scores": z_scores, "top_hits": top_hits},
              f, indent=2)
print(f"\nElapsed : {time.time()-START:.1f}s | Saved /tmp/pysr_bbn_nuclear_results.json | DONE.")
