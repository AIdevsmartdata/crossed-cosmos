"""Fast gate threshold test - minimal cases only."""
import sys
sys.path.insert(0, '/root/crossed-cosmos/mcmc/a71_prod')
from wolf_background import wolf_kg_integrate, kg_gate, tune_V0, _F
import numpy as np

h = 0.6774
Om = 0.1432 / h**2
Or = 4.15e-5 / h**2

def qt(xi, phi_i, m2v, beta=0., n_eval=100):
    V0 = tune_V0(xi, beta, m2v, phi_i, 0., Om, Or)
    # Quick Friedmann check
    F_i = _F(phi_i, xi)
    print(f"  F(phi_init) = {F_i:.4f}", end="")
    if F_i < 0.01:
        print(" -> F_collapse at init (gate trivially triggers)")
        return False, f'F_init={F_i:.4f} < 0.01', 'F_collapse_at_init'
    p = dict(xi=xi, beta=beta, m2=m2v, phi_init=phi_i, phidot_init=0.,
             omega_m=0.1432, omega_r=4.15e-5, h=h, V0=V0)
    r = wolf_kg_integrate(p, N_init=-5., n_eval=n_eval, method='LSODA')
    if not r['success'] or r['N_grid'] is None or len(r['N_grid']) == 0:
        print(f" -> ODE_FAIL: {r['message']}")
        return False, 'ODE_FAIL', r['message']
    g, reason = kg_gate(r['phi_traj'], r['F_traj'], r['lnH_traj'], r['N_grid'])
    pm = float(np.max(np.abs(r['phi_traj'])))
    fm = float(np.min(r['F_traj']))
    print(f" -> phi_max={pm:.3f}, F_min={fm:.4f}")
    return g, f'phi_max={pm:.3f}, F_min={fm:.4f}', reason

print("=== FAST KG GATE TESTS ===")

# For xi=2.31: F(phi) = 1 - 2.31*phi^2
# F < 0.01 when phi > sqrt(0.99/2.31) = 0.6544
print("xi=2.31: F collapse threshold = phi > 0.6544")
print(f"F(0.6) = {1-2.31*0.6**2:.4f}")
print(f"F(0.66) = {1-2.31*0.66**2:.4f}")
print(f"F(0.65) = {1-2.31*0.65**2:.4f}")
print(f"F(0.655) = {1-2.31*0.655**2:.4f}")
print()

# Test C redesign: phi_init=0.66 (F_init < 0 -> immediate gate)
print("Test C redesign: xi=2.31, phi_init=0.66")
g, v, r = qt(2.31, 0.66, -0.5)
print(f"  gate_pass={g}, reason={r}")

print()
print("Test B redesign: xi=0.30, phi_init=1.5, m2=-2.0 (strong tachyon)")
g, v, r = qt(0.30, 1.5, -2.0)
print(f"  gate_pass={g}, reason={r}")

print()
print("Test A (stable): xi=0.10, phi_init=0.5, m2=-0.5")
g, v, r = qt(0.10, 0.5, -0.5)
print(f"  gate_pass={g}, reason={r}")

print()
print("Test D (LCDM): xi=1e-12, phi_init=0.01, m2=0")
g, v, r = qt(1e-12, 0.01, 0.0)
print(f"  gate_pass={g}, reason={r}")

print()
print("DONE")
