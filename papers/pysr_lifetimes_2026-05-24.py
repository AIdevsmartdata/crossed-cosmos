#!/usr/bin/env python3
"""PySR run #2 : lifetimes τ (hadrons + leptons) — ratios uniquement.

Lifetimes absolus dimensionnels → on les transforme en RATIOS adimensionnels
τ_i/τ_j cross-particules + Γ_i/m_i (largeurs naturelles).
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
print(f"PySR LIFETIMES — κ=1/6 framework on τ ratios")
print("=" * 78)

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

# Lifetimes PDG 2024 in seconds (or upper/lower bound)
TAUS = {
    "μ":     2.1969811e-6,
    "τ":     2.903e-13,
    "n":     880.2,
    "π+":    2.6033e-8,
    "K+":    1.2380e-8,
    "K_S":   8.954e-11,
    "K_L":   5.116e-8,
    "D+":    1.040e-12,
    "D0":    4.103e-13,
    "Ds":    5.04e-13,
    "B+":    1.638e-12,
    "B0":    1.519e-12,
    "Bs":    1.520e-12,
    "Bc":    5.10e-13,
    "Λ":     2.617e-10,
    "Σ+":    8.018e-11,
    "Σ-":    1.479e-10,
    "Ξ0":    2.90e-10,
    "Ξ-":    1.639e-10,
    "Ω":     8.21e-11,
    "Λc":    2.026e-13,
    "Λb":    1.466e-12,
    "Ξb-":   1.572e-12,
}

# Build all ratios τ_i/τ_j (preserve > 1 only to avoid duplicates)
PRE_REGISTERED = []
particles = list(TAUS.keys())
for i, p_i in enumerate(particles):
    for p_j in particles[i+1:]:
        r = TAUS[p_i] / TAUS[p_j]
        if r < 1:
            r = 1/r
            PRE_REGISTERED.append((f"τ({p_j})/τ({p_i})", r))
        else:
            PRE_REGISTERED.append((f"τ({p_i})/τ({p_j})", r))

# Cap at 60 ratios (sample most varied logs)
PRE_REGISTERED.sort(key=lambda x: math.log10(x[1]))
if len(PRE_REGISTERED) > 60:
    step = len(PRE_REGISTERED) // 60
    PRE_REGISTERED = PRE_REGISTERED[::step][:60]

# Add absolute lifetimes in natural units τ/ℏ where ℏ = 6.58e-25 GeV·s → τ·m_p where m_p in GeV
# τ × m_p (in GeV·s ≈ ℏ units) gives dimensionless number
HBAR_GEV_S = 6.582e-25
for p, tau in TAUS.items():
    val = tau * (0.938272 / HBAR_GEV_S)  # τ × m_p / ℏ = τ in "units of ℏ/m_p"
    PRE_REGISTERED.append((f"τ({p})·m_p/ℏ", val))

print(f"\nTotal observables : {len(PRE_REGISTERED)}")

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
print(f"RESULTS — LIFETIMES ({len(PRE_REGISTERED)} observables)")
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

print(f"\nTop 20 matches :")
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
    print(f"  {name:>30} obs={val:.4e} pred={cand_v:.4e} ({rel:.4f}%) TW={tw} {formula}")
    top_hits.append({"name": name, "obs": float(val), "pred": float(cand_v),
                     "rel_pct": float(rel), "tw": float(tw), "formula": formula})

output = {
    "domain": "lifetimes",
    "n_obs": len(PRE_REGISTERED),
    "n_candidates": n_cand,
    "z_scores": z_scores,
    "top_hits": top_hits,
}
with open("/tmp/pysr_lifetimes_results.json", "w") as f:
    json.dump(output, f, indent=2)
print(f"\nElapsed : {time.time()-START:.1f}s")
print(f"Saved : /tmp/pysr_lifetimes_results.json")
print(f"DONE.")
