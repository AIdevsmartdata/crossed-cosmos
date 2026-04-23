# Runtime Settings Deep Tuning — qwen-tq3.service (turbo-tan fork)

**Binary.** `/home/remondiere/github-repos/llama.cpp-tq3/build_sm120/bin/llama-server`
Version `1 (794c5dc)`, GNU 13.3.0, CUDA 12.8, sm_120.
**Host.** RTX 5060 Ti 16 GB (15850 MiB), i5-14600KF (20 threads = 6P HT + 8E), 32 GB DDR5.
**Model.** Qwen3.6-35B-A3B-TQ3_4S (3.07 BPW MoE, 2-bit experts / 4-bit attn), mmproj BF16 CPU.
**Current state.** VRAM 13.4 GB used / 2.5 GB free; 99–102 tok/s TG.

Help dump: 569 lines, `/tmp/llama_help_full.txt`. Categorised below.

---

## 1. Flag inventory (by category)

### (a) Sampling
`--samplers` (ordered chain; default
`penalties;dry;top_n_sigma;top_k;typ_p;top_p;min_p;xtc;temperature`),
`--sampling-seq` (compact), `--temp`, `--top-k`, `--top-p`, `--min-p`,
`--top-n-sigma`, `--typical`, `--xtc-probability`, `--xtc-threshold`,
`--dry-multiplier`, `--dry-base`, `--dry-allowed-length`,
`--dry-penalty-last-n`, `--dry-sequence-breaker`,
`--mirostat N`, `--mirostat-lr`, `--mirostat-ent`,
`--repeat-penalty`, `--repeat-last-n`, `--presence-penalty`,
`--frequency-penalty`, `--penalize-nl`, `--logit-bias`, `--seed`.

### (b) Cache / memory
`-ctk/-ctv`, `-ctkd/-ctvd` (draft), `--cache-reuse N` (KV-shift reuse),
`-cram/--cache-ram N` (MiB; default 8192), `-kvu/--kv-unified`,
`--clear-idle`, `-ctxcp/--ctx-checkpoints`, `--swa-full`,
`--mlock`, `--no-mmap`, `--defrag-thold` (DEPRECATED),
`--slot-save-path`, `-sps/--slot-prompt-similarity`,
`-fit` (auto fit), `-margin`, `--op-offload`.

### (c) Batching / threading
`-b/--batch-size` (logical, default 2048), `-ub/--ubatch-size` (phys, 512),
`-np/--parallel N` (slots), `-cb/--cont-batching`,
`-t/--threads`, `-tb/--threads-batch`,
`-C/--cpu-mask`, `-Cr/--cpu-range`, `--cpu-strict`, `--prio` (0–3),
`--poll` (0–100), `-Cb/-Crb/--prio-batch/--poll-batch`.

### (d) Flash Attention
`-fa [on|off|auto]` only. **No `-fa 2`, no Kimi-Linear, no FA-variant selector in this fork.**
FA kernel auto-dispatches per compute cap (sm_120 gets the Ampere+ path).

### (e) Speculative decoding — **two paths**
1. **Model-draft** (classic): `-md/--model-draft`, `--draft-max` (16),
   `--draft-min`, `--draft-p-min` (0.75), `-cd/--ctx-size-draft`,
   `-ngld`, `-devd`, `-td/-tbd`, `-ctkd/-ctvd`, `-otd`, `-cmoed/-ncmoed`,
   `--spec-replace`, `-hfd/--hf-repo-draft`.
2. **Model-less ngram** (*zero VRAM*): `--spec-type`
   `{none|ngram-cache|ngram-simple|ngram-map-k|ngram-map-k4v|ngram-mod}`,
   `--spec-ngram-size-n`, `--spec-ngram-size-m` (default 48),
   `--spec-ngram-min-hits`.
3. Presets: `--fim-qwen-7b-spec`, `--fim-qwen-14b-spec`.

### (f) Tool-calling / reasoning
`--reasoning-format {none|deepseek|...}` (current `deepseek`),
`-rea/--reasoning [on|off|auto]`, `--reasoning-budget N` (cap think tokens),
`--reasoning-budget-message`,
`--chat-template-kwargs` (JSON, e.g. `{"enable_thinking":false}`),
forced pure-content parser flag (line 495).

