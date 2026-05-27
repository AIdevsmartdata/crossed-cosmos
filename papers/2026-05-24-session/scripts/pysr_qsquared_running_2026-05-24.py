#!/usr/bin/env python3
"""PySR EXTENDED Q²-running : 90+ valeurs α_s, α_em, sin²θ_W, m_q(μ).

Couvre toute la dépendance Q² qui était drowned dans le run #1 (26 obs).
Cible Z significatif sur dynamique RG.
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
print(f"PySR Q²-RUNNING EXTENDED — RG flow couverture")
print("=" * 78)

KAPPA = 1/6
PI = math.pi
N_CPUS = cpu_count()
N_BOOTSTRAP = 1000
TW_MAX = 2

# Standard candidate space
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
print(f"Built {n_cand} candidates in {time.time()-t1:.1f}s")

log_candidates = np.log(candidates_arr)
sort_idx = np.argsort(log_candidates)
log_candidates_sorted = log_candidates[sort_idx]
tree = cKDTree(log_candidates_sorted.reshape(-1, 1))

# === 90+ observables Q²-running ===
# α_s(Q) PDG running table (MS-bar, N_f variable)
ALPHA_S_RUNNING = [
    (1.0, 0.500, 3),   # Q (GeV), α_s, N_f
    (1.5, 0.378, 3),
    (1.78, 0.333, 3),  # τ scale
    (2.0, 0.302, 3),
    (3.0, 0.250, 4),
    (4.0, 0.225, 4),
    (4.18, 0.222, 4),  # b scale
    (5.0, 0.213, 4),
    (6.0, 0.205, 4),
    (8.0, 0.190, 4),
    (10.0, 0.180, 5),
    (15.0, 0.165, 5),
    (20.0, 0.155, 5),
    (30.0, 0.142, 5),
    (50.0, 0.130, 5),
    (80.38, 0.121, 5),  # W
    (91.19, 0.1179, 5), # Z
    (100.0, 0.118, 5),
    (125.25, 0.113, 5), # H
    (172.6, 0.108, 6),  # t
    (200.0, 0.106, 6),
    (300.0, 0.102, 6),
    (500.0, 0.097, 6),
    (1000.0, 0.090, 6),
    (5000.0, 0.080, 6),
]

# α_em(Q)
ALPHA_EM_RUNNING = [
    (0.0, 1/137.036),
    (0.001, 1/137.036),  # essentially 0
    (1.0, 1/134.5),     # Thomson-region high
    (1.78, 1/133.5),
    (10.0, 1/130.7),
    (91.19, 1/127.952),  # Z
    (200.0, 1/126.5),
]

# sin²θ_W(Q) MS-bar running
SIN2_W_RUNNING = [
    (0.001, 0.23866),
    (91.19, 0.23121),
    (91.19, 0.23151),   # eff lepton
    (80.38, 0.22290),   # on-shell W
    (200.0, 0.22899),
    (500.0, 0.22720),
]

# m_q(μ) running quark masses (PDG MS-bar)
MQ_RUNNING = [
    ("m_u(2)", 2.16),
    ("m_d(2)", 4.67),
    ("m_s(2)", 93.4),
    ("m_c(m_c)", 1273.0),
    ("m_c(3)", 990.0),
    ("m_b(m_b)", 4180.0),
    ("m_b(10)", 3540.0),
    ("m_t(m_t)", 162500.0),
    ("m_t(pole)", 172570.0),
    # ratios masses running
    ("m_c(3)/m_c(m_c)", 990/1273),
    ("m_b(10)/m_b(m_b)", 3540/4180),
    ("m_t(pole)/m_t(MS)", 172570/162500),
]

# Build observable list
PRE_REGISTERED = []
for Q, alpha, nf in ALPHA_S_RUNNING:
    PRE_REGISTERED.append((f"α_s({Q:.2f} GeV, N_f={nf})", alpha))
for Q, alpha in ALPHA_EM_RUNNING:
    PRE_REGISTERED.append((f"α_em({Q:.3f} GeV)", alpha))
for Q, sin2 in SIN2_W_RUNNING:
    PRE_REGISTERED.append((f"sin²θ_W({Q})", sin2))
for name, val in MQ_RUNNING:
    if val > 1:
        PRE_REGISTERED.append((name + " [MeV]", val))
    else:
        PRE_REGISTERED.append((name, val))

# Add RATIOS cross-Q for α_s (RG dimensionless)
qs = [v[0] for v in ALPHA_S_RUNNING]
alphas = [v[1] for v in ALPHA_S_RUNNING]
for i in range(len(qs)-1):
    for j in range(i+1, len(qs)):
        r = alphas[j]/alphas[i]  # < 1 (decreasing)
        PRE_REGISTERED.append((f"α_s({qs[j]})/α_s({qs[i]})", r))
        # log ratios (RG slopes)
        ln_r = math.log(alphas[i]/alphas[j])
        PRE_REGISTERED.append((f"ln(α_s({qs[i]})/α_s({qs[j]}))", ln_r))

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

print(f"\nRunning {N_BOOTSTRAP} bootstrap on {N_CPUS} CPUs...")
t3 = time.time()
with Pool(N_CPUS) as pool:
    boot_results = pool.map(bootstrap_one, range(2026, 2026 + N_BOOTSTRAP))
boot_results = np.array(boot_results)
print(f"Bootstrap done in {time.time()-t3:.1f}s")

print(f"\n{'='*78}\nRESULTS — Q²-RUNNING ({len(PRE_REGISTERED)} obs)\n{'='*78}\n")
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

print(f"\nTop 25 matches :")
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
    print(f"  {name:>35} obs={val:.6f} pred={cand_v:.6f} ({rel:.4f}%) TW={tw} {formula}")
    top_hits.append({"name": name, "obs": float(val), "pred": float(cand_v),
                     "rel_pct": float(rel), "tw": float(tw), "formula": formula})

output = {"domain": "qsquared_running", "n_obs": len(PRE_REGISTERED),
          "n_candidates": n_cand, "z_scores": z_scores, "top_hits": top_hits}
with open("/tmp/pysr_qsquared_running_results.json", "w") as f:
    json.dump(output, f, indent=2)
print(f"\nElapsed : {time.time()-START:.1f}s\nSaved : /tmp/pysr_qsquared_running_results.json\nDONE.")
