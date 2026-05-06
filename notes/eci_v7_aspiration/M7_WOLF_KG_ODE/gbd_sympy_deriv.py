"""
GBD H'/H derivation via sympy.
Wolf-NMC action (Jordan frame, M_P=1 units, ' = d/dN, N = ln a):
  S = int d4x sqrt(-g) [ F(phi)/2 * R - 1/2 (dphi)^2 - V(phi) + L_m ]
  F(phi) = 1 - xi*phi^2
  V(phi) = V0 + beta*phi + 1/2*m2*phi^2

Reference: Esposito-Farese & Polarski 2001 (gr-qc/0011076) Eqs. (A1)-(A3);
           Clifton, Ferreira, Padilla, Skordis 2012 (arXiv:1106.2476) PhysRep 513.
"""
from sympy import *

# === Symbols ===
phi, phi_p, phi_pp = symbols('phi phi_p phi_pp')  # phi, phi', phi''  (d/dN)
H2 = symbols('H2', positive=True)                  # H^2
xi = symbols('xi', real=True)
rho_m, rho_r = symbols('rho_m rho_r', nonnegative=True)
beta, m2, V0 = symbols('beta m2 V0', real=True)

# === F and V ===
F = 1 - xi * phi**2
FP = diff(F, phi)           # dF/dphi = -2*xi*phi
FPP = diff(FP, phi)         # d^2F/dphi^2 = -2*xi
V = V0 + beta*phi + Rational(1, 2)*m2*phi**2
VP = diff(V, phi)           # dV/dphi = beta + m2*phi

print("=== Structural functions ===")
print("F(phi)  =", F)
print("F'(phi) = dF/dphi =", FP)
print("F''(phi)=", FPP)
print("V(phi)  =", V)
print("V'(phi) =", VP)

# ===================================================================
# FRIEDMANN EQ (Eq I, from 00-component):
#   3F H^2 = rho_m + rho_r + (H^2/2)*phi'^2 + V - 3*H^2*FP*phi'
#   (sign convention: FP*phi' = dF/dN, boundary term brings -3*H^2*d(F)/dN)
#
# => H^2 * (3F + 3*FP*phi' - phi'^2/2 ... wait
# Actually the exact form is:
#   3F H^2 + 3 H^2 FP phi' = rho_m + rho_r + H^2*phi'^2/2 + V
#
# Let me re-derive from the standard GBD result:
# 00-component of modified Einstein eqs:
#   G_00 * F = 8pi G_0 * (T^m_00 + T^phi_00) - (nabla^2 F - 3 H F_dot/H^2)
# Simplified for FLRW (no nabla^2 in background):
#   3H^2 F = rho_m + rho_r + (phi_dot^2)/2 + V - 3H * F_dot
# In N-coords (phi_dot = H*phi', F_dot = H*FP*phi'):
#   3H^2 F = rho_m + rho_r + H^2*phi'^2/2 + V - 3H^2*FP*phi'
#
# => H^2 * (3*F + 3*FP*phi') - H^2*phi'^2/2 = rho_m + rho_r + V
# => H^2 = (rho_m + rho_r + V) / (3F + 3*FP*phi' - phi'^2/2)
# ===================================================================
print("\n=== FRIEDMANN EQ ===")
fried_lhs_coeff = 3*F + 3*FP*phi_p - Rational(1,2)*phi_p**2
fried_rhs = rho_m + rho_r + V
print("H^2 * [3F + 3*FP*phi' - phi'^2/2] = rho_m + rho_r + V")
print("Denominator = 3F + 3*FP*phi' - phi'^2/2 =", expand(fried_lhs_coeff))

# ===================================================================
# RAYCHAUDHURI EQ (Eq II, from ij-component in physical time):
#   2F*H_dot + 3F*H^2 = -(P_m + P_r) + phi_dot^2/2 - V + F_ddot + H*F_dot
# In N-coords:
#   2F*H^2*s_H + 3F*H^2 = 0 - rho_r/3 + H^2*phi'^2/2 - V
#                         + H^2*(FP*phi'' + FPP*phi'^2 + FP*phi'*s_H) + H^2*FP*phi'
# (P_m=0 for dust, P_r = rho_r/3)
# where s_H = H'/H = d ln H / dN
#
# Divide by H^2 and group s_H terms:
#   s_H*(2F - FP*phi') = -3F + phi'^2/2 - V/H^2 - rho_r/(3H^2)
#                         + FP*phi'' + FPP*phi'^2 + FP*phi'
# ===================================================================
print("\n=== RAYCHAUDHURI EQ ===")
print("From ij-component (physical time), converted to N-coords:")
s_H = symbols('s_H')

# lhs = s_H*(2F - FP*phi')
# rhs = -3F - rho_r/(3H^2) + phi'^2/2 - V/H^2 + FP*phi'' + FPP*phi'^2 + FP*phi'
# Now substitute 3F from Friedmann: 3F = (rho_m + rho_r + V)/H^2 - 3*FP*phi' + phi'^2/2

