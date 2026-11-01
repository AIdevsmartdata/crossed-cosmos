#!/usr/bin/env python3
"""o4_ordre_J3.py — vérification adverse (Opus) : test de la FORCE de l'amélioration (I) à l'ordre J^3.

Cas L_0 = 1, J_M = infini du cadre de BS83 (liens horizontaux plats) : une tranche = modèle O(4) PUR sur Z^3,
poids exp(2J <s_x, s_y>). La prop. 4.3 + (4.1) s'y appliquent ; la méthode donne E[s_0.s_e] <= 2 G~(0,e).
Vérité (développement de haute température) : E[s_0.s_e] = u + 4 u^3 + O(J^5), u = I_2(2J)/I_1(2J) = J/2 - J^3/12 + ...
  (4 chemins de longueur 3 qui ferment une plaquette avec le lien ; chacun contribue u^3 — vérifié sur l'anneau de 4
   sites par développement en caractères : E = u + u^3 + ...).
Méthode : G~(0,e) = sum_w J^|w| prod_z A~_{n_z}(J), avec A~_n = int f_n h, h = rho((1-l)^2)^3 (Cauchy–Schwarz, 6 liens).
          G_ex(0,e) : même chose avec le facteur EXACT c(l) = prod_liens rho(s_l) pour la marche directe (ordre J^3).
Test : coefficient de J^3 de 2G~ >= celui de la vérité (sinon (I) serait TROP FORTE => faux) ; et 2G_ex = vérité.
"""
import sympy as sp
from itertools import product

J, l0, l1, a, b = sp.symbols("J l0 l1 a b", positive=True)
K = 6  # ordre de troncature en J pour les séries
# M_J(s) = sum_k (J^2 s)^k/(k!(k+1)!) ; rho(s) = M(s)/M(1)
s = sp.Symbol("s")
M = sum((J**2 * s)**k / (sp.factorial(k) * sp.factorial(k + 1)) for k in range(4))
rho = lambda x: sp.series((M.subs(s, x) / M.subs(s, 1)), J, 0, K).removeO()
f = lambda n, lam: lam**(n - 1) * (1 - lam) / sp.factorial(n - 1)

def At(n, puissance=3):
    """A~_n(J) = int_0^1 f_n(l) rho((1-l)^2)^puissance dl, en série de J."""
    h = sp.series(rho((1 - l0)**2)**puissance, J, 0, K).removeO()
    return sp.expand(sp.integrate(sp.expand(f(n, l0) * h), (l0, 0, 1)))

A = {n: At(n) for n in (1, 2, 3)}
# marches de longueur 1 et 3 de 0 à e1 sur Z^3
dirs = [(1,0,0),(-1,0,0),(0,1,0),(0,-1,0),(0,0,1),(0,0,-1)]
def poids_marche(pas):
    pos = (0,0,0); visites = {pos: 1}
    for d in pas:
        pos = tuple(p + q for p, q in zip(pos, d)); visites[pos] = visites.get(pos, 0) + 1
    if pos != (1,0,0): return None
    w = J**len(pas)
    for n in visites.values(): w *= A[n]
    return w
G = 0; nb = {}
for L in (1, 3):
    for pas in product(dirs, repeat=L):
        w = poids_marche(pas)
        if w is not None:
            G += w; nb[L] = nb.get(L, 0) + 1
G = sp.expand(sp.series(sp.expand(G), J, 0, 4).removeO())
# version EXACTE (sans Cauchy–Schwarz) pour la marche directe : c = rho(a0 a1) rho(a0)^5 rho(a1)^5, a = 1 - l
c_ex = sp.series(rho((1 - l0) * (1 - l1)) * rho(1 - l0)**5 * rho(1 - l1)**5, J, 0, 4).removeO()
direct_ex = J * sp.integrate(sp.integrate(sp.expand(f(1, l0) * f(1, l1) * c_ex), (l0, 0, 1)), (l1, 0, 1))
G_ex = sp.expand(sp.series(G - J * A[1]**2 + direct_ex, J, 0, 4).removeO())
# vérité
x = 2 * J
u = sp.series(sp.besseli(2, x) / sp.besseli(1, x), J, 0, 6).removeO()
verite = sp.expand(sp.series(u + 4 * u**3, J, 0, 4).removeO())
print("nombre de marches 0->e1 : longueur 1 :", nb.get(1), " longueur 3 :", nb.get(3))
print("A~_1(J) =", sp.series(A[1], J, 0, 4))
print("2 G~ (Cauchy-Schwarz)      =", sp.expand(2 * G))
print("2 G_ex (facteur exact)      =", sp.expand(2 * G_ex))
print("vérité u + 4u^3             =", verite)
c3 = lambda e: sp.Rational(sp.expand(e).coeff(J, 3))
print("coeff J^3 : CS =", c3(2*G), "=", float(c3(2*G)), " exact =", c3(2*G_ex), " vérité =", c3(verite))
print("borne CS >= vérité à l'ordre J^3 :", c3(2*G) >= c3(verite), " ; exact == vérité :", sp.simplify(c3(2*G_ex) - c3(verite)) == 0)
# sensibilité : avec h = rho^p, quel p ferait échouer la borne ?
for p in (3, 4, 6):
    Ap = At(1, p)
    Gp = sp.expand(sp.series(G - J * A[1]**2 + J * Ap**2, J, 0, 4).removeO())
    print(f"  h = rho^{p} : coeff J^3 de 2G = {c3(2*Gp)} ({float(c3(2*Gp)):.4f})  >= vérité ({float(c3(verite)):.4f}) ? {c3(2*Gp) >= c3(verite)}")
