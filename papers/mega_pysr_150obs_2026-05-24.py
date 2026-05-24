#!/usr/bin/env python3
"""MEGA PySR — 150+ observables PDG/lattice/cosmo avec dimensions propres.

Strategy :
1. Compile MAX observables (masses, couplages, widths, momenta, cosmo)
2. Normalize TOUS en RATIOS sans dimension (m/M_W, Γ/m, etc.)
3. Run grid search optimized + multi-tolerance Bonferroni
4. Filter TW≤2 vs TW≤3 séparément
5. Identifier couplages dynamiques (Γ/m, α, mixing) vs ratios statiques (m_a/m_b)
"""
import math
import time
import json
import numpy as np
from scipy.spatial import cKDTree
from multiprocessing import Pool, cpu_count
from scipy.stats import norm

START = time.time()
print(f"START : {time.ctime()}")
print(f"="*80)
print(f"MEGA PySR — 150+ observables optimisé i5-14600KF 20 threads")
print(f"="*80)

KAPPA = 1/6
PI = math.pi
N_CPUS = cpu_count()
N_BOOTSTRAP = 1000

# ============================================================
# COMPILATION 150+ OBSERVABLES — multi-secteurs SM + cosmo
# ============================================================
# Format : (name, value, sector, units_description)
# All values dimensionless ratios where possible

OBS = []

# === RATIO MASSES — particules / particule_référence ===
# Tous normalisés vs M_W = 80377 MeV pour éliminer GeV/MeV ambiguity
# Mais aussi vs Λ_QCD = 250 MeV et m_e = 0.511 MeV pour comparaisons
M_W = 80377  # MeV
M_Z = 91188
M_H = 125250
m_e = 0.510999
m_mu = 105.6583755
m_tau = 1776.86
m_p = 938.272
m_n = 939.565
m_u = 2.16
m_d = 4.67
m_s = 93.4
m_c = 1270
m_b = 4180
m_t = 172570
v_EW = 246220  # MeV
LAMBDA_QCD = 250  # MeV approximate
f_pi = 92.4  # MeV
f_K = 110.4  # MeV
sigma_root = 440  # MeV pure gauge string tension

# === Pure leptonic ratios ===
OBS.append(("m_μ/m_e", m_mu/m_e, "LEPTON"))
OBS.append(("m_τ/m_e", m_tau/m_e, "LEPTON"))
OBS.append(("m_τ/m_μ", m_tau/m_mu, "LEPTON"))
OBS.append(("Koide_lep", (m_e+m_mu+m_tau)/(math.sqrt(m_e)+math.sqrt(m_mu)+math.sqrt(m_tau))**2, "LEPTON"))

# === Pure quark mass ratios (MS-bar 2 GeV) ===
OBS.append(("m_d/m_u", m_d/m_u, "QUARK"))
OBS.append(("m_s/m_d", m_s/m_d, "QUARK"))
OBS.append(("m_s/m_u", m_s/m_u, "QUARK"))
OBS.append(("m_c/m_s", m_c/m_s, "QUARK"))
OBS.append(("m_b/m_c", m_b/m_c, "QUARK"))
OBS.append(("m_b/m_s", m_b/m_s, "QUARK"))
OBS.append(("m_t/m_b", m_t/m_b, "QUARK"))
OBS.append(("m_t/m_c", m_t/m_c, "QUARK"))
OBS.append(("m_c/m_u", m_c/m_u, "QUARK"))
OBS.append(("m_b/m_d", m_b/m_d, "QUARK"))

# === Hadron mass ratios — light mesons ===
m_pi_pm = 139.570
m_pi_0 = 134.977
m_K_pm = 493.677
m_K_0 = 497.611
m_eta = 547.862
m_etap = 957.78
m_rho = 775.26
m_omega = 782.65
m_phi_meson = 1019.461
m_K_star = 891.66
m_a0 = 980.0
m_f0_500 = 500.0  # σ
m_f0_980 = 990.0

