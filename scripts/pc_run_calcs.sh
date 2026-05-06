#!/bin/bash
# pc_run_calcs.sh — Kevin's PC, run all pending ECI calculations + commit + push to GH
# Usage: bash /home/remondiere/eci-v8/scripts/pc_run_calcs.sh
# Idempotent: checks file existence before each step; safe to re-run

set -u  # do NOT set -e: we want to continue past failures and log them
set -o pipefail

# === CONFIG ===
REPO_ROOT="/home/remondiere/eci-v8"
LOG_ROOT="$REPO_ROOT/logs/run_$(date +%Y%m%d_%H%M%S)"
mkdir -p "$LOG_ROOT"
RUN_LOG="$LOG_ROOT/run.log"

# Activate conda env (mamba/sage installed via install_sage_pc.sh)
source "$HOME/miniforge3/etc/profile.d/conda.sh" 2>/dev/null \
  || source "$HOME/anaconda3/etc/profile.d/conda.sh" 2>/dev/null \
  || { echo "[ERR] no conda found" | tee -a "$RUN_LOG"; exit 1; }
conda activate sage 2>>"$RUN_LOG" || { echo "[ERR] cannot activate 'sage' env" | tee -a "$RUN_LOG"; exit 1; }

echo "=== ECI run started $(date -u +%FT%TZ) ===" | tee -a "$RUN_LOG"
echo "REPO_ROOT=$REPO_ROOT" | tee -a "$RUN_LOG"
echo "LOG_ROOT=$LOG_ROOT" | tee -a "$RUN_LOG"
which python pari-gp gp sage 2>/dev/null | tee -a "$RUN_LOG"
python --version 2>>"$RUN_LOG" | tee -a "$RUN_LOG"

# === STEP 1: M82 r3c1 high-precision (mpmath + PARI subprocess) ===
M82_DIR="$REPO_ROOT/notes/eci_v7_aspiration/M82_HIGHPREC"
M82_SCRIPT="$M82_DIR/r3c1_highprec_v3.py"
if [ -f "$M82_SCRIPT" ]; then
  echo -e "\n=== [STEP 1] M82 r3c1_highprec_v3.py ===" | tee -a "$RUN_LOG"
  echo "Smoke test first..." | tee -a "$RUN_LOG"
  python "$M82_SCRIPT" --smoke > "$LOG_ROOT/m82_smoke.log" 2>&1 \
    && echo "[OK] M82 smoke" | tee -a "$RUN_LOG" \
    || echo "[WARN] M82 smoke failed (see m82_smoke.log)" | tee -a "$RUN_LOG"
  echo "Full run..." | tee -a "$RUN_LOG"
  python "$M82_SCRIPT" > "$LOG_ROOT/m82_full.log" 2>&1 \
    && echo "[OK] M82 full" | tee -a "$RUN_LOG" \
    || echo "[WARN] M82 full failed (see m82_full.log)" | tee -a "$RUN_LOG"
  cp -v "$LOG_ROOT/m82_full.log" "$M82_DIR/r3c1_highprec_v3.log" 2>>"$RUN_LOG"
else
  echo "[SKIP] M82 script not found at $M82_SCRIPT" | tee -a "$RUN_LOG"
fi

# === STEP 2: M87 RMT PARI/GP zero statistics (if scripts present) ===
M87_DIR="$REPO_ROOT/notes/eci_v7_aspiration/M87_RMT_NUMERICAL"
M87_R1="$M87_DIR/r_1_test_v2.gp"
M87_PC="$M87_DIR/pair_correlation_v2.gp"
if [ -f "$M87_R1" ]; then
  echo -e "\n=== [STEP 2a] M87 r_1_test_v2.gp ===" | tee -a "$RUN_LOG"
  if command -v gp >/dev/null 2>&1; then
    cd "$M87_DIR" && gp -q < "$M87_R1" > "$LOG_ROOT/m87_r1.log" 2>&1 \
      && echo "[OK] M87 r_1 test" | tee -a "$RUN_LOG" \
      || echo "[WARN] M87 r_1 test failed" | tee -a "$RUN_LOG"
    cp -v "$LOG_ROOT/m87_r1.log" "$M87_DIR/r_1_test_v2.log" 2>>"$RUN_LOG"
  else
    echo "[SKIP] gp (PARI/GP) not on PATH; sudo apt install pari-gp" | tee -a "$RUN_LOG"
  fi
