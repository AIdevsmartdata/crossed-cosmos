#!/usr/bin/env python3
"""
M151 / Step 3 -- Investigate the linear combination

  g(tau) = f_a(tau) - lambda * f_b(tau)

with lambda chosen so g(tau_Q) = 0. Check if g'(tau_Q) is also zero
(i.e. tau_Q is a double zero of g).

If yes -> g has weight 3 with double zero at tau_Q,
   W^Q = g / eta^12 has weight -3 with structural double zero at tau_Q. (A) PROVED.

We use multiplicativity for ALL n up to N_MAX, including filling missing a_p.
"""

import mpmath as mp
mp.mp.dps = 50

# Kronecker symbol
def kronecker(a, b):
    if b == 0:
        return 1 if abs(a) == 1 else 0
    if b < 0:
        b = -b
        s = -1 if a < 0 else 1
    else:
        s = 1
    while b % 2 == 0:
        b //= 2
        if a % 2 == 0:
            return 0
        if a % 8 in (3, 5):
            s = -s
    a = a % b
    while a != 0:
        while a % 2 == 0:
            a //= 2
            if b % 8 in (3, 5):
                s = -s
        a, b = b, a
        if a % 4 == 3 and b % 4 == 3:
            s = -s
        a = a % b
    return s if b == 1 else 0


def chi(n):
    return kronecker(-22, n)


# Now compute a_p for ALL primes p up to N_MAX directly from CM Hecke theta-series formula:
#   For CM newform with CM field K, weight k, nebentypus chi_{D_K}:
#     - If p inert in K (i.e. (D_K/p) = -1): a_p = 0
#     - If p split or ramified: a_p = lambda(p) + chi(p) * conjugate(lambda(p)) * ?
#       Actually for weight-k CM form by K, with grossencharacter psi of "type" (k-1, 0):
#         a_p = psi(p_1) + psi(p_2)  where p O_K = p_1 p_2 (split case)
#         psi has the property |psi(p_i)|^2 = N(p_i)^{k-1} = p^{k-1}
#         For weight 3, |psi(p)|^2 = p^2.
#         So a_p = psi(p_1) + bar psi(p_1) = 2 Re psi(p_1).
#         AND psi(p_1) is an integer in O_K (some Hecke character).
#
# We have a_p for p in {2, 3, 5, 7, 11, 13, 17, 19} from LMFDB seed.
# Need a_p for p in {23, 29, 31, 37, 41, 43, 47, ...} for a_n up to ~50.
#
# Method: from LMFDB query, get more a_p values. Let me look it up via WebFetch.

# For now: derive a_p for split p from PRINCIPAL FORM REPRESENTATIONS.
# K = Q(sqrt -22), O_K = Z[sqrt -22], h(-88) = 2.
# For split primes p: there are alpha = a + b sqrt(-22) with N(alpha) = a^2 + 22 b^2 = p (using form (1,0,22))
# OR 2 a^2 + 11 b^2 = p (using form (2, 0, 11)).
# For weight-3 CM form with character chi, the eigenvalue a_p = 2 a (when p is represented by
# principal form (1, 0, 22) as a^2 + 22 b^2 = p) and a_p = some linear in (alpha) for non-principal.
#
# Specifically: psi(p_1) = alpha = a + b sqrt(-22) where a^2 + 22 b^2 = p (principal form).
# Then a_p = psi(p_1) + bar psi(p_1) = 2a.
# For non-principal split (2 a^2 + 11 b^2 = p), psi differs by class group character.
# The TWO newforms 88.3.b.a and 88.3.b.b correspond to the two Hecke characters extending chi.

# Let me find a_23 via quadratic forms:
# 23 = 1^2 + 22 * 1^2 = 1 + 22 = 23 ✓ (principal, with a=1, b=1)
# So for 88.3.b.* :  a_23 = +/- 2*1 = +/- 2.
# Sign depends on which CM form (a or b).

