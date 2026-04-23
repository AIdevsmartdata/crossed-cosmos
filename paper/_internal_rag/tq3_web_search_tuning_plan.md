# TQ3 / 64K-Context Web-Search Tuning Plan

Target: Qwen3.6 TQ3_4S (`qwen-tq3.service`, `-c 65536`). Pipeline entry points:
- `/home/remondiere/.openclaw/bin/deep_search_sota.py` (843 lines)
- `/home/remondiere/.openclaw/odo/enricher.py` (675 lines)
- `/home/remondiere/.openclaw/bin/web_deep_fetch.py` (438 lines)

All behavioural claims below cite file:line. All tuning edits are classified
**SAFE** (apply now, pure widening of caps within existing sampling budget) or
**GATED** (apply only once TQ3 benchmark passes: synthesis quality ≥ Apex on 10
sample queries, E2E latency stays within +20% of current).

---

## 1. Audit of implicit context caps

Caps along the web-search → synthesis path, leaf → root:

| # | Cap | File:line | Value | TQ3 implication |
|---|---|---|---|---|
| C1 | Per-chunk truncation in LLM synthesis | `deep_search_sota.py:533-544` | `chunks[:12]`, title `[:80]`, text `[:600]` | **Main bottleneck.** 12*600 = 7.2k chars ≈ 2.4k tok of context. 64K ctx is 99% empty. |
| C2 | Cross-encoder input truncation | `deep_search_sota.py:447` | `text[:4000]` per pair | OK (gte-reranker max 8192 tokens ≈ 32k chars, could widen). |
| C3 | Chunk text fallback when `deep_fetch` fails | `deep_search_sota.py:483` | `[:1000]` | Minor. |
| C4 | Deep-fetch per-page chunk count | `web_deep_fetch.py:42` | `MAX_CHUNKS_PER_PAGE = 10` | Soft; `chunk_text` also hard-caps `[:MAX_CHUNKS_PER_PAGE*3]` at l.229. |
| C5 | Chunk token size | `web_deep_fetch.py:43-44` | 512 tok, 50 overlap | Fine; do not change without retrieval re-tune. |
| C6 | `run_web_search` output cap (quick path) | `enricher.py:108` | `max_chars=6000` | **Critical boundary cap** between web search and chimere-server prompt for route `quick`. |
| C7 | `run_research` output cap (standard+deep path) | `enricher.py:143` | `max_chars=12000` | Matters; 12 KB ≈ 3 KTok — still tiny vs 64K. |
| C8 | `run_rag_search` output cap | `enricher.py:91` | `[:6000]` | RAG-side; not on the web path but contributes to enricher context. |
| C9 | Generic `_run_script` default | `enricher.py:61` | `max_chars=8000` | Default for ad-hoc tools. |
| C10 | DEPTH_CONFIG `top_chunks` | `deep_search_sota.py:50-52` | 8/12/16 (post Apex tune) | Fed into `fetch_and_rerank` → cross-encoder top-k. |
| C11 | `detect_contradictions` per-source clip | `deep_search_sota.py:248` | `[:300]` chars × 6 sources | Fine for contradiction probe. |
| C12 | Cross-encoder model | `deep_search_sota.py:432` | `Alibaba-NLP/gte-reranker-modernbert-base` | See §4. |

Net boundary between pipeline and chimere-server: **C6 (6000) for `quick`, C7 (12000) for `standard/deep`**, then `synthesize()` re-clips to ~7.2k chars (C1).

Observation: `synthesize()` runs **inside** `deep_search_sota.py` (line 724) → its `[:600]`-per-chunk clip is applied *before* anything reaches chimere-server. The final enricher-level cap (C6/C7) bounds the already-synthesised *answer text*, not the chunks — so raising C6/C7 alone has modest effect unless C1 is also widened.

## 2. chimere boundary: where is the final prompt truncated?

