#!/usr/bin/env python3
"""b7_constantes.py — constantes RIGOUREUSES de la borne inclinée à partir des certificats cert_incline (m, a/b = e^λ, P, Hmin, Hmax).
Borne (volume infini, tranches = Z^3 ; sur un tore pair L >= 2R : facteur 2 de plus par couche) :
   |<W_{RxT}>| <= C^T exp(-σ R T),  θ = J P/2^30 < 1 (rationnel),  σ = λ − log θ,  λ = log(a/b),
   C = K0/(1 − θ²),  K0 = max(1, r̄(1)(a/b + b/a + 4)·2^30/P)^m · Hmax/Hmin   (Ã1 <= 1/2 absorbe le 2 par couche).
Arithmétique : rationnels exacts (fractions) pour θ, K0, C ; boules arb (python-flint) pour les logarithmes ; garde : deux
précisions (prec 128 et 256) doivent donner des boules qui se recoupent ; ctx.cap n'intervient pas (aucune série tronquée)
mais on vérifie qu'il est inchangé (valeur 10 par défaut) et que le résultat ne dépend pas de cap (calcul refait à cap = 40).
Usage : b7_constantes.py [dossier des certificats cert_J*_a*_b*.json] [dossier des fichiers de poids] (défauts : data, data).
Sortie : JSON avec, pour chaque certificat, θ, σ_inf (borne inférieure certifiée), C_sup, R_min_sup = log C / σ.
"""
import sys, json, glob, re
from fractions import Fraction as F
from flint import arb, ctx, fmpq
def poids(Jtag):
    t = open(f'{POIDS}/poids_m11_J{Jtag}_100000.txt').read().split()
    Q = int(t[0]); n = int(t[1]); return Q, [int(x) for x in t[2:2+n]]
def calcule(c, Jtag, prec):
    ctx.prec = prec
    m, a, b, P, Hmin, Hmax = c['m'], c['a'], c['b'], c['P'], c['Hmin'], c['Hmax']
    Q, p = poids(Jtag); assert Q == 2**40
    J = F(int(Jtag), 100000); rho = F(P, 2**30); theta = J * rho
    if theta >= 1: return None
    r1 = F(p[0], Q); ratio = r1 * (F(a, b) + F(b, a) + 4) / rho
    K0 = max(F(1), ratio)**m * F(Hmax, Hmin)
    C = K0 / (1 - theta**2); C_tore = 2 * C
    lam = arb(fmpq(a, b)).log(); lth = arb(fmpq(theta.numerator, theta.denominator)).log()
    sigma = lam - lth
    lC = arb(fmpq(C.numerator, C.denominator)).log()
    Rmin = lC / sigma
    return dict(theta=float(theta), theta_lt_1=theta < 1, lam=lam, sigma=sigma, C=C, lC=lC, Rmin=Rmin,
                Rmin_tore=(arb(fmpq(C_tore.numerator, C_tore.denominator)).log()) / sigma, K0=float(K0))
res = []
DOSSIER = sys.argv[1] if len(sys.argv) > 1 else 'data'
POIDS = sys.argv[2] if len(sys.argv) > 2 else DOSSIER
for f in sorted(glob.glob(DOSSIER + '/cert_J*_a*_b*.json')):
    c = json.load(open(f))
    if c['violations'] != 0: continue
    Jtag = re.search(r'cert_J(\d+)_', f).group(1)
    r128 = calcule(c, Jtag, 128); r256 = calcule(c, Jtag, 256)
    if r128 is None:
        res.append(dict(fichier=f.split('/')[-1], beta=2*int(Jtag)/100000, theta_ge_1=True)); continue
    garde = r128['sigma'].overlaps(r256['sigma']) and r128['Rmin'].overlaps(r256['Rmin'])
    old = ctx.cap; ctx.cap = 40; r40 = calcule(c, Jtag, 256); ctx.cap = old
    garde_cap = r40['sigma'].overlaps(r256['sigma'])
    s = r256['sigma']; R = r256['Rmin']
    res.append(dict(fichier=f.split('/')[-1], beta=2*int(Jtag)/100000, m=c['m'], e_lambda=f"{c['a']}/{c['b']}",
                    lam=float(r256['lam'].mid()), theta=r256['theta'],
                    sigma_inf=float(s.lower()), C_sup=float(r256['C']) * (1 + 1e-15), K0=r256['K0'],
                    Rmin_sup=float(R.upper()), Rmin_tore_sup=float(r256['Rmin_tore'].upper()),
                    garde_precision=bool(garde), garde_cap=bool(garde_cap)))
print(json.dumps(res, indent=1, ensure_ascii=False))
