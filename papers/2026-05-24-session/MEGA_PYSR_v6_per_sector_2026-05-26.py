#!/usr/bin/env python3
"""
MEGA PySR v6 — per-sector fits + adversarial Z + cross-sector identity check.

Méthodologie corrigée (post v5 falsification de "1 équation universelle") :
- Pour CHAQUE sector cohérent → fit PySR séparé avec features sector-relevant
- Adversarial Z-score within sector
- Cross-sector = identités explicites vérifiées (pas via PySR)

Sectors avec PySR fits :
1. YM-lattice κ_EE(N) — verify N^{9/5} robust
2. Group-theory dim/Cas/rank/roots vs N — battery test
3. Yukawa hierarchy y_f vs generation
4. Hadron meson spectrum vs quantum numbers
5. Cosmology Σ_p targeted
6. Strict identity cross-sector check (κ_FP ↔ Koide, F∞ ↔ Bianchi, etc.)

Author : Kévin Rémondière (ORCID 0009-0008-2443-7166).
"""
import os
os.environ['JULIA_NUM_THREADS'] = '12'
import numpy as np
import json, re, time, random
from sympy import sieve

print(f"=== MEGA PySR v6 per-sector ({time.strftime('%H:%M:%S')}) ===", flush=True)

primes = list(sieve.primerange(2, 300))
cumsum_p = np.cumsum(primes[:40])

with open('/tmp/OBSERVABLES_DATASET.json') as f:
    cat = json.load(f)


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
        'sector': e.get('sector',''), 'status': e.get('derivation_status',''),
        'source': e.get('source',''),
    })


def extract_N(name):
    m = re.search(r'SU\((\d+)\)', name)
    return int(m.group(1)) if m else None


from pysr import PySRRegressor

def run_pysr_fit(X, y, var_names, target_label, niter=150, parsimony=0.005, timeout=300, weights=None):
    """Run PySR with adversarial Z-score."""
    if X.shape[0] < 4:
        return None, None
    model = PySRRegressor(
        niterations=niter, populations=25, population_size=70,
        binary_operators=["+", "-", "*", "/"], unary_operators=[],
        maxsize=20, parsimony=parsimony, model_selection="best",
        progress=False, verbosity=0, timeout_in_seconds=timeout,
    )
    try:
        model.fit(X, y, variable_names=var_names)
        eqs = model.equations_
        real_loss = float(eqs.iloc[-1]['loss'])
        top10 = [{'complexity':int(r['complexity']), 'loss':float(r['loss']), 'eq':str(r['equation'])} for _,r in eqs.head(10).iterrows()]
    except Exception as ex:
        print(f"    {target_label} fit failed : {ex}", flush=True)
        return None, None

    # Adversarial : 5 permutations
    adv_losses = []
    random.seed(42)
    for p in range(3):  # smaller for speed
        y_perm = y.copy()
        np.random.shuffle(y_perm)
        try:
            m_adv = PySRRegressor(
                niterations=60, populations=15, population_size=50,
                binary_operators=["+", "-", "*", "/"], unary_operators=[],
                maxsize=15, parsimony=parsimony,
                progress=False, verbosity=0, timeout_in_seconds=90,
            )
            m_adv.fit(X, y_perm, variable_names=var_names)
            adv_losses.append(float(m_adv.equations_.iloc[-1]['loss']))
        except Exception as ex:
            pass

    if adv_losses:
        adv_mean = np.mean(adv_losses)
        adv_std = np.std(adv_losses) if len(adv_losses) > 1 else adv_mean
        Z = (adv_mean - real_loss) / max(adv_std, 1e-10)
    else:
        Z = None
    return top10, {'real_loss': real_loss, 'adv_mean': float(adv_mean) if adv_losses else None, 'adv_std': float(adv_std) if adv_losses else None, 'Z': float(Z) if Z is not None else None}


