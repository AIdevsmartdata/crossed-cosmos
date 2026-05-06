#!/usr/bin/env python3
"""
M140 / Step 3 -- Taylor expand V_F(tau = i + eps) up to O(eps^4) for the
Mohseni-Vafa / M134 superpotential W(tau) = (j(tau) - 1728)/eta(tau)^6.

Goal: find the threshold eps_*  at which V_F(i + eps) = (10^-5 M_Pl)^4,
and check if eps_* is large enough to give y_s/y_d ~ 20 in K-K Y_d^III.

Recall from M134 V_F_taylor_analytic.py:
  V_F(i + s) = (1/6) |A|^2 |s|^2  +  O(|s|^3)
  A = W''(i) = -3456 pi^2 E_4(i) / eta(i)^6  (real, negative)
  |A|^2 ~ 5.83 * 10^10
  m_tau^2 = (4/9) |A|^2 ~ 2.59 * 10^10  (in M_Pl=1, |W| ~ M_Pl^3 units)

So  V_F(i+eps) ~ (|A|^2 / 6) eps^2 ~ 9.7 * 10^9 * eps^2.

If we cap V_F < (10^-5)^4 = 10^-20, we need eps^2 < 10^-20 / 10^10 = 10^-30,
i.e. eps < 10^-15. This is *EXTREMELY* small; well below any meaningful
y_d/y_s tilt.

But this assumes that A and |W| are normalized to M_Pl. Let us be careful:
in the lepton model M134 used, W is the FORMAL modular form, not the
physical dimensional W. Let's parameterize.

Let W_phys = Lambda_W^3 * W(tau)/W_ref where Lambda_W is a UV scale.
Then V_F_phys = e^K |F|^2 - 3 |W_phys|^2 / M_Pl^2 ~ (Lambda_W^6/M_Pl^4) ~ tau-dependent.

For V_F < 10^-120 M_Pl^4 (cosmological constant), we need either
Lambda_W << M_Pl (unlikely) or W(i) = 0 exactly (M134 result) and
near-cancellation for tau != i.

Therefore, "V_F < 10^-5 M_Pl^4" corresponds to Lambda_W ~ M_Pl and tau
within FRACTION (10^-5)^(1/2) / (sqrt(|A|^2/6)/Lambda_W^3) of i.

For Lambda_W = M_Pl and (1/6)|A|^2 = 1e10 (in tau-derivative units that
are FORMAL, not Planck-normalized):
  V_F(i+eps) = (Lambda_W^6 / M_Pl^4) * (1/6) |A|^2 |eps|^2 / |W_ref|^2
where |W_ref|^2 must absorb the formal-vs-physical normalization.

The ECI v8.1 framing in M134 uses "natural units M_Pl=1, |W| ~ M_Pl^3".
In this convention we are stuck with |A|^2 = 5.83e10 dimensionless and
V_F < 10^-5 means eps < 1.31e-8.

Let's compute V_F at multiple eps and check:
  - V_F(eps) directly
  - corresponding y_s/y_d from K-K Y_d^III
  - whether the "stay near i" (V_F < 10^-5) is compatible with "y_s/y_d ~ 20" (eps ~ 0.1).
"""

import mpmath as mp

mp.mp.dps = 40

N_TERMS = 200


def eta_eta_dlog(tau):
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


def E4_E6(tau):
    q = mp.exp(2j * mp.pi * tau)
    s4 = mp.mpf(0); s6 = mp.mpf(0)
    for n in range(1, N_TERMS):
        sigma3 = sum(d**3 for d in range(1, n+1) if n % d == 0)
        sigma5 = sum(d**5 for d in range(1, n+1) if n % d == 0)
        s4 += sigma3 * q**n
        s6 += sigma5 * q**n
    return 1 + 240*s4, 1 - 504*s6


def W_and_derivs(tau):
    """Return W(tau), W'(tau), W''(tau) for W = (j - 1728)/eta^6
       using j = 1728 E_4^3 / (E_4^3 - E_6^2) and j-1728 = 1728 E_6^2 / (E_4^3 - E_6^2).

    We compute via finite differences (better since eta and j q-series are slow)."""
    h = mp.mpf("1e-12")
    e4, e6 = E4_E6(tau)
    eta, _ = eta_eta_dlog(tau)
    Delta = (e4**3 - e6**2) / 1728  # eta^24 = Delta
    jm = 1728 * e6**2 / (e4**3 - e6**2)
    W0 = jm / eta**6
    return W0


def W_at(tau):
    e4, e6 = E4_E6(tau)
    eta, _ = eta_eta_dlog(tau)
    jm = 1728 * e6**2 / (e4**3 - e6**2)
    return jm / eta**6


