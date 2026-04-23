# Tool-calling audit + plan — Qwen3.6 TQ3_4S + odo stack

**Date.** 2026-04-22. **Scope.** `qwen-tq3.service` (port 8083, turbo-tan/llama.cpp-tq3), `odo.service` (port 8084), pipelines under `~/.openclaw/odo/pipelines/`. **Authority.** PRINCIPLES rule 1 (file:line citations) and rule 12 (no "easy" without evidence).

## 1. Current tool-calling surface (what actually exists)

### 1.1 Tool *declarations* in pipelines (YAML)

| Pipeline | `tools_allowed` |
|---|---|
| `code.yaml:44-48` | `run_code, web_search, file_read, file_write` |
| `cyber.yaml:93-95` | `web_search, ioc_lookup` (also per-step: `cyber.yaml:35-37`) |
| `default.yaml:39` | `run_code, web_search, file_read, file_write, calculator, ioc_lookup` |
| `kine.yaml`, `research.yaml`, `kinebot-dev.yaml:91`, `kinebot-review.yaml` | subsets of the above |

### 1.2 Tool *definitions* actually registered — odo.py

- `TOOL_DEFINITIONS` dict at `odo.py:341-366` contains **only 2 entries**: `web_search` and `calculator`.
- `_build_tool_definitions` at `odo.py:379-381` silently drops every tool name not in the dict: `return [TOOL_DEFINITIONS[t] for t in tools_allowed if t in TOOL_DEFINITIONS]`.
- **Consequence.** `run_code`, `file_read`, `file_write`, `ioc_lookup` appear in YAMLs but are **never injected** into the OpenAI payload. They are dead strings.

### 1.3 Tool *trigger* gating — `_should_inject_tools`

- `odo.py:336-339` — `TOOL_TRIGGER_KEYWORDS` only keys on `web_search` (FR/EN search verbs) and `calculator` (IMC, pourcentage, …).
- Injection requires a keyword hit (`odo.py:369-376`). If the user query contains no trigger keyword, `tools` + `tool_choice` are not sent, even when `tools_allowed` is non-empty.

### 1.4 Tool *execution* layer — it does not exist

- Searched `odo.py`, `pipeline_executor.py`, `orchestrator.py` for any of `execute_tool`, `run_tool`, `tool_registry`, `function_call`. Only hits are payload-plumbing (`odo.py:746-749`) and `reasoning_content` stripping (`odo.py:1311-1328`).
- When the model emits `tool_calls`, odo relays them to the HTTP client. There is **no resolver**: the client must execute and loop. None of our clients (OpenClaw gateway, `aide`, Telegram) implement that loop for arbitrary tools today.
- `enricher.py` *does* run real scripts (`subprocess` at `enricher.py:16,64`) — `run_rag_search`, `run_web_search`, `run_cyberbro`, `run_csv_analysis`, `run_research` — but these are **pre-prompt context injection**, not post-response tool execution. The model sees results as user-side context, never chooses to call.

### 1.5 Qwen3.6 native tool format

- Served chat_template (queried `GET /props` at runtime) uses the explicit `<tool_call>\n<function=NAME>\n<parameter=…>` XML-ish block for emission (template offset 2956) and `<tool_response>` for replies (4314).
- llama.cpp's Jinja+grammar layer converts that to OpenAI `tool_calls[]` on output. Verified live (section 2 below): the server returns `tool_calls` in OpenAI format; raw `<tool_call>` tokens are absorbed.
- Template also supports `<think>...</think>` split (offset 5213), which is what `--reasoning-format deepseek` extracts into `reasoning_content`.

## 2. tau3-bench claim: `--reasoning-format deepseek` breaks tool calling — VERDICT: REFUTED on TQ3

Live probe against `qwen-tq3.service` (port 8083, service flags include `--reasoning-format deepseek` per `qwen-tq3.service:28`):

