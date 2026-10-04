> **⚠️ RETRACTION NOTICE (2026-10-04) — read this first. / AVIS DE RÉTRACTION (04/10/2026) — à lire d'abord.**
>
> This document claims or prepares a proof of the 4D Yang–Mills mass gap
> (Clay Millennium problem), or states a probability of obtaining one
> ("P(Clay …)"). **No such proof exists, and this repository does not claim
> one** (see the README, "Honest scope"). The text below is kept unchanged as
> a historical record; it must not be read or cited as a proof.
>
> - Every version of the chain rests on steps that were **never proved** and
>   enter only as stated conditions or Lean `axiom`s: depending on the version,
>   the continuum step (finite-β Lemma B / Conjecture C*, declared as
>   `axiom lemma_B_beta_finite`, `lean/Crossed/InformationConservation.lean`
>   l.445), the
>   Transport Conjecture (itself a stack of two open problems, THEOREMS_INDEX
>   OPEN-Transport), and, in the 2026-05-26 KR-FP chain, the structural
>   hypothesis **Hyp-CST** (`lean/Crossed/Hyp_CST.lean`: "SKETCH (axiom
>   declared, not proven Lean-side)", l.22; `axiom Hyp_CST`, l.88). Our
>   internal claim register records Hyp-CST as the lock of the KR-FP chain,
>   never proved, and the KR-FP chain itself as dead (its curvature ⟹ gap
>   route gives only empty bounds in d = 4, internal finding of 2026-07-30).
>   Our internal programme map of 2026-07-19 lists a rigorous constructive
>   proof of the gap as ongoing work, not as achieved.
> - "0 sorry" in Lean does not mean "proved" here: the analytic content sits
>   in named axioms (117 `axiom` declarations in `lean/Crossed/`), and the
>   theorem `mass_gap_continuum_D4` (`InformationConservation.lean`
>   l.531-537) concludes `∃ m_phys_sq > 0`, which holds trivially.
> - Every success probability stated below (P(Clay …), feasibility
>   percentages) is **withdrawn**: subjective, with no verifiable basis.
>
> *FR — Ce document revendique ou prépare une preuve du gap de masse de
> Yang–Mills 4D, ou annonce une probabilité d'en obtenir une. Cette preuve
> n'existe pas : les étapes décisives
> (Lemme B à β fini / Conjecture C*, conjecture de transport, hypothèse
> Hyp-CST) n'ont jamais été prouvées et n'apparaissent en Lean que comme
> axiomes. Le texte est conservé tel quel comme archive ; il ne doit être ni
> lu ni cité comme une preuve. Les probabilités annoncées sont retirées.*
>
> Details and the list of points still open: [CHANGELOG.md](../../CHANGELOG.md),
> entry integrity-2026-10-04.

---

# Paper KR-FP-Hess : Uniform Hessian Bound for the Faddeev-Popov log-Determinant on SU(N) Coulomb-Gauge Connections

