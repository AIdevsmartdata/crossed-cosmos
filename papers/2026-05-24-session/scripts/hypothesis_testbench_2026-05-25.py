"""
ECI Hypothesis Testbench — 2026-05-25 soir
============================================
Tests les hypotheses calculables (H1-H12 + Higgs-modules) avec les valeurs SM
observees. Back-of-envelope numerique : on extrait les nombres predits par
chaque hypothese et on cherche des patterns simples (rationnels, transcendants,
ratios de courbure, etc.)

Auteur : Kevin Remondiere
"""
import numpy as np
from scipy.optimize import brentq, curve_fit
import json

print("="*78)
print("ECI HYPOTHESIS TESTBENCH — 2026-05-25 soir")
print("="*78)

# ============================================================================
# Donnees observees (PDG 2024)
# ============================================================================
# Masses fermions MeV (mass scheme MS-bar @ mu = m_t pour quarks lourds, sinon pole)
MASSES_MEV = {
    'e':       0.511,
    'mu':      105.658,
    'tau':     1776.86,
    'u':       2.16,      # PDG MS-bar @ 2 GeV
    'd':       4.67,
    's':       93.4,
    'c':       1.27e3,
    'b':       4.18e3,
    't':       172.57e3,
    'nu1':     0.05e-9,   # m_nu_lightest ~ 0.05 eV (cosmological + osc)
    'nu2':     0.05e-9 + 8.6e-12,  # +sqrt(Dm_sol^2)
    'nu3':     0.05e-9 + 50e-12,   # +sqrt(Dm_atm^2)
}

# Higgs et VEV
v_GeV      = 246.22
mH_GeV     = 125.10
mW_GeV     = 80.377
mZ_GeV     = 91.1876
sin2_thetaW = 0.23121

# CKM (Wolfenstein 2024)
lambda_CKM = 0.22500   # = sin(theta_C) approx
A_CKM      = 0.826
rho_bar    = 0.159
eta_bar    = 0.348
delta_CKM_rad = np.deg2rad(65.8)  # CP-violating phase

# PMNS (NuFIT 5.3 normal ordering)
theta12_rad = np.deg2rad(33.41)
theta23_rad = np.deg2rad(49.1)
theta13_rad = np.deg2rad(8.54)
delta_PMNS_rad = np.deg2rad(197)

# Couplages
alpha_em_MZ = 1/127.952
alpha_s_MZ  = 0.1180

# Cosmologie (Planck 2018 + DESI)
n_s = 0.9649
r_upper = 0.036    # BICEP/Keck 2021
Omega_DM_over_b = 5.36
eta_B = 6.12e-10
Lambda_over_MP4 = 1.105e-122

# Notre mesure ECI
kappa_SU2 = 0.5080
kappa_SU3 = 0.6025
kappa_inf_meas = 0.6776
zeta3_over_sqrtpi = 1.2020569 / np.sqrt(np.pi)  # = 0.6782

# ============================================================================
# H1 : Masses fermions = v * exp(-S_inst[F_f])
# ============================================================================
print("\n" + "="*78)
print("H1 : MASSES FERMIONS = v * exp(-S_inst)")
print("="*78)

v_MeV = v_GeV * 1000
S_inst = {}
for f, m in MASSES_MEV.items():
    if m > 0 and f.startswith(('e','mu','tau','u','d','s','c','b','t')):
        S_inst[f] = -np.log(m / v_MeV)
        print(f"  {f:5s} : m = {m:>12.4g} MeV, S_inst = {S_inst[f]:>7.3f}")

print("\n  Hierarchie S_e:S_mu:S_tau =")
S_e, S_mu, S_tau = S_inst['e'], S_inst['mu'], S_inst['tau']
print(f"    {S_e:.3f} : {S_mu:.3f} : {S_tau:.3f}")
print(f"    Ratios :     1.000 : {S_mu/S_e:.4f} : {S_tau/S_e:.4f}")
print(f"    Differences : {S_mu-S_e:.3f} (mu-e), {S_tau-S_mu:.3f} (tau-mu), {S_tau-S_e:.3f} (tau-e)")

