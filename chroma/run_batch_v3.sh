#!/bin/bash
# run_batch_v3.sh — STOCK CHROMA GEVP T2g/Eg production runner
# v3 (2026-05-16)
#
# Stage A: SU(2) Wilson heatbath gauge generation (purgaug)
# Stage B: Measurement (chroma with GLUEBALL_OPS + WILSLP)
# Stage C: Cleanup intermediate configs (keep summaries + DB outputs)
#
# Usage: nohup bash run_batch_v3.sh > logs/batch.log 2>&1 &
#
# Parameters (override via env):
#   BETAS         (default "2.40 2.50 2.60")
#   NROW          (default "16 16 16 16")
#   NCFGS         (set by deploy_v3 from disk audit)
#   SAVE_INTERVAL (default 20 — equilibrium decorrelation)
#   NWARMUP       (default 200 sweeps)
#   JOBS_MEAS     (default = nproc / 4, but cap at 4)
#
# Output:
#   configs/cfg_b<B>_<idx>.lime   - gauge configs (~4 MB each)
#   output/b<B>/glue_<idx>.qdpdb  - elemental operator binary DBs
#   output/b<B>/glue_<idx>.out.xml - chroma measurement summary
#   logs/b<B>/{gen,meas}_*.log    - generation + measurement logs

set -eo pipefail

cd "$(dirname "$0")"
WORKDIR="$(pwd)"
TEMPLATE_DIR="$WORKDIR/xml"

# -----------------------------------------------------------------------------
# Parameters
# -----------------------------------------------------------------------------
BETAS="${BETAS:-2.40 2.50 2.60}"
NROW="${NROW:-16 16 16 16}"
NCFGS="${NCFGS:-__NCFGS_PER_BETA__}"   # replaced by deploy_v3 sed at install time
SAVE_INTERVAL="${SAVE_INTERVAL:-20}"
NWARMUP="${NWARMUP:-200}"

# Auto-detect parallel jobs: leave 2 cores idle for system, cap at 4
NPROC=$(nproc)
JOBS_MEAS_DEFAULT=$(( (NPROC - 2) / 4 ))
[ "$JOBS_MEAS_DEFAULT" -lt 1 ] && JOBS_MEAS_DEFAULT=1
[ "$JOBS_MEAS_DEFAULT" -gt 4 ] && JOBS_MEAS_DEFAULT=4
JOBS_MEAS="${JOBS_MEAS:-$JOBS_MEAS_DEFAULT}"

# Per-measurement OMP threads (chroma is OMP-aware)
OMP_PER_JOB=$(( NPROC / (JOBS_MEAS + 1) ))   # +1 leaves capacity for I/O
[ "$OMP_PER_JOB" -lt 1 ] && OMP_PER_JOB=1
export OMP_NUM_THREADS=$OMP_PER_JOB

mkdir -p configs output logs xml

cat << HEADER
=============================================================
GEVP T2g/Eg STOCK CHROMA v3 batch start
Date         : $(date -u)
Host         : $(hostname)
WORKDIR      : $WORKDIR
BETAS        : $BETAS
NROW         : $NROW
NCFGS/beta   : $NCFGS
SAVE_INTERVAL: $SAVE_INTERVAL  (every Nth sweep)
NWARMUP      : $NWARMUP        (thermalization)
NPROC        : $NPROC
JOBS_MEAS    : $JOBS_MEAS      (parallel chroma instances)
OMP_PER_JOB  : $OMP_PER_JOB    (OMP threads per chroma)
=============================================================
HEADER

T_START_TOTAL=$(date +%s)

