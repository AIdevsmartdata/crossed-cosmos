#!/usr/bin/env python3
"""
M162 Sub-task 6: Process remaining fields not yet in 04_results.json.

Skip-ahead: process h=5 fields and remaining h=4 fields. Use simpler classifier
to avoid lindep timeouts on huge Hecke polynomials.
"""

import json
import os
import time
import cypari2
pari = cypari2.Pari(sizemax=8 * 1024 * 1024 * 1024)

with open("/root/crossed-cosmos/notes/eci_v7_aspiration/M162_OPUS_HEEGNER_H3_H4/01_targets.json") as f:
    target_fields = json.load(f)

OUT_PATH = "/root/crossed-cosmos/notes/eci_v7_aspiration/M162_OPUS_HEEGNER_H3_H4/04_results.json"

# Load existing
existing = []
done_D = set()
if os.path.exists(OUT_PATH):
    with open(OUT_PATH) as f:
        existing = json.load(f)
    done_D = set(r["D"] for r in existing)
    print(f"Already processed: {sorted(done_D, key=abs)}")

remaining = [f for f in target_fields if abs(f["D"]) <= 200 and f["D"] not in done_D]
# Reverse priority: do h=5 first (small), then larger h=4
remaining.sort(key=lambda f: (f["h"], abs(f["D"])))
print(f"Remaining: {[(f['D'], f['h']) for f in remaining]}")

GP_LFUN_SCRIPT = """
default(realprecision, 80);
chi = znchar(Mod({c}, {N}));
mf = mfinit([{N}, 5, chi], 1);
B = mfeigenbasis(mf);
results = vector(#B);
for(j=1, #B,
  F = B[j];
  Lobj = lfunmf(mf, F);
  Lobj_use = if(type(Lobj) == "t_VEC" && #Lobj == 6 && type(Lobj[1]) == "t_VEC" && #Lobj[1] == 2, Lobj, Lobj[1]);
  L1 = lfun(Lobj_use, 1);
  L2 = lfun(Lobj_use, 2);
  L3 = lfun(Lobj_use, 3);
  L4 = lfun(Lobj_use, 4);
  Rf = Pi * L1 / L2;
  results[j] = [mfcoef(F, 2), mfcoef(F, 3), mfcoef(F, 5), L1, L2, L3, L4, Rf];
);
results
"""


def find_kronecker_conrey(D, N):
    G = pari.znstar(N, 1)
    if pari.gcd(N-1, N) == 1:
        c_try = N - 1
        chi_data = pari.znchar(pari(f"Mod({c_try}, {N})"))
        chi = chi_data[1]
        order = int(pari.charorder(G, chi))
        if order == 2:
            ok = True
            tests = 0
            for p in [3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67]:
                if pari.gcd(p, N) != 1:
                    continue
                val = pari.chareval(G, chi, p)
                chi_p = 1 if val == 0 else -1 if val == pari("1/2") else None
                kron = int(pari.kronecker(D, p))
                if chi_p != kron:
                    ok = False
                    break
                tests += 1
                if tests >= 8:
                    break
            if ok and tests >= 6:
                return N - 1
    candidates = []
    for c in range(1, N):
        if pari.gcd(c, N) != 1:
            continue
        chi_data = pari.znchar(pari(f"Mod({c}, {N})"))
        chi = chi_data[1]
        order = int(pari.charorder(G, chi))
        if order != 2:
            continue
        ok = True
        tests = 0
        for p in [3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67]:
            if pari.gcd(p, N) != 1:
                continue
            val = pari.chareval(G, chi, p)
            chi_p = 1 if val == 0 else -1 if val == pari("1/2") else None
            kron = int(pari.kronecker(D, p))
            if chi_p != kron:
                ok = False
                break
            tests += 1
            if tests >= 8:
                break
        if ok and tests >= 6:
            candidates.append(c)
    return candidates[-1] if candidates else None


def small(x):
    try:
        return abs(float(pari.real(x))) + abs(float(pari.imag(x)))
    except Exception:
        try:
            return abs(float(x))
        except Exception:
            return 1.0


EPS_RESID = 1e-50
EPS_NUM = 1e-15
B9 = 10**9


