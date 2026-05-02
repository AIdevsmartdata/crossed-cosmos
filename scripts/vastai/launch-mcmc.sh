#!/usr/bin/env bash
# launch-mcmc.sh — launch a Cobaya MCMC inside a Vast.ai Docker container with
# the MPI flags that actually work on this platform.
#
# Critical findings (2026-05-02 debug session, see notes/vastai-debug-2026-05-02.md):
#   1. Vast.ai instances are Docker containers; OpenMPI cannot bind to cores or
#      pin memory due to cgroup limits → must use `--bind-to none`.
#   2. Open MPI's vader (shared-memory) BTL has CMA single-copy disabled in this
#      container kernel → `--mca btl_vader_single_copy_mechanism none`.
#   3. cobaya-run script wrapper does some import gymnastics that prevent its
#      MPI detection from seeing rank>0. Use `python -m cobaya run` directly.
#   4. set +e + nohup + setsid + < /dev/null is the only combination that
#      survives SSH session close. Plain `&` + `disown` does NOT survive.
#
# Usage:
#   bash launch-mcmc.sh <YAML> [<extra cobaya args>]
# Example:
#   bash launch-mcmc.sh mcmc/chains/eci_v50_run1/eci.input.yaml --packages-path mcmc/packages

set -e

if [[ $# -lt 1 ]]; then
    echo "Usage: bash $0 <yaml> [extra args]" >&2
    exit 1
fi
YAML="$1"; shift

# Ensure we have all the env vars
[[ -f /etc/profile.d/vastai-physics.sh ]] && source /etc/profile.d/vastai-physics.sh
[[ -f $HOME/.venv/physics/bin/activate ]] && source "$HOME/.venv/physics/bin/activate"

NPROC=$(nproc)
NCHAINS="${NCHAINS:-4}"
THREADS_PER_CHAIN=$(( NPROC / NCHAINS / 2 ))     # leave half cores idle for headroom
[[ $THREADS_PER_CHAIN -lt 1 ]] && THREADS_PER_CHAIN=1
[[ $THREADS_PER_CHAIN -gt 32 ]] && THREADS_PER_CHAIN=32

export OMP_NUM_THREADS=$THREADS_PER_CHAIN
export OPENBLAS_NUM_THREADS=1
export MKL_NUM_THREADS=1
export OMPI_ALLOW_RUN_AS_ROOT=1
export OMPI_ALLOW_RUN_AS_ROOT_CONFIRM=1
export PYTHONWARNINGS=ignore

# Docker-friendly OpenMPI flags
MPI_FLAGS=(
    --allow-run-as-root
    --bind-to none
    --mca btl_vader_single_copy_mechanism none
    --oversubscribe
    -np "$NCHAINS"
)

echo "=== launch-mcmc.sh — $(date) ==="
echo "  YAML:               $YAML"
echo "  chains × threads:   $NCHAINS × $THREADS_PER_CHAIN  (= $((NCHAINS*THREADS_PER_CHAIN)) of $NPROC cores)"
echo "  extra cobaya args:  $*"
echo ""

mpirun "${MPI_FLAGS[@]}" python3 -W ignore -m cobaya run "$YAML" "$@"

echo ""
echo "=== launch-mcmc.sh DONE — $(date) ==="
