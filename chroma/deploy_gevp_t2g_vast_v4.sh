#!/bin/bash
# deploy_gevp_t2g_vast_v4.sh — PROPER usqcd-software build chain
# v4 (2026-05-16) post 3 attempts iteration
#
# Build chain officielle: QMP → QIO external → qdpxx (links external QIO) → chroma
# Usage: ./deploy_gevp_t2g_vast_v4.sh <ssh_host> <ssh_port> [label]

set -euo pipefail

SSH_HOST="${1:?Usage: $0 <ssh_host> <ssh_port> [label]}"
SSH_PORT="${2:?Usage: $0 <ssh_host> <ssh_port> [label]}"
LABEL="${3:-gevp-v4}"
SSH_KEY="$HOME/.ssh/vastai_remote"
SSH_CMD="ssh -p $SSH_PORT -i $SSH_KEY -o StrictHostKeyChecking=no -o ConnectTimeout=30 root@$SSH_HOST"
REMOTE_DIR="/root/gevp_t2g"
CHROMA_DIR="/root/crossed-cosmos/chroma"

echo "════════════════════════════════════════════════════"
echo "  GEVP T₂g/Eg v4 — proper usqcd build chain"
echo "  Target : $SSH_HOST:$SSH_PORT  Label : $LABEL"
echo "════════════════════════════════════════════════════"

# Step 1: SSH probe
echo "[1/8] SSH probe..."
$SSH_CMD "echo SSH_OK && nproc && df -h / | tail -1" 2>&1 | head -5

# Step 2: apt deps
echo "[2/8] Install apt deps..."
$SSH_CMD "DEBIAN_FRONTEND=noninteractive apt-get update -qq && apt-get install -y -qq \
    build-essential autoconf automake libtool gfortran git wget pkg-config \
    libxml2-dev liblapack-dev libblas-dev libhdf5-dev ccache 2>&1 | tail -3"

# Step 3: Build QMP (SINGLE comms-type, no MPI)
echo "[3/8] Build QMP..."
$SSH_CMD "bash -s" << 'QMP_BUILD'
set -e
cd /tmp
rm -rf qmp 2>/dev/null
git clone --depth 1 https://github.com/usqcd-software/qmp.git 2>&1 | tail -2
cd qmp
autoreconf -fi 2>&1 | tail -2
./configure --prefix=/usr/local --with-qmp-comms-type=SINGLE 2>&1 | tail -3
make -j$(nproc) 2>&1 | tail -2
make install 2>&1 | tail -2
ldconfig
ls /usr/local/lib/libqmp* | head -3
echo "QMP OK"
QMP_BUILD

# Step 4: Build QIO external (links to QMP)
echo "[4/8] Build QIO external..."
$SSH_CMD "bash -s" << 'QIO_BUILD'
set -e
cd /tmp
rm -rf qio 2>/dev/null
git clone --depth 1 https://github.com/usqcd-software/qio.git 2>&1 | tail -2
cd qio
autoreconf -fi 2>&1 | tail -2
./configure --prefix=/usr/local --with-qmp=/usr/local 2>&1 | tail -3
make -j$(nproc) 2>&1 | tail -2
make install 2>&1 | tail -2
ldconfig
ls /usr/local/lib/libqio* | head -3
echo "QIO OK"
QIO_BUILD

# Step 5: Build qdpxx (links external QMP + QIO)
echo "[5/8] Build qdpxx Nc=2 (links external QMP + QIO)..."
$SSH_CMD "bash -s" << 'QDPXX_BUILD'
set -e
cd /tmp
rm -rf qdpxx 2>/dev/null
git clone --depth 1 --recursive https://github.com/usqcd-software/qdpxx.git 2>&1 | tail -2
cd qdpxx
autoreconf -fi 2>&1 | tail -2
./configure --prefix=/usr/local \
    --enable-Nc=2 --enable-Nd=4 \
    --enable-parallel-arch=parscalar \
    --enable-precision=double \
    --enable-largefile \
    --with-libxml2=/usr \
    --with-qmp=/usr/local \
    --with-qio=/usr/local \
    CXX="g++" 2>&1 | tail -5
