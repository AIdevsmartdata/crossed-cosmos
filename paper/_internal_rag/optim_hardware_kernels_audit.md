# Hardware & Kernel Optimisation Audit — qwen-tq3 / RTX 5060 Ti sm_120

**Date:** 2026-04-22  
**Target:** `~/github-repos/llama.cpp-tq3/build_sm120/`  
**GPU:** RTX 5060 Ti 16 GB (Blackwell sm_120, 180 W TDP, max SM clock 3090 MHz)  
**CPU:** i5-14600KF (P-core AVX2 + AVX-VNNI), 32 GB DDR5  

---

## 1. Current Build Flag Inventory

Extracted from `build_sm120/CMakeCache.txt`:

| Flag | Current Value | Notes |
|---|---|---|
| `CMAKE_BUILD_TYPE` | `Release` | Correct. `-O3 -DNDEBUG` applied. |
| `CMAKE_CUDA_ARCHITECTURES` | `120` | Correct for sm_120. |
| `GGML_CUDA` | `ON` | CUDA backend active. |
| `GGML_NATIVE` | `OFF` | **MISSING AVX-VNNI** (see §4). |
| `GGML_LTO` | `OFF` | LTO disabled — missed CPU-side gains. |
| `GGML_CUDA_FA` | `ON` | Flash Attention enabled. |
| `GGML_CUDA_FA_ALL_QUANTS` | `OFF` | Only f16/bf16 KV paths compiled for FA. |
| `GGML_CUDA_FORCE_MMQ` | `OFF` | cuBLAS auto-select. |
| `GGML_CUDA_FORCE_CUBLAS` | `OFF` | cuBLAS auto-select. |
| `GGML_CUDA_NO_VMM` | `OFF` | VMM enabled (Linux driver 590.48 — fine). |
| `GGML_AVX` | `ON` | |
| `GGML_AVX2` | `ON` | |
| `GGML_AVX_VNNI` | `OFF` | **MISSING** — i5-14600KF has avx_vnni. |
| `GGML_AVX512` | `OFF` | Correct — i5-14600KF has no AVX-512. |
| `GGML_OPENMP` | `ON` | Correct. |
| `GGML_CPU_REPACK` | `ON` | Good — weight repack for CPU MoE. |

---

## 2. Missing / Recommended Build Flags

### 2.1 `GGML_AVX_VNNI=ON` — **HIGH IMPACT** ★★★

The i5-14600KF exposes `avx_vnni` in `/proc/cpuinfo` but the build has `GGML_AVX_VNNI=OFF`.  
AVX-VNNI provides `vpdpbusd` (INT8 dot product in 256-bit YMM registers) used by `ggml-cpu` repack + sgemm paths for MoE CPU expert GEMV.  
With `ncmoe=4`, CPU handles 4 layers of experts. AVX-VNNI gives 2× throughput over plain AVX2 INT8 on IQ3_S expert loops.

**To enable:**
```cmake
-DGGML_AVX_VNNI=ON
```

### 2.2 `GGML_LTO=ON` — **MEDIUM IMPACT** ★★

Link-Time Optimisation allows the linker to inline/devirtualise across translation units.  
Typical gain: 3–8% on CPU paths (MoE routing, token sampling, prompt processing).  
CUDA device code is unaffected (nvcc handles its own IPO). Safe on GCC ≥ 12 with `-flto=auto`.

**To enable:**
```cmake
-DGGML_LTO=ON
```

### 2.3 `GGML_CUDA_FA_ALL_QUANTS=ON` — **HIGH IMPACT** ★★★

With `GGML_CUDA_FA_ALL_QUANTS=OFF`, Flash Attention falls back from the MMA kernel to the tile or WMMA kernel whenever KV cache uses non-f16 types (Q8_0/Q4_0 configured in production: `-ctk q8_0 -ctv q4_0`).  
Setting this ON compiles FA kernels for all quantised KV types and enables the fast `BEST_FATTN_KERNEL_MMA_F16` path on sm_120.  
Given that Blackwell `BLACKWELL_MMA_AVAILABLE` is defined at sm_120 and the `fattn-mma-f16.cuh` path is selected at runtime (`BEST_FATTN_KERNEL_MMA_F16`), this is the single highest-priority compile flag for the attention layers of the 10 full-attention GDN layers.

**To enable:**
```cmake
-DGGML_CUDA_FA_ALL_QUANTS=ON
```
Note: increases build time and binary size (~+40 MB) because it compiles FA for every quant combination.

### 2.4 `GGML_CUDA_FORCE_MMQ=ON` — **LOW-MEDIUM** ★

