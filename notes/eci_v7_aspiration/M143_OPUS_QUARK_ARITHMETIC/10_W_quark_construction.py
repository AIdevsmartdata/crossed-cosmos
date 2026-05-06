#!/usr/bin/env python3
"""
M143 / Step 10 -- Construct W^Q with structural double zero at the candidate
quark modulus tau_Q = i sqrt(11/2) (CM point of Q(sqrt -22), D=-88, h=2).

Background:
  W^L = (j-1728)/eta^6 has W^L(i) = 0 + W^{L'}(i) = 0 because j has a critical
  point at tau=i and E_6(i) = 0 (Klein).  This forces D_tau W = 0 in N=1 SUGRA
  with K = -3 log(2 Im tau).

For tau_Q = i sqrt(11/2), neither E_4 nor E_6 vanishes generically. The
critical points of j(tau) are EXACTLY tau=i (where E_6=0) and tau=rho (where
E_4=0). At tau_Q, j'(tau_Q) is NON-ZERO.

So a "double zero of j" at tau_Q is NOT structurally available.

What IS structurally available?
  Hilbert class polynomial H_{-88}(j) = j^2 - 6294842640000 j + 15798135578688000000
  vanishes EXACTLY at tau_Q AND at tau_Q' = i sqrt 22 (the other CM rep of Q(sqrt -22)).

  But H_{-88}(j(tau)) has SIMPLE zero (not double) at tau_Q, unless we choose a
  square: (H_{-88}(j))^2 has double zero. But this doesn't make D_tau W vanish
  unless we include the right Kahler structure.

Modular form approach: by Shimura reciprocity, certain weight-1 (or higher)
forms have prescribed CM points as zeros. E.g., theta series associated to
binary quadratic forms.

Alternative simpler approach:
  Consider W^Q(tau) = H_{-88}(j(tau)) / eta(tau)^k
  where k is chosen so the weight matches D_tau condition.

For W^L = (j-1728)/eta^6, j has weight 0 (modular function), eta^6 has weight 3
(half-integer * 6 = 3 mod 24, with eta multiplier system), so W^L is weight (-3)
under SL(2,Z) with appropriate multiplier.

For W^Q = H_{-88}(j(tau)) / eta(tau)^k, j is weight 0 so H_{-88}(j(tau)) is also
weight 0 (a modular FUNCTION, not form). To match the SUGRA convention W must be
weight -3, hence eta^6 denominator: W^Q = H_{-88}(j(tau))/eta(tau)^6.

Now the key question: does W^Q(tau_Q) = 0 force D_tau W^Q(tau_Q) = 0?

W^Q(tau_Q) = H_{-88}(j(tau_Q)) / eta^6(tau_Q) = 0  (since H_{-88}(j(tau_Q)) = 0).
W^Q'(tau_Q) = [H'_{-88}(j(tau_Q)) j'(tau_Q) eta^6 - H_{-88}(j) * 6 eta^5 eta'] / eta^12
            = H'_{-88}(j(tau_Q)) j'(tau_Q) / eta^6  (since H_{-88}(j(tau_Q)) = 0).

Now D_tau W^Q = W^Q'(tau_Q) + (3 i / (2 Im tau_Q)) * W^Q(tau_Q)
              = H'_{-88}(j(tau_Q)) j'(tau_Q) / eta^6  + 0

This is NON-ZERO generically because:
  - H'_{-88}(j) is a polynomial of degree 1 in j; H'_{-88}(j_a) = 2 j_a - 6294842640000
    = 2*2509696.077 - 6294842640000  ≈ -6294837620607.85, i.e. NON-ZERO.
  - j'(tau_Q) is generically non-zero (only at i, rho does j' = 0).
  - eta^6(tau_Q) is non-zero finite.

So W^Q(tau_Q) = 0 but D_tau W^Q(tau_Q) != 0 -- meaning V_F at tau_Q
is NOT zero (not Minkowski SUSY) but rather positive (AdS-broken or runaway).

>>> Conclusion: W^Q = H_{-88}(j)/eta^6 gives a SIMPLE zero at tau_Q (only W=0),
not a Minkowski SUSY vacuum.  Different from W^L.

To get DOUBLE zero W = W' = 0 at tau_Q, we need (H_{-88}(j))^2 / eta^12.
This has weight -6 in eta multiplier system, NOT -3.
"""