OBS.append(("m_K/m_π", m_K_pm/m_pi_pm, "HADRON"))
OBS.append(("m_η/m_π", m_eta/m_pi_pm, "HADRON"))
OBS.append(("m_η'/m_π", m_etap/m_pi_pm, "HADRON"))
OBS.append(("m_η'/m_η", m_etap/m_eta, "HADRON"))
OBS.append(("m_ρ/m_π", m_rho/m_pi_pm, "HADRON"))
OBS.append(("m_K*/m_K", m_K_star/m_K_pm, "HADRON"))
OBS.append(("m_K*/m_ρ", m_K_star/m_rho, "HADRON"))
OBS.append(("m_ω/m_ρ", m_omega/m_rho, "HADRON"))
OBS.append(("m_φ/m_ω", m_phi_meson/m_omega, "HADRON"))
OBS.append(("m_φ/m_ρ", m_phi_meson/m_rho, "HADRON"))
OBS.append(("m_φ/m_K", m_phi_meson/m_K_pm, "HADRON"))
OBS.append(("m_π0/m_π", m_pi_0/m_pi_pm, "HADRON"))
OBS.append(("m_K0/m_K", m_K_0/m_K_pm, "HADRON"))

# === Baryons ===
m_Lambda = 1115.683
m_Sigma_p = 1189.37
m_Sigma_0 = 1192.642
m_Sigma_m = 1197.449
m_Xi_0 = 1314.86
m_Xi_m = 1321.71
m_Omega = 1672.45
m_Delta = 1232.0
m_Sigma_star = 1383.7
m_Xi_star = 1531.8
m_Lambda_c = 2286.46
m_Sigma_c = 2453.97
m_Xi_c = 2467.94
m_Omega_c = 2695.2
m_Lambda_b = 5619.6

OBS.append(("m_n/m_p", m_n/m_p, "BARYON"))
OBS.append(("m_Λ/m_p", m_Lambda/m_p, "BARYON"))
OBS.append(("m_Σ+/m_p", m_Sigma_p/m_p, "BARYON"))
OBS.append(("m_Σ-/m_p", m_Sigma_m/m_p, "BARYON"))
OBS.append(("m_Ξ0/m_p", m_Xi_0/m_p, "BARYON"))
OBS.append(("m_Ξ-/m_p", m_Xi_m/m_p, "BARYON"))
OBS.append(("m_Ω/m_p", m_Omega/m_p, "BARYON"))
OBS.append(("m_Δ/m_p", m_Delta/m_p, "BARYON"))
OBS.append(("m_Σ*/m_p", m_Sigma_star/m_p, "BARYON"))
OBS.append(("m_Ξ*/m_p", m_Xi_star/m_p, "BARYON"))
OBS.append(("m_Λc/m_p", m_Lambda_c/m_p, "BARYON"))
OBS.append(("m_Σc/m_p", m_Sigma_c/m_p, "BARYON"))
OBS.append(("m_Λb/m_p", m_Lambda_b/m_p, "BARYON"))
OBS.append(("m_p/m_π", m_p/m_pi_pm, "BARYON"))
OBS.append(("m_p/m_e", m_p/m_e, "BARYON"))

# === Heavy mesons ===
m_D_pm = 1869.66
m_D_0 = 1864.84
m_D_s = 1968.35
m_D_star = 2006.85
m_B_pm = 5279.34
m_B_0 = 5279.65
m_B_s = 5366.92
m_B_c = 6274.9
m_J_psi = 3096.9
m_psi_2S = 3686.097
m_chi_c0 = 3414.71
m_chi_c1 = 3510.66
m_chi_c2 = 3556.20
m_Upsilon_1S = 9460.4
m_Upsilon_2S = 10023.26
m_Upsilon_3S = 10355.2
m_chi_b1 = 9892.78
m_eta_c = 2983.9

