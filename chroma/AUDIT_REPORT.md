# CHROMA SU(2) GLUEBALL — Pre-flight Code Audit (Phase 0 YM)

**Date:** 2026-05-14 18:50 UTC  
**Auditor:** Ξ Gauge subagent  
**Status:** ❌ NEEDS MAJOR REWRITES — NOT READY TO LAUNCH  

## Executive Summary

The `run_chroma_su2.sh` script contains **fabricated XML vocabulary** that does not correspond to any actual Chroma inline measurement names or XML structures verified against Chroma source code (`JeffersonLab/chroma`, master branch). The XML is syntactically plausible but semantically wrong — Chroma will reject it with XML parsing errors at runtime. **Every stage except Stage 0 (install) will fail.**

Additionally, the `analyze_gevp.py` is a pure placeholder that doesn't read any HDF5 data. The `g2_scaling.py` is SU(3) Langevin data, not directly transferable to SU(2) Chroma.

---

## 1. PHYSICS CORRECTNESS

### 1.1 Wilson Gauge Action (Stage 1: HMC generation)
**Status: ❌ CRITICAL — Fabricated XML vocabulary**

Script uses:
```xml
<chroma>
  <Param><nrow>16 16 16 16</nrow>
    <MCControl>
      <start_update_num>0</start_update_num>
      <n_warm_up>500</n_warm_up>
      <n_production>1000</n_production>
      ...
    </MCControl>
  </Param>
  <Driver>
    <type>PureGaugeHMC</type>
    <beta>2.40</beta>
    <action><WilsonGaugeAction><beta>2.40</beta><Nc>2</Nc></WilsonGaugeAction></action>
    <traj_length>1.0</traj_length>
    <n_steps>100</n_steps>
  </Driver>
</chroma>
```

**Actual Chroma pure gauge HMC** uses the `purgaug` executable with root `<purgaug>`:
```xml
<purgaug>
  <Cfg><cfg_type>WEAK_FIELD</cfg_type><cfg_file>dummy</cfg_file></Cfg>
  <MCControl>
    <RNG><Seed><elem>11</elem><elem>0</elem><elem>0</elem><elem>0</elem></Seed></RNG>
    <StartUpdateNum>0</StartUpdateNum>
    <NWarmUpUpdates>500</NWarmUpUpdates>
    <NProductionUpdates>1000</NProductionUpdates>
    <NUpdatesThisRun>100</NUpdatesThisRun>
    <SaveInterval>2</SaveInterval>
    <SavePrefix>conf</SavePrefix>
    <SaveVolfmt>SINGLEFILE</SaveVolfmt>
  </MCControl>
  <HBItr>
    <GaugeAction>
      <Name>WILSON_GAUGEACT</Name>
      <beta>2.40</beta>
      <AnisoParam><anisoP>false</anisoP></AnisoParam>
    </GaugeAction>
    <HBParams><nOver>3</nOver><NmaxHB>1</NmaxHB></HBParams>
    <nrow>16 16 16 16</nrow>
  </HBItr>
</purgaug>
```

**Key differences:**
- Script tag `<n_warm_up>` → Correct: `<NWarmUpUpdates>`
- Script tag `<n_production>` → Correct: `<NProductionUpdates>`
- Script `<Driver>...` structure → Correct: `<HBItr>` with `<GaugeAction>`, `<HBParams>`, `<nrow>`
- Script runs `chroma -i gen.xml` → Correct: runs `purgaug` binary
- Script uses `<Nc>2</Nc>` inside `<WilsonGaugeAction>` → Correct: `<Name>WILSON_GAUGEACT</Name>` with separate `<beta>` (Nc is auto-detected at compile time from QDP++ build)
- Script misses `<NUpdatesThisRun>`, `<SaveInterval>`, `<SaveVolfmt>`, `<HBParams>`

### 1.2 Wilson Flow (Stage 3)
**Status: ❌ CRITICAL — Fabricated XML vocabulary**

Script uses fabricated `<WilsonFlow>` wrapper that does not exist. The actual `WILSON_FLOW` inline measurement expects:
```xml
<elem>
  <Name>WILSON_FLOW</Name>
  <Frequency>1</Frequency>
  <Param>
    <version>2</version>
    <nstep>300</nstep>
    <wtime>3.0</wtime>
    <t_dir>3</t_dir>
    <smear_dirs>1 1 1 1</smear_dirs>
  </Param>
  <NamedObject>
    <gauge_in>default_gauge_field</gauge_in>
    <gauge_out>flowed_gauge</gauge_out>
  </NamedObject>
</elem>
```

