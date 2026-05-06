#!/usr/bin/env python3
"""
M140 / Step 1 -- Compute the King-King (2002.00969) weight-2 A4 modular forms
Y_1, Y_2, Y_3 at and near tau = i.

Reference (verbatim, eq. 19 of King-King 2002.00969):
  Y_3^(2)(tau) = ( Y_1, Y_2, Y_3 )^T
  Y_1(tau) = (1 + 12q + 36q^2 + 12q^3 + 84q^4 + 72q^5 + ...)
  Y_2(tau) = -6 q^(1/3) (1 + 7q + 8q^2 + 18q^3 + 14q^4 + ...)
  Y_3(tau) = -18 q^(2/3) (1 + 2q + 5q^2 + 4q^3 + 8q^4 + ...)

where q = exp(2 pi i tau).

Constraint (eq. 20):  Y_2^2 + 2 Y_1 Y_3 = 0    (1''-singlet vanishes)

We compute Y_i(tau) for tau = i + epsilon at multiple epsilon, and look at
the K-K best-fit point tau ~ 0.036 + 2.35 i for sanity.
"""

import mpmath as mp

mp.mp.dps = 40

# Use the exact eta-quotient definitions of K-K eq.(18) for high accuracy:
#
#  Y_1(tau) = (i / 2pi) [ eta'(tau/3)/eta(tau/3) + eta'((tau+1)/3)/eta((tau+1)/3)
#                       + eta'((tau+2)/3)/eta((tau+2)/3) - 27 eta'(3 tau)/eta(3 tau) ]
#  Y_2(tau) = (-i / pi) [ eta'(tau/3)/eta(tau/3) + omega^2 eta'((tau+1)/3)/eta((tau+1)/3)
#                       + omega eta'((tau+2)/3)/eta((tau+2)/3) ]
#  Y_3(tau) = (-i / pi) [ eta'(tau/3)/eta(tau/3) + omega eta'((tau+1)/3)/eta((tau+1)/3)
#                       + omega^2 eta'((tau+2)/3)/eta((tau+2)/3) ]
#
# We compute eta and eta' via the q-product with high-N truncation.

N_TERMS = 200
omega = mp.exp(2j * mp.pi / 3)


def eta_and_dlog_eta(tau):
    """Return (eta(tau), eta'(tau)/eta(tau)) using
    eta(tau) = q^(1/24) prod_{n>=1} (1 - q^n).
    eta'/eta = (2 pi i)/24 + (2 pi i) sum_{n>=1} -n q^n / (1 - q^n)
            = (2 pi i)[ 1/24 - sum_{n>=1} n q^n / (1 - q^n) ]
    """
    q = mp.exp(2j * mp.pi * tau)
    # eta:
    prod = mp.mpf(1)
    for n in range(1, N_TERMS):
        prod *= 1 - q**n
    eta = q**(mp.mpf(1)/24) * prod
    # dlog_eta = (2 pi i) [1/24 - sum n q^n/(1-q^n)]
    s = mp.mpc(0, 0)
    for n in range(1, N_TERMS):
        s += n * q**n / (1 - q**n)
    dlog = 2j * mp.pi * (mp.mpf(1)/24 - s)
    return eta, dlog


def Yvec(tau):
    """Return (Y_1, Y_2, Y_3) at tau."""
    a = tau / 3
    b = (tau + 1) / 3
    c = (tau + 2) / 3
    d = 3 * tau

    _, da = eta_and_dlog_eta(a)
    _, db = eta_and_dlog_eta(b)
    _, dc = eta_and_dlog_eta(c)
    _, dd = eta_and_dlog_eta(d)

    Y1 = (1j / (2 * mp.pi)) * (da + db + dc - 27 * dd)
    Y2 = (-1j / mp.pi) * (da + omega**2 * db + omega * dc)
    Y3 = (-1j / mp.pi) * (da + omega * db + omega**2 * dc)
    return Y1, Y2, Y3


def report(tau, label):
    Y1, Y2, Y3 = Yvec(tau)
    cons = Y2**2 + 2 * Y1 * Y3  # should be 0
    print(f"\n{label}: tau = {tau}")
    print(f"  Y_1 = {mp.nstr(Y1, 10)}")
    print(f"  Y_2 = {mp.nstr(Y2, 10)}")
    print(f"  Y_3 = {mp.nstr(Y3, 10)}")
    print(f"  |Y_1| = {mp.nstr(abs(Y1), 6)},  |Y_2| = {mp.nstr(abs(Y2), 6)},  |Y_3| = {mp.nstr(abs(Y3), 6)}")
    print(f"  constraint Y_2^2 + 2 Y_1 Y_3 = {mp.nstr(cons, 6)} (should be ~ 0)")
    return Y1, Y2, Y3


print("=" * 70)
print("Reference / sanity points")
print("=" * 70)

# tau = i*infty asymptote:  Y -> (1, 0, 0)
# tau = i (S fixed point):  Y_1 should be |Y1|=1.0225...,  the K-K paper says
# the point tau = i ALSO has structure but is not at the cusp.

report(mp.mpc(0, 1), "tau = i (S-fixed)")
report(mp.mpc(-mp.mpf(1)/2, mp.sqrt(3)/2), "tau = omega = exp(2 pi i / 3) (ST-fixed)")
report(mp.mpc(0, 5), "tau = 5 i (near cusp)")
report(mp.mpc(0, 10), "tau = 10 i (deeper near cusp)")

print("\n" + "=" * 70)
print("King-King (2002.00969) BEST-FIT POINT for the quark sector")
print("=" * 70)
report(mp.mpc(0.0361, 2.352), "K-K Table 5  tau = 0.0361 + 2.352 i")
report(mp.mpc(0.0361, 2.353), "K-K Table 6  tau = 0.0361 + 2.353 i")

print("\n" + "=" * 70)
print("Re tau tilt analysis around tau = i")
print("=" * 70)
print("Below, we set tau = i + epsilon (real epsilon) and watch Y_i.")
print()
header = f"{'eps':>10s} {'|Y1|':>14s} {'|Y2|':>14s} {'|Y3|':>14s} {'Y2/Y1':>14s} {'Y3/Y1':>14s}"
print(header)
print('-' * len(header))
import math
for eps_log in range(-5, 0):
    eps = mp.mpf(10)**eps_log
    Y1, Y2, Y3 = Yvec(mp.mpc(eps, 1))
    ratio2 = Y2 / Y1
    ratio3 = Y3 / Y1
    print(f"{mp.nstr(eps, 4):>10s} {mp.nstr(abs(Y1), 6):>14s} {mp.nstr(abs(Y2), 6):>14s} "
          f"{mp.nstr(abs(Y3), 6):>14s} {mp.nstr(abs(ratio2), 6):>14s} {mp.nstr(abs(ratio3), 6):>14s}")

# Same with imaginary epsilon: tau = i + i eps  (Im tau shift only)
print()
print("Im-only tilt: tau = i (1 + delta), delta real small")
print(header)
print('-' * len(header))
for delta_log in range(-5, 0):
    delta = mp.mpf(10)**delta_log
    Y1, Y2, Y3 = Yvec(mp.mpc(0, 1 + delta))
    ratio2 = Y2 / Y1
    ratio3 = Y3 / Y1
    print(f"{mp.nstr(delta, 4):>10s} {mp.nstr(abs(Y1), 6):>14s} {mp.nstr(abs(Y2), 6):>14s} "
          f"{mp.nstr(abs(Y3), 6):>14s} {mp.nstr(abs(ratio2), 6):>14s} {mp.nstr(abs(ratio3), 6):>14s}")
