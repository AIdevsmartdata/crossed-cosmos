"""
M164 sub-task: synthesis check on Kanno-Watari 2012.01111 vs ECI v9
two-modulus W structure.

ECI v9 W (M134 + M151):
  W(tau_L, tau_Q) = c_L (j(tau_L) - 1728)/eta(tau_L)^6
                  + c_Q H_{-88}(j(tau_Q))^2 f_{88.3.b.a}(tau_Q) / eta(tau_Q)^12

Kanno-Watari arXiv:2012.01111 framework:
  Y = (X^(1) x X^(2))/Z_2  Borcea-Voisin K3 x K3 orbifold (CY 4-fold)
  Or:  Y = (E_phi x E_tau x X^(2))/Z_2^2  (eq 4 of Kanno-Watari)
  W = int_Y G ^ Omega_Y  flux superpotential

For singular K3 surface X^(i) with CM-type complex structure:
  - rank(T_X^(i)) = 2, rank(S_X^(i)) = 20
  - T_X^(i) ⊗ Q has CM by imaginary quadratic field K^(i)
  - tau_X^(i) is "the" CM point in upper half plane

For ECI v9:
  X^(1) singular K3 with K^(1) = Q(i),     tau_X^(1) = i           (D = -4,  h = 1)
  X^(2) singular K3 with K^(2) = Q(sqrt-22), tau_X^(2) = i sqrt(11/2) (D = -88, h = 2)

The Borcea-Voisin orbifold Y has two complex structure moduli that, on a CM
locus, correspond to tau_L = tau_X^(1) and tau_Q = tau_X^(2).

Flux superpotential at CM point:
  Omega_Y = Omega_{X^(1)} ^ Omega_{X^(2)}  (modulo Z_2 quotient)
  W(tau_L, tau_Q) = sum_{a,b in flux quanta} N_{a,b} * pi_a(tau_L) * pi_b(tau_Q)

where pi_a are PERIODS of K3 over Q-basis of T_0^(i).

KEY INSIGHT (Chowla-Selberg / Gross periods):
For a CM elliptic curve E_K with CM by K = Q(sqrt-D), the period
  Omega_K = Gamma-product over residues of chi_K mod |D|
This is the Chowla-Selberg formula. For D = -4: Omega ~ Gamma(1/4)^2.
For D = -88: Omega ~ products Gamma(n/88)^{chi_{-22}(n)}.

Kanno-Watari W=0 condition translates to ALGEBRAIC vanishing of the
period integral via Hodge structure being CM-type. The flux quanta N_{a,b}
must be chosen in Q so that the linear combination of CM periods (which
are transcendental Gamma-products) cancels.

ECI v9 W is meromorphic modular form on H_L x H_Q.
Kanno-Watari W is flux superpotential, a FUNCTION on M_cpx(Y) with
discrete flux choices N_{a,b}.

These two viewpoints are NOT identical, but they have the SAME zero locus
on the CM-type locus (= our (tau_L, tau_Q) = (i, i sqrt(11/2)) point).

CONCLUSION (M164 verdict):
- (D) PARTIAL match: Kanno-Watari F-theory CM-type K3 x K3 orbifold provides
  a structural compactification framework whose vacuum locus contains the
  ECI v9 (tau_L, tau_Q) CM point. But the explicit Mohseni-Vafa modular form
  W = (j-1728)/eta^6 + H_{-88}^2 f / eta^12 is NOT directly the period
  integral of Kanno-Watari; it is the Mohseni-Vafa modular-invariance EFT
  REWRITING of that period integral near the CM point.
- (B) REDUCED in the sense that A SPECIFIC F-theory compactification
  (Kanno-Watari Borcea-Voisin K3 x K3 with X^(1) singular K3 over Q(i),
  X^(2) singular K3 over Q(sqrt-22)) is identified.
- The single specialist gap is: derive the modular form (j-1728)/eta^6
  + H^2 f/eta^12 from the period integral int_Y G ^ Omega_Y. This requires
  Hodge-theoretic computation of the period basis on T_0^(1) x T_0^(2) and
  recognizing the modular reorganization at CM-type points.
"""

print("M164 synthesis written.")
print()
print("Key correspondence:")
print("  ECI v9 tau_L = i        <->  Kanno-Watari X^(1) singular K3, K^(1) = Q(i)")
print("  ECI v9 tau_Q = i√(11/2) <->  Kanno-Watari X^(2) singular K3, K^(2) = Q(√-22)")
print()
print("Kanno-Watari W = int_Y G ^ Omega_Y (flux superpotential)")
print("ECI v9 W = (j-1728)/eta^6 + H_{-88}^2 f / eta^12 (modular form per Mohseni-Vafa)")
print()
print("Vacuum: (tau_L, tau_Q) = (i, i√(11/2)) is CM-type point in M_cpx(Y).")
print("At this point: both Kanno-Watari W = 0 (with appropriate flux)")
print("                AND ECI v9 W = 0 (forced by E_6(i) = 0 and H_{-88}(j(tau_Q)) = 0).")
print()
print("Verdict: (D) PARTIAL with strong (B) elements. Probability per prior: ~50%.")
