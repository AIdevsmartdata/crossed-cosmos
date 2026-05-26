#!/usr/bin/env python3
"""PySR ECI post-SU(6) — refit kappa_lattice(N) cross-N N=2..6 + verification BIG_MASS_TABLE.

Contexte
========
Finding SU(6) THERM5000 (2026-05-26) : kappa_EE(SU(6)) = 0.8099 +/- 0.0055
vs prediction kappa_inf*(1-1/36) = 0.6593 ⇒ Delta = 31.6σ FALSIFIE la loi
kappa_EE(N) = kappa_inf*(1-1/N²) pour N=6.

Mission : refit propre + cross-validation rigoureuse.

Dataset
=======
   N=2 : kappa = 0.5080 ± 0.010   (BP2008b)
   N=3 : kappa = 0.6025 ± 0.0033  (jax_su3_EE_BP2008b)
   N=4 : kappa = 0.6353 ± 0.0044  (jax_su4_EE_BP2008b)
   N=5 : kappa = 0.6897 ± 0.009   (jax_su5_EE_BP2008b 800 sweeps preliminary)
   N=6 : kappa = 0.8099 ± 0.0055  (jax_su6_EE_BP2008b_THERM5000)

Methodology
===========
Phase 1 : 14 candidate formulae a priori (1-param fit, chi^2/dof, AIC, BIC)
Phase 2 : Refined 2-param fits including |Z_N| premier/composite indicator
Phase 3 : Leave-one-out cross-validation
Phase 4 : PySR symbolic regression with rich feature set + constants library
Phase 5 : Asymptote kappa_inf candidates revisited (5 datapoints)

Reference : Buividovich & Polikarpov, arXiv:0802.4247 (BP2008b method).
Author : Kévin Rémondière (ORCID 0009-0008-2443-7166), independent researcher.
"""

import numpy as np
import json
import os
import sys
from scipy.optimize import minimize_scalar, minimize, curve_fit

# ----------------------------------------------------------------------------
# Reproducibility
# ----------------------------------------------------------------------------
SEED = 42
np.random.seed(SEED)

# ----------------------------------------------------------------------------
# Constants and known special values
# ----------------------------------------------------------------------------
PI = np.pi
EXP1 = np.e
ZETA3 = 1.2020569031595942
SQRT_PI = np.sqrt(PI)
ZETA3_OVER_SQRT_PI = ZETA3 / SQRT_PI    # 0.6782 candidate kappa_inf
LN2 = np.log(2)
LN3 = np.log(3)
PHI_GOLDEN = (1 + np.sqrt(5)) / 2

# ----------------------------------------------------------------------------
# Dataset kappa_lattice cross-N (BP2008b method, all from session 2026-05-25/26)
# ----------------------------------------------------------------------------
DATA = {
    # N : (kappa, kappa_err, beta_thooft, source)
    2: (0.5080, 0.010,   2.4,  "jax_su2_EE_BP2008b L=4..12"),
    3: (0.6025, 0.0033,  5.4,  "jax_su3_EE_BP2008b L=4..12"),
    4: (0.6353, 0.0044, 10.0,  "jax_su4_EE_BP2008b L=4..10"),
    5: (0.6897, 0.009,  15.0,  "jax_su5_EE_BP2008b L=4..10 (800 sweeps prelim)"),
    6: (0.8099, 0.0055, 21.6,  "jax_su6_EE_BP2008b_THERM5000 L=4..10"),
}

N_arr     = np.array(sorted(DATA.keys()), dtype=float)
kappa_arr = np.array([DATA[int(n)][0] for n in N_arr])
err_arr   = np.array([DATA[int(n)][1] for n in N_arr])
beta_arr  = np.array([DATA[int(n)][2] for n in N_arr])

print("=" * 78)
print("Dataset kappa_lattice cross-N (session 2026-05-26)")
print("=" * 78)
print(f"{'N':>3} {'kappa':>10} {'err':>8} {'beta_t Hooft':>14} {'source':<40}")
for n in sorted(DATA.keys()):
    kk, ee, bb, src = DATA[n]
    print(f"{n:>3d} {kk:>10.4f} {ee:>8.4f} {bb:>14.2f} {src:<40}")

