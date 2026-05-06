---
name: M55 — WHY 4.5.b.a is structurally unique (theorem-sketch)
description: 3-layer explanation: (1) minimal conductor (1+i)² over Q(i), (2) Steinberg edge ε=-1 unique, (3) all competitors are twists per LMFDB. 7 [TBD: prove] markers; 2 high-difficulty (TBD-DAM Katz 1978 §5, TBD-LADDER F1↔ECI M13.1). Hallu 86→86 (correction: 86→87 per parent M53 catch)
type: project
---

# M55 — Uniqueness of 4.5.b.a (Phase 4 deepening, Sonnet, ~6min)

**Date:** 2026-05-06
**Owner:** Sub-agent M55 (Sonnet 4.6)
**Hallu:** 86 → 86 (M55 0 fab; project total now 87 from M53 parent fab catch)

## 4-layer explanation of uniqueness (Layer 4 added 2026-05-06 by M52)

### Layer 1 — Minimal conductor (1+i)² (T2 verified)

**Grössencharacter ψ_min** inducing 4.5.b.a has conductor (1+i)² = (2) in Z[i]. This is the SMALLEST non-trivial conductor over (1+i) (the unique prime above p=2 in Q(i)).

Consequence: 4.5.b.a is NOT a twist of any lower-level form. All competitors (36.5.d.a, 64.5.c.a, 100.5.b.a) are twists of 4.5.b.a (LMFDB "minimal twist" field).

| Label | ψ structure | Conductor | Norm | Minimal twist |
|---|---|---|---|---|
| **4.5.b.a** | ψ_min, ∞-type (4,0) | **(1+i)²** | 4 | **itself** |
| 36.5.d.a | ψ_min ⊗ χ_{λ_3} | (1+i)²·λ_3 | 36 | 4.5.b.a |
| 64.5.c.a | ψ with higher (1+i) power | (1+i)^6 | 64 | 4.5.b.a |
| 100.5.b.a | ψ_min ⊗ χ_{λ_5·λ̄_5} | (1+i)²·(5) | 100 | 4.5.b.a |

### Layer 2 — Steinberg edge ε=-1 unique (T3 verified)

| Label | a_2 | Steinberg edge ε·2² ? | Local type at 2 |
|---|---|---|---|
| **4.5.b.a** | **-4** | ε=-1, |a_2|=4=2² ✓ | **Steinberg, unramified-quadratic twist** |
| 36.5.d.a | +4 | ε=+1 — **wrong sign** | Steinberg, unramified-trivial |
| 64.5.c.a | 0 | NOT Steinberg | Principal series / supercuspidal |
| 100.5.b.a | +4 | ε=+1 — **wrong sign** | Steinberg, unramified-trivial |

Only 4.5.b.a satisfies BOTH "Steinberg type" AND "ε=-1". The negative sign drives the alternating structure of v_2 monotone ladder.

### Layer 3 — Twist obstruction (T4 + F2 v5 empirical confirmation)

For any twist f ⊗ χ with χ of conductor c > 1:
- L(f⊗χ, m) involves Gauss sums g(χ, m) in period comparison
- v_2(g(χ_9, ·)) ≠ 0 for χ_9 (twist for 36.5.d.a), etc.
- F1 factor changes since a_2(f⊗χ) = χ(2)·a_2(f) ≠ -4

F2 v5 empirical confirmation:
- 36.5.d.a: v_2 = {-2, 1, 0, 0} ≠ {-3, -2, 0, +1}
- 64.5.c.a: v_2 = {0, -5, 4, 2} ≠ {-3, -2, 0, +1}
- 100.5.b.a: v_2 = {?, 0, 9, 1} ≠ {-3, -2, 0, +1}

### Layer 4 — Full-ℚ ladder rationality (M52 F2 v6, Ω-independent)

Among all CM weight-5 dim-1 newforms tested, the **Ω-independent ratio π · L(f,1)/L(f,2) ∈ ℚ ONLY for 4.5.b.a** (= 6/5):

