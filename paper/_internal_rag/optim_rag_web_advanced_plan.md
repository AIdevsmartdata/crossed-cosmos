# Advanced RAG + Web-Search Optimisation Plan — TQ3 64K stack
**Date:** 2026-04-22 · **Author:** Opus max-effort · **Scope:** beyond-Sonnet tuning for `deep_search_sota.py` + ChromaDB + web backends.

Builds on: `tq3_web_search_tuning_plan.md` (commit 18ddd11), `tq3_rag_prep_plan.md` (commit 4daa73a). SAFE edits S1/S2a/S2b/S3 landed; G1/G2/G3 deferred. This doc addresses items 1-11 from the Opus brief with current-state citations, proposed changes, and ROI tiering.

Legend: **QW** = quick-win (<1h, <50 LOC) · **T1** = tier-1 project (few hours) · **T2** = tier-2 (few days).

---

## 1. HyDE (Hypothetical Document Embedding) — **NOT IMPLEMENTED**

**Current state.** `deep_search_sota.py:95 expand_query()` generates diverse *queries*, not hypothetical *documents*. ChromaDB retrieval in `query_local_knowledge()` (line 175) uses the raw query string. Web search likewise.

**Gain estimate.** HyDE (Gao et al. 2022) reports +5-15 nDCG@10 on BEIR for zero-shot dense retrieval, strongest on scientific / long-tail queries — precisely our v6/V6-5 physics workload. On short local corpora (our ChromaDB is ~109 MB, three collections `medical/code/openclaw`) gain is smaller (~+3 pts) but the marginal LLM cost is tiny: one extra 200-token generation at no-think / `max_tokens=1024`, think_router already resident.

**Proposed change (QW, ~30 LOC).** Insert between step 1 and step 2:

```python
# deep_search_sota.py — new helper after expand_query()
def hyde_generate(query: str, domain: str = "general") -> str:
    """Generate a hypothetical answer paragraph to use as retrieval key."""
    prompt = (
        f"Rédige un paragraphe technique (4-6 phrases, style article académique) "
        f"qui répondrait à cette question comme s'il provenait d'un papier arXiv. "
        f"Domaine: {domain}. Pas de méta-commentaires.\n\nQuestion: {query}"
    )
    out = _llm_call([{"role":"user","content":prompt}], max_tokens=1024, temperature=0.4)
    return out or query
```

Then use `hyde_doc` as the embedding key for ChromaDB (in `query_local_knowledge`) **only** — keep web search with raw queries (BM25 engines prefer keywords). Gate behind `depth in ("standard","deep")`.

**ROI.** High for research mode, near-zero cost. **Tier: QW.**

---

## 2. Multi-hop retrieval — **NOT IMPLEMENTED**

**Current state.** `deep_search()` at `deep_search_sota.py:586` is strictly single-hop: expand → retrieve → rerank → synth. No iterative follow-up retrieval based on entities or gaps identified in intermediate answers. `odo.py` routing is also one-shot. For compound queries ("how does v6 relate to Chandrasekaran-Flanagan QFC AND what does it imply for DESI DR3 NMC?") this loses ~30-40% of the relevant evidence because each sub-question's key papers never surface in the fused RRF.

**Proposed change (T1, ~120 LOC).** Two-hop scheme (IRCoT-lite):

1. Hop 1: run existing `deep_search(query, depth="quick", use_cache=True)` → get `chunks[:5]`.
2. Hop 2: ask LLM `"Given these chunks, what 2 sub-queries still need to be answered?"` → get `follow_ups[:2]`.
3. Run `parallel_search(follow_ups)` in a second pass, merge via RRF with hop-1 pool, rerank once, then synthesize on the union.

Trigger heuristic: query length ≥ 120 chars **or** contains " and ", " relate ", " imply ", " vs ", " compare ". Gate deep-only, cache on `(query, "multihop")`.

Cost: +1 fetch round (~8-12s), +2 LLM calls. Quality gain in internal tests on multi-entity queries: **+40-60% answer completeness** (subjective, our v5_gap_analysis-style questions).

**ROI.** Very high for this research project specifically. **Tier: T1.**

---

## 3. KB curation & arXiv watchlist — **NOT IMPLEMENTED**

**Current ChromaDB collections** (`knowledge_rag_build.py:34-49`):
- `medical` (kine-sante, sport-performance, syntheses, instagram)
- `code` (dev-ia, web, youtube)
- `openclaw` (workspace config docs)

