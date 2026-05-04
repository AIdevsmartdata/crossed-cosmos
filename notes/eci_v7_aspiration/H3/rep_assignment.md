# H3.A — Rep Assignment from LYD20 (arXiv:2006.10722)

## Source

Liu, Yao, Ding (2020), "Modular Invariant Quark and Lepton Models in Double
Covering of S_4 Modular Group", arXiv:2006.10722, Phys. Rev. D 103, 056013 (2021).

## Chosen Assignment: LYD20 Model VI (All-singlet Q ~ 3)

**Table reference**: Table I (tab:quark_mod) in LYD20, row "Model VI".
**Equation reference for superpotential**: Eq. (6) in the quark sector subsection
(labeled \eq:Wq6 in the TeX source, line 1372-1375).
**Mass matrix**: Eq. labeled \eq:Mq_6, lines 1379-1390 in TeX source.

### Why Model VI is chosen as "simplest"

Model VI uses **Q ~ 3 (triplet), all right-handed quarks as singlets**, which is the
most transparent structure for our ECI v7 goals:
- Up-sector M_u is **diagonal in generation index** (each row = one right-handed field),
  one coupling per row → 3 coupling parameters α_u, β_u, γ_u for up-sector only.
- No doublet assignments → no mixing between u^c and c^c within a doublet.
- This minimises the parameter count in the up-sector (3 real couplings + τ).

### Field Assignments (LYD20 Table I, Model VI)

| Field  | S'_4 rep       | Modular weight k_I           |
|--------|----------------|------------------------------|
| Q      | **3** (triplet)| k_Q                          |
| u^c    | **1̂** (hat-1) | 1 - k_Q                      |
| c^c    | **1** (trivial)| 2 - k_Q                      |
| t^c    | **1̂'**(hat-1')| 5 - k_Q                      |
| d^c    | **1̂** (hat-1) | 1 - k_Q                      |
| s^c    | **1̂'**(hat-1')| 5 - k_Q                      |
| b^c    | **1̂** (hat-1) | 5 - k_Q                      |
| H_u    | **1** (trivial)| 0                            |
| H_d    | **1** (trivial)| 0                            |

Weight condition (LYD20 Eq. near line 1369):
```
k_Q = 1 - k_{u^c} = 2 - k_{c^c} = 5 - k_{t^c}
    = 1 - k_{d^c} = 5 - k_{s^c} = 5 - k_{b^c}
```

### Modular Invariance Check

The Yukawa coupling W ⊃ q^c (Q Y^(k_Y))_1 H must have total weight zero.
The modular weight of the coupling: k_{q^c} + k_Q + k_Y + 0 = 0 mod (automorphy).

