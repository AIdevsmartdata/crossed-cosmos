"""
A5 / cm_alpha_normalized.py — DEFINITIVE structural test.

For each weight-5 CM newform f with CM by K:
  1. Compute L(f, m) for m=1..4 via AFE (verified by FE).
  2. Define each form's OWN Omega_f by:
        Omega_f^4 := L(f, 4) * 60     (HURWITZ-NORMALIZED: forces alpha_4 = 1/60)
     equivalently
        Omega_f^4 := L(f, 1) * pi^3 * 10  (forces alpha_1 = 1/10)
     these are CONSISTENT iff the FE alpha_4 = alpha_1/6 holds (it does).
  3. Compute alpha_2 = L(f, 2) * pi^2 / Omega_f^4.
  4. Test: is alpha_2 = 1/12 universally?

This is the parameter-free question: when each CM form is Hurwitz-anchored
(alpha_1 = 1/10), is alpha_2 = 1/12 universal or K-specific?

The answer follows IMMEDIATELY from the period-free ratio computed earlier:
   2 alpha_2 / alpha_1 = (5/3 if alpha_2 = 1/12 and alpha_1 = 1/10)
i.e., alpha_2 = (5/6) alpha_1.

Since alpha_2/alpha_1 (period-free) is:
   Q(i):       5/6 = 0.833...   <- target
   Q(sqrt-7):  0.576            <- 5.76/10? 9/16?
   Q(sqrt-2):  0.530            <- 1/2 + change
   Q(sqrt-11): 0.411            <- 5/12?
   Q(sqrt-3):  0.385            <- 5/13?

If we Hurwitz-anchor each (alpha_1 = 1/10), then alpha_2 = (alpha_2/alpha_1) * 1/10:
   Q(i):       1/12      = 0.0833    <- the original
   Q(sqrt-7):  0.0576
   Q(sqrt-2):  0.0530
   Q(sqrt-11): 0.0411
   Q(sqrt-3):  0.0385

VERDICT: alpha_2 = 1/12 is NOT universal — it only holds for Q(i).
Therefore the c=1 Cardy hit (1/12 = c/12 for c=1 free boson) is K-SPECIFIC,
not a universal Bernoulli structure.

But: are these other values themselves "interesting rationals"? Let's check.
"""

import json
from mpmath import mp, mpf, mpc, sqrt, pi, gamma, gammainc, pslq
from fractions import Fraction

mp.dps = 60

CM_FORMS = [
    {"label": "4.5.b.a",  "N": 4,  "D_K": -4,  "d": 1,  "Knote": "Q(i)"},
    {"label": "7.5.b.a",  "N": 7,  "D_K": -7,  "d": 7,  "Knote": "Q(sqrt-7)"},
    {"label": "8.5.d.a",  "N": 8,  "D_K": -8,  "d": 2,  "Knote": "Q(sqrt-2)"},
    {"label": "11.5.b.a", "N": 11, "D_K": -11, "d": 11, "Knote": "Q(sqrt-11)"},
    {"label": "12.5.c.a", "N": 12, "D_K": -3,  "d": 3,  "Knote": "Q(sqrt-3)"},
]


def load_traces(label):
    path = f"/tmp/mf_{label.replace('.', '_')}.json"
    d = json.load(open(path))
    return d["data"][0]["traces"]


def L_value(traces, N_level, weight, s, X=mpf(1)):
    s = mpf(s)
    k = mpf(weight)
    sqrt_N = sqrt(mpf(N_level))
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


def find_small_rational_via_pslq(x, max_coeff=10000):
    """PSLQ to find p/q with high precision."""
    rel = pslq([x, mpf(1)], tol=mpf("1e-40"), maxcoeff=max_coeff)
    if rel and rel[0] != 0:
        return Fraction(-rel[1], rel[0])
    return None


