# TQ3 / chimere-server Rust FFI Rebuild Strategy

**Date:** 2026-04-22
**Question:** Rebuild chimere-server against `turbo-tan/llama.cpp-tq3` libllama.so (B2), bypass it entirely (B1), or run a hybrid stack?
**Verdict up front:** **Hybrid (option 7)** for the migration window. B2 is feasible but not free; B1 is free but costly in lost features.

---

## 1. Evidence — chimere-server FFI anatomy

Files inspected (all absolute paths):

- `/home/remondiere/github-repos/chimere/chimere-server/Cargo.toml` (L15): depends on local crate `ggml-ffi = { path = "ffi" }`. Single binary target `chimere-server` (L30-32).
- `/home/remondiere/github-repos/chimere/chimere-server/build.rs` (L86-111): hardcodes `{IKLLAMACPP_DIR}/build_sm120/src` and `/ggml/src` as link search paths; `rustc-link-lib=dylib=llama` and `=ggml`; sets rpath to the ik_llama build directory. Placeholder `{IKLLAMACPP_DIR}` is resolved at build time from env (the installed build uses `/home/remondiere/ik_llama.cpp`).
- `/home/remondiere/github-repos/chimere/chimere-server/ffi/build.rs` (L45-72): compiles `chimere_sampler.cpp` with **include dirs pointing into ik_llama private headers** (`{IKLLAMACPP_DIR}/src` for `llama-grammar.h`, `/common` for `common.h`) and statically links `libcommon.a` from `build_sm120/common`.
- `/home/remondiere/github-repos/chimere/chimere-server/ffi/build.rs` (L102-108): nvcc compiles `ggml_cuda_gemv.cu` with `-I{ggml_src_dir}/ggml-cuda`, i.e. against ik_llama's private CUDA kernel headers.
- `/home/remondiere/github-repos/chimere/chimere-server/src/llama_backend.rs` (L257-357): Rust `extern "C"` block declaring **~45 llama_* symbols** plus an MTP subset (L354-357).
- `/home/remondiere/github-repos/chimere/chimere-server/ffi/chimere_sampler.cpp` (L44-231): thin wrapper around `common_sampler_init / _sample / _accept / _reset / _free / _get_candidates` from `common/sampling.h`.
- `/home/remondiere/github-repos/chimere/chimere-server/src/engram.rs` (799 LOC) and `engram_lookup.rs` (1452 LOC): **zero `extern "C"`, zero mention of `libllama` or `ik_llama`**. Pure Rust. Confirmed by grep (match count 0).

## 2. ABI diff — ik_llama vs turbo-tan

Raw diff `include/llama.h`: **1858 lines** of divergence (1594 turbo-tan vs 1529 ik_llama lines total).

### 2a. Core API: compatible

ik_llama has **already absorbed** the mainline late-2025 rename. Both headers export:

| Symbol used by chimere FFI (`llama_backend.rs`) | ik_llama | turbo-tan |
|---|---|---|
| `llama_model_load_from_file` | yes | yes |
| `llama_init_from_model` | yes | yes |
| `llama_vocab_n_tokens` | yes | yes |
| `llama_model_get_vocab`, `llama_free_model`, `llama_free`, `llama_decode`, `llama_get_logits_ith`, `llama_batch_get_one`, `llama_batch_init/free`, `llama_kv_cache_clear`, `llama_tokenize`, `llama_token_to_piece`, `llama_chat_apply_template`, `llama_model_chat_template`, `llama_state_seq_get_size/data/set_data`, `llama_get_embeddings`, `llama_model_is_hybrid/recurrent`, `llama_backend_init/free`, `llama_*_default_params` | yes | yes |

Of the ~45 `llama_*` symbols in `llama_backend.rs:257-357`, the vast majority resolve identically.

### 2b. Core API: **4 symbols are ik_llama-only** (MTP speculative decoding)

Confirmed by grep on turbo-tan header (match count 0) and on ik header (4 matches):

- `llama_set_mtp_op_type` (ik `llama.h`, used `llama_backend.rs:355`)
- `llama_set_draft_input_hidden_state` (ik, used L356)
- `llama_model_n_nextn_layer` (ik, used L354)
- `llama_model_has_recurrent` — actually present in ik, but turbo-tan uses a different name. grep: 0 matches in turbo-tan. `llama_backend.rs:343` calls it.

