#!/usr/bin/env python3
"""V-CH (independent check of the chordal certificate, 28/09/2026) -- certificat INDEPENDANT, mpmath.iv + coefficients exacts (fractions).

Aucun import du code de CH. Differences de methode avec cert_ch.py :
  * arithmetique : mpmath.iv (intervalles a bornes flottantes, arrondi dirige) et non Arb/python-flint ;
  * coefficients : fractions exactes (coefs_exacts.py), resolution descendante propre ;
  * queues : induction elementaire |zeta_n| <= 2^-n (Z(2) <= e-1 < 2), |mu_n| <= (e-2) 2^-n,
    ||A_j|| <= 3 ||q_j|| (psi <= 1 : avec g(th) = sin^3 th - (th - sin th cos th)/2, g' = sin^2 th (3 cos th - 1), g(0) = 0, g(pi/2) > 0), Markov pour A'_j ; pas d'estimation de Cauchy complexe ;
  * quadrature : partition UNIFORME EN THETA (t = cos theta), poids exacts int_T R^k dt = int sin^{k+1},
    borne sup_T(g) * int_T R^k (et non |T| sup(g R^k)) ;
  * evaluation polynomiale : Horner naif sur intervalle (pas de forme centree).

Verifie, pour chaque boite K = [k0,k1] :
    Nt_lo / Z_hi^2  >  max(J0_hi, J1_hi),   m_lo > 0 sur chaque sous-intervalle,
avec  J0 = (2/(5 pi)) int (At/3)^2 R^5/(2m),  J1 = (2/(3 pi)) int Dt^2 R^3/(2m) + (2/3) J0,
      m = min(A, E) - |A'| R / 6,  At = A'/k,  Dt = (E - A)/k.
"""
import sys, os, json, pickle, time, argparse, hashlib
from fractions import Fraction as Fr
from multiprocessing import Pool
from mpmath import iv, mpf

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)

G = {}

def ivF(x):
    x = Fr(x)
    return iv.mpf(x.numerator) / iv.mpf(x.denominator)

def check_prec(P):
    assert iv.prec == P, f"GARDE PREC : iv.prec = {iv.prec} != {P}"
    w = (iv.mpf(1)/3).delta
    assert w <= mpf(2)**(-(P-2)), f"GARDE PREC : largeur 1/3 = {w} incompatible avec prec {P}"

def init(pkl, D, P):
    iv.prec = P
    check_prec(P)
    d = pickle.load(open(pkl, 'rb'))
    assert d['M'] >= D + 2
    A, e, Nt, Z = d['A'], d['e'], d['Nt'], d['Z']
    # gardes de longueur (analogue du piege du 27/09 : aucune serie tronquee silencieusement)
    for j in range(D+1):
        assert len(A[j]) == j+1 and len(e[j]) == j+1, j
        assert d['res'][j] == 0, f"residu de solvabilite non nul j={j}"
    assert A[0] == [1] and e[0] == [1]
    # familles de polynomes : liste (j, shift, coeffs exacts)
    Apol  = [(j, 0, A[j]) for j in range(D+1)]
    Epol  = [(j, 0, e[j]) for j in range(D+1)]
    Atil  = [(j, 1, [i*A[j][i] for i in range(1, j+1)]) for j in range(1, D+1)]           # A'_j / k
    Dtil  = [(j, 1, [e[j][i]-A[j][i] for i in range(j+1)]) for j in range(1, D+1)]         # (e_j - A_j)/k
    fam = {}
    for name, pol in (('A', Apol), ('E', Epol), ('At', Atil), ('Dt', Dtil)):
        fam[name] = [(j, s, [ivF(c) for c in cs]) for (j, s, cs) in pol]
    MN = len(Nt) - 1
    G.update(scale=Fr(os.environ.get('VCH_LHS_SCALE','1')), P=P, D=D, fam=fam, Nt=[ivF(c) for c in Nt], MN=MN, Z=[ivF(c) for c in Z], MZ=len(Z)-1)