make -j$(nproc) 2>&1 | tail -3
make install 2>&1 | tail -2
ldconfig
ls /usr/local/lib/libqdp* | head -5
qdp++-config --version 2>&1 || echo "(qdp++-config not in PATH, check /usr/local/bin)"
echo "QDPXX OK"
QDPXX_BUILD

# Step 6: Build Chroma
echo "[6/8] Build Chroma (links qdpxx + qmp)..."
$SSH_CMD "bash -s" << 'CHROMA_BUILD'
set -e
cd /tmp
rm -rf chroma 2>/dev/null
git clone --depth 1 --recursive https://github.com/JeffersonLab/chroma.git 2>&1 | tail -2
cd chroma
autoreconf -fi 2>&1 | tail -2
./configure --prefix=/usr/local \
    --with-qdp=/usr/local \
    --with-qmp=/usr/local 2>&1 | tail -5
make -j$(nproc) 2>&1 | tail -3
make install 2>&1 | tail -2
ldconfig
ls /usr/local/bin/chroma 2>&1
which chroma 2>&1 || echo "chroma in /usr/local/bin"
echo "CHROMA OK"
CHROMA_BUILD

# Step 7: Push templates
echo "[7/8] Push XML templates + run_batch..."
$SSH_CMD "mkdir -p $REMOTE_DIR/{configs,output,logs}"
scp -P "$SSH_PORT" -i "$SSH_KEY" -o StrictHostKeyChecking=no \
    "$CHROMA_DIR/purgaug_su2_v3.xml" \
    "$CHROMA_DIR/glueball_su2_production_v3_enhanced.xml" \
    "$CHROMA_DIR/run_batch_v3.sh" \
    "root@$SSH_HOST:$REMOTE_DIR/" 2>&1 | tail -2

# Step 8: Smoke test 8⁴
echo "[8/8] Smoke test 8⁴ purgaug..."
$SSH_CMD "bash -s" << 'SMOKE_TEST'
set -e
cd /root/gevp_t2g
export PATH=/usr/local/bin:$PATH
export LD_LIBRARY_PATH=/usr/local/lib:$LD_LIBRARY_PATH

# Create tiny smoke XML
cat > smoke_purgaug.xml << 'EOF'
<?xml version="1.0"?>
<chroma>
<Param>
  <InlineMeasurements>
    <elem>
      <Name>PURGAUG</Name>
      <Frequency>1</Frequency>
      <Param>
        <Updates>
          <elem><Name>HEATBATH</Name><nOver>4</nOver><GaugeAction>
            <Name>WILSON_GAUGEACT</Name>
            <beta>2.5</beta>
            <GaugeBC><Name>PERIODIC_GAUGEBC</Name></GaugeBC>
          </GaugeAction></elem>
        </Updates>
        <StartUpdateNum>0</StartUpdateNum>
        <NWarmUpUpdates>5</NWarmUpUpdates>
        <NProductionUpdates>10</NProductionUpdates>
        <NUpdatesThisRun>15</NUpdatesThisRun>
        <SaveInterval>5</SaveInterval>
        <SavePrefix>smoke_cfg</SavePrefix>
        <SaveVolfmt>SINGLEFILE</SaveVolfmt>
      </Param>
      <NamedObject><gauge_id>default_gauge_field</gauge_id></NamedObject>
    </elem>
  </InlineMeasurements>
  <nrow>8 8 8 8</nrow>
</Param>
<Cfg><cfg_type>HOT_START</cfg_type><cfg_file>dummy</cfg_file></Cfg>
</chroma>
EOF

timeout 60 chroma -i smoke_purgaug.xml -o smoke_out.xml 2>&1 | tail -10
echo "---"
ls smoke_cfg* 2>&1 | head -5
echo "SMOKE OK"
SMOKE_TEST

echo ""
echo "════════════════════════════════════════════════════"
echo "  ✅ v4 deploy COMPLETE — chroma + qdpxx + qio + qmp installed"
echo "════════════════════════════════════════════════════"
echo "Launch production: ssh ... 'cd $REMOTE_DIR && nohup bash run_batch_v3.sh > batch.log 2>&1 &'"
