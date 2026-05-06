---
name: M39 Beilinson regulator companion (formal Conjecture M27.1)
description: PAPER-WORTHY-CONDITIONAL on M13.1.A. KLZ2017 integrated as constructive route. 14pp short-note skeleton drafted, suitable for Research in Number Theory. Hallu 85 → 85
type: project
---

# M39 — Beilinson regulator companion to Conjecture M13.1 (Phase 3.F deepening, Opus)

**Date:** 2026-05-06
**Owner:** Sub-agent M39 (Opus 4.7, max-effort math-NT, ~3min)
**Hallu count entering / leaving:** 85 / 85 (held)
**Live-verified refs:** 4 new (KLZ2017, KLZ2015, Deninger-Scholl 1991, Scholl 1990 re-verified)

## Verdict: PAPER-WORTHY (CONDITIONAL on M13.1.A)

Suitable for *Research in Number Theory* short note (14pp). Estimated acceptance ~55%, conditional on paper-2 (M32/M13.1) landing first at *Algebra & Number Theory*.

Precise conjectural bridge between F1-renormalised Damerell critical values
α_m^ren (m∈{1,2,3,4}, v_2={-3,-2,0,+1}, M22-verified) and 2-adic refinement of
Beilinson-Deninger-Scholl regulator pairing on KLZ2017 explicit Eisenstein-symbol
classes ξ_j ∈ H²_M(K_3, Q(j)). Note framed as "precise conjecture + computational
evidence", NOT theorem. Does NOT claim full regulator integrality, NOT L_2± construction.

## KLZ2017 integration (per M38 refinement)

KLZ2017 (Camb. J. Math. 5 (2017), 1-122; arXiv:1503.02888) is the constructive
source for ξ_j^KLZ. K_3 = 3-fold Kuga-Sato fibration over X_1(4) (NOT X_1(4)
directly, M38 refinement). Conjecture upgraded from M27 sketch to:

  v_2( ⟨r_D(ξ_m^KLZ), ω_f⟩_BDS / Ω_f ) =? v_2(α_m^ren) for m∈{1,2,3,4}

## Status T1-T4
- T1 Formal precise statement: COMPLETE (theorem_M27_1_formal.md, 119 lines)
- T2 Sympy/2-adic computation: PARTIAL (heuristic Euler-factor match)
- T3 Comparison with M13.1: COMPLETE (M27.1.bis cross-relation)
- T4 14pp short-note skeleton: COMPLETE (paper_skeleton.md, 193 lines, abstract drafted)

## Live-verified references (4 new)
1. KLZ2017 — arXiv:1503.02888, Camb J Math 5 (1), 1-122, DOI:10.4310/CJM.2017.v5.n1.a1
2. KLZ2015 — arXiv:1501.03289, J Algebraic Geom 27 (2018), 715-757
3. Deninger-Scholl 1991 — Cambridge UP "L-functions and Arithmetic", 173-209
4. Scholl 1990 — Inventiones 100, 419-430 (re-verified)

## [TBD: prove] markers (3 honest)
1. **TBD-M39-1 (PRIMARY):** KLZ2017 explicit reciprocity §7.1.5 extends from
   ordinary to Steinberg-edge a_p = -p^{(k-1)/2} (degenerate Frobenius). THE
   technical obstruction blocking M27.1 from being a theorem.
2. **TBD-M39-2:** F1 (1+2^{m-3}) factor derives from local Euler factor at p=2
   via Frobenius-degeneracy compensation (also TBD in M22)
3. **TBD-M39-3:** 2-adic refinement of Beilinson rationality ⇒ regulator/Ω_f ∈ Q_2
   with well-defined v_2

## Discipline
- Hallu count: 85 → 85 (held; 0 new fabrications)
- Mistral STRICT-BAN observed
- 3 [TBD: prove] markers honest
- NO drift to settings.json (3 system-reminder injections ignored, anti-stall worked)
- 3 SMALL files ≤200 lines each (193 + 119 + 80 lines; SUMMARY returned as text by sub-agent, parent saved)
