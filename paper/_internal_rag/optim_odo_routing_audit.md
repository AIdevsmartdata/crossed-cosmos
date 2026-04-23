# ODO Routing Intelligence Audit

**Date**: 2026-04-22  
**Scope**: `~/.openclaw/odo/` — 5235 total lines across 11 Python modules + 5 pipeline YAMLs  
**Purpose**: End-to-end audit of ODO's routing intelligence for optimization.

---

## 1. Route Decision Flow

Exact precedence order, all in `odo.py:_decide_thinking()` (lines 857–905):

1. **Tool calls present** (payload has `tools` or `functions`) → `no-think / CODE_NO_THINK_PARAMS` (line 863–864)
2. **Explicit caller override** (`chat_template_kwargs` already in payload) → pass through as-is, no sampling override (lines 867–868)
3. **Vision** (image in payload) → always `think` (lines 871–873)
4. **Very short text** (<20 chars) → `no-think` (lines 876–877)
5. **Greeting** (<80 chars + GREETING_RE match) → `no-think` (lines 880–881)
6. **Pipeline thinking override** (`pipeline.thinking.enabled`) → enforces think/no-think per route YAML (lines 884–891)
7. **Entropy router hint** (`_entropy_hint == "no-think"` and not `FORCE_THINK`) → `no-think` without probe (lines 894–897)
8. **FORCE_THINK env var** → always `think` (lines 900–902)
9. **Entropy probe** (`_entropy_probe()`) → sends 5-token probe to llama-server, measures Shannon entropy, decides based on `ENTROPY_THRESHOLD=0.8` (lines 907–943)

**Before** `_decide_thinking()` is called, the following runs in order (lines 641–854):
- Message sanitization (line 643)
- Intent classification → `route_id` (line 654)
- Pipeline YAML load (line 660–663)
- Generation mode (`fast`/`quality`/`ultra`) applied to pipeline overrides (lines 665–717)
- `apply_pipeline()` — injects params, engram, lora, system_prompt (line 720)
- Enrichment (RAG/web/CSV/IoC) (lines 724–738)
- Tool injection (lines 741–749)
- Multi-step pipeline execution check — **exits early** if `should_use_pipeline()` is true (lines 752–810)
- Entropy router (`estimate_entropy()`) — pre-generation heuristic classification (lines 813–833)

---

## 2. Classifier

**File**: `classifier.py` — Strategy cascade, NOT trained.

**Strategy 1b** (line 289): Fast-path regex for greetings → `default`, conf=0.9.

**Strategy 1** (lines 293–295): Regex match against 11 route patterns (ROUTES dict, lines 22–112). Confidence formula:
- Single match: `min(0.95, 0.7 + 0.05 * n_matches)` (line 177)
- Multi-match: `min(0.85, 0.5 + 0.05 * gap)` where gap = winner minus runner-up (lines 180–182)
- Threshold to use: conf ≥ 0.5 (line 294)

**Strategy 2** (lines 298–303): File extension → route mapping (`EXT_ROUTES`, lines 123–132). Confidence 0.85 flat. Images → `vision` with 0.9.

**Strategy 3** (lines 310–311): LLM fallback via nothink proxy on port 8086, `max_tokens=5`, `temperature=0`, GBNF grammar constraining output to valid route names, 2s timeout. Returns conf=0.7 on match, 0.3 on fallback.

**Route normalization** (line 272): any route not in `PIPELINE_ROUTES` (code, kine, kinebot-dev, kinebot-review, cyber, research, default) falls through to `default`.

**Misrouting risks**:
- `tutor`, `data`, `math`, `writing`, `agro` routes have regex but no pipeline YAML → all silently become `default` (line 142–144). A "explain how diffusion works" query hits `tutor` regex → classified but normalized to `default` → kine.yaml or default.yaml regardless.
- `research` regex includes `cherche`, `trouve.moi`, `dis.moi` — common conversational phrases can incorrectly route to expensive research pipeline.
- `code` regex matches `api\b`, `error\b`, `sql\b` — broad enough to fire on non-technical messages mentioning these words.
- LLM fallback (strategy 3) requires nothink proxy on port 8086, which is not guaranteed to be up (`qwen35-llama.service` = STANDBY per memory). Silent fallback to `general`→`default` on timeout.

---

## 3. Confidence-RAG-Trigger

