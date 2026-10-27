#!/usr/bin/env python3
# cert_ch.py -- TACHE CH (28/09/2026) : certificat Arb, metrique CORDALE, D_ch(kappa) = E_kappa[x2^2] <= 1/4.
#
# Inegalite certifiee (RAPPORT_CH.md par. 3), pour tout kappa dans [0, K] :
#     Nt(kappa) / Z(kappa)^2  >  max( J0t(kappa), J1t(kappa) )
#   * Z(kappa) = E_Haar[e^{kappa x1}] = sum_k kappa^{2k} / (4^k k! (k+1)!)
#   * Nt/Z^2 = (E x2^2 - Var x1)/kappa^2,  N = Z^2/3 - (4/3) Z'' Z + Z'^2 = kappa^2 Nt
#   * J0t, J1t = majorants (divises par kappa^2) de l'exces de Beckmann du champ explicite
#       V = cos(a) [A(y1) e1 - A'(y1) z/3] + sin(a) [e^{kappa y1}/Z] e2   (div V = 0, V.n = (u - ubar) e^{kappa x1}/Z)
#     J0 = (2/(5 pi)) int (A'/3)^2 R^5 / (2m) dy1,  J1 = (2/(3 pi)) int (E-A)^2 R^3 / (2m) dy1 + (2/3) J0,
#     m(y1) = min(A, E) - |A'| R / 6  (minorant de <v, V>),  R = sqrt(1 - y1^2).
#   A = sum_j kappa^j A_j(t) : A_j polynome de degre j, L[A_j] = q_j, L[p] = t p - (1 - t^2) p'/3.
#
# Garde-fous (lecon du 27/09, ctx.cap = 10 par defaut) : ctx.cap ET ctx.prec fixes explicitement et relus ;
# cap >= L sinon refus ; CHAQUE arb_series construite et chaque produit/quotient doit avoir .prec == L.
# Les series tronquees a l'ordre D sont completees par des restes de Cauchy (tous les ordres > D).
import argparse, json, hashlib, sys, time, math
from fractions import Fraction
from flint import arb, arb_poly, arb_series, ctx, fmpq

NCHK = 0


def fixe_contexte(prec, cap):
    ctx.prec = prec
    ctx.cap = cap
    assert ctx.prec == prec and ctx.cap == cap, "contexte non fixe"


def chk(s, L, nom):
    """GARDE 2 : toute serie doit avoir exactement la longueur L."""
    global NCHK
    NCHK += 1
    assert s.prec == L, f"GARDE 2 : serie {nom} de longueur {s.prec} != L = {L} (ctx.cap = {ctx.cap})"
    return s


def coeffs_pad(s, L):
    c = list(s.coeffs())
    assert len(c) <= L
    return c + [arb(0)] * (L - len(c))


def aq(fr):
    return arb(fmpq(fr.numerator, fr.denominator))


def zcoef_frac(n):
    """coefficient de kappa^n dans Z : n = 2k -> 1/(4^k k! (k+1)!), 0 sinon (exact)."""
    if n % 2:
        return Fraction(0)
    k = n // 2
    return Fraction(1, 4 ** k * math.factorial(k) * math.factorial(k + 1))


# ---------------------------------------------------------------- series scalaires (Arb, longueur L)
def series_scalaires(D, L):
    zs = [aq(zcoef_frac(n)) for n in range(L + 2)]
    Z = chk(arb_series(zs[:L], prec=L), L, "Z")
    Zp = chk(arb_series([(n + 1) * zs[n + 1] for n in range(L)], prec=L), L, "Z'")
    Zpp = chk(arb_series([(n + 1) * (n + 2) * zs[n + 2] for n in range(L)], prec=L), L, "Z''")
    iz = chk(1 / Z, L, "1/Z")
    m1 = chk(Zp * iz, L, "m1")
    mu = chk(m1 * iz, L, "mu = m1/Z")
    Z2 = chk(Z * Z, L, "Z^2")
    ZppZ = chk(Zpp * Z, L, "Z''Z")
    Zp2 = chk(Zp * Zp, L, "Z'^2")
    N = chk(Z2 / 3 - ZppZ * arb(4) / 3 + Zp2, L, "N")
    return dict(Z=coeffs_pad(Z, L), iz=coeffs_pad(iz, L), mu=coeffs_pad(mu, L), N=coeffs_pad(N, L), m1=coeffs_pad(m1, L))


