#!/usr/bin/env python3
"""PySR symbolic regression sur DESI DR1 BAO data.

Cherche la forme fonctionnelle de :
  H(z)/H_0   --or--   rho_DE(z)/rho_DE(0)   --or--   residual vs LCDM

depuis les bins DESI DR1, sans imposer Modular Quintessence ou CPL a priori.
"""
import numpy as np
import math, sys
try:
    from pysr import PySRRegressor
    print("PySR available")
except ImportError:
    print("PySR not installed - installing...")
    import subprocess
    subprocess.run(['pip', 'install', '--user', 'pysr'], check=True)
    from pysr import PySRRegressor
from scipy.integrate import quad
from scipy.optimize import minimize

# DESI DR1 BAO data (Adame et al. 2024)
desi_data = [
    (0.295, 'DV', 7.93, 0.15),
    (0.510, 'DM', 13.62, 0.25),
    (0.510, 'DH', 20.98, 0.61),
    (0.706, 'DM', 16.85, 0.32),
    (0.706, 'DH', 20.08, 0.60),
    (0.930, 'DM', 21.71, 0.28),
    (0.930, 'DH', 17.88, 0.35),
    (1.317, 'DM', 27.79, 0.69),
    (1.317, 'DH', 13.82, 0.42),
    (1.491, 'DV', 26.07, 0.67),
    (2.330, 'DM', 39.71, 0.94),
    (2.330, 'DH', 8.52, 0.17),
]

c_km_s = 299792.458

# Group by z_eff to get all observables per redshift
z_eff_set = sorted(set(d[0] for d in desi_data))
print(f"Effective redshifts : {z_eff_set}")

# For each z_eff, we have DM/r_d and DH/r_d (or DV/r_d)
# We can derive H(z)/H_0 via:  DH(z) = c / H(z), so DH/r_d * (H_0 * r_d / c) = H_0 / H(z)
# i.e.  H(z)/H_0 = c / (H_0 * r_d) * 1/(DH/r_d)
# We need a fiducial (H_0 * r_d / c).
# Use Planck-best : H_0 = 67.4, r_d = 147.05  =>  H_0*r_d/c = 67.4*147.05/299792.458 = 0.033054
H0_rd_c_fid = 67.4 * 147.05 / c_km_s
print(f"Fiducial H_0*r_d/c = {H0_rd_c_fid:.5f}")

# Reconstruct H(z)/H_0 from DH measurements (where available)
H_over_H0_data = []
for z, dt, val, err in desi_data:
    if dt == 'DH':
        # val = DH/r_d, so H/H_0 = (H_0*r_d/c) / val
        ratio = H0_rd_c_fid / val
        ratio_err = ratio * err / val
        H_over_H0_data.append((z, ratio, ratio_err))

# Reconstruct H(z)/H_0 from DV measurements (which give a combination)
# DV = (z * DM^2 * DH)^(1/3), so this requires breaking the combination
# Skip DV for now (needs more inversion)

# Also reconstruct DA(z) via DM = (1+z) * DA (approx for flat)
# For LCDM comparison, use the DH-only points

print(f"\nReconstructed H(z)/H_0 from DH bins :")
print(f"{'z':>6} {'H/H_0':>10} {'err':>10}")
for z, r, e in H_over_H0_data:
    print(f"{z:>6.3f} {r:>10.4f} {e:>10.4f}")

# ============================================================
# Symbolic regression target 1 : E(z) = H(z)/H_0
# ============================================================
print("\n" + "="*78)
print("PYSR SEARCH 1 : E(z) = H(z)/H_0 vs z")
print("="*78)

X = np.array([[r[0]] for r in H_over_H0_data])  # z values
y = np.array([r[1] for r in H_over_H0_data])    # H/H_0 values
weights = np.array([1/r[2]**2 for r in H_over_H0_data])  # inverse variance

# Reference : E_LCDM(z) = sqrt(Om*(1+z)^3 + 1-Om) at Om=0.315
def E_LCDM(z, Om=0.315):
    return np.sqrt(Om*(1+z)**3 + (1-Om))

print(f"LCDM Om=0.315 predictions :")
for z, r, e in H_over_H0_data:
    pred = E_LCDM(z)
    resid = (r - pred) / e
    print(f"  z={z:.3f}  observed={r:.4f}  LCDM={pred:.4f}  residual={resid:+.2f}σ")

