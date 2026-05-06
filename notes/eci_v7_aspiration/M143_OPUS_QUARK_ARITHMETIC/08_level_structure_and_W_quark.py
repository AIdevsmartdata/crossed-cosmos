#!/usr/bin/env python3
"""
M143 / Step 8 -- Level structure for K-K A_4 model and search for a quark
analog W^Q with structural double-zero at tau_Q.

K-K uses Gamma(3) (modular level 3, A_4 = SL(2,Z)/Gamma(3)).
The fundamental domain of Gamma(3) is bigger than F_SL(2,Z); specifically
[Gamma(3) : SL(2,Z)] = 24 (NOT 12 because Gamma vs PGamma),
or rather index of P-Gamma(3) in PSL(2,Z) is 12.

Atkin-Lehner-like involutions on X(3) and Hauptmoduls:
  X(3) is genus 0 with 4 cusps {0, 1, 2, infty}.
  Its Hauptmodul (uniformizer) can be chosen as the cube root of j/(j-1728), or
  as the eta-quotient h_3 = (eta(tau)/eta(3 tau))^12 / 27 - 1 ratio.

For Gamma_0(N), N=2,3,4,11, the involution w_N = ((0,-1),(N,0)) has fixed point
i/sqrt(N), reduced to F_SL(2,Z) by S as i sqrt(N).

Gamma_0(11) is *interesting* because:
  - X_0(11) has GENUS 1, with j-invariant being a rational function of t (Hauptmodul).
  - The CM points of X_0(11) include i sqrt(11/?) values.
  - The unique elliptic curve E_11 = "y^2 + y = x^3 - x^2 - 10x - 20" has w_11 acting.
  - But the AL FIXED POINT of w_11 on X_0(11) is at i/sqrt(11) = 0.302 i (in F: i sqrt 11 = 3.317 i).

X_0(N) AL fixed point of w_N at i/sqrt(N) reduced via S to i sqrt(N).
None of i sqrt(N) for N in {2..11} matches Im=2.352 within 1%, except none.

But there's another structure: AL fixed points of w_N COMBINED with Gamma_0(N) cosets.

For Gamma_0(11), the FULL set of CM points coming from elliptic curves with
CM by orders of conductor f in Q(sqrt -1), Q(sqrt -2), etc., includes:

  D = -7  (conductor 1):  tau = (1 + i sqrt 7)/2 in F.
  D = -11 (conductor 1):  tau = (1 + i sqrt 11)/2.
  D = -3 conductor 11:    tau = (11 + i sqrt 3)/2 ?
  More generally complex CM points with D = -d, conductor f have Im tau = (f/d) sqrt d.

The K-K Im tau ~ 2.35 doesn't match any conductor-1 CM in Q(sqrt -d) for small d.

Let me NOW try to search the LMFDB-style table of CM points with  Im tau in [2.3, 2.4]:
  CM j values are real and integer (for h(K) = 1) or algebraic of degree h(K).

  Class h(K) = 1:  j(tau) integer.
  Class h(K) = 2:  j roots of (t-j_1)(t-j_2) over Q.
  Class h(K) = 3:  cubic number, etc.

Im tau in [2.3, 2.4] from h(K) = 2:
   Q(sqrt -22):  d=22, tau = i sqrt 22 has Im sqrt 22 = 4.69 (too high)
                or (1+i sqrt 22)/2 has Im sqrt 22 / 2 = 2.345!  YES!
   Q(sqrt -22), d=22: NORMALIZED tau = (1 + i sqrt 22)/2.
     Im tau = sqrt(22)/2 = sqrt(11/2) = 2.3452!
     d = 22 mod 4 = 2 mod 4, but for non-fundamental discriminants we have D = -88 actually
     check: 22 = 2 * 11, and 22 mod 4 = 2, so the discriminant of Q(sqrt -22) is -88
     (since 22 = 2 mod 4). Class number h(-88) = ?

Actually NO -- for d non-square-free or with d % 4 in {1, 2}, discriminant differs:
  Q(sqrt -d), d square-free, fundamental disc:
     d = 1, 2 mod 4:  D_K = -4 d.  E.g. d=22 (22 mod 4 = 2), D_K = -88.  h(-88) = 2.
     d = 3 mod 4:    D_K = -d.   E.g. d=23, D_K = -23.  h(-23) = 3.

  So Q(sqrt -22) has discriminant -88, class number h(-88) = 2.
  CM points: tau = i sqrt 22 (= D_K/2 sqrt | D_K|/2 in some norm...) No.
  Actually for D_K = -88, CM points are (b + sqrt(-88))/(2a) for ax^2 + bxy + cy^2
  with b^2 - 4ac = -88, gcd(a,b,c)=1, |b| <= a <= c.
  a=1, b=0, c=22: tau = i sqrt 88 / 2 = i sqrt 22 = 2 i sqrt 22 / 2 = i sqrt 22.
                 Wait: (0 + sqrt(-88))/2 = i sqrt 88 / 2 = i (2 sqrt 22)/2 = i sqrt 22.
                 Im = sqrt 22 = 4.69. Not 2.35.
  a=2, b=2, c=12: discriminant = 4 - 96 = -92. NO.
  Try a=2, b=0, c=11: disc = -88. tau = i sqrt 88 / (2*2) = i sqrt 22 / 2 = 2.345!  YES.
  Class number of -88 is 2; reps are tau_1 = i sqrt 22 (a=1), tau_2 = i sqrt(22)/2 (a=2).

  So tau_2 = i sqrt 22 / 2 = i sqrt(11/2) IS A CM POINT of Q(sqrt -22)!!!!

Let me verify by computing j(i sqrt(22)/2) numerically and checking if it matches one
of the two roots of the Hilbert class polynomial H_{-88}(X).

H_{-88}(X) = X^2 - a X + b for some integers a, b.
Looking up: h(-88) = 2.  The j-invariants for D=-88 are
  j_1 + j_2 = ?  j_1 * j_2 = ?
"""

