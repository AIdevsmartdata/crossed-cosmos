#!/bin/bash
# Phase 4 — SU(2) 0++ glueball operator measurement on saved gauge configs.
#
# Runs the custom glueball_correlator binary on every config (or every Nth via
# STRIDE) for all four beta values.  Output XML per config goes to
#   /root/results_phase4/b{TAG}/glue_{IDX}.out.xml
# Each XML contains <O>O(0) ... O(L_t-1)</O>.
#
# Build first:
#   cd /root/crossed-cosmos/chroma && make -f Makefile.glueball
#   then symlink/copy ./glueball_correlator to a path on $PATH, eg.
#   cp glueball_correlator $HOME/install/chroma/bin/

set -u

INSTALL="$HOME/install"
WORKDIR="/root/configs"
RESDIR="/root/results_phase4"
JOBS=24
STRIDE=5
APE_ALPHA=0.5
APE_ITER=20
LATTICE="16 16 16 16"
T_DIR=3
BIN="$INSTALL/chroma/bin/glueball_correlator"

if [ ! -x "$BIN" ]; then
  echo "ERROR: $BIN not found. Build first via Makefile.glueball." >&2
  exit 1
fi

mkdir -p "$RESDIR"

run_one_config () {
  local CFG="$1" TAG="$2" IDX="$3"
  local RES_BDIR="$RESDIR/b${TAG}"
  mkdir -p "$RES_BDIR"
  local XML="$RES_BDIR/glue_${IDX}.ini.xml"
  local OUT="$RES_BDIR/glue_${IDX}.out.xml"
  local LOG="$RES_BDIR/glue_${IDX}.log"
  if [ -f "$LOG" ] && grep -q "ran successfully" "$LOG" 2>/dev/null; then
    return 0
  fi
  cat > "$XML" <<XML_EOF
<?xml version="1.0"?>
<glueball>
  <nrow>${LATTICE}</nrow>
  <t_dir>${T_DIR}</t_dir>
  <APE_alpha>${APE_ALPHA}</APE_alpha>
  <APE_iter>${APE_ITER}</APE_iter>
  <Cfg>
    <cfg_type>SZINQIO</cfg_type>
    <cfg_file>${CFG}</cfg_file>
  </Cfg>
</glueball>
XML_EOF
  "$BIN" -i "$XML" -o "$OUT" -geom 1 1 1 1 > "$LOG" 2>&1
}
export -f run_one_config
export INSTALL RESDIR BIN LATTICE T_DIR APE_ALPHA APE_ITER

measure_beta () {
  local BETA="$1"
  local TAG="${BETA/./}"
  local BETA_DIR="$WORKDIR/b${TAG}"
  local cnt
  cnt=$(ls $BETA_DIR/cfg_b${TAG}_.lime* 2>/dev/null | wc -l)
  if [ "$cnt" -eq 0 ]; then
    echo "[$(date)] β=$BETA: no configs, skip"
    return
  fi
  echo "[$(date)] β=$BETA: $cnt configs available, stride=$STRIDE → measuring ~$((cnt/STRIDE))"
  local TASKFILE="/tmp/phase4_tasks_${TAG}.txt"
  : > "$TASKFILE"
  for i in $(seq 1 $STRIDE $cnt); do
    CFG="$BETA_DIR/cfg_b${TAG}_.lime$i"
    [ -f "$CFG" ] || continue
    printf "%s %s %s\n" "$CFG" "$TAG" "$i" >> "$TASKFILE"
  done
  xargs -a "$TASKFILE" -n 3 -P "$JOBS" bash -c "run_one_config \"\$0\" \"\$1\" \"\$2\""
  echo "[$(date)] β=$BETA: phase4 done"
}

echo "============================================================"
echo "Chroma Phase 4 — 0++ glueball operator — $(date)"
echo "JOBS=$JOBS STRIDE=$STRIDE  APE alpha=$APE_ALPHA iter=$APE_ITER"
echo "OUTPUT: $RESDIR"
echo "============================================================"
for BETA in 2.40 2.45 2.50 2.60; do
  measure_beta "$BETA"
done
echo "[$(date)] PHASE 4 DONE"