# Test pattern S_i = a + b*i ? (linear in generation)
gen_lepton = [1, 2, 3]
S_lepton = [S_e, S_mu, S_tau]
slope, intercept = np.polyfit(gen_lepton, S_lepton, 1)
print(f"\n  Pattern lineaire S_gen = a*gen + b :")
print(f"    a = {slope:.3f}, b = {intercept:.3f}")
print(f"    Predit S_e={intercept+slope:.3f} (obs {S_e:.3f}), Δ={(intercept+slope)/S_e-1:+.1%}")
print(f"    Predit S_mu={intercept+2*slope:.3f} (obs {S_mu:.3f}), Δ={(intercept+2*slope)/S_mu-1:+.1%}")
print(f"    Predit S_tau={intercept+3*slope:.3f} (obs {S_tau:.3f}), Δ={(intercept+3*slope)/S_tau-1:+.1%}")
# Geometrique : S_i = S_0 * q^i ?
log_S = np.log(np.abs(S_lepton))
q_geom, ln_S0 = np.polyfit(gen_lepton, log_S, 1)
q_ratio = np.exp(q_geom)
print(f"\n  Pattern geometrique S_gen = S_0 * q^gen :")
print(f"    q = {q_ratio:.4f}, ln(S_0) = {ln_S0:.3f}")

# Ratios masses up/down/lepton
print(f"\n  Ratios masses cross-secteurs (gen 1):")
print(f"    m_u/m_d = {MASSES_MEV['u']/MASSES_MEV['d']:.4f}")
print(f"    m_d/m_e = {MASSES_MEV['d']/MASSES_MEV['e']:.4f}")
print(f"    m_u/m_e = {MASSES_MEV['u']/MASSES_MEV['e']:.4f}")
print(f"    m_t/m_b = {MASSES_MEV['t']/MASSES_MEV['b']:.4f}")
print(f"    m_t/m_e = {MASSES_MEV['t']/MASSES_MEV['e']:.4g}")

# ============================================================================
# H3 : m_H = courbure du potentiel
# ============================================================================
print("\n" + "="*78)
print("H3 : HIGGS m_H = courbure du potentiel")
print("="*78)

lambda_H = mH_GeV**2 / (2 * v_GeV**2)
print(f"  lambda_H = m_H^2 / (2*v^2) = {lambda_H:.6f}")
print(f"  m_H / v = {mH_GeV/v_GeV:.4f}")
print(f"  m_H / (sqrt(2)*v) = {mH_GeV/(np.sqrt(2)*v_GeV):.4f}")
print(f"  Comparaisons :")
print(f"    1/(4*pi) = {1/(4*np.pi):.6f}")
print(f"    1/8 = {1/8:.6f}")
print(f"    1/(2*pi^2) = {1/(2*np.pi**2):.6f}")
print(f"    g^2/8 (g_EW=0.65) = {0.65**2/8:.6f}")
print(f"    sin^2(thetaW)/2 = {sin2_thetaW/2:.6f}")
# lambda_H ~ 0.129 close to sin^2(thetaW)/2 = 0.116 ! ~10% off
print(f"  Best match : lambda_H ~ sin^2(thetaW)/2 a {(lambda_H/(sin2_thetaW/2)-1)*100:+.1f}%")

# Yukawa top = O(1)
y_top = np.sqrt(2) * (MASSES_MEV['t']/1000) / v_GeV
print(f"\n  y_top = sqrt(2)*m_t/v = {y_top:.4f} (= 1.000 a {abs(y_top-1)*100:.2f}%)")
print(f"  y_top^2 = {y_top**2:.4f} (= 1 ?)")

# ============================================================================
# H5 : Inflation n_s = 1 - 2/N_e, r = 8/N_e^2
# ============================================================================
print("\n" + "="*78)
print("H5 : INFLATION n_s = 1 - 2/N_e, r = 8/N_e^2")
print("="*78)

N_e_from_ns = 2 / (1 - n_s)
r_predit = 8 / N_e_from_ns**2
print(f"  n_s obs = {n_s}")
print(f"  N_e inferred (de n_s) = {N_e_from_ns:.2f}  (slow-roll typique 50-60)")
print(f"  r predit = 8/N_e^2 = {r_predit:.5f}")
print(f"  r upper bound BICEP/Keck = {r_upper}")
print(f"  Compatible : {'OUI' if r_predit < r_upper else 'NON'} (predit < bound)")
print()
print(f"  Relation de consistance ECI : r = 2*(1-n_s)^2")
r_consist = 2 * (1 - n_s)**2
print(f"    r_consist = {r_consist:.5f} (idem {r_predit:.5f}) ✓")
print(f"  → Si r mesure par CMB-S4, on peut tester directement la prediction.")

