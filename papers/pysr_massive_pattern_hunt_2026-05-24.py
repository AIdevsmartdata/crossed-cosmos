#!/usr/bin/env python3
"""Massive PySR pattern hunt on PDG hadronic + cosmological dimensionless ratios.

Features : κ, π, e, √2, √3, integers 1-12, log, exp.
Targets : 50+ ratios.
Statistical Bonferroni assessment via random control.
Cross-validation : fit on subset, predict rest.
"""
import numpy as np
import math
import random
import itertools

kappa = 1/6
alpha = 5/6  # 1-κ
phi_plus = 3
D = 4
N_c = 3
alpha_EM = 1/137.036
sin2_theta_W = 0.2312
pi_const = math.pi
e_const = math.e
sqrt2 = math.sqrt(2)
sqrt3 = math.sqrt(3)
sqrt5 = math.sqrt(5)

# ==============================================================
# PDG 2024 data (MeV unless noted) — 50+ ratios
# ==============================================================
data = {
    # Baryons
    "p": 938.272, "n": 939.565,
    "Lambda": 1115.683, "Sigma_p": 1189.37, "Sigma_0": 1192.642, "Sigma_m": 1197.449,
    "Xi_0": 1314.86, "Xi_m": 1321.71, "Omega": 1672.45,
    "Delta": 1232.0, "Sigma_star": 1383.7, "Xi_star": 1531.8,
    "Lambda_c": 2286.46, "Sigma_c": 2453.97,
    "Lambda_b": 5619.6,
    # Mesons
    "pi_pm": 139.570, "pi_0": 134.977,
    "K_pm": 493.677, "K_0": 497.611, "K_star": 891.66,
    "eta": 547.862, "eta_prime": 957.78,
    "rho": 775.26, "omega": 782.65,
    "phi": 1019.461,
    "D_pm": 1869.66, "D_0": 1864.84, "D_s": 1968.35, "D_star": 2006.85,
    "B_pm": 5279.34, "B_0": 5279.65, "B_s": 5366.92,
    "J_psi": 3096.9, "psi_2S": 3686.097, "chi_c0": 3414.71,
    "Upsilon_1S": 9460.4, "Upsilon_2S": 10023.26,
    # Leptons
    "e": 0.5110, "mu": 105.66, "tau": 1776.86,
    # Quark masses (MS-bar at scale)
    "m_u": 2.16, "m_d": 4.67, "m_s": 93.4,
    "m_c": 1270, "m_b": 4180, "m_t": 172570,
    # Higgs/EW
    "M_W": 80377, "M_Z": 91188, "M_H": 125250,
    # QCD scales
    "Lambda_QCD": 250, "f_pi": 92.4, "sigma_root": 440,
    # Predicted glueballs (Athenodorou-Teper 2021)
    "g_0pp": 1730, "g_2pp": 2400, "g_0mp": 2595,
}

# Build pairwise mass ratios for all combinations
pairs = []
keys = list(data.keys())
for i in range(len(keys)):
    for j in range(len(keys)):
        if i != j and data[keys[i]] > data[keys[j]]:
            ratio = data[keys[i]] / data[keys[j]]
            pairs.append((f"{keys[i]}/{keys[j]}", ratio))

# Filter to dimensionless ratios in range [0.1, 100] (most physical)
pairs_filtered = [(n, v) for n, v in pairs if 0.05 < v < 200]
print(f"Total ratios to test : {len(pairs_filtered)}")

# ==============================================================
# Build candidate formulas library
# ==============================================================
candidates = []

# Constants
for n_name, n_val in [("π", pi_const), ("e", e_const), ("√2", sqrt2), ("√3", sqrt3),
                       ("κ", kappa), ("1-κ", alpha), ("π²", pi_const**2),
                       ("2π", 2*pi_const), ("π/2", pi_const/2), ("π/3", pi_const/3),
                       ("π/4", pi_const/4), ("π/6", pi_const/6)]:
    candidates.append((n_name, n_val))

# Integer combinations
for a in range(1, 13):
    for b in range(1, 13):
        if a == b:
            continue
        candidates.append((f"{a}/{b}", a/b))
        # Half integers
        if a/b > 0.5 and a/b < 20:
            candidates.append((f"√({a}/{b})", math.sqrt(a/b)))

