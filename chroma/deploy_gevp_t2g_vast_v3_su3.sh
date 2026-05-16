#!/bin/bash
# deploy_gevp_t2g_vast_v3_su3.sh — STOCK CHROMA GEVP T2g/Eg SU(3) pipeline turnkey
# v3 (2026-05-16) — SU(3) Nc=3 variant of deploy_gevp_t2g_vast_v3.sh
#
# Strategy:
#   - Build qdpxx (CPU) + chroma from source with --enable-Nc=3 (SU(3)).
#   - Use stock chroma binary with native InlineMeasurements (GLUEBALL_OPS + WILSLP + purgaug).
#   - NO custom C++ binary. NO fake CUDA streams. NO ccache+nvcc.
#   - Python post-process for GEVP T2g/Eg irrep projection (see analyze_gevp_v3.py).
#
# Usage:
#   ./deploy_gevp_t2g_vast_v3_su3.sh <ssh_host> <ssh_port> [vast_label]
#
# Example:
#   ./deploy_gevp_t2g_vast_v3_su3.sh ssh4.vast.ai 39858 g1-su3-v3
#
# Key changes from SU(2) script (G audit issues remain fixed, see SU(2) v3 header):
#   SU(2)→SU(3) DELTAS:
#     - qdpxx --enable-Nc=3 (vs Nc=2)
#     - Lattice 16^3x32 anisotropic-volume (vs 16^4 isotropic)
#     - β=5.85/5.95/6.05 SU(3) Wilson scaling window (vs 2.40/2.50/2.60 SU(2))
#     - Disk per .lime config ~22 MB SU(3) (vs ~4 MB SU(2)) — 5.5x more storage
#     - APE smearing extended to 0/10/25/50 (vs 0/10/25) — extra DB output
#     - Cooling steps 30 (vs 20) for QTOP
#     - Per-job memory ~2.5x SU(2), so JOBS_MEAS cap = 3 (vs 4)
#     - ETA ~2-3x SU(2) wall-clock per config (more arithmetic per link)
#
# Disk budget:
#   1 config 16^3x32 SU(3) = 4 dirs * 16^3*32 * 4 complex * 9 (3x3 complex SU(3)) * 8 (double)
#                          = 4 * 131072 * 4 * 9 * 8 / 2 (compressed)
#                          ≈ 22 MB raw, ~12-18 MB compressed (SINGLEFILE)
#   3 betas * 500 configs = 1500 * 22 MB = 33 GB raw configs
#   GLUEBALL_OPS DBs per config (4 APE levels * ~3 MB) = 12 MB -> 18 GB total
#   WILSLP + QTOP + scratch ~ 10 GB
#   Need at least 60 GB free; safety target 100 GB.
#
# Track A (CPU) ETA: ~20-30h on RTX 3090 instance with 16-24 cores Xeon
#   - SU(3) plaquette has 3x3 complex matrices (vs 2x2 SU(2)): ~2.25x flops per link
#   - APE smearing 50 iterations: extra ~30% wall-clock vs 25 iter SU(2)
#   - QTOP cooling 30 steps SU(3) vs 20 SU(2): ~50% more cooling time
#
# Track A SU(3) for full 500 cfg/β = NCFGS=500 -> 20-30h overnight
# Track A SU(3) for first scout 200 cfg/β = NCFGS=200 -> 8-12h overnight (recommended)

set -eo pipefail

SSH_HOST="${1:?Usage: $0 <ssh_host> <ssh_port> [label]}"
SSH_PORT="${2:?Usage: $0 <ssh_host> <ssh_port> [label]}"
LABEL="${3:-gevp-t2g-su3-v3}"
SSH_KEY="${SSH_KEY:-$HOME/.ssh/vastai_remote}"
SSH_OPTS="-o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null -o ConnectTimeout=30 -o ServerAliveInterval=30"
SSH_CMD="ssh -p $SSH_PORT -i $SSH_KEY $SSH_OPTS root@$SSH_HOST"
SCP_CMD="scp -P $SSH_PORT -i $SSH_KEY $SSH_OPTS"
CHROMA_DIR="/root/crossed-cosmos/chroma"
REMOTE_DIR="/root/gevp_t2g_su3"

