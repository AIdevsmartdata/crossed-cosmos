"""
Debug ODE stiffness. Run minimal test with print statements.
"""
import numpy as np
import sys

h = 0.6774
Omega_m = 0.1432 / h**2
# NOTE: omega_r = Omega_r * h^2 (physical), so Omega_r = omega_r_phys / h^2
# omega_r (physical) = 4.15e-5 / h^2? NO.
# Standard: omega_r = Omega_r * h^2 ≈ 4.15e-5 (radiation density parameter)
# So Omega_r = omega_r_phys / h^2 where omega_r_phys = 4.15e-5
# But 4.15e-5 is ALREADY the physical omega_r = Omega_r * h^2 at h=1? No.
# omega_r ≡ Omega_r * h^2 = 4.15e-5 (standard value from Planck 2018, CMB temperature)
# So Omega_r = omega_r / h^2 = 4.15e-5 / 0.6774^2 = 4.15e-5 / 0.4589 ≈ 9.04e-5

omega_r_phys = 4.15e-5  # = Omega_r * h^2
Omega_r = omega_r_phys / h**2  # correct
print(f"h={h}, h^2={h**2:.4f}")
print(f"Omega_m={Omega_m:.4f}")
print(f"Omega_r={Omega_r:.6f}  [should be ~9e-5]")

# But in the earlier code I wrote: omega_r = 4.15e-5 / 0.6774**2 (=9.04e-5)
# Then: Omega_r = omega_r / h**2 = 9.04e-5 / 0.4589 = 1.97e-4  <- double-divided!
omega_r_wrong = 4.15e-5 / h**2  # 9.04e-5
Omega_r_wrong = omega_r_wrong / h**2  # 1.97e-4
print(f"\nBUG CHECK: omega_r (already Omega_r*h^2): {4.15e-5:.3e}")
print(f"Omega_r_correct = 4.15e-5 / h^2 = {Omega_r:.4e}")
print(f"Omega_r_WRONG (double-divided) = {Omega_r_wrong:.4e}")
print(f"Using: Omega_r = {Omega_r:.4e} for tests")

Omega_L = 1.0 - Omega_m - Omega_r
print(f"Omega_L = {Omega_L:.4f}")
V0 = 3.0 * Omega_L
print(f"V0 = {V0:.4f}")

# Friedmann check at N=0
rho_m0 = 3.*Omega_m
rho_r0 = 3.*Omega_r
total0 = rho_m0 + rho_r0 + V0
print(f"\nFriedmann at N=0: rho_m={rho_m0:.4f} + rho_r={rho_r0:.4e} + V0={V0:.4f} = {total0:.4f}")
print(f"H^2(0) = {total0/3.:.6f}  [should be 1.0]")

# Initial conditions at N_init=-5
N_init = -5.0
rho_m_i = 3.*Omega_m*np.exp(-3.*N_init)
rho_r_i = 3.*Omega_r*np.exp(-4.*N_init)
H2_i = (rho_m_i + rho_r_i + V0)/3.
lnH_i = 0.5*np.log(H2_i)
print(f"\nAt N=-5: rho_m={rho_m_i:.3e}, rho_r={rho_r_i:.3e}, H2={H2_i:.3e}, lnH={lnH_i:.2f}")

# Try a single RHS evaluation at N=-5
phi = 0.01; phi_p = 0.0; xi = 0.10; beta = 0.0; m2 = 0.0
lnH = lnH_i
H2 = np.exp(2.*lnH)
rho_m = 3.*Omega_m*np.exp(-3.*N_init)
rho_r = 3.*Omega_r*np.exp(-4.*N_init)
F = 1. - xi*phi**2; FP = -2.*xi*phi; FPP = -2.*xi
V = V0; VP = 0.
N_sH = (-rho_m/H2 - (4./3.)*rho_r/H2 - 2.*V/H2
        + FP*phi_p + 6.*FP**2 + FPP*phi_p**2)
