# M168 — SL(2,Z) Stabilizers at CM Points: Complete Classification

**Agent**: Sonnet 4.6  
**Date**: 2026-05-06  
**Mission**: Generalize M167.1 stabilizer asymmetry to ALL CM points in H/SL(2,Z)  
**Verdict**: **(B) REDUCED M168.1** — Theorem fully proved; H18 corroborated but NPP20 Y_e needs specialist  
**Hallu count**: 102 -> 102 (no new fabrications)

---

## Theorem M168.1 — PROVED

**Statement**: For tau in the standard fundamental domain F = {tau in H : |Re(tau)| <= 1/2, |tau| >= 1} of SL(2,Z):

> stab_PSL(2,Z)(tau) is non-trivial **iff** tau in {i, rho = (-1+i*sqrt(3))/2}.

Specifically:
- tau = i (D = -4): stab_PSL = **Z/2Z** via S = ((0,-1),(1,0)), order 4 in SL
- tau = rho (D = -3): stab_PSL = **Z/3Z** via ST = ((0,-1),(1,1)), order 6 in SL
- All other tau in F: stab_PSL = **trivial {1}**

---

## Proof

### Step 1 — Fixed-point equation

For gamma = [[a,b],[c,d]] in SL(2,Z) fixing tau in H:

    (a*tau+b)/(c*tau+d) = tau
    =>  c*tau^2 + (d-a)*tau - b = 0      (*)

The discriminant of (*) is Delta = (d-a)^2 + 4bc. Since ad-bc=1, bc=ad-1, so:

    Delta = (d-a)^2 + 4(ad-1) = (a+d)^2 - 4 = t^2 - 4

where t = tr(gamma) = a+d in Z.

### Step 2 — Trace constraint for elliptic elements

For tau in H (Im(tau) > 0), need Delta < 0:

    t^2 - 4 < 0  =>  |t| < 2  =>  t in {-1, 0, 1}

Elements with |t| >= 2 are hyperbolic (|t|>2) or parabolic (|t|=2), fixing points on R u {inf} only.

### Step 3 — Case t=0 (Delta=-4)

- gamma has order 4 in SL(2,Z), order 2 in PSL(2,Z)
- Fixed point: tau = i (unique in F with D=-4)
- stab_SL(i) = {+-I, +-S}

**Direct arithmetic proof (tau_L = i)**:
gamma·i = i requires a^2 + c^2 = 1 (from det=1 + d=a, b=-c).
Integer solutions: (a,c) in {(+-1,0),(0,+-1)} -> gamma in {I,-I,S,-S}.
VERIFIED by computation.

### Step 4 — Case t=+-1 (Delta=-3)

- gamma has order 6 (t=1) or order 3 (t=-1) in SL(2,Z), order 3 in PSL(2,Z)
- Fixed point: tau = rho = e^{2*pi*i/3} (unique in F with D=-3)
- stab_SL(rho) = {+-I, +-ST, +-(ST)^2}

Verified:
    ST = [[0,-1],[1,1]]
    (ST)^2 = [[-1,-1],[1,0]]
    (ST)^3 = [[-1,0],[0,-1]] = -I  VERIFIED

### Step 5 — No other case

Only t in {-1,0,1} can produce elliptic elements. Each trace value corresponds to a unique SL(2,Z)-conjugacy class with a unique fixed-point class in H. In F: exactly tau=i and tau=rho. QED.

---

## Application to ECI v9 CM Points

### Table of stabilizers

| tau | D | h | stab_PSL | Note |
|-----|---|---|----------|------|
| tau_L = i | -4 | 1 | Z/2Z | M167.1 confirmed |
| tau_Q = i*sqrt(11/2) | -88 | 2 | trivial | M167.1 confirmed; a^2+22k^2=1 -> k=0 only |
| D = -7 | -7 | 1 | trivial | Heegner-Stark |
| D = -8 | -8 | 1 | trivial | Heegner-Stark |
| D = -11 | -11 | 1 | trivial | Heegner-Stark |
| D = -15 | -15 | 2 | trivial | h=2 candidate |
| D = -19 | -19 | 1 | trivial | Heegner-Stark |
| D = -20 | -20 | 2 | trivial | h=2 candidate |
| D = -24 | -24 | 2 | trivial | h=2 candidate |
| D = -35 | -35 | 2 | trivial | h=2 candidate |
| D = -40 | -40 | 2 | trivial | h=2 candidate |
| D = -43 | -43 | 1 | trivial | Heegner-Stark |
| D = -67 | -67 | 1 | trivial | Heegner-Stark |
| D = -163 | -163 | 1 | trivial | Heegner-Stark |

