# Vast.ai MCMC pipeline — debug journal 2026-05-02

Recipe to launch a Cobaya MCMC on a Vast.ai instance, with the failures encountered and the workarounds that resolved each. Captured during a session that finally produced live chains on EPYC 7V13 (contract 36023758) at ~280 steps/min/chain × 4 chains, after about 90 min of debugging.

The artefacts are:

- `scripts/vastai/setup-system.sh` — system layer (sudo). Apt + LaTeX + CUDA env. Hardware-auto-detected (CPU AVX, GPU compute capability). Idempotent.
- `scripts/vastai/postinstall-base.sh` — original user-level Python install. Has `set -e`, so if any `pip install` fails, it aborts and leaves the venv half-built.
- `scripts/vastai/postinstall-resume.sh` — recovery script with `set +e` and the failure-specific patches below. **This is what to actually run** after `setup-system.sh`.
- `scripts/vastai/launch-mcmc.sh` — the working MCMC launch wrapper with Docker-friendly MPI flags.

## Failures encountered, in order

### F1 — Wrong Docker image name
Initial rental specified `vastai/cuda:12.4.1-cudnn-devel-ubuntu22.04`. Result: `Error response from daemon: pull access denied for vastai/cuda, repository does not exist`. Vast.ai's standard images are under `nvidia/cuda`, not `vastai/cuda`.

**Fix:** use `nvidia/cuda:12.4.1-cudnn-devel-ubuntu22.04`.

### F2 — SSH key not registered on account
`POST /api/v0/ssh-keys/` and `/api/v0/users/current/ssh-keys/` both return `"Not found"`. The user account has exactly one `ssh_key` field exposed via `/api/v0/users/current/`, prepopulated with the user's local-PC pubkey.

**Fix:** for runtime SSH from the orchestrator (this VPS), use `vastai attach ssh <instance_id> "<pubkey>"` from the `vastai` Python CLI. That endpoint works where the REST one does not. After invocation, wait ~10 s for the proxy to propagate, then `ssh -p <port> -i <privkey> root@ssh<idx>.vast.ai` succeeds.

### F3 — `polychord-py3` does not exist on PyPI
The `postinstall-base.sh` step 4 hard-codes `pip install polychord-py3`, which fails. Combined with `set -e`, this aborts the entire postinstall, leaving steps 5–9 unrun.

**Fix:** drop `polychord-py3` from the install list; use `dynesty + nautilus-sampler + ultranest` for nested sampling instead. PolyChord proper requires source build (`git clone https://github.com/PolyChord/PolyChordLite && cd PolyChordLite && pip install .`), and is only worth it if Bayes-factor extraction needs PolyChord specifically. See `postinstall-resume.sh`.

### F4 — AxiCLASS Makefile assumes `python` not `python3`
AxiCLASS's `python/Makefile` invokes bare `python`. Ubuntu 22.04 only has `python3` on PATH. Build aborts with `/bin/sh: 1: python: not found`.

**Fix (workaround):** activate the venv (`source ~/.venv/physics/bin/activate`) before running `make` — venv's `bin/python` shim is on PATH.

**Fix (proper):** use `python3 -m pip install . --no-build-isolation` directly in `python/`, skipping the Makefile's pip-install step.

### F5 — pip build isolation hides Cython
Running `pip install -e .` in `AxiCLASS/python/` without `--no-build-isolation` triggers PEP 517 build, which spins up an isolated venv that doesn't have Cython.

**Fix:** `pip install --no-build-isolation -e .`.

### F6 — AxiCLASS 3.3.0 has an FP precision bug on Zen 3
After successfully building and installing AxiCLASS classy v3.3.0, *every* `cl.compute()` call — even `Class().set({}).compute()` for bare LCDM — fails with:

