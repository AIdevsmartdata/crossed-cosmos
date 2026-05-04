"""
Debug: Check matrix conventions in SVD for V_CKM.

In LYD20 convention: W_q = q^c M Q H
  M acts on Q from the right, q^c from the left.
  So if q^c is a row vector and Q is a column vector, M is a 3×3 matrix
  where row i corresponds to right-handed quark q^c_i.

Mass matrix M: (n_q^c) × (n_Q)
  SVD: M = U_L Σ U_R†
  M†M = U_R Σ² U_R†    → U_R diagonalizes M†M, columns are RIGHT eigenvectors
  MM† = U_L Σ² U_L†    → U_L diagonalizes MM†, columns are LEFT eigenvectors

In the mass basis:
  u_mass = U_R† u_flavor   (for Q = left-handed quarks)
  u^c_mass = U_L† u^c_flavor   (for right-handed quarks)

V_CKM mixes the LEFT-HANDED quarks:
  V_CKM = U_{uL}† U_{dL}

But M_u = U_{uL} Σ_u U_{uR}†  → U_{uL} is the LEFT singular vectors (= U from SVD(M_u))
      M_d = U_{dL} Σ_d U_{dR}†  → U_{dL} is the LEFT singular vectors (= U from SVD(M_d))

So V_CKM = U_{uL}† U_{dL}  (using LEFT singular vectors, NOT right)

Let me check both conventions.
"""

import numpy as np
from numpy import pi, sqrt, exp
import sys
sys.path.insert(0, '/root/crossed-cosmos/notes/eci_v7_aspiration/H3')
from mass_matrix import M_u, M_d

TAU_LYD20 = -0.4999 + 0.8958j
TAU_CM    = 1j

# LYD20 best-fit parameters
alpha_u = 1.0
beta_u  = 62.2142
gamma_u = 0.00104

alpha_d  = 1.0
beta_d   = 0.7378
gamma_d1 = 1.4946
gamma_d2 = -0.1958 - 0.2762j

Mu = M_u(TAU_LYD20, alpha_u, beta_u, gamma_u)
Md = M_d(TAU_LYD20, alpha_d, beta_d, gamma_d1, gamma_d2)

print("M_u at LYD20 best-fit τ (absolute values):")
print(np.abs(Mu))

print("\nM_d at LYD20 best-fit τ (absolute values):")
print(np.abs(Md))

# SVD: M = U @ diag(s) @ Vh
# U columns = left singular vectors (=U_L)
# Vh rows   = right singular vectors (= U_R†)
from scipy.linalg import svd

Uu, su, Uvh = svd(Mu)   # M_u = Uu @ diag(su) @ Uvh
Ud, sd, Dvh = svd(Md)   # M_d = Ud @ diag(sd) @ Dvh

# Sort by ascending singular values (lightest first)
iu = np.argsort(su)
id_ = np.argsort(sd)
su = su[iu]; Uu = Uu[:, iu]; Uvh = Uvh[iu, :]
sd = sd[id_]; Ud = Ud[:, id_]; Dvh = Dvh[id_, :]

print(f"\nSingular values M_u (sorted ascending): {su}")
print(f"Singular values M_d (sorted ascending): {sd}")

print(f"\nm_u/m_t = {su[0]/su[2]:.4e}")
print(f"m_c/m_t = {su[1]/su[2]:.4e}")
print(f"m_d/m_b = {sd[0]/sd[2]:.4e}")
print(f"m_s/m_b = {sd[1]/sd[2]:.4e}")

# LYD20 reports: m_u/m_c = 0.00204, m_c/m_t = 0.00268, m_d/m_s = 0.05182, m_s/m_b = 0.01309
print(f"\nLYD20 reported: m_u/m_c = 0.00204, m_c/m_t = 0.00268")
print(f"Our computed:   m_u/m_c = {su[0]/su[1]:.5f}, m_c/m_t = {su[1]/su[2]:.5f}")
print(f"LYD20 reported: m_d/m_s = 0.05182, m_s/m_b = 0.01309")
print(f"Our computed:   m_d/m_s = {sd[0]/sd[1]:.5f}, m_s/m_b = {sd[1]/sd[2]:.5f}")

# Check BOTH V_CKM conventions
# Convention 1: V = U_uL† U_dL  (left singular vectors)
V_left = Uu.conj().T @ Ud
print(f"\nConvention 1: V = U_uL† U_dL (left singular vectors)")
print(f"|V_CKM| =")
print(np.abs(V_left))
print(f"  |V_us| = {np.abs(V_left[0,1]):.5f}")

# Convention 2: V = U_uR† U_dR  (right singular vectors)
# U_R = Uvh.conj().T  (rows of Vh are right sing. vecs, columns of Vh† = right sing. vecs)
U_uR = Uvh.conj().T   # shape (3,3), columns = right sing. vecs of M_u
U_dR = Dvh.conj().T
V_right = U_uR.conj().T @ U_dR
print(f"\nConvention 2: V = U_uR† U_dR (right singular vectors)")
print(f"|V_CKM| =")
print(np.abs(V_right))
print(f"  |V_us| = {np.abs(V_right[0,1]):.5f}")

# Convention 3: M_u is defined as q^c M Q, so for mass eigenvalues:
#   m_eigenvalues are sing values of M (= M_u in our code)
#   LEFT mixing (from Q side) = U_L from SVD of M^T = V from SVD of M
#   Actually: SVD of M = U Σ V†  →  M = U Σ V†
#   The LEFT-handed Q rotation is V (right singular vectors of M, which are LEFT-handed in the Lagrangian sense when M appears as q_L M q_R)
#
# Wait: in the superpotential convention W = u^c_i M_{ij} Q_j
# This is (u^c)^T M Q. The mass matrix M acts on Q from the right.
# Diagonalizing: u^c → U†u^c, Q → V Q  (where M = U Σ V†)
# The PHYSICAL CKM comes from Q rotation, which is V (= right singular vectors of M).
# So V_CKM = V_u† V_d where V_u, V_d are RIGHT singular vectors of M_u, M_d.

# But scipy SVD gives M = U @ diag(s) @ Vh, so RIGHT singular vectors are rows of Vh
# → columns of Vh.conj().T
# Already done above as U_uR, U_dR

print(f"\nConvention 3: same as Convention 2 (right sing vecs of M)")
print(f"  should give same result.")

# Convention 4: M.T convention (some papers define M_u differently)
# If M is written as Q M u^c (transposed from our notation):
Mu_T = Mu.T
Md_T = Md.T
UuT, suT, UvhT = svd(Mu_T)
UdT, sdT, DvhT = svd(Md_T)
iuT = np.argsort(suT); idT = np.argsort(sdT)
UuT = UuT[:, iuT]; UdT = UdT[:, idT]
V_transposed = UuT.conj().T @ UdT
print(f"\nConvention 4: V = U_uL† U_dL with M transposed")
print(f"|V_CKM| =")
print(np.abs(V_transposed))
print(f"  |V_us| = {np.abs(V_transposed[0,1]):.5f}")

# Target from LYD20: |V_us| ~ 0.22731, |V_cb| ~ 0.04873, |V_ub| ~ 0.00298
print(f"\nTarget: |V_us| = 0.22731, |V_cb| = 0.04873, |V_ub| = 0.00298")
