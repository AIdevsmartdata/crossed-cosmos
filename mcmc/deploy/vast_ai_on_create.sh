#!/usr/bin/env bash
# Vast.ai On-start script for ECI NMC MCMC.
# Paste the contents of this file into the "On-start Script" textbox
# when creating the instance. Runs as root, once, at first boot.
#
# Constraints propagated from mcmc/benchmark/REPORT.md:
#   - hi_class Cython requires numpy<2  -> pin numpy==1.26.4
#   - CLASS Makefile default -pthread does NOT enable OpenMP
#     -> must set OMPFLAG=-fopenmp and add -fopenmp to CFLAGS/LDFLAGS
#   - Plik-lite is the production likelihood (handled by YAML, not here)
#   - Cobaya builtin checkpointing handles spot preemption (handled at run time)

set -euo pipefail
export DEBIAN_FRONTEND=noninteractive

LOG=/var/log/onstart.log
exec > >(tee -a "$LOG") 2>&1
echo ">>> Vast.ai on-create start: $(date -Iseconds)"

# ---------------------------------------------------------------------------
# 1. System packages
# ---------------------------------------------------------------------------
apt-get update -y
apt-get install -y --no-install-recommends \
    git build-essential gfortran \
    libgsl-dev libcfitsio-dev \
    libopenmpi-dev openmpi-bin libomp-dev \
    tmux curl rsync ca-certificates \
    python3.11 python3.11-venv python3.11-dev \
    htop less

# ---------------------------------------------------------------------------
# 2. Source checkout
# ---------------------------------------------------------------------------
cd /root
if [ ! -d eci ]; then
    git clone --depth 1 https://github.com/AIdevsmartdata/crossed-cosmos.git eci
fi
cd /root/eci

# ---------------------------------------------------------------------------
# 3. Python venv with numpy<2 pin (hi_class Cython ABI constraint)
# ---------------------------------------------------------------------------
python3.11 -m venv .venv-mcmc
# shellcheck disable=SC1091
source .venv-mcmc/bin/activate
pip install --upgrade pip wheel

pip install \
    'numpy==1.26.4' \
    'scipy>=1.11,<1.14' \
    'matplotlib>=3.7' \
    'cython<3.1' \
    'mpi4py>=3.1' \
    'cobaya>=3.5' \
    'getdist>=1.5' \
    'pyyaml' 'tqdm' 'dill' 'packaging' 'requests'

# ---------------------------------------------------------------------------
# 4. Build CLASS / hi_class with EXPLICIT OpenMP
#    (Makefile default -pthread does NOT enable OpenMP — benchmark §4.3)
# ---------------------------------------------------------------------------
cd /root/eci/mcmc/nmc_patch/hi_class_nmc
make clean || true

OMPFLAG="-fopenmp" \
CFLAGS="-O3 -march=native -mavx2 -mtune=native -flto -fopenmp" \
LDFLAGS="-fopenmp -flto" \
    make -j"$(nproc)" class

# Sanity: binary must contain OpenMP symbols.
if ! nm -D class 2>/dev/null | grep -qi omp; then
    if ! ldd class | grep -qi gomp; then
        echo "!!! CLASS binary missing OpenMP — aborting." >&2
        exit 1
    fi
fi

# classy Python binding against the freshly built libclass.
# --no-build-isolation: reuse the venv's Cython instead of PEP 517 isolated
# build env (which lacks Cython and fails). Verified locally 2026-04-22.
pip install --no-build-isolation -e python/

# ---------------------------------------------------------------------------
# 5. Cobaya packages (Planck 2018 + DESI DR2 + Pantheon+)
#    Skip CAMB: we use classy only.
# ---------------------------------------------------------------------------
cd /root/eci
mkdir -p mcmc/packages
cobaya-install cosmo -p mcmc/packages/ --skip camb --no-progress-bars

# ---------------------------------------------------------------------------
# 6. Convenience: auto-activate venv on interactive SSH
# ---------------------------------------------------------------------------
cat >> /root/.bashrc <<'EOF'
# ECI MCMC env
if [ -f /root/eci/.venv-mcmc/bin/activate ]; then
    # shellcheck disable=SC1091
    source /root/eci/.venv-mcmc/bin/activate
    cd /root/eci
fi
EOF

echo ">>> Vast.ai on-create complete: $(date -Iseconds)"
echo ">>> SSH in and run:  bash mcmc/deploy/run_vast.sh   (inside tmux)"
