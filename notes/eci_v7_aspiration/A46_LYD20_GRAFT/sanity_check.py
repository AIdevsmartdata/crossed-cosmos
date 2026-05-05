"""Sanity check: at LYD20 published best-fit (tau, params), verify the
M_d transcription reproduces (m_d/m_s, m_s/m_b) = (0.05036, 0.01773)."""

import sys
sys.path.insert(0, '/root/crossed-cosmos/notes/eci_v7_aspiration/A46_LYD20_GRAFT')
sys.path.insert(0, '/root/crossed-cosmos/notes/eci_v7_aspiration/A16_THETA13_PREDICTION')

import numpy as np
from lyd20_fit_pinned import (extra_forms, M_u_unified, M_d_unified, ckm_from_M)

# LYD20 best-fit (line 1531-1538)
tau_LYD = -0.2123 + 1.5201j
beta_u_alpha_u   = 325.6502
gamma_u_alpha_u  = 2427.3101
delta_u_alpha_u  = 219.3019
beta_d_alpha_d   = 466.6990
gamma_d_alpha_d  = -234.0473
delta_d_alpha_d  = 2.3388

print(f"LYD20 best-fit tau = {tau_LYD}")
print(f"alpha_u_v_u = 2.7758e-5 GeV; alpha_d_v_d = 1.72111e-5 GeV (overall scales)")
print()

F = extra_forms(tau_LYD)

# Up sector
Mu = M_u_unified(F, alpha_u=1.0, beta_u=beta_u_alpha_u,
                 gamma_u=gamma_u_alpha_u, delta_u=delta_u_alpha_u)
sv_u = np.linalg.svd(Mu, compute_uv=False)
sv_u = np.sort(sv_u)
print(f"Up-sector singular values (alpha_u=1):  {sv_u}")
print(f"  m_u/m_c (predicted) = {sv_u[0]/sv_u[1]:.6f}   (LYD20: 0.001929)")
print(f"  m_c/m_t (predicted) = {sv_u[1]/sv_u[2]:.6f}   (LYD20: 0.002725)")
print()

# Down sector
Md = M_d_unified(F, alpha_d=1.0, beta_d=beta_d_alpha_d,
                 gamma_d=gamma_d_alpha_d, delta_d=delta_d_alpha_d)
sv_d = np.linalg.svd(Md, compute_uv=False)
sv_d = np.sort(sv_d)
print(f"Down-sector singular values (alpha_d=1):  {sv_d}")
print(f"  m_d/m_s (predicted) = {sv_d[0]/sv_d[1]:.6f}   (LYD20: 0.050345)")
print(f"  m_s/m_b (predicted) = {sv_d[1]/sv_d[2]:.6f}   (LYD20: 0.017726)")
print()

# CKM
V, Vus, Vcb, Vub, J_q, _, _ = ckm_from_M(Mu, Md)
print(f"CKM elements:")
print(f"  |V_us| = {Vus:.5f}   (LYD20: 0.22513 from sin(theta12_q))")
print(f"  |V_cb| = {Vcb:.5f}   (LYD20: 0.03888 from sin(theta23_q))")
print(f"  |V_ub| = {Vub:.5f}   (LYD20: 0.00337 from sin(theta13_q))")
print(f"  J_CKM  = {J_q:+.4e}")
print()

# Print verdict
checks = []
checks.append(("m_u/m_c", sv_u[0]/sv_u[1], 0.001929, 0.10))
checks.append(("m_c/m_t", sv_u[1]/sv_u[2], 0.002725, 0.10))
checks.append(("m_d/m_s", sv_d[0]/sv_d[1], 0.050345, 0.10))
checks.append(("m_s/m_b", sv_d[1]/sv_d[2], 0.017726, 0.10))
checks.append(("|V_us|",  Vus, 0.22752, 0.10))
checks.append(("|V_cb|",  Vcb, 0.038886, 0.10))
checks.append(("|V_ub|",  Vub, 0.003379, 0.20))

print("=" * 60)
print("SANITY CHECK")
print("=" * 60)
n_pass = 0
for name, pred, ref, tol in checks:
    pct = abs(pred - ref) / ref * 100
    status = "PASS" if pct < tol * 100 else "FAIL"
    if status == "PASS":
        n_pass += 1
    print(f"  {name}:  {pred:.5e}  vs LYD20 {ref:.5e}  ({pct:5.2f}%)  {status}")
print(f"  -- {n_pass}/{len(checks)} pass")