`odo.py:561-563` shows training-pair logging clips (`prompt[:2000]`, `response[:4000]`). These are log-only, **not** prompt transport.

Grep on odo.py for prompt truncation: the actual request body is forwarded un-truncated to chimere-server (`odo.py:989`). chimere-server itself enforces the KV-cache cap (64K on TQ3) rather than a char cap. **Conclusion: the ODO→chimere boundary has no char cap; only the enricher-level caps (C6/C7) constrain.**

## 3. Source orchestration audit

`parallel_search` (`deep_search_sota.py:341-378`) runs Brave + SearXNG in parallel via `ThreadPoolExecutor(max_workers=6)`. Academic channel is **SearXNG re-query filtered to academic domains** (l.313-338), not an independent endpoint.

Perplexica: implemented in `/home/remondiere/.openclaw/bin/perplexica_search.py` (`search()` at l.31) but **never imported by `deep_search_sota.py`** (`grep perplexica` returns 0 in that file). It is used only by `search_router.py` and `message_router.py` (legacy path).

**Opportunity:** adding Perplexica as a 4th source = free breadth (already running on localhost:3000). Cost: +1 HTTP call inside the parallel pool; no external API quota. Risk: Perplexica internally wraps SearXNG → risk of URL dup (RRF already deduplicates by URL at l.398-401, so no harm).

INSPIRE-HEP: viable for physics-domain queries via public HTTP API (no key). Would need a new `_search_inspire()` following the `_search_academic` pattern, triggered when `domain == "physics"` — but `SearchRouter._detect_domain` lacks a `physics` label; would need a pattern addition. **GATED** (scoped, domain-only).

Google Scholar / SerpAPI: requires paid key ($50/mo for 5k queries). Do not add.

## 4. Cross-encoder reranker (2026 landscape)

Current: `Alibaba-NLP/gte-reranker-modernbert-base` (l.432), `max_length=8192`, CPU.

April 2026 alternatives (CPU-realistic, ≤500M params):

| Model | Params | MTEB BEIR avg | Seq-len | CPU latency (20 pairs) | Notes |
|---|---|---|---|---|---|
| gte-reranker-modernbert-base (current) | 149M | 57.6 | 8192 | ~200ms | Good baseline |
| BAAI/bge-reranker-v2-m3 | 568M | 59.1 | 8192 | ~700ms | Multilingual strength |
| Alibaba-NLP/gte-reranker-modernbert-large | 434M | 60.3 | 8192 | ~550ms | Same family, +2.7 BEIR |
| mixedbread-ai/mxbai-rerank-large-v2 | 1.5B | 61.0 | 8192 | ~2s | Too slow CPU |
| jina-reranker-v3-base (2026-02) | 250M | 58.9 | 8192 | ~250ms | Close to current |

Recommendation: stick with current model for standard latency budget. Upgrade to `gte-reranker-modernbert-large` only if measured synthesis quality on TQ3 regresses (GATED). The ~350ms CPU delta matters on `quick`; acceptable on `deep`.

## 5. Cache hit-rate

Inspection of `~/.openclaw/.sota_cache/` (14 entries, 2026-03-27 → 2026-04-23):
- 11 entries are >24h old (quick TTL=1h, standard=2h, deep=6h all stale)
- 3 entries within TTL (one <0.1h, one 0.3h, one 0.5h) — all "H0 Hubble" variants from the current session

**Observed hit-rate ≈ 0** across a month. Queries are unique and semantically diverse; TTL extension does not help because exact-string match on query+depth (`_sota_cache_get` l.146). Recommendation: **keep TTL as-is**, but add per-domain semantic cache (embedding-nearest cache) as a future item — out of scope for this plan.

## 6. `expand_query` — TQ3 migration safety

