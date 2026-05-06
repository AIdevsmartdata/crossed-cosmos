---
name: M56 Nested-sampling Pipeline B v2 — script ready, NOT auto-launched
description: Paper-grade dynesty/ultranest nested sampling pipeline b v2 (replaces M50 harmonic-mean biased Bayes factor). 755-line script. ETA 3-5h fast / 10-18h publication. Don't launch until M50 NUTS atterrit. Hallu 86 unchanged
type: project
---

# M56 — Nested-sampling Pipeline B v2 (Phase 4 prep, Sonnet, ~5min)

**Date:** 2026-05-06
**Owner:** Sub-agent M56 (Sonnet)
**Hallu count:** 86 → 86 (held; no fab; published API signatures only)

## Files written

- `/root/crossed-cosmos/notes/eci_v7_aspiration/M56_NESTED_SAMPLING/pipeline_b_v2_nested_sampling.py` — 755 lines, AST OK
- `/root/crossed-cosmos/notes/eci_v7_aspiration/M56_NESTED_SAMPLING/dispatch_v2.md` — launch instructions

## Why nested sampling > harmonic-mean

- Newton & Raftery 1994: harmonic-mean estimator
- Murray & Aitkin 1999 *Biometrika*: harmonic-mean has INFINITE variance in general — one low-likelihood tail sample arbitrarily inflates log Z
- Skilling 2006 *Bayesian Analysis* 1:833: nested sampling gives log Z with O(1/√n_live) uncertainty
- M50 smoke log_BF = +14732 is **numerical artefact**, NOT a result

## Sampler choice

- **dynesty 2.x** (Speagle 2020, MNRAS 493:3132): DynamicNestedSampler, multi-ellipsoid bounds, slice/random-walk sampling
- **ultranest** (Buchner 2021, JOSS 4(42):3001, arXiv:2101.09604): ReactiveNestedSampler, MLFriends + RegionSampler, more conservative

Script supports both via `--sampler dynesty|ultranest` flag.

## JAX compatibility

Neither package has JAX support. Likelihood wrapped as pure-numpy callable. cosmopower-jax bypassed in NS path; uses EH+KMJ+numpy. GPU not used (multiprocessing.Pool cannot fork CUDA safely).

## Script design

| Component | Approach |
|---|---|
| Data loaders | Reused verbatim from v77 (Tristram 2024 PR4 diag, DESI DR2 7-bin, Pantheon+ N=1701, KiDS S_8) |
| Prior transform | scipy.special.ndtri for Gaussian priors |
| Likelihood | Pure-numpy `_loglike_numpy`; -inf for unphysical H² < 0 (Wolf ξ=2.31 at high z) |
| Module-level wrappers | `_loglike_global` / `_prior_transform_global` picklable for Pool |
| Output | HDF5 via h5py: posterior samples + log_Z + log_Z_err for both variants + propagated log_BF |

## Honest scope (carries M50 caveats forward)

NS does NOT fix:
1. θ_* EH+KMJ bias (M50)
2. Wolf KG ODE not integrated (still distance-only contest)
3. Diagonal-only PR4 covariance
4. KiDS linear approximation for σ_8

What NS DOES fix:
- Replaces harmonic-mean biased log_Z with paper-grade unbiased log_Z + uncertainty
- Provides reliable log_BF (publication-quality)

## Runtime + launch decision

| Mode | n_live | dlogz | CPU | ETA |
|---|---|---|---|---|
| Smoke | 50 | 2.0 | 1 | ~10 min |
| Fast | 500 | 0.5 | 18 | ~3-5h |
| Publication | 1000 | 0.1 | 18 | ~10-18h |

**Do NOT launch** until M50 NUTS (tmux v77ecicontest) has landed.

Install: `pip install dynesty h5py` in venv first.

## Discipline log
- Mistral STRICT-BAN observed
- WebFetch blocked → used stable published API signatures
- 0 new fabrications
- All data references reused verbatim from M47/M50 (Tristram 2024, DESI 2025, Brout 2022, Asgari 2020)
- Sub-agent return-as-text protocol used (parent saved)
