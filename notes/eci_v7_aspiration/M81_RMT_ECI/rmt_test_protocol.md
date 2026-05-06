---
name: M81 RMT test protocol — PARI/GP + Sage skeletons for L(4.5.b.a, s) zero statistics
description: Computational protocol to verify Katz-Sarnak SO(even) prediction + GUE pair correlation. PARI ~50 zeros up to height 50. Anomaly trigger r_1 > 2.5
type: project
---

# RMT test protocol for L(f = 4.5.b.a, s)

## PARI/GP script (Kevin's PC, PARI 2.11+)

```gp
\\ Step 1: Build modular form f = 4.5.b.a
mf = mfinit([4, 5, Mod(3,4)], 1);  \\ Gamma_0(4), weight 5, char 4.b (chi(3)=-1)
an = mfcoefs(mf, 2000);
\\ Cross-check: an[3] (= a_2) should be -4; an[6] (= a_5) should be -14

\\ Step 2: L-function object with zeros up to height 50
lf = lfuninit(mf, [50]);
zeros = lfunzeros(lf, [0, 50]);  \\ gamma_n in [0,50]
print("N zeros found: ", length(zeros));

\\ Step 3: Analytic conductor and normalized gaps
q_an = 4 * (5 / (2*Pi))^2;  \\ ~ 2.534
Delta(T) = 2*Pi / log(q_an * T / (2*Pi));
norm_gaps = vector(length(zeros)-1, j,
  (zeros[j+1]-zeros[j]) / Delta((zeros[j]+zeros[j+1])/2));

\\ Step 4: Compare first gap to SO(even) prediction
print("First normalized gap r_1 = ", norm_gaps[1]);
\\ GUE prediction: mean(norm_gaps) ~ 1; if r_1 > 2.5 this is anomalous

\\ Step 5: Pair correlation over all pairs within window 10
\\ (output raw data for external histogram vs GUE formula)
```

## Sage alternative

```python
f = CuspForms(Gamma0(4), 5).newforms(names='a')[0]  # need chi_4 char
L = f.lseries()
zeros = L.zeros(50)
```

## Interpretation thresholds

| r_1 (first normalized gap) | Interpretation |
|---|---|
| 0.5 – 2.0 | Normal; confirms GUE/SO(even) |
| > 2.5 | Anomalous; possible CM arithmetic effect |
| Systematic deviation from GUE | Requires full recheck before any claim |

## Action plan

1. Kevin runs PARI/GP script on PC (estimated 5-10 minutes for 50 zeros up to height 50)
2. If r_1 > 2.5 OR systematic GUE deviation: dispatch deeper sub-agent for full pair-correlation histogram + bootstrap analysis
3. If conventional: log as CONFIRMS-EXISTING (still publishable as numerics letter Exp. Math.)
4. Cross-cite: Hamieh-Wong 2412.03034 (Hilbert modular Katz-Sarnak Dec 2024)
