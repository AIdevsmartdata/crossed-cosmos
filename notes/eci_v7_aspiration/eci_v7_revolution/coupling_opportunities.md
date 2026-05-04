# ECI v7 — Coupling Opportunities Catalogue

**Six couplings**, ordered as in the brief Stage 3. Each entry: (i) conjecture in 3–5 lines, (ii) closest existing literature with verified arXiv ID, (iii) concrete next-step proof or experiment, (iv) effort estimate.

Status tags: **[VERIFIED]** read source, **[VERIFIED-UPSTREAM]** verified by an earlier agent in this project's audit trail, **[DERIVED]** computed myself, **[CONJECTURED]** educated guess, **[SPECULATIVE]** handwave.

---

## (a) NMC χ field × particle physics (neutrino sector / DM portal)

| Field | Content |
|---|---|
| **Conjecture** | The NMC scalar χ (mass m_χ ≲ H₀ ≃ 10⁻³³ eV, eci.tex A4) couples to SM neutrinos via a gravitational portal `(g_χν / M_P) χ ν̄_L ν_R`. Coupling g_χν is constrained by χ being non-thermal DM today (cosmological coherence length ≃ Mpc); cosmological imprint is a sub-percent suppression of structure on small scales (P(k) suppression at k > 0.1 h/Mpc). [CONJECTURED] |
| **Closest existing lit** | Generic ultralight scalar–neutrino coupling: Fardon–Nelson–Weiner 2003 (hep-ph/0309800, mass-varying neutrinos, [VERIFIED-UPSTREAM in eci.bib]). NMC quintessence as DM via gravitational interaction: Wolf 2025 (arXiv:2504.07679 [VERIFIED-UPSTREAM]) does NOT discuss this; closest contemporary is Karam-Sánchez-López-Terente Díaz 2026 (Karam2026 in eci.bib) on Palatini NMC. |
| **Next step** | (i) Compute the χν̄ν vertex from the NMC action `−½ξ_χRχ²`. The vertex is suppressed by `(ξ_χ/M_P²) · m_ν` — at ξ_χ ≃ 0.024 (Cassini saturation), m_ν ≃ 0.1 eV, this gives a coupling `g ≃ 10⁻²⁰` per Planck mass. (ii) Project onto cosmological structure-formation: Δ(P(k=0.1 h/Mpc))/P ≃ (g · χ₀/M_P)² ≲ 10⁻⁴ — sub-percent, *currently undetectable*. (iii) Forecast: would require LSST + DESI DR4 cross-correlation, ~2032+. |
| **Effort** | 6 weeks for the vertex calculation + cosmological projection. Then 6+ years for the experimental window. |
| **Yield assessment** | **Low**. Coupling is too small to be observable at currently scoped surveys. Park as future work. |

---

## (b) S′₄ doublet Hecke closure × Yukawa textures  ★ HIGHEST YIELD

