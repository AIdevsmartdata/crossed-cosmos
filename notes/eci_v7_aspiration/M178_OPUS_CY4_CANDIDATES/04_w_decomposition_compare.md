# M178 sub-task 4 — Comparison W^L + W^Q decomposition across (α), (β), (γ)

## ECI v9 target structure

ECI v9 framework requires (per the M171/M173/M177 thread) a **two-modulus** F-theory-type vacuum structure with:
- Lepton sector: τ_L = i ∈ Q(i), W^L period
- Quark sector: τ_Q = i√(11/2) ∈ Q(√-22), W^Q period

The total flux superpotential should ideally factor as:

$$W_{\text{total}} = W^L(\tau_L) + W^Q(\tau_Q) + W^{\text{cross}}(\tau_L, \tau_Q)$$

with W^{cross} either zero (clean factorization) or a small mixing term.

## (α) Borcea-Voisin Y_α = (X_a^L × X_b^Q)/Z_2 — KW eq (49)

From M178 sub-task 1 + Kanno-Watari verbatim eq (49):

$$\Omega_{Y_\alpha} = \Omega_{X^L} \wedge \Omega_{X^Q}$$

with KW expansion:
$$\Omega_{Y_\alpha} = v^L_{(20)} v^Q_{(20)} + (v^L_{(20)} t^Q + t^L v^Q_{(20)}) + \text{higher}$$

Period integral:
$$W(Y_\alpha) = \int_{Y_\alpha} G \wedge \Omega_{Y_\alpha}$$

For decomposable flux G = G^L ⊗ 1 + 1 ⊗ G^Q ∈ H^2(X^L) ⊕ H^2(X^Q) ⊂ H^4(Y_α):
- The first term G^L ⊗ 1 paired with v^L_{(20)} ⊗ v^Q_{(20)} gives ∫_{X^L} G^L ∧ v^L_{(20)} times a period of v^Q_{(20)}
- This is a **PRODUCT** structure: W = W^L · W^Q + cross terms

**This is NOT a sum decomposition W = W^L + W^Q.** KW's superpotential is **multiplicative** in the K3 periods.

KW Case A vs B for ECI v9:
- ECI v9 satisfies eq (45) trivially: ρ^(1)_{(20)}(K_0^(1)) = ρ^(2)_{(20)}(K_0^(2)) = Q (both K_0^(i) = Q since K^(i) imag quadratic, totally imaginary, K_0 = real subfield)
- ECI v9 satisfies ρ^(1)_{(20)}(K^(1)) ≠ ρ^(2)_{(20)}(K^(2)) since K^(1) = Q(i) ≠ Q(√-22) = K^(2)
- → KW Case A: DW = 0 fluxes possible, W = 0 IMPOSSIBLE in W_(20|20) component (M171)

**Status (α) for W^L + W^Q:** The KW formula is multiplicative, not additive. **DOES NOT match ECI v9 W^L + W^Q sum target.** And W = 0 is obstructed (Case B fails).

## (β) V_4-orbifold — three sub-cases

From M178 sub-task 2:
- (β1) collapses to (α) Galois descent → same multiplicative period structure
- (β2) generic V_4-equivariant CY 4-fold → no defined periods to ECI v9 anchors
- (β3) Galois descent obstructed by ECI v9 anchor selection

**Status (β) for W^L + W^Q:** No improvement over (α). Either equivalent or unconstructed.

## (γ) Rank-4 CM K3 Km(E_1 × E_2) — single K3 with biquadratic CM

From M178 sub-task 3:

X_γ = Km(E_1 × E_2) is a K3 surface (dim 2), NOT a CY 4-fold. To get a CY 4-fold from X_γ we need additional structure.

### Option (γ1): X_γ × T^2 (no involution)

Y_γ = X_γ × T^2 is a CY 4-fold (Calabi-Yau if T^2 has trivial canonical, true). But this is a TRIVIAL fibration; not a "Borcea-Voisin" non-symplectic quotient. The W superpotential here is:

$$W(Y_{\gamma_1}) = \int_{Y_{\gamma_1}} G \wedge \Omega_{X_\gamma} \wedge dz_{T^2}$$

For G ∈ H^4(Y_γ_1) decomposable:
- W = ∫_{X_γ} G^X ∧ Ω_{X_γ} · (T^2 period)

The periods of Ω_{X_γ} take values in H^{2,0}(X_γ) ⊗ Q ≅ Q(i, √-22) — biquadratic CM field.

