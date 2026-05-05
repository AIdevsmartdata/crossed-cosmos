"""Identify which observable is breaking chi^2."""

import sys
sys.path.insert(0, '/root/crossed-cosmos/notes/eci_v7_aspiration/A46_LYD20_GRAFT')
sys.path.insert(0, '/root/crossed-cosmos/notes/eci_v7_aspiration/A16_THETA13_PREDICTION')
import numpy as np
from numpy import log, exp
from lyd20_fit_pinned import (extra_forms, M_u_unified, M_d_unified, ckm_from_M,
                               M_e, light_nu_mass, pmns_angles, diag_charged_lepton,
                               PDG_QUARK, PDG_NU, PDG_M_E_MU, PDG_M_MU_TAU)

tau_LYD = -0.2123 + 1.5201j
F = extra_forms(tau_LYD)

# Quark
Mu = M_u_unified(F, 1.0, 325.6502, 2427.3101, 219.3019)
Md = M_d_unified(F, 1.0, 466.6990, -234.0473, 2.3388)
V, Vus, Vcb, Vub, J_q, sv_u, sv_d = ckm_from_M(Mu, Md)
sv_u_s = np.sort(sv_u); sv_d_s = np.sort(sv_d)

# Lepton
Me = M_e(F, 1.0, 0.0187, 0.1466)
Mnu = light_nu_mass(F, 1.0, 0.6834, 0.3043e-3)  # mass_scale in eV
s12, s13, s23, dCP, J_l, m_nu = pmns_angles(Me, Mnu)
_, sv_e = diag_charged_lepton(Me); sv_e = np.sort(sv_e)

# Print all observables vs targets
def chi2_pull(name, pred, target_tup):
    targ, sigma = target_tup
    if "delta_CP" in name:
        diff = pred - targ
        while diff > 180: diff -= 360
        while diff < -180: diff += 360
        c = (diff/sigma)**2
    else:
        c = ((pred - targ)/sigma)**2
    print(f"  {name:18s} pred={pred:+.5e}  target={targ:+.5e}  sigma={sigma:.2e}  chi2={c:.3f}")
    return c

total = 0
print("=== QUARK SECTOR (8 obs) ===")
total += chi2_pull("m_u/m_c",  sv_u_s[0]/sv_u_s[1], PDG_QUARK["m_u/m_c"])
total += chi2_pull("m_c/m_t",  sv_u_s[1]/sv_u_s[2], PDG_QUARK["m_c/m_t"])
total += chi2_pull("m_d/m_s",  sv_d_s[0]/sv_d_s[1], PDG_QUARK["m_d/m_s"])
total += chi2_pull("m_s/m_b",  sv_d_s[1]/sv_d_s[2], PDG_QUARK["m_s/m_b"])
total += chi2_pull("|V_us|",   Vus, PDG_QUARK["Vus"])
total += chi2_pull("|V_cb|",   Vcb, PDG_QUARK["Vcb"])
total += chi2_pull("|V_ub|",   Vub, PDG_QUARK["Vub"])
total += chi2_pull("|J_CKM|",  abs(J_q), (3.06e-5, 0.18e-5))

print(f"Quark partial chi^2 = {total:.3f}")
prev = total
print()
print("=== LEPTON SECTOR (8 obs incl. delta_CP) ===")
total += chi2_pull("sin2_t12",  s12, PDG_NU["sin2_12"])
total += chi2_pull("sin2_t13",  s13, PDG_NU["sin2_13"])
total += chi2_pull("sin2_t23",  s23, PDG_NU["sin2_23"])
total += chi2_pull("delta_CP",  dCP, PDG_NU["delta_CP"])
total += chi2_pull("Dm21_sq",   m_nu[1]**2 - m_nu[0]**2, PDG_NU["Dm21_sq"])
total += chi2_pull("Dm32_sq",   m_nu[2]**2 - m_nu[1]**2, PDG_NU["Dm32_sq"])
total += chi2_pull("m_e/m_mu",  sv_e[0]/sv_e[1], PDG_M_E_MU)
total += chi2_pull("m_mu/m_tau",sv_e[1]/sv_e[2], PDG_M_MU_TAU)

print(f"Lepton partial chi^2 = {total - prev:.3f}")
print(f"TOTAL = {total:.3f}")
print()
print(f"Predicted neutrino masses (eV): {m_nu}")
print(f"Sum m_nu (meV): {sum(m_nu)*1e3:.4f}  (LYD20: 63.06)")
