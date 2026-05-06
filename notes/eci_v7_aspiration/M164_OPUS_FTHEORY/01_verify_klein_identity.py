"""
M164 sub-task: verify Klein identity W^L = (j-1728)/eta^6 = E_6^2 / eta^30
Significance: E_6^2/eta^30 places W^L in standard "modular form / eta power"
form like Curio-Lust 1997 hep-th/9703007 (W' = Theta_{E_8}/eta^12) and
Donagi-Grassi-Witten hep-th/9607091 (W = Theta_{E_8}/eta^8 character form).
"""
from mpmath import mp, mpc, mpf, exp, pi, sqrt
mp.dps = 40


def qq_(tau):
    return exp(2j * pi * tau)


def E4(tau, N=200):
    q = qq_(tau)
    s = mpf(1)
    for n in range(1, N):
        s3 = sum(d**3 for d in range(1, n+1) if n % d == 0)
        s += 240 * s3 * q**n
    return s


def E6(tau, N=200):
    q = qq_(tau)
    s = mpf(1)
    for n in range(1, N):
        s5 = sum(d**5 for d in range(1, n+1) if n % d == 0)
        s -= 504 * s5 * q**n
    return s


def eta(tau, N=400):
    q = qq_(tau)
    s = mpf(1)
    for n in range(1, N):
        s *= (1 - q**n)
    return s * q**(mpf(1)/24)


def Delta(tau, N=400):
    return eta(tau, N)**24


def j_inv(tau, N=200):
    return E4(tau, N)**3 / Delta(tau, N)


tau_i = mpc(0, 1)
tau_test = mpc(0.3, 1.7)

print('=== Klein identity 1728 * Delta = E_4^3 - E_6^2 ===')
for tau in [tau_i, tau_test]:
    lhs = 1728 * Delta(tau)
    rhs = E4(tau)**3 - E6(tau)**2
    print(f'tau = {complex(tau)}')
    print(f'  1728 * Delta = {lhs}')
    print(f'  E_4^3 - E_6^2 = {rhs}')
    if abs(rhs) > 1e-50:
        print(f'  ratio = {lhs/rhs}')
    print()

print('=== j(tau) - 1728 = E_6^2 / Delta ===')
for tau in [tau_i, tau_test]:
    lhs = j_inv(tau) - 1728
    rhs = E6(tau)**2 / Delta(tau)
    print(f'tau = {complex(tau)}')
    print(f'  j - 1728 = {lhs}')
    print(f'  E_6^2/Delta = {rhs}')
    print()

print('=== W^L = (j-1728)/eta^6 = E_6^2 / eta^30 ===')
for tau in [tau_i, tau_test]:
    lhs = (j_inv(tau) - 1728) / eta(tau)**6
    rhs = E6(tau)**2 / eta(tau)**30
    print(f'tau = {complex(tau)}')
    print(f'  (j-1728)/eta^6 = {lhs}')
    print(f'  E_6^2/eta^30   = {rhs}')
    if abs(rhs) > 1e-50:
        print(f'  ratio = {lhs/rhs}')
    print()

# Weight check: E_6 has weight 6, eta has weight 1/2
# E_6^2 weight = 12, eta^30 weight = 15
# E_6^2 / eta^30 weight = 12 - 15 = -3 (Mohseni-Vafa weight kappa = 3 in lepton sector)
print('Weight verification:')
print('  E_6^2 weight: 2 * 6 = 12')
print('  eta^30 weight: 30 * 1/2 = 15')
print('  E_6^2/eta^30 weight: 12 - 15 = -3 (matches M-V kappa=3 with multiplier system)')
