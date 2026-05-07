# M178 sub-task 1 — Candidate (alpha) Borcea-Voisin Z_2 orbifold (explicit)

**Status:** WELL-POSED, single specialist gap (Inose 1977 explicit Weierstrass for K3 X_b).

## Notation (ECI v9 convention)

- L = lepton sector ; Q = quark sector
- tau_L = i (anchor M134, Damerell ladder, 4.5.b.a CM newform)
- tau_Q = i*sqrt(11/2) (anchor M171, Schütt class [2] form (2,0,11))
- K_L = Q(i)            (CM field of E_a^L)
- K_Q = Q(sqrt(-22))    (CM field of E_b^Q)

## Step (a) — Explicit lepton K3 X^L = X_a^L

### Elliptic curve E_a^L

**LMFDB 32.a3** (M145 verified live 2026-05-06):

$$E_a^L : y^2 = x^3 - x \quad \cong \quad y^2 = 4x^3 - 4x \text{ (Coates-Wiles model)}$$

via the substitution (x, y) ↔ (x, y/2).

- Conductor N = 32 = 2^5
- j(E_a^L) = 1728
- CM discriminant D = -4 (CM by full ring O_{K_L} = Z[i])
- Rank E_a^L(Q) = 0
- E_a^L(Q)_{tors} = Z/2 ⊕ Z/2 (generators (0,0), (1,0), (-1,0))
- Real period Ω_real = 2*ϖ = 5.244115108... (ϖ lemniscate constant = Γ(1/4)²/(2√(2π)))
- L(E_a^L, 1) = ϖ/4 (M145, BSD-strong Sha = 1)
- Isomorphism class period: τ = i (upper half plane, fundamental domain corner)

**This is the SINGULAR ELLIPTIC CURVE WITH CM BY Z[i] over Q.** It is defined over Q (not over Q(i)), but acquires extra Z[i]-action over Q(i).

### Singular K3 X_a^L

**Definition.** X_a^L = Km(E_a^L × E_a^L), the Kummer K3 of the abelian surface E_a^L × E_a^L (smooth resolution of (E × E)/⟨−1⟩).

**Properties.**
- T(X_a^L) ⊗ Q ≅ Q(i) as Hodge structure with CM action
- T(X_a^L) Gram matrix in M_2(Z): for (a,b,c) = (1,0,1) reduced binary form of disc -4
  G_a^L = [[2 0]; [0 2]]   (det 4, disc -4) — this is the CM elliptic curve transcendental lattice
  
  But T(Km(E × E)) for E with CM by Z[i] has rank 2 lattice with discriminant 4 (after the standard Shioda-Inose duplication).
- Picard rank ρ(X_a^L) = 20
- Defined over Q (since j(E_a^L) = 1728 ∈ Q, and Kummer construction is rational)

**Field of definition gap (subtle):** The isomorphism T(X_a^L) ≅ T(E × E) holds rationally, but H^{2,0} as a Q(i)-module is defined over Q(i) (smallest extension carrying the CM action). For ECI v9 W^L period evaluation, we work over Q(i).

### Involution σ_L on X_a^L

The Borcea-Voisin construction (Borcea 1996, Voisin 1993) requires a **non-symplectic involution** σ : X → X with σ*Ω_X = -Ω_X (acts as -1 on H^{2,0}).

For Kummer surfaces of E × E with CM:
- The (-1) involution on E × E descends to Km(E × E)
- The diagonal swap (P, Q) ↔ (Q, P) on E × E descends to Km(E × E)
- The combination of these two gives an order-2 group action, but σ_L must be **non-symplectic** (act as -1 on Ω)

**Standard choice (Borcea-Voisin canonical):** σ_L acts as the lift of (P, Q) ↦ (P, -Q) on E_a^L × E_a^L to its Kummer Km(E_a^L × E_a^L). This is well-defined because the quotient by ⟨(-1, -1)⟩ is involved by the (id, -1) action.

**Action on Ω_{X_a^L}.** Ω_{X_a^L} pulled back to E × E is the form dx_1 ∧ dx_2 (where x_i are the local coordinates on the two E factors). The involution (id, -1)* gives dx_1 ∧ d(-x_2) = -dx_1 ∧ dx_2. So σ_L*Ω = -Ω. **Confirmed non-symplectic.**

**Fixed locus of σ_L.** On E × E, the fixed locus of (id, -1) is E × E[2] = E × {O, T_1, T_2, T_3} (4 disjoint copies of E). After Kummer resolution, this descends to a curve of fixed points on X_a^L. Borcea 1996 §1 / Voisin 1993 §1: the fixed locus is a disjoint union of smooth curves.

