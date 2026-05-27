# RABENSTEIN-BODENDORFER-BUIVIDOVICH-SCHAEFER 2018 — REFIT cross-N
**Date** : 2026-05-24
**Author** : Kévin Rémondière (chercheur indépendant, Oloron)
**Reference** : Rabenstein, Bodendorfer, Buividovich, Schäfer, *"Lattice study of Rényi entanglement entropy in SU(N_c) lattice Yang-Mills theory with N_c = 2, 3, 4"*, **Phys. Rev. D 100, 034504 (2019)**, arXiv:1812.04279v2 (25 Oct 2019). Verified live via arXiv + PDF download.

## 1. Hypothesis under test
Standard prediction : C(l) ∝ (N²−1) at short distances (free-gluon count).
Alternative : C(l) ∝ (1−κ)(N²−1), κ = 1/(N(N−1)) = 1/(2|Φ⁺(SU(N))|).

Predicted ratios C(SU(N))/C(SU(2)) :
- Standard : 1 : 8/3 : 5 = 1 : 2.667 : 5.000
- Alternative : 1 : (8·5/6)/(3/2) : (15·11/12)/(3/2) = 1 : 4.444 : 9.167

## 2. Data extracted (paper §IV, Figure 3 plateau fits, page 6+8)
The paper gives explicit constant-value fits to the entropic C-function in the small-l (asymptotic freedom) regime, fitting all data points with l√σ < 1.1 (SU(2)), 1.3 (SU(3)), 0.7 (SU(4)) :

| N | C(plateau) | err | χ²/d.o.f. (paper) | source |
|---|---|---|---|---|
| 2 | 0.054 | 0.001 | ≈ 0.2 | Fig. 3 top |
| 3 | 0.173 | 0.005 | (n.r.) | Fig. 3 mid |
| 4 | 0.411 | 0.006 | ≈ 0.6 | Fig. 3 bot |

Lattice 16³×32, pseudo-heatbath + Cabibbo-Marinari, string-tension scale-setting (Lucini-Teper-Wenger 2005).
Configurations 24k–2.5M per (β, l) — see Table I.

## 3. Measured ratios vs predictions
- C(SU(3))/C(SU(2)) = **3.204 ± 0.110**
- C(SU(4))/C(SU(2)) = **7.611 ± 0.179**

| Prediction | SU(3) ratio | dev | SU(4) ratio | dev | χ² (2 dof) |
|---|---|---|---|---|---|
| Standard (N²−1) | 2.667 | **+4.9σ** | 5.000 | **+14.6σ** | 235.5 |
| (1−κ)(N²−1) | 4.444 | **−11.3σ** | 9.167 | **−8.7σ** | 202.4 |

**Both formally rejected** at >10σ overall significance. The alternative is marginally less bad in χ² but is on the *opposite* side of the data from standard (overshoots while standard undershoots).

## 4. Paper's own collapse C(l)/(N²−1)
The authors rescale by (N²−1) (Fig. 4) and claim short-distance collapse. Numerically :

| N | C/(N²−1) | C/[(1−κ)(N²−1)] |
|---|---|---|
| 2 | 0.01800 | 0.03600 |
| 3 | 0.02162 | 0.02595 |
| 4 | 0.02740 | 0.02989 |

Paper-normalization spread (max/min) = 1.52×. Alternative-normalization spread (excluding SU(2)) = 1.15× (better) ; including SU(2) = 1.39× (better than standard 1.52×). **Mild improvement** in collapse if SU(2) is included with the alternative.

## 5. Empirical scaling
Weighted fit C(N) ∝ (N²−1)^p over N=2,3,4 gives **p = 1.261**. Neither hypothesis (both p=1) is consistent. The empirical p > 1 reflects that C grows faster than linearly in (N²−1).

If SU(3) → SU(4) ratio is taken in isolation (paper warns SU(2) plateau is unreliable — abstract : *"results for SU(2) proved inconclusive, with inconsistent behavior across different lattice spacings"*) :
- Measured : C(SU(4))/C(SU(3)) = **2.376 ± 0.077**
- Standard : 15/8 = 1.875 → **+6.5σ off**
- Alternative : 13.75/6.667 = 2.062 → **+4.1σ off**

Even excluding the contested SU(2), the alternative is **rejected at >4σ** by the measured SU(3)→SU(4) jump.

## 6. Caveats
1. The three plateau fits are at *different* l√σ windows (1.1 / 1.3 / 0.7) — not strictly matched physical scale. The paper acknowledges this for SU(4) (need smaller l√σ to stay in asymptotic-freedom regime).
2. Lattice spacings a√σ are not jointly tuned ; SU(4) plateaus use a√σ ∈ [0.15, 0.22].
3. The α-interpolation cubic-spline integration error is not fully propagated into the quoted errors.
4. The paper itself (§IV) says : "we no longer distinguish data points with different values of lattice spacing. For small cut lengths, this plot **again confirms the scaling of entanglement entropy with N²−1**." — qualitative confirmation only, no χ² test of (N²−1) vs alternatives is performed by the authors.

## 7. Verdict
- The (1−κ)(N²−1) prediction with κ=1/(N(N−1)) is **rejected by Rabenstein 2018 plateau data at >4σ** even in the most favorable SU(3)→SU(4) sub-test.
- Standard (N²−1) is *also* statistically rejected (>6σ on the same sub-test), confirming that the lattice data shows a faster-than-linear growth in (N²−1) at the plateaus measured.
- The empirical exponent ≈ 1.26 sits between the two hypotheses ; the alternative is marginally closer to the data than standard, but both are formally excluded.
- The test is **discriminative** : neither prediction passes. The alternative is *less wrong* on the SU(3)/SU(4) sub-test (4.1σ vs 6.5σ) and on the collapse spread (1.39× vs 1.52×), but is *more wrong* on the SU(2) ratio (where the paper itself warns the SU(2) datum is unreliable).
- Honest conclusion : **the published plateau fits do not support the (1−κ)(N²−1) hypothesis as stated**. They suggest C(l) scales faster than (N²−1), which neither hypothesis predicts. A continuum-limit extrapolation (absent in the paper) is required before a clean verdict ; the present numbers reject both linear-in-(N²−1) laws.

## 8. Effort
Data extraction : 25 min (PDF parsed via Read tool ; explicit plateau values on Fig. 3 annotations + Table I configurations). No author contact required.
