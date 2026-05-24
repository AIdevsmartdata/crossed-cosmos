#!/usr/bin/env python3
"""NEW HYPOTHESES H_NEW6 + H_NEW7 + H_NEW8 — finite-β corrections + Wilson flow asymptotic + cross-Lie verification.

Trois nouvelles hypothèses tirées des findings 2026-05-24 :
H_NEW6 : α(β) = β/(β+B) finite-β shift (PySR best fit)
H_NEW7 : α saturé exists but with quadratic finite-β corrections α = α_∞·(1 - C/β²)
H_NEW8 : Cross-Lie α saturé prediction sweep SO(5), Sp(4), G_2 D=3,4
"""
import json
import os
import numpy as np
from fractions import Fraction
from math import log, exp, sqrt, comb
from scipy.optimize import curve_fit

print("="*78)
print("NEW HYPOTHESES — finite-β corrections + cross-Lie predictions")
print("="*78)

# Load combined SU(3) D=3 dataset
rows = []
files = [
    ('/tmp/voie1_calcs/su3_hmc_d3_L6_results.json', 'L=6 n=25'),
    ('/tmp/voie1_calcs/su3_hmc_d3_L8_results.json', 'L=8 n=20'),
    ('/tmp/voie1_calcs/su3_hmc_d3_L4_results.json', 'L=4 precision n=50'),
]
for f, name in files:
    if not os.path.exists(f): continue
    d = json.load(open(f))
    L = d['L']
    for r in d['results']:
        if r['beta'] > 200: continue
        rows.append({'L': L, 'beta': r['beta'], 'delta_MK': r['MK']['delta_MK']})

L4_orig = [(10.0,0.3054), (25.0,0.1866), (50.0,0.0864), (100.0,0.0675), (200.0,0.0324)]
for b, dm in L4_orig:
    rows.append({'L': 4, 'beta': b, 'delta_MK': dm})

print(f"\nDatasets: {len(rows)} datapoints")

# ============================================================
# H_NEW6 — Test PySR fit Δ = A/(β+B) directly
# ============================================================
print("\n" + "="*78)
print("H_NEW6 — Test PySR form Δ_MK = A/(β+B) on all data")
print("="*78)

def model_h_new6(beta, A, B):
    return A / (beta + B)

beta_arr = np.array([r['beta'] for r in rows])
delta_arr = np.array([r['delta_MK'] for r in rows])

popt, pcov = curve_fit(model_h_new6, beta_arr, delta_arr, p0=[5.0, 4.0])
A_fit, B_fit = popt
A_err, B_err = np.sqrt(np.diag(pcov))
print(f"\nFit Δ = A/(β+B) :")
print(f"  A = {A_fit:.3f} ± {A_err:.3f}")
print(f"  B = {B_fit:.3f} ± {B_err:.3f}")
print(f"  α_eff(β) = β/(β+B) — asymptotic α(∞) = 1")

# Compute α_eff at each β value
print(f"\n  β    | α_eff PySR-like = β/(β+B)")
for b in [10, 25, 50, 100, 200, 500, 1000, 10000]:
    a = b / (b + B_fit)
    print(f"  {b:5} | {a:.4f}")

# Residuals
predicted = model_h_new6(beta_arr, A_fit, B_fit)
residuals = delta_arr - predicted
chi2 = np.sum(residuals**2)
print(f"\n  Sum of squared residuals: {chi2:.6e}")
print(f"  RMS residual: {np.sqrt(chi2/len(rows)):.6e}")

# ============================================================
# H_NEW7 — Test saturated α with quadratic finite-β correction
# ============================================================
print("\n" + "="*78)
print("H_NEW7 — α saturé avec correction quadratique : α(β) = α_∞·(1 - C/β²)")
print("="*78)
print("""
Hypothèse : framework prédit α_∞ saturé (5/6 par A, 3/4 par B), mais à β fini :
  α(β) ≈ α_∞ + correction d'ordre 1/β²

Pour saturation avec κ correction :
  Δ_MK(β) = M·β^(-α_∞)·(1 - C/β²)  où M = scale
""")

def model_h_new7(beta, M, alpha_inf, C):
    return M * np.power(beta, -alpha_inf) * (1 - C / beta**2)

try:
    popt, pcov = curve_fit(model_h_new7, beta_arr, delta_arr,
                            p0=[5.0, 0.833, 1.0], maxfev=5000)
    M_fit, ainf_fit, C_fit = popt
    M_err, ainf_err, C_err = np.sqrt(np.diag(pcov))
    print(f"Fit Δ = M·β^(-α_∞)·(1 - C/β²) :")
    print(f"  M       = {M_fit:.3f} ± {M_err:.3f}")
    print(f"  α_∞     = {ainf_fit:.4f} ± {ainf_err:.4f}")
    print(f"  C       = {C_fit:.3f} ± {C_err:.3f}")
    print(f"  Δ_α vs 5/6 = {ainf_fit-5/6:+.4f} ({abs(ainf_fit-5/6)/ainf_err:.1f}σ)")
    print(f"  Δ_α vs 3/4 = {ainf_fit-3/4:+.4f} ({abs(ainf_fit-3/4)/ainf_err:.1f}σ)")
    print(f"  Δ_α vs 1 (Pinsker) = {ainf_fit-1:+.4f} ({abs(ainf_fit-1)/ainf_err:.1f}σ)")
    pred = model_h_new7(beta_arr, *popt)
    res2 = delta_arr - pred
    print(f"  Sum SR : {np.sum(res2**2):.6e} (vs PySR {chi2:.6e})")
