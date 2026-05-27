#!/usr/bin/env python3
"""Comprehensive analysis of β-scan FAST V3 data.

7 analyses :
1. Bootstrap error bars on c_3D (resample within α samples)
2. Continuum extrapolation a(β) → 0 (1-loop, 2-loop, polynomial)
3. Cross-validation L-out (drop each L, predict from others)
4. Autocorrelation MC time
5. Heatmap visualisation c_3D(β, L)
6. Symbolic forms PySR-style attempts (manual library)
7. Log-corrections fit S_2 = α·A + β·A·log(L) + γ

Author : Kévin Rémondière (ORCID 0009-0008-2443-7166).
"""
import json
import numpy as np
from scipy.optimize import curve_fit
from scipy.stats import linregress

DATA_PATH = '/root/cc-private/papers/2026-05-24-session/data/jax_su2_EE_BETASCAN_results.json'

with open(DATA_PATH) as f:
    data = json.load(f)

results = data['results']
ALPHA_GRID = data['alpha_grid']
BETAS = sorted([float(b) for b in results.keys()])
L_VALUES = sorted([int(L) for L in results[str(BETAS[0])].keys()])

print("=" * 78)
print("SUPER-ANALYSIS β-scan SU(2) 4D BP2008b FAST V3")
print("=" * 78)
print(f"βs : {BETAS}")
print(f"Ls : {L_VALUES}")
print(f"α points: {len(ALPHA_GRID)}")
print()

# Helper : compute c_3D for (β, L)
def c_3D(beta, L):
    r = results[str(beta)][str(L)]
    T_half = r.get('T_half', L)
    A_3D = 2 * L * L * T_half
    return r['S_2'] / A_3D, r.get('S_2_err', 0) / A_3D

# Helper : 1-loop a²(β) for SU(2) Wilson
def a2_1loop(beta):
    g2 = 4.0 / beta
    return g2 * np.exp(-12 * np.pi**2 * beta / 22.0)

# Helper : 2-loop a²(β) for SU(2)
def a2_2loop(beta):
    # b_0 = 22/(48π²), b_1 = ...
    b0 = 22.0 / (48 * np.pi**2)
    b1 = 102.0 / (16 * np.pi**2)**2  # for SU(N)
    g2 = 4.0 / beta
    return g2 * np.exp(-1.0 / (2 * b0 * g2)) * (b0 * g2)**(b1 / (2 * b0**2))


# =============================================================================
# ANALYSIS 1 : BOOTSTRAP ERROR BARS
# =============================================================================
print("\n" + "=" * 78)
print("1. BOOTSTRAP ERROR BARS (resample α samples per (β,L))")
print("=" * 78)
N_BOOT = 1000

print(f"\n{'L':>4} {'β':>5} {'c_3D nominal':>14} {'c_3D bootstrap':>20} {'σ_bootstrap':>14}")
print("-" * 70)
c_3D_bootstrap = {}
for L in L_VALUES:
    c_3D_bootstrap[L] = {}
    for b in BETAS:
        r = results[str(b)][str(L)]
        per_alpha_means = []
        for alpha in r['alpha_grid']:
            samples = r['results_per_alpha'][str(alpha)]['samples']
            per_alpha_means.append(samples)
        # Bootstrap
        boot_S2 = []
        for _ in range(N_BOOT):
            S2_boot = 0
            alphas = r['alpha_grid']
            integrand = []
            for i, alpha in enumerate(alphas):
                s = np.array(per_alpha_means[i])
                boot_samples = np.random.choice(s, size=len(s), replace=True)
                integrand.append(np.mean(boot_samples))
            # Trapezoidal integration
            S2 = np.trapezoid(integrand, alphas)
            boot_S2.append(S2)
        boot_S2 = np.array(boot_S2)
        T_half = r.get('T_half', L)
        A_3D = 2 * L * L * T_half
        c_nom = r['S_2'] / A_3D
        c_boot_mean = boot_S2.mean() / A_3D
        c_boot_std = boot_S2.std() / A_3D
        c_3D_bootstrap[L][b] = (c_boot_mean, c_boot_std)
        print(f"{L:>4} {b:>5.1f} {c_nom:>14.6f} {c_boot_mean:>20.6f} {c_boot_std:>14.6f}")

# =============================================================================
# ANALYSIS 2 : CONTINUUM EXTRAPOLATION a(β) → 0
# =============================================================================
print("\n" + "=" * 78)
print("2. CONTINUUM EXTRAPOLATION (a(β) → 0, multiple models)")
print("=" * 78)

