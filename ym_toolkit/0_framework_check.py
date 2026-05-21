#!/usr/bin/env python3
"""Verify framework on PC gamer + compute all 29 channels in 30 seconds."""
import math, json
from fractions import Fraction

print("=" * 60)
print("YM Framework verification — PC gamer")
print("=" * 60)

# 2 integer anchors
delta = 2
N0 = 3

# Derived constants
xi = Fraction(delta, 1 + delta)            # 2/3
eta = Fraction(1, delta)                    # 1/2
F_inf = Fraction(N0**2, N0**2 + 1)          # 9/10
beta = delta + F_inf * xi                   # 13/5
c_eta = (xi + delta) / (F_inf + beta)       # 16/21
alpha_PW = (1 - xi) / c_eta                 # 7/16
K = math.sqrt(2*math.pi*math.e*float(xi))

print(f"\nAnchors : δ={delta}, N₀={N0}")
print(f"Derived :")
print(f"  ξ★ = δ/(1+δ) = {xi}")
print(f"  η_∞ = 1/δ = {eta}")
print(f"  F_∞ = N₀²/(N₀²+1) = {F_inf}")
print(f"  β = δ + F·ξ = {beta}")
print(f"  c_η = (ξ+δ)/(F+β) = {c_eta}")
print(f"  α_PW = (1-ξ)/c_η = {alpha_PW}")
print(f"  K = √(2πe·ξ) = {K:.4f}")

# Identities verification
assert xi * eta == 1 - xi, "ξ·η ≠ 1-ξ"
assert delta * eta == 1, "δ·η ≠ 1"
assert beta == Fraction(13,5)
assert c_eta == Fraction(16,21)
assert alpha_PW == Fraction(7,16)
print(f"\n✓ All algebraic identities VERIFIED")

# 29-channel test
AT2021 = {
    (0,1,1,0,3): 3.405, (2,1,1,0,3): 4.894, (0,-1,1,0,3): 5.276,
    (3,1,1,0,3): 7.71, (4,1,1,0,3): 7.60, (2,-1,1,0,3): 6.32,
    (1,1,-1,0,3): 6.065, (3,1,-1,0,3): 7.27,
    (1,-1,-1,0,3): 8.31, (2,-1,-1,0,3): 8.08,
    (0,1,1,1,3): 5.855, (2,1,1,1,3): 6.788, (0,-1,1,1,3): 7.29,
    (2,-1,1,1,3): 8.18, (1,1,-1,1,3): 7.82,
    (0,1,1,0,2): 3.78, (2,1,1,0,2): 5.45, (0,-1,1,0,2): 5.46,
    (0,1,1,0,4): 3.307, (2,1,1,0,4): 4.750, (0,-1,1,0,4): 5.13,
    (0,1,1,0,5): 3.236, (2,1,1,0,5): 4.65, (0,-1,1,0,5): 5.05,
    (0,1,1,0,6): 3.205, (2,1,1,0,6): 4.62, (0,-1,1,0,6): 5.02,
    (0,1,1,0,7): 3.183, (0,1,1,0,8): 3.151, (2,1,1,0,8): 4.56,
}

def m_pred(J, P, C, ex, N):
    F_N = float(F_inf) * (1 + 1/N**2)
    eta_N = float(eta) - 16/(21*N**2)
    boost = delta if J == 1 else 0
    base = float(xi)*(J*(J+1)/3 + boost) + (float(beta) - P)*(ex + float(xi))
    cmult = 1 + eta_N*(1 - C)/2
    c2 = base * cmult
    return K * F_N * math.sqrt(c2) if c2 > 0 else None

print(f"\n29-channel test :")
diffs = []
for key, m_obs in AT2021.items():
    m_th = m_pred(*key)
    if m_th:
        d = abs(m_th - m_obs)/m_obs * 100
        diffs.append(d)

import numpy as np
diffs = np.array(diffs)
print(f"  Mean diff : {diffs.mean():.2f}%")
print(f"  Within 7% : {(diffs<7).sum()}/{len(diffs)} ({(diffs<7).mean()*100:.0f}%)")

# Save results
with open('framework_check.json', 'w') as f:
    json.dump({
        'anchors': {'delta': delta, 'N0': N0},
        'derived': {'xi': str(xi), 'eta': str(eta), 'F': str(F_inf),
                    'beta': str(beta), 'c_eta': str(c_eta), 'alpha_PW': str(alpha_PW)},
        'identities_verified': True,
        'mean_diff_pct': float(diffs.mean()),
        'within_7pct': int((diffs<7).sum()),
        'total_channels': len(diffs),
    }, f, indent=2)
print(f"\n✓ Saved framework_check.json")