By default, ggml auto-selects between cuBLAS GEMM and the MMQ (quantised matrix multiply) kernel.  
For small batch sizes (generation, batch=1), the custom `mul_mat_vec_q_moe` path in `mmvq.cu` is faster than cuBLAS. `GGML_CUDA_FORCE_MMQ=ON` prevents cuBLAS from winning the auto-select for weight matrices.  
Risk: slightly slower prompt processing for very long prompts. Recommend A/B test (see §9).

---

## 3. Blackwell sm_120 Kernel Audit

### 3.1 Active sm_120 codepaths (confirmed in source)

| File | Feature | sm_120 guard |
|---|---|---|
| `vecdotq.cuh` | `VDR_TQ3_1S_Q8_1_MMVQ=8` (doubled VDR) | `__CUDA_ARCH__ >= 1200` |
| `vecdotq.cuh` | `VDR_TQ3_4S_Q8_1_MMVQ=8` (doubled VDR) | `__CUDA_ARCH__ >= 1200` |
| `mma.cuh` | `mxf4` block-scaled Blackwell MMA | `BLACKWELL_MMA_AVAILABLE` |
| `mmq.cuh` | Blackwell-specific MMQ tiling | `BLACKWELL_MMA_AVAILABLE` |
| `fattn.cu` | MMA_F16 fattn kernel selection | `cc >= BLACKWELL` |
| `common.cuh` | TF32 cuBLAS math mode | Runtime: always set |

The sm_120-specific `VDR=8` in `vecdotq.cuh` means the MMVQ kernel processes 8 elements per thread per call vs 4 on older arches — this is already active because we compile with `CUDA_ARCHITECTURES=120`.

### 3.2 FP8 / FP4 Blackwell tensor cores

The `mxf4` MMA instruction (`mma.sync.aligned.kind::mxf4.block_scale...`) in `mma.cuh` uses Blackwell FP4 (E2M1) tensor cores. This path is **only reachable when weight tensors are quantised to `q4_0` or lower in FP4 block-scaled format** — not the current IQ3_S TQ3 format. Turbo-tan's TQ3 uses INT8 dp4a (`ggml_cuda_dp4a`) via `vecdotq.cuh`, not the mxf4 tensor core. There is currently no FP8-based path for TQ3 weights. This is the **one Blackwell feature not yet utilised** for TQ3 inference (see §4 below).

### 3.3 TF32

`cublasSetMathMode(CUBLAS_TF32_TENSOR_OP_MATH)` is set unconditionally in `common.cuh:1444` and `solve_tri.cu:76`. TF32 is active for any cuBLAS SGEMM call. On sm_120 TF32 gives ~2× throughput vs FP32. This is already enabled.

---

## 4. One Kernel-Level Feature Not Yet Enabled

**`BLACKWELL_MMA_AVAILABLE` FP4 path for TQ3 weights via new block-scaled quant.**

The Blackwell sm_120 silicon has native FP4 (E2M1) tensor cores with 2× block scaling (`mxf4`). Turbo-tan already has the CUDA inline assembly for this path (`mma.cuh` lines 1049–1062), but TQ3's 3-bit ternary format routes through INT8 dp4a, not the FP4 tensor core path. A `TQ3_BW` block format that maps ternary weights to 4-bit E2M1 representation with block scales could engage the `mxf4` instruction.  

This is distinct from the `VDR=8` speedup which is already active. Estimated throughput gain from FP4 tensor core path vs dp4a: 1.5–2× for MMVQ kernel, translating to ~10–20 tok/s on the attention layers.

---

## 5. Thermal / Power Analysis

**Current GPU spec:** 180 W TDP, max SM clock 3090 MHz, 16 GB GDDR7.  
No live bench was run in this audit (would require model loaded). Recommended monitoring approach:

```bash
# Run during a 60s llama-bench session:
nvidia-smi --query-gpu=power.draw,temperature.gpu,clocks.sm,clocks_throttle_reasons.sw_power_cap \
    --format=csv -l 1 > /tmp/gpu_thermal_$(date +%s).csv &
NVIDIASMI_PID=$!
# ... run bench ...
kill $NVIDIASMI_PID
```

Key thresholds on RTX 5060 Ti:
- Temperature throttle: > 83°C
- Power cap throttle: > 180 W sustained
- SM clock drop from 3090 → 2600 MHz = ~16% TG loss

If sustained generation hits 180 W (likely at 90 tok/s), driver may engage `SW_POWER_CAP` throttle. Recommended: `nvidia-smi -pl 175` to leave 5 W headroom and avoid the throttle cliff.

---

## 6. CPU MoE Offload Analysis

