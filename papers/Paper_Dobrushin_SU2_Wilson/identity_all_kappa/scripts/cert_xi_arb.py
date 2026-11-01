#!/usr/bin/env python3
"""cert_xi_arb.py -- certificat par intervalles (Arb, python-flint) de l'inegalite reduite  Xi(kappa) < 0  sur des boites de kappa.

Inegalite reduite (RAPPORT §3).  Pour kappa > 0,  E(t) = e^{kappa t}/Zb(kappa),  R = sqrt(1-t^2),
  A = solution reguliere de  t A - R^2 A'/3 = q := (t - m1) E   (m1 = I2/I1),  <g> = (2/pi) int g R E dt,
     Xi(kappa) = <R^2 u^2> + (3/5)<w^2> - <R^2>,  u = A/E,  w = t u - t + m1 = (t A - q)/E,  <R^2> = 3 m1/kappa.
  Xi < 0  ==>  F_CS(kappa, alpha) <= E_kappa[x2^2] pour tout alpha (borne par tranche), donc D_ch(kappa) = E_kappa[x2^2].
  (Le meme Xi vaut -3 Delta - S, S >= 0 : identite exacte, RAPPORT §2 ; ici on certifie Xi < 0 SANS utiliser cette identite.)

Methode (aucune serie en kappa : kappa est une BOULE Arb, A est entiere en t) :
  * m1 = I2/I1 et Zb = 2 I1/kappa sont croissantes en kappa : encadrees par leurs valeurs aux extremites de la boite.
  * q_n = [kappa^{n-1}/(n-1)! - m1 kappa^n/n!]/Zb  (n >= 1), q_0 = -m1/Zb.
  * A~ = polynome de degre N, obtenu par RECURSION DESCENDANTE exacte de  L[A~]_m = q_m (m = N+1..1),
    L[t^n] = (1+n/3) t^{n+1} - (n/3) t^{n-1} ; residu r = q - L[A~] = r0 + sum_{n>=N+2} q_n t^n  (exact), |r0| <= sum_{n>=N+2}|q_n|
    (condition de solvabilite  int r R dt = 0).
  * delta = A - A~ est la solution reguliere de L[delta] = r :  |delta| <= (3 pi/4) sup|r|   (h(t) = R^-3 int_t^1 R ds <= pi/4 sur [0,1)).
  * partie t >= 0 (theta in [0, pi/2]) : cellules uniformes en theta, evaluation de A~ en forme centree  p(tc) + p'(T)(T - tc),
    somme de Riemann SUPERIEURE a poids exacts  int sin^2, int sin^4.
  * partie t <= 0 : deux modes.
      'taylor'     : memes cellules (aucune hypothese) ;
      'analytique' : majorant explicite  u(t) <= 3 min{(1+m1)/(1-t), ((m1-t) kappa + 1)/(kappa^2 (1-t^2))}  (R(s) <= R(t) pour s <= t <= 0),
                     |w| <= m1 + |t|(1 + ubar), somme de Riemann superieure (la partie t<0 est exponentiellement petite).
      'auto'       : les deux modes sont calcules, on retient celui qui passe avec la meilleure marge ; si aucun ne passe : bissection de la boite.
Garde-fous (piege flint cap = 10) : ctx.prec ET ctx.cap fixes et relus ; aucune arb_series n'est utilisee, mais le cap est fixe (>= N+5) et relu ;
garde 1 : refus si cap < N+5 ; garde 2 : refus si N+2 <= kappa ; garde 3 : refus si prec < 64 ; le script gates_xi.py rejoue avec d'autres caps.
"""
import argparse, json, hashlib, sys, time, math
from fractions import Fraction
from multiprocessing import Pool
from flint import arb, arb_poly, ctx, fmpq
import flint

def fixe_contexte(prec, cap):
    ctx.prec = prec
    ctx.cap = cap
    assert ctx.prec == prec and ctx.cap == cap, "contexte non fixe"

def aq(fr):
    fr = Fraction(fr)
    return arb(fmpq(fr.numerator, fr.denominator))

