#!/usr/bin/env python3
"""Isolate κ-containing patterns from pure-rational patterns.

Test : are κ-formulas (with explicit κ=1/6 or 1-κ=5/6) giving MORE matches than
pure-rational formulas of comparable complexity?

This separates "framework predictions" from "natural number coincidences".
"""
import numpy as np
import math
import random

kappa = 1/6
alpha = 5/6
pi_const = math.pi
e_const = math.e
sqrt2 = math.sqrt(2)

# Reload data
data = {
    "p": 938.272, "n": 939.565, "Lambda": 1115.683, "Sigma_p": 1189.37,
    "Sigma_0": 1192.642, "Sigma_m": 1197.449, "Xi_0": 1314.86, "Xi_m": 1321.71,
    "Omega": 1672.45, "Delta": 1232.0, "Sigma_star": 1383.7, "Xi_star": 1531.8,
    "Lambda_c": 2286.46, "Sigma_c": 2453.97, "Lambda_b": 5619.6,
    "pi_pm": 139.570, "pi_0": 134.977, "K_pm": 493.677, "K_0": 497.611,
    "K_star": 891.66, "eta": 547.862, "eta_prime": 957.78,
    "rho": 775.26, "omega": 782.65, "phi": 1019.461,
    "D_pm": 1869.66, "D_0": 1864.84, "D_s": 1968.35, "D_star": 2006.85,
    "B_pm": 5279.34, "B_0": 5279.65, "B_s": 5366.92,
    "J_psi": 3096.9, "psi_2S": 3686.097, "chi_c0": 3414.71,
    "Upsilon_1S": 9460.4, "Upsilon_2S": 10023.26,
    "e": 0.5110, "mu": 105.66, "tau": 1776.86,
    "m_u": 2.16, "m_d": 4.67, "m_s": 93.4, "m_c": 1270, "m_b": 4180, "m_t": 172570,
    "M_W": 80377, "M_Z": 91188, "M_H": 125250,
    "Lambda_QCD": 250, "f_pi": 92.4, "sigma_root": 440,
    "g_0pp": 1730, "g_2pp": 2400, "g_0mp": 2595,
}

pairs = []
keys = list(data.keys())
for i in range(len(keys)):
    for j in range(len(keys)):
        if i != j and data[keys[i]] > data[keys[j]]:
            ratio = data[keys[i]] / data[keys[j]]
            if 0.05 < ratio < 200:
                pairs.append((f"{keys[i]}/{keys[j]}", ratio))

print(f"Total ratios : {len(pairs)}")

# Build two SEPARATE candidate sets
# Set A: pure rational + π (no κ)
candidates_pure = []
for n_name, n_val in [("π", pi_const), ("e", e_const), ("√2", sqrt2),
                       ("π²", pi_const**2), ("2π", 2*pi_const),
                       ("π/2", pi_const/2), ("π/3", pi_const/3),
                       ("π/4", pi_const/4), ("π²/3", pi_const**2/3)]:
    candidates_pure.append((n_name, n_val))
for a in range(1, 13):
    for b in range(1, 13):
        if a == b: continue
        candidates_pure.append((f"{a}/{b}", a/b))
        if 0.2 < a/b < 20:
            candidates_pure.append((f"√({a}/{b})", math.sqrt(a/b)))

# Set B: κ-containing (explicit kappa=1/6 or 1-κ=5/6)
candidates_kappa = [
    ("κ", kappa),
    ("1-κ", alpha),
    ("1+κ", 1+kappa),
    ("κ·π", kappa*pi_const),
    ("(1-κ)·π", alpha*pi_const),
    ("(1-κ)·π/2", alpha*pi_const/2),
    ("(1+κ)·π/2", (1+kappa)*pi_const/2),
    ("π/(1-κ)", pi_const/alpha),
    ("π²/(1-κ)", pi_const**2/alpha),
    ("π²·κ", pi_const**2*kappa),
    ("1/(1-κ)", 1/alpha),
    ("κ/(1-κ)", kappa/alpha),  # = 1/5
    ("(1-κ)/κ", alpha/kappa),  # = 5
    ("(1+κ)/(1-κ)", (1+kappa)/alpha),
    ("(1-κ)²", alpha**2),
    ("1-κ²", 1-kappa**2),
    ("2(1-κ)/(1+κ)", 2*alpha/(1+kappa)),
    ("κ + π·κ²", kappa + pi_const*kappa**2),
    ("π/3·(1+κ)", pi_const/3*(1+kappa)),
    ("π/3·(1-κ)", pi_const/3*alpha),
    ("π²/(3(1-κ))", pi_const**2/(3*alpha)),
]

# Deduplicate
seen = set()
candidates_pure_d = []
for n, v in candidates_pure:
    k = round(v, 4)
    if k not in seen:
        seen.add(k)
        candidates_pure_d.append((n, v))
candidates_pure = candidates_pure_d

seen = set()
candidates_kappa_d = []
for n, v in candidates_kappa:
    k = round(v, 4)
    if k not in seen:
        seen.add(k)
        candidates_kappa_d.append((n, v))
candidates_kappa = candidates_kappa_d