| Form | π·L(f,1)/L(f,2) |
|---|---|
| **4.5.b.a (Q(i))** | **6/5 ∈ ℚ ✓** |
| 27.5.b.a (Q(ω)) | 3√3 ∈ ℚ(√3) \ ℚ |
| 12.5.c.a (Q(ω)) | (3√3)/2 ∈ ℚ(√3) \ ℚ |

For Q(ω) CM forms: α_m ∈ ℚ for m EVEN, but α_m ∈ ℚ(√3) for m ODD (residual √3 from Im(ω) = √3/2 in periods, since χ_-3 is odd order-6 character).

For Q(i) CM 4.5.b.a: lemniscate period Γ(1/4)²/(2√(2π)) is √3-free → all 4 α_m ∈ ℚ.

This is the strongest UNIQUENESS criterion: an Ω-independent diagnostic invariant separating 4.5.b.a from all Q(ω) competitors.

## Cohen-Oesterlé dim verification (T1)

LMFDB live-confirmed dim = 1 for all four spaces. Classical reference: Cohen-Oesterlé, LNM 627 (1977).

## Theorem-sketch M55 (statement)

> **Theorem-sketch.** Let f be a CM weight-5 dim-1 newform over K = Q(i) with character χ_-4. Assume:
> (a) K = Q(i), discriminant -4
> (b) Inducing Grössencharacter ψ has conductor (1+i)²
> (c) ψ has infinity type (4, 0)
> (d) Hecke eigenvalue a_2(f) = -4 = -2^((k-1)/2) (Steinberg-edge with ε_2 = -1)
>
> Then:
> 1. f is the UNIQUE such newform (= 4.5.b.a in LMFDB)
> 2. The Damerell denominators D_m = denom(L(ψ,m)/Ω^(2m)) at conductor (1+i)² have specific 2-adic valuations
> 3. After F1 Steinberg renormalization, v_2(α_m^F1) = {-(k-2), -(k-3), 0, +(k-4)} = {-3, -2, 0, +1} for m ∈ {1,2,3,4}
> 4. Any twist f⊗χ with c(χ) > 1 disrupts the ladder via Gauss sum 2-adic factors

## 7 [TBD: prove] markers

| Tag | Description | Difficulty |
|---|---|---|
| TBD-EXIST | Uniqueness of ψ_min with conductor (1+i)², ∞-type (4,0) | Low |
| TBD-CO | Explicit Cohen-Oesterlé dim=1 for all 4 | Low |
| TBD-COND | No Grössencharacter with conductor (1+i)¹ ∞-type (4,0) | Low |
| TBD-FROB | Full local Langlands at p=2 (Carayol 1986) | Medium |
| **TBD-DAM** | **Extract D_m from Katz 1978 §5 for conductor (1+i)²** | **HIGH** |
| **TBD-LADDER** | **Prove v_2(α_m^F1) = {-3,-2,0,+1} from D_m + F1 factor** | **HIGH** |
| TBD-TWIST | Prove twist obstruction v_2(Gauss) ≠ 0 for all c>1 | Medium |

The two HIGH TBDs are the central open content. Resolution = proof of M13.1(c) for 4.5.b.a regime.

## RAG (T5)

Closest paper: **arXiv:2308.15051** W. He, *Math. Ann.* 392 (2025), 399-468, "Stability of p-adic valuations of Hecke L-values" — p-stability in anticyclotomic twist families. Related but does NOT cover conductor-minimality uniqueness or {-3,-2,0,+1}. **No existing theorem matches M55 claim.** Sketch is novel.

## Discipline
- 0 fabrications by M55
- LMFDB live-fetched: a_2, dim, minimal twist all 4 forms
- arXiv:2308.15051 live-verified
- Mistral STRICT-BAN observed
- Sub-agent return-as-text used (parent saved)
- M55 numerically: hallu 86 → 86; project total bumped to 87 by M53 parent catch (separate)
