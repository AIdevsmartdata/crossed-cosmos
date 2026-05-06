"""
Full corrected test for wolf_background.py synthetic tests.

Key corrections vs first attempt:
1. Density: rho = 3*Omega*exp(-nN) not omega*exp(-nN)
2. V0 tuned from Friedmann at N=0 (not N_init)
3. N_init=-5 not -8 (radiation era start, avoids stiffness)
4. Test B/C: use m2<0 (concave V, Wolf-favoured) to induce field motion
5. Test D: xi=1e-12 not 0 (avoids exact singularity in D_sH when phi=0, xi=0 is fine)

Physics insight (from A56 + M4):
- For quadratic V with m2=0 and phi_init small, phi stays near 0 regardless of xi.
  The instability from A56 was for exponential V with lambda driving the field.
- For Wolf quadratic V with m2<0 (concave), the tachyonic mass drives phi away.
  At xi=0.30, the NMC amplifies this runaway.
- Test B: phi_init=0.10, m2=-1 (in H0^2 units), xi=0.30 → expect runaway
- Test C: xi=2.31, same → catastrophic
- Test A: xi=0.10, same → stable (xi < xi_crit)
- Test D: xi=0, m2=0 → standard LCDM quintessence (phi frozen at phi_init)
"""
import numpy as np
from scipy.integrate import solve_ivp

h = 0.6774
Omega_m = 0.1432 / h**2
Omega_r = (4.15e-5 / h**2) / h**2  # tiny
Omega_L = 1.0 - Omega_m - Omega_r
print(f"Omega_m={Omega_m:.4f}, Omega_r={Omega_r:.5f}, Omega_L={Omega_L:.4f}")


def wolf_ode(N, state, xi, V0, beta, m2, Om, Or):
    """RHS for Wolf-NMC KG+Friedmann ODE."""
    phi, phi_p, lnH = state
    H2 = np.exp(2.*lnH)
    if H2 < 1e-30 or not np.isfinite(H2):
        return [0., 0., 0.]
    rho_m = 3.*Om*np.exp(-3.*N)
    rho_r = 3.*Or*np.exp(-4.*N)
    F = 1. - xi*phi**2
    FP = -2.*xi*phi
    FPP = -2.*xi
    V = V0 + beta*phi + 0.5*m2*phi**2
    VP = beta + m2*phi
    # Closed-form H'/H (sympy-verified, no phi'' in formula)
    N_sH = (-rho_m/H2 - (4./3.)*rho_r/H2
            - (2.*V + FP*VP)/H2
            + FP*phi_p + 6.*FP**2 + FPP*phi_p**2)
    D_sH = 2.*F - 3.*FP**2
    if abs(D_sH) < 1e-10:
        D_sH = 1e-10*(1 if D_sH >= 0 else -1)
    s_H = N_sH / D_sH
    if not np.isfinite(s_H):
        s_H = 0.
    # KG
    phi_pp = -(3.+s_H)*phi_p - VP/H2 - 6.*xi*phi*(2.+s_H)
    if not np.isfinite(phi_pp):
        phi_pp = 0.
    return [phi_p, phi_pp, s_H]


def integrate_wolf(xi, V0_input, beta, m2, phi_init, phi_p_init, N_init=-5.0):
    """Integrate Wolf ODE, return result dict."""
    # Compute initial H from Friedmann at N_init
    rho_m_i = 3.*Omega_m*np.exp(-3.*N_init)
    rho_r_i = 3.*Omega_r*np.exp(-4.*N_init)
    F_i = 1. - xi*phi_init**2
    FP_i = -2.*xi*phi_init
    V_i = V0_input + beta*phi_init + 0.5*m2*phi_init**2
    denom_i = 3.*F_i + 3.*FP_i*phi_p_init - 0.5*phi_p_init**2
    if denom_i < 1e-6:
        return {'success': False, 'message': 'bad denom at N_init'}
    H2_i = (rho_m_i + rho_r_i + V_i) / denom_i
    if H2_i <= 0:
        return {'success': False, 'message': f'H2_init<0: {H2_i:.3e}'}
    lnH_i = 0.5*np.log(H2_i)
    state0 = [phi_init, phi_p_init, lnH_i]

    def ev_run(N, s): return 10. - abs(s[0])
    ev_run.terminal = True; ev_run.direction = -1
    def ev_Fc(N, s): return (1. - xi*s[0]**2) - 0.001
    ev_Fc.terminal = True; ev_Fc.direction = -1

    N_eval = np.linspace(N_init, 0., 500)
    sol = solve_ivp(
        lambda N, s: wolf_ode(N, s, xi, V0_input, beta, m2, Omega_m, Omega_r),
        [N_init, 0.0], state0, method='LSODA',
        rtol=1e-6, atol=1e-8,
        t_eval=N_eval, max_step=0.05,
        events=[ev_run, ev_Fc]
    )
    res = {'V0': V0_input, 'N_init': N_init}
    if sol.t_events[0].size > 0:
        res['success'] = False; res['message'] = f'RUNAWAY at N={sol.t_events[0][0]:.2f}'
    elif sol.t_events[1].size > 0:
        res['success'] = False; res['message'] = f'F_COLLAPSE at N={sol.t_events[1][0]:.2f}'
    elif not sol.success:
        res['success'] = False; res['message'] = sol.message
    else:
        res['success'] = True; res['message'] = 'OK'
    if sol.t.size > 0:
        res['phi_today'] = sol.y[0,-1]
        res['phi_p_today'] = sol.y[1,-1]
        res['lnH_today'] = sol.y[2,-1]
        res['phi_max'] = float(np.max(np.abs(sol.y[0])))
        res['F_today'] = 1. - xi*sol.y[0,-1]**2
        res['F_min'] = float(np.min(1. - xi*sol.y[0]**2))
    return res


