#!/usr/bin/env bash
# Vast.ai On-start script for ECI NMC MCMC (PLUGIN ROUTE, v5.0).
# Paste the contents of this file into the "On-start Script" textbox
# when creating the instance. Runs as root, once, at first boot.
#
# This script installs the Python-plugin route:
#   - vanilla CLASS (`classy`) — NOT the hi_class NMC C patch
#   - Cobaya `ECINMCTheory` plugin from mcmc/cobaya_nmc/ (added to PYTHONPATH
#     by the plugin's `python_path: ./mcmc/cobaya_nmc/` field in the YAML,
#     resolved relative to Cobaya's working directory = /root/eci)
#   - Likelihoods: bao.desi_dr2 + sn.pantheonplus only (no Planck)
#
# The C-patch route (hi_class_nmc) is NOT installed here. It is kept in-tree
# at mcmc/nmc_patch/hi_class_nmc/ for the v5.1 CMB-joint analysis.

set -euo pipefail
export DEBIAN_FRONTEND=noninteractive

LOG=/var/log/onstart.log
exec > >(tee -a "$LOG") 2>&1
echo ">>> Vast.ai on-create start (PLUGIN ROUTE): $(date -Iseconds)"

# ---------------------------------------------------------------------------
# 1. System packages
# ---------------------------------------------------------------------------
apt-get update -y
apt-get install -y --no-install-recommends \
    git build-essential gfortran \
    libgsl-dev libcfitsio-dev \
    libopenmpi-dev openmpi-bin libomp-dev \
    tmux curl rsync ca-certificates \
    python3 python3-venv python3-dev \
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
# 3. Python venv
#    numpy<2 pin preserved for classy ABI compatibility (classy Cython is
#    still built against numpy 1.x in most wheels as of Apr 2026).
# ---------------------------------------------------------------------------
python3 -m venv .venv-mcmc
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
    'classy' \
    'pyyaml' 'tqdm' 'dill' 'packaging' 'requests'

# Sanity: classy imports and runs a background compute.
python - <<'PY'
from classy import Class
c = Class()
c.set({'output':'mPk', 'H0':67.36})
c.compute()
print("classy OK, h =", c.h())
PY

# ---------------------------------------------------------------------------
# 4. Sanity: ECINMCTheory plugin imports.
#    Cobaya resolves the plugin via the YAML's `python_path: ./mcmc/cobaya_nmc/`
#    at run time; we just confirm the file parses.
# ---------------------------------------------------------------------------
python - <<'PY'
import sys, os
sys.path.insert(0, '/root/eci/mcmc/cobaya_nmc')
from eci_nmc_theory import ECINMCTheory
print("ECINMCTheory OK:", ECINMCTheory.__name__)
PY

# ---------------------------------------------------------------------------
# 5. Cobaya data packages — DESI DR2 + Pantheon+ only.
#    Skip camb (we use classy), skip Planck (plugin route has no CMB).
# ---------------------------------------------------------------------------
cd /root/eci
mkdir -p mcmc/packages
cobaya-install \
    bao.desi_dr2.desi_bao_all \
    sn.pantheonplus \
    -p mcmc/packages/ \
    --skip camb --no-progress-bars

# ---------------------------------------------------------------------------
# 6. Convenience: auto-activate venv on interactive SSH
# ---------------------------------------------------------------------------
cat >> /root/.bashrc <<'EOF'
# ECI MCMC env (plugin route)
if [ -f /root/eci/.venv-mcmc/bin/activate ]; then
    # shellcheck disable=SC1091
    source /root/eci/.venv-mcmc/bin/activate
    cd /root/eci
fi
EOF

echo ">>> Vast.ai on-create complete (PLUGIN ROUTE): $(date -Iseconds)"
echo ">>> SSH in and run:  bash mcmc/deploy/run_vast.sh   (inside tmux)"
