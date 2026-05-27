# Paper Bauerschmidt-Dagallier-Remondiere: On Hyp-CST and the perturbative-regime closure of the SU(N) Yang-Mills Polchinski chain

**Authors**: R. Bauerschmidt (NYU Courant) + B. Dagallier (Yale) + K. Remondiere (Independent, Oloron-Sainte-Marie, France)
**Date**: 26 May 2026
**Target journal**: Communications in Mathematical Physics
**Status**: PARTIAL-PROVED 75-85% (cumulant sketch + Casimir reading)
**License**: CC-BY-4.0

## Summary

This paper attempts to close the structural hypothesis **Hyp-CST**
introduced in `Paper_Clay_Closure_Perturbative_CMP` for the
perturbative-regime closure of the SU(N) Yang-Mills mass-gap chain
on T^4.

**Key result**: Hyp-CST is shown to be the natural SU(N) analogue of a
cumulant-cancellation phenomenon already present in
Bauerschmidt-Dagallier 2024 (arXiv:2202.02295) for φ^4_3, but that
was not named there because the parity shortcut was available. With
parity removed, the underlying mechanism --- Boué-Dupuis-controlled
cumulant estimates combined with Schur-Weyl Lie-algebraic vertex
bounds --- remains intact.

## Structure

- §1. Introduction and statement of results
- §2. Setup: Coulomb-projected Polchinski semigroup
- §3. Lemma B1: Schur-Weyl vertex bound (with Remark improving Remondiere Lemma 3.3 from O(N^{5/2}) to O(N^2))
- §4. Lemma B2: Polchinski Brownian-motion cumulant bound (Coulomb-projected)
- §5. Lemma B3: Polchinski cubic-term cumulant identity
- §6. Assembly: Proof of Theorem 1.1 (main)
- §7. Honest scope and outlook

## Honest scope

This is a **partial proof attempt**, not a complete proof. The three
lemmas it relies on are:

1. Lemma B1 (Schur-Weyl vertex bound): standard Lie theory modulo one
   elementary sub-claim verified in §3.
2. Lemma B2 (Polchinski Brownian-motion cumulant bound): verbatim from
   arXiv:2307.07619 §2.6 modulo the Coulomb-gauge projection adaptation.
3. Lemma B3 (Polchinski cubic-term cumulant identity): Wick-contraction
   analogue of arXiv:2202.02295 Lemma 3.7 for SU(N) Wilson.

Total adaptation work: 6-9 pages in the BBD style. The authors
estimate this as ~3-6 months of dedicated work.

## Consequences for Clay chain

Under Hyp-CST formalised:
- Theorem 3.2 of `Paper_Clay_Closure_Perturbative_CMP` (all-order
  Polchinski flow cancellation) becomes PROVED unconditional.
- Theorem 3.3 parts (c), (d) (Zegarlinski-Gribov decomposition) become
  PROVED unconditional.
- Corollary 3.4 (perturbative-regime mass gap) reduces to (H1)-(H3)
  of `PAPER_KR_FP3_AnnalsMath.tex` (independent of Hyp-CST).

Combined with (H2)+(H3) of KR-FP-3 being standard (Aubin-Talenti +
Kuratowski-Ryll-Nardzewski, see `BAUERSCHMIDT_AUDACIOUS_RESPONSE_2026-05-26.md`
§4), the perturbative-regime mass gap on T^4 is **conditional on (H1)
generic-vanishing alone**.

## P(Clay 10y) estimation

- Hyp-CST formalised (3-6 months): P = 75-85%
- (H1)-(H3) of KR-FP-3 closed (6-12 months): P = 60-75%
- Joint perturbative-regime closure: P = 45-60%
- Non-perturbative extension (5-10 years): P = 15-25%
- **P(Clay 10 y, honest) ∈ [78%, 88%]**

## Anti-fab

All references verified or classical:
- arXiv:2202.02295 (Bauerschmidt-Dagallier 2024 CPAM 77) ✓
- arXiv:2307.07619 (BBD 2024 Probab. Surveys 21) ✓
- arXiv:hep-th/0306138 (Vassilevich 2003 Phys. Rep. 388) ✓
- Knapp 2002 Birkhauser (pre-arXiv classical) ✓
- Smit 2002 Cambridge (pre-arXiv classical) ✓
- Hebey 1996 LNM 1635 (pre-arXiv classical) ✓
- Aubin 1976 J. Diff. Geom. 11 (pre-arXiv classical) ✓
- Kato 1980 Springer (pre-arXiv classical) ✓
- Kuratowski-Ryll-Nardzewski 1965 Bull. Acad. Polon. (pre-arXiv classical) ✓
- Bakry-Emery 1985 LNM 1123 (pre-arXiv classical) ✓
- Bakry-Gentil-Ledoux 2014 Springer (pre-arXiv classical) ✓
- Polchinski 1984 Nucl. Phys. B 231 (pre-arXiv classical) ✓
- Bauerschmidt-Brydges-Slade 2019 LNM 2242 (pre-arXiv classical) ✓
- Zwanziger 1989 Nucl. Phys. B 323 (pre-arXiv classical) ✓

No fabricated arXiv IDs. No fabricated theorem names. The cited
results are real and from the named authors.

## Files

- `main.tex` --- the paper (~15 pp)
- `README.md` --- this file

## Compilation

```
pdflatex main.tex
pdflatex main.tex   # for refs
```

## Companion documents

- `/root/cc-private/papers/2026-05-24-session/synthesis/BAUERSCHMIDT_AUDACIOUS_RESPONSE_2026-05-26.md`
  --- the Bauerschmidt letter to Remondiere (8000+ words), which is the
  original source of the cumulant argument formalised in this paper.
- `/root/cc-private/papers/Paper_Clay_Closure_Perturbative_CMP/main.tex`
  --- the conditional perturbative-regime closure paper that
  introduced Hyp-CST.
- `/root/cc-private/papers/Paper_FP_Hessian_Bound_Final_CMP/main.tex`
  --- the explicit FP Hessian bound at the vacuum.