| Field | Content |
|---|---|
| **Conjecture** | The S′₄ unhatted weight-2 doublet `Y₂^(2) = (Y_a, Y_b)` of NPP20 (arXiv:2006.03058, eq. 3.12 [VERIFIED-UPSTREAM E2]) is Hecke-stable with eigenvalue **λ(p) = 1+p** for p ∈ {3,5,7,11,13} — confirmed by sympy in `numerical_closure.py`. [VERIFIED-UPSTREAM E2]. The hatted doublet 2̂ at odd weights and the cusp triplet 3̂ at k=2 must satisfy analogous Hecke constraints; once these are also closed, the full Yukawa texture for S′₄ at level 4 is constrained beyond NPP20/LYD20/dMVP26 by Schur equivariance. The structural constraint reduces the number of free Yukawa parameters by (at least) the dimension of the Hecke-quotient kernel. |
| **Closest existing lit** | Modular flavour S′₄: NPP20 = arXiv:2006.03058 [VERIFIED-UPSTREAM] (Nucl.Phys.B 963, 2021, 115301); LYD20 = arXiv:2006.10722 [VERIFIED-UPSTREAM] (PRD 103, 056013); dMVP26 = arXiv:2604.01422 [VERIFIED-UPSTREAM, no journal-ref yet] (quark fit with canonical-Kähler effects). Hecke operators on Γ(N): Diamond-Shurman 2005 Ch.5; on Γ_0(N) Maass forms: Bruinier-Ono-Rhoades 2008 = arXiv:0802.0963 [VERIFIED-UPSTREAM A2]. **No paper in this list tests Hecke closure on S′₄ doublets explicitly — E2 is the first.** |
| **Next step** | (i) Extend `numerical_closure.py` to cover the cusp triplet 3̂ at k=2 and the hatted 2̂ at k ∈ {3,5} (NPP20 §3.3 eq. 3.14). Estimate: 4 weeks sympy. (ii) Combine with dMVP26 quark fit: hold the modulus τ at the dMVP26 best-fit, impose Hecke-closure on the Yukawa matrices, recompute (m_u, m_c, m_t) and CKM. Estimate: 8 weeks sympy + RGE. (iii) Compare to PDG: target σ ≲ 1.5% on m_c/m_t. |
| **Effort** | 4–6 months total to a **publishable result**. |
| **Yield assessment** | **High**. v7 Paper-A and Paper-B target. The Hecke-closure constraint is genuinely novel (zero hits in arXiv search) and the link to PDG retrodiction is concrete. |

---

## (c) Bianchi V Hadamard state × inflationary tensor-to-scalar ratio r