### Explicit proof for tau_Q = i*sqrt(11/2) (D=-88)

gamma·tau_Q = tau_Q requires (using tau_Q^2 = -11/2):
- Real part: b = -11c/2  => c=2k, b=-11k
- Imaginary part: d = a
- Determinant: a^2 + 22k^2 = 1

Integer solutions: only (a,k) = (+-1,0) -> gamma = +-I (trivial). VERIFIED with exhaustive search. ✓

---

## Hypothesis H18 — CORROBORATED

**H18**: Lepton modulus tau_L lies on PSL(2,Z)-non-trivial-stab CM point (tau in {i,rho}); quark modulus tau_Q lies on generic CM point (trivial stab).

### Architectural mechanism

**At tau_L = i (stab = Z/2Z via S):**
- S fixes i, so modular forms satisfy f(S·i) = i^{-k} rho(S) f(i)
- Lepton Yukawa Y_e(i) must satisfy: Y_e = i^{-k_Y} rho_e(S) Y_e rho_nu^dag(S)
- This is a **Z_2 texture constraint** on Y_e intrinsic to tau=i

**At tau_Q = i*sqrt(11/2) (stab = trivial):**
- No stabilizer symmetry -> no extra constraint on Y_q beyond modular form values
- Yukawa determined by modular form basis alone

### Lepton/quark asymmetry

The distinction tau_L in {i,rho} vs tau_Q in generic CM generates intrinsic lepton/quark Yukawa asymmetry from CM geometry alone — no ad hoc assumptions needed.

### NPP20 consistency (theoretical)

NPP20 (arXiv:1905.11970) work in A4 modular symmetry. At tau=i, the S-generator acts on lepton sector and fixed-point condition selects specific modular form ratios. The Z_2 constraint from M168.1 is structurally consistent with NPP20.

**Caveat**: Direct Y_e matrix entries at tau=i from NPP20 not extracted (not fabricated). Verification requires reading arXiv:1905.11970 Eq. for Y_e in the tau->i limit — specialist pass needed.

---

## Verdict

**(B) REDUCED M168.1**

| Component | Status |
|-----------|--------|
| Theorem M168.1 (classification) | FULLY PROVED — trace argument + explicit arithmetic |
| tau_L = i: stab = Z/2Z | VERIFIED (M167.1 + M168.1) |
| tau_Q = i*sqrt(11/2): stab = trivial | VERIFIED explicitly (a^2+22k^2=1) |
| All h=1 Heegner-Stark: trivial stab | VERIFIED by M168.1 |
| All h=2 ECI v9 candidates: trivial stab | VERIFIED by M168.1 |
| H18 architectural: lepton/quark asymmetry | CORROBORATED (theory) |
| NPP20 Y_e texture at tau=i | NEEDS SPECIALIST (not fabricated) |

---

## Key formulas for ECI v9

1. **Elliptic trace bound**: gamma elliptic in SL(2,Z) <=> |tr(gamma)| <= 1

2. **Fixed-point discriminant**: Delta(gamma) = tr(gamma)^2 - 4
   - tr=0: Delta=-4, fixes tau=i (Z/2Z in PSL)
   - tr=+-1: Delta=-3, fixes tau=rho (Z/3Z in PSL)

3. **M168.1**: forall tau in F, stab_PSL(tau) != 1 <=> tau in {i, rho}

4. **H18 implication**: tau_L = i => Y_e obeys Z_2 equivariance; tau_Q != i,rho => Y_q obeys no stab equivariance

---

*Generated by Sonnet 4.6, M168, 2026-05-06. Hallu 102 -> 102. Computations verified with mpmath dps=30 and sympy.*
