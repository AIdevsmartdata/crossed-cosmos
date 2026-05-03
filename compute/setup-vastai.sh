#!/usr/bin/env bash
# setup-vastai.sh — bootstrap a Vast.ai instance for the ECI numerical campaign.
#
# Usage on a fresh Vast.ai instance:
#   wget https://raw.githubusercontent.com/AIdevsmartdata/crossed-cosmos/main/compute/setup-vastai.sh
#   bash setup-vastai.sh
#
# Then `cd ~/crossed-cosmos/compute/CN_*/` and run the per-item README.
#
# Tested image baseline: pytorch/pytorch:2.4.0-cuda12.1-cudnn9-runtime
# OR: nvidia/cuda:12.4.1-cudnn-devel-ubuntu22.04
#
# Critical Docker/MPI quirks (carry-over from scripts/vastai/launch-mcmc.sh):
#   --bind-to none, --mca btl_vader_single_copy_mechanism none, --oversubscribe

set -euo pipefail

REPO_HTTPS="https://github.com/AIdevsmartdata/crossed-cosmos.git"
INSTALL_ROOT="${HOME}/crossed-cosmos"
VENV="${HOME}/.venv/physics"
LOG_DIR="${HOME}/setup-vastai-logs"
mkdir -p "$LOG_DIR"

echo "=== [0/8] system info ==="
{ uname -a; nvidia-smi || true; nproc; free -h; df -h .; } | tee "$LOG_DIR/00_sysinfo.log"

echo "=== [1/8] system deps ==="
sudo apt-get update -qq 2>&1 | tee "$LOG_DIR/10_apt.log"
sudo apt-get install -yq --no-install-recommends \
    git build-essential gfortran cmake ninja-build pkg-config \
    libopenblas-dev liblapack-dev libfftw3-dev libfftw3-mpi-dev \
    libopenmpi-dev openmpi-bin openmpi-common \
    libgsl-dev libcfitsio-dev \
    python3-dev python3-venv python3-pip \
    curl wget jq htop tmux vim 2>&1 | tee -a "$LOG_DIR/10_apt.log"

echo "=== [2/8] clone repo ==="
if [[ ! -d "$INSTALL_ROOT" ]]; then
    git clone --depth 1 "$REPO_HTTPS" "$INSTALL_ROOT" 2>&1 | tee "$LOG_DIR/20_clone.log"
else
    git -C "$INSTALL_ROOT" pull --ff-only 2>&1 | tee "$LOG_DIR/20_clone.log"
fi

echo "=== [3/8] python venv ==="
python3 -m venv "$VENV"
# shellcheck disable=SC1090
source "$VENV/bin/activate"
pip install -U pip wheel 2>&1 | tee "$LOG_DIR/30_pip_base.log"

echo "=== [4/8] core scientific stack ==="
pip install \
    "numpy<2" scipy sympy mpmath \
    matplotlib seaborn corner getdist \
    h5py pandas tqdm rich \
    pytest pytest-cov hypothesis \
    2>&1 | tee "$LOG_DIR/40_pip_sci.log"

echo "=== [5/8] JAX cuda12 + accelerators ==="
pip install --upgrade "jax[cuda12]" 2>&1 | tee "$LOG_DIR/50_pip_jax.log"
python -c "import jax; print('JAX devices:', jax.devices())" 2>&1 | tee -a "$LOG_DIR/50_pip_jax.log"

echo "=== [6/8] MCMC stack (Cobaya + AxiCLASS + cosmopower) ==="
pip install \
    cobaya \
    cosmopower-jax \
    anesthetic chainconsumer \
    emcee \
    2>&1 | tee "$LOG_DIR/60_pip_mcmc.log"

# AxiCLASS
if [[ ! -d "${HOME}/AxiCLASS" ]]; then
    git clone --depth 1 https://github.com/PoulinV/AxiCLASS.git "${HOME}/AxiCLASS"
    pushd "${HOME}/AxiCLASS"
    make -j"$(nproc)" 2>&1 | tee "$LOG_DIR/61_axiclass_make.log" || true
    pushd python
    pip install -e . 2>&1 | tee -a "$LOG_DIR/61_axiclass_make.log"
    popd
    popd
fi

echo "=== [7/8] tensor-network stack (for C3 DMRG/MERA) ==="
pip install \
    tenpy \
    quimb \
    opt-einsum \
    2>&1 | tee "$LOG_DIR/70_pip_tn.log"

echo "=== [8/8] sanity checks ==="
{
    python -c "import jax; print('jax', jax.__version__, 'devices', jax.devices())"
    python -c "import cobaya; print('cobaya', cobaya.__version__)"
    python -c "import classy; print('classy', classy.__version__)" || echo "classy not yet importable; rebuild AxiCLASS if needed"
    python -c "import tenpy; print('tenpy', tenpy.__version__)"
    python -c "import sympy, mpmath; print('sympy', sympy.__version__, 'mpmath', mpmath.__version__)"
} | tee "$LOG_DIR/80_sanity.log"

cat <<EOF

=== setup complete ===

To activate the env in a new shell:
    source $VENV/bin/activate

To re-source MPI flags:
    source /etc/profile.d/vastai-physics.sh   # if present

Items ready to run:
    cd $INSTALL_ROOT/compute/C1_fv_qei_bounce && cat README.md
    cd $INSTALL_ROOT/compute/C2_holographic_complexity && cat README.md
    cd $INSTALL_ROOT/compute/C3_dmrg_krylov && cat README.md
    cd $INSTALL_ROOT/compute/C4_joint_mcmc && cat README.md
    cd $INSTALL_ROOT/compute/C5_hadamard_bvii0 && cat README.md

Setup logs in $LOG_DIR/

EOF
