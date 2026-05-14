#!/bin/bash
# ============================================================
# CHROMA_SU2_GLUEBALL.sh — ECI YM Phase 0 Falsifier
# SU(2) Wilson action, β = 2.40, 2.50, 2.60 (Claude-corrected)
# Protocol: M47_D1 consolidated + β scaling
# Target: Vast GPU instance (A40/A100/4090 or CPU 32+ cores)
# ETA: 6-8h per β, total <24h for 3 betas
# Cost: $3-8/β on spot GPU, $0.50-2.00/β on CPU-only
# ============================================================
set -euo pipefail

INSTALL_DIR="$HOME/install/chroma"
WORK_DIR="$HOME/chroma_work"
LOG_DIR="$WORK_DIR/logs"
BETAS="2.40 2.50 2.60"        # Claude-corrected canonical scaling window
LATTICE="16 16 16 16"
N_CONFIGS=500                  # fast test; increase to 1000 for precision
N_THERM=500
TRAJ_STEP=2
MPI_PROCS=$(nproc 2>/dev/null || echo 16)

# ── Stage 0: Software stack ───────────────────────────────
stage_install() {
    echo "[$(date)] Stage 0 — Software stack"
    export DEBIAN_FRONTEND=noninteractive
    apt-get update -qq && apt-get install -y -qq \
        build-essential cmake g++ gfortran \
        libopenmpi-dev openmpi-bin \
        libxml2-dev libtinfo-dev libtinyxml-dev \
        libhdf5-openmpi-dev liblapack-dev libblas-dev \
        git wget python3 python3-pip python3-venv \
        python3-numpy python3-scipy > /dev/null 2>&1

    mkdir -p "$HOME/install"

    # QMP
    if [ ! -f "$HOME/install/qmp/lib/libqmp.so" ]; then
        git clone --depth 1 https://github.com/usqcd-software/qmp.git /tmp/qmp
        mkdir -p /tmp/qmp/build && cd /tmp/qmp/build
        cmake .. -DQMP_MPI=ON -DCMAKE_INSTALL_PREFIX="$HOME/install/qmp"
        make -j$(nproc) install
    fi

    # QDP++
    if [ ! -f "$HOME/install/qdpxx/lib/libqdpxx.so" ]; then
        git clone --depth 1 https://github.com/usqcd-software/qdpxx.git /tmp/qdpxx
        mkdir -p /tmp/qdpxx/build && cd /tmp/qdpxx/build
        cmake .. -DQDP_USE_MPI=ON -DQDP_USE_OPENMP=ON \
            -DCMAKE_PREFIX_PATH="$HOME/install/qmp" \
            -DCMAKE_INSTALL_PREFIX="$HOME/install/qdpxx"
        make -j$(nproc) install
    fi

    # Chroma
    if [ ! -f "$HOME/install/chroma/bin/chroma" ]; then
        git clone --depth 1 https://github.com/JeffersonLab/chroma.git /tmp/chroma
        mkdir -p /tmp/chroma/build && cd /tmp/chroma/build
        cmake .. -DCMAKE_PREFIX_PATH="$HOME/install/qmp;$HOME/install/qdpxx" \
            -DCHROMA_QUDA=OFF -DCMAKE_INSTALL_PREFIX="$HOME/install/chroma" \
            -DBUILD_LAPACK=ON
        make -j$(nproc) install
    fi

    export PATH="$HOME/install/chroma/bin:$PATH"
    export LD_LIBRARY_PATH="$HOME/install/qmp/lib:$HOME/install/qdpxx/lib:$LD_LIBRARY_PATH"
    echo "[$(date)] Stage 0 — DONE"
}

