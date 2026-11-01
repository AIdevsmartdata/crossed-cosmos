#!/usr/bin/env python3
"""Exploration EXACTE (fractions) : developpement en kappa du critere (*) :
    Xi(kappa) = (2/pi) int_{-1}^{1} R^3 [ (A^2 + R^2 A'^2/15)/E - E ] dt  = kappa^2 * sum_j xi_j kappa^j
(rationnels). Regarde les signes des xi_j (a quoi ressemble la serie ?).
"""
import sys
from fractions import Fraction as F
from math import factorial, gamma, pi

J = int(sys.argv[1]) if len(sys.argv) > 1 else 24

# ---------- series scalaires en kappa (listes de Fraction, longueur J+3)
M = J + 4
Z = [F(0)] * (M + 2)
for k in range(0, (M + 2) // 2 + 1):
    if 2 * k <= M + 1:
        Z[2 * k] = F(1, 4 ** k * factorial(k) * factorial(k + 1))
def mul(a, b, n):
    return [sum(a[i] * b[k - i] for i in range(k + 1)) for k in range(n + 1)]
zeta = [F(0)] * (M + 2); zeta[0] = F(1)
for n in range(1, M + 2):
    zeta[n] = -sum(Z[i] * zeta[n - i] for i in range(1, n + 1))
Zp = [(n + 1) * Z[n + 1] for n in range(M + 1)]
mu = mul(Zp, zeta[:M + 1], M)        # m1 = Z'/Z

# ---------- polynomes en t : dict degre -> Fraction  (liste de coefficients)
def padd(p, q):
    n = max(len(p), len(q)); r = [F(0)] * n
    for i, c in enumerate(p): r[i] += c
    for i, c in enumerate(q): r[i] += c
    return r
def pmul(p, q):
    r = [F(0)] * (len(p) + len(q) - 1)
    for i, a in enumerate(p):
        if a == 0: continue
        for j, b in enumerate(q):
            r[i + j] += a * b
    return r
def pscal(p, c): return [c * a for a in p]
def pder(p): return [i * p[i] for i in range(1, len(p))] or [F(0)]

# E_j(t) = sum_{n+k=j} t^n/n! zeta_k ;  Einv_j(t) = sum_{n+k=j} (-t)^n/n! Z_k ; A_j
E = []; Einv = []
for j in range(J + 1):
    E.append([zeta[j - n] / factorial(n) for n in range(j + 1)])
    Einv.append([(-1) ** n * Z[j - n] / factorial(n) for n in range(j + 1)])
A = []
for j in range(J + 1):
    q = [F(0)] * (j + 2)
    for i, c in enumerate(E[j]): q[i + 1] += c
    for a in range(1, j + 1):
        if mu[a] == 0: continue
        for i, c in enumerate(E[j - a]): q[i] -= mu[a] * c
    a_ = [F(0)] * (j + 3)
    for n in range(j, -1, -1):
        a_[n] = (q[n + 1] + a_[n + 2] * F(n + 2, 3)) / (1 + F(n, 3))
    assert q[0] + a_[1] / 3 == 0, ("residu solvabilite", j)
    A.append(a_[:j + 1])
print("A0, A1, A2 =", A[0], A[1], A[2])

# series produit de series a coefficients polynomiaux : S[j] = sum_{a+b=j} P[a]*Q[b]
def smul(P, Q, n):
    out = []
    for j in range(n + 1):
        acc = [F(0)]
        for a in range(j + 1):
            acc = padd(acc, pmul(P[a], Q[j - a]))
        out.append(acc)
    return out
A2 = smul(A, A, J)
Ap = [pder(a) for a in A]
Ap2 = smul(Ap, Ap, J)
# term1 = (A^2) * Einv ; term2 = R^2 A'^2/15 * Einv ; (1 - t^2) factor included below
T1 = smul(A2, Einv, J)
T2 = smul(Ap2, Einv, J)
# integrand series (without R^3) : G_j(t) = T1_j + (1-t^2) T2_j/15 - E2_j with E_j
G = []
for j in range(J + 1):
    g = padd(T1[j], pscal(pmul([F(1), F(0), F(-1)], T2[j]), F(1, 15)))
    g = padd(g, pscal(E[j], F(-1)))
    G.append(g)
# int_{-1}^1 R^3 t^{2b} dt = B(b+1/2, 5/2) ; (2/pi) * that = rational
from fractions import Fraction
def beta_half(b):
    # (2/pi) * Gamma(b+1/2) Gamma(5/2) / Gamma(b+3)
    # Gamma(b+1/2) = sqrt(pi) (2b)!/(4^b b!) ; Gamma(5/2) = 3 sqrt(pi)/4 ; Gamma(b+3) = (b+2)!
    return F(2) * F(factorial(2 * b), 4 ** b * factorial(b)) * F(3, 4) / factorial(b + 2)
mom = [beta_half(b) for b in range(0, J + 4)]
xi = []
for j in range(J + 1):
    s = F(0)
    for n, c in enumerate(G[j]):
        if n % 2 == 0:
            s += c * mom[n // 2]
    xi.append(s)
print("sanity: Xi_0 =", xi[0], " (attendu 0) ; Xi_1 =", xi[1])
for j in range(J + 1):
    print(f"Xi coef kappa^{j:2d} : {float(xi[j]): .6e}   {xi[j] if j < 6 else ''}")
print("ratio Xi/(kappa^2): premiers termes:", [float(x) for x in xi[2:8]])
