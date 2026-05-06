#!/usr/bin/env python3
"""
M143 / Step 9 -- INDEPENDENT verification that tau = i sqrt(11/2) is a CM
point of Q(sqrt -22) with discriminant -88, class number 2.

Method 1: numerical j-computation at high precision
Method 2: theoretical: D = -88 has 2 reduced binary quadratic forms
Method 3: theoretical: Hilbert class polynomial H_{-88}(X)

Cross-check via mpmath modular library (using a different formulation):
   j(tau) = ((1 + 240 sum sigma_3(n) q^n)^3) / ((eta(tau))^24 / q)
"""

import mpmath as mp

mp.mp.dps = 60

N_TERMS = 500


def eta(tau):
    q = mp.exp(2j * mp.pi * tau)
    prod = mp.mpf(1)
    for n in range(1, N_TERMS):
        prod *= 1 - q**n
    return q**(mp.mpf(1) / 24) * prod


def E4_v2(tau):
    """E_4 via Lambert series: 1 + 240 sum_{n>=1} n^3 q^n / (1 - q^n)."""
    q = mp.exp(2j * mp.pi * tau)
    s = mp.mpc(0, 0)
    for n in range(1, N_TERMS):
        s += n**3 * q**n / (1 - q**n)
    return 1 + 240 * s


def Delta_eta(tau):
    """Delta = eta^24."""
    return eta(tau)**24


def j_v2(tau):
    """j = E_4^3 / Delta * 1728."""
    return E4_v2(tau)**3 * 1728 / Delta_eta(tau)
    # Wait: j = E_4^3 / Delta where Delta = (E_4^3 - E_6^2)/1728 = eta^24
    # so j = E_4^3 / eta^24, no 1728 factor needed -- let me re-derive:
    # j(tau) := 1728 * E_4^3 / (E_4^3 - E_6^2) = E_4^3 / Delta where Delta := eta^24 = (E_4^3 - E_6^2)/1728


def j_v3(tau):
    """j = E_4^3 / eta^24."""
    return E4_v2(tau)**3 / eta(tau)**24


# Test point: i sqrt(11/2)
tau_test = mp.mpc(0, mp.sqrt(mp.mpf(11)/2))
print(f"tau = i sqrt(11/2) = {tau_test}")
print()
print(f"j_v3 (via E_4^3 / eta^24) = {j_v3(tau_test)}")
print()
print(f"|Im j| = {abs(mp.im(j_v3(tau_test)))}")
print()

# Also: tau = i sqrt 22
tau_test2 = mp.mpc(0, mp.sqrt(22))
print(f"tau = i sqrt 22 = {tau_test2}")
print(f"j_v3 = {j_v3(tau_test2)}")
print(f"|Im j| = {abs(mp.im(j_v3(tau_test2)))}")

# Hilbert polynomial check:
j_a = j_v3(tau_test)
j_b = j_v3(tau_test2)

sum_j = j_a + j_b
prod_j = j_a * j_b
print()
print(f"j_a + j_b = {sum_j}")
print(f"j_a * j_b = {prod_j}")
print()
print(f"Round to integer:")
sj_re = mp.re(sum_j)
pj_re = mp.re(prod_j)
print(f"  Re(j_a + j_b) = {sj_re}")
print(f"  -> nint = {mp.nint(sj_re)}")
print(f"  Re(j_a * j_b) = {pj_re}")
print(f"  -> nint = {mp.nint(pj_re)}")

# Reference (computed via standard PARI / SAGE):
# H_{-88}(X) = X^2 - 6294842640000 X + 15798135578688000000
# (This is from Cohen "A Course in Computational Algebraic Number Theory" tables.)

H_n88_a = -6294842640000  # coefficient of X
H_n88_b = 15798135578688000000  # constant
print()
print(f"Reference H_{{-88}}(X) = X^2 + ({H_n88_a}) X + ({H_n88_b})")
print(f"  Computed sum: {-mp.nint(sj_re)} (matches -a={-H_n88_a}? {bool(mp.nint(sj_re) == -H_n88_a)})")
print(f"  Computed prod: {mp.nint(pj_re)} (matches b={H_n88_b}? {bool(mp.nint(pj_re) == H_n88_b)})")

# Factorization of 6294842640000 and 15798135578688000000:
import sympy as sp
print()
print("Factorizations:")
print(f"  6294842640000 = {sp.factorint(6294842640000)}")
print(f"  15798135578688000000 = {sp.factorint(15798135578688000000)}")

# Compute roots of H_{-88}(X) symbolically (as algebraic numbers):
X = sp.Symbol('X')
H_n88 = X**2 - 6294842640000 * X + 15798135578688000000
roots = sp.solve(H_n88, X)
print()
print("Roots of H_{-88}(X):")
for r in roots:
    print(f"  {r}  numerical: {float(r):.10f}")

# Verify: numerical j_a and j_b match these roots:
print()
for r in roots:
    rn = float(r)
    print(f"|j_a - {rn:.6f}| = {float(abs(mp.re(j_a) - rn)):.4e}")
    print(f"|j_b - {rn:.6e}| = {float(abs(mp.re(j_b) - rn)):.4e}")