`-ot exps=CPU` / `-ncmoe N` keeps N layers' expert matrices on system RAM.  
With 32 GB DDR5 and current usage ~8.8 GB (OS + Docker), approximately **20 GB headroom** is available.  
Each layer's expert set at IQ3_S ≈ 3 expert kinds × 8 experts × ~500 KB = ~12 MB/layer.  
Practical budget for CPU experts: up to ~16 layers offloaded (~192 MB) with zero VRAM pressure.

**MoE prefetch patch** (documented in `chimere-prefetch-patch-2026-03-20.md`): exists only in `ik_llama.cpp`, **not** in turbo-tan (`llama.cpp-tq3`). Port viability: the patch hooks `ggml_compute_forward_mul_mat_id()` in `ggml.c` with a callback registered via `ggml_set_moe_prefetch_fn()`. Turbo-tan has the same function in `ggml/src/ggml.c`. Port is feasible in ~200 lines with the GPU GEMV helper from `chimere-rewrite/ffi/ggml_cuda_gemv.cu`. Estimated gain: same as measured in ik_llama: +10–14 tok/s at ncmoe=4.

---

## 7. Memory Allocation / cgroup

`MemoryMax=30064771072` (~28 GB) — this is **not** a bottleneck. Current resident: ~8.8 GB.  
No NUMA concern: i5-14600KF has a single-die UMA topology (all cores share one IMC). DDR5 on Raptor Lake Refresh uses dual-channel interleaving, not NUMA nodes. `numactl --hardware` would show 1 node.

---

## 8. NVMe KV Offload

Not implemented in turbo-tan or stock llama.cpp as of this audit. The `--no-kv-offload` flag in llama-bench refers to keeping KV on GPU vs CPU RAM, not disk.  
For 32K context with Q8_0/Q4_0 KV: KV size ≈ 10 attention layers × 32768 × 64 × 2 types × 2 bytes ≈ ~40 MB — well within VRAM. Not a concern at current context lengths.

---

## 9. Docker / CPU Accounting

Docker containers (idle total): ~117 MB RAM, ~0.03% CPU.  
No collision with llama-server threading. OpenMP thread pool for llama-server will pin to available P-cores. Docker containers run at default CFS scheduler priority — no interference with real-time GPU work.

**Recommendation:** If running llama-bench under load, optionally pin llama-server with `taskset -c 0-9` (P-cores only, avoid E-cores for latency-critical threads). The i5-14600KF has 6 P-cores + 8 E-cores; E-core IPC is ~60% of P-core for AVX2 MoE.

---

## 10. Disk I/O — GGUF Load Profile

NVMe0 (931 GB, PCIe NVMe, rotational=0).  
13 GB GGUF at ~3–4 GB/s sequential NVMe read: estimated cold-start ~3–4 s (not 30 s).  
Linux page cache will retain the mapping after first load. `mmap()` is used by llama.cpp for model weights; pages remain in page cache until evicted under memory pressure. Warm restart: effectively instantaneous for weight reads; only KV cache and context state need reinit.

**To verify:**  
```bash
time systemctl --user restart qwen35-custom
# first run: cold
sync && echo 3 | sudo tee /proc/sys/vm/drop_caches
time systemctl --user restart qwen35-custom
# second run: warm (pagecache)
```

---

## 11. Recommended Rebuild Command

```bash
cd ~/github-repos/llama.cpp-tq3
rm -rf build_sm120_v2 && mkdir build_sm120_v2 && cd build_sm120_v2

cmake .. \
  -DCMAKE_BUILD_TYPE=Release \
  -DGGML_CUDA=ON \
  -DCMAKE_CUDA_ARCHITECTURES=120 \
  -DGGML_NATIVE=OFF \
  -DGGML_LTO=ON \
  -DGGML_AVX_VNNI=ON \
  -DGGML_CUDA_FA_ALL_QUANTS=ON \
  -DGGML_CUDA_FORCE_MMQ=ON \
  -DGGML_OPENMP=ON \
  -DLLAMA_BUILD_TOOLS=ON \
  -DLLAMA_BUILD_TESTS=OFF \
  -DLLAMA_BUILD_EXAMPLES=OFF \
  -G Ninja

ninja -j$(nproc)
```

Delta vs current: adds `GGML_LTO`, `GGML_AVX_VNNI`, `GGML_CUDA_FA_ALL_QUANTS`, `GGML_CUDA_FORCE_MMQ`.  
Build time estimate: +3–5 min (FA_ALL_QUANTS compiles many kernel instantiations).

---

## 12. bench_matrix.sh

