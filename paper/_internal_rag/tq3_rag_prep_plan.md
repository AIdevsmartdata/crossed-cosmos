# TQ3 RAG Pipeline Integration Prep Plan

**Date**: 2026-04-22
**Target**: Qwen3.6-35B-A3B-TQ3_4S (port 8083, `qwen-tq3.service`)
**Replaces** (or coexists with): Qwen3.6 APEX I-Quality via chimere-server (port 8081)
**Scope**: pre-migration actions on the RAG stack only. Does NOT cover the llama.cpp-tq3 build itself (separate post-mortem) nor the APEX tokenizer fix (documented in `chimere_apex_tokenizer_fix_2026-04-23.md`).

Every claim below cites a file:line. "TODO-NOW" = safe to run before TQ3 service is live. "TODO-POST" = after `systemctl --user start qwen-tq3`.

---

## 1. ChromaDB collection integrity

**Inspection** (run 2026-04-22 08:45):
- Path: `~/.openclaw/data/chromadb/` (109 MB, sqlite 58 MB).
- 4 collections (sqlite `collections` table):
  | name | dim | approx vectors |
  |---|---|---|
  | `medical` | 1024 | 3766 |
  | `code` | 1024 | 3843 |
  | `openclaw` | 1024 | 1704 |
  | `kinebot_android` | 384 | 47 |
- Embedder: `Qwen/Qwen3-Embedding-0.6B`, CPU, confirmed at `~/.openclaw/bin/knowledge_rag_build.py:26` (`EMBED_MODEL = "Qwen/Qwen3-Embedding-0.6B"`) and `:175` (`SentenceTransformer(EMBED_MODEL, device="cpu")`).
- `kinebot_android` is 384-dim → different embedder (likely `all-MiniLM-L6-v2`). Not touched by the main pipeline; ignore for this migration.

**Re-indexing needed?** **NO.** The embedder is a separate model loaded on CPU (`knowledge_rag_build.py:175`). It has no dependency on the generation model's tokenizer or weights. TQ3 swap does not invalidate vectors.

**TODO-NOW**:
```bash
# Snapshot ChromaDB before any restart — rollback insurance
cp -a ~/.openclaw/data/chromadb ~/.openclaw/data/chromadb.pre-tq3-$(date +%Y%m%d)
# Sanity read (read-only, shouldn't conflict with any writer)
sqlite3 ~/.openclaw/data/chromadb/chroma.sqlite3 \
  "SELECT name, dimension FROM collections;"
```

---

## 2. `knowledge_search.py` — assumptions audit

File: `~/.openclaw/bin/knowledge_search.py` (268 lines, read entirely).

- **Pure markdown grep over `~/.openclaw/workspaces/main/knowledge/`** (`:25-26`). No ChromaDB, no LLM call.
- Zero generation-model assumption. No tokenizer, no context-length reference, no port binding.
- **Verdict**: TQ3-safe, no change needed.

The *vector* variant is `~/.openclaw/bin/knowledge_rag_query.py` (separate file). `knowledge_search.py` is the lexical fallback.

---

## 3. `confidence_rag_trigger.py` — trigger & threshold audit

File: `~/.openclaw/odo/confidence_rag_trigger.py`.

- Backend URL: `CHIMERE_BACKEND` env, default `http://127.0.0.1:8081` (`:32`). **Currently points at APEX via chimere-server.**
- Sends an OpenAI-compatible `/v1/chat/completions` probe (`:95`) with `logprobs=True, top_logprobs=5` (`:86-87`).
- Decision thresholds (hard-coded, `:142-167`):
  - hedge regex match → `deep_rag`
  - `mean_entropy > 0.6` → `deep_rag`
  - `mean_entropy > 0.35` → `quick_rag`
  - `mean_entropy == 0.0` (no logprobs, chimere-server FFI case) + short/cutoff → `quick_rag`
  - else → `skip_rag`

**Model dependence**:
- Entropy thresholds (0.35 / 0.6) were calibrated against APEX. TQ3 at 3.07 BPW has **measurably higher intrinsic entropy** (any aggressive quant does). Thresholds will **over-trigger** RAG on TQ3 unless recalibrated.
- The fallback branch `mean_entropy == 0.0` at `:151` exists precisely because chimere-server FFI doesn't return logprobs. Direct `llama-server` on 8083 **does** return logprobs → the fallback branch will *not* fire, and raw entropy comparisons take over. This is a behaviour change.

**Recommendation**: post-migration, run a 20-prompt calibration pass and lift thresholds ~15-20% (e.g. 0.40 / 0.70). Not a blocker for first-launch.

**TODO-POST** (calibration):
```bash
CHIMERE_BACKEND=http://127.0.0.1:8083 \
  python3 ~/.openclaw/odo/confidence_rag_trigger.py  # runs the __main__ self-test, :223-240
```

---

## 4. Engram L1-L4 — the real loss

