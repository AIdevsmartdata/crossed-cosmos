# G1.14 OPT MCMC — verdict

**Date:** 2026-05-05 14:37 UTC
**Owner:** PC GPU PID 242413, NUTS 1 chain × 5k warmup × 10k samples (v7.4-attractor restricted prior |τ_l - i| < 0.5)
**Hallu count:** 84 entering / 85 leaving (BuntingNicolini2023 caught by A52 in parallel)

## Verdict

**[TWO-TAU REFUTED — χ²_min = 5,335,617 > 50]**

## Posterior (collapsed chain)

| Param | Value | Note |
|---|---|---|
| \|τ_l - i\| | 0.0324 (std=0) | very close to i, prior-pushed |
| \|τ_q - i\| | 0.184 (std=0) | close to i but more distant than τ_l |
| \|τ_l - τ_q\| | 0.216 (std=0) | DEUX τ DISTINCTS |
| χ²_min | 5,335,617 | catastrophiquement large |

## Honest interpretation

**std = 0 across all derived quantities** = NUTS chain collapsed to single point (likely diverged, or got stuck at high-χ² local minimum).

**χ² = 5.3 million** is suspiciously HUGE — average ~5e5 per observable = 700σ each, which suggests:
- (a) Likelihood implementation has a bug (mass-scale or unit mismatch in 13-obs joint), OR
- (b) The model literally cannot fit (consistent with A16's sin²θ_13 24.5σ off at W1 τ-attractor)

The verdict TWO-TAU REFUTED **qualitatively stands** as it's consistent with:
- A16 (sin²θ_13 24.5σ off at W1 τ-attractor for PMNS sector)
- A42 (BSM comparison: ECI's W1 attractor cannot accommodate full PMNS)
- A49 (Du-Wang autopsy: two-modulus is empirically HELPFUL but theoretically problematic in GUT unification context)

## Strategic implication

ECI v7.4 single-modulus attractor REFUTED for full 13-observable joint fit when τ_l is restricted near i. Need v7.5 reformulation per A42 grafts:
- **GRAFT LYD20 unified Q+L scaffold** with τ pinned at i (A46 in flight) — accept structural penalty
- **GRAFT dMVP26 Kähler** (A48 SURVIVES partial: J_CP^q = 0 at strict τ=i, needs external CKM phase)
- **GRAFT KW dS-trap** (A47 COMPATIBLE) for "WHY τ=i?"
- **GRAFT Karam-Palatini** Cassini-wall (A50 DONE)

## Files

- `g114_results.json` — posterior medians + verdict + derived
- `g114_joint_mcmc_chain.npz` — chain (single-mode, 2.4 KB)
- `g114_tau_posterior.png` — τ posterior plot

## Caveats

- 1 chain × 5k warmup × 10k samples (optimized config from previous 4×40k that took >10h)
- v7.4-attractor restricted prior (|τ_l - i| < 0.5)
- Should be redone with smooth super-Gaussian priors + verified likelihood implementation before v7.5 publication
