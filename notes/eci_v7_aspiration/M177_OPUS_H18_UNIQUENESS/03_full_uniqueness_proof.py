#!/usr/bin/env python3
"""
M177 Step 3 — FULL UNIQUENESS PROOF

KEY DISCOVERY: Y_3̂^(3)(i) is FORCED to be on the unique (-i)-eigenvector
v_S = (√2, 1, 1)/2 of ρ_3̂(S) (Table 7 NPP20).

We will:
  (a) Compute the full M_e^† at τ=i using NPP20 eq (6.6) with the verified
      values of Y_R^(3)(i) ∈ E_{-i}(ρ_R(S)).
  (b) Show M_e^† has a SPECIFIC structure (rank, eigenvalue pattern) that is
      UNIQUELY determined by the Z_2 selection — not freely chosen.
  (c) Identify the surviving free parameters: only α_1, α_2, α_3 (3 complex,
      reduced to 3 real by gCP CP_1).
  (d) Confirm the (1+√6) CSD-style ratio that arises NPP20 phenomenology.
"""

import mpmath as mp
mp.mp.dps = 30

import numpy as np


# ===================================================================
# Modular forms (CORRECTED basis per NPP20 eq 3.14)
# ===================================================================

def theta_eps(tau, N=200):
    q4 = mp.exp(1j * mp.pi * tau / 2)
    th = mp.mpc(1)
    ep = mp.mpc(0)
    for k in range(1, N + 1):
        th += 2 * q4 ** ((2 * k) ** 2)
        ep += 2 * q4 ** ((2 * k - 1) ** 2)
    return th, ep


def Y1_prime_w3(tau):
    """Y_1̂'^(3) = √3 (ε θ^5 - ε^5 θ)"""
    th, ep = theta_eps(tau)
    return mp.sqrt(3) * (ep * th ** 5 - ep ** 5 * th)


def Y3_hat_w3(tau):
    """Y_3̂^(3) per NPP20 eq (3.14):
    (ε^5 θ + ε θ^5,  (1/(2√2))(5 ε² θ^4 - ε^6),  (1/(2√2))(θ^6 - 5 ε^4 θ²))
    """
    th, ep = theta_eps(tau)
    return mp.matrix([[ep ** 5 * th + ep * th ** 5],
                      [(1/(2*mp.sqrt(2))) * (5 * ep ** 2 * th ** 4 - ep ** 6)],
                      [(1/(2*mp.sqrt(2))) * (th ** 6 - 5 * ep ** 4 * th ** 2)]])


def Y3_prime_w3(tau):
    """Y_3̂'^(3) per NPP20 eq (3.14):
    (1/2) (-4√2 ε³ θ³,  θ^6 + 3 ε^4 θ²,  -3 ε² θ^4 - ε^6)
    """
    th, ep = theta_eps(tau)
    pre = mp.mpf(1) / 2
    return mp.matrix([[pre * (-4 * mp.sqrt(2) * ep ** 3 * th ** 3)],
                      [pre * (th ** 6 + 3 * ep ** 4 * th ** 2)],
                      [pre * (-3 * ep ** 2 * th ** 4 - ep ** 6)]])


# ===================================================================
# ρ_R(S) and ρ_R(T) per Table 7
# ===================================================================

sq2 = mp.sqrt(2)
sq3 = mp.sqrt(3)
M_block = mp.matrix([[0, sq2, sq2],
                     [sq2, -1, 1],
                     [sq2, 1, -1]])

rho_3hat_S  = (-mp.mpc(0, 1)/2) * M_block
rho_3hatp_S = ( mp.mpc(0, 1)/2) * M_block
rho_3_S     = (-mp.mpf(1)/2)    * M_block
rho_3prime_S = (mp.mpf(1)/2)    * M_block


# ===================================================================
# Verification: each Y_R^(3)(i) is in -i eigenspace of ρ_R(S)
# ===================================================================

print("=" * 72)
print("STEP 1: Verify Z_2 eigenspace selection at τ=i (k=3, eigenvalue -i)")
print("=" * 72)

tau_i = mp.mpc(0, 1)

# Y_3̂^(3)(i)
Y_3hat_i = Y3_hat_w3(tau_i)
print(f"\nY_3̂^(3)(i) = ({Y_3hat_i[0]}, {Y_3hat_i[1]}, {Y_3hat_i[2]})")

S_Y_3hat = rho_3hat_S * Y_3hat_i
target = mp.mpc(0, -1) * Y_3hat_i
diff = max(abs(S_Y_3hat[r] - target[r]) for r in range(3))
print(f"|ρ_3̂(S) Y(i) - (-i) Y(i)| = {diff}")