def ball_interval(lo, hi):
    lo, hi = Fraction(lo), Fraction(hi)
    c = (lo + hi) / 2
    r = aq((hi - lo) / 2).upper()
    B = aq(c) + arb(0, r)
    assert B.lower() <= aq(lo).lower() and B.upper() >= aq(hi).upper()
    return B

def coefficients(Kb, N):
    """Renvoie (m1, Zb, q[0..N+1], a[0..N]) en boules."""
    klo = Kb.lower(); khi = Kb.upper()
    def m1_pt(k):
        return k.bessel_i(2) / k.bessel_i(1)
    def Zb_pt(k):
        return 2 * k.bessel_i(1) / k
    m1 = m1_pt(klo).union(m1_pt(khi))
    Zb = Zb_pt(klo).union(Zb_pt(khi))
    fact = [arb(1)]
    for n in range(1, N + 4):
        fact.append(fact[-1] * n)
    kp = [arb(1)]
    for n in range(1, N + 4):
        kp.append(kp[-1] * Kb)
    q = [(-m1) / Zb]
    for n in range(1, N + 2):
        q.append((kp[n - 1] / fact[n - 1] - m1 * kp[n] / fact[n]) / Zb)
    a = [arb(0)] * (N + 3)
    for mm in range(N + 1, 0, -1):
        # coefficient t^mm de L[A~] : ((mm+2)/3) a_{mm-1} - ((mm+1)/3) a_{mm+1} = q_mm
        a[mm - 1] = (3 * q[mm] + (mm + 1) * a[mm + 1]) / (mm + 2)
    return m1, Zb, q, a[:N + 1]

def tail_q(Kb, N):
    """majorant de sum_{n>=N+2} |q_n| : |q_n| <= kappa^{n-1}/(n-1)!  (n > kappa, Zb >= 1)."""
    kmax = abs(Kb).upper()
    assert kmax < N + 2, "GARDE 2 : N+2 <= kappa"
    t0 = kmax ** (N + 1)
    for j in range(1, N + 2):
        t0 = t0 / j
    return (t0 / (1 - kmax / (N + 2))).upper()

def F2(th):   # int_0^th sin^2
    return th / 2 - (2 * th).sin() / 4

def F4(th):   # int_0^th sin^4
    return 3 * th / 8 - (2 * th).sin() / 4 + (4 * th).sin() / 32

def cellules_taylor(P, dP, Kb, m1, Zb, eps, th_a, th_b, ncell):
    """Somme de Riemann superieure sur theta in [th_a, th_b] (cellules uniformes) : renvoie (S_A, S_W) avec
       S_A = sum sup(A^2/E) int sin^4,   S_W = sum sup((tA-q)^2/E) int sin^2."""
    S_A = arb(0); S_W = arb(0)
    for i in range(ncell):
        th0 = th_a + (th_b - th_a) * i / ncell
        th1 = th_a + (th_b - th_a) * (i + 1) / ncell
        c0 = th0.cos(); c1 = th1.cos()
        tlo = c1.lower(); thi = c0.upper()
        T = tlo.union(thi)
        tc = T.mid()
        Atil = P(tc) + dP(T) * (T - tc)
        Ab = Atil + arb(0, eps)
        Eb = (Kb * T).exp() / Zb
        qb = (T - m1) * Eb
        tAq = T * Ab - qb
        Elo = Eb.lower()
        assert Elo > 0
        A2 = (abs(Ab).upper()) ** 2
        W2 = (abs(tAq).upper()) ** 2
        w4 = F4(th1) - F4(th0)
        w2 = F2(th1) - F2(th0)
        S_A += (A2 / Elo) * w4.upper()
        S_W += (W2 / Elo) * w2.upper()
    return S_A.upper(), S_W.upper()

