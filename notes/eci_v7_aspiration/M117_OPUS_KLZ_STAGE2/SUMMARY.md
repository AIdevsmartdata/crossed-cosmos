---
name: M117 Opus KLZ Stage 2 — (B) REDUCED + structural correction R3-C-1 mis-typed (critical not non-critical) + fab catch arXiv:2402.03247 Brunault-Letang = CNN hardware FABRICATION
description: Opus deep math 95min. KEY: R3-C-1 in M71 paper conflates Deligne critical (L(f,m) for 1≤m≤k-1=4 BOTH critical) with Beilinson non-critical regulator. Probability 30-40% → 10-15% original ; reformulation R3-C-1' = 5α_1=6α_2 ∈ Q ~95% (M52 already). FAB CAUGHT: arXiv:2402.03247 cited in M76 STAGE2_PLAN.md as "Brunault-Letang 2024 Beilinson-Kato" is HEANA CNN hardware paper (Vatsavai-Karempudi-Thakkar TODAES 2024). 6 references live-verified Brunault 1602.03025 etc.
type: project
---

# M117 — Opus KLZ Eisenstein Stage 2 attack on R3-C-1 (DEEP STRUCTURAL CORRECTION)

**Date:** 2026-05-06 | **Hallu count: 96 → 97** (arXiv:2402.03247 CNN paper fab caught) | **Mistral STRICT-BAN**

## VERDICT: (B) REDUCED — major structural reformulation found

R3-C-1 cannot be solved as currently stated in M71 paper §3, but Opus identified the **fundamental structural mis-typing**:

L(f, 1) and L(f, 2) for f = 4.5.b.a (weight 5) are **BOTH CRITICAL** (Deligne 1979 sense: 1 ≤ m ≤ k-1 = 4). The Beilinson regulator framework (KLZ Eisenstein-symbols arXiv:1503.02888, Brunault Rogers-Zudilin arXiv:1602.03025, Schappacher-Scholl 1988, Deninger-Scholl 1991) applies **only to NON-CRITICAL L-values**.

Therefore R3-C-1 as M71 §3 (eq:K0identity) writes "lifts to an identity in K_0(IndCoh_Nilp(LocSys_GL_2))_Q" via "Beilinson regulator class identity 5·[c_1] = 6·[c_2]" is **structurally mis-typed**. The ratio R(f) = π·L(f,1)/L(f,2) is a **Deligne critical-value ratio** controlled by Damerell-Shimura periods Ω_f^4 cancellation, NOT a Beilinson regulator quotient.

## FAB CAUGHT (parent fabrication)

**arXiv:2402.03247** cited in `/root/crossed-cosmos/notes/eci_v7_aspiration/M76_SAGE_STAGE2/STAGE2_PLAN.md` as "Brunault-Letang 2024 (2024) provides explicit Beilinson-Kato regulator computations" is a **FABRICATION**.

WebFetch arXiv:2402.03247 → actual title:
> "HEANA: A Hybrid Time-Amplitude Analog Optical Accelerator with Flexible Dataflows for Energy-Efficient CNN Inference"
> Authors: Sairam Sri Vatsavai, Venkata Sai Praneeth Karempudi, Ishan Thakkar
> Journal: ACM TODAES 2024

CNN hardware paper, NOT number theory. **Hallu count 96 → 97**.

## Reformulation candidates

**R3-C-1' (Damerell ladder identity 5·α_1 = 6·α_2 in ℚ)** — already known via M52:
- α_1 = 1/10, α_2 = 1/12
- 5 · (1/10) = 6 · (1/12) = 1/2 EXACTLY ✓
- PARI 80-digit + Sage 1e-16 verified
- Probability ~95% (= 5α_1 = 6α_2 ∈ ℚ trivially given M52)

**R3-C-1'' (Damerell lift to K_0 of motive M(f))**:
- Probability ~30-40% (unchanged)
- Requires Steinberg-edge KLZ extension at p=2 ramified

