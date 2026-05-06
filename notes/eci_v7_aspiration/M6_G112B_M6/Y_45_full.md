# M6 — Full Y_45 Matrix Derivation

**Sub-agent:** M6 (Sonnet 4.6)
**Date:** 2026-05-06
**Hallu count entering / leaving:** 85 / 85

---

## 1. Definition: Y_45^{ij} = κ_i · f^{ij}(τ*)

The 45_H Yukawa matrix in the ECI v7.4 modular S'_4 SU(5) framework is:

```
Y_45^{u}_{ij} = κ_i · f^{ij}(τ*)          [up-sector coupling, SU(5) 10×10×45]
Y_45^{d}_{ij} = (−3) · κ_i · f^{ij}(τ*)   [down-sector, Georgi-Jarlskog factor]
```

where:
- κ_i ∈ {κ_u, κ_c, κ_t} are three independent per-row coupling strengths
- f^{ij}(τ*) is the modular template from A22 (see f_ij_at_tau_i.md)
- τ* = −0.1897 + 1.0034i is the W1 attractor modulus
- The factor −3 is the Georgi-Jarlskog Clebsch-Gordan from SU(5) 45_H
  representation acting on the d-sector (d-quarks and charged leptons have
  opposite-sign coupling relative to the 5_H; the ratio m_s/m_μ ≈ 1/3 at
  the GUT scale is explained by this −3 factor)

---

## 2. Georgi-Jarlskog factor: derivation sketch

For SU(5) with 5_H (fundamental) and 45_H:

```
Yukawa Lagrangian: ε_{αβγδε} (10_i)^{αβ} (10_j)^{γδ} (45_H)^ε_ζ + h.c.
```

The 45_H decomposes under SU(3)×SU(2)×U(1) as:
- Contains (3̄,1)_{1/3} component T_45 — the colored Higgs triplet
  mediating proton decay via Haba's Eqs. (18)−(23)
- In the down-quark / charged lepton sector, the 45_H gives an extra
  Clebsch factor: Y_d,lept from 45_H gets a −3 relative to Y_d,lept from 5_H

This is the Georgi-Jarlskog mechanism (Phys. Lett. B 86:297, 1979) that
explains m_s/m_μ ≈ 1/3 and m_d/m_e ≈ 3 without extra fields.

For the proton-decay operator, the relevant coupling is between:
- The colored triplet T_45 of 45_H
- The diquark and lepton-quark operators entering the d=6 4-Fermi vertices

The result: Y_45^{d}_{ij} = −3 × Y_45^{u}_{ij} for the RLRL operators
(Haba arXiv:2402.15124 Sec. 3–4, PTEP 2024 053B07, live-verified by A22).

---

## 3. κ_i values from M2/A26 fit

From A26 (M2 PASS), the GUT-scale Yukawa eigenvalues are:
```
y_u = 2.488 × 10⁻⁶
y_c = 1.214 × 10⁻³
y_t = 4.454 × 10⁻¹
```

The M2 fit determines the TOTAL up-quark matrix M_u^{total} = M_u^{(5)} + M_u^{(45)}.
The κ_i are NOT individually fixed by M2 (M2 fits only M_u^{(5)} = α_u × f^{ij}(τ*)).
The κ_i are free parameters of the 45_H sector, constrained by:

1. **Perturbativity:** max(κ_i × |f^{ij}|) < 4π ~ 12.6
   At τ*: max(|f^{ij}|) is the (2,0) entry = 546.97
   → κ_t < 12.6 / 546.97 ~ 0.023

2. **Top quark mass:** κ_t × |f^{t,t}(τ*)| must not cancel the 5_H top contribution.
   The 5_H gives y_t = 0.4454; the 45_H correction must be sub-leading:
   κ_t × |f^{tt}(τ*)| < 0.5 × 0.4454 (M6 Bayesian scan prior)
   |f^{tt}(τ*)| = |f^{2,2}(τ*)| = 502.93
   → κ_t < 0.5 × 0.4454 / 502.93 ~ 4.4 × 10⁻⁴

3. **Charm mass closure (+19.5%):** The M3 Patel-Shukla matching gives:
   κ_c × |f^{cc}(τ*)| ~ 0.44 × y_c (the +19.5% closure condition)
   |f^{cc}(τ*)| = |f^{1,1}(τ*)| = 6.357
   → κ_c ~ 0.44 × 1.214×10⁻³ / 6.357 ~ 8.40 × 10⁻⁵

4. **Up quark mass:** κ_u unconstrained within perturbativity (y_u emerges from
   destructive interference of Y_5 and Y_45 contributions — "modular naturalness"
   hypothesis allows κ_u ~ 10⁻³ to 10⁻² with fine cancellation)