These are **ik_llama's MTP extensions**. They do not exist in turbo-tan mainline. On Qwen3.5 (non-MTP model) they are currently runtime no-ops or probed via `llama_model_n_nextn_layer() == 0` guards, but the **symbol must still resolve at link time**. Under turbo-tan, the final `cargo build --release` will fail with `undefined reference` unless these 4 call sites are `#[cfg]`-gated out.

### 2c. common_sampler API: **signature drift**

- ik_llama `common/sampling.h`: `common_sampler_accept(smpl, llama_context*, token, accept_grammar)` (4 args).
- turbo-tan `common/sampling.h:45`: `common_sampler_accept(smpl, token, accept_grammar)` (3 args).

`chimere_sampler.cpp:67` uses the 4-arg form. Rebuild against turbo-tan's `libcommon.a` would fail to compile.

Other `common_sampler_*` used (init/sample/reset/free/get_candidates) appear signature-compatible — but this requires verification on each call site.

### 2d. ggml-cuda private headers: divergent

`/home/remondiere/github-repos/chimere/chimere-server/ffi/ggml_cuda_gemv.cu` (463 LOC) `#include`s files from `ggml/src/ggml-cuda/` (e.g. `mmvq.cuh`, `convert.cuh`) — these are **not a stable API**. Between ik_llama and turbo-tan the `ggml-cuda/` directory contents differ (e.g. turbo-tan has `add-id.cu`, `cumsum.cu`, `cp-async.cuh`, `cpy-utils.cuh`, `argmax.cu`; ik has some of these, missing others). Rebuilding under turbo-tan is **likely to fail until the .cu wrapper is ported**.

### 2e. ftype IDs: diverge on TQ quants (expected)

turbo-tan: `TQ3_0=200, TQ3_1S=43, TQ3_4S=45` (the whole point of the fork).
ik_llama: classical `TQ1_0=36, TQ2_0=37` plus deleted Q4_0_X_Y slots.

Not an FFI issue — chimere's Rust code does not enumerate ftype.

## 3. Engram preservation

Verified: `engram.rs` and `engram_lookup.rs` contain zero llama-FFI references (grep count 0 for `ik_llama|libllama|llama_backend|extern "C"` across both files, 2251 LOC total). L1-L4 memory including FHRR hash table is entirely pure-Rust on top of safetensors + memmap2. **Any rebuild preserves Engram automatically.**

## 4. Option analysis

### B1 — Simple swap (odo → turbo-tan llama-server on 8083, bypass chimere)

- Effort: **0.5 h** (write systemd unit for turbo-tan `llama-server`, add odo pipeline variant).
- Risk: **low**.
- Loses: Engram L1-L4, DRY sampling, RAMP tensor-type routing, TTS/vision hooks, `common_sampler` integration. Everything that makes chimere-server *chimere*.
- When justified: TQ3 model only used for narrow "speed" routes.

### B2 — Full rebuild of chimere-server FFI against turbo-tan

Required patches:

1. **Gate MTP symbols** (`llama_backend.rs:354-357`) behind `#[cfg(feature = "ik_llama_mtp")]`. ~15 LOC + Cargo.toml feature flag. Caller paths (`mtp_scheduler.rs`) must also be feature-gated.
2. **Port `chimere_sampler.cpp:67`** — drop the `lctx` argument from the `common_sampler_accept` call. 1-line change.
3. **Audit other `common_sampler_*` signatures** in turbo-tan (init, sample, get_candidates, free, reset). Probably all compatible — but must read turbo-tan's `sampling.h` fully (expected 30 min).
4. **Port `ggml_cuda_gemv.cu`** — replace ik_llama ggml-cuda internal header includes with turbo-tan equivalents. Symbols like `mul_mat_vec_q_cuda<IQ3_S>` may have renamed template parameters. Expected 2-4 h of mechanical porting + one CUDA rebuild cycle to surface each compile error.
5. **Retarget link paths** in both `build.rs` files — trivial (`LIBLLAMA_DIR` env var + conditional).
6. **libggml.so symbol surface**: turbo-tan's libggml exports IQ3_S quant functions identically (they come from upstream llama.cpp and have not been renamed). Low risk.