# ── Stage 1: Gauge generation (HMC) ────────────────────────
stage_generate() {
    local BETA=$1
    local DIR="$WORK_DIR/beta_${BETA}"
    mkdir -p "$DIR/configs" "$LOG_DIR"

    local LAST_CONF="$DIR/configs/conf_$(($N_CONFIGS * $TRAJ_STEP + $N_THERM)).lime"
    if [ -f "$LAST_CONF" ]; then
        echo "[$(date)] Stage 1 β=$BETA — configs exist, skip"
        return 0
    fi

    echo "[$(date)] Stage 1 β=$BETA — HMC generation"
    cat > "$DIR/gen.xml" << XEOF
<?xml version="1.0"?>
<chroma>
  <annotation>SU(2) pure gauge ${LATTICE} beta=${BETA}</annotation>
  <Param>
    <nrow>${LATTICE}</nrow>
    <MCControl>
      <start_update_num>0</start_update_num>
      <n_warm_up>${N_THERM}</n_warm_up>
      <n_production>$(($N_CONFIGS * $TRAJ_STEP))</n_production>
      <checkpoint><checkpoint_frequency>${TRAJ_STEP}</checkpoint_frequency></checkpoint>
      <output><cfg_dir>${DIR}/configs</cfg_dir><cfg_prefix>conf</cfg_prefix></output>
    </MCControl>
    <RNG><Seed><elem>42</elem></Seed></RNG>
  </Param>
  <Driver>
    <type>PureGaugeHMC</type>
    <beta>${BETA}</beta>
    <action><WilsonGaugeAction><beta>${BETA}</beta><Nc>2</Nc></WilsonGaugeAction></action>
    <traj_length>1.0</traj_length>
    <n_steps>100</n_steps>
  </Driver>
</chroma>
XEOF
    cd "$DIR"
    mpirun -np 1 "$HOME/install/chroma/bin/chroma" -i gen.xml -o hmc_out.xml > "$LOG_DIR/hmc_beta${BETA}.log" 2>&1
    echo "[$(date)] Stage 1 β=$BETA — DONE (configs: $(ls configs/*.lime 2>/dev/null | wc -l))"
}

# ── Stage 2: Wilson loop → string tension ──────────────────
stage_loops() {
    local BETA=$1
    local DIR="$WORK_DIR/beta_${BETA}"
    local LOOP_DIR="$DIR/loops"
    mkdir -p "$LOOP_DIR"

    echo "[$(date)] Stage 2 β=$BETA — Wilson loops"
    for conf in "$DIR"/configs/conf_*.lime; do
        local base=$(basename "$conf" .lime)
        local out="$LOOP_DIR/${base}.loops.dat"
        [ -f "$out" ] && continue

        cat > /tmp/meas_loops.xml << XEOF
<?xml version="1.0"?>
<chroma>
  <Param><nrow>${LATTICE}</nrow><InlineMeasurements><elem>
    <Name>WILSON_LOOP</Name><Frequency>1</Frequency>
    <Param>
      <smear><ape><kappa>0.5</kappa><n_steps>5</n_steps></ape></smear>
      <r_min>1</r_min><r_max>8</r_max><t_dir>3</t_dir><t_max>7</t_max>
    </Param>
  </elem></InlineMeasurements></Param>
  <Cfg><cfg_type>SCIDAC</cfg_type><cfg_file>${conf}</cfg_file></Cfg>
</chroma>
XEOF
        "$HOME/install/chroma/bin/chroma" -i /tmp/meas_loops.xml -o /tmp/out.xml > /dev/null 2>&1
    done
    echo "[$(date)] Stage 2 β=$BETA — DONE ($(ls "$LOOP_DIR"/*.loops.dat 2>/dev/null | wc -l) files)"
}

# ── Stage 3: Wilson flow + glueball correlators ────────────
stage_flow() {
    local BETA=$1
    local DIR="$WORK_DIR/beta_${BETA}"
    local FLOW_DIR="$DIR/flow"
    mkdir -p "$FLOW_DIR"

    local FLOW_TIMES="0.5 1.0 1.5 2.0 2.5 3.0"

    echo "[$(date)] Stage 3 β=$BETA — Wilson flow + glueball"
    for conf in "$DIR"/configs/conf_*.lime; do
        local base=$(basename "$conf" .lime)
        local out="$FLOW_DIR/${base}_glue.h5"
        [ -f "$out" ] && continue

        cat > /tmp/flow_glue.xml << XEOF
<?xml version="1.0"?>
<chroma>
  <annotation>Wilson flow SU(2) glueball, flow_times=${FLOW_TIMES}</annotation>
  <Param><nrow>${LATTICE}</nrow>
    <WilsonFlow>
      <step_size>0.01</step_size>
      <n_step>300</n_step>
      <measurement_frequency>50</measurement_frequency>
      <LinkSmearing><stout><rho>0.1</rho><n_steps>5</n_steps></stout></LinkSmearing>
      <InlineMeasurements><elem>
        <Name>GLUEBALL_CORRELATOR</Name><Frequency>1</Frequency>
        <Param>
          <loops>
            <elem><type>Plaquette</type><size>1</size></elem>
            <elem><type>Rectangle</type><size>2 1</size></elem>
            <elem><type>Square</type><size>2</size></elem>
          </loops>
          <t_min>0</t_min><t_max>7</t_max>
          <irreps><elem>A1g</elem><elem>Eg</elem><elem>T2g</elem></irreps>
        </Param>
      </elem></InlineMeasurements>
    </WilsonFlow>
  </Param>
  <Cfg><cfg_type>SCIDAC</cfg_type><cfg_file>${conf}</cfg_file></Cfg>
</chroma>
XEOF
        "$HOME/install/chroma/bin/chroma" -i /tmp/flow_glue.xml -o /tmp/flow_out.xml > /dev/null 2>&1
    done
    echo "[$(date)] Stage 3 β=$BETA — DONE ($(ls "$FLOW_DIR"/*_glue.h5 2>/dev/null | wc -l) files)"
}

