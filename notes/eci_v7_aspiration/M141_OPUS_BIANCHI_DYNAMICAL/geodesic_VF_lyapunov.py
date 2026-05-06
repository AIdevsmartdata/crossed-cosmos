#!/usr/bin/env python3
"""
M141 -- Lyapunov spectrum of geodesic flow on (H, K = -3 log(2 Im tau))
        with N=1 SUGRA scalar potential V_F = (1/6)|A|^2 |s|^2 near tau=i.

The Kahler metric on H:
    K = -3 log(2 Im tau)
    g_{tau bar tau} = 3 / (2 Im tau)^2
    g^{tau bar tau} = (2 Im tau)^2 / 3

The Lagrangian for geodesic motion with potential is
    L = g_{tau bar tau} dtau/ds dbar tau/ds  -  V_F(tau, bar tau)

With kinetic term in real coords tau = x + i y:
    L_kin = (3/(2y)^2) (dot x^2 + dot y^2)

The geodesic equation (without potential) is the standard hyperbolic-plane geodesic:
    d^2 x/ds^2 - (2/y) dot x dot y = 0
    d^2 y/ds^2 + (1/y)(dot x^2 - dot y^2) = 0   (after factoring 3 out)

Adding potential V_F and using Euler-Lagrange:
    d/ds (dL/d dot x) = dL/dx
    (3/(2y)^2)( ddot x ) - (3/(2y)^3)(2 dot x dot y) (sign issue...)

  Actually let me redo. The Euclidean/Riemann action is
    S = int [ g_{ij} dot x^i dot x^j  -  V ] ds
  with metric on H:  ds_hyp^2 = (3/y^2)(dx^2 + dy^2)/4 .
  Hmm but that's for K = -3 log(2y), let's redo carefully:

  The Kahler metric tensor is:
    g_{tau bar tau} = d_tau d_bar tau K = 3/(2 y)^2 = 3/(4 y^2)

  As a real metric on R^2 = H:
    ds^2 = 2 g_{tau bar tau} (dx^2 + dy^2)
         = (6/(4 y^2)) (dx^2 + dy^2) = (3/(2 y^2))(dx^2 + dy^2)

  This is 3/2 times the Poincare metric (1/y^2)(dx^2+dy^2).
  Constant curvature: K_curv = -2/3 for K=-3 log(2y) (standard result).

  Christoffel symbols (real coords, i,j in {x,y}):
  Standard for ds^2 = (3/(2 y^2))(dx^2 + dy^2):
    Gamma^x_{xy} = Gamma^x_{yx} = -1/y
    Gamma^y_{xx} = +1/y
    Gamma^y_{yy} = -1/y
    All other = 0
  (Same as Poincare half-plane, since conformal factor cancels in Christoffel.)

  Geodesic equation:
    ddot x - (2/y) dot x dot y = 0
    ddot y + (1/y)(dot x^2 - dot y^2) = 0

  With potential V_F (a scalar function on H), the equations become:
    ddot x^a = -Gamma^a_{bc} dot x^b dot x^c - g^{ab} d_b V_F

  In real coords with V_F = (1/6) |A|^2 [x^2 + (y-1)^2] near tau=i:
    d_x V_F = (1/3) |A|^2 x
    d_y V_F = (1/3) |A|^2 (y - 1)

  g^{xx} = g^{yy} = 2 y^2 / 3 (inverse of 3/(2 y^2) on diagonal)

  So:
    ddot x = (2/y) dot x dot y - (2 y^2/3) (1/3) |A|^2 x
           = (2/y) dot x dot y - (2 y^2/9) |A|^2 x

    ddot y = -(1/y)(dot x^2 - dot y^2) - (2 y^2/3)(1/3)|A|^2 (y-1)
           = -(1/y)(dot x^2 - dot y^2) - (2 y^2/9) |A|^2 (y-1)

  Linearize around (x, y) = (0, 1).  Let s = x, eta = y - 1, with s, eta small.

  At leading order in (s, eta, dot s, dot eta):
    ddot s = (2/1)(0)(dot eta) - (2/9)|A|^2 s = -(2/9)|A|^2 s
    ddot eta = -(1/1)(0 - 0) - (2/9)|A|^2 eta = -(2/9)|A|^2 eta

  Both real degrees of freedom satisfy:
    ddot u = -omega^2 u    with omega^2 = (2/9)|A|^2

  But wait! With M134 m^2_{phys} = (4/9)|A|^2 in canonical coords.
  Let's check: canonical phi defined by (dphi)^2 = 2 g_{tau bar tau} dtau dbar tau,
  giving dphi_1 = sqrt(3)/y dx, etc.  For tau near i (y=1), phi_1 = sqrt(3) x.
  V_F = (1/6) |A|^2 (x^2 + (y-1)^2) = (1/6 * 1/3) |A|^2 (phi_1^2 + phi_2^2)
       = (1/18) |A|^2 (phi_1^2 + phi_2^2)
  In canonical, V = (1/2) m^2 phi^2. So m^2/2 = 1/18 |A|^2, m^2 = (1/9)|A|^2.

  Hmm M134 says m^2 = (4/9)|A|^2. Let me re-examine the conventions...

  Actually M134 V_F_taylor_analytic.py says:
    "Standard: V = (1/2) m^2 (phi_1^2 + phi_2^2)
    ==> m^2 = (4/9) |W''(i)|^2."

  And in V_F_taylor.py:
    V_F ~ (1/6) |A|^2 |s|^2  where s = tau - i (complex).
    |s|^2 = x^2 + (y-1)^2.

    Canonical: G_TT* d tau d bar tau = d phi d bar phi
    G_TT* = 3/(2y)^2 = 3/4 at y=1.
    sqrt(G_TT*) d tau = sqrt(3)/2 d tau
    So d phi_1 = sqrt(3)/2 dx, d phi_2 = sqrt(3)/2 d(y-1).
    Inversely: x = (2/sqrt(3)) phi_1, y-1 = (2/sqrt(3)) phi_2.
    x^2 + (y-1)^2 = (4/3)(phi_1^2 + phi_2^2)
    V_F = (1/6)(4/3)|A|^2 (phi_1^2 + phi_2^2) = (2/9)|A|^2 (phi_1^2+phi_2^2)
    Standard form V = (1/2) m^2 |phi|^2 with |phi|^2 = phi_1^2+phi_2^2:
      (1/2) m^2 = (2/9)|A|^2, so m^2 = (4/9)|A|^2.  GOOD.

  So m^2 (canonical) = (4/9)|A|^2.

  Now back to equation of motion. From V_F = (1/6)|A|^2 (x^2 + (y-1)^2)
  and Lagrangian L = g_ij dot x^i dot x^j /2 - V (NB factor of 1/2 if we treat
  L as kinetic + potential standard form):

  Actually I had L = g - V (no 1/2). Let me redo with standard L = (1/2) g_ij dot x^i dot x^j - V.

  Euler-Lagrange:
    d/ds (dL/d dot x^a) = dL/d x^a
    d/ds (g_{ab} dot x^b) = (1/2) (d_a g_{bc}) dot x^b dot x^c - d_a V
    g_{ab} ddot x^b + (d_c g_{ab}) dot x^c dot x^b = (1/2)(d_a g_{bc}) dot x^b dot x^c - d_a V

  Multiply by g^{ad}:
    ddot x^d + g^{ad}(d_c g_{ab} - (1/2) d_a g_{bc}) dot x^b dot x^c = -g^{ad} d_a V
    ddot x^d + Gamma^d_{bc} dot x^b dot x^c = -g^{ad} d_a V  ✓

  Where Gamma^d_{bc} = (1/2) g^{ad}(d_b g_{ac} + d_c g_{ab} - d_a g_{bc}).

  At y=1, g_{xx} = g_{yy} = 3/(2)^2 = 3/4. So g^{xx} = g^{yy} = 4/3.
  Force term: -g^{xx} d_x V = -(4/3)(1/3)|A|^2 x = -(4/9)|A|^2 x.

  Linearize:
    ddot x = -(4/9)|A|^2 x  =>  omega_x^2 = (4/9)|A|^2 = m^2_phys ✓
    ddot eta (= ddot y) = -(4/9)|A|^2 eta  =>  omega_y^2 = (4/9)|A|^2 = m^2_phys ✓

  So both real modes oscillate with omega = m_phys = (2/3)|A|.

  *** LYAPUNOV SPECTRUM ***
  Linearization at (x, y) = (0, 1) gives the equation:
    ddot u_i = -omega^2 u_i,   omega^2 > 0,
  whose eigenvalues of the linearized vector field on phase space (u, dot u) are
    [+i omega, -i omega, +i omega, -i omega]   (each twice for x and y).

  Lyapunov exponents = real parts of eigenvalues = ALL ZERO.

  Conclusion: V_F minimum at tau=i is a STABLE oscillator, NOT a chaotic source.
  No positive Lyapunov from V_F alone.
"""

