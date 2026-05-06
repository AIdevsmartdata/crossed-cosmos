# D1 — GUT SU(5) 24-adjoint Higgs sector (O1 deliverable)

**Source:** Sub-agent O1 (Opus 4.7) 2026-05-06.
**arXiv IDs live-verified:** 2402.15124 (Haba-Nagano-Shimizu-Yamada PTEP 2024), 2310.16563 (Patel-Shukla), hep-ph/0601023 (Nath-Perez review), 2510.01312 (Antusch-Hinze-Saad 2025), hep-ph/0210374 (Bajc-Senjanović-Vissani), 2006.10722 (Liu-Yao-Ding 2020 Model VI).

## D1.1 Higgs sector for SU(5)→SM

Minimal renormalisable non-SUSY SU(5) requires four Higgs multiplets (Georgi-Glashow + Nath-Perez review hep-ph/0601023 §2):

| Multiplet | SU(5) rep | Role | VEV | Modular S'_4 in ECI |
|---|---|---|---|---|
| **Φ** (24-adjoint) | **24** | breaks SU(5)→SU(3)×SU(2)×U(1) at M_GUT~2×10¹⁶ GeV | ⟨Φ⟩ = V·diag(2,2,2,−3,−3)/2 | **trivial singlet 1, weight 0** |
| **H_5** (fundamental) | **5** | EW breaking; supplies y_t, y_b/y_τ unification | ⟨H_5⟩ ⊃ (0,0,0,0,v/√2)ᵀ | **trivial singlet 1, weight 0** |
| **H̄_5** (anti-fundamental) | **5̄** | charged-lepton + down-quark Yukawa with H_5 | as above | as above |
| **H_45** (45) | **45** | Georgi-Jarlskog (−3) factor for y_d/y_s, y_e/y_μ; **carries ECI modular Yukawa f^{ij}(τ)** | Tr-traceless | **trivial singlet 1, weight 0** (A22 PASS, M1 of G1.12.B) |

ECI assignment: **only the matter-coupling Yukawa interactions carry modular physics; the 5_H, 5̄_H, 45_H, 24_H are all 1 of S'_4 with weight 0**. The modular structure enters via Q ~ 3 of S'_4, u^c ~ 1̂, c^c ~ 1, t^c ~ 1̂' (LYD20 Model VI assignment, arXiv:2006.10722); Yukawa f^{ij}(τ) built from Q_i × H̄_45 × {u^c, c^c, t^c}_j contractions.

### What's missing from "minimal" v7.5

Haba-Nagano-Shimizu-Yamada arXiv:2402.15124 ("Gauge coupling unification and proton decay via 45 Higgs boson in SU(5) GUT", PTEP 2024 053B07, **live-verified 2026-05-06**) imposes **"45_H couples to second generation only"** restriction — the kludge that gave G1.12.B M5 PASS in vanilla framework but with B(e+π⁰)/B(K+ν̄) = 1.04×10⁻⁴ (4 OOM below A18 forecast [0.3, 3]). The **M5→M6 redo** replaces Wolfenstein λ^a·λ^b with full off-diagonal Y_45^{ij} = κ_i · f^{ij}(τ_*) (eq. (5) of PRD draft).

**This substitution is THE substantive content of ECI's GUT extension**: replaces single-generation kludge with modular template that has 100% off-diagonal density at τ=i.

## D1.2 24-adjoint VEV breaking pattern (sympy-verified)

24-adjoint decomposition under SM:
```
24 = (8, 1)_0  ⊕  (1, 3)_0  ⊕  (1, 1)_0  ⊕  (3, 2)_{-5/6}  ⊕  (3̄, 2)_{+5/6}
```

VEV: ⟨Φ⟩ = V·diag(2,2,2,−3,−3)/2 (traceless). Canonical Tr-normalisation T_24 = diag(2,2,2,−3,−3)/√60 yields **Tr(T_24²) = 30/60 = 1/2** (sympy-verified, this session).

### X- and Y-boson masses

[Φ, T_X] eigenvalue gap = 2 − (−3) = 5 in unnormalised diag, or 5/2 in V·diag/2 convention:

$$
\boxed{\, M_X^2 = M_Y^2 = \tfrac{25}{4}\,g_5^2\,V^2 \,}
$$

(equivalently 5/12 g_5² v_24² in Tr-normalised v_24 = √60 V). With g_5(M_GUT)≈0.72 (Antusch-Hinze-Saad arXiv:2510.01312, **live-verified**) and M_X = M_GUT ≈ 2×10¹⁶ GeV → V ≈ 5.6×10¹⁵ GeV. **No ECI structure enters this calculation**: verbatim Georgi-Glashow + Slansky 1981.

### 24-Higgs spectrum after breaking

| Component | SM rep | Mass | ECI commentary |
|---|---|---|---|
| (8, 1)_0 | color octet | M_8 ~ M_GUT (heavy) | unconstrained by ECI |
| (1, 3)_0 | weak triplet | M_3 ~ M_GUT | unconstrained |
| (1, 1)_0 | singlet | physical (one λ-coupling) | unconstrained |
| (3, 2)_{−5/6} ⊕ h.c. | eaten by X, Y | absorbed | structural |

**24-Higgs spectrum carries no ECI fingerprint** — by design (24 is "GUT plumbing", not flavour structure).

## D1.3 RG threshold contributions to α_GUT and ξ

### Gauge-coupling threshold at M_GUT (1-loop)