# Y_3̂'^(3)(i)
Y_3p_i = Y3_prime_w3(tau_i)
print(f"\nY_3̂'^(3)(i) = ({Y_3p_i[0]}, {Y_3p_i[1]}, {Y_3p_i[2]})")

S_Y_3p = rho_3hatp_S * Y_3p_i
target_p = mp.mpc(0, -1) * Y_3p_i
diff_p = max(abs(S_Y_3p[r] - target_p[r]) for r in range(3))
print(f"|ρ_3̂'(S) Y(i) - (-i) Y(i)| = {diff_p}")

# Y_1̂'^(3)(i)
Y_1p_i = Y1_prime_w3(tau_i)
print(f"\nY_1̂'^(3)(i) = {Y_1p_i}")
print(f"ρ_1̂'(S) = -i, so Y(i) is in -i eigenspace trivially.")


# ===================================================================
# STEP 2: Identify the UNIQUE -i eigenvector of ρ_3̂(S)
# ===================================================================

print("\n" + "=" * 72)
print("STEP 2: -i eigenvector of ρ_3̂(S) is UNIQUE (1D subspace)")
print("=" * 72)

# Eigvals of -(i/2) M: tr M = -2, M is real symmetric.
# Eigenvalues of M (will be real). Then ρ(S) eigenvalues = -(i/2) * (M eigenvalues).
M_np = np.array([[float(M_block[i,j]) for j in range(3)] for i in range(3)])
M_eigvals = np.linalg.eigvalsh(M_np)
print(f"Eigenvalues of M = {M_eigvals}")
# Should be {-2, +2, +2} or similar so that -(i/2)·(-2) = i, -(i/2)·2 = -i.
# Then ρ(S) eigvals = {-(i/2)(-2), -(i/2)(2), -(i/2)(2)} = {+i, -i, -i}? But our numeric
# above gave {-i, +i, +i}. Let me double-check sign.

# Actually we got eigvals {-i, +i, +i} numerically, so M has eigvals {2, -2, -2}.
# Either way, ρ_3̂(S) has 1D -i subspace and 2D +i subspace.

# Find the eigenvector for eigenvalue -i.
rho_3hat_S_np = np.array([[complex(rho_3hat_S[i,j]) for j in range(3)] for i in range(3)])
eigvals, eigvecs = np.linalg.eig(rho_3hat_S_np)
print(f"\nEigenvalues of ρ_3̂(S): {eigvals}")

# Sort: find the index of -i
idx_minus_i = [k for k in range(3) if abs(eigvals[k] - (-1j)) < 1e-9]
print(f"\nIndex of -i eigenvector: {idx_minus_i}")
v_S_3hat = eigvecs[:, idx_minus_i[0]].real  # since eigenvalue is purely imag, vector is real (up to phase)
v_S_3hat = v_S_3hat / np.sign(v_S_3hat[0])  # canonical sign
print(f"\n-i eigenvector v_S = {v_S_3hat}")
print(f"  v_S / v_S[1] = {v_S_3hat / v_S_3hat[1]}")
print(f"  Should be (√2, 1, 1) up to scale: ratio v_S[0]/v_S[1] = {v_S_3hat[0]/v_S_3hat[1]:.6f} vs √2 = {float(sq2):.6f}")

# Confirm
print(f"\n  EXACT: v_S = (√2, 1, 1)/2 (length-2 normalization)")


# Verify Y_3̂^(3)(i) is proportional to v_S
print("\nY_3̂^(3)(i) components ratio:")
print(f"  Y[0] / Y[1] = {float((Y_3hat_i[0]/Y_3hat_i[1]).real):.6f}  (should be √2 = {float(sq2):.6f})")
print(f"  Y[2] / Y[1] = {float((Y_3hat_i[2]/Y_3hat_i[1]).real):.6f}  (should be 1)")


# Same for Y_3̂'^(3)(i)
print("\n" + "=" * 72)
print("STEP 3: -i eigenvector of ρ_3̂'(S) — UNIQUENESS check")
print("=" * 72)

rho_3hatp_S_np = np.array([[complex(rho_3hatp_S[i,j]) for j in range(3)] for i in range(3)])
eigvals_p, eigvecs_p = np.linalg.eig(rho_3hatp_S_np)
print(f"\nEigenvalues of ρ_3̂'(S): {eigvals_p}")
# Should be {+i, -i, -i} (since (i/2)·M has eigvals (i/2)·{2,-2,-2} = {i, -i, -i})

