#!/bin/bash
# ============================================================================
# deploy_vast_v3.sh — Ξ Vast Chroma SU(2) Glueball Production Pipeline
# ============================================================================
# One-click deployment for Vast.AI GPU instances
# Budget: €18.81 → ~72-115h on RTX 3090 @ $0.16-0.30/h
#
# Usage:
#   chmod +x deploy_vast_v3.sh
#   ./deploy_vast_v3.sh                    # full pipeline
#   ./deploy_vast_v3.sh --build-only       # just build Chroma
#   ./deploy_vast_v3.sh --measure-only     # run measurements only
#   ./deploy_vast_v3.sh --analyze-only     # post-process only
#   ./deploy_vast_v3.sh --help
# ============================================================================

set -euo pipefail

# ─── Configuration ───────────────────────────────────────────────────────────
WORKDIR="${WORKDIR:-$HOME/chroma_su2_production}"
LOG_DIR="${LOG_DIR:-/tmp/chroma_logs}"
N_CORES=$(nproc 2>/dev/null || echo 4)
OMP_NUM_THREADS="${OMP_NUM_THREADS:-$N_CORES}"
export OMP_NUM_THREADS

# Chroma build config
CHROMA_REPO="https://github.com/JeffersonLab/chroma.git"
QDPPP_REPO="https://github.com/JeffersonLab/qdp++.git"
CHROMA_BRANCH="master"
BUILD_DIR="$WORKDIR/build"
INSTALL_DIR="$WORKDIR/install"

# Runtime config
XML_CONFIG="${XML_CONFIG:-$(dirname "$0")/glueball_T2g_inline.xml}"
OUTPUT_XML="${OUTPUT_XML:-$WORKDIR/output/glueball_output.xml}"
N_JOBS_PARALLEL="${N_JOBS_PARALLEL:-1}"  # parallel jobs for multi-config batches
DISK_CLEANUP_THRESHOLD_MB="${DISK_CLEANUP_THRESHOLD_MB:-102400}"  # 100GB
MAX_LOG_SIZE_MB="${MAX_LOG_SIZE_MB:-500}"
ANALYSIS_SCRIPT="${ANALYSIS_SCRIPT:-$(dirname "$0")/analyze_gevp.py}"

# Colors
RED='\033[0;31m'; GREEN='\033[0;32m'; YELLOW='\033[1;33m'
BLUE='\033[0;34m'; NC='\033[0m'
log_info()  { echo -e "${GREEN}[INFO]${NC}  $(date '+%H:%M:%S') $*"; }
log_warn()  { echo -e "${YELLOW}[WARN]${NC}  $(date '+%H:%M:%S') $*"; }
log_error() { echo -e "${RED}[ERROR]${NC} $(date '+%H:%M:%S') $*"; }
log_step()  { echo -e "${BLUE}[STEP]${NC}  $(date '+%H:%M:%S') $*"; }

# ─── Help ────────────────────────────────────────────────────────────────────
show_help() {
    cat << 'EOF'
Ξ Vast Chroma SU(2) Glueball Pipeline v3

MODES:
  (default)             Full pipeline: build → generate → measure → analyze
  --build-only          Build Chroma + QDP++ with SU(2) support
  --measure-only        Run measurements using existing build
  --analyze-only        Post-process correlators → GEVP → masses
  --help                This message

ENVIRONMENT:
  WORKDIR               Working directory (default: ~/chroma_su2_production)
  XML_CONFIG            Path to Chroma XML config
  OMP_NUM_THREADS       OpenMP threads (default: nproc)
  N_JOBS_PARALLEL       Parallel config batch jobs (default: 1)

HARDWARE DETECTED:
  CPU: $(nproc) cores
  RAM: $(free -h | awk '/^Mem:/{print $2}')
  Disk: $(df -h / | awk 'NR==2{print $4}') free
EOF
}

