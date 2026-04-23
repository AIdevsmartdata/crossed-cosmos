#!/usr/bin/env bash
# V8-tq3-preflight.sh — pre-flight check before starting qwen-tq3.service
# Run AFTER build + download complete, BEFORE `systemctl --user start qwen-tq3`.
# Exit 0 = green, exit 1 = hard block, exit 2 = soft warn (proceed with caution).
set -u

BIN=/home/remondiere/github-repos/llama.cpp-tq3/build_sm120/bin/llama-server
GGUF=/home/remondiere/.openclaw/models/Qwen3.6-35B-A3B-TQ3_4S/Qwen3.6-35B-A3B-TQ3_4S.gguf
PORT=8083
WARN=0
FAIL=0

say()  { printf '[preflight] %s\n' "$*"; }
warn() { printf '[preflight][WARN] %s\n' "$*"; WARN=1; }
fail() { printf '[preflight][FAIL] %s\n' "$*"; FAIL=1; }

# 1. Binary sanity
[[ -x "$BIN" ]] || fail "binary missing: $BIN"
"$BIN" --version >/dev/null 2>&1 || fail "binary --version failed (linker/sm120 issue?)"

# 2. GGUF present + readable
[[ -r "$GGUF" ]] || fail "GGUF missing: $GGUF"
GGUF_SIZE_GB=$(stat -c%s "$GGUF" 2>/dev/null | awk '{printf "%.2f", $1/1073741824}')
say "GGUF size: ${GGUF_SIZE_GB} GiB"
# TQ3_4S card says 12.4 GiB. Accept 12.0-13.0.
awk "BEGIN{exit !($GGUF_SIZE_GB > 12.0 && $GGUF_SIZE_GB < 13.0)}" \
  || warn "GGUF size outside expected 12.0-13.0 GiB range (partial download?)"

# 3. GGUF magic
MAGIC=$(head -c4 "$GGUF" | xxd -p)
[[ "$MAGIC" == "47475546" ]] || fail "GGUF magic bytes wrong (got $MAGIC, want 47475546 = 'GGUF')"

# 4. Cache type tq3_0 supported
"$BIN" --help 2>&1 | grep -q "tq3_0" \
  || fail "binary does not list tq3_0 as cache type — fork built without TQ3 support"

# 5. Port 8083 free
if ss -ltn 2>/dev/null | awk '{print $4}' | grep -q ":${PORT}$"; then
  fail "port $PORT already in use (another service is bound)"
fi

# 6. VRAM budget
# Qwen3.6-35B-A3B has 32 full-attn layers (approx for Qwen3.5/3.6 MoE). KV cache bytes:
#   bytes_per_token = 2 (K+V) * n_layers_full_attn * n_kv_heads * head_dim * bpw/8
# With Qwen3.5-35B-A3B: 10/40 layers are full attn, rest GDN (no KV). Qwen3.6 likely similar.
# Ballpark @ 64K ctx, K=q4_0 (4.5 bpw), V=tq3_0 (~3 bpw), 10 full-attn layers,
# 4 kv heads x 128 head_dim: ~650 MB. Safe.
# Model weights: 12.4 GiB. Total VRAM target: ~13.5 GiB. Fits in 16 GiB.
FREE_MIB=$(nvidia-smi --query-gpu=memory.free --format=csv,noheader,nounits 2>/dev/null | head -1)
TOTAL_MIB=$(nvidia-smi --query-gpu=memory.total --format=csv,noheader,nounits 2>/dev/null | head -1)
say "VRAM free=${FREE_MIB} MiB / total=${TOTAL_MIB} MiB"
NEED_MIB=14500  # 12.4 GiB weights + ~700 MB KV @ 64K + ~1.4 GB compute buffers
if (( FREE_MIB < NEED_MIB )); then
  warn "VRAM free ${FREE_MIB} MiB < need ~${NEED_MIB} MiB. Stop chimere-server/qwen35-* first, OR start at -c 16384."
fi

# 7. Verify tokenizer+chat_template embedded via dry-run load (1s timeout OK — we just want first logs)
LOG=$(mktemp)
timeout 30 "$BIN" -m "$GGUF" -ngl 0 -c 512 --port 28083 --host 127.0.0.1 \
  >"$LOG" 2>&1 &
PID=$!
sleep 12
kill -TERM "$PID" 2>/dev/null; wait "$PID" 2>/dev/null
grep -qi "tokenizer"       "$LOG" || warn "dry-run: no tokenizer log line (parsing may have failed earlier)"
grep -qi "chat_template\|chat template\|jinja" "$LOG" || warn "dry-run: no chat template detected in GGUF"
grep -qi "unknown ggml_type\|unsupported\|failed to load" "$LOG" && fail "dry-run reported a fatal load error (see $LOG)"
say "dry-run log: $LOG"

# 8. Summary
if (( FAIL )); then
  say "RESULT: FAIL — do NOT start service. Review errors above."
  exit 1
fi
if (( WARN )); then
  say "RESULT: WARN — proceed with the auto-mitigation cascade (V8-tq3-launch.sh)."
  exit 2
fi
say "RESULT: GREEN — safe to: systemctl --user start qwen-tq3"
exit 0
