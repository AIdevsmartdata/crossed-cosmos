# C4 Joint MCMC — Pre-registration Design Document v1
**Date:** 2026-05-04
**ECI version:** v6.0.43 (Zenodo DOI 10.5281/zenodo.20019492) + v6.0.44 patch
**Status:** PRE-REGISTRATION — to be tagged `c4-preregistration-v1` before any production booking
**Source:** synthesised from agent campaign 2026-05-04 (P4_5 design report) + scaffolding in `compute/C4_joint_mcmc/`

---

## 0. Why this document exists

`compute/C4_joint_mcmc/` was scaffolded in v6.0.42 (commit 22:07 2026-05-03) with a `README.md` only — all scripts (`make_yamls.py`, `compute_evidence.py`, `plot_corner.py`) are TODO stubs. This document locks the **priors, datasets, sampler config, and decision thresholds** before any Vast.ai Profile L booking, so the production run is pre-registered and not p-hackable.

Cobaya 3.6.2, cosmopower_jax 0.5.5, hi_class_public, AxiCLASS in `~/.venv-mcmc-bench` on the local PC (Tailscale 100.91.123.14). PolyChord installed 2026-05-04 09:30 via `cobaya-install polychord --packages-path compute/C4_joint_mcmc/packages/`. KiDS-1000 S8 wrapper `cobaya_nmc/eci_kids_s8.py` operational and tested.

**Pre-run blocker remaining:** AxiCLASS EDE module (M9) — needs sanity test with `nlive=20, num_repeats=5` on Profile S ($4) before Profile L commitment.

---

## 1. References (triangulated 2026-05-04)

| Topic | Reference | arXiv |
|---|---|---|
| Cobaya | Torrado-Lewis JCAP 05 057 | 2005.05290 |
| PolyChord | Handley-Hobson-Lasenby MNRAS 450 L61 | 1502.01856 |
| Suspiciousness | Handley-Lemos PRD 100 043512 | 1902.04029 |
| DESI DR2 BAO | DESI Collab PRD 112 083515 | 2503.14738 |
| Pantheon+ | Brout et al. ApJ 938 110 | 2202.04077 |
| KiDS-1000 3×2pt | Asgari et al. A&A 645 A104 | 2007.15633 |
| ACT DR6 lensing map | Madhavacheril et al. ApJ 962 113 | 2304.05203 |
| ACT DR6 lensing PS | Qu et al. | 2304.05202 |
| Coupled-DE Amendola | Amendola PRD 60 043501 | astro-ph/9904120 |
| GW170817 α_T | LIGO/Virgo ApJL | 1710.05834 |
| Cassini | Bertotti-Iess-Tortora Nature 425 374 | DOI:10.1038/nature01997 |
| Dark Dimension | Montero-Vafa-Valenzuela JHEP | **2205.12293** (NOT 2203.10757) |
| Tsallis HDE | Tavayef et al. PLB 781 195 | 1804.02983 |
| SH0ES | Riess et al. ApJL | 2112.04510 (optional only) |
| NMC quintessence (primary external risk) | Wolf-García-García-Anton-Ferreira PRL 135 081001 | **2504.07679** |

**KiDS-1000 S8 = 0.759 +0.024/−0.021** (Asgari 2021). NOT 0.766 (= deprecated KiDS-450).

---

## 2. Model set (10 models, locked)

### 2.1 Shared base parameters
H_0 ∈ Flat[55, 85] km/s/Mpc; ω_b ∈ Flat[0.017, 0.027]; ω_cdm ∈ Flat[0.09, 0.15]; n_s ∈ Flat[0.90, 1.05]; log(10¹⁰ A_s) ∈ Flat[2.5, 3.5]; τ_reio ∈ Flat[0.02, 0.12]. Σmν fixed: m_ncdm = 0.06 eV, N_ur = 2.0328, N_ncdm = 1.

### 2.2 Per-model definitions

