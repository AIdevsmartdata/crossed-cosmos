#!/usr/bin/env python3
"""
M161B Sub-task 5: ROBUST classification v2 — uses float() for comparisons
to avoid PARI precision-aware comparison pitfalls.

R(f) at 80-digit precision; residuals at 1e-50 threshold for "exact" status.
"""

import cypari2
import json
pari = cypari2.Pari()
pari.set_real_precision(80)
pari.allocatemem(2 * 1024 * 1024 * 1024)

target_fields = [
    {"D": -15, "d_K": 15, "K": "Q(sqrt(-15))", "N": 15, "conrey": 14},
    {"D": -20, "d_K": 5,  "K": "Q(sqrt(-5))",  "N": 20, "conrey": 19},
    {"D": -24, "d_K": 6,  "K": "Q(sqrt(-6))",  "N": 24, "conrey": 5},
    {"D": -35, "d_K": 35, "K": "Q(sqrt(-35))", "N": 35, "conrey": 34},
    {"D": -40, "d_K": 10, "K": "Q(sqrt(-10))", "N": 40, "conrey": 19},
    {"D": -88, "d_K": 22, "K": "Q(sqrt(-22))", "N": 88, "conrey": 21},
]

EPS_RESID = 1e-50  # exactness threshold (residual MUST be < this)
EPS_NUM = 1e-15    # numerical noise floor (residual ABOVE this = NOT zero)
B9 = 10**9

def small(x):
    """Return float(|x|), handling PARI's precision-aware zero."""
    try:
        # PARI may print "0.E-18" which is exactly zero in float
        f = float(pari.abs(x))
        return f
    except Exception:
        return 1.0  # treat as not small

def classify_R(Rf, d_K):
    """Classify R(f) into Q, Q*sqrt(d_K), Q(i, sqrt(d_K)) or other."""
    sqDk = pari(f"sqrt({d_K})")
    Re_R = pari.real(Rf)
    Im_R = pari.imag(Rf)
    has_im = small(Im_R) > EPS_NUM

    result = {
        "Re_str": str(Re_R)[:60],
        "Im_str": str(Im_R)[:60],
        "has_im": has_im,
    }

    # Test 1: R ∈ Q
    Rfq = pari.bestappr(Rf, B9)
    rq = small(Rf - Rfq)
    result["Q_appr"] = str(Rfq)
    result["Q_residual"] = rq

    # Test 2: R ∈ Q*sqrt(d_K) — only sensible if real
    if not has_im:
        Rfr = pari.bestappr(Rf / sqDk, B9)
        rr = small(Rf - Rfr * sqDk)
        result["sqrt_appr"] = str(Rfr)
        result["sqrt_residual"] = rr
    else:
        result["sqrt_appr"] = None
        result["sqrt_residual"] = None

    # Verdict
    # Note: bestappr always returns SOMETHING; the residual tells us if it's "real"
    if rq < EPS_RESID:
        # Numerically Q-rational at 80-digit
        result["verdict"] = "Q"
        result["value"] = str(Rfq)
        return result
    if not has_im and result["sqrt_residual"] is not None and result["sqrt_residual"] < EPS_RESID:
        result["verdict"] = "Q*sqrt(d_K)"
        result["value"] = f"({result['sqrt_appr']})*sqrt({d_K})"
        return result

    # Test 3: Biquadratic Q(i, sqrt(d_K))
    if has_im:
        # R = a + b*sqrt(d) + c*i + d*i*sqrt(d) where a, b, c, d ∈ Q
        # Equiv: Re(R) = a + b*sqrt(d), Im(R) = c + d*sqrt(d)
        Re_q = pari.bestappr(Re_R, B9)
        Re_r_per_sq = pari.bestappr(Re_R / sqDk, B9)
        Im_q = pari.bestappr(Im_R, B9)
        Im_r_per_sq = pari.bestappr(Im_R / sqDk, B9)

        # Use lindep [1, sqrt(d), Re(R)] and [1, sqrt(d), Im(R)]
        ld_re = pari.lindep([pari(1), sqDk, Re_R])
        ld_im = pari.lindep([pari(1), sqDk, Im_R])
        result["lindep_Re"] = str(ld_re)
        result["lindep_Im"] = str(ld_im)

        # Try to extract coefficients
        try:
            a_re, b_re, c_re = int(ld_re[0]), int(ld_re[1]), int(ld_re[2])
            a_im, b_im, c_im = int(ld_im[0]), int(ld_im[1]), int(ld_im[2])
            # Check magnitudes
            COEFF_BOUND = 10**11
            if (c_re != 0 and c_im != 0 and
                abs(a_re) < COEFF_BOUND and abs(b_re) < COEFF_BOUND and abs(c_re) < COEFF_BOUND and
                abs(a_im) < COEFF_BOUND and abs(b_im) < COEFF_BOUND and abs(c_im) < COEFF_BOUND):
                Re_pred = -(pari(a_re) + pari(b_re) * sqDk) / pari(c_re)
                Im_pred = -(pari(a_im) + pari(b_im) * sqDk) / pari(c_im)
                res_re = small(Re_R - Re_pred)
                res_im = small(Im_R - Im_pred)
                result["Re_residual"] = res_re
                result["Im_residual"] = res_im
                if res_re < EPS_RESID and res_im < EPS_RESID:
                    result["verdict"] = "Q(i,sqrt(d_K))"
                    result["value"] = f"Re=({-pari(a_re)/pari(c_re)})+({-pari(b_re)/pari(c_re)})*sqrt({d_K}); Im=({-pari(a_im)/pari(c_im)})+({-pari(b_im)/pari(c_im)})*sqrt({d_K})"
                    return result
        except Exception as e:
            result["lindep_error"] = str(e)

    # Higher-order test: Try R ∈ Q(sqrt(d_K), i) more loosely
    # ...for now if not classified, mark unclassified
    result["verdict"] = "OTHER"
    result["value"] = None
    return result

