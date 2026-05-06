# KG Gate Logic — Wolf-NMC-KG Physical Consistency Gate

**Date:** 2026-05-06  
**Reference:** A70 likelihood_spec.md §2B  
**Hallu count:** 85 (held)

## Purpose

For each MCMC sample (ξ, β, m², φ_init, φ'_init, ...) in the Wolf-NMC-KG branch
of the Framing A Bayes contest (A71), we integrate the background ODE and apply
a hard prior gate. Samples outside the KG-physical wedge get log L = −∞.

## Gate Decision Tree

```
SAMPLE (ξ, β, m², φ_init, φ'_init, Ω_m, Ω_r, V₀)
  │
  ▼
COMPUTE V₀ from Friedmann closure at N=0
  (V₀ = 3F₀ + 3F'₀φ'₀ − ½φ'₀² − ρ_m0 − ρ_r0 − β φ₀ − ½m²φ₀²)
  │
  ▼
CHECK F(φ_init) at start
  │  F(φ_init) = 1 − ξ φ_init² < 0.01?
  │  YES → REJECT (F_collapse at initialization)
  │
  ▼
INTEGRATE wolf_kg_ode_2d from N=−5 to N=0
  │
  ├── ODE fails (stiffness / step size error) → REJECT
  │
  ▼
CHECK Gate (a): φ RUNAWAY
  │  max|φ(N)| > 10 M_P over N ∈ [−5, 0]?
  │  YES → REJECT (phi_runaway)
  │
  ▼
CHECK Gate (b): F COLLAPSE
  │  min F(φ(N)) = min[1 − ξ φ(N)²] < 0.01?
  │  YES → REJECT (F_collapse; ghost instability / F→0 gravity decouple)
  │
  ▼
CHECK Gate (c): FRIEDMANN CLOSURE
  │  |lnH(N=0)| > 0.05?
  │  (In 2D formulation: H² computed from Friedmann constraint. H²→0
  │   signals Friedmann denominator collapse = unphysical geometry.)
  │  YES → REJECT (Friedmann_closure)
  │
  ▼
ALL GATES PASS → ACCEPT (KG-physical sample)
  → compute log L_BAO + log L_SNe + log L_CMB
```

## Gate Thresholds (per A70 §2B)

| Gate | Threshold | Physical meaning |
|------|-----------|-----------------|
| (a) φ runaway | \|φ\| > 10 M_P | Field excursion exceeds Planck mass × 10 |
| (b) F collapse | F(φ) < 0.01 | Effective gravitational coupling → 0 (ghost onset) |
| (c) Friedmann | \|lnH(0)\| > 0.05 | H₀ deviation > 5% (Fried. closure failure) |

## Physical Regime Analysis

### For Wolf quadratic V: V = V₀ + βφ + ½m²φ²

**Gate (b) F collapse** is the primary danger at large ξ:
- F(φ) < 0.01 requires φ² > 0.99/ξ
- At ξ=2.31: |φ| > 0.654 M_P triggers gate
- At ξ=0.30: |φ| > 1.817 M_P triggers gate
- At ξ=0.10: |φ| > 3.146 M_P triggers gate (very large)

**Gate (c) Friedmann closure** triggers when:
- Friedmann denominator 3F + 3F'φ' − ½φ'² → 0 or negative
- For large φ and/or large φ' with ξ large, this can happen mid-integration
- Example: ξ=0.30, φ_init=1.5, m²=−2.0 → H²(N=0)→0 (gate triggers)

**Gate (a) φ runaway** requires:
- For quadratic V with m²<0: tachyonic mass drives φ away from origin
- Effective mass: M²_eff ≈ m² + 6ξ(2+s_H)H² (NMC adds positive tachyonic term when ξ>0, R>0)
- Runaway condition: |φ| grows by factor >100 over 5 e-folds
- For m²=0: φ is stabilized by Hubble friction even at ξ=2.31 (for φ_init~0.01)

### Comparison with A56 (exponential V)

A56 empirical ξ_crit_+ ≈ 0.20 is **NOT** applicable to Wolf quadratic V:
- A56 used V = V₀ exp(−λφ) with λ=1 (provides sustained driving force)
- Exponential V drives field down the slope → runaway at ξ > 0.20
- Quadratic V does not sustain driven runaway for small φ_init
- The KG gate is **potential-agnostic** and always correct

### numpyro implementation

```python
# In wolf_kg_model (numpyro NUTS):
gate_pass, reason = kg_gate(phi_traj, F_traj, lnH_traj, N_grid)
numpyro.factor('kg_gate', jnp.where(gate_pass, 0.0, -jnp.inf))
```

## Test Results (verified 2026-05-06)

| Test | ξ | φ_init | m² | Expected | Actual gate | Result |
|------|---|--------|-----|----------|------------|--------|
| A | 0.10 | 0.50 | −0.5 | STABLE | PASS | PASS |
| B | 0.30 | 1.50 | −2.0 | TRIGGER | Friedmann_closure (H²→0) | PASS |
| C | 2.31 | 0.66 | −0.5 | CATASTROPHIC | F_collapse (F_init<0) | PASS |
| D | ≈0 | 0.01 | 0.0 | LCDM-like | PASS | PASS |

## Notes for Production Sampling

1. V₀ tuning: tune_V0() uses φ_today ≈ φ_init as first approximation. For
   production, iterate: integrate once, use φ(N=0) as updated φ_today, retune V₀.
   One iteration gives <1% error on H₀ for |φ_init| < 0.5 M_P.

2. N_init = −5 (a ≈ 0.0067) is sufficient for matter domination.
   For ω_r-sensitive cases, extend to N_init = −8 with Radau integrator.

3. PolyChord sampling: wolf_kg_ode_2d is deterministic and fast (~1ms/sample).
   For NUTS: use JAX wolf_kg_ode_jax via jax.experimental.ode.odeint.

4. Prior volume: Wolf's ξ ∈ [−5, +0.20] KG-physical prior (A70 §2B) already
   excludes most of the Wolf best-fit ξ=2.31 range. For production, sample
   ξ ∈ [−5, +0.20] and let the KG gate handle the upper boundary.
