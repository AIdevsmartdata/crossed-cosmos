"""
M176 sub-task 4 follow-up — Hilbert class field of Q(sqrt(-22)) — VERIFY
=========================================================================

CRITICAL CROSS-CHECK: The Hilbert class field H(-88) of K = Q(sqrt(-22)):
is it Q(sqrt(-22), sqrt(2)) or Q(sqrt(-22), sqrt(-11)) or something else?

By genus theory (Gauss): the GENUS FIELD of K = Q(sqrt(-22)) is the maximal abelian
extension of K contained in the Hilbert class field that is generated over Q by sqrts.

For K = Q(sqrt(d)) with d squarefree, factor d = ε p_1 ... p_r with ε = ±1.
For d = -22 = (-1)(2)(11): factorization (-1)*(2)*(11), so signs distribute:
  primes ramified in K = {2, 11} (since |disc K| = 88 = 2^3 * 11)

Genus field = K(sqrt(p_1*), sqrt(p_2*), ...) where p_i* = (-1)^{(p-1)/2} p for odd p,
and 2* = -1 or ±2 etc.

For 11: 11 = 3 mod 4, so 11* = -11.
For 2: 2* = ... in genus theory, 2 contributes via different mechanism.

Standard result for d = -22: the genus field is K(sqrt(-1)) = Q(sqrt(-22), i)
  -- BUT only if 2 is "ramified appropriately" in K.

Actually, for d = -22 with class number 2 (= 2^1, where 1 = number of primes ramified - 1
in standard Gauss formula μ - 1 with μ = number of distinct prime factors of disc):
  disc(K) = -88 = -2^3 * 11; ramified primes = {2, 11}; μ = 2, so genus class number = 2^{μ-1} = 2.

Since h_K = 2 = genus class number, the genus field IS the full HCF.

So we need to determine which biquadratic field over Q is the HCF of Q(sqrt(-22)).
The candidates (degree 2 over K, abelian over Q):
  K(sqrt(-1)) = Q(sqrt(-22), i)        --- our compositum candidate!
  K(sqrt(2))  = Q(sqrt(-22), sqrt(2))  --- M171/M176 sub-task 3 candidate (Schütt)
  K(sqrt(-2)) = Q(sqrt(-22), sqrt(-2)) = Q(sqrt(-2), sqrt(11)) (since (sqrt(-22))*(sqrt(-2)) = -sqrt(44) = -2 sqrt(11))
  K(sqrt(11)) = Q(sqrt(-22), sqrt(11)) = same as above (since K already contains sqrt(-22) and 11/(-22) = -1/2)

Actually K(sqrt(-2)) = K(sqrt(11)) since sqrt(-2) * sqrt(-22) = sqrt(44) = 2 sqrt(11),
so sqrt(11) ∈ K(sqrt(-2)) and vice versa. Same field.

Three candidates for genus field of Q(sqrt(-22)):
  (A) Q(sqrt(-22), i)            = Q(sqrt(-1), sqrt(-22))   contains Q(sqrt(22))   real
  (B) Q(sqrt(-22), sqrt(2))      = Q(sqrt(2), sqrt(-22))    contains Q(sqrt(-11))  imag
  (C) Q(sqrt(-22), sqrt(-2))     = Q(sqrt(-2), sqrt(11))    contains Q(sqrt(-22))  imag

All three are biquadratic over Q with V_4 Galois group. They are all DIFFERENT degree-4 fields.

WHICH ONE is the genuine Hilbert class field of K = Q(sqrt(-22))?

DEFINITIVE ANSWER (Cox, "Primes of the form x^2 + n y^2", 1989):
For K = Q(sqrt(-22)), n = 22, the principal form is x^2 + 22 y^2 representing primes
p with p splits completely in HCF(K).

By Cox Theorem 9.2 / standard: HCF(Q(sqrt(-n))) = K(j(O_K)) for class number > 1.
j(O_K) = j(i sqrt(22)) = 3,147,421,320,000 + 2,225,561,184,000 sqrt(2).
j(O_K) ∈ Q(sqrt(2)).
Hence HCF(K) = K(sqrt(2)) = Q(sqrt(-22), sqrt(2)) [option (B)].

This MATCHES Schütt's framework (M176 script 03) and CONTRADICTS the
biquadratic compositum K^(1) * K^(2) = Q(i, sqrt(-22)) being the HCF.

CONCLUSION: K^(1) * K^(2) = Q(i, sqrt(-22)) ≠ HCF(K^(2)) = Q(sqrt(-22), sqrt(2)).

These are TWO DIFFERENT biquadratic fields, both of degree 4 over Q.
Q(i, sqrt(-22)):              real subfield Q(sqrt(22)),  imag subfields Q(i), Q(sqrt(-22))
Q(sqrt(-22), sqrt(2)):        real subfield Q(sqrt(2)),   imag subfields Q(sqrt(-22)), Q(sqrt(-11))

So the M171 'open route (b)' (compositum K^(1) * K^(2)) is NOT the same field as the
HCF that natively shows up in Shioda-Inose. The two biquadratic extensions are
LINEARLY DISJOINT over Q(sqrt(-22)) (they intersect in K^(2) = Q(sqrt(-22))).

Their further compositum is the TRIQUADRATIC field
  M = Q(i, sqrt(-22), sqrt(2)) = Q(sqrt(-1), sqrt(2), sqrt(-22))
of degree 8 over Q with Galois group V_3 = Z/2 x Z/2 x Z/2.

VERIFY by sympy:
"""