def majorant_negatif(Kb, m1, Zb, NTN):
    """Borne SUPERIEURE rigoureuse de  C_- = (2/pi) int_{-1}^0 R E [ R^2 u^2 + (3/5) w^2 ] dt  (partie t <= 0 de <R^2 u^2> + (3/5)<w^2>)."""
    pi = arb.pi()
    tot = arb(0)
    for i in range(NTN):
        th0 = pi / 2 + pi * i / (2 * NTN)
        th1 = pi / 2 + pi * (i + 1) / (2 * NTN)
        c0 = th0.cos(); c1 = th1.cos()          # c0 >= c1 (t decroissant en theta)
        tlo = c1.lower(); thi = c0.upper()
        T = tlo.union(thi)
        ub1 = (3 * (1 + m1) / (1 - T)).upper()
        d = (1 - T * T).lower()
        if d > 0:
            ub2 = (3 * ((m1 - T) * Kb + 1) / (Kb * Kb * (1 - T * T))).upper()
            ubar = ub1 if ub1 < ub2 else ub2
        else:
            ubar = ub1
        absT = abs(T).upper()
        wbar = (m1 + absT * (1 + ubar)).upper()
        Ehi = ((Kb * T).exp() / Zb).upper()
        w2 = F2(th1) - F2(th0)
        w4 = F4(th1) - F4(th0)
        tot += Ehi * (ubar * ubar * w4.upper() + arb(3) / 5 * wbar * wbar * w2.upper())
    return ((2 / pi) * tot).upper()

