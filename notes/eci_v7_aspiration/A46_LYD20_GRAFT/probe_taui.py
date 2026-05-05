"""Why does tau=i return chi^2=1e10?"""
import sys
sys.path.insert(0, '/root/crossed-cosmos/notes/eci_v7_aspiration/A46_LYD20_GRAFT')
import numpy as np
from numpy import log, exp
from lyd20_fit_pinned import (extra_forms, M_u_unified, M_d_unified, M_e, M_D, M_N_inv,
                               light_nu_mass, ckm_from_M, diag_charged_lepton, pmns_angles)

tau = 0.0 + 1.0j
F = extra_forms(tau)
print("Modular form values at tau=i:")
for k, v in F.items():
    if abs(v) < 1e-15:
        print(f"  {k}:  ZERO ({v})")
    elif abs(v) < 1e-3:
        print(f"  {k}:  {v:.4e}  small")

# Build matrices with LYD-best params
Mu = M_u_unified(F, 1.0, 325.6502, 2427.3101, 219.3019)
Md = M_d_unified(F, 1.0, 466.6990, -234.0473, 2.3388)
Me = M_e(F, 1.0, 0.0187, 0.1466)
Mnu = light_nu_mass(F, 1.0, 0.6834, 0.3043e-3)

print("\nMatrix sizes (Frobenius):")
print(f"  M_u: {np.linalg.norm(Mu):.4e}")
print(f"  M_d: {np.linalg.norm(Md):.4e}")
print(f"  M_e: {np.linalg.norm(Me):.4e}")
print(f"  M_nu: {np.linalg.norm(Mnu):.4e}")

print("\nSingular values:")
print(f"  M_u sv: {np.sort(np.linalg.svd(Mu, compute_uv=False))}")
print(f"  M_d sv: {np.sort(np.linalg.svd(Md, compute_uv=False))}")
print(f"  M_e sv: {np.sort(np.linalg.svd(Me, compute_uv=False))}")
print(f"  M_nu sv: {np.sort(np.linalg.svd(Mnu, compute_uv=False))}")