import mpmath as mp

mp.mp.dps = 50

N_TERMS = 400


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
        sig = sum(d**3 for d in range(1, n + 1) if n % d == 0)
        s += sig * q**n
    return 1 + 240 * s


def E6(tau):
    q = mp.exp(2j * mp.pi * tau)
    s = mp.mpc(0, 0)
    for n in range(1, N_TERMS):
        sig = sum(d**5 for d in range(1, n + 1) if n % d == 0)
        s += sig * q**n
    return 1 - 504 * s


def j_inv(tau):
    e4 = E4(tau)
    e6 = E6(tau)
    Delta_ = (e4**3 - e6**2) / 1728
    return e4**3 / Delta_


print("=" * 70)
print("CRITICAL TEST: is tau = i sqrt(22)/2 a CM point of Q(sqrt -22)?")
print("=" * 70)

# CM point candidates for D = -88
tau_cm_a1 = 1j * mp.sqrt(22)
tau_cm_a2 = (1j * mp.sqrt(22)) / 2  # This is what we care about

# Also (a=2, b=2, c=12 not valid as we saw); but for D=-88, h=2 we have only 2 forms:
# (1, 0, 22) and (2, 0, 11), giving tau = (0 + sqrt(-88))/(2a)
# tau_1 = i sqrt 88 / 2 = i sqrt 22 (Im = 4.690)
# tau_2 = i sqrt 88 / 4 = i sqrt 22 / 2 = i sqrt 5.5 = i sqrt(11/2)  (Im = 2.345)

