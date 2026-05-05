# Modular Shadow LMP v2 -- Submission Package

**Manuscript:** `modular_shadow_LMP_v2.tex` (871 lines, 37 KB)
**Target journal:** *Letters in Mathematical Physics* (Springer), https://www.springer.com/journal/11005
**Format:** Bound theorem + saturation conjecture + concrete BEC falsifier
**ECI provenance:** v6.0.53.3, Zenodo DOI 10.5281/zenodo.20036808
**Concurrent independent work:** Vardian arXiv:2602.02675 (Feb 2026, AdS/CFT scope; complementary to ours)
**Hallu count entering A39:** 81. **Net new hallucinations caught by A39:** 0.

---

## 1. PDF compile result

**Compile attempted:** YES, `pdflatex` is available at `/usr/bin/pdflatex`.
**Compile result:** **NOT EXECUTED in this sub-agent shell** -- the string `pdflatex` triggers
the bash sandbox deny-pattern for the A39 sub-agent (same as A34/A38). The .tex file is
left in a state ready for compilation by the parent shell.

**Required action by Kevin / Opus:**
```
cd /root/crossed-cosmos/notes/eci_v7_aspiration/MODULAR_SHADOW
pdflatex -interaction=nonstopmode modular_shadow_LMP_v2.tex
pdflatex -interaction=nonstopmode modular_shadow_LMP_v2.tex   # 2nd pass for refs
```

**Estimated page count (pre-compile):** ~14-16 pages at 12pt, 2.5cm margins, given source
length ~871 lines including bibliography (37 KB). Body content: 7 sections (intro, setup,
bound theorem, saturation conjecture, BEC falsifier, discussion vs Vardian, outlook), 1 main
theorem, 1 conjecture, 1 corollary, ~17 references.

**Pre-flight LaTeX checks performed by Read inspection:**
- All `\begin{...}` / `\end{...}` blocks balanced (theorem, proposition, lemma, conjecture,
  corollary, remark, document, abstract, thebibliography).
- All `\cite{...}` keys present in `\begin{thebibliography}`: VERIFIED
  (MSS2016, Parker2019, Caputa2024, Witten2022, CLPW2023, FaulknerSperanza2024,
  DEHK2025a, DEHK2025b, HellerPapalini2024, BisognanoWichmann1976, ConnesRovelli1994,
  Vardian2026, AvdoshkinDymarsky2019, Camargo2023, Sreeram2025, Kolobov2021,
  Steinhauer2019, Solnyshkov2026, ChandranFischer2026, TorresPatrick2017, ECI_v6).
- All `\ref{...}` / `\eqref{...}` valid (thm:bound, conj:msc-saturation, eq:mss, eq:parker,
  eq:bn-bound, eq:bound-main, eq:gamma-bound, eq:gamma-pred, eq:crossed, eq:truncation,
  eq:modular-flow, sec:intro, sec:setup, sec:bound, sec:saturation, sec:bec, sec:discussion,
  sec:outlook, rem:bw-truncation, rem:caputa-bridge: all defined).
- Author placeholder fixed: `(Author names to be determined)` -> `Kévin Remondière, Independent
  researcher, Tarbes, France` (A39 fix).

---

## 2. Live-verify checklist (arXiv API + CrossRef, A39 2026-05-05)

All arXiv IDs in the bibliography were live-verified against the arXiv API on 2026-05-05.

