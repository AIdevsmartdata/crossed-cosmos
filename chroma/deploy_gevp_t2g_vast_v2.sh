#!/bin/bash
# deploy_gevp_t2g_vast_v2.sh — Déploiement GEVP T₂g/Eg Chroma OPTIMISÉ Vast GPU
# v2 (2026-05-16) : QDP-JIT CUDA + arch flags + parallel β + OMP + disk audit
#
# Usage: ./deploy_gevp_t2g_vast_v2.sh <ssh_host> <ssh_port> [vast_label] [gpu_arch]
# Exemple: ./deploy_gevp_t2g_vast_v2.sh ssh4.vast.ai 39858 g1-su2 sm_86

set -euo pipefail

SSH_HOST="${1:?Usage: $0 <ssh_host> <ssh_port> [label] [gpu_arch]}"
SSH_PORT="${2:?Usage: $0 <ssh_host> <ssh_port> [label] [gpu_arch]}"
LABEL="${3:-gevp-t2g-v2}"
GPU_ARCH="${4:-sm_86}"  # sm_86 RTX 3090 / sm_89 RTX 4090 / sm_70 V100 / sm_80 A100
SSH_KEY="$HOME/.ssh/vastai_remote"
SSH_CMD="ssh -p $SSH_PORT -i $SSH_KEY -o StrictHostKeyChecking=no -o ConnectTimeout=30 root@$SSH_HOST"
CHROMA_DIR="/root/crossed-cosmos/chroma"
REMOTE_DIR="/root/gevp_t2g"

echo "══════════════════════════════════════════════"
echo "  GEVP T₂g/Eg Chroma — Vast v2 OPTIMISED"
echo "  Cible : root@$SSH_HOST:$SSH_PORT"
echo "  Label : $LABEL"
echo "  GPU arch : $GPU_ARCH"
echo "══════════════════════════════════════════════"

# Step 1: Test SSH + GPU + disk audit
echo "[1/7] Test SSH + GPU detect + disk audit..."
$SSH_CMD "bash -c '
echo \"=== GPU ===\";
nvidia-smi --query-gpu=name,memory.total,memory.free,compute_cap --format=csv,noheader;
echo \"=== DISK ===\";
df -h / | tail -1;
echo \"=== CPU ===\";
nproc;
echo \"=== RAM ===\";
free -h | head -2;
echo \"=== CUDA ===\";
nvcc --version | tail -2 || echo NO_NVCC
'"

# Step 2: Verify disk space (need ≥60 GB for compile + 1500 configs)
echo ""
echo "[2/7] Disk audit critique..."
DISK_FREE=$($SSH_CMD "df / | tail -1 | awk '{print \$4}'")
DISK_FREE_GB=$((DISK_FREE / 1024 / 1024))
echo "  Disk free: ${DISK_FREE_GB} GB"
if [ "$DISK_FREE_GB" -lt 60 ]; then
    echo "  ⚠️  ATTENTION : <60 GB. Configs limités automatiquement."
    NCFGS_PER_BETA=$((DISK_FREE_GB * 1024 / 75 / 4))  # 75 MB/config, 4 betas safety
    echo "  Auto-adjust NCFGS=${NCFGS_PER_BETA}/β"
else
    NCFGS_PER_BETA=500
fi

# Step 3: Install Chroma + QDP-JIT GPU build
echo ""
echo "[3/7] Installation Chroma + QDP-JIT GPU optimised..."
$SSH_CMD "GPU_ARCH=$GPU_ARCH bash -s" << 'DEPCHECK'
set -e
if [ -f /usr/local/lib/libqdp.so ] && [ -f /usr/local/lib/libchroma.so ]; then
    echo "✅ Chroma+QDP-JIT déjà présents"
    exit 0
fi

apt-get update -qq 2>&1 | tail -1
apt-get install -y -qq \
    libxml2-dev build-essential gfortran libopenmpi-dev openmpi-bin \
    liblapack-dev libblas-dev git ccache 2>&1 | tail -2

# Compile cache for repeat builds
export PATH="/usr/lib/ccache:$PATH"
ccache --set-config max_size=5G

# QDP-JIT GPU build (CUDA enabled)
cd /tmp
echo "📦 QDP-JIT v1.46.0 GPU build ($GPU_ARCH)..."
wget -q https://github.com/usqcd-software/qdp-jit/archive/refs/tags/v1.46.0.tar.gz -O qdp.tar.gz
tar xzf qdp.tar.gz && cd qdp-jit-1.46.0
mkdir -p build && cd build

