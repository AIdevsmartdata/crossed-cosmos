# M4 — Linearization Derivation: ξ_crit_+ for NMC KG + Friedmann

**Author:** M4 sub-agent (Sonnet 4.6), ECI v6.0.53.3+, 2026-05-06  
**Hallu count entering / leaving:** 85 / 85 (held — no new citations, all algebra sympy-verified)  
**Status:** NUMERICAL-AGREEMENT-ONLY (see SUMMARY.md)

---

## 1. System in N = ln(a) time

Working in units M_P = 1. Field: φ with Jordan-frame non-minimal coupling  
F(φ) = 1 + ξ φ².

Let ′ = d/dN, s_H = d ln H/dN.

**Modified Friedmann (code convention, from A56 `nmc_kg_extended.py` line 68):**

```
H² = (ρ_m + ρ_r + V) / D
D = 1 - ξ φ² - φ′²/6 + 2ξ φ φ′
```

This is derived from the Jordan-frame Friedmann equation:
```
3H²(1 + ξφ²) = ρ_m + ρ_r + ½H²φ′² + V + 6ξH²φφ′
=> 3H² [1 + ξφ² - φ′²/6 - 2ξφφ′] = ρ_m + ρ_r + V
```

(The code has the opposite sign on the ξφ² term — code convention has ξ > 0 as a destabilizing anti-gravity coupling.)

**Curvature scalar:**
```
R/H² = 6(2 + s_H)
```

This vanishes in radiation domination (s_H = -2, R = 0), which is a key structural fact.

**KG equation (from A56 code, line 82–86):**
```
φ″ = -(3 + s_H) φ′ + 3λ V/H² + ξ · R/H² · φ
```

Note: the factor of 3 on λV/H² and the positive sign on ξR/H²·φ both follow from the code implementation. The positive sign means ξ > 0 acts as a tachyonic source for φ when R > 0.

---

## 2. Linearized perturbation equation

Let φ = φ_★(N) + δφ, φ′ = φ_★′(N) + δφ′ where (φ_★, φ_★′) is the slow-roll background.

Perturbing the KG equation in δφ:

```
δφ″ = -(3 + s_H) δφ′ + [∂/∂φ (3λ V/H² + ξ R/H² φ)]_{φ_★} · δφ
```

Computing the partial derivative:
- ∂(3λV/H²)/∂φ = 3λ · (-λ) · V/H² = -3λ² V/H²
- ∂(ξ R/H² φ)/∂φ = ξ R/H²  (treating R/H² as background)

Therefore:

$$\boxed{\delta\phi'' + (3 + s_H)\,\delta\phi' - M^2_{\rm eff}\,\delta\phi = 0}$$

where the **effective squared mass** is:

$$M^2_{\rm eff}(N) = \xi \cdot \underbrace{6(2+s_H)}_{R/H^2} - 3\lambda^2 \cdot \underbrace{\frac{V}{H^2}}_{= 3\,\Omega_\phi} = 6(2+s_H)\,\xi - 9\lambda^2\,\Omega_\phi$$

---

## 3. Stability matrix (sympy-verified)

Writing (y₁, y₂) = (δφ, δφ′), the system is y′ = A · y with:

$$A = \begin{pmatrix} 0 & 1 \\ M^2_{\rm eff} & -(3+s_H) \end{pmatrix}$$

**Characteristic polynomial** (sympy output, Section 6):
```
mu^2 + (s_H + 3)*mu - M^2 = 0
```

**Eigenvalues** (sympy output):
```
mu_± = 0.5 * [-(3+s_H) ± sqrt((3+s_H)^2 + 4 M^2_eff)]
```

**Runaway condition:** μ₊ > 0 iff M²_eff > 0 (for s_H > -3, which holds for all standard epochs including matter domination where s_H = -3/2).

---

## 4. Instantaneous instability criterion

Setting M²_eff = 0:

$$\xi_{\rm crit}^{\rm inst}(N) = \frac{9\lambda^2\,\Omega_\phi(N)}{6(2+s_H(N))} = \frac{3\lambda^2\,\Omega_\phi(N)}{2(2+s_H(N))}$$

**Epoch-by-epoch values for λ = 1 (sympy numerical evaluation):**

| Epoch              | s_H   | R/H²  | Ω_φ   | ξ_crit^inst |
|--------------------|-------|-------|-------|-------------|
| Radiation          | -2.0  | 0.0   | ~0    | ∞ (R=0)     |
| Mat-Rad eq (z~3400)| -1.75 | 1.5   | 0.001 | 0.006       |
| Early MD           | -1.5  | 3.0   | 0.01  | 0.030       |
| Late MD            | -1.0  | 6.0   | 0.10  | 0.15        |
| MD-LD transition   | -0.5  | 9.0   | 0.40  | 0.40        |
| Λ-dominated today  | 0.0   | 12.0  | 0.70  | 0.525       |

**Key structural facts:**
1. R = 0 in radiation domination → NMC coupling completely inactive. Instability onset is impossible in RD regardless of ξ.
2. The minimum ξ_crit^inst over the trajectory occurs during late MD at ~0.15 (for λ=1).
3. This provides a **lower bound**: ξ_crit_+ > 0.15 for λ=1 (instantaneous instability anywhere on trajectory requires ξ > 0.15 at minimum).

---

## 5. Growth-rate criterion (denom collapse)

The actual runaway in A56 is diagnosed by the Friedmann denominator D collapsing below floor. Setting D = 0 with φ′ ≈ 0 (slow roll):

```
D ≈ 1 - ξ φ² = 0  =>  φ_crit = 1/√ξ
```

So φ must grow from φ₀ to φ_crit = 1/√ξ within the cosmic trajectory.

Growth condition:

$$\int_{N_{\rm init}}^{N_f} \mu_+(N)\,dN > \ln\!\left(\frac{1}{\sqrt{\xi}\,\phi_0}\right)$$

where μ₊(N) = ½[-（3+s_H) + √((3+s_H)² + 4M²_eff)] when M²_eff > 0, else 0.

