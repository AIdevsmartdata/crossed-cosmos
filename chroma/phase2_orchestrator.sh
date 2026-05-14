#!/bin/bash
# Orchestrator: for each beta, wait until heatbath done, then measure
# The wflow_parallel script is idempotent (skips done configs), so we can
# launch it BEFORE heatbath is done to start measuring early, then re-run
# at the end to catch the remaining.

is_heatbath_running () {
  local b=$1
  pgrep -fa "purgaug -i /root/configs/b${b}/" >/dev/null 2>&1
}

run_phase2_when_safe () {
  local b=$1
  local beta=$2
  echo "[$(date)] β=$beta — initial measurement pass on partial configs"
  /root/chroma_wflow_parallel.sh "$beta"
  # if heatbath still running, wait for completion then re-measure (catches remaining configs)
  while is_heatbath_running "$b"; do
    sleep 30
  done
  echo "[$(date)] β=$beta — heatbath finished, final pass to catch remaining configs"
  /root/chroma_wflow_parallel.sh "$beta"
}

# β=2.50: heatbath currently running, configs already available
run_phase2_when_safe 250 2.50

# β=2.60: queue. Wait until heatbath starts then completes.
# Strategy: poll until configs dir has files, then run wflow
while [ "$(ls /root/configs/b260/cfg_b260_.lime* 2>/dev/null | wc -l)" -lt 50 ]; do
  sleep 30
done
run_phase2_when_safe 260 2.60

# β=2.45 (queued via run_b245.sh, runs after β=2.60)
while [ "$(ls /root/configs/b245/cfg_b245_.lime* 2>/dev/null | wc -l)" -lt 50 ]; do
  sleep 30
done
run_phase2_when_safe 245 2.45

echo "[$(date)] ORCHESTRATOR DONE — all 4 betas measured"
