"""
M149 sub-task 3-4: Construct q_tau embeddings K* -> GL_2^+(Q) for K = Q(sqrt(-22))
and test fixed-point property.

CMR 2005 (math/0501424) Eq (4.5)-(4.6): For O = Z + Z*tau the maximal order,
  q_tau: K ↪ M_2(Q),
  q_tau(K^*) = {g ∈ GL_2^+(Q): g(tau) = tau}        (4.6)

The embedding is determined by left multiplication on K = Q + Q*tau in basis {1, tau}.
For alpha = a + b*tau ∈ K with tau^2 = c_0 + c_1*tau (minimal polynomial coefficients):
  alpha * 1   = a + b*tau                    → column (a, b)
  alpha * tau = a*tau + b*tau^2
              = a*tau + b*(c_0 + c_1*tau)
              = b*c_0 + (a + b*c_1)*tau     → column (b*c_0, a + b*c_1)
So q_tau(a + b*tau) = [[a, b*c_0], [b, a + b*c_1]].

For K = Q(sqrt(-22)), maximal order O_K = Z[sqrt(-22)], tau_principal = sqrt(-22),
tau^2 = -22 = -22 + 0*tau, so c_0 = -22, c_1 = 0:
  q_principal(a + b*sqrt(-22)) = [[a, -22*b], [b, a]]

For tau_Q = sqrt(-22)/2 = tau_principal/2, this is NOT in the standard CMR setup
because Z + Z*tau_Q is NOT a ring. But the ideal Lambda_Q = Z + Z*tau_Q is still
an O_K-module. We can define q_{tau_Q} in two ways:

(I) "Naive" Mobius stabilizer: g ∈ GL_2^+(Q) such that g.tau_Q = tau_Q.
    Find {[[a,b],[c,d]]: (a*tau_Q + b)/(c*tau_Q + d) = tau_Q}.
    => a*tau_Q + b = c*tau_Q^2 + d*tau_Q = -11/2*c + d*tau_Q
    => coeffs: a = d, b = -11*c/2.
    With det = a*d - b*c = a^2 + 11*c^2/2 > 0 (for (a,c) != (0,0)).
    Stabilizer = {[[a, -11c/2], [c, a]] : (a,c) ∈ Q^2 \ {0}}.

    Compare q_principal(K^*) = {[[a, -22b], [b, a]]}. The stabilizer of
    tau_Q in GL_2^+(Q) is RELATED to that of tau_principal by the substitution
    b -> c/2 (so that -22*b = -11*c). So Stab(tau_Q) is the SAME GROUP, but
    parametrized by (a, c) with c = 2*b. We have:
       Stab(tau_Q) = q_principal(K^*) AS A SUBGROUP OF GL_2^+(Q)?
    Let's check: an element of Stab(tau_Q) has form [[a, -11c/2], [c, a]].
    Element of q_principal(K^*) has form [[a, -22b], [b, a]] for a,b ∈ Q.
    Comparing: c = b in 2nd row, but then 1st row has -11c/2 = -11b/2 vs -22b.
    These match only if -11b/2 = -22b, i.e. -11b/2 + 22b = 33b/2 = 0, i.e. b = 0.
    So q_principal(K^*) ∩ Stab(tau_Q) = scalars only.

    DIFFERENT GROUPS! Stab(tau_Q) is q_{tau_Q,naive}(K^*) where q_{tau_Q,naive}
    uses the basis (1, tau_Q) of Q-vector space K, but K = Q + Q*tau_Q since
    Q*tau_Q = Q*sqrt(-22). Both are Q + Q*sqrt(-22) = K. So as Q-vector space
    K = Q + Q*tau_Q with basis {1, tau_Q}. Multiplication of alpha = a + b*tau_Q
    (with a, b ∈ Q) on K:
      alpha * 1 = a + b*tau_Q     → (a, b)
      alpha * tau_Q = a*tau_Q + b*tau_Q^2 = -11b/2 + a*tau_Q  → (-11b/2, a)
    => q_{tau_Q,naive}(a + b*tau_Q) = [[a, -11b/2], [b, a]]

    BUT: the entries -11b/2 are not in Z if b is odd. So q_{tau_Q,naive}(O_K)
    does NOT land in M_2(Z): for alpha = sqrt(-22) = 2*tau_Q (so a=0, b=2),
    q_{tau_Q,naive}(sqrt(-22)) = [[0, -11], [2, 0]] which IS in M_2(Z).
    For alpha = 1 + sqrt(-22) = 1 + 2*tau_Q, q = [[1, -11], [2, 1]] ∈ M_2(Z) ✓.
    For alpha = tau_Q itself (which is NOT in O_K!), q = [[0, -11/2], [1, 0]].
    But tau_Q ∉ O_K, so this case is NOT physical.

(II) Honest CMR construction at non-principal CM point:
    Use the Q(τ)-isomorphism K → Lambda_Q ⊗ Q given by α ↦ α (multiplication
    on Lambda_Q via O_K). The matrix of multiplication-by-α on Lambda_Q
    in basis {1, tau_Q} computes q_{tau_Q}.

    For α = a + b*sqrt(-22) (with a,b ∈ Q so α ∈ K), and tau_Q = sqrt(-22)/2:
       α * 1 = a + b*sqrt(-22) = a + 2b*tau_Q       → (a, 2b)
       α * tau_Q = a*tau_Q + b*sqrt(-22)*tau_Q
                 = a*tau_Q + b*(-22)/2  [since sqrt(-22)*tau_Q = sqrt(-22)*sqrt(-22)/2 = -22/2]
                 = -11b + a*tau_Q       → (-11b, a)
    So q_{tau_Q}(a + b*sqrt(-22)) = [[a, -11b], [2b, a]]

    Now check: this matrix is in M_2(Q) and the Mobius action on tau_Q gives
    (a*tau_Q + (-11b))/((2b)*tau_Q + a) = (a*tau_Q - 11b)/(a + 2b*tau_Q).
    Multiply num and den by (a - 2b*tau_Q):
       num: (a*tau_Q - 11b)(a - 2b*tau_Q) = a^2*tau_Q - 2ab*tau_Q^2 - 11ab + 22b^2*tau_Q
          = a^2*tau_Q - 2ab*(-11/2) - 11ab + 22b^2*tau_Q
          = a^2*tau_Q + 11ab - 11ab + 22b^2*tau_Q
          = (a^2 + 22b^2)*tau_Q
       den: (a + 2b*tau_Q)(a - 2b*tau_Q) = a^2 - 4b^2*tau_Q^2 = a^2 - 4b^2*(-11/2) = a^2 + 22b^2
    => Mobius = (a^2 + 22b^2)*tau_Q / (a^2 + 22b^2) = tau_Q ✓

    GREAT — q_{tau_Q}(K^*) FIXES tau_Q as Mobius transformation.

NOW THE KEY POINT (M149): the matrices [[a, -11b], [2b, a]] for a,b ∈ Z
do NOT represent O_K ≅ Z[sqrt(-22)] (which is alpha = a + b*sqrt(-22) for a,b ∈ Z).
They represent multiplication on the IDEAL Lambda_Q = (1/2)(2, sqrt(-22)),
not on O_K.

The image q_{tau_Q}(O_K) in M_2(Q) consists of matrices:
   {[[a, -11b], [2b, a]] : a, b ∈ Z}
This is a Z-subring of M_2(Q) (closed under matrix multiplication), and
isomorphic to O_K = Z[sqrt(-22)]. It is the EMBEDDING that fixes tau_Q.

CONCLUSION: the embedding q_{tau_Q}: K^* -> GL_2^+(Q) DOES exist for the
non-principal CM point tau_Q = i*sqrt(11/2), but it is NOT the same as
q_{tau_principal}: it is RELATED by a conjugation by S = [[1, 0], [0, 2]]
or [[1, 0], [0, 1/2]] (passing from basis {1, tau_principal} to {1, tau_Q}).
"""
import sympy as sp
from sympy import sqrt, I, Matrix, symbols, simplify, expand, Rational, S

