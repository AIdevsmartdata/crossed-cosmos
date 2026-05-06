---
name: M9 Three-model comparison table — ECI vs Wolf vs AKW
description: Full parameter/mechanism/fit/falsifier comparison for the three-way DESI dark energy contest
type: project
---

# Three-Model Comparison: ECI vs Wolf 2025 vs Antusch-King-Wang 2026

**Date:** 2026-05-06
**Owner:** Sub-agent M9
**Sources:** A69 SUMMARY (Wolf, live-verified), A70 likelihood_spec.md (ECI priors), akw_paper_analysis.md (AKW, live-verified), arXiv:2604.08449 abstract+HTML
**Hallu count:** 85 (unchanged)

---

## 1. Identity

| Field | ECI v7.5 | Wolf 2025 | Antusch-King-Wang 2026 |
|---|---|---|---|
| arXiv | (ECI v7.4 = 10.5281/zenodo.19686398) | 2504.07679 | 2604.08449 |
| Authors | Remondiere | Wolf, García-García, Anton, Ferreira | Antusch, King, Wang |
| Published | Submitted 2026-05-05 | PRL 135, 081001 (2025) | Preprint Apr 2026 |
| Primary motivation | Modular flavor + proton decay unified cosmology | DESI NMC scalar-tensor | DESI coupled quintessence |

---

## 2. Action / Lagrangian

### ECI v7.5 (Cassini-clean)
Jordan frame (Faraoni convention):
```
S = ∫d⁴x √(−g) [ −½(M_P² + ξ_χ χ²) R + ½(∂χ)² − V(χ) + L_matter ]
V(χ) = V₀ exp(−λ χ/M_P)
```
NMC present (ξ_χ) but constrained to Cassini-clean wedge |ξ_χ| < 0.024.

### Wolf 2025 (NMC large-ξ)
Jordan frame (Horndeski-G4 / Brans-Dicke):
```
S = ∫d⁴x √(−g) [ M_P²/2 · F(φ) R − ½X − V(φ) + L_matter ]
F(φ) = 1 − ξ (φ²/M_P²),  X = ∂_μ φ ∂^μ φ
V(φ) = V₀ + β φ + ½ m² φ²   (V₀ tuned, not sampled)
G(φ) = 1, J(φ) = 0   (no k-essence, no Galileon)
```
Best-fit ξ = 2.31 — far outside Cassini-clean wedge and outside KG-physical domain.

### Antusch-King-Wang 2026 (coupled DM-DE)
Einstein frame (minimal coupling to gravity):
```
S = ∫d⁴x √(−g) [ M_P²/2 R − ½(∇φ)² − V(φ) − m(φ) ψ̄ψ ]
V(φ) = V₀ + αφ   (linear, illustrative)
m(φ) = μ f(φ),  f(φ)/f₀ = 1 + βφ − γφ²
```
No ξ coupling to Ricci scalar. DM-DE interaction via field-dependent DM mass.

---

## 3. Free parameter spaces

| Parameter | ECI | Wolf-KG | AKW (illustrative) |
|---|---|---|---|
| H₀ | yes (uniform [50,90]) | yes | yes |
| ω_b | yes (BBN prior) | yes | yes |
| ω_c | yes | yes | yes |
| n_s | yes | yes | yes |
| ln(10¹⁰ A_s) | yes | yes | yes |
| τ_reio | yes (Planck prior) | yes | yes |
| ξ_χ (NMC) | yes, |ξ|<0.024 (Cassini gate) | yes, [−5, +0.20] (KG gate) | NO — model doesn't have ξ |
| λ (exponential V slope) | yes | NO — quadratic V | NO |
| χ₀/M_P (initial field) | yes | yes (φ_init) | yes (φ_init) |
| φ'_init (initial velocity) | implicit | yes | implicit |
| β (linear V term Wolf) | NO | yes | NO |
| m² (quadratic V term Wolf) | NO | yes | NO |
| α (linear V slope AKW) | NO | NO | yes |
| β_coupling (DM-DE coupling linear) | NO | NO | yes |
| γ_coupling (DM-DE coupling quadratic) | NO | NO | yes |
| **Total free params** | **9** | **11** | **~9 (illustrative; TBD full MCMC)** |

**Note:** AKW parameter count is from the illustrative phenomenological realization only.
A full MCMC fit with all datasets may have different parameterization. [TBD: read §3 for
full MCMC parameter list.]

---

## 4. Key physical mechanisms

| Mechanism | ECI | Wolf | AKW |
|---|---|---|---|
| Source of w(z) deviation from −1 | Quintessence rolling + exponential V | NMC ξ φ² R modifies G_eff | Coupling Q = −ρ_DM (d ln m/dφ) φ̇ shifts effective w |
| Phantom crossing (w < −1)? | NO — w_φ ≥ −1 always (canonical kinetic) | Effective (CPL-level); w_φ might not be < −1 in KG-physical regime | YES apparent phantom via w_eff ≠ w_φ without phantom field |
| Coupling to gravity | NMC ξ (small, Cassini-clean) | NMC ξ (large, Cassini-violating) | Minimal (ξ = 0) |
| DE-DM energy exchange | NO — separate conservation | NO — separate conservation | YES — explicit Q exchange rate |
| "Frozen field" initial condition required? | No explicit requirement | No explicit requirement | YES — frozen phase in radiation era mandatory for CMB evasion |
| KG-physical stability | PASSES (ξ < ξ_crit; F > 0 always) | FAILS at ξ = 2.31 (A56/M4 gate: φ → runaway unless CPL-effective) | PASSES (F = 1 always; no ghost risk from F) |
| Solar system constraint | Automatic (Cassini-clean by construction) | FAILS (requires new screening physics) | Automatic (minimal coupling; no 5th force from ξ) |
| UV motivation | Modular flavor S'_4, proton decay, CM anchor | Phenomenological | Phenomenological |