```
POST /v1/chat/completions  { "messages":[{"role":"user","content":"What is 17*23?"}],
  "tools":[calculate], "tool_choice":"auto" }
→ content: ''
  tool_calls: [{"function":{"name":"calculate","arguments":"{\"expression\":\"17*23\"}"}, "id":"..."}]
  reasoning_content: "The user wants to calculate 17 and 23. I will use the `calculate` tool..."
```

Tool call emitted correctly in OpenAI schema, arguments are valid JSON, reasoning cleanly split into `reasoning_content`. **The Apr-2 finding does not reproduce on the turbo-tan fork + Qwen3.6 template.** Likely explanation: Apr-2 was measured on Qwen3.5 + `ik_llama` where the combination of a different template and older `--reasoning-format` parser corrupted the closing `</tool_call>` tag. The 3.6 template is robust.

**Action.** Keep `--reasoning-format deepseek` as-is in `qwen-tq3.service:28`. Add a regression test (quick win 1 below) to catch any future break.

## 3. Missing features — evidence

| Feature | Status | Evidence |
|---|---|---|
| Think-tool (scratch-space tool) | absent | no match for `think.*tool`/`scratch` in `~/.openclaw/odo/` |
| JSON-schema structured output | server-capable, never used by odo | live probe accepts `response_format:{type:"json_schema",...}` and returns valid JSON; but `grep response_format odo.py` → 0 hits |
| Function registry (name → callable) | absent | no `TOOL_HANDLERS`/`execute_tool` in odo tree |
| MCP server | absent | `grep -r mcp /home/remondiere/.openclaw/odo/` → 0 hits |
| Parallel tool calls | server emits array, but odo single-slot (`qwen-tq3.service:22` `-np 1`) | n/a |
| Streaming tool calls | reasoning streamed (`odo.py:1140-1141,1241`), tool_calls not specifically handled | visual |

## 4. Hidden gaps (security + correctness)

- **`calculator`.** No implementation anywhere under `~/.openclaw/bin/` that actually evaluates `{expression}`. Trust-the-model-to-compute. Arithmetic at 3.07 BPW is not trustworthy — measured 17×23 call above returned the *intent* only; if the client doesn't execute, the model either hallucinates a result or stops. Actually tested — it stops (empty content, tool_call only).
- **`ioc_lookup`.** The underlying tool exists (`~/.openclaw/agents/cyber/tools/cyberbro_tool.py`, invoked from `enricher.py:121-129`) but is reachable only through enrichment auto-trigger, not through model-initiated tool calls. If the model emits `ioc_lookup(...)` OpenAI-style, nothing executes it.
- **`file_read` / `file_write`.** Declared in 5 pipelines. Zero sandbox code. If a downstream client ever does implement the loop naïvely, the model can read `~/.openclaw/.env` (line 1 of `MEMORY.md` index: `Secrets: ~/.openclaw/.env`) or overwrite `openclaw.json`. Currently non-exploitable only because no loop exists.
- **`run_code`.** Same story. `~/.openclaw/bin/sandbox_verify.py` and `code_runner.py` exist but are not wired to a model-initiated tool path.

## 5. Concrete plan

### 5.1 Quick wins (< 1 day each)

**QW1. Tool-calling regression test (30 min).** Prevents silent regressions if template or flags change.

```python
# ~/.openclaw/bin/tests/test_tool_calling_tq3.py
import json, requests, sys
r = requests.post("http://127.0.0.1:8083/v1/chat/completions", json={
    "messages":[{"role":"user","content":"What is 17*23?"}],
    "tools":[{"type":"function","function":{"name":"calculate",
        "description":"Math","parameters":{"type":"object",
        "properties":{"expression":{"type":"string"}},"required":["expression"]}}}],
    "tool_choice":"auto","max_tokens":512,"temperature":0.3}, timeout=60)
m = r.json()["choices"][0]["message"]
assert m.get("tool_calls"), f"no tool_calls in {m}"
args = json.loads(m["tool_calls"][0]["function"]["arguments"])
assert "17" in args["expression"] and "23" in args["expression"]
print("OK")
```
Hook into a systemd `qwen-tq3-healthcheck.timer` or just CI on push.

