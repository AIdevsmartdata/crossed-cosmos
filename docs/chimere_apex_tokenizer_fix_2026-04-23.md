# chimere-server Apex tokenizer mismatch fix (2026-04-23)

**Problem observed.** After swapping `chimere-server.service` from
`chimere-v3-ramp.gguf` (Qwen3.5 base) to `Qwen3.6-35B-A3B-APEX-I-Quality.gguf`
(Qwen3.6 base) keeping the pre-existing `CHIMERE_TOKENIZER` pointing at
`models--Qwen--Qwen3.5-35B-A3B/.../tokenizer.json`, the server booted and
answered, but:
- odo+web_search queries hallucinated (invented arXiv IDs, wrong H₀ values)
- `prompt_tokens` reported only 611 tokens when ~2500 of RAG context was fed

**Root cause.** The Rust chimere-server binary requires an **external** HF
tokenizer.json (see `src/bin/chimere-server.rs` L106–244) and does not
fall back to the GGUF-embedded vocab. Qwen3.5 tokenizer has 151 936 vocab
entries; Qwen3.6 APEX has **248 320** per GGUF dump (`gguf-dump` output
showed `tokenizer.ggml.tokens = [..., 248320 strings]`, pre-tokenizer
`qwen35`, bos=248044, eos=248046). Any retrieval context containing
vocabulary beyond ~152 k was re-tokenized incorrectly by chimere-server,
producing a shortened + garbled prompt at the Rust→FFI→ik_llama boundary.
The model then generated from training priors → hallucinations.

**Diagnosis sequence.**
1. Direct `/v1/chat/completions` call to chimere-server :8081 with thinking
   enabled → 3910 completion tokens of thinking but empty final content.
2. Bypass test: launched `ik_llama.cpp/build_sm120/bin/llama-server` directly
   on :8082 with same GGUF, no external tokenizer (llama-server uses GGUF
   internal vocab). Query answered cleanly at 56 tok/s.
3. This isolated the Rust wrapper + external tokenizer as the bug.

**Fix.**
```bash
HFDIR=~/.cache/huggingface/hub/models--Qwen--Qwen3.6-35B-A3B
mkdir -p "$HFDIR/snapshots/main"
cd "$HFDIR/snapshots/main"
curl -sL -o tokenizer.json \
  https://huggingface.co/Qwen/Qwen3.6-35B-A3B/resolve/main/tokenizer.json
curl -sL -o tokenizer_config.json \
  https://huggingface.co/Qwen/Qwen3.6-35B-A3B/resolve/main/tokenizer_config.json
```
Verify: the downloaded `tokenizer.json` has 248 044 vocab + 26 added tokens
(close to the GGUF 248 320 after internal padding). Edit
`~/.config/systemd/user/chimere-server.service`:
```
Environment=CHIMERE_TOKENIZER=/home/remondiere/.cache/huggingface/hub/models--Qwen--Qwen3.6-35B-A3B/snapshots/main/tokenizer.json
```
Also:
- `CHIMERE_MODEL=/home/remondiere/.openclaw/models/Qwen3.6-35B-A3B-APEX-GGUF/Qwen3.6-35B-A3B-APEX-I-Quality.gguf`
- `CHIMERE_MMPROJ=/home/remondiere/.openclaw/models/Qwen3.6-35B-A3B-APEX-GGUF/mmproj-F16.gguf`
- `CHIMERE_NCMOE=20` (22 GB model on 16 GB VRAM needs 20 MoE layers on CPU)
- `MemoryMax=28G` (from 20 G)

**Post-fix validation.**
- Direct :8081 simple Planck H₀ query: clean `67.4 ± 0.5 km/s/Mpc` answer,
  1.4 s, 57 completion tokens, factually correct.
- odo → chimere → web_search e2e query: `prompt_tokens = 2583` (vs 611
  pre-fix), model reads the injected "Knowledge Base" context and reasons
  over it rather than hallucinating.

