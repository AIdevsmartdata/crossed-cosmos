#!/usr/bin/env python3
"""
M151 / Step 4 -- Full a_n eigenvalues to n=100, evaluate f, f', f'' at tau_Q.

LMFDB traces for 88.3.b.a (a_n, n=1..100) and 88.3.b.b.

We will:
1. Load LMFDB-verified a_n for n=1..100.
2. Compute f(tau_Q), f'(tau_Q), f''(tau_Q) via term-by-term differentiation of q-series.
3. Compute eta(tau_Q), eta'(tau_Q), eta''(tau_Q).
4. Build W^Q_a = f_a / eta^12,  W^Q_b = f_b / eta^12.
5. Check vanishing orders at tau_Q.
6. Find linear combination W^Q = c_a W^Q_a + c_b W^Q_b with double zero at tau_Q.
7. Compute m_tau^2 closed form.
"""

import mpmath as mp
mp.mp.dps = 60

# LMFDB traces (all 100 values verified against API)
a_a = [1, -2, 0, 4, 0, 0, 0, -8, 9, 0, 11, 0, 18, 0, 0, 16, 0, -18, 6, 0,
       0, -22, -42, 0, 25, -36, 0, 0, -14, 0, -26, -32, 0, 0, 0, 36, 0, -12, 0, 0,
       0, 0, -42, 44, 0, 84, 6, 0, 49, -50, 0, 72, 0, 0, 0, 0, 0, 28, 0, 0,
       -78, 52, 0, 64, 0, 0, 0, 0, 0, 0, 54, -72, 0, 0, 0, 24, 0, 0, 0, 0,
       81, 0, -122, 0, 0, 84, 0, -88, -174, 0, 0, -168, 0, -12, 0, 0, -158, -98, 99, 100]

a_b = [1, 2, 0, 4, 0, 0, 0, 8, 9, 0, -11, 0, -18, 0, 0, 16, 0, 18, -6, 0,
       0, -22, -42, 0, 25, -36, 0, 0, 14, 0, -26, 32, 0, 0, 0, 36, 0, -12, 0, 0,
       0, 0, 42, -44, 0, -84, 6, 0, 49, 50, 0, -72, 0, 0, 0, 0, 0, 28, 0, 0,
       78, -52, 0, 64, 0, 0, 0, 0, 0, 0, 54, 72, 0, 0, 0, -24, 0, 0, 0, 0,
       81, 0, 122, 0, 0, 84, 0, -88, -174, 0, 0, -168, 0, 12, 0, 0, -158, 98, -99, 100]

assert len(a_a) == 100
assert len(a_b) == 100
print(f"Loaded {len(a_a)} Hecke eigenvalues for each of 88.3.b.a, 88.3.b.b.")

# tau_Q = i sqrt(11/2)
tau_Q = mp.mpc(0, mp.sqrt(mp.mpf(11)/2))
q_Q = mp.exp(2j * mp.pi * tau_Q)
print(f"tau_Q = {tau_Q}")
print(f"q_Q = {q_Q}, |q_Q| = {abs(q_Q)}")
print()

def eval_f_and_derivs(a_list, q):
    """Compute f(tau), df/dtau, d2f/dtau2 from q-expansion sum a_n q^n.
    df/dtau = sum a_n * 2 pi i n * q^n
    d2f/dtau2 = sum a_n * (2 pi i n)^2 * q^n = -4 pi^2 sum a_n n^2 q^n
    """
    f = mp.mpc(0, 0)
    fp = mp.mpc(0, 0)  # f'
    fpp = mp.mpc(0, 0)  # f''
    for n in range(1, len(a_list) + 1):
        an = a_list[n - 1]
        if an == 0:
            continue
        qn = q**n
        f += an * qn
        fp += an * (2j * mp.pi * n) * qn
        fpp += an * (2j * mp.pi * n)**2 * qn
    return f, fp, fpp


