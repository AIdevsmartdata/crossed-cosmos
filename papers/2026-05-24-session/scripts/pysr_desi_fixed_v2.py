#!/usr/bin/env python3
"""PySR symbolic regression sur DESI DR1 — FIXED reconstruction H(z)/H_0."""
import numpy as np
import math
from pysr import PySRRegressor

# DESI DR1 BAO
desi_dh_data = [
    (0.510, 20.98, 0.61),
    (0.706, 20.08, 0.60),
    (0.930, 17.88, 0.35),
    (1.317, 13.82, 0.42),
    (2.330, 8.52, 0.17),
]

c_km_s = 299792.458
H0_fid = 67.4
rd_fid = 147.05
# DH(z) = c/H(z), so DH/r_d = c / (H(z) * r_d) = (c / (H_0 * r_d)) / (H(z)/H_0)
# Therefore : H(z)/H_0 = (c / (H_0 * r_d)) / (DH/r_d)
# c / (H_0 * r_d) = 299792.458 / (67.4 * 147.05) = 30.249
inv_H0rd_c = c_km_s / (H0_fid * rd_fid)
print(f"c / (H_0 * r_d) = {inv_H0rd_c:.5f}")

H_over_H0 = []
for z, dh_rd, err in desi_dh_data:
    ratio = inv_H0rd_c / dh_rd
    ratio_err = ratio * err / dh_rd
    H_over_H0.append((z, ratio, ratio_err))

print(f"\nReconstructed H(z)/H_0 (FIXED) :")
print(f"{'z':>6} {'H/H_0':>10} {'err':>10} {'LCDM':>10} {'resid':>10}")
def E_LCDM(z, Om=0.315):
    return np.sqrt(Om*(1+z)**3 + (1-Om))
for z, r, e in H_over_H0:
    pred = E_LCDM(z)
    resid = (r - pred) / e
    print(f"{z:>6.3f} {r:>10.4f} {e:>10.4f} {pred:>10.4f} {resid:>+10.2f}σ")

# Now we see the actual residuals are O(1σ) — not 30000σ
# PySR target : E(z) directly
X = np.array([[r[0]] for r in H_over_H0])
y = np.array([r[1] for r in H_over_H0])
w = np.array([1/r[2]**2 for r in H_over_H0])

print("\n=== PySR run on E(z) = H(z)/H_0 ===")
model = PySRRegressor(
    niterations=80,
    binary_operators=["+", "-", "*", "/"],
    unary_operators=["square", "cube", "sqrt", "exp"],
    complexity_of_constants=1,
    verbosity=0,
    parallelism="serial",
    random_state=42,
    deterministic=True,
    populations=20,
)
model.fit(X, y, weights=w)
print(model.equations_[["complexity", "loss", "equation"]].head(12).to_string())

# Now compute rho_DE(z)/rho_DE(0) = [E(z)^2 - Om*(1+z)^3] / (1 - Om)
print("\n=== rho_DE(z)/rho_DE(0) with Om=0.315 fixed ===")
Om = 0.315
y_rho = []
y_rho_err = []
for z, r, e in H_over_H0:
    rho = (r**2 - Om*(1+z)**3) / (1 - Om)
    rho_err = 2 * r * e / (1 - Om)
    y_rho.append(rho)
    y_rho_err.append(abs(rho_err))

print(f"{'z':>6} {'rho_DE_ratio':>15} {'err':>10}")
for i, (z, r, e) in enumerate(H_over_H0):
    print(f"{z:>6.3f} {y_rho[i]:>15.4f} {y_rho_err[i]:>10.4f}")

X2 = np.array([[r[0]] for r in H_over_H0])
y2 = np.array(y_rho)
w2 = np.array([1/e**2 for e in y_rho_err])

print("\n=== PySR run on rho_DE(z)/rho_DE(0) ===")
model2 = PySRRegressor(
    niterations=80,
    binary_operators=["+", "-", "*", "/"],
    unary_operators=["exp", "log", "sqrt", "square"],
    complexity_of_constants=1,
    verbosity=0,
    parallelism="serial",
    random_state=42,
    deterministic=True,
    populations=20,
)
model2.fit(X2, y2, weights=w2)
print(model2.equations_[["complexity", "loss", "equation"]].head(12).to_string())

# Compare best PySR forms to Modular Quintessence prediction
# MQ : rho_DE_ratio = exp(-14*pi * (alpha*(1-a) + beta*(1-a)^2))
#                   = exp(-14*pi * (alpha*z/(1+z) + beta*(z/(1+z))^2))

# Try the MQ form with optimized alpha, beta on the rho_DE_ratio data
from scipy.optimize import minimize
def MQ_form(z, alpha, beta):
    a = 1/(1+z)
    delta = alpha*(1-a) + beta*(1-a)**2
    return np.exp(-14*np.pi*delta)

def chi2_MQ_rho(params):
    alpha, beta = params
    chi2 = 0
    for i, (z, _, _) in enumerate(H_over_H0):
        pred = MQ_form(z, alpha, beta)
        chi2 += ((pred - y_rho[i]) / y_rho_err[i])**2
    return chi2

# Multi-start
best_chi2 = 1e10
best_params = None
for trial in range(20):
    np.random.seed(trial)
    init = [np.random.uniform(-0.1, 0.1), np.random.uniform(-0.1, 0.1)]
    res = minimize(chi2_MQ_rho, init, method='Nelder-Mead')
    if res.fun < best_chi2:
        best_chi2 = res.fun
        best_params = res.x

print(f"\n=== MQ form fit on rho_DE_ratio data (Om=0.315 fixed) ===")
print(f"alpha = {best_params[0]:.5f}, beta = {best_params[1]:.5f}")
print(f"chi2 = {best_chi2:.3f}, dof = {len(H_over_H0)-2} = {len(H_over_H0)-2}, chi2/dof = {best_chi2/(len(H_over_H0)-2):.3f}")

# Predictions per bin
print(f"\nPer-bin comparison :")
print(f"{'z':>6} {'rho_obs':>12} {'rho_MQ':>12} {'resid':>10}")
for i, (z, _, _) in enumerate(H_over_H0):
    pred = MQ_form(z, *best_params)
    resid = (pred - y_rho[i]) / y_rho_err[i]
    print(f"{z:>6.3f} {y_rho[i]:>12.4f} {pred:>12.4f} {resid:>+10.2f}σ")

print("\nDONE.")
