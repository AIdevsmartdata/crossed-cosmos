# ECI MCMC v5 Posterior Summary

**Generated:** 2026-05-02
**Chain prefix:** `/root/crossed-cosmos/mcmc/chains/eci_v50plusS8_run1/output_2026_05_02/eci_v50plusS8`
**Burn-in:** 30%
**Post-burnin samples:** 17859 (4400, 4561, 4524, 4374 per chain)
**Likelihoods:** DESI DR2 BAO + Pantheon+
**Theory:** vanilla CLASS 3.3.4 + ECINMCTheory plugin (quasi-static NMC postprocessing)
**Sampled parameters:** 9 (H0, omega_b, omega_cdm, n_s, logA, w0_fld, wa_fld, xi_chi, chi_initial)

---

## Parameter posteriors

| Parameter | Mean | 68% CI | 95% CI |
|---|---|---|---|
| H0 | 66.74955 | [65.36127, 67.65212] | [65.36127, 67.65212] |
| omega_b | 0.02236 | [0.02177, 0.02369] | [0.02177, 0.02369] |
| omega_cdm | 0.11255 | [0.10788, 0.11833] | [0.10788, 0.11833] |
| n_s | 0.96881 | [0.92203, 0.99372] | [0.92203, 0.99372] |
| logA | 2.98961 | [2.90299, 3.07045] | [2.90299, 3.07045] |
| w0_fld | -0.86006 | [-0.88295, -0.84372] | [-0.88295, -0.84372] |
| wa_fld | -0.22519 | [-0.36078, -0.11768] | [-0.36078, -0.11768] |
| xi_chi | 0.00081 | [-0.06750, 0.06927] | [-0.09546, 0.09565] |
| chi_initial | 0.12374 | [0.07160, 0.17608] | [0.05313, 0.19588] |

---

## Per-parameter prior-dominated assessment

- **H0** ($H_0$ [km/s/Mpc]): pdom_score=0.36 [WEAKLY INFORMATIVE], ESS≈11817, mean=66.7495, 68% CI=[65.3613, 67.6521]
- **omega_b** ($\Omega_b h^2$): pdom_score=0.36 [WEAKLY INFORMATIVE], ESS≈11817, mean=0.0224, 68% CI=[0.0218, 0.0237]
- **omega_cdm** ($\Omega_c h^2$): pdom_score=0.23 [WEAKLY INFORMATIVE], ESS≈11817, mean=0.1126, 68% CI=[0.1079, 0.1183]
- **n_s** ($n_s$): pdom_score=0.23 [WEAKLY INFORMATIVE], ESS≈11817, mean=0.9688, 68% CI=[0.9220, 0.9937]
- **logA** ($\ln(10^{10}A_s)$): pdom_score=0.36 [WEAKLY INFORMATIVE], ESS≈11817, mean=2.9896, 68% CI=[2.9030, 3.0704]
- **w0_fld** ($w_0$): pdom_score=0.36 [WEAKLY INFORMATIVE], ESS≈11817, mean=-0.8601, 68% CI=[-0.8829, -0.8437]
- **wa_fld** ($w_a$): pdom_score=0.23 [WEAKLY INFORMATIVE], ESS≈11817, mean=-0.2252, 68% CI=[-0.3608, -0.1177]
- **xi_chi** ($\xi_\chi$): pdom_score=0.00 [PRIOR-DOMINATED], ESS≈11817, mean=0.0008, 68% CI=[-0.0675, 0.0693]
- **chi_initial** ($\chi_\mathrm{ini}$): pdom_score=0.00 [PRIOR-DOMINATED], ESS≈11817, mean=0.1237, 68% CI=[0.0716, 0.1761]

---

## Discriminator: H0 vs SH0ES tension

H0 posterior: 66.75 +/- 0.86 km/s/Mpc. SH0ES anchor: 73.04 +/- 1.04. Tension: 4.7σ (in quadrature).

Whether H0 has shifted toward resolving the Hubble tension (SH0ES: 73.04 +/- 1.04)
must be read from the posterior mean and its displacement relative to both the
Planck/BAO anchor (~67.4) and the SH0ES anchor. Without CMB in this run, H0 is
constrained primarily by the BAO angular scale (the acoustic scale angle theta_s
is degenerate with H0*r_d), so expect a broad H0 posterior. A shift toward 73
would be surprising without CMB data to fix r_d independently. If H0 is near
the Planck/BAO anchor and xi_chi does not shift it noticeably, this 9-param run
is consistent with null ECI effect on H0, as expected at this dataset level.

---

## Discriminator: xi_chi vs Cassini hard wall

xi_chi posterior: mean = 0.0008, 68% CI = [-0.0675, 0.0693], 95% CI = [-0.0955, 0.0956]. Fraction of posterior weight with |xi_chi| > 0.024 (Cassini wall): 76.1%. Prior-dominated score: 0.00 (0=flat=prior-dominated, 1=strongly informative).

**Honest interpretation:**
xi_chi posterior is broadly consistent with zero (< 3 sigma detection). The data weakly prefer xi_chi near zero but do not rule out NMC couplings within the sampled range.

**Key benchmark:** Wolf+2025 (arXiv:2504.07679) report log B = 7.34 +/- 0.6
for NMC vs LCDM using Planck PR4 + DR2 BAO + Pantheon+. That strong Bayes factor
came from Planck's sensitivity to G_eff modifications in the CMB power spectrum,
not from BAO+SN alone. This 9-param run lacks Planck and should therefore NOT
be expected to reproduce that Bayes factor. If the Savage-Dickey BF from this
run is near 1 (inconclusive), that is fully consistent with Wolf+2025, not in
contradiction with it.

