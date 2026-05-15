#!/bin/bash
# ============================================================================
# measure_all.sh — Phase E3 measurement campaign (FIXED)
#
# Fixes the signature mismatch bug in run_e3_full.sh: builds proper input
# XML per config and calls `glueball_correlator_v3 -i in.xml -o out.xml`
# with the structured <glueball> block the binary expects.
#
# IDEMPOTENT: skips configs already measured successfully (log contains
# "ran successfully"). Safe to re-run.
#
# Can be launched AFTER purgaug HMC phase ends, or IN PARALLEL with HMC
# (the loop simply skips betas whose config dir is empty).
#
# USAGE:
#   bash /root/measure_all.sh                # serial mode (JOBS=4)
#   JOBS=8 bash /root/measure_all.sh         # 8 parallel measurements
#   BETAS="2.50" bash /root/measure_all.sh   # one beta only
#   BETAS="2.50 2.60" JOBS=8 bash /root/measure_all.sh
# ============================================================================

exec > /root/measure_all.log 2>&1
set -u

GLUEBALL="${GLUEBALL:-/root/glueball_correlator_v3}"
CONFIGS="${CONFIGS:-/root/configs}"
RESULTS="${RESULTS:-/root/results_phase4_v3}"
JOBS="${JOBS:-4}"
BETAS="${BETAS:-2.50 2.60}"
LATTICE="${LATTICE:-16 16 16 16}"
T_DIR="${T_DIR:-3}"
APE_ALPHA="${APE_ALPHA:-0.5}"
APE_ITERS="${APE_ITERS:-10 25}"

# Sanity check binary
if [ ! -x "$GLUEBALL" ]; then
    echo "ERROR: binary not executable: $GLUEBALL"
    exit 1
fi

"$GLUEBALL" 2>&1 | head -1 | grep -q "Usage: glueball_correlator_v3" || {
    echo "ERROR: $GLUEBALL does not have expected signature"
    exit 1
}

# ============================================================================
# measure_one_config — measure a single config (xargs-callable)
# Arguments: CFG_PATH TAG IDX
# ============================================================================
measure_one_config() {
    local CFG="$1" TAG="$2" IDX="$3"
    local RES_DIR="$RESULTS/$TAG"
    local IN="/tmp/glueball_input_${TAG}_${IDX}.xml"
    local OUT="$RES_DIR/glue_${IDX}.out.xml"
    local LOG="$RES_DIR/glue_${IDX}.log"

    if [ -f "$LOG" ] && grep -q "ran successfully" "$LOG" 2>/dev/null; then
        return 0
    fi

    cat > "$IN" << XEOF
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
XEOF

    "$GLUEBALL" -i "$IN" -o "$OUT" > "$LOG" 2>&1

    if grep -q "ran successfully" "$LOG" 2>/dev/null; then
        echo "[OK] $TAG cfg $IDX  $(grep raw_plaquette "$OUT" 2>/dev/null | head -1)"
    else
        echo "[FAIL] $TAG cfg $IDX -- see $LOG"
    fi
}
export -f measure_one_config
export GLUEBALL CONFIGS RESULTS LATTICE T_DIR APE_ALPHA APE_ITERS

# ============================================================================
# measure_beta — process all configs for one beta value
# ============================================================================
measure_beta() {
    local BETA="$1"
    local TAG="b$(echo $BETA | sed 's/\.//')"
    local CFG_DIR="$CONFIGS/$TAG"
    local RES_DIR="$RESULTS/$TAG"

    mkdir -p "$RES_DIR"

    if [ ! -d "$CFG_DIR" ]; then
        echo "[$(date)] $TAG: directory $CFG_DIR not found, skip"
        return
    fi

    local TASKFILE="/tmp/measure_${TAG}_tasks.txt"
    : > "$TASKFILE"

    # purgaug SaveVolfmt=SINGLEFILE writes one file per config.
    # Filename pattern: $SavePrefix${index} -- here SavePrefix=$CFG_DIR/glue_.
    # Extensions vary by Chroma version (.lime, .lime.0, none).
    for cfg in "$CFG_DIR"/glue_*; do
        [ -f "$cfg" ] || continue
        # Skip Chroma XML sidecars and metadata
        case "$cfg" in
            *.xml|*.xml[0-9]*|*.ini.xml*|*.log|*.info|*.dat) continue ;;
        esac
        local fname
        fname=$(basename "$cfg")
        # Extract index: glue_42.lime -> 42, glue_42 -> 42, glue_.lime42 -> 42
        local idx
        idx=$(echo "$fname" | sed -E 's/^glue_//' | sed -E 's/^\.lime//' | sed -E 's/\.lime[0-9]*$//' | sed -E 's/\.[^.]+$//')
        [ -z "$idx" ] && idx="0"
        # Skip if idx contains non-numeric (defensive against odd extensions)
        case "$idx" in
            ''|*[!0-9]*) continue ;;
        esac
        printf "%s %s %s\n" "$cfg" "$TAG" "$idx" >> "$TASKFILE"
    done

    local n
    n=$(wc -l < "$TASKFILE")
    echo "============================================================"
    echo "[$(date)] $TAG: $n configs to measure with $JOBS parallel workers"
    echo "============================================================"

    if [ "$n" -gt 0 ]; then
        xargs -a "$TASKFILE" -n 3 -P "$JOBS" bash -c \
            'measure_one_config "$0" "$1" "$2"'
    fi

    echo "[$(date)] $TAG: measurement phase done ($n configs)"
}

# ============================================================================
# MAIN
# ============================================================================
echo "============================================================"
echo "Phase E3 measurement campaign (FIXED)"
echo "Date: $(date)"
echo "Binary: $GLUEBALL"
echo "Configs dir: $CONFIGS"
echo "Results dir: $RESULTS"
echo "Betas: $BETAS  JOBS=$JOBS"
echo "Lattice: $LATTICE  t_dir=$T_DIR"
echo "APE: alpha=$APE_ALPHA iters=$APE_ITERS"
echo "============================================================"

for BETA in $BETAS; do
    measure_beta "$BETA"
done

echo ""
echo "============================================================"
echo "[$(date)] CAMPAIGN COMPLETE"
echo "Results: $RESULTS/b*/glue_*.out.xml"
echo ""
echo "Next: run GEVP analysis offline"
echo "  python3 /root/crossed-cosmos/analysis/gevp_glueball_e3.py \\"
echo "    --results-dir $RESULTS --betas 250 260"
echo "============================================================"

touch /root/measure_all_done
