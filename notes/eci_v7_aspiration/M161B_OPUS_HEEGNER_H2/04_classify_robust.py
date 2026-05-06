#!/usr/bin/env python3
"""
M161B Sub-task 4: Robust classification of R(f) for ALL h=2 newforms,
including the higher-degree forms with COMPLEX L-values.

For each newform f at level N=|D|, weight 5, character chi_D:
- Compute L(f, m) at 80-digit precision
- Compute R(f) = pi * L(f,1) / L(f,2)
- Classify R(f) as:
  (R) Real rational  R ∈ Q
  (S) Real Q*sqrt(d_K)
  (B) Biquadratic Q(i, sqrt(d_K))
  (X) Other / unclassified

Output a clean summary suitable for SUMMARY.md.
"""

import cypari2
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

EPS = pari("1.0e-50")
B9 = 10**9

def real_norm(z):
    """Return |z| as PARI real."""
    return pari.abs(z)

def is_small(x, eps=EPS):
    """Check if PARI quantity has absolute value below eps."""
    try:
        a = pari.abs(x)
        # Compare a < eps using PARI comparison
        return a < eps
    except Exception:
        return False

def classify_R(Rf, d_K):
    """Classify R(f) into Q, Q*sqrt(d_K), Q(i, sqrt(d_K)) or other."""
    sqDk = pari(f"sqrt({d_K})")
    # Test 1: real rational
    Re = pari.real(Rf)
    Im = pari.imag(Rf)
    has_im = not is_small(Im, pari("1.0e-30"))

    result = {"Re": Re, "Im": Im, "has_im": has_im}

    # Try Q
    Rfq = pari.bestappr(Rf, B9)
    rq = real_norm(Rf - Rfq)
    result["Q_appr"] = Rfq
    result["Q_residual"] = rq

    # Try Q*sqrt(d_K) — only meaningful if real
    if not has_im:
        Rfr = pari.bestappr(Rf / sqDk, B9)
        rr = real_norm(Rf - Rfr * sqDk)
        result["sqrt_appr"] = Rfr
        result["sqrt_residual"] = rr
    else:
        result["sqrt_appr"] = None
        result["sqrt_residual"] = None

    # Try biquadratic Q(i, sqrt(d_K)) using lindep on basis [1, sqrt(d_K), i, i*sqrt(d_K)]
    try:
        i_unit = pari("I")
        basis = [pari(1), sqDk, i_unit, i_unit * sqDk]
        target_real = pari.real(Rf)
        target_imag = pari.imag(Rf)
        # For real Rf, only [1, sqrt(d_K)] in real part
        # For complex Rf, need full basis — but lindep over R is limited
        # Better: separate Re(Rf), Im(Rf) and check each is in Q + Q*sqrt(d_K)
        Re_q = pari.bestappr(Re, B9)
        Re_r = pari.bestappr(Re / sqDk, B9)
        Im_q = pari.bestappr(Im, B9) if has_im else pari(0)
        Im_r = pari.bestappr(Im / sqDk, B9) if has_im else pari(0)
        # Test Re ∈ Q + Q*sqrt(d_K) using lindep
        ld_re = pari.lindep([pari(1), sqDk, Re])
        ld_im = pari.lindep([pari(1), sqDk, Im]) if has_im else None
        result["lindep_Re"] = ld_re
        result["lindep_Im"] = ld_im
    except Exception as e:
        result["lindep_error"] = str(e)

    # VERDICT
    if rq < EPS:
        result["verdict"] = "Q"
        result["value"] = Rfq
        return result
    if not has_im and result["sqrt_residual"] < EPS:
        result["verdict"] = "Q*sqrt"
        result["value"] = result["sqrt_appr"]
        return result

    # Check biquadratic: Re and Im both in Q + Q*sqrt(d_K) ?
    if has_im:
        # Use lindep [1, sqrt(d), Re] and [1, sqrt(d), Im]
        ld_re = result.get("lindep_Re")
        ld_im = result.get("lindep_Im")
        # Lindep returns a vector [a, b, c] with a + b*sqrt(d) + c*Re = 0 if rel exists
        # Magnitude of c: if c = 0, no rel; if c ≠ 0 and small, exact rel
        try:
            if ld_re is not None and ld_im is not None:
                a_re, b_re, c_re = int(ld_re[0]), int(ld_re[1]), int(ld_re[2])
                a_im, b_im, c_im = int(ld_im[0]), int(ld_im[1]), int(ld_im[2])
                if c_re != 0 and c_im != 0:
                    # Re = -(a_re + b_re*sqrt(d)) / c_re
                    # Im = -(a_im + b_im*sqrt(d)) / c_im
                    Re_expected = -(pari(a_re) + pari(b_re) * sqDk) / pari(c_re)
                    Im_expected = -(pari(a_im) + pari(b_im) * sqDk) / pari(c_im)
                    res_re = real_norm(Re - Re_expected)
                    res_im = real_norm(Im - Im_expected)
                    if res_re < EPS and res_im < EPS:
                        result["verdict"] = "Biquadratic Q(i,sqrt(d))"
                        result["value"] = (Re_expected, Im_expected)
                        return result
        except Exception as e:
            pass

    result["verdict"] = "OTHER"
    result["value"] = None
    return result

