# A15 — Modular weight-5 multiplet 4.5.b.a vs axion DM (g_aγγ, m_a)

**Date:** 2026-05-05 mid-day
**Owner:** Sonnet sub-agent A15 (parent persisted)
**Hallu count entering / leaving:** 77 / 77 (held; one initial WebFetch wrong-paper caught and corrected via WebSearch)

## Verdict

**WEAK, bordering DEAD-END.** No published modular-axion model uses SL(2,ℤ) weight-5 cusp forms. Matter-field weights in 2024-2025 modular-axion literature are uniformly even (k ∈ {2,4,6,8,10,12,20,24,28}) because Eisenstein E_4, E_6 generate the relevant rings. There is **no derived formula mapping weight-5 of 4.5.b.a to a specific m_a or g_aγγ**.

## Live-verified references (6/6, no Mistral)

| Tag | arXiv | Verified content |
|---|---|---|
| HKK24 | 2402.02071 | Higaki-Kawamura-Kobayashi, "Finite modular axion", JHEP 04 (2024) 147. Uses **k=12**, stabilizes at **Im τ ≫ 1 (near i∞)**, NOT at τ=i. f_a ~ 10¹⁶ GeV. No m_a / g_aγγ. |
| HKKNS24 | 2412.18435 | Higaki et al., "Large and small hierarchies from finite modular symmetries". k=10 universal; Im τ ≫ 1. |
| FKKNO24 | 2409.19261 | Funakoshi et al., "Moduli stabilization and light axion by Siegel modular forms". Six Sp(4,ℤ) fixed points incl. τ=i; ring has only weights 2,4,6 — no weight 5. |
| **Ahn25** | **2511.06355** | **Y.H. Ahn, "Flavored QCD axion and Modular invariance" (Nov 2025). Stabilizes at τ₀ ≈ i (Eq. 42) — CM-by-Q(i) — but uses even weights only (4,8,12,20,24,28) built from E_4, E_6. m_a ≈ 0.9×10⁻² eV (~9 meV), \|g_aγγ\| ≈ 1.7×10⁻¹³ GeV⁻¹, f_a = 4×10¹⁰ GeV.** |
| Cap24 | 2401.13728 | Caputo-Raffelt astro bound g_aγγ < few × 10⁻¹¹ GeV⁻¹. |
| IAXO25 | 2504.00079 | BabyIAXO sensitivity ~1.5×10⁻¹¹ GeV⁻¹ (m_a≈0.02 eV); IAXO target ~10⁻¹² GeV⁻¹. Construction starts 2026; physics 2028-2030. |

## Why weight-5 has no axion footprint

1. Yukawa modular forms transform under Γ_N matching the flavor symmetry; weight-5 of Γ_1(4) (where 4.5.b.a lives) is a *narrower* congruence subgroup than the SL(2,ℤ) and Γ_N (N=2,3,4,5) used in modular-axion model building.
2. Even-weight Eisenstein dominance: Ahn 2511.06355 — the only paper that stabilizes at τ=i (the CM-by-Q(i) point!) — explicitly builds the potential from holomorphic E_4, E_6.
3. The axion *is* Re τ; modular weight enters only as CW-potential normalization, not as a coupling-strength selector. K=Q(i)-specificity (D_K=-4) does not propagate into (m_a, g_aγγ) — those are set by the seesaw scale f_a = 4×10¹⁰ GeV.

## No 2026-2030 falsifier

Even granting the speculative bridge "weight-5 → Ahn-type τ=i model": Ahn predicts g_aγγ ≈ 1.7×10⁻¹³ GeV⁻¹ at m_a ≈ 9 meV, which is **factor ≥6 below 2030 IAXO sensitivity** and outside ADMX/HAYSTAC/MADMAX mass ranges (those cover μeV-100 μeV). MADMAX OB300 at CERN 2026-2029 reaches ~10⁻¹³ but only at m_a ~ 100 μeV, two orders below the 9 meV target.

## Cross-K specificity (A5 logic)

A5 showed α_2 = 1/12 holds **only** for K=Q(i). In Ahn's axion model, τ ≈ i is a generic finite-modular fixed point — the predicted (m_a, g_aγγ) does not depend on D_K = -4. K-specificity is **not** transmitted to axion observables.

## Honest probability

**P(real bridge weight-5 4.5.b.a → testable axion DM constraint by 2030) ≈ 5%.**

Decomposition: ~25% structural correlation at τ=i; × 1/5 for weight-5 vs even-weight ring mismatch; × 1/4 for experimental sensitivity gap ≥ 6 by 2030; rounded up for unmodeled channels.

**Below the ≤15% real-bridge threshold.** Recommend NOT adding modular-axion phenomenology to v7.4. Optional one-paragraph "related work" mention that Ahn 2511.06355 anchors at τ=i — a thin shared coincidence, not a derived bridge.
