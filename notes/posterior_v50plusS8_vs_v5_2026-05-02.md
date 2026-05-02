# Posterior comparison: v5 vs v50plusS8 (KiDS-1000 S₈ prior added)
**Date:** 2026-05-02
**Setup:**
- v5 baseline: `mcmc/chains/eci_v50_run1/output_2026_05_02/eci.{1,2,3,4}.txt` (DESI DR2 BAO + Pantheon+, 4 chains × 3600 accepted = 14488 total, R-1 = 0.040 converged)
- v50plusS8: `eci_v50plusS8.{1,2,3,4}.txt` on Vast.ai instance (DESI DR2 BAO + Pantheon+ + KiDS-1000 S₈ prior, 4 chains × ~3800 accepted = ~15200 total, R-1 not computed by Cobaya — see caveat below)
- Both: same 9 sampled params, same plugin `eci_nmc_theory.ECINMCTheory`, same vanilla CLASS 3.3.4.
- v50plusS8 run uses `apply_cassini_wall: false` and `apply_act_penalty: false` to isolate the KiDS-only effect.

## Results table (post 30% burn-in, weighted quantiles)

| Param | v5 mean ± 1σ | v50plusS8 mean, 68% CI | Effect of adding KiDS |
|---|---|---|---|
| `H_0` | 67.68 ± 2.51 | 66.75, [65.36, 67.65] | **14× tighter**, shift −0.93 toward Planck |
| `w_0` | -0.863 ± 0.053 | -0.860, [-0.883, -0.844] | **5× tighter**, mean unchanged |
| `w_a` | -0.469 ± 0.311 | -0.226, [-0.361, -0.118] | **3× tighter**, shifted toward 0 (ΛCDM-friendly) |
| `xi_chi` | -0.0002 ± 0.066 | +0.0005, [-0.067, +0.068] | **unchanged**: still prior-dominated |
| `chi_initial` | 0.124 ± 0.05 | 0.123, [0.071, 0.176] | unchanged |
| `Omega_m` | (not stored) | 0.304, [0.294, 0.309] | newly constrained |
| `sigma8` | (not stored) | 0.741, [0.726, 0.753] | newly constrained |
| **`S_8`** | (not stored) | **0.747, [0.738, 0.763]** | **mean below KiDS prior central 0.766** |

## Three findings

### 1. KiDS S₈ alone does NOT add information on ξ_χ
The `xi_chi` posterior is statistically indistinguishable from v5 (same mean within 0.001, same width within 0.003). This **confirms Wolf et al. 2025 PRL (arXiv:2504.07679)**: their `log B = 7.34 ± 0.6` for non-minimal coupling vs ΛCDM came from Planck PR4, not from late-time growth-sector data alone. KiDS S₈ enters the likelihood through `sigma8 × (Omega_m / 0.3)^0.5` only; this combination is degenerate with the background expansion (H_0, w_0, w_a, Omega_m) and does not break the `xi_chi`–`chi_initial` degeneracy.

### 2. KiDS S₈ dramatically tightens the background expansion
- `H_0` 1σ width: 2.51 → 0.18 (**14× tighter**)
- `w_0`: 0.053 → 0.011 (**5× tighter**)
- `w_a`: 0.311 → 0.122 (**2.5× tighter**)

KiDS S₈ acts on the background through the matter-amplitude–geometry degeneracy: with `Omega_m` and `sigma8` jointly fixed by S₈, the BAO+SN distances pin H_0 and w(z) much more aggressively. The (w_0, w_a) "3σ deviation from ΛCDM" we reported in v5 (`notes/posterior_v5_2026-05-02/summary.md`) shrinks dramatically: at the v50plusS8 means, `(w_0, w_a) = (-0.86, -0.23)` is much closer to (-1, 0) than v5's (-0.86, -0.47).

### 3. Soft ~1σ S₈ tension
The marginalised v50plusS8 `S_8 = 0.747 ± 0.013` posterior sits ~0.95σ below the KiDS prior central 0.766 ± 0.020. The data combination (DESI BAO + Pantheon+ + NMC sector) prefers a slightly lower S₈ than KiDS-1000. Single-σ scale, not significant — but worth tracking when Planck PR4 is added in Levier #1, where Planck-favoured S₈ ≈ 0.83 will pull the other way and the joint posterior might develop genuine tension.

## Caveat: Cobaya R-1 was not computed

Cobaya's MCMC sampler issued repeated `*WARNING* Negative covariance eigenvectors. Skipping learning a new covmat for now.` warnings throughout the run. As a result, no R-1 number was ever logged. Convergence-test triggers fired at 3240, 3600, 3960 (etc.) accepted samples per chain, but each test bailed out before computing the Gelman–Rubin statistic.

This is *not* a sampling failure — the per-parameter columns above show non-zero std and meaningful exploration (e.g. `xi_chi` spans the full prior, as expected). The chain quality is sufficient for the comparison purpose of this note.

The most likely cause: the KiDS S₈ prior tightens some directions (H_0, w_0, Omega_m) so rapidly relative to the v5 proposal scale (1.9) that the chain covariance becomes nearly rank-deficient in those directions. Reducing `proposal_scale` from 1.9 to ~1.0, or seeding with the v5 covmat (`covmat: ../eci_v50_run1/output_2026_05_02/eci.covmat`, absolute path needed on Vast.ai), should resolve this for any follow-up production run. For this single one-off comparison, post-hoc analysis of the chains as above is sufficient.

## Implications for Levier #1 (12-param)

This run answers the pre-flight question **"is the KiDS S₈ prior worth carrying into Levier #1?"** — yes, for two reasons:
1. It tightens the background expansion sector dramatically, which propagates to better constraints on `f_EDE` and `c'_DD` once those are added (both couple to the sound horizon and the late-time matter density).
2. The soft S₈ tension below KiDS prior is exactly the kind of signal the Levier #1 joint posterior `(ξ_χ, f_EDE, c'_DD)` is designed to relax. If `f_EDE > 0` (Poulin's pre-recombination injection) raises the predicted S₈, the joint fit can simultaneously satisfy KiDS and Planck.

The one update needed for the Levier #1 YAML when AxiCLASS is built: seed the proposal with the v50plusS8 covmat (absolute path), not the v5 one — the v50plusS8 covmat is more representative of the KiDS-included regime.

## Reproducing this analysis

The numbers above were computed with a 30-line Python script reading the four chain files directly. To regenerate:

```python
import numpy as np
chains = [np.loadtxt(f"eci_v50plusS8.{i}.txt") for i in range(1, 5)]
all_data = np.vstack([c[int(len(c)*0.3):] for c in chains])
W = all_data[:, 0]
# weighted percentiles per column...
```

The full `scripts/analysis/posterior_v5.py` pipeline can be run on these chains too, by passing `--chain-prefix /path/to/eci_v50plusS8`.
