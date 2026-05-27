#!/usr/bin/env python3
"""
H44 — Recherche systématique pattern p/q sur observables SM.

Pour chaque observable X, chercher p/q minimisant |X - p/q| avec q ≤ 50,
puis identifier si q a une interpretation structurelle (= dim G, # generators, etc.).

Author : Kévin Rémondière (ORCID 0009-0008-2443-7166).
"""
import numpy as np
from fractions import Fraction

# SM observables (PDG 2024 or as noted)
OBS = {
    # EW
    'sin²θ_W (MS-bar)': 0.23121,
    'cos²θ_W (MS-bar)': 0.76879,
    'sin²θ_W (eff lept)': 0.23156,
    '(m_W/m_Z)²': (80.379/91.1876)**2,
    'ρ param': 1.00038,
    # Couplings
    'α_s(M_Z)': 0.1179,
    'α_em(M_Z)': 1/127.951,
    # Masses (ratios to v=246.22)
    'm_H/v': 125.10/246.22,
    'm_W/v': 80.379/246.22,
    'm_Z/v': 91.1876/246.22,
    'm_t/v': 172.57/246.22,
    'm_b/v': 4.18/246.22,
    'm_τ/v': 1.7768/246.22,
    'm_μ/v': 0.10566/246.22,
    'm_e/v': 0.5110e-3/246.22,
    # Higgs
    'm_H/m_Z': 125.10/91.1876,
    'm_H/m_W': 125.10/80.379,
    'λ_H': (125.10**2)/(2*246.22**2),
    # Yukawa squared
    'y_top²': 2*(172.57)**2/(246.22**2),
    'y_b²': 2*(4.18)**2/(246.22**2),
    'y_τ²': 2*(1.7768)**2/(246.22**2),
    # CKM
    'V_us': 0.2253,
    'V_cb': 0.0410,
    'V_ub': 0.00367,
    'J_CP': 3.05e-5,
    # PMNS
    'sin²θ₁₂': 0.307,
    'sin²θ₂₃': 0.546,
    'sin²θ₁₃': 0.0220,
    # Cosmo
    'n_s': 0.965,
    'r upper': 0.036,
    'Ω_DM/Ω_b': 5.36,
    'h² Ω_DM': 0.120,
}

def best_rational(x, q_max=50, tol_frac=0.05):
    """Find p/q with smallest q such that |x - p/q|/x < tol_frac."""
    best = None
    for q in range(1, q_max+1):
        p = round(x * q)
        if p <= 0: continue
        diff = abs(x - p/q)/x
        if best is None or diff < best[2]:
            best = (p, q, diff)
    return best

print("="*78)
print("H44 — Pattern p/q sur observables SM (q ≤ 50)")
print("="*78)

structural_q = {
    1: 'trivial', 2: 'rank(SU(3))', 3: 'fund SU(3)/generations',
    4: 'rank SO(5)', 5: 'fund SU(5)', 6: '|Φ⁺(SU(3))|·2',
    7: 'fund SU(7)', 8: 'adj SU(3) (gluons)', 9: 'dim(SU(3))+1=N²',
    10: 'adj SO(5) or dim SO(5)', 11: 'b_2(K3)·1/2', 12: 'octahedron edges',
    13: 'dim_fund+adj+rank SU(3)=3+8+2 ★', 14: 'dim G_2',
    15: 'dim adj SU(4)', 16: 'fund SO(10) spinor', 17: 'prime',
    18: '2·dim(SU(3))+2', 19: 'prime',
    20: 'dim adj SO(5)? no, dim Λ²V SU(5)/2',
    21: 'b_2(K3)-1', 22: 'b_2(K3) ★', 23: 'M_24 23A',
    24: '|Φ⁺(SU(5))|·2 = adj SU(5)', 25: 'fund⊗fund SU(5)',
    26: '?', 27: 'fund E_6', 28: '?', 29: 'prime',
    30: 'adj E_6 + 2', 31: 'prime', 32: 'spinor SO(7)',
    33: 'fund Λ⁵F4', 34: '?', 35: 'dim adj SU(6)',
    36: 'fund⊗fund SU(6)', 37: 'prime', 38: '?',
    39: '3·dim_fund(SU(13))?', 40: '?', 41: 'prime',
    42: '6·7 = 2·dim G_2 + 14', 43: 'prime',
    44: '?', 45: 'dim adj SO(10) - 1', 46: '?',
    47: 'prime', 48: 'dim adj SU(7) - 1', 49: 'fund⊗fund SU(7)',
    50: '?'
}

print(f"\n{'Observable':<25} {'value':<12} {'best p/q':<10} {'Δ%':<8} {'q interpretation':<30}")
print("-" * 100)

results = []
for name, x in OBS.items():
    res = best_rational(x, q_max=50, tol_frac=0.01)
    if res is None: continue
    p, q, diff = res
    interp = structural_q.get(q, '?')
    diff_pct = diff * 100
    flag = "★" if diff_pct < 0.5 else ("✓" if diff_pct < 1 else " ")
    print(f"{name:<25} {x:<12.5f} {p}/{q:<7} {diff_pct:<7.2f} {flag} {interp}")
    results.append({'name': name, 'value': x, 'p_q': (p, q), 'diff_pct': diff_pct, 'interp': interp})

# Sort by quality of fit
print(f"\n{'='*78}")
print("TOP RATIOS p/q par qualité (<0.3% match)")
print(f"{'='*78}")
for r in sorted(results, key=lambda x: x['diff_pct'])[:15]:
    p, q = r['p_q']
    print(f"  {r['name']:<25} = {p}/{q} = {p/q:.5f}  Δ={r['diff_pct']:.3f}%  {r['interp']}")

# Group by denominator q to find common structures
print(f"\n{'='*78}")
print("Groupement par dénominateur q")
print(f"{'='*78}")
from collections import defaultdict
by_q = defaultdict(list)
for r in results:
    if r['diff_pct'] < 1:
        p, q = r['p_q']
        by_q[q].append((r['name'], p, r['diff_pct']))
for q in sorted(by_q):
    if len(by_q[q]) >= 2:
        print(f"\n  q={q} ({structural_q.get(q, '?')}) :")
        for name, p, dpct in by_q[q]:
            print(f"    {p}/{q} → {name} (Δ={dpct:.2f}%)")

# Special check : SU(3) state-space hypothesis 13 = 3+8+2
print(f"\n{'='*78}")
print("Test interpretation 'SU(3) state-space' : q = 13")
print(f"{'='*78}")
print(f"13 = dim_fund + dim_adj + rank = 3 + 8 + 2")
print(f"")
for r in results:
    if r['p_q'][1] == 13 and r['diff_pct'] < 1:
        p, q = r['p_q']
        if p == 3:
            interp = "fraction fund/total state-space"
        elif p == 10:
            interp = "fraction (adj+rank)/total"
        elif p == 11:
            interp = "fraction (adj+rank+1)/total"
        else:
            interp = f"unclear (p={p})"
        print(f"  {r['name']} = {p}/13 = {p/13:.5f}  Δ={r['diff_pct']:.2f}%  {interp}")

# Total state-space generalization
print(f"\nSU(N) state-space size N + (N²-1) + (N-1) = N² + 2N - 2:")
for N in [2, 3, 4, 5, 6]:
    ss = N + (N**2 - 1) + (N-1)
    print(f"  SU({N}) : N + dim_adj + rank = {N} + {N**2-1} + {N-1} = {ss}")
    print(f"    fund/total = {N}/{ss} = {N/ss:.5f}")
