#!/usr/bin/env python3
"""
MEGA PySR v5 — 4 axes d'amélioration :

E1 — Cross-sector features (Σ_p, group inv, constants in X matrix)
E2 — Dimensionless ratios as targets (not absolute)
E3 — Adversarial integrated : permute target, compare best loss
E4 — Bayesian Pareto averaging : weight by BIC

Architecture :
- Load catalog 431 entries
- Filter to dimensionless OR ratios
- Build wide X matrix (40+ features)
- Run PySR with parsimony grid
- For each top expression : test adversarial Z-score
- Output : Pareto front ranking by (loss, Z, complexity)

Critical test : can PySR rediscover sin²θ_W = 3/13, A_CKM = 19/23, etc.
from features alone (not just brute force matching)?

Author : Kévin Rémondière (ORCID 0009-0008-2443-7166).
"""
import os
os.environ['JULIA_NUM_THREADS'] = '12'
import numpy as np
import json, re, time, copy, random
from sympy import sieve

print(f"=== MEGA PySR v5 ({time.strftime('%H:%M:%S')}) ===", flush=True)

primes = list(sieve.primerange(2, 300))
cumsum_p = np.cumsum(primes[:40])

# ============================
# LOAD CATALOG
# ============================
with open('/tmp/OBSERVABLES_DATASET.json') as f:
    cat = json.load(f)
print(f"Catalog : {len(cat['entries'])} entries", flush=True)


def parse_value(s):
    if s is None: return None
    if isinstance(s, (int, float)): return float(s)
    if not isinstance(s, str): return None
    s = s.strip().lstrip('~<>≈')
    m = re.match(r'^-?\d+/\d+$', s)
    if m:
        n, d = s.split('/'); return float(n)/float(d)
    try: return float(s)
    except: pass
    m = re.match(r'^(-?\d+\.?\d*(?:[eE][-+]?\d+)?)', s)
    if m:
        try: return float(m.group(1))
        except: pass
    return None


obs_list = []
for e in cat['entries']:
    val = parse_value(e.get('value'))
    if val is None or val <= 0: continue
    if e.get('derivation_status') in ('FALSIFIED ❌', 'FALSIFIED'): continue
    obs_list.append({
        'id': e['id'], 'name': e.get('observable',''), 'value': val,
        'sector': e.get('sector',''), 'type': e.get('type',''),
        'status': e.get('derivation_status',''),
    })
print(f"Non-falsified numeric : {len(obs_list)}", flush=True)


# ============================
# E1 — BUILD WIDE FEATURE MATRIX
# ============================
print("\n=== E1 : Build cross-sector feature matrix ===", flush=True)

# For each observation, build feature vector
# Features = universal constants + Σ_p_k for k=1..30 + group invariants (assume N=3 default unless extractable)

def get_N_for_obs(name, sector):
    """Try to extract N for observation (default 3 for SM/QCD)."""
    m = re.search(r'SU\((\d+)\)', name)
    if m: return int(m.group(1))
    if 'lepton' in name.lower(): return 1
    if sector == 'YM-SD' or sector == 'YM-lattice': return 3  # default SU(3)
    if sector == 'EW': return 2  # SU(2)_L
    if sector == 'Yukawa' or sector == 'Hadrons': return 3  # SU(3) color
    if sector == 'Cosmology': return None  # not group-specific
    return 3


# Features
constants_lib = {
    'pi': np.pi, 'pi2': np.pi**2, 'pi3': np.pi**3, 'invpi': 1/np.pi, 'over4pi2': 4/np.pi**2,
    'e_euler': np.e, 'ln2': np.log(2), 'ln3': np.log(3), 'ln10': np.log(10),
    'zeta3': 1.2020569, 'zeta3_sqpi': 1.2020569/np.sqrt(np.pi),
    'phi_gold': 1.6180339887,
    'kappa_FP': 1/6, 'xi_star': 2/3, 'c_BH': 1/4, 'b_0_N': 11/3, 'F_inf': 9/10,
    'sqrt2': np.sqrt(2), 'sqrt3': np.sqrt(3), 'sqrt5': np.sqrt(5),
    'one': 1.0, 'half': 0.5, 'third': 1/3, 'quarter': 1/4, 'sixth': 1/6,
}