**QW2. Implement a real `calculator` + register `run_code`, `file_read`, `ioc_lookup` definitions (2 h).** Stops the dead-string problem and adds a sandboxed executor. Edit `odo.py:341-366` to extend `TOOL_DEFINITIONS` and add a `TOOL_HANDLERS` dict:

```python
# odo.py, near TOOL_DEFINITIONS (~ line 341)
import ast, operator as op, pathlib
_SAFE_OPS = {ast.Add:op.add, ast.Sub:op.sub, ast.Mult:op.mul, ast.Div:op.truediv,
             ast.Pow:op.pow, ast.Mod:op.mod, ast.USub:op.neg, ast.UAdd:op.pos,
             ast.FloorDiv:op.floordiv}
def _safe_eval(node):
    if isinstance(node, ast.Constant) and isinstance(node.value,(int,float)): return node.value
    if isinstance(node, ast.BinOp):   return _SAFE_OPS[type(node.op)](_safe_eval(node.left), _safe_eval(node.right))
    if isinstance(node, ast.UnaryOp): return _SAFE_OPS[type(node.op)](_safe_eval(node.operand))
    raise ValueError(f"unsafe node {type(node).__name__}")

_SANDBOX_ROOT = pathlib.Path.home() / ".openclaw/sandbox"
_SANDBOX_ROOT.mkdir(exist_ok=True)
def _safe_path(p):
    p = (_SANDBOX_ROOT / p).resolve()
    if _SANDBOX_ROOT not in p.parents and p != _SANDBOX_ROOT:
        raise ValueError("path escape")
    return p

TOOL_HANDLERS = {
  "calculate": lambda args: {"result": _safe_eval(ast.parse(args["expression"], mode="eval").body)},
  "file_read": lambda args: {"content": _safe_path(args["path"]).read_text()[:8000]},
  "file_write": lambda args: (_safe_path(args["path"]).write_text(args["content"][:32000]), {"ok":True})[1],
  # run_code delegated to sandbox_verify.py (already exists in ~/.openclaw/bin/)
  # ioc_lookup delegated to cyberbro_tool (already wired in enricher.py:121)
}
```

Add the missing definitions (run_code, file_read, file_write, ioc_lookup) to `TOOL_DEFINITIONS` mirroring the OpenAI schema. Keep the sandbox root outside `~/.openclaw/` — files and secrets are protected by prefix check.

**QW3. JSON-schema enforcement for extraction pipelines (1 h).** Server supports it (verified live). Add optional `response_schema:` key to pipeline YAML and plumb through:

```python
# odo.py, inside apply_pipeline (~ line 420, next to grammar handling)
schema = pipeline.get("response_schema")
if schema:
    result["response_format"] = {"type": "json_schema", "json_schema": {"schema": schema}}
```

Use first in `cyber.yaml` (triage step outputs structured IOC list) and `research.yaml` (citation extraction). Immediate win: zero malformed-JSON parsing downstream.

### 5.2 Medium (1–5 days)

**M1. Tool-execution loop in odo (2 d).** Non-streaming path first. When the model returns `tool_calls`, resolve via `TOOL_HANDLERS`, append `{role:"tool", tool_call_id, content}` to messages, re-POST, loop ≤ 4 turns. Gate per-pipeline (`pipeline["execute_tools"]: true`). Guards: timeout per tool, total budget, deny-list of tool names per route (cyber cannot `file_write`, etc.).

**M2. Structured-prompt wrapper ("Pre-Act" pattern) (1 d).** MEMORY.md notes "+22 %". Prepend, when tools present, a fixed system fragment forcing the model to emit `<plan>...</plan>` before the tool call. Template-only, no training.

