#!/usr/bin/env python3
# gate_numerique.py -- CH (chordal certificate), gate G6 [numerique, PAS une preuve] : controles independants du chemin Arb.
#  (a) A(t) par quadrature directe (mpmath, formule integrale A = 3 G/(1-t^2)^{3/2}) contre la serie sum k^j A_j(t) ;
#  (b) le champ V : divergence (differences finies) ~ 0 dans la boule, flux V.x = (u - ubar) e^{k x1}/Z sur S^3 ;
#  (c) borne de Beckmann COMPLETE B(k,a) = (1/2pi^2) int_B |V| par quadrature 3D directe (y1, y2, rho), sans la
#      formule close en theta de l'exploration ; verifie B <= Var(u) + cos^2 a max(J0,J1) <= E x2^2 <= 1/4 ;
#  (d) comparaison aux LP de ../calc/lp2d_m14.log (valeurs recopiees ci-dessous) (minorants discretises de D_ch).
import sys, os, math
import numpy as np
import mpmath as mp
from numpy.polynomial.legendre import leggauss
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import cert_ch as C
from flint import arb

mp.mp.dps = 30
D = 80
C.fixe_contexte(128, 200)
sc = C.series_scalaires(D, D + 5)
A, E, Ap, _ = C.polys_t(sc, D)
Af = [[float(c.mid()) for c in p.coeffs()] for p in A]
Apf = [[float(c.mid()) for c in p.coeffs()] for p in Ap]


def serie(polys, k, t):
    return sum(k ** j * np.polynomial.polynomial.polyval(t, c) for j, c in enumerate(polys) if c)


def mom(k):
    k = mp.mpf(k)
    Z = mp.quad(lambda s: mp.sqrt(1 - s * s) * mp.e ** (k * s), [-1, 1]) * 2 / mp.pi
    m1 = mp.quad(lambda s: s * mp.sqrt(1 - s * s) * mp.e ** (k * s), [-1, 1]) * 2 / mp.pi / Z
    m2 = mp.quad(lambda s: s * s * mp.sqrt(1 - s * s) * mp.e ** (k * s), [-1, 1]) * 2 / mp.pi / Z
    return Z, m1, m2


def A_direct(k, t, Z, m1):
    k, t = mp.mpf(k), mp.mpf(t)
    if t >= 0:
        G = mp.quad(lambda s: (s - m1) * mp.e ** (k * s) * mp.sqrt(1 - s * s), [t, 1]) / Z
    else:
        G = -mp.quad(lambda s: (s - m1) * mp.e ** (k * s) * mp.sqrt(1 - s * s), [-1, t]) / Z
    return 3 * G / (1 - t * t) ** mp.mpf(1.5)


ok = True
print("(a) A serie contre A quadrature directe")
emax = 0
for k in (0.3, 1.0, 4 / 3):
    Z, m1, m2 = mom(k)
    for t in (-0.99, -0.6, -0.1, 0.0, 0.35, 0.8, 0.999):
        d = abs(float(A_direct(k, t, Z, m1)) - serie(Af, k, t))
        emax = max(emax, d)
print(f"    max |A_serie - A_direct| = {emax:.2e}")
ok &= emax < 1e-10

print("(b) divergence et flux du champ V (differences finies, points aleatoires)")
rng = np.random.default_rng(20260928)


def Vfield(k, al, y, Z):
    y1 = y[0]
    a = serie(Af, k, y1)
    ap = serie(Apf, k, y1)
    Ee = math.exp(k * y1) / Z
    z = np.array([0.0, y[1], y[2], y[3]])
    V1 = a * np.array([1.0, 0, 0, 0]) - ap / 3 * z
    V2 = Ee * np.array([0, 1.0, 0, 0])
    return math.cos(al) * V1 + math.sin(al) * V2


dmax = fmax = 0
for k in (0.5, 4 / 3):
    Z, m1, m2 = [float(x) for x in mom(k)]
    for _ in range(40):
        al = rng.uniform(0, math.pi)
        y = rng.normal(size=4)
        y *= rng.uniform(0, 0.97) / np.linalg.norm(y)
        h = 1e-5
        div = sum((Vfield(k, al, y + h * np.eye(4)[i], Z)[i] - Vfield(k, al, y - h * np.eye(4)[i], Z)[i]) / (2 * h) for i in range(4))
        dmax = max(dmax, abs(div))
        x = rng.normal(size=4)
        x /= np.linalg.norm(x)
        u = math.cos(al) * x[0] + math.sin(al) * x[1]
        ub = math.cos(al) * m1
        w = (u - ub) * math.exp(k * x[0]) / Z
        fmax = max(fmax, abs(Vfield(k, al, x, Z) @ x - w))