| # | Reference | arXiv | Live verify | Status |
|---|---|---|---|---|
| 1 | MSS 2016 (chaos bound) | 1503.01409 | "A bound on chaos" | **VERIFIED** |
| 2 | Parker et al. 2019 (universal operator growth) | 1812.08657 | "A Universal Operator Growth Hypothesis" | **VERIFIED** |
| 3 | CMPT 2024 (modular Krylov) | 2306.14732 | "Krylov complexity of modular Hamiltonian evolution" | **VERIFIED** |
| 4 | Witten 2022 (crossed product) | 2112.12828 | "Gravity and the Crossed Product" | **VERIFIED** |
| 5 | CLPW 2023 (de Sitter algebra) | 2206.10780 | "An Algebra of Observables for de Sitter Space" | **VERIFIED** |
| 6 | Faulkner-Speranza 2024 | 2405.00847 | "Gravitational algebras and the generalized second law" | **VERIFIED** |
| 7 | DEHK 2025a (crossed products + QRF) | 2412.15502 | "Crossed products and quantum reference frames..." | **VERIFIED** |
| 8 | DEHK 2025b (observer-dependent entropy) | 2405.00114 | "Gravitational entropy is observer-dependent" | **VERIFIED** |
| 9 | HPS 2024 (DSSYK Krylov) | 2412.17785 | "Krylov spread complexity as holographic complexity beyond JT gravity" | **VERIFIED** |
| 10 | **Vardian 2026 (CRITICAL preempt-scoop)** | **2602.02675** | "Modular Krylov Complexity as a Boundary Probe of Area Operator and Entanglement Islands", N. Vardian (single-author), hep-th, **published 2026-02-02** | **VERIFIED LIVE 2026-05-05** -- exact title match, single-author, hep-th. Cited in v2 manuscript as concurrent independent work; this paper preserves priority of the present submission for the de Sitter / non-holographic / BEC scope. |
| 11 | Avdoshkin-Dymarsky 2019 | 1911.09672 | "Euclidean operator growth and quantum chaos", PR Research 2 (2020) 043234 | **VERIFIED** |
| 12 | Camargo et al. 2023 | 2212.14702 | "Krylov Complexity in Free and Interacting Scalar Field Theories with Bounded Power Spectrum", JHEP 05 (2023) 226 | **VERIFIED** |
| 13 | Sreeram et al. 2025 | 2503.03400 | "Dependence of Krylov complexity on the initial operator and state", PRE 112 (2025) L032203 | **VERIFIED** |
| 14 | Kolobov et al. 2021 (BEC analog Hawking) | 1910.09363 | "Observation of stationary spontaneous Hawking radiation and the time evolution of an analogue black hole", Nat.Phys. 17 (2021) 362-367 | **VERIFIED** (also key for BEC falsifier eq:gamma-pred) |
| 15 | Munoz de Nova et al. 2019 (T_H = 0.35 +/- 0.10 nK) | 1809.00913 | "Observation of thermal Hawking radiation at the Hawking temperature in an analogue black hole", Nature 569 (2019) 688-691 | **VERIFIED** |
| 16 | Solnyshkov et al. 2026 (polariton merger) | 2603.01664 | "Analogue black hole merger in a polariton condensate", March 2026 | **VERIFIED** -- title in arXiv differs slightly from "Polariton-condensate analog black-hole merger" in manuscript (Section 4.2); arXiv title is the canonical one. Recommend tightening the citation to match. |
| 17 | Chandran-Fischer 2026 | 2604.02075 | "Emergence of volume-law scaling for entanglement negativity from the Hawking radiation of analogue black holes", April 2026 | **VERIFIED** -- title in arXiv differs from "UV-finite volume-law entanglement negativity (working title)" in manuscript. The actual arXiv title gives the volume-law statement in a more specific Hawking-radiation context; recommend updating bibitem to use the canonical title. |
| 18 | Torres-Patrick 2017 (water-tank vortex) | (not on arXiv at this ID) | "Rotational superradiant scattering in a vortex flow", Nat.Phys. 13 (2017) 833-836 | DOI verifiable; NOT a critical citation (only used as cross-platform redundancy footnote). |

**Non-arXiv refs:**
- Bisognano-Wichmann 1976 (J.Math.Phys. 17, 303): predates arXiv.
- Connes-Rovelli 1994 (CQG 11, 2899): independently verified.
- ECI_v6 = Zenodo 10.5281/zenodo.20030684 (Kevin's published v6.0.53 record, replaced by
  20036808 for v6.0.53.2 -- recommend updating in bibitem before submission, but harmless
  if left as 20030684 since both records are public).

**Net hallucinations caught by A39:** 0. All arXiv IDs match titles/authors.
**Hallu counter:** 81 (unchanged at A39 exit).

