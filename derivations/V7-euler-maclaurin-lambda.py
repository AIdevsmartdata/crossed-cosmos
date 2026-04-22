#!/usr/bin/env python3
"""
V7 — Euler-Maclaurin / zeta-regularised spectral sum on Odlyzko 10^5 zeros.

Computes:
  rho_Lambda^ZSA(Lambda_UV) = (Lambda_UV^4 / (2 pi)^2) * [ S(Lambda_UV) - I(Lambda_UV) ]

with
  S(Lambda_UV) = sum_{n<=N} f(gamma_n / Lambda_UV)
  I(Lambda_UV) = int_0^infty f(gamma / Lambda_UV) * rhobar(gamma) dgamma
  rhobar(gamma) = (1/(2 pi)) * log(gamma / (2 pi))   (Riemann-von Mangoldt)

Test two cutoffs:
  f1(t) = exp(-t^2)
  f2(t) = 1/(1+t^2)^2

Deliverables: .py, .png (log-log), .md report.
"""

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from scipy import integrate

ZEROS_PATH = "/tmp/odlyzko_zeros1.txt"
OUT_PNG = "/home/remondiere/crossed-cosmos/derivations/V7-euler-maclaurin-lambda.png"

# ---------- load zeros ----------
gammas = np.loadtxt(ZEROS_PATH)
N = len(gammas)
print(f"Loaded {N} Odlyzko zeros; gamma_1 = {gammas[0]:.6f}, gamma_N = {gammas[-1]:.6f}")

# ---------- cutoff functions ----------
def f_gauss(t):
    return np.exp(-t*t)

def f_rational(t):
    return 1.0/(1.0+t*t)**2

CUTOFFS = {"gauss": f_gauss, "rational": f_rational}

# Riemann-von Mangoldt smooth density
def rhobar(gamma):
    # avoid log of very small — gamma_1 ~14 so gamma/(2pi) > 1 always here
    return np.log(gamma/(2.0*np.pi))/(2.0*np.pi)

# ---------- compute S and I for a grid of Lambda_UV ----------
# Lambda_UV grid: log-spaced between gamma_1 and gamma_N
Lambdas = np.logspace(np.log10(gammas[0]*1.01), np.log10(gammas[-1]), 80)

results = {}

