#!/usr/bin/env python3
"""
M134 -- ANALYTIC computation of the Hessian of V(tau) candidates at tau=i.

Strategy: Use known facts about modular forms at tau = i to get exact closed-form
expressions for the second derivatives.

KEY FACTS:
  E_4(i) = 3 G(1/4)^8 / (2 pi)^6
  E_6(i) = 0
  Delta(i) = E_4(i)^3 / 1728
  j(i) = 1728

  Ramanujan derivative formulas:
  q d/dq E_2  = (E_2^2 - E_4)/12
  q d/dq E_4  = (E_2 E_4 - E_6)/3
  q d/dq E_6  = (E_2 E_6 - E_4^2)/2
  q d/dq Delta = E_2 Delta            (so dlog Delta = E_2 d log q = 2 pi i E_2 dtau)
  q d/dq j   = -E_6/Delta * E_4^2 / something... let me derive

  Notation: 'partial' means d/dtau. Then q d/dq = (1/(2 pi i)) d/dtau.
  So d/dtau = 2 pi i q d/dq.

  Therefore:
    dE_2/dtau  = 2 pi i (E_2^2 - E_4)/12
    dE_4/dtau  = 2 pi i (E_2 E_4 - E_6)/3
    dE_6/dtau  = 2 pi i (E_2 E_6 - E_4^2)/2
    dDelta/dtau = 2 pi i E_2 Delta
    dj/dtau   = -2 pi i E_6 E_4^2 / Delta
                  (since j = 1728 E_4^3/Delta, log j = 3 log E_4 - log Delta + const,
                   d log j / dtau = 3 (E_2 E_4 - E_6)/(3 E_4) * 2pi i / 2 ... let me redo)

  Cleanly: j = 1728 E_4^3 / (E_4^3 - E_6^2), so j - 1728 = 1728 E_6^2 / (E_4^3 - E_6^2)
                                                          = E_6^2 / Delta

  Therefore  j(tau) - 1728 = E_6(tau)^2 / Delta(tau).      (*)

  This is a CRUCIAL identity:   |j-1728|^2 = |E_6|^4 / |Delta|^2.

  At tau = i, E_6 has a simple zero, so j-1728 has a double zero (consistent with
  j: H/SL(2,Z) -> C being a 2:1 map ramified at tau = i).

  d(j - 1728)/dtau = 2 E_6 (dE_6/dtau)/Delta - E_6^2 (dDelta/dtau)/Delta^2
                  = (E_6/Delta) [ 2 (dE_6/dtau) - E_6 (dDelta/dtau)/Delta ]
                  = (E_6/Delta) * 2 pi i [ (E_2 E_6 - E_4^2) - E_6 E_2 ]
                  = (E_6/Delta) * 2 pi i * (-E_4^2)
                  = -2 pi i E_6 E_4^2 / Delta

  At tau = i, E_6(i) = 0, so dj/dtau(i) = 0. Good (j has critical point at tau=i).

  d^2(j-1728)/dtau^2 = d/dtau [ -2 pi i E_6 E_4^2 / Delta ]
                     = -2 pi i [ (dE_6/dtau) E_4^2 / Delta
                                  + E_6 * 2 E_4 (dE_4/dtau) / Delta
                                  - E_6 E_4^2 (dDelta/dtau)/Delta^2 ]
  At tau = i, E_6(i) = 0, so the last two terms vanish, and only the first term survives.

  d^2 (j-1728)/dtau^2 (i) = -2 pi i * (dE_6/dtau) E_4^2 / Delta  [at tau = i]
                          = -2 pi i * [ 2 pi i (E_2 E_6 - E_4^2)/2 ] E_4^2 / Delta
                          = -2 pi i * [ -2 pi i E_4^2 / 2 ] E_4^2 / Delta            [E_6(i)=0]
                          = -2 pi i * (-pi i) E_4^4 / Delta
                          = -2 pi^2 E_4^4 / Delta              [careful with i*i = -1]

  Let me redo: -2pi i * (-pi i) = -2 pi i * (-pi i) = -2pi*(-pi)*i*i = 2 pi^2 * (-1) = -2 pi^2
  So d^2(j-1728)/dtau^2 (i) = -2 pi^2 E_4(i)^4 / Delta(i).

  Using Delta(i) = E_4(i)^3 / 1728:
    d^2(j-1728)/dtau^2 (i) = -2 pi^2 E_4(i) * 1728 = -3456 pi^2 E_4(i)
                          = -3456 pi^2 * 3 G(1/4)^8/(2 pi)^6
                          = -3456 pi^2 * 3 G(1/4)^8 / (64 pi^6)
                          = - (3456 * 3) / 64 * G(1/4)^8 / pi^4
                          = - 162 * G(1/4)^8 / pi^4

  So d^2 j/dtau^2 (i) = -162 G(1/4)^8 / pi^4.    [exact analytic formula]

  Numerically: G(1/4) ~ 3.62561, G(1/4)^8 ~ 29657.85, pi^4 ~ 97.41
    d^2 j/dtau^2 (i) ~ -162 * 29657.85 / 97.41 ~ -49315.9   (purely real and NEGATIVE)

  So near tau=i, j - 1728 ~ -1/2 * 49316 * (tau - i)^2 + ...
  And |j - 1728|^2 ~ (1/4) * 49316^2 * |tau - i|^4 ~ 6.078e8 * |tau-i|^4

  But wait -- |j - 1728|^2 is order (tau-i)^4, NOT (tau-i)^2!
  ==> V_1 has a quartic minimum, NOT a quadratic minimum!  Hessian is ZERO at tau=i.

  Hmm but the numerics gave H_xx ~ 1233 (clearly not zero)... let me re-examine.
  Actually my numerics used h=1e-3, and at tau=i the function is genuinely quartic
  (j-1728 ~ A (tau-i)^2 with A ~ 24827 from numerics, so |j-1728|^2 ~ A^2 |tau-i|^4
  ~ 6.16e8 * |tau-i|^4).

  At h=1e-3, V(i+h) - 2V(i) + V(i-h) = 2 (V(h) - V(0)) since V(i)=V(-h*shift)=V(h*shift)
  by symmetry. V at tau=i+h = (24827)^2 * h^4 = 6.16e8 * 10^-12 = 6.16e-4.
  So Vxx ~ (6.16e-4 + 6.16e-4)/h^2 = 1.232e-3 / 1e-6 = 1232.  That matches! It is the
  *quartic* term seen as a discrete second difference.

  ==> V_1 is NOT QUADRATIC near tau=i; it's QUARTIC. The "Hessian" measured by
  finite differences is artifact of the quartic shape.

  This is BAD: a quartic minimum has FLAT Hessian -> mass^2 = 0 -> moduli problem
  (massless scalar). This contradicts our naive interpretation. To be useful for
  modulus stabilization, V must have non-zero Hessian.

  REMEDY: use V = |j-1728| instead of |j-1728|^2:
    V_1' = |j(tau) - 1728|  ~  C (tau_1^2 + tau_2'^2)  near tau = i (where tau_2' = tau_2-1)
  is QUADRATIC. (Because |j-1728| ~ |A| * (tau-i)^2 -> | (tau-i) |^2 = tau_1^2 + tau_2'^2.)
  But V_1' is non-smooth (cusp at tau=i because absolute value of holo function).

  REAL REMEDY: use V_inv = |E_6|^2 / |Delta| (which is actually = |j-1728|^2 / 1)
  Wait: |j-1728| = |E_6|^2 / |Delta|.
  So V_inv2 = |E_6|^2 / |Delta| = |j(tau) - 1728|. (NOT squared.)
  This is QUADRATIC near tau = i.

  Let me verify: with E_6 ~ s (tau - i) near tau=i (s = dE_6/dtau (i) = 2 pi i (-E_4^2)/2 = -pi i E_4^2),
  E_6^2 ~ s^2 (tau-i)^2 = -pi^2 E_4^4 (tau-i)^2.
  Delta(i) = E_4^3/1728.
  E_6^2/Delta ~ -pi^2 E_4^4 (tau-i)^2 / (E_4^3/1728) = -1728 pi^2 E_4 (tau-i)^2.
  j(tau) - 1728 = E_6^2/Delta ~ -1728 pi^2 E_4(i) (tau-i)^2.
  Numerically: -1728 * pi^2 * 1.4558 * (tau-i)^2 = -24827.5 (tau-i)^2.   <-- matches numerics!

  So |j(tau) - 1728| ~ 24827.5 |tau-i|^2.

  V_inv2(tau) = |E_6(tau)|^2 / |Delta(tau)| = |j(tau) - 1728|.

  V_inv2 near tau=i: V_inv2 ~ 24827.5 |tau-i|^2 = 24827.5 (x^2 + (y-1)^2).
  Hessian: V_xx = V_yy = 2 * 24827.5 = 49655, V_xy = 0.   <-- matches numerics!

  m^2(Kahler) = (2/3) (V_xx + V_yy) = (2/3)*99310 = 66206.7.  <-- matches.

  PERFECT. So the GOOD candidate is V_inv2 = |j - 1728|, NOT |j-1728|^2.
  Equivalently V_inv2 = |E_6|^2/|Delta|.

  Mass formula:
    m^2_tau (V_inv2 candidate) = (2/3) * 2 * 1728 * pi^2 * E_4(i)
                              = (2304/1) * pi^2 * E_4(i) / 1                  -- wait
                              = (2/3) * 4 * 1728 * pi^2 * E_4(i) / 2

  Let me redo cleanly. V_inv2(tau) = |j(tau) - 1728|.
  Near tau=i: j-1728 = c (tau-i)^2 + O((tau-i)^3), c = -1728 pi^2 E_4(i).
  |j-1728| = |c| * |tau-i|^2 = 1728 pi^2 E_4(i) * (x^2 + (y-1)^2).
  So V_xx = V_yy = 2 * 1728 pi^2 E_4(i) = 3456 pi^2 E_4(i).
  m^2 = (2/3)(Vxx + Vyy) = (4/3) * 3456 pi^2 E_4(i) = 4608 pi^2 E_4(i).

  Numerically: 4608 * pi^2 * 1.4558 = 4608 * 9.8696 * 1.4558 = 66206.5.  CONFIRMED.

  And in closed form using E_4(i) = 3 G(1/4)^8/(2 pi)^6:
    m^2 = 4608 pi^2 * 3 G(1/4)^8 / (2 pi)^6
        = 4608 * 3 * pi^2 * G(1/4)^8 / (64 pi^6)
        = 13824 / 64 * G(1/4)^8 / pi^4
        = 216 * G(1/4)^8 / pi^4         [exact in units where the V_inv2 prefactor = 1]

  EXACT: m^2_tau (V = |j-1728|) = 216 G(1/4)^8 / pi^4.

  Numerics: 216 * 29657.85 / 97.41 = 216 * 304.466 = 65,765 ... close but let me re-evaluate
  G(1/4) = 3.6256099082...
  G(1/4)^8 = 3.6256099082^8 = ?
  3.6256^2 = 13.1450; 13.1450^2 = 172.79; 172.79^2 = 29856.1
  Hmm.  Let me be precise via mpmath below.
"""

