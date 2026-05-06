---
name: Q(omega) period normalization table — M52
type: data
---

# Q(omega) Damerell Period Table — F2 v6

**PARI/GP 2.15.4, prec=80 decimal digits, 2026-05-06**

## Omega candidates (numerical values)

| Label | Formula | Value |
|---|---|---|
| O1 | (1/sqrt(3))*(Gamma(1/3)/Gamma(2/3))^(1/12) [Chowla-Selberg chi/12] | 0.61113 |
| O2 | Gamma(1/3)^3/(2*Pi*sqrt(3)) [Damerell-Hurwitz full] | 1.76664 |
| O3 | Gamma(1/3)^3/(4*Pi*sqrt(3)) [F2 v5 current] | 0.88332 |
| O4 | Gamma(1/3)*Gamma(1/6)/(4*Pi*sqrt(3)) [Lemniscate] | 0.68511 |
| O5 | sqrt(Gamma(1/3)*Gamma(2/3))/sqrt(3) | 1.09964 |
| O6 | Gamma(1/3)/(sqrt(3)*Pi^(1/3)) | 1.05605 |
| O7 | Gamma(1/3)^(3/2)/(sqrt(Pi)*3^(1/4)) [Borwein-Zucker] | 1.87970 |
| O8 | Gamma(1/3)^3/(2^(1/3)*3*Pi) [Fermat cubic] | 1.61910 |

Note: O2/O3 = 2.000 EXACTLY. O3 = O2/2 (F2 v5 used the half-period).

## 27.5.b.a alpha_m = L(f,m)*Pi^(4-m)/Omega^4

Traces a1..8 = [1, 0, 0, 16, 0, 0, 71, 0]
L(f,1..4) = (3.67287, 2.22062, 1.34258, 1.08230)

| Omega | m=1 | m=2 | m=3 | m=4 | Notes |
|---|---|---|---|---|---|
| O1 | 816.449... | 157.13... | 30.239... | 7.759... | All large, no simple rationals |
| **O2** | **27*sqrt(3)/4** | **9/4** | **sqrt(3)/4** | **1/9** | EXACT algebraics! Even-m rational |
| O3 | 27^2*sqrt(3)/4 | **36** | 16*sqrt(3)/4 | **16/9** | x16 inflated (F2v5 result) |
| O4 | 516.9... | 99.48... | 19.14... | 4.913... | No pattern |
| O5 | 77.89... | 14.99... | 2.885... | 0.740... | No pattern |
| O6 | 91.56... | 17.62... | 3.391... | 0.870... | No pattern |
| O7 | 9.122... | 1.756... | 0.338... | 0.0867... | No simple rationals |
| O8 | 16.571... | 3.189... | 0.614... | 0.157... | No pattern |

**WINNER: O2.** Structure: {27sqrt(3)/4, 9/4, sqrt(3)/4, 1/9}
Even-m: {9/4, 1/9} RATIONAL. Odd-m: {27sqrt(3)/4, sqrt(3)/4} in Q(sqrt(3)).
Cross-parity ratio: Pi*L(f,1)/L(f,2) = 3*sqrt(3) (exact irrational).

## 12.5.c.a alpha_m = L(f,m)*Pi^(4-m)/Omega^4

Traces a1..8 = [1, 0, 9, 0, 0, 0, -94, 0]
L(f,1..4) = (1.09318, 1.32187, 1.19881, 1.08720)

| Omega | m=1 | m=2 | m=3 | m=4 | Notes |
|---|---|---|---|---|---|
| O1 | 243.0... | 93.53... | 27.001... | 7.794... | m=3 near 27 but not exact |
| O2 | 3.480... | 1.339... | 0.387... | 0.1116... | ratios: m2/m4=12, m1/m3=9 (rational) |
| O3 | 55.68... | 21.43... | 6.186... | 1.786... | No simple rationals |
| O4 | 153.9... | 59.22... | 17.09... | 4.935... | No pattern |
| **O5** | 23.182... | 8.923... | 2.576... | 0.744... | m=1 near 255/11, m=3 near 85/33 but NOT exact |
| O6 | 27.25... | 10.49... | 3.028... | 0.874... | No pattern |
| O7 | 2.715... | 1.045... | 0.302... | 0.087... | No pattern |
| O8 | 4.932... | 1.898... | 0.548... | 0.158... | No pattern |
| Omega_right | 2*sqrt(3) | **4/3** | 2*sqrt(3)/9 | **1/9** | EXACT! (see below) |

**WINNER: Omega_right = (9*L(f,4)_{12})^{1/4} = 1.76863...**
This is NOT equal to O2 (ratio: Omega_right/O2 = 1.001130, off by 0.11%).
Structure: {2sqrt(3), 4/3, 2sqrt(3)/9, 1/9}
Even-m: {4/3, 1/9} RATIONAL. Odd-m: {2sqrt(3), 2sqrt(3)/9} in Q(sqrt(3)).
Cross-parity ratio: Pi*L(f,1)/L(f,2) = 3*sqrt(3)/2 (exact irrational).

## Invariant L-value ratios (Omega-independent)

| Form | Pi^2*L(2)/L(4) | Pi^2*L(1)/L(3) | Pi*L(1)/L(2) |
|---|---|---|---|
| 4.5.b.a | **5** (rational) | **12/5** (rational) | **6/5** (rational) |
| 27.5.b.a | **81/4** (rational) | **27** (rational) | 3*sqrt(3) (irrational) |
| 12.5.c.a | **12** (rational) | **9** (rational) | 3*sqrt(3)/2 (irrational) |

KEY DIAGNOSTIC: Pi*L(f,1)/L(f,2) is rational ONLY for 4.5.b.a (Q(i) CM).
For Q(omega) CM: this ratio = 3*sqrt(3) or 3*sqrt(3)/2, irrational.
This is the OMEGA-INDEPENDENT signature distinguishing Q(i) from Q(omega).

## Reference: Q(i) period O_{Q(i)} = Gamma(1/4)^2/(2*sqrt(2*Pi))

4.5.b.a confirmed: (1/10, 1/12, 1/24, 1/60) all rational, denominators lcm=60.
Ladder ratios: 12/10=6/5, 24/12=2, 60/24=5/2 — all rational.
ALL FOUR alphas in Q.

## Algebraic structure of Q(omega) ladders

For 27.5.b.a: {alpha_1, alpha_2, alpha_3, alpha_4} = {27sqrt(3)/4, 9/4, sqrt(3)/4, 1/9}
  - alpha_1/alpha_3 = 27 (rational)
  - alpha_2/alpha_4 = 81/4 (rational)
  - alpha_2*alpha_4 = (9/4)*(1/9) = 1/4 (rational)
  - alpha_1*alpha_3 = 27*(3^(1/2)/4)^2 * ... = 27*3/16 = 81/16 (rational!)

For 12.5.c.a: {2sqrt(3), 4/3, 2sqrt(3)/9, 1/9}
  - alpha_1/alpha_3 = 9 (rational)
  - alpha_2/alpha_4 = 12 (rational)
  - alpha_2*alpha_4 = (4/3)*(1/9) = 4/27 (rational)
  - alpha_1*alpha_3 = 2*sqrt(3)*(2*sqrt(3)/9) = 4*3/9 = 4/3 (rational!)

The products alpha_{odd}*alpha_{odd} and alpha_{even}*alpha_{even} are always rational.
This is because alpha_m * alpha_{k-1-m} is independent of sqrt(3) by the functional equation.