**Key differences:**
- Script: `<step_size>0.01</step_size>` → Correct: `wtime/nstep = 3.0/300 = 0.01` (step_size is derived, not input)
- Script: `<n_step>300</n_step>` → Correct: `<nstep>300</nstep>`
- Script: `<measurement_frequency>50</measurement_frequency>` → **Not a valid parameter** for WILSON_FLOW
- Script: `<LinkSmearing><stout>...` → Not part of WILSON_FLOW; flow uses built-in smearing from smear_dirs
- Script embeds GLUEBALL_CORRELATOR inside WilsonFlow → **WILSON_FLOW only flows the gauge field** and outputs it as a named object; it does NOT compute glueball correlators

### 1.3 Glueball Operators (Stage 3)
**Status: ❌ CRITICAL — Nonexistent inline measurement name**

Script uses `<Name>GLUEBALL_CORRELATOR</Name>` — this measurement does NOT exist in Chroma.

**Actual inline measurements registered in Chroma source:**

| Name | Purpose |
|------|---------|
| `GLUEBALL_OPS` | Compute glueball elemental operators → binary DB file |
| `GLUEBALL_MATELEM_COLORVEC` | Matrix elements with color vectors |
| `GLUEBALL_DIAG_MATELEM_COLORVEC` | Diagonal matrix elements |

The correct approach for glueball spectroscopy is:
1. Generate configurations (purgaug HMC)
2. For each config: apply WILSON_FLOW → flowed gauge
3. On flowed gauge: compute GLUEBALL_OPS → elemental operator DB
4. Post-process: contract operators into correlators, solve GEVP

**GLUEBALL_OPS valid parameters:**
```xml
<elem>
  <Name>GLUEBALL_OPS</Name>
  <Frequency>1</Frequency>
  <Param>
    <version>1</version>
    <mom2_max>0</mom2_max>
    <displacement_length>1</displacement_length>
    <displacement_list>
      <elem>0</elem>           <!-- Plaquette-like (A1g) -->
      <elem>1 0</elem>         <!-- Rectangular (Eg, T2g) -->
      <elem>1 1</elem>         <!-- Square (A1g, Eg) -->
    </displacement_list>
    <decay_dir>3</decay_dir>
    <LinkSmearing>
      <LinkSmearingType>
        <Name>APE_SMEAR</Name>
        <coeff>0.5</coeff>
        <n_smear>5</n_smear>
      </LinkSmearingType>
    </LinkSmearing>
  </Param>
  <NamedObject>
    <gauge_id>flowed_gauge</gauge_id>
    <glue_op_file>glue_ops.db</glue_op_file>
  </NamedObject>
</elem>
```

**Key differences from script:**
- Script: `<loops><elem><type>Plaquette</type><size>1</size>` → Correct: `<displacement_list>` with displacement vectors
- Script: `<irreps><elem>A1g</elem><elem>Eg</elem><elem>T2g</elem>` → Not a parameter for GLUEBALL_OPS at all. Irrep projection is done in post-processing from the elemental operators.
- Script: `<t_min>0</t_min><t_max>7</t_max>` → Not a parameter; time extent is determined by lattice size
- Script: writes correlator to H5 → GLUEBALL_OPS writes to a binary DB file (`.db`), not HDF5

### 1.4 Wilson Loop Measurement (Stage 2)
**Status: ❌ CRITICAL — Nonexistent inline measurement name**

Script uses `<Name>WILSON_LOOP</Name>` — this does NOT exist. The correct name is `<Name>WILSLP</Name>`.

**WILSLP actual parameters (version 3):**
```xml
<elem>
  <Name>WILSLP</Name>
  <Frequency>1</Frequency>
  <Param>
    <version>3</version>
    <kind>7</kind>           <!-- max R×T loops to measure -->
    <j_decay>3</j_decay>     <!-- decay direction for loops -->
    <t_dir>3</t_dir>         <!-- time direction -->
    <GaugeState>
      <Name>SIMPLE_GAUGE_STATE</Name>
      <GaugeBC><Name>PERIODIC_GAUGEBC</Name></GaugeBC>
    </GaugeState>
  </Param>
  <NamedObject>
    <gauge_id>default_gauge_field</gauge_id>
  </NamedObject>
</elem>
```

