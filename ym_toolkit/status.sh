#!/bin/bash
cd /home/remondiere/crossed-cosmos/ym_toolkit/
echo "=== YM Pipeline Status $(date +%H:%M) ==="
echo ""
echo "── Running processes ──"
ps aux | grep -E "python3.*[1]_hmc_su2|python3.*[1]_pysr|python3.*[2]_hessian" | awk "{print \$2, \$10, \$11, \$12, \$13}" | head -10
echo ""
echo "── GPU ──"
nvidia-smi --query-gpu=memory.used,memory.total,utilization.gpu --format=csv,noheader
echo ""
echo "── Latest logs (3 lines each) ──"
for log in logs/*.log; do
  if [ -f "$log" ]; then
    echo "[$(basename $log)]"
    tail -3 "$log" 2>&1
  fi
done
echo ""
echo "── Results ready ──"
ls -la results/ 2>&1 | tail -10