| # | Model | Extra params | Total | nlive | Theory plugin |
|---|---|---|---|---|---|
| M1 | ΛCDM (null) | — | 6 | 500 | classy vanilla |
| M2 | ECI dust+structure | ξ_χ ∈ [-0.1, 0.1], χ_ini ∈ [0.05, 0.20]; **Cassini wall \|ξ_χ\|·(χ_0/M_P)² < 6e-6** | 8 | 500 | classy + ECINMCTheory |
| M3 | wCDM | w_0 ∈ [-1.3, -0.7] | 7 | 500 | classy PPF |
| M4 | CPL w_0w_a | w_0 ∈ [-1.2, -0.5], w_a ∈ [-2.0, 1.0] | 8 | 500 | classy PPF |
| M5 | Coupled-DE Amendola | β_c ∈ [0, 0.5], w_φ ∈ [-1, -0.5] | 8 | 500 | hi_class + bespoke plugin |
| M6 | BH/DHOST (α_T=0) | α_B ∈ [-0.5, 0.5], α_M ∈ [-0.5, 0.5] | 8 | 500 | hi_class Horndeski |
| M7 | Holo-Tsallis | δ ∈ [1, 2], c²_HDE ∈ [0.5, 1.5] | 8 | 500 | bespoke plugin |
| M8 | Dark Dim (proxy) | λ ∈ [0.1, 2.0] (exp quintessence) | 7 | 500 | classy scalar field |
| M9 | EDE+late-DE | f_EDE ∈ [0, 0.2], log z_c ∈ [2.5, 4.5], θ_ini ∈ [0.1, π−0.1], w_late ∈ [-1.1, -0.7] | **10** | **1000** | AxiCLASS + PPF |
| M10 | NMC quintessence | w_0 ∈ [-1.2, -0.5], ξ_φ ∈ [-0.1, 0.1] (no Cassini wall) | 8 | 500 | hi_class scalar |

---

## 3. Likelihood stack (locked)

```
log L_total = log L_BAO + log L_SN + log L_WL + log L_CMB
```

- **L_BAO:** `bao.desi_dr2.desi_bao_all` (7 z_eff bins, full covariance)
- **L_SN:** `sn.pantheonplus` (1701 light curves / 1550 distinct SNe; M_B marginalised)
- **L_WL Phase 1:** Gaussian prior S_8 = 0.759 +0.024/−0.021 via `cobaya_nmc/eci_kids_s8.py`
- **L_CMB:** `planck_2018_lowl.{TT,EE}` + `planck_2018_highl_plik.TTTEEE_lite` + `act_dr6_lenslike.ACTDR6LensLike`

Partial-dataset runs (BAO-only, +SN, +WL) generated as by-products to trace dataset-pulling.

**SH0ES NOT used in main evidence chain** (introduces H_0 prior conflict; H_0 left to data).

---

## 4. Sampler config (LOCKED)

```yaml
sampler:
  polychord:
    nlive: 500          # 1000 for M9 only
    num_repeats: 30
    do_clustering: true
    precision_criterion: 0.001
    max_ndead: -1
    boost_posterior: 0.0
    feedback: 3
    path: packages/code/PolyChordLite
```

**MPI flags for Vast.ai Docker:**
```
mpirun -np 4 --bind-to none --mca btl_vader_single_copy_mechanism none --oversubscribe \
       python -m cobaya run model.yaml
```

**Fallback:** Cobaya MCMC (R−1 < 0.05) + `anesthetic` harmonic Z post-processing. Error ~1–2 nat — adequate for ranking, not for |log B| < 2 discrimination.

---

## 5. Compute budget on Vast.ai

Per `VASTAI_SIZING.md` Profile L: 64 vCPU + 4×A100 80 GB PCIe + 256 GB DDR5 at ~$5/h.

