#!/usr/bin/env python3
"""Exploration (NUMERIQUE, non certifiee) : le critere reduit de la preuve D7 (Prop. alpha + (eq:1d)) pour kappa > 4/3.

Pour kappa donne : champ A(t) (solution bornee de t A - (1-t^2) A'/3 = q), E(t) = e^{kappa t}/Z,
  m(t) = min(A,E) - |A'| R/6,   J0 = (2/(5 pi)) int (A'/3)^2 R^5/(2m) dt,
  J1 = (2/(3 pi)) int (E-A)^2 R^3/(2m) dt + (2/3) J0,   Delta = E x2^2 - Var x1 = m1^2 + 4 m1/kappa - 1.
Critere D7 : m > 0 sur [-1,1] et max(J0,J1) < Delta  (ratio < 1).
A est calcule par sa serie de Taylor en t (A est ENTIERE en t), a_0 = 3 int_0^1 q sqrt(1-s^2) ds par serie, puis recursion.
"""
import sys, math
import numpy as np
from flint import arb, ctx

def champ(kappa, prec):
    ctx.prec = prec
    k = arb(kappa)
    I1 = k.bessel_i(1); I2 = k.bessel_i(2)
    Zb = 2 * I1 / k
    m1 = I2 / I1
    N = int(2.2 * kappa) + int(prec / 3.0) + 60
    # q_n : coefficients de q(s) = (s - m1) e^{k s} / Zb
    fact = [arb(1)]
    for n in range(1, N + 3):
        fact.append(fact[-1] * n)
    kp = [arb(1)]
    for n in range(1, N + 3):
        kp.append(kp[-1] * k)
    q = [(-m1 * kp[0] / fact[0]) / Zb]
    for n in range(1, N + 2):
        q.append((kp[n - 1] / fact[n - 1] - m1 * kp[n] / fact[n]) / Zb)
    # b_n = int_0^1 s^n sqrt(1-s^2) ds = (1/2) Gamma((n+1)/2) Gamma(3/2) / Gamma((n+4)/2)
    g32 = arb(3) / 2
    g32 = g32.gamma()
    a0 = arb(0)
    for n in range(N + 1):
        bn = ((arb(n + 1) / 2).gamma() * g32 / (arb(n + 4) / 2).gamma()) / 2
        a0 += q[n] * bn
    a0 = 3 * a0
    a = [a0, -3 * q[0]]
    for n in range(1, N):
        a.append(((n + 2) * a[n - 1] - 3 * q[n]) / (n + 1))
    return dict(k=k, Zb=Zb, m1=m1, a=a, N=N)

def evalpoly(a, t):
    r = arb(0)
    for c in reversed(a):
        r = r * t + c
    return r

def evalpoly_d(a, t):
    r = arb(0)
    for n in range(len(a) - 1, 0, -1):
        r = r * t + n * a[n]
    return r

def scan(kappa, nth=300, prec=None, verbose=False):
    if prec is None:
        prec = int(40 + 3.2 * 2 * kappa * 1.5 + 200)
    F = champ(kappa, prec)
    k, Zb, m1, a = F['k'], F['Zb'], F['m1'], F['a']
    x, w = np.polynomial.legendre.leggauss(nth)
    th = (x + 1) * math.pi / 2
    wt = w * math.pi / 2
    J0 = arb(0); J1p = arb(0)
    mmin = None; tmin = None
    pi = arb.pi()
    for thi, wi in zip(th, wt):
        t = arb(math.cos(thi))
        R = (1 - t * t).sqrt()
        A = evalpoly(a, t)
        Ap = evalpoly_d(a, t)
        E = (k * t).exp() / Zb
        mn = A if A < E else E
        m = mn - abs(Ap) * R / 6
        mf = float(m.mid())
        if mmin is None or mf < mmin:
            mmin = mf; tmin = float(t.mid())
        sin = arb(math.sin(thi))
        if mf <= 0:
            continue
        J0 += wi * (Ap / 3) ** 2 * sin ** 6 / (2 * m)
        J1p += wi * (E - A) ** 2 * sin ** 4 / (2 * m)
    J0 = 2 / (5 * pi) * J0
    J1 = 2 / (3 * pi) * J1p + J0 * 2 / 3
    Delta = m1 * m1 + 4 * m1 / k - 1
    ratio = max(float(J0.mid()), float(J1.mid())) / float(Delta.mid())
    return dict(kappa=kappa, m1=float(m1.mid()), Ex22=float((m1 / k).mid()), Delta=float(Delta.mid()), J0=float(J0.mid()), J1=float(J1.mid()),
                ratio=ratio, mmin=mmin, tmin=tmin, rad=float(J0.rad()), prec=prec, N=F['N'])

if __name__ == "__main__":
    ks = [float(s) for s in sys.argv[1:]] or [0.5, 4 / 3, 2, 3, 4, 5, 6]
    for kk in ks:
        r = scan(kk)
        print(f"kappa={r['kappa']:8.4f} m1={r['m1']:.6f} E[x2^2]={r['Ex22']:.6f} Delta={r['Delta']:.6e} J0={r['J0']:.6e} J1={r['J1']:.6e} ratio={r['ratio']:.4f} "
              f"min m={r['mmin']:.3e} at t={r['tmin']:+.3f}  (rad J0 {r['rad']:.1e}, prec {r['prec']}, N {r['N']})", flush=True)