print("=" * 70)
print("M161B Sub-task 4: ROBUST classification of R(f) for h=2 newforms")
print("=" * 70)

all_results = []

for fld in target_fields:
    D = fld["D"]
    d_K = fld["d_K"]
    N = fld["N"]
    c = fld["conrey"]
    print()
    print(f"=== D={D}  K={fld['K']}  N={N}  Conrey c={c} ===")
    chi = pari.znchar(pari(f"Mod({c}, {N})"))
    mf = pari.mfinit([N, 5, chi], 1)
    B = pari.mfeigenbasis(mf)
    nforms = int(pari.length(B))
    print(f"  nforms = {nforms}")

    for j in range(1, nforms + 1):
        F = B[j-1]
        a2 = pari.mfcoef(F, 2)
        a2_t = pari.type(a2)
        print(f"  --- j={j}, a2={a2}, type={a2_t} ---")
        try:
            Lobj = pari.lfunmf(mf, F)
            try:
                L1 = pari.lfun(Lobj, 1)
            except:
                L1 = pari.lfun(Lobj[0], 1)
                Lobj = Lobj[0]
            L1 = pari.lfun(Lobj, 1)
            L2 = pari.lfun(Lobj, 2)
            L3 = pari.lfun(Lobj, 3)
            L4 = pari.lfun(Lobj, 4)
        except Exception as e:
            print(f"    L computation failed: {e}")
            continue

        Rf = pari.Pi() * L1 / L2
        result = classify_R(Rf, d_K)
        result["D"] = D
        result["d_K"] = d_K
        result["j"] = j
        result["a2"] = a2
        result["a2_type"] = str(a2_t)
        result["L1"] = L1
        result["L2"] = L2
        result["Rf"] = Rf

        # Print
        print(f"    L1={L1}")
        print(f"    L2={L2}")
        print(f"    R(f)={Rf}")
        print(f"    Re(R)={result['Re']}, Im(R)={result['Im']}, has_im={result['has_im']}")
        print(f"    Q residual = {result['Q_residual']}")
        if result.get("sqrt_residual") is not None:
            print(f"    Q*sqrt({d_K}) residual = {result['sqrt_residual']}")
        print(f"    VERDICT: {result['verdict']}, value = {result['value']}")
        all_results.append(result)

print()
print("=" * 70)
print("FINAL TABLE: R(f) for ALL h=2 newforms")
print("=" * 70)
print()
print(f"{'D':>5} {'j':>2} {'a2':>30} {'verdict':>30} {'value':>40}")
print("-" * 110)
for r in all_results:
    a2_str = str(r["a2"])[:28]
    val_str = str(r.get("value"))[:38]
    print(f"{r['D']:>5} {r['j']:>2} {a2_str:>30} {r['verdict']:>30} {val_str:>40}")

print()
print("=" * 70)
print("SUMMARY")
print("=" * 70)
n_Q = sum(1 for r in all_results if r["verdict"] == "Q")
n_Qsqrt = sum(1 for r in all_results if r["verdict"] == "Q*sqrt")
n_biquad = sum(1 for r in all_results if r["verdict"] == "Biquadratic Q(i,sqrt(d))")
n_other = sum(1 for r in all_results if r["verdict"] == "OTHER")
print(f"  Total newforms: {len(all_results)}")
print(f"  R(f) ∈ Q:                       {n_Q}")
print(f"  R(f) ∈ Q*sqrt(d_K) (M97 pattern): {n_Qsqrt}")
print(f"  R(f) ∈ Q(i, sqrt(d_K)) biquad:   {n_biquad}")
print(f"  Other/unclassified:               {n_other}")
print()

# Restrict to rational newforms (a2 in Z) — the "principal" CM forms
rational_results = [r for r in all_results if r["a2_type"] == "t_INT"]
print(f"Restricting to RATIONAL coefficient newforms (the principal CM forms):")
print(f"  Total: {len(rational_results)}")
n_Q_r = sum(1 for r in rational_results if r["verdict"] == "Q")
n_Qsqrt_r = sum(1 for r in rational_results if r["verdict"] == "Q*sqrt")
print(f"  R(f) ∈ Q:                  {n_Q_r}  <-- M114.B violation count (should be 0 for h=2)")
print(f"  R(f) ∈ Q*sqrt(d_K):        {n_Qsqrt_r}  <-- M97 pattern count")
print(f"  Other:                     {len(rational_results) - n_Q_r - n_Qsqrt_r}")
print()

# Save results to file
import json
def serialize(r):
    return {
        "D": r["D"],
        "d_K": r["d_K"],
        "j": r["j"],
        "a2_str": str(r["a2"]),
        "a2_type": r["a2_type"],
        "verdict": r["verdict"],
        "value_str": str(r.get("value")),
        "Re_str": str(r["Re"]),
        "Im_str": str(r["Im"]),
        "Q_residual_str": str(r["Q_residual"]),
        "sqrt_residual_str": str(r.get("sqrt_residual")),
        "Rf_str": str(r["Rf"]),
    }

with open("04_results.json", "w") as f:
    json.dump([serialize(r) for r in all_results], f, indent=2)
print(f"Results saved to 04_results.json")
