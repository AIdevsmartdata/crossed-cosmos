# H3.B — S'_4 Clebsch-Gordan Tables

## Source

Novichkov, Penedo, Petcov (NPP20), "Double Cover of Modular S_4 for Flavour
Model Building", arXiv:2006.03058, Nucl. Phys. B 963, 115301 (2021).

All tables below are TRANSCRIBED from the TeX source at:
  `/tmp/agents_v647_evening/H3/npp20_src/S4prime.tex`
Appendix C (Tensor Products and Clebsch-Gordan Coefficients), lines 2276-2570.

**Notation**: α_i = components of left multiplet, β_i = components of right multiplet.

---

## Table 1: Products involving 1-dimensional irreps (NPP20 Tab. tab:1r, lines 2283-2354)

### Singlet × singlet → singlet

| Left ⊗ Right | Result | CG coefficient |
|---|---|---|
| 1' ⊗ 1' | 1 | α₁β₁ |
| 1' ⊗ 1̂ | 1̂' | α₁β₁ |
| 1' ⊗ 1̂' | 1̂ | α₁β₁ |
| 1̂ ⊗ 1̂ | 1' | α₁β₁ |
| 1̂ ⊗ 1̂' | 1 | α₁β₁ |
| 1̂' ⊗ 1̂' | 1' | α₁β₁ |

### Singlet × doublet → doublet

| Product | Result | CG coefficient (2-vector) |
|---|---|---|
| 1' ⊗ 2 | 2 | α₁(β₂, -β₁)ᵀ |
| 1̂' ⊗ 2 | 2̂ | α₁(β₂, -β₁)ᵀ |
| 1' ⊗ 2̂ | 2̂ | α₁(β₂, -β₁)ᵀ |
| 1̂ ⊗ 2̂ | 2 | α₁(β₂, -β₁)ᵀ |
| 1̂ ⊗ 2 | 2̂ | α₁(β₁, β₂)ᵀ |
| 1̂' ⊗ 2̂ | 2 | α₁(β₁, β₂)ᵀ |

### Singlet × triplet → triplet

| Product | Result | CG coefficient (3-vector) |
|---|---|---|
| 1' ⊗ 3 | 3' | α₁(β₁, β₂, β₃)ᵀ |
| 1̂ ⊗ 3 | 3̂ | α₁(β₁, β₂, β₃)ᵀ |
| 1̂' ⊗ 3 | 3̂' | α₁(β₁, β₂, β₃)ᵀ |
| 1' ⊗ 3' | 3 | α₁(β₁, β₂, β₃)ᵀ |
| 1̂ ⊗ 3' | 3̂' | α₁(β₁, β₂, β₃)ᵀ |
| 1̂' ⊗ 3' | 3̂ | α₁(β₁, β₂, β₃)ᵀ |
| 1' ⊗ 3̂ | 3̂' | α₁(β₁, β₂, β₃)ᵀ |
| 1̂ ⊗ 3̂ | 3' | α₁(β₁, β₂, β₃)ᵀ |
| 1̂' ⊗ 3̂ | 3 | α₁(β₁, β₂, β₃)ᵀ |
| 1' ⊗ 3̂' | 3̂ | α₁(β₁, β₂, β₃)ᵀ |
| 1̂ ⊗ 3̂' | 3 | α₁(β₁, β₂, β₃)ᵀ |
| 1̂' ⊗ 3̂' | 3' | α₁(β₁, β₂, β₃)ᵀ |

**Note**: All singlet-triplet products give trivial CG (just rescale by α₁).

---

## Table 2: Products of two 2-dimensional irreps (NPP20 Tab. tab:22, lines 2357-2406)

### 2 ⊗ 2 = 1 ⊕ 1' ⊕ 2

CG coefficients:
- **1** component: (1/√2)(α₁β₁ + α₂β₂)
- **1'** component: (1/√2)(α₁β₂ - α₂β₁)
- **2** component: (1/√2)[(α₂β₂ - α₁β₁), (α₁β₂ + α₂β₁)]ᵀ

### 2 ⊗ 2̂ = 1̂ ⊕ 1̂' ⊕ 2̂

CG coefficients:
- **1̂** component: (1/√2)(α₁β₁ + α₂β₂)
- **1̂'** component: (1/√2)(α₁β₂ - α₂β₁)
- **2̂** component: (1/√2)[(α₂β₂ - α₁β₁), (α₁β₂ + α₂β₁)]ᵀ

### 2̂ ⊗ 2̂ = 1 ⊕ 1' ⊕ 2

CG coefficients:
- **1** component: (1/√2)(α₁β₂ - α₂β₁)
- **1'** component: (1/√2)(α₁β₁ + α₂β₂)
- **2** component: (1/√2)[(α₁β₂ + α₂β₁), (α₁β₁ - α₂β₂)]ᵀ

