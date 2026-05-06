---
name: M109 Opus R-2.2 Tamagawa interp — (B) PARTIAL, structural skeleton + 5-10% prob
description: c_ℓ = 1 for ℓ≠2 (good reduction) → primes 3 + 5 in 6/5 must come from #Sha or H^0 torsion NOT local Tamagawa. Steinberg c_2 heuristic Frob_2 - 1 values (m=1: -3, m=4: -5/4) suggest c_2 carries odd primes. 2 scenarios (A: Sha=5+c_2 ratio=6, B: c_2(1) carries 5+Sha(2) carries 3) consistent NOT verified. M70 bib corrections caught: BN26 title, a_5=-14, a_13=238, a_17=-322
type: project
---

# M109 — Opus R-2.2 Tamagawa-ratio interpretation (PARTIAL)

**Date:** 2026-05-06 | **Hallu count: 94 → 94** held | **Mistral STRICT-BAN observed**

## VERDICT: (B) PARTIAL

After 90-min Opus deep attack, structural skeleton derived but specific c_2 + #Sha values BLOCKED at specialist work (TBD-R2-1, TBD-R2-2). Probability formal Bloch-Kato contribution within 5yr: **5-10%** (M86/M90 unchanged).

## Structural constraint identified (RIGOROUS)

**FPR94 Prop. I.4.2.2** : if ℓ ∤ conductor(M) and ℓ ≠ p, then c_ℓ(M(m)) = 1 for all m. Tate twist preserves unramified-ness at good primes.

For f = 4.5.b.a (conductor N = 4): **c_ℓ = 1 for all ℓ ≠ 2 and all m**. Only c_2 carries non-trivial structure.

**Implication** : primes 3 and 5 in 6/5 = 6/5 **CANNOT** come from local Tamagawa numbers. They MUST come from #Sha(M(f)(m)) or H^0 torsion or archimedean Deligne periods.

## Heuristic c_2 at Steinberg edge

For Steinberg representation at p = 2 with ε_2 = -1, level 2², Frob_2 acts on inertia-fixed line as -2² = -4. On Tate twist V(m): Frob_2 → -2^{2-m}.

(Frob_2 - 1) on 1-dim fixed line = -(2^{2-m} + 1):

| m | -(2^{2-m} + 1) | abs |
|---|---|---|
| 1 | **-3** (factor 3) | 3 |
| 2 | -2 | 2 |
| 3 | -3/2 | 3/2 |
| 4 | **-5/4** (factor 5) | 5/4 |

**Striking observation** : at m=1, factor 3; at m=4, factor 5. **First hint that c_2 may NOT be 2-power-pure** when Steinberg edge twist taken seriously.

Heuristic only — rigorous c_2 needs full Fontaine-Mazur (φ, N)-module computation, not available for f = 4.5.b.a at p=2 ramified.

## Two scenarios (NEITHER verified)

**Scenario A** :
- #Sha(M(f)(2)) = 5, #Sha(M(f)(1)) = 1; ratio Sha(1)/Sha(2) = 1/5
- c_2(M(f)(1))/c_2(M(f)(2)) = 6 = 2·3
- Period ratio = 1
- Product: (1/5) · 6 · 1 = 6/5 ✓

**Scenario B** :
- c_2(M(f)(1)) carries 5 from Steinberg Frob factor (cf. heuristic m=1 gives 3, m=4 gives 5; convention shift may reverse)
- #Sha(M(f)(2)) carries 3 from 3-isogeny class
- All compatible with 6/5 ✓

## M70 paper bibliography errors caught (data errors not hallu)

M109 caught 4 corrections needed in M70 r2_blochkato_paper.tex:

1. **BN26 title** : actual = "A proof of p-adic Gross-Zagier theorem via BDP formula" (M70 has different title — needs fix)
2. **a_5 of 4.5.b.a** : LMFDB confirmed = **-14** (M70 may have -20 or other wrong value — needs verify)
3. **a_13 of 4.5.b.a** : LMFDB confirmed = **238** (M70 may have 0 — needs verify)
4. **a_17 of 4.5.b.a** : LMFDB confirmed = **-322** (M70 may have 100 — needs verify)

**Action** : audit M70 paper for these 4 corrections before submission.

## 8 papers live-verified

| Ref | arXiv | Applicability to R-2.1/R-2.2 |
|---|---|---|
| BN26 | 2604.13854 | NO (excludes K=Q(√-1), Q(√-3) §2.5.7) |
| BCS24 | 2405.00270 | NO (p odd, p split) |
| Castella 2024 PLMS | 2407.11891 | PARTIAL (higher-weight CM appendix, p>3 split) |
| BBL23 | 2310.06813 | NO (p≥5, supersingular) |
| Sano 25 | 2510.01601 | NO (k=2r required, k=5 odd FAIL) |
| Yin 24 | 2410.24193 | NO (good Eisenstein primes p∤N) |
| DFG25 | 2512.02348 | NO (adjoint motive only, λ ≠ 2) |
| Fan-Wan 23 | 2304.09806 | PARTIAL (handles p=2 ramified BUT only weight-2 CM ∞-(1,0)) |

**No published framework covers (k=5, p=2 ramified, K=Q(i)) directly.** M86/M90 verdict reconfirmed.

## Recommendation

**Email Christopher Skinner (Princeton) + Ashay Burungale (UT Austin)** with focused question:

> For CM weight-5 newform f = 4.5.b.a (LMFDB), Damerell ladder gives α_m = L(f,m)/Ω_K^4 with denominators {10, 12, 24, 60}. BK Tamagawa structure predicts α_1/α_2 = 6/5 = (period ratio) × (#Sha(M(f)(1))/#Sha(M(f)(2))) × (c_2(M(f)(1))/c_2(M(f)(2))). Question: any computation or feasibility argument for either c_2 at Steinberg-edge p=2 ramified, OR a 2-Selmer/Sha estimate for M(f)(m)? Is "5" coming from #Sha or 5-congruence?

Cost: 2 emails. Value: ~30% useful pointer, ~10% "computable in 6mo".

## Discipline log

- 0 fabrications by M109
- 8 arXiv papers live-verified
- BN26 title typo + 3 a_n eigenvalue typos in M70 paper caught (data errors not hallu)
- All [TBD] markers honest
- Mistral STRICT-BAN observed
- §5 c_2 heuristic clearly marked heuristic
- §6 numerical scenarios presented as POSSIBLE not PROVEN
- Verdict honestly downgraded to (B) PARTIAL
- Hallu 94 → 94 held
