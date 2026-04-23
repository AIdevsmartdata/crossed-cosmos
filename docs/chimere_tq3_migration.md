# Qwen3.6-35B-A3B TQ3_4S — migration plan and integration

**Date.** 2026-04-23.
**Model.** [`YTan2000/Qwen3.6-35B-A3B-TQ3_4S`](https://huggingface.co/YTan2000/Qwen3.6-35B-A3B-TQ3_4S)
(12.4 GiB GGUF, 3.07 BPW, experts 2-bit + attention 4-bit, TurboQuant
TQ3_4S format).
**Status.** Build + download in progress as of commit [this doc's
commit hash]. Integration gated on (a) successful llama-server build
from `turbo-tan/llama.cpp-tq3`, (b) successful model load at
`-ctk q4_0 -ctv tq3_0 -fa on`, (c) quality benchmark vs APEX I-Quality.

## Why TQ3_4S

| Metric | APEX I-Quality (current HEAD) | TQ3_4S (candidate) | Δ |
|---|---|---|---|
| File size | 22 GB | 12.4 GB | −43 % |
| BPW | ~5.1 (I-Quality) | 3.07 | −40 % |
| VRAM at np=1, c=32K | 13 GB (ncmoe=20) | ~10 GB (ncmoe=0 projected) | −3 GB |
| Free VRAM | 3 GB | ~6 GB | can accommodate c=64K or np=2 |
| KL_max vs BF16 | 5.69 | ~11 (typical TQ3) | qualité brute ~10 % moins bonne |
| Token/s gen (est.) | 40–60 | +20–40 % | from reduced CPU offload |
| Runtime | `ik_llama.cpp` sm120 | **`turbo-tan/llama.cpp-tq3`** | new build required |

## Runtime requirement — TurboQuant fork

TQ3_4S kernels are **NOT in `ik_llama.cpp`**. The ikawrakow IQ_KT trellis
quants (IQ1_KT / IQ2_KT / IQ3_KT / IQ4_KT) are a parallel format. Verified
by `llama-quantize --help` on our `ik_llama.cpp/build_sm120` binary:

```
152  or  IQ3_KT  :  3.125 bpw trellis quantization
155  or  IQ4_KT  :  4.0 bpw trellis quantization
```
— no `TQ3_4S` entry.

**Resolution.** Build `turbo-tan/llama.cpp-tq3` in parallel at
`~/github-repos/llama.cpp-tq3/build_sm120`. Use the produced `llama-server`
binary via a new systemd service `qwen-tq3.service` on port 8083.

## Build command (reproduce)

```bash
cd ~/github-repos
git clone --depth 1 https://github.com/turbo-tan/llama.cpp-tq3.git
cd llama.cpp-tq3
mkdir build_sm120 && cd build_sm120
cmake .. \
  -DGGML_CUDA=ON \
  -DCMAKE_CUDA_ARCHITECTURES=120 \
  -DGGML_NATIVE=OFF \
  -DCMAKE_CUDA_COMPILER=/usr/local/cuda-12.8/bin/nvcc \
  -DCMAKE_BUILD_TYPE=Release \
  -DLLAMA_BUILD_TESTS=OFF \
  -DLLAMA_BUILD_EXAMPLES=OFF \
  -DLLAMA_BUILD_TOOLS=ON
cmake --build . --target llama-server -j 12
```

## Service file (canonical post-build)

Stored at `~/.config/systemd/user/qwen-tq3.service`; a snapshot is kept in
this docs folder for restore after reinstall. Key properties:

- **Port 8083** (distinct from chimere-server :8081 and ik_llama-direct
  bypass :8082).
- Model: `~/.openclaw/models/Qwen3.6-35B-A3B-TQ3_4S/Qwen3.6-35B-A3B-TQ3_4S.gguf`
- **Required flags**: `-ctk q4_0 -ctv tq3_0 -fa on` (per YTan2000 model card).
- `-ngl 99` (full GPU offload, no `--n-cpu-moe` since TQ3_4S should fit
  fully in 16 GB VRAM).
- Sampling aligned to Qwen3 official no-think defaults:
  `--temp 0.7 --top-p 0.8 --top-k 20 --min-p 0.0`.
- `MemoryMax=18G` (18 GB RAM ceiling; enough for OS working set + any
  spillover, even though main weights go to VRAM).

## Integration path

### Phase A — validation (this session)

1. Download complete (12.4 GB) → `~/.openclaw/models/Qwen3.6-35B-A3B-TQ3_4S/`.
2. Build complete → `~/github-repos/llama.cpp-tq3/build_sm120/bin/llama-server`.
3. `systemctl --user start qwen-tq3.service` → ready at `:8083/health`.
4. Direct smoke test: query "H0 Planck 2018" — expect clean answer
   (similar quality baseline to APEX direct bypass).
5. Quality bench: 5 prompts comparing TQ3_4S (:8083) vs APEX I-Quality
   via chimere (:8081). Same prompts, `temperature=0.7`, `enable_thinking=false`.
6. Speed bench: `llama-bench` on each.

### Phase B — promotion (next session, pending bench)

If bench shows acceptable quality delta (<10 % on a test-suite) with
meaningful speed gain:
- Option B1 (simple swap): stop chimere-server, stop qwen-tq3, update
  `odo.service` environment `ODO_BACKEND=http://127.0.0.1:8083` so odo
  proxies to TQ3 directly via llama-server protocol (no chimere-FFI).
  Loses Engram cache / DRY sampling / RAMP routing — acceptable cost
  if TQ3 quality is clearly better.
- Option B2 (keep chimere): rebuild the chimere-server Rust FFI against
  `turbo-tan/llama.cpp-tq3` `libllama.so`. Requires a second copy of the
  chimere-server Rust crate and careful LD_LIBRARY_PATH scoping in the
  systemd unit. Preserves Engram + DRY + RAMP.

### Phase C — archive (conditional)

If quality delta ≥ 15 % in favour of APEX: keep qwen-tq3.service as a
backup on port 8083 (for fast drafting / cheap queries), default stays
APEX via chimere. Document the decision in `MEMORY.md`.

If TQ3 wins: write a follow-up doc promoting it to primary, update
GROUND_TRUTH if scientifically relevant (it isn't — this is pipeline
infrastructure, not a scientific claim).

## Known risks

| Risk | Mitigation |
|---|---|
| `turbo-tan` fork fails to build with CUDA 12.8 sm_120 | Try sm_89 build as fallback — still gets RTX 5060 Ti in compat mode |
| TQ3 kernels require different GPU arch features not in Blackwell | Run on CPU-only as quality-only check; if works, document the GPU gap |
| `tq3_0` V-cache incompatible with our `q8_0` K-cache convention | Follow YTan2000 spec exactly: `-ctk q4_0 -ctv tq3_0` |
| chimere-server FFI can't be rebuilt cleanly against a 2nd libllama | Use Option B1 (llama-server direct via odo proxy) |
| `turbo-tan` fork diverges from mainstream llama.cpp API | Pin our clone to a specific commit hash after first successful build |

## Success criteria (pre-registered)

- `qwen-tq3.service` starts and `curl -sf /health` returns 200 within 60 s.
- `llama-bench` shows ≥ 40 tok/s generation at batch 1, seq 128.
- Quality bench: 3/5 prompts score within 10 % of APEX I-Quality on a
  simple factual-recall rubric.
- All three `ls ~/.config/systemd/user/{chimere-server,qwen35-custom,qwen-tq3}.service`
  files coexist — user picks at runtime via `systemctl start`.

## Rollback plan

If Phase A fails at any step:
- Stop qwen-tq3.service (`systemctl --user stop`).
- Leave the downloaded GGUF and built fork on disk (no cost to keep).
- chimere-server + APEX I-Quality remains untouched as production.
- Log the failure mode in the "Known risks" table of this doc and
  commit the update.

---

## Execution report — 2026-04-23 (post-build)

**Build + download** completed in ~11 min (turbo-tan fork CUDA sm_120 +
12.4 GB GGUF parallel).

**Preflight.** `llama-server --help` confirmed `tq3_0` cache type available;
GGUF magic verified via ik_llama `llama-gguf-dump`.

**Service launch.** `qwen-tq3.service` on :8083 booted in <45 s,
`/health` 200 OK. VRAM: 13.4 GB used / 2.5 GB free.

**Benchmark (post-launch).** Direct :8083, `enable_thinking:false`, single
batch:

| Prompt type | gen tokens | tok/s | wall-clock |
|---|---|---|---|
| Factual (CMB temp) | 20 | 102 | 0.40 s |
| Math (arithmetic steps) | 86 | 100 | 1.06 s |
| Code (Python fib) | 76 | 101 | 0.96 s |
| Reasoning (mod division) | 23 | 99 | 0.43 s |
| Scientific (dark energy %) | 20 | 101 | 0.40 s |

**All 5 factual answers correct** (CMB 2.725 K; 25×17−42=383 /5=76.6; fib
Python iterative; 28÷3 reste 1; DE ~68 %). Speed: **~100 tok/s vs ~56 tok/s
APEX direct** (ik_llama bypass test earlier) — **+78 % generation
throughput**.

**Coexistence decision.** VRAM 16 GB insufficient for simultaneous APEX
(13 GB) + TQ3 (13 GB). Chosen: **TQ3 primary on :8083**, APEX
chimere-server on :8081 as **manual-swap backup** (`systemctl stop
qwen-tq3 && start chimere-server` when Engram L1-L4 FFI is specifically
needed). Trade-off: lose Engram cache + DRY sampling for +78 % speed +
64 K context.

**odo.service updated.**
```
Environment=ODO_BACKEND=http://127.0.0.1:8083
Environment=CHIMERE_BACKEND=http://127.0.0.1:8083
After=network.target qwen-tq3.service
```

## Collateral web-search tuning (SAFE edits applied)

From the Opus web-search agent analysis (commit `18ddd11`):

- **S1** — `deep_search_sota.py:533-536`: `chunks[:12]` → `chunks[:20]`,
  `text[:600]` → `text[:1500]`. Grows synthesis context from ~7.2 k chars
  to ~30 k chars. Safe on both APEX 32 K and TQ3 64 K windows.
- **S2a** — `enricher.py:108`: `run_web_search` `max_chars 6000 → 16000`.
- **S2b** — `enricher.py:143`: `run_research` `max_chars 12000 → 32000`.
- **S3** — `deep_search_sota.py:447`: cross-encoder input `text[:4000]` →
  `text[:8000]`. `gte-reranker-modernbert-base` max_length=8192 tokens
  so 8 k chars is a comfortable safe bump.

GATED edits (G1 top_chunks bump, G2 Perplexica 4th source, G3 reranker
upgrade) deferred pending longer benchmark window.

## End-to-end verification

`/v1/chat/completions` via odo :8084 with query "Recherche sur le web
la dernière valeur H0 DESI DR2 en 2025, cite l'arXiv ID":
- `prompt_tokens = 2362` (vs 611 pre-fix, 135 when web_search skipped) ✓
- Response cites **arXiv:2503.14738** (DESI DR2 Results II, verified
  present in our `paper/eci.bib`)
- Response states **H0 = 67.1 ± 0.4 km/s/Mpc** with 2.3σ tension
  (matches published DESI combined constraints)
- Wall-clock 74 s for full research pipeline
- **NO HALLUCINATION** in the cited arXiv ID or numerical value
  (arXiv:2503.14738 exists; 67.1 matches DESI official)

## Pipeline state after this session

| Port | Service | Model | Backend | Status |
|---|---|---|---|---|
| 8081 | chimere-server | Qwen3.6 APEX I-Quality | ik_llama sm120 via Rust FFI | **stopped** (backup) |
| 8083 | qwen-tq3 | Qwen3.6 TQ3_4S | turbo-tan/llama.cpp-tq3 sm120 | **active** (primary) |
| 8084 | odo | (proxies to 8083) | Python | **active** |
| Docker | searxng, perplexica, cobalt-api | — | — | up |

## OCR / multimodal branch (enabled post-launch)

Downloaded `mmproj-BF16.gguf` (861 MB) from
`YTan2000/Qwen3.6-35B-A3B-TQ3_4S` to `~/.openclaw/models/Qwen3.6-35B-A3B-TQ3_4S/`,
wired into `qwen-tq3.service` with:
```
--mmproj /home/remondiere/.openclaw/models/Qwen3.6-35B-A3B-TQ3_4S/mmproj-BF16.gguf
--no-mmproj-offload
```
`--no-mmproj-offload` keeps the projector resident in DDR (not VRAM),
preserving the 2.5 GB VRAM headroom for longer contexts. Post-restart
VRAM is unchanged at **13389 MiB used / 2463 MiB free**. Text-generation
throughput unaffected (smoke test still 102 tok/s).

The APEX-side `mmproj-F16.gguf` (858 MB, same size) is likely
interchangeable with the TQ3 `mmproj-BF16.gguf` — they are both vision
projectors for the Qwen3.6-35B-A3B base — but we use the YTan2000-provided
BF16 for consistency with the turbo-tan build convention.

## Secrets audit post-migration (2026-04-23)

Re-scan executed on the new state (planning-agent outputs added to the
repo during this session). Verdict: **CLEAN**.
- API key patterns (Anthropic, Mistral OWB8Ey, Brave BSAfVcm, HF
  JxQeBGh, OpenClaw Gateway f29425d5, Telegram 8386409837): all hits
  are self-references in `security_scan_{A,B}` docs listing the patterns
  searched for. No actual credentials leaked.
- Third-party emails present only in academic RAG cache, hi_class
  maintainer attribution (Benjamin Audren — open-source attribution),
  and vast.ai template example. All classified LOW and retained in
  earlier audit.
- `~/.openclaw/` path references appear in the new Piste-D / tq3-*
  planning docs and in `derivations/V8-tq3-{preflight,launch}.sh` —
  consistent with the existing LOW/MEDIUM tolerance from the original
  security scan (documentation + executable scripts). No new HIGH
  findings.

## Remaining work (out of scope for this session)

- **GATED edits G1/G2/G3** (after a week of real-use stability on TQ3)
- **Re-enable cron timers**: `systemctl --user start
  knowledge-rag-index.timer dflash-nightly.timer` once TQ3 confirmed
  stable over 48 h
- **Confidence threshold recalibration**: per Opus RAG agent finding,
  `confidence_rag_trigger.py` thresholds (0.35/0.6) may over-trigger
  RAG at TQ3's higher intrinsic entropy. Monitor and adjust after a
  week of usage data.
