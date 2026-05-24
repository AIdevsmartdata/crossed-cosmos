#!/usr/bin/env python3
"""PySR run #1 : running couplings α_s(Q), α_em(Q), sin²θ_W(Q).

Test si le framework κ=1/6 prédit les VALEURS DYNAMIQUES (en fonction de Q),
pas juste les ratios statiques.

Setup : TW≤2 filter κ^a·(1-κ)^b·(1+κ)^c·π^d·n/m, 1000 bootstrap Bonferroni.
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
print(f"PySR RUNNING COUPLINGS — κ=1/6 framework on dynamical Q-running")
print("=" * 78)

KAPPA = 1/6
PI = math.pi
N_CPUS = cpu_count()
N_BOOTSTRAP = 1000
TW_MAX = 2

# Build candidate space (same recipe as mega-run)
a_set = np.array([-3, -2, -1, -0.5, 0, 0.5, 1, 1.5, 2, 3])
b_set = np.array([-2, -1, -0.5, 0, 0.5, 1, 2])
c_set = np.array([-1, -0.5, 0, 0.5, 1])
d_set = np.array([-1, -0.5, 0, 0.5, 1])
n_set = np.arange(1, 21)
m_set = np.arange(1, 21)

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
print(f"Built {n_cand} candidates in {elapsed:.1f}s")

log_candidates = np.log(candidates_arr)
sort_idx = np.argsort(log_candidates)
log_candidates_sorted = log_candidates[sort_idx]
tree = cKDTree(log_candidates_sorted.reshape(-1, 1))

# Pre-registered : running coupling values from PDG running tables
# Each tuple : (name, value_observed, error)
PRE_REGISTERED = [
    # === α_s(Q) PDG running, MS-bar, N_f=5 except low Q ===
    ("α_s(1 GeV)",        0.400),  # PDG 2024 N_f=3
    ("α_s(M_τ=1.777)",    0.333),  # PDG 2024
    ("α_s(2 GeV)",        0.302),  # PDG running
    ("α_s(M_b=4.18)",     0.222),  # PDG b-quark mass
    ("α_s(5 GeV)",        0.213),
    ("α_s(10 GeV)",       0.180),
    ("α_s(20 GeV)",       0.155),
    ("α_s(M_W=80.38)",    0.121),  # PDG
    ("α_s(M_Z=91.19)",    0.1179), # PDG world avg
    ("α_s(M_H=125.25)",   0.113),
    ("α_s(200 GeV)",      0.106),
    ("α_s(M_t=172.6)",    0.108),  # top scale
    # === α_em(Q) running ===
    ("α_em(0)",           1/137.036),       # Sommerfeld
    ("α_em(M_τ)",         1/133.5),
    ("α_em(M_Z)",         1/127.952),       # PDG MS-bar
    # === sin²θ_W(Q) running ===
    ("sin²θ_W(0)",        0.23866),         # low-Q
    ("sin²θ_W(M_Z)_MS",   0.23121),         # PDG MS-bar
    ("sin²θ_W^eff",       0.23151),         # leptonic effective
    ("sin²θ_W(M_W)_OS",   1 - (80.377/91.188)**2),  # on-shell
    # === Ratios across scales ===
    ("α_s(M_Z)/α_s(1GeV)",       0.1179/0.4),
    ("α_s(M_Z)/α_s(M_τ)",        0.1179/0.333),
    ("α_em(M_Z)/α_em(0)",        137.036/127.952),
    ("α_em(M_Z)/α_s(M_Z)",       (1/127.952)/0.1179),
    ("1/α_s(M_Z) - 1/α_s(1GeV)", 1/0.1179 - 1/0.4),  # log running coefficient
    ("ln(α_s(M_τ)/α_s(M_Z))",    math.log(0.333/0.1179)),  # RG coefficient
    ("ln(M_Z/Λ_QCD)",            math.log(91.19/0.240)),  # = 5.94 ≈ 2π·0.946
]

target_vals = np.array([v for _, v in PRE_REGISTERED])
target_logs = np.log(np.abs(target_vals))

real_distances, real_indices = tree.query(target_logs.reshape(-1, 1), k=1)
real_rel = np.exp(real_distances.flatten()) - 1

tolerance_levels = [1e-5, 1e-4, 1e-3, 5e-3, 0.01, 0.02, 0.05]

real_hits = {tol: int(np.sum(real_rel < tol)) for tol in tolerance_levels}

val_min, val_max = np.abs(target_vals).min(), np.abs(target_vals).max()
log_min, log_max = math.log(val_min), math.log(val_max)

def bootstrap_one(seed):
    np.random.seed(seed)
    rand_logs = np.random.uniform(log_min, log_max, len(target_vals))
    distances, _ = tree.query(rand_logs.reshape(-1, 1), k=1)
    rel = np.exp(distances.flatten()) - 1
    return tuple(int(np.sum(rel < t)) for t in tolerance_levels)

print(f"\nRunning {N_BOOTSTRAP} bootstrap trials on {N_CPUS} CPUs...")
t3 = time.time()
with Pool(N_CPUS) as pool:
    boot_results = pool.map(bootstrap_one, range(2026, 2026 + N_BOOTSTRAP))
boot_results = np.array(boot_results)
print(f"Bootstrap done in {time.time()-t3:.1f}s")

print(f"\n{'='*78}")
print(f"RESULTS — RUNNING COUPLINGS ({len(PRE_REGISTERED)} observables)")
print(f"{'='*78}\n")
print(f"{'Tol':>10} {'Real':>6} {'Random μ±σ':>18} {'Z':>10} {'p-value':>15}")
print("-"*70)

z_scores = {}
for i, tol in enumerate(tolerance_levels):
    real = real_hits[tol]
    rand_mean = boot_results[:, i].mean()
    rand_std = boot_results[:, i].std()
    z = (real - rand_mean) / max(rand_std, 0.01)
    p_value = 1 - norm.cdf(z)
    sig = "✓✓" if z > 4 else "✓" if z > 3 else "🟡" if z > 2 else ""
    print(f"  <{tol*100:.4f}% {real:>6} {rand_mean:>8.1f}±{rand_std:>6.2f} {z:>+9.2f}σ {p_value:>15.3e} {sig}")
    z_scores[tol] = {"real": int(real), "random_mean": float(rand_mean),
                     "random_std": float(rand_std), "z": float(z), "p": float(p_value)}

print(f"\nTop matches sorted by rel diff :")
sort_real = np.argsort(real_rel)
top_hits = []
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
    top_hits.append({"name": name, "obs": float(val), "pred": float(cand_v),
                     "rel_pct": float(rel), "tw": float(tw), "formula": formula})

output = {
    "domain": "running_couplings",
    "n_obs": len(PRE_REGISTERED),
    "n_candidates": n_cand,
    "z_scores": z_scores,
    "top_hits": top_hits,
}
with open("/tmp/pysr_running_couplings_results.json", "w") as f:
    json.dump(output, f, indent=2)
print(f"\nElapsed : {time.time()-START:.1f}s")
print(f"Saved : /tmp/pysr_running_couplings_results.json")
print(f"DONE.")
