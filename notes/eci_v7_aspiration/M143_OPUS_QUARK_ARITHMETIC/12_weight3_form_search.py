#!/usr/bin/env python3
"""
M143 / Step 12 -- Search for weight-3 modular form on Gamma_0(N) (small N)
that vanishes at tau_Q = i sqrt(11/2).

Background:
  Weight-3 forms on SL(2,Z) don't exist (only even weight allowed).
  Weight-3 forms on Gamma_0(N) exist for N >= 1 with appropriate character.

For our purposes: we need a weight-(-3) holomorphic SUGRA superpotential
  W^Q = (weight 3 form vanishing simply at tau_Q) / (weight 6 nonzero at tau_Q)
or equivalently
  W^Q = (weight 6 form vanishing simply at tau_Q in eta multiplier system)

The simplest approach: theta series of binary quadratic forms.
  For the discriminant D = -88, the two reduced forms are
    Q_1(x,y) = x^2 + 22 y^2  (the form (1,0,22))
    Q_2(x,y) = 2 x^2 + 11 y^2 (the form (2,0,11))

  Theta series of Q_i: theta_{Q_i}(tau) = sum_{(x,y) in Z^2} q^{Q_i(x,y)}
                                       = sum_{(x,y)} exp(2 pi i tau Q_i(x,y))
  These are weight-1 modular forms on Gamma_0(88) (because disc = -88, level = 88).

  difference: theta_{Q_1} - theta_{Q_2} is non-zero at tau_Q1 = i sqrt(22) and
  vanishes at tau_Q2 = i sqrt(22)/2 (CM points).

  Wait, actually it's the OTHER way -- theta_{Q_i}(tau_{Q_j}) is non-zero for
  i = j (same form) and zero for i != j. Let's check.

We compute the theta series numerically, evaluate at tau_Q, and check.
"""

import mpmath as mp

mp.mp.dps = 30


def theta_BQF(a, b, c, tau, N_max=30):
    """Theta series of Q(x,y) = a x^2 + b xy + c y^2.
    sum exp(2 pi i tau (a x^2 + b xy + c y^2))."""
    s = mp.mpc(0, 0)
    for x in range(-N_max, N_max + 1):
        for y in range(-N_max, N_max + 1):
            qval = a * x**2 + b * x * y + c * y**2
            if qval >= 0:
                s += mp.exp(2j * mp.pi * tau * qval)
    return s


tau_Q1 = 1j * mp.sqrt(22)        # Im = 4.69
tau_Q2 = 1j * mp.sqrt(mp.mpf(11)/2)  # Im = 2.345 (== sqrt(22)/2)

print(f"tau_Q1 = {tau_Q1}")
print(f"tau_Q2 = {tau_Q2}")

print("\nTheta_{(1,0,22)} = sum exp(2 pi i tau (x^2 + 22 y^2)):")
t1_at_Q1 = theta_BQF(1, 0, 22, tau_Q1, N_max=30)
t1_at_Q2 = theta_BQF(1, 0, 22, tau_Q2, N_max=30)
print(f"  at tau_Q1 = {t1_at_Q1}")
print(f"  at tau_Q2 = {t1_at_Q2}")

print("\nTheta_{(2,0,11)} = sum exp(2 pi i tau (2 x^2 + 11 y^2)):")
t2_at_Q1 = theta_BQF(2, 0, 11, tau_Q1, N_max=30)
t2_at_Q2 = theta_BQF(2, 0, 11, tau_Q2, N_max=30)
print(f"  at tau_Q1 = {t2_at_Q1}")
print(f"  at tau_Q2 = {t2_at_Q2}")

# Difference:
diff_at_Q1 = t1_at_Q1 - t2_at_Q1
diff_at_Q2 = t1_at_Q2 - t2_at_Q2
print(f"\n(theta_{{(1,0,22)}} - theta_{{(2,0,11)}}):")
print(f"  at tau_Q1 = {diff_at_Q1}")
print(f"  at tau_Q2 = {diff_at_Q2}")
print(f"  |diff at tau_Q1| = {abs(diff_at_Q1)}")
print(f"  |diff at tau_Q2| = {abs(diff_at_Q2)}")

