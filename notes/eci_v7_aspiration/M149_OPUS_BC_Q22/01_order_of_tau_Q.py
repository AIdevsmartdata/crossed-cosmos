"""
M149 sub-task 3 — identify the order O_tau_Q for tau_Q = i*sqrt(11/2).

CMR 2005 (math/0501424) Definition 4.1: A K-lattice for K imaginary quadratic
with O its ring of integers requires Lambda subset C, finitely generated O-module,
Lambda ⊗_O K ≅ K. The choice of tau in the construction (4.5) requires
O = Z + Z*tau (i.e. tau is an algebraic integer such that {1, tau} is a Z-basis
of the maximal order O_K).

For K = Q(sqrt(-22)), we have d = -22 ≡ 2 (mod 4), so disc(K) = -88, and
the maximal order is O_K = Z[sqrt(-22)] with Z-basis {1, sqrt(-22)}.

For tau_Q = i*sqrt(11/2) = i*sqrt(22)/2 = sqrt(-22)/2:
   Z + Z*tau_Q = Z + Z*(sqrt(-22)/2)
   tau_Q^2 = -11/2 ∉ Z

So Z + Z*tau_Q is NOT a ring (closure under multiplication fails).
Therefore tau_Q is NOT directly the standard CMR-CM tau ∈ H with O = Z + Z*tau.

The reduced form (a,b,c) = (2,0,11) of disc -88 gives tau = sqrt(-88)/4
= i*sqrt(88)/4 = 2i*sqrt(22)/4 = i*sqrt(22)/2 = tau_Q. CORRECT.

The lattice Lambda_(2,0,11) = Z + Z*tau_Q (NOT a ring, just a Z-module / lattice).
Its O_K-action: O_K = Z[sqrt(-22)] acts on Lambda? Let's check.
sqrt(-22) * tau_Q = sqrt(-22) * sqrt(-22)/2 = -22/2 = -11 ∈ Z ⊂ Lambda. CHECK.
sqrt(-22) * 1 = sqrt(-22) = 2*tau_Q ∈ Lambda. CHECK.
So Lambda IS an O_K-module. It is the ideal a = (2, sqrt(-22))? Let's check.

The ideal (2, sqrt(-22)) in O_K = Z[sqrt(-22)]:
   = {2a + sqrt(-22)*b : a, b ∈ Z[sqrt(-22)]}
   = {2(a_1 + a_2*sqrt(-22)) + sqrt(-22)(b_1 + b_2*sqrt(-22)) : a_i, b_i ∈ Z}
   = {(2*a_1 - 22*b_2) + sqrt(-22)*(2*a_2 + b_1) : a_i, b_i ∈ Z}
   = {even integer + sqrt(-22)*(any integer)}
   = 2*Z + sqrt(-22)*Z

This is a Z-module of index 2 in O_K. As a fractional ideal divided by... let's
match it to Lambda = Z + Z*tau_Q = Z + Z*(sqrt(-22)/2):
   Z + Z*(sqrt(-22)/2) = (1/2) * (2*Z + sqrt(-22)*Z) = (1/2) * (2, sqrt(-22))_O

So Lambda = (1/2) * a, where a = (2, sqrt(-22)) is a non-principal ideal of O_K.
The class [a] ∈ Cl(O_K) is the non-trivial class (Cl(O_K) = Z/2).

Verification: a^2 = (2, sqrt(-22))^2 = (4, 2*sqrt(-22), -22) = (4, 22, 2*sqrt(-22))
            = 2*(2, 11, sqrt(-22)) = 2*(2, sqrt(-22), 1) [since 11 = (sqrt(-22))^2/(-2)... no]
GCD(4, 22) = 2 → a^2 = 2*(2, 11, sqrt(-22)) = 2*(1) = (2) since gcd(2,11) = 1.
So a^2 = (2), hence a is non-principal of order 2 in Cl(O_K).
"""
import sympy as sp
from sympy import sqrt, I, Rational, simplify, S, symbols, Matrix

# Setup
sqrt_m22 = sp.sqrt(-22)
tau_Q = sqrt_m22 / 2     # = i*sqrt(22)/2 = i*sqrt(11/2)
print(f"tau_Q = {tau_Q} = {sp.simplify(tau_Q)}")
print(f"      = i*sqrt(11/2) = {sp.simplify(I*sp.sqrt(Rational(11,2)))}")
print(f"  numerical: {complex(tau_Q.evalf(30))}")

# Check tau_Q^2
tQ2 = sp.expand(tau_Q**2)
print(f"\ntau_Q^2 = {tQ2}")
print(f"  ∈ Z? {tQ2.is_integer}")  # No, = -11/2

