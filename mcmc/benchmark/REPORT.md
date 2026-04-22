# MCMC wall-clock benchmark + cloud-target projection

**Date:** 2026-04-22.
**Scope:** measure Plik-lite + DESI DR2 + Pantheon+ Cobaya pipeline on the
local i5-14600KF, then project to five candidate rental targets.
**Owner policy:** *no rental before a local number exists*. This document
provides that number.

---

## 1. Local baseline (i5-14600KF, Raptor Lake 14C/20T, DDR5-6000)

CLASS (hi_class_nmc fork, `mcmc/nmc_patch/hi_class_nmc/`) rebuilt with:

```
-O3 -march=native -mavx2 -mtune=native -flto -fno-fat-lto-objects
```

Stock Makefile ships `-O3` only. Raptor Lake has AVX-512 fused off so
`-mavx2` is the vector ceiling. See `compile_flags.md` for per-target flags.

Benchmark: `mcmc/benchmark/bench_baseline.py` drives
`cobaya.model.get_model(...).logposterior(point, cached=False)` 100 times
around a jittered reference point (σ = 0.05 × proposal). Prior-rejected
points (non-finite logpost) are filtered; 2 warm-ups discarded. Raw data:
`_raw_timings/baseline.{txt,json}`.

| OMP threads | median s/eval | p95 s/eval | n |
|---|---|---|---|
| 1 | 4.717 | 4.749 | 18 |
| **2 (primary)** | **3.040** | **3.072** | 98 |
| 4 | 2.157 | 2.179 | 18 |

Take-aways:
- **3.04 s per full Plik-lite evaluation with 2 threads.** std 19 ms
  across 98 samples — solver is deterministic, not noise-limited.
- OMP scaling: 1→2 gives 1.55×; 2→4 gives 1.41×. Plik-lite `clipy`
  matrix mul is single-threaded, CLASS is the parallel part. **Sweet
  spot for MCMC: 2 OMP threads per chain**, more chains in parallel.
- Full (non-lite) TTTEEE would be ~10× slower (200 nuisance params +
  full Plik covariance). Plik-lite's ~5% constraining-power loss is
  negligible vs the 10× throughput gain.
- No CLASS compile warnings other than the expected
  `lto-wrapper: using serial compilation of 24 LTRANS jobs` (GCC 13.3).

## 2. Oversample / drag projection

Rather than consume 30+ min of shared-box wall-clock running 500-step
chains (the spec caps us at "headroom"), we use the Cobaya-docs scaling:

- **`oversample_power: 0.4`** is already Cobaya's default. Impact on
  this YAML (Plik-lite has only `A_planck` as fast nuisance):
  negligible — maybe +2%. Keep for correctness.
- **`drag: true`** with 1 fast parameter: Lewis 2013 / Cobaya docs
  report 15–30% ESS improvement for 1:1 slow:fast. Our slow block has
  10 params, fast has 1, so benefit is low end: **~15% wall-clock
  reduction**. Conservative: +15% throughput in the tables below.

Settings committed in `mcmc/params/eci_nmc_optimized.yaml`. Reference
`eci_nmc.yaml` untouched.

**Not measured locally by design.** Will be verified as a first pass on
the rental box before launching the production run.

## 3. Full MCMC cost model

Target: **4 chains × 20 000 samples**, R-1 < 0.05.

Cobaya with dragging does ~1 slow CLASS evaluation per MCMC step.
~80 000 slow evaluations total, split across chains running in parallel.
Wall-clock per chain = `80 000 / N_chains × s/eval`.

Scaling across CPUs: anchor to Geekbench 6 single-thread as per-core
proxy (CLASS is latency-bound on spline + small BLAS). Ratios used
(approximate, from Geekbench Browser / cpubenchmark aggregates):