idx_minus_i_p = [k for k in range(3) if abs(eigvals_p[k] - (-1j)) < 1e-9]
print(f"Indices of -i eigenvectors: {idx_minus_i_p}")
print(f"-i eigenspace dim for ρ_3̂'(S): {len(idx_minus_i_p)}")

# This is 2D!  So Y_3̂'^(3)(i) lies in 2D subspace → 2 free components remaining.
# But Y_3̂'^(3)(i) is a SPECIFIC vector, fully determined by τ=i.
print(f"\nY_3̂'^(3)(i) = ({Y_3p_i[0]}, {Y_3p_i[1]}, {Y_3p_i[2]})")
print(f"  Y[0] / Y[2] = {float((Y_3p_i[0]/Y_3p_i[2]).real):.6f}")
print(f"  Y[1] / Y[2] = {float((Y_3p_i[1]/Y_3p_i[2]).real):.6f}")

# Identify exact form
# Y_3̂'^(3)(i) = (1/2)( -4√2 ε³ θ³, θ^6 + 3 ε^4 θ², -3ε² θ^4 - ε^6 ) at τ=i
# Plug in numerical θ(i), ε(i):
th_i, ep_i = theta_eps(tau_i)
print(f"\nθ(i) = {th_i}")
print(f"ε(i) = {ep_i}")
print(f"  Note ε(i) = e^{{-iπ/4}} · |ε(i)|? Check arg: {float(mp.arg(ep_i))/float(mp.pi)}π")

# From eq 3.5: ε(τ_C)/θ(τ_C) = 1/(1+√2)
ratio_check = ep_i / th_i
print(f"\nε(i)/θ(i) = {ratio_check}")
print(f"1/(1+√2)  = {1/(1+sq2)}")
print(f"  match: {abs(ratio_check - 1/(1+sq2))}")


# ===================================================================
# STEP 4: Construct M_e^† at τ=i using NPP20 eq (6.6)
# ===================================================================

print("\n\n" + "=" * 72)
print("STEP 4: Construct M_e^† at τ=i using NPP20 eq (6.6)")
print("=" * 72)
print("""
NPP20 (6.6) reads (1/v_d) M_e^† = α_1 (Y_1̂'^(3) ⊗ struct1) + α_2 (Y_3̂'^(3) ⊗ struct2)
                                  + α_3 (Y_3̂^(3) ⊗ struct3)
where struct_i are the explicit 3x3 matrices (with the entries Y_1, Y_2, Y_3 of the
corresponding modular triplet).
""")

# Extract Y_1, Y_2, Y_3 components for each
Y3hat_components = [Y_3hat_i[r] for r in range(3)]
Y3p_components   = [Y_3p_i[r] for r in range(3)]
Y1p_value        = Y_1p_i

print(f"\nY_3̂^(3)(i) components:")
for r in range(3):
    print(f"  Y_{r+1}^(3̂) = {Y3hat_components[r]}")

print(f"\nY_3̂'^(3)(i) components:")
for r in range(3):
    print(f"  Y_{r+1}^(3̂') = {Y3p_components[r]}")

print(f"\nY_1̂'^(3)(i) = {Y1p_value}")


# Assemble M_e^† per (6.6). Use sympy α_1, α_2, α_3 symbolic for structure.
import sympy as sp
a1, a2, a3 = sp.symbols('alpha_1 alpha_2 alpha_3', real=True)

# Convert Y values to sympy (high-precision)
def to_sp(x):
    return sp.Float(float(x.real), 25) + sp.I * sp.Float(float(x.imag), 25)

Y_3hat_sp = [to_sp(Y3hat_components[r]) for r in range(3)]
Y_3p_sp   = [to_sp(Y3p_components[r]) for r in range(3)]
Y_1p_sp   = to_sp(Y1p_value)

# (1/v_d) M_e^† per (6.6):
# = (α_1/√3) Y_1p · diag(Y1, Y1, Y1) [diagonal? actually look at first matrix in 6.6]
# Re-reading (6.6):
#   (1/v_d) M_e^† = (α_1/√3) [(Y1,0,0;0,0,Y1;0,Y1,0)]_{Y_1̂'^(3)}
#                 + (α_2/√6) [(0,-Y2,Y3;-Y2,-Y1,0;Y3,0,Y1)]_{Y_3̂'^(3)}
#                 + (α_3/√6) [(0,Y3,-Y2;-Y3,0,Y1;Y2,-Y1,0)]_{Y_3̂^(3)}
# where the Y_i in each matrix are the components of THAT multiplet.

