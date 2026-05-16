#!/bin/bash
# deploy_gevp_t2g_vast.sh — Déploiement GEVP T₂g/Eg Chroma sur instance Vast GPU
# Usage: ./deploy_gevp_t2g_vast.sh <ssh_host> <ssh_port> [vast_label]
# Exemple: ./deploy_gevp_t2g_vast.sh ssh5.vast.ai 34342 v100-gevp

set -euo pipefail

SSH_HOST="${1:?Usage: $0 <ssh_host> <ssh_port> [label]}"
SSH_PORT="${2:?Usage: $0 <ssh_host> <ssh_port> [label]}"
LABEL="${3:-gevp-t2g}"
SSH_KEY="$HOME/.ssh/vastai_remote"
SSH_CMD="ssh -p $SSH_PORT -i $SSH_KEY -o StrictHostKeyChecking=no -o ConnectTimeout=30 root@$SSH_HOST"
BINARY_SRC="/tmp/glueball_GEVP_T2g"
CHROMA_DIR="/root/crossed-cosmos/chroma"
REMOTE_DIR="/root/gevp_t2g"

echo "══════════════════════════════════════════════"
echo "  GEVP T₂g/Eg Chroma — Déploiement Vast"
echo "  Cible : root@$SSH_HOST:$SSH_PORT"
echo "  Label : $LABEL"
echo "══════════════════════════════════════════════"

# Step 1: Test SSH
echo ""
echo "[1/6] Test connexion SSH..."
if ! $SSH_CMD "echo SSH_OK" 2>/dev/null; then
    echo "❌ SSH échoué. Vérifier l'instance Vast."
    exit 1
fi
echo "✅ SSH OK"

# Step 2: Check GPU
echo ""
echo "[2/6] Vérification GPU..."
$SSH_CMD "nvidia-smi --query-gpu=name,memory.total,memory.free --format=csv,noheader 2>/dev/null || echo 'NO_GPU'"

# Step 3: Install dependencies (Chroma/QDP++ si absent)
echo ""
echo "[3/6] Installation dépendances..."
$SSH_CMD "bash -s" << 'DEPCHECK'
set -e
HAS_CHROMA=0
if command -v chroma &>/dev/null || ldconfig -p | grep -q libchroma; then
    echo "✅ Chroma déjà présent"
    HAS_CHROMA=1
elif [ -f /usr/local/lib/libchroma.so ]; then
    echo "✅ libchroma trouvée"
    HAS_CHROMA=1
fi

if [ "$HAS_CHROMA" -eq 0 ]; then
    echo "📦 Installation Chroma + QDP++..."
    apt-get update -qq && apt-get install -y -qq \
        libxml2-dev build-essential gfortran libopenmpi-dev openmpi-bin \
        liblapack-dev libblas-dev 2>&1 | tail -3
    
    # QDP++
    cd /tmp
    wget -q https://github.com/usqcd-software/qdp-jit/archive/refs/tags/v1.46.0.tar.gz -O qdp.tar.gz
    tar xzf qdp.tar.gz && cd qdp-jit-1.46.0
    mkdir build && cd build
    ../configure --prefix=/usr/local --enable-parallel-arch=parscalar --enable-precision=double \
        --with-libxml2 --enable-large-time 2>&1 | tail -3
    make -j$(nproc) 2>&1 | tail -3 && make install 2>&1 | tail -3
    
    # Chroma
    cd /tmp
    wget -q https://github.com/JeffersonLab/chroma/archive/refs/tags/chroma-3.44.0.tar.gz -O chroma.tar.gz
    tar xzf chroma.tar.gz && cd chroma-chroma-3.44.0
    mkdir build && cd build
    ../configure --prefix=/usr/local --with-qdp=/usr/local 2>&1 | tail -3
    make -j$(nproc) 2>&1 | tail -3 && make install 2>&1 | tail -3
    ldconfig
    echo "✅ Chroma installé"
fi
DEPCHECK

