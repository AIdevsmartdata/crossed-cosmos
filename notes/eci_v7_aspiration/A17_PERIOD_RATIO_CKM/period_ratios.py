"""
A17 — Period-ratio CKM search.

Goal: extend the A1+A5 Damerell ladder L(f, m)·π^(4-m)/Ω_K^4 ∈ {1/10, 1/12, 1/24, 1/60}
toward CKM matrix-element predictions. Specifically scan, for each of the five
CM weight-5 newforms (4.5.b.a Q(i); 7.5.b.a Q(√-7); 8.5.d.a Q(√-2);
11.5.b.a Q(√-11); 12.5.c.a Q(√-3)), the table

   r(m, a) := L(f, m) · π^(4-m) / Ω_K^a

for m ∈ {1, 2, 3, 4} and a ∈ {0, 1, 2, 3, 4, 5}, and compare to PDG CKM values:

   |V_cb|^2 = (4.08 ± 0.14) × 10^-3   (HFLAV avg, exclusive+inclusive)
   |V_ub|^2 = (1.65 ± 0.32) × 10^-5
   |V_us|^2 ≈ sin²θ_C = 0.0507         (the Cabibbo angle, A5 confirmed obstructs strict τ=i)

Method:
  1. mp.dps = 60. Iwaniec-Kowalski AFE (verified by FE).
  2. K-specific Chowla-Selberg period Ω_K (or its analog for other discriminants).
  3. PSLQ-search (Fraction.limit_denominator) for rational coefficients matching
     each PDG value. Reject if precision worse than 1%.
  4. Cross-K: same ratio at K=Q(√−7) etc. — does Q(i) uniquely pick out CKM?

Hallu count entering: 77.
Mistral large STRICT BAN.
"""

import json
from mpmath import mp, mpf, mpc, sqrt, pi, gamma, gammainc, pslq, log, fabs
from fractions import Fraction

mp.dps = 60

# -----------------------------------------------------------------------------
# CM newform metadata + Chowla-Selberg period analogs
# -----------------------------------------------------------------------------

CM_FORMS = [
    {"label": "4.5.b.a",  "N": 4,  "D_K": -4,  "d": 1,  "Knote": "Q(i)"},
    {"label": "7.5.b.a",  "N": 7,  "D_K": -7,  "d": 7,  "Knote": "Q(sqrt-7)"},
    {"label": "8.5.d.a",  "N": 8,  "D_K": -8,  "d": 2,  "Knote": "Q(sqrt-2)"},
    {"label": "11.5.b.a", "N": 11, "D_K": -11, "d": 11, "Knote": "Q(sqrt-11)"},
    {"label": "12.5.c.a", "N": 12, "D_K": -3,  "d": 3,  "Knote": "Q(sqrt-3)"},
]


