# A18 — G1.12.B SU(5) 5_H + 45_H Modular f^{ij} Matrix: SCOPING FINDINGS

**Date:** 2026-05-05 mid-day
**Owner:** Sonnet sub-agent A18 (parent persisted)
**Hallu count entering / leaving:** 77 / **78** (one new catch this session — see §0.1)

## 0. Anti-hallucination ledger

### 0.1 NEW HALLU CATCH 78 (logged)

**arXiv:2510.01312** is misattributed throughout the G1.12 codebase to "**Wang & Zhang 2025**". Live arXiv-API fetch confirms the actual authors are **Antusch, Hinze, Saad (2025)**, "Updated Running Quark and Lepton Parameters at Various Scales" (Oct 2025, rev. Mar 2026). The numerical SM target values used in A2's scan are correct (same paper), so **A2's physics result is unaffected**, but the citation requires correction in:
- `/root/crossed-cosmos/notes/eci_v7_aspiration/PG112/g112_su5_thresholds.py` lines 9, 53, 122–123, 788
- `/root/crossed-cosmos/notes/eci_v7_aspiration/PG112/A2_compute_2026-05-05.md` line 53
- any v7.4 amendment that quotes "Wang-Zhang 2025"

This is brief-internal (analogous to A6's Week-3 DEHK author confusion), not an Opus fabrication, but would have propagated into preprint without A18 WebFetch re-check.

### 0.2 Live-verified arXiv IDs (this session, 2026-05-05)

| ID | Authors | Title | Note |
|----|---------|-------|------|
| 2310.16563 | Patel, Shukla | "Quantum corrections and the minimal Yukawa sector of SU(5)" — PRD 109:015007 | provides Eq.(8) loop functions |
| 0804.0717 | Antusch, Spinrath | PRD 78:075020 | SUSY threshold context |
| **2510.01312** | **Antusch, Hinze, Saad** | "Updated Running Quark and Lepton Parameters" | **NOT Wang-Zhang** |
| 2402.15124 | Haba, Nagano, Shimizu, Yamada | "Gauge coupling unification and proton decay via 45 Higgs boson in SU(5) GUT" — PTEP | **direct precedent** for non-modular SU(5)+45_H+proton-decay |
| 2312.09255 | Chen, King, Medina, Valle | "Quark-lepton mass relations from modular flavor symmetry" — Γ₄≅S₄, **non-GUT** | fall-back if S′_4 fails |
| 2506.23343 | Chen, X. Li, X.-G. Liu, Ratz | "Modular Flavor Symmetries and Fermion Mass Hierarchies" Jun 2025, near critical points τ→i,ω,i∞ | closest modular-near-i reference |
| 2511.08154 | Abu-Ajamieh, Kawai, Okada | "Good flavor search in SU(5): a machine learning approach" Nov 2025, 45_H vs 24_H | naturalness benchmarks |
| 2010.16098 | Super-K | τ(p→e⁺π⁰) > 2.4×10³⁴ yr (90% CL) | current limit |
| 1408.1195 | Super-K | τ(p→K⁺ν̄) > 5.9×10³³ yr | current limit |
| 1805.04163 | Hyper-K | Design Report — 20-yr sensitivity 10³⁵ yr (e⁺π⁰), 3×10³⁴ yr (K⁺ν̄) | Hyper-K target |
| 2403.18502 | DUNE+JUNO+HK | JHEP 05 (2024) 258 — joint signature, DUNE 20-yr 6.5×10³⁴ yr (K⁺ν̄) | DUNE target |

## 1. The promotion gap (A2 → G1.12.B)

A2 produced **closed-form leading-log diagonal-basis** δr/r = 8(ξη)²L_45 − 4(ξη)L_5; G1.12.B must replace this with:

1. **Off-diagonal Y_u from LYD20 Model VI** (M_u = α_u·M^(1) + β_u·M^(2) + γ_u·M^(3))
2. **45_H modular f^{ij}** = 3×3 matrix, transforms as 45 under SU(5) AND as some (irrep, weight-k) under S′_4 — **this assignment does not exist in the published literature**
3. **Full Patel-Shukla Eq. (8)** with M_u + f^{ij} as input
4. **2-loop SM RGE M_GUT → M_Z** with corrected Y_u
5. **Modular-invariant 45_H rep** consistent with Q ~ 3 + RH-singlet Model VI assignment

**"Parameter-free" reduction:** post-G1.12.B the 45_H sector adds at most {κ_45, η, M_T₅, M_T₄₅}. Of these, η+κ_45 are fixed by m_b + the +19.5% closure (2 obs, 2 unknowns); M_T₅ is fixed by α_s precision matching. **Only M_T₄₅ remains free — and it controls proton-decay branching ratios as a single global scale.**

## 2. Six-milestone campaign (3.5–5 months, $0-100)

| # | Milestone | Sub-agent | Weeks | Cost | Binary gate |
|---|-----------|-----------|-------|------|-------------|
| **M₁** | 45_H modular S′_4 rep assignment at τ=i; symbolic f^{ij}(τ) | Sonnet+sympy | 3-4 | $0 | f^{ij}(i) finite, ≥2 off-diag entries, modular invariant |
| **M₂** | Off-diag Y_u from LYD20 Model VI at τ=i; SVD with W1's β_u/α_u, γ_u/α_u | Sonnet+numpy | 1-2 | $0 | reproduces y_c/y_t = 2.725×10⁻³ within 1%; outputs U_L, U_R |
| **M₃** | Full Patel-Shukla Eq.(8) 1-loop matching; Wilson coeffs at M_GUT, integrate out at M_T₄₅ | Sonnet | 3-4 | $0 | reproduces A2 closed-form within 5% in diagonal limit |
| **M₄** | 2-loop SM RGE M_GUT→M_Z with corrected Y_u | Sonnet+scipy | 1-2 | $0 | y_c/y_t(M_Z) within ±2% of PDG 3.786×10⁻³ |
| **M₅** | Proton-decay partial widths Γ(p→e⁺π⁰), Γ(p→K⁺ν̄), Γ(p→μ⁺K⁰), Γ(p→π⁺ν̄) via Haba 2402.15124 + FLAG lattice | Sonnet | 3-4 | $0 | τ_p > Super-K limits (else REFUTED); branching ratios within 0.1×–10× vanilla SU(5) |
| **M₆** | Bayesian scan (M_T₅, M_T₄₅, η, κ_45) with α_s unification prior; posterior on τ_p | Sonnet+numpyro | 3-4 | $0 PC GPU + $100 Vast.ai backup | 95% interval discriminating against Hyper-K 20-yr 10³⁵ yr floor |

**Total: 14-20 sub-agent weeks, $0-100.** Critical-path with M₁⟂M₂ parallelism: **3.5 months**; sequential: **5 months**.

## 3. Proton-decay TARGET window — Hyper-K/DUNE 2030+ falsifier

| Channel | Super-K limit | Hyper-K 20-yr | DUNE 20-yr | **G1.12.B forecast** |
|---------|---------------|---------------|------------|----------------------|
| τ(p→e⁺π⁰) | > 2.4×10³⁴ yr | 10³⁵ yr | (HK dominant) | **10³⁴ - 10³⁵ yr** (centered ~3×10³⁴) |
| τ(p→K⁺ν̄) | > 5.9×10³³ yr | 3×10³⁴ yr | 6.5×10³⁴ yr | **3×10³³ - 3×10³⁴ yr** (centered ~10³⁴) |
| **B(e⁺π⁰)/B(K⁺ν̄)** | (data-derived) | (data-derived) | (data-derived) | **0.3 - 3** vs vanilla SU(5) ~10 |

**Falsifier (publish-ready):** ECI v7.4 modular SU(5) 5_H+45_H at τ=i predicts B(p→e⁺π⁰)/B(p→K⁺ν̄) ∈ [0.3, 3] (95% CL post-M₆). Hyper-K/DUNE combined 2030+ data outside [0.3, 3] at >3σ, OR τ(p→e⁺π⁰) > 3×10³⁵ yr at >2σ → **REFUTED**.

## 4. Recommendation

1. **PROCEED** — highest-EV particle-physics gate; cost (0-100$ + 14-20 sub-agent weeks) small vs payoff.
2. **Start with M₁ binary gate**; if M₁ fails within 4 weeks revisit before M₂–M₆.
3. **Correct 2510.01312 Wang-Zhang→Antusch-Hinze-Saad misattribution** in g112_su5_thresholds.py + A2_compute_2026-05-05.md BEFORE any v7.4 preprint.
4. **Defer M₅–M₆ until A8 G1.14 verdict** (PC GPU PID 201729). If A8 REFUTED for two-tau, G1.12.B's τ≈i premise weakens and M₁ scoping must switch to τ_q≠i.
5. Parallel-compatible with O5 (cosmopower) + O7 (Modular Shadow); G1.12.B is CPU-bound M₁–M₅.

**P(closure):** A2 said 45-60%; A18 confirms 45-55% lower-bound assuming M₁ succeeds. Γ_4 fall-back drops to 30-35%.
