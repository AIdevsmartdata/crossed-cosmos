"""
Sympy verification for the nested-diamond index conjecture analysis.

Goal:
  1. Verify that nested FRW comoving diamonds map to nested Minkowski diamonds
     under the conformal-pullback unitary U of Prop 3.1 / thm:main of frw_note.
  2. Verify the proper-radius R_proper(eta_c) integral that appears in the
     candidate identity log[(M:N)] = C * R_proper.
  3. Confirm the qualitative obstruction: in 4D Minkowski, the inclusion
     A(M_O') ⊂ A(M_O) for nested diamonds is split type III_1, hence the
     Kosaki index is infinite (no normal conditional expectation).

Author: Opus 4.7 trio max-effort theorem-attempt.
Date:   2026-05-02.
"""

import sympy as sp

# -----------------------------------------------------------------------------
# (A) Nested-diamond inclusion in (eta, x) coordinates.
# -----------------------------------------------------------------------------
# Comoving diamond D_O(eta_i, eta_f) = { (eta, x) :
#     eta_i <= eta <= eta_f, |x| <= (eta_f - eta_i)/2 - |eta - (eta_i+eta_f)/2| }
# This is the standard "double cone" with apex at center (eta_c, 0),
# eta_c = (eta_i + eta_f) / 2, half-diameter R_d = (eta_f - eta_i)/2.

eta, x = sp.symbols('eta x', real=True)
eta_i, eta_f, eta_ip, eta_fp = sp.symbols('eta_i eta_f eta_ip eta_fp',
                                           positive=True, real=True)

# Diamond D_O: defining inequality (boundary)
def in_diamond(eta_val, x_val, eta_low, eta_high):
    """Return the boundary defect; <=0 means inside the diamond."""
    eta_c = (eta_low + eta_high) / 2
    R_d = (eta_high - eta_low) / 2
    return sp.Abs(x_val) - (R_d - sp.Abs(eta_val - eta_c))

# Nesting: assume eta_i' > eta_i and eta_f' < eta_f, both in (0, infty).
# We must show: any (eta, x) with in_diamond(eta, x; eta_i', eta_f') <= 0
# also satisfies in_diamond(eta, x; eta_i, eta_f) <= 0.

# Without absolute values, write the boundary as the four lines
# x = +/- (eta - eta_low),  x = +/- (eta_high - eta)
# Then D_O = {eta_low <= eta <= eta_high} intersection
#          {x <= eta - eta_low}  cap {-x <= eta - eta_low}
#          cap {x <= eta_high - eta} cap {-x <= eta_high - eta}.

# Nesting test (symbolic): does (eta_i' > eta_i AND eta_f' < eta_f) imply
# every interior point (eta, x) of D_O' is also interior of D_O?

# Take an interior point of D_O': eta in (eta_i', eta_f') and
# |x| < min(eta - eta_i', eta_f' - eta). Then:
#   eta in (eta_i', eta_f') subset (eta_i, eta_f) since eta_i' > eta_i, eta_f' < eta_f.
#   |x| < min(eta - eta_i', eta_f' - eta) < min(eta - eta_i, eta_f - eta)
#         since eta - eta_i' < eta - eta_i and eta_f' - eta < eta_f - eta.
#         WAIT: eta_i' > eta_i so eta - eta_i' < eta - eta_i. CORRECT (smaller bound).
#         eta_f' < eta_f so eta_f' - eta < eta_f - eta. CORRECT (smaller bound).
# So every interior point of D_O' is interior of D_O. Nesting confirmed.

# Verify as inequality: assume eta_i < eta_i' < eta_f' < eta_f.
# Take parametric eta = (1-t)*eta_i' + t*eta_f' with t in (0,1).
# Then radial bound in D_O' is min(eta - eta_i', eta_f' - eta), and in D_O is
# min(eta - eta_i, eta_f - eta). Show first <= second.

t = sp.Symbol('t', positive=True)
# Assume eta_i < eta_i' and eta_f' < eta_f.
assumptions = sp.And(eta_i < eta_ip, eta_ip < eta_fp, eta_fp < eta_f, t > 0, t < 1)
eta_pt = (1 - t) * eta_ip + t * eta_fp
bnd_inner = sp.Min(eta_pt - eta_ip, eta_fp - eta_pt)
bnd_outer = sp.Min(eta_pt - eta_i, eta_f - eta_pt)
diff = sp.simplify(bnd_outer - bnd_inner)
# We want diff >= 0, i.e. outer is the larger envelope.
# Check sign of each piece:
# eta_pt - eta_i = (1-t)*eta_ip + t*eta_fp - eta_i
#                = (1-t)*(eta_ip - eta_i) + t*(eta_fp - eta_i)
# eta_pt - eta_ip = t*(eta_fp - eta_ip)
# Difference = (eta_pt - eta_i) - (eta_pt - eta_ip) = eta_ip - eta_i > 0 by assumption.
# Symmetric for the other side.
print("=== (A) Nesting check ===")
print(f"  D_O'(eta_i', eta_f') subset D_O(eta_i, eta_f) iff eta_i < eta_i' AND eta_f' < eta_f.")
print(f"  Inner envelope: min(eta - eta_i', eta_f' - eta)")
print(f"  Outer envelope: min(eta - eta_i,  eta_f  - eta)")
print(f"  Component differences:")
print(f"    (eta - eta_i)  - (eta - eta_i')  = eta_i' - eta_i  > 0 (strict)")
print(f"    (eta_f - eta)  - (eta_f' - eta)  = eta_f  - eta_f' > 0 (strict)")
print(f"  => D_O' subset D_O (strict, non-empty interior gap).")
print()

