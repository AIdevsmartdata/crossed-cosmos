#!/bin/bash
set -u
INSTALL="$HOME/install"
WORKDIR="/root/configs"
RESDIR="/root/results"
JOBS=24
STRIDE=5
WFLOW_STEPS=50
WFLOW_TIME=4.0

mkdir -p "$RESDIR"

run_one_config () {
  local CFG="$1" TAG="$2" IDX="$3"
  local RES_BDIR="$RESDIR/b${TAG}"
  mkdir -p "$RES_BDIR"
  local XML="$RES_BDIR/wflow_${IDX}.ini.xml"
  local OUT="$RES_BDIR/wflow_${IDX}.out.xml"
  local LOG="$RES_BDIR/wflow_${IDX}.log"
  if [ -f "$LOG" ] && grep -q "ran successfully" "$LOG" 2>/dev/null; then
    return 0
  fi
  cat > "$XML" <<XML_EOF
<?xml version="1.0"?>
<chroma>
  <Param>
    <InlineMeasurements>
      <elem>
        <Name>PLAQUETTE</Name>
        <Frequency>1</Frequency>
        <Param><version>2</version></Param>
        <NamedObject><gauge_id>default_gauge_field</gauge_id></NamedObject>
      </elem>
      <elem>
        <Name>WILSON_FLOW</Name>
        <Frequency>1</Frequency>
        <Param>
          <version>2</version>
          <nstep>${WFLOW_STEPS}</nstep>
          <wtime>${WFLOW_TIME}</wtime>
          <t_dir>3</t_dir>
          <smear_dirs>1 1 1 1</smear_dirs>
        </Param>
        <NamedObject>
          <gauge_in>default_gauge_field</gauge_in>
          <gauge_out>wflow_gfield_${IDX}</gauge_out>
        </NamedObject>
      </elem>
      <elem>
        <Name>WILSLP</Name>
        <Frequency>1</Frequency>
        <Param>
          <version>3</version>
          <kind>7</kind>
          <j_decay>3</j_decay>
          <t_dir>3</t_dir>
          <GaugeState>
            <Name>SIMPLE_GAUGE_STATE</Name>
            <GaugeBC><Name>PERIODIC_GAUGEBC</Name></GaugeBC>
          </GaugeState>
        </Param>
        <NamedObject>
          <gauge_id>wflow_gfield_${IDX}</gauge_id>
        </NamedObject>
      </elem>
    </InlineMeasurements>
    <nrow>16 16 16 16</nrow>
  </Param>
  <RNG><Seed><elem>11</elem><elem>11</elem><elem>11</elem><elem>0</elem></Seed></RNG>
  <Cfg>
    <cfg_type>SZINQIO</cfg_type>
    <cfg_file>${CFG}</cfg_file>
  </Cfg>
</chroma>
XML_EOF
  "$INSTALL/chroma/bin/chroma" -i "$XML" -o "$OUT" -geom 1 1 1 1 > "$LOG" 2>&1
}
export -f run_one_config
export INSTALL RESDIR WFLOW_STEPS WFLOW_TIME

measure_beta () {
  local BETA="$1"
  local TAG="${BETA/./}"
  local BETA_DIR="$WORKDIR/b${TAG}"
  local cnt
  cnt=$(ls $BETA_DIR/cfg_b${TAG}_.lime* 2>/dev/null | wc -l)
  if [ "$cnt" -eq 0 ]; then
    echo "[$(date)] β=$BETA: no configs yet, skipping"
    return
  fi
  echo "[$(date)] β=$BETA: $cnt configs available, stride=$STRIDE → measuring ~$((cnt/STRIDE))"
  local TASKFILE="/tmp/wflow_tasks_${TAG}.txt"
  : > "$TASKFILE"
  for i in $(seq 1 $STRIDE $cnt); do
    CFG="$BETA_DIR/cfg_b${TAG}_.lime$i"
    [ -f "$CFG" ] || continue
    printf "%s %s %s\n" "$CFG" "$TAG" "$i" >> "$TASKFILE"
  done
  xargs -a "$TASKFILE" -n 3 -P "$JOBS" bash -c 'run_one_config "$0" "$1" "$2"'
  echo "[$(date)] β=$BETA: done"
}

echo "============================================================"
echo "Chroma SU(2) Phase 2 parallel — $(date)"
echo "JOBS=$JOBS STRIDE=$STRIDE NSTEP=$WFLOW_STEPS WTIME=$WFLOW_TIME"
echo "============================================================"
for BETA in "$@"; do
  measure_beta "$BETA"
done
echo "[$(date)] ALL MEASUREMENTS DONE"
