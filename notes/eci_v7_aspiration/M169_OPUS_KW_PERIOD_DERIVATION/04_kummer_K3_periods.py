"""
M169 — Kummer K3 X^(1) = Km(E_phi x E_tau_L) with E_phi at CM by Q(i),
E_tau_L generic with modulus tau_L in H.

For E_phi = E_i (fixed at i, CM by Q(i)):
  T_{E_phi} = Z[i] (rank 2 lattice), T_{E_phi} (x) Q = Q(i)
For E_tau generic:
  T_{E_tau} = Z^2 (rank 2 lattice), T_{E_tau} (x) Q = generic Hodge str

Kummer K3 X = Km(E_phi x E_tau) has H^2(X; Q) ~ T_{E_phi} (x) T_{E_tau} + (level 0)
  T_X = T_{E_phi} (x) T_{E_tau}     (rank 2 + 2 = 4)
  S_X = (rest), rank 18

Period domain D(T_X) signature (2, 2) is 2-complex-dim.
The point E_phi = E_i FIXED imposes a 1-dim constraint, so the moduli
sub-locus is 1-complex-dim parametrized by tau_L in H/SL(2,Z).

So tau_L is the modulus of E_tau within the family where E_phi is fixed
at i.

Holomorphic (2,0)-form: Omega(X) = dz_1 ^ dz_2 where dz_1 is on E_phi,
dz_2 on E_tau. Omega varies as
  Omega(X) = (1, tau_L, i, i tau_L) in T_X (x) C
(in basis e_1, e_2 (x) f_1, f_2 with E_phi acting by i and E_tau by tau)
or in modular form language
  Omega(X)(tau_L) = pi_E(i) . pi_E(tau_L) = (Gamma(1/4)^2/(2 sqrt pi)) . eta(tau_L)^?

The period of X over the standard generators of T_X is
  Omega(E_i, E_tau_L) = Omega(E_i) * Omega(E_tau_L)   (Kunneth)

In terms of modular forms on tau_L:
  Omega(E_tau_L) ~ 2 pi i eta(tau_L)^2  (= a/c-period of E_tau, normalised)
  Omega(E_i)     ~ Gamma(1/4)^2 / (2 sqrt pi)  ~ 3.708...

So the K3 period over Q-basis of T_X:
  pi_4(tau_L) ~ Omega(E_i) * eta(tau_L)^2

Holomorphic (2,0) ~ eta(tau_L)^2 -- which is a weight-1 modular form
with multiplier system on Gamma_0(?).

Now: the FLUX SUPERPOTENTIAL W_KW = int_Y G ^ Omega_Y on the BV fourfold
Y = (X^(1) x X^(2))/Z_2. The (4,0)-form is
  Omega_Y = Omega_{X^(1)} ^ Omega_{X^(2)}
        ~ eta(tau_L)^2 * Omega(X^(2))(tau_Q)

where Omega(X^(2)) involves D(T_0^(2)) periods.

Choose flux G in (T_0^(1) (x) T_0^(2)) (x) Q with appropriate components:
  G = sum_a N_a v_a  with N_a in Q

Then:
  W_KW = sum_a N_a * (v_a, Omega_Y)

The key claim of ECI v9 (Mohseni-Vafa modular invariance): there exists a
flux choice {N_a} such that
  W_KW(tau_L, tau_Q) ~ c_L (j(tau_L) - 1728)/eta(tau_L)^6
                    + c_Q H_{-88}(j(tau_Q))^2 f_{88.3.b.a}(tau_Q)/eta(tau_Q)^12

This is a STRONG claim. Let me check the modular weight constraint:
  W_KW transforms as Omega_Y, with weight (k_L, k_Q) = (1, 1) since each
  Omega(X^(i)) is weight 1 (proportional to eta^2 which has weight 1).

But (j-1728)/eta^6 has weight 0 - 3 = -3 (or 0 with eta^6 in denominator, weight -3).
H^2 f / eta^12 has weight 0 + 3 - 6 = -3.

So both ECI v9 W^L and W^Q have weight -3.

For the KW expression W = int G ^ Omega_Y to MATCH ECI v9 weight -3:
  W has weight -3 in tau_L and -3 in tau_Q.
  Omega_Y has weight 1 in tau_L and 1 in tau_Q. (just from eta(tau_L)^2 etc.)
  So we need to MULTIPLY by something of weight -4 in each variable.

Where does that weight -4 come from? It must come from the integration cycle
or from auxiliary form (1/eta(tau)^8 like factor).

Mohseni-Vafa (2510.19927) identify the SUGRA superpotential Kahler weight
kappa = 3 with the "modular weight kappa" of the modular form. In their
EFT, W has modular weight kappa=3 (positive convention) which corresponds
to weight -3 in the convention used here (sign convention difference).

The KW W (eq. 1) is the BARE flux-period integral with no auxiliary factor.
This is a (4,0)-form integrated over an 4-cycle, so it's a function on
M_{cpx str}^{[Y]} with modular weight 0 + 0 = "weight 0" modulo
Cocycle of Omega_Y under SL(2,Z) acting on tau_L and tau_Q.

But Omega_Y carries weight (1,1) under the identification of tau_L, tau_Q
with the K3 periods. So W_KW has weight (1, 1) -- NOT (-3, -3).

Therefore W_KW =/= W_ECI directly. They differ by a weight (-4, -4) factor.

This is the KAHLER NORMALIZATION ISSUE noted in M164 sub-tasks but never
fully resolved.

POSSIBLE RESOLUTION: include the eta^{-8} factor needed for weight matching.
But there is no eta^{-8} in KW eq. (1).

STRUCTURAL PROBLEM: KW W has weight (1, 1); ECI v9 W has weight (-3, -3).
These cannot be equal as functions on H_L x H_Q. They MUST differ.

UNLESS: the normalization of Omega_Y in KW already includes (j(tau)-1728) /
eta^6 type factor implicit in their "C^(i)" coefficients.

C^(i) := (v_(20)^(i), v_(02)^(i)) is the inner product of (2,0) and (0,2)
forms, which transforms with weight (k, kbar) under modular group.

For E_tau elliptic curve:
  Omega(E_tau) = 1 dz, so |Omega(E_tau)|^2 ~ Im(tau).
  Or in normalized basis Omega ~ eta^2 dt with t = q-coord, then
  C ~ |eta|^4 Im(tau).

Therefore the coefficient G_(20)(02) / (2 C^(i)) in eq. (53) carries
non-trivial modular weight, and the products t^(1) t^(2) similarly.

When properly normalized, the KW quadratic form does carry NEGATIVE
modular weight (because of the C^(i) factor in denominator).
"""

print("M169 Kummer K3 period analysis -- structural verification.")
print()
print("The naive comparison KW W ~ ECI v9 W fails on MODULAR WEIGHT:")
print("  KW W has weight (+1, +1) in (tau_L, tau_Q) [from Omega_Y]")
print("  ECI v9 W has weight (-3, -3) [from Mohseni-Vafa].")
print()
print("Discrepancy: weight (-4, -4) factor needed.")
print()
print("RESOLUTION pathway: the SUGRA Kahler potential K = -log(int Omega ^ Omega-bar)")
print("introduces 'normalized' superpotential W_norm = W / (Im tau)^{k/2} (... etc.)")
print("which can shift weight. But this is a Kahler-frame transformation, not")
print("a re-derivation.")
print()
print("More likely: the proper identification involves EINSTEIN frame normalization")
print("with the gravitino mass m_3/2 = e^{K/2} |W| of weight 0 by definition.")
print()
print("=> The (D)->(B) closure additionally requires a careful Kahler-frame")
print("   matching between KW W (Planck-units flux) and ECI v9 W (Kahler-")
print("   normalized SUGRA EFT). This is a NON-TRIVIAL physical step.")
