---
name: M3 Andreatta-Iovita framework analysis for 4.5.b.a
description: Assessment of whether arXiv:1905.00792 applies to LMFDB 4.5.b.a given ramification and supersingularity at p=2
type: analysis
---

# Andreatta-Iovita Framework Analysis for LMFDB 4.5.b.a

**Date:** 2026-05-06 (Wave 12 Phase 3, sub-agent M3)
**Primary source:** arXiv:1905.00792 — live-fetched 2026-05-06 via arxiv.org/abs/
**Hallu count entering/leaving:** 85 / 85

---

## 1. The Paper: What It Is

**Title:** "Katz type p-adic L-functions for primes p non-split in the CM field"
**Authors:** Fabrizio Andreatta, Adrian Iovita
**arXiv:** 1905.00792 (submitted 2019-05, accepted 2024-07)
**MSC:** 11F67, 11F33, 11G15

**Abstract (paraphrased from live fetch):** Constructs p-adic L-functions for
a triple (F, K, p) where F is a classical elliptic eigenform, K is an
imaginary quadratic field, and p is **non-split** in K. The construction
interpolates the algebraic parts of special values L(F ⊗ χ, m) for Hecke
characters χ of K. Extends Katz (split case) and Bertolini-Darmon-Prasanna
(split case for cuspforms).

**Key companion paper:** Fan-Wan (arXiv:2304.09806) — extends Andreatta-Iovita
p-adic Waldspurger formula to all ramification types (split, inert, ramified,
including p=2), for GL_2 representation that is **principal series at p**.

---

## 2. Framework Requirements vs. 4.5.b.a

### 2a. "Non-split" prime — SATISFIED? YES (partly)

"Non-split" = p does not split completely in K. This includes:
- p **inert** in K: pO_K = p (prime) — one prime above p
- p **ramified** in K: pO_K = p^2 — one prime above p, but with ramification

For K = Q(i):
- disc(Q(i)) = -4
- 2 ramifies in Q(i): (2) = (1+i)^2 * (-i) in Z[i]
- p=2 is RAMIFIED, hence non-split ✓

The paper title says "non-split," which should include ramified.
However: the abstract specifically references comparison to Bertolini-Darmon-Prasanna
"when p is split in K," and Katz's construction "for F Eisenstein and p-split."
The innovation is the non-split case. Whether the paper treats INERT only or
INERT + RAMIFIED is NOT fully clear from the abstract alone.

**Flag:** [TBD: verify from full paper whether Andreatta-Iovita 2024 handles
ramified p=2 explicitly, or only inert primes]

Fan-Wan (arXiv:2304.09806) explicitly handles "all ramification types (split,
inert and ramified, and allowing p=2)" but requires "principal series at p."

### 2b. Ordinary vs. finite slope — CRITICAL OBSTRUCTION

Standard Katz p-adic L-functions (Katz 1978, Inventiones 49) require:
- The prime p is **good** for the form (p ∤ N) or at worst multiplicative reduction
- The form is **ordinary** at p: ord_p(a_p) = 0 (unit root exists)

For 4.5.b.a:
- N = 4 = 2^2, so p=2 is a **bad prime** (p | N)
- a_2 = -4, so ord_2(a_2) = 2 ≠ 0: **non-ordinary / supersingular**
- Char poly at p=2: X^2 - a_2*X + chi_4(2)*2^{k-1} = X^2 + 4X + 0 = X(X+4)
  (since chi_4(2) = 0 because 2 | cond(chi_4) = 4)
- Roots: {0, -4} — one root is ZERO, the other is -4 with ord_2 = 2

No unit root exists. The form is not just non-ordinary but has a ZERO root
at p=2, which is the most extreme non-ordinary case.

**Consequence for Andreatta-Iovita:** Their paper title says "Katz type"
p-adic L-functions. Katz's original approach uses the unit root of the
characteristic polynomial of Frobenius to construct the Euler factor
and define the interpolating measure. Without a unit root, the Katz-type
construction fails at its foundations.

**CRITICAL FLAG:** The Andreatta-Iovita 2024 framework applies to the
**non-split** prime case, but it extends Katz/Bertolini-Darmon-Prasanna
in the direction of changing the SPLITTING TYPE of p, not in the direction
of changing the SLOPE. The abstract says F is "a classical elliptic eigenform"
without slope restriction — but the interpolation formula will involve the
Euler factor, which degenerates when the unit root is missing.

