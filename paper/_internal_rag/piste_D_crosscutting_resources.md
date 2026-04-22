# Piste D — Cross-Cutting Resource Plan (RAG / Compute / Knowledge)
# Produced 2026-04-22 · Respects PRINCIPLES rules 1, 12, V6-1, V6-4
# Checked against FAILED.md F-1 through F-19: no closed avenue re-opened here.

---

## Preamble

No piste A, B, or C plan files have landed in `paper/_internal_rag/` as of
2026-04-22. This plan is therefore written against the consolidated picture in
`v8_consolidated_landscape_synthesis.md` (Parts B–E) and the GROUND_TRUTH.md
v4.6 / v6 companion section. It will require a delta when A/B/C plans arrive.

Piste mapping (from landscape synthesis):
- **Piste A** = v5 revision + Fisher forecast track (NMC quintessence, DESI DR3).
- **Piste B** = v6 → v7 theorem-development track (Liu 2026 QFC connection,
  modular-complexity, type-II algebra).
- **Piste C** = Submission / dissemination logistics (arXiv endorsement, HAL,
  journal ports).

---

## SECTION 1 — RAG (Knowledge Cache)

### 1.1 Current coverage (verified 2026-04-22)

43 `.txt` extracts in `paper/_rag/`. **Piste A** (NMC/DESI): 21 entries, all
core papers present (Chiba1999, DESIDR2, Wolf2025, Ye2025, PanYe2026,
ScherrerSen2008, PoulinSmith2026, Yip2024, Montero2022, AAL2023, AAL2025,
BEFPS2000, DEF1996PRD, Faraoni2004, Poulin2019, OOSV2018, OoguriVafa2007,
BedroyaVafa2019, Bedroya2025DS, PettorinoBaccigalupi2008, Oliveira2025NMC).
**Piste B** (v6/v7 algebra): 18 entries covering CLPW2023, DEHK2025a/b,
FaulknerSperanza2024, KFLS2024, Wall2011, Fan2022, BrownSusskind2018,
Caputa2024, Bianconi2025, BRSS2019, ConnesRovelli1994, SchusterHaferkampHuang2025,
Pedraza2022Threads, Carrasco2023, ElingGuedensJacobson2006, FrameCovariance2025,
TiettoVerlinde2025. **Piste C**: CryptoCensorship.

**Known bad entries (correct before citing):**
- `Faraoni2000.txt` — wrong paper (Bento-Lemos gr-qc/0008028). Correct target:
  gr-qc/0006091 (Faraoni "Inflation and quintessence with nonminimal coupling").
- `Matsubara2003` — astro-ph/0305472 is Rossa-Dettmar. Correct: astro-ph/0006269.
- `DEF1993PRL` — no arXiv; paywalled PRL 70(1993)2220. Use DEF1996PRD as proxy.

### 1.2 Gap analysis — papers missing from RAG that matter for A/B/C

Priority is **impact × availability** (all papers below are freely downloadable).

#### PRIORITY 1 — BLOCKING for Piste B (v7 theorem work)

**Liu 2026 — arXiv:2601.07915**
- Title: "Quantum focusing conjecture on perturbative quantum gravity"
- Why critical: v6 landscape synthesis explicitly identifies the Liu 2026 QFC
  proof on horizon subalgebras as the main parallel result to v6's
  complexity-bounded GSL. The v7 follow-up (connecting v6 Pinsker step to Liu
  QFC) cannot proceed without this paper cached at section level.
- Action: fetch full PDF, extract §§2-4 (QFC setup and proof), add as
  `Liu2026.txt` (~80 kB expected).
- URL: https://arxiv.org/abs/2601.07915
- Unblocks: **Piste B** (v7 connection note).
- Estimated extract size: ~60-90 kB txt.

**Hollands-Longo 2025 — arXiv:2503.04651**
- Title: "A new proof of the quantum null energy condition"
- Why critical: landscape synthesis lists this as "REINFORCES" v6 via simplified
  QNEC proof. The strengthened-QNEC step in v6 §3 cites this; no extract
  exists despite KFLS2024 being cached.
- Action: fetch and extract as `HollandsLongo2025.txt` (~50 kB).
- URL: https://arxiv.org/abs/2503.04651
- Unblocks: **Piste B** (v6 §3 strengthening citation, v7 QNEC step).
- Estimated extract size: ~40-60 kB txt.

