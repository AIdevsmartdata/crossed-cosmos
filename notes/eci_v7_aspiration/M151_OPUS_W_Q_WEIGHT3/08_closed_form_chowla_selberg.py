#!/usr/bin/env python3
"""
M151 / Step 8 -- CLOSED FORM via Chowla-Selberg for tau_Q = i sqrt(11/2).

Chowla-Selberg formula for K = Q(sqrt -d), discriminant D_K = -d (d square-free, d ≡ 3 mod 4)
or D_K = -4d (d square-free, d ≡ 1, 2 mod 4):

  prod_{tau in CM} eta(tau)^{w_K} (Im tau)^{1/4} = some explicit Gamma-product
  involving Gamma(n/|D_K|) with n in (Z/|D_K|)* weighted by chi_{D_K}.

Specifically: for K imaginary quadratic with discriminant D, class number h, w units,
  prod_{[a]} (Im tau_a) |eta(tau_a)|^4 = (1/(4 pi sqrt|D|)) prod_{n=1}^{|D|-1} Gamma(n/|D|)^{chi(n)}
  taken over the h CM equivalence classes [a].

For D = -88, h = 2, w = 2. The two CM points are tau_Q and tau_Q1.

Chowla-Selberg gives:
  Im(tau_Q) Im(tau_Q1) * |eta(tau_Q)|^4 |eta(tau_Q1)|^4
    = (1/(4 pi sqrt 88))^h * prod_{n=1}^{87} Gamma(n/88)^{chi_{-22}(n)}

For h=2, the FULL product version:
  (Im tau_Q * Im tau_Q1) * |eta(tau_Q) eta(tau_Q1)|^4
    = factor * prod Gamma(n/88)^chi(n)

OR, by the explicit Chowla-Selberg formula (1949):
  prod_{[a] in Cl(K)} (Im tau_a |eta(tau_a)|^4) = (sqrt|D|/(4 pi))^h * prod_{n=1, gcd(n,D)=1}^{|D|-1} Gamma(n/|D|)^{chi(n)*w/(2h)}

For our specific case, we want eta(tau_Q) (just the (2,0,11) representative).
By PROPORTIONALITY: |eta(tau_Q)|^4 / |eta(tau_Q1)|^4 is a known ratio.

Specifically: tau_Q1 = i sqrt 22, tau_Q = i sqrt(11/2) = tau_Q1 / 2.
And eta(tau/2) related to eta(tau) by no simple relation; need to use product formula.

Let me COMPUTE NUMERICALLY:
  |eta(tau_Q)|, |eta(tau_Q1)|
  prod_n Gamma(n/88)^chi(n)
"""

import mpmath as mp
mp.mp.dps = 60

N_TERMS = 600


def eta_full(tau):
    q = mp.exp(2j * mp.pi * tau)
    p = mp.mpc(1, 0)
    for n in range(1, N_TERMS):
        p *= 1 - q**n
    return q**(mp.mpf(1)/24) * p


tau_Q = mp.mpc(0, mp.sqrt(mp.mpf(11)/2))
tau_Q1 = mp.mpc(0, mp.sqrt(mp.mpf(22)))

eta_Q = eta_full(tau_Q)
eta_Q1 = eta_full(tau_Q1)

print(f"tau_Q = {tau_Q}")
print(f"tau_Q1 = {tau_Q1}")
print()
print(f"eta(tau_Q) = {eta_Q}")
print(f"eta(tau_Q1) = {eta_Q1}")
print()

abs_eta_Q = abs(eta_Q)
abs_eta_Q1 = abs(eta_Q1)
print(f"|eta(tau_Q)| = {abs_eta_Q}")
print(f"|eta(tau_Q1)| = {abs_eta_Q1}")
print()

# Im tau_Q = sqrt(11/2),  Im tau_Q1 = sqrt 22.
Im_Q = mp.sqrt(mp.mpf(11)/2)
Im_Q1 = mp.sqrt(22)
print(f"Im tau_Q  = sqrt(11/2) = {Im_Q}")
print(f"Im tau_Q1 = sqrt 22 = {Im_Q1}")
print()

