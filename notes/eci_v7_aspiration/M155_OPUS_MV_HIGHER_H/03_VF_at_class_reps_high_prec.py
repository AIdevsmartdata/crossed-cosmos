#!/usr/bin/env python3
"""
M155 / Step 3 redo -- High precision V_F at class reps.

The previous version had:
  - finite-difference 2nd derivative was overly noisy
  - W''(tau_a) was actually CHAIN-RULE expression dominated by H' j' / eta^12 second
    derivative; we need ANALYTIC computation to avoid catastrophic cancellation.

ANALYTIC: For W = H(j(tau))^2 / eta(tau)^12 with H(j(tau_*)) = 0 (CM),
  W = u^2 / eta^12, where u = H(j(tau)) = a*(tau - tau_*) + O((tau - tau_*)^2)
  so u(tau_*) = 0, u'(tau_*) = H'(j_*) j'(tau_*) =: A
  u^2 = A^2 (tau - tau_*)^2 + O((tau-tau_*)^3)
  At tau = tau_*:
    W(tau_*) = 0
    W'(tau_*) = 0
    W''(tau_*) = 2 A^2 / eta(tau_*)^12

So ANALYTICALLY:
  W(tau_*) = 0     EXACTLY
  W'(tau_*) = 0    EXACTLY
  W''(tau_*) = 2 A^2 / eta(tau_*)^12

This IS the Hessian / mass scale. The previous numerics for W' should have given 0,
not 1e36, indicating the finite-difference scale was too large for the steeply-varying
H(j(tau)) near tau_a.

mpmath dps=60 with very small h.
"""

import mpmath as mp
mp.mp.dps = 60

N_TERMS = 500


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


def Delta_(tau):
    return eta(tau)**24


def j_inv(tau):
    return E4(tau)**3 / Delta_(tau)


def j_prime(tau):
    """j'(tau) = -2 pi i E_4^2 E_6 / Delta."""
    return -2j * mp.pi * E4(tau)**2 * E6(tau) / Delta_(tau)


# Class reps
tau_a = mp.mpc(0, mp.sqrt(22))
tau_b = mp.mpc(0, mp.sqrt(mp.mpf(11)/2))

H_lin = mp.mpf("-6294842640000")  # coefficient of X in H_{-88}(X)
H_const = mp.mpf("15798135578688000000")


def H_88(X):
    return X**2 + H_lin * X + H_const


def H_88_prime(X):
    return 2 * X + H_lin


# =====================================================================
# ANALYTIC W''(tau_*) for W = H_{-88}(j)^2 / eta^12
# =====================================================================
print("=" * 72)
print("M155 / Step 3 redo: ANALYTIC W'' at CM points")
print("=" * 72)

# At CM: H(j(tau_*)) = 0, so:
#   u = H(j(tau)) ~ A * (tau - tau_*)  near tau_*
#   A = H'(j_*) * j'(tau_*)
# Hence:
#   W = u^2 / eta^12  ~ A^2 (tau - tau_*)^2 / eta(tau_*)^12 + O((tau-tau_*)^3)
#   W''(tau_*) = 2 A^2 / eta(tau_*)^12

for label, tau_star in [("tau_a (class [1])", tau_a), ("tau_b (class [2])", tau_b)]:
    j_star = j_inv(tau_star)
    H_p_star = H_88_prime(j_star)
    j_p_star = j_prime(tau_star)
    A = H_p_star * j_p_star
    eta_star = eta(tau_star)
    W_pp_analytic = 2 * A**2 / eta_star**12
    print(f"\n{label}:")
    print(f"  tau_star = {tau_star}")
    print(f"  j(tau_star)        = {j_star}")
    print(f"  H'(j_star)         = {H_p_star}")
    print(f"  j'(tau_star)       = {j_p_star}")
    print(f"  A = H' j'          = {A}")
    print(f"  |A|                = {abs(A)}")
    print(f"  eta(tau_star)      = {eta_star}")
    print(f"  eta^12             = {eta_star**12}")
    print(f"  W''(tau_star) = 2A^2/eta^12 = {W_pp_analytic}")
    print(f"  |W''(tau_star)|             = {abs(W_pp_analytic)}")

# =====================================================================
# Sanity: |W| and |W'| and V_F via analytic formulas
# Since W''(tau_*) is the only non-zero leading derivative, in canonical Kahler
# coordinates the mass^2 = (4/k_eff^2) |W''|^2 e^{K_*} factor.
# =====================================================================