import sympy as sp
from sympy import sqrt, I, Rational, expand, simplify, gcd, prime, isprime
from sympy.polys.numberfields import minimal_polynomial as min_poly

print("="*72)
print("M176 sub-task 4 follow-up: HCF of Q(sqrt(-22)) -- definitive identification")
print("="*72)

# Verify j(O_K) lies in Q(sqrt(2)) -- already done in script 01
# So HCF(K) = K(sqrt(2)) = Q(sqrt(-22), sqrt(2))

# Construct explicit primitive element for HCF(K)
# alpha = sqrt(-22) + sqrt(2)
# alpha^2 = -22 + 2 + 2 sqrt(-22) * sqrt(2) = -20 + 2 sqrt(-44) = -20 + 4 sqrt(-11)
# Hmm not clean. Try alpha = sqrt(2) * sqrt(-22) = sqrt(-44) = 2 sqrt(-11).
# So sqrt(-11) lies in K(sqrt(2)) = Q(sqrt(-22), sqrt(2)).
# And sqrt(2) = sqrt(-22) / sqrt(-11) (after rationalizing).
# Confirmed: K(sqrt(2)) = K(sqrt(-11)) as the same field, biquadratic Q(sqrt(-22), sqrt(-11))
#           = Q(sqrt(-22), sqrt(2)) -- three quadratic subfields:
#                                       Q(sqrt(-22)), Q(sqrt(2)), Q(sqrt(-11))

print("\nHCF(Q(sqrt(-22))) = Q(sqrt(-22), sqrt(2))")
print("                  = Q(sqrt(-22), sqrt(-11))      [same field]")
print("                  = Q(sqrt(2), sqrt(-11))        [same field]")
print("Quadratic subfields:  Q(sqrt(-22)), Q(sqrt(2)), Q(sqrt(-11))")
print("Real subfield: Q(sqrt(2))")
print("")

# Verify sqrt(-11) ∈ Q(sqrt(-22), sqrt(2)) explicitly
alpha = sqrt(-22) * sqrt(2)
alpha_sq = expand(alpha * alpha)
print(f"sqrt(-22) * sqrt(2) = {alpha}")
print(f"   squared = {alpha_sq}")
print(f"   = sqrt(-44) = 2 * sqrt(-11)  -- yes, sqrt(-11) ∈ Q(sqrt(-22), sqrt(2))")

# Now compare with the OTHER candidate K^(1)·K^(2) = Q(i, sqrt(-22))
beta = I * sqrt(-22)
beta_sq = expand(beta * beta)
print(f"\ni * sqrt(-22) = {beta}")
print(f"   squared = {beta_sq}")
print(f"   = sqrt(22)  (REAL)  -- so Q(sqrt(22)) ⊂ Q(i, sqrt(-22))")

