#!/usr/bin/env python3
"""M3 stability sub-window test for the V7-BK-fit ν = 1.109 finding.

Splits the 100,000 Odlyzko zeros into three sub-windows and runs the
M3 (BK + cosine) fit on each, checking ν stability."""
from __future__ import annotations
import sys, json, warnings, numpy as np
from pathlib import Path
warnings.filterwarnings("ignore")
from scipy.optimize import least_squares
sys.path.insert(0, "/root/crossed-cosmos/derivations")

ZEROS_PATH = Path("/tmp/odlyzko_cache/zeros1")
zeros_all = np.loadtxt(ZEROS_PATH)
print(f"loaded {len(zeros_all)} zeros, T range [{zeros_all[0]:.1f}, {zeros_all[-1]:.1f}]")

# Helper functions adapted from V7 scripts
def unfold(zeros):
    g = zeros / (2*np.pi)
    g = np.maximum(g, 1e-30)
    return g * np.log(g)

def R2_GUE(x):
    out = np.ones_like(x)
    mask = np.abs(x) > 1e-10
    pi_x = np.pi * x[mask]
    out[mask] = 1.0 - (np.sin(pi_x)/pi_x)**2
    return out

def compute_R2(unfolded, n_bins=60, x_max=3.0):
    n = len(unfolded)
    diffs = []
    chunk = 10000
    for i in range(0, n, chunk):
        upper = min(i+chunk*2, n)
        block = unfolded[i:upper]
        for k in range(len(block)):
            others = block[k+1:]
            if len(others)==0: continue
            d = others - block[k]
            d = d[d < x_max]
            if len(d): diffs.append(d)
    diffs = np.concatenate(diffs)
    bins = np.linspace(0, x_max, n_bins+1)
    counts, _ = np.histogram(diffs, bins=bins)
    width = bins[1] - bins[0]
    R2 = (counts*2.0)/(n*width)
    sigma = np.sqrt(np.maximum(counts,1))*2.0/(n*width)
    x = 0.5*(bins[1:]+bins[:-1])
    return x, R2, sigma

def delta_BK_unit(x, L):
    """Bogomolny-Keating arithmetic correction unit amplitude."""
    if L < 0.1: L = 0.1
    PMAX = 10**5
    sieve = np.ones(PMAX+1, dtype=bool); sieve[:2]=False
    for i in range(2, int(np.sqrt(PMAX))+1):
        if sieve[i]: sieve[i*i::i]=False
    primes = np.where(sieve)[0]
    out = np.zeros_like(x)
    for p in primes[:1000]:
        log_p = np.log(p)
        for k in range(1,4):
            coef = (log_p/k)**2 / p**k
            arg = 2*np.pi*x*k/L
            out += coef * np.cos(arg)
    return -2*out/(2*np.pi)**2

def fit_M3(x, R2, sigma, L_init):
    """Fit M3: residual = A * delta_BK(x, L) + C * cos(nu*x + phi)"""
    R2g = R2_GUE(x)
    res = R2 - R2g
    # Free params: A, L, C, nu, phi
    def model(params):
        A, L, C, nu, phi = params
        return A * delta_BK_unit(x, L) + C * np.cos(nu*x + phi)
    def residuals(params):
        return (res - model(params)) / sigma
    p0 = [0.4, L_init, 0.03, 1.1, 0.4]
    out = least_squares(residuals, p0, method="lm", max_nfev=5000)
    chi2 = float((out.fun**2).sum())
    A, L, C, nu, phi = out.x
    return {"A":float(A),"L":float(L),"C":float(C),"nu":float(nu),"phi":float(phi),
            "chi2":chi2,"dof":len(x)-5,"success":bool(out.success)}

# Three sub-windows
windows = [
    ("first 25k",  0,    25000),
    ("middle 50k", 25000, 75000),
    ("last 25k",   75000, 100000),
    ("full 100k",  0, 100000),
]

results = {}
for name, lo, hi in windows:
    sub = zeros_all[lo:hi]
    n = len(sub)
    L_init = float(np.log(np.mean(sub) / (2*np.pi)))
    print(f"\n=== {name} (n={n}, T_mean={np.mean(sub):.1f}, L={L_init:.3f}) ===")
    unf = unfold(sub)
    x, R2, sigma = compute_R2(unf, n_bins=60, x_max=3.0)
    fit = fit_M3(x, R2, sigma, L_init)
    fit["window"] = name
    fit["n"] = n
    fit["T_mean"] = float(np.mean(sub))
    fit["L_init"] = L_init
    results[name] = fit
    print(f"  A={fit['A']:.4f}  L={fit['L']:.3f}  C={fit['C']:.4f}  nu={fit['nu']:.4f}  phi={fit['phi']:.3f}")
    print(f"  chi2/dof = {fit['chi2']/fit['dof']:.3f}")

# Comparison summary
print("\n=== ν STABILITY ACROSS SUB-WINDOWS ===")
nus = [results[w[0]]["nu"] for w in windows]
print(f"{'window':<14} {'n':>6} {'A':>8} {'L':>8} {'C':>8} {'nu':>8} {'phi':>8} {'chi2/dof':>10}")
for name, lo, hi in windows:
    r = results[name]
    print(f"{name:<14} {r['n']:>6} {r['A']:>8.4f} {r['L']:>8.3f} {r['C']:>8.4f} {r['nu']:>8.4f} {r['phi']:>8.3f} {r['chi2']/r['dof']:>10.3f}")

print(f"\nν spread (sub-windows only): {max(nus[:3]) - min(nus[:3]):.4f}")
print(f"ν mean (sub-windows): {np.mean(nus[:3]):.4f}")
print(f"ν median (all): {np.median(nus):.4f}")

with open("/tmp/m3_stability_results.json","w") as f:
    json.dump(results, f, indent=2)
print("\nresults saved /tmp/m3_stability_results.json")
