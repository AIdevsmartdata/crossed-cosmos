import math
from math import pi, sqrt, log, log10, exp

# Constants CODATA 2022
c = 2.99792458e8
G = 6.67430e-11
hbar = 1.054571817e-34
kB = 1.380649e-23
e_C = 1.602176634e-19  # C
alpha_fs = 7.2973525693e-3  # fine structure

# Masses in GeV (convert from kg where needed)
GeV_in_kg = 1.782661921e-27
MeV_in_kg = 1.782661921e-30
eV_in_kg = 1.782661921e-36

M_P_kg = sqrt(hbar*c/G)
M_P_GeV = M_P_kg * c**2 / (1e9 * e_C)  # = 2.435e18 for reduced, 1.221e19 for non-reduced
print(f"M_P (non-reduced) = {M_P_GeV:.4e} GeV")
M_P_reduced_GeV = M_P_GeV / sqrt(8*pi)
print(f"M_P (reduced) = {M_P_reduced_GeV:.4e} GeV")

omega_P = sqrt(c**5/(G*hbar))
print(f"omega_P = {omega_P:.4e} rad/s")

H0_SI = 67.4 * 1000 / 3.0857e22
print(f"H_0 = {H0_SI:.4e} s^-1")

# Particle masses
m_e_GeV = 0.5109989461e-3
m_p_GeV = 0.93827208816
m_nu_GeV = 0.06e-9  # 0.06 eV sum upper bound
v_EW_GeV = 246
Lambda_QCD_GeV = 0.217
F_pi_GeV = 0.0924  # 92.4 MeV

# Cosmological constant
Omega_L = 0.6847
rho_L_SI = Omega_L * 3 * H0_SI**2 * c**2 / (8*pi*G)  # J/m^3
# Lambda dimension: [L^-2]
Lambda_SI = 3 * Omega_L * (H0_SI/c)**2  # m^-2
print(f"Lambda = {Lambda_SI:.4e} m^-2")

# Lambda^(1/4) in energy units
# rho_Lambda in GeV^4 natural units:
# rho_Lambda = Omega_L * 3 * H_0^2 * M_P^2 (reduced) — no: rho_L = 3 H_0^2 M_P^2 Omega_L
# Easier: compute from SI then convert
# rho_L_SI in J/m^3 = (energy)^4 with energy in natural units
# 1 GeV = 1.602e-10 J; 1 m = 5.068e15 GeV^-1 (natural units)
# rho_L in GeV^4 = rho_L_SI * m^3 / J -> conv: 1 J/m^3 in GeV^4
J_in_GeV = 1 / (1e9 * e_C)  # J -> GeV
GeV_inv_m = c*hbar / (e_C*1e9)  # 1 GeV^-1 in m
m_to_invGeV = 1/GeV_inv_m
rho_L_GeV4 = rho_L_SI * J_in_GeV / (m_to_invGeV**3)
Lambda_quarter_GeV = rho_L_GeV4**0.25
Lambda_quarter_eV = Lambda_quarter_GeV * 1e9
print(f"Lambda^(1/4) = {Lambda_quarter_eV:.4f} eV (claimed 2.24 meV = 0.00224 eV)")
print(f"                {Lambda_quarter_eV*1000:.4f} meV")

# ----- Relation 2: (H_0/omega_P)^2
r2 = (H0_SI/omega_P)**2
Lambda_over_MP4 = rho_L_GeV4 / M_P_GeV**4
print(f"\n[#2] (H_0/omega_P)^2        log10 = {log10(r2):.3f}")
print(f"     Lambda/M_P^4 (non-red)  log10 = {log10(Lambda_over_MP4):.3f}")
Lambda_over_MPred4 = rho_L_GeV4 / M_P_reduced_GeV**4
print(f"     Lambda/M_P^4 (reduced)  log10 = {log10(Lambda_over_MPred4):.3f}")

