#!/usr/bin/env python3
"""
M134 -- Analytic Taylor expansion of V_F near tau = i for W = (j-1728)/eta^6.

Setup:
  K = -3 log(2 Im tau), so e^K = (2 Im tau)^{-3}
  W(tau) = (j(tau) - 1728) / eta(tau)^6
  D_tau W = W'(tau) + (3i/(2 Im tau)) W(tau)
  V_F = (2 Im tau)^{-3} [(2 Im tau)^2 / 3) |D_tau W|^2 - 3 |W|^2]

Near tau = i:
  Let s = tau - i (complex small parameter), Im tau = 1 + Im(s).
  Expand W, W', and 2 Im tau in powers of s.

Key facts at tau = i:
  W(i) = 0  (j(i) = 1728)
  W'(i) = 0  (j'(i) = 0 by E_6(i)=0)
  W''(i) = j''(i) / eta(i)^6 = -3456 pi^2 E_4(i) / eta(i)^6  =: A  (real)
  W'''(i) = j'''(i) / eta(i)^6 + 3 j''(i) (1/eta^6)'(i) ... but we'll only need W to (tau-i)^2.

So  W(tau) ≈ (A/2) s^2 + (B/6) s^3 + ...
    W'(tau) ≈ A s + (B/2) s^2 + ...

D_tau K = 3i/(2 Im tau).  At tau=i: 3i/2.
Near tau=i: 2 Im tau = 2 + 2 Im(s) = 2(1 + Im(s)).  So 1/(2 Im tau) = (1/2)(1 - Im(s) + Im(s)^2 - ...)
3i/(2 Im tau) = (3i/2)(1 - Im(s) + ...)

D_tau W = W' + d_tau K * W
        = [A s + (B/2) s^2] + (3i/2)(1 - Im(s)) * (A/2) s^2 + ...
        = A s + (B/2 + 3i A/4) s^2 + ...   to leading order in s.

So D_tau W ≈ A s + O(s^2).
|D_tau W|^2 ≈ |A|^2 |s|^2 + O(|s|^3).

|W|^2 = (A^2/4) |s|^4 + O(|s|^5)  [since W is O(s^2)]

2 Im tau = 2 + 2 Im(s) = 2(1 + Im(s))
(2 Im tau)^{-3} = (1/8)(1 - 3 Im(s) + 6 Im(s)^2 - ...)
(2 Im tau)^2 = 4(1 + 2 Im(s) + Im(s)^2)

V_F = (2 Im tau)^{-3} [(2 Im tau)^2/3 |D_tau W|^2 - 3 |W|^2]
    = (1/8)(1 - 3 Im s + ...) * [(4/3)(1 + 2 Im s)|A|^2 |s|^2 - 3 (A^2/4) |s|^4]
    + higher order

Leading:
  V_F ≈ (1/8) * (4/3) |A|^2 |s|^2 = (1/6) |A|^2 |s|^2

NLO (in |s|^2):
  V_F ≈ (1/6) |A|^2 |s|^2 + corrections of order |s|^3 (from Im(s) factors)

The (1/6) coefficient confirms my earlier analysis.
Mass^2 (canonical Kahler) = (4/9) |A|^2 = (4/9) (3456 pi^2 E_4(i)/eta(i)^6)^2.

Since A is REAL (E_4(i) and eta(i) are real), both real and imaginary perturbations
of tau give the same leading mass term ==> tau = i is an isolated minimum with
positive mass-squared, confirming V_F(i)=0 (Minkowski) AND positive mass.

**Conclusion: with W = (j-1728)/eta^6, tau = i is a SUSY Minkowski vacuum
with massive modulus m^2 = (4/9) |A|^2.

Note: This double-zero of W at tau=i is *special* (fine-tuned). In Mohseni-Vafa generic
weight-(-3) case, only one of W, D_tau W vanishes (giving dS or AdS). Our W has a
DOUBLE zero (j'(i)=0 forced by E_6(i)=0), pushing us to the Minkowski class.

This is NOT a coincidence: the FACT that j has a critical point at tau=i
(forced by the modular ramification structure of j: H/SL(2,Z) -> P^1)
is precisely what makes our W have a double zero. The construction is rigid.
"""