import mpmath as mp
import sympy as sp

mp.mp.dps = 40

N_TERMS = 300


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


def Delta_(tau):
    return eta(tau)**24


# Compute j and its derivative at tau_Q via Ramanujan:
#   d j/d tau = -2 pi i E_14 / Delta where E_14 = E_4^2 E_6
# So j'(tau) = -2 pi i E_4^2 E_6 / Delta = -2 pi i E_4^2 E_6 / eta^24

def j_prime(tau):
    """j'(tau) = -2 pi i E_4^2 E_6 / Delta."""
    e4 = E4(tau)
    e6 = E6(tau)
    return -2j * mp.pi * e4**2 * e6 / eta(tau)**24


# Test at tau = i (should be 0 since E_6(i) = 0):
tau_i = mp.mpc(0, 1)
print(f"j'(i) = {j_prime(tau_i)} (should be ~0 since E_6(i)=0)")

# At tau_Q:
tau_Q = mp.mpc(0, mp.sqrt(mp.mpf(11)/2))
j_at_Q = j_inv(tau_Q)
j_prime_at_Q = j_prime(tau_Q)
print(f"\ntau_Q = i sqrt(11/2) = {tau_Q}")
print(f"j(tau_Q) = {j_at_Q}")
print(f"j'(tau_Q) = {j_prime_at_Q}")
print(f"|j'(tau_Q)| = {abs(j_prime_at_Q)}")

# H_{-88}(X) = X^2 - 6294842640000 X + 15798135578688000000
H_a = mp.mpf("-6294842640000")
H_b = mp.mpf("15798135578688000000")

H_at_Q = j_at_Q**2 + H_a * j_at_Q + H_b
H_prime_at_Q = 2 * j_at_Q + H_a   # H'(X) = 2X + H_a (note H_a is signed coefficient)
# Wait: H_{-88}(X) = X^2 - 6294842640000 X + 15798135578688000000, so:
# H = X^2 + (-6294842640000) X + 15798135578688000000
# H' = 2X + (-6294842640000) = 2X - 6294842640000

H_prime_at_Q = 2 * j_at_Q - mp.mpf("6294842640000")

print(f"\nH_{{-88}}(j(tau_Q)) = {H_at_Q} (should be 0)")
print(f"|H_{{-88}}(j(tau_Q))| = {abs(H_at_Q)}")
print(f"H'_{{-88}}(j(tau_Q)) = {H_prime_at_Q}")
print(f"|H'_{{-88}}(j(tau_Q))| = {abs(H_prime_at_Q)}")

# So the derivative of H(j(tau)) at tau_Q is H'(j) j'(tau_Q):
W_Q_prime = H_prime_at_Q * j_prime_at_Q
print(f"\n[H_{{-88}}(j(tau))]' at tau_Q = H' * j' = {W_Q_prime}")
print(f"|...| = {abs(W_Q_prime)}")

# ==> H_{-88}(j(tau)) has a SIMPLE zero at tau_Q (not double).
# So W^Q = H_{-88}(j) / eta^6 has W^Q(tau_Q) = 0 BUT W^Q'(tau_Q) != 0,
# hence D_tau W^Q != 0 and V_F(tau_Q) > 0 (NOT Minkowski SUSY).

print("\n" + "=" * 70)
print("To get Minkowski SUSY at tau_Q, we need DOUBLE ZERO of W:")
print("  W^Q,double = H_{-88}(j(tau))^2 / eta^12")
print("This has weight -6 (in eta multiplier system) -- NOT the SUGRA-natural -3.")
print("=" * 70)