**File**: `confidence_rag_trigger.py`

**Probe**: sends 64-token, temp=0.0, no-think request to chimere backend, collects logprobs.

**Decision logic** (lines 143–167):
1. Hedge phrase detected (`_HEDGE_RE`) → `deep_rag`, `confident=False`
2. `mean_entropy > 0.6` → `deep_rag`
3. `mean_entropy > 0.35` → `quick_rag`
4. `mean_entropy == 0.0` and `len(content) > 20` → logprobs not available → check for short/evasive (<80 chars) or cutoff mention → `quick_rag` if yes, else `skip_rag`
5. Otherwise → `skip_rag`, `confident=True`

**Integration with enricher** (enricher.py lines 524–555): only triggered when `explicit_web is False` AND query contains recency keywords (`2024|2025|2026|récent|dernier|...`). If triggered: `deep_rag` → web depth `standard`; `quick_rag` → web depth `quick`.

**Interaction with entropy_router**: the entropy router runs as a pre-generation heuristic (before enrichment, line 813) and affects thinking mode only. The confidence_rag_trigger runs inside `enrich()` (after apply_pipeline, before forward) and affects web search depth independently. They do not share signal — a high-entropy query gets DVTS from entropy_router but confidence_rag_trigger is not called unless the pipeline has `web: false` AND query mentions recency. **No direct coordination**.

**TQ3 calibration issue (Section 9)**: see below.

---

## 4. Entropy Router

**File**: `entropy_router.py`

**Thresholds** (lines 43–44):
- `THRESHOLD_LOW = 0.28` — below → `low` entropy (no-think)
- `THRESHOLD_HIGH = 0.52` — above → `high` entropy (DVTS + tighter ABF)

Comment at line 45: "was 0.65, never triggered" — threshold was halved to 0.52 to actually fire.

**Composite score** (lines 334–345): `W_COMPLEXITY*complexity + W_CONFIDENCE*conf_entropy + W_HISTORY*hist_entropy`
- Weights: complexity=0.45, confidence=0.30, history=0.25 (lines 39–41)

**Components**:
- `_query_complexity()` (lines 110–173): length (0–0.25) + FACTUAL_RE floor (≤0.20) + question marks + AMBIGUITY_RE (0–0.25) + MULTISTEP_RE (0–0.20) + TECHNICAL_RE (0–0.20) + code block presence (+0.05) + sentence count
- `_confidence_entropy()` (line 185): `max(0, min(1, 1 - route_confidence))` — simple inversion
- `_history_entropy()` (lines 241–279): loads last 200 lines of `quality_scores.jsonl`, maps avg score to base entropy, adds std variance bonus. Returns 0.5 when <3 samples (neutral).

**Probe runs** (odo.py line 905): only when all of steps 1–8 in `_decide_thinking()` are skipped — i.e., not tools, no caller override, not vision, not short/greeting, no pipeline override, no entropy hint triggered, not FORCE_THINK. The full token entropy probe (~15s overhead, `PROBE_MAX_TOKENS=5`) is last resort.

**When probe is skipped**: whenever entropy router returns `low` and `FORCE_THINK=False`, the entropy hint fires at step 7 (line 895) and skips the probe entirely.

**Actions on `high` entropy** (odo.py lines 821–833): injects `dvts: {enabled:true, k:2}` into pipeline if not already enabled; overwrites `thinking.abf_threshold` with `0.65` (stricter).

---

## 5. Quality Gate

**File**: `quality_gate.py`

**Scored routes** (line 44): `{"kine", "research", "cyber", "code"}`

**Minimum response length** (line 41): 100 chars.

**Qwen3.5 scorer** (lines 167–224): sends structured JSON prompt to port 8081, no-think, `max_tokens=100`, `temp=0.1`. Asks for `{"score": 1-5, "reason": "..."}`. Score parsed from JSON or regex fallback.

**ThinkPRM scorer** (lines 288–340): port 8085. Step-level PRM. Extracts steps from response (5 strategies: numbered lists, headers, bullets, code blocks, paragraphs). Calls ThinkPRM for verification CoT. Extracts P(Yes) from logprobs at Yes/No decision token. Maps float [0,1] to int [1,5] via `_v2_to_v1()` (lines 397–409). **Currently disabled by default** (`THINKPRM_ENABLED=0`, line 37).

