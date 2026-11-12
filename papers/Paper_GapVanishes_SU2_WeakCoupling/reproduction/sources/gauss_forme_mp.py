#!/usr/bin/env python3
r"""V2 : forme de K -> R(K) = V_K/Gamma_K en HAUTE PRECISION (mpmath, 50 chiffres).  Le balayage en double precision
de gauss_formules.py souffre d'une annulation catastrophique dans V_K = (1+2e)^{-3/2} - (1+e)^{-3} (e = s/K petit) ;
ici on verifie : (i) R(K) decroit vers (s/c)^2 quand K croit ; (ii) le developpement
R = (1/rho^2) [1 + (5/4)(1 - rho^2) e^2 + O(e^3)], rho = c/s, e = s/K (calcul a la main, controle symbolique ici)."""
import json
import mpmath as mp
import sympy as S
mp.mp.dps = 50
def R(rho, e):
    V = (1 + 2*e)**mp.mpf(-1.5) - (1 + e)**(-3)
    u = (rho*e/(1 + e))**2
    G = (1 + e)**(-3) * ((1 - u)**mp.mpf(-1.5) - 1)
    return V / G
out = {}
for rho in ['0.9', '0.5', '0.121', '0.0161', '1e-3', '1e-6']:
    r = mp.mpf(rho)
    es = [mp.mpf(10)**(k/mp.mpf(20)) for k in range(-140, 61)]   # e = s/K de 1e-7 a 1e3
    vals = [R(r, e) for e in es]
    dec = all(vals[i] <= vals[i+1] for i in range(len(vals)-1))   # R croissante en e  <=>  decroissante en K
    out[rho] = {"R_croissante_en_e_(decroissante_en_K)": dec, "min": mp.nstr(min(vals), 15), "limite": mp.nstr(1/r**2, 15),
                "ecart_relatif_e_1e-3_mesure": mp.nstr(R(r, mp.mpf('1e-3'))*r**2 - 1, 8),
                "ecart_relatif_e_1e-3_predit": mp.nstr(mp.mpf(5)/4*(1 - r**2)*mp.mpf('1e-6'), 8)}
e, rho = S.symbols('e rho', positive=True)
V = (1 + 2*e)**S.Rational(-3, 2) - (1 + e)**(-3)
G = (1 + e)**(-3) * ((1 - rho**2*e**2/(1 + e)**2)**S.Rational(-3, 2) - 1)
out["serie_symbolique_rho2_R"] = str(S.simplify(S.series(rho**2*V/G, e, 0, 3).removeO()))
print(json.dumps(out, indent=1))
