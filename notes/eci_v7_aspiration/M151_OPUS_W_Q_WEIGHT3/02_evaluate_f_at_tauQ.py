#!/usr/bin/env python3
"""
M151 / Step 2 -- Evaluate weight-3 newforms 88.3.b.a, 88.3.b.b at tau_Q.

We have a_n for n=1..20.
We extend by multiplicativity using Hecke relations:
  a_{p^k} = a_p * a_{p^{k-1}} - chi(p) * p^{k-1} * a_{p^{k-2}}
For weight 3, p^{k-1} should be p^(weight-1) = p^2.
  a_{p^k} = a_p a_{p^{k-1}} - chi(p) p^2 a_{p^{k-2}}

For CM newforms with chi = chi_{-22} (Kronecker -22/.) of conductor 88, the multiplicativity
holds with chi(p) = (-22/p).

We extend a_n for n up to ~50 by:
  - a_{mn} = a_m a_n if gcd(m,n)=1
  - a_{p^k} = a_p a_{p^{k-1}} - chi(p) p^2 a_{p^{k-2}}
"""

import mpmath as mp
mp.mp.dps = 40

# Kronecker symbol (-22/n) -- compute via prime factorization
def kronecker(a, b):
    """Compute Kronecker symbol (a/b) for any integer a and any positive integer b."""
    if b == 0:
        return 1 if abs(a) == 1 else 0
    # Make b positive
    if b < 0:
        b = -b
        s = -1 if a < 0 else 1
    else:
        s = 1
    # Factor out 2s from b
    while b % 2 == 0:
        b //= 2
        if a % 2 == 0:
            return 0
        if a % 8 in (3, 5):
            s = -s
    # Now b is odd positive
    a = a % b
    while a != 0:
        while a % 2 == 0:
            a //= 2
            if b % 8 in (3, 5):
                s = -s
        # Swap a, b
        a, b = b, a
        if a % 4 == 3 and b % 4 == 3:
            s = -s
        a = a % b
    return s if b == 1 else 0


def chi_neg22(n):
    """Kronecker character chi_{-22}(n) = (-22/n) -- nebentypus of 88.3.b.*"""
    return kronecker(-22, n)


# Test
print("Kronecker (-22/p) for small odd primes (excluding ramified 2, 11):")
for p in [3, 5, 7, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47]:
    print(f"  (-22/{p}) = {chi_neg22(p)}")
print()

# LMFDB Hecke eigenvalues
a_a_seed = {
    1: 1, 2: -2, 3: 0, 4: 4, 5: 0, 6: 0, 7: 0, 8: -8, 9: 9, 10: 0,
    11: 11, 12: 0, 13: 18, 14: 0, 15: 0, 16: 16, 17: 0, 18: -18, 19: 6, 20: 0
}
a_b_seed = {
    1: 1, 2: 2, 3: 0, 4: 4, 5: 0, 6: 0, 7: 0, 8: 8, 9: 9, 10: 0,
    11: -11, 12: 0, 13: -18, 14: 0, 15: 0, 16: 16, 17: 0, 18: 18, 19: -6, 20: 0
}

# Verify Hecke relation a_4 = a_2^2 - chi(2) * 2^2 * a_1
# chi(2) = 0 (ramified), so a_4 = a_2^2 = (-2)^2 = 4. ✓
print(f"Hecke check 88.3.b.a: a_4 ?= a_2^2 - chi(2)*4*a_1: {(-2)**2 - 0} = a_4 = {a_a_seed[4]}  ✓")
# a_8 = a_2 a_4 - chi(2) * 4 * a_2 = -2 * 4 - 0 = -8. ✓
print(f"Hecke check 88.3.b.a: a_8 ?= a_2*a_4 - chi(2)*4*a_2: {(-2)*4 - 0} = a_8 = {a_a_seed[8]}  ✓")
# a_9 = a_3^2 - chi(3) * 9 * a_1 = 0 - (-1)*9*1 = 9. ✓ chi(3) = (-22/3) = ?
print(f"chi(3) = (-22/3) = {chi_neg22(3)}")
print(f"Hecke check 88.3.b.a: a_9 ?= a_3^2 - chi(3)*9*a_1 = 0 - ({chi_neg22(3)})*9*1 = {-chi_neg22(3)*9}, a_9 = {a_a_seed[9]}  ✓ if matches")
# a_18 = a_2 a_9 = -2 * 9 = -18. ✓
print(f"Hecke check 88.3.b.a: a_18 ?= a_2*a_9 = {(-2)*9} = a_18 = {a_a_seed[18]}  ✓")
# a_22 = a_2 a_11 = -2 * 11 = -22. (level prime ramified, so a_11 is special)
# Actually for level-N prime, a_p is the Atkin-Lehner eigenvalue * p^{(k-1)/2} or similar
print()