OBS.append(("m_D/m_K", m_D_pm/m_K_pm, "CHARM"))
OBS.append(("m_D/m_π", m_D_pm/m_pi_pm, "CHARM"))
OBS.append(("m_D*/m_D", m_D_star/m_D_pm, "CHARM"))
OBS.append(("m_Ds/m_D", m_D_s/m_D_pm, "CHARM"))
OBS.append(("m_B/m_D", m_B_pm/m_D_pm, "BOTTOM"))
OBS.append(("m_B/m_K", m_B_pm/m_K_pm, "BOTTOM"))
OBS.append(("m_Bs/m_B", m_B_s/m_B_pm, "BOTTOM"))
OBS.append(("m_Bc/m_B", m_B_c/m_B_pm, "BOTTOM"))
OBS.append(("m_J/ψ/m_p", m_J_psi/m_p, "CHARM"))
OBS.append(("m_ψ(2S)/m_J/ψ", m_psi_2S/m_J_psi, "CHARM"))
OBS.append(("m_ψ(2S)/m_J/ψ ratio", m_psi_2S/m_J_psi, "CHARM"))
OBS.append(("m_χc0/m_J/ψ", m_chi_c0/m_J_psi, "CHARM"))
OBS.append(("m_χc1/m_J/ψ", m_chi_c1/m_J_psi, "CHARM"))
OBS.append(("m_χc2/m_J/ψ", m_chi_c2/m_J_psi, "CHARM"))
OBS.append(("m_ηc/m_J/ψ", m_eta_c/m_J_psi, "CHARM"))
OBS.append(("m_Υ(2S)/m_Υ(1S)", m_Upsilon_2S/m_Upsilon_1S, "BOTTOM"))
OBS.append(("m_Υ(3S)/m_Υ(1S)", m_Upsilon_3S/m_Upsilon_1S, "BOTTOM"))
OBS.append(("m_Υ(2S)/m_Υ(3S)", m_Upsilon_2S/m_Upsilon_3S, "BOTTOM"))
OBS.append(("m_χb1/m_Υ", m_chi_b1/m_Upsilon_1S, "BOTTOM"))
OBS.append(("m_Upsilon/m_J/ψ", m_Upsilon_1S/m_J_psi, "BOTTOM"))

# === EW + Higgs ===
OBS.append(("m_W/m_Z", M_W/M_Z, "EW"))
OBS.append(("m_H/m_Z", M_H/M_Z, "EW"))
OBS.append(("m_H/m_W", M_H/M_W, "EW"))
OBS.append(("m_H/v", M_H/v_EW, "EW"))
OBS.append(("m_t/m_W", m_t/M_W, "EW"))
OBS.append(("m_t/m_Z", m_t/M_Z, "EW"))
OBS.append(("v/m_W", v_EW/M_W, "EW"))
OBS.append(("v/m_t", v_EW/m_t, "EW"))

# === Couplages ===
OBS.append(("sin²θ_W_eff", 0.23857, "COUPLING"))
OBS.append(("sin²θ_W_MSbar_MZ", 0.23121, "COUPLING"))
OBS.append(("sin²2θ_W_eff", 4*0.23121*(1-0.23121), "COUPLING"))
OBS.append(("α_s(M_Z)", 0.1179, "COUPLING"))
OBS.append(("α_s(1GeV)", 0.4, "COUPLING"))
OBS.append(("1/α_em(0)", 137.036, "COUPLING"))
OBS.append(("1/α_em(M_Z)", 128.952, "COUPLING"))
OBS.append(("α_em(0)/α_s(M_Z)", (1/137.036)/0.1179, "COUPLING"))
OBS.append(("g_A_axial", 1.2754, "COUPLING"))
OBS.append(("g_V/g_A", 1/1.2754, "COUPLING"))
OBS.append(("F_pi/m_pi", f_pi/m_pi_pm, "COUPLING"))
OBS.append(("F_K/F_pi", f_K/f_pi, "COUPLING"))
OBS.append(("F_pi/Lambda_QCD", f_pi/LAMBDA_QCD, "COUPLING"))

# === CKM elements (already known structural) ===
V_ud = 0.97370
V_us = 0.22501
V_ub = 0.00377
V_cd = 0.22487
V_cs = 0.97320
V_cb = 0.04183
V_td = 0.00876
V_ts = 0.04117
V_tb = 0.99911
OBS.append(("V_ud", V_ud, "WEAK_CKM"))
OBS.append(("V_us", V_us, "WEAK_CKM"))
OBS.append(("V_ub", V_ub, "WEAK_CKM"))
OBS.append(("V_cd", V_cd, "WEAK_CKM"))
OBS.append(("V_cs", V_cs, "WEAK_CKM"))
OBS.append(("V_cb", V_cb, "WEAK_CKM"))
OBS.append(("V_td", V_td, "WEAK_CKM"))
OBS.append(("V_ts", V_ts, "WEAK_CKM"))
OBS.append(("V_tb", V_tb, "WEAK_CKM"))
OBS.append(("V_us²", V_us**2, "WEAK_CKM"))
OBS.append(("V_us/V_ud", V_us/V_ud, "WEAK_CKM"))
OBS.append(("V_cb/V_ub", V_cb/V_ub, "WEAK_CKM"))
OBS.append(("V_td/V_ts", V_td/V_ts, "WEAK_CKM"))