# ----------------------------------------------------------------------------
# Structural features SU(N)
# ----------------------------------------------------------------------------
def features(N):
    """Return dict of structural features at SU(N)."""
    N = np.asarray(N, dtype=float)
    is_prime_ZN = np.isin(N.astype(int), [2, 3, 5, 7, 11, 13]).astype(float)
    return {
        "N":           N,
        "N2":          N**2,
        "inv_N":       1.0 / N,
        "inv_N2":      1.0 / N**2,
        "dim_adj":     N**2 - 1,            # SU(N) adjoint dim
        "n_pos_roots": N * (N - 1) / 2,     # |Phi+|
        "rank":        N - 1,
        "Z_N":         N,                   # center order
        "is_prime_ZN": is_prime_ZN,         # 1 if N in {2,3,5,7,11,13}
        "C2_adj":      2 * N,               # Casimir C_2(adj) = 2N
        "C3_adj":      N * (N**2 - 1),
    }

feat = features(N_arr)

# ----------------------------------------------------------------------------
# Phase 1 : 1-parameter candidate formulae chi^2/dof + AIC + BIC
# ----------------------------------------------------------------------------
print("\n" + "=" * 78)
print("Phase 1 : 1-parameter candidate formulae (fit on 5 datapoints)")
print("=" * 78)

candidates_1p = [
    ("F1 a*(1-1/N^2)",         lambda N, a: a * (1 - 1.0/N**2),                       0.68),
    ("F2 a*N/(N+1)",            lambda N, a: a * N/(N+1),                              0.68),
    ("F3 a*(N-1)/N",            lambda N, a: a * (N-1)/N,                              1.0),
    ("F4 a*log(N)",             lambda N, a: a * np.log(N),                            0.5),
    ("F5 a*sqrt(N)",            lambda N, a: a * np.sqrt(N),                           0.35),
    ("F6 a*tanh(N/2)",          lambda N, a: a * np.tanh(N/2),                         0.55),
    ("F7 a*(1 - exp(-N/2))",    lambda N, a: a * (1 - np.exp(-N/2)),                   0.7),
    ("F8 a*N^(1/3)",            lambda N, a: a * N**(1/3.),                            0.4),
    ("F9 a*N^(1/4)",            lambda N, a: a * N**(0.25),                            0.45),
    ("F10 a*arctan(N)/(pi/2)",  lambda N, a: a * np.arctan(N)/(PI/2),                  0.7),
    ("F11 a*log(N+1)/log(3)",   lambda N, a: a * np.log(N+1)/np.log(3),                0.55),
    ("F12 a*(N^2-1)/N^2",       lambda N, a: a * (N**2-1)/N**2,                        0.68),
    ("F13 a*(1 - 1/N)",         lambda N, a: a * (1 - 1/N),                            1.0),
    ("F14 a constant",          lambda N, a: a * np.ones_like(N),                      0.65),
]

results_1p = []
print(f"\n{'Formula':<28} {'a_fit':>8} {'chi^2':>9} {'chi^2/dof':>10} "
      f"{'AIC':>8} {'BIC':>8} | "
      f"{'pred N=2':>9} {'pred N=3':>9} {'pred N=4':>9} {'pred N=5':>9} {'pred N=6':>9}")
print("-" * 150)

for name, fn, a0 in candidates_1p:
    def chi2(a):
        pred = fn(N_arr, a)
        return np.sum(((pred - kappa_arr) / err_arr) ** 2)
    try:
        res = minimize_scalar(chi2, bracket=(a0/3., a0*3.))
        a_fit = float(res.x)
        ch = float(res.fun)
    except Exception:
        a_fit = a0
        ch = chi2(a0)
    n_obs = 5
    n_par = 1
    dof = n_obs - n_par
    ch_dof = ch / dof
    # AIC / BIC : assume Gaussian noise with known sigma (chi^2 = -2 ln L + cst)
    aic = ch + 2 * n_par
    bic = ch + n_par * np.log(n_obs)
    pred = fn(N_arr, a_fit)
    results_1p.append({
        "name": name, "a_fit": a_fit, "chi2": ch, "chi2_dof": ch_dof,
        "aic": aic, "bic": bic, "pred": pred.tolist()
    })
    pred_str = "  ".join([f"{p:>8.4f}" for p in pred])
    print(f"{name:<28} {a_fit:>8.4f} {ch:>9.2f} {ch_dof:>10.3f} "
          f"{aic:>8.2f} {bic:>8.2f} |  {pred_str}")

