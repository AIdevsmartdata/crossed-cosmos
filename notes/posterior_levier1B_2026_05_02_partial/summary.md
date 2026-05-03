# Levier #1B MCMC — Posterior Summary

**Generated:** 2026-05-02
**Chain prefix:** `/root/crossed-cosmos/mcmc/chains/eci_levier1B_run1/snapshot_2026_05_02_partial/eci_levier1B`
**Burn-in:** 30%
**Post-burnin samples:** 21731 (5518, 5503, 5396, 5314 per chain)
**Likelihoods:** Planck 2018 lowl.TT + lowl.EE + NPIPE highl CamSpec TTTEEE +
lensing.native + DESI DR2 BAO + Pantheon+ + KiDS-1000 S₈ (Gaussian prior)
**Priors:** Cassini wall ON (`|ξ_χ|·(χ₀/Mₚ)² < 6×10⁻⁶`); ACT penalty OFF
**Theory:** vanilla CLASS 3.3.4 + `eci_nmc_theory.ECINMCTheory`
**Sampled params:** 10 cosmological + 9 Planck nuisance = 19 total

---

## Cosmological parameter posteriors

| Parameter | Mean | 68% CI | 95% CI | ESS |
|---|---|---|---|---|
| H0 | 67.77342 | [67.20338, 68.35837] | [66.64742, 68.92266] | 20843 |
| omega_b | 0.02232 | [0.02223, 0.02241] | [0.02212, 0.02250] | 20843 |
| omega_cdm | 0.11806 | [0.11730, 0.11883] | [0.11665, 0.11959] | 20843 |
| n_s | 0.96656 | [0.96320, 0.97022] | [0.95968, 0.97304] | 20843 |
| logA | 3.03583 | [3.02559, 3.04623] | [3.01446, 3.05624] | 20843 |
| tau_reio | 0.05366 | [0.04882, 0.05863] | [0.04350, 0.06308] | 20843 |
| w0_fld | -0.87288 | [-0.92366, -0.82181] | [-0.97381, -0.77317] | 20843 |
| wa_fld | -0.45192 | [-0.62517, -0.26691] | [-0.79885, -0.11621] | 20843 |
| xi_chi | -0.00077 | [-0.01661, 0.01541] | [-0.02323, 0.02269] | 20843 |
| chi_initial | 0.12404 | [0.07348, 0.17408] | [0.05325, 0.19565] | 20843 |

---

## Planck nuisance parameter posteriors

(Shown for chain-health verification only; not used in cosmological interpretation.)

| Parameter | Mean | 68% CI |
|---|---|---|
| A_planck | 1.0003 | [0.9981, 1.0027] |
| amp_143 | 17.5564 | [15.6150, 19.5243] |
| amp_217 | 11.4419 | [9.5665, 13.3090] |
| amp_143x217 | 8.3190 | [6.4416, 10.1907] |
| n_143 | 1.0120 | [0.8279, 1.1921] |
| n_217 | 1.5636 | [1.1576, 1.9691] |
| n_143x217 | 1.7720 | [1.1896, 2.3524] |
| calTE | 0.9966 | [0.9929, 1.0003] |
| calEE | 0.9973 | [0.9937, 1.0008] |

---

## Discriminator: H₀ vs SH0ES

H0 = 67.77 +/- 0.58 km/s/Mpc. SH0ES: 73.04 +/- 1.04. Tension: 4.4sigma (in quadrature). Planck anchor: ~67.4 km/s/Mpc. H0 tension NOT resolved.

---

## Discriminator: ξ_χ vs zero (NMC detection)

log B_10 (Savage-Dickey KDE, bw=0.0020) = -1.45. Prior density at 0: 5.00 [1/0.2]. Posterior density at 0: 21.2658. Interpretation: weak/moderate evidence FOR LCDM over NMC. Compare to Wolf+2025 (arXiv:2504.07679): log B = 7.34 +/- 0.6 (NMC vs LCDM, Planck PR4 + DR2 BAO + Pantheon+).