print("=" * 70)
print("M161B Sub-task 5: ROBUST CLASSIFICATION (float-based comparison)")
print("=" * 70)

all_results = []

for fld in target_fields:
    D = fld["D"]
    d_K = fld["d_K"]
    N = fld["N"]
    c = fld["conrey"]
    print()
    print("=" * 60)
    print(f"D={D}  K={fld['K']}  N={N}  Conrey c={c}")
    print("=" * 60)

    chi = pari.znchar(pari(f"Mod({c}, {N})"))
    mf = pari.mfinit([N, 5, chi], 1)
    B = pari.mfeigenbasis(mf)
    nforms = int(pari.length(B))
    print(f"  Total newforms: {nforms}")

    for j in range(1, nforms + 1):
        F = B[j-1]
        a2 = pari.mfcoef(F, 2)
        a3 = pari.mfcoef(F, 3)
        a5 = pari.mfcoef(F, 5)
        a7 = pari.mfcoef(F, 7)
        a2_t = str(pari.type(a2))
        try:
            Lobj = pari.lfunmf(mf, F)
            try:
                L1 = pari.lfun(Lobj, 1)
            except:
                Lobj = Lobj[0]
                L1 = pari.lfun(Lobj, 1)
            L1 = pari.lfun(Lobj, 1)
            L2 = pari.lfun(Lobj, 2)
            L3 = pari.lfun(Lobj, 3)
            L4 = pari.lfun(Lobj, 4)
        except Exception as e:
            print(f"  j={j}: L computation error: {e}")
            continue

        Rf = pari.Pi() * L1 / L2
        result = classify_R(Rf, d_K)
        result["D"] = D
        result["d_K"] = d_K
        result["j"] = j
        result["a2"] = str(a2)
        result["a2_type"] = a2_t
        result["L1"] = str(L1)
        result["L2"] = str(L2)
        result["L3"] = str(L3)
        result["L4"] = str(L4)
        result["Rf"] = str(Rf)

        is_rational = (a2_t == "t_INT")
        marker = "[RATIONAL]" if is_rational else "[Hecke field]"
        print(f"  --- j={j} {marker} a_2={a2}, a_3={a3}, a_5={a5}, a_7={a7} ---")
        print(f"      L(f,1)={float(L1):.10g}  L(f,2)={float(L2):.10g}  L(f,3)={float(L3):.10g}  L(f,4)={float(L4):.10g}")
        if has_im := result["has_im"]:
            print(f"      R(f) = {float(pari.real(Rf)):.10g} + {float(pari.imag(Rf)):.10g}*I  (complex)")
        else:
            print(f"      R(f) = {float(Rf):.15g}  (real)")
        print(f"      Q residual: {result['Q_residual']:.3e}")
        if result.get("sqrt_residual") is not None:
            print(f"      Q*sqrt({d_K}) residual: {result['sqrt_residual']:.3e}")
        print(f"      VERDICT: {result['verdict']}, value = {result['value']}")
        all_results.append(result)

print()
print("=" * 70)
print("SUMMARY TABLE: VERDICTS for ALL h=2 newforms")
print("=" * 70)
print()
hdr = f"{'D':>5}  {'j':>2}  {'a2':>5}  {'type':>11}  {'verdict':>20}  value"
print(hdr)
print("-" * 100)
for r in all_results:
    a2_str = str(r["a2"])[:5]
    a2_type = r["a2_type"][2:] if r["a2_type"].startswith("t_") else r["a2_type"]
    val_str = str(r.get("value"))[:50]
    print(f"{r['D']:>5}  {r['j']:>2}  {a2_str:>5}  {a2_type:>11}  {r['verdict']:>20}  {val_str}")

print()
print("=" * 70)
print("STATISTICS")
print("=" * 70)
n_total = len(all_results)
n_Q = sum(1 for r in all_results if r["verdict"] == "Q")
n_Qsqrt = sum(1 for r in all_results if r["verdict"] == "Q*sqrt(d_K)")
n_biquad = sum(1 for r in all_results if r["verdict"] == "Q(i,sqrt(d_K))")
n_other = sum(1 for r in all_results if r["verdict"] == "OTHER")

print(f"  TOTAL newforms tested: {n_total}")
print(f"  R(f) ∈ Q:                {n_Q}")
print(f"  R(f) ∈ Q*sqrt(d_K):      {n_Qsqrt}")
print(f"  R(f) ∈ Q(i, sqrt(d_K)):  {n_biquad}")
print(f"  Other:                   {n_other}")

rationals = [r for r in all_results if r["a2_type"] == "t_INT"]
n_rat = len(rationals)
n_rat_Q = sum(1 for r in rationals if r["verdict"] == "Q")
n_rat_Qsqrt = sum(1 for r in rationals if r["verdict"] == "Q*sqrt(d_K)")

print()
print(f"Rational coefficient newforms (CM by class group principal char):")
print(f"  Total: {n_rat}")
print(f"  R(f) ∈ Q:               {n_rat_Q} <-- M114.B violations (should be 0!)")
print(f"  R(f) ∈ Q*sqrt(d_K):     {n_rat_Qsqrt} <-- M97 pattern preserved")

with open("05_results.json", "w") as f:
    json.dump(all_results, f, indent=2, default=str)
print()
print(f"Full results saved to 05_results.json")
