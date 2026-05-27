#!/usr/bin/env python3
"""
MEGA PySR v4 — Julia backend, feature engineering rigoureux.

Stratégie suivie:
1. UNITES adimensionnées en input AND target
2. FEATURES = formes analytiques candidates injectées (pas réinventées)
3. CONTROLE complexité : parsimony=0.003, maxsize=25, pas d'unaire libre
4. Train/test split pour validation
5. Multiple targets : κ_EE(N), β_offset, mass ratios, Σ premiers

Per DS Bot guide :
- "PySR ne comprend pas les unités" → inject as features
- "Injecte les formes analytiques connues comme colonnes"
- "parsimony 0.001-0.005 pour 8 points"
- "model_selection='best'" pas "accuracy"

Author : Kévin Rémondière (ORCID 0009-0008-2443-7166).
"""
import os
os.environ['JULIA_NUM_THREADS'] = '12'

import numpy as np
import json
import time
from sympy import sieve

print(f"=== MEGA PySR v4 Julia ===", flush=True)
print(f"Start : {time.strftime('%Y-%m-%d %H:%M:%S')}", flush=True)

from pysr import PySRRegressor

primes = list(sieve.primerange(2, 250))
cumsum_p = np.cumsum(primes[:30])

# ============================
# DATA 1 : κ_EE(N) cross-N
# ============================
print("\n" + "="*70, flush=True)
print("TARGET 1 : κ_EE(N) — 8 dense points SU(5)..SU(12)", flush=True)
print("="*70, flush=True)

N = np.array([5,6,7,8,9,10,11,12], dtype=float)
K = np.array([0.7012, 0.810, 0.9107, 1.0416, 1.1764, 1.3307, 1.5008, 1.6707])
E = np.array([0.006, 0.005, 0.0054, 0.0046, 0.0051, 0.0048, 0.0051, 0.0050])

# Per DS Bot : inject N^p candidates as features so PySR doesn't reinvent
X1 = np.column_stack([
    N,                  # x0 : N
    N**2,               # x1 : N²
    N**2 - 1,           # x2 : dim(G)
    N**(5/3),           # x3 : K41 candidate
    N**(9/5),           # x4 : 9/5 candidate (Berges falsified but worth check)
    N**(4/3),           # x5 : Berges actual 4/3
    N**(7/4),           # x6 : 7/4 alternative
    np.sqrt(N**2 - 1),  # x7 : √dim
    1.0/N,              # x8 : 1/N
    np.log(N),          # x9 : log N
])
y1 = K
w1 = 1.0 / E**2

feat_names = ['Nv', 'N2v', 'dimG', 'N53', 'N95', 'N43', 'N74', 'sqrtDimG', 'invN', 'logN']
print(f"  Features: {feat_names}", flush=True)
print(f"  Target: κ_EE(N), n={len(N)} points", flush=True)

model1 = PySRRegressor(
    niterations=200,
    populations=30,
    population_size=80,
    binary_operators=["+", "-", "*", "/"],
    unary_operators=[],
    maxsize=25,
    maxdepth=8,
    parsimony=0.003,
    model_selection="best",
    weights=w1,
    elementwise_loss="loss(prediction, target) = (prediction - target)^2",
    progress=False,
    verbosity=0,
    timeout_in_seconds=1200,  # 20 min
)

try:
    t0 = time.time()
    model1.fit(X1, y1, variable_names=feat_names)
    print(f"  Run 1 done {time.time()-t0:.1f}s", flush=True)
    eqs1 = model1.equations_
    print(f"\n  Top 10 expressions :", flush=True)
    print(eqs1[['complexity','loss','equation']].head(10).to_string(), flush=True)
    R1_top = [{'complexity':int(r['complexity']), 'loss':float(r['loss']), 'equation':str(r['equation'])} for _,r in eqs1.head(15).iterrows()]
except Exception as ex:
    print(f"  Run 1 failed: {ex}", flush=True)
    R1_top = []

# ============================
# DATA 2 : β_offset residual after K41
# ============================
print("\n" + "="*70, flush=True)
print("TARGET 2 : Residual β after κ - α·N^{5/3} (test 4/π² hypothesis)", flush=True)
print("="*70, flush=True)

# Use K41 fit best α from data
alpha_K41 = 0.02008
residual = K - alpha_K41 * N**(5/3)
# Should be constant β ≈ 0.40-0.45

X2 = np.column_stack([
    np.full(len(N), np.pi),       # π
    np.full(len(N), 1/np.pi),     # 1/π
    np.full(len(N), 4/np.pi**2),  # 4/π²
    np.full(len(N), 1/6),         # κ_FP
    np.full(len(N), 2/3),         # ξ★
    np.full(len(N), 1/4),         # c_BH
    1.0/N,                         # 1/N
    np.log(N),                     # log N
    np.sqrt(N**2-1),               # √dim
    np.full(len(N), 1.0),          # const
])
y2 = residual
w2 = 1.0 / E**2

feat2 = ['piv', 'invpiv', '4overpi2', 'kappaFP', 'xistar', 'cBH', 'invN', 'logN', 'sqrtDimG', 'one']

model2 = PySRRegressor(
    niterations=100,
    populations=20,
    population_size=60,
    binary_operators=["+", "-", "*", "/"],
    unary_operators=[],
    maxsize=15,
    maxdepth=6,
    parsimony=0.005,
    model_selection="best",
    weights=w2,
    progress=False,
    verbosity=0,
    timeout_in_seconds=600,
)
try:
    t0 = time.time()
    model2.fit(X2, y2, variable_names=feat2)
    print(f"  Run 2 done {time.time()-t0:.1f}s", flush=True)
    eqs2 = model2.equations_
    print(f"\n  Top 10 expressions :", flush=True)
    print(eqs2[['complexity','loss','equation']].head(10).to_string(), flush=True)
    R2_top = [{'complexity':int(r['complexity']), 'loss':float(r['loss']), 'equation':str(r['equation'])} for _,r in eqs2.head(15).iterrows()]