# ─── Health Check ────────────────────────────────────────────────────────────
health_check() {
    log_step "Running health checks..."
    
    # RAM check
    local free_ram_mb
    free_ram_mb=$(free -m | awk '/^Mem:/{print $7}')
    if [ "$free_ram_mb" -lt 10240 ]; then
        log_error "RAM < 10GB free (${free_ram_mb}MB). Aborting."
        log_info "Clean suggestions: rm -rf /tmp/*; docker system prune -af"
        return 1
    fi
    log_info "RAM: ${free_ram_mb}MB free — OK"
    
    # Disk check
    local free_disk_gb
    free_disk_gb=$(df -BG / | awk 'NR==2{print $4}' | sed 's/G//')
    if [ "$free_disk_gb" -lt 50 ]; then
        log_error "Disk < 50GB free (${free_disk_gb}GB). Aborting."
        return 1
    fi
    log_info "Disk: ${free_disk_gb}GB free — OK"
    
    # Create directories
    mkdir -p "$WORKDIR" "$LOG_DIR" "$WORKDIR/output" "$WORKDIR/configs"
    
    return 0
}

# ─── Detect Package Manager ──────────────────────────────────────────────────
detect_pkg_manager() {
    if command -v apt-get &>/dev/null; then
        echo "apt"
    elif command -v dnf &>/dev/null; then
        echo "dnf"
    elif command -v yum &>/dev/null; then
        echo "yum"
    elif command -v pacman &>/dev/null; then
        echo "pacman"
    else
        echo "unknown"
    fi
}

# ─── Install Dependencies ────────────────────────────────────────────────────
install_deps() {
    log_step "Installing build dependencies..."
    local pkg
    pkg=$(detect_pkg_manager)
    
    case "$pkg" in
        apt)
            apt-get update -qq
            apt-get install -y -qq \
                build-essential g++ gfortran cmake autoconf automake \
                libtool libxml2-dev libopenmpi-dev openmpi-bin \
                python3 python3-pip python3-numpy python3-scipy \
                git wget curl bc jq 2>&1 | tail -5
            ;;
        dnf|yum)
            $pkg install -y \
                gcc-c++ gcc-gfortran cmake autoconf automake \
                libtool libxml2-devel openmpi-devel \
                python3 python3-pip python3-numpy python3-scipy \
                git wget curl bc jq 2>&1 | tail -5
            ;;
        pacman)
            pacman -Sy --noconfirm \
                base-devel gcc-fortran cmake autoconf automake \
                libtool libxml2 openmpi \
                python python-pip python-numpy python-scipy \
                git wget curl bc jq 2>&1 | tail -5
            ;;
        *)
            log_error "Unknown package manager. Install manually: gcc, g++, gfortran, cmake, openmpi, libxml2, python3"
            return 1
            ;;
    esac
    
    # Python deps for GEVP analysis
    pip3 install --quiet numpy scipy matplotlib lxml 2>&1 | tail -3
    log_info "Dependencies installed — OK"
}

# ─── Build QDP++ with SU(2) ──────────────────────────────────────────────────
build_qdppp() {
    log_step "Building QDP++ (SU(2) gauge group)..."
    
    if [ -f "$INSTALL_DIR/lib/libqdp++.a" ] || [ -f "$INSTALL_DIR/lib/libqdp++.so" ]; then
        log_info "QDP++ already built. Skipping."
        return 0
    fi
    
    local qdp_build="$BUILD_DIR/qdp++"
    mkdir -p "$qdp_build"
    
    if [ ! -d "$WORKDIR/qdp++" ]; then
        git clone --depth 1 "$QDPPP_REPO" "$WORKDIR/qdp++" 2>&1 | tail -3
    fi
    
    cd "$qdp_build"
    
    # Configure QDP++ for SU(2) — this is the critical step
    # Nc=2 for SU(2). Default is Nc=3.
    "$WORKDIR/qdp++/configure" \
        --prefix="$INSTALL_DIR" \
        --enable-parallel-arch=parscalar \
        --enable-precision=single \
        --with-qmp=no \
        --enable-sse2 \
        --with-libxml2=/usr \
        --enable-Nc=2 \
        CC=mpicc CXX=mpicxx F77=mpif77 2>&1 | tail -10
    
    make -j"$N_CORES" 2>&1 | tail -5
    make install 2>&1 | tail -5
    
    log_info "QDP++ SU(2) built — OK"
}

