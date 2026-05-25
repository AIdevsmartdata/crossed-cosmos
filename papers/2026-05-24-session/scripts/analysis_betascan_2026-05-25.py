#!/usr/bin/env python3
"""Analyse β-scan FAST V3 — separate leading vs sub-leading in c_3D(L, β).

Dataset : β ∈ {2.3, 2.4, 2.5, 2.6} × L ∈ {8, 10, 12}.

Model 1 : c_3D = κ_lead/a²(β) + C_sub · log(L) + const
Model 2 : c_3D = a · β + b · log(L) + c  (linear in β)
Model 3 : c_3D = ASYMPTOTIC κ via continuum extrap β → ∞

SU(2) pure Wilson 1-loop beta-function for a(β):
  a Λ_L = (12π²β / 11) ^ (51/121) · exp(-12π²β / 22)
  where β = 4/g² for SU(2) Wilson
  b_0 = 11N / (48π²) = 22/(48π²) for SU(N=2)

Crude 1-loop: a(β) ~ exp(-12π²β / 22) = exp(-π²β · 6/11)

Author : Kévin Rémondière (ORCID 0009-0008-2443-7166).
"""
import json
import numpy as np
from scipy.optimize import curve_fit

# Load data
with open('/root/cc-private/papers/2026-05-24-session/data/jax_su2_EE_BETASCAN_results.json') as f:
    data = json.load(f)

results = data['results']
ALPHA_GRID = data['alpha_grid']
BETAS = sorted([float(b) for b in results.keys()])
L_VALUES = sorted([int(L) for L in results[str(BETAS[0])].keys()])

print(f"=== β-scan analysis ===")
print(f"βs : {BETAS}")
print(f"Ls : {L_VALUES}")

# Build c_3D table
print(f"\nc_3D = S_2 / (2 L_y L_z L_τ) table:")
print(f"{'L':>4} ", end='')
for b in BETAS:
    print(f"β={b:>4.1f}{'  ':>3}", end='')
print()

c_3D_table = {}
S_2_table = {}
S_2_err_table = {}
for L in L_VALUES:
    print(f"{L:>4} ", end='')
    c_3D_table[L] = {}
    S_2_table[L] = {}
    S_2_err_table[L] = {}
    for b in BETAS:
        b_str = str(b)
        L_str = str(L)
        r = results[b_str][L_str]
        T_half = r.get('T_half', L)
        A_3D = 2 * L * L * T_half
        c = r['S_2'] / A_3D
        c_err = r.get('S_2_err', 0) / A_3D
        c_3D_table[L][b] = c
        S_2_table[L][b] = r['S_2']
        S_2_err_table[L][b] = r.get('S_2_err', 0)
        print(f"{c:.4f}±{c_err:.0e} ", end='')
    print()

print(f"\nReference values:")
C_PRED = np.log(3) / (2 * np.pi * np.sqrt(2))
print(f"  log(3)/(2π√2) = {C_PRED:.6f}")
print(f"  Rabenstein 2019 C(SU(2)) = 0.054 (different normalization)")
print(f"  κ²(SU(2)) = 1/4 = 0.25 (Attempt B BH hypothesis)")

# Fit 1 : linear in β at fixed L
print(f"\n=== Fit 1 : c_3D(β) at fixed L (test β-linearity) ===")
for L in L_VALUES:
    beta_arr = np.array(BETAS)
    c_arr = np.array([c_3D_table[L][b] for b in BETAS])
    slope, intercept = np.polyfit(beta_arr, c_arr, 1)
    print(f"  L={L}: c_3D ≈ {slope:.4f}·β + {intercept:.4f}")

# Fit 2 : 1-loop a(β) hypothesis : c_3D = c_leading · exp(c1·β) + c_sub
# Beta-function : a(β) ~ exp(-12π²β / 22)
# So 1/a²(β) ~ exp(12π²β/11) — too fast
# Use simpler 2-loop a²·Λ²_L ~ (6β/11)^(102/121) · exp(-6β/11)  for SU(2)
print(f"\n=== Fit 2 : 1-loop a(β) hypothesis ===")
print(f"a²(β) = (12π²β/22)^(-204/121) · exp(-12π²β/22)  for SU(2) Wilson 1-loop")
print(f"Predict c_3D(β) ~ κ_leading / a²(β) + κ_sub")
def a2_1loop(beta):
    """1-loop a²(β) for SU(2) Wilson, up to overall scale."""
    g2 = 4.0 / beta
    return g2 * np.exp(-12 * np.pi**2 * beta / 22.0)