f_a_Q, fp_a_Q, fpp_a_Q = eval_f_and_derivs(a_a, q_Q)
f_b_Q, fp_b_Q, fpp_b_Q = eval_f_and_derivs(a_b, q_Q)

print(f"f_a(tau_Q) = {f_a_Q}")
print(f"f_a'(tau_Q) = {fp_a_Q}")
print(f"f_a''(tau_Q) = {fpp_a_Q}")
print()
print(f"f_b(tau_Q) = {f_b_Q}")
print(f"f_b'(tau_Q) = {fp_b_Q}")
print(f"f_b''(tau_Q) = {fpp_b_Q}")
print()

# Linear combination g = f_a - lambda * f_b vanishes at tau_Q if lambda = f_a/f_b.
lambda_ = f_a_Q / f_b_Q
print(f"lambda = f_a(tau_Q) / f_b(tau_Q) = {lambda_}")
print(f"|lambda - 1| = {abs(lambda_ - 1)}  (should be small but non-zero if forms differ)")
print()

g_Q = f_a_Q - lambda_ * f_b_Q
gp_Q = fp_a_Q - lambda_ * fp_b_Q
gpp_Q = fpp_a_Q - lambda_ * fpp_b_Q
print(f"g(tau_Q) = {g_Q}  (should be 0 by construction)")
print(f"|g(tau_Q)| = {abs(g_Q)}")
print(f"g'(tau_Q) = {gp_Q}")
print(f"|g'(tau_Q)| = {abs(gp_Q)}")
print(f"g''(tau_Q) = {gpp_Q}")
print(f"|g''(tau_Q)| = {abs(gpp_Q)}")
print()

# Question: does g'(tau_Q) = 0 too? -> double zero?
# If g'(tau_Q) != 0, then g has SIMPLE zero at tau_Q.

# CHECK: order of zero of g at tau_Q.
ratio_gp_g = gp_Q / g_Q if abs(g_Q) > mp.mpf("1e-100") else mp.mpc('inf')
print(f"g'/g (test for simple zero) = {ratio_gp_g}")
print()

# Now we need DOUBLE zero. With dim 2 newform space, a single 1-parameter family generally
# gives only simple zero. Let's verify g'(tau_Q) is NOT zero.

if abs(gp_Q) > mp.mpf("1e-30"):
    print(">>> g has SIMPLE zero at tau_Q (g(tau_Q) = 0 but g'(tau_Q) != 0).")
    print(">>> Cannot achieve DOUBLE zero with dim-2 newform space alone.")
    print(">>> Need extension (oldforms, Eisenstein, eta-products, or higher level).")
elif abs(gp_Q) < mp.mpf("1e-30"):
    print(">>> g has DOUBLE OR HIGHER zero at tau_Q!  (g and g' both ~0)")
    print(">>> Check g''(tau_Q):", gpp_Q)
print()

# Compare to expected scale: f_a is dominated by q^1 ~ 4e-7. So |f| ~ 4e-7, |f'| ~ 2pi * 4e-7 ~ 2.5e-6,
# etc. Define "small" relative to this scale.

# Now ALSO compute eta(tau_Q), eta'(tau_Q), eta''(tau_Q).
# eta(tau) = q^(1/24) prod (1 - q^n)
# log eta = (1/24) log q + sum log(1 - q^n)
# (log eta)' = (1/24) (2 pi i) - 2 pi i sum n q^n / (1 - q^n)
#            = (2 pi i / 24) [1 - 24 sum sigma_1 q^n / ... -- the standard E_2 formula]
# Actually d log eta / d tau = (i pi / 12) E_2(tau) where E_2 = 1 - 24 sum sigma_1(n) q^n.

