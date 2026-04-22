# Piste A — DR3 + Euclid DR1 First-Mover NMC Pipeline: Investigation Plan

*Date: 2026-04-22. Author: Kevin Remondière.*
*Honesty gates: PRINCIPLES rule 1 (every tool/benchmark cited must link to a
specific URL, verified or flagged [UNVERIFIED]); rule 12 (no claim beyond what
derivations support). FAILED.md F-2 codifies V6-4: Piste A is a FUTURE FIT
TOOL for v5-extension, NOT a new falsifier for v6. No cosmological claim for
v6 is introduced here.*

---

## 0. Scope and purpose

Piste A builds an operational NMC MCMC pipeline able to consume DESI DR3 +
Euclid DR1 + Pantheon+/Union3 + LSST Y1 shear data the day they are released
(expected 2026 Q4–2027 Q2 for DESI DR3; ~2027 for Euclid DR1). The pipeline
would make this repo a first-mover in the NMC quintessence community for the
next data-release cycle.

Scientific scope: v5 extension only. Piste A does not introduce any new
falsifier for v6; it operationalises the DR3/LSST Y10 forecast targets already
stated in v5 §3.5 and in D16.

---

## 1. Inventory of existing assets

### 1.1 Cobaya plugin route (operational, limited)

`mcmc/cobaya_nmc/eci_nmc_theory.py` (299 lines):
- Wraps vanilla `classy` (quintessence_exponential, minimally-coupled).
- Post-processes the perturbation sector with the D14 analytic G_eff/eta map
  in the quasi-static sub-horizon approximation.
- Integrates chi(a) as a minimally-coupled thawing scalar (no xi back-reaction
  on H); the NMC Friedmann term -6 xi H chi chi' is ignored.
- Loads D13 B_num tabulated correction from
  `derivations/_results/D13-summary.json`.
- Exposes: G_eff_over_GN(a), eta_slip(a), fsigma8(z), wa_nmc_correction.
- **Critical limitation**: quasi-static approximation only; not valid for
  Euclid lensing power spectrum (which samples super-Hubble and horizon-scale
  modes); NOT trustworthy for CMB likelihoods.
- Validated against: DESI DR2 BAO + Pantheon+, D17 MCMC (ξ_χ = 0.003
  +0.065/-0.070, R-1=0.036, ESS=1646).

### 1.2 hi_class NMC C-patch (partially implemented)

Base: `hi_class_public` upstream commit `50f447c` (Pr #15).
Location: `mcmc/nmc_patch/hi_class_nmc/`
Status per `PATCH_DIFF.md`:

**Implemented (139 insertions, 2 files):**
- `include/background.h`: `nonminimal_coupling` enum value added;
  `V_chi_form` field (enum: monomial/exponential/cosine) added to `struct background`.
- `gravity_smg/gravity_models_smg.c`: Parser block reading 5 `parameters_smg`
  entries; G_i case in `gravity_models_get_Gs_smg` computing
  G2 = X - V, DG4 = -xi*phi^2/2; initial-condition case; diagnostic printout.
- The patch reuses hi_class's existing Horndeski machinery: M2_smg = 2G4 =
  1 - xi*phi^2, alpha_B, alpha_M, and full perturbation coefficients are
  computed automatically from the G_i.

**Not yet implemented (per PATCH_DIFF.md §"Not yet implemented"):**
- Explicit `xi phi^2 < 1e-6` weak-coupling assert for initial conditions
  (design §B.3).
- G_eff(z,k) output column (design §D); currently derived externally from
  alpha_B, alpha_M, M2_smg post-processing.
- Validation tests E.2 (small-xi analytic match) and E.3 (xi=0.1 sanity).

### 1.3 Derivations

- D13: B_num tabulated correction (numeric fit of Delta_w_a).
- D14: analytic G_eff map (quasi-static).
- D16: Fisher forecast (σ(ξ_χ)|DR3 = 0.155, σ(ξ_χ)|DR3+LSST = 0.090).
- D17: DR2 + Pantheon+ MCMC chains.

### 1.4 Deploy infrastructure

`mcmc/deploy/`: Vast.ai EPYC spot runbook, `vast_ai_on_create.sh`, MPI run
script, checkpoint rsync, teardown checklist. Validated at ~$2.40 per 3.6h
run on EPYC 9965.

---

## 2. Data-readiness gaps

### 2.1 Current working likelihood

`bao.desi_dr2.desi_bao_all` — Cobaya built-in as of Cobaya ≥3.5
(https://cobaya.readthedocs.io/en/latest/likelihood_desi.html [UNVERIFIED —
confirm exact module name against Cobaya release notes when DR3 ships]).

