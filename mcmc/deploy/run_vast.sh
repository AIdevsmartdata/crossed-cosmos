#!/usr/bin/env bash
# Launch the ECI NMC MCMC on a Vast.ai CPU spot instance.
# Run inside `tmux` so the chain survives SSH drops. Cobaya checkpoints every
# 30 minutes by default; re-running this script on a resumed instance will
# auto-resume from the last checkpoint.

set -euo pipefail

cd /root/eci
# shellcheck disable=SC1091
source .venv-mcmc/bin/activate

TIMESTAMP=$(date -Iseconds | tr ':' '-')
mkdir -p chains
LOG="chains/run_${TIMESTAMP}.log"

# Thread budget
#   EPYC 9965 = 192 threads. Cobaya R-1 scales ~sqrt(N_chains); 4-8 chains
#   is the convergence sweet spot. We run MPI=8 with OMP=2 per rank (16
#   threads pinned), and let CLASS internal OMP opportunistically use the
#   remaining cores for Boltzmann solves.
export OMP_NUM_THREADS=2
export OMP_PROC_BIND=false
export OMP_PLACES=cores

# mpirun flags
#   --bind-to none      : Vast.ai cgroups reject hard CPU-set binding
#   --map-by slot:PE=2  : 2 processing elements per slot -> matches OMP=2
#   --oversubscribe     : safety against host reporting fewer slots than cores
MPI_NP=${MPI_NP:-8}

echo ">>> Starting ECI MCMC at $(date -Iseconds)"
echo ">>> Logging to $LOG"
echo ">>> MPI ranks: $MPI_NP   OMP per rank: $OMP_NUM_THREADS"

mpirun -np "$MPI_NP" \
    --bind-to none \
    --map-by slot:PE=2 \
    --oversubscribe \
    cobaya-run -r mcmc/params/eci_nmc_optimized.yaml 2>&1 | tee "$LOG"

STATUS=${PIPESTATUS[0]}
echo ">>> cobaya-run exit status: $STATUS"

# Package chains
TAR="chains_${TIMESTAMP}.tar.gz"
tar czf "$TAR" chains/
sha256sum "$TAR" > "${TAR}.sha256"

echo ">>> Chains written: $(pwd)/$TAR"
echo ">>> Checksum:       $(pwd)/${TAR}.sha256"
echo ">>> Retrieve from local workstation with:"
echo "    scp -P <port> root@<IP>:/root/eci/$TAR ./"
echo "    scp -P <port> root@<IP>:/root/eci/${TAR}.sha256 ./"
echo "    sha256sum -c ${TAR}.sha256"

exit "$STATUS"
