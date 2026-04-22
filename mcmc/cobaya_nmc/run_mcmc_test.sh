#!/usr/bin/env bash
# 5-minute smoke-test MCMC for the ECINMCTheory plugin.
# 2 chains x ~200 steps; goal = verify Cobaya accepts the plugin.
set -euo pipefail

HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO="$(cd "${HERE}/../.." && pwd)"
PY="${REPO}/.venv-compute/bin/python"
COBAYA="${REPO}/.venv-compute/bin/cobaya-run"

cd "${HERE}"
rm -rf chains
mkdir -p chains

# Sanity: plugin imports
"${PY}" test_plugin.py

# Launch 2 chains (mpiexec if available, else 2 sequential processes).
if command -v mpiexec >/dev/null 2>&1; then
    mpiexec -n 2 "${COBAYA}" eci_nmc_plugin.yaml --force 2>&1 | tee chains/run.log
else
    echo "[info] mpiexec not found; running 2 sequential chains."
    "${COBAYA}" eci_nmc_plugin.yaml --force 2>&1 | tee chains/run.log
fi

echo
echo "=== smoke test complete ==="
ls -la chains/