print("\n--- Summary: TWO biquadratic fields, both of degree 4 over Q ---")
print("\n[Field A]  K_HCF = Q(sqrt(-22), sqrt(2))   == Hilbert class field of Q(sqrt(-22))")
print("           Quadratic subfields: Q(sqrt(-22)), Q(sqrt(2)) [REAL], Q(sqrt(-11))")
print("           Disc/Q: 4 * 88 * 44 / something... by conductor-disc:")
print("             chars: trivial, chi_{-88}, chi_8, chi_{-11}")
print("             conductors: 1, 88, 8, 11")
print("             disc = 1 * 88 * 8 * 11 = 7744 = 2^6 * 11^2  -- no wait that's not right")

# Compute disc using conductor-disc for the V_4 abelian extension
# Three nontrivial characters: chi_2, chi_8, chi_{-11};
# chi_2 = quadratic char of Q(sqrt(-22)) has cond 88
# chi_8 = quadratic char of Q(sqrt(2)) has cond 8
# chi_{-11} = quadratic char of Q(sqrt(-11)) has cond 11
# Wait, sqrt(-11): -11 = 1 mod 4, so disc(Q(sqrt(-11))) = -11, cond = 11.
# sqrt(2): 2 squarefree, 2 mod 4 -> disc = 8, cond = 8
# sqrt(-22): cond = 88 as computed.
# disc(K_HCF/Q) = 1 * 88 * 8 * 11 = 7744 = 2^6 * 11^2
disc_HCF = 88 * 8 * 11
print(f"\n[Field A] disc(K_HCF/Q) = 88 * 8 * 11 = {disc_HCF} = {sp.factor(disc_HCF)}")

print("\n[Field B]  K_compositum = Q(i, sqrt(-22))   == compositum of K^(1), K^(2) (M171 route b)")
print("           Quadratic subfields: Q(i), Q(sqrt(-22)), Q(sqrt(22)) [REAL]")
# chars: trivial, chi_{-4} (cond 4), chi_{-88} (cond 88), chi_{88} (cond 88)
# Q(sqrt(22)): 22 = 2 mod 4, disc = 4*22 = 88, cond = 88.
disc_compo = 4 * 88 * 88
print(f"           disc(K_compositum/Q) = 4 * 88 * 88 = {disc_compo} = {sp.factor(disc_compo)}")

print("\n[Triquadratic compositum]  M = Q(i, sqrt(-22), sqrt(2)) = K_compositum * K_HCF")
print("           Galois group: (Z/2)^3 of order 8")
print("           Seven quadratic subfields:")
print("             Q(i), Q(sqrt(2)), Q(sqrt(-2)), Q(sqrt(11)), Q(sqrt(-11)), Q(sqrt(22)), Q(sqrt(-22))")

# Discriminant of M:
# 7 nontrivial chars: cond(chi_{-1})=4, cond(chi_8)=8, cond(chi_{-8})=8, cond(chi_{11})=44? actually
# Q(sqrt(11)): 11 = 3 mod 4, disc = 4*11 = 44, cond = 44.
# Q(sqrt(-11)): disc = -11, cond = 11.
# Q(sqrt(22)): cond = 88.
# Q(sqrt(-22)): cond = 88.
# Q(sqrt(-2)): -2 = 2 mod 4, disc = -8, cond = 8.
# Hmm wait, the 7 subfields... let me list:
# (Z/2)^3 has 7 nontrivial chars, they correspond to the 7 quadratic subfields of M.
# disc(M/Q) = product of all 7 conductors = 4 * 8 * 8 * 44 * 11 * 88 * 88
#           = ... let me compute
disc_M = 4 * 8 * 8 * 44 * 11 * 88 * 88
print(f"           disc(M/Q) = 4 * 8 * 8 * 44 * 11 * 88 * 88 = {disc_M}")
print(f"                     = {sp.factor(disc_M)}")
