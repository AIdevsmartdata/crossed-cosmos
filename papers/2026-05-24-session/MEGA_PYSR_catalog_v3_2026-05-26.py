#!/usr/bin/env python3
"""
MEGA PySR catalog v3 — fix sector names + proper Runs 2 & 3.

Run 2 : Group-theory invariants (37 entries)
   → Test if PySR recovers dim G = N²-1, Casimir, rank from N
Run 3 : Σ_p_metaselector (17 entries)
   → For each observable, find best k, test Z-score adversarial

Author : Kévin Rémondière (ORCID 0009-0008-2443-7166).
"""
import os
os.environ['JULIA_NUM_THREADS'] = '12'
import numpy as np
import json, re, time
from sympy import sieve

print(f"=== MEGA PySR catalog v3 ({time.strftime('%H:%M:%S')}) ===", flush=True)

primes = list(sieve.primerange(2, 250))
cumsum_p = np.cumsum(primes[:30])

with open('/tmp/OBSERVABLES_DATASET.json') as f:
    cat = json.load(f)
print(f"Catalog loaded : {len(cat['entries'])} entries", flush=True)


def parse_value(s):
    if s is None: return None
    if isinstance(s, (int, float)): return float(s)
    if not isinstance(s, str): return None
    s = s.strip().lstrip('~<>≈')
    m = re.match(r'^-?\d+/\d+$', s)
    if m:
        n, d = s.split('/')
        return float(n)/float(d)
    try: return float(s)
    except: pass
    m = re.match(r'^(-?\d+\.?\d*(?:[eE][-+]?\d+)?)', s)
    if m:
        try: return float(m.group(1))
        except: pass
    return None


def parse_N(entry):
    s = str(entry.get('N_dof_or_group', ''))
    m = re.search(r'SU\((\d+)\)', s)
    if m: return int(m.group(1))
    return None


# Extract
obs_list = []
for e in cat['entries']:
    val = parse_value(e.get('value'))
    if val is None: continue
    obs_list.append({
        'id': e['id'], 'name': e.get('observable',''), 'value': val,
        'sector': e.get('sector',''), 'type': e.get('type',''),
        'status': e.get('derivation_status',''),
        'N': parse_N(e), 'N_dof_str': str(e.get('N_dof_or_group',''))
    })

by_sector = {}
for o in obs_list:
    by_sector.setdefault(o['sector'], []).append(o)

print(f"\nSectors with data ({len(by_sector)}):", flush=True)
for s, lst in sorted(by_sector.items(), key=lambda x: -len(x[1])):
    print(f"  {s:25s}: {len(lst)} values", flush=True)


# ============================
# RUN 2 (FIXED) : Group-theory invariants
# ============================
print("\n" + "="*70, flush=True)
print("RUN 2 (FIXED) : Group-theory invariants — recover dim G, etc.", flush=True)
print("="*70, flush=True)

gt = by_sector.get('Group-theory', [])
print(f"  {len(gt)} entries in 'Group-theory'", flush=True)
for o in gt[:10]:
    print(f"    [{o['id']:3d}] {o['name'][:40]:40s} = {o['value']:8.4f}  (N_dof: {o['N_dof_str'][:30]})", flush=True)

# Try to extract structured (name, N, value)
# Look for "dim SU(N)" pattern
import re
dim_data = []  # (N, dim_G value)
casimir_data = []
rank_data = []
n_roots_data = []
for o in gt:
    n = o['name']
    val = o['value']
    # dim SU(N) or dim(SU(N))
    m = re.search(r'(?:dim\s*SU|dim\s*\(\s*SU)\((\d+)\)', n)
    if m:
        Nv = int(m.group(1))
        dim_data.append((Nv, val))
        continue
    # Casimir SU(N)
    m = re.search(r'(?:C_?2|Casimir).*SU\((\d+)\)', n, re.IGNORECASE)
    if m:
        Nv = int(m.group(1))
        casimir_data.append((Nv, val))
        continue
    # rank SU(N)
    m = re.search(r'rank.*SU\((\d+)\)', n, re.IGNORECASE)
    if m:
        Nv = int(m.group(1))
        rank_data.append((Nv, val))
        continue
    # # roots
    m = re.search(r'roots.*SU\((\d+)\)', n, re.IGNORECASE)
    if m:
        Nv = int(m.group(1))
        n_roots_data.append((Nv, val))
        continue

