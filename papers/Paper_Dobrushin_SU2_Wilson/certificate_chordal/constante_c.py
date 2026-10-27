#!/usr/bin/env python3
# constante_c.py -- CH (chordal certificate) : 1/4 - E_k[x2^2] = (4Z'' - Z)/(12 Z) >= k^2/(96 Z(k)) >= k^2/(96 Z(4/3)) sur [0, 4/3].
# (4Z'' - Z = sum_k 3k/(k+2) k^{2k}/(4^k k!(k+1)!) : coefficients >= 0, premier terme k^2/8.) Z(4/3) majore par Arb.
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import cert_ch as C
from fractions import Fraction as F
from flint import arb, fmpq
C.fixe_contexte(128, 200)
# verification exacte des coefficients de 4Z'' - Z
ok = True
for k in range(0, 40):
    n = 2 * k
    c = 4 * (n + 1) * (n + 2) * C.zcoef_frac(n + 2) - C.zcoef_frac(n)
    ok &= c == F(3 * k, k + 2) * C.zcoef_frac(n)
print("coefficients 4Z''-Z = 3k/(k+2) z_2k (k < 40) :", ok)
Zmax = C.majZ(arb(fmpq(4, 3)), 0)
c = (1 / (96 * Zmax)).lower()
print("Z(4/3) dans", Zmax.str(20, radius=True), "; c = 1/(96 Z(4/3)) >=", c.str(12, radius=True))
ok &= c > arb("0.0084")
print("D_ch(k) <= 1/4 - 0.0084 k^2 sur [0,4/3] :", ok)
sys.exit(0 if ok else 1)
