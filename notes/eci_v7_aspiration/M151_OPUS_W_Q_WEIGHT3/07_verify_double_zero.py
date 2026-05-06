#!/usr/bin/env python3
"""
M151 / Step 7 -- VERIFY analytically that W^Q has double zero at tau_Q.

W^Q(tau) = H(tau)^2 * f(tau) / eta(tau)^{12}

where H(tau) = H_{-88}(j(tau)) and f = 88.3.b.a (or any non-vanishing weight-3 form).

Let g(tau) = H(tau)^2.
At tau_Q: H(tau_Q) = 0.  So g(tau_Q) = 0.
H'(tau_Q) := H_{-88}'(j(tau_Q)) * j'(tau_Q) =: alpha (NONZERO at tau_Q since H_{-88} has simple roots).
g'(tau) = 2 H(tau) H'(tau).
g'(tau_Q) = 2 * 0 * alpha = 0.  ✓ DOUBLE ZERO at tau_Q (g vanishes to order 2).

g''(tau) = 2 (H'(tau))^2 + 2 H(tau) H''(tau).
g''(tau_Q) = 2 alpha^2 + 0 = 2 alpha^2 != 0.

Now W^Q = g * f / eta^{12}.  Define D(tau) = f(tau)/eta(tau)^{12}.
W^Q = g * D.
W^Q'(tau) = g'(tau) D(tau) + g(tau) D'(tau).
At tau_Q:
W^Q'(tau_Q) = 0 * D(tau_Q) + 0 * D'(tau_Q) = 0. ✓ DOUBLE ZERO at tau_Q.

W^Q''(tau) = g'' D + 2 g' D' + g D''.
At tau_Q: W^Q''(tau_Q) = g''(tau_Q) * D(tau_Q) + 0 + 0 = 2 alpha^2 * D(tau_Q).
       = 2 (H_{-88}'(j(tau_Q)) j'(tau_Q))^2 * f(tau_Q) / eta(tau_Q)^{12}.

So the structural result is:
  W^Q'(tau_Q) = 0 EXACTLY (analytically).
  W^Q''(tau_Q) = 2 alpha^2 * D(tau_Q) = closed-form expression in
                  H_{-88}'(j(tau_Q)), j'(tau_Q), f(tau_Q), eta(tau_Q).

For VERIFICATION we use higher-order finite differences with adaptive precision.
"""

import mpmath as mp
mp.mp.dps = 80

a_a = [1, -2, 0, 4, 0, 0, 0, -8, 9, 0, 11, 0, 18, 0, 0, 16, 0, -18, 6, 0,
       0, -22, -42, 0, 25, -36, 0, 0, -14, 0, -26, -32, 0, 0, 0, 36, 0, -12, 0, 0,
       0, 0, -42, 44, 0, 84, 6, 0, 49, -50, 0, 72, 0, 0, 0, 0, 0, 28, 0, 0,
       -78, 52, 0, 64, 0, 0, 0, 0, 0, 0, 54, -72, 0, 0, 0, 24, 0, 0, 0, 0,
       81, 0, -122, 0, 0, 84, 0, -88, -174, 0, 0, -168, 0, -12, 0, 0, -158, -98, 99, 100]

H_coef_a = mp.mpf("-6294842640000")
H_coef_b = mp.mpf("15798135578688000000")

tau_Q = mp.mpc(0, mp.sqrt(mp.mpf(11)/2))

N_TERMS = 500


def eta(tau):
    q = mp.exp(2j * mp.pi * tau)
    p = mp.mpc(1, 0)
    for n in range(1, N_TERMS):
        p *= 1 - q**n
    return q**(mp.mpf(1)/24) * p


def E4(tau):
    q = mp.exp(2j * mp.pi * tau)
    s = mp.mpc(0, 0)
    for n in range(1, N_TERMS):
        sigma3 = sum(d**3 for d in range(1, n+1) if n % d == 0)
        s += sigma3 * q**n
    return 1 + 240 * s


def E6(tau):
    q = mp.exp(2j * mp.pi * tau)
    s = mp.mpc(0, 0)
    for n in range(1, N_TERMS):
        sigma5 = sum(d**5 for d in range(1, n+1) if n % d == 0)
        s += sigma5 * q**n
    return 1 - 504 * s


def Delta_(tau):
    return eta(tau)**24


def j(tau):
    return E4(tau)**3 / Delta_(tau)


def H88(tau):
    j_t = j(tau)
    return j_t**2 + H_coef_a * j_t + H_coef_b


def f_a(tau, a_list=a_a):
    q = mp.exp(2j * mp.pi * tau)
    s = mp.mpc(0, 0)
    for n in range(1, len(a_list) + 1):
        an = a_list[n-1]
        if an != 0:
            s += an * q**n
    return s


def WQ_func(tau):
    return H88(tau)**2 * f_a(tau) / eta(tau)**12