print(f"\n  Structured extracted:", flush=True)
print(f"    dim G : {dim_data}", flush=True)
print(f"    Casimir : {casimir_data}", flush=True)
print(f"    rank : {rank_data}", flush=True)
print(f"    # roots : {n_roots_data}", flush=True)

R2_results = {}
# Run PySR on dim G if enough points
if len(dim_data) >= 4:
    from pysr import PySRRegressor
    Ns = np.array([d[0] for d in dim_data], dtype=float)
    dims = np.array([d[1] for d in dim_data])
    print(f"\n  RUN 2a : Fit dim G({Ns.tolist()}) = {dims.tolist()}", flush=True)
    X2a = Ns.reshape(-1,1)
    model2a = PySRRegressor(
        niterations=100, populations=20, population_size=60,
        binary_operators=["+", "-", "*", "/"], unary_operators=[],
        maxsize=10, parsimony=0.003, model_selection="best",
        progress=False, verbosity=0, timeout_in_seconds=300,
    )
    try:
        t0 = time.time()
        model2a.fit(X2a, dims, variable_names=['Nv'])
        print(f"    Done {time.time()-t0:.1f}s", flush=True)
        eqs = model2a.equations_
        print(eqs[['complexity','loss','equation']].head(5).to_string(), flush=True)
        # Expect : N²-1
        R2_results['dim_G'] = [{'complexity':int(r['complexity']),'loss':float(r['loss']),'eq':str(r['equation'])} for _,r in eqs.head(5).iterrows()]
    except Exception as ex:
        print(f"    Failed: {ex}", flush=True)
        R2_results['dim_G'] = []
else:
    print(f"  dim G : only {len(dim_data)} points, skip", flush=True)


# ============================
# RUN 3 (FIXED) : Σ_p_metaselector verification
# ============================
print("\n" + "="*70, flush=True)
print("RUN 3 (FIXED) : Σ_premiers metaselector verification + Z-score", flush=True)
print("="*70, flush=True)

sig = by_sector.get('Σ_p_metaselector', [])
print(f"  {len(sig)} entries in 'Σ_p_metaselector'", flush=True)

# For each entry, look at ln(value) and find best k
R3_results = []
print(f"\n  Per-observable best k match:", flush=True)
print(f"  {'observable':50s} {'value':>10s} {'|ln(val)|':>10s} {'best_k':>7s} {'Σ_k':>5s} {'rel%':>8s} {'k_meta':>8s}", flush=True)
for o in sig:
    if o['value'] is None or o['value'] <= 0: continue
    abs_val = abs(o['value'])
    log_val = abs(np.log(abs_val)) if abs_val > 0 else 0
    # Find best k for ln(val) ≈ Σ_k
    best_k = None
    best_rel = 1.0
    best_sigma = 0
    for k in range(1, 30):
        s = cumsum_p[k-1]
        # Test both abs_val and log_val as target
        for target, scale in [(abs_val, 'val'), (log_val, 'log')]:
            if s > 0:
                rel = abs(target - s) / max(target, s)
                if rel < best_rel:
                    best_rel = rel
                    best_k = k
                    best_sigma = int(s)
    # Catalog conjectured k from N_dof_str
    k_meta = None
    m = re.search(r'k\s*=\s*(\d+)', o['N_dof_str']) or re.search(r'dim\s*[A-Za-z_0-9]+\s*=\s*(\d+)', o['N_dof_str'])
    if m: k_meta = int(m.group(1))

    match_flag = "★" if best_rel < 0.005 else ""
    print(f"  {o['name'][:50]:50s} {abs_val:10.4f} {log_val:10.4f} {best_k or 0:>7d} {best_sigma:>5d} {best_rel*100:>7.2f}% {str(k_meta or '?'):>8s} {match_flag}", flush=True)
    R3_results.append({
        'name': o['name'], 'value': abs_val, 'log_val': log_val,
        'best_k': best_k, 'sigma_k': best_sigma, 'rel': best_rel, 'k_meta': k_meta
    })