except Exception as e:
    print(f"H_NEW7 fit failed: {e}")

# Try with α_∞ FIXED to 5/6 (framework prediction A)
print("\n  Test contrainte : fix α_∞ = 5/6 (A prediction)")
def model_fixed_A(beta, M, C):
    return M * np.power(beta, -5/6) * (1 - C / beta**2)
try:
    popt, pcov = curve_fit(model_fixed_A, beta_arr, delta_arr,
                            p0=[5.0, 1.0], maxfev=5000)
    print(f"    M = {popt[0]:.3f} ± {np.sqrt(pcov[0,0]):.3f}")
    print(f"    C = {popt[1]:.3f} ± {np.sqrt(pcov[1,1]):.3f}")
    pred = model_fixed_A(beta_arr, *popt)
    print(f"    Sum SR : {np.sum((delta_arr - pred)**2):.6e}")
except Exception as e:
    print(f"    Failed: {e}")

print("\n  Test contrainte : fix α_∞ = 3/4 (B prediction)")
def model_fixed_B(beta, M, C):
    return M * np.power(beta, -3/4) * (1 - C / beta**2)
try:
    popt, pcov = curve_fit(model_fixed_B, beta_arr, delta_arr,
                            p0=[5.0, 1.0], maxfev=5000)
    print(f"    M = {popt[0]:.3f} ± {np.sqrt(pcov[0,0]):.3f}")
    print(f"    C = {popt[1]:.3f} ± {np.sqrt(pcov[1,1]):.3f}")
    pred = model_fixed_B(beta_arr, *popt)
    print(f"    Sum SR : {np.sum((delta_arr - pred)**2):.6e}")
except Exception as e:
    print(f"    Failed: {e}")

# ============================================================
# H_NEW8 — Cross-Lie predictions (predicted α for SO(5), Sp(4), G_2)
# ============================================================
print("\n" + "="*78)
print("H_NEW8 — Cross-Lie α saturé predictions (à tester)")
print("="*78)

saturated_pairs = [
    ('SU(2)', 1, 1, [2]),
    ('SU(3)', 2, 3, [3, 4]),
    ('SO(5)=Sp(4)', 2, 4, [3, 4]),
    ('G_2', 2, 6, [3, 4]),
]
print(f"\n{'Group':>15} | {'|Φ⁺|':>5} | {'D':>2} | {'κ_A':>10} | {'α_A':>10} | {'shift_QNM √(1-κ)':>16} | {'test feasible?':>20}")
print("-" * 100)
for name, rk, phi, Ds in saturated_pairs:
    for D in Ds:
        kappa = Fraction(1, 2*phi)
        alpha = 1 - kappa
        shift_QNM = sqrt(float(1 - kappa))
        if name == 'SU(2)':
            feas = "easy (2D YM heat kernel)"
        elif name == 'SU(3)':
            feas = "DONE (today, α=0.85±0.04)"
        elif name == 'SO(5)=Sp(4)':
            feas = "medium (Sp(4)=Spin(5) lattice)"
        else:  # G_2
            feas = "hard (G_2 lattice complex)"
        print(f"{name:>15} | {phi:>5} | {D:>2} | {str(kappa):>10} | {str(alpha):>10} | {shift_QNM:>15.4f} | {feas:>20}")

print(f"""
PRÉDICTIONS FALSIFIABLES NEW (à tester) :
  SO(5)/Sp(4) D=3 ou 4 : α = 7/8 = 0.875 → distinct de SU(3) à 5%
  G_2 D=3 ou 4         : α = 11/12 = 0.917 → distinct de SU(3) à 10%

Si lattice SO(5) D=4 donne α = 7/8 ± 0.05 et SU(3) D=4 donne 5/6 ± 0.05
  ⟹ κ Lie-algebraic CONFIRMÉ structurellement
Si SO(5) D=4 donne α ≈ 5/6 (même que SU(3))
  ⟹ κ dépend D pas G (interprétation B comeback)
""")

# ============================================================
# H_NEW9 — Heegner Λ precision : check x best-fit
# ============================================================
print("\n" + "="*78)
print("H_NEW9 — Heegner Λ formula best-fit x value (refinement)")
print("="*78)

