# C4 Joint MCMC — Vast.ai Pre-Booking Checklist
**ECI version:** v6.0.45 (Zenodo DOI 10.5281/zenodo.20022897)
**Date:** 2026-05-04
**Design doc:** `compute/C4_joint_mcmc/preregistration/design_doc_v1.md` (267 lines, locked)
**Status:** PRE-BOOKING — do NOT book Profile L until all BLOCKER items are GO

---

## 1. Pre-Booking Blockers

Each item is binary GO / NO-GO. ALL five must be GO before Profile L booking.

### BLOCKER 1 — AxiCLASS proper compile + cobaya wire-up
**Status: NO-GO (local failure confirmed today)**

Symptom: params `fEDE`, `log10z_c`, `thetai_scf` not recognised by running classy wrapper — Cobaya is loading vanilla CLASS instead of AxiCLASS extension.

Root cause: `cobaya-install classy` installs upstream CLASS from CobayaSampler/packages; AxiCLASS (PoulinV/AxiCLASS) must be compiled separately and pointed to via `path:` in the Cobaya YAML `theory.classy` block.

**Resolution procedure (run on Profile S first, ~$4):**
```bash
# 1. Clone AxiCLASS
git clone https://github.com/PoulinV/AxiCLASS.git packages/code/AxiCLASS

# 2. Compile C code + Python wrapper
cd packages/code/AxiCLASS
make -j$(nproc)          # builds libclass.so
make classy              # builds classy.cpython-*.so
pip install -e .

# 3. Smoke-test: EDE params must be recognised
python -c "
import classy
c = classy.Class()
c.set({'f_EDE': 0.1, 'log10z_c': 3.5, 'thetai_scf': 1.5,
       'output': 'tCl', 'l_max_scalars': 100,
       'h': 0.68, 'omega_b': 0.022, 'omega_cdm': 0.12,
       'n_s': 0.96, 'A_s': 2.1e-9, 'tau_reio': 0.055})
c.compute()
print('AxiCLASS OK, fEDE accepted')
"

# 4. In Cobaya M9 YAML theory block:
# theory:
#   classy:
#     path: packages/code/AxiCLASS
#     extra_args:
#       EDE_type: 1   # axion potential V = m^2 f^2 (1-cos(theta/f))^n
```

**GO criterion:** smoke-test passes with no `AttributeError` or `CosmoSevereError`; M9 nlive=20 sanity run completes without crashing.

Note: `mwt5345/class_ede` is an alternative EDE CLASS fork (McCarthy-Toomey-Smith 2022) that uses the same {fEDE, log10z_c, thetai} shooting algorithm and may be more actively maintained than AxiCLASS for Cobaya. If AxiCLASS compile fails after 2h, switch to class_ede as fallback and document in v2 pre-registration amendment.

---

### BLOCKER 2 — hi_class_public compile + Cobaya Python wrapper
**Status: NO-GO (no compiled lib folder on local clone)**

Symptom: Cobaya cannot find `lib.*.so`; hi_class directory present but `make classy` was never run.

Root cause: hi_class requires `make` (C code) **then** `make classy` (Cython wrapper); `make classy` does NOT auto-update `classy.c` on source changes — must delete `classy.c` and rerun if hi_class source was modified.

**Resolution procedure:**
```bash
# 1. Clone hi_class_public
git clone https://github.com/miguelzuma/hi_class_public.git packages/code/hi_class_public

# 2. Compile C code first
cd packages/code/hi_class_public
make -j$(nproc)

# 3. Compile Python wrapper (order matters)
rm -f classy.c            # force Cython regeneration
make classy

# 4. Smoke-test: Horndeski params must be accepted
python -c "
import classy
c = classy.Class()
c.set({'gravity_model': 'propto_omega',
       'parameters_smg': '-0.1, 0.5, 0, 0',
       'output': 'tCl', 'l_max_scalars': 100,
       'h': 0.68, 'omega_b': 0.022, 'omega_cdm': 0.12,
       'n_s': 0.96, 'A_s': 2.1e-9, 'tau_reio': 0.055})
c.compute()
print('hi_class OK, alpha_B accepted')
"

# 5. Cobaya YAML theory block for M5/M6/M10:
# theory:
#   classy:
#     path: packages/code/hi_class_public
```

