#!/usr/bin/env bash
# =============================================================================
# vastai-physics-postinstall.sh — user-level Python venv with the full
#                                 computational physics stack.
#
# Runs WITHOUT sudo. Assumes vastai-physics-setup.sh was run as root first.
#
# Creates: ~/.venv/physics  (or VENV_DIR if set)
#
# Stack:
#   - numpy < 2 (ABI compat with classy etc.), scipy, sympy, mpmath, h5py, pandas
#   - JAX with CUDA 12 wheel, PyTorch with CUDA 12.4 wheel
#   - Cobaya, PolyChord, dynesty, nautilus-sampler, ultranest, emcee, zeus-mcmc
#   - GetDist, anesthetic, chainconsumer, corner, arviz
#   - camb, classy_sz, cosmopower, cosmopower_jax
#   - GUDHI (Python), ripser, persim (persistent homology)
#   - sympy, mpmath, primesieve (number theory / Riemann zeros)
#   - LLM/ML side: transformers, datasets, accelerate, vllm (optional, GPU only)
#   - Then: AxiCLASS + hi_class compiled with -O3 -march=native, pip-installed
#
# Usage:   bash vastai-physics-postinstall.sh
#          [VENV_DIR=~/myvenv bash vastai-physics-postinstall.sh]
# =============================================================================

set -euo pipefail

VENV_DIR="${VENV_DIR:-$HOME/.venv/physics}"

if [[ ! -f /etc/profile.d/vastai-physics.sh ]]; then
    echo "WARNING: /etc/profile.d/vastai-physics.sh missing. Run vastai-physics-setup.sh first."
fi
[[ -f /etc/profile.d/vastai-physics.sh ]] && source /etc/profile.d/vastai-physics.sh

CPU_CORES=$(nproc)
JOBS=$((CPU_CORES > 16 ? 16 : CPU_CORES))   # cap at 16 to avoid ld OOM on big repos

GPU_PRESENT=0
if command -v nvidia-smi &>/dev/null && nvidia-smi -L | grep -q GPU; then
    GPU_PRESENT=1
    GPU_NAME=$(nvidia-smi --query-gpu=name --format=csv,noheader | head -1)
    echo ">> GPU detected: $GPU_NAME"
fi

# ----------------------------- 1. venv -------------------------------------
echo ">> [1/9] Creating venv at $VENV_DIR"
mkdir -p "$(dirname "$VENV_DIR")"
if [[ ! -d "$VENV_DIR" ]]; then
    python3 -m venv "$VENV_DIR"
fi
# shellcheck disable=SC1090
source "$VENV_DIR/bin/activate"
pip install --upgrade pip wheel setuptools build packaging

# ----------------------------- 2. Core scientific (numpy<2 critical) -------
echo ">> [2/9] Core scientific (numpy<2 for classy ABI, scipy, sympy, mpmath, h5py, pandas)"
pip install --upgrade \
    "numpy<2" "scipy>=1.13" sympy mpmath h5py pandas \
    matplotlib seaborn plotly bokeh ipython jupyter rich tqdm \
    Cython wheel build

# ----------------------------- 3. JAX + PyTorch (CUDA 12) ------------------
echo ">> [3/9] JAX + PyTorch with CUDA"
if [[ $GPU_PRESENT -eq 1 ]]; then
    pip install --upgrade "jax[cuda12]" "jaxlib"
    pip install --upgrade torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu124 || \
    pip install --upgrade torch torchvision torchaudio  # fallback to default
else
    echo "  no GPU — installing CPU-only JAX/torch"
    pip install --upgrade jax jaxlib torch
fi

# ----------------------------- 4. MCMC / nested sampling -------------------
echo ">> [4/9] MCMC + nested sampling stack"
pip install --upgrade \
    "cobaya[mcmc]" \
    "polychord-py3" \
    dynesty nautilus-sampler ultranest \
    emcee zeus-mcmc \
    pymc pyro-ppl numpyro \
    optuna nevergrad

# ----------------------------- 5. Posterior analysis + plots ---------------
echo ">> [5/9] Posterior analysis"
pip install --upgrade \
    getdist anesthetic chainconsumer corner arviz \
    samana

# ----------------------------- 6. Cosmology emulators / Boltzmann backups --
echo ">> [6/9] Cosmology side libraries"
pip install --upgrade camb classy_sz \
    cosmopower cosmopower_jax \
    halomod hmf

