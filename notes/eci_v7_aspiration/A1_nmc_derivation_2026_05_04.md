# NMC Thawing Quintessence: Derivation of w_0, w_a from First Principles

**ECI v6.0.45 | 2026-05-04**

---

## Anti-Hallucination Notice

The morning sympy script (`/tmp/agents_v643_morning/P3_5/coupled_de_sympy.py`) cited
"Pan-Yang JCAP 2018, arXiv:1804.05064 eq. 18" for `Δw_a^NMC = -2 ξ_χ Ω_φ0`.

**arXiv:1804.05064 VERIFIED via API**: this is "The FABLE simulations" by Henden et al. 2018
(galaxy-cluster hydrodynamics). No Pan-Yang NMC quintessence paper exists. The coefficient
`-2` was HALLUCINATED. This document provides the correct derivation.

---

## Setup

**Lagrangian:**
```
L_χ = -½(∂χ)² - V(χ) - ½ ξ_χ R χ²
V(χ) = V_0 exp(-λχ/M_P)   (exponential potential)
```

**All reference arXiv IDs verified via export.arxiv.org/api/query:**
- arXiv:0712.3450 = Scherrer-Sen 2008 PRD 77 083515 "Thawing quintessence with a nearly flat potential" [VERIFIED]
- arXiv:2504.07679 = Wolf-García-García-Anton-Ferreira 2025 PRL 135 081001 "Assessing cosmological evidence for non-minimal coupling" [VERIFIED]
- arXiv:2509.13302 = Adam-Hertzberg+ JCAP 04 (2026) 052 "Comparing Minimal and Non-Minimal Quintessence Models to 2025 DESI Data" [VERIFIED]
- arXiv:2510.14941 = Sánchez López-Karam-Hazra 2025 "Non-Minimally Coupled Quintessence in Light of DESI" [VERIFIED]
- arXiv:0802.1086 = Pettorino-Baccigalupi 2008 PRD 77 103003 "Coupled and Extended Quintessence" [VERIFIED]

---

## Step 1: Klein-Gordon Equation

Variation of the action w.r.t. χ in flat FLRW gives:
```
χ̈ + 3Hχ̇ + V'(χ) = ξ_χ R χ
R = 6(2H² + Ḣ)   (Ricci scalar, flat FLRW)
V'(χ) = -λV(χ)/M_P
```

## Step 2: NMC Stress-Energy Tensor

In the Jordan frame with perturbative ξ_χ (following Pettorino-Baccigalupi 0802.1086):
```
ρ_χ = ½χ̇² + V(χ) + 6 ξ_χ H χ χ̇
p_χ = ½χ̇² - V(χ) - ξ_χ(2Ḣ + 4H²)χ² - 4 ξ_χ H χ χ̇
```
(Terms O(ξ_χ (χ/M_P)²) dropped as subdominant for perturbative coupling.)

## Step 3: Slow-Roll Attractor

Under slow-roll conditions (χ̈ ≪ 3Hχ̇ and χ̇² ≪ V), using R ≈ 12H² (near de Sitter):
```
χ̇_SR = λV(χ)/(3HM_P) + 4 ξ_χ H χ + O(ξ_χ²)
```

From Friedmann: H² = V/(3M_P² Ω_φ), so:
```
χ̇²/V = λ² Ω_φ / 3    [at O(ξ_χ⁰)]
```

