# R5 Spectral Correspondence: Residual Gaps and 6-Month Work Plan

**ECI v6.0.25 | D3_R5_spectral | 2026-05-03**

---

## Preamble: Correction to v6.0.23 "Algebraic Identity"

The v6.0.23 ECI changelog claimed a pointwise algebraic identity
`D_HY = -D_CCM + i*Delta*id` under substitution `u = e^x`.

**This identity is incorrect** (sympy_check.py, 2026-05-03, all blocks PASS):

- Under `u = e^x`, D_CCM pulls back to `-i d/dx` (momentum operator).
- D_HY = `i*(x d/dx + Delta)` is the dilatation operator.
- Their difference is `i*(x-1)*d/dx`, which vanishes only at `x = 1`.

**What does hold** (verified):

- Both operators have the same continuous spectrum `sigma = R`.
- Both are unitarily equivalent to multiplication by `t` on `L^2(R, dt)` via
  Mellin/Plancherel (verified by eigenvalue computation).
- D_HY = D_sa - epsilon, where D_sa = `i*(x d/dx + 1/2)` is self-adjoint.
- The correspondence is at the level of **spectral type equivalence**
  (isomorphic von Neumann algebras), not pointwise operator equality.

This correction strengthens rather than weakens R5: the paper now honestly
claims a spectral type correspondence supported by verified computation,
rather than an algebraic identity that does not hold.

---

## Three Explicit Residual Gaps

### G1: Hypothesis H1 — Bianchi IX Hadamard State Existence

**What is needed:** Existence of a Hadamard quasifree state on the Bianchi IX
spacetime on Lebesgue-almost-every trajectory of the Wainwright-Hsu billiard.

**Current state of knowledge:**
- Banerjee-Niedermaier 2023 (arXiv:2305.XXXXX) proves an analogous result
  for Bianchi I (flat minisuperspace, no BKL chaos).
- The ECI repo has `paper/bvii0_sle_bieberbach` treating Bianchi VII_0, which
  has intermediate complexity.
- Bianchi IX is harder on two counts:
  1. **S³ topology** introduces non-trivial global geometry into the two-point
     Hadamard parametrix construction.
  2. **Mixmaster chaos** (Misner 1969) means the BKL billiard is genuinely
     ergodic on `PSL(2,Z)\H`; the Hadamard condition must be verified not just
     for a single trajectory but for a full-measure set.
- No published proof exists for Bianchi IX Hadamard states.

**Estimated effort:** 2-4 months of dedicated research (A4-style sequel paper,
analogous to the VII_0 work but requiring new techniques for Mixmaster chaos).

**Blocking nature for R5:** H1 is essential. Without it, the BFV folium is
not even defined on Bianchi IX in a controlled sense, and the entire left-hand
side of the correspondence is undefined.

**What R5 can do now:** State H1 explicitly as an open hypothesis, cite
Banerjee-Niedermaier 2023 and the Bianchi VII_0 partial result as evidence,
and characterise precisely what additional input is required (principally:
a Sobolev-regularity estimate for the Hadamard parametrix uniform over BKL
billiard orbits).

---

### G2: Hypothesis H2 — CCM-BFV-Eisenstein Conformal Pullback

**What is needed:** An explicit identification between:
- the CCM cutoff `p <= lambda^2` (Euler product restricted to primes below lambda²),
- the Eisenstein conductor restriction on `PSL(2,Z)\H` (selecting cusp forms
  whose L-functions have conductor <= some bound), and
- the BFV folium coarse-graining scale (the infrared UV split in the Tomita-
  Takesaki modular flow of the type II_infty algebra).

**Current state of knowledge:**
- The CCM cutoff is purely number-theoretic: it restricts the Euler product
  to `prod_{p <= lambda^2} (1 - p^{-s})^{-1}`.
- The Eisenstein conductor cutoff is an automorphic concept with known
  Maass-Selberg theory.
- The BFV folium coarse-graining is a quantum-gravity concept (Brunetti-
  Fredenhagen-Verch, 2003), operating at the level of spacetime algebras.
- **No published framework** connects these three different cutoff notions.
- The v6.0.24 Mellin pullback (`1/(s_1 s_2)` on cusp -> `Gamma(1/2-it)/Gamma(3/2-it)`)
  is suggestive but does not constitute an identification: it shows only that
  the Gamma-function structures match, not that the cutoffs are identified.

