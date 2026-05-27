# KEVINOTRON -- Architecture Document
# Lattice Gauge Theory EE Engine
# Kevin Remondiere (ORCID 0009-0008-2443-7166)

## Overview

Three-layer engine for measuring entanglement entropy in 4D lattice
gauge theories via the BP2008b alpha-integration (replica trick).

```
+================================================================+
|                     KEVINOTRON STACK                            |
+================================================================+
|                                                                |
|  LAYER 3: ORCHESTRATOR + DATA PIPELINE                         |
|  +---------------------------------------------------------+  |
|  |  orchestrate.py                                          |  |
|  |  - Multi-group x multi-L x multi-beta scan              |  |
|  |  - Dispatches Rust jobs (11 alpha-points per config)     |  |
|  |  - Parses logs, trapezoidal integration, fits            |  |
|  |  - Publication-ready plots + LaTeX tables                |  |
|  +---------------------------------------------------------+  |
|           |                            ^                       |
|           | spawn                      | .log + .npy           |
|           v                            |                       |
|  LAYER 1: RUST CPU (Production MC)     |                       |
|  +---------------------------------------------------------+  |
|  |  kevinotron (single binary)                              |  |
|  |  --group G2|SU2|SU3|SU4                                  |  |
|  |  --ls 8 --beta 10.0 --alpha 0.5                         |  |
|  |  --n-therm 500 --n-meas 200 --n-skip 5                  |  |
|  |                                                          |  |
|  |  trait GaugeGroup {                                      |  |
|  |    fn dim_fund() -> usize;                               |  |
|  |    fn dim_adj() -> usize;                                |  |
|  |    fn identity() -> LinkMatrix;                          |  |
|  |    fn random_near_id(eps, rng) -> LinkMatrix;            |  |
|  |    fn dagger(U) -> LinkMatrix;                           |  |
|  |    fn trace_re(U) -> f64;                                |  |
|  |    fn beta_norm() -> f64;                                |  |
|  |    fn reproject(U) -> LinkMatrix;                        |  |
|  |  }                                                       |  |
|  |                                                          |  |
|  |  impl GaugeGroup for G2  { 7x7 real, SO(7) polar }      |  |
|  |  impl GaugeGroup for SU2 { 2x2 complex, Cayley-Klein }  |  |
|  |  impl GaugeGroup for SU3 { 3x3 complex, Taylor12+proj } |  |
|  |  impl GaugeGroup for SU4 { 4x4 complex, Taylor12+proj } |  |
|  |                                                          |  |
|  |  Outputs:                                                |  |
|  |    stdout: ALPHA lines (machine-parseable)               |  |
|  |    --dump-config: writes config_{group}_L{L}.npy         |  |
|  +---------------------------------------------------------+  |
|           |                                                    |
|           | .npy configs (thermalized gauge field)             |
|           v                                                    |
|  LAYER 2: JAX GPU (Spectral Analysis)                          |
|  +---------------------------------------------------------+  |
|  |  jax_ds/spectral.py                                      |  |
|  |  - Loads .npy link configurations                         |  |
|  |  - Builds covariant Laplacian on GPU                     |  |
|  |    Delta = sum_mu [ 2I - U_mu(x) delta_{x,x+mu}        |  |
|  |                         - U_mu(x-mu)^dag delta_{x,x-mu}]|  |
|  |  - Builds Faddeev-Popov operator (adjoint rep)           |  |
|  |    M_FP = -D_mu^adj D_mu^adj (ghost Laplacian)          |  |
|  |  - Full diag via jnp.linalg.eigh (dense, fits VRAM)     |  |
|  |  - Spectral dimension d_s from heat kernel               |  |
|  |    P(t) = sum exp(-t lambda_k)                           |  |
|  |    d_s(t) = -2 d(ln P)/d(ln t)                          |  |
|  |  - EE cross-validation: rebuild alpha-action on GPU      |  |
|  +---------------------------------------------------------+  |
|                                                                |
+================================================================+
```


