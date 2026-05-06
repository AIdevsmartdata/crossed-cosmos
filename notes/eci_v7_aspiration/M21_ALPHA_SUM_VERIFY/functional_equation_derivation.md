---
name: M21 functional equation derivation — alpha_m vs alpha_{k-m}
description: Sympy-verified derivation of the constraint between alpha_m and alpha_{k-m} from the functional equation of L(f,s).
type: analysis
agent: M21 (Sonnet 4.6)
date: 2026-05-06
hallu_count_in: 85
hallu_count_out: 85
---

# Functional Equation Derivation: alpha_m vs alpha_{k-m}

## Setup

For a newform f of weight k, level N, nebentypus chi, the completed L-function is:

    Lambda(s) = N^{s/2} * (2pi)^{-s} * Gamma(s) * L(f, s)

The functional equation states:

    Lambda(s) = epsilon * Lambda_bar(k - s)

where epsilon = root number (|epsilon|=1), and for self-dual forms Lambda_bar = Lambda, so:

    Lambda(s) = epsilon * Lambda(k - s)     [self-dual case]

## Derivation of the alpha_m / alpha_{k-m} ratio

Expanding the functional equation at integer points m and k-m (both in the critical strip {1,...,k-1}):

    N^{m/2} * (2pi)^{-m} * Gamma(m) * L(f, m) = epsilon * N^{(k-m)/2} * (2pi)^{-(k-m)} * Gamma(k-m) * L(f, k-m)

Rearranging:

    L(f, m) / L(f, k-m) = epsilon * N^{(k-2m)/2} * (2pi)^{2m-k} * Gamma(k-m) / Gamma(m)

Now define the Damerell-Shimura normalization:

    alpha_m := L(f, m) * pi^{k-m} / Omega_K^{2(k-1)}

where Omega_K is the Chowla-Selberg period of the CM field K of f.

Then:

    alpha_m / alpha_{k-m} = [L(f,m) * pi^{k-m}] / [L(f,k-m) * pi^m]
                          = [L(f,m) / L(f,k-m)] * pi^{k-2m}
                          = epsilon * N^{(k-2m)/2} * (2pi)^{2m-k} * Gamma(k-m)/Gamma(m) * pi^{k-2m}
                          = epsilon * N^{(k-2m)/2} * 2^{2m-k} * pi^{2m-k} * Gamma(k-m)/Gamma(m) * pi^{k-2m}

Note: pi^{2m-k} * pi^{k-2m} = pi^0 = 1. So ALL pi factors cancel:

    alpha_m / alpha_{k-m} = epsilon * N^{(k-2m)/2} * 2^{2m-k} * Gamma(k-m) / Gamma(m)

**This ratio is determined ENTIRELY by (epsilon, N, k, m). No L-values needed.**

### Sympy verification (symbolic, exact)

For f = 4.5.b.a: k=5, N=4, epsilon=+1.

**Pair (m=2, m=3):**

    R(2) = alpha_2 / alpha_3
         = (+1) * 4^{(5-4)/2} * 2^{4-5} * Gamma(3) / Gamma(2)
         = 4^{1/2} * 2^{-1} * 2! / 1!
         = 2 * (1/2) * 2
         = 2

Check: alpha_2 / alpha_3 = (1/12) / (1/24) = 24/12 = 2. CONFIRMED.

**Pair (m=1, m=4):**

    R(1) = alpha_1 / alpha_4
         = (+1) * 4^{(5-2)/2} * 2^{2-5} * Gamma(4) / Gamma(1)
         = 4^{3/2} * 2^{-3} * 3! / 0!
         = 8 * (1/8) * 6
         = 6

Check: alpha_1 / alpha_4 = (1/10) / (1/60) = 60/10 = 6. CONFIRMED.

## Consequence for pair-sums

Since alpha_m / alpha_{k-m} = R(m; k, N, epsilon), we have:

    alpha_{k-m} = alpha_m / R(m)

    alpha_m + alpha_{k-m} = alpha_m * (1 + 1/R(m)) = alpha_m * (R(m) + 1) / R(m)

**CRITICAL OBSERVATION**: The pair-sum alpha_m + alpha_{k-m} is NOT determined by
(k, N, epsilon) alone — it also requires alpha_m itself. However, the SHAPE of
the pair-sum (whether it is a clean rational / 2-power) depends on R(m).

## The rationality condition

For R(m) to be rational (necessary for the pair-sum formula to give a clean rational):

    R(m) = epsilon * N^{(k-2m)/2} * 2^{2m-k} * Gamma(k-m)/Gamma(m)

The factor N^{(k-2m)/2} is rational iff (k-2m) is even OR N is a perfect square.

For weight k=5 and m=2: k-2m = 5-4 = 1. So N^{1/2} is rational iff N is a perfect square.

**Conclusion**: R(2; k=5, N, eps) is rational IFF N is a perfect square.

Similarly R(1; k=5, N, eps) = eps * N^{3/2} * (3/4) is rational IFF N is a perfect square.

For N=4: R(2)=2 (rational, clean). alpha_2 + alpha_3 = alpha_2 * 3/2.
For N=9: R(2)=3 (rational, clean). alpha_2 + alpha_3 = alpha_2 * 4/3.
For N=16: R(2)=4 (rational, clean). alpha_2 + alpha_3 = alpha_2 * 5/4.
For N=27: R(2) = sqrt(27) = 3*sqrt(3) (IRRATIONAL). No clean pair-sum.
For N=36: R(2) = sqrt(36)/2 * 2 = 6 (rational). alpha_2 + alpha_3 = alpha_2 * 7/6.
For N=100: R(2) = sqrt(100)/2 * 2 = 10 (rational). alpha_2 + alpha_3 = alpha_2 * 11/10.

