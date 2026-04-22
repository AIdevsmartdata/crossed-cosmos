# V8-Cassini-frozen-field — Report
**Date:** 2026-04-22  
**Script:** `derivations/V8-chi-z-Cassini.py`  
**Plot:** `derivations/V8-chi-z-Cassini.png`  
**Pre-registration:** `paper/_internal_rag/REGISTRY_FALSIFIERS.md § V8-Cassini-frozen-field`

---

## 1. Question

Does the frozen-field approximation χ(z) ≈ χ₀ = M_P/10 used in v5's Cassini
PPN bound hold to within 5% from z = 0.1 to z = 0 at the v5 MAP cosmology?

---

## 2. Method

**Klein-Gordon slow-roll on FLRW.**  
Potential: V_χ = V_0 exp(−α χ/M_P), so V_{χ,χ} = −(α/M_P) V_χ.  
Slow-roll KG: dχ/dN ≈ −V_{χ,χ}/(3H²) = (α/M_P) V_χ/(3H²).  
Converting to redshift coordinate (dN = −dz/(1+z)):

    dχ/dz = −(α/M_P) V_χ(χ) / [3 H²(z) (1+z)]

**H²(z) = H_0² [Ω_m(1+z)³ + Ω_Λ f_DE(z)]**  
with CPL dark energy:

    f_DE(z) = exp{3[(1+w_0+w_a) ln(1+z) + w_a(1/(1+z) − 1)]}

**V_0 normalisation:** V_0 = 3 H_0² Ω_Λ exp(α χ_0/M_P), so that V_χ(z=0) = 3H_0²Ω_Λ.

**Initial condition:** χ(z=0) = χ_0 = 0.1 M_P (frozen field assumption as baseline).

**ODE solver:** `scipy.integrate.solve_ivp` RK45, rtol=1e-10, atol=1e-12.

**MAP cosmology parameters:**
| Parameter | Value |
|-----------|-------|
| w_0       | −0.881 |
| w_a       | −0.272 |
| α         | 0.095 |
| Ω_m       | 0.3153 |
| Ω_Λ       | 0.6847 |
| χ_0       | 0.1 M_P |

---

## 3. Results

### 3.1 χ(z) trajectory at MAP α = 0.095

| z    | χ (M_P)    | ε_SR        |
|------|-----------|-------------|
| 0.00 | 0.10000000 | 2.116 × 10⁻³ |
| 0.05 | 0.09691751 | 1.880 × 10⁻³ |
| 0.10 | 0.09414639 | 1.672 × 10⁻³ |
| 0.15 | 0.09164938 | 1.487 × 10⁻³ |
| 0.20 | 0.08939497 | 1.322 × 10⁻³ |
| 0.25 | 0.08735615 | 1.175 × 10⁻³ |
| 0.30 | 0.08550959 | 1.044 × 10⁻³ |

Slow-roll parameter ε_SR ≪ 1 throughout: slow-roll approximation is self-consistent.

### 3.2 Key numbers

| Quantity | Value |
|----------|-------|
| χ(z=0)   | 0.10000000 M_P |
| χ(z=0.1) | 0.09414639 M_P |
| Δχ = χ(0.1)−χ(0) | −5.854 × 10⁻³ M_P |
| **\|Δχ\|/χ₀** | **5.854%** |

### 3.3 Sensitivity scan α ∈ (0, 0.1]

| α (endpoint) | |Δχ|/χ₀ |
|---|---|
| 0.005 | 0.038% |
| 0.050 | 1.59% |
| 0.095 (MAP) | 5.854% |
| 0.100 (max) | 6.162% |

The maximum across the full M3 α range is **6.162%** at α = 0.100.

---

## 4. Slow-roll validity

ε_SR ≈ 2 × 10⁻³ at z = 0 and ≈ 1.7 × 10⁻³ at z = 0.1. Both are well below
unity. The condition |η_SR| ≪ 1 (second slow-roll parameter) is implied by
the exponential potential's flat tilt at χ ∼ 0.1 M_P, α = 0.095. Slow-roll
is self-consistent; no correction to the approximation is required in this
redshift window.

---

## 5. Verdict

**Pre-registered threshold (REGISTRY_FALSIFIERS.md):**
- PASS: |Δχ|/χ₀ < 5%
- BORDERLINE: 5% ≤ |Δχ|/χ₀ < 15%
- FAIL: |Δχ|/χ₀ ≥ 15%

**VERDICT: BORDERLINE**

At the MAP α = 0.095: |Δχ|/χ₀ = **5.85%** (just above the 5% PASS threshold).  
Across the full M3 α range (0, 0.1]: max = **6.16%** at α = 0.100.

The frozen-field approximation misses the field by ~5.9% over the interval
z ∈ [0, 0.1]. Since |γ−1| = 4 ξ_χ² χ²/M_P², the Cassini bound has a
corresponding theory uncertainty:

    δ|γ−1| / |γ−1| ≈ 2 |Δχ|/χ₀ ≈ 11.7%

This is sub-dominant compared to the observational Cassini precision
(|γ−1| ≤ 2.3 × 10⁻⁵ at ~0.001% precision) but is a non-negligible
systematic in the analytic PPN bound derivation.

---

## 6. Required v5 caveat

Add the following sentence to §3.5 or the caption of the PPN bound (D7):

> "The Cassini bound is evaluated at the frozen-field value χ₀ = M_P/10.
> A slow-roll integration of the thawing Klein-Gordon equation over
> z ∈ [0, 0.1] shows Δχ/χ₀ ≈ 5.9% at the MAP potential slope
> α = 0.095, implying a ~12% theory uncertainty on |γ−1| from field
> evolution. This is within the BORDERLINE regime (pre-registered
> V8-Cassini-frozen-field); the bound remains conservative and honest
> but carries this caveat."

No revision of the numerical bound is required; a one-sentence caveat suffices.

---

## 7. Artefacts

| File | Description |
|------|-------------|
| `derivations/V8-chi-z-Cassini.py` | ODE integration, sensitivity scan |
| `derivations/V8-chi-z-Cassini.png` | χ(z) trajectory + |Δχ|/χ₀ vs α |
| `derivations/V8-chi-z-Cassini-report.md` | This report |

*PRINCIPLES rule 1: all numbers above are outputs of V8-chi-z-Cassini.py
(reproducible). No claim exceeds what the slow-roll ODE supports.*
