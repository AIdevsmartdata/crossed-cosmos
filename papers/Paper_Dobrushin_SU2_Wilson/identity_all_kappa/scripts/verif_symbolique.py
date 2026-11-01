#!/usr/bin/env python3
"""VERIFICATION SYMBOLIQUE (sympy) des identites algebriques de la preuve (D7 etendu a tout kappa).

Rien n'est ecrit en dur : chaque verdict est le resultat d'un calcul sympy (simplify == 0) ; le script sort avec un code != 0
si une identite echoue.

Objets : t in (-1,1), R = sqrt(1 - t^2), E(t) = exp(kappa t) (la constante 1/Zbar et le facteur 2/pi s'en vont des identites),
u(t) fonction quelconque C^1 (AUCUNE EDO n'est utilisee dans (1)-(3)), mu-moyenne <g> = (2/pi) int g R E dt / Zbar.

(1) IDENTITE-CLE.  Pour toute u,
      W := (1/3) (R^2 u' + (kappa R^2 - 3t) u)^2 - [ R^2 u^2 + (1/15) R^4 (5 u'^2 + 4 kappa u u' + 2 kappa^2 u^2) ]
    verifie  R E W = d/dt ( R E h u^2 )  avec  h = (kappa/5) R^4 - t R^2.
    Donc <W> = 0 (les termes de bord s'annulent : R = 0 en +-1).
(2) Avec l'EDO  R^2 u' + (kappa R^2 - 3t) u = 3 (m1 - t)  :  (1/3)<(...)^2> = 3 <(t - m1)^2> = 3 Var,  d'ou
      <R^2 u^2> + (1/15) <R^4 (5 u'^2 + 4 kappa u u' + 2 kappa^2 u^2)> = 3 Var                         (ID)
    et Xi := <R^2 u^2> + (1/15)<R^4 (u' + kappa u)^2> - <R^2> = -3 Delta - (1/15) <R^4 (4 u'^2 + 2 kappa u u' + kappa^2 u^2)>.
    On verifie ici l'identite algebrique  5u'^2 + 4 k u u' + 2 k^2 u^2 = (u' + k u)^2 + (4 u'^2 + 2 k u u' + k^2 u^2)
    et  4 u'^2 + 2 k u u' + k^2 u^2 = (2 u' + k u / 2)^2 + (3/4) k^2 u^2 .
(3) Moments : (R^3 E)' = R E (kappa R^2 - 3 t),  (R^5 E)' = R E (kappa R^4 - 5 t R^2),  (t R^3 E)' = R E (R^2 - 3 t^2 + kappa t R^2).
(4) Riccati : m' = 1 - 3 m/kappa - m^2 ; minorant ell = (sqrt(kappa^2+4) - 2)/kappa :
      ell' - (1 - 3 ell/kappa - ell^2) = -(s - 2)^2/(s kappa^2) < 0 ,  s = sqrt(kappa^2 + 4),   et   ell^2 + 4 ell/kappa - 1 = 0.
(5) Delta = m^2 + 4 m/kappa - 1 = E x2^2 - Var x1  avec  E x2^2 = m/kappa,  Var x1 = 1 - 3m/kappa - m^2  (moments de x1 sur S^3).
(6) Delta = -kappa d/dkappa (m/kappa) ; (7) Delta = (kappa/3) Cov(x1^2, x1) > 0 (inegalite de Chebyshev sur la loi cosh-symetrisee).
"""
import sys
import sympy as sp

t, k = sp.symbols('t kappa', positive=True)
u = sp.Function('u')(t)
up = sp.diff(u, t)
R = sp.sqrt(1 - t ** 2)
E = sp.exp(k * t)
ok_all = True

def verdict(nom, expr):
    global ok_all
    z = sp.simplify(expr)
    ok = (z == 0)
    ok_all = ok_all and ok
    print(f"[{'OK ' if ok else 'ECHEC'}] {nom}" + ("" if ok else f"  -> reste : {z}"))
    return ok

