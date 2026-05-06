#!/usr/bin/env python3
"""
M161B Sub-task 2c: Find Conrey index for the Kronecker character chi_D mod |D|.
Then explore the weight-5 newforms in S_5(N, chi_D).

For h=2 fields, the spaces S_5(N, chi_D) may contain multiple newforms:
- Two CM newforms attached to ψ on K (one for each class group character)
- Possibly non-CM newforms

We need to identify the CM newforms (those with Hecke character ψ on K).
Then compute L(f, m) for m=1,2,3,4 at high precision.
"""

import cypari2
pari = cypari2.Pari()
pari.set_real_precision(80)
pari.allocatemem(2 * 1024 * 1024 * 1024)  # 2 GB

target_fields = [
    {"D": -15, "K": "Q(sqrt(-15))", "N": 15, "h": 2},
    {"D": -20, "K": "Q(sqrt(-5))",  "N": 20, "h": 2},
    {"D": -24, "K": "Q(sqrt(-6))",  "N": 24, "h": 2},
    {"D": -35, "K": "Q(sqrt(-35))", "N": 35, "h": 2},
    {"D": -40, "K": "Q(sqrt(-10))", "N": 40, "h": 2},
    {"D": -88, "K": "Q(sqrt(-22))", "N": 88, "h": 2},
]

def find_kronecker_conrey(D, N):
    """Find Conrey index c such that znchar(Mod(c, N)) is chi_D = Kronecker(D, .)."""
    G = pari.znstar(N, 1)
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
        for p in [3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47]:
            if pari.gcd(p, N) != 1:
                continue
            val = pari.chareval(G, chi, p)
            chi_p = 1 if val == 0 else -1 if val == pari("1/2") else None
            kron = int(pari.kronecker(D, p))
            if chi_p != kron:
                ok = False
                break
            tests += 1
        if ok and tests >= 6:
            candidates.append(c)
    return candidates

print("=" * 70)
print("M161B Sub-task 2c: Conrey indices for h=2 quadratic fields")
print("=" * 70)

for fld in target_fields:
    D = fld["D"]
    N = fld["N"]
    print()
    print(f"D={D:>4}  K={fld['K']:>14}  N={N}")
    candidates = find_kronecker_conrey(D, N)
    fld["conrey_candidates"] = candidates
    print(f"  Conrey indices matching chi_D: {candidates}")
    if candidates:
        # Use the largest (closest to N-1) by convention from M62 pattern
        fld["conrey"] = candidates[-1]
        # also check d-1 pattern
        if (N - 1) in candidates:
            fld["conrey"] = N - 1
            print(f"  --> M62 d-1 pattern works: c={N-1}")
        else:
            print(f"  --> No d-1 pattern; using largest c={fld['conrey']}")
    else:
        fld["conrey"] = None
        print(f"  *** NO CONREY MATCH ***")

# Now explore the modular form spaces
print()
print("=" * 70)
print("Exploring weight-5 modular form spaces (mfinit)")
print("=" * 70)

for fld in target_fields:
    D = fld["D"]
    N = fld["N"]
    c = fld.get("conrey")
    print()
    print(f"=== D={D:>4}  N={N}  Conrey c={c} ===")
    if c is None:
        print(f"  Skipping (no Conrey index)")
        continue

    chi = pari.znchar(pari(f"Mod({c}, {N})"))
    try:
        # mfinit([N, k, chi], 1) — newforms only
        mf = pari.mfinit([N, 5, chi], 1)
    except Exception as e:
        print(f"  mfinit failed: {e}")
        continue

    try:
        B = pari.mfeigenbasis(mf)
        nforms = int(pari.length(B))
        print(f"  nforms = {nforms}")
        for j in range(1, nforms + 1):
            F = B[j-1]
            try:
                a2 = pari.mfcoef(F, 2)
                a3 = pari.mfcoef(F, 3)
                a5 = pari.mfcoef(F, 5)
                a7 = pari.mfcoef(F, 7)
                a11 = pari.mfcoef(F, 11)
                a13 = pari.mfcoef(F, 13)
                # Determine Hecke field: degree of coefficient field
                try:
                    deg = "rational" if isinstance(a2, type(pari("0"))) and pari.type(a2) == 't_INT' else f"a2_type={pari.type(a2)}"
                except:
                    deg = "?"
                print(f"  newform j={j}: a2={a2}  a3={a3}  a5={a5}  a7={a7}  a11={a11}  a13={a13}")
                fld[f"newform_{j}_coeffs"] = {2: a2, 3: a3, 5: a5, 7: a7}
            except Exception as e:
                print(f"  newform j={j}: error {e}")
        fld["nforms"] = nforms
    except Exception as e:
        print(f"  mfeigenbasis failed: {e}")

print()
print("=" * 70)
print("Summary of newform searches")
print("=" * 70)
for fld in target_fields:
    print(f"  D={fld['D']:>4}  N={fld['N']:>3}  conrey={fld.get('conrey')}  nforms={fld.get('nforms', '?')}")
