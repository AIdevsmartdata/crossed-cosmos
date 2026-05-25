#!/usr/bin/env python3
"""PySR v2 — κ_EE cross-N symbolic regression, enriched dataset.

Dataset enrichi 2026-05-25 :
- BP2008b SU(2) post-fix L=4..12 β=2.4 (5 points)
- BP2008b SU(3) post-fix L=4..12 β=5.4 (5 points)
- Wilson V6 σ_lat SU(2) β=2.3..2.7 (5 points, different observable)
- BP2008b pre-fix SU(2) historical c values (5 points, β=2.4)

Target : trouver κ(N, L) ou κ(N) qui ajuste tout simultanément.

Author : Kévin Rémondière (ORCID 0009-0008-2443-7166).
"""
import numpy as np
import json
import os


# ============================================================================
# Dataset assembly
# ============================================================================

# BP2008b post-fix data (sign-corrected |c|)
bp_postfix = [
    # (Nc, L, beta, |c|, err)
    (2, 4,  2.4, 2.0457, 0.0627),
    (2, 6,  2.4, 3.0104, 0.0590),
    (2, 8,  2.4, 4.0902, 0.0631),
    (2, 10, 2.4, 5.0892, 0.0600),
    (2, 12, 2.4, 6.0660, 0.0666),
    (3, 4,  5.4, 2.3721, 0.0574),
    (3, 6,  5.4, 3.7588, 0.0537),
    (3, 8,  5.4, 4.8104, 0.0496),
    (3, 10, 5.4, 6.0594, 0.0622),
    (3, 12, 5.4, 7.2113, 0.0620),
]

Nc_arr = np.array([d[0] for d in bp_postfix], dtype=float)
L_arr = np.array([d[1] for d in bp_postfix], dtype=float)
beta_arr = np.array([d[2] for d in bp_postfix], dtype=float)
c_arr = np.array([d[3] for d in bp_postfix])
err_arr = np.array([d[4] for d in bp_postfix])
kappa_arr = c_arr / L_arr
kappa_err_arr = err_arr / L_arr

print("=" * 78)
print("Dataset BP2008b post-fix : c = κ·L per (Nc, L)")
print("=" * 78)
print(f"{'Nc':>3} {'L':>3} {'β':>5} {'|c|':>8} {'κ=c/L':>10} {'err':>8}")
for i in range(len(bp_postfix)):
    print(f"{Nc_arr[i]:>3.0f} {L_arr[i]:>3.0f} {beta_arr[i]:>5.2f} "
          f"{c_arr[i]:>8.4f} {kappa_arr[i]:>10.5f} {kappa_err_arr[i]:>8.5f}")

# Plateau κ per Nc (L ≥ 8)
kappa_plateaus = {}
for Nc in [2, 3]:
    mask = (Nc_arr == Nc) & (L_arr >= 8)
    w = 1.0 / kappa_err_arr[mask]**2
    k_mean = np.sum(w * kappa_arr[mask]) / np.sum(w)
    k_err = 1.0 / np.sqrt(np.sum(w))
    kappa_plateaus[Nc] = (k_mean, k_err)
    print(f"\nκ(SU({Nc})) plateau = {k_mean:.5f} ± {k_err:.5f}")


# ============================================================================
# Comprehensive χ² test of candidate formulas (analytical, no PySR needed)
# ============================================================================

print("\n" + "=" * 78)
print("Candidate formulas χ² fit (1 parameter A, fit to 2 plateau points)")
print("=" * 78)

k2_mean, k2_err = kappa_plateaus[2]
k3_mean, k3_err = kappa_plateaus[3]