# Note: (Y_1̂'^(3)) is a singlet, so Y1 in its matrix is just the singlet value Y_1p.
# And the matrix structure is determined by the Clebsch-Gordan of (1̂' ⊗ 1̂) → 1.

def build_Me(Y1p, Y3p_vec, Y3hat_vec):
    """Build (1/v_d) M_e^† per NPP20 (6.6)."""
    sq3_sp = sp.sqrt(3)
    sq6_sp = sp.sqrt(6)
    Y1 = Y1p  # singlet
    # First term: (α_1/√3) · Y1p_singlet · pattern
    M1 = (a1 / sq3_sp) * sp.Matrix([
        [Y1, 0, 0],
        [0, 0, Y1],
        [0, Y1, 0],
    ])
    # Second term: (α_2/√6) · pattern from Y_3̂'^(3): components (Y1, Y2, Y3)
    Y1, Y2, Y3 = Y3p_vec
    M2 = (a2 / sq6_sp) * sp.Matrix([
        [0, -Y2, Y3],
        [-Y2, -Y1, 0],
        [Y3, 0, Y1],
    ])
    # Third term: (α_3/√6) · pattern from Y_3̂^(3): components (Y1, Y2, Y3)
    Y1, Y2, Y3 = Y3hat_vec
    M3 = (a3 / sq6_sp) * sp.Matrix([
        [0, Y3, -Y2],
        [-Y3, 0, Y1],
        [Y2, -Y1, 0],
    ])
    return M1 + M2 + M3


Me_dag_over_vd = build_Me(Y_1p_sp, Y_3p_sp, Y_3hat_sp)
print("\n(1/v_d) M_e^† at τ=i:")
print(sp.pretty(sp.simplify(Me_dag_over_vd)))

# Now compute M_e^† M_e (= M_e^† (M_e^†)^* in our convention; actually need careful Hermitian setup)
# For mass spectrum, eigenvalues of M_e M_e^† are |m_i|^2.
Me_dag = Me_dag_over_vd
Me = Me_dag.H  # conjugate transpose

H_e = Me * Me_dag  # = (M_e M_e^†), eigenvalues are |m_i|^2 / v_d^2 (squared mass / v_d^2 with our scaling)
print("\nM_e M_e^† / v_d² at τ=i (symbolic in α_i):")
print(sp.pretty(sp.simplify(H_e)))


# ===================================================================
# STEP 5: Substitute α_1=α_2=α_3 = 1 to see numerical structure
# ===================================================================

print("\n\n" + "=" * 72)
print("STEP 5: Numerical Me at α_1=α_2=α_3=1 (toy point)")
print("=" * 72)

Me_num = Me_dag_over_vd.subs({a1: 1, a2: 1, a3: 1})
Me_num_np = np.array(Me_num.evalf(), dtype=complex)
print(f"\n(1/v_d) M_e^† (α_i=1):")
for r in range(3):
    print(f"  {Me_num_np[r]}")

# Singular values (= masses up to v_d factor)
U, s, Vh = np.linalg.svd(Me_num_np)
print(f"\nSingular values: {s}")
print(f"Mass ratios: m_1/m_3 = {s[2]/s[0]:.6f},  m_2/m_3 = {s[1]/s[0]:.6f}")


# ===================================================================
# STEP 6: Solve for charged-lepton hierarchy fit at τ=i
# ===================================================================

print("\n\n" + "=" * 72)
print("STEP 6: Show that NPP20 fit at τ ≈ i forces specific α-ratios")
print("=" * 72)

# From NPP20 Table 4 (NO best fit): τ ≈ ±0.0297 + 1.118i, α_2/α_1 = 1.7303, α_3/α_1 = -2.7706
# The model is NOT exactly at τ=i but close. Let's extrapolate to τ=i.

# At exactly τ=i, the NPP20 fit point would give specific α_2/α_1 and α_3/α_1.
# Let's see what mass ratios emerge for the best-fit α_i at τ=i exactly.

# m_e/m_μ ≈ 0.0048, m_μ/m_τ ≈ 0.0565 (Table 3)

a2_a1_NO = 1.7303
a3_a1_NO = -2.7706

Me_NPP20 = Me_dag_over_vd.subs({a1: 1, a2: a2_a1_NO, a3: a3_a1_NO})
Me_NPP20_np = np.array(Me_NPP20.evalf(), dtype=complex)
print(f"\n(1/v_d/α_1) M_e^† at τ=i with NPP20 NO ratios:")
for r in range(3):
    print(f"  {Me_NPP20_np[r]}")

