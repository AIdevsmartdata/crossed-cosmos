"""
M144 Direction 2 — Bost-Connes KMS_∞ at τ=i for K = Q(i)

What the Connes-Marcolli-Ramachandran (CMR) paper (arXiv:math/0501424)
actually says for K = Q(i):

(A) The CM system (A_K, sigma_t).  K = Q(i), O = Z[i], class number h_K = 1.
    Algebra A_K is Morita equivalent to C_0(A_K^*) ⋊ K^* / O^* (Eq 4.17).
    Time evolution sigma_t(f)(L, L') = |L/L'|^{it} f(L, L')          (Eq 4.20)
    where |L/L'| = covol(Lambda')/covol(Lambda) = ratio of K-lattice norms.
    Hamiltonian H eps_J = log n(J) eps_J  for J an ideal in O = Z[i]   (Eq 4.24)
    Partition function Z(beta) = sum_{J ideal} n(J)^{-beta} = zeta_K(beta)   (Eq 4.25)

(B) KMS states (CMR Theorem 5.1):
    - In 0 < beta <= 1: unique KMS state.
    - For beta > 1: extremal KMS_beta states are parameterized by invertible
      K-lattices E_beta ≃ A_{K,f}^* / K^*    (with free transitive action of
      idele class group I_K / K^* as symmetries).  No special role of tau=i.
    - KMS_∞ states are weak limits of KMS_beta states.  The extremal KMS_∞
      states evaluated on the arithmetic subalgebra A_{K,Q} take values in
      K^{ab} (the maximal abelian extension of K).
      Class field theory isomorphism (5.3):
        alpha . phi_{infty,L} = phi_{infty,L} . theta^{-1}(alpha)
      for alpha in Gal(K^{ab}/K).

(C) The role of tau in the CMR-CM system: each invertible K-lattice
    L = (Lambda, phi) corresponds to an elliptic curve E = C/Lambda WITH
    CM by O = Z[i].  Up to isomorphism there is ONE such elliptic curve
    (h_K = 1), with j-invariant j(i) = 1728.  The KMS_∞ state phi_{∞,L}
    is parametrized by the idele s ∈ A_{K,f}^* / K^*, NOT by tau.

KEY POINT for ECI:
    The "ground state" in the BC-CMR sense is NOT a single state at tau=i;
    it is a whole orbit of states under the idele class group action.
    The point tau = i (j=1728) is the unique CM modulus for E = C/Z[i],
    which is ENCODED in the algebra (since K-lattices automatically have
    CM by Z[i]) but NOT a distinguished KMS_∞ ground state.

(D) NEW BRIDGE INSIGHT discovered here:
    The arithmetic subalgebra A_{K,Q} ⊂ A_K is the analog of the modular
    field on Y(2) = X(2) \ {cusps}, and CMR Eq 5.13:
        F_tau = K^{ab}     for any CM modulus tau (Shimura)
    The modulus tau enters via the embedding q_tau: K^* → GL_2^+(Q).
    For K = Q(i), the natural embedding sends τ = i, hence
        q_i: K^* → GL_2^+(Q)
        a + bi → ((a, b), (-b, a))     (rotation matrices)
    The action of K^* preserves tau = i.

    Therefore, the FIXED POINT τ=i of K^* ⊂ GL_2^+(Q) acting on H is
    AUTOMATICALLY where the CMR-CM system "lives" geometrically.

    This is the rigorous formulation of the M141 (D) reframing in
    operator-algebraic language: the SUGRA Kähler manifold (H, K=-3 log 2 Im τ)
    has its fixed point τ=i which IS the unique modulus of an O = Z[i]-CM
    elliptic curve in Q(i)-class number 1.

(E) NO contact with V_F:
    The CMR system is defined PURELY ARITHMETICALLY. V_F enters nowhere.
    The KMS_∞ ground state and the V_F minimum at τ=i are anchored at the
    same point for the same fundamental reason: tau=i is the j-1728 = 0
    point AND simultaneously the Z[i] CM modulus. But this is a KINEMATIC
    coincidence (encoding the structure of Q(i)) not a dynamical link.
"""
import sympy as sp
from sympy import I, Matrix, symbols, exp

# Verify the q_tau embedding for K = Q(i), tau = i:
# K^* = (Q(i))^* embeds into GL_2^+(Q) by
#   a + b*i -> matrix that acts as multiplication by (a + b*i) on Q + i*Q
# Using the basis (1, i): (a + bi)*1 = a + bi, (a + bi)*i = -b + ai
# So the matrix is [[a, -b], [b, a]] (column vectors!) i.e.
#   q(a + bi) = ((a, -b), (b, a))
#
# The action on H by Mobius transformation:
#   M.tau = (M_11 tau + M_12) / (M_21 tau + M_22)
# At tau = i:
#   q(a+bi).i = (a*i - b) / (b*i + a) = (-b + a i) / (a + b i)
# Multiply num and den by (a - bi):
#   = (-b + ai)(a - bi) / (a^2 + b^2)
#   = (-ab + ab i^2 + a^2 i + b^2 i) / (a^2 + b^2)   -- wait let me recompute
#   = (-ab + b^2 i + a^2 i - ab i^2) / (a^2 + b^2)
#   = (-ab + ab + (a^2 + b^2) i) / (a^2 + b^2)
#   = i.