# For each L, fit c_3D(β) using different a(β) models
for L in L_VALUES:
    print(f"\n--- L = {L} ---")
    beta_arr = np.array(BETAS)
    c_arr = np.array([c_3D(b, L)[0] for b in BETAS])
    err_arr = np.array([c_3D_bootstrap[L][b][1] for b in BETAS])

    # Model 1 : linear in β
    slope, intercept, r_val, p_val, std_err = linregress(beta_arr, c_arr)
    print(f"  Linear: c = {slope:.4f}·β + {intercept:.4f} (R²={r_val**2:.4f})")
    print(f"    β→∞ extrap : c → ∞ (linear)")

    # Model 2 : 1/a²(β) 1-loop
    inv_a2 = 1.0 / a2_1loop(beta_arr)
    if inv_a2[0] > 0:
        x = inv_a2 / inv_a2[0]
        try:
            slope2, intercept2, r_val2, _, _ = linregress(x, c_arr)
            print(f"  1/a²(1-loop): c = {slope2:.5f}·[1/a²/1/a²(β=2.3)] + {intercept2:.5f} (R²={r_val2**2:.4f})")
            print(f"    β→∞ extrap : c → ∞ (1/a²)")
            print(f"    a→0 limit isolated sub-leading : {intercept2:.5f}")
        except Exception as e:
            print(f"  1/a² fit failed: {e}")

    # Model 3 : quadratic in β
    try:
        coef = np.polyfit(beta_arr, c_arr, 2)
        print(f"  Quadratic: c = {coef[0]:.4f}·β² + {coef[1]:.4f}·β + {coef[2]:.4f}")
        # Extrapolate to β = 3.0, 4.0, ...
        for b_ext in [2.7, 3.0, 4.0]:
            c_ext = coef[0]*b_ext**2 + coef[1]*b_ext + coef[2]
            print(f"    β={b_ext}: c → {c_ext:.4f}")
    except Exception as e:
        print(f"  Quadratic fit failed: {e}")

# =============================================================================
# ANALYSIS 3 : CROSS-VALIDATION L-OUT
# =============================================================================
print("\n" + "=" * 78)
print("3. CROSS-VALIDATION L-OUT (drop each L, predict from others)")
print("=" * 78)

for L_drop in L_VALUES:
    L_used = [L for L in L_VALUES if L != L_drop]
    print(f"\n--- Drop L={L_drop}, fit from L={L_used} ---")

    pred_errors = []
    for b in BETAS:
        c_used = np.array([c_3D(b, L)[0] for L in L_used])
        c_true = c_3D(b, L_drop)[0]
        # Linear extrapolation in 1/L²
        x = 1.0 / np.array(L_used)**2
        x_target = 1.0 / L_drop**2
        if len(L_used) >= 2:
            slope, intercept, _, _, _ = linregress(x, c_used)
            c_pred = slope * x_target + intercept
            err = (c_pred - c_true) / c_true * 100
            pred_errors.append(abs(err))
            print(f"  β={b}: true={c_true:.4f}, pred={c_pred:.4f}, err={err:.2f}%")
    if pred_errors:
        print(f"  Mean abs error : {np.mean(pred_errors):.2f}%")

# =============================================================================
# ANALYSIS 4 : MC AUTOCORRELATION
# =============================================================================
print("\n" + "=" * 78)
print("4. MC AUTOCORRELATION (within ∂S/∂α samples)")
print("=" * 78)

