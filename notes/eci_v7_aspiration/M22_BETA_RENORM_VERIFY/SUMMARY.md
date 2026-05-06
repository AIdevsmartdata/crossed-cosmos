---
name: M22 β-renormalized monotonicity validation
description: FORMULA-SPECIFIC verdict. Only F1 (M13 baseline) achieves strict monotonicity 1/8 formulas. M13 paper must derive F1 from Frobenius degeneracy compensation BEFORE claiming monotone pattern as evidence
type: project
---

# M22 — β-renormalization robustness (Phase 3.D)

**Date:** 2026-05-06
**Owner:** Sub-agent M22 (Sonnet)
**Hallu count entering / leaving:** 85 / 85

---

## Verdict: FORMULA-SPECIFIC

Only F1 (M13 baseline α_m · (-2^{m-1}) · (1+2^{m-3})) achieves strict monotonicity v_2 = {-3, -2, 0, +1}.

7 alternative renormalizations tested:
- F2 Pollack-style: triple tie {-1, -1, -1, +1}
- F3 FE-antisymmetrization: symmetric {-2, -3, -3, -2}
- F4 FE-symmetrization: symmetric {-3, -4, -4, -3}
- F5 Euler-factor compensation: degenerate {+∞, -2, -3, -2}
- F6 Iwasawa-log: unchanged {-1, -2, -3, -2}
- F7 Gauss-triangular: weak {-1, -1, 0, +4}
- F8 Galois-twist: oscillating {-1, 0, -1, +3}

**Strictly monotone: 1/8. Weakly increasing: 3/8.**

## Key insight: F1 IS theoretically motivated

The (1+p^{m-3}) factor "arises naturally from local Euler factor structure when β=0
forces renormalization of classical Pollack framework, adapted to Steinberg-edge case."

[TBD: prove exact Euler-factor derivation of F1.]

## NEW STRUCTURAL FINDING (interlinking M13's three findings)

**Cross-newform check** revealed that α_3/α_2 = 1/√N rationality requires N perfect square.

Among small CM weight-5 newforms (per A5 data):
- 4.5.b.a: N=4=2² ✓
- All others (N=7, 8, 11, 12): irrational α_3, v_2 undefined

**M13's three findings are STRUCTURALLY INTERLINKED via N=p²**:
- Finding 1 (Steinberg-edge a_p = -p^{(k-1)/2}) requires N=p²
- Finding 2 (functional-equation symmetrization clean) requires N square
- Finding 3 (β-renorm monotonicity well-defined) requires N square

This rationality is a consequence of the Steinberg-edge property: N=p²=4 ⟹ √N=p=2 rational prime.

## Implications for Conjecture M13.1

**M13.1(c)** ("Damerell ladder consistency post-renormalization") supported BUT not proven:
- Computation shows F1 gives monotone v_2, consistent with conjecture
- Monotonicity under F1 specifically ≠ "L-function has monotone 2-adic structure" — formula does work
- Paper-2 must:
  (i) state F1 as canonical renormalization motivated by Euler-factor theory
  (ii) prove the Euler-factor motivation for F1
  (iii) then state M13.1(c) as theorem about F1-renormalized values

## Recommendation to M13/paper-2

In the paper, **explicitly derive F1 from Frobenius degeneracy compensation BEFORE claiming the monotone pattern as evidence for p-adic interpolation**. Without that derivation, a referee will correctly note that monotonicity was achieved by formula choice.

## Files
- `SUMMARY.md` — this file
- `formula_comparison_table.md` — 8-formula × 4-m v_2 table
- `cross_newform_check.md` — rationality obstacle for non-square N

## Discipline
- Hallu count: 85 → 85
- Mistral STRICT-BAN observed
- Exact rational arithmetic, hand-verified, no Bash needed
