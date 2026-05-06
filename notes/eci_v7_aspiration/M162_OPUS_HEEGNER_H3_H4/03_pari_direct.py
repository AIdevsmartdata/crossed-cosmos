#!/usr/bin/env python3
"""
M162 Sub-task 3: PARI direct gp execution at 80-digit precision (M161B workaround).

For each h=3, h=4, h=5 imaginary quadratic field K, level N=|D|, weight 5,
character chi_D (Conrey index from 02_newforms.json), compute:
  - L(f, m) for m=1,2,3,4 at 80-digit precision
  - R(f) = pi*L(f,1)/L(f,2)
  - Damerell ladder alpha_m = L(f, m) * pi^(4-m)/L(f,4)
  - Verdict: Q vs Q*sqrt(d_K) vs Q(i) vs Q(i, sqrt(d_K))
  - alpha_1/(sqrt(d_K)*d_K) for M161B.2 c-test
"""

import json
import cypari2
pari = cypari2.Pari(sizemax=8 * 1024 * 1024 * 1024)

with open("/root/crossed-cosmos/notes/eci_v7_aspiration/M162_OPUS_HEEGNER_H3_H4/02_newforms.json") as f:
    target_fields = json.load(f)

# Filter: keep only fields with valid Conrey
target_fields = [f for f in target_fields if f.get("conrey") is not None]