### 2.2 Missing likelihoods per expected dataset

| Dataset | Expected release | Cobaya module status | Gap |
|---|---|---|---|
| DESI DR3 BAO | ~2026 Q4 | `bao.desi_dr3.*` — does not yet exist | Need upstream Cobaya PR or local wrapper |
| DESI DR3 full-shape P(k) | ~2026 Q4 | No existing module; DESI DR2 full-shape not in Cobaya [UNVERIFIED] | Custom likelihood class + window functions |
| Pantheon+ SN (current) | Available | `sn.pantheonplus` — Cobaya built-in | Ready |
| Union3 SN [UNVERIFIED] | 2024 (released) | `sn.union3` — [UNVERIFIED if in Cobaya] | Likely needs custom wrapper |
| Euclid photometric (3×2pt) | ~2027 | Not yet open-sourced | CRITICAL blocker; see Risk §5 |
| Euclid spectroscopic P(k) | ~2027 | Not yet open-sourced | CRITICAL blocker |
| LSST Y1 shear | ~2027 | Not in Cobaya; DESC+Rubin forthcoming | Custom wrapper + intrinsic alignment model |

**For the BAO-only route** (minimal pipeline, highest confidence):
- Only DR3 BAO is needed; Pantheon+ is already available.
- Gap: one Cobaya likelihood wrapper for DR3 BAO in the DESI-released format.
- DESI releases BAO data as FITS tables + covariance; the existing
  `desi_bao_all` wrapper pattern is directly replicable once the DR3 tables
  are posted (https://data.desi.lbl.gov/public/ [UNVERIFIED — monitor DESI
  data portal for DR3 drop]).