**Fact**: Engram is implemented inside the Rust FFI layer of `chimere-server`, consuming `CHIMERE_ENGRAM_DIR=~/.openclaw/data/engram` (21 MB). Plain `llama-server` (the TQ3 binary at `build_sm120/bin/llama-server`) has no Engram hook. Confirmed by `odo.py:63` which routes only to a single OpenAI-compat URL — no Engram sidecar exists at the odo layer.

### Option (a) — Accept loss
- Pros: zero work, unblocks TQ3 today.
- Cons: L2/L3 recall features disappear; dynamic engram system-prompt injection in odo (`odo.py:703-716`) still runs because it's a *prompt-level* feature (odo injects via system message, not FFI). **→ only the FFI-level KV/state-persistence Engram is lost, not the prompt-level dynamic engram.** This is a much smaller loss than feared.

### Option (b) — Rebuild chimere-server against turbo-tan libllama
- Requires: link chimere-server Rust FFI against `llama.cpp-tq3` fork's `libllama.so` instead of `ik_llama.cpp`'s.
- Risk: TQ3_4S tensor types (`TQ3_0`, 3.07 BPW) are only understood by the turbo-tan fork's GGUF loader. The FFI must expose them; likely `ggml-quants.h` additions.
- Effort: 1-2 days (build + FFI ABI check + re-test tokenizer fix).
- Benefit: keeps FFI Engram, keeps 8081 as the stable port.

### Option (c) — Odo-level caching emulation
- Implement a simple KV cache keyed by `(conversation_id, turn_hash)` at odo ingress, serving as "L1" poor-man's engram.
- Effort: half-day. Doesn't replicate L2/L3 semantic recall but covers the hot-path.

**Recommendation**: **(a) now**, **(b) in a follow-up sprint**. Option (c) is a distraction unless the FFI-Engram loss shows up in user-visible metrics (look at chimere stats endpoint post-migration).

---

## 5. Re-index decision

Answered in §1. **Confirmed NO re-index needed** — embedder is independent (`knowledge_rag_build.py:26,175`). The migration doc section "ChromaDB" should state this explicitly.

One caveat: if TQ3 changes the tokenizer (cf. the APEX tokenizer bug doc), then *retrieved chunks may tokenize differently in the generation context*. But the retrieval step itself is untouched. No corrective action.

---

## 6. Pre-warming (executable now)

All commands below are TODO-NOW, safe to run before `qwen-tq3` is live.

### 6.1 Pre-warm the CPU embedder
`SentenceTransformer` lazy-loads on first ingest call (`knowledge_rag_build.py:175`). Force the HF cache now:
```bash
~/.openclaw/venvs/kine-rag/bin/python -c "\
from sentence_transformers import SentenceTransformer; \
m = SentenceTransformer('Qwen/Qwen3-Embedding-0.6B', device='cpu'); \
print('embed dim =', m.get_sentence_embedding_dimension())"
```

### 6.2 Pre-warm ChromaDB client
```bash
~/.openclaw/venvs/kine-rag/bin/python -c "\
import chromadb; \
c = chromadb.PersistentClient(path='$HOME/.openclaw/data/chromadb'); \
print([x.name for x in c.list_collections()])"
```

### 6.3 Pre-warm cross-encoder reranker (if `deep_search_sota` will be invoked)
Reranker model name is referenced in the deep-search pipeline; the generic pre-warm:
```bash
~/.openclaw/venvs/kine-rag/bin/python -c "\
from sentence_transformers import CrossEncoder; \
CrossEncoder('BAAI/bge-reranker-v2-m3', device='cpu')" 2>&1 | tail -3
```
(Non-critical — reranker is only in `deep` depth.)

### 6.4 Pause scheduled jobs during migration window
```bash
systemctl --user stop knowledge-rag-index.timer          # 6h cron, could collide
systemctl --user stop engram-write-nightly.timer        # chimere FFI writes to engram dir
# Don't disable — just stop. Re-arm after TQ3 is stable:
# systemctl --user start knowledge-rag-index.timer
```

### 6.5 Snapshot ChromaDB (see §1)
Already listed — do this once.

### 6.6 Verify model file integrity (avoid post-launch surprise)
```bash
ls -la ~/.openclaw/models/Qwen3.6-35B-A3B-TQ3_4S/Qwen3.6-35B-A3B-TQ3_4S.gguf
# expected ~12.4 GB = 13_298_875_360 bytes (confirmed present 2026-04-23 08:47)
```

---

## 7. Honest risk list

