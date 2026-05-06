#!/usr/bin/env python3
"""
M143 / Step 3 -- TEST: is the K-K fit consistent with tau_Q PURELY IMAGINARY?

Reason: if Re tau_Q = 0 fits the data (K-K Re tau_Q = 0.0361 may be soft / phase
artifact), then tau_Q = i Im tau_Q is on the imaginary axis, where the
CM points i, i sqrt(2), i sqrt(3), i sqrt(5), i sqrt(6), i sqrt(7), ... live.

Im tau_Q = 2.352 sits between i sqrt(5) = 2.236 (h=2) and i sqrt(6) = 2.449 (h=2).

Distance to closest CM:
  i sqrt 5 = 2.2360679...   diff = 0.116
  i sqrt 6 = 2.4494897...   diff = 0.097
  i sqrt(11/2) = 2.3452     diff = 0.007

Test: would tau_Q = i sqrt(11/2) (= i sqrt(5.5)) fit K-K?

Rerun K-K Y_d^III at tau = 0 + i sqrt(11/2) and see y_d, y_s, y_b ratios.
"""

import mpmath as mp

mp.mp.dps = 40

N_TERMS = 200
omega = mp.exp(2j * mp.pi / 3)


def eta_and_dlog_eta(tau):
    q = mp.exp(2j * mp.pi * tau)
    prod = mp.mpf(1)
    for n in range(1, N_TERMS):
        prod *= 1 - q**n
    eta_ = q**(mp.mpf(1) / 24) * prod
    s = mp.mpc(0, 0)
    for n in range(1, N_TERMS):
        s += n * q**n / (1 - q**n)
    dlog = 2j * mp.pi * (mp.mpf(1) / 24 - s)
    return eta_, dlog


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
    Y1 = Y[0]; Y2 = Y[1]; Y3 = Y[2]
    return mp.matrix([[Y1**3 + 2*Y1*Y2*Y3], [Y1**2 * Y2 + 2*Y2**2 * Y3], [Y1**2 * Y3 + 2*Y3**2 * Y2]])


def Yvec6_II(Y):
    Y1 = Y[0]; Y2 = Y[1]; Y3 = Y[2]
    return mp.matrix([[Y3**3 + 2*Y1*Y2*Y3], [Y3**2 * Y1 + 2*Y1**2 * Y2], [Y3**2 * Y2 + 2*Y2**2 * Y1]])


def Y_d_III(tau, phi, alpha_d, beta_d, gamma_d_I, gamma_d_II):
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
    M[1, 0] = beta_d * phi**3 * Y2
    M[1, 1] = beta_d * phi**3 * Y1
    M[1, 2] = beta_d * phi**3 * Y3
    M[2, 0] = phi * (gamma_d_I * Y6I_3 + gamma_d_II * Y6II_3)
    M[2, 1] = phi * (gamma_d_I * Y6I_2 + gamma_d_II * Y6II_2)
    M[2, 2] = phi * (gamma_d_I * Y6I_1 + gamma_d_II * Y6II_1)
    return M


def singular_values(M):
    Mh = M.transpose_conj()
    A = Mh * M
    eigvals, _ = mp.eig(A)
    eigvals_re = sorted([abs(mp.re(ev)) for ev in eigvals], reverse=True)
    sv = [mp.sqrt(e) for e in eigvals_re]
    return sv


def report(tau, label, alpha_d, beta_d, gamma_d_I, gamma_d_II, phi):
    M = Y_d_III(tau, phi, alpha_d, beta_d, gamma_d_I, gamma_d_II)
    sv = singular_values(M)
    yd, ys, yb = sv[2], sv[1], sv[0]
    print(f"\n{label}: tau = {mp.nstr(tau, 12)}")
    print(f"  y_b = {mp.nstr(yb, 6)}")
    print(f"  y_s = {mp.nstr(ys, 6)}")
    print(f"  y_d = {mp.nstr(yd, 6)}")
    print(f"  y_s/y_d = {mp.nstr(ys/yd, 6)}    (target ~ 19.8)")
    print(f"  y_b/y_s = {mp.nstr(yb/ys, 6)}    (target ~ 73)")
    print(f"  y_b/y_d = {mp.nstr(yb/yd, 6)}    (target ~ 1444)")
    return yd, ys, yb