#### PRIORITY 2 — BLOCKING for Piste A (observational caveat / M3 update)

**Barrow et al. 2025 — arXiv:2504.12205**
- Why critical: landscape synthesis lists "Barrow 2504.12205" as relevant to
  the M3 observational caveat in v6. Needed to confirm whether Barrow 2025
  introduces a constraint on the chameleon/α sector that affects M3.
- Action: fetch abstract + §§2-3, add as `Barrow2025.txt` (~40 kB).
- URL: https://arxiv.org/abs/2504.12205
- Unblocks: **Piste A** (M3 caveat update) + **Piste B** (v6 CONJECTURAL label
  on M3 remains honest).
- Estimated extract size: ~30-50 kB txt.

**Sanchez-Lopez-Karam-Hazra 2025 — arXiv:2510.14941**
- Title: "Updated thawing quintessence constraints" (per landscape synthesis).
- Why critical: listed as ALIGNS with v5 in Part C; a text extract enables
  quoting their σ(ξ_χ) result verbatim (rule 1: no paraphrase from memory).
- Action: fetch §§3-4, add as `SanchezLopez2025.txt` (~50 kB).
- URL: https://arxiv.org/abs/2510.14941
- Unblocks: **Piste A** (v5 §3.5 Wolf-consolidated revision, comparison table).
- Estimated extract size: ~40-60 kB txt.

#### PRIORITY 3 — USEFUL for Piste A (Fisher / DR3 forecasting)

**DESI DR3 forecast / science requirements papers** (2025-2026)
- The Fisher forecast (V8-fisher-forecast-DR3-LSST, status RUN-CONFIRMS-STRUCTURAL-NULL)
  used internal specifications. For publication, the BAO covariance should be
  cited from DESI Science Requirements papers.
- Candidate: DESI Collaboration forecast paper for DR3 (no single canonical arXiv
  at time of writing; watch 2601.* submissions in 2026-H1).
- Action: monitor arXiv listings; add when available.
- Unblocks: **Piste A** (rigorous DR3 forecast citation).

**KFLS2024 — arXiv:2406.01669 (Kudler-Flam-Leutheusser-Satishchandran)**
- Already cached as `KFLS2024.txt` (text-only, no PDF). However, the INDEX.md
  entry for KFLS2024 is missing — it was added in the v6 audit but not indexed.
  Action: add an INDEX.md entry and verify §§3-4 cover the FLRW type-II
  construction (key for Piste B v6-D FLRW extension).
- Unblocks: **Piste B** (v6-D FLRW extension, open question (iv) in v6.0.4 §7).

**CCM spectral triples — arXiv:2511.22755**
- Already tested in V7-Test5 (REGISTRY_FALSIFIERS V7-Test5, status
  RUN-STRUCTURED-UNKNOWN). WebFetch of full PDF was performed and confirmed:
  the paper contains only 1-point predictions, no 2-point formula. The paper
  is therefore **NOT needed in RAG** for any piste: F-9 definitively closed
  the ZSA/CCM line, and FAILED.md F-17 closes the heat-kernel Λ branch.
  Do NOT add to RAG; adding it would invite re-exploration of a closed avenue.

### 1.3 RAG additions — prioritised fetch list

| # | Shortkey | arXiv | kB est. | Piste | Urgency |
|---|---|---|---|---|---|
| 1 | Liu2026 | 2601.07915 | ~80 | B | NOW (blocks v7) |
| 2 | HollandsLongo2025 | 2503.04651 | ~50 | B | NOW (blocks v6 §3 cite) |
| 3 | Barrow2025 | 2504.12205 | ~40 | A+B | Week 1 |
| 4 | SanchezLopez2025 | 2510.14941 | ~50 | A | Week 1 |
| 5 | KFLS2024 INDEX entry | (cached) | — | B | Week 1 (5 min) |
| 6 | Faraoni2000 corrected | gr-qc/0006091 | ~30 | A | Week 1 |
| 7 | Matsubara2003 corrected | astro-ph/0006269 | ~30 | A | Before submission |
| 8 | Kirklin2025 | (TBD — search arXiv) | ~60 | B | Week 2 |
| 9 | DESI DR3 forecast | 2026-H1 arXiv | ~80 | A | Watch/monitor |

---

## SECTION 2 — Compute Budget

### 2.1 Workstation specification

