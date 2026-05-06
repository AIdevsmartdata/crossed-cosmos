---
name: M54 F8 lepton ordering — TENSION not refutation; m_1=0 exact prediction
description: ECI v7.4 NPP20+CSD(1+√6) Littlest Modular Seesaw at τ=i gives NORMAL ordering with m_1=0 exact (2 RHN, M_ν rank-2). Tavartkiladze 2512.24804 predicts INVERTED — but uses Γ_2≃S_3 (different group). TENSION not refutation. JUNO 2030+ + KamLAND-Zen 2027 testable. Hallu 86 unchanged
type: project
---

# M54 — F8 lepton ordering executed (Phase 4 follow-up, Sonnet, ~5min)

**Date:** 2026-05-06
**Owner:** Sub-agent M54 (Sonnet)
**Hallu count:** 86 → 86 (held; Tavartkiladze 2512.24804 WebFetch-verified)

## Verdict: TENSION (not refutation) + new sharp prediction m_1=0

| Item | Result |
|---|---|
| ECI v7.4 lepton ordering at τ=i | **NORMAL** (m_1 = 0, m_1 < m_2 < m_3) |
| Tavartkiladze 2512.24804 prediction | **INVERTED** (Γ_2 ≃ S_3 minimal models at τ=i) |
| F8 verdict | **TENSION** (different model classes, different orderings) |

## ECI v7.4 lepton sector

**Source**: v75_amendment.tex §8.3 lines 965-1017 — NPP20 + CSD(1+√6) Littlest Modular Seesaw at τ_S=i (H11' axiom, Option C).

**DKLL19 Table 1 Case B alignment** (cited line 888):
```
Y_3^(2)(τ=i) ∝ (1, 1+√6, 1-√6)
CSD parameter n = 1+√6 ≈ 3.449
```

**2-RHN seesaw structure**:
```
Dirac col_1 = (0, a, a)^T            [N_atm, mass M_1]
Dirac col_2 = (b, (1+√6)b, (1-√6)b)^T [N_sol, mass M_2 ≫ M_1]
M_ν = v²_u [col_1 col_1^T / M_1 + col_2 col_2^T / M_2]
```

**M_ν is rank-2 (3×3, 2 RHN) ⟹ m_1 = 0 EXACTLY**

With M_1 ≪ M_2: m_3 (N_atm) dominates m_2 (N_sol) ⟹ **m_1 < m_2 < m_3 NORMAL**.

Verbatim from v75_amendment.tex lines 978-982:
> "predicting normal ordering with m_1=0, Dirac CP phase δ_CP ≈ −87°, first-octant sin²θ_23 ≈ 0.46–0.55, and Σm_ν ≈ 0.06 eV"

## Numerical crosscheck (a=b=1, M_1=1, M_2=1000)

```
col_1 = (0, 1, 1)
col_2 = (1, 3.449, -1.449)
M_ν ≈ [[0.001, 0.00345, -0.00145],
        [0.00345, 1.0119, 0.9950],
        [-0.00145, 0.9950, 1.0021]]
Eigenvalues = {0, 0.00265, 2.013}
Masses ∝ {0, 0.0515, 1.419}
→ NORMAL ordering confirmed analytically.
```

Δm²_21 > 0 (solar, NormalOrdering) and Δm²_32 > 0 (atmospheric, NO) — consistent with NuFIT 5.3 NO ✓.

## Why TENSION not refutation

| Property | ECI v7.4 | Tavartkiladze 2025 |
|---|---|---|
| Modular group | Sp'(4) / S'_4 level-4 holomorphic | Γ_2 ≃ S_3 level-2 non-holomorphic |
| τ=i alignment | (1, 1+√6, 1-√6) DKLL19 | Different S_3 texture |
| CSD parameter | n = 1+√6 ≈ 3.449 | N/A |
| m_1 | 0 (exact, from 2RHN) | Non-zero allowed |
| Ordering | NORMAL | INVERTED |

**τ=i fixed point alone does NOT determine ordering** — the modular symmetry group matters.

## Implications for v7.6 / paper portfolio

1. **M49 B5b paragraph must be AMENDED**: Tavartkiladze 2512.24804 is no longer a "corroboration bridge" — it's a TENSION. Revised wording for v7.6 §10:
   > "Tavartkiladze (arXiv:2512.24804) demonstrates that minimal Γ_2 ≃ S_3 textures at τ=i predict inverted ordering — in TENSION with ECI v7.4's normal ordering prediction from Sp'(4)/CSD(1+√6), illustrating that τ=i alone does not determine neutrino ordering without specifying the modular symmetry group."

2. **F8 remains ACTIVE** as observational falsifier:
   - **JUNO 2030+** at 3-4σ NMO sensitivity will resolve ordering
   - **If INVERTED**: ECI v7.4 lepton sector tension (not refutation; could be lepton sector revision or next-order modular correction)
   - **If NORMAL**: ECI corroborated, Tavartkiladze S_3 models in tension

3. **NEW SHARP PREDICTION**: ECI v7.4 implies **m_1 = 0 exactly** (rank-2 M_ν from 2-RHN seesaw):
   - Testable by KamLAND-Zen 2027 / nEXO 2030+ via m_ββ ~ m_2 sin²θ_12 × (few meV)
   - At edge of next-generation 0νββ sensitivity
   - **Falsifiable** if 0νββ measures m_ββ > 50 meV

## Discipline log
- 0 fabrications
- Tavartkiladze 2512.24804 abstract WebFetch-verified
- ECI v7.4 lepton sector quoted verbatim from v75_amendment.tex
- Numerical crosscheck via numpy
- Hallu 86 → 86 (held)
- Sub-agent return-as-text protocol used (parent saved)