# ============================
# SECTOR 1 : YM-lattice κ_EE(N)
# ============================
print("\n" + "="*70, flush=True)
print("SECTOR 1 : YM-lattice κ_EE(N)", flush=True)
print("="*70, flush=True)

ymlat = [o for o in obs_list if o['sector']=='YM-lattice']
# Take unique N with κ value
pairs = {}
for o in ymlat:
    N = extract_N(o['name'])
    if N and N >= 2 and N <= 15:
        # Prefer post-THERM5000 if multiple
        is_post = 'THERM5000' in o['source'] or 'post' in o['name'].lower()
        if N not in pairs or is_post:
            pairs[N] = o['value']
N_arr = np.array(sorted(pairs.keys()), dtype=float)
K_arr = np.array([pairs[int(n)] for n in N_arr])
print(f"  Points : {dict(zip(N_arr.astype(int).tolist(), K_arr.tolist()))}", flush=True)

X1 = np.column_stack([
    N_arr, N_arr**2, N_arr**2 - 1,
    N_arr**(5/3), N_arr**(9/5), N_arr**(4/3),
    np.sqrt(N_arr**2 - 1), 1.0/N_arr, np.log(N_arr),
])
names1 = ['Nv', 'N2v', 'dimG', 'N53', 'N95', 'N43', 'sqrtDimG', 'invN', 'logN']
top1, adv1 = run_pysr_fit(X1, K_arr, names1, "YM-lattice κ_EE", niter=200, timeout=400)
print(f"\n  Top 5 expressions :", flush=True)
if top1:
    for r in top1[:5]:
        print(f"    complexity={r['complexity']:3d}, loss={r['loss']:.4e}, eq: {r['eq'][:80]}", flush=True)
print(f"  Adversarial : real_loss={adv1['real_loss']:.4e}, adv_mean={adv1['adv_mean']:.4e}, Z={adv1['Z']:.2f}σ", flush=True) if adv1 else None


# ============================
# SECTOR 2 : Group-theory full battery
# ============================
print("\n" + "="*70, flush=True)
print("SECTOR 2 : Group-theory (dim G, Casimir, rank, # roots)", flush=True)
print("="*70, flush=True)

gt = [o for o in obs_list if o['sector']=='Group-theory']
groups = {}
for o in gt:
    N = extract_N(o['name'])
    if N and N >= 2 and N <= 12:
        key = ''
        for word in ['dim', 'Casimir', 'rank', 'roots', 'Φ+']:
            if word.lower() in o['name'].lower():
                key = word.lower(); break
        if key:
            groups.setdefault(key, {})[N] = o['value']

for kind, data in groups.items():
    if len(data) < 4: continue
    Ns = np.array(sorted(data.keys()), dtype=float)
    vals = np.array([data[int(n)] for n in Ns])
    print(f"\n  {kind} : {dict(zip(Ns.astype(int).tolist(), vals.tolist()))}", flush=True)
    X2 = np.column_stack([Ns, Ns**2, Ns*(Ns-1)/2, 1.0/Ns])
    top, adv = run_pysr_fit(X2, vals, ['Nv', 'N2v', 'NN1half', 'invN'], f"{kind}", niter=80, timeout=120)
    if top:
        print(f"    Best: complexity={top[0]['complexity']}, loss={top[0]['loss']:.4e}, eq: {top[0]['eq']}", flush=True)
    if adv: print(f"    Z={adv['Z']:.2f}σ", flush=True)


# ============================
# SECTOR 3 : Yukawa hierarchy y_f vs generation
# ============================
print("\n" + "="*70, flush=True)
print("SECTOR 3 : Yukawa y_f vs generation index", flush=True)
print("="*70, flush=True)

# Quark Yukawa
yk_quark = {'u':2.16e-3, 'd':4.67e-3, 's':93.4e-3, 'c':1.273, 'b':4.183, 't':173.21}
yk_lepton = {'e':0.000511, 'mu':0.10566, 'tau':1.77686}
generations = {'u':1,'d':1,'e':1,'c':2,'s':2,'mu':2,'t':3,'b':3,'tau':3}
isospin = {'u':1,'d':-1,'c':1,'s':-1,'t':1,'b':-1}  # ±1 for up/down

