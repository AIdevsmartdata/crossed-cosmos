"""Check functional equation: L(k-m) / L(m) = ?

For Lambda(s) = N^(s/2) (2 pi)^(-s) Gamma(s) L(s) with FE Lambda(s) = eps Lambda(k-s):
  L(k-s) = eps * N^(s - k/2) * (2 pi)^(k - 2s) * Gamma(s)/Gamma(k-s) * L(s)

Setting s=m, k=5, eps=+1:
  L(5-m)/L(m) = N^(m - 5/2) * (2 pi)^(5-2m) * Gamma(m)/Gamma(5-m).

For 4.5.b.a, N=4:
  m=1: L(4)/L(1) = 4^(-3/2) * (2pi)^3 * 1/6 = (1/8) * 8 pi^3 * 1/6 = pi^3 / 6.
  m=2: L(3)/L(2) = 4^(-1/2) * (2pi)^1 * 1/2 = (1/2) * 2 pi * 1/2 = pi/2.

Verify against computed values.
"""
from mpmath import mp, mpf, pi
mp.dps = 50

L1 = mpf('0.152447133591')
L2 = mpf('0.399105662458')
L3 = mpf('0.626913708592')
L4 = mpf('0.787803000538')

print('--- 4.5.b.a (N=4, k=5, eps=+1) ---')
print('L(4)/L(1) =', L4/L1, '  expected pi^3/6 =', pi**3/6)
print('L(3)/L(2) =', L3/L2, '  expected pi/2  =', pi/2)
print()
print('Ratios match? L(4)/L(1) vs pi^3/6:', abs(L4/L1 - pi**3/6) / (pi**3/6))
print('Ratios match? L(3)/L(2) vs pi/2:', abs(L3/L2 - pi/2) / (pi/2))
print()
# So: L(2) = L(3) * 2/pi, L(1) = L(4) * 6/pi^3
# alpha_1 = L(1) pi^3 / Omega^4 = (6 L(4)) / Omega^4 = 6 alpha_4 -- consistent with Gamma sym
# alpha_2 = L(2) pi^2 / Omega^4 = 2 L(3) pi / Omega^4 = 2 alpha_3
# So alpha_3 = alpha_2 / 2, alpha_4 = alpha_1 / 6 -- GOOD.
