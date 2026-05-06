"""
Test corrected density conventions for Wolf-KG ODE.
Key fix: rho_m(N) = 3*Omega_m*exp(-3N), rho_r(N) = 3*Omega_r*exp(-4N)
with H0=1 normalization (Omega_m = omega_m/h^2).
"""
import numpy as np
from scipy.integrate import solve_ivp

omega_m = 0.1432
omega_r = 4.15e-5 / 0.6774**2
h = 0.6774
Omega_m = omega_m / h**2
Omega_r = omega_r / h**2
Omega_L = 1.0 - Omega_m - Omega_r
V0 = 3.0 * Omega_L
print(f"V0={V0:.4f}, Omega_m={Omega_m:.4f}, Omega_r={Omega_r:.5f}")


def rhs(N, state, xi, V0, beta, m2, Om, Or):
    phi, phi_p, lnH = state
    H2 = np.exp(2.*lnH)
    rho_m = 3.*Om*np.exp(-3.*N)
    rho_r = 3.*Or*np.exp(-4.*N)
    F = 1. - xi*phi**2
    FP = -2.*xi*phi
    FPP = -2.*xi
    V = V0 + beta*phi + 0.5*m2*phi**2
    VP = beta + m2*phi
    N_sH = (-rho_m/H2 - (4./3.)*rho_r/H2
            - (2.*V + FP*VP)/H2
            + FP*phi_p + 6.*FP**2 + FPP*phi_p**2)
    D_sH = 2.*F - 3.*FP**2
    if abs(D_sH) < 1e-10:
        D_sH = 1e-10
    s_H = N_sH / D_sH
    phi_pp = -(3.+s_H)*phi_p - VP/H2 - 6.*xi*phi*(2.+s_H)
    return [phi_p, phi_pp, s_H]


# Test with N_init = -5 (a ~ 0.0067, well into radiation domination)
N_init = -5.0
rho_m_i = 3.*Omega_m*np.exp(-3.*N_init)
rho_r_i = 3.*Omega_r*np.exp(-4.*N_init)
H2_i = (rho_m_i + rho_r_i + V0) / 3.
lnH_i = 0.5*np.log(H2_i)
state0 = [0.01, 0.0, lnH_i]
print(f"N_init={N_init}: lnH_i={lnH_i:.3f}, H_i={np.exp(lnH_i):.3f}")

tests = [
    ('A', 0.10, 'STABLE_EXPECTED'),
    ('B', 0.30, 'GATE_EXPECTED'),
    ('C', 2.31, 'CATASTROPHIC_EXPECTED'),
    ('D', 1e-12, 'LCDM_LIKE'),
]

for label, xi_val, expect in tests:
    try:
        sol = solve_ivp(
            lambda N, s: rhs(N, s, xi_val, V0, 0., 0., Omega_m, Omega_r),
            [N_init, 0.0], state0, method='LSODA',
            rtol=1e-6, atol=1e-8,
            t_eval=np.linspace(N_init, 0, 200),
            max_step=0.1
        )
        if sol.success:
            phi_f = sol.y[0, -1]
            lnH_f = sol.y[2, -1]
            phi_max = np.max(np.abs(sol.y[0]))
            F_min = np.min(1. - xi_val*sol.y[0]**2)
            print(f"Test {label} (xi={xi_val:.3g}): OK, phi_today={phi_f:.4e}, lnH_today={lnH_f:.4f}, phi_max={phi_max:.4e}, F_min={F_min:.4f}")
        else:
            print(f"Test {label} (xi={xi_val:.3g}): FAIL [{sol.message}]")
    except Exception as e:
        print(f"Test {label} (xi={xi_val:.3g}): ERROR [{e}]")

print("DONE")
