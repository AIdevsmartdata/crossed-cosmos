#!/bin/bash
# ============================================================================
# run_phase4_v3.sh — Phase 4 glueball measurement with v3 variational basis
#
# Runs glueball_correlator_v3 on SU(2) gauge configs across all beta values.
# Outputs XML per config to /root/results_phase4_v3/b{TAG}/glue_{IDX}.out.xml
#
# The v3 binary produces 12 operators (6 shapes × 2 APE levels) per config.
# These are used for OFFLINE GEVP in Python.
#
# IDEMPOTENT: skips configs whose log already contains "ran successfully".
#
# USAGE:
#   1. Build first:  cd /root/crossed-cosmos/chroma && make -f Makefile.glueball_v3
#   2. Symlink binary: cp glueball_correlator_v3 $HOME/install/chroma/bin/
#   3. Run:  bash run_phase4_v3.sh
#
#   Or override params via env:
#     STRIDE=10 JOBS=8  bash run_phase4_v3.sh
# ============================================================================

set -u

# --- Paths ---
INSTALL="${HOME}/install"
WORKDIR="${HOME}/configs"
RESDIR="/root/results_phase4_v3"
BIN="${INSTALL}/chroma/bin/glueball_correlator_v3"

# --- Parameters ---
JOBS="${JOBS:-8}"               # parallel configs (keep modest for I/O)
STRIDE="${STRIDE:-1}"           # process every Nth config (1 = all)
APE_ALPHA="${APE_ALPHA:-0.5}"   # APE smearing parameter
APE_ITERS="10 25"               # two smearing levels for variational basis
LATTICE="16 16 16 16"
T_DIR=3

# --- Check binary ---
if [ ! -x "$BIN" ]; then
  echo "ERROR: $BIN not found or not executable." >&2
  echo "Build: cd /root/crossed-cosmos/chroma && make -f Makefile.glueball_v3" >&2
  echo "Then:  cp glueball_correlator_v3 $INSTALL/chroma/bin/" >&2
  exit 1
fi

mkdir -p "$RESDIR"

# ============================================================================
# run_one_config — measure a single gauge configuration
# ============================================================================
run_one_config() {
  local CFG="$1" TAG="$2" IDX="$3"
  local RES_BDIR="$RESDIR/b${TAG}"
  mkdir -p "$RES_BDIR"

  local XML="${RES_BDIR}/glue_${IDX}.ini.xml"
  local OUT="${RES_BDIR}/glue_${IDX}.out.xml"
  local LOG="${RES_BDIR}/glue_${IDX}.log"

  # Idempotent: skip if already done
  if [ -f "$LOG" ] && grep -q "ran successfully" "$LOG" 2>/dev/null; then
    return 0
  fi

  # Generate input XML
  cat > "$XML" <<XML_EOF
<?xml version="1.0"?>
<glueball>
  <nrow>${LATTICE}</nrow>
  <t_dir>${T_DIR}</t_dir>
  <APE_alpha>${APE_ALPHA}</APE_alpha>
  <APE_iters>${APE_ITERS}</APE_iters>
  <Cfg>
    <cfg_type>SZINQIO</cfg_type>
    <cfg_file>${CFG}</cfg_file>
  </Cfg>
</glueball>
XML_EOF

  # Run on a single MPI rank (no domain decomposition needed for spectroscopy)
  "$BIN" -i "$XML" -o "$OUT" -geom 1 1 1 1 > "$LOG" 2>&1

  # Quick sanity check on output
  if [ -f "$OUT" ] && grep -q "ran successfully" "$LOG" 2>/dev/null; then
    echo "[OK] b${TAG} cfg ${IDX}: $(grep 'raw_plaquette' "$OUT" | head -1)"
  else
    echo "[FAIL] b${TAG} cfg ${IDX} — check $LOG"
  fi
}
export -f run_one_config
export INSTALL RESDIR BIN LATTICE T_DIR APE_ALPHA APE_ITERS

# ============================================================================
# measure_beta — process all configs for a given beta
# ============================================================================
measure_beta() {
  local BETA="$1"
  local TAG="${BETA/./}"       # 2.40 → 240
  local BETA_DIR="$WORKDIR/b${TAG}"

  if [ ! -d "$BETA_DIR" ]; then
    echo "[$(date)] β=$BETA: directory $BETA_DIR not found, skip"
    return
  fi

  local cnt
  cnt=$(ls "$BETA_DIR"/cfg_b${TAG}_*.lime* 2>/dev/null | wc -l)
  if [ "$cnt" -eq 0 ]; then
    echo "[$(date)] β=$BETA: no configs, skip"
    return
  fi

  echo "============================================================"
  echo "[$(date)] β=$BETA: $cnt configs available, stride=$STRIDE"
  echo "         → measuring ~$(( (cnt + STRIDE - 1) / STRIDE )) configs"
  echo "         → 12 operators/config (6 shapes × 2 APE levels)"
  echo "============================================================"

  local TASKFILE="/tmp/phase4_v3_tasks_${TAG}.txt"
  : > "$TASKFILE"

  # Build config file list
  # Support both .lime and .limeN naming conventions
  for cfg_path in "$BETA_DIR"/cfg_b${TAG}_*.lime*; do
    [ -f "$cfg_path" ] || continue
    # Extract index: cfg_b240_.lime42 → 42, cfg_b240_.lime → 0
    local idx
    idx=$(basename "$cfg_path" | sed 's/.*\.lime//')
    [ -z "$idx" ] && idx="0"
    # Stride filter
    if [ "$(( idx % STRIDE ))" -eq 0 ] 2>/dev/null; then
      printf "%s %s %s\n" "$cfg_path" "$TAG" "$idx" >> "$TASKFILE"
    fi
  done

  local task_count
  task_count=$(wc -l < "$TASKFILE")
  echo "[$(date)] β=$BETA: $task_count tasks to run with $JOBS parallel workers"

  if [ "$task_count" -gt 0 ]; then
    xargs -a "$TASKFILE" -n 3 -P "$JOBS" bash -c \
      "run_one_config \"\$0\" \"\$1\" \"\$2\""
  fi

  echo "[$(date)] β=$BETA: phase4 v3 done"
}

# ============================================================================
# MAIN
# ============================================================================
echo "============================================================"
echo "Chroma Phase 4 v3 — 0⁺⁺ glueball variational basis"
echo "Date: $(date)"
echo "Binary: $BIN"
echo "JOBS=$JOBS  STRIDE=$STRIDE  APE α=$APE_ALPHA"
echo "APE iters: $APE_ITERS  (→ 12 operators/config)"
echo "Output: $RESDIR"
echo "============================================================"

for BETA in 2.40 2.45 2.50 2.55 2.60; do
  measure_beta "$BETA"
done

echo ""
echo "============================================================"
echo "[$(date)] PHASE 4 v3 COMPLETE"
echo "Output files: $RESDIR/b*/glue_*.out.xml"
echo ""
echo "Next: run GEVP analysis in Python:"
echo "  python3 /root/crossed-cosmos/analysis/gevp_glueball.py \\"
echo "    --results-dir $RESDIR --beta 240"
echo "============================================================"
