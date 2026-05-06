#!/usr/bin/env python3
"""
M143 / Step 5 -- Use K-K eq 62 (Cabibbo angle theta_12) to pin Im tau more
precisely than the y_d/y_s/y_b scan.

K-K eq 62:  theta_12 ~ 12 exp(-(2pi/3) Im(tau)) * |beta_u^II/beta_u^I|

K-K Table 5 inputs: beta_u^I = -0.1264, beta_u^II = 0.2697 - 0.1971i
K-K Table 5 output: theta_12^q = 13.027 deg = 0.227 rad

Solve for Im tau and check whether i sqrt(N) for any N matches.
"""

import mpmath as mp

mp.mp.dps = 30


# K-K Table 5 inputs:
beta_I = mp.mpf("-0.1264")
beta_II = mp.mpc("0.2697", "-0.1971")
ratio_beta = beta_II / beta_I
abs_ratio = abs(ratio_beta)
print(f"|beta^II / beta^I| = {abs_ratio}")

# K-K Table 5 output:  theta_12^q = 0.227 rad (= 13.027 deg).
theta_12 = mp.mpf("0.227")

# K-K eq 62:  theta_12 = 12 exp(-(2pi/3) Im(tau)) * |beta_u^II/beta_u^I|
# So:  exp(-(2pi/3) Im(tau)) = theta_12 / (12 * |beta^II/beta^I|)
# Im(tau) = -(3/(2 pi)) ln(theta_12 / (12 * abs_ratio))

Im_tau_from_th12 = -(3 / (2 * mp.pi)) * mp.log(theta_12 / (12 * abs_ratio))
print(f"\nFrom K-K eq 62 (theta_12 = 12 exp(-(2pi/3) Im(tau)) |beta^II/beta^I|):")
print(f"  Im(tau) = {Im_tau_from_th12}")
print(f"  Reference K-K Table 5: Im(tau) = 2.352")
print(f"  Relative discrepancy: {abs(Im_tau_from_th12 - mp.mpf('2.352')) / mp.mpf('2.352')}")

# Same for theta_23 (eq 64).  K-K Table 5: theta_23^q = 0.0358 rad
gamma_I = mp.mpf("0.6253")
gamma_II = mp.mpc("0.4958", "-0.2187")
ratio_gamma = gamma_II / gamma_I
factor_gamma = abs(1 + ratio_gamma)
print(f"\n|1 + gamma^II/gamma^I| = {factor_gamma}")
theta_23 = mp.mpf("0.0358")  # K-K Table 5 output

Im_tau_from_th23 = -(3 / (2 * mp.pi)) * mp.log(theta_23 / (12 * factor_gamma))
print(f"From K-K eq 64 (theta_23 = 12 exp(-(2pi/3) Im(tau)) |1 + gamma^II/gamma^I|):")
print(f"  Im(tau) = {Im_tau_from_th23}")

# Same for theta_13 (eq 63).  K-K Table 5: theta_13^q = 0.00314 rad
factor_th13 = abs(1 - gamma_II / gamma_I)
print(f"\n|1 - gamma^II/gamma^I| = {factor_th13}")
theta_13 = mp.mpf("0.00314")

# theta_13 = 72 exp(-(4pi/3) Im(tau)) |1 - gamma^II/gamma^I|
# Im(tau) = -(3/(4 pi)) ln(theta_13 / (72 * factor_th13))
Im_tau_from_th13 = -(3 / (4 * mp.pi)) * mp.log(theta_13 / (72 * factor_th13))
print(f"From K-K eq 63 (theta_13 = 72 exp(-(4pi/3) Im(tau)) |1 - gamma^II/gamma^I|):")
print(f"  Im(tau) = {Im_tau_from_th13}")

print("\n" + "=" * 70)
print("CKM-pinned Im tau values for K-K Table 5 best-fit:")
print(f"  theta_12  --> Im tau = {mp.nstr(Im_tau_from_th12, 8)}")
print(f"  theta_23  --> Im tau = {mp.nstr(Im_tau_from_th23, 8)}")
print(f"  theta_13  --> Im tau = {mp.nstr(Im_tau_from_th13, 8)}")
print(f"  K-K Table 5 reports Im tau = 2.352")
print("=" * 70)

# Each of theta_ij yields its own Im tau; consistency is the K-K fit.
# Now: how close is Im tau = 2.352 to special CM values?

print("\nSpecial Im tau values (CM/AL or square-root rationals):")
candidates = [
    ("sqrt(5) = i sqrt 5  Q(sqrt-5) h=2", mp.sqrt(5)),
    ("sqrt(11/2) (no-CM)", mp.sqrt(mp.mpf(11)/2)),
    ("sqrt(6) = i sqrt 6  Q(sqrt-6) h=2", mp.sqrt(6)),
    ("sqrt(43)/sqrt(8)", mp.sqrt(mp.mpf(43)/8)),
    ("sqrt(28)/sqrt(5)", mp.sqrt(mp.mpf(28)/5)),
    ("sqrt(33)/sqrt(6)", mp.sqrt(mp.mpf(33)/6)),
    ("sqrt(11/2)*1.003", mp.sqrt(mp.mpf(11)/2)*mp.mpf("1.003")),
]
for label, x in candidates:
    diff = mp.mpf("2.352") - x
    print(f"  {label}: {mp.nstr(x, 12)}  diff to 2.352 = {mp.nstr(diff, 4)}")