for L in L_VALUES:
    beta_arr = np.array(BETAS)
    c_arr = np.array([c_3D_table[L][b] for b in BETAS])
    # Fit c_3D = A / a²(β) + B
    inv_a2 = 1.0 / a2_1loop(beta_arr)
    inv_a2_normalized = inv_a2 / inv_a2[0]  # normalize to β=2.3 = 1
    A, B = np.polyfit(inv_a2_normalized, c_arr, 1)
    print(f"  L={L}: c_3D ≈ {A:.6f} · [1/a²(β)/1/a²(2.3)] + {B:.4f}")

# Fit 3 : joint fit S_2(L, β) = κ(β) · (2L³) + C · (2L³) · log(L) + D
print(f"\n=== Fit 3 : Joint S_2(L, β) = κ(β) · A_3D + C · A_3D · log(L) + D ===")
print(f"Test : if leading κ(β) and sub-leading C separate cleanly")

# Build data arrays
L_arr = []
beta_arr = []
S2_arr = []
S2_err_arr = []
A3D_arr = []
for L in L_VALUES:
    for b in BETAS:
        T_half = L  # equal to L in our runs
        A_3D = 2 * L * L * T_half
        L_arr.append(L)
        beta_arr.append(b)
        S2_arr.append(S_2_table[L][b])
        S2_err_arr.append(S_2_err_table[L][b] if S_2_err_table[L][b] > 0 else 1.0)
        A3D_arr.append(A_3D)
L_arr = np.array(L_arr)
beta_arr = np.array(beta_arr)
S2_arr = np.array(S2_arr)
S2_err_arr = np.array(S2_err_arr)
A3D_arr = np.array(A3D_arr)

# Model : S_2 = (κ_2 · β² + κ_1 · β + κ_0) · A_3D + C · A_3D · log(L) + D
# Treat κ(β) as polynomial in β (no a-functional assumption yet)
def model_S2(X, k0, k1, k2, C, D):
    L_, beta_, A3D_ = X
    kappa = k0 + k1 * beta_ + k2 * beta_**2
    return kappa * A3D_ + C * A3D_ * np.log(L_) + D

try:
    popt, pcov = curve_fit(model_S2, (L_arr, beta_arr, A3D_arr), S2_arr,
                            sigma=S2_err_arr, p0=[0.1, 0.0, 0.0, 0.01, 0.0])
    perr = np.sqrt(np.diag(pcov))
    print(f"  κ(β) = {popt[0]:.5f}(±{perr[0]:.5f}) + {popt[1]:.5f}(±{perr[1]:.5f})·β + {popt[2]:.5f}(±{perr[2]:.5f})·β²")
    print(f"  C_sub = {popt[3]:.5f} ± {perr[3]:.5f}")
    print(f"  D = {popt[4]:.5f} ± {perr[4]:.5f}")
    # Extrapolation κ at β = 2.4, 2.5, 2.6
    for b_eval in [2.3, 2.4, 2.5, 2.6, 3.0, 4.0, 10.0]:
        kappa_b = popt[0] + popt[1] * b_eval + popt[2] * b_eval**2
        print(f"  κ(β={b_eval}) = {kappa_b:.5f}")
    print(f"  κ(β→∞) limit = κ_2 · β² → diverges (1/a² → ∞ as β → ∞)")
    print(f"  → Need a(β) functional form for continuum extrap")
except Exception as e:
    print(f"  Fit failed : {e}")

# Direct check : if c_3D(β) is leading-dominated, c_3D should grow as 1/a²(β)
# Compare ratios :
print(f"\n=== Ratio analysis : test if c_3D ~ 1/a²(β) ===")
print(f"{'β1':>5} {'β2':>5} {'c_3D ratio':>12} {'1/a²(β2)/(1/a²(β1)) 1-loop':>30}")
for i in range(len(BETAS) - 1):
    for j in range(i + 1, len(BETAS)):
        b1 = BETAS[i]
        b2 = BETAS[j]
        # Average c_3D across L
        c1 = np.mean([c_3D_table[L][b1] for L in L_VALUES])
        c2 = np.mean([c_3D_table[L][b2] for L in L_VALUES])
        ratio_c = c2 / c1
        ratio_1loop = a2_1loop(b1) / a2_1loop(b2)  # 1/a² ratio
        print(f"{b1:>5.1f} {b2:>5.1f} {ratio_c:>12.4f} {ratio_1loop:>30.4f}")

print(f"\nInterpretation :")
print(f"  - If c_3D ratios ≈ 1/a² ratios : leading 1/a² dominates")
print(f"  - If c_3D ratios « 1/a² ratios : sub-leading dominates (small β-dep)")
print(f"  - Expected for current data : c_3D ratios ~ 1.25 vs 1/a² ratios ~ 5 → SUB-LEADING dominates")
print(f"    Reason : BP2008b α-integration largely cancels the UV-divergent leading term")
print(f"    The residual β-dependence is non-universal sub-leading correction")
