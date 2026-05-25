#!/usr/bin/env python3
"""Mega calc hypothèses parallèles pendant SU(3)/SU(4) GPU running.

5 hypothèses testées :
  1. Sub-leading C(SU(N)) cross-N pattern
  2. κ/σ ratio universel Wilson V6 + BP2008b
  3. Continued fractions κ_∞ = 0.6776 → fraction simple
  4. Finite-size c(L) corrections (1/L², log(L)/L)
  5. Recherche systématique candidats κ_∞

Author : Kévin Rémondière (ORCID 0009-0008-2443-7166).
"""
import numpy as np
import json

print("="*78)
print("MEGA CALC HYPOTHÈSES — 2026-05-25 evening")
print("="*78)


# ============================================================================
# Data assembly
# ============================================================================

# BP2008b post-fix κ(N) plateaus
kappa_data = {2: (0.5080, 0.0036), 3: (0.6025, 0.0033)}
kappa_inf_measured = 0.67761
kappa_inf_err = 0.00297

# BP2008b post-fix c(L) data
c_data = {
    (2, 4): (2.0457, 0.0627),
    (2, 6): (3.0104, 0.0590),
    (2, 8): (4.0902, 0.0631),
    (2, 10): (5.0892, 0.0600),
    (2, 12): (6.0660, 0.0666),
    (3, 4): (2.3721, 0.0574),
    (3, 6): (3.7588, 0.0537),
    (3, 8): (4.8104, 0.0496),
    (3, 10): (6.0594, 0.0622),
    (3, 12): (7.2113, 0.0620),
}

# Wilson V6 σ_lat data (SU(2) β-scan, from R=4 plateau)
wilson_sigma = {
    2.3: (0.16078, 0.00860),
    2.4: (0.10288, 0.00340),
    2.5: (0.06144, 0.00164),
    2.6: (0.04579, 0.00110),
    2.7: (0.03894, 0.00076),
}

# ============================================================================
# Hypothesis 1 : Finite-size c(L) corrections
# ============================================================================

print("\n" + "="*78)
print("H1 : Finite-size c(L) = κ·L + b + a/L corrections")
print("="*78)

from scipy.optimize import curve_fit

for Nc in [2, 3]:
    Ls = np.array([L for (N, L) in c_data if N == Nc])
    cs = np.array([c_data[(Nc, L)][0] for L in Ls])
    es = np.array([c_data[(Nc, L)][1] for L in Ls])

    # Linear : c = a·L + b
    def linear(L, a, b):
        return a*L + b
    popt, pcov = curve_fit(linear, Ls, cs, sigma=es, absolute_sigma=True)
    a_lin, b_lin = popt
    chi2_lin = np.sum(((cs - linear(Ls, *popt))/es)**2)

    # Linear + 1/L : c = κ·L + b + d/L
    def linear_inv(L, kappa, b, d):
        return kappa*L + b + d/L
    try:
        popt2, pcov2 = curve_fit(linear_inv, Ls, cs, sigma=es, absolute_sigma=True,
                                  p0=[0.5, 0, 0])
        chi2_inv = np.sum(((cs - linear_inv(Ls, *popt2))/es)**2)
        print(f"\n  SU({Nc}) linear        : κ={a_lin:.5f}±{np.sqrt(pcov[0,0]):.5f}, "
              f"b={b_lin:.4f}±{np.sqrt(pcov[1,1]):.4f}, χ²/dof = {chi2_lin:.2f}/{len(Ls)-2}")
        print(f"  SU({Nc}) linear + d/L : κ={popt2[0]:.5f}±{np.sqrt(pcov2[0,0]):.5f}, "
              f"b={popt2[1]:.4f}, d={popt2[2]:.4f}, χ²/dof = {chi2_inv:.2f}/{len(Ls)-3}")
        # Log L correction
        def linear_log(L, kappa, b, d):
            return kappa*L + b + d*np.log(L)
        popt3, pcov3 = curve_fit(linear_log, Ls, cs, sigma=es, absolute_sigma=True,
                                  p0=[0.5, 0, 0])
        chi2_log = np.sum(((cs - linear_log(Ls, *popt3))/es)**2)
        print(f"  SU({Nc}) linear + d·log L : κ={popt3[0]:.5f}±{np.sqrt(pcov3[0,0]):.5f}, "
              f"b={popt3[1]:.4f}, d={popt3[2]:.4f}, χ²/dof = {chi2_log:.2f}/{len(Ls)-3}")
    except Exception as e:
        print(f"  Fit error: {e}")


# ============================================================================
# Hypothesis 2 : Wilson σ_lat fit β-dependence + κ/σ ratio
# ============================================================================

