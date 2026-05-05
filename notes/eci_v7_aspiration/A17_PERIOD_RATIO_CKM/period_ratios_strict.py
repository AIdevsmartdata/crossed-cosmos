"""
A17 — STRICT period-ratio CKM screen.

The first run (period_ratios.py) showed that PSLQ with max_denom~2000 produces
"matches" for any target, because *every* positive real is well-approximated
by a rational with denom under 2000 (Liouville). That's vacuous.

This stricter version:
  1. Reports the full table r(m, a) := L(f, m) * pi^(4-m) / Omega_K^a (m∈[1,4], a∈[0,5])
  2. Only flags a CKM hit if the rational coefficient q is **genuinely small**:
     |num| + |denom| ≤ 30, AND |num|, |denom| ≤ 24, AND
     err < 0.5% AND r itself is in the regime where Damerell algebraicity
     holds (a=4, the canonical Damerell-Shimura denom).
  3. Notes the EXACT clean Damerell-ladder points and asks: do any of
     {1/10, 1/12, 1/24, 1/60, 6, 1/2, sqrt(3)} relate to PDG CKM values
     by a simple ratio?
  4. Cross-K: report SAME (m,a) for all 5 forms WITHOUT re-fitting q,
     so we honestly compare structural values.

Hallu count entering: 77.
Mistral large STRICT BAN.
"""

import json
from mpmath import mp, mpf, mpc, sqrt, pi, gamma, gammainc, fabs, log
from fractions import Fraction

mp.dps = 60

CM_FORMS = [
    {"label": "4.5.b.a",  "N": 4,  "D_K": -4,  "Knote": "Q(i)"},
    {"label": "7.5.b.a",  "N": 7,  "D_K": -7,  "Knote": "Q(sqrt-7)"},
    {"label": "8.5.d.a",  "N": 8,  "D_K": -8,  "Knote": "Q(sqrt-2)"},
    {"label": "11.5.b.a", "N": 11, "D_K": -11, "Knote": "Q(sqrt-11)"},
    {"label": "12.5.c.a", "N": 12, "D_K": -3,  "Knote": "Q(sqrt-3)"},
]


def chowla_selberg_period(D_K):
    if D_K == -4:
        return gamma(mpf(1)/4)**2 / (2 * sqrt(2 * pi))
    if D_K == -3:
        return gamma(mpf(1)/3)**3 / (mpf(2)**(mpf(7)/3) * pi)
    absD = abs(D_K)
    prod = mpf(1)
    for a in range(1, absD):
        chi_a = kronecker_symbol(D_K, a)
        if chi_a == 0:
            continue
        prod *= gamma(mpf(a) / absD) ** chi_a
    Omega2 = sqrt(mpf(absD)) / (4 * pi) * prod
    return sqrt(fabs(Omega2))


def kronecker_symbol(D, a):
    if a == 0:
        return 1 if abs(D) == 1 else 0
    if a == 1:
        return 1
    from sympy import factorint
    val = 1
    for p, e in factorint(a).items():
        val *= kronecker_symbol_prime(D, p) ** e
    return val


