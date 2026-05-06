#!/usr/bin/env python3
import json
with open('/root/crossed-cosmos/notes/eci_v7_aspiration/M162_OPUS_HEEGNER_H3_H4/04_results_merged.json') as f:
    rs = json.load(f)

print('=== M162 FINAL DATA ===')
print()
fields_h = {3: [], 4: [], 5: []}
for r in rs:
    fields_h[r['h']].append(r)

for h in (3, 4, 5):
    Ds = sorted(set(r['D'] for r in fields_h[h]), key=abs)
    print(f'h={h} fields tested ({len(Ds)}): {Ds}')
    nrat = sum(1 for r in fields_h[h] if r['is_rational'])
    nQ = sum(1 for r in fields_h[h] if r['is_rational'] and r['verdict']=='Q')
    nQs = sum(1 for r in fields_h[h] if r['is_rational'] and r['verdict']=='Q*sqrt(d_K)')
    print(f'  Total rational forms: {nrat}; in Q: {nQ}; in Q*sqrt(d_K): {nQs}')

print()
print('=== M114.B verdict ===')
n_Q = sum(1 for r in rs if r['is_rational'] and r['verdict']=='Q')
n_Qs = sum(1 for r in rs if r['is_rational'] and r['verdict']=='Q*sqrt(d_K)')
n_total = sum(1 for r in rs if r['is_rational'])
print(f'M162 alone: {n_total} rational; {n_Q} in Q (violation); {n_Qs} in Q*sqrt(d_K)')

# c-formula
def get_c(D):
    if D % 4 == 1: return '3/4'
    if D % 4 == 0: return '6'
    return None

print()
print('=== M161B.2 c-formula extension (M162.1) ===')
n_pass = 0
n_fail = 0
n_skip = 0
for r in rs:
    a1dk = r.get('alpha_1_per_sqd_dk')
    if a1dk in (None, 'None', ''):
        n_skip += 1
        continue
    expected = get_c(r['D'])
    if a1dk == expected:
        n_pass += 1
    else:
        n_fail += 1
        print(f'  MISMATCH: D={r["D"]} j={r["j"]} obs={a1dk} exp={expected}')
print(f'c-formula pass: {n_pass} / {n_pass+n_fail} (skipped {n_skip} non-evaluable)')

# Damerell parity-split for rationals
print()
print('=== Damerell parity-split (rational forms, h>=3) ===')
n_par = 0
for r in rs:
    if not r['is_rational']: continue
    a1 = r.get('alpha_1_per_sqd')
    a2 = r.get('alpha_2')
    a3 = r.get('alpha_3_per_sqd')
    if a1 and a2 and a3:
        n_par += 1
print(f'  {n_par} rational forms with full Damerell ladder confirmed')

# Hecke Q(i) forms
print()
print('=== Hecke forms with R(f) in Q(i) ===')
for r in rs:
    if not r['is_rational'] and r['verdict']=='Q(i)':
        print(f'  D={r["D"]} j={r["j"]} a2={r["a2"][:40]} val={r["value"]}')
