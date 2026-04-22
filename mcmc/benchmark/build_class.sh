#!/usr/bin/env bash
# Build hi_class_nmc with Raptor Lake-optimized flags.
# Flags (i5-14600KF): -O3 -march=native -mavx2 -mtune=native -flto
# AVX-512 is fused-off on Raptor Lake consumer dies, so avx2 is the ceiling.
#
# Usage:   bash mcmc/benchmark/build_class.sh
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
CLASS_DIR="$REPO_ROOT/mcmc/nmc_patch/hi_class_nmc"
VENV="$REPO_ROOT/.venv-mcmc-bench"
LOG="$REPO_ROOT/mcmc/benchmark/_raw_timings/class_build.log"

export OPTFLAG="-O3 -march=native -mavx2 -mtune=native -flto -fno-fat-lto-objects"
export OMPFLAG="-fopenmp"
export CC="gcc"

cd "$CLASS_DIR"
rm -rf build libclass.a class python/build python/classy*.so 2>/dev/null || true

echo "[build_class] OPTFLAG=$OPTFLAG"
echo "[build_class] starting make at $(date -Iseconds)"
t0=$(date +%s)
make -j"$(nproc)" OPTFLAG="$OPTFLAG" OMPFLAG="$OMPFLAG" CC="$CC" 2>&1 | tee "$LOG" | tail -30
t1=$(date +%s)
echo "[build_class] CLASS built in $((t1 - t0))s"

# Build classy python binding inside bench venv
echo "[build_class] building classy python extension..."
source "$VENV/bin/activate"
cd python
t2=$(date +%s)
CC=gcc OPT="$OPTFLAG" python setup.py build_ext --inplace 2>&1 | tee -a "$LOG" | tail -15
t3=$(date +%s)
echo "[build_class] classy built in $((t3 - t2))s"

# Install into venv site-packages so `import classy` works anywhere
python setup.py install 2>&1 | tail -5

echo "[build_class] DONE. Total: $((t3 - t0))s"
python -c "import classy; print('classy OK, version=', classy.__version__ if hasattr(classy,'__version__') else 'n/a')"
