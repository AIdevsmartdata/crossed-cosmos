"""
A5_HURWITZ_INTERP / cm_alpha_ratio_test.py
==========================================

CLEAN test: is alpha_2 = 1/12 STRUCTURAL (universal across CM weight-5 newforms)
or COINCIDENCE (specific to K=Q(i))?

We bypass the period normalization issue by computing the DIMENSIONLESS RATIO

    R(f) := L(f, 2)^2 / ( L(f, 1) * L(f, 3) )    [purely arithmetic, no period]

For the K=Q(i) form 4.5.b.a we have alpha_1 = 1/10 and alpha_2 = 1/12 (with alpha_3
= alpha_2/2 = 1/24 forced by Gamma).

So R(4.5.b.a) = (1/12)^2 / ((1/10)(1/24)) * (pi^2)^2 / (pi^3 pi^1)
              = (1/144) / (1/240)
              = 240/144 = 5/3.

For ANOTHER CM form g, if alpha_2 / alpha_1 = (1/12)/(1/10) = 5/6 universally, then
R(g) = ((5/6)^2 * alpha_1^2) / (alpha_1 * (alpha_1/12)) = ((5/6)^2) / (1/12) * 12 ... wait,
let me redo. The functional equation forces alpha_{k-m}/alpha_m = Gamma(k-m)/Gamma(m).
So alpha_3 = alpha_2 * Gamma(2)/Gamma(3) = alpha_2 * 1/2.
And alpha_4 = alpha_1 * Gamma(1)/Gamma(4) = alpha_1 * 1/6.

L(f, m) = alpha_m * Omega_K^4 / pi^(4-m), so
  L(f,2)^2 / (L(f,1) L(f,3)) = (alpha_2)^2 pi^(4) / (alpha_1 alpha_3 pi^(3+1))
                              = (alpha_2)^2 / (alpha_1 alpha_3)
                              = (alpha_2)^2 / (alpha_1 * alpha_2/2)
                              = 2 alpha_2 / alpha_1.

So R(f) = 2 alpha_2 / alpha_1 — purely the algebraic ratio, INDEPENDENT of Omega_K!

For K=Q(i): R = 2 * (1/12) / (1/10) = 20/12 = 5/3.

If alpha_2/alpha_1 = 1/12 / 1/10 = 5/6 is UNIVERSAL across all imaginary quadratic
CM weight-5 newforms, R = 5/3 for all. If it varies, it's K-specific.

Similarly, we can compute the FULL ratio chain:
  Q1(f) := L(f,2) * L(f,3) / L(f,1) / L(f,4) = alpha_2 alpha_3 / (alpha_1 alpha_4)
        = (alpha_2 * alpha_2/2) / (alpha_1 * alpha_1/6)
        = 3 (alpha_2/alpha_1)^2.

For K=Q(i): Q1 = 3 * (5/6)^2 = 3 * 25/36 = 25/12.

Method
------
1. Fetch a_n via LMFDB API (1000 traces per form).
2. Use Iwaniec-Kowalski AFE to compute L(f,m) for m=1..4.
3. Compute R(f) and Q1(f) for each.
4. PSLQ-search for small rationals.
"""

import json
import os
from mpmath import mp, mpf, mpc, sqrt, pi, gamma, gammainc, pslq
from sympy import factorint, primerange
from fractions import Fraction

mp.dps = 60

CM_FORMS = [
    {"label": "4.5.b.a",  "N": 4,  "D_K": -4,  "d": 1},
    {"label": "7.5.b.a",  "N": 7,  "D_K": -7,  "d": 7},
    {"label": "8.5.d.a",  "N": 8,  "D_K": -8,  "d": 2},
    {"label": "11.5.b.a", "N": 11, "D_K": -11, "d": 11},
    {"label": "12.5.c.a", "N": 12, "D_K": -3,  "d": 3},
]


def load_traces(label):
    path = f"/tmp/mf_{label.replace('.', '_')}.json"
    d = json.load(open(path))
    r = d["data"][0]
    traces = r["traces"]
    return traces  # list, traces[n-1] = a_n for n = 1..1000


def L_value(traces, N_level, weight, s, X=mpf(1)):
    """Approximate functional equation Iwaniec-Kowalski (5.16) for cusp form
    of weight k, level N, sign +1."""
    s = mpf(s) if not isinstance(s, (mpc, complex)) else s
    k = mpf(weight)
    N_lvl = mpf(N_level)
    sqrt_N = sqrt(N_lvl)
    two_pi = 2 * pi
    Gs = gamma(s)
    Gks = gamma(k - s)
    cutoff1 = two_pi * X / sqrt_N
    cutoff2 = two_pi / (X * sqrt_N)
    total1 = mpf(0)
    total2 = mpf(0)
    for n in range(1, len(traces) + 1):
        an = traces[n - 1]
        if an == 0:
            continue
        x1 = cutoff1 * n
        total1 += mpf(an) / mpf(n)**s * gammainc(s, x1) / Gs
        x2 = cutoff2 * n
        total2 += mpf(an) / mpf(n)**(k - s) * gammainc(k - s, x2) / Gks
    lam_ratio = (sqrt_N / two_pi)**(k - 2*s) * Gks / Gs
    return total1 + lam_ratio * total2


def best_rational(x, max_denom=10000):
    fx = Fraction(str(float(x))).limit_denominator(max_denom)
    err = abs(mpf(fx.numerator) / mpf(fx.denominator) - x)
    return fx, err