**Key observation:** For G^X chosen in T(X_γ) ⊗ Q (transcendental flux), the period decomposes Q-linearly via the biquadratic structure:

$$Q(i, √-22) = Q ⊕ Q·i ⊕ Q·√-22 ⊕ Q·(i·√-22)$$

The period integral W^L^Q := ∫_{X_γ} G^X ∧ Ω_{X_γ} can be written as:

$$W^L^Q = w_0 + w_i · i + w_{Q} · √-22 + w_{LQ} · i√-22$$

with w_0, w_i, w_Q, w_{LQ} ∈ Q (rational coefficients given by lattice pairings).

**This DOES factor naturally**: project onto the Q(i)-component and Q(√-22)-component:
- W^L := w_0 + w_i · i ∈ Q(i)
- W^Q := w_0 + w_Q · √-22 ∈ Q(√-22) (with shared w_0)

But **W ≠ W^L + W^Q** in general (the projection involves overlapping w_0).

### Option (γ2): Borcea-Voisin (X_γ × E_3) / Z_2 with E_3 elliptic curve

For Y_γ_2 to be a CY 4-fold via Borcea-Voisin:
- Need non-symplectic involution σ_γ : X_γ → X_γ acting as -1 on Ω_{X_γ}
- And (-1) on E_3
- Y_γ_2 = (X_γ × E_3) / ⟨σ_γ × (-1)⟩ smooth resolution

**Existence of σ_γ:** Garbagnati-Sarti 2008 ("On symplectic and non-symplectic automorphisms of K3 surfaces") study K3 surfaces with non-symplectic automorphisms; in particular K3 with order-2 non-symplectic involution and CM action. For rank-4 transcendental lattice, such involutions exist when the CM type has appropriate signature.

For T(X_γ) ⊗ Q ≅ Q(i, √-22) with biquadratic CM, the complex conjugation on the K-action gives an involution. **Specifically:**
- Q(i, √-22) has 4 embeddings into C, paired by complex conjugation as: σ_0 = id ↔ σ_3 = i ↦ -i, √-22 ↦ -√-22 ; σ_1 = i ↦ i, √-22 ↦ -√-22 ↔ σ_2 = i ↦ -i, √-22 ↦ √-22
- The involution τ : i ↦ -i on K induces a non-symplectic involution on T(X_γ) ⊗ Q (acts as -1 on the (2,0)-component since complex conjugation on Hodge structure flips (2,0) ↔ (0,2))

So σ_γ = (i ↦ -i)-induced involution on X_γ = Km(E_1 × E_2) corresponds to (P_1, P_2) ↦ (-P_1, P_2) on E_1 × E_2 (since complex conjugation on E_1 = (-1) action). 

**Action on Ω_{X_γ}.** Same as (α): σ_γ*Ω = -Ω. Non-symplectic. ✓

**Y_γ_2 = (X_γ × E_3)/⟨σ_γ × (-1)⟩** is a Borcea-Voisin CY 4-fold candidate.

### W decomposition for Y_γ_2

Ω_{Y_γ_2} = Ω_{X_γ} ∧ ω_{E_3} with ω_{E_3} the holomorphic 1-form on E_3.

Period: W(Y_γ_2) = ∫_{Y_γ_2} G ∧ Ω_{X_γ} ∧ ω_{E_3}

For decomposable G:
- W = (∫_{X_γ} G^X ∧ Ω_{X_γ}) · (∫_{E_3} G^{E_3} ∧ ω_{E_3})

This is **PRODUCT structure again, not sum**. Same as (α) — Borcea-Voisin always gives product periods.