# ---------------------------------------------------------------- polynomes en t (Arb)
def solveL(q):
    """q = [q_0..q_{d+1}] ; renvoie a = [a_0..a_d] avec L[sum a_n t^n] = q (descente), et le residu de l'equation t^0."""
    dd = len(q) - 2
    a = [arb(0)] * (dd + 3)
    for mm in range(dd + 1, 0, -1):
        # coeff t^mm : a_{mm-1} (1 + (mm-1)/3) - a_{mm+1} (mm+1)/3 = q_mm
        a[mm - 1] = (q[mm] + a[mm + 1] * (mm + 1) / 3) * 3 / (mm + 2)
    resid = -a[1] / 3 - q[0]
    return a[:dd + 1], resid


def polys_t(sc, D):
    iz, mu = sc["iz"], sc["mu"]
    fact = [arb(math.factorial(n)) for n in range(D + 3)]
    A, E, Ap, resids = [], [], [], []
    for j in range(D + 1):
        q = [arb(0)] * (j + 2)
        e = [arb(0)] * (j + 1)
        for n in range(j + 1):
            k = j - n
            q[n + 1] += iz[k] / fact[n]
            q[n] -= mu[k] / fact[n]
            e[n] += iz[k] / fact[n]
        a, r = solveL(q)
        resids.append(r)
        A.append(arb_poly(a))
        E.append(arb_poly(e))
        Ap.append(arb_poly(a).derivative())
    return A, E, Ap, resids