def main():
    print("=" * 78)
    print("A5: HURWITZ-anchored alpha_2 across imaginary-quadratic CM weight-5 newforms")
    print("=" * 78)
    print()
    print("Anchor: force alpha_1 := L(f,1) * pi^3 / Omega_f^4 = 1/10 (Hurwitz lemniscatic)")
    print("Then alpha_2 = L(f,2) * pi^2 / Omega_f^4 = 10 * L(f,2) / (L(f,1) * pi).")
    print()

    # Load all and compute
    rows = []
    for fd in CM_FORMS:
        traces = load_traces(fd["label"])
        L1 = L_value(traces, fd["N"], 5, mpf(1))
        L2 = L_value(traces, fd["N"], 5, mpf(2))
        L3 = L_value(traces, fd["N"], 5, mpf(3))
        L4 = L_value(traces, fd["N"], 5, mpf(4))
        # FE consistency check
        fe_ok_43 = abs(L4/L1 - pi**3/(6*mpf(fd["N"])**(mpf(3)/2)*mpf(fd["N"])**(-mpf(3)/2))) < 1
        # The correct FE: L(k-m)/L(m) = N^(m-k/2)*(2pi)^(k-2m)*Gamma(m)/Gamma(k-m)
        # For m=1, k=5: L(4)/L(1) = N^(-3/2)*(2pi)^3*1/6 = (2pi)^3/(6 N^{3/2}) = 4 pi^3 / (3 N^(3/2))
        N = mpf(fd["N"])
        expected_43 = (2*pi)**3 / (6 * N**(mpf(3)/2))
        expected_32 = (2*pi)**1 / (2 * N**(mpf(1)/2))
        agree_43 = abs(L4/L1 - expected_43)/expected_43
        agree_32 = abs(L3/L2 - expected_32)/expected_32
        # Hurwitz-anchored alpha_2:
        # alpha_1 forced to 1/10 means Omega_f^4 := L(f,1) * pi^3 * 10
        # Then alpha_2 = L(f,2) * pi^2 / Omega_f^4 = L(f,2) / (L(f,1) * pi * 10)
        alpha_2_anchored = L2 / (L1 * pi * mpf(10))
        # Find rational
        rat_pslq = find_small_rational_via_pslq(alpha_2_anchored, max_coeff=100000)
        rat_simple, err = best_rational(alpha_2_anchored, max_denom=10000)
        rows.append({
            "label": fd["label"],
            "Knote": fd["Knote"],
            "D_K": fd["D_K"],
            "L1": L1, "L2": L2, "L3": L3, "L4": L4,
            "agree_43": agree_43, "agree_32": agree_32,
            "alpha_2": alpha_2_anchored,
            "rat_pslq": rat_pslq,
            "rat_simple": rat_simple,
            "err_simple": err,
        })

    # Print L-values, FE check
    print("L-values and FE consistency:")
    print(f"{'Label':<10} {'K':>12} {'L(1)':>12} {'L(2)':>12} {'L(3)':>12} {'L(4)':>12}  FE43  FE32")
    for r in rows:
        print(f"{r['label']:<10} {r['Knote']:>12} {float(r['L1']):>12.8f} {float(r['L2']):>12.8f} "
              f"{float(r['L3']):>12.8f} {float(r['L4']):>12.8f}  {float(r['agree_43']):.1e}  {float(r['agree_32']):.1e}")

    print()
    print("=" * 78)
    print("CRITICAL TEST: Hurwitz-anchored alpha_2 (each K with its own period)")
    print("=" * 78)
    print(f"{'Label':<10} {'K':>12} {'D_K':>5} {'alpha_2':>20} {'PSLQ rational':>18} {'~simple':>10} 1/12?")
    for r in rows:
        a2 = r["alpha_2"]
        pslq_rat = r["rat_pslq"]
        sim_rat = r["rat_simple"]
        is_12 = "YES" if abs(a2 - mpf(1)/12) < mpf("1e-6") else "no"
        pslq_str = str(pslq_rat) if pslq_rat else "(none)"
        print(f"{r['label']:<10} {r['Knote']:>12} {r['D_K']:>5} {float(a2):>20.14f} {pslq_str:>18} "
              f"{str(sim_rat):>10} {is_12}")

    print()
    print("=" * 78)
    print("INTERPRETATION")
    print("=" * 78)
    print("""
    Q(i): alpha_2 = 1/12 (= B_2/2, classical Bernoulli, matches Cardy c=1)
    Other K: alpha_2 differs.

    These other values, multiplied by various small integers, should reveal
    the actual structural pattern. In Lozano-Robledo's notation, the
    Bernoulli-Hurwitz number BH^0_k = (2pi/sqrt|D_K|)^0 * e * L(psi^k, k)/Omega^k.

    For K=Q(i), e=4 (= w_K = 4 roots of unity), and BH^0_k normalizes to the
    classical Hurwitz lemniscatic numbers. For other K with w_K=2 (or 6 for d=3),
    the e factor differs, AND the discriminant scaling (2pi/sqrt|D_K|)^0 = 1
    drops out at j=0 BUT enters the j>0 (i.e. m < k=5) cases.
    """)


if __name__ == "__main__":
    main()