**Note**: Order matters — left/right columns must be matched consistently.

---

## Table 3: Products of 2-dim and 3-dim irreps (NPP20 Tab. tab:23, lines 2410-2471)

### 2 ⊗ 3 = 3 ⊕ 3'

CG coefficients (α = doublet, β = triplet):
- **3** component:
  - (α₁β₁, (√3/2)α₂β₃ - (1/2)α₁β₂, (√3/2)α₂β₂ - (1/2)α₁β₃)ᵀ
- **3'** component:
  - (-α₂β₁, (√3/2)α₁β₃ + (1/2)α₂β₂, (√3/2)α₁β₂ + (1/2)α₂β₃)ᵀ

### 2 ⊗ 3̂ = 3̂ ⊕ 3̂'

Same CG coefficients as 2 ⊗ 3 above (with same structure, hatted irreps).

### 2̂ ⊗ 3 = 3̂ ⊕ 3̂'

Same CG coefficients as 2 ⊗ 3 above.

### 2̂ ⊗ 3̂' = 3 ⊕ 3'

Same CG coefficients as 2 ⊗ 3 above.

### 2 ⊗ 3' = 3 ⊕ 3' (and related)

CG coefficients (α = doublet, β = triplet):
- **3** component:
  - (-α₂β₁, (√3/2)α₁β₃ + (1/2)α₂β₂, (√3/2)α₁β₂ + (1/2)α₂β₃)ᵀ
- **3'** component:
  - (α₁β₁, (√3/2)α₂β₃ - (1/2)α₁β₂, (√3/2)α₂β₂ - (1/2)α₁β₃)ᵀ

Applies similarly to: 2 ⊗ 3̂' = 3̂ ⊕ 3̂', 2̂ ⊗ 3' = 3̂ ⊕ 3̂', 2̂ ⊗ 3̂ = 3 ⊕ 3'.

---

## Table 4: Products of two 3-dimensional irreps (NPP20 Tab. tab:33, lines 2474-2570)

### 3 ⊗ 3 = 1 ⊕ 2 ⊕ 3 ⊕ 3'
### 3' ⊗ 3' = 1 ⊕ 2 ⊕ 3 ⊕ 3'
### 3̂ ⊗ 3̂' = 1 ⊕ 2 ⊕ 3 ⊕ 3'

CG coefficients (α, β = triplets):
- **1** component: (1/√3)(α₁β₁ + α₂β₃ + α₃β₂)
- **2** component: (1/√2)[(2α₁β₁ - α₂β₃ - α₃β₂)/√3, α₂β₂ + α₃β₃]ᵀ
- **3** component: (1/√2)[(α₃β₃ - α₂β₂), (α₁β₃ + α₃β₁), (-α₁β₂ - α₂β₁)]ᵀ
- **3'** component: (1/√2)[(α₃β₂ - α₂β₃), (α₂β₁ - α₁β₂), (α₁β₃ - α₃β₁)]ᵀ

### 3 ⊗ 3' = 1' ⊕ 2 ⊕ 3 ⊕ 3'
### 3̂ ⊗ 3̂ = 1' ⊕ 2 ⊕ 3 ⊕ 3'
### 3̂' ⊗ 3̂' = 1' ⊕ 2 ⊕ 3 ⊕ 3'

CG coefficients:
- **1'** component: (1/√3)(α₁β₁ + α₂β₃ + α₃β₂)
- **2** component: (1/√2)[(α₂β₂ + α₃β₃), (-2α₁β₁ + α₂β₃ + α₃β₂)/√3]ᵀ
- **3** component: (1/√2)[(α₃β₂ - α₂β₃), (α₂β₁ - α₁β₂), (α₁β₃ - α₃β₁)]ᵀ
- **3'** component: (1/√2)[(α₃β₃ - α₂β₂), (α₁β₃ + α₃β₁), (-α₁β₂ - α₂β₁)]ᵀ

### Cross-products with mixed hatted/unhatted:

| Product | Result |
|---|---|
| 3 ⊗ 3̂ | 1̂ ⊕ 2̂ ⊕ 3̂ ⊕ 3̂' |
| 3 ⊗ 3̂' | 1̂' ⊕ 2̂ ⊕ 3̂ ⊕ 3̂' |
| 3' ⊗ 3̂ | 1̂' ⊕ 2̂ ⊕ 3̂ ⊕ 3̂' |
| 3' ⊗ 3̂' | 1̂ ⊕ 2̂ ⊕ 3̂ ⊕ 3̂' |

