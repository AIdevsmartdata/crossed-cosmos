#!/bin/bash
# deploy_gevp_t2g_vast_v3.sh — STOCK CHROMA GEVP T2g/Eg pipeline turnkey
# v3 (2026-05-16) — Built on G-audit recommendations §9.16 "use Chroma inline measurements"
#
# Strategy:
#   - Build qdpxx (CPU) + chroma from source with --enable-Nc=2 (SU(2)).
#   - Use stock chroma binary with native InlineMeasurements (GLUEBALL_OPS + WILSLP + purgaug).
#   - NO custom C++ binary. NO fake CUDA streams. NO ccache+nvcc.
#   - Python post-process for GEVP T2g/Eg irrep projection (see analyze_gevp_v3.py).
#
# Usage:
#   ./deploy_gevp_t2g_vast_v3.sh <ssh_host> <ssh_port> [vast_label]
#
# Example:
#   ./deploy_gevp_t2g_vast_v3.sh ssh4.vast.ai 39858 g1-su2-v3
#
# Issues fixed vs v2 (G audit /root/crossed-cosmos/notes/G_deploy_v2_audit_2026-05-16.md):
#   C-1: QDP-JIT 404 -> use qdpxx CPU build (stable tag qdp1-46-0 exists)
#   C-2: Chroma 3.44.0 dot -> chroma-3-44-0 hyphens
#   C-3: ccache+nvcc incompat -> ccache+g++ only (CPU build)
#   C-4: --enable-jit-clang -> dropped, no JIT for CPU
#   C-5: /usr/local/cuda assumption -> dropped, CPU build
#   C-6: GPU arch mapping -> not needed
#   C-7: laxiste libqdp.so detection -> check Nc=2 via qdp++-config --Nc
#   D-1: qdp++-config absent -> exists in CPU qdpxx
#   D-2: pipefail missing -> set -eo pipefail everywhere
#   D-3: fallback g++ no .cu -> not relevant (CPU)
#   E-1: custom binary parses only -i -o -> use stock chroma with -i -o (canonical)
#   E-2: XML schema mismatch -> stock chroma <chroma><Param><InlineMeasurements> templates
#   E-3: kill SMI_PID fragile -> trap based monitor (no CUDA needed)
#   E-4: 8^3x16 vs 16^4 smoke -> consistent 8^4 smoke (small + fast)
#   F-1: batch broken by E-1 -> stock chroma loops on configs
#   F-3: RANDOM collision -> per-config XML with unique RNG seed file
#   F-4: 3 streams OOM risk -> drop, use OMP_NUM_THREADS native parallelism
#   F-5: -cuda-stream ghost -> removed
#   F-7: cleanup *.lime too aggressive -> cleanup configs/ only, not output/
#   F-8: awk parses non-existent m_eff.dat -> Python reads QDP DB binary
#   B-1: $(nvidia-smi) local expand -> properly escaped \$()
#
# Track A (CPU, this script) ETA: ~10-15h on RTX 3090 instance (20-core Xeon)
#   - SU(2) 16^4 lattice is small; CPU build is competitive with GPU for Nc=2.
#   - Avoids ALL qdp-jit instability and CUDA toolchain mess.
# Track B (GPU qdp-jit master): not yet supported. See workflow doc §6.

set -eo pipefail

SSH_HOST="${1:?Usage: $0 <ssh_host> <ssh_port> [label]}"
SSH_PORT="${2:?Usage: $0 <ssh_host> <ssh_port> [label]}"
LABEL="${3:-gevp-t2g-v3}"
SSH_KEY="${SSH_KEY:-$HOME/.ssh/vastai_remote}"
SSH_OPTS="-o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null -o ConnectTimeout=30 -o ServerAliveInterval=30"
SSH_CMD="ssh -p $SSH_PORT -i $SSH_KEY $SSH_OPTS root@$SSH_HOST"
SCP_CMD="scp -P $SSH_PORT -i $SSH_KEY $SSH_OPTS"
CHROMA_DIR="/root/crossed-cosmos/chroma"
REMOTE_DIR="/root/gevp_t2g"

