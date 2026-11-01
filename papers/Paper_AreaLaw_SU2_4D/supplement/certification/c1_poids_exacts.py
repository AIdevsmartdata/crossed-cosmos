#!/usr/bin/env python3
"""c1_poids_exacts.py — encadrements EXACTS (rationnels) des poids par site Ã_n(J) et des facteurs de pas r̄(n).

Définitions (voir PREUVE.md) :
  c_k = 1/(k!(k+1)!),  M_J(s) = Σ_k c_k (J² s)^k  ( = I_1(2J√s)/(J√s) ),  ρ_J(s) = M_J(s)/M_J(1),
  h_J(λ) = ρ_J((1−λ)²)³  (facteur par site, pire cas des 6 liens, factorisation de Cauchy–Schwarz),
  Ã_n(J) = ∫_0^1 λ^{n−1}(1−λ)/(n−1)! · h_J(λ) dλ.
Avec u = 1−λ :  ∫_0^1 (1−u)^{n−1} u · u^j du /(n−1)! = (j+1)!/(n+j+1)!  (intégrale bêta exacte).
Troncature : M_J(s) = M_K(s) + reste, 0 ≤ reste ≤ τ := c_{K+1} J^{2K+2} / (1 − J²/((K+2)(K+3)))  pour s ∈ [0,1].
  Majorant :  h ≤ ((M_K(u²) + τ)/M_K(1))³ ;  minorant : h ≥ (M_K(u²)/(M_K(1) + τ))³.
Facteurs de pas : r̃(1) = Ã_1, r̃(N) = Ã_N/Ã_{N−1} (N ≥ 2), et r̃(N) ≤ 1/(N+1) (lemme de Tchebychev).
  u_1 = Ã_1^sup ; u_N = min(Ã_N^sup/Ã_{N−1}^inf, 1/(N+1)) (2 ≤ N ≤ Kn) ; u_{Kn+1} = 1/(Kn+2) (borne de queue) ;
  W̄_n = max(u_n, …, u_{Kn+1}) (majorant non croissant), puis p_n = ⌈W̄_n · Q⌉, Q = 2^40.
Usage : c1_poids_exacts.py J_num J_den [Kn] [K_M] [sortie_poids] [sortie_json]
"""
import sys, json
from fractions import Fraction as F
from math import factorial

def poly_mul(a, b):
    r = [F(0)] * (len(a) + len(b) - 1)
    for i, x in enumerate(a):
        if x == 0:
            continue
        for j, y in enumerate(b):
            r[i + j] += x * y
    return r

def encadrements(J, Kn=12, KM=10):
    c = [F(1, factorial(k) * factorial(k + 1)) for k in range(KM + 2)]
    J2 = J * J
    assert J2 < F(1), "J doit être < 1"
    MK1 = sum(c[k] * J2**k for k in range(KM + 1))
    tau = c[KM + 1] * J2**(KM + 1) / (1 - J2 / ((KM + 2) * (KM + 3)))
    # polynôme en u : M_K(u²) = Σ c_k J^{2k} u^{2k}
    P = [F(0)] * (2 * KM + 1)
    for k in range(KM + 1):
        P[2 * k] = c[k] * J2**k
    Pup = P[:]; Pup[0] += tau
    cube_up = poly_mul(poly_mul(Pup, Pup), Pup)
    cube_lo = poly_mul(poly_mul(P, P), P)
    den_up = MK1**3
    den_lo = (MK1 + tau)**3
    def integ(coeffs, n):
        return sum(cf * F(factorial(j + 1), factorial(n + j + 1)) for j, cf in enumerate(coeffs))
    A_sup = {n: integ(cube_up, n) / den_up for n in range(1, Kn + 1)}
    A_inf = {n: integ(cube_lo, n) / den_lo for n in range(1, Kn + 1)}
    return A_sup, A_inf, tau, MK1

def facteurs(J, Kn=12, KM=10):
    A_sup, A_inf, tau, MK1 = encadrements(J, Kn, KM)
    u = {1: A_sup[1]}
    for N in range(2, Kn + 1):
        u[N] = min(A_sup[N] / A_inf[N - 1], F(1, N + 1))
    u[Kn + 1] = F(1, Kn + 2)
    W = {}
    run = F(0)
    for n in range(Kn + 1, 0, -1):
        run = max(run, u[n]); W[n] = run
    return A_sup, A_inf, u, W, tau

if __name__ == "__main__":
    Jn, Jd = int(sys.argv[1]), int(sys.argv[2])
    Kn = int(sys.argv[3]) if len(sys.argv) > 3 else 12
    KM = int(sys.argv[4]) if len(sys.argv) > 4 else 10
    J = F(Jn, Jd)
    A_sup, A_inf, u, W, tau = facteurs(J, Kn, KM)
    Q = 2**40
    p = [-(-W[n].numerator * Q // W[n].denominator) for n in range(1, Kn + 2)]  # plafond exact
    for n in range(1, Kn + 2):
        assert F(p[n - 1], Q) >= W[n]
    # contrôles : monotonie, ordre, cohérence
    assert all(A_inf[n] <= A_sup[n] for n in A_sup)
    assert all(W[n] >= W[n + 1] for n in range(1, Kn + 1))
    out = {"J": f"{Jn}/{Jd}", "J_float": float(J), "beta_W": f"{2*Jn}/{Jd}", "Kn": Kn, "K_M": KM,
           "tau_reste": float(tau),
           "A_inf": {n: float(A_inf[n]) for n in A_inf}, "A_sup": {n: float(A_sup[n]) for n in A_sup},
           "largeur_relative_max": max(float((A_sup[n] - A_inf[n]) / A_inf[n]) for n in A_sup),
           "u": {n: float(u[n]) for n in u}, "W": {n: float(W[n]) for n in W},
           "Q": Q, "p": p,
           "facteur_pas_BS_certifie": float(J * (5 * W[1] + W[2])),
           "comparaison_BS_a_n": {"a1": 0.5, "r2": 1/3}}
    if len(sys.argv) > 5:
        with open(sys.argv[5], "w") as f:
            f.write(f"{Q} {Kn + 1} " + " ".join(str(x) for x in p) + "\n")
    js = json.dumps(out, indent=1, ensure_ascii=False)
    if len(sys.argv) > 6:
        with open(sys.argv[6], "w") as f:
            f.write(js + "\n")
    print(js)
