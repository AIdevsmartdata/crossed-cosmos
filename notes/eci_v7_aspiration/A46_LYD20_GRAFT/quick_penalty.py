"""Quick penalty estimate via direct chi^2 evaluation at LYD-best params,
swept over tau. This is a LOWER bound on the actual fit chi^2 at each tau."""
import sys
sys.path.insert(0, '/root/crossed-cosmos/notes/eci_v7_aspiration/A46_LYD20_GRAFT')
import numpy as np
from numpy import log, exp
from lyd20_fit_pinned import (extra_forms, M_u_unified, M_d_unified, M_e,
                               light_nu_mass, ckm_from_M, pmns_angles,
                               diag_charged_lepton, PDG_QUARK, PDG_NU,
                               PDG_M_E_MU, PDG_M_MU_TAU, fit_joint, chi2_joint)
import time

# Use small DE / fast for relative comparison
print("Quick joint fits (popsize=12, 1 round + polish)...")
t0 = time.time()

results = {}
for tau, label in [(0.0+1.0j, "tau=i pinned"),
                    (-0.2123+1.5201j, "LYD20-best"),
                    (-0.1897+1.0034j, "W1*")]:
    res = fit_joint(tau, label, n_de_rounds=1, popsize=8, maxiter=80,
                    seed=42, verbose=False)
    results[label] = res['chi2_min']
    print(f"  {label:20s} chi2 = {res['chi2_min']:.2f}  ({time.time()-t0:.0f}s)")

c_i = results["tau=i pinned"]
c_LYD = results["LYD20-best"]
c_W1 = results["W1*"]
print()
print(f"PENALTY tau=i  / LYD-best = {c_i / max(c_LYD, 1e-6):.2f}x")
print(f"PENALTY tau=W1 / LYD-best = {c_W1 / max(c_LYD, 1e-6):.2f}x")
