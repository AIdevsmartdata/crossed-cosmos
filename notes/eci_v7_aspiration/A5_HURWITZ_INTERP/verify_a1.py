"""Quick check of A1's claim alpha_m for 4.5.b.a Q(i)."""
from mpmath import mp, mpf, pi, gamma, sqrt
mp.dps = 60

Omega_K = gamma(mpf(1)/4)**2 / (2 * sqrt(2 * pi))
L1 = mpf('0.152447133591')
L2 = mpf('0.399105662458')
L3 = mpf('0.626913708592')
L4 = mpf('0.787803000538')

print('Omega_K =', Omega_K)
print('Omega_K^4 =', Omega_K**4)
print()
print('alpha_1 = L(1) * pi^3 / Omega_K^4 =', L1 * pi**3 / Omega_K**4)
print('  expected 1/10 = 0.1')
print('alpha_2 = L(2) * pi^2 / Omega_K^4 =', L2 * pi**2 / Omega_K**4)
print('  expected 1/12 ~ 0.0833')
print('alpha_3 = L(3) * pi^1 / Omega_K^4 =', L3 * pi / Omega_K**4)
print('  expected 1/24 ~ 0.0417')
print('alpha_4 = L(4) / Omega_K**4 =', L4 / Omega_K**4)
print('  expected 1/60 ~ 0.01667')