print(f"    max |div V| = {dmax:.2e} ; max |V.x - w| sur S^3 = {fmax:.2e}")
ok &= dmax < 1e-6 and fmax < 1e-10

print("(c) Beckmann complet par quadrature 3D directe (y1 x y2 x rho, poids 2 pi rho)")
g1, w1 = leggauss(160)
g2, w2 = leggauss(80)
g3, w3 = leggauss(40)
LPm14 = {0.5: [0.24350, 0.24377, 0.24453, 0.24556, 0.24658, 0.24728, 0.24742],
         1.0: [0.22526, 0.22629, 0.22910, 0.23291, 0.23665, 0.23933, 0.24015],
         4 / 3: [0.20887, 0.21059, 0.21524, 0.22145, 0.22752, 0.23185, 0.23324]}
for k in (0.25, 0.5, 1.0, 4 / 3):
    Z, m1, m2 = [float(x) for x in mom(k)]
    Ex2 = (1 - m2) / 3
    Var1 = m2 - m1 * m1
    y1 = g1
    a_ = serie(Af, k, y1)
    ap_ = serie(Apf, k, y1)
    Ee = np.exp(k * y1) / Z
    R = np.sqrt(1 - y1 ** 2)
    # J0, J1 numeriques (meme definition que le certificat, m(y1) = min(A,E) - |A'| R/6)
    mm = np.minimum(a_, Ee) - np.abs(ap_) * R / 6
    J0 = (w1 * (2 / (5 * np.pi)) * (ap_ / 3) ** 2 * R ** 5 / (2 * mm)).sum()
    J1 = (w1 * (2 / (3 * np.pi)) * (Ee - a_) ** 2 * R ** 3 / (2 * mm)).sum() + 2 / 3 * J0
    row = []
    for ia, al in enumerate(np.linspace(0, np.pi / 2, 7)):
        ca, sa = math.cos(al), math.sin(al)
        tot = 0.0
        for i in range(len(g1)):
            y2 = R[i] * g2
            wy2 = w2 * R[i]
            rho_max = np.sqrt(np.maximum(R[i] ** 2 - y2 ** 2, 0))
            rho = rho_max[:, None] * (g3[None, :] + 1) / 2
            wr = w3[None, :] * rho_max[:, None] / 2
            b = ca * ap_[i] / 3
            V0 = ca * a_[i]
            V1c = sa * Ee[i] - b * y2[:, None]
            nrm = np.sqrt(V0 ** 2 + V1c ** 2 + (b * rho) ** 2)
            tot += w1[i] * (wy2[:, None] * wr * 2 * np.pi * rho * nrm).sum()
        Bv = tot / (2 * np.pi ** 2)
        varu = ca * ca * Var1 + sa * sa * Ex2
        borne = varu + ca * ca * max(J0, J1)
        row.append(Bv)
        c1 = Bv <= borne + 1e-9
        c2 = borne <= Ex2 + 1e-12
        ok &= c1 and c2
        if not (c1 and c2):
            print(f"    ECHEC k={k} a={al}: B={Bv} borne={borne} Ex2={Ex2}")
    lp = LPm14.get(k)
    print(f"    k={k:.4f} E x2^2={Ex2:.6f} Var x1={Var1:.6f} J0={J0:.3e} J1={J1:.3e}  B(a=0..pi/2)=" +
          " ".join(f"{v:.5f}" for v in row) + ("" if lp is None else "  | LP m14 = " + " ".join(f"{v:.5f}" for v in lp)))
    if lp is not None:
        ecart = max(l - b for l, b in zip(lp, row))
        print(f"      max(LP - B) = {ecart:.1e} (LP = minorant discretise ; ecart attendu <= erreur de discretisation ~1e-4)")
        ok &= ecart < 5e-4
    ok &= abs(row[-1] - Ex2) < 1e-7
print("GATE_NUMERIQUE", "OK" if ok else "ECHEC")
sys.exit(0 if ok else 1)
