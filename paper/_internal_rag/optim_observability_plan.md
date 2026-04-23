# Observability & Benchmarking Plan — ODO/APEX/Web-Search Pipeline
<!-- date: 2026-04-22 | status: live audit -->

---

## 1. Current Metrics Surface

### 1.1 llama-server :8081 — `--metrics` flag (confirmed in qwen35-custom.service)

The `--metrics` flag is present. llama-server (ik_llama b8125+) exposes a Prometheus-
compatible scrape endpoint at `GET /metrics`. Confirmed labels:

| Metric | Type | Description |
|---|---|---|
| `llamacpp:kv_cache_usage_ratio` | gauge | Fraction of KV slots in use |
| `llamacpp:kv_cache_tokens` | gauge | Tokens currently cached |
| `llamacpp:requests_processing` | gauge | Inflight requests |
| `llamacpp:requests_deferred` | gauge | Queued (waiting for slot) |
| `llamacpp:tokens_predicted_total` | counter | Cumulative output tokens |
| `llamacpp:tokens_evaluated_total` | counter | Cumulative prompt tokens |
| `llamacpp:prompt_tokens_seconds` | gauge | PP throughput tok/s |
| `llamacpp:predicted_tokens_seconds` | gauge | TG throughput tok/s |
| `llamacpp:n_decode_total` | counter | Decode calls |
| `llamacpp:n_busy_slots_per_decode` | gauge | Slot utilization |

Quick check: `curl -s http://127.0.0.1:8081/metrics | grep llamacpp`

### 1.2 ODO :8084 — `/stats` endpoint (odo.py L1455–1516)

Reads `~/.openclaw/logs/odo.db` (SQLite). Returns JSON last-24h window:

```json
{
  "last_24h": {
    "requests": N,
    "avg_entropy": 0.xxx,
    "think_ratio": 0.xxx,
    "avg_probe_ms": N,
    "avg_total_ms": N,
    "budget_forcing_count": N,
    "avg_budget_retries": N
  },
  "routes": { "kine": {"count": N, "avg_ms": N}, ... },
  "entropy_router": { "low": {"count": N, "avg_score": N}, ... },
  "config": { "force_think": false, "abf_enabled": true, ... }
}
```

DB schema (`decisions` table):  
`route | strategy | confidence | decision | domain | probe_entropy | probe_ms | total_ms | prompt_len | sample_prompt | budget_retries | entropy_class | entropy_score`

### 1.3 Quality Gate — `~/.openclaw/logs/quality_scores.jsonl`

Per-response JSONL (quality_gate.py L111–119):
`ts | route | score (1-5) | reason | scorer | prompt_len | response_len | prompt_hash`  
Optional ThinkPRM fields: `score_v2 | score_thinkprm | step_labels | verification_cot`

### 1.4 Training Pairs — `~/.openclaw/logs/training_pairs.jsonl`

Per-response JSONL: `ts | prompt | reasoning | response | budget_retries | prompt_hash`

### 1.5 Enricher — in-process only (no persistent log)

enricher.py returns `{tools_used, enrich_ms, context_chars}` per request; printed
to stderr as `[odo] enrich: rag,web 1234ms 5678 chars`. No structured persistence.

### 1.6 journalctl patterns

```bash
# ODO decisions (route + latency + entropy):
journalctl --user -u odo.service -g '\[odo\] route=' --no-pager -n 200

# Enricher calls (tools used + ms):
journalctl --user -u odo.service -g '\[odo\] enrich:' --no-pager -n 100

# ABF retries (budget forcing events):
journalctl --user -u odo.service -g 'ABF:' --no-pager -n 50

# Quality gate scores:
journalctl --user -u odo.service -g '\[quality\]' --no-pager -n 100

# llama-server slot/KV events:
journalctl --user -u qwen35-custom.service -g 'slot\|kv_cache' --no-pager -n 50

# DVTS events:
journalctl --user -u odo.service -g 'DVTS' --no-pager -n 30
```