# Test: scaling behavior near tau_Q
# If W^Q is exactly C * (tau - tau_Q)^2 + higher, then |W^Q (tau_Q + eps)| / eps^2 -> |C|.
print("Scaling test: |W^Q(tau_Q + eps)| / eps^2 should approach |W^Q''(tau_Q)|/2 as eps -> 0:")
W_pp_pred = mp.mpc(0, 0)
for eps_exp in [-1, -2, -3, -4, -5, -6]:
    eps = mp.mpf(10)**eps_exp
    val = WQ_func(tau_Q + eps)
    print(f"  eps = 1e{eps_exp}: |W^Q(tau_Q + eps)|/eps^2 = {mp.nstr(abs(val)/eps**2, 8)}")
print()
print("Scaling test: |W^Q(tau_Q + eps)| / eps^4 should grow if order < 4, stable if order = 4:")
for eps_exp in [-1, -2, -3, -4]:
    eps = mp.mpf(10)**eps_exp
    val = WQ_func(tau_Q + eps)
    print(f"  eps = 1e{eps_exp}: |W^Q(tau_Q + eps)|/eps^4 = {mp.nstr(abs(val)/eps**4, 8)}")
print()

# A CLEAN test: |W^Q(tau_Q + eps)| / eps^2 should converge to C (= W''/2 essentially).
# If W has a double zero, this should be roughly constant for small eps.

# Compute analytical W^Q''(tau_Q) value:
j_Q = j(tau_Q)
Hp_jQ = 2 * j_Q + H_coef_a
E4_Q = E4(tau_Q)
E6_Q = E6(tau_Q)
Delta_Q = Delta_(tau_Q)
jp_Q = -2j * mp.pi * E4_Q**2 * E6_Q / Delta_Q
Hjp_Q = Hp_jQ * jp_Q
f_a_Q = f_a(tau_Q)
eta_Q = eta(tau_Q)
eta12_Q = eta_Q**12

W_pp_pred = 2 * Hjp_Q**2 * f_a_Q / eta12_Q

print(f"ANALYTICAL W^Q''(tau_Q) = {W_pp_pred}")
print(f"|W^Q''(tau_Q)| = {abs(W_pp_pred)}")
print()

# Predicted leading behavior near tau_Q: W^Q(tau_Q + eps) ≈ (W''/2) eps^2 + O(eps^3)
print("Compare W^Q(tau_Q + eps) to (W''/2) eps^2:")
half_W_pp = W_pp_pred / 2
for eps_exp in [-3, -4, -5, -6, -7]:
    eps = mp.mpf(10)**eps_exp
    actual = WQ_func(tau_Q + eps)
    predicted = half_W_pp * eps**2
    ratio = actual / predicted if predicted != 0 else None
    print(f"  eps = 1e{eps_exp}: actual/predicted = {mp.nstr(ratio, 8)}")
print()

# Now V_F potential at tau_Q + s.
# V_F = e^K * [G^{tau,taubar} |D_tau W|^2 - 3 |W|^2]
# K = -3 log(2 Im tau).  At tau_Q, Im tau_Q = sqrt(11/2).
# G_{tau,taubar} = 3 / (2 Im tau)^2 = 3 / (2 sqrt(11/2))^2 = 3 / (2 * 11/2 * 2 ) = 3/22.
# G^{tau,taubar} = 22/3.
# e^K = (2 Im tau_Q)^{-3} = (2 sqrt(11/2))^{-3} = (2 sqrt(22)/2)^{-3} ... wait, 2 sqrt(11/2) = sqrt(22).
# So e^K = (sqrt 22)^{-3} = 22^{-3/2} = 1/(22 sqrt 22).

print("Kahler factor at tau_Q:")
print(f"  Im tau_Q = sqrt(11/2) = {mp.sqrt(mp.mpf(11)/2)}")
print(f"  2 Im tau_Q = 2 sqrt(11/2) = sqrt 22 = {mp.sqrt(22)}")
print(f"  e^K = (2 Im tau_Q)^{{-3}} = 22^{{-3/2}} = {mp.mpf(22)**(-mp.mpf(3)/2)}")
print(f"  G_{{tau,taubar}} = 3/(2 Im tau)^2 = 3/22 = {mp.mpf(3)/22}")
print(f"  G^{{tau,taubar}} = 22/3 = {mp.mpf(22)/3}")
print()

# Mass formula for SUGRA at Minkowski SUSY vacuum (W=DW=0):
# V_F(tau_Q + s) ≈ e^K * G^{tau,taubar} * |W''(tau_Q)|^2 * |s|^2 / 2  (leading order in s)
# Hmm wait, more carefully:
# Near tau_Q: W = (W''/2) s^2 + (W'''/6) s^3 + ... (since W = W' = 0 at tau_Q)
# W' = W'' s + (W'''/2) s^2 + ...
# D_tau W = W' + (3i/(2 Im tau)) W = W'' s + ... + (3i/(2 sqrt(11/2)) (W''/2) s^2 + ...
# Leading |D_tau W|^2 = |W''|^2 |s|^2.
# Leading |W|^2 = (1/4) |W''|^2 |s|^4.

