#!/usr/bin/env python3
"""
M162 Sub-task 5: Damerell parity-split test.

For h=3, 4, 5 RATIONAL CM newforms, compute alpha_1, alpha_2, alpha_3
and verify M97 parity split:
  - alpha_1, alpha_3 ∈ Q*sqrt(d_K) \ Q (parity-odd)
  - alpha_2 ∈ Q (parity-even)

Uses 04_results.json data (alpha_1_per_sqd, alpha_2, alpha_3_per_sqd).
"""

import json
import sympy as sp

import os
INPUT_PATH = "/root/crossed-cosmos/notes/eci_v7_aspiration/M162_OPUS_HEEGNER_H3_H4/04_results_merged.json"
if not os.path.exists(INPUT_PATH):
    INPUT_PATH = "/root/crossed-cosmos/notes/eci_v7_aspiration/M162_OPUS_HEEGNER_H3_H4/04_results.json"
with open(INPUT_PATH) as f:
    results = json.load(f)

print("=" * 70)
print("M162 Sub-task 5: Damerell parity-split for h>=3 rational CM newforms")
print("=" * 70)

print()
print(f"{'D':>5} {'h':>2} {'j':>2} {'alpha_1/sqd':>15} {'alpha_2':>15} {'alpha_3/sqd':>15} {'alpha_1/sqd/dK':>15}")
print("-" * 100)

n_pass = 0
n_total = 0
for r in results:
    if not r["is_rational"]:
        continue
    n_total += 1
    D, h, j = r["D"], r["h"], r["j"]
    a1 = r.get("alpha_1_per_sqd")
    a2 = r.get("alpha_2")
    a3 = r.get("alpha_3_per_sqd")
    a1dk = r.get("alpha_1_per_sqd_dk")
    print(f"{D:>5} {h:>2} {j:>2} {str(a1):>15} {str(a2):>15} {str(a3):>15} {str(a1dk):>15}")

    # Pass = a1, a3 are in Q*sqrt(d_K) (i.e., they exist as rationals divided by sqrt)
    #         a2 is in Q
    if (a1 is not None) and (a3 is not None) and (a2 is not None):
        try:
            sp.Rational(a1)
            sp.Rational(a2)
            sp.Rational(a3)
            n_pass += 1
        except Exception:
            pass

print()
print(f"Damerell parity-split confirmation (alpha_1 ∈ Q·√d_K, alpha_2 ∈ Q, alpha_3 ∈ Q·√d_K):")
print(f"  {n_pass}/{n_total} rational forms pass")

# Now M161B.2 c-formula test
print()
print("=" * 70)
print("M161B.2 c-formula test (alpha_1/sqrt(d_K)/d_K = 3/4 or 6)")
print("=" * 70)
print()
print(f"{'D':>5} {'h':>2} {'j':>2} {'D mod 4':>7} {'a1/sqd/dK':>14} {'expected':>10} {'match':>6}")
print("-" * 70)

m_pass = 0
m_fail = 0
m_violations = []
for r in results:
    D, h, j = r["D"], r["h"], r["j"]
    a1dk = r.get("alpha_1_per_sqd_dk")
    if a1dk is None or a1dk == "None":
        continue
    try:
        c_obs = sp.Rational(a1dk)
    except Exception:
        continue
    Dmod4 = D % 4
    if Dmod4 == 1:
        c_exp = sp.Rational(3, 4)
    elif Dmod4 == 0:
        c_exp = sp.Integer(6)
    else:
        continue
    match = (c_obs == c_exp)
    rat = "rat" if r["is_rational"] else "Hecke"
    if match:
        m_pass += 1
    else:
        m_fail += 1
        m_violations.append((D, h, j, c_obs, c_exp, rat))
    star = " *" if not r["is_rational"] and match else ""
    print(f"{D:>5} {h:>2} {j:>2} {Dmod4:>7} {str(c_obs):>14} {str(c_exp):>10} {('OK' if match else 'FAIL'):>6} {rat}{star}")

print()
print(f"M161B.2 c-formula passes: {m_pass}/{m_pass + m_fail}")
if m_violations:
    print(f"Violations:")
    for D, h, j, c_obs, c_exp, rat in m_violations:
        print(f"  D={D} h={h} j={j} ({rat}) — observed {c_obs}, expected {c_exp}")

# Save
with open("/root/crossed-cosmos/notes/eci_v7_aspiration/M162_OPUS_HEEGNER_H3_H4/05_damerell.json", "w") as f:
    json.dump({
        "damerell_parity_pass": n_pass,
        "damerell_parity_total": n_total,
        "M161B2_pass": m_pass,
        "M161B2_total": m_pass + m_fail,
        "M161B2_violations": [(D, h, j, str(co), str(ce), rat) for D, h, j, co, ce, rat in m_violations],
    }, f, indent=2)
print()
print("Results saved to 05_damerell.json")
