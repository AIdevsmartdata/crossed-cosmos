"""A62 — null/sanity test.

How many small-q hits would we get if α_m were random rationals instead of
the K=Q(i) ladder values?

Plus: cross-K test for the BEST candidates we identified.
"""
import json
import random
from fractions import Fraction
from math import gcd
from mpmath import mp, mpf, sqrt, pi, fabs

mp.dps = 60

# Same PDG table
PDG = {
    "|V_us|":           (mpf("0.22501"),    mpf("0.00068")),
    "|V_cb|":           (mpf("0.04183"),    mpf("0.00079")),
    "|V_ub|":           (mpf("0.003820"),   mpf("0.00020")),
    "|V_td|":           (mpf("0.00858"),    mpf("0.00026")),
    "|V_tb|":           (mpf("1.0140"),     mpf("0.0290")),
    "|V_cb|^2":         (mpf("0.04183")**2, 2 * mpf("0.04183") * mpf("0.00079")),
    "|V_ub|^2":         (mpf("0.003820")**2, 2 * mpf("0.003820") * mpf("0.00020")),
    "|V_td|^2":         (mpf("0.00858")**2, 2 * mpf("0.00858") * mpf("0.00026")),
    "|V_tb|^2":         (mpf("1.0140")**2,  2 * mpf("1.0140") * mpf("0.0290")),
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


def small_q_hits_for_value(expr_value, max_sum=30, max_each=24, sigma_thresh=0.1):
    """Count number of (target, q) pairs that give sigma_dist < thresh."""
    n_hits = 0
    for ckm_name, (val, sig) in PDG.items():
        for denom in range(1, max_each + 1):
            for num in range(1, max_each + 1):
                if num + denom > max_sum or gcd(num, denom) != 1:
                    continue
                q = mpf(num) / mpf(denom)
                pred = q * expr_value
                if fabs(pred - val) / sig < sigma_thresh:
                    n_hits += 1
    return n_hits


# Build expressions over a "ladder"
def build_expressions(a):
    out = []
    for m in [1, 2, 3, 4]:
        out.append((f"a{m}", a[m]))
    for i in [1, 2, 3, 4]:
        for j in [i, i+1, i+2, i+3]:
            if j > 4: continue
            out.append((f"a{i}*a{j}", a[i] * a[j]))
    seen = set()
    for i in [1, 2, 3, 4]:
        for j in [1, 2, 3, 4]:
            for k in [1, 2, 3, 4]:
                key = tuple(sorted([i,j,k]))
                if key in seen: continue
                seen.add(key)
                out.append((f"a{key[0]}*a{key[1]}*a{key[2]}", a[key[0]]*a[key[1]]*a[key[2]]))
    for i in [1, 2, 3, 4]:
        for j in [1, 2, 3, 4]:
            if i == j: continue
            out.append((f"a{i}/a{j}", a[i]/a[j]))
    for m in [1, 2, 3, 4]:
        for k in [-3, -2, -1, 1, 2, 3]:
            out.append((f"a{m}*pi^{k}", a[m] * pi**k))
    for m in [1, 2, 3, 4]:
        for n in [2, 3, 5, 6, 7, 10]:
            out.append((f"a{m}*sqrt({n})", a[m] * sqrt(mpf(n))))
    for m in [1, 2, 3, 4]:
        out.append((f"a{m}^2", a[m]**2))
    for i in [1, 2, 3, 4]:
        for j in [i, i+1, i+2, i+3]:
            if j > 4: continue
            for k in [-2, -1, 1, 2]:
                out.append((f"a{i}*a{j}*pi^{k}", a[i]*a[j]*pi**k))
    return out


# Q(i) ladder
a_Qi = {1: mpf(1)/10, 2: mpf(1)/12, 3: mpf(1)/24, 4: mpf(1)/60}

# Random rational replacements with same magnitude (denominators between 5 and 100)
random.seed(42)
n_trials = 8
print("=" * 80)
print("NULL TEST: how many sigma<0.1 hits do random small-rational ladders give?")
print("=" * 80)

# Q(i) baseline
exprs_Qi = build_expressions(a_Qi)
hits_Qi = sum(small_q_hits_for_value(v, sigma_thresh=0.1) for _, v in exprs_Qi)
print(f"\nQ(i) ladder (1/10, 1/12, 1/24, 1/60):  {hits_Qi} sigma<0.1 hits across {len(exprs_Qi)} expressions")

# Random ladders with same order of magnitude
for trial in range(n_trials):
    a_rand = {}
    for m in [1, 2, 3, 4]:
        # random rational with magnitude similar to alpha_m
        target_mag = float(a_Qi[m])
        while True:
            denom = random.randint(5, 100)
            num = random.randint(1, denom)
            v = num/denom
            if 0.5 * target_mag < v < 2 * target_mag:
                break
        a_rand[m] = mpf(num)/mpf(denom)
    exprs_r = build_expressions(a_rand)
    n_h = sum(small_q_hits_for_value(v, sigma_thresh=0.1) for _, v in exprs_r)
    print(f"Trial {trial}: ladder=({Fraction(int(round(float(a_rand[1])*100)),100)}-ish, "
          f"...) -> {n_h} sigma<0.1 hits")

print("\n--- Conclusion ---")
print("If random ladders give ~similar N hits, then Q(i) hits are NOT uniquely")
print("structural — they're just artifacts of small-q dense rational approximation.")
print("If Q(i) gives substantially MORE hits, that would suggest structural alignment.")