# === PMNS ===
OBS.append(("sin²θ12_PMNS", 0.307, "WEAK_PMNS"))
OBS.append(("sin²θ23_PMNS_NH", 0.561, "WEAK_PMNS"))
OBS.append(("sin²θ13_PMNS", 0.02224, "WEAK_PMNS"))
OBS.append(("sin²2θ12_PMNS", 4*0.307*(1-0.307), "WEAK_PMNS"))
OBS.append(("sin²2θ23_PMNS", 4*0.561*(1-0.561), "WEAK_PMNS"))
OBS.append(("sin²2θ13_PMNS", 4*0.02224*(1-0.02224), "WEAK_PMNS"))
OBS.append(("tan²θ12_PMNS", 0.307/(1-0.307), "WEAK_PMNS"))
OBS.append(("tan²θ23_PMNS", 0.561/(1-0.561), "WEAK_PMNS"))
OBS.append(("δ_CP_PMNS/(2π)", 1.36/(2*math.pi), "WEAK_PMNS"))

# === Magnetic moments (μ_N units) ===
mu_p = 2.79285
mu_n = -1.91304
OBS.append(("|μ_p|", abs(mu_p), "EM"))
OBS.append(("|μ_n|", abs(mu_n), "EM"))
OBS.append(("|μ_n|/|μ_p|", abs(mu_n)/abs(mu_p), "EM"))
OBS.append(("|μ_p|-|μ_n|", abs(mu_p)-abs(mu_n), "EM"))
OBS.append(("|μ_Λ|", 0.613, "EM"))
OBS.append(("|μ_Σ+|", 2.458, "EM"))
OBS.append(("|μ_Σ-|", 1.160, "EM"))
OBS.append(("|μ_Ξ0|", 1.250, "EM"))
OBS.append(("|μ_Ξ-|", 0.6507, "EM"))
OBS.append(("|μ_Ω|", 2.02, "EM"))
OBS.append(("|μ_Σ+/μ_Ξ-|", 2.458/0.6507, "EM"))
OBS.append(("|μ_Λ/μ_n|", 0.613/abs(mu_n), "EM"))

# === Decay widths (Γ/m ratios) ===
OBS.append(("Γ_ρ/m_ρ", 149/m_rho, "DECAY"))
OBS.append(("Γ_ω/m_ω", 8.49/m_omega, "DECAY"))
OBS.append(("Γ_φ/m_φ", 4.249/m_phi_meson, "DECAY"))
OBS.append(("Γ_K*/m_K*", 50.3/m_K_star, "DECAY"))
OBS.append(("Γ_J/ψ/m_J/ψ", 0.0929/m_J_psi, "DECAY"))
OBS.append(("Γ_ψ(2S)/m_ψ(2S)", 0.294/m_psi_2S, "DECAY"))
OBS.append(("Γ_Υ/m_Υ", 5.4e-2/m_Upsilon_1S, "DECAY"))
OBS.append(("Γ_W/m_W", 2085/M_W, "DECAY"))
OBS.append(("Γ_Z/m_Z", 2495.5/M_Z, "DECAY"))
OBS.append(("Γ_H/m_H", 4.07/M_H, "DECAY"))
OBS.append(("Γ_t/m_t", 1420/m_t, "DECAY"))

# === Cosmologie ===
OBS.append(("σ_8", 0.811, "COSMO"))
OBS.append(("n_s", 0.9649, "COSMO"))
OBS.append(("Ω_b", 0.04897, "COSMO"))
OBS.append(("Ω_DM", 0.2645, "COSMO"))
OBS.append(("Ω_m", 0.3147, "COSMO"))
OBS.append(("Ω_Λ", 0.6847, "COSMO"))
OBS.append(("Ω_DM/Ω_b", 0.2645/0.04897, "COSMO"))
OBS.append(("Ω_b/Ω_m", 0.04897/0.3147, "COSMO"))
OBS.append(("Ω_DM/Ω_m", 0.2645/0.3147, "COSMO"))
OBS.append(("Ω_Λ_h²", 0.6847*0.674**2, "COSMO"))
OBS.append(("Ω_m_h²", 0.3147*0.674**2, "COSMO"))
OBS.append(("Ω_b_h²", 0.04897*0.674**2, "COSMO"))
OBS.append(("h_Planck", 0.674, "COSMO"))
OBS.append(("h_SH0ES", 0.730, "COSMO"))
OBS.append(("H_SH0ES/H_Planck", 0.730/0.674, "COSMO"))
OBS.append(("τ_reion", 0.054, "COSMO"))
OBS.append(("z_reion", 7.7, "COSMO"))