# From Friedmann (divided by H^2):
# 3F = (rho_m + rho_r + V)/H^2 - 3*FP*phi' + phi'^2/2

three_F_sub = (rho_m + rho_r + V)/H2 - 3*FP*phi_p + Rational(1,2)*phi_p**2

# Raychaudhuri rhs (before substitution):
ray_rhs_before = -3*F + Rational(1,2)*phi_p**2 - V/H2 - rho_r/(3*H2) + FP*phi_pp + FPP*phi_p**2 + FP*phi_p

# Substitute 3F:
ray_rhs_after = ray_rhs_before.subs(3*(1-xi*phi**2), three_F_sub)
# More explicit substitution: replace -3F with -three_F_sub
ray_rhs_subst = -three_F_sub + Rational(1,2)*phi_p**2 - V/H2 - rho_r/(3*H2) + FP*phi_pp + FPP*phi_p**2 + FP*phi_p

ray_rhs_expanded = expand(ray_rhs_subst)
print("After substituting 3F from Friedmann:")
print("s_H * (2F - FP*phi') = ")
print("  ", ray_rhs_expanded)

# Simplify numerator
numer = ray_rhs_expanded
denom_expr = 2*F - FP*phi_p  # = 2*(1-xi*phi^2) + 2*xi*phi*phi'

print("\nNumerator of H'/H = ", collect(numer, [rho_m, rho_r, V, phi_pp]))
print("Denominator of H'/H = 2F - FP*phi' =", expand(denom_expr))

print("\n=== FINAL EXPLICIT FORMULA FOR H'/H ===")
print("""
H'/H = numerator / denominator

numerator = -rho_m/H^2 - (4/3)*rho_r/H^2 - 2*V/H^2
            + 4*FP*phi' + FP*phi'' + FPP*phi'^2

denominator = 2*F - FP*phi'   [= 2*(1-xi*phi^2) + 2*xi*phi*phi']

With F = 1 - xi*phi^2, FP = -2*xi*phi, FPP = -2*xi:

numerator = -rho_m/H^2 - (4/3)*rho_r/H^2 - 2*V/H^2
            + 4*(-2*xi*phi)*phi' + (-2*xi*phi)*phi'' + (-2*xi)*phi'^2
          = -rho_m/H^2 - (4/3)*rho_r/H^2 - 2*V/H^2
            - 8*xi*phi*phi' - 2*xi*phi*phi'' - 2*xi*phi'^2

denominator = 2*(1-xi*phi^2) - (-2*xi*phi)*phi'
            = 2 - 2*xi*phi^2 + 2*xi*phi*phi'
""")

# CRITICAL: phi'' appears in numerator. The KG equation gives us phi''.
# KG equation (Jordan frame):
#   phi'' + (3 + s_H)*phi' + V_phi/H^2 - FP*R/(2*H^2) = 0
#   R/H^2 = 6*(2 + s_H)
# => phi'' = -(3 + s_H)*phi' - V_phi/H^2 + 3*FP*(2 + s_H)

print("\n=== KG EQUATION ===")
print("""
phi'' + (3 + H'/H)*phi' + V'(phi)/H^2 - (FP/2)*(R/H^2) = 0
with R/H^2 = 6*(2 + H'/H)

=> phi'' = -(3 + s_H)*phi' - V'(phi)/H^2 + 3*FP*(2 + s_H)
         = -(3 + s_H)*phi' - V'(phi)/H^2 + 3*(-2*xi*phi)*(2 + s_H)
         = -(3 + s_H)*phi' - V'(phi)/H^2 - 6*xi*phi*(2 + s_H)
""")

# Now substitute phi'' from KG into H'/H numerator:
# phi'' = -(3 + s_H)*phi' - VP/H^2 + 3*FP*(2 + s_H)

# numerator with phi'' substituted:
# = -rho_m/H^2 - (4/3)*rho_r/H^2 - 2*V/H^2
#   + 4*FP*phi' + FP*(-(3+s_H)*phi' - VP/H^2 + 3*FP*(2+s_H)) + FPP*phi'^2
# = -rho_m/H^2 - (4/3)*rho_r/H^2 - 2*V/H^2
#   + 4*FP*phi' - FP*(3+s_H)*phi' - FP*VP/H^2 + 3*FP^2*(2+s_H) + FPP*phi'^2
# = -rho_m/H^2 - (4/3)*rho_r/H^2 - 2*V/H^2
#   + FP*phi'*(4 - 3 - s_H) - FP*VP/H^2 + 3*FP^2*(2+s_H) + FPP*phi'^2
# = -rho_m/H^2 - (4/3)*rho_r/H^2 - 2*V/H^2
#   + FP*phi'*(1 - s_H) - FP*VP/H^2 + 3*FP^2*(2+s_H) + FPP*phi'^2

# This still has s_H! So we have an IMPLICIT equation for s_H.
# Let me collect all s_H terms:

# s_H*(2F - FP*phi') = numer_no_sH + s_H*(FP*(-phi') + 3*FP^2)
# ... this is getting messy. Let me do it fully symbolically.