# V_F = e^K [G^{tau,taubar} |D_tau W|^2 - 3 |W|^2]
#     ≈ e^K G^{tau,taubar} |W''|^2 |s|^2  (leading)

# m_tau^2 = (1/G_{tau,taubar}) * d^2 V_F / d s d sbar |_{s=0}
# Actually canonical mass: V = (1/2) m^2 |phi|^2 in canonical coords.
# d phi / d tau = sqrt(G_{tau,taubar})
# |s|^2 = (1/G) |phi|^2
# V_F ≈ (e^K / G) |W''|^2 |phi|^2 = (e^K G^{-1}) |W''|^2 |phi|^2.
# WAIT: it's e^K * G^{-1} (since we have G^-1 in V already).
# m^2 = 2 * (e^K * G^{-1}) * |W''|^2 = ... hmm need to be very careful.

# REFER TO M134's analysis sugra_F_term.py:
#   m^2 = (4/9) |W''(i)|^2 (specific to tau_S = i with Im=1).
# General formula: at Im tau_0:
#   m^2 = (1/G_{tau,taubar}^2) * e^K * G_{tau,taubar} * |W''|^2 = (e^K / G_{tau,taubar}) * |W''|^2
#       = (2 Im tau)^{-3} * (2 Im tau)^2 / 3 * |W''|^2 = (1/3) (2 Im tau)^{-1} |W''|^2 ... hmm doesn't match.

# Let me redo carefully using M134's sugra_F_term derivation:
# M134 says m^2 = (4/9) |W''(i)|^2 at tau = i (Im tau = 1).
# Generalization: at tau_0 with Im tau_0 = t,
#   d phi / d tau = sqrt(G) = sqrt(3/(2t)^2) = sqrt 3 / (2t).
#   d tau = (2t / sqrt 3) d phi.
#   |s|^2 = (4 t^2 / 3) |phi|^2.
#   V_F ≈ e^K * G^{-1} * |W''|^2 * |s|^2 = (1/(2t)^3) * (4 t^2/3) * |W''|^2 * (4 t^2/3) |phi|^2
#       = (4 t^2 / 3) * (4 t^2 / 3) / (2t)^3 * |W''|^2 |phi|^2
#       = 16 t^4 / 9 / (8 t^3) * |W''|^2 |phi|^2
#       = 16 t / 72 * |W''|^2 |phi|^2 = 2 t / 9 * |W''|^2 |phi|^2.
#   V = (1/2) m^2 |phi|^2 -> m^2 = 4 t / 9 * |W''|^2.
#
# At tau = i: t = 1, m^2 = 4/9 |W''(i)|^2. ✓ matches M134.
# At tau_Q: t = sqrt(11/2), m^2 = (4 sqrt(11/2) / 9) |W''(tau_Q)|^2.

t_Q = mp.sqrt(mp.mpf(11)/2)
m2_Q = (4 * t_Q / 9) * abs(W_pp_pred)**2
print(f"m_tau^2 at tau_Q (M134-natural Kahler factor):")
print(f"  m^2 = (4 sqrt(11/2) / 9) * |W^Q''(tau_Q)|^2")
print(f"       = (4 * sqrt(11/2) / 9) * |W^Q''(tau_Q)|^2")
print(f"       = {m2_Q}")
print()
print(f"  In Mpl^2 units (scientific): {mp.nstr(m2_Q, 12)}")
print()

# Compare to M134 m^2(i) = 2^16 * 3^6 * pi * Gamma(1/4)^4
m2_i_lemniscate = mp.mpf(2)**16 * mp.mpf(3)**6 * mp.pi * mp.gamma(mp.mpf(1)/4)**4
print(f"M134 m_tau^2(i) = 2^16 * 3^6 * pi * Gamma(1/4)^4 = {mp.nstr(m2_i_lemniscate, 12)}")
print(f"Ratio m^2(tau_Q) / m^2(i) = {mp.nstr(m2_Q / m2_i_lemniscate, 6)}")
print()

# CHOWLA-SELBERG for tau_Q = i sqrt(11/2):
# log eta(tau) at CM tau in K, K = Q(sqrt -22), D=-88:
#   log |eta(tau)| = -1/(8 pi sqrt(88)) * sum_{n=1..87} chi_{-22}(n) log Gamma(n/88)
#   plus the (Im tau)^(1/4) factor.
# For SPECIFIC tau_Q = i sqrt(11/2) = (representative of (2,0,11) class), the formula gives
# a specific Gamma-product.

# Closed form via Chowla-Selberg involves Gamma(p/88) for p coprime to 88.
print("Closed form involves Gamma values for K = Q(sqrt -22), specifically Gamma(p/88) for p in (Z/88)*.")
print("These are 'CM periods' for D = -88 (Chowla-Selberg).")