| Phase | Instance | Duration | Cost |
|---|---|---|---|
| Pre-run sanity (M1+M9 + PolyChord MPI) | Profile S (RTX 4090) | 8 h | $4 |
| cosmopower-jax emulator training (M5, M9) | Profile L | 6 h | $30 |
| Production run all 10 models | Profile L | ~100 h (3-5× safety) | $500 |
| Post-processing + plots | Profile M (A6000) | 24 h | $17 |
| **Total** | | **~138 h** | **~$551** |

Within $600-1000 budget. Reserve $200 for restarts → ceiling $750.

**Set Vast.ai email alerts at $200/$400/$600 BEFORE booking.**

---

## 6. Pre-registration protocol

Before any Profile L booking, commit and tag `c4-preregistration-v1` with:

```
compute/C4_joint_mcmc/preregistration/
├── design_doc_v1.md          # this file
├── model_definitions.yaml    # 10 models, all parameters, all priors
├── likelihood_config.yaml    # exact Cobaya module names + cobaya version
├── sampler_config.yaml       # PolyChord nlive/num_repeats per model
├── dataset_checksums.md      # SHA256 of input data files
└── decision_criteria.md      # §7 thresholds verbatim
```

### 6.1 Amendment protocol
Any prior change after tagging → new tag `c4-preregistration-v2` with changelog. Both analyses reported in paper. Change reason documented.

### 6.2 Dataset SHA256 to lock
- `packages/data/bao_data/desi_dr2/desi_bao_dr2_data.txt`
- `packages/data/sn_data/pantheon_plus/Pantheon+SH0ES.dat`
- KiDS-1000 S8 hardcoded in `eci_kids_s8.py` (0.759 +0.024/-0.021) — N/A for SHA
- `packages/data/planck_2018/plc_3.0/` (full directory hash)
- `packages/data/act_dr6_lenslike/ACTDR6Lens*.fits`

---

## 7. Decision criteria (LOCKED — Jeffreys natural-units thresholds)

| \|log B_{i,1}\| (nat) | Jeffreys label | Interpretation |
|---|---|---|
| < 1 | inconclusive | cannot distinguish |
| 1–3 | moderate | weak preference |
| 3–5 | strong | clear preference |
| > 5 | very strong | decisive |

### 7.1 ECI-specific falsification window (PRE-REGISTERED)

| log B_{M2,M1} | Outcome | Action |
|---|---|---|
| > +5 | ECI decisive win | submit; check look-elsewhere |
| +1 to +5 | ECI moderate win | claim; continue v7 |
| **−3 to +1** | **Bayes-comparable (EXPECTED)** | "not falsified"; DR3 forecast |
| −5 to −3 | ΛCDM moderate win | dataset-by-dataset diagnosis |
| < −5 | ECI decisively disfavoured | report falsification, revise theory |

**Predicted outcome:** log B_{M2,M1} ∈ [−3, +1]. Coupled-DE (M5) likely tops. ECI gains from KiDS-1000 (S8 suppression via NMC structure). CMB constrains M1 and M2 similarly (Cassini forces ξ_χ → 0).

### 7.2 No-go triggers during production
- R−1 > 5 after 10⁵ evals → kill, reduce prior width, restart
- spend > $600 with < 5 models converged → stop, partial report, second booking
- MPI deadlock → re-apply `--bind-to none --oversubscribe`
- M9 stiff ODE → fall back to CPL EDE proxy, flag in paper
- cosmopower-jax OOM → CPU CLASS fallback

---

## 8. Predicted discrimination matrix [WORKING-CONJECTURE — falsifiable]

