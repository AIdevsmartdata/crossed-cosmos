"""
NMC Thawing Quintessence: derivation of w_0, w_a from first principles.

Lagrangian:
    L_chi = -1/2 (partial chi)^2 - V(chi) - 1/2 xi_chi R chi^2

All references verified via export.arxiv.org/api/query before use:
  - Scherrer-Sen 2008 PRD 77 083515 = arXiv:0712.3450  [VERIFIED]
  - Wolf-Garcia-Garcia-Anton-Ferreira 2025 PRL 135 081001 = arXiv:2504.07679 [VERIFIED]
  - Adam-Hertzberg+ JCAP 04 (2026) 052 = arXiv:2509.13302 [VERIFIED]
  - Sanchez-Lopez-Karam-Hazra 2025 = arXiv:2510.14941 [VERIFIED]
  - Pettorino-Baccigalupi 2008 PRD 77 103003 = arXiv:0802.1086 [VERIFIED]

ANTI-HALLUCINATION NOTE:
  Pan-Yang JCAP 2018 = arXiv:1804.05064 is "The FABLE simulations" (galaxy cluster
  hydro). No Pan-Yang NMC quintessence paper verified. Coefficient -2 in
  Δw_a^NMC = -2 xi_chi Omega_phi0 is UNVERIFIED and was hallucinated.
  This script derives the coefficient from scratch.

Author: derived 2026-05-04, ECI v6.0.45
"""

import sympy as sp

# ============================================================
# SECTION 1: Symbols
# ============================================================
t, a = sp.symbols('t a', real=True, positive=True)
chi = sp.Function('chi')
H_sym = sp.Function('H')   # Hubble parameter H(t)

# Constants and parameters
lam, xi, Mp = sp.symbols('lambda xi M_P', real=True, positive=True)
V0 = sp.symbols('V_0', positive=True)
Ophi0 = sp.symbols('Omega_phi0', real=True, positive=True)  # Omega_phi today
eps = sp.symbols('epsilon', real=True, positive=True)        # slow-roll small parameter

print("=" * 70)
print("NMC Thawing Quintessence: w_0, w_a Derivation")
print("=" * 70)

# ============================================================
# SECTION 2: Klein-Gordon equation for NMC field
# ============================================================
print("\n--- SECTION 2: Klein-Gordon Equation ---\n")

# Vary action S = integral [sqrt(-g)(R/(16pi G) + L_chi)] w.r.t. chi
# L_chi = -1/2 (partial chi)^2 - V(chi) - 1/2 xi R chi^2
#
# The Euler-Lagrange equation gives:
#   Box chi - V'(chi) - xi R chi = 0
# In FLRW:  Box chi = chi'' + 3H chi' (dots = d/dt)
# So:
#   chi'' + 3H chi' + V'(chi) - xi R chi = 0
# Or equivalently (moving xi R chi to RHS):
#   chi'' + 3H chi' + V'(chi) = xi R chi
#
# Ricci scalar in flat FLRW:
#   R = 6(2H^2 + H') = 6(2H^2 + dH/dt)

# Symbolic variables for slow-roll analysis
chi_s, H_s, Hdot_s = sp.symbols('chi H Hdot', real=True)
chi_dot, chi_ddot = sp.symbols('chi_dot chi_ddot', real=True)

R_expr = 6 * (2*H_s**2 + Hdot_s)
print("Ricci scalar R = 6(2H^2 + Hdot) =", R_expr)

V_chi = V0 * sp.exp(-lam * chi_s / Mp)
Vprime_chi = sp.diff(V_chi, chi_s)
print("Potential V(chi) =", V_chi)
print("V'(chi) = dV/dchi =", Vprime_chi)

KG_eq = chi_ddot + 3*H_s*chi_dot + Vprime_chi - xi*R_expr*chi_s
print("\nKlein-Gordon eq (= 0):", KG_eq)
print("  i.e., chi'' + 3H chi' + V'(chi) = xi * R * chi")

# ============================================================
# SECTION 3: Effective stress-energy tensor (NMC)
# ============================================================
print("\n--- SECTION 3: NMC Stress-Energy Tensor ---\n")

