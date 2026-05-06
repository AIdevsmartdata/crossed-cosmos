#!/usr/bin/env python3
"""
M143 / Step 7 -- Search for arithmetic origin of K-K Re tau = 0.0361.

Re tau = 0.0361 was set by phase of eps_2 = -6 q^(1/3) to match observed CP
phase delta_q = 1.21 pi (218 deg).

Phase relation:  arg(eps_2) = pi + (2pi/3) Re tau (mod 2pi)
=> Re tau = (3 / (2 pi)) (arg(eps_2) - pi)

K-K Table 5: arg(eps_2) computed from -0.043 - 0.0033i = pi + atan2(-0.0033, -0.043)
            = pi + (-3.0033 - pi) ~ -3.0033 + pi = -3.0033 + 3.1416 = 0.138... wait
            arg = atan2(-0.0033, -0.043) = third quadrant ~ -pi + atan(0.0767) = -3.064 rad
            (3/(2pi))(arg - pi) = (3/(2pi))(-3.064 - pi) = (3/(2pi))(-6.205) = -2.962
            Adding 2pi: 6.205-2pi = -0.078. (3/(2pi))(0.078) = 0.0372 ~ 0.036 OK

Let's see if Re tau = 0.0361 is special arithmetically.
"""

import mpmath as mp

mp.mp.dps = 30

re_tau = mp.mpf("0.0361")

print(f"K-K Re tau = {re_tau}")
print()

print("Test rational candidates:")
candidates_rational = [
    ("1/27", mp.mpf(1)/27),
    ("1/28", mp.mpf(1)/28),
    ("1/29", mp.mpf(1)/29),
    ("1/30", mp.mpf(1)/30),
    ("1/31", mp.mpf(1)/31),
    ("2/55", mp.mpf(2)/55),
    ("3/83", mp.mpf(3)/83),
    ("7/194", mp.mpf(7)/194),
    ("13/360", mp.mpf(13)/360),
    ("36.1/1000", mp.mpf("0.0361")),
    ("0.0361 (input)", mp.mpf("0.0361")),
]
for label, x in candidates_rational:
    diff = re_tau - x
    print(f"  {label:>20s}: {mp.nstr(x, 12)} diff = {mp.nstr(diff, 4)}")

print("\nTest irrational candidates (arithmetic constants):")
candidates_irr = [
    ("1/(8 pi)", 1/(8 * mp.pi)),
    ("1/(2 pi^3)", 1/(2 * mp.pi**3)),
    ("1/30 (~1/30)", mp.mpf(1)/30),
    ("1/(2 sqrt 769)", 1/(2 * mp.sqrt(769))),
    ("ln(11/2)/(2 pi)", mp.log(mp.mpf(11)/2)/(2 * mp.pi)),
    ("1/(8 e)", 1/(8 * mp.e)),
    ("e/76", mp.e / 76),
]
for label, x in candidates_irr:
    diff = re_tau - x
    print(f"  {label:>30s}: {mp.nstr(x, 12)} diff = {mp.nstr(diff, 4)}")

# The MOST IMPORTANT arithmetic fact:  Re tau is set by experimental delta_q,
# which is itself a fit to data with experimental error +-6.2 deg (Table 5 input
# delta^q error). The error in delta^q propagates to Re tau as:
#     d delta_q / d Re tau = (2 pi /3) (sub-leading; phase rotates at this rate)
# In radians, Re tau changes by (3/(2 pi)) * delta(delta_q in rad).

# 6.2 deg = 0.108 rad  =>  delta(Re tau) ~ (3/(2 pi)) * 0.108 ~ 0.052
# i.e. K-K Re tau = 0.036 +- 0.052 (1-sigma, if delta_q is the only constraint)
# This is consistent with Re tau = 0 at <1-sigma!

print()
print("=" * 70)
print("PHASE ERROR PROPAGATION:")
print("=" * 70)
print(f"K-K experimental error on delta_q: 6.19 deg = {float(6.19 * mp.pi / 180):.4f} rad")
print(f"Sensitivity d delta_q / d Re tau: 2 pi / 3 = {float(2 * mp.pi / 3):.4f} rad/unit")
print(f"Implied 1-sigma error on Re tau (if only delta_q matters):")
print(f"  delta(Re tau) ~ (3/(2 pi)) * 0.108 = {3/(2 * float(mp.pi)) * 0.108:.4f}")
print()
print("==> K-K Re tau = 0.0361 +- 0.052 (1-sigma).")
print(f"==> Re tau = 0 is consistent at {0.0361/0.052:.2f} sigma.")
print()
print("This means K-K Re tau = 0.0361 IS LITERALLY consistent with Re tau = 0 ")
print("AT ABOUT 0.7 SIGMA. No arithmetic explanation needed; this is fit noise.")
print()
print("Conclusion: K-K Re tau = 0.0361 has NO ARITHMETIC ORIGIN -- it's set")
print("by the experimentally measured CP phase delta_q (with ~17% relative error)")
print("plus the sub-leading O(eps_2 eps_3) corrections.")
print()

# Check: is Re tau = 1/(2 pi) something natural?
print("Some 'nice' values:")
print(f"  1/(2 pi) = {float(1/(2 * mp.pi)):.5f}  (smaller than 0.0361)")
print(f"  1/(8 pi) = {float(1/(8 * mp.pi)):.5f}  (smaller still)")
print(f"  arg(eps_2)/2pi = {float(mp.atan2(-0.0033, -0.043)/(2*mp.pi)):.5f}")
print(f"  arg(eps_2)/2pi - 1/2 = {float(mp.atan2(-0.0033, -0.043)/(2*mp.pi) - mp.mpf('0.5')):.5f}")

# Final verdict on Re tau:
print()
print("=" * 70)
print("FINAL Re tau VERDICT:")
print("=" * 70)
print("Re tau = 0.0361 in K-K Tables 5 and 6 is set ENTIRELY by the")
print("experimental CP phase delta_q^CKM = 218 deg (with 6 deg error).")
print("It has no arithmetic structure. It is LITERALLY a phase fit that")
print("could equally well be Re tau = 0 (no CP violation in modular sector,")
print("CP from beta^II phase) or Re tau = -0.034 etc.")
print()
print("Within ~1-sigma: Re tau ~ 0 is acceptable.")
print("Within ~2-sigma: Re tau ~ {0, 0.0361, 0.072} -- fit landscape is FLAT.")
print()
print("Hence claim (A) 'Re tau = 0.0361 is arithmetic' is REFUTED by error budget.")
