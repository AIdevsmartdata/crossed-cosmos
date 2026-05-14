#!/bin/bash
# Standalone β=2.45 heatbath, waits for the main production to finish first
INSTALL="$HOME/install"
WORKDIR="/root/configs"
BETA=2.45
BETA_TAG=245
NPROC_MPI=16
LATTICE="16 16 16 16"
GEOM="2 2 2 2"
N_WARMUP=500
N_PRODUCTION=5000
SAVE_INTERVAL=10
BETA_DIR="$WORKDIR/b${BETA_TAG}"
XML="$BETA_DIR/purgaug_b${BETA_TAG}.ini.xml"
LOG="$BETA_DIR/purgaug.log"
OUT="$BETA_DIR/purgaug.out.xml"
mkdir -p "$BETA_DIR"

echo "[$(date)] β=2.45 launcher: waiting for main production (purgaug β=2.40/2.50/2.60) to clear..."
# wait until no purgaug processes remain
while pgrep -fa "purgaug -i /root/configs/b2[456]0/" >/dev/null 2>&1; do
  sleep 30
done
echo "[$(date)] main production done. Starting β=2.45."

cat > "$XML" <<XML_EOF
<?xml version="1.0"?>
<purgaug>
  <Cfg><cfg_type>WEAK_FIELD</cfg_type><cfg_file>dummy</cfg_file></Cfg>
  <MCControl>
    <RNG><Seed><elem>2456</elem><elem>0</elem><elem>0</elem><elem>0</elem></Seed></RNG>
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
      <NamedObject><gauge_id>default_gauge_field</gauge_id></NamedObject>
    </elem>
  </InlineMeasurements>
  <HBItr>
    <GaugeAction>
      <Name>WILSON_GAUGEACT</Name>
      <beta>${BETA}</beta>
      <GaugeState>
        <Name>SIMPLE_GAUGE_STATE</Name>
        <GaugeBC><Name>PERIODIC_GAUGEBC</Name></GaugeBC>
      </GaugeState>
    </GaugeAction>
    <HBParams><nOver>4</nOver><NmaxHB>1</NmaxHB></HBParams>
    <nrow>${LATTICE}</nrow>
  </HBItr>
</purgaug>
XML_EOF

mpirun -n ${NPROC_MPI} --allow-run-as-root "$INSTALL/chroma/bin/purgaug" \
    -i "$XML" -o "$OUT" -geom $GEOM > "$LOG" 2>&1

echo "[$(date)] β=2.45 heatbath done. Configs:"
ls "$BETA_DIR/cfg_b${BETA_TAG}_.lime"* 2>/dev/null | wc -l

# Then launch Phase 2 for β=2.45 (will use any spare cores)
echo "[$(date)] β=2.45 measurements (Phase 2):"
/root/chroma_wflow_parallel.sh 2.45
echo "[$(date)] β=2.45 FULL DONE"