## Memory Budget (VRAM: 16 GB RTX 5060 Ti)

Matrix dimensions for the covariant Laplacian (fundamental rep):
  dim = N_sites x d_fund = L^3 x 2L x d_fund

For Faddeev-Popov (adjoint rep):
  dim = N_sites x d_adj = L^3 x 2L x d_adj

### Fundamental Laplacian

| Group | d_f | L  | N_sites | dim     | dense f64 bytes | dense f64 GB | fits 16GB? |
|-------|-----|----|---------|---------|-----------------|--------------|------------|
| SU(2) |  2  |  4 |    512  |   1024  |       8 MB      |     0.01     |    YES     |
| SU(2) |  2  |  6 |   2592  |   5184  |     215 MB      |     0.20     |    YES     |
| SU(2) |  2  |  8 |   8192  |  16384  |    2.15 GB      |     2.0      |    YES     |
| SU(2) |  2  | 10 |  20000  |  40000  |   12.8 GB       |    12.0      |  TIGHT     |
| SU(2) |  2  | 12 |  41472  |  82944  |   55.0 GB       |    51.3      |    NO      |
| SU(3) |  3  |  4 |    512  |   1536  |      18 MB      |     0.02     |    YES     |
| SU(3) |  3  |  6 |   2592  |   7776  |     484 MB      |     0.45     |    YES     |
| SU(3) |  3  |  8 |   8192  |  24576  |    4.83 GB      |     4.5      |    YES     |
| SU(3) |  3  | 10 |  20000  |  60000  |   28.8 GB       |    26.8      |    NO      |
| SU(4) |  4  |  4 |    512  |   2048  |      34 MB      |     0.03     |    YES     |
| SU(4) |  4  |  6 |   2592  |  10368  |     860 MB      |     0.80     |    YES     |
| SU(4) |  4  |  8 |   8192  |  32768  |    8.59 GB      |     8.0      |    YES     |
| G2    |  7  |  4 |    512  |   3584  |     103 MB      |     0.10     |    YES     |
| G2    |  7  |  6 |   2592  |  18144  |    2.63 GB      |     2.5      |    YES     |
| G2    |  7  |  8 |   8192  |  57344  |   26.3 GB       |    24.5      |    NO      |

### Faddeev-Popov (adjoint)

| Group | d_adj | L  | dim     | dense f64 GB | fits 16GB? |
|-------|-------|----|---------|--------------|------------|
| SU(2) |   3   | 4  |   1536  |     0.02     |    YES     |
| SU(2) |   3   | 6  |   7776  |     0.45     |    YES     |
| SU(2) |   3   | 8  |  24576  |     4.5      |    YES     |
| SU(3) |   8   | 4  |   4096  |     0.13     |    YES     |
| SU(3) |   8   | 6  |  20736  |     3.4      |    YES     |
| SU(3) |   8   | 8  |  65536  |    34.0      |    NO      |
| SU(4) |  15   | 4  |   7680  |     0.47     |    YES     |
| SU(4) |  15   | 6  |  38880  |    12.1      |  TIGHT     |
| G2    |  14   | 4  |   7168  |     0.41     |    YES     |
| G2    |  14   | 6  |  36288  |    10.5      |  TIGHT     |

Note: complex128 entries use 16 bytes (SU(N)), float64 use 8 bytes (G2).
The "dense f64 GB" column accounts for this (complex = 2x storage).

**PRACTICAL CUTOFFS (16 GB VRAM):**
- Fundamental Laplacian: L <= 8 for SU(2,3,4); L <= 6 for G2
- FP operator (adjoint): L <= 8 for SU(2); L <= 6 for SU(3),SU(4),G2
- L=4 : all groups, both operators, comfortably in VRAM


## Benchmark Estimates (CPU vs GPU)