echo "=============================================="
echo "  GEVP T2g/Eg STOCK CHROMA v3 SU(3) turnkey"
echo "  Target  : root@$SSH_HOST:$SSH_PORT"
echo "  Label   : $LABEL"
echo "  Mode    : CPU build qdpxx Nc=3"
echo "  Strategy: stock chroma + GLUEBALL_OPS + WILSLP + QTOP + purgaug"
echo "  Lattice : 16^3 x 32  (anisotropic-volume)"
echo "  Betas   : 5.85, 5.95, 6.05  (SU(3) Wilson)"
echo "=============================================="

# -----------------------------------------------------------------------------
# Step 1: SSH probe + retry
# -----------------------------------------------------------------------------
echo "[1/8] SSH probe + GPU/disk/CPU audit..."
for try in 1 2 3; do
    if $SSH_CMD "echo SSH_OK" >/dev/null 2>&1; then
        echo "  SSH OK (attempt $try)"
        break
    fi
    if [ "$try" -eq 3 ]; then
        echo "  ERROR: SSH failed after 3 attempts" >&2
        exit 1
    fi
    sleep 5
done

$SSH_CMD "bash -c '
echo \"=== HOST ===\";
hostname;
echo \"=== CPU ===\";
nproc; head -1 /proc/cpuinfo | grep -oP \"model name\\s*:\\s*\\K.*\" || echo unknown;
echo \"=== RAM ===\";
free -h | head -2;
echo \"=== DISK ===\";
df -h / | tail -1;
echo \"=== GPU (info only, not used by CPU build) ===\";
nvidia-smi --query-gpu=name,memory.total,driver_version --format=csv,noheader 2>/dev/null | head -2 || echo NO_GPU;
echo \"=== OS ===\";
. /etc/os-release && echo \"\$PRETTY_NAME\";
'"

# -----------------------------------------------------------------------------
# Step 2: Disk audit + auto-adjust NCFGS (SU(3) needs 5.5x storage)
# -----------------------------------------------------------------------------
echo ""
echo "[2/8] Disk audit + adaptive NCFGS..."
DISK_FREE=$($SSH_CMD "df / | tail -1 | awk '{print \$4}'")
DISK_FREE_GB=$((DISK_FREE / 1024 / 1024))
echo "  Disk free: ${DISK_FREE_GB} GB"

# Each SU(3) 16^3x32 .lime config ~ 22 MB
# 3 betas * NCFGS configs * 22 MB raw + ~12 MB DBs each = ~34 MB / config
# 3*500*34 = 51 GB ; safety 100 GB; min 60 GB.
if [ "$DISK_FREE_GB" -lt 60 ]; then
    echo "  ERROR: <60 GB free, can't run any sensible SU(3) production"
    echo "  HINT: rent instance with >=100 GB disk for full NCFGS=500/β SU(3) run"
    exit 1
elif [ "$DISK_FREE_GB" -lt 100 ]; then
    NCFGS_PER_BETA=$((DISK_FREE_GB * 500 / 100))  # proportional, min 200
    [ "$NCFGS_PER_BETA" -lt 200 ] && NCFGS_PER_BETA=200
    echo "  WARN: <100 GB. Auto-adjust NCFGS=${NCFGS_PER_BETA}/beta (vs 500 baseline)"
else
    NCFGS_PER_BETA=500
    echo "  Disk OK. NCFGS=500/beta full production."
fi

# -----------------------------------------------------------------------------
# Step 3: Install Chroma + QDP++ from source with Nc=3 (CPU build)
# -----------------------------------------------------------------------------
echo ""
echo "[3/8] Install qdpxx (Nc=3) + chroma from source..."
$SSH_CMD "bash -s" << 'INSTALL_EOF'
set -eo pipefail

# Idempotence: skip if already built with Nc=3
if [ -f /usr/local/bin/chroma ] && /usr/local/bin/qdp++-config --Nc 2>/dev/null | grep -q "^3$"; then
    echo "  qdpxx Nc=3 + chroma already installed, skipping"
    exit 0
fi

# Install deps
export DEBIAN_FRONTEND=noninteractive
apt-get update -qq 2>&1 | tail -1
apt-get install -y -qq \
    build-essential gfortran \
    libxml2-dev libxml2-utils \
    libopenmpi-dev openmpi-bin \
    liblapack-dev libblas-dev \
    git wget tar ccache python3-numpy python3-scipy \
    autoconf automake libtool m4 \
    2>&1 | tail -3

# ccache for g++ ONLY (NOT for nvcc)
export PATH="/usr/lib/ccache:$PATH"
ccache --set-config max_size=5G 2>/dev/null || true