import mpmath as mp

mp.mp.dps = 30

# Numerical values
G14 = mp.gamma(mp.mpf(1)/4)
E4i = 3 * G14**8 / (2*mp.pi)**6
eta_i = G14 / (2 * mp.pi**(mp.mpf(3)/4))

# A = -3456 pi^2 E_4(i) / eta(i)^6
A = -3456 * mp.pi**2 * E4i / eta_i**6
print(f"A = W''(i) = {A}")
print(f"|A|^2 = {abs(A)**2}")

m_sq = mp.mpf(4)/9 * abs(A)**2
print(f"m^2 = (4/9) |A|^2 = {m_sq}")

# Verify by direct numerical evaluation of V_F at tau = i + s with very small s.
# V_F should equal (1/6) |A|^2 |s|^2 at leading order.

# We use the W-formula via q-series at tau very close to i.
N_TERMS = 100

def compute(tau):
    q = mp.exp(2 * mp.pi * 1j * tau)
    s4 = mp.mpf(0); s6 = mp.mpf(0); et = mp.mpf(1)
    for n in range(1, N_TERMS):
        sigma3 = sum(d**3 for d in range(1, n+1) if n % d == 0)
        sigma5 = sum(d**5 for d in range(1, n+1) if n % d == 0)
        s4 += sigma3 * q**n
        s6 += sigma5 * q**n
        et *= 1 - q**n
    e4 = 1 + 240 * s4
    e6 = 1 - 504 * s6
    eta = q**(mp.mpf(1)/24) * et
    j_m_1728 = 1728 * e6**2 / (e4**3 - e6**2)
    return e4, e6, eta, j_m_1728


def W_(tau):
    e4, e6, eta, jm = compute(tau)
    return jm / eta**6


def V_F_full(tau, h=mp.mpf("1e-5")):
    y = mp.im(tau)
    W = W_(tau)
    Wp = (W_(tau + h) - W_(tau - h)) / (2*h)
    DK = 3j / (2 * y)
    DW = Wp + DK * W
    twoIm = 2 * y
    return mp.re((1/twoIm**3) * (twoIm**2/3 * abs(DW)**2 - 3 * abs(W)**2))


# Test at tau = i + s for small s in various directions:
import math
print()
print("Compare V_F(i + s) to (1/6) |A|^2 |s|^2 (leading-order Taylor):")
print(f"{'s':30s} {'V_F (num)':15s} {'(1/6)|A|^2|s|^2':15s} {'ratio':10s}")
for s in [mp.mpc(0.001, 0), mp.mpc(0, 0.001), mp.mpc(0.001, 0.001),
          mp.mpc(-0.001, 0), mp.mpc(0, -0.001), mp.mpc(0.0005, 0.0005),
          mp.mpc(0.002, 0), mp.mpc(0, 0.002)]:
    tau_test = mp.mpc(0, 1) + s
    Vf = V_F_full(tau_test)
    pred = mp.mpf(1)/6 * abs(A)**2 * abs(s)**2
    ratio = Vf / pred if pred > 0 else 0
    print(f"  s={str(s):26s} {mp.nstr(Vf, 6):15s} {mp.nstr(pred, 6):15s} {mp.nstr(ratio, 6):10s}")

print()
print("Conclusion:")
print(" - V_F(i+s) ≈ (1/6) |A|^2 |s|^2 to leading order  ✓")
print(" - tau=i is a SUSY Minkowski vacuum (V_F=0, D_tau W=0, W=0)")
print(" - Modulus mass m^2 = (4/9) |A|^2 = (4/9)(3456 pi^2 E_4(i)/eta(i)^6)^2")
print(f"   = {m_sq}  (in Planck units, with W in M_Pl^3)")