# But: in Mohseni-Vafa Tables 1-2, at tau = i, only specific weights k mod 12 give Minkowski.
# For weight -6, what does the M-V classification predict at tau_Q ≠ i, rho?
# M-V proves criticality only at i, rho fixed points.  At tau_Q, the criticality of
# V_F is NOT GUARANTEED by symmetry; we'd need to check explicitly.

# Compute V_F at tau_Q with W = (H/eta^6)^2 * (some normalization):
print()
print("Numerical V_F test for W^Q = H_{-88}(j(tau))^2 / eta^12:")
print()

# K = -3 log(2 Im tau).  e^K = 1 / (2 Im tau)^3.
# K_tau tau-bar = 3 / (2 Im tau)^2 = 3 / (tau - tau-bar)^2 actually different sign
# Using K = -k log(-(tau - taubar)/2i) with k=3:
#   K_tau = -k / (tau - taubar) = -k / (2 i Im tau)
#   K_tautaubar = k / (tau - taubar)^2 with appropriate i factors...
# Standard:
#   K = -3 log(-i (tau - taubar)) = -3 log(2 Im tau)
#   K_tau = -3 / (tau - taubar) = -3 / (2 i Im tau) = 3 i / (2 Im tau)
#   K_tau-bar = 3 i / (2 Im tau) (but mathematically with bars, K_taubar = -K_tau...)
# Actually the standard formulas:
#   K = -k log(2 t_2) where t_2 = Im tau.
#   K_tau = ∂_tau (-k log(2 Im tau)) = -k * (1/(2 Im tau)) * (1/(2 i)) = -k/(2i*2 Im tau) ... messy
# Let's redo: tau = t1 + i t2, Im tau = t2.  ∂_tau = (1/2)(∂_t1 - i ∂_t2).
#   ∂_tau Im tau = ∂_tau t2 = (1/2)(0 - i) = -i/2 .
#   K = -k log(2 t2). ∂_tau K = -k * (1/(2 t2)) * 2 * (-i/2) = -k * (-i)/(2 t2) = (i k)/(2 t2).
# So K_tau = i k / (2 t2). With k=3: K_tau = (3 i) / (2 Im tau). YES.
# D_tau W = W' + K_tau W = W' + (3 i / (2 Im tau)) W.

t2 = mp.im(tau_Q)
K_tau = 3j / (2 * t2)
print(f"K_tau at tau_Q: {K_tau}")

# W_double = H^2 / eta^12
def W_double(tau):
    return (j_inv(tau)**2 - mp.mpf("6294842640000") * j_inv(tau) + mp.mpf("15798135578688000000"))**2 / eta(tau)**12

# Need W'(tau_Q):
# W'(tau) = 2 H(j(tau)) H'(j(tau)) j'(tau) / eta^12 - 12 (H(j(tau)))^2 eta'/eta / eta^12
# At tau_Q, H(j(tau_Q)) = 0, so first term has factor H = 0; second term has factor H^2 = 0.
# So W'(tau_Q) = 0 EXACTLY.  Hence D_tau W = 0 at tau_Q. SUSY vacuum candidate.

# Compute W'(tau_Q) numerically by finite difference:
def W_double_v(tau):
    """Compute as float to avoid issues."""
    H = j_inv(tau)**2 - mp.mpf("6294842640000") * j_inv(tau) + mp.mpf("15798135578688000000")
    return H**2 / eta(tau)**12

# evaluate near tau_Q:
W_at_Q = W_double_v(tau_Q)
print(f"W^Q,double(tau_Q) = {W_at_Q} (should be 0)")
print(f"|W^Q,double(tau_Q)| = {abs(W_at_Q)}")

# Numerical derivative:
h = mp.mpf("1e-12")
W_plus = W_double_v(tau_Q + h)
W_minus = W_double_v(tau_Q - h)
W_prime_num = (W_plus - W_minus) / (2 * h)
print(f"W^Q,double'(tau_Q) ~ {W_prime_num} (should be 0)")
print(f"|W'| ~ {abs(W_prime_num)}")

