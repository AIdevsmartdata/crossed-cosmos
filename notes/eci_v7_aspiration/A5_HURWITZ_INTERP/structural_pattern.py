"""
A5 / structural_pattern.py — Look for structural pattern in alpha_2 across K.

Hypothesis 1: alpha_2(K) = 1/(12 * sqrt(|D_K|/4)) ??
Hypothesis 2: alpha_2(K) = 1/(12 * w_K * h_K) for various K? ??
Hypothesis 3: alpha_2(K) = (some Bernoulli quotient over K) ?

We test these against the numerical alpha_2 values.

Note: when we Hurwitz-anchor alpha_1 := 1/10 across all K, we are picking a
period for K which may NOT be the canonical CM period. The "true" structural
question is: with the *correct* canonical period Omega_K (from Chowla-Selberg
or from the L-function central value), what is alpha_2(K)?

Better test: use PSLQ with multiple algebraic candidates.
"""
from mpmath import mp, mpf, mpc, sqrt, pi, gamma, gammainc, pslq
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


def chowla_selberg_period_h1(d):
    """For class-number-1 K = Q(sqrt-d), d in {1,2,3,7,11,19,43,67,163}:
    Returns the canonical period Omega_K of the CM elliptic curve y^2 = ... over K.
    Formula (Schertz 2010, Selberg-Chowla):
        Omega_K = sqrt(pi) * prod_{a=1}^{|D|-1} Gamma(a/|D|)^{chi(a)} / (2 sqrt(|D|))
    Actually multiple conventions exist; we use the one giving Omega_Qi = ϖ = Gamma(1/4)^2/(2 sqrt(pi))
    --- this is the LEMNISCATE constant, NOT the half-period of the standard model.

    For K=Q(i): Omega_K (canonical) = Gamma(1/4)^2 / (2 sqrt(pi)) = ϖ ≈ 2.622... no wait
    that's 5.244... Let me be precise:
        Lemniscate constant ϖ = 2 int_0^1 dt/sqrt(1-t^4) = Gamma(1/4)^2/(2 sqrt(2 pi))
                              = 2.62205755...
        In Hurwitz convention this is the full period.
    """
    from sympy.ntheory.residue_ntheory import jacobi_symbol
    if d == 1: D = -4
    elif d == 2: D = -8
    elif d == 3: D = -3
    elif d in (7, 11, 19, 43, 67, 163): D = -d
    else: return None
    absD = abs(D)
    h = 1
    w = {1: 4, 2: 2, 3: 6, 7: 2, 11: 2}[d]
    # chi = (D/.) = Kronecker symbol mod absD
    def chi(a):
        if a == 0: return 0
        if absD % 2 == 0:  # D = -4 or -8
            if a % 2 == 0: return 0
            if D == -4: return jacobi_symbol(-1, a)
            if D == -8:  # (-8/a) = (-2/a)
                return jacobi_symbol(-2, a)
        else:
            return jacobi_symbol(D, a)
    # Schertz Thm 6.3.1: Omega_K = (1/sqrt(2 pi |D|)) * prod_a Gamma(a/|D|)^{chi(a) w / (2h)}
    prod_log = mpf(0)
    from mpmath import log
    for a in range(1, absD):
        c = chi(a)
        if c != 0:
            prod_log += c * log(gamma(mpf(a)/absD))
    prod = mpf(1) * (prod_log * mpf(w) / mpf(2 * h)).exp()
    Omega = (mpf(1) / sqrt(2 * pi * absD)) * prod
    return Omega


CM_FORMS = [
    {"label": "4.5.b.a",  "N": 4,  "D_K": -4,  "d": 1,  "w_K": 4, "h_K": 1, "Knote": "Q(i)"},
    {"label": "7.5.b.a",  "N": 7,  "D_K": -7,  "d": 7,  "w_K": 2, "h_K": 1, "Knote": "Q(sqrt-7)"},
    {"label": "8.5.d.a",  "N": 8,  "D_K": -8,  "d": 2,  "w_K": 2, "h_K": 1, "Knote": "Q(sqrt-2)"},
    {"label": "11.5.b.a", "N": 11, "D_K": -11, "d": 11, "w_K": 2, "h_K": 1, "Knote": "Q(sqrt-11)"},
    {"label": "12.5.c.a", "N": 12, "D_K": -3,  "d": 3,  "w_K": 6, "h_K": 1, "Knote": "Q(sqrt-3)"},
]