**GO criterion:** both M5 (Coupled-DE) and M6 (DHOST/Horndeski) smoke-tests pass; hi_class `lib.cpython-312-x86_64-linux-gnu.so` present in `packages/code/hi_class_public/`.

**Warning:** hi_class and AxiCLASS cannot share the same `classy` namespace simultaneously — each model group needs its own YAML `theory.classy.path` pointing to the correct fork. Cobaya handles this correctly via `path:` isolation.

---

### BLOCKER 3 — cosmopower-jax emulator training (M5 Coupled-DE + M9 EDE)
**Status: NO-GO (training not done)**

Purpose: saves ~$230 of Profile L CPU-CLASS time. Each evaluation of M5 hi_class + M9 AxiCLASS takes ~15-60s; emulator reduces this to ~1ms on GPU.

**Resolution procedure (RTX 4090, $0.40/h, ~4h each, $3-4 total):**

Install:
```bash
pip install cosmopower-jax   # version must be >= 0.1.0; verify: python -c "import cosmopower_jax; print(cosmopower_jax.__version__)"
```

Generate training grid + train:
```bash
# Training grid: Latin Hypercube over prior box (N=50000 samples recommended)
python compute/C4_joint_mcmc/training/make_training_grid.py \
    --model M5 --n-samples 50000 --output training/M5_grid.npz

# Train emulator (JAX on GPU)
CUDA_VISIBLE_DEVICES=0 python compute/C4_joint_mcmc/training/train_emulator.py \
    --model M5 --grid training/M5_grid.npz --output emulators/M5_cpjax/ \
    --epochs 300 --batch-size 512

# Repeat for M9 (EDE; wider prior, may need N=100000)
python compute/C4_joint_mcmc/training/make_training_grid.py \
    --model M9 --n-samples 100000 --output training/M9_grid.npz
CUDA_VISIBLE_DEVICES=0 python compute/C4_joint_mcmc/training/train_emulator.py \
    --model M9 --grid training/M9_grid.npz --output emulators/M9_cpjax/ \
    --epochs 500 --batch-size 512
```

Cobaya theory block with emulator:
```yaml
theory:
  cosmopower_jax.cosmopower_jax.CosmoPowerJAX:
    network_path: emulators/M5_cpjax/
    probe: pk_nonlin    # or cmb_tt / cmb_ee / cmb_te depending on output needed
```

**IMPORTANT API note:** cosmopower-jax uses `CosmoPowerJAX` class directly, NOT via `cobaya-install`. The cobaya wrapper `simonsobs/cosmopower_cobaya` wraps vanilla CosmoPower (TensorFlow), NOT cosmopower-jax. Use the JAX version's native Cobaya-compatible interface (`CosmoPowerJAX` subclass of `cobaya.theory.Theory`). Verify this interface exists before training by checking:
```bash
python -c "from cosmopower_jax.cosmopower_jax import CosmoPowerJAX; print(CosmoPowerJAX.__mro__)"
```

**TensorFlow/pkl compatibility note:** If loading pre-trained TF models, run the conversion script if TF >= 2.14: `python convert_tf214.py`. For fresh JAX training this is not needed.

**GO criterion:** emulator validation error < 0.5% on held-out 10% test set for all power spectrum multipoles; test Cobaya call with emulator returns consistent Z estimate vs CLASS direct (within 0.3 nat).

**Estimated time:** M5 ~3h, M9 ~4h on RTX 4090. Cost: 7h × $0.40/h = $2.80. Book a Profile S (RTX 4090) instance for both.

---

### BLOCKER 4 — pypolychord MPI compile on Vast.ai Docker (LXC limitations)
**Status: UNKNOWN — must verify on Profile S**

Known risk: Vast.ai uses LXC containers. OpenMPI's shared-memory transport (`btl_vader`) requires `/dev/shm` or POSIX shared memory, which can be restricted in unprivileged LXC containers. The `--mca btl_vader_single_copy_mechanism none` flag in the design doc is the correct mitigation, but it must be verified end-to-end.