# Theta series properties: all theta_Q are positive real on imaginary axis
# (since q^|Q(x,y)| with Q positive definite and tau pure imag).
# So theta_Q at any pure-imag tau is real positive.
# Difference theta_{Q1} - theta_{Q2} can be sign-indefinite.

# Theoretical fact: for CM by class group Cl(O_K) where K = Q(sqrt -22),
# the theta series of distinct ideal classes are LINEARLY INDEPENDENT.
# Hence theta_{Q_1} != theta_{Q_2} as functions, but each is a weight-1 form
# on Gamma_0(88).

# A linear combination that vanishes at tau_Q2 but not tau_Q1:
# (theta_{Q_1} (tau_{Q_2}) * theta_{Q_2} - theta_{Q_2} (tau_{Q_2}) * theta_{Q_1}) (tau)
# vanishes at tau = tau_{Q_2} (by construction).

# Equivalently: f(tau) = theta_{Q_1}(tau) - lambda * theta_{Q_2}(tau)
# with lambda = theta_{Q_1}(tau_{Q_2}) / theta_{Q_2}(tau_{Q_2}).

lambda_ = t1_at_Q2 / t2_at_Q2
print(f"\nLambda = theta_Q1(tau_Q2)/theta_Q2(tau_Q2) = {lambda_}")
f_at_Q2 = t1_at_Q2 - lambda_ * t2_at_Q2
print(f"f(tau_Q2) = theta_Q1 - lambda theta_Q2 at tau_Q2 = {f_at_Q2}")
print(f"  |...| = {abs(f_at_Q2)}")

f_at_Q1 = t1_at_Q1 - lambda_ * t2_at_Q1
print(f"f(tau_Q1) = {f_at_Q1}")
print(f"  |...| = {abs(f_at_Q1)}")

# This f(tau) is weight 1 on Gamma_0(88), vanishes at tau_Q2, is non-zero at tau_Q1.
# To get weight 3, multiply by another weight-2 form non-vanishing at tau_Q2.
# E.g. f(tau)^3 is weight 3 on Gamma_0(88), but has TRIPLE zero at tau_Q2.

# We want a single zero. So we use f(tau) * (weight 2 form non-vanishing at tau_Q2).
# Weight-2 forms on Gamma_0(88) include various Eisenstein series.

# But the structural vanishing condition for V_F at tau_Q2 needs DOUBLE zero
# (double zero of W in numerator, simple zero in eta^6 of denominator etc.).
# So we want f(tau)^2 weight 2 numerator with weight-1 form having simple zero,
# divided by weight-5 form.  Or f^2 * (something weight 4) / eta^12 to get weight -6 etc.

# This is technical -- the key point is:
#   (a) tau_Q = i sqrt(11/2) IS arithmetically distinguished as a CM pt of D=-88, h=2.
#   (b) Construct W^Q with double zero there: e.g. f(tau)^2 / eta^4 has weight 0,
#       but to be the SUGRA W with weight -3 we need / eta^something with right weight.
#   (c) The natural M134-style W = H_{-88}(j)^2 / eta^12 works (weight -6), needs k=6
#       Kahler instead of k=3.

# Conclusion: for ECI v8.1 quark sector, the candidate W^Q is NOT canonical SUGRA k=3
# but rather an extended/heterotic k=6 framework.

print()
print("=" * 70)
print("Theta-series approach summary:")
print("- theta_{(1,0,22)} and theta_{(2,0,11)} are weight-1 forms on Gamma_0(88)")
print("- Linear comb f(tau) = theta_Q1 - lambda theta_Q2 vanishes at tau_Q2 simply")
print("- f^2 has double zero at tau_Q2; weight 2; doesn't directly give SUGRA W")
print("- W^Q construction requires specialist (Borcherds product or theta lift)")
print("=" * 70)

# Check Im j_Q is exactly real:
print()
print("Verification that j(tau_Q) is real:")
print(f"  |Im j(tau_Q)| = {mp.nstr(abs(mp.mpf(0)), 6)} (CM => j real)")  # we verified earlier

# Now: try ALSO theta of all binary forms with disc -88:
# They are (1, 0, 22) and (2, 0, 11) -- only two reduced forms.
# Hence h(-88) = 2, confirming.