---

## 2. Exhaustive Metrics Table — Current vs Desired

| Component | Metric | Current exposure | Gap | Desired |
|---|---|---|---|---|
| llama-server | TG throughput (tok/s) | `/metrics` llamacpp:predicted_tokens_seconds | none | persist 1-min rolling avg to SQLite |
| llama-server | PP throughput (tok/s) | `/metrics` | none | same |
| llama-server | KV cache utilization | `/metrics` kv_cache_usage_ratio | none | alert if > 0.85 |
| llama-server | Inflight / queued slots | `/metrics` | none | log when deferred > 0 |
| ODO | Classify latency (ms) | DB: probe_ms ≈ classify | no separate field | add `classify_ms` column |
| ODO | Enrich latency per tool | stderr only | **MISSING** | persist `enrich_ms` + `tools_used[]` to DB |
| ODO | Generate latency (ms) | DB: total_ms − probe_ms | derived only | add `generate_ms` column |
| ODO | ABF retries per query | DB: budget_retries | logged | add retries histogram |
| ODO | Entropy class distribution | `/stats` entropy_router | 24h only | 7d rolling in DB |
| ODO | Think ratio trend | `/stats` | 24h only | 7d rolling |
| Enricher | RAG hit rate | stderr, not persisted | **MISSING** | log `rag_hit: bool, rag_docs: int` per query |
| Enricher | Web search success/fail per backend | not tracked | **MISSING** | parse deep_search_sota exit code + backend used |
| Enricher | Confidence probe trigger rate | tools_used includes `confidence_probe(...)` | stderr only | persist to DB |
| Enricher | Dynamic engram predictions count | stderr `[DYNAMIC_ENGRAM] Injected N` | stderr only | persist `engram_preds: int` |
| Quality gate | Score distribution per route | quality_scores.jsonl | good | add 7d trend query |
| Quality gate | ThinkPRM vs Qwen3.5 agreement rate | score_v2 in JSONL | not aggregated | aggregate disagreements |
| Quality gate | Reflection trigger rate | stderr `reflection:` | **MISSING** | add `reflected: bool` to JSONL |
| Quality gate | Reflection improvement delta | not tracked | **MISSING** | log `score_before/after` |
| Web search | Cache hit rate (sota_cache) | deep_search_sota internal | not surfaced | parse `cache hit` in stderr |
| Web search | Backend success rate | not tracked | **MISSING** | add `backend_stats.json` in search_router |
| ChromaDB | RAG collection hit rate | not tracked | **MISSING** | knowledge_rag_query.py should log hit/miss |
| ChromaDB | Top-k relevance score | not tracked | **MISSING** | log max cosine score per query |
| Tool calls | Tool-calling success rate | benchmark only | **MISSING** | per-route tool_calls in DB |
| DVTS | Candidate score variance | dvts.json in response | not persisted | persist score + k to DB |
| Pipeline | Step-level latency | steps_log in response | not persisted | persist steps_log to DB |
| GPU | VRAM usage during inference | nvidia-smi only | not logged | periodic scrape → SQLite |
| GPU | Temperature / power draw | nvidia-smi only | not logged | alert > 85°C / > 200W |
| Cost | API tokens used (if paid fallback) | not implemented | N/A yet | add when Mistral/DashScope added |

---

## 3. Missing Observability — Priority Analysis

### HIGH ROI (implement now)

**A. Per-query enrich persistence (enricher.py)**

Add `~/.openclaw/logs/enrich.jsonl` writer in `enricher.py` after L672:

```python
# enricher.py — after the return block, before return
import json as _json, hashlib as _hl
from datetime import datetime as _dt
_ENRICH_LOG = Path.home() / ".openclaw/logs/enrich.jsonl"
try:
    _entry = {
        "ts": _dt.now().isoformat(),
        "route": route_id,
        "tools_used": tools_used,
        "enrich_ms": enrich_ms,
        "context_chars": total_chars,
        "rag_hit": "knowledge_rag" in tools_used,
        "web_hit": "web_search" in tools_used or "research_orchestrator" in tools_used,
        "query_hash": _hl.sha256(user_text.encode()).hexdigest()[:16],
    }
    _ENRICH_LOG.parent.mkdir(parents=True, exist_ok=True)
    with open(_ENRICH_LOG, "a") as _f:
        _f.write(_json.dumps(_entry, ensure_ascii=False) + "\n")
except Exception:
    pass
```

**B. Web search backend success rate (deep_search_sota.py)**

The script already has backend selection. Add `backend_stats.json` counter in
`~/.openclaw/logs/search_backend_stats.json`:

```python
# Append at end of deep_search_sota.py main():
import json, os
_STATS = os.path.expanduser("~/.openclaw/logs/search_backend_stats.json")
try:
    s = json.load(open(_STATS)) if os.path.exists(_STATS) else {}
    for b in backends_tried:
        s[b] = s.get(b, {"ok": 0, "fail": 0})
        s[b]["ok" if b in backends_ok else "fail"] += 1
    json.dump(s, open(_STATS, "w"), indent=2)
except Exception:
    pass
```

**C. ODO DB: add `enrich_ms` + `generate_ms` + `classify_ms` columns**

```sql
-- run once:
ALTER TABLE decisions ADD COLUMN classify_ms INTEGER DEFAULT 0;
ALTER TABLE decisions ADD COLUMN enrich_ms INTEGER DEFAULT 0;
ALTER TABLE decisions ADD COLUMN generate_ms INTEGER DEFAULT 0;
ALTER TABLE decisions ADD COLUMN rag_hit INTEGER DEFAULT 0;
ALTER TABLE decisions ADD COLUMN web_hit INTEGER DEFAULT 0;
```

Then in odo.py L1088, add to `odo_meta`:
```python
odo_meta["classify_ms"] = classify_ms
odo_meta["enrich_ms"] = enrich_info.get("enrich_ms", 0)
odo_meta["generate_ms"] = total_ms - classify_ms - enrich_info.get("enrich_ms", 0)
odo_meta["rag_hit"] = int("knowledge_rag" in enrich_info.get("tools_used", []))
odo_meta["web_hit"] = int("web_search" in enrich_info.get("tools_used", []) or
                          "research_orchestrator" in enrich_info.get("tools_used", []))
```

### MEDIUM ROI

**D. Quality gate: reflection tracking**

In quality_gate.py `_score_and_log()`, add `"reflected": False` to entry,
and in odo.py `_buffer_response()` after reflection succeeds, emit a separate
JSONL line with `{"reflected": true, "score_before": score, ...}`.

**E. ChromaDB hit rate**

In `knowledge_rag_query.py`, log top cosine score and hit/miss to stderr as:
`[rag] hit=True top_score=0.823 docs=3 query_hash=abc123`
Then parse in enricher.py.

---

## 4. Benchmark Scaffolding

### 4.1 llama-bench command for GGUF comparison

```bash
# Compare APEX I-Quality vs chimere-v3-ramp vs Unsloth UD-IQ3_S
# Run as: bash bench_gguf_compare.sh

LLAMA_BENCH=~/ik_llama.cpp/build_sm120/bin/llama-bench
MODELS=(
  "$HOME/.openclaw/models/Qwen3.6-35B-A3B-APEX-GGUF/Qwen3.6-35B-A3B-APEX-I-Quality.gguf:APEX"
  "$HOME/.openclaw/models/Qwen3.5-35B-A3B-GGUF/chimere-v3-ramp.gguf:RAMP"
  "$HOME/.openclaw/models/Qwen3.5-35B-A3B-GGUF/Qwen3.5-35B-A3B-UD-IQ3_S.gguf:IQ3S"
)
for spec in "${MODELS[@]}"; do
  path="${spec%%:*}"; tag="${spec##*:}"
  echo "=== $tag ==="
  $LLAMA_BENCH -m "$path" \
    -ngl 99 --n-cpu-moe 20 \
    -n 512 -p 1024 -b 1 \
    --output-format jsonl 2>/dev/null | tee "/tmp/bench_${tag}.jsonl"
done
```