```
Error in Class: thermodynamics_init(L:382) :error in thermodynamics_lists(...);
=>thermodynamics_lists(L:1146) :error in background_tau_of_z(...);
=>background_tau_of_z(L:285) :condition (z < pba->z_table[pba->bt_size-1]) is true;
   out of range: z=0.000000e+00 < z_min=6.661338e-16
```

`6.66e-16` is `3 × machine_epsilon_double`, which suggests AxiCLASS's background-table construction uses a slightly-positive z_min and the boundary check then fails the legitimate `z=0` query. Verified: independent of `-O3`, `-O2`, `-O0`, `-march=native`, `-ffast-math`. Reproducible on multiple param combinations and on bare-default LCDM.

**Fix:** install vanilla CLASS upstream (`https://github.com/lesgourg/class_public.git`), which is at v3.3.4 and does not exhibit the bug. Vanilla CLASS works for the v5 sanity-check (no EDE). For Levier #1 12-param with EDE, AxiCLASS will need patching — record this as a TODO for the v8-bis math.CT phase, not a blocker for the v5 sanity. **Actionable:** open an issue at `PoulinV/AxiCLASS` referencing the upstream `lesgourg/class_public` 3.3.4 patch, possibly the commit at HEAD of `class_public/source/background.c::background_tau_of_z`.

### F7 — `cobaya-install classy` requires `--packages-path`
Per Cobaya's design, `cobaya-install` writes data into a configurable packages directory, but if `COBAYA_PACKAGES_PATH` is unset and no `-p` is given, it errors.

**Fix:** always invoke as `cobaya-install <component> -p mcmc/packages`. Likewise, `cobaya-run --packages-path mcmc/packages`. The repo gitignore should exclude `mcmc/packages/`.

### F8 — Cobaya `VersionCheckError` for classy < 3.3.3
With AxiCLASS 3.3.0 or upstream 3.3.4, Cobaya's classy interface still requires `>= 3.3.3` and rejects 3.3.0. (Upstream 3.3.4 passes, AxiCLASS 3.3.0 fails.)

**Fix:** add `ignore_obsolete: true` under `theory.classy:` in the YAML. Cobaya documents this as the right knob for "running a modified CLASS." The current `mcmc/chains/eci_v50_run1/eci.input.yaml` has been patched accordingly.

### F9 — DESI / Pantheon+ data not installed by default
Cobaya likelihood `bao.desi_dr2.desi_bao_all` and `sn.pantheonplus` need their data files downloaded.

**Fix:** `cobaya-install bao.desi_dr2.desi_bao_all sn.pantheonplus -p mcmc/packages`. ~57 MB total.

### F10 — `mpi4py` not installed in the venv
The venv was created fresh by `postinstall-base.sh` and does not inherit the system's `python3-mpi4py`. Running `mpirun -np 4 python -c "from mpi4py import MPI"` would `ModuleNotFoundError`.

**Fix:** `pip install --no-binary=mpi4py mpi4py`. The `--no-binary` flag forces a source build linked against the system's OpenMPI 4.1.2, ensuring the `mpi4py.MPI.get_vendor() == ('Open MPI', (4,1,2))` matches `mpirun --version`. With binary wheels (default on PyPI), mpi4py ships with its own MPICH bundled, which conflicts with the system's OpenMPI.

### F11 — `mpirun -np 4 cobaya-run` fails with lock collision
With mpi4py installed and verified working (`mpirun -np 4 python -c "from mpi4py import MPI; print(MPI.COMM_WORLD.Get_rank(), MPI.COMM_WORLD.Get_size())"` correctly prints rank 0..3 / size 4), the `cobaya-run YAML` script wrapper still fails with:

```
[output] *ERROR* File ./eci.input.yaml.locked is locked by another process,
you are running with MPI disabled but may have more than one process.
Make sure that you have mpi4py installed and working.
```

The wrapper's MPI detection somehow returns `size = 1` per process, while `cobaya.mpi.size()` in a fresh `python -c` call inside `mpirun` correctly returns 4. The exact cause was not traced; possibly an interaction between cobaya-run's lazy import and how Open MPI initialises the Python ABI.

