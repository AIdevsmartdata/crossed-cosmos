#!/usr/bin/env python3
"""
M161B Sub-task 3: Compute L(f, m) for m=1,2,3,4 for the CM newforms found
in sub-task 2c.

For each h=2 D, focus on the rational CM newforms (j=1, j=2 in M97-style
notation). These are typically Galois conjugates over Q (one is the
chi-twist of the other).

Compute R(f) = pi * L(f,1) / L(f,2) and test if it lies in:
- Q (uniqueness pattern continuing from Q(i))
- Q · sqrt(d) (M97 pattern from h=1 non-Q(i) Heegner-Stark fields)
- Q · sqrt(d') for d' = D/4 or other related quadratic
- Biquadratic Q(i, sqrt(d)) per M108-REFINED Lemma

NOTE: For h=2, "d" in field K=Q(sqrt(d)) may not equal -|D|. We use
- D = fundamental discriminant
- d_K = D for K = Q(sqrt(d_K))
- |d_K| is what we test in sqrt term

For reference, in h=1:
- D=-3, d=3
- D=-4, d=1 (UNIQUE, R rational)
- D=-7, d=7
- D=-8, d=2
- D=-11, d=11
- D=-19, d=19
- D=-43, d=43
- D=-67, d=67
- D=-163, d=163

For h=2 mission targets:
- D=-15, K=Q(sqrt(-15)), d=15
- D=-20, K=Q(sqrt(-5)),  d=5  (NOTE: d != |D|/4 = 5 here, hmm wait yes it does)
  Actually D=-20 so |D|=20, and d_K = -5, so d=5. Disc = 4·d_K = -20. Yes.
- D=-24, K=Q(sqrt(-6)),  d=6  (D = 4·(-6) = -24)
- D=-35, K=Q(sqrt(-35)), d=35
- D=-40, K=Q(sqrt(-10)), d=10 (D = 4·(-10))
- D=-88, K=Q(sqrt(-22)), d=22 (D = 4·(-22))
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

def classify_R(Rf, d_K, label):
    """Test rationality of R = pi*L1/L2."""
    sqd = pari(f"sqrt({d_K})")
    sqDk = pari(f"sqrt({d_K})")  # |d_K|
    B9 = 10**9
    Rfq = pari.bestappr(Rf, B9)
    Rfr = pari.bestappr(Rf / sqDk, B9)
    rq = abs(Rf - Rfq)
    rr = abs(Rf - Rfr * sqDk)
    print(f"  Rf = {Rf}")
    print(f"  Rf bestappr Q = {Rfq}, residual = {rq}")
    print(f"  Rf/sqrt({d_K}) bestappr = {Rfr}, residual sqrt = {rr}")
    if pari.abs(rq) < pari("1e-50"):
        print(f"  VERDICT_{label}: Rf IN Q  =  {Rfq}")
        return ("Q", Rfq)
    elif pari.abs(rr) < pari("1e-50"):
        print(f"  VERDICT_{label}: Rf IN Q*sqrt({d_K}) = ({Rfr})*sqrt({d_K})")
        return ("Q*sqrt", Rfr)
    else:
        # Test biquadratic Q(i, sqrt(d_K)): Rf = a + b*i + c*sqrt(d_K) + d*i*sqrt(d_K)?
        # For real Rf (which should be the case for CM L-values), no i component.
        # Test Q + Q*sqrt(d_K), but bestappr already failed.
        # Try: Rf as a*sqrt(d_K) + b for general a, b ∈ Q
        # Use lindep to find linear relation [1, sqrt(d_K), Rf]
        try:
            ld = pari.lindep([pari(1), sqDk, Rf])
            if ld is not None:
                print(f"  Lindep [1, sqrt({d_K}), Rf] = {ld}")
        except Exception as e:
            pass
        return ("UNCLASSIFIED", None)

print("=" * 70)
print("M161B Sub-task 3: L-values and R(f) for h=2 rational CM newforms")
print("=" * 70)

for fld in target_fields:
    D = fld["D"]
    d_K = fld["d_K"]
    N = fld["N"]
    c = fld["conrey"]
    print()
    print("=" * 60)
    print(f"=== D={D}  K={fld['K']}  N={N}  Conrey c={c} ===")
    print("=" * 60)
    chi = pari.znchar(pari(f"Mod({c}, {N})"))
    try:
        mf = pari.mfinit([N, 5, chi], 1)
        B = pari.mfeigenbasis(mf)
        nforms = int(pari.length(B))
        print(f"  nforms = {nforms}")
    except Exception as e:
        print(f"  mfinit/eigenbasis failed: {e}")
        continue

    fld["lvalues"] = {}
    for j in range(1, nforms + 1):
        F = B[j-1]
        # Determine if a_2 is rational
        try:
            a2 = pari.mfcoef(F, 2)
            a2_type = pari.type(a2)
            print(f"  --- j={j}, a2={a2}, type={a2_type} ---")
        except Exception as e:
            print(f"  j={j}: cannot read a2: {e}")
            continue

        try:
            Lobj = pari.lfunmf(mf, F)
        except Exception as e:
            print(f"  j={j}: lfunmf failed: {e}")
            continue

        # For higher-degree forms, lfunmf returns a vector of L-functions.
        # Compute L-values; if Lobj is a vector, lfun(Lobj[1], 1) etc.
        # First check type of Lobj
        try:
            L1 = pari.lfun(Lobj, 1)
            L2 = pari.lfun(Lobj, 2)
            L3 = pari.lfun(Lobj, 3)
            L4 = pari.lfun(Lobj, 4)
        except Exception as e:
            # might be a vector; try Lobj[0] (cypari2 0-indexed)
            try:
                # If Lobj is a t_VEC of L-functions (one per Galois conjugate)
                Lobj_first = Lobj[0]
                L1 = pari.lfun(Lobj_first, 1)
                L2 = pari.lfun(Lobj_first, 2)
                L3 = pari.lfun(Lobj_first, 3)
                L4 = pari.lfun(Lobj_first, 4)
                print(f"    [used Lobj[0] for higher-degree form]")
            except Exception as e2:
                print(f"  j={j}: lfun failed: {e}, retry: {e2}")
                continue

        print(f"    L(f,1) = {L1}")
        print(f"    L(f,2) = {L2}")
        print(f"    L(f,3) = {L3}")
        print(f"    L(f,4) = {L4}")

        Rf = pari.Pi() * L1 / L2
        Rf_str = str(Rf)[:80]
        print(f"    R(f) = pi*L(f,1)/L(f,2) = {Rf_str}...")
        verdict, value = classify_R(Rf, d_K, f"D{D}_j{j}")
        fld["lvalues"][j] = {"L1": L1, "L2": L2, "L3": L3, "L4": L4, "R": Rf, "verdict": verdict, "value": value}

print()
print("=" * 70)
print("SUMMARY: R(f) classification for each h=2 newform")
print("=" * 70)
for fld in target_fields:
    print()
    print(f"D={fld['D']}, K={fld['K']}, d_K={fld['d_K']}:")
    for j, data in fld.get("lvalues", {}).items():
        v = data["verdict"]
        val = data["value"]
        print(f"  j={j}: VERDICT = {v}, value = {val}")