def tails(k1, D):
    """Queues j > D (majorants), k1 = borne sup de la boite (k1 < 2).
       alpha_j = 3 e^2 2^-j (1 + j (e-2)) >= ||A_j||_inf ;  ||e_j|| <= e^2 2^-j ;  ||A'_j|| <= j^2 alpha_j."""
    E2 = iv.exp(iv.mpf(2)); em2 = iv.e - 2
    x = iv.mpf(k1)/2
    xb = x.b
    assert xb < 1
    def S(fn, shift):
        # sum_{j>D} k1^{j-shift} 2^{-j} fn(j) = k1^{-shift} sum x^j fn(j) ; fn polynome croissant de degre <= 3
        tot = iv.mpf(0); j = D+1
        term = lambda j: iv.mpf(xb)**j * fn(j)
        while True:
            tj = term(j)
            tot += tj
            if j > D+50 and tj.b < mpf(2)**(-200): break
            j += 1
        # reste : ratio term(j+1)/term(j) <= xb ((j+1)/j)^3 =: r < 1
        r = iv.mpf(xb)*((iv.mpf(j+1)/j)**3)
        assert r.b < 1
        rest = term(j+1)/(1-r)
        return ((tot + rest)/(iv.mpf(k1)**shift)).b
    al = lambda j: 3*E2*(1 + j*em2)
    tA  = S(al, 0)
    tE  = S(lambda j: E2, 0)
    tAt = S(lambda j: j*j*al(j), 1)
    tDt = S(lambda j: E2 + al(j), 1)
    return dict(A=tA, E=tE, At=tAt, Dt=tDt)

def fold(name, Kp):
    fam = G['fam'][name]
    deg = max(len(cs) for (_, _, cs) in fam) - 1
    c = [iv.mpf(0)]*(deg+1)
    for (j, s, cs) in fam:
        kp = Kp[j-s]
        for i, a in enumerate(cs):
            if a != 0: c[i] += a*kp
    assert len(c) == deg+1
    return c

def horner(c, T):
    r = iv.mpf(0)
    for a in reversed(c):
        r = r*T + a
    return r

def ser(coefs, K):
    r = iv.mpf(0)
    for a in reversed(coefs): r = r*K + a
    return r

def Zbound4():
    """Z(4), Z'(4), Z''(4) majores (series a coefficients >= 0, somme partielle + reste geometrique)."""
    z = G['Z']; MZ = G['MZ']
    s0 = s1 = s2 = iv.mpf(0)
    for n in range(MZ+1):
        s0 += z[n]*iv.mpf(4)**n
        if n >= 1: s1 += n*z[n]*iv.mpf(4)**(n-1)
        if n >= 2: s2 += n*(n-1)*z[n]*iv.mpf(4)**(n-2)
    return s0, s1, s2