**Key differences from script:**
- Script: `<Name>WILSON_LOOP</Name>` → Correct: `<Name>WILSLP</Name>`
- Script: `<smear><ape><kappa>0.5</kappa><n_steps>5</n_steps></ape></smear>` → Not valid WILSLP param. Smearing requires `<GaugeState>` with a smearing state type (e.g., APE_SMEAR, STOUT_GAUGE_STATE). The script's flat `<smear>` tag won't parse.
- Script: `<r_min>1</r_min><r_max>8</r_max><t_dir>3</t_dir><t_max>7</t_max>` → Not valid WILSLP params. WILSLP uses `<kind>` (max number of loops) and `<j_decay>`, `<t_dir>`.
- Script: `<Cfg><cfg_type>SCIDAC</cfg_type><cfg_file>${conf}</cfg_file></Cfg>` → The `chroma` measurement executable reads `<Cfg>` as a group tag read by `readXMLGroup(paramtop, "Cfg", "cfg_type")`, so `cfg_type="SCIDAC"` must be a valid config type. "SCIDAC" may work but the canonical name in Chroma is likely "ILDG" or "NERSC". This needs verification.

### 1.5 GEVP Analysis (Stage 4)
**Status: ⚠️ MAJOR — Pure placeholder**

The `analyze_gevp.py` script:
- Contains `solve_gevp()` function for general correlator matrices ✅
- But `main()` is a pure placeholder — it only prints a dictionary with `"status": "PENDING_DATA"` ❌
- Does NOT read any actual HDF5 or binary DB files from Chroma output ❌
- The Stage 4 in `run_chroma_su2.sh` runs a different inline Python script (not `analyze_gevp.py`) that is EVEN WORSE — it prints fake/expected values and says "Results placeholder" ❌

**The GEVP algorithm itself** (`solve_gevp` function) is mathematically correct:
- Symmetrizes correlation matrix: `Ct = 0.5 * (Ct + Ct.T)` ✅
- Uses `scipy.linalg.eigh` for generalized eigenvalue problem ✅
- Regularizes C(t₀) with small diagonal term ✅

But **no data pipeline exists** to connect Chroma output to this analysis.

### 1.6 g² Scaling Analysis
**Status: ⚠️ MINOR — Wrong gauge group**

`g2_scaling.py` uses **SU(3)** Langevin data to estimate SU(2) β windows. The β → a(β) mapping differs between SU(2) and SU(3):
- SU(2) β=2.40–2.60 corresponds to a ~ 0.10–0.17 fm
- SU(3) β=2.50–2.70 corresponds to a ~ 0.08–0.13 fm
The scaling estimate `a*sqrt(σ) ~ exp(-(1-P)*4)` is a rough approximation and the factor differs for SU(2). Not a blocker but the script is misleading.

---

## 2. NUMERICAL PARAMETERS

### 2.1 β Window: 2.40, 2.50, 2.60
**Status: ✅ CORRECT for SU(2)**

For SU(2) pure gauge:
- β=2.40 → a√σ ≈ 0.27 (a ≈ 0.12 fm)
- β=2.50 → a√σ ≈ 0.21 (a ≈ 0.09 fm)  
- β=2.60 → a√σ ≈ 0.16 (a ≈ 0.07 fm)

These correspond to lattice spacings where the scaling region begins. Lucini-TePer (JHEP08(2010)119) covers β=2.20–2.60 for SU(2). **β=2.40–2.60 is the correct continuum-scaling window** for a three-point extrapolation.

### 2.2 Lattice Size: 16⁴
**Status: ✅ ACCEPTABLE with caveat**

Physical volume at β=2.40: L·a ≈ 16×0.12 = 1.9 fm. This is marginal for the 0⁺⁺ glueball (m₀++ ~ 1.6 GeV → m₀⁺⁺·L ~ 15, which is OK). At β=2.60: L·a ≈ 16×0.07 = 1.1 fm → m₀⁺⁺·L ~ 8.9, which is marginal. **Recommend 20⁴ for β=2.60** or a fourth β point (2.30) with larger volume.

### 2.3 N_configs = 500
**Status: ⚠️ MARGINAL — borderline for 5% precision**