# Now extend a_n to n up to N_MAX using multiplicativity
def extend_a(a_seed, chi, N_MAX=500):
    """Extend Hecke eigenvalues by multiplicativity.
    a_{p^k} = a_p * a_{p^{k-1}} - chi(p) * p^2 * a_{p^{k-2}}  (weight 3)
    a_{mn} = a_m * a_n if gcd(m, n) = 1
    """
    a = dict(a_seed)
    a[1] = 1
    # Sieve primes up to N_MAX
    primes = []
    is_p = [True] * (N_MAX + 1)
    is_p[0] = is_p[1] = False
    for i in range(2, N_MAX + 1):
        if is_p[i]:
            primes.append(i)
            for j in range(i * i, N_MAX + 1, i):
                is_p[j] = False
    # First, extend a_{p^k} for known primes using Hecke
    for p in primes:
        if p > N_MAX:
            break
        if p not in a:
            # We don't have a_p ; can't extend
            continue
        ap = a[p]
        # a_{p^k} for k=2, 3, ...
        prev2 = a[1]  # a_{p^0} = 1
        prev1 = ap    # a_{p^1}
        k = 2
        pk = p * p
        while pk <= N_MAX:
            # a_{p^k} = a_p * a_{p^{k-1}} - chi(p) * p^2 * a_{p^{k-2}}
            ak = ap * prev1 - chi(p) * p**2 * prev2
            if pk not in a:
                a[pk] = ak
            prev2 = prev1
            prev1 = ak
            k += 1
            pk *= p
    # Now extend by multiplicativity to all n <= N_MAX
    for n in range(2, N_MAX + 1):
        if n in a:
            continue
        # Find prime factor
        for p in primes:
            if p > n:
                break
            if n % p == 0:
                # Find p^k || n
                m = n
                pk = 1
                while m % p == 0:
                    m //= p
                    pk *= p
                # n = pk * m, gcd(pk, m) = 1
                if pk in a and m in a:
                    a[n] = a[pk] * a[m]
                break
    return a


N_MAX = 500
a_a = extend_a(a_a_seed, chi_neg22, N_MAX=N_MAX)
a_b = extend_a(a_b_seed, chi_neg22, N_MAX=N_MAX)

# Verify against seed
print("Extended a_a vs seed (n=1..20):")
mismatch_a = []
for n in range(1, 21):
    if a_a[n] != a_a_seed[n]:
        mismatch_a.append((n, a_a_seed[n], a_a[n]))
print(f"  Mismatches: {mismatch_a if mismatch_a else 'None ✓'}")
mismatch_b = []
for n in range(1, 21):
    if a_b[n] != a_b_seed[n]:
        mismatch_b.append((n, a_b_seed[n], a_b[n]))
print("Extended a_b vs seed (n=1..20):")
print(f"  Mismatches: {mismatch_b if mismatch_b else 'None ✓'}")
print()

# Print extended a_n for n=21..50
print("Extended a_n for 88.3.b.a, n=21..50:")
print("  ", [a_a.get(n, '?') for n in range(21, 51)])
print("Extended a_n for 88.3.b.b, n=21..50:")
print("  ", [a_b.get(n, '?') for n in range(21, 51)])
print()

# Now evaluate f(tau_Q) = sum a_n q^n
tau_Q = mp.mpc(0, mp.sqrt(mp.mpf(11)/2))
q_Q = mp.exp(2j * mp.pi * tau_Q)
print(f"q_Q = {q_Q}")
print()

def eval_f(a_dict, q, N_MAX):
    s = mp.mpc(0, 0)
    for n in range(1, N_MAX + 1):
        if n in a_dict:
            s += a_dict[n] * q**n
    return s

f_a_Q = eval_f(a_a, q_Q, N_MAX)
f_b_Q = eval_f(a_b, q_Q, N_MAX)

print(f"f_88.3.b.a (tau_Q) = {f_a_Q}")
print(f"|f_a (tau_Q)|     = {abs(f_a_Q)}")
print()
print(f"f_88.3.b.b (tau_Q) = {f_b_Q}")
print(f"|f_b (tau_Q)|     = {abs(f_b_Q)}")
print()

# Compare:
ratio = f_a_Q / f_b_Q if f_b_Q != 0 else None
print(f"Ratio f_a/f_b at tau_Q = {ratio}")
print()
print("Convergence check: a_n |q|^n bound")
for n in [50, 100, 200, 300, 400]:
    if n in a_a:
        bound = abs(a_a[n]) * abs(q_Q)**n
        print(f"  n={n}: |a_n q^n| ~ {mp.nstr(bound, 5)}")
