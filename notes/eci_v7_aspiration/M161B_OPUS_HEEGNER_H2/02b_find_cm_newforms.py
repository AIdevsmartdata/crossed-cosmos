#!/usr/bin/env python3
"""
M161B Sub-task 2b: Find Conrey index for the Kronecker character mod |D|.

Approach: znconreychar / znchargenerator finds primitive characters; we
match the Kronecker character chi_D directly using PARI's chartoprimitive
or by enumerating quadratic characters.

For prime |D|: there is a unique quadratic Dirichlet character mod |D|.
For composite |D|: there may be multiple, distinguished by behavior at
  the primes dividing |D|.

The Kronecker symbol chi_D (mod |D|) has order 2, real, and primitive
(since D is fundamental). We find its Conrey index by direct enumeration
using PARI's chareval.

Use bnrchar / charinit / chargalois more carefully.
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

print("=" * 70)
print("M161B Sub-task 2b: Match Kronecker char mod N via PARI character API")
print("=" * 70)

for fld in target_fields:
    D = fld["D"]
    N = fld["N"]
    print()
    print(f"Field K={fld['K']}, D={D}, N={N}")
    print("-" * 50)

    # Use znconreyconductor / direct znchar enumeration
    # PARI znchar(Mod(c, N)) returns [G, chi] where chi is the character.
    # chareval(G, chi, n) returns the exponent k such that chi(n) = exp(2*pi*i*k/order)
    # For order 2: 0 means chi(n) = +1, 1/2 means chi(n) = -1.

    G = pari.znstar(N, 1)
    candidates = []
    coprime_classes = [c for c in range(1, N) if pari.gcd(c, N) == 1]

    for c in coprime_classes:
        chi_data = pari.znchar(pari(f"Mod({c}, {N})"))
        chi_order = int(pari.charorder(G, chi_data))
        if chi_order != 2:
            continue
        # chi has order 2; check if chi(p) = Kronecker(D, p) for several primes
        ok = True
        tests_done = 0
        for p in [3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47]:
            if pari.gcd(p, N) != 1:
                continue
            try:
                val = pari.chareval(G, chi_data, p)
                # val is in [0, 1), val=0 -> +1, val=1/2 -> -1
                if val == 0:
                    chi_p = 1
                elif val == pari("1/2"):
                    chi_p = -1
                else:
                    chi_p = None
                kron = int(pari.kronecker(D, p))
                if chi_p != kron:
                    ok = False
                    break
                tests_done += 1
            except Exception as e:
                ok = False
                break
        if ok and tests_done >= 5:
            candidates.append(c)

    print(f"  Conrey candidates (order 2, matching Kronecker on tested primes): {candidates}")

    # Use the first candidate and verify
    if candidates:
        c = candidates[0]
        fld["conrey"] = c
        chi_data = pari.znchar(pari(f"Mod({c}, {N})"))
        print(f"  Using Conrey c={c}, chi order = {pari.charorder(G, chi_data)}")
        # Verify primitivity / conductor
        try:
            cond = pari.zncharconductor(G, chi_data)
            print(f"  conductor = {cond}")
        except:
            try:
                # Alternative API
                prim_data = pari.charinduce(G, chi_data)
                print(f"  charinduce = {prim_data}")
            except Exception as e:
                print(f"  conductor check failed: {e}")
    else:
        print(f"  *** NO valid Conrey index found ***")
        fld["conrey"] = None

print()
print("Summary:")
for fld in target_fields:
    print(f"  D={fld['D']:>4}  N={fld['N']:>3}  conrey={fld.get('conrey', 'None')}")