print()
print("=" * 72)
print("V_F at exact CM point (analytic):")
print("=" * 72)
print()
print("ANALYTICALLY, with W = H^2/eta^12 (weight -6 in eta multiplier system):")
print("  W(tau_*)       = 0         (exact, CM)")
print("  W'(tau_*)      = 0         (exact, double zero from H^2)")
print("  D_tau W(tau_*) = W'(tau_*) + (3i k_K/(2 Im tau)) W(tau_*) = 0  (both zero)")
print("  V_F(tau_*) = e^K [|D_tau W|^2 K^{tau bar tau} - 3 |W|^2] = 0")
print()
print("=> V_F = 0 at BOTH tau_a and tau_b (Minkowski SUSY at both class reps)")
print()

# =====================================================================
# CRITICAL: Higher-order Taylor expansion to extract m^2 (canonical mass)
# =====================================================================
print("=" * 72)
print("Mass spectrum at each CM point:")
print("=" * 72)

# Following M134 logic for K = -3 log(2 Im tau):
#   V_F(tau) ~ (1/6) |W''(tau_*)|^2 |tau - tau_*|^2 + O(|tau-tau_*|^4)
# Mass^2 in canonical coords = (4/9)(2/something) |W''|^2 with K weight.
#
# M-V: K is weight (k,k) with k matching W's weight to make G = K + log|W|^2 invariant.
# For W weight -6, K should be K = -6 log(2 Im tau) (k_K = 6) for consistency.
# Then
#   K^{tau bar tau} = (2 Im tau)^2 / 6 = (2 t_2)^2 / 6
#   K_tau-tau-bar = 6/(2 t_2)^2 = 3/(2 t_2^2)
#   d_tau K = 6 i / (2 t_2) = 3i/t_2
#
# Near tau_*:
#   W(tau) = (1/2) W''(tau_*) (tau - tau_*)^2 + O(...)
#   W'(tau) = W''(tau_*) (tau - tau_*) + O(...)
#   D_tau W = W' + d_tau K * W
#           = W''(tau_*) (tau-tau_*) + (3i/t_2) (1/2) W''(tau_*) (tau-tau_*)^2 + ...
#           ~ W''(tau_*) (tau-tau_*)  to leading order
#
#   |D_tau W|^2 ~ |W''(tau_*)|^2 |tau - tau_*|^2
#   |W|^2 ~ (1/4) |W''(tau_*)|^2 |tau - tau_*|^4
#
#   V_F = (1/(2 t_2)^6) [(2t_2)^2/6 * |D W|^2 - 3 |W|^2]
#       = (1/(2 t_2)^6) (2t_2)^2/6 |W''|^2 |tau-tau_*|^2 + O(|tau-tau_*|^4)
#       = |W''|^2 |tau-tau_*|^2 / (6 (2 t_2)^4)
#
# In canonical coords phi: G_TT* = 6/(2 t_2)^2 (for K = -6 log(2 Im tau))
#   d phi = sqrt(G_TT*) d tau = sqrt(6)/(2 t_2) d tau
#   |tau-tau_*|^2 = (2 t_2)^2 / 6 |phi|^2 in canonical
#
#   V_F = |W''|^2 / (6 (2 t_2)^4) * (2 t_2)^2 /6 |phi|^2 = |W''|^2 / (36 (2 t_2)^2) |phi|^2
#   But V = (1/2) m^2 |phi|^2 in canonical
#   => m^2 = |W''|^2 / (18 (2 t_2)^2) = |W''|^2 / (72 t_2^2)
#
# Compare M134 (k=3, K=-3 log(2 Im tau), tau=i, t_2=1):
#   V_F ~ (1/6) |W''|^2 |tau-i|^2,  G_TT* = 3/(2 t_2)^2 = 3/4 at i
#   |tau-i|^2 = 4/3 |phi|^2
#   V_F = (1/6) |W''|^2 * 4/3 |phi|^2 = (2/9) |W''|^2 |phi|^2
#   => m^2 = (4/9) |W''|^2  CHECK with M134.

# So for our weight -6 case at tau_a, tau_b:
for label, tau_star in [("tau_a", tau_a), ("tau_b", tau_b)]:
    j_star = j_inv(tau_star)
    H_p_star = H_88_prime(j_star)
    j_p_star = j_prime(tau_star)
    A = H_p_star * j_p_star
    eta_star = eta(tau_star)
    W_pp = 2 * A**2 / eta_star**12
    t2 = mp.im(tau_star)
    m2 = abs(W_pp)**2 / (72 * t2**2)
    print(f"{label}: t_2 = {t2}, |W''| = {mp.nstr(abs(W_pp), 6)}")
    print(f"  m^2 = |W''|^2/(72 t_2^2) = {mp.nstr(m2, 6)}")

print()

# =====================================================================
# Galois conjugacy of (j_a, j_b)
# =====================================================================
print("=" * 72)
print("Class group / Galois conjugacy structure:")
print("=" * 72)