# Chowla-Selberg LHS: prod over CM classes [a] of (Im tau_a) |eta(tau_a)|^4
# For h=2, two terms multiply.
LHS = (Im_Q * abs_eta_Q**4) * (Im_Q1 * abs_eta_Q1**4)
print(f"Chowla-Selberg LHS = (Im tau_Q |eta|^4) * (Im tau_Q1 |eta|^4) = {LHS}")
print()

# RHS: (sqrt|D|/(4 pi))^h * prod Gamma(n/|D|)^{chi(n) * w/(2h)}
# For K = Q(sqrt -22): D = -88, |D| = 88, h = 2, w = 2.
# Exponent in Gamma product: w/(2h) = 2/(4) = 1/2.
# So RHS = (sqrt 88 / (4 pi))^2 * prod_{n=1}^{87} Gamma(n/88)^{(1/2) chi(n)}.

# Define chi(n) = (-22/n) Kronecker symbol.

def kronecker(a, b):
    if b == 0:
        return 1 if abs(a) == 1 else 0
    if b < 0:
        b = -b
        s = -1 if a < 0 else 1
    else:
        s = 1
    while b % 2 == 0:
        b //= 2
        if a % 2 == 0:
            return 0
        if a % 8 in (3, 5):
            s = -s
    a = a % b
    while a != 0:
        while a % 2 == 0:
            a //= 2
            if b % 8 in (3, 5):
                s = -s
        a, b = b, a
        if a % 4 == 3 and b % 4 == 3:
            s = -s
        a = a % b
    return s if b == 1 else 0


def chi(n):
    return kronecker(-22, n)

# Verify chi has conductor 88.
print("chi values for n = 1..87:")
chi_vals = {n: chi(n) for n in range(1, 88)}
print(f"  chi at primes: " + " ".join(f"chi({p})={chi_vals[p]}" for p in [3,5,7,11,13,17,19,23,29,31,37,41,43,47,53,59]))
print()

# Compute prod_{n=1}^{87} Gamma(n/88)^{(1/2) chi(n)}
log_prod = mp.mpf(0)
for n in range(1, 88):
    cn = chi(n)
    if cn != 0:
        log_prod += (mp.mpf(cn)/2) * mp.log(mp.gamma(mp.mpf(n)/88))

prod_gamma = mp.exp(log_prod)
print(f"prod_{{n=1, chi(n)!=0}}^{{87}} Gamma(n/88)^{{(1/2) chi(n)}} = {prod_gamma}")
print()

# Coefficient (sqrt 88 / (4 pi))^2:
coeff = (mp.sqrt(88) / (4 * mp.pi))**2
print(f"(sqrt 88 / (4 pi))^2 = {coeff}")
print()

RHS = coeff * prod_gamma
print(f"Chowla-Selberg RHS (predicted) = {RHS}")
print()

ratio = LHS / RHS
print(f"Ratio LHS / RHS = {ratio}")
print()

if abs(ratio - 1) < mp.mpf("1e-20"):
    print(">>> Chowla-Selberg formula VERIFIED to 20+ digits.")
elif abs(ratio - 1) < mp.mpf("1e-10"):
    print(">>> Approximately VERIFIED.")
else:
    print(">>> Chowla-Selberg constant might have different normalization. Investigating.")
print()

# Even if the precise CS constant is off, the LHS has a closed form involving these Gamma products.

# NOW: compute m_tau^2 in closed form with Chowla-Selberg substituted.

# We have:
#   W^Q''(tau_Q) = 2 [H'(j_Q) j'(tau_Q)]^2 f_a(tau_Q) / eta(tau_Q)^12

# H'(j_Q) = 2 j(tau_Q) - (j_Q + j_Q1) = 2 j_Q - (j_Q + j_Q1) = j_Q - j_Q1.
# j_Q - j_Q1 = -2 * 2225561184000 sqrt 2 = -4451122368000 sqrt 2.
# (Verified above: H'(j_Q) = -4451122368000 sqrt 2.)

