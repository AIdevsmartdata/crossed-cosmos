# D18b — Bias marginalisation / orthogonality test for the v6 ECI falsifier

**Date:** 2026-04-21
**Inputs:** `D18b-bias-marginalization.py` (Fisher), D18 survey specs
**Figure:** `figures/D18b-bias-orthogonality.pdf`
**Summary:** `_results/D18b-summary.json`

## Motivation

The v6 cosmological falsifier reads

    Δfσ_8(z)/fσ_8(z) |_ECI = ε_0 · Θ(PH_2[δn(z)]) · (1+z)^{-γ},
    Θ(x) = exp[-(x/x_c)^α],  α = 0.095, γ = 1.

DESI DR3 measures fσ_8(z) from ELG redshift-space distortions in
z ∈ [0.8, 1.6]. ELGs trace cosmic filaments — precisely the structures
carrying the PH_2 signal — and have a scale-dependent bias
b(z,k) = b_0(z) + b_k·k².  If the z/k-dependence of Θ is degenerate with
the bias nuisance, the ECI signal is absorbed in the b(z)-fit and the
falsifier dies.

## Method

Parameter vector θ = (ε_0, δb_0, δb_k) at fiducial
(0.02, 0, 0, α=0.095, γ=1). Bias shifts leak into the RSD-extracted
fσ_8 through the Kaiser monopole leakage coefficient

    L(z) = 1 / (b_0(z) + f(z)/3),    b_0(z) = 0.84 / D(z)  (DESI ELG).

Observable:

    fσ_8^obs(z) = fσ_8^ΛCDM(z) · [1 + δb(z,k_eff) · L(z)]
                                · [1 + ε_0 · Θ(z) · (1+z)^{-γ}].

Derivatives evaluated at fiducial; k_eff = 0.12 h/Mpc (effective RSD
scale for DESI ELG). Gaussian priors σ(b_0)=0.5, σ(b_k)=2 h⁻²Mpc²
(loose — conservative worst-case for orthogonality).

## Results

| Combo        | ρ(ε₀, δb₀) | ρ(ε₀, δb_k) | σ(ε₀)_fix | σ(ε₀)_marg | degradation |
|--------------|------------|-------------|-----------|------------|-------------|
| DR3          | −0.997     | −0.057      | 0.068     | 1.48       | 21.7×       |
| DR3 + Euclid | −0.998     | −0.057      | 0.055     | 1.48       | 26.8×       |

**ε₀ for S/N = 1**
- fixed-bias:  DR3 → 0.068,  DR3+Euclid → 0.055
- **marginalised: DR3 → 1.48,  DR3+Euclid → 1.48** (far outside the
  Cassini-allowed band ε₀ ∈ [0.012, 0.048] from D18/D15).

S/N at fiducial ε₀ = 0.02:
- fixed-bias:  DR3 = 0.29,  DR3+Euclid = 0.36
- marginalised: **both ≈ 0.01**.

## Why the degeneracy is catastrophic

α = 0.095 is so small that Θ(z) is nearly flat across the DESI ELG
range: Θ varies only from 0.40 (z=0.85) to 0.42 (z=1.55). The
redshift-kernel of the signal is therefore dominated by (1+z)^{-γ},
a smooth monotonic function.

The bias leakage kernel L(z) = 1/(b_0(z) + f/3) is *also* a smooth
monotone function of z (because b_0 ∝ 1/D(z) grows with z). Numerically,
over z ∈ [0.85, 1.75]:

    corr( Θ(z)·(1+z)^{−1},  L(z) ) = 0.99991.

The two kernels are ~parallel in z-space to four decimal places. Any
nominal ECI shift can be reabsorbed into an overall δb_0 with residual
< 1%. This is the geometric origin of ρ = −0.998.

The scale-term δb_k is *orthogonal* (|ρ| = 0.057), confirming the
analytic argument: a polynomial in k does not mimic a *flat in k*
modulation at fixed k_eff. But with a single effective scale per
redshift bin (which is what RSD delivers), b_k contributes negligibly.

## S/N(ε₀) sweep,  ε₀ ∈ [0.005, 0.05]

Marginalised S/N is linear in ε₀ (Fisher) with slope
1/σ(ε₀)_marg ≈ 0.68. Across the whole Cassini-allowed band (ε₀ ≤ 0.048)
the marginalised S/N stays below 0.033 — three orders of magnitude
below the JCAP gate.

## Verdict

**DEGENERATE** (max |ρ| = 0.998).
Impact on D18: **overrides** its conclusion for the *bias-free* forecast.
D18 reported S/N ≈ 0.3–0.5 at fiducial with fixed bias; marginalising
over a realistic DESI ELG bias model collapses the detection to
S/N ~ 10⁻². The falsifier as currently written is not actionable with
DR3 (or DR3 + Euclid DR1) RSD.

## Path forward

The degeneracy is driven by the *flatness of Θ* (tiny α) and the
smoothness of (1+z)^{−γ}. Mitigations — none of which are in scope
here, all require new derivations:

1. **Break the z-degeneracy**: replace the ansatz with one in which
   the topological kernel has structure on Δz ≲ 0.1 (e.g. Θ activated
   only at a specific persistence threshold tied to shell-crossing at
   z_* ≈ 1 — localised in z). A *sharp* feature cannot be absorbed in
   b_0(z) fit per-bin.
2. **Use the k-dependence**: measure P^ELG(k,μ,z) directly at multiple
   k-bins and fit Θ(PH_2;k) as a sharp activator at k_* ≈ 0.15, which
   *is* orthogonal to polynomial b(k) (|ρ(ε₀,b_k)|=0.057 even here,
   but the leverage requires a full-shape likelihood, not compressed
   fσ_8).
3. **Cross-correlate with an independent tracer** (LRG, QSO) whose
   bias evolves differently; the common ECI term appears in both while
   the bias nuisance does not.
4. **JHEP-fallback**: drop the cosmological-falsifier claim; retain
   the formal/PPN content only.

## Recommendation

The JCAP claim — as predicated on D18's fixed-bias forecast — does
not survive a realistic DESI ELG bias marginalisation. Before
submission, the falsifier must either (i) be re-written with a
z-localised Θ-feature, (ii) be recast as a full-shape P(k,μ,z)
likelihood, or (iii) be replaced by the JHEP-fallback decision.

The degradation is not a factor 2–5 (MIXED); it is a factor ~27
(DEGENERATE). This does not fit the "ambiguous" category.