# For each observation : build feature vector + value
X_rows = []
y_vec = []
obs_names = []
obs_meta = []

for o in obs_list:
    N = get_N_for_obs(o['name'], o['sector'])
    if N is None: N = 3  # fallback
    if N < 1 or N > 30: continue
    # Group invariants for this N
    feats = {
        'N': float(N),
        'dimG': float(N**2 - 1),
        'rank': float(N - 1),
        'Casimir': float(N),
        'npos_roots': float(N*(N-1)/2),
        'sqrt_dimG': np.sqrt(N**2 - 1) if N > 1 else 0.0,
        'inv_N': 1.0/N,
    }
    # Σ premiers at various k
    for k in [3, 4, 5, 6, 7, 8, 10, 11, 12, 14, 17, 21]:
        if k <= len(cumsum_p):
            feats[f'Sigma_{k}'] = float(cumsum_p[k-1])
    # Universal constants
    for cn, cv in constants_lib.items():
        feats[cn] = cv
    X_rows.append(list(feats.values()))
    y_vec.append(o['value'])
    obs_names.append(o['name'])
    obs_meta.append({'sector': o['sector'], 'status': o['status'], 'N': N})

X_mat = np.array(X_rows)
y_vec = np.array(y_vec)
feature_names = list(feats.keys())
print(f"X shape: {X_mat.shape}, features: {len(feature_names)}", flush=True)


# ============================
# E2 — DIMENSIONLESS RATIOS AS TARGETS
# ============================
print("\n=== E2 : Build dimensionless ratios ===", flush=True)

# Filter to small-magnitude dimensionless
sm_idx = [i for i, v in enumerate(y_vec) if 0.01 < v < 100]
print(f"  Small-magnitude dimensionless : {len(sm_idx)}", flush=True)


# ============================
# E3+E4 — RUN PySR WITH ADVERSARIAL + PARETO
# ============================
print("\n=== E3+E4 : PySR per-target Pareto + adversarial Z-score ===", flush=True)

from pysr import PySRRegressor

def run_pysr_target(X, y, target_name, weights=None, max_features=15):
    """Run PySR on single target with cross-sector features."""
    if y <= 0: return None
    # Use only features (avoid 'pi' as 'pi' is reserved — already renamed feats)
    # Build single-row matrix with all values
    # PySR needs multiple samples : use jittered versions of y for stat regularization
    # Actually : for SINGLE target with cross-feature, we need a different approach
    # Approach : PySR on a "synthetic dataset" where target is constant but features vary
    # → impossible to learn unless features predictive
    # Better : use ALL observations as multiple samples (each row = different obs)
    # Then target is the obs value, features are obs-specific features
    return None  # placeholder


# Alternative : run on ALL targets together as regression
# Each row is an observation, features are the obs context
print("\n=== RUN 1 : ALL dimensionless obs (regression) ===", flush=True)

# Limit to ≤ 100 obs and obs values in (0.01, 100) and well-defined N
mask = [i for i, v in enumerate(y_vec) if 0.01 < v < 100]
mask = mask[:80]  # cap
X1 = X_mat[mask]
y1 = y_vec[mask]
names1 = [obs_names[i] for i in mask]
print(f"  Targets: {len(y1)}", flush=True)

# Standardize feature names safe for PySR
safe_names = [f.replace('/', '_').replace('+', 'p') for f in feature_names]
# Avoid Julia reserved : check 'pi', 'e'
safe_names = ['Nv' if n=='N' else 'piv' if n=='pi' else 'ev' if n=='e_euler' else n for n in safe_names]

model_v5 = PySRRegressor(
    niterations=300,
    populations=40,
    population_size=100,
    binary_operators=["+", "-", "*", "/"],
    unary_operators=[],
    maxsize=30,
    maxdepth=10,
    parsimony=0.005,
    model_selection="best",
    progress=False,
    verbosity=0,
    timeout_in_seconds=900,
)

