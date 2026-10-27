#!/usr/bin/env python3
"""Read the 256 boxes <k0, k1, lb, h0, h1> of lean/KevYM/Certif/DobrushinCordale/Donnees.lean (exact rationals)
and write them as a JSON list [k0, k1, lb, h0, h1, index] for cert_vch.py (--boxes) and compare_CH.py.
Written for the archive; it only parses the Lean data file (no import of ../certificate_chordal)."""
import json, re, sys
from fractions import Fraction as F

src, dst = sys.argv[1], sys.argv[2]
txt = open(src, encoding="utf-8").read()
body = txt[txt.index("def boites : List Boite := ["):txt.index("theorem boites_length")]
num = r"\((-?\d+):ℚ\)(?:/(\d+))?"
rows = []
for m in re.finditer(r"⟨" + r",\s*".join([num] * 5) + r"⟩", body):
    g = m.groups()
    vals = [F(int(g[2 * i]), int(g[2 * i + 1]) if g[2 * i + 1] else 1) for i in range(5)]
    rows.append([str(v) for v in vals] + [len(rows)])
assert len(rows) == 256, len(rows)
assert F(rows[0][0]) == 0 and F(rows[-1][1]) == F(4, 3)
assert all(F(rows[i][1]) == F(rows[i + 1][0]) for i in range(len(rows) - 1))
json.dump(rows, open(dst, "w"), indent=0)
print(f"{len(rows)} boxes read from {src.split('/')[-1]}, chained from 0 to 4/3")
print(",".join(f"{r[0]}:{r[1]}" for r in rows), file=open(dst + ".boxes", "w"))