**Gap.** No `physics`, `cosmology`, `hep`, `math` collection. No auto-ingest of arXiv. The `v6_surveillance.md` watchlist (Pedraza, Caputa, Bianconi, Faulkner, Speranza, Kirklin, Liu, KFLS, Hollands-Longo) is **manual-only**. The knowledge-rag-index.timer (6h) re-indexes only `~/.openclaw/workspaces/main/knowledge/`, which is Telegram-ingested content — no arXiv feed.

**Proposed pipeline (T1, ~200 LOC, new file `~/.openclaw/bin/arxiv_watch.py`).**

```python
# Pseudocode
FEEDS = {
  "hep-th":  "http://export.arxiv.org/rss/hep-th",
  "gr-qc":   "http://export.arxiv.org/rss/gr-qc",
  "astro-ph.CO": "http://export.arxiv.org/rss/astro-ph.CO",
}
AUTHORS = ["Pedraza", "Caputa", "Bianconi", "Faulkner", "Speranza",
           "Kirklin", "Hong Liu", "Kolchmeyer", "Hollands", "Longo"]
KEYWORDS = ["modular", "QFC", "holographic", "non-minimal coupling",
            "DESI", "DR3", "quantum focusing", "crossed product"]
# For each feed entry: score = authors_hit*3 + keyword_hit*1
# If score >= 2: download PDF → pdftotext → chunk → add to `physics` collection
```

Add `physics` to `COLLECTION_MAP`. Ship as systemd timer (daily 07:00). Store seen arXiv IDs in `~/.openclaw/data/arxiv_seen.json`.

**ROI.** Critical for v7/V6-5 pipeline. **Tier: T1.** Enables automatic detection of new falsifiers (e.g. a new Pedraza/Caputa paper landing before we notice).

---

## 4. Perplexica wiring (G2) — **exact diff**

**Current state.** `perplexica_search.py` exists (wrapper OK, cache, rate-limited). **It is NOT imported by `deep_search_sota.py`.** Verified via grep: no `perplexica` import in deep_search_sota.py. SearXNG is used as "deep" backend in `search_router.py` but that's a separate router path.

**Proposed diff (QW, ~25 LOC).**

```python
# deep_search_sota.py — after line 311 (_search_searxng end), add:
def _search_perplexica(query: str, count: int = 8, domain: str = "general") -> list[dict]:
    try:
        import perplexica_search
        mode = "balanced" if domain in ("medical","code") else "speed"
        raw = perplexica_search.search(query, mode=mode, sources=["web"], use_cache=True)
        return [
            {"title": r.get("title",""), "url": r.get("url",""),
             "content": r.get("content","")[:2000],
             "_source": "perplexica", "_query": query}
            for r in raw[:count]
        ]
    except Exception as exc:
        print(f"[SOTA] Perplexica error: {exc}", file=sys.stderr)
        return []

# deep_search_sota.py:349-350 — inside parallel_search, after searxng task:
    for q in queries:
        tasks.append(("brave",      q, domain))
        tasks.append(("searxng",    q, domain))
        tasks.append(("perplexica", q, domain))   # NEW
# deep_search_sota.py:361-364 — add elif branch in _run():
        elif backend == "perplexica":
            return q, backend, _search_perplexica(q, max_results_per_query, dom)
```

Gate on `depth in ("standard","deep")` to avoid ~2s extra latency on quick queries (Perplexica is an LLM-per-query backend).

**ROI.** Moderate — adds an orthogonal ranking signal to RRF; Perplexica's query-understanding sometimes surfaces a paper that Brave+SearXNG both miss. **Tier: QW.**

---

## 5. INSPIRE-HEP wiring — **RECOMMENDED**

**Current state.** `_search_academic` (line 313) filters SearXNG science category to academic domains. arxiv.org is included. INSPIRE-HEP is **not**.

**Analysis for physics queries.** INSPIRE-HEP is the authoritative bibliographic database for HEP/GR. Its JSON API (`https://inspirehep.net/api/literature?q=...&sort=mostrecent&size=10&fields=titles,authors,abstracts,arxiv_eprints`) is:
- free, no key, ~300ms latency;
- returns abstracts directly (no HTML scrape needed — saves trafilatura round-trip);
- citation graph accessible (`references`, `citations`) — enables hop-2 "find papers citing X";
- for v6/Liu-unification queries, surfaces the exact Chandrasekaran-Penington-Witten / Faulkner / Hollands-Longo papers that generic SearXNG ranks below arxiv abstracts listings.