# κ-formulas
candidates.extend([
    ("κ·π", kappa*pi_const),
    ("κ·π²", kappa*pi_const**2),
    ("(1-κ)·π", alpha*pi_const),
    ("(1-κ)·π/2", alpha*pi_const/2),
    ("π/(1-κ)", pi_const/alpha),
    ("π²/(1-κ)", pi_const**2/alpha),
    ("π²·κ", pi_const**2*kappa),
    ("1/(1-κ)", 1/alpha),
    ("(1+κ)/(1-κ)", (1+kappa)/alpha),
    ("κ + π·κ²", kappa + pi_const*kappa**2),
    ("(1-κ)²", alpha**2),
    ("1-κ²", 1-kappa**2),
    ("2(1-κ)/(1+κ)", 2*alpha/(1+kappa)),
    ("π/3·(1+κ)", pi_const/3*(1+kappa)),
    ("π/3·(1-κ)", pi_const/3*alpha),
    ("π²/(3(1-κ))", pi_const**2/(3*alpha)),
    ("e·κ", e_const*kappa),
    ("e/(1-κ)", e_const/alpha),
    ("π·κ²", pi_const*kappa**2),
    ("π²·κ²", pi_const**2*kappa**2),
    ("κ/(1-κ)", kappa/alpha),  # = 1/5
    ("(1-κ)/κ", alpha/kappa),  # = 5
])

# Drop near-duplicates (numerical)
seen_vals = set()
unique_candidates = []
for n, v in candidates:
    key = round(v, 4)
    if key not in seen_vals:
        seen_vals.add(key)
        unique_candidates.append((n, v))
candidates = unique_candidates
print(f"Total candidate formulas (deduped) : {len(candidates)}")

# ==============================================================
# Per-ratio search for best candidate
# ==============================================================
print("\n" + "="*78)
print("Phase 1 : per-ratio best candidate (tight match < 1%)")
print("="*78)

tight_matches = []  # < 1%
medium_matches = []  # 1-3%
all_results = []

for ratio_name, ratio_val in pairs_filtered:
    best_diff = float('inf')
    best_name = None
    best_pred = 0
    for c_name, c_val in candidates:
        if c_val <= 0:
            continue
        diff = abs(ratio_val - c_val)
        rel = abs(diff/ratio_val*100)
        if rel < best_diff:
            best_diff = rel
            best_name = c_name
            best_pred = c_val
    all_results.append((ratio_name, ratio_val, best_name, best_pred, best_diff))
    if best_diff < 1:
        tight_matches.append((ratio_name, ratio_val, best_name, best_pred, best_diff))
    elif best_diff < 3:
        medium_matches.append((ratio_name, ratio_val, best_name, best_pred, best_diff))

print(f"\nTight matches < 1% : {len(tight_matches)} / {len(pairs_filtered)}")
print(f"{'Ratio':>20} {'Value':>10} {'Best formula':>20} {'Pred':>10} {'Rel %':>8}")
print("-"*75)
for n, v, fn, fp, d in sorted(tight_matches, key=lambda x: x[4])[:40]:
    print(f"{n:>20} {v:>10.5f} {fn:>20} {fp:>10.5f} {d:>7.3f}%")

print(f"\nMedium matches 1-3% : {len(medium_matches)}")
print(f"{'Ratio':>20} {'Value':>10} {'Best formula':>20} {'Pred':>10} {'Rel %':>8}")
print("-"*75)
for n, v, fn, fp, d in sorted(medium_matches, key=lambda x: x[4])[:25]:
    print(f"{n:>20} {v:>10.5f} {fn:>20} {fp:>10.5f} {d:>7.3f}%")

# ==============================================================
# Bonferroni baseline : random ratios
# ==============================================================
print("\n" + "="*78)
print("Phase 2 : Bonferroni baseline (random control)")
print("="*78)

random.seed(42)
n_random = len(pairs_filtered)
# Generate random ratios in same range as observed
obs_min = min(v for _, v in pairs_filtered)
obs_max = max(v for _, v in pairs_filtered)
print(f"\nObserved ratio range : [{obs_min:.3f}, {obs_max:.3f}]")
print(f"Generating {n_random} random log-uniform ratios in same range :")