Total: **4-8 hours** of careful work, with two risks:
- The ggml-cuda header port could cascade if turbo-tan refactored the CUDA wrapper internals (possible — it tracks mainline more aggressively).
- Engram + DRY sampling themselves are preserved; only the plumbing changes.

Gain: **full feature parity with TQ3 backend**. Engram + DRY + RAMP + TQ3 quality all in one binary.

**Proposed invocation** (once turbo-tan libs are built):

```bash
export IKLLAMACPP_DIR=/home/remondiere/github-repos/llama.cpp-tq3
cd /home/remondiere/github-repos/chimere/chimere-server
# Apply patch set 1-4 first (feature-gate MTP, fix sampler_accept arity, port .cu)
cargo build --release --features "server,turbo_tan_backend" \
  --no-default-features
```

Then a **parallel systemd unit** `chimere-server-tq3.service` on port **8082**, with its own `LD_LIBRARY_PATH=.../llama.cpp-tq3/build_sm120/src:.../ggml/src` and rpath baked in by build.rs — does not collide with the existing ik_llama-linked `chimere-server.service` on 8081.

### Hybrid — chimere (ik_llama, 8081) + bare turbo-tan llama-server (8083) + odo routing

- Effort: **1 h**. Ship a `turbo-tan-server.service` on 8083 using stock `llama-server` from `build_sm120/bin/`. Add `odo` pipeline variant `research-tq3.yaml` with `ODO_BACKEND_OVERRIDE=http://127.0.0.1:8083`.
- Preserves APEX I-Quality on 8081 untouched.
- TQ3 available for high-context / speed-focused queries via a pipeline switch.
- Downside: queries routed to 8083 get no Engram / DRY / RAMP. But that is the *intended* use for TQ3 (long-context research, where Engram retrieval overhead is less valuable).
- This matches the existing split `qwen35-custom / qwen35-q4km` topology the user already operates.

## 5. Ranking

| Option | Effort | Risk | Value preserved |
|---|---|---|---|
| **Hybrid** | **1 h** | **low** | APEX 100% + TQ3 available on-demand |
| B2 (rebuild) | 4-8 h | medium (ggml-cuda port) | 100% (unified) |
| B1 (swap) | 0.5 h | low | ~40% (no Engram/DRY/RAMP anywhere) |

## 6. Decision tree

```
TQ3 build completes?
├── immediate need < 2 days ──► Hybrid (ship turbo-tan llama-server on 8083)
│       │
│       └── once validated, reassess B2 as background project
│
└── > 2 days available         ──► B2 (feature-gate MTP + sampler_accept + .cu port)
        │
        └── if .cu port blocks ──► fall back to Hybrid, disable ggml_cuda_gemv feature
```

## 7. Recommendation

**Hybrid now, B2 later (background).**

- Immediate win: TQ3 accessible on 8083 within 1 h once turbo-tan `llama-server` builds complete.
- Zero risk to current APEX I-Quality production (8081 untouched).
- Defer the FFI rebuild until the .cu port can be done unhurried.
- The 4 MTP symbols + `common_sampler_accept` arity change are a **small patch set** (<50 LOC); the real unknown is `ggml_cuda_gemv.cu` (463 LOC) against turbo-tan's ggml-cuda internals, which is best done carefully.

## 8. Concrete hybrid steps

1. `cd ~/github-repos/llama.cpp-tq3/build_sm120 && ninja llama-server` — wait for completion.
2. Create `~/.config/systemd/user/turbo-tan-server.service` with `ExecStart=.../build_sm120/bin/llama-server --port 8083 -m <tq3_gguf> -ngl 99 --n-cpu-moe 4 -c 65536 -np 1` and `Conflicts=` nothing (parallel OK).
3. Add odo pipeline `~/.openclaw/odo/pipelines/research-tq3.yaml` with backend override to 127.0.0.1:8083.
4. Test: `curl :8083/health` then route a research query through odo with the new pipeline.
5. Document in MEMORY.md.