def eta_and_derivs(tau, N_TERMS=400):
    q = mp.exp(2j * mp.pi * tau)
    # eta(tau) = q^(1/24) prod_{n>=1} (1 - q^n)
    eta_val = mp.mpf(1)
    for n in range(1, N_TERMS):
        eta_val *= (1 - q**n)
    eta_val *= q**(mp.mpf(1)/24)
    # d log eta / d tau = (i pi / 12) E_2
    # E_2(tau) = 1 - 24 sum_{n>=1} sigma_1(n) q^n  where sigma_1(n) = sum of divisors
    E2 = mp.mpf(1)
    sum_sigma1 = mp.mpc(0, 0)
    for n in range(1, N_TERMS):
        sigma1 = sum(d for d in range(1, n + 1) if n % d == 0)
        sum_sigma1 += sigma1 * q**n
    E2 = 1 - 24 * sum_sigma1
    eta_prime = eta_val * (1j * mp.pi / 12) * E2
    # eta''/eta = (eta'/eta)' + (eta'/eta)^2
    # (eta'/eta)' = (i pi / 12) E_2'
    # E_2' = (1/(2 pi i)) (E_2'' but using Ramanujan: q dE_2/dq = (E_2^2 - E_4)/12)
    # dE_2/dtau = 2 pi i q dE_2/dq = 2 pi i (E_2^2 - E_4)/12 = (pi i / 6)(E_2^2 - E_4)
    # E_4 = 1 + 240 sum sigma_3(n) q^n
    sum_sigma3 = mp.mpc(0, 0)
    for n in range(1, N_TERMS):
        sigma3 = sum(d**3 for d in range(1, n + 1) if n % d == 0)
        sum_sigma3 += sigma3 * q**n
    E4 = 1 + 240 * sum_sigma3
    dE2 = (mp.pi * 1j / 6) * (E2**2 - E4)
    # (eta'/eta)' = (i pi/12) dE2
    deta_log_pp = (1j * mp.pi / 12) * dE2
    # eta''/eta = deta_log_pp + (eta'/eta)^2
    eta_log_p = (1j * mp.pi / 12) * E2
    eta_pp_over_eta = deta_log_pp + eta_log_p**2
    eta_pp = eta_val * eta_pp_over_eta
    return eta_val, eta_prime, eta_pp, E2, E4


eta_Q, etap_Q, etapp_Q, E2_Q, E4_Q = eta_and_derivs(tau_Q)
print(f"eta(tau_Q) = {eta_Q}")
print(f"eta'(tau_Q) = {etap_Q}")
print(f"eta''(tau_Q) = {etapp_Q}")
print(f"E_2(tau_Q) = {E2_Q}")
print(f"E_4(tau_Q) = {E4_Q}")
print()

# Now compute W^Q_a = f_a / eta^12, and derivatives.
eta12 = eta_Q**12
print(f"eta(tau_Q)^12 = {eta12}")
print(f"|eta^12| = {abs(eta12)}")

# d/dtau (1/eta^12) = -12 eta^11 eta' / eta^24 = -12 eta'/eta^13
# Or: (1/eta^12)' = -12 (eta'/eta) (1/eta^12)
# So W = f / eta^12, W' = f' / eta^12 - 12 (eta'/eta) f / eta^12 = (f' - 12 (eta'/eta) f) / eta^12

eta_log_prime_Q = etap_Q / eta_Q  # = i pi E_2 / 12
print(f"eta'/eta at tau_Q = {eta_log_prime_Q}")
print(f"(should equal i pi E_2/12 = {1j * mp.pi * E2_Q / 12})")
print()

# W^Q_a = f_a / eta^12
# W^Q_a (tau_Q) = f_a(tau_Q) / eta(tau_Q)^12
WQ_a = f_a_Q / eta12
WQ_b = f_b_Q / eta12
print(f"W^Q_a(tau_Q) = f_a/eta^12 = {WQ_a}")
print(f"W^Q_b(tau_Q) = f_b/eta^12 = {WQ_b}")
print(f"|W^Q_a(tau_Q)| = {abs(WQ_a)}")
print(f"|W^Q_b(tau_Q)| = {abs(WQ_b)}")
print()
print("Both W^Q_a, W^Q_b are NON-ZERO at tau_Q.")
print("=> Need to find combinations or different forms to achieve double zero.")