# Generic: for prime p represented by principal form (1, 0, 22) as p = a^2 + 22 b^2 with a > 0,
#  (the a > 0 convention), then a_p (one form) = 2a, a_p (other form) = -2a.
# For prime p represented by NON-principal form (2, 0, 11) as p = 2 a^2 + 11 b^2,
#  a_p = (something involving 2a) for one form, opposite for the other.

# Let me compute systematically.

def find_repr_principal(p):
    """If p = a^2 + 22 b^2, return (a, b). Else None."""
    for b in range(int((mp.mpf(p)/22)**(0.5)) + 1):
        a2 = p - 22 * b * b
        if a2 < 0:
            break
        a = int(round(mp.mpf(a2)**(mp.mpf(1)/2)))
        if a * a == a2:
            return (a, b)
    return None


def find_repr_nonprincipal(p):
    """If p = 2 a^2 + 11 b^2, return (a, b). Else None."""
    for b in range(int((mp.mpf(p)/11)**(0.5)) + 1):
        rem = p - 11 * b * b
        if rem < 0:
            break
        if rem % 2 != 0:
            continue
        a2 = rem // 2
        a = int(round(mp.mpf(a2)**(mp.mpf(1)/2)))
        if a * a == a2:
            return (a, b)
    return None


# Test:
print("Principal (1,0,22) representations p = a^2 + 22 b^2:")
for p in [3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97]:
    rp = find_repr_principal(p)
    nrp = find_repr_nonprincipal(p)
    chi_p = chi(p)
    print(f"  p={p:3d}, chi={chi_p:+2d}: principal {rp}, nonprincipal {nrp}")
print()

# So for each split p (chi(p)=+1), it's represented uniquely by one of the two forms
# (forms (1,0,22) and (2,0,11) with class group reps).

# Conjecture: a_p for 88.3.b.a = +2*a if p = a^2 + 22 b^2 (principal, a>0)
#                              = -2*a if p = 2 a^2 + 11 b^2 (nonprincipal, a>0)
# For 88.3.b.b: opposite sign or differing by chi_class_group character (of order 2).

# LMFDB seed: a_p for p=2,3,5,7,11,13,17,19 (88.3.b.a):
#   p=2 (ramified): a_2 = -2 (88.3.b.a)
#   p=3 (chi=-1): a_3 = 0
#   p=5 (chi=-1): a_5 = 0
#   p=7 (chi=-1): a_7 = 0
#   p=11 (ramified): a_11 = 11
#   p=13 (chi=+1): a_13 = 18 (=2*9), and 13 = ? Let's check: principal? 13 = 1+22? no. nonprincipal? 13 = 2*1 + 11 = 13 ✓ (a=1,b=1). So 13 is represented by nonprincipal as 2*1^2 + 11*1^2.
#     CONJECTURE FAILS: a_13 = 18, not -2. Coefficient is 18 = 2*9 = 2*9.
#     Look at primary decomposition with weight 3: a_p = 2 Re(alpha) with N(alpha) = 13.
#     But 13 is represented by 2 a^2 + 11 b^2 with (a,b) = (1, 1) -> N = 13. The element is
#     not in O_K = Z[sqrt -22] but in the FRACTIONAL ideal (2, sqrt(-22)) with norm 2.
#     Specifically the ideal (sqrt -22 + alpha) where alpha satisfies 2 alpha^2 + 11 b^2 = 13.

