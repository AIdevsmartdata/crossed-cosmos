# A Priori Predictions for Unmeasured Gauge Groups

**Date**: 2026-05-27
**Status**: BLIND predictions -- measure with Kevinotron THEN compare
**Method**: Linear regression + Neural network ensemble (10 seeds)
**Baseline formula**: S2/A = 6.42 * C2 + 2.33 * ln|Z| - 7.38

## Honest caveats

- 31 data points from 4 groups is MARGINAL for extrapolation
- Only 4 distinct groups -> any formula with 3+ free parameters is unconstrained
- Neural network has 45 params for 19 training points (overfit risk)
- These predictions should be treated as ORDER-OF-MAGNITUDE guides
- Z-score adversarial testing is mandatory before claiming any match

## Group properties

| Group | C2(adj) | dim(adj) | \|Z\| | d_fund | n_roots=\|Phi+\| | rank |
|-------|---------|----------|-------|--------|------------------|------|
| SU(2) | 2       | 3        | 2     | 2      | 1                | 1    |
| SU(3) | 3       | 8        | 3     | 3      | 3                | 2    |
| SU(4) | 4       | 15       | 4     | 4      | 6                | 3    |
| G2    | 4       | 14       | 1     | 7      | 6                | 2    |
| SU(5) | 5       | 24       | 5     | 5      | 10               | 4    |
| SU(6) | 6       | 35       | 6     | 6      | 15               | 5    |
| SO(7) | 5       | 21       | 2     | 7      | 9                | 3    |
| Sp(4) | 3       | 10       | 2     | 4      | 4                | 2    |

## Predictions at matched string tension (sigma*a^2 ~ 0.047)

### SU(5) (C2=5, dim=24, |Z|=5, d_fund=5)

| Method          | S2/A (L=4) | S2/A (L=12) | S2/A (L=inf est.) |
|-----------------|-----------|-------------|-------------------|
| Linear baseline | --        | --          | 28.27             |
| NN ensemble     | 23.87     | 23.85       | ~23.85            |

**Discriminating test**: S2(SU(5))/S2(SU(4)) ratio should be volume-independent.
Linear prediction: 28.27/21.54 ~ 1.31.
NN prediction: 23.85/21.54 ~ 1.11 (lower, because NN saturates -- see caveats).
**Trusted range**: 24 -- 28 (linear more reliable for SU(N) extrapolation).

### SU(6) (C2=6, dim=35, |Z|=6, d_fund=6)

| Method          | S2/A (L=4) | S2/A (L=12) | S2/A (L=inf est.) |
|-----------------|-----------|-------------|-------------------|
| Linear baseline | --        | --          | 35.07             |
| NN ensemble     | 24.51     | 24.50       | ~24.50            |

**Note**: NN extrapolation clearly unreliable for SU(6) (saturating at ~24.5).
Linear baseline is more trustworthy: S2/A ~ 35 at matched sigma*a^2.

### SO(7) (C2=5, dim=21, |Z|=2, d_fund=7)

| Method          | S2/A (L=4) | S2/A (L=12) | S2/A (L=inf est.) |
|-----------------|-----------|-------------|-------------------|
| Linear baseline | --        | --          | 26.11             |
| NN ensemble     | 23.18     | 23.14       | ~23.14            |

**Key test**: SO(7) has |Z|=2 like SU(2) but C2=5, dim=21.
Compares the Casimir vs dimension dependence outside SU(N).
SO(7) supset G2 as maximal subgroup -> ratio SO(7)/G2 probes the center effect
(|Z|=2 vs |Z|=1 at nearby Casimir).
**Trusted range**: 23 -- 26.

### Sp(4) (C2=3, dim=10, |Z|=2, d_fund=4)

| Method          | S2/A (L=4) | S2/A (L=12) | S2/A (L=inf est.) |
|-----------------|-----------|-------------|-------------------|
| Linear baseline | --        | --          | 13.36             |
| NN ensemble     | 14.09     | 13.90       | ~13.90            |