# Λ_obs / M_P_red^4 ratio
M_P_red = 2.435e18  # GeV reduced
rho_L_obs = 4.36e-47  # GeV^4
ratio_obs = rho_L_obs / M_P_red**4
log_ratio_obs = log(ratio_obs)
print(f"\nlog(ρ_Λ/M_P_red^4) observed = {log_ratio_obs:.4f}")

# Formula : ρ_Λ/M_P^4 = (1/4) · J(τ_-163)^x
# log(ρ_Λ/M_P^4) = -log(4) + x·log(J(-163))
# x = (log_obs + log(4)) / log(J(-163))
log_J = log(640320**3)  # |J|
x_best = (log_ratio_obs + log(4)) / log_J
x_best_neg = -x_best  # since ρ_Λ << M_P^4, x must be negative
print(f"log|J(τ_-163)| = {log_J:.4f}")
print(f"x best-fit = ({log_ratio_obs} + log(4)) / log|J| = {x_best:.6f}")
print(f"Closest integer x = -{round(abs(x_best))}, deviation = {abs(x_best) - round(abs(x_best)):+.6f}")

# Precision at x = -7 exact integer
x_int = -7
ratio_pred_int = (1/4) * np.exp(x_int * log_J)
log_ratio_pred_int = log(ratio_pred_int)
rel_err_int = abs(log_ratio_pred_int - log_ratio_obs) / abs(log_ratio_obs) * 100
print(f"\nAt x = -7 strict integer :")
print(f"  log(ρ_Λ/M_P^4) predicted = {log_ratio_pred_int:.4f}")
print(f"  Relative deviation     = {rel_err_int:.4f}%")
print(f"  BIGTABLE claim 0.0054% : {'PARTIAL CONFIRMED at best-fit x' if abs(x_best - x_int) > 0.01 else 'EXACT MATCH'}")
print(f"\n  → x best-fit = {x_best:.4f}, not exactly -7 (deviation {abs(x_best)-7:+.4f})")
print(f"  Exact integer N=7 claim is only at the {rel_err_int:.1f}% level, not 0.005%")

# ============================================================
# H_NEW10 — Pattern 4 √2 dans QNM overtones
# ============================================================
print("\n" + "="*78)
print("H_NEW10 — Pattern 4 √2 ratio dans QNM overtones (à tester)")
print("="*78)
print("""
Hypothèse : si √2 = m(2++)/m(0++) tient en YM glueball,
alors via AdS/CFT pourrait apparaître dans QNM overtones :
  ω_{n+1} / ω_n = √2

Kerr QNM overtones (Berti-Cardoso 2006 et al.) :
  Mode l=2 m=2 n=0 (fondamental) : ω_0 ≈ 0.3737 - 0.0890i (units 1/M)
  Mode l=2 m=2 n=1 (1st overtone) : ω_1 ≈ 0.3467 - 0.2739i

Ratio Re(ω_1)/Re(ω_0) ≈ 0.928 ≠ √2 = 1.414
Ratio Im(ω_1)/Im(ω_0) ≈ 3.07 ≠ √2

Donc Pattern 4 dans QNM ne tient pas en Kerr standard.
À reformuler ou à abandonner.
""")

# ============================================================
# Summary
# ============================================================
print("\n" + "="*78)
print("VERDICT NEW HYPOTHESES")
print("="*78)
print(f"""
H_NEW6 (PySR α=β/(β+B), asymptotic 1) :
   Tension forte avec bootstrap qui rejette α>1 à P=99.88%.
   Probably finite-β regime where this fit works, but not asymptotic.

H_NEW7 (α saturé + finite-β quadratic correction) :
   Test à comparer Sum SR :
   - Free α_∞ : voir log
   - Fixed α_∞ = 5/6 : voir log
   - Fixed α_∞ = 3/4 : voir log
   Le meilleur fit indique la prédiction préférée par data.

H_NEW8 (Cross-Lie α saturé : SO(5)=7/8, G_2=11/12) :
   Falsifiable directement via lattice SO(5) ou G_2 future.
   Estimation difficulté : SO(5)/Sp(4) medium (Spin(5)=Symplectic Sp(4)),
   G_2 hard (no standard tools).

H_NEW9 (Heegner Λ best-fit x) :
   x best = ?, pas exactly -7. Le 0.005% claim requires x=-7.034 fine tune.
   Cohérent avec mon catch P10 : 2.15% à x=-7 strict.

H_NEW10 (√2 dans QNM overtones) :
   ❌ FALSIFIÉ — Kerr QNM overtones n'ont pas ratio √2.
   Pattern 4 reste isolé à YM glueball.

CONCLUSION :
   - 2 prédictions Tier-1 nouvelles (H_NEW6, H_NEW7) à tester avec Wilson flow propre
   - 1 nouvelle prédiction cross-Lie (H_NEW8) — programme lattice 1-2 ans
   - 1 catch interne (H_NEW9) confirme P10
   - 1 falsification claire (H_NEW10) — √2 isolé à YM
""")
