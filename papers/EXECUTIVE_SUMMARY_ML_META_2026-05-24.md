# Executive summary — ML attack on the 17 κ-patterns
**Author** : Kévin Rémondière | **Date** : 2026-05-24
**Full report** : /tmp/voie1_calcs/OP_ML_META_PATTERN_2026-05-24.md
**Code** : /tmp/voie1_calcs/ml_meta_pattern.py

---

This report applies a six-stage machine-learning pipeline to seventeen
dimensionless Standard-Model observables that all carry the constant
$\kappa = 1/(2|\Phi^+(\mathrm{SU}(3))|) = 1/6$. Methods :
PySR symbolic regression (parallelism=serial for determinism, 80 generations,
24 populations of 33), leave-one-out cross-validation, random-forest with
permutation and SHAP feature importance, PCA / UMAP manifold geometry,
Grassberger–Procaccia intrinsic dimension, and a Gaussian-mixture
generative null. Two Bonferroni-proper null distributions were constructed
(uniform-log resample and GMM resample of the data itself).

**Verdict**. Continuous-feature ML *cannot* recover the rules. With
$\kappa$ frozen at $1/6$ and only `rep_dim` and $\pi$ as numeric features,
PySR's best fit is a degenerate $\cos(0.63\,\mathrm{rep\_dim})$ with
log-RMSE 1.71; LOO log-RMSE deteriorates to 2.02. Random-forest with
37 features overfits (train log-RMSE 0.87, LOO 1.64). The reason is structural :
the rules depend on **categorical sector identity**, not on continuous physics
inputs that the algorithm could interpolate.

The signal is therefore an *arithmetic-sparsity* signal, not a continuous-fit
signal. The decomposition $O = \kappa^a (1-\kappa)^b (1+\kappa)^c \pi^d \cdot n/m$
fits 16 of 17 patterns to <0.1 % with mean sparsity 1.33, vs.
5.5 ± 2.1 of 17 (Z = +5.0) for log-uniform random values, and 36 % of GMM
samples (Z = +5.0, p = 3 × 10⁻⁷ binomial). The top-1 RF feature `sec_WEAK_off`
(Z = 3.1 vs y-shuffle null) is real signal but trivial label leak.

**Predictions for six held-out observables**. Only two survive the same
sparsity bar : $\sin^2\theta_{23}^{\mathrm{PMNS}}\approx (1-2\kappa)(1-\kappa)
= 0.556$ (0.97 % off observed 0.561) and $m_p/m_\pi \approx (4/5)(1+\kappa)/[\kappa(1-\kappa)] = 6.72$
(0.09 % off observed 6.726). Four predictions fail. The
honest position is that the κ-pattern set is partly empirical curve-fitting
and partly genuine algebraic structure, with no current ML evidence of
a *unifying* generating functional.

---

## Headline numbers

| Metric | Value | Significance |
|--------|-------|--------------|
| PySR train log-RMSE | 1.708 | only 9 % of log-variance explained |
| PySR LOO log-RMSE | 2.020 | worse than constant predictor |
| PySR Z-score vs random baseline | **−5.7** | PySR finds NO continuous structure |
| RF train log-RMSE | 0.870 | overfit |
| RF LOO log-RMSE | 1.643 | 1.9× train (overfit confirmed) |
| Sparsity-decomposition N_found (real) | 16/17 | mean sparsity 1.33 |
| Sparsity Z vs log-uniform null | **+5.0** | strong arithmetic signal |
| Binomial Z vs GMM-of-data null | **+4.97** (p=3e-7) | structure survives strongest null |
| Top RF feature Z vs y-shuffle | +3.06 | real but trivial (categorical proxy) |
| PCA n components for 90% var | 6 | high-dim categorical, no 1-D manifold |
| Held-out predictions <1σ | 1/6 | weak generalization |

## Key predictions (with σ-match)

1. **sin²θ₂₃ PMNS** = (1-2κ)(1-κ) = 5/9 = **0.5556** vs observed 0.561 ± 0.020.
   *0.97 % off, 0.27σ — CLEAN MATCH within experimental uncertainty.*

2. **m_p/m_π** = (4/5)(1+κ)/[κ(1-κ)] = **6.72** vs observed 6.726.
   *0.09 % off — striking but uses inverse-κ mode absent from the 17 patterns.*

3-6 (sin²θ₁₂, δ_CP, V_td, g_A) all fail at the sparsity bar.
