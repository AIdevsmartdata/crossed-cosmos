"""
A5 / structural_pattern_v2.py — Targeted PSLQ for the structural identity.

OBSERVATION: 12 * alpha_2(K) * sqrt|D_K| takes values:
  Q(i):       2     (= 2/1)
  Q(sqrt-7):  ~1.829   (= 64/35 = 64/(5*7) ?)
  Q(sqrt-2):  1.800    (= 9/5 ?)
  Q(sqrt-11): ~1.636   (= 18/11 ?)
  Q(sqrt-3):  0.800    (= 4/5 ?)

Pattern guess: 12 * alpha_2 * sqrt|D| = c * h_K * w_K^? / |D|^?

Let's test PSLQ with sufficient candidate basis.
"""
from mpmath import mp, mpf, sqrt, pi, gamma, gammainc, pslq
from fractions import Fraction
import json

mp.dps = 60


def load_traces(label):
    return json.load(open(f"/tmp/mf_{label.replace('.', '_')}.json"))["data"][0]["traces"]


def L_value(traces, N_level, weight, s, X=mpf(1)):
    s = mpf(s); k = mpf(weight)
    sqrt_N = sqrt(mpf(N_level)); two_pi = 2 * pi
    Gs = gamma(s); Gks = gamma(k - s)
    cutoff1 = two_pi * X / sqrt_N; cutoff2 = two_pi / (X * sqrt_N)
    total1 = mpf(0); total2 = mpf(0)
    for n in range(1, len(traces) + 1):
        an = traces[n - 1]
        if an == 0: continue
        x1 = cutoff1 * n; x2 = cutoff2 * n
        total1 += mpf(an) / mpf(n)**s * gammainc(s, x1) / Gs
        total2 += mpf(an) / mpf(n)**(k - s) * gammainc(k - s, x2) / Gks
    lam_ratio = (sqrt_N / two_pi)**(k - 2*s) * Gks / Gs
    return total1 + lam_ratio * total2


CM_FORMS = [
    {"label": "4.5.b.a",  "N": 4,  "D_K": -4,  "d": 1,  "w_K": 4, "h_K": 1, "Knote": "Q(i)"},
    {"label": "7.5.b.a",  "N": 7,  "D_K": -7,  "d": 7,  "w_K": 2, "h_K": 1, "Knote": "Q(sqrt-7)"},
    {"label": "8.5.d.a",  "N": 8,  "D_K": -8,  "d": 2,  "w_K": 2, "h_K": 1, "Knote": "Q(sqrt-2)"},
    {"label": "11.5.b.a", "N": 11, "D_K": -11, "d": 11, "w_K": 2, "h_K": 1, "Knote": "Q(sqrt-11)"},
    {"label": "12.5.c.a", "N": 12, "D_K": -3,  "d": 3,  "w_K": 6, "h_K": 1, "Knote": "Q(sqrt-3)"},
]