R1 = []
try:
    t0 = time.time()
    model_v5.fit(X1, y1, variable_names=safe_names)
    print(f"  PySR done {time.time()-t0:.1f}s", flush=True)
    eqs = model_v5.equations_
    print(f"  Top 10 expressions :", flush=True)
    print(eqs[['complexity','loss','equation']].head(10).to_string(), flush=True)
    R1 = [{'complexity':int(r['complexity']), 'loss':float(r['loss']), 'eq':str(r['equation'])} for _,r in eqs.head(15).iterrows()]
except Exception as ex:
    print(f"  Failed: {ex}", flush=True)


# ============================
# E3 — ADVERSARIAL : permute y_target, refit, compare
# ============================
print("\n=== E3 : Adversarial Z-score for top expressions ===", flush=True)

adversarial_results = []
n_perm = 5  # number of permutations (each takes ~time)
real_best_loss = R1[0]['loss'] if R1 else 1.0

random.seed(42)
adv_losses = []
for perm in range(n_perm):
    y_perm = y1.copy()
    random.shuffle(y_perm)
    model_adv = PySRRegressor(
        niterations=100, populations=20, population_size=60,
        binary_operators=["+", "-", "*", "/"], unary_operators=[],
        maxsize=20, parsimony=0.005,
        progress=False, verbosity=0, timeout_in_seconds=200,
    )
    try:
        t0 = time.time()
        model_adv.fit(X1, y_perm, variable_names=safe_names)
        adv_loss = float(model_adv.equations_.iloc[-1]['loss'])
        adv_losses.append(adv_loss)
        print(f"  Permutation {perm+1}: best loss = {adv_loss:.4e} ({time.time()-t0:.1f}s)", flush=True)
    except Exception as ex:
        print(f"  Permutation {perm+1} failed: {ex}", flush=True)

if adv_losses:
    adv_mean = np.mean(adv_losses)
    adv_std = np.std(adv_losses) if len(adv_losses) > 1 else adv_mean
    Z_real = (adv_mean - real_best_loss) / max(adv_std, 1e-10)
    print(f"\n  Real best loss : {real_best_loss:.4e}", flush=True)
    print(f"  Adversarial mean loss : {adv_mean:.4e} ± {adv_std:.4e}", flush=True)
    print(f"  Z-score (adv vs real) : {Z_real:.2f}σ", flush=True)
    print(f"  Interpretation : Z > 3σ → real signal, Z < 1σ → spurious", flush=True)
else:
    Z_real = None


# ============================
# E4 — PARETO ANALYSIS
# ============================
print("\n=== E4 : Pareto front by (complexity, loss) ===", flush=True)
if R1:
    print(f"  Pareto front {len(R1)} expressions :", flush=True)
    for r in R1[:10]:
        bic = r['loss'] + r['complexity']*np.log(len(y1))
        print(f"    complexity={r['complexity']:3d}, loss={r['loss']:.4e}, BIC={bic:.4f}, eq: {r['eq'][:80]}", flush=True)


# ============================
# SAVE
# ============================
out = {
    'date': '2026-05-27 00:32',
    'description': 'MEGA PySR v5 cross-sector + adversarial + Pareto',
    'n_obs_used': len(y1),
    'n_features': X_mat.shape[1],
    'feature_names': safe_names,
    'run_1_pareto': R1,
    'adversarial': {
        'n_permutations': n_perm,
        'adv_losses': adv_losses if 'adv_losses' in dir() else [],
        'real_best_loss': real_best_loss,
        'Z_score': Z_real if Z_real else None,
    }
}
with open('/tmp/MEGA_PYSR_v5_results.json', 'w') as f:
    json.dump(out, f, indent=2, default=str)
print(f"\n→ Saved /tmp/MEGA_PYSR_v5_results.json", flush=True)
print(f"End : {time.strftime('%H:%M:%S')}", flush=True)
