# gaps.md — Piste A6: SLE Hadamard State on Bianchi VI_0 (Sol solvmanifold)
# ECI v6.0.24/25/26 "hardest Type A rigorous-pending"
# Date: 2026-05-03 evening

## STATUS SUMMARY

**For massive conformally coupled scalar**: construction is in principle complete
modulo two hard open lemmas (C and D below). NOT a hard-negative result.

**For massless conformally coupled scalar**: IR obstruction is genuine and unresolved.
Same obstruction as Bianchi I (BN23 §4) and flat FLRW (Olbermann 2007). Hard-negative
for the massless case without IR modification.

---

## VERIFIED (sympy_check.py, all assertions pass)

| # | Claim | Method | Status |
|---|-------|--------|--------|
| 1 | [e1,e2]=0, [e3,e1]=e1, [e3,e2]=-e2 | sympy adj matrices | PASS |
| 2 | Unimodularity: tr(ad ei)=0 all i | sympy trace | PASS |
| 3 | Solvability: det(Killing form)=0 | sympy det | PASS |
| 4 | G = R^2 ⋊_{diag(e^t,e^{-t})} R, det=1 | sympy | PASS |
| 5 | Coadjoint orbit invariant: a(t)b(t)=const | sympy simplify | PASS |
| 6 | Conformal coupling xi=1/6 in 3+1D (NOT 1/8) | sympy Rational | PASS |
| 7 | Generic orbits = hyperbola ab=lambda | algebra | PASS |

**CORRECTION CAUGHT**: The task prompt stated xi=1/8. This is WRONG for 3+1 spacetime
dimensions. The correct value is xi=1/6 = (n-2)/(4(n-1)) with n=4. The value xi=1/8
is the 2+1 dimensional value. Verified symbolically.

---

## VERIFIED CITATIONS (arXiv API / web fetch)

| Citation | Claimed | Verified |
|----------|---------|----------|
| Banerjee-Niedermaier 2023 | arXiv:2305.11388 | YES — JMP 64 (2023) 113503 |
| Avetisyan-Verch 2013 | arXiv:1212.6180 | YES — CQG 30 (2013) 155006, covers Bianchi I-VII |
| Auslander-Kostant 1971 | Inventiones 14, 255-354 | YES — DOI 10.1007/BF01389744 confirmed |
| Kirillov 2004 | "Lectures on the Orbit Method", AMS | YES — GSM vol.64, 408pp, ISBN 978-0-8218-3530-2 |
| Radzikowski 1996 | CMP 179:529-553 | YES — DOI 10.1007/BF02100096 confirmed |
| Olbermann 2007 | CQG 24:5011-5030 | YES — arXiv:0704.2986 confirmed |

**NOTE ON AVETISYAN-VERCH SCOPE**: The paper title says "Bianchi I-VII". The Roman numeral
VII is the upper bound; VI_0 is a subcase of VI and is explicitly within scope of their
semidirect product R^2 ⋊_F R framework with F having real distinct eigenvalues summing
to zero. The table referred to in the task prompt (Table 1) is described as covering this
unified semidirect product family. However, the full PDF was not accessible for detailed
table extraction — this should be verified against the actual paper.

---

## OPEN ITEMS / GAPS

### Lemma C — Exact positivity of omega^2_{n,lambda}(t)
- **What is needed**: Lower bound omega^2_{n,lambda}(t) >= c*lambda^2 > 0 for all
  t in supp(f), all n, all lambda != 0, for actual Bianchi VI_0 solutions a_i(t).
- **Why hard**: The eigenvalue kappa_n(lambda, a_i(t)) of the Mathieu operator
  [-a3^{-2} d_s^2 + lambda^2(a1^{-2}e^{-2s} + a2^{-2}e^{2s})] depends on
  the ratio a1/a2, which evolves dynamically. When a1/a2 changes, the Mathieu
  parameter q = lambda^2 a1/a2 / a3^2 changes. Need to rule out eigenvalue
  crossing through zero.
- **Tools**: Floquet-Mathieu theory (Abramowitz & Stegun ch.20), monotonicity of
  Mathieu eigenvalues in q, WKB lower bounds for modified Mathieu.
- **Estimated effort**: 2-4 weeks for an analyst familiar with special functions.
- **Risk level**: LOW — the eigenvalue is structurally positive (operator is positive
  definite for lambda != 0 since potential term lambda^2*cosh(2s) > 0); need
  rigorous proof of spectral gap from zero.

### Lemma D — Adiabatic order >= 2 for Sol-sector mode functions
- **What is needed**: Analog of BN23 Lemma 2.3 for the mode functions chi_{n,lambda}
  satisfying the temporal equation (7) with Sol-sector frequency omega_{n,lambda}(t).
- **Why hard**: omega_{n,lambda}(t) is not a simple function of lambda (unlike
  Bianchi I where omega_k(t) = |k|/a(t)). Instead it is the n-th Mathieu eigenvalue
  of a time-dependent operator. Need:
  1. Asymptotic expansion of Mathieu eigenvalue in lambda as lambda -> infty
  2. Show chi_{n,lambda} agrees with the WKB mode to order lambda^{-2}
  3. Apply BN23's Gronwall argument with the Mathieu asymptotics
- **Key reference needed**: Dunster (1990) SIAM J Math Anal 21:995-1018 on Bessel
  functions of large imaginary order. Olver's asymptotics for modified Bessel K_{inu}.
  (These references NOT yet verified via arXiv — need to check.)
- **Estimated effort**: 4-8 weeks. This is the bottleneck.
- **Risk level**: MEDIUM — the Bessel-K asymptotics are known; combining them with
  BN23's functional-analytic framework requires nontrivial work but no fundamental barrier.

