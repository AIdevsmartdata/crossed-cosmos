# A70 — Full likelihood + priors specification

## 1. Models under test

### Model ECI-Cassini (Framing A + B)
Jordan-frame action (Faraoni convention, A64 eq.):
  S = ∫d⁴x √(−g) [ −½(M_P² + ξ_χ χ²) R + ½(∂χ)² − V(χ) + L_matter ]
  V(χ) = V₀ exp(−λ χ/M_P)

Parameters: θ_ECI = {H₀, ω_b, ω_c, n_s, A_s, τ, ξ_χ, λ_χ, χ₀}

### Model Wolf-NMC-KG (Framing A — KG-restricted)
Jordan-frame action (A69/lagrangian.tex verbatim):
  S = ∫d⁴x √(−g) [ M_P²/2 · F(φ)R − ½X − V(φ) + L_matter ]
  F(φ) = 1 − ξ(φ²/M_P²)
  V(φ) = V₀ + β φ + ½ m² φ²
  (G=1, J=0 — no k-mouflage, no Galileon)

Parameters: θ_Wolf = {H₀, ω_b, ω_c, n_s, A_s, τ, ξ, β, m², φ_init, φ'_init}
  where V₀ is NOT free: tuned analytically to close Friedmann today.

### Model CPL-ECI-eff (Framing B — EFT fluid)
  w(z) = w₀_ECI + w_a_ECI (1 − a)
  w₀, w_a derived from ECI background ODE (cosmopower emulator)

### Model CPL-Wolf-eff (Framing B — EFT fluid)
  w(z) = w₀_W + w_a_W (1 − a)
  Directly parameterized.

---

## 2. Priors table

### 2A. ECI-Cassini priors (Framing A primary)

| Parameter     | Prior type     | Range / Mean ± σ       | Justification                                    |
|---------------|---------------|-------------------------|--------------------------------------------------|
| H₀ [km/s/Mpc]| Uniform        | [50, 90]                | Wide; spans Planck (67.4) and SH0ES (73.0)       |
| ω_b           | Gaussian       | 0.02218 ± 0.00055       | BBN prior (Cooke et al. 2018) [TBD: verify ref]  |
| ω_c           | Uniform        | [0.08, 0.20]            | Wide, data-driven                                |
| n_s           | Uniform        | [0.90, 1.05]            | Standard CMB range                               |
| ln(10¹⁰ A_s) | Uniform        | [2.7, 3.5]              | Standard CMB range                               |
| τ_reio        | Gaussian       | 0.054 ± 0.007           | Planck 2018 low-ℓ polarization                   |
| ξ_χ           | Uniform (hard) | [−0.024, +0.024]        | Cassini gate: \|ξ_χ\|(χ₀/M_P)² ≲ 6×10⁻⁶ at χ₀/M_P≈0.016 |
| λ_χ           | Uniform        | [0.5, 4.0]              | ECI exponential slope (A25 range)                |
| χ₀/M_P        | Uniform        | [5×10⁻³, 5×10⁻²]       | Initial field value; consistent with Cassini      |

**Note on ξ_χ:** RG running (A73) shows ξ_χ(M_GUT) = −0.029, so the prior
range [−0.024, +0.024] is consistent with the full UV trajectory.

### 2B. Wolf-NMC-KG priors (Framing A — KG-restricted)

| Parameter     | Prior type     | Range                   | Justification                                    |
|---------------|---------------|-------------------------|--------------------------------------------------|
| H₀ [km/s/Mpc]| Uniform        | [50, 90]                | Same as ECI                                      |
| ω_b           | Gaussian       | 0.02218 ± 0.00055       | Same BBN prior                                   |
| ω_c           | Uniform        | [0.08, 0.20]            | Same                                             |
| n_s           | Uniform        | [0.90, 1.05]            | Same                                             |
| ln(10¹⁰ A_s) | Uniform        | [2.7, 3.5]              | Same                                             |
| τ_reio        | Gaussian       | 0.054 ± 0.007           | Same                                             |
| ξ (Wolf NMC)  | Uniform        | [−5.0, +0.20]           | KG-physical wedge from A56 empirical ξ_crit_+≈0.20 |
| β [M_H² M_P]  | Uniform        | [−10, +10]              | Linear V term; Wolf quadratic potential          |
| m² [M_H²]     | Uniform        | [−10, +10]              | Concave V (m²<0) favoured by Wolf; allow both    |
| φ_init/M_P    | Uniform        | [10⁻³, 5×10⁻²]         | Initial field displacement                       |
| φ'_init/M_P   | Uniform        | [−0.1, +0.1]            | Initial field velocity (H-units)                 |

**KG gate (hard):** Per-sample integrate KG + Friedmann ODE from N=−8 to 0.
Set logL = −∞ if any of:
  (a) φ > 10 M_P (runaway)
  (b) F(φ) = 1 − ξ(φ/M_P)² < 0.01 (ghost / F-collapse)
  (c) a_today < 0.95 or > 1.05 (Friedmann closure failure)

**Caveat:** A56's ξ_crit_+ ≈ 0.20 was derived for exponential V. Wolf's
quadratic V may have slightly different ξ_crit. The numerical gate is
potential-agnostic; do NOT hardcode 0.20 as a prior boundary.

### 2C. CPL-effective priors (Framing B — both sides)

| Parameter     | Prior type | Range         | Used by      |
|---------------|-----------|---------------|--------------|
| H₀ [km/s/Mpc]| Uniform    | [50, 90]      | Both         |
| ω_b           | Gaussian   | 0.02218 ± 0.00055 | Both     |
| ω_c           | Uniform    | [0.08, 0.20]  | Both         |
| n_s           | Uniform    | [0.90, 1.05]  | Both         |
| ln(10¹⁰ A_s) | Uniform    | [2.7, 3.5]    | Both         |
| τ_reio        | Gaussian   | 0.054 ± 0.007 | Both         |
| w₀            | Uniform    | [−2.0, +0.0]  | Both         |
| w_a           | Uniform    | [−3.0, +3.0]  | Both         |
| M_B [mag]     | Uniform    | [−20.0, −18.5]| Both (SNe)   |

---

## 3. Likelihood components

### 3.1 CMB — Planck 2018 Plik TT+TE+EE
Likelihood: official Planck 2018 Plik coadded (NOT PR4 — A69 correction).
Implementation: `clik` library from Planck Legacy Archive.
  log L_CMB = −½ (C_ℓ − C_ℓ^th)^T Σ⁻¹ (C_ℓ − C_ℓ^th)

### 3.2 BAO — DESI DR2 (arXiv:2503.14738)
7 z-bins {0.30, 0.51, 0.71, 0.93, 1.32, 1.49, 2.33}.
Observables: D_M(z)/r_d, D_H(z)/r_d (or D_V for BGS).

### 3.3 SNe Ia — Pantheon+
Reference: Brout et al. 2022 [TBD: verify arXiv ID].
1701 SN-Ia. Marginalize M_B analytically.
Note: Wolf used DES-Y5 rotated; we use Pantheon+ for reproducibility.

### 3.4 CMB lensing — ACT DR6
Reference: Madhavacheril et al. 2024 [TBD: verify arXiv ID].
Compressed: A_lens amplitude + shape.

### 3.5 Combined log-likelihood
  log L_tot = log L_CMB + log L_BAO + log L_SNe + log L_lens + KG_gate(θ)
KG gate active only in Framing A.

---

## 4. Background ODE pipeline

### For ECI-Cassini side
- **A25 emulator**: cosmopower-jax custom_log (pkl) for log₁₀H(z) and w(z)
  on ξ_χ ∈ [−0.10, +0.10] grid.
- **NEW (2026-05-05 night)**: A56-extended emulator at
  `/home/remondiere/pc_calcs/cosmopower_nmc_emulator_extended/` covers
  ξ ∈ [−5.0, +0.198] (KG-physical wedge); H val MSE = 1.5e-3.
- ECI prior |ξ_χ| < 0.024 → A25 emulator sufficient. Extended emulator
  useful for Wolf-KG side.

### For Wolf-NMC-KG side (Framing A)
- **Required:** hi_class scalar-tensor Boltzmann solver, OR standalone
  Friedmann+KG ODE in JAX + new emulator on Wolf-quadratic-V grid.
- For PolyChord: direct ODE per sample (slower, exact).
- For NUTS: train new emulator [TBD: scope as A71 subtask].

### KG ODE system (Wolf quadratic V, Jordan frame, M_P=1, ' = d/dN)
  H² = (1/3) [ρ_m + ρ_r + ½H²φ'² + V(φ)] / F(φ),  F(φ) = 1 − ξφ²
  φ'' = −(3 + H'/H) φ' − V'(φ)/H² + ξ φ R/H²,  R/H² = 6(2 + H'/H)
  H'/H = symbolic GBD form

KG-gate: φ > 10 OR F(φ) < 0.01 → logL = −∞.

### Boltzmann code for perturbations
- **hi_class** (https://github.com/miguelzuma/hi_class_public)
  [TBD: confirm version + parameter names for Wolf quadratic V]

---

## 5. Evidence calculation

### Primary (PolyChord 1.20 — matches Wolf method)
- nlive = 500, num_repeats = 30 (11-dim space)
- log B = log Z_model − log Z_ΛCDM

### Cross-check (Thermodynamic Integration via NUTS)
- 16 temperature steps, β ∈ [10⁻⁴, 1.0] geometric
- 2000 NUTS samples per temperature per chain
- log Z ≈ ∫₀¹ ⟨log L⟩_β dβ
- Consistency: |log Z_TI − log Z_PolyChord| < 0.5 → OK

### Savage-Dickey density ratio (supplementary, Framing B)
- B(model vs ΛCDM) = π(test_pt) / p(test_pt | data)
- KDE Silverman bandwidth on marginal samples of ξ
- Pass π(0) explicitly; never infer from samples.

---

## 6. Sanity validation before publishing

**MANDATORY GATE — do not report H_A0/H_A1 until:**
1. Wolf-NMC-KG posterior peaks at ξ < 0.20 (H_sanity)
2. ECI-Cassini posterior reproduces A25 baseline H₀ = 70.20 ± 5.74 within 1σ
3. ΛCDM baseline log B = 0.0 (verify ±0.05)
4. PolyChord ↔ TI cross-check within ±0.5 log-units
5. Gelman-Rubin R̂ < 1.01 for all params (NUTS chains)

If any gate fails: STOP, debug, do not publish.