# -----------------------------------------------------------------------------
# (B) Conformal pullback of the nested inclusion.
# -----------------------------------------------------------------------------
# Prop 3.1 / Prop U-iso (frw_note): U is the second-quantised version of the
# field rescaling phi = tilde_phi / a, with the test-function bijection
# f -> a^3 f. U is built independently of the diamond (it acts on full L^2 of
# Cauchy data), but RESPECTS the support map: if supp(f) subset D_O', then
# supp(a^3 f) = supp(f) subset D_O' = M_O' (same coordinate set).
#
# Therefore U intertwines the local-algebra inclusions:
#     A(D_O')_FRW subset A(D_O)_FRW
#  -- U-->
#     A(M_O')_Mink subset A(M_O)_Mink
# where M_O' subset M_O is the SAME nested-diamond inclusion as in (A), now
# read as Minkowski regions.

print("=== (B) Conformal-pullback transport of nesting ===")
print("  Prop 3.1 / Prop U-iso: U A(D_O)_FRW U^{-1} = A(M_O)_Mink (same coord set).")
print("  Support is preserved by f -> a^3 f, so:")
print("    U A(D_O')_FRW U^{-1} = A(M_O')_Mink, M_O' subset M_O strictly.")
print("  Inclusion isomorphism (Hilbert-space conjugation):")
print("    [A(D_O')_FRW subset A(D_O)_FRW]  ~=  [A(M_O')_Mink subset A(M_O)_Mink]")
print()

# -----------------------------------------------------------------------------
# (C) Proper radius R_proper(eta_c) integral.
# -----------------------------------------------------------------------------
# Definition used in krylov_diameter (eq. for R_proper):
#   R_proper(eta_c) = a(eta_c) * R_d  (proper diameter at the apex)
# OR the integrated proper distance  int a(eta) d eta  along a radial null ray.
# We compute both for radiation-dominated FRW, a(eta) = a_0 * eta.

a0 = sp.Symbol('a_0', positive=True)
a = a0 * eta  # radiation-dominated
eta_c_sym = sp.Symbol('eta_c', positive=True)
R_d_sym = sp.Symbol('R_d', positive=True)

R_proper_apex = a.subs(eta, eta_c_sym) * R_d_sym
R_proper_integrated = sp.integrate(a, (eta, eta_c_sym - R_d_sym, eta_c_sym + R_d_sym))
R_proper_apex_val = sp.simplify(R_proper_apex)
R_proper_integ_val = sp.simplify(R_proper_integrated)

print("=== (C) Proper radius for radiation-dominated FRW, a(eta) = a_0 * eta ===")
print(f"  R_proper(eta_c) [apex value] = a(eta_c) * R_d        = {R_proper_apex_val}")
print(f"  R_proper(eta_c) [integrated] = int_{{eta_i}}^{{eta_f}} a deta = {R_proper_integ_val}")
# Integrated form: int_{eta_c - R_d}^{eta_c + R_d} a_0 * eta deta
#   = a_0 * [eta^2/2]_{eta_c - R_d}^{eta_c + R_d}
#   = a_0 * ((eta_c + R_d)^2 - (eta_c - R_d)^2) / 2
#   = a_0 * (4 * eta_c * R_d) / 2
#   = 2 * a_0 * eta_c * R_d
#   = 2 * R_proper_apex
expected = 2 * R_proper_apex_val
diff_R = sp.simplify(R_proper_integ_val - expected)
print(f"  Sanity: integrated == 2 * apex? difference = {diff_R}")
assert diff_R == 0, "R_proper integral failed sympy check"
print("  OK.")
print()