### Obstruction E — Full wavefront set proof
- **What is needed**: Prove WF(W_2) ⊂ N^+ x N^+ (Radzikowski criterion).
- **Strategy**: 
  1. Decompose WF(W_2) via Plancherel
  2. In each sector (n,lambda), apply propagation-of-singularities to chi_{n,lambda}
  3. Show boost (Sol fiber direction s) does not mix future/past null sheets
- **Why the boost is not catastrophic**: The boost acts within the spatial fiber (s
  direction), not along the null bicharacteristics. The temporal evolution of
  wavevectors k_i under k_dot_i = -H_i k_i is standard cosmological redshift,
  which preserves future-pointing.
- **Estimated effort**: 3-6 weeks for a microlocal analyst.
- **Risk level**: MEDIUM — the geometry is clear; the Sol fiber introduces technical
  complications in the microlocal parametrix construction.

### Obstruction F — Solvmanifold quotient (compactification)
- **What is needed**: Show SLE Hadamard state on Sol descends to Gamma\Sol for
  cocompact lattice Gamma ⊂ Sol.
- **Technical issue**: Sol admits compact quotients (Anosov diffeomorphisms on T^2).
  The Plancherel theory on Gamma\Sol is discrete with possible spectral gaps.
  Need: equivariance of SLE minimiser under Gamma, and preservation of Hadamard
  property under the quotient map.
- **Estimated effort**: 2-4 weeks.
- **Risk level**: LOW — Hadamard is a local UV condition; quotient by a discrete
  isometry group preserves local UV structure. The main work is bookkeeping.

### Obstruction G — Mass term, IR modification
- **What is needed**: For massless field, either (a) add mass m > 0 and state results
  for massive SLE on Bianchi VI_0, or (b) propose IR-safe variant of SLE.
- **Status**: The IR obstruction is genuine. Option (a) is straightforward given the
  rest of the construction. Option (b) requires new ideas (not in scope of BN23).
- **Recommendation**: Proceed with (a). State clearly that massless case is IR-obstructed.

---

## WHAT DOES NOT GENERALIZE FROM BN23

1. **Plane wave Fourier analysis**: Bianchi I uses phi(x) = int chi_k(t) e^{ik.x} d^3k.
   For Sol, eigenfunctions are NOT plane waves but involve Bessel-K functions in the
   s-fiber. This requires complete rewriting of mode decomposition.

2. **Simple dispersion relation**: BN23 uses omega_k^2(t) = |k|^2/a(t)^2 (single scale
   factor for Bianchi I). For Sol, omega_{n,lambda}^2(t) is the n-th Mathieu eigenvalue
   of a 1D Schrodinger operator with time-dependent potential. This is much harder to
   handle analytically.

3. **Direct Bogoliubov transformation**: BN23's Bogolubov transformation is between
   plane-wave modes. For Sol, the transformation must be done per Mathieu eigenmode,
   requiring eigenfunction expansion theory for time-dependent operators.

---

## WHAT DOES GENERALIZE FROM BN23

1. **SLE minimisation principle**: The variational structure is identical — minimise
   smeared energy over Bogolubov transformations. The Sol structure enters only through
   omega^2 and the Plancherel measure.

2. **Adiabatic WKB strategy**: The adiabatic order argument works at the level of the
   temporal equation (7), which has the same form as BN23 Eq.(2.3) after substituting
   the Sol-sector frequency.

3. **Radzikowski criterion application**: The wavefront set argument is standard once
   the mode functions are shown to have correct adiabatic order.

4. **Conformal time rescaling**: The chi_bar = V^{1/2} chi rescaling works identically.

---

## HONEST BOTTOM LINE

This is doable but requires genuine mathematical work beyond a straightforward
generalization. The claim "hardest Type A" in ECI v6.0.24-26 is accurate:
- Bianchi I (BN23): easy Fourier analysis
- Bianchi II (Heisenberg): harder Plancherel, but Kirillov orbit theory for nilpotent
  groups is well understood
- Bianchi VI_0 (this work): solvable non-nilpotent Plancherel, Bessel fibers,
  Mathieu eigenvalue time-dependence, and compactification by Anosov lattice

Estimated total work: 4-6 months for an expert, 9-12 months more realistically.
The massless case is genuinely obstructed at IR (hard negative there).
The massive case is open but achievable.

---

## HALLUCINATIONS / ERRORS CAUGHT IN THIS ANALYSIS

1. **xi = 1/8**: Task prompt stated conformal coupling xi = 1/8. WRONG for 3+1D.
   Correct value is xi = 1/6. Caught by sympy arithmetic.

2. **BN23 covers Bianchi I only**: Task prompt implied BN23 covers multiple Bianchi
   types. Verified: BN23 (arXiv:2305.11388) covers Bianchi I ONLY. Avetisyan-Verch
   (arXiv:1212.6180) covers I-VII for harmonic analysis (not SLE/Hadamard states).

3. **"Kirillov 2004" year check**: Verified as correct — AMS GSM vol.64 (2004).

4. **Auslander-Kostant Inventiones vol/pages**: Verified as Inventiones 14 (1971),
   pp.255-354. The citation is correct.

5. **"Complementary series for Sol"**: Task prompt asked if Sol has complementary
   series "à la SL(2,R)". Answer: NO — Sol is Type I exponential solvable, no
   complementary or discrete series. This is a non-obstruction.

6. **Plancherel measure for Sol**: Stated as d_mu(lambda) ~ |lambda| d_lambda.
   This comes from the symplectic volume on the generic coadjoint orbit (hyperbola
   ab=lambda in R^2). This needs further verification against Avetisyan-Verch Table 1.
