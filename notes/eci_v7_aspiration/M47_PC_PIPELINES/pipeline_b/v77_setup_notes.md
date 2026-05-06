# v7.7 pipeline B — setup notes (PC gamer)

Sub-agent M47, 2026-05-06. Hallu count 86 -> 86.

## Target machine

Kevin's PC gamer — Tailscale `100.91.123.14`
- Intel Core i5 (6 P-cores), 32 GB RAM
- RTX 5060 Ti 16 GB GDDR7 (Blackwell sm_120, CUDA 13.1, driver 590.48.01)
- venv: `/home/remondiere/crossed-cosmos/.venv-mcmc-bench`
  (Python 3.11, JAX 0.10, blackjax 1.5, cosmopower-jax 0.5.5)

## JAX patch (already applied per memory note 2026-05-04)

File: `<venv>/lib/python3.11/site-packages/jax/_src/core.py`
Around line 2445, before `ShapedArray(...)` constructor call:
```python
kwargs.pop("named_shape", None)
```
This unblocks pickle loading of cosmopower-jax 0.5.5 trained models on JAX 0.10+.
(Cosmopower's pickled `ShapedArray` carries the deprecated `named_shape` kwarg.)

To verify:
```bash
source /home/remondiere/crossed-cosmos/.venv-mcmc-bench/bin/activate
python -c "import cosmopower_jax; print(cosmopower_jax.__version__)"
```
Expected: `0.5.5`. Then test a CMB prediction:
```bash
python -c "
from cosmopower_jax.cosmopower_jax import CosmoPowerJAX
import jax.numpy as jnp
emu = CosmoPowerJAX(probe='cmb_TT', path=None)  # default user dir
x = jnp.array([[0.0224, 0.120, 67.5, 3.044, 0.965, 0.054]])
print(emu.predict(x).shape)
"
```
Expected: `(1, ~2500)`.

## Frontend priorities

### 1. cosmopower-jax 0.5.5 (READY, recommended)
- 386 predictions/sec on RTX 5060 Ti per memory note
- theta_s emulator: needs `theta_s` probe pickle in user cosmopower dir
  (download: `https://github.com/dpiras/cosmopower/releases/download/v0.1.0/`)
- adequate for v7.7 BAO+SNe primary; CMB legs have ~0.5% theta_s emulator bias

### 2. classy 3.x (AMBITIOUS, slow)
- requires `pip install classylss` or full classy build with cython 3.0
- ~10s per evaluation; with 4 chains x 10000 steps = 40000 calls = ~110 hours wallclock
- **NOT recommended for first run**; use cosmopower-jax frontend first.
- CLASS may not jit-compile under JAX; we wrap in `jax.pure_callback` which
  blocks GPU acceleration. classy frontend is essentially CPU-only.

### 3. EH+KMJ analytic fallback (smoke only)
- 3.1-sigma theta_MC bias per M26 audit -- DO NOT use as primary.
- Pipeline auto-falls-back to this if both classy and cosmopower-jax fail to import.

## Data files needed on PC

```
/home/remondiere/data/desi_dr2/
    desi_gaussian_bao_ALL_GCcomb_mean.txt   (sha256 9ac154ab... per a71_prod log)
    desi_gaussian_bao_ALL_GCcomb_cov.txt    (sha256 252a1432...)
/home/remondiere/data/pantheonplus/
    Pantheon+SH0ES.dat
    Pantheon+SH0ES_STAT+SYS.cov
/home/remondiere/data/planck_pr4/                  [TBD: needs PR4 NPIPE compressed]
    planck_pr4_compressed.json                     (5-param mean + 5x5 cov)
/home/remondiere/data/kids_1000/                   [TBD: optional, pipeline uses S_8 scalar]
```
The first two are confirmed live in a71_prod (S9 acquisition 2026-05-06).
PR4 compressed is the bottleneck — pipeline currently scaffolds with PR3 numbers.

## Launch procedure

```bash
cd /home/remondiere/crossed-cosmos
source .venv-mcmc-bench/bin/activate

# Re-apply tailscale shield (per memory note: each PC reboot)
sudo bash /home/remondiere/pc_calcs/tailscale_shield.sh

# Smoke test (1-2 minutes)
python notes/eci_v7_aspiration/M47_PC_PIPELINES/pipeline_b/v77_class_pipeline.py --smoke

# Full run in tmux
tmux new -d -s v77 \
  "cd /home/remondiere/crossed-cosmos && \
   source .venv-mcmc-bench/bin/activate && \
   python notes/eci_v7_aspiration/M47_PC_PIPELINES/pipeline_b/v77_class_pipeline.py \
      --frontend cosmopower --n_warmup 5000 --n_samples 5000 --n_chains 4 \
      2>&1 | tee /home/remondiere/v77_run_$(date +%Y%m%d_%H%M).log"

# Monitor
tmux attach -t v77
```

## Honest caveats (must read before paper)

- `_planck_pr4_fallback()` returns PR3 (Aghanim 2018) numbers as scaffold;
  before any paper-quality run, replace with Tristram et al. 2024 PR4 NPIPE
  compressed mean + 5x5 cov from arXiv:2309.10034 (or successor).
- `loglike_total_v77` uses harmonic-mean log-evidence — biased! For
  publication-grade Bayes factor, replace with `dynesty` or `ultranest`
  nested sampling (~10x slower, ~1 day wallclock).
- `H_nmc()` is a SIMPLIFIED CPL+xi multiplicative form; for full ECI vs Wolf
  contest the M9 KG-aware Friedmann ODE must be integrated. Pipeline B v0
  is therefore **diagnostic-grade**, not paper-grade.
- KiDS-1000 enters as compressed S_8 only; sigma_8 is computed via a linear
  approximation, not full Boltzmann -- replace with cosmopower-jax sigma_8
  emulator if available.

## Expected runtime

| Frontend       | Smoke  | Full (4x10k)            |
|----------------|--------|-------------------------|
| cosmopower-jax | ~2 min | 2-4 hours (target)      |
| classy         | ~30 min| 24-72 hours (avoid)     |
| EH+KMJ smoke   | ~30 s  | ~1 hour (DO NOT TRUST)  |

`v77_results.npz` size ~ 50 MB for full run.
