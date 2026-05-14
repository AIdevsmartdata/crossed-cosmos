#!/bin/bash
# Wait until ALL Phase 1 (4 betas) are done + main orchestrator done, then run Phase 2 v2
echo "[$(date)] Waiting for Phase 1 + Phase 2 v1 cascade to finish..."
while true; do
  done_count=0
  for b in 240 250 260 245; do
    n=$(ls /root/configs/b$b/cfg_b${b}_.lime* 2>/dev/null | wc -l)
    [ "$n" -ge 500 ] && done_count=$((done_count+1))
  done
  hb_running=$(pgrep -f "purgaug -i" | wc -l)
  v1_running=$(pgrep -f "chroma_wflow_parallel.sh\|chroma -i.*results/b.*wflow" | wc -l)
  if [ "$done_count" -eq 4 ] && [ "$hb_running" -eq 0 ] && [ "$v1_running" -eq 0 ]; then
    echo "[$(date)] Cascade complete (4 betas done, no heatbath/wflow v1 running). Launching v2."
    break
  fi
  sleep 60
done
/root/chroma_wflow_v2.sh
