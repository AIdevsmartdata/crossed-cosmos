# Changelog

All notable changes to ECI are logged here. Format loosely follows
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/), semver.

Scope: v4.0 (first public release) through the current v5.0 pre-release head.
v1–v3 were private drafts and are not archived here.

---

## [5.0.0] — PLANNED (post-MCMC, pre-EPJ C submission)

Target: release cut at the moment the MCMC posterior on $\xi_\chi$ lands and
the paper is ready to upload to the EPJ C Editorial Manager.

### Planned
- **MCMC posterior integration.** Replace the §3.5 forecast-style bound
  $|\xi_\chi| \lesssim 10^{-3}$ with the measured posterior from the hi_class NMC
  production chains (Planck 2018 + ACT DR6 + DESI DR2 + PantheonPlus + DESY5),
  propagated into the §4 predictions table row 1b (DR3/LSST Y10 horizon).
- **Svjour3 submission format.** Promote `submission/epjc/eci_svjour3.tex` to the
  canonical manuscript, with one compile pass confirming 0 undefined references and
  the journal-provided class file bundle vendored under `submission/epjc/_vendor/`.
- **Editorial Manager upload.** Cover letter, referee suggestions, AI-use
  disclosure, author-status note, and the main PDF bundled as a single zip ready to
  drop into Springer EM.
- **Final Zenodo archive.** Cut `v5.0.0` git tag → Zenodo auto-archives →
  cross-link the new DOI in the EPJ C cover letter and on the repo README.
- **Adversarial review V12 (post-MCMC).** One full SHIP/FIX/BLOCK pass over the
  MCMC-integrated manuscript, logged in `paper/_adversarial_review_v5_0_0.md`.

### Scope guard
No new physics, no new derivation, no new reference after the v5.0 tag. If a v5.0
referee raises a point of substance, it goes into v5.1. v5.0 is the submission
snapshot; v5.1+ is the response-to-referees line.

---

## [4.8.x-dev] — 2026-04-20 → 2026-04-21 (unreleased, HEAD of the v5.0 pre-release line)

Not a tagged release. Umbrella for the MCMC-readiness work that precedes v5.0.

### Added
- `submission/epjc/` — vendored svjour3 bundle (`svjour3.cls`, `svepjc3.clo`,
  `svglov3.clo`, `spphys.bst`) plus the full ECI v4.7 manuscript ported to
  svjour3 format as `eci_svjour3.tex` (commits `29dbe2e`, `b6bc30c`).
- Cover letter compile fix: amsmath + amssymb packages added so `\lesssim`
  renders (`ae80501`).
- Deep citation audit of 14 load-bearing references, with one correction
  propagated into §3.5 (Chiba 1999 parenthetical PRL 82,1836 → PRD 60,083508,
  commits `23c2cf8`, `62e1c95`).
- `mcmc/nmc_patch/hi_class_nmc/` — fork of hi_class_public upstream 50f447c
  with the NMC $(\xi R \chi^2 / 2)$ term implemented as a Horndeski sub-case
  (commits `2eaf5cb`, `a0c23f3`, `4be6354`). Smoke-tested: NMC(ξ=0) reproduces
  `quintessence_monomial` on H(z) to machine precision.
- `mcmc/cobaya-nmc/` — Python Theory plugin wrapping vanilla `classy` with
  D14 $G_{\rm eff}$ / $\eta$ post-processing for a fast pre-screen MCMC
  (`8f5f179`).
- `mcmc-deploy/` — Dockerfile, `run_mcmc.sh`, YAML validator, and an AWS
  spot launch walkthrough for eu-west-3 (commits `07bdae4`, `d65c02f`).
- `mcmc-bench/` — CLASS optimized build + 100-eval local baseline, optimized
  YAML (Plik-lite + drag + explicit blocking), and `REPORT.md` with a 5-target
  projection and a Hetzner recommendation (commits `cade786`, `5ab132b`,
  `fe066f7`).
- Exotic-physics scan updates: §3.4 BSM caveats, §A3 Haferkamp saturation
  cite, Appendix A preamble with HolographicPseudoEnt2024, new bib entries
  MuonG2Final2025 / CMSWmass2024 / HolographicPseudoEnt2024 (commits `fae3f61`,
  `407f1c6`, `fae81bc`).