GP_SCRIPT = """
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

print("=" * 70)
print("M162 Sub-task 3: PARI direct gp 80-digit L-values for h=3, 4, 5")
print("=" * 70)

all_results = []
for fld in target_fields:
    D, d_K, N, c = fld["D"], fld["d_K"], fld["N"], fld["conrey"]
    h = fld["h"]
    print()
    print("=" * 60)
    print(f"D={D}  K={fld['K']}  N={N}  Conrey c={c}  h={h}  d_K={d_K}")
    print("=" * 60)

    script = GP_SCRIPT.format(c=c, N=N)
    try:
        results = pari(script)
    except Exception as e:
        print(f"  GP script error: {e}")
        continue
    nforms = int(pari.length(results))
    print(f"  Total newforms: {nforms}")

    sqDk = pari(f"sqrt({d_K})")

    for j in range(1, nforms + 1):
        row = results[j-1]
        a2, a3, a5, L1, L2, L3, L4, Rf = (row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7])
        a2_t = str(pari.type(a2))
        is_rat = (a2_t == "t_INT")
        marker = "[Q-rat]" if is_rat else "[Hecke field]"

        Im_R = pari.imag(Rf)
        Re_R = pari.real(Rf)
        im_size = small(Im_R)
        has_im = im_size > EPS_NUM

        print()
        print(f"  --- j={j} {marker} a_2={a2}, a_3={a3}, a_5={a5} ---")
        if has_im:
            print(f"      R(f)={Rf} (complex, |Im|={im_size:.3e})")
        else:
            print(f"      R(f)={Rf} (real)")

        # Test Q
        Rfq = pari.bestappr(Rf, B9)
        rq = small(Rf - Rfq)
        # Test Q*sqrt(d_K)
        if not has_im:
            Rfr = pari.bestappr(Rf / sqDk, B9)
            rr = small(Rf - Rfr * sqDk)
        else:
            Rfr = None
            rr = None

        # Verdict
        verdict = "OTHER"
        value = None
        if rq < EPS_RESID:
            verdict = "Q"
            value = str(Rfq)
        elif not has_im and rr is not None and rr < EPS_RESID:
            verdict = "Q*sqrt(d_K)"
            value = f"({Rfr})*sqrt({d_K})"
        elif has_im:
            # biquadratic test
            ld_re = pari.lindep([pari(1), sqDk, Re_R])
            ld_im = pari.lindep([pari(1), sqDk, Im_R])
            try:
                a_r, b_r, c_r = int(ld_re[0]), int(ld_re[1]), int(ld_re[2])
                a_i, b_i, c_i = int(ld_im[0]), int(ld_im[1]), int(ld_im[2])
                COEFF_BOUND = 10**11
                if (c_r != 0 and c_i != 0 and
                    abs(a_r) < COEFF_BOUND and abs(b_r) < COEFF_BOUND and abs(c_r) < COEFF_BOUND and
                    abs(a_i) < COEFF_BOUND and abs(b_i) < COEFF_BOUND and abs(c_i) < COEFF_BOUND):
                    Re_pred = -(pari(a_r) + pari(b_r) * sqDk) / pari(c_r)
                    Im_pred = -(pari(a_i) + pari(b_i) * sqDk) / pari(c_i)
                    res_re = small(Re_R - Re_pred)
                    res_im = small(Im_R - Im_pred)
                    if res_re < EPS_RESID and res_im < EPS_RESID:
                        verdict = "Q(i,sqrt(d_K))"
                        Re_q_part = -pari(a_r) / pari(c_r)
                        Re_s_part = -pari(b_r) / pari(c_r)
                        Im_q_part = -pari(a_i) / pari(c_i)
                        Im_s_part = -pari(b_i) / pari(c_i)
                        value = f"Re=({Re_q_part})+({Re_s_part})*sqrt({d_K}); Im=({Im_q_part})+({Im_s_part})*sqrt({d_K})"
            except Exception:
                pass
            # Q(i)
            ld_re_q = pari.lindep([pari(1), Re_R])
            ld_im_q = pari.lindep([pari(1), Im_R])
            try:
                a_r, b_r = int(ld_re_q[0]), int(ld_re_q[1])
                a_i, b_i = int(ld_im_q[0]), int(ld_im_q[1])
                if b_r != 0 and b_i != 0 and abs(a_r) < 10**11 and abs(b_r) < 10**11:
                    Re_pred = -pari(a_r) / pari(b_r)
                    Im_pred = -pari(a_i) / pari(b_i)
                    res_re = small(Re_R - Re_pred)
                    res_im = small(Im_R - Im_pred)
                    if res_re < EPS_RESID and res_im < EPS_RESID and verdict == "OTHER":
                        verdict = "Q(i)"
                        value = f"({-pari(a_r)/pari(b_r)})+({-pari(a_i)/pari(b_i)})*I"
            except Exception:
                pass

        # alpha_m bootstrap (only if rational)
        a1_q_str = a2_q_str = a3_q_str = None
        a1_per_sqd_dk_str = None
        if not has_im:
            try:
                # alpha_m = L(f,m) * pi^(4-m) / L(f,4)
                pi_val = pari("Pi")
                a1 = L1 * pi_val ** 3 / L4
                a2_alpha = L2 * pi_val ** 2 / L4
                a3_alpha = L3 * pi_val / L4
                a1_per_sqd = pari.bestappr(a1 / sqDk, B9)
                a1_q_str = str(a1_per_sqd)
                a2_q = pari.bestappr(a2_alpha, B9)
                a2_q_str = str(a2_q)
                a3_per_sqd = pari.bestappr(a3_alpha / sqDk, B9)
                a3_q_str = str(a3_per_sqd)
                a1_per_sqd_dk = pari.bestappr(a1 / sqDk / d_K, B9)
                a1_per_sqd_dk_str = str(a1_per_sqd_dk)
            except Exception as e:
                print(f"      Damerell ladder error: {e}")

        print(f"      VERDICT: {verdict}, value = {value}")
        print(f"      Q residual = {rq:.3e}")
        if rr is not None:
            print(f"      Q*sqrt({d_K}) residual = {rr:.3e}")
        if a1_q_str is not None:
            print(f"      alpha_1/sqrt(d_K) = {a1_q_str}")
            print(f"      alpha_2 = {a2_q_str}")
            print(f"      alpha_3/sqrt(d_K) = {a3_q_str}")
            print(f"      alpha_1/(sqrt(d_K)*d_K) = {a1_per_sqd_dk_str}  [M161B.2: 3/4 if D mod 4 = 1, 6 if D mod 4 = 0]")

        all_results.append({
            "D": D,
            "d_K": d_K,
            "h": h,
            "j": j,
            "a2": str(a2),
            "a3": str(a3),
            "a5": str(a5),
            "a2_type": a2_t,
            "is_rational": is_rat,
            "L1": str(L1),
            "L2": str(L2),
            "L3": str(L3),
            "L4": str(L4),
            "Rf": str(Rf),
            "verdict": verdict,
            "value": value,
            "Q_residual": rq,
            "sqrt_residual": rr,
            "alpha_1_per_sqd": a1_q_str,
            "alpha_2": a2_q_str,
            "alpha_3_per_sqd": a3_q_str,
            "alpha_1_per_sqd_dk": a1_per_sqd_dk_str,
        })

print()
print("=" * 70)
print("RATIONAL-NEWFORM VERDICT TABLE")
print("=" * 70)
print(f"{'D':>5} {'h':>2} {'j':>2} {'a2':>5} {'verdict':>20} {'a1/(sqd*dK)':>14}  R(f) value")
print("-" * 110)
for r in all_results:
    if not r["is_rational"]:
        continue
    val_str = str(r.get("value"))[:50] if r.get("value") else "None"
    a1pred = r.get("alpha_1_per_sqd_dk", "?")
    print(f"{r['D']:>5} {r['h']:>2} {r['j']:>2} {r['a2']:>5} {r['verdict']:>20} {str(a1pred):>14}  {val_str}")

print()
print("=" * 70)
print("STATISTICS")
print("=" * 70)
n_total = len(all_results)
n_rat = sum(1 for r in all_results if r["is_rational"])
n_Q = sum(1 for r in all_results if r["verdict"] == "Q")
n_Qsqrt = sum(1 for r in all_results if r["verdict"] == "Q*sqrt(d_K)")
n_biquad = sum(1 for r in all_results if r["verdict"] == "Q(i,sqrt(d_K))")
n_Qi = sum(1 for r in all_results if r["verdict"] == "Q(i)")
n_other = sum(1 for r in all_results if r["verdict"] == "OTHER")
print(f"Total newforms tested: {n_total}")
print(f"  Rational a_p (Q-rat): {n_rat}")
print(f"  R(f) ∈ Q:                    {n_Q}")
print(f"  R(f) ∈ Q*sqrt(d_K):          {n_Qsqrt}")
print(f"  R(f) ∈ Q(i):                 {n_Qi}")
print(f"  R(f) ∈ Q(i, sqrt(d_K)):      {n_biquad}")
print(f"  Other:                       {n_other}")
print()
rat_results = [r for r in all_results if r["is_rational"]]
print(f"Among {len(rat_results)} rational newforms (h>=3 CM):")
print(f"  R(f) ∈ Q: {sum(1 for r in rat_results if r['verdict']=='Q')} <-- M114.B uniqueness violation count")
print(f"  R(f) ∈ Q*sqrt(d_K): {sum(1 for r in rat_results if r['verdict']=='Q*sqrt(d_K)')} <-- M97 pattern count")

import json as _json
with open("/root/crossed-cosmos/notes/eci_v7_aspiration/M162_OPUS_HEEGNER_H3_H4/03_results.json", "w") as f:
    _json.dump(all_results, f, indent=2, default=str)
print()
print("Results saved to 03_results.json")