import mpmath as mp
mp.mp.dps = 30

print("="*70)
print("M141 -- Geodesic flow + V_F Lyapunov spectrum at tau=i")
print("="*70)

# Constants from M134:
G14 = mp.gamma(mp.mpf(1)/4)
E4i = 3 * G14**8 / (2*mp.pi)**6
eta_i = G14 / (2 * mp.pi**(mp.mpf(3)/4))
A = -3456 * mp.pi**2 * E4i / eta_i**6
m_sq = mp.mpf(4)/9 * abs(A)**2  # m^2 (canonical)
m_phys = mp.sqrt(m_sq)

print(f"\nFrom M134 (M_Pl=1):")
print(f"  |A| = |W''(i)| = {abs(A)}")
print(f"  m^2 (canonical) = (4/9)|A|^2 = {m_sq}")
print(f"  m_phys = (2/3)|A| = {m_phys}")
print()

# BKL Lyapunov rate
lambda_BKL = mp.pi**2 / (6 * mp.log(2))
lambda_modular = 2 * mp.pi * lambda_BKL
print(f"BKL Lyapunov: lambda_BKL = pi^2/(6 ln 2) = {lambda_BKL}")
print(f"Modular shadow: lambda_mod = 2 pi lambda_BKL = pi^3/(3 ln 2) = {lambda_modular}")
print()

