#!/usr/bin/env python3
"""Exploration : verifie que le champ A(t) calcule par la serie de Taylor en t (a0 par serie, recursion) satisfait
   (i) l'EDO  t A - (1-t^2) A'/3 = (t - m1) E   (residu), (ii) A(t) = 3 R^-3 int_t^1 q R ds (quadrature mpmath), (iii) bornes A(+-1).
Puis balaye kappa : bornes (I-ID) et signe de Xi.
"""
import sys, math
from mpmath import mp, mpf, quad, sqrt, exp, besseli, pi as mpi
from flint import arb, ctx
sys.path.insert(0, __file__.rsplit('/', 1)[0])
from ratio_scan import champ, evalpoly, evalpoly_d

def check(kappa):
    prec = int(60 + 3.2 * 3 * kappa + 200)
    F = champ(kappa, prec)
    k, Zb, m1, a = F['k'], F['Zb'], F['m1'], F['a']
    mp.dps = 40
    kk = mpf(kappa)
    Zm = 2 * besseli(1, kk) / kk
    m1m = besseli(2, kk) / besseli(1, kk)
    print(f"kappa={kappa}: m1(arb)={float(m1.mid()):.12f} m1(mp)={float(m1m):.12f}")
    worst_res = 0.0; worst_q = 0.0
    for t0 in [-0.97, -0.6, -0.1, 0.0, 0.3, 0.75, 0.95, 0.999]:
        t = arb(t0)
        A = evalpoly(a, t); Ap = evalpoly_d(a, t)
        E = (k * t).exp() / Zb
        res = t * A - (1 - t * t) * Ap / 3 - (t - m1) * E
        # quadrature
        tt = mpf(t0)
        f = lambda s: (s - m1m) * exp(kk * s) / Zm * sqrt(1 - s * s)
        if t0 >= 0:
            I = quad(f, [tt, 1])
        else:
            I = -quad(f, [-1, tt])
        Aq = 3 * I / (1 - tt * tt) ** mpf(1.5)
        worst_res = max(worst_res, abs(float(res.mid())))
        worst_q = max(worst_q, abs(float(A.mid()) - float(Aq)) / (abs(float(Aq)) + 1e-300))
        print(f"   t={t0:+.3f}  A={float(A.mid()):.10e}  quad={float(Aq):.10e}  rel.diff={abs(float(A.mid()) - float(Aq)) / (abs(float(Aq)) + 1e-300):.1e}  |ODE res|={abs(float(res.mid())):.1e}")
    # bornes
    for te in (1, -1):
        t = arb(te)
        A = evalpoly(a, t)
        E = (k * t).exp() / Zb
        att = (1 - m1) * E if te == 1 else (1 + m1) * E
        print(f"   A({te:+d}) = {float(A.mid()):.10e}  attendu {float(att.mid()):.10e}")

if __name__ == "__main__":
    for kk in [float(v) for v in sys.argv[1:]] or [0.7, 4.0, 15.0]:
        check(kk)