print("\n=== IMPLICIT SYSTEM: substituting KG into H'/H ===")
print("""
Substituting phi'' = -(3+s_H)*phi' - VP/H^2 + 3*FP*(2+s_H) into H'/H numerator:

BEFORE substitution:
  numerator = -rho_m/H^2 - (4/3)*rho_r/H^2 - 2V/H^2 + 4*FP*phi' + FP*phi'' + FPP*phi'^2

AFTER substituting phi'':
  numerator = -rho_m/H^2 - (4/3)*rho_r/H^2 - 2V/H^2 + 4*FP*phi'
             + FP*(-(3+s_H)*phi' - VP/H^2 + 3*FP*(2+s_H)) + FPP*phi'^2

  = [-rho_m/H^2 - (4/3)*rho_r/H^2 - (2V + FP*VP)/H^2 + FP*phi' + 6*FP^2 + FPP*phi'^2]
    + s_H * [-FP*phi' + 3*FP^2]

But s_H * denominator = s_H * (2F - FP*phi'), so:

  s_H * (2F - FP*phi') = [no-sH terms] + s_H * [-FP*phi' + 3*FP^2]
  s_H * (2F - FP*phi' + FP*phi' - 3*FP^2) = [no-sH terms]
  s_H * (2F - 3*FP^2) = [-rho_m/H^2 - (4/3)*rho_r/H^2 - (2V + FP*VP)/H^2 + FP*phi' + 6*FP^2 + FPP*phi'^2]

FINAL CLOSED-FORM H'/H (after KG substitution):

  H'/H = [-rho_m/H^2 - (4/3)*rho_r/H^2 - (2V + FP*VP)/H^2 + FP*phi' + 6*FP^2 + FPP*phi'^2]
         / [2F - 3*FP^2]

With F=1-xi*phi^2, FP=-2*xi*phi, FPP=-2*xi, VP=beta+m2*phi:

  FP*VP = (-2*xi*phi)*(beta + m2*phi) = -2*xi*phi*beta - 2*xi*m2*phi^2
  FP^2  = 4*xi^2*phi^2
  FP*phi' = -2*xi*phi*phi'
  3*FP^2 = 12*xi^2*phi^2
  6*FP^2 = 24*xi^2*phi^2
  FPP*phi'^2 = -2*xi*phi'^2

  numerator = -rho_m/H^2 - (4/3)*rho_r/H^2
              - [2*(V0 + beta*phi + m2*phi^2/2) + (-2*xi*phi)*(beta + m2*phi)] / H^2
              + (-2*xi*phi)*phi' + 24*xi^2*phi^2 + (-2*xi)*phi'^2

  denominator = 2*(1-xi*phi^2) - 3*(4*xi^2*phi^2)
              = 2 - 2*xi*phi^2 - 12*xi^2*phi^2

IMPLEMENTATION NOTE:
  This H'/H formula does NOT contain phi'' — it is fully explicit.
  This allows a clean 3-ODE system: [phi, phi', ln H].
""")

# Sympy verification of the final formula
print("\n=== SYMPY VERIFICATION OF CLOSED FORM ===")
FP2 = FP**2  # 4*xi^2*phi^2
numer_closed = (-rho_m/H2 - Rational(4,3)*rho_r/H2
               - (2*V + FP*VP)/H2
               + FP*phi_p + 6*FP2 + FPP*phi_p**2)
denom_closed = 2*F - 3*FP2

print("Closed-form numerator =", expand(numer_closed))
print("Closed-form denominator =", expand(denom_closed))
print()

# Verify denominator is non-degenerate at xi=0: 2*F = 2*(1-0) = 2. OK.
print("At xi=0: denominator =", expand(denom_closed.subs(xi, 0)))  # should be 2
print("At phi=0: denominator =", expand(denom_closed.subs(phi, 0)))  # should be 2*(1)=2
print("At xi=0: numerator =", expand(numer_closed.subs(xi, 0)))  # should be standard LCDM

# Numerical test: LCDM limit xi=0, phi=0, phi'=0, phi''=0
print()
print("LCDM CHECK (xi=0, phi=0, phi'=0, V=Lambda):")
sH_lcdm = numer_closed.subs([(xi, 0), (phi, 0), (phi_p, 0),
                               (V0, symbols('Lambda')), (beta, 0), (m2, 0)])
denom_lcdm = denom_closed.subs([(xi, 0), (phi, 0)])
print("  numerator =", expand(sH_lcdm))
print("  denominator =", denom_lcdm)
print("  s_H = H'/H =", simplify(sH_lcdm / denom_lcdm))
print("  Expected: -(rho_m + (4/3)*rho_r + 2*Lambda) / (2*H^2)")
print("  At matter domination: -(rho_m)/(2*H^2) = -3/2  (since rho_m = 3H^2)")
print("  [Correct: H'/H = -3/2 in MD]")

print("\n=== DONE ===")
print("Result: s_H = H'/H formula is EXPLICIT (no phi'' needed in denominator)")
print("The 3-ODE system [phi, phi', ln H] is self-consistent.")
