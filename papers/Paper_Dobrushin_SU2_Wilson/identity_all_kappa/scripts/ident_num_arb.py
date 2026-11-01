#!/usr/bin/env python3
"""ident_num_arb.py -- verification NUMERIQUE (ball-tracked, non rigoureuse en quadrature) de l'identite exacte du RAPPORT §2 :

    Xi(kappa) := <R^2 u^2> + (3/5) <w^2> - <R^2>   (definition)
    S(kappa)  := (1/15) < R^4 (4 u'^2 + 2 kappa u u' + kappa^2 u^2) >  >= 0
    Delta     := m1^2 + 4 m1/kappa - 1  (= E x2^2 - Var x1)
    IDENTITE : Xi + 3 Delta + S = 0,          donc  Xi <= -3 Delta < 0.

<g> = (2/pi) int_{-1}^1 g R E dt (loi marginale de x1 sous q_kappa), u = A/E, w = t u - t + m1, A = solution reguliere de t A - R^2 A'/3 = (t-m1) E.
A est calculee par la recursion descendante en t (Taylor, degre N) en precision Arb elevee ; quadrature de Gauss-Legendre en theta
(noeuds/poids en precision Arb), deux regles (M et 3M/2 noeuds) : leur ecart estime l'erreur de quadrature.
Verdicts CALCULES : residu de l'identite, Xi < 0, Xi <= -3 Delta, S >= 0.  Etiquette : [numerique].
"""
import argparse, json, hashlib, sys, time, math
from fractions import Fraction
from flint import arb, arb_poly, ctx, fmpq
import flint

def aq(fr):
    fr = Fraction(fr)
    return arb(fmpq(fr.numerator, fr.denominator))

def tableau(kfr, N, prec):
    ctx.prec = prec
    k = aq(kfr)
    I1 = k.bessel_i(1); I2 = k.bessel_i(2)
    Zb = 2 * I1 / k
    m1 = I2 / I1
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
    return k, Zb, m1, arb_poly(a[:N + 1])

def gl_rule(M):
    xs = []; ws = []
    for j in range(M):
        x, w = arb.legendre_p_root(M, j, weight=True)
        xs.append(x); ws.append(w)
    return xs, ws

def moments(k, Zb, m1, P, rule):
    xs, ws = rule
    pi = arb.pi()
    dP = P.derivative()
    acc = dict(P0=arb(0), t=arb(0), t2=arb(0), R2u2=arb(0), w2=arb(0), S=arb(0), one=arb(0))
    for x, w in zip(xs, ws):
        th = pi / 2 * (x + 1)
        wt = pi / 2 * w
        t = th.cos(); s = th.sin()
        A = P(t); Ap = dP(t)
        E = (k * t).exp() / Zb
        u = A / E
        up = (Ap - k * A) / E
        ww = t * u - t + m1
        # <g> = (2/pi) int g R E dt = (2/pi) int g sin^2(th) E dth
        meas = wt * 2 / pi * s * s * E
        R2 = s * s
        acc['one'] += meas
        acc['t'] += meas * t
        acc['t2'] += meas * t * t
        acc['P0'] += meas * R2
        acc['R2u2'] += meas * R2 * u * u
        acc['w2'] += meas * ww * ww
        acc['S'] += meas * R2 * R2 * (4 * up * up + 2 * k * u * up + k * k * u * u) / 15
    return acc

def un_kappa(kfr, prec_bonus=0):
    kappa = float(kfr)
    N = int(3.3 * kappa) + 100
    prec = int(300 + 3.2 * kappa) + prec_bonus
    M1 = max(120, int(3 * kappa) + 80)
    M2 = int(1.5 * M1)
    k, Zb, m1, P = tableau(kfr, N, prec)
    res = []
    for M in (M1, M2):
        ctx.prec = prec
        acc = moments(k, Zb, m1, P, gl_rule(M))
        P0e = 3 * m1 / k
        Xi = acc['R2u2'] + arb(3) / 5 * acc['w2'] - P0e
        Delta = m1 * m1 + 4 * m1 / k - 1
        resid = Xi + 3 * Delta + acc['S']
        res.append(dict(M=M, Xi=Xi, S=acc['S'], Delta=Delta, resid=resid, one=acc['one'], P0_quad=acc['P0'], P0_exact=P0e,
                        t_quad=acc['t'], m1=m1, Var_quad=acc['t2'] - acc['t'] ** 2))
    r1, r2 = res
    ctx.prec = 64
    out = dict(kappa=str(kfr), N=N, prec=prec, M1=M1, M2=M2,
               Xi=float(r2['Xi'].mid()), S=float(r2['S'].mid()), Delta=float(r2['Delta'].mid()),
               residu_M1=float(abs(r1['resid'].mid())), residu_M2=float(abs(r2['resid'].mid())),
               ecart_Xi_M1_M2=float(abs((r1['Xi'] - r2['Xi']).mid())),
               masse_ecart=float(abs((r2['one'] - 1).mid())),
               P0_ecart=float(abs((r2['P0_quad'] - r2['P0_exact']).mid())),
               m1_ecart=float(abs((r2['t_quad'] - r2['m1']).mid())),
               rad_Xi=float(r2['Xi'].rad()))
    out['Xi_sur_P0'] = out['Xi'] / float((3 * r2['m1'] / aq(kfr)).mid())
    out['verdict_identite'] = bool(out['residu_M2'] < 1e-20 * max(1.0, abs(out['Xi'])) and out['ecart_Xi_M1_M2'] < 1e-20)
    out['verdict_Xi_neg'] = bool(out['Xi'] < 0)
    out['verdict_Xi_le_m3Delta'] = bool(out['Xi'] <= -3 * out['Delta'])
    out['verdict_S_pos'] = bool(out['S'] >= 0)
    return out

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--kappas", type=str, required=True, help="liste de rationnels separes par des virgules")
    ap.add_argument("--out", type=str, required=True)
    a = ap.parse_args()
    t0 = time.time()
    res = []
    for ks in a.kappas.split(","):
        r = un_kappa(Fraction(ks))
        res.append(r)
        print(f"kappa={float(Fraction(ks)):9.4f} Xi={r['Xi']:+.10e} (Xi/P0={r['Xi_sur_P0']:+.6f})  S={r['S']:.6e}  Delta={r['Delta']:.6e}  "
              f"|residu|={r['residu_M2']:.1e}  ecart M1/M2={r['ecart_Xi_M1_M2']:.1e}  masse-1={r['masse_ecart']:.1e}  "
              f"ident={'OK' if r['verdict_identite'] else 'ECHEC'} Xi<0={'OK' if r['verdict_Xi_neg'] else 'ECHEC'} Xi<=-3D={'OK' if r['verdict_Xi_le_m3Delta'] else 'ECHEC'}", flush=True)
    ok = all(r['verdict_identite'] and r['verdict_Xi_neg'] and r['verdict_Xi_le_m3Delta'] and r['verdict_S_pos'] for r in res)
    out = dict(script_sha256=hashlib.sha256(open(__file__, "rb").read()).hexdigest(), python_flint=flint.__version__, resultats=res, tout_ok=ok,
               secondes=round(time.time() - t0, 1))
    json.dump(out, open(a.out, "w"), indent=1)
    print(f"BILAN identite numerique : {'TOUT_OK' if ok else 'ECHEC'} sur {len(res)} valeurs de kappa ; {out['secondes']} s")
    sys.exit(0 if ok else 1)

if __name__ == "__main__":
    main()