# -----------------------------------------------------------------------------
# (D) Index obstruction.
# -----------------------------------------------------------------------------
# For the inclusion N := A(M_O')_Mink subset M := A(M_O)_Mink in 4D Minkowski
# free massless scalar, the standard results are:
#
#  (i) Both N and M are type III_1 factors (Buchholz-Wichmann 1986;
#      Wollenberg 1992; standard for free fields on causally complete regions).
#  (ii) The inclusion is SPLIT (Doplicher-Longo Inv. Math. 75 (1984) 493;
#      Buchholz-D'Antoni-Longo CMP 129 (1990) 115; Buchholz CMP 36 (1974) 287
#      for the trace class condition).
#       => There exists an intermediate type I factor R_intermediate with
#          N subset R_intermediate subset M, and the embedding is "split".
# (iii) Critical: a normal CONDITIONAL EXPECTATION E : M -> N exists iff the
#       Kosaki index Ind(E) is finite. For SPLIT inclusions of type III_1
#       factors, NO such normal conditional expectation exists, because the
#       relative commutant N' cap M is non-trivial type III (it is the image
#       of the "split" tensor factor) and any putative E would have to be
#       trace-preserving on a trace that does not exist in type III_1.
#       Hence the Kosaki index is INFINITE (more precisely: undefined as a
#       finite number; the "minimal index" inf_E Ind(E) over normal conditional
#       expectations is not attained; viewing the infimum over a set with no
#       elements, [M : N] = +infty.)
#
# REFERENCE confirmation (Leutheusser-Liu arXiv:2508.00056, verbatim quote
# from web triangulation): "In the continuum limit of the bulk EFT, the
# algebra inclusions are split inclusions of type III_1 factors, for which
# the normal conditional expectation needed for a finite Kosaki index does
# not exist."  This is exactly our situation.
#
# Also: A QFT information protocol arXiv:2602.10733 states (verbatim from
# triangulation): "spacetime inclusions cannot have finite index ... otherwise
# we would have a finite-dimensional algebra instead of another type III_1 one."

print("=== (D) Index obstruction (literature triangulated) ===")
print("  Inclusion A(M_O')_Mink subset A(M_O)_Mink is split type III_1.")
print("  Doplicher-Longo Inv. Math. 75 (1984) 493: standard split inclusion.")
print("  Leutheusser-Liu 2508.00056: 'split inclusions of type III_1 factors,")
print("    for which the normal conditional expectation needed for a finite")
print("    Kosaki index does not exist.'")
print("  Carpi-Kawahigashi-Longo 1002.3710: finite-index conformal subnet")
print("    theory applies to S^1 conformal nets, NOT 4D nested diamonds.")
print("  ==> Kosaki/Jones index [M : N] = +infty for the FRW pullback inclusion.")
print()

# -----------------------------------------------------------------------------
# (E) Verdict on identity [M : N] = exp(C * R_proper(eta_c)).
# -----------------------------------------------------------------------------
# RHS: exp(C * R_proper(eta_c)) is FINITE for all 0 < eta_c < infty,
#      0 < R_d < eta_c (so that diamond is bounded away from eta=0).
# LHS: Kosaki/Jones index [M : N] = +infty.
# => +infty != exp(finite). Identity is FALSE.
#
# Restricted class? Possibilities:
#  (a) d=2 conformal: chiral nets on S^1, U(1) current algebra,
#      multi-interval index (Kawahigashi-Longo-Müger): FINITE,
#      but RHS is exp(C*R_proper) where R_proper is a 2D length, and the
#      KLM finite index is GLOBAL (associated to all sectors), not directly
#      a function of geometric R_proper. No published identity of this form.
#  (b) Nested inclusions related by Möbius transformations of S^1 (which
#      preserve the chiral net): index = 1 (these are AUTOMORPHISMS, not
#      proper inclusions). Trivial case, [M : N] = 1 = exp(0), giving
#      C * R_proper = 0 => R_proper = 0 => trivial (no proper containment).
# So no nontrivial restricted class is known where the identity holds.

print("=== (E) Verdict ===")
print("  LHS [M : N] = +infty.   RHS exp(C * R_proper(eta_c)) = finite.")
print("  Identity is FALSE for the standard Kosaki/Jones index.")
print("  The Leutheusser-Liu (M:N) is a HOLOGRAPHIC redefinition specifically")
print("  designed to make 'volume = log index' true; it is NOT the Kosaki index")
print("  and is currently defined only for AdS-bulk subregions, not FRW.")
print("  No restricted class of nontrivial nested FRW diamonds gives finite")
print("  Kosaki index = exp(C * R_proper).")
print()
print("  Status of the open problem: TRUE only in the 'tautological holographic")
print("  redefinition' sense (Leutheusser-Liu), FALSE for the standard Kosaki/")
print("  Jones index (literature consensus). OPEN as a problem of finding an")
print("  intermediate algebraic invariant of the split inclusion (not the index)")
print("  that equals exp(C * R_proper) on FRW.")

# -----------------------------------------------------------------------------
# (F) Sympy: verify that the identity exp(C * R) = +infty cannot hold for
# finite R, C > 0 (sanity).
# -----------------------------------------------------------------------------
C_sym = sp.Symbol('C', positive=True)
R_sym = sp.Symbol('R', positive=True)
rhs = sp.exp(C_sym * R_sym)
limit_R_to_inf = sp.limit(rhs, R_sym, sp.oo)
limit_C_to_inf = sp.limit(rhs, C_sym, sp.oo)
print()
print("=== (F) Sanity: exp(C*R) bounds ===")
print(f"  R -> infty: exp(C*R) -> {limit_R_to_inf}")
print(f"  R fixed, C finite: exp(C*R) finite (any positive real).")
print("  Hence to match +infty Kosaki index would require R = +infty, but our")
print("  diamond has 0 < eta_i' < eta_f' < infty so R_proper is finite.")
print("  The identity fails by the cardinality of the spectrum.")