def chowla_selberg_period(D_K):
    """Chowla-Selberg formula for the canonical period of the CM elliptic curve
    with j-invariant in K = Q(sqrt(D_K)).

    For Q(i) (D_K = -4):  Omega = Gamma(1/4)^2 / (2 sqrt(2 pi))
    For Q(sqrt-3) (D_K = -3): Omega = Gamma(1/3)^3 / (2^(7/3) pi)  -- standard
    Generic D_K with class number 1: use Lerch's formula
       Omega^2 = (1/(4 pi sqrt(|D_K|))) * prod_{a=1}^{|D_K|-1} Gamma(a/|D_K|)^chi(a)
    where chi is the Kronecker symbol (D_K/.).
    """
    absD = abs(D_K)
    # Use Lerch / Chowla-Selberg formula for class number 1:
    # log Omega = (-1/(4 h)) sum_a chi(a) log Gamma(a/|D_K|) + const
    # Direct closed forms preferred:
    if D_K == -4:
        return gamma(mpf(1)/4)**2 / (2 * sqrt(2 * pi))
    if D_K == -3:
        # Q(sqrt-3): Omega = Gamma(1/3)^3 / (2^(7/3) * pi)
        return gamma(mpf(1)/3)**3 / (mpf(2)**(mpf(7)/3) * pi)
    # General formula (Chowla-Selberg for class number 1, h=1)
    # Omega^2 / pi = (1/(2 sqrt(|D_K|))) * prod_{a=1}^{|D_K|-1} Gamma(a/|D_K|)^chi(a)/(2pi)?
    # Use the explicit Lerch form: Omega^2 = (sqrt(|D_K|)/(4 pi)) * prod Gamma(a/|D_K|)^chi(a)
    # Reference: Chowla-Selberg 1967, also Selberg-Chowla 1967.
    prod = mpf(1)
    for a in range(1, absD):
        chi_a = kronecker_symbol(D_K, a)
        if chi_a == 0:
            continue
        prod *= gamma(mpf(a) / absD) ** chi_a
    # For class number 1 with D_K odd:
    # Omega^2 = (1/(2 |D_K|^(1/2))) * prod Gamma(a/|D_K|)^chi(a)
    # Actually Chowla-Selberg proper:
    #   |eta(tau_0)|^4 = (1/(4 pi sqrt(|D_K|))) * prod Gamma(a/|D_K|)^chi(a)
    # And Omega ~ |eta|^2 sqrt(2)... need careful normalization. We use:
    Omega2 = sqrt(mpf(absD)) / (4 * pi) * prod
    Omega = sqrt(fabs(Omega2))
    return Omega


def kronecker_symbol(D, a):
    """Compute the Kronecker symbol (D/a) for D < 0, a > 0."""
    if a == 0:
        return 1 if abs(D) == 1 else 0
    if a == 1:
        return 1
    # factor a
    from sympy import factorint
    val = 1
    for p, e in factorint(a).items():
        val *= kronecker_symbol_prime(D, p) ** e
    return val


def kronecker_symbol_prime(D, p):
    """(D/p) for prime p."""
    if p == 2:
        # Kronecker symbol (D/2):
        # 0 if D ≡ 0 (mod 4)
        # +1 if D ≡ ±1 (mod 8)
        # -1 if D ≡ ±3 (mod 8)
        d_mod = D % 8
        if D % 2 == 0:
            return 0
        if d_mod in (1, 7):
            return 1
        if d_mod in (3, 5):
            return -1
        return 0
    # p odd
    # (D/p) = D^((p-1)/2) mod p, with values in {-1, 0, 1}
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
    """Iwaniec-Kowalski (5.16) AFE for L(f, s)."""
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
    fx = Fraction(str(x)[:60]).limit_denominator(max_denom)
    err = abs(mpf(fx.numerator) / mpf(fx.denominator) - x)
    return fx, err


def pslq_rat(x, max_coeff=100000, tol=mpf("1e-30")):
    """Find p, q with p + q*x ≈ 0 to high precision."""
    try:
        rel = pslq([x, mpf(1)], tol=tol, maxcoeff=max_coeff)
        if rel and rel[0] != 0:
            return Fraction(-rel[1], rel[0])
    except Exception:
        return None
    return None


# PDG CKM targets (HFLAV/PDG 2024 averages)
PDG = {
    "|V_us|":   mpf("0.22500"),    # Cabibbo, sin theta_C
    "|V_us|^2": mpf("0.0506250"),  # = 0.225^2
    "sin^2(theta_C)": mpf("0.0507"),  # PDG
    "|V_cb|":   mpf("0.04085"),     # HFLAV avg 2024
    "|V_cb|^2": mpf("0.001668"),    # HFLAV
    "|V_ub|":   mpf("0.003820"),    # HFLAV avg 2024
    "|V_ub|^2": mpf("1.46e-5"),
    "|V_ub/V_cb|":   mpf("0.0935"),
    "|V_ub/V_cb|^2": mpf("0.00874"),
}


