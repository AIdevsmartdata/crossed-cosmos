#!/usr/bin/env python3
"""PySR mega-run : κ_EE(N) cross-groupe + c(L) finite-size.

Data observables :
- κ(SU(2)) = c(L)/L plateau = 0.5065 ± 0.010 (L=4..12 β=2.4)
- κ(SU(3)) = c(L)/L plateau ≈ 0.601 ± 0.010 (L=4..12 β=5.4 matched 't Hooft)

Theoretical hypotheses to discriminate :
  H1 ECI strict     : κ = 1/(2|Φ⁺|) = 1/(N(N-1))     → SU(2)=0.5, SU(3)=0.167
  H2 ECI alt        : κ = 1/|Φ⁺| = 2/(N(N-1))         → SU(2)=1.0, SU(3)=0.333
  H3 BH universel   : κ = 1/4 const                    → SU(2)=0.25, SU(3)=0.25
  H4 sqrt(N)        : κ = A·sqrt(N)                    → SU(2)=A√2, SU(3)=A√3, ratio 1.225
  H5 log(N²-1)      : κ = A·log(N²-1)                  → SU(2)=A·log3, SU(3)=A·log8
  H6 sqrt(N²-1)     : κ = A·sqrt(N²-1)                 → SU(2)=A√3, SU(3)=A√8

Author : Kévin Rémondière (ORCID 0009-0008-2443-7166).
"""
import numpy as np

# ============================================================================
# Dataset assembled from session 2026-05-25 BP2008b post-fix runs
# ============================================================================

# c(L) per N, β=2.4 SU(2), β=5.4 SU(3) (matched 't Hooft λ=10/3)
# Sign-corrected (|c| reported)
data = {
    # (N, L, β) : (|c|, err)
    (2, 4,  2.4) : (2.0457, 0.0627),
    (2, 6,  2.4) : (3.0104, 0.0590),
    (2, 8,  2.4) : (4.0902, 0.0631),
    (2, 10, 2.4) : (5.0892, 0.0600),
    (2, 12, 2.4) : (6.0660, 0.0666),
    (3, 4,  5.4) : (2.3721, 0.0574),
    (3, 6,  5.4) : (3.7588, 0.0537),
    (3, 8,  5.4) : (4.8104, 0.0496),
    (3, 10, 5.4) : (6.0594, 0.0622),
    (3, 12, 5.4) : (7.2113, 0.0620),
}

# Convert to arrays for PySR
N_vals = []
L_vals = []
beta_vals = []
c_vals = []
err_vals = []
for (N, L, beta), (c, err) in data.items():
    N_vals.append(N)
    L_vals.append(L)
    beta_vals.append(beta)
    c_vals.append(c)
    err_vals.append(err)

N_arr = np.array(N_vals)
L_arr = np.array(L_vals)
beta_arr = np.array(beta_vals)
c_arr = np.array(c_vals)
err_arr = np.array(err_vals)

# Compute κ = c/L per row (the leading area-law coefficient)
kappa_arr = c_arr / L_arr
kappa_err_arr = err_arr / L_arr

print("Dataset cross-N κ_EE :")
print(f"{'N':>2} {'L':>3} {'β':>5} {'|c|':>8} {'κ=c/L':>8} {'err':>8}")
for N, L, b, c, k, e in zip(N_vals, L_vals, beta_vals, c_vals, kappa_arr, kappa_err_arr):
    print(f"{N:>2} {L:>3} {b:>5.2f} {c:>8.4f} {k:>8.4f} {e:>8.4f}")

# κ(N) plateau per N (averaging L=8..12)
print("\nκ(N) plateau (L=8..12 average) :")
for N_target in [2, 3]:
    mask = (N_arr == N_target) & (L_arr >= 8)
    if mask.sum() > 0:
        k_mean = np.average(kappa_arr[mask], weights=1/kappa_err_arr[mask]**2)
        k_sem = 1/np.sqrt(np.sum(1/kappa_err_arr[mask]**2))
        print(f"  SU({N_target}) : κ = {k_mean:.4f} ± {k_sem:.4f}")

# ============================================================================
# Closed-form predictions tested manually
# ============================================================================

print("\n=== Manual closed-form predictions vs measured κ(L=8..12 mean) ===")
kappa_SU2 = np.average(kappa_arr[N_arr==2], weights=1/kappa_err_arr[N_arr==2]**2)
kappa_SU3 = np.average(kappa_arr[N_arr==3], weights=1/kappa_err_arr[N_arr==3]**2)

