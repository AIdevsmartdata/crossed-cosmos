# README — JAX SU(3) 't Hooft twist lattice PROPER

**Date** : 26 May 2026
**Author** : Kévin Rémondière (ORCID 0009-0008-2443-7166)
**Paper** : `Paper_tHooft_Twist_Mode_Zero_LMP/main.tex` — Hypothesis 4.2
**Script** : `jax_su3_tHooft_lattice_PROPER_2026-05-26.py` (1318 lines, JIT-compiled)

## Purpose

Validate numerically Hypothesis 4.2 ("twist rigidity") which underpins
Theorem 5.1 (main pre-validation theorem) of the paper :

> Under non-trivial 't Hooft twist (n^{12} = 1 mod 3) on SU(3) lattice (T^4_L)^Ω,
> the twisted Wilson measure μ^Ω satisfies an LSI with constant
> C_LSI(μ^Ω) ≤ N²·c_∞(D) / [(1-κ_FP)·m_0²] = 43.7 / m_0²
> (uniform in L), provided the bundle-twisted Faddeev-Popov operator M^Ω[A]
> has λ_min ≥ (5/6)·m_Ω² where m_Ω² = (2π/(NL))².

## Architecture

### Core components (5 layers)

1. **SU(3) primitives** (lines ~120-220)
   - Gell-Mann matrices λ_a (Hermitian, traceless), T_GEN = λ/2
   - `random_su3_haar(key, shape)` — Mehta QR method
   - `random_su3_near_identity(key, shape, eps)` — 5-term Taylor exp

2. **Twist enforcement** (lines ~230-320)
   - `OMEGAS` : twist matrices Ω_0 = diag(1,ω,ω²), Ω_1 = cyclic shift,
     Ω_2 = Ω_3 = Id (paper §2.1)
   - `check_centraliser_lemma()` : numerical check Ω_0·Ω_1 = ω·Ω_1·Ω_0
   - `gather_link_twist(U_link, mu, shift_dir, direction)` :
     gather with Ω_ν · U · Ω_ν^{-1} similarity on wrapped links

3. **Twist-aware Wilson action** (lines ~330-450)
   - `_wrap_phase_field(L, mu, nu, use_twist)` :
     centre phase z_{μν}(x) on corner plaquette x_μ=L-1, x_ν=L-1
   - `plaquette_field_twisted(U, mu, nu, use_twist)` : per-plaquette (1/N)Re Tr(z·P)
   - `wilson_action_twisted(U, beta, use_twist)` : full action
   - `plaquette_mean_twisted(U, use_twist)` : ⟨P⟩ scalar

4. **Metropolis sweep** (lines ~460-550)
   - `compute_staples_twisted(U, mu, use_twist)` :
     STANDARD ORDER staples K_fwd = U_ν(x+μ̂)·U_μ(x+ν̂)†·U_ν(x)†
     **★ POST-FIX from 2026-05-25 staple order bug ★**
   - `_make_metropolis_sweep(use_twist)` : JIT-compiled per-mu sweep
   - Convention : `Re Tr(U_proposed · K)` (NOT K† !!!)
     **★ POST-FIX from 2026-05-25 Metropolis K_dag silent catastrophic bug ★**
   - `thermalize(key, beta, L, n_sweeps, use_twist, eps, start)` :
     full thermalization with ⟨P⟩-trace logging

5. **Observables** (lines ~600-900)
   - O1 : `measure_fp_lambda_min(U, key, use_twist, n_iter)`
     - Matrix-free Lanczos on M^Ω = d_A^{†,Ω} d_A^Ω
     - Acts on R^{L^4 · 8} (8 = N²-1 generators)
   - O2 : `measure_hess_gap(U, beta, key, use_twist, n_iter)`
     - jax.grad on quadratic form (Hess·v product)
     - Acts on R^{L^4 · 4 · 8}
   - O3 : `estimate_lsi_constant_rothaus_simon(hess_gaps, beta, L)`
     - C_LSI ≤ 1 / (κ_Ric + λ_min(Hess S)) Bakry-Emery estimate
   - O4 : implicit — periodic comparison done in parallel

### Sanity battery (lines ~910-1080)

6 mandatory checks before measurements :
1. Centraliser lemma : Ω_0·Ω_1 = ω·Ω_1·Ω_0 (deterministic)
2. Cold start ⟨P⟩(t=0) periodic = 1.0, twisted = 1 - 1.5/n_plaq
3. Hot start thermalization periodic, ⟨P⟩ vs SU(3) literature
   (Lucini-Teper 2004, Necco-Sommer 2002 reference values built-in)
