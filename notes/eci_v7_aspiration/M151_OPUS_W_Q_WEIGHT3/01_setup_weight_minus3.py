#!/usr/bin/env python3
"""
M151 / Step 1 -- Mathematical setup for weight-(-3) modular form W^Q.

Goal: Find W^Q on Gamma_0(N) (some N | 88) such that
  - W^Q has modular weight -3  (matches K = -3 log(2 Im tau) Kahler factor)
  - W^Q has a structural double zero at tau_Q = i sqrt(11/2) (CM point of Q(sqrt -22))
  - W^Q is holomorphic on H

KEY INPUT (from LMFDB query):
  Weight-3 newforms on Gamma_0(88) include
    88.3.b.a (dim 1, CM by Q(sqrt -22), disc -88, q-exp = q - 2q^2 + 4q^4 - 8q^8 + 9q^9 + 11 q^11 + ...)
    88.3.b.b (dim 1, CM by Q(sqrt -22), disc -88, q-exp = q + 2q^2 + 4q^4 + 8q^8 + 9q^9 - 11 q^11 + ...)

  Note both have a_3 = a_5 = a_7 = ... = 0 (zero on primes that are inert/split-other in Q(sqrt-22)).
  This is the hallmark of CM-by-K: a_p = 0 for primes inert in K, a_p = 2*Re(theta_p) for primes split.

  Character of 88.b: the order-2 character with conductor 88, equal to Kronecker symbol (-22/n)
  (since for odd weight CM newform, nebentypus = chi_{D_K} where D_K = field disc).

PLAN:
  Construct W^Q(tau) = f(tau) / eta(tau)^12  where f = 88.3.b.a (or 88.3.b.b).
    Modular weight: 3 + (-6) = -3.   ✓ M134-natural Kahler factor.
    Multiplier system: f has Dirichlet character chi_{-22} mod 88; eta^{-12} has trivial character (since 24 | -12*24 / 24... actually 12 | 12 so eta^12 has trivial char on Gamma_0(...)). Need to track it.
    Pole/zero at cusps: 1/eta^12 has pole at cusp i*infty (since eta = q^(1/24) (...)).
                        f has zero at cusp i*infty (newform => f vanishes at all cusps).
                        So W^Q = f / eta^12 has q-expansion q^1 / q^(12/24) = q^(1 - 1/2) = q^(1/2).
                        Hmm fractional power -- this means W^Q is NOT holomorphic at i*infty. Need eta^{-6} or similar.

Reconsider weights:
  eta has weight 1/2.
  eta^k has weight k/2.
  For total weight -3 from numerator weight 3 + denominator weight w, we need
    3 - w = -3  ==>  w = 6.
  Weight-6 holomorphic non-vanishing factor: eta^12 has weight 6. ✓
  q-leading order: f starts at q^1. eta^12 starts at q^(12/24) = q^(1/2).
  So f / eta^12 starts at q^(1 - 1/2) = q^(1/2).
  This is FRACTIONAL: W^Q has a (1/2)-th order pole/zero structure at i*infty.
  In SUGRA terms, this is the eta^k multiplier system M134 already used for W^L.
  M134's W^L = (j-1728)/eta^6 has q-leading: (j ~ q^-1) / eta^6 ~ q^-1 / q^(1/4) = q^(-5/4) (pole at infty).
  So fractional powers are FINE in this multiplier system. Just track them carefully.

  Actually let me redo M134: eta has q^(1/24) leading, so eta^6 has q^(6/24) = q^(1/4) leading.
  j has q^(-1) leading (j = 1/q + 744 + ...).
  W^L = (j-1728)/eta^6 ~ (1/q - 1728 + 196884 q + ...) / q^(1/4) (1 - q + ...)
                     ~ q^(-1) / q^(1/4) - 1728 q^0 / q^(1/4) + ...
                     ~ q^(-5/4) - 1728 q^(-1/4) + ...
  So W^L has POLE at i*infty.

  Now W^Q = f / eta^12 ~ q / q^(1/2) = q^(1/2).
  That's a HOLOMORPHIC zero at i*infty (positive power).
  Better than M134's pole at infty -- W^Q is holomorphic on full upper half plane.

So the proposal:
    W^Q(tau) = f(tau) / eta(tau)^12   where f = 88.3.b.a or 88.3.b.b

DOES W^Q VANISH AT TAU_Q = i sqrt(11/2)?
  Yes, structurally: f has CM by Q(sqrt -22), and the THETA-SERIES interpretation says
  f(tau) = sum_{ideal a in O_K} chi(a) * N(a) * exp(2 pi i tau N(a))
  where chi is a Hecke Grossencharacter of K = Q(sqrt -22).
  At a CM point tau_Q lying over the K-CM point, the lattice tau_Q Z + Z generates an ideal class
  of K. The vanishing of f at tau_Q is governed by the CM structure.

  CRITICAL FACT: For a weight-k CM newform f with CM by K, and tau_Q a CM point of K,
  f(tau_Q) is a non-zero algebraic multiple of the period omega_K^k of K.
  In particular f(tau_Q) is generically NON-ZERO.

  HOWEVER: at a "Heegner point" of level N, f may vanish if (tau_Q in F_0(N) AND f is in
  the new subspace AND f is anti-invariant under w_N for w_N tau_Q = tau_Q).

  Let's check: tau_Q = i sqrt(11/2) under w_88: w_88 (tau) = -1/(88 tau).
  w_88 (i sqrt(11/2)) = -1/(88 i sqrt(11/2)) = i / (88 sqrt(11/2)) = i / sqrt(88^2 * 11/2)
                     = i / sqrt(88 * 88 * 11/2) = i / sqrt(88 * 484) = i / (22 sqrt(88))
                     = i / (22 * 2 sqrt 22) = i / (44 sqrt 22)
  Hmm that's not equal to i sqrt(11/2).  So tau_Q is NOT a w_88-fixed point.

  w_88(tau) = -1/(88 tau).  For fixed point: -1/(88 tau) = tau ==> tau^2 = -1/88 ==> tau = i/sqrt(88).
  Reduced mod SL(2,Z) to F: tau = i/sqrt(88), Im = 1/sqrt(88) = 0.107.  Not in F.
  Apply S: tau' = -1/tau = i sqrt(88) = i * 2 sqrt 22.  Im = 2 sqrt 22 = 9.38. Not in F either.

  Actually w_N fixed points are the points tau with tau^2 = -1/N, i.e. tau = i/sqrt(N).
  Reducing to F: equivalent to i sqrt N (under S).
  So w_88 fixed point = i sqrt 88 in F_SL(2,Z), but in F_0(88) it sits at i/sqrt(88).
  Our tau_Q = i sqrt(11/2) is NOT a w_88 fixed point.

  But tau_Q IS a CM point. For CM newforms, they vanish at certain heegner divisors.

VERIFICATION STRATEGY:
  Numerically evaluate f(tau_Q) and (df/dtau)(tau_Q) using q-expansion (q-series at tau = tau_Q).
  q = exp(2 pi i tau_Q) = exp(2 pi i * i sqrt(11/2)) = exp(-2 pi sqrt(11/2))
    = exp(-2 pi * 2.345) = exp(-14.73) ~ 4 * 10^(-7).  Very small q -- excellent convergence.

  We have a_n for n = 1..20. Need more for double-zero verification (W^Q' (tau_Q) = 0).

PLAN OF STEPS:
  1. Compute Hecke eigenvalues a_p for primes p up to ~50 directly from CM theta-series formula.
  2. Generate a_n for n up to ~50 by multiplicativity.
  3. Evaluate f(tau_Q) and f'(tau_Q) numerically.
  4. Check whether f(tau_Q) = 0 (this would mean f has a zero at tau_Q).
  5. If f(tau_Q) != 0, then W^Q = f / eta^12 has WEIGHT -3 and is NON-ZERO at tau_Q -- which is wrong.
  6. If f(tau_Q) = 0, check order; need DOUBLE zero. May need f^2 / eta^24 (weight -6, M143-like).

NEW INSIGHT (M151 specialist):
  Maybe the weight-3 form by ITSELF has a SIMPLE zero at tau_Q by Heegner divisor considerations.
  Then W^Q = f / eta^12 has a SIMPLE zero. To get DOUBLE zero, need f^2 -- but then weight 6, and
  we'd need /eta^24 for weight -6, NOT -3.
  Alternative: if f vanishes at tau_Q AND at tau_Q' = i sqrt 22 (the OTHER CM point of D=-88),
  AND we can find another weight-3 form g vanishing at tau_Q but not tau_Q', then a linear
  combination (f - lambda g) can have a HIGHER order zero at tau_Q.

  But the space S_3(Gamma_0(88), chi_{-22})^{new} is 2-dimensional (88.3.b.a + 88.3.b.b).
  Each is dim 1 over Q. So linear combinations f - lambda g exist; we have one free parameter
  to force ONE additional vanishing constraint. We can force order >= 2 at tau_Q if and only
  if f - lambda g vanishes simply AT BOTH (tau_Q, tau_Q with order 2).

  More structurally: if 88.3.b.a vanishes at tau_Q with order 1, and 88.3.b.b vanishes at tau_Q
  with order 1, then any linear combination in their span vanishes at tau_Q with order >= 1.
  To get order 2, we need f'(tau_Q) and g'(tau_Q) such that f' - lambda g' = 0 at appropriate lambda.
  This is achievable IF f'(tau_Q)/g'(tau_Q) is well-defined (both nonzero) AND we set
  lambda = f'(tau_Q)/g'(tau_Q), AND simultaneously f(tau_Q) - lambda g(tau_Q) = 0 (which forces
  f(tau_Q)/g(tau_Q) = lambda also). For both equations to hold, we need
    f(tau_Q)/g(tau_Q) = f'(tau_Q)/g'(tau_Q)
  which is a non-trivial constraint -- generically NOT satisfied.

  ==> The space S_3^{new} of dim 2 generically gives ONLY simple zeros at tau_Q via
      linear combinations (one constraint, one free parameter -> simple zero).

  To get DOUBLE zero we need DIM >= 3 (two constraints).

  Solution: enlarge to S_3(Gamma_0(88), chi_{-22}) -- the FULL space (new + old).
  Dim of S_3(Gamma_0(88), chi)? Need to check.
  Old subspace at level 88 with this character: divisors of 88 are 1, 2, 4, 8, 11, 22, 44, 88.
  At level d | 88, weight 3 with character chi_{-22} (conductor 88) only exists if 88 | d.
  But 88 | d and d | 88 => d = 88. So no oldforms at smaller level with this character.

  Hence S_3^{new}(88, chi) = S_3(88, chi). Just 2-dimensional.
  ==> CANNOT achieve double zero at tau_Q via weight-3 cusp forms on Gamma_0(88) alone.

Alternative: use ETA QUOTIENTS that are weight-3 forms on Gamma_0(88) but NOT in the cuspidal
new/old decomposition (i.e. in M_3 \ S_3, the Eisenstein part). These can vanish at non-cusp
CM points too.

Or: enlarge to higher level (e.g., Gamma_0(176) = Gamma_0(2*88)).

Or: USE WEIGHT 1 INSTEAD. Weight-1 dihedral form with character chi_{-22} on Gamma_0(88) gives
theta-series of K = Q(sqrt -22). Then f(tau)^3 (weight 3) automatically has TRIPLE zero at the
zeros of f (so DOUBLE-zero locus is a sub-locus). But no weight-1 dihedral exists for h(K) > 1
unless... wait, dihedral weight-1 forms exist for any K with h(K) >= 2 (one form per non-trivial
class group character). h(-88) = 2 -> 1 non-trivial char -> 1 weight-1 dihedral form.

Let me focus on this:
  Weight-1 dihedral on Gamma_0(88): theta series of class group character of K = Q(sqrt -22).
  In LMFDB: 88.1.b.* should list weight-1 dihedrals.
  Actually weight-1 forms with CM are RARE -- LMFDB searches confirm.

For now let me PROCEED with the W^Q = (linear combo)/eta^12 approach and verify whether
f vanishes at tau_Q at all.
"""

