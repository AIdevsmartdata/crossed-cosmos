#!/usr/bin/env python3
r"""V2 : controle de la formule gaussienne V_K, Gamma_K(t) (3 couleurs independantes), symbolique + Monte-Carlo,
et forme de K -> V_K/Gamma_K (la borne du Theoreme A est inf_K (1/t) log(V_K/Gamma_K) ; on verifie que la limite
K -> oo vaut (s/c)^2 et on regarde si l'inf est atteint a l'infini).
(Y0, Yt) dans R^3 x R^3, chaque couleur a : (Y0^a, Yt^a) ~ N(0, [[s,c],[c,s]]), couleurs independantes.
f_K(y) = exp(-|y|^2/(2K)).
"""
import json
import numpy as np
import sympy as S

s, c, K = S.symbols('s c K', positive=True)
Sig = S.Matrix([[s, c], [c, s]])
# E exp(-(x^T x)/(2K)) pour x ~ N(0,Sig) en dimension 2 : det(I + Sig/K)^{-1/2}
E2 = (S.eye(2) + Sig / K).det() ** S.Rational(-1, 2)
Ef = (1 + s / K) ** S.Rational(-1, 2)       # une couleur, une variable
Ef2 = (1 + 2 * s / K) ** S.Rational(-1, 2)  # f_K^2 = exp(-y^2/K)
V3 = Ef2 ** 3 - Ef ** 6
G3 = E2 ** 3 - Ef ** 6
V_auteur = (1 + 2 * s / K) ** S.Rational(-3, 2) - (1 + s / K) ** (-3)
G_auteur = (1 + s / K) ** (-3) * ((1 - c ** 2 / (K + s) ** 2) ** S.Rational(-3, 2) - 1)
res = {"V_identique": S.simplify(V3 - V_auteur) == 0,
       "Gamma_identique_numerique": [float((G3 - G_auteur).subs({s: sv, c: cv, K: kv}))
                                      for sv, cv, kv in [(1.1377, 0.1377, 0.7), (1.0, 0.9, 3.0), (2.0, 0.01, 50.0)]]}
eps = S.symbols('epsilon', positive=True)
rho = S.symbols('rho', positive=True)
Vs = S.series(V_auteur.subs({K: s / eps}), eps, 0, 4).removeO()
Gs = S.series(G_auteur.subs({K: s / eps, c: rho * s}), eps, 0, 4).removeO()
res["V_serie"] = str(S.expand(Vs))
res["Gamma_serie"] = str(S.expand(Gs))
res["limite_ratio_K_inf"] = str(S.limit((V_auteur / G_auteur).subs({K: s / eps, c: rho * s}), eps, 0))

# Monte-Carlo
rng = np.random.default_rng(20261111)
sv, cv, kv = 1.1377494917, 0.1377494917, 0.8
n = 4_000_000
L = np.linalg.cholesky(np.array([[sv, cv], [cv, sv]]))
z = rng.standard_normal((n, 3, 2)) @ L.T
Y0, Yt = z[..., 0], z[..., 1]
f0 = np.exp(-(Y0 ** 2).sum(1) / (2 * kv)); ft = np.exp(-(Yt ** 2).sum(1) / (2 * kv))
res["MC"] = {"Var_mc": float(f0.var()), "Var_formule": float(V_auteur.subs({s: sv, K: kv})),
             "Cov_mc": float(np.mean(f0 * ft) - f0.mean() * ft.mean()),
             "Cov_formule": float(G_auteur.subs({s: sv, c: cv, K: kv})),
             "erreur_type_cov": float(np.std(f0 * ft) / np.sqrt(n))}

# forme de K -> ratio, pour plusieurs rho = c/s
def ratio(r, x):  # x = K/s
    e = 1.0 / x
    V = (1 + 2 * e) ** -1.5 - (1 + e) ** -3
    u = (r * e / (1 + e)) ** 2
    G = (1 + e) ** -3 * np.expm1(-1.5 * np.log1p(-u))
    return V / G
xs = np.logspace(-3, 6, 2001)
forme = {}
for r in [0.9, 0.5, 0.121, 0.0161, 1e-3, 1e-6]:
    R = np.array([ratio(r, x) for x in xs])
    forme[str(r)] = {"min_sur_grille": float(R.min()), "x_argmin": float(xs[R.argmin()]),
                     "limite_1_sur_rho2": 1 / r ** 2, "monotone_decroissante": bool(np.all(np.diff(R) <= 1e-9 * R[1:]))}
res["forme_en_K"] = forme
print(json.dumps(res, indent=1))