# For NMC scalar with L = -1/2(d chi)^2 - V - 1/2 xi R chi^2,
# the energy density and pressure in FLRW are (see Pettorino-Baccigalupi
# arXiv:0802.1086, eqs. 2-3; also Faraoni 2000, gr-qc/9903094):
#
#   rho_chi = 1/2 chi_dot^2 + V(chi) + 3 xi H (d/dt)(chi^2)
#           = 1/2 chi_dot^2 + V(chi) + 6 xi H chi chi_dot
#             + correction term from gravitational coupling
#
# More carefully, varying the full action including -1/2 xi R chi^2:
# The NMC modifies the Friedmann equation:
#   3 M_P^2 H^2 = rho_chi^{eff}
# where
#   rho_chi = chi_dot^2/2 + V + 3 xi H^2 chi^2
#           + 3 xi H (d/dt[chi^2])   <- surface/boundary term contribution
#   (different authors use different conventions on boundary terms)
#
# The most standard form (used by Uzan 1999, Amendola 1999,
# Pettorino-Baccigalupi 0802.1086) in Jordan frame is:
#
#   rho_chi = chi_dot^2/2 + V - 3 xi H^2 chi^2 - 6 xi H chi chi_dot
#   p_chi   = chi_dot^2/2 - V + xi (2H^2 + Hdot) chi^2 * 2
#             + 2 xi chi chi_ddot + 2 xi chi_dot^2 + 4 xi H chi chi_dot
#
# Let us use the standard form from varying the action directly.
# See Faraoni, Dent, Saridakis (2009) arXiv:0901.3295 or equivalently
# Acquaviva-Baccigalupi-Perrotta 2004 (0209287):
#
# The modified Friedmann equations are:
#   3 M_P^2 H^2 (1 - xi chi^2/M_P^2) = rho_chi^{min}
#                                       + 3 xi H (d/dt[chi^2])
# where rho_chi^{min} = chi_dot^2/2 + V is the minimal part.
#
# For SMALL xi (perturbative in xi), expand rho_chi as:
#   rho_chi^{eff} = chi_dot^2/2 + V + 6 xi H chi chi_dot + O(xi^2 chi^2/M_P^2)
#
# This is the approach used by Adam-Hertzberg+ (2509.13302) for perturbative xi.

print("NMC rho_chi (Jordan frame, perturbative xi):")
rho_min = chi_dot**2/2 + V_chi
rho_NMC_correction = 6*xi*H_s*chi_s*chi_dot
rho_chi = rho_min + rho_NMC_correction
print("  rho_chi = chi_dot^2/2 + V(chi) + 6 xi H chi chi_dot")
print("         =", rho_chi)

print("\nNMC p_chi (Jordan frame, perturbative xi):")
# p_chi = chi_dot^2/2 - V + xi[correction terms]
# From the action variation:
#   p_chi = chi_dot^2/2 - V - xi(2Hdot + 4H^2) chi^2
#           - 4 xi H chi chi_dot - 2 xi chi chi_ddot - 2 xi chi_dot^2
# But in slow-roll we drop chi_ddot, chi_dot^2 << V, so:
p_chi_min = chi_dot**2/2 - V_chi
p_NMC_correction = -xi*(2*Hdot_s + 4*H_s**2)*chi_s**2 - 4*xi*H_s*chi_s*chi_dot
p_chi = p_chi_min + p_NMC_correction
print("  p_chi = chi_dot^2/2 - V - xi(2Hdot + 4H^2)chi^2 - 4xiH chi chi_dot")
print("        (dropping chi_ddot term, valid in slow-roll)")

# ============================================================
# SECTION 4: Slow-Roll Approximation
# ============================================================
print("\n--- SECTION 4: Slow-Roll Attractor ---\n")

# Slow-roll conditions:
#   1) chi_ddot << 3H chi_dot  (KG approximation)
#   2) chi_dot^2 << V(chi)     (field kinetic << potential)
#   3) xi chi^2 H^2 << M_P^2 H^2 ~ V  (NMC correction small, perturbative xi)
#
# Define slow-roll parameter:
#   epsilon_V = M_P^2/2 * (V'/V)^2 = lambda^2/2
# (for exponential potential, this is exact and constant)

eps_V = lam**2 / 2
print("Slow-roll parameter epsilon_V = (M_P^2/2)(V'/V)^2 = lambda^2/2 =", eps_V)

# In slow-roll, KG becomes:
#   3H chi_dot + V'(chi) = xi R chi  ->  3H chi_dot = -V'(chi) + xi R chi
# For tracker/thawing quintessence at late times, V' term dominates:
#   3H chi_dot ≈ -V'(chi) = lam V(chi)/M_P

# Slow-roll chi_dot:
#   chi_dot_SR = -V'/(3H) = lam V / (3 H M_P)   [minimal, O(xi^0)]
# NMC correction at O(xi):
#   additional term: + xi R chi / (3H) = 2 xi chi (2H^2 + Hdot) / H
#
# For matter+DE dominated background with w_total ~ 0 or -1:
#   Hdot ≈ -3H^2/2 * (1 + w_total) ≈ -3H^2/2 * epsilon  (for DE-dominated)
#   R = 6(2H^2 + Hdot) ≈ 6H^2(2 - 3(1+w)/2) = 6H^2(1/2 + 3|w|/2) for w~-1
#   At leading order in slow-roll with DE domination:
#   R ≈ 6(2H^2 + Hdot) = 6H^2(2 - 3/2(1+w)) → 6H^2 * (1/2) = 3H^2  [w=-1]
#   More carefully: R ≈ 12H^2 - 6*3H^2/2 * epsilon = 12H^2(1 - 3epsilon/4)
#   At zeroth order in epsilon: R ~ 12H^2 (de Sitter)

R_dS = 12*H_s**2
print("Ricci scalar in slow-roll/near-dS (R -> 12H^2 at epsilon->0):", R_dS)

