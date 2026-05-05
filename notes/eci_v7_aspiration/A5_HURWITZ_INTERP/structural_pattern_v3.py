"""
A5 / structural_pattern_v3.py — Use the CANONICAL Chowla-Selberg period
for each K, then test alpha_1, alpha_2, alpha_3, alpha_4 directly.

The Chowla-Selberg period is defined for a CM elliptic curve E/K with
End(E) = O_K and the discriminant of E "minimal" in a Q-bar sense. Its real
period is

  Omega_K^CS = (1/sqrt(2 pi |D_K|)) * prod_{a=1}^{|D|-1} Gamma(a/|D|)^{chi_D(a) * w/(2h)}

where w = |O_K^*|, h = h_K, chi_D = Kronecker character mod |D|.

For class-number-1 K (d in {1,2,3,7,11,19,43,67,163}):
  d=1:  D=-4,  w=4,  h=1
  d=2:  D=-8,  w=2,  h=1
  d=3:  D=-3,  w=6,  h=1
  d=7:  D=-7,  w=2,  h=1
  d=11: D=-11, w=2,  h=1
"""
from mpmath import mp, mpf, sqrt, pi, gamma, gammainc, log, exp, pslq
from sympy.ntheory.residue_ntheory import jacobi_symbol
from fractions import Fraction
import json

mp.dps = 80


def kron_chi(D, a):
    """Kronecker (D|a) for D = fundamental discriminant of imag quadratic field, a int."""
    if a == 0: return 0
    if a == 1: return 1
    # D < 0
    absD = abs(D)
    # Pull out 2's from a
    s = 1
    while a % 2 == 0:
        a //= 2
        # (D|2) for D < 0:
        if absD % 8 in (1, 7):
            pass  # (D|2) = +1
        elif absD % 8 in (3, 5):
            s = -s
        else:
            return 0  # D even, (D|2) = 0
    if a == 1:
        return s
    # a is now odd > 1
    return s * jacobi_symbol(D, a)


def chowla_selberg_period(d):
    """Class-number-1 imag quadratic Chowla-Selberg period."""
    if d == 1:   D, w, h = -4, 4, 1
    elif d == 2: D, w, h = -8, 2, 1
    elif d == 3: D, w, h = -3, 6, 1
    elif d == 7: D, w, h = -7, 2, 1
    elif d == 11: D, w, h = -11, 2, 1
    else: raise ValueError(f"d={d} not class-number-1")
    absD = abs(D)
    log_prod = mpf(0)
    for a in range(1, absD):
        c = kron_chi(D, a)
        if c != 0:
            log_prod += c * log(gamma(mpf(a)/absD))
    # Omega = (1/sqrt(2 pi |D|)) * exp((w/(2h)) * log_prod)
    Omega = (mpf(1) / sqrt(2 * pi * absD)) * exp(log_prod * mpf(w) / mpf(2 * h))
    return Omega, D, w, h


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
    {"label": "4.5.b.a",  "N": 4,  "d": 1,  "Knote": "Q(i)"},
    {"label": "7.5.b.a",  "N": 7,  "d": 7,  "Knote": "Q(sqrt-7)"},
    {"label": "8.5.d.a",  "N": 8,  "d": 2,  "Knote": "Q(sqrt-2)"},
    {"label": "11.5.b.a", "N": 11, "d": 11, "Knote": "Q(sqrt-11)"},
    {"label": "12.5.c.a", "N": 12, "d": 3,  "Knote": "Q(sqrt-3)"},
]


def main():
    # Sanity: Q(i) Chowla-Selberg should give the lemniscate period (~2.622)
    print("=" * 78)
    print("Sanity: Chowla-Selberg periods for class-number-1 K")
    print("=" * 78)
    for fd in CM_FORMS:
        Omega, D, w, h = chowla_selberg_period(fd["d"])
        print(f"  {fd['Knote']:<12}: D={D}, w={w}, h={h}, Omega_K(CS) = {float(Omega):.10f}")

    print()
    print("Note Q(i) target: Gamma(1/4)^2 / (2 sqrt(2 pi)) = ", float(gamma(mpf(1)/4)**2/(2*sqrt(2*pi))))

    # Now: compute alpha_m = L(f, m) * pi^(4-m) / Omega^4 with the *CS period*
    print()
    print("=" * 78)
    print("alpha_m using canonical Chowla-Selberg period for each K")
    print("=" * 78)
    print(f"{'K':<12} {'D_K':>5} {'alpha_1':>20} {'alpha_2':>20} {'alpha_3':>20} {'alpha_4':>20}")
    rows = []
    for fd in CM_FORMS:
        traces = load_traces(fd["label"])
        Omega, D, w, h = chowla_selberg_period(fd["d"])
        L1 = L_value(traces, fd["N"], 5, mpf(1))
        L2 = L_value(traces, fd["N"], 5, mpf(2))
        L3 = L_value(traces, fd["N"], 5, mpf(3))
        L4 = L_value(traces, fd["N"], 5, mpf(4))
        a1 = L1 * pi**3 / Omega**4
        a2 = L2 * pi**2 / Omega**4
        a3 = L3 * pi    / Omega**4
        a4 = L4         / Omega**4
        rows.append({**fd, "Omega": Omega, "D_K": D, "w": w, "h": h,
                     "L1": L1, "L2": L2, "L3": L3, "L4": L4,
                     "a1": a1, "a2": a2, "a3": a3, "a4": a4})
        print(f"{fd['Knote']:<12} {D:>5} {float(a1):>20.10f} {float(a2):>20.10f} "
              f"{float(a3):>20.10f} {float(a4):>20.10f}")

    print()
    print("Search for clean rationals via PSLQ + brute Fraction:")
    for r in rows:
        print(f"\n  {r['Knote']} (D_K={r['D_K']}, w={r['w']}):")
        for label, val in [("a1", r["a1"]), ("a2", r["a2"]),
                            ("a3", r["a3"]), ("a4", r["a4"])]:
            # First brute Fraction
            f = Fraction(str(float(val))).limit_denominator(5000)
            err = abs(mpf(f.numerator)/mpf(f.denominator) - val)
            # Also try multiplied by w / (some power of |D|)
            f2 = Fraction(str(float(val * r["w"]))).limit_denominator(5000)
            err2 = abs(mpf(f2.numerator)/mpf(f2.denominator) - val * r["w"])
            print(f"    {label} = {float(val):+.14f}, ~ {f} (err {float(err):.2e}); "
                  f"a*w = {float(val*r['w']):+.10f} ~ {f2}")

    # KEY question: for K=Q(i), Q(sqrt-3) (the d's excluded by Lozano-Robledo),
    # is alpha_2 = 1/12 specifically?

    print()
    print("=" * 78)
    print("Verdict on alpha_2 = 1/12 universality")
    print("=" * 78)
    target = mpf(1)/12
    print(f"Target: alpha_2 = 1/12 = {float(target):.14f}")
    print()
    for r in rows:
        diff = r["a2"] - target
        print(f"  {r['Knote']:<12}: alpha_2 = {float(r['a2']):.14f}, diff from 1/12 = {float(diff):+.6f}")


if __name__ == "__main__":
    main()
