# Papers — crossed-cosmos / ECI collection

Landing page for the four preprints maintained in this repository.
All documents are CC BY 4.0 — Kevin Remondière (Independent Researcher, ORCID [0009-0008-2443-7166](https://orcid.org/0009-0008-2443-7166)).

Concept DOI (all versions): [10.5281/zenodo.19686398](https://doi.org/10.5281/zenodo.19686398)

---

## Quick index

| # | Paper | Track | Pages | Direct PDF | Zenodo DOI | Status |
|---|---|---|---:|---|---|---|
| 1 | **v5** — ECI phenomenological | `astro-ph.CO` | 14 | [eci.pdf](https://github.com/AIdevsmartdata/crossed-cosmos/releases/download/v5.0.2/eci.pdf) | [10.5281/zenodo.19696017](https://doi.org/10.5281/zenodo.19696017) | preprint · endorsement pending |
| 2 | **v6** — GSL on type-II crossed products | `hep-th` | 7 | [v6_jhep.pdf](https://github.com/AIdevsmartdata/crossed-cosmos/releases/download/v6.0.6/v6_jhep.pdf) | [10.5281/zenodo.19699006](https://doi.org/10.5281/zenodo.19699006) | preprint · endorsement pending |
| 3 | **v7-note** — Bogomolny–Keating fit | `math.SP` | 4 | [v7_note.pdf](https://github.com/AIdevsmartdata/crossed-cosmos/releases/download/v7-note-0.1/v7_note.pdf) | via concept DOI | preprint · endorsement pending |
| 4 | **Chimère Ω** — local-first LLM blueprint | `cs.LG` | 7 | [chimere_omega.pdf](https://github.com/AIdevsmartdata/crossed-cosmos/releases/download/chimere-omega-0.1/chimere_omega.pdf) | via concept DOI | blueprint · workshop track |

---

## Paper 1 — v5 phenomenological companion

**Title.** ECI — Entanglement, Complexity, Information: a framework paper threading six programs into one predictive canvas.
**Primary arXiv category.** `astro-ph.CO` (cross-list `gr-qc`, `hep-th`).
**Target journal.** European Physical Journal C (SCOAP3 OA).

**Abstract (TL;DR).**
A phenomenological architecture assembling six independently-established research programs (2022–2026) into a unified predictive canvas:
(i) type-II observer-dependent von Neumann algebras via the QRF crossed product;
(ii) DESI DR2 dynamical-dark-energy preference at 2.6–3.9σ, addressed by non-minimally coupled thawing quintessence ξ_χ R χ²/2;
(iii) H₀ tension reduced to ~2σ by Early Dark Energy;
(iv) Dark Dimension scenario c′ ≈ 0.05;
(v) Cryptographic Censorship as a working-conjecture bulk selection rule (with an explicit toy dS/FLRW dictionary);
(vi) persistent-homology diagnostics of primordial non-Gaussianity.

**Main quantitative result.**
A 4-chain MPI MCMC (19,700 samples, Gelman–Rubin R−1 = 0.036) on DESI DR2 BAO + Pantheon+ yields ξ_χ = 0.003 +0.065/−0.070 at 68% CL with χ₀ = M_P/10. Savage–Dickey BF₀₁ ≈ 1.

**Honesty statement.**
The posterior is only weakly informed by DR2+SN precision (half-width ratio posterior/prior ≈ 0.7). This is a consistency check, NOT a detection. Seven falsifiable predictions are listed for DESI DR3, Euclid DR1, CMB-S4, Simons Observatory, Eöt-Wash, optical clocks, KM3NeT.

**Tags.** `cosmology` · `dark-energy` · `DESI-DR2` · `Pantheon+` · `quintessence` · `non-minimal-coupling` · `MCMC` · `early-dark-energy` · `Hubble-tension` · `dark-dimension` · `swampland` · `persistent-homology`

**Build.**
```bash
cd paper && latexmk -pdf eci.tex
```

---

## Paper 2 — v6 formal companion

**Title.** From Faulkner–Speranza to a complexity-bounded generalised second law in type-II crossed-product algebras.
**Primary arXiv category.** `hep-th` (cross-list `gr-qc`, `math-ph`, `math.OA`).
**Target journal.** Journal of High Energy Physics (JHEP).

**Abstract (TL;DR).**
A differential upper bound on the rate of generalised entropy along the Connes–Tomita–Takesaki modular flow τ_R of a type-II crossed-product observer algebra A_R:

$$
\frac{dS_\text{gen}[R]}{d\tau_R} \le \kappa_R \cdot \mathcal{C}_k[\rho_R(\tau_R)] \cdot \Theta(\text{PH}_k[\delta n])
$$

with C_k the k-design complexity and PH_k the order-k persistent-homology Betti number. A tightened logistic envelope
$\kappa_R \mathcal{C}_k (1 - \mathcal{C}_k/\mathcal{C}_k^{\max}) \Theta$
is established in the scrambling regime (Prop. 1) with C_k^max ~ exp(S_R), dovetailing with the Fan (2022) logarithmic Krylov law at saturation. A dequantisation map bridges the type-II factor to classical persistent homology. The bound recovers Wall monotonicity and the Faulkner–Speranza modular form in the Θ→1 limit.

**Postulates labelled explicitly.**
- M1 — modular-complexity ansatz (Brown–Susskind-style)
- M2 — semiclassical LLN/CLT recovery without explicit bound
- M3 — chameleon-type activator profile for Θ
Conclusion reads "proposed inequality under stated assumptions". NOT a theorem for M1/M2/M3.

**PH_k covariance.**
Derived via Berkouk–Ginot (2018) derived isometry theorem on ℝ + Kashiwara–Schapira–Guillermou (2012) microlocal sheaves. Convolution distance lifted to the derived setting.

**Audit trail.**
- 18/18 pre-write rigour gates PASS
- Adversarial v1/v2/v3 full sweeps → SHIP → GO
- Peer-eco (Gemini Pro + Flash + Magistral): 2 MINOR / 1 MAJOR / 0 REJECT
- 4 companion numerical scripts under `derivations/` (dequantisation map, submultiplicativity Lemma 1, JT consistency, CLT convergence at N ∈ {12,16,20})

**Tags.** `quantum-gravity` · `generalised-second-law` · `von-Neumann-algebras` · `crossed-product` · `type-II` · `modular-flow` · `Connes-Tomita-Takesaki` · `persistent-homology` · `complexity` · `k-designs` · `Faulkner-Speranza` · `scrambling` · `derived-isometry` · `microlocal-sheaves`

**Build.**
```bash
cd paper/v6 && latexmk -pdf v6_jhep.tex
```

---

## Paper 3 — v7 short note

**Title.** Empirical Bogomolny–Keating 2-point correction on 10⁵ Odlyzko zeros, and a no-go for log-type saturation envelopes in complexity-bounded generalised second law inequalities.
**Primary arXiv category.** `math.SP` (cross-list `math.NT`, `hep-th`).
**Target venue.** technical note; possibly JSTAT or J. Number Theory depending on receipt.

**Abstract (TL;DR).**
Two independent small-scale results from a pre-registered testing pipeline for the v6 inequality:

*Result 1 (empirical).* On the first 10⁵ non-trivial Riemann zeros of Odlyzko's public table, the empirical pair correlation R_2^emp(x) deviates from the pure Montgomery–Dyson GUE prediction at χ² = 434.19 / 58 dof. Adding the Bogomolny–Keating (1996) arithmetic 2-point correction brings χ²/dof down to 4.17 at best-fit amplitude A = 0.41 and effective height L_eff = 7.44. Residual ν ≈ 1 oscillation is most plausibly an unfolding miscalibration — consistent with Odlyzko–Rudnick–Sarnak (1996) expectations.

*Result 2 (no-go).* In the Fan (2022) logarithmic Krylov scrambling regime, any saturation-envelope Φ(x) with Φ(1) ≠ 0 fails the boundary condition dS_gen/dτ_R → 0. A recent log-type envelope proposal Φ(x) ∝ log(1 + x/x*) is thereby excluded; the logistic Φ(x) = 1 − x of the v6.2 companion satisfies the boundary.

Both reported as technical notes — neither modifies the companion paper.

**Tags.** `Riemann-zeros` · `pair-correlation` · `Montgomery-Dyson-GUE` · `Bogomolny-Keating` · `Odlyzko-zeros` · `random-matrix-theory` · `Krylov-complexity` · `scrambling`

**Build.**
```bash
cd paper/v7_note && latexmk -pdf v7_note.tex
```

---

## Paper 4 — Chimère Ω blueprint

**Title.** Chimère Ω — a physico-cognitively-inspired local-first LLM runtime (blueprint / position paper).
**Primary arXiv category.** `cs.LG` (cross-list `cs.CL`).
**Target venue.** workshop track (NeurIPS workshop, ICML workshop, COLM). NOT a theorem paper.

**Abstract (TL;DR).**
Blueprint paper proposing an architecture for a local-first physico-cognitively-inspired LLM runtime, citing verified 2025–2026 SOTA on hybrid Mamba-2 / attention architectures (Qwen3-Next, Nemotron-H arXiv:2504.03624, Granite-4.0). Three falsifiable hypotheses:

- **H1** — Free-Energy under Censorship (FEC) objective with SAE + SIGReg auxiliary terms improves long-range reasoning over standard cross-entropy training.
- **H2** — RG-flow-inspired MoE coarse-graining yields scale-aware expert specialisation cheaper than uniform top-k gating.
- **H3** — Engram write policy gated by `(Surprise_B, V_verify, C_A3)` triple yields persistent context with bounded write rate, compatible with ≥ 90% of cloud-scale dense-model quality under 8 GB VRAM.

Persistent-homology language is **analogical** (the cosmological PH_k features of v6 inspire the architecture but do not appear as ML features in the runtime). Each hypothesis has an explicit falsifier. Production runtime is public at [AIdevsmartdata/chimere](https://github.com/AIdevsmartdata/chimere).

**Tags.** `large-language-models` · `local-inference` · `hybrid-architecture` · `Mamba-2` · `mixture-of-experts` · `RG-flow` · `concept-routing` · `long-context`

**Build.**
```bash
cd paper/chimere_omega && latexmk -pdf chimere_omega.tex
```

---

## Submission status tracker

| Milestone | v5 | v6 | v7 | Chimère Ω |
|---|:---:|:---:|:---:|:---:|
| Preprint drafted | done | done | done | done |
| Zenodo DOI | done | done | done | done |
| GitHub release | done | done | done | done |
| Endorsement request sent | 2026-04-24 | 2026-04-24 | 2026-04-24 | N/A |
| Endorsement received | — | — | — | N/A |
| arXiv submitted | — | — | — | workshop |
| arXiv ID | — | — | — | — |
| Journal submitted | — | — | — | — |
| Accepted | — | — | — | — |

## Scope statement (for peer reviewers)

- **None of these four papers is peer-reviewed.**
- **None is a derivation of a theorem.** v5 is a framework synthesis, v6 is a proposed inequality under stated postulates, v7 is a small technical note, Chimère Ω is a design blueprint.
- All **caveats and weakly-informed statements** are in the abstracts — not buried in an appendix.
- The **D18/D18b falsifier** (fσ_8 × Θ(PH_2)) was killed at DR3 + Euclid precision and is NOT claimed.
- All **three postulates M1/M2/M3** of v6 are labelled as POSTULATE / ANSATZ / CONJECTURAL inside the paper.
- **Cryptographic Censorship (A3)** of v5 is labelled as a working conjecture, not a theorem, with an explicit toy dS/FLRW dictionary making downstream uses traceable.

## How to cite

Concept DOI (stable across versions):
```bibtex
@misc{Remondiere2026ECI,
  author       = {Remondi\`ere, Kevin},
  title        = {ECI --- Entanglement, Complexity, Information: a framework paper},
  year         = {2026},
  doi          = {10.5281/zenodo.19686398},
  url          = {https://github.com/AIdevsmartdata/crossed-cosmos}
}
```

Per-version BibTeX entries are in each paper's `CITATION.cff` and in `eci.bib`.

## Contact

**Kevin Remondière** — Independent Researcher
Email: kevin.remondiere@gmail.com
ORCID: [0009-0008-2443-7166](https://orcid.org/0009-0008-2443-7166)
GitHub: [AIdevsmartdata/crossed-cosmos](https://github.com/AIdevsmartdata/crossed-cosmos)

Corrections, objections, and collaboration inquiries are welcome. I prioritize replies from colleagues working on:
- DESI DR2 NMC quintessence pipelines (v5)
- Type-II crossed-product algebraic QFT (v6)
- Persistent-homology cosmology (v5 A6, v6 PH_k covariance)
- Pre-registered tests of scrambling bounds (v7)
- Local-first hybrid LLM architectures (Chimère Ω)