# CRITICAL: enable CUDA + arch
../configure --prefix=/usr/local \
    --enable-parallel-arch=parscalar \
    --enable-precision=double \
    --with-libxml2 \
    --enable-cuda \
    --with-cuda=/usr/local/cuda \
    --with-cuda-arch=$GPU_ARCH \
    --enable-jit-clang \
    --enable-large-time \
    CXX="ccache nvcc -ccbin g++" \
    CXXFLAGS="-O3 -DUSE_CUDA -arch=$GPU_ARCH" 2>&1 | tail -5

make -j$(nproc) 2>&1 | tail -3
make install 2>&1 | tail -3

# Chroma 3.44 with GPU QDP-JIT
cd /tmp
echo "📦 Chroma 3.44.0..."
wget -q https://github.com/JeffersonLab/chroma/archive/refs/tags/chroma-3.44.0.tar.gz -O chroma.tar.gz
tar xzf chroma.tar.gz && cd chroma-chroma-3.44.0
mkdir -p build && cd build
../configure --prefix=/usr/local \
    --with-qdp=/usr/local \
    CXXFLAGS="-O3 -march=native -DUSE_CUDA -arch=$GPU_ARCH" 2>&1 | tail -3
make -j$(nproc) 2>&1 | tail -3
make install 2>&1 | tail -3
ldconfig
echo "✅ Chroma + QDP-JIT GPU installed"
DEPCHECK

# Step 4: Setup + copy binary/source
echo ""
echo "[4/7] Setup distant + copy source..."
$SSH_CMD "mkdir -p $REMOTE_DIR/{configs,output,logs}"
scp -P "$SSH_PORT" -i "$SSH_KEY" -o StrictHostKeyChecking=no \
    "$CHROMA_DIR/glueball_correlator_GEVP_T2g.cc" \
    "$CHROMA_DIR/wilson_loop.in.xml" \
    "root@$SSH_HOST:$REMOTE_DIR/" 2>&1 | tail -3

# Step 5: Compile binary with GPU flags
echo ""
echo "[5/7] Compile binary GPU-enabled..."
$SSH_CMD "GPU_ARCH=$GPU_ARCH bash -s" << COMPILE
set -e
cd $REMOTE_DIR
export LD_LIBRARY_PATH=/usr/local/lib:\$LD_LIBRARY_PATH
nvcc -ccbin g++ -O3 -arch=$GPU_ARCH -DUSE_CUDA -std=c++17 \
    -o glueball_GEVP_T2g \
    glueball_correlator_GEVP_T2g.cc \
    \$(chroma-config --cxxflags --libs) \
    \$(qdp++-config --cxxflags --libs) \
    -lcudart -lcublas 2>&1 | tail -5 || \
    g++ -O3 -march=native -std=c++17 \
        -o glueball_GEVP_T2g \
        glueball_correlator_GEVP_T2g.cc \
        \$(chroma-config --cxxflags --libs) \
        \$(qdp++-config --cxxflags --libs) 2>&1 | tail -5
echo "✅ Binary compiled"
ls -la glueball_GEVP_T2g
COMPILE

# Step 6: Smoke test (GPU stress)
echo ""
echo "[6/7] Smoke test GPU 8³×16 + nvidia-smi monitor..."
$SSH_CMD "cd $REMOTE_DIR && \
    export LD_LIBRARY_PATH=/usr/local/lib:\$LD_LIBRARY_PATH && \
    export OMP_NUM_THREADS=8 && \
    nvidia-smi --query-gpu=utilization.gpu,memory.used --format=csv -l 5 > nvidia_smoke.log 2>&1 & SMI_PID=\$! && \
    timeout 120 ./glueball_GEVP_T2g \
        -i wilson_loop.in.xml -lattice 8 8 8 16 -beta 2.50 -ncfgs 10 2>&1 | tail -8; \
    kill \$SMI_PID 2>/dev/null; \
    echo '=== GPU usage during smoke ==='; \
    head -10 nvidia_smoke.log"