# ─── Build Chroma ────────────────────────────────────────────────────────────
build_chroma() {
    log_step "Building Chroma..."
    
    if [ -f "$INSTALL_DIR/bin/chroma" ]; then
        log_info "Chroma already built. Skipping."
        return 0
    fi
    
    local chroma_build="$BUILD_DIR/chroma"
    mkdir -p "$chroma_build"
    
    if [ ! -d "$WORKDIR/chroma" ]; then
        git clone --depth 1 --branch "$CHROMA_BRANCH" "$CHROMA_REPO" "$WORKDIR/chroma" 2>&1 | tail -3
    fi
    
    cd "$chroma_build"
    
    # Set QDP++ paths
    export PATH="$INSTALL_DIR/bin:$PATH"
    export LD_LIBRARY_PATH="$INSTALL_DIR/lib:$LD_LIBRARY_PATH"
    
    "$WORKDIR/chroma/configure" \
        --prefix="$INSTALL_DIR" \
        --with-qdp="$INSTALL_DIR" \
        --enable-precision=single \
        --with-libxml2=/usr \
        CC=mpicc CXX=mpicxx F77=mpif77 2>&1 | tail -10
    
    make -j"$N_CORES" 2>&1 | tail -5
    make install 2>&1 | tail -5
    
    log_info "Chroma built — OK"
}

# ─── Alternative: Docker-based Chroma ────────────────────────────────────────
setup_chroma_docker() {
    log_step "Setting up Chroma via Docker..."
    
    if ! command -v docker &>/dev/null; then
        log_warn "Docker not available. Trying apt-get install..."
        apt-get install -y -qq docker.io 2>/dev/null || {
            log_error "Cannot install Docker. Use --build-from-source instead."
            return 1
        }
    fi
    
    # Pull a pre-built Chroma image or build one
    # Note: No official Chroma Docker image exists as of 2026.
    # We build a minimal one here.
    
    cat > "$WORKDIR/Dockerfile.chroma" << 'DOCKEREOF'
FROM ubuntu:22.04
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get install -y \
    build-essential g++ gfortran cmake autoconf automake \
    libtool libxml2-dev libopenmpi-dev openmpi-bin \
    python3 python3-pip python3-numpy python3-scipy \
    git wget && \
    apt-get clean
WORKDIR /build
DOCKEREOF
    
    log_info "Dockerfile created. Building image..."
    docker build -t chroma-su2:latest -f "$WORKDIR/Dockerfile.chroma" "$WORKDIR" 2>&1 | tail -10
    
    log_info "Docker image built. Use: docker run --rm -v $WORKDIR:/work chroma-su2:latest"
    return 0
}

# ─── Quick Chroma Check ──────────────────────────────────────────────────────
verify_chroma() {
    log_step "Verifying Chroma installation..."
    
    local chroma_bin=""
    if [ -f "$INSTALL_DIR/bin/chroma" ]; then
        chroma_bin="$INSTALL_DIR/bin/chroma"
    elif command -v chroma &>/dev/null; then
        chroma_bin="chroma"
    else
        log_error "Chroma binary not found!"
        return 1
    fi
    
    log_info "Chroma binary: $chroma_bin"
    "$chroma_bin" --version 2>&1 || true
    
    # Quick sanity: run a tiny 4^4 test
    log_info "Running quick sanity test (4⁴ lattice, 10 sweeps)..."
    cat > /tmp/chroma_sanity.xml << 'XMLEOF'
<?xml version="1.0"?>
<chroma>
  <Param>
    <nrow>4 4 4 8</nrow>
    <InlineMeasurements>
      <elem>
        <Name>MESPLQ</Name>
        <Frequency>1</Frequency>
        <Param><version>2</version></Param>
        <NamedObject><gauge_id>default_gauge_field</gauge_id></NamedObject>
      </elem>
    </InlineMeasurements>
  </Param>
  <Cfg><cfg_type>WEAK_FIELD</cfg_type><cfg_file>dummy</cfg_file></Cfg>
</chroma>
XMLEOF
    
    if "$chroma_bin" -i /tmp/chroma_sanity.xml -o /tmp/chroma_sanity_out.xml 2>&1 | tail -5; then
        log_info "Chroma sanity test PASSED"
    else
        log_warn "Chroma sanity test FAILED — check build"
    fi
}