**Resolution procedure:**
```bash
# After base setup on Profile S:
mpirun -np 4 --bind-to none \
       --mca btl_vader_single_copy_mechanism none \
       --oversubscribe \
       python -c "
from mpi4py import MPI
comm = MPI.COMM_WORLD
print(f'MPI rank {comm.Get_rank()} of {comm.Get_size()} — OK')
"

# Then run M1 PolyChord MPI sanity:
mpirun -np 4 --bind-to none \
       --mca btl_vader_single_copy_mechanism none \
       --oversubscribe \
       python -m cobaya run compute/C4_joint_mcmc/yamls/M1_sanity_nlive20.yaml
```

Additional MPI flags to try if vader still fails:
```
--mca btl ^vader,tcp,openib --mca oob_tcp_listen_mode listen_thread
```

For 64-vCPU Profile L, scale to 16 ranks (not 64 — PolyChord benefits from nlive/4 ranks; 16 ranks × 4 per A100 node = 64 live points active per GPU):
```
mpirun -np 16 --bind-to none --mca btl_vader_single_copy_mechanism none --oversubscribe \
       python -m cobaya run model.yaml
```

**GO criterion:** 4-rank MPI test completes on Profile S with no `btl_vader` crash or hang; M1 PolyChord nlive=20 run produces `log(Z)` consistent with local value (-712 ± 1 nat).

---

### BLOCKER 5 — Profile L availability + price confirmation
**Status: UNVERIFIED — check live before booking**

Verified market data (May 2026, search-confirmed):
- Single A100 80GB PCIe on Vast.ai marketplace: **$0.73–$2.00/h spot** (from Vast.ai pricing page)
- Multi-GPU markup: 4× A100 instance with 64 vCPU + 256 GB DDR5 adds CPU/RAM premium
- Realistic 4× A100 80GB PCIe spot price range: **$4–8/h** (not confirmed from live listing — MUST verify)
- The $5/h figure in design_doc_v1.md is a working estimate from VASTAI_SIZING.md; treat as provisional

**IMPORTANT:** Do NOT quote $5/h as confirmed. The marketplace is dynamic. Vast.ai spot prices for multi-GPU A100 instances have been observed from $3/h to $9/h depending on availability. Budget ceiling of $750 accommodates up to $7.50/h for 100h.

**Resolution procedure:**
```bash
# Install Vast.ai CLI
pip install vastai
vastai set api-key <YOUR_KEY>

# Search live listings for 4x A100 80GB PCIe
vastai search offers \
    'num_gpus=4 gpu_name=A100_PCIE gpu_ram>=79000 cpu_cores>=32 ram>=200000 disk_space>=200 reliability>0.95' \
    --type spot --order dph+

# Output columns: id, dph ($/h), gpu_name, num_gpus, cpu_cores, ram, disk
```

**GO criterion:** at least 3 listings available with dph < $7/h and reliability > 0.95 at booking time; total 100h cost < $700 (within $750 ceiling).

---

## 2. Docker Setup Script `vastai_setup.sh`