echo "=============================================="
echo "  GEVP T2g/Eg STOCK CHROMA v3 turnkey"
echo "  Target  : root@$SSH_HOST:$SSH_PORT"
echo "  Label   : $LABEL"
echo "  Mode    : CPU build qdpxx Nc=2"
echo "  Strategy: stock chroma + GLUEBALL_OPS + WILSLP + purgaug"
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
# Step 2: Disk audit + auto-adjust NCFGS
# -----------------------------------------------------------------------------
echo ""
echo "[2/8] Disk audit + adaptive NCFGS..."
DISK_FREE=$($SSH_CMD "df / | tail -1 | awk '{print \$4}'")
DISK_FREE_GB=$((DISK_FREE / 1024 / 1024))
echo "  Disk free: ${DISK_FREE_GB} GB"

# Each SU(2) 16^4 .lime config ~ 4 MB (4 dirs * 16^4 * 4 complex * 2*2 SU(2) * 16 bytes)
# 3 betas * 500 configs = 1500 * 4 MB = 6 GB raw configs
# GLUEBALL_OPS DB output per config ~ 10 MB -> 15 GB total
# Smearing scratch + WILSLP output ~ 5 GB
# Need at least ~30 GB free for clean run; safety target 60 GB
if [ "$DISK_FREE_GB" -lt 30 ]; then
    echo "  ERROR: <30 GB free, can't run any sensible production"
    exit 1
elif [ "$DISK_FREE_GB" -lt 60 ]; then
    NCFGS_PER_BETA=$((DISK_FREE_GB * 50 / 6))  # roughly proportional
    echo "  WARN: <60 GB. Auto-adjust NCFGS=${NCFGS_PER_BETA}/beta (vs 500 baseline)"
else
    NCFGS_PER_BETA=500
    echo "  Disk OK. NCFGS=500/beta full production."
fi

# -----------------------------------------------------------------------------
# Step 3: Install Chroma + QDP++ from source with Nc=2 (CPU build)
# -----------------------------------------------------------------------------
echo ""
echo "[3/8] Install qdpxx (Nc=2) + chroma from source..."
$SSH_CMD "bash -s" << 'INSTALL_EOF'
set -eo pipefail

# Idempotence: skip if already built with Nc=2
if [ -f /usr/local/bin/chroma ] && /usr/local/bin/qdp++-config --Nc 2>/dev/null | grep -q "^2$"; then
    echo "  qdpxx Nc=2 + chroma already installed, skipping"
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
# 3a. QMP (Message Passing) — REQUIRED by qdpxx configure even for parscalar
# Single-rank SINGLE comms-type (no MPI runtime needed)
# -----------------------------------------------------------------------------
echo "  Installing QMP (SINGLE comms-type)..."
cd /tmp
rm -rf qmp
git clone --depth 1 https://github.com/usqcd-software/qmp.git 2>&1 | tail -2
cd qmp
autoreconf -fi 2>&1 | tail -2
./configure --prefix=/usr/local --with-qmp-comms-type=SINGLE 2>&1 | tail -3
make -j$(nproc) 2>&1 | tail -2
make install 2>&1 | tail -2
ldconfig
echo "  ✓ QMP installed: $(ls /usr/local/lib/libqmp* 2>/dev/null | head -1)"

# -----------------------------------------------------------------------------
# 3b. QDP++ CPU (qdpxx) with Nc=2
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
echo "  Configuring qdpxx Nc=2 Nd=4 parscalar..."
../configure \
    --prefix=/usr/local \
    --enable-Nc=2 \
    --enable-Nd=4 \
    --enable-parallel-arch=parscalar \
    --enable-precision=double \
    --enable-largefile \
    --with-libxml2=/usr \
    CXX="g++" \
    CXXFLAGS="-O3 -std=c++17 -march=native" \
    2>&1 | tail -3

echo "  Building qdpxx (this takes 5-15 min on 16-20 cores)..."
make -j"$(nproc)" 2>&1 | tail -3
make install 2>&1 | tail -3
ldconfig

# Verify
echo "  qdp++-config --Nc = $(qdp++-config --Nc)"
if [ "$(qdp++-config --Nc)" != "2" ]; then
    echo "  ERROR: qdp++ not built with Nc=2"
    exit 1
fi

# -----------------------------------------------------------------------------
# 3c. Chroma (CPU) with qdpxx Nc=2
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

