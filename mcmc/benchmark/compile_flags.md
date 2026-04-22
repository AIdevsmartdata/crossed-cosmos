# CLASS compile flags per architecture

CLASS (hi_class fork under `mcmc/nmc_patch/hi_class_nmc/`) is built via its
Makefile. All targets below override `OPTFLAG` and leave the rest of the
Makefile untouched. `OMPFLAG` should always be `-fopenmp` (the stock value
`-pthread` is OpenMP-off; fine for a bench but wrong for prod).

Reproduce any target with:

```
cd mcmc/nmc_patch/hi_class_nmc
rm -rf build libclass.a class python/build python/classy*.so
make -j$(nproc) OPTFLAG="<flags>" OMPFLAG="-fopenmp"
# Python binding (numpy<2 required for this fork's Cython):
cd python && python setup.py build_ext --inplace && python setup.py install
```

| Target | `-march` | `-mtune` | extra | confirmed |
|---|---|---|---|---|
| **i5-14600KF (this box)**        | `native` | `native` | `-O3 -mavx2 -flto -fno-fat-lto-objects` | yes — CLASS built, classy loads, 98/100 evals succeed (see baseline.json) |
| **AWS c7i.24xlarge (SPR)**       | `sapphirerapids` | `sapphirerapids` | `-O3 -mavx2 -flto` — **do NOT** add `-mavx512f`/`-mavx512fp16` without a benchmark: CLASS is latency-bound on memory pulls, gather/scatter on AVX-512 often regress | projected |
| **Hetzner AX162-R (EPYC 7502P, Rome)** | `znver2` | `znver2` | `-O3 -mavx2 -flto` | projected |
| **Vast.ai EPYC 9654 (Genoa, Zen 4)**    | `znver4` | `znver4` | `-O3 -mavx2 -flto`; AVX-512 is **double-pumped** on Zen 4 so `-mavx512f` gives at best +5% on CLASS's dense-linear kernels and risks miscompiles on older GCC. Validate before enabling. | projected |
| **Vast.ai EPYC 9965 (Turin, Zen 5)**    | `znver5` (GCC ≥14) or `znver4` fallback | same | `-O3 -mavx2 -flto`. Zen 5 has a native 512-bit AVX-512 datapath so `-mavx512f` may finally be a net win. Needs A/B. | projected |
| **OVH ADV-3 (EPYC 9254, Zen 4)**        | `znver4` | `znver4` | same as Genoa | projected |

## Why not `-Ofast` / `-ffast-math`

CLASS integrates stiff ODEs and interpolates with tight relative-tolerance
requirements. `-ffast-math` enables `-freciprocal-math` and
`-fno-signed-zeros`, both of which have been observed (Lesgourgues mailing
list, 2019; chimere-server regressions on our side) to shift the
background ODE solution by several σ on `H(z)` for exotic cosmologies —
including w0-wa near `w0 ≈ -1`. **Do not use.**

## Correctness check

`mcmc/benchmark/_raw_timings/baseline.txt` is the reference. After any
recompile, a single-evaluation logpost at the reference point should
reproduce to < 1e-4 relative (CLASS spline indexing is deterministic at
`-O3` without `-ffast-math`). `test_plugin.py` in `mcmc/cobaya_nmc/` gives
a quick smoke-level check.

## Compile time observed

- i5-14600KF (14 cores, -j20, -flto): **CLASS build ≈ 18s**, Cython +
  setup.py install ≈ 12s. See `_raw_timings/class_build.log`.
- GCC 13.3 emits one harmless warning about `lto-wrapper: using serial
  compilation of 24 LTRANS jobs` — this is a GCC limitation on
  small codebases, not a correctness issue. No other warnings relevant
  to production.

## One known warning

The fork's `python/classy.pyx` references the numpy typedef `np.int_t`
which was removed in NumPy 2.x. **Pin `numpy<2`** in the CLASS-side venv,
or patch the `.pyx` to use `np.intp_t`. We chose to pin. Upstream hi_class
will need the patch before numpy 2 is unavoidable.
