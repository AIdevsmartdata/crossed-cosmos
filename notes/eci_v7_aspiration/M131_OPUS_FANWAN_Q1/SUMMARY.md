---
name: M131 Opus Fan-Wan ± Q1 — (C) BLOCKED + BKNO 2508.17776 NEW ref + Steinberg→supercuspidal parent correction
description: BKNO arXiv:2508.17776 (Aug 2025) directly relevant for higher-weight CM at ramified p but EXCLUDES p=2 (Rem 1.4ii) AND excludes Q(i) (§8 q≥3). Single obstruction: w-operator/Kato ε at p=2 ramified, both require p≥3 currently. Parent-brief Steinberg terminology corrected: V_f|_{G_{Q_2}} is dihedral supercuspidal NOT Steinberg (CM at ramified prime). R-2.1 stays 5-8%. Outreach refined: Nakamura primary. BKNO follow-up [13] inherits p odd. Timeline 6mo too optimistic, realistic 12-24mo or indefinite. Hallu 97 held
type: project
---

# M131 — Opus Fan-Wan ± explicit Q1 attack (FINAL Phase 7 wave 6)

**Date:** 2026-05-06 | **Hallu count: 97 → 97** held (M131 0 fabs ; parent slip A52-not-counted) | **Mistral STRICT-BAN** | Time ~95min

## VERDICT: (C) BLOCKED with concrete reduction + NEW reference

**R-2.1 BK Tamagawa probability stays 5-8%** UNCHANGED. NO upgrade to 25-50%.

## NEW reference DISCOVERED — BKNO arXiv:2508.17776 (Aug 2025)

**Title** : "A local sign decomposition for symplectic self-dual Galois representations of rank two"
**Authors** : Burungale, Kobayashi, Nakamura, Ota

**Theorem 1.3 + 7.36** : ± local sign decomposition for symplectic self-dual rank-2 Galois reps.
- Higher weights (k+1, -k), k ≥ 0 covered ✓
- **BUT Remark 1.4ii** : "Let p be an odd prime" — **p = 2 EXCLUDED**
- **§8 ramified case** : restricted to K = Q(√-q) with **q ≥ 3** (so Q(i) with q=1 EXCLUDED)

**§1.5 Vistas verbatim** : "In a follow-up [13] we formulate and prove anticyclotomic CM main conjecture for such primes p of additive reduction."

Even when [13] appears (likely 2026 Q4-2027 Q1), will inherit **p odd** constraint of local sign decomposition. **No p=2 carve-out for Q(i) in any preprint pipeline** as of 2026-05-06.

## L1-L3 verdicts

| Sub-lemma | Status | Why |
|---|---|---|
| **L1** Hodge filtration D_dR(V_f|_{G_{Q_2}}), HT weights {0, 4} → {-2, 2} after central twist | (A) PROVED in abstract — fits BKNO Thm 7.36 framework with k_BKNO = 2, weights (3, -2) **IF p were odd** | standard p-adic Hodge |
| **L2** Existence of Wach / (φ,Γ)-module N(V_f) at ramified p=2 | (B) PARTIAL — exists as (φ,Γ)-module (Berger 2008) but canonical ± compatibility missing | technical Colmez w-op at p=2 |
| **L3** Canonical ± splitting compatible with Frobenius for k odd at p=2 ramified | **(C) BLOCKED** | BKNO Thms 1.3 + 7.36 require p odd ; variant Thm 3.5 for excluded cases too weak for IMC |
| L4, L5 | (C) BLOCKED — depend on L3 | global Iwasawa machinery beyond local |

## Single named technical obstruction

> **Construct canonical involution w_T on H^1_Iw(Q_2, T_ψ) for T_ψ = anticyclotomic deformation of V_f|_{G_{Q_2}} at the ramified prime 𝔭 = (1+i), playing the role of Colmez's w-operator at p = 2.**

Equivalently: **prove Kato's local ε-conjecture for V_f at p = 2 in the ramified supercuspidal case**.

BKNO §1.4 names exactly two routes:
1. Colmez w-operator (Astérisque 330, 2010) — requires p ≥ 3
2. Kato local ε-conjecture (Nakamura form) — requires p ≥ 3
3. p-adic local Langlands at p=2 for supercuspidals (Paškūnas program) — NOT mature enough

