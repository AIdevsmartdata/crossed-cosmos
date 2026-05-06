---
name: R6 Lemniscate-Damerell rationality dichotomy — Sonnet short note skeleton
description: Observation 3.1 (3 newforms PARI 80-digit) + Conjecture 3.3 (provisional, scope-limited). Structural Chowla-Selberg explanation. RNT/JNT 4-6pp short note ready. Hallu 87→87
type: project
---

# R6 — Lemniscate-Damerell rationality dichotomy (Sonnet, ~4min)

**Date:** 2026-05-06
**Hallu count:** 87 → 87 (held; classical refs only, no exotic IDs introduced)

## Files
- `SUMMARY.md` (this file) — verdict + observation + conjecture
- `paper_skeleton.md` — 4-6pp RNT/JNT short note structure with 8 standard refs + 1 [TBD: confirm]

## Key observation (PARI 80-digit, 3 newforms)

Define **R(f) = π · L(f, 1)/L(f, 2)** — Ω-independent invariant of CM weight-5 newforms.

| Form | K | R(f) | Status |
|---|---|---|---|
| **4.5.b.a** | Q(i) | **6/5** | **∈ ℚ** |
| 27.5.b.a | Q(ω) | 3√3 | ∈ ℚ(√3) \ ℚ |
| 12.5.c.a | Q(ω) | (3√3)/2 | ∈ ℚ(√3) \ ℚ |

Plus full Damerell ladder rationality:
- 4.5.b.a (Q(i)): all 4 α_m ∈ ℚ — (1/10, 1/12, 1/24, 1/60)
- Q(ω) cases: α_m ∈ ℚ for m even, ∈ ℚ(√3) for m odd

## Parity structure (key diagnostic)

| Ratio | 4.5.b.a | 27.5.b.a | 12.5.c.a | Pattern |
|---|---|---|---|---|
| π² · L(2)/L(4) | 5 | 81/4 | 12 | always ℚ (even/even) |
| π² · L(1)/L(3) | 12/5 | 27 | 9 | always ℚ (odd/odd, √3 cancels) |
| **π · L(1)/L(2)** | **6/5** | **3√3** | **(3√3)/2** | **ℚ ONLY for K = Q(i) (mixed parity)** |

Mixed-parity ratio is the diagnostic. ODD vs EVEN unpaired indices reveal residual √3 from Im(ω) = √3/2.

## Structural explanation (heuristic, not proof)

For K = Q(i): Chowla-Selberg gives Ω_K = Γ(1/4)²/(2√(2π)) — **lemniscate, real, √3-FREE**.
For K = Q(ω): Ω_K = Γ(1/3)³/(2π√3) — **contains 1/√3 from D_K = -3**.

Hecke Grössencharacter:
- ψ on Q(i): order-4 χ_-4, ∞-type (4,0); even-character pairing → no irrational survives at any m
- ψ on Q(ω): order-6 χ_-3, odd cubic; odd-m positions inherit unpaired √3 via Im(ω)

[TBD: prove formally] via Damerell 1983 + Shimura 1977 §5 period decomposition for order-6 characters.

## Conjecture 3.3 (provisional, NOT a theorem)

For h_K = 1 imaginary quadratic K = Q(√-d):
- (a) R(f) ∈ ℚ ⟺ K = Q(i)
- (b) K = Q(ω) ⟹ R(f) ∈ ℚ(√3) \ ℚ
- (c) Other K (d ∈ {7, 11, 19, 43, 67, 163}): R(f) ∈ ℚ(√d) \ ℚ likely

[TBD: prove] requires:
1. Order-N character parity proof (Shimura 1977 §5)
2. Damerell denominators at conductors beyond (1+i)² (Damerell 1983)
3. Broader sweep K = Q(√-7), Q(√-11) [50+ CPU-hr]

## Honesty discipline

- "Theorem" downgraded to "Observation" + "Conjecture"
- 3 newforms only ⟹ pattern not yet broad-tested
- WebFetch denied during M52 → no live-verify of Chowla-Selberg today; standard textbook knowledge used
- Hallu 87 → 87
- 1 ref ([GS81]) flagged [TBD: confirm] — do NOT cite until MathSciNet verified

## Paper-readiness

**Adequate for RNT/JNT short note IF**:
1. Broader sweep done (K = Q(√-7), Q(√-11))
2. Formal parity proof or Damerell-Shimura citation chain
3. "Conjecture/Observation" framing throughout (not "Theorem")

**Companion to**: M22 paper, M55 uniqueness, M57 Adelic Katz.

## Discipline log
- 0 fabrications by R-6
- All 8 main refs are standard / textbook-level (Chowla-Selberg 1967, Damerell 1971+1983, Shimura 1977, Katz 1978, Cohen-Oesterlé 1977, LMFDB, Borwein-Borwein 1987)
- 1 ref [GS81] flagged for live-verify before submission
- Mistral STRICT-BAN observed
- Sub-agent return-as-text protocol used (parent saved both SUMMARY + paper_skeleton)
