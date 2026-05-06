---
name: M3 Paper-2 viability outline (conditional)
description: Conditional 6-week outline for Katz-type p-adic L-function paper — NEEDS-FURTHER-SCOPING verdict
type: planning
---

# Paper-2 Viability and Conditional Outline

**Date:** 2026-05-06 (Wave 12 Phase 3, sub-agent M3)
**Overall verdict:** NEEDS-FURTHER-SCOPING (see SUMMARY.md for full argument)
**Hallu count:** 85 (unchanged)

---

## Why NOT "VIABLE" (as defined in the brief)

The brief asks for a "VIABLE / DEAD-END / NEEDS-FURTHER-SCOPING" verdict
on a 6-week paper for *Compositio Math* or *Algebra & Number Theory*.

A VIABLE verdict would require a **concrete 2-adic statement** derivable
from existing frameworks applied to 4.5.b.a. The M3 analysis finds:

1. **No existing framework covers the triple obstruction** (ramified + supersingular + bad prime at p=2).
2. **The 2-adic structure of {alpha_m}** is not consistent with a standard Katz interpolation pattern (differences not 2-adically small, char poly has a zero root).
3. **The theoretical gap** is not a minor TBD — it requires new mathematics (constructing p-adic L-functions at supersingular, ramified, bad primes for CM forms).

Therefore: the paper cannot currently be written as a **derivation** from
existing theory. It could instead be written as:
- (A) A **survey/announcement** identifying the open problem, or
- (B) A **research paper** that SOLVES the open problem (i.e., constructs
  the p-adic L-function) — this is more than 6-week work.

---

## However: a narrower paper IS potentially viable

The A76 sketch proposed:
> *"Katz-type p-adic L-functions for the CM newform 4.5.b.a and the algebraic ratio 1/60"*

This could be reframed as:

> **"Obstacles to p-adic interpolation at the supersingular ramified prime p=2 for LMFDB 4.5.b.a, and a conjecture"**

This reframing converts the DEAD-END for the "derive from existing theory" goal
into a VIABLE paper identifying and sharpening the open problem.

---

## Conditional 6-Week Outline (Reframed Paper)

**Title (candidate):** "The CM newform 4.5.b.a and the p-adic L-function problem
at the supersingular ramified prime p=2"

**Target:** *Research in Number Theory* (Springer), *Journal of Number Theory*,
or *International Journal of Number Theory* — more appropriate than Compositio
Math (which would require a solved problem, not a problem-identification paper).

**Length:** ~15 pages

### Week 1: Setup and LMFDB anchor

- §1: The newform 4.5.b.a: level, weight, nebentypus chi_4, CM by Q(i).
  Eta product f = eta(z)^4 eta(2z)^2 eta(4z)^4.
  Hecke eigenvalues from Grossencharacter formula: a(p) = 2 Re((a+bi)^4).

- §2: The Damerell ladder {alpha_m}_{m=1}^4 = {1/10, 1/12, 1/24, 1/60}.
  These are L(f,m)/Omega_K^{2m} for K=Q(i), proven algebraic by Damerell (1971)
  and Shimura (1977). Cite Chowla-Selberg for Omega_K = Gamma(1/4)^2/(2*sqrt(pi)).

  Note: these alpha_m are DEFINED at complex special values, not p-adic.

### Week 2: Classical Katz framework and why it fails

- §3: Katz 1978 (Inventiones 49) framework summary.
  For a CM form F of weight k, CM field K, ordinary at a prime p inert or
  split in K, with p ∤ N: Katz constructs a p-adic measure mu_F on
  Gal(K(p^\infty)/K) interpolating L(F, chi, m) for Hecke characters chi.

- §4: First obstruction — RAMIFICATION. p=2 ramifies in Q(i).
  Katz assumes p split or inert (p ∤ disc(K)). Since disc(Q(i))=-4, p=2|4.
  Reference: Andreatta-Iovita (1905.00792) for the non-split extension —
  they handle inert+ramified but STILL require ordinarity (Katz-type construction).

- §5: Second obstruction — SUPERSINGULARITY. Newton slope h=2=(k-1)/2.
  a_2 = -4, ord_2(a_2) = 2. The characteristic polynomial X(X+4) has a zero root.
  No unit root exists. Standard Katz Euler factor construction fails.
  Reference Pollack (2003) and Kobayashi (2003) ± construction for elliptic curves —
  but this applies to weight 2 (elliptic curves), not weight 5.

- §6: Third obstruction — BAD PRIME. p=2 | N=4.
  The local type at p=2 for 4.5.b.a: since chi_4 has conductor 4=2^2 and p=2,
  the local representation is NOT principal series at p.
  [TBD: Determine local Weil-Deligne representation at p=2 for 4.5.b.a.]

### Week 3: 2-adic structure of the Damerell ratios

- §7: Exact computation of v_2(alpha_m) = {-1, -2, -3, -2} for m={1,2,3,4}.
  Show that the denominator 2-parts are {2, 4, 8, 4}.
  The consecutive ratios are {5/6, 1/2, 2/5} with v_2 = {-1, -1, +1}.

