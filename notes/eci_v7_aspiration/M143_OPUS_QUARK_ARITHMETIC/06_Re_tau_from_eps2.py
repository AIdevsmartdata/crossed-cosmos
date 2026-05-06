#!/usr/bin/env python3
"""
M143 / Step 6 -- Verify K-K Re tau = 0.0361 is set by the q-expansion of
the small Yukawa observables eps_2, eps_3 (eq 59 in K-K).

K-K eq 59:
   Y_1 = 1 + O(q)
   Y_2 = -6 q^(1/3) + O(q)
   Y_3 = -18 q^(2/3) + O(q)
   q = exp(2 pi i tau)

K-K Table 5 best-fit values:
   eps_2 := Y_2 / Y_1 ~ -6 q^(1/3)  =>  -0.043 - 0.0033i
   eps_3 := Y_3 / Y_1 ~ -18 q^(2/3) =>  -0.00094 - 0.00014i

Now q^(1/3) = exp((2 pi i tau)/3) = exp(-(2 pi /3) Im tau) * exp(i (2 pi /3) Re tau)

So eps_2 = -6 q^(1/3) has phase = pi + (2 pi /3) Re tau
   arg(eps_2) = atan2(-0.0033, -0.043) = pi + atan2(-0.0033, -0.043) (third quadrant)

Likewise eps_3 = -18 q^(2/3) phase = pi + (4 pi /3) Re tau
   arg(eps_3) = atan2(-0.00014, -0.00094)

Solve for Re tau and check whether it is "rational" or "arithmetic".
"""

import mpmath as mp

mp.mp.dps = 30


def to_principal(theta):
    """Map angle to (-pi, pi]."""
    while theta > mp.pi:
        theta -= 2 * mp.pi
    while theta <= -mp.pi:
        theta += 2 * mp.pi
    return theta


# K-K Table 5 numerical values (eq 59):
eps2 = mp.mpc("-0.043", "-0.0033")
eps3 = mp.mpc("-0.00094", "-0.00014")

arg2 = mp.atan2(mp.im(eps2), mp.re(eps2))
arg3 = mp.atan2(mp.im(eps3), mp.re(eps3))
print(f"arg(eps_2) = {arg2} rad = {arg2 * 180 / mp.pi} deg")
print(f"arg(eps_3) = {arg3} rad = {arg3 * 180 / mp.pi} deg")

# arg(eps_2) = pi + (2 pi /3) Re tau (mod 2 pi)
# Re tau = (3 / (2 pi)) * (arg(eps_2) - pi) (taking principal -pi <= ... <= pi)
# but arg is in (-pi, pi]; eps_2 third quadrant => arg = -pi + alpha where alpha is small
# Let's compute:
Re_tau_from_eps2 = 3 / (2 * mp.pi) * to_principal(arg2 - mp.pi)
Re_tau_from_eps3 = 3 / (4 * mp.pi) * to_principal(arg3 - mp.pi)

print(f"\nFrom eps_2: Re tau = {Re_tau_from_eps2}")
print(f"From eps_3: Re tau = {Re_tau_from_eps3}")
print(f"K-K Table 5: Re tau = 0.0361")

# Now also: |eps_2| = 6 exp(-(2 pi /3) Im tau)
# Im tau = -(3/(2 pi)) ln(|eps_2| / 6)
Im_tau_from_eps2 = -(3 / (2 * mp.pi)) * mp.log(abs(eps2) / 6)
Im_tau_from_eps3 = -(3 / (4 * mp.pi)) * mp.log(abs(eps3) / 18)
print(f"\nFrom |eps_2|: Im tau = {Im_tau_from_eps2}")
print(f"From |eps_3|: Im tau = {Im_tau_from_eps3}")
print(f"K-K Table 5: Im tau = 2.352")

# Now: with the K-K best-fit tau, compute the predicted eps_2, eps_3 numerically
# from full q-expansion.

print("\n" + "=" * 70)
print("Reverse cross-check: from K-K best-fit tau predict eps_2, eps_3")
print("=" * 70)

tau_kk = mp.mpc("0.0361", "2.352")
q = mp.exp(2j * mp.pi * tau_kk)
q_third = q**(mp.mpf(1) / 3)
q_two_thirds = q**(mp.mpf(2) / 3)
eps2_pred = -6 * q_third
eps3_pred = -18 * q_two_thirds
print(f"q = exp(2 pi i tau) = {q}")
print(f"|q| = {abs(q)}")
print(f"eps_2 (predicted) = -6 q^(1/3) = {eps2_pred}")
print(f"eps_3 (predicted) = -18 q^(2/3) = {eps3_pred}")
print(f"K-K eq 59 reports: eps_2 = -0.043 - 0.0033i, eps_3 = -0.00094 - 0.00014i")

