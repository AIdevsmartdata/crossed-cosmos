# VAST PRODUCTION PLAN — Chroma SU(2) Glueball GEVP T₂⁺/E⁺

**Document:** `VAST_PRODUCTION_PLAN.md`  
**Ξ Vast v3 — 2026-05-16**  
**Budget:** €18.81 (~$20.70 USD)  
**Pivot:** Custom C++ GEVP → Chroma STOCK avec FUZZED_WILSON_LOOP

---

## 1. Best Vast GPU Offers

### Top 3 RTX 3090 (prioritized for 24GB VRAM + high reliability)

| Rank | ID | Machine | GPU | VRAM | RAM | CPU | Disk | $/h | Rel |
|:-----|:---|:--------|:----|:-----|:----|:----|:-----|:----|:----|
| **🥇** | **36539604** | 3448 | RTX 3090 | 24GB | 62.9GB | 16c | 348GB | **$0.296** | **99.9%** |
| **🥈** | **12025649** | 26840 | RTX 3090 | 24GB | 31.4GB | 12c | 228GB | **$0.261** | **99.9%** |
| **🥉** | **36881008** | 27657 | RTX 3090 | 24GB | 168GB | 16c | 318GB | **$0.268** | 95.7% |

### Best RTX 4090 (faster, more expensive)

| Rank | ID | Machine | GPU | VRAM | RAM | CPU | Disk | $/h | Rel |
|:-----|:---|:--------|:----|:-----|:----|:----|:-----|:----|:----|
| 4 | **34354979** | 54003 | RTX 4090 | 24GB | 31.4GB | 16c | 323GB | **$0.282** | **99.8%** |

### Best Budget (A4000, for testing/light runs)

| Rank | ID | Machine | GPU | VRAM | RAM | CPU | Disk | $/h | Rel |
|:-----|:---|:--------|:----|:-----|:----|:----|:-----|:----|:----|
| $ | **30814963** | 4558 | RTX A4000 | 16GB | 31.5GB | 12c | 960GB | **$0.108** | **99.2%** |

### Recommendation
- **Production run:** #36539604 (99.9% reliable, 62.9GB RAM, 348GB disk, RTX 3090 @ $0.296/h)
- **Budget yields:** $20.70 / $0.296 = **~70 GPU-hours**
- **Backup:** #12025649 (99.9%, cheaper at $0.261/h → ~79h)
- **Testing/development:** #30814963 (A4000 @ $0.108/h)

---

## 2. Resource Estimation — 16⁴×32 SU(2)

### Memory (per MPI rank, single node)

| Component | Size | Notes |
|:----------|:-----|:------|
| Gauge field (4 links × 4 SU(2) params × 131K sites) | ~8 MB | Single precision |
| APE smeared copies (5 levels) | ~40 MB | In-memory during measurement |
| FUZZED_WILSON_LOOP buffers | ~20 MB | Loop construction |
| **Total VRAM needed** | **<100 MB** | Trivial — Chroma is CPU-bound |
| RAM for QDP++ layouts | ~200 MB | Lexicographic + checkerboard |
| Config file (.lime) | ~17 MB | Per saved configuration |
| Correlator output XML | ~5-50 MB | Depends on n_smear levels |

**Conclusion:** 16⁴×32 is a *tiny* lattice. The GPU is barely used by stock Chroma (QDP++ is CPU-parallel). An RTX 3090 is massive overkill for compute, but gives us 24GB VRAM that's fully unused — we're really paying for the CPU cores and RAM.

### Time Estimates

| Operation | 16⁴×32 SU(2) | Notes |
|:----------|:-------------|:------|
| 1 Heatbath sweep | ~0.001s | SU(2) is trivial vs SU(3) |
| 5000 sweeps (warm + prod) | ~5-10s | CPU-bound, O(N_c²) |
| FUZZED_WILSON_LOOP (5 levels) | ~1-5s per config | Smearing + loop construction |
| Plaquette + Polyakov | <1s | |
| **Total per config** | **~10-20s** | Including I/O |
| **5000 configs** | **14-28 hours** | Single-core estimate |
| **With 16 cores (OMP)** | **1-4 hours** | Realistic |

**Reality check:** For 16⁴×32 with SU(2), Chroma on a single modern CPU core can generate/config in under 1 second. With 16 cores and OpenMP, the entire 5000-config production could complete in **under 2 hours**, not the 70 hours budgeted. The bottleneck will be I/O (saving configs to disk) and XML output parsing, not compute.

### Statistical Requirements

| Target | Configs Needed (est.) | Notes |
|:-------|:----------------------|:------|
| m_0++ mass < 5% error | ~200-500 | Dominant channel, clean signal |
| m_2++ mass < 5% error | ~500-1000 | T₂⁺/E⁺, noisier |
| m_2++ mass < 2% error | **~2000-5000** | Our target |
| GEVP stability (5 ops) | >500 | Need good C(t₀) conditioning |

