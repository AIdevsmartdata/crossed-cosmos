#!/usr/bin/env python3
"""flux_champ_exact.py -- [numerique] flux L1 EXACT du champ explicite de D7 et encadrement de D_ch(kappa, alpha).

Pour kappa, alpha donnes (c = cos alpha, s = sin alpha), V = c [A e1 - A' z/3] + s E e2 (champ de D7, valable pour tout kappa) :
  F(kappa, alpha) = (1/(2 pi^2)) int_B |V| dy          (quadrature 3D : y1 par Gauss-Legendre en theta, (y2, rho) en polaires)
est une borne superieure de D_ch(kappa, alpha) (lemme du flux).  On calcule aussi
  B(kappa, alpha) = E x2^2 + (c^2/6) Xi(kappa)         (borne 'tranche', RAPPORT §2)  avec  Xi = <R^2 u^2> + (3/5)<w^2> - <R^2>,
  Low(kappa, alpha) = Var(<v,x>) = E x2^2 - c^2 Delta   (borne inferieure : f = <v,x> est 1-lipschitzienne).
Chaine attendue (verdicts CALCULES) :  Low <= F <= B <= E x2^2  (a la precision numerique de la quadrature), avec B = E x2^2 en alpha = pi/2.
"""
import argparse, json, hashlib, math, os, sys, time
from fractions import Fraction
os.environ.setdefault("OPENBLAS_NUM_THREADS", "1")
import numpy as np
from flint import arb, ctx
import flint

_GL = {}
def gl(n):
    if n not in _GL:
        _GL[n] = np.polynomial.legendre.leggauss(n)
    return _GL[n]

def champ(kappa, prec):
    ctx.prec = prec
    k = arb(kappa)
    I1 = k.bessel_i(1); I2 = k.bessel_i(2)
    Zb = 2 * I1 / k
    m1 = I2 / I1
    N = int(2.5 * kappa) + int(prec / 3.0) + 60
    fact = [arb(1)]
    for n in range(1, N + 4):
        fact.append(fact[-1] * n)
    kp = [arb(1)]
    for n in range(1, N + 4):
        kp.append(kp[-1] * k)
    q = [(-m1) / Zb]
    for n in range(1, N + 2):
        q.append((kp[n - 1] / fact[n - 1] - m1 * kp[n] / fact[n]) / Zb)
    a = [arb(0)] * (N + 3)
    for mm in range(N + 1, 0, -1):
        a[mm - 1] = (3 * q[mm] + (mm + 1) * a[mm + 1]) / (mm + 2)
    return k, Zb, m1, a[:N + 1]

def horner(a, t):
    r = arb(0)
    for c in reversed(a):
        r = r * t + c
    return r

def horner_d(a, t):
    r = arb(0)
    for n in range(len(a) - 1, 0, -1):
        r = r * t + n * a[n]
    return r

def tabule(kappa, nt=240):
    prec = int(80 + 3.5 * kappa * 2 + 200)
    k, Zb, m1, a = champ(kappa, prec)
    x, w = gl(nt)
    th = (x + 1) * math.pi / 2
    wt = w * math.pi / 2
    T = np.cos(th); S = np.sin(th)
    A = np.zeros(nt); Ap = np.zeros(nt); E = np.zeros(nt)
    Xi_acc = arb(0)
    for i, ti in enumerate(T):
        t = arb(float(ti)); s = arb(float(S[i]))
        Av = horner(a, t); Apv = horner_d(a, t); Ev = (k * t).exp() / Zb
        A[i] = float(Av.mid()); Ap[i] = float(Apv.mid()); E[i] = float(Ev.mid())
        u = Av / Ev; ww = t * u - t + m1
        Xi_acc += float(wt[i]) * 2 / arb.pi() * s * s * Ev * (s * s * u * u + arb(3) / 5 * ww * ww)
    P0 = 3 * m1 / k
    Xi = float((Xi_acc - P0).mid())
    Delta = float((m1 * m1 + 4 * m1 / k - 1).mid())
    return dict(T=T, S=S, wt=wt, A=A, Ap=Ap, E=E, m1=float(m1.mid()), kappa=kappa, Xi=Xi, Delta=Delta, Ex22=float((m1 / k).mid()))

def flux(tab, alpha, nr=40, nphi=80):
    c, s = math.cos(alpha), math.sin(alpha)
    xr, wr = gl(nr); xp, wp = gl(nphi)
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
        total += tab['wt'][i] * tab['S'][i] * inner
    return total / math.pi

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--kappas", type=str, default="0.25,0.5,1,1.3333333333333333,2,3,4,6,8,10,15,20,30,50")
    ap.add_argument("--alphas", type=str, default="0,15,30,45,60,75,90")
    ap.add_argument("--out", type=str, required=True)
    a = ap.parse_args()
    t0 = time.time()
    rows = []
    ok_all = True
    for kk in [float(Fraction(x)) for x in a.kappas.split(",")]:
        tab = tabule(kk)
        for ad in [float(x) for x in a.alphas.split(",")]:
            al = math.radians(ad)
            c2 = math.cos(al) ** 2
            F = flux(tab, al)
            B = tab['Ex22'] + c2 * tab['Xi'] / 6
            Low = tab['Ex22'] - c2 * tab['Delta']
            tol = 5e-7
            chaine = (Low <= F + tol) and (F <= B + tol) and (B <= tab['Ex22'] + tol)
            ok_all = ok_all and chaine
            rows.append(dict(kappa=kk, alpha_deg=ad, Ex22=tab['Ex22'], Xi=tab['Xi'], Delta=tab['Delta'], Low=Low, F=F, B=B, chaine_ok=bool(chaine)))
            print(f"kappa={kk:8.4f} alpha={ad:5.1f}  Low={Low:.7f} <= F={F:.7f} <= B={B:.7f} <= E x2^2={tab['Ex22']:.7f}   {'OK' if chaine else 'ECHEC'}", flush=True)
    out = dict(script_sha256=hashlib.sha256(open(__file__, "rb").read()).hexdigest(), python_flint=flint.__version__, numpy=np.__version__, lignes=rows, chaine_ok_partout=bool(ok_all),
               secondes=round(time.time() - t0, 1))
    json.dump(out, open(a.out, "w"), indent=1)
    print(f"BILAN chaine Low <= F <= B <= E x2^2 : {'TOUT_OK' if ok_all else 'ECHEC'} sur {len(rows)} couples (kappa, alpha) ; {out['secondes']} s")
    sys.exit(0 if ok_all else 1)

if __name__ == "__main__":
    main()