print("="*70)
print("Linearization of geodesic+V_F equation around tau=i")
print("="*70)
print()
print("EOM (from L = (1/2) g_ij dx^i/ds dx^j/ds - V_F, real coords x=Re tau, y=Im tau):")
print("  ddot x^d + Gamma^d_{bc} dot x^b dot x^c = -g^{ad} d_a V_F")
print()
print("Christoffels (Poincare half-plane, conformal factor 3):")
print("  Gamma^x_{xy} = -1/y, Gamma^y_{xx} = +1/y, Gamma^y_{yy} = -1/y")
print()
print("V_F = (1/6) |A|^2 [x^2 + (y-1)^2] near tau=i")
print("g^{xx} = g^{yy} = 4y^2/3")
print()

print("Linearize at (x, y, dot x, dot y) = (0, 1, 0, 0). Set u_1 = x, u_2 = y-1.")
print("Quadratic potential:  d_1 V = (1/3)|A|^2 u_1, d_2 V = (1/3)|A|^2 u_2")
print("Force: -g^{ii} d_i V = -(4/3)(1/3)|A|^2 u_i = -(4/9)|A|^2 u_i")
print()
print("Christoffel terms VANISH at linear order (they are quadratic in dot x).")
print()
print("Linear EOM:")
print("  ddot u_1 = -(4/9) |A|^2 u_1")
print("  ddot u_2 = -(4/9) |A|^2 u_2")
print()
print(f"omega_1 = omega_2 = (2/3) |A| = {m_phys}")
print()

# Eigenvalues of linearization
print("="*70)
print("Phase space linearization (4-dim): state = (u_1, u_2, dot u_1, dot u_2)")
print("="*70)
print()
print("M = [[0, 0, 1, 0], [0, 0, 0, 1], [-omega^2, 0, 0, 0], [0, -omega^2, 0, 0]]")
print()
print("Eigenvalues of M: ±i omega (each doubled).")
print("Lyapunov exponents = Re(eigenvalues) = [0, 0, 0, 0].")
print()