def main():
    print("=" * 78)
    print("A5: structural pattern of alpha_2 across CM weight-5 newforms")
    print("=" * 78)

    rows = []
    for fd in CM_FORMS:
        traces = load_traces(fd["label"])
        L1 = L_value(traces, fd["N"], 5, mpf(1))
        L2 = L_value(traces, fd["N"], 5, mpf(2))
        # Hurwitz-anchored alpha_2 (each K with its own period set so alpha_1=1/10):
        a2_hurw = L2 / (L1 * pi * mpf(10))
        rows.append({
            "label": fd["label"], "Knote": fd["Knote"],
            "D_K": fd["D_K"], "d": fd["d"],
            "w_K": fd["w_K"], "h_K": fd["h_K"],
            "L1": L1, "L2": L2,
            "alpha_2_hurw": a2_hurw,
        })

    # Look for: alpha_2 = ? * (1/12) for some K-dependent factor
    print()
    print(f"{'K':>12} {'D_K':>5} {'w_K':>5} {'h_K':>5} {'alpha_2(Hurwitz)':>20} {'12*alpha_2':>12} {'sqrt|D|*alpha_2*12':>20}")
    for r in rows:
        a2 = r["alpha_2_hurw"]
        f1 = 12 * a2
        f2 = sqrt(abs(r["D_K"])) * a2 * 12
        print(f"{r['Knote']:>12} {r['D_K']:>5} {r['w_K']:>5} {r['h_K']:>5} {float(a2):>20.14f} {float(f1):>12.8f} {float(f2):>20.10f}")

    print()
    print("Hypothesis tests (12 * alpha_2 = ?):")
    for r in rows:
        a2 = r["alpha_2_hurw"]
        candidates = {
            "1": mpf(1),
            "2/sqrt|D|": 2 / sqrt(abs(r["D_K"])),
            "4/sqrt|D|": 4 / sqrt(abs(r["D_K"])),
            "w_K/sqrt|D|": mpf(r["w_K"]) / sqrt(abs(r["D_K"])),
            "w_K * 2/(|D|)": 2 * mpf(r["w_K"]) / abs(r["D_K"]),
            "(2/sqrt|D|)^2": 4 / abs(r["D_K"]),
            "1/sqrt|D|": 1 / sqrt(abs(r["D_K"])),
        }
        f1 = 12 * a2
        print(f"  {r['Knote']}:  12*alpha_2 = {float(f1):+.10f}")
        for name, val in candidates.items():
            if abs(f1 - val) < mpf("1e-4"):
                print(f"    MATCH: 12*alpha_2 ~ {name} = {float(val):+.10f}")

    # Try the ratio alpha_2(K) / alpha_2(Q(i)) — does it follow simple K-dependence?
    print()
    print("Ratios alpha_2(K) / alpha_2(Q(i)):")
    a2_qi = next(r["alpha_2_hurw"] for r in rows if r["d"] == 1)
    for r in rows:
        ratio = r["alpha_2_hurw"] / a2_qi
        print(f"  {r['Knote']}: ratio = {float(ratio):+.10f}")
        # Test: is ratio = sqrt|D_K|/2?
        cand = sqrt(abs(r["D_K"])) / 2
        print(f"    test sqrt|D_K|/2 = {float(cand):+.10f}")
        # Test: is ratio related to L(chi, 1) where chi is the Kronecker character?
        # L(chi_D, 1) = pi h_K w_K / (sqrt|D| * something) -- Dirichlet class number formula
        # For class-number-1 imag quadratic: L(chi_D, 1) = 2 pi h_K / (w_K sqrt|D_K|)
        L_chi_1 = 2 * pi * mpf(r["h_K"]) / (mpf(r["w_K"]) * sqrt(abs(r["D_K"])))
        print(f"    L(chi_D, 1) (Dirichlet) = {float(L_chi_1):+.10f}")
        # Test: ratio * L(chi, 1) = const?
        prod = ratio * L_chi_1
        print(f"    ratio * L(chi,1) = {float(prod):+.10f}")

    # PSLQ multi-search: find rational a, b s.t. alpha_2 = a/b * (some K-dep base)
    print()
    print("PSLQ search: alpha_2(K) vs combinations of sqrt|D|, w_K, h_K, pi, ...")
    for r in rows:
        a2 = r["alpha_2_hurw"]
        D = mpf(abs(r["D_K"]))
        sqD = sqrt(D)
        candidates_basis = [a2, mpf(1)/12, mpf(1)/(12*sqD), mpf(1)/(D*12)]
        rel = pslq(candidates_basis, tol=mpf("1e-25"), maxcoeff=10000)
        print(f"  {r['Knote']}: alpha_2 vs (1/12, 1/(12 sqD), 1/(12 D)) PSLQ = {rel}")


if __name__ == "__main__":
    main()
