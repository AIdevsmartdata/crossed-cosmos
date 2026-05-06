#!/usr/bin/env python3
"""
M162 Sub-task 8: h=5 only fields — write to separate JSON to avoid clash with 06.

h=5 fields: D ∈ {-47, -79, -103, -127}.
These should be small N so fast.
"""

import json
import time
import cypari2
pari = cypari2.Pari(sizemax=8 * 1024 * 1024 * 1024)

h5_targets = [
    {"D": -47, "d_K": 47, "K": "Q(sqrt(-47))", "N": 47, "h": 5},
    {"D": -79, "d_K": 79, "K": "Q(sqrt(-79))", "N": 79, "h": 5},
    {"D": -103, "d_K": 103, "K": "Q(sqrt(-103))", "N": 103, "h": 5},
    {"D": -127, "d_K": 127, "K": "Q(sqrt(-127))", "N": 127, "h": 5},
]

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


def find_kronecker_conrey(D, N):
    G = pari.znstar(N, 1)
    candidates = []
    for c_try in [N - 1] + list(range(1, N)):
        if c_try < 1:
            continue
        if pari.gcd(c_try, N) != 1:
            continue
        if c_try in candidates:
            continue
        chi_data = pari.znchar(pari(f"Mod({c_try}, {N})"))
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
            if c_try == N - 1:
                return N - 1
            candidates.append(c_try)
    return candidates[-1] if candidates else None


print("=" * 70)
print("M162 Sub-task 8: h=5 only fields")
print("=" * 70)

all_h5_results = []

for fld in h5_targets:
    D, N, d_K, h = fld["D"], fld["N"], fld["d_K"], fld["h"]
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

        Im_R = pari.imag(Rf)
        Re_R = pari.real(Rf)
        has_im = small(Im_R) > EPS_NUM

        cls = "OTHER"
        val = None
        rq = rr = None

        if not has_im:
            Rfq = pari.bestappr(Rf, B9)
            rq = small(Rf - Rfq)
            Rfr = pari.bestappr(Rf / sqDk, B9)
            rr = small(Rf - Rfr * sqDk)
            if rq < EPS_RESID:
                cls = "Q"
                val = str(Rfq)
            elif rr < EPS_RESID:
                cls = "Q*sqrt(d_K)"
                val = f"({Rfr})*sqrt({d_K})"
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
                        cls = "Q(i)"
                        val = f"({Re_pred})+({Im_pred})*I"
            except Exception:
                pass

        a1_per_sqd_dk_str = a1_per_sqd_str = a2_alpha_str = a3_per_sqd_str = None
        try:
            if not has_im:
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

        print(f"  j={j} {'[Q-rat]' if is_rat else '[Hecke]'} a2={str(a2)[:80]}")
        print(f"      cls={cls} val={str(val)[:60] if val else 'None'}")
        if a1_per_sqd_dk_str:
            print(f"      alpha_1/(sqd*dK)={a1_per_sqd_dk_str}")

        all_h5_results.append({
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

with open("/root/crossed-cosmos/notes/eci_v7_aspiration/M162_OPUS_HEEGNER_H3_H4/08_h5_results.json", "w") as f:
    json.dump(all_h5_results, f, indent=2, default=str)
print()
print(f"DONE: {len(all_h5_results)} entries saved.")
print(f"  Rational forms: {sum(1 for r in all_h5_results if r['is_rational'])}")