**M3. MCP server façade (3 d).** Expose odo tools via the stdio MCP protocol so Claude Code and other MCP clients can reuse them. Minimal: Python `mcp` package wrapping the `TOOL_HANDLERS` registry from QW2. Port 8085 (reserved — unused in MEMORY.md port table).

**M4. Think-tool (2 d).** Register a no-op tool `think(thought: string)` that just echoes back. Forces the model to externalise reasoning as a structured call instead of free text. Paper result: +54 % on τ-bench (MEMORY.md). Template support confirmed — Qwen3.6 already emits `<think>` via `reasoning_format deepseek`, but an explicit *tool* gives the model a discrete action and lets us log/inspect thoughts separately from the final message.

### 5.3 Big (> 1 week)

**B1. RC-GRPO / DPO on tool-use traces (3 w, GPU-night).** Use existing `grpo_nightly.py` scaffold. Reward: `tool_call_valid_json ∧ tool_args_pass_schema ∧ final_answer_correct`. Dataset source: replay Chimere prod logs plus τ3-bench + ToolBench public sets. Target: raise TQ3 τ3-retail score from ≈20 % to ≥ 60 %.

**B2. Training-free: EvoPress / ParoQuant re-evaluation for tool layers (1 w).** Keep experts at TQ3 but bump attention + first-block MoE gate to Q5. Rationale: tool dispatch depends on attention precision (argument copying), which TQ3_4S attenuates (4-bit attn per `chimere_tq3_migration.md:5`). Budget: +1 GB VRAM, already available (6 GB free post-TQ3).

**B3. Proper observability (1 w).** Per-tool success rate, per-route tool-call latency, argument-validation failure log. Feeds B1 reward model.

## 6. Highest-ROI ordering

1. QW2 (dead-string fix + sandboxed exec) — unblocks every other item.
2. QW3 (JSON-schema) — immediate quality gain on cyber + research.
3. M1 (execution loop) — turns decorative `tools_allowed` into real capability.
4. M4 (think tool) — largest published gain (+54 %).
5. B1 (RC-GRPO) — only after 1–4 produce training data.

## 7. Risks

- QW2 sandbox: symlink-escape. Mitigation: `.resolve()` + parents check shown above; add `O_NOFOLLOW` if porting to `os.open`.
- M1 loop divergence: hard cap 4 iterations; return partial content on overflow.
- M3 MCP: duplicate attack surface. Bind to loopback only (mirror gateway 25443 policy from MEMORY.md).

## 8. File:line reference index

- `~/.openclaw/odo/odo.py:336-339` — TOOL_TRIGGER_KEYWORDS
- `~/.openclaw/odo/odo.py:341-366` — TOOL_DEFINITIONS (only 2 tools)
- `~/.openclaw/odo/odo.py:369-381` — trigger + build helpers
- `~/.openclaw/odo/odo.py:420-422` — grammar plumbing (template for QW3)
- `~/.openclaw/odo/odo.py:740-749` — tools injection site
- `~/.openclaw/odo/enricher.py:16,64,78,102,121,134` — pre-prompt enrichment tools (not model-callable)
- `~/.openclaw/odo/pipelines/{code,cyber,default,kine,kinebot-dev,kinebot-review,research}.yaml` — `tools_allowed` declarations
- `~/.config/systemd/user/qwen-tq3.service:22,28` — `-np 1`, `--reasoning-format deepseek`
- `~/.openclaw/models/Qwen3.6-35B-A3B-TQ3_4S/` chat_template (via `/props`) — offsets 2709 (`<tools>`), 2956 (`<tool_call>`), 4314 (`<tool_response>`), 5213 (`<think>`), 5793 (`tool_calls` assistant rendering)
- `~/.openclaw/bin/sandbox_verify.py`, `code_runner.py` — existing sandboxed runners, unwired
- `~/.openclaw/agents/cyber/tools/cyberbro_tool.py` — real IOC tool, wired only via enricher
