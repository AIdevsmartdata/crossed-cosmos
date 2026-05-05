"""
A62 — SYSTEMATIC CKM extension of A17 K=Q(i) Damerell-ladder search.

A17 found two clean hits at K=Q(i):
  |V_us|     = (9/4) · α_1                = 9/40   = 0.22500   → 0.015 σ
  |V_cb|^2   = α_1 · α_4                  = 1/600  = 0.001667  → 0.024 σ

with α_m ∈ {1/10, 1/12, 1/24, 1/60} for m ∈ {1,2,3,4}.

A62 systematically extends to:
  - all double  α_i · α_j        for i,j ∈ {1,2,3,4}
  - all triple  α_i · α_j · α_k  for i,j,k ∈ {1,2,3,4}
  - α_i · π^k     for k ∈ {-3..3}
  - α_i · √n      for small n
  - all CKM targets including |V_ub|, |V_td|, |V_tb|, J_CKM and ratios.
  - small-q PSLQ-style search:  q · (algebraic-expr) ≈ |V_X|^n
                                with q rational, |num|+|denom| ≤ N_max
  - cross-K test: re-build α_m at K = Q(√-2), Q(√-3), Q(√-7), Q(√-11)
    using the SAME (m,a) recipe, see if same q hits same target.

Hallu count entering: 85.
mp.dps = 60. Mistral large STRICT BAN.
Honest framing: any q hit is EMPIRICAL — small-q coincidences are common.
"""

import json
import os
from fractions import Fraction
from math import gcd

from mpmath import mp, mpf, sqrt, pi, gamma, gammainc, fabs

mp.dps = 60

# ----------------------------------------------------------------------------
# CM forms and Chowla–Selberg periods (mirroring A17)
# ----------------------------------------------------------------------------
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


def L_value(traces, N_level, weight, s):
    s = mpf(s)
    k = mpf(weight)
    sqrt_N = sqrt(mpf(N_level))
    two_pi = 2 * pi
    Gs = gamma(s)
    Gks = gamma(k - s)
    cutoff1 = two_pi / sqrt_N
    cutoff2 = two_pi / sqrt_N
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


# ----------------------------------------------------------------------------
# PDG / HFLAV CKM values (2024 averages)
# ----------------------------------------------------------------------------
PDG = {
    # element                value          1-sigma uncertainty
    "|V_us|":        (mpf("0.22501"),    mpf("0.00068")),
    "|V_cb|":        (mpf("0.04183"),    mpf("0.00079")),
    "|V_ub|":        (mpf("0.003820"),   mpf("0.00020")),
    "|V_td|":        (mpf("0.00858"),    mpf("0.00026")),
    "|V_tb|":        (mpf("1.0140"),     mpf("0.0290")),  # PDG combined unitarity
    "|V_us|^2":      (mpf("0.22501")**2, 2 * mpf("0.22501") * mpf("0.00068")),
    "|V_cb|^2":      (mpf("0.04183")**2, 2 * mpf("0.04183") * mpf("0.00079")),
    "|V_ub|^2":      (mpf("0.003820")**2, 2 * mpf("0.003820") * mpf("0.00020")),
    "|V_td|^2":      (mpf("0.00858")**2, 2 * mpf("0.00858") * mpf("0.00026")),
    "|V_tb|^2":      (mpf("1.0140")**2,  2 * mpf("1.0140") * mpf("0.0290")),
    "|V_ub/V_cb|":   (mpf("0.003820") / mpf("0.04183"),
                       mpf("0.003820") / mpf("0.04183")
                       * sqrt((mpf("0.00020")/mpf("0.003820"))**2
                              + (mpf("0.00079")/mpf("0.04183"))**2)),
    "|V_td/V_ts|":   (mpf("0.2050"),     mpf("0.0070")),
    "|V_td/V_cb|":   (mpf("0.00858") / mpf("0.04183"),
                       mpf("0.00858") / mpf("0.04183")
                       * sqrt((mpf("0.00026")/mpf("0.00858"))**2
                              + (mpf("0.00079")/mpf("0.04183"))**2)),
    "|V_us|*|V_cb|": (mpf("0.22501") * mpf("0.04183"),
                       mpf("0.22501") * mpf("0.04183")
                       * sqrt((mpf("0.00068")/mpf("0.22501"))**2
                              + (mpf("0.00079")/mpf("0.04183"))**2)),
    "J_CKM":         (mpf("3.18e-5"),    mpf("0.15e-5")),
    # sin theta_C
    "sin_thetaC":    (mpf("0.22501"),    mpf("0.00068")),
    # Wolfenstein lambda^2 (used in Bjorken)
    "lambda^2":      (mpf("0.22501")**2, 2 * mpf("0.22501") * mpf("0.00068")),
    # |V_us|^2 + |V_cb|^2 first-row + 23 sum
    "|V_us|^2+|V_cb|^2": (mpf("0.22501")**2 + mpf("0.04183")**2,
                          sqrt((2*mpf("0.22501")*mpf("0.00068"))**2
                               + (2*mpf("0.04183")*mpf("0.00079"))**2)),
}


