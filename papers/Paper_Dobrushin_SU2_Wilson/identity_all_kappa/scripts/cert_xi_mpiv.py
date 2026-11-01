#!/usr/bin/env python3
"""cert_xi_mpiv.py -- implementation INDEPENDANTE (mpmath.iv + fractions) du certificat  Xi(kappa) < 0  sur des boites de kappa.

Ecrite sans lire ni importer cert_xi_arb.py (memes MATHEMATIQUES -- cf. RAPPORT §3 --, code et outils differents) :
  * arithmetique par intervalles : mpmath.iv (bornes flottantes, arrondi dirige) et non Arb/python-flint ; AUCUN import de flint ;
  * Zb(kappa) = sum_j kappa^{2j}/(4^j j!(j+1)!) et Zb'(kappa) calcules par leur SERIE (coefficients fractions exacts) + reste geometrique
    elementaire, aux extremites de la boite (Zb et m1 = Zb'/Zb sont croissantes) : aucune fonction de Bessel ;
  * recursion descendante des coefficients de A~ en arithmetique d'intervalles avec kappa = intervalle ;
  * evaluation de A~ par Horner NAIF sur l'intervalle T de chaque cellule (pas de forme centree) ;
  * partition uniforme en theta avec NT different de celui de l'implementation Arb, poids exacts int sin^2, int sin^4 ;
  * bornes de queue : sum_{n>=N+2}|q_n| <= sum_{j>=N+1} kappa^j/j! <= kappa^{N+1}/(N+1)! * (N+2)/(N+2-kappa) (ecrite independamment).
Verdict calcule : ok <=> borne superieure de Xi < 0.
"""
import argparse, json, hashlib, sys, time, os
from fractions import Fraction as Fr
from math import factorial
from multiprocessing import Pool
from mpmath import iv, mpf
import mpmath

def ivF(x):
    x = Fr(x)
    return iv.mpf(x.numerator) / iv.mpf(x.denominator)

def check_prec(P):
    assert iv.prec == P, f"GARDE PREC : iv.prec = {iv.prec} != {P}"
    w = (iv.mpf(1) / 3).delta
    assert w <= mpf(2) ** (-(P - 3)), f"GARDE PREC : largeur de 1/3 = {w} incompatible avec prec {P}"

def zbar_pt(kfr, J, P):
    """(Zb, Zb') en kappa = kfr (Fraction), serie tronquee a J termes + reste geometrique."""
    k = ivF(kfr)
    k2 = k * k
    s0 = iv.mpf(0); s1 = iv.mpf(0)
    pw = iv.mpf(1)              # k^{2j}
    for j in range(J + 1):
        cj = ivF(Fr(1, 4 ** j * factorial(j) * factorial(j + 1)))
        t0 = cj * pw
        s0 += t0
        if j >= 1:
            s1 += 2 * j * cj * pw / k
        pw = pw * k2
    # reste : terme suivant t_{J+1}, rapport <= k^2/(4 (J+2)(J+3)) <= 1/2
    rj = k2 / (4 * (J + 2) * (J + 3))
    assert rj.b < mpf(1) / 2, "J trop petit"
    cj1 = ivF(Fr(1, 4 ** (J + 1) * factorial(J + 1) * factorial(J + 2)))
    t_next = cj1 * pw
    rest0 = 2 * t_next
    rest1 = 2 * 2 * (J + 1) * cj1 * pw / k      # majorant du reste de Zb' (meme rapport, facteur 2j <= 2(J+1)(...))
    # reste de Zb' : sum_{j>J} 2j c_j k^{2j-1} <= 2 (J+1) (k^{2J+1} c_{J+1}) * 2  (rapport <= 1/2 et 2j/(2J+2) <= (j/(J+1)) <= 2^{j-J-1} pour j >= J+1)
    z0 = iv.mpf([s0.a - 0, s0.b]) + iv.mpf([0, rest0.b])
    z1 = iv.mpf([s1.a, s1.b]) + iv.mpf([0, 2 * rest1.b])
    return z0, z1

