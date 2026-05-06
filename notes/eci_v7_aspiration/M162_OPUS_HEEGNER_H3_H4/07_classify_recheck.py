#!/usr/bin/env python3
"""
M162 Sub-task 7: Re-classify all OTHER verdicts at full 80-digit precision.

For Hecke forms with R(f) ∈ "OTHER", test:
  - Q(i, sqrt(d_K)) biquadratic
  - Q(sqrt(d_K)) (real)
  - Higher-degree extensions of Q

For RATIONAL forms already classified, sanity-check the verdict.
"""

import json
import cypari2
pari = cypari2.Pari(sizemax=8 * 1024 * 1024 * 1024)
pari.set_real_precision(80)

with open("/root/crossed-cosmos/notes/eci_v7_aspiration/M162_OPUS_HEEGNER_H3_H4/04_results.json") as f:
    results = json.load(f)


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


def classify_full(Rf_str, d_K, sqDk):
    Rf = pari(Rf_str)
    Im_R = pari.imag(Rf)
    Re_R = pari.real(Rf)
    has_im = small(Im_R) > EPS_NUM

    if not has_im:
        Rfq = pari.bestappr(Rf, B9)
        rq = small(Rf - Rfq)
        if rq < EPS_RESID:
            return ("Q", str(Rfq))
        Rfr = pari.bestappr(Rf / sqDk, B9)
        rr = small(Rf - Rfr * sqDk)
        if rr < EPS_RESID:
            return ("Q*sqrt(d_K)", f"({Rfr})*sqrt({d_K})")
        return ("OTHER", None)

    # complex
    # Test Q(i)
    try:
        ld_re_q = pari.lindep([pari(1), Re_R])
        ld_im_q = pari.lindep([pari(1), Im_R])
        a_r, b_r = int(ld_re_q[0]), int(ld_re_q[1])
        a_i, b_i = int(ld_im_q[0]), int(ld_im_q[1])
        if b_r != 0 and b_i != 0 and abs(a_r) < 10**11 and abs(b_r) < 10**11:
            Re_pred = -pari(a_r) / pari(b_r)
            Im_pred = -pari(a_i) / pari(b_i)
            if small(Re_R - Re_pred) < EPS_RESID and small(Im_R - Im_pred) < EPS_RESID:
                return ("Q(i)", f"({Re_pred})+({Im_pred})*I")
    except Exception:
        pass

    # Test Q(i, sqrt(d_K)) biquadratic — Re, Im each in Q + Q*sqrt(d_K)
    try:
        ld_re = pari.lindep([pari(1), sqDk, Re_R])
        ld_im = pari.lindep([pari(1), sqDk, Im_R])
        a_r, b_r, c_r = int(ld_re[0]), int(ld_re[1]), int(ld_re[2])
        a_i, b_i, c_i = int(ld_im[0]), int(ld_im[1]), int(ld_im[2])
        if (c_r != 0 and c_i != 0 and abs(a_r) < 10**11 and abs(b_r) < 10**11 and abs(c_r) < 10**11
            and abs(a_i) < 10**11 and abs(b_i) < 10**11 and abs(c_i) < 10**11):
            Re_pred = -(pari(a_r) + pari(b_r) * sqDk) / pari(c_r)
            Im_pred = -(pari(a_i) + pari(b_i) * sqDk) / pari(c_i)
            if small(Re_R - Re_pred) < EPS_RESID and small(Im_R - Im_pred) < EPS_RESID:
                Re_q = -pari(a_r) / pari(c_r)
                Re_s = -pari(b_r) / pari(c_r)
                Im_q = -pari(a_i) / pari(c_i)
                Im_s = -pari(b_i) / pari(c_i)
                return ("Q(i,sqrt(d_K))", f"Re=({Re_q})+({Re_s})*sqrt({d_K}); Im=({Im_q})+({Im_s})*sqrt({d_K})")
    except Exception:
        pass

    return ("OTHER", None)


print("=" * 70)
print("M162 Sub-task 7: Full classification recheck")
print("=" * 70)

upgraded_count = 0
for r in results:
    Rf_str = r["Rf"]
    d_K = r["d_K"]
    sqDk = pari(f"sqrt({d_K})")
    cls_old = r["verdict"]
    cls_new, val_new = classify_full(Rf_str, d_K, sqDk)
    if cls_new != cls_old:
        rat = "rat" if r["is_rational"] else "Hecke"
        print(f"  D={r['D']:>5} h={r['h']} j={r['j']} ({rat}): {cls_old} --> {cls_new}  val={val_new}")
        r["verdict"] = cls_new
        r["value"] = val_new
        upgraded_count += 1

print()
print(f"Upgraded {upgraded_count} verdicts")

# Final stats
n_total = len(results)
n_rat = sum(1 for r in results if r["is_rational"])

print()
print("=" * 70)
print("FINAL VERDICTS")
print("=" * 70)
from collections import Counter
v_all = Counter(r["verdict"] for r in results)
v_rat = Counter(r["verdict"] for r in results if r["is_rational"])
v_hecke = Counter(r["verdict"] for r in results if not r["is_rational"])
print(f"All ({n_total}): {dict(v_all)}")
print(f"Rational ({n_rat}): {dict(v_rat)}")
print(f"Hecke ({n_total - n_rat}): {dict(v_hecke)}")

print()
print("Rational forms by verdict (M114.B test):")
print(f"  R(f) ∈ Q (uniqueness violation): {v_rat.get('Q', 0)}")
print(f"  R(f) ∈ Q*sqrt(d_K) (M97 pattern): {v_rat.get('Q*sqrt(d_K)', 0)}")
print(f"  R(f) ∈ OTHER: {v_rat.get('OTHER', 0)}")

# Save updated
with open("/root/crossed-cosmos/notes/eci_v7_aspiration/M162_OPUS_HEEGNER_H3_H4/04_results.json", "w") as f:
    json.dump(results, f, indent=2, default=str)
print()
print("Updated results saved.")

# Group by D, list "interesting" non-rational forms
print()
print("=" * 70)
print("Non-rational forms with R(f) NOT 'OTHER':")
print("=" * 70)
for r in results:
    if not r["is_rational"] and r["verdict"] != "OTHER":
        print(f"  D={r['D']:>5} h={r['h']} j={r['j']} a2={r['a2'][:50]} verdict={r['verdict']} val={r['value']}")