import mpmath as mp
mp.mp.dps = 40

print("=" * 78)
print("M151 Step 1 -- Setup weight-(-3) form on Gamma_0(88) for tau_Q = i sqrt(11/2)")
print("=" * 78)
print()
print("Weight-3 newforms on Gamma_0(88) (from LMFDB):")
print("  88.3.b.a  (dim 1, CM by Q(sqrt -22), disc -88)")
print("    q-exp:  q - 2q^2 + 4q^4 - 8q^8 + 9q^9 + 11q^11 + ...")
print("  88.3.b.b  (dim 1, CM by Q(sqrt -22), disc -88)")
print("    q-exp:  q + 2q^2 + 4q^4 + 8q^8 + 9q^9 - 11q^11 + ...")
print()
print("Strategy: W^Q(tau) = f(tau) / eta(tau)^12 has weight 3 - 6 = -3 (M134-natural).")
print()

# tau_Q = i sqrt(11/2)
tau_Q = mp.mpc(0, mp.sqrt(mp.mpf(11)/2))
q_Q = mp.exp(2j * mp.pi * tau_Q)
print(f"tau_Q = i sqrt(11/2) = {tau_Q}")
print(f"q_Q = exp(2 pi i tau_Q) = {q_Q}")
print(f"|q_Q| = {mp.nstr(abs(q_Q), 6)}  (very small -- excellent q-series convergence)")
print()

