#!/usr/bin/env python3
"""V7-BK-fit delta_BK formula bisect (against canonical V7-test5 residuals)."""
import warnings; warnings.filterwarnings("ignore")
import numpy as np
from scipy.optimize import least_squares
from pathlib import Path

# ---------- canonical V7-test5 residuals ----------
data = np.loadtxt("/tmp/V7-test5-residuals.csv")
# columns: x R2_emp R2_GUE residual sigma
x_full, _, _, res_full, sigma_full = data.T

# Same mask as V7-BK-fit.py: x > 0.1, dof=58
mask = x_full > 0.1
x = x_full[mask]
res = res_full[mask]
sigma = sigma_full[mask]
dof_data = mask.sum()
print(f"Loaded {len(x_full)} bins, mask x>0.1 -> dof={dof_data}")
print(f"GUE-only chi^2 = {np.sum((res/sigma)**2):.2f} / {dof_data} = "
      f"{np.sum((res/sigma)**2)/dof_data:.3f}\n")

# ---------- L_mean = mean(log(g/2pi)) like V7-BK-fit.py ----------
gammas = np.loadtxt("/tmp/odlyzko_zeros1.txt")
L_mean = float(np.log(gammas/(2.0*np.pi)).mean())
print(f"L_mean = {L_mean:.5f}\n")

# ---------- primes ----------
PMAX = 10**6
sieve = np.ones(PMAX+1, dtype=bool); sieve[:2]=False
for i in range(2, int(np.sqrt(PMAX))+1):
    if sieve[i]: sieve[i*i::i] = False
primes = np.where(sieve)[0].astype(np.float64)
logp = np.log(primes)

def delta_BK(x, A, L, prefactor_form, weight_form):
    arg = (2.0*np.pi/L) * np.outer(x, logp)
    if weight_form == "(logp/(p-1))^2":
        weight = (logp/(primes - 1.0))**2
    elif weight_form == "(logp)^2/p":
        weight = (logp**2) / primes
    sum_p = (np.cos(arg) * weight[None, :]).sum(axis=1)
    if prefactor_form == "-2/(2pi)^2":
        pref = -2.0 / (2.0*np.pi)**2
    elif prefactor_form == "-2/L^2":
        pref = -2.0 / L**2
    return A * pref * sum_p

def chi2_M1(prefactor, weight):
    pred = delta_BK(x, 1.0, L_mean, prefactor, weight)
    return float(np.sum(((res - pred)/sigma)**2))

def fit_M2(prefactor, weight):
    def resid(p):
        A, L = p
        return (res - delta_BK(x, A, L, prefactor, weight)) / sigma
    out = least_squares(resid, [0.5, L_mean], method="trf", max_nfev=5000,
                        bounds=([-10.0, 0.5], [10.0, 30.0]))
    return float((out.fun**2).sum()), float(out.x[0]), float(out.x[1]), bool(out.success)

variants = [
    ("A ORIGINAL    -2/(2pi)^2 (logp/(p-1))^2", "-2/(2pi)^2", "(logp/(p-1))^2"),
    ("B pref-only   -2/L^2     (logp/(p-1))^2", "-2/L^2",     "(logp/(p-1))^2"),
    ("C weight-only -2/(2pi)^2 (logp)^2/p",     "-2/(2pi)^2", "(logp)^2/p"),
    ("D BOTH        -2/L^2     (logp)^2/p",     "-2/L^2",     "(logp)^2/p"),
]
print(f"{'variant':<46} {'M1 chi^2':>10} {'M1/dof':>8} {'M2 chi^2':>10} {'M2/dof':>8} {'A_fit':>9} {'L_fit':>8}")
print("-"*108)
for name, pref, wt in variants:
    m1 = chi2_M1(pref, wt)
    m2, A, L, ok = fit_M2(pref, wt)
    flag = "" if ok else " *"
    print(f"{name:<46} {m1:>10.2f} {m1/dof_data:>8.3f} {m2:>10.2f} {m2/(dof_data-2):>8.3f} {A:>9.4f} {L:>8.3f}{flag}")
print()
print("v7-note targets: M1 ~ 11.911, M2 ~ 4.173")
