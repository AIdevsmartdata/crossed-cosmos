#!/usr/bin/env python3
"""Refit K41 et alternatives sur 8 dense points (N=5..12)."""
import numpy as np
from scipy.optimize import curve_fit

# 8 dense data points
N = np.array([5, 6, 7, 8, 9, 10, 11, 12], dtype=float)
K = np.array([0.7012, 0.810, 0.9107, 1.0416, 1.1764, 1.3307, 1.5008, 1.6707])
E = np.array([0.006, 0.005, 0.0054, 0.0046, 0.0047, 0.0048, 0.0051, 0.0050])

print("=== Refit 8 dense points N=5..12 ===")
print(f"Data : {list(zip(N.astype(int), K, E))}")

# 1. Fixed K41 p=5/3
def K41(n, a, b):
    return a*n**(5/3) + b
popt, _ = curve_fit(K41, N, K, sigma=E, absolute_sigma=True)
chi2 = np.sum(((K - K41(N, *popt))/E)**2)
print(f"\n1. K41 p=5/3 fixed : α={popt[0]:.5f}, β={popt[1]:.4f}, χ²/dof={chi2/(len(N)-2):.2f}")
for n, k, e in zip(N, K, E):
    p = K41(n, *popt)
    print(f"   SU({int(n)}): obs {k:.4f}, pred {p:.4f}, Δ={k-p:+.4f} ({(k-p)/e:+.1f}σ)")

# 2. Free p
def powerlaw(n, a, p, b):
    return a*n**p + b
try:
    popt2, _ = curve_fit(powerlaw, N, K, sigma=E, p0=[0.02, 1.5, 0.4], absolute_sigma=True)
    chi2 = np.sum(((K - powerlaw(N, *popt2))/E)**2)
    print(f"\n2. Free power : α={popt2[0]:.5f}, p={popt2[1]:.4f}, β={popt2[2]:.4f}, χ²/dof={chi2/(len(N)-3):.2f}")
    for n, k, e in zip(N, K, E):
        p = powerlaw(n, *popt2)
        print(f"   SU({int(n)}): obs {k:.4f}, pred {p:.4f}, Δ={(k-p)/e:+.1f}σ")
    # Predictions
    for npred in [13, 14, 15, 20]:
        print(f"   SU({npred}): pred = {powerlaw(npred, *popt2):.4f}")
except Exception as ex:
    print(f"Free power fit failed: {ex}")

# 3. Linear dim(G) = N²-1
def dimG(n, a, b):
    return a*(n**2-1) + b
popt3, _ = curve_fit(dimG, N, K, sigma=E, absolute_sigma=True)
chi2 = np.sum(((K - dimG(N, *popt3))/E)**2)
print(f"\n3. Linear dim(G)=N²-1 : α={popt3[0]:.5f}, β={popt3[1]:.4f}, χ²/dof={chi2/(len(N)-2):.2f}")
for n, k, e in zip(N, K, E):
    p = dimG(n, *popt3)
    print(f"   SU({int(n)}): obs {k:.4f}, pred {p:.4f}, Δ={(k-p)/e:+.1f}σ")

# 4. Linear in N
def linearN(n, a, b):
    return a*n + b
popt4, _ = curve_fit(linearN, N, K, sigma=E, absolute_sigma=True)
chi2 = np.sum(((K - linearN(N, *popt4))/E)**2)
print(f"\n4. Linear in N : α={popt4[0]:.5f}, β={popt4[1]:.4f}, χ²/dof={chi2/(len(N)-2):.2f}")
for n, k, e in zip(N, K, E):
    p = linearN(n, *popt4)
    print(f"   SU({int(n)}): Δ={(k-p)/e:+.1f}σ")

# 5. N·log(N)
def NlogN(n, a, b):
    return a*n*np.log(n) + b
popt5, _ = curve_fit(NlogN, N, K, sigma=E, absolute_sigma=True)
chi2 = np.sum(((K - NlogN(N, *popt5))/E)**2)
print(f"\n5. κ = α·N·log(N) + β : α={popt5[0]:.5f}, β={popt5[1]:.4f}, χ²/dof={chi2/(len(N)-2):.2f}")
for n, k, e in zip(N, K, E):
    p = NlogN(n, *popt5)
    print(f"   SU({int(n)}): Δ={(k-p)/e:+.1f}σ")
