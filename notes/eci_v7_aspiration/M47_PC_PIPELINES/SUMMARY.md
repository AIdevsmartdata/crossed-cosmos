---
name: M47 — PC-gamer-deployable computational pipelines (F2 + v7.7 CLASS)
description: Pipeline A (F2 pure-Python sweep, ~15-30 min decisive on M13.1(c) Steinberg-specificity) + Pipeline B (v7.7 CLASS-grade θ* MCMC, GPU 2-4h, NUTS scripts only — not promised results). Pivoted from .sage to .py per CRITICAL_UPDATE_M47.md. Hallu 86 unchanged
type: project
---

# M47 — PC-gamer pipeline pack (Phase 3.G #4, Opus, ~12min)

**Date:** 2026-05-06
**Hallu count:** 86 → 86 (held; 0 new fabrications; pivot to Python caught mid-mission)

## Target machine
Kevin's PC gamer:
- Tailscale 100.91.123.14
- Intel i5 20 P-cores, RTX 5060 Ti 16 GB
- venv `/home/remondiere/crossed-cosmos/.venv-mcmc-bench`
- sympy 1.14, JAX 0.10 + named_shape patch, blackjax 1.5, cosmopower-jax 0.5.5

## Pipeline A — F2 pure-Python sweep (DECISIVE, READY)

- File: `pipeline_a/f2_python_sweep.py`
- Cost: **~15-30 min wallclock** (LMFDB REST throttle dominated, NOT 5 CPU-hr — much cheaper than M44 budget)
- Goal: test if F1-renormalized v_2 = {-3,-2,0,+1} is Steinberg-edge specific for f = 4.5.b.a
- Sample: 4.5.b.a anchor + 9 candidates at levels {9, 12, 16, 25, 27, 36, 49, 100}
- Output: `pipeline_a/f2_sweep_results.csv` (16 cols)
- **Falsify**: any NON-STEINBERG row with monotone v_2 = [-3,-2,0,+1]

## Pipeline B — v7.7 CLASS-grade θ* MCMC (SCRIPTS-ONLY, AMBITIOUS)

- File: `pipeline_b/v77_class_pipeline.py`
- Cost: 2-4h GPU on RTX 5060 Ti (cosmopower-jax frontend) OR 24-72h CPU (classy via `jax.pure_callback`)
- Two NMC variants:
  - `eci_nmc` (ξ_χ ≈ -0.024, Cassini-clean, KG-passing)
  - `wolf_nmc` (ξ = 2.31, Wolf 2025 KG-failing per M7+M9)
- Likelihoods: DESI DR2 BAO + Pantheon+ + Planck PR4 compressed (PR3 scaffold) + KiDS-1000 S_8
- NUTS: 4 chains × 5000 warmup + 5000 samples, target_accept=0.85, blackjax 1.5
- Output: `pipeline_b/v77_results.npz` (chains + log-Bayes factor harmonic-mean diagnostic)
- `--smoke` mode for 50/50/1 quick sanity (~2 min)

## Honest scope caveats (must read before paper claim)

1. Pipeline B `_planck_pr4_fallback()` returns **PR3 (Aghanim 2018)** numbers as scaffold — explicitly marked `[TBD: replace with Tristram 2024 PR4 NPIPE]`
2. `H_nmc()` is simplified multiplicative `(1 + ξ·f(z))` form, NOT full M9 KG-aware Friedmann ODE — diagnostic-grade only
3. `loglike_total_v77` uses harmonic-mean log-evidence (BIASED); paper-grade Bayes factor needs nested sampling (dynesty/ultranest)
4. cosmopower-jax θ_s emulator has ~0.5% relative bias vs full CLASS — "v7.7 CLASS-grade" is slight overreach unless classy frontend wired (1-3 day task)
5. F2 sweep gives Q-rational projection of a_n via LMFDB `traces` field; for dim>1 newforms this is the trace, not eigenvalue — interpret cautiously

## Dispatch

- `dispatch.sh` — 6-step automated dispatcher (SSH probe → scp 7 files → verify sympy/JAX/blackjax/cosmopower-jax → smoke B → launch A in tmux session `f2py`, B armed for `--launch-b`)
- `manual_launch.md` — Kevin self-serve fallback if Tailscale SSH issue

Modes: `--full` (default), `--only-scp`, `--launch-b`.

## Discipline log
- 0 new fabrications; hallu 86 → 86
- Mistral STRICT-BAN observed
- NO drift to settings.json
- Pivoted to pure-Python per CRITICAL_UPDATE_M47.md (no SageMath on PC OR VPS)
- ast.parse PASS for both .py + .sage (no Sage-specific syntax)
- Sub-agent return-as-text protocol used for SUMMARY.md

## Followups (parent decision)
1. Run `dispatch.sh` once Tailscale SSH confirmed (DONE 13:44 CEST)
2. After F2 CSV: examine VERDICT block; if INCONCLUSIVE, broaden SWEEP_LABELS via LMFDB filter `weight=5,cm=true,is_steinberg_at_p=2:false`
3. Pipeline B GATED on F2 result; smoke first, then full
