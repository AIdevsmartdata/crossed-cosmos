---
name: M123 BMF investigation — (B) BMF correspondence structural BUT non-cuspidal Eisenstein splitting + NEW Malkin 2010.07238 bridge
description: NO cuspidal BMF G in LMFDB ↔ f=4.5.b.a (theorem not gap: BC(f)/Q(i) = ψ_4 ⊕ ψ_4^c non-cuspidal Eisenstein since f has CM by Q(i) with char = quadratic Q(i)/Q char). Palacios 2023 + Barrera Salazar-Palacios 2024 study non-cuspidal object. NEW BRIDGE: Malkin arXiv:2010.07238 motivic fundamental groups CM elliptic curves + Bianchi 3-folds = geometric realization lemniscate-Damerell at Bianchi level. M108 Galois descent SUPPORTED: BC(f) exact splitting no cuspidal residue
type: project
---

# M123 — BMF Investigation: ψ_4 ↔ Bianchi modular form?

**Date:** 2026-05-06 | **Hallu 97 → 97** held (M123 0 fabs) | **Mistral STRICT-BAN**

## VERDICT: (B) Structural correspondence non-cuspidal + NEW geometric bridge

- **(B1)** No cuspidal BMF G on PSL(2, Z[i])\H³ has L(G, s) = L(f = 4.5.b.a, s). **THEOREM**, not gap (character obstruction)
- **(B2)** Non-cuspidal BC(f)/Q(i) exists, studied (Palacios 2023, Barrera Salazar-Palacios 2024). p-adic L = product 2 Katz functions
- **(B3)** **NEW BRIDGE**: Malkin arXiv:2010.07238 connects motivic fundamental groups of CM elliptic curves to Bianchi 3-folds Γ_1(p)\H³. Lemniscate CM periods = Hodge correlator integrals
- **(B4)** LMFDB weight-2 only for BMFs ; ψ_4 GL_1 admits no cuspidal GL_2/Q(i) lift
- **(B5)** **M108 Galois descent SUPPORTED**: BC(f) = ψ_4 ⊕ ψ_4^c exact splitting NO cuspidal residue

## Core obstruction theorem

f = 4.5.b.a has CM by Q(i) with character χ_4 = quadratic character of Q(i)/Q.

**Theorem (Palacios 2023)**: When f is a CM form whose character is that of K/Q extension, BC_{K/Q}(Π(f)) splits as ψ_4 ⊕ ψ_4^c (Eisenstein, non-cuspidal).

For f = 4.5.b.a / Q(i) :
- ψ_4 has ∞-type (4, 0)
- ψ_4^c = ψ_4^{Galois conjugate} has ∞-type (0, 4)
- L(BC(f), s) = L(ψ_4, s) · L(ψ_4^c, s) = L(f, s)
- **Irreducibility fails → BC non-cuspidal Eisenstein**

## NEW bridge for ECI: Malkin arXiv:2010.07238

**Verbatim abstract** : "we describe a connection between realizations of the action of the motivic Galois group on the motivic fundamental groups of Gaussian and Eisenstein elliptic curves punctured at the p-torsion points, π_1^Mot(E-E[p], v_0), and the geometry of the Bianchi hyperbolic threefolds Γ_1(p)\H^3"

Key results :
- **Homomorphism** from cohomology complex of local system on Γ_1(p)\H³ to **depth-2 graded quotient** of motivic fundamental group's Lie algebra
- Generalizes Goncharov (math/0510310) projective-line cyclotomic
- **Hodge correlators** generate canonical real periods (= CM periods of lemniscate)
- Double shuffle relations on Hodge correlator integrals deforming depth-2

**For ECI**: This is the **geometric realization of lemniscate-Damerell structure at Bianchi level**. Gaussian elliptic curve = lemniscate E : y² = x³ - x (CM by Z[i]) ; Bianchi 3-fold Γ_1(p)\H³ captures motivic depth filtration. CM periods (Ω_K^{2k} for ψ_4) appear as Hodge correlator integrals.

## Damerell + ECI confirmation

L(ψ_4, 4) / Ω_K^8 ∈ Q̄ confirmed (Damerell ; Hida UCLA notes ; Bannai-Kobayashi).

For ψ_4 (k=4 in Damerell ∞-type notation) : algebraic normalization used in M52.

Malkin 2010.07238 framework provides geometric home : period integrals (Hodge correlators on Γ_1(p)\H³) = algebraic-over-Ω_K ratios controlled by Damerell.

ECI M52 Ω-independent 6/5 invariant compatible (specific 6/5 value requires further CM period computation beyond M123 scope).

## M108 Galois descent SUPPORTED

BC(f) / Q(i) = ψ_4 ⊕ ψ_4^c is **exact Galois orbit** under Gal(Q(i)/Q) = {1, σ}.
- σ acts ψ_4^σ = ψ_4^c (swaps ∞-type (4,0) ↔ (0,4))
- Non-cuspidality guarantees **exact splitting** — no higher-order obstruction, no cuspidal residue
- **NEW finding**: exactness of Galois splitting at Bianchi level supports M108 Galois descent argument. 2-dim representation Π(f) on GL_2/Q descends from GL_1/Q(i) without cuspidal correction terms.

## Brown-Fonseca M_{1,3}^{Γ_1(4)} and Malkin

No published "Brown-Fonseca M_{1,3} → BMF Γ_1(4)" functorial map found. Closest analog :
- Hain-Matsumoto arXiv:1512.03975 : universal mixed elliptic motives over M_{1,1}, extensions over Q/Z not Z[i]
- **Malkin arXiv:2010.07238**: correct framework for M_{1,3}^{Γ_1(p)} over Z[i]. Bianchi 3-fold Γ_1(p)\H³ + punctured CM elliptic curve plays role of M_{1,3}
- Functorial map BMF on Γ_1(4) ⊂ SL_2(O_K) ↔ M_{1,3}^{Γ_1(4)} **not established** in literature ; Malkin depth-2 partial

**M_{1,3}^{Γ_1(4)} question from M113 remains conditional/speculative.**

## 10 verified references (live)

1. Malkin arXiv:2010.07238 (2020) ✓ verbatim
2. Palacios arXiv:2302.13758 (2023) ✓ Theorem 1.2/1.3
3. Barrera Salazar-Palacios arXiv:2412.18045 (Dec 2024) ✓
4. Boxer-Calegari-Gee-Newton-Thorne arXiv:2309.15880 (2023) ✓
5. Rahm-Tsaknias arXiv:1703.07663 JTNB 31(1) 2019 ✓
6. Anderson et al. arXiv:2509.17256 Canad. Math. Bull. 69(1) 2026 (parallel weight only) ✓
7. Goncharov arXiv:math/0510310 ✓
8. Rahm-Sengun arXiv:1104.5303 (2011) ✓
9. Cremona-Thalagoda-Yasaki arXiv:2502.00141 (2025, weight 2 only) ✓
10. LMFDB BMF base-change knowledge article ✓

## Discipline log

- Hallu 97 → 97 held (M123 0 fabs)
- 10 references live-verified WebFetch
- BMF correspondence theorem derived from cited Palacios 2023
- Malkin 2010.07238 NEW bridge identified
- Mistral STRICT-BAN observed

## Action items

1. **Add Malkin 2010.07238 to R-6 paper bibliography** (NEW reference for lemniscate-Damerell × Bianchi connection)
2. **Update memory** : note BC(f)/Q(i) exact non-cuspidal splitting supports M108
3. **Future**: investigate if Malkin's depth-2 framework gives motivic interpretation of M52 6/5 ratio