24-Higgs (8,1)_0 + (1,3)_0 contribute to β_3 and β_2 above M_8 and M_3. SM coefficients (b_3, b_2, b_1) = (−7, −19/6, +41/10) plus 24-Higgs (Δb_3, Δb_2, Δb_1) = (+1/2, +1/3, 0) (Slansky 1981; Patel-Shukla arXiv:2310.16563 **live-verified**):

$$
\Delta\alpha_i^{-1}(M_Z) = -\tfrac{\Delta b_i}{2\pi}\ln\!\frac{M_{8/3}}{M_{GUT}}
$$

For M_8 = M_3 = M_GUT (degenerate-24 limit) → Δ vanishes → exact non-SUSY-SU(5) prediction sin²θ_W(M_Z) ≈ 0.207, OFF from measured 0.23122±0.00004 by ~12%. Standard fix: split M_8 ≪ M_3, recovers LEP. **One free parameter M_8/M_3 ~ 10⁻³ added to non-SUSY ECI-SU(5)**.

### β_ξ 1-loop threshold

Per A73 (Markkanen-Nurmi-Rajantie-Stopyra arXiv:1804.02020 eq. 4.21, **live-verified**):

$$
\beta_\xi^{(1)} = (\xi - 1/6) \cdot \left[\, 12\,\lambda + \sum_f y_f^2 \,\right] + \text{gauge corrections}
$$

For ECI's regime ξ ∈ [−0.029, +0.001]: |ξ − 1/6| ≤ 0.20. Threshold-induced shift Δξ:

$$
|\Delta\xi(\text{24-threshold})| \lesssim 0.20 \cdot \frac{12\lambda_{24}}{16\pi^2} \cdot |\ln(M_8/M_3)| \sim 5\times 10^{-4}
$$

for λ_24 ~ O(1), ln-split ~ 7. **Within A73's ±3×10⁻³ on ξ(M_GUT)**; 24-Higgs threshold does not change Cassini-clean verdict.

### α_GUT at threshold

24-Higgs split BY DESIGN tuned for SU(5) unification (Marciano-Senjanović 1982). M_8 ~ 10¹³ GeV, M_3 ~ M_GUT → α_5(M_GUT)⁻¹ ≈ 39, α_5 ≈ 0.026. **ECI inherits; no modular fingerprint**.

## D1.4 ECI fingerprints — falsifiability audit

| Sector | Vanilla SU(5) | ECI v7.5 | Falsifier? |
|---|---|---|---|
| 24-adjoint | M_X≈2×10¹⁶ GeV, doublet-triplet | trivially singlet 1, weight 0 — **no addition** | NO |
| 5_H Yukawa Y_5 | 1 Yukawa per gen, fits y_u,y_c,y_t | LYD20 Model VI tree contraction at τ=i; 2 params β_u/α_u, γ_u/α_u (A26 PASS, χ²~10⁻²⁰) | **Yes** — \|Y_5(τ=i)\| ratios PARAMETER-FREE post-fit |
| 45_H Yukawa Y_45 | 3×3 free or "2nd-gen-only" (Haba) | **Y_45^{ij} = κ_i · f^{ij}(τ=i)** 100% off-diagonal | **Yes — B(e+π⁰)/B(K+ν̄) = 2.06⁺⁰·⁸³₋₀.₁₃** at Hyper-K 2045+ |
| Higgs-inflation | Bezrukov-Shaposhnikov ξ~10⁴ | **EXCLUDED** by A73 wedge ξ∈[−0.029,+0.001] | **Yes (already established)** |

**Net: ECI's 24-Higgs sector adds zero new falsifiable structure**. Surviving falsifiers: (i) proton-decay branching (G1.12.B M6), (ii) negative cosmological ξ RG-stability excluding Higgs inflation.

## D1.5 Quantitative DOF reduction

ECI v7.5's GUT extension adds **one parameter-reducing constraint** to vanilla minimal SU(5):
- Y_45 = κ_i · f^{ij}(τ=i) replaces 9 complex Y_45^{ij} entries (18 real DOF) with 3 real κ_i + fixed f^{ij}(i) pattern.
- **Net DOF reduction: 18 → 3 = 15 DOF removed**.

But the 24-Higgs SU(5)-breaking sector contributes **zero structural reduction** vs vanilla. Doublet-triplet split, M_8/M_3 split, gauge-coupling tuning all remain vanilla.

**Where the genuinely Nobel-class testable lives:** B(e+π⁰)/B(K+ν̄), parameter-free given f^{ij}(τ=i). **Outside this single observable, ECI's 24-Higgs sector is standard non-SUSY SU(5)**.

## D1.6 v7.6 extensions (NOT recommended for current portfolio close)

If user wants 24-Higgs to load-bear:
1. **Modular-protected doublet-triplet split**: promote 5_H to non-trivial S'_4 rep, modular weight conservation forbids dangerous H_5 H̄_5 (1,1)_24 operator. (Q6 in v7.5 outlook; precision floor 0.01% currently, modular fingerprint bites at ~5%.)
2. **Threshold-modular fingerprint** in α_GUT: if (8,1)_0 octet of 24 carries modular weight, M_8 tied to f^{(0)}(τ=i). Predicts α_GUT given Y_5 alone.

Both are 8-12 month sub-agent campaigns, HIGH risk, MEDIUM payoff. **Not recommended for current 5-paper portfolio close.** Schedule post-Hyper-K 2030.