# Run PySR
try:
    model = PySRRegressor(
        niterations=40,
        binary_operators=["+", "-", "*", "/"],
        unary_operators=["square", "cube", "sqrt"],
        extra_sympy_mappings={},
        loss="loss(prediction, target) = (prediction - target)^2",
        weights=True,
        complexity_of_constants=1,
        verbosity=1,
        parallelism="serial",
        random_state=42,
        deterministic=True,
        populations=15,
    )
    model.fit(X, y, weights=weights)
    print("\n=== Top 5 PySR equations ===")
    print(model.equations_.head(10) if hasattr(model, 'equations_') else "No equations")
except Exception as e:
    print(f"PySR run 1 failed : {e}")
    import traceback
    traceback.print_exc()

# ============================================================
# Symbolic regression target 2 : RESIDUAL vs LCDM
# ============================================================
print("\n" + "="*78)
print("PYSR SEARCH 2 : E(z)^2 - E_LCDM(z, Om=0.315)^2  = (1-Om)*[rho_DE_ratio - 1]")
print("="*78)

# Try residual = E^2 - E_LCDM^2 (corresponds to (1-Om)*[rho_DE_ratio - 1])
Om_fid = 0.315
y_resid = np.array([r[1]**2 - E_LCDM(r[0], Om_fid)**2 for r in H_over_H0_data])
weights_resid = np.array([1/((2*r[1]*r[2])**2) for r in H_over_H0_data])

print(f"Residuals y = E^2 - E_LCDM^2 :")
for i, (z, r, e) in enumerate(H_over_H0_data):
    print(f"  z={z:.3f}  E^2 - E_LCDM^2 = {y_resid[i]:+.4f}")

try:
    model2 = PySRRegressor(
        niterations=40,
        binary_operators=["+", "-", "*", "/"],
        unary_operators=["exp", "log", "sqrt", "square"],
        complexity_of_constants=1,
        verbosity=1,
        parallelism="serial",
        random_state=42,
        deterministic=True,
        populations=15,
    )
    model2.fit(X, y_resid, weights=weights_resid)
    print("\n=== Top 5 PySR equations (residual) ===")
    print(model2.equations_.head(10) if hasattr(model2, 'equations_') else "No equations")
except Exception as e:
    print(f"PySR run 2 failed : {e}")
    import traceback
    traceback.print_exc()

# ============================================================
# Symbolic regression target 3 : w(z) = -1 + (2/3)*(1+z)*d_ln(rho)/dz
# ============================================================
# Need to compute w(z) via numerical derivative
# Use finite difference on rho_DE(z) = E^2 - Om*(1+z)^3
print("\n" + "="*78)
print("PYSR SEARCH 3 : rho_DE(z) / rho_DE(0)")
print("="*78)

# rho_DE(z)/rho_DE(0) = [E(z)^2 - Om*(1+z)^3] / [E(0)^2 - Om] = [E(z)^2 - Om*(1+z)^3] / (1-Om)
rho_DE_ratio = []
rho_DE_err = []
for z, r, e in H_over_H0_data:
    rho_z = r**2 - Om_fid*(1+z)**3
    rho_0 = 1 - Om_fid
    ratio = rho_z / rho_0
    # Propagate error from E
    ratio_err = (2*r*e) / rho_0
    rho_DE_ratio.append(ratio)
    rho_DE_err.append(abs(ratio_err))

print(f"rho_DE(z)/rho_DE(0) reconstruction (assuming Om=0.315) :")
for i, (z, r, e) in enumerate(H_over_H0_data):
    print(f"  z={z:.3f}  rho_DE_ratio = {rho_DE_ratio[i]:.4f} +/- {rho_DE_err[i]:.4f}")

y_rho = np.array(rho_DE_ratio)
weights_rho = np.array([1/e**2 for e in rho_DE_err])

try:
    model3 = PySRRegressor(
        niterations=40,
        binary_operators=["+", "-", "*", "/"],
        unary_operators=["exp", "log", "sqrt"],
        complexity_of_constants=1,
        verbosity=1,
        parallelism="serial",
        random_state=42,
        deterministic=True,
        populations=15,
    )
    model3.fit(X, y_rho, weights=weights_rho)
    print("\n=== Top 5 PySR equations (rho_DE ratio) ===")
    print(model3.equations_.head(10) if hasattr(model3, 'equations_') else "No equations")
except Exception as e:
    print(f"PySR run 3 failed : {e}")
    import traceback
    traceback.print_exc()

print("\nDONE.")
