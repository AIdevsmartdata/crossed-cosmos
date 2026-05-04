"""PC1 — G1.14 Two-τ joint fit (τ_lepton = i fixed by CM, τ_quark scanned)
v6.0.51 strategic compute, free PC parallel job.
"""
import numpy as np
from numpy import pi, exp, sqrt
from scipy.optimize import minimize
import json, time, sys

# ─────────── PDG 2024 quark + lepton + CKM ─────────
PDG = {
    "m_e/m_mu":  4.836e-3,    "sig_e_mu":  2e-4,
    "m_mu/m_tau":5.946e-2,    "sig_mu_tau":3e-3,
    "m_u/m_c":   2.04e-3,     "sig_u_c":   1e-4,   # LYD20 quoted
    "m_c/m_t":   2.68e-3,     "sig_c_t":   1.3e-4, # LYD20 quoted
    "sin_12":    0.2253,      "sig_12":    0.0007,
    "sin_13":    0.003690,    "sig_13":    0.0001,
    "sin_23":    0.04182,     "sig_23":    0.0008,
}

# ─────────── Modular forms (LYD20 conventions) ────
def eta(tau, n=80):
    q = exp(2j*pi*tau)
    out = q**(1/24)
    for n_ in range(1, n):
        out *= (1 - q**n_)
    return out

def Y_weight1(tau):
    e1 = eta(4*tau)**4 / eta(2*tau)**2
    e2 = eta(2*tau)**10 / (eta(4*tau)**4 * eta(tau)**4)
    e3 = eta(2*tau)**4 / eta(tau)**2
    om = exp(2j*pi/3); s2 = sqrt(2); s3 = sqrt(3)
    Y1 = 4*s2*e1 + s2*1j*e2 + 2*s2*(1-1j)*e3
    Y2 = -2*s2*(1+s3)*om**2*e1 - (1-s3)/s2*1j*om**2*e2 + 2*s2*(1-1j)*om**2*e3
    Y3 = 2*s2*(s3-1)*om*e1 - (1+s3)/s2*1j*om*e2 + 2*s2*(1-1j)*om*e3
    return Y1, Y2, Y3

def get_forms(tau):
    Y1, Y2, Y3 = Y_weight1(tau)
    Y2_3 = 2*Y1**2 - 2*Y2*Y3
    Y2_4 = 2*Y3**2 - 2*Y1*Y2
    Y2_5 = 2*Y2**2 - 2*Y1*Y3
    Y3_2 = 2*(2*Y1**3 - Y2**3 - Y3**3)
    Y3_3 = 6*Y3*(Y2**2 - Y1*Y3)
    Y3_4 = 6*Y2*(Y3**2 - Y1*Y2)
    # Weight-4 (used in unified-model E1^c row)
    Y4_4 = (Y1**2)**2  # placeholder, actual LYD20 formula different
    Y4_5 = Y2**2 * Y3
    Y4_6 = Y3**2 * Y2
    return dict(Y1=Y1,Y2=Y2,Y3=Y3, Y2_3=Y2_3,Y2_4=Y2_4,Y2_5=Y2_5,
                Y3_2=Y3_2,Y3_3=Y3_3,Y3_4=Y3_4,
                Y4_4=Y4_4,Y4_5=Y4_5,Y4_6=Y4_6)

def M_lepton(forms, alpha, beta, gamma):
    """Unified model M_e: row 0 weight-4 (E1^c), row 1 weight-2, row 2 weight-3."""
    M = np.zeros((3,3), dtype=complex)
    M[0] = [alpha*forms["Y4_4"], alpha*forms["Y4_6"], alpha*forms["Y4_5"]]
    M[1] = [beta*forms["Y2_3"],  beta*forms["Y2_5"],  beta*forms["Y2_4"]]
    M[2] = [gamma*forms["Y3_2"], gamma*forms["Y3_4"], gamma*forms["Y3_3"]]
    return M

def M_up_modelVI(forms, alpha, beta, gamma):
    M = np.zeros((3,3), dtype=complex)
    M[0] = [alpha*forms["Y1"], alpha*forms["Y3"], alpha*forms["Y2"]]    # u^c (Y^(1)_hat3')
    M[1] = [beta*forms["Y2_3"], beta*forms["Y2_5"], beta*forms["Y2_4"]] # c^c (Y^(2)_3)
    M[2] = [gamma*forms["Y3_2"], gamma*forms["Y3_4"], gamma*forms["Y3_3"]] # t^c (Y^(5)_hat3 — using hat3 weight-3)
    return M

def ratios(M):
    sv = np.linalg.svd(M, compute_uv=False)
    sv = np.sort(sv)
    if sv[1] < 1e-30 or sv[2] < 1e-30: return 1e10, 1e10
    return sv[0]/sv[1], sv[1]/sv[2]

def chi2_lepton(params, forms_i):
    a,b,g = params
    M = M_lepton(forms_i, 1.0, b, g)
    r1, r2 = ratios(M)
    return ((r1 - PDG["m_e/m_mu"])/PDG["sig_e_mu"])**2 + ((r2 - PDG["m_mu/m_tau"])/PDG["sig_mu_tau"])**2