# K-K Table 5 best-fit parameters
alpha_d = mp.mpf("-2.387")
beta_d = mp.mpf("2.672")
gamma_d_I = mp.mpf("0.6253")
gamma_d_II = mp.mpc("0.4958", "-0.2187")
phi = mp.mpf("0.05663")

print("=" * 70)
print("M143 / Step 3 -- Test pure-imaginary tau_Q candidates with K-K params")
print("=" * 70)

# Reference: K-K best-fit
tau_kk = mp.mpc("0.0361", "2.352")
print("\n>>> Baseline: K-K best-fit tau = 0.0361 + 2.352i (full):")
report(tau_kk, "K-K best-fit", alpha_d, beta_d, gamma_d_I, gamma_d_II, phi)

# Test: Re tau = 0, Im tau = 2.352 (drop the Re component)
print("\n>>> TEST 1: tau = 0 + 2.352i (Re tau = 0 exactly):")
report(mp.mpc(0, "2.352"), "Re=0 only", alpha_d, beta_d, gamma_d_I, gamma_d_II, phi)

# Test: tau = i sqrt(11/2)  (special imaginary)
sqrt_11_over_2 = mp.sqrt(mp.mpf(11) / 2)
print(f"\n>>> TEST 2: tau = i sqrt(11/2) = i {sqrt_11_over_2}:")
report(mp.mpc(0, sqrt_11_over_2), "i sqrt(11/2)", alpha_d, beta_d, gamma_d_I, gamma_d_II, phi)

# Test: tau = i sqrt(5)  (h=2 CM)
print(f"\n>>> TEST 3: tau = i sqrt(5) = i {mp.sqrt(5)} (Q(sqrt-5) CM, h=2):")
report(mp.mpc(0, mp.sqrt(5)), "i sqrt 5", alpha_d, beta_d, gamma_d_I, gamma_d_II, phi)

# Test: tau = i sqrt(6)  (h=2 CM)
print(f"\n>>> TEST 4: tau = i sqrt(6) = i {mp.sqrt(6)} (Q(sqrt-6) CM, h=2):")
report(mp.mpc(0, mp.sqrt(6)), "i sqrt 6", alpha_d, beta_d, gamma_d_I, gamma_d_II, phi)

# Test: tau = i sqrt(22)/2 = i sqrt(5.5) -- variant
print(f"\n>>> TEST 5: tau = i sqrt(22)/2 (same as sqrt(11/2)):")
report(mp.mpc(0, mp.sqrt(22)/2), "i sqrt(22)/2", alpha_d, beta_d, gamma_d_I, gamma_d_II, phi)

# Now: scan Re tau at fixed Im tau = sqrt(11/2)
print(f"\n>>> Re tau scan at Im tau = sqrt(11/2):")
for re_tau in [mp.mpf("0"), mp.mpf("0.001"), mp.mpf("0.01"), mp.mpf("0.0361"), mp.mpf("0.05"), mp.mpf("0.1")]:
    tau = mp.mpc(re_tau, sqrt_11_over_2)
    report(tau, f"Re={re_tau}", alpha_d, beta_d, gamma_d_I, gamma_d_II, phi)

# Now: scan Im tau at Re tau = 0
print(f"\n>>> Im tau scan at Re tau = 0:")
for im_tau in [mp.sqrt(5), mp.sqrt(11)/mp.sqrt(2), mp.mpf("2.30"), mp.mpf("2.35"), mp.mpf("2.352"), mp.mpf("2.40"), mp.sqrt(6)]:
    tau = mp.mpc(0, im_tau)
    report(tau, f"Im={mp.nstr(im_tau, 8)}", alpha_d, beta_d, gamma_d_I, gamma_d_II, phi)