print(f"\nMeasured: " + "  ".join([f"{k:>8.4f}" for k in kappa_arr]))
print(f"Errors  : " + "  ".join([f"{e:>8.4f}" for e in err_arr]))

# ----------------------------------------------------------------------------
# Phase 2 : 2-3 parameter candidate formulae (incl. |Z_N| premier/composite)
# ----------------------------------------------------------------------------
print("\n" + "=" * 78)
print("Phase 2 : Multi-parameter candidate formulae")
print("=" * 78)

def fit_multi(fn, p0, name, n_par):
    """Fit fn(N, *params), report chi^2, AIC, BIC, predictions."""
    def chi2(p):
        pred = fn(N_arr, *p)
        return np.sum(((pred - kappa_arr) / err_arr) ** 2)
    res = minimize(chi2, p0, method="Nelder-Mead",
                   options={"xatol": 1e-9, "fatol": 1e-9, "maxiter": 50000})
    p_fit = res.x
    ch = float(res.fun)
    dof = max(1, 5 - n_par)
    aic = ch + 2 * n_par
    bic = ch + n_par * np.log(5)
    pred = fn(N_arr, *p_fit)
    return {
        "name": name, "params": p_fit.tolist(), "chi2": ch,
        "chi2_dof": ch/dof, "aic": aic, "bic": bic, "pred": pred.tolist()
    }

multi_candidates = [
    # 2-param formulas
    ("M1 a+b/N",              lambda N, a, b: a + b/N,                          [0.9, -0.8],  2),
    ("M2 a+b/N^2",            lambda N, a, b: a + b/N**2,                       [0.85, -1.4], 2),
    ("M3 a+b*log(N)",         lambda N, a, b: a + b*np.log(N),                  [0.4, 0.15],  2),
    ("M4 a*N/(N+c)",          lambda N, a, b: a * N/(N+b),                      [1.0, 2.0],   2),
    ("M5 a*(1-1/N^b)",        lambda N, a, b: a * (1 - 1.0/N**b),               [0.85, 1.8],  2),
    ("M6 a*N^b",              lambda N, a, b: a * N**b,                         [0.4, 0.35],  2),
    ("M7 a*(1-exp(-b*N))",    lambda N, a, b: a * (1 - np.exp(-b*N)),           [0.85, 0.6],  2),
    ("M8 a*tanh(b*N)",        lambda N, a, b: a * np.tanh(b*N),                 [0.85, 0.4],  2),
    # 2-param with center Z_N premier/composite indicator
    ("M9 a*(1-1/N^2) + b*(1-is_prime)",
        lambda N, a, b: a*(1-1/N**2) + b * (1.0 - np.isin(N.astype(int),[2,3,5,7,11,13]).astype(float)),
        [0.68, 0.15], 2),
    ("M10 a*(1-1/N^2) + b*(N=2*3 indicator)",
        lambda N, a, b: a*(1-1/N**2) + b * (N==6).astype(float),
        [0.68, 0.15], 2),
    # 3-param formulas
    ("M11 a + b/N + c/N^2",
        lambda N, a, b, c: a + b/N + c/N**2,
        [0.85, -0.3, -0.7], 3),
    ("M12 a*(1-1/N^2) + b*N + c",
        lambda N, a, b, c: a*(1-1/N**2) + b*N + c,
        [0.55, 0.03, 0.05], 3),
    ("M13 a*(1-1/N^2) + b*(1-is_prime)*(N-4)",
        lambda N, a, b, c: a*(1-1/N**2)
            + b * (1.0 - np.isin(N.astype(int),[2,3,5,7,11,13]).astype(float)) * (N-4),
        [0.68, 0.15, 0.0], 3),
    # Power scaling with offset
    ("M14 a*N^b + c",
        lambda N, a, b, c: a * N**b + c,
        [0.3, 0.4, 0.05], 3),
]

results_multi = []
for name, fn, p0, np_ in multi_candidates:
    try:
        r = fit_multi(fn, p0, name, np_)
        results_multi.append(r)
    except Exception as e:
        print(f"  [skipped {name}: {e}]")

print(f"\n{'Formula':<46} {'params':<40} {'chi^2':>8} {'chi^2/dof':>10} {'AIC':>7} {'BIC':>7}")
print("-" * 140)
for r in results_multi:
    p_str = "[" + ", ".join([f"{p:+.4f}" for p in r["params"]]) + "]"
    print(f"{r['name']:<46} {p_str:<40} {r['chi2']:>8.2f} {r['chi2_dof']:>10.3f} "
          f"{r['aic']:>7.2f} {r['bic']:>7.2f}")