---

## Discriminator: (w0, wa) vs LCDM

w0 = -0.860 +/- 0.014 (LCDM=-1: 9.7σ). wa = -0.225 +/- 0.093 (LCDM=0: 2.4σ). 2D consistency with (-1,0): 1σ: NO (combined 10.0σ), 2σ: NO (combined 10.0σ), 3σ: NO (combined 10.0σ). NOTE: this uses a diagonal covariance; compute proper contour from triangle plot.

**Context:** w0 deviates from -1 by 9.7 sigma (marginally); wa deviates from 0 by 2.4 sigma. This is consistent with the DESI DR2 preference for dynamical dark energy reported by the DESI collaboration. The NMC correction wa_nmc_correction is a derived quantity; check its posterior mean and whether it shifts wa_fld appreciably.

---

## Honest verdict: is this run informative?

Parameters tightly constrained (posterior meaningfully narrower than prior):
**(none strongly constrained)**

Parameters essentially prior-dominated (posterior covers >80% of prior width):
**xi_chi, chi_initial**

If xi_chi and chi_initial are prior-dominated: this is the expected outcome for
DESI DR2 BAO + Pantheon+ without CMB. These likelihoods primarily constrain the
expansion history (H0, omega_m, w0, wa) and are nearly insensitive to the NMC
coupling xi_chi (which modifies G_eff in the growth sector). The run serves as a
valid sanity check and a starting point for the Levier #1 production run, but
should not be cited as evidence for or against ECI without CMB data.

If the chains show very low ESS (< 100) for any parameter, the sampler has not
explored the posterior well. An R-1 below 0.02 is necessary but not sufficient;
check per-parameter ESS and visual chain traces before drawing conclusions.

---

## Implications for Levier #1 (12-parameter run)

**Context:** Levier #1 adds 3 EDE parameters (f_EDE, log10z_c, theta_i) and the
Dark Dimension parameter c'_DD to the 9 parameters here, plus includes Planck PR4
TTTEEE+lensing and KiDS-1000 S8 data. See `notes/calculation_triage_2026_05_02.md`
section A1 for the full discriminator criteria.

### What this 9-param run tells us about the 12-param prior space

**Tightly constrained directions (already settled):** (none strongly constrained)
These parameters are unlikely to shift dramatically when EDE and c'_DD are added,
because their constraint comes from BAO+SN which will remain in Levier #1. Adding
Planck will tighten omega_b, n_s, and logA substantially (expected factor ~5-10x
reduction in posterior width for those parameters).

**Prior-dominated directions (will be constrained by new data):** xi_chi, chi_initial
These are precisely the parameters where Planck and KiDS-1000 add information:
- **xi_chi**: CMB is sensitive to G_eff(k) modifications in the growth sector.
  Wolf+2025's log B = 7.34 came almost entirely from Planck. Expect a factor ~3-10x
  tighter constraint on xi_chi once Planck is included.
- **chi_initial**: Weakly constrained by BAO+SN; Planck's ISW and lensing power
  provide some sensitivity. Expect modest improvement.
- **logA**: Without CMB, amplitude is unconstrained by BAO+SN; Planck fixes it to
  ~0.014 precision.

### New parameters in Levier #1

- **f_EDE**: Expected to be constrained by Planck (both the pre-recombination
  energy injection and its effect on the acoustic scale). DESI DR2 BAO alone is
  insensitive to f_EDE < 0.1. If the Levier #1 run recovers f_EDE < 0.05 at 2 sigma,
  the EDE sector is not needed and Levier #1 reduces to the NMC+LCDM case.
- **log10z_c, theta_i**: Prior-dominated until Planck is included.
- **c'_DD**: Constrained indirectly via Delta_N_eff correction. ACT DR6 bound
  Delta_N_eff < 0.13 (3 sigma) must be satisfied. The N2 simplified estimator
  (numerics/N2-kk-neff.py) flags all c'=0.05 cases as excluded under the thermal
  estimator; the Levier #1 run will test whether the Boltzmann treatment rescues
  this. If the posterior for c'_DD is rail-limited against the prior boundary,
  stop Levier #1 and address the N4 Boltzmann freeze-in calculation first (EXPLORE-A A4).

### Compute worthiness assessment

If (w0, wa) in this 9-param run are already > 2 sigma from (-1, 0), and if
xi_chi shows even a weak preference away from zero (pdom_score > 0.3), the
Levier #1 production run is justified: there is a signal direction to pursue.

If both xi_chi and (w0, wa) are consistent with LCDM at 1 sigma and the ESS for
the NMC parameters is very high (> 500) indicating the sampler is exploring a
flat surface, then Levier #1 is a speculative investment: the compute is justified
only if you accept the prior probability that Planck will reveal NMC effects hidden
from BAO+SN. The Wolf+2025 empirical anchor (log B = 7.34) is the strongest
external argument in favour of spending that compute.

**Recommendation:** Run Levier #1 only after verifying (a) R-1 < 0.02 in this
9-param run, (b) ESS > 200 for all parameters, and (c) chain traces look stationary.
Do not upgrade to 12 parameters on a chain that has not converged at 9.

---

## Files produced

- `triangle.pdf` — triangle plot (all 9 sampled parameters)
- `marginals.pdf` — 1-D marginals with flat prior overlay
- `summary.tex` — LaTeX table (importable directly into paper)
- `summary.md` — this file

## Reproducing this analysis

```bash
python scripts/analysis/posterior_v5.py \
    --chain-prefix /path/to/eci \
    --burnin 0.30 \
    --outdir notes/posterior_v5_2026-05-02
```

See `notes/posterior_v5_README.md` for full options.
