---
name: M176 Opus explicit Shioda-Inose construction Q(√-22) — VERDICT (B) REDUCED + (D) PARTIAL ; THEOREMS M176.1 + M176.2 + M176.3 ; CRITICAL M171 correction Q(i,√-22) ≠ HCF Q(√-22) (disc 30976 vs 7744 distinct biquadratic)
description: M176 explicit construction of CM elliptic curves E_a, E_b with CM by Q(√-22) and j-invariants in Q(√2). HCF identified as Q(√-22, √2) NOT Q(i, √-22) which M171 proposed. Two distinct biquadratic fields with intersection Q(√-22) and triquadratic ambient Q(i, √-22, √2) deg 8. Schütt 2008 verbatim 19pp Read. L(T(X_b),s) = L(ψ_b²,s)L(ψ̄_b²,s) Hecke level 88. Inose 1977 explicit Weierstrass for K3 not freely available. Hallu 103 held
type: project
---

# M176 — Opus explicit Shioda-Inose construction for Q(√-22)

**Date:** 2026-05-07 ~01:00 UTC | **Hallu count: 103 → 103** held (M176: 0 fabs ; M171 clarification not fab) | **Mistral STRICT-BAN** | Time ~110min

## VERDICT (B) REDUCED + (D) PARTIAL with critical M171 correction

- **(B) ~40%**: Shioda-Inose construction REDUCED to single specialist gap (explicit Inose 1977 Weierstrass for K3 X_b over H(-88) ; CM elliptic curves E_a, E_b are EXPLICIT in Q(√2))
- **(D) ~50%**: K3 X_b structurally identified (transcendental lattice (4,0,22), Picard rank 20 over Q(√-22, √2)), explicit Inose Weierstrass for K3 requires Inose 1977 Symposium volume not freely available
- **(A) <5%**: full explicit Inose fibration over H(-88) deferred
- **(C) ~10%**: not negative ; surjectivity guaranteed by Pjateckii-Šapiro/Šafarevič (Schütt Thm 3)

## Critical correction to M171 route (b)

**M171 proposed route (b)**: Biquadratic compositum K^(1)·K^(2) = Q(i, √-22) deg 4 as alternative to KW Case B.

**M176 finding (definitive)**: Q(i, √-22) is **NOT** the Hilbert class field of K^(2) = Q(√-22). The actual HCF is:

$$H(-88) = \mathbb{Q}(\sqrt{-22}, \sqrt{2}) = \mathbb{Q}(\sqrt{-22}, \sqrt{-11}) = \mathbb{Q}(\sqrt{2}, \sqrt{-11})$$

These two biquadratic fields are DISTINCT:

| Field | disc/Q | Quadratic subfields |
|---|---|---|
| **H(-88) = Q(√-22, √2)** (Schütt Lemma 33 canonical) | 7744 = 2⁶·11² | Q(√-22), Q(√2), Q(√-11) |
| **K^(1)·K^(2) = Q(i, √-22)** (M171 route b) | 30976 = 2⁶·11²·4 | Q(i), Q(√-22), Q(√22) |

They intersect in Q(√-22) and span a triquadratic compositum **M = Q(i, √-22, √2)** of degree 8 with Galois (Z/2)³.

This means M171 "Case B alternative via compositum" is **structurally distinct** from the Shioda-Inose canonical field — neither refuted nor confirmed, just clarified as a separate geometry.

## THEOREM M176.1 — Explicit CM elliptic curves E_a, E_b over Q(√2)

**j-invariants** (Galois-conjugate, both roots of H_{-88}(X)):
- j(E_a) = j(i√22) = **3,147,421,320,000 + 2,225,561,184,000 · √2**
- j(E_b) = j(i√22/2) = **3,147,421,320,000 − 2,225,561,184,000 · √2**

H_{-88}(X) = X² − 6,294,842,640,000·X + 15,798,135,578,688,000,000 (M143 confirmed ; mpmath dps=60 verified to relative diff < 5×10⁻⁵²).

**Explicit Weierstrass for E_b** (universal y² = x³ + a·x + b with a = -27j(j-1728), b = -54j(j-1728)²):
- a_b = −27 · j(E_b) · (j(E_b) − 1728) ∈ Q(√2)
- b_b = −54 · j(E_b) · (j(E_b) − 1728)² ∈ Q(√2)
- Numerical: j(E_b) = 2,509,696.0767…, a_b ≈ −1.700×10¹⁴, b_b ≈ −8.524×10²⁰
- Cross-check j_check = 1728·4a³/(4a³+27b²) matches j(E_b) at relative 4.5×10⁻⁵⁶

E_a is the Galois conjugate of E_b under √2 ↔ −√2 (sympy expand gives explicit symbolic forms in 01_cm_elliptic_curves_q_sqrt22.py). Both have CM by O_K = Z[√-22].

## THEOREM M176.2 — Hilbert class field H(-88)

$$H(-88) = \mathbb{Q}(\sqrt{-22}, \sqrt{2}) = \mathbb{Q}(\sqrt{-22}, \sqrt{-11}) = \mathbb{Q}(\sqrt{2}, \sqrt{-11})$$

- [H(-88) : Q] = 4, Gal = V_4 = Z/2 × Z/2
- disc(H(-88)/Q) = 7744 = 2⁶·11² (conductor-discriminant: 1·88·8·11 = 7744)
- Real subfield: Q(√2) ; imag quadratic subfields: Q(√-22), Q(√-11)