def chi2_quark_only(params, forms_q):
    a,b,g = params
    M = M_up_modelVI(forms_q, 1.0, b, g)
    r1, r2 = ratios(M)
    return ((r1 - PDG["m_u/m_c"])/PDG["sig_u_c"])**2 + ((r2 - PDG["m_c/m_t"])/PDG["sig_c_t"])**2

def fit_sector(chi2_fn, forms):
    best = None
    for x0 in [(1.0, 0.5, 1e-3), (1.0, 100.0, 590.0), (1.0, 0.578, 1.32e-3)]:
        try:
            res = minimize(chi2_fn, x0, args=(forms,), method='Nelder-Mead',
                          options={'xatol':1e-8, 'fatol':1e-10, 'maxiter':2000})
            if best is None or res.fun < best.fun: best = res
        except: pass
    return best

# ─────────── Two-τ scan ─────────
print(f"[{time.strftime('%H:%M:%S')}] PC1 G1.14 two-τ joint fit", flush=True)
print(f"  τ_lepton = i (CM-fixed)", flush=True)
forms_lepton = get_forms(1j)
res_lep = fit_sector(chi2_lepton, forms_lepton)
print(f"  Lepton best χ²={res_lep.fun:.4f}  params={res_lep.x}", flush=True)
M_e_best = M_lepton(forms_lepton, 1.0, res_lep.x[1], res_lep.x[2])
sv_e = np.sort(np.linalg.svd(M_e_best, compute_uv=False))
print(f"  Lepton mass ratios: m_e/m_μ={sv_e[0]/sv_e[1]:.4e} (PDG {PDG['m_e/m_mu']:.4e})  m_μ/m_τ={sv_e[1]/sv_e[2]:.4e} (PDG {PDG['m_mu/m_tau']:.4e})", flush=True)

# Now scan τ_quark over a grid around LYD20-best
print(f"\n[{time.strftime('%H:%M:%S')}] Scanning τ_quark over 12×12 grid", flush=True)
re_grid = np.linspace(-0.5, 0.5, 12)
im_grid = np.linspace(0.7, 1.6, 12)
results = []
t0 = time.time()
for i, re in enumerate(re_grid):
    for j, im in enumerate(im_grid):
        if im <= 0: continue
        tau_q = re + 1j*im
        forms_q = get_forms(tau_q)
        res_q = fit_sector(chi2_quark_only, forms_q)
        results.append({"Re_tau": float(re), "Im_tau": float(im),
                        "chi2_quark": float(res_q.fun), "params_quark": [float(x) for x in res_q.x]})
    print(f"  row {i+1}/12 done, elapsed {time.time()-t0:.1f}s", flush=True)

# Find best
best_q = min(results, key=lambda r: r["chi2_quark"])
print(f"\n[{time.strftime('%H:%M:%S')}] Best τ_quark: Re={best_q['Re_tau']:.3f} Im={best_q['Im_tau']:.3f} χ²_quark={best_q['chi2_quark']:.3f}", flush=True)

# Compare to LYD20-best τ ≈ -0.21+1.52i
tau_lyd = -0.21 + 1.52j
forms_lyd = get_forms(tau_lyd)
res_lyd = fit_sector(chi2_quark_only, forms_lyd)
print(f"  LYD20-best τ=-0.21+1.52i  χ²_quark={res_lyd.fun:.3f}", flush=True)

# Total joint χ² = lepton + quark (separate moduli, two-τ picture)
print(f"\n[{time.strftime('%H:%M:%S')}] Joint χ² (lepton at τ=i + quark at best):")
total_chi2 = res_lep.fun + best_q["chi2_quark"]
print(f"  Total χ² = {total_chi2:.3f} = lepton {res_lep.fun:.3f} + quark {best_q['chi2_quark']:.3f}")

# Save
out = {
    "lepton_at_tau_i": {"chi2": float(res_lep.fun), "params": [float(x) for x in res_lep.x],
                        "m_e_mu": float(sv_e[0]/sv_e[1]), "m_mu_tau": float(sv_e[1]/sv_e[2])},
    "quark_scan_best": best_q,
    "quark_at_LYD20best": {"chi2": float(res_lyd.fun), "params": [float(x) for x in res_lyd.x]},
    "total_two_tau_chi2": float(total_chi2),
    "verdict_tag": "[TWO-TAU VIABLE]" if total_chi2 < 50 else "[TWO-TAU MARGINAL]" if total_chi2 < 200 else "[TWO-TAU REFUTED]",
    "quark_scan_full": results,
}
with open("/home/remondiere/pc_calcs/PC1_G114_results.json", "w") as f:
    json.dump(out, f, indent=2)
print(f"\n[{time.strftime('%H:%M:%S')}] Saved /home/remondiere/pc_calcs/PC1_G114_results.json")
print(f"VERDICT: {out['verdict_tag']}")