# j'(tau_Q) = -2 pi i E_4(tau_Q)^2 E_6(tau_Q) / Delta(tau_Q).
# At CM points, E_4, E_6, Delta have closed forms as products of Gamma values (Chowla-Selberg).

# f_a(tau_Q) = sum a_n q_Q^n. CM-anchored. Closed form via theta-series of grossencharacter.

# eta(tau_Q)^12 = closed form via Chowla-Selberg.

# This is HEAVY closed form work. Let me get the leading magnitude in Gamma values.

# Numerical: eta(tau_Q)^12 = ? Compare to Chowla-Selberg.
print("="*78)
print("Numerical magnitudes for closed-form construction:")
print("="*78)

eta12_Q = eta_Q**12
print(f"|eta(tau_Q)|^12 = {abs(eta12_Q)}")
print(f"|eta(tau_Q1)|^12 = {abs(eta_Q1**12)}")
print()

# H'(j_Q) j'(tau_Q):
# H'(j_Q) = -4451122368000 sqrt 2.
# j'(tau_Q) = -2 pi i * E_4^2 * E_6 / Delta at tau_Q.
# Exact closed form involves CM values of E_4, E_6, eta.

# For tau_Q (CM of D=-88), E_4(tau_Q) and E_6(tau_Q) have explicit values:
#   E_4(tau_Q) is real (CM tau on imag axis, E_4(it) is real).
#   E_6(tau_Q) is purely imaginary times something.
# Numerically (high precision):
sqrt2 = mp.sqrt(2)
def E4_func(tau):
    q = mp.exp(2j * mp.pi * tau)
    s = mp.mpc(0, 0)
    for n in range(1, N_TERMS):
        sigma3 = sum(d**3 for d in range(1, n+1) if n % d == 0)
        s += sigma3 * q**n
    return 1 + 240 * s

def E6_func(tau):
    q = mp.exp(2j * mp.pi * tau)
    s = mp.mpc(0, 0)
    for n in range(1, N_TERMS):
        sigma5 = sum(d**5 for d in range(1, n+1) if n % d == 0)
        s += sigma5 * q**n
    return 1 - 504 * s

E4_Q = E4_func(tau_Q)
E6_Q = E6_func(tau_Q)
print(f"E_4(tau_Q) = {E4_Q}")
print(f"E_6(tau_Q) = {E6_Q}")
print(f"|E_4(tau_Q)| = {abs(E4_Q)}")
print(f"|E_6(tau_Q)| = {abs(E6_Q)}")
print()

# E_6 should be sqrt of (E_4^3 - 1728 Delta) (up to signs).
Delta_Q = eta_Q**24
print(f"Delta(tau_Q) = eta^24 = {Delta_Q}")
print()

# Verify E_4^3 - E_6^2 = 1728 Delta:
e43_e62 = E4_Q**3 - E6_Q**2
print(f"E_4^3 - E_6^2 = {e43_e62}")
print(f"1728 * Delta = {1728 * Delta_Q}")
print(f"diff = {abs(e43_e62 - 1728 * Delta_Q)}  (should be 0)")
print()

# Now j'(tau_Q):
jp_Q = -2j * mp.pi * E4_Q**2 * E6_Q / Delta_Q
print(f"j'(tau_Q) = -2 pi i E_4^2 E_6 / Delta = {jp_Q}")
print()

# H'(j_Q) j'(tau_Q):
H_coef_a_local = mp.mpf("-6294842640000")
j_Q = E4_Q**3 / Delta_Q
Hp_jQ = 2 * j_Q + H_coef_a_local
Hjp_Q = Hp_jQ * jp_Q
print(f"H'(j_Q) j'(tau_Q) = {Hjp_Q}")
print()

# Closed form for H'(j_Q) j'(tau_Q):
# H'(j_Q) = j_Q - j_Q1 = -4451122368000 sqrt 2
# j'(tau_Q) = -2 pi i E_4^2 E_6 / Delta = (CM closed form)
# Numerical:
print(f"|Hjp_Q| = {abs(Hjp_Q)}")
print(f"|Hjp_Q|^2 = {abs(Hjp_Q)**2}")
print()