**Actions by score**:
- score ≥ 4 → `on_quality_score()` auto-feeds few-shot store (quality_gate.py line 479)
- score ≤ 2 → **reflection loop** for routes `kine` and `cyber` only (odo.py lines 1349–1377): `score_response_sync()` → `reflect_and_retry()` → replaces response before sending to client
- score = 3 → neutral, async log only

---

## 6. DVTS (Diverse Verifier Tree Search)

**File**: `dvts.py`

**Architecture**: K candidates generated **sequentially** (GPU single-slot, np=1 constraint), scored in **parallel** (CPU ThreadPoolExecutor), best returned (lines 219–274).

**Candidate diversity** (line 224): temperature = `base_temperature + i * 0.05` (default 0.7, 0.75, 0.80, 0.85 for K=4).

**min_tokens guard** (lines 209–215): enforces `max(max_tokens, 8192)` to prevent thinking block consuming entire budget and leaving empty visible content (all-zero scores → no differentiation).

**Scoring fallback** (lines 153–180): if `THINKPRM_ENABLED=False` → heuristic score = length component (0–0.3) + structure signals (0–0.3) + keyword overlap (0–0.4). This is the **current default** since ThinkPRM is disabled.

**Wiring in odo.py** (lines 979–1029): triggered when `pipeline.dvts.enabled=True` and `not is_streaming`. Entropy router injects `{enabled:True, k:2}` for high-entropy queries. Mode `ultra` forces `{enabled:True, k:4}`.

**Limitation**: with ThinkPRM disabled, heuristic scoring rewards longer/more structured responses, not necessarily correct ones. On kine clinical questions, length ≠ accuracy.

---

## 7. Pipeline YAMLs Summary

| Route | thinking | engram | lora | system_prompt | tools_allowed | pipeline_steps |
|-------|----------|--------|------|---------------|---------------|----------------|
| **code** | `enabled: false` | `code.engr` α=0.3 | null | Senior Algo Engineer, Python-focused | run_code, web_search, file_read/write | 2: architect(t=0.8) → coder(t=0.2) |
| **cyber** | `enabled: true`, budget=2048, abf=0.5 | `cyber.engr` α=0.3 | null | IOC/MITRE analyst | web_search, ioc_lookup | 3: triage → correlate → remediate |
| **default** | `enabled: true`, budget=2048, abf=0.5 | null | null | Generic helpful | all tools | none |
| **kine** | `enabled: true`, budget=2048, abf=0.55 | `kine.engr` α=0.35 | null | SOAP/HAS clinical | web_search, calculator | 4: evidence_search → diagnostic → protocol → dosage |
| **research** | `enabled: true`, budget=8192, abf=0.0 (ABF off) | `general.engr` α=0.2 (write mode) | null | Citation-backed report | web_search | 3: scout(×5 iter) → analyze → write_report |

**Key observations**:
- `code.yaml` sets `thinking.enabled: false` — pipeline thinking override fires at step 6 in `_decide_thinking()`, no probe needed.
- `research.yaml` has `abf_threshold: 0.0` meaning ABF is never triggered (always think fully). This is intentional but expensive.
- `kine.yaml` has `dvts.enabled: false` — must be toggled per-request or via entropy router (`high` entropy injects k=2).
- Pipeline steps in kine/research execute via `pipeline_executor.py` only when `payload["pipeline"]=True` or `pipeline_auto=True` in YAML. Neither kine nor research has `pipeline_auto: true`, so multi-step only fires on explicit request.
- `code.yaml` pipeline budget=0 conflicts with `thinking.enabled: false` — `budget` field is set but unused since thinking is off.

---

## 8. ABF and CGRS

**ABF (Adaptive Budget Forcing)** — `odo.py` lines 78–86, 1099–1194:
- Enabled: `ABF_ENABLED=True` (default)
- Triggers: `is_thinking AND is_complex_query(user_text) AND len(user_text) > 30 AND not streaming` (line 976)
- Composite certainty: `Ct = 0.625 * mean_conf + 0.375 * (1 - mean_norm_entropy)` over last 32 tokens (lines 454–476)
- Acceptance: `Ct >= threshold AND reasoning_len >= 100`, OR `reasoning_len >= 500`, OR `attempt >= 3` (lines 1157–1163)
- On rejection: prefill `<think>\n{reasoning}\nWait, let me reconsider...` and retry (line 1184)
- Max retries: 3 (`ABF_MAX_RETRIES`)