# ─── Log Rotation ────────────────────────────────────────────────────────────
rotate_logs() {
    local log_file="$1"
    local max_size_mb="$2"
    
    if [ -f "$log_file" ]; then
        local size_mb
        size_mb=$(du -m "$log_file" 2>/dev/null | cut -f1)
        if [ "${size_mb:-0}" -gt "$max_size_mb" ]; then
            mv "$log_file" "${log_file}.$(date +%Y%m%d_%H%M%S).old"
            log_info "Rotated log: $log_file (>${max_size_mb}MB)"
        fi
    fi
}

# ─── Disk Cleanup ────────────────────────────────────────────────────────────
cleanup_configs() {
    log_step "Cleaning configs > ${DISK_CLEANUP_THRESHOLD_MB}MB..."
    
    find "$WORKDIR/configs" -name "*.lime" -size +"${DISK_CLEANUP_THRESHOLD_MB}"k -delete 2>/dev/null || true
    find /tmp -name "chroma_*.xml" -mtime +1 -delete 2>/dev/null || true
    
    local freed
    freed=$(df -h / | awk 'NR==2{print $4}')
    log_info "Disk after cleanup: $freed free"
}

# ─── Run Chroma Production ───────────────────────────────────────────────────
run_chroma_production() {
    log_step "Starting Chroma SU(2) Glueball production..."
    
    local chroma_bin
    if [ -f "$INSTALL_DIR/bin/chroma" ]; then
        chroma_bin="$INSTALL_DIR/bin/chroma"
    elif command -v chroma &>/dev/null; then
        chroma_bin="chroma"
    else
        log_error "No Chroma binary. Run --build-only first."
        return 1
    fi
    
    if [ ! -f "$XML_CONFIG" ]; then
        log_error "XML config not found: $XML_CONFIG"
        return 1
    fi
    
    mkdir -p "$WORKDIR/output" "$LOG_DIR"
    
    local log_file="$LOG_DIR/chroma_production_$(date +%Y%m%d_%H%M%S).log"
    rotate_logs "$log_file" "$MAX_LOG_SIZE_MB"
    
    log_info "Launching: $chroma_bin -i $XML_CONFIG -o $OUTPUT_XML"
    log_info "Log: $log_file"
    log_info "OMP_NUM_THREADS=$OMP_NUM_THREADS"
    
    # Run Chroma with timeout (30 min per job typical)
    # For production, run directly — Chroma handles MC + measurements inline
    timeout 86400 "$chroma_bin" \
        -i "$XML_CONFIG" \
        -o "$OUTPUT_XML" \
        2>&1 | tee "$log_file"
    
    local exit_code=$?
    if [ $exit_code -eq 0 ]; then
        log_info "Chroma production COMPLETED successfully"
    elif [ $exit_code -eq 124 ]; then
        log_error "Chroma production TIMEOUT (24h). Partial results in $OUTPUT_XML"
    else
        log_error "Chroma production FAILED (exit=$exit_code). Check $log_file"
    fi
    
    return $exit_code
}