---

## 5. Fit quality to DESI DR2

| Metric | ECI | Wolf | AKW |
|---|---|---|---|
| log B vs ΛCDM | −1.37 (A41 baseline; full MCMC pending A71) | +7.34 ± 0.6 vs min. coupled scalar; [TBD vs ΛCDM directly] | [TBD: no log B reported; χ²=1.38 vs binned w(z) only] |
| Datasets used | DESI DR2+Planck 2018+Pantheon+ (A70) | DESI DR2+Planck 2018+ACT DR6+DES-Y5 SN | DESI DR2+CMB+Union3 SN (partial spec; [TBD]) |
| w_eff reported | Near −1 (ξ~0, Cassini-clean) | w₀ = −1.06, wₐ = −0.95 (CPL-effective) | w_eff ≈ −1.2 at z=1.0 → −0.9 at z=0.4 |
| G_eff(0)/G_N | ~1.00 (Cassini-clean) | 1.77 (4.3σ from GR) | ~1.00 (minimal coupling) |
| Cassini-compatible? | YES (by design) | NO (screening required) | YES (no NMC) |
| Full Bayesian evidence vs ΛCDM | [TBD: A71 result pending] | log B = +7.34 (vs min. coupled scalar) | [TBD: not computed in paper] |

---

## 6. Structural failure modes / consistency gates

| Gate | ECI | Wolf | AKW |
|---|---|---|---|
| KG-physical (F > 0, no runaway) | PASS | FAIL at ξ = 2.31 (A56, M4) | PASS (F = 1 fixed) |
| Cassini / solar system | PASS (|ξ| < 0.024) | FAIL (new screening physics needed) | PASS (ξ = 0) |
| Ghost-free kinetic (G > 0) | PASS | PASS (G = 1) | PASS (canonical kinetic) |
| CMB pre-recombination coupling small | Automatic (small ξ) | [TBD: Wolf doesn't analyze] | REQUIRED BY DESIGN — frozen field condition |
| UV completeness | Partial (S'_4 modular GUT) | None stated | None stated |
| Proton decay prediction | YES (B(p→e⁺π⁰)/B(p→K⁺ν̄) = 2.06) | None | None |
| H₀ tension addressed? | Partial (H₀ = 70.20 ± 5.74; A25) | YES (primary motivation) | [TBD: not stated explicitly] |
| S₈ tension addressed? | [TBD] | [TBD] | [TBD — DM-DE coupling can affect growth] |

---

## 7. Observable predictions for degeneracy breaking

(See also degeneracy_breaking_observables.md for full list)

| Observable | ECI signature | Wolf signature | AKW signature |
|---|---|---|---|
| w(z) shape | Near-ΛCDM (w ≈ −1), slow roll | CPL: w₀ < −1, wₐ large | w_eff crosses −1 (apparent phantom) |
| G_eff(z) | ~G_N (ξ ≈ 0) | 1.77 G_N today, scale-dependent | G_N (minimal coupling) |
| fσ₈(z) | Near-ΛCDM growth | Enhanced growth (G_eff > G_N) | Modified via DM energy injection |
| DM velocity dispersion | Unchanged | Unchanged | Modified (DM gains energy → warmer?) |
| ISW effect | Near-ΛCDM | Possibly enhanced | Modified by DM-DE coupling |
| CMB lensing | Near-ΛCDM | Enhanced | Modified at late times |
| Void statistics | Near-ΛCDM | Modified (5th-force-like enhancement) | Modified (DM density profile changes) |
| DM mass variation with redshift | None | None | YES — m_DM(φ(z)) varies |

---

## 8. Structural relationship to ECI axiom H8'

ECI's H8' axiom cites arXiv:2310.10369 (King-Wang 2023) for modulus stabilisation
at the fixed point τ = i, providing the dS-trap mechanism that grounds ECI's cosmological
constant prediction. The King-Wang in H8' is a pure modular-gravity paper.

The King-Wang in AKW 2026 is the SAME King (Stephen F. King, Southampton) and Wang (Xin Wang)
working in a completely different phenomenological regime: standard model Yukawa-inspired
coupling of DE to DM, no modular symmetry, no SUSY, no fixed-point stabilisation.

There is NO technical contradiction between ECI H8' and AKW 2026 — they are separate
research threads by the same authors. The AKW 2026 paper does not cite arXiv:2310.10369
in the abstract; their DESI-focused work appears to be a distinct phenomenological program.
[TBD: check full reference list of 2604.08449 for self-citation.]
