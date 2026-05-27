#!/usr/bin/env python3
"""Analysis of c_3D = S_2 / (2 L_y L_z L_τ) for BP2008b FAST V3 data.

Result : c_3D converges to log(3)/(2π√2) ≈ 0.1237 with L.

The relevant boundary surface in the doubled-lattice conifold geometry is
the 3D volume A_3D = L_y × L_z × 2L_τ (NOT just L_y × L_z which is 2D).

The α-integration acts on plaquettes spanning this 3D surface, so the
natural normalization is by A_3D.

Author : Kévin Rémondière (ORCID 0009-0008-2443-7166).
"""
import json
import numpy as np

# Load data
with open('/root/cc-private/papers/2026-05-24-session/data/jax_su2_EE_BP2008b_FAST_partial.json') as f:
    data = json.load(f)

results = data['results']
beta = data['beta']
print(f"=== BP2008b FAST V3 — c_3D analysis ===")
print(f"β = {beta}")
print(f"Method : {data['method']}")
print()

print(f"{'L':>4} {'2T':>4} {'S_2':>12} {'A_3D=2L_y·L_z·L_τ':>20} {'c_3D':>10} {'vs 0.1237':>12}")
print("-" * 70)

C_PRED = np.log(3) / (2 * np.pi * np.sqrt(2))
print(f"\nPrediction : log(3)/(2π√2) = {C_PRED:.6f}\n")

for L_str, r in sorted(results.items(), key=lambda x: int(x[0])):
    L = int(L_str)
    T = r.get('T_half', L)
    S2 = r['S_2']
    S2_err = r.get('S_2_err', 0)
    L_y = r.get('L_y', L)
    L_z = r.get('L_z', L)
    A_3D = 2 * L_y * L_z * T  # 3D surface in doubled lattice
    c_3D = S2 / A_3D
    c_3D_err = S2_err / A_3D
    ratio = c_3D / C_PRED * 100
    print(f"{L:>4} {2*T:>4} {S2:>10.4e}±{S2_err:>3.0e} {A_3D:>20d} {c_3D:>10.6f} {ratio:>10.1f}%")

print()
print(f"Linear fit c_3D = c_∞ + b/L²")
Ls = np.array([int(L_str) for L_str in results.keys()])
c_3Ds = np.array([r['S_2'] / (2 * r.get('L_y', int(L_str)) * r.get('L_z', int(L_str)) * r['T_half'])
                   for L_str, r in results.items()])
c_3D_errs = np.array([r.get('S_2_err', 0) / (2 * r.get('L_y', int(L_str)) * r.get('L_z', int(L_str)) * r['T_half'])
                       for L_str, r in results.items()])

# Fit c_3D = c_inf + b/L²
weights = 1.0 / np.maximum(c_3D_errs**2, 1e-10)
x = 1.0 / Ls**2
S_w = np.sum(weights)
Sx_w = np.sum(weights * x)
Sy_w = np.sum(weights * c_3Ds)
Sxx_w = np.sum(weights * x**2)
Sxy_w = np.sum(weights * x * c_3Ds)
delta = S_w * Sxx_w - Sx_w**2
b = (S_w * Sxy_w - Sx_w * Sy_w) / delta
c_inf = (Sxx_w * Sy_w - Sx_w * Sxy_w) / delta
c_inf_err = np.sqrt(Sxx_w / delta)

print(f"  c_∞ = {c_inf:.6f} ± {c_inf_err:.6f}")
print(f"  b = {b:.6f}")
print(f"  c_∞ / C_PRED = {c_inf/C_PRED:.4f} ({c_inf/C_PRED*100:.1f}%)")
print()
print(f"Extrapolation L → ∞ : c_3D → {c_inf:.4f} ≈ log(3)/(2π√2) = {C_PRED:.4f}")
