#!/usr/bin/env python3
"""table4_fractions.py — second calcul, ÉCRIT SÉPARÉMENT (relecture à froid de la v1.1, autre instance Claude), des constantes du
Tableau 4 : θ, K0, C en fractions exactes, logarithmes en `decimal` à 60 chiffres (sans Arb ni python-flint). Concordance avec
b7_constantes.py ; R_min sur tore impair (constante 2 K0/(1 − θ)) calculé en plus.  Usage : table4_fractions.py [dossier des poids]"""
from fractions import Fraction as F
from decimal import Decimal as D, getcontext
getcontext().prec = 60
def ln(fr): return (D(fr.numerator)/D(fr.denominator)).ln() if isinstance(fr,F) else D(fr).ln()
def dec(fr): return D(fr.numerator)/D(fr.denominator)
import sys
DATA = sys.argv[1] if len(sys.argv) > 1 else 'data'   # dossier contenant les quatre fichiers de poids (J* copié depuis supplement/data/)
W = {J: f'{DATA}/poids_m11_J{J}_100000.txt' for J in (40674, 40500, 40000, 35294)}
def p1(J):
    t = open(W[J]).read().split(); assert int(t[0])==2**40 and int(t[1])==13; return int(t[2])
rows = [(40674,201,200,2639868799,663255845757),(40674,251,250,2639863512,663389751364),
        (40500,10,9,2648763350,647937564146),(40000,5,4,2678382511,632089802916),(35294,7,4,2898427727,568404757891),
        (40674,1,1,2639854087,663930282414)]
for (J,a,b,P,Hmin) in rows:
    Ji = F(J,100000); th = Ji*F(P,2**30); r1 = F(p1(J),2**40)
    ratio = F(2**30)*r1*(F(a,b)+F(b,a)+4)/P
    K0 = max(F(1),ratio)**11 * F(2**40,Hmin)
    C = K0/(1-th**2); Codd = K0/(1-th)
    sig = ln(F(a,b)) - ln(th)
    Rmin = ln(C)/sig; Rt = ln(2*C)/sig; Rodd = ln(2*Codd)/sig; Rodd_w = ln(Codd)/sig
    print(f"J={J} a/b={a}/{b} P={P}: theta<1={th<1} 1-theta={float(1-th):.10e} ratio={float(ratio):.10f} K0={float(K0):.10f}")
    print(f"   sigma={sig:.12E}  C={dec(C):.10E}  Rmin={Rmin:.6f}  Rmin_torus(2C)={Rt:.6f}  Codd={dec(Codd):.6E} Rmin_odd_torus={Rodd:.4f} Rmin_odd_weak={Rodd_w:.4f}")
# v1.0
J=40674; A=2639854083; Hmin=663930282413
th = F(J,100000)*F(A,2**30); r1=F(p1(J),2**40)
K0 = (6*r1*F(2**30,A))**11*F(2**40,Hmin); C=K0/(1-th)
print("v1.0: theta*=",th, "1-theta*=",float(1-th)," -log theta*=", -ln(th), " K0=",dec(K0), " C*=",dec(C), " Rmin=", ln(C)/(-ln(th)))
print("6 r1/rho' =", float(6*r1*F(2**30,A)))
