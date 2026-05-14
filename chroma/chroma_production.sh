#!/bin/bash
# Chroma SU(2) production: heatbath at 3 beta values, lattice 16^4
# β = 2.40, 2.50, 2.60 ; 500 configs each ; save every 10 sweeps
# Output: LIME files in /root/configs/b{beta}/

set -e

INSTALL="$HOME/install"
WORKDIR="/root/configs"
NPROC_MPI=16   # geom 2x2x2x2 for 16^4 lattice -> subgrid 8x8x8x8
LATTICE="16 16 16 16"
GEOM="2 2 2 2"
N_WARMUP=500
N_PRODUCTION=5000   # 5000/SaveInterval=10 = 500 configs
SAVE_INTERVAL=10

mkdir -p "$WORKDIR"

run_beta () {
  local BETA="$1"
  local BETA_TAG="$(echo $BETA | sed 's/\.//')"   # 2.40 -> 240
  local BETA_DIR="$WORKDIR/b${BETA_TAG}"
  mkdir -p "$BETA_DIR"
  local XML="$BETA_DIR/purgaug_b${BETA_TAG}.ini.xml"
  local LOG="$BETA_DIR/purgaug.log"
  local OUT="$BETA_DIR/purgaug.out.xml"

  echo "[$(date)] === Generating β=$BETA on 16^4, ${N_PRODUCTION} updates ==="
  cat > "$XML" <<EOF
<?xml version="1.0"?>
<purgaug>
  <Cfg>
    <cfg_type>WEAK_FIELD</cfg_type>
    <cfg_file>dummy</cfg_file>
  </Cfg>
  <MCControl>
    <RNG>
      <Seed>
        <elem>$((RANDOM % 100000))</elem>
        <elem>0</elem>
        <elem>0</elem>
        <elem>0</elem>
      </Seed>
    </RNG>
    <StartUpdateNum>0</StartUpdateNum>
    <NWarmUpUpdates>${N_WARMUP}</NWarmUpUpdates>
    <NProductionUpdates>${N_PRODUCTION}</NProductionUpdates>
    <NUpdatesThisRun>${N_PRODUCTION}</NUpdatesThisRun>
    <SaveInterval>${SAVE_INTERVAL}</SaveInterval>
    <SavePrefix>${BETA_DIR}/cfg_b${BETA_TAG}_</SavePrefix>
    <SaveVolfmt>SINGLEFILE</SaveVolfmt>
  </MCControl>
  <InlineMeasurements>
    <elem>
      <Name>POLYAKOV_LOOP</Name>
      <Frequency>10</Frequency>
      <Param><version>2</version></Param>
      <NamedObject>
        <gauge_id>default_gauge_field</gauge_id>
      </NamedObject>
    </elem>
  </InlineMeasurements>
  <HBItr>
    <GaugeAction>
      <Name>WILSON_GAUGEACT</Name>
      <beta>${BETA}</beta>
      <GaugeState>
        <Name>SIMPLE_GAUGE_STATE</Name>
        <GaugeBC>
          <Name>PERIODIC_GAUGEBC</Name>
        </GaugeBC>
      </GaugeState>
    </GaugeAction>
    <HBParams>
      <nOver>4</nOver>
      <NmaxHB>1</NmaxHB>
    </HBParams>
    <nrow>${LATTICE}</nrow>
  </HBItr>
</purgaug>
EOF
  echo "  XML written to $XML"

  echo "[$(date)] Running purgaug β=$BETA  (mpirun -n ${NPROC_MPI} geom ${GEOM})"
  /usr/bin/time -v mpirun -n ${NPROC_MPI} --allow-run-as-root \
    "$INSTALL/chroma/bin/purgaug" \
    -i "$XML" \
    -o "$OUT" \
    -geom $GEOM \
    > "$LOG" 2>&1

  echo "[$(date)] β=$BETA done. Configs in $BETA_DIR/cfg_b${BETA_TAG}_.lime*"
  ls "$BETA_DIR/cfg_b${BETA_TAG}_.lime"* 2>/dev/null | wc -l
}

echo "============================================================"
echo "Chroma SU(2) heatbath production — $(date)"
echo "Lattice ${LATTICE}, MPI ${NPROC_MPI} procs (geom ${GEOM})"
echo "Each β: ${N_WARMUP} warmup + ${N_PRODUCTION} updates, save every ${SAVE_INTERVAL}"
echo "Output: ${WORKDIR}/b{beta}/"
echo "============================================================"

for BETA in 2.40 2.50 2.60; do
  run_beta "$BETA"
  echo
done

echo "[$(date)] ALL HEATBATH DONE"
echo "Disk usage:"
du -sh "$WORKDIR"
df -h /root | tail -1