print("\n" + "="*78)
print("H2 : Wilson σ_lat SU(2) β-dep + κ/σ ratio")
print("="*78)

# Fit σ_lat(β) = A · exp(-c·β) (asymptotic freedom 1-loop expectation)
betas = np.array(sorted(wilson_sigma.keys()))
sigmas = np.array([wilson_sigma[b][0] for b in betas])
sig_errs = np.array([wilson_sigma[b][1] for b in betas])

def exp_decay(b, A, c):
    return A * np.exp(-c*b)
popt, pcov = curve_fit(exp_decay, betas, sigmas, sigma=sig_errs, absolute_sigma=True,
                        p0=[100, 3.5])
print(f"\nFit σ_lat(β) = A·exp(-c·β):")
print(f"  A = {popt[0]:.3e} ± {np.sqrt(pcov[0,0]):.2e}")
print(f"  c = {popt[1]:.4f} ± {np.sqrt(pcov[1,1]):.4f}")
print(f"  1-loop expect c = 12π²/22 ≈ {12*np.pi**2/22:.4f}")

# κ_EE(SU(2)) / σ_lat at β=2.4
sigma_at_24 = wilson_sigma[2.4][0]
kappa_at_24 = kappa_data[2][0]
ratio = kappa_at_24 / sigma_at_24
ratio_err = np.sqrt((kappa_data[2][1]/sigma_at_24)**2 + (kappa_at_24*wilson_sigma[2.4][1]/sigma_at_24**2)**2)
print(f"\nκ(SU(2))/σ_lat(β=2.4) = {ratio:.3f} ± {ratio_err:.3f}")
print(f"  (Dimensional analysis : κ_EE per |∂A|_3D / σ_lat per a² → different units)")


# ============================================================================
# Hypothesis 3 : Continued fractions κ_∞ = 0.6776
# ============================================================================

print("\n" + "="*78)
print("H3 : Continued fractions κ_∞ ≈ 0.67761")
print("="*78)

def continued_fraction(x, max_terms=10):
    cf = []
    for _ in range(max_terms):
        a = int(np.floor(x))
        cf.append(a)
        x = x - a
        if abs(x) < 1e-12:
            break
        x = 1.0 / x
    return cf

def cf_to_rational(cf):
    """Convert continued fraction to p/q."""
    if len(cf) == 1:
        return cf[0], 1
    p_prev, q_prev = 1, 0
    p, q = cf[0], 1
    for a in cf[1:]:
        p_new = a*p + p_prev
        q_new = a*q + q_prev
        p_prev, q_prev = p, q
        p, q = p_new, q_new
    return p, q

cf = continued_fraction(kappa_inf_measured, max_terms=15)
print(f"\nκ_∞ = {kappa_inf_measured:.7f}")
print(f"Continued fraction : {cf[:10]}")
print(f"\nConvergents (rational approximations) :")
for i in range(2, min(8, len(cf)+1)):
    p, q = cf_to_rational(cf[:i])
    val = p/q
    err = abs(val - kappa_inf_measured)
    print(f"  {p}/{q} = {val:.7f}  Δ = {err:.2e}  ({err/kappa_inf_measured*100:.3f}%)")


# ============================================================================
# Hypothesis 5 : Systematic search candidates κ_∞
# ============================================================================

print("\n" + "="*78)
print("H5 : Systematic search constants candidates for κ_∞")
print("="*78)

import math
candidates = {
    # Simple fractions
    "2/3":              2/3,
    "11/16":            11/16,
    "27/40":            27/40,
    "16/23":            16/23,
    "9/13":             9/13,
    # Logarithms
    "ln(2)":            math.log(2),
    "ln(3)/ln(e^π)":    math.log(3)/math.pi,  # = ln(3)/π
    "log10(5)":         math.log10(5),
    "log10(e^2)":       2*math.log10(math.e),
    "ln(5/2)":          math.log(5/2),
    # π combinations
    "1 - 1/π":          1 - 1/math.pi,
    "(π-1)/π":          (math.pi-1)/math.pi,
    "π/(π+1.5)":        math.pi/(math.pi+1.5),
    "2/(π-1.05)":       2/(math.pi-1.05),
    "π^2/(π^2+6)":      math.pi**2/(math.pi**2+6),
    "log(π)/log(2π)":   math.log(math.pi)/math.log(2*math.pi),
    # e combinations
    "1 - 1/e":          1 - 1/math.e,
    "1 - 1/(e+1)":      1 - 1/(math.e+1),
    "ln(2)/ln(e)":      math.log(2),  # same as above
    "(e-1)/e":          (math.e-1)/math.e,  # = 1-1/e
    # Sqrt
    "sqrt(15)/(2π)":    math.sqrt(15)/(2*math.pi),
    "sqrt(2)/(1+sqrt(2)/2)": math.sqrt(2)/(1+math.sqrt(2)/2),
    "1/sqrt(2.18)":     1/math.sqrt(2.18),
    # Combinations
    "1 - 1/π + 1/π²":   1 - 1/math.pi + 1/math.pi**2,
    "1 - ln(2)/π":      1 - math.log(2)/math.pi,
    "ln(2)·π/3.16":     math.log(2)*math.pi/3.16,
    "(π+1)/(π+2)":      (math.pi+1)/(math.pi+2),
    "π/(π+sqrt(2.1))":  math.pi/(math.pi+math.sqrt(2.1)),
    # Catalan, Apery
    "Catalan/sqrt(2)":  0.9159655942/math.sqrt(2),  # ≈ 0.6476
    "Apery/sqrt(π)":    1.2020569032/math.sqrt(math.pi),  # ≈ 0.6781
    "Euler-Mascheroni·(1+φ)": 0.5772156649*(1+(1+math.sqrt(5))/2),
    # Physical constants
    "α_fine·1000":      7.2973525693e-3 * 1000,
}

