"""Probe chi^2 surface around starting points to find feasibility."""
import sys
sys.path.insert(0, '/root/crossed-cosmos/notes/eci_v7_aspiration/A46_LYD20_GRAFT')
import numpy as np
from numpy import log, exp
from lyd20_fit_pinned import chi2_joint, extra_forms

# Use LYD20 best params evaluated at tau=i (different tau from LYD's best)
for tau in [0.0+1.0j, -0.2123+1.5201j, -0.1897+1.0034j]:
    F = extra_forms(tau)
    params = [
        log(325.6502), log(2427.3101), log(219.3019),
        log(466.6990), log(234.0473), -1.0,
        log(2.3388),
        log(0.0187), log(0.1466),
        0.6834,
        log(0.3043e-3),
    ]
    chi2 = chi2_joint(params, F)
    print(f"tau={tau}  chi2 at LYD-params: {chi2:.4e}")
