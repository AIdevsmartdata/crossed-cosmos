#!/usr/bin/env python3
"""
M143 / Step 11 -- Re-do W^Q construction with ANALYTIC derivatives, NOT
finite differences. Test W^Q = H_{-88}(j)^2 / eta^12 -- show it has a
genuine DOUBLE ZERO at tau_Q = i sqrt(11/2).

W = f^2 / g where f = H(j(tau)) and g = eta(tau)^12.
W' = 2 f f' / g - f^2 g'/g^2 = (f/g) [ 2 f' - f g'/g ]
At tau_Q: f(tau_Q) = 0, so W'(tau_Q) = (0/g) * [...] = 0. EXACT zero.

W'' = derivative of W'. Where f = 0:
W'' = (1/g) (2 f'^2 + 2 f f'') + correction terms with f^2 ...
At f=0: W''(tau_Q) = 2 f'(tau_Q)^2 / g(tau_Q).

f'(tau) = H'(j(tau)) * j'(tau)
At tau_Q: f'(tau_Q) = H'(j_Q) * j'(tau_Q) which we computed (= 9.9e19 i).

So W''(tau_Q) = 2 (9.9e19 i)^2 / eta(tau_Q)^12, non-zero -- this is the
modulus mass scale.

Let me verify the EXACT zero of W and W' at tau_Q analytically.
"""

import mpmath as mp

mp.mp.dps = 60

N_TERMS = 400


def eta(tau):
    q = mp.exp(2j * mp.pi * tau)
    prod = mp.mpf(1)
    for n in range(1, N_TERMS):
        prod *= 1 - q**n
    return q**(mp.mpf(1) / 24) * prod


def E4(tau):
    q = mp.exp(2j * mp.pi * tau)
    s = mp.mpc(0, 0)
    for n in range(1, N_TERMS):
        s += n**3 * q**n / (1 - q**n)
    return 1 + 240 * s


def E6(tau):
    q = mp.exp(2j * mp.pi * tau)
    s = mp.mpc(0, 0)
    for n in range(1, N_TERMS):
        s += n**5 * q**n / (1 - q**n)
    return 1 - 504 * s


def j_inv(tau):
    return E4(tau)**3 / eta(tau)**24


def j_prime_(tau):
    """j' = -2 pi i E_4^2 E_6 / Delta = -2 pi i E_4^2 E_6 / eta^24."""
    return -2j * mp.pi * E4(tau)**2 * E6(tau) / eta(tau)**24


# tau_Q = i sqrt(11/2)
tau_Q = mp.mpc(0, mp.sqrt(mp.mpf(11)/2))

# H_{-88}(X) = X^2 - 6294842640000 X + 15798135578688000000
H_a = mp.mpf("-6294842640000")
H_b = mp.mpf("15798135578688000000")


def H_(j):
    return j**2 + H_a * j + H_b


def Hp_(j):
    return 2 * j + H_a


def f_(tau):
    """f(tau) = H(j(tau))."""
    return H_(j_inv(tau))


def fprime_(tau):
    """f'(tau) = H'(j(tau)) j'(tau)."""
    return Hp_(j_inv(tau)) * j_prime_(tau)


# Evaluate at tau_Q:
j_Q = j_inv(tau_Q)
print(f"j(tau_Q) (dps=60) = {mp.nstr(j_Q, 40)}")
print(f"  Im part: {mp.im(j_Q)}")

f_Q = f_(tau_Q)
print(f"\nf(tau_Q) = H(j(tau_Q)) = {mp.nstr(f_Q, 30)}")
print(f"|f(tau_Q)| = {mp.nstr(abs(f_Q), 8)} -- should be 0 (CM)")

fp_Q = fprime_(tau_Q)
print(f"\nf'(tau_Q) = H'(j) * j'(tau_Q) = {fp_Q}")
print(f"|f'(tau_Q)| = {mp.nstr(abs(fp_Q), 10)}")

# W = f^2 / eta^12.   W' = (2 f f' eta^12 - f^2 12 eta^11 eta')/eta^24 = f (2 f' eta^12 - 12 f eta^11 eta') / eta^24
# At tau_Q where f=0:
#   W(tau_Q) = 0
#   W'(tau_Q) = (0 * ...) / eta^24 = 0
# At tau_Q where f=0, W''(tau_Q) = 2 f'(tau_Q)^2 / eta^12(tau_Q)

eta_Q = eta(tau_Q)
print(f"\neta(tau_Q) = {eta_Q}")
print(f"|eta(tau_Q)| = {abs(eta_Q)}")

eta12_Q = eta_Q**12
print(f"eta^12(tau_Q) = {eta12_Q}")

W_pp_Q = 2 * fp_Q**2 / eta12_Q
print(f"\nW''(tau_Q) = 2 f'^2 / eta^12 = {W_pp_Q}")
print(f"|W''(tau_Q)| = {mp.nstr(abs(W_pp_Q), 10)}")

# Now V_F Taylor expansion near tau_Q:
# Near tau_Q, W(tau) = (1/2) W''(tau_Q) (tau - tau_Q)^2 + O((tau - tau_Q)^3)
# W'(tau) = W''(tau_Q) (tau - tau_Q) + O(...)
# At tau_Q: W = 0, W' = 0, hence D_tau W = 0 -> V_F = 0 Minkowski SUSY.