def build(kfr_lo, kfr_hi, N, P):
    """m1, Zb (intervalles, croissants), q[0..N+1], a[0..N] (coefficients de A~)."""
    kmax = float(kfr_hi)
    J = int(2 * kmax) + 60
    z0l, z1l = zbar_pt(kfr_lo, J, P)
    z0h, z1h = zbar_pt(kfr_hi, J, P)
    m_lo = (z1l / z0l).a; m_hi = (z1h / z0h).b
    Zl = z0l.a; Zh = z0h.b
    m1 = iv.mpf([m_lo, m_hi]); Zb = iv.mpf([Zl, Zh])
    K = iv.mpf([ivF(kfr_lo).a, ivF(kfr_hi).b])
    # q_n
    q = [(-m1) / Zb]
    kp = iv.mpf(1)
    kpm1 = iv.mpf(1)
    fact = [iv.mpf(1)]
    for n in range(1, N + 4):
        fact.append(fact[-1] * n)
    pows = [iv.mpf(1)]
    for n in range(1, N + 4):
        pows.append(pows[-1] * K)
    for n in range(1, N + 2):
        q.append((pows[n - 1] / fact[n - 1] - m1 * pows[n] / fact[n]) / Zb)
    a = [iv.mpf(0)] * (N + 3)
    for mm in range(N + 1, 0, -1):
        a[mm - 1] = (3 * q[mm] + (mm + 1) * a[mm + 1]) / (mm + 2)
    return K, m1, Zb, a[:N + 1]

def horner(c, T):
    r = iv.mpf(0)
    for x in reversed(c):
        r = r * T + x
    return r

def F2(th):
    return th / 2 - iv.sin(2 * th) / 4

def F4(th):
    return 3 * th / 8 - iv.sin(2 * th) / 4 + iv.sin(4 * th) / 32

def absmax(x):
    return max(abs(x.a), abs(x.b))

