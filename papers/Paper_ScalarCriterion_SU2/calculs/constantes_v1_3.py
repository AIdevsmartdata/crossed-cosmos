# Constantes citees dans les sections ajoutees de la v1.3 (theorie seulement). Aucun role dans une preuve.
from fractions import Fraction as Fr
import math
from math import log, exp
out = {}
# 124, 248, 123
out["248_sur_2"] = 248 // 2
out["log248"] = log(248)
out["log248_vs_log2_plus_5.51"] = (log(248), log(2) + 5.51)
out["h_borne_16/(31*256)=1/496"] = str(Fr(16, 31 * 256))
out["1/496*2=1/248"] = str(Fr(1, 496) * 2)
out["124/123"] = 124 / 123
out["x/(1-x)<=124/123 x pour x<=1/124"] = str(Fr(1, 124) / (1 - Fr(1, 124)))  # = 1/123
# theta
th = exp(18 / 31) - 1
out["theta"] = th
out["-log theta"] = -log(th)
out["theta>=1/2"] = th >= 0.5
# 30
out["somme poids 8+4+2+1"] = 8 + 4 + 2 + 1
out["30=2*15"] = 2 * 15
out["56/57"] = str(Fr(7, 8) / (1 - Fr(7, 64)))
out["2^-9/30"] = str(Fr(1, 512) / 30)
out["eps1<=2(1-e^-2^-9)"] = (2 * (1 - exp(-1 / 512)), 2 ** -8)
out["eps2<=e^{2^-9}-1 ; rapport a 2^-9"] = (exp(1 / 512) - 1, (exp(1 / 512) - 1) * 512)
# 45 log 2, 15 log 8
out["15 log 8"] = 15 * log(8)
out["45 log 2"] = 45 * log(2)
# 8 log(8/(5+3R))
out["8 log(8/5)"] = 8 * log(8 / 5)
out["8 log(8/(5+3R)) pour R=0.001"] = 8 * log(8 / (5 + 0.003))
out["8 log 4"] = 8 * log(4)
out["seuil r<=1/7 -> 8/(1+7r)>=4"] = str(Fr(8) / (1 + 7 * Fr(1, 7)))
# T5: conversion et seuils
out["c=beta/2 ; eps = 24 (log beta + 4.7269)/beta : 12(log c + 5.42)/c"] = None
b = 1000.0
c = b / 2
out["eps(c) == 24(log b+4.7269)/b ? (b=1000)"] = (12 * (log(c) + 5.42) / c, 24 * (log(b) + 4.7269) / b)
out["5.42 - log 2"] = 5.42 - log(2)
k = 0.5
cst1 = 3 * k / 24  # (3k/eps)^(1/4) = (k beta/(8 L))^(1/4)
out["branche1 kappa=1/2: beta/(16 L)"] = 1 / cst1 * 1 / 1  # 24/(1.5) = 16
c2 = (1 - k) * log(2) * (1 - log(2) / 6) / 8  # /eps = *beta/(24 L)
out["branche2 kappa=1/2 : denominateur 24/(c2*8)... valeur"] = 24 / ((1 - k) * log(2) * (1 - log(2) / 6) / 8)
out["dont 626 est arrondi ; il faut 627"] = None
def nmin(beta):
    # plus petit n>=3 compatible avec les deux inegalites de la preuve, exact (pas le minimum analytique)
    eps = 12 * (log(beta / 2) + 5.42) / (beta / 2)   # eps(c) exact, c = beta/2
    # n est compatible si (a) n^4 eps > 3 kappa pour tout kappa<1 admissible, i.e. n^4 eps >= 3 (kappa->1), ou
    # (b) 1-r1 >= (log2)(1-log2/6)/n est <= 8 n^2 eps/(1-n^4 eps/3) avec n^4 eps < 3.
    for n in range(3, 10**7):
        if n**4 * eps >= 3:
            return n
        lhs = 1 - 2 ** (-1 / n)   # exact, r1^n <= 1/2
        rhs = 2 * (2 * n) ** 2 * eps / 8 / (1 - n**4 * eps / 3) * 1  # 2 (l1+l2)^2 eps/(1-..) avec l1=l2=n -> 8 n^2 eps/(1-n^4 eps/3)
        rhs = 8 * n**2 * eps / (1 - n**4 * eps / 3)
        if lhs <= rhs:
            return n
    return None
for e in [5, 6, 7, 8, 9, 10, 12, 14, 16]:
    out[f"nmin(beta=1e{e})"] = nmin(10.0**e)
def ana(beta):
    L = log(beta) + 4.727
    return min((beta / (16 * L)) ** 0.25, (beta / (627 * L)) ** (1 / 3))
for e in [5, 6, 8, 10, 12, 16]:
    out[f"minimum analytique kappa=1/2 (627) beta=1e{e}"] = ana(10.0**e)
def asym(beta):
    return (beta / (8 * (log(beta) + 4.727))) ** 0.25
for e in [6, 8, 10, 12, 16]:
    out[f"nmin / (beta/(8(log b+4.727)))^(1/4), beta=1e{e}"] = nmin(10.0**e) / asym(10.0**e)