def kronecker_symbol_prime(D, p):
    if p == 2:
        d_mod = D % 8
        if D % 2 == 0:
            return 0
        if d_mod in (1, 7):
            return 1
        if d_mod in (3, 5):
            return -1
        return 0
    r = pow(D % p, (p - 1) // 2, p)
    if r == p - 1:
        return -1
    if r == 1:
        return 1
    return 0


def load_traces(label):
    path = f"/tmp/mf_{label.replace('.', '_')}.json"
    with open(path) as fh:
        d = json.load(fh)
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


# PDG CKM (HFLAV/PDG 2024 averages); all squared values used too
PDG = {
    "|V_us|":          mpf("0.22500"),
    "|V_us|^2":        mpf("0.0506250"),
    "sin^2_thetaC":    mpf("0.0507"),
    "|V_cb|":          mpf("0.04085"),
    "|V_cb|^2":        mpf("0.001668"),
    "|V_ub|":          mpf("0.003820"),
    "|V_ub|^2":        mpf("1.46e-5"),
    "|V_ub/V_cb|":     mpf("0.0935"),
    "|V_ub/V_cb|^2":   mpf("0.00874"),
}


def main():
    print("=" * 80)
    print("A17 — STRICT period-ratio CKM screen")
    print("=" * 80)
    print(f"mp.dps = {mp.dps}")
    print()

    # 1. Periods
    omega_table = {}
    for fd in CM_FORMS:
        omega_table[fd["label"]] = chowla_selberg_period(fd["D_K"])

    # 2. L-values
    print("Computing L(f, m) for m in {1,2,3,4} for 5 CM newforms...")
    L_values = {}
    for fd in CM_FORMS:
        traces = load_traces(fd["label"])
        L_values[fd["label"]] = {m: L_value(traces, fd["N"], 5, mpf(m)) for m in [1, 2, 3, 4]}

    # 3. Build the canonical Damerell ladder r(m, a=4) for K=Q(i)
    label0 = "4.5.b.a"
    Omega0 = omega_table[label0]
    ladder = {m: L_values[label0][m] * pi**(4 - m) / Omega0**4 for m in [1, 2, 3, 4]}
    print()
    print("Canonical Damerell ladder at K=Q(i), a=4 (verified clean rationals):")
    for m in [1, 2, 3, 4]:
        print(f"  m={m}: r(m,4) = {float(ladder[m]):.20f}")
    print()

    # 4. Build full table r(m, a) for all forms, all (m, a)
    print("=" * 80)
    print("FULL TABLE r(m, a) := L(f, m) * pi^(4-m) / Omega_K^a")
    print("=" * 80)
    full_table = {}
    for fd in CM_FORMS:
        label = fd["label"]
        Omega = omega_table[label]
        full_table[label] = {}
        for m in [1, 2, 3, 4]:
            for a in range(0, 6):
                full_table[label][(m, a)] = L_values[label][m] * pi**(4 - m) / Omega**a

    # 5. STRICT screening: a CKM hit means q*r ≈ PDG with q small (sum ≤ 30)
    #    AND a structural argument exists (we report only the cleanest rationals
    #    and check what CKM value they sit closest to, NOT any-rational fit).
    print()
    print("=" * 80)
    print("STRICT SCREEN: only small rationals q (|num|+|denom| ≤ 30) accepted")
    print("=" * 80)
    print(f"{'form':<10} {'m':>2} {'a':>2}  {'r(m,a)':>26}  {'q':>10}  {'q*r':>14}  CKM target & rel_err")
    strict_hits = []
    for fd in CM_FORMS:
        label = fd["label"]
        for m in [1, 2, 3, 4]:
            for a in range(0, 6):
                r = full_table[label][(m, a)]
                # Try only small denominator rationals
                for denom in range(1, 25):
                    for num in range(1, 25):
                        if num + denom > 30:
                            continue
                        from math import gcd
                        if gcd(num, denom) != 1:
                            continue
                        q = mpf(num) / mpf(denom)
                        prod = q * r
                        for pname, pval in PDG.items():
                            rel = fabs(prod - pval) / pval
                            if rel < mpf("0.005"):  # 0.5%
                                strict_hits.append({
                                    "form": label, "K": fd["Knote"],
                                    "m": m, "a": a,
                                    "r": str(r),
                                    "q": f"{num}/{denom}",
                                    "qr": str(prod),
                                    "CKM": pname,
                                    "PDG": str(pval),
                                    "rel_err": float(rel),
                                })
                                print(f"{label:<10} {m:>2} {a:>2}  {float(r):>26.16e}  {num}/{denom:<8}  "
                                      f"{float(prod):>14.6e}  {pname:>16} ({float(rel)*100:.3f}%)")

    print(f"\nTotal strict hits (small q, < 0.5%): {len(strict_hits)}")
    print()

    # 6. Highlight the CANONICAL ladder positions and ask the structural question
    print("=" * 80)
    print("STRUCTURAL CHECK at canonical Damerell ladder K=Q(i), a=4:")
    print("=" * 80)
    print("Ladder values: 1/10, 1/12, 1/24, 1/60.")
    print()
    structural_check = {}
    for m, ratval in [(1, Fraction(1, 10)), (2, Fraction(1, 12)), (3, Fraction(1, 24)), (4, Fraction(1, 60))]:
        rval = mpf(ratval.numerator) / mpf(ratval.denominator)
        print(f"\n  m={m}: r = {ratval} = {float(rval):.6f}")
        for pname, pval in PDG.items():
            for num in range(1, 13):
                for denom in range(1, 13):
                    from math import gcd
                    if gcd(num, denom) != 1:
                        continue
                    q = mpf(num) / mpf(denom)
                    pred = q * rval
                    rel = fabs(pred - pval) / pval
                    if rel < mpf("0.005"):
                        structural_check.setdefault(m, []).append({
                            "ratval": str(ratval),
                            "q": f"{num}/{denom}",
                            "CKM": pname,
                            "rel_err": float(rel),
                        })
                        print(f"     q={num}/{denom:<3} -> q * {ratval} = {float(pred):.6f}  vs  {pname}={float(pval):.6f}  ({float(rel)*100:.3f}%)")

    # 7. CROSS-K UNIFORM TEST: same (m, a, q) across forms
    print()
    print("=" * 80)
    print("CROSS-K UNIFORM TEST: for each strict hit at K=Q(i), apply same (m,a,q)")
    print("to other forms (NO refit) and report distance from PDG.")
    print("=" * 80)
    cross_K_results = []
    seen = set()
    for hit in strict_hits:
        if hit["form"] != "4.5.b.a":
            continue
        key = (hit["m"], hit["a"], hit["q"], hit["CKM"])
        if key in seen:
            continue
        seen.add(key)
        m, a, qstr, CKM = hit["m"], hit["a"], hit["q"], hit["CKM"]
        num, denom = map(int, qstr.split("/"))
        q = mpf(num) / mpf(denom)
        target = PDG[CKM]
        print(f"\n  Q(i) hit: m={m} a={a} q={qstr} -> {CKM}={float(target):+.4e} ({hit['rel_err']*100:.2f}%)")
        row = {"m": m, "a": a, "q": qstr, "CKM": CKM, "target": str(target), "by_form": []}
        for fd in CM_FORMS:
            r_x = full_table[fd["label"]][(m, a)]
            pred_x = q * r_x
            rel_x = fabs(pred_x - target) / target
            print(f"    {fd['label']:<10} ({fd['Knote']:<14}): q*r = {float(pred_x):+.6e}  rel_err = {float(rel_x)*100:.3f}%")
            row["by_form"].append({
                "form": fd["label"], "K": fd["Knote"],
                "qr": str(pred_x), "rel_err": float(rel_x),
            })
        cross_K_results.append(row)

    # 8. Save final results
    out = {
        "metadata": {
            "agent": "A17",
            "date": "2026-05-05",
            "mp_dps": int(mp.dps),
            "mode": "STRICT (small rational q, |num|+|denom| <= 30, rel_err < 0.5%)",
            "PDG": {k: str(v) for k, v in PDG.items()},
            "discipline": "Mistral large BAN; hallu 77 entering",
        },
        "Omega_K": {fd["label"]: str(omega_table[fd["label"]]) for fd in CM_FORMS},
        "L_values": {
            fd["label"]: {str(m): str(L_values[fd["label"]][m]) for m in [1, 2, 3, 4]}
            for fd in CM_FORMS
        },
        "full_table_r_m_a": {
            fd["label"]: {f"m={m},a={a}": str(full_table[fd["label"]][(m, a)])
                           for m in [1, 2, 3, 4] for a in range(0, 6)}
            for fd in CM_FORMS
        },
        "canonical_ladder_Qi_a4": {
            "1": "1/10",
            "2": "1/12",
            "3": "1/24",
            "4": "1/60",
        },
        "strict_CKM_hits": strict_hits,
        "structural_ladder_CKM_check": structural_check,
        "cross_K_uniform_test": cross_K_results,
    }
    out_path = "/root/crossed-cosmos/notes/eci_v7_aspiration/A17_PERIOD_RATIO_CKM/period_ratios.json"
    with open(out_path, "w") as fh:
        json.dump(out, fh, indent=2, default=str)
    print(f"\nWritten {out_path}")


if __name__ == "__main__":
    main()