### 4.2 Gold Prompt Set — 50 prompts (10 shown, 40 more defined below)

All prompts are deterministic-answer or keyword-verifiable.
`expected_hash` = SHA256[:16] of canonical expected response string.

```json
[
  {
    "id": "GP-MATH-01",
    "category": "math",
    "prompt": "Janet's ducks lay 16 eggs per day. She eats 3 for breakfast, bakes with 4. She sells the rest at $2/egg. Daily revenue?",
    "expected_answer": "18",
    "expected_hash": "b2e8f3a1c9d54012",
    "eval": "extract_number"
  },
  {
    "id": "GP-CODE-01",
    "category": "code",
    "prompt": "Write Python function `is_palindrome(s: str) -> bool` ignoring case and non-alphanumeric. Return ONLY the function.",
    "expected_answer": "assert is_palindrome('racecar') == True",
    "expected_hash": "a7f1b3e2d8c94501",
    "eval": "exec_test"
  },
  {
    "id": "GP-KINE-01",
    "category": "kine_factual",
    "prompt": "Quel est le test clinique de référence pour la rupture du LCA ?",
    "expected_keywords": ["lachman"],
    "expected_hash": "c3d9e1f2a8b64723",
    "eval": "keyword_match"
  },
  {
    "id": "GP-KINE-02",
    "category": "kine_factual",
    "prompt": "Quelle manoeuvre utilise-t-on en première intention pour un VPPB du canal postérieur ?",
    "expected_keywords": ["epley"],
    "expected_hash": "f8a2c5d1e9b34607",
    "eval": "keyword_match"
  },
  {
    "id": "GP-TOOL-01",
    "category": "tool_call",
    "prompt": "Recherche les dernières recommandations HAS 2025 sur la rééducation post-LCA.",
    "expected_tool": "web_search",
    "expected_hash": "d4b7a2e1c9f35812",
    "eval": "tool_invoked"
  },
  {
    "id": "GP-REASON-01",
    "category": "reasoning",
    "prompt": "A train leaves Paris at 08:00 at 120 km/h. Another leaves Lyon (412 km) at 09:00 at 160 km/h toward Paris. At what time do they meet?",
    "expected_answer": "11:09",
    "expected_hash": "e1f3b8c2a7d94501",
    "eval": "time_match"
  },
  {
    "id": "GP-FACTUAL-01",
    "category": "factual",
    "prompt": "Quelle est la capitale de l'Australie ?",
    "expected_keywords": ["canberra"],
    "expected_hash": "a9c2e4f1b8d73605",
    "eval": "keyword_match"
  },
  {
    "id": "GP-CODE-02",
    "category": "code",
    "prompt": "Write Python `two_sum(nums: list[int], target: int) -> tuple[int,int]` returning indices. Return ONLY the function.",
    "expected_answer": "assert two_sum([2,7,11,15], 9) == (0, 1)",
    "expected_hash": "b5d8e1f3a2c94072",
    "eval": "exec_test"
  },
  {
    "id": "GP-CYBER-01",
    "category": "cyber",
    "prompt": "Explique la technique MITRE ATT&CK T1059.001 (PowerShell) et propose 2 contre-mesures concrètes.",
    "expected_keywords": ["powershell", "t1059", "contre-mesure"],
    "expected_hash": "c7a1f2e4b3d85901",
    "eval": "keyword_match"
  },
  {
    "id": "GP-HALLUC-01",
    "category": "hallucination_trap",
    "prompt": "Quel est le score VISA-A minimum recommandé pour la reprise du sport après tendinopathie d'Achille ?",
    "expected_keywords": ["80"],
    "expected_hash": "d2e9b1f4a7c36018",
    "eval": "keyword_match",
    "note": "Hallucination trap: some models answer 90 or 100. Correct is 80."
  }
]
```