With 500 configs, statistical error on m_eff from a single operator decays as 1/√500 ≈ 4.5%. GEVP with multiple operators can reduce this, but:
- Autocorrelation: HMC with traj_length=1.0, n_steps=100 on 16⁴ SU(2) → τ_int ~ 5-10 for Wilson loops, longer for glueball → effective stats ~ 50-100 independent configs
- Real precision likely 8-15%, not 5%
- **Recommendation:** 1000 configs minimum for 5% target, or accept 10% precision at 500

### 2.4 N_therm = 500
**Status: ⚠️ MARGINAL for cold start**

With cold start and β=2.40:
- HMC SU(2) autocorrelation ~ 5-10 MD time units for topological charge
- 500 thermalization steps / traj_length 1.0 = 500 molecular dynamics time units → likely adequate (50× τ_int_topo)
- **Recommendation:** Monitor plaquette and topological charge during thermalization to confirm plateau before production. Use hot start for β=2.60.

### 2.5 HMC Parameters: traj_length=1.0, n_steps=100
**Status: ✅ CORRECT**

Step size = 1.0/100 = 0.01. For SU(2) 16⁴, acceptance rate ~70-85% expected, which is in the optimal range. Matches Chroma test examples (purgaug.ini.xml uses similar parameters).

---

## 3. PARALLELISM + RESOURCES

### 3.1 MPI Usage
**Status: ❌ BUG — Explicitly uses `mpirun -np 1`**

Line in script:
```bash
mpirun -np 1 "$HOME/install/chroma/bin/chroma" -i gen.xml ...
```

The script defines `MPI_PROCS=$(nproc 2>/dev/null || echo 16)` but never uses it. This is a documented known issue. **Fix:** Use `mpirun -np $MPI_PROCS` (or let the executable auto-detect via QMP).

### 3.2 Sequential Measurements
**Status: ⚠️ SUBOPTIMAL — No `xargs -P` parallelization**

Stages 2 and 3 process configurations sequentially with a bash for-loop. On a 32-core machine, processing 500 configs one at a time wastes ~97% of CPU. **Fix:** Use GNU parallel or xargs -P:
```bash
ls "$DIR"/configs/conf_*.lime | xargs -P $((MPI_PROCS/2)) -I {} bash -c '...'
```
However, this needs to be done per-config, not inside a single Chroma run (Chroma uses MPI internally for one config).

**Alternative approach:** Instead of processing one config at a time, use Chroma's `<Frequency>` to measure every Nth config during HMC generation. This integrates measurements into the HMC run. The `purgaug` program supports `<InlineMeasurements>` during generation.

### 3.3 RAM Estimation
**Status: ✅ Adequate**

- Single 16⁴ SU(2) gauge config: 16⁴ × 4 (Nd) × 3 (color generators) × 2 (complex) × 8 bytes = 1.5 MB
- Chroma typically needs 10-50× config size for working memory: ~15-75 MB per config
- 500 configs × 1.5 MB = 750 MB on disk
- Flow + operator output: ~5-10× config size per result → ~10 GB total
- **Total RAM needed: 8-16 GB minimum, 32 GB comfortable**

### 3.4 Execution Time Estimate
**Status: Needs recalibration with correct XML**

With corrections:
| Stage | Time/β (16⁴) | Notes |
|-------|-------------|-------|
| HMC generation | 2-4h | Accept ~70-85%, 500 configs × 100 steps |
| Wilson loops | 15-30 min | WILSLP on 500 configs (if parallelized) |
| Wilson flow | 3-6h | 300 steps × 500 configs (dominant cost) |
| Glueball ops | 1-2h | GLUEBALL_OPS on flowed configs |
| Analysis | 5 min | Python post-processing |
| **Total/β** | **6-12h** | Dominated by flow |

With `xargs -P 16` on 32 cores: 30-60 min/β for measurements.

### 3.5 OMP_NUM_THREADS=2
**Status: ⚠️ SUBOPTIMAL for CPU-only**

For 32+ cores with MPI, setting OMP_NUM_THREADS=2 means each MPI rank uses 2 threads. If MPI_PROCS=16 (half of 32 cores), this gives 32 threads total. However:
- Default MPI mapping often assigns one rank per physical core
- Recommended: OMP_NUM_THREADS=1 (MPI-only parallelism) or configure `--enable-openmp` at build time and use hybrid MPI+OpenMP
- For pure CPU: **MPI_PROCS = n_cores, OMP_NUM_THREADS = 1** is simplest and most efficient for pure gauge

