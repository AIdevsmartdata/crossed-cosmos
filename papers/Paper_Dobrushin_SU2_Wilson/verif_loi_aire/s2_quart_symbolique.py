#!/usr/bin/env python3
"""s2_quart_symbolique.py -- controle (sympy + mpmath) des identites de la preuve du Theoreme 6 de la note (section 4 : borne du quart, identite chordale).

Usage : python3 -I s2_quart_symbolique.py <sortie.json>
Verdicts calcules ; code de retour != 0 en cas d'echec. Reimplementation independante (ne lit aucun script du
dossier identity_all_kappa/).
"""
import json
import sys

import mpmath as mp
import sympy as sp

OK = {}
res = {}
t, k, m = sp.symbols('t kappa m', real=True)
R = sp.sqrt(1 - t**2)
E = sp.exp(k * t)
u = sp.Function('u')(t)
up = sp.diff(u, t)

# (1) (R^3 E)' = R E (kappa R^2 - 3 t)  ;  (t R^3 E)' = R E (R^2 + kappa t R^2 - 3 t^2)
OK['F1'] = sp.simplify(sp.diff(R**3 * E, t) - R * E * (k * R**2 - 3 * t)) == 0
OK['F4'] = sp.simplify(sp.diff(t * R**3 * E, t) - R * E * (R**2 + k * t * R**2 - 3 * t**2)) == 0

# (2) EDO : A = u E, q = (t-m)E ; t A - R^2 A'/3 - q = E*(t u - t + m - R^2 (u'+kappa u)/3)
A = u * E
q = (t - m) * E
w = t * u - t + m
expr = sp.simplify((t * A - R**2 * sp.diff(A, t) / 3 - q) / E - (w - R**2 * (up + k * u) / 3))
OK['EDO_forme_u_w'] = expr == 0

# (3) identite differentielle R E W = (R E h u^2)'  pour u quelconque
h = k / 5 * R**4 - t * R**2
W = sp.Rational(1, 3) * (R**2 * up + (k * R**2 - 3 * t) * u)**2 - R**2 * u**2 \
    - sp.Rational(1, 15) * R**4 * (5 * up**2 + 4 * k * u * up + 2 * k**2 * u**2)
diffid = sp.simplify(sp.expand(R * E * W - sp.diff(R * E * h * u**2, t)))
OK['identite_RE_W'] = diffid == 0
# terme de bord : R E h u^2 contient R^3
OK['bord_R3'] = sp.simplify(R * E * h / R**3 - E * (k / 5 * R**2 - t)) == 0

# (4) elimination de u' : u' = 3w/R^2 - kappa u
wv, uv, Rv = sp.symbols('w u R', real=True)
upv = 3 * wv / Rv**2 - k * uv
lhs = Rv**4 * (5 * upv**2 + 4 * k * uv * upv + 2 * k**2 * uv**2) / 15
rhs = 3 * wv**2 - sp.Rational(6, 5) * k * Rv**2 * uv * wv + k**2 / 5 * Rv**4 * uv**2
OK['elimination'] = sp.simplify(lhs - rhs) == 0
# (5) carres
sq = 12 * wv**2 - 6 * k * Rv**2 * uv * wv + k**2 * Rv**4 * uv**2 \
    - (12 * (wv - k * Rv**2 * uv / 4)**2 + k**2 / 4 * Rv**4 * uv**2)
OK['completion_carres'] = sp.expand(sq) == 0
# (6) combinaison : Xi = <R^2u^2> + 3/5<w^2> - <R^2>, (ID) et <R^2> = 3(Var+Delta) => Xi = -3 Delta - S
a1, a2, a3, a4, V, Dl = sp.symbols('RRuu ww RRuw R4uu Var Delta', real=True)  # moyennes formelles
RRuu_from_ID = 3 * V - 3 * a2 + sp.Rational(6, 5) * k * a3 - k**2 / 5 * a4
Xi = RRuu_from_ID + sp.Rational(3, 5) * a2 - 3 * (V + Dl)
Sexpr = sp.Rational(1, 5) * (12 * a2 - 6 * k * a3 + k**2 * a4)
OK['Xi_egale_moins3Delta_moins_S'] = sp.simplify(Xi - (-3 * Dl - Sexpr)) == 0