predictions = {
    "ECI κ=1/(2|Φ⁺|)=1/(N(N-1))" : lambda N: 1.0/(N*(N-1)),
    "ECI κ=1/|Φ⁺|=2/(N(N-1))"   : lambda N: 2.0/(N*(N-1)),
    "BH universel κ=1/4"          : lambda N: 0.25,
    "√N scaling κ=A·√N (A fixed at SU(2))" : lambda N: kappa_SU2 * np.sqrt(N/2),
    "log(N²-1) κ=A·log(N²-1)"    : lambda N: kappa_SU2 * np.log(N**2-1)/np.log(3),
    "√(N²-1) κ=A·√(N²-1)"        : lambda N: kappa_SU2 * np.sqrt((N**2-1)/3),
    "(N²-1)/N² κ=A·(N²-1)/N²"    : lambda N: kappa_SU2 * ((N**2-1)/N**2) / (3/4),
    "1/log(N) κ=A/log(N)"         : lambda N: kappa_SU2 * np.log(2)/np.log(N),
    "exp(-1/N)"                   : lambda N: kappa_SU2 * np.exp(-1/N + 1/2),
}

print(f"\n{'Formula':<40} {'SU(2) pred':>12} {'SU(3) pred':>12} {'SU(3) ratio':>14} {'Match SU(3)?':>15}")
print("-"*100)
for name, fn in predictions.items():
    p2 = fn(2)
    p3 = fn(3)
    ratio = p3/p2
    deviation = abs(kappa_SU3 - p3) / kappa_err_arr[N_arr==3].mean()
    match = "✓" if deviation < 2 else ("⚠" if deviation < 5 else "✗")
    print(f"{name:<40} {p2:>12.4f} {p3:>12.4f} {ratio:>14.4f} {match:>3} ({deviation:.1f}σ)")

print(f"\nMeasured : SU(2)={kappa_SU2:.4f}, SU(3)={kappa_SU3:.4f}, ratio={kappa_SU3/kappa_SU2:.4f}")

# ============================================================================
# PySR symbolic regression
# ============================================================================

try:
    from pysr import PySRRegressor
    print("\n=== PySR symbolic regression : κ = f(N) ===")
    print("Using L=8..12 plateau values for both SU(2) and SU(3)...")

    # Average per N (plateau)
    Ns = []
    ks = []
    es = []
    for N_target in [2, 3]:
        mask = (N_arr == N_target) & (L_arr >= 8)
        Ns.append(N_target)
        ks.append(np.average(kappa_arr[mask], weights=1/kappa_err_arr[mask]**2))
        es.append(1/np.sqrt(np.sum(1/kappa_err_arr[mask]**2)))

    X = np.array(Ns).reshape(-1, 1).astype(float)
    y = np.array(ks)

    model = PySRRegressor(
        niterations=80,
        binary_operators=["+", "-", "*", "/", "^"],
        unary_operators=["sqrt", "log", "exp", "inv(x)=1/x"],
        extra_sympy_mappings={"inv": lambda x: 1/x},
        model_selection="best",
        progress=False,
        verbosity=0,
        random_state=42,
        deterministic=True,
        parallelism="serial",  # avoid issues
    )
    model.fit(X, y, variable_names=["N"])
    print(model)
    print("\nBest formula : ", model.sympy())
except ImportError:
    print("\n[PySR not available — manual analysis only]")
except Exception as e:
    print(f"\n[PySR error : {e}]")

# ============================================================================
# Joint c(L, N) fit
# ============================================================================

try:
    from pysr import PySRRegressor
    print("\n=== PySR joint fit : c = f(L, N) ===")
    print("Using ALL 10 datapoints (L=4..12, N=2,3)")

    X = np.column_stack([L_arr.astype(float), N_arr.astype(float)])
    y = c_arr

    model2 = PySRRegressor(
        niterations=100,
        binary_operators=["+", "-", "*", "/", "^"],
        unary_operators=["sqrt", "log", "exp"],
        model_selection="best",
        progress=False,
        verbosity=0,
        random_state=42,
        deterministic=True,
        parallelism="serial",
    )
    model2.fit(X, y, variable_names=["L", "N"])
    print(model2)
    print("\nBest formula c(L,N) :", model2.sympy())
except Exception as e:
    print(f"\n[PySR joint fit error : {e}]")

print("\nDONE.")