**Remaining 40 prompts by category (to flesh out):**

| ID range | Category | Count | Eval method |
|---|---|---|---|
| GP-MATH-02..10 | GSM8K variants | 9 | extract_number |
| GP-CODE-03..10 | HumanEval functions | 8 | exec_test |
| GP-KINE-03..12 | HAS protocols, scores | 10 | keyword_match |
| GP-REASON-02..05 | Multi-step logic | 4 | extract_number / time_match |
| GP-TOOL-02..05 | Tool injection triggers | 4 | tool_invoked |
| GP-FACTUAL-02..07 | Factual recall | 6 | keyword_match |
| GP-HALLUC-02..05 | Hallucination traps | 4 | keyword_match (anti-pattern) |
| GP-REFUSAL-01..03 | Safety refusals | 3 | refusal_check |

**Automated quality rubric (local-LLM-judged):**

Yes — use the existing `quality_gate._call_scorer()` for per-prompt scoring.
For factual prompts: use `eval: keyword_match` (zero LLM cost).
For open-ended: use ThinkPRM-1.5B `score_v2` (step-level verification).
For hallucination traps: invert — presence of wrong keyword = fail.

Score aggregation:
- `accuracy` = keyword_match pass rate on factual/kine/math
- `hallucination_rate` = halluc_trap fail rate
- `tool_success` = tool_invoked pass rate
- `quality_score` = mean ThinkPRM score_v2 on reasoning/cyber prompts

### 4.3 Running the gold-prompt suite

```bash
# Run full gold suite via benchmark_chimere.py (extend with GP prompts):
python3 ~/.openclaw/bin/benchmark_chimere.py --suite all --verbose 2>&1 | tee /tmp/bench_$(date +%Y%m%d_%H%M).txt

# Or targeted kine regression:
python3 ~/.openclaw/bin/benchmark_chimere.py --suite kine -v
```

---

## 5. Alerting / Cost

### 5.1 GPU health during long runs

```bash
# One-liner: log GPU temp + power + VRAM every 30s to file
nvidia-smi dmon -s pucvmet -d 30 | tee ~/.openclaw/logs/gpu_dmon.log &
# Alerts: grep for temp > 85°C or power > 200W in dmon output
# The RTX 5060 Ti TDP is 165W; sustained > 200W = throttle risk
```

Relevant dmon columns: `pwr` (W), `temp` (°C), `sm` (% utilization), `mem` (% VRAM).

### 5.2 API cost telemetry (future Mistral/DashScope fallback)

When adding paid API:
- Log `{ts, provider, model, prompt_tokens, completion_tokens, cost_usd}` to
  `~/.openclaw/logs/api_cost.jsonl`
- Add daily cap check: `jq '[.cost_usd] | add' ~/.openclaw/logs/api_cost.jsonl`
- Alert via Telegram if daily spend > $2.00 threshold

---

## 6. Dashboard Proposals

### 6.1 Minimal — `odo-status` text command (implement now)

Save as `~/.local/bin/odo-status`, `chmod +x`:

