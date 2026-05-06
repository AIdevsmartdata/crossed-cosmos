#!/usr/bin/env python3
import json
import sys
sys.path.append('/tmp')

with open('/root/crossed-cosmos/notes/eci_v7_aspiration/M162_OPUS_HEEGNER_H3_H4/04_results_merged.json') as f:
    rs = json.load(f)

ds = {}
for r in rs:
    ds.setdefault(r['D'], []).append(r)

print(f'{"D":>5} {"h":>2} {"d_K":>3} {"#total":>6} {"#rational":>9} {"#Q":>3} {"#Q*sqrt":>7} {"#Q(i)":>5} {"#OTHER":>6}')
print('-'*70)
for D in sorted(ds.keys(), key=abs):
    field = ds[D]
    h = field[0]['h']
    d_K = field[0]['d_K']
    n = len(field)
    n_rat = sum(1 for r in field if r['is_rational'])
    rat_only = [r for r in field if r['is_rational']]
    q = sum(1 for r in rat_only if r['verdict']=='Q')
    qsq = sum(1 for r in rat_only if r['verdict']=='Q*sqrt(d_K)')
    qi = sum(1 for r in rat_only if r['verdict']=='Q(i)')
    other = sum(1 for r in rat_only if r['verdict']=='OTHER')
    print(f'{D:>5} {h:>2} {d_K:>3} {n:>6} {n_rat:>9} {q:>3} {qsq:>7} {qi:>5} {other:>6}')

print()
print('Hecke forms with R(f) in Q(i):')
for r in rs:
    if not r['is_rational'] and r['verdict']=='Q(i)':
        print(f'  D={r["D"]} j={r["j"]}, a2={r["a2"][:50]}, val={r["value"]}')

print()
print('Total rationals:')
n_rat_total = sum(1 for r in rs if r['is_rational'])
n_Q = sum(1 for r in rs if r['is_rational'] and r['verdict']=='Q')
n_Qsqrt = sum(1 for r in rs if r['is_rational'] and r['verdict']=='Q*sqrt(d_K)')
print(f'  {n_rat_total} rationals; {n_Q} in Q (M114.B violation); {n_Qsqrt} in Q*sqrt(d_K)')
