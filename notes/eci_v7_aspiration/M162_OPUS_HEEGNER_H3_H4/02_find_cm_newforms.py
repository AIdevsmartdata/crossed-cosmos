#!/usr/bin/env python3
"""
M162 Sub-task 2: Find Conrey index for chi_D mod |D| at each target field;
explore weight-5 newforms via mfinit + mfeigenbasis; tag rational CM forms.

Following M161B 02c approach.
"""

import json
import cypari2
pari = cypari2.Pari(sizemax=8 * 1024 * 1024 * 1024)
pari.set_real_precision(30)  # not yet 80, just for newform exploration

with open("/root/crossed-cosmos/notes/eci_v7_aspiration/M162_OPUS_HEEGNER_H3_H4/01_targets.json") as f:
    target_fields = json.load(f)


def find_kronecker_conrey(D, N):
    """Find Conrey index c such that znchar(Mod(c, N)) = chi_D = Kronecker(D, .)."""
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
        for p in [3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67]:
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
            candidates.append(c)
    return candidates


print("=" * 70)
print("M162 Sub-task 2: Conrey indices + newform exploration")
print("=" * 70)

results_data = []
for fld in target_fields:
    D = fld["D"]
    N = fld["N"]
    print()
    print(f"=== D={D:>4}  N={N}  d_K={fld['d_K']}  h={fld['h']} ===")

    candidates = find_kronecker_conrey(D, N)
    if not candidates:
        print(f"  *** NO CONREY MATCH ***")
        fld["conrey"] = None
        results_data.append({**fld, "conrey": None, "rational_count": 0, "total_count": 0})
        continue

    # M62 d-1 pattern preference
    if (N - 1) in candidates:
        conrey = N - 1
        print(f"  Conrey c = N-1 = {conrey} (M62 d-1 pattern)")
    else:
        conrey = candidates[-1]
        print(f"  Conrey candidates: {candidates}, using largest = {conrey}")
    fld["conrey"] = conrey

    # Now do mfinit to count rational newforms
    chi = pari.znchar(pari(f"Mod({conrey}, {N})"))
    try:
        mf = pari.mfinit([N, 5, chi], 1)
    except Exception as e:
        print(f"  mfinit failed: {e}")
        results_data.append({**fld, "conrey": conrey, "rational_count": 0, "total_count": 0, "mfinit_error": str(e)})
        continue

    try:
        B = pari.mfeigenbasis(mf)
        nforms = int(pari.length(B))
        print(f"  Total newforms in S_5({N}, chi): {nforms}")

        rational_count = 0
        rationals_a2 = []
        for j in range(1, nforms + 1):
            F = B[j-1]
            try:
                a2 = pari.mfcoef(F, 2)
                a2_t = str(pari.type(a2))
                if a2_t == "t_INT":
                    rational_count += 1
                    rationals_a2.append(int(a2))
            except Exception as e:
                print(f"    j={j}: error {e}")
        print(f"  Rational newforms (CM-genus): {rational_count}")
        if rationals_a2:
            print(f"    a_2 values: {rationals_a2}")
        results_data.append({
            **fld,
            "conrey": conrey,
            "rational_count": rational_count,
            "total_count": nforms,
            "rationals_a2": rationals_a2,
        })
    except Exception as e:
        print(f"  mfeigenbasis failed: {e}")
        results_data.append({**fld, "conrey": conrey, "rational_count": 0, "total_count": 0, "mfeigen_error": str(e)})

print()
print("=" * 70)
print("SUMMARY")
print("=" * 70)
print(f"{'D':>5} {'N':>4} {'h':>2} {'conrey':>6} {'#rat':>5} {'#total':>6}  a_2 list")
print("-" * 80)
total_rat = 0
total_fields = 0
for r in results_data:
    rats = r.get("rationals_a2", [])
    rats_str = str(rats)[:40]
    print(f"{r['D']:>5} {r['N']:>4} {r['h']:>2} {str(r.get('conrey')):>6} {r.get('rational_count', 0):>5} {r.get('total_count', 0):>6}  {rats_str}")
    if r.get("conrey") is not None:
        total_fields += 1
        total_rat += r.get("rational_count", 0)

print()
print(f"Total fields with valid Conrey: {total_fields}")
print(f"Total rational CM newforms: {total_rat}")

with open("/root/crossed-cosmos/notes/eci_v7_aspiration/M162_OPUS_HEEGNER_H3_H4/02_newforms.json", "w") as f:
    json.dump(results_data, f, indent=2, default=str)
print(f"\nSaved newform exploration to 02_newforms.json")