### (g) Jinja / chat template
`--jinja/--no-jinja`, `--chat-template JINJA_TEMPLATE`,
`--chat-template-file PATH`, `--chat-template-kwargs`.

### (h) Other
`--metrics` (Prometheus), `--slots`, `--embedding`, `--pooling`,
`--grammar`, `--grammar-file`, `--json-schema`, `--json-schema-file`,
`-ngl`, `-ncmoe`, `-cmoe`, `-ot/--override-tensor`, `-sm/--split-mode`,
`-mg`, `-dev`, `--host`, `--port`, `--api-key`, `--log-file`,
`--log-colors`, `--log-timestamps`, `--log-prefix`, `-v/-lv`.

---

## 2. Flag-level audit — current vs recommended

| # | Flag | Current | Recommended / Test | Rationale |
|---|------|---------|-------------------|-----------|
|  1 | `-fa` | `on` | keep `on` | No FA2/linear variant exposed in this build. Already optimal. |
|  2 | `-ctk` | `q4_0` | **A/B** `q8_0` | K is most error-sensitive. Δ ≈ +200 MB at 64 K ctx; likely +quality, ≤2 % TG cost. |
|  3 | `-ctv` | `tq3_0` | keep; also A/B `q4_0` | `tq3_0` is TurboQuant V-only codec — saves ~40 % vs `q4_0`. Headroom-driven. |
|  4 | `-c` | `65536` | keep | Qwen3.6 native 256K gated; 64 K is the sane cap for 16 GB. |
|  5 | `-np` | `1` | keep for interactive | `-np 2` halves per-slot ctx. Not worth it for OpenClaw/odo single-user. |
|  6 | `-b` | `4096` | **test `8192`** | Long-prompt prefill (RAG ingest) is compute-bound; bigger logical batch → faster PP on 2k-token prompts. |
|  7 | `-ub` | `512` | **test `1024` then `2048`** | sm_120 has slack; Mar-5 IQ3_S benchmark showed `-ub 2048` SEGV *on ik_llama*, stock/turbo-tan path is safer. |
|  8 | `-t / -tb` | `14/14` | **sweep 6,10,14,20; split `-t 10 -tb 20`** | 6P+HT = 12 strong threads; gen is latency-bound on P-cores only, prefill benefits from all 20. Expect +3–6 % TG at `-t 10`, +10 % PP at `-tb 20`. |
|  9 | `--prio` | default(0) | **`--prio 2`** (batch `--prio-batch 2`) | "high" nice for llama-server only, no effect on desktop responsiveness because P-cores already oversubscribed. |
| 10 | `--poll` | 50 | test `100` | Busy-poll worker wakeup — +1-2 % TG at ~5 % extra CPU idle. |
| 11 | `--cpu-mask` | none | **`-C 0xFFF`** (pin to 12 P-HT threads) | Stops migration to E-cores mid-gen. |
| 12 | Sampling (svc defaults) | no-think `0.7/0.8/20/0` | keep as service default, **force odo to override per-route** | Matches Qwen3 official no-think. Think overrides (1.0/0.95/20/0) done by odo — confirmed OK. |
| 13 | `--samplers` | default chain | keep (`penalties;dry;top_n_sigma;top_k;typ_p;top_p;min_p;xtc;temperature`) | Already DRY-before-temp, which is correct. |
| 14 | `--dry-multiplier` | 0 | **`0.8` for code route, 0 default** | Penrose DRY 0.8/1.75/2 is the canonical anti-loop config. chimere-server Rust FFI uses DRY; parity at the HTTP layer. |
| 15 | `--dry-base` | 1.75 | 1.75 (canonical) | |
| 16 | `--dry-allowed-length` | 2 | 2 | |
| 17 | `--dry-penalty-last-n` | -1 (=ctx) | keep | |
| 18 | `--dry-sequence-breaker` | default | add `\n`, ``` ``` ``` for code | Avoid penalising legitimate code repetition. |
| 19 | `--xtc-probability` | 0 | stays 0 for code/tools; optional 0.2 for creative routes | XTC + tool-JSON = corruption risk. |
| 20 | `--top-n-sigma` | 0 | keep | Qwen3 not tuned for it. |
| 21 | `--mirostat` | 0 | **never enable** | Disables top-k/top-p; incompatible with Qwen3 sampling matrix. |
| 22 | `--reasoning-format` | `deepseek` | **keep for reasoning routes, add `none` variant on 8085** for tool-heavy (MEMORY warning confirmed). | Split endpoint or per-request `--chat-template-kwargs`. |
| 23 | `-rea` | unset(=auto) | explicit `-rea auto` | cosmetic; makes intent in unit file. |
| 24 | `--reasoning-budget` | -1 | test `4096` cap | Prevents think-block overflow observed in odo logs. |
| 25 | `--jinja` | on | keep | Required for Qwen3.6 `{% generation %}` blocks. |
| 26 | `--chat-template-file` | unset (GGUF embedded) | **extract + inspect** via `llama-gguf` → decide. Likely keep embedded. | Embedded template is usually upstream-blessed; override only if we want a *tool-call-pre-formatted* variant. |
| 27 | `--chat-template-kwargs` | unset | per-request via odo | Already covered. |
| 28 | `--cache-reuse` | default (256?) | **test `128`** | Long multi-turn convos benefit from smaller reuse chunks (more hits). |
| 29 | `-cram` | 8192 | bump to `16384` | RAM-backed slot cache; we have 22 GB free. |
| 30 | `-kvu/--kv-unified` | unset (auto) | explicit `--kv-unified` with `-np 1` | Simpler memory, allows `--clear-idle`. |
| 31 | `--slot-save-path` | unset | **set** `~/.openclaw/cache/tq3-slots/` | Persist KV across service restart → instant resume of long sessions. |
| 32 | `-sps/--slot-prompt-similarity` | 0.10 | test `0.25` for odo-style repeated system prompts | More aggressive slot reuse. |
| 33 | `--metrics` | on | keep | Prometheus. |
| 34 | `--slots` | on (default) | keep | odo uses `/stats`. |
| 35 | `--embedding` | off | **leave off** | TQ3_4S is generative; embedding quality << Qwen3-Embedding-0.6B. Not worth the pool-mode switch. |
| 36 | `--log-timestamps` | off | **on** | Journald correlation. |
| 37 | `--log-prefix` | off | on | Structured journal parsing. |
| 38 | Speculative (classic) | off | **HIGH-PRIORITY A/B** `-md Qwen3-1.7B-Q4_K_M.gguf -ngld 99 --draft-max 8 --draft-p-min 0.8 -ctkd q4_0 -ctvd q4_0 -cd 8192` | ~1.2 GB VRAM cost, fits in 2.5 GB headroom. Expected 1.5–2.5× TG on code, 1.2–1.7× on prose (MoE verifier + dense draft family-match). 3–6× claim in prompt is optimistic for Qwen MoE (experts limit accept rate); realistic 1.8× median. |
| 39 | Speculative (ngram) | off | **zero-cost A/B** `--spec-type ngram-map-k4v --spec-ngram-min-hits 1` | No VRAM, no draft model. +20–40 % TG on repetitive outputs (code, JSON, tables). Keep as fallback if model-draft OOMs. |
| 40 | `--grammar-file` | unset | reserve for tool-call JSON enforcement via odo. | Per-request not service-level. |
| 41 | `--logit-bias` | unset | none at service level | Per-route via odo. |
| 42 | `-ncmoe` | unset | keep unset (TQ3 fits fully offloaded `-ngl 99`) | Offloading experts to CPU would kill 100 tok/s. |

---

## 3. Jinja template inspection

Embedded template lives in GGUF `tokenizer.chat_template`. Extract with:

```bash
~/github-repos/llama.cpp-tq3/build_sm120/bin/llama-gguf \
  ~/.openclaw/models/Qwen3.6-35B-A3B-TQ3_4S/Qwen3.6-35B-A3B-TQ3_4S.gguf r \
  | grep -A 200 chat_template
