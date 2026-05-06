---
name: S9 Real DESI DR2 + Pantheon+ + Planck 2018 data acquisition
description: Real data acquired (sha256-verified). Smoke test re-run reveals likelihood bug → posterior at multiple prior boundaries
type: project
---

# S9 — Real cosmological data acquisition + smoke test re-run

**Date:** 2026-05-06
**Owner:** Sub-agent S9 (Sonnet) + parent (sync to PC + smoke test re-run)
**Hallu count entering / leaving:** 85 / 85

---

## Verdict

**PARTIAL.** Real data acquired and sha256-verified. Smoke test re-run
on PC RTX 5060 Ti reveals **posterior anomaly** with real data: multiple
parameters land at prior boundaries (n_s = 0.90 lower, log₁₀(10¹⁰A_s) = 3.50
upper) and ω_b = 0.01909 sits **~22σ below** the BBN expected value
(0.02218 ± 0.00055). This is a strong signature of a **likelihood
implementation bug**, not a physical signal.

The smoke test mechanically **PASSES** (R̂ = 1.0018 < 1.05, ESS = 1121 > 100)
because NUTS converges *to a wrong posterior*. **Production runs are NOT
launched** until the likelihood bug is debugged.

---

## Data acquired (sha256-verified)

### DESI DR2 BAO
- Source: `CobayaSampler/bao_data` GitHub (downstream of arXiv:2503.14738)
- 13 data points, 13×13 covariance
- mean sha256: `9ac154ab583ce759c0f7eef3c978c7c70a6ead2d18774caceadf1a350a640585`
- cov sha256:  `252a143274c8a07c78694c119617d36594f6d7965d00319ca611c6ffb886e509`
- PC path: `/home/remondiere/data/desi_dr2/`

**Critical discrepancy caught**: previous A71 hardcoded `DESI_DR2_DEFAULT` was off by **2.1-2.8σ** vs real values:

| Bin | Old | Real | Pull |
|---|---|---|---|
| LRG1 DH/rd z=0.51 | 20.98 | 21.863 | **+2.1σ** |
| LRG2 DM/rd z=0.706 | 16.85 | 17.351 | **+2.8σ** |
| LRG2 DH/rd z=0.706 | 20.08 | 19.455 | **−1.9σ** |
| Lya DM/rd z=2.33 | 39.71 | 38.989 | **−1.4σ** |

z_eff values also corrected: QSO 1.491→1.484; LRG+ELG 0.930→0.934; ELG 1.317→1.321.

### Pantheon+
- Source: `PantheonPlusSH0ES/DataRelease` (Brout et al. 2022 arXiv:2202.04077)
- 1701 SN-Ia, full STAT+SYS 1701×1701 covariance
- `Pantheon+SH0ES.dat` sha256: `1cb0fc37...8cf8`
- `Pantheon+SH0ES_STAT+SYS.cov` sha256: `abf806d9...fdc`
- PC path: `/home/remondiere/data/pantheonplus/`
- Note: correct observable is `m_b_corr` (Tripp-corrected), NOT `MU_SH0ES`

### Planck 2018 compressed
- Source: arXiv:1807.06209 Table 2 (Aghanim et al. 2018)
- bestfit + 1σ: ω_b=0.02237±0.00015, ω_c=0.1200±0.0012, 100θ_MC=1.04092±0.00031, ln(10¹⁰As)=3.044±0.014, n_s=0.9649±0.0042
- Off-diagonal covariance: **[TBD: approximate]** — PLA tarball ~1.8 GB not downloaded
- PC path: `/home/remondiere/data/planck_2018_compressed/`
- Diagonal corrected (ω_c variance was 2.0e-6, real 1.44e-6; n_s variance was 2.2e-5, real 1.764e-5)

---

## likelihoods.py update

- 550 → 802 lines (+346 insertions, -93 deletions)
- Syntax verified (`ast.parse` OK)
- API signatures preserved (smoke test still runs)
- Loads from disk if `/home/remondiere/data/...` exists, else falls back to hardcoded defaults
- Env vars overridable: `DESI_DR2_DATA_PATH`, `PANTHEONPLUS_DATA_PATH`, `PLANCK2018_DATA_PATH`
- Module-level cache for Pantheon+ STAT+SYS (32MB, avoid re-parse per call)

