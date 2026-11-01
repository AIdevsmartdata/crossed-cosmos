#!/usr/bin/env python3
"""ident_num_mp.py -- verification NUMERIQUE INDEPENDANTE de l'identite du RAPPORT §2 (mpmath seul, sans python-flint, sans serie de Taylor en t).

u(t) = A(t)/E(t) est calcule par sa REPRESENTATION INTEGRALE a integrande positive :
    t <= m1 :  u(t) = 3 R^-3 int_{-1}^t (m1 - s) R(s) e^{-kappa (t-s)} ds ,
    t >= m1 :  u(t) = 3 R^-3 int_t^1 (s - m1) R(s) e^{ kappa (s-t)} ds ,
(substitution s = cos(phi), integrandes entieres en phi), puis les moyennes <g> = (2/pi) int g R E dt par quadrature tanh-sinh (mpmath.quad) en theta.
Forme SANS DERIVEE de la somme de carres :  u' = 3w/R^2 - kappa u  donne
    S = (1/15)<R^4 (4u'^2 + 2 kappa u u' + kappa^2 u^2)> = (1/5) < 12 w^2 - 6 kappa R^2 u w + kappa^2 R^4 u^2 > = (1/5)< 12 (w - kappa R^2 u/4)^2 + kappa^2 R^4 u^2/4 > >= 0.
Verdicts calcules : residu de  Xi + 3 Delta + S = 0 ; forme (ID) :  <R^2 u^2> + 3<w^2> - (6 kappa/5)<R^2 u w> + (kappa^2/5)<R^4 u^2> = 3 Var x1 ;
Xi < 0 ; Xi <= -3 Delta.   Etiquette : [numerique] (30 chiffres, quadrature adaptative).
"""
import argparse, json, hashlib, sys, time
from fractions import Fraction
from mpmath import mp, mpf, quad, sin, cos, exp, pi, besseli, acos, sqrt
import mpmath

def un_kappa(kfr, dps):
    mp.dps = dps
    k = mpf(kfr.numerator) / kfr.denominator
    I1 = besseli(1, k); I2 = besseli(2, k)
    Zb = 2 * I1 / k
    m1 = I2 / I1
    thm = acos(m1)                       # t = m1  <=>  theta = thm
    def u_of_theta(th):
        t = cos(th); R = sin(th)
        if th >= thm:                     # t <= m1 : representation de gauche
            f = lambda ph: (m1 - cos(ph)) * sin(ph) ** 2 * exp(-k * (t - cos(ph)))
            I = quad(f, [th, pi])
        else:                             # t >= m1 : representation de droite
            f = lambda ph: (cos(ph) - m1) * sin(ph) ** 2 * exp(k * (cos(ph) - t))
            I = quad(f, [0, th])
        return 3 * I / R ** 3
    def mean(g):
        # <g> = (2/pi) int g R E dt = (2/pi) int g sin^2(th) E dth
        h = lambda th: g(th) * sin(th) ** 2 * exp(k * cos(th)) / Zb * 2 / pi
        return quad(h, [0, thm / 2, thm, (thm + pi) / 2, pi])
    cache = {}
    def U(th):
        key = th
        if key not in cache:
            cache[key] = u_of_theta(th)
        return cache[key]
    def W(th):
        return cos(th) * U(th) - cos(th) + m1
    P0 = mean(lambda th: sin(th) ** 2)
    one = mean(lambda th: mpf(1))
    mt = mean(lambda th: cos(th))
    P1 = mean(lambda th: sin(th) ** 2 * U(th) ** 2)
    W2 = mean(lambda th: W(th) ** 2)
    T1 = mean(lambda th: sin(th) ** 2 * U(th) * W(th))
    Q = mean(lambda th: sin(th) ** 4 * U(th) ** 2)
    S = (12 * W2 - 6 * k * T1 + k ** 2 * Q) / 5
    Xi = P1 + mpf(3) / 5 * W2 - 3 * m1 / k
    Delta = m1 ** 2 + 4 * m1 / k - 1
    resid = Xi + 3 * Delta + S
    Var = 1 - 3 * m1 / k - m1 ** 2
    resid_ID = P1 + 3 * W2 - mpf(6) * k / 5 * T1 + k ** 2 / 5 * Q - 3 * Var
    return dict(kappa=str(kfr), dps=dps, m1=float(m1), Xi=float(Xi), S=float(S), Delta=float(Delta), residu=float(abs(resid)), residu_ID=float(abs(resid_ID)),
                masse_ecart=float(abs(one - 1)), P0_ecart=float(abs(P0 - 3 * m1 / k)), m1_ecart=float(abs(mt - m1)),
                Xi_sur_P0=float(Xi / (3 * m1 / k)),
                verdict_identite=bool(abs(resid) < mpf(10) ** (-(dps - 10))), verdict_ID=bool(abs(resid_ID) < mpf(10) ** (-(dps - 10))),
                verdict_Xi_neg=bool(Xi < 0), verdict_Xi_le_m3Delta=bool(Xi <= -3 * Delta), verdict_S_pos=bool(S >= 0))

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--kappas", type=str, required=True)
    ap.add_argument("--dps", type=int, default=30)
    ap.add_argument("--out", type=str, required=True)
    a = ap.parse_args()
    t0 = time.time()
    res = []
    for ks in a.kappas.split(","):
        r = un_kappa(Fraction(ks), a.dps)
        res.append(r)
        print(f"kappa={float(Fraction(ks)):8.4f} Xi={r['Xi']:+.10e} (Xi/P0={r['Xi_sur_P0']:+.6f}) S={r['S']:.6e} Delta={r['Delta']:.6e} |residu|={r['residu']:.1e} |residu_ID|={r['residu_ID']:.1e} "
              f"mass-1={r['masse_ecart']:.1e} m1_quad-m1={r['m1_ecart']:.1e}  ident={'OK' if r['verdict_identite'] else 'ECHEC'} ID={'OK' if r['verdict_ID'] else 'ECHEC'}", flush=True)
    ok = all(r['verdict_identite'] and r['verdict_ID'] and r['verdict_Xi_neg'] and r['verdict_Xi_le_m3Delta'] and r['verdict_S_pos'] for r in res)
    out = dict(script_sha256=hashlib.sha256(open(__file__, "rb").read()).hexdigest(), mpmath=mpmath.__version__, resultats=res, tout_ok=ok, secondes=round(time.time() - t0, 1))
    json.dump(out, open(a.out, "w"), indent=1)
    print(f"BILAN identite (mpmath, representation integrale) : {'TOUT_OK' if ok else 'ECHEC'} sur {len(res)} valeurs ; {out['secondes']} s")
    sys.exit(0 if ok else 1)

if __name__ == "__main__":
    main()