# -----------------------------------------------------------------------------
# Stage A: Gauge generation per beta (purgaug, serial - heatbath is fast)
# -----------------------------------------------------------------------------
gen_one_beta() {
    local beta="$1"
    local tag="${beta/./}"
    local outdir="configs"
    local logdir="logs/b${tag}"
    mkdir -p "$logdir"

    # NPROD total updates = NWARMUP + NCFGS * SAVE_INTERVAL (configs taken every SAVE_INTERVAL)
    local nprod=$(( NWARMUP + NCFGS * SAVE_INTERVAL ))
    local seed=$(( 42 + $(echo "$beta" | tr -d '.') ))

    local input_xml="xml/gen_b${tag}.in.xml"
    local output_xml="logs/b${tag}/gen.out.xml"

    # Skip if already done (count existing configs)
    # NOTE: purgaug SavePrefix=configs/cfg_b240 -> files configs/cfg_b240.lime0, .lime1, ...
    local existing
    existing=$(ls "$outdir"/cfg_b${tag}.lime* 2>/dev/null | wc -l)
    if [ "$existing" -ge "$NCFGS" ]; then
        echo "  [gen b=$beta] $existing configs already exist (>= $NCFGS), skipping"
        return 0
    fi

    # Generate purgaug input from template
    sed \
        -e "s|__BETA__|$beta|g" \
        -e "s|__NWARMUP__|$NWARMUP|g" \
        -e "s|__NPROD__|$nprod|g" \
        -e "s|__NUPDATES__|$nprod|g" \
        -e "s|__SAVE_INTERVAL__|$SAVE_INTERVAL|g" \
        -e "s|__SAVE_PREFIX__|${outdir}/cfg_b${tag}|g" \
        -e "s|__NROW__|$NROW|g" \
        -e "s|__SEED1__|$seed|g" \
        "$TEMPLATE_DIR/purgaug_su2_v3.xml" > "$input_xml"

    echo "  [gen b=$beta] purgaug start ($NCFGS configs, $nprod total sweeps)..."
    local T0=$(date +%s)

    # Run purgaug (serial single-rank, OMP-parallel internally)
    if ! OMP_NUM_THREADS=$NPROC purgaug \
            -i "$input_xml" \
            -o "$output_xml" \
            -geom 1 1 1 1 \
            > "$logdir/gen.log" 2>&1 ; then
        echo "  [gen b=$beta] FAIL (see $logdir/gen.log)"
        tail -20 "$logdir/gen.log"
        return 1
    fi

    local T1=$(date +%s)
    local DT=$((T1 - T0))
    local nproduced
    nproduced=$(ls "$outdir"/cfg_b${tag}.lime* 2>/dev/null | wc -l)
    echo "  [gen b=$beta] OK ${DT}s, $nproduced configs produced"
}

# -----------------------------------------------------------------------------
# Stage B: Measurement (chroma with GLUEBALL_OPS, parallel over configs)
# -----------------------------------------------------------------------------
meas_one_config() {
    local cfg_path="$1"
    local beta="$2"
    local idx="$3"
    local tag="${beta/./}"
    local logdir="logs/b${tag}"
    local outdir="output/b${tag}"
    mkdir -p "$logdir" "$outdir"

    local input_xml="xml/meas_b${tag}_${idx}.in.xml"
    local output_xml="$outdir/glue_${idx}.out.xml"
    local glue_op_file_base="$outdir/glue_${idx}"
    local log_file="$logdir/meas_${idx}.log"

    # Idempotence
    if [ -f "$output_xml" ] && grep -q "ran successfully" "$output_xml" 2>/dev/null; then
        echo "  [meas b=$beta idx=$idx] already done, skip"
        return 0
    fi

    # Generate measurement input from template
    sed \
        -e "s|__CFG_FILE__|$cfg_path|g" \
        -e "s|__NROW__|$NROW|g" \
        -e "s|__GLUE_OP_FILE__|$glue_op_file_base|g" \
        "$TEMPLATE_DIR/glueball_su2_production_v3_enhanced.xml" > "$input_xml"

    local T0=$(date +%s)
    if OMP_NUM_THREADS=$OMP_PER_JOB chroma \
            -i "$input_xml" \
            -o "$output_xml" \
            -geom 1 1 1 1 \
            > "$log_file" 2>&1 ; then
        local T1=$(date +%s)
        local DT=$((T1 - T0))
        if grep -q "ran successfully" "$output_xml" 2>/dev/null; then
            echo "  [meas b=$beta idx=$idx] OK ${DT}s"
        else
            echo "  [meas b=$beta idx=$idx] PARTIAL ${DT}s (no 'ran successfully' tag)"
            tail -5 "$log_file"
        fi
    else
        echo "  [meas b=$beta idx=$idx] FAIL (see $log_file)"
        tail -10 "$log_file"
    fi
}

export -f meas_one_config
export NROW OMP_PER_JOB TEMPLATE_DIR