**Key test**: Sp(4) ~ SO(5) locally. Same |Z|=2 as SU(2), same C2=3 as SU(3),
but dim=10 not 8. Direct test of whether dim_adj matters beyond C2 + ln|Z|.
If S2(Sp(4)) ~ S2(SU(3)) ~ 14: formula is C2 + ln|Z| dominant.
If S2(Sp(4)) > S2(SU(3)): dim_adj matters independently.
**Best constrained prediction**: both methods agree S2/A ~ 13.4 -- 14.1.
**This is the most discriminating test** -- closest to training data range.

## PySR discoveries (2026-05-27 run)

### Best free-form equation (PySR Level 1A, 31 points)
```
S2/A = 5.68 * coupling - 4.05 * n_roots - dim_adj + 3.5/L^2
```
- Max residual: 0.91%, mean residual: 0.28%
- Uses coupling (=beta), n_roots=C2*(C2-1)/2, dim_adj, 1/L^2
- Complexity 13, loss 0.0047

### Factorized beta-dependence (G2 multi-beta, 16 points)
```
S2/A = 5.747 * beta + 3.978 / L^2 - 39.488
```
- Max residual: 0.88% across all G2 data

### Best hypothesis test (4 groups, matched beta, L>=8)

| Hypothesis     | R^2     | max residual |
|----------------|---------|-------------|
| dim_adj + lnZ  | 0.992   | 4.81%       |
| dim_adj/C2     | 0.983   | 5.60%       |
| dim_adj        | 0.964   | 8.01%       |
| C2             | 0.946   | 10.08%      |

Winner: dim_adj + ln|Z| (R^2 = 0.992). This suggests entanglement counts
adjoint degrees of freedom plus center superselection sectors.

### Residual structure (PySR on residuals of linear model)
```
residual ~ -0.457 / (dim_adj - n_roots^2)
```
- Suggests non-linear group-theoretic correction involving dim_adj vs n_roots^2
- For SU(N): dim_adj = N^2-1, n_roots^2 = [N(N-1)/2]^2 -- never equal
- For G2: dim_adj = 14, n_roots^2 = 36 -- denominator = -22

## Formula candidates to test

1. **Baseline**: S2/A = a*C2 + b*ln|Z| + c (known: a=6.37, b=2.36, c=-7.40)
2. **PySR best**: S2/A = 5.68*beta - 4.05*n_roots - dim_adj + 3.5/L^2
3. **Factorized**: S2/A = [a*dim_adj + b*ln|Z| + c] * beta/d_fund * [1 + d/L^2]
4. **Per-gluon**: S2/(A*dim) = f(C2, |Z|) should decrease monotonically
5. **Normalized**: S2/A / (beta/d_fund) ~ 1.55*d_fund - 0.17*n_roots + 2.76

## How to validate

1. Run `python3 kevinotron_ml.py` to generate numerical predictions
2. Implement SU(5), SU(6), SO(7), Sp(4) in Kevinotron Rust code
3. Measure S2/A at matched sigma*a^2 ~ 0.047 for L=4,6,8,10,12
4. Compare with predictions in this file
5. Compute chi^2 / ndof for each formula candidate
6. The formula that predicts ALL groups (including new ones) at <2% wins

## Risk assessment

| Prediction | Confidence | Reason |
|-----------|------------|--------|
| SU(5) S2/A ~ 28 | HIGH | Linear extrapolation in SU(N), well-constrained |
| SU(6) S2/A ~ 35 | HIGH | Same reason |
| SO(7) S2/A ~ 25 | MEDIUM | Extrapolation outside SU(N) family |
| Sp(4) S2/A ~ 14 | LOW | Different Lie algebra type, only 1 non-SU(N) calibration point (G2) |
| dim_adj matters | MEDIUM | G2 vs SU(4) shows 1-gluon difference -> 19% effect is large |
| kappa_EE(N) = kappa_inf*(1-1/N^2) | MEDIUM | Only 3 SU(N) data points for the fit |
