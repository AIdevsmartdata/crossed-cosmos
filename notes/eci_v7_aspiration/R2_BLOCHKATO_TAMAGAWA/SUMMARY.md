---
name: R2 Bloch-Kato Tamagawa for M(f) — VERDICT REVISED to NEEDS-DEEPER (10-15%)
description: R-2 second wave verdict: BUYUKBODUK-NEAMTI BLOCKED by 5 compounding hypothesis violations (K ≠ Q(i) EXPLICIT EXCLUSION!). All 2024-2025 TNC papers (Castella, BBL, Sano, Yin, DFG) also blocked for (p=2 ramified, k=5 odd, K=Q(i), N=4) regime. Conjecture R-2.1 stated; 5 [TBD: prove] including 6/5 = Selmer-quotient × Tamagawa-ratio factorization VERY HIGH OPEN. Hallu 87→87
type: project
---

# R-2 Bloch-Kato Tamagawa for M(f), 4.5.b.a — REVISED verdict (Opus second wave, ~3h)

**Date:** 2026-05-06
**Hallu count:** 87 → 87 (held; 8+ refs live-verified including HTML hypothesis extraction)

## VERDICT REVISED: NEEDS-DEEPER (not VIABLE-NEW-PISTE)

R-2 first wave verdict was VIABLE-NEW-PISTE (~55%). **Second wave revises to NEEDS-DEEPER (~10-15%)** after careful HTML extraction of Buyukboduk-Neamti hypothesis list.

Probability of formal Bloch-Kato Tamagawa contribution within Phase 3.G+ window: ~10-15%.

## Why REVISED

First wave claimed Buyukboduk-Neamti 2604.13854 was "PARTIAL FIT". Second wave's careful HTML reading found **explicit exclusions**:

### 5 compounding hypothesis violations (Buyukboduk-Neamti EXPLICITLY EXCLUDES our case)

| Hypothesis (B-N verbatim) | 4.5.b.a status |
|---|---|
| (p > 3) | p = 2 ✗ |
| (Disc) **K ≠ Q(√-1), Q(√-3)** "additional automorphisms require separate treatment" | **K = Q(i) EXPLICITLY EXCLUDED** ✗ |
| (Disc) disc(K/Q) odd | -4 even ✗ |
| (p split) (p) = 𝔭 𝔭^c in K | (2) = (1+i)² ramified ✗ |
| (Heeg) all primes dividing N split in K | 2 \| 4, 2 ramifies ✗ |
| (Level) ord_p(N_f) ≤ 1 | ord_2(4) = 2 ✗ |

### All other 2024-2025 TNC papers also BLOCKED

| Paper | p > 3 split | weight even | adjoint only | p ∤ N | applies? |
|---|---|---|---|---|---|
| Buyukboduk-Neamti 2026 | yes | no | no | yes | **NO** (5 violations) |
| Castella 2024 (PLMS) | yes | no | no | yes | **NO** (p=2 ramified) |
| BBL 2024 | yes (p≥5) | no | no | yes | **NO** (p=2) |
| Sano 2025 | yes (split) | yes | no | yes | **NO** (k=5 odd, p\|N) |
| Yin 2024 | weak (Eisenstein) | no | no | yes | **NO** (p=2 \| N) |
| Diamond-Flach-Guo 2025 | weak | no | YES (adjoint) | weak | **PARTIAL** (only adjoint Sym²f) |

Existing 2024-2025 TNC literature has **NO machinery** for the (p=2 ramified, k=5 odd, K=Q(i), N=4) regime of f = 4.5.b.a.

## Conjecture R-2.1 (stated, OPEN)