# -----------------------------------------------------------------------------
# 3a. QDP++ CPU (qdpxx) with Nc=3
# -----------------------------------------------------------------------------
cd /tmp
rm -rf qdpxx*
echo "  Cloning qdpxx (tag qdp1-46-0)..."
wget -q https://github.com/usqcd-software/qdpxx/archive/refs/tags/qdp1-46-0.tar.gz -O qdpxx.tar.gz
tar xzf qdpxx.tar.gz
cd qdpxx-qdp1-46-0

# autoreconf for safety on fresh extract
autoreconf -fi 2>&1 | tail -3 || true

mkdir -p build && cd build
echo "  Configuring qdpxx Nc=3 Nd=4 parscalar..."
../configure \
    --prefix=/usr/local \
    --enable-Nc=3 \
    --enable-Nd=4 \
    --enable-parallel-arch=parscalar \
    --enable-precision=double \
    --enable-largefile \
    --with-libxml2=/usr \
    CXX="g++" \
    CXXFLAGS="-O3 -std=c++17 -march=native" \
    2>&1 | tail -3

echo "  Building qdpxx Nc=3 (this takes 10-25 min on 16-24 cores, SU(3) is heavier than SU(2))..."
make -j"$(nproc)" 2>&1 | tail -3
make install 2>&1 | tail -3
ldconfig

# Verify
echo "  qdp++-config --Nc = $(qdp++-config --Nc)"
if [ "$(qdp++-config --Nc)" != "3" ]; then
    echo "  ERROR: qdp++ not built with Nc=3"
    exit 1
fi

# -----------------------------------------------------------------------------
# 3b. Chroma (CPU) with qdpxx Nc=3
# -----------------------------------------------------------------------------
cd /tmp
rm -rf chroma*
echo "  Cloning chroma (tag chroma-3-44-0)..."
wget -q https://github.com/JeffersonLab/chroma/archive/refs/tags/chroma-3-44-0.tar.gz -O chroma.tar.gz
tar xzf chroma.tar.gz
cd chroma-chroma-3-44-0

autoreconf -fi 2>&1 | tail -3 || true

mkdir -p build && cd build
echo "  Configuring chroma..."
../configure \
    --prefix=/usr/local \
    --with-qdp=/usr/local \
    CXX="g++" \
    CXXFLAGS="-O3 -std=c++17 -march=native" \
    2>&1 | tail -3

echo "  Building chroma SU(3) (this takes 15-35 min)..."
make -j"$(nproc)" 2>&1 | tail -3
make install 2>&1 | tail -3
ldconfig

# Verify chroma + purgaug exist
which chroma purgaug 2>&1
echo "  chroma --help (short): "
chroma --help 2>&1 | head -3 || echo "  (chroma --help may not be supported, normal)"
INSTALL_EOF

# -----------------------------------------------------------------------------
# Step 4: Setup remote workspace + copy templates
# -----------------------------------------------------------------------------
echo ""
echo "[4/8] Setup remote workspace + copy templates..."
$SSH_CMD "mkdir -p $REMOTE_DIR/{configs,output,logs,xml,analysis}"

$SCP_CMD \
    "$CHROMA_DIR/glueball_su3_production_v3.xml" \
    "$CHROMA_DIR/purgaug_su3_v3.xml" \
    "$CHROMA_DIR/run_batch_v3_su3.sh" \
    "$CHROMA_DIR/analyze_gevp_v3.py" \
    "root@$SSH_HOST:$REMOTE_DIR/xml/" 2>&1 | tail -3 || {
        echo "  WARN: scp partial fail, retry..."
        sleep 3
        $SCP_CMD \
            "$CHROMA_DIR/glueball_su3_production_v3.xml" \
            "$CHROMA_DIR/purgaug_su3_v3.xml" \
            "$CHROMA_DIR/run_batch_v3_su3.sh" \
            "$CHROMA_DIR/analyze_gevp_v3.py" \
            "root@$SSH_HOST:$REMOTE_DIR/xml/"
    }

# -----------------------------------------------------------------------------
# Step 5: Sanity check stock binaries
# -----------------------------------------------------------------------------
echo ""
echo "[5/8] Verify stock binaries..."
$SSH_CMD "bash -c '
which chroma purgaug || { echo BIN_MISSING ; exit 1 ; }
echo Chroma Nc:
qdp++-config --Nc
echo Chroma Nd:
qdp++-config --Nd
ldconfig -p | grep -E \"libqdp|libchroma\" | head -4
'"