# ----------------------------------------------------------------------------
# Build algebraic expressions to test:
#   - α_i (singletons)
#   - α_i · α_j (doubles, ordered i<=j)
#   - α_i · α_j · α_k (triples)
#   - α_i / α_j and other ratios
#   - α_i · π^k for small k
#   - α_i · √n for n ∈ {2,3,5,6,7,10}
# ----------------------------------------------------------------------------

def build_expressions(alpha, label_prefix=""):
    """Return list of (expr_label, expr_value) for all algebraic combos.

    alpha is a dict m -> value (1..4).
    """
    out = []
    # singletons
    for m in [1, 2, 3, 4]:
        out.append((f"{label_prefix}a{m}", alpha[m]))

    # doubles (ordered i<=j)
    for i in [1, 2, 3, 4]:
        for j in [i, i+1, i+2, i+3]:
            if j > 4:
                continue
            out.append((f"{label_prefix}a{i}*a{j}", alpha[i] * alpha[j]))

    # triples (sorted)
    seen = set()
    for i in [1, 2, 3, 4]:
        for j in [1, 2, 3, 4]:
            for k in [1, 2, 3, 4]:
                key = tuple(sorted([i, j, k]))
                if key in seen:
                    continue
                seen.add(key)
                out.append((f"{label_prefix}a{key[0]}*a{key[1]}*a{key[2]}",
                            alpha[key[0]] * alpha[key[1]] * alpha[key[2]]))

    # ratios α_i / α_j  (i != j)
    for i in [1, 2, 3, 4]:
        for j in [1, 2, 3, 4]:
            if i == j:
                continue
            out.append((f"{label_prefix}a{i}/a{j}", alpha[i] / alpha[j]))

    # α_i · π^k
    for m in [1, 2, 3, 4]:
        for k in [-3, -2, -1, 1, 2, 3]:
            out.append((f"{label_prefix}a{m}*pi^{k}", alpha[m] * pi**k))

    # α_i · √n
    for m in [1, 2, 3, 4]:
        for n in [2, 3, 5, 6, 7, 10]:
            out.append((f"{label_prefix}a{m}*sqrt({n})", alpha[m] * sqrt(mpf(n))))

    # α_i^2, α_i^(1/2)
    for m in [1, 2, 3, 4]:
        out.append((f"{label_prefix}a{m}^2", alpha[m]**2))
        out.append((f"{label_prefix}sqrt(a{m})", sqrt(alpha[m])))

    # α_i · α_j · π^k for small k
    for i in [1, 2, 3, 4]:
        for j in [i, i+1, i+2, i+3]:
            if j > 4:
                continue
            for k in [-2, -1, 1, 2]:
                out.append((f"{label_prefix}a{i}*a{j}*pi^{k}",
                            alpha[i] * alpha[j] * pi**k))

    return out


