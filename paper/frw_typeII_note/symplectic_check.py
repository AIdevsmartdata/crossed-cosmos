"""
Verify: for the conformally coupled massless scalar on conformally flat FRW
(ds^2 = a(eta)^2 (-deta^2 + dx^2)), the rescaling phi_tilde = a phi maps the
*classical* solution space and its symplectic form to that of the flat
massless KG on Minkowski.

Test functions / solutions are functions on M.  We compute:

  sigma_FRW(phi1, phi2)
    = int_Sigma sqrt(h) n^mu (phi1 d_mu phi2 - phi2 d_mu phi1)

with Sigma = {eta = eta_0}, h = a^6 (induced 3-metric det), n^mu = (1/a, 0,0,0)
(unit future-pointing normal in the FRW metric), so

  sqrt(h) n^mu d_mu = a^3 * (1/a) * d_eta = a^2 * d_eta.

Hence:
  sigma_FRW(phi1, phi2) = int d^3x  a^2  (phi1 d_eta phi2 - phi2 d_eta phi1).

Now substitute phi_i = phi_tilde_i / a.

We expect: sigma_FRW(phi1, phi2) = sigma_Mink(phi_tilde_1, phi_tilde_2)
                                 = int d^3x (phi_tilde_1 d_eta phi_tilde_2
                                             - phi_tilde_2 d_eta phi_tilde_1).

The reviewer worries about derivatives of a(eta).  Let's see if they cancel.
"""
import sympy as sp

eta, x, y, z = sp.symbols('eta x y z', real=True)
# scale factor a(eta) and rescaled fields phi_tilde_i (functions of eta, x, y, z)
a = sp.Function('a')(eta)
pt1 = sp.Function('phitilde1')(eta, x, y, z)
pt2 = sp.Function('phitilde2')(eta, x, y, z)

# Original fields phi_i
phi1 = pt1 / a
phi2 = pt2 / a

# Integrand of FRW symplectic form (modulo int d^3x):
integrand_FRW = a**2 * (phi1 * sp.diff(phi2, eta) - phi2 * sp.diff(phi1, eta))
integrand_FRW_expanded = sp.expand(integrand_FRW)

# Integrand of Minkowski symplectic form:
integrand_Mink = pt1 * sp.diff(pt2, eta) - pt2 * sp.diff(pt1, eta)
integrand_Mink_expanded = sp.expand(integrand_Mink)

diff = sp.simplify(integrand_FRW_expanded - integrand_Mink_expanded)

print("=== FRW symplectic integrand (with phi_i = phi_tilde_i / a) ===")
print(integrand_FRW_expanded)
print()
print("=== Minkowski symplectic integrand (in phi_tilde) ===")
print(integrand_Mink_expanded)
print()
print("=== Difference (FRW - Mink) after simplification ===")
print(diff)
print()
print("Cancellation occurs <=>", diff == 0)