candidates = [
    # (name, formula(Nc, A), A0_guess)
    ("κ = A · (1 - 1/Nc²)",     lambda Nc, A: A * (1 - 1.0/Nc**2),               0.68),
    ("κ = A · sqrt(Nc)",         lambda Nc, A: A * np.sqrt(Nc),                   0.36),
    ("κ = A constant",           lambda Nc, A: A * np.ones_like(Nc),              0.55),
    ("κ = A · (Nc-1)/Nc",        lambda Nc, A: A * (Nc-1)/Nc,                     1.02),
    ("κ = A · log(Nc)/log(2)",  lambda Nc, A: A * np.log(Nc)/np.log(2),         0.51),
    ("κ = A · (Nc²-1)/(Nc²+1)", lambda Nc, A: A * (Nc**2-1)/(Nc**2+1),           0.847),
    ("κ = A · exp(-1/Nc)",       lambda Nc, A: A * np.exp(-1/Nc),                 0.838),
    ("κ = A · tanh(Nc/2)",       lambda Nc, A: A * np.tanh(Nc/2),                 0.527),
    ("κ = A · sin(π·Nc/4)",      lambda Nc, A: A * np.sin(np.pi*Nc/4),            0.508),
    ("κ = A · log(Nc²+1)",       lambda Nc, A: A * np.log(Nc**2+1),               0.317),
    ("κ = A · (1 - 1/(2Nc))",   lambda Nc, A: A * (1 - 1.0/(2*Nc)),              0.676),
    ("κ = A · arctan(Nc)/(π/2)",lambda Nc, A: A * np.arctan(Nc)/(np.pi/2),       0.687),
    ("κ = A · (1 - Nc^{-1.5})",  lambda Nc, A: A * (1 - Nc**(-1.5)),             0.768),
    ("κ = A · Nc^{0.275}",       lambda Nc, A: A * Nc**0.275,                     0.420),
]

print(f"\n{'Formula':<35} {'A_fit':>10} {'SU(2) pred':>12} {'SU(3) pred':>12} "
      f"{'Δσ(SU3)':>10} {'χ²':>8}")
print("-" * 100)

best_formulas = []
for name, fn, A0 in candidates:
    # Fit A by least-squares to 2 plateaus weighted by err
    from scipy.optimize import minimize_scalar
    def chi2(A):
        p2 = fn(np.array([2.0]), A)[0]
        p3 = fn(np.array([3.0]), A)[0]
        return ((p2 - k2_mean)/k2_err)**2 + ((p3 - k3_mean)/k3_err)**2
    result = minimize_scalar(chi2, bracket=(A0/2, A0*2))
    A_fit = result.x
    chi2_min = result.fun
    p2 = fn(np.array([2.0]), A_fit)[0]
    p3 = fn(np.array([3.0]), A_fit)[0]
    dev3 = abs(k3_mean - p3) / k3_err
    print(f"{name:<35} {A_fit:>10.4f} {p2:>12.5f} {p3:>12.5f} "
          f"{dev3:>10.2f} {chi2_min:>8.3f}")
    best_formulas.append((chi2_min, name, A_fit, p2, p3))

best_formulas.sort()
print(f"\nTop 5 candidats (lowest χ²) :")
for chi2_v, name, A, p2, p3 in best_formulas[:5]:
    print(f"  {name}  →  A = {A:.4f}, χ²={chi2_v:.3f}")


# ============================================================================
# PySR symbolic regression on (Nc, L) joint c(Nc, L)
# ============================================================================

try:
    from pysr import PySRRegressor
    print("\n" + "=" * 78)
    print("PySR symbolic regression : c = f(Nc, L) on 10 datapoints")
    print("=" * 78)

    X = np.column_stack([Nc_arr, L_arr])
    y = c_arr
    weights = 1.0 / err_arr**2

    model = PySRRegressor(
        niterations=200,
        population_size=60,
        binary_operators=["+", "-", "*", "/"],
        unary_operators=["sqrt", "log", "exp", "square", "neg"],
        model_selection="best",
        progress=False,
        verbosity=0,
        random_state=42,
        deterministic=True,
        parallelism="serial",
        elementwise_loss="loss(x, y, w) = w * (x - y)^2",
        complexity_of_constants=2,
    )
    model.fit(X, y, variable_names=["Nc", "L"], weights=weights)
    print("\nPySR best models :")
    print(model)
    print(f"\nBest equation : {model.sympy()}")
except ImportError:
    print("\n[PySR not available — analytical fit only]")
except Exception as e:
    print(f"\n[PySR error : {e}]")


# ============================================================================
# PySR on κ(Nc) plateau (just 2 points — overfitting alert)
# ============================================================================