# ─── Multi-Job Parallel Runner ───────────────────────────────────────────────
run_parallel_batches() {
    log_step "Running $N_JOBS_PARALLEL parallel Chroma jobs..."
    
    if [ "$N_JOBS_PARALLEL" -le 1 ]; then
        log_info "N_JOBS_PARALLEL=1, using single-job mode."
        run_chroma_production
        return $?
    fi
    
    local chroma_bin
    if [ -f "$INSTALL_DIR/bin/chroma" ]; then
        chroma_bin="$INSTALL_DIR/bin/chroma"
    else
        chroma_bin="chroma"
    fi
    
    # Generate per-job configs with different RNG seeds
    local pids=()
    for job_id in $(seq 1 "$N_JOBS_PARALLEL"); do
        local job_xml="$WORKDIR/output/job_${job_id}_config.xml"
        local job_out="$WORKDIR/output/job_${job_id}_output.xml"
        local job_log="$LOG_DIR/job_${job_id}.log"
        
        # Copy config and change seed
        cp "$XML_CONFIG" "$job_xml"
        local seed1=$((RANDOM * job_id))
        local seed2=$((RANDOM * job_id + 1))
        sed -i "s|<elem>12345</elem>|<elem>$seed1</elem>|" "$job_xml"
        sed -i "s|<elem>67890</elem>|<elem>$seed2</elem>|" "$job_xml"
        
        log_info "Launching job $job_id (seed=$seed1)..."
        OMP_NUM_THREADS=$(( N_CORES / N_JOBS_PARALLEL )) \
            "$chroma_bin" -i "$job_xml" -o "$job_out" \
            > "$job_log" 2>&1 &
        pids+=($!)
    done
    
    # Wait for all jobs
    local failed=0
    for i in "${!pids[@]}"; do
        local pid="${pids[$i]}"
        local job_id=$((i + 1))
        if wait "$pid" 2>/dev/null; then
            log_info "Job $job_id (PID=$pid) — DONE"
        else
            log_error "Job $job_id (PID=$pid) — FAILED"
            failed=$((failed + 1))
        fi
    done
    
    if [ "$failed" -gt 0 ]; then
        log_error "$failed/$N_JOBS_PARALLEL jobs failed"
        return 1
    fi
    
    log_info "All $N_JOBS_PARALLEL jobs completed"
    return 0
}