## Table of R(m; k=5, N, eps=+1) for perfect-square levels N

| N   | sqrt(N) | R(2) = sqrt(N) | R(1) = (3/4)*N^{3/2} | Notes |
|-----|---------|----------------|----------------------|-------|
| 4   | 2       | 2              | 6                    | 4.5.b.a |
| 9   | 3       | 3              | 243/4 = 60.75        | 9.5.? |
| 16  | 4       | 4              | 48                   | |
| 25  | 5       | 5              | 375/4 = 93.75        | |
| 36  | 6       | 6              | 162                  | 36.5.d.a (twist of 4.5.b.a) |
| 49  | 7       | 7              | 3087/4 = 771.75      | |
| 64  | 8       | 8              | 384                  | 64.5.c.a (twist) |
| 100 | 10      | 10             | 750                  | 100.5.b.a (twist) |

## Does the pair-sum = 2^{-3} only for 4.5.b.a?

alpha_2 + alpha_3 = alpha_2 * (R(2)+1)/R(2) = alpha_2 * (sqrt(N)+1)/sqrt(N)

For this to equal 2^{-3} = 1/8:

    alpha_2 = (1/8) * sqrt(N) / (sqrt(N)+1)

For N=4 (4.5.b.a):
    alpha_2 = (1/8) * 2/3 = 1/12. CHECK: M13 gives alpha_2 = 1/12. CONFIRMED.

For N=9 (some CM weight-5 form):
    alpha_2 would need to be (1/8)*3/4 = 3/32.
    This specific value for a level-9 CM form is NOT guaranteed — it depends on Damerell's theorem.

For N=36 (36.5.d.a, twist of 4.5.b.a):
    alpha_2 for 36.5.d.a differs from 4.5.b.a because twisting modifies L-values.
    For a quadratic twist by chi_9, L(f x chi_9, m) ≠ L(f, m) in general.
    So alpha_2(36.5.d.a) ≠ 1/12.

## Weight-7 CM forms

For k=7, the critical integers are m in {1,2,3,4,5,6}. Pairs: (1,6), (2,5), (3,4).

R(m; k=7, N, eps=+1) = N^{(7-2m)/2} * 2^{2m-7} * Gamma(7-m)/Gamma(m)

For m=3 (middle pair, k/2=3.5):
    R(3) = N^{1/2} * 2^{-1} * Gamma(4)/Gamma(3) = sqrt(N) * (1/2) * 2 = sqrt(N)

Same structure as weight-5! R(3; k=7) = sqrt(N), rational iff N perfect square.

For 3.7.b.a (N=3, CM by Q(sqrt(-3))):
    R(3) = sqrt(3) — irrational! No clean middle-pair sum.

For a weight-7 CM form at N=4 (if it exists):
    R(3) = 2 — rational. alpha_3+alpha_4 = alpha_3 * 3/2.

For weight-7 at N=9 (hypothetical):
    R(3) = 3 — rational.

## Weight-3 CM forms

For k=3, critical integers m in {1,2}. Only one pair: (1,2).

R(1; k=3, N, eps=+1) = N^{(3-2)/2} * 2^{2-3} * Gamma(2)/Gamma(1) = sqrt(N) * (1/2) * 1 = sqrt(N)/2

For this to be rational: N must be a perfect square.

For 27.3.b.a (N=27): R(1) = sqrt(27)/2 = 3*sqrt(3)/2 — irrational.
For 12.3.c.a (N=12): R(1) = sqrt(12)/2 = sqrt(3) — irrational.
For 4.3.b.a (N=4, if it exists): R(1) = 1 — rational. alpha_1+alpha_2 = 2*alpha_1.

## Summary of the general pattern

The condition for a RATIONAL pair-sum (alpha_m + alpha_{k-m} is rational) is:

    N^{(k-2m)/2} must be rational, i.e., N is a perfect square, OR k-2m is even.

For weight k and middle pair m = floor(k/2):
    k - 2m = 1 if k odd, k - 2m = 0 if k even.
    If k EVEN: all pairs give rational R automatically (N^{integer/2} = integer if N perfect square, but k-2m even means N^0=1 for the middle pair when k even).

Wait — for k=5 (odd), the only pairs are (1,4) and (2,3). For m=2: k-2m=1. For m=1: k-2m=3.
For BOTH pairs to have rational R, we need N = perfect square.

For k=4 (even): pairs (1,3) and (2,2) — but m=2=k/2=2 is NOT in {1,...,k-1}/2 (it's not paired with a different m). So only pair (1,3): k-2*1=2, giving R(1)=N^1 * 2^{-2} * 2 = N/2 — rational for any N.

**For even weight k, R(m) is always rational. For odd weight k, R(m) is rational iff N is a perfect square.**

This is a general structural property.

## Conclusion for the derivation

The functional equation FORCES the ratio alpha_m/alpha_{k-m} = R(m; k, N, eps).
Whether the PAIR-SUM is clean depends on:
1. R(m) being rational (needs N = perfect square for odd k)
2. The base Damerell value alpha_m being a "nice" rational

For 4.5.b.a: N=4 (perfect square) ensures rational R(m). The specific value alpha_2=1/12
(from Damerell, verified numerically in M13) gives the clean pair-sum alpha_2+alpha_3 = 1/8.

The clean 2-power nature (1/8 = 2^{-3}) is specific to:
- The level N=4 (gives R(2)=2, the simplest possible rational value)
- The Damerell value alpha_2=1/12 (gives sum = 1/12 * 3/2 = 1/8)

For other perfect-square levels (N=9, 16, ...) with different Damerell values,
the pair-sum is rational but NOT necessarily a clean 2-power.