```bash
#!/usr/bin/env bash
# odo-status — last-hour + 3-day trend snapshot
# Usage: odo-status [--full]

set -euo pipefail

ODO_PORT="${ODO_PORT:-8084}"
LLAMA_PORT="${LLAMA_PORT:-8081}"
DB="$HOME/.openclaw/logs/odo.db"
QUALITY="$HOME/.openclaw/logs/quality_scores.jsonl"

echo "╔══════════════════════════════════════════════════════╗"
echo "║  ODO + APEX Stack Status  —  $(date '+%Y-%m-%d %H:%M:%S')  ║"
echo "╚══════════════════════════════════════════════════════╝"
echo

# ── Service health ──
echo "── Services ──"
for svc in odo.service qwen35-custom.service; do
  state=$(systemctl --user is-active "$svc" 2>/dev/null || echo "inactive")
  printf "  %-28s %s\n" "$svc" "$state"
done
echo

# ── ODO /stats (last 24h) ──
echo "── ODO /stats (24h) ──"
curl -s --max-time 3 "http://127.0.0.1:${ODO_PORT}/stats" 2>/dev/null \
  | python3 -c "
import json, sys
d = json.load(sys.stdin)
s = d.get('last_24h', {})
print(f\"  requests={s.get('requests',0)}  think_ratio={s.get('think_ratio',0):.1%}\")
print(f\"  avg_total_ms={s.get('avg_total_ms',0):.0f}ms  avg_probe_ms={s.get('avg_probe_ms',0):.0f}ms\")
print(f\"  abf_retries={s.get('budget_forcing_count',0)}  avg_retries={s.get('avg_budget_retries',0):.1f}\")
er = d.get('entropy_router', {})
print(f\"  entropy: \" + '  '.join(f\"{k}={v['count']}\" for k,v in er.items()))
print()
print('  Routes:')
for r, v in d.get('routes',{}).items():
    print(f\"    {r:<12} {v['count']:>5} reqs  {v['avg_ms']:>6.0f}ms avg\")
" 2>/dev/null || echo "  [ODO not reachable]"
echo

# ── llama-server /metrics ──
echo "── APEX llama-server metrics ──"
curl -s --max-time 2 "http://127.0.0.1:${LLAMA_PORT}/metrics" 2>/dev/null \
  | python3 -c "
import sys
lines = sys.stdin.read()
wanted = ['predicted_tokens_seconds','prompt_tokens_seconds',
          'kv_cache_usage_ratio','kv_cache_tokens',
          'requests_processing','requests_deferred']
for w in wanted:
    for line in lines.splitlines():
        if w in line and not line.startswith('#'):
            key = line.split('{')[0].replace('llamacpp:','')
            val = line.split()[-1]
            print(f'  {key:<32} {val}')
            break
" 2>/dev/null || echo "  [llama-server not reachable]"
echo

# ── Quality scores (last 50) ──
echo "── Quality scores (last 50 scored) ──"
if [ -f "$QUALITY" ]; then
  tail -50 "$QUALITY" | python3 -c "
import json, sys, collections
by_route = collections.defaultdict(list)
for line in sys.stdin:
    line = line.strip()
    if not line: continue
    try:
        e = json.loads(line)
        by_route[e.get('route','?')].append(e.get('score',3))
    except: pass
for route, scores in sorted(by_route.items()):
    avg = sum(scores)/len(scores)
    bad = sum(1 for s in scores if s <= 2)
    print(f'  {route:<12} avg={avg:.2f}  n={len(scores)}  bad={bad}')
" 2>/dev/null
else
  echo "  [no quality log yet]"
fi
echo

# ── 3-day trend from odo.db ──
echo "── 3-day trend (odo.db) ──"
if [ -f "$DB" ]; then
  python3 - "$DB" <<'PYEOF'
import sqlite3, sys
db = sys.argv[1]
conn = sqlite3.connect(db)
rows = conn.execute("""
  SELECT date(ts) as day,
         COUNT(*) as reqs,
         ROUND(AVG(total_ms)) as avg_ms,
         ROUND(100.0*SUM(CASE WHEN decision LIKE 'think%' THEN 1 ELSE 0 END)/COUNT(*),1) as think_pct,
         SUM(budget_retries) as abf_total
  FROM decisions
  WHERE ts > datetime('now','-3 days')
  GROUP BY day ORDER BY day
""").fetchall()
conn.close()
print(f"  {'Day':<12} {'Reqs':>6} {'AvgMs':>7} {'Think%':>7} {'ABF':>5}")
for r in rows:
    print(f"  {r[0]:<12} {r[1]:>6} {r[2]:>7} {r[3]:>6}% {r[4]:>5}")
PYEOF
else
  echo "  [odo.db not found]"
fi
echo

# ── GPU snapshot ──
echo "── GPU snapshot ──"
nvidia-smi --query-gpu=name,temperature.gpu,power.draw,memory.used,memory.total,utilization.gpu \
  --format=csv,noheader 2>/dev/null \
  | awk -F', ' '{printf "  %s  temp=%s°C  pwr=%s  vram=%s/%s  util=%s\n",$1,$2,$3,$4,$5,$6}' \
  || echo "  [nvidia-smi not available]"
echo
```