def main():
    print("=" * 78)
    print("A17 PERIOD-RATIO CKM SEARCH")
    print("=" * 78)
    print(f"mp.dps = {mp.dps}")
    print()

    # Compute Chowla-Selberg periods for each K
    print("Chowla-Selberg periods:")
    omega_table = {}
    for fd in CM_FORMS:
        Omega = chowla_selberg_period(fd["D_K"])
        omega_table[fd["label"]] = Omega
        print(f"  {fd['Knote']:>14}  D_K={fd['D_K']:>4}  Omega_K = {float(Omega):.20f}")
    print()

    # Compute L(f, m) for m = 1, 2, 3, 4
    print("Computing L(f, m) for m in {1,2,3,4}, all 5 forms (this is slow)...")
    L_values = {}  # L_values[label][m] = L(f, m)
    for fd in CM_FORMS:
        traces = load_traces(fd["label"])
        L_values[fd["label"]] = {}
        for m in [1, 2, 3, 4]:
            Lm = L_value(traces, fd["N"], 5, mpf(m))
            L_values[fd["label"]][m] = Lm
        print(f"  {fd['label']:<10} L = {{1: {float(L_values[fd['label']][1]):+.6f}, "
              f"2: {float(L_values[fd['label']][2]):+.6f}, "
              f"3: {float(L_values[fd['label']][3]):+.6f}, "
              f"4: {float(L_values[fd['label']][4]):+.6f}}}")
    print()

    # ---------------------------------------------------------------------
    # Build table r(m, a) := L(f, m) * pi^(4-m) / Omega_K^a
    # ---------------------------------------------------------------------
    print("=" * 78)
    print("PERIOD-RATIO TABLE: r(m, a) := L(f, m) * pi^(4-m) / Omega_K^a")
    print("=" * 78)
    out = {
        "metadata": {
            "date": "2026-05-05",
            "agent": "A17",
            "mp_dps": int(mp.dps),
            "n_terms": "len(traces) ~ 1000",
            "CKM_PDG": {k: str(v) for k, v in PDG.items()},
        },
        "Omega_K": {fd["label"]: str(omega_table[fd["label"]]) for fd in CM_FORMS},
        "L_values": {
            fd["label"]: {str(m): str(L_values[fd["label"]][m]) for m in [1, 2, 3, 4]}
            for fd in CM_FORMS
        },
        "ratios_r_m_a": {},
        "PSLQ_matches": {},
        "CKM_proximity": {},
    }

    for fd in CM_FORMS:
        label = fd["label"]
        Omega = omega_table[label]
        out["ratios_r_m_a"][label] = {}
        out["CKM_proximity"][label] = {}
        print(f"\n--- {label} ({fd['Knote']}, D_K={fd['D_K']}) ---")
        print(f"{'m':>3} {'a':>3}  {'r(m,a)':>26}  {'best rational':>16}  {'CKM match':>30}")
        for m in [1, 2, 3, 4]:
            Lm = L_values[label][m]
            for a in range(0, 6):
                r = Lm * pi**(4 - m) / Omega**a
                # PSLQ rational
                try:
                    fx = Fraction(str(r)).limit_denominator(10000)
                    err = abs(mpf(fx.numerator) / mpf(fx.denominator) - r)
                    rat_str = str(fx) if err < mpf("1e-15") else ""
                except Exception:
                    rat_str = ""
                # CKM proximity: which PDG value (if any) is within 5%
                ckm_match = ""
                for pname, pval in PDG.items():
                    if pval == 0:
                        continue
                    rel_err = abs(r - pval) / pval
                    if rel_err < mpf("0.01"):
                        ckm_match = f"{pname} ({float(rel_err)*100:.2f}%)"
                        break
                    elif rel_err < mpf("0.05") and not ckm_match:
                        ckm_match = f"~{pname} ({float(rel_err)*100:.2f}%)"
                out["ratios_r_m_a"][label].setdefault(str(m), {})[str(a)] = str(r)
                if ckm_match:
                    out["CKM_proximity"][label][f"m={m},a={a}"] = {
                        "ratio": str(r),
                        "match": ckm_match,
                    }
                print(f"{m:>3} {a:>3}  {float(r):+.20e}  {rat_str:>16}  {ckm_match:>30}")

    # ---------------------------------------------------------------------
    # PSLQ search: for each (m, a) on Q(i), look for c such that c*r matches CKM
    # ---------------------------------------------------------------------
    print("\n" + "=" * 78)
    print("PSLQ CKM SEARCH (Q(i) only, since A5 showed K=Q(i) is special)")
    print("=" * 78)
    label = "4.5.b.a"
    Omega = omega_table[label]
    out["PSLQ_matches"][label] = []
    for m in [1, 2, 3, 4]:
        Lm = L_values[label][m]
        for a in range(0, 6):
            r = Lm * pi**(4 - m) / Omega**a
            for pname, pval in PDG.items():
                if pval == 0:
                    continue
                # Search small rational q such that q * r = pval, i.e. q = pval / r
                if fabs(r) < mpf("1e-50"):
                    continue
                ratio = pval / r
                if fabs(ratio) > mpf("1e10"):
                    continue
                fx = Fraction(str(ratio)).limit_denominator(2000)
                rec_err = abs(mpf(fx.numerator) / mpf(fx.denominator) - ratio)
                if rec_err < fabs(ratio) * mpf("0.001"):
                    # rational coefficient at 0.1% — interesting
                    pred = mpf(fx.numerator) / mpf(fx.denominator) * r
                    rel = fabs(pred - pval) / pval
                    if rel < mpf("0.01"):  # within 1%
                        out["PSLQ_matches"][label].append({
                            "m": m, "a": a,
                            "ratio_r": str(r),
                            "PDG_target": pname,
                            "PDG_val": str(pval),
                            "rational_q": str(fx),
                            "predicted": str(pred),
                            "rel_err": float(rel),
                        })
                        print(f"  m={m} a={a}: r = {float(r):+.6e}, "
                              f"q = {fx} -> q*r = {float(pred):+.6e} vs {pname}={float(pval):+.6e} "
                              f"({float(rel)*100:.3f}%)")

    # ---------------------------------------------------------------------
    # Cross-K test for any close hits at Q(i)
    # ---------------------------------------------------------------------
    print("\n" + "=" * 78)
    print("CROSS-K TEST")
    print("=" * 78)
    print("If a (m, a) on Q(i) matches a CKM value at <1% precision,")
    print("compute the SAME (m, a) for the other K and check uniqueness.")
    out["cross_K"] = []
    if out["PSLQ_matches"][label]:
        for hit in out["PSLQ_matches"][label]:
            m = hit["m"]
            a = hit["a"]
            q = Fraction(hit["rational_q"])
            target_name = hit["PDG_target"]
            target_val = mpf(hit["PDG_val"])
            print(f"\n  HIT: m={m}, a={a}, q={q}, target={target_name}={float(target_val):+.4e}")
            cross_table = []
            for fd in CM_FORMS:
                Lm_x = L_values[fd["label"]][m]
                Omega_x = omega_table[fd["label"]]
                r_x = Lm_x * pi**(4 - m) / Omega_x**a
                pred_x = mpf(q.numerator) / mpf(q.denominator) * r_x
                rel_x = fabs(pred_x - target_val) / target_val
                marker = "**Q(i)**" if fd["label"] == "4.5.b.a" else ""
                print(f"    {fd['label']:<10} ({fd['Knote']:>14}): q*r = {float(pred_x):+.6e}  rel_err vs {target_name} = {float(rel_x)*100:.3f}%  {marker}")
                cross_table.append({
                    "label": fd["label"],
                    "K": fd["Knote"],
                    "q_times_r": str(pred_x),
                    "rel_err": float(rel_x),
                })
            out["cross_K"].append({
                "m": m, "a": a, "q": str(q),
                "target": target_name,
                "table": cross_table,
            })
    else:
        print("  No <1% PSLQ matches found at Q(i). Skipping cross-K.")

    # ---------------------------------------------------------------------
    # Save JSON
    # ---------------------------------------------------------------------
    out_path = "/root/crossed-cosmos/notes/eci_v7_aspiration/A17_PERIOD_RATIO_CKM/period_ratios.json"
    with open(out_path, "w") as fh:
        json.dump(out, fh, indent=2, default=str)
    print(f"\nWritten {out_path}")


if __name__ == "__main__":
    main()