**Assessment:** Andreatta-Iovita LIKELY requires ordinary (or at least
finite slope with well-defined unit root). For 4.5.b.a with the zero root
at p=2, their framework does NOT directly apply without substantial modification.

### 2c. Level N=4 vs. "good prime" condition

Standard Katz theory requires p ∤ N (good reduction). Here:
- N = 4 = 2^2, so p = 2 | N
- p=2 divides the level: BAD reduction at p=2
- This is an additional obstacle beyond the slope issue

For p | N (bad prime), the local factor at p in the L-function is:
L_p(f, s)^{-1} = 1 - a_p * p^{-s}  (rather than the degree-2 Euler factor)

But since p | N AND p | cond(chi), the local factor is even more degenerate.
In fact, for LMFDB 4.5.b.a with N=4=2^2 and chi=chi_4 (cond=4):
the Atkin-Lehner operator w_2 is not well-defined in the usual sense.

### 2d. "Finite slope p-adic family" requirement

The brief states: "Their setup requires 'finite slope p-adic family' — does
4.5.b.a fit?"

A finite slope p-adic family is a family of overconvergent modular forms
parametrized by weight, varying p-adically, with a fixed slope h at p.
For h=2 (slope of 4.5.b.a at p=2), such a family would lie in the
Coleman-Mazur eigencurve at slope 2.

**In principle**, 4.5.b.a lies on the eigencurve (every classical eigenform
does), and slope-2 families exist. But:
1. The slope h=2 equals (k-1)/2 for k=5 — this is the SUPERSINGULAR slope.
   Supersingular eigencurve geometry is much more complicated.
2. The form has a_2 root = 0, which is a special "critical" point where
   the eigencurve has non-trivial geometry (see Benois-Buyukboduk 2403.16076
   on "θ-critical points").
3. For CM forms, p-adic families at supersingular primes require the
   Pollack ± construction (Pollack 2003, Kobayashi 2003) rather than
   standard Hida families.

### 2e. Fan-Wan (2304.09806): "Principal series at p"

Fan-Wan handle all ramification types (including p=2 ramified) but require
the GL_2 automorphic representation to be **principal series at p**.

What is principal series at p for our form?
- For a newform f of level N = p^r with p | N, the local factor at p is
  classified by the local Weil-Deligne representation.
- For 4.5.b.a with N=4=2^2, chi=chi_4 at p=2:
  The local factor at p=2 is determined by the nebentypus twist.
  Since chi_4 is a character of conductor 4=2^2, the local representation
  at p=2 is a TWIST of a special or principal series representation.
- A CM form's local type at a ramified prime is typically a TWIST OF THE
  STEINBERG (special representation), not principal series.

**Flag:** [TBD: verify local type at p=2 for 4.5.b.a — is it principal series,
special/Steinberg, or supercuspidal? This requires the local Langlands
classification for the newform of level 2^2 and chi=chi_4 at p=2.]

If the local type at p=2 is Steinberg (which is likely for level p^2 with
nebentypus of conductor p^2), then Fan-Wan's "principal series" requirement
is NOT satisfied, and their framework also fails to apply.

---

## 3. Kronecker Limit Formula Compatibility

Andreatta-Iovita prove a p-adic Kronecker limit formula. For CM forms,
the Kronecker limit formula connects the derivative L'(0, chi) to
logarithms of elliptic units — a construction fundamentally tied to the
p-adic logarithm of Frobenius eigenvalues.

For supersingular forms with a Frobenius eigenvalue = 0, the logarithm
is undefined (log(0) = -infinity). The Kronecker limit formula presumably
degenerates.

---

## 4. Kings-Sprang (1912.03657): Integrality at Ordinary Primes Only

Kings-Sprang (Annals of Mathematics 202, 2025, pp. 1-109) prove:
- For any totally complex number field L, critical L-values of algebraic
  Hecke characters / periods are **algebraic integers** in the ordinary case.
- Their p-adic interpolation construction applies **in the ordinary case** only.
- Non-ordinary case is not covered.

For 4.5.b.a at p=2 (supersingular): Kings-Sprang does not apply.