print("="*70)
print("M149 — q_tau embeddings for K = Q(sqrt(-22)), h_K = 2")
print("="*70)

a, b = symbols('a b', real=True)

# Setup
sqrt_m22 = sp.sqrt(-22)
tau_principal = sqrt_m22                  # primitive of O_K
tau_Q = sqrt_m22 / 2                       # non-principal CM point

print(f"\ntau_principal = sqrt(-22), tau_principal^2 = {sp.expand(tau_principal**2)}")
print(f"tau_Q          = sqrt(-22)/2, tau_Q^2          = {sp.expand(tau_Q**2)}")

# Mobius action helper
def mobius(M, tau):
    return (M[0,0]*tau + M[0,1]) / (M[1,0]*tau + M[1,1])

# CMR-standard q_principal: alpha = a + b*sqrt(-22), b=integer indices O_K
# Matrix [[a, -22*b], [b, a]]
q_principal = Matrix([[a, -22*b], [b, a]])
print("\n" + "-"*70)
print("(A) q_principal(K^*): standard CMR embedding for tau_principal = sqrt(-22)")
print(f"  q_principal(a + b*sqrt(-22)) = {q_principal.tolist()}")
print(f"  det = {sp.expand(q_principal.det())} = a^2 + 22*b^2 > 0 ✓")
print(f"  Mobius action on tau_principal: M.tau = {sp.simplify(mobius(q_principal, tau_principal))}")
diff_principal = sp.simplify(mobius(q_principal, tau_principal) - tau_principal)
print(f"  Verification: M.tau_principal - tau_principal = {diff_principal} (should be 0)")

