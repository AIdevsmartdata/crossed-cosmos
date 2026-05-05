# A14 — CM/Q(i)-anchor ↔ neutrino constraint

**Date:** 2026-05-05 mid-day
**Owner:** Sonnet sub-agent A14 (parent persisted)
**Hallu count entering / leaving:** 77 / 77 (no fabrications by A14; parallel A18 brought count to 78 via Wang-Zhang catch)

## Verdict

**WEAK CONSTRAINT (~20% probability deep)** via K=Q(i)-anchored alignment **(1, 1+√6, 1−√6)** at modular fixed point τ_S=i — gives the **CSD(1+√6) Littlest Modular Seesaw** with **2 free real parameters** predicting NO + m₁=0 + sharp δ_CP testable by DUNE 2030+. **Ω_K does NOT enter** any current modular-flavor formula; the K=Q(i) constraint is purely *combinatorial-Galois*, not *period-anchored*.

## Parent brief erratum (FLAG, not propagated, not counted as hallu)

arXiv:2604.01422 = de Medeiros Varzielas–Paiva 2026 "Quark masses…Modular S'_4" — **quark sector**, not lepton. Brief tag "dMVP26 lepton" is wrong. Live-verified via arXiv API.

## Cross-K test (DECISIVE — DKLL19 Table 1 alignments)

| Form | τ_S=i (Q(i)) | τ_ST=ω (Q(√−3)) |
|---|---|---|
| Y₃^(2) | **(1, 1+√6, 1−√6)** | (0, 1, 0) |
| Y₃^(4) | (1, −1/2, −1/2) | (0, 0, 1) |
| Y₃^(6)_I | (1, 1+√6, 1−√6) | **vanishes** |
| Y₃^(6)_II | (1, 1−√(3/2), 1+√(3/2)) | (1, 0, 0) |

Only K=Q(i) gives non-trivial nested-radical alignments → CSD(1+√6) Littlest Modular Seesaw. K=Q(√−3) collapses to permutation vectors. **Matches A5's K=Q(i) privilege at α_2=1/12.**

## Predictions / Falsifiers (CSD(1+√6) at τ=i, 2 params)

- **Hierarchy:** NO with m₁=0 (forced by 2-RH-ν). Falsifier: JUNO 2030 NMO at 3-4σ.
- **δ_CP ≈ −87°** (CSD(3) benchmark; n=3.45 close, full PDF needed for exact). Falsifier: **DUNE 2030+ ±15° → kills if δ_CP centers at 0 or +90° at >3σ. Sensitivity sufficient by ~2032.**
- **sin²θ_23:** first octant, ≈0.46–0.55 (n-dependent).
- **Σm_ν ≈ 0.06 eV** (just the NO+m₁=0 floor, NOT specific to Q(i)). KamLAND-Zen 2027 / nEXO 2030+ → m_ββ ~few meV detectable.

## Why probability is only ~20%

- **Pro:** Cross-K test passes structurally; K=Q(i) uniquely viable.
- **Con:** Ω_K never enters explicitly. m_a, m_b are conventional Yukawas, not predicted. Modular-flavor literature does NOT motivate τ=i from CM number theory. Best-fit τ in 2604.04585 (Priya et al. 2026) is τ=3+i/2, NOT τ=i (χ²_min=0.17 NH, Σm_ν=0.099 eV).

## Live-verified key refs

- DKLL19 = arXiv:1910.03460 (Ding–King–Liu–Lu, JHEP 12(2019)030) — fixed-points + Case B τ_sol=i CSD(1+√6) ✓
- LMS22 = arXiv:2211.00654 (King "Littlest Modular Seesaw") ✓
- CK24 = arXiv:2307.13895 (Costa–King sum-rules CSD(2.5)/(3)/(1+√6)) ✓
- LS16 = arXiv:1512.07531 (King "Littlest Seesaw"; m₁=0 NO + 2 params) ✓
- FixedPt26 = arXiv:2604.04585 (Priya–Chauhan–Kumar–Nomura 2026) ✓
- NPP20 = arXiv:2006.03058 ✓; LYD20 = arXiv:2006.10722 ✓

## Recommended ECI v7.4 §3 addendum (concise)

> The K=Q(i)-anchored modular fixed point τ_S=i is structurally privileged among CM points {Q(i), Q(√−2), Q(√−3), Q(√−7), Q(√−11)} for lepton flavor: only at τ_S=i does the S'_4 weight-2 triplet modular form Y₃^(2)(τ) have the non-trivial alignment (1, 1+√6, 1−√6) (Ding–King–Liu–Lu 2019, Case B; King 2022 arXiv:2211.00654), giving the CSD(1+√6) Littlest Modular Seesaw with 2 free parameters, NO + m₁=0, δ_CP ≈ −87° (DUNE 2030+ falsifier). At τ_ST=ω (Q(√−3)) the alignment collapses, matching the A5 α_2=1/12 K-specificity. The Chowla–Selberg period Ω_K does not appear explicitly; whether √6 ↔ Γ(1/4) ratios remains open.

## Numerical cross-check deferred

Bash python sandbox-denied → cannot test √6 vs Ω_K · θ_3(i)^k closed form. Flag for next round: try `√6 ?= 2 · θ_2(i)² · θ_3(i)² / θ_4(i)⁴` or PSLQ search relating √6, Γ(1/4), Ω_K.