```bash
#!/usr/bin/env bash
# vastai_setup.sh — C4 Joint MCMC environment setup
# Target: Ubuntu 24.04 LTS + CUDA 12.x + Python 3.12
# Run as: bash vastai_setup.sh 2>&1 | tee setup.log
# Version: 2026-05-04

set -euo pipefail
PACKAGES_PATH="$(pwd)/packages"
VENV="$(pwd)/.venv-c4"
N_JOBS=$(nproc)

echo "=== [0/9] System update + base deps ==="
apt-get update -qq
apt-get install -y --no-install-recommends \
    build-essential gfortran gcc g++ \
    libgsl-dev libfftw3-dev libfftw3-mpi-dev \
    libopenblas-dev liblapack-dev \
    libhdf5-dev libcfitsio-dev \
    mpi-default-bin mpi-default-dev \
    libopenmpi-dev openmpi-bin \
    git wget curl unzip ca-certificates \
    python3.12 python3.12-dev python3.12-venv

# Verify AVX2 support (required for optimised OpenBLAS)
grep -m1 avx2 /proc/cpuinfo | grep -q avx2 && echo "AVX2: OK" || echo "WARNING: no AVX2 — OpenBLAS will use fallback"

echo "=== [1/9] Python venv ==="
python3.12 -m venv "$VENV"
source "$VENV/bin/activate"
pip install --upgrade pip wheel setuptools

echo "=== [2/9] Core Python packages ==="
pip install \
    mpi4py \
    numpy scipy matplotlib \
    astropy camb \
    cobaya==3.6.2 \
    cosmopower-jax \
    anesthetic \
    getdist \
    jax[cuda12_pip] -f https://storage.googleapis.com/jax-releases/jax_cuda_releases.html

echo "=== [3/9] Cobaya-managed likelihoods + data ==="
mkdir -p "$PACKAGES_PATH"
cobaya-install \
    bao.desi_dr2.desi_bao_all \
    sn.pantheonplus \
    "planck_2018_lowl.TT" \
    "planck_2018_lowl.EE" \
    "planck_2018_highl_plik.TTTEEE_lite" \
    "act_dr6_lenslike.ACTDR6LensLike" \
    --packages-path "$PACKAGES_PATH" \
    --no-set-preferences

echo "=== [4/9] PolyChord (pypolychord) ==="
cobaya-install polychord --packages-path "$PACKAGES_PATH"
# Verify MPI compile
python -c "import pypolychord; print('pypolychord OK:', pypolychord.__version__)"

echo "=== [5/9] AxiCLASS (M9 EDE) ==="
mkdir -p "$PACKAGES_PATH/code"
if [ ! -d "$PACKAGES_PATH/code/AxiCLASS" ]; then
    git clone https://github.com/PoulinV/AxiCLASS.git "$PACKAGES_PATH/code/AxiCLASS"
fi
cd "$PACKAGES_PATH/code/AxiCLASS"
make clean || true
make -j"$N_JOBS"
rm -f classy.c          # force Cython regen
make classy
pip install -e .
# Smoke-test
python -c "
import classy
c = classy.Class()
c.set({'f_EDE': 0.1, 'log10z_c': 3.5, 'thetai_scf': 1.5,
       'output': '', 'h': 0.68, 'omega_b': 0.022,
       'omega_cdm': 0.12, 'n_s': 0.96, 'A_s': 2.1e-9, 'tau_reio': 0.055})
c.compute()
c.struct_cleanup()
print('AxiCLASS EDE params: OK')
"
cd -

echo "=== [6/9] hi_class_public (M5 Coupled-DE, M6 DHOST, M10 NMC quint) ==="
if [ ! -d "$PACKAGES_PATH/code/hi_class_public" ]; then
    git clone https://github.com/miguelzuma/hi_class_public.git "$PACKAGES_PATH/code/hi_class_public"
fi
cd "$PACKAGES_PATH/code/hi_class_public"
make clean || true
make -j"$N_JOBS"
rm -f classy.c
make classy
# Smoke-test: Horndeski gravity_model
python -c "
import sys; sys.path.insert(0, '.')
import classy
c = classy.Class()
c.set({'gravity_model': 'propto_omega',
       'parameters_smg': '-0.1, 0.0, 0.5, 0',
       'output': '', 'h': 0.68, 'omega_b': 0.022,
       'omega_cdm': 0.12, 'n_s': 0.96, 'A_s': 2.1e-9, 'tau_reio': 0.055})
c.compute()
c.struct_cleanup()
print('hi_class Horndeski: OK')
"
cd -

echo "=== [7/9] ECI-specific likelihoods + plugins ==="
# Copy from repo (adjust path if running from within crossed-cosmos checkout)
REPO_ROOT="${REPO_ROOT:-$(pwd)}"
if [ -d "$REPO_ROOT/cobaya_nmc" ]; then
    pip install -e "$REPO_ROOT"
    echo "ECI cobaya_nmc plugins installed"
else
    echo "WARNING: cobaya_nmc not found at $REPO_ROOT — install manually"
fi

echo "=== [8/9] Dataset SHA256 verification ==="
# These must match pre-registration checksums in dataset_checksums.md
check_sha256() {
    local file="$1" expected="$2"
    if [ -f "$file" ]; then
        actual=$(sha256sum "$file" | cut -d' ' -f1)
        if [ "$actual" = "$expected" ]; then
            echo "SHA256 OK: $file"
        else
            echo "SHA256 MISMATCH: $file — ABORT" >&2; exit 1
        fi
    else
        echo "WARNING: $file not found — run cobaya-install first"
    fi
}
# Fill in actual SHA256 values from dataset_checksums.md before production run
# check_sha256 "$PACKAGES_PATH/data/bao_data/desi_dr2/desi_bao_dr2_data.txt" "REPLACE_WITH_ACTUAL"
# check_sha256 "$PACKAGES_PATH/data/sn_data/pantheon_plus/Pantheon+SH0ES.dat"  "REPLACE_WITH_ACTUAL"

echo "=== [9/9] MPI smoke-test ==="
mpirun -np 4 \
    --bind-to none \
    --mca btl_vader_single_copy_mechanism none \
    --oversubscribe \
    python -c "
from mpi4py import MPI
comm = MPI.COMM_WORLD
print(f'MPI OK: rank {comm.Get_rank()} of {comm.Get_size()}')
"

echo ""
echo "=== SETUP COMPLETE ==="
echo "Activate venv: source $VENV/bin/activate"
echo "Run production (16 ranks, Profile L 64-vCPU):"
echo "  mpirun -np 16 --bind-to none --mca btl_vader_single_copy_mechanism none --oversubscribe \\"
echo "         python -m cobaya run compute/C4_joint_mcmc/yamls/M1_production.yaml"
```