```bash
#!/usr/bin/env bash
# bench_matrix.sh — A/B benchmark for qwen-tq3 sm_120 build variants
# Usage: ./bench_matrix.sh /path/to/model.gguf [output_csv]
# Requires: llama-bench in PATH or specified via LLAMA_BENCH env var

set -euo pipefail

MODEL="${1:?Usage: $0 <model.gguf> [output.csv]}"
OUTPUT="${2:-/tmp/bench_results_$(date +%Y%m%d_%H%M%S).csv}"
LLAMA_BENCH="${LLAMA_BENCH:-$HOME/github-repos/llama.cpp-tq3/build_sm120/bin/llama-bench}"

if [[ ! -f "$LLAMA_BENCH" ]]; then
  echo "ERROR: llama-bench not found at $LLAMA_BENCH" >&2
  exit 1
fi

echo "Model: $MODEL"
echo "Output: $OUTPUT"
echo "llama-bench: $LLAMA_BENCH"

# Common args: single GPU offload, no examples, CSV output
BASE_ARGS="-m '$MODEL' -ngl 99 --output csv"

run_bench() {
  local label="$1"; shift
  local extra="$*"
  echo "--- Running: $label ---"
  eval "$LLAMA_BENCH $BASE_ARGS $extra -o csv" 2>/dev/null \
    | tail -n +2 \
    | awk -v lbl="$label" -F',' 'NR>0{print lbl","$0}' \
    >> "$OUTPUT"
}

# CSV header
echo "variant,model,size,params,backend,ngl,n_batch,n_ubatch,n_threads,type_k,type_v,n_gpu_layers,split_mode,main_gpu,no_kv_offload,flash_attn,tensor_split,use_mmap,embeddings,n_prompt,n_gen,test,t_ms,speed" \
  > "$OUTPUT"

# === Baseline (current build) ===
# TG only (generation speed)
run_bench "baseline_tg512" \
  "-p 512 -n 512 -t 4 -nkvo 0 -fa 1"

run_bench "baseline_tg128" \
  "-p 128 -n 512 -t 4 -nkvo 0 -fa 1"

# === KV type variants ===
run_bench "kv_q8q4_tg" \
  "-p 512 -n 512 -t 4 -nkvo 0 -fa 1 -ctk q8_0 -ctv q4_0"

run_bench "kv_f16f16_tg" \
  "-p 512 -n 512 -t 4 -nkvo 0 -fa 1 -ctk f16 -ctv f16"

run_bench "kv_q4q4_tg" \
  "-p 512 -n 512 -t 4 -nkvo 0 -fa 1 -ctk q4_0 -ctv q4_0"

# === Flash Attention on/off ===
run_bench "no_fa_tg" \
  "-p 512 -n 512 -t 4 -nkvo 0 -fa 0"

# === Thread count sweep for CPU MoE (ncpu) ===
for T in 2 4 6 8 10 14; do
  run_bench "threads_${T}_tg" \
    "-p 512 -n 512 -t $T -nkvo 0 -fa 1"
done

# === Prompt processing speed ===
run_bench "baseline_pp512" \
  "-p 512 -n 0 -t 4 -nkvo 0 -fa 1"

run_bench "pp_threads14" \
  "-p 512 -n 0 -t 14 -nkvo 0 -fa 1"

# === Batch sizes ===
for UB in 256 512 1024 2048; do
  run_bench "ubatch_${UB}_pp" \
    "-p 2048 -n 0 -ub $UB -t 4 -nkvo 0 -fa 1"
done

# === Context lengths ===
for CTX in 4096 8192 16384 32768; do
  run_bench "ctx_${CTX}_tg" \
    "-p $CTX -n 128 -t 4 -nkvo 0 -fa 1"
done

echo ""
echo "Results written to: $OUTPUT"
echo "Preview:"
column -t -s',' "$OUTPUT" | head -20
```

---

## Summary Table: Priority Flags

| Priority | Flag | Impact | Rationale |
|---|---|---|---|
| 1 | `GGML_CUDA_FA_ALL_QUANTS=ON` | +5–15% TG | Enables MMA_F16 FA kernel for Q8_0/Q4_0 KV types on sm_120 |
| 2 | `GGML_AVX_VNNI=ON` | +5–10% CPU MoE | i5-14600KF has avx_vnni; INT8 dot-product SIMD for expert GEMV |
| 3 | `GGML_LTO=ON` | +3–8% CPU paths | Link-time inlining across TUs for CPU MoE routing and sampling |
| — | `GGML_CUDA_FORCE_MMQ=ON` | ±3% TG | Prevents cuBLAS fallback on small-batch matmuls; test before deploying |

**Unactivated Blackwell feature:** FP4 `mxf4` tensor core MMA path — exists in hardware and partially in code (`mma.cuh`), not reachable with current TQ3 INT8/ternary quantisation format.

**Total `.cu` files in turbo-tan tree:** 189  
(63 in `ggml/src/ggml-cuda/` + 126 elsewhere including examples, tests, and vendor)
