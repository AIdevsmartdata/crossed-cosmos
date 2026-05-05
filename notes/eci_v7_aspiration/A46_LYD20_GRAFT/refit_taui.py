"""Re-fit only tau=i scenario with much more aggressive init strategy."""
import sys, time, json
sys.path.insert(0, '/root/crossed-cosmos/notes/eci_v7_aspiration/A46_LYD20_GRAFT')
import numpy as np
from numpy import log, exp
from scipy.optimize import differential_evolution, minimize
from lyd20_fit_pinned import (extra_forms, chi2_joint, fit_joint,
                               M_u_unified, M_d_unified, M_e, light_nu_mass,
                               ckm_from_M, pmns_angles, diag_charged_lepton)

tau_i = 0.0 + 1.0j
F = extra_forms(tau_i)
bounds = [(0.0, 12.0)]*5 + [(-1.0, 1.0)] + [(-3.0, 8.0)] + [(-8.0, 5.0)]*2 + [(-3.0, 3.0)] + [(-12.0, 0.0)]

# Strategy: 5 fully random DE rounds with different seeds, no warm start
print("Re-fit at tau=i with 5 random-init DE rounds (popsize=20, maxiter=300)...")
best = (1e20, None)
t0 = time.time()
for r in range(5):
    rng = np.random.default_rng(1000 + 137*r)
    n_pop = 20 * 11
    init_pop = np.zeros((n_pop, 11))
    for i in range(n_pop):
        for j, (lo, hi) in enumerate(bounds):
            init_pop[i, j] = rng.uniform(lo, hi)
    res = differential_evolution(
        chi2_joint, bounds, args=(F,),
        maxiter=300, tol=1e-9, seed=1000 + 137*r,
        popsize=20, mutation=(0.5, 1.5), recombination=0.9,
        workers=1, disp=False, init=init_pop,
    )
    if res.fun < best[0]:
        best = (float(res.fun), res.x)
    print(f"  round {r+1}/5  chi2={res.fun:.3f}  best={best[0]:.3f}  t={time.time()-t0:.1f}s", flush=True)

# Polish
if best[1] is not None:
    rng = np.random.default_rng(0)
    for k in range(8):
        x0 = best[1] + 0.05 * rng.standard_normal(len(best[1]))
        try:
            r = minimize(chi2_joint, x0, args=(F,), method="Nelder-Mead",
                         options={"xatol": 1e-9, "fatol": 1e-7, "maxiter": 5000})
            if r.fun < best[0]:
                best = (float(r.fun), r.x)
        except Exception:
            pass
    print(f"  After polish: chi2={best[0]:.3f}  t={time.time()-t0:.1f}s")

chi2_i = best[0]
print(f"\nFINAL chi2(tau=i) = {chi2_i:.4f}")

# Patch the JSON
with open("/root/crossed-cosmos/notes/eci_v7_aspiration/A46_LYD20_GRAFT/lyd20_pinned_results.json") as f:
    data = json.load(f)
data["fit_tau_i_pinned"]["chi2_min"] = float(chi2_i)
data["comparison"]["chi2_tau_i"] = float(chi2_i)
data["comparison"]["penalty_tau_i_vs_LYD"] = float(chi2_i / max(data["comparison"]["chi2_tau_LYD"], 1e-6))
data["verdict"] = (
    f"GRAFT VIABLE (penalty {data['comparison']['penalty_tau_i_vs_LYD']:.2f}x)"
    if data['comparison']['penalty_tau_i_vs_LYD'] < 5
    else f"GRAFT MARGINAL (penalty {data['comparison']['penalty_tau_i_vs_LYD']:.2f}x)"
)

# Also reconstruct predicted observables at the fitted point
xopt = best[1]
(lbu, lgu, ldu, lbd, lgd_abs, sgnd, ldd, lbe, lge, g2g1, lmass) = xopt
bu = exp(lbu); gu = exp(lgu); du = exp(ldu)
bd = exp(lbd); gd = (1.0 if sgnd >= 0 else -1.0) * exp(lgd_abs); dd = exp(ldd)
be = exp(lbe); ge = exp(lge); mass_scale = exp(lmass)
Mu = M_u_unified(F, 1.0, bu, gu, du)
Md = M_d_unified(F, 1.0, bd, gd, dd)
V, Vus, Vcb, Vub, J_q, sv_u, sv_d = ckm_from_M(Mu, Md)
Me = M_e(F, 1.0, be, ge)
Mnu = light_nu_mass(F, 1.0, g2g1, mass_scale)
s12, s13, s23, dCP, J_l, m_nu = pmns_angles(Me, Mnu)
_, sv_e = diag_charged_lepton(Me); sv_e = np.sort(sv_e)
sv_u_s = np.sort(sv_u); sv_d_s = np.sort(sv_d)
data["fit_tau_i_pinned"]["params"] = {
    "beta_u/alpha_u": float(bu), "gamma_u/alpha_u": float(gu),
    "delta_u/alpha_u": float(du), "beta_d/alpha_d": float(bd),
    "gamma_d/alpha_d": float(gd), "delta_d/alpha_d": float(dd),
    "beta_e/alpha_e": float(be), "gamma_e/alpha_e": float(ge),
    "g2/g1": float(g2g1), "mass_scale_eV": float(mass_scale),
}
data["fit_tau_i_pinned"]["predicted_quarks"] = {
    "m_u/m_c": float(sv_u_s[0]/sv_u_s[1]), "m_c/m_t": float(sv_u_s[1]/sv_u_s[2]),
    "m_d/m_s": float(sv_d_s[0]/sv_d_s[1]), "m_s/m_b": float(sv_d_s[1]/sv_d_s[2]),
    "Vus": float(Vus), "Vcb": float(Vcb), "Vub": float(Vub), "J_CKM": float(J_q),
}
data["fit_tau_i_pinned"]["predicted_leptons"] = {
    "sin2_theta_12": float(s12), "sin2_theta_13": float(s13),
    "sin2_theta_23": float(s23), "delta_CP_deg": float(dCP),
    "J_PMNS": float(J_l), "m_nu_eV": [float(x) for x in m_nu],
    "sum_m_nu_eV": float(sum(m_nu)),
    "Dm21_sq_eV2": float(m_nu[1]**2 - m_nu[0]**2),
    "Dm32_sq_eV2": float(m_nu[2]**2 - m_nu[1]**2),
    "m_e/m_mu": float(sv_e[0]/sv_e[1]), "m_mu/m_tau": float(sv_e[1]/sv_e[2]),
}

with open("/root/crossed-cosmos/notes/eci_v7_aspiration/A46_LYD20_GRAFT/lyd20_pinned_results.json", "w") as f:
    json.dump(data, f, indent=2)
print(f"Updated lyd20_pinned_results.json with new chi2(tau=i)={chi2_i:.3f}")
print(f"PENALTY tau=i / LYD-best = {data['comparison']['penalty_tau_i_vs_LYD']:.2f}x")
