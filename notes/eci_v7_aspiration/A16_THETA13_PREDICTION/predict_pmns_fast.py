"""Fast version of A16 PMNS prediction: 3 DE rounds + polish, prints progress."""
import sys, time, json, os
sys.path.insert(0, '/root/crossed-cosmos/notes/eci_v7_aspiration/A16_THETA13_PREDICTION')
import numpy as np
from numpy import pi, sqrt, exp
from scipy.linalg import svd, eigh
from scipy.optimize import minimize, differential_evolution
import warnings
warnings.filterwarnings("ignore")

# Re-use modular forms + matrices from the slow version
from predict_pmns import (all_forms, M_e, M_D, M_N_inv, light_nu_mass,
                          diag_charged_lepton, diag_neutrino, pmns_angles,
                          chi2_neutrino, PDG_NU)


def fit_fast(tau_l, label, seed=42, n_de_rounds=3):
    F = all_forms(tau_l)
    bounds = [(-10.0, 10.0), (-15.0, 5.0), (-5.0, 8.0), (-5.0, 8.0), (-5.0, 8.0)]
    best = (1e20, None)
    t0 = time.time()
    for s in range(n_de_rounds):
        r = differential_evolution(
            chi2_neutrino, bounds, args=(F,),
            maxiter=600, tol=1e-8, seed=seed + 100 * s, popsize=20,
            mutation=(0.5, 1.5), recombination=0.9, workers=1, disp=False
        )
        if r.fun < best[0]:
            best = (float(r.fun), r.x)
        print(f"  [{label}] DE round {s+1}/{n_de_rounds}  chi2={r.fun:.3f}  best={best[0]:.3f}  t={time.time()-t0:.1f}s", flush=True)
    rng = np.random.default_rng(seed)
    for _ in range(10):
        x0 = best[1] + 0.05 * rng.standard_normal(len(best[1]))
        try:
            r = minimize(chi2_neutrino, x0, args=(F,), method="Nelder-Mead",
                         options={"xatol": 1e-12, "fatol": 1e-12, "maxiter": 30000})
            if r.fun < best[0]:
                best = (float(r.fun), r.x)
        except Exception:
            pass
    chi2_final, x = best
    g2_g1, log_mass, log_ae, log_be, log_ge = x
    g1, g2 = 1.0, g2_g1
    mass_scale = exp(log_mass); alpha_e = exp(log_ae); beta_e = exp(log_be); gamma_e = exp(log_ge)
    Me = M_e(F, alpha_e, beta_e, gamma_e)
    Mnu = light_nu_mass(F, g1, g2, mass_scale)
    s12, s13, s23, dCP, J, m_nu = pmns_angles(Me, Mnu)
    _, sv_e = diag_charged_lepton(Me); sv_e = np.sort(sv_e)
    me_mmu = float(sv_e[0]/sv_e[1]); mmu_mt = float(sv_e[1]/sv_e[2])
    Dm21 = float(m_nu[1]**2 - m_nu[0]**2); Dm32 = float(m_nu[2]**2 - m_nu[1]**2)
    return {
        "label": label, "tau_l": [float(tau_l.real), float(tau_l.imag)],
        "chi2_min": float(chi2_final),
        "params": {"g2/g1": float(g2_g1), "mass_scale_eV": float(mass_scale),
                   "alpha_e": float(alpha_e), "beta_e": float(beta_e), "gamma_e": float(gamma_e)},
        "predicted": {
            "sin2_theta_12": float(s12), "sin2_theta_13": float(s13),
            "sin2_theta_23": float(s23), "delta_CP_deg": float(dCP),
            "J_PMNS": float(J), "m_nu_eV": [float(x) for x in m_nu],
            "Dm21_sq_eV2": Dm21, "Dm32_sq_eV2": Dm32,
            "sum_m_nu_eV": float(sum(m_nu)),
            "m_e/m_mu": me_mmu, "m_mu/m_tau": mmu_mt,
        },
    }


