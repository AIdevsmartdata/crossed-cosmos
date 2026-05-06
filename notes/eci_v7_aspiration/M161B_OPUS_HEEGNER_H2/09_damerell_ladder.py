#!/usr/bin/env python3
"""
M161B Sub-task 9: Bootstrap Damerell ladder for h=2 rational newforms.

Compute alpha_m = L(f, m) * Pi^(4-m) / L(f, 4)  for m = 1, 2, 3.

M97 baseline:
- alpha_odd (alpha_1, alpha_3) ∈ Q*sqrt(d_K) \\ Q  (parity-odd)
- alpha_2 ∈ Q  (parity-even)

For h=2, test the same parity split.
"""

import cypari2
pari = cypari2.Pari(sizemax=8*1024*1024*1024)

target_fields = [
    {"D": -15, "d_K": 15, "K": "Q(sqrt(-15))", "N": 15, "conrey": 14},
    {"D": -20, "d_K": 5,  "K": "Q(sqrt(-5))",  "N": 20, "conrey": 19},
    {"D": -24, "d_K": 6,  "K": "Q(sqrt(-6))",  "N": 24, "conrey": 5},
    {"D": -35, "d_K": 35, "K": "Q(sqrt(-35))", "N": 35, "conrey": 34},
    {"D": -40, "d_K": 10, "K": "Q(sqrt(-10))", "N": 40, "conrey": 19},
    {"D": -88, "d_K": 22, "K": "Q(sqrt(-22))", "N": 88, "conrey": 21},
]

GP_SCRIPT = """
default(realprecision, 80);
chi = znchar(Mod({c}, {N}));
mf = mfinit([{N}, 5, chi], 1);
B = mfeigenbasis(mf);
ratresults = vector(2);
idx = 0;
for(j=1, #B,
  F = B[j];
  if(type(mfcoef(F, 2)) != "t_INT", next);
  Lobj = lfunmf(mf, F);
  is_rational = (type(Lobj) == "t_VEC" && #Lobj == 6 && type(Lobj[1]) == "t_VEC" && #Lobj[1] == 2);
  if(!is_rational, next);
  L1 = lfun(Lobj, 1);
  L2 = lfun(Lobj, 2);
  L3 = lfun(Lobj, 3);
  L4 = lfun(Lobj, 4);
  a1 = L1*Pi^3/L4;
  a2 = L2*Pi^2/L4;
  a3 = L3*Pi/L4;
  Rf = Pi*L1/L2;
  idx = idx + 1;
  ratresults[idx] = [j, mfcoef(F,2), L1, L2, L3, L4, Rf, a1, a2, a3];
);
ratresults
"""

EPS = 1e-50
EPS_NUM = 1e-15
B9 = 10**9

def small(x):
    try:
        return abs(float(pari.real(x))) + abs(float(pari.imag(x)))
    except:
        try:
            return abs(float(x))
        except:
            return 1.0

def classify_alpha(alpha, d_K, name):
    """Classify alpha_m as Q, Q*sqrt(d_K), or other."""
    sqDk = pari(f"sqrt({d_K})")
    aq = pari.bestappr(alpha, B9)
    rq = small(alpha - aq)
    asq = pari.bestappr(alpha / sqDk, B9)
    rs = small(alpha - asq * sqDk)
    if rq < EPS:
        return ("Q", str(aq), rq, rs)
    elif rs < EPS:
        return ("Q*sqrt(d_K)", f"({asq})*sqrt({d_K})", rq, rs)
    else:
        return ("OTHER", None, rq, rs)

print("=" * 70)
print("M161B Sub-task 9: BOOTSTRAP DAMERELL LADDER for h=2 rational newforms")
print("=" * 70)
print()

all_data = []

