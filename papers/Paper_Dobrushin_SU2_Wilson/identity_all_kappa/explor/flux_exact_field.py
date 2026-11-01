#!/usr/bin/env python3
"""Exploration (NUMERIQUE) : flux L1 EXACT du champ explicite de D7, F(kappa, alpha) = (1/(2 pi^2)) int_B |V_alpha| dy,
compare a E_kappa[x2^2].  Si F(kappa, alpha) <= E x2^2 pour tout alpha, le CHAMP de D7 prouve l'identite (seule l'estimation
du second ordre, Prop. alpha, est trop grossiere).  Sinon il faut aussi ameliorer le champ.

V_alpha = cos(a) [A(y1) e1 - A'(y1) z / 3] + sin(a) E(y1) e2,  z = (0,y2,y3,y4).
|V|^2 = cos^2 A^2 + (sin E - cos (A'/3) y2)^2 + cos^2 (A'/3)^2 rho^2,   rho^2 = y3^2 + y4^2.
Region : y1^2 + y2^2 + rho^2 <= 1, mesure 2 pi rho drho dy2 dy1.  Pour y1 fixe : (y2, rho) = r (cos phi, sin phi), r in [0,R], phi in [0,pi],
  rho drho dy2 = r^2 sin(phi) dr dphi.
"""
import sys, math
import numpy as np
from flint import arb, ctx
sys.path.insert(0, __file__.rsplit('/', 1)[0])
from ratio_scan import champ, evalpoly, evalpoly_d

def tabule(kappa, nt=240, prec=None):
    if prec is None:
        prec = int(40 + 3.2 * 2 * kappa * 1.5 + 200)
    F = champ(kappa, prec)
    k, Zb, m1, a = F['k'], F['Zb'], F['m1'], F['a']
    x, w = np.polynomial.legendre.leggauss(nt)
    th = (x + 1) * math.pi / 2
    wt = w * math.pi / 2          # dt = sin(th) dth
    T = np.cos(th); S = np.sin(th)
    A = np.zeros(nt); Ap = np.zeros(nt); E = np.zeros(nt)
    for i, ti in enumerate(T):
        t = arb(float(ti))
        A[i] = float(evalpoly(a, t).mid()); Ap[i] = float(evalpoly_d(a, t).mid()); E[i] = float(((k * t).exp() / Zb).mid())
    return dict(T=T, S=S, wt=wt, A=A, Ap=Ap, E=E, m1=float(m1.mid()), kappa=kappa)

def flux(tab, alpha, nr=48, nphi=96):
    c, s = math.cos(alpha), math.sin(alpha)
    xr, wr = np.polynomial.legendre.leggauss(nr)
    xp, wp = np.polynomial.legendre.leggauss(nphi)
    phi = (xp + 1) * math.pi / 2; wphi = wp * math.pi / 2
    cphi, sphi = np.cos(phi), np.sin(phi)
    total = 0.0
    for i in range(len(tab['T'])):
        R = tab['S'][i]
        r = (xr + 1) * R / 2; wrr = wr * R / 2
        Ai, Api, Ei = tab['A'][i], tab['Ap'][i], tab['E'][i]
        y2 = np.outer(r, cphi); rho = np.outer(r, sphi)
        V2 = (c * Ai) ** 2 + (s * Ei - c * (Api / 3) * y2) ** 2 + (c * Api / 3) ** 2 * rho ** 2
        integrand = np.sqrt(V2) * (r ** 2)[:, None] * sphi[None, :]
        inner = np.einsum('i,ij,j->', wrr, integrand, wphi)
        total += tab['wt'][i] * tab['S'][i] * inner / tab['S'][i]   # dt = sin(th) dth -> weight wt*S ; the (1/S) cancels : keep explicit below
    return total

def flux2(tab, alpha, nr=48, nphi=96):
    c, s = math.cos(alpha), math.sin(alpha)
    xr, wr = np.polynomial.legendre.leggauss(nr)
    xp, wp = np.polynomial.legendre.leggauss(nphi)
    phi = (xp + 1) * math.pi / 2; wphi = wp * math.pi / 2
    cphi, sphi = np.cos(phi), np.sin(phi)
    total = 0.0
    for i in range(len(tab['T'])):
        R = tab['S'][i]
        r = (xr + 1) * R / 2; wrr = wr * R / 2
        Ai, Api, Ei = tab['A'][i], tab['Ap'][i], tab['E'][i]
        y2 = np.outer(r, cphi); rho = np.outer(r, sphi)
        V2 = (c * Ai) ** 2 + (s * Ei - c * (Api / 3) * y2) ** 2 + (c * Api / 3) ** 2 * rho ** 2
        integrand = np.sqrt(V2) * (r ** 2)[:, None] * sphi[None, :]
        inner = np.einsum('i,ij,j->', wrr, integrand, wphi)
        total += tab['wt'][i] * tab['S'][i] * inner      # int dt = int sin(th) dth
    return total / math.pi        # (1/(2 pi^2)) * 2 pi = 1/pi

if __name__ == "__main__":
    ks = [float(v) for v in sys.argv[1:]] or [1.3333333333, 3, 4, 6, 10]
    alphas = [math.pi / 2 * j / 12 for j in range(13)]
    for kk in ks:
        tab = tabule(kk)
        ex22 = tab['m1'] / kk
        print(f"kappa={kk}  E[x2^2]={ex22:.8f}", flush=True)
        worst = -1e9
        for al in alphas:
            F = flux2(tab, al)
            worst = max(worst, F - ex22)
            print(f"   alpha={math.degrees(al):6.2f} deg  F={F:.8f}   F - E x2^2 = {F - ex22:+.3e}", flush=True)
        print(f"   max_alpha (F - E x2^2) = {worst:+.3e}", flush=True)
