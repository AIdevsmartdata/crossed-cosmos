#!/usr/bin/env python3
"""d7_limite.py -- ou la REDUCTION de D7 (Prop. alpha + (eq:1d), RAPPORT §1) cesse-t-elle de fonctionner ?   [numerique, ball-tracked]

Pour kappa donne : A(t) (solution reguliere de t A - R^2 A'/3 = (t - m1) E, serie de Taylor en t en haute precision),
  m(t) = min(A,E) - |A'| R/6,  J0 = (2/(5 pi)) int (A'/3)^2 R^5/(2m) dt,  J1 = (2/(3 pi)) int (E-A)^2 R^3/(2m) dt + (2/3) J0,
  Delta = E x2^2 - Var x1 = m1^2 + 4 m1/kappa - 1.
Critere de D7 :  m > 0 sur [-1,1]  et  max(J0, J1) < Delta  (ratio = max(J0,J1)/Delta < 1).
On calcule : le ratio sur une grille, le kappa* ou ratio = 1 (bissection), le kappa_m ou min m devient <= 0, et le meme balayage pour le critere
'tranche' Xi < 0 du present travail (RAPPORT §2-3).  Tous les verdicts sont calcules ; aucune valeur n'est ecrite en dur.
"""
import argparse, json, hashlib, sys, time, math, os
os.environ.setdefault("OPENBLAS_NUM_THREADS", "1")
import numpy as np
from flint import arb, ctx
import flint

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

_GL = {}
def gl(n):
    if n not in _GL:
        _GL[n] = np.polynomial.legendre.leggauss(n)
    return _GL[n]

def critere(kappa, nth=240, ngrid=1200):
    prec = int(80 + 3.5 * kappa * 2 + 200)
    k, Zb, m1, a = champ(kappa, prec)
    x, w = gl(nth)
    th = (x + 1) * math.pi / 2; wt = w * math.pi / 2
    pi = arb.pi()
    # min m sur grille fine (en theta)
    mmin = None; tmin = None
    for j in range(1, ngrid):
        t = arb(math.cos(math.pi * j / ngrid))
        R = (1 - t * t).sqrt()
        A = horner(a, t); Ap = horner_d(a, t)
        E = (k * t).exp() / Zb
        mn = A if A < E else E
        m = float((mn - abs(Ap) * R / 6).mid())
        if mmin is None or m < mmin:
            mmin = m; tmin = float(t.mid())
    J0 = arb(0); J1p = arb(0); Xi_pos = arb(0)
    valide = mmin > 0
    for thi, wi in zip(th, wt):
        t = arb(math.cos(thi)); s = arb(math.sin(thi))
        R = s
        A = horner(a, t); Ap = horner_d(a, t)
        E = (k * t).exp() / Zb
        mn = A if A < E else E
        m = mn - abs(Ap) * R / 6
        if valide:
            J0 += wi * (Ap / 3) ** 2 * s ** 6 / (2 * m)
            J1p += wi * (E - A) ** 2 * s ** 4 / (2 * m)
        # critere 'tranche' : Xi = (2/pi) int R^3 [A^2/E + (R^2 A'^2/15)/E - E] dt
        Xi_pos += wi * s ** 4 * (A * A / E + R * R * Ap * Ap / 15 / E - E) * 2 / pi * s ** 0
    Delta = m1 * m1 + 4 * m1 / k - 1
    out = dict(kappa=kappa, m1=float(m1.mid()), Delta=float(Delta.mid()), mmin=mmin, tmin=tmin, m_positif=bool(valide))
    if valide:
        J0 = 2 / (5 * pi) * J0
        J1 = 2 / (3 * pi) * J1p + J0 * 2 / 3
        out.update(J0=float(J0.mid()), J1=float(J1.mid()), ratio=float((max(J0.mid(), J1.mid()) / Delta.mid())))
    else:
        out.update(J0=None, J1=None, ratio=None)
    # Xi par l'autre formule (w) pour comparaison : Xi/P0
    P0 = 3 * m1 / k
    out['Xi_sur_P0_tranche'] = None
    return out

