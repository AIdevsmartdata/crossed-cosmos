#!/usr/bin/env python3
"""
M155 / Step 1 -- Verbatim re-Read of Mohseni-Vafa arXiv:2510.19927 §3-4.

PURPOSE: Lock down EXACTLY what M-V's Tables 1-2 classification depends on.

VERBATIM EXTRACTS (pages 13-15 of v3, 20 Feb 2026):

§4.1 Symmetries of the Scalar Potential
========================================
"We investigate the behavior of the scalar potential at the symmetry points
 tau_0 = i, omega, which are stabilized by S and ST, respectively. We will
 assume that at these points V is regular."

(4.1) V = e^K [K^{tau bar tau} D_tau W D_bar tau bar W - 3 |W|^2]
(4.2) D_tau W = d_tau W + (d_tau K) W
(4.3) D_tau W = d_tau (e^G) / (e^K bar W)
(4.4) D_tau W -> (c tau + d)^{2-k} D_tau W  (modular weight 2-k)
(4.5) d_tau V -> (c tau + d)^2 d_tau V
(4.6) tau=i; S: d_tau V -> -d_tau V
(4.7) tau=omega; ST: d_tau V -> e^{2 pi i / 3} d_tau V
(4.8) d_tau V|_{tau_0} = 0     -- CRITICALITY GUARANTEED BY MODULARITY

§4.2 No Multiplier System; Forms of Even Weight
================================================
"In this section we will assume symmetry points are regular and consider the
 case in which there is no multiplier system and the forms are of even weight."

(4.11) W(i)         -> (i)^{-k} W(i)
(4.12) D_tau W(i)   -> (i)^{2-k} D_tau W(i)
(4.13) W(i) = 0          for k != 4n
(4.14) D_tau W(i) = 0    for k - 2 != 4n

(4.17) W(omega) = 0          for k != 6n
(4.18) D_tau W(omega) = 0    for k - 2 != 6n

  Table 1: Vacua at tau = i for even k:
  ---------------------------------------
  k       2    4    6    8    10   12
  W       0    !=0  0    !=0  0    !=0
  D_tau W !=0  0    !=0  0    !=0  0
  V       dS   AdS  dS   AdS  dS   AdS

  Table 2: Vacua at tau = omega for even k:
  -----------------------------------------
  k       2    4    6    8    10   12
  W       0    0    !=0  0    0    !=0
  D_tau W !=0  0    0    !=0  0    0
  V       dS   Mink AdS  dS   Mink AdS

§5 Discussion (page 16):
"It would be interesting to draw conclusions about the sign of the Hessian at
 the elliptic points directly from symmetry considerations (perhaps combined
 with other features) and thereby make statements about (in)stability. One
 could also EXTEND THE ANALYSIS TO CONGRUENCE SUBGROUPS AND MULTI-MODULUS MODULI
 SPACES, where additional elliptic points further enrich the vacuum structure."

------------------------------------------------------------------------------
DEPENDENCIES IDENTIFIED:
------------------------------------------------------------------------------

(D1) Modulus weight k mod 12  (PRIMARY axis -- both Tables 1 and 2)
(D2) Stabilizer subgroup of tau_0 in SL(2,Z):
     - tau=i:     <S>     order 2 in PSL(2,Z), gauge symmetry Z_4
     - tau=omega: <ST>    order 3 in PSL(2,Z), gauge symmetry Z_6
(D3) Multiplier system m mod 24 (treated by absorbing into k' = k + m/2 in §4.3)

NOT DEPENDENCIES:
- (E1) Discriminant D of CM lattice -- ABSENT
- (E2) Class number h_K           -- ABSENT
- (E3) Heegner / non-Heegner      -- ABSENT
- (E4) Atkin-Lehner level         -- ABSENT
- (E5) Congruence subgroup        -- §5 EXPLICITLY says this is OPEN extension

------------------------------------------------------------------------------
KEY MECHANISM (M-V's logic):
------------------------------------------------------------------------------

The classification works because:

  1. tau_0 is FIXED by some non-trivial gamma in SL(2,Z) (gamma * tau_0 = tau_0)
  2. W has modular weight -k:  W(gamma tau) = (c tau + d)^{-k} W(tau)
  3. At tau_0: W(tau_0) = (c tau_0 + d)^{-k} W(tau_0)
     => either W(tau_0) = 0  OR  (c tau_0 + d)^{-k} = 1
  4. The factor (c tau_0 + d) at fixed point has finite order:
     - tau=i, gamma=S=(0,-1;1,0): c i + d = -i + 0 = -i; (-i)^{-k} = i^k
       i^k = 1 <=> k = 0 mod 4
     - tau=omega, gamma=ST: c omega + d = ... = e^{i pi / 3}; cube root condition
       e^{-i k pi / 3} = 1 <=> k = 0 mod 6
  5. Same logic for D_tau W (weight 2-k):  vanishing condition shifted by 2.

CRUCIAL: This only works because tau_0 is FIXED IN SL(2,Z) (h=1 CM points i, omega).
For h>=2 CM points like tau_Q = i sqrt(11/2), tau_Q is NOT fixed by any non-trivial
element of SL(2,Z). Instead, it's fixed by an element of a CONGRUENCE SUBGROUP (e.g.
Atkin-Lehner involution w_N on Gamma_0(N)).

------------------------------------------------------------------------------
WHY h>=2 IS A FUNDAMENTALLY DIFFERENT REGIME:
------------------------------------------------------------------------------

For SL(2,Z) on the upper half-plane H, the orbit-stabilizer theorem gives:
  - Generic tau: stabilizer = {1, -1}  (trivial in PSL(2,Z))
  - tau = i:     stabilizer = <S>      order 2 in PSL(2,Z) (Z_4 in SL(2,Z))
  - tau = omega: stabilizer = <ST>     order 3 in PSL(2,Z) (Z_6 in SL(2,Z))
  - These are the ONLY two orbits with non-trivial stabilizer.

For Gamma_0(N) (Hecke congruence subgroup of level N), there can be ADDITIONAL
elliptic points. For Atkin-Lehner involution w_N on X_0(N), the fixed points are
at tau = i sqrt(N) (for generic N) -- and these are NOT fixed by SL(2,Z).

For our quark sector:
  K = Q(sqrt -22), D = -88, h = 2
  Class [1]: form (1, 0, 22), tau = i sqrt 22
  Class [2]: form (2, 0, 11), tau_Q = i sqrt(11/2) = i sqrt 22 / 2

These are NOT in the SL(2,Z) orbit of each other. They're related by Atkin-Lehner
w_22 on Gamma_0(22) (or w_88 on Gamma_0(88)).

The M-V classification CANNOT directly apply at these points because:
  (a) tau is not fixed by SL(2,Z) (no S or ST analog)
  (b) W transforms under Gamma_0(N) not full SL(2,Z) -- different multiplier system
  (c) Class group acts on the SET of class representatives, not on each separately

------------------------------------------------------------------------------
WHAT A TABLES 3-4 EXTENSION WOULD LOOK LIKE:
------------------------------------------------------------------------------

For h=2 CM at K = Q(sqrt -D), D = 88 (our case), we have:
  - tau_a = principal class rep (form (1, 0, D/4) for D = 0 mod 4)
  - tau_b = non-principal class rep (form (a, 0, D/(4a)) for some a | D/4)

The relevant symmetry group is now Gamma_0(N) where N = level of CM ideal.
For class [a]:
  - Stabilizer in Gamma_0(N) is some subgroup (typically <w_N> Atkin-Lehner)
  - Modular weight under Gamma_0(N) determines classification

Tables 3-4 conjecture (M155 PROPOSAL):
  Table 3: tau_a = i sqrt(D/4)     (principal CM rep, fixed by w_N on Gamma_0(N))
  Table 4: tau_b = i sqrt(D/(4 a^2))  (non-principal CM rep)
  Each as function of:
    - weight k mod 4 (for w_N involution: w_N^2 = -id, like S^2 = -id)
    - class index [a] (does class group action shift k effectively?)

ACTUAL CLASSIFICATION QUESTION FOR M155:
  Is the N=1 SUGRA scalar potential V_F invariant under class group action?
  Or does V_F take DIFFERENT values at different class representatives?

ANSWER from M-V framework:
  V_F is built from K and W. K = -3 log(2 Im tau) is invariant under SL(2,Z),
  but tau_a and tau_b have DIFFERENT Im values:
    Im(tau_a) = sqrt(D/4) = sqrt 22 = 4.690
    Im(tau_b) = sqrt(D/(4 a^2)) = sqrt(11/2) = 2.345
  e^K = (2 Im tau)^{-3}: differs by (Im tau_b / Im tau_a)^3 = (2.345/4.690)^3 = 1/8

  W is a modular form (weight -k under whatever group); for h=2 CM, W must be a
  modular form for Gamma_0(N), and W can take DIFFERENT VALUES at different class
  reps. In fact, W(tau_a) and W(tau_b) are CM-conjugate algebraic numbers
  (Galois orbit of class group), and |W(tau_a)|^2 + |W(tau_b)|^2 is rational.

  GENERICALLY V_F(tau_a) != V_F(tau_b).

  CONJECTURE: V_F is EQUIVARIANT under class group, not invariant.
  Specifically, V_F(tau_a) and V_F(tau_b) are ALGEBRAIC CONJUGATES.
"""