random_tight = 0
random_medium = 0
log_min = math.log(obs_min)
log_max = math.log(obs_max)
for _ in range(n_random):
    rand_val = math.exp(random.uniform(log_min, log_max))
    best_diff = float('inf')
    for c_name, c_val in candidates:
        if c_val <= 0:
            continue
        rel = abs(rand_val - c_val)/rand_val*100
        if rel < best_diff:
            best_diff = rel
    if best_diff < 1:
        random_tight += 1
    elif best_diff < 3:
        random_medium += 1

print(f"\nRandom control (Bonferroni baseline) :")
print(f"  Random tight matches < 1% : {random_tight} / {n_random} ({100*random_tight/n_random:.1f}%)")
print(f"  Random medium matches 1-3% : {random_medium} / {n_random} ({100*random_medium/n_random:.1f}%)")
print(f"\nObserved (real data) :")
print(f"  Real tight < 1% : {len(tight_matches)} / {len(pairs_filtered)} ({100*len(tight_matches)/len(pairs_filtered):.1f}%)")
print(f"  Real medium 1-3% : {len(medium_matches)} / {len(pairs_filtered)} ({100*len(medium_matches)/len(pairs_filtered):.1f}%)")
print(f"\nZ-score tight matches : {(len(tight_matches)-random_tight)/math.sqrt(max(1,random_tight)):.2f}")
print(f"Z-score medium matches : {(len(medium_matches)-random_medium)/math.sqrt(max(1,random_medium)):.2f}")

# ==============================================================
# Phase 3 : group by formula family
# ==============================================================
print("\n" + "="*78)
print("Phase 3 : Formula family analysis")
print("="*78)

# Count how many ratios match each formula at <1%
formula_counts = {}
for n, v, fn, fp, d in tight_matches:
    formula_counts[fn] = formula_counts.get(fn, []) + [(n, v, d)]

print(f"\nFormulas matching multiple ratios at <1% :")
for f, ratios in sorted(formula_counts.items(), key=lambda x: -len(x[1])):
    if len(ratios) >= 2:
        print(f"\n  Formula '{f}' matches {len(ratios)} ratios :")
        for rn, rv, rd in ratios:
            print(f"    {rn:>20} = {rv:>10.5f}  ({rd:.3f}% diff)")

# ==============================================================
# Phase 4 : log-decomposition (powers of 2, 3, π)
# ==============================================================
print("\n" + "="*78)
print("Phase 4 : log-decomposition log(r) = a·log(2) + b·log(3) + c·log(π)")
print("="*78)

log2 = math.log(2)
log3 = math.log(3)
logpi = math.log(pi_const)

# For each ratio, find (a, b, c) integers minimizing |a·log2 + b·log3 + c·logπ - log(r)|
def find_int_combo(target, max_int=4):
    best = (0, 0, 0, 0)
    best_diff = float('inf')
    for a in range(-max_int, max_int+1):
        for b in range(-max_int, max_int+1):
            for c in range(-max_int, max_int+1):
                pred = a*log2 + b*log3 + c*logpi
                if abs(a)+abs(b)+abs(c) > 6:
                    continue
                diff = abs(pred - target)
                if diff < best_diff:
                    best_diff = diff
                    best = (a, b, c, pred)
    return best, best_diff

log_tight = []
for n, v in pairs_filtered:
    if v <= 0:
        continue
    lv = math.log(v)
    (a, b, c, pred), diff = find_int_combo(lv)
    rel = math.exp(diff) - 1  # log diff → relative
    pct = abs(rel)*100
    if pct < 1:
        formula = f"2^{a}·3^{b}·π^{c}"
        log_tight.append((n, v, formula, math.exp(pred), pct))

print(f"\nLog-decomposition matches < 1% : {len(log_tight)}")
for n, v, f, p, d in sorted(log_tight, key=lambda x: x[4])[:30]:
    print(f"  {n:>20} {v:>10.5f} ≈ {f:>15} = {p:>10.5f}  ({d:.3f}%)")

# ==============================================================
# Phase 5 : cross-validation
# ==============================================================
print("\n" + "="*78)
print("Phase 5 : Cross-validation tight matches")
print("="*78)