| Operation               | CPU (Rust, 14 cores) | GPU (RTX 5060 Ti) | Speedup |
|--------------------------|---------------------|--------------------|---------|
| MC sweep G2 L=4          |       0.02s         |      N/A (seq)     |   --    |
| MC sweep G2 L=8          |       0.8s          |      N/A (seq)     |   --    |
| MC sweep SU(3) L=8       |       0.3s          |      N/A (seq)     |   --    |
| eigh 1024x1024 real      |       2s            |      0.02s         |  100x   |
| eigh 7168x7168 real      |       180s          |      0.5s          |  360x   |
| eigh 16384x16384 complex |       ~60min        |      3s            |  1200x  |
| Build Laplacian 7168     |       10s           |      0.3s          |   33x   |
| Heat kernel P(t) 7168    |       0.1s          |      0.001s        |  100x   |

**Strategy:** Rust CPU does ALL Monte Carlo (inherently sequential Metropolis).
GPU does ALL spectral analysis (dense eigendecomposition is massively parallel).


## File Layout

```
kevinotron/
  ARCHITECTURE.md          # this file
  Cargo.toml               # Rust workspace
  src/
    main.rs                # CLI dispatcher
    groups/
      mod.rs               # trait GaugeGroup
      g2.rs                # G2 7x7 real
      su2.rs               # SU(2) 2x2 complex via Cayley-Klein
      su3.rs               # SU(3) 3x3 complex
      su4.rs               # SU(4) 4x4 complex
    lattice.rs             # Lattice4D<G: GaugeGroup>
    metropolis.rs          # Sweep + alpha-deformed action
    io.rs                  # .npy config dump, log output
  jax_ds/
    spectral.py            # Covariant Laplacian + FP operator + d_s
    adjoint.py             # Ad(U) construction for all groups
    cross_validate.py      # EE cross-check: reproduce Rust results on GPU
    utils.py               # .npy loader, plotting
  scripts/
    orchestrate.py         # Multi-run dispatcher
    analyze.py             # Full analysis pipeline
```


## Data Flow

```
                      orchestrate.py
                           |
           +------+--------+--------+------+
           |      |        |        |      |
           v      v        v        v      v
     Rust(a=0) Rust(a=0.1) ... Rust(a=0.9) Rust(a=1)
           |      |        |        |      |
           v      v        v        v      v
     .log+.dat  .log+.dat  ...   .log+.dat .log+.dat
           |      |                 |      |
           +------+---------+------+------+
                            |
                     analyze.py
                    (trapezoidal int)
                            |
                     +------+------+
                     |             |
                     v             v
              S2/A tables    config.npy (from a=0 run)
                                   |
                                   v
                            spectral.py (GPU)
                            (Laplacian, FP, d_s)
                                   |
                                   v
                            d_s, lambda_min, etc.
```


## NPY Config Format

The Rust binary can dump thermalized configurations in .npy format.
Layout for group with d_fund-dim fundamental representation on L^3 x 2L lattice:

```
Shape: (4, L, L, L, 2L, d_fund, d_fund)
         ^  ^--------^   ^     ^--------^
         mu  spatial     temporal  matrix

dtype: float64 for G2 (real 7x7)
       complex128 for SU(N) (complex NxN)
```

This matches the JAX lattice layout in kevinotron_fast.py exactly,
so JAX can load the config with a single jnp.load() call.


## Build & Run

```bash
# Build Rust binary
cd kevinotron
cargo build --release
# Binary at target/release/kevinotron

# Single alpha-point
./target/release/kevinotron --group g2 --ls 8 --beta 10.0 --alpha 0.5

# Full EE with config dump
./target/release/kevinotron --group g2 --ls 8 --beta 10.0 --full-ee --dump-config

# Spectral analysis on GPU
python3 jax_ds/spectral.py --config config_g2_L8.npy --group g2

# Full orchestrated run
python3 scripts/orchestrate.py --groups g2 su3 --ls 4 6 8 --betas 10.0
```