# ============================================================================
# H8 : m_nu / m_e ~ 10^-7 (distance modules)
# ============================================================================
print("\n" + "="*78)
print("H8 : m_nu / m_e ratio (ECI predit ~ 10^-7)")
print("="*78)

m_nu_meV = 50  # m_nu_lightest ~ 0.05 eV = 50 meV (cosmo bound)
m_e_MeV = MASSES_MEV['e']
ratio_nu_e = (m_nu_meV * 1e-9) / m_e_MeV  # both in MeV
print(f"  m_nu (lightest, cosmo bound) ~ {m_nu_meV} meV")
print(f"  m_e = {m_e_MeV} MeV")
print(f"  ratio = {ratio_nu_e:.3e}")
print(f"  log10(ratio) = {np.log10(ratio_nu_e):.2f}")
print(f"  ECI predit : ~ 10^-7  =>  {'OUI MATCH' if 1e-8 < ratio_nu_e < 1e-6 else 'NON'}")

# ============================================================================
# H9 : G_N = 1 / Σ κ_i, hierarchie M_Pl
# ============================================================================
print("\n" + "="*78)
print("H9 : G_N = 1 / Σ κ_i (intrications totales)")
print("="*78)

# κ(SU(N)) predit pour N=2,...,6 avec κ_inf = ζ(3)/√π
N_values = np.array([2, 3, 4, 5, 6])
kappa_pred = zeta3_over_sqrtpi * (1 - 1/N_values**2)
print(f"  κ_∞ = ζ(3)/√π = {zeta3_over_sqrtpi:.5f}")
print(f"  N : κ(SU(N)) :")
for N, k in zip(N_values, kappa_pred):
    print(f"    N={N} : κ = {k:.5f}")
sum_inv_kappa = np.sum(1/kappa_pred)
print(f"  Σ 1/κ_i (SU(2..6)) = {sum_inv_kappa:.4f}")
print(f"  G_N ∝ 1/{sum_inv_kappa:.4f} (en unites de la physique)")
print(f"  Pour hierarchie M_Pl/M_EW ~ 10^17, besoin facteur additionnel")
print(f"  (extra dim, grand N, ou volume modules)")

# ============================================================================
# H : Higgs-modules unification — ratios SUSY MSSM
# ============================================================================
print("\n" + "="*78)
print("HIGGS-MODULES : courbures principales de M predisent ratios m_H/m_h")
print("="*78)
print(f"  Si SUSY MSSM avec 5 Higgs : h, H, A, H^±")
print(f"  Predictions ECI :")
print(f"    m_H/m_h = sqrt(g_perp/g_parallel)  (rapport courbures)")
print(f"    m_A     ~ courbure CP, relie a δ_CKM = {np.rad2deg(delta_CKM_rad):.1f}°")
print(f"    m_H^±   ~ courbure chargee, relie a sin^2(θ_W) = {sin2_thetaW:.4f}")
print()
print(f"  CKM phase delta = {np.rad2deg(delta_CKM_rad):.1f}° = {delta_CKM_rad:.4f} rad")
print(f"  Test : delta_CKM = π/5 ? = {np.pi/5:.4f} rad = 36° (NON)")
print(f"  Test : delta_CKM = π*phi/8 (phi=1.618) ? = {np.pi*1.618/8:.4f} = 36.4° (NON)")
print(f"  Test : delta_CKM = 2π/(5+sqrt(5)) ? = {2*np.pi/(5+np.sqrt(5)):.4f} rad = 49.7° (NON)")
print(f"  Test : tan(delta_CKM) = {np.tan(delta_CKM_rad):.4f}")
print(f"           ratio eta_bar/rho_bar = {eta_bar/rho_bar:.4f} (geom recouvrement)")