**Why this is the deepest gap:**
The three cutoffs live in fundamentally different mathematical settings
(number theory, automorphic forms, operator algebras). Bridging them requires
either:
(a) a new theorem of the type "the BFV renormalisation group flow on Bianchi IX
    algebras is controlled by the prime-counting function pi(lambda^2)", or
(b) a purely formal analogy elevated to a definition (which would reduce H2
    to a tautology and weaken the correspondence claim).

**Blocking nature for R5:** H2 is needed to identify *which* part of the CCM
spectral triple corresponds to *which* part of the BFV folium. Without H2,
the correspondence exists only at the level of "both operators have spectrum R",
which is too weak to publish as a substantive result.

**What R5 can do now:** Articulate H2 as a precise conjecture, show that it
is consistent with all available structural evidence (Mellin Gamma match,
common spectral type), and identify the minimal mathematical object that would
constitute a proof (a natural isomorphism between two renormalisation-group
functors, one number-theoretic and one operator-algebraic).

---

### G3: Maass-Selberg Sector Non-Mixing and Scope of Correspondence

**What is needed:** Clarification of whether the R5 correspondence requires
Eisenstein-sector mixing (which is blocked) or only algebra-level isomorphism
(which is not blocked).

**The obstruction:** The Maass-Selberg c-function for `SL(2,Z)` is scalar
(a single meromorphic function of `s`). Eisenstein series do not mix between
different sectors under the `PSL(2,Z)` action. The scattering matrix is
diagonal: `phi(s) = xi(2s-1)/xi(2s)`.

**Why the stronger framing was refuted (Sonnet adversarial review, v6.0.25):**
The "Eisenstein Sector Duality" framing claimed that BKL chaos *kills* cusp
matrix coefficients, leaving only the Eisenstein sector. This is wrong: by the
Selberg trace formula, BKL chaos (expressed via the prime-geodesic theorem on
`PSL(2,Z)\H`) *enhances* cusp matrix coefficients at scales set by the length
spectrum of closed geodesics. The Eisenstein sector is not singled out by BKL
dynamics.

**What is salvageable:** The WEAKER claim: the operator algebras generated
by D_HY and D_CCM are isomorphic as abstract von Neumann algebras (both are
type I, with continuous spectrum R). This does NOT require sector mixing.
The Eisenstein series appear naturally because the CCM construction uses
`L^2(PSL(2,Z)\H)` as its ambient space, and the Eisenstein sector is the
continuous spectrum portion of that space. BKL chaos does not need to kill
anything; it needs only to produce a modular flow that is spectrally of the
same type.

**Where zeta zeros appear (correct framing):** The Riemann zeros
`gamma_n` appear as scattering resonances at `s = 1/2 + i*gamma_n/2` in
the Maass-Selberg scattering matrix, not as eigenvalues. This is off by a
factor of 2 from the eigenvalue claim (`s = 1/2 + i*gamma_n`) that would
be needed for an RH-type proof. The R5 paper must state this clearly and
NOT claim any RH implications.

**What R5 can do now:** Frame the Eisenstein sector connection as follows:
"The CCM operator D^(lambda,N) acts on `L^2([lambda^{-1}, lambda], du/u)`,
whose spectral theory via Mellin transform is equivalent to L-function
analysis on the critical strip. The BFV modular flow generator on Bianchi IX
is spectrally equivalent to D_HY, which in turn is spectrally equivalent
(same operator type, same von Neumann algebra) to D_CCM. This places both
operators in the same spectral universality class without claiming spectral
equality or mixing of automorphic sectors."

---

## 6-Month Work Plan

### Month 1: Operator Algebra Foundations (Gap G3 partial)

**Tasks:**
- Write rigorous proof that D_HY and D_CCM generate isomorphic type-I von
  Neumann algebras (this is essentially immediate from spectral theory but
  needs clean write-up).
- Compute the Mellin intertwiner U: L^2(R+, dx) -> L^2(R, dt) explicitly and
  verify it conjugates D_HY to multiplication by t.
- Write Section 4 (algebraic identity, corrected) and Section 5 (Eisenstein
  sector via Maass-Selberg) of the R5 paper.