# Split tight matches into 'fit' and 'blind'
# Take light hadrons as fit, heavy as blind
light_keys = {"p", "n", "Lambda", "Sigma_p", "Xi_0", "Omega", "Delta",
              "pi_pm", "K_pm", "eta", "rho", "omega", "phi", "K_star",
              "e", "mu", "tau", "f_pi", "Lambda_QCD"}
heavy_keys = {"J_psi", "psi_2S", "chi_c0", "Upsilon_1S", "Upsilon_2S",
              "D_pm", "D_0", "D_s", "D_star", "B_pm", "B_0", "B_s",
              "Lambda_b", "Lambda_c", "Sigma_c", "M_W", "M_Z", "M_H",
              "m_c", "m_b", "m_t"}

def is_light_ratio(name):
    parts = name.split("/")
    return all(p in light_keys for p in parts)

def is_heavy_ratio(name):
    parts = name.split("/")
    return any(p in heavy_keys for p in parts)

light_tight = [r for r in tight_matches if is_light_ratio(r[0])]
heavy_tight = [r for r in tight_matches if is_heavy_ratio(r[0])]

print(f"\nLight tight matches : {len(light_tight)}")
print(f"Heavy tight matches : {len(heavy_tight)}")

# Identify formula vocabulary used by LIGHT
light_formulas = set()
for r in light_tight:
    light_formulas.add(r[2])
print(f"\nFormula vocabulary from LIGHT ({len(light_formulas)} formulas) :")
for f in sorted(light_formulas):
    print(f"  {f}")

# Test : how many heavy ratios match ONLY light-formulas at <2% ?
heavy_using_light_voc = 0
heavy_total = sum(1 for r in pairs_filtered if is_heavy_ratio(r[0]))
for ratio_name, ratio_val in pairs_filtered:
    if not is_heavy_ratio(ratio_name):
        continue
    best_in_light = float('inf')
    for f_name in light_formulas:
        # Find candidate value for f_name
        for c_n, c_v in candidates:
            if c_n == f_name:
                rel = abs(ratio_val - c_v)/ratio_val*100
                if rel < best_in_light:
                    best_in_light = rel
                break
    if best_in_light < 2:
        heavy_using_light_voc += 1

print(f"\nBlind test : heavy ratios matching ANY light-vocabulary formula at <2% :")
print(f"  {heavy_using_light_voc} / {heavy_total} ({100*heavy_using_light_voc/max(1,heavy_total):.1f}%)")

# ==============================================================
# Final summary
# ==============================================================
print("\n" + "="*78)
print("FINAL SUMMARY")
print("="*78)
print(f"""
Total ratios tested        : {len(pairs_filtered)}
Tight matches (<1%)        : {len(tight_matches)} ({100*len(tight_matches)/len(pairs_filtered):.1f}%)
Medium matches (1-3%)      : {len(medium_matches)} ({100*len(medium_matches)/len(pairs_filtered):.1f}%)
Random baseline tight      : {random_tight} ({100*random_tight/n_random:.1f}%)
Random baseline medium     : {random_medium} ({100*random_medium/n_random:.1f}%)
Z-score tight              : {(len(tight_matches)-random_tight)/math.sqrt(max(1,random_tight)):.2f}σ
Z-score medium             : {(len(medium_matches)-random_medium)/math.sqrt(max(1,random_medium)):.2f}σ

Log-decomp tight (<1%)     : {len(log_tight)}

Cross-val heavy/light voc  : {heavy_using_light_voc}/{heavy_total} ({100*heavy_using_light_voc/max(1,heavy_total):.0f}%)

Formula families repeated  : {sum(1 for k, v in formula_counts.items() if len(v) >= 2)}
""")

# Top patterns to report
print("Top NEW or REPEATED patterns to investigate :")
print("-"*60)
for f, ratios in sorted(formula_counts.items(), key=lambda x: -len(x[1]))[:10]:
    if len(ratios) >= 2:
        print(f"  '{f}' matches {len(ratios)} ratios :")
        for rn, rv, rd in ratios:
            print(f"    {rn:>20} = {rv:>10.5f}  ({rd:.3f}%)")

print("\nDONE.")