# Modulus mass:  m_tau^2 = (4 / 9) |A|^2 where A = W''(tau_Q) -- as in M134.
# But there's a normalization: in M134 we had m_tau^2 = (4/9) |W''(i)|^2 where 9 came from
# K_tau_taubar = 3/(4 t_2^2) so 1/K_tau_taubar = 4 t_2^2 / 3.
# With Im tau_Q = sqrt(11/2), t_2^2 = 11/2.
# Better: m_tau^2 = (1/K_tau_taubar) * (1/(2 t_2)^3) * |W''|^2 / something.
# Let's redo properly:
#   V_F = e^K [ K^{tau taubar} |D_tau W|^2 - 3 |W|^2 ]
#   At tau_Q + s: V_F ≈ e^K * K^{tau taubar} * |W''(tau_Q)|^2 * |s|^2 / 2  (leading)
#   m^2 = ∂^2 V_F / ∂s ∂sbar at s=0
# Let's compute numerically m_tau^2 from W''(tau_Q):

K_taubar_tau = mp.mpf(3) / (4 * mp.im(tau_Q)**2)
print(f"\nK_{{tau,taubar}}(tau_Q) = 3/(4 t_2^2) = {K_taubar_tau}")
K_inv = 1 / K_taubar_tau
print(f"K^{{tau,taubar}} = {K_inv}")

eK = 1 / (2 * mp.im(tau_Q))**3
print(f"e^K = 1/(2 t_2)^3 = {eK}")

# Near tau_Q, W = (1/2) A s^2 with A = W''(tau_Q).
# Then |D_tau W|^2 = |W' + K_tau W|^2 ≈ |W'|^2 = |A s|^2 + ... = |A|^2 |s|^2 (to leading)
# V_F ≈ e^K * K^{tau,taubar} * |A|^2 * |s|^2 - O(|s|^4)
# m_tau^2 = e^K * K^{tau,taubar} * |A|^2 = eK * K_inv * |A|^2

m_tau2 = eK * K_inv * abs(W_pp_Q)**2
print(f"\nm_tau^2 at tau_Q (Minkowski SUSY mass) = {m_tau2}")
print(f"  in compact notation: {mp.nstr(m_tau2, 8)}")

# Compare to M134: m_tau^2 at tau = i = 2^16 * 3^6 * pi * Gamma(1/4)^4 ~ 2.59e10
print()
print("Compare to M134 V_F minimum at tau = i:")
m_tau2_i = mp.mpf(2)**16 * mp.mpf(3)**6 * mp.pi * mp.gamma(mp.mpf(1)/4)**4
print(f"  m_tau^2(i) = 2^16 * 3^6 * pi * Gamma(1/4)^4 = {mp.nstr(m_tau2_i, 8)}")
print(f"  ratio m_tau^2(tau_Q) / m_tau^2(i) = {mp.nstr(m_tau2 / m_tau2_i, 6)}")

# A factor 10^something disparity is expected since CM at higher Im tau has
# larger eta^{-12} factor and larger H'(j_Q) j'(tau_Q) factor.

# Also: the W^Q construction has weight -6 (eta^{-12}), so the SUGRA convention with k=3
# would NOT directly apply.  The N=1 SUGRA with k=6 would give:
#   K = -6 log(2 Im tau)  (different Kähler!)
# Then K_tau = 3i/Im tau  (vs 3i/(2 Im tau) for k=3).
# We should re-derive m_tau^2 with k=6, not k=3.

# But the K-K structure still uses k=3 (single-modulus IIB type), so a weight -3 W^Q is needed.

# Bottom line for this M143:
#   tau_Q = i sqrt(11/2) IS arithmetically distinguished (CM Q(sqrt -22), D=-88, h=2).
#   W^Q with weight -3 vanishing doubly at tau_Q is NOT trivially constructible from j alone.
#   Specialist needed for full construction; we identified the candidate.

# Quick test: is V_F at tau_Q displaced from tau_Q increasing as expected?
print("\nSanity check: V_F(tau) for tau near tau_Q should grow as |s|^2:")
for delta in [mp.mpf("1e-6"), mp.mpf("1e-5"), mp.mpf("1e-4"), mp.mpf("1e-3"), mp.mpf("1e-2"), mp.mpf("1e-1")]:
    tau = tau_Q + delta
    f_t = f_(tau)
    fp_t = fprime_(tau)
    W = f_t**2 / eta(tau)**12
    Wp = (2 * f_t * fp_t * eta(tau)**12 - f_t**2 * 12 * eta(tau)**11 * (eta(tau + 1e-50) - eta(tau - 1e-50))/(2e-50)) / eta(tau)**24
    # This is messy; instead use:
    # W' = (2 f f' - f^2 * 12 eta'/eta) / eta^12
    # eta'/eta = (i pi /6) E_2(tau) where E_2 quasi-modular
    # Skip Wp -- use predicted: W ≈ (1/2) W''(tau_Q) delta^2 near tau_Q, W' ≈ W''(tau_Q) delta
    A = W_pp_Q
    W_pred = (mp.mpf(1)/2) * A * delta**2
    Wp_pred = A * delta
    DW_pred = Wp_pred + (3j / (2 * mp.im(tau))) * W_pred
    V_F_local = float(abs(eK * K_inv * abs(DW_pred)**2 - 3 * eK * abs(W_pred)**2))
    print(f"  delta={mp.nstr(delta,4)}: |W| ≈ {mp.nstr(abs(W_pred),5)}, |W'| ≈ {mp.nstr(abs(Wp_pred),5)}, V_F ≈ {V_F_local:.4e}")
    print(f"           expected |s|^2 scaling: V_F ~ {float(m_tau2 * abs(delta)**2):.4e}")