| # | Risk | Likelihood | Mitigation |
|---|---|---|---|
| R1 | `knowledge-rag-index.timer` fires at 00:00 during TQ3 bring-up, opening a ChromaDB writer while odo's confidence probe indirectly holds a reader. SQLite WAL normally handles it, but the 7200 s `TimeoutStartSec` means a stuck ingest blocks for 2 h. | **Medium** | §6.4 stop the timer before launch. |
| R2 | `confidence_rag_trigger` thresholds over-trigger on TQ3 due to higher intrinsic entropy at 3.07 BPW. Symptom: web-search spam on simple prompts, higher latency. | **High** | §3 recalibrate post-launch; optionally set `ODO_CONFIDENCE_DISABLED=1` for first 24h (env gate doesn't exist yet — follow-up). |
| R3 | odo still points at `ODO_BACKEND=http://127.0.0.1:8081` (`odo.py:63`). If APEX chimere-server is stopped but odo isn't updated, ALL requests 500. | **High** | Explicit cut-over: either keep APEX on 8081 AND TQ3 on 8083 (coexist), or `systemctl --user edit odo.service` adding `Environment=ODO_BACKEND=http://127.0.0.1:8083`. |
| R4 | Same for `CHIMERE_BACKEND` in `confidence_rag_trigger.py:32` and `dvts.py:32` and `quality_gate.py:32` — **three** files use this env. Missing one → broken probe. | **Medium** | Set `CHIMERE_BACKEND` in `odo.service` env block (single source). |
| R5 | Loss of FFI Engram (chimere-server not in path). Silent quality drop, no error. | **Medium** | Option (a) accepted in §4; monitor via user feedback 48h. |
| R6 | Disk: TQ3 12.4 GB + APEX 22 GB + mmproj + chroma (109 MB) + engram (21 MB) + chromadb snapshot (≈110 MB). Current free: **420 GB / 915 GB** (52% used). Plenty of margin. | **Low** | No action. |
| R7 | Embedder CPU load (Qwen3-Embedding-0.6B, CPU, ~14 threads available, TQ3 uses `-t 14` per service file) — embedder and TQ3 threadpool will fight if `knowledge-rag-index` runs concurrently with TQ3 generation. | **Medium** | §6.4 timer stop; long-term pin embedder to `taskset -c 0-3`. |
| R8 | ChromaDB has **no** PID lock file (verified: no `*.pid`, no `*.lock` in dir). Concurrent writers rely on SQLite locking only. If a query segfaults mid-write, WAL may be left in an inconsistent state. | **Low** | §1 snapshot is the backstop. |
| R9 | `knowledge_rag_query.py` contains **zero** backend reference (Grep returned nothing) — i.e. pure retrieval, no LLM call. Good: migration-inert. | n/a | No action. Confirmed by Grep on `/home/remondiere/.openclaw/bin/knowledge_rag_query.py` for `8081|8083|BACKEND|engram|rerank|CrossEncoder`: 0 hits. |
| R10 | The APEX tokenizer bug (per `chimere_apex_tokenizer_fix_2026-04-23.md`) applied a fix that re-tokenizes ingested RAG chunks at generation time. TQ3 via plain `llama-server` uses its own tokenizer from the GGUF — if the TQ3 GGUF embeds a *different* tokenizer version, retrieved chunks may tokenize with subtle whitespace differences. | **Low-medium** | Sanity: `llama-gguf ~/.../Qwen3.6-35B-A3B-TQ3_4S.gguf | grep -i tokenizer` after launch. Not blocking. |

---

## 8. Top-3 pre-launch actions (ordered)

1. **Snapshot ChromaDB** (§1). One command, 2 s, full rollback insurance.
2. **Stop `knowledge-rag-index.timer` and `engram-write-nightly.timer`** (§6.4) — eliminates R1 and R7.
3. **Decide backend cut-over strategy** (§7/R3): coexist (keep both APEX 8081 + TQ3 8083, odo stays on APEX) OR hard cut (edit odo.service with `ODO_BACKEND=http://127.0.0.1:8083` + `CHIMERE_BACKEND=http://127.0.0.1:8083`). Coexist is lower-risk. Write the decision down in the migration doc before starting the service.

## 9. Post-launch checklist (TODO-POST)

- [ ] `curl http://127.0.0.1:8083/health`
- [ ] Tokenizer parity check (R10 command)
- [ ] Confidence threshold calibration (§3)
- [ ] Restart `knowledge-rag-index.timer` and `engram-write-nightly.timer`
- [ ] 48 h user-feedback watch for FFI Engram loss (R5)
- [ ] If stable: plan option (b) sprint (chimere-server rebuilt against turbo-tan libllama)

---

## References

- `~/.openclaw/bin/knowledge_search.py` — lexical markdown search (migration-inert)
- `~/.openclaw/bin/knowledge_rag_build.py:26,175` — embedder definition
- `~/.openclaw/bin/knowledge_rag_query.py` — retrieval (no LLM dependency)
- `~/.openclaw/odo/odo.py:63` — `ODO_BACKEND` env
- `~/.openclaw/odo/confidence_rag_trigger.py:32,142-167` — `CHIMERE_BACKEND`, entropy thresholds
- `~/.openclaw/odo/{quality_gate,dvts}.py:32` — additional `CHIMERE_BACKEND` / `ODO_BACKEND` refs
- `~/.config/systemd/user/qwen-tq3.service` — new service, port 8083
- `~/.config/systemd/user/knowledge-rag-index.service` — ingest pipeline timer
- `~/crossed-cosmos/docs/chimere_tq3_migration.md` — umbrella migration doc
- `~/crossed-cosmos/docs/chimere_apex_tokenizer_fix_2026-04-23.md` — tokenizer post-mortem