# (7) tranche : boule 3D de rayon R : int dz = 4 pi R^3/3 ; int |z|^2 dz = (3/5) R^2 vol
r, Rs = sp.symbols('r R_s', positive=True)
vol = sp.integrate(4 * sp.pi * r**2, (r, 0, Rs))
m2 = sp.integrate(4 * sp.pi * r**4, (r, 0, Rs))
OK['boule3D_moments'] = sp.simplify(vol - 4 * sp.pi * Rs**3 / 3) == 0 and sp.simplify(m2 - sp.Rational(3, 5) * Rs**2 * vol) == 0
# loi de x1 sous Haar (2/pi) R dt ; |B^4| = pi^2/2 ; |S^3| = 2 pi^2
OK['loi_x1_normalisee'] = sp.simplify(sp.integrate(2 / sp.pi * sp.sqrt(1 - t**2), (t, -1, 1)) - 1) == 0
OK['champ_constant_kappa0_donne_quart'] = sp.simplify((sp.pi**2 / 2) / (2 * sp.pi**2) - sp.Rational(1, 4)) == 0
# constantes de Fubini : (1/2pi^2) * (4pi/3) R^3 = (2/(3pi)) R^3 ; (2/(3pi)) int R^3 E = (1/3) <R^2> avec <g> = (2/pi) int g R E
OK['constantes_fubini'] = sp.simplify((4 * sp.pi / 3) / (2 * sp.pi**2) - 2 / (3 * sp.pi)) == 0 and \
    sp.simplify((2 / (3 * sp.pi)) / (2 / sp.pi) - sp.Rational(1, 3)) == 0 and \
    sp.simplify((1 / (3 * sp.pi)) / (2 / sp.pi) - sp.Rational(1, 6)) == 0

# (8) Riccati => d/dk (m/k) = -Delta/k, Delta = m^2 + 4m/k - 1
mf = sp.Function('mf')(k)
ric = 1 - 3 * mf / k - mf**2
dmk = sp.diff(mf / k, k).subs(sp.diff(mf, k), ric)
OK['derivee_m_sur_k'] = sp.simplify(dmk + (mf**2 + 4 * mf / k - 1) / k) == 0
# (9) Cov(t^2,t) = <t^3> - <t^2> m, <t^2> = 1 - 3m/k, <t^3> = m - 3/k + 12 m/k^2  => 3 Delta / k
cov = (m - 3 / k + 12 * m / k**2) - (1 - 3 * m / k) * m
OK['cov_t2_t'] = sp.simplify(cov - 3 * (m**2 + 4 * m / k - 1) / k) == 0

# ---- numerique (mpmath) ----
mp.mp.dps = 40


def mom(kap):
    Z = mp.quad(lambda s: 2 / mp.pi * mp.sqrt(1 - s**2) * mp.e**(kap * s), [-1, 1])
    m1 = mp.quad(lambda s: 2 / mp.pi * s * mp.sqrt(1 - s**2) * mp.e**(kap * s), [-1, 1]) / Z
    m2_ = mp.quad(lambda s: 2 / mp.pi * s**2 * mp.sqrt(1 - s**2) * mp.e**(kap * s), [-1, 1]) / Z
    return Z, m1, m2_


grid = [mp.mpf(x) / 20 for x in range(1, 81)] + [mp.mpf(x) for x in (5, 6, 8, 10, 20, 50)]
errs_bessel, errs_ric, dch, deltas = [], [], [], []
for kap in grid:
    Z, m1, m2_ = mom(kap)
    errs_bessel.append(abs(m1 - mp.besseli(2, kap) / mp.besseli(1, kap)))
    errs_bessel.append(abs(Z - 2 * mp.besseli(1, kap) / kap))
    mm = mp.besseli(2, kap) / mp.besseli(1, kap)
    dm = mp.diff(lambda x: mp.besseli(2, x) / mp.besseli(1, x), kap)
    errs_ric.append(abs(dm - (1 - 3 * mm / kap - mm**2)))
    ex2 = (1 - m2_) / 3
    dch.append((float(kap), float(mm / kap)))
    errs_bessel.append(abs(ex2 - mm / kap))
    deltas.append(float(mm**2 + 4 * mm / kap - 1))