# Now: would Re tau = 0 work?
print("\n" + "=" * 70)
print("Could Re tau = 0 (pure imaginary tau_Q) reproduce the CKM?")
print("=" * 70)
# At Re tau = 0, eps_2 and eps_3 are PURELY REAL.
# arg(eps_2) = pi (since negative real), arg(eps_3) = pi.
# Then in K-K eq 64 (theta_23) and eq 63 (theta_13), the phase structure
# becomes purely real. The CP phase delta_q would be zero.
# But K-K Table 5: delta_q = 1.21 pi ~ 218 deg, NOT zero.
# So Re tau = 0 would predict no CP violation, conflict with experiment.

# Let's compute: at Re tau = 0.0361, delta_q comes from arg structure of beta^II.
# The independent verification: with Re tau = 0, the model predicts
# Re tau = 0 is INCOMPATIBLE with non-zero CP phase delta_q.

# Concrete: what is the mapping arg(eps_2) <-> arg(beta^II/beta^I) <-> delta_q?
# K-K eq 62: theta_12 = |2 eps_2 (beta^II/beta^I)|, but the COMPLEX phase of theta_12
# combines with phase of theta_13, theta_23 to give delta_q.

# KEY: K-K's eq 59 explicitly:
#   eps_2 = -6 q^(1/3), so arg(eps_2) = pi + (2 pi /3) Re tau (mod 2pi)
#   eps_3 = -18 q^(2/3), arg(eps_3) = pi + (4 pi /3) Re tau (mod 2pi)
# Re tau = 0 ==> arg(eps_2) = arg(eps_3) = pi exactly.

# delta_q sources: at Re tau = 0, the only complex phases in CKM are the FIT
# phases of beta_u^II, gamma_d^II, etc.
# K-K Table 5 has beta_u^II = 0.2697 - 0.1971i (complex), so even at Re tau = 0,
# delta_q can be non-zero from beta_u^II fit phase.
# But: would the WHOLE fit work?

# This is where chi^2 reoptimization is needed -- doable but complex.
# Instead, let's do the simplest test: fix Re tau = 0 in K-K's framework and
# refit just Im tau for chi^2 minimum at K-K's other params.

# Actually we did that in step 4: chi^2_y(tau=0+i 2.55) was MINIMUM at 0.0008.
# But that ignored the CKM constraint.

# Let's test: at Re tau = 0, with K-K Table 5 alpha,beta,gamma,phi, what are the
# predicted CKM angles AND y-Yukawas?

print()
print("With K-K Table 5 alpha_d, beta_d, gamma_d, phi parameters:")
print("Re tau = 0, varying Im tau:")

# We need a CKM angle predictor.  Simplest: use K-K eq 62-64 (leading order)
# and acknowledge they are only approximate.

# K-K Table 5 inputs:
beta_uI = mp.mpf("-0.1264")
beta_uII = mp.mpc("0.2697", "-0.1971")
gamma_uI = mp.mpf("2.720")  # actually unused for Y_d^III; relevant for Y_u^VI

# Actually the K-K eq 62-64 use beta_u^I, beta_u^II for theta_12 (UP-quark sector),
# and gamma_d^I, gamma_d^II for theta_13 and theta_23 (DOWN-quark sector).

gamma_dI = mp.mpf("0.6253")
gamma_dII = mp.mpc("0.4958", "-0.2187")

ratio_b = beta_uII / beta_uI
factor_g_minus = 1 - gamma_dII / gamma_dI
factor_g_plus = 1 + gamma_dII / gamma_dI