# Step 7: Generate optimised batch script
echo ""
echo "[7/7] Génération batch script optimisé..."
$SSH_CMD "cat > $REMOTE_DIR/run_batch_v2.sh" << BATCHSCRIPT
#!/bin/bash
# run_batch_v2.sh — GEVP T₂g 3β optimisé (parallel sub-batches + OMP)
# Usage: nohup bash run_batch_v2.sh > batch.log 2>&1 &

set -e
cd /root/gevp_t2g
export LD_LIBRARY_PATH=/usr/local/lib:\$LD_LIBRARY_PATH
export OMP_NUM_THREADS=\$(nproc)
export CUDA_VISIBLE_DEVICES=0
export QDP_TRACK_MEMORY_USAGE=1

BETAS=(2.40 2.50 2.60)
NCFGS=$NCFGS_PER_BETA
LATTICE="16 16 16 32"
SUB_BATCHES=3  # 3 parallel CUDA streams sub-batches per β

echo "GEVP T₂g batch v2 — \$(date)"
echo "  BETAS: \${BETAS[*]}"
echo "  Configs/β: \$NCFGS"
echo "  Lattice: \$LATTICE"
echo "  OMP threads: \$OMP_NUM_THREADS"
echo "  Sub-batches: \$SUB_BATCHES parallel"
echo "  GPU: $(nvidia-smi --query-gpu=name --format=csv,noheader 2>/dev/null || echo 'unknown')"

for beta in "\${BETAS[@]}"; do
    echo ""
    echo "══════ β=\$beta — \$(date) ══════"
    OUTDIR="output/beta_\${beta}"
    mkdir -p "\$OUTDIR"

    # Sub-batch parallel via CUDA streams (chacun N_configs/SUB_BATCHES)
    SUB_NCFGS=\$((NCFGS / SUB_BATCHES))
    for sub in \$(seq 0 \$((SUB_BATCHES-1))); do
        SUB_OUT="\$OUTDIR/sub_\$sub"
        mkdir -p "\$SUB_OUT"
        ./glueball_GEVP_T2g \
            -i wilson_loop.in.xml \
            -lattice \$LATTICE \
            -beta \$beta \
            -ncfgs \$SUB_NCFGS \
            -seed \$((42 + sub * 1000 + RANDOM)) \
            -output "\$SUB_OUT" \
            -cuda-stream \$sub \
            > "\$SUB_OUT/log.txt" 2>&1 &
    done
    wait  # Wait all sub-batches done for this β

    # Concatenate sub-batches
    cat \$OUTDIR/sub_*/m_eff.dat > \$OUTDIR/m_eff_all.dat 2>/dev/null || true
    echo "✅ β=\$beta done — \$(date) — \$(ls \$OUTDIR/sub_*/log.txt | wc -l) sub-batches"
done

echo ""
echo "══════ BATCH COMPLET — \$(date) ══════"
echo "Extraction m_eff:"
for beta in "\${BETAS[@]}"; do
    M_EFF_2PP=\$(awk '/m_eff_2pp/{sum+=\$2; n++} END{if(n>0)printf "%.4f", sum/n}' output/beta_\${beta}/m_eff_all.dat 2>/dev/null || echo "pending")
    echo "  β=\$beta: m_2pp = \$M_EFF_2PP"
done

# Cleanup configs to save space (keep only summaries)
find output -name "*.lime" -size +100M -delete 2>/dev/null || true
echo "Disk usage final: \$(du -sh output | cut -f1)"
BATCHSCRIPT

$SSH_CMD "chmod +x $REMOTE_DIR/run_batch_v2.sh"

echo ""
echo "══════════════════════════════════════════════"
echo "  ✅ Déploiement v2 OPTIMISÉ terminé"
echo ""
echo "  Optimisations appliquées :"
echo "    • QDP-JIT GPU build avec arch $GPU_ARCH"
echo "    • NVCC -arch=$GPU_ARCH -O3 -DUSE_CUDA"
echo "    • OMP_NUM_THREADS = nproc"
echo "    • 3 sub-batches CUDA streams parallèles par β"
echo "    • ccache compile cache 5GB"
echo "    • Disk audit + auto-adjust NCFGS si <60GB"
echo "    • Cleanup configs >100MB post-run"
echo ""
echo "  ETA estimé : ~4-5h (×3 speedup vs sequential)"
echo "  Lancement  : ssh ... cd $REMOTE_DIR && nohup bash run_batch_v2.sh > batch.log 2>&1 &"
echo "══════════════════════════════════════════════"
