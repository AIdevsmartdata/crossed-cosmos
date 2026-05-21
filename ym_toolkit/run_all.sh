#!/bin/bash
# YM ML Pipeline — PC gamer orchestrator
cd "$(dirname "${BASH_SOURCE[0]:-$0}")"
mkdir -p logs results

start_job() {
    local name=$1 script=$2 args=$3
    local logf="logs/${name}_$(date +%H%M).log"
    nohup python3 -u $script $args > $logf 2>&1 &
    local pid=$!
    echo "  ✓ $name [PID $pid] → $logf"
    echo "$pid" > logs/${name}.pid
}

echo "=== YM ML Pipeline START $(date) ==="
echo ""
echo "Phase 1 — HMC SU(2) cross-β"
start_job "hmc_b23" "1_hmc_su2.py" "--L 8 --beta 2.3 --n_configs 200 --thermalize 100 --output results/hmc_b23.npz"
start_job "hmc_b25" "1_hmc_su2.py" "--L 8 --beta 2.5 --n_configs 200 --thermalize 100 --output results/hmc_b25.npz"
start_job "hmc_b27" "1_hmc_su2.py" "--L 8 --beta 2.7 --n_configs 200 --thermalize 100 --output results/hmc_b27.npz"
echo ""
echo "Phase 2 — PySR symbolic regression"
start_job "pysr" "../pc_gamer_runs/H_PC_priority_2026-05-21/1_pysr_symbolic_regression.py" ""
echo ""
echo "=== Logs : tail -f logs/*.log ==="