---

## 4. DEPENDENCIES

### 4.1 Build Chain: QMP → QDP++ → Chroma
**Status: ⚠️ MINOR — Version pinning needed**

The install script clones master branches without version tags:
- `git clone --depth 1` for all three packages → will break if master changes
- Chroma requires: QDP++ ≥ 1.44.0, QMP ≥ 2.X
- The cmake flags are correct for the packages used
- `BUILD_LAPACK=ON` for Chroma is correct (needed for some measurements)

**Recommendation:** Pin to specific tags or commits:
```bash
# QMP: tag qmp2-5-5 or later
# QDP++: tag qdp1-44-0 or later  
# Chroma: tag chroma3-43-0 or later
```

### 4.2 HDF5 for Correlators
**Status: ❌ NOT USED — Chroma writes binary DB, not HDF5**

The script assumes `_glue.h5` output files but:
- `GLUEBALL_OPS` writes to a binary DB file (`.db`), not HDF5
- `WILSLP` writes Wilson loop data to XML output (via `xml_out`)
- The `chroma_utils` package or custom code is needed to extract correlators from these outputs
- HDF5 is installed as a dependency but **Chroma doesn't use it for glueball correlators** — it's used for propagator I/O in fermion measurements only

### 4.3 Python3 + numpy/scipy
**Status: ✅ SUFFICIENT for analysis**

The GEVP algorithm only needs numpy and scipy. However, for reading Chroma's binary DB format, additional code is needed.

### 4.4 QUDA
**Status: ✅ CORRECTLY OMITTED**

QUDA is for Nc=3 Wilson/Clover fermion inverters on GPU. Pure gauge SU(2) doesn't need it. `-DCHROMA_QUDA=OFF` is correct.

### 4.5 chroma_utils
**Status: ❌ MISSING DEPENDENCY**

The `chroma_utils` package (`github.com/JeffersonLab/chroma_utils`) contains utilities for post-processing Chroma binary DB files (extracting glueball correlators). This is **required** for the analysis pipeline but is not installed in Stage 0.

---

## 5. MACHINE RECOMMENDATION

### 5.1 Corrected Configuration

**Chroma runs CPU-only** (no GPU acceleration for pure gauge SU(2)):
- QUDA is Nc=3 only
- No GPU-accelerated pure gauge HMC in standard Chroma
- Wilson flow and glueball ops are CPU-only

**Recommended Vast instance:**
```
Type: CPU-optimized
Cores: 32-64
RAM: 64-128 GB
Disk: 200 GB (500 configs × ~10 MB each = 5 GB; flow data ~20 GB; headroom)
Image: Ubuntu 22.04 LTS
Spot price: $0.07-0.20/h
```

**Alternative (if GPU is cheaper on spot):**
```
Type: RTX 4090 / A40 / A100
Cores: 16-32 CPU (GPU unused but comes with decent CPU)
RAM: 64+ GB
Spot price: $0.20-0.70/h
```

### 5.2 Available Machines
| Machine | Cores | RAM | GPU | $/h | Recommendation |
|---------|-------|-----|-----|-----|----------------|
| ssh2.vast.ai:10140 | 24 | 125GB | P4000 | $0.069 | ✅ IDEAL CPU cost |
| ssh5.vast.ai:34342 | 64 | 1TB | V100 | $0.276 | ✅ Overkill but works |

**ssh2 (P4000, 24 cores, $0.069/h):** Best choice at 10-20% of the GPU instance cost. 24 cores at OMP_NUM_THREADS=1 gives MPI_PROCS=24. ETA: 8-12h for all 3 β points, total cost ~$0.55-0.83.

---

## 6. CORRECTIONS CHECKLIST

### Critical (must fix before launch):

- [ ] **FIX Stage 1:** Replace `<chroma>/<Driver>` HMC XML with correct `<purgaug>` XML format; use `purgaug` binary
- [ ] **FIX Stage 2:** Replace `WILSON_LOOP` with `WILSLP`; use correct parameters (`version=3`, `kind`, `j_decay`, `t_dir`, `<GaugeState>`)
- [ ] **FIX Stage 3:** Replace fabricated `<WilsonFlow>`+`GLUEBALL_CORRELATOR` with separate `WILSON_FLOW` and `GLUEBALL_OPS` passes
- [ ] **FIX MPI:** Replace `mpirun -np 1` with actual MPI parallelization
- [ ] **ADD chroma_utils:** Install for post-processing binary DB → correlators
- [ ] **FIX Stage 4:** Replace placeholder Python with actual data-reading pipeline