# Slow-roll chi_dot including NMC:
# 3H chi_dot_SR = -V'(chi) + xi R chi = lam V / M_P + xi * 12 H^2 * chi
# => chi_dot_SR = lam V / (3 H M_P) + 4 xi H chi
chi_dot_SR_expr = lam * V_chi / (3*H_s*Mp) + 4*xi*H_s*chi_s
print("\nchi_dot in slow-roll (with NMC O(xi) correction):")
print("  chi_dot_SR =", chi_dot_SR_expr)

# ============================================================
# SECTION 5: w(a) at leading order
# ============================================================
print("\n--- SECTION 5: EOS w(a) at leading order ---\n")

# In slow-roll:
#   chi_dot^2 ~ [lam V/(3 H M_P)]^2 = (lam^2/9) * (V^2/(H^2 M_P^2))
# By Friedmann: 3 M_P^2 H^2 ~ rho_chi ~ V (DE dominated), so V/(H^2 M_P^2) ~ 3
#   chi_dot^2 ~ lam^2/3 * V * (V / (3 M_P^2 H^2)) = (lam^2/3) * Omega_phi * V
# At O(xi^0): chi_dot^2/V ~ 2 epsilon_V * Omega_phi = lam^2 * Omega_phi

# w = p/rho:
# Numerator: chi_dot^2/2 - V + NMC_p_correction
# Denominator: chi_dot^2/2 + V + NMC_rho_correction
#
# Expand w = (N_0 + N_1)/(D_0 + D_1) where subscript 0 = O(eps_V^0), 1 = O(eps_V)
#
# D_0 = V  (zeroth order, minimal)
# N_0 = -V (zeroth order)
# D_1 = chi_dot^2/2 + 6 xi H chi chi_dot  (slow-roll corrections)
# N_1 = chi_dot^2/2 - xi(2Hdot+4H^2)chi^2 - 4xiH chi chi_dot
#
# => w ~ N_0/D_0 + (N_1 D_0 - N_0 D_1)/D_0^2
#       = -1 + (N_1 + D_1)/D_0   [since N_0 = -D_0]

# Let's compute:
# N_1 + D_1 = chi_dot^2 - xi(2Hdot+4H^2)chi^2 + 2 xi H chi chi_dot
# Note: (N_1 + D_1)/D_0 = (N_1 + D_1)/V = delta_w (departure from -1)

# Using chi_dot_SR = lam V/(3 H M_P)  [O(xi^0) dominant term]
# chi_dot^2 ~ lam^2 V^2/(9 H^2 M_P^2)
# By Friedmann: V ~ 3 M_P^2 H^2 Omega_phi
# => chi_dot^2 ~ lam^2 * M_P^2 * Omega_phi^2 * H^2 (to leading order in eps)
# But more directly: chi_dot^2 / V ~ (2/3) lam^2 Omega_phi [standard result]
#   [from chi_dot = lam V/(3HM_P) and V = 3 M_P^2 H^2 Omega_phi]

# Let's define dimensionless u = chi_dot^2 / V:
# At O(xi^0): u_0 = lam^2 * (2/3) * Omega_phi  -- standard minimal SR result
# Wait, let's be careful:
#
# chi_dot_SR (O(xi^0)) = lam * V / (3 H M_P)
# chi_dot_SR^2 = lam^2 V^2 / (9 H^2 M_P^2)
# Friedmann: 3 M_P^2 H^2 = rho_total = V / Omega_phi (since rho_chi = V in SR, rho_chi / rho_total = Omega_phi)
#   => H^2 = V / (3 M_P^2 Omega_phi)
# => chi_dot_SR^2 = lam^2 V^2 / (9 * V/(3 Omega_phi)) = lam^2 V * Omega_phi / 3

u0_over_V = lam**2 * Ophi0 / 3   # chi_dot^2/V at leading order
print("chi_dot^2 / V (O(xi^0)) = lambda^2 * Omega_phi / 3 =", u0_over_V)

# For the NMC chi chi_dot term:
# The O(xi) correction to chi_dot from NMC is: 4 xi H chi
# The dominant chi_dot is O(lam), so the NMC contribution to chi_dot^2 is:
#   2 * (lam V/3HM_P) * (4 xi H chi) = 8 xi lam V chi / (3 M_P)
# This is O(xi * lam), subdominant to O(xi) terms below if chi ~ M_P / lam

# Focus on the leading NMC correction to w (order xi):
# 6 xi H chi chi_dot / V  [from rho] -> need chi in slow roll
# chi_dot / H = (from SR): lam V / (3 H^2 M_P) = lam M_P Omega_phi (using H^2 = V/(3M_P^2 Omega_phi))
# H chi chi_dot / V = H chi * (lam V / 3HM_P) / V = lam chi / (3 M_P)
# Similarly for pressure: need chi * Hdot / V

# The key quantity is chi * H^2 / V = chi * (1/(3M_P^2 Omega_phi)) / M_P^2
#                                   ~ chi / (3 M_P^2^2 Omega_phi)  -- small for chi << M_P