def small_q_search(expr_value, target, sigma, max_sum=30, max_each=24):
    """Find rationals q = num/denom (gcd=1, |num|+|denom|<=max_sum,
    each ≤ max_each) such that q * expr_value ≈ target."""
    hits = []
    for denom in range(1, max_each + 1):
        for num in range(1, max_each + 1):
            if num + denom > max_sum:
                continue
            if gcd(num, denom) != 1:
                continue
            q = mpf(num) / mpf(denom)
            pred = q * expr_value
            rel = fabs(pred - target) / fabs(target)
            sigma_dist = fabs(pred - target) / sigma
            if sigma_dist < mpf("0.5"):
                hits.append({
                    "q": f"{num}/{denom}",
                    "q_num": num, "q_denom": denom,
                    "pred": pred,
                    "rel_err": float(rel),
                    "sigma_dist": float(sigma_dist),
                })
    return hits


def main():
    print("=" * 80)
    print("A62 — SYSTEMATIC CKM extension of A17 K=Q(i) Damerell ladder")
    print("=" * 80)
    print(f"mp.dps = {mp.dps}")
    print()

    # 1. Compute periods + L-values for all 5 CM forms
    print("Computing Chowla-Selberg periods + L(f, m)...")
    omega_table = {}
    L_table = {}
    alpha_table = {}  # alpha_table[label][m] = L(f,m) * pi^(4-m) / Omega^4

    for fd in CM_FORMS:
        omega_table[fd["label"]] = chowla_selberg_period(fd["D_K"])
        traces = load_traces(fd["label"])
        L_table[fd["label"]] = {m: L_value(traces, fd["N"], 5, mpf(m))
                                 for m in [1, 2, 3, 4]}
        Omega = omega_table[fd["label"]]
        alpha_table[fd["label"]] = {
            m: L_table[fd["label"]][m] * pi**(4 - m) / Omega**4
            for m in [1, 2, 3, 4]
        }
        # Diagnostic: at K=Q(i) we expect 1/10, 1/12, 1/24, 1/60
        if fd["label"] == "4.5.b.a":
            print("  K=Q(i) ladder check:")
            for m in [1, 2, 3, 4]:
                print(f"    a_{m} = {float(alpha_table[fd['label']][m]):.20f}")

    alpha_Qi = alpha_table["4.5.b.a"]

    # 2. Build all algebraic expressions at K=Q(i)
    print("\nBuilding algebraic expressions over Q(i) ladder...")
    exprs_Qi = build_expressions(alpha_Qi, label_prefix="")
    print(f"  total expressions = {len(exprs_Qi)}")

    # 3. Systematic small-q PSLQ-style search vs each CKM target
    print("\nSmall-q search (|num|+|denom|≤30, each≤24, sigma_dist<0.5)...")
    all_hits = []
    for ckm_name, (val, sig) in PDG.items():
        # Also test square: target = val (interpret expr as |V|^n directly)
        for expr_label, expr_val in exprs_Qi:
            hits = small_q_search(expr_val, val, sig, max_sum=30, max_each=24)
            for h in hits:
                all_hits.append({
                    "CKM_target": ckm_name,
                    "PDG_value": str(val),
                    "PDG_sigma": str(sig),
                    "expr_label": expr_label,
                    "expr_value": str(expr_val),
                    "q": h["q"],
                    "predicted": str(h["pred"]),
                    "rel_err": h["rel_err"],
                    "sigma_dist": h["sigma_dist"],
                })

    print(f"  total hits: {len(all_hits)}")

    # 4. Filter to "clean" ones: sigma_dist < 0.1 AND prefer simple expressions
    print("\nFiltering: sigma_dist < 0.1 (clean fits)...")
    clean = [h for h in all_hits if h["sigma_dist"] < 0.1]
    clean.sort(key=lambda h: (h["sigma_dist"], len(h["expr_label"]), h["q"]))
    print(f"  clean hits: {len(clean)}")
    for h in clean[:30]:
        print(f"    {h['CKM_target']:<22} q={h['q']:<8} expr={h['expr_label']:<30} "
              f"sigma={h['sigma_dist']:.3f}  rel_err={h['rel_err']*100:.3f}%")

    # 5. Cross-K test for each clean hit (apply same expr+q to other K)
    print("\nCross-K test (apply same q + structural recipe to other K)...")
    cross_K_results = []
    seen_recipes = set()
    for h in clean:
        recipe_key = (h["CKM_target"], h["expr_label"], h["q"])
        if recipe_key in seen_recipes:
            continue
        seen_recipes.add(recipe_key)
        target = PDG[h["CKM_target"]][0]
        sig = PDG[h["CKM_target"]][1]
        num, denom = map(int, h["q"].split("/"))
        q = mpf(num) / mpf(denom)
        row = {
            "CKM_target": h["CKM_target"],
            "expr_label": h["expr_label"],
            "q": h["q"],
            "Q(i)_sigma_dist": h["sigma_dist"],
            "by_K": [],
        }
        for fd in CM_FORMS:
            # Re-evaluate the expression at this K using its alpha table
            alpha_K = alpha_table[fd["label"]]
            # Rebuild expressions for this K using same labelling
            local_exprs = dict(build_expressions(alpha_K))
            if h["expr_label"] not in local_exprs:
                continue
            expr_K = local_exprs[h["expr_label"]]
            pred_K = q * expr_K
            rel_K = float(fabs(pred_K - target) / fabs(target))
            sigma_K = float(fabs(pred_K - target) / sig)
            row["by_K"].append({
                "K": fd["Knote"],
                "form": fd["label"],
                "expr_value": str(expr_K),
                "pred": str(pred_K),
                "rel_err": rel_K,
                "sigma_dist": sigma_K,
            })
        cross_K_results.append(row)

    # 6. Identify K=Q(i)-specific hits: sigma_dist at Q(i) < 0.1 AND >5sigma at all others
    print("\nIdentifying K=Q(i)-SPECIFIC hits (Q(i)<0.1σ, all others >5σ)...")
    Qi_specific = []
    for row in cross_K_results:
        Qi = next((b for b in row["by_K"] if b["K"] == "Q(i)"), None)
        if Qi is None:
            continue
        others = [b for b in row["by_K"] if b["K"] != "Q(i)"]
        if Qi["sigma_dist"] < 0.1 and all(o["sigma_dist"] > 5.0 for o in others):
            Qi_specific.append(row)
            print(f"\n  CKM={row['CKM_target']:<22}  expr={row['expr_label']:<30}  q={row['q']}")
            print(f"    Q(i)        : sigma={Qi['sigma_dist']:.3f}  rel={Qi['rel_err']*100:.3f}%")
            for o in others:
                print(f"    {o['K']:<12}: sigma={o['sigma_dist']:.1f}  rel={o['rel_err']*100:.1f}%")

    print(f"\n  K=Q(i)-specific count: {len(Qi_specific)}")

    # 7. Save
    out = {
        "metadata": {
            "agent": "A62",
            "date": "2026-05-05",
            "mp_dps": int(mp.dps),
            "discipline": "Mistral large STRICT BAN; hallu 85 entering",
            "honest_caveat": "Small-q coincidences expected by random; q hits must be cross-K-specific to count as evidence.",
        },
        "PDG_targets": {k: {"value": str(v[0]), "sigma": str(v[1])} for k, v in PDG.items()},
        "alpha_Qi": {str(m): str(alpha_Qi[m]) for m in [1, 2, 3, 4]},
        "Omega_K": {fd["label"]: str(omega_table[fd["label"]]) for fd in CM_FORMS},
        "all_hits_count": len(all_hits),
        "clean_hits_count": len(clean),
        "clean_hits_top30": clean[:30],
        "cross_K_results": cross_K_results,
        "Qi_specific_hits": Qi_specific,
        "Qi_specific_count": len(Qi_specific),
    }
    out_path = "/root/crossed-cosmos/notes/eci_v7_aspiration/A62_CKM_SYSTEMATIC/ckm_hits.json"
    with open(out_path, "w") as fh:
        json.dump(out, fh, indent=2, default=str)
    print(f"\nWritten {out_path}")
    return out


if __name__ == "__main__":
    main()
