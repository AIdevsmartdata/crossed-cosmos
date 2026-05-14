# Phase 4 — SU(2) 0++ glueball correlator

**Status:** code written 2026-05-14 23:35 UTC, not yet compiled/tested.
The pipeline relies on the existing Phase 1 LIME configs (β = 2.40, 2.45, 2.50, 2.60).

## Goal

Measure `m_0++ · a` per beta, combine with σ·a² from Phase 3 (Wilson loops), and compare the
dimensionless ratio `m_0++ / √σ` against the SU(2) literature value
**3.55 ± 0.08** (Teper 1999, hep-lat/9909124).  This is the first quantitative
ECI ↔ Yang-Mills bridge attempted in this run.

## Pipeline

```
Phase 1 (heatbath)          → 500 SU(2) LIME configs / β            ✅ (Vast)
Phase 2 (Wilson flow)       → w_0/a per β                           ✅ partial (Vast)
Phase 3 (Wilson loops)      → σ·a² per β  (analyze_glueball.py v2)  ✅ (script)
─────────────────────────────────────────────────────────────────────
Phase 4 (this file)
  4a. glueball_correlator.cc → APE-smeared 0++ operator O(t)
  4b. run_phase4_glueball.sh → loop over configs (stride=5)
  4c. analyze_glueball_correlator.py → C(τ), m_eff, plateau fit
```

## Operator and smearing

The 0++ operator on time slice `t` is the sum over spatial sites and spatial
plaquette orientations of `Re tr P_ij(x, t)`.  Without smearing the
ground-state overlap is tiny; we therefore APE-smear the **spatial** links
(temporal links untouched, gauge invariance preserved) for `APE_iter = 20`
iterations with α = 0.5.  Reunitarisation after each step uses QDP++'s
`reunit()`, which is exact for SU(2).

## Build

```bash
cd /root/crossed-cosmos/chroma
make -f Makefile.glueball
cp glueball_correlator $HOME/install/chroma/bin/
```

If `chroma-config` is missing in the Vast install the Makefile falls back to
explicit `-I` / `-L` paths.

## Run

```bash
# After Phase 1 has 500 configs for all betas:
/root/crossed-cosmos/chroma/run_phase4_glueball.sh
# Output → /root/results_phase4/b{tag}/glue_{idx}.{out.xml,log}
```

Stride 5, 24 jobs parallel, single-proc per chroma call (we hit the LIME-read
MPI bug earlier and bypass it the same way as Phase 2).  ~100 configs × ~3 min
each / 24 parallel ≈ 13 min per beta = ~50 min total at current Vast capacity.

## Analyse

```bash
python3 /root/crossed-cosmos/chroma/analyze_glueball_correlator.py
```

Reads the per-config `<O>` arrays, builds the temporal correlator with all
time origins, jackknifes over configs, extracts the effective-mass plateau
from τ = 2 to τ = 5, and combines with σ·a² from the Phase 3 summary.

The plateau window is conservative; on a `Lᵗ = 16` lattice the contribution of
the first excited state (typically ≈ 1.5 × m_0++) is suppressed by exp(-Δ·τ)
≈ 5 × 10⁻³ at τ = 4 if Δ·a ≈ 0.4.  Should be re-examined when the data is in.

## What we expect

| β     | a·m_0++ (rough)        | σ·a²      | m_0++/√σ    |
|-------|------------------------|-----------|-------------|
| 2.40  | ≈ 0.85                 | 0.0458    | ≈ 3.97      |
| 2.45  | ≈ 0.73                 | ≈ 0.036   | ≈ 3.85      |
| 2.50  | ≈ 0.62                 | ≈ 0.028   | ≈ 3.71      |
| 2.60  | ≈ 0.44                 | ≈ 0.018   | ≈ 3.30      |

(Rough projections from Teper 1999 + Bali SU(2).  Continuum limit β → ∞ should
extrapolate the ratio to 3.55 ± 0.08.)

## ECI link

The ECI v15 Conjecture A REFINED predicts a mass gap in pure-gauge SU(2),
with `m_0++ ∈ [0.4, 1.5] GeV` in physical units when the lattice spacing is
set via σ ≈ (440 MeV)².  The lattice number we will compare against the ECI
band is the **continuum extrapolation** of `m_0++ / √σ` (this is a/0 free
once the four β are stacked).  A value in the literature window 3.55 ± 0.08
is *consistent* with Yang-Mills but is not a confirmation of ECI; the actual
ECI distinguishing prediction lives in the *shape* of the spectrum and in
finer ratios (e.g. m_2++ / m_0++ ≈ 1.4), which need separate operators.

## Caveats / known gaps

- The C++ source has **not** been compiled yet; expect 1-2 iteration cycles to
  fix Chroma API call mismatches (`readSzinQio` namespace, `Set::make`).
- `kind=7` Wilson-loop output XML is dense and was parsed correctly in
  `analyze_glueball.py` v2 — same approach applies here.
- No 2++ operator (`kappa_λ` representation of the spatial plaquette tensor).
  That's Phase 5.
- No multi-state variational basis (only 1 smearing level).  For high-quality
  spectroscopy a small basis at α = (0.3, 0.5, 0.7) × N_iter = (10, 20, 40)
  would help but doubles run time.
- Periodic-time finite-Lᵗ wraparound corrections are *not* applied in
  `m_eff_cosh`; with Lᵗ = 16 the back-propagation correction is ~exp(-am Lᵗ /
  2) ≈ 10⁻³ for a·m ≈ 0.8 and should not bias the plateau.