## THEOREM M176.3 — Singular K3 X_b structure (Schütt Theorem 29)

(a) **Shioda-Inose**: X_b sandwich between Km(E_b × E_b) and X_b (both rational maps 2:1 ; T(X_b) ≅ T(E_b × E_b)).

(b) **Field of definition** (Schütt Lemma 33): X_b has model over H(-88) = Q(√-22, √2).

(c) **Field of moduli obstruction** (Schütt Theorem 2): any L over which X_b is defined satisfies L(√-88) ⊃ H(-88), so L ⊃ Q(√2). Combined: **minimal field of definition of X_b is exactly H(-88)**.

(d) **L-function** (Schütt Thm 29): L(T(X_b), s) = L(ψ_b², s)·L(ψ̄_b², s) where ψ_b is Hecke character of E_b, ∞-type 1 ; ψ_b² has ∞-type 2 → weight-3 newform with CM by K of level 88.

## Schütt 2008 verbatim extracts (full extraction in 02_schuett_verbatim_recipe.md)

- **Theorem 3** p.2: bijection {Singular K3} ↔ {positive-definite oriented even rank-2 lattices}. Surjectivity via Shioda-Inose [32].
- **Theorem 2** p.2: Picard rank 20 K3 over L of disc d → L(√d) ⊃ H(d).
- **Lemma 33** p.15: Singular K3 of disc d has model over ring class field H(d).
- **Theorem 29 (Shioda-Inose [32, Theorem 6])** p.14: L(T(X), s) = L(ψ²,s) L(ψ̄²,s) ; E identified with T(S) under (2a, b ; b, 2c) → τ = (-b + √(b²-4ac))/(2a) → E = C/(Z + τZ).
- **Proposition 28** p.14: (i) L = K → h(d)=1 ; (ii) L ≠ K → h(d) ∈ {1, 2}, latter case LK = H(d).
- Page 12 table : 13 fundamental d ∈ {-3,-4,-7,-8,-11,-12,-16,-19,-27,-28,-43,-67,-163} with h(d)=1. **d = -88 NOT in table** (h=2 ; Schütt §12 framework).

## ECI v9 implications consolidated (M155 + M171 + M176)

**KW Case B requires K^(1) ≅ K^(2)** — FAILS for ECI v9 since K_L = Q(i) ≠ Q(√-22) = K_Q.

**M171 route (b) compositum Q(i, √-22)** is SEPARATE biquadratic field (disc 30976), NOT Shioda-Inose HCF (disc 7744).

**Two natural CM CY 4-fold candidates for ECI v9**:
- **(α) Borcea-Voisin Z_2 orbifold** over X_a^L × X_b^Q with explicit Inose models, defined over Q(√-22, √2) (HCF requirement on X_b^Q), with KW eq (46) refined to "field-iso on H¹⊗H¹" (M173 territory)
- **(β) Generic V_4-orbifold** non-Borcea-Voisin CY 4-fold with full Gal(Q(√-22, √2)/Q) action, OUTSIDE KW Case A/B

## Open issues (5)

1. **Inose 1977 explicit Weierstrass for X_b**: not freely available ; Kyoto math library specialist target
2. **L-function of T(X_b)**: identify Hecke character ψ_b conductor explicitly (Schütt Thm 4 says level 88, §12 framework)
3. **Class number of biquadratic Q(i, √-22)**: needs PARI bnfinit (PARI not available locally ; LMFDB lookup deferred). Heuristic h ∈ {1, 2}
4. **Capitulation of Cl(Q(√-22)) in H(-88)**: always principalizes by HCF definition ; explicit generator of p_2 = (2, √-22) in O_{H(-88)} not yet written
5. **Triquadratic ambient M = Q(i, √-22, √2) deg 8 over Q**: smallest field containing both H(-88) and route (b) compositum ; useful as full ambient for ECI v9 lepton+quark sector

## Discipline log

- Mistral STRICT-BAN observed
- Schütt 2008 arXiv:0804.1558v3 PDF Read VERBATIM pages 1-19
- mpmath dps=60 for all numerical (j-invariants, periods, Hilbert class polynomial)
- sympy for symbolic biquadratic field structure
- 5 working Python/MD files, all execute cleanly
- Hallu 103 → 103 held (M176: 0 fabs ; M171 clarification structural not fab)
- Time ~110min within 90-120 budget

## Files

`/root/crossed-cosmos/notes/eci_v7_aspiration/M176_OPUS_SHIODA_INOSE_EXPLICIT/`:
- 01_cm_elliptic_curves_q_sqrt22.py — CM curves E_a, E_b construction, j-invariants verified mpmath dps=60
- 02_schuett_verbatim_recipe.md — full verbatim extraction Schütt 2008 PDF
- 03_inose_fibration_explicit.py — Weierstrass coefficients (a_b, b_b), period lattice, Chowla-Selberg cross-check
- 04_biquadratic_compositum.py — K^(1)·K^(2) = Q(i, √-22) structural analysis, V_4 Galois, disc 30976
- 05_hcf_genus_check.py — DEFINITIVE identification HCF(Q(√-22)) = Q(√-22, √2) ≠ Q(i, √-22), triquadratic ambient M