**For the full pipeline** (DR3 + Euclid + LSST):
- Euclid likelihood is the dominant unknown: as of 2026-04-22, Euclid DR1
  likelihoods are expected to be released alongside data but the timeline and
  API are not confirmed [UNVERIFIED — monitor https://www.euclid-ec.org/].
- LSST shear requires an intrinsic alignment (IA) nuisance model and photo-z
  calibration parameters (15–20 additional nuisance parameters), not
  marginalised in any current ECI MCMC.

### 2.3 hi_class-to-Cobaya interface for full-shape P(k)

The Cobaya plugin route (`eci_nmc_theory.py`) uses quasi-static G_eff
post-processing on a minimally-coupled background. For full-shape P(k) (needed
for DR3 and Euclid spectroscopic), the correct route is the hi_class C-patch
route: let hi_class compute alpha_B(z), alpha_M(z), M2_smg(z) self-consistently
and expose P(k,z) via the `classy_sz` or `hi_class` Python wrapper. The
`CosmoBolognaLib` / `MontePython` wrappers for hi_class [UNVERIFIED] or a
Cobaya `ExternalTheory` wrapping the hi_class Python binding are the two
practical paths.

---

## 3. Validation programme

Objective: test the DR3-ready pipeline against known-truth ξ_χ injections
BEFORE real data arrives. Candidates:

### 3.1 AbacusSummit (recommended first choice)

AbacusSummit is a suite of high-accuracy N-body simulations (Maksimova et al.
2021, MNRAS 508:4017; https://abacussummit.readthedocs.io/). It provides mock
HOD galaxy catalogs in DESI-like geometry. Standard ΛCDM cosmologies only;
does not natively provide NMC runs.

**Validation use**: Run the pipeline on AbacusSummit ΛCDM mocks with ξ_χ = 0
injected; recover ξ_χ = 0 ± expected σ. Tests pipeline mechanics and
likelihood wrapper, not the NMC signal. At ~$1–2 per MCMC run, this is the
cheapest validation gate.

### 3.2 DESI EDR / DR1 mocks (EZmocks)

DESI provides EZmock catalogs alongside DR1 (https://data.desi.lbl.gov/public/edr/
[UNVERIFIED exact path for DR1 mocks]). These reproduce the DESI DR1
clustering statistics. Same caveat: ΛCDM-truth only; inject ξ_χ = 0 and
recover.

### 3.3 Euclid Flagship2 (recommended for Euclid validation)

Euclid Flagship2 is a 3.36 trillion-particle simulation in a Euclid-like
survey volume (Potter et al. 2017; Castander et al. 2023 [UNVERIFIED arXiv
ID — do not cite without verification]). Access: Euclid Consortium internal
for DR1; public release status is [UNVERIFIED as of 2026-04-22].

**Validation use**: If accessible, test the 3×2pt Euclid likelihood wrapper
on Flagship2 mocks before real DR1 data. Critical for catching photo-z and IA
nuisance degeneracies.

### 3.4 ξ_χ-injected synthetic data (recommended complement)

Generate synthetic BAO+SN+P(k) mock observations at ξ_χ = {0, 0.05, 0.10}
using the hi_class C-patch output and white Gaussian noise at DR3 precision.
Run the full MCMC and verify recovery. This is the only way to test the NMC
signal chain end-to-end before real data. Cost: 1–2 Vast.ai runs (~$5–10 total).

### 3.5 Uchuu/Uchuu-SDSS

Uchuu is a 2.1 trillion-particle simulation (Ishiyama et al. 2021, MNRAS 506:4210;
http://skiesanduniverses.org/Simulations/Uchuu/ [UNVERIFIED current URL]).
Uchuu-SDSS provides SDSS/eBOSS-like mocks. Less relevant for DESI-DR3 geometry
than AbacusSummit but useful for cross-validation.

**Priority order**: synthetic ξ_χ injection > AbacusSummit ΛCDM > DESI EZmocks
> Euclid Flagship2 (if accessible).

---

## 4. Compute budget

Reference pricing: Vast.ai H100 SXM spot as of 2026-04 [UNVERIFIED — verify
at https://cloud.vast.ai/create/ before committing budget].
Typical H100 spot: $1.80–$3.50/GPU-h depending on host and time.
EPYC 9965 CPU spot (used in current runbook): $0.50–$0.80/h.

The MCMC is CPU-bound (CLASS/hi_class integration); GPU not needed.

### 4a. Patch completion + CI tests (small)

Tasks: implement E.2 + E.3 validation tests, weak-coupling assert, G_eff
output column, and write 2–3 CI integration tests (ξ_χ=0 recovery, monomial
vs exponential potential).

Compute: purely local dev; no cloud needed.
Estimated cost: **€0 cloud**; ~20 hours developer time.

### 4b. 4-chain MPI MCMC on DR3 + Pantheon+ (medium)

Configuration: 4 chains × 2 MPI ranks each = 8 MPI processes.
CLASS calls/chain: ~50 000 accepted samples at DR3 precision.
Wall-clock target (analogous to current DR2 run scaled for DR3 σ):
~8–12 h on EPYC 9965 (more params, same architecture).

Cost: $0.70/h × 10 h × 1 instance = **~$7 (~€6.50)**.

Safety cap: $20 (covers 2 full runs + overhead).

### 4c. Full 4-chain MPI on DR3 + Euclid DR1 + Pantheon+ + LSST Y1 (large)

Configuration: 4 chains × 4 MPI ranks + CMB Plik-lite + Euclid 3×2pt +
LSST shear + ~25 nuisance parameters. Wall-clock: ~30–48 h estimated
(Euclid likelihood calls are expensive; [UNVERIFIED — depends on Euclid
likelihood implementation speed]).

Cost: $0.70/h × 40 h × 1 instance = **~$28 (~€26)**.
Conservative (2× overrun): **~€52**.

For nested sampling (PolyChord, to get proper Bayes evidence vs BF_01):
add 3–5× wall-clock multiplier → ~€80–130 per full evidence run.

**Summary table:**

| Scenario | Wall-clock | Vast.ai cost |
|---|---|---|
| (a) Patch + CI | local only | €0 |
| (b) DR3 + Pantheon+ MCMC | ~10 h | ~€6.50 |
| (c) DR3 + Euclid + Pantheon+ + LSST Y1 | ~40 h | ~€26–52 |
| (c) nested sampling variant | ~150 h | ~€80–130 |

---

## 5. Risk map

### Risk 1 (CRITICAL): Euclid DR1 likelihood not open-sourced at release

The Euclid Collaboration may release the likelihood code only to consortium
members for 12–24 months post-data-release (analogous to Planck's ~6-month
embargo on the Plik likelihood). If this happens, the full DR3+Euclid pipeline
cannot be assembled until the likelihood is public.

**Mitigation**: (a) Monitor https://www.euclid-ec.org/ and the Euclid GitHub
organisation [UNVERIFIED URL]. (b) Prepare a synthetic Euclid-like Fisher
likelihood as a stand-in (already feasible with D16 infrastructure). (c) The
BAO-only DR3 pipeline (Piste A §3.1 route) does not depend on Euclid and can
proceed independently.

### Risk 2 (HIGH): hi_class Boltzmann instabilities in NMC phantom-crossing regime

The hi_class Horndeski machinery is known to develop numerical instabilities
when the effective Planck mass M2_smg = 1 - xi*phi^2 approaches zero
(ghost-crossing, or when xi > 0 and phi^2 → 1/xi). For the NMC model at
|ξ_χ| ≤ 0.10 and χ_0 = M_P/10, M2_smg = 1 - 0.1×(0.1)^2 = 0.999 —
well within the stable regime. However, during the MCMC sampling, proposals
with |ξ_χ| up to 0.30 and χ_0 up to M_P/2 are possible depending on prior
choice; at ξ_χ = 0.30, χ_0 = 0.3 M_P: M2_smg = 1 - 0.30×0.09 = 0.973 —
still safe. At ξ_χ = 1.0 and χ_0 = M_P: M2_smg = 0, ghost crossing.

**Mitigation**: Add a prior boundary `xi_chi * chi_0^2 < 0.5` in the MCMC
yaml, and implement the weak-coupling assert from design §B.3 (already in the
"Not yet implemented" list). Document this as a hard sampler prior.

### Risk 3 (MEDIUM): DESI DR3 systematic masking and window-function incompatibility

DESI DR3 full-shape P(k) will be released with survey window functions that
differ from DR2 in footprint and masking strategy. The current pipeline does
not implement window-function convolution (the DR2 BAO-only route absorbs this
at the likelihood level). For full-shape P(k), the window-function matrix must
be computed from the DESI DR3 randoms and convolved with the theory P(k).

**Mitigation**: Use the BAO-only DR3 route as the first milestone. Full-shape
P(k) extension is a second milestone contingent on the DESI DR3 data release
format. `pypower` + `pycorr` [UNVERIFIED: https://github.com/cosmodesi/pypower]
are the standard DESI tools for window functions.

---

## 6. Six-month roadmap

Target: pipeline operational and validated before DESI DR3 release
(expected 2026 Q4 / 2027 Q1).

### Month 1 (May 2026) — Complete the C-patch

Tasks:
1. Implement validation tests E.2 (small-ξ analytic match: G_eff → 1 + 2ξχ²
   at linear order) and E.3 (ξ=0.1, exponential potential, sanity vs
   quintessence_exponential baseline).
2. Add weak-coupling guard: `class_test(xi*phi*phi > 0.9, ...)` with error msg.
3. Add G_eff(z,k) post-processing as an output column derived from M2_smg,
   alpha_B, alpha_M. Verify against D14 formula at k = 0.1 h/Mpc.
4. Run hi_class NMC background at MAP (ξ_χ=0.003, χ_0=M_P/10, exponential
   potential α=0.55) and compare H(z), P(k,z=0) to the Cobaya plugin route.
   Acceptable tolerance: ΔH/H < 0.1%, ΔP/P < 0.5% at k < 0.2 h/Mpc.

Deliverable: `mcmc/nmc_patch/hi_class_nmc/` passes all 3 tests; results
committed to `derivations/V9-hiclass-patch-validation.py`.

### Month 2 (June 2026) — Cobaya interface for hi_class route

Tasks:
1. Write a Cobaya `ExternalTheory` wrapper that calls hi_class via its Python
   binding (`classy`) with `gravity_model = nonminimal_coupling`.
2. Interface: exposes P(k,z), H(z), angular_diameter_distance(z), fsigma8(z).
3. Wire into existing MCMC yaml (`eci_nmc_optimized.yaml` or successor).
4. Run synthetic validation MCMC: inject ξ_χ = 0.05, recover within 1σ.

Deliverable: `mcmc/cobaya_nmc/eci_hiclass_theory.py`; validation chains in
`mcmc/chains/V9-synthetic-inject/`.

### Month 3 (July 2026) — BAO DR3 likelihood wrapper + monitoring

Tasks:
1. Write a template Cobaya BAO likelihood wrapper for the DESI DR3 table
   format (mirror of the existing `desi_bao_all` structure).
2. Validate against DESI DR2 data (the wrapper should exactly reproduce the
   DR2 run with the DR3-format code path).
3. Monitor DESI data portal (https://data.desi.lbl.gov/public/) weekly for
   DR3 early-access announcements.
4. Run AbacusSummit ΛCDM mock pipeline: inject ξ_χ=0, recover ξ_χ=0 ±σ.
   Cost: ~€6.

Deliverable: `mcmc/cobaya_nmc/desi_dr3_bao.py`; AbacusSummit validation
report in `mcmc/_results/V9-abacus-validation.md`.

### Month 4 (August 2026) — DR3 + Pantheon+ MCMC (full hi_class route)

Tasks:
1. Full 4-chain MPI MCMC on DESI DR3 BAO + Pantheon+ using hi_class route.
   (Only feasible if DR3 is released; otherwise run on DR2 as final
   hi_class-route validation at full-data scale.)
2. Compare ξ_χ posterior against D17 Cobaya-plugin-route chains. Acceptable:
   median shift < 0.5σ, σ(ξ_χ) change < 20%.
3. Cost: ~€7 per run; budget 2 runs = €14.

Deliverable: `mcmc/chains/V10-dr3-hiclass/`; updated D17-successor table
in v5 §4.

### Month 5 (September 2026) — Euclid likelihood monitoring + LSST shear prep

Tasks:
1. Monitor Euclid DR1 likelihood release (https://www.euclid-ec.org/).
2. If Euclid likelihood is public: wrap it as a Cobaya likelihood and test
   on Flagship2 mocks (or synthetic Gaussian mock at DR1 precision).
3. If not public: build synthetic Fisher-level Euclid 3×2pt likelihood as
   a DR1 stand-in (extends D16 Fisher code).
4. Design LSST Y1 shear likelihood interface: identify intrinsic alignment
   model (NLA or TATT), photo-z bin structure, nuisance parameters (target:
   DESC SRD-compatible [UNVERIFIED: https://github.com/LSSTDESC/DESC_SRD]).

Deliverable: Euclid wrapper or synthetic stand-in; LSST nuisance parameter
design document.

### Month 6 (October 2026) — Full combined pipeline + paper update

Tasks:
1. Full 4-chain MCMC: DR3 + Euclid (or stand-in) + Pantheon+ + LSST Y1.
   Cost: ~€26–52 (spot; reserve €100 for safety).
2. If σ(ξ_χ)|combined < 0.12 (within D16 forecast): write forecasted result
   as v5 §4 update (Table 2 extension). No new falsifier; just the forecast
   in operation.
3. Archive pipeline: Dockerfile + on-create script updated for full dataset.
4. Submit v5.0.x with DR3 result note (if DR3 has dropped by then).

Deliverable: `mcmc/chains/V11-dr3-euclid-lsst/`; v5.0.x revision.

---

## 7. Honesty caveats (Rule 1 / Rule 12)

1. **All Vast.ai pricing is [UNVERIFIED]**: spot prices fluctuate. Verify at
   https://cloud.vast.ai/create/ before committing budget. The €6–52 estimates
   use $0.70/h for a 48-core EPYC instance, which matches the current runbook's
   $0.50–0.80/h range but is not a guarantee.

2. **DESI DR3 release timeline is [UNVERIFIED]**: "expected 2026 Q4" is based
   on the DESI survey schedule and the DR2 (2025 Q1) cadence. The actual date
   may slip. Monitor https://data.desi.lbl.gov/public/.

3. **Euclid DR1 likelihood open-source status is [UNVERIFIED]**: The embargo
   policy is not confirmed. Risk 1 above is a direct consequence.

4. **AbacusSummit, Euclid Flagship2, Uchuu URLs**: cited with best-available
   references but specific data-access policies and URLs must be verified at
   access time. Do not assume public availability of Flagship2 for non-members.

5. **σ(ξ_χ) forecasts**: D16 uses the D13 linear predictor (B_num fixed at
   Ω_Λ=0.7). The 30–40% nonlinearity at χ_0 ≠ M_P/10 is documented in
   v5_gap_analysis §A1. The numbers here are illustrative, not publication-
   ready; a 2D (χ_0, ξ_χ) Fisher grid is needed for a submission-quality
   forecast table.

6. **Piste A is a pipeline project, not a new cosmological falsifier**:
   consistent with FAILED.md F-2 (V6-4). The pipeline will produce a ξ_χ
   posterior at DR3 precision; whether that posterior constitutes evidence for
   or against NMC coupling is a result of the MCMC, not a claim made here.

---

*Internal working document. No claim herein enters paper/*.tex without
WebSearch verification (rule 1) and derivation anchor (rule 12).*