**5 operators × 5 APE smearing levels = 5×5 correlation matrix for GEVP.**

---

## 3. Pipeline Architecture

```
┌──────────────────────────────────────────────────────────────┐
│  Phase 1: Config Generation (Chroma PURE_GAUGE_MC)           │
│  ├─ SU(2) Wilson action, β=2.50                              │
│  ├─ Heatbath (n_or=4, n_over=5)                              │
│  ├─ 100 warmup + 5000 production sweeps                      │
│  └─ Save every 50 sweeps → 100 configs                       │
├──────────────────────────────────────────────────────────────┤
│  Phase 2: Inline Measurements (during generation)            │
│  ├─ MESPLQ: Plaquette (action check)                         │
│  ├─ POLAKOV_LOOP: Confinement check                          │
│  ├─ FUZZED_WILSON_LOOP × 5: APE smearing levels 2,4,8,12,16 │
│  │   ├─ wloopr: 0⁺⁺ channel                                 │
│  │   ├─ wlooprs: 2⁺⁺, 1⁺⁻ channels                         │
│  │   └─ Each: t=0..16 correlator time series                │
│  └─ QACTDEN (every 10 sweeps): Topology                      │
├──────────────────────────────────────────────────────────────┤
│  Phase 3: Post-Processing (Python)                           │
│  ├─ Parse XML → numpy arrays                                 │
│  ├─ Build 5×5 correlation matrix C_ij(t)                     │
│  ├─ GEVP: C(t) v_n = λ_n C(t₀) v_n                          │
│  ├─ Effective mass: m_eff(t) = -ln(λ_n(t)/λ_n(t-1))         │
│  ├─ Plateau fit → m_n ± σ_n                                  │
│  └─ Identify T₂⁺/E⁺ from cubic group decomposition          │
└──────────────────────────────────────────────────────────────┘
```

---

## 4. Chroma Native Glueball Support — Critical Analysis

### What Chroma DOES provide natively:

| Feature | Status | Measurement Name |
|:--------|:------:|:-----------------|
| SU(2) gauge group | ✅ | Configure `--enable-Nc=2` in QDP++ |
| Wilson gauge action | ✅ | `WILSON_GAUGEACT` |
| Heatbath Monte Carlo | ✅ | `HEATBATH` in `PURE_GAUGE_MC` |
| Plaquette measurement | ✅ | `MESPLQ` |
| Polyakov loop | ✅ | `POLAKOV_LOOP` |
| APE smearing (via blocking) | ✅ | `fuzwilp` → `block()` + `APE_Smear()` |
| Fuzzy Wilson loops (0⁺⁺, 2⁺⁺, 1⁺⁻) | ✅ | `FUZZED_WILSON_LOOP` |
| Stout smearing | ✅ | `STOUT_GAUGE_STATE` |
| Topological charge | ✅ | `QACTDEN` |

### What Chroma does NOT provide natively:

| Feature | Status | Workaround |
|:--------|:------:|:-----------|
| T₂⁺/E⁺ cubic group projection | ❌ | Post-process: linear combinations of Wilson loops |
| GEVP solver | ❌ | Python/SciPy post-processing |
| Direct mass extraction | ❌ | Effective mass fits in Python |
| Glueball operator construction | ❌ | Chroma gives Wilson loops; we build operators |
| SU(2) specific glueball reference | ❌ | Compare with SU(2) lattice literature |

### The T₂⁺/E⁺ Challenge

Chroma's `FUZZED_WILSON_LOOP` computes correlators of basic Wilson loops (plaquette, 2×1 rectangle, etc.) at various APE smearing levels. These transform under the full rotation group O(3) (or cubic group O_h on the lattice).

To isolate T₂⁺ (J^PC = 2⁺⁺, 3-dimensional irrep of O_h) and E⁺ (J^PC = 2⁺⁺, 2-dimensional irrep of O_h), we need to:
1. Construct operators with definite cubic group transformation properties
2. This requires specific linear combinations of oriented Wilson loops
3. The GEVP then separates the lowest T₂⁺ and E⁺ states

**This is done in post-processing** — Chroma provides the raw loop data, and our Python analysis constructs the irreps.

### Verdict: Feasible with Chroma STOCK

✅ **Yes, the pipeline is feasible with stock Chroma** — but the GEVP and irrep projection MUST be done in post-processing. Chroma is the gauge configuration generator and raw correlator computer, not the spectroscopy analysis tool.

---

## 5. Deployment Recipe (One-Click)