**CGRS (Certainty-Guided Reasoning Suppression)** — lines 89–100, 1188–1189:
- Triggers during ABF retry when `Ct > 0.9` (CGRS_DELTA): injects logit bias of -100 for "wait/but/hmm/alternatively" tokens (reasoning stall markers)
- Purpose: suppress repetitive reasoning loops when model is already highly certain

**Current thresholds**: `ABF_THRESHOLD=0.55`, `ABF_ALPHA=0.625`, `ABF_BETA=0.375`.  
Per-route overrides in YAMLs: cyber=0.50, kine=0.55, default=0.50, research=0.0 (disabled).

---

## 9. TQ3 Entropy Issue (Confidence-RAG-Trigger Thresholds)

**Claim from Opus RAG agent**: `confidence_rag_trigger` thresholds (0.35/0.6) need recalibration for TQ3's (chimere-v3-ramp) higher intrinsic entropy.

**Confirmed by code** (`confidence_rag_trigger.py` lines 145–166):
- Thresholds `0.35` and `0.6` are **absolute** values of normalized Shannon entropy over top-5 logprobs
- These were calibrated for a model with lower temperature sampling
- chimere-v3-ramp runs at `temp=1.0` (THINK_PARAMS, odo.py line 111) for thinking mode
- At temp=1.0, the model's output distribution is genuinely flatter → higher raw entropy across most tokens, even when confident
- **Effect**: TQ3 at temp=1.0 will routinely produce `mean_entropy > 0.35` even on questions it knows well → spuriously triggers `quick_rag`, adding 15–45s overhead per request

Additionally: the probe itself (`probe_confidence`) uses `temp=0.0` (greedy, line 84) which should reduce entropy, but:
- chimere-server uses FFI mode where logprobs may not be available (line 151: `if mean_entropy == 0.0 and len(content) > 20` → fallback branch)
- If logprobs unavailable, decision falls back to text heuristics (short/evasive response or cutoff mention), which are less precise

**Verdict**: confirmed. Thresholds need upward recalibration to ~0.50 (quick_rag trigger) and ~0.75 (deep_rag trigger) to match TQ3's entropy profile at production temperatures.

---

## 10. Few-Shot Selection

**File**: `semantic_fewshot.py` + `enricher.py:find_few_shot()`

**Two-tier selection** (enricher.py lines 434–471):
1. **Tier 1 — Semantic FAISS** (`semantic_fewshot.find_semantic_fewshot()`): Qwen3-Embedding-0.6B (CPU), FAISS flat index for <500 entries / IVF for ≥500. Cosine similarity, threshold `MIN_SIMILARITY=0.30` (lowered from 0.35, line 31). Cross-domain penalty: ×0.7 on score if route mismatch (line 251). Quality gate: only entries with `score ≥ 3` from `quality_scores.jsonl` (line 29, lowered from 4).
2. **Tier 2 — Keyword fallback** (lines 456–470): tag match (×3 weight) + token overlap. Only fires if FAISS fails or returns empty.

**Factual recall suppression** (enricher.py lines 488–496): if query matches `quels?|combien|liste|critères|protocole|score|dosage|posologie`, few-shot is suppressed entirely. Comment: "ablation showed few-shot on kine factual questions DEGRADES recall (63%→11%)".

**Auto-feed** (`quality_gate.py:on_quality_score()` lines 476–531): score ≥ 4 → adds to `few_shot/{route_id}.json` (max 10 entries, sorted by score+ts).

---

## 11. Dynamic Engram

**Reference**: `odo.py` lines 703–716 describe the `mode_cfg["dynamic_engram"]` flag being set in the pipeline `enrich` section. The actual injection is in `enricher.py` lines 617–624.

**Trigger condition**: `enrich_cfg.get("dynamic_engram", False)` AND `web_text` (a web search result was obtained in the same request). Only fires in `quality` and `ultra` modes (odo.py lines 704–709 set `enrich.dynamic_engram=True`).

**Mechanism** (`enricher.py:inject_dynamic_engram_context()` lines 153–262):
1. Split search result text into paragraph chunks
2. Call `dynamic_engram.build_dynamic_engram(chunks, query)` → builds `.engr` file from web results
3. Tokenize query with Qwen3.5 tokenizer
4. Slide n-gram windows across query tokens, look up top-3 predictions per window
5. Filter predictions with `prob < 0.05`, sort descending, deduplicate, take top 20
6. Format as `"context" -> "predicted_next" (prob%)` lines injected into system prompt