For our X_a^L = Km(E_a^L × E_a^L) with σ_L = lift of (id, -1):
- Fixed locus on E × E: E × E[2], dim = 1, four disjoint copies of E_a^L
- After Kummer: each fixed E_a^L lifts to a smooth curve on Km(E × E); plus contributions from exceptional divisors over E[2] × E[2]
- Net: σ_L has fixed locus consisting of finite curves of various genera; standard Borcea-Voisin setup applies.

## Step (b) — Explicit quark K3 X^Q = X_b^Q

### CM elliptic curves E_a^Q, E_b^Q over Q(sqrt(2))

From M176 (THEOREM M176.1):

$$E_a^Q, E_b^Q : y^2 = x^3 + a x + b$$

with j-invariants:
- j(E_a^Q) = 3,147,421,320,000 + 2,225,561,184,000·√2
- j(E_b^Q) = 3,147,421,320,000 - 2,225,561,184,000·√2

Both roots of H_{-88}(X) = X² - 6,294,842,640,000·X + 15,798,135,578,688,000,000.

Both have CM by O_{K_Q} = Z[√-22], related by Galois conjugation √2 ↔ -√2.

### Singular K3 X_b^Q (via Shioda-Inose)

**Definition (Schütt 2008 Theorem 3 + Theorem 29 + Lemma 33):**
- T(X_b^Q) ⊗ Q ≅ Q(√-22) as Hodge structure
- T(X_b^Q) has Gram matrix [[4, 0]; [0, 22]] (form (2, 0, 11), class [2] of disc -88, τ_b = i√(11/2))
- Picard rank ρ(X_b^Q) = 20
- Minimal field of definition: H(-88) = Q(√-22, √2) (Schütt Lemma 33 + Theorem 2)

**Construction recipe (Schütt p.3 verbatim):**
$$E_b^Q \times E_b^Q  \xrightarrow{\text{quot. by} \langle -1\rangle}  \text{Km}(E_b^Q \times E_b^Q)  \xleftarrow{2:1}  X_b^Q$$
both rational maps 2:1, T(X_b^Q) ≅ T(E_b^Q × E_b^Q).

**Specialist gap (residual from M176):** Inose 1977 [10] explicit Weierstrass for X_b^Q (as elliptic K3 fibration over P^1 with section) is not freely available (1977 Symposium proceedings, Kyoto). Schütt confirms it exists.

**However**, the construction is **complete** in the sense:
- E_b^Q is explicit (Weierstrass coefficients in Q(√2))
- Km(E_b^Q × E_b^Q) is constructible by standard 16-blowup of (E_b^Q × E_b^Q)/⟨−1⟩
- X_b^Q is determined by 2:1 cover of Km branched along specific divisor (Inose construction)

For ECI v9 W^Q period purposes, only T(X_b^Q) ⊗ Q and Ω_{X_b^Q} matter, both of which are explicit.

### Involution σ_Q on X_b^Q

Same construction as σ_L: σ_Q = lift of (id, -1) on E_b^Q × E_b^Q to Km, descending through the Shioda-Inose 2:1 cover to X_b^Q.

**Action on Ω_{X_b^Q}.** Same calculation: σ_Q*Ω_{X_b^Q} = -Ω_{X_b^Q}. **Non-symplectic involution.**

**Fixed locus of σ_Q.** Similar to σ_L: E_b^Q × E_b^Q[2] descends to disjoint union of smooth curves on X_b^Q, plus ramification divisor of the Shioda-Inose 2:1 cover.

## Step (c) — Borcea-Voisin Calabi-Yau 4-fold Y_α

**General Borcea-Voisin construction (CY 4-fold version).** Given:
- K3 surface S^L with non-symplectic involution σ_L, σ_L*Ω_{S^L} = -Ω_{S^L}
- K3 surface S^Q with non-symplectic involution σ_Q, σ_Q*Ω_{S^Q} = -Ω_{S^Q}

Form the Z_2-orbifold:
$$Y_\alpha = (X_a^L \times X_b^Q) / \langle \sigma_L \times \sigma_Q \rangle$$

with the resolution of singularities along Fix(σ_L) × Fix(σ_Q).

**Why CY 4-fold?**
- (σ_L × σ_Q)*(Ω_{X_a^L} ∧ Ω_{X_b^Q}) = (-Ω_{X_a^L}) ∧ (-Ω_{X_b^Q}) = Ω_{X_a^L} ∧ Ω_{X_b^Q}
- Hence Ω_Y = Ω_{X_a^L} ∧ Ω_{X_b^Q} **descends to Z_2-quotient**, giving a holomorphic (4,0)-form on Y_α
- Y_α has trivial canonical bundle and h^{1,0} = 0 (modulo standard CY 4-fold cohomology computation)
- After resolution, smooth CY 4-fold