# Verify class number h(-88) = 2 by direct counting of binary quadratic forms.
# Forms of disc -88: a x^2 + b xy + c y^2 with b^2 - 4ac = -88, |b|<=a<=c, gcd=1.
# b even (since disc = -88 = 0 mod 4): b in {0, +-2, +-4, ...}
# a = 1: b = 0, c = 22. valid. (1, 0, 22)
# a = 2: b = 0, c = 11. valid. (2, 0, 11)
# a = 2: b = 2, c = (4+88)/8 = 11.5 -- not integer.
# a = 3: b = 0, c = 88/12, not integer; b = 2, c = (4+88)/12, not integer; b = +-2 -> 88+4 = 92, /12 no.
# a = 4: b = 0, c = 88/16 no; b = +-2, c = 92/16 no; b = +-4, c = 104/16 no.
# Total: 2 forms => h(-88) = 2.  YES, confirmed.

print("\nClass number h(-88) = 2 (verified by binary form enumeration).")
print(f"Two CM j-invariants for D=-88:")
print(f"  tau_1 = i sqrt 22 = {tau_cm_a1}")
print(f"  tau_2 = i sqrt(22)/2 = {tau_cm_a2}")

j_1 = j_inv(tau_cm_a1)
j_2 = j_inv(tau_cm_a2)

print(f"\nj(tau_1) = {j_1}")
print(f"j(tau_2) = {j_2}")
print(f"\nImaginary parts:")
print(f"  Im j(tau_1) = {mp.im(j_1)}")
print(f"  Im j(tau_2) = {mp.im(j_2)}")
print(f"\n(Both should be REAL since CM points are SL(2,Z)-equivalent to F-rep on imaginary axis)")
print(f"Both should be ALGEBRAIC INTEGERS satisfying H_{-88}(j) = 0.")

# H_{-88}(X) = X^2 - aX + b. Compute a = j_1 + j_2 and b = j_1 j_2.
sum_j = j_1 + j_2
prod_j = j_1 * j_2
print(f"\nj_1 + j_2 = {sum_j}")
print(f"j_1 * j_2 = {prod_j}")

# Round to integers if possible:
sum_j_re = mp.re(sum_j)
prod_j_re = mp.re(prod_j)
sum_j_int = mp.nint(sum_j_re)
prod_j_int = mp.nint(prod_j_re)
print(f"\nNearest integer values:")
print(f"  round(j_1 + j_2) = {sum_j_int},  diff = {mp.nstr(sum_j_re - sum_j_int, 5)}")
print(f"  round(j_1 * j_2) = {prod_j_int},  diff = {mp.nstr(prod_j_re - prod_j_int, 5)}")

if abs(sum_j_re - sum_j_int) < mp.mpf("1e-10") and abs(prod_j_re - prod_j_int) < mp.mpf("1e-10"):
    print(f"\n>>> H_{{-88}}(X) = X^2 - ({sum_j_int}) X + ({prod_j_int}) = 0  (Hilbert class polynomial)")
    print(f"\nThis CONFIRMS tau_2 = i sqrt(11/2) IS A CM POINT of Q(sqrt -22), discriminant -88, h=2.")
else:
    print("\n>>> WARNING: numerical precision insufficient or NOT a CM point.")

# Also: distance from K-K Im tau = 2.352 to sqrt(11/2):
print()
print(f"K-K Im tau = 2.352 vs sqrt(11/2) = {mp.sqrt(mp.mpf(11)/2)}")
print(f"  diff = {mp.mpf('2.352') - mp.sqrt(mp.mpf(11)/2)}")
print(f"  relative = {abs(mp.mpf('2.352') - mp.sqrt(mp.mpf(11)/2)) / mp.sqrt(mp.mpf(11)/2) * 100}% (within ~0.3%)")

# Compare to the K-K experimental error budget:
print(f"\nK-K experimental Im tau pinning ~ 0.003 (1-sigma from theta_12)")
print(f"Distance to sqrt(11/2) = 0.0068 = ~2.3 sigma")
print(f"So sqrt(11/2) lies just outside 2-sigma of K-K's central value 2.352.")
print(f"NOT ruled out at 3-sigma; tension at 2.3-sigma.")