| Field | Content |
|---|---|
| **Conjecture** | The SLE state on Bianchi V (B1 + E3, [VERIFIED-UPSTREAM] for the leading-order Hadamard property; Dunster slope −1.19±0.07 numerically confirmed via arXiv:2412.12595) gives a *natural* vacuum on an anisotropic background. The induced 2-point function determines a tensor-to-scalar ratio `r = r(p_1, p_2, p_3)` where the p_i are the Kasner exponents (Bianchi V Taub: `(−1/3, 2/3, 2/3)`, B1 verified). For the isotropic limit `(0, 0, 0) → (1/3, 1/3, 1/3)`, r → standard FRW value; the Bianchi V correction is `Δr ≃ (anisotropy moduli) · r_FRW`. [SPECULATIVE — connection between Hadamard state and r-prediction not established in the literature.] |
| **Closest existing lit** | Bianchi V cosmology: Wainwright-Ellis 1997 (book, no arXiv); SLE construction on Bianchi I: Banerjee-Niedermaier 2023 = arXiv:2305.11388 [VERIFIED-UPSTREAM B1]; Brum-Them 2013 = arXiv:1302.3174 [VERIFIED-UPSTREAM]. **There is no paper in our trace that derives an r-prediction from a Bianchi V Hadamard state.** The c'_inflation = 0.108 working conjecture in eci.tex line 99 is from a *toy trace-ratio matching*, not from the Bianchi V geometry. |
| **Next step** | (i) Compute the 2-point function W_SLE(x, x') in the Bianchi V Taub vacuum at superhorizon scales. (ii) Decompose into scalar + tensor modes and read off the tensor power spectrum P_T(k). (iii) Compare to scalar power spectrum P_S(k) to give r = P_T/P_S. (iv) For the Taub axis ((−1/3, 2/3, 2/3)), the anisotropy moduli give a directional r — the prediction would be `r(direction)` not just a scalar r. |
| **Effort** | 6 months for the calculation; result might be `r ≃ r_isotropic · (1 + O(anisotropy))` with correction below LiteBIRD sensitivity δr ≃ 10⁻³. |
| **Yield assessment** | **Low**. Even if the calculation is doable, the Bianchi V correction is likely below LiteBIRD sensitivity. Honest claim: the v7 architecture is *consistent* with LiteBIRD r ≲ 10⁻³ axionic but does not predict a specific r-value. Park as v7.1 future work. |

---

## (d) Type-II crossed product × Connes–Marcolli SM spectral action  ★ SECOND-HIGHEST YIELD

| Field | Content |
|---|---|
| **Conjecture** | The modular flow `σ_t` on the type-II∞ crossed product `M̃(D) = M(D) ⋊_α ℝ` (eci.tex A1) interpolates between the cosmological IR observer (CLPW2023) and the SM-scale UV. The Connes-Chamseddine-Marcolli (CCM) spectral action `S_CCM = Tr(f(D/Λ))` gives the SM Lagrangian + GR at UV with a specific D = Dirac operator on the noncommutative geometry. Conjecture: `σ_t` ↔ RG flow on the CCM spectral triple `(A_F, H_F, D_F)`, with `σ_t` running the cutoff Λ. The Yukawa fixed-points of this flow at IR are exactly the Hecke-closed S′₄ doublets/triplets (coupling b). [SPECULATIVE — this is the unification claim. No published paper proves this.] |
| **Closest existing lit** | CCM SM spectral action: Connes-Chamseddine-Marcolli 2007 (cited as CCM2025 in eci.bib, [VERIFIED-UPSTREAM bib]); update arXiv:2403.11952 (Connes-Chamseddine 2024 SM) — *not verified live this session*. Modular flow as RG: Bisognano-Wichmann 1976 + Faulkner-Speranza 2024 (arXiv:2406.18558 [VERIFIED-UPSTREAM bib]). Maass-form approach to spectral triples: Marcolli-Lott 2018 (Q-lattices, no specific arXiv ID checked here). |
| **Next step** | (i) Construct an explicit semi-finite spectral triple `(A_F^c, H_F^c, D_F^c)` for the *cosmological* observer (CLPW + DEHK type-II envelope), as opposed to the original *SM* triple of CCM. (ii) Show that Tomita–Takesaki on this cosmological triple is equivalent to dimensional regularisation on the SM triple. (iii) Match the modular Hamiltonian eigenvalues to the SM Yukawa eigenvalues at the modular fixed point τ ≃ i. **This is hard mathematics.** |
| **Effort** | 12–18 months for a finite-truncation (low-rank) version (Numerical-result-3 of the manifesto); 3–5 years for a full version. Possibly never closes. |
| **Yield assessment** | **High if it closes**. Would be the conceptual bridge that *forces* the S′₄ Hecke closure of (b) from cosmological algebraic structure. v7 Paper-C target. **Do not over-promise**: this is the speculative anchor, not a deliverable. |

---

## (e) A₄ triplet × neutrino mass matrix

| Field | Content |
|---|---|
| **Conjecture** | The A₄ modular Yukawa programme (Feruglio 2017, level 3) constrains the lepton mass matrix via a triplet Y = (Y_1, Y_2, Y_3) of weight 2. ECI's Hecke-closure result (A2 morning, [VERIFIED-UPSTREAM] for the polyharmonic Maass framework + level-3 quasi-modular Eisenstein f_3 with λ(p)=1+p for gcd(p,3)=1) gives a *sum rule* on the triplet's q-expansion: `a_Y(p) = 1+p` for the triplet's Eisenstein component. This sum rule was not used in Feruglio's original fit. Imposing it adds at least one constraint, reducing the lepton-mass free-parameter count. |
| **Closest existing lit** | A₄ modular: Feruglio 2017 = arXiv:1706.08749 (cited in eci.bib bibliography but not verified live); recent A₄ neutrino fits: Petcov-Tanimoto 2023 = arXiv:2306.05730 (not verified live this session). Hecke closure on A₄ triplets: A2 morning agent's `[VERIFIED-UPSTREAM]` for level-3 Eisenstein. |
| **Next step** | (i) Identify the A₄ triplet at level 3, weight 2 (it lives in the Eisenstein part of M_2(Γ(3))). (ii) Compute its q-expansion via sympy and verify Hecke closure with λ(p) = 1+p. A2 indicated this is already ~done numerically; redo cleanly with full S′₄-style write-up. (iii) Compare to Feruglio's lepton-mass fit; show how the Hecke constraint sharpens the prediction for `Δm²_atm/Δm²_sol`. |
| **Effort** | 3–4 months. |
| **Yield assessment** | **Moderate**. Less novel than (b) — the A₄ programme has been worked over many times. But it's a clean, low-risk application of the Hecke-closure framework to neutrinos that complements (b) on the lepton side. Could be a short PLB or PRD paper. |

---

## (f) Faulkner–Speranza modular bound × Krylov complexity (Fan 2022 / Parker 2018)

| Field | Content |
|---|---|
| **Conjecture** | The FS24 modular GSL `dS_gen/dτ ≥ 0` (arXiv:2406.18558 [VERIFIED-UPSTREAM bib]) and the Parker et al. 2018 universal Krylov bound `b_n ≃ πn` (arXiv:1812.08657 [VERIFIED-UPSTREAM]) jointly give: on a type-II∞ algebra with semi-finite trace, the *anomalous-dimension* of any operator under the modular flow `σ_t` is bounded by `γ_O ≤ 2π · (Krylov diameter)^{-1}`. This is an algebraic version of the Maldacena-Shenker-Stanford bound `λ_L ≤ 2π T_H`. [CONJECTURED — the joint-application has not been published.] eci.tex §sec:mss-shadow already establishes the *modular shadow* connection. |
| **Closest existing lit** | FS24 = arXiv:2406.18558 [VERIFIED-UPSTREAM bib]; Parker et al. = arXiv:1812.08657 (PRX 9 041017) [VERIFIED-UPSTREAM]; Fan 2022 (Krylov complexity for QFT, arXiv:2208.09844, *not verified live this session* — flag if cited). MSS chaos bound: arXiv:1503.01409 (Maldacena-Shenker-Stanford 2015). |
| **Next step** | (i) Restate the FS24 bound on a type-II∞ Krylov-truncated subalgebra. (ii) Show that the bound `γ_O ≤ 2π / d_Krylov` follows. (iii) Apply to the SM: at the SU(3) × SU(2) × U(1) gauge sector, compute the Krylov diameter on a finite lattice and check whether the anomalous dimension of, e.g., the strange-quark mass operator satisfies the bound at the QCD scale. |
| **Effort** | 6–9 months. |
| **Yield assessment** | **Moderate**. Could yield a math-physics paper (Comm.Math.Phys. or Lett.Math.Phys.) of structural value, but no direct experimental discriminator. Park as v7.1 follow-up. |

---

## Summary table — yield × effort × novelty

| Coupling | Novelty | Effort | Yield | v7 priority |
|---|---|---|---|---|
| (a) NMC χ × neutrinos / DM portal | Low | 6 weeks + 6 yr expt | Low | Park |
| **(b) S′₄ doublet × CKM Yukawa** | **High** | **4–6 months** | **High** | **Paper-A + Paper-B** |
| (c) Bianchi V × inflation r | Moderate | 6 months | Low (sub-LiteBIRD) | Park to v7.1 |
| **(d) Type-II × CCM spectral action** | **High** | **12–18 months** | **High if closes** | **Paper-C (companion)** |
| (e) A₄ × neutrino mass matrix | Moderate | 3–4 months | Moderate | Short PLB/PRD |
| (f) FS24 × Krylov × SM γ_O | Moderate | 6–9 months | Moderate | Park to v7.1 |

**Two strongest = (b) and (d).** (b) is closable in 4–6 months and is the v7 headline. (d) is the architectural anchor; v7 ships with it as an open companion programme, not a closed result.