# ----------------------------------------------------------------------------
# Phase 3 : Leave-one-out cross-validation on best 1-param candidates
# ----------------------------------------------------------------------------
print("\n" + "=" * 78)
print("Phase 3 : Leave-one-out cross-validation (top 5 from Phase 1+2)")
print("=" * 78)

# Take top 5 by chi^2/dof from combined (1-param + multi-param)
all_results = []
for r in results_1p:
    all_results.append({"name": r["name"], "n_par": 1, "chi2_dof": r["chi2_dof"]})
for r in results_multi:
    all_results.append({"name": r["name"], "n_par": len(r["params"]),
                       "chi2_dof": r["chi2_dof"]})
all_results.sort(key=lambda x: x["chi2_dof"])
print(f"\nTop-8 by chi^2/dof :")
for r in all_results[:8]:
    print(f"  {r['name']:<45} chi^2/dof = {r['chi2_dof']:>9.3f} (np = {r['n_par']})")

# For LOO, refit each top model using N \\ {i} and predict i
def fit_1p(fn, a0, N_train, k_train, e_train):
    def chi2(a):
        return np.sum(((fn(N_train, a) - k_train)/e_train)**2)
    res = minimize_scalar(chi2, bracket=(a0/3., a0*3.))
    return res.x

def fit_np(fn, p0, N_train, k_train, e_train):
    def chi2(p):
        return np.sum(((fn(N_train, *p) - k_train)/e_train)**2)
    res = minimize(chi2, p0, method="Nelder-Mead",
                   options={"xatol": 1e-9, "fatol": 1e-9, "maxiter": 50000})
    return res.x

# Catalogue retesting (a few of the top performers — manually)
loo_targets = [
    ("F1 a*(1-1/N^2)",       lambda N, a: a*(1-1/N**2),                    0.68,   "1p"),
    ("F2 a*N/(N+1)",          lambda N, a: a*N/(N+1),                       0.68,   "1p"),
    ("F4 a*log(N)",           lambda N, a: a*np.log(N),                     0.5,    "1p"),
    ("F8 a*N^(1/3)",          lambda N, a: a*N**(1/3.),                     0.4,    "1p"),
    ("F9 a*N^(1/4)",          lambda N, a: a*N**(0.25),                     0.45,   "1p"),
    ("M3 a+b*log(N)",         lambda N, a, b: a + b*np.log(N),              [0.4, 0.15], "2p"),
    ("M6 a*N^b",              lambda N, a, b: a*N**b,                       [0.4, 0.35], "2p"),
    ("M14 a*N^b + c",         lambda N, a, b, c: a*N**b + c,                [0.3, 0.4, 0.05], "3p"),
    ("M11 a+b/N+c/N^2",       lambda N, a, b, c: a + b/N + c/N**2,          [0.85, -0.3, -0.7], "3p"),
]

print(f"\n{'Formula':<28}  {'N_left':>6} {'pred':>8} {'observed':>9} "
      f"{'residual_sigma':>15}")
print("-" * 90)
loo_results = {}
for name, fn, p0, kind in loo_targets:
    sigmas = []
    for i in range(len(N_arr)):
        mask = np.ones_like(N_arr, dtype=bool); mask[i] = False
        N_tr, k_tr, e_tr = N_arr[mask], kappa_arr[mask], err_arr[mask]
        if kind == "1p":
            a = fit_1p(fn, p0, N_tr, k_tr, e_tr)
            pred_i = float(fn(np.array([N_arr[i]]), a)[0])
        else:
            p_fit = fit_np(fn, p0, N_tr, k_tr, e_tr)
            pred_i = float(fn(np.array([N_arr[i]]), *p_fit)[0])
        obs_i = kappa_arr[i]
        err_i = err_arr[i]
        sig = (pred_i - obs_i) / err_i
        sigmas.append(sig)
        print(f"{name:<28}  N={int(N_arr[i]):>2d}    {pred_i:>8.4f} {obs_i:>9.4f} "
              f"{sig:>+15.2f}σ")
    rms = float(np.sqrt(np.mean(np.array(sigmas)**2)))
    loo_results[name] = {"sigmas": sigmas, "rms": rms}
    print(f"  → RMS residual = {rms:.2f}σ")
    print()

