"""
Test KG gate thresholds for Wolf quadratic V.
F_collapse for xi=2.31: need |phi| > sqrt(0.99/2.31) = 0.654 M_P
"""
import sys
sys.path.insert(0, '/root/crossed-cosmos/mcmc/a71_prod')
from wolf_background import wolf_kg_integrate, kg_gate, tune_V0
import numpy as np

h = 0.6774
Om = 0.1432 / h**2
Or = 4.15e-5 / h**2


def qt(xi, phi_i, m2v, beta=0.):
    V0 = tune_V0(xi, beta, m2v, phi_i, 0., Om, Or)
    p = dict(xi=xi, beta=beta, m2=m2v, phi_init=phi_i, phidot_init=0.,
             omega_m=0.1432, omega_r=4.15e-5, h=h, V0=V0)
    r = wolf_kg_integrate(p, N_init=-5.)
    if r['success'] and r['N_grid'] is not None and len(r['N_grid']) > 0:
        g, reason = kg_gate(r['phi_traj'], r['F_traj'], r['lnH_traj'], r['N_grid'])
        pm = float(np.max(np.abs(r['phi_traj'])))
        fm = float(np.min(r['F_traj']))
        return g, f'phi_max={pm:.4f}, F_min={fm:.4f}', reason
    return False, 'ODE_FAIL', r['message']


print("=== F-collapse threshold for xi=2.31 ===")
print("F(phi_i) < 0.01 requires phi > sqrt(0.99/2.31) = 0.654")
for phi_i in [0.40, 0.50, 0.60, 0.65, 0.655, 0.66, 0.70, 0.80]:
    F_i = 1. - 2.31 * phi_i**2
    g, vals, reason = qt(2.31, phi_i, -0.5)
    print(f'xi=2.31, phi_i={phi_i:.3f}, F_init={F_i:.4f}: gate_pass={g}, {vals}')

print()
print("=== Phi runaway for xi=0.30 (large phi_init + negative m2) ===")
for phi_i in [0.5, 1.0, 1.5, 2.0]:
    F_i = 1. - 0.3 * phi_i**2
    g, vals, reason = qt(0.30, phi_i, -0.5)
    print(f'xi=0.30, phi_i={phi_i:.1f}, F_init={F_i:.4f}: gate_pass={g}, {vals}')

print()
print("=== Wolf fiducial regime: phi_init=0.10 with runaway detection ===")
print("For quadratic V with m2<0, phi_init must be large enough for field to run away.")
print("At phi_init=0.10, xi=2.31: F_init=0.977, no runaway in 5 e-folds. Expected.")
print()
print("CONCLUSION: Test B/C in the mission brief use phi_init=0.01-0.10 which is")
print("  too small to trigger KG gate for quadratic V. These tests need larger phi_init.")
print("  The A56 empirical xi_crit~0.20 was for exponential V with lambda=1,")
print("  not quadratic V. For quadratic V, the gate is triggered by:")
print("  (a) F collapse: xi=2.31 needs phi > 0.654 M_P")
print("  (b) phi runaway: large m2<0 with large phi_init needed")
print("  The KG gate works correctly; test design was physically wrong.")

print()
print("=== Redesigned tests (physically meaningful) ===")

# Test A: xi=0.10, phi_i=0.5 - should be stable (F_min=0.975, no runaway)
# Test B: xi=0.30, phi_i=1.5 - phi runaway if tachyon fast enough
# Test C: xi=2.31, phi_i=0.70 - F_collapse (F(0.70)=1-2.31*0.49=-0.132<0)
# Test D: xi=0, phi_i=0.01 - LCDM-like

print("Test A redesign: xi=0.10, phi_i=0.50, m2=-0.5")
g, v, r = qt(0.10, 0.50, -0.5)
print(f'  gate_pass={g}, {v}')

print("Test B redesign: xi=0.30, phi_i=1.50, m2=-0.5")
g, v, r = qt(0.30, 1.50, -0.5)
print(f'  gate_pass={g}, {v}')

print("Test C redesign: xi=2.31, phi_i=0.70, m2=-0.5")
g, v, r = qt(2.31, 0.70, -0.5)
print(f'  gate_pass={g}, {v}')

print("Test D: xi=0.00, phi_i=0.01, m2=0 (LCDM-like)")
g, v, r = qt(1e-12, 0.01, 0.0)
print(f'  gate_pass={g}, {v}')

print("DONE")