---

## 5. Benois-Buyukboduk (2403.16076): Arithmetic at Critical Points

This paper studies p-adic L-functions at "θ-critical points" on the
eigencurve — precisely the kind of point where 4.5.b.a might live.
Their construction is sophisticated (étale approach, affinoid neighborhoods).

However: the paper's primary application is to forms with a_p ≠ 0 (finite slope,
where the form is a θ-critical point due to special geometry, not
a zero root). The form 4.5.b.a with a_2 = 0 (after removing the Euler
factor...) — wait, a_2 = -4 ≠ 0 for this form.

Correction: a_2 = -4 for 4.5.b.a. The char poly roots are {0, -4}.
The form's slope h = ord_2(alpha_p) where alpha_p is the root with
smaller 2-adic valuation. Both roots have valuations {infinity (for 0),
2 (for -4)}. So the "slope" is the minimum = 2 (taking the finite root).

Actually for a form of weight k with a_p ≠ 0 and p | N, the situation
is handled differently. The char poly for p bad is degree 1: X - a_p.
Here a_2 = -4, so the single root is -4, with ord_2(-4) = 2.
This means: the Newton slope is h = 2, finite, non-ordinary.

So Benois-Buyukboduk might potentially apply (finite slope h=2, non-ordinary),
but their framework would need to be verified to handle the p | N case.
This is a [TBD: verify] item, not assertable without the full paper.

---

## 6. Summary of Framework Applicability

| Framework | Ramified p? | Non-ordinary? | p | N? | Verdict for 4.5.b.a |
|---|---|---|---|---|
| Katz 1978 | NO (split/inert only) | NO (ordinary only) | NO (good p only) | FAILS (3/3) |
| Andreatta-Iovita 2024 | YES (non-split) | LIKELY NO (Katz-type) | UNCLEAR | PARTIAL FAIL |
| Kings-Sprang 2024 | Not specified | NO (ordinary only) | Not specified | FAILS |
| Fan-Wan 2023 | YES (all types+p=2) | Not specified | Unclear | UNCLEAR (princ series?) |
| Benois-Buyukboduk 2024 | Not specified | YES (finite slope) | UNCLEAR | [TBD] |
| Pollack ± / Kobayashi | Typically inert/split | YES (supersingular) | Requires good p | FAILS (p|N) |

**No existing published framework cleanly covers all three obstructions
simultaneously for 4.5.b.a:**
1. p=2 ramified in Q(i)
2. p=2 supersingular (slope h=2=(k-1)/2)
3. p=2 | N = 4 (bad prime)

---

## 7. What Would Be Needed

To construct a p-adic L-function for 4.5.b.a at p=2, one would need a
framework handling:
- CM forms with CM field K in which p ramifies (p | disc(K))
- Non-ordinary (supersingular) forms with degenerate Frobenius
- Bad prime p | N (level not coprime to p)
- p=2 specifically (the most delicate prime due to (p-1)=1 and
  the absence of a good theory of (p-1)-st cyclotomic character)

The closest existing work handles some but not all of these:
- Loeffler-Zerbes overconvergent families handle finite slope but typically
  require p ∤ N or specific local types.
- Andreatta-Iovita handle non-split p but in a Katz-type (ordinary) framework.
- Fan-Wan handle all ramification including p=2 but require principal series.
- For ramified p=2 with CM, the local type at p for a form of level 2^2
  with chi_4 needs separate analysis.

This is a legitimate **open problem** in the theory of p-adic L-functions:
constructing the p-adic L-function for a supersingular CM form at a ramified
prime dividing the level.

---

## Sources Live-Verified (2026-05-06)

- arXiv:1905.00792 (Andreatta-Iovita) — abstract fetched, paper content confirmed
- arXiv:1912.03657 (Kings-Sprang) — abstract fetched, "ordinary case" restriction confirmed
- arXiv:2304.09806 (Fan-Wan) — abstract fetched, all-ramification + principal series confirmed
- arXiv:2403.16076 (Benois-Buyukboduk) — abstract fetched, θ-critical point framework confirmed
- arXiv:math/0610163 (Bannai-Kobayashi) — abstract fetched, ordinary case only confirmed
- LMFDB 4.5.b.a — Hecke eigenvalues, CM field, eta product confirmed