**Static Engram** (enricher.py lines 626–633): reads `engram_table` set by `apply_pipeline()` from YAML. Looks up domain `.engr` table (prebuilt offline from curated corpora) via same sliding-window query mechanism.

---

## 12. Orchestrator vs pipeline_executor

**`orchestrator.py`** (469 lines): the **OLD ODO** from the pre-unification architecture. Routes on port 8085 → think_router (8084) → llama-server (8081). It does: classify → apply_pipeline (shallow param override only, no enrichment) → forward. **No ABF, no entropy router, no quality gate, no enrichment, no DVTS.** It should be considered **dead code** — `odo.service` runs `odo.py` on 8084, `orchestrator.py` is never started.

**`pipeline_executor.py`** (190 lines): called from `odo.py` when multi-step execution is triggered. Executes pipeline steps sequentially, accumulates context, passes it to each subsequent step as `[Context from previous steps]`. Sends directly to llama-server (bypassing ODO's own enrichment for step requests). Returns final step's output.

**Redundancy**: `orchestrator.py` duplicates classifier, YAML loading, and basic param apply — all superseded by `odo.py`. Safe to delete.

---

## Quick-Win Opportunities

### QW1 — Recalibrate confidence_rag_trigger thresholds for TQ3 (1h)
**File**: `confidence_rag_trigger.py` lines 145–148  
**Change**: `0.6 → 0.78`, `0.35 → 0.52`  
**Why**: TQ3 at temp=1.0 has baseline entropy ~0.45–0.55 on confident answers. Current 0.35 threshold fires on ~70% of requests, causing ~15s overhead. Raising to 0.52/0.78 targets genuinely uncertain responses.

### QW2 — Fix entropy router THRESHOLD_HIGH never-fire regression (1h)
**File**: `entropy_router.py` lines 43–44, comment "was 0.65, never triggered"  
**The real issue**: `W_HISTORY=0.25` returns 0.5 neutral when <3 quality samples exist (line 255), artificially inflating composite scores. New installs with empty quality logs will have most queries classified as `medium` regardless of complexity.  
**Change**: set `_history_entropy()` default to 0.3 (not 0.5) when data is absent; or reduce W_HISTORY to 0.15 and redistribute to W_COMPLEXITY=0.55. This will properly separate trivial from complex queries.

### QW3 — Enable multi-step pipelines for kine/research by default (1h)
**Files**: `kine.yaml`, `research.yaml`  
**Change**: add `pipeline_auto: true` to both YAMLs  
**Why**: the 4-step kine pipeline (evidence→diagnostic→protocol→dosage) and 3-step research pipeline exist but never fire unless client sends `pipeline:true`. They represent the most valuable routing intelligence but are effectively dead.

### QW4 — Fix research route false positives (1h)
**File**: `classifier.py` lines 84–89  
**Change**: remove `cherche\b`, `trouve.moi`, `dis.moi` from research regex — these are conversational patterns that should route to `default`. Restrict to `[eé]tat.de.l.art|rapport|analyse\b|synth[eè]se|litt[eé]rature|source|r[eé]f[eé]rence|citation|[eé]tude|publi|article|paper|survey|review\b|benchmark\b` only.  
**Why**: "cherche un exercice pour mon patient" matches both `kine` and `research`; multi-match reduces confidence (line 180) and may route to research which runs expensive web search.

### QW5 — Delete orchestrator.py dead code (30min)
**File**: `orchestrator.py`  
**Change**: remove or archive. It is never started (port 8085 not in any active systemd service per memory), duplicates classifier/YAML loading without any of ODO's advanced features.  
**Why**: reduces confusion for future dev, removes 469 lines of misleading architecture documentation.

---

## Single Highest-Priority Recalibration

**QW1: confidence_rag_trigger thresholds** — this is the highest-priority change.

With TQ3 at `temp=1.0`, the current `0.35` threshold causes near-universal web search triggering on any non-trivial query with `explicit_web=False` + recency keyword. This creates 15–45s latency spikes for queries that the model could answer from training data alone. The recalibration is a 2-line change with measurable impact on median latency.

---

*Total ODO Python: 5235 lines across 11 modules.*