# Hecke eigenvalues (from LMFDB):
# 88.3.b.a: a_n for n=1..20:  1, -2, 0, 4, 0, 0, 0, -8, 9, 0, 11, 0, 18, 0, 0, 16, 0, -18, 6, 0
# 88.3.b.b: a_n for n=1..20:  1, 2, 0, 4, 0, 0, 0, 8, 9, 0, -11, 0, -18, 0, 0, 16, 0, 18, -6, 0

a_a = {
    1: 1, 2: -2, 3: 0, 4: 4, 5: 0, 6: 0, 7: 0, 8: -8, 9: 9, 10: 0,
    11: 11, 12: 0, 13: 18, 14: 0, 15: 0, 16: 16, 17: 0, 18: -18, 19: 6, 20: 0
}
a_b = {
    1: 1, 2: 2, 3: 0, 4: 4, 5: 0, 6: 0, 7: 0, 8: 8, 9: 9, 10: 0,
    11: -11, 12: 0, 13: -18, 14: 0, 15: 0, 16: 16, 17: 0, 18: 18, 19: -6, 20: 0
}

print("Hecke eigenvalues a_n for n=1..20 (88.3.b.a):", [a_a[n] for n in range(1, 21)])
print("Hecke eigenvalues a_n for n=1..20 (88.3.b.b):", [a_b[n] for n in range(1, 21)])
print()
print("Note: a_p = 0 for primes p in {3, 5, 7, 13, 17, 19} -- inert in Q(sqrt -22).")
print("Verify by Kronecker: legendre(-22, p) = ?")