**R3-C-1''' (further lift to LocSys_GL_2 K_0)**:
- Probability ~10-15% (Scholze Bourbaki 1252 Conj. 1.5 still open)

## Brunault Theorem 1.1 application analysis

Brunault arXiv:1602.03025 Theorem 1.1 gives explicit Beilinson regulator on K^k = E^k over Y(N):

∫*_{X^k\{0,∞}} Eis_D^{k_1, k_2}(u_1, u_2) = (k_1+2)(k_2+2)/(2N^{k+2}) · (2π)^{k+1} · i^{k_1-k_2+1} · Λ*(F_eisen-product, 0)

For weight k+2 = 5: k = 3 (Kuga-Sato 3-fold E³ over X_1(N)). (k_1, k_2) ∈ {(0,3), (1,2), (2,1), (3,0)} with k_1 + k_2 = 3.

**Critical observation**: Theorem 1.1 produces ONE Λ* of an **Eisenstein-product modular form**, not a ratio L(f,1)/L(f,2). For f = 4.5.b.a, N = 4: Eisenstein products on Γ_1(16). Mapping to L(f, m) of f itself requires f-isotypic projection + Rankin-Selberg unfolding.

**Adapted falsifier path**: re-state R3-C-1 at **non-critical** twists. Critical strip = {1, 2, 3, 4}. Non-critical integers = m ≤ 0 or m ≥ 5. Ratios L(f, 0)/L(f, 5) or L(f, -1)/L(f, 6) accessible to KLZ + Brunault.

## 6 references live-verified

1. **Kings-Loeffler-Zerbes 2017** "Rankin-Eisenstein classes and explicit reciprocity laws" arXiv:1503.02888 ✓
2. **Kings-Loeffler-Zerbes 2018** "Rankin-Eisenstein classes for modular forms" arXiv:1501.03289 ✓ (M39 mis-cited journal — TBD verify)
3. **Brunault 2017** "Régulateurs modulaires explicites via Rogers-Zudilin" arXiv:1602.03025 Compositio Math. 153 ✓
4. **Brunault-Chida 2016** "Regulators for Rankin-Selberg products" arXiv:1503.04626 ✓ (weight 2 only)
5. **Schappacher-Scholl 1988** Perspectives in Math. 4, pp 273-304 ✓ ("weight two" only explicit)
6. **Ito 2016** arXiv:1605.01145 ✓ (CM elliptic, weight 2 only)

## Recommendations

1. **M71 paper §3 amendment** : Conjecture R3-C-1 "lifts to identity in K_0(IndCoh_Nilp(LocSys_GL_2))_Q" → soften to "is conjectured to lift, conditional on Scholze 1252 Conjecture 1.5 made explicit". Add Remark stating L(f,1) + L(f,2) are BOTH critical, framework is **Deligne 1979** not Beilinson 1985, categorical lift conditional on geometric-Langlands number-field analog.

2. **M76 STAGE2_PLAN.md correction** : remove arXiv:2402.03247 fab citation. Replace with arXiv:1602.03025 (Brunault Compositio 2017).

3. **Re-state R3-C-1 Stage 2 falsifier** at non-critical twists L(f, -1)/L(f, 6) where Brunault Thm 1.1 + KLZ apply directly.

4. **Stage 2 cost revised** : 150-300 CPU-hr (Steinberg-edge KLZ extension + regulator numerics). Original 50-100 underestimated p=2 ramified specialist work.

5. **Outreach refined** : Brunault (ENS Lyon, Theorem 1.1 specialization) ; Loeffler (EPFL, KLZ §7 Steinberg-edge) ; Mellit (Vienna, polylog regulator code) ; Scholze (Bonn, low priority, Bourbaki 1252 explicit).

## TBD inventory (5 honest)

1. TBD-M117-1 : Steinberg-edge KLZ §7 explicit reciprocity at a_2 = -2^{(k-1)/2}
2. TBD-M117-2 : K_0(IndCoh_Nilp(LocSys_GL_2))_Q over number fields (Scholze 1252 explicit)
3. TBD-M117-3 : explicit Damerell α_m at weight 5 CM Q(i) **first principles** (M52 numerical, Damerell 1970/1971+Shimura 1976 weight 2 only)
4. TBD-M117-4 : Brunault Eis_D^{k_1, k_2} on K_3 = E³ over X_1(4) at τ = i with f-isotypic projection
5. **TBD-M117-5 NEW** : re-derivation R3-C-1 at non-critical twists where KLZ + Brunault directly apply

## Discipline log

- Hallu count: 96 → 97 (arXiv:2402.03247 fab caught in M76 STAGE2_PLAN.md)
- 6 NEW arXiv WebFetch verifications
- Brunault Theorem 1.1 read full PDF
- Schappacher-Scholl 1988 weight-2 limitation verified
- Mistral STRICT-BAN observed
- Honest (B) REDUCED — major structural reformulation > overclaim PROVED
- Time: 95min within 90-120 budget