| Model | BAO | +SN | +KiDS | Full +CMB | Driver |
|---|---|---|---|---|---|
| M5 Coupled-DE | +3±2 | +2±2 | +3±2 | +1±2 | DR2 best-fit; S8 helped |
| M4 CPL | +2±1 | +2±1 | +2±1 | +1±1 | DR2 w_a hint |
| M9 EDE+late | -1±3 | 0±3 | 0±3 | +2±3 | H_0 helps; wide-prior penalty |
| M3 wCDM | +1±1 | +1±1 | +1±1 | 0±1 | DR2 w≠-1 |
| M10 NMC quint | 0±1 | 0±1 | 0±1 | -1±1 | ξ_φ → 0 |
| M1 ΛCDM | 0 | 0 | 0 | 0 | reference |
| **M2 ECI** | -1±2 | -1±2 | 0±2 | **-2±2** | KiDS pulls up; CMB → ξ_χ → 0 |
| M6 BH/DHOST | 0±2 | 0±2 | 0±2 | -1±2 | α_T=0 kills main signal |
| M8 Dark Dim | -1±2 | 0±2 | 0±2 | -2±2 | proxy; CMB penalty |
| M7 Holo-Tsallis | -1±2 | -1±2 | -1±2 | -2±2 | extra δ; poor CMB |

**Predicted ranking:** M5 > M4 > M9 > M3 ≈ M10 ≈ M1 > M2 > M6 > M8 > M7.

---

## 9. Anti-hallucination corrections from agent campaign 2026-05-04

Verified during P4_5 design (none had propagated to repo, all caught in agent briefs / external task statements):

1. Dark Dimension arXiv ID: 2205.12293 (NOT 2203.10757 = quantum optics)
2. KiDS-1000 S_8 = 0.759 +0.024/−0.021 (NOT 0.766 = KiDS-450 deprecated)
3. PolyChord install: `cobaya-install polychord` (NOT `pip install polychord-py3` which doesn't exist on PyPI)
4. Pantheon+: 1701 light curves, 1550 distinct SNe (NOT "1701 SNe Ia")
5. ACT DR6 lensing map = 2304.05203 (Madhavacheril); ACT DR6 PS = 2304.05202 (Qu) — distinct papers
6. Karwal-Kamionkowski 2016 = arXiv:1608.01309 (NOT 1601.05005 = elastomer)

---

## 10. Forward-looking R&D items

### 10.1 Calculations to redo for v7 paper (priority order)

1. **Re-compute Levier #1 ECI v_50 chains with corrected KiDS-1000 S_8 = 0.759.** The April 30 chains used the deprecated 0.766 value indirectly. Effect: ξ_χ posterior median may shift by ~0.1σ.
2. **Re-derive (w_0, w_a) NMC trajectory analytically** (`derivations/w0-wa-nmc/` companion, deferred per eci.tex line 153). Without this, ECI-NMC and Coupled-DE cannot be discriminated in DESI DR2 (w_0, w_a) plane. Sympy + numerical integration.
3. **Bedroya c'_DD prune-analysis re-frame.** The April 30 c'_inf = 0.044 ± 0.021 result IS consistent with BOVW c' ≃ 0.05 within 1σ; the apparent tension was a normalization confusion (|w_a|_CPL = 0.44 ≠ c'_inf = 0.044 because they map differently). Update v8 paper interpretation accordingly.
4. **Hecke closure of Feruglio Y(τ)** (G4 from P1_4). Run sympy/sage check that Y(τ) for Γ_N at N=2,3,4 closes under Hecke operators T(p) for small primes. Gateway test for the Maass-form ↔ KMS structural overlap programme.
5. **Wassermann-Gui analysis for LE6 WZW.** Existing technology; never done explicitly for E6. Bridge to ECI's algebraic-envelope route.

### 10.2 New directions (ranked by promise + feasibility)

**HIGH:** Maass-form Yukawa from KMS matrix elements (P1_3 NEW HERE). Replaces holomorphic Feruglio Y(τ) with non-holomorphic polyharmonic Maass forms generated by ⟨ω | π(O) | ω⟩ in a vN algebra with KMS state ω. Provides first-principles motivation for Qu-Ding 2024 JHEP extension that the top-down literature currently lacks. Two genuine obstructions (chirality, discreteness) require new mathematics, but no known no-go.