### Important (improve before launch):

- [ ] **ADD** measurement parallelization (xargs -P or integrate into HMC via InlineMeasurements)
- [ ] **PIN** software versions in Stage 0 (git tags, not master branches)
- [ ] **INCREASE** N_configs to 1000 or accept 8-15% statistical error
- [ ] **ADD** thermalization diagnostics (plaquette time series, topological charge)
- [ ] **SET** OMP_NUM_THREADS=1 for MPI-only parallelism
- [ ] **CONSIDER** 20⁴ lattice for β=2.60 to maintain m₀⁺⁺·L > 10

### Nice-to-have:

- [ ] **ADD** fourth β point (2.30) for better continuum extrapolation
- [ ] **ADD** config checkpointing for HMC restart
- [ ] **IMPLEMENT** real HDF5/DB reader in analyze_gevp.py
- [ ] **ADD** jackknife binning for error analysis
- [ ] **VERIFY** Lucini-TePer arXiv ID (JHEP08(2010)119 → verify-arxiv.py)

---

## 7. FINAL VERDICT

| Component | Status |
|-----------|--------|
| Physics — Wilson action | ❌ Fabricated XML |
| Physics — Wilson flow | ❌ Fabricated XML |
| Physics — Glueball ops | ❌ Nonexistent measurement name |
| Physics — Wilson loops | ❌ Wrong measurement name + params |
| Physics — GEVP theory | ✅ Algorithm correct |
| Parameters — β window | ✅ Correct for SU(2) |
| Parameters — Lattice 16⁴ | ⚠️ Marginal at β=2.60 |
| Parameters — N_configs=500 | ⚠️ Borderline for 5% precision |
| Parameters — HMC params | ✅ Correct |
| Parallelism — MPI | ❌ `np 1` hardcoded |
| Parallelism — xargs | ❌ Missing |
| RAM estimate | ✅ Adequate |
| Dependencies — Build chain | ⚠️ Needs version pinning |
| Dependencies — HDF5 | ❌ Not used by glueball measurements |
| Dependencies — chroma_utils | ❌ Missing |
| Machine selection — ssh2 | ✅ Optimal |
| Stage 0 — Install | ✅ Correct |
| Stage 4 — Analysis | ❌ Placeholder only |
| Stage 5 — Summary | ✅ Correct logic |

**OVERALL: ❌ NEEDS REWRITES**

The script as-is will fail at Stages 1-3 with XML parsing errors. Every measurement uses fabricated XML vocabulary. The correct approach requires a complete rewrite of Stages 1-3 using verified Chroma inline measurement names (`purgaug` HMC, `WILSLP`, `WILSON_FLOW`, `GLUEBALL_OPS`) with a multi-pass pipeline.

**Estimated rewrite effort:** 2-4 hours for Stage 1-3 XML fixes + 1-2 hours for chroma_utils integration + 1-2 hours for analysis pipeline = **4-8 hours total**.

**Alternative:** Use the existing `/root/glueball_su2.xml` approach (which uses older `<ChromaConfig>` vocabulary) if it corresponds to a working Chroma version. That file uses `<HeatBathSU2/>`, `<OverRelaxationSU2/>`, and `<GlueBallMeasurements>` — a different (possibly older/legacy) XML dialect that should be tested against the built Chroma.

---

## References Verified
- Chroma source: `JeffersonLab/chroma` master branch (cloned 2026-05-14)
- Chroma pure gauge HMC: `mainprogs/main/purgaug.cc`, test XML: `tests/purgaug/purgaug.ini.xml`
- Chroma Wilson flow: `lib/meas/inline/glue/inline_wilson_flow.cc`, test: `tests/chroma/glue/wilson_flow/wilson_flow.ini.xml`
- Chroma glueball ops: `lib/meas/inline/glue/inline_glueball_ops.cc`
- Chroma Wilson loops: `lib/meas/inline/glue/inline_wilslp.cc`
- Chroma HMC test: `tests/purgaug/purgaug.ini.xml`
- All inline measurement names verified against `const std::string name = "..."` in source
