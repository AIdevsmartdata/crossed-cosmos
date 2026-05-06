#!/usr/bin/env python3
"""
M162 Sub-task 4: Full L-value computation in single GP script per field.

Strategy: Single direct gp script per field combining mfinit + lfunmf + L-values
at 80-digit precision. Writes results incrementally to JSON.

We use the Conrey pre-known mapping when available; otherwise enumerate.
For D ≡ 1 mod 4, often c = N-1 works (M62 pattern). For D ≡ 0 mod 4, varies.

Limit scope to fields with |D| <= 200 to control wall-clock time, plus a few
larger ones for h=4 cross-check.
"""

import json
import os
import time
import cypari2
pari = cypari2.Pari(sizemax=8 * 1024 * 1024 * 1024)

with open("/root/crossed-cosmos/notes/eci_v7_aspiration/M162_OPUS_HEEGNER_H3_H4/01_targets.json") as f:
    target_fields = json.load(f)

# Restrict to |D| <= 200 for the main run; we'll add larger fields if time permits
SMALL_TARGETS = [t for t in target_fields if abs(t["D"]) <= 200]

# Known Conrey indices: build a table by computation OR by simple formula
# For D ≡ 1 mod 4 fundamental: usually conrey = N-1 = -D-1
# For D ≡ 0 mod 4 fundamental: varies. Pre-compute.

CONREY_OVERRIDES = {
    # h=2 known from M161B
    -15: 14, -20: 19, -24: 5, -35: 34, -40: 19, -88: 21,
}


def find_kronecker_conrey(D, N):
    """Find Conrey index c with znchar(Mod(c, N)) = chi_D."""
    G = pari.znstar(N, 1)
    candidates = []
    if (N - 1) > 0 and pari.gcd(N-1, N) == 1:
        # try N-1 first
        for c_try in [N-1] + list(range(1, N)):
            if c_try in candidates:
                continue
            if pari.gcd(c_try, N) != 1:
                continue
            chi_data = pari.znchar(pari(f"Mod({c_try}, {N})"))
            chi = chi_data[1]
            order = int(pari.charorder(G, chi))
            if order != 2:
                continue
            ok = True
            tests = 0
            for p in [3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73]:
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
                if c_try == N-1:
                    return [N-1]
                candidates.append(c_try)
    return candidates


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


def classify_real(Rf, sqDk, d_K):
    Rfq = pari.bestappr(Rf, B9)
    rq = small(Rf - Rfq)
    Rfr = pari.bestappr(Rf / sqDk, B9)
    rr = small(Rf - Rfr * sqDk)
    if rq < EPS_RESID:
        return ("Q", str(Rfq), rq, rr)
    if rr < EPS_RESID:
        return ("Q*sqrt(d_K)", f"({Rfr})*sqrt({d_K})", rq, rr)
    return ("OTHER", None, rq, rr)


print("=" * 70)
print("M162 Sub-task 4: Full L-values via direct GP script")
print(f"Targets (|D| <= 200): {len(SMALL_TARGETS)}")
print("=" * 70)

OUT_PATH = "/root/crossed-cosmos/notes/eci_v7_aspiration/M162_OPUS_HEEGNER_H3_H4/04_results.json"

# Resume support
all_results = []
done_D = set()
if os.path.exists(OUT_PATH):
    try:
        with open(OUT_PATH) as f:
            all_results = json.load(f)
        done_D = set((r["D"], r["j"]) for r in all_results)
        print(f"Resumed: {len(all_results)} entries from previous run")
    except Exception:
        all_results = []
        done_D = set()

processed_D = set(r["D"] for r in all_results)

