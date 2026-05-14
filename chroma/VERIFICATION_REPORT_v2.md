# CHROMA SU(2) GLUEBALL v2 — Source-Verified Rewrite Report

**Date:** 2026-05-14 19:30 UTC  
**Author:** Ξ Gauge subagent  
**Status:** ✅ VERIFIED — 0 fabrications  

## Executive Summary

The `run_chroma_su2_v2.sh` script has been completely rewritten with **every XML tag verified against the actual Chroma source code** at `/tmp/chroma` (JeffersonLab/chroma, master branch). The previous v1 script contained 7 critical fabrications — nonexistent XML tags and measurement names. The v2 script uses only source-verified vocabulary.

---

## What Was Fixed (7 Critical Fabrications → 0)

### Fix 1: Stage 1 — purgaug XML (was `<chroma>+<Driver>`, now `<purgaug>+<HBItr>`)

| v1 (FABRICATED) | v2 (VERIFIED) | Source |
|---|---|---|
| `<chroma>` root | `<purgaug>` root | `purgaug.cc:main` reads `"/purgaug"` |
| `<Driver><type>PureGaugeHMC</type>` | `<HBItr>` with `<GaugeAction>`, `<HBParams>`, `<nrow>` | `purgaug.cc:HBItrParams::read` |
| `<n_warm_up>` | `<NWarmUpUpdates>` | `purgaug.cc:MCControl::read` |
| `<n_production>` | `<NProductionUpdates>` | `purgaug.cc:MCControl::read` |
| Missing | `<NUpdatesThisRun>`, `<SaveInterval>`, `<SaveVolfmt>` | `purgaug.cc:MCControl::read` |
| `<Nc>2</Nc>` in action | Auto-detected from QDP++ `Nc` build | `wilson_gaugeact.h` — no Nc param |
| HMC algorithm | **Heatbath** (HB+OR, correct for SU(2)) | `purgaug.cc:mciter` — single HB sweep |

### Fix 2: Stage 2 — Wilson loop measurement name

| v1 (FABRICATED) | v2 (VERIFIED) | Source |
|---|---|---|
| `<Name>WILSON_LOOP</Name>` | `<Name>WILSLP</Name>` | `inline_wilslp.cc:31` |
| `<r_min>/<r_max>/<t_max>` | `<kind>/<j_decay>/<t_dir>` | `inline_wilslp.cc:Param_t::read` |
| `<smear><ape>...` | `<GaugeState><Name>SIMPLE_GAUGE_STATE</Name>...` | `inline_wilslp.cc:Param_t::read` (version 3) |

### Fix 3: Stage 3 — Wilson flow parameters

| v1 (FABRICATED) | v2 (VERIFIED) | Source |
|---|---|---|
| `<step_size>0.01</step_size>` | `<nstep>300</nstep><wtime>3.0</wtime>` (derived: step_size=wtime/nstep) | `inline_wilson_flow.cc:Param_t::read` |
| `<n_step>300</n_step>` | `<nstep>300</nstep>` | `inline_wilson_flow.cc:Param_t::read` |
| `<measurement_frequency>` | Not a WILSON_FLOW param | Verified absent from source |
| `<stout>...` in flow | WILSON_FLOW uses internal `smear_dirs` | `inline_wilson_flow.cc` — no smearing sub-tag |

### Fix 4: Stage 3 — Glueball measurement name

| v1 (FABRICATED) | v2 (VERIFIED) | Source |
|---|---|---|
| `<Name>GLUEBALL_CORRELATOR</Name>` | `<Name>GLUEBALL_OPS</Name>` | `inline_glueball_ops.cc:119` |
| `<loops><elem><type>Plaquette</type>...` | `<displacement_list><elem>0</elem><elem>1 0</elem>...` | `inline_glueball_ops.cc:Param_t::read` |
| `<irreps><elem>A1g</elem>...` | Irrep not a GLUEBALL_OPS param — done in post-processing | Verified absent from source |
| `<t_min>/<t_max>` | Not a param — time extent from lattice | Verified absent from source |
| HDF5 `.h5` output | Binary DB `.db` output | `inline_glueball_ops.cc` — uses `BinaryStoreDB` |

### Fix 5: Stage 3 — Link smearing name

| v1 (FABRICATED) | v2 (VERIFIED) | Source |
|---|---|---|
| `<stout>...` as a flat tag | `<LinkSmearing><LinkSmearingType><Name>APE_SMEAR</Name>...` | `ape_link_smearing.cc:44` |
| STOUT as flow parameter | STOUT_SMEAR is a LinkSmearingType (not a gauge state) | `stout_link_smearing.cc:44` |