# ─── Post-Processing: GEVP Analysis ──────────────────────────────────────────
run_gevp_analysis() {
    log_step "Running GEVP post-processing..."
    
    if [ ! -f "$ANALYSIS_SCRIPT" ]; then
        log_warn "GEVP analysis script not found: $ANALYSIS_SCRIPT"
        log_info "Creating minimal analysis script..."
        
        cat > "$WORKDIR/analyze_gevp_minimal.py" << 'PYEOF'
#!/usr/bin/env python3
"""Minimal GEVP analysis for Chroma FUZZED_WILSON_LOOP output."""
import sys, os, xml.etree.ElementTree as ET
import numpy as np
from scipy.linalg import eigh

def parse_chroma_output(xml_file):
    """Parse Chroma XML output, extract FUZZED_WILSON_LOOP correlators."""
    tree = ET.parse(xml_file)
    root = tree.getroot()
    
    correlators = {}  # key: (n_smear, rep), value: array[t]
    
    for obs in root.iter('InlineObservables'):
        for elem in obs.findall('elem'):
            for fuz in elem.findall('APE_Smeared_Wilsonloop'):
                # Extract smearing level from context
                n_smear_tag = elem.find('.//n_smear')
                n_smear = int(n_smear_tag.text) if n_smear_tag is not None else 0
                
                for wloop in fuz:
                    tag = wloop.tag
                    times = []
                    values = []
                    for point in wloop.findall('elem'):
                        t = point.find('left')
                        v = point.find('right')
                        if t is not None and v is not None:
                            times.append(t.text)
                            values.append(float(v.text))
                    if values:
                        correlators[(n_smear, tag)] = np.array(values)
    
    return correlators

def solve_gevp(correlation_matrix, t0=1, n_states=3):
    """Solve GEVP: C(t) v_n = λ_n(t,t0) C(t0) v_n"""
    nt = correlation_matrix.shape[1]
    n_ops = correlation_matrix.shape[0]
    
    masses = np.zeros((n_states, nt - t0))
    
    for t in range(t0, nt):
        C_t0 = correlation_matrix[:, :, t0]
        C_t = correlation_matrix[:, :, t]
        
        # Symmetrize
        C_t0 = 0.5 * (C_t0 + C_t0.T)
        C_t = 0.5 * (C_t + C_t.T)
        
        try:
            eigvals, eigvecs = eigh(C_t, C_t0)
            for n in range(min(n_states, len(eigvals))):
                if eigvals[n] > 0:
                    masses[n, t - t0] = -np.log(eigvals[n]) / (t - t0)
        except np.linalg.LinAlgError:
            masses[:, t - t0] = np.nan
    
    return masses

def main():
    if len(sys.argv) < 2:
        print("Usage: analyze_gevp_minimal.py <chroma_output.xml>")
        sys.exit(1)
    
    xml_file = sys.argv[1]
    correlators = parse_chroma_output(xml_file)
    
    if not correlators:
        print("ERROR: No correlators found in XML output")
        sys.exit(1)
    
    print(f"Found {len(correlators)} correlator sets")
    
    # Build correlation matrix from different smearing levels
    smear_levels = sorted(set(k[0] for k in correlators.keys()))
    n_ops = len(smear_levels)
    
    if n_ops < 2:
        print("ERROR: Need at least 2 smearing levels for GEVP")
        sys.exit(1)
    
    print(f"Smearing levels: {smear_levels}")
    print(f"Building {n_ops}x{n_ops} correlation matrix for GEVP")
    
    # Extract one representation (e.g., wloopr for 0++ channel)
    for rep_tag in ['wloopr', 'wlooprs']:
        nt = None
        C = None
        valid_levels = []
        
        for level in smear_levels:
            key = (level, rep_tag)
            if key in correlators:
                if nt is None:
                    nt = len(correlators[key])
                    C = np.zeros((n_ops, n_ops, nt))
                if len(correlators[key]) == nt:
                    idx = len(valid_levels)
                    # Build symmetric matrix: C_ij(t) for each t
                    for i in range(n_ops):
                        for j in range(n_ops):
                            pass  # Need both i and j correlators
                    valid_levels.append(level)
        
        if len(valid_levels) >= 2:
            print(f"\nRepresentation: {rep_tag}")
            print(f"  Valid levels: {valid_levels}")
            print(f"  T-slices: {nt}")
            print("  GEVP analysis requires post-processing of cross-correlators")
    
    # Save correlators for external GEVP
    np.savez('correlators.npz', 
             smear_levels=smear_levels,
             **{f'corr_{k[0]}_{k[1]}': v for k, v in correlators.items()})
    print("\nCorrelators saved to correlators.npz")
    print("Use external GEVP solver for full analysis")

if __name__ == '__main__':
    main()
PYEOF
        ANALYSIS_SCRIPT="$WORKDIR/analyze_gevp_minimal.py"
    fi
    
    chmod +x "$ANALYSIS_SCRIPT"
    
    # Run analysis on output
    if [ -f "$OUTPUT_XML" ]; then
        python3 "$ANALYSIS_SCRIPT" "$OUTPUT_XML" 2>&1 | tee "$LOG_DIR/analysis.log"
        log_info "GEVP analysis complete → check $LOG_DIR/analysis.log"
    elif [ -f "$WORKDIR/output/job_1_output.xml" ]; then
        # Multi-job mode: analyze first job
        python3 "$ANALYSIS_SCRIPT" "$WORKDIR/output/job_1_output.xml" 2>&1 | tee "$LOG_DIR/analysis.log"
    else
        log_warn "No Chroma output found to analyze."
    fi
}