i5-14600KF (6P+8E cores, 20 threads) + RTX 5060 Ti 16GB VRAM + 32GB DDR5.
Reference baselines from this repo:
- V8-Cassini ODE (scipy): <5 min, local.
- V8-Fisher-DR3-LSST (numpy Fisher): <30 min, local.
- V6 symbolic (sympy CLT check N∈{12,16,20}): <10 min, local.

### 2.2 Local-only tasks (workstation is sufficient)

All of the following fit comfortably on the workstation:

| Task | Tool | Time est. | Piste |
|---|---|---|---|
| χ(z) ODE | scipy | <5 min | A |
| Fisher (5-param, nuisance marg) | numpy | <30 min | A |
| Fisher (7-param extended) | numpy | <2 hr | A |
| Sympy algebraic checks v6 §3-4 | sympy | <30 min | B |
| GRF PH_k 2D mock (256²) | gudhi/ripser | <1 hr | A |
| GRF PH_k 3D field (64³) | gudhi | ~4 hr | A |
| NMC background ξ_χ scan (20 pts) | hi_class Python | ~2 hr | A |
| MCMC plugin route, 2-param | Cobaya | ~12 hr | A |
| MCMC plugin route, 5-param | Cobaya | ~48 hr | A |
| svjour3 port + bib-audit | latexmk | ~4 hr | C |

**MCMC note (48 hr):** run with `taskset -c 0-7` (P-cores only) +
`PYTHONUNBUFFERED=1` + nohup to avoid thermal throttle. Plugin route
(not C-patch) is correct per GROUND_TRUTH.md Part E.3.

### 2.3 Cloud-required tasks

The following tasks exceed workstation capacity OR require wall-clock time
incompatible with a solo researcher using the machine interactively:

| Task | Why cloud | Spec needed | €/hr est.* | Hours | Total € est. |
|---|---|---|---|---|---|
| Full 4-chain MPI MCMC, 6-param (ξ_χ, α, f_EDE, z_c, w₀, wₐ) vs DR3+CMB | Memory: needs CLASS with NMC C-patch; 4-chain MPI needs ≥32 cores | H100 SXM 80GB × 1 node, 32 cores | ~2.5 | ~72 | ~180 |
| hi_class C-patch NMC benchmarking (compile + parameter sweep) | C build + sweep; CLASS compile slow on i5 | A100 40GB × 1, 16 cores | ~1.5 | ~20 | ~30 |
| Drop-Upcycling / LoRA fine-tune for v7 (if chimere-omega extension) | VRAM: base model + adapter > 16GB at fp16 | A100 80GB × 1 | ~2.0 | ~10 | ~20 |