CG coefficients for 3 ⊗ 3̂ → 1̂ ⊕ 2̂ ⊕ 3̂ ⊕ 3̂' are same structure as 3⊗3 above
but produce hatted irreps. From LYD20 App (TeX line 1819):
  3 ⊗ 3̂ → 1̂ ⊕ 2̂ ⊕ 3̂ ⊕ 3̂'

---

## Key Products for Model VI (LYD20)

Model VI uses Q ~ 3 with the following couplings:

### (Q ⊗ Y^(1)_{3̂'})_{1̂'} : 3 ⊗ 3̂' → 1̂'

From 3 ⊗ 3̂' = 1̂' ⊕ 2̂ ⊕ 3̂ ⊕ 3̂' (from LYD20 App line 1824: `3 ⊗ 3̂' → 1̂'`):

The **1̂'** component of 3 ⊗ 3̂' with CG (from LYD20 App lines 1828):
  `1̂' ~ α₁β₁ + α₂β₃ + α₃β₂`

So for u^c row: u^c (Q Y^(1)_{3̂'})_{1̂'} = u^c · (Q₁Y₁ + Q₂Y₃ + Q₃Y₂)
where Y_i are components of Y^(1)_{3̂'} in LYD20 notation (Y₁, Y₂, Y₃ = 
weight-1 modular forms, transforming as 3̂').

**Mass matrix row for u^c**: [α_u Y₁, α_u Y₃, α_u Y₂]

### (Q ⊗ Y^(2)_{3})_{1} : 3 ⊗ 3 → 1

From 3 ⊗ 3 = 1 ⊕ 2 ⊕ 3 ⊕ 3', the **1** component:
  `1 ~ (1/√3)(α₁β₁ + α₂β₃ + α₃β₂)`

For c^c row: c^c (Q Y^(2)_{3})_1 = c^c · (Q₁Y^(2)₃ + Q₂Y^(2)₅ + Q₃Y^(2)₄)
(using LYD20 component notation: Y^(2)_3 = Y^(2)_3 component, etc.)

**Mass matrix row for c^c**: [β_u Y^(2)₃, β_u Y^(2)₅, β_u Y^(2)₄]

### (Q ⊗ Y^(5)_{3̂})_{1̂} : 3 ⊗ 3̂ → 1̂

From 3 ⊗ 3̂ = 1̂ ⊕ 2̂ ⊕ 3̂ ⊕ 3̂' (LYD20 line 1819):
  `1̂ ~ α₁β₁ + α₂β₃ + α₃β₂`

For t^c row: t^c (Q Y^(5)_{3̂})_{1̂} = t^c · (Q₁Y^(5)₃ + Q₂Y^(5)₅ + Q₃Y^(5)₄)

**Mass matrix row for t^c**: [γ_u Y^(5)₃, γ_u Y^(5)₅, γ_u Y^(5)₄]

---

## Modular Form Components (NPP20 notation)

### Weight-1 triplet Y^(1)_{3̂} (NPP20 Eq. k1triplet, line 708)

In NPP20 basis (θ, ε = Jacobi theta constants):
```
Y^(1)_{3̂}(τ) = (√2 εθ, ε², -θ²)ᵀ
```

**LYD20 uses Y^(1)_{3̂'} at weight 1** (different basis — LYD20 seed is 3̂' not 3̂).
In LYD20: the weight-1 modular forms Y₁, Y₂, Y₃ transform as 3̂' (lines 317-330).

### Weight-2 modular forms Y^(2) (NPP20 Eq. k2, lines 769-783)

```
Y^(2)_{2}(τ) = ((1/√2)(θ⁴ + ε⁴), -√6 ε²θ²)ᵀ

Y^(2)_{3'}(τ) = ((1/√2)(θ⁴ - ε⁴), -2εθ³, -2ε³θ)ᵀ
```

In LYD20 notation (lines 381-382):
- Y^(2)_2 = (Y^(2)_1, Y^(2)_2)ᵀ (the doublet)
- Y^(2)_3 = (Y^(2)_3, Y^(2)_4, Y^(2)_5)ᵀ (the triplet 3)

### Weight-3 modular forms Y^(3) (NPP20 Eq. k3, lines 826-844)

```
Y^(3)_{1̂'}(τ) = √3(εθ⁵ - ε⁵θ)

Y^(3)_{3̂}(τ) = (ε⁵θ + εθ⁵, (1/2√2)(5ε²θ⁴ - ε⁶), (1/2√2)(θ⁶ - 5ε⁴θ²))ᵀ

Y^(3)_{3̂'}(τ) = (1/2)(-4√2 ε³θ³, θ⁶ + 3ε⁴θ², -3ε²θ⁴ - ε⁶)ᵀ
```

### Weight-4 modular forms Y^(4) (NPP20 Eq. k4, lines 851-878)

```
Y^(4)_{1}(τ)  = (1/2√3)(θ⁸ + 14ε⁴θ⁴ + ε⁸)

Y^(4)_{2}(τ)  = ((1/4)(θ⁸ - 10ε⁴θ⁴ + ε⁸), √3(ε²θ⁶ + ε⁶θ²))ᵀ

Y^(4)_{3}(τ)  = (3/2√2)(√2(ε²θ⁶ - ε⁶θ²), ε³θ⁵ - ε⁷θ, -εθ⁷ + ε⁵θ³)ᵀ

Y^(4)_{3'}(τ) = ((1/4)(θ⁸ - ε⁸), (1/2√2)(εθ⁷ + 7ε⁵θ³), (1/2√2)(7ε³θ⁵ + ε⁷θ))ᵀ
```

### Weight-5 modular forms Y^(5) (NPP20 App lines 2585-2621)

```
Y^(5)_{2̂}(τ) = ((3/2)(ε³θ⁷ - ε⁷θ³), (√3/4)(εθ⁹ - ε⁹θ))ᵀ

Y^(5)_{3̂,1}(τ) = ((6√2/√5)ε⁵θ⁵, (3/8√5)(5ε²θ⁸ + 10ε⁶θ⁴ + ε¹⁰),
                    -(3/8√5)(θ¹⁰ + 10ε⁴θ⁶ + 5ε⁸θ²))ᵀ

Y^(5)_{3̂,2}(τ) = ((3/4)(εθ⁹ - 2ε⁵θ⁵ + ε⁹θ), (3/√2)(-ε²θ⁸ + ε⁶θ⁴),
                    (3/√2)(-ε⁴θ⁶ + ε⁸θ²))ᵀ

Y^(5)_{3̂'}(τ) = (2(ε³θ⁷ + ε⁷θ³), (1/4√2)(θ¹⁰ - 14ε⁴θ⁶ - 3ε⁸θ²),
                   (1/4√2)(3ε²θ⁸ + 14ε⁶θ⁴ - ε¹⁰))ᵀ
```

**Note**: NPP20 has TWO 3̂ multiplets at weight 5 (Y^(5)_{3̂,1} and Y^(5)_{3̂,2}).
LYD20's Y^(5)_{3̂} = some linear combination of these. For our Model VI, the
precise combination used by LYD20 can be inferred from the explicit mass matrix
entries. The key point is that the structure of M_u has been verified by LYD20
authors using their CG coefficients.

### Weight-6 modular forms Y^(6) (NPP20 App lines 2623-2708)

```
Y^(6)_{1}(τ)  = (1/4√6)(θ¹² - 33ε⁴θ⁸ - 33ε⁸θ⁴ + ε¹²)

Y^(6)_{1'}(τ) = (3/2)√(3/2)(ε²θ¹⁰ - 2ε⁶θ⁶ + ε¹⁰θ²)

Y^(6)_{2}(τ)  = ((1/8)(θ¹² + 15ε⁴θ⁸ + 15ε⁸θ⁴ + ε¹²),
                  -(√3/4)(ε²θ¹⁰ + 14ε⁶θ⁶ + ε¹⁰θ²))ᵀ

Y^(6)_{3}(τ)  = ((3/2)(ε²θ¹⁰ - ε¹⁰θ²),
                  (3/4√2)(5ε³θ⁹ - 6ε⁷θ⁵ + ε¹¹θ),
                  (3/4√2)(εθ¹¹ - 6ε⁵θ⁷ + 5ε⁹θ³))ᵀ

Y^(6)_{3',1}(τ) = (-(3/8√13)(θ¹² - 3ε⁴θ⁸ + 3ε⁸θ⁴ - ε¹²),
                    (3√2/√13)(3ε⁵θ⁷ + ε⁹θ³),
                    (3√2/√13)(ε³θ⁹ + 3ε⁷θ⁵))ᵀ

Y^(6)_{3',2}(τ) = (3(ε⁴θ⁸ - ε⁸θ⁴),
                    -(3/4√2)(εθ¹¹ + 2ε⁵θ⁷ - 3ε⁹θ³),
                    (3/4√2)(3ε³θ⁹ - 2ε⁷θ⁵ - ε¹¹θ))ᵀ
```

---

## Basis Conversion Note (LYD20 vs NPP20)

LYD20 uses Y^(1)_{3̂'} as the weight-1 seed (transforms as 3̂'), while NPP20 uses
Y^(1)_{3̂}. These are related by a basis change. For the numerical implementation
(H3.C/D), we use the **LYD20 basis** throughout, implementing the modular forms
as polynomials in Y₁, Y₂, Y₃ per LYD20 Appendix (lines 346-395), which avoids
the basis mismatch issue. The mass matrices in H3.C are written directly in terms
of LYD20's Y^(k)_i components.