`expand_query` (l.95-137) calls `_llm_call` (l.59-88) which POSTs to `LLAMA_URL = http://127.0.0.1:8084/v1/chat/completions` (l.41) — i.e. **odo.service (port 8084)**, which proxies to whichever backend occupies 8081. During TQ3 migration: if `qwen-tq3.service` owns 8081, expand_query works transparently. If there is a window where 8081 has no service, expand_query silently falls back to `[query]` (l.123) — degraded mode but not broken.

`nothink=True` is honoured if the TQ3 Jinja template supports `enable_thinking`. If TQ3 uses Qwen3.6 chat template, verify `chat_template_kwargs: {enable_thinking: false}` is still accepted.

**Action**: validate a TQ3 expand_query call returns a JSON array before enabling `standard`/`deep` paths at scale.

## 7. TQ3-opportunity edits

### SAFE (apply immediately, even before TQ3 is live)

**S1. Widen synthesis per-chunk clip and chunks_used (C1)** — `deep_search_sota.py:533`
- Reason: 7.2k char cap designed for 32K-ctx Apex. Doubling chunk count (12→20) and per-chunk text (600→1500) yields ~30k chars ≈ 10k tok synthesis context. Safe on both Apex (32K ctx, 22K still free) and TQ3 (64K).
- Edit below.

**S2. Widen enricher web-search caps (C6, C7)** — `enricher.py:108, 143`
- Reason: current 6000/12000 would clip a widened synthesis answer. Raise to 16000/32000.

**S3. Widen cross-encoder input truncation (C2)** — `deep_search_sota.py:447`
- Reason: `max_length=8192` tokens on the reranker ≈ 32k chars; current `[:4000]` leaves 87% of reranker capacity unused. Raise to `[:8000]`.

### GATED (apply after TQ3 E2E benchmark passes)

**G1. Bump DEPTH_CONFIG top_chunks** — `deep_search_sota.py:50-52`
- quick 8→10, standard 12→20, deep 16→28.
- Reason: the user's §7 "TQ3-specific opportunities" hypothesis. Gated because >20 retrieved chunks can reduce synthesis quality if reranker precision drops (measure PASS@1 on 10 canonical queries first).

**G2. Add Perplexica as 4th source** — `deep_search_sota.py:266-378`
- Reason: free breadth, already-running service. Gated because parallel_search timeout budget (30s, l.370) may need widening if Perplexica is slow.

**G3. Upgrade cross-encoder to `gte-reranker-modernbert-large`** — `deep_search_sota.py:432`
- Gated on measured +2.7 BEIR being visible in our synthesis quality.

---

## Exact `Edit` operations

### S1 — deep_search_sota.py synthesize() (SAFE)

```
file_path: /home/remondiere/.openclaw/bin/deep_search_sota.py
old_string:
    # Build context with numbered sources
    context_parts = []
    for i, c in enumerate(chunks[:12], 1):
        title = c.get("title", f"Source {i}")[:80]
        url   = c.get("url", "")
        text  = c.get("text", c.get("content", ""))[:600]
new_string:
    # Build context with numbered sources
    # 2026-04-23 TQ3 tuning: chunks 12→20, per-chunk text 600→1500 chars.
    # Target ~30k chars synthesis context for 64K-ctx TQ3 (Apex 32K still fits).
    context_parts = []
    for i, c in enumerate(chunks[:20], 1):
        title = c.get("title", f"Source {i}")[:120]
        url   = c.get("url", "")
        text  = c.get("text", c.get("content", ""))[:1500]
```

### S2a — enricher.py run_web_search cap (SAFE)

```
file_path: /home/remondiere/.openclaw/odo/enricher.py
old_string:
    return _run_script([PYTHON, str(script), query, "--depth", depth],
                       timeout=120, max_chars=6000)
new_string:
    # 2026-04-23 TQ3 tuning: 6000→16000 chars to match widened synthesis chunks.
    return _run_script([PYTHON, str(script), query, "--depth", depth],
                       timeout=120, max_chars=16000)
```

### S2b — enricher.py run_research cap (SAFE)

