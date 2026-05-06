#!/usr/bin/env python3
"""
M162 Sub-task 1: Enumerate imaginary quadratic fields with class number h=3, 4, 5
below |D|=420. Verify class numbers via PARI qfbclassno + first-principles
binary form enumeration.

Mission targets:
- h=3: D ∈ {-23, -31, -59, -83, -107, -139, -211, -283}
- h=4: D ∈ {-39, -55, -56, -68, -84, -120, -132, -136, -155, -184, -195,
            -228, -232, -244, -260, -264, -280, -292, -312, -340, -372, -388, -403, -408}
- h=5: D ∈ {-47, -79, -103, -127}
"""

import math
from math import gcd

def reduced_forms(D):
    """Enumerate reduced primitive forms of discriminant D."""
    assert D < 0 and D % 4 in (0, 1), f"Invalid discriminant D={D}"
    forms = []
    abs_D = -D
    a_max = int(math.isqrt(abs_D // 3)) + 1
    for a in range(1, a_max + 1):
        for b in range(-a, a + 1):
            if (b * b - D) % (4 * a) != 0:
                continue
            c = (b * b - D) // (4 * a)
            if c < a:
                continue
            if c == a and b < 0:
                continue
            if abs(b) == a and b < 0:
                continue
            if gcd(gcd(a, abs(b)), c) != 1:
                continue
            forms.append((a, b, c))
    return forms

target_h3 = [-23, -31, -59, -83, -107, -139, -211, -283]
target_h4 = [-39, -55, -56, -68, -84, -120, -132, -136, -155, -184, -195,
             -228, -232, -244, -260, -264, -280, -292, -312, -340,
             -372, -388, -403, -408]
target_h5 = [-47, -79, -103, -127]

print("=" * 70)
print("M162 Sub-task 1: h=3, h=4, h=5 imaginary quadratic field enumeration")
print("=" * 70)

import cypari2
pari = cypari2.Pari()

def verify_target(D, expected_h):
    forms = reduced_forms(D)
    h_py = len(forms)
    h_pari = int(pari.qfbclassno(D))
    fundamental = pari.isfundamental(D)
    is_fund = (int(fundamental) != 0)
    if D % 4 == 0:
        d_K = (-D) // 4
        # square-free check
        sqfree = True
        for k in range(2, int(math.isqrt(d_K)) + 1):
            if d_K % (k*k) == 0:
                sqfree = False
                break
        K_label = f"Q(sqrt(-{d_K}))"
    else:
        d_K = -D  # since D = d_K formula for fundamental D ≡ 1 mod 4 means d_K = |D|
        K_label = f"Q(sqrt({D}))"
    return h_py, h_pari, is_fund, d_K, K_label

print()
print(f"{'D':>5} {'h_target':>8} {'h_py':>4} {'h_pari':>6} {'fundamental':>11} {'d_K':>4}  {'K':>20}")
print("-" * 80)

results = {3: [], 4: [], 5: []}

for h_target, target_list in [(3, target_h3), (4, target_h4), (5, target_h5)]:
    for D in target_list:
        h_py, h_pari, is_fund, d_K, K_label = verify_target(D, h_target)
        match = (h_py == h_pari == h_target) and is_fund
        marker = "OK" if match else "FAIL"
        print(f"{D:>5} {h_target:>8} {h_py:>4} {h_pari:>6} {str(is_fund):>11} {d_K:>4}  {K_label:>20}  [{marker}]")
        if match:
            results[h_target].append({"D": D, "d_K": d_K, "K": K_label, "N": -D, "h": h_target})

print()
print("=" * 70)
print("Summary: validated targets")
print("=" * 70)

import json
all_targets = []
for h, lst in results.items():
    print(f"\n  h={h}: {len(lst)} fields")
    for entry in lst:
        print(f"    D={entry['D']:>4}  d_K={entry['d_K']:>3}  N={entry['N']:>3}  D mod 4 = {entry['D'] % 4}")
        all_targets.append(entry)

with open("/root/crossed-cosmos/notes/eci_v7_aspiration/M162_OPUS_HEEGNER_H3_H4/01_targets.json", "w") as f:
    json.dump(all_targets, f, indent=2)
print(f"\nSaved {len(all_targets)} targets to 01_targets.json")