# ---- (1) identite-cle
h = k / 5 * R ** 4 - t * R ** 2
W = sp.Rational(1, 3) * (R ** 2 * up + (k * R ** 2 - 3 * t) * u) ** 2 \
    - (R ** 2 * u ** 2 + sp.Rational(1, 15) * R ** 4 * (5 * up ** 2 + 4 * k * u * up + 2 * k ** 2 * u ** 2))
verdict("(1) R E W - d/dt( R E h u^2 ) = 0   [u quelconque]", R * E * W - sp.diff(R * E * h * u ** 2, t))

# ---- (3) moments
verdict("(3a) (R^3 E)' = R E (k R^2 - 3t)", sp.diff(R ** 3 * E, t) - R * E * (k * R ** 2 - 3 * t))
verdict("(3b) (R^5 E)' = R E (k R^4 - 5 t R^2)", sp.diff(R ** 5 * E, t) - R * E * (k * R ** 4 - 5 * t * R ** 2))
verdict("(3c) (t R^3 E)' = R E (R^2 - 3t^2 + k t R^2)", sp.diff(t * R ** 3 * E, t) - R * E * (R ** 2 - 3 * t ** 2 + k * t * R ** 2))

# ---- (2) algebre de la somme de carres
a, b = sp.symbols('a b')    # a = u', b = u
verdict("(2a) 5a^2+4kab+2k^2b^2 = (a+kb)^2 + (4a^2+2kab+k^2b^2)",
        5 * a ** 2 + 4 * k * a * b + 2 * k ** 2 * b ** 2 - ((a + k * b) ** 2 + (4 * a ** 2 + 2 * k * a * b + k ** 2 * b ** 2)))
verdict("(2b) 4a^2+2kab+k^2b^2 = (2a+kb/2)^2 + (3/4)k^2 b^2",
        4 * a ** 2 + 2 * k * a * b + k ** 2 * b ** 2 - ((2 * a + k * b / 2) ** 2 + sp.Rational(3, 4) * k ** 2 * b ** 2))
# discriminant de 4a^2+2kab+k^2b^2 (definie positive)
disc = sp.discriminant(4 * a ** 2 + 2 * k * a * b + k ** 2 * b ** 2, a)
print(f"      discriminant en a de 4a^2+2kab+k^2b^2 = {sp.simplify(disc)}  (< 0 pour k,b != 0 : forme definie positive)")
ok_all = ok_all and bool(sp.simplify(disc) == -12 * k ** 2 * b ** 2)

# ---- (2c) l'identite de definition de Xi : A = u E, A' = (u' + k u) E
A = sp.Function('A')(t)
uu = sp.Function('v')(t)
Aexpr = uu * E
Apr = sp.diff(Aexpr, t)
lhs_int = R ** 3 * (Aexpr ** 2 + R ** 2 * Apr ** 2 / 15 - E ** 2) / E
rhs_int = R ** 3 * E * (uu ** 2 + R ** 2 * (sp.diff(uu, t) + k * uu) ** 2 / 15 - 1)
verdict("(2c) R^3 (A^2 + R^2 A'^2/15 - E^2)/E = R^3 E (u^2 + R^2 (u'+k u)^2/15 - 1)", lhs_int - rhs_int)

# ---- (4) Riccati
s = sp.sqrt(k ** 2 + 4)
ell = (s - 2) / k
verdict("(4a) ell' - (1 - 3 ell/k - ell^2) = -(s-2)^2/(s k^2)",
        sp.diff(ell, k) - (1 - 3 * ell / k - ell ** 2) + (s - 2) ** 2 / (s * k ** 2))