**Fix:** invoke as `python -m cobaya run YAML` rather than `cobaya-run YAML`. This bypasses the script-wrapper and lets Python initialise MPI normally before `cobaya.mpi` is imported.

### F12 — OpenMPI cgroup binding in Docker
`mpirun` with default flags emits warnings:

```
WARNING: Open MPI tried to bind a process but failed.
  Error message: failed to bind memory
  Location: ../orte/mca/rtc/hwloc/rtc_hwloc.c:447
```

…and depending on kernel version may further fail with `--bind-to core --map-by socket` because the Docker container's cgroup doesn't expose all host cores or socket topology to OpenMPI.

**Fix:** pass `--bind-to none --mca btl_vader_single_copy_mechanism none --oversubscribe` to `mpirun`. Disables binding (no big deal — with 4 chains × 32 threads on 256-logical-core EPYC 7V13, OS scheduling is fine), and disables CMA single-copy in the shared-memory BTL (which is restricted by container security policies).

### F13 — `nohup ... &` does not survive SSH close in this Docker setup
Even with `nohup`, when the orchestrator's SSH session closes, the backgrounded process is killed. This appears specific to the Vast.ai SSH proxy + container init combination.

**Fix:** `nohup setsid bash launch-mcmc.sh < /dev/null > log 2>&1 & disown`. The `setsid` creates a new session group and detaches from the controlling terminal entirely. This survives SSH close on Vast.ai instances. (Tested 2026-05-02: launched at 17:42:45 from this VPS, immediately closed SSH, and the chains continued progressing through 17:43:45 — F13 confirmed fixed.)

### F14 — Cobaya output prefix collision after killed process
After `pkill -9` of a previous launch, residual `eci.input.yaml.locked` (zero-byte) remains and re-launches detect it as a "currently locked" file.

**Fix:** between launches, `rm -f eci.* eci.input.yaml.locked` in the YAML's output dir.

## What lives where, after the working launch

```
/root/                               on the Vast.ai instance
├── crossed-cosmos/                  cloned from github.com/AIdevsmartdata
│   ├── eci.{1,2,3,4}.txt            chain output (live)
│   ├── eci.input.yaml               (mirror of mcmc/chains/eci_v50_run1/eci.input.yaml)
│   ├── eci.input.yaml.locked        cobaya MPI lock file (presence == active run)
│   ├── eci.checkpoint, eci.covmat, eci.progress, eci.updated.yaml
│   └── mcmc/packages/               cobaya-installed DESI + Pantheon+ data
├── src/
│   ├── class_public/                vanilla CLASS 3.3.4 (preferred for sanity)
│   ├── AxiCLASS/                    AxiCLASS 3.3.0 (broken FP — patch TODO)
│   └── hi_class_public/             hi_class for αM/αB
├── .venv/physics/                   Python 3.10 venv with the 122-pkg stack
├── launch_mcmc.sh                   working MCMC launcher
├── mcmc_run.log                     live launch output (filtered tail useful)
└── /etc/profile.d/vastai-physics.sh tunable env (CFLAGS, BLAS threads, CUDA)
```

Acceptance rate at ~50 %, ~280 steps/min/chain → ~5 k steps in ~18 min, full convergence (R-1 < 0.10) expected in 30–45 min on this hardware.

## TODO carried forward

- File an upstream issue against `PoulinV/AxiCLASS` for the F6 FP-bug. Reference vanilla CLASS 3.3.4 as the patched-source baseline.
- For Levier #1 12-param (which needs EDE), either (a) backport the CLASS 3.3.4 fix into AxiCLASS, or (b) merge AxiCLASS's EDE patches onto vanilla CLASS 3.3.4 manually. Estimated work: 1-2 days.
- Add `mcmc/packages/` to `.gitignore` so we don't accidentally commit 60+ MB of likelihood data.