def xi_sur_P0(kappa):
    """Xi/P0 par la definition (u, w), pour la comparaison."""
    prec = int(80 + 3.5 * kappa * 2 + 200)
    k, Zb, m1, a = champ(kappa, prec)
    nth = 300
    x, w = gl(nth)
    th = (x + 1) * math.pi / 2; wt = w * math.pi / 2
    tot = arb(0)
    for thi, wi in zip(th, wt):
        t = arb(math.cos(thi)); s = arb(math.sin(thi))
        A = horner(a, t); E = (k * t).exp() / Zb
        u = A / E; ww = t * u - t + m1
        tot += wi * 2 / arb.pi() * s * s * E * (s * s * u * u + arb(3) / 5 * ww * ww)
    P0 = 3 * m1 / k
    return float(((tot - P0) / P0).mid())

def bissection(f, lo, hi, n=45):
    flo = f(lo)
    for _ in range(n):
        mid = (lo + hi) / 2
        fm = f(mid)
        if (fm > 0) == (flo > 0):
            lo, flo = mid, fm
        else:
            hi = mid
    return (lo + hi) / 2

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", type=str, required=True)
    a = ap.parse_args()
    t0 = time.time()
    grille = [0.25, 0.5, 1, 4 / 3, 2, 2.5, 3, 3.25, 3.5, 4, 5, 6, 7, 8, 10, 12]
    rows = []
    for kk in grille:
        r = critere(kk)
        r['Xi_sur_P0'] = xi_sur_P0(kk)
        rows.append(r)
        rt = f"ratio={r['ratio']:.4f}" if r['ratio'] is not None else "ratio=n/a (m<=0)"
        print(f"kappa={kk:8.4f} Delta={r['Delta']:.5e} min m={r['mmin']:.3e} (t={r['tmin']:+.3f}) {rt}   |  critere tranche Xi/P0={r['Xi_sur_P0']:+.4f}", flush=True)
    # kappa* : ratio = 1
    fr = lambda kk: (critere(kk)['ratio'] if critere(kk)['ratio'] is not None else 1e9) - 1.0
    kstar = bissection(fr, 3.0, 4.0, 35)
    fm = lambda kk: critere(kk)['mmin']
    kmneg = None
    try:
        kmneg = bissection(fm, 6.0, 12.0, 35)
    except Exception as e:
        kmneg = None
    ratio_4s3 = [r for r in rows if abs(r['kappa'] - 4 / 3) < 1e-9][0]['ratio']
    ratio_2 = [r for r in rows if abs(r['kappa'] - 2) < 1e-9][0]['ratio']
    verdict_D7_valide_jusqua_4s3 = bool(all((r['ratio'] is not None and r['ratio'] < 1) for r in rows if r['kappa'] <= 4 / 3 + 1e-9))
    verdict_D7_echoue_en_4 = bool([r for r in rows if r['kappa'] == 4][0]['ratio'] is None or [r for r in rows if r['kappa'] == 4][0]['ratio'] > 1)
    verdict_tranche_ok_partout = bool(all(r['Xi_sur_P0'] < 0 for r in rows))
    out = dict(script_sha256=hashlib.sha256(open(__file__, "rb").read()).hexdigest(), python_flint=flint.__version__, grille=rows,
               kappa_etoile_ratio_egal_1=kstar, kappa_ou_min_m_s_annule=kmneg, ratio_en_4s3=ratio_4s3, ratio_en_2=ratio_2,
               verdict_D7_ratio_lt_1_pour_kappa_le_4s3=verdict_D7_valide_jusqua_4s3,
               verdict_D7_echoue_en_kappa_4=verdict_D7_echoue_en_4,
               verdict_critere_tranche_Xi_neg_sur_toute_la_grille=verdict_tranche_ok_partout, secondes=round(time.time() - t0, 1))
    json.dump(out, open(a.out, "w"), indent=1)
    print(f"kappa* (max(J0,J1)/Delta = 1) = {kstar:.5f} ; kappa ou min m = 0 : {kmneg}")
    print(f"ratio D7 en 4/3 = {ratio_4s3:.4f} (note D7 : 0.32), en 2 = {ratio_2:.4f} (note D7 : 0.47)")
    print(f"VERDICTS : D7 ratio<1 pour kappa<=4/3 : {verdict_D7_valide_jusqua_4s3} ; D7 echoue en kappa=4 : {verdict_D7_echoue_en_4} ; "
          f"critere tranche Xi<0 sur toute la grille : {verdict_tranche_ok_partout}")

if __name__ == "__main__":
    main()