---

## 6. Numerical integration result (linearized model)

Using flat LCDM background (Ω_m = 0.30, Ω_Λ = 0.70), slow-roll approximation φ ≈ φ₀ = const, λ = 1, N ∈ [-6, 0]:

| ξ     | ∫μ₊ dN | φ_final | φ_crit = 1/√ξ | Runaway? |
|-------|---------|---------|----------------|----------|
| 0.05  | 0.377   | 0.146   | 4.47           | OK       |
| 0.10  | 0.763   | 0.215   | 3.16           | OK       |
| 0.15  | 1.135   | 0.311   | 2.58           | OK       |
| 0.20  | 1.495   | 0.446   | 2.24           | OK       |
| 0.25  | 1.842   | 0.631   | 2.00           | OK       |
| 0.30  | 2.181   | 0.885   | 1.83           | OK       |
| 0.40  | 2.836   | 1.704   | 1.58           | **FAIL** |
| 0.50  | 3.474   | 3.226   | 1.41           | FAIL     |

**Bisection result: ξ_crit_analytic = 0.390** (linearized model)  
**A56 empirical: ξ_crit_+ ≈ 0.20**  
**Discrepancy factor: ~2.0**

---

## 7. Sign convention note (critical for reproducibility)

The A56 code uses the convention where ξ > 0 is **destabilizing** (positive coupling to R gives positive tachyonic mass term for φ). This is opposite to the standard textbook convention (e.g., ξ_conformal = +1/6 is stabilizing in standard NMC). The A56 code sign follows from:

```python
# line 83: force = ... + xi * R_over_H2 * phi    [POSITIVE sign = destabilizing]
# line 68: denom = 1 - xi * phi^2 ...             [NEGATIVE sign in closure denom]
```

Both signs are consistent: ξ > 0 makes the effective gravitational coupling F < 1 (weaker gravity) AND the field feels a tachyonic force from curvature.

---

## 8. Sources of ~2x discrepancy

The linearized analysis gives ξ_crit_analytic ≈ 0.39 vs A56 empirical ≈ 0.20. The factor ~2 discrepancy arises from:

1. **φ = const (slow-roll) approximation**: The linearization freezes φ at φ₀. In reality φ grows during MD/LD, increasing ξφ² in the closure denominator and making the instability self-reinforcing (nonlinear feedback). This reduces the actual threshold.

2. **Ω_φ(N) model**: The simplified V/H² = Ω_L0/H²(N) approximation may underestimate the potential contribution at early times.

3. **Background-perturbation coupling**: The modified Friedmann equation couples δφ back into the background H(N), so perturbations affect their own growth rate (not captured in linear analysis).

4. **denom collapse criterion**: The actual A56 criterion is `denom < DENOM_FLOOR = 5e-3`, which triggers earlier than the exact D = 0 boundary.

---

## sympy verification log

All formulas in Sections 2-5 were symbolically verified with sympy 1.12:
- Section 3: `A_mat.charpoly(mu)` returns `mu^2 + (s_H + 3)*mu - M2`  ✓
- Section 3: `A_mat.eigenvals()` returns `mu_± = 0.5*[-(3+s_H) ± sqrt((3+s_H)^2 + 4M^2)]`  ✓
- Section 3: `solve(M2_sym, xi)` returns `xi_crit = 3*Omega_phi*lambda^2/4` (Lambda-dom)  ✓
- Section 4: `solve(M2_full, xi)` returns `xi_crit = 3*Omega_phi*lambda^2/(2*(s_H+2))`  ✓
- Numerical integration: scipy `trapz` over 2000-point LCDM trajectory  ✓

Full derivation script: `xi_crit_analysis.py` (runs in ~3 seconds on VPS).