# Adversarial : randomize and see if same level of matches
print(f"\n  ADVERSARIAL : 100 random observables in similar range:", flush=True)
import random
random.seed(42)
n_excellent_real = sum(1 for r in R3_results if r['rel'] < 0.005)
n_excellent_rand = 0
n_trials = 100
for trial in range(n_trials):
    # Random val in [10^-200, 10^200] range
    log_val_rand = abs(random.uniform(-200, 200))
    best_rel = 1.0
    for k in range(1, 30):
        s = cumsum_p[k-1]
        if s > 0:
            rel = abs(log_val_rand - s) / max(log_val_rand, s)
            best_rel = min(best_rel, rel)
    if best_rel < 0.005:
        n_excellent_rand += 1

import math
sigma_rand = math.sqrt(max(n_excellent_rand, 1))
z_real = (n_excellent_real - n_excellent_rand) / sigma_rand if sigma_rand > 0 else 0
print(f"  Real obs <0.5%: {n_excellent_real}/{len(R3_results)}", flush=True)
print(f"  Random <0.5%:   {n_excellent_rand}/{n_trials}", flush=True)
print(f"  Z = (real - rand)/√rand = {z_real:.2f}σ", flush=True)


# ============================
# RUN 5 (NEW) : Cross-sector dimensionless < 10 — strict template match (no offset)
# ============================
print("\n" + "="*70, flush=True)
print("RUN 5 (NEW) : Strict template matches (no random rationals)", flush=True)
print("="*70, flush=True)

# Only check against EXACT-known templates : κ_FP=1/6, κ_inf, etc.
templates = {
    'κ_FP=1/6': 1/6,
    'ξ★=2/3': 2/3,
    'c_BH=1/4': 1/4,
    'F∞=9/10': 9/10,
    'd_s=3': 3.0,
    'd_s=7/3': 7/3,
    'b_0/N=11/3': 11/3,
    'ζ(3)/√π': 1.2020569/np.sqrt(np.pi),
    'cos²θ_W=10/13': 10/13,
    'sin²θ_W=3/13': 3/13,
    'A_CKM=19/23': 19/23,
}

print(f"\n  Strict template hits (rel < 0.001) :", flush=True)
strict_hits = []
for o in obs_list:
    if o['value'] is None or o['value'] <= 0: continue
    if o['status'] in ('FALSIFIED ❌', 'FALSIFIED'): continue
    for tname, tval in templates.items():
        if tval > 0:
            rel = abs(o['value'] - tval) / max(abs(o['value']), abs(tval))
            if rel < 0.001:
                strict_hits.append({'obs': o['name'], 'sector': o['sector'], 'value': o['value'], 'template': tname, 'tval': tval, 'rel': rel})
                break
strict_hits.sort(key=lambda x: x['rel'])
for h in strict_hits[:30]:
    print(f"  [{h['sector'][:12]:12s}] {h['obs'][:35]:35s} = {h['value']:8.4e} → {h['template']:20s} (rel={h['rel']*100:.4f}%)", flush=True)


# ============================
# SAVE
# ============================
out = {
    'date': '2026-05-26 23:45',
    'catalog_entries_used': len(obs_list),
    'run_2_group_theory': R2_results,
    'run_3_sigma_premiers': R3_results,
    'run_3_adversarial': {'n_excellent_real': n_excellent_real, 'n_excellent_random_100': n_excellent_rand, 'Z': z_real},
    'run_5_strict_template_hits': strict_hits,
}
with open('/tmp/MEGA_PYSR_catalog_v3.json', 'w') as f:
    json.dump(out, f, indent=2, default=str)
print(f"\n→ Saved /tmp/MEGA_PYSR_catalog_v3.json", flush=True)
print(f"End : {time.strftime('%H:%M:%S')}", flush=True)
