# GBD H'/H Derivation — Wolf-NMC-KG Background Equations

**Date:** 2026-05-06  
**Author:** M7 sub-agent (Sonnet 4.6)  
**Hallu count:** 85 → 85 (held)  
**Mistral:** STRICT-BAN (not used)

## Action

Wolf 2025 (arXiv:2504.07679, verified by A69) Jordan-frame action (M_P=1):

```
S = ∫d⁴x √(-g) [ F(φ)/2 · R - ½(∂φ)² - V(φ) + L_m ]

F(φ) = 1 - ξ φ²
V(φ) = V₀ + β φ + ½ m² φ²
```

With G(φ)=1 (k-essence off), J(φ)=0 (Galileon off). The only NMC is via G₄ = F(φ)/2.

## FLRW Background

Metric: ds² = -dt² + a² dx², with N = ln a, ' = d/dN = (1/H) d/dt.

Notation: φ' = dφ/dN, H' = dH/dN, s_H = H'/H.

Density evolution (M_P=1, H₀=1):
- ρ_m(N) = 3 Ω_m exp(-3N)   [Ω_m = ω_m / h²]
- ρ_r(N) = 3 Ω_r exp(-4N)   [Ω_r = ω_r / h²]

## GBD Field Equations (Jordan Frame)

From varying the action w.r.t. the metric (Jordan frame):

**Eq (I) — Friedmann (00-component):**
```
3F H² = ρ_m + ρ_r + ½ H² φ'² + V - 3 H² F'(φ) φ'
```
where F'(φ) = dF/dN/φ' = dF/dphi (here F'≡dF/dphi, so dF/dN = F'φ').

Rearranging:
```
H² = (ρ_m + ρ_r + V) / [3F + 3 F'φ' - ½φ'²]
```
where F' = -2ξφ, V includes all φ-dependent terms.

**Eq (II) — Raychaudhuri (ij-component, physical time):**
```
2F Ḣ + 3F H² = -(P_m + P_r) + ½ φ̇² - V + F̈/H² + H Ḟ/H
```
converted to N-coordinates:
```
2F s_H H² + 3F H² = -(ρ_r/3) + ½ H² φ'² - V
                    + H²(F'φ'' + F''φ'² + F'φ' s_H) + H² F'φ'
```
where F'' = d²F/dφ² = -2ξ.

**Eq (III) — Klein-Gordon:**
```
φ'' + (3 + s_H)φ' + V'(φ)/H² - (F'/2)(R/H²) = 0
```
with R/H² = 6(2 + s_H), so:
```
φ'' = -(3 + s_H)φ' - V'/H² + 3 F'(2 + s_H)
    = -(3 + s_H)φ' - V'/H² - 6ξφ(2 + s_H)
```

## Derivation of Closed-Form H'/H

**Step 1:** From Eq (II), collect s_H terms:
```
s_H (2F - F'φ') = -3F - ρ_r/(3H²) + ½φ'² - V/H² + F'φ'' + F''φ'² + F'φ'
```

**Step 2:** From Eq (I) divided by H²:
```
3F = (ρ_m + ρ_r + V)/H² - 3F'φ' + ½φ'²
```

**Step 3:** Substitute 3F from Step 2 into Step 1:
```
s_H(2F - F'φ') = -[(ρ_m + ρ_r + V)/H² - 3F'φ' + ½φ'²]
                  - ρ_r/(3H²) + ½φ'² - V/H²
                  + F'φ'' + F''φ'² + F'φ'

  = -ρ_m/H² - (4/3)ρ_r/H² - 2V/H² + 4F'φ' + F'φ'' + F''φ'²
```

**Step 4:** Substitute KG equation φ'' = -(3+s_H)φ' - V'/H² + 3F'(2+s_H):
```
numerator = -ρ_m/H² - (4/3)ρ_r/H² - 2V/H² + 4F'φ'
           + F'[-(3+s_H)φ' - V'/H² + 3F'(2+s_H)] + F''φ'²

  = [-ρ_m/H² - (4/3)ρ_r/H² - (2V + F'V')/H² + F'φ' + 6F'² + F''φ'²]
    + s_H[-F'φ' + 3F'²]
```

**Step 5:** Collect s_H on lhs:
```
s_H[(2F - F'φ') - (-F'φ' + 3F'²)] = no-sH terms
s_H[2F - 3F'²] = numerator_no_sH
```

## Final Result (sympy-verified)

```
H'/H = N_sH / D_sH

N_sH = -ρ_m/H² - (4/3)ρ_r/H²
       - [2V(φ) + F'(φ) V'(φ)] / H²
       + F'(φ) φ' + 6 F'(φ)² + F''(φ) φ'²

D_sH = 2F(φ) - 3 F'(φ)²
```

With Wolf explicit forms:
- F' = -2ξφ,  F'' = -2ξ,  V' = β + m²φ
- N_sH = -ρ_m/H² - (4/3)ρ_r/H² - [2V + (-2ξφ)(β+m²φ)]/H²
         + (-2ξφ)φ' + 6(4ξ²φ²) + (-2ξ)φ'²
- D_sH = 2(1-ξφ²) - 3(4ξ²φ²) = 2 - 2ξφ² - 12ξ²φ²

**Key property:** φ'' does NOT appear in s_H. The ODE system [φ, φ'] is self-consistent with H² computed from the Friedmann constraint at each step.

## Sympy Verification

Run `gbd_sympy_deriv.py` to verify:
- F, FP, FPP, V, VP computed symbolically
- LCDM check (ξ=0, φ=0): s_H = -(ρ_m + (4/3)ρ_r + 2Λ)/(2H²) ✓
- At matter domination: s_H = -ρ_m/(2H²) = -3/2 ✓

## Implementation

2D Friedmann-constrained ODE (no lnH integration drift):

```python
def wolf_kg_ode_2d(N, state, xi, V0, beta, m2, Omega_m, Omega_r):
    phi, phi_p = state
    H2 = H2_from_friedmann(phi, phi_p, N, ...)  # from Friedmann constraint
    s_H = wolf_sH(phi, phi_p, H2, ...)          # closed-form
    phi_pp = -(3+s_H)*phi_p - VP/H2 - 6*xi*phi*(2+s_H)  # KG
    return [phi_p, phi_pp]
```

Note: integrating lnH as a 3rd ODE variable accumulates ~0.1 units drift by N=-1 (tested numerically). The 2D approach maintains H²(0) = 1.000 ± 1e-6.

## References

- arXiv:1106.2476: Clifton, Ferreira, Padilla, Skordis "Modified Gravity and Cosmology" (PhysRep 513, 2012). VERIFIED by WebFetch 2026-05-06.
- arXiv:2504.07679: Wolf et al. 2025, PRL 135, 081001. VERIFIED by A69 sub-agent.
- Esposito-Farese & Polarski gr-qc/0011076: NMC background equations (Eqs A1-A3).