D_sH = 2.*F - 3.*FP**2
s_H = N_sH / D_sH
phi_pp = -(3.+s_H)*phi_p - VP/H2 - 6.*xi*phi*(2.+s_H)
print(f"\nRHS at N=-5 (xi=0.1):")
print(f"  H2={H2:.3e}, rho_m/H2={rho_m/H2:.6f}, rho_r/H2={rho_r/H2:.4e}")
print(f"  N_sH={N_sH:.6f}, D_sH={D_sH:.6f}, s_H={s_H:.6f}")
print(f"  phi_pp={phi_pp:.8f}")
print(f"  Expected s_H at N=-5 MD: ~-1.5 (matter domination)")

# The stiffness: at N=-5, radiation dominated: s_H = H'/H ≈ -2 (rad dom)
# rho_r/H2 at N=-5 ≈ 3*9e-5*e20 / (rho_tot/3)
# rho_r(N=-5) = 3*9e-5 * e^20 ≈ 3*9e-5 * 4.85e8 ≈ 1.31e5
# rho_m(N=-5) = 3*0.312 * e^15 ≈ 0.936 * 3.27e6 ≈ 3.06e6
# H2(N=-5) ≈ (3.06e6 + 1.31e5)/3 ≈ 1.06e6
# rho_m/H2 ≈ 3.06e6/1.06e6 ≈ 2.89
# This is fine! Let me check what s_H comes out to
print("\nManual check:")
print(f"  rho_m={rho_m:.3e}, rho_r={rho_r:.3e}")
print(f"  H2={H2:.3e}")
print(f"  rho_m/H2 = {rho_m/H2:.4f}  [should be ~2.9 if matter-dominated]")
print(f"  rho_r/H2 = {rho_r/H2:.4f}  [should be ~0.12 if some radiation]")
print(f"  V/H2 = {V/H2:.4e}  [should be tiny at N=-5]")

# Now try scipy with LSODA directly for just a few steps
from scipy.integrate import solve_ivp

def rhs(N, state):
    phi, phi_p, lnH = state
    H2 = np.exp(2.*lnH)
    if not np.isfinite(H2) or H2 < 1e-30:
        return [0., 0., 0.]
    Om = Omega_m; Or = Omega_r
    rho_m = 3.*Om*np.exp(-3.*N)
    rho_r = 3.*Or*np.exp(-4.*N)
    xi = 0.1; beta = 0.; m2 = 0.; V0_l = V0
    F = 1.-xi*phi**2; FP = -2.*xi*phi; FPP = -2.*xi
    V = V0_l; VP = 0.
    N_sH = (-rho_m/H2 - (4./3.)*rho_r/H2 - (2.*V+FP*VP)/H2
            + FP*phi_p + 6.*FP**2 + FPP*phi_p**2)
    D_sH = 2.*F - 3.*FP**2
    if abs(D_sH) < 1e-10: D_sH = 1e-10
    s_H = N_sH / D_sH
    phi_pp = -(3.+s_H)*phi_p - VP/H2 - 6.*xi*phi*(2.+s_H)
    return [phi_p, phi_pp, s_H]

state0 = [0.01, 0.0, lnH_i]
print(f"\nIntegrating from N={N_init} to N=0...")
print(f"  Initial state: phi={state0[0]}, phi_p={state0[1]}, lnH={state0[2]:.2f}")

# Very small first step to see if it works
sol = solve_ivp(rhs, [N_init, -4.9], state0, method='LSODA',
                rtol=1e-4, atol=1e-6, max_step=0.01,
                t_eval=np.array([-4.9]))
print(f"  Step to N=-4.9: success={sol.success}, msg={sol.message}")
if sol.success:
    print(f"  phi={sol.y[0,-1]:.6f}, lnH={sol.y[2,-1]:.4f}, s_H_eff={sol.y[2,-1]-lnH_i:.4f}")

# Full integration
sol2 = solve_ivp(rhs, [N_init, 0.0], state0, method='LSODA',
                 rtol=1e-5, atol=1e-7, max_step=0.1,
                 t_eval=np.linspace(N_init, 0, 50))
print(f"\nFull integration LSODA: success={sol2.success}, msg={sol2.message}")
if sol2.t.size > 0:
    print(f"  phi_today={sol2.y[0,-1]:.6f}")
    print(f"  lnH_today={sol2.y[2,-1]:.6f}  [should be ~0]")

print("\nDONE")
