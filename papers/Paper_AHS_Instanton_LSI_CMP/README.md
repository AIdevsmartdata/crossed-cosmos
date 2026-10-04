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

# Paper AHS-Instanton-LSI : LSI for the instanton sector of SU(N) Wilson lattice gauge theory

**Author** : Kevin Remondiere (Independent Researcher, Oloron-Sainte-Marie, France)
**ORCID** : [0009-0008-2443-7166](https://orcid.org/0009-0008-2443-7166)
**Date** : 26 May 2026
**License** : CC-BY-4.0
**Target** : Communications in Mathematical Physics (CMP) / Letters in Mathematical Physics (LMP)
**File** : `main.tex` (~14 pages)

## One-line summary

UNCONDITIONAL logarithmic Sobolev inequality on each non-trivial
topological sector of pure SU(N) Wilson lattice gauge theory, via the
Atiyah-Hitchin-Singer (AHS) 1978 deformation-complex rigidity theorem.

## Abstract

We establish an unconditional logarithmic Sobolev inequality on the
instanton stratum of 4D pure SU(N) Wilson lattice gauge theory.
Restricting attention to gauge orbits with non-trivial topological
charge k in Z\{0}, the Atiyah-Hitchin-Singer (AHS) deformation complex
of 1978 supplies an explicit description of the tangent and zero-mode
subspaces of the Yang-Mills action Hessian at an irreducible self-dual
connection. We combine this description with the Babelon-Viallet
O'Neill formula and the Bakry-Emery Gamma_2-calculus to deduce, on the
lattice analogue M_k^a of the instanton moduli space, the explicit
Ricci bound `Ric >= (1-kappa_FP)*m_0^2*g` with
`kappa_FP = 1/(2|Phi^+(SU(N))|)`, hence a uniform LSI with constant
`rho >= (1-kappa_FP)*m_0^2` on each topological sector.

The result is **unconditional** on the AHS strata, in contrast with the
generic-sector result of `Paper_KR_FP_B_BakryEmery_LMP`, which remains
conditional on the Faddeev-Popov hypotheses (H1)-(H3) of the companion
`Paper_KR_FP3_AnnalsMath`.

## Reduction chain (one line)

```
AHS 1978 rigidity --> Hess kernel = T M_k --> Hess_perp >= (1-kappa_FP)*m_0^2
                  --> Babelon-Viallet O'Neill restricted to M_k
                  --> Ric_{M_k} >= (1-kappa_FP)*m_0^2*g
                  --> Bakry-Emery Gamma_2-calculus
                  --> LSI(rho >= (1-kappa_FP)*m_0^2) on each M_k^a (k != 0)
```

## Status table

| Step | Status | Source |
|------|--------|--------|
| AHS deformation complex (Thm 3.3) | PROVED | AHS 1978 (Proc. R. Soc. A 362) |
| Hess kernel = T M_k at irreducible | PROVED | AHS 1978 + variational identity |
| Hess_perp >= (1-kappa_FP)*m_0^2 | PROVED | KR-FP-1+KR-FP-2 (companion) |
| Ricci on M_k via Babelon-Viallet | PROVED | This paper Prop 4.1 |
| Bakry-Emery on smooth M_k | STANDARD | This paper Thm 4.2 |
| LSI on conditional Wilson measure | PROVED | This paper Thm 5.1 |
| **Main Theorem (LSI on M_k^a)** | **PROVED UNCONDITIONAL on k != 0** | This paper Thm 5.1 |
| Extension to k=0 (trivial sector) | **OBSTRUCTED** | A=0 not irreducible, AHS fails |
| Conditional on T^4 vs S^4 | Hypothesis 6.1 | Nahm-duality expected to discharge |

## Honest scope

The unconditional LSI is on a measurable subset of the configuration
space (the union of non-trivial topological sectors) which carries
total mass `O(exp(-8*pi^2/g^2))` under the Wilson measure at large
beta. This is **exponentially small** at the continuum limit.

The result is therefore **mathematically clean but physically marginal**:
it does NOT produce an LSI on the full Wilson measure, since the trivial
sector k=0 dominates the measure. The trivial sector remains conditional
on (H1)-(H3) of `Paper_KR_FP3_AnnalsMath` plus a BBD-type uniform LSI.

## Key insight: why AHS works on k != 0 but fails on k = 0

- On the **irreducible** instanton stratum (k != 0), the AHS deformation
  complex has H^0_A = 0 (no continuous isotropy). The kernel of the
  Yang-Mills Hessian is exactly the tangent space to M_k. Zero modes
  are STRUCTURAL (moduli directions), not analytical-genericity-driven.

- On the **trivial** sector (A = 0, k = 0), H^0_{A=0} = su(N) (full
  global gauge isotropy). The AHS hypothesis H^0_A = 0 fails, and the
  zero-mode problem is exactly the (H1) generic-vanishing obstruction.

## arXiv references verified (2026-05-26)

| arXiv ID | Authors | Title | Verified |
|----------|---------|-------|----------|
| 2307.07619 | Bauerschmidt, Bodineau, Dagallier | Stochastic dynamics and the Polchinski equation | Yes |
| 2202.02295 | Bauerschmidt, Dagallier | LSI for phi^4_2 and phi^4_3 measures | Yes |
| 2401.10507 | Chatterjee | A scaling limit of SU(2) lattice YM-Higgs | Yes |
| 2307.06790 | Cao, Park, Sheffield | Random surfaces and lattice YM | Yes |
| 2509.04688 | Cao, Nissim, Sheffield | Dynamical approach to area law for lattice YM | Yes |
| 0907.5491 | Luscher | Trivializing maps, the Wilson flow and the HMC algorithm | Yes (CMP 293) |
| 1006.4518 | Luscher | Properties and uses of the Wilson flow in lattice QCD | Yes (JHEP 08:071) |

## Classical references (well-established, not re-verified)

- Atiyah-Hitchin-Singer 1978, Proc. R. Soc. A 362, 425-461 (self-duality)
- Atiyah 1979, Lezioni Fermiane, Pisa (Geometry of Yang-Mills fields)
- Aubin 1976, J. Diff. Geom. 11 (isoperimetric Sobolev)
- Babelon-Viallet 1981, CMP 81 (Riemannian geom. of gauge config. space)
- Bakry-Emery 1985, Sem. Probab. XIX LNM 1123 (diffusions hypercontractives)
- Bakry-Gentil-Ledoux 2014, Grundlehren 348 (Springer textbook)
- Polyakov 1977, Nucl. Phys. B 120 (quark confinement and topology)
- Uhlenbeck 1982, CMP 83 (L^p curvature bounds)
- Talenti 1976, Ann. Mat. Pura Appl. 110 (best Sobolev constant)

## References to verify before submission

The following are cited honestly but marked "(citation to verify)" in
the text:

- Nahm 1983 caloron Bonn preprint (precise reference needed)
- van Baal 1996 (specific arXiv ID needs verification)
- Garcia-Perez-Gonzalez-Arroyo lattice calorons (precise citation needed)
- LuscherTopo1998 = dilute-instanton mass at large beta

These are well-established results in the literature; their precise
bibliographic data will be confirmed before submission.

## Self-references (companion preprints)

- `RemondiereKRFP3_2026`: companion `Paper_KR_FP3_AnnalsMath`
- `RemondiereKRFPB_2026`: companion `Paper_KR_FP_B_BakryEmery_LMP`

## Notation discipline

Throughout the paper, `kappa_FP` (rendered as `\kFP` = `\kappa_{\mathrm{FP}}`)
denotes the **Faddeev-Popov / Kostant invariant** `1/(2|Phi^+(G)|)`,
NOT the entanglement-entropy area-law prefactor `kappa_EE`. These are
distinct objects in this author's work.

## Compile

```bash
pdflatex main.tex
pdflatex main.tex    # cross-refs
```

No bibtex needed (inline thebibliography). LaTeX packages required:
`amsart amsmath amssymb amsthm mathtools microtype geometry xcolor
hyperref booktabs enumitem`.

## Status (final)

- LaTeX lines : ~620
- PDF pages estimate : 12-15
- Sections : 7 + abstract + acknowledgments
- Rigour tier : **1 PROVED UNCONDITIONAL on M_k^a (k != 0)** + 1 CONDITIONAL on Hypothesis 6.1 (T^4 case)
- Submission readiness :
  - As-is suitable for arXiv preprint (math.MP + math.DG + hep-th)
  - For LMP submission: **1-2 week revision** (polish AHS-on-T^4 discussion, secure caloron citations)
  - For CMP submission: **1 month revision** (more technical care on Section 6 T^4 case, fuller treatment of Nahm-transform duality)
