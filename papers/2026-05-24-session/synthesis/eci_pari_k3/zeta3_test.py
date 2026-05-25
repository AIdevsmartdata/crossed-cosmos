"""
Test: does partial L(K3, 3) = ζ(3) Apéry constant?

If yes, this would be a remarkable empirical hit, but we need to:
1. Check if it converges to ζ(3) or to L(K3, 3) (different number).
2. Cross-check with mathematical theory.

For a K3 over Q with Picard rank rho = 20 (max for Q):
  L(K3, s) = L_NS(s) * L_T(s)
  L_NS(s) = factor involving zeta(s-1) (Tate twist of zeta function)
  L_T(s) = transcendental L-function, weight 3 modular form

So at s = 3:
  L_NS(3) = involves zeta(2) factor (since shift s -> s-1 gives zeta(2))
  But also product of zetas: zeta(s)^a * zeta(s-1)^b * zeta(s-2)^c

For Picard rank 20 over Q, NS has rank 20 over Q with characters as cycles.
Specifically: L(NS, s) = product (chi(p)/p^{s-1})^{-1} where chi indexes algebraic cycles.

Let me consider a simpler case: the Fermat quartic K3 has very explicit structure.
Its zeta function (over Q) at integer values can be computed.
"""

import numpy as np
from sympy import sieve, isprime
from mpmath import mp, mpf, zeta as mpzeta

mp.dps = 30
print(f"ζ(3) = {float(mpzeta(3)):.10f}")
print()

# Fermat quartic K3 partial Frobenius data
data_fermat = [(3,6),(5,-26),(7,14),(11,22),(13,-42),(17,310),(19,38),(23,46),(29,-74),(31,62),(37,-218),(41,838),(43,86),(47,94)]

# Recompute partial L at s=3 PROPERLY: L_p(T) = 1 - a_p T + p^2 T^2 - ... (degree 22)
# But we only know a_p, not higher coeffs. So linearize as 1 - a_p T.
# For p large, T = p^{-s} small, so L_p ≈ 1 - a_p / p^s ≈ 1 (good approx).

def L_partial_linear(data, s):
    log_L = 0.0
    for p, a_p in data:
        T = p**(-s)
        log_L -= np.log(1 - a_p * T)
    return np.exp(log_L)

print(f"L_partial(K3 Fermat, s=3) over p=3..47 (linear) = {L_partial_linear(data_fermat, 3):.6f}")
print(f"L_partial(K3 Fermat, s=2.5) = {L_partial_linear(data_fermat, 2.5):.6f}")
print(f"L_partial(K3 Fermat, s=2)  = {L_partial_linear(data_fermat, 2):.6f}")
print(f"L_partial(K3 Fermat, s=4)  = {L_partial_linear(data_fermat, 4):.6f}")
print()

# Note: the QUADRATIC term we're missing in L_p(T) = 1 - a_p T + p^2 T^2 (degree 2 not full 22)
# For K3, full L_p has degree 22. But for QUADRATIC factor, it's already significant.
# Let's add it:
def L_partial_quad(data, s):
    log_L = 0.0
    for p, a_p in data:
        T = p**(-s)
        # Approx L_p(T) ≈ (1 - alpha_1 T)(1 - alpha_2 T)... for 22 terms
        # Quadratic: 1 - a_p T + p^2 T^2
        L_p = 1 - a_p * T + p**2 * T**2
        log_L -= np.log(abs(L_p))
    return np.exp(log_L)

print(f"L_partial(K3, s=3, quadratic): {L_partial_quad(data_fermat, 3):.6f}")
print()

# More relevant: the TRANSCENDENTAL L-function L_T(K3, s) is weight-3 modular form
# evaluated at s=3, which is L(f, 3) where f is the weight-3 CM newform.
# For 16.3.b.a: L(f, 3) = ?

# Compute partial L(f, 3) using only the McKay newform a_p
# Form 16.3.b.a has: a_5 = -6, a_9 = 9 (=a_3^2 from sym, but a_3 = 0)
# a_13 = 10, a_17 = -30, a_25 = 11 (=a_5^2 - p_5 = 36-25 = 11), a_29 = ?

# Use only the a_p that the CM newform gives nonzero (p ≡ 1 mod 4)
cm_form_ap = {1: 1, 5: -6, 9: 9, 13: 10, 17: -30, 25: 11}
# Note 25 = 5^2, not prime
# For p ≡ 1 mod 4, p prime: 5, 13, 17, 29, 37, 41
# a_5 = -6, a_13 = 10, a_17 = -30
# a_29 = ?, a_37 = ?, a_41 = ?

