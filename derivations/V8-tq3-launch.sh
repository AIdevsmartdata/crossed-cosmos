#!/usr/bin/env bash
# V8-tq3-launch.sh — auto-mitigation cascade for qwen-tq3 OOM failures.
# Tries -c 65536, then 32768, 16384, 8192. Rolls back to chimere-server on total failure.
set -u

UNIT=qwen-tq3.service
FALLBACK=chimere-server.service
HEALTH="http://127.0.0.1:8083/health"
DROPIN_DIR="$HOME/.config/systemd/user/${UNIT}.d"
OVERRIDE="$DROPIN_DIR/10-ctx-override.conf"

mkdir -p "$DROPIN_DIR"

try_ctx() {
  local ctx=$1
  echo "[launch] trying -c $ctx"
  cat >"$OVERRIDE" <<EOF
[Service]
ExecStart=
ExecStart=/home/remondiere/github-repos/llama.cpp-tq3/build_sm120/bin/llama-server \\
  -m /home/remondiere/.openclaw/models/Qwen3.6-35B-A3B-TQ3_4S/Qwen3.6-35B-A3B-TQ3_4S.gguf \\
  -ngl 99 -fa on -ctk q4_0 -ctv tq3_0 \\
  -c ${ctx} -np 1 -b 4096 -ub 512 -t 14 --threads-batch 14 \\
  --jinja --reasoning-format deepseek --no-context-shift --metrics --cont-batching \\
  --temp 0.7 --top-p 0.8 --top-k 20 --min-p 0.0 \\
  --host 127.0.0.1 --port 8083
EOF
  systemctl --user daemon-reload
  systemctl --user restart "$UNIT"
  for i in $(seq 1 40); do
    sleep 3
    if curl -sf "$HEALTH" >/dev/null 2>&1; then
      echo "[launch] OK at -c $ctx"
      return 0
    fi
    # Detect CUDA OOM in journal early
    if journalctl --user -u "$UNIT" --since "90 seconds ago" 2>/dev/null \
       | grep -qiE "cudaMalloc.*out of memory|CUDA error.*out of memory|failed to allocate"; then
      echo "[launch] OOM at -c $ctx"
      return 1
    fi
  done
  echo "[launch] timeout at -c $ctx"
  return 1
}

for ctx in 65536 32768 16384 8192; do
  if try_ctx "$ctx"; then
    echo "[launch] SUCCESS ctx=$ctx (override persisted in $OVERRIDE)"
    exit 0
  fi
done

echo "[launch] ALL ctx sizes failed — rolling back to $FALLBACK"
systemctl --user stop "$UNIT"
rm -f "$OVERRIDE"; systemctl --user daemon-reload
# Only start fallback if it's not already running
systemctl --user is-active --quiet "$FALLBACK" || systemctl --user start "$FALLBACK"
exit 1