# So Z + Z*tau_Q is NOT a ring - because Z + Z*tau_Q closed under multiplication
# would require tau_Q^2 = a + b*tau_Q for some a,b ∈ Z.
# But tau_Q^2 = -11/2, so we'd need a = -11/2 ∉ Z. CONFIRMED NOT A RING.

# Identify the ideal class
print("\n" + "="*68)
print("Step 2: Lambda = Z + Z*tau_Q as O_K-module (O_K = Z[sqrt(-22)])")
print("="*68)

# O_K action: alpha = sqrt(-22), check alpha*1 and alpha*tau_Q in Lambda
alpha = sqrt_m22
v1 = sp.expand(alpha * 1)             # = sqrt(-22)
v2 = sp.expand(alpha * tau_Q)         # = -11

# Express v1 in basis {1, tau_Q}: 1*0 + tau_Q*?
# sqrt(-22) = 0 + tau_Q * (sqrt(-22)/tau_Q) = 0 + tau_Q * 2 (since tau_Q = sqrt(-22)/2)
v1_in_basis = sp.simplify(v1 / tau_Q)  # = 2
print(f"  alpha * 1 = sqrt(-22) = 0*1 + {v1_in_basis}*tau_Q")
v2_in_basis = sp.simplify(v2)
print(f"  alpha * tau_Q = -11 = {v2_in_basis}*1 + 0*tau_Q")
print("  Both coefficients integer => Lambda is O_K-module ✓")

# Lambda as fractional ideal
print("\n" + "="*68)
print("Step 3: Lambda = (1/2) * (2, sqrt(-22)) as fractional ideal of O_K")
print("="*68)
# Lambda = Z + Z*(sqrt(-22)/2) = (1/2)*(2*Z + sqrt(-22)*Z)
# Now (2, sqrt(-22)) in O_K = {2*a + sqrt(-22)*b : a,b ∈ O_K}
#   = 2*Z + sqrt(-22)*Z  (verified above in docstring)

# Check: ideal a = (2, sqrt(-22)). Norm: N(a) = 2 (since gcd(N(2), N(sqrt(-22))) = gcd(4, 22) = 2)
# More precisely, [O_K : a] = 2.
# a^2 = (4, 2*sqrt(-22), -22). Now (4, -22) = (gcd(4,22)) = (2). And 2*sqrt(-22) ∈ (2).
# So a^2 = (2). Hence [a]^2 = [1] in Cl(O_K). Since a is non-principal (otherwise
# 2 = N(a) would equal a norm, but no element x+y*sqrt(-22) has x^2+22*y^2 = 2),
# [a] is the non-trivial class of order 2.

# Verify no element has norm 2
print("Check no element of Z[sqrt(-22)] has norm 2 (a non-principal):")
for x in range(-3, 4):
    for y in range(-3, 4):
        n = x*x + 22*y*y
        if n == 2:
            print(f"  FOUND: x={x}, y={y}: norm = {n}")
            break
else:
    print("  NO element has norm 2 (since min nonzero norm 22*y^2 for y!=0 is 22)")
    print("  ⇒ ideal a = (2, sqrt(-22)) is NON-PRINCIPAL")
    print("  ⇒ [a] is the non-trivial class of Cl(O_K) ≅ Z/2")

# So Lambda corresponds to the NON-PRINCIPAL class. The principal class
# would be the lattice Z + Z*sqrt(-22) = O_K, which is Z + Z*tau_principal
# where tau_principal = sqrt(-22) = i*sqrt(22) ≈ 4.690i.

print("\n" + "="*68)
print("Step 4: The two CM points of disc -88 (h_K = 2 representatives)")
print("="*68)
tau_principal = sqrt_m22
tau_nonprincipal = sqrt_m22 / 2
print(f"  Principal class: tau_1 = sqrt(-22) = {complex(tau_principal.evalf(30))}")
print(f"    Lattice Lambda_1 = O_K = Z + Z*sqrt(-22)  (the maximal order itself)")
print(f"    Im(tau_1) = sqrt(22) ≈ {float(sp.sqrt(22)):.6f}")
print(f"  Non-principal class: tau_2 = sqrt(-22)/2 = {complex(tau_nonprincipal.evalf(30))}")
print(f"    Lattice Lambda_2 = (1/2)*(2, sqrt(-22))  ⊂ K")
print(f"    Im(tau_2) = sqrt(22)/2 = sqrt(11/2) ≈ {float(sp.sqrt(Rational(11,2))):.6f}")
print()
print("ECI quark modulus tau_Q = i*sqrt(11/2) corresponds to the NON-PRINCIPAL CLASS.")
print()
print("Important: in CMR Eq (4.5), the embedding q_tau is defined for tau such")
print("that O = Z + Z*tau. For our K = Q(sqrt(-22)) this is tau = sqrt(-22) (principal).")
print("For the non-principal tau_Q, we need a generalization: q_{tau_Q}(K^*) = ?")