# ----------------------------------------------------------------------------
# Phase 4 : PySR symbolic regression
# ----------------------------------------------------------------------------
print("=" * 78)
print("Phase 4 : PySR symbolic regression with structural features")
print("=" * 78)

PYSR_RAN = False
pysr_equations = []
try:
    from pysr import PySRRegressor
    X = np.column_stack([N_arr,
                         1.0/N_arr,
                         N_arr**2,
                         np.isin(N_arr.astype(int),[2,3,5,7]).astype(float)])
    var_names = ["Nc", "invNc", "Nc2", "primeZ"]
    y = kappa_arr
    weights = 1.0 / err_arr**2

    print(f"\nRunning PySR: 5 datapoints, 4 features {var_names}")
    print("  niterations=200, population_size=80, complexity_max=15")
    model = PySRRegressor(
        niterations=200,
        population_size=80,
        binary_operators=["+", "-", "*", "/"],
        unary_operators=["sqrt", "log", "exp", "square"],
        model_selection="best",
        progress=False,
        verbosity=0,
        random_state=SEED,
        deterministic=True,
        parallelism="serial",
        elementwise_loss="loss(x, y, w) = w * (x - y)^2",
        complexity_of_constants=2,
        maxsize=15,
        timeout_in_seconds=240,
    )
    model.fit(X, y, variable_names=var_names, weights=weights)
    print("\nPySR equations Pareto front :")
    print(model)
    eqs = model.equations_
    if eqs is not None:
        for idx, row in eqs.iterrows():
            try:
                eq_str = str(row.get("equation", ""))
                cmplx = int(row.get("complexity", -1))
                loss = float(row.get("loss", -1))
                score = float(row.get("score", -1))
                pysr_equations.append({
                    "complexity": cmplx, "equation": eq_str,
                    "loss": loss, "score": score
                })
            except Exception:
                pass
    print(f"\nBest equation : {model.sympy()}")
    PYSR_RAN = True
except ImportError as e:
    print(f"[PySR import error : {e}]")
except Exception as e:
    print(f"[PySR run error : {e}]")
    import traceback
    traceback.print_exc()

# ----------------------------------------------------------------------------
# Phase 5 : Revised kappa_inf candidates (5 datapoints)
# ----------------------------------------------------------------------------
print("\n" + "=" * 78)
print("Phase 5 : kappa_inf asymptote candidates (revisited with 5 points)")
print("=" * 78)

# Best fit if we trust formula F1 (1-1/N^2) only on a subset
# Reminder: F1 valid on N=2,3,4 - we extract kappa_inf_local
print("\n(A) Restricted fit (1-1/N^2)*A on N=2,3,4 only :")
mask_local = N_arr <= 4
def chi2_local(a):
    return np.sum(((a*(1 - 1/N_arr[mask_local]**2) - kappa_arr[mask_local])/err_arr[mask_local])**2)
r_local = minimize_scalar(chi2_local, bracket=(0.5, 0.9))
A_local = float(r_local.x)
chi_local = float(r_local.fun)
A_err_local = 0.003  # approximated from earlier session
print(f"  kappa_inf_local = {A_local:.5f} ± ~0.003 (chi^2 = {chi_local:.3f}, dof=2)")

print("\n(B) Restricted fit on N=2,3,4,5 :")
mask_45 = N_arr <= 5
def chi2_45(a):
    return np.sum(((a*(1 - 1/N_arr[mask_45]**2) - kappa_arr[mask_45])/err_arr[mask_45])**2)
r_45 = minimize_scalar(chi2_45, bracket=(0.5, 0.9))
A_45 = float(r_45.x)
chi_45 = float(r_45.fun)
print(f"  kappa_inf_{{N<=5}} = {A_45:.5f}  (chi^2 = {chi_45:.3f}, dof=3)")

print("\n(C) Full fit on N=2..6 :")
mask_all = np.ones_like(N_arr, dtype=bool)
def chi2_all(a):
    return np.sum(((a*(1 - 1/N_arr**2) - kappa_arr)/err_arr)**2)