The K3-period factor ∫_{X_γ} G^X ∧ Ω_{X_γ} **does** carry biquadratic CM Q(i, √-22) (as opposed to (α)'s pair of separate Q(i), Q(√-22)).

### Comparison (γ1) vs (γ2) vs (α)

| Variant | Geometry | Ω_Y | W structure | Field of CM |
|---|---|---|---|---|
| (α) | (X_a^L × X_b^Q)/Z_2 | Ω_X^L ∧ Ω_X^Q | W^L · W^Q + cross | Q(i) AND Q(√-22) (separate) |
| (γ1) | X_γ × T^2 | Ω_X_γ ∧ dz | W^X_γ · W^T^2 | Q(i, √-22) (single biquadratic) |
| (γ2) | (X_γ × E_3)/Z_2 | Ω_X_γ ∧ ω_E_3 | W^X_γ · W^E_3 | Q(i, √-22) (single biquadratic) on K3 |

**Key insight:** (γ) variants put both Q(i) and Q(√-22) on a SINGLE K3 (X_γ), as a UNIFIED biquadratic CM field. This is structurally **different** from (α) which has two separate K3 sectors.

## ECI v9 fit assessment

### Does ECI v9 want sectorial (α) or unified (γ)?

**Arguments for (α) sectorial:**
- ECI v9 explicitly distinguishes lepton vs quark sectors with τ_L ≠ τ_Q
- Two independent moduli (M134 τ_L = i, M171 τ_Q = i√(11/2))
- Phenomenologically: lepton mixing (PMNS) and quark mixing (CKM) are distinct sectors
- Each has its own modular form (M_L = 4.5.b.a wt-5, M_Q = ?)

**Arguments for (γ) unified:**
- The biquadratic compositum Q(i, √-22) IS the natural ambient for K_L · K_Q = Q(i) · Q(√-22)
- A single CY 4-fold geometry is "more economical" than two-K3 product
- The cross-modular term in M173 (H¹⊗H¹) might be more naturally realized via biquadratic CM
- Marcolli's noncommutative geometry approach could favor a single F-theory base

### KW eq (47) status

Recall KW eq (47): K_0 := ρ^{(1)}_{(20)}(K_0^{(1)}) = ρ^{(2)}_{(20)}(K_0^{(2)}) is the equality condition for SUSY flux existence.

For ECI v9: K_L = Q(i), K_0^L = Q ; K_Q = Q(√-22), K_0^Q = Q. Both totally imaginary quadratic, both have K_0^{(i)} = Q. So K_0 = Q. **eq (47) is SATISFIED.**

This means **DW = 0 fluxes EXIST** in ECI v9, in BOTH cases (α) and (γ_2).

The W = 0 strengthening (eq 46) requires K^(1) ≅ K^(2) (Case B), which fails for both:
- (α): K^L = Q(i) ≠ Q(√-22) = K^Q ✗ Case B fails
- (γ_2): single K3 X_γ has CM by biquadratic Q(i, √-22), not a single quadratic K. **KW framework does not directly apply** since KW assumes attractive K3 (rank T_X = 2). γ_2 has rank T_X = 4, in KW §2.5 territory.

### KW §2.5 (non-attractive K3) for (γ_2)

KW page 11 verbatim (recalled from M171): **"we do not ask whether the Hodge structure on H¹(Z⁽¹⁾;ℚ) ⊗ H¹(Z⁽²⁾;ℚ) is CM-type."** Out-of-scope for KW.

KW §2.5 (eq 63): T_X ⊊ T_0 escape, requires non-attractive K3.

(γ_2) has X_γ non-attractive (rank T_X = 4, ρ = 18, 18 + 4 = 22 = b_2(K3)). KW §2.5 is APPLICABLE.

**This is a NEW result from M178** : (γ_2) sits in the KW §2.5 non-attractive regime, OPENS A ROUTE NOT EXPLORED in M171.

## Summary of W decomposition status

| Candidate | KW Section | DW=0 (eq 47) | W=0 (eq 46) | W = W^L + W^Q? |
|---|---|---|---|---|
| (α) | §2.4 (attractive Z_2) | YES | NO (Case B fails) | NO (multiplicative) |
| (β1) ≡ (α)/Q | §2.4 | YES | NO | NO |
| (β2) | not covered | open | open | open (unconstructed) |
| (β3) | obstructed | n/a | n/a | n/a |
| (γ_1) X_γ × T^2 | not BV-orbifold | KW n/a | KW n/a | NO (multiplicative) |
| (γ_2) (X_γ × E_3)/Z_2 | §2.5 (non-attractive K3) | OPEN | OPEN | NO (multiplicative) |

**Key finding:** None of the candidates gives ECI v9 a clean W = W^L + W^Q **sum** decomposition. All Borcea-Voisin-style constructions give **product** periods. This is intrinsic to the K3 × K3 / K3 × T² Calabi-Yau 4-fold geometry — not a defect of any specific candidate.

**ECI v9 framework needs to either:**
1. Accept multiplicative W^L · W^Q + cross structure (modify ECI v9 manifesto)
2. Use a fundamentally different CY 4-fold geometry (not Borcea-Voisin)
3. Reinterpret W^L + W^Q as additive in a different sense (e.g., effective superpotential after Kaluza-Klein reduction)