# ============================================================================
# H_compression : 5 invariants → 25 observables
# ============================================================================
print("\n" + "="*78)
print("COMPRESSION : 5 invariants → 25 observables")
print("="*78)
n_obs = 25
n_inv = 5
print(f"  Compression ratio : {n_obs}/{n_inv} = {n_obs/n_inv:.1f}x")
print(f"  Si 3 hypotheses confirmees a <5%, ECI passe TIER 2 -> TIER 1")
print(f"  Si 5 hypotheses confirmees, ECI = cadre de classification")

# ============================================================================
# H : CKM lambda = angle Cabibbo et structure
# ============================================================================
print("\n" + "="*78)
print("H2 : CKM lambda = angle Cabibbo et structure geometrique")
print("="*78)

# Wolfenstein
print(f"  lambda = sin(theta_C) = {lambda_CKM:.5f}")
print(f"  Vus/Vud ≈ lambda")
print()
print(f"  Test sin(theta_C) = simple fonction ?")
print(f"    sqrt(m_d/m_s) = {np.sqrt(MASSES_MEV['d']/MASSES_MEV['s']):.4f}  (Gatto-Sartori-Tonin)")
print(f"    Predit lambda = sqrt(m_d/m_s) = {np.sqrt(MASSES_MEV['d']/MASSES_MEV['s']):.4f} vs obs {lambda_CKM:.4f}")
print(f"    Δ = {(np.sqrt(MASSES_MEV['d']/MASSES_MEV['s'])/lambda_CKM-1)*100:+.1f}%  (GST formula classique)")
print()
# A_CKM
print(f"  A = {A_CKM:.4f}")
print(f"    A relie a m_c/m_t = {MASSES_MEV['c']/MASSES_MEV['t']:.5e}")
print(f"    A^2 * lambda^4 = {A_CKM**2 * lambda_CKM**4:.5e}")
print(f"    m_c/m_t a comparer")

# ============================================================================
# Output JSON for further analysis
# ============================================================================
results = {
    'h1_S_inst': S_inst,
    'h1_lepton_S_pattern': {
        'slope': float(slope), 'intercept': float(intercept),
        'q_geom_ratio': float(q_ratio)
    },
    'h3_lambda_H': float(lambda_H),
    'h3_lambda_H_vs_sin2thetaW_over_2': float(lambda_H/(sin2_thetaW/2)),
    'h3_y_top': float(y_top),
    'h5_N_e_inferred': float(N_e_from_ns),
    'h5_r_predit': float(r_predit),
    'h5_consistency_r_vs_ns': float(r_consist),
    'h8_m_nu_over_m_e': float(ratio_nu_e),
    'h8_log10_ratio': float(np.log10(ratio_nu_e)),
    'h9_sum_inv_kappa_SU2_to_6': float(sum_inv_kappa),
    'h2_GST_lambda_predict': float(np.sqrt(MASSES_MEV['d']/MASSES_MEV['s'])),
    'h2_GST_vs_obs': float(np.sqrt(MASSES_MEV['d']/MASSES_MEV['s'])/lambda_CKM),
    'kappa_inf_meas': kappa_inf_meas,
    'kappa_inf_zeta3_sqrtpi': float(zeta3_over_sqrtpi),
    'kappa_inf_match_sigma': abs(kappa_inf_meas - zeta3_over_sqrtpi) / 0.003,
}

with open('/tmp/voie1_calcs/hypothesis_testbench_2026-05-25.json', 'w') as f:
    json.dump(results, f, indent=2, default=str)

print("\n" + "="*78)
print("SUMMARY — top matches a verifier en theorie")
print("="*78)
print(f"  H5 r-n_s consistency : {r_consist:.5f} (testable CMB-S4)")
print(f"  H8 m_nu/m_e : {ratio_nu_e:.2e} ECI predit 10^-7 -> MATCH ✓")
print(f"  H2 GST lambda : {np.sqrt(MASSES_MEV['d']/MASSES_MEV['s'])/lambda_CKM:.3f} of obs")
print(f"  H3 y_top = {y_top:.3f} (= 1 a {abs(y_top-1)*100:.1f}%)")
print(f"  H1 lepton pattern S_gen lineaire/geom : explore")
print(f"  H9 G_N = 1/Σκ converge {sum_inv_kappa:.2f} (besoin facteur conversion)")
print(f"\nResultats sauves : /tmp/voie1_calcs/hypothesis_testbench_2026-05-25.json")
