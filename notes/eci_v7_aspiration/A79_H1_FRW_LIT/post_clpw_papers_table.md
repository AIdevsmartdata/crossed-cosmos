# A79 — Post-CLPW FRW type-II$_\infty$ literature table

**Date:** 2026-05-05 evening
**Owner:** Opus 4.7 sub-agent A79 (Wave 12 Phase 1)
**Hallu count entering / leaving:** 85 / 85
**Live verification:** all arXiv IDs queried via `https://export.arxiv.org/api/query`
on 2026-05-05 (UA `A79-FRW-typeII-lit-review/1.0`); raw XML/JSON archived in
`raw/arxiv_results.txt`, `raw/arxiv_recent.json`, `raw/key_papers_full.xml`,
`raw/relevant_abstracts.txt`.

CLPW = Chandrasekaran--Longo--Penington--Witten 2023 (arXiv:2206.10780),
established type II$_1$ for the static patch of de Sitter.
"FRW" below means a spatially-homogeneous-isotropic cosmological background
that is **not** the static patch of dS, i.e. genuinely time-dependent
along the comoving worldline (radiation-dominated, matter-dominated, $\Lambda$CDM,
slow-roll inflation, etc.).

## Status legend

- **PROVEN (FRW)** — paper proves type II$_\infty$ (or II$_1$) for a comoving observer
  in a non-stationary cosmological FRW spacetime, with explicit factor classification.
- **PROVEN (qdS)** — proven for slow-roll / quasi-de-Sitter, where the algebra
  still lives on the static patch, with the rolling inflaton acting as a clock.
- **PROVEN (dS)** — proven for global / static-patch de Sitter only,
  no time-dependent background.
- **PROVEN (BH/horizon)** — proven for Killing horizons; FRW-irrelevant
  but methodologically related.
- **GENERAL FRAMEWORK** — observer-/QRF-/dressing-level construction
  applicable to FRW once a clock is supplied; does not by itself prove
  the FRW factor type.
- **ADJACENT** — entropy / IR / asymptotic-safety result on dS that
  constrains but does not establish FRW factor type.

---

## Table