print(f"\n{'Re tau':>10s} {'Im tau':>10s} {'theta_12':>14s} {'theta_13':>14s} {'theta_23':>14s} {'delta_q (deg)':>16s}")
for re_tau in [mp.mpf("0"), mp.mpf("0.018"), mp.mpf("0.0361"), mp.mpf("0.072")]:
    for im_tau_label in ["sqrt(11/2)", "2.352", "sqrt 5", "sqrt 6"]:
        if im_tau_label == "sqrt(11/2)":
            im_tau = mp.sqrt(mp.mpf(11)/2)
        elif im_tau_label == "2.352":
            im_tau = mp.mpf("2.352")
        elif im_tau_label == "sqrt 5":
            im_tau = mp.sqrt(5)
        else:
            im_tau = mp.sqrt(6)
        # Compute eps_2 and eps_3 at this tau (full complex):
        tau = mp.mpc(re_tau, im_tau)
        q_ = mp.exp(2j * mp.pi * tau)
        eps2_ = -6 * q_**(mp.mpf(1)/3)
        eps3_ = -18 * q_**(mp.mpf(2)/3)
        # K-K eq 71 LEADING ORDER:  theta_12 = |2 eps_2 (beta^II/beta^I)|
        # which is |12 q^(1/3)| * |beta^II/beta^I|.  But more precisely:
        th12 = abs(2 * eps2_ * ratio_b)
        th23 = abs(2 * eps2_ * factor_g_plus)
        th13 = abs(eps3_ * factor_g_minus * 4)  # eq 72: |eps3*(2 gamma^II/gamma^I) - 2 eps3| = 2 eps3 |1 - gamma^II/gamma^I|
        # wait: K-K eq 72 reads "theta_13 ~ |2 eps_3 (gamma^I - 2 gamma^II)/gamma^I - 2 eps_3|"
        # actually = 2 eps_3 |1 - gamma^II/gamma^I| -- but the coefficient is 72 not 36.
        # Let me follow eq 72 LITERALLY: theta_13 ~ |eps_2^2 (gamma^I - 2 gamma^II)/gamma^I - 2 eps_3|
        # Actually re-reading: "theta_13 = |Y_u^{3,1}/Y_u^{3,3} - Y_d^{3,1}/Y_d^{3,3}| =
        # |eps_2^2 (gamma^I - 2 gamma^II)/gamma^I - 2 eps_3| = 72 e^(-(4 pi /3) Im tau) |1 - gamma^II/gamma^I|"
        # The 72 = 18 * 2 / |something| we missed; |2 eps_3| = 2*18 = 36 (no 72). Let me just use the analytic K-K formula.
        # Hmm K-K eq 71: "theta_12 ~ |2 eps_2 beta^II/beta^I| = 12 e^(-(2 pi /3) Im tau) |beta^II/beta^I|"
        # 2 * 6 = 12, that's |2 eps_2| * |beta^II/beta^I|, i.e. theta_12 = 2 |eps_2| |ratio| = 12 e^(-...) |ratio|.
        # K-K eq 72: theta_13 = 72 e^(-(4 pi /3) Im tau) |1 - gamma^II/gamma^I|.
        # |2 eps_3| = 36, so where does 72 come from? Looking at eq 72: |eps_2^2 (gamma^I - 2 gamma^II)/gamma^I - 2 eps_3|.
        # Note eps_2^2 ~ 36 e^(-(4 pi /3) Im tau) e^(i (4 pi /3) Re tau), and eps_3 ~ 18 e^(-(4 pi /3) Im tau) e^(i (4 pi /3) Re tau)
        # so eps_2^2 and eps_3 BOTH scale as e^(-(4 pi /3) Im tau)! They have same magnitude order,
        # and we get an interference. Let me just compute LEADING ORDER:
        # theta_13 ~ |eps_2^2 (gamma^I - 2 gamma^II) / gamma^I - 2 eps_3|
        th13_complex = eps2_**2 * (gamma_dI - 2*gamma_dII)/gamma_dI - 2 * eps3_
        th13 = abs(th13_complex)
        # theta_23 ~ |2 eps_2 (gamma^I + gamma^II)/gamma^I| = 12 e^(-(2 pi /3) Im tau)|1 + gamma^II/gamma^I|
        th23_complex = 2 * eps2_ * (1 + gamma_dII/gamma_dI)
        th23 = abs(th23_complex)
        # delta_q from arg combination -- approximate as arg(theta_13_complex) - arg(theta_12_complex * theta_23_complex)
        arg12 = mp.atan2(mp.im(2 * eps2_ * ratio_b), mp.re(2 * eps2_ * ratio_b))
        arg13 = mp.atan2(mp.im(th13_complex), mp.re(th13_complex))
        arg23 = mp.atan2(mp.im(th23_complex), mp.re(th23_complex))
        delta_q = (arg13 - arg12 - arg23)
        delta_q_deg = float(delta_q * 180 / mp.pi)
        # bring to (0, 360)
        while delta_q_deg < 0:
            delta_q_deg += 360
        while delta_q_deg > 360:
            delta_q_deg -= 360
        print(f"{mp.nstr(re_tau, 6):>10s} {mp.nstr(im_tau, 8):>10s} {mp.nstr(th12, 5):>14s} {mp.nstr(th13, 5):>14s} {mp.nstr(th23, 5):>14s} {delta_q_deg:>14.2f}")

print()
print("Targets (K-K Table 5):")
print(f"  theta_12 = 0.227,   theta_13 = 0.00314,  theta_23 = 0.0358,  delta_q = 218 deg (= 1.21 pi)")