def classify_minimal(Rf, sqDk, d_K):
    """Lighter classifier; only test Q, Q*sqrt, and Q(i)."""
    Im_R = pari.imag(Rf)
    Re_R = pari.real(Rf)
    has_im = small(Im_R) > EPS_NUM
    if not has_im:
        Rfq = pari.bestappr(Rf, B9)
        rq = small(Rf - Rfq)
        Rfr = pari.bestappr(Rf / sqDk, B9)
        rr = small(Rf - Rfr * sqDk)
        if rq < EPS_RESID:
            return ("Q", str(Rfq), rq, rr)
        if rr < EPS_RESID:
            return ("Q*sqrt(d_K)", f"({Rfr})*sqrt({d_K})", rq, rr)
        return ("OTHER", None, rq, rr)
    else:
        try:
            ld_re_q = pari.lindep([pari(1), Re_R])
            ld_im_q = pari.lindep([pari(1), Im_R])
            a_r, b_r = int(ld_re_q[0]), int(ld_re_q[1])
            a_i, b_i = int(ld_im_q[0]), int(ld_im_q[1])
            if b_r != 0 and b_i != 0 and abs(a_r) < 10**11 and abs(b_r) < 10**11:
                Re_pred = -pari(a_r) / pari(b_r)
                Im_pred = -pari(a_i) / pari(b_i)
                if small(Re_R - Re_pred) < EPS_RESID and small(Im_R - Im_pred) < EPS_RESID:
                    return ("Q(i)", f"({Re_pred})+({Im_pred})*I", small(Rf - pari.bestappr(Rf, B9)), None)
        except Exception:
            pass
        return ("OTHER", None, small(Rf - pari.bestappr(Rf, B9)), None)


for fld in remaining:
    D = fld["D"]
    if D in set(r["D"] for r in existing):
        continue
    N = fld["N"]
    d_K = fld["d_K"]
    h = fld["h"]
    print()
    print(f"=== D={D:>4}  N={N}  d_K={d_K}  h={h} ===")
    t0 = time.time()
    conrey = find_kronecker_conrey(D, N)
    if conrey is None:
        print(f"  *** NO CONREY MATCH ***")
        continue
    print(f"  Conrey c = {conrey}")

    script = GP_LFUN_SCRIPT.format(c=conrey, N=N)
    try:
        results = pari(script)
    except Exception as e:
        print(f"  GP error: {e}")
        continue

    nforms = int(pari.length(results))
    elapsed = time.time() - t0
    print(f"  newforms = {nforms}  ({elapsed:.1f}s)")

    sqDk = pari(f"sqrt({d_K})")
    pi_val = pari("Pi")

    for j in range(1, nforms + 1):
        row = results[j-1]
        a2, a3, a5, L1, L2, L3, L4, Rf = (row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7])
        a2_t = str(pari.type(a2))
        is_rat = (a2_t == "t_INT")

        cls, val, rq, rr = classify_minimal(Rf, sqDk, d_K)

        a1_per_sqd_dk_str = a1_per_sqd_str = a2_alpha_str = a3_per_sqd_str = None
        try:
            Im_R = pari.imag(Rf)
            if small(Im_R) <= EPS_NUM:
                a1_alpha = L1 * pi_val ** 3 / L4
                a2_alpha_v = L2 * pi_val ** 2 / L4
                a3_alpha = L3 * pi_val / L4
                a1_per_sqd = pari.bestappr(a1_alpha / sqDk, B9)
                a1_per_sqd_str = str(a1_per_sqd)
                a2_alpha_str = str(pari.bestappr(a2_alpha_v, B9))
                a3_per_sqd = pari.bestappr(a3_alpha / sqDk, B9)
                a3_per_sqd_str = str(a3_per_sqd)
                a1_per_sqd_dk = pari.bestappr(a1_alpha / sqDk / d_K, B9)
                a1_per_sqd_dk_str = str(a1_per_sqd_dk)
        except Exception:
            pass

        print(f"  j={j} {'[Q-rat]' if is_rat else '[Hecke]'} a2={str(a2)[:60]}  cls={cls}  val={str(val)[:60] if val else 'None'}")
        if is_rat and a1_per_sqd_dk_str:
            print(f"      alpha_1/(sqd*dK)={a1_per_sqd_dk_str}")

        existing.append({
            "D": D, "d_K": d_K, "h": h, "N": N, "j": j,
            "conrey": conrey,
            "a2": str(a2), "a3": str(a3), "a5": str(a5),
            "a2_type": a2_t, "is_rational": is_rat,
            "L1": str(L1), "L2": str(L2), "L3": str(L3), "L4": str(L4),
            "Rf": str(Rf),
            "verdict": cls, "value": val,
            "Q_residual": rq, "sqrt_residual": rr,
            "alpha_1_per_sqd": a1_per_sqd_str,
            "alpha_2": a2_alpha_str,
            "alpha_3_per_sqd": a3_per_sqd_str,
            "alpha_1_per_sqd_dk": a1_per_sqd_dk_str,
        })

    with open(OUT_PATH, "w") as f:
        json.dump(existing, f, indent=2, default=str)
    print(f"  Saved (total: {len(existing)} entries)")

print()
print("DONE")
