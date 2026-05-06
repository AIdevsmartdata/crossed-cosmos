---
name: M171 Opus KW non-cyclotomic K3 — VERDICT (C)/(D) MIXED + CRITICAL M164 correction (cyclotomic was misreading) ; real KW obstruction is K^(1)≇K^(2), Case B fails for ECI v9 in W_(20|20)
description: M171 caught M164 caveat 2 misreading (KW eq 46 is field-iso K^(1)≅K^(2) NOT cyclotomic). Verbatim KW p.28+29 confirmed. ECI v9 vacuum in KW Case A only (DW=0, eq 45 satisfied) NOT Case B (eq 46 W=0 fails since Q(i)≠Q(√-22)). Singular K3 with T(X)⊗Q≅Q(√-22) DOES exist (Schütt 2008 Shioda-Inose), but KW Case B Borcea-Voisin route NOT applicable. 2 escape routes open: H¹⊗H¹ component (OUT-OF-SCOPE in KW) ; generic CY4 non-Borcea-Voisin. M164 caveat 2 NEEDS UPDATE. Hallu 102→103 (+1 M164 misreading cluster)
type: project
---

# M171 — Opus Kanno-Watari extension to non-cyclotomic K = ℚ(√-22)

**Date:** 2026-05-06 | **Hallu count: 102 → 103** (+1 M164 caveat 2 misreading caught) | **Mistral STRICT-BAN** | Time ~115min

## VERDICT (C)/(D) MIXED with critical M164 correction

- (D) PARTIAL ~50%: structural extension to non-cyclotomic K well-defined ; obstruction sharply identified
- (C) NEGATIVE ~30%: KW Case B explicitly cannot realize ECI v9 in W_(20|20)
- (B) REDUCED ~15%: alternative routes (H¹⊗H¹, generic CY 4-fold) leave open partial constructions
- (A) PROVED <5%

**Net effect on M164**: (D) PARTIAL with strong (B)-leaning **slightly degraded** to (D) PARTIAL with mild (C) elements. Not a refutation of F-theory embedding overall, but specifically KW Case B Borcea-Voisin route is **NOT directly applicable** for ECI v9.

## ⚠️ Primary finding: M164's "cyclotomic" attribution was WRONG

**M164 SUMMARY caveat 2 stated**: "Kanno-Watari treat CM K3 with K = Q(ζ_m) cyclotomic (eq 46). Q(i) = Q(ζ_4) ✓ but Q(√-22) is non-cyclotomic — needs refinement."

**This is a mis-reading.** Verbatim from KW arXiv:2012.01111 page 28, eq (46):
> "When ρ⁽¹⁾_(20)(K⁽¹⁾) = ρ⁽²⁾_(20)(K⁽²⁾) ⊂ ℚ̄..."

This is a **field-isomorphism** constraint: the (2,0)-period embeddings of K^(1) and K^(2) coincide as subfields of ℚ̄. It is NOT a cyclotomic constraint. The cyclotomic K = ℚ(ζ_m) requirement appears only in **§3.2.3 (page 43)**, applies only to K3 with Z_m non-symplectic automorphism of order m > 2, and is a different framework (KW §3 generalized orbifolds with Γ ≠ Z_2). KW §2.4 (the relevant section for ECI v9 attractive K3 with rank T_X = 2) treats arbitrary imaginary quadratic K^(i).

**Hallu count**: 102 → 103. This M164 caveat 2 misreading is a fabrication-equivalent (claim in our SUMMARY not supported by source PDF), caught by M171 sub-agent. Cluster +1.

## Real obstruction: K^(1) ≇ K^(2) (consistent with M169)

For imaginary quadratic K^(i) of discriminants d_i, eq (46) ⟺ K^(1) ≅ K^(2) ⟺ d_1 = d_2. ECI v9 has d_L = -4 ≠ -88 = d_Q, so K^(1) = ℚ(i) ≇ ℚ(√-22) = K^(2), and **eq (46) FAILS**.

Hence ECI v9 falls into KW **Case A** (eq 45 satisfied since K_0^(1) = K_0^(2) = ℚ for any imaginary quadratic ; eq 46 violated). KW page 29 verbatim:
> "In case A), with the condition (45), the component W_(20|20) = W_(20|02) is level-4 ... Any flux in this component satisfies the DW = 0 condition but **always violates the W = 0 condition**."

So the standard KW Borcea-Voisin Z_2 orbifold cannot realize ECI v9's W = 0 Minkowski SUSY in the level-4 W_(20|20) component.

## Singular K3 with T(X) ⊗ ℚ ≅ ℚ(√-22) DOES exist

Confirmed via Schütt 2008 arXiv:0804.1558 (PDF Read pp 1-3 verbatim): Pjateckii-Šapiro/Šafarevič/Shioda-Inose theorem gives bijection {Singular K3} ⟷ {even rank-2 positive-definite lattices}.

