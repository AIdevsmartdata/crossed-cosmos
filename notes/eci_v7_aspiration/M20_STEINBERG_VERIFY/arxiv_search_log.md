---
name: M20 ArXiv search log — Steinberg-edge identity verification
date: 2026-05-06
agent: M20 (Sonnet 4.6, validation)
---

# ArXiv Search Log — M20 Steinberg-Edge Verification

## Search queries executed

### Query 1: "Steinberg edge eigenvalue modular form"
Search engine: WebSearch
Result: No papers with the literal phrase "Steinberg edge" applied to CM newform eigenvalues.
The term "Steinberg" in modular forms refers to the STEINBERG REPRESENTATION (special representation
= Steinberg twist by unramified character), NOT to a named "Steinberg-edge" phenomenon.
The phrase "Steinberg-edge" used by M13 appears to be M13's own coinage, NOT an established
mathematical term in the literature.

### Query 2: "critical slope CM newform Hecke eigenvalue ramified principal series weight"
Result: Several relevant papers found.
- arXiv:1905.05687 (2019): Discusses classical points of eigenvariety ramified over weight space
  and local splitting of Galois representation. Abstract level only — confirms "theta-critical" is
  a known concept but does NOT mention "Steinberg-edge" eigenvalue identity.
- Bellaiche papers (critical p-adic L-functions, Brandeis preprints): Discuss critical slope CM
  forms and eigencurve geometry. Confirm that critical-slope CM points are ramified on the
  eigencurve. Do NOT state a_p = p^((k-1)/2) explicitly.
- Key quote found: "A classical point is ramified with respect to the weight map if and only if
  there exists p | p such that the local Galois representation splits and the point has critical
  p-slope." — consistent with 4.5.b.a being theta-critical, but this is about slope not
  about the eigenvalue size.

### Query 3: "Atkin-Lehner Li newforms ramified prime Hecke eigenvalue a_p conductor squared"
Result: Atkin-Li 1978 "Twists of newforms and pseudo-eigenvalues of W-operators"
(Inventiones Mathematicae 48, pp. 221-243) is the canonical reference.
- DOI: 10.1007/BF01390245
- Pseudo-eigenvalue formula: a_q(g) = -delta(q)*q^(k/2-1) for prime q dividing Np.
- This gives |a_q| = q^(k/2-1) = q^((k-2)/2), NOT q^((k-1)/2) — DIFFERENT EXPONENT.
- Critical difference: M13 claims |a_p| = p^((k-1)/2), the Atkin-Li formula gives p^((k-2)/2).
  These are only equal when k=2. For k=5: (k-1)/2 = 2 vs (k-2)/2 = 3/2. M13 is CORRECT,
  Atkin-Li pseudo-eigenvalue applies to DIFFERENT quantity (the Atkin-Lehner pseudo-eigenvalue
  eta, not a_p directly).
- RESOLUTION: The Atkin-Li formula applies to W_p pseudo-eigenvalue eta, NOT to a_p.
  For CM newforms, a_p is determined by the Hecke character value psi(pi), which has size
  N(pi)^((k-1)/2) = p^((k-1)/2) by the Hecke character unitarity condition.

### Query 4: "Newton polygon CM newform Hodge polygon ramified prime"
Result: Several papers on Newton vs Hodge polygons for L-functions of Kloosterman sums.
NOT directly relevant to the 4.5.b.a question (those concern different families of L-functions).
No explicit statement of |a_p| = p^((k-1)/2) for CM newforms.

### Query 5: "theta critical eigencurve CM newform Bellaiche Stevens"
Result: Bellaiche "Critical p-adic L-functions" (Inventiones 2012, DOI: 10.1007/s00222-011-0358-z)
and Bellaiche preprints found. The concept of "theta-critical" CM forms is KNOWN:
- A CM form is theta-critical at p if its slope equals (k-1)/2 (= "critical slope").
- Slope = v_p(a_p) for p | N (the p-adic valuation of the T_p eigenvalue).
- For 4.5.b.a: a_2 = -4, so v_2(a_2) = v_2(4) = 2 = (5-1)/2 = 2. YES, critical slope.
- This theta-critical behavior IS KNOWN in the Bellaiche-Stevens literature.

### Query 6: Atkin-Li 1978 pseudo-eigenvalue formula check
- "ag(q) = -delta(q)*q^(k/2-1)" from one source.
Note: k/2-1 ≠ (k-1)/2 in general. For k=5: k/2-1 = 1.5, (k-1)/2 = 2.
These are DIFFERENT formulas — the pseudo-eigenvalue and a_p are different quantities.

### Query 7: MathOverflow / specialized searches
No direct hit on "Steinberg-edge eigenvalue identity" as a named result.
No paper explicitly states "a_p = pm p^((k-1)/2) for all CM newforms at ramified p."

## Key references live-verified
1. Atkin-Li 1978 (Inventiones 48): CONFIRMED REAL. DOI: 10.1007/BF01390245.
   Pseudo-eigenvalue formula is for W_p operator, not a_p.
2. Bellaiche "Critical p-adic L-functions" (Inventiones 2012): CONFIRMED REAL.
   Discusses theta-critical CM points on eigencurve.
3. arXiv:1905.05687 (2019, local splitting): CONFIRMED REAL abstract.
4. LMFDB data for 4.5.b.a: CONFIRMED (a_2 = -4, CM by Q(i)).
5. LMFDB data for 8.5.d.a: CONFIRMED (a_2 = 4, CM by Q(sqrt(-2))).
6. LMFDB data for 7.5.b.a: CONFIRMED (a_7 = 49 = 7^2, CM by Q(sqrt(-7))).
7. LMFDB data for 20.5.d.a: CONFIRMED (a_2 = -4, a_5 = 25, CM by Q(sqrt(-5))).
8. LMFDB data for 12.5.c.a: CONFIRMED (a_3 = 9 = 3^2, CM by Q(sqrt(-3))).

## Hallu count: 85 (unchanged — no new citations introduced)