verdict("(4b) ell^2 + 4 ell/k - 1 = 0", ell ** 2 + 4 * ell / k - 1)
# developpements : m = I2/I1 = k/4 - k^3/96 + ..., ell = k/4 - k^3/64 + ... => m - ell ~ k^3/192
ser_ell = sp.series(ell, k, 0, 6).removeO()
print("      serie de ell :", ser_ell)
I1 = sp.besseli(1, k); I2 = sp.besseli(2, k)
ser_m = sp.series(I2 / I1, k, 0, 6).removeO()
print("      serie de m   :", ser_m)
diff_ser = sp.expand(ser_m - ser_ell)
c1 = diff_ser.coeff(k, 1); c3 = diff_ser.coeff(k, 3); c0 = diff_ser.coeff(k, 0); c2 = diff_ser.coeff(k, 2); c4 = diff_ser.coeff(k, 4)
ok_c = (c0 == 0 and c1 == 0 and c2 == 0 and c3 == sp.Rational(1, 192) and c4 == 0)
ok_all = ok_all and ok_c
print(f"[{'OK ' if ok_c else 'ECHEC'}] (4c) m - ell = k^3/192 + O(k^5) : coefficients k^0..k^4 = {[c0, c1, c2, c3, c4]}")

# ---- (5) moments de x1 sur S^3 : m = I2/I1 verifie l'equation de Riccati (Bessel)
m = sp.Function('m')
ric = sp.diff(I2 / I1, k) - (1 - 3 * (I2 / I1) / k - (I2 / I1) ** 2)
# on verifie numeriquement (haute precision) car sympy ne simplifie pas bien les Bessel
import mpmath as mpm
mpm.mp.dps = 50
worst = max(abs(mpm.mpf(sp.N(ric.subs(k, mpm.mpf(x)), 50))) for x in ['0.3', '1', '2.5', '7', '20'])
print(f"[{'OK ' if worst < mpm.mpf(10) ** -40 else 'ECHEC'}] (5) Riccati m' = 1 - 3m/k - m^2 pour m = I2/I1 : residu max {mpm.nstr(worst, 3)} en 5 points (numerique)")
ok_all = ok_all and worst < mpm.mpf(10) ** -40

# ---- (6) Delta = -kappa d/dkappa (m/kappa)  (monotonie de E x2^2) : avec m' = 1 - 3 m/kappa - m^2
mm = sp.Function('mm')(k)
expr = sp.diff(mm / k, k).subs(sp.Derivative(mm, k), 1 - 3 * mm / k - mm ** 2)
verdict("(6) d/dk (m/k) = -Delta/k  avec Delta = m^2 + 4m/k - 1  (m' = Riccati)", expr + (mm ** 2 + 4 * mm / k - 1) / k)
# ---- (7) Delta = (kappa/3) Cov_kappa(x1^2, x1) : moments  <t> = m, <t^2> = 1 - 3m/k, <t^3> = m - 3/k + 12 m/k^2  (par parties : (R^3 E)', (t R^3 E)')
mom1, mom2, mom3 = mm, 1 - 3 * mm / k, mm - 3 / k + 12 * mm / k ** 2
cov = mom3 - mom2 * mom1
verdict("(7) Cov(x1^2, x1) = 3 Delta / kappa", cov - 3 * (mm ** 2 + 4 * mm / k - 1) / k)
# controle numerique de <t^3> (mpmath, quadrature) en 3 valeurs de kappa
mpm.mp.dps = 30
def moment(kv, n):
    kv = mpm.mpf(kv)
    Zb = 2 * mpm.besseli(1, kv) / kv
    return mpm.quad(lambda th: mpm.cos(th) ** n * mpm.sin(th) ** 2 * mpm.exp(kv * mpm.cos(th)) / Zb * 2 / mpm.pi, [0, mpm.pi / 2, mpm.pi])
worst3 = 0
for kv in ['0.7', '3', '9']:
    kk_ = mpm.mpf(kv); m1v = moment(kv, 1)
    worst3 = max(worst3, abs(moment(kv, 3) - (m1v - 3 / kk_ + 12 * m1v / kk_ ** 2)), abs(moment(kv, 2) - (1 - 3 * m1v / kk_)))
print(f"[{'OK ' if worst3 < mpm.mpf(10) ** -25 else 'ECHEC'}] (7') moments <t^2>, <t^3> par quadrature : ecart max {mpm.nstr(worst3, 3)} en 3 points (numerique)")
ok_all = ok_all and worst3 < mpm.mpf(10) ** -25

print("TOUTES LES VERIFICATIONS SYMBOLIQUES : " + ("REUSSIES" if ok_all else "ECHEC"))
sys.exit(0 if ok_all else 1)