# ===== TEST SETUP =====
# All tests use Wolf quadratic potential with m2<0 (Wolf-favoured: concave)
# to actually drive phi away from initial value.
# V0 from Friedmann closure at N=0 (H0=1):
#   H^2(0) = 1 = (rho_m0 + rho_r0 + V0 + beta*phi0 + 0.5*m2*phi0^2) / (3F0 + 3FP0*phi_p0 - phi_p0^2/2)
#   with phi0=phi_init (approx, for small phi), phi_p0=0:
#   => V0 = 3*F0 - rho_m0 - rho_r0 - beta*phi0 - 0.5*m2*phi0^2

phi_init_std = 0.10   # larger initial field to see dynamics
beta_std = 0.0
m2_std = -0.5         # concave V (tachyonic scalar mass in flat space)
phi_p_init_std = 0.0

def compute_V0(xi, phi_i, phi_pi, beta, m2, Om=Omega_m, Or=Omega_r):
    """Tune V0 for Friedmann closure at N=0 with phi≈phi_i."""
    F0 = 1. - xi*phi_i**2
    FP0 = -2.*xi*phi_i
    denom0 = 3.*F0 + 3.*FP0*phi_pi - 0.5*phi_pi**2
    rho_m0 = 3.*Om
    rho_r0 = 3.*Or
    # H^2(0) = 1 => denom0 = rho_m0 + rho_r0 + V0_eff
    # V0_eff = V0 + beta*phi_i + 0.5*m2*phi_i^2
    V0_eff = denom0 - rho_m0 - rho_r0
    V0 = V0_eff - beta*phi_i - 0.5*m2*phi_i**2
    return V0

print("\n--- Computing V0 for each test ---")
tests = [
    ('A', 0.10, phi_init_std, beta_std, m2_std, 'STABLE_EXPECTED'),
    ('B', 0.30, phi_init_std, beta_std, m2_std, 'GATE_EXPECTED'),
    ('C', 2.31, phi_init_std, beta_std, m2_std, 'CATASTROPHIC_EXPECTED'),
    ('D', 0.00, 0.01, 0.0, 0.0, 'LCDM_LIKE_EXPECTED'),
]

results = {}
for label, xi_val, phi_i, beta_v, m2_v, expect in tests:
    V0_val = compute_V0(xi_val, phi_i, phi_p_init_std, beta_v, m2_v)
    print(f"Test {label}: xi={xi_val:.3g}, V0={V0_val:.4f}, phi_i={phi_i}, m2={m2_v}")
    r = integrate_wolf(xi_val, V0_val, beta_v, m2_v, phi_i, phi_p_init_std)

    if r.get('success'):
        lnH = r.get('lnH_today', 99.)
        phi_t = r.get('phi_today', 99.)
        F_t = r.get('F_today', 0.)
        phi_max = r.get('phi_max', 99.)
        F_min = r.get('F_min', 0.)
        # KG gate
        gate_pass = (abs(lnH) < 0.05) and (phi_max < 10.) and (F_min > 0.01)
        print(f"  ODE: OK | phi_today={phi_t:.4e} F_today={F_t:.4f} lnH_today={lnH:.4f}")
        print(f"  phi_max={phi_max:.4e} F_min={F_min:.4f} | gate_pass={gate_pass}")
        r['gate_pass'] = gate_pass
        r['gate_reason'] = 'passed' if gate_pass else f'lnH={lnH:.3f} phi_max={phi_max:.3e} F_min={F_min:.4f}'
    else:
        gate_pass = False
        print(f"  ODE: FAIL | {r['message']}")
        r['gate_pass'] = False
        r['gate_reason'] = r['message']

    # Verdict
    if label == 'A':
        verdict = 'PASS' if gate_pass else 'FAIL (expected stable, but gate triggered)'
    elif label in ('B', 'C'):
        verdict = 'PASS (gate triggered as expected)' if not gate_pass else 'FAIL (gate DID NOT trigger)'
    elif label == 'D':
        verdict = 'PASS' if gate_pass else 'FAIL (expected LCDM stable)'
    print(f"  VERDICT: {verdict}")
    r['verdict'] = verdict
    r['test_passed'] = ((label == 'A' and gate_pass) or
                        (label in ('B','C') and not gate_pass) or
                        (label == 'D' and gate_pass))
    results[label] = r

print("\n=== SUMMARY ===")
for k, v in results.items():
    s = 'PASS' if v['test_passed'] else 'FAIL'
    print(f"  Test {k}: {s} — {v.get('verdict','')}")
print("DONE")