**Honesty gate verdict:**
GATE FAIL — CASSINI-WIDE AND STRADDLES ZERO: The posterior straddles 0 with a 68% CI width 27x the Cassini prior width. Planck does NOT detect NMC at this run's significance. This run is consistent with a null result (Scenario C). Savage-Dickey log B_10 = -1.45.

---

## Discriminator: (w₀, w_a) vs ΛCDM

w0 = -0.873 +/- 0.051 (2.5sigma from -1). wa = -0.452 +/- 0.180 (2.5sigma from 0). Combined 2D deviation from LCDM: 3.6sigma (diagonal cov approx).

---

## Discriminator: S₈ tension

S_8 cannot be computed directly (sigma8 and/or Omega_m not in chain columns). Re-run with `derived: [sigma8, Omega_m]` in the YAML if needed. KiDS-1000 prior: S_8 = 0.766 +/- 0.02. Planck 2018 estimate: S_8 = 0.83 +/- 0.013.

---

## Scenario classification

SCENARIO C — NULL RESULT: xi_chi consistent with 0 AND H_0 does not retreat. NMC alone + Planck + KiDS does not reduce cosmological tensions at this run's significance. Confirms motivation for full Levier #1 with EDE. Renew effort on AxiCLASS shooting fix.
S_8 retreat: CANNOT EVALUATE (sigma8 not in chain; add as derived param)

---

## Bayes factor summary

| Quantity | This run | Wolf+2025 (arXiv:2504.07679) |
|---|---|---|
| log B (NMC vs ΛCDM) | -1.45 (Savage-Dickey KDE) | 7.34 ± 0.6 |
| Dataset | Planck 2018 + DESI DR2 + Pantheon+ + KiDS | Planck PR4 + DESI DR2 + Pantheon+ |
| Cassini wall | ON | not specified |
| ξ_χ prior | [-0.1, 0.1] uniform + Cassini | same range |

**Caveat:** The Savage-Dickey ratio computed here uses a 1-D Gaussian KDE and a
uniform prior density at ξ_χ=0. It approximates — but does not replace — a proper
nested sampling evidence ratio. The Wolf+2025 log B = 7.34 was computed via
MultiNest. Treat our SD estimate as a sanity check, not a precision measurement.

---

## Comparison to v5 and v50plusS8 baselines

| Run | ξ_χ 68% CI | ξ_χ constrained? | Planck? | KiDS? |
|---|---|---|---|---|
| v5 (baseline) | [-0.067, 0.066] | No | No | No |
| v50plusS8 | [-0.067, 0.068] | No | No | Yes |
| Levier #1B | [FILL_LO68, FILL_HI68] | SEE GATE | Yes | Yes |

The v50plusS8 ablation confirmed: **KiDS S₈ alone does not constrain ξ_χ.**
Any tightening seen in levier1B comes from Planck's sensitivity to G_eff(k)
in the CMB power spectrum, consistent with Wolf+2025's finding.

---

## Files produced

- `triangle_cosmo.pdf` — triangle plot (10 cosmological parameters)
- `marginals_cosmo.pdf` — 1-D marginals (cosmological, with tau_reio)
- `marginals_nuisance.pdf` — 1-D marginals (9 Planck nuisance parameters)
- `xi_chi_comparison.pdf` — side-by-side ξ_χ: v5 / v50plusS8 / levier1B
- `summary.tex` — LaTeX table (importable into paper)
- `summary.md` — this file

## Reproducing this analysis

```bash
python3 scripts/analysis/posterior_levier1B.py \
    --chain-prefix /root/crossed-cosmos/eci_levier1B \
    --burnin 0.30 \
    --outdir notes/posterior_levier1B_2026-05-02
```

See `notes/posterior_levier1B_README.md` for full interpretation guide.