### Benchmark κ values (from Bayesian scan initial condition):
```
κ_u (benchmark) = 0.05 × y_u / |f^{uu}(τ*)| = 6.77 × 10⁻⁸
κ_c (from +19.5% closure) = 0.44 × y_c / |f^{cc}(τ*)| = 8.40 × 10⁻⁵
κ_t (benchmark) = 10⁻⁴ (baseline, below perturbativity hard limit)
```

### Viable window κ values (from M6 explicit viable scan in modular_grid_results.json):
```
κ_u ∈ [10^{-3.5}, 10^{-2.5}] = [3.16×10⁻⁴, 3.16×10⁻³]
κ_c ∈ [10^{-5}, 10^{-3}]
M_{T_45} ∈ [10^{13}, 10^{15}] GeV
```

NOTE: The viable κ_u is ~1000–4000× larger than the "natural" benchmark.
This is the fine-tuning issue discussed in the PRD draft Discussion section.

---

## 4. Full Y_45 matrix at viable-window benchmark

Taking κ_u = 10⁻³ (central of viable window), κ_c = 8.40×10⁻⁵, κ_t = 10⁻⁴:

**Y_45^{u} (magnitudes):**
```
|Y_45^u_{ij}| = κ_i × |f^{ij}(τ*)|

      j=0 (u)         j=1 (c)         j=2 (t)
i=u:  1.837×10⁻³      2.053×10⁻³      0.822×10⁻³
i=c:  8.507×10⁻⁴      5.340×10⁻⁴      9.425×10⁻⁴
i=t:  5.470×10⁻²      2.088×10⁻²      5.029×10⁻²
```

**Y_45^{d} = −3 × Y_45^{u} (magnitudes, ×3):**
```
      j=0 (d)         j=1 (s)         j=2 (b)
i=u:  5.511×10⁻³      6.159×10⁻³      2.466×10⁻³
i=c:  2.552×10⁻³      1.620×10⁻³      2.828×10⁻³
i=t:  1.641×10⁻¹      6.264×10⁻²      1.509×10⁻¹
```

The (1,0), (1,1), (1,2) u-row entries of Y_45^{u} entering the proton-decay
amplitude are ALL of order 10⁻³. None is Wolfenstein-suppressed to 10⁻⁴ or
smaller. This is the critical difference from Haba's vanilla (κ_u ~ λ⁵ ~ 5×10⁻⁴).

---

## 5. Comparison to Haba-vanilla Y_45

| Entry | Haba vanilla (2nd-gen-only) | ECI modular (this work) | Ratio |
|-------|---------------------------|------------------------|-------|
| Y_45^u_{1,1} (u-row, u-quark) | λ⁵ ~ 5×10⁻⁴ | 1.84×10⁻³ (viable κ_u=10⁻³) | ~3.7 |
| Y_45^u_{1,2} (u-row, c-quark) | ~0 (2nd-gen-only) | 2.05×10⁻³ | ∞ |
| Y_45^u_{2,2} (c-row, c-quark) | λ⁴ ~ 2×10⁻³ | 5.34×10⁻⁴ (κ_c=8.4×10⁻⁵) | 0.27 |
| Y_45^d_{1,1} (u-row, d-quark) | 3λ⁵ ~ 1.5×10⁻³ | 5.51×10⁻³ | ~3.7 |
| Y_45^d_{2,1} (c-row, d-quark) | 3λ⁴ ~ 6×10⁻³ | 2.55×10⁻³ | 0.42 |

The modular off-diagonal entries (u-row, c-col) and (u-row, t-col) are
entirely absent in Haba vanilla, but contribute comparably to the diagonal
in the ECI modular framework.

---

## 6. Impact on p→e⁺π⁰ vs p→K⁺ν̄ ratio

**Key amplitude for p→e⁺π⁰:** involves Y_45^{u}_{1,1} × Y_45^{d}_{1,1} (leading)
At κ_u = 10⁻³: |Y_45^{u}_{1,1} × Y_45^{d}_{1,1}| ~ 1.84×10⁻³ × 5.51×10⁻³ = 1.01×10⁻⁵

**Key amplitude for p→K⁺ν̄:** involves coherent sum including Y_45^{u}_{2,2} × Y_45^{d}_{1,1}
and Y_45^{u}_{1,1} × Y_45^{d}_{1,2} (Haba Eq. 22 bracket)

The B-ratio B(e+π⁰)/B(K+ν̄) is determined by the ratio of these amplitude-squared
sums, not just single matrix entries. See b_ratio_derivation.md for the full calculation.
