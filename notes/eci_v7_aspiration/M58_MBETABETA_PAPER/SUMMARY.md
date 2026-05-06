---
name: M58 m_ββ paper LMP/PRD letter — sharp prediction [1.4, 3.7] meV
description: ECI v7.4 NPP20+CSD(1+√6) at τ=i gives m_1=0 exact → m_ββ ∈ [1.4, 3.7] meV (NuFIT 5.3 NO, Majorana phases free). KamLAND-Zen 800 current 28-122 meV (8-33× above). KamLAND-Zen2 2027 6-10 meV floor consistent. Post-2035 <2 meV decisive. Falsifier m_ββ>50 meV. Hallu 87→87
type: project
---

# M58 — m_ββ LMP letter (Sonnet, ~5min)

**Date:** 2026-05-06
**Hallu count:** 87 → 87 (held; NuFIT/KamLAND values from training, flagged for live re-verify before submission)

## Headline result

ECI v7.4 NPP20 + CSD(1+√6) Littlest Modular Seesaw at τ_S = i:
- 2-RHN seesaw → M_ν RANK-2 → **m_1 = 0 EXACT**
- NORMAL ordering: m_1 < m_2 < m_3
- Predicted **m_ββ ∈ [1.4, 3.7] meV** (Majorana phases free, NuFIT 5.3 NO)

## Numerical derivation (NuFIT 5.3 NO + m_1 = 0)

| Component | Value | Source |
|---|---|---|
| sin²θ_12 | 0.303 | NuFIT 5.3 |
| sin²θ_13 | 0.022 | NuFIT 5.3 |
| Δm²_21 | 7.41×10⁻⁵ eV² | NuFIT 5.3 |
| Δm²_31 | 2.511×10⁻³ eV² | NuFIT 5.3 |
| m_2 | 8.61 meV | √(Δm²_21) |
| m_3 | 50.1 meV | √(Δm²_31) |
| **A_2** = \|U_e2\|² m_2 | **2.55 meV** | computed |
| **A_3** = \|U_e3\|² m_3 | **1.10 meV** | computed |
| m_ββ_max (Δφ=0) | 3.65 meV | A_2 + A_3 |
| m_ββ_min (Δφ=π) | 1.45 meV | A_2 - A_3 (>0 since A_2 > A_3) |

**ECI v7.4 prediction: m_ββ ∈ [1.4, 3.7] meV**

## Falsifier protocol (5 sharp tests)

| ID | Observation | ECI v7.4 status |
|---|---|---|
| F8a | m_ββ > 50 meV at ≥3σ | **FALSIFIES** (IO or quasi-degenerate implied) |
| F8b | m_ββ > 10 meV at ≥2σ | **STRONG TENSION** |
| F8c | m_ββ ∈ [1.4, 3.7] meV positive signal | **CORROBORATES** |
| F8d | JUNO INVERTED ordering ≥3σ (~2030) | **FALSIFIES** |
| F8e | DUNE δ_CP ≠ -87° at ≥3σ | **FALSIFIES** lepton sector |

## Experimental status

| Experiment | Era | Sensitivity m_ββ (meV) | ECI test? |
|---|---|---|---|
| KamLAND-Zen 800 | now | 28-122 (NME range) | factor 8-33× above ECI; no tension |
| KamLAND-Zen2 / KamLAND2-Zen | ~2027 | 6-10 | floor consistent with ECI; not decisive |
| nEXO | 2030-2035 | 4-9 | similar; not decisive |
| LEGEND-1000 | 2032+ | 6-9 | similar |
| Post-2035 < 2 meV | undefined | < 2 | **first DECISIVE test** of ECI window |

## Tension with Tavartkiladze 2512.24804 (M54 finding)

- ECI v7.4 (Sp'(4)/S'_4 holomorphic): NO + m_1=0 → m_ββ ≤ 3.7 meV
- Tavartkiladze (Γ_2/S_3 non-holomorphic): IO with m_3=0 → m_ββ ≳ 34 meV (quasi-degenerate)

**Order-of-magnitude qualitative gap**, testable by KamLAND-Zen2. If KamLAND-Zen2 finds 30-50 meV: corroborates Tavartkiladze, falsifies ECI v7.4. If null at 6-10 meV: ECI consistent, Tavartkiladze constrained.

## Files
- `SUMMARY.md` (this file)
- `paper_skeleton.md` — 3-5pp LMP/PRD letter structure
- `experimental_status.md` — KamLAND-Zen, nEXO, LEGEND, JUNO, DUNE timeline + sensitivities

## Production checklist
- [ ] WebFetch NuFIT 6.0 (live nu-fit.org) for latest values
- [ ] WebFetch KamLAND-Zen latest PRL for confirmed limit
- [ ] Verify DKLL19 + LMS22 arXiv numbers
- [ ] Run sympy verification of m_ββ extrema to 4 sig figs
- [ ] Add FIG. 1 (m_ββ vs m_1 band plot)
- [ ] Confirm Hallu before submission (currently 87)

## Discipline
- 0 fabrications by M58
- NuFIT 5.3 + KamLAND-Zen 800 values from training (2025); flagged for live re-verify
- Mistral STRICT-BAN observed
- Sub-agent return-as-text for SUMMARY (parent saved); experimental_status.md saved by M58 directly
- Hallu 87 → 87
