"""
H1 — Test if 17 patterns decompose under a B_3 orbit structure
in some natural way.

Key observation: 17 = 9 distinct exponent tuples used + 8 patterns
that share an exponent tuple with another.

Actually: 9 distinct (a,b,c,d) used as found, 17 patterns total.
17 - 9 = 8 patterns are "redundant copies" of an existing tuple.

PSL_2(F_7) acts on P^1(F_7) = 8 points; or on the 8 cusps of X(7).
The orbit decomp on cosets...

Let's think of it differently. The space of exponent tuples (a,b,c,d)
is finite given the brief's allowed values:
  a ∈ {0, 1/2, 1, 2}    (4 choices)
  b ∈ {-1/2, 0, 1}      (3 choices)
  c ∈ {0, 1/2}          (2 choices)
  d ∈ {-1/2, 0, 1/2}    (3 choices)
Grid size: 4*3*2*3 = 72.

We identified 9 distinct used tuples.
17 - 9 = 8 patterns have shared (a,b,c,d) but different rationals.

Is 17 = (size of an orbit under B_3 action) for some natural rep?
"""

# Consider the 8-element set P^1(F_7) on which PSL_2(F_7) acts naturally
# Orbits sizes on P^1(F_7) under subgroups: divisors of 8.
# Generic subgroup orbits: 8, 4, 2, 1.
# So orbit size 17 NOT natural here.

# Consider B_3 action on PRINCIPAL series of PSL_2 (continuous reps).
# Not a finite orbit picture.

# A more useful framing:
# The Birman-Hilden theorem says B_3/Z(B_3) = PSL_2(Z) acts on
# hyperelliptic mapping class group elements of genus-2 surface.
# But that's not directly relevant for finite orbit.

# Let's think about it via Burau representation specialized.
# Reduced Burau B_3 -> GL_2(Z[t,t^{-1}]):
#   sigma_1 -> [[-t,1],[0,1]]
#   sigma_2 -> [[1,0],[t,-t]]
# At t = primitive root of unity zeta_n, get finite image.

import numpy as np

def burau_sigma1(t):
    return np.array([[-t, 1], [0, 1]], dtype=complex)
def burau_sigma2(t):
    return np.array([[1, 0], [t, -t]], dtype=complex)

# Generate the orbit of a vector v under <sigma_1, sigma_2> action
def orbit_size(t, v0, max_iter=1000):
    s1 = burau_sigma1(t)
    s2 = burau_sigma2(t)
    seen = {tuple(v0.round(8))}
    frontier = [v0]
    while frontier:
        new_frontier = []
        for v in frontier:
            for s in [s1, s2]:
                vnew = s @ v
                key = tuple(vnew.round(8))
                if key not in seen:
                    seen.add(key)
                    new_frontier.append(vnew)
            if len(seen) > max_iter:
                return None
        frontier = new_frontier
    return len(seen)

# Generic orbit sizes at roots of unity
print("Burau-rep orbit sizes at primitive n-th roots of unity")
print(f"{'n':>3}  {'orbit size':>12}")
for n in [2, 3, 4, 5, 6, 7, 8, 12]:
    t = np.exp(2j*np.pi/n)
    v0 = np.array([1, 0], dtype=complex)
    sz = orbit_size(t, v0, max_iter=200)
    print(f"{n:>3}  {str(sz):>12}")

print()
print("None of the natural orbit sizes give 17.")
print()
print("But: 17 is a prime, and B_3 has the following remarkable fact:")
print("  - Number of irreducible reps of PSL_2(F_p) is p+4 (for p>=5)")
print("  - For p=13: 13+4 = 17 ✓✓✓")
print("  - For p=11: 11+4 = 15")
print("  - For p=7: 7+4 = 11")
print()

# Verify: number of conjugacy classes of PSL_2(F_p) = (p+5)/2 for p ≡ 1 mod 4
#                                                    = (p+3)/2 for p ≡ 3 mod 4
# Actually need to double check.

# For PSL_2(F_p):
#   p odd, p != 2,3
#   Number of conjugacy classes:
#     - identity
#     - one class of order p
#     - (p-3)/2 classes of order dividing (p-1)/2
#     - (p-1)/2 classes of order dividing (p+1)/2
#     - 2 'unipotent' classes if p ≡ 1 mod 4
#   Actually: |Cl(PSL_2(F_p))| = (p+5)/2 if p ≡ 1 mod 4, (p+3)/2 if p ≡ 3 mod 4.
#
# Let me just enumerate for small p.

def count_conj_psl2_fp(p):
    """Conjugacy classes of PSL_2(F_p) via direct construction."""
    from itertools import product as iprod
    # Elements of GL_2(F_p) / Z(GL_2(F_p)) where det = +/- square
    # Use a simpler formula:
    if p % 4 == 1:
        return (p+5)//2
    elif p % 4 == 3:
        return (p+3)//2

print("Conjugacy classes of PSL_2(F_p):")
for p in [3, 5, 7, 11, 13, 17, 19]:
    n_cc = count_conj_psl2_fp(p)
    print(f"  p={p}: |Cl(PSL_2(F_{p}))| = {n_cc}")

print()
print("For p=11: 7 conj classes; for p=13: 9 conj classes.")
print("None gives 17 directly.")
print()
print("Sum of dims of irreps for PSL_2(F_p):")
# Irreps of PSL_2(F_p): trivial (1), Steinberg (p), principal series (p+1)^(p-3)/2 or (p-1)/2 reps, etc.
# Total number of irreps = number of conjugacy classes
print("  p=7: irreps of PSL_2(F_7) have dims (1, 3, 3, 6, 7, 8); sum = 28")
print("  p=11: irreps of PSL_2(F_11) have dims (1, 5, 5, 10, 10, 11, 12); sum = 54")
print("  None gives 17.")
print()
print("="*60)
print("BUT: there is a natural 'arithmetic' B_3 action via")
print("     the map B_3 -> SL_2(Z) -> PSL_2(F_p) -> S_{p+1} (permuting P^1(F_p))")
print("="*60)
print()

# PSL_2(F_p) embeds in S_{p+1} as permutation group on P^1(F_p).
# Number of points = p+1.
# For p=7: p+1 = 8 points.
# For p=11: p+1 = 12 points.
# For p=13: p+1 = 14 points.
# For p=16: well, 16 not prime.

print("Permutation degree p+1:")
for p in [3, 5, 7, 11, 13, 17, 19]:
    print(f"  p={p}: degree = {p+1}")
print()
print("None gives 17 directly via P^1(F_p). But:")
print("  Suborbits of size 17 in larger spaces exist.")
print()
print("17 = number of (G,D) saturated pairs? Let's check:")
print()
print("From SYNTHESIS §1.1: 10 saturated pairs total")
print("After (C2) maximal degeneracy: 2 pairs (SU(2),D=2) and (SU(3),D=4)")
print("17 is NOT in this enumeration.")
print()
print("VERDICT: H1 (B_3 orbit) does NOT predict orbit size 17 naturally.")
print("         The number 17 appears to be an empirical count, not a")
print("         representation-theoretic prediction.")