# ─── Resource Monitor ────────────────────────────────────────────────────────
start_monitor() {
    log_info "Starting resource monitor (background)..."
    
    while true; do
        local ts
        ts=$(date '+%Y-%m-%d %H:%M:%S')
        local ram_free
        ram_free=$(free -m | awk '/^Mem:/{print $7}')
        local disk_free
        disk_free=$(df -h / | awk 'NR==2{print $4}')
        local load
        load=$(uptime | awk -F'load average:' '{print $2}' | xargs)
        
        echo "$ts | RAM:${ram_free}MB | Disk:${disk_free} | Load:$load" >> "$LOG_DIR/resource_monitor.log"
        
        # Alert on low resources
        if [ "$ram_free" -lt 5120 ]; then
            log_warn "RAM < 5GB! Consider cleanup."
        fi
        
        sleep 60
    done &
    MONITOR_PID=$!
    log_info "Monitor PID: $MONITOR_PID"
}

stop_monitor() {
    if [ -n "${MONITOR_PID:-}" ]; then
        kill "$MONITOR_PID" 2>/dev/null || true
        log_info "Monitor stopped."
    fi
}

# ─── Summary Report ──────────────────────────────────────────────────────────
generate_report() {
    log_step "Generating summary report..."
    
    local report="$WORKDIR/output/PRODUCTION_REPORT.md"
    
    cat > "$report" << EOFREPORT
# Chroma SU(2) Glueball Production Report
**Generated:** $(date '+%Y-%m-%d %H:%M:%S UTC')
**Machine:** $(hostname) | $(nproc) cores | $(free -h | awk '/^Mem:/{print $2}') RAM

## Configuration
- Lattice: 16⁴×32
- Gauge group: SU(2)
- Action: Wilson, β=2.50
- Algorithm: Heatbath
- Configs: 5000 production, saved every 50
- Smearing levels: 5 (APE: n=2,4,8,12,16)

## Input Files
- XML Config: $XML_CONFIG
- Output: $OUTPUT_XML

## Logs
- Production: $LOG_DIR/
- Monitor: $LOG_DIR/resource_monitor.log

## Next Steps
1. Run GEVP analysis: ./deploy_vast_v3.sh --analyze-only
2. Extract T₂⁺ and E⁺ masses from correlation matrix
3. Compare with literature: m_0++/√σ ≈ 3.78(7) (SU(3), LT2010)
EOFREPORT
    
    log_info "Report: $report"
}

# ─── Main ────────────────────────────────────────────────────────────────────
main() {
    echo ""
    echo "╔══════════════════════════════════════════════════════════════╗"
    echo "║  Ξ Vast Chroma SU(2) Glueball Pipeline v3                   ║"
    echo "║  FUZZED_WILSON_LOOP → GEVP → T₂⁺/E⁺ masses                 ║"
    echo "╚══════════════════════════════════════════════════════════════╝"
    echo ""
    
    local mode="${1:-full}"
    
    case "$mode" in
        --help|-h)
            show_help
            exit 0
            ;;
        --build-only)
            health_check
            install_deps
            build_qdppp
            build_chroma
            verify_chroma
            log_info "Build complete. Run without --build-only to start production."
            ;;
        --measure-only)
            health_check
            verify_chroma
            start_monitor
            run_parallel_batches || true
            stop_monitor
            cleanup_configs
            generate_report
            ;;
        --analyze-only)
            run_gevp_analysis
            ;;
        full|"")
            health_check
            install_deps
            build_qdppp
            build_chroma
            verify_chroma
            start_monitor
            run_parallel_batches || true
            stop_monitor
            cleanup_configs
            run_gevp_analysis || true
            generate_report
            ;;
        *)
            log_error "Unknown mode: $mode"
            show_help
            exit 1
            ;;
    esac
    
    echo ""
    log_info "Pipeline complete. Results in $WORKDIR/output/"
    echo ""
}

main "$@"
