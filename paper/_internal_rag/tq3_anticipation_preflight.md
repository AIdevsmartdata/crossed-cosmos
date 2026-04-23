# TQ3_4S anticipation + pre-flight (V8)

Scope: Qwen3.6-35B-A3B-TQ3_4S on turbo-tan/llama.cpp-tq3 fork, RTX 5060 Ti (sm_120, 16 GiB), CUDA 12.8. Port 8083 (does not collide with chimere-server @ 8081 APEX fallback).

Observed state at 2026-04-22 08:49:

- Build: COMPLETED. `build_sm120/bin/llama-server` linked; `libggml-cuda.so.0.9.11` present. No sm_120 build failures — the `-DCMAKE_CUDA_ARCHITECTURES=120` + CUDA 12.8 combo that already worked for ik_llama sm120 also works here.
- GGUF: `~/.openclaw/models/Qwen3.6-35B-A3B-TQ3_4S/Qwen3.6-35B-A3B-TQ3_4S.gguf` present, 12.39 GiB (13 298 875 360 B). Magic `GGUF` verified by preflight.
- Binary `--help` advertises `tq3_0` for `-ctk`/`-ctv` → TurboQuant cache types registered.
- VRAM right now: 2907 / 16311 MiB free — qwen35-custom (chimere-server path) still holds the card. This is the #1 concrete launch blocker: preflight will warn, launch will OOM until we free VRAM.

## Section 1 — Failure-mode table

Bit-width notation: weights ≈ 3.07 BPW (experts 2b, attention 4b, mmproj BF16). KV: K=q4_0 (4.5 BPW), V=tq3_0 (~3 BPW).

| # | Phase | Failure | Detection signal | Auto? | Mitigation |
|---|---|---|---|---|---|
| B1 | build | `no kernel image available for execution on the device` (sm_89-only kernels) | runtime CUDA error on first kernel | yes (journal grep) | rebuild with `-DCMAKE_CUDA_ARCHITECTURES=120` (already done) + `-DGGML_NATIVE=OFF` |
| B2 | build | nvcc 12.8 + gcc-13 `error: identifier "__builtin_…"` | `/tmp/tq3_build.log` | n/a (build succeeded) | set `CUDAHOSTCXX=g++-12` |
| B3 | build | `undefined reference to ggml_type_tq3_0` | linker stage | n/a | ensure `libggml.so` not a stale system copy; `LD_LIBRARY_PATH=$BUILD/bin` |
| L1 | load | `unknown ggml_type N` where N is TQ3 enum id drift | server stderr | yes (grep) | confirm fork built from same branch as GGUF producer; rebuild |
| L2 | load | GGUF version > supported | `gguf_init_from_file: unsupported version` | yes | update fork |
| L3 | load | tokenizer missing / chat_template missing | silent garbled output on first gen | partial (preflight dry-run greps) | use `--chat-template qwen3` explicit, or re-download GGUF |
| L4 | load | `-ctv tq3_0` rejected at runtime (advertised in --help but kernel missing) | `ggml_cuda_cpy: unsupported type` | yes (grep) | fall back to `-ctv q4_0` (minor quality loss) |
| L5 | load | mmproj BF16 incompatible | N/A — not used in service unit | skip | no mmproj loaded |
| R1 | runtime | CUDA OOM at model load | `cudaMalloc.*out of memory` | yes | **cascade**: c=65536 → 32768 → 16384 → 8192 (V8-tq3-launch.sh) |
| R2 | runtime | OOM at first decode (KV buffer grows lazily) | same, after 1st request | yes | same cascade |
| R3 | runtime | Port 8083 busy | `bind: address in use` | yes (preflight ss check) | kill stale process |
| R4 | runtime | Garbled tokens (tokenizer mismatch, cf. APEX bug) | gibberish in curl test | manual | add `--chat-template qwen3`; if persists, re-download GGUF |
| R5 | runtime | `--reasoning-format deepseek` eats tool calls (τ3-bench finding 2026-04-02) | tool calls missing in response | known | drop flag if we wire TQ3 into odo/tool flows |
| Q1 | quality | 2-bit experts → hallucinations on long context | eval vs APEX baseline | manual | accept or fall back to APEX |
| Q2 | quality | Chat template drift at low BPW (`<think>` emitted inconsistently) | sampled outputs | manual | raise temp floor; switch to APEX for reasoning-critical flows |
| Q3 | quality | Multi-turn coherence drift (known TQ3 weakness vs I-Q) | long-session smoke test | manual | route long sessions to chimere-server |
| SYS | ops | VRAM already held by qwen35-custom/chimere-server | `nvidia-smi` free < 14.5 GiB | yes (preflight) | stop holder before start |

Three most likely failure modes (ranked): **R1 (load OOM because VRAM still held by chimere-server/qwen35-custom)**, **R4 (tokenizer/template-driven gibberish — same class of bug we hit on APEX)**, **R5 (reasoning-format deepseek clobbering tool calls — pre-registered from τ3-bench 2026-04-02)**.