# Re-think: the Hecke eigenvalue a_p for weight-3 CM form is GENERATED by some psi(p_1) for
# split p, where psi : ideals -> C, |psi(I)|^2 = N(I)^2.
# The ELEMENT psi(p_1) is an algebraic integer in K satisfying |psi(p_1)|^2 = p^2 (when p_1 is split).
# For principal split p = alpha alpha_bar with alpha = a + b sqrt(-22):
#   psi(p_1) = alpha^? ... actually in the "principal" Hecke character of weight (k-1, 0) = (2, 0),
#   psi(p_1) = alpha^2  (that's the natural choice giving the right weight).
# Then a_p = alpha^2 + bar alpha^2 = (alpha + bar alpha)^2 - 2 alpha bar alpha = (2a)^2 - 2 p = 4a^2 - 2p.
# For p = 23 = 1 + 22: a_23 = 4*1 - 2*23 = 4 - 46 = -42.
# Check structure: |psi|^2 = |alpha^2|^2 = N(alpha)^2 = p^2. ✓
#
# For p = 13 = 2*1^2 + 11*1^2 (nonprincipal): the prime ideal is non-principal. We need its
# square is principal (since h=2 -> p_1^2 is principal).
# Specifically, p_1^2 = (alpha^2) = (some element of O_K).
# alpha for nonprincipal "ideal" associated to (2 a^2 + 11 b^2 = 13) representation:
#   the ideal class generator is gamma = sqrt(-22)/2 + 1/2 ? No, we need integral generator
#   of (2, sqrt(-22)) since 2 = (sqrt(-22))^2 / -11 ... messy.
# Alternative: in O_K = Z[sqrt -22]:
#   p = 13 split: 13 O_K = p_1 p_2 with p_1 = (13, ...) for some integer u with u^2 ≡ -22 mod 13.
#   u^2 ≡ -22 ≡ 4 (mod 13), so u = ±2.  p_1 = (13, 2 + sqrt -22).  N(p_1) = 13.
#   p_1 not principal (13 != a^2 + 22 b^2 for any (a,b)).
#   p_1^2 = ?  Norm 13^2 = 169.
#   Try alpha = 9 + 2 sqrt(-22):  N(alpha) = 81 + 88 = 169.  So alpha = 9 + 2 sqrt -22 has N = 169.
#   And alpha generates p_1^2 (since p_1^2 has norm 169 and is principal -- by h=2).
#
# Then psi(p_1)^2 = psi(p_1^2) = alpha = 9 + 2 sqrt -22 (up to unit/sign).
# psi(p_1) = sqrt(alpha) = sqrt(9 + 2 sqrt -22) -- not in K -- so this isn't quite right.
# Subtle: psi is a Hecke character on IDEALS, of weight (k-1, 0) = (2, 0).
# For p_1 non-principal, psi(p_1) isn't an element of K but a complex number with |psi|^2 = p^2.
# psi(p_1)^2 = psi(p_1^2) = generator of p_1^2 = alpha = 9 + 2 sqrt -22.
# So psi(p_1) = ± sqrt(alpha) where sqrt is in C.
# alpha = 9 + 2 sqrt(-22) has |alpha| = sqrt(81 + 88) = sqrt(169) = 13.
# arg(alpha) = arctan(2 sqrt 22 / 9) -- some angle.
# psi(p_1) = sqrt(13) * exp(i arg/2).
# a_p = psi(p_1) + psi(p_2) = psi(p_1) + bar psi(p_1) = 2 Re psi(p_1) = 2 sqrt 13 cos(arg/2)
# This depends on which sqrt we pick, but typically lands on a small integer.
# 2 Re sqrt(9 + 2 sqrt -22 i) where sqrt -22 = sqrt 22 i.
# alpha = 9 + 2 sqrt 22 i. To take sqrt:
#   sqrt(alpha) = (1/sqrt 2) * sqrt(|alpha| + Re alpha) + i * sign(Im alpha) * sqrt(|alpha| - Re alpha) * (1/sqrt 2)
#   = (1/sqrt 2) * sqrt(13 + 9) + i * sqrt(13 - 9) / sqrt 2 = sqrt 22 / sqrt 2 + i * 2 / sqrt 2
#   = sqrt 11 + i sqrt 2
# So psi(p_1) = sqrt 11 + i sqrt 2 (one choice).
# a_p = 2 Re psi(p_1) = 2 sqrt 11.  But LMFDB gives a_13 = 18 (rational integer).
# Hmm, sqrt 11 is irrational. Doesn't match.
#
# WAIT: LMFDB reports rational integer a_p. So 88.3.b.a has rational coefficients.
# So a_p is integer. 18 = 2 * 9 is integer.
#
# Then alpha (generator of p_1^2 in O_K) with the Hecke relation a_p = (alpha + bar alpha) something...
# Hmm, perhaps:
#   psi(p_1) is defined ON IDEALS only; psi(p_1)^2 = psi(p_1^2) but psi(p_1) is defined up to
#   a class group character. For h=2, there's a sign ambiguity.
#   psi(p_1) = +/- sqrt(alpha)
#   a_p = psi(p_1) + psi(bar p_1) = +/- (sqrt alpha + sqrt bar alpha) where the signs are
#   correlated by the chosen Hecke character extension.
#
# Note: 88.3.b.a vs 88.3.b.b is the choice of class group character.
# So a_p (88.3.b.a) and a_p (88.3.b.b) for non-principal p differ by a sign.
#
# HMMMM but BOTH have a_13 = 18 of the same sign! Let me re-check LMFDB:
# 88.3.b.a: 1, -2, 0, 4, 0, 0, 0, -8, 9, 0, 11, 0, 18, ... (positive 18)
# 88.3.b.b: 1, 2, 0, 4, 0, 0, 0, 8, 9, 0, -11, 0, -18, ... (negative 18!)
# Yes a_13 differs by sign across forms. OK.
#
# But 18 != 2 sqrt 11. Maybe the Hecke character is different.
#
# Let me try: a_13 = 18 as a sum of two algebraic integers in O_K.
# Need beta in O_K with N(beta) = 13^2 = 169 and tr(beta) = 18.
# beta = x + y sqrt(-22) with N = x^2 + 22 y^2 = 169 and tr = 2x = 18, so x = 9.
# Then 81 + 22 y^2 = 169 -> y^2 = 4 -> y = +/- 2.
# beta = 9 + 2 sqrt(-22).
# N(beta) = 169 = 13^2 ✓.  tr(beta) = 18 ✓.
# So the Hecke character generates p_1^2 by beta = 9 + 2 sqrt(-22).
# AND psi(p_1) is NOT sqrt(beta) (which would be irrational); rather:
# psi(p_1) is the "type-(2,0)" character, normalized so:
#   psi(p_1)^2 = beta * (unit factor)  or
#   psi is defined directly on IDEALS without taking square root.
#
# In MORE PRECISE TERMS: for weight-k CM form by K, the Hecke character psi satisfies
#   psi((alpha)) = alpha^(k-1)  for principal alpha  (ignoring infinite type)
# And on a non-principal ideal p, psi(p) is defined to be SOME (k-1)-th power of a generator
# of p, but since p is non-principal, this ISN'T well-defined and we need a class field theory
# argument to fill in.
#
# Simpler approach: for weight 3, the relation is
#   a_p = alpha + bar alpha  where alpha + bar alpha = tr(beta) = 2*Re(beta) for beta = a generator
#   of p^something with norm p^(k-1) = p^2.
#
# In our case for non-principal p of norm 13: p^2 is principal generated by beta = 9 + 2 sqrt(-22).
# The Hecke relation gives a_p = trace of square-root-like-thing.
# Empirically, the "psi(p)" for non-principal p has psi(p)^2 = beta, and psi(p) is well-defined
# in O_K up to a sign coming from the class group. So
#   psi(p) = +/- (3 + sqrt(-22)) / something... no wait, sqrt(beta) needs solving x^2 = 9 + 2 sqrt -22.
#   In K: solve x = u + v sqrt -22 with x^2 = 9 + 2 sqrt -22.
#   x^2 = u^2 - 22 v^2 + 2 u v sqrt -22 = 9 + 2 sqrt -22.
#   Equations: u^2 - 22 v^2 = 9, 2 u v = 2, so u v = 1, v = 1/u.
#   u^2 - 22/u^2 = 9 -> u^4 - 9 u^2 - 22 = 0.
#   u^2 = (9 +/- sqrt(81 + 88))/2 = (9 +/- 13)/2 = 11 or -2.
#   u^2 = 11 (positive) -> u = sqrt 11 IRRATIONAL.  So sqrt beta is NOT in K.
#
# OK so psi(p) NOT in K either. But a_p = psi(p) + psi(bar p) = 2 Re psi(p).
# psi(p) is in C with psi(p)^2 = beta = 9 + 2 sqrt -22 = 9 + 2 sqrt 22 i.
# |psi(p)|^2 = |beta| = 13. So |psi(p)| = sqrt 13.
# psi(p) = sqrt 13 * exp(i theta) with 2 theta = arg(beta) = arctan(2 sqrt 22 / 9).
# 2 Re psi(p) = 2 sqrt 13 cos(theta) = 2 sqrt 13 * sqrt((1+cos 2 theta)/2)
#             = 2 sqrt 13 * sqrt((1 + 9/13)/2) = 2 sqrt 13 * sqrt(11/13) = 2 sqrt 11.
#
# So a_13 PREDICTS 2 sqrt 11 ≈ 6.633. But LMFDB says a_13 = 18. CONTRADICTION.