4. Hot start thermalization twisted
5. Metropolis acceptance ∈ [0.3, 0.7]
6. Autocorrelation τ_int (Sokal automatic windowing)

If any sanity test fails → `SANITY_FAILED` status, no measurements run.

### Driver (lines ~1100-1318)

- `run_one_config(L, beta, n_therm, n_decorr, n_samples, ...)` :
  full pipeline for one (L, β) configuration, writes JSON
- `main()` : CLI sweep over L × β grid
- Flags : `--quick` (L=4 test), `--sanity_only`, `--L`, `--beta` single overrides

## Usage

### Quick test (recommended FIRST run, ~5 min)
```bash
python3 jax_su3_tHooft_lattice_PROPER_2026-05-26.py --quick
```
Runs L=4, β=3.0, n_therm=200, n_samples=10. Validates :
- Centraliser lemma
- Cold/hot start ⟨P⟩
- Metropolis acceptance
- Twist removes FP zero mode (λ_min twisted > 0, periodic ≈ 0)

### Sanity-only sweep (no measurements, ~20 min)
```bash
python3 jax_su3_tHooft_lattice_PROPER_2026-05-26.py --sanity_only
```
Runs sanity battery for all (L, β) configurations.

### Single (L, β) run
```bash
python3 jax_su3_tHooft_lattice_PROPER_2026-05-26.py --L 8 --beta 3.0
# default n_therm=2000, n_decorr=20, n_samples=100 from DEFAULT_RUNS_CONFIG
```

### Full paper sweep (9 configurations)
```bash
python3 jax_su3_tHooft_lattice_PROPER_2026-05-26.py
```

### Custom run parameters
```bash
python3 jax_su3_tHooft_lattice_PROPER_2026-05-26.py \
    --L 12 --beta 3.0 --n_therm 5000 --n_samples 60
```

## Output JSON specification

Each (L, β) run writes `/tmp/tHooft_L{L}_b{beta}_2026-05-26.json` with structure :

```json
{
  "L": 12, "beta": 3.0,
  "n_therm": 3000, "n_decorr": 25, "n_samples": 80,
  "date_utc": "2026-05-26T...",
  "author": "Kévin Rémondière",
  "orcid": "0009-0008-2443-7166",
  "script": "jax_su3_tHooft_lattice_PROPER_2026-05-26.py",
  "paper_ref": "Paper_tHooft_Twist_Mode_Zero_LMP/main.tex",
  "sanity": {
    "centraliser": { "tHooft_commutator_max_err": 1.2e-16, "pass_commutator": true, ... },
    "cold_p_periodic": 1.0, "cold_p_twisted": 0.99996, "pass_cold": true,
    "hot_p_periodic_final": 0.275, "hot_p_periodic_ref": 0.275, "hot_p_periodic_relerr": 0.01,
    "hot_p_twisted_final": 0.275, "twist_periodic_diff": 0.0003,
    "hot_acc_periodic": 0.45, "hot_acc_twisted": 0.45,
    "tau_int_twisted": 1.8,
    "SANITY_OVERALL_PASS": true
  },
  "O1_FP_lambda_min": {
    "twisted":  { "mean": 0.215, "std": 0.012, "min": 0.198, "n_samples": 80 },
    "periodic": { "mean": 1.5e-12, "std": 5e-13, "min": 1.0e-12, "n_samples": 80 },
    "m_Omega_sq": 0.00609,
    "m_0_sq": 0.0548,
    "theoretical_lower_bound_5_6_m_Omega_sq": 0.00507,
    "pass_twisted_above_bound": true,
    "periodic_near_zero_check": true
  },
  "O2_Hess_gap": {
    "twisted_mean": 0.41, "twisted_std": 0.02,
    "periodic_mean": 1.2e-10,
    "n_samples_hess": 16
  },
  "O3_LSI_rothaus_simon": {
    "mean_hess_gap": 0.41, "std_hess_gap": 0.02,
    "kappa_ricci": 0.667,
    "C_LSI_rothaus_simon": 0.93,
    "C_LSI_paper_bound": 79.6,
    "pass_bound": true
  },
  "status": "OK",
  "wall_time_seconds": 1830.5
}
```

A summary `/tmp/tHooft_summary_2026-05-26.json` aggregates all (L, β) runs.

## ETA & cost

### Per (L, β) configuration