def cert_box(args):
    kfr_lo, kfr_hi, N, NT, mode, P, scale = args
    iv.prec = P
    check_prec(P)
    kfr_lo, kfr_hi = Fr(kfr_lo), Fr(kfr_hi)
    K, m1, Zb, a = build(kfr_lo, kfr_hi, N, P)
    kmax = iv.mpf(K.b)                       # intervalle degenere (borne superieure de la boite)
    assert kmax.b < N + 2, "GARDE : N+2 <= kappa"
    # queue : kappa^{N+1}/(N+1)! * (N+2)/(N+2-kappa)   (tout en arithmetique d'intervalles)
    t0 = kmax ** (N + 1)
    for j in range(1, N + 2):
        t0 = t0 / j
    tail = t0 * (N + 2) / (N + 2 - kmax)
    eps = (3 * iv.pi / 4 * 2 * tail).b
    pi = iv.pi
    NTN = max(64, NT // 4)

    def cellules_taylor(th_a, th_b, ncell):
        SA = iv.mpf(0); SW = iv.mpf(0)
        for i in range(ncell):
            th0 = th_a + (th_b - th_a) * i / ncell
            th1 = th_a + (th_b - th_a) * (i + 1) / ncell
            c0 = iv.cos(th0); c1 = iv.cos(th1)
            T = iv.mpf([c1.a, c0.b])
            A = horner(a, T) + iv.mpf([-eps, eps])
            Eb = iv.exp(K * T) / Zb
            qb = (T - m1) * Eb
            tAq = T * A - qb
            Elo = Eb.a
            assert Elo > 0
            SA += iv.mpf(absmax(A)) ** 2 / Elo * iv.mpf((F4(th1) - F4(th0)).b)
            SW += iv.mpf(absmax(tAq)) ** 2 / Elo * iv.mpf((F2(th1) - F2(th0)).b)
        return SA, SW

    def neg_analytique():
        tot = iv.mpf(0)
        for i in range(NTN):
            th0 = pi / 2 + pi * i / (2 * NTN)
            th1 = pi / 2 + pi * (i + 1) / (2 * NTN)
            c0 = iv.cos(th0); c1 = iv.cos(th1)
            T = iv.mpf([c1.a, c0.b])
            ub1 = (3 * (1 + m1) / (1 - T)).b
            den = (1 - T * T).a
            if den > 0:
                ub2 = (3 * ((m1 - T) * K + 1) / (K * K * (1 - T * T))).b
                ubar = min(ub1, ub2)
            else:
                ubar = ub1
            wbar = (m1 + iv.mpf(absmax(T)) * (1 + iv.mpf(ubar))).b
            Ehi = (iv.exp(K * T) / Zb).b
            w2 = (F2(th1) - F2(th0)).b; w4 = (F4(th1) - F4(th0)).b
            tot += iv.mpf(Ehi) * (iv.mpf(ubar) ** 2 * iv.mpf(w4) + iv.mpf(3) / 5 * iv.mpf(wbar) ** 2 * iv.mpf(w2))
        return (2 / pi) * tot

    P0 = 3 * m1 / K
    res = None
    modes = ['taylor', 'analytique'] if mode == 'auto' else [mode]
    for md in modes:
        if md == 'taylor':
            SA, SW = cellules_taylor(iv.mpf(0), pi, 2 * NT)
            Cneg = iv.mpf(0)
        else:
            SA, SW = cellules_taylor(iv.mpf(0), pi / 2, NT)
            Cneg = neg_analytique()
        Xi = ivF(scale) * ((2 / pi) * (SA + iv.mpf(3) / 5 * SW) + Cneg) - P0
        ratio_hi = (Xi / P0).b
        ok = bool(Xi.b < 0)
        cand = dict(k0=str(kfr_lo), k1=str(kfr_hi), mode=md, ratio_hi_f=float(ratio_hi), eps=float(eps), ok=ok)
        # on retient le certificat de meilleure marge (plus petit rapport Xi_hi/P0), qu'il passe ou non
        if res is None or cand['ratio_hi_f'] < res['ratio_hi_f']:
            res = cand
    check_prec(P)
    return res

def init_worker(p):
    iv.prec = p
    check_prec(p)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--prec", type=int, default=0)
    ap.add_argument("--N", type=int, default=0)
    ap.add_argument("--NT", type=int, required=True, help="cellules uniformes en theta sur [0, pi/2]")
    ap.add_argument("--k0", type=str, required=True)
    ap.add_argument("--k1", type=str, required=True)
    ap.add_argument("--NK", type=int, required=True)
    ap.add_argument("--mode", type=str, default="auto", choices=["taylor", "analytique", "auto"])
    ap.add_argument("--procs", type=int, default=1)
    ap.add_argument("--scale", type=str, default="1")
    ap.add_argument("--out", type=str, required=True)
    a = ap.parse_args()
    t0 = time.time()
    K0, K1 = Fr(a.k0), Fr(a.k1)
    N = a.N or int(3.2 * float(K1)) + 60
    P = a.prec or int(160 + 2.2 * float(K1))
    jobs = []
    for i in range(a.NK):
        lo = K0 + (K1 - K0) * i / a.NK; hi = K0 + (K1 - K0) * (i + 1) / a.NK
        jobs.append((str(lo), str(hi), N, a.NT, a.mode, P, a.scale))
    with Pool(a.procs, initializer=init_worker, initargs=(P,)) as pool:
        res = pool.map(cert_box, jobs, chunksize=1)
    toutes = all(r["ok"] for r in res)
    pire = max(res, key=lambda r: r["ratio_hi_f"])
    couverture = all(Fr(res[i]["k1"]) == Fr(res[i + 1]["k0"]) for i in range(len(res) - 1)) and Fr(res[0]["k0"]) == K0 and Fr(res[-1]["k1"]) == K1
    for r in res[:: max(1, len(res) // 30)]:
        print(f"kappa [{float(Fr(r['k0'])):.6f},{float(Fr(r['k1'])):.6f}] mode={r['mode']:10s} Xi_hi/P0 <= {r['ratio_hi_f']:+.5f}  {'OK' if r['ok'] else 'ECHEC'}", flush=True)
    out = dict(script_sha256=hashlib.sha256(open(__file__, "rb").read()).hexdigest(), mpmath=mpmath.__version__, prec=P, N=N, NT=a.NT, k0=a.k0, k1=a.k1, NK=a.NK,
               mode=a.mode, scale=a.scale, n_boites=len(res), couverture_continue=couverture, n_ok_taylor=sum(1 for r in res if r['ok'] and r['mode'] == 'taylor'),
               n_ok_analytique=sum(1 for r in res if r['ok'] and r['mode'] == 'analytique'), boites=res, toutes_ok=toutes, pire_ratio=pire["ratio_hi_f"],
               secondes=round(time.time() - t0, 1))
    json.dump(out, open(a.out, "w"), indent=1)
    print(f"BILAN {'TOUTES_OK' if toutes else 'ECHEC'} {sum(r['ok'] for r in res)}/{len(res)} boites ; pire Xi_hi/P0 = {pire['ratio_hi_f']:+.6f} ; "
          f"couverture continue [{a.k0},{a.k1}] = {couverture} ; {out['secondes']} s")
    sys.exit(0 if toutes else 1)

if __name__ == "__main__":
    main()
