#!/usr/bin/env bash
# =============================================================================
# vastai-physics-setup.sh — full system-level setup for theoretical/computational
#                           physics research on a Vast.ai instance.
# =============================================================================
# Targets: Ubuntu 22.04 or 24.04 with NVIDIA GPU (CUDA 12.x driver pre-installed
# by the Vast.ai image). Auto-detects CPU AVX support and GPU compute capability
# and configures CFLAGS / CUDA arch accordingly.
#
# Domains covered:
#   - Cosmology: CLASS / AxiCLASS / hi_class / Cobaya / PolyChord / GetDist
#   - Quantum gravity / math.OA: sympy, mpmath, numpy with high-precision support
#   - Persistent homology: GUDHI, Ripser
#   - Number theory: mpmath, primesieve (Riemann zeros, v7-note)
#   - ML / LLM (Chimère side): PyTorch CUDA, transformers, vllm
#   - LaTeX: full publishers stack
#   - Build chain: GCC 13 + gfortran + cmake + ninja
#   - Numerics: OpenBLAS pthreads, LAPACK, FFTW3 MPI, GSL, HDF5 MPI
#   - Parallel: OpenMPI + hwloc + numactl
#   - Monitoring: nvtop, htop, iotop, dstat, sysstat
#
# Usage:   sudo bash vastai-physics-setup.sh
# =============================================================================

set -euo pipefail

if [[ $EUID -ne 0 ]]; then
    echo "ERROR: must run as root.  sudo bash $0" >&2
    exit 1
fi

echo "=========================================================================="
echo "  vastai-physics-setup.sh — $(date)"
echo "=========================================================================="

# ----------------------------- 0. Hardware detect ---------------------------
echo ">> [0/12] Hardware detection"
CPU_MODEL=$(grep -m1 "model name" /proc/cpuinfo | sed 's/model name[ \t]*: //')
CPU_CORES=$(nproc)
RAM_GB=$(free -g | awk '/^Mem:/{print $2}')
HAS_AVX2=$(grep -m1 -o avx2 /proc/cpuinfo || true)
HAS_AVX512=$(grep -m1 -o avx512f /proc/cpuinfo || true)
CPU_VENDOR=$(grep -m1 vendor_id /proc/cpuinfo | awk '{print $3}')

GPU_NAME="(none)"
GPU_CC=""
if command -v nvidia-smi &>/dev/null; then
    GPU_NAME=$(nvidia-smi --query-gpu=name --format=csv,noheader | head -1)
    # compute capability via deviceQuery is heavy; rely on name → arch table
    case "$GPU_NAME" in
        *H100*)     GPU_CC=90 ;;
        *A100*)     GPU_CC=80 ;;
        *A6000*|*A40*) GPU_CC=86 ;;
        *RTX*40*|*L40*|*4090*|*4080*|*4070*|*4060*) GPU_CC=89 ;;
        *RTX*50*|*5090*|*5080*|*5070*|*5060*|*Blackwell*) GPU_CC=120 ;;
        *RTX*30*|*3090*|*3080*|*3070*|*3060*) GPU_CC=86 ;;
        *V100*)     GPU_CC=70 ;;
        *)          GPU_CC=80 ;;  # safe default for unknown
    esac
fi

echo "    CPU:     $CPU_MODEL"
echo "    cores:   $CPU_CORES"
echo "    RAM:     ${RAM_GB} GB"
echo "    AVX2:    ${HAS_AVX2:-no}"
echo "    AVX512:  ${HAS_AVX512:-no}"
echo "    GPU:     $GPU_NAME"
echo "    GPU CC:  sm_${GPU_CC}"

# Pick CFLAGS — keep -march=native (instance-specific), add lane width as fallback
CFLAGS_TUNING="-O3 -march=native -ffast-math -fopenmp -fPIC"

# OpenBLAS coretype: only set if not native-tuned, else let runtime pick
OPENBLAS_CORETYPE_HINT=""
if [[ -n "$HAS_AVX512" ]]; then OPENBLAS_CORETYPE_HINT="SkylakeX"
elif [[ -n "$HAS_AVX2" ]];  then OPENBLAS_CORETYPE_HINT="Haswell"
fi

# ----------------------------- 1. apt update -------------------------------
echo ""
echo ">> [1/12] apt update"
apt-get update -qq

# ----------------------------- 2. Build essentials -------------------------
echo ">> [2/12] Build chain (gcc, gfortran, cmake, ninja, ccache)"
apt-get install -y --no-install-recommends \
    build-essential gcc g++ gfortran \
    cmake ninja-build pkg-config ccache \
    git wget curl ca-certificates gnupg jq unzip xz-utils \
    rsync less tmux

# ----------------------------- 3. Linear algebra ---------------------------
echo ">> [3/12] BLAS/LAPACK/FFTW3/GSL/HDF5 with MPI variants"
apt-get install -y --no-install-recommends \
    libopenblas-dev libopenblas-pthread-dev \
    liblapack-dev liblapacke-dev \
    libfftw3-dev libfftw3-mpi-dev libfftw3-bin \
    libgsl-dev libgsl27 \
    libhdf5-dev libhdf5-mpi-dev hdf5-tools

# ----------------------------- 4. MPI + topology pinning -------------------
echo ">> [4/12] OpenMPI + hwloc + numactl"
apt-get install -y --no-install-recommends \
    openmpi-bin openmpi-common libopenmpi-dev \
    libhwloc-dev hwloc \
    numactl libnuma-dev

# ----------------------------- 5. Python toolchain -------------------------
echo ">> [5/12] Python build deps + system mpi4py"
apt-get install -y --no-install-recommends \
    python3 python3-dev python3-pip python3-venv \
    python3-mpi4py cython3

