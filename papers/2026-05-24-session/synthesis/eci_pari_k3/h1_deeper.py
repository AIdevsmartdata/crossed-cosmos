"""
Deeper H1 test: factor L-function of Fermat quartic via modular forms.

For the Fermat quartic K3 (Picard rank 20), the L-function decomposes as:
  L(K3, s) = L(NS, s) * L(T, s)
where:
- L(NS, s) is "trivial" Hecke series from algebraic cycles (Tate twists of zeta(s)/zeta(s-1))
- L(T, s) is the transcendental part, dim 2 -> a modular form of weight 3

Specifically (verified mathematical fact):
  Fermat quartic K3 is CM by Q(zeta_8) ~= Q(i, sqrt(2))
  Transcendental lattice T_X = U(2) ⊕ U(2) or similar, rank 2
  L(T, s) corresponds to a Hecke Grossencharacter ψ on Q(zeta_8)
  The associated modular form has weight 3 and level related to 8.

CHECK: Compute Frobenius traces and see if they match coefficients
of a known modular form.

For K3 of CM type, the L-function is essentially:
  L(K3, s)/L(NS, s) ∝ L(ψ, s) for a Grossencharacter

For Fermat quartic, a_p = (Tr from transcendental part):
  - If p ≡ 1 mod 8: a_p ≠ 0 (split in Q(zeta_8))
  - If p ≡ 3, 5, 7 mod 8: a_p = 0 (inert / partially split)

Wait - this is for the transcendental part alone, which is 2-dim and Galois-rational.
"""

import numpy as np
from sympy import isprime, sieve

# From PARI computation
# (p, #X(F_p), Tr(Frob|H^2))
data = [
    (3, 16, 6),
    (5, 0, -26),
    (7, 64, 14),
    (11, 144, 22),
    (13, 128, -42),
    (17, 600, 310),
    (19, 400, 38),
    (23, 576, 46),
    (29, 768, -74),
    (31, 1024, 62),
    (37, 1152, -218),
    (41, 2520, 838),
    (43, 1936, 86),
    (47, 2304, 94),
]

print("="*80)
print("Fermat quartic K3 Frobenius: structure analysis")
print("="*80)
print(f"{'p':<4} {'p mod 8':<8} {'p mod 4':<8} {'Tr':<10} {'Tr - 2p':<10} {'(Tr-2p)/p':<14} {'(Tr-2p)/p^2':<14}")
for p, n, tr in data:
    print(f"{p:<4} {p%8:<8} {p%4:<8} {tr:<10} {tr - 2*p:<10} {(tr - 2*p)/p:<14.4f} {(tr - 2*p)/p**2:<14.4f}")

print()
print("Observation: Tr - 2p is the contribution from the 20 NS cycles minus the 2 already counted in '+2p'")
print("For p ≡ 3 mod 4 (3, 7, 11, 19, 23, 31, 43, 47): Tr = 2p exactly")
print("  => Transcendental + 18 NS cycles all give zero contribution")
print("  => Geometric Frobenius on H^2_geom has eigenvalues: p, p, and 20 others summing to zero")
print()
print("For p ≡ 1 mod 4 (5, 13, 17, 29, 37, 41): Tr varies wildly")
print("  => Extra Picard cycles defined over F_p")
print()

# CRITICAL TEST: Compute the "transcendental" trace = Tr(Frob | T_X)
# For Fermat quartic, T_X is 2-dimensional and gives a CM modular form of weight 3.
# This modular form is known: f(tau) = sum a_n q^n with specific properties.

# Actually, the Fermat quartic L-function has been studied (Pinch, Schoen, etc.)
# Known result: L(T(Fermat^4), s) = L(f, s) where f is a CM newform of weight 3
# Level 64 = 8^2 (or 16) and character chi_{-4} or chi_8

# Let's check: for p inert in Q(zeta_8) the transcendental part contributes 0
# Q(zeta_8) = Q(sqrt(-1), sqrt(2)), has discriminant 256 = 2^8
# Primes p inert iff p ≢ 1 (mod 8)
# Primes that split iff p ≡ 1 (mod 8)
# Among p=3..47, p ≡ 1 mod 8: only 17, 41

# Verify: p=17 has anomalous Tr=310, p=41 has anomalous Tr=838 ✓
# So the "anomaly" is from EXTRA picard cycles over F_p
# AND/OR from transcendental contribution

print("="*80)
print("ECI hypothesis test: does sum a_p relate to primes/dim G?")
print("="*80)