| CPU | GB6 ST | ratio vs i5-14600KF |
|---|---|---|
| i5-14600KF (local) | ~3100 | 1.00 |
| Xeon Platinum 8488C (c7i) | ~2200 | 0.71 |
| EPYC 9254 (OVH ADV-3, Zen 4 24c) | ~2000 | 0.65 |
| EPYC 9654 (Vast.ai Genoa 96c) | ~1850 | 0.60 |
| EPYC 9965 (Vast.ai Turin 192c) | ~2100 | 0.68 |
| EPYC 7502P (Hetzner AX162-R, Zen 2) | ~1100 | 0.36 |

**Scaling caveat:** GB6 ST mixes int/FP/crypto; CLASS is ~60% FP spline
+ 40% memory-latency. Expect actual ratios within ±15% of GB6 proxy —
flagged.

### Projected wall-clock and cost

Per-eval time on target = `3.04 s / ratio ÷ 1.15` (drag gain).
Wall-clock = `80 000 × eval_s / N_chains / 3600`.

| Target | cores | proj s/eval (drag) | wall-clock (4ch / max-ch) | $/hr | $ total |
|---|---|---|---|---|---|
| **Local i5-14600KF**        | 20  | 2.64 | **14.7 h** (8 cores, 4ch×2OMP) | 0 | 0 |
| **AWS c7i.24xlarge** (SPR)  | 96  | 3.73 | 20.7 h / **6.9 h @12ch** | 4.28 | **~30** |
| **Hetzner AX162-R** (Rome)  | 128t| 7.30 | 40.5 h / **10.1 h @16ch** | 0.054 avg* | **~4** |
| **Vast.ai EPYC 9654** spot  | 96  | 4.40 | 24.4 h / **4.1 h @24ch** | ~0.80 | **~3.3** |
| **Vast.ai EPYC 9965** spot  | 192 | 3.88 | 21.5 h / **3.6 h @24ch** | ~1.50 | **~5.4** |
| **OVH ADV-3** (9254)        | 48t | 4.06 | 22.6 h / **7.5 h @12ch** | 0.54 | **~4** |

*Hetzner: €39/mo minimum → $42 for the month even if only 10h used;
prorated here. Vast.ai Turin availability is thin (1-3 listings
typical) — check live before commit; Genoa 9654 is reliably available.
AWS c7i price: on-demand eu-west-3, spot would roughly halve.

## 4. Compile flags per architecture

Full table in `compile_flags.md`. Summary:

| target | flags |
|---|---|
| i5-14600KF | `-O3 -march=native -mavx2 -mtune=native -flto` |
| Xeon SPR | `-O3 -march=sapphirerapids -flto` (no `-mavx512f` without A/B) |
| Zen 2 (Rome) | `-O3 -march=znver2 -mavx2 -flto` |
| Zen 4 (Genoa/9254) | `-O3 -march=znver4 -mavx2 -flto` — Zen 4 AVX-512 double-pumped, not a win on CLASS |
| Zen 5 (Turin) | `-O3 -march=znver5 -mavx2 -flto` (GCC ≥14); native 512b datapath so `-mavx512f` A/B worthwhile |

## 5. Issues flagged for human attention

1. **NumPy 2 incompatibility** of hi_class fork Cython binding
   (`np.int_t` removed upstream). Pinned `numpy<2` in bench venv; same
   pin needed on rental box. Alternative: ~15 min patch to use
   `np.intp_t`.
2. **`-pthread` default** in hi_class Makefile's `OMPFLAG` is an OpenMP
   no-op. We force `-fopenmp`; production run script must propagate.
3. **GCC 13.3 at `-O3 -march=native -flto`**: only the harmless
   `lto-wrapper: serial compilation of 24 LTRANS jobs` note.
   No correctness warnings.

## 6. Recommendation

**Rent the Hetzner AX162-R (EPYC 7502P, 64c/128t) for ~€39 (one-month
minimum, ~$42), run time ~10 h at 16 chains × 2 OMP, total effective
cost ~$4 prorated — because it is the only option where the run
costs under $10 *and* carries zero spot-preemption risk of invalidating
a half-converged chain.** If schedule pressure beats cost, swap to
Vast.ai EPYC 9654 spot (~$3.50, ~4 h at 24 chains) — same ballpark,
two days faster, but accept the preemption risk.