### Fix 6: Config type

| v1 (suspicious) | v2 (VERIFIED) | Source |
|---|---|---|
| `cfg_type="SCIDAC"` | `cfg_type="SZINQIO"` (what purgaug saves) | `purgaug.cc:saveState` uses `CFG_TYPE_SZINQIO` |

### Fix 7: MPI + Parallelism

| v1 (BUG) | v2 (FIXED) | Notes |
|---|---|---|
| `mpirun -np 1` hardcoded | `purgaug` runs single-MPI internally; chroma measurements parallelized via `xargs -P` | `MPI_PROCS` now used for xargs parallelism |
| Sequential for-loop | `stage_loops_parallel()` + `stage_flow_glue_parallel()` with `xargs -P $((MPI_PROCS/2))` | Config-level parallelism |

---

## Verified XML Tags — Complete Registry

### purgaug binary (`/purgaug`)
```
Cfg/cfg_type, Cfg/cfg_file
MCControl/RNG/Seed/elem
MCControl/StartUpdateNum, NWarmUpUpdates, NProductionUpdates
MCControl/NUpdatesThisRun, SaveInterval, SavePrefix, SaveVolfmt
HBItr/GaugeAction/Name, beta, AnisoParam/anisoP, GaugeState/Name, GaugeBC/Name
HBItr/HBParams/nOver, NmaxHB
HBItr/nrow
InlineMeasurements/elem/Name, Frequency, Param, NamedObject
```

### chroma binary (`/chroma`)
```
Param/nrow
Param/InlineMeasurements/elem/...
Cfg/cfg_type, Cfg/cfg_file
RNG/Seed/elem (optional)
```

### Inline Measurements (verified names)
```
WILSLP, WILSON_FLOW, GLUEBALL_OPS, PLAQUETTE, POLYAKOV_LOOP,
GLUEBALL_MATELEM_COLORVEC, GLUEBALL_DIAG_MATELEM_COLORVEC,
QTOP_NAIVE, QACTDEN, PLAQ_DENSITY, FUZZED_WILSON_LOOP,
APPLY_GAUGE_STATE, RANDOM_GAUGE_TRANSF
```

### Gauge Actions (verified names)
```
WILSON_GAUGEACT
```

### Gauge States (verified names)
```
SIMPLE_GAUGE_STATE, PERIODIC_GAUGE_STATE, STOUT_GAUGE_STATE
```

### Link Smearing Types (verified names)
```
APE_SMEAR, STOUT_SMEAR, HYP_SMEAR, PHASE_STOUT_SMEAR, NONE
```

### Config Types (verified names)
```
WEAK_FIELD, SZINQIO, SZIN, NERSC, SCIDAC, MILC, KYU, WUP,
DISORDERED, UNIT, CPPACS, CERN, CLASSICAL_SF
```

### VOLFMT Types (verified names)
```
SINGLEFILE, MULTIFILE, PARTFILE
```

---

## Parameter Changes vs v1

| Parameter | v1 | v2 | Reason |
|---|---|---|---|
| Algorithm | HMC | Heatbath (purgaug) | SU(2) exact; purgaug is the Chroma pure gauge binary |
| sweeps per config | traj_length=1.0, n_steps=100 | 1 HB + 3 OR per update | HB is exact per sweep; 3 OR improves decorrelation |
| N_updates | N_CONFIGS × TRAJ_STEP = 1000 | N_PROD = 1000, SaveInterval = 2 → 500 configs | Same effective config count |
| Wilson loop smearing | `<smear><ape>` (fabricated XML) | `<GaugeState><Name>SIMPLE_GAUGE_STATE</Name>` | Correct WILSLP v3 API |
| Flow time | step_size=0.01, n_step=300 | wtime=3.0, nstep=300 | step_size = wtime/nstep = 0.01 (derived, not input) |
| Glueball smearing | `<stout>...` (not in WILSON_FLOW) | APE_SMEAR with 5 steps, α=0.5, no time smear | Standard choice; STOUT_SMEAR available as alternative |
| DB output files | .h5 | .db (BinaryStoreDB) | Chroma uses QDP++ BinaryStoreDB, not HDF5 for glue ops |
| Config type | SCIDAC | SZINQIO | purgaug saves SZINQIO; reading back must match |

---

## Estimated Runtime (Corrected)

