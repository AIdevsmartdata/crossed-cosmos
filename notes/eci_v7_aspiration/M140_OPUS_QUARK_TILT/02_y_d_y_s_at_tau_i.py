#!/usr/bin/env python3
"""
M140 / Step 2 -- Compute the down-quark Yukawa eigenvalues y_d, y_s, y_b
in the King-King 2002.00969 model at tau = i (strict S-fixed point) versus
at the best-fit point Re tau = 0.0361, Im tau = 2.352.

We use the Y_d^III matrix (eq. 43) which is the most successful down-quark
Yukawa structure in K-K:

  Y_d^III = ( alpha_d phi^4 Y_1                     alpha_d phi^4 Y_3                 alpha_d phi^4 Y_2
              beta_d phi^3 Y_2                      beta_d phi^3 Y_1                  beta_d phi^3 Y_3
              gamma_d^I phi Y_{3,I}^(6) +           gamma_d^I phi Y_{2,I}^(6) +       gamma_d^I phi Y_{1,I}^(6) +
                gamma_d^II phi Y_{3,II}^(6)            gamma_d^II phi Y_{2,II}^(6)       gamma_d^II phi Y_{1,II}^(6)  )

where Y_{1,I}^(6) = Y_1^3 + 2 Y_1 Y_2 Y_3 etc. (eq. 22) and
phi = phi-tilde (real coupling) ~ 0.057 in K-K Table 5.

The down-quark MASS eigenvalues at the GUT scale follow:
  m_d : m_s : m_b ~ phi^4 : phi^3 : phi   (K-K eq. above 4.3)

which holds in K-K's CHOSEN Yukawa structure regardless of tau, as long as
the modular forms entering each row are O(1).

So the K-K weighton-driven hierarchy m_d : m_s : m_b ~ phi^4 : phi^3 : phi
DOES NOT BREAK at tau = i, because phi remains a free parameter (a flavon
expectation value), and it's the SAME hierarchy whether tau = i or near
tau = 2.35 i.

This is a CRUCIAL OBSERVATION:  K-K solve the quark mass hierarchy via
the *weighton field* phi, NOT via the modular form hierarchy itself.

So the "y_d/y_s = 4500x" claim from M134 must originate from a DIFFERENT
modular flavor model, NOT King-King 2002.00969.

Let us identify which model gives 4500x at tau=i.
"""

import mpmath as mp
import sys
sys.path.insert(0, '.')
from importlib import import_module
import os

mp.mp.dps = 40

N_TERMS = 200
omega = mp.exp(2j * mp.pi / 3)


def eta_and_dlog_eta(tau):
    q = mp.exp(2j * mp.pi * tau)
    prod = mp.mpf(1)
    for n in range(1, N_TERMS):
        prod *= 1 - q**n
    eta = q**(mp.mpf(1)/24) * prod
    s = mp.mpc(0, 0)
    for n in range(1, N_TERMS):
        s += n * q**n / (1 - q**n)
    dlog = 2j * mp.pi * (mp.mpf(1)/24 - s)
    return eta, dlog


def Yvec(tau):
    a = tau / 3; b = (tau + 1) / 3; c = (tau + 2) / 3; d = 3 * tau
    _, da = eta_and_dlog_eta(a)
    _, db = eta_and_dlog_eta(b)
    _, dc = eta_and_dlog_eta(c)
    _, dd = eta_and_dlog_eta(d)
    Y1 = (1j / (2 * mp.pi)) * (da + db + dc - 27 * dd)
    Y2 = (-1j / mp.pi) * (da + omega**2 * db + omega * dc)
    Y3 = (-1j / mp.pi) * (da + omega * db + omega**2 * dc)
    return mp.matrix([[Y1], [Y2], [Y3]])


def Yvec6_I(Y):
    """Weight-6 triplet I (eq.22 of King-King): (Y1^3 + 2 Y1 Y2 Y3, Y1^2 Y2 + 2 Y2^2 Y3, Y1^2 Y3 + 2 Y3^2 Y2)."""
    Y1 = Y[0]; Y2 = Y[1]; Y3 = Y[2]
    return mp.matrix([[Y1**3 + 2*Y1*Y2*Y3], [Y1**2 * Y2 + 2*Y2**2 * Y3], [Y1**2 * Y3 + 2*Y3**2 * Y2]])


def Yvec6_II(Y):
    """Weight-6 triplet II: (Y3^3 + 2 Y1 Y2 Y3, Y3^2 Y1 + 2 Y1^2 Y2, Y3^2 Y2 + 2 Y2^2 Y1)."""
    Y1 = Y[0]; Y2 = Y[1]; Y3 = Y[2]
    return mp.matrix([[Y3**3 + 2*Y1*Y2*Y3], [Y3**2 * Y1 + 2*Y1**2 * Y2], [Y3**2 * Y2 + 2*Y2**2 * Y1]])