---

## [4.7.0] — 2026-04-20

Focus: unifying thesis, observer-frame hygiene, exotic-physics sweep, HAL exit.

### Added
- `section_1_5_thesis_B.tex` — Hypothesis B (observer-dependent cosmology,
  scoped to late-time quasi-dS $\Omega_\Lambda \gtrsim 0.7$) integrated via
  `\input` after §1 (commits `ebe9e83`, `50fa5a8`, `91439f9`, `d445ddc`).
- Observer-frame qualifiers propagated to §3.5 (solar-system-frame on the
  Cassini bound), §3.6 (causal-diamond regime on the EFT heuristic), and
  Appendix A (QRF-subregion link for the A3 working-conjecture status)
  (`e13327c`).
- `paper/exotic_physics_scan.md` — arXiv-verified 2024–2026 anomaly scan
  across 6 physics domains (`43613e7`).
- `paper/class_plan.md` — self-training notes on CLASS / hi_class plus the
  NMC patch implementation plan (`7849d52`).
- PRINCIPLES.md §11 — ground-truth discipline rule, plus a DECISIONS.md /
  GROUND_TRUTH.md sync (`d1df706`).

### Changed
- Abstract clause (v) updated to link A3 explicitly to the observer-dependent
  reading of A1 (Team B synthesis).
- Ma–Huang PRU citation upgraded from "effective existence" to "existence
  constructed from quantum one-way functions" at the CFT level; the
  cosmological transposition of A3 remains a working conjecture.

### Removed
- HAL deposit `hal-05598836` withdrawn gracefully — the CNRS moderator
  rejected on affiliation grounds (independent researcher, no laboratory
  backing). Zenodo remains the sole permanent archive (`75f5b32`).

### Verified
- V11-adversarial review via Magistral-medium — SHIP verdict, 3/3 PASS
  (`d683e4b`).

---

## [4.6.0] — 2026-04-20

Focus: §3.7 linear perturbation observables, §5 quarantine, internal RAG.

### Added
- §3.7 — closed-form NMC perturbation observables ($G_{\rm eff}$, $\eta$,
  $f\sigma_8$) from the D14 derivation, reporting null at Euclid / LSST Y10
  precision (commits `de832d8`, `2bfaf7e`). Honest null is the point: detection
  would require $\chi_0 \gtrsim 0.5\,M_P$ or a breach of the current PPN bound.
- §3.6 Res(ii) — D15 minimum chameleon screening profile
  ($\alpha = 0.095$, $\rho_c = 1.3 \times 10^{-8}$ g/cm³) cited as a
  comparison to Khoury–Weltman 2004, not as a derivation
  (commits `2519aa5`, `36319e5`).
- `KhouryWeltman2004` and `Boisseau2000` bib entries (`ef78f34`, `a4a99df`).
- `paper/_internal_rag/INDEX.md`, `GROUND_TRUTH.md`, `DECISIONS.md`,
  `PRINCIPLES.md` — aggregate derivation results, reviews, open caveats, and
  rejected attempts into a single narrative layer for downstream agents
  (commits `0aca46c`, `5c65ae0`).

### Changed
- §5 (A3 toy dictionary) quarantined to Appendix A "Speculative" with an
  explicit italic preamble stating the appendix is not on the critical
  predictive path (`775c184`). Peer-v2 6/6 identified §5 as the single
  weakest element; honest response was to quarantine rather than defend.
- Unicode $\Lambda \to \verb|\Lambda|$ in §3.7 caption (LaTeX compile
  hygiene) (`ef78f34`).

### Fixed
- `section_3_7.tex` — replaced missing `\ref{sec:action}` with a hard §2
  reference; compile clean with 0 undefined references (`6b93377`).

### Verified
- V10-adv via Magistral-medium — SHIP (3 FULL, 1 PARTIAL) (`4f8c8cb`).
- peer-v3 — 1min.ai 3-model eco peer review (qwen3-max + 2 credit-blocked)
  (`a274407`).

---

## [4.5.0] — 2026-04-20

Focus: A3 toy-dictionary attempt, D13 numerical B(Ω_Λ), peer-v2 triangulation.