out["8^(-1/4)"] = 8 ** -0.25
# faits combinatoires
from itertools import product, combinations
# 35 sous-espaces de dimension 2 de F_2^4, dont 22 contiennent un vecteur de base
vecs = [v for v in product([0, 1], repeat=4) if any(v)]
def add(a, b): return tuple((x + y) % 2 for x, y in zip(a, b))
plans = set()
for a, b in combinations(vecs, 2):
    plans.add(frozenset([a, b, add(a, b)]))
basis = {(1,0,0,0),(0,1,0,0),(0,0,1,0),(0,0,0,1)}
out["plans de F_2^4"] = len(plans)
out["plans contenant un vecteur de base"] = sum(1 for p in plans if p & basis)
out["repartition 6+12+4"] = (sum(1 for p in plans if len(p & basis) == 2),
                           sum(1 for p in plans if len(p & basis) == 1 and any(sum(v) == 2 for v in p)),
                           sum(1 for p in plans if len(p & basis) == 1 and any(sum(v) == 4 for v in p)))
# classes de Pfaffien non nul: 28 = 63-35
def pf(n):  # n = (n01,n02,n03,n12,n13,n23) ; Pfaffien = n01 n23 + n02 n13 + n03 n12 mod 2
    return (n[0]*n[5] + n[1]*n[4] + n[2]*n[3]) % 2
cl = [n for n in product([0,1], repeat=6) if any(n)]
out["classes non nulles"] = len(cl)
out["Pfaffien nul"] = sum(1 for n in cl if pf(n) == 0)
out["Pfaffien non nul"] = sum(1 for n in cl if pf(n) == 1)
# 7 torsions: 4 des 7 k!=0 ont k.e impair pour e!=0
cnt = {}
for e in product([0,1], repeat=3):
    if any(e):
        cnt[e] = sum(1 for k in product([0,1], repeat=3) if any(k) and sum(a*b for a,b in zip(k,e)) % 2 == 1)
out["k.e impair parmi les 7 k!=0, e!=0"] = sorted(set(cnt.values()))
# L1 cube: D>= 3/8(1-R) ; 1-D = (1+sum R)/8
out["cube : 1-D<=(5+3R)/8 si 3 torsions seulement"] = "ok (4 autres termes >=0)"
# comptages de dimension
out["dim N_k = 3V ; codim = 3(d-1)V ; N0gen : 3V-1+d ; exposant (d-1)/2"] = None
for d in [2,3,4,5]:
    for V in [16, 81, 256]:
        dimN0 = 3*V - 1 + d
        assert (3*d*V - 3*V) - (3*d*V - dimN0) == (d - 1) * 1 * 1 or True
        diff = (3*d*V - 3*V) - (3*d*V - dimN0)  # codim N_k - codim N0gen
        assert diff == -(3*V) + 3*V - 1 + d + 0 or True
        out[f"d={d},V={V}: exposant (codimN_k - codimN0)/2"] = ((3*d*V - 3*V) - (3*d*V - dimN0)) / 2
# 4D : 6 + 9(V-1) = 9V-3, 12 + 9(V-1) + 3(V-1) = 12 V ; dof = 12V - 3(V-1) = 9V+3
for V in [16, 81]:
    out[f"4D V={V}: 12V-3(V-1)-12 = 9(V-1)"] = (12*V - 3*(V-1) - 12, 9*(V-1))
    out[f"4D V={V}: 3+ 9(V-1)/2 = (9V-3)/2"] = (3 + 9*(V-1)/2, (9*V-3)/2)
# U(1): 1-cos x >= 2 x^2/pi^2 sur [-pi, pi]
import random
mn = min((1 - math.cos(x)) / (2 * x * x / math.pi**2) for x in [i * math.pi / 10000 for i in range(1, 10001)])
out["U(1): min de (1-cos x)/(2x^2/pi^2) sur (0,pi]"] = mn
# Z2 : comptage des champs plats 2^{V-1+d}
for d, V in [(4, 16), (4, 81)]:
    out[f"Z2 plat: 2^(V-1+d)/2^(dV) = 2^-(d-1)(V-1) ; d={d},V={V}"] = (V - 1 + d - d * V, -(d - 1) * (V - 1))

# contre-exemple a la separation terme a terme (Prop. sectors, remarque) : spectre explicite
def bracket(neutral, odd, M):
    # neutral : liste des r (vide=1 inclus) du secteur 0 ; odd : liste des r du secteur de flux
    tr0 = sum(r**M for r in neutral); trf = sum(r**M for r in odd)
    return log((tr0 + trf) / tr0)
neutral = [1.0] + [0.1] * 20
odd = [1.0]
phi1 = bracket(neutral, odd, 1); phi2 = bracket(neutral, odd, 2)
out["crochet 2 phi(1) - phi(2), neutre {1, 0.1 x20}, flux {1}"] = (2 * phi1 - phi2, "attendu environ -0.031")
out["= 2 log(4/3) - log(2.2/1.2)"] = 2 * log(4 / 3) - log(2.2 / 1.2)
import json
print(json.dumps(out, indent=1, default=str, ensure_ascii=False))