# Importantly, what does Im tau = sqrt(11/2) PREDICT for theta_12?
print("\n" + "=" * 70)
print("Reverse: predict theta_ij at i sqrt(11/2):")
Im_test = mp.sqrt(mp.mpf(11)/2)
th12_pred = 12 * mp.exp(-(2*mp.pi/3) * Im_test) * abs_ratio
th23_pred = 12 * mp.exp(-(2*mp.pi/3) * Im_test) * factor_gamma
th13_pred = 72 * mp.exp(-(4*mp.pi/3) * Im_test) * factor_th13
print(f"  Im tau = sqrt(11/2) = {Im_test}")
err12 = float(abs(th12_pred-mp.mpf("0.227"))/mp.mpf("0.227")*100)
err23 = float(abs(th23_pred-mp.mpf("0.0358"))/mp.mpf("0.0358")*100)
err13 = float(abs(th13_pred-mp.mpf("0.00314"))/mp.mpf("0.00314")*100)
print(f"  predicted theta_12 = {mp.nstr(th12_pred, 6)}  (target 0.227)  err = {err12:.2f}%")
print(f"  predicted theta_23 = {mp.nstr(th23_pred, 6)}  (target 0.0358) err = {err23:.2f}%")
print(f"  predicted theta_13 = {mp.nstr(th13_pred, 6)}  (target 0.00314) err = {err13:.2f}%")

# Same for sqrt 5 and sqrt 6 (the CM points):
for label, Im_test in [("sqrt 5  Q(sqrt-5)", mp.sqrt(5)),
                        ("sqrt 6  Q(sqrt-6)", mp.sqrt(6))]:
    th12_pred = 12 * mp.exp(-(2*mp.pi/3) * Im_test) * abs_ratio
    th23_pred = 12 * mp.exp(-(2*mp.pi/3) * Im_test) * factor_gamma
    th13_pred = 72 * mp.exp(-(4*mp.pi/3) * Im_test) * factor_th13
    err12 = float(abs(th12_pred-mp.mpf("0.227"))/mp.mpf("0.227")*100)
    err23 = float(abs(th23_pred-mp.mpf("0.0358"))/mp.mpf("0.0358")*100)
    err13 = float(abs(th13_pred-mp.mpf("0.00314"))/mp.mpf("0.00314")*100)
    print(f"\n  Im tau = {label}, value = {mp.nstr(Im_test, 8)}")
    print(f"  predicted theta_12 = {mp.nstr(th12_pred, 6)}, err = {err12:.1f}%")
    print(f"  predicted theta_23 = {mp.nstr(th23_pred, 6)}, err = {err23:.1f}%")
    print(f"  predicted theta_13 = {mp.nstr(th13_pred, 6)}, err = {err13:.1f}%")

# Conclusion: Im tau is exponentially pinned by CKM angles.
# We expect about a 1-2% pinning resolution from each of theta_12, theta_23.

print("\n" + "=" * 70)
print("PRECISION OF Im(tau) PINNING (treating coefficients as O(1) free):")
print("Each percent error in theta_12 corresponds to delta Im(tau) =")
print(f"  3/(2 pi) * 1% = {float(3/(2 * mp.pi) * 0.01):.4f}  ~ 0.005")
print()
print("So a 1% uncertainty on theta_12 gives 0.005 uncertainty on Im(tau).")
print(f"K-K experimental theta_12^q error (Table 5 input): 0.0814 deg = 0.00142 rad => 0.00142/0.227 = 0.6%")
print(f"Implied delta Im(tau) ~= 0.6% * 3/(2 pi) ~ 0.003")
print()
print(f"K-K's Im tau = 2.352 +/- ~0.003 (CKM-pinned).")
print(f"Distance to i sqrt(11/2) = 2.345: {abs(mp.mpf('2.352') - mp.sqrt(mp.mpf(11)/2))} = ~0.007 (~2-sigma)")
print(f"Distance to i sqrt 5     = 2.236: {abs(mp.mpf('2.352') - mp.sqrt(5))} = ~0.116 (>30-sigma!)")
print(f"Distance to i sqrt 6     = 2.449: {abs(mp.mpf('2.352') - mp.sqrt(6))} = ~0.097 (>30-sigma!)")
print()
print("==> sqrt 5, sqrt 6 (h=2 CM) are RULED OUT at ~30-sigma by CKM angle precision.")
print("==> sqrt(11/2) is at ~2-sigma; can't rule out, can't claim either.")
print()
print("BUT: the |beta^II/beta^I| coefficient is itself a fit parameter,")
print("so the absolute prediction has an O(1) prefactor uncertainty -- the")
print("'Im tau pinning' is conditional on the fit choice of these coefs.")