> Let M = M(f) be the Scholl 1990 motive of f = 4.5.b.a (rank-2 motivic weight w = 4). For each m ∈ {1,2,3,4}:
> 
> L^*(M(m), 0) / Ω^±_m(M) = (#H^1_f(Q, V_2(f)(m)) / #H^0(...)) × c_2(m) × c_∞(m) / Tam_unit(m)
> 
> where Ω^±_m is Deligne period, H^1_f is Bloch-Kato Selmer, c_2 local Tamagawa at p=2 ramified.
> 
> **Furthermore**, the Ω-independent ratio (M52 F2 v6 PARI 80-digit verified):
> 
> π · L(f, 1) / L(f, 2) = **6/5**
> 
> conjecturally factors as: (Ω^+_1/Ω^+_2) × (#H^1_f(M(1))/#H^1_f(M(2))) × (c_2(1)/c_2(2)) × (c_∞(1)/c_∞(2))
> 
> with "6" potentially from c_2 ratio + Selmer quotient, and "5" from corresponding factor.

**[TBD-R2-3 VERY HIGH OPEN]**: explicit factorization 6/5 = Selmer-quotient × Tamagawa-ratio × archimedean is the central novel content R-2 proposes.

## 5 [TBD: prove] markers (honest)

| Tag | Description | Difficulty |
|---|---|---|
| TBD-R2-1 | c_2(m) for ramified principal series at p=2 (Tate local epsilon factors) | HIGH |
| TBD-R2-2 | #H^1_f(Q, V_2(f)(m)) at m=1,2,3,4 (no Heegner, no Kolyvagin available) | HIGH |
| TBD-R2-3 | Factorize 6/5 = c_2(1)/c_2(2) × Selmer ratio × Γ ratio | **VERY HIGH** (R-2 central novel content) |
| TBD-R2-4 | Deligne periods Ω^±_m via Chowla-Selberg + lemniscate | MEDIUM (M52 verified) |
| TBD-R2-5 | Reduction to M57 + IMC at p=2 ramified | HIGH (blocked by M28 falsified) |

## What WOULD unblock the route (5-10 year programme)

1. **M57.A proved**: existence of L_2^±(f) (currently OPEN; Kriz/Fan-Wan collaboration)
2. **Anticyclotomic IMC at p=2 ramified**: currently FALSIFIED for all published frameworks (Hsieh, Chida-Hsieh, Arnold, Pollack-Weston). NEW framework needed.
3. **c_2(m) computed**: TBD-R2-1
4. **Selmer rank #H^1_f(M(m))**: TBD-R2-2

## Compatibility with prior modules

- **M27 (Hodge):** TRIVIAL via Pohlmann 1968 — verdict UNCHANGED. R-2 uses motivic cohomology beyond pure Hodge; consistent.
- **M31 (BSD subsumed):** weight-2-only verdict UNCHANGED. R-2 reopens higher-weight as STANDALONE conjecture (M31 originally framed as "subsumed by M13.1 paper-2"; R-2 upgrades to its own conjecture).
- **M39 (Beilinson regulator companion):** non-critical s = k = 5; R-2 at critical 1 ≤ m ≤ 4. DISJOINT.
- **M52 (Ω-independent 6/5):** SOURCE of R-2 leverage; the 6/5 must be derivable from BK identity.
- **M55 (4-layer uniqueness):** R-2 supplies a 5th layer (BK rationality) intrinsic to 4.5.b.a.
- **M57 (Adelic Katz):** OPEN existence of L_2^± is necessary first step. Together (M57 + R-2) form the IMC pair at p=2 ramified.

## 8 live-verified refs

1. **Bloch-Kato 1990** Grothendieck Festschrift Vol I, PiM 86, 333-400 — DOI 10.1007/978-0-8176-4574-8_9 (live-verified)
2. **Fontaine-Perrin-Riou 1994** PSPM 55 Part 1, 599-706
3. **Buyukboduk-Neamti 2026** arXiv:2604.13854 — HTML hypothesis list extracted, K ≠ Q(i) explicit
4. **Burungale-Buyukboduk-Lei 2024** arXiv:2310.06813 — p ≥ 5 explicit
5. **Castella 2024** arXiv:2407.11891 — PLMS 2025; p > 3 split
6. **Sano 2025** arXiv:2510.01601 — k = 2r even only
7. **Yin 2024** arXiv:2410.24193 — "good Eisenstein" excludes p \| N
8. **Diamond-Flach-Guo 2025** arXiv:2512.02348 — adjoint motive ONLY

## Files
- `SUMMARY.md` (this) — REVISED verdict NEEDS-DEEPER
- `conjecture_R2.md` (192 lines) — full Conjecture R-2.1 with Selmer/Tamagawa/period definitions
- `bdp_route.md` (138 lines) — 5 hypothesis violations + 5 companion paper non-applicability table

## Discipline
- 0 fabrications by R-2 (either wave)
- 1st wave OVER-OPTIMISTIC ("PARTIAL FIT" → 2nd wave corrected to BLOCKED)
- HTML verbatim hypothesis extraction (live-fetched 2026-05-06)
- Mistral STRICT-BAN observed
- 5 [TBD] markers honest, none hidden
- Honesty bar: BK is **Clay-ADJACENT** (HC subsumes BK in pure-Hodge per Deligne 1971), not Clay itself
- Sub-agent return-as-text used (3 files saved by parent)
- Hallu 87 → 87