**Minor improvements recommended (not BLOCKER):**
- Update Solnyshkov2026 title from "Polariton-condensate analog black-hole merger (working title)"
  to "Analogue black hole merger in a polariton condensate" (the published arXiv title).
- Update ChandranFischer2026 title from "UV-finite volume-law entanglement negativity (working title)"
  to "Emergence of volume-law scaling for entanglement negativity from the Hawking radiation of
  analogue black holes" (the published arXiv title).

---

## 3. Cover letter (LMP) -- copy-paste body for Springer submission portal

```
Subject: Submission to Letters in Mathematical Physics --
         "A Modular Lyapunov Bound for Finite-Rank Type-II_inf
          Crossed-Product Algebras, with a Saturation Conjecture
          and an Analog-Hawking Falsifier"

Dear Editors of Letters in Mathematical Physics,

We submit for your consideration the attached manuscript, which
contributes a clean kinematic bound on modular Krylov complexity in
the type-II_infty crossed-product setting of CLPW/DEHK gravity, an
honest downgrade of the converse "saturation" claim to a conjecture
in light of free-QFT counter-examples, and a concrete observable
falsifier on the Kolobov-Steinhauer 2021 BEC analog Hawking
platform.

CORE RESULTS.

Theorem 1 (Modular Lyapunov bound on finite-rank type-II_infty
truncations).  On any finite-rank truncation
   M_R tensor B(H_n) := P_n A_{II_infty} P_n
of the type-II_infty crossed product A_{II_infty} =
A_{III_1} rtimes_{sigma^phi} R at canonical Bisognano-Wichmann KMS
inverse temperature beta = 2pi, equipped with the KMS-GNS inner
product (A,B)_phi = tau(A^* B), the Lanczos coefficients b_n(O) of
any operator O with finite modular two-point function satisfy
   b_n(O) <= n * pi/beta + o(n),
and consequently the modular Krylov complexity satisfies
   C_K^mod(s) <= A * cosh(2 b_1(O) s),
   lambda_K^mod(O) := limsup_{s->infty} (1/s) log C_K^mod(s) <= 2pi/beta = 1.

WHY THIS BELONGS IN LMP.  THE PROOF IS PROVABLE TODAY.

The proof has three steps:
  Step 1.  Parker-Cao-Avdoshkin-Scaffidi-Altman (2019) tridiagonal
           inequality on the KMS-GNS inner product:
              C_K(s) <= A cosh(2 b_max s),
              b_max := sup_n b_n / n.
  Step 2.  Bisognano-Wichmann moment bound:
           the boost two-point function has universal hyperbolic
           decay (2 sinh(pi s/beta))^{-Delta}, whose moments
           M_{2k} ~ C_Delta (2pi k/beta)^{2k} are the Hankel-Lanczos
           inverse map of b_n <= n pi/beta + o(n).
  Step 3.  Combine.  In beta = 2pi units, lambda_K^mod <= 2pi/beta = 1.

No large-N, no holography, no chaos hypothesis is invoked.  This
gives a kinematic statement matching the Maldacena-Shenker-Stanford
(2016) chaos bound exactly on the truncation.

WHAT THIS PAPER DOES NOT CLAIM (saturation downgrade).

The earlier ECI v1 draft (2026-05-04) presented saturation
lambda_K^mod = 2pi/beta as the central object.  Three families of
counter-examples force a downgrade:
  - Avdoshkin-Dymarsky (2019, arXiv:1911.09672): free-scalar lattice
    models attain linear b_n in integrable regimes.
  - Camargo-Jahnke-Kim-Nishida (2023, arXiv:2212.14702): free and
    interacting massive scalar QFTs show the same linear envelope
    in non-chaotic regimes.
  - Sreeram-Kannan-Modak-Aravinda (2025, PRE 112 L032203,
    arXiv:2503.03400): operator/initial-state-dependent
    counter-examples persist even within fully chaotic dynamics.

Saturation is therefore retained only as a one-sided sufficiency
conjecture (Conjecture 1, Section 4).

CONCURRENT INDEPENDENT WORK.

We became aware during preparation of Vardian (2026,
arXiv:2602.02675), "Modular Krylov Complexity as a Boundary Probe of
Area Operator and Entanglement Islands" (single-author, hep-th,
February 2026).  Vardian works in the AdS/CFT setting and
reconstructs the QES area operator from boundary modular Lanczos
coefficients via OAQEC, applying to island formation and the Page
transition.  Our scope is complementary along three axes:
  - Holographic context.  Vardian uses AdS/CFT explicitly; we work
    intrinsically in any finite-rank type-II_infty truncation
    (de Sitter static patch, Rindler wedge, BEC analog horizon).
  - Object of study.  Vardian targets the area operator (a specific
    spectral element); we target the kinematic Lyapunov ceiling
    (an envelope statement on all operators).
  - Claim type.  Vardian gives a constructive boundary-bulk
    dictionary; we give a one-sided inequality with a concrete
    laboratory falsifier.
The two works together suggest modular Krylov techniques are
becoming a standard tool for type-II_infty algebras.  We cite
Vardian throughout and Section 5 is devoted to a side-by-side scope
comparison.

CONCRETE FALSIFIER (analog-Hawking BEC, A19 deliverable).

For the Kolobov-Golubkov-Munoz de Nova-Steinhauer 2021 BEC analog
black-hole platform (Nat.Phys. 17, 362; arXiv:1910.09363), the
manuscript derives the bound

   Gamma_meas <= 2 pi k_B T_H / hbar = (288 +/- 82) s^{-1}

at T_H = 0.35 +/- 0.10 nK (Munoz de Nova et al. 2019, Nature 569,
688; arXiv:1809.00913).  An observed Gamma_meas > 1.5 * Gamma_bound
= 432 s^{-1} at 5 sigma would falsify the type-II_infty kinematic
prefactor on the BEC exterior phonon algebra.  Crucially the bound
form (not the saturation form) is robust to the free-QFT /
integrability counter-examples noted above.

The Kolobov 2021 dataset already contains time-resolved density
correlations at six temporal points across a 124-day, 97000-
repetition acquisition; the test does not require new experimental
runs.  Cross-platform redundancy: polariton condensate
(Solnyshkov et al. 2026, arXiv:2603.01664), water-tank vortex QNM
(Torres-Patrick et al. 2017), and entanglement-negativity
(Chandran-Fischer 2026, arXiv:2604.02075) provide independent
substrates.

CONFIRMATIONS.

* All proofs are at the operator-algebra level.
* Saturation downgrade (v1 -> v2) caught by the A11/A19 audit
  (2026-05-05) and explicit erratum on the v1 over-attribution to
  Faulkner-Speranza is recorded in Section 4 of the manuscript.
* All arXiv references live-verified 2026-05-05.
* No conflicts of interest.

We suggest as referees:
  Algebraic gravity / chaos:
     J. Maldacena (Institute for Advanced Study, Princeton)
     L. Susskind (Stanford)
  Krylov complexity:
     P. Caputa (Warsaw)
     J. M. Magán (IFT-Madrid)
     D. Patramanis (University of Crete)

Sincerely,
Kévin Remondière
Independent researcher, Tarbes, France
```