# So my understanding is wrong. Let me reconsider.

# Maybe a_13 = 18 is NOT a CM relation for p=13 split, but for p=13 inert?
# Check: chi(13) = (-22/13).
# (-22/13) = (-22 mod 13 / 13) = (4/13) (using 22 mod 13 = 9, so -22 mod 13 = -9 = 4).
# (4/13) = 1 (4 is a QR mod 13).
# So chi(13) = +1 -> 13 SPLIT, my analysis above applies.

# But a_13 = 18 doesn't match. Maybe weight conventions or different Hecke theta.

# RESOLUTION: I think the right formula for weight-k CM form is
#   psi : I_K -> C* such that psi((alpha)) = alpha^(k-1) for PRINCIPAL ideals (alpha).
# This means psi on principal ideals is psi((alpha)) = alpha^(k-1), and a_p for SPLIT principal p:
#   p = N(alpha), with alpha = a + b sqrt(-22), p = a^2 + 22 b^2.
#   Then p_1 = (alpha) is principal, psi(p_1) = alpha^(k-1) = alpha^2 = (a + b sqrt -22)^2.
#   Re alpha^2 = a^2 - 22 b^2.
#   a_p = 2 Re alpha^2 = 2 (a^2 - 22 b^2) = 2 a^2 - 44 b^2 + sign?
#
# Test p = 23 = 1 + 22: a = 1, b = 1. a_p = 2*(1 - 22) = -42.
# Hmm LMFDB doesn't show a_23 in our seed (need to check).
#
# Test p = 47 = 25 + 22 = 5^2 + 22 -> a=5, b=1. a_p = 2*(25 - 22) = 6.
# LMFDB doesn't show a_47.
#
# For non-principal p (h=2 case): p_1 NOT principal, but p_1^2 = (beta) principal.
# psi(p_1)^2 = psi(p_1^2) = beta^(k-1) = beta^2. So psi(p_1) = +/- beta.
# a_p = +/- beta + bar beta = +/- 2 Re beta = +/- 2x where beta = x + y sqrt -22.
#
# For p = 13, beta = 9 + 2 sqrt(-22), so a_p = +/- 2*9 = +/- 18.
#
# YES MATCHES! a_13 = 18 for 88.3.b.a, a_13 = -18 for 88.3.b.b. ✓
#
# Note: psi(p_1)^2 = beta means psi(p_1) = sqrt(beta) -- but if sqrt(beta) is NOT in K, we get a
# COMPLEX (non-rational) coefficient. HOWEVER, in this specific case beta IS in O_K and beta^2
# is also in O_K with N(beta^2) = N(p_1^4) = p^4 = 28561.
# Hmm wait. Let me recompute. psi(p_1)^2 = psi(p_1^2). psi(p_1^2) = beta^? Let me re-examine.
#
# Type-(k-1, 0) Hecke character: psi((alpha)) = alpha^(k-1) for PRINCIPAL alpha.
# weight k=3 -> k-1 = 2.
# So psi((alpha)) = alpha^2 for principal (alpha).
#
# For non-principal p_1 with p_1^2 = (beta) principal:
#   psi(p_1^2) = psi((beta)) = beta^2.
#   psi(p_1)^2 = psi(p_1^2) = beta^2.
#   So psi(p_1) = +/- beta.  (the ambiguity is the class group character)
#
# a_p = psi(p_1) + psi(bar p_1) where bar p_1 = p_2.
# psi(p_2) = psi(bar p_1) = bar psi(p_1) (by conjugation property).
# psi(p_1) = +/- beta = +/- (9 + 2 sqrt -22).
# a_p = +/- 2 Re beta = +/- 18.   MATCHES!!! ✓✓✓

