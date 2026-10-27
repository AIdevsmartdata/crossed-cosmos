#!/usr/bin/env python3
"""V-CH (independent check of the chordal certificate) : controles EXACTS (sympy/fractions), independants de CH.
 (a) D_ch(0) = 1/4 : E_sigma[u^2] = 1/4 sur S^3 (coordonnees hyperspheriques, sympy) ; cout du couplage par reflexion.
 (b) E_k[x2^2] = (1 - Z''/Z)/3 : developpement exact, c2 = 1/96 ; positivite des coefficients de 4Z''-Z (symbolique en k).
 (c) Z(4/3) (encadrement mpmath.iv via serie + reste), c = 1/(96 Z(4/3)).
 (d) E_k[x2^2] aux kappa des LP de ../calc/lp2d_m14.log (comparaison numerique).
"""
import sympy as sp
from fractions import Fraction as F
from math import factorial
from mpmath import iv, mp, besseli, mpf
th1, th2, ph = sp.symbols('th1 th2 ph', real=True)
# S^3 : x1 = cos th1, x2 = sin th1 cos th2, x3 = sin th1 sin th2 cos ph, x4 = sin th1 sin th2 sin ph ; dσ = sin^2 th1 sin th2
jac = sp.sin(th1)**2*sp.sin(th2)
vol = sp.integrate(jac, (th1, 0, sp.pi), (th2, 0, sp.pi), (ph, 0, 2*sp.pi))
x1 = sp.cos(th1); x2 = sp.sin(th1)*sp.cos(th2)
Eu2 = sp.integrate(x2**2*jac, (th1, 0, sp.pi), (th2, 0, sp.pi), (ph, 0, 2*sp.pi))/vol
Eabs = sp.integrate(sp.Abs(sp.cos(th1))*sp.cos(th1)**2*jac, (th1, 0, sp.pi), (th2, 0, sp.pi), (ph, 0, 2*sp.pi))/vol
print("(a) |S^3| =", sp.simplify(vol), " E[u^2] =", sp.simplify(Eu2), " (u = x2 ; par symetrie toute direction)")
# couplage x -> Rx de nu+ = u_+ sigma vers nu- = u_- sigma : cout = int_{u>0} |x-Rx| u dσ = int_{u>0} 2u^2 = E[u^2]
cost = sp.simplify(2*sp.integrate(x1**2*jac, (th1, 0, sp.pi/2), (th2, 0, sp.pi), (ph, 0, 2*sp.pi))/vol)
print("    cout du couplage par reflexion (u = x1) =", cost, " ; valeur de f=u : Cov(u,u) = E u^2 =", sp.simplify(sp.integrate(x1**2*jac,(th1,0,sp.pi),(th2,0,sp.pi),(ph,0,2*sp.pi))/vol))
# (b)
K = 14
z = [F(0)]*(2*K+3)
for k in range(K+2): z[2*k] = F(1, 4**k*factorial(k)*factorial(k+1))
# verif moments par l'integrale S^3 pour k<=3
for k in range(4):
    m = sp.integrate(x1**(2*k)*jac, (th1, 0, sp.pi), (th2, 0, sp.pi), (ph, 0, 2*sp.pi))/vol
    assert sp.simplify(m/sp.factorial(2*k) - sp.Rational(z[2*k].numerator, z[2*k].denominator)) == 0
kk = sp.symbols('k', positive=True, integer=True)
zk = lambda n: 1/(4**n*sp.factorial(n)*sp.factorial(n+1))
coef = sp.simplify(sp.combsimp(4*(2*kk+2)*(2*kk+1)*zk(kk+1)/zk(kk) - 1))
print("(b) [k^{2k}](4Z''-Z) / z_{2k} =", coef, "  (>= 0 pour k >= 0 ; = 1 pour k=1 -> coefficient 1/8)")
n = 2*K
Z = z[:n+1]
Zpp = [(i+2)*(i+1)*z[i+2] for i in range(n+1)]
inv = [F(0)]*(n+1); inv[0] = F(1)
for i in range(1, n+1): inv[i] = -sum(Z[j]*inv[i-j] for j in range(1, i+1))
r = [sum(Zpp[j]*inv[i-j] for j in range(i+1)) for i in range(n+1)]          # Z''/Z = E x1^2
Ex2 = [(F(1) if i == 0 else F(0)) - r[i] for i in range(n+1)]
Ex2 = [c/3 for c in Ex2]
print("    E_k[x2^2] = " + " + ".join(f"({Ex2[i]}) k^{i}" for i in range(0, 11, 2)))
print("    c2 =", -Ex2[2], "=", float(-Ex2[2]), "> 0 :", -Ex2[2] > 0)
# (c)
iv.prec = 128
Kq = iv.mpf(4)/3
s = iv.mpf(0)
for k in range(40): s += iv.mpf(Kq)**(2*k) / (iv.mpf(4)**k*iv.mpf(factorial(k))*iv.mpf(factorial(k+1)))
t40 = (Kq**80/(iv.mpf(4)**40*iv.mpf(factorial(40))*iv.mpf(factorial(41))))*2   # reste <= 2 x premier terme omis (ratio < 1/2)
Zq = s + iv.mpf([0, t40.b])
print("(c) Z(4/3) in", Zq, " ; mpmath 2 I1(k)/k =", 2*besseli(1, mpf(4)/3)/(mpf(4)/3))
c = 1/(96*Zq)
print("    c = 1/(96 Z(4/3)) in", c, " >= 0.0084052 :", c.a >= mpf('0.0084052'))
# (d)
mp.dps = 30
for kap, lp in ((0, 0.2500), (0.5, 0.2474), (1, 0.2402), (mpf(4)/3, 0.2332), (2, 0.2164)):
    kap = mpf(kap)
    if kap == 0: v = mpf(1)/4
    else:
        Zv = 2*besseli(1, kap)/kap
        # Z'' via derivee numerique haute precision
        from mpmath import diff
        Zpp_ = diff(lambda s_: 2*besseli(1, s_)/s_, kap, 2)
        v = (1 - Zpp_/Zv)/3
    print(f"(d) kappa={float(kap):.4f}  E x2^2 = {float(v):.6f}   LP(calc) = {lp}")