meas_one_beta() {
    local beta="$1"
    local tag="${beta/./}"
    local outdir="configs"

    local cfg_list
    cfg_list=$(ls "$outdir"/cfg_b${tag}.lime* 2>/dev/null | head -n "$NCFGS")
    local cnt
    cnt=$(echo "$cfg_list" | wc -l)
    if [ -z "$cfg_list" ] || [ "$cnt" -eq 0 ]; then
        echo "  [meas b=$beta] NO CONFIGS to measure"
        return 1
    fi
    echo "  [meas b=$beta] $cnt configs to measure with $JOBS_MEAS parallel jobs"

    # Build task list: cfg_path beta idx
    local taskfile="/tmp/meas_tasks_${tag}.txt"
    : > "$taskfile"
    local i=0
    for cfg in $cfg_list ; do
        # Extract idx from filename. SavePrefix=configs/cfg_b240 produces cfg_b240.lime0, .lime1, ...
        local idx
        idx=$(basename "$cfg" | sed -E 's/^cfg_b[0-9]+\.lime//')
        [ -z "$idx" ] && idx="$i"
        # Skip if not numeric (e.g. .ini.xml siblings)
        [[ "$idx" =~ ^[0-9]+$ ]] || continue
        printf "%s %s %s\n" "$cfg" "$beta" "$idx" >> "$taskfile"
        i=$((i + 1))
    done

    # Parallel measurement via xargs
    xargs -a "$taskfile" -n 3 -P "$JOBS_MEAS" \
        bash -c 'meas_one_config "$0" "$1" "$2"'
}

# -----------------------------------------------------------------------------
# Main loop
# -----------------------------------------------------------------------------
echo ""
echo "========== Stage A: Gauge generation (PARALLEL across beta) =========="
# Launch all beta generations in parallel background jobs
pids=()
for beta in $BETAS ; do
    (
        echo ""
        echo "-------- beta=$beta --------"
        if ! gen_one_beta "$beta" ; then
            echo "  gen_one_beta failed for beta=$beta, skipping its measurements"
        fi
    ) &
    pids+=($!)
done
# Wait for all parallel gen jobs
for pid in "${pids[@]}"; do wait $pid || true; done
echo "Stage A complete (all beta)."

echo ""
echo "========== Stage B: Measurements =========="
for beta in $BETAS ; do
    echo ""
    echo "-------- beta=$beta --------"
    meas_one_beta "$beta" || echo "  meas_one_beta returned non-zero for beta=$beta"
done

# -----------------------------------------------------------------------------
# Stage C: Summary + light cleanup (configs only, NOT output)
# -----------------------------------------------------------------------------
echo ""
echo "========== Stage C: Summary =========="
T_END_TOTAL=$(date +%s)
DT_TOTAL=$((T_END_TOTAL - T_START_TOTAL))
H_TOTAL=$((DT_TOTAL / 3600))
M_TOTAL=$(( (DT_TOTAL % 3600) / 60 ))
echo "Total wall time: ${H_TOTAL}h${M_TOTAL}m"

echo ""
for beta in $BETAS ; do
    tag="${beta/./}"
    n_cfgs=$(ls configs/cfg_b${tag}.lime* 2>/dev/null | wc -l)
    n_done=$(grep -l "ran successfully" output/b${tag}/glue_*.out.xml 2>/dev/null | wc -l)
    n_dbs_ape10=$(ls output/b${tag}/glue_*.ape10.qdpdb 2>/dev/null | wc -l)
    n_dbs_ape25=$(ls output/b${tag}/glue_*.ape25.qdpdb 2>/dev/null | wc -l)
    echo "  beta=$beta : configs=$n_cfgs measured=$n_done DBs(ape10)=$n_dbs_ape10 DBs(ape25)=$n_dbs_ape25"
done

echo ""
echo "Disk usage:"
du -sh configs output logs 2>/dev/null

# Optional cleanup: tar up + remove configs/ (saves 5-10 GB)
# (Disabled by default - user may want to inspect or re-measure)
# echo "Tarring configs/ (saves space)..."
# tar czf configs_archive.tar.gz configs/ && rm -rf configs/

echo ""
echo "=============================================================="
echo "BATCH v3 COMPLETE — $(date -u)"
echo "Next: python3 analyze_gevp_v3.py"
echo "=============================================================="
