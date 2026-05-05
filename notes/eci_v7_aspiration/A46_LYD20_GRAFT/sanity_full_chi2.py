"""Full chi^2 sanity check at LYD20 published best fit."""

import sys
sys.path.insert(0, '/root/crossed-cosmos/notes/eci_v7_aspiration/A46_LYD20_GRAFT')
import numpy as np
from numpy import log, exp
from lyd20_fit_pinned import chi2_joint, extra_forms

# LYD20 best-fit (line 1531-1538)
tau_LYD = -0.2123 + 1.5201j
beta_u_alpha_u   = 325.6502
gamma_u_alpha_u  = 2427.3101  # positive in published fit
delta_u_alpha_u  = 219.3019
beta_d_alpha_d   = 466.6990
gamma_d_alpha_d  = -234.0473  # NEGATIVE in published fit
delta_d_alpha_d  = 2.3388
beta_e_alpha_e   = 0.0187
gamma_e_alpha_e  = 0.1466
g2_g1            = 0.6834
g1sq_vu_sq_Lambda_meV = 0.3043   # meV
g1sq_vu_sq_Lambda_eV  = 0.3043e-3

# Encode as 11-vector
sgn_d = -1.0  # negative gamma_d
params = [
    log(beta_u_alpha_u),
    log(gamma_u_alpha_u),
    log(delta_u_alpha_u),
    log(beta_d_alpha_d),
    log(abs(gamma_d_alpha_d)),
    sgn_d,
    log(delta_d_alpha_d),
    log(beta_e_alpha_e),
    log(gamma_e_alpha_e),
    g2_g1,
    log(g1sq_vu_sq_Lambda_eV),
]
F = extra_forms(tau_LYD)
chi2 = chi2_joint(params, F)
print(f"At LYD20 best-fit (tau={tau_LYD}, published params):")
print(f"  chi2_joint = {chi2:.4f}  (target ~ <20 across 19 obs)")