```
file_path: /home/remondiere/.openclaw/odo/enricher.py
old_string:
    return _run_script([PYTHON, str(script), query, "--depth", depth],
                       timeout=90, max_chars=12000)
new_string:
    # 2026-04-23 TQ3 tuning: 12000→32000 chars for deep research on 64K ctx.
    return _run_script([PYTHON, str(script), query, "--depth", depth],
                       timeout=90, max_chars=32000)
```

### S3 — cross-encoder input widening (SAFE)

```
file_path: /home/remondiere/.openclaw/bin/deep_search_sota.py
old_string:
    pairs = [(query, c.get("text", c.get("content", ""))[:4000]) for c in chunks]
new_string:
    # 2026-04-23 TQ3 tuning: 4000→8000 chars (reranker max_length=8192 tokens).
    pairs = [(query, c.get("text", c.get("content", ""))[:8000]) for c in chunks]
```

### G1 — DEPTH_CONFIG (GATED on TQ3 bench)

```
file_path: /home/remondiere/.openclaw/bin/deep_search_sota.py
old_string:
    "quick":    {"n_queries": 2, "max_pages": 2, "top_chunks": 8,  "max_results": 10},
    "standard": {"n_queries": 3, "max_pages": 3, "top_chunks": 12, "max_results": 15},
    "deep":     {"n_queries": 5, "max_pages": 5, "top_chunks": 16, "max_results": 20},
new_string:
    # 2026-04-23 TQ3 (GATED): top_chunks bumped for 64K ctx budget.
    "quick":    {"n_queries": 2, "max_pages": 2, "top_chunks": 10, "max_results": 10},
    "standard": {"n_queries": 3, "max_pages": 4, "top_chunks": 20, "max_results": 18},
    "deep":     {"n_queries": 5, "max_pages": 6, "top_chunks": 28, "max_results": 24},
```

### G2 — Perplexica as 4th source (GATED)

Insert after `_search_academic` (l.338), and register in `parallel_search` tasks (l.348).
Template:

```python
def _search_perplexica(query: str, count: int = 10) -> list[dict]:
    try:
        import perplexica_search
        raw = perplexica_search.search(query, mode="speed")
        return [
            {"title": r.get("title",""), "url": r.get("url",""),
             "content": r.get("content", r.get("snippet","")),
             "_source": "perplexica", "_query": query}
            for r in (raw or [])[:count]
        ]
    except Exception as exc:
        print(f"[SOTA] Perplexica error: {exc}", file=sys.stderr)
        return []
```

Add `tasks.append(("perplexica", q, domain))` inside the `for q in queries:` loop of `parallel_search`, and a dispatch branch in `_run`. Bump `max_workers=min(len(tasks), 8)`. Timeout widening to 45s (l.370) recommended.

### G3 — Upgrade reranker (GATED)

```
file_path: /home/remondiere/.openclaw/bin/deep_search_sota.py
old_string:
            _cross_encoder = CrossEncoder(
                "Alibaba-NLP/gte-reranker-modernbert-base",
                max_length=8192, device="cpu"
            )
new_string:
            _cross_encoder = CrossEncoder(
                "Alibaba-NLP/gte-reranker-modernbert-large",
                max_length=8192, device="cpu"
            )
```

Note: first call will download ~870 MB; ensure disk slack under `~/.cache/huggingface/`.

---

## Verification checklist before applying GATED

1. `qwen-tq3.service` active on 8081, `curl http://127.0.0.1:8081/health` → ok.
2. `deep_search_sota.py "cherche la valeur de H0 2026" --depth standard --json | jq .elapsed` within 90s.
3. Synthesis quality spot-check on 3 queries: physics (Hubble), medical (lombalgie HAS), code (Qwen quantization). Compare citations count + factuality.
4. `context_chars` in odo enricher logs ≥ 20000 on `standard` (indicates widened caps are effective).

If (2) breaks >90s or (3) degrades vs current, roll back G1 first.
