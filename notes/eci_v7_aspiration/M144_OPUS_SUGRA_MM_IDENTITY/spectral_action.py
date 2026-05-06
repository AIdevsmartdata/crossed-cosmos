"""
M144 Direction 3 — Spectral action S(D) for the SUGRA Kähler manifold

Setup
-----
Connes spectral action principle:
    S = Tr f(D^2 / Lambda^2)
where D is the Dirac operator, Lambda is a UV scale, f is a positive
even function. Asymptotic expansion as Lambda -> infinity:

    S ~ sum_{k>=0} f_k * Lambda^(d-2k) * a_{2k}(D^2)

where d = dimension of the manifold, a_{2k} are Seeley-DeWitt heat-kernel
coefficients, and f_k = (1/Gamma(k)) * int_0^infty u^{k-1} f(u) du.

For a 2-d Kahler manifold M = H/Gamma equipped with a metric of constant
Gaussian curvature K, the heat kernel of the Laplacian Delta_g satisfies
    K(t, x, x) ~ (1/(4 pi t)) * sum_{k>=0} a_{2k}(x) t^k
with
    a_0 = 1
    a_2 = R/6 = K/3   (since Ricci scalar R = 2 K in 2-d)
    a_4 = (1/360) (5 R^2 - 2 |Riem|^2 + 2 |Ric|^2 + 12 Delta R)
        = (1/360)(60 K^2 / d-related)  for constant curvature 2-d

For a 2-d manifold of CONSTANT Gaussian curvature K, R = 2K, |Ric|^2 = 2 K^2,
|Riem|^2 = 4 K^2, so
    a_4 = (1/360)(5 * 4 K^2 - 2 * 4 K^2 + 2 * 2 K^2 + 0)
        = (1/360)(20 K^2 - 8 K^2 + 4 K^2)
        = (1/360)(16 K^2)
        = (2/45) K^2.

Computation here
----------------
Compute the local Seeley-DeWitt coefficients for the Kähler 3 metric
(K = -2/3) and the Poincaré metric (K = -1).

The integrated coefficients on Gamma\H are obtained by
    int_M a_{2k} dvol = a_{2k}(point) * Vol(Gamma\H)

For Gamma = PSL(2, Z), Vol(Gamma\H_Poincare) = pi/3 (Gauss-Bonnet).
For ds^2 = c ds_P^2, Vol scales by c (in 2-d, dvol scales by sqrt(g)).
"""
import sympy as sp
from sympy import symbols, log, diff, simplify, sqrt, Rational, pi, integrate

x, y = symbols('x y', positive=True, real=True)

# Metric data
# Kähler 3: ds^2 = (3/(2 y^2)) (dx^2 + dy^2),  K_curv = -2/3
# Poincaré: ds^2 = (1/y^2)   (dx^2 + dy^2),    K_curv = -1
K_kahler = -Rational(2, 3)
K_poinc  = -Rational(1)

# In 2-d, Ricci scalar R = 2 K.
R_kahler = 2 * K_kahler
R_poinc  = 2 * K_poinc

# Seeley-DeWitt coefficients for 2-d constant-curvature manifold
def a0_local(K):
    return Rational(1)

def a2_local(K):
    return Rational(1, 3) * K   # = R/6 = (2K)/6 = K/3

def a4_local(K):
    return Rational(2, 45) * K**2

# Volumes
# Vol(PSL(2,Z) \ H, Poincaré) = pi/3 (classical Gauss-Bonnet)
# Vol(PSL(2,Z) \ H, Kähler 3) = (3/2) * pi/3 = pi/2
vol_poinc  = sp.pi / 3
vol_kahler = sp.Rational(3, 2) * vol_poinc

# Integrated heat-kernel coefficients
print("="*68)
print("Seeley-DeWitt coefficients on PSL(2,Z) \\ H")
print("="*68)
print()
print("Kähler 3 (K = -2/3):")
print(f"  a_0 (local)       = {a0_local(K_kahler)}")
print(f"  a_2 (local) = K/3 = {a2_local(K_kahler)}")
print(f"  a_4 (local)       = {a4_local(K_kahler)}")
print(f"  Vol               = {vol_kahler}")
print(f"  int a_0 dvol      = {a0_local(K_kahler) * vol_kahler}")
print(f"  int a_2 dvol      = {a2_local(K_kahler) * vol_kahler}")
print(f"  int a_4 dvol      = {a4_local(K_kahler) * vol_kahler}")
print()
print("Poincaré (K = -1):")
print(f"  a_0 (local)       = {a0_local(K_poinc)}")
print(f"  a_2 (local)       = {a2_local(K_poinc)}")
print(f"  a_4 (local)       = {a4_local(K_poinc)}")
print(f"  Vol               = {vol_poinc}")
print(f"  int a_0 dvol      = {a0_local(K_poinc) * vol_poinc}")
print(f"  int a_2 dvol      = {a2_local(K_poinc) * vol_poinc}")
print(f"  int a_4 dvol      = {a4_local(K_poinc) * vol_poinc}")
print()