def main():
    print("FAST A16 -- PMNS prediction at W1 attractor", flush=True)
    print("=" * 60, flush=True)

    tau_LYD = -0.2123 + 1.5201j
    print(f"\n[1] LYD20 sanity check at tau = {tau_LYD}", flush=True)
    res_LYD = fit_fast(tau_LYD, "LYD20_check", seed=42)
    p = res_LYD["predicted"]
    print(f"    sin^2 t12={p['sin2_theta_12']:.4f} (LYD20: 0.34981)", flush=True)
    print(f"    sin^2 t13={p['sin2_theta_13']:.4f} (LYD20: 0.02193)", flush=True)
    print(f"    sin^2 t23={p['sin2_theta_23']:.4f} (LYD20: 0.56393)", flush=True)
    print(f"    delta_CP={p['delta_CP_deg']:.1f} deg (LYD20: 266.18)", flush=True)
    print(f"    chi2_min={res_LYD['chi2_min']:.2f}", flush=True)

    tau_W1 = -0.1897 + 1.0034j
    print(f"\n[2] W1 attractor tau = {tau_W1}", flush=True)
    res_W1 = fit_fast(tau_W1, "W1_attractor", seed=42)
    p = res_W1["predicted"]
    print(f"    sin^2 t12={p['sin2_theta_12']:.4f}", flush=True)
    print(f"    sin^2 t13={p['sin2_theta_13']:.4f}  PDG: {PDG_NU['sin2_13'][0]:.4f}", flush=True)
    print(f"    sin^2 t23={p['sin2_theta_23']:.4f}", flush=True)
    print(f"    delta_CP={p['delta_CP_deg']:.1f} deg", flush=True)
    print(f"    chi2_min={res_W1['chi2_min']:.2f}", flush=True)

    tau_i = 0.0 + 1.0j
    print(f"\n[3] CM tau = i", flush=True)
    res_i = fit_fast(tau_i, "tau_eq_i", seed=42)
    p = res_i["predicted"]
    print(f"    sin^2 t12={p['sin2_theta_12']:.4f}", flush=True)
    print(f"    sin^2 t13={p['sin2_theta_13']:.4f}", flush=True)
    print(f"    sin^2 t23={p['sin2_theta_23']:.4f}", flush=True)
    print(f"    delta_CP={p['delta_CP_deg']:.1f} deg", flush=True)
    print(f"    chi2_min={res_i['chi2_min']:.2f}", flush=True)

    out = {
        "version": "ECI v6.0.53.2", "agent": "A16-fast", "date": "2026-05-05",
        "method": "LYD20 unified-model lepton, fast 3-DE-round refit at multiple tau",
        "pdg_nufit_2024": {k: list(v) for k, v in PDG_NU.items()},
        "experimental_reach": {
            "Daya_Bay_RENO_2024": {"sigma_sin2_t13": 0.0007, "year": 2024},
            "JUNO_2026":          {"sigma_sin2_t13": 0.0005, "year": 2026,
                                   "ref": "JUNO Collab arXiv:2204.13249"},
            "DUNE_2030":          {"sigma_sin2_t13": 0.0001, "year": 2030,
                                   "ref": "DUNE TDR Vol II arXiv:2002.03005"},
        },
        "fit_LYD20_check":  res_LYD,
        "fit_W1_attractor": res_W1,
        "fit_tau_eq_i":     res_i,
    }
    s13_W1 = res_W1["predicted"]["sin2_theta_13"]
    s13_pdg, s13_pdg_sigma = PDG_NU["sin2_13"]
    pull_W1 = (s13_W1 - s13_pdg) / s13_pdg_sigma
    pull_i = (res_i["predicted"]["sin2_theta_13"] - s13_pdg) / s13_pdg_sigma
    if abs(pull_W1) > 1.0 and res_W1["chi2_min"] < 50:
        verdict = (f"PREDICTION DIFFERS FROM PDG (testable): W1 sin^2 t13 = {s13_W1:.4f} "
                   f"vs PDG {s13_pdg:.4f} (pull = {pull_W1:.2f} sigma)")
    elif res_W1["chi2_min"] > 50:
        verdict = (f"FIT POOR (chi2 = {res_W1['chi2_min']:.1f}); W1 tau may not "
                   f"accommodate full PMNS sector. Predicted s^2 t13 = {s13_W1:.4f} "
                   f"vs PDG {s13_pdg:.4f} (pull = {pull_W1:.2f} sigma) -- "
                   f"interpret as best-effort point estimate.")
    else:
        verdict = (f"WITHIN ERRORS: W1 sin^2 t13 = {s13_W1:.4f} "
                   f"vs PDG {s13_pdg:.4f} (pull = {pull_W1:.2f} sigma)")
    out["verdict"] = verdict
    out["pull_W1_vs_PDG_sin2_t13"] = float(pull_W1)
    out["pull_tau_i_vs_PDG_sin2_t13"] = float(pull_i)

    out_path = "/root/crossed-cosmos/notes/eci_v7_aspiration/A16_THETA13_PREDICTION/theta13_prediction.json"
    with open(out_path, "w") as f:
        json.dump(out, f, indent=2)
    print()
    print("VERDICT:", verdict, flush=True)
    print("Saved", out_path, flush=True)


if __name__ == "__main__":
    main()