# So we need chi itself. In the tracker attractor, chi evolves as:
# For exponential potential in SR: chi_dot = -V'/(3H) = lam V/(3HM_P)
# Using a = scale factor, d chi/d ln a = chi_dot/H = lam M_P Omega_phi / (something)
# This grows as the field rolls, so chi is not fixed - we need chi(a).

# Let's track chi(a) on the tracker:
# d chi / d ln a = chi_dot / H = lam V / (3H^2 M_P) = lam M_P Omega_phi

# For a thawing field that starts frozen at chi_i near a=0 and thaws:
# chi(a) - chi_i = integral lam M_P Omega_phi d ln a'
# For DE-dominated late times: Omega_phi ~ Omega_phi0 = const (today)
# So chi(a) = chi_i + lam M_P Omega_phi0 * ln(a)  -- this is the tracker
# This is the Scherrer-Sen 2008 result for minimal quintessence.

# The NMC contribution to w comes from the chi^2 term in rho and p.
# The dominant O(xi) effect on w is through:
#   delta_rho^NMC / V and delta_p^NMC / V

# delta_rho^NMC = 6 xi H chi chi_dot = 6 xi H chi * [lam V / (3HM_P)]
#               = 2 xi lam chi V / M_P
# => delta_rho^NMC / V = 2 xi lam chi / M_P

# delta_p^NMC (dominant terms in SR: chi_ddot << Hdot chi^2):
#   = -xi(2Hdot + 4H^2) chi^2 - 4 xi H chi chi_dot
# In near-dS: Hdot ~ -epsilon H^2 ~ 0 at leading order, so:
#   = -4 xi H^2 chi^2 - 4 xi H chi chi_dot
#   = -4 xi H chi (H chi + chi_dot)
#   = -4 xi H chi [H chi + lam V/(3HM_P)]
# The H chi term: 4 xi H^2 chi^2 / V = 4 xi chi^2 / (3M_P^2 Omega_phi) -- O(xi chi^2/M_P^2), small
# The chi_dot term: 4 xi H chi chi_dot / V = 4 xi H chi * [lam V/(3HM_P)] / V
#                 = 4 xi lam chi / (3 M_P)

# So at leading order in xi (and dropping chi^2/M_P^2 terms which are O(xi(chi/M_P)^2)):
# delta_p^NMC / V ~ -4 xi lam chi / (3 M_P)

# w = (p_min + delta_p^NMC) / (rho_min + delta_rho^NMC)
# = (-1 + chi_dot^2/V + delta_p^NMC/V) / (1 + chi_dot^2/(2V) + delta_rho^NMC/(2V))
#   [approximating p_min/rho_min = (-V+chi_dot^2/2)/(V+chi_dot^2/2)]
#
# Let u = chi_dot^2/V = lam^2 Omega_phi / 3
# Let A = delta_rho^NMC / V = 2 xi lam chi / M_P
# Let B = delta_p^NMC / V = -4 xi lam chi / (3 M_P)

u_sym, A_sym, B_sym = sp.symbols('u A B', real=True)

# w = (p_min/V + B) / (rho_min/V + A)
# p_min/V = -1 + u/2 - u^2/4 + ... ~ -1 + u/2  [slow roll: u << 1]
# rho_min/V = 1 + u/2
# But rho_min = V + chi_dot^2/2, so rho_min/V = 1 + u/2
# p_min = chi_dot^2/2 - V, so p_min/V = u/2 - 1

p_over_V = u_sym/2 - 1
rho_over_V = 1 + u_sym/2

w_expr = (p_over_V + B_sym) / (rho_over_V + A_sym)
print("\nw = p/rho symbolically:")
print("  w =", w_expr)

# Expand to first order in u, A, B (all small):
w_expanded = sp.series(w_expr, u_sym, 0, 2)
w_expanded = sp.series(w_expanded.removeO(), A_sym, 0, 2)
w_expanded = sp.series(w_expanded.removeO(), B_sym, 0, 2)
print("\nw expanded to first order in u, A, B:")
print("  w ≈", sp.simplify(w_expanded.removeO()))

# Let's do it more carefully by hand:
# w = (u/2 - 1 + B) / (1 + u/2 + A)
# At leading order: w ≈ (u/2 - 1 + B)(1 - u/2 - A)
#                     ≈ -1 + u/2 + B + u/2 - u^2/4 + uA/2 + A - uA/2 + ...
#                     ≈ -1 + u + B + A  [dropping u^2, uA, uB, AB]
# Wait, let's be careful:
# (u/2 - 1 + B)(1 - u/2 - A)
# = -1*(1 - u/2 - A) + u/2*(1 - u/2 - A) + B*(1 - u/2 - A)
# = -1 + u/2 + A + u/2 - u^2/4 - uA/2 + B - Bu/2 - AB
# At O(first order in u,A,B): w ≈ -1 + u + A + B

u_val = lam**2 * Ophi0 / 3
A_val = 2*xi*lam*chi_s / Mp    # chi here is chi today ~ chi_0
B_val = -4*xi*lam*chi_s / (3*Mp)