try:
    print("\n" + "=" * 78)
    print("PySR on κ(Nc) plateau (2 points, complex formulas overfit)")
    print("=" * 78)

    Nc_plat = np.array([2.0, 3.0]).reshape(-1, 1)
    k_plat = np.array([k2_mean, k3_mean])
    err_plat = np.array([k2_err, k3_err])
    w_plat = 1.0 / err_plat**2

    model_k = PySRRegressor(
        niterations=300,
        population_size=80,
        binary_operators=["+", "-", "*", "/", "^"],
        unary_operators=["sqrt", "log", "exp", "neg", "inv(x)=1/x"],
        extra_sympy_mappings={"inv": lambda x: 1/x},
        model_selection="best",
        progress=False,
        verbosity=0,
        random_state=42,
        deterministic=True,
        parallelism="serial",
        elementwise_loss="loss(x, y, w) = w * (x - y)^2",
        complexity_of_constants=2,
        constraints={"^": (-1, 1)},  # exponent limited
    )
    model_k.fit(Nc_plat, k_plat, variable_names=["Nc"], weights=w_plat)
    print("\nκ(Nc) candidates (Pareto front) :")
    print(model_k)
    print(f"\nBest κ(Nc) : {model_k.sympy()}")
except Exception as e:
    print(f"\n[PySR κ(Nc) error : {e}]")


# ============================================================================
# Fit κ_∞ in (1-1/Nc²)·κ_∞ closure
# ============================================================================

print("\n" + "=" * 78)
print("Refined κ_∞ : (1-1/Nc²)·κ_∞ fit")
print("=" * 78)

# A from each point individually
A_su2 = k2_mean / (1 - 1/4)  # 1 - 1/4 = 3/4
A_su2_err = k2_err / (3/4)
A_su3 = k3_mean / (1 - 1/9)  # 8/9
A_su3_err = k3_err / (8/9)
print(f"  κ_∞ from SU(2) : {A_su2:.5f} ± {A_su2_err:.5f}")
print(f"  κ_∞ from SU(3) : {A_su3:.5f} ± {A_su3_err:.5f}")

# Weighted average
A_w = (A_su2/A_su2_err**2 + A_su3/A_su3_err**2) / (1/A_su2_err**2 + 1/A_su3_err**2)
A_w_err = 1/np.sqrt(1/A_su2_err**2 + 1/A_su3_err**2)
print(f"\n  κ_∞ weighted average : {A_w:.5f} ± {A_w_err:.5f}")

# Comparaison candidats
print(f"\n  Candidats κ_∞ :")
for name, val in [
    ("2/3", 2/3),
    ("1 - 1/π", 1 - 1/np.pi),
    ("ln(2)", np.log(2)),
    ("1 - 1/e", 1 - 1/np.e),
    ("π²/16", np.pi**2/16),
    ("(π-1)/π", (np.pi-1)/np.pi),
    ("sqrt(15)/(2π)", np.sqrt(15)/(2*np.pi)),
    ("4·(2-√3)", 4*(2-np.sqrt(3))),
    ("e/4", np.e/4),
    ("(3-1/π)/√(2π)", (3-1/np.pi)/np.sqrt(2*np.pi)),
    ("0.6779 measured", A_w),
]:
    dev = abs(val - A_w) / A_w_err if A_w_err > 0 else 999
    marker = "★" if dev < 2 else ("⚠" if dev < 5 else "")
    print(f"    {name:<25} = {val:.5f}  Δσ = {dev:>6.2f}  {marker}")


# ============================================================================
# Save dataset for re-use
# ============================================================================

output = {
    "session": "2026-05-25",
    "method": "BP2008b post-fix + cross-N",
    "data": [
        {"Nc": int(d[0]), "L": int(d[1]), "beta": float(d[2]),
         "c": float(d[3]), "c_err": float(d[4]),
         "kappa": float(d[3]/d[1]), "kappa_err": float(d[4]/d[1])}
        for d in bp_postfix
    ],
    "kappa_plateaus": {str(Nc): {"mean": float(v[0]), "err": float(v[1])}
                       for Nc, v in kappa_plateaus.items()},
    "kappa_inf_fit": {"value": float(A_w), "err": float(A_w_err)},
    "candidate_formulas_chi2": [
        {"formula": name, "A_fit": float(A), "chi2": float(chi2_v),
         "SU2_pred": float(p2), "SU3_pred": float(p3)}
        for chi2_v, name, A, p2, p3 in best_formulas
    ]
}

out_path = "/tmp/pysr_kappa_v2_results.json"
with open(out_path, "w") as f:
    json.dump(output, f, indent=2)
print(f"\nResults saved : {out_path}")
print("\nDONE.")
