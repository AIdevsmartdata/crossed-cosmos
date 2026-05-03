# Levier #1B MCMC — Posterior Summary

**Generated:** 2026-05-03
**Chain prefix:** `/root/crossed-cosmos/mcmc/chains/eci_levier1B_run1/snapshot_2026_05_03_FINAL/eci_levier1B`
**Burn-in:** 30%
**Post-burnin samples:** 48360 (12250, 12159, 12007, 11944 per chain)
**Likelihoods:** Planck 2018 lowl.TT + lowl.EE + NPIPE highl CamSpec TTTEEE +
lensing.native + DESI DR2 BAO + Pantheon+ + KiDS-1000 S₈ (Gaussian prior)
**Priors:** Cassini wall ON (`|ξ_χ|·(χ₀/Mₚ)² < 6×10⁻⁶`); ACT penalty OFF
**Theory:** vanilla CLASS 3.3.4 + `eci_nmc_theory.ECINMCTheory`
**Sampled params:** 10 cosmological + 9 Planck nuisance = 19 total

---

## Cosmological parameter posteriors

| Parameter | Mean | 68% CI | 95% CI | ESS |
|---|---|---|---|---|
| H0 | 67.66824 | [67.10298, 68.24595] | [66.54783, 68.77703] | 46411 |
| omega_b | 0.02233 | [0.02223, 0.02242] | [0.02214, 0.02251] | 46411 |
| omega_cdm | 0.11805 | [0.11734, 0.11878] | [0.11661, 0.11949] | 46411 |
| n_s | 0.96657 | [0.96310, 0.97007] | [0.95959, 0.97328] | 46411 |
| logA | 3.03556 | [3.02518, 3.04604] | [3.01472, 3.05654] | 46411 |
| tau_reio | 0.05333 | [0.04863, 0.05824] | [0.04346, 0.06304] | 46411 |
| w0_fld | -0.86367 | [-0.91526, -0.81425] | [-0.96471, -0.76777] | 46411 |
| wa_fld | -0.47226 | [-0.65416, -0.28874] | [-0.82835, -0.12660] | 46411 |
| xi_chi | -0.00003 | [-0.01638, 0.01632] | [-0.02296, 0.02272] | 46411 |
| chi_initial | 0.12490 | [0.07478, 0.17544] | [0.05443, 0.19597] | 46411 |

---

## Planck nuisance parameter posteriors

(Shown for chain-health verification only; not used in cosmological interpretation.)

| Parameter | Mean | 68% CI |
|---|---|---|
| A_planck | 1.0005 | [0.9980, 1.0030] |
| amp_143 | 17.5086 | [15.5447, 19.4296] |
| amp_217 | 11.3886 | [9.5178, 13.2331] |
| amp_143x217 | 8.2741 | [6.3936, 10.1018] |
| n_143 | 1.0189 | [0.8453, 1.1969] |
| n_217 | 1.5784 | [1.1883, 1.9792] |
| n_143x217 | 1.8067 | [1.2338, 2.3833] |
| calTE | 0.9967 | [0.9931, 1.0003] |
| calEE | 0.9975 | [0.9939, 1.0011] |

---

## Discriminator: H₀ vs SH0ES

H0 = 67.67 +/- 0.57 km/s/Mpc. SH0ES: 73.04 +/- 1.04. Tension: 4.5sigma (in quadrature). Planck anchor: ~67.4 km/s/Mpc. H0 tension NOT resolved.

---

## Discriminator: ξ_χ vs zero (NMC detection)

log B_10 (Savage-Dickey KDE, bw=0.0017) = -1.37. Prior density at 0: 5.00 [1/0.2]. Posterior density at 0: 19.6541. Interpretation: weak/moderate evidence FOR LCDM over NMC. Compare to Wolf+2025 (arXiv:2504.07679): log B = 7.34 +/- 0.6 (NMC vs LCDM, Planck PR4 + DR2 BAO + Pantheon+).

**Honesty gate verdict:**
GATE FAIL — CASSINI-WIDE AND STRADDLES ZERO: The posterior straddles 0 with a 68% CI width 27x the Cassini prior width. Planck does NOT detect NMC at this run's significance. This run is consistent with a null result (Scenario C). Savage-Dickey log B_10 = -1.37.

---

## Discriminator: (w₀, w_a) vs ΛCDM

w0 = -0.864 +/- 0.050 (2.7sigma from -1). wa = -0.472 +/- 0.180 (2.6sigma from 0). Combined 2D deviation from LCDM: 3.8sigma (diagonal cov approx).

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
| log B (NMC vs ΛCDM) | -1.37 (Savage-Dickey KDE) | 7.34 ± 0.6 |
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
    --outdir notes/posterior_levier1B_2026-05-03
```

See `notes/posterior_levier1B_README.md` for full interpretation guide.
