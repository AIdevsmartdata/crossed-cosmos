#!/bin/bash
# vps_fetch_results.sh — VPS Hostinger, fetch latest PC results from GH + report new files
# Usage: bash /root/crossed-cosmos/scripts/vps_fetch_results.sh

set -u
set -o pipefail

REPO_ROOT="/root/crossed-cosmos"
cd "$REPO_ROOT" || { echo "[ERR] cannot cd $REPO_ROOT"; exit 1; }

echo "=== VPS fetch started $(date -u +%FT%TZ) ==="

# Save current HEAD before pull (to detect what's new)
HEAD_BEFORE=$(git rev-parse HEAD)
echo "HEAD before: $HEAD_BEFORE"

# Fetch latest from GH
git fetch origin main 2>&1 | sed 's/^/[fetch] /'
git pull --ff-only origin main 2>&1 | sed 's/^/[pull] /' \
  || { echo "[ERR] non-FF pull — manual merge needed"; exit 1; }

HEAD_AFTER=$(git rev-parse HEAD)
echo "HEAD after:  $HEAD_AFTER"

if [ "$HEAD_BEFORE" = "$HEAD_AFTER" ]; then
  echo "[INFO] no new commits since last fetch"
else
  echo -e "\n=== NEW COMMITS ==="
  git log --oneline "$HEAD_BEFORE..$HEAD_AFTER"
  echo -e "\n=== NEW FILES ==="
  git diff --name-only "$HEAD_BEFORE..$HEAD_AFTER" | grep -E '\.(log|md|csv|json)$' | head -30
fi

# Summarize the latest M82 / M87 / M76 results
echo -e "\n=== KEY RESULT FILES (status snapshot) ==="
for f in \
  notes/eci_v7_aspiration/M82_HIGHPREC/r3c1_highprec_v3.log \
  notes/eci_v7_aspiration/M87_RMT_NUMERICAL/r_1_test_v2.log \
  notes/eci_v7_aspiration/M87_RMT_NUMERICAL/pair_correlation_v2.log \
  notes/eci_v7_aspiration/M76_SAGE_STAGE2/r3_c1_falsifier_v2.log \
  notes/eci_v7_aspiration/M76_SAGE_STAGE2/f1_falsifier_v2.log \
  notes/eci_v7_aspiration/M50_NUTS_GPU/wolf_chain_4.log
do
  if [ -f "$REPO_ROOT/$f" ]; then
    SIZE=$(stat -c%s "$REPO_ROOT/$f")
    MTIME=$(stat -c%y "$REPO_ROOT/$f" | cut -d. -f1)
    echo "[OK] $f  ($SIZE bytes, $MTIME)"
    # Print last 10 lines for quick verdict
    echo "    --- last 10 lines ---"
    tail -10 "$REPO_ROOT/$f" | sed 's/^/    /'
    echo ""
  else
    echo "[MISSING] $f"
  fi
done

# Quick PASS/FAIL grep for M82 + M87 verdicts
echo -e "\n=== VERDICT GREP ==="
grep -hE 'PASS|FAIL|ANOMAL|verdict|Verdict|VERDICT|deviation' \
     notes/eci_v7_aspiration/M82_HIGHPREC/*.log \
     notes/eci_v7_aspiration/M87_RMT_NUMERICAL/*.log \
     notes/eci_v7_aspiration/M76_SAGE_STAGE2/*.log \
     2>/dev/null | head -20

echo -e "\n=== VPS fetch finished $(date -u +%FT%TZ) ==="
