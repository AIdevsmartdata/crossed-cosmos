#!/usr/bin/env python3
"""Finalize: merge 04 + 08 (h=5) into canonical 04_results.json."""
import json
import shutil

with open('/root/crossed-cosmos/notes/eci_v7_aspiration/M162_OPUS_HEEGNER_H3_H4/04_results.json') as f:
    main = json.load(f)
with open('/root/crossed-cosmos/notes/eci_v7_aspiration/M162_OPUS_HEEGNER_H3_H4/08_h5_results.json') as f:
    h5 = json.load(f)

main_keys = set((r['D'], r['j']) for r in main)
added = 0
for r in h5:
    if (r['D'], r['j']) not in main_keys:
        main.append(r)
        added += 1

with open('/root/crossed-cosmos/notes/eci_v7_aspiration/M162_OPUS_HEEGNER_H3_H4/04_results.json', 'w') as f:
    json.dump(main, f, indent=2, default=str)
print(f'Final merged: {len(main)} entries (added {added} h=5)')

# Also dump compact CSV-like output of all rationals
print()
print('All rational forms (final):')
print(f'{"D":>5} {"h":>2} {"j":>2} {"a_2":>4} {"verdict":>20} {"R/sqrt(d_K)":>20} {"a1/sqd/dK":>10}')
for r in main:
    if r['is_rational']:
        print(f"{r['D']:>5} {r['h']:>2} {r['j']:>2} {r['a2']:>4} {r['verdict']:>20} {str(r['value']):>40} {str(r.get('alpha_1_per_sqd_dk')):>10}")