# ----- Relation 3: Lambda^(1/4) ~ m_nu
sum_mnu_eV = 0.06  # lower bound from oscillations
avg_mnu_eV = sum_mnu_eV/3
print(f"\n[#3] Lambda^(1/4) = {Lambda_quarter_eV*1000:.3f} meV")
print(f"     <m_nu> = {avg_mnu_eV*1000:.2f} meV (Σ=0.06 eV / 3)")
print(f"     ratio = {Lambda_quarter_eV*1000/(avg_mnu_eV*1000):.2f}")

# ----- Relation 4: (F_pi/M_P)^6 ~ Lambda/M_P^4
r4 = (F_pi_GeV/M_P_GeV)**6
print(f"\n[#4] (F_pi/M_P)^6                  log10 = {log10(r4):.3f}")
print(f"     Lambda/M_P^4                   log10 = {log10(Lambda_over_MP4):.3f}")
print(f"     Claimed doc: predicted -120.7, obs -121.55")

# ----- Relation 5: (m_e/M_P)^5 * alpha^4
r5 = (m_e_GeV/M_P_GeV)**5 * alpha_fs**4
print(f"\n[#5] (m_e/M_P)^5 * alpha^4         log10 = {log10(r5):.3f}")

# ----- Relation 7: <H> ~ Lambda^(1/6) * M_P^(1/3)
# Using non-reduced M_P
vH_pred_GeV = Lambda_quarter_GeV**(4/6) * M_P_GeV**(1/3)
# Lambda^(1/6) in GeV: Lambda_quarter^(4/6) = rho_L^(1/6)
# Actually Gonzalo et al. formula: <H> ~ Lambda^(1/6) * M_P^(1/3), where Lambda has dim (energy)^4 so Lambda^(1/6) has energy^(2/3)
vH_pred_GeV = rho_L_GeV4**(1/6) * M_P_GeV**(1/3)
print(f"\n[#7] <H> predicted = rho_L^(1/6) M_P^(1/3) = {vH_pred_GeV*1000:.1f} MeV")
print(f"     <H> observed = 246 GeV = 246000 MeV")
print(f"     Ratio obs/pred = {246*1000/(vH_pred_GeV*1000):.1f}x")
# Doc claims 106 MeV predicted, 246 GeV obs, ratio 2300

# ----- Relation 8: optimum k for (H_0/omega_P) ~ (m_e/M_P)^k
r_log = log10(H0_SI/omega_P)
me_over_MP_log = log10(m_e_GeV/M_P_GeV)
k_opt = r_log / me_over_MP_log
print(f"\n[#8] H_0/omega_P: log10 = {r_log:.3f}")
print(f"     m_e/M_P: log10 = {me_over_MP_log:.3f}")
print(f"     k_optimum = {k_opt:.3f} (doc claims 2.72 — non-rational)")

# ----- Relation 11: Dark dimension length
# l_DD = hbar c / m_KK, m_KK ~ Lambda^(1/4) / alpha
# For alpha=1: m_KK = Lambda^(1/4) ~ 2.3 meV -> l = hbar c / E
# hbar*c = 197 MeV fm = 197e-3 GeV * 1e-15 m = 1.97e-16 GeV m
hbarc_GeVm = 1.9733e-16
mKK_GeV_alpha1 = Lambda_quarter_GeV
l_DD_m = hbarc_GeVm / mKK_GeV_alpha1
print(f"\n[#11] alpha=1: m_KK = {mKK_GeV_alpha1*1e12:.3f} meV -> l_DD = {l_DD_m*1e6:.1f} μm")
# Doc claims 88 μm for alpha=1

# ----- Koide formula
# Q = (m_e + m_mu + m_tau) / (sqrt(m_e) + sqrt(m_mu) + sqrt(m_tau))^2
m_mu_MeV = 105.6583745
m_tau_MeV = 1776.93
m_e_MeV = 0.5109989461
num = m_e_MeV + m_mu_MeV + m_tau_MeV
den = (sqrt(m_e_MeV) + sqrt(m_mu_MeV) + sqrt(m_tau_MeV))**2
Q = num/den
print(f"\n[#9] Koide Q = {Q:.6f} (doc claims 0.666661 observed, 2/3 = {2/3:.6f})")