import mpmath as mp
mp.mp.dps = 30

# E_4(i) closed form
G14 = mp.gamma(mp.mpf(1)/4)
E4i = 3 * G14**8 / (2*mp.pi)**6

print("="*70)
print("M134 -- analytic Hessian of V_inv2 = |j-1728| at tau=i")
print("="*70)
print(f"G(1/4)               = {G14}")
print(f"G(1/4)^8             = {G14**8}")
print(f"E_4(i) [closed form] = {E4i}")
print(f"E_4(i) numerical     = 1.45576289...")
print()

# Coefficient c in j-1728 = c (tau-i)^2 + ...
c = -1728 * mp.pi**2 * E4i
print(f"c (j-1728 leading)   = {c}")
print(f"|c|                  = {abs(c)}")
print(f"  (matches numeric ratio 24827.6: |c| should ~ 24827.6)")
print()

# Mass^2 with Kahler metric, V = |j-1728|
m2 = 4608 * mp.pi**2 * E4i
print(f"m^2 (Kahler) for V=|j-1728|: 4608 pi^2 E_4(i)")
print(f"  = {m2}")
print()

# Closed form:
m2_closed = 216 * G14**8 / mp.pi**4
print(f"m^2 closed form: 216 G(1/4)^8 / pi^4 = {m2_closed}")
print(f"  diff = {abs(m2 - m2_closed)}")
print()

