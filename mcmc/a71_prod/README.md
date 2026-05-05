# A71 — ECI vs LCDM Framing B: NUTS Pipeline

**Status:** Files written on VPS 2026-05-05. Smoke test pending on PC RTX 5060 Ti.

## Overview

NUTS via numpyro + cosmopower-jax A25 emulator. Framing B only (CPL-effective phenomenological, no KG ODE gate).

## Prerequisites (PC only)

1. Python venv: `/home/remondiere/crossed-cosmos/.venv-mcmc-bench/`
2. Emulator pkls (A25):
   - `/home/remondiere/pc_calcs/cosmopower_nmc_emulator/nmc_kg_w.pkl`
   - `/home/remondiere/pc_calcs/cosmopower_nmc_emulator/nmc_kg_logH.pkl`
3. JAX named_shape patch applied (see `reference_jax_patch.md`; applied automatically at import)
4. Packages: `numpyro`, `jax`, `cosmopower-jax==0.5.5`, `numpy`

## Module layout

| File | Role | Lines |
|---|---|---|
| `emulators.py` | cosmopower-jax pkl loader + JAX patch | ~155 |
| `priors.py` | numpyro prior definitions | ~120 |
| `background.py` | Pure-JAX CPL H(z), chi(z), r_d, CPL fit | ~185 |
| `likelihoods.py` | DESI DR2 BAO + Pantheon+ + Planck compressed | ~340 |
| `numpyro_models.py` | lcdm_model, cpl_model, eci_cassini_cpl_model | ~200 |
| `smoke_test.py` | LCDM smoke test (4×1000×1000) | ~195 |
| `run_eci_cassini.py` | ECI production run (4×8000×4000) | ~185 |

## Quickstart (from PC repo root)

```bash
source .venv-mcmc-bench/bin/activate

# 1. Verify emulator import (must pass before smoke test)
python -c "import mcmc.a71_prod.emulators"

# 2. Smoke test (LCDM only, 4×1000×1000, ~5-15 min)
python -m mcmc.a71_prod.smoke_test --chains 4 --warmup 1000 --samples 1000

# 3. Production ECI run (4×8000×4000, ~2-4h)
python -m mcmc.a71_prod.run_eci_cassini \
  --chains 4 --warmup 4000 --samples 8000 \
  --output /home/remondiere/pc_calcs/A71/eci_run_01/
```

## [TBD] gaps — must address before production

1. **[TBD: locate real DESI DR2 data]** — `/home/remondiere/data/desi_dr2/` does not exist on PC.
   Currently using hardcoded values from Table 1 of arXiv:2503.14738. Confirm exact numerical values
   against paper before final run. Full covariance matrix (off-diagonal between bins) not yet implemented.

2. **[TBD: locate Pantheon+ data]** — `/home/remondiere/data/` does not exist on PC.
   Currently using synthetic SNe data (200 SN, sigma_mu=0.15). Replace with real Pantheon+ mu_obs + cov_inv.

3. **[TBD: Planck 2018 compressed covariance]** — `PLANCK2018_COV_APPROX` in likelihoods.py uses
   approximate diagonal + main off-diag values. Use exact covariance from PLA chains R3.01.

4. **[TBD: theta_MC approximation]** — `theta_MC_approx()` in likelihoods.py is a rough scaling relation.
   Replace with CLASS/CAMB-computed theta_* or a dedicated emulator for final run.

5. **[TBD: ACT DR6 lensing]** — loglike_act_dr6_lensing not yet implemented. Madhavacheril et al. 2024
   arXiv ID and A_lens values not yet live-verified. Add as 4th likelihood term.

6. **[TBD: ECI emulator lambda range]** — A25 training range λ ∈ [0.05, 3.0]; prior goes to 4.0.
   Either trim prior to [0.5, 3.0] or retrain emulator with λ ∈ [0.5, 4.5].

7. **[TBD: H0 consistency between ECI emulator and sampled H0]** — `eci_cassini_cpl_model` samples H0
   from prior independently. Should be linked to emulator H(z=0) output. See comment in numpyro_models.py.

8. **[TBD: chain_method fallback]** — If `parallel` fails on GPU (named_shape errors), set
   `--chain-method sequential`. Automatic fallback is coded for smoke_test.py.

9. **[TBD: Cooke et al. 2018 BBN prior]** — omega_b prior uses mean=0.02218, sigma=0.00055. Verify
   exact reference (Cooke, Pettini, Steidel 2018 — no arXiv ID live-verified; do not cite without check).

10. **[TBD: Aubourg 2015 arXiv:1411.1074 r_d formula]** — sound_horizon_EH() uses Aubourg et al. 2015
    fitting formula. Live-verify arXiv:1411.1074 before citing in paper (VPS API available).

## arXiv IDs confirmed (live, 2026-05-05)

- Brout et al. 2022 Pantheon+ cosmological constraints: **arXiv:2202.04077**
- Aghanim et al. 2018 Planck 2018 VI cosmological parameters: **arXiv:1807.06209**
- DESI DR2 BAO: **arXiv:2503.14738**

## Hallu discipline

Hallu count: 85 entering → 85 leaving. Mistral STRICT-BAN observed.
No new arXiv IDs fabricated. All uncertain references marked [TBD].