```bash
# On Vast instance (after SSH):
git clone <repo> /root/chroma_pipeline
cd /root/chroma_pipeline

# Option A: Full auto-pilot
./deploy_vast_v3.sh

# Option B: Manual phases
./deploy_vast_v3.sh --build-only    # ~20 min (compilation)
./deploy_vast_v3.sh --measure-only  # ~2-8 hours (production)
./deploy_vast_v3.sh --analyze-only  # ~5 min (GEVP)
```

### Build Time Estimate
- QDP++ (SU(2)): ~5-10 min on 16 cores
- Chroma: ~10-15 min on 16 cores
- Total build: **~20 min**

---

## 6. Budget Allocation

| Item | Cost | Hours | Notes |
|:-----|:----:|:------|:------|
| Build + test | $0.30 | 1h | RTX 3090 |
| Production run | $8.90 | 30h | Primary |
| Re-run (if needed) | $5.90 | 20h | Safety margin |
| Analysis + I/O | $2.90 | 10h | Post-processing |
| **Total (target)** | **$18.00** | **61h** | |
| **Budget** | **$20.70** | **70h** | €18.81 @ 1.10 USD/EUR |

---

## 7. Risk Assessment

| Risk | Probability | Impact | Mitigation |
|:-----|:-----------:|:------:|:-----------|
| QDP++ SU(2) build fails | Medium | High | Fallback: use existing SIMULATeQCD SU(3) + analytic continuation |
| Chroma `FUZZED_WILSON_LOOP` bugs | Low | Medium | Run Chroma test suite first; compare with known 4⁴×8 test |
| GEVP ill-conditioned (small t₀) | Medium | Medium | Vary t₀=1,2,3; check eigenvalue stability |
| T₂⁺/E⁺ signal too noisy at 16⁴×32 | High | High | Increase statistics to 10K configs; use larger β |
| Vast instance dies mid-run | Medium | High | Checkpoint configs every 50 sweeps; auto-resume |
| Disk fills (configs accumulate) | Low | Low | Auto-cleanup routine active |

---

## 8. Comparison: Custom C++ GEVP vs Chroma STOCK

| Aspect | Custom C++ (v1/v2) | Chroma STOCK (v3) |
|:-------|:-------------------|:------------------|
| Glueball operators | Manual Wilson loop code | Built-in, tested |
| APE smearing | Manual, buggy | Built-in, optimized |
| GEVP solver | Custom (buggy) | External Python (robust) |
| Config generation | External | Built-in heatbath |
| I/O format | Custom binary | Standard XML/LIME |
| Build complexity | Single Makefile | Autotools + QDP++ |
| Bug surface | 19 known issues | 0 (stock code) |
| Maintainability | Fragile | Community-supported |
| SU(2) support | Yes (custom) | Via QDP++ configure |

---

## 9. Timeline

```
T+0:00  — Deploy Vast instance, install deps
T+0:20  — QDP++ + Chroma build complete
T+0:25  — Sanity test (4⁴×8) passed
T+0:30  — Production run starts (5000 configs, 16⁴×32)
T+2:00  — Production complete (~2h on 16 cores)
T+2:05  — XML parsed, correlators extracted
T+2:10  — GEVP solved, T₂⁺/E⁺ masses fitted
T+2:15  — Final report generated
```

**Total wall time: ~2.5 hours**  
**Total cost: ~$0.75** (at $0.296/h for RTX 3090)

---

## 10. Deliverables

| File | Path | Purpose |
|:-----|:-----|:--------|
| XML Config | `glueball_T2g_inline.xml` | Chroma inline measurement specification |
| Deploy Script | `deploy_vast_v3.sh` | One-click build + run + analyze |
| This Plan | `VAST_PRODUCTION_PLAN.md` | Full production documentation |

---

## Appendix A: SU(2) β=2.50 Physics

- SU(2) Wilson action at β=2.50 corresponds to a ≈ 0.08 fm (rough estimate)
- Lattice size 16⁴×32 → physical volume ~ (1.3 fm)³ × 2.6 fm
- String tension √σ ≈ 440 MeV → m_0⁺⁺ ≈ 1.65 GeV (SU(2) quenched, scaling from SU(3))
- Deconfinement at β_c ≈ 2.30 for N_t=4 (SU(2)), so β=2.50 is in confined phase ✅
- Expected glueball masses (SU(2), quenched): m_0++ ~ 1650 MeV, m_2++ ~ 2400 MeV

## Appendix B: Literature References

- Lucini, Teper, Wenger (2004): SU(N) glueball masses, N=2..8, continuum limit
- Athenodorou, Teper (2020): SU(2) glueball spectrum, high precision
- Morningstar, Peardon (1999): Glueball operator construction, cubic group irreps
- Berg, Billoire (2008): SU(2) phase structure