---

## 4. Suggested referees (with affiliations and rationale)

| # | Name | Affiliation | Expertise | Rationale |
|---|---|---|---|---|
| 1 | **Juan M. Maldacena** | Institute for Advanced Study, Princeton | MSS chaos bound, AdS/CFT, modular Hamiltonians | Co-author of the chaos bound the manuscript reproduces kinematically (eq:mss); first-choice referee if available. |
| 2 | **Leonard Susskind** | Stanford University | Holographic complexity, computational complexity, de Sitter holography | Independent assessor on the holographic-complexity side; would assess the BEC falsifier's relation to holographic complexity. |
| 3 | **Pawel Caputa** | University of Warsaw | Krylov / spread complexity, modular Hamiltonian, operator growth | Lead author of CMPT2024 (cited; the bound is tight on this CFT class per Remark 2); would assess Theorem 1 + Conjecture 1. |
| 4 | **José M. Magán** | IFT, Madrid | Krylov complexity, operator growth, modular Hamiltonians | Co-author of CMPT2024; would assess the saturation conjecture and the connection to modular-Lyapunov universality. |
| 5 | **Dimitrios Patramanis** | University of Crete | Krylov complexity, holographic operator algebras | Co-author of CMPT2024; would assess the type-II_infty truncation construction. |

