"""
Selberg trace formula light test.

For a compact Riemann surface M_g of genus g, Selberg's trace formula relates:
  sum_n h(lambda_n)   <->   sum_{[gamma]} length terms over geodesics

For K3, dim_R = 4, not a Riemann surface, but the analogue:
  Spec(Laplacian) <-> Lattice of cohomology classes [F]

ECI hypothesis (informal): the eigenvalues of D̸ on K3 with twisting
[F] reproduce the sequence of primes in some labeling.

Sanity test: compute eigenvalues of Laplacian on T^4 (4-torus) and check
relationship to primes.

For flat T^4 = R^4 / Z^4, Laplacian eigenvalues are:
  lambda_{n_1, n_2, n_3, n_4} = 4*pi^2 * (n_1^2 + n_2^2 + n_3^2 + n_4^2)

Distinct values (sorted):
  0, 4pi^2, 8pi^2, 12pi^2, 16pi^2, 20pi^2, 24pi^2, ...
  = 4pi^2 * {0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, ...}
The set is the same as integers representable as sum of 4 squares (= ALL integers, by Lagrange).

So on T^4, spectrum is uniform = {n : n in N}.
Multiplicities r_4(n) = number of ways n = sum of 4 squares.

Not directly related to primes.

For K3 with metric (Ricci-flat hyperkähler), Laplacian has different spectrum.
"""

import numpy as np
from sympy import isprime, primerange, divisors
from mpmath import mp, mpf
mp.dps = 30

# Eigenvalues of Laplacian on T^4
def eig_T4_count(N):
    """Number of eigenvalues less than N (in units of 4pi^2)."""
    return sum(1 for n in range(N+1) for a in range(int(np.sqrt(n))+1)
               for b in range(int(np.sqrt(n))+1)
               for c in range(int(np.sqrt(n))+1)
               for d in range(int(np.sqrt(n))+1)
               if a*a+b*b+c*c+d*d <= n)

# Test Selberg analog: trace of e^{-tL} = sum e^{-t lambda_n}
print("="*70)
print("Selberg-like trace on T^4")
print("="*70)
from itertools import product
print("Eigenvalues of -Laplacian/(4pi^2) on T^4 (multiplicities):")
multiplicities = {}
for n in range(15):
    count = 0
    for a, b, c, d in product(range(-int(np.sqrt(n))-1, int(np.sqrt(n))+2), repeat=4):
        if a*a + b*b + c*c + d*d == n:
            count += 1
    multiplicities[n] = count
    print(f"  n={n}: multiplicity r_4(n) = {count}")

# Sum of r_4(n) for n prime
sum_r4_prime = sum(multiplicities[p] for p in [2,3,5,7,11,13] if p in multiplicities)
print(f"\nSum r_4(p) for p in [2,3,5,7,11,13]: {sum_r4_prime}")

# ECI relevance: not obvious connection
print()
print("="*70)
print("Now: Laplacian on Calabi-Yau K3 (numerical approximation)")
print("="*70)
print()
print("K3 metric is Ricci-flat hyperkähler (no closed form known generally).")
print("Spectrum of Laplacian on K3 has FIRST eigenvalue lambda_1 ≈ ?")
print()
print("For Kummer K3, lambda_1 can be computed numerically (with massive effort).")
print("For algebraic K3 with explicit metric: still hard.")
print()
print("In ECI: spectrum of D̸ (Dirac) on K3 with twist [F] is what matters.")
print("Index theorem (Atiyah-Singer): dim ker D̸ - dim coker D̸ = c_2([F]) - rank.")
print("For K3 with c_1 = 0, second Chern class c_2 indexes the topology.")
print()

# Bertin-Kemler / Tate twists: ζ_K3(s) at integer values relates to volumes
# At s = 3 (= weight+1), ζ_K3(3) relates to L(K3, 3) which is the Beilinson regulator value

# Compute partial sums of L(K3, s) at s=3 for Fermat quartic
print("="*70)
print("Partial L(K3, s=3) for Fermat quartic")
print("="*70)