| Stage | Time/β (16⁴, 24 cores) | Notes |
|---|---|---|
| Stage 1: Heatbath | 0.5–1.5 h | HB is fast; 1000 sweeps × 16⁴ × SU(2) |
| Stage 2: Wilson loops | 0.5–1 h | xargs -P 12; ~30s/config |
| Stage 3: Flow+glue | 3–6 h | Dominant cost; Flow: ~20-40s/config, Glueball: ~10-20s/config |
| Stage 4: Analysis | 5 min | Python post-processing |
| **Total/β** | **4–8.5 h** | Down from 6-12h v1 estimate (HB faster than HMC) |
| **All 3 β** | **12–25 h** | With parallel stages |

On ssh2.vast.ai (24 cores, $0.069/h): **$0.83–1.73 total**.

---

## Remaining Work (Not in v2)

1. **glueball_op DB reader**: The GLUEBALL_OPS binary DB format requires `chroma_utils` C++ code for reading. A Python wrapper or standalone C++ extractor is needed. `chroma_utils` is installed in Stage 0 but the Python analysis stage needs to call it.

2. **Irrep projection**: The elemental operators from GLUEBALL_OPS need to be contracted into A1g, Eg, T2g irreps. This requires the cubic group projection coefficients (available in standard lattice literature).

3. **GEVP implementation**: The GEVP algorithm itself is available in `analyze_gevp.py` but needs data input plumbing.

4. **chroma_utils build**: `chroma_utils` is cloned but not built (requires same QDP++/QMP environment). The `extract_glueball` tool in chroma_utils reads binary DB → ASCII.

5. **Continuum extrapolation**: With 3 β points (2.40, 2.50, 2.60), a linear a²σ → 0 extrapolation is possible. The v2 script provides the a√σ values from Stage 4a.

---

## Source Verification Log

All tags verified against these files in `/tmp/chroma`:

| File | Lines Verified | Content |
|---|---|---|
| `mainprogs/main/purgaug.cc` | 1–350 | purgaug XML schema, MCControl, HBItr |
| `mainprogs/main/chroma.cc` | 1–80 | chroma measurement binary schema |
| `lib/meas/inline/glue/inline_wilson_flow.cc` | 1–160 | WILSON_FLOW params (nstep, wtime, t_dir, smear_dirs) |
| `lib/meas/inline/glue/inline_wilslp.cc` | 1–80 | WILSLP params (version 3, kind, j_decay, t_dir, GaugeState) |
| `lib/meas/inline/glue/inline_glueball_ops.cc` | 1–560 | GLUEBALL_OPS params (displacement_list, LinkSmearing, etc.) |
| `lib/actions/gauge/gaugeacts/wilson_gaugeact.cc` | 1–60 | WILSON_GAUGEACT name, beta, AnisoParam |
| `lib/actions/gauge/gaugestates/simple_gaugestate.cc` | 24 | SIMPLE_GAUGE_STATE name |
| `lib/meas/smear/ape_link_smearing.cc` | 1–140 | APE_SMEAR params (link_smear_num, link_smear_fact, no_smear_dir) |
| `lib/meas/smear/stout_link_smearing.cc` | 1–120 | STOUT_SMEAR params |
| `lib/io/enum_io/enum_cfgtype_io.cc` | 1–30 | Valid cfg_type strings |
| `lib/io/enum_io/enum_qdpvolfmt_io.cc` | 1–20 | Valid volfmt strings |
| `tests/purgaug/purgaug.ini.xml` | 1–70 | Canonical purgaug input |
| `tests/chroma/glue/wilson_flow/wilson_flow.ini.xml` | 1–40 | Canonical WILSON_FLOW input |
| `tests/chroma/glue/wilslp/wilslp.ini.xml` | 1–60 | Canonical WILSLP input |

**Fabrications: 0**

---

## Post-Review Fix: WILSLP Output Parser

The Stage 4a Python parser was corrected to match the actual WILSLP output XML format (verified against `meas/glue/wilslp.cc`):

| Previous (assumed) | Correct (verified) |
|---|---|
| `<ReTr>/<ImTr>` elements | `<loop>` array with whitespace-separated values |
| Flat `<R>/<T>` per element | `<wils_loop2>/<wloop2>/<elem><r>R</r><loop>W(R,0) W(R,1) ...</loop>` |

WILSLP v3 writes three loop types:
- `<wils_loop1>`: space-space planar (R×R squares, not used for string tension)
- `<wils_loop2>`: time-like planar (R×T rectangles, used for Creutz ratios)
- `<wils_loop3>`: off-axis time-like (if kind has bit 4 set)

Creutz ratios are extracted from `wils_loop2` data using the standard formula:
χ(R,T) = -ln(W(R,T)·W(R-1,T-1) / (W(R,T-1)·W(R-1,T)))
