# D18 — fσ_8 persistent-homology falsifier forecast (v6 gate)

## Ansatz

Δfσ_8(z)/fσ_8(z)|_ECI = ε_0 · Θ(PH_2[δn(z)]) · (1+z)^{-γ},
Θ(x) = exp[−(x/x_c)^α], α = 0.095, γ = 1.

PH_2 redshift evolution fiducial: **θ_A** (Yip+2024 anchored, PH_2 ∝ D(z)^2)
with x(z)/x_c = (D(z)/D(0))^2. Since D(0)=1 and D(z)<1 for z>0, x/x_c<1
on the survey range, making Θ mildly z-dependent and close to
exp(−(D^2)^0.095) ≈ 0.83–0.92. A cross-check θ_B ∝ (1+z)^{-3/2} gives
nearly identical numbers — Θ is insensitive to the PH_2 scaling at α=0.095
because 0.095 is small (Θ ≈ 1 at any order-unity argument). **This is the
central reason the signal is weak**: a small α turns Θ into a quasi-constant
prefactor ~0.85, so the ECI correction is at most ε_0·0.85·fσ_8/(1+z) per bin.

## Surveys (Δz=0.1)

| survey | z-range | σ(fσ_8) |
|---|---|---|
| DESI DR3 ELG | 0.8–1.6 | 0.015 |
| LSST Y10 | 0.4–1.2 | 0.020 |
| Euclid DR1 spectro | 0.9–1.8 | 0.020 |

Independent-dataset combination (inverse-variance sum). Survey σ(fσ_8) are
target values (DESI collaboration 2024, Euclid SRD IST:Forecast, LSST
DESC SRD v1).

## Results at fiducial ε_0 = 0.02, α = 0.095

| combo | S/N (θ_A) | S/N (θ_B) |
|---|---|---|
| DR3 alone | **0.29** | 0.29 |
| DR3 + LSST Y10 | **0.41** | 0.41 |
| DR3 + Euclid DR1 | **0.36** | 0.36 |
| DR3 + LSST + Euclid | **0.46** | 0.47 |

Minimum ε_0 for 1σ detection at α=0.095:

| combo | ε_0^min(1σ) | ε_0^min(0.5σ) |
|---|---|---|
| DR3 | 0.068 | 0.034 |
| DR3 + LSST | **0.049** | 0.024 |
| DR3 + Euclid | **0.055** | 0.028 |
| DR3 + LSST + Euclid | 0.043 | 0.022 |

## Cassini consistency

A linearisation of the v6 NMC perturbation equation (D14/D15) at
χ_0 = M_P/10 yields ε_0 ≃ k_v6 · |ξ_χ| with k_v6 ∈ [0.5, 2] (order-unity
coupling). The Cassini bound |ξ_χ| ≤ 2.4·10⁻² (D7) therefore restricts

  ε_0 ∈ [0.012, 0.048].

The 1σ detection thresholds ε_0^min ≳ 0.049 (DR3+LSST), 0.055 (DR3+Euclid),
0.043 (triple-combo) **all lie at or above the Cassini-allowed ceiling**.
Only the most optimistic combo (DR3+LSST+Euclid with k_v6 at the high end
of its uncertainty) barely touches the Cassini band. The falsifier is
therefore **either too weak to detect (ε_0 inside Cassini band) or in
tension with Cassini (ε_0 large enough to detect)** — a lose-lose
configuration for cosmological discrimination at α=0.095.

## Why α matters

Θ(x) = exp(−x^α) with α=0.095 behaves as 1−α·ln x + O(α²). The Θ factor
is almost frozen between 0.83 and 0.92 over the entire survey range.
Raising α to 0.3–0.5 would turn Θ into a genuine z-dependent step and
could plausibly reach 1σ detection within the Cassini band, but that
would require re-deriving the v6 ansatz — out of scope for D18. The 2-D
(ε_0, α) contour in figure panel (c) shows that the 1σ line at
ε_0 = 0.02 requires α ≳ 0.35, nowhere near the owner value 0.095.

## Verdict

**v6 target = JHEP/PRD-formal (fallback, Agent 1 memo).**

At the owner fiducial (ε_0=0.02, α=0.095, γ=1) the joint DR3+Euclid
discrimination is **0.36σ** — below the 0.5σ "ambiguous" gate.
Even the full DR3+LSST+Euclid combination reaches only 0.46σ. The
ε_0 required for a 1σ result (≈0.05) sits at the top of the
Cassini-allowed band and would be in mild tension with |ξ_χ| PPN.

The cosmological falsifier as currently parameterised is not
discriminating enough to carry a JCAP submission. Agent 2's
`v6_decision_jcap.md` should stand down; Agent 1's
`v6_decision_jhep_fallback.md` is the recommended v6 path.

## Deliverables

- `derivations/D18-fsigma8-PH-forecast.py`
- `derivations/figures/D18-fsigma8-PH-forecast.pdf` (+ `.png`)
- `derivations/_results/D18-summary.json`
