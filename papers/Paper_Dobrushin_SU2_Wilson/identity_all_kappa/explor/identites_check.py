#!/usr/bin/env python3
"""Verification NUMERIQUE des identites exactes (derivees a la main) liant les moments de u = A/E :
  P0 = E[R^2] = 3 m1/kappa ;  Var = Var x1 = m1/kappa - Delta,  Delta = m1^2 + 4 m1/kappa - 1
  P1 = E[R^2 u^2], T = E[t R^2 u^2], W = E[w^2] (w = t(u-1)+m1), Q1 = E[R^4 u'^2]
  (I1) E[R^2 u] = 3 Var x1
  (I2) Bochner :  9 Var = Q1 + 3 P1 + 2 kappa T
  (I3) W = Q1/9 + 5 kappa T/9      et  W = Var - P1/3 + kappa T/3
  (I4) Xi := P1 + (3/5) W - P0 = (4/5) P1 + (kappa/5) T + (3/5) Var - P0  ;  Xi = E[R^2 (u-1)^2] + (3/5) W - 6 Delta
E[g] = (2/pi) int R E g dt  (loi marginale de x1 sous q_kappa).
"""
import sys, math
import numpy as np
from flint import arb, ctx
sys.path.insert(0, __file__.rsplit('/', 1)[0])
from ratio_scan import champ, evalpoly, evalpoly_d

def moments(kappa, nth=400):
    prec = int(60 + 3.2 * 3 * kappa + 200)
    F = champ(kappa, prec)
    k, Zb, m1, a = F['k'], F['Zb'], F['m1'], F['a']
    x, w = np.polynomial.legendre.leggauss(nth)
    th = (x + 1) * math.pi / 2; wt = w * math.pi / 2
    T = np.cos(th); S = np.sin(th)
    A = np.zeros(nth); Ap = np.zeros(nth); E = np.zeros(nth)
    for i, ti in enumerate(T):
        t = arb(float(ti))
        A[i] = float(evalpoly(a, t).mid()); Ap[i] = float(evalpoly_d(a, t).mid()); E[i] = float(((k * t).exp() / Zb).mid())
    m1f = float(m1.mid())
    R = S
    u = A / E
    up = (Ap - u * kappa * E) / E             # u' = (A' - kappa A)/E
    # expectation under marginal law (2/pi) R E dt ; dt = sin(th) dth
    def Ex(g):
        return 2 / math.pi * np.sum(wt * S * R * E * g)
    d = {}
    d['m1'] = m1f
    d['P0'] = Ex(R ** 2); d['P0_exact'] = 3 * m1f / kappa
    Delta = m1f ** 2 + 4 * m1f / kappa - 1
    Var = m1f / kappa - Delta
    d['Delta'] = Delta; d['Var'] = Var; d['Var_num'] = Ex(T ** 2) - Ex(T) ** 2
    d['I1_lhs'] = Ex(R ** 2 * u); d['I1_rhs'] = 3 * Var
    P1 = Ex(R ** 2 * u ** 2); Tm = Ex(T * R ** 2 * u ** 2); Q1 = Ex(R ** 4 * up ** 2)
    wv = T * (u - 1) + m1f
    W = Ex(wv ** 2)
    d['P1'] = P1; d['T'] = Tm; d['Q1'] = Q1; d['W'] = W
    d['I2_lhs'] = 9 * Var; d['I2_rhs'] = Q1 + 3 * P1 + 2 * kappa * Tm
    d['I3a'] = Q1 / 9 + 5 * kappa * Tm / 9; d['I3b'] = Var - P1 / 3 + kappa * Tm / 3
    Xi = P1 + 0.6 * W - d['P0_exact']
    d['Xi'] = Xi; d['Xi_I4'] = 0.8 * P1 + kappa / 5 * Tm + 0.6 * Var - d['P0_exact']
    d['Xi_I4b'] = Ex(R ** 2 * (u - 1) ** 2) + 0.6 * W - 6 * Delta
    return d

if __name__ == "__main__":
    ks = [float(v) for v in sys.argv[1:]] or [0.5, 1.3333333333, 3, 6, 12]
    for kk in ks:
        d = moments(kk)
        print(f"--- kappa={kk}  m1={d['m1']:.8f}  P0 num/exact = {d['P0']:.8f}/{d['P0_exact']:.8f}  Var num/exact = {d['Var_num']:.8f}/{d['Var']:.8f}")
        print(f"   (I1) E[R^2 u] = {d['I1_lhs']:.8f}  vs 3Var = {d['I1_rhs']:.8f}")
        print(f"   (I2) 9Var = {d['I2_lhs']:.8f}  vs Q1+3P1+2kT = {d['I2_rhs']:.8f}   (P1={d['P1']:.6f} T={d['T']:+.6f} Q1={d['Q1']:.6f})")
        print(f"   (I3) W = {d['W']:.8f}  vs Q1/9+5kT/9 = {d['I3a']:.8f}  vs Var-P1/3+kT/3 = {d['I3b']:.8f}")
        print(f"   (I4) Xi = {d['Xi']:.8f}  vs {d['Xi_I4']:.8f}  vs {d['Xi_I4b']:.8f}")