# So the formula is:
# For split principal p = a^2 + 22 b^2:
#   alpha = a + b sqrt(-22) (in O_K), p_1 = (alpha).
#   psi(p_1) = alpha^2 = (a^2 - 22 b^2) + 2ab sqrt(-22).
#   a_p = 2 Re alpha^2 = 2 (a^2 - 22 b^2).
# For split non-principal p (then p = 2 a^2 + 11 b^2 in form (2,0,11)):
#   p_1 generates ideal class with p_1^2 principal. Find beta in O_K with N(beta) = p^2 and
#   beta = x + y sqrt(-22) with x = +/-(a^2 - 22 b^2)/something... actually we need beta s.t.
#   p_1^2 = (beta) ...
#   For p = 13 = 2*1+11*1 (non-principal): beta = 9 + 2 sqrt -22 with N = 81+88 = 169 = 13^2 ✓
#   For p = 17 = ? Check: 17 = a^2 + 22 b^2: a=?  17 < 22 so b=0 gives a^2 = 17, NO.
#                       17 = 2 a^2 + 11 b^2: b=1 -> 2 a^2 = 6 -> a^2 = 3 NO. b=0 -> a^2 = 17/2 NO. INERT?
#   chi(17) = ? 17 mod 11 = 6, (-22/17) = (-22 mod 17/17) = (-5/17) = (12/17) = (3/17)(4/17) = (3/17).
#   (3/17) by QR: (3/17)(17/3) = (-1)^((3-1)/2*(17-1)/2) = (-1)^(1*8) = 1. (17/3) = (2/3) = -1.
#   So (3/17) = -1. chi(17) = -1, INERT, a_17 = 0. ✓
#
# For non-principal split p, we need beta in O_K with N(beta) = p^2 and beta = "generator of p_1^2".
# This beta is unique up to multiplication by a unit (of which O_K^* = {+/-1} for K imag quad with D < -4).
#
# Let me code: for each prime p with chi(p) = +1 and p NOT principally represented,
# find beta = x + y sqrt(-22) with x^2 + 22 y^2 = p^2 and (x + y sqrt(-22)) generates ideal that
# is THE square of the non-principal prime above p.
# Pragmatic: enumerate all (x, y) with x^2 + 22 y^2 = p^2 and tr = 2x.
# Constraint: beta should not be N(alpha) for principal alpha. I.e., we want beta NOT in (O_K)^2 essentially.