**HIGH:** Weyl-rigidity envelope (P2_1, arXiv:2508.08194). Closest existing theorem supporting algebraic-envelope strategy. Original-result gap = extending to ECI's specific type II_∞ M̃(D). If this can be done, Theorem 1's escape route becomes constructive.

**MEDIUM:** Refute or weaken the v7 (∞,2)-functor U conjecture (P2_4). Krylov 2π saturation + rational E6-MTC are mathematically incompatible (Rabinovici et al. JHEP 03 2022). The v7 manifesto must either weaken C1 to a spectral condition compatible with rational MTCs, or replace target with a non-semisimple/non-rational structure (e.g., the von Neumann factor itself, or a derived/non-semisimple tensor category).

**MEDIUM:** The structural connection between ECI's ξ_χ NMC and Wolf-García-García-Anton-Ferreira's ξ NMC (PRL 135 081001). Both modify G_eff but the Wolf result has G_eff(0)/G_N = 1.77 (4.3σ from unity!) which would directly falsify ECI's H4 hypothesis if sustained. Two paths: (a) demonstrate ξ_χ ECI is a strict subset of Wolf ξ, in which case ECI inherits the local-gravity tension; (b) demonstrate ECI's ξ_χ is structurally distinct and immune to Cassini/LLR. Decisive for v7 paper framing.

**LOW:** Dark Dimension c'_DD = 0.05 vs ECI c'_modular = 1/6 reconciliation. The species-scale derivation gives c'_modular = 1/6 in ECI; the de-Sitter slope c'_DD ≈ 0.05 is the Bedroya phenomenological best-fit. Three distinct parameters per eci.tex section. Worth a dedicated note clarifying which c' is which.

### 10.3 Vast.ai compute prioritisation

If $1000 budget total:
- $4 Profile S sanity (M1, M9, PolyChord MPI)
- $80 cosmopower-jax emulator training for M5, M9
- $500 Profile L production (10 models)
- $200 reserve for restarts/diagnosis
- $200 Levier #1 re-run with corrected S_8 + (w_0, w_a) NMC trajectory derivation chains

Total $984. Within budget.

### 10.4 Paper sequence

1. **eci.tex v6.0.44** (this commit): audit acknowledgement + design doc reference. No scientific content change.
2. **eci v6.0.45** (after C4 production): add joint-MCMC results section, update prediction table with explicit NMC quintessence falsification window (Wolf et al. log B = 7.34 as the bar to clear).
3. **C4 paper companion** (2026-Q3): standalone joint-MCMC paper with all 10 models, suspiciousness map, dataset-pulling diagnostics. Falsifies or supports specific BSM DE candidates.
4. **eci v7.0** (2026-Q4 if 3 of 5 v7 R&D items resolve positively, else v6.0.4x): re-formulated (∞,2)-functor U with weakened C1; explicit Maass-form ↔ KMS overlap programme; Weyl-envelope reformulation of Theorem 1's escape route.

---

## Appendix: Anti-Hallucination Status

| Claim | Status | Verification |
|---|---|---|
| Dark Dimension arXiv | **2205.12293** | arXiv API verified Montero-Vafa-Valenzuela JHEP |
| KiDS-1000 S_8 | **0.759 +0.024/−0.021** | arXiv:2007.15633 + 2503.19441 cross-check |
| PolyChord install method | `cobaya-install polychord` | confirmed pypolychord NOT on PyPI |
| Wolf et al. authors | Wolf, García-García, Anton, Ferreira | NOT García-Bellido (caught) |
| Karwal-Kamionkowski 2016 | arXiv:1608.01309 | 1601.05005 = elastomer paper (rejected) |
| `c' = ⅓·c_DDC` | FABRICATED relation | independent in arXiv:2507.03090 |
| m_KK DM scale | keV | NOT 10⁻³ eV (= L⁻¹ dimension scale) |
| ECI Theorem 1 H1-H4 | verbatim eci.tex 539-551 | read directly, not paraphrased |