---

## Smoke test re-run (PC RTX 5060 Ti, 142.7s)

### Results with REAL data

| Param | Posterior median ± σ | Expected (Planck-like) | Anomaly |
|---|---|---|---|
| H₀ | 71.22 ± 0.13 | 67.4 (Planck) — 73.0 (SH0ES) | INTERMEDIATE — borderline OK |
| ω_b | **0.01909 ± 0.00013** | 0.02237 ± 0.00015 (Planck) | **−22σ** ❗ at BBN/Planck cost |
| ω_c | 0.14580 ± 0.00020 | 0.1200 ± 0.0012 (Planck) | **+22σ** ❗ |
| n_s | **0.90006 ± 0.00008** | 0.9649 ± 0.0042 (Planck) | **−15σ** ❗ at lower prior boundary [0.90, 1.05] |
| log₁₀(10¹⁰A_s) | **3.49998 ± 0.00003** | 3.044 ± 0.014 (Planck) | **+32σ** ❗ at upper prior boundary [2.7, 3.5] |
| τ_reio | 0.05411 ± 0.00711 | 0.054 ± 0.007 (Planck) | OK ✅ |

R̂ max = 1.0018 (< 1.05) ✅
ESS min = 1121 (> 100) ✅

### Diagnosis

Multiple **prior boundary hits** + ω_b deeply below BBN expected = **likelihood implementation bug**, not physical signal. NUTS converges to a wrong posterior.

Hypothesized causes (Phase 2 debug):
1. **Planck 2018 compressed θ_MC formula**: A71 used a power-law approximation [TBD]; this likely does not correctly compute θ_*(H₀, ω_b, ω_c, ...). Wrong θ_MC in the 5×5 Gaussian cost moves all 5 compressed parameters wrong.
2. **Sound horizon r_d**: A71 uses Eisenstein-Hu approximation `sound_horizon_EH(omega_b, omega_m)`. EH approximation is good to ~1-2% but DESI DR2 is constrained to 0.3% — bias propagates into ω_b, ω_m posterior.
3. **Pantheon+ M_B handling**: A71's analytical M_B marginalization may have wrong sign or wrong covariance treatment with full 1701×1701 cov.
4. **Off-diagonal Planck 2018 cov**: marked [TBD: approximate] — diagonal-only cov fails to capture parameter correlations, breaks 5-parameter Gaussian.

---

## Action items for Phase 2

1. **Debug Planck compressed**: replace power-law θ_MC with CLASS-computed θ_* OR train a small θ_* emulator OR use full clik wrapper.
2. **Replace EH sound horizon** with CLASS r_d at 0.3% precision (or compute r_d via background ODE).
3. **Verify Pantheon+ analytical M_B marginalization**: compare to brute-force marginalization on a few samples.
4. **Download full Planck 2018 PR3.01 5×5 covariance** matrix (off-diagonal).
5. **Re-run smoke test** after fixes; expected: ω_b ≈ 0.0224, n_s ≈ 0.965, log₁₀(10¹⁰A_s) ≈ 3.04, H₀ ≈ 67-72 (Planck/SH0ES interplay).

**Production runs (`run_eci_cassini.py`) are HELD until Phase 2 likelihood debug completes.**

---

## Discipline

- Hallu count: 85 → 85 (S9 + parent)
- Mistral STRICT-BAN observed
- 3 arXiv IDs live-verified: 2503.14738, 2202.04077, 1807.06209
- 6+ [TBD] markers explicitly placed (off-diagonal Planck cov, exact θ_MC, etc.)

## Files
- `desi_dr2/` — 18 files, ~72 KB
- `pantheonplus/` — 5 files, ~33 MB
- `planck_2018_compressed/` — 1 file (json)
- `SUMMARY.md` — this file

PC mirror at `/home/remondiere/data/{desi_dr2,pantheonplus,planck_2018_compressed}/`.