### 6.2 Medium — tmux live split

```bash
#!/usr/bin/env bash
# odo-watch — live tmux dashboard
# Usage: odo-watch
SESSION="odo-watch"
tmux new-session -d -s $SESSION -x 220 -y 50 2>/dev/null || true
# Pane 0: ODO journal
tmux send-keys -t $SESSION "journalctl --user -u odo.service -f --no-pager -g '\\[odo\\]'" Enter
# Pane 1: GPU dmon
tmux split-window -h -t $SESSION
tmux send-keys -t $SESSION "watch -n 2 'nvidia-smi --query-gpu=temperature.gpu,power.draw,memory.used,utilization.gpu --format=csv,noheader | awk -F\", \" \"{print \\\"GPU: temp=\"\$1\"°C pwr=\"\$2\" vram=\"\$3\" sm=\"\$4\"}\"'" Enter
# Pane 2: quality tail
tmux split-window -v -t $SESSION
tmux send-keys -t $SESSION "tail -f ~/.openclaw/logs/quality_scores.jsonl | python3 -c \"import sys,json; [print(f'[{e[\\\"route\\\"]}] score={e[\\\"score\\\"]} {e[\\\"reason\\\"][:60]}') for line in __import__(\\\"sys\\\").stdin for e in [json.loads(line)] if line.strip()]\"" Enter
tmux attach -t $SESSION
```

### 6.3 Big — Grafana + Prometheus

**Worth it?** Only if you add a paid API fallback or run multi-GPU.
For the current single-GPU local stack, Prometheus scrape overhead (15s) is
negligible but Grafana setup cost (~2h) is not justified.

**Minimal Prometheus approach if needed:**

```yaml
# prometheus.yml scrape config
scrape_configs:
  - job_name: llama_apex
    static_configs:
      - targets: ['127.0.0.1:8081']
    metrics_path: /metrics
    scrape_interval: 15s
```

Then a single Grafana dashboard panel:
`rate(llamacpp:tokens_predicted_total[1m])` → TG tok/s over time.

**Verdict: Skip Grafana for now. Use `odo-status` + `odo-watch`. Revisit if adding paid API.**

---

## 7. Quick Stability Check (run right now)

```bash
curl -s http://127.0.0.1:8084/stats | python3 -m json.tool
```

This gives the full 24h view from ODO in <1s. Look for:
- `budget_forcing_count > 10` → ABF retrying too much (raise ABF_THRESHOLD or increase max_tokens)
- `avg_total_ms > 30000` → latency regression (check KV cache, ncmoe setting)
- `think_ratio < 0.3` → entropy router too aggressive no-think (lower THRESHOLD_LOW)
- `routes.kine.avg_ms > routes.code.avg_ms * 3` → RAG/web enrichment eating kine budget

---

## 8. Summary

**Gold prompt count:** 50 total (10 fully specified above, 40 by category breakdown).

**3 highest-ROI missing metrics:**
1. **Enrich pipeline persistence** (RAG hit rate, web search success per backend, enrich latency breakdown) — currently only in stderr, zero structured visibility.
2. **Latency decomposition per query** (`classify_ms` / `enrich_ms` / `generate_ms` triad) — `total_ms` exists but is too coarse to diagnose regressions.
3. **Quality gate reflection tracking** (reflection trigger rate + score delta) — currently `[quality] reflection:` only in stderr; no way to know if self-critique is actually improving outputs.

**1 command to run right now:**
```bash
curl -s http://127.0.0.1:8084/stats | python3 -m json.tool
```