### Added
- §5 — explicit conjectural CFT→cosmology dictionary naming one testable
  consequence (bulk-geometry exclusion for super-Gibbons–Hawking coarse-grained
  horizon entropy at reheating) (commits `9a03f30`, `d529dce`). A3 axiom kept
  as "working conjecture" status; §5 body rewritten to depend on the
  dictionary, not on A3 itself.
- D13 — full numerical B(Ω_Λ) integration, $B_{\rm num} \in \{9.00, 9.18,
  9.05, 8.11\}$ at $\Omega_\Lambda \in \{0.5, 0.6, 0.7, 0.8\}$, replacing the
  heuristic $(8/\sqrt{3})A$ coefficient (`9912725`).
- §3.5 Caveat 2 + table `tab:B_of_OmegaL` — D13 numerics propagated;
  prediction row 1b rescaled to $\Delta w_a^{\rm ECI} \approx 1.1 \times 10^{-2}$
  (`d8ff646`).
- `paper/_v4.5_A3_decision.md` — decision note for Option Y (toy dictionary)
  over Option X (plain demotion) (`40d37ca`).

### Changed
- Abstract wording for A3: "selection rule" → "working conjecture with §5
  toy dictionary" per V8-adv minor flag (`752408b`).

### Verified
- peer-v2: 3-model frontier pre-review (GPT-5.4 + Gemini 3.1 Pro + Grok 4),
  unanimous MAJOR REVISIONS on §5 (`5ea4bec`).
- V8-adv — SHIP with 1 MINOR (abstract wording) (`4db2c14`).

---

## [4.4.0] — 2026-04-20

Focus: audit artefacts, D11 no-ghost proof, D12 exponential attractor.

### Added
- D11 — no-ghost proof from the kinetic 2×2 matrix, with a Faraoni
  cross-check and explicit numerical margins (`bd13077`).
- D12 — exponential-potential attractor analysis,
  $\alpha \leq \sqrt{2}$ viability band (`40404ec`).
- `paper/equation_map.md` — equation ↔ script cross-reference (`82893f0`).
- `paper/convention_audit.md` — Faraoni metric / NMC sign / M_P unit audit
  (`e9e1438`).
- `paper/literature_map.md` — 29 axiom / phenomenology claims against
  primary references (`d285054`).

### Verified
- V7-adv — SHIP (0 BLOCK, 0 MAJOR, 3 MINOR) (`c857c33`).
- V6-mistral cross-model review — 3/4 FULL-PARTIAL, 1 functional-form
  divergence on D7 PPN (Mistral's linear-in-ξ derivation is known-incomplete;
  canonical Chiba/Faraoni is quadratic) (`4c8ccd1`).
- peer-v1 AI peer pre-review (Claude + Gemini + Magistral triangulation)
  (`16243a6`).

---

## [4.3.0] — 2026-04-20

Focus: convention lock, axiom prose tightening, bib discipline.

### Added
- §2 Conventions subsection — Faraoni mostly-plus signature, reduced Planck
  $M_P = 2.435 \times 10^{18}$ GeV, $\xi > 0$ attractive (`f62ea1d`).
- A4 amendment — $\chi$ is a 4D effective field; decoupling choice flagged
  (`e8b8767`).
- A5 species-scale equation carried in-text (`5d0152c`).
- A6 Matsubara–Yip Euler-characteristic equation carried in-text
  (`d95c52b`).
- No-ghost prose derivation from the kinetic matrix (`aa46ed3`).
- $\alpha \leq \sqrt{2}$ attractor prose line (`4675b05`).
- Bib: 6 entries + DOI upgrades for Calabrese2025 / Calles2025 (`f0d3f2c`);
  Halliwell1987 (`28746a3`).

### Fixed
- 4 orphan bib citations (AAL2023, DESY5, DESIForecast, Matsubara2003) now
  actually cited in-text (`b7510da`).
- 3 stale `% TODO-BIB:` markers removed, including a trailing one in
  `section_3_6` comment block (`4633ce8`).

### Verified
- V5-adv — FIX (4 orphaned bib entries, no physics issues), then rerun SHIP
  (commits `0297eab`, `d921099`).

---

## [4.2.1] — 2026-04-20

Focus: §3.5 and §3.6 rewrite with real DR2+DESY5 covariance and the
species-scale cutoff.