# Now f_a(tau_Q): CM theta series value.
# f_a(tau_Q) = some Gamma value (M48 doublon).
print("f_a(tau_Q) numerical (high precision):")
def f_a_func(tau):
    a_a = [1, -2, 0, 4, 0, 0, 0, -8, 9, 0, 11, 0, 18, 0, 0, 16, 0, -18, 6, 0,
           0, -22, -42, 0, 25, -36, 0, 0, -14, 0, -26, -32, 0, 0, 0, 36, 0, -12, 0, 0,
           0, 0, -42, 44, 0, 84, 6, 0, 49, -50, 0, 72, 0, 0, 0, 0, 0, 28, 0, 0,
           -78, 52, 0, 64, 0, 0, 0, 0, 0, 0, 54, -72, 0, 0, 0, 24, 0, 0, 0, 0,
           81, 0, -122, 0, 0, 84, 0, -88, -174, 0, 0, -168, 0, -12, 0, 0, -158, -98, 99, 100]
    q = mp.exp(2j * mp.pi * tau)
    s = mp.mpc(0, 0)
    for n in range(1, len(a_a) + 1):
        an = a_a[n-1]
        if an != 0:
            s += an * q**n
    return s

f_Q = f_a_func(tau_Q)
print(f"  f_a(tau_Q) = {f_Q}")
print()

# Final m^2 closed form:
W_pp = 2 * Hjp_Q**2 * f_Q / eta12_Q
m2_Q = (4 * Im_Q / 9) * abs(W_pp)**2
print(f"W^Q''(tau_Q) = {W_pp}")
print(f"|W^Q''(tau_Q)|^2 = {abs(W_pp)**2}")
print(f"m_tau^2 = (4 sqrt(11/2) / 9) |W^Q''|^2 = {m2_Q}")
print()

# Closed form factorization:
# m^2 = (4 sqrt(11/2)/9) * 4 * |H'|^2 * |j'|^2 * |f|^2 / |eta^{12}|^2
# H' = -4451122368000 sqrt 2 = -2^? * 3^? * ...
# 4451122368000 = ?
factors = mp.mpf("4451122368000")
print(f"4451122368000 = {factors}")
# Factor: 4451122368 = 2^? * ...
# 4451122368000 / 1000 = 4451122368
# 4451122368 / 2^? : 4451122368 = 4451122368 / 2 = 2225561184 -> /2 = 1112780592 -> /2 = 556390296 -> /2 = 278195148 -> /2 = 139097574 -> /2 = 69548787
# So 4451122368 = 2^6 * 69548787. 69548787 / 3 = 23182929 /3 = 7727643 /3 = 2575881 /3 = 858627 /3 = 286209 /3 = 95403 /3 = 31801. So 69548787 = 3^7 * 31801.
# 31801 = ? = 31801 / 7 = 4543 (no, 7*4543 = 31801? 7*4000=28000, 7*500=3500, 7*43=301. 28000+3500+301=31801 yes.). So 31801 = 7 * 4543.
# 4543 / 11 = 413. 11*413 = 4543 ✓. So 4543 = 11 * 413.
# 413 / 7 = 59. 7*59 = 413 ✓. 59 prime.
# So 31801 = 7 * 11 * 7 * 59 = 7^2 * 11 * 59.
# Hmm let me redo:
# 4451122368000 = 2^? * 3^? * ...
import sympy
print(f"sympy.factorint(4451122368000) = {sympy.factorint(4451122368000)}")
# This will give the prime factorization.
print()

# And 6294842640000 (j_Q + j_Q1) = ?
print(f"6294842640000 factorization: {sympy.factorint(6294842640000)}")
print()

# 15798135578688000000 (j_Q * j_Q1) = ?
print(f"15798135578688000000 factorization: {sympy.factorint(15798135578688000000)}")