# -----------------------------------------------------------------------------
# Step 6: Smoke test small lattice (single update + single measurement)
# -----------------------------------------------------------------------------
echo ""
echo "[6/8] Smoke test 8^4 SU(3) lattice (purgaug + GLUEBALL_OPS)..."
$SSH_CMD "bash -s" << SMOKE_EOF
set -eo pipefail
cd "$REMOTE_DIR"
export OMP_NUM_THREADS=\$(nproc)

# Tiny purgaug input: 8^4 lattice, 2 warmup, 2 production, save 1 config
# Use SU(3) β=5.95 (medium scaling)
cat > xml/smoke_purgaug.in.xml << 'PURGAUG_SMOKE'
<?xml version="1.0"?>
<purgaug>
  <Cfg>
    <cfg_type>WEAK_FIELD</cfg_type>
    <cfg_file>dummy</cfg_file>
  </Cfg>
  <MCControl>
    <RNG>
      <Seed>
        <elem>13</elem>
        <elem>0</elem>
        <elem>0</elem>
        <elem>0</elem>
      </Seed>
    </RNG>
    <StartUpdateNum>0</StartUpdateNum>
    <NWarmUpUpdates>2</NWarmUpUpdates>
    <NProductionUpdates>2</NProductionUpdates>
    <NUpdatesThisRun>2</NUpdatesThisRun>
    <SaveInterval>1</SaveInterval>
    <SavePrefix>configs/smoke_cfg</SavePrefix>
    <SaveVolfmt>SINGLEFILE</SaveVolfmt>
  </MCControl>
  <InlineMeasurements>
    <elem>
      <Name>POLYAKOV_LOOP</Name>
      <Frequency>1</Frequency>
      <Param><version>2</version></Param>
      <NamedObject><gauge_id>default_gauge_field</gauge_id></NamedObject>
    </elem>
  </InlineMeasurements>
  <HBItr>
    <GaugeAction>
      <Name>WILSON_GAUGEACT</Name>
      <beta>5.95</beta>
      <GaugeState>
        <Name>SIMPLE_GAUGE_STATE</Name>
        <GaugeBC><Name>PERIODIC_GAUGEBC</Name></GaugeBC>
      </GaugeState>
    </GaugeAction>
    <HBParams>
      <nOver>4</nOver>
      <NmaxHB>1</NmaxHB>
    </HBParams>
    <nrow>8 8 8 8</nrow>
  </HBItr>
</purgaug>
PURGAUG_SMOKE

mkdir -p configs output logs

echo "  Running SU(3) purgaug smoke (8^4, 4 updates, beta=5.95)..."
SMOKE_START=\$(date +%s)
timeout 300 purgaug \
    -i xml/smoke_purgaug.in.xml \
    -o logs/smoke_purgaug.out.xml \
    -geom 1 1 1 1 2>&1 | tail -10
SMOKE_END=\$(date +%s)
SMOKE_DT=\$((SMOKE_END - SMOKE_START))
echo "  purgaug SU(3) smoke duration: \${SMOKE_DT}s"

ls -la configs/ | head -5
ls -la logs/smoke_purgaug.out.xml

# Now run a measurement on the produced config
SMOKE_CFG=\$(ls configs/smoke_cfg.lime* 2>/dev/null | head -1)
if [ -z "\$SMOKE_CFG" ]; then
    echo "  ERROR: purgaug did not produce a config file"
    ls configs/
    exit 1
fi
echo "  Smoke config: \$SMOKE_CFG"

# Build a chroma measurement input
cat > xml/smoke_meas.in.xml << MEAS_SMOKE
<?xml version="1.0"?>
<chroma>
  <Param>
    <InlineMeasurements>
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
        <NamedObject><gauge_id>default_gauge_field</gauge_id></NamedObject>
      </elem>
      <elem>
        <Name>GLUEBALL_OPS</Name>
        <Frequency>1</Frequency>
        <Param>
          <version>1</version>
          <mom2_max>0</mom2_max>
          <displacement_length>1</displacement_length>
          <displacement_list>
            <elem>0</elem>
            <elem>1</elem>
            <elem>2</elem>
          </displacement_list>
          <decay_dir>3</decay_dir>
          <LinkSmearing>
            <LinkSmearingType>APE_SMEAR</LinkSmearingType>
            <link_smear_fact>0.5</link_smear_fact>
            <link_smear_num>10</link_smear_num>
            <no_smear_dir>3</no_smear_dir>
          </LinkSmearing>
        </Param>
        <NamedObject>
          <gauge_id>default_gauge_field</gauge_id>
          <glue_op_file>output/smoke_glue_op.qdpdb</glue_op_file>
        </NamedObject>
      </elem>
    </InlineMeasurements>
    <nrow>8 8 8 8</nrow>
  </Param>
  <Cfg>
    <cfg_type>SZINQIO</cfg_type>
    <cfg_file>\$SMOKE_CFG</cfg_file>
  </Cfg>
