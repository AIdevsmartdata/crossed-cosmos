#!/usr/bin/env python3
"""F(N) glueball re-fit: scan c ∈ [0.4, 1.2] + scan m_inf to minimize χ²
Resolves the F(N) tension found at c=0.80 (χ²=41.5)"""
import json
import numpy as np

LATTICE = {
    2: (3.78, 0.04),
    3: (3.56, 0.05),
    4: (3.45, 0.06),
    5: (3.40, 0.07),
}

def F_N(N, c):
    return (1 + c/N**2) / (1 + c/9)

def chi2(c, m_inf):
    s = 0.0
    for N, (obs, err) in LATTICE.items():
        pred = m_inf * F_N(N, c)
        s += ((pred - obs) / err) ** 2
    return s

# Grid search c × m_inf
best = (None, None, float("inf"))
for c in np.arange(0.0, 2.0, 0.01):
    for m_inf in np.arange(3.0, 4.5, 0.01):
        s = chi2(c, m_inf)
        if s < best[2]:
            best = (c, m_inf, s)

c_best, m_inf_best, chi2_best = best
print(f"BEST FIT: c = {c_best:.3f}, m_inf = {m_inf_best:.3f}, χ² = {chi2_best:.3f}")
print(f"  (PUSH-2 was c=0.80, m_inf=3.36 → χ²=41.5)")
print()
print(f"Best fit predictions :")
print(f"{'N':>3} | {'F(N)':>7} | {'Pred':>7} | {'Lattice':>15} | {'Δ%':>6} | {'σ':>5}")
print("-" * 60)
for N, (obs, err) in LATTICE.items():
    pred = m_inf_best * F_N(N, c_best)
    delta_pct = abs(pred - obs) / obs * 100
    sigma = abs(pred - obs) / err
    print(f"{N:>3} | {F_N(N, c_best):>7.4f} | {pred:>7.3f} | {obs:>9.3f}±{err:.2f} | {delta_pct:>5.1f}% | {sigma:>5.2f}")

# Predictions for SU(6-10)
print(f"\nPREDICTIONS SU(6-10) at best fit c={c_best:.3f}, m_inf={m_inf_best:.3f}:")
for N in range(6, 11):
    pred = m_inf_best * F_N(N, c_best)
    print(f"  SU({N}): m_0++/√σ = {pred:.3f}")

# Test c=0.67 specifically (Kevin's suggestion)
print(f"\nTest c=0.67:")
for m_inf in [3.4, 3.6, 3.8]:
    chi = chi2(0.67, m_inf)
    print(f"  c=0.67, m_inf={m_inf}: χ²={chi:.3f}")

# Save
with open("/tmp/FN_refit_results.json", "w") as f:
    json.dump({
        "best_c": c_best, "best_m_inf": m_inf_best, "best_chi2": chi2_best,
        "push2": {"c": 0.80, "m_inf": 3.36, "chi2": chi2(0.80, 3.36)},
        "kevin_c067": {"c": 0.67, "best_m_inf_for_c": min(np.arange(3.0, 4.5, 0.01), key=lambda m: chi2(0.67, m)),
                       "best_chi2_for_c": min(chi2(0.67, m) for m in np.arange(3.0, 4.5, 0.01))}
    }, f, indent=2)
print(f"\nSaved /tmp/FN_refit_results.json")
