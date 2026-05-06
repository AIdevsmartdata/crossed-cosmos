#!/usr/bin/env python3
"""
M143 / Step 4 -- Chi-squared landscape on the imaginary axis (Re tau = 0).

For the K-K Y_d^III model with K-K best-fit parameters (alpha_d, beta_d,
gamma_d^I, gamma_d^II, phi from K-K Table 5), scan Im tau and compute
chi^2 against:
  y_s/y_d target = 19.80  (running quark mass ratio at GUT scale per K-K)
  y_b/y_s target = 73.0
  y_b/y_d target = 1444   (= 19.8 * 73 within a few percent)

Plus the absolute size: y_b should be ~ 0.0354 for Yukawa to bottom mass.

Goal: identify the BEST Im tau on the imaginary axis (Re=0 forced),
then compare it to candidate CM points i sqrt(5), i sqrt(6), i sqrt(11/2).

If best Im tau is well within the experimental error of i sqrt(N) for some N,
that's evidence for an arithmetic origin.
"""

import mpmath as mp

mp.mp.dps = 30

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


def yukawa_at(tau, params):
    alpha_d, beta_d, gamma_d_I, gamma_d_II, phi = params
    M = Y_d_III(tau, phi, alpha_d, beta_d, gamma_d_I, gamma_d_II)
    sv = singular_values(M)
    yd, ys, yb = sv[2], sv[1], sv[0]
    return yd, ys, yb


# K-K Table 5 best-fit parameters
params = (mp.mpf("-2.387"), mp.mpf("2.672"), mp.mpf("0.6253"),
          mp.mpc("0.4958", "-0.2187"), mp.mpf("0.05663"))

# Targets at GUT scale (K-K Table 5):
# y_d * 10^5 = 2.45 -> y_d_target = 2.45e-5
# y_s * 10^4 = 4.85 -> y_s_target = 4.85e-4
# y_b * 10^2 = 3.54 -> y_b_target = 3.54e-2
y_d_target = mp.mpf("2.45e-5")
y_s_target = mp.mpf("4.85e-4")
y_b_target = mp.mpf("3.54e-2")

# Experimental relative errors at GUT scale (per K-K Table 4 / Antusch-Maurer 2013, ~10-20%)
sigma_rel = 0.15  # 15% conservative


def chi2_yukawa(tau, params):
    yd, ys, yb = yukawa_at(tau, params)
    chi2 = ((yd - y_d_target) / (sigma_rel * y_d_target))**2 \
        + ((ys - y_s_target) / (sigma_rel * y_s_target))**2 \
        + ((yb - y_b_target) / (sigma_rel * y_b_target))**2
    return chi2, (yd, ys, yb)


print("=" * 70)
print("M143 / Step 4 -- Chi^2 landscape on imaginary axis (Re=0)")
print("=" * 70)
print(f"\nTargets: y_d = {y_d_target}, y_s = {y_s_target}, y_b = {y_b_target}")
print(f"Sigma rel = {sigma_rel*100:.0f}%")

# Reference: K-K best-fit
tau_ref = mp.mpc("0.0361", "2.352")
chi2_ref, (yd, ys, yb) = chi2_yukawa(tau_ref, params)
print(f"\nReference K-K: tau = 0.0361 + 2.352i")
print(f"  y_d={mp.nstr(yd,5)}, y_s={mp.nstr(ys,5)}, y_b={mp.nstr(yb,5)}")
print(f"  chi^2 = {mp.nstr(chi2_ref, 6)}")

# Scan imaginary axis
print(f"\n{'Im tau':>14s} {'y_d/1e-5':>12s} {'y_s/1e-4':>12s} {'y_b/1e-2':>12s} {'chi^2':>14s}")
print("-" * 80)
chi2_min = mp.mpf("inf")
im_min = None
for im_tau in mp.linspace(2.20, 2.55, 36):
    tau = mp.mpc(0, im_tau)
    chi2, (yd, ys, yb) = chi2_yukawa(tau, params)
    if chi2 < chi2_min:
        chi2_min = chi2
        im_min = im_tau
    marker = ""
    print(f"{mp.nstr(im_tau, 6):>14s} {mp.nstr(yd*1e5, 5):>12s} {mp.nstr(ys*1e4, 5):>12s} {mp.nstr(yb*1e2, 5):>12s} {mp.nstr(chi2, 6):>14s}{marker}")

print(f"\nMinimum chi^2 at Im tau = {mp.nstr(im_min, 8)}, chi^2 = {mp.nstr(chi2_min, 6)}")

# Refine around minimum
print(f"\nFine-grained around best Im tau:")
chi2_min2 = mp.mpf("inf")
im_min2 = im_min
for im_tau in mp.linspace(im_min - mp.mpf("0.02"), im_min + mp.mpf("0.02"), 21):
    tau = mp.mpc(0, im_tau)
    chi2, (yd, ys, yb) = chi2_yukawa(tau, params)
    if chi2 < chi2_min2:
        chi2_min2 = chi2
        im_min2 = im_tau
    print(f"  Im={mp.nstr(im_tau,8)}  chi^2={mp.nstr(chi2, 6)}  y_d={mp.nstr(yd*1e5, 5)}  y_s={mp.nstr(ys*1e4,5)}")