```

Decision tree:
- If template === upstream Unsloth Qwen3.6 → **keep**.
- If it lacks `{% generation %}` / tool_call_id role mapping → **override** with a custom file based on Qwen3.5 Jinja already battle-tested in think_router.
- **Known pitfall (MEMORY)**: Qwen3.5 template accepts only `system|user|assistant|tool`. Qwen3.6 likely same; odo already sanitises.

---

## 4. Benchmark matrix

Driver: `llama-bench` + a 256-prompt OpenClaw replay set (mix: 40 % code, 30 % tool-calls, 30 % prose).
Metrics: PP tok/s, TG tok/s, VRAM peak, tool-call accept rate (`tau3` subset, 10 retail tasks), KLD vs fp16 reference (opt).

| Axis | Values | Baseline | Realistic Δ TG |
|---|---|---|---|
| `-ctk` | q4_0 / q8_0 | q4_0 | -2 % TG, +quality, +200 MB |
| `-ub` | 512 / 1024 / 2048 | 512 | +3-8 % PP, 0 TG |
| `-b` | 4096 / 8192 | 4096 | +5-10 % PP on >4 K prompts |
| threads | `-t 6/10/14/20`, `-tb 14/20` | 14/14 | up to +5 % TG at 10, +8 % PP at 20 |
| `--prio/--poll` | 2 / 100 | 0 / 50 | +1-3 % TG |
| ngram spec | off / map-k4v / mod | off | **+20-40 % TG on code** |
| model-draft | off / Qwen3-1.7B Q4 | off | **+80-150 % TG on code**, +20-60 % prose |
| DRY | off / 0.8-1.75-2 | off | 0 TG, quality↑ on long code |
| `--reasoning-format` | deepseek / none | deepseek | tool-call accept +10-20 pts when `none` on tool routes |

---

## 5. Prioritised action plan

**P0 — free lunches, deploy now (no risk):**
1. `--log-timestamps --log-prefix`.
2. `--prio 2 --prio-batch 2 --poll 100`.
3. `-cram 16384`.
4. `--slot-save-path ~/.openclaw/cache/tq3-slots/`.
5. Explicit `-rea auto --reasoning-budget 4096`.

**P1 — measure-then-ship (1 evening of benching):**
6. `-ctk q8_0` (quality, small VRAM cost).
7. `-ub 1024`, `-b 8192` (PP gains on long RAG contexts).
8. Threading sweep → pick winner; add `-C 0xFFFFF` pin.
9. `--spec-type ngram-map-k4v --spec-ngram-min-hits 1` — zero-VRAM 20–40 % freebie on code/JSON.

**P2 — high-impact, needs VRAM budgeting (1 day):**
10. Classic speculative decoding with Qwen3-1.7B Q4_K_M drafter. Validate
    VRAM fit (draft ~1.2 GB → leaves ~1.3 GB margin). If OOM with `-ub 1024`,
    fall back to `-ub 512` while keeping speculative.
11. Service-level DRY for code route (via odo `chat_template_kwargs` passthrough or a second unit on port 8086 with `--dry-multiplier 0.8`).

**P3 — optional / per-route via odo:**
12. Per-route `--reasoning-format none` for tool-heavy calls (tau3-bench confirmed the deepseek-breaks-tools finding).
13. Grammar / JSON-schema enforcement for tool call endpoints.
14. Template extraction + custom override if embedded is suboptimal.

---

## 6. A/B protocol (concrete)

1. Snapshot baseline: `llama-bench -m … -ngl 99 -fa 1 -ctk q4_0 -ctv tq3_0 -p 512,2048 -n 256 -r 5 -ub 512 -b 4096 -t 14`.
2. Change **one axis** per run. 5 repetitions, discard first (warmup).
3. Tool-call sanity on each winner: 10 retail tau3 tasks (odo logs → accept rate, schema compliance).
4. Promote winner into a `qwen-tq3-next.service` unit on port 8087 (drop-in);
   run 48 h parallel to 8083 under odo canary (10 % traffic).
5. If no regression (TG ≥ baseline, tool accept ≥ 80 %, no OOM), flip odo
   backend to 8087, retire 8083.

---

## 7. ik_llama feature parity notes

ik_llama.cpp (port 8082 tests) exposes **beyond** turbo-tan:
- `-rtr` (runtime repacking), `-mla` / `-amb` (attention), `-fmoe` (fused MoE),
  `-ser`, `-khad` (Hadamard-transformed KV).
None are TQ3-compatible today (TurboQuant codec absent from ik). Not portable
without substantial backport work (cf. `ik-llama-iq3xxs-ssm-out-bug.md`).
Flag that `-khad` on KV cache is the single most interesting future port
(beats tq3_0 quality/size tradeoff) — track upstream PR #21089.

**End of plan.**