def cert_box(k0, k1, N, NT, mode, NTN=None, scale=1):
    """mode in {'taylor','analytique'}; scale > 1 : sabotage (multiplie la partie positive)."""
    if NTN is None:
        NTN = max(64, NT // 4)
    Kb = ball_interval(k0, k1)
    m1, Zb, q, a = coefficients(Kb, N)
    tq = tail_q(Kb, N)
    rbar = (2 * tq).upper()
    eps = (3 * arb.pi() / 4 * rbar).upper()
    P = arb_poly(a)
    dP = P.derivative()
    pi = arb.pi()
    if mode == 'taylor':
        SA, SW = cellules_taylor(P, dP, Kb, m1, Zb, eps, arb(0), pi, 2 * NT)
        Cneg = arb(0)
    elif mode == 'analytique':
        SA, SW = cellules_taylor(P, dP, Kb, m1, Zb, eps, arb(0), pi / 2, NT)
        Cneg = majorant_negatif(Kb, m1, Zb, NTN)
    else:
        raise ValueError(mode)
    P0 = 3 * m1 / Kb
    sc = aq(Fraction(scale))
    Xi_hi = sc * ((2 / pi) * (SA + arb(3) / 5 * SW) + Cneg) - P0
    ratio_hi = (Xi_hi / P0).upper()
    return dict(k0=str(k0), k1=str(k1), mode=mode, Xi_hi=Xi_hi, P0=P0, ratio_hi=ratio_hi, eps=eps, Cneg=Cneg,
                ok=bool(Xi_hi.upper() < 0))

def cert_box_auto(args):
    k0, k1, N, NT, neg, adapt, prec, cap, scale = args
    fixe_contexte(prec, cap)
    out = []
    def go(lo, hi, depth):
        modes = ['taylor', 'analytique'] if neg == 'auto' else [neg]
        meilleur = None
        for md in modes:
            r = cert_box(lo, hi, N, NT, md, scale=scale)
            # on garde le certificat qui passe avec la meilleure marge (plus petit rapport Xi_hi/P0) ; a defaut le moins mauvais
            if meilleur is None or float(r['ratio_hi'].upper()) < float(meilleur['ratio_hi'].upper()):
                meilleur = r
        if meilleur['ok']:
            out.append(meilleur); return
        if depth < adapt:
            mid = (lo + hi) / 2
            go(lo, mid, depth + 1); go(mid, hi, depth + 1)
            return
        out.append(meilleur)
    go(Fraction(k0), Fraction(k1), 0)
    return [dict(k0=r['k0'], k1=r['k1'], mode=r['mode'], ratio_hi=r['ratio_hi'].str(10, radius=False), ratio_hi_f=float(r['ratio_hi'].upper()),
                 Xi_hi=r['Xi_hi'].str(10, radius=False), P0=r['P0'].str(10, radius=False), eps=float(r['eps']), ok=r['ok']) for r in out]

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--prec", type=int, default=0, help="0 = automatique : 160 + 2.2 k1")
    ap.add_argument("--cap", type=int, default=0, help="0 = automatique : N + 60")
    ap.add_argument("--N", type=int, default=0, help="degre de A~ en t ; 0 = automatique : 3.2 k1 + 60")
    ap.add_argument("--NT", type=int, required=True, help="cellules uniformes en theta sur [0, pi/2]")
    ap.add_argument("--k0", type=str, required=True)
    ap.add_argument("--k1", type=str, required=True)
    ap.add_argument("--NK", type=int, required=True, help="nombre de boites uniformes sur [k0,k1]")
    ap.add_argument("--neg", type=str, default="auto", choices=["taylor", "analytique", "auto"])
    ap.add_argument("--adapt", type=int, default=0, help="bissections recursives max si une boite echoue")
    ap.add_argument("--procs", type=int, default=1)
    ap.add_argument("--scale", type=str, default="1", help="sabotage : multiplie la partie positive de Xi (gate negatif), rationnel")
    ap.add_argument("--out", type=str, required=True)
    a = ap.parse_args()
    t0 = time.time()
    K0, K1 = Fraction(a.k0), Fraction(a.k1)
    N = a.N or int(3.2 * float(K1)) + 60
    prec = a.prec or int(160 + 2.2 * float(K1))
    cap = a.cap or (N + 60)
    assert prec >= 64, "GARDE 3 : precision trop faible"
    assert cap >= N + 5, f"GARDE 1 : cap = {cap} < N+5 = {N + 5}"
    fixe_contexte(prec, cap)
    scale = Fraction(a.scale)
    jobs = []
    for i in range(a.NK):
        lo = K0 + (K1 - K0) * i / a.NK
        hi = K0 + (K1 - K0) * (i + 1) / a.NK
        jobs.append((lo, hi, N, a.NT, a.neg, a.adapt, prec, cap, scale))
    if a.procs > 1:
        with Pool(a.procs) as pool:
            chunks = pool.map(cert_box_auto, jobs, chunksize=1)
    else:
        chunks = [cert_box_auto(j) for j in jobs]
    res = [r for ch in chunks for r in ch]
    nb_tay = sum(1 for r in res if r['mode'] == 'taylor' and r['ok']); nb_ana = sum(1 for r in res if r['mode'] == 'analytique' and r['ok'])
    toutes = all(r["ok"] for r in res)
    pire = max(res, key=lambda r: r["ratio_hi_f"])
    couverture = all(Fraction(res[i]["k1"]) == Fraction(res[i + 1]["k0"]) for i in range(len(res) - 1)) and Fraction(res[0]["k0"]) == K0 and Fraction(res[-1]["k1"]) == K1
    for r in res[:: max(1, len(res) // 40)]:
        print(f"kappa [{float(Fraction(r['k0'])):.6f},{float(Fraction(r['k1'])):.6f}] mode={r['mode']:10s} Xi_hi/P0 <= {r['ratio_hi_f']:+.5f}  eps={r['eps']:.1e}  {'OK' if r['ok'] else 'ECHEC'}", flush=True)
    out = dict(script_sha256=hashlib.sha256(open(__file__, "rb").read()).hexdigest(), python_flint=flint.__version__, prec=ctx.prec, cap=ctx.cap, N=N, NT=a.NT,
               k0=a.k0, k1=a.k1, NK=a.NK, neg=a.neg, adapt=a.adapt, scale=str(scale), n_boites=len(res), couverture_continue=couverture,
               n_ok_taylor=nb_tay, n_ok_analytique=nb_ana,
               boites=res, toutes_ok=toutes, pire_ratio=pire["ratio_hi"], secondes=round(time.time() - t0, 1))
    json.dump(out, open(a.out, "w"), indent=1)
    print(f"BILAN {'TOUTES_OK' if toutes else 'ECHEC'} {sum(r['ok'] for r in res)}/{len(res)} boites (taylor {nb_tay}, analytique {nb_ana}) ; "
          f"pire Xi_hi/P0 = {pire['ratio_hi']} ; couverture continue [{a.k0},{a.k1}] = {couverture} ; {out['secondes']} s")
    sys.exit(0 if toutes else 1)

if __name__ == "__main__":
    main()