def box(args):
    k0, k1, NT = args
    P, D = G['P'], G['D']
    iv.prec = P
    if os.environ.get('VCH_SABOTAGE_PREC'): iv.prec = int(os.environ['VCH_SABOTAGE_PREC'])
    check_prec(P)
    k0, k1 = Fr(k0), Fr(k1)
    K = iv.mpf([ivF(k0).a, ivF(k1).b])
    Kp = [iv.mpf(1)]
    for _ in range(D+1): Kp.append(Kp[-1]*K)
    tl = tails(ivF(k1).b, D)
    C = {n: fold(n, Kp) for n in ('A', 'E', 'At', 'Dt')}
    # Nt(K) et Z(K) : series exactes + restes (coefficients majorants, rayon 4)
    MN, MZ = G['MN'], G['MZ']
    z = G['Z']
    # reste de Z : sum_{n>MZ} z_n k^n <= Z(4) (k/4)^(MZ+1)/(1-k/4)
    Z4, Z4p, Z4pp = Zbound4()
    q = iv.mpf(ivF(k1).b)/4
    rZ = (Z4*q**(MZ+1)/(1-q)).b
    Zk = ser(z, K) + iv.mpf([-rZ, rZ])
    # reste de Nt = N/k^2 : |n_{k}| <= p_k, P = Z^2/3 + (4/3) Z'' Z + Z'^2 a coefficients >= 0 ; p_k <= P(4) 4^-k
    P4 = Z4**2/3 + iv.mpf(4)/3*Z4pp*Z4 + Z4p**2
    rN = (P4/16 * q**(MN+1)/(1-q)).b
    Ntk = ser(G['Nt'], K) + iv.mpf([-rN, rN])
    lhs = Ntk / Zk**2 * ivF(G['scale'])
    # quadrature en theta
    pi = iv.pi
    th = [pi*i/NT for i in range(NT+1)]
    F6 = lambda t: 5*t/16 - 15*iv.sin(2*t)/64 + 3*iv.sin(4*t)/64 - iv.sin(6*t)/192
    F4 = lambda t: 3*t/8 - iv.sin(2*t)/4 + iv.sin(4*t)/32
    f6 = [F6(t) for t in th]; f4 = [F4(t) for t in th]
    J0h = iv.mpf(0); J1ph = iv.mpf(0); J0l = iv.mpf(0); J1pl = iv.mpf(0)
    mmin = None
    for i in range(NT):
        ca, cb = iv.cos(th[i+1]), iv.cos(th[i])
        T = iv.mpf([ca.a, cb.b])
        sa, sb = iv.sin(th[i]), iv.sin(th[i+1])
        Rlo = min(sa.a, sb.a)
        if Rlo < 0: Rlo = mpf(0)
        Rhi = mpf(1) if (th[i].a <= (pi/2).b and th[i+1].b >= (pi/2).a) else max(sa.b, sb.b)
        A_ = horner(C['A'], T) + iv.mpf([-tl['A'], tl['A']])
        E_ = horner(C['E'], T) + iv.mpf([-tl['E'], tl['E']])
        At = horner(C['At'], T) + iv.mpf([-tl['At'], tl['At']])
        Dt = horner(C['Dt'], T) + iv.mpf([-tl['Dt'], tl['Dt']])
        absAt_hi = max(abs(At.a), abs(At.b))
        absAt_lo = mpf(0) if (At.a <= 0 <= At.b) else min(abs(At.a), abs(At.b))
        absDt_hi = max(abs(Dt.a), abs(Dt.b))
        absDt_lo = mpf(0) if (Dt.a <= 0 <= Dt.b) else min(abs(Dt.a), abs(Dt.b))
        Kb = ivF(k1).b; Ka = ivF(k0).a
        # m = min(A,E) - |A'| R/6,  |A'| = k |At|
        m_lo = (iv.mpf(min(A_.a, E_.a)) - iv.mpf(Kb)*iv.mpf(absAt_hi)*iv.mpf(Rhi)/6).a
        m_hi = (iv.mpf(min(A_.b, E_.b)) - iv.mpf(Ka)*iv.mpf(absAt_lo)*iv.mpf(Rlo)/6).b
        assert m_lo > 0, f"m_lo <= 0 : K=[{k0},{k1}] i={i} m_lo={m_lo}"
        mmin = m_lo if mmin is None else min(mmin, m_lo)
        W5 = f6[i+1] - f6[i]; W3 = f4[i+1] - f4[i]
        g0h = (iv.mpf(absAt_hi)**2/9) / (2*iv.mpf(m_lo))
        g1h = iv.mpf(absDt_hi)**2 / (2*iv.mpf(m_lo))
        g0l = (iv.mpf(absAt_lo)**2/9) / (2*iv.mpf(m_hi)) if m_hi > 0 else iv.mpf(0)
        g1l = iv.mpf(absDt_lo)**2 / (2*iv.mpf(m_hi)) if m_hi > 0 else iv.mpf(0)
        J0h += g0h*iv.mpf(W5.b); J1ph += g1h*iv.mpf(W3.b)
        J0l += g0l*iv.mpf(max(W5.a, 0)); J1pl += g1l*iv.mpf(max(W3.a, 0))
    c0 = 2/(5*pi); c1 = 2/(3*pi)
    J0_hi = (c0*J0h).b; J1_hi = (c1*J1ph + iv.mpf(2)/3*c0*J0h).b
    J0_lo = (c0*J0l).a; J1_lo = (c1*J1pl + iv.mpf(2)/3*c0*J0l).a
    ok = lhs.a > max(J0_hi, J1_hi)
    check_prec(P)
    return dict(k0=str(k0), k1=str(k1), lb=float(lhs.a), ub=float(lhs.b), J0_hi=float(J0_hi), J1_hi=float(J1_hi),
                J0_lo=float(J0_lo), J1_lo=float(J1_lo), m_lo=float(mmin), marge=float((lhs.a - max(J0_hi, J1_hi)).a), ok=bool(ok),
                tails={k: float(v) for k, v in tl.items()}, rN=float(rN), rZ=float(rZ))

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--pkl', default=os.path.join(HERE, 'out', 'coefs_M100.pkl'))
    ap.add_argument('--D', type=int, required=True)
    ap.add_argument('--prec', type=int, required=True)
    ap.add_argument('--NT', type=int, required=True)
    ap.add_argument('--NK', type=int, default=0, help='couverture uniforme de [0,4/3] en NK boites')
    ap.add_argument('--boxes', default='', help='liste k0:k1,k0:k1 (rationnels)')
    ap.add_argument('--procs', type=int, default=24)
    ap.add_argument('--out', required=True)
    a = ap.parse_args()
    if a.NK:
        bx = [(str(Fr(4, 3)*i/a.NK), str(Fr(4, 3)*(i+1)/a.NK)) for i in range(a.NK)]
    else:
        bx = [tuple(s.split(':')) for s in a.boxes.split(',')]
    dM = pickle.load(open(a.pkl, 'rb'))['M']
    if dM < a.D + 2:
        print(f'REFUS : pickle M={dM} < D+2={a.D+2} (serie trop courte)'); sys.exit(1)
    t0 = time.time()
    with Pool(a.procs, initializer=init, initargs=(a.pkl, a.D, a.prec)) as pool:
        res = pool.map(box, [(k0, k1, a.NT) for (k0, k1) in bx], chunksize=1)
    nok = sum(r['ok'] for r in res)
    for r in res:
        print(f"K=[{r['k0']},{r['k1']}] lb={r['lb']:.6e} ub={r['ub']:.6e} J0<={r['J0_hi']:.5e} J1<={r['J1_hi']:.5e} "
              f"(J0>={r['J0_lo']:.5e} J1>={r['J1_lo']:.5e}) m>={r['m_lo']:.4f} marge={r['marge']:.4e} {'OK' if r['ok'] else 'ECHEC'}")
    w = min(res, key=lambda r: r['marge'])
    cover = None
    if a.NK:
        cover = all(Fr(res[i]['k1']) == Fr(res[i+1]['k0']) for i in range(len(res)-1)) and Fr(res[0]['k0']) == 0 and Fr(res[-1]['k1']) == Fr(4, 3)
    print(f"BILAN D={a.D} prec={a.prec} NT={a.NT} boites={len(res)} OK={nok}/{len(res)} pire marge={w['marge']:.4e} "
          f"en [{w['k0']},{w['k1']}] couverture_[0,4/3]={cover} queue_max(At)={max(r['tails']['At'] for r in res):.2e} "
          f"{time.time()-t0:.0f}s")
    json.dump(dict(args=vars(a), res=res, nok=nok, cover=cover,
                   pkl_sha=hashlib.sha256(open(a.pkl, 'rb').read()).hexdigest()), open(a.out, 'w'), indent=1)
    sys.exit(0 if nok == len(res) else 2)

if __name__ == '__main__':
    main()