| # | arXiv | Date | Authors | Title (truncated) | Setting | FRW claim? | Status |
|---|------|------|---------|-------------------|---------|------------|--------|
| 1 | [2406.01669](https://arxiv.org/abs/2406.01669) | 2024-06-03 | Kudler-Flam, Leutheusser, Satishchandran | Algebraic Observational Cosmology | FLRW asymptotically dS in past (inflationary epoch), comoving observer | **YES** — gravitationally dressed algebra for comoving observer in FLRW; inflaton zero-mode is the dynamical clock; all states mixed with well-defined vN entropy | **PROVEN (qdS-FLRW)** |
| 2 | [2406.02116](https://arxiv.org/abs/2406.02116) | 2024-06-04 | Chen, Penington | A clock is just a way to tell the time: gravitational algebras in cosmological spacetimes | Slow-roll inflation, evaporating Schwarzschild-dS BH | **YES** — type II$_\infty$ factor for slow-roll inflation with rolling inflaton as physical clock (no external clock); also for compact wedges bounded by extremal surfaces in spacetimes with no Killing symmetry, where the algebra **is** a crossed product | **PROVEN (qdS) + PROVEN (no-isometry wedge)** |
| 3 | [2504.07630](https://arxiv.org/abs/2504.07630) | 2025-04-10 | Speranza | An intrinsic cosmological observer | Slow-roll inflation à la Chen-Penington 2024 | **YES** — recasts CP24 algebra explicitly as crossed product via Connes-Takesaki flow of weights; observer constructed *intrinsically* from the QFT, not added externally | **PROVEN (qdS), structural reformulation** |
| 4 | [2407.20671](https://arxiv.org/abs/2407.20671) | 2024-07-30 | Gomez | Inflationary Cosmology as flow of integrable weights | dS type III$_1$ + integrable-weight centralizers | **PARTIAL** — for *every* integrable weight on $A_{dS}$, the centralizer is a type II$_\infty$ factor admitting a crossed-product representation. Inflationary cosmology = flow of weights. Negative result: no type II$_1$ dS algebra is the $\varepsilon\to 0$ limit | **PROVEN (II$_\infty$ as weight-centralizer) + no-go for $\varepsilon=0$** |
| 5 | [2603.25990](https://arxiv.org/abs/2603.25990) | 2026-03-27 | Seo | Implication of dressed form of relational observable on von Neumann algebra | quasi-dS (background breaks isometries) | **YES** — quasi-dS gets type II$_\infty$ (trace diverges in $G\to 0$ limit) via Stückelberg-style local dressing, **distinct** from the type II$_1$ of pure dS | **PROVEN (qdS), reinforces II$_\infty$ for non-stationary** |
| 6 | [2602.22153](https://arxiv.org/abs/2602.22153) | 2026-02-25 | Blommaert, Chen | Time in gravitational subregions and in closed universes | JT gravity subregion + Milne-type closed Big-Bang universes | **YES (Milne)** — extrinsic curvature of Cauchy slices acts as physical clock; type II crossed-product construction repeated for **Milne-type closed BB universes** (no observer needed) | **PROVEN (Milne BB), 2D** |
| 7 | [2511.00622](https://arxiv.org/abs/2511.00622) | 2025-11-01 | Chen, Xu | An algebra for covariant observers in de Sitter space | $d$-dim dS, all $SO(1,d)$ constraints (linearization-instability cure) | **NO (dS)** — covariant observer = superposition of geodesics with fluctuating static patch; type II classification | **PROVEN (dS, covariant)** |
| 8 | [2510.24833](https://arxiv.org/abs/2510.24833) | 2025-10-28 | Giddings | Gravitational dressing: from the crossed product to more general algebraic structure | Generic spacetime, perturbative gravity | **NO** — argues the crossed-product / III$\to$II transition is a small piece of a more general (non-algebraic, holographic-like) structure | **GENERAL FRAMEWORK** |
| 9 | [2505.22708](https://arxiv.org/abs/2505.22708) | 2025-05-28 | Giddings | Quantum gravity observables: observation, algebras, and mathematical structure | Generic | **NO** — relational-observables classification; gravitational dressings reduce to crossed products in special cases | **GENERAL FRAMEWORK** |
| 10 | [2412.21185](https://arxiv.org/abs/2412.21185) | 2024-12-30 | Jensen, Raju, Speranza | Holographic observers for time-band algebras | AdS time-band + bulk macroscopic observer | **NO (AdS)** — coarse-grained algebra has non-trivial commutant; reduces to modular crossed product at leading $G_N$. Theorem: this is the **only** crossed product of a type III$_1$ algebra producing a tracial algebra | **PROVEN (AdS) + uniqueness theorem methodologically applicable to FRW** |
| 11 | [2405.00114](https://arxiv.org/abs/2405.00114) | 2024-04-30 | De Vuyst, Eccles, Hoehn, Kirklin | Gravitational entropy is observer-dependent | Generic crossed product + QRF | **NO** — "PW=CLPW": Page-Wootters $\equiv$ CLPW. Different observers $\to$ different II algebras $\to$ different entropies | **GENERAL FRAMEWORK (QRF=observer)** |
| 12 | [2412.15502](https://arxiv.org/abs/2412.15502) | 2024-12-20 | De Vuyst, Eccles, Hoehn, Kirklin | Crossed products and quantum reference frames | Generic perturbative-gravity subregion | **NO** — extension of [11] to many observers, possibly entangled clocks; observer-dependent entropy + four worked examples | **GENERAL FRAMEWORK** |
| 13 | [2411.19931](https://arxiv.org/abs/2411.19931) | 2024-11-29 | De Vuyst, Eccles, Hoehn, Kirklin | Linearization (in)stabilities and crossed products | Generic, with/without isometry, with/without boundary | **PARTIAL (closed)** — for **spatially closed** spacetimes the second-order boost constraints are unambiguously justified; this includes closed FRW | **PROVEN (closed-FRW constraints) at the level of perturbation theory** |
| 14 | [2601.07915](https://arxiv.org/abs/2601.07915) | 2026-01-12 | Chandrasekaran, Flanagan | Subregion algebras in classical and quantum gravity | Killing horizons + finite causal diamonds | **NO** — type II$_\infty$ at each horizon cut with vN entropy = generalized entropy; Connes cocycle = area op; quantum focusing conjecture | **PROVEN (BH/horizon)** |
| 15 | [2405.00847](https://arxiv.org/abs/2405.00847) | 2024-05-01 | Faulkner, Speranza | Gravitational algebras and the generalized second law | Killing horizons | **NO** — GSL from crossed product; novel generalization to interacting + asymptotically flat | **PROVEN (BH/horizon)** |
| 16 | [2503.19957](https://arxiv.org/abs/2503.19957) | 2025-03-25 | Kudler-Flam, Prabhu, Satishchandran | Vacua and infrared radiation in de Sitter QFT | Free fields on dS | **NO** — necessary+sufficient condition for dS-invariant vacuum: commutation with horizon "memory observable". Massless minimally-coupled scalar fails | **ADJACENT** (dS IR pathology forbids dS-invariant vacuum for $m=0,\xi=0$ — directly relevant to ECI's $\xi=1/6$ choice in `frw_note.tex`) |
| 17 | [2511.17382](https://arxiv.org/abs/2511.17382) | 2025-11-21 | Ribes-Metidieri, Agullo, Bonga | Entanglement and correlations between local observables in dS | dS Bunch-Davies, local modes | **NO** — fully-local entanglement between compactly supported modes; curvature ↑ correlations but ↓ entanglement | **ADJACENT** |
| 18 | [2502.05135](https://arxiv.org/abs/2502.05135) | 2025-02-07 | D'Angelo, Ferrero, Fröb | De Sitter quantum gravity within asymptotic safety | dS Einstein-Hilbert flow | **NO** — UV fixed point evidence | **ADJACENT** |
| 19 | [2404.12324](https://arxiv.org/abs/2404.12324) | 2024-04-18 | Cadamuro, Fröb, Moreira-Ferrera | The Sine-Gordon QFT in de Sitter spacetime | Massless SG, $\beta^2 < 4\pi$, dS | **NO** — interacting Haag-Kastler net on dS, but boost-invariance broken | **ADJACENT (interacting net on dS)** |
| 20 | [2412.15549](https://arxiv.org/abs/2412.15549) | 2024-12-20 | Penington, Witten | Algebras and states in super-JT gravity | $\mathcal{N}=2$ super-JT | **NO** — type II$_1$ at each boundary; Lorentzian derivation of algebraic structure of canonically-quantized bosonic JT + matter | **PROVEN (2D super-JT II$_1$)** |
| 21 | [2507.01419](https://arxiv.org/abs/2507.01419) | 2025-07-02 | Requardt | The Crossed Product, Modular Dynamics and III$\to$II$_\infty$ transition | Generic, conceptual | **NO** — review-style analysis of modular evolution and projector/partial-isometry change at III$\to$II$_\infty$ | **GENERAL FRAMEWORK** |
| 22 | [2501.06009](https://arxiv.org/abs/2501.06009) | 2025-01-10 | Requardt | Role of type II$_\infty$ vN algebras and tensor structure in QG | Generic, conceptual | **NO** — type II$_\infty$ as $\mathcal{B}(\mathcal{H}_I)\otimes\mathcal{R}_{0,1}$; "internal" II$_1$ encodes hidden gravitational dof | **GENERAL FRAMEWORK** |

---

## Verification log

All arXiv IDs above were live-verified via the arXiv API on 2026-05-05.
The 7 flagship FRW-relevant papers (1, 2, 3, 4, 5, 6, 7 in the table) were
double-verified via direct `id_list` lookup; raw XML in
`raw/key_papers_full.xml` (16104 bytes, 7/7 entries returned, titles +
authors + dates match the table above).

No bibdata was supplied by Mistral or any external LLM cross-check;
all entries originate from arXiv API XML returned to this session.

## Anti-hallu ledger

- 22 entries, 22 verified arXiv IDs.
- 0 fabricated authors.
- 0 fabricated titles.
- 0 Mistral-sourced refs.
- 0 paywalled-only refs (all on arXiv).

**Hallu count: 85 (held).**