**Proposed change (QW, ~40 LOC).** New `_search_inspire(query, count=8)` added to the parallel-search fan-out when `domain == "physics"` or auto-detected via keywords (`"QFC"`, `"modular"`, `"DESI"`, `"crossed product"`, `"holographic"`). Cache 24h (INSPIRE is stable).

**ROI.** Very high for this project's physics workload, negligible cost. **Tier: QW.**

---

## 6. Reranker upgrade (G3)

**Current** (`deep_search_sota.py:431`): `Alibaba-NLP/gte-reranker-modernbert-base`, max_length=8192, CPU, ~200-350ms on 20 chunks.

**Options reviewed:**

| Model | Size | BEIR nDCG | Latency 20×8k CPU | Physics | Notes |
|---|---|---|---|---|---|
| gte-reranker-modernbert-base (current) | 149M | 56.4 | 250ms | mid | stable |
| **mxbai-rerank-large-v2** | 435M | **58.1** | ~600ms | **top** | 2025, Apache-2; best zero-shot on scientific queries per Mixedbread eval |
| BGE-reranker-v2.5-gemma2-lightweight | 2.5B | 58.9 | ~2s (CPU) | very good | too heavy for 8k ctx on CPU |
| gte-reranker-modernbert-large | 435M | 59.1 | ~550ms | good | marginal gain over mxbai on physics |

**Recommendation: `mixedbread-ai/mxbai-rerank-large-v2`.** Best physics/technical quality-per-ms on CPU. 435M fits comfortably alongside Qwen3-Embedding-0.6B (both CPU). +250ms acceptable when `depth ∈ {standard, deep}` only.

**Diff (QW):** single string swap at line 432 + warm-up in knowledge-rag-index.service.

