#!/usr/bin/env bash
# ============================================================================
# ECI v4/v5 MCMC runner — container entrypoint.
# Assumes the repo is bind-mounted at /opt/eci and this script is invoked via
# the Dockerfile ENTRYPOINT.
# ============================================================================
set -euo pipefail

REPO="${REPO:-/opt/eci}"
PARAMS="${PARAMS:-$REPO/mcmc/params/eci_nmc.yaml}"
PACKAGES="${PACKAGES:-$REPO/mcmc/packages}"
CHAINS_DIR="${CHAINS_DIR:-$REPO/mcmc/chains}"
NCHAINS="${NCHAINS:-4}"
OMP_NUM_THREADS="${OMP_NUM_THREADS:-5}"
export OMP_NUM_THREADS

TIMESTAMP="$(date -u +%Y%m%dT%H%M%SZ)"
LOG="$CHAINS_DIR/run_${TIMESTAMP}.log"

mkdir -p "$PACKAGES" "$CHAINS_DIR"

# --- Optional env file (Planck clik keys, S3 creds, …) ---------------------
if [[ -f "$REPO/mcmc/deploy/.env" ]]; then
    # shellcheck disable=SC1091
    set -a && source "$REPO/mcmc/deploy/.env" && set +a
fi

echo "[run_mcmc] $(date -u) — starting ECI MCMC" | tee -a "$LOG"
echo "[run_mcmc] params   = $PARAMS"            | tee -a "$LOG"
echo "[run_mcmc] packages = $PACKAGES"          | tee -a "$LOG"
echo "[run_mcmc] chains   = $CHAINS_DIR"        | tee -a "$LOG"
echo "[run_mcmc] np       = $NCHAINS  OMP=$OMP_NUM_THREADS" | tee -a "$LOG"

# --- Install cosmological likelihoods (~5 GB, idempotent) -------------------
# --force-reinstall-upgrades skipped; cobaya-install is idempotent.
echo "[run_mcmc] cobaya-install cosmo -p $PACKAGES" | tee -a "$LOG"
cobaya-install cosmo -p "$PACKAGES" --skip-global 2>&1 | tee -a "$LOG"

# --- Run the chain ----------------------------------------------------------
# -r : resume if chains already exist (spot-interruption friendly)
# cobaya writes a .checkpoint every ~30 min by default.
echo "[run_mcmc] launching mpirun -np $NCHAINS cobaya-run -r $PARAMS" | tee -a "$LOG"
set +e
mpirun --allow-run-as-root -np "$NCHAINS" cobaya-run -r "$PARAMS" \
    --packages-path "$PACKAGES" 2>&1 | tee -a "$LOG"
RC=${PIPESTATUS[0]}
set -e

echo "[run_mcmc] cobaya-run exit=$RC at $(date -u)" | tee -a "$LOG"

# --- Tarball the chains -----------------------------------------------------
CHAIN_BASE="$(basename "$(grep -E '^output:' "$PARAMS" | awk '{print $2}' | tr -d '"')" 2>/dev/null || true)"
TARBALL="$CHAINS_DIR/chains_${TIMESTAMP}.tar.gz"
echo "[run_mcmc] archiving → $TARBALL" | tee -a "$LOG"
tar -czf "$TARBALL" -C "$REPO/mcmc" chains 2>>"$LOG" || \
    echo "[run_mcmc] WARN: tar failed" | tee -a "$LOG"

# --- Optional S3 upload -----------------------------------------------------
if [[ -n "${S3_BUCKET:-}" ]]; then
    echo "[run_mcmc] uploading to s3://$S3_BUCKET/" | tee -a "$LOG"
    if command -v aws >/dev/null 2>&1; then
        aws s3 cp "$TARBALL" "s3://$S3_BUCKET/eci_mcmc/chains_${TIMESTAMP}.tar.gz" \
            2>&1 | tee -a "$LOG" || \
            echo "[run_mcmc] WARN: S3 upload failed; tarball remains on local disk" | tee -a "$LOG"
        aws s3 cp "$LOG" "s3://$S3_BUCKET/eci_mcmc/run_${TIMESTAMP}.log" \
            2>&1 | tee -a "$LOG" || true
    else
        echo "[run_mcmc] WARN: aws CLI not in PATH, skipping S3 upload" | tee -a "$LOG"
    fi
else
    echo "[run_mcmc] S3_BUCKET not set — tarball kept at $TARBALL" | tee -a "$LOG"
fi

exit "$RC"