fi
if [ -f "$M87_PC" ]; then
  echo -e "\n=== [STEP 2b] M87 pair_correlation_v2.gp ===" | tee -a "$RUN_LOG"
  if command -v gp >/dev/null 2>&1; then
    cd "$M87_DIR" && gp -q < "$M87_PC" > "$LOG_ROOT/m87_pc.log" 2>&1 \
      && echo "[OK] M87 pair correlation" | tee -a "$RUN_LOG" \
      || echo "[WARN] M87 pair correlation failed" | tee -a "$RUN_LOG"
    cp -v "$LOG_ROOT/m87_pc.log" "$M87_DIR/pair_correlation_v2.log" 2>>"$RUN_LOG"
  fi
fi
if [ ! -f "$M87_R1" ] && [ ! -f "$M87_PC" ]; then
  echo "[SKIP] M87 scripts not yet present (sub-agent still running on VPS)" | tee -a "$RUN_LOG"
fi

# === STEP 3: M76 Stage 2 R3-C-1 + F1 falsifier (Sage 10.7) ===
M76_DIR="$REPO_ROOT/notes/eci_v7_aspiration/M76_SAGE_STAGE2"
for s in r3_c1_falsifier_v2.sage f1_falsifier_v2.sage; do
  if [ -f "$M76_DIR/$s" ]; then
    echo -e "\n=== [STEP 3] M76 $s ===" | tee -a "$RUN_LOG"
    cd "$M76_DIR" && sage "$s" > "$LOG_ROOT/m76_${s%.sage}.log" 2>&1 \
      && echo "[OK] M76 $s" | tee -a "$RUN_LOG" \
      || echo "[WARN] M76 $s failed" | tee -a "$RUN_LOG"
    cp -v "$LOG_ROOT/m76_${s%.sage}.log" "$M76_DIR/${s%.sage}.log" 2>>"$RUN_LOG"
  fi
done

# === STEP 4: M50 NUTS GPU Wolf chain status ===
echo -e "\n=== [STEP 4] M50 NUTS GPU status ===" | tee -a "$RUN_LOG"
M50_DIR="$REPO_ROOT/notes/eci_v7_aspiration/M50_NUTS_GPU"
[ -d "$M50_DIR" ] && ls -la "$M50_DIR" | tee -a "$RUN_LOG" || echo "[INFO] No M50 dir (running elsewhere?)" | tee -a "$RUN_LOG"
# Detect any running NUTS process
ps aux | grep -iE "nuts|numpyro|jax.*sample" | grep -v grep | tee -a "$RUN_LOG" || echo "[INFO] No NUTS process active" | tee -a "$RUN_LOG"

# === STEP 5: GIT commit + push to GH ===
echo -e "\n=== [STEP 5] git commit + push ===" | tee -a "$RUN_LOG"
cd "$REPO_ROOT" || { echo "[ERR] cannot cd $REPO_ROOT" | tee -a "$RUN_LOG"; exit 1; }
git status --short | tee -a "$RUN_LOG"
git add -- "notes/eci_v7_aspiration/M82_HIGHPREC/*.log" \
            "notes/eci_v7_aspiration/M87_RMT_NUMERICAL/*.log" \
            "notes/eci_v7_aspiration/M76_SAGE_STAGE2/*.log" \
            "logs/run_*/" 2>/dev/null || true
if ! git diff --cached --quiet 2>/dev/null; then
  git commit -m "PC run $(date -u +%FT%TZ): M82 high-prec + M87 RMT + M76 Stage2 logs" \
    | tee -a "$RUN_LOG"
  git push origin main 2>&1 | tee -a "$RUN_LOG" \
    && echo "[OK] pushed to GH" | tee -a "$RUN_LOG" \
    || echo "[WARN] push failed (network? auth?)" | tee -a "$RUN_LOG"
else
  echo "[INFO] no new logs to commit" | tee -a "$RUN_LOG"
fi

echo -e "\n=== ECI run finished $(date -u +%FT%TZ) ===" | tee -a "$RUN_LOG"
echo "Logs at: $LOG_ROOT"
echo "Tail with: tail -f $RUN_LOG"