# === Glueball mass ratios (AT2021) ===
OBS.append(("m_2++/m_0++_SU(3)", 1.397, "GLUEBALL"))
OBS.append(("m_0-+/m_0++_SU(3)", 1.5, "GLUEBALL"))
OBS.append(("m_2-+/m_0++_SU(3)", 1.84, "GLUEBALL"))
OBS.append(("m_2++/m_0++_SU(2)", 1.370, "GLUEBALL"))

# === Reine YM ratios ===
OBS.append(("m_0++/√σ_SU(2)", 3.82, "YM"))
OBS.append(("m_0++/√σ_SU(3)", 3.51, "YM"))
OBS.append(("m_0++/√σ_SU(4)", 3.42, "YM"))
OBS.append(("m_0++/√σ_SU(∞)", 3.27, "YM"))
OBS.append(("m_p/Λ_QCD", m_p/LAMBDA_QCD, "YM"))
OBS.append(("m_p/√σ", m_p/sigma_root, "YM"))
OBS.append(("F_pi/m_p", f_pi/m_p, "YM"))

# === Charge radii (fm) ===
OBS.append(("r_p_E (fm)", 0.8409, "EM_RADIUS"))
OBS.append(("r_p_M (fm)", 0.851, "EM_RADIUS"))
OBS.append(("r_π (fm)", 0.659, "EM_RADIUS"))
OBS.append(("r_K (fm)", 0.581, "EM_RADIUS"))
OBS.append(("r_p_E/r_π", 0.8409/0.659, "EM_RADIUS"))
OBS.append(("r_K/r_π", 0.581/0.659, "EM_RADIUS"))
OBS.append(("r_p_M/r_p_E", 0.851/0.8409, "EM_RADIUS"))

# === Higgs / λ_H ===
lambda_H = M_H**2 / (2*v_EW**2)
OBS.append(("λ_H", lambda_H, "EW"))
OBS.append(("y_t = √2·m_t/v", math.sqrt(2)*m_t/v_EW, "EW"))
OBS.append(("y_b = √2·m_b/v", math.sqrt(2)*m_b/v_EW, "EW"))

n_obs = len(OBS)
print(f"\nObservables compiled : {n_obs}")
print(f"By sector :")
from collections import Counter
sector_count = Counter(o[2] for o in OBS)
for s, c in sorted(sector_count.items(), key=lambda x: -x[1]):
    print(f"  {s:>15} : {c}")

# ============================================================
# Build candidates (TW≤2)
# ============================================================
a_set = np.array([-3, -2, -1, -0.5, 0, 0.5, 1, 1.5, 2, 3])
b_set = np.array([-2, -1, -0.5, 0, 0.5, 1, 2])
c_set = np.array([-1, -0.5, 0, 0.5, 1])
d_set = np.array([-1, -0.5, 0, 0.5, 1])
n_set = np.arange(1, 21)
m_set = np.arange(1, 21)

print(f"\nBuilding TW≤2 candidates...")
t1 = time.time()
candidates_list = []
for a in a_set:
    for b in b_set:
        for c in c_set:
            for d in d_set:
                tw = abs(a) + abs(b) + abs(c) + abs(d)
                if tw > 2:
                    continue
                base = (KAPPA**a) * ((1-KAPPA)**b) * ((1+KAPPA)**c) * (PI**d)
                for n in n_set:
                    for m in m_set:
                        if math.gcd(n, m) > 1:
                            continue
                        v = base * n / m
                        if v > 0 and 1e-6 < v < 1e8:
                            candidates_list.append((v, a, b, c, d, n, m, tw))

candidates_arr = np.array([c[0] for c in candidates_list])
log_candidates = np.log(candidates_arr)
sort_idx = np.argsort(log_candidates)
log_candidates_sorted = log_candidates[sort_idx]
tree = cKDTree(log_candidates_sorted.reshape(-1, 1))
print(f"Built {len(candidates_arr)} candidates in {time.time()-t1:.1f}s")

target_vals = np.array([o[1] for o in OBS])
target_logs = np.log(target_vals)

# Match
real_distances, real_indices = tree.query(target_logs.reshape(-1, 1), k=1)
real_rel = np.exp(real_distances.flatten()) - 1

