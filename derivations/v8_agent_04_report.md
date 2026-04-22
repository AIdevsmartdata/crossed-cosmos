# V8-agent-04: Landau order-parameter ↔ Θ(PH_k[δn])

**Verdict: α-DIFFERENT**

## Setup

Analogy tested: PH_1[δn] as Landau order parameter of a percolation-type
phase transition in a 2D Gaussian random field δn with tunable correlation
length ξ (Gaussian power spectrum P(k) ∝ exp(−k²ξ²)).

Libraries: NumPy/SciPy cubical β_1 proxy (GUDHI/Ripser unavailable).
Cross-check: Gaussian Kinematic Formula (Adler–Taylor 2007) analytic χ(ν).

Grid: 256×256, 10 realisations per ξ, scan ξ ∈ [0.2, 6.0] grid cells,
ν ∈ [−2.5, 2.5].

## Results

**Phase transition:** β_1^peak(ξ) decreases monotonically with ξ. The
percolation transition of the 2D GRF lies at ξ ≲ 0.2 grid cells — below
the scan range — consistent with bond-percolation theory (threshold ν ≈ 0,
correlation length diverges at ξ → 0 in the continuum limit). The
descending flank covers the full ξ range explored.

**Chameleon fit** Θ(ξ) = exp(−(ξ/ξ_c)^α) to the descending flank:

| Source | ξ_c (grid units) | α |
|---|---|---|
| Numerical β_1 proxy | 6.52 | **2.12 ± 0.02** |
| GKF analytic χ peak | 12.00 | **0.43 ± 0.08** |

**v5 M3 Barrow-anchored target:** α ∈ (0, 0.1], fiducial 0.095.

Neither the cubical homology proxy (α ≈ 2.1) nor the GKF analytic
cross-check (α ≈ 0.43) falls within the v5 M3 target band.

## Physical Interpretation

The GRF percolation transition produces a power-law decay of β_1^peak(ξ):
β_1 ∝ ξ^{−d} in d=2 (Morse theory on smooth fields), leading to a
stretched-exponential fit with α ~ 2 (quadratic exponent, equivalent to a
Gaussian envelope). The GKF analytic envelope gives α ~ 0.4 — smaller but
still 4× above the M3 ceiling.

Matching α ∈ (0, 0.1] would require an extremely flat (nearly power-law)
order parameter decay, inconsistent with the GRF percolation universality
class (α_perco ~ 4/3 in 2D). The chameleon activator α ~ 0.095 is a
phenomenological choice (solar-system screening) and does not arise
naturally from PH_k topology on a Gaussian density field.

## Verdict

**α-DIFFERENT**: extracted α ≈ 2.1 (numerical) / 0.43 (GKF) vs. v5 M3
target α ∈ (0, 0.1]. The analogy is suggestive but the quantitative
exponent does not match. Θ(PH_k) could function as an order parameter near
the percolation transition, but its shape exponent is set by GRF universality
(α ~ 0.4–2), not by the Barrow-NMC chameleon constraint (α ~ 0.095).

## Outputs

- `derivations/V8-agent-04-landau-phk.py` — full computation
- `derivations/V8-agent-04-landau-phk.png` — 3-panel figure
- `derivations/_results/V8-agent-04-summary.json` — machine-readable summary

## References

- Yip, Biagetti et al. 2024, arXiv:2403.13985
- Adler & Taylor 2007, *Random Fields and Geometry*
- D15-screening-profile.py (α_min constraint from Cassini)
- D18-fsigma8-PH-forecast.py (ALPHA_FID = 0.095)