# So D_tau W = W' + K_tau * W = 0 at tau_Q (both vanish).
DW = W_prime_num + K_tau * W_at_Q
print(f"D_tau W = W' + K_tau W = {DW} (should be ~0)")
print(f"|D_tau W| = {abs(DW)}")

# V_F = e^K [|D_tau W|^2 / K_tau-tau-bar - 3 |W|^2]
# K_tau-tau-bar = 3/(2 Im tau)^2 = 3/(4 t_2^2)
# 1/K_tau-tau-bar = 4 t_2^2 / 3
# e^K = 1/(2 Im tau)^3 = 1/(8 t_2^3)
# So V_F = (1/(8 t_2^3)) * [(4 t_2^2 /3) * |D W|^2 - 3 |W|^2]
#        = (1/(8 t_2^3)) * (4 t_2^2 /3) [|D W|^2 - (9/(4 t_2^2)) |W|^2]
#        = (1/(6 t_2)) [|D W|^2 - (9/(4 t_2^2)) |W|^2]

V_F = (1/(6*t2)) * (abs(DW)**2 - (9/(4*t2**2)) * abs(W_at_Q)**2)
print(f"V_F(tau_Q) = {V_F} (should be 0 for Minkowski SUSY)")
print()
print("If both W(tau_Q) = 0 AND D_tau W = 0, then V_F = 0 -- Minkowski SUSY at tau_Q.")
print()

# Check that W is non-vanishing OFF tau_Q:
print("Sanity: V_F at tau slightly displaced from tau_Q:")
for delta in [mp.mpf("0.001"), mp.mpf("0.01"), mp.mpf("0.1")]:
    tau_test = tau_Q + delta
    W = W_double_v(tau_test)
    h_ = mp.mpf("1e-10")
    W_p = (W_double_v(tau_test + h_) - W_double_v(tau_test - h_)) / (2 * h_)
    t2_local = mp.im(tau_test)
    DW_local = W_p + (3j/(2*t2_local)) * W
    V_F_local = (1/(6*t2_local)) * (abs(DW_local)**2 - (9/(4*t2_local**2)) * abs(W)**2)
    print(f"  tau = tau_Q + {delta}, V_F = {V_F_local}, |W| = {abs(W)}")

# Cross-check: is there a SIMPLER weight-(-3) construction?
# Idea: weight (-3) means we want eta^6 in denominator. So
#   W^Q = (some weight-3 modular form vanishing simply at tau_Q AND tau_Q')
# A weight-3 form is a section of sqrt(K) for K canonical; with multiplier system this is
# eta(tau)^k for k=6.  In SL(2,Z) we have NO weight-3 modular forms (only even weight).
# In Gamma_0(N) at level N=4 (or other) there are weight-3 forms, e.g. theta series of
# some quadratic forms.

# For Q(sqrt -22), the theta function of the binary quadratic form (1, 0, 22)
# is a weight-1 modular form for Gamma_1(88).  The theta of (2, 0, 11) is also.
# These are theta_Q(tau) = sum exp(2 pi i Q(m,n) tau) where Q is the form.

# Then theta_Q1 - theta_Q2 vanishes at tau_Q1 (corresponds to form Q1) and is non-zero
# at tau_Q2.

# This is the ARITHMETIC origin of CM-zero modular forms (Heegner-Stark, Gross-Zagier).

# For ECI v8.1 quark sector, the candidate W^Q would be a weight-3 (or some) Hecke
# eigenform on Gamma_0(88) vanishing at tau_Q = i sqrt(11/2).

# This is BEYOND scope of M143 but is a CONCRETE specialist target.
print()
print("=" * 70)
print("Summary: W^Q = (H_{-88}(j))^2/eta^12 gives V_F = 0 at tau_Q.")
print("(weight -6 multiplier; M-V Tables 1-2 don't classify this case at tau_Q.)")
print("Specialist construction: weight-3 form on Gamma_0(88) vanishing at tau_Q.")
print("=" * 70)