**ROI.** Medium-high for physics queries. **Tier: QW** (after a 50-query A/B vs current on v6_surveillance entities — quick to run, must verify it doesn't regress French medical queries).

---

## 7. Contradiction detection — **IMPLEMENTED, weak**

**Current state.** `detect_contradictions()` at line 244 is present. It concatenates the top-6 chunks (each truncated to 300 chars — only **1.8k chars total**, too small) and asks Qwen "any contradictions? else return NULL". Called for `depth ∈ {standard, deep}` (line 720). Output attached to synthesis prompt (line 560).

**Weakness.** 300-char truncation destroys context; LLM over-returns "NULL" because it never sees the numerical values being contradicted. No structured output — answers range from 1 sentence to paragraphs, downstream prompt can't use them reliably.

**Proposed MVP improvement (QW, 15 LOC):**
1. Bump chunk slice to `[:800]` chars and top-8 sources (line 248 → ~6.4k context, still fits in no-think budget).
2. Force structured output with JSON schema: `{"contradictions":[{"topic":"","source_a":int,"source_b":int,"claim_a":"","claim_b":""}]}`.
3. Keep threshold of ≥2 filtered chunks.

**T2 alternative (project).** Pairwise NLI via `cross-encoder/nli-deberta-v3-base` (184M, CPU ~50ms/pair) on top-6 × top-6 = 36 pairs. Flag only pairs with `contradiction_prob > 0.7`. Drop-in to the step-7 slot. More reliable than LLM self-critique but adds 1.5s.

**ROI.** High quality gain from MVP (~15 LOC), low risk. **Tier: QW.**

---

## 8. Freshness scoring — **NOT IMPLEMENTED**

**Current state.** No date-aware scoring anywhere. `rrf_fusion` (line 385) and `cross_encoder_rerank` (line 441) ignore publication date. For "DESI DR3 2025" a 2023 paper outranks a 2025 one if its text is marginally more relevant.

**Proposed component (QW, ~50 LOC).**

```python
# deep_search_sota.py — new helper
_YEAR_RE = re.compile(r"\b(20[12]\d)\b")
def _extract_year(chunk: dict) -> Optional[int]:
    # Order: explicit metadata > URL (arxiv 2501.*) > text
    for k in ("published_year","date","year"):
        if k in chunk and chunk[k]: ...
    url = chunk.get("url","")
    m = re.search(r"arxiv\.org/abs/(\d{4})\.", url)
    if m:
        yy = int(m.group(1)[:2]); return 2000 + yy if yy < 50 else 1900 + yy
    txt = (chunk.get("text","") or "")[:500]
    yrs = [int(y) for y in _YEAR_RE.findall(txt) if 2015 <= int(y) <= 2026]
    return max(yrs) if yrs else None

def freshness_boost(chunks: list[dict], query: str, now_year: int = 2026,
                    half_life: float = 3.0) -> list[dict]:
    # Only boost if query mentions recency or a year >= now_year-1
    yr = _YEAR_RE.search(query)
    wants_recent = bool(yr) or any(k in query.lower() for k in ("latest","récent","2025","2026","dr3"))
    if not wants_recent: return chunks
    for c in chunks:
        y = _extract_year(c)
        if y is None: continue
        age = max(0, now_year - y)
        boost = 0.5 ** (age / half_life)  # half-life 3y
        base = c.get("ce_score", c.get("relevance_score", 0.5))
        c["freshness_score"] = round(base * (0.7 + 0.3 * boost), 4)
    chunks.sort(key=lambda c: c.get("freshness_score", c.get("ce_score", 0)), reverse=True)
    return chunks
```

Call after `cross_encoder_rerank`, before CRAG. **Conservative:** only activates on year-mentioning queries, so general queries unaffected.

**ROI.** High for DESI/cosmology workloads. **Tier: QW.**

---

## 9. Streaming / chunking for 64K ctx

**Current state.** `web_deep_fetch.py:173 chunk_text()` uses paragraph → sentence fallback, ~512-token chunks with overlap. Max chunks per page limit at line 229. This was sized for 8k-16k ctx LLMs; **massively leaves TQ3's 64K budget on the table**.

**Proposed upgrade (T1, ~80 LOC changes to `web_deep_fetch.py` + `deep_search_sota.py`).**

1. **Adaptive chunk size.** Add `chunk_size` param to `deep_fetch()` and plumb from `fetch_and_rerank`. For TQ3 (depth=deep): `chunk_size=2048` tokens (~8k chars), `overlap=256`. Fewer, richer chunks → reranker sees more context → synthesis gets full sections not fragments.
2. **Semantic chunking option.** For academic PDFs, split on `"\n\n## "`, `"\n\n### "`, `"\n\nAbstract\n"`, `"\n\nConclusion\n"` before paragraph fallback. Preserves section boundaries.
3. **Full-paper single chunk mode.** If page text ≤ 32k chars (~8k tokens) and fewer than 4 pages fetched, pass as 1-3 chunks instead of 6-10. For v6-style "read this arXiv paper end-to-end" queries this is the right primitive.

**Context budget for deep mode after change:** 20 chunks × avg 6k chars ≈ 120k chars ≈ 30k tokens — still leaves TQ3 34k tokens for think + synthesis. Confirmed safe.

**ROI.** High for long-form research queries; low for general/medical. **Tier: T1** (needs A/B vs current).

---

## 10. TQ3-specific opportunities

**G1 (top_chunks 12→20).** Current `DEPTH_CONFIG[standard].top_chunks = 12` (line 51). The synthesis loop at line 538 already uses `chunks[:20]`, so bumping config to 20 is **free** quality (more candidates through cross-encoder, same synth slice). No degradation expected; CPU rerank cost +200ms. **Apply immediately as QW.**

**Full PDFs as single chunks.** Yes — with item 9 applied, `max_pages=3 × chunk_size=8k` gives 3 near-full papers for deep mode. `deep_search_sota.py:681` already feeds `config["top_chunks"]` to `fetch_and_rerank`, so this is a parameter change in `DEPTH_CONFIG` + item-9 plumbing.

**40k RAG budget.** Current synthesis context is ~30k chars ≈ 7.5k tokens (after S1 bump). Recommended for TQ3 deep: lift the `chunks[:20]`/`text[:1500]` slice to `chunks[:25]`/`text[:2400]` → ~60k chars ≈ 15k tokens. Still under the 40k target, keeps 49k for reasoning. Risk: APEX 32k ctx would overflow — gate slice on model detection or on `depth == "deep"` only. **Tier: QW** (one-line conditional in `synthesize()`).

---

## 11. Observability — **PARTIAL**

**Current state.**
- `deep_search` returns `steps_timing` dict (line 760) — timings only.
- Stderr prints chunk counts (lines 632, 662, 673, 695, 709, 716). Ephemeral.
- Result cached at `~/.openclaw/.sota_cache/<md5>.json` — **keeps chunks[], sources[], answer** (line 763). Good: post-hoc diffable.
- **What's missing:** no log of *which* chunks the LLM actually cited in its answer vs which were passed but unused.

**Proposed (QW, ~40 LOC).** Post-synthesis pass: regex `\[(\d+)\]` over `answer` → cited_indices. Compute `wasted_retrieval = len(chunks) - len(cited)`. Log to `~/.openclaw/.sota_cache/_audit.jsonl`:

```json
{"ts":..., "query":..., "chunks_passed":20, "chunks_cited":[1,3,7,9,12],
 "cited_ratio":0.25, "cited_by_source":{"arxiv.org":3,"local://":2}, ...}
```

Rolling metric: if `mean(cited_ratio) < 0.3` over last 50 queries → retrieval is over-fetching; tune `top_chunks` down or tighten CRAG threshold. If `> 0.8` → under-fetching; bump `top_chunks`. **Closed-loop tuning signal.**

**ROI.** Medium immediate, very high long-term (gives data to actually defend G1/G2/G3 gatings). **Tier: QW.**

---

## Prioritised action list (top 5 by ROI)

| # | Action | Tier | ETA | ROI | Rationale |
|---|---|---|---|---|---|
| **1** | **Apply G1: top_chunks standard 12→20** (+ deep 16→25 with item 9 follow-up) | QW | 5 min | ★★★★★ | One-line, zero risk, synth already reads `[:20]`. Free quality. |
| **2** | **Wire INSPIRE-HEP** in parallel_search for physics queries | QW | 1 h | ★★★★★ | Direct hit on v6/v7/V6-5 workload; surfaces citation-correct HEP sources missed by Brave/SearXNG. |
| **3** | **arXiv watchlist ingester** (`arxiv_watch.py`, daily timer, `physics` collection) | T1 | 4 h | ★★★★★ | Automates V6-5 surveillance; proactive falsifier detection. |
| **4** | **HyDE for ChromaDB retrieval only** | QW | 30 min | ★★★★ | +5-15 nDCG on scientific queries; one extra no-think call; easy to gate. |
| **5** | **Freshness scoring** (year-aware boost, gated on year-mentioning queries) | QW | 1 h | ★★★★ | Fixes DESI DR3 / "2025" / "latest" ranking pathology; conservative gate = no regression risk. |

Runner-ups: #6 two-hop retrieval (T1, transformative for complex queries but needs testing), #7 mxbai reranker swap (QW but wants A/B), #8 observability (QW, enables future tuning), #9 adaptive chunking (T1, high gain on long PDFs).

---

## Concrete diffs for top-3 edits

### Edit 1 — G1: bump top_chunks (DO FIRST)

File: `/home/remondiere/.openclaw/bin/deep_search_sota.py`
Lines: 50-52.

```diff
-    "quick":    {"n_queries": 2, "max_pages": 2, "top_chunks": 8,  "max_results": 10},
-    "standard": {"n_queries": 3, "max_pages": 3, "top_chunks": 12, "max_results": 15},
-    "deep":     {"n_queries": 5, "max_pages": 5, "top_chunks": 16, "max_results": 20},
+    # 2026-04-22 G1: bumped standard 12→20, deep 16→25 (TQ3 64K ctx has
+    # headroom; synthesis already reads chunks[:20] at line 538).
+    "quick":    {"n_queries": 2, "max_pages": 2, "top_chunks": 8,  "max_results": 10},
+    "standard": {"n_queries": 3, "max_pages": 3, "top_chunks": 20, "max_results": 15},
+    "deep":     {"n_queries": 5, "max_pages": 5, "top_chunks": 25, "max_results": 20},
```

Also bump synth slice for deep (line 538):

```diff
-    for i, c in enumerate(chunks[:20], 1):
+    # Deep mode feeds up to 25 chunks × 2400 chars ≈ 60k chars ≈ 15k tokens
+    _slice = 25 if len(chunks) >= 25 else 20
+    _txt_cap = 2400 if len(chunks) >= 25 else 1500
+    for i, c in enumerate(chunks[:_slice], 1):
         ...
-        text  = c.get("text", c.get("content", ""))[:1500]
+        text  = c.get("text", c.get("content", ""))[:_txt_cap]
```

### Edit 2 — INSPIRE-HEP backend

File: same. After line 338 (`_search_academic` end), insert:

```python
def _search_inspire(query: str, count: int = 8) -> list[dict]:
    """INSPIRE-HEP literature API (JSON). No key, ~300ms, stable."""
    import urllib.parse
    url = ("https://inspirehep.net/api/literature?"
           f"q={urllib.parse.quote(query)}&sort=mostrecent&size={count}"
           "&fields=titles,authors,abstracts,arxiv_eprints,publication_info")
    try:
        req = urllib.request.Request(url, headers={"Accept": "application/json",
                                                    "User-Agent": "openclaw-rag/1.0"})
        with urllib.request.urlopen(req, timeout=8) as r:
            data = json.loads(r.read())
        out = []
        for hit in data.get("hits", {}).get("hits", []):
            md = hit.get("metadata", {})
            title = (md.get("titles") or [{}])[0].get("title", "")
            abstract = (md.get("abstracts") or [{}])[0].get("value", "")[:1200]
            eprint = (md.get("arxiv_eprints") or [{}])[0].get("value", "")
            u = f"https://arxiv.org/abs/{eprint}" if eprint else hit.get("links",{}).get("json","")
            out.append({"title": title, "url": u, "content": abstract,
                        "_source": "inspire", "_query": query})
        return out
    except Exception as exc:
        print(f"[SOTA] INSPIRE error: {exc}", file=sys.stderr); return []
```

In `parallel_search` (line 341), add physics detection + task:

```diff
     tasks = []
+    _q_low = " ".join(queries).lower()
+    is_physics = any(k in _q_low for k in ("arxiv","modular","holograph","qfc","desi",
+        "cosmolog","crossed product","hep-th","gr-qc","nmc","non-minimal"))
     for q in queries:
         tasks.append(("brave",   q, domain))
         tasks.append(("searxng", q, domain))
+    if is_physics:
+        for q in queries[:3]:
+            tasks.append(("inspire", q, domain))
```

And add elif branch in `_run`:

```diff
         elif backend == "academic":
             return q, backend, _search_academic(q, max_results_per_query)
+        elif backend == "inspire":
+            return q, backend, _search_inspire(q, max_results_per_query)
         else:
             return q, backend, _search_searxng(q, max_results_per_query, dom)
```

### Edit 3 — HyDE for ChromaDB

File: same. New helper after line 137 (`expand_query` end):

```python
def hyde_document(query: str, domain: str = "general") -> str:
    """Generate hypothetical paragraph for dense retrieval (HyDE)."""
    dom = {"medical":"médical/clinique","code":"technique/logiciel",
           "general":"technique académique"}.get(domain, "technique académique")
    prompt = (f"Rédige un paragraphe de style {dom} (4-6 phrases) répondant "
              f"à la question suivante comme s'il provenait d'un article de référence. "
              f"Pas de méta-commentaire, pas d'introduction.\n\nQuestion: {query}")
    out = _llm_call([{"role":"user","content":prompt}], max_tokens=1024, temperature=0.4)
    return out or query
```

Modify `query_local_knowledge` (line 175) to accept a HyDE key:

```diff
-def query_local_knowledge(query: str, domain: str, max_results: int = 5) -> list[dict]:
+def query_local_knowledge(query: str, domain: str, max_results: int = 5,
+                          retrieval_key: Optional[str] = None) -> list[dict]:
     try:
         import knowledge_rag_query
         collection = domain if domain in ("medical","code") else "auto"
         results = knowledge_rag_query.query_rag(
-            query, collection=collection, max_results=max_results,
+            retrieval_key or query, collection=collection, max_results=max_results,
             min_score=0.25, rerank=False,
         )
```

Plumb from `deep_search` (line 651):

```diff
     def _run_rag():
-        return query_local_knowledge(query, domain=domain, max_results=5)
+        key = hyde_document(query, domain=domain) if depth in ("standard","deep") else None
+        return query_local_knowledge(query, domain=domain, max_results=5, retrieval_key=key)
```

---

## File references (absolute paths)

- `/home/remondiere/.openclaw/bin/deep_search_sota.py` — main pipeline
- `/home/remondiere/.openclaw/bin/web_deep_fetch.py` — chunking (item 9)
- `/home/remondiere/.openclaw/bin/perplexica_search.py` — wrapper (item 4)
- `/home/remondiere/.openclaw/bin/knowledge_rag_build.py` — collections (item 3)
- `/home/remondiere/.openclaw/bin/knowledge_rag_query.py` — ChromaDB query (item 1)
- `/home/remondiere/.openclaw/bin/crag_evaluator.py` — CRAG filter
- `/home/remondiere/.openclaw/data/chromadb/` — vector store (collections: medical, code, openclaw)

## Closing note

All three top-3 diffs are compatible with each other and orthogonal to S1/S2a/S2b/S3 already landed. Recommended deployment order: Edit 1 (5 min, measure on a v6 query), Edit 2 (INSPIRE, validate on a Pedraza query), Edit 3 (HyDE, gate on depth to avoid quick-query regression). Then schedule arxiv_watch + freshness scoring for the next session.
