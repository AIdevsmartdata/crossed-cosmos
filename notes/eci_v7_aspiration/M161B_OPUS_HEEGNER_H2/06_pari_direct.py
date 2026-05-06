#!/usr/bin/env python3
"""
M161B Sub-task 6: PARI direct execution at 80-digit precision via gp scripts.

The cypari2 binding has a precision propagation issue with lfunmf — but
direct gp execution preserves the realprecision setting throughout.

Approach: build a single gp script for each h=2 field, execute via pari
eval, parse the output.
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
results = vector(#B);
for(j=1, #B,
  F = B[j];
  Lobj = lfunmf(mf, F);
  /* Distinguish: rational form has Lobj as length-6 L-data with sub-comp len 2;
     Hecke form has Lobj as vector of length=deg, each sub-component an L-data length 6 */
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
    """Return float(|x|) carefully."""
    try:
        return abs(float(pari.real(x))) + abs(float(pari.imag(x)))
    except:
        try:
            return abs(float(x))
        except:
            return 1.0

EPS_RESID = 1e-50
EPS_NUM = 1e-15
B9 = 10**9

print("=" * 70)
print("M161B Sub-task 6: PARI direct gp execution at 80-digit precision")
print("=" * 70)

all_results = []

for fld in target_fields:
    D, d_K, N, c = fld["D"], fld["d_K"], fld["N"], fld["conrey"]
    print()
    print("=" * 60)
    print(f"D={D}  K={fld['K']}  N={N}  Conrey c={c}")
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

        # Check has_im
        Im_R = pari.imag(Rf)
        Re_R = pari.real(Rf)
        im_size = small(Im_R)
        has_im = im_size > EPS_NUM

        print()
        print(f"  --- j={j} {marker} a_2={a2}, a_3={a3}, a_5={a5} ---")
        if has_im:
            print(f"      L(f,1)={L1}")
            print(f"      L(f,2)={L2}")
            print(f"      R(f)={Rf}  (complex, |Im|={im_size:.3e})")
        else:
            print(f"      L(f,1)={L1}")
            print(f"      L(f,2)={L2}")
            print(f"      R(f)={Rf}  (real)")

        # Test Q
        Rfq = pari.bestappr(Rf, B9)
        rq = small(Rf - Rfq)
        # Test Q*sqrt(d_K) — for real Rf
        if not has_im:
            Rfr = pari.bestappr(Rf / sqDk, B9)
            rr = small(Rf - Rfr * sqDk)
        else:
            Rfr = None
            rr = None

        print(f"      Q residual = {rq:.3e}")
        if rr is not None:
            print(f"      Q*sqrt({d_K}) residual = {rr:.3e}")
            print(f"      bestappr Q*sqrt = ({Rfr})*sqrt({d_K})")

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
            # Test biquadratic: Re, Im each in Q + Q*sqrt(d_K)
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
                    print(f"      lindep Re: {ld_re}, residual = {res_re:.3e}")
                    print(f"      lindep Im: {ld_im}, residual = {res_im:.3e}")
                    if res_re < EPS_RESID and res_im < EPS_RESID:
                        verdict = "Q(i,sqrt(d_K))"
                        Re_q_part = -pari(a_r) / pari(c_r)
                        Re_s_part = -pari(b_r) / pari(c_r)
                        Im_q_part = -pari(a_i) / pari(c_i)
                        Im_s_part = -pari(b_i) / pari(c_i)
                        value = f"Re=({Re_q_part})+({Re_s_part})*sqrt({d_K}); Im=({Im_q_part})+({Im_s_part})*sqrt({d_K})"
            except Exception as e:
                pass
            # Also try Q(i): Re, Im both rational
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

        print(f"      VERDICT: {verdict}, value = {value}")

        all_results.append({
            "D": D,
            "d_K": d_K,
            "j": j,
            "a2": str(a2),
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
        })

print()
print("=" * 70)
print("FINAL VERDICT TABLE")
print("=" * 70)
print()
hdr = f"{'D':>5}  {'j':>2}  {'a2':>5}  {'rational?':>10}  {'verdict':>20}  value"
print(hdr)
print("-" * 100)
for r in all_results:
    a2_str = str(r["a2"])[:5]
    rat = "Q-rat" if r["is_rational"] else "Hecke"
    val_str = str(r.get("value"))[:50] if r.get("value") else "None"
    print(f"{r['D']:>5}  {r['j']:>2}  {a2_str:>5}  {rat:>10}  {r['verdict']:>20}  {val_str}")

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
print(f"  Rational coefficient (Q-rat): {n_rat}")
print(f"  R(f) ∈ Q:                    {n_Q}")
print(f"  R(f) ∈ Q*sqrt(d_K):          {n_Qsqrt}")
print(f"  R(f) ∈ Q(i):                 {n_Qi}")
print(f"  R(f) ∈ Q(i, sqrt(d_K)):      {n_biquad}")
print(f"  Other:                       {n_other}")

# h=2 rational newforms only
rat_results = [r for r in all_results if r["is_rational"]]
print()
print(f"Among {len(rat_results)} rational newforms (h=2 CM-principal-genus):")
print(f"  R(f) ∈ Q:               {sum(1 for r in rat_results if r['verdict']=='Q')} <-- M114.B uniqueness violation count")
print(f"  R(f) ∈ Q*sqrt(d_K):     {sum(1 for r in rat_results if r['verdict']=='Q*sqrt(d_K)')} <-- M97 pattern count")

import json
with open("06_results.json", "w") as f:
    json.dump(all_results, f, indent=2, default=str)
print()
print(f"Results saved to 06_results.json")