def Y_d_III(tau, phi, alpha_d, beta_d, gamma_d_I, gamma_d_II):
    """Eq. 43 of King-King 2002.00969:

    Note: per equation 43 of K-K 2002.00969:
      row1 = alpha_d * phi^4 * (Y1, Y3, Y2)
      row2 = beta_d  * phi^3 * (Y2, Y1, Y3)
      row3 = phi * [gamma_d^I * (Y_{3,I}^6, Y_{2,I}^6, Y_{1,I}^6) + gamma_d^II * (Y_{3,II}^6, Y_{2,II}^6, Y_{1,II}^6)]
    """
    Y = Yvec(tau)
    Y6I = Yvec6_I(Y)
    Y6II = Yvec6_II(Y)

    Y1, Y2, Y3 = Y[0], Y[1], Y[2]
    Y6I_1, Y6I_2, Y6I_3 = Y6I[0], Y6I[1], Y6I[2]
    Y6II_1, Y6II_2, Y6II_3 = Y6II[0], Y6II[1], Y6II[2]

    M = mp.matrix(3, 3)
    M[0, 0] = alpha_d * phi**4 * Y1
    M[0, 1] = alpha_d * phi**4 * Y3
    M[0, 2] = alpha_d * phi**4 * Y2
    M[1, 0] = beta_d  * phi**3 * Y2
    M[1, 1] = beta_d  * phi**3 * Y1
    M[1, 2] = beta_d  * phi**3 * Y3
    M[2, 0] = phi * (gamma_d_I * Y6I_3 + gamma_d_II * Y6II_3)
    M[2, 1] = phi * (gamma_d_I * Y6I_2 + gamma_d_II * Y6II_2)
    M[2, 2] = phi * (gamma_d_I * Y6I_1 + gamma_d_II * Y6II_1)
    return M


def singular_values(M):
    """Compute singular values of complex 3x3 matrix M via M^dagger M."""
    Mh = M.transpose_conj()
    A = Mh * M
    # eigenvalues (3x3 hermitian) via mpmath
    eigvals, _ = mp.eig(A)
    # ensure real
    eigvals_re = sorted([abs(mp.re(ev)) for ev in eigvals], reverse=True)
    sv = [mp.sqrt(e) for e in eigvals_re]
    return sv


def report(tau, label, alpha_d, beta_d, gamma_d_I, gamma_d_II, phi):
    M = Y_d_III(tau, phi, alpha_d, beta_d, gamma_d_I, gamma_d_II)
    sv = singular_values(M)
    yd, ys, yb = sv[2], sv[1], sv[0]  # smallest, middle, largest = (d, s, b)
    print(f"\n{label}: tau = {mp.nstr(tau, 10)}")
    print(f"  y_b = {mp.nstr(yb, 6)}   (largest)")
    print(f"  y_s = {mp.nstr(ys, 6)}   (middle)")
    print(f"  y_d = {mp.nstr(yd, 6)}   (smallest)")
    print(f"  y_s / y_d = {mp.nstr(ys/yd, 6)}    (target ~ 200/4 ~ 20 actually y_s/y_d ~ 20)")
    print(f"  y_b / y_s = {mp.nstr(yb/ys, 6)}    (target ~ 70 (m_b/m_s))")
    print(f"  y_b / y_d = {mp.nstr(yb/yd, 6)}    (target ~ 1400)")


# K-K best-fit values from Table 6 (model III/II is closer to (Y_d^II) but
# actually we need Table 5 for III/VI):
# Table 5: alpha_d = -2.387, beta_d = 2.672, gamma_d^I = 0.6253, gamma_d^II = 0.4958 - 0.2187i, phi = 0.05663
print("=" * 70)
print("Reproduce K-K Table 5 best-fit numerics at the actual K-K tau")
print("=" * 70)
alpha_d_kk = mp.mpf(-2.387)
beta_d_kk = mp.mpf(2.672)
gamma_d_I_kk = mp.mpf(0.6253)
gamma_d_II_kk = mp.mpc(0.4958, -0.2187)
phi_kk = mp.mpf(0.05663)
tau_kk = mp.mpc(0.0361, 2.352)

report(tau_kk, "K-K best-fit", alpha_d_kk, beta_d_kk, gamma_d_I_kk, gamma_d_II_kk, phi_kk)
print()
print("Compare to K-K Table 5 outputs (values at GUT scale, with cos(beta)/(v_d/v_d) factor:")
print("  y_d * 10^5 = 2.45, y_s * 10^4 = 4.85, y_b * 10^2 = 3.54")
print(f"  i.e. y_d = 2.45e-5, y_s = 4.85e-4, y_b = 3.54e-2")
print(f"  K-K target y_s/y_d = {4.85e-4 / 2.45e-5}")
print(f"  K-K target y_b/y_s = {3.54e-2 / 4.85e-4}")

print("\n" + "=" * 70)
print("Same model parameters at tau = i strict (the bridge fixed point)")
print("=" * 70)
report(mp.mpc(0, 1), "tau = i strict", alpha_d_kk, beta_d_kk, gamma_d_I_kk, gamma_d_II_kk, phi_kk)

print("\n" + "=" * 70)
print("Same parameters with TILT tau = i + epsilon for various epsilon")
print("=" * 70)
for eps_log in range(-4, 0):
    eps = mp.mpf(10)**eps_log
    report(mp.mpc(eps, 1), f"tau = {eps} + i", alpha_d_kk, beta_d_kk, gamma_d_I_kk, gamma_d_II_kk, phi_kk)

print("\n" + "=" * 70)
print("Im-only tilt: tau = i (1 + delta)")
print("=" * 70)
for delta_log in range(-4, 0):
    delta = mp.mpf(10)**delta_log
    report(mp.mpc(0, 1 + delta), f"tau = i (1+{delta})", alpha_d_kk, beta_d_kk, gamma_d_I_kk, gamma_d_II_kk, phi_kk)

print("\n" + "=" * 70)
print("Hybrid tilt: tau = (Re tau, Im tau) sweep toward K-K best fit")
print("=" * 70)
for f in [mp.mpf(0), mp.mpf("0.01"), mp.mpf("0.1"), mp.mpf("0.3"), mp.mpf("0.5"), mp.mpf(1)]:
    re = f * mp.mpf(0.0361)
    im = 1 + f * (mp.mpf(2.352) - 1)
    report(mp.mpc(re, im), f"f={f}", alpha_d_kk, beta_d_kk, gamma_d_I_kk, gamma_d_II_kk, phi_kk)