# Spectral action expansion
# S(Lambda) ~ f_0 Lambda^d * int a_0 dvol + f_1 Lambda^{d-2} * int a_2 dvol + ...
# Here d = 2 (real dimension):
# S(Lambda) ~ f_0 Lambda^2 * Vol + f_1 * (cosmological term ~ K * Vol) + O(1/Lambda^2)
print("="*68)
print("Spectral action expansion (real dim d=2)")
print("="*68)
print()
print("S(Lambda) = f_0 Lambda^2 (int a_0) + f_1 (int a_2) + f_2 (1/Lambda^2)(int a_4) + ...")
print()
print("Kähler 3 expansion:")
print(f"  S = f_0 Lambda^2 * {vol_kahler}  +  f_1 * ({a2_local(K_kahler) * vol_kahler})  + ...")
print(f"    = (pi/2) f_0 Lambda^2 + ({a2_local(K_kahler) * vol_kahler}) f_1 + O(1/Lambda^2)")
print()
print("Poincaré expansion:")
print(f"  S = f_0 Lambda^2 * {vol_poinc}  +  f_1 * ({a2_local(K_poinc) * vol_poinc})  + ...")
print()

# Compare with V_F potential mass
# V_F minimum at tau=i: V_F(i) = 0, m_tau^2 = 2^16 * 3^6 * pi * Gamma(1/4)^4
# From M134: m_tau^2 (M_Pl=1) = (4/9) |W''(i)|^2 = 4 * 3456^2 * pi * Gamma(1/4)^4
print("="*68)
print("Comparison with V_F mass")
print("="*68)
print()
print("V_F at tau=i:")
print("  V_F(i) = 0  (Minkowski SUSY vacuum)")
print("  m_tau^2 = 2^16 * 3^6 * pi * Gamma(1/4)^4")
print("         (from quadratic Hessian (4/9)|W''(i)|^2 = (4/9)*3456^2*pi*Gamma(1/4)^4)")
print()
print("In the spectral action S(Lambda):")
print("  - 'Cosmological constant' term: f_0 Lambda^2 * Vol      [at order Lambda^2]")
print("  - 'Einstein-Hilbert' term:      f_1 * (R Vol)/12        [at order 1]")
print()
print("Mapping to SUGRA action (to leading order in derivatives):")
print("  Spectral S contains    f_0 Lambda^2 Vol  ↔  Lambda  (cosmological, at tau=i this VANISHES because V_F(i)=0)")
print("  Spectral S contains  f_1 * (chi Euler)  ↔  topological term, NOT mass")
print()

# Comparing the *value* of spectral action at one specific scaling
# If we identify Lambda = m_tau (the modulus mass), then
#    f_0 * m_tau^2 * Vol_kahler = f_0 * m_tau^2 * pi/2
# Numerical:
import math, mpmath
mpmath.mp.dps = 30
gamma14 = mpmath.gamma(mpmath.mpf(1)/4)
m_tau2 = mpmath.mpf(2)**16 * mpmath.mpf(3)**6 * mpmath.pi * gamma14**4
print(f"m_tau^2 = {m_tau2}")
print(f"m_tau   = {mpmath.sqrt(m_tau2)}")
vol_kah_num = mpmath.pi / 2
print(f"Vol(Kähler 3) = pi/2 = {vol_kah_num}")
print(f"m_tau^2 * Vol = {m_tau2 * vol_kah_num}")
print()
print("Test: does any combination of (m_tau^2, K, Vol, pi) equal a 'spectral action'?")
print(f"  pi^2 * m_tau^2 / 12         = {mpmath.pi**2 * m_tau2 / 12}")
print(f"  m_tau^2 * Vol_kah * (-K)    = {m_tau2 * vol_kah_num * mpmath.mpf(2)/3}")
print()
print("VERDICT for Direction 3:")
print("  V_F does NOT directly appear in the heat-kernel expansion of the")
print("  Laplacian on the Kähler manifold. It is a SEPARATE piece of data")
print("  (a SUGRA F-term potential), not derivable from spectral data of the")
print("  metric. The heat kernel only knows about (R, Vol, chi).")
print()
print("  HOWEVER: there is a nontrivial structural fact:")
print("    chi(PSL(2,Z) \\ H) = 1/12  (Gauss-Bonnet via cusp + ramif points)")
print("    int K dvol = 2 pi chi = pi/6      (Gauss-Bonnet)")
print("    For Kahler 3: K_kahler * Vol_kahler = (-2/3)(pi/2) = -pi/3")
print("    And int K_kahler dvol_kahler must equal 2 pi chi_kahler.")
print("    chi_kahler = chi(PSL(2,Z) \\ H) = -1/6 + corrections from ramification points.")

# The actual Euler characteristic via Gauss-Bonnet:
print()
print("="*68)
print("Gauss-Bonnet sanity check")
print("="*68)
print()
print("Gauss-Bonnet (closed surface): int K dvol = 2 pi chi.")
print("For PSL(2,Z) \\ H (orbifold): Riemann-Hurwitz / orbifold version.")
print()
print("Poincaré: int K_P dvol_P = (-1) * (pi/3) = -pi/3.")
print("=> chi_orb = -1/6.")
print()
print("Kähler 3: int K_K dvol_K = (-2/3) * (pi/2) = -pi/3.")
print("=> chi_orb = -1/6.   ✓ Same! (conformal invariance of int K dvol in 2-d)")
print()
print("KEY OBSERVATION: int K dvol is a CONFORMAL INVARIANT in 2-d.")
print("So any conformal rescaling K_phi -> c K_phi preserves int K dvol.")
print("=> Gauss-Bonnet does NOT distinguish Kähler 3 from Poincaré at integrated level.")