# ----------------------------- 6. Persistent homology / number theory ------
echo ">> [6/12] GUDHI + libprimesieve + libsuitesparse"
apt-get install -y --no-install-recommends \
    libgudhi-dev libgmp-dev libmpfr-dev libmpc-dev \
    libcgal-dev libeigen3-dev libsuitesparse-dev \
    libprimesieve-dev primesieve

# ----------------------------- 7. NLopt + nested sampling deps -------------
echo ">> [7/12] NLopt + Multinest fallback deps"
apt-get install -y --no-install-recommends \
    libnlopt-dev libnlopt-cxx-dev libboost-all-dev

# ----------------------------- 8. LaTeX (paper-quality plots + builds) ----
echo ">> [8/12] LaTeX full publisher stack"
DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
    texlive-latex-base texlive-latex-extra texlive-fonts-recommended \
    texlive-fonts-extra texlive-publishers texlive-science \
    texlive-bibtex-extra latexmk biber dvipng cm-super \
    || echo "  (LaTeX install partial — continue)"

# ----------------------------- 9. Monitoring -------------------------------
echo ">> [9/12] Monitoring tools"
apt-get install -y --no-install-recommends \
    htop nvtop iotop sysstat dstat strace lsof tree jq

# ----------------------------- 10. CUDA paths sanity check -----------------
echo ">> [10/12] CUDA detection"
if [[ -d /usr/local/cuda ]]; then
    echo "    CUDA root: /usr/local/cuda → $(readlink -f /usr/local/cuda)"
elif compgen -G "/usr/local/cuda-*" > /dev/null; then
    LATEST_CUDA=$(ls -d /usr/local/cuda-* | sort -V | tail -1)
    echo "    CUDA root: $LATEST_CUDA"
    ln -sf "$LATEST_CUDA" /usr/local/cuda
fi
if command -v nvcc &>/dev/null; then
    echo "    nvcc: $(nvcc --version | grep release)"
else
    echo "    WARNING: nvcc not on PATH. Will export from /etc/profile.d below."
fi

# ----------------------------- 11. Profile env (CFLAGS, BLAS threads, CUDA, nvcc PATH) -----
echo ">> [11/12] Install /etc/profile.d/vastai-physics.sh"
cat > /etc/profile.d/vastai-physics.sh <<PROFEOF
# Auto-sourced env for physics research workloads on this Vast.ai instance.
# Re-source with: source /etc/profile.d/vastai-physics.sh

# CFLAGS / CXXFLAGS / FFLAGS for native compile of Boltzmann codes etc.
export CFLAGS="${CFLAGS_TUNING}"
export CXXFLAGS="${CFLAGS_TUNING}"
export FFLAGS="-O3 -march=native -ffast-math -fopenmp"

# OpenBLAS / threading: avoid double-threading (OMP × BLAS)
export OMP_NUM_THREADS=4              # reset per-job; 4 is a common sweet spot
export OPENBLAS_NUM_THREADS=1
export MKL_NUM_THREADS=1
export VECLIB_MAXIMUM_THREADS=1
export NUMEXPR_NUM_THREADS=1
export OMP_PLACES=cores
export OMP_PROC_BIND=close
export OMP_DYNAMIC=false
${OPENBLAS_CORETYPE_HINT:+export OPENBLAS_CORETYPE=$OPENBLAS_CORETYPE_HINT}

# CUDA env (always export, even if /usr/local/cuda not yet present)
export CUDA_HOME=/usr/local/cuda
export PATH=\$CUDA_HOME/bin:\$PATH
export LD_LIBRARY_PATH=\$CUDA_HOME/lib64:\${LD_LIBRARY_PATH:-}

# JAX wants this for compute-cap autodetect; also speeds CUDA preamble
export XLA_PYTHON_CLIENT_PREALLOCATE=false
export XLA_FLAGS="--xla_gpu_cuda_data_dir=\$CUDA_HOME"

# Python: avoid bytecode pollution in shared dirs
export PYTHONDONTWRITEBYTECODE=1

# OpenMPI: prefer shared memory + tcp for single-node, ucx for multi
export OMPI_MCA_btl=self,vader,tcp
export OMPI_MCA_pml=ob1
PROFEOF
chmod +x /etc/profile.d/vastai-physics.sh
echo "    wrote /etc/profile.d/vastai-physics.sh (active at next login or 'source' it)"

# ----------------------------- 12. ccache config ---------------------------
echo ">> [12/12] ccache setup (speeds rebuilds 5-10x)"
mkdir -p /root/.ccache
ccache -M 5G
ccache --set-config compiler_check=content
echo '    ccache cache: /root/.ccache  (size 5G)'

# ----------------------------- summary -------------------------------------
cat <<NEXTEOF

==========================================================================
SYSTEM SETUP DONE.

CPU       : $CPU_MODEL
RAM       : ${RAM_GB} GB / cores: $CPU_CORES / AVX2: ${HAS_AVX2:-no} / AVX512: ${HAS_AVX512:-no}
GPU       : $GPU_NAME (sm_${GPU_CC})
CFLAGS    : $CFLAGS_TUNING

Versions:
  gcc      : $(gcc --version | head -1)
  gfortran : $(gfortran --version | head -1)
  mpirun   : $(mpirun --version 2>/dev/null | head -1)
  python3  : $(python3 --version)
  CUDA     : $(nvcc --version 2>/dev/null | grep release || echo 'not in PATH yet — open new shell')

Next steps (run as the working user, not root):

  source /etc/profile.d/vastai-physics.sh
  bash ~/vastai-physics-postinstall.sh   # creates venv + installs full Python stack

==========================================================================
NEXTEOF