def find_beta_for_p2(p):
    """Find x, y >= 0 with x^2 + 22 y^2 = p^2 and (x, y) not from a principal split rep."""
    candidates = []
    for y in range(int((mp.mpf(p)/mp.mpf(22))**(0.5)) + 2):
        x2 = p*p - 22 * y * y
        if x2 < 0:
            break
        x = int(round(mp.mpf(x2)**(mp.mpf(1)/2)))
        if x*x == x2 and x > 0 and y > 0:
            candidates.append((x, y))
    # If p = a^2 + 22 b^2 (principal split), then alpha^2 = (a + b sqrt -22)^2 = (a^2 - 22b^2) + 2ab sqrt -22.
    # So one candidate (x, y) = (a^2 - 22 b^2, 2ab) -- principal psi value.
    # Others are non-principal beta.
    rp = find_repr_principal_v2(p)
    if rp:
        a, b = rp
        x_principal = abs(a*a - 22 * b * b)
        y_principal = 2 * abs(a) * abs(b)
        candidates_filtered = [c for c in candidates if c != (x_principal, y_principal)]
    else:
        candidates_filtered = candidates
    return candidates_filtered


def find_repr_principal_v2(p):
    for b in range(int((mp.mpf(p)/22)**(0.5)) + 2):
        a2 = p - 22 * b * b
        if a2 < 0:
            break
        a = int(round(mp.mpf(a2)**(mp.mpf(1)/2)))
        if a*a == a2 and a >= 0:
            return (a, b)
    return None


