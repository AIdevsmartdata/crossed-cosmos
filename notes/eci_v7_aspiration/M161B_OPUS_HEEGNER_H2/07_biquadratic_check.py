#!/usr/bin/env python3
"""
M161B Sub-task 7: Biquadratic Q(i, sqrt(d_K)) check for the Hecke-field
newforms (j=3, j=4, j=5).

These complex L-values come from non-genus class group characters chi_g
applied to the principal Hecke character. The structure should be:
- Real(R) ∈ Q + Q*sqrt(d_K)
- Imag(R) ∈ Q + Q*sqrt(d_K)
- Equivalent to R(f) ∈ K' = Q(i, sqrt(d_K)) biquadratic.

Use lindep at high precision to test linear relations among
[1, sqrt(d_K), Re(R)] and [1, sqrt(d_K), Im(R)].
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

# Run gp script that handles ALL Galois conjugates for non-rational newforms
GP_SCRIPT_ALL = """
default(realprecision, 80);
chi = znchar(Mod({c}, {N}));
mf = mfinit([{N}, 5, chi], 1);
B = mfeigenbasis(mf);
results = vector(#B);
for(j=1, #B,
  F = B[j];
  Lobj = lfunmf(mf, F);
  /* Distinguish rational (Lobj is single L-data) vs Hecke (Lobj is vector of L-data) */
  is_rational = (type(Lobj) == "t_VEC" && #Lobj == 6 && type(Lobj[1]) == "t_VEC" && #Lobj[1] == 2);
  if(is_rational,
    \\\\ rational form: single L-function
    L1 = lfun(Lobj, 1);
    L2 = lfun(Lobj, 2);
    L3 = lfun(Lobj, 3);
    L4 = lfun(Lobj, 4);
    Rf = Pi * L1 / L2;
    results[j] = [1, [mfcoef(F,2), mfcoef(F,3), mfcoef(F,5), L1, L2, L3, L4, Rf]],
    \\\\ Hecke field form: vector of L-functions, one per Galois conjugate
    nconj = #Lobj;
    conjugate_data = vector(nconj);
    for(k=1, nconj,
      Lk = Lobj[k];
      L1 = lfun(Lk, 1);
      L2 = lfun(Lk, 2);
      L3 = lfun(Lk, 3);
      L4 = lfun(Lk, 4);
      Rf = Pi * L1 / L2;
      conjugate_data[k] = [L1, L2, L3, L4, Rf];
    );
    results[j] = [nconj, [mfcoef(F,2), mfcoef(F,3), mfcoef(F,5)], conjugate_data]
  );
);
results
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

def test_R_classification(Rf, d_K):
    """Comprehensive R classification including biquadratic and per-conjugate."""
    sqDk = pari(f"sqrt({d_K})")
    Re_R = pari.real(Rf)
    Im_R = pari.imag(Rf)
    has_im = small(Im_R) > EPS_NUM

    info = {"Re": Re_R, "Im": Im_R, "has_im": has_im}

    # Q test
    Rfq = pari.bestappr(Rf, B9)
    rq = small(Rf - Rfq)
    info["Q"] = (Rfq, rq)

    # Q*sqrt(d_K) test (for real)
    if not has_im:
        Rfr = pari.bestappr(Rf / sqDk, B9)
        rr = small(Rf - Rfr * sqDk)
        info["Qsqrt"] = (Rfr, rr)

    # Q(i) test (for complex)
    if has_im:
        Re_q = pari.bestappr(Re_R, B9)
        Im_q = pari.bestappr(Im_R, B9)
        res_re = small(Re_R - Re_q)
        res_im = small(Im_R - Im_q)
        info["Qi"] = (Re_q, Im_q, res_re, res_im)

    # Q(i)*sqrt(d_K) test (Re, Im both rational multiple of sqrt)
    if has_im:
        Re_r = pari.bestappr(Re_R / sqDk, B9)
        Im_r = pari.bestappr(Im_R / sqDk, B9)
        res_re = small(Re_R - Re_r * sqDk)
        res_im = small(Im_R - Im_r * sqDk)
        info["Qisqrt"] = (Re_r, Im_r, res_re, res_im)

    # Biquadratic Q(i, sqrt(d_K)): Re, Im each in Q + Q*sqrt(d_K)
    if has_im:
        ld_re = pari.lindep([pari(1), sqDk, Re_R])
        ld_im = pari.lindep([pari(1), sqDk, Im_R])
        try:
            ar, br, cr = int(ld_re[0]), int(ld_re[1]), int(ld_re[2])
            ai, bi, ci = int(ld_im[0]), int(ld_im[1]), int(ld_im[2])
            COEFF_BOUND = 10**12
            if (cr != 0 and ci != 0 and
                abs(ar) < COEFF_BOUND and abs(br) < COEFF_BOUND and abs(cr) < COEFF_BOUND and
                abs(ai) < COEFF_BOUND and abs(bi) < COEFF_BOUND and abs(ci) < COEFF_BOUND):
                Re_pred = -(pari(ar) + pari(br) * sqDk) / pari(cr)
                Im_pred = -(pari(ai) + pari(bi) * sqDk) / pari(ci)
                res_re = small(Re_R - Re_pred)
                res_im = small(Im_R - Im_pred)
                info["biquad"] = ((ar, br, cr), (ai, bi, ci), Re_pred, Im_pred, res_re, res_im)
        except Exception as e:
            info["biquad_err"] = str(e)

    # Q*sqrt(d_K) for complex: separately Re and Im in Q*sqrt(d_K)?
    # i.e., R = a*sqrt(d) + b*i*sqrt(d) with a,b ∈ Q
    if has_im:
        Re_q_per_sq = pari.bestappr(Re_R / sqDk, B9)
        Im_q_per_sq = pari.bestappr(Im_R / sqDk, B9)
        res_re_p = small(Re_R - Re_q_per_sq * sqDk)
        res_im_p = small(Im_R - Im_q_per_sq * sqDk)
        info["Q*sqrt_complex"] = (Re_q_per_sq, Im_q_per_sq, res_re_p, res_im_p)

    return info

def classify(info, has_im):
    """Pick the cleanest verdict."""
    if "Q" in info and info["Q"][1] < EPS:
        return ("Q", str(info["Q"][0]))
    if "Qsqrt" in info and info["Qsqrt"][1] < EPS:
        return ("Q*sqrt(d_K)", f"({info['Qsqrt'][0]})*sqrt(d_K)")
    if has_im:
        if "Qi" in info and info["Qi"][2] < EPS and info["Qi"][3] < EPS:
            return ("Q(i)", f"({info['Qi'][0]}) + ({info['Qi'][1]})*I")
        if "Qisqrt" in info and info["Qisqrt"][2] < EPS and info["Qisqrt"][3] < EPS:
            return ("Q(i)*sqrt(d_K)", f"({info['Qisqrt'][0]} + {info['Qisqrt'][1]}*I)*sqrt(d_K)")
        if "biquad" in info:
            (ar, br, cr), (ai, bi, ci), Re_p, Im_p, rr_e, rr_i = info["biquad"]
            if rr_e < EPS and rr_i < EPS:
                Re_q = pari(-ar) / pari(cr)
                Re_s = pari(-br) / pari(cr)
                Im_q = pari(-ai) / pari(ci)
                Im_s = pari(-bi) / pari(ci)
                return ("Q(i,sqrt(d_K)) biquad", f"Re=({Re_q})+({Re_s})sqd; Im=({Im_q})+({Im_s})sqd")
        if "Q*sqrt_complex" in info:
            r, i, rr_e, rr_i = info["Q*sqrt_complex"]
            if rr_e < EPS and rr_i < EPS:
                return ("Q(i)*sqrt(d_K)", f"({r}+{i}*I)*sqrt(d_K)")
    return ("OTHER", None)

print("=" * 70)
print("M161B Sub-task 7: COMPREHENSIVE classification incl. biquadratic + conjugates")
print("=" * 70)

all_results = []

for fld in target_fields:
    D, d_K, N, c = fld["D"], fld["d_K"], fld["N"], fld["conrey"]
    print()
    print("=" * 60)
    print(f"D={D}  K={fld['K']}  N={N}  Conrey c={c}")
    print("=" * 60)

    script = GP_SCRIPT_ALL.format(c=c, N=N)
    try:
        results = pari(script)
    except Exception as e:
        print(f"  GP error: {e}")
        continue
    nforms = int(pari.length(results))
    print(f"  Total newforms: {nforms}")

    sqDk = pari(f"sqrt({d_K})")

    for j in range(1, nforms + 1):
        row = results[j-1]
        # Format: [is_rational_count, ...]
        # If rational: row = [1, [a2, a3, a5, L1, L2, L3, L4, Rf]]
        # If Hecke: row = [nconj, [a2, a3, a5], conjugate_data]
        kind = int(row[0])

        if kind == 1:
            # Rational form
            data = row[1]
            a2, a3, a5, L1, L2, L3, L4, Rf = (data[k] for k in range(8))
            print()
            print(f"  --- j={j} [Q-rat] a_2={a2}, a_3={a3}, a_5={a5} ---")
            print(f"      L(f,1) = {L1}")
            print(f"      L(f,2) = {L2}")
            print(f"      R(f)   = {Rf}")
            info = test_R_classification(Rf, d_K)
            verdict, value = classify(info, info["has_im"])
            if "Q" in info:
                print(f"      Q residual = {info['Q'][1]:.3e}")
            if "Qsqrt" in info:
                print(f"      Q*sqrt({d_K}) residual = {info['Qsqrt'][1]:.3e}, value = ({info['Qsqrt'][0]})*sqrt({d_K})")
            print(f"      VERDICT: {verdict}, value = {value}")
            all_results.append({
                "D": D, "d_K": d_K, "j": j, "k": None,
                "a2": str(a2), "a2_type": "t_INT",
                "is_rational": True,
                "L1": str(L1), "L2": str(L2), "L3": str(L3), "L4": str(L4),
                "Rf": str(Rf),
                "verdict": verdict, "value": str(value) if value else None,
            })
        else:
            # Hecke form: kind = number of conjugates
            nconj = kind
            mfdata = row[1]
            a2, a3, a5 = mfdata[0], mfdata[1], mfdata[2]
            conjugate_data = row[2]
            print()
            print(f"  --- j={j} [Hecke field, {nconj} conjugates] a_2={a2} ---")
            for k in range(1, nconj + 1):
                cd = conjugate_data[k-1]
                L1, L2, L3, L4, Rf = (cd[m] for m in range(5))
                print(f"    conjugate k={k}:")
                print(f"      L(f,1) = {L1}")
                print(f"      L(f,2) = {L2}")
                print(f"      R(f)   = {Rf}")
                info = test_R_classification(Rf, d_K)
                verdict, value = classify(info, info["has_im"])
                if "Q" in info:
                    print(f"      Q residual = {info['Q'][1]:.3e}")
                if "Qsqrt" in info:
                    print(f"      Q*sqrt({d_K}) residual = {info['Qsqrt'][1]:.3e}")
                if "biquad" in info:
                    (ar, br, cr), (ai, bi, ci), Re_p, Im_p, rr_e, rr_i = info["biquad"]
                    print(f"      biquad lindep Re=({ar},{br},{cr}), Im=({ai},{bi},{ci}); res Re={rr_e:.3e}, Im={rr_i:.3e}")
                if "Qi" in info:
                    print(f"      Q(i) residual: Re={info['Qi'][2]:.3e}, Im={info['Qi'][3]:.3e}")
                if "Q*sqrt_complex" in info:
                    print(f"      Q(i)*sqrt residual: Re={info['Q*sqrt_complex'][2]:.3e}, Im={info['Q*sqrt_complex'][3]:.3e}")
                print(f"      VERDICT: {verdict}, value = {value}")
                all_results.append({
                    "D": D, "d_K": d_K, "j": j, "k": k,
                    "a2": str(a2), "a2_type": "t_POLMOD",
                    "is_rational": False,
                    "L1": str(L1), "L2": str(L2), "L3": str(L3), "L4": str(L4),
                    "Rf": str(Rf),
                    "verdict": verdict, "value": str(value) if value else None,
                })

print()
print("=" * 70)
print("COMPREHENSIVE FINAL TABLE")
print("=" * 70)
print(f"\n{'D':>5} {'j':>2} {'k':>3} {'rat':>5} {'verdict':>30} value")
print("-" * 110)
for r in all_results:
    rat = "Q" if r["is_rational"] else "K_f"
    k_str = "-" if r["k"] is None else str(r["k"])
    val = (r["value"] or "")[:50]
    print(f"{r['D']:>5} {r['j']:>2} {k_str:>3} {rat:>5} {r['verdict']:>30} {val}")

print()
print("=" * 70)
print("SUMMARY")
print("=" * 70)
n_total = len(all_results)
print(f"Total newform/conjugate samples: {n_total}")
verdicts = {}
for r in all_results:
    verdicts[r["verdict"]] = verdicts.get(r["verdict"], 0) + 1
for v, n in sorted(verdicts.items(), key=lambda x: -x[1]):
    print(f"  {v}: {n}")
print()

# Restrict to rationals
rats = [r for r in all_results if r["is_rational"]]
print(f"Rational newforms only ({len(rats)}):")
for v in set(r["verdict"] for r in rats):
    n = sum(1 for r in rats if r["verdict"] == v)
    print(f"  {v}: {n}")

print()
import json
with open("07_results.json", "w") as f:
    json.dump(all_results, f, indent=2, default=str)
print("Results saved to 07_results.json")