# ---------------------------------------------------------------- majorants (restes de Cauchy)
def majZ(r, d, KK=120):
    """sum_{n>=d} n!/(n-d)! z_n r^(n-d), z_n >= 0 (serie majorante de Z^{(d)} sur |kappa| <= r)."""
    r = arb(r)
    s = arb(0)
    for k in range(KK + 1):
        n = 2 * k
        if n < d:
            continue
        s += aq(zcoef_frac(n)) * (math.factorial(n) // math.factorial(n - d)) * r ** (n - d)
    # reste k > KK : rapport des termes consecutifs decroissant en k, majore par ratio(KK) <= 1/2
    k = KK
    ratio = r * r * (2 * k + 2) * (2 * k + 1) / ((2 * k + 2 - d) * (2 * k + 1 - d) * 4 * (k + 1) * (k + 2))
    assert ratio.upper() < arb(1) / 2
    n = 2 * (KK + 1)
    nxt = aq(zcoef_frac(n)) * (math.factorial(n) // math.factorial(n - d)) * r ** (n - d)
    return s + arb(0, 1) * 2 * nxt.upper()


def constantes(rho, rhoN):
    rho = arb(rho)
    Zr = majZ(rho, 0)
    Zmin = 2 - Zr  # |Z(kappa)| >= 1 - (Z(rho) - 1) sur |kappa| <= rho
    assert Zmin.lower() > 0, "Z peut s'annuler dans le disque"
    m1max = majZ(rho, 1) / Zmin
    ME = rho.exp() / Zmin
    MA = 3 * (arb.pi() / 2) * (1 + m1max) * rho.exp() / Zmin
    ZN = majZ(rhoN, 0)
    Nmaj = ZN * ZN / 3 + majZ(rhoN, 2) * ZN * 4 / 3 + majZ(rhoN, 1) ** 2
    return dict(Zmin=Zmin.lower(), m1max=m1max.upper(), ME=ME.upper(), MA=MA.upper(), Nmaj=Nmaj.upper())


def geo_j2(J, x, shift):
    """majorant de sum_{j >= J} j^2 x^(j - shift), 0 <= x < 1."""
    r = arb(J + 1) ** 2 / arb(J) ** 2 * x
    assert r.upper() < 1
    return (arb(J) ** 2 * x ** (J - shift) / (1 - r)).upper()


def restes(cst, D, k1, rho, rhoN):
    x = arb(k1) / rho
    assert x.upper() < 1
    MA, ME = cst["MA"], cst["ME"]
    t = {}
    t["Dt"] = ((ME + MA) / rho * x ** D / (1 - x)).upper()          # sum_{j>=D+1} k^{j-1} |E_j - A_j|
    t["At"] = (MA / rho * geo_j2(D + 1, x, 1)).upper()             # sum_{j>=D+1} k^{j-1} |A_j'|  (Markov)
    t["A"] = (MA * x ** (D + 1) / (1 - x)).upper()
    t["E"] = (ME * x ** (D + 1) / (1 - x)).upper()
    t["Ap"] = (MA * geo_j2(D + 1, x, 0)).upper()
    xN = arb(k1) / rhoN
    t["N"] = (cst["Nmaj"] / arb(rhoN) ** 2 * xN ** (D + 1) / (1 - xN)).upper()  # sum_{n>D} |N_{n+2}| k^n
    return t


# ---------------------------------------------------------------- evaluation
def ball_interval(lo, hi):
    """boule Arb contenant [lo, hi] (lo, hi rationnels)."""
    c = (lo + hi) / 2
    r = aq((hi - lo) / 2).upper()
    B = aq(c) + arb(0, r)
    assert B.lower() <= aq(lo).lower() and B.upper() >= aq(hi).upper()
    return B


def collapse(polys, Kb, shift):
    """sum_j Kb^(j - shift) polys[j] pour j >= shift."""
    acc = arb_poly([0])
    Kp = arb(1)
    for j in range(shift, len(polys)):
        acc += polys[j] * Kp
        Kp = Kp * Kb
    return acc


def ev_centre(p, dp, tc, T):
    """p(T) inclus dans p(tc) + p'(T) [T - tc] (forme centree)."""
    return p(tc) + dp(T) * (T - tc)


def pm(tail):
    return arb(0, tail)


def boite(k0, k1, P, sc, cst, D, NT, rho, rhoN):
    Kb = ball_interval(k0, k1)
    A, E, Ap = P
    kmax = abs(Kb).upper()          # |kappa| <= kmax sur toute la boule
    t = restes(cst, D, kmax, rho, rhoN)
    # polynomes en t pour la boite (kappa = boule)
    PDt = collapse([E[j] - A[j] for j in range(D + 1)], Kb, 1)   # (E - A)/kappa
    PAt = collapse(Ap, Kb, 1)                                    # A'/kappa
    PA = collapse(A, Kb, 0)
    PE = collapse(E, Kb, 0)
    PAp = collapse(Ap, Kb, 0)
    dPDt, dPAt, dPA, dPE, dPAp = [p.derivative() for p in (PDt, PAt, PA, PE, PAp)]
    two5pi = 2 / (5 * arb.pi())
    two3pi = 2 / (3 * arb.pi())
    J0 = arb(0)
    J1v = arb(0)
    mmin = None
    for i in range(NT):
        a = Fraction(-1) + Fraction(2 * i, NT)
        b = Fraction(-1) + Fraction(2 * (i + 1), NT)
        T = ball_interval(a, b)
        tc = arb(fmpq((a + b).numerator, (a + b).denominator)) / 2
        w = aq(b - a)
        Dt = ev_centre(PDt, dPDt, tc, T) + pm(t["Dt"])
        At = ev_centre(PAt, dPAt, tc, T) + pm(t["At"])
        Av = ev_centre(PA, dPA, tc, T) + pm(t["A"])
        Ev = ev_centre(PE, dPE, tc, T) + pm(t["E"])
        Apv = ev_centre(PAp, dPAp, tc, T) + pm(t["Ap"])
        # R^2 = 1 - t^2 sur [a, b] : majorant exact
        t2min = Fraction(0) if a <= 0 <= b else min(a * a, b * b)
        R2hi = aq(1 - t2min)
        Rhi = R2hi.sqrt().upper()
        R3hi = (R2hi * R2hi.sqrt()).upper()
        R5hi = (R2hi * R2hi * R2hi.sqrt()).upper()
        minAE = Av.lower() if Av.lower() < Ev.lower() else Ev.lower()
        mlo = (minAE - abs(Apv).upper() * Rhi / 6).lower()
        assert mlo > 0, f"m <= 0 : boite kappa [{k0},{k1}], t [{a},{b}], m >= {mlo}"
        mmin = mlo if mmin is None or mlo < mmin else mmin
        At2 = (abs(At).upper()) ** 2
        Dt2 = (abs(Dt).upper()) ** 2
        J0 += w * (two5pi * At2 / 9 * R5hi / (2 * mlo)).upper()
        J1v += w * (two3pi * Dt2 * R3hi / (2 * mlo)).upper()
    J0 = J0.upper()
    J1 = (J1v + J0 * 2 / 3).upper()
    # minorant de Nt/Z^2 : Nt(K) (Horner, boule) - reste ; Z(k1) majore (coefficients >= 0)
    Nt = arb_poly(sc["N"][2:D + 3])
    NtK = (Nt(Kb) - pm(t["N"])).lower()
    Zhi = majZ(kmax, 0).upper()
    LB = (NtK / (Zhi * Zhi)).lower()
    Jmax = J0 if J0 > J1 else J1
    marge = (LB - Jmax).lower()
    return dict(k0=str(k0), k1=str(k1), LB=LB, J0=J0, J1=J1, m=mmin, marge=marge, ok=bool(marge > 0),
                restes={k: float(v) for k, v in t.items()})


def arbstr(x):
    return x.str(20, radius=True)


def exact_str(x):
    """valeur EXACTE (dyadique) d'une boule de rayon nul (extremite .lower()/.upper()), en 'p/q'."""
    assert x.rad() == 0, "exact_str : boule de rayon non nul"
    m, e = x.mid().man_exp()
    fr = Fraction(int(m)) * (Fraction(2) ** int(e))
    return f"{fr.numerator}/{fr.denominator}"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--D", type=int, required=True, help="ordre de troncature en kappa")
    ap.add_argument("--prec", type=int, required=True)
    ap.add_argument("--cap", type=int, required=True)
    ap.add_argument("--NT", type=int, required=True, help="nombre de sous-intervalles en t = y1")
    ap.add_argument("--NK", type=int, required=True, help="nombre de boites en kappa")
    ap.add_argument("--K", type=str, default="4/3")
    ap.add_argument("--rho", type=int, default=2)
    ap.add_argument("--rhoN", type=int, default=4)
    ap.add_argument("--boites", type=str, default="", help="i0:i1 sous-ensemble (tests)")
    ap.add_argument("--sans-garde-cap", action="store_true")
    ap.add_argument("--out", type=str, required=True)
    a = ap.parse_args()
    t0 = time.time()
    D = a.D
    L = D + 5
    fixe_contexte(a.prec, a.cap)
    if not a.sans_garde_cap:
        assert ctx.cap >= L, f"GARDE 1 : ctx.cap = {ctx.cap} < L = {L}"
    sc = series_scalaires(D, L)
    A, E, Ap, resids = polys_t(sc, D)
    rmax = max(abs(r).upper() for r in resids)
    assert all(r.contains(0) for r in resids), "residu de solvabilite ne contient pas 0"
    cst = constantes(a.rho, a.rhoN)
    K = Fraction(a.K)
    NK = a.NK
    i0, i1 = (0, NK) if not a.boites else map(int, a.boites.split(":"))
    res = []
    for i in range(i0, i1):
        k0, k1 = K * i / NK, K * (i + 1) / NK
        r = boite(k0, k1, (A, E, Ap), sc, cst, D, a.NT, a.rho, a.rhoN)
        res.append(r)
        print(f"boite {i:4d} kappa [{float(k0):.5f},{float(k1):.5f}]  LB={float(r['LB']):.6e}  J0={float(r['J0']):.6e} "
              f"J1={float(r['J1']):.6e}  m>={float(r['m']):.4f}  marge={float(r['marge']):.4e}  {'OK' if r['ok'] else 'ECHEC'}",
              flush=True)
    toutes = all(r["ok"] for r in res)
    sha = hashlib.sha256(open(__file__, "rb").read()).hexdigest()
    out = dict(version="ch-v1", script_sha256=sha, D=D, L=L, prec=ctx.prec, cap=ctx.cap, NT=a.NT, NK=NK, K=a.K,
               rho=a.rho, rhoN=a.rhoN, n_assert_prec=NCHK, residu_solvabilite_max=float(rmax),
               constantes={k: arbstr(v) for k, v in cst.items()},
               N_premiers=[arbstr(c) for c in sc["N"][:6]],
               boites=[dict(k0=r["k0"], k1=r["k1"], LB=arbstr(r["LB"]), J0=arbstr(r["J0"]), J1=arbstr(r["J1"]),
                            LB_lo_exact=exact_str(r["LB"]), J0_hi_exact=exact_str(r["J0"]), J1_hi_exact=exact_str(r["J1"]),
                            m=arbstr(r["m"]), marge=arbstr(r["marge"]), ok=r["ok"], restes=r["restes"]) for r in res],
               toutes_ok=toutes, secondes=round(time.time() - t0, 1))
    json.dump(out, open(a.out, "w"), indent=1)
    pire = min(res, key=lambda r: float(r["marge"]))
    print(f"assertions .prec == L : {NCHK} ; residu max {float(rmax):.2e} ; constantes {out['constantes']}")
    print(f"pire marge {float(pire['marge']):.6e} (kappa [{pire['k0']},{pire['k1']}]) ; "
          f"{'TOUTES_OK' if toutes else 'ECHEC'} {sum(r['ok'] for r in res)}/{len(res)} ; {out['secondes']} s")
    sys.exit(0 if toutes else 1)


if __name__ == "__main__":
    main()