print(f"\nRefined min chi^2 at Im = {mp.nstr(im_min2, 8)}")

# Now check candidates
print("\n" + "=" * 70)
print("Candidate CM Im tau values for the imaginary axis:")
print("=" * 70)
candidates = [
    ("i sqrt(5)        h(K)=2", mp.sqrt(5)),
    ("i sqrt(11/2)     non-CM", mp.sqrt(mp.mpf(11)/2)),
    ("i sqrt(6)        h(K)=2", mp.sqrt(6)),
    ("i (Im=2.352 KK)  fit",    mp.mpf("2.352")),
    ("i sqrt(22)/2     same as 11/2",  mp.sqrt(22)/2),
    ("i sqrt(33)/sqrt 6 = sqrt 5.5", mp.sqrt(mp.mpf(33))/mp.sqrt(6)),
    ("(1+i sqrt(22))/2 D=22", (1 + 1j*mp.sqrt(22))/2),  # has Re=1/2 not 0
]
print(f"\n{'candidate':>30s} {'tau':>30s} {'chi^2':>12s} {'(y_d, y_s, y_b)':>40s}")
for label, im_tau in candidates:
    if isinstance(im_tau, mp.mpc):
        tau = im_tau
    else:
        tau = mp.mpc(0, im_tau)
    chi2, (yd, ys, yb) = chi2_yukawa(tau, params)
    yvals = f"({mp.nstr(yd*1e5,3)}, {mp.nstr(ys*1e4,3)}, {mp.nstr(yb*1e2,3)})"
    print(f"{label:>30s} {mp.nstr(tau, 8):>30s} {mp.nstr(chi2, 5):>12s} {yvals:>40s}")

print()
print("=" * 70)
print("Q(sqrt -d) discriminants for d = 5, 6, 11/2 (which is sqrt -22 / 2, NOT integer).")
print("=" * 70)

# Now: does Re-optimizing K-K parameters at the candidate CM tau give as good a fit?
# Quick sensitivity: try perturbing alpha_d, beta_d to see if we can reach chi2 < 1.

print("\n>>> Mini-optimization at tau = i sqrt(11/2) (perturb alpha_d, beta_d, phi):")

import itertools
tau_test = mp.mpc(0, mp.sqrt(mp.mpf(11)/2))
best_chi2 = mp.mpf("inf")
best_params = None

# Adjust phi (controls y_b/y_s/y_d hierarchy via phi^4 vs phi^3 vs phi)
# Adjust alpha_d (controls y_d), beta_d (controls y_s), and gamma's (control y_b)
for phi_scale in [0.95, 0.98, 1.0, 1.02, 1.05]:
    for alpha_scale in [0.95, 1.0, 1.05]:
        for beta_scale in [0.95, 1.0, 1.05]:
            new_params = (params[0]*alpha_scale, params[1]*beta_scale, params[2], params[3], params[4]*phi_scale)
            chi2, _ = chi2_yukawa(tau_test, new_params)
            if chi2 < best_chi2:
                best_chi2 = chi2
                best_params = (alpha_scale, beta_scale, phi_scale)

print(f"  Best chi^2 with simple param scaling = {mp.nstr(best_chi2, 5)}, scales = {best_params}")

print("\n>>> Mini-optimization at tau = i sqrt(5):")
tau_test = mp.mpc(0, mp.sqrt(5))
best_chi2 = mp.mpf("inf")
best_params = None
for phi_scale in [0.95, 0.98, 1.0, 1.02, 1.05]:
    for alpha_scale in [0.95, 1.0, 1.05]:
        for beta_scale in [0.95, 1.0, 1.05]:
            new_params = (params[0]*alpha_scale, params[1]*beta_scale, params[2], params[3], params[4]*phi_scale)
            chi2, _ = chi2_yukawa(tau_test, new_params)
            if chi2 < best_chi2:
                best_chi2 = chi2
                best_params = (alpha_scale, beta_scale, phi_scale)
print(f"  Best chi^2 with simple param scaling = {mp.nstr(best_chi2, 5)}, scales = {best_params}")

print("\n>>> Mini-optimization at tau = i sqrt(6):")
tau_test = mp.mpc(0, mp.sqrt(6))
best_chi2 = mp.mpf("inf")
best_params = None
for phi_scale in [0.95, 0.98, 1.0, 1.02, 1.05]:
    for alpha_scale in [0.95, 1.0, 1.05]:
        for beta_scale in [0.95, 1.0, 1.05]:
            new_params = (params[0]*alpha_scale, params[1]*beta_scale, params[2], params[3], params[4]*phi_scale)
            chi2, _ = chi2_yukawa(tau_test, new_params)
            if chi2 < best_chi2:
                best_chi2 = chi2
                best_params = (alpha_scale, beta_scale, phi_scale)
print(f"  Best chi^2 with simple param scaling = {mp.nstr(best_chi2, 5)}, scales = {best_params}")
