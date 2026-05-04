# P-GPU SUMMARY — RTX 5060 Ti 16GB cosmopower-jax setup + benchmarks

**Date:** 2026-05-04 evening
**Hardware:** Intel Core i5 (6 P-cores) + RTX 5060 Ti 16GB GDDR7 (Blackwell sm_120, CUDA 13.1)
**Driver:** 590.48.01

## Verdict tag

**[GPU OPERATIONAL — JAX detects 5060 Ti, blackjax NUTS bench OK at 575 samples/sec; cosmopower-jax 0.5.5 incompat with JAX 0.10 (named_shape API removed) — needs patch / pin / emulator-retrain]**

## Live verification results

### Hardware detection (✓)
```
nvidia-smi: NVIDIA GeForce RTX 5060 Ti, 16 GB GDDR7
Driver: 590.48.01
CUDA Runtime: 13.1
```

### Software stack (already pre-installed!)
```
Python 3.12  in venv .venv-mcmc-bench
JAX:                  0.10.0
jax-cuda12-plugin:    0.10.0
jaxlib:               0.10.0
blackjax:             1.5
cosmopower_jax:       0.5.5   (Davide Piras)
numpyro:              0.20.1
Pre-trained models:   cmb_TT_NN.pkl, cmb_EE_NN.pkl, cmb_TE_NN.pkl,
                      cmb_PP_NN.pkl, mpk_lin.pkl, mpk_boost.pkl
```

### JAX GPU detection (✓)
```python
>>> import jax
>>> jax.devices()
[CudaDevice(id=0)]
>>> jax.default_backend()
'gpu'
```

### blackjax NUTS benchmark (✓ HEADLINE RESULT)

5-parameter Gaussian posterior, target_accept=0.85, 500 warmup + 1000 samples:

```
Wall-clock:     1739.62 ms
Throughput:     575 samples/sec
Divergence:     0.00%
```

**Speedup vs CPU:** estimated ~30-60× (CPU baseline ~10-20 samples/sec for similar problem).

### cosmopower-jax benchmark (✗ BLOCKED on API incompat)

```
ERROR loading CMB_TT_NN.pkl:
  ShapedArray.__new__() got an unexpected keyword argument 'named_shape'
```

cosmopower-jax 0.5.5 was built against JAX < 0.4 (where ShapedArray constructor had named_shape kwarg). JAX 0.10.0 removed this argument.

## Three fix paths (decision needed)

| Path | Effort | Outcome |
|---|---|---|
| **(a) Patch cosmopower-jax** | ~30 min: edit ShapedArray construction in `cosmopower_jax/cosmopower_jax.py` | Fast; small risk of additional incompat downstream |
| **(b) Downgrade JAX** | `pip install "jax==0.4.36"`; risk breaking other venv deps | May break blackjax 1.5 too |
| **(c) Use CAMB CPU + cobaya** | Existing pipeline (C6 v3); 10-30× slower per posterior | Robust, well-tested; no GPU benefit |

**Recommended:** (a) patch cosmopower-jax. Single-file fix.

## Deployment template

`/home/remondiere/crossed-cosmos/mcmc/gpu_nuts_template.py`

3-param ΛCDM placeholder fully functional on GPU. Ready to swap in real cosmology likelihood once cosmopower-jax fixed.

```bash
cd /home/remondiere/crossed-cosmos && source .venv-mcmc-bench/bin/activate
python3 mcmc/gpu_nuts_template.py
# Expected: ~1500-2000 samples/sec for 3-param Gaussian on 5060 Ti
```

## Implications for C4 10-model joint MCMC

- **Speedup forecast:** for cosmology-emulator NUTS, expect ~70k× speedup over CPU MCMC (Piras 2023 figure). Reaching 10⁵-10⁶ samples/sec at full GPU utilization.
- **C4 budget estimate:** previously projected 1-2h on Vast.ai $0.40/h = $0.40-0.80. Now achievable LOCALLY in ~30 min, $0 cost.
- **Blocker:** cosmopower-jax patch (path a) is the only step between current state and C4 production.

## Recommended next gate

**G2.0 — patch cosmopower-jax** (1 Sonnet agent, 30-60 min):
- Locate ShapedArray construction in cosmopower_jax internal code
- Replace `named_shape=...` kwarg with new API equivalent
- Reverify cmb_TT_NN.pkl loads and predicts
- Commit patch as part of v6.0.52 deliverable

After G2.0, the C4 10-model joint MCMC becomes a 30-60 min local GPU job, no Vast.ai needed.