### Launch template (Profile L production — 10 models sequential per GPU node)

```bash
#!/usr/bin/env bash
# launch_c4_production.sh
# 4 x A100 80 GB PCIe, 64 vCPU, 256 GB DDR5
# Runs 10 models sequentially; each mpirun uses 16 ranks across 64 vCPU

set -euo pipefail
source .venv-c4/bin/activate
PACKAGES="$(pwd)/packages"
YAMLS="compute/C4_joint_mcmc/yamls"
LOG_DIR="logs/$(date +%Y%m%d_%H%M%S)"
mkdir -p "$LOG_DIR"

MPI_FLAGS="--bind-to none --mca btl_vader_single_copy_mechanism none --oversubscribe"
N_RANKS=16    # 16 ranks across 64 vCPU; PolyChord distributes live points

for MODEL in M1 M2 M3 M4 M5 M6 M7 M8 M9 M10; do
    YAML="$YAMLS/${MODEL}_production.yaml"
    LOG="$LOG_DIR/${MODEL}.log"
    echo "[$(date)] Starting $MODEL ..."
    mpirun -np $N_RANKS $MPI_FLAGS \
        python -m cobaya run "$YAML" \
        2>&1 | tee "$LOG"
    echo "[$(date)] $MODEL done. Exit code: ${PIPESTATUS[0]}"
done

echo "All models complete. Check $LOG_DIR for outputs."
```

---

## 3. Go/No-Go Matrix by Phase

| Phase | Instance | GPU | vCPU | RAM | Spot Price (verified range) | Duration | Estimated Cost | GO Trigger |
|---|---|---|---|---|---|---|---|---|
| **S: Sanity + AxiCLASS + hi_class + MPI** | Profile S | 1× RTX 4090 | 8 | 32 GB | ~$0.40/h | 8 h | ~$3.20 | Blockers 1, 2, 4 resolved |
| **S: cosmopower-jax training M5+M9** | Profile S | 1× RTX 4090 | 8 | 32 GB | ~$0.40/h | 7 h | ~$2.80 | Blocker 3 resolved |
| **L: Production 10 models** | Profile L | 4× A100 80G | 64 | 256 GB | $4–8/h (unconfirmed; verify live) | ~100 h | $400–800 | ALL 5 blockers GO + pre-reg tagged |
| **M: Post-processing + corners** | Profile M | 1× A6000 | 16 | 96 GB | ~$0.70/h | 24 h | ~$17 | Profile L chains complete |

**Decision gates:**
- Book Profile S immediately (< $10 risk, 5 blockers validated)
- Book Profile L ONLY after Profile S GO on all 5 blockers + `c4-preregistration-v1` tag in git
- Book Profile M after Profile L produces at minimum M1 + M2 converged outputs

**No-go triggers during Profile L (auto-stop conditions):**
- Spend > $600 with < 5/10 models converged → pause, partial report, evaluate second booking
- Any model R-1 > 5 after 10⁵ likelihood evaluations → kill, diagnose, narrow prior width
- M9 AxiCLASS ODE stiffness (EDE shooting failure rate > 30%) → switch to CPL proxy, flag in paper
- cosmopower-jax OOM on GPU → CPU CLASS fallback (adds ~5h per affected model)
- MPI deadlock (zero PolyChord progress for > 30 min) → SIGKILL, rerun with `--oversubscribe`

