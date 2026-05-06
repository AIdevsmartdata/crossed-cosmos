"""
Test B xi=0.30, C xi=2.31 separately. Check if runaway occurs.
"""
import numpy as np
from scipy.integrate import solve_ivp

h = 0.6774
Omega_m = 0.1432 / h**2
Omega_r = (4.15e-5 / h**2) / h**2
Omega_L = 1.0 - Omega_m - Omega_r
V0 = 3.0 * Omega_L


def rhs(N, state, xi, V0, Om, Or):
    phi, phi_p, lnH = state
    H2 = np.exp(2.*lnH)
    rho_m = 3.*Om*np.exp(-3.*N)
    rho_r = 3.*Or*np.exp(-4.*N)
    F = 1. - xi*phi**2
    FP = -2.*xi*phi
    FPP = -2.*xi
    V = V0
    VP = 0.
    N_sH = (-rho_m/H2 - (4./3.)*rho_r/H2
            - 2.*V/H2
            + FP*phi_p + 6.*FP**2 + FPP*phi_p**2)
    D_sH = 2.*F - 3.*FP**2
    if abs(D_sH) < 1e-10:
        D_sH = 1e-10
    s_H = N_sH / D_sH
    phi_pp = -(3.+s_H)*phi_p - 6.*xi*phi*(2.+s_H)
    return [phi_p, phi_pp, s_H]


N_init = -5.0
rho_m_i = 3.*Omega_m*np.exp(-3.*N_init)
rho_r_i = 3.*Omega_r*np.exp(-4.*N_init)
H2_i = (rho_m_i + rho_r_i + V0) / 3.
lnH_i = 0.5*np.log(H2_i)
state0 = [0.01, 0.0, lnH_i]

for xi_val in [0.10, 0.30, 2.31]:
    def ev_runaway(N, s): return 10.0 - abs(s[0])
    ev_runaway.terminal = True
    ev_runaway.direction = -1
    def ev_Fcollapse(N, s): return (1. - xi_val*s[0]**2) - 0.001
    ev_Fcollapse.terminal = True
    ev_Fcollapse.direction = -1

    sol = solve_ivp(
        lambda N, s: rhs(N, s, xi_val, V0, Omega_m, Omega_r),
        [N_init, 0.0], state0, method='LSODA',
        rtol=1e-6, atol=1e-8,
        t_eval=np.linspace(N_init, 0, 300),
        max_step=0.05,
        events=[ev_runaway, ev_Fcollapse]
    )
    if sol.t_events[0].size > 0:
        status = f"RUNAWAY at N={sol.t_events[0][0]:.2f}"
    elif sol.t_events[1].size > 0:
        status = f"F_COLLAPSE at N={sol.t_events[1][0]:.2f}"
    elif sol.success:
        phi_f = sol.y[0,-1]; lnH_f = sol.y[2,-1]
        phi_max = np.max(np.abs(sol.y[0]))
        F_today = 1. - xi_val*phi_f**2
        status = f"OK: phi_today={phi_f:.4e}, F_today={F_today:.4f}, lnH_today={lnH_f:.4f}, phi_max={phi_max:.4e}"
    else:
        status = f"FAIL: {sol.message}"
    print(f"xi={xi_val}: {status}")
print("DONE")