**Output:** Sections 4-5 drafted, with all claims at proposition level
(not theorem) since H1 and H2 are not yet established.

### Month 2: Maass-Selberg and Scattering Resonances (Gap G3)

**Tasks:**
- Pin down the precise statement about zeta zeros as scattering resonances
  at `s = 1/2 + i*gamma_n/2` in the `SL(2,Z)` Maass-Selberg formalism.
- Verify the c-function formula `phi(s) = xi(2s-1)/xi(2s)` and show that
  the poles are at `s = (1 + i*gamma_n)/2`, consistent with resonances at
  `Re(s) = 1/2`.
- Confirm explicitly that no sector-mixing is needed for the algebra-level
  correspondence (this blocks the "strong duality" refutation cleanly).

**Output:** Section 5 completed; G3 resolved (correspondence does not require
sector mixing, and zeta zeros appear only as resonances at s=1/2+i*gamma_n/2).

### Months 3-4: H1 Preliminary (Gap G1)

**Tasks:**
- Identify the precise additional input needed to extend Banerjee-Niedermaier
  2023 (Bianchi I) to Bianchi IX.
- The key technical ingredient: Sobolev regularity of the Hadamard parametrix
  uniform over BKL billiard orbits in `PSL(2,Z)\H`.
- Survey existing Hadamard state results for cosmological spacetimes with
  chaotic dynamics (Minguzzi 2019, Sanders 2013 are starting points).
- Write a detailed "Hypothesis H1 analysis" section to be circulated for
  external comment.

**Output:** Not a proof of H1, but a precise formulation of what is needed
and a research roadmap. This section becomes Appendix A of the R5 paper.

### Month 5: H2 Conjecture Formulation (Gap G2)

**Tasks:**
- Formulate H2 as a precise conjecture: identify the mathematical objects
  that would need to be shown isomorphic (renormalization-group functor in
  BFV sense vs. Euler product restriction functor in CCM sense).
- Check whether the Connes-Consani 2014 spectral realization of primes
  (via adele rings) provides a bridge to the BFV algebra.
- Examine whether the "conductor cutoff" in automorphic forms literature
  (Iwaniec-Kowalski "Analytic Number Theory" Ch.5) can be mapped to the
  BFV coarse-graining scale.

**Output:** H2 stated as a precise conjecture with supporting evidence and
clear statement of what would constitute a proof.

### Month 6: Paper Assembly and Submission

**Tasks:**
- Assemble all sections into final R5 paper draft.
- Circulate to 2-3 external readers (one from quantum gravity, one from
  operator algebras/NCG, one from analytic number theory).
- Submit to Comm. Math. Phys. (preferred over JHEP given operator algebra
  content) or JHEP Letters.

**Output:** Submitted preprint, arXiv:2026.XXXXX

---

## Status Summary Table

| Gap | Hypothesis | Severity | Current Status | 6-mo Target |
|-----|-----------|----------|----------------|-------------|
| G1 | H1: Bianchi IX Hadamard | Blocking | Open research program | Precise formulation + roadmap |
| G2 | H2: CCM-BFV pullback | Most severe | No framework exists | Precise conjecture + evidence |
| G3 | Sector mixing | Resolved | Refuted (Sonnet review, v6.0.25) | Not needed for algebra-level correspondence |
| -- | Algebraic identity | Corrected | v6.0.23 claim incorrect | Replaced by spectral type equivalence |
| -- | Zeta zeros framing | Corrected | Resonances at s=1/2+i*gamma_n/2, not eigenvalues | Stated correctly in paper |

---

## Key References for Gap Work

- Banerjee-Niedermaier 2023: Hadamard states on Bianchi I (baseline for G1)
- Hartnoll-Yang 2025 (arXiv:2502.02661): BKL-Bianchi IX D_HY operator
- Connes-Consani-Moscovici 2025 (arXiv:2511.22755): CCM spectral triple
- Selberg 1956: Trace formula (establishes that BKL chaos enhances, not kills, cusp coefficients)
- Iwaniec-Sarnak 2000: Perspectives on the Riemann Hypothesis (context for cautious framing)
- Brunetti-Fredenhagen-Verch 2003: BFV generally-covariant quantum field theory framework
- Misner 1969: Mixmaster universe (Bianchi IX chaos)
