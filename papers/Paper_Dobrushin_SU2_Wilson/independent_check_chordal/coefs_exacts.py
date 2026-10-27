#!/usr/bin/env python3
"""V-CH (independent check of the chordal certificate, 28/09/2026) -- coefficients EXACTS (fractions),
ecrits sans lire ni importer le code de CH (../certificate_chordal).

Objets (kappa = |g|, loi  mu_k  ~ exp(k x1) sur S^3, Haar normalise) :
  Z(k)   = E[exp(k x1)] = sum_k z_{2k} k^{2k},  z_{2k} = E[x1^{2k}]/(2k)!   (moments verifies par sympy ici)
  zeta   = 1/Z,  mu = Z'/Z  (= m1),  e_j(t) = coef de k^j dans exp(k t)/Z
  q_j    = t e_j - sum_a mu_a e_{j-a}
  A_j    = solution polynomiale de  t A - (1-t^2) A'/3 = q_j  (resolution descendante, residu de solvabilite)
  N      = Z^2/3 - (4/3) Z'' Z + Z'^2 ,  Nt = N/k^2
Sortie : pickle de fractions.
"""
import sys, os, pickle, time, hashlib
from fractions import Fraction as F
from math import factorial
import sympy as sp

def moments_sympy(kmax=6):
    """E[x1^{2k}] sur S^3 : densite de x1 = (2/pi) sqrt(1-t^2) (verifiee : normalisation) ; comparaison a C_k/4^k."""
    t = sp.symbols('t')
    dens = 2/sp.pi*sp.sqrt(1-t**2)
    assert sp.simplify(sp.integrate(dens, (t, -1, 1)) - 1) == 0
    for k in range(kmax+1):
        m = sp.integrate(t**(2*k)*dens, (t, -1, 1))
        cat = sp.Rational(factorial(2*k), factorial(k)*factorial(k+1)*4**k)
        assert sp.simplify(m - cat) == 0, (k, m, cat)
    # contre-controle de la densite marginale : sur S^3, x1 = cos(theta), mesure ~ sin^2(theta) dtheta
    th = sp.symbols('th')
    for k in range(4):
        a = sp.integrate(sp.cos(th)**(2*k)*sp.sin(th)**2, (th, 0, sp.pi))/sp.integrate(sp.sin(th)**2, (th, 0, sp.pi))
        cat = sp.Rational(factorial(2*k), factorial(k)*factorial(k+1)*4**k)
        assert sp.simplify(a - cat) == 0
    return True

def main(M):
    t0 = time.time()
    moments_sympy()
    # Z : coefficients en kappa^n (n <= M+4)
    NZ = M + 6
    Z = [F(0)]*(NZ+1)
    for k in range(NZ//2 + 1):
        if 2*k <= NZ:
            Z[2*k] = F(1, 4**k*factorial(k)*factorial(k+1))
    # zeta = 1/Z
    zeta = [F(0)]*(NZ+1); zeta[0] = F(1)
    for n in range(1, NZ+1):
        zeta[n] = -sum(Z[i]*zeta[n-i] for i in range(1, n+1))
    Zp = [ (n+1)*Z[n+1] for n in range(NZ) ] + [F(0)]
    mu = [ sum(Zp[i]*zeta[n-i] for i in range(n+1)) for n in range(NZ+1) ]
    # e_j(t) : liste de coefficients en t (degre j)
    e = []
    for j in range(M+2):
        e.append([ zeta[j-b]/factorial(b) for b in range(j+1) ])
    # q_j = t e_j - sum_{a>=1} mu_a e_{j-a}  (mu_0 = 0)
    assert mu[0] == 0
    A, res = [], []
    for j in range(M+1):
        q = [F(0)]*(j+2)
        for i, c in enumerate(e[j]): q[i+1] += c
        for a in range(1, j+1):
            if mu[a] == 0: continue
            for i, c in enumerate(e[j-a]): q[i] -= mu[a]*c
        # L[t^n] = (1+n/3) t^{n+1} - (n/3) t^{n-1}
        a_ = [F(0)]*(j+3)
        for n in range(j, -1, -1):
            a_[n] = (q[n+1] + a_[n+2]*F(n+2, 3)) / (1 + F(n, 3))
        r = q[0] + a_[1]/3          # coefficient t^0 : -(1/3) a_1 = q_0  <=> residu nul
        res.append(r)
        A.append(a_[:j+1])
        # verification directe L[A_j] == q_j
        LA = [F(0)]*(j+2)
        for n, c in enumerate(a_[:j+1]):
            LA[n+1] += c*(1+F(n, 3))
            if n >= 1: LA[n-1] -= c*F(n, 3)
        assert all(LA[i] == q[i] for i in range(j+2)), j
    # N
    Zpp = [ (n+2)*(n+1)*Z[n+2] for n in range(NZ-1) ] + [F(0), F(0)]
    def mul(a, b, n):
        return [ sum(a[i]*b[k-i] for i in range(k+1)) for k in range(n+1) ]
    Nn = M + 2
    ZZ, ZppZ, ZpZp = mul(Z, Z, Nn), mul(Zpp, Z, Nn), mul(Zp, Zp, Nn)
    N = [ ZZ[k]/3 - F(4, 3)*ZppZ[k] + ZpZp[k] for k in range(Nn+1) ]
    assert N[0] == 0 and N[1] == 0
    Nt = N[2:]
    out = dict(M=M, Z=Z, zeta=zeta, mu=mu, e=e[:M+1], A=A, res=res, Nt=Nt)
    print(f"M={M}  residus de solvabilite nuls pour j<=M : {all(r == 0 for r in res)}")
    print(f"A0={A[0]} A1={A[1]} A2={A[2]}")
    print(f"Nt0 = {Nt[0]} (attendu 1/48),  Nt impairs nuls : {all(Nt[k]==0 for k in range(1,len(Nt),2))}")
    print(f"max_n |zeta_n| 2^n (n<={NZ}) = {float(max(abs(zeta[n])*2**n for n in range(NZ+1)))}")
    print(f"max_n |mu_n| 2^n = {float(max(abs(mu[n])*2**n for n in range(NZ+1)))}  (borne prouvee e-2 = 0.71828)")
    os.makedirs(os.path.join(os.path.dirname(os.path.abspath(__file__)), "out"), exist_ok=True)
    fn = os.path.join(os.path.dirname(os.path.abspath(__file__)), "out", f"coefs_M{M}.pkl")
    with open(fn, 'wb') as f: pickle.dump(out, f)
    print("ecrit", fn, "sha256", hashlib.sha256(open(fn,'rb').read()).hexdigest()[:16], f"{time.time()-t0:.1f}s")

if __name__ == "__main__":
    main(int(sys.argv[1]) if len(sys.argv) > 1 else 100)