def autocorr_time(samples, max_lag=10):
    """Estimate integrated autocorrelation time."""
    s = np.array(samples)
    if len(s) < 2 * max_lag:
        max_lag = max(1, len(s) // 4)
    s = s - s.mean()
    var = s.var()
    if var == 0:
        return 1.0
    rho = []
    for lag in range(1, max_lag + 1):
        c = np.mean(s[:-lag] * s[lag:]) / var if lag < len(s) else 0
        rho.append(c)
        if c < 0.1:
            break
    tau = 1 + 2 * sum(max(0, r) for r in rho)
    return tau

print(f"\n{'L':>4} {'β':>5} {'α=0.0 τ':>8} {'α=0.5 τ':>8} {'α=1.0 τ':>8}")
print("-" * 45)
for L in L_VALUES:
    for b in BETAS:
        r = results[str(b)][str(L)]
        tau_0 = autocorr_time(r['results_per_alpha']['0.0']['samples'])
        tau_5 = autocorr_time(r['results_per_alpha']['0.5']['samples'])
        tau_1 = autocorr_time(r['results_per_alpha']['1.0']['samples'])
        print(f"{L:>4} {b:>5.1f} {tau_0:>8.2f} {tau_5:>8.2f} {tau_1:>8.2f}")

# =============================================================================
# ANALYSIS 5 : LOG-CORRECTIONS FIT
# =============================================================================
print("\n" + "=" * 78)
print("5. LOG-CORRECTIONS FIT : S_2 = A·V + B·V·log(L) + C")
print("=" * 78)
print("Test if there's a sub-leading log(L) correction beyond linear in L³")

# Build data
L_data = []
beta_data = []
S2_data = []
A3D_data = []
for L in L_VALUES:
    for b in BETAS:
        r = results[str(b)][str(L)]
        T_half = r.get('T_half', L)
        A_3D = 2 * L * L * T_half
        L_data.append(L)
        beta_data.append(b)
        S2_data.append(r['S_2'])
        A3D_data.append(A_3D)
L_data = np.array(L_data)
beta_data = np.array(beta_data)
S2_data = np.array(S2_data)
A3D_data = np.array(A3D_data)

# Fit S_2 = (a + b·β) · V + c · V · log(L) + d (per β-slot)
def model_log(X, a, b, c, d):
    L_, V_, beta_ = X
    return (a + b * beta_) * V_ + c * V_ * np.log(L_) + d

try:
    popt, pcov = curve_fit(model_log, (L_data, A3D_data, beta_data), S2_data,
                            p0=[0.1, 0.05, 0.001, 0.0])
    perr = np.sqrt(np.diag(pcov))
    print(f"  S_2 = ({popt[0]:.4f}(±{perr[0]:.4f}) + {popt[1]:.4f}(±{perr[1]:.4f})·β)·V")
    print(f"        + {popt[2]:.6f}(±{perr[2]:.6f})·V·log(L) + {popt[3]:.4f}(±{perr[3]:.4f})")
    print(f"  Log(L) coefficient relative size: {popt[2]:.4f} vs main {popt[0]:.4f} → {abs(popt[2]/popt[0])*100:.1f}%")
except Exception as e:
    print(f"  Log fit failed: {e}")

# =============================================================================
# ANALYSIS 6 : SYMBOLIC LIBRARY (manual PySR-style)
# =============================================================================
print("\n" + "=" * 78)
print("6. SYMBOLIC LIBRARY SEARCH (manual exhaustive on 12 c_3D points)")
print("=" * 78)
print("Look for closed-form c_3D(β, L) = f(β) · g(L)")

# Try simple forms
print(f"\nReference: log(3)/(2π√2) = {np.log(3)/(2*np.pi*np.sqrt(2)):.6f}")

print(f"\nFit c_3D = a + b·β at each L:")
for L in L_VALUES:
    c_arr = np.array([c_3D(b, L)[0] for b in BETAS])
    slope, intercept, r2, _, _ = linregress(BETAS, c_arr)
    print(f"  L={L}: c = {slope:.4f}·β + {intercept:.4f}, R²={r2**2:.4f}")

print(f"\nFit c_3D = a·g²(β) + b avec g² = 4/β:")
for L in L_VALUES:
    c_arr = np.array([c_3D(b, L)[0] for b in BETAS])
    g2 = 4.0 / np.array(BETAS)
    slope, intercept, r2, _, _ = linregress(g2, c_arr)
    print(f"  L={L}: c = {slope:.4f}/β·4 + {intercept:.4f}, R²={r2**2:.4f}")
    print(f"    Sign of slope (decreasing in g²?): {'NEG' if slope < 0 else 'POS'}")

# Bigger search : c_3D(β, L) = α·β + γ·log(L)
print(f"\nGlobal fit c_3D = a + b·β + c·log(L):")
def model_global(X, a, b, c):
    beta_, L_ = X
    return a + b * beta_ + c * np.log(L_)

beta_global = []
L_global = []
c_global = []
for L in L_VALUES:
    for b in BETAS:
        beta_global.append(b)
        L_global.append(L)
        c_global.append(c_3D(b, L)[0])
beta_global = np.array(beta_global)
L_global = np.array(L_global)
c_global = np.array(c_global)

popt_g, _ = curve_fit(model_global, (beta_global, L_global), c_global, p0=[0, 0.1, 0])
print(f"  c = {popt_g[0]:.4f} + {popt_g[1]:.4f}·β + {popt_g[2]:.4f}·log(L)")
preds = model_global((beta_global, L_global), *popt_g)
residuals = c_global - preds
print(f"  Residuals std: {residuals.std():.6f}")
print(f"  Largest residual: {residuals[np.argmax(np.abs(residuals))]:.6f} at (β={beta_global[np.argmax(np.abs(residuals))]}, L={L_global[np.argmax(np.abs(residuals))]})")

# =============================================================================
# ANALYSIS 7 : HEATMAP TEXT VISUALISATION
# =============================================================================
print("\n" + "=" * 78)
print("7. HEATMAP c_3D(β, L) — text visualisation")
print("=" * 78)

print(f"\n{'L':>4} ", end='')
for b in BETAS:
    print(f"β={b:<4.1f}    ", end='')
print()
for L in L_VALUES:
    print(f"{L:>4} ", end='')
    for b in BETAS:
        c, _ = c_3D(b, L)
        # ASCII intensity
        normalized = (c - 0.105) / (0.145 - 0.105)
        n_chars = max(0, min(10, int(normalized * 10)))
        bar = "█" * n_chars + " " * (10 - n_chars)
        print(f"{bar} ", end='')
    print()

# Save full analysis as JSON
analysis_results = {
    'bootstrap': {str(L): {str(b): list(c_3D_bootstrap[L][b]) for b in BETAS} for L in L_VALUES},
    'continuum_models': "see log",
    'cross_validation': "see log",
    'autocorrelation_means': "see log",
    'log_corrections_fit': popt.tolist() if 'popt' in dir() else [],
    'global_fit': popt_g.tolist(),
}
with open('/root/cc-private/papers/2026-05-24-session/data/super_analysis_betascan.json', 'w') as f:
    json.dump(analysis_results, f, indent=2)

print("\n" + "=" * 78)
print(f"All analyses complete. Saved to data/super_analysis_betascan.json")
print("=" * 78)