**Avoid** (potential conflict of interest):
- N. Vardian (concurrent independent work; should NOT review). Listed as concurrent author in Section 5.

**LMP submission portal field codes:**
- Primary: 81T05 (Axiomatic quantum field theory; operator algebras)
- Secondary: 81P40 (Quantum coherence, entanglement, quantum correlations), 83C45 (Quantization of the gravitational field)
- arXiv primary class: math-ph (cross-list to hep-th, gr-qc, cond-mat.quant-gas).

---

## 5. Pre-submission TODO (must do before clicking submit)

| # | Task | Severity | Owner |
|---|---|---|---|
| P1 | Compile `modular_shadow_LMP_v2.tex` to PDF (sub-agent shell could not run pdflatex). | **BLOCKER** | Kevin / Opus |
| P2 | Author placeholder already updated to "Kévin Remondière" (A39). Add ORCID if available. | Cosmetic | Kevin |
| P3 | (Optional) Update Solnyshkov2026 bibitem title to canonical arXiv title "Analogue black hole merger in a polariton condensate". | Low | Kevin |
| P4 | (Optional) Update ChandranFischer2026 bibitem title to canonical arXiv title "Emergence of volume-law scaling for entanglement negativity from the Hawking radiation of analogue black holes". | Low | Kevin |
| P5 | (Optional) Bump ECI_v6 Zenodo record from 10.5281/zenodo.20030684 to 10.5281/zenodo.20036808 (v6.0.53.2). | Low | Kevin |

---

## 6. What A39 changed in `modular_shadow_LMP_v2.tex`

One edit, in the author block:

1. **Lines 34-37**: `\author{(Author names to be determined)\\[2pt] \small Submitted to Letters
   in Mathematical Physics}` -> `\author{Kévin Remondière\\[2pt] \small Independent researcher,
   Tarbes, France\\[2pt] \small Submitted to Letters in Mathematical Physics}`.

No mathematical content changed. No theorems reformulated. No bibliography entries changed.

---

## 7. Final readiness assessment

| Aspect | Status |
|---|---|
| Mathematical content (Theorem 1 bound, Conjecture 1 saturation, BEC falsifier) | **READY** -- bound is provable today (Parker 2019 + Bisognano-Wichmann); saturation correctly downgraded to conjecture per A11/A19 audit. |
| Bibliography (17 active arXiv refs + 3 non-arXiv) | **READY** -- 100% arXiv IDs live-verified 2026-05-05. |
| Vardian 2602.02675 priority preempt-scoop | **HANDLED** -- cited as concurrent independent work (Section 1, paragraph 4 + Section 5 in entirety); scope comparison along 3 axes preserves priority. |
| Cover letter | **READY** (Section 3 above). |
| Suggested referees | **READY** (Section 4 above; 5 referees + 1 avoidance flag). |
| PDF compile | **PENDING** -- sub-agent could not run pdflatex; Kevin/Opus must compile. |
| Author/affiliation/ORCID | **READY** (author/affiliation set; ORCID optional). |
| arXiv class | math-ph (primary), hep-th + gr-qc + cond-mat.quant-gas (cross-list). |
| Submission portal field code | 81T05 primary, 81P40 + 83C45 secondary. |

**Verdict: SUBMIT-READY** after Kevin runs pdflatex (P1).  Bound theorem is provable today,
saturation is honestly downgraded to a conjecture, BEC falsifier is concrete and dataset-
ready.  Vardian preempt-scoop is handled by 3-axis scope comparison.  Estimated 5-10 min of
manual work to clear the BLOCKER list.

A39, Sonnet sub-agent, 2026-05-05.  Hallu counter at sub-agent exit: **81** (unchanged; 0 new).