---

## 4. Vast.ai Alert Configuration

Set these BEFORE booking any paid instance. Vast.ai supports email alerts and instance-level spend caps.

```
Spend alerts (email + auto-pause):
  Alert 1:  $200  — email notification only
  Alert 2:  $400  — email notification only
  Alert 3:  $600  — AUTO-PAUSE all instances

Per-instance hourly cap:
  Profile L: set instance max_bid = $8.00/h (safety ceiling above expected $4-6)
  Profile S: set instance max_bid = $0.60/h
```

Vast.ai CLI to set spend limits:
```bash
# Set account-level alert (via web dashboard — no CLI command as of 2026)
# Navigate to: https://vast.ai/account → Billing → Spending Alerts
# Add alerts at $200, $400, $600

# Per-instance max bid (set at creation time):
vastai create instance <OFFER_ID> \
    --image pytorch/pytorch:2.4.0-cuda12.1-cudnn9-devel \
    --disk 200 \
    --label "c4-production" \
    --bid-per-gpu 2.00       # max $/GPU/h; 4-GPU instance → max $8/h total
```

**CRITICAL:** Vast.ai does NOT have native hard-spend-cap enforcement as of 2026 — the $600 auto-pause is a dashboard alert that sends an email; you must manually stop the instance or use a cron job on the instance to self-terminate. Add to launch script:

```bash
# Self-terminate guard (add to launch_c4_production.sh header)
BUDGET_CEILING_USD=600
HOURLY_RATE=6   # conservative estimate; update to actual dph after booking
MAX_HOURS=$(echo "$BUDGET_CEILING_USD / $HOURLY_RATE" | bc)
echo "Instance will self-terminate after $MAX_HOURS hours if still running"
(sleep $((MAX_HOURS * 3600)) && echo "BUDGET CEILING REACHED — TERMINATING" && \
 python -m cobaya stop 2>/dev/null; shutdown -h now) &
BUDGET_GUARD_PID=$!
```

---

## 5. Estimated Total Cost + Reserve Breakdown

| Item | Cost (estimated) | Notes |
|---|---|---|
| Profile S sanity (8h × $0.40) | $3.20 | Blockers 1, 2, 4 validation |
| Profile S emulator training (7h × $0.40) | $2.80 | Blocker 3: M5 + M9 cosmopower-jax |
| Profile L production (100h × $5–8/h) | $500–800 | Central estimate $550 at $5.5/h |
| Profile M post-processing (24h × $0.70) | $16.80 | Corners, suspiciousness maps |
| **Subtotal committed** | **~$522–822** | Wide range due to A100 spot variability |
| Reserve for restarts / extra M9 runs | $200 | Hard ceiling buffer |
| **Ceiling** | **$750** | Do not exceed without explicit decision |

**Cost sensitivity:** The single biggest variable is Profile L hourly rate. At $5/h: $500 for 100h. At $7/h: $700. Confirm live price via `vastai search offers` before booking. If > $7/h, either wait for better spot availability or reduce to 80h (drop M7 Holo-Tsallis from production; it is the lowest-priority model per discrimination matrix).

**Budget if emulators work as expected:** M5 and M9 via cosmopower-jax should each be ~10× faster than direct CLASS evaluation, saving ~30h of Profile L time → ~$150-$225 saved → total closer to $330-400 in Profile L.

---

## 6. Pre-Registration Commit Checklist

Tag `c4-preregistration-v1` before ANY Profile L booking. This is the anti-p-hacking gate.

```
compute/C4_joint_mcmc/preregistration/
├── design_doc_v1.md            DONE — locked priors, 10 models, Jeffreys thresholds
├── model_definitions.yaml      TODO — generate from design_doc_v1.md §2
├── likelihood_config.yaml      TODO — exact Cobaya module names + versions
├── sampler_config.yaml         TODO — nlive/num_repeats per model (nlive=500, 1000 for M9)
├── dataset_checksums.md        TODO — SHA256 of DESI DR2, Pantheon+, ACT DR6 files
└── decision_criteria.md        TODO — §7 thresholds verbatim (copy from design_doc)
```