# ECI hypothesis: sum_{p prime, p <= N} a_p = something matching dim G or sum of primes
# Try various sums:
trs = [t for p, n, t in data]
ps = [p for p, n, t in data]
print(f"Primes used: {ps}")
print(f"Frobenius traces: {trs}")
print()

# Various partial sums
for k in range(2, len(trs)+1):
    s_a = sum(trs[:k])
    s_abs = sum(abs(t) for t in trs[:k])
    s_a_minus_2p = sum(t - 2*p for p, n, t in data[:k])
    p_last = ps[k-1]
    print(f"k={k}, p_max={p_last}: sum a_p = {s_a}, sum |a_p| = {s_abs}, sum(a_p - 2p) = {s_a_minus_2p}")

# Sum of first k primes for comparison
print()
print("Sum of first k primes (for ECI comparison):")
prime_sums = []
for k in range(2, 16):
    prime_sums.append(sum(list(sieve.primerange(2, 200))[:k]))
    print(f"  Σ first {k} primes = {prime_sums[-1]}")

# Test: do partial sums of a_p match Σ first k primes for some k?
print()
print("Match: sum a_p vs Σ first k primes?")
prime_seq = list(sieve.primerange(2, 200))
for k in range(2, len(trs)+1):
    sum_ap = sum(trs[:k])
    # find closest Σ first j primes
    best_j = min(range(1, 20), key=lambda j: abs(sum(prime_seq[:j]) - sum_ap))
    print(f"  k={k}: sum a_p = {sum_ap}, closest Σ first {best_j} primes = {sum(prime_seq[:best_j])}, diff = {sum_ap - sum(prime_seq[:best_j])}")

print()
print("="*80)
print("CRITICAL: Are these traces matching a known modular form?")
print("="*80)
# A weight-3 newform on Gamma_0(N) with CM by Q(i) or Q(sqrt(-2))
# has a_p = 0 for p inert and a_p = (alpha + alpha-bar) for p split

# For the trans part of Fermat quartic K3, the modular form is f_8 or f_16 weight 3
# Known: Fermat quartic K3 has Hecke L-function ~ L(psi, s) for psi Grossencharacter on Q(i)
# Actually it's related to the eta product: f(tau) = eta(2 tau)^4 eta(4 tau)^4 ? (weight 4 newform)

# Let me check transcendental trace = (Tr/Frob/22) for various primes
print(f"{'p':<4} {'p mod 8':<8} {'Tr - 20*p (if 20 alg cycles each contributing +p)':<55}")
for p, n, tr in data:
    # If 20 algebraic cycles each contribute +p to Tr (i.e. Frob acts as +1 on them up to a Tate twist):
    # Then transcendental part should give Tr_trans = Tr - 20*p
    tr_trans = tr - 20*p
    print(f"{p:<4} {p%8:<8} {tr_trans:<55}")

print()
print("OR: if some cycles contribute +p and others -p:")
print("Try: a_p (transcendental, 2-dim) = Tr - (k_+ - k_-)*p")
print("where k_+ + k_- = 20 (algebraic ranks) and k_+ - k_- determines algebraic trace")
print()

# Standard result: Fermat quartic K3 transcendental T has Hecke character
# from the modular form eta(2 tau)^8 eta(4 tau)^4 / eta(tau)^4 ?
# or similar.

# For diagonal K3 like x^4+y^4+z^4+w^4=0:
# The L-function factorizes via Jacobi sums.
# Specifically: #X(F_p) = sum_{a+b+c+d=0} ... involving 4th-power Jacobi sums

# Let me just test: Sum |a_p|/p^s for various s
print("="*80)
print("Sum |a_p|/p^s vs ECI quantities:")
print("="*80)
import math
for s in [0.5, 1.0, 1.5, 2.0]:
    sum_val = sum(abs(t)/p**s for p, n, t in data)
    print(f"  s={s}: sum |a_p|/p^s = {sum_val:.4f}")

# Check log of L-function values:
# L(K3, s) at s=2: should be near pole
# At s=3: regular value
# At s=1: pole or special value related to BSD-like analog

# Sum log L_p(1/p^s)
print()
print("Effective L-function values via local factors L_p(T) = 1 - a_p T + p^2 T^2:")
for s in [1.0, 1.5, 2.0]:
    L_log = 0
    for p, n, tr in data:
        T = p**(-s)
        local = 1 - tr*T + p**2 * T**2
        L_log += -math.log(abs(local)) if local != 0 else 100
    print(f"  log L_partial(s={s}) ≈ {L_log:.4f}")