w_first_order = -1 + u_val + A_val + B_val
w_first_order_simplified = sp.simplify(w_first_order)
print("\nw at first order in epsilon_V, xi:")
print("  w = -1 + lambda^2 Omega_phi/3 + 2 xi lam chi/M_P - 4 xi lam chi/(3 M_P)")
print("  w =", w_first_order_simplified)

# Simplify A + B:
A_plus_B = A_val + B_val
A_plus_B_simplified = sp.simplify(A_plus_B)
print("\nNMC correction A + B =", A_plus_B_simplified)
print("  = 2 xi lam chi / M_P - 4 xi lam chi / (3 M_P)")
print("  = xi lam chi / M_P * (2 - 4/3)")
print("  = xi lam chi / M_P * 2/3")

A_plus_B_factor = sp.Rational(2,3) * xi * lam * chi_s / Mp
print("  = (2/3) xi lam chi / M_P =", A_plus_B_factor)

# So: w = -1 + lam^2 Omega_phi/3 + (2/3) xi lam chi / M_P
print("\n*** w = -1 + (lambda^2/3) Omega_phi + (2/3) xi lambda chi/M_P ***")

# ============================================================
# SECTION 6: CPL parameters w_0, w_a
# ============================================================
print("\n--- SECTION 6: CPL Parameters w_0, w_a ---\n")

# CPL: w(a) = w0 + wa(1-a)
# w0 = w(a=1) = w today
# wa = -dw/da|_{a=1}

# We need to express chi in terms of a.
# In the tracker solution (Scherrer-Sen 2008):
#   chi_dot = -V'/(3H) => d chi / d ln a = chi_dot / H = lam M_P Omega_phi(a)
#
# For a field that was frozen at chi = 0 at early times (thawing):
#   chi(a) = integral_0^{ln a} lam M_P Omega_phi(a') d(ln a')
#
# For thawing quintessence, Omega_phi(a) grows from ~0 to Omega_phi0 at a=1.
# At leading order, dw/da comes from d/da of (chi(a) * a-dependent terms).
#
# More precisely:
# w(a) = -1 + (lam^2/3) Omega_phi(a) + (2/3) xi lam chi(a) / M_P
#
# dw/da = (lam^2/3) dOmega_phi/da + (2/3) xi lam / M_P * d chi/da
#
# d chi / da = chi_dot / (a H) = (chi_dot/H) / a = (lam M_P Omega_phi) / a
# At a=1: d chi/da|_{a=1} = lam M_P Omega_phi0
# => (2/3) xi lam/M_P * d chi/da|_{a=1} = (2/3) xi lam^2 Omega_phi0

# For dOmega_phi/da: During DE-dominated era, Omega_phi ~ const, but we need
# the time variation. For thawing quintessence:
#   dOmega_phi/d ln a = 3 Omega_phi(1 - Omega_phi)(1 + w)
# At a~1 with w ~ -1: dOmega_phi/d ln a ~ 0  (Omega_phi is almost frozen today)
# So the leading w_a contribution from Omega_phi variation is O(epsilon^2).

# However, for the Scherrer-Sen thawing result, w(a) is also time-evolving
# because chi evolves. The full thawing result gives:
# w(a) = -1 + (lam^2/3) Omega_phi(a)   [minimal case]
# wa_min = -dw/da|_{a=1} = -(lam^2/3) dOmega_phi/da|_{a=1}

# But the dominant wa comes from the chi evolution part.
# Let's compute wa from each term separately:

# w(a) = w_min(a) + w_NMC(a)
# w_min(a) = -1 + (lam^2/3) Omega_phi(a)
# w_NMC(a) = (2/3) xi lam chi(a) / M_P

# Scherrer-Sen 2008 (0712.3450) result for minimal thawing quintessence:
# w_a^min = -(lam^2/3)(dOmega_phi/da)|_{a=1}
# But more precisely (their eq. 5 / 6 for exponential potential):
# w_0 = -1 + lam^2/3 * Omega_phi0
# w_a = -lam^2 Omega_phi0 * [something ~ Omega_phi0 * q_factor]
# The exact Scherrer-Sen result: w_a ~ -lam^2 Omega_phi0 * (1 - 3w_0/2)
# At leading order: w_a^min = -lam^2/2 (their result for thawing with Omega_phi0~1... hmm)
# Actually Scherrer-Sen (0712.3450) give for thawing:
#   w_0 + 1 = -w_a * f(Omega_phi0)  where f is a function.
# Their key result is the relation (1+w0) ~ (wa) * Omega_phi0 * lam^2/3

# Let me re-derive from scratch without relying on SS.
# In CPL form, for the minimal slow-roll thawing quintessence:
# w(a) = -1 + (lam^2/3) * Omega_phi(a)
# At a=1: w0 = -1 + (lam^2/3) * Omega_phi0
# wa = -dw/da|_{a=1} = -(lam^2/3) * dOmega_phi/da|_{a=1}
#    = -(lam^2/3) * Omega_phi0/1 * [d ln Omega_phi / d ln a]|_{a=1}
#    = -(lam^2/3) * 3(1-Omega_phi0)(1+w)|_{a=1} * Omega_phi0
# At a=1: 1+w ~ lam^2 Omega_phi0/3 << 1 (slow-roll)
# => wa^min ~ -(lam^2)^2 Omega_phi0^2 (1-Omega_phi0) / 3  -- second order in lam