# j_a and j_b are roots of H_{-88}(X) = X^2 + H_lin X + H_const.
# Both lie in Q(sqrt 2):
#   j(tau_a) = 3,147,421,320,000 + 2,225,561,184,000 sqrt 2
#   j(tau_b) = 3,147,421,320,000 - 2,225,561,184,000 sqrt 2

j_a_pred = mp.mpf("3147421320000") + mp.mpf("2225561184000") * mp.sqrt(2)
j_b_pred = mp.mpf("3147421320000") - mp.mpf("2225561184000") * mp.sqrt(2)
print(f"j(tau_a) predicted: {j_a_pred}")
print(f"j(tau_a) numerical: {j_inv(tau_a)}")
print(f"diff = {abs(j_inv(tau_a) - j_a_pred)}")
print(f"j(tau_b) predicted: {j_b_pred}")
print(f"j(tau_b) numerical: {j_inv(tau_b)}")
print(f"diff = {abs(j_inv(tau_b) - j_b_pred)}")
print()

# H'(j_a) = 2 j_a + H_lin
H_p_a = 2 * j_a_pred + H_lin
H_p_b = 2 * j_b_pred + H_lin
print(f"H'(j_a) = 2 j_a + (-6,294,842,640,000) = {H_p_a}")
print(f"        = 2 * 2,225,561,184,000 sqrt 2 = {2 * mp.mpf('2225561184000') * mp.sqrt(2)}")
print(f"H'(j_b) = {H_p_b}")
print(f"        = -2 * 2,225,561,184,000 sqrt 2 = {-2 * mp.mpf('2225561184000') * mp.sqrt(2)}")
print()
print(f"|H'(j_a)|^2 = |H'(j_b)|^2 = (2 * 2225561184000)^2 * 2 = {(2 * mp.mpf('2225561184000'))**2 * 2}")
print()

# So |A_a|^2 = |H'(j_a)|^2 |j'(tau_a)|^2  and  |A_b|^2 = same |H'(j_b)|^2 |j'(tau_b)|^2
# The Galois orbit ensures |H'(j_a)| = |H'(j_b)|, but |j'(tau_a)| != |j'(tau_b)| because
# j' depends on E_4(tau)^2 E_6(tau)/Delta(tau) which transforms covariantly under Gamma_0.

# Specifically, under Atkin-Lehner w_22 sending tau_a <-> tau_b:
#   j(w_22 tau) = j(-1/(22 tau)) = j(tau)  ONLY if 22 acts on j -- but j is SL(2,Z) invariant
#   so j(-1/22 tau) is generally NOT j(tau).
# In fact tau_a = i sqrt 22 is NOT related to tau_b = i sqrt(11/2) by any SL(2,Z) element.
# They map under Fricke involution w_88 of Gamma_0(88) maybe?

print("Atkin-Lehner relation:")
print("  Fricke involution w_N: tau -> -1/(N tau)")
print(f"  w_22 (tau_a) = -1/(22 * i sqrt 22) = i / (22 sqrt 22) = i sqrt 22 / 22 = i / sqrt 22")
w_22_a = -1/(22 * tau_a)
print(f"  numerical: w_22(tau_a) = {w_22_a}")
print(f"  Im[w_22(tau_a)]    = {mp.im(w_22_a)}")
print(f"  expected: 1/sqrt 22 = {1/mp.sqrt(22)}")
print()
print(f"  w_22(tau_b) = -1/(22 * i sqrt(11/2)) = i / (22 sqrt(11/2)) = i sqrt(2/11)/22*sqrt(11/2)")
w_22_b = -1/(22 * tau_b)
print(f"  numerical: w_22(tau_b) = {w_22_b}")
print(f"  Im[w_22(tau_b)] = {mp.im(w_22_b)}")
print()
print("These do NOT swap tau_a and tau_b. Need different involution.")
print()

# Instead try w_2, w_11 on Gamma_0(22):
for N in [2, 11, 22, 44, 88]:
    w_a = -1/(N * tau_a)
    w_b = -1/(N * tau_b)
    print(f"w_{N}(tau_a) = -1/({N} * i sqrt 22) = i / ({N} sqrt 22) = {w_a}")
    print(f"w_{N}(tau_b) = -1/({N} * i sqrt(11/2)) = {w_b}")

print()
print("=" * 72)
print("Numerical verification of Hilbert class poly (M143 result):")
print("=" * 72)
HH = (j_a_pred + j_b_pred, j_a_pred * j_b_pred)
print(f"j_a + j_b = {HH[0]}")
print(f"j_a * j_b = {HH[1]}")