print(f"Pure rational/π candidates : {len(candidates_pure)}")
print(f"κ-containing candidates : {len(candidates_kappa)}")

# Per-ratio : best PURE match and best KAPPA match
def best_match(val, candidates):
    best = (float('inf'), None, 0)
    for n, c in candidates:
        if c <= 0:
            continue
        diff = abs(val - c)/val * 100
        if diff < best[0]:
            best = (diff, n, c)
    return best

results_pure = []
results_kappa = []
for n, v in pairs:
    p_diff, p_name, p_val = best_match(v, candidates_pure)
    k_diff, k_name, k_val = best_match(v, candidates_kappa)
    results_pure.append((n, v, p_name, p_val, p_diff))
    results_kappa.append((n, v, k_name, k_val, k_diff))

# Stats
pure_tight = sum(1 for r in results_pure if r[4] < 1)
kappa_tight = sum(1 for r in results_kappa if r[4] < 1)
pure_med = sum(1 for r in results_pure if 1 <= r[4] < 3)
kappa_med = sum(1 for r in results_kappa if 1 <= r[4] < 3)

print(f"\n{'Pure rational + π':>25} : {pure_tight}/{len(pairs)} tight ({100*pure_tight/len(pairs):.1f}%)")
print(f"{'κ-containing':>25} : {kappa_tight}/{len(pairs)} tight ({100*kappa_tight/len(pairs):.1f}%)")

# Normalize by candidate count :
# Density = matches per candidate per ratio
pure_density = pure_tight / len(candidates_pure)
kappa_density = kappa_tight / len(candidates_kappa)
print(f"\nMatches per candidate :")
print(f"  Pure : {pure_density:.2f}")
print(f"  Kappa : {kappa_density:.2f}")
print(f"  Ratio kappa/pure : {kappa_density/max(0.01,pure_density):.2f}")

# When κ wins over pure : κ gives BETTER match than pure
kappa_wins = 0
pure_wins = 0
ties = 0
for i in range(len(pairs)):
    p = results_pure[i][4]
    k = results_kappa[i][4]
    if k < p - 0.01:
        kappa_wins += 1
    elif p < k - 0.01:
        pure_wins += 1
    else:
        ties += 1

print(f"\nHead-to-head : κ vs pure best-match per ratio :")
print(f"  κ wins (better than pure) : {kappa_wins} / {len(pairs)}")
print(f"  Pure wins : {pure_wins} / {len(pairs)}")
print(f"  Ties : {ties}")

# Top κ wins where pure doesn't have a tight match
print(f"\nκ provides tight match (<0.5%) where pure can't (>2%) :")
print(f"  These are STRUCTURAL κ-fingerprints :")
print(f"\n  {'Ratio':>20} {'Value':>10} {'Pure best':>20} {'%':>6} {'κ formula':>20} {'%':>6}")
print("-"*100)
struct_kappa = []
for i in range(len(pairs)):
    p_n, p_v = pairs[i]
    p_diff = results_pure[i][4]
    p_name = results_pure[i][2]
    k_diff = results_kappa[i][4]
    k_name = results_kappa[i][2]
    if k_diff < 0.5 and p_diff > 2:
        struct_kappa.append((p_n, p_v, p_name, p_diff, k_name, k_diff))

for n, v, pn, pd, kn, kd in sorted(struct_kappa, key=lambda x: x[5])[:15]:
    print(f"  {n:>20} {v:>10.5f} {pn:>20} {pd:>5.2f}% {kn:>20} {kd:>5.3f}%")

print(f"\nTotal structural κ-fingerprints : {len(struct_kappa)}")

# Random baseline for κ-only candidates
random.seed(42)
random_kappa_tight = 0
for _ in range(len(pairs)):
    rand_val = math.exp(random.uniform(math.log(0.05), math.log(200)))
    best = min(abs(rand_val - c)/rand_val*100 for _, c in candidates_kappa if c > 0)
    if best < 1:
        random_kappa_tight += 1

print(f"\n=== KAPPA-only Bonferroni ===")
print(f"Observed κ-tight : {kappa_tight} / {len(pairs)} ({100*kappa_tight/len(pairs):.1f}%)")
print(f"Random κ-tight : {random_kappa_tight} / {len(pairs)} ({100*random_kappa_tight/len(pairs):.1f}%)")
z = (kappa_tight - random_kappa_tight)/math.sqrt(max(1, random_kappa_tight))
print(f"Z-score κ-tight : {z:.2f}σ")

# Format simplicity weight
# A formula is "simpler" if it has fewer operators
def complexity(formula_name):
    # Count operators + constants
    ops = sum(formula_name.count(c) for c in "+-*/√^()")
    return ops

# Print structural κ-fingerprints clean
print(f"\n=== TOP STRUCTURAL FINDINGS (κ-only, tight, pure-inaccessible) ===")
print(f"\nThese are the cleanest framework predictions :")
for n, v, pn, pd, kn, kd in sorted(struct_kappa, key=lambda x: x[5])[:10]:
    print(f"  {n:>20} = {v:.5f} ≈ {kn} ({kd:.3f}%)")
    print(f"    Pure fallback : {pn} ({pd:.2f}%)")

print("\nDONE.")
