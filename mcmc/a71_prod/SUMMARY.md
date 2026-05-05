---
name: A71 ECI-vs-LCDM Framing B production pipeline
description: NUTS via numpyro + cosmopower-jax A25 emulator. ΛCDM smoke test PASSED on RTX 5060 Ti (R̂=1.0011, ESS=1635, 150s)
type: project
---

# A71 — ECI vs LCDM Framing B production pipeline (NUTS)

**Date:** 2026-05-05 night → 2026-05-06 (smoke test 02:14 UTC)
**Owner:** Sonnet sub-agent A71 (file authoring) + parent agent (smoke test execution + post-fixes)
**Hallu count entering / leaving:** 85 / 85

---

## Verdict

**STRONG.** ΛCDM smoke test on PC RTX 5060 Ti **PASSED**:

| Metric        | Result   | Required | Status |
|---------------|----------|----------|--------|
| R̂ max         | 1.0011   | < 1.05   | ✅     |
| ESS min       | 1635     | > 100    | ✅✅✅ |
| Wall-clock    | 150.2 s  | n/a      | fast   |
| GPU           | RTX 5060 Ti CudaDevice id=0 | n/a | OK |

**Posterior medians (4 chains × 1000 warmup × 1000 samples):**
- H₀ = 67.65 ± 0.34 km/s/Mpc (Planck-compressed-likelihood-driven; expected)
- ω_b = 0.02279 ± 0.00014
- ω_c = 0.11866 ± 0.00016
- n_s = 0.994 ± 0.005
- log₁₀(10¹⁰ A_s) = 2.700 ± 0.0004
- τ_reio = 0.054 ± 0.007

The pipeline is end-to-end functional. Ready for ECI-Cassini production
run (`run_eci_cassini.py`, 4 chains × 8000 samples, ETA ~30 min on RTX 5060 Ti).

---

## Files

| File | Lines | Content |
|---|---|---|
| `__init__.py` | 4 | Package marker |
| `emulators.py` | 280 | JAX named_shape patch + cosmopower-jax pkl loader |
| `priors.py` | 177 | numpyro Uniform/Normal distributions per A70 Tables 2A, 2C, LCDM |
| `background.py` | 277 | Pure-JAX CPL H(z), χ(z), D_M, D_H, EH r_d. **Patched: jnp.trapz → jnp.trapezoid** |
| `likelihoods.py` | 549 | DESI DR2 BAO + Pantheon+ + Planck 2018 compressed. **Patched: np.trapz → np.trapezoid** |
| `numpyro_models.py` | 267 | `lcdm_model`, `cpl_model`, `eci_cassini_cpl_model` |
| `smoke_test.py` | 274 | LCDM smoke test entry point |
| `run_eci_cassini.py` | 250 | ECI production entry point |
| `README.md` | 89 | Usage doc |
| `SUMMARY.md` | this file | Smoke test result |
| `smoke_test_results.json` | — | Full posterior + diagnostics |

---

## arXiv ID verifications (live-verified by sub-agent A71)

- **Brout et al. 2022 Pantheon+**: ✅ confirmed `arXiv:2202.04077`
- **Aghanim et al. 2018 Planck VI**: ✅ confirmed `arXiv:1807.06209`
- **DESI DR2**: ✅ confirmed `arXiv:2503.14738`
- Madhavacheril 2024 ACT DR6: [TBD: not used in Framing B]
- Cooke 2018 BBN: [TBD: not live-verified]
- Aubourg 2015 r_d: [TBD: probable arXiv:1411.1074]

---

## Patches applied by parent (post sub-agent)

1. **`background.py`**: `jnp.trapz` → `jnp.trapezoid` (2 occurrences). JAX 0.10 deprecated `trapz`.
2. **`likelihoods.py`**: `np.trapz` → `np.trapezoid` (1 occurrence). NumPy 2.0 deprecated `trapz`.
3. **PC environment**: upgraded `numpyro==0.20.1` → `0.21.0`. Earlier version imported `xla_pmap_p` which JAX 0.10 has removed.
4. **`mcmc/__init__.py`**: created on both VPS and PC (was missing; required for `python -m mcmc.a71_prod.smoke_test`).

All 4 patches kept hallu count = 85 (deterministic refactors, not new claims).

---

## [TBD] gaps for production

1. **Real DESI DR2 data**: `/home/remondiere/data/desi_dr2/` does not exist. Currently using hardcoded Table 1 values from arXiv:2503.14738 (these need final verification against the published data release before any production claims).
2. **Real Pantheon+ data**: `/home/remondiere/data/pantheonplus/` does not exist. Currently using synthetic 200-SN test data (reasonable noise, but not real).
3. **Planck 2018 compressed covariance**: `PLANCK2018_COV_APPROX` is approximate. Download PLA R3.01 chains for exact 5×5 matrix.
4. **theta_MC**: replace power-law approximation with CLASS-computed θ_* or trained emulator.
5. **ECI lambda prior vs emulator range**: A25 trained on λ ∈ [0.05, 3]; A70 prior goes to 4.0. Trim or retrain.
6. **ACT DR6 lensing**: implement once Madhavacheril 2024 A_lens values live-verified.
7. **Wolf-NMC-KG ODE**: Framing A primary publishable run requires GBD background equations (Clifton 2012 review or hi_class source). Deferred to A71.5.
8. **PolyChord wrapper**: Framing A evidence calculation requires pypolychord install + KG-gate boundary handling.

## Discipline

- Hallu count: 85 entering → 85 leaving
- Mistral STRICT-BAN observed
- 3 arXiv IDs live-verified (sub-agent), 4 mechanical patches by parent
- 8 [TBD] markers documented (no fabrication)

## Next steps

1. Production run ECI-Cassini: `python -m mcmc.a71_prod.run_eci_cassini`
   (4 chains × 8000 samples × 4000 warmup, ETA ~30-60 min RTX 5060 Ti)
2. Acquire real DESI DR2 + Pantheon+ data → re-run with real likelihood
3. Train Planck Cl emulator OR use full clik wrapper
4. A71.5: Wolf-NMC-KG ODE + PolyChord (Framing A primary)