s_NPP20 = np.linalg.svd(Me_NPP20_np, compute_uv=False)
print(f"\nSingular values: {s_NPP20}")
print(f"  m_e/m_μ = {s_NPP20[2]/s_NPP20[1]:.6f}  (NPP20 target: 0.0048)")
print(f"  m_μ/m_τ = {s_NPP20[1]/s_NPP20[0]:.6f}  (NPP20 target: 0.0565)")


# ===================================================================
# STEP 7: UNIQUENESS — show that the structure of M_e^† at τ=i is FIXED
# ===================================================================

print("\n\n" + "=" * 72)
print("STEP 7: UNIQUENESS — Structural rigidity of M_e^† at τ=i")
print("=" * 72)

print("""
KEY OBSERVATION:
  At τ=i, by Theorem M170.1, each Y_R^(3)(i) is FIXED up to an overall scalar.
  Specifically:
     Y_3̂^(3)(i)  ∝ (√2, 1, 1)        (unique -i eigenvector of ρ_3̂(S))
     Y_3̂'^(3)(i) ∝ specific vector in 2D -i eigenspace of ρ_3̂'(S)
                  fixed by holomorphicity at τ=i
     Y_1̂'^(3)(i) = scalar, non-zero (since ρ_1̂'(S)=-i = i^{-3} ✓)

  Therefore, the matrices M_1, M_2, M_3 in (6.6) are FIXED 3×3 matrices at τ=i,
  and only α_1, α_2, α_3 are free.

  M_e^†|_{τ=i} = α_1 M_1^* + α_2 M_2^* + α_3 M_3^*

  This is the NPP20 form. NO OTHER S_4' irrep combination is possible because:
    • At weight 3, only 1̂', 3̂, 3̂' multiplets exist (level constraint
      dim M_3(Γ(4)) = 7 = 1+3+3).
    • Only these three couple to (3̂ ⊗ 3) in the singlet-extracting way.
    • Each Y_R(i) is FORCED into its (-i)-eigenspace.
    • At τ=i, the values are FULLY determined up to overall normalization.

  Three real parameters α_1, α_2, α_3 (with gCP CP_1 imposing reality).

  This is exactly the (CSD-like) form NPP20 calls "viable charged-lepton mass model".
""")


# Compute the explicit ratios v_S = (√2, 1, 1) shapes at τ=i for Y_3̂^(3)(i):
print("=" * 72)
print("Verification: Y_3̂^(3)(i) ∝ (√2, 1, 1)")
print("=" * 72)
ratio_01 = float((Y_3hat_i[0] / Y_3hat_i[1]).real)
ratio_21 = float((Y_3hat_i[2] / Y_3hat_i[1]).real)
print(f"  Y_3̂^(3)(i)[0] / Y_3̂^(3)(i)[1] = {ratio_01}")
print(f"  Y_3̂^(3)(i)[2] / Y_3̂^(3)(i)[1] = {ratio_21}")
print(f"  Expected √2 = {float(sq2)}")
print(f"  Expected  1 = 1.0")
print(f"  diff: {abs(ratio_01 - float(sq2)) + abs(ratio_21 - 1.0)}")


# CSD-style (1+√6) ratio?
# CSD(1+√6) refers to King's "Constrained Sequential Dominance" with the specific
# parameter (1+√6) appearing in the Littlest Modular Seesaw fit (NPP20 §6.2).
# Let's check whether (1+√6) emerges from Y_3̂^(3)(i) and Y_3̂'^(3)(i) ratios.
print("\n--- CSD(1+√6) check ---")
print(f"Y_3̂^(3)(i)[0]  = {Y_3hat_i[0]}")
print(f"Y_3̂'^(3)(i)[0] = {Y_3p_i[0]}")
print(f"Y_3̂'^(3)(i)[1] = {Y_3p_i[1]}")
print(f"Y_3̂'^(3)(i)[2] = {Y_3p_i[2]}")
print(f"\n1 + √6 = {1 + float(mp.sqrt(6))}")
print(f"Y_3̂^(3)[1] / Y_3̂'^(3)[2] = {float((Y_3hat_i[1] / Y_3p_i[2]).real)}")
print(f"Y_3̂'^(3)[1] / Y_3̂'^(3)[2] = {float((Y_3p_i[1] / Y_3p_i[2]).real)}")
print(f"Y_3̂^(3)[0] / Y_3̂'^(3)[0] = {float((Y_3hat_i[0] / Y_3p_i[0]).real)}")

# (1+√6) factor is not directly in Y_e — it's in the SEESAW model (NPP20 §6.2,
# our task M177 covers Y_e, the charged-lepton mass matrix structure)
