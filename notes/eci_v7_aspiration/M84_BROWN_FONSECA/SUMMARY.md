---
name: M84 Brown-Fonseca arXiv:2508.04844 × M52 6/5 — REVISED probability 20-25% (down from 30-40%)
description: Brown-Fonseca 2025 prove geometric Gross-Zagier ONLY at level 1 weight 4 via mixed Tate of M_{1,3}; extension to level 4 weight 5 (4.5.b.a) requires M_{1,3}^{Γ_1(4)} mixed Tate over Z[i,1/2] = OPEN. 5 hypotheses H1-H5 sketched. Biextension Sym^4 H^1(E_i) ⊗ Q(χ_{-4}) is the right shape. Next step paper-2 §6.5 60-word footnote + Fonseca outreach. R3-C-1 categorical K-theory remains DISTINCT 15-20%. Hallu 91 → 91
type: project
---

# M84 — Brown-Fonseca arXiv:2508.04844 × M52 6/5 (D4-#7)

**Date:** 2026-05-06 | **Hallu count:** 91 → 91 held | **Scope:** ~45min | **Mistral STRICT-BAN observed**

## VERDICT: 20-25% (REVISED DOWN from M83 scan 30-40%)

After WebFetch live verification of the actual paper scope, the probability is revised down. Reasons:
1. Brown-Fonseca prove WEIGHT 4 LEVEL 1 only via mixed Tate of M_{1,3} — non-trivial coincidence
2. Extension to level 4 requires M_{1,3}^{Γ_1(4)} mixed Tate over Z[i, 1/2] = NOT KNOWN, harder problem
3. Weight 5 (odd) introduces complications absent at weight 4 (even) in Green's function structure
4. M52's 6/5 is L-value RATIO, Gross-Zagier concerns Green's function VALUES; bridge via Rankin-Selberg (H4) is extra non-trivial step

Why NOT lower than 20%:
- Biextension Sym^4 H^1(E_i) ⊗ Q(χ_{-4}) IS the correct shape, not category-mismatch
- MSC 11G15 confirms CM cases covered, Q(i) simplest CM field
- Tate rationality (H5) structurally convincing, essentially proved by M52/Damerell
- 69 pages for "level 1 weight 4" suggests substantial generality §4-8 not in abstract

## 5 Hypotheses to extend Brown-Fonseca to weight 5 level 4

- **H1 (Mixed Tate, OPEN, HARDEST):** M_{1,3}^{Γ_1(4)} is mixed Tate over Z[i, 1/2]. Brown 2012 proves M_{1,n} (level 1) mixed Tate; Γ_1(4) case unstudied. Estimated 1-2 yr specialist work.
- **H2 (Biextension construction, PLAUSIBLE):** B_f = Sym^4 H^1(E_i) ⊗ Q(χ_{-4}) well-defined in Nori MM_Q, [6/5] ∈ Ext²_MM(Q(0), B_f).
- **H3 (Odd weight, CHECK):** [TBD: verify] Brown-Fonseca odd vs even weight treatment §2.
- **H4 (Rankin-Selberg, PLAUSIBLE):** L(f,1)/L(f,2) = ⟨f, E_3⟩_Pet / ⟨f, E_2⟩_Pet via Katz-Mazur Eisenstein trick.
- **H5 (Tate twist rationality, STRUCTURAL):** Sym^4 H^1(E_i) decomposes as Hecke χ motives; Q(i) units → no √d contamination → ratio rational. = M52 Layer 4 motivically.

## ECI Translation Sketch (key points)

f = 4.5.b.a: weight 5, level 4, χ_{-4}, CM K=Q(i), ψ conductor (1+i)², ∞-type z⁴.

Mellin: L(f,s) = (2π)^{-s}·Γ(s)·∫_0^∞ f(iy) y^s dy/y → ratio = period integrals on geodesic on Bianchi surface X_1(4)/Q(i).