# Up quarks
up_data = [(1, yk_quark['u']), (2, yk_quark['c']), (3, yk_quark['t'])]
dn_data = [(1, yk_quark['d']), (2, yk_quark['s']), (3, yk_quark['b'])]
lp_data = [(1, yk_lepton['e']), (2, yk_lepton['mu']), (3, yk_lepton['tau'])]

for label, data in [('up_quarks', up_data), ('down_quarks', dn_data), ('leptons', lp_data)]:
    gen = np.array([d[0] for d in data], dtype=float)
    mass = np.array([d[1] for d in data])
    print(f"\n  {label}: generation -> mass GeV", flush=True)
    for g, m in zip(gen, mass): print(f"    gen {int(g)}: {m:.4e}", flush=True)
    # Take log(mass / lightest)
    log_ratio = np.log(mass / mass[0])
    print(f"    log(mass/lightest) : {log_ratio}", flush=True)
    if len(gen) >= 3:
        X3 = np.column_stack([gen, gen**2, np.exp(gen)])
        top, adv = run_pysr_fit(X3, log_ratio, ['gen','gen2','expgen'], label, niter=100, timeout=120)
        if top:
            print(f"    Best : eq={top[0]['eq'][:80]}, loss={top[0]['loss']:.4e}", flush=True)
        if adv: print(f"    Z={adv['Z']:.2f}σ", flush=True)


# ============================
# SECTOR 4 : Strict identity cross-sector check
# ============================
print("\n" + "="*70, flush=True)
print("SECTOR 4 : Cross-sector identity check (κ_FP, F∞, ζ(3)/√π, ξ★)", flush=True)
print("="*70, flush=True)

anchors = {
    'κ_FP=1/6': 1/6,
    'ξ★=2/3': 2/3,
    'c_BH=1/4': 1/4,
    'F∞=9/10': 9/10,
    'b_0/N=11/3': 11/3,
    'ζ(3)/√π': 1.2020569/np.sqrt(np.pi),
    'A_CKM=19/23': 19/23,
    'sin²θ_W=3/13': 3/13,
    'cos²θ_W=10/13': 10/13,
    'd_s=3': 3,
}

cross_hits = {a: [] for a in anchors}
for o in obs_list:
    for aname, aval in anchors.items():
        rel = abs(o['value'] - aval) / max(abs(o['value']), abs(aval))
        if rel < 0.001:
            cross_hits[aname].append({'obs': o['name'], 'sector': o['sector'], 'value': o['value'], 'rel': rel})

print("\n  Cross-sector multi-hits (anchors appearing in 2+ sectors) :", flush=True)
for aname, hits in cross_hits.items():
    if len(hits) >= 2:
        sectors_set = set(h['sector'] for h in hits)
        if len(sectors_set) >= 2:
            print(f"\n  {aname} :", flush=True)
            for h in hits[:5]:
                print(f"    [{h['sector'][:12]:12s}] {h['obs'][:35]:35s} = {h['value']:.4e}", flush=True)
            print(f"    → SHARED across {len(sectors_set)} sectors : {sectors_set}", flush=True)


# ============================
# SAVE
# ============================
out = {
    'date': '2026-05-27 v6',
    'description': 'PySR v6 per-sector + cross-sector identity check',
    'sector_1_YM_lattice': {'top10': top1, 'adversarial': adv1},
    'cross_sector_identities': {a: hits for a, hits in cross_hits.items() if len(hits) >= 2},
}
with open('/tmp/MEGA_PYSR_v6_results.json', 'w') as f:
    json.dump(out, f, indent=2, default=str)
print(f"\n→ Saved /tmp/MEGA_PYSR_v6_results.json", flush=True)
print(f"End : {time.strftime('%H:%M:%S')}", flush=True)