Note: ε_V = (M_P/V)²(V')²/2 = λ²/2 (constant for exponential potential).

## Step 4: w(a) at Leading Order

Define:
- u = χ̇²/V = λ²Ω_φ/3
- A = 6ξ_χHχχ̇/V = 2ξ_χλχ/M_P  (from ρ NMC correction)
- B = [-ξ_χ(2Ḣ+4H²)χ² - 4ξ_χHχχ̇]/V ≈ -4ξ_χλχ/(3M_P)  (from p NMC correction, slow-roll)

Then w = p_χ/ρ_χ = (u/2 - 1 + B)/(1 + u/2 + A).

Expanding to first order in u, A, B (all small):
```
w ≈ -1 + u + A + B
```

The key combination:
```
A + B = 2ξ_χλχ/M_P - 4ξ_χλχ/(3M_P) = (2/3) ξ_χλχ/M_P
```
**Verified by sympy.**

Therefore:
```
w = -1 + (λ²/3)Ω_φ + (2/3) ξ_χ λ χ / M_P
```

## Step 5: CPL Fit

The tracker slow-roll solution gives χ evolving as:
```
dχ/d(ln a) = χ̇/H = λ M_P Ω_φ(a)
```

Linearizing near a=1:
```
χ(a) ≈ χ_0 + λ M_P Ω_φ,0 (a-1)
```

Therefore dw/da has two contributions:
1. From dΩ_φ/da: using dΩ_φ/d(ln a) = 3Ω_φ(1-Ω_φ)(1+w_φ), at leading order
   (1+w)|_{a=1} = λ²Ω_φ,0/3, so dΩ_φ/da|_{a=1} = λ²Ω_φ,0²(1-Ω_φ,0)
2. From dχ/da via the NMC term: (2/3)ξ_χλ/M_P × dχ/da|_{a=1} = (2/3)ξ_χλ²Ω_φ,0

CPL parameters:
```
w_0^NMC = -1 + (λ²/3) Ω_φ,0 + (2/3) ξ_χ λ χ_0/M_P

w_a^NMC = -w'(a=1) = -λ²Ω_φ,0 [Ω_φ,0(1-Ω_φ,0) + (2/3)ξ_χ]
```

NMC correction alone:
```
Δw_a^NMC = -(2/3) ξ_χ λ² Ω_φ,0
```

## Step 6: Result

**[CORRECTED]** The correct result is:

```
Δw_a^NMC = -(2/3) ξ_χ λ² Ω_φ,0
```

NOT `-2 ξ_χ Ω_φ,0` as the hallucinated "Pan-Yang" derivation claimed.

**Key differences:**
1. The coefficient is `-(2/3) λ²`, not `-2`. Dimensionally: the original claim has wrong units — w_a is dimensionless but `ξ_χ Ω_φ,0` alone is also dimensionless, yet the `-2` was written with no λ-dependence. This is a fatal inconsistency since λ controls the potential steepness.
2. The factor `λ²` arises from χ̇/H = λ M_P Ω_φ on the slow-roll attractor — it cannot be absent.
3. For typical thawing quintessence (λ ~ 1, ξ_χ ~ 0.1, Ω_φ,0 ~ 0.7): Δw_a ~ -0.047, while the hallucinated formula would give Δw_a ~ -0.14 (3× too large).

## Full Final Expressions

```
w_0^NMC = -1 + (λ²/3) Ω_φ,0 + (2/3) ξ_χ λ χ_0/M_P

w_a^NMC = -λ² Ω_φ,0 [Ω_φ,0(1-Ω_φ,0) + (2/3)ξ_χ]

Δw_a^NMC ≡ w_a^NMC - w_a^min = -(2/3) ξ_χ λ² Ω_φ,0
```

## Sanity Checks (all pass)

- ξ_χ=0: recovers minimal thawing wa = -λ²Ω_φ,0²(1-Ω_φ,0) ✓
- λ→0 (CC limit): w_a → 0 ✓
- Ω_φ,0 → 0: w_a → 0 ✓
- ξ_χ > 0: Δw_a < 0 (NMC deepens thawing), consistent with Wolf+2025 (arXiv:2504.07679) ✓

## Files

- `/tmp/agents_v645_afternoon/A1_nmc_sympy/derivation.py` — executable sympy (run with python3)
- `/tmp/agents_v645_afternoon/A1_nmc_sympy/derivation.tex` — LaTeX for eci.tex insertion
- `/tmp/agents_v645_afternoon/A1_nmc_sympy/derivation.md` — this file

---

**Hallucination note:** The morning's Pan-Yang citation (arXiv:1804.05064) was fabricated.
This derivation supersedes all prior coefficient claims for Δw_a^NMC.
Hallucination counter: 57 → 58 (Pan-Yang catch counted in morning; this confirms it).