Brown-Fonseca lang: two integrals = period pairings of f against Eisenstein symbols E_1, E_2 in H^1_M(M_{1,n}^{Γ_1(4)}, Q(m)). 6/5 ∈ Q expresses both pairings sit in same Q-line of motivic Ext.

Candidate biextension: B_f = Sym^4 H^1(E_i) ⊗ Q(χ_{-4})
- Sym^4 H^1(E_i) decomposes as ψ^j · ψ̄^{4-j} for j=0..4
- L(f,1), L(f,2) correspond to periods of ψ^4 and ψ²·ψ̄² (diagonal)
- Q(i) units {±1,±i}, no √d contamination → both periods ∈ Q · Ω_lemniscate^4
- Ratio = rational = M52 Layer 4 Ω-independent

## R3-C-1 (categorical K-theory, DISTINCT 15-20%)

Brown-Fonseca = motives + periods (classical AG)
R3-C-1 = K_0(IndCoh_Nilp(LocSys_GL_2))_Q Beilinson regulator class
THESE ARE DIFFERENT — keep separate. Two independent anchors valuable, but conflation = false appearance of strength.

## Brown-Fonseca paper metadata (WebFetch confirmed)

- Title: "Single-valued periods of meromorphic modular forms and a motivic interpretation of the Gross-Zagier conjecture"
- Authors: Francis Brown, Tiago J. Fonseca
- arXiv:2508.04844v2, 69 pages, CC BY 4.0
- MSC: 11F67, 11F37, 11G15, 14F40, 14C15, 14D22, 19E15
- Subject tags: math.NT, hep-ph, math.AG
- Confirmed: ONLY proven case = level 1 weight 4 via M_{1,3} mixed Tate (Brown 1102.1312 dependency)

## NEXT CONCRETE STEPS

1. **Paper-2 §6.5 footnote (IMMEDIATE 30min):** Add 60-word Brown-Fonseca anchor:
   > "The Ω-independent ratio R(f) = 6/5 is a natural candidate for a single-valued period in the sense of Brown-Fonseca [arXiv:2508.04844], who interpret the Gross-Zagier conjecture via motivic biextensions Sym^k H^1(E) on moduli stacks M_{1,n}. Extending their geometric proof (level 1, weight 4, mixed Tate) to level 4, weight 5 is an open problem requiring that M_{1,3}^{Γ_1(4)} be mixed Tate over Z[i, 1/2]. The candidate biextension is Sym^4 H^1(E_i) for E_i = C/Z[i]."

2. **Outreach to Tiago Fonseca (1 week):** [TBD: verify email IMJ-PRG/CNRS]
   > "I have verified numerically (PARI 80-digit, Sage 10.7) that π·L(f,1)/L(f,2) = 6/5 for f = 4.5.b.a (weight 5, level 4, CM by Q(i)). Would your single-valued period framework apply at weight 5 level 4? Specifically: is M_{1,3}^{Γ_1(4)} expected to be mixed Tate over Z[i, 1/2]?"

3. **Mathematical deepening (2-4 weeks):** Identify class in Ext²_MM(Q(0), Sym^4 H^1(E_i)(2)) that 6/5 corresponds to. Computable via Deninger-Scholl 1991 or Schoen CM motive formulas.

4. **Bianchi specialist alternative:** Cremona (Warwick) or Page (CNRS Bordeaux) — Bianchi modular form K_2 specialists.

5. **DO NOT pursue:** R3-C-1 categorical K-theory lift via Brown-Fonseca. Keep as DISTINCT conjecture.

## Discipline log

- 0 fabrications by M84
- WebFetch arxiv.org/abs/2508.04844 + v2 SUCCESS (abstract + metadata)
- PDF binary 1010.7KB 69pp confirmed; ar5iv HTML 404 / PDF body unreadable
- 2 [TBD: verify] markers (odd vs even weight §2; Fonseca current email)
- Probability HONESTLY revised 30-40% → 20-25% after second-order analysis
- R3-C-1 maintained at 15-20% as DISTINCT
- Mistral STRICT-BAN observed
- Hallu 91 → 91