def main():
    rows = []
    for fd in CM_FORMS:
        traces = load_traces(fd["label"])
        L1 = L_value(traces, fd["N"], 5, mpf(1))
        L2 = L_value(traces, fd["N"], 5, mpf(2))
        a2 = L2 / (L1 * pi * mpf(10))   # Hurwitz-anchored
        rows.append({**fd, "L1": L1, "L2": L2, "alpha_2": a2})

    print("=" * 78)
    print("Quantity Q(K) = 12 * alpha_2 * sqrt|D_K|: PSLQ rational search")
    print("=" * 78)
    print()
    print(f"{'K':>12} {'D_K':>5} {'w_K':>3} {'12*alpha_2*sqrt|D|':>20} {'best fraction':>20} {'err':>10}")
    for r in rows:
        Q = 12 * r["alpha_2"] * sqrt(abs(r["D_K"]))
        # Best rational approx with various denominators
        best = None
        best_err = mpf(1)
        for max_d in [100, 1000, 10000]:
            f = Fraction(str(float(Q))).limit_denominator(max_d)
            err = abs(mpf(f.numerator)/mpf(f.denominator) - Q)
            if err < best_err:
                best_err = err
                best = f
        print(f"{r['Knote']:>12} {r['D_K']:>5} {r['w_K']:>3} {float(Q):>20.14f} {str(best):>20} {float(best_err):.2e}")

    # PSLQ test: is Q(K) = (rational) * w_K? Or = (rational) / (w_K)?
    print()
    print("Q(K) / w_K:")
    for r in rows:
        Q = 12 * r["alpha_2"] * sqrt(abs(r["D_K"]))
        ratio = Q / mpf(r["w_K"])
        f = Fraction(str(float(ratio))).limit_denominator(1000)
        err = abs(mpf(f.numerator)/mpf(f.denominator) - ratio)
        print(f"  {r['Knote']}: Q/w_K = {float(ratio):+.10f}  ~ {f} (err {float(err):.2e})")

    print()
    print("Q(K) * w_K (product, since Q(i) has w_K=4):")
    for r in rows:
        Q = 12 * r["alpha_2"] * sqrt(abs(r["D_K"]))
        prod = Q * mpf(r["w_K"])
        f = Fraction(str(float(prod))).limit_denominator(1000)
        err = abs(mpf(f.numerator)/mpf(f.denominator) - prod)
        print(f"  {r['Knote']}: Q*w_K = {float(prod):+.10f}  ~ {f} (err {float(err):.2e})")

    # Alternative anchoring: instead of Hurwitz alpha_1=1/10, anchor each form
    # so that alpha_4 = something related to its CANONICAL period.
    # Recall Lozano-Robledo: BH^0_k = (2pi/sqrt|D|)^0 * e * L(psi^k, k) / Omega^k
    # for K = Q(sqrt-d), d not in {1,3}; the "e" is a normalization.
    # For d=1 we had H_4 = 1/10 (Hurwitz). For other K, the "Hurwitz" analogue
    # has different rational values.
    # Let's check: alpha_1 already varies! What is alpha_1 with the CHOWLA-SELBERG
    # canonical period?

    print()
    print("=" * 78)
    print("alpha_1(Hurwitz=1/10) IS the imposed normalization.")
    print("Question: does the canonical Chowla-Selberg period agree?")
    print("=" * 78)
    print()

    # Use the standard CS period of an elliptic curve over Q with CM by O_K.
    # For class number 1, the period of E/Q (or E/K) is determined up to QQ-bar.
    # For K=Q(i), N=4 form: A1 confirmed Omega_K^4 = (2pi)^4 / (10 * pi^3 * L(f,1)) =>
    # Omega_K = Gamma(1/4)^2/(2 sqrt(2 pi)) (Chowla-Selberg / Hurwitz).
    #
    # For K=Q(sqrt-7), N=7 form: the canonical CM elliptic curve has j=−3375 (the
    # famous one). Its period (real) is Omega_E ~ ???
    # From Chowla-Selberg: Omega_K = (2 pi)^{1/2} / sqrt(7) * prod ...

    # Actually let's not go there. The point is established by the Hurwitz-anchored test.

    # Try one more thing: PSLQ on alpha_2 itself with basis (1, 1/D, 1/sqrt(D), L(chi_D,1)/pi)
    print("Final PSLQ: alpha_2(K) on basis (1, 1/sqrt|D|, L(chi,1)/pi):")
    from sympy.ntheory.residue_ntheory import jacobi_symbol
    for r in rows:
        D = abs(r["D_K"])
        w = r["w_K"]
        h = r["h_K"]
        # Dirichlet: L(chi_D, 1) = 2 pi h / (w sqrt|D|)  for imag quad
        L_chi_1 = 2 * pi * h / (w * sqrt(D))
        a2 = r["alpha_2"]
        basis = [a2, mpf(1), mpf(1)/sqrt(D), L_chi_1 / pi, mpf(1)/(D)]
        rel = pslq(basis, tol=mpf("1e-25"), maxcoeff=10000)
        print(f"  {r['Knote']}: PSLQ on (a2, 1, 1/sqD, L(chi,1)/pi, 1/D) = {rel}")
        if rel and rel[0] != 0:
            # Decode: rel[0] * a2 + rel[1] * 1 + rel[2] / sqD + rel[3] L_chi/pi + rel[4]/D = 0
            print(f"    decoded: a2 = {-rel[1]/rel[0]} - {rel[2]/rel[0]}/sqrt(D) - {rel[3]/rel[0]}*L(chi,1)/pi - {rel[4]/rel[0]}/D")


if __name__ == "__main__":
    main()