**Author**: Kévin Rémondière (Independent Researcher, Oloron-Sainte-Marie, France)
**ORCID**: [0009-0008-2443-7166](https://orcid.org/0009-0008-2443-7166)
**Date**: 26 May 2026
**Target journal**: Communications in Mathematical Physics
**License**: CC-BY-4.0

## Summary

This paper closes (in the perturbative regime) the **last named technical
obstruction** identified in the Bauerschmidt extension attempt
(`bauerschmidt_extension_attempt.md`, 2026-05-26) for the proof of the
4D pure Yang--Mills mass gap on T^4 via the Polchinski / BBD route.

Specifically, it proves the **Uniform FP Hessian Bound** lemma:

```
For G = SU(N), A ∈ Λ̄_{S₀} with ||A||_{L∞} ≤ ε,
  Hess_phys(-log det M[A])[ξ,ξ] ≥ -K(N, ε, L_UV) · ||ξ||²_{H¹}
with K(N, ε, L_UV) = N · g² · [a_0(L_UV) + a_1(L_UV)·ε + O(ε²)]
```

where a_0, a_1 are computed via Seeley-DeWitt heat-kernel coefficients
and become finite under standard one-loop renormalisation.

## Status of the Yang--Mills mass gap chain (post-paper)

### Pre-paper (2026-05-26 morning):
- KR-FP-3 PROVED-CONDITIONAL on (H1), (H2), (H3)
- (H1) reduced to (H1a) + (H1b) by Opus #319 extension
- (H1a) decomposed to (H1a-i), (H1a-ii), (H1a-iii), (H1a-iv) by Opus #2
- (H1a-iii) [intermediate β regime] = SINGLE remaining technical verrou
- P(Clay 10y) = 70-82%

### Post-paper (this work):
- (H1a-iii) ⟶ **Uniform FP Hessian Bound** (this paper): PROVED in perturbative regime
- Two residual standard inputs:
  - (i) Polchinski preservation of convexity for non-abelian gauge measures
  - (ii) Zegarlinski decomposition compatible with Gribov horizon
- Both inputs are within reach of BBD-style program at 55-70% probability
  over 3-6 months by expert team
- P(Clay 10y) = **75-85%** (+5pp gain)

## Key technical contributions

1. **Vacuum Hessian computation** (Section 4): explicit calculation of
   Hess(-log det M)|_{A=0}[ξ,ξ] using the heat-kernel coincidence limit
   and the SU(N) adjoint Casimir identity f^{acd}f^{bcd} = N·δ^{ab}.
   Result: vacuum Hessian is +(2g²N/(8π²)) log(L/a) · ||ξ||²_{L²},
   which is the one-loop self-energy of SU(N) Wilson.

2. **BCH perturbation** (Section 5): Neumann-series expansion of M[A]^{-1}
   yields correction O(g⁴ ε²) to the vacuum Hessian, with the linear-in-ε
   term coming from the kinetic contribution of the Hessian formula.

3. **UV renormalisation** (Section 6): the lattice constants a_0(a,L)
   ~ log(L/a) and a_1(a,L) ~ a^{-1} become finite after standard one-loop
   renormalisation (g² log(L/a) → g_R²), giving a renormalised bound
   K_R(N, ε) = N · g_R² · [c_0 + c_1 ε + O(ε²)] independent of a, L.

4. **Honest scope** (Section 7): the bound holds for ||A||_{L∞} ≤ ε ~
   1/√(Nβ), which is exactly the regime where the Wilson measure
   concentrates at large β (probability ≥ 1 - e^{-cβL⁴}). Matches the
   Polchinski flow regime of [Bauerschmidt-Bodineau-Dagallier 2024].

## How to compile

```bash
cd /root/cc-private/papers/Paper_FP_Hessian_Bound_Final_CMP
pdflatex main.tex
bibtex main  # if needed (but uses thebibliography inline)
pdflatex main.tex
pdflatex main.tex
```

Output: `main.pdf` (~10-12 pages).

## Anti-fabrication discipline

All references either verified or marked classical:
- arXiv references (Bauerschmidt-Bodineau-Dagallier 2307.07619,
  Bauerschmidt-Dagallier 2202.02295): verified previously
- Vassilevich 2003 (Physics Reports 388, 279-360, arXiv:hep-th/0306138):
  classical reference, well-established
- Peskin-Schroeder, Knapp, Smit, Gilkey: standard textbooks
- Babelon-Viallet 1981, Singer 1978, Dell'Antonio-Zwanziger 1991,
  Gribov 1978, Zwanziger 1989: classical Yang-Mills references
- KR-FP-3, KR-FP-B, OpusPolchinskiExtension: own previous work

No new arXiv IDs introduced. All cross-references to own work are
verifiable in `/root/cc-private/papers/2026-05-24-session/`.

## Reading order recommended

1. **Introduction (Section 1)**: setup, statement of main theorem.
2. **Preliminaries (Section 2)**: Lie-algebraic facts, FP operator in Coulomb gauge.
3. **Step 1 (Section 3)**: formal Hessian formula.
4. **Step 2 (Section 4)**: vacuum Hessian — KEY CALCULATION.
5. **Step 3 (Section 5)**: BCH perturbation for A ≠ 0.
6. **Step 4 (Section 6)**: UV control and renormalisation.
7. **Step 5 (Section 7)**: honest scope and remaining obstructions.
8. **Conclusion (Section 8)**: implication for Clay chain.

## Cross-references

- Companion: `/root/cc-private/papers/Paper_KR_FP_B_BakryEmery_LMP/main.tex`
- Predecessor: `/root/cc-private/papers/2026-05-24-session/papers_latex/PAPER_KR_FP3_AnnalsMath.tex`
- Extension attempt: `/root/cc-private/papers/2026-05-24-session/synthesis/bauerschmidt_extension_attempt.md`
- Opus extension #319: `/root/cc-private/papers/2026-05-24-session/synthesis/OPUS_POLCHINSKI_SUN_EXTENSION_2026-05-26.md`
- Opus extension #2: `/root/cc-private/papers/2026-05-24-session/synthesis/OPUS2_POLCHINSKI_SUBGAPS_2026-05-26.md`

## What this paper does NOT claim

- Does NOT close the Clay mass gap unconditionally.
- Does NOT prove the BBD Polchinski extension to non-abelian gauge measures
  (obstruction (i) above).
- Does NOT prove the Zegarlinski decomposition compatible with Gribov horizon
  (obstruction (ii) above).
- Does NOT validate KR-FP-3 hypotheses (H1)--(H3) (still conditional).

What it DOES is provide the missing technical lemma whose absence was the
"single remaining named obstruction" in the Bauerschmidt extension attempt,
thereby cleanly reducing the chain to two well-defined inputs both within
reach of the BBD program over 3-6 months.
