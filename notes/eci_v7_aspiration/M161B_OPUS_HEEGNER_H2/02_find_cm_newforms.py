#!/usr/bin/env python3
"""
M161B Sub-task 2: Find weight-5 CM newforms attached to imaginary quadratic
fields with h=2.

For h=1 (M97), Heegner-Stark, the CM newform is unique at level N = |D| (or
N = |D|/4 for D = -4, etc.) with the quadratic Kronecker character chi_D.

For h=2, there exist multiple Hecke characters of K with the same infinity
type, distinguished by class group character. The associated theta series
on Gamma_0(|D|) split into different newforms.

PARI test approach:
1. For each h=2 D, examine the space S_5(N, chi_D) where chi_D is the
   Kronecker symbol mod |D|.
2. Find newforms with CM by K = Q(sqrt(D)).
3. Compute L-values L(f,1), L(f,2), L(f,3), L(f,4) at 80-digit precision.

Conductor formula (M85): For ECI/CM weight k=5 on K with disc D,
  N = |D| · cond(psi)^2 / cond(chi)
For trivial conductor and fundamental D, expect N = |D|.

For h=2 with non-trivial class character, the conductor may differ.
The principal genus character gives N_0 = |D|, but other characters can
give larger conductors.

This sub-task does the PARI search for forms at N in {|D|} primarily,
with fallback to N = 2*|D|, 4*|D| if necessary.
"""

import cypari2
pari = cypari2.Pari()
pari.set_real_precision(80)
pari.allocatemem(1024 * 1024 * 1024)  # 1 GB stack

# h=2 target fields: D and the associated Kronecker character mod |D|
# Conrey index pattern from M62/M97: chi = Mod(|D|-1, |D|) for prime D
# For composite D, find the Kronecker character via:
# chi(n) = Kronecker(D, n)
# Then identify Conrey index via znchar

target_fields = [
    {"D": -15, "K": "Q(sqrt(-15))", "N": 15, "h": 2},
    {"D": -20, "K": "Q(sqrt(-5))",  "N": 20, "h": 2},
    {"D": -24, "K": "Q(sqrt(-6))",  "N": 24, "h": 2},
    {"D": -35, "K": "Q(sqrt(-35))", "N": 35, "h": 2},
    {"D": -40, "K": "Q(sqrt(-10))", "N": 40, "h": 2},
    {"D": -88, "K": "Q(sqrt(-22))", "N": 88, "h": 2},
]

def find_kronecker_conrey(D, N):
    """Find Conrey index of the Kronecker character chi_D mod N."""
    # chi_D(n) = Kronecker(D, n) for gcd(n, N) = 1
    # We search over odd Conrey indices for the matching character.
    G = pari.znstar(N, 1)
    # Get list of all primitive characters
    chars = []
    candidate_n = []
    for c in range(1, N):
        if pari.gcd(c, N) != 1:
            continue
        # znchar(Mod(c, N)) returns the Conrey-form character data
        chi_list = pari.znchar(pari(f"Mod({c}, {N})"))
        # Test if chi(p) = Kronecker(D, p) for first several primes
        ok = True
        for p in [3, 5, 7, 11, 13, 17, 19, 23, 29]:
            if pari.gcd(p, N) != 1:
                continue
            # chareval(G, chi, n) returns log_zeta value, or oo
            # Simpler: use chareval with second flag = -1 for value
            # The cleanest: use chareval(G, chi, p, [zeta, ord])
            # We just check sign
            # value of chi(p) as 0 (if 1), 1/2 (if -1), or fractional
            # Use chareval with the right syntax:
            try:
                val = pari.chareval(G, chi_list, p)  # returns rational in [0,1)
                # 0 -> +1, 1/2 -> -1
                kron = int(pari.kronecker(D, p))
                if kron == 1 and val != 0:
                    ok = False
                    break
                if kron == -1 and val != pari("1/2"):
                    ok = False
                    break
                if kron == 0:
                    # p divides N, skip
                    continue
            except Exception:
                ok = False
                break
        if ok:
            candidate_n.append(c)
    return candidate_n

print("=" * 70)
print("M161B Sub-task 2: Identify Kronecker Conrey indices for h=2 fields")
print("=" * 70)

for fld in target_fields:
    D = fld["D"]
    N = fld["N"]
    print()
    print(f"Field K={fld['K']}, D={D}, N={N}")
    print("-" * 50)
    candidates = find_kronecker_conrey(D, N)
    print(f"  Conrey candidates matching Kronecker(D,.): {candidates}")
    fld["conrey_candidates"] = candidates

    # Verify that each candidate gives the right Kronecker pattern
    if candidates:
        c = candidates[0]
        chi = pari.znchar(pari(f"Mod({c}, {N})"))
        print(f"  Using Conrey c={c}: chi(p) for p in [3..29]:")
        for p in [3, 5, 7, 11, 13, 17, 19, 23]:
            if pari.gcd(p, N) == 1:
                try:
                    val = pari.chareval(pari.znstar(N, 1), chi, p)
                    sign = "+1" if val == 0 else ("-1" if val == pari("1/2") else f"order_{val}")
                    kron = int(pari.kronecker(D, p))
                    match = "OK" if (sign == "+1" and kron == 1) or (sign == "-1" and kron == -1) else "MISMATCH"
                    print(f"    p={p:>3}: chi={sign}  Kron(D,p)={kron:+d}  [{match}]")
                except Exception as e:
                    print(f"    p={p:>3}: error {e}")

print()
print("=" * 70)
print("Sub-task 2 complete: Conrey indices identified for h=2 quadratic chars")
print("=" * 70)