### Added
- D10 — DESI DR2 $(w_0, w_a)$ covariance correction to D7, reconstructed via
  the pivot-minimisation identity ($\sigma(w_0) = 0.057$, $\sigma(w_a) = 0.215$,
  $\rho = -0.89$) (`9bf0bdf`).
- D8 — Swampland × NMC cross-constraint derivation + (c', ξ) 2D plot; bulk
  finding is that the cross-constraint tightens $|\xi|$ by ≈250× and that the
  A4 $\chi$ cannot be the A5 bulk mode (commits `5af5e10`, `22412fa`,
  `26725f3`).
- D9 — numerical NMC Klein–Gordon integration validating the D7 analytic B
  coefficient (`44be544`).
- D7 novelty audit — (a) re-derivation of prior work (Chiba 1999, Wolf 2025);
  (b) novel closed form for the NMC Scherrer–Sen tail (`9ac5aba`).
- §3.6 — Swampland × NMC cross-constraint subsection (`f5cdf47`).
- `paper/_rag/` — primary-source cache for Dark Dimension, Swampland, NMC-PPN,
  DESI DR2 (`926a6e5`).
- Bib: Chiba1999 (gr-qc/9903094) and DamourEspositoFarese1993 (PRL 70, 2220)
  cited explicitly in D7 (`4667039`).

### Changed
- §3.5 Caveat 4 rewritten with the real DR2+DESY5 covariance; Mahalanobis
  distances 3.29σ (ECI), 3.33σ (Scherrer–Sen), 4.36σ (ΛCDM) (`1d74e17`).
- §3.6 primary cutoff value $c' = 1/6$ (species scale) adopted over
  $c' = 0.05$ (de-Sitter slope), which is retained only as a parenthetical
  (`4c31c76`).
- Prediction row 1b updated for DR2+DESY5 $\sigma(w_a) = 0.215$ (`d3cf8df`).

### Verified
- V1 verification of D8 Swampland × NMC cross-constraint (`5c3be27`).
- V2 verification of D10 DESI DR2 covariance + ECI Mahalanobis distances
  (`3623ae2`).
- V3-adv of §3.5 + §3.6 — SHIP verdict (`a20af13`).
- Bib audit of 4 RAG-flagged attribution issues (no fixes needed) (`64939d5`).

---

## [4.2.0] — 2026-04-20

Focus: §3.6 Swampland × NMC, D8/D9/D10 bulk derivations.

Summary tag for the D8-through-D10 work listed under v4.2.1. v4.2.0 was the
first cut of §3.6; v4.2.1 was the audit-cleanup pass. Blog cross-reference
to `ca-se-passe-la-haut` (2025-10 … 2026-04) added (`aa3ce2d`).

---

## [4.1.0] — 2026-04-20

Focus: §3.5 PPN/NMC constraints on $\xi_\chi$, D7 derivation.

### Added
- §3.5 — PPN/NMC constraints on $\xi_\chi$ via the D7 derivation
  (DEF 1993 + Scherrer–Sen + NMC closed form), integrated via `\input` with
  label `sec:xi_constraints` (commits `5dc87f4`, `ec95eef`).
- D7 — $\gamma - 1$ derivation using Damour–Esposito-Farèse 1993, NMC
  Scherrer–Sen extension, and a $(w_0, w_a)$ plot (`ab8627c`).
- §4 predictions table row 1b — DR3 / LSST Y10 is flagged as the true
  ECI-vs-wCDM horizon for $w_a$ (`384df32`).
- D7 night-session report — verdict, numerical outcome, follow-ups
  (`644c6eb`).
- Track C automated bib audit via Crossref + arXiv APIs (`3594a1c`).

### Removed
- `hal/web-form-fields.md` deleted — the HAL deposit was complete at
  `hal-05598836`, the operational note no longer applied (`1e4e91a`).

---

## [4.0.5] — 2026-04-20

Focus: HAL deposit scaffolding, SWORD workarounds, web-deposit fallback.

### Added
- HAL SWORD deposit scaffold — TEI metadata + credential-safe curl wrapper
  (`b362852`).
- HAL deposit ID `hal-05598836` (CNRS timestamp) embedded in the eci.tex
  title-page thanks line (`79f826a`).

### Fixed
- HAL SWORD Content-Disposition filename corrected to TEI (HAL expects `.xml`
  even for zip bundles) (`3a5e182`).
- `eci.tei.xml` renamed to `eci.xml` (HAL's SWORD regex rejects multiple
  dots in filenames) (`c91d1ec`).
- `X-Allow-Completion` header removed (HAL misinterprets it as a
  test-collection lookup) (`e9e1438`-era precursor, `e9a6b68`).
- Documented all web-form fields as a copy-paste fallback after SWORD
  returned "Test collection HAL not found" (known HAL bug on fresh
  accounts) (`523901c`).

Note: the HAL deposit was later withdrawn in v4.7.0 on affiliation grounds;
Zenodo remained the sole permanent archive.

---

## [4.0.4] — 2026-04-20

Focus: v4.0.x scaffold completion — derivations, numerics, MCMC stub,
EPJ C dossier.

### Added
- D1–D4 and D6 derivations + N1–N4 numerical sanity checks, recovered from
  interrupted agents (`0ed63bd`).
- D5 derivation + N5 numerical check + MCMC scaffold + EPJ C submission
  dossier (cover letter, suggested referees) (`3d01776`).

---

## [4.0.3] — 2026-04-20

### Added
- Zenodo DOI `10.5281/zenodo.19686399` embedded in `README.md`,
  `CITATION.cff`, and `eci.tex` (`9b6cadc`).

---

## [4.0.2] — 2026-04-20

Retag of v4.0.1 with no content delta; preserved for Zenodo archival
continuity.

---

## [4.0.1] — 2026-04-20

Focus: v4 self-audit before first peer review.

### Added
- `derivations/`, `numerics/`, `docs/` scaffolding.
- `AI_USE.md` — transparency disclosure of AI-assisted tool usage.
- `docs/REVIEW_NOTES.md` — self-audit response log.

### Changed
- **A3 downgraded from axiom to "working conjecture"** in the manuscript,
  with explicit caveat that Cryptographic Censorship is proven only in
  AdS/CFT and that its cosmological extension is not established.
- **Prediction (1) flagged as non-discriminating** vs wCDM inside the quoted
  $(w_0, w_a)$ band pending the $w_a(w_0; \xi_\chi)$ analytic computation.
- JEPA / modular-flow structural analogy postponed to a companion paper
  (out of scope for the framework paper).
- Editorial target: **EPJ C** (SCOAP3 OA, IF 4.3) primary; *Foundations of
  Physics* backup.
- Explicit Faraoni sign-convention note ($\xi = 1/6$ conformal) added next
  to every NMC equation.

### Fixed (bibliography, carried from the v4.0 private scaffold)
- arXiv:2507.03090 re-attributed to Bedroya–Obied–Vafa–Wu,
  *Evolving Dark Sector and the Dark Dimension Scenario* (v3 had mis-attributed
  to Anchordoqui–Antoniadis–Lüst).
- arXiv:2511.16606 re-attributed to Wang & Piao,
  *Dark energy after pre-recombination EDE in light of DESI DR2, ACT, SPT*
  (v3 had "Jiang–Piao").
- arXiv:2604.09148 removed — it is Rossi-Yu-Michaux on neutrino cosmic web,
  unrelated to Shiu–Cole. Correct Shiu–Cole refs: arXiv:1812.06960 (JHEP 03
  (2019) 054) and arXiv:1712.08159 (JCAP 03 (2018) 025).
- arXiv:2512.09852 de-listed — authors were Calles et al., not "Shiu–Cole".

### Updated (experimental bounds)
- Ġ/G bound updated from Williams–Turyshev–Boggs 2004 to
  Biskupek–Müller–Torre, *Universe* 7(2), 34 (2021), DOI
  10.3390/universe7020034: Ġ/G = (−5.0 ± 9.6) × 10⁻¹⁵ yr⁻¹ (≈ 2 orders of
  magnitude tighter).
- N_eff bound updated from Planck 2018 to ACT DR6 (Calabrese et al.),
  JCAP 11 (2025) 063, arXiv:2503.14454: N_eff = 2.86 ± 0.13. Critical for
  Dark Dimension viability.

---

## [3.x] — private drafts

Not archived publicly. v4 is the first public release.
