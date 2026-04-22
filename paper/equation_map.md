# Equation map — ECI v4.4

For every displayed equation in the paper, the supporting derivation script
under `derivations/`. Walked `paper/eci.tex`, `paper/section_3_5_constraints.tex`,
`paper/section_3_6_swampland_cross.tex`.

Status legend:
- `PASS` — equation statement symbolically / numerically matched by a committed,
  runnable script.
- `PARTIAL` — script covers the equation's ingredients but not the displayed form
  verbatim (e.g. closed-form coefficient derived, numerical verification missing).
- `NO SCRIPT` — no derivation committed; minimal script suggested in the Notes column.

| tex file | label / eq# | line | statement | script | status |
|---|---|---|---|---|---|
| eci.tex | (A1) S_gen | 40 | S_gen = A/(4 G_N) + S_matter (type-II crossed-product entropy) | — | NO SCRIPT — definitional; no derivation script needed, but a stub `D13-crossed-product-entropy.py` reproducing CLPW2023 Eq. for S_gen in the II_1 algebra would close the axiom. |
| eci.tex | eq:speciesH | 64 | Λ_sp(H) = M_P (H/M_P)^{c'} | derivations/D8-swampland-nmc-cross.py | PASS (used as input; algebraic identity from Montero2022 Eq. 2.2 reproduced in D8 header comments lines 7–14) |
| eci.tex | eq:A6-euler | 74 | ⟨χ_E(ν)⟩_{fNL} − ⟨χ_E(ν)⟩_0 ≃ (fNL σ0 S3/6) H_3(ν) φ(ν) (Matsubara genus shift) | derivations/D5-persistent-homology.py | PARTIAL (D5 is a pedagogical stub per plan v4.4 item; Matsubara H_3 shift is not coded as a symbolic assert). Suggested: extend D5 with sympy verification of the Hermite-polynomial coefficient against Matsubara 2003 Eq. (analogue). |
| eci.tex | (action) | 86 | S = ∫ d⁴x √(−g) [ M_P²/2 · R − ½(∂φ)² − V_φ − ½(∂χ)² − V_χ − ½ ξ_χ R χ² + L_SM + L_KK ] + S_QRF | derivations/D1-kg-nmc.py, D2-stress-nmc.py | PASS (action ingredient verified; sign convention Faraoni; reduced M_P) |
| eci.tex | (KG φ) | 93 | □φ − V_φ'(φ) = 0 | derivations/D1-kg-nmc.py | PASS (ξ→0 limit of the NMC KG equation; trivially reproduced) |
| eci.tex | (KG χ NMC) | 95 | □χ − V_χ'(χ) − ξ_χ R χ = 0 | derivations/D1-kg-nmc.py | PASS (symbolic Euler–Lagrange reproduction, matches Faraoni Eq. 2.9) |
| eci.tex | (Einstein) | 99 | G_μν = (1/M_P²)[T_μν^SM + T_μν^(φ) + T_μν^(χ) + T_μν^KK] | derivations/D2-stress-nmc.py | PARTIAL (sum-over-sources form is axiomatic; D2 verifies the NMC piece of the r.h.s.; no explicit script for the full Einstein equation — standard GR textbook result. No action needed.) |
| eci.tex | (NMC stress tensor) | 104 | T_μν^(χ) = ∇μχ∇νχ − ½ gμν[(∇χ)² + 2V_χ] + ξ_χ[gμν □(χ²) − ∇μ∇ν(χ²) − G_μν χ²] | derivations/D2-stress-nmc.py | PASS (Faraoni 2.12–2.13 form; trace + effective M_P² shift reproduced) |
| eci.tex | (no-ghost, inline) | ~109 | ξ_χ χ² / M_P² < 1 | derivations/D3-noghost.py | PASS (symbolic det-K computation, numerical table for ξ=0.1) |
| section_3_5 | eq:gamma_PPN_full | 22 | γ−1 = −F'(χ0)² / [Z F(χ0) + (3/2) F'(χ0)²] = −4 ξ_χ² χ0² / [M_P² + ξ_χ χ0²(6 ξ_χ − 1)] | derivations/D7-ppn-xi-bound.py | PASS (full DEF1993 / Hwang–Noh form and the expanded rational expression reproduced) |
| section_3_5 | eq:gamma_PPN_lead | 29 | γ−1 ≃ −4 ξ_χ² χ0² / M_P² + O(ξ_χ³) | derivations/D7-ppn-xi-bound.py | PASS (Taylor expansion in ξ_χ; ξ→0 limit asserted to give GR) |
| section_3_5 | eq:xi_bound | 45 | |ξ_χ|·(χ0/M_P) ≲ ½ √|γ−1|_max ≈ 2.4×10⁻³ | derivations/D7-ppn-xi-bound.py | PASS (Cassini |γ−1| ≤ 2.3e-5 input → numerical bound) |
| section_3_5 | eq:xi_max_numeric | 53 | \|ξ_χ\| ≲ ξ_max ≈ 2.4×10⁻² at χ0 = M_P/10 | derivations/D7-ppn-xi-bound.py | PASS |
| section_3_5 | eq:wa_NMC | 70 | w_a = −A(Ω_Λ)(1+w_0) + B(Ω_Λ) ξ_χ √(1+w_0) (χ0/M_P) + O(ξ²), with B(0.7) ≃ 7.30 | derivations/D4-wa-w0-nmc.py, derivations/D9-wa-numerical.py | PASS (D4 symbolic B coefficient; D9 numerical CPL fit cross-check against analytic B at several ξ, χ0) |
| section_3_5 | (ECI band half-width) | 98 | Δw_a^ECI = B(0.7) ξ_max √(1+w_0) (χ0/M_P) ≈ 8.8×10⁻³ | derivations/D9-wa-numerical.py | PASS (band width computed at lines ~372–380) |
| section_3_6 | eq:Lambda_SDC | 24 | Λ(H) ~ M_P (H/M_P)^{c'}, c' = 1/6 at species scale | derivations/D8-swampland-nmc-cross.py | PASS (numerical evaluation at H_0 reproduces Λ(H_0) ≃ 2.2×10⁸ GeV) |
| section_3_6 | eq:eft_bulk | 50 | ξ_χ χ0² ≲ Λ² ⇔ \|ξ_χ\|(χ0/M_P)² ≲ (H_0/M_P)^{2c'} | derivations/D8-swampland-nmc-cross.py | PASS (heuristic EFT bound encoded symbolically; marked as heuristic in the paper and in the script header) |
| section_3_6 | eq:xi_crossbound | 65 | \|ξ_χ\| ≲ 8.4×10⁻¹⁹ (c'=1/6, χ0 = M_P/10) | derivations/D8-swampland-nmc-cross.py | PASS (V1-D8-verification.md §4 independent check to 0.1%) |

## Summary

- Displayed equations (labelled or numbered) walked: **17**.
- `PASS` (script reproduces statement): **13** (~76%).
- `PARTIAL` (ingredients covered, displayed form not fully asserted): **3** (eq:A6-euler, Einstein-sum form, S_gen).
- `NO SCRIPT`: **1** (A1 / S_gen — definitional; optional stub suggested).

### Recommendations for v4.5

1. **D5 upgrade** (already flagged in plan): extend `D5-persistent-homology.py` with a symbolic verification of the Matsubara `H_3(ν) φ(ν)` coefficient in Eq. `eq:A6-euler`, matching the prefactor `σ_0 S_3 / 6`.
2. **Optional `D13-crossed-product-entropy.py`**: 30-line sympy/numpy stub reproducing `S_gen = A/(4 G_N) + S_matter` in the II_1 algebra (CLPW2023 Eq. 4.15 form), to close the A1 axiom gap.
3. **D8 figure annotation**: `section_3_6` already flags `FIGURE-UPDATE-PENDING` for `c'=1/6` as the primary marked exponent; carry out in v4.5.
4. No action required on the Einstein-equation line (sum-over-sources is definitional).
