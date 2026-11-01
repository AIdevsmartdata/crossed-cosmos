#!/usr/bin/env python3
"""anneau4_controle.py : sur l'anneau de 4 sites (O(4), poids exp(2J<s,s'>)), Z = sum_j d_j^2 m_j(J)^4 (caractères),
E[s0.s1] = (1/2) d/dJ1 log Z ; on vérifie E = u + u^3 + O(J^5) (un chemin de longueur 3 contribue u^3)."""
import sympy as sp
J = sp.Symbol('J', positive=True)
def m(j2, x):   # m_j(x) = I_{2j+1}(2x)/x, j2 = 2j
    return sp.besseli(j2 + 1, 2 * x) / x
J1 = sp.Symbol('J1', positive=True)
Z = sum((j2 + 1)**2 * m(j2, J1) * m(j2, J)**3 for j2 in range(0, 6))
E = sp.diff(sp.log(Z), J1).subs(J1, J) / 2
Es = sp.series(E, J, 0, 7).removeO()
u = sp.series(sp.besseli(2, 2*J)/sp.besseli(1, 2*J), J, 0, 7).removeO()
print("E[s0.s1] anneau 4 =", sp.expand(Es))
print("u + u^3            =", sp.expand(sp.series(u + u**3, J, 0, 7).removeO()))
print("différence (ordre <= J^4) :", sp.expand(sp.series(Es - u - u**3, J, 0, 5).removeO()))
