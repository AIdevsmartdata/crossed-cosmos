"""
Diagnose why lnH_today = -34.5 instead of 0.
Step through integration and see where it goes wrong.
"""
import numpy as np
from scipy.integrate import solve_ivp

h = 0.6774
Omega_m = 0.1432 / h**2
Omega_r = 4.15e-5 / h**2  # correct: Omega_r = omega_r_phys/h^2
Omega_L = 1.0 - Omega_m - Omega_r
V0 = 3.0 * Omega_L
print(f"Omega_m={Omega_m:.4f}, Omega_r={Omega_r:.4e}, V0={V0:.4f}")

def rhs_with_print(N, state, xi=0.1):
    phi, phi_p, lnH = state
    H2 = np.exp(2.*lnH)
    if not np.isfinite(H2) or H2 < 1e-30:
        return [0., 0., 0.]
    rho_m = 3.*Omega_m*np.exp(-3.*N)
    rho_r = 3.*Omega_r*np.exp(-4.*N)
    F = 1.-xi*phi**2; FP = -2.*xi*phi; FPP = -2.*xi
    V = V0; VP = 0.
    N_sH = (-rho_m/H2 - (4./3.)*rho_r/H2 - (2.*V)/H2
            + FP*phi_p + 6.*FP**2 + FPP*phi_p**2)
    D_sH = 2.*F - 3.*FP**2
    if abs(D_sH) < 1e-10: D_sH = 1e-10
    s_H = N_sH / D_sH
    phi_pp = -(3.+s_H)*phi_p - VP/H2 - 6.*xi*phi*(2.+s_H)
    return [phi_p, phi_pp, s_H]

# Track N and lnH values
N_init = -5.0
rho_m_i = 3.*Omega_m*np.exp(-3.*N_init)
rho_r_i = 3.*Omega_r*np.exp(-4.*N_init)
H2_i = (rho_m_i + rho_r_i + V0)/3.
lnH_i = 0.5*np.log(H2_i)
state0 = [0.01, 0.0, lnH_i]

print(f"\nN_init={N_init}, lnH_i={lnH_i:.4f}")

# Track evolution in checkpoints
eval_pts = np.array([-5., -4., -3., -2., -1., 0.])
sol = solve_ivp(lambda N, s: rhs_with_print(N, s, 0.1),
                [N_init, 0.0], state0, method='LSODA',
                rtol=1e-6, atol=1e-8,
                t_eval=eval_pts, max_step=0.1)
print(f"\nLSODA success: {sol.success}, msg: {sol.message}")
if sol.t.size > 0:
    for i, N in enumerate(sol.t):
        phi = sol.y[0,i]; phi_p = sol.y[1,i]; lnH = sol.y[2,i]
        # Cross-check: compute what lnH SHOULD be from Friedmann
        F = 1.-0.1*phi**2; FP = -2.*0.1*phi
        rho_m = 3.*Omega_m*np.exp(-3.*N)
        rho_r = 3.*Omega_r*np.exp(-4.*N)
        denom_f = 3.*F + 3.*FP*phi_p - 0.5*phi_p**2
        if denom_f > 0:
            H2_frid = (rho_m + rho_r + V0) / denom_f
            lnH_frid = 0.5*np.log(H2_frid)
        else:
            lnH_frid = float('nan')
        print(f"  N={N:.1f}: phi={phi:.6f}, lnH_ode={lnH:.4f}, lnH_friedmann={lnH_frid:.4f}, discrepancy={lnH-lnH_frid:.4f}")

# The problem: our lnH equation (d lnH/dN = s_H) integrates lnH independently.
# But H must also satisfy the Friedmann constraint at each step.
# If s_H is wrong, lnH drifts away from the Friedmann constraint.
# Solution: instead of integrating lnH as a free ODE variable,
# ENFORCE Friedmann at each step to compute H^2 directly.
# This is the "reduced" or "constraint-enforced" ODE:
#   phi'' = -(3+s_H)*phi' - VP/H^2 - 6*xi*phi*(2+s_H)
#   where H^2 is COMPUTED from Friedmann, not from integrating lnH.
# But then we need phi'' explicitly in terms of phi, phi', and H^2,
# which requires knowing s_H first.

print("\n--- Constraint-enforced approach ---")
print("Instead of integrating lnH, compute H^2 directly from Friedmann at each step.")
print("This eliminates the drift error.")

# State: [phi, phi_p] only. H^2 computed from Friedmann constraint.
def H2_from_friedmann(phi, phi_p, xi, V0, N, Om, Or):
    """Compute H^2 from Friedmann constraint."""
    rho_m = 3.*Om*np.exp(-3.*N)
    rho_r = 3.*Or*np.exp(-4.*N)
    F = 1.-xi*phi**2; FP = -2.*xi*phi
    V = V0
    denom = 3.*F + 3.*FP*phi_p - 0.5*phi_p**2
    if denom < 1e-10:
        return None
    H2 = (rho_m + rho_r + V) / denom
    if H2 <= 0:
        return None
    return H2

def rhs_2d(N, state, xi=0.1):
    """2D ODE: [phi, phi_p]. H^2 from Friedmann constraint each step."""
    phi, phi_p = state
    H2 = H2_from_friedmann(phi, phi_p, xi, V0, N, Omega_m, Omega_r)
    if H2 is None or not np.isfinite(H2):
        return [0., 0.]
    # s_H from closed-form formula
    rho_m = 3.*Omega_m*np.exp(-3.*N)
    rho_r = 3.*Omega_r*np.exp(-4.*N)
    FP = -2.*xi*phi; FPP = -2.*xi
    N_sH = (-rho_m/H2 - (4./3.)*rho_r/H2 - 2.*V0/H2
            + FP*phi_p + 6.*FP**2 + FPP*phi_p**2)
    D_sH = 2.*(1.-xi*phi**2) - 3.*FP**2
    if abs(D_sH) < 1e-10: D_sH = 1e-10
    s_H = N_sH / D_sH
    phi_pp = -(3.+s_H)*phi_p - 6.*xi*phi*(2.+s_H)
    return [phi_p, phi_pp]

state0_2d = [0.01, 0.0]
sol2 = solve_ivp(lambda N, s: rhs_2d(N, s, 0.1),
                 [N_init, 0.0], state0_2d, method='LSODA',
                 rtol=1e-6, atol=1e-8,
                 t_eval=eval_pts, max_step=0.1)
print(f"2D (Friedmann-constrained) success: {sol2.success}, msg: {sol2.message}")
if sol2.t.size > 0:
    for i, N in enumerate(sol2.t):
        phi = sol2.y[0,i]; phi_p = sol2.y[1,i]
        H2 = H2_from_friedmann(phi, phi_p, 0.1, V0, N, Omega_m, Omega_r)
        lnH = 0.5*np.log(H2) if H2 and H2 > 0 else float('nan')
        print(f"  N={N:.1f}: phi={phi:.6f}, phi_p={phi_p:.6e}, H2={H2:.4e}, lnH={lnH:.4f}")
print("DONE")