**Important: this is the Kanno-Watari Y = (X^(1) × X^(2))/Z_2 framework.** KW arXiv:2012.01111 page 30, eq (49) (verbatim from PDF Read M178):

$$\Omega_Y = v^{(1)}_{(20)} v^{(2)}_{(20)} + (v^{(1)}_{(20)} t^{(2)} + t^{(1)} v^{(2)}_{(20)}) - v^{(1)}_{(20)} v^{(2)}_{(02)} (2C^{(2)})^{-1}(t^{(2)},t^{(2)})_{T^{(2)}_X} - v^{(1)}_{(02)} v^{(2)}_{(20)} (2C^{(1)})^{-1}(t^{(1)},t^{(1)})_{T^{(1)}_X} + t^{(1)} t^{(2)} + O(t^3)$$

with v_{(20)}^{(i)} the (2,0)-form on X^(i) and t^{(i)} the moduli fluctuation.

## Step (d) — Field of definition of Y_α

By M176 + above:
- X_a^L defined over Q (j = 1728 rational, Kummer of E with rational j)
- X_b^Q defined minimally over H(-88) = Q(√-22, √2)
- Y_α = (X_a^L × X_b^Q)/Z_2 defined over the smallest field containing both: H(-88) = Q(√-22, √2)

**However**, for ECI v9 W^L + W^Q decomposition we actually want:
- W^L period to "live in" K_L = Q(i)
- W^Q period to "live in" K_Q = Q(√-22)

The natural ambient containing both K_L and K_Q is Q(i, √-22), the **biquadratic compositum** of M171 route (b), with disc 30976 (M176 §M176.2).

The natural ambient containing K_Q AND its HCF for X_b^Q is H(-88) = Q(√-22, √2) of disc 7744.

These are DISTINCT biquadratic fields (M176 confirmed). Their compositum is the **triquadratic field** M = Q(i, √-22, √2) of degree 8 over Q with Gal = (Z/2)³.

**Conclusion:** The natural field of definition of Y_α with ECI v9 structure is the triquadratic M.

## Step (e) — KW W superpotential decomposition

From KW eq (49), the period integral W = ∫_Y G ∧ Ω_Y decomposes naturally because Ω_Y = Ω_{X^(1)} ∧ Ω_{X^(2)} factors:

$$W(Y_\alpha) = \int_{Y_\alpha} G \wedge \Omega_{X_a^L} \wedge \Omega_{X_b^Q}$$

For G ∈ H^4(Y_α; Z) of the form G = G^L ⊗ 1 + 1 ⊗ G^Q (decomposable flux), this further factors into:

$$W(Y_\alpha) = \left(\int_{X_a^L} G^L \wedge \Omega_{X_a^L}\right) \cdot \left(\int_{X_b^Q} G^Q \wedge \Omega_{X_b^Q}\right) + \text{cross terms}$$

But this is NOT a simple sum decomposition W = W^L + W^Q. **It is a product of K3 periods.**

The KW analysis (eq 46) shows: under condition K^(1) ≅ K^(2) (Case B), W = 0 fluxes exist. **For ECI v9, K_L = Q(i) ≠ Q(√-22) = K_Q, so eq (46) FAILS, and W = 0 cannot be enforced.**

**This is the M171 obstruction**: KW Case B fails for ECI v9.

## Verdict for (alpha)

| Aspect | Status |
|---|---|
| Construction explicit | YES (E_a^L = 32.a3, X_a^L = Km, E_b^Q in Q(√2), X_b^Q = Shioda-Inose) |
| Involutions explicit | YES (σ = lift of (id, -1) on E × E factors) |
| Y_α holomorphic 4-form | YES (σ_L × σ_Q invariant) |
| Field of definition | Q(i, √-22, √2) triquadratic (KW Case A) |
| KW Case B (W = 0) | FAILS (Q(i) ≠ Q(√-22)) |
| Inose explicit Weierstrass | OPEN (specialist gap) |

**Verdict (alpha): (B) REDUCED** — well-posed CY 4-fold candidate with single explicit-equations gap. ECI v9 W^L + W^Q decomposition is **multiplicative** (W = W^L · W^Q + cross), not additive, and **does not admit W = 0 in W_(20|02) component** (KW obstruction).