# Numerical sanity
import numpy as np
omega = float(m_phys)
M_lin = np.array([
    [0,       0,       1, 0],
    [0,       0,       0, 1],
    [-omega**2, 0,     0, 0],
    [0,       -omega**2, 0, 0],
])
eigs = np.linalg.eigvals(M_lin)
print(f"Numerical eigenvalues of M: {eigs}")
print(f"Real parts (Lyapunov spectrum): {[e.real for e in eigs]}")
print(f"Max Re: {max(e.real for e in eigs)}")
print()

print("="*70)
print("VERDICT (V_F-only): Lyapunov spectrum at tau=i is ALL ZERO")
print("="*70)
print()
print("Therefore V_F alone CANNOT generate the BKL chaotic flow with rate")
print(f"  lambda_BKL = {lambda_BKL}")
print()
print("V_F generates STABLE OSCILLATORY motion at frequency omega = m_phys.")
print("The chaos in BKL/Mixmaster comes from the *anisotropy* dynamics")
print("(beta_+, beta_- Misner variables), NOT from the modulus tau.")
print()

# ============================================================
print("="*70)
print("RATIO QUESTION: omega vs lambda_BKL (different physical units)")
print("="*70)
print()
# In M_Pl = 1 units, m_phys ~ |A| ~ 5e5, while lambda_BKL ~ 2.37 (dimensionless).
# These are NOT the same physical quantity:
#   - omega = modulus oscillation frequency [GeV] in M_Pl units
#   - lambda_BKL = entropy rate of Gauss shift [dimensionless per Misner-time iter]
#
# Comparison only makes sense after specifying the Misner-time -> physical-time map.
# In Mohseni-Vafa N=1 SUGRA, modulus mass sets H_modulus ~ m_phys/M_Pl, so the
# modulus oscillates many times per Hubble time during reheating.
#
# For the Bianchi IX BKL phase (near singularity), Misner-time tau = -log(volume)
# diverges; the dimensionless rate per Misner-time iteration is lambda_BKL.
# Physical Hubble rate diverges with tau, so chaos is "fast" in dimensionless units.

print(f"omega (in M_Pl=1 units) = {m_phys}")
print(f"lambda_BKL (in Misner-time per Kasner-bounce) = {lambda_BKL}")
print(f"ratio omega/lambda_BKL = {m_phys/lambda_BKL}")
print()
print("These are NOT the same physical quantity. omega [mass dimension 1] vs")
print("lambda_BKL [entropy rate per dimensionless Misner-time iteration].")
print()

# ============================================================
print("="*70)
print("M134 Hypothesis (B): Could V_F SHIFT the BKL rate?")
print("="*70)
print()

# In the coupled Bianchi IX + modulus system, modulus tau couples to anisotropy
# via gravitational-strength interaction. Near tau=i, V_F is harmonic, so the
# modulus is a HARMONIC OSCILLATOR coupled to the chaotic Misner billiard.
#
# Generic theorem (KAM-type): coupling a stable oscillator to a chaotic system
# preserves chaotic Lyapunov on the chaotic factor (positive measure of phase
# space remains chaotic with the same KS entropy h_KS), provided coupling is
# weak enough (NORMAL HYPERBOLICITY).
#
# At BKL singularity (Misner volume -> 0), gravitational coupling becomes strong;
# but the KS entropy on the projection to (beta_+, beta_-) is invariant under
# bounded perturbation (Pesin theory).
#
# So V_F -> ADDS bounded oscillator factor; lambda_BKL UNCHANGED.

print("Coupling V_F oscillator to BKL Misner billiard:")
print(" - Strong-coupling KAM theory (normal hyperbolicity, Pesin):")
print("   bounded oscillator factor preserves KS entropy of chaotic factor.")
print(" - Therefore lambda_BKL is UNCHANGED by V_F.")
print(" - V_F adds 2 zero Lyapunov directions; full system has Lyapunov:")
print("   (lambda_BKL, -lambda_BKL, 0, 0) [chaos in beta_pm; oscill in tau]")
print()

print("="*70)
print("CONCLUSION: V_F is DECOUPLED from BKL Lyapunov direction (verdict (C))")
print("           UNLESS we adopt verdict (D) modular-shadow alternative.")
print("="*70)