echo "  Building chroma (this takes 10-25 min)..."
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
    "$CHROMA_DIR/glueball_su2_production_v3.xml" \
    "$CHROMA_DIR/purgaug_su2_v3.xml" \
    "$CHROMA_DIR/run_batch_v3.sh" \
    "$CHROMA_DIR/analyze_gevp_v3.py" \
    "root@$SSH_HOST:$REMOTE_DIR/xml/" 2>&1 | tail -3 || {
        echo "  WARN: scp partial fail, retry..."
        sleep 3
        $SCP_CMD \
            "$CHROMA_DIR/glueball_su2_production_v3.xml" \
            "$CHROMA_DIR/purgaug_su2_v3.xml" \
            "$CHROMA_DIR/run_batch_v3.sh" \
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
echo "[6/8] Smoke test 8^4 lattice (purgaug + GLUEBALL_OPS)..."
# Use a remote heredoc for fully self-contained smoke test
$SSH_CMD "bash -s" << SMOKE_EOF
set -eo pipefail
cd "$REMOTE_DIR"
export OMP_NUM_THREADS=\$(nproc)

# Tiny purgaug input: 8^4 lattice, 2 warmup, 2 production, save 1 config
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
        <elem>11</elem>
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
      <beta>2.50</beta>
      <GaugeState>
        <Name>SIMPLE_GAUGE_STATE</Name>
        <GaugeBC><Name>PERIODIC_GAUGEBC</Name></GaugeBC>
      </GaugeState>
    </GaugeAction>
    <HBParams>
      <nOver>3</nOver>
      <NmaxHB>1</NmaxHB>
    </HBParams>
    <nrow>8 8 8 8</nrow>
  </HBItr>
</purgaug>
PURGAUG_SMOKE

mkdir -p configs output logs

echo "  Running purgaug smoke (8^4, 4 updates)..."
SMOKE_START=\$(date +%s)
timeout 180 purgaug \
    -i xml/smoke_purgaug.in.xml \
    -o logs/smoke_purgaug.out.xml \
    -geom 1 1 1 1 2>&1 | tail -10
SMOKE_END=\$(date +%s)
SMOKE_DT=\$((SMOKE_END - SMOKE_START))
echo "  purgaug smoke duration: \${SMOKE_DT}s"

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

echo "  Running chroma measurement smoke..."
MEAS_START=\$(date +%s)
timeout 240 chroma \
    -i xml/smoke_meas.in.xml \
    -o logs/smoke_meas.out.xml \
    -geom 1 1 1 1 2>&1 | tail -15
MEAS_END=\$(date +%s)
MEAS_DT=\$((MEAS_END - MEAS_START))
echo "  chroma meas duration: \${MEAS_DT}s"

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
# Step 7: Push production scripts (already done in step 4, just chmod + summary)
# -----------------------------------------------------------------------------
echo ""
echo "[7/8] Finalize production scripts..."
$SSH_CMD "cd $REMOTE_DIR && \
    cp xml/run_batch_v3.sh . && \
    cp xml/analyze_gevp_v3.py . && \
    chmod +x run_batch_v3.sh && \
    sed -i 's|__NCFGS_PER_BETA__|$NCFGS_PER_BETA|g' run_batch_v3.sh && \
    head -30 run_batch_v3.sh | tail -20"

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
echo "  Deploy v3 STOCK CHROMA terminated"
echo ""
echo "  Build       : qdpxx + chroma from source, Nc=2 Nd=4 CPU"
echo "  Binaries    : /usr/local/bin/{chroma,purgaug}"
echo "  Workdir     : $REMOTE_DIR"
echo "  NCFGS/beta  : $NCFGS_PER_BETA  (auto-adjusted from disk)"
echo "  Betas       : 2.40 2.50 2.60 (16^4 lattice)"
echo "  ETA prod    : ~10-15h CPU build, 16^4 SU(2)"
echo "  ETA gauge   : ~3-5h  per beta (purgaug heatbath)"
echo "  ETA measure : ~4-6h  per beta (GLUEBALL_OPS + WILSLP)"
echo ""
echo "  Next steps:"
echo "    1. ssh -p $SSH_PORT -i $SSH_KEY root@$SSH_HOST"
echo "    2. cd $REMOTE_DIR && nohup bash run_batch_v3.sh > logs/batch.log 2>&1 &"
echo "    3. tail -f logs/batch.log"
echo "    4. After complete: python3 analyze_gevp_v3.py"
echo "=============================================="