# Now q_{tau_Q}: alpha = a + b*sqrt(-22), in basis {1, tau_Q} of Lambda_Q ⊗ Q
# Matrix [[a, -11*b], [2*b, a]]
q_tauQ = Matrix([[a, -11*b], [2*b, a]])
print("\n" + "-"*70)
print("(B) q_{tau_Q}(K^*): CMR embedding for tau_Q = sqrt(-22)/2 (non-principal)")
print(f"  q_{{tau_Q}}(a + b*sqrt(-22)) = {q_tauQ.tolist()}")
print(f"  det = {sp.expand(q_tauQ.det())} = a^2 + 22*b^2 > 0 ✓ (SAME as q_principal!)")
print(f"  Mobius action on tau_Q: M.tau = {sp.simplify(mobius(q_tauQ, tau_Q))}")
diff_Q = sp.simplify(mobius(q_tauQ, tau_Q) - tau_Q)
print(f"  Verification: M.tau_Q - tau_Q = {diff_Q} (should be 0)")

# Check the conjugation relation
print("\n" + "-"*70)
print("(C) Conjugation relation: q_{tau_Q} = S * q_principal * S^{-1}")
S_mat = Matrix([[1, 0], [0, Rational(1,2)]])
S_inv = S_mat.inv()
print(f"  S = {S_mat.tolist()}")
print(f"  S^-1 = {S_inv.tolist()}")
conjugate = S_mat * q_principal * S_inv
print(f"  S * q_principal * S^-1 = {sp.simplify(conjugate).tolist()}")
print(f"  Equal to q_tauQ? {sp.simplify(conjugate - q_tauQ) == sp.zeros(2,2)}")
# Other direction: S = diag(1, 1/2) sends tau_principal to (tau_principal)/2 = tau_Q
print(f"  S.tau_principal = (1*tau + 0)/(0 + (1/2)) = 2*tau? Let's check.")
print(f"    Using Mobius: (1*tau_principal + 0)/(0*tau_principal + 1/2) = 2*tau_principal = {complex((2*tau_principal).evalf(30))}")
print(f"    But tau_Q = tau_principal/2 = {complex(tau_Q.evalf(30))}")
print(f"    => S maps tau_principal -> 2*tau_principal, NOT tau_Q.")
print(f"    So we need S' = [[1,0],[0,2]] sending Mobius (tau)/2 = tau_principal*1/2.")
S_prime = Matrix([[1, 0], [0, 2]])
print(f"  S' = {S_prime.tolist()}")
print(f"    S'.tau_principal = tau_principal/2 = tau_Q? = {complex(mobius(S_prime, tau_principal).evalf(30))}")
print(f"  Conjugation S' * q_principal * (S')^-1 = {sp.simplify(S_prime * q_principal * S_prime.inv()).tolist()}")
# This should equal q_tauQ
print(f"  Compare q_tauQ = {q_tauQ.tolist()}")
diff_conj = sp.simplify(S_prime * q_principal * S_prime.inv() - q_tauQ)
print(f"  Difference: {diff_conj.tolist()} (should be zero)")