# ── Stage 4: GEVP analysis + m_0++ / sqrt(σ) ───────────────
stage_analysis() {
    local BETA=$1
    local DIR="$WORK_DIR/beta_${BETA}"
    local OUT="$DIR/result.txt"

    echo "[$(date)] Stage 4 β=$BETA — GEVP analysis"

    python3 << PYEOF > "$OUT" 2>/dev/null
import numpy as np
from scipy.linalg import eigh

# Mock analysis — replace with real HDF5 reads from flow/ + loops/
# This computes the effective mass plateau from correlator data

# Expected values for SU(2) from literature:
# Lucini-TePer JHEP 08(2010)119: m_0++/sqrt(σ) ≈ 3.78(15)
# Athenodorou-TePer arXiv:2106.00364: m_0++/sqrt(σ) ≈ 3.56(11) SU(2)

beta = float("$BETA")
print(f"=== Chroma SU(2) Glueball Analysis β={beta} ===")
print(f"Protocol: M47_D1 consolidated + β scaling")
print(f"Reference: Athenodorou-TePer 2021 (2106.00364)")
print(f"Reference: Lucini-TePer JHEP 08(2010)119")
print(f"")
print(f"Results placeholder — replace with actual HDF5 reads")
print(f"Expected m_0++/sqrt(σ) from lattice ≈ 3.56–3.78")
print(f"ECI v15 Theorem C.6 prediction ≈ 3.78")
print(f"")
print(f"STATUS: PENDING (correlator data collection needed)")
print(f"DELIVERABLES: m_0++/sqrt(σ) ± stat ± syst")
PYEOF
    echo "[$(date)] Stage 4 β=$BETA — DONE → $OUT"
}

# ── Stage 5: Master falsification summary ──────────────────
stage_summary() {
    echo "============================================"
    echo " CHROMA SU(2) GLUEBALL — FALSIFICATION TEST"
    echo "============================================"
    echo ""
    for BETA in $BETAS; do
        local DIR="$WORK_DIR/beta_${BETA}"
        echo "β=$BETA:"
        echo "  configs: $(ls "$DIR"/configs/*.lime 2>/dev/null | wc -l)"
        echo "  loops:   $(ls "$DIR"/loops/*.loops.dat 2>/dev/null | wc -l)"
        echo "  flow:    $(ls "$DIR"/flow/*_glue.h5 2>/dev/null | wc -l)"
        [ -f "$DIR/result.txt" ] && tail -5 "$DIR/result.txt"
        echo ""
    done
    echo "Decision tree:"
    echo "  Δ < 5%  vs LT2010 3.78 → MP1 VALIDATED → Phase 1 Go"
    echo "  Δ 5-10% → MP1 marginal → recalibrate"
    echo "  Δ > 10% → MP1 FALSIFIED → PIVOT"
    echo ""
    echo "[$(date)] Protocol complete."
}

# ── Main ───────────────────────────────────────────────────
export OMP_NUM_THREADS=2
export PATH="$HOME/install/chroma/bin:$PATH"
export LD_LIBRARY_PATH="$HOME/install/qmp/lib:$HOME/install/qdpxx/lib:$LD_LIBRARY_PATH"

mkdir -p "$WORK_DIR" "$LOG_DIR"

echo "=== CHROMA SU(2) GLUEBALL PROTOCOL ==="
echo "Betas: $BETAS"
echo "Lattice: $LATTICE"
echo "MPI procs: $MPI_PROCS"
echo "Started: $(date)"
echo ""

stage_install

for BETA in $BETAS; do
    stage_generate "$BETA"
    stage_loops "$BETA"
    stage_flow "$BETA"
    stage_analysis "$BETA"
done

stage_summary
