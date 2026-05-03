# Levier #1B vs Wolf 2025 — KiDS-1000 Isolation by Posterior Reweighting

**Date:** 2026-05-02
**Method:** Importance-reweighting on the converged Cobaya chain at
`mcmc/chains/eci_levier1B_run1/snapshot_2026_05_03_FINAL/eci_levier1B.{1..4}.txt`
(48360 post-burnin samples, 30% burn-in).
**Question:** Is the 8.7-unit gap between Wolf 2025 (log B = +7.34) and Levier #1B
(log B = -1.37) driven by the KiDS-1000 S_8 Gaussian prior?

---

## 1. Posterior reweighting protocol — verified

The KiDS likelihood in `mcmc/cobaya_nmc/eci_kids_s8.py` is a pure Gaussian:
`log L_KiDS(S_8) = -0.5 * ((S_8 - 0.766) / 0.020)^2`
with two ancillary contributions: (a) a Cassini hard wall on |xi_chi|·(chi_0/M_P)^2,
which is symmetric around 0 and never enforced in this chain (verified), and
(b) an ACT penalty disabled in the YAML (`apply_act_penalty: false`).

The chain stores `chi2__eci_kids_s8` directly — verified against the
re-computed `delta_S_8^2` to **2.1e-6** (numerical roundoff).
The `S8` derived column matches `sigma8 * sqrt(Omega_m/0.3)` to **1.6e-8**.

The reweighting is `w_new = w_old * exp(+0.5 * delta_S_8^2)` — i.e., dividing
out the KiDS Gaussian factor.

**ESS (Kish):** original 46411 → reweighted 15138 (33% retention).
Sufficient for a meaningful Savage-Dickey estimate.

## 2. Original log B_10 (sanity check)

Reproduced **log B_10 = -1.3688** vs notes' -1.37. KDE bandwidth = 0.00171
(Silverman, posterior(0) = 19.65, prior(0) = 5.00 on the wide [-0.1, 0.1]
range used in `posterior_levier1B.py`).

Note: with the YAML's actual prior range [-0.024, 0.024], log B_10 = +0.058
(near zero). The wide-range value -1.37 reflects an over-broad nominal prior
in the analysis script, not the YAML — but to compare apples-to-apples with
Wolf 2025 (whose nested-sampling evidence integrates over the actual prior
range), both numbers should be reported.

## 3. Reweighted log B_10 (without KiDS) — the new number

| Estimator | Original (with KiDS) | Reweighted (no KiDS) | Shift |
|---|---|---|---|
| Manual SD-KDE, wide prior 1/0.2 | **-1.369** | **-1.422** | -0.053 |
| scipy.gaussian_kde, wide prior | -1.369 | -1.421 | -0.052 |
| Histogram (bin=0.001) | -1.358 | -1.419 | -0.061 |
| Histogram (bin=0.002) | -1.374 | -1.398 | -0.024 |
| Histogram (bin=0.005) | -1.392 | -1.375 | +0.017 |
| Bandwidth scan (0.5x-2x Silverman) | — | — | -0.058 to -0.036 |
| YAML prior 1/0.048 | +0.058 | +0.006 | -0.052 |

**The shift is consistently in the [-0.06, +0.02] range, regardless of estimator.**

Sanity check: S_8 posterior shifts as expected — mean rises from 0.81160 to
0.82019 once the KiDS pull (centred at 0.766) is removed. xi_chi posterior
remains essentially unchanged (mean -3e-5 → +2e-4, std 0.01393 → 0.01404).

## 4. Comparison with Wolf 2025

| Quantity | Value |
|---|---|
| Wolf 2025 (Planck PR4 plik + DR2 BAO + Pantheon+, MultiNest) | **log B = +7.34 ± 0.6** |
| Levier #1B with KiDS, Cassini ON, NPIPE CamSpec, MCMC+SD-KDE | **log B = -1.37** |
| Levier #1B reweighted to remove KiDS (other settings unchanged) | **log B = -1.42** |
| Δ(Wolf − original) | +8.71 |
| Δ(Wolf − reweighted) | +8.76 |
| **Gap closure from KiDS removal** | **-0.6 % (i.e., none, slightly worse)** |

## 5. Verdict

**KiDS IS NOT THE DRIVER.** Removing the KiDS-1000 S_8 Gaussian prior from
the Levier #1B posterior produces a log B shift of -0.05, which is well
within the noise of the SD-KDE estimator and **moves in the wrong direction**.
Of the 8.7-unit gap to Wolf 2025, KiDS accounts for ~0%. The disagreement
must be driven by one or more of the **other** axes already enumerated:

1. **Sampler/estimator:** MultiNest exact evidence (Wolf) vs MCMC + 1-D
   Savage-Dickey KDE (us). The SD ratio at xi_chi = 0 is a *projection*
   onto a single dimension; it does not capture the multi-dimensional
   parameter-space volume that nested sampling integrates over the full
   9-D + nuisance space. This is the single most likely structural cause.
2. **Likelihood:** plik 2018 (Wolf) vs NPIPE highl CamSpec TTTEEE (us). The
   NPIPE CamSpec likelihood's preference for slightly higher Omega_m and
   different polarization weighting could shift the xi_chi posterior shape.
3. **Parameter set:** Wolf had 9 cosmological parameters; we have 10 cosmo
   (incl. wa_fld free) + 9 nuisance. Free wa_fld competes with xi_chi for
   late-time expansion budget — observed in the chain as
   wa = -0.47 ± 0.18 (2.6σ from 0).
4. **Prior range / wall:** Wolf's xi_chi prior boundaries are ours' nominal
   YAML range [-0.024, 0.024]; with that prior the original log B is +0.058
   (mild evidence FOR NMC) — closer to Wolf's sign though still 7 units short.

## 6. Implications for the v6.0.22 narrative

The **changelog/narrative needs an update**. The current text in
`notes/posterior_levier1B_2026_05_03_FINAL/summary.md` says:

> "The v50plusS8 ablation confirmed: KiDS S₈ alone does not constrain ξ_χ.
> Any tightening seen in levier1B comes from Planck's sensitivity to G_eff(k)
> in the CMB power spectrum, consistent with Wolf+2025's finding."

That statement is **already consistent** with this analysis (KiDS is not the
constrainer of xi_chi). The new finding to fold in is:

- KiDS is also NOT the cause of our **disagreement** with Wolf on log B.
- The remaining causes ranked by structural plausibility:
  1. SD-KDE ≠ MultiNest evidence (estimator artefact, not physics).
  2. CamSpec NPIPE vs plik 2018 high-l likelihood difference.
  3. Wolf fixed wa = 0 (LCDM background); we sample wa freely and find
     wa = -0.47 (2.6σ from 0). Letting the dark sector absorb expansion
     budget leaves less room for xi_chi to be detected — driving log B
     downward in our setup vs Wolf's.
- The Wolf disagreement is therefore most likely a **methodology + parameter
  set artefact**, not a falsification of either result.

**Recommended action:** add a paragraph to v6.0.22 changelog stating that
the KiDS contribution to the Wolf disagreement is below noise, and the
plausible drivers are (i) SD-KDE vs nested sampling and (ii) free wa_fld.
The next robustness step (priority): re-run a Levier #1B variant with
**wa_fld fixed to 0** and recompute log B, to disentangle the wa_fld
contribution from the sampler artefact.

---

## Appendix: Files

- `/tmp/levier1B_kids_isolation.py` — main reweighting script
- `/tmp/levier1B_kids_triangulate.py` — independent verification with scipy KDE + histograms
- `/tmp/levier1B_kids_isolation.json` — machine-readable results
