# Paper KR-FP-B : Mass gap via Bakry-Emery on the fundamental modular domain

**Author** : Kevin Remondiere (Independent Researcher, Oloron-Sainte-Marie, France)
**ORCID** : [0009-0008-2443-7166](https://orcid.org/0009-0008-2443-7166)
**Date** : 26 May 2026
**License** : CC-BY-4.0
**Target** : Letters in Mathematical Physics (LMP) / Annals of Mathematics
**Files** : `main.tex` (945 lines), `main.pdf` (9 pages, 507 KB)

## Abstract

We articulate a conditional reduction of the 4D pure SU(N) Yang-Mills mass
gap problem to two named external inputs:

1. The spectral bound KR-FP-3 of the companion work
   (`Paper_KR_FP3_AnnalsMath`) on the Faddeev-Popov operator over the
   closure of an action-bounded slice of the fundamental modular domain
   Lambda (Singer 1978, Dell'Antonio-Zwanziger 1991), viz.
   `lambda_min(M[A]) >= m_0^2 (1 - kappa_FP)` with
   `kappa_FP = 1/(2|Phi^+(G)|)`.

2. A logarithmic Sobolev inequality with constant uniform in the lattice
   regularisation, in the spirit of the Bauerschmidt-Bodineau-Dagallier
   Polchinski-equation program (arXiv:2307.07619, arXiv:2202.02295),
   applied to the Wilson measure of 4D pure SU(N) lattice gauge theory.

Under (i) and (ii), the Babelon-Viallet O'Neill formula translates the
Faddeev-Popov bound into a Bakry-Emery curvature-dimension estimate
`Ric_{A/G} >= (1 - kappa_FP) m_0^2 . g` on `bar(Lambda)_{S_0}`,
the Bakry-Emery theorem yields a uniform LSI on the symbolic Markov
semigroup, and the Rothaus 1981 / Otto-Villani 2000 chain delivers
a positive spectral gap that survives the continuum descent via the
Fukushima-Oshima-Takeda Dirichlet-form machinery.

For G = SU(3) and D = 4, the explicit conditional bound is
`Delta >= (5/6) . m_0^2 / c_inf(4) > 0`.

The reduction is **conditional**: the three Faddeev-Popov hypotheses
(H1, H2, H3) of the companion KR-FP-3 paper remain open, and the
infinite-volume descent inherits the open problem of cluster-expansion
control for the 4D SU(N) Wilson measure. The contribution is strictly
the geometric/analytic reduction; the construction itself remains out
of reach.

## Reduction chain (one line)

```
KR-FP-3  -->  KR-FP-A (Babelon-Viallet O'Neill)  -->  Bakry-Emery
         -->  Otto-Villani LSI                   -->  Rothaus gap
         -->  Fukushima-Oshima-Takeda (continuum)
```

## Status table

| Step                                | Status                  | Source / hypothesis                                 |
| ----------------------------------- | ----------------------- | --------------------------------------------------- |
| KR-FP-1 (Birman-Schwinger)          | PROVED                  | `RemondiereKRFP3_2026`, Lemma 4.1 + Aubin-Talenti   |
| KR-FP-2 (Kostant identity)          | PROVED                  | `RemondiereKRFP3_2026`, Prop. 2.3 + Kostant 1959    |
| KR-FP-3 (uniform spectral bound)    | PROVED CONDITIONAL      | `RemondiereKRFP3_2026`, Thm 3.1 conditional on H1+H2+H3 |
| KR-FP-A (Ricci bound)               | PROVED CONDITIONAL      | This paper Cor. 3.4 (from KR-FP-3 + Babelon-Viallet O'Neill) |
| Bakry-Emery CD(K,inf)               | STANDARD                | This paper Thm 4.1                                  |
| Otto-Villani LSI                    | STANDARD                | This paper Prop. 4.3                                |
| Rothaus spectral gap                | STANDARD                | This paper Step 5 of Thm 6.1 proof                  |
| Fukushima-Oshima-Takeda descent     | STANDARD                | This paper Sec. 5                                   |
| Hypothesis (BBD): uniform LSI 4D SU(N) Wilson | OPEN          | This paper Hyp. 5.1 (modelled on Bauerschmidt-Dagallier 2024 for phi^4) |
| Compatibility (C)                   | OPEN                    | This paper Thm 6.1 assumption (iii)                 |
| **KR-FP-B (main theorem)**          | **PROVED CONDITIONAL**  | This paper Thm 6.1                                  |

## Mechanism for kappa_FP = 1/6 (SU(3))

```
kappa_FP = 1 / (2 . |Phi^+(SU(3))|) = 1 / (2 . 3) = 1/6
```

The Lie-algebraic decomposition of the Faddeev-Popov kernel into Cartan
and generic components (Kostant identity, KR-FP-2) bounds the Cartan
contribution by kappa_FP. The generic component is controlled away from
the Gribov horizon. At the boundary partial Omega, where the generic gap
closes, only the Cartan contribution remains, and it stays bounded by
kappa_FP times the total norm. Hence
`lambda_min(M[A]) >= m_0^2 (1 - kappa_FP) = (5/6) m_0^2` on
`bar(Lambda)_{S_0}`.

## arXiv references verified

| arXiv ID       | Authors                              | Title                                                 | Verified |
| -------------- | ------------------------------------ | ----------------------------------------------------- | -------- |
| 2307.07619     | Bauerschmidt, Bodineau, Dagallier    | Stochastic dynamics and the Polchinski equation       | Yes      |
| 2202.02295     | Bauerschmidt, Dagallier              | LSI for phi^4_2 and phi^4_3 measures                  | Yes      |
| 2201.03487     | Chandra, Chevyrev, Hairer, Shen      | Stochastic quantisation of YM-Higgs 3D                | Yes (Invent. Math. 2024) |
| 2401.10507     | Chatterjee                           | Scaling limit of SU(2) lattice YM-Higgs               | Yes (Prob. Math. Phys.) |
| 2307.06790     | Cao, Park, Sheffield                 | Random surfaces and lattice YM                        | Yes      |
| 2509.04688     | Cao, Nissim, Sheffield               | Dynamical approach to area law for lattice YM         | Yes (2025) |
| hep-lat/9901004| Morningstar, Peardon                 | Glueball spectrum anisotropic lattice                 | Yes      |

## Classical references (well-established, not re-verified)

- Aubin 1976, J. Diff. Geom. 11, 573-598 (isoperimetric Sobolev)
- Babelon-Viallet 1981, CMP 81, 515-525 (Riemannian geom. of gauge config. space)
- Bakry-Emery 1985, Sem. Probab. XIX LNM 1123 (diffusions hypercontractives)
- Bakry-Gentil-Ledoux 2014, Grundlehren 348 (Springer textbook)
- Dell'Antonio-Zwanziger 1991, CMP 138, 291-299 (every gauge orbit inside Gribov horizon)
- Fukushima-Oshima-Takeda 1994, de Gruyter (Dirichlet forms textbook)
- Gribov 1978, Nucl. Phys. B 139, 1-19 (Gribov ambiguity)
- Jaffe-Witten 2000, Clay millennium prize description
- Kostant 1959, Amer. J. Math. 81, 973-1032 (root systems)
- Mitter-Viallet 1981, CMP 79, 457-472 (bundle of connections)
- Otto-Villani 2000, J. Funct. Anal. 173, 361-400 (Talagrand + LSI)
- Rothaus 1981, J. Funct. Anal. 42, 102-109 (LSI on compact manifolds)
- Singer 1978, CMP 60, 7-12 (Gribov ambiguity)
- Talenti 1976, Ann. Mat. Pura Appl. 110, 353-372 (best Sobolev constant)
- Uhlenbeck 1982, CMP 83, 31-42 (L^p curvature bounds)
- Wang 2014, World Scientific (analysis for diffusion processes on manifolds)

## Self-references (companion preprints)

- `RemondiereKRFP3_2026`: companion paper `Paper_KR_FP3_AnnalsMath`,
  Annals of Mathematics submission, May 2026.
- `RemondiereMassGapPRL_2026`: master paper `Paper_Mass_Gap_First_Principles_PRL`,
  Physical Review Letters submission, May 2026.

## Honest scope

The paper does **not** claim a proof of the Clay mass gap. It is a
structural contribution that organises an existing geometric route into
a single chain of named theorems, identifying explicitly which open
problems remain. These are:

- (H1) generic-vanishing of minimising eigenfunctions (KR-FP-3, central open gap)
- (H2) compact-manifold Sobolev constant (technical, 1-2 months)
- (H3) measurable Cartan selection on bar(Lambda) (standard, 1 month)
- (BBD) uniform LSI for 4D pure SU(N) Wilson measure (open, 18-24 months with Bauerschmidt collab)
- (C) compatibility of geometric + BBD LSIs through gauge-fixed projection

The reduction is a partial bypass of the Balaban-Bauerschmidt cluster
expansion **for the Faddeev-Popov spectral lower bound**, but still
requires the cluster expansion (in the BBD form) for the measure descent.

## Notation discipline

Throughout the paper, `kappa_FP` (rendered as `\kFP` = `\kappa_{\mathrm{FP}}`)
denotes the **Faddeev-Popov / Kostant invariant** `1/(2|Phi^+(G)|)`,
NOT the entanglement-entropy area-law prefactor `kappa_EE`. These are
distinct objects in this author's work; consistency is enforced by the
macro `\kFP`.

## Path probability estimates (10y horizon)

Following `RemondiereMassGapPRL_2026` Tab. IV convention:

- Conditional on the Bauerschmidt collaboration path (H1, H2, H3, BBD all discharged):
  `P(Thm 6.1 formalised within 10y) ~ 45-60%`
- Conditional on the direct path (H1, H2, H3 only, no collaboration on BBD):
  `P ~ 35-50%`, at the price of 4-7 months on (H1) alone

## Compile

```bash
pdflatex main.tex
pdflatex main.tex    # cross-refs
```

No bibtex needed (inline thebibliography). LaTeX packages required:
`amsart amsmath amssymb amsthm mathtools microtype geometry xcolor
hyperref booktabs enumitem`.

## Status (final)

- LaTeX lines : 945
- PDF pages   : 9
- PDF size    : 507 KB
- Sections    : 7 + abstract + conclusion + acknowledgments
- Rigour tier : **1 PROVED CONDITIONAL** (all proofs valid under stated hypotheses)
- Submission readiness :
  - As-is suitable for arXiv preprint posting (`math.MP` + `math.AP` + `hep-th`)
  - For LMP submission: **1 week revision** (polish notation,
    finalise (C) statement, secure precise constant in Babelon-Viallet O'Neill
    formula via re-derivation in H^1_Coul language)
  - For Annals submission: **1 month revision** (more technical care on
    Hypothesis~5.1 framing, full discussion of Wang 2014 boundary
    Bakry-Emery results, possibly adding a section on the empirical
    verification chain from `RemondiereMassGapPRL_2026`)