print("M155 / Step 1 -- M-V re-Read complete")
print("=" * 70)
print()
print("Tables 1-2 depend on:")
print("  (D1) k mod 12 (PRIMARY)")
print("  (D2) Stabilizer in SL(2,Z): <S> for tau=i, <ST> for tau=omega")
print("  (D3) Multiplier m mod 24 (absorbed via k' = k + m/2)")
print()
print("Tables 1-2 do NOT depend on:")
print("  - Discriminant D of CM lattice")
print("  - Class number h_K")
print("  - Heegner / non-Heegner condition")
print("  - Atkin-Lehner level N")
print()
print("M-V §5 explicitly defers congruence-subgroup extension as OPEN.")
print()
print("For h=2 CM Q(sqrt -22), tau_Q = i sqrt(11/2) is NOT in any orbit")
print("of SL(2,Z) singular point i, omega, infty.")
print("=> M-V framework CANNOT apply directly.")
print()
print("The analog of Tables 1-2 for h=2 CM requires:")
print("  (a) Replace SL(2,Z) by Gamma_0(N) for some level N | (4 |D_K|)")
print("  (b) Stabilizer = Atkin-Lehner involution w_N (acts as w_N^2 = -id)")
print("  (c) Account for class group action: V_F(tau_a) vs V_F(tau_b)")
print("  (d) Forms of weight k under Gamma_0(N) (not SL(2,Z))")
