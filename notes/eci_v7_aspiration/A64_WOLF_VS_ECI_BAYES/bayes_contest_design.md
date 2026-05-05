# A64 — Bayes contest full design

## 1. Two branches under test

### ECI-main (Cassini-clean wedge)
- Action: S = ∫d⁴x √(−g) [ −½(M_P² + ξ_χ χ²) R + ½(∂χ)² − V(χ) + L_matter ]
- Faraoni convention, Jordan frame, no Galileon kinetic term
- Free cosmo params: {H₀, ω_b, ω_c, n_s, A_s, τ}; NMC sector: {ξ_χ, m_χ, χ₀}
- **Prior on ξ_χ:** hard cutoff |ξ_χ| < 0.024 (uniform inside; zero outside). Justified by Cassini bound |ξ_χ|·(χ₀/M_P)² ≲ 6×10⁻⁶ at the assumption χ₀/M_P ≈ 0.016 (state explicitly in prior)
- Status: equivalent to ECI v7.4 with log B = −1.37 vs ΛCDM (A41 reference)

### ECI-V (Vainshtein large-ξ branch)
- Action: S_V = S_main + ∫d⁴x √(−g) [ J(χ) X² ] where X = ½(∂χ)²
- J(χ) = α_J / Λ_J⁴ with Λ_J the Galileon scale (free in [10⁻³, 10⁻¹] eV)
- **Prior on ξ_χ:** smooth super-Gaussian on [−5, +10], width σ_ξ = 3, exponent n=4 (flat-top, soft-edge)
- **Prior on α_J:** log-uniform in [10⁻², 10²]
- Vainshtein radius r_V = (ξ_χ M² / M_P²)^{1/3} · Λ_J⁻¹ — must satisfy r_V > 10 AU at solar system to evade Cassini
- Status: requires A56 (|ξ|<10) + new J(χ)X² backend

## 2. Datasets

Per A41 R2 spec:
- **Planck PR4** (NPIPE, Camspec or HiLLiPoP+LoLLiPoP — choose HiLLiPoP for consistency with A57)
- **DESI DR2** BAO (D_M/r_d, D_H/r_d, D_V/r_d at 7 effective z bins)
- **Pantheon+** SN-Ia Hubble diagram (uncalibrated, marginalize M_B)
- **KiDS-Legacy** S₈ + cosmic shear ξ_± (gives ECI-V leverage; sensitive to fifth force at small scales)
- Optional add-on (post-launch): LiteBIRD r constraint — discriminator if ECI-V predicts non-trivial B-mode signature

## 3. Sampler config

- **Backend:** NUTS via numpyro on JAX (matches A25, A57)
- **Emulators:** cosmopower-jax 0.5.5 with custom_log probe (A25 pattern); separate emulator for ECI-V branch with J(χ)X² Friedmann modification
- **Walkers:** 8 chains × 4000 warmup × 8000 production
- **Convergence:** Gelman-Rubin R̂ < 1.01 on all params; ESS > 400 per param
- **GPU:** RTX 5060 Ti, JAX patched per memo (jax_named_shape patch)

## 4. Bayes factor methodology

**Primary:** Savage-Dickey density ratio
- Test point: ξ_χ = 0 (ΛCDM-NMC limit) ⇒ log B(model vs ΛCDM)
- Cross-test: ξ_χ = 2.31 (Wolf central) ⇒ checks if ECI-V can recover Wolf
- Requires posterior density estimate at the test point — use kernel density (sklearn KDE, Silverman bandwidth)

**Secondary:** Thermodynamic integration (TI)
- 16 temperature steps β ∈ [10⁻⁴, 1.0] geometric
- 2000 samples per step
- Z = exp(∫₀¹ ⟨log L⟩_β dβ)
- Compute log B(ECI-main vs ECI-V) directly = log Z_main − log Z_V

**Cross-check:** SDDR vs TI must agree within ±0.5 log units. If discrepancy >1, flag and investigate (likely posterior multimodality in ECI-V).

## 5. Pre-registered hypotheses (frozen 2026-05-05)

| Hyp | Criterion | Interpretation |
|---|---|---|
| **H0** | log B(ECI-main vs ECI-V) > +1 | Cassini-clean wedge wins. Wolf signal is screening-fragile (vanishes when Galileon kinetic is properly normalized against solar-system data). ECI v7.4 confirmed in its current form. |
| **H1** | log B(ECI-V vs ECI-main) > +1 | Wolf large-ξ recovered inside ECI. ECI-main loses; we must absorb J(χ)X² Galileon as a canonical sector and re-derive Cassini compatibility via Vainshtein. v7.5 reformulation triggered. |
| **H2** | log B ∈ [−1, +1] | Tie. Neither branch decisively preferred. Add LiteBIRD r + DESI Y3 data; revisit Q3 2027. |
| **H3** (sanity) | log B(ECI-V vs Wolf-vanilla) consistent with A41 log B = +7.34 ± 0.6 reference (within ±2σ on aggregate) | Validates that ECI-V at large ξ_χ recovers Wolf's published signal. If FAILS, our likelihood implementation has a bug — DO NOT publish, debug instead. |

## 6. Contingency matrix

| Outcome | A56 | A57 | J(χ)X² backend | Action |
|---|---|---|---|---|
| All green | ✓ | ✓ | ✓ | Run A64 production; report log B; decide H0/H1/H2 |
| A56 fails (|ξ| numerics break) | ✗ | ✓ | — | Defer A64; restrict to Karam Palatini analytical sub-branch (R1 path) |
| A57 fails | ✓ | ✗ | ✓ | Run A64 with reduced model set (ECI-main + ECI-V only, no 11-model context) |
| J backend bug | ✓ | ✓ | ✗ | Sample ECI-main only; log B vs ΛCDM only; defer Wolf contest |
| H3 sanity fails | — | — | — | DO NOT report H0/H1; debug J(χ)X² implementation |

## 7. Reporting template (frozen)

A64 production run will report:
1. Posterior on (ξ_χ, α_J, Λ_J, H₀, S₈) for both branches
2. log B values: ECI-main vs ECI-V (primary), ECI-main vs ΛCDM, ECI-V vs ΛCDM, ECI-V vs Wolf-vanilla (sanity)
3. Goodness-of-fit per dataset (χ²/dof) for both branches
4. Vainshtein radius posterior in ECI-V (must be > 10 AU at >95% credibility for solar-system viability)
5. Hypothesis decision: H0 / H1 / H2 with criterion shown
6. Hallu count delta (must be 0 unless a verified citation issue surfaces)

## 8. ETA

- T+0 (today, 2026-05-05): A64 design seeded
- T+5d: A56 expected complete
- T+14d: A57 expected complete
- T+21d: J(χ)X² backend coded + Wolf-mock validation
- T+28d (~2026-06-02): A64 production run
- T+30d: A64 results paper (or pre-registered null report)
