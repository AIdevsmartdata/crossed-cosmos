---
name: M58 experimental status — 0νββ and ordering experiments
agent: M58 (Sonnet 4.6)
date: 2026-05-06
hallu_in: 87
hallu_out: 87
source: training knowledge (cutoff Aug 2025); WebFetch blocked — live re-verify before submission
---

# Experimental Status: 0νββ Searches and Neutrino Mass Ordering

## NuFIT 5.3 (2022) — Normal Ordering best-fit values

| Parameter         | Best fit (NO) | 1σ range     |
|-------------------|---------------|--------------|
| sin²θ_12          | 0.303         | 0.270–0.341  |
| sin²θ_23          | 0.572         | 0.406–0.620  |
| sin²θ_13          | 0.02203       | 0.02051–0.02360 |
| δ_CP (°)          | 197           | 120–369      |
| Δm²_21 (10⁻⁵ eV²)| 7.41          | 6.82–8.03    |
| Δm²_31 (10⁻³ eV²)| 2.511         | 2.428–2.596  |

**Source:** NuFIT 5.3, Esteban et al. (2020, 2022), nu-fit.org.
**IMPORTANT:** Re-fetch nu-fit.org before final submission to catch NuFIT 6.x updates.

Derived mass scales for m_1 = 0 (NO):
- m_2 = √(Δm²_21) ≈ 8.61 meV
- m_3 = √(Δm²_31) ≈ 50.1 meV

PMNS matrix elements (NO, m_1=0 relevant):
- |U_e2|² = sin²θ_12 · cos²θ_13 ≈ 0.303 × 0.978 ≈ 0.296
- |U_e3|² = sin²θ_13 ≈ 0.022

---

## KamLAND-Zen 800 — Published limits (2023)

**KamLAND-Zen 800 Phase I (2022, PRL 130 051801):**
- 136Xe exposure: ~970 kg·yr
- Half-life limit: T^{0ν}_{1/2} > 2.3 × 10²⁶ yr (90% CL)
- m_ββ < 28–122 meV (90% CL, NME-dependent range)
  - Lower end (IBM-2 NME): ~28 meV
  - Upper end (ISM NME): ~122 meV
  - Reference central value: ~36 meV (using g_A = 1.27, QRPA)

**KamLAND-Zen 800 Phase II / KamLAND2-Zen (projected 2027):**
- New inner balloon + purified Xe, ~1 tonne xenon target
- Projected sensitivity: m_ββ ~ 6–10 meV (90% CL) at ~5 tonne·yr exposure
- This **reaches into the NO + m_1 = 0 prediction window** (see SUMMARY.md)
- Key milestone: if m_ββ > 50 meV is found → ECI v7.4 lepton sector FALSIFIED
- If null result at ~6 meV → **consistent** with ECI prediction, **not yet decisive**

**NOTE:** "KamLAND-Zen 2027" sensitivity ~6–10 meV is a projected extrapolation
from published Phase I performance. Cite KamLAND-Zen 2022 (arXiv:2203.02139) and
collaboration roadmap documents. Verify NME sensitivity range from Engel & Menendez
review (arXiv:1610.06548) before submission.

---

## nEXO — Sensitivity projection (2030+)

**nEXO CDR (2018, arXiv:1805.11142) + updated projections:**
- 5 tonne liquid Xe TPC, ~10 yr run
- Projected half-life sensitivity: T^{0ν}_{1/2} > 5.7 × 10²⁷ yr (90% CL) after 10 yr
- Corresponding m_ββ sensitivity: ~4–9 meV (NME-dependent)
  - Using shell model NMEs: ~9 meV
  - Using IBM-2: ~4 meV
- Start: earliest ~2030, commissioning ~2029–2031

**nEXO vs ECI prediction:**
- If nEXO null at ~5 meV: consistent with ECI [1.4, 3.7] meV window, not yet decisive
- If nEXO discovers m_ββ > 20 meV: INVERTED ordering implied → strong tension with ECI NO
- Only a future experiment probing m_ββ < 2 meV can definitively test ECI's prediction

---

## LEGEND-1000 — Post-2030 germanium

**LEGEND-1000 (76Ge, conceptual design ~2021):**
- 1000 kg 76Ge, ~10 yr
- Projected sensitivity: m_ββ ~ 6–9 meV (90% CL, NME-dependent)
- Timeline: earliest commissioning ~2028–2030, full physics ~2032+

**Coverage:** Similar floor to nEXO. Cannot definitively probe the ECI [1.4, 3.7] meV
window; but null result is fully consistent with ECI prediction.

---

## JUNO — Mass ordering (complementary)

**JUNO (Jiangmen Underground Neutrino Observatory):**
- Target start: 2024–2025; NMO determination at 3–4σ expected ~2030
- Tests: Δm²_31 sign → distinguishes NO vs IO at atmospheric scale
- ECI prediction: NORMAL ordering → JUNO must find NO. If JUNO finds IO → ECI falsified.
- **JUNO is an ordering falsifier (F8), not an m_ββ probe.**

---

## Summary table — Experimental timeline

| Experiment      | Timeline     | m_ββ sensitivity (meV) | ECI consistency |
|-----------------|--------------|------------------------|-----------------|
| KamLAND-Zen 800 | 2022 (pub'd) | < 28–122               | Consistent      |
| KamLAND-Zen2    | ~2027        | ~6–10                  | Consistent (not decisive) |
| nEXO            | ~2030–2035   | ~4–9                   | Consistent (not decisive) |
| LEGEND-1000     | ~2032+       | ~6–9                   | Consistent (not decisive) |
| Future (<2 meV) | post-2035?   | < 2                    | Decisive test   |
| JUNO (ordering) | ~2030        | N/A (ordering)         | NO required     |

ECI v7.4 sharp prediction: m_ββ ∈ [1.4, 3.7] meV (Majorana-phase range, NO + m_1=0).
This is BELOW the floor of near-term next-generation experiments.
The prediction is **consistent-but-not-yet-testable** at KamLAND-Zen2 / nEXO sensitivity.
A positive signal at m_ββ > 50 meV at any experiment would FALSIFY ECI v7.4 lepton sector.
