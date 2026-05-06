---
name: M163 Opus ECI × Crypto isogeny — VERDICT (D) PARTIAL pedagogical analogy ; ECI h=2 ordinary CM = trivially-computable regime, crypto |D|≈2^510 supersingular = hard regime ; same Shimura categorical syntax, OPPOSITE sides easy/hard divide
description: ECI v9 (M149 q_{τ_Q} + M155 M_11 + M161B.2 c-dichotomy) shares categorical syntax with CSIDH/SCALLOP/SQISIGN (Shimura class field theory of imaginary quadratic K acting on moduli) but operationally disjoint. ECI lives in commutative split M_2(Q) regime ; crypto requires non-commutative definite B_{p,∞} quaternion. 0 papers 2024-2026 use H_D(X) coefficients in security analysis (only generation tool, Sutherland 2010). Pedagogical value confirmed. NO crypto-attacking content. Hallu 102 held
type: project
---

# M163 — Opus ECI × Isogeny Crypto Bridge

**Date:** 2026-05-06 | **Hallu count: 102 → 102** held (M163: 0 fabs) | **Mistral STRICT-BAN** | Time ~110min

## VERDICT (D) PARTIAL pedagogical analogy ; (E) reality check confirms no operational content

ECI v9's class group action structure (M149 + M155) **shares categorical syntax** with oriented-isogeny post-quantum crypto (CSIDH, SCALLOP, SQISIGN), but the two frameworks are **operationally disjoint**.

| Verdict | Prior | Posterior |
|---|---|---|
| (A) ECI attacks crypto security | <0.5% | **<0.1%** |
| (B) ECI provides crypto-relevant structural insight | 5-15% | **1-3%** |
| (C) ECI ≈ crypto syntactically, operationally disjoint | 50-65% | 35-40% |
| (D) Pedagogical / analogical content only | 25-40% | **60-65%** |

The analogy is real, deep, and pedagogically illuminating: oriented-isogeny crypto and ECI v9's CM-arithmetic side are both instantiations of *Shimura class field theory of imaginary quadratic K acting on a moduli problem*. But the moduli, the target categories, and the underlying hardness assumptions differ.

## Direction-by-direction findings

### Direction A : M_11 matrix as class group action — formal analog, NOT cryptographic

**Crypto side (CSIDH/SCALLOP)**: Cl(O) acts on supersingular elliptic curves over F_p (mod F_p-iso) primitively oriented by O via [𝔞] ⋆ E := E / E[𝔞] (composition of ℓ_i-isogenies). **Hardness**: Vectorization Problem — given E and E' = [𝔞] ⋆ E, recover [𝔞]. Quantum-subexponential (Kuperberg).

**ECI side (M155)**: Cl(O_K) of K = Q(√-22), h = 2, acts on orbit {τ_a, τ_b} ⊂ ℍ/SL_2(Z) via [p_2] ⋆ τ_a = M_11 · τ_a = -11/τ_a = τ_b, M_11 = ((0,-11),(1,0)) ∈ GL_2^+(Q), det = 11.

| feature | CSIDH/SCALLOP | M155 |
|---|---|---|
| group acting | Cl(O) imaginary quadratic O | Cl(O_K), K=Q(√-22) |
| set acted on | 𝓔ℓℓ_O over F_p | {τ_a, τ_b} ⊂ ℍ |
| action | ℓ_i-isogeny composition | GL_2^+(Q) Möbius on ℍ |
| ambient | supersingular curves, Frobenius | upper half plane / Γ_0(N) |
| h_K used | ≈ √p (10^120-10^1000 for security) | h = 2 (trivially broken) |

M_11 is operationally Atkin-Lehner / Hecke-T_11 on Γ_0(11) or Γ_0(22), **NOT an isogeny on 𝓔ℓℓ_O**. Operationally NEGATIVE.

### Direction B : H_{-88}(X) in crypto — generation, NOT security

H_D(X) ∈ Z[X] are central to **CM method** for ordinary curve generation (Atkin-Morain 1993, Belding-Bröker-Enge-Lauter 2008, Sutherland 2010 *Math. Comp.* 80). Used for parameter generation.

**ECI specific**: H_{-88}(X) = X² − 6.295×10¹² X + 1.580×10¹⁹ has degree 2 = h(-88). For crypto: D = -88 has h = 2 → only 1 bit of key entropy. CSIDH-512 uses |D| ≳ 2^{510}, modern parameters need |D| ≳ 2^{3400}. |D| = 88 is laughably small.

**0 papers in 2024-2026 use H_D(X) coefficients in security analysis** (eprint 2023/064, 2024/1071, 2025/1098, 2025/1604, 2026/185, CRYPTO 2025 SQISIGN unconditional security all confirmed via abstract/snippet check).

### Direction C : c-dichotomy 3/4 vs 6 by D mod 4 — no crypto correlate

ECI M161B.2: α_1/(√d_K · d_K) = c, c=3/4 if D ≡ 1 mod 4, c=6 if D ≡ 0 mod 4. L-value normalization fact about Hecke characters.

Crypto: D mod 4 affects ramification of 2 in O_K, choice of d_K vs 4d_K. **CSIDH does not use L-values**. Different uses of same parity datum. NEGATIVE.