For u^c row: k_{u^c} + k_Q + k_Y = (1-k_Q) + k_Q + k_Y = 1 + k_Y = 0 → k_Y = -1
But LYD20 uses k_Y = 1 (weight-1 modular forms Y^(1)_{3̂'}), giving
  k_{u^c} + k_Q + k_{Y^(1)} = (1-k_Q) + k_Q + 1 = 2 ≠ 0.

**Correction**: In SUSY formalism the Kähler weight is -k (negative), so the
superpotential coupling requires k_{field1} + k_{field2} + k_{Y} = 0 where
all weights are positive integers. Checking:
  u^c: weight (1-k_Q), Q: weight k_Q, Y^(1): weight 1 → sum = 2 ≠ 0.

**Re-reading**: LYD20 convention is that the NEGATIVE of the modular weight is used
for chiral superfields (weight = -k_I in the sense that (cτ+d)^{+k_I} appears
in modular transformation). The sum rule is k_{q^c} + k_Q + k_Y = total weight of
operator, and modular invariance requires this equals the weight of H (= 0), so
k_{q^c} + k_Q + k_Y = 0 in the convention where weights are added as positive numbers.

Checking Model VI's u^c coupling (LYD20 line 1373):
  W_u ∋ α_u u^c (Q Y^(1)_{3̂'})_{1̂'} H_u
  Weight: k_{u^c} + k_Q + k_{Y^(1)} = (1-k_Q) + k_Q + 1 = 2

This is non-zero unless one uses the SUSY convention that the superpotential has
conformal weight 3, and the modular weight of W must equal 0. The convention in
LYD20 is: the WEIGHT OF THE COUPLING is k_{u^c} + k_Q + k_{Y}, and for
H_u with k=0 one needs k_{u^c} + k_Q + k_Y = 0. The resolution is that LYD20
assigns modular weight as k_I (positive), and the invariance condition is:

  SUM of all modular weights in the coupling = 0

So for u^c (Q Y^(1))_1 H_u: (-k_{u^c}) + (-k_Q) + (-k_Y^(1)) + 0 = 0 where
(-k_I) is the transformation weight appearing in (cτ+d)^{-k_I}. Thus:
  -(1-k_Q) - k_Q - 1 = -2 ≠ 0.

**The actual LYD20 convention** (from context at line 477 and abstract): the weight
k_I appears in (cτ+d)^{+k_I} for the modular form, but fields transform as
(cτ+d)^{-k_I}. For the superpotential to be modular-invariant, one needs
  Σ(field weights in rep) + (modular form weight) = 0
Reading line 1369: k_Q = 1 - k_{u^c} means k_{u^c} = 1 - k_Q. Then
  W_u ∋ u^c · Q · Y^(1): sum = k_{u^c} + k_Q + 1 = (1-k_Q) + k_Q + 1 = 2.
This is 2, but since W must have weight ≥ 0 for SUSY and the H_u has weight 0,
the entire operator must have total weight = 0. The discrepancy suggests the 2 is
cancelled by noting that in a weight-k field f, the kinematic coupling in W picks
up (cτ+d)^{-k_{field}} so the FIELD contributions are -k_{field}. Thus:
  (-k_{u^c}) + (-k_Q) + k_{Y^(1)} = -(1-k_Q) - k_Q + 1 = -1 + k_Q - k_Q + 1 = 0. ✓

**Conclusion**: Modular invariance is verified. The LYD20 convention is that
fields carry weight -k_I (transform as (cτ+d)^{-k_I}) while modular forms Y carry
positive weight k_Y. The sum rule is: Σ(-k_{fields}) + k_Y = 0. Model VI satisfies
this for each coupling term as confirmed by LYD20 authors.

### Superpotential (LYD20 Eq. Wq6, lines 1372-1375)

Up-sector (3 couplings, all real after field redefinitions with gCP):
```
W_u = α_u · u^c (Q Y^(1)_{3̂'})_{1̂'} H_u
    + β_u · c^c (Q Y^(2)_{3})_{1}  H_u
    + γ_u · t^c (Q Y^(5)_{3̂})_{1̂} H_u
```

Down-sector (4 couplings, γ_{d2} complex without gCP):
```
W_d = α_d · d^c (Q Y^(1)_{3̂'})_{1̂'} H_d
    + β_d · s^c (Q Y^(5)_{3̂})_{1̂}  H_d
    + γ_{d1} · b^c (Q Y^(5)_{3̂',I})_{1̂'} H_d
    + γ_{d2} · b^c (Q Y^(5)_{3̂',II})_{1̂'} H_d
```

### Parameter Count

Up-sector free parameters (real, with gCP imposed → all real):
- α_u, β_u, γ_u: 3 real couplings (phases absorbed)
- Re(τ), Im(τ): 2 real parameters for modulus
- α_u v_u: 1 overall mass scale (sets m_t)

**Total up-sector for mass ratios**: 3 ratios (β_u/α_u, γ_u/α_u) + 2 (τ) = 4 free
parameters fitting 3 mass ratios {m_u/m_c, m_c/m_t, and m_t as scale}.

Down-sector adds 3 more real couplings (α_d, β_d, γ_{d1}) + 1 complex (γ_{d2})
for CKM structure.

**Total model parameters (LYD20 p.~line 1391)**: 6 real + 1 complex + 2(τ) = 10
free real parameters total. This is Model VI ("without gCP, 10 parameters").

### Best Fit from LYD20 (Model VI, lines 1393-1406)

```
τ = -0.4999 + 0.8958i
β_u/α_u = 62.2142
γ_u/α_u = 0.00104
β_d/α_d = 0.7378
γ_{d1}/α_d = 1.4946
γ_{d2}/α_d = -0.1958 - 0.2762i   [complex!]
α_u v_u = 0.07989 GeV
α_d v_d = 0.00091 GeV
```

**Predictions at best fit**:
- θ^q_{12} = 0.22731, θ^q_{13} = 0.00298, θ^q_{23} = 0.04873, δ^q_CP = 67.20°
- m_u/m_c = 0.00204, m_c/m_t = 0.00268
- m_d/m_s = 0.05182, m_s/m_b = 0.01309

Note: θ^q_{23} is larger than experiment (PDG: 0.03888). This is flagged by LYD20.

### Alternative Choice: Model VI with gCP (9 parameters)

For our ECI v7 work we will also implement **Model VII with gCP** (which gives
all observables within 1σ per LYD20 line 1438), but Model VI is chosen for H3.C/D
because its M_u has the simpler diagonal-row structure.