*Vast.ai spot pricing for H100/A100 fluctuates; as of 2026-04 public pricing
page (https://vast.ai/pricing) spot H100 SXM runs approximately $2-3/hr and
A100 40GB approximately $1-2/hr on competitive bids. Do not treat these
figures as guaranteed — verify at bid time.

**Scientific yield per €:**

1. **hi_class C-patch benchmarking** (~€30): highest yield. Enables the one
   missing ingredient that blocks PRD/JCAP submission (GROUND_TRUTH Part E.3).
   The C-patch itself is multi-week authorship work; the cloud cost is only for
   running the completed patch at scale.
2. **Full MPI MCMC** (~€180): required for PRD/JCAP; not required for EPJ C
   framework paper. Given GROUND_TRUTH editorial target = EPJ C, this is
   medium-priority until the journal tier is escalated.
3. **LoRA fine-tune** (~€20): only relevant if chimere-omega expands; currently
   out-of-scope for v5/v6.

**Recommendation:** defer cloud spend until hi_class C-patch (weeks of authorship)
is written. The workstation handles all currently executable tasks.

### 2.4 What the workstation already proved it handles

The V8 Cassini and Fisher agents both completed locally in <30 min. This
confirms the workstation is adequate for:
- Any single-ODE integration with scipy.
- Any 5-7 parameter Fisher matrix (numpy, no Boltzmann code).
- Any sympy algebraic check up to ~100-term polynomials.
- Any GRF PH_k on grids up to 3D 64³.

---

## SECTION 3 — Knowledge Gaps

### 3.1 Piste A — NMC quintessence / DESI DR3 Fisher track

**Gap A1: hi_class Cython internals and NMC background EOM modification**
- What: CLASS computes H(z), δ_m(z) via Boltzmann code; NMC adds an
  effective G_eff/G_N(z) and a source term in the scalar EOM. The hi_class
  module (arXiv:1307.1724, Zumalacárregui et al.) implements Horndeski
  functions; adapting it for the specific ξ_χ R χ²/2 coupling requires
  modifying the α_M, α_B, α_K functions.
- Recommended reading:
  (a) Zumalacárregui et al. 2017, "hi_CLASS: Horndeski in the Cosmic Linear
      Anisotropy Solving System", JCAP 2017(08):019,
      https://arxiv.org/abs/1605.06349 — §§2-3 (Horndeski functions).
  (b) Bellini & Sawicki 2014, "Maximal freedom at minimum cost: linear
      large-scale structure in general modifications of gravity",
      https://arxiv.org/abs/1404.3713 — α-function parameterisation.
  (c) Faraoni 2004 (already cached: `Faraoni2004.txt`) — NMC EOM as reference.
- Time to fill: ~2 days (read + implement α_M(z) for ξ_χ).

**Gap A2: Cobaya likelihood interfacing for the plugin route**
- What: the MCMC "plugin route" means Cobaya calls a Python likelihood, not
  CLASS directly. The author has the hi_class_nmc patch in `mcmc/nmc_patch/`
  but the Cobaya likelihood interface for it may need validation against
  DESI DR2 covariance matrices.
- Recommended reading:
  (a) Cobaya documentation and paper: Torrado & Lewis 2021, JCAP 2021(05):057,
      https://arxiv.org/abs/2005.05290 — §§2-4 (likelihood API).
  (b) Lewis & Bridle 2002 (CosmoMC precursor): understanding the Markov chain
      diagnostics (Gelman-Rubin R-1 < 0.01), https://arxiv.org/abs/astro-ph/0205436.
  (c) DESI DR2 2503.14738 (already cached: `DESIDR2.txt`) — covariance matrix
      format for BAO likelihood plugin.
- Time to fill: ~1 day (Cobaya API is well-documented; the interface is the
  bottleneck, not the theory).

**Gap A3: NMC post-Wolf 2025 landscape — Sanchez-Lopez et al.**
- What: the v5 Wolf-consolidated revision (Part E item 2 in landscape synthesis)
  needs to quote updated σ(ξ_χ) from Sanchez-Lopez 2025. Currently only the
  abstract is known from training; RAG cache missing (see §1.2 item 4).
- Recommended reading:
  (a) Sanchez-Lopez et al. 2025, arXiv:2510.14941 (fetch for RAG, Priority 4).
  (b) Pan-Ye 2026 (already cached: `PanYe2026.txt`) — cross-comparison.
- Time to fill: ~2 hr (read §§3-4 of the paper once cached).

### 3.2 Piste B — v6 formal track / v7 theorem development

**Gap B1: Liu 2026 QFC proof technique on horizon subalgebras**
- What: the v7 follow-up paper (landscape synthesis Part B, medium cost) is
  "explicit connection between v6 Pinsker step and Liu 2026 QFC proof". This
  requires understanding Liu's proof method (half-sided modular inclusion,
  Borchers-Wiesbrock technique, or Haag-Kastler nets on horizon algebras).
  The author must know enough to identify which step in Liu corresponds to
  the Pinsker inequality step in v6.
- Recommended reading:
  (a) Liu et al. 2026, arXiv:2601.07915 (fetch for RAG, Priority 1) — full paper.
  (b) Leutheusser-Liu 2022 "Causal connectability between quantum systems and
      the black hole interior", arXiv:2110.05497 — precursor, half-sided modular
      inclusion in black hole context, https://arxiv.org/abs/2110.05497.
  (c) Haag 1992, "Local Quantum Physics" (Springer, 2nd ed. 1996) — Chapter V
      (Tomita-Takesaki modular theory) and Chapter VI (nets of algebras). No
      arXiv; find via library or Springer link. This is the algebraic QFT primer
      needed if modular inclusion is not already mastered.
- Time to fill: ~3-5 days if modular inclusion is new; ~1 day if familiar.

**Gap B2: Half-sided modular inclusion details beyond Faulkner-Speranza 2020**
- What: the connection to Liu 2026 requires understanding the Borchers-Wiesbrock
  half-sided modular inclusion theorem, which is the structural tool that Liu
  uses for the QFC subalgebra statement. The v6 paper uses Tomita-Takesaki
  flow but may not have the half-sided inclusion statement explicit.