a, b = symbols('a b', real=True)
M = Matrix([[a, -b], [b, a]])
tau_i = I

def mobius(M, tau):
    return (M[0,0]*tau + M[0,1]) / (M[1,0]*tau + M[1,1])

result = sp.simplify(mobius(M, tau_i))
print("Mobius action of q(a+bi) on tau=i:")
print(f"  M = {M}")
print(f"  M.i = {result}")
print(f"  Simplified: {sp.simplify(result - I)}")  # should be 0
print()
print("=> q(K^*) fixes tau = i for K = Q(i).  CHECK.")
print()
print("Geometric meaning: the elliptic curve E_i = C/Z[i] has")
print("End(E_i) ⊗ Q = Q(i).  The CM action of Q(i) on E_i lifts to the")
print("CMR algebra via the q_i embedding.  All extremal KMS_infty states")
print("are sourced from this single CM modulus tau = i (h_K=1).")

print()
print("="*68)
print("NUMERICAL: zeta_K(beta) for K = Q(i)")
print("="*68)
import mpmath
mpmath.mp.dps = 30
# zeta_{Q(i)}(s) = zeta(s) * L(s, chi_4)  where chi_4 is the quadratic character mod 4
# (chi_4(1) = 1, chi_4(3) = -1, chi_4(0) = chi_4(2) = 0)
# Equivalently, zeta_{Q(i)}(s) = sum_{J ideal} N(J)^{-s}
def L_chi4(s):
    """Dirichlet L-function for the unique non-trivial Dirichlet character mod 4."""
    # L(s, chi_4) = sum_{n>=0} (-1)^n / (2n+1)^s
    # Use mpmath's built-in dirichlet character
    return mpmath.dirichlet(s, [0, 1, 0, -1])

def zeta_Qi(s):
    return mpmath.zeta(s) * L_chi4(s)

# Some test values
for beta_val in [1.5, 2.0, 3.0, 10.0, 100.0]:
    zk = zeta_Qi(beta_val)
    print(f"  zeta_K({beta_val:6.2f}) = {zk}")
print()
print("Special values:")
print(f"  L(1, chi_4) = pi/4 = {mpmath.pi/4}, mpmath value = {L_chi4(1)}")
print(f"  L(2, chi_4) = G (Catalan) = {mpmath.catalan}, mpmath = {L_chi4(2)}")
print()
print("For ECI the partition function Z(β) = ζ_K(β) at τ=i has")
print("'free energy' F(β) = -log Z(β)/β. The β → ∞ limit (KMS_∞ ground state)")
print("is a single state up to the I_K/K^* orbit.")

print()
print("="*68)
print("CONCLUSION DIRECTION 2")
print("="*68)
print()
print("1) The CMR-CM system for K=Q(i) is a real, well-defined operator")
print("   algebra (A_K, sigma_t).  Its KMS_∞ ground states ARE parameterized")
print("   by the idele class group A_{K,f}^* / K^*, all anchored at tau=i.")
print()
print("2) V_F's minimum at tau=i and the BC-CMR ground state being 'at' tau=i")
print("   are LINKED: they both come from the FORCED structure that tau=i is")
print("   the unique Z[i]-CM modulus (j(i) = 1728, E_6(i) = 0).")
print()
print("3) BUT: V_F is a SUGRA scalar potential on the field-space H, while")
print("   the CMR algebra is an arithmetic operator algebra.  There is NO")
print("   direct identity 'V_F = -log(KMS_∞ density)' or similar.  The two")
print("   are different mathematical objects that coincide on tau=i because")
print("   tau=i is the unique structural fixed point of the K^* action.")
print()
print("4) NEW (M144): The Bost-Connes-Marcolli-Ramachandran Q(i) algebra")
print("   gives an ARITHMETIC backbone for ECI v8.1's tau=i kinematic bridge")
print("   that goes beyond M134's geometric statement.  The KMS_∞ states")
print("   evaluate the modular field F_{tau=i} = Q(i)^{ab} = Q(i, j(i) torsion)")
print("   = abelian extension generated by torsion of E_i = C/Z[i].")
print()
print("5) Falsifiable prediction: for ECI to have an OPERATOR-ALGEBRAIC")
print("   modular-shadow bridge (M45 TBD-3), the M_BIX wedge algebra A_obs")
print("   should sit inside A_K (Q(i) BC-CMR) in some natural way.")
print("   M141's geodesic-flow bridge is GL_2-system territory (Q-lattices),")
print("   but the Q(i)-CM specialization picks out tau=i.")
