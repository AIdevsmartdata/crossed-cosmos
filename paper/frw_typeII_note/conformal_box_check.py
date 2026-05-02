"""
Verify the conformal-covariance identity (eq. (5) in frw_note.tex):

    Box_Mink (a phi)  =  a^3 (Box_g - R/6) phi      (Wald sign convention)

for the metric g = a(eta)^2 eta_Mink (conformally flat FRW), with arbitrary
smooth a(eta) and arbitrary smooth phi(eta, x, y, z).

Sign convention: Wald 1994, "Quantum Field Theory in Curved Spacetime",
eq. (4.6.9): the EOM of the d=4 conformally coupled massless scalar is
(Box_g - R/6) phi = 0.
"""
import sympy as sp

eta, x, y, z = sp.symbols('eta x y z', real=True)
a = sp.Function('a')(eta)
phi = sp.Function('phi')(eta, x, y, z)

# Metric ds^2 = a(eta)^2 (-deta^2 + dx^2 + dy^2 + dz^2)
g = sp.diag(-a**2, a**2, a**2, a**2)
g_inv = g.inv()
sqrtg = a**4   # sqrt(-det g) = a^4
coords = [eta, x, y, z]

# Box_g phi = (1/sqrt(-g)) d_mu (sqrt(-g) g^{mu nu} d_nu phi)
def Box(psi):
    s = 0
    for mu in range(4):
        for nu in range(4):
            s += sp.diff(sqrtg * g_inv[mu, nu] * sp.diff(psi, coords[nu]), coords[mu])
    return s / sqrtg

# Ricci scalar R = 6 a''/a^3 for ds^2 = a^2 (-deta^2 + dx^2)
# (re-derivable from Christoffels; cf. Wald eq. (5.1.13))
R = 6 * sp.diff(a, eta, 2) / a**3

# Minkowski d'Alembertian
def BoxMink(psi):
    return -sp.diff(psi, eta, 2) + sp.diff(psi, x, 2) + sp.diff(psi, y, 2) + sp.diff(psi, z, 2)

LHS = sp.simplify(BoxMink(a * phi))
RHS = sp.simplify(a**3 * (Box(phi) - R * phi / 6))

diff = sp.simplify(LHS - RHS)

print("=== Conformal-covariance identity (Wald sign convention) ===")
print()
print("Box_Mink (a phi)  =  a^3 (Box_g - R/6) phi  ?")
print("Difference (LHS - RHS) after simplify =", diff)
print()
print("Identity holds (should be 0):", diff == 0)