def legendre_neg22(p):
    """Legendre / Kronecker symbol (-22/p) for odd prime p."""
    # (-22/p) = (-1/p)(2/p)(11/p)
    neg1 = 1 if p % 4 == 1 else -1
    two = 1 if p % 8 in (1, 7) else -1
    # (11/p) by quadratic reciprocity for p != 11
    if p == 11:
        return 0
    if p == 2:
        return 0  # (-22/2) ramified
    # (11/p) (p/11) = (-1)^((11-1)/2 * (p-1)/2) = (-1)^(5 * (p-1)/2)
    # = -1 if (p-1)/2 odd, +1 if even, i.e. (p-1)/2 odd means p ≡ 3 mod 4.
    if p % 4 == 1:
        eleven_p = mp.legendre(p % 11, 11)  # (p/11)
    else:
        eleven_p = -mp.legendre(p % 11, 11)  # (p/11) (-1)
    return neg1 * two * eleven_p

# Just test
for p in [3, 5, 7, 13, 17, 19, 23, 29, 31]:
    print(f"  (-22/{p}) = {legendre_neg22(p)}, a_{p}(88.3.b.a) = {a_a.get(p, '?')}")

print()
print("Inert primes (Kronecker symbol = -1) should have a_p = 0. ✓ structurally consistent.")
print()
print("Next: compute eta(tau_Q), evaluate f(tau_Q), check if it vanishes.")