# Step 4: Setup remote directory + copy binary
echo ""
echo "[4/6] Setup répertoire distant..."
$SSH_CMD "mkdir -p $REMOTE_DIR/configs $REMOTE_DIR/output"
if [ -f "$BINARY_SRC" ]; then
    echo "  Copy glueball_GEVP_T2g ($(du -h $BINARY_SRC | cut -f1))..."
    scp -P $SSH_PORT -i $SSH_KEY -o StrictHostKeyChecking=no \
        "$BINARY_SRC" "root@$SSH_HOST:$REMOTE_DIR/glueball_GEVP_T2g"
else
    echo "⚠️  Binaire source absent ($BINARY_SRC). Compilation sur cible..."
    scp -P $SSH_PORT -i $SSH_KEY -o StrictHostKeyChecking=no \
        "$CHROMA_DIR/glueball_correlator_GEVP_T2g.cc" "root@$SSH_HOST:$REMOTE_DIR/"
    $SSH_CMD "cd $REMOTE_DIR && g++ -O3 -std=c++17 -o glueball_GEVP_T2g \
        glueball_correlator_GEVP_T2g.cc \$(chroma-config --cxxflags --libs) \$(qdp++-config --cxxflags --libs)"
fi

# Copy XML input
scp -P $SSH_PORT -i $SSH_KEY -o StrictHostKeyChecking=no \
    "$CHROMA_DIR/wilson_loop.in.xml" "root@$SSH_HOST:$REMOTE_DIR/input.xml" 2>/dev/null || true

# Step 5: Smoke test
echo ""
echo "[5/6] Smoke test (lattice 8³×16)..."
$SSH_CMD "cd $REMOTE_DIR && timeout 60 ./glueball_GEVP_T2g \
    -i input.xml -lattice 8 8 8 16 -beta 2.50 -ncfgs 10 2>&1 | tail -5" || echo "⚠️ Smoke test partiel"

# Step 6: Generate batch script
echo ""
echo "[6/6] Génération script batch..."
$SSH_CMD "cat > $REMOTE_DIR/run_batch.sh" << 'BATCHSCRIPT'
#!/bin/bash
# run_batch.sh — Lancement GEVP T₂g sur 1500 configs × 3 β
# Usage: nohup bash run_batch.sh > batch.log 2>&1 &

set -e
cd /root/gevp_t2g
export LD_LIBRARY_PATH=/usr/local/lib:$LD_LIBRARY_PATH

BETAS=(2.40 2.50 2.60)
NCFGS=500
LATTICE="16 16 16 32"

echo "GEVP T₂g batch — $(date)"
echo "BETAS: ${BETAS[*]}"
echo "Configs/β: $NCFGS"
echo "Lattice: $LATTICE"

for beta in "${BETAS[@]}"; do
    echo ""
    echo "══════ β=$beta — $(date) ══════"
    OUTDIR="output/beta_${beta}"
    mkdir -p "$OUTDIR"
    ./glueball_GEVP_T2g \
        -i input.xml \
        -lattice $LATTICE \
        -beta $beta \
        -ncfgs $NCFGS \
        -output "$OUTDIR" \
        2>&1 | tee "$OUTDIR/log.txt"
    echo "✅ β=$beta done — $(date)"
done

echo ""
echo "══════ BATCH COMPLET — $(date) ══════"
echo "Extraction m_eff:"
for beta in "${BETAS[@]}"; do
    echo "  β=$beta: $(grep 'm_eff_2pp' output/beta_${beta}/summary.txt 2>/dev/null || echo 'pending')"
done
BATCHSCRIPT

$SSH_CMD "chmod +x $REMOTE_DIR/run_batch.sh"

echo ""
echo "══════════════════════════════════════════════"
echo "  ✅ Déploiement GEVP T₂g terminé"
echo ""
echo "  Répertoire distant : $REMOTE_DIR"
echo "  Lancement batch     : ssh -p $SSH_PORT -i $SSH_KEY root@$SSH_HOST"
echo "                         cd $REMOTE_DIR && nohup bash run_batch.sh > batch.log 2>&1 &"
echo ""
echo "  Monitoring : ssh ... tail -f $REMOTE_DIR/batch.log"
echo "  ETA        : ~4h/β × 3β = ~12h sur V100"
echo "══════════════════════════════════════════════"
