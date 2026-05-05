"""A62 — restrict to TRULY parsimonious hits (q=1 or q=k for tiny integer k).

If a CKM target equals exactly α_m or a product α_i*α_j or similar with q=1,
that's structurally unambiguous. Otherwise, q=k (k small integer) is also clean.
"""
import json
from mpmath import mp, mpf, sqrt, pi, fabs

mp.dps = 60

# K=Q(i) Damerell ladder
a = {1: mpf(1)/10, 2: mpf(1)/12, 3: mpf(1)/24, 4: mpf(1)/60}

PDG = {
    "|V_us|":           (mpf("0.22501"),    mpf("0.00068")),
    "|V_cb|":           (mpf("0.04183"),    mpf("0.00079")),
    "|V_ub|":           (mpf("0.003820"),   mpf("0.00020")),
    "|V_td|":           (mpf("0.00858"),    mpf("0.00026")),
    "|V_tb|":           (mpf("1.0140"),     mpf("0.0290")),
    "|V_cb|^2":         (mpf("0.04183")**2, 2 * mpf("0.04183") * mpf("0.00079")),
    "|V_ub|^2":         (mpf("0.003820")**2, 2 * mpf("0.003820") * mpf("0.00020")),
    "|V_td|^2":         (mpf("0.00858")**2, 2 * mpf("0.00858") * mpf("0.00026")),
    "|V_ub/V_cb|":      (mpf("0.003820")/mpf("0.04183"),
                          (mpf("0.003820")/mpf("0.04183"))
                          * sqrt((mpf("0.00020")/mpf("0.003820"))**2
                                 + (mpf("0.00079")/mpf("0.04183"))**2)),
    "|V_td/V_cb|":      (mpf("0.00858")/mpf("0.04183"),
                          (mpf("0.00858")/mpf("0.04183"))
                          * sqrt((mpf("0.00026")/mpf("0.00858"))**2
                                 + (mpf("0.00079")/mpf("0.04183"))**2)),
    "|V_td/V_ts|":      (mpf("0.2050"),     mpf("0.0070")),
    "|V_us|*|V_cb|":    (mpf("0.22501")*mpf("0.04183"),
                          mpf("0.22501")*mpf("0.04183")
                          * sqrt((mpf("0.00068")/mpf("0.22501"))**2
                                 + (mpf("0.00079")/mpf("0.04183"))**2)),
    "|V_us|^2+|V_cb|^2": (mpf("0.22501")**2 + mpf("0.04183")**2,
                          sqrt((2*mpf("0.22501")*mpf("0.00068"))**2
                               + (2*mpf("0.04183")*mpf("0.00079"))**2)),
    "J_CKM":            (mpf("3.18e-5"),    mpf("0.15e-5")),
}

# Build all parsimonious expressions: monomials in {a1,a2,a3,a4, pi, sqrt(n)}
# with degree ≤ 3 in α and at most one π^k (k in -2..2) and no sqrt for purity.
def build_parsimonious():
    out = []
    # bare alpha
    for m in [1, 2, 3, 4]:
        out.append((f"a{m}", a[m]))
    # alpha pairs
    for i in [1, 2, 3, 4]:
        for j in [i, i+1, i+2, i+3]:
            if j > 4: continue
            out.append((f"a{i}*a{j}", a[i]*a[j]))
    # alpha triples
    seen = set()
    for i in [1,2,3,4]:
        for j in [1,2,3,4]:
            for k in [1,2,3,4]:
                key = tuple(sorted([i,j,k]))
                if key in seen: continue
                seen.add(key)
                out.append((f"a{key[0]}*a{key[1]}*a{key[2]}", a[key[0]]*a[key[1]]*a[key[2]]))
    # alpha ratios
    for i in [1,2,3,4]:
        for j in [1,2,3,4]:
            if i == j: continue
            out.append((f"a{i}/a{j}", a[i]/a[j]))
    # multiply each by pi^k for k in {-2,-1,1,2}
    base = list(out)
    for label, val in base:
        for k in [-2, -1, 1, 2]:
            out.append((f"({label})*pi^{k}", val * pi**k))
    return out


exprs = build_parsimonious()

# Restrict q to TINY: q=1, q=k for k in 2..6, or q=1/k for k in 2..6
TINY_QS = [(1,1), (2,1), (3,1), (4,1), (5,1), (6,1),
           (1,2), (1,3), (1,4), (1,5), (1,6),
           (3,2), (5,2), (5,3), (5,4), (5,6), (3,4), (2,3),
           (4,3), (4,5), (3,5), (6,5), (7,4), (7,5), (8,3),
           (9,4), (9,8)]  # last few include A17's 9/4

print("=" * 100)
print("A62 — TINY-q-only Q(i) hits  (q in {1, 1/k, k, simple fractions})")
print("=" * 100)
print(f"{'CKM target':<22} {'q':<8} {'expr':<35} {'pred':<18} {'rel %':>8} {'sigma':>8}")
print("-" * 100)

clean_tiny = []
for ckm_name, (val, sig) in PDG.items():
    for num, denom in TINY_QS:
        from math import gcd
        if gcd(num, denom) != 1:
            continue
        q = mpf(num)/mpf(denom)
        for label, expr_val in exprs:
            pred = q * expr_val
            sigma = float(fabs(pred - val) / sig)
            if sigma < 0.1:
                rel = float(fabs(pred-val)/fabs(val))*100
                clean_tiny.append({
                    "CKM": ckm_name,
                    "q": f"{num}/{denom}",
                    "expr": label,
                    "pred": str(pred),
                    "rel_err": rel,
                    "sigma": sigma,
                })

clean_tiny.sort(key=lambda h: (h["sigma"], h["q"], h["expr"]))
for h in clean_tiny[:60]:
    print(f"{h['CKM']:<22} {h['q']:<8} {h['expr']:<35} {float(h['pred']):<18.10g} "
          f"{h['rel_err']:>8.4f} {h['sigma']:>8.4f}")

# Save
with open('/root/crossed-cosmos/notes/eci_v7_aspiration/A62_CKM_SYSTEMATIC/ckm_tiny_q.json', 'w') as fh:
    json.dump(clean_tiny, fh, indent=2, default=str)
print(f"\nTotal tiny-q sigma<0.1 hits: {len(clean_tiny)}")
print("Written ckm_tiny_q.json")
