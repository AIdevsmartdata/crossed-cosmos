# ECI v4 — MCMC pipeline (scaffold)

**Status: SCAFFOLD.** The Cobaya input and run wrapper here are functional once
Cobaya + CLASS + the external likelihoods are installed, but the **CLASS NMC
patch is not yet implemented** — `nmc_xi_chi` is passed through as an
`extra_args` placeholder and CLASS will currently ignore it. See
`nmc_patch/README.md` and `nmc_patch/CLASS_patch_design.md` for the design of
the still-TODO patch.

## Goal

Joint constraint on the ECI v4 parameter set

- `w0`, `wa` — CPL dark-energy EOS
- `xi_chi` — non-minimal coupling ξ_χ of the scalar χ to R
- `f_EDE`  — early-dark-energy fraction at z_c

from the combined data set

- **Planck 2018**  low-ℓ TT + EE, high-ℓ Plik-lite TTTEEE
- **ACT DR6**     (lite likelihood, via `cobaya-install cosmo`)
- **DESI DR2**    BAO (MontePython-style likelihood packaged with Cobaya)
- **Pantheon+**   SN Ia

## Software stack

| Component            | Version        | Role                           |
|----------------------|----------------|--------------------------------|
| Cobaya               | 3.5+           | MCMC driver + likelihood glue  |
| CLASS                | 3.2+ (patched) | Boltzmann code (TODO: NMC)     |
| getdist              | 1.5+           | Chain analysis / triangle plots|
| MontePython-style    | via Cobaya     | DESI DR2 BAO likelihood        |

## Hardware target

- CPU: Intel i5-14600KF (6P + 8E cores, 20 threads)
- RAM: 32 GB DDR5
- Expected wallclock: **~3 days** for 4 chains × ~20 k steps each,
  running 5 OMP threads per chain (`OMP_NUM_THREADS=5`, 4 MPI ranks).
  CLASS is the bottleneck (~0.5–1 s per cosmology at default precision).

## Install

```bash
python3 -m venv ~/.venvs/cobaya && source ~/.venvs/cobaya/bin/activate
pip install --upgrade pip wheel
pip install cobaya getdist
# Installs CLASS, Planck clik, ACT, Pantheon+, DESI BAO data into packages/
cobaya-install cosmo -p packages/
```

The `cosmo` keyword fetches CLASS, CAMB, Planck clik, ACT DR6, BAO (inc. DESI
DR2), Pantheon+ in one shot. If CLASS is already built locally with the NMC
patch, set `path:` in the `theory.classy` block of the YAML to that build.

## Run

```bash
# single-node, 4 MPI chains, 5 OMP threads each
export OMP_NUM_THREADS=5
mpirun -np 4 cobaya-run params/eci_nmc.yaml
# or simply:
bash run.sh
```

Output chains land in `chains/eci_nmc.*.txt`. Use `-r` to resume.

## Analyze

```python
from getdist import loadMCSamples, plots
s = loadMCSamples("chains/eci_nmc", settings={"ignore_rows": 0.3})
g = plots.get_subplot_plotter()
g.triangle_plot(s, ["w0", "wa", "xi_chi", "f_EDE", "H0"], filled=True)
g.export("chains/eci_nmc_triangle.pdf")
```

Convergence target: Gelman-Rubin `R-1 < 0.05` on all sampled params
(set in the YAML sampler block).

## Known caveats (READ BEFORE TRUSTING A RESULT)

1. **CLASS NMC patch is a stub.** Without modifications to
   `source/background.c` and `source/perturbations.c` the parameter
   `xi_chi` has **no effect** on the Boltzmann solution. The resulting
   posterior on `xi_chi` would therefore be prior-dominated. The real
   implementation must add the ξ_χ R χ²/2 term — see
   `nmc_patch/CLASS_patch_design.md`.
2. **`f_EDE` requires CLASS_EDE** (Hill+20) or equivalent. Plain CLASS does
   not ship an EDE module; expect to either link against CLASS_EDE or add
   an axion-like fluid. Current YAML treats `f_EDE` as a free parameter
   passed to CLASS — will be silently ignored by vanilla CLASS.
3. **DESI DR2 likelihood** ships with Cobaya ≥ 3.5.1; older Cobaya needs a
   manual MontePython drop-in.
4. **Planck 2018 clik** requires ~2 GB download during `cobaya-install`.

## Layout

```
mcmc/
├── README.md                (this file)
├── run.sh                   (bash wrapper)
├── params/
│   └── eci_nmc.yaml         (Cobaya input)
└── nmc_patch/
    ├── README.md            (status + source-file map)
    └── CLASS_patch_design.md (equations to add)
```