# These come from Hecke Grossencharacter on Q(i):
# a_p = 2 * Re(alpha^2) where p = N(alpha) = a^2 + b^2 with alpha = a + bi
# For p = 29: 29 = 25 + 4 = 5^2 + 2^2, so alpha = 5 + 2i, alpha^2 = 25 + 20i - 4 = 21 + 20i, Re=21
#   a_29 = 42 or -42?
# Verify with our data: Fermat quartic Tr-2p for p=29: -132 = ??? * (Sym^2 contribution)
# Sym^2 a_29 (E:y^2=x^3-x): a_29(E) = -10, sym2 = 100 - 29 = 71. Sign convention.

# 16.3.b.a is the unique CM newform with these properties.
# Compute L(16.3.b.a, 3) numerically:

# Use full series sum from a_n
import mpmath as mpm
mp.dps = 30

# Compute partial sum sum a_n / n^s for n up to 1000
def L_cm_partial_3(n_max, s=3):
    # Compute coefficients using formula a_n = 0 unless n is rep by sum a^2+b^2
    # AND involves character chi_{-4}(d) for divisors
    # For simplicity: just use the formula a_p = 2 Re(alpha^2) and a_{p^k} = ...
    # For CM newform of weight 3 on Q(i), a_n is a multiplicative function:
    # a_p = chi(p) * (alpha + alpha-bar) where alpha is Hecke character of p
    # For weight 3: a_p(f) = sum over alpha with N(alpha)=p of (alpha)^2

    sum_an_n_s = mpf(0)
    for n in range(1, n_max+1):
        if n == 1:
            a_n = 1
        else:
            # Brute compute: find decomp n = sum a^2 + b^2 with multiplicities
            # For Q(i), a_n = sum over (a, b) coprime to 1+i with a^2 + b^2 = n of (a + bi)^2
            # = sum (a^2 - b^2 + 2abi)
            # Real part = sum (a^2 - b^2) over decomps
            # For prime p ≡ 1 mod 4: unique up to ±, ±i, so 4 elements, but Re part = ±2(a^2-b^2)
            a_n = 0
            # We need n to be sum of 2 squares
            for a in range(0, int(np.sqrt(n))+1):
                bsq = n - a*a
                if bsq < 0: continue
                b = int(round(np.sqrt(bsq)))
                if b*b != bsq: continue
                # (a + bi)^2 = a^2 - b^2 + 2abi, real part = a^2 - b^2
                if a == 0:
                    # b^2 = n => contributes (bi)^2 = -b^2 = -n
                    a_n += -n if a > 0 or b > 0 else 0
                elif b == 0:
                    a_n += a*a
                else:
                    a_n += 2 * (a*a - b*b)
        if a_n != 0:
            sum_an_n_s += mpf(a_n) / mpf(n)**s
    return sum_an_n_s

# Too slow for n=1000 with this. Just use first few terms
print("Partial L(CM 16.3.b.a, s=3) with explicit formula a_n = 2 Re(alpha^2):")
L_part = L_cm_partial_3(100, 3)
print(f"  n_max=100: L_part = {float(L_part):.6f}")
L_part = L_cm_partial_3(500, 3)
print(f"  n_max=500: L_part = {float(L_part):.6f}")

# More important: the actual L(16.3.b.a, 3) value from LMFDB
# This is a critical L-value, related to motivic ζ at central s = 3

# Theoretical statement: for the CM newform of weight 3 level 16 char chi_-4,
# the central L-value L(f, 1) = π / 4 * (specific algebraic number)
# At s = w = 3 (right-most edge of critical strip), L is just convergent value

# But Beilinson regulator suggests L(K3, 3) is related to volume of period domain

print()
print("="*70)
print("Conclusion on H1 / partial L matching ζ(3):")
print("="*70)
print("The observation L_partial(K3, 3) ≈ 1.2035 ≈ ζ(3) = 1.2021 (1.1% diff) is suggestive.")
print("BUT: with only 14 primes and linear approximation, this is unreliable.")
print("Need higher-order L_p coefficients to be accurate.")
print()
print("Adversarial test: same partial sum with random a_p satisfying |a_p| <= 22p")

# Adversarial
np.random.seed(42)
n_trials = 1000
matches_zeta3 = []
target = float(mpzeta(3))
for trial in range(n_trials):
    fake_data = [(p, np.random.uniform(-22*p, 22*p)) for p, _ in data_fermat]
    L_fake = L_partial_linear(fake_data, 3)
    matches_zeta3.append(L_fake)

matches_zeta3 = np.array(matches_zeta3)
print(f"Random Sato-Tate trace, L_partial(s=3): mean = {matches_zeta3.mean():.4f}, std = {matches_zeta3.std():.4f}")
print(f"Real: {L_partial_linear(data_fermat, 3):.4f}")
print(f"Target ζ(3) = {target:.4f}")
print(f"Distance real to ζ(3): {abs(L_partial_linear(data_fermat, 3) - target):.4f}")
print(f"Fraction of trials within same distance to ζ(3): {np.mean(abs(matches_zeta3 - target) <= abs(L_partial_linear(data_fermat, 3) - target))*100:.2f}%")