for fld in target_fields:
    D, d_K, N, c = fld["D"], fld["d_K"], fld["N"], fld["conrey"]
    print()
    print("=" * 60)
    print(f"D={D}  K={fld['K']}  N={N}  d_K={d_K}")
    print("=" * 60)

    script = GP_SCRIPT.format(c=c, N=N)
    try:
        results = pari(script)
    except Exception as e:
        print(f"  GP error: {e}")
        continue

    nrat = int(pari.length(results))
    print(f"  Number of rational newforms: {nrat}")

    for idx in range(1, nrat + 1):
        row = results[idx-1]
        if row == 0:
            continue  # uninitialized slot
        j, a2, L1, L2, L3, L4, Rf, a1b, a2b, a3b = (row[k] for k in range(10))
        print()
        print(f"  --- j={j}, a_2(f)={a2} ---")
        print(f"      L(f,1)={float(L1):.10g}  L(f,2)={float(L2):.10g}  L(f,3)={float(L3):.10g}  L(f,4)={float(L4):.10g}")

        cls_a1 = classify_alpha(a1b, d_K, "a1")
        cls_a2 = classify_alpha(a2b, d_K, "a2")
        cls_a3 = classify_alpha(a3b, d_K, "a3")
        cls_R = classify_alpha(Rf, d_K, "R")

        print(f"      alpha_1 = L1*Pi^3/L4 = {float(a1b):.10g}")
        print(f"        VERDICT: {cls_a1[0]}, value = {cls_a1[1]}, residuals Q={cls_a1[2]:.3e}, Qsqrt={cls_a1[3]:.3e}")
        print(f"      alpha_2 = L2*Pi^2/L4 = {float(a2b):.10g}")
        print(f"        VERDICT: {cls_a2[0]}, value = {cls_a2[1]}, residuals Q={cls_a2[2]:.3e}, Qsqrt={cls_a2[3]:.3e}")
        print(f"      alpha_3 = L3*Pi/L4   = {float(a3b):.10g}")
        print(f"        VERDICT: {cls_a3[0]}, value = {cls_a3[1]}, residuals Q={cls_a3[2]:.3e}, Qsqrt={cls_a3[3]:.3e}")
        print(f"      R(f)   = Pi*L1/L2   = {float(Rf):.10g}")
        print(f"        VERDICT: {cls_R[0]}, value = {cls_R[1]}")

        # Compute q ratios
        sqd = pari(f"sqrt({d_K})")
        a1_per_sq = pari.bestappr(a1b / sqd, B9)
        a3_per_sq = pari.bestappr(a3b / sqd, B9)
        a2_q = pari.bestappr(a2b, B9)

        print(f"      DAMERELL: a1/sqd = {a1_per_sq}, a2 = {a2_q}, a3/sqd = {a3_per_sq}")
        print(f"      q_d = R/sqd = {pari.bestappr(Rf/sqd, B9)}")

        # New M97 structural test: a1/sqd ?= 3*d_K/4 ?
        # This was for h=1 Type IV primes only. For h=2 not expected directly.
        a1_dk_ratio = pari.bestappr(a1b / sqd / d_K, B9)
        print(f"      a1/(sqd*d_K) = {a1_dk_ratio} [M97 Type IV: 3/4]")

        all_data.append({
            "D": D, "d_K": d_K, "j": int(j),
            "a2": str(a2),
            "a1_boot_q": str(a1_per_sq),
            "a2_boot_q": str(a2_q),
            "a3_boot_q": str(a3_per_sq),
            "R_q_d": str(pari.bestappr(Rf/sqd, B9)),
            "a1_per_sqd_dk": str(a1_dk_ratio),
            "alpha_1_class": cls_a1[0],
            "alpha_2_class": cls_a2[0],
            "alpha_3_class": cls_a3[0],
        })

print()
print("=" * 70)
print("PARITY-SPLIT TABLE: alpha_1, alpha_2, alpha_3 for h=2 rational newforms")
print("=" * 70)
print()
hdr = f"{'D':>5} {'j':>2} {'a1 cls':>15} {'a2 cls':>10} {'a3 cls':>15} {'q_d':>20}"
print(hdr)
print("-" * 100)
for r in all_data:
    print(f"{r['D']:>5} {r['j']:>2} {r['alpha_1_class']:>15} {r['alpha_2_class']:>10} {r['alpha_3_class']:>15} {r['R_q_d']:>20}")

# Verify parity-split holds
print()
print("M97 PARITY-SPLIT CHECK: alpha_1, alpha_3 in Q*sqrt(d_K), alpha_2 in Q?")
correct = sum(1 for r in all_data if r['alpha_1_class'] == 'Q*sqrt(d_K)' and r['alpha_2_class'] == 'Q' and r['alpha_3_class'] == 'Q*sqrt(d_K)')
print(f"  Confirmed: {correct}/{len(all_data)}")

import json
with open("09_damerell_ladder.json", "w") as f:
    json.dump(all_data, f, indent=2, default=str)
print(f"  Saved to 09_damerell_ladder.json")
