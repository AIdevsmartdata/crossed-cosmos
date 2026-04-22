#!/usr/bin/env bash
# Incremental off-site backup of the chains/ directory.
# Intended for cron every 30 min on the Vast.ai instance:
#   */30 * * * * /root/eci/mcmc/deploy/checkpoint_rsync.sh >> /var/log/ckpt.log 2>&1
#
# The owner supplies BACKUP_TARGET at runtime. Examples:
#   export BACKUP_TARGET='user@u123456.your-storagebox.de:eci-chains/'
#   export BACKUP_TARGET='rsync://user@rsync.net/eci-chains/'
# S3 is NOT handled here (use `aws s3 sync` in a separate cron if needed).
#
# No secrets are read from this script. SSH keys must be pre-provisioned in
# /root/.ssh/ by the owner after first SSH login.

set -euo pipefail

CHAINS_DIR="/root/eci/chains"
LOCK="/tmp/ckpt_rsync.lock"

# Allow cron env to be minimal; source /etc/environment for BACKUP_TARGET if set there.
if [ -z "${BACKUP_TARGET:-}" ] && [ -f /etc/environment ]; then
    # shellcheck disable=SC1091
    set -a; . /etc/environment; set +a
fi

if [ -z "${BACKUP_TARGET:-}" ]; then
    echo "[$(date -Iseconds)] BACKUP_TARGET unset; skipping." >&2
    exit 0
fi

if [ ! -d "$CHAINS_DIR" ]; then
    echo "[$(date -Iseconds)] $CHAINS_DIR absent; nothing to back up."
    exit 0
fi

# Single-flight: skip if a previous rsync is still running.
exec 9>"$LOCK"
if ! flock -n 9; then
    echo "[$(date -Iseconds)] Previous rsync still running; skipping."
    exit 0
fi

echo "[$(date -Iseconds)] rsync -> $BACKUP_TARGET"

# --partial + --append-verify: safe resume of interrupted transfers.
# Exclude lock/progress scratch files Cobaya writes mid-step.
rsync -av --partial --append-verify \
    --exclude '*.lock' \
    --exclude '*.tmp' \
    --exclude '*.progress' \
    -e "ssh -o StrictHostKeyChecking=accept-new -o ConnectTimeout=20" \
    "$CHAINS_DIR/" \
    "$BACKUP_TARGET"

echo "[$(date -Iseconds)] rsync OK"
