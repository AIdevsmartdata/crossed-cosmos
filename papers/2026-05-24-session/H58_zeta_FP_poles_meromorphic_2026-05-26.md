# H58 — ζ_{Δ_FP}(s) poles + heterogeneous anchors verdict

**Verdict** : weak PLAUSIBLE 30-40%, strong FALSIFIED.

## Standard spectral zeta theory

For Δ non-negative elliptic on d-dim closed Riemannian (Seeley 1967, Ray-Singer 1971):
$$\zeta_\Delta(s) = \frac{1}{\Gamma(s)} \int_0^\infty t^{s-1} [\text{Tr}(e^{-t\Delta}) - \text{tr} P_0] dt$$

Small-t heat-kernel : Tr(e^{-tΔ}) ~ Σ a_k(Δ)·t^{(k-d)/2} → ζ_Δ has **simple poles at s = (d-k)/2**, k=0,1,2,.. with residues Res_{(d-k)/2} = a_k/Γ((d-k)/2).

## A/Ḡ caveats

(i) **Gribov horizon ∂Ω̄** : zero-modes at horizon, branson-Gilkey boundary SD doubles poles with half-integer entries.
(ii) **Infinite-dim ambient** : d_s ≠ topological, defined by short-t scaling Tr(e^{-tΔ_FP}) ~ t^{-d_s/2}.
(iii) **Cone singularity** : Ω̄ convex cone with codim-1 boundary, precise regime where fractal d_s arises.

## Candidate d_s vs anchors

| d_s | leading pole | pole list with boundary 1/2-steps | matches |
|-----|-------------|----|---|
| 2 (Greensite) | 1 | 1, 1/2, 0, -1/2, ... | none of fractional anchors |
| 8/3 | 4/3 | 4/3, 5/6, 1/3, -1/6, ... | near-miss -1/6 (wrong sign) |
| **10/3 (Gribov fractal H46)** | **5/3** | **5/3, 7/6, 2/3, 1/6, -1/3, -5/6** | **ξ★=2/3 ✓ + κ_FP=1/6 ✓** |
| 4 (naive 4D) | 2 | 2, 3/2, 1, 1/2, 0, ... | none |

Pour d_s = 10/3, pole sequence s_k = 5/3 - k/2. **s_2 = 2/3 = ξ★** et **s_3 = 1/6 = κ_FP** landent sur poles prédits.

## Heterogeneous origins (other anchors)

| Anchor | Mechanism |
|--------|-----------|
| κ_FP = 1/6 | SD a_2 of Δ_FP (Kostant) ✓ |
| ξ★ = 2/3 | spectral pole d_s=10/3 (if confirmed) |
| **β_YM = -11/24** | **a_4 SD coefficient (H51 STRUCTURAL)** ✓ |
| F∞ = 9/10 | K41 intermittency 1-1/10 (not SD) |
| c∞ = 1/4 | Bekenstein area-law (not SD) |
| sin²θ_W = 3/13 | empirical numerology / AdS_5/Γ |

## Verdict

- **Strong H58** (all anchors = ζ residues) : **FALSIFIED** by pole-counting.
- **Weak H58** ({κ_FP, ξ★, β_YM} = SD coefficients of Δ_FP, d_s=10/3) : **plausible**, partial.

## Discriminating lattice test

SU(2) β=2.4 L∈{8,12,16}, ~2 days:
1. Coulomb gauge fix (overrelaxation 1000 iter), build M_FP
2. Lanczos lowest 200 λ_i
3. Fit ρ(λ) ~ λ^{(d_s-2)/2} log-log on small-λ tail :
   - d_s=2 (Greensite) → ρ const
   - **d_s=10/3 → ρ(λ) ~ λ^{2/3}**
   - d_s=4 → ρ(λ) ~ λ
4. Cross-check Z(t) = Σ exp(-λ_i·t) ~ t^{-d_s/2}
5. **Discriminator** : d_s = 10/3 ± 0.1 supports {κ_FP, ξ★, β_YM} ζ-pole interpretation.

## Verified refs

1. hep-lat/0509054 Greensite-Olejnik-Zwanziger VERIFIED
2. hep-th/0306138 Vassilevich heat kernel manual VERIFIED
3. hep-th/9505061 Elizalde et al. ζ-regularization VERIFIED

INVALIDATED during verification : 0802.0577 (Müller torsion suggested) is actually Bermudez Dirac oscillator. Wrong ID.

## Author

Kévin Rémondière (ORCID 0009-0008-2443-7166)

## Links

[[H51_seeley_dewitt_minus_11_over_24_2026-05-26]]
[[H56_HypCST_Wick_pairing_closure_2026-05-26]]