Hardest-to-recover-from: **L1 (enum drift between fork and GGUF producer)** — only remedy is rebuild from matching branch, not detectable from --help; and **Q1/Q2 quality drift** — invisible to preflight, only surfaces under real load, requires side-by-side eval vs APEX.

## Section 2 — Memory budget

Qwen3.5-35B-A3B established baseline: 10 full-attention layers, 30 GDN (no KV). Assuming Qwen3.6-35B-A3B preserves the hybrid ratio (model card treats it as a minor iteration), and using the standard formula

    KV_bytes = 2 * n_full_attn * n_kv_heads * head_dim * ctx * (bpw/8)

with n_full_attn=10, n_kv_heads=4, head_dim=128, ctx=65536, K=q4_0 (4.5 BPW) + V=tq3_0 (3.0 BPW → mean 3.75):

    KV ≈ 2 * 10 * 4 * 128 * 65536 * (3.75/8) / 2 ≈ 630 MiB

Weights 12.4 GiB + KV 0.63 GiB + compute buffers ~1.0-1.4 GiB ≈ **14.0-14.4 GiB peak**. Fits 16 GiB — but **only if we first stop qwen35-custom/chimere-server**. Current free=2907 MiB is a hard blocker.

Sensitivity: if Qwen3.6 actually bumped full-attn layers to 16 (some MoE refactors do), KV triples to ~1.9 GiB and total reaches ~15.7 GiB — still fits but squeezes compute buffers. The cascade to c=32768 halves KV and gives clear headroom.

## Section 3 — Pre-flight script (copy at `derivations/V8-tq3-preflight.sh`)

Written separately at `/home/remondiere/crossed-cosmos/derivations/V8-tq3-preflight.sh`. Summary of checks:

1. Binary exists and `--version` runs (catches linker/sm120 regressions).
2. GGUF present, size 12-13 GiB (catches partial download), magic bytes = `GGUF`.
3. Binary advertises `tq3_0` cache type in `--help` (catches fork built without TQ3).
4. Port 8083 free.
5. VRAM free ≥ 14.5 GiB; WARN if not (will guide cascade launcher).
6. 12-second dry-run at `-ngl 0 -c 512` on an unused port; grep stderr for `tokenizer`, `chat_template`/`jinja`, and fatal load errors like `unknown ggml_type`, `unsupported`, `failed to load`.

Exit codes: 0=green, 1=hard FAIL, 2=WARN (cascade launcher handles it).

## Section 4 — Auto-mitigation cascade (at `derivations/V8-tq3-launch.sh`)

Pseudocode:

    for ctx in 65536, 32768, 16384, 8192:
        write systemd drop-in at ~/.config/systemd/user/qwen-tq3.service.d/10-ctx-override.conf
        systemctl --user daemon-reload && restart qwen-tq3
        poll /health for up to 120 s
        if journal shows CUDA OOM → next ctx
        if /health responds → SUCCESS, persist override
    if all fail → stop qwen-tq3, remove override, daemon-reload,
                  start chimere-server (if not already active)

This is the drop-in/override path rather than mutating the base unit file — the original `qwen-tq3.service` stays canonical.

## Section 5 — Rollback (order matters)

Correct sequence, zero-disruption:

    systemctl --user stop qwen-tq3              # frees port 8083 + VRAM
    systemctl --user is-active --quiet chimere-server \
      || systemctl --user start chimere-server  # rebinds 8081 APEX I-Quality

Safety notes: do NOT stop chimere-server before confirming qwen-tq3 is running — chimere-server is the odo default backend @ 8081, so losing it mid-swap breaks every downstream path (Claude Code, OpenClaw, aider). The service files use different ports (8083 vs 8081), so both CAN coexist VRAM-permitting; in practice on a 16 GiB card we run one at a time.

## Section 6 — Pre-registered auto-detections (grep patterns for journal)

    # launch-time OOM (known-good detection)
    cudaMalloc.*out of memory|CUDA error.*out of memory|failed to allocate

    # type-system drift
    unknown ggml_type|unsupported.*type|failed to load model

    # tokenizer/template
    (load_|loader: ).*tokenizer.*(error|missing)
    chat template.*not found

    # port collision
    bind: Address already in use

    # sm_120 kernel gap
    no kernel image is available for execution on the device

The launch cascade watches the first two in near-real-time; the rest are diagnostics for post-mortem.

## Section 7 — Quality smoke test (to run after GREEN preflight + successful launch)

Minimal, not in scope of auto-cascade:

    curl -s http://127.0.0.1:8083/v1/chat/completions \
      -H 'Content-Type: application/json' \
      -d '{"model":"tq3","messages":[{"role":"user","content":"En une phrase: qui es-tu?"}],"max_tokens":128}'

Compare to same prompt on 8081 (APEX). Look for: coherent French, no token repetition, closes with punctuation. If this passes, run the 10-task τ3-bench subset and compare tool-calling accuracy vs APEX's 20% baseline before promoting TQ3 as primary.