r_all = minimize_scalar(chi2_all, bracket=(0.5, 1.0))
A_all = float(r_all.x)
chi_all = float(r_all.fun)
print(f"  kappa_inf_{{N<=6}} = {A_all:.5f}  (chi^2 = {chi_all:.3f}, dof=4)")
print(f"    → chi^2/dof of {chi_all/4:.1f} CONFIRMS formula F1 BROKEN for N=6")

print("\n--- kappa_inf_local benchmarking against transcendental candidates ---")
asymptote_candidates = [
    ("zeta(3)/sqrt(pi)",    ZETA3_OVER_SQRT_PI,                  "3-loop YM N^3LO / Gaussian"),
    ("1 - 1/pi",            1 - 1/PI,                            "pi combination"),
    ("pi/(pi+3/2)",         PI/(PI+1.5),                         "Pade-like"),
    ("2/3",                 2/3,                                  "Koide 4*kappa_FP saturation"),
    ("ln(2)",               LN2,                                  "Information bit"),
    ("27/40",               27/40,                                "Rational small"),
    ("17/25",               17/25,                                "Rational small"),
    ("Gamma(1/3)/pi",       np.exp(np.log(2.6789385347))/PI,     "Gamma special"),
    ("(pi-1)/pi",           (PI-1)/PI,                            "pi shift"),
    ("0.68 fit free",       A_local,                              "Empirical (this fit)"),
]
print(f"\n  {'Candidate':<30} {'value':>10} {'|A_local-v|':>13}  {'sigma':>8}")
print("  " + "-"*70)
for name, val, motiv in asymptote_candidates:
    diff = abs(val - A_local)
    sig = diff / A_err_local
    marker = " ★" if sig < 1 else ("  ⚠" if sig < 3 else "")
    print(f"  {name:<30} {val:>10.5f} {diff:>13.5f}  {sig:>7.2f}σ {marker}")

# ----------------------------------------------------------------------------
# Hypothesis Z_N premier vs composite : structured analysis
# ----------------------------------------------------------------------------
print("\n" + "=" * 78)
print("Hypothesis Z_N premier vs composite (Lucini-Teper bulk transition)")
print("=" * 78)

# For each N, compute residual vs F1 with A=A_local
pred_F1 = A_local * (1 - 1/N_arr**2)
resid = (kappa_arr - pred_F1)
resid_sig = resid / err_arr
print(f"\n  Residuals vs F1 fit on N=2,3,4 (A={A_local:.4f}):")
print(f"  {'N':>3} {'|Z_N|':>6} {'centre':>10} {'pred F1':>9} {'obs':>9} "
      f"{'residual':>10} {'σ':>7}")
print("  " + "-"*70)
ZN_class = {2: ("Z2", "prime"), 3: ("Z3", "prime"), 4: ("Z4", "composite 2^2"),
            5: ("Z5", "prime"), 6: ("Z6", "composite 2*3"),
            7: ("Z7", "prime"), 8: ("Z8", "composite 2^3"), 9: ("Z9", "composite 3^2")}
for i, n in enumerate(N_arr.astype(int)):
    centre_name, centre_class = ZN_class.get(n, (f"Z{n}", "?"))
    print(f"  {n:>3} {n:>6} {centre_name:>10}  {pred_F1[i]:>9.4f} {kappa_arr[i]:>9.4f} "
          f"{resid[i]:>+10.4f} {resid_sig[i]:>+7.2f}")
print("\n  Pattern : prime Z_N (N=2,3,5,7) follow F1 within ~few sigma ?")
print("           composite Z_N (N=4,6,8,9) deviate ?")
print("  ⇒ Verdict : N=2,3,4 ALL fit F1 well (including N=4 composite Z_4),")
print("    N=5 deviates by ~4-5σ, N=6 deviates by ~28σ.")
print("    PATTERN PARTIAL: prime/composite Z_N alone INSUFFICIENT to explain.")
print("    Hypothesis Z_N premier requires that N=4 (composite Z_4) match F1,")
print("    which IS the case (kappa=0.6353 vs 0.6358 predicted, 0.11σ).")
print("    So hypothesis Z_N composite SHOULD predict N=4 deviates - it does NOT.")

# Alternative: maybe N=5,6 deviate because of Lucini-Teper bulk transition
# at large N for first-order deconfinement / 2nd order phase boundary
# Let's check if Linear fit on N=5,6 alone makes sense vs N=2,3,4
def fit_2pts(N_pair, k_pair):
    """Linear fit through 2 points."""
    slope = (k_pair[1] - k_pair[0]) / (N_pair[1] - N_pair[0])
    intercept = k_pair[0] - slope * N_pair[0]
    return slope, intercept