print(f"\nκ_∞ measured = {kappa_inf_measured:.5f} ± {kappa_inf_err:.5f}\n")
matches = []
for name, val in candidates.items():
    dev = abs(val - kappa_inf_measured)
    dev_sigma = dev / kappa_inf_err
    matches.append((dev_sigma, name, val, dev))

matches.sort()
print(f"{'Candidate':<40} {'Value':>12} {'|Δ|':>10} {'σ':>6}")
print("-"*80)
for dev_s, name, val, dev in matches[:12]:
    marker = "★★★" if dev_s < 1 else ("★★" if dev_s < 2 else ("★" if dev_s < 5 else ""))
    print(f"{name:<40} {val:>12.5f} {dev:>10.5f} {dev_s:>6.2f}σ  {marker}")


# ============================================================================
# Hypothesis 4 : Sub-leading C(N) extraction
# ============================================================================

print("\n" + "="*78)
print("H4 : Sub-leading C extraction from c(L) intercept")
print("="*78)

# Refit c(L) = κ·L + C·log(L) + b finite-size to extract sub-leading
from scipy.optimize import curve_fit

for Nc in [2, 3]:
    Ls = np.array([L for (N, L) in c_data if N == Nc])
    cs = np.array([c_data[(Nc, L)][0] for L in Ls])
    es = np.array([c_data[(Nc, L)][1] for L in Ls])

    def full_model(L, kappa, C, const):
        return kappa*L + C*np.log(L) + const
    try:
        popt, pcov = curve_fit(full_model, Ls, cs, sigma=es, absolute_sigma=True,
                                p0=[0.5, 0.1, 0])
        chi2 = np.sum(((cs - full_model(Ls, *popt))/es)**2)
        print(f"\n  SU({Nc}) c(L) = κ·L + C·log(L) + const:")
        print(f"    κ = {popt[0]:.5f} ± {np.sqrt(pcov[0,0]):.5f}")
        print(f"    C (sub-leading) = {popt[1]:.5f} ± {np.sqrt(pcov[1,1]):.5f}")
        print(f"    const = {popt[2]:.5f} ± {np.sqrt(pcov[2,2]):.5f}")
        print(f"    χ²/dof = {chi2:.2f}/{len(Ls)-3}")
    except Exception as e:
        print(f"  Fit error: {e}")

print("\nReference predictions C(SU(2)) :")
print(f"  log(3)/(2π√2) = {np.log(3)/(2*np.pi*np.sqrt(2)):.5f}")
print(f"  log(3)/(2π) = {np.log(3)/(2*np.pi):.5f}")
print(f"  Rabenstein 2019 SU(2) C ≈ 0.054 (CFT)")


# ============================================================================
# Save results
# ============================================================================

import json
results = {
    "session": "2026-05-25 evening mega calc",
    "kappa_inf_measured": kappa_inf_measured,
    "kappa_inf_err": kappa_inf_err,
    "best_candidates_kappa_inf": [
        {"name": name, "value": float(val), "deviation_sigma": float(dev_s)}
        for dev_s, name, val, dev in matches[:5]
    ],
    "data": {
        "kappa_plateaus": {str(N): list(kappa_data[N]) for N in kappa_data},
        "c_data": {f"{N}_{L}": list(c_data[(N,L)]) for (N,L) in c_data},
        "wilson_sigma": {str(b): list(wilson_sigma[b]) for b in wilson_sigma},
    },
}
with open("/tmp/hypothesis_megacalc_results.json", "w") as f:
    json.dump(results, f, indent=2)
print(f"\nResults saved : /tmp/hypothesis_megacalc_results.json")
print("\nDONE.")
