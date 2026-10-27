#!/usr/bin/env python3
"""V-CH [numerical] : borne de Beckmann complete (1/2pi^2) int_B |V| par Monte-Carlo (numpy), champ construit avec
MES coefficients exacts (coefs_M100.pkl) ; + contre-verifications ponctuelles div V = 0 et V.x = w sur S^3.
Comparaison aux LP de ../calc/lp2d_m14.log (kappa = 4/3 : 0.20887 / 0.22145 / 0.23324 pour alpha = 0, pi/4, pi/2)."""
import pickle, numpy as np
d = pickle.load(open(__import__('os').path.join(__import__('os').path.dirname(__import__('os').path.abspath(__file__)), 'out', 'coefs_M100.pkl'), 'rb'))
D = 80
k = 4/3
cA = np.zeros(D+1); cE = np.zeros(D+1)
for j in range(D+1):
    for i, c in enumerate(d['A'][j]): cA[i] += float(c)*k**j
    for i, c in enumerate(d['e'][j]): cE[i] += float(c)*k**j
A = np.polynomial.Polynomial(cA); Ap = A.deriv(); E = np.polynomial.Polynomial(cE)
Z = sum(float(c)*k**n for n, c in enumerate(d['Z']))
m1 = sum(float(c)*k**n for n, c in enumerate(d['mu']))
t = np.linspace(-1, 1, 7)
print("controle E(t) vs exp(kt)/Z :", np.max(np.abs(E(t) - np.exp(k*t)/Z)))
print("controle ODE t A - (1-t^2)A'/3 - (t-m1)E :", np.max(np.abs(t*A(t) - (1-t**2)*Ap(t)/3 - (t-m1)*E(t))))
rng = np.random.default_rng(20260928)
n = 4_000_000
y = rng.normal(size=(n, 4)); y /= np.linalg.norm(y, axis=1)[:, None]; y *= rng.random(n)[:, None]**0.25   # uniforme dans B^4
y1 = y[:, 0]; z = y[:, 1:]
Ex2 = (1 - sum(float(c)*k**n_*n_*(n_-1) for n_, c in enumerate(d['Z']) if n_ >= 2)/Z/k**0 * 1) / 3
# E x1^2 = Z''/Z
Zpp = sum(float(c)*n_*(n_-1)*k**(n_-2) for n_, c in enumerate(d['Z']) if n_ >= 2)
Ex2 = (1 - Zpp/Z)/3
for al, lp in ((0.0, 0.20887), (np.pi/4, 0.22145), (np.pi/2, 0.23324)):
    ca, sa = np.cos(al), np.sin(al)
    V = np.zeros_like(y)
    V[:, 0] = ca*A(y1)
    V[:, 1:] = -ca*(Ap(y1)/3)[:, None]*z
    V[:, 1] += sa*E(y1)
    nv = np.linalg.norm(V, axis=1)
    B = 0.25*nv.mean(); err = 0.25*nv.std()/np.sqrt(n)
    print(f"alpha={al:.4f}  Beckmann B = {B:.5f} +- {err:.5f}   LP(calc) = {lp}   E x2^2 = {Ex2:.5f}")
# flux sur S^3
x = rng.normal(size=(200000, 4)); x /= np.linalg.norm(x, axis=1)[:, None]
for al in (0.3, 1.1):
    ca, sa = np.cos(al), np.sin(al)
    V = np.zeros_like(x); V[:, 0] = ca*A(x[:, 0]); V[:, 1:] = -ca*(Ap(x[:, 0])/3)[:, None]*x[:, 1:]; V[:, 1] += sa*E(x[:, 0])
    u = ca*x[:, 0] + sa*x[:, 1]
    w = (u - ca*m1)*np.exp(k*x[:, 0])/Z
    print(f"flux alpha={al}: max|V.x - w| = {np.max(np.abs((V*x).sum(1) - w)):.2e}")