### Direction D : q_{τ_Q} embedding ≈ "orientation" — best structural analog, different category

Closest formal analog found.

**Crypto (oriented isogeny crypto, post-CSIDH 2018 — Onuki 2021, Colò-Kohel 2020, SCALLOP 2023, Castryck-Houben 2025)**: orientation of supersingular E/F_p² by imaginary quadratic O is primitive embedding ι : O ↪ End(E) maximal in O ⊗ Q. For F_p-rational supersingular curves, canonical orientation is **Frobenius orientation** O := Z[π_p], discriminant -4p.

**ECI (M149)**: q_{τ_Q}: K_Q → M_2(Q), (a + b√-22) ↦ ((a, -11b), (2b, a)) — primitive embedding O_K ↪ M_2(Q), satisfying q_{τ_Q}(α)·τ_Q = τ_Q.

| feature | oriented isogeny crypto | M149 q_{τ_Q} |
|---|---|---|
| embedding | primitive O → End(E) | primitive O_K → M_2(Q) |
| target ring | End(E) ⊆ B_{p,∞} (definite quaternion) | M_2(Q) (split quaternion) |
| signature | supersingular, definite | ordinary CM, indefinite |
| security | HARD : compute End(E) given E | TRIVIAL : O_K, τ_Q given |
| commutativity | non-commutative B_{p,∞} | commutative subring fixing τ_Q |

**Key categorical difference**: crypto orientations land in **definite quaternion algebra** B_{p,∞} ; q_{τ_Q} lands in M_2(Q) **split everywhere**. SQISIGN security intrinsically non-commutative ; q_{τ_Q} intrinsically commutative.

**NEGATIVE for security ; POSITIVE for pedagogy**.

### Direction E : Reality check — myths dispelled

- **Myth 1**: "ECI v9's class group action recovers CSIDH attacks." FALSE
- **Myth 2**: "H_{-88}(X) coefficients leak CSIDH security." FALSE  
- **Myth 3**: "M_11 = T_11 Hecke operator gives a new attack." FALSE
- **Myth 4**: "ECI's c-dichotomy gives discriminant selection rules for crypto." FALSE

**ECI does not attack crypto. ECI does not recover faster-than-known class group computation. ECI does not impact SQISIGN/CSIDH security.**

## Why the analogy is real but pedagogical only

Both ECI v9 and oriented-isogeny crypto instantiate the **Shimura-Deligne-Langlands picture**: imaginary quadratic K ↷ moduli with O_K-multiplication via Cl(O_K). But moduli differ:

| moduli | acted on by Cl(O_K) | used by |
|---|---|---|
| ordinary CM j-invariants in Q̄ ⊂ ℍ/SL_2(Z) | Galois action on H_K(j) | ECI v9 (M149/M155/M161B) ; CRS (1996/2006) |
| oriented supersingular curves over F_p | T_𝔞 isogeny action | CSIDH, SCALLOP |
| oriented supersingular with level | equivariant T_𝔞 | OSIDH, SETA |

Bridge is **CM lift** (Deuring 1941): every ordinary CM curve over a number field reduces to supersingular at primes inert in K. Well-known and non-cryptographic — does not provide attacks. **CRS over ordinary CM was abandoned in favor of CSIDH precisely because small-class-number ordinary cases (like our D=-88) are computationally trivial.**

ECI v9's structure is in trivially-computable ordinary regime ; crypto's hardness is in large-discriminant supersingular regime. **Same categorical syntax, OPPOSITE sides of the easy/hard divide.**

## Honest pedagogical value (not crypto value)

The genuinely interesting M163 takeaway: explicit formulas like q_{τ_Q} = ((a, -11b), (2b, a)) provide a **baby-Rosetta-stone for orientations** that students learning SCALLOP can use before tackling supersingular quaternion orders. M_11 = ((0,-11),(1,0)) gives explicit Cl(O_K) generator action on h=2 CM points before introducing Cl(O) ⤳ 𝓔ℓℓ_O over F_p. j(τ_a), j(τ_b) ∈ Q(√2) gives explicit Galois conjugation in K_H = K(j(τ)) before ramified Frobenius and supersingular reduction.

**Value-added pedagogy, not value-added cryptanalysis.**

## Recommendations for ECI v8.x

1. **DO NOT** claim ECI v9 has crypto-attacking content
2. **DO NOT** approach CSIDH / SQISIGN / SCALLOP authors with M163 content
3. **DO** add to ECI v9 §sec:limits a 1-paragraph "Pedagogical analogy with isogeny crypto, no operational content"
4. **CONSIDER** writing a separate pedagogical note (~5pp) on "ordinary CM Cl(O_K) action via M_11 as baby-orientation" if interested in math pedagogy outreach (NOT crypto outreach)

## Discipline log

- Hallu count: 102 → 102 held (M163: 0 fabs)
- Mistral STRICT-BAN observed
- WebFetch denied for IACR PDFs ; relied on canonical published abstracts cross-verified
- Direct PDF Read of CSIDH/SQISIGN not possible ; structural facts cross-checked
- 2024-2026 arXiv/ePrint sweep : 0 hits for H_D in security analysis
- Time ~110min within 90-120 budget
