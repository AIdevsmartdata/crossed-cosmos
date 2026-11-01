#!/usr/bin/env python3
"""serie_identite_exacte.py -- verification EXACTE (fractions, aucun flottant, aucun intervalle) de l'identite
        Xi(kappa) + 3 Delta(kappa) + S(kappa) = 0
comme serie formelle en kappa, ordre par ordre, jusqu'a kappa^J.  [calcul exact : demontre l'identite aux J premiers ordres ; ne la demontre pas pour tout kappa
(la preuve analytique est dans RAPPORT §2) mais attrape toute erreur d'algebre ou de convention].

Objets (series en kappa a coefficients POLYNOMES en t, rationnels exacts) :
  Zb = sum kappa^{2k}/(4^k k!(k+1)!),  zeta = 1/Zb,  m1 = Zb'/Zb,  E(t) = e^{kappa t}/Zb,  1/E = Zb e^{-kappa t},
  A_j : solution polynomiale de L[A_j] = q_j (q = (t - m1) E), u = A/E, u' = du/dt, w = t u - t + m1,
  <g> = (2/pi) int g R E dt  avec  (2/pi) int t^{2b} R dt = Catalan_b/4^b  (exact).
  Xi = <R^2 u^2> + (3/5)<w^2> - 3 m1/kappa ;  S = (1/15)<R^4 (4u'^2 + 2 kappa u u' + kappa^2 u^2)> ;  Delta = m1^2 + 4 m1/kappa - 1.
Verdict calcule : tous les coefficients de Xi + 3 Delta + S valent EXACTEMENT 0 jusqu'a l'ordre J ; et on affiche les premiers coefficients de Xi, Delta, S.
"""
import sys, json, hashlib
from fractions import Fraction as F
from math import factorial

J = int(sys.argv[1]) if len(sys.argv) > 1 else 30
out_path = sys.argv[2] if len(sys.argv) > 2 else None
M = J + 6

def smul_scal(a, b, n):                     # produit de series scalaires
    return [sum(a[i] * b[k - i] for i in range(k + 1)) for k in range(n + 1)]

Z = [F(0)] * (M + 2)
for k in range(0, (M + 2) // 2 + 1):
    if 2 * k <= M + 1:
        Z[2 * k] = F(1, 4 ** k * factorial(k) * factorial(k + 1))
zeta = [F(0)] * (M + 2); zeta[0] = F(1)
for n in range(1, M + 2):
    zeta[n] = -sum(Z[i] * zeta[n - i] for i in range(1, n + 1))
Zp = [(n + 1) * Z[n + 1] for n in range(M + 1)]
mu = smul_scal(Zp, zeta[:M + 1], M)         # m1 = sum mu_a kappa^a  (mu_0 = 0)
assert mu[0] == 0

# polynomes en t : listes de Fractions
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
def ptimes_t(p): return [F(0)] + list(p)

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
    assert q[0] + a_[1] / 3 == 0, ("residu de solvabilite non nul", j)
    A.append(a_[:j + 1])

def smul(P, Q, n):                           # produit de series a coefficients polynomiaux
    out = []
    for j in range(n + 1):
        acc = [F(0)]
        for a in range(j + 1):
            acc = padd(acc, pmul(P[a], Q[j - a]))
        out.append(acc)
    return out
def sadd(P, Q, n):
    return [padd(P[j] if j < len(P) else [F(0)], Q[j] if j < len(Q) else [F(0)]) for j in range(n + 1)]
def sscal(P, c): return [pscal(p, c) for p in P]
def sshift(P, s, n):                         # multiplication par kappa^s
    return [([F(0)] if j - s < 0 else P[j - s]) for j in range(n + 1)]

# u = A * Einv
U = smul(A, Einv, J)
Up = [pder(p) for p in U]
# m1 comme serie a coefficients constants
M1 = [[mu[j]] for j in range(J + 1)]
T = [[F(0), F(1)] if j == 0 else [F(0)] for j in range(J + 1)]       # t (kappa^0)
ONE = [[F(1)] if j == 0 else [F(0)] for j in range(J + 1)]
Rsq = [[F(1), F(0), F(-1)]]                                           # R^2 = 1 - t^2 (polynome)
def mulpoly(P, poly, n=J):
    return [pmul(p, poly) for p in P]
# w = t u - t + m1
W = sadd(sadd(smul(T, U, J), sscal(smul(T, ONE, J), F(-1)), J), M1, J)
# moyennes <g> = (2/pi) int g R E dt : g serie a coefficients polynomiaux ; poids E serie
def moyenne(G):
    GE = smul(G, E, J)                       # serie en kappa, coefficients polynomes en t
    res = []
    for j in range(J + 1):
        s = F(0)
        for n, c in enumerate(GE[j]):
            if n % 2 == 0:
                b = n // 2
                s += c * F(factorial(2 * b), 4 ** b * factorial(b) * factorial(b + 1))
        res.append(s)
    return res

R2U2 = mulpoly(smul(U, U, J), Rsq[0])
W2 = smul(W, W, J)
R4 = pmul(Rsq[0], Rsq[0])
UU = smul(U, U, J); UUp = smul(U, Up, J); UpUp = smul(Up, Up, J)
brk = sadd(sadd(sscal(UpUp, F(4)), sscal(sshift(UUp, 1, J), F(2)), J), sshift(UU, 2, J), J)    # 4u'^2 + 2 kappa u u' + kappa^2 u^2
Sser = [x / 15 for x in moyenne(mulpoly(brk, R4))]
Ser_P1 = moyenne(R2U2)
Ser_W2 = moyenne(W2)
# 3 m1/kappa : serie  3 mu_{a+1}
P0 = [3 * mu[j + 1] for j in range(J)] + [None]
Xi = [Ser_P1[j] + F(3, 5) * Ser_W2[j] - (P0[j] if P0[j] is not None else F(0)) for j in range(J + 1)]
# Delta = m1^2 + 4 m1/kappa - 1
m1sq = smul_scal(mu[:J + 1], mu[:J + 1], J)
Delta = [m1sq[j] + 4 * mu[j + 1] - (1 if j == 0 else 0) for j in range(J)] + [None]
reste = []
ok = True
Jv = J - 1                                   # P0 et Delta connus jusqu'a l'ordre J-1
for j in range(Jv + 1):
    r = Xi[j] + 3 * Delta[j] + Sser[j]
    reste.append(r)
    ok = ok and (r == 0)
print(f"ordre jusqu'a kappa^{Jv} : Xi + 3 Delta + S == 0 EXACTEMENT (rationnels) : {ok}")
for j in range(0, min(Jv, 12) + 1, 2):
    print(f"  kappa^{j:2d} : Xi = {str(Xi[j]):>28s}   Delta = {str(Delta[j]):>22s}   S = {str(Sser[j]):>28s}   ({float(Xi[j]):+.6e}, {float(Delta[j]):+.6e}, {float(Sser[j]):+.6e})")
print(f"  coefficients impairs nuls : {all(Xi[j] == 0 and Delta[j] == 0 and Sser[j] == 0 for j in range(1, Jv + 1, 2))}")
signes_S = all(Sser[j] >= 0 for j in range(0, Jv + 1, 2)) if False else None
if out_path:
    json.dump(dict(script_sha256=hashlib.sha256(open(__file__, 'rb').read()).hexdigest(), ordre=Jv, identite_exacte=bool(ok),
                   Xi_premiers=[str(x) for x in Xi[:8]], Delta_premiers=[str(x) for x in Delta[:8]], S_premiers=[str(x) for x in Sser[:8]]), open(out_path, 'w'), indent=1)
sys.exit(0 if ok else 1)