def predict_ap(p):
    """Predict a_p for 88.3.b.a using CM formula. Returns +/- value (sign is convention)."""
    if p == 2 or p == 11:
        # Ramified primes; use empirical value.
        return None
    chi_p = chi(p)
    if chi_p == -1:
        return 0  # inert
    # Split: try principal first
    rp = find_repr_principal_v2(p)
    if rp:
        a, b = rp
        # a_p = 2 (a^2 - 22 b^2)
        return 2 * (a*a - 22 * b * b)
    # Non-principal split: find beta
    candidates = find_beta_for_p2(p)
    if candidates:
        # Take smallest x (canonical?)
        x, y = candidates[0]
        return 2 * x  # sign convention positive
    return None


print("CM-predicted a_p (88.3.b.a) vs LMFDB:")
seed_a = {2: -2, 3: 0, 5: 0, 7: 0, 11: 11, 13: 18, 17: 0, 19: 6}
for p in [3, 5, 7, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103]:
    pred = predict_ap(p)
    chi_p = chi(p)
    lmfdb = seed_a.get(p, '?')
    rp = find_repr_principal_v2(p)
    nrp = find_repr_nonprincipal(p) if rp is None else None
    note = ''
    if rp:
        note = f"principal {rp}"
    elif nrp:
        note = f"non-principal {nrp}"
    print(f"  p={p:3d}, chi={chi_p:+2d}: predicted a_p = {pred}, LMFDB = {lmfdb}  ({note})")

print()
print("If predictions match LMFDB, we have full a_p formula -> can compute a_n for all n.")
print()


# Note: I had find_repr_nonprincipal using non-principal form (2,0,11), but for SPLIT non-principal p,
# the right thing is finding beta with N=p^2.
# Let me look for sign conventions: 88.3.b.a might use +sign convention for principal, and -sign for non-principal.
# a_19 = 6 and 19 = ? Principal: 19 = a^2 + 22 b^2? a^2 = 19 NO. b=1 -> a^2 = -3 NO. NOT principal.
#        Non-principal: 19 = 2 a^2 + 11 b^2? b=1 -> 2a^2 = 8 -> a^2 = 4 -> a = 2 ✓. So 19 = 2*4 + 11.
# Predict a_19 via beta of norm 19^2 = 361:
#  361 = x^2 + 22 y^2. Try y=0 -> x = 19. (19, 0). principal? 19 = (sqrt 19)^2 from (19, 0)? No, we need
#  alpha = 19 (rational); then alpha^2 = 361 = (19, 0) in (x, y) coords, but psi for this would correspond
#  to p split principal... but 19 is NOT principal split.
#
#  Other beta's: y=1 -> x^2 = 339 NO. y=2 -> x^2 = 273 NO. y=3 -> x^2 = 163 NO. y=4 -> x^2 = 9 -> x=3. (3, 4).
#   3^2 + 22*16 = 9 + 352 = 361 ✓.
#  So beta = 3 + 4 sqrt -22. a_19 = 2*3 = 6 ✓✓✓.
#
# Now for p=19 nonprincipal, predict_ap should pick (3, 4) not (19, 0). My code picks first candidate.
# Let me re-examine: find_beta_for_p2(19) returns candidates with x>0 and y>0, so (19, 0) would be excluded
# (y=0 not >0). Good, candidates = [(3, 4)]. predict_ap = 2*3 = 6. ✓ matches!

# Similarly for p=13: candidates with y>0 starts at y=1, x^2 = 169 - 22 = 147 NO. y=2 -> x^2 = 169-88 = 81 -> x=9.
#   (9, 2). a_p = 2*9 = 18 ✓.

# So my predictor works for 88.3.b.a.