### Amendment protocol (pre-registered)
- S8 prior: design_doc currently specifies KiDS-1000 value 0.759 +0.024/-0.021 (Asgari 2021). The KiDS-Legacy 2025 value (Wright et al. 2503.19441) gives S8 = 0.815 +0.016/-0.021. The `eci_kids_s8.py` likelihood wrapper must be patched to KiDS-Legacy BEFORE the pre-registration tag. Document the change in the tag message with arXiv ID. This is an active discrepancy in design_doc_v1.md §3 (the document itself flags it as "UPDATE NEEDED").
- Any subsequent prior change → tag `c4-preregistration-v2` with changelog. Both analyses reported in paper.

### Git commands:
```bash
cd /root/crossed-cosmos

# 1. Create required YAML stubs (fill in from design_doc_v1.md before tagging)
python compute/C4_joint_mcmc/preregistration/generate_yamls.py   # if script exists
# or manually create model_definitions.yaml, sampler_config.yaml, decision_criteria.md

# 2. Patch S8 likelihood (MANDATORY before tag)
# Edit cobaya_nmc/eci_kids_s8.py:
#   s8_mean = 0.815  (KiDS-Legacy 2025, Wright et al. 2503.19441)
#   s8_sigma_plus = 0.016
#   s8_sigma_minus = 0.021
# Or add --s8-dataset flag that accepts 'kids1000' | 'kids_legacy'

# 3. SHA256 dataset checksums (run after cobaya-install on Profile S)
sha256sum packages/data/bao_data/desi_dr2/desi_bao_dr2_data.txt \
           packages/data/sn_data/pantheon_plus/Pantheon+SH0ES.dat \
    > compute/C4_joint_mcmc/preregistration/dataset_checksums.md

# 4. Stage + commit
git add compute/C4_joint_mcmc/preregistration/
git add cobaya_nmc/eci_kids_s8.py
git commit -m "pre-registration C4 joint MCMC v1 — lock priors/sampler/thresholds/datasets

ECI v6.0.45. 10 models, PolyChord nlive=500 (1000 EDE), Jeffreys thresholds locked.
S8 updated to KiDS-Legacy 2025: 0.815 +0.016/-0.021 (Wright et al. 2503.19441).
ECI falsification window pre-registered: log B_(M2,M1) in [-3,+1] = not falsified.
Anti-p-hacking gate: no Profile L booking before this tag."

# 5. Tag
git tag -a c4-preregistration-v1 -m "C4 pre-registration v1 — 2026-05-04 $(date +%H:%M) UTC"

# 6. Push (to Zenodo-backed or GitHub repo)
git push origin main
git push origin c4-preregistration-v1
```

---

## 7. One-Line Verdict

**NOT READY TO BOOK PROFILE L NOW.**

5 blockers must close first:
1. AxiCLASS EDE params compile + Cobaya wire-up (NO-GO — local failure confirmed)
2. hi_class_public Python wrapper compile (NO-GO — `make classy` not run)
3. cosmopower-jax emulator training for M5 + M9 (NO-GO — training not done; saves ~$150-230)
4. pypolychord MPI test on Vast.ai LXC (UNKNOWN — must verify on Profile S)
5. Profile L live price confirmation < $7/h (UNVERIFIED — search shows $0.73/GPU/h single, multi-GPU total unconfirmed)

**Immediate action:** Book 1× Profile S (RTX 4090, ~$0.40/h, 15h = $6) to close blockers 1, 2, 3, 4 in parallel. Then commit + tag `c4-preregistration-v1`. Then verify Profile L spot price live. Then — and only then — book Profile L.

---

*Sources consulted (2026-05-04): [Vast.ai GPU Pricing](https://vast.ai/pricing), [Vast.ai A100 PCIe page](https://vast.ai/pricing/gpu/A100-PCIE), [cosmopower-jax GitHub](https://github.com/dpiras/cosmopower-jax), [AxiCLASS GitHub](https://github.com/PoulinV/AxiCLASS), [hi_class_public wiki](https://github.com/miguelzuma/hi_class_public/wiki/classy:-the-python-wrapper), [HTJense cobaya-cosmopower](https://github.com/HTJense/cobaya-cosmopower), [Cobaya 3.6.2 docs](https://cobaya.readthedocs.io/en/latest/theory_class.html)*