# ----------------------------- 7. Math libraries --------------------------
echo ">> [7/9] Persistent homology + number theory"
pip install --upgrade \
    gudhi ripser persim giotto-tda \
    primesieve

# ----------------------------- 8. LLM / ML side (Chimère) ------------------
echo ">> [8/9] LLM / ML side"
pip install --upgrade \
    transformers datasets accelerate sentencepiece tokenizers \
    "huggingface_hub[cli]" peft trl bitsandbytes \
    safetensors einops xformers \
    || echo "  (some ML wheels failed — non-fatal, continue)"
# vllm only if recent CUDA + sufficient RAM
if [[ $GPU_PRESENT -eq 1 ]] && [[ $(free -g | awk '/^Mem:/{print $2}') -ge 32 ]]; then
    pip install --upgrade vllm 2>/dev/null || echo "  vllm install skipped"
fi

# ----------------------------- 9. AxiCLASS + hi_class native build ---------
echo ">> [9/9] AxiCLASS + hi_class — clone & native build"
SRC_DIR="$HOME/src"
mkdir -p "$SRC_DIR"
cd "$SRC_DIR"

# AxiCLASS (Poulin EDE branch)
if [[ ! -d AxiCLASS ]]; then
    git clone --depth 1 https://github.com/PoulinV/AxiCLASS.git
fi
( cd AxiCLASS && make clean >/dev/null 2>&1 || true
  echo "  building AxiCLASS with -j$JOBS native flags"
  make -j$JOBS CC=gcc OPTFLAG="-O3 -march=native -ffast-math -fopenmp" 2>&1 | tail -5
  cd python && pip install -e . 2>&1 | tail -3 ) || echo "  AxiCLASS build had issues — check $SRC_DIR/AxiCLASS/Makefile"

# hi_class
if [[ ! -d hi_class_public ]]; then
    git clone --depth 1 https://github.com/miguelzuma/hi_class_public.git
fi
( cd hi_class_public && make clean >/dev/null 2>&1 || true
  echo "  building hi_class with -j$JOBS native flags"
  make -j$JOBS CC=gcc OPTFLAG="-O3 -march=native -ffast-math -fopenmp" 2>&1 | tail -5
  cd python && pip install -e . 2>&1 | tail -3 ) || echo "  hi_class build had issues"

# ----------------------------- Smoke tests --------------------------------
echo ""
echo "=========================================================================="
echo "SMOKE TESTS"
echo "=========================================================================="
python -c "
import sys
print(f'Python:      {sys.version.split()[0]}')
import numpy, scipy, sympy, mpmath
print(f'numpy:       {numpy.__version__}')
print(f'scipy:       {scipy.__version__}')
print(f'sympy:       {sympy.__version__}')
print(f'mpmath:      {mpmath.__version__}')

try:
    import jax
    print(f'jax:         {jax.__version__}  devices={jax.devices()}')
except Exception as e:
    print(f'jax:         ERROR {e}')

try:
    import torch
    print(f'torch:       {torch.__version__}  cuda={torch.cuda.is_available()}  device_count={torch.cuda.device_count()}')
except Exception as e:
    print(f'torch:       ERROR {e}')

try:
    import classy
    cl = classy.Class()
    cl.set({'output': 'tCl'})
    cl.compute()
    print(f'classy:      OK (computed tCl)')
except Exception as e:
    print(f'classy:      ERROR {e}')

try:
    import cobaya
    print(f'cobaya:      {cobaya.__version__}')
except Exception as e:
    print(f'cobaya:      ERROR {e}')

try:
    import gudhi
    print(f'gudhi:       {gudhi.__version__}')
except Exception as e:
    print(f'gudhi:       ERROR {e}')
" || true

cat <<EOF

==========================================================================
POSTINSTALL DONE.

Activate the venv:
   source $VENV_DIR/bin/activate

Or persist:
   echo 'source $VENV_DIR/bin/activate' >> ~/.bashrc

Sources cloned:  $SRC_DIR/AxiCLASS  $SRC_DIR/hi_class_public

Quick MCMC launch template:
   mpirun -np 4 --bind-to core --map-by socket cobaya-run path/to/your.yaml
==========================================================================
EOF