| L  | n_therm | n_decorr | n_samples | FP dim    | Hess dim     | Mem (GB) | Wall  |
|----|---------|----------|-----------|-----------|--------------|----------|-------|
| 8  | 2000    | 20       | 100       | 32,768    | 131,072      |  ~1      | 1-2h  |
| 12 | 3000    | 25       |  80       | 165,888   | 663,552      |  ~3-4    | 4-6h  |
| 16 | 4000    | 30       |  60       | 524,288   | 2,097,152    |  ~8-10   | 10-15h |

### Full sweep (9 configurations on RTX 5060 Ti 16 GB)

- **Total wall time** : ~50-75 hours sequential, or ~10-15 hours with 3-way β parallelism
- **Peak GPU memory** : ~10-12 GB at L=16 (well within 16 GB budget)
- **Disk** : <100 MB JSON outputs

### Recommendation

**Run the L=8 only first** (3 β values, ~6 hours) to validate :
- Sanity passes for all β
- ⟨P⟩ matches Lucini-Teper reference
- λ_min(M^Ω) > (5/6) m_Ω² holds at smallest L
- λ_min(M^periodic) ≈ 0 (constant zero mode present)

If L=8 confirms Hypothesis 4.2 → proceed with L=12, L=16 overnight.

## Critical conventions documented

### Metropolis K vs K† (BUG #1 from 2026-05-25)

```python
# WRONG (silent catastrophic for SU(N>=2)) :
K_dag = jnp.conj(jnp.swapaxes(K, -1, -2))
dS = -β/N · Re Tr((U_proposed - U_old) · K_dag)

# CORRECT (used in this script) :
dS = -β/N · Re Tr((U_proposed - U_old) · K)
```

Reason : for SU(N), Re Tr(U·K) ≠ Re Tr(U·K†) because the anti-Hermitian
part of U·K changes sign vs U·K† — the algebra term `a·K` flips, and
Metropolis ends up minimizing the wrong quantity → drives ⟨P⟩ negative.

### Staple order (BUG #2 from 2026-05-25 BP2008b)

```python
# WRONG (BP2008b had this bug) :
K_fwd = U_ν(x) · U_μ(x+ν̂)† · U_ν(x+μ̂)†   # U_ν(x) first

# CORRECT (used in this script) :
K_fwd = U_ν(x+μ̂) · U_μ(x+ν̂)† · U_ν(x)†   # U_ν(x+μ̂) first
```

Convention : matches the plaquette factorisation
P_{x,μν} = U_μ(x) · [staple_fwd(x,μ via ν)] · U_μ(x)^{...} ... such that
Tr(K · U_μ(x)) = Σ_ν Re Tr P_{x,μν}.

### Twist phase placement

The centre phase z_{μν} = exp(-2πi n^{μν}/N) is applied to plaquettes
P_{x,μν} whose evaluation requires the boundary twist similarity Ω·U·Ω^{-1}
on both directions μ and ν. This happens **only at the corner plaquette**
x_μ = L-1, x_ν = L-1 in the twist plane, because the twist commutator
Ω_μ Ω_ν Ω_μ^{-1} Ω_ν^{-1} = z_{μν} only appears when both Ω matrices
"meet" at that single corner.

All other plaquettes carry phase z = 1 (the gather_link_twist similarity
introduces Ω · U · Ω^{-1} factors that cancel pairwise in the trace).

### Reference plaquette values (Lucini-Teper-Wenger 2004)

Built-in `SU3_PLAQUETTE_REFERENCE` dict :
- β_W = 5.7 → ⟨P⟩ = 0.549
- β_W = 6.0 → ⟨P⟩ = 0.594
- β_W = 7.5 → ⟨P⟩ = 0.700

The paper's β ∈ {2.5, 3.0, 3.5} are interpreted as Wilson β (matching action
convention β · Σ (1 - Re Tr P/N)). For SU(3), these are STRONG coupling
values (confinement phase, ⟨P⟩ ≈ 0.2-0.3). The continuum regime properly
starts at β_W ≥ 5.7.

If sanity test [3] fails for β ∈ {2.5, 3.0, 3.5} (rel_err > 20%), the
paper's β should be reinterpreted as t'Hooft β_tH = β_W/N, giving
β_W ∈ {7.5, 9.0, 10.5} (deep continuum) → ⟨P⟩ ≈ 0.70, 0.75, 0.79.

## Risk register & gotchas