# L(K3, s) = ∏_p L_p(p^-s)^-1
# For p with Tr=a_p known: L_p(T) ≈ 1 - a_p T + p^2 T^2 - ... (degree 22)
# We only have a_p, so approximate L_p(T) ≈ 1 - a_p T as leading order
data_fermat = [(3,6),(5,-26),(7,14),(11,22),(13,-42),(17,310),(19,38),(23,46),(29,-74),(31,62),(37,-218),(41,838),(43,86),(47,94)]

def L_partial_3(data):
    """Partial L-function at s=3, using only a_p (first-order approximation)."""
    log_L = 0.0
    for p, a_p in data:
        T = p**(-3)
        # L_p(T) ≈ 1 - a_p T (linearized) + ...
        L_p = 1 - a_p * T
        if L_p > 0:
            log_L += -np.log(L_p)
        else:
            return None
    return np.exp(log_L)

L_val = L_partial_3(data_fermat)
print(f"Partial L(K3, 3) over p=3..47 (linear approx) = {L_val:.6f}")
print()
print(f"Compare to ECI key constants:")
print(f"  ζ(3) Apery = {float(mpf('1.2020569032')):.4f}")
print(f"  ζ(3)/√π = {float(mpf('1.2020569032') / mpf(np.pi).sqrt()):.4f}")
print(f"  π/(1-κ) with κ=1/6 = {np.pi / (5/6):.4f}")
print(f"  exp(2/3) = {np.exp(2/3):.4f}")

# Better: compute log L derivative at s=1, sum a_p/p
print()
print("Sum a_p/p (related to log L_K3(s) at s=1, related to BSD analog):")
sum_ap_p = sum(a/p for p, a in data_fermat)
print(f"  Sum a_p / p (p=3..47): {sum_ap_p:.4f}")
print(f"  Compare: log(?)  - the Tamagawa number, regulator, etc.")
print(f"  Compare: 2π√(2/15) (CKM phase ECI) = {2*np.pi*np.sqrt(2/15):.4f}")
print(f"  Compare: π√(2/15) = {np.pi*np.sqrt(2/15):.4f}")

# Sum a_p * log(p) / p (Mertens-like)
sum_ap_logp_p = sum(a * np.log(p) / p for p, a in data_fermat)
print(f"  Sum a_p log p / p (p=3..47): {sum_ap_logp_p:.4f}")

# Sum a_p^2 / p^2 (variance, related to BSD rank)
sum_ap2_p2 = sum(a**2 / p**2 for p, a in data_fermat)
print(f"  Sum a_p^2 / p^2 (p=3..47): {sum_ap2_p2:.4f}")

# Key: if a_p ~ 2p for many primes (algebraic dominates), then
#   sum a_p / p ≈ 2 * (number of primes) for those primes
# Plus contribution from anomalous primes (5, 13, 17, 29, 37, 41)
n_alg_primes = sum(1 for p, a in data_fermat if abs(a - 2*p) < 0.1)
print(f"\n  Number of primes with a_p = 2p exactly: {n_alg_primes}")
print(f"  Sum 2 * (algebraic primes) = {n_alg_primes * 2}")

# For ECI: does sum (a_p / p) = 2k for some k = dim G?
# For p=3..47: 14 primes, 8 have a_p=2p contributing 2*8=16 to sum a_p/p
# Plus 6 anomalous primes contributing (sum a_p/p for those)
sum_anom = sum(a/p for p, a in data_fermat if abs(a - 2*p) > 0.1)
print(f"  Sum a_p/p for anomalous (≡1 mod 4): {sum_anom:.4f}")
print(f"  Total = 16 + {sum_anom:.4f} = {16 + sum_anom:.4f}")
print()
print("So sum a_p/p ≈ 17.25 over p=3..47.")
print("Reach 281 = Σ_14 primes? Only if EXTENDED summing many more primes.")
print("Pattern Σ_k a_p/p increasing slowly, not matching Σ primes directly.")
