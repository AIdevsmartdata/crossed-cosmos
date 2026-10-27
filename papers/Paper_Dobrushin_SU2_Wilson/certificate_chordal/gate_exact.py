#!/usr/bin/env python3
# gate_exact.py -- CH (chordal certificate), gate G2 : chemin EXACT (fractions) independant d'Arb.
#  (a) series Z, 1/Z, m1, mu, N en rationnels exacts ; N_0 = N_1 = 0, N_2 = 1/48, N impairs = 0 ;
#  (b) A_j par descente EXACTE : residu de solvabilite (equation t^0) == 0 exactement pour tout j <= D ;
#  (c) les boules Arb de cert_ch.py (memes fonctions, cap 200, prec 128) CONTIENNENT les rationnels exacts ;
#  (d) developpement exact de E x2^2 = (1 - Z''/Z)/3 : 1/4 - k^2/96 + ... ; A_1 = 3t/4, E_1 = t.
import sys, os, math
from fractions import Fraction as F
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import cert_ch as C
from flint import arb

D = int(sys.argv[1]) if len(sys.argv) > 1 else 80
L = D + 5


def mul(a, b):
    return [sum(a[i] * b[n - i] for i in range(n + 1)) for n in range(L)]


def inv(a):
    r = [F(0)] * L
    r[0] = 1 / a[0]
    for n in range(1, L):
        r[n] = -sum(a[i] * r[n - i] for i in range(1, n + 1)) / a[0]
    return r


z = [C.zcoef_frac(n) for n in range(L + 2)]
Z = z[:L]
Zp = [(n + 1) * z[n + 1] for n in range(L)]
Zpp = [(n + 1) * (n + 2) * z[n + 2] for n in range(L)]
iz = inv(Z)
m1 = mul(Zp, iz)
mu = mul(m1, iz)
N = [a / 3 - F(4, 3) * b + c for a, b, c in zip(mul(Z, Z), mul(Zpp, Z), mul(Zp, Zp))]
ok = True
print(f"D = {D}, L = {L}")
print(f"(a) N_0 = {N[0]}, N_1 = {N[1]}, N_2 = {N[2]}, N_4 = {N[4]}, impairs nuls : {all(N[n] == 0 for n in range(1, L, 2))}")
ok &= N[0] == 0 and N[1] == 0 and N[2] == F(1, 48) and all(N[n] == 0 for n in range(1, L, 2))

Aex, Eex = [], []
resmax = F(0)
for j in range(D + 1):
    q = [F(0)] * (j + 2)
    e = [F(0)] * (j + 1)
    for n in range(j + 1):
        k = j - n
        q[n + 1] += iz[k] / math.factorial(n)
        q[n] -= mu[k] / math.factorial(n)
        e[n] += iz[k] / math.factorial(n)
    dd = len(q) - 2
    a = [F(0)] * (dd + 3)
    for mm in range(dd + 1, 0, -1):
        a[mm - 1] = (q[mm] + a[mm + 1] * (mm + 1) / 3) * 3 / (mm + 2)
    res = -a[1] / 3 - q[0]
    resmax = max(resmax, abs(res))
    Aex.append(a[:dd + 1])
    Eex.append(e)
print(f"(b) residu de solvabilite exact, max sur j <= {D} : {resmax}")
ok &= resmax == 0
print(f"(d) A_0 = {Aex[0]}, A_1 = {Aex[1]}, E_1 = {Eex[1]}, A_2 = {Aex[2]}")
ok &= Aex[0] == [1] and Aex[1] == [0, F(3, 4)] and Eex[1] == [0, 1]
m2 = mul(Zpp, iz)
Ex2 = [(F(1) if n == 0 else F(0)) / 3 - m2[n] / 3 for n in range(L)]
print("(d) E x2^2 = " + " + ".join(f"({Ex2[n]}) k^{n}" for n in range(0, 9, 2)) + " + ...")
ok &= Ex2[0] == F(1, 4) and Ex2[2] == F(-1, 96)


# (c) contenance des boules Arb
def contient(b, fr):
    mm, ee = b.mid().man_exp()
    rm, re_ = b.rad().man_exp()
    mid = F(int(mm)) * (F(2) ** int(ee))
    rad = F(int(rm)) * (F(2) ** int(re_))
    return abs(mid - fr) <= rad


C.fixe_contexte(128, 200)
sc = C.series_scalaires(D, L)
A, E, Ap, resids = C.polys_t(sc, D)
n_tests = 0
n_ko = 0
for nom, ex in (("iz", iz), ("mu", mu), ("N", N)):
    for n in range(D + 3):
        n_tests += 1
        if not contient(sc[nom][n], ex[n]):
            n_ko += 1
for j in range(D + 1):
    ca = A[j].coeffs()
    ce = E[j].coeffs()
    for i, fr in enumerate(Aex[j]):
        n_tests += 1
        b = ca[i] if i < len(ca) else arb(0)
        if not contient(b, fr):
            n_ko += 1
    for i, fr in enumerate(Eex[j]):
        n_tests += 1
        b = ce[i] if i < len(ce) else arb(0)
        if not contient(b, fr):
            n_ko += 1
print(f"(c) contenance Arb >= exact : {n_tests - n_ko}/{n_tests} ; rayon max A_{D} : "
      f"{max(float(c.rad()) for c in A[D].coeffs()):.2e}")
ok &= n_ko == 0
print("GATE_EXACT", "OK" if ok else "ECHEC")
sys.exit(0 if ok else 1)