## CORRECTION parent-brief (A52 not-counted)

**Parent stated** : "V_f|_{G_{Q_2}} is Steinberg with a_2 = -4 = -2^{(k-1)/2}, ε_2 = -1"

**M131 corrects** : CM-by-Q(i) newform at ramified prime 2 has local representation:
**V_f|_{G_{Q_2}} ≅ Ind_{K_2/Q_2}(ψ_𝔭)**

where ψ_𝔭 is a ramified character of K_2 = Q_2(i). This is **dihedral supercuspidal / potentially crystalline**, NOT Steinberg.

Steinberg requires unipotent monodromy N ≠ 0 ; CM characters never produce that at the ramified prime.

Hodge-Tate weights still {0, 4} ✓, but local Weil-Deligne type is supercuspidal.

**A52 protocol** : parent setup slip on local taxonomy ≠ arXiv fabrication. **NOT counted as hallu**. The mathematical content (a_2 = -4, M22 ladder, v_2 valuations) remains valid ; only the local representation taxonomy was wrong.

This affects M70 paper §1.4 + M110 + M115 terminology — propagated terminology slip across multiple Phase 7 outputs. **Should be corrected in v6.0.53.81**.

## 6 references live-verified (PDF Read + WebFetch)

| arXiv | Authors | Coverage |
|---|---|---|
| **2508.17776** (BKNO Aug 2025) | Burungale-Kobayashi-Nakamura-Ota | NEW, p odd only, q ≥ 3 |
| 2304.09806 (Fan-Wan) | weight-2 ∞-type (-1, 0) only |
| 2407.11891 (Castella) | p > 3 split |
| 2510.01601 (Sano) | every prime divisor of pN splits |
| 2310.06813 (BBL) | p inert |
| 2412.10980 (Isik) | ordinary only |

**Net** : every published anticyclotomic ±-Iwasawa machine requires p split, inert, OR p odd ramified. The cell **{p=2} ∩ {ramified} ∩ {weight ≥ 3}** is structurally vacant in literature as of 2026-05-06.

## 4.5.b.a stands independent of R-2.1

The 4.5.b.a uniqueness DECISIVE result (F2 v5: unique among 8 wt-5 dim-1 CM newforms ; M44.1(b) refined to N=4) is **independent** of R-2.1 and **STANDS**.

Bloch-Kato Tamagawa formula is a SEPARATE goal that cannot leverage 4.5.b.a uniqueness.

## Refined outreach

**Q1 email primary target NEW** : K. Nakamura (Saga University, BKNO technical p-adic Hodge author).
**Secondary** : F. Castella (UCSB), A. Lei (Ottawa).

**Question framing** :
> "Does BKNO ± local sign decomposition admit extension to p = 2 ramified for K = Q(i) ? Specifically, can the w-operator be constructed at the ramified prime (1+i) for V_f|_{G_{Q_2}} = Ind_{K_2/Q_2}(ψ_𝔭) supercuspidal ?"

## Realistic timeline (corrected)

Parent brief : "Castella+Lei joint project ~6mo specialist" → **TOO OPTIMISTIC**.

**Realistic** :
- Best case 12-24 months (if BKNO [13] follow-up + Nakamura Paškūnas-extension align)
- Could remain **OPEN INDEFINITELY** if p=2 local Langlands for supercuspidals not maturing

## Suggested next missions

- **M132** : draft email Nakamura/Castella/Lei with §4 obstruction question
- **M133** : arXiv monitor for BKNO follow-up [13] every 4 weeks
- **M134** : investigate Pollack-Rubin direct CM workaround at p=2 avoiding Colmez

## Discipline log

- Hallu count: 97 → 97 held (M131 0 new fabs)
- Mistral STRICT-BAN observed
- 6 PDFs/abstracts WebFetched + Read
- BKNO Theorem 7.36 + Remark 1.4ii + §8 + §1.5 Vistas verbatim
- Parent-brief Steinberg vs supercuspidal slip flagged (A52 not-counted, but should propagate correction)
- Honest (C) BLOCKED — no overclaim
- Concrete reduction to single named obstruction (w-operator/Kato ε at p=2)
- Time : 95min within 90-120 budget