res['err_max_bessel_moments'] = float(max(errs_bessel))
res['err_max_riccati'] = float(max(errs_ric))
OK['moments_bessel'] = max(errs_bessel) < mp.mpf('1e-25')
OK['riccati'] = max(errs_ric) < mp.mpf('1e-20')
vals = [d for _, d in dch]
OK['Dch_strictement_decroissante_et_sous_quart'] = all(vals[i + 1] < vals[i] for i in range(len(vals) - 1)) and max(vals) < 0.25
OK['Delta_positif_grille'] = min(deltas) > 0
res['Dch_table'] = {str(round(kv, 4)): round(d, 10) for kv, d in dch if kv in (0.05, 0.5, 1.0, 1.35, 2.0, 3.0, 4.0, 6.0, 10.0, 50.0)}


# Xi + 3 Delta + S = 0 par quadrature directe (u = A/E, A = 3 R^-3 int_t^1 (s-m) E R ds)
def chain(kap):
    kap = mp.mpf(kap)
    Z = 2 * mp.besseli(1, kap) / kap
    mm = mp.besseli(2, kap) / mp.besseli(1, kap)
    Ef = lambda s: mp.e**(kap * s) / Z

    def Afun(s):
        if 1 - s**2 < mp.mpf('1e-14'):
            # limite exacte de l'EDO en t = +-1 : A(1) = (1-m)E(1), A(-1) = (1+m)E(-1)
            return (1 - mm) * Ef(s) if s > 0 else (1 + mm) * Ef(s)
        if s >= 0:
            I = mp.quad(lambda x: (x - mm) * Ef(x) * mp.sqrt(1 - x**2), [s, 1])
            return 3 * I / (1 - s**2)**mp.mpf(1.5)
        I = mp.quad(lambda x: (x - mm) * Ef(x) * mp.sqrt(1 - x**2), [-1, s])
        return -3 * I / (1 - s**2)**mp.mpf(1.5)

    def avg(g):
        # <g> = (2/pi) int g R E dt, changement t = cos(theta)
        return mp.quad(lambda th: 2 / mp.pi * g(mp.cos(th)) * mp.sin(th)**2 * Ef(mp.cos(th)),
                       mp.linspace(0, mp.pi, 9), method='gauss-legendre')

    def uw(s):
        a = Afun(s)
        uu = a / Ef(s)
        ww = s * uu - s + mm
        return uu, ww

    RRuu = avg(lambda s: (1 - s**2) * uw(s)[0]**2)
    ww2 = avg(lambda s: uw(s)[1]**2)
    RR = avg(lambda s: 1 - s**2)
    Xi = RRuu + mp.mpf(3) / 5 * ww2 - RR
    Dl = mm**2 + 4 * mm / kap - 1
    S = avg(lambda s: (12 * (uw(s)[1] - kap * (1 - s**2) * uw(s)[0] / 4)**2 + kap**2 / 4 * (1 - s**2)**2 * uw(s)[0]**2)) / 5
    return Xi, Dl, S


mp.mp.dps = 25
chk = {}
for kap in ('0.5', '2', '4'):
    Xi, Dl, S = chain(kap)
    chk[kap] = {'Xi': float(Xi), 'Delta': float(Dl), 'S': float(S), 'residu': float(Xi + 3 * Dl + S)}
res['chaine_Xi_Delta_S'] = chk
OK['Xi_plus_3Delta_plus_S_nul_numerique'] = all(abs(v['residu']) < 1e-12 for v in chk.values())

res['verdicts'] = {kk: bool(vv) for kk, vv in OK.items()}
res['tous_ok'] = all(bool(vv) for vv in OK.values())
out = sys.argv[1] if len(sys.argv) > 1 else 's2_quart_symbolique.json'
with open(out, 'w') as f:
    json.dump(res, f, indent=1)
for kk, vv in res['verdicts'].items():
    print(f'{kk:45s} {vv}')
print('chaine', chk)
print('tous_ok =', res['tous_ok'])
sys.exit(0 if res['tous_ok'] else 1)