# IMPORTANT: q_tauQ is actually q_principal conjugated by g_Q ∈ GL_2^+(Q)
# such that g_Q.tau_principal = tau_Q. Specifically g_Q = [[1, 0], [0, 2]],
# which has det 2, sends tau_principal to tau_principal/2 = tau_Q.

print("\n" + "="*70)
print("(D) Numerical verification mpmath dps=30")
print("="*70)
import mpmath
mpmath.mp.dps = 30

tau_Q_num = mpmath.mpc(0, mpmath.sqrt(mpmath.mpf(11)/2))
print(f"  tau_Q numerical: {tau_Q_num}")

# Test on alpha = 3 + 2*sqrt(-22):  q_tauQ = [[3, -22], [4, 3]]
M_test = mpmath.matrix([[3, -22], [4, 3]])
res = (M_test[0,0]*tau_Q_num + M_test[0,1]) / (M_test[1,0]*tau_Q_num + M_test[1,1])
print(f"  alpha = 3 + 2*sqrt(-22), q_{{tau_Q}}(alpha) = [[3, -22], [4, 3]]")
print(f"  M.tau_Q = {res}")
print(f"  |M.tau_Q - tau_Q| = {abs(res - tau_Q_num)}")
print(f"  Fixed point CONFIRMED to dps=30.")

# Try a few more alpha
for ai, bi in [(1, 1), (5, -3), (7, 2), (-1, 4)]:
    M = mpmath.matrix([[ai, -11*bi], [2*bi, ai]])
    if M[0,0]*M[1,1] - M[0,1]*M[1,0] == 0:
        continue
    res = (M[0,0]*tau_Q_num + M[0,1]) / (M[1,0]*tau_Q_num + M[1,1])
    err = abs(res - tau_Q_num)
    print(f"  alpha = {ai} + {bi}*sqrt(-22): err = {err}")

print("\n" + "="*70)
print("CONCLUSION (B): q_{tau_Q} EXISTS as embedding K^* -> GL_2^+(Q)")
print("                fixing tau_Q = i*sqrt(11/2).")
print()
print("Specifically: q_{tau_Q}(a + b*sqrt(-22)) = [[a, -11b], [2b, a]]")
print()
print("This is q_{tau_principal} CONJUGATED by g_Q = diag(1, 2) ∈ GL_2^+(Q).")
print("The principal CM point tau = sqrt(-22) (Im=4.690) and the non-principal")
print("tau_Q = sqrt(-22)/2 (Im=2.345) are LINKED by g_Q in PSL_2(Q+).")
print()
print("IMPORTANT: g_Q is NOT in PSL_2(Z), so tau_principal and tau_Q are")
print("NOT equivalent in the modular curve X(1) = H/PSL_2(Z) — they are")
print("DISTINCT CM points there. But in PSL_2(Q+) they are linked.")
print("="*70)