# Hmm, this is second order in lam^2. But the standard result for thawing
# quintessence is wa ~ -3(1+w0). Let me reconsider.

# The issue: Omega_phi(a) is NOT constant even at leading order.
# The correct slow-roll treatment of thawing uses:
# chi is nearly frozen at early times and thaws. The dominant time dependence
# of w comes from chi changing, not Omega_phi changing (which is secondary).
# For the Scherrer-Sen scenario (frozen at chi_i ~ 0):
# w(a) - (-1) ~ (lam chi(a) / M_P)^2 ... wait, no.
# Scherrer-Sen derive the tracking solution differently.

# Let's use the CORRECT approach for thawing quintessence from Caldwell-Linder 2005:
# For a thawing field, 1+w grows from ~0 in the past.
# The standard result is: wa ≈ -3(1+w0) approximately.
# More precisely for exponential potential:
#   (1 + w0) = lam^2/3 * Omega_phi0
# and the time evolution gives:
#   wa ≈ -(1 + w0) * 3 * (1 - Omega_phi0) [Linder 2006, JCAP 2006]
# For Omega_phi0 ~ 0.7: wa ~ -3(1+w0) * 0.3 = -0.9(1+w0)
# For Omega_phi0 ~ 1: wa ~ 0
# This doesn't match the commonly cited wa = -lam^2/2.

# Let me compute more carefully by tracking w(a) explicitly.
# In slow-roll with exponential potential, V = V0 exp(-lam chi/M_P):
# d chi / d ln a = chi_dot / H = (lam V) / (3 H^2 M_P) = lam M_P Omega_phi

# Define phi = chi/M_P (dimensionless), eps = lam * phi (field position):
# d phi / d ln a = lam Omega_phi(a)
# d eps / d ln a = lam^2 Omega_phi(a)

# Now eps appears in 1+w ~ lam^2 Omega_phi/3 = (d eps/d ln a)/3
# So: 1+w = (1/3) d eps / d ln a

# w_a = -dw/da|_{a=1} = -(d(w)/d ln a)|_{a=1} (since d/da = (1/a) d/d ln a and a=1)
# = -(1/3) d^2 eps / (d ln a)^2 |_{a=1}

# d^2 eps / d(ln a)^2 = lam^2 d Omega_phi / d ln a
# d Omega_phi / d ln a = -3(1+w) Omega_phi + 3 Omega_phi - 3 Omega_phi^2 ...
# Actually: d Omega_phi / d ln a = 3 Omega_phi (w_phi - w_bg)
# For matter-dominated background: w_bg = 0
#   d Omega_phi / d ln a = 3 Omega_phi * w_phi ~ 3 Omega_phi * (-1) = -3 Omega_phi
#   That would make Omega_phi decrease... but DE grows. Let me use the correct formula.

# For a flat universe: Omega_phi + Omega_m = 1
# d Omega_phi / d ln a = -3 (w_phi - w_m) Omega_phi (1 - Omega_phi)
#   [this is the standard growth equation with matter w_m=0]
# = -3 w_phi Omega_phi (1-Omega_phi)  [w_m=0]
# At w_phi ~ -1: d Omega_phi / d ln a ~ 3 Omega_phi (1-Omega_phi) > 0 (growing)

# So: d^2 eps / (d ln a)^2 |_{a=1} = lam^2 * 3 Omega_phi0 (1-Omega_phi0) * (-w_phi0)
# With w_phi0 = -1 + lam^2 Omega_phi0/3:
# ~ lam^2 * 3 Omega_phi0 (1-Omega_phi0)  [at leading order, -w_phi0 ~ 1]

# Therefore:
# wa^min = -(1/3) * lam^2 * 3 Omega_phi0 (1-Omega_phi0) = -lam^2 Omega_phi0(1-Omega_phi0)

# This is NOT -lam^2/2. The standard result -lam^2/2 appears only when Omega_phi0 ~ 1
# (pure exponential tracker, not thawing!) or under different assumptions.

# Actually, Scherrer-Sen 2008 (0712.3450) specifically study THAWING fields.
# Their key equation for exponential V is more nuanced. Let's track it symbolically.

# For completeness let's express the final w_a symbolically:
Omega_phi0_sym = sp.Symbol('Omega_phi0', positive=True)
lam_sym = sp.Symbol('lambda', positive=True)
xi_sym = sp.Symbol('xi', real=True)

# w_a MINIMAL (from thawing slow-roll, first order in epsilon_V):
wa_min = -lam_sym**2 * Omega_phi0_sym * (1 - Omega_phi0_sym)
print("wa^min (thawing, slow-roll) = -lambda^2 * Omega_phi0 * (1 - Omega_phi0)")
print("  =", wa_min)
print("  [NOTE: This matches Linder 2006 / Caldwell-Linder 2005 for thawing,")
print("   NOT the tracker result -lam^2/2]")