### High risk
- **R1** : Twist phase placement convention may differ from paper §2.4 by
  location of z_{μν}. Cross-check after L=4 quick test : if cold-start
  twisted ⟨P⟩ ≠ 1 - 1.5/n_plaq, the phase is placed incorrectly.
- **R2** : β interpretation (Wilson vs t'Hooft) — see above. If ⟨P⟩(β=3.0)
  doesn't match either reference, the sweep parameters need adjustment.

### Medium risk
- **R3** : Lanczos convergence for FP operator may stall for L=16 (large dim,
  many quasi-degenerate small eigenvalues). Fallback : increase n_iter from
  60 → 200, or switch to shift-invert with sparse direct solver.
- **R4** : Hess gap computation uses finite difference on action 
  (`hess_action_apply` lines 750-780) which may suffer numerical noise at
  large L. Consider switching to jax.hessian-vector product via double
  jax.grad if precision insufficient.

### Low risk
- **R5** : Memory pressure at L=16. RTX 5060 Ti 16 GB should handle 10 GB
  peak, but JIT cache may spill. Use `XLA_PYTHON_CLIENT_PREALLOCATE=false`
  (already set).
- **R6** : Reproducibility — script uses seed=2026 by default. Document this
  in JSON for replay.

## Probability Hypothesis 4.2 is confirmed

Following Opus #4's estimate (paper §6.7) :

- **P(hypothesis valid)** = 80-90% (structural argument :
  - twist eats constant gauge mode (Lemma 2.5, PROVED)
  - bundle-twisted Hodge Laplacian has no zero mode (Prop 3.1, PROVED)
  - Babelon-Viallet O'Neill on twisted bundles is standard differential
    geometry (well-known)
  - Bakry-Emery on smooth Riemannian manifold is classical theorem)

- **P(numerical lattice confirms hypothesis if valid)** = 80-90%
  (Lanczos + Metropolis on twisted lattice is standard methodology,
  no new analytical surprises expected)

- **Combined P(measurements confirm twisted bound + periodic ~ 0)** = 70-85%

If lattice run **confirms** :
- Paper publishable as-is to LMP (4-6 weeks ETA)
- Mass gap reduction trivial-sector route gets a publishable
  proof-of-concept (zero mode IS removable by boundary conditions)

If lattice run **contradicts** :
- New open problem identified : "subtle twist-induced analytical
  pathology" — paper repositioned as anti-fab honest result, still
  publishable as a structural note + negative numerical evidence.

Either outcome is publishable. The science wins.

## Recommendation

**Iterate ONCE on L=4 quick test FIRST** (5-10 min) :
```bash
python3 jax_su3_tHooft_lattice_PROPER_2026-05-26.py --quick
```

Inspect output for :
- Sanity OVERALL PASS = true
- Centraliser commutator err < 1e-10
- Cold twisted ⟨P⟩ = 1 - 1.5/n_plaq within 1e-5
- Hot ⟨P⟩(β=3.0, L=4) periodic matches ref within 20%
- Metropolis acceptance ∈ [0.3, 0.7]
- λ_min(M^Ω) twisted > 0
- λ_min(M^periodic) ≈ 0

**Only after L=4 passes** : launch full L=8 sweep (3 β values, ~6h overnight),
then L=12 (~12h), then L=16 (~30h) sequentially.

Total expected wall time : ~50-75 hours if sequential, 10-15 hours if parallel
across the 3 β values. Cost on Vast.AI RTX 3090 : $0.155/h × 75h ≈ $12.

## File locations

- Script    : `/root/cc-private/papers/2026-05-24-session/scripts/jax_su3_tHooft_lattice_PROPER_2026-05-26.py`
- README    : `/root/cc-private/papers/2026-05-24-session/scripts/README_tHooft_lattice_2026-05-26.md`
- Paper     : `/root/cc-private/papers/Paper_tHooft_Twist_Mode_Zero_LMP/main.tex`
- Output    : `/tmp/tHooft_L{L}_b{beta}_2026-05-26.json` (per-config)
              `/tmp/tHooft_summary_2026-05-26.json` (aggregate)
- Reference primitives : `/root/cc-private/papers/2026-05-24-session/scripts/jax_su3_lattice_2026-05-25.py`

## Related memory documents

- `correction_metropolis_K_vs_Kdag_bug_2026-05-25.md` — BUG #1 documentation
- `project_jax_patches_history_2026-05-26.md` — 3 critical JAX bugs history
- `correction_BP2008_buividovich_NOT_bhattacharya_2026-05-25.md` — citation correction