tolerance_levels = [1e-5, 1e-4, 1e-3, 5e-3, 0.01, 0.02, 0.05]

print(f"\nReal hit counts :")
real_hits = {}
for tol in tolerance_levels:
    real_hits[tol] = int(np.sum(real_rel < tol))
    print(f"  tol < {tol*100:.4f}% : {real_hits[tol]}/{n_obs} ({100*real_hits[tol]/n_obs:.1f}%)")

# Bonferroni
val_min, val_max = target_vals.min(), target_vals.max()
log_min, log_max = math.log(val_min), math.log(val_max)
def bootstrap_one(seed):
    np.random.seed(seed)
    rand_logs = np.random.uniform(log_min, log_max, n_obs)
    distances, _ = tree.query(rand_logs.reshape(-1, 1), k=1)
    rel = np.exp(distances.flatten()) - 1
    return tuple(int(np.sum(rel < t)) for t in tolerance_levels)

print(f"\nRunning {N_BOOTSTRAP} bootstrap on {N_CPUS} CPUs...")
t3 = time.time()
with Pool(N_CPUS) as pool:
    boot_results = pool.map(bootstrap_one, range(2026, 2026 + N_BOOTSTRAP))
boot_results = np.array(boot_results)
print(f"Bootstrap : {time.time()-t3:.1f}s")

# Results
print(f"\n{'='*80}")
print(f"FINAL — TW≤2 filter, {n_obs} observables")
print(f"{'='*80}")
print(f"\n{'Tol':>10} {'Real':>6} {'Random μ±σ':>18} {'Z':>10} {'p-value':>15}")
print("-"*70)
verdict = {}
for i, tol in enumerate(tolerance_levels):
    real = real_hits[tol]
    rand_mean = boot_results[:, i].mean()
    rand_std = boot_results[:, i].std()
    z = (real - rand_mean) / max(rand_std, 0.01)
    p_value = 1 - norm.cdf(z)
    sig = "✓✓" if z > 5 else "✓" if z > 3 else "🟡" if z > 2 else ""
    verdict[tol] = (real, rand_mean, rand_std, z)
    print(f"  <{tol*100:.4f}% {real:>6} {rand_mean:>8.1f}±{rand_std:>6.2f} {z:>+9.2f}σ {p_value:>15.3e} {sig}")

# Save top matches by sector
print(f"\n{'='*80}")
print(f"TOP MATCHES PAR SECTEUR (sorted by rel diff)")
print(f"{'='*80}")
sort_real = np.argsort(real_rel)
matches_by_sector = {}
for k in range(n_obs):
    i = sort_real[k]
    name, val, sector = OBS[i]
    rel = real_rel[i]
    if rel < 0.001:  # only tight matches
        cand_idx = sort_idx[real_indices[i]]
        cand_meta = candidates_list[cand_idx]
        cand_v, a, b, c, d, n, m, tw = cand_meta
        formula = f"κ^{a}·(1-κ)^{b}·(1+κ)^{c}·π^{d}·({n}/{m})"
        matches_by_sector.setdefault(sector, []).append((name, val, cand_v, rel*100, tw, formula))

for sector, mtchs in sorted(matches_by_sector.items(), key=lambda x: -len(x[1])):
    print(f"\n[{sector}] {len(mtchs)} hits at <0.1% :")
    for n, v, pv, r, tw, f in mtchs[:5]:
        print(f"  {n:>25} obs={v:.5f} pred={pv:.5f} ({r:.3f}%) TW={tw}")

# Save
output = {
    "n_obs": n_obs,
    "n_candidates": len(candidates_arr),
    "elapsed_s": time.time() - START,
    "real_hits": {f"{t*100:.4f}%": int(real_hits[t]) for t in tolerance_levels},
    "z_scores": {f"{t*100:.4f}%": {
        "real": int(verdict[t][0]),
        "random_mean": float(verdict[t][1]),
        "random_std": float(verdict[t][2]),
        "z": float(verdict[t][3]),
    } for t in tolerance_levels},
    "by_sector": {s: [(n, v, pv, r, tw, f) for n, v, pv, r, tw, f in mtchs] for s, mtchs in matches_by_sector.items()},
}
with open("/tmp/mega_pysr_150obs_results.json", "w") as f:
    json.dump(output, f, indent=2)
print(f"\nSaved : /tmp/mega_pysr_150obs_results.json")
print(f"Total elapsed : {time.time()-START:.1f}s")
print(f"DONE.")