**Collateral optimisations applied to the web-search pipeline.** Not
strictly part of the chimere bug, but landed together:
- `~/.openclaw/bin/deep_search_sota.py`:
  - `DEPTH_CONFIG.top_chunks`: 5/8/12 → **8/12/16** (more context for the
    64 K-capable Apex model, reduces synthesis hallucinations).
  - `include_academic = depth in ("standard","deep")` (was deep-only):
    arXiv/academic sources now pulled at standard depth — important for
    physics/cosmology queries.
  - `use_neural = depth in ("standard","deep")` (was deep-only):
    gte-reranker-modernbert-base CPU cross-encoder rerank now runs at
    standard depth; +~5 s first call, cached thereafter.
- `~/.openclaw/odo/enricher.py`:
  - research timeout 120→**90 s** (deep_search_sota caps ~60 s internally;
    90 s gives slack for cross-encoder warmup + synthesis).
  - non-research web timeout 60→**45 s**.
- Removed hardcoded `/home/remondiere/.openclaw/venvs/pipeline/bin/python`
  from `_run_all.py` (replaced by `os.environ.get("PIPELINE_PYTHON",
  sys.executable)`) — also solves a private-toolchain path leak flagged by
  an earlier security audit.

**Files touched outside the repo.** These live in `$HOME/.config/` and
`$HOME/.openclaw/` and are not part of `crossed-cosmos`:
- `~/.config/systemd/user/chimere-server.service`
- `~/.openclaw/bin/deep_search_sota.py`
- `~/.openclaw/odo/enricher.py`
- `~/.cache/huggingface/hub/models--Qwen--Qwen3.6-35B-A3B/` (new)

A small copy of the canonical service file is attached below for
posterity.

## Canonical chimere-server.service (post-fix)

```systemd
[Unit]
Description=Chimere Server — Rust FFI ik_llama sm120, Qwen3.6-35B-A3B APEX I-Quality, 64K ctx, Engram+Sampling+DRY
After=network.target

[Service]
Type=simple
Environment=LD_LIBRARY_PATH=/home/remondiere/ik_llama.cpp/build_sm120/ggml/src:/home/remondiere/ik_llama.cpp/build_sm120/src:/usr/local/cuda-12.8/lib64
Environment=CHIMERE_LLAMA_BACKEND=1
Environment=CHIMERE_MODEL=/home/remondiere/.openclaw/models/Qwen3.6-35B-A3B-APEX-GGUF/Qwen3.6-35B-A3B-APEX-I-Quality.gguf
Environment=CHIMERE_TOKENIZER=/home/remondiere/.cache/huggingface/hub/models--Qwen--Qwen3.6-35B-A3B/snapshots/main/tokenizer.json
Environment=CHIMERE_MMPROJ=/home/remondiere/.openclaw/models/Qwen3.6-35B-A3B-APEX-GGUF/mmproj-F16.gguf
Environment=CHIMERE_PORT=8081
Environment=CHIMERE_NCMOE=20
Environment=CHIMERE_KV_MAX_SEQ=65536
Environment=CHIMERE_ENGRAM_DIR=/home/remondiere/.openclaw/data/engram
ExecStart=/home/remondiere/github-repos/chimere/chimere-server/target/release/chimere-server
Restart=on-failure
RestartSec=10
MemoryMax=28G

[Install]
WantedBy=default.target
```

**Lesson for future model swaps.** When changing `CHIMERE_MODEL` across
families (3.5 → 3.6, or any vocab-incompatible bump), always update
`CHIMERE_TOKENIZER` in lockstep to an HF repo tokenizer.json whose
vocab size matches the GGUF metadata vocab size (inspect via
`gguf-dump --no-tensors ... | grep tokenizer.ggml.tokens`). The quiet
failure mode (truncated prompt + hallucinated output with no explicit
error) is the one that burned this cycle.
