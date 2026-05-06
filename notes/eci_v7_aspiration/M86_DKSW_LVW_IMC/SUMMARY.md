---
name: M86 DKSW23 × LVW joint IMC at p=2 ramified Q(i) — REVISED 5-10% (down from 25-35%)
description: DKSW23 arXiv:2310.16399 categorical mismatch (totally real F required, K=Q(i) imaginary quadratic). LVW arXiv:2501.03673 explicit FAIL on 3 hypotheses (odd disc, p splits, integer ℓ). 5 GAPS open. R-2.1 needs 3rd framework. Recommend outreach Lei OR Castella. 80-word v7.6 §10 paragraph drafted. Hallu 91 → 91
type: project
---

# M86 — DKSW23 × LVW joint IMC framework (D4-#10)

**Date:** 2026-05-06 | **Hallu count:** 91 → 91 held | **Mistral STRICT-BAN observed**

## VERDICT: 5-10% (REVISED DOWN from M83 scan 25-35%)

After live verification of both papers (arXiv abstract + LVW HTML hypothesis extraction):

### DKSW23 = arXiv:2310.16399 (Dasgupta-Kakde-Silliman-Wang Oct 2023)

- "The Brumer-Stark Conjecture over Z" 56 pages
- Closes p=2 case via group-ring Hilbert Eisenstein + Ribet at p=2
- **REQUIRES F totally real** (Brumer 1967/Stark 1980/Tate 1984 setup)
- **CATEGORICAL MISMATCH**: K=Q(i) imaginary quadratic, no totally real F available

### LVW = arXiv:2501.03673 (Longo-Vigni-Wang Jan 2025)

- Generalized Rubin formula for Hecke characters
- Extends BDP (1,0) → (1+ℓ, -ℓ), ℓ ∈ ℕ_0 → covers k=2+2ℓ EVEN weights only
- Explicit hypotheses (Assumption 1.1 verbatim):
  - K imaginary quadratic ✓
  - **disc(K) odd** ✗ (Q(i) disc = -4, EVEN — FAIL)
  - **p splits in K** ✗ (p=2 ramifies in Q(i) as (1+i)² — FAIL)
  - **p ∤ D_K** ✗ (2 | 4 — FAIL)
  - **Infinity type (1+ℓ,-ℓ), ℓ ∈ ℤ** ✗ (k=5 → ℓ=3/2 ∉ ℤ — FAIL)
- LVW: NO IMC stated, only Selmer dim-1 + Rubin formula

## Hypothesis Compatibility Matrix

**DKSW23 at (p=2 ramified, k=5 odd, K=Q(i)):**

| Hypothesis | Our regime | Status |
|---|---|---|
| F totally real base | Q(i) imaginary quad | **FAIL — categorical** |
| K/F abelian CM extension | No F available | **FAIL** |
| p=2 handling | p=2 ramified | PASS — DKSW23 novelty |
| Brumer-Stark unit existence | Requires totally real F | **FAIL** |

**LVW at (p=2 ramified, k=5 odd, K=Q(i)):**

| Hypothesis | Our regime | Status |
|---|---|---|
| K imaginary quadratic | Q(i) ✓ | PASS |
| disc(K/Q) odd | D = 4, even | **FAIL — explicit** |
| p splits in K | p=2 ramifies | **FAIL — explicit** |
| p ∤ D_K | 2 \| 4 | **FAIL — explicit** |
| ∞-type (1+ℓ,-ℓ), ℓ ∈ ℤ | k=5 → ℓ=3/2 ∉ ℤ | **FAIL** |
| Sign(FE) = -1 | root number f = +1 | **TENSION** |
| Heegner hypothesis on N | N=4, 2 ramifies | **FAIL** |

The hypotheses are **NOT joint-compatible**. LVW fails 5/7 conditions for K=Q(i). DKSW23 fails categorically.

**Key insight on the categorical split:** DKSW23 = totally real F + CM extension K/F (Brumer-Stark setup); LVW = imaginary quadratic K + split p (BDP setup). Our regime (K=Q(i), p=2 ramified) falls in a **third category** not covered by either.

## 5 GAPS (genuine open problems)

| Gap | Content | Blocker |
|---|---|---|
| 1 | Imag-quadratic Brumer-Stark analog at p=2 ramified | No published framework |
| 2 | LVW extended to even disc K=Q(i) | BDP requires split p; ramified needs different geometric setup |
| 3 | LVW extended to odd weight k=5 | ℓ=3/2 non-integer → p-adic interpolation in weight space |
| 4 | L_2^{anti-cyc}(f, T) construction | M57 OPEN, Fan-Wan/Kriz stalled at Hodge filtration p=2 |
| 5 | Sel_2^{anti-cyc}(K, T_f) structure | No Kolyvagin/Euler system at p=2 ramified for CM |

All 5 are genuine OPEN problems, not minor technicalities. Gap 1 alone = substantial research programme.

## Next Concrete Step

**Option A (recommended, 2 weeks):** Email Antonio Lei (Ottawa) OR Francesc Castella (UCSB). Both work on BDP-type at non-split primes. Direct ask: "Has BDP/Rubin formula been extended to p ramified in K? For K=Q(i) specifically?" Cost: 1 email; ~30% chance of useful pointer.

**Option B (3-6 mo):** Self-study Castella-Wan (if exists) + Pollack-Weston "On anticyclotomic μ-invariants of modular forms" — check if "ramified" cases include Q(i).

**Option C (inadvisable now):** Approach DKSW23 authors — they work totally real side, unlikely to comment on imag-quad extension.

## Discipline log

- 0 fabrications
- arXiv abstracts WebFetch-verified for both papers
- LVW HTML hypothesis extraction successful (Assumption 1.1 verbatim)
- M83's 25-35% revised DOWN to 5-10% AFTER reading actual hypotheses
- Mistral STRICT-BAN observed
- Hallu 91 → 91