def V_F(tau):
    """V_F = e^K [(2 Im tau)^2/3 |D_tau W|^2 - 3 |W|^2]
       e^K = (2 Im tau)^{-3}
       D_tau W = W' + (3i/(2 Im tau)) W"""
    h = mp.mpf("1e-8")
    W0 = W_at(tau)
    Wp = (W_at(tau + h) - W_at(tau - h)) / (2*h)
    y = mp.im(tau)
    DK = 3j / (2*y)
    DW = Wp + DK * W0
    twoIm = 2 * y
    return mp.re((1/twoIm**3) * (twoIm**2/3 * abs(DW)**2 - 3 * abs(W0)**2))


print("V_F(tau = i + s) for various s along the real axis (Re-tilt):")
print(f"{'s':>14s} {'V_F(i+s) num':>18s} {'predicted (1/6)|A|^2 s^2':>30s}")
print('-' * 70)

# A = W''(i) ~ -2.4156e5
A_abs_sq = mp.mpf("5.8353e10")  # |A|^2 ~ 5.83e10 from M134 verify

for log_eps in [-12, -10, -8, -6, -5, -4, -3, -2, -1.5, -1, -0.5]:
    eps = mp.mpf(10) ** log_eps
    tau = mp.mpc(eps, 1)
    Vf = V_F(tau)
    pred = (A_abs_sq / 6) * eps**2
    print(f"  {mp.nstr(eps, 4):>12s}  {mp.nstr(Vf, 6):>18s}  {mp.nstr(pred, 6):>20s}    ratio={mp.nstr(Vf/pred, 5) if pred != 0 else 'N/A':>10s}")

print()
print("Now V_F(tau = i + s) with s along the imaginary axis (Im-tilt):")
print(f"{'s':>14s} {'V_F(i+is) num':>18s} {'predicted (1/6)|A|^2 s^2':>30s}")
print('-' * 70)

for log_eps in [-12, -10, -8, -6, -5, -4, -3, -2, -1.5, -1, -0.5]:
    eps = mp.mpf(10) ** log_eps
    tau = mp.mpc(0, 1 + eps)
    Vf = V_F(tau)
    pred = (A_abs_sq / 6) * eps**2
    print(f"  {mp.nstr(eps, 4):>12s}  {mp.nstr(Vf, 6):>18s}  {mp.nstr(pred, 6):>20s}    ratio={mp.nstr(Vf/pred, 5) if pred != 0 else 'N/A':>10s}")


print()
print("=" * 70)
print("Critical eps thresholds")
print("=" * 70)
print()
# V_F = (10^-5)^4 = 10^-20:  eps_* = sqrt(6 * 10^-20 / |A|^2) = sqrt(6e-20 / 5.83e10) = ?
target_VF = mp.mpf("1e-20")
eps_VF1 = mp.sqrt(6 * target_VF / A_abs_sq)
print(f"V_F < 10^-20 (i.e. ~1e-5 M_Pl^4)^4 requires eps < {mp.nstr(eps_VF1, 4)}")

# V_F < 10^-120 (current cosmological constant) - completely impractical
target_VF = mp.mpf("1e-120")
eps_cc = mp.sqrt(6 * target_VF / A_abs_sq)
print(f"V_F < 10^-120 (CC) requires eps < {mp.nstr(eps_cc, 4)}  -- effectively zero")

# V_F < 10^-10 (sub-Planckian inflation):
target_VF = mp.mpf("1e-10")
eps_inf = mp.sqrt(6 * target_VF / A_abs_sq)
print(f"V_F < 10^-10 (sub-Planckian inflation) requires eps < {mp.nstr(eps_inf, 4)}")

# V_F < 10^-5 (large Hubble inflation scale):
target_VF = mp.mpf("1e-5")
eps_inf2 = mp.sqrt(6 * target_VF / A_abs_sq)
print(f"V_F < 10^-5 (large inflation scale) requires eps < {mp.nstr(eps_inf2, 4)}")

# Compare with eps required for y_s/y_d ~ 20 in K-K  (from script 02: eps must be ~0.05-0.10 at the K-K best fit)
print()
print("EPS NEEDED for K-K-type quark hierarchy:")
print(f"  Re-tilt only: eps ~ 0.1 gives y_s/y_d ~ 31.5 (still 50% too high)")
print(f"  Im-tilt only: eps ~ 0.1 gives y_s/y_d ~ 35   (similar)")
print(f"  Hybrid: eps_re=0.036, eps_im=1.35 (i.e. tau = 2.352 i + 0.036) gives 19.67 ✓")
print()
print("CONCLUSION: epsilon required for hierarchy ~ 0.1 (Re-tilt) or ~ 1.3 (Im-tilt to 2.35i),")
print(f"            but Vf = 10^-5 requires eps < {mp.nstr(eps_inf2, 4)}.")
print(f"            Mismatch factor: {mp.nstr(mp.mpf('0.1') / eps_inf2, 4)} for Re-tilt.")