for fld in SMALL_TARGETS:
    D = fld["D"]
    if D in processed_D:
        print(f"  Skipping D={D} (already done)")
        continue
    N = fld["N"]
    d_K = fld["d_K"]
    h = fld["h"]
    print()
    print(f"=== D={D:>4}  N={N}  d_K={d_K}  h={h} ===")

    t0 = time.time()
    if D in CONREY_OVERRIDES:
        conrey = CONREY_OVERRIDES[D]
    else:
        candidates = find_kronecker_conrey(D, N)
        if not candidates:
            print(f"  *** NO CONREY MATCH ***")
            continue
        if (N - 1) in candidates:
            conrey = N - 1
        else:
            conrey = candidates[-1]

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
        im_size = small(Im_R)
        has_im = im_size > EPS_NUM

        if not has_im:
            cls, val, rq, rr = classify_real(Rf, sqDk, d_K)
        else:
            # Try Q(i): Re,Im rational
            Re_R = pari.real(Rf)
            cls = "OTHER"
            val = None
            try:
                ld_re_q = pari.lindep([pari(1), Re_R])
                ld_im_q = pari.lindep([pari(1), Im_R])
                a_r, b_r = int(ld_re_q[0]), int(ld_re_q[1])
                a_i, b_i = int(ld_im_q[0]), int(ld_im_q[1])
                if b_r != 0 and b_i != 0 and abs(a_r) < 10**11 and abs(b_r) < 10**11:
                    Re_pred = -pari(a_r) / pari(b_r)
                    Im_pred = -pari(a_i) / pari(b_i)
                    res_re = small(Re_R - Re_pred)
                    res_im = small(Im_R - Im_pred)
                    if res_re < EPS_RESID and res_im < EPS_RESID:
                        cls = "Q(i)"
                        val = f"({Re_pred})+({Im_pred})*I"
            except Exception:
                pass
            # biquadratic
            if cls == "OTHER":
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
                            cls = "Q(i,sqrt(d_K))"
                            val = f"Re=({-pari(a_r)/pari(c_r)})+({-pari(b_r)/pari(c_r)})*sqrt({d_K}); Im=({-pari(a_i)/pari(c_i)})+({-pari(b_i)/pari(c_i)})*sqrt({d_K})"
                except Exception:
                    pass
            rq = small(pari.bestappr(Rf, B9) - Rf)
            rr = None

        # Damerell ladder if real
        a1_per_sqd_dk_str = a1_per_sqd_str = a2_alpha_str = a3_per_sqd_str = None
        if not has_im:
            try:
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

        print(f"  j={j} {'[Q-rat]' if is_rat else '[Hecke]'} a2={a2}  cls={cls}  val={str(val)[:60] if val else 'None'}")
        if is_rat and a1_per_sqd_dk_str is not None:
            print(f"      alpha_1/(sqd*dK)={a1_per_sqd_dk_str}  [exp: 3/4 if D mod 4=1, 6 if 0]")

        all_results.append({
            "D": D,
            "d_K": d_K,
            "h": h,
            "N": N,
            "j": j,
            "conrey": conrey,
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
            "verdict": cls,
            "value": val,
            "Q_residual": rq,
            "sqrt_residual": rr,
            "alpha_1_per_sqd": a1_per_sqd_str,
            "alpha_2": a2_alpha_str,
            "alpha_3_per_sqd": a3_per_sqd_str,
            "alpha_1_per_sqd_dk": a1_per_sqd_dk_str,
        })

    # Write incrementally after each field
    with open(OUT_PATH, "w") as f:
        json.dump(all_results, f, indent=2, default=str)

print()
print("=" * 70)
print("DONE — Final summary")
print("=" * 70)
n_rat = sum(1 for r in all_results if r["is_rational"])
n_Q = sum(1 for r in all_results if r["verdict"] == "Q")
n_Qsqrt = sum(1 for r in all_results if r["verdict"] == "Q*sqrt(d_K)")
n_Qi = sum(1 for r in all_results if r["verdict"] == "Q(i)")
n_biquad = sum(1 for r in all_results if r["verdict"] == "Q(i,sqrt(d_K))")
n_other = sum(1 for r in all_results if r["verdict"] == "OTHER")
print(f"Total newforms: {len(all_results)}; rational: {n_rat}")
print(f"  R(f) ∈ Q: {n_Q}; Q*sqrt(d_K): {n_Qsqrt}; Q(i): {n_Qi}; Q(i,sqrt): {n_biquad}; OTHER: {n_other}")

rat_only = [r for r in all_results if r["is_rational"]]
print(f"\nAmong {len(rat_only)} rational forms:")
print(f"  R(f) ∈ Q (M114.B violation): {sum(1 for r in rat_only if r['verdict']=='Q')}")
print(f"  R(f) ∈ Q*sqrt(d_K) (M97 pattern): {sum(1 for r in rat_only if r['verdict']=='Q*sqrt(d_K)')}")
print(f"\nResults saved to {OUT_PATH}")