- §8: Verify that these valuations are NOT consistent with a standard 2-adic
  interpolation: within the congruence class m ≡ 1 (mod 2), the difference
  alpha_1 - alpha_3 = 7/120 has v_2 = -3 (not 2-adically small).

- §9: HOWEVER — state that with the CORRECT Euler factor, the "true" p-adic
  special values (the ones that would be interpolated) are NOT the raw alpha_m.
  The correct objects would be:
      Lambda_m = (explicit Euler factor at p=2) * alpha_m
  and the Euler factor could restore 2-adic continuity.
  Problem: the Euler factor is ill-defined here (zero root).

  [TBD: conjecture what the correct Euler-factor-corrected values should be,
  using analogy with Pollack ± or Loeffler-Zerbes overconvergent approach.]

### Week 4: Survey of nearest frameworks

- §10: Fan-Wan (2304.09806) — all ramification types, principal series condition.
  Determine whether 4.5.b.a satisfies "principal series at p=2."
  [TBD: local type computation — this is a key open question for the paper.]

- §11: Benois-Buyukboduk (2403.16076) — θ-critical points on eigencurve.
  Relevance: 4.5.b.a with slope h=2 at p=2 may be a θ-critical point.
  [TBD: verify from their framework.]

- §12: Kings-Sprang (1912.03657) — integrality in ordinary case.
  Conclude: does not apply. BUT note that their integrality theorem for
  the critical values (in the ordinary case) motivates asking whether
  alpha_m for 4.5.b.a are similarly "integral" after appropriate normalization.
  Observation: 120*alpha_m = {12, 10, 5, 2} are ALL integers.
  This is a formal integrality (trivially, since alpha_m are rational with
  denominators dividing 120), not a deep integrality in the Kings-Sprang sense.

### Week 5: The conjecture

- §13: Formulate the main conjecture.

  **Conjecture M3.1:** There exists a 2-adic L-function L_{2,+}(f, s) and
  L_{2,-}(f, s) (Pollack ± type, extended to weight 5 and CM by Q(i))
  such that at special values s = m for m=1,2,3,4:
      L_{2,±}(f, m) = (explicit Euler-type factor) * alpha_m * Omega_K^{2m}
  where the Euler-type factor compensates for the supersingularity and
  the ± accounts for the degenerate char poly root at p=2.

  Evidence: purely formal (structure of the Damerell ratios + analogy with
  Kobayashi/Pollack for elliptic curves).

  Note: This conjecture should be labelled SPECULATIVE in the paper.
  The paper's contribution is to SHARPEN the problem, not to prove this.

- §14: Equivalent reformulation: what congruence property do the alpha_m
  satisfy that is consistent with such an L-function?
  Observation: alpha_2 - alpha_4 = 1/15, v_2 = 0. If a corrected
  alpha_m' = alpha_m * (correction), can we achieve v_2(alpha_2' - alpha_4') >= 1?
  Compute what the correction factor must be for this to hold.

### Week 6: Write-up and references

- §15: Conclusions. The open problem is:
  1. Construct L_{2,±}(f,-) for weight-5 CM forms at ramified supersingular primes.
  2. Connect to the Iwasawa main conjecture for f/K.
  3. Determine whether the "60" in alpha_4 = 1/60 has a p-adic avatar.

- References: Damerell (1971), Katz (1978), Shimura (1977), Chowla-Selberg (1967),
  Andreatta-Iovita (1905.00792), Kings-Sprang (1912.03657), Fan-Wan (2304.09806),
  Benois-Buyukboduk (2403.16076), Pollack (2003), Kobayashi (2003),
  LMFDB (live reference), NPP20 (for ECI context appendix).

---

## Realistic Assessment

**Can this be written in 6 weeks?** YES — at the "problem sharpening" level.
The mathematics required to fill all [TBD] items would take 3-6 months.

**Is it publishable?** Potentially, at a mid-tier journal (*J. Number Theory*,
*Res. Number Theory*), as a problem-identification paper with concrete computation.
NOT suitable for Compositio Math or ANT without solving the open problem.

**Added value beyond A76:** A76 identified the sub-channel in 1 page.
A paper-2 at this level would provide:
- The explicit 2-adic computation (weeks 3-4)
- The survey of why existing frameworks fail (weeks 2-4)
- A precise conjecture (week 5)
This is genuine mathematical content.

**Risk:** If someone else (Andreatta, Iovita, Loeffler, Zerbes, ...) has already
treated this case, the paper would be scooped. Should search for:
"p-adic L-function CM level 4 weight 5" or "supersingular CM weight 5" before
committing.

---

## Files needed if we proceed

1. Local type computation at p=2 for 4.5.b.a (Weil-Deligne rep)
2. Verification of Fan-Wan principal series condition
3. Explicit computation of L(f, m) to high precision (to verify alpha_m)
4. Literature sweep for any existing paper on level 4 weight 5 p-adic L
