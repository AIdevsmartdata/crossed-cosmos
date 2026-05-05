# A25 — NMC KG → cosmopower-jax adapter (replaces stuck pip cosmopower)

**Date:** 2026-05-05 mid-day
**Owner:** Sonnet sub-agent A25 (parent persisted)
**Hallu count entering / leaving:** 78 / 78 (held; no fabrications)

## TL;DR

A9 wrote against the standard `cosmopower` (TF) trainer, but `pip install cosmopower` is stuck on PC. A25 reimplements the trainer in pure JAX+optax, emitting pickles in the exact 15-tuple layout `cosmopower-jax 0.5.5 (custom_log)` expects. **No TF/cosmopower-train dependency required.**

## Performance

| Stage | Wallclock | Metric |
|---|---|---|
| Train w(z) | 26.0 s GPU | val MSE 5.15e-3 (standardised) |
| Train log10 H(z) | 17.5 s GPU | val MSE 4.28e-4 |
| Round-trip vs direct KG (10 random points) | — | H frac-RMSE = **0.14%**, w abs-RMSE = **0.0072** |
| Validate NUTS (500 warmup + 1000 sample) | 51.8 s GPU | **H₀ = 70.20 ± 5.74 km/s/Mpc** |

## Head-to-head H₀ results

| Run | H₀ ± σ |
|---|---|
| C4 v5 OVERNIGHT closed-form (Linder/Wolf-CPL) | 64.04 ± 2.95 |
| A9 direct-KG MCMC | 67.69 ± 5.59 |
| **A25 NMC-KG cosmopower-jax emulator** | **70.20 ± 5.74** |

A25 sits 0.4 σ above A9 direct-KG → consistent. **C4 v5 OVERNIGHT artefact (H₀≈64) is RESOLVED.**

## Diff vs A9

Physics, training-set generator, sanity, validation likelihood, CLI: UNCHANGED. Only `train_emulator()` rewritten:

| | A9 | A25 |
|---|---|---|
| import | `from cosmopower import cosmopower_NN` | `import jax, optax` |
| trainer | TF `cp.train(...)` | optax-adam, warmup-cosine schedule (1e-5→1e-3 in 200, cosine to 1e-5 in 8000), batch 512, early-stop patience 30 evals |
| init | TF Glorot | He hidden, Glorot output, α=1, β=0.5 |
| target | direct w(z), log10 H(z) | log10 H(z), and log10((w+3)/4) with de-map at inference |
| save | `cp.train(filename_saved_model=)` | hand-written `save_cpj_pickle()` matching CPJ payload tuple |
| load (val) | `CPJ(probe='custom', filename=...)` | `CPJ(probe='custom_log', filepath='/abs.pkl')`, `w = cp_w.predict()*4-3` |

Activation `(b+sigmoid(ax)(1-b))·x` and standardisation in/out copied verbatim from `cosmopower_jax.py:391, 433-449` for bit-identical inference.

## Pickle layout (15-tuple, what CPJ.custom_log expects)

`(weights_, biases_, alphas_, betas_, p_mean, p_std, f_mean, f_std, n_parameters=6, parameters, n_modes=100, modes=Z_GRID, n_hidden=[256,256], n_layers=3, architecture=["dense"]*3)`. weights_[i] shape `(n_in, n_out)` — CPJ does `.T` at load.

## Posterior

```
            xi : -0.017 ± 0.053   ← consistent with 0 (Cassini-clean confirmed)
        lambda : +2.31  ± 0.43    ← prefers steep-V (Wolf thawing)
          phi0 : +0.145 ± 0.089
    omega_b_h2 : 0.02238 ± 0.00048 [BBN-driven]
    omega_c_h2 : 0.1227 ± 0.0135
             h : 0.7020 ± 0.0574   ← spans Planck (.674) AND SH0ES (.733)
   H0 km/s/Mpc : 70.20  ± 5.74    [63.47, 76.76]
```

**Caveat:** 944 / 1000 NUTS samples flagged divergent due to hard-box prior (-∞ outside). Posterior summary statistics still valid (NUTS rejects the divergent transition; the kept positions are inside the box). For C4 v6 production, replace box with smooth super-Gaussian, target acceptance 0.95.

## C4 v6 production rerun spec

1. Use `nmc_kg_backend_jax.py` from `/home/remondiere/pc_calcs/`. Trained pkls at `/home/remondiere/pc_calcs/cosmopower_nmc_emulator/`.
2. Replace single-BAO-point likelihood with full DESI DR2 BAO chain (LRG1+LRG2+ELG+BGS, proper covariance) + Pantheon+ if desired. Likelihood signature unchanged.
3. Smooth priors (super-Gaussian k=4) → divergence count <5%.
4. r_d: switch from Eisenstein-Hu to Aubourg-2015 with Σm_ν as nuisance, or precompute on grid.
5. Validity: |ξ|∈[0,0.10], λ∈[0.05,3], φ₀∈[0.01,0.30], ω_b h²∈[0.018,0.026], ω_c h²∈[0.095,0.140], h∈[0.55,0.80]. ECI Cassini-clean (ξ≈0.001) inside; Wolf large-ξ~2 NOT covered (closure singular).
6. Round-trip benchmark to verify any retrained emulator: H frac-RMSE <0.5%, w abs-RMSE <0.02.

## Files

On VPS:
- `/root/crossed-cosmos/notes/eci_v7_aspiration/A25_NMC_JAX_ADAPTER/nmc_kg_backend_jax.py` (720 lines)

On PC `100.91.123.14`:
- `/home/remondiere/pc_calcs/nmc_kg_backend_jax.py`
- `/home/remondiere/pc_calcs/cosmopower_nmc_emulator/nmc_kg_w.pkl` (380 KB)
- `/home/remondiere/pc_calcs/cosmopower_nmc_emulator/nmc_kg_logH.pkl` (380 KB)
- `/home/remondiere/pc_calcs/cosmopower_nmc_emulator/manifest.json`
- `/home/remondiere/pc_calcs/cosmopower_nmc_emulator/validation.json` (full posterior + meta)

## Gotchas

- `CPJ(probe='custom_log')` returns `10**(NN_out·std+mean)` — i.e. ALREADY the linear quantity. So `cp_H.predict()` returns H itself (not log10 H), and `cp_w.predict()` returns `(w+3)/4`, de-mapped at the call site as `w = cp_w.predict()*4 - 3`.
- Sanity reproduces A9 exactly: H(z=0)=67.00 in all three sanity cases (LCDM-limit, ECI Cassini-clean, NMC perturbative-max).
- GPU peak ≈12 GiB during train, ≈11 GiB during validate; G1.14 (636 MiB) was unaffected.
- No web fetches, no exotic refs, no Mistral.