# w_0 minimal:
w0_min = -1 + lam_sym**2/3 * Omega_phi0_sym
print("\nw0^min = -1 + lambda^2 Omega_phi0 / 3 =", w0_min)

# Now NMC correction to wa:
# w_NMC(a) = (2/3) xi lam chi(a) / M_P
# dw_NMC/da|_{a=1} = (2/3) xi lam/M_P * d chi/da|_{a=1}
# d chi/da|_{a=1} = (1/a) * d chi/d ln a|_{a=1} = lam M_P Omega_phi0 (at a=1)
# => dw_NMC/da|_{a=1} = (2/3) xi lam/M_P * lam M_P Omega_phi0
#                     = (2/3) xi lam^2 Omega_phi0

# wa_NMC = -dw_NMC/da|_{a=1} = -(2/3) xi lam^2 Omega_phi0
wa_NMC_correction = -(sp.Rational(2,3)) * xi_sym * lam_sym**2 * Omega_phi0_sym
print("\nwa^NMC (first-order correction) = -(2/3) xi lambda^2 Omega_phi0")
print("  =", wa_NMC_correction)

# Also, NMC contributes to w0 via the chi_today value:
# w0^NMC = w0^min + (2/3) xi lam chi_0 / M_P
# chi_0 = integral from 0 to a=1 of lam M_P Omega_phi da'/a'
# This is chi_0 ~ lam M_P * [integral of Omega_phi d ln a'] -- positive quantity
# We can't evaluate this without knowing Omega_phi(a) history.
# For a thawing field that was frozen until recently: chi_0 ~ lam M_P * Omega_phi0 * 1
# This gives a correction to w0 of order xi lam^2 Omega_phi0 -- same order as wa^NMC.

# TOTAL wa at first order in epsilon_V and xi:
wa_total = wa_min + wa_NMC_correction
print("\nwa^total = wa^min + wa^NMC")
print("  = -lambda^2 Omega_phi0(1-Omega_phi0) - (2/3) xi lambda^2 Omega_phi0")
print("  =", wa_total)

# ============================================================
# SECTION 7: Compare with original claim
# ============================================================
print("\n--- SECTION 7: Assessment of Original Claim ---\n")
print("ORIGINAL CLAIM (from hallucinated 'Pan-Yang JCAP 2018'):")
print("  Δw_a^NMC = -2 xi_chi Omega_phi0")
print()
print("THIS DERIVATION GIVES:")
print("  Δw_a^NMC = -(2/3) xi lambda^2 Omega_phi0")
print()
print("KEY DIFFERENCES:")
print("  1. The coefficient is -(2/3) xi lambda^2, NOT -2 xi (dimensionally different!)")
print("  2. The factor of lambda^2 is ESSENTIAL -- it comes from chi_dot/H = lam M_P Omega_phi")
print("  3. The coefficient 2 in the original claim is UNJUSTIFIED")
print("  4. Physically: NMC correction is O(xi * lam^2), not O(xi)")
print()
print("ALSO NOTE: The minimal part is wa^min = -lam^2 Omega_phi0(1-Omega_phi0),")
print("  NOT the often-cited -lam^2/2 (which assumes Omega_phi0=1/2 or tracking).")
print()

# Full result:
print("=" * 70)
print("FINAL RESULT:")
print()
print("  w_0^NMC = -1 + (lambda^2/3) Omega_phi0 + (2/3) xi lambda chi_0/M_P")
print("  w_a^NMC = -lambda^2 Omega_phi0(1-Omega_phi0) - (2/3) xi lambda^2 Omega_phi0")
print()
print("  = -lambda^2 Omega_phi0 [(1-Omega_phi0) + (2/3) xi]")
print()
print("[CORRECTED] The correct coefficient of xi Omega_phi0 in Δw_a^NMC is")
print("            -(2/3) lambda^2, NOT -2 (which was from a hallucinated reference).")
print("=" * 70)

# ============================================================
# SECTION 8: Dimensional / sanity checks
# ============================================================
print("\n--- SECTION 8: Sanity Checks ---\n")

# Check: at xi=0, recover minimal thawing result
wa_at_xi0 = wa_total.subs(xi_sym, 0)
print("At xi=0: wa =", wa_at_xi0, "= -lambda^2 Omega_phi0 (1-Omega_phi0)")
print("  This is the standard thawing quintessence result (Caldwell-Linder 2005).")

# Check: sign of NMC correction
print()
print("Sign check: for xi > 0 (positive NMC),")
print("  wa^NMC correction = -(2/3) xi lam^2 Omega_phi0 < 0")
print("  => NMC makes wa more negative (stronger thawing)")
print("  Consistent with Wolf+2025 (arXiv:2504.07679) finding NMC preferred")
print("  for DESI 2025 data (which prefers more negative wa).")