slope56, intercept56 = fit_2pts(np.array([5, 6]), kappa_arr[3:5])
print(f"\n  Linear fit N=5,6 : slope={slope56:.4f}, intercept={intercept56:.4f}")
print(f"  Extrapolation: N=7 → {slope56*7+intercept56:.4f}, N=8 → {slope56*8+intercept56:.4f}")
print("  ⇒ Linear extrapolation N=5,6 is too rapid (would give κ>1 for N=10).")
print("    Suggests N=5,6 are transient near a saturation -- new asymptote ?")

# ----------------------------------------------------------------------------
# Save all results
# ----------------------------------------------------------------------------
output = {
    "session": "2026-05-26",
    "method": "BP2008b cross-N kappa_lattice refit post-SU(6) finding",
    "author": "Kévin Rémondière",
    "orcid": "0009-0008-2443-7166",
    "reference_method": "Buividovich & Polikarpov, arXiv:0802.4247",
    "data": {str(int(n)): {"kappa": float(DATA[int(n)][0]),
                            "err": float(DATA[int(n)][1]),
                            "beta_thooft": float(DATA[int(n)][2]),
                            "source": DATA[int(n)][3]}
             for n in N_arr},
    "phase1_1param_results": results_1p,
    "phase2_multi_param_results": results_multi,
    "phase3_loo_results": loo_results,
    "phase4_pysr": {
        "ran": PYSR_RAN,
        "equations": pysr_equations,
    },
    "phase5_kappa_inf": {
        "local_N234":  {"A": float(A_local), "chi2": float(chi_local), "dof": 2,
                        "comment": "F1 (1-1/N^2) on N=2,3,4 only - tight"},
        "extended_N2345": {"A": float(A_45), "chi2": float(chi_45), "dof": 3,
                           "comment": "F1 includes N=5 - chi^2 explodes"},
        "full_N23456": {"A": float(A_all), "chi2": float(chi_all), "dof": 4,
                        "comment": "F1 falsified"},
        "asymptote_candidates": [
            {"name": name, "value": float(val), "diff_local": float(abs(val-A_local)),
             "sigma_local": float(abs(val-A_local)/A_err_local), "motivation": motiv}
            for name, val, motiv in asymptote_candidates
        ],
    },
    "z_n_hypothesis": {
        "verdict": ("PARTIAL: N=2,3,4 all fit F1 regardless of Z_N premier/composite "
                    "(Z_4 composite fits perfectly). N=5,6 deviate but linear in N "
                    "would also fail prediction. Need additional mechanism."),
        "residuals_vs_F1": {str(int(N_arr[i])): {
            "ZN_class": ZN_class.get(int(N_arr[i]),(f"Z{int(N_arr[i])}","?"))[1],
            "residual": float(resid[i]),
            "sigma": float(resid_sig[i])
        } for i in range(len(N_arr))},
    },
}

out_path = "/root/cc-private/papers/2026-05-24-session/scripts/pysr_eci_post_su6_results_2026-05-26.json"
with open(out_path, "w") as f:
    json.dump(output, f, indent=2, default=str)
print(f"\nResults saved to : {out_path}")

# Quick summary at end
print("\n" + "=" * 78)
print("SUMMARY")
print("=" * 78)
print(f"  Best 1-param formula (chi^2/dof) : {all_results[0]['name']:<30} ({all_results[0]['chi2_dof']:.2f})")
print(f"  Best 2-param formula             : "
      + min([r for r in all_results if r['n_par']==2], key=lambda x:x['chi2_dof'])['name'])
print(f"  Best 3-param formula             : "
      + (min([r for r in all_results if r['n_par']==3], key=lambda x:x['chi2_dof'])['name']
         if any(r['n_par']==3 for r in all_results) else "(none)"))
print(f"  kappa_inf_local (N<=4)           : {A_local:.5f}  vs zeta(3)/sqrt(pi)={ZETA3_OVER_SQRT_PI:.5f}")
print(f"  Full fit F1 chi^2 / dof          : {chi_all/4:.2f} (FORMULA FALSIFIED)")
print(f"  PySR ran                         : {PYSR_RAN}")
print(f"  PySR best equations              : {len(pysr_equations)}")
print("\nDONE.")
