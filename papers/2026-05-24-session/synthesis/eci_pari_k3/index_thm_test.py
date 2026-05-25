"""
Last sanity test: Could ECI "primes" be related to Atiyah-Singer index multiplicities
on K3 rather than Frobenius traces?

For Dirac operator D̸ twisted by [F] on K3:
  ind(D̸_{[F]}) = c_2([F]) - rank([F])

For K3 with self-dual instanton number n (= c_2 = n):
  ind = n  (since rank = 0 for SU(N) bundle with c_1 = 0)
  Number of fermion zero modes = n - 24*(something via Atiyah-Singer + grav anomaly)

Specifically: A-genus(K3) = 2 for K3 (since K3 is spin, A^(K3) = 1 + ... + chern integral)
So for U(1) bundle of c_2 = n: dim ker D̸ = n - 24*2 = n - 48? Or n - 2 ?

Atiyah-Singer for K3:
  A-roof genus L(X) = - p_1 / 24 + 7 p_1^2 - 4 p_2 / 5760
  For K3: p_1 = 0 (signature -16), p_2 = ?
  Actually for K3: chi(K3) = 24, sig(K3) = -16

  Index of D̸ for spin Dirac: ind(D̸_spin) = A-hat([K3]) = -16/8 = -2  (mod sign)

For Dirac D̸_E twisted by vector bundle E:
  ind(D̸_E) = ∫_X ch(E) * A-hat(K3) = (rk E)*(A-hat) + c_1(E)^2/2 - c_2(E) ... etc.

For SU(N) bundle (c_1 = 0):
  ind(D̸_E) = N * (-2) - c_2(E) = -2N - c_2(E)

Number of zero modes of D̸ on K3 with SU(N) bundle of c_2 = n:
  ker D̸ - coker D̸ = -2N - n

For K3, ker D̸ are the 4D fermion zero modes (after KK reduction).
3 generations <=> ind = -3 (or +3 for left-handed).

So: 3 = 2N + n, with N gauge group, n instanton number.
N = 1 (U(1)): n = 1
N = 2 (SU(2)): n = -1 (anti-instanton)
N = 3 (SU(3)): n = -3 (negative, unphysical)
N = 5 (SU(5) GUT): n = -7
N = 10 (SO(10)): n = -17

These integer constraints don't match "first N primes" pattern.

But maybe the SUM ∑_i n_i over multiple bundles = ECI primes ?
ECI: dim G = k <-> first k primes sum
   k=8 (SU(3)): sum of 8 primes = 77 = M_Pl/v ratio
   k=14 (G_2): sum of 14 primes = 281 = Λ exponent
"""

import numpy as np
from sympy import sieve

print("="*70)
print("Test: are 'primes ECI' related to fermion zero mode counts on K3?")
print("="*70)

# For Atiyah-Singer index sequence
# K3 has chi = 24, sig = -16, A-hat = -2 (for half-Dirac)
# 24 = b_2(K3) + 2 = 22 + 2 (Hodge numbers)
# 16 = signature absolute value

# Decompose ECI "primes" in terms of K3 invariants:
print(f"K3 invariants:")
print(f"  chi(K3) = 24")
print(f"  sig(K3) = -16")
print(f"  b_2(K3) = 22")
print(f"  Number of generators of cohomology lattice = 22")
print()

# ECI claims:
# eta_B = exp(-(b_2(K3) - 1)) = exp(-21)
# This is the number of NONTRIVIAL Bianchi classes (excluding the trivial one)

# Number 21 = b_2 - 1 = 22 - 1 = 21. ✓
# Number 22 = b_2(K3) itself
# Number 24 = chi(K3)
# Number 8 = dim SU(3) (gauge generators)
# Number 14 = dim G_2 (dark)

# Now first 14 primes sum to 281. Is 281 expressible in K3 invariants?
# 281 = 11 * 25 + 6 = 7 * 40 + 1 = ...
# 281 = 282 - 1 = 6 * 47 - 1 = ...
# Hmm not obviously.

# First 8 primes sum to 77.
# 77 = 7 * 11 = b_2 * 3.5 (not integer)
# 77 = 24 + 53 = ...
# 77 = chi(K3) * 3 + 5

# Could ECI primes encode "characteristic class integers" on K3?
# The Chern numbers of K3 in dimension D=8 (twice K3) are integers like
# c_2^2 = 0, c_4 = 24 etc.

# Let me try: what if primes are NOT primes in N but in some
# arithmetic structure of K3 (like ideal class representatives)?
# Q(zeta_8) has class number 1, so trivial.
# Q(i) has class number 1.
# Q(sqrt(-3)) has class number 1.

# Conclusion: not enough structure in K3 to derive primes naturally.
print("="*70)
print("Verdict: K3 has 22 cohomology generators but no canonical")
print("identification with 'first k primes'. The sequence p_1, p_2, ...")
print("does not appear to be a natural arithmetic invariant of K3.")
print("="*70)
print()

# Alternative: could primes encode dimensions of Galois orbits?
# For Q(zeta_8): Galois group = (Z/8)^* of order 4
# Orbits of Gal on H^2(K3, Q_l) have sizes 1, 2, or 4 typically.
# Sum of orbit sizes = 22 (total dimension).
# But Sum of first k primes (k = orbit count) is unrelated.

# Sum first k primes can match certain physical quantities by NUMERICAL ACCIDENT,
# but I can't find a STRUCTURAL reason.

print("Best mechanism for 'primes ECI':")
print("Option 1: Anthropic/landscape selection: among all possible Σ_k sequences,")
print("  the universe selects k = dim(G_active) such that observable matches.")
print("Option 2: Spectral encoding: but K3 spectrum doesn't directly give primes.")
print("Option 3: Selberg trace formula: requires identifying geodesic length spectrum")
print("  with prime sequence, which is not directly possible for K3.")
print("Option 4: Beilinson regulator: L(K3, n) at special n encodes specific zeta values,")
print("  which themselves are transcendental but expressible via primes.")
print()
print("HONEST CONCLUSION: 'primes ECI' is a NUMERICAL OBSERVATION currently,")
print("not derivable from K3 arithmetic via available tools. Mechanism still missing.")
