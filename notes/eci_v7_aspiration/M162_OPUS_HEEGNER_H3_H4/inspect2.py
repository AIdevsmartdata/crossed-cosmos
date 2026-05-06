#!/usr/bin/env python3
"""Inspect h=3 j=1 forms: although a_p ∈ cubic field, alpha_1/sqd/dK = 3/4 exactly."""
import json
with open('/root/crossed-cosmos/notes/eci_v7_aspiration/M162_OPUS_HEEGNER_H3_H4/04_results.json') as f:
    rs = json.load(f)

print('h=3 forms (all 6 fields, both j):')
print()
for D in sorted(set(r['D'] for r in rs if r['h']==3), reverse=True):
    rs_D = [r for r in rs if r['D']==D]
    print(f"D={D} (Q(sqrt({D}))):")
    for r in rs_D:
        a2 = r['a2'][:60]
        print(f"  j={r['j']} {'rat' if r['is_rational'] else 'Hecke'} a2={a2}")
        print(f"    L1={r['L1'][:50]}...")
        print(f"    Rf={r['Rf'][:60]}...")
        print(f"    alpha_1/sqd={r.get('alpha_1_per_sqd')}, alpha_1/sqd/dK={r.get('alpha_1_per_sqd_dk')}")
        print(f"    alpha_2={r.get('alpha_2')}")
        print(f"    alpha_3/sqd={r.get('alpha_3_per_sqd')}")
    print()