# Also: m^2 in terms of E_4(i) only:
# 4608 = 4608, pi^2 factor.
# Using j-Hauptmodul normalization 1728 fixes the scale.

# What about V_1 = |j-1728|^2? It's quartic at tau=i, so the "Hessian"
# from a finite-difference test is actually fourth-order content.
# V_1 = |j-1728|^2 ~ |c|^2 |tau-i|^4 = (1728 pi^2 E_4(i))^2 (x^2 + (y-1)^2)^2.
# Quartic. Mass^2 from quadratic Taylor = 0. Moduli problem.

print("="*70)
print("V_1 = |j-1728|^2 (the candidate originally proposed)")
print("="*70)
print("V_1 ~ |c|^2 (x^2 + (y-1)^2)^2  near tau=i  (QUARTIC, not quadratic).")
print("==> Hessian at tau=i is ZERO (massless modulus). NO mass term.")
print(f"|c|^2 = {abs(c)**2}")
print()
print("Lesson: |j-1728|^2 is too FLAT at tau=i. Use V_inv2 = |j-1728| (quadratic at i).")
print()

# Cross-check vs Bianchi IX modular shadow rate lambda_modular = pi^3 / (3 ln 2)
print("="*70)
print("Cross-domain check vs Bianchi IX shadow flow rate")
print("="*70)
lambda_modular = mp.pi**3 / (3 * mp.log(2))
print(f"lambda_modular = pi^3/(3 ln 2) = {lambda_modular}")
print(f"m_tau^2 (V=|j-1728|, units of [V]) = {m2}")
print()
print("If we identify V's units of [V] = (Planck mass)^4 / (Planck mass)^2 = M_Pl^2,")
print(f"then m_tau ~ sqrt(66206) M_Pl ~ 257 M_Pl  (TRANS-PLANCKIAN!).")
print("Need a small overall coefficient lambda_V in V = lambda_V |j-1728| to make")
print("m_tau ~ Hubble during inflation (~ 1e-5 M_Pl) or m_tau ~ TeV.")
print()
print("Hubble scale H ~ 1e-5 M_Pl needs m_tau^2 ~ 1e-10 M_Pl^2 ==> lambda_V ~ 1.5e-15.")
print("That's a tiny prefactor -- typical of non-perturbative effects: e^{-S} with S~35.")
print()

# ratio m_tau^2 / lambda_modular for fun
ratio = m2 / lambda_modular
print(f"m_tau^2 / lambda_modular = {ratio}")
print(f"   ratio is O(10^4) -- not a precise universal number.")
