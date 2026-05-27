#!/usr/bin/env python3
"""PySR form factors : G_E^p, G_M^p, G_E^n, G_M^n, F_π(Q²) électromagnétiques.

Setup TW≤2 même candidate space.
"""
import math
import time
import json
import numpy as np
from scipy.spatial import cKDTree
from multiprocessing import Pool, cpu_count
from scipy.stats import norm

START = time.time()
print(f"START : {time.ctime()}\n" + "="*78 + f"\nPySR FORM FACTORS — hadronic Q² dependence\n" + "="*78)

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

# Form factor dipole parameterizations from Ye-Arrington 2017 + Jlab
# G_E^p(Q²) = (1 + Q²/M_V²)^{-2} avec M_V² = 0.71 GeV²
# At specific Q² values, normalized to G_E^p(0) = 1, G_M^p(0) = μ_p
M_V_SQ = 0.71  # GeV²

PRE_REGISTERED = []
# Dipole approximation at various Q² (GeV²)
Q2_values = [0.01, 0.05, 0.1, 0.2, 0.5, 1.0, 2.0, 5.0, 10.0]
for Q2 in Q2_values:
    G_dipole = (1 + Q2/M_V_SQ)**(-2)
    PRE_REGISTERED.append((f"G_E^p({Q2})_dipole", G_dipole))
    G_M_p = 2.79285 * G_dipole  # μ_p
    PRE_REGISTERED.append((f"G_M^p({Q2})/μ_p_dipole", G_dipole))  # G_M/μ_p ratio

# Pion form factor F_π(Q²)
# Monopole : F_π(Q²) = 1/(1 + Q²/m_ρ²)
M_RHO_SQ = 0.775**2  # GeV²
for Q2 in Q2_values:
    F_pi = 1/(1 + Q2/M_RHO_SQ)
    PRE_REGISTERED.append((f"F_π({Q2})", F_pi))

# Charge radii ratios PDG
PRE_REGISTERED.extend([
    ("r_p_E [fm]", 0.84087),
    ("r_p_M [fm]", 0.851),
    ("r_n_E²·(-1) [fm²]", 0.1161),
    ("r_K [fm]", 0.560),
    ("r_π [fm]", 0.659),
    ("r_p/r_π", 0.84087/0.659),
    ("r_p/r_K", 0.84087/0.560),
    ("r_K/r_π", 0.560/0.659),
    ("r_n²/r_p²", 0.1161/0.84087**2),
    ("r_p_E/r_p_M", 0.84087/0.851),
])

# DIS structure function ratios (proxy : F_2^p(x, Q²) at fixed x)
# F_2 typical values from CT18 / NNPDF (rounded)
F2_DATA = [
    ("F_2^p(x=0.1, Q²=10)", 0.435),
    ("F_2^p(x=0.3, Q²=10)", 0.286),
    ("F_2^p(x=0.5, Q²=10)", 0.118),
    ("F_2^p(x=0.7, Q²=10)", 0.026),
    ("F_2^n/F_2^p(x=0.1)", 0.880),
    ("F_2^n/F_2^p(x=0.5)", 0.580),
    ("F_2^p(x=0.1)/F_2^p(x=0.3)", 0.435/0.286),
    ("xg(x=0.1, Q²=10)", 1.65),
    ("xg(x=0.3, Q²=10)", 0.350),
]
PRE_REGISTERED.extend(F2_DATA)

# Cross sections (low-energy hadronic)
PRE_REGISTERED.extend([
    ("σ_ππ_total/σ_KK(1GeV)", 1.45),  # approx
    ("σ_pp_inelastic(13TeV)/σ_pp_total(13TeV)", 80/110),  # approx
    ("R(e+e- → hadrons / μμ) at √s=2GeV", 2.2),
    ("R(e+e- → hadrons / μμ) at √s=10GeV", 3.7),
])

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

print(f"\nResults FORM FACTORS ({len(PRE_REGISTERED)} obs) :\n")
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

print(f"\nTop 20 :")
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
    print(f"  {name:>40} obs={val:.4f} pred={cand_v:.4f} ({rel:.4f}%) TW={tw} {formula}")
    top_hits.append({"name": name, "obs": float(val), "pred": float(cand_v),
                     "rel_pct": float(rel), "tw": float(tw), "formula": formula})

with open("/tmp/pysr_form_factors_results.json", "w") as f:
    json.dump({"domain": "form_factors", "n_obs": len(PRE_REGISTERED),
               "n_candidates": n_cand, "z_scores": z_scores, "top_hits": top_hits},
              f, indent=2)
print(f"\nElapsed : {time.time()-START:.1f}s | Saved /tmp/pysr_form_factors_results.json | DONE.")