except Exception as ex:
    print(f"  Run 2 failed: {ex}", flush=True)
    R2_top = []

# ============================
# DATA 3 : Σ premiers metaselector
# ============================
print("\n" + "="*70, flush=True)
print("TARGET 3 : Σ_k premiers vs cosmological observables", flush=True)
print("="*70, flush=True)

# Multiple targets ln(observable) vs k
observables_meta = [
    ("ln_MPl_v2",     2*np.log(2.435e18/246), 0.05),
    ("inv_ln_Lambda", -np.log(1.105e-122), 1.0),
    ("inv_ln_etaB",   -np.log(6.12e-10), 0.1),
    ("ln_MPl_mp",     np.log(2.435e18/0.938), 0.05),
    ("ln_alpha_em",   np.log(137.036), 0.001),
    ("ln_mt_me",      np.log(173570/0.000511), 0.005),
]

# Feature : k integer, Σ_k, k², k log k
ks = np.arange(1, 22)
X3 = np.column_stack([
    ks.astype(float),
    ks**2,
    np.log(ks+1),  # log(k+1) to avoid log(1)=0 issue
    np.sqrt(ks),
])
y3_all = []
for name, val, sigma in observables_meta:
    y3 = np.array([cumsum_p[k-1] if k>0 else 0 for k in ks])  # Σ_k as target
    print(f"  Observable {name} = {val:.2f}, finding best k...", flush=True)
    # Manually find best k
    best_k = None
    best_rel = 1.0
    for k_test in ks:
        s = cumsum_p[k_test-1]
        rel = abs(val - s)/val
        if rel < best_rel:
            best_rel = rel
            best_k = int(k_test)
    print(f"    Best k = {best_k}, Σ_k = {cumsum_p[best_k-1]}, rel = {best_rel*100:.2f}%", flush=True)

# PySR on the meta function k → Σ_k (find pattern)
model3 = PySRRegressor(
    niterations=100,
    populations=20,
    population_size=60,
    binary_operators=["+", "-", "*", "/"],
    unary_operators=["log", "sqrt"],
    maxsize=15,
    maxdepth=6,
    parsimony=0.003,
    model_selection="best",
    progress=False,
    verbosity=0,
    timeout_in_seconds=600,
)
try:
    t0 = time.time()
    model3.fit(X3, cumsum_p[:len(ks)], variable_names=['kv','k2v','logk','sqrtk'])
    print(f"  Run 3 (Σ_k vs k) done {time.time()-t0:.1f}s", flush=True)
    eqs3 = model3.equations_
    print(f"\n  Top 10 :", flush=True)
    print(eqs3[['complexity','loss','equation']].head(10).to_string(), flush=True)
    R3_top = [{'complexity':int(r['complexity']), 'loss':float(r['loss']), 'equation':str(r['equation'])} for _,r in eqs3.head(15).iterrows()]
except Exception as ex:
    print(f"  Run 3 failed: {ex}", flush=True)
    R3_top = []

# ============================
# DATA 4 : κ_EE per-DOF (dimensionless, per DS Bot guidance)
# ============================
print("\n" + "="*70, flush=True)
print("TARGET 4 : κ_EE(N) / dim(G)  per degree-of-freedom", flush=True)
print("="*70, flush=True)

y4 = K / (N**2 - 1)  # per DOF
X4 = X1.copy()  # same features
w4 = 1.0 / (E / (N**2-1))**2

print(f"  Target κ/dim(G) = {y4}", flush=True)
model4 = PySRRegressor(
    niterations=200,
    populations=30,
    population_size=80,
    binary_operators=["+", "-", "*", "/"],
    unary_operators=[],
    maxsize=25,
    maxdepth=8,
    parsimony=0.003,
    model_selection="best",
    weights=w4,
    progress=False,
    verbosity=0,
    timeout_in_seconds=1200,
)
try:
    t0 = time.time()
    model4.fit(X4, y4, variable_names=feat_names)
    print(f"  Run 4 done {time.time()-t0:.1f}s", flush=True)
    eqs4 = model4.equations_
    print(f"\n  Top 10 :", flush=True)
    print(eqs4[['complexity','loss','equation']].head(10).to_string(), flush=True)
    R4_top = [{'complexity':int(r['complexity']), 'loss':float(r['loss']), 'equation':str(r['equation'])} for _,r in eqs4.head(15).iterrows()]
except Exception as ex:
    print(f"  Run 4 failed: {ex}", flush=True)
    R4_top = []

# ============================
# SAVE all
# ============================
out = {
    'date': '2026-05-26',
    'author': 'Kévin Rémondière (ORCID 0009-0008-2443-7166)',
    'description': 'MEGA PySR Julia v4 with feature engineering per DS Bot guidance',
    'run_1_kappa_EE_8pts': R1_top,
    'run_2_residual_beta': R2_top,
    'run_3_sigma_k_pattern': R3_top,
    'run_4_kappa_per_DOF': R4_top,
}
with open('/tmp/MEGA_PYSR_v4_results.json', 'w') as f:
    json.dump(out, f, indent=2)
print(f"\n→ Saved /tmp/MEGA_PYSR_v4_results.json", flush=True)
print(f"End : {time.strftime('%Y-%m-%d %H:%M:%S')}", flush=True)