for cname, f in CUTOFFS.items():
    S_arr = np.empty_like(Lambdas)
    I_arr = np.empty_like(Lambdas)
    residue_arr = np.empty_like(Lambdas)
    rho_arr = np.empty_like(Lambdas)

    for i, Lam in enumerate(Lambdas):
        t = gammas / Lam
        S = float(np.sum(f(t)))

        # Smooth integral: int_{gamma_min}^{gamma_N} f(gamma/Lam) rhobar(gamma) dgamma
        # Lower limit: start at gamma_1 (below this there are no zeros and rhobar would be negative/ill)
        # Actually rhobar has zero at gamma = 2pi ~ 6.28; Odlyzko zeros start at 14.13, so rhobar > 0 throughout.
        # We integrate from gamma_1 to a large upper cutoff effectively set by f decay, but cap at gammas[-1]
        # for apples-to-apples comparison with the discrete sum which only runs up to gamma_N.
        def integrand(g):
            return f(g/Lam)*rhobar(g)
        # use quad
        I_val, _ = integrate.quad(integrand, gammas[0], gammas[-1], limit=200)
        S_arr[i] = S
        I_arr[i] = I_val
        residue_arr[i] = S - I_val
        rho_arr[i] = (Lam**4/(2.0*np.pi)**2) * (S - I_val)

    results[cname] = dict(S=S_arr, I=I_arr, residue=residue_arr, rho=rho_arr)
    print(f"\n[{cname}] sample:")
    for idx in [0, len(Lambdas)//4, len(Lambdas)//2, 3*len(Lambdas)//4, -1]:
        print(f"  Lam={Lambdas[idx]:10.3f}  S={S_arr[idx]:12.4f}  I={I_arr[idx]:12.4f}  "
              f"S-I={residue_arr[idx]:+12.4e}  rho={rho_arr[idx]:+.4e}")

# ---------- plot ----------
fig, axes = plt.subplots(1, 2, figsize=(14, 5.5))

# Left: residue S-I vs Lambda_UV (log-log absolute value with sign markers)
ax = axes[0]
for cname, col in [("gauss", "C0"), ("rational", "C1")]:
    r = results[cname]["residue"]
    ax.plot(Lambdas, np.abs(r), label=f"|S-I|  [{cname}]", color=col)
    # overplot sign
    pos = r > 0
    ax.scatter(Lambdas[pos], np.abs(r[pos]), marker="^", s=12, color=col, alpha=0.6)
    ax.scatter(Lambdas[~pos], np.abs(r[~pos]), marker="v", s=12, color=col, alpha=0.6)
ax.set_xscale("log"); ax.set_yscale("log")
ax.set_xlabel(r"$\Lambda_{UV}$")
ax.set_ylabel(r"$|S(\Lambda) - I(\Lambda)|$  (dimensionless residue)")
ax.set_title("Discrete sum minus smooth integral")
ax.legend(); ax.grid(True, which="both", alpha=0.3)

# Right: rho_Lambda^ZSA
ax = axes[1]
for cname, col in [("gauss", "C0"), ("rational", "C1")]:
    rho = results[cname]["rho"]
    ax.plot(Lambdas, np.abs(rho), label=f"|rho^ZSA|  [{cname}]", color=col)
    pos = rho > 0
    ax.scatter(Lambdas[pos], np.abs(rho[pos]), marker="^", s=12, color=col, alpha=0.6)
    ax.scatter(Lambdas[~pos], np.abs(rho[~pos]), marker="v", s=12, color=col, alpha=0.6)
# Reference slope Lambda^4
ref = Lambdas**4 / (2*np.pi)**2 * 1e-2
ax.plot(Lambdas, ref, "k--", alpha=0.4, label=r"$\propto \Lambda^4$ (ref)")
ax.set_xscale("log"); ax.set_yscale("log")
ax.set_xlabel(r"$\Lambda_{UV}$")
ax.set_ylabel(r"$|\rho_\Lambda^{ZSA}|$")
ax.set_title(r"$\rho_\Lambda^{ZSA} = (\Lambda^4/(2\pi)^2)(S-I)$")
ax.legend(); ax.grid(True, which="both", alpha=0.3)

plt.tight_layout()
plt.savefig(OUT_PNG, dpi=130)
print(f"\nSaved plot -> {OUT_PNG}")

# ---------- diagnostics for report ----------
# (1) scaling of residue vs Lambda at large Lambda
# Fit |S-I| ~ A * Lambda^p for Lambda in [Lambda_N/10, Lambda_N]
print("\n--- Scaling diagnostics ---")
for cname in CUTOFFS:
    r = np.abs(results[cname]["residue"])
    mask = (Lambdas > gammas[-1]/10) & (r > 0)
    if mask.sum() >= 5:
        p, logA = np.polyfit(np.log(Lambdas[mask]), np.log(r[mask]), 1)
        print(f"  [{cname}] |S-I| ~ Lambda^{p:+.3f} at large Lambda (near gamma_N)")
    # value of rho at Lambda = gamma_N
    print(f"  [{cname}] rho^ZSA(Lam=gamma_N) = {results[cname]['rho'][-1]:+.6e}")
    # value of rho at Lambda = gamma_N/2
    idx_half = np.argmin(np.abs(Lambdas - gammas[-1]/2))
    print(f"  [{cname}] rho^ZSA(Lam=gamma_N/2) = {results[cname]['rho'][idx_half]:+.6e}")

# Ratio residue / sqrt(N) (Montgomery-like fluctuation scaling)
print("\n--- Residue scale vs sqrt(N_eff) ---")
for cname in CUTOFFS:
    r_last = results[cname]["residue"][-1]
    # N_eff ~ number of zeros inside cutoff
    N_eff = np.sum(gammas <= Lambdas[-1])
    print(f"  [{cname}] |S-I|={abs(r_last):.4e}, sqrt(N_eff)={np.sqrt(N_eff):.2f}, "
          f"ratio={abs(r_last)/np.sqrt(N_eff):.4e}")

# save arrays
np.savez("/home/remondiere/crossed-cosmos/derivations/_cache/V7_euler_maclaurin.npz",
         Lambdas=Lambdas,
         **{f"{c}_S": results[c]["S"] for c in CUTOFFS},
         **{f"{c}_I": results[c]["I"] for c in CUTOFFS},
         **{f"{c}_residue": results[c]["residue"] for c in CUTOFFS},
         **{f"{c}_rho": results[c]["rho"] for c in CUTOFFS})
print("Saved arrays -> _cache/V7_euler_maclaurin.npz")