- Recommended reading:
  (a) Borchers 2000, "On revolutionizing quantum field theory with Tomita's
      modular theory", J. Math. Phys. 41(6):3604,
      https://doi.org/10.1063/1.533323 — §§3-4 (half-sided inclusion theorem).
  (b) Wiesbrock 1993, "Half-sided modular inclusions of von Neumann algebras",
      Commun. Math. Phys. 157:83, https://doi.org/10.1007/BF02098018.
  (c) Hollands-Longo 2025, arXiv:2503.04651 (fetch for RAG, Priority 2) —
      simplified QNEC proof that may use the same technique in accessible form.
- Time to fill: ~2-3 days (modular inclusion is a precise mathematical
  statement; Wiesbrock 1993 is 15 pages).

**Gap B3: Algebraic QFT primer (only if not already mastered)**
- What: if the author has not worked through Tomita-Takesaki modular theory
  at the von Neumann algebra level (not just the physicist's summary), v7
  will require it.
- Recommended reading:
  (a) Haag 1992 "Local Quantum Physics" (Springer, 2nd ed.) — Chapters V-VI.
      No arXiv; access via institutional library.
  (b) Witten 2018, "APS Medal Lecture: Entanglement, quantum matter, and
      topology", arXiv:1803.04993 — accessible physicist entry point to
      algebraic QFT and type-II algebras.
      https://arxiv.org/abs/1803.04993
  (c) CLPW 2023 (already cached) — de Sitter type-II_1 construction with
      explicit modular-flow discussion; treat as working example.
- Time to fill: ~1 week if starting from scratch; ~0 if already familiar.

### 3.3 Piste C — Submission / dissemination logistics

**Gap C1: arXiv endorsement process for hep-th (2026)**
- What: v6 targets `hep-th` primary. First-time submissions to `hep-th` in
  2026 require an endorser. The process is: (1) request endorsement code via
  arXiv account → (2) endorser submits code → (3) paper is accepted. Typical
  wait: 1-2 weeks; some senior authors respond within 48 hr.
- Recommended reading:
  (a) arXiv endorsement policy (official): https://arxiv.org/help/endorsement
      — read the current 2026 version; do not rely on memory of 2023 policy.
  (b) arXiv moderation page: https://arxiv.org/help/moderation — understand
      what triggers cross-list vs hold.
  (c) No paper to read; this is a process gap. Action: identify 2 potential
      endorsers from the v6 watchlist (Pedraza, Leutheusser, Satishchandran,
      Hollands) and draft a brief endorsement request email BEFORE submitting.
- Time to fill: 0 hr reading; ~2 hr preparation + 1-2 week wait.

**Gap C2: svjour3 (Springer JHEP) LaTeX port**
- What: JHEP requires svjour3; GROUND_TRUTH D.7 flags this open. Port involves
  class file swap, \maketitle restructure, bibliography style (jhep.bst).
- Reading: JHEP author guidelines:
  https://link.springer.com/journal/13130/submission-guidelines (svjour3 template).
- Time to fill: ~4 hr (port + compile clean + bib-audit re-run).

**Gap C3: HAL alternative sub-archive for v5**
- What: if arXiv gr-qc endorsement delayed, HAL (hal.science) is the French
  open-repository fallback; sub-archive `domain:phys.grqc` or `phys.hphe`.
- Reading: https://doc.archives-ouvertes.fr/en/ — submission guide.
- Time to fill: ~1 hr once PDF is final.

---

## SECTION 4 — Consolidated 6-Month Resource Ramp-Up Plan

Integrates Pistes A + B + C with honest sequencing constraints.

### Month 1 (April–May 2026) — Foundation

**Week 1 (now):**
- Fetch RAG Priority 1-2: Liu2026.txt, HollandsLongo2025.txt (2 hr).
- Fetch RAG Priority 3-4: Barrow2025.txt, SanchezLopez2025.txt (2 hr).
- Fix RAG bad entries: Faraoni2000 → gr-qc/0006091; Matsubara2003 → correct ID (1 hr).
- Add KFLS2024 entry to INDEX.md (5 min).
- **v5 §3.5 Wolf-consolidated edit**: 30 min prose + recompile → push v5.0.2 (Piste A).
- **χ(z) caveat**: add one-sentence frozen-field caveat to v5 §3.5 per
  V8-Cassini-BORDERLINE verdict (30 min).

**Week 2-4:**
- Read Liu2026 §§2-4 (Gap B1): map Pinsker step alignment with Liu QFC.
- Read Hollands-Longo 2025 (Gap B2): identify QNEC simplification technique.
- Read Sanchez-Lopez 2025 §§3-4 (Gap A3): update v5 comparison table.
- Identify arXiv endorser candidates; draft endorsement email (Gap C1).
- Begin svjour3 port for v6 (Gap C2): 4 hr, local.

### Month 2 (May–June 2026) — Submission push

- Submit v5.0.2 to EPJ C SCOAP3 (Piste C/A).
- Submit v6.0.4 to arXiv hep-th + gr-qc (pending endorsement) and JHEP
  (Piste C/B).
- Run local 2-param MCMC (ξ_χ, α) plugin route (~12 hr, workstation) as
  feasibility check for journal referee expectations.

### Month 3-4 (June–August 2026) — v7 scoping

- Write v7 technical note: v6 Pinsker step ↔ Liu 2026 QFC (~1 week authorship
  once B1+B2 gaps filled).
- Begin hi_class C-patch (Gap A1): α_M, α_B, α_K for ξ_χ R χ²/2.
  3-4 weeks C authorship; no cloud until benchmarking phase.
- Weekly arXiv surveillance (V6-5 rule): Pedraza-Svesko, Caputa, Hollands, Liu.

### Month 5-6 (August–October 2026) — Data horizon prep

- DESI DR3 release (2026-H2 expected): update Fisher code with actual
  covariance (2-4 hr, local).
- If hi_class C-patch complete: A100 sweep (~€30 cloud) for ξ_χ × f_EDE × α.
- If DR3 strongly confirms dynamical DE: escalate v5 to PRD/JCAP data-analysis
  tier (requires full MCMC, ~€180 cloud).
- FLRW extension scoping (v6-D): read KFLS2024 §§3-4; assess compatibility
  with KS-covariance RUN-CONDITIONAL (V8-KS register).

---

## Top-3 Highest-ROI Resource Investments

**ROI-1 — Fetch Liu2026.txt + HollandsLongo2025.txt** (2 hr, €0)
These two papers are the only RAG gaps that block v7 theorem work (Piste B).
Without them, the Pinsker ↔ QFC connection note cannot be written at rule-1
standards. Cost: 2 hours. Yield: unblocks an entire medium-term paper.

**ROI-2 — v5 §3.5 Wolf-consolidated prose edit** (30 min, €0)
Directly implements landscape synthesis item 2 and GROUND_TRUTH weakness D.9.
Eliminates the hardest reviewer flag (negative literature claim + superseded
Cassini vs Wolf). Cost: 30 min. Yield: v5.0.2 ready for EPJ C submission.

**ROI-3 — arXiv endorser outreach for hep-th** (2 hr preparation, €0)
The single process bottleneck for v6 arXiv deposit. Identification of one
endorser from {Pedraza, Leutheusser, Satishchandran, Hollands} takes one email.
Without endorsement, v6 cannot be deposited and JHEP cannot receive it. Cost:
2 hr + 1-2 week wait. Yield: removes the v6 submission blocker entirely.

## Recommended first-week action (sequential)

1. (Day 1, 4 hr) Fetch and extract Liu2026.txt, HollandsLongo2025.txt,
   Barrow2025.txt, SanchezLopez2025.txt → add to `paper/_rag/` and update
   INDEX.md.
2. (Day 1-2, 1 hr) Fix Faraoni2000 and Matsubara2003 RAG entries.
3. (Day 2, 1 hr) v5 §3.5 Wolf-consolidated edit + χ(z) caveat sentence →
   commit v5.0.2 draft.
4. (Day 2-3, 2 hr) Read Liu2026 §§2-4; annotate with alignment to v6 Pinsker
   step in a `derivations/V7-liu-pinsker-alignment.md` scratch file.
5. (Day 3, 2 hr) Draft endorsement request email; send to first candidate.
6. (Day 4-5, 4 hr) svjour3 port for v6 → compile clean.

Total first-week cost: ~14 hr authorship, €0, no cloud.

---

*Document discipline: all URLs in this plan are publicly verifiable arXiv or
journal links. No Vast.ai price is presented as guaranteed — the pricing page
URL is cited instead. No FAILED.md entry (F-1 through F-19) is re-opened.*