</chroma>
MEAS_SMOKE

echo "  Running SU(3) chroma measurement smoke..."
MEAS_START=\$(date +%s)
timeout 360 chroma \
    -i xml/smoke_meas.in.xml \
    -o logs/smoke_meas.out.xml \
    -geom 1 1 1 1 2>&1 | tail -15
MEAS_END=\$(date +%s)
MEAS_DT=\$((MEAS_END - MEAS_START))
echo "  chroma SU(3) meas duration: \${MEAS_DT}s"

# Verify output
ls -la logs/smoke_meas.out.xml output/smoke_glue_op.qdpdb 2>&1 | head -5

# Check 'ran successfully' marker
if grep -q "ran successfully" logs/smoke_meas.out.xml 2>/dev/null; then
    echo "  SMOKE OK: 'ran successfully' marker found"
else
    echo "  SMOKE PARTIAL: 'ran successfully' not in output XML"
    grep -i -E "error|abort|exception" logs/smoke_meas.out.xml | head -5 || true
fi
SMOKE_EOF

# -----------------------------------------------------------------------------
# Step 7: Push production scripts
# -----------------------------------------------------------------------------
echo ""
echo "[7/8] Finalize production scripts..."
$SSH_CMD "cd $REMOTE_DIR && \
    cp xml/run_batch_v3_su3.sh . && \
    cp xml/analyze_gevp_v3.py . && \
    chmod +x run_batch_v3_su3.sh && \
    sed -i 's|__NCFGS_PER_BETA__|$NCFGS_PER_BETA|g' run_batch_v3_su3.sh && \
    head -30 run_batch_v3_su3.sh | tail -20"

# -----------------------------------------------------------------------------
# Step 8: Summary
# -----------------------------------------------------------------------------
echo ""
echo "[8/8] Deploy summary..."
$SSH_CMD "bash -c '
echo === Installed ===;
which chroma purgaug 2>&1;
echo Nc=\$(qdp++-config --Nc) Nd=\$(qdp++-config --Nd);
echo;
echo === Remote dir tree ===;
ls -la $REMOTE_DIR/;
echo;
echo === XML templates ===;
ls -la $REMOTE_DIR/xml/;
echo;
echo === Disk ===;
df -h $REMOTE_DIR | tail -1;
'"

echo ""
echo "=============================================="
echo "  Deploy v3 STOCK CHROMA SU(3) terminated"
echo ""
echo "  Build       : qdpxx + chroma from source, Nc=3 Nd=4 CPU"
echo "  Binaries    : /usr/local/bin/{chroma,purgaug}"
echo "  Workdir     : $REMOTE_DIR"
echo "  NCFGS/beta  : $NCFGS_PER_BETA  (auto-adjusted from disk)"
echo "  Betas       : 5.85 5.95 6.05 (16^3 x 32 lattice)"
echo "  ETA prod    : ~20-30h CPU build, 16^3x32 SU(3) full 500 cfg/β"
echo "  ETA prod    : ~8-12h with NCFGS=200/β (recommended first run)"
echo "  ETA gauge   : ~5-8h  per beta (purgaug heatbath SU(3))"
echo "  ETA measure : ~8-12h per beta (GLUEBALL_OPS APE 0/10/25/50 + WILSLP + QTOP)"
echo ""
echo "  Next steps:"
echo "    1. ssh -p $SSH_PORT -i $SSH_KEY root@$SSH_HOST"
echo "    2. cd $REMOTE_DIR && nohup bash run_batch_v3_su3.sh > logs/batch.log 2>&1 &"
echo "    3. tail -f logs/batch.log"
echo "    4. After complete: python3 analyze_gevp_v3.py (Nc=3 mode)"
echo ""
echo "  Falsifier critère:"
echo "    Test : c_2++(SU(3)) converge vers 0.6385 ± 0.0205 (8-pt P01 RELAUNCH) ?"
echo "    Si oui -> Plan v5 §C Option B robust, channel-dependent F(N) confirmé"
echo "    Si non -> reconsidérer (probable issue technique GEVP/smearing)"
echo "=============================================="
