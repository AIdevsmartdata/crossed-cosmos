#!/usr/bin/env bash
# ---------------------------------------------------------------------------
# ECI v4 MCMC launcher
# Expected runtime on i5-14600KF (4 MPI ranks × 5 OMP threads): ~3 days
# for 4 chains to reach Gelman-Rubin R-1 < 0.05 on the full parameter set.
# ---------------------------------------------------------------------------
set -euo pipefail

HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$HERE"

export OMP_NUM_THREADS="${OMP_NUM_THREADS:-5}"
NCHAINS="${NCHAINS:-4}"

mkdir -p chains

# -r  resume if chains already exist
if command -v mpirun >/dev/null 2>&1; then
    exec mpirun -np "$NCHAINS" cobaya-run -r params/eci_nmc.yaml
else
    echo "WARN: mpirun not found — running a single chain. Install openmpi-bin." >&2
    exec cobaya-run -r params/eci_nmc.yaml
fi