For ℚ(√-22), |d_K|=88, h_K=2, the two transcendental lattices correspond to:
- Binary form (1,0,22) [class 1, τ_a = i√22]
- Binary form (2,0,11) [class 2, τ_b = i√(11/2) ← ECI v9 anchor]

Construction via Shioda-Inose: T(X) = T(E × E') with CM elliptic curves E, E' over ℚ(√-22). Field of definition contains the Hilbert class field H(-88) (Schütt Theorem 2).

## Chowla-Selberg P_{-88} verified (mpmath dps=30)

For K = ℚ(√-22): |d_K|=88, h_K=2, w_K=2. χ_{-88} character has **20 residues with χ=+1** and **20 with χ=-1** mod 88:
- χ=+1: {1, 9, 13, 15, 19, 21, 23, 25, 29, 31, 35, 43, 47, 49, 51, 61, 71, 81, 83, 85}
- χ=-1: {3, 5, 7, 17, 27, 37, 39, 41, 45, 53, 57, 59, 63, 65, 67, 69, 73, 75, 79, 87}

log_10(P_{-88}) = 1.98454821676494... ; geom mean |Ω(E_a)|² = 2.5651119...

## Escape routes evaluated

1. **§2.5 T_X ⊊ T_0 escape (eq 63)**: requires non-attractive K3. ECI v9 has both K3 attractive (T_X = T_0, T̄₀ = 0). **CLOSED**
2. **§3 cyclotomic Γ = Z_m, m > 2**: KW §3.2.3 requires K^(i) ⊃ ℚ(ζ_m). ℚ(√-22) is not contained in any quadratic-cyclotomic field beyond ℚ(ζ_88) of degree 40. **CLOSED**
3. **H¹(Z⁽¹⁾;ℚ) ⊗ H¹(Z⁽²⁾;ℚ) component**: KW page 11 verbatim: *"we do not ask whether the Hodge structure on H¹(Z⁽¹⁾;ℚ) ⊗ H¹(Z⁽²⁾;ℚ) is CM-type."* Out-of-scope in KW. **OPEN — specialist follow-up**
4. **Generic CY 4-fold not Borcea-Voisin**: not analyzed by KW. **OPEN**

## Recommendations

1. **Update M164 SUMMARY caveat 2**: replace "cyclotomic constraint" with "field-isomorphism K^(1) ≅ K^(2)" (correction)
2. **ECI v9 manifesto §4.5**: clarify KW arXiv:2012.01111 closest published F-theory framework, but Case B (DW = W = 0 in W_(20|02)) requires K^(1) ≅ K^(2). For ECI v9 with Q(i) ≠ Q(√-22), only Case A applies (DW = 0 fluxes only, NOT W = 0)
3. **Specialist follow-up to Kanno or Watari** (Kavli IPMU): 
   - (a) Does H¹(Z⁽¹⁾) ⊗ H¹(Z⁽²⁾) admit W = 0 fluxes for distinct CM fields?
   - (b) Is there a Case B analog for non-isomorphic CM fields via biquadratic compositum K^(1) · K^(2) = ℚ(i, √-22) of degree 4?
4. **Mohseni-Vafa generic disclaimer "no string examples currently known"** remains the honest fallback for ECI v9 in the same epistemic class.

## Sources verified verbatim

- **Kanno-Watari arXiv:2012.01111** (PDF Read pages 1-58 verbatim, /tmp/kanno_watari.pdf, 825KB)
  - Eq (46) verbatim: page 28
  - Eq (47) verbatim: page 29
  - Page 28 footnote 41 (Aspinwall-Kallosh required K^(1) = K^(2))
  - Page 43 §3.2.3 cyclotomic K = ℚ(ζ_m) appears for Γ = Z_m, m > 2
  - Page 44 footnote 70 (general K-and-T relation)
- **Schütt 2008 arXiv:0804.1558** (PDF Read pages 1-3 verbatim) — singular K3 / transcendental lattice bijection, field of definition theorem
- **mpmath dps = 30** Chowla-Selberg numerical verification (P_{-4} = 27.50, P_{-88} log_10 = 1.985)

## Discipline log

- Mistral STRICT-BAN observed
- KW arXiv:2012.01111 PDF Read 58pp verbatim
- Schütt 2008 PDF Read pp 1-3 verbatim
- mpmath dps=30 numerical
- **Hallu count 102 → 103 (+1 M164 caveat 2 misreading caught by M171, cluster fab)**
- Time ~115min within 90-120 budget

## Files

- /root/crossed-cosmos/notes/eci_v7_aspiration/M171_OPUS_KW_NONCYCLOTOMIC/01_kw_eq46_obstruction.py
- /root/crossed-cosmos/notes/eci_v7_aspiration/M171_OPUS_KW_NONCYCLOTOMIC/02_chowla_selberg_q_sqrt22.py