def main():
    print("=" * 78)
    print("CM weight-5 newform L-value ratios: alpha-ladder structural test")
    print("=" * 78)

    results = {}
    for fd in CM_FORMS:
        label = fd["label"]
        N = fd["N"]
        traces = load_traces(label)
        print(f"\n--- {label}, K=Q(sqrt(-{fd['d']})), D_K={fd['D_K']}, level N={N} ---")
        print(f"   first 8 a_n: {traces[:8]}")
        # Sanity: L(f, 5/2) should be real positive for sign +1
        L_half = L_value(traces, N, 5, mpf(5)/2)
        print(f"   L(f, 5/2) = {float(L_half):+.10f}  (sanity: real, > 0 expected)")
        # Critical L-values
        Lvals = {}
        for m in [1, 2, 3, 4]:
            Lvals[m] = L_value(traces, N, 5, mpf(m))
            print(f"   L(f, {m}) = {float(Lvals[m]):+.12f}")
        # Functional equation check: alpha_3/alpha_2 = 1/2, alpha_4/alpha_1 = 1/6
        # i.e. L(f,3)/L(f,2) = (1/2) * pi^(-1)  -- wait, let me redo.
        # alpha_m = L(f,m) * pi^(4-m) / Omega^4. Functional eq: alpha_4/alpha_1 = 1/6.
        # So L(f,4)/L(f,1) = (1/6) * pi^(0)/pi^3 = 1/(6 pi^3).
        # And L(f,3)/L(f,2) = (1/2) * pi^1/pi^2 = 1/(2 pi).
        # Check:
        ratio_43 = Lvals[4] / Lvals[1]
        expected_43 = 1 / (6 * pi**3)
        ratio_32 = Lvals[3] / Lvals[2]
        expected_32 = 1 / (2 * pi)
        print(f"   FE check: L(4)/L(1) = {float(ratio_43):+.10f}, expected 1/(6 pi^3) = {float(expected_43):+.10f}, agreement {float(abs(ratio_43-expected_43)/abs(expected_43)):.3e}")
        print(f"   FE check: L(3)/L(2) = {float(ratio_32):+.10f}, expected 1/(2 pi) = {float(expected_32):+.10f}, agreement {float(abs(ratio_32-expected_32)/abs(expected_32)):.3e}")
        # Period-free ratio R(f) = L(f,2)^2 / (L(f,1) L(f,3)) = 2 alpha_2 / alpha_1
        # Actually wait: derivation
        #   alpha_m = L(f,m) * pi^(4-m) / Omega^4
        #   alpha_2/alpha_1 = (L(2) pi^2) / (L(1) pi^3) = L(2)/(L(1) pi)
        #   So 2 alpha_2/alpha_1 = 2 L(2) / (L(1) pi).
        # For Q(i): 2 * (1/12) / (1/10) = 20/12 = 5/3. So 5/3 = 2 L(2) / (L(1) pi)
        # i.e. L(2) / L(1) = (5/6) pi.
        ratio_21_pi = Lvals[2] / Lvals[1] / pi  # should be alpha_2 / alpha_1
        ratio_21 = Lvals[2] / Lvals[1]
        bf, err = best_rational(ratio_21_pi, max_denom=1000)
        print(f"   alpha_2/alpha_1 = L(2) / (L(1) pi) = {float(ratio_21_pi):+.12f}  ~ {bf} (err {float(err):.2e})")
        results[label] = {
            "Lvals": Lvals,
            "alpha_ratio_2_to_1": ratio_21_pi,
            "alpha_ratio_2_to_1_rational": bf,
            "alpha_ratio_2_to_1_err": err,
        }
        # PSLQ: search for integer relation between alpha_2/alpha_1 and 1
        # i.e. find integers a, b with a * (alpha_2/alpha_1) + b = 0 (rational)
        rel = pslq([ratio_21_pi, mpf(1)], tol=1e-20, maxcoeff=10000)
        print(f"   PSLQ on (alpha_2/alpha_1, 1): {rel}")
        if rel and rel[0] != 0:
            implied_rat = Fraction(-rel[1], rel[0])
            print(f"      => alpha_2/alpha_1 = {implied_rat}  (= {float(implied_rat):+.10f})")
        results[label]["pslq"] = rel

    # ---------------- SUMMARY ----------------
    print()
    print("=" * 78)
    print("SUMMARY: alpha_2 / alpha_1 ratio (period-free)")
    print("=" * 78)
    print(f"{'Label':<12} {'D_K':>5} {'alpha_2/alpha_1':>20} {'~rational':>15} {'matches 5/6?':>15}")
    print("-" * 78)
    target_ratio_qi = mpf(5)/mpf(6)  # Q(i) value: (1/12)/(1/10) = 5/6
    for label, r in results.items():
        D_K = next(f["D_K"] for f in CM_FORMS if f["label"] == label)
        ratio = r["alpha_ratio_2_to_1"]
        bf = r["alpha_ratio_2_to_1_rational"]
        match = "YES" if abs(ratio - target_ratio_qi) < mpf("1e-6") else f"no (off by {float(ratio - target_ratio_qi):+.4f})"
        print(f"{label:<12} {D_K:>5} {float(ratio):>20.10f} {str(bf):>15} {match:>15}")

    # Universal claim: if 5/6 universal, then alpha_2 = 1/12 implies alpha_1 = 1/10 universal
    # If alpha_2/alpha_1 varies: structural meaning of "1/12" is K-dependent

    print()
    print("VERDICT logic:")
    print("  - If alpha_2/alpha_1 = 5/6 across all forms => 1/12 IS structural")
    print("    (Bernoulli-type universal Hurwitz coefficient for any imag quadratic)")
    print("  - If alpha_2/alpha_1 varies with D_K => 1/12 is Q(i)-specific")
    print("    (the c=1 Cardy hit is COINCIDENCE)")


if __name__ == "__main__":
    main()