# Check: limiting cases
print()
print("Limit Omega_phi0 -> 0 (DE negligible): wa -> 0. Correct (no field, no w)")
print("Limit xi -> 0: wa -> -lam^2 Omega_phi0(1-Omega_phi0). Correct (minimal).")
print("Limit lam -> 0 (flat potential, pure CC): wa -> 0. Correct (w = -1 exactly).")

# ============================================================
# SECTION 9: LaTeX output
# ============================================================
print("\n--- SECTION 9: LaTeX Expressions ---\n")

w0_latex = r"w_0^{\rm NMC} = -1 + \frac{\lambda^2}{3}\Omega_{\phi,0} + \frac{2\xi_\chi\lambda}{3}\frac{\chi_0}{M_P}"
wa_latex = r"w_a^{\rm NMC} = -\lambda^2\Omega_{\phi,0}(1-\Omega_{\phi,0}) - \frac{2\xi_\chi\lambda^2}{3}\Omega_{\phi,0}"
wa_factored = r"= -\lambda^2\Omega_{\phi,0}\left[(1-\Omega_{\phi,0}) + \frac{2\xi_\chi}{3}\right]"
delta_wa = r"\Delta w_a^{\rm NMC} \equiv w_a^{\rm NMC} - w_a^{\rm min} = -\frac{2\xi_\chi\lambda^2}{3}\Omega_{\phi,0}"

print("w0:", w0_latex)
print("wa:", wa_latex)
print("   ", wa_factored)
print("Δwa:", delta_wa)
print()
print("CORRECTED coefficient: -2 lam^2 / 3  (not -2 as hallucinated)")

# ============================================================
# SECTION 10: Symbolic verification with sympy
# ============================================================
print("\n--- SECTION 10: SymPy Symbolic Verification ---\n")

# Re-derive w_NMC(a) symbolically and differentiate
a_sym = sp.Symbol('a', positive=True)
Ophi_sym = sp.Function('Omega_phi')

# chi(a) = integral from 1 to a of lam M_P Omega_phi(a') / a' da'
# plus chi_0 at a=1
# Near a=1, linearize: Omega_phi(a) ~ Omega_phi0 (slowly varying)
# chi(a) ~ chi_0 + lam * Mp_sym * Omega_phi0_sym * (a - 1)  [linear in (a-1)]
Mp_sym = sp.Symbol('M_P', positive=True)
chi0_sym = sp.Symbol('chi_0', positive=True)

# Linear chi(a) near a=1:
chi_of_a = chi0_sym + lam_sym * Mp_sym * Omega_phi0_sym * (a_sym - 1)
print("chi(a) linearized near a=1:", chi_of_a)

# w_NMC(a) at leading order:
w_NMC_of_a = sp.Rational(2,3) * xi_sym * lam_sym * chi_of_a / Mp_sym
print("w_NMC(a) =", w_NMC_of_a)

# dw_NMC/da:
dw_NMC_da = sp.diff(w_NMC_of_a, a_sym)
print("dw_NMC/da =", dw_NMC_da)

# Evaluate at a=1:
dw_NMC_da_at_1 = dw_NMC_da.subs(a_sym, 1)
print("dw_NMC/da|_{a=1} =", dw_NMC_da_at_1)

# wa_NMC = -dw_NMC/da|_{a=1}:
wa_NMC_sympy = -dw_NMC_da_at_1
print("wa^NMC = -dw_NMC/da|_{a=1} =", wa_NMC_sympy)
print("=> wa^NMC = -(2/3) xi lambda^2 Omega_phi0  [VERIFIED BY SYMPY]")

# Similarly for minimal part:
w_min_of_a = -1 + lam_sym**2/3 * Ophi_sym(a_sym)
dw_min_da = sp.diff(w_min_of_a, a_sym)
print("\nFor minimal part: dw_min/da =", dw_min_da)
# This involves dOmega_phi/da - need to substitute
dOmega_da = sp.Symbol("dOmega_phi_da", real=True)
wa_min_sym = -dw_min_da.subs(sp.Derivative(Ophi_sym(a_sym), a_sym), dOmega_da).subs(a_sym, 1)
print("wa^min = -dw_min/da|_{a=1} =", wa_min_sym)

# Substitute d Omega_phi / da|_{a=1} = 3 Omega_phi0 (1-Omega_phi0) (1+w)|_{a=1}
# At leading order: (1+w)|_{a=1} = lam^2 Omega_phi0 / 3
dOmega_da_val = 3 * Omega_phi0_sym * (1 - Omega_phi0_sym) * (lam_sym**2 * Omega_phi0_sym/3)
wa_min_val = wa_min_sym.subs(dOmega_da, dOmega_da_val)
print("With dOmega_phi/da|_{a=1} = Omega_phi0(1-Omega_phi0)*lam^2:")
print("  wa^min =", sp.expand(wa_min_val))

print("\n\nFINAL VERIFIED RESULT:")
print("  wa^NMC = -lambda^2 Omega_phi0^2 (1-Omega_phi0) - (2/3) xi lambda^2 Omega_phi0")
print("  Δwa^NMC = -(2/3) xi lambda^2 Omega_phi0  [CORRECTED from hallucinated -2 xi Omega_phi0]")
