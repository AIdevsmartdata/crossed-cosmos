#!/usr/bin/env python3
"""
M170 step 4 — Search for the correct ρ_3̂(S) matrix that makes Y_3̂^(3)(i)
an eigenvector with eigenvalue -i.

Key insight: NPP20 layout's OCR is bad, but the M_block-times-i/2 form is consistent
with group relations. There must be a basis convention issue.

Constraints:
  • ρ(T) = diag(i, -1, 1) — fixed by T-action on Y_3̂^(3) entries (verified)
  • ρ(S)² = -I (R-odd irrep)
  • (ρ(S) ρ(T))³ = +I
  • ρ(S) is symmetric (Table 7 caption)
  • ρ(S)†ρ(S) = I (unitary)

Test: at τ=i, Y_3̂^(3)(i) is computed from NPP20 formula. We require:
  ρ(S) Y_3̂^(3)(i) = -i · Y_3̂^(3)(i)
"""

import mpmath as mp
mp.mp.dps = 30
import numpy as np
import sympy as sp


# Compute Y_3̂^(3)(i) numerically
def theta_eps(tau, N=80):
    q4 = mp.exp(1j * mp.pi * tau / 2)
    th = mp.mpc(1)
    ep = mp.mpc(0)
    for k in range(1, N + 1):
        th += 2 * q4 ** ((2 * k) ** 2)
        ep += 2 * q4 ** ((2 * k - 1) ** 2)
    return th, ep


tau_C = mp.mpc(0, 1)
th_C, ep_C = theta_eps(tau_C)

# Y_3̂^(3)(i) — three components:
pre = 1 / (2 * mp.sqrt(2))
Y1 = pre * (ep_C ** 5 * th_C + ep_C * th_C ** 5)
Y2 = pre * (5 * ep_C ** 2 * th_C ** 4 - ep_C ** 6)
Y3 = pre * (th_C ** 6 - 5 * ep_C ** 4 * th_C ** 2)

Y_vec = np.array([complex(Y1), complex(Y2), complex(Y3)])
print(f"Y_3̂^(3)(i) numeric = {Y_vec}")
print(f"  norm = {np.linalg.norm(Y_vec)}")
print(f"\nY[0]/Y[1] = {Y_vec[0]/Y_vec[1]}")
print(f"Y[1]/Y[2] = {Y_vec[1]/Y_vec[2]}")
# Note: Y[1] == Y[2] numerically — strong hint about basis structure

# Verify directly:
print(f"\nNoting Y_3̂^(3)(i) entries:")
print(f"  [0] = (1/(2√2)) ε(i) θ(i) (θ(i)⁴ + ε(i)⁴) = {(1/(2*mp.sqrt(2)))*ep_C*th_C*(th_C**4 + ep_C**4)}")
print(f"  [1] = (1/(2√2)) ε²(i) (5θ(i)⁴ - ε(i)⁴) = {(1/(2*mp.sqrt(2)))*ep_C**2*(5*th_C**4 - ep_C**4)}")
print(f"  [2] = (1/(2√2)) θ²(i) (θ(i)⁴ - 5ε(i)⁴) = {(1/(2*mp.sqrt(2)))*th_C**2*(th_C**4 - 5*ep_C**4)}")

# Hmm, [0] = εθ(θ⁴+ε⁴)/(2√2) = εθ⁵ + ε⁵θ all divided.
# Check [1]=[2] symmetry: [1]=ε²(5θ⁴-ε⁴)/(2√2), [2]=θ²(θ⁴-5ε⁴)/(2√2)
# At τ=i, ratio ε/θ = √2-1 ≈ 0.414. Let's compute:
r = ep_C / th_C
print(f"\nε/θ at i = {r}")
ratio_12 = (5 - r**4) / (1/r**2 * (1/r**4 - 5))
# Actually just compute Y[1]/Y[2]:
print(f"Y[1]/Y[2] (from formula) = {(ep_C**2*(5*th_C**4 - ep_C**4)) / (th_C**2*(th_C**4 - 5*ep_C**4))}")
# This should be 1 from our numerics


# ============================================================
# Search candidate ρ_3̂(S) — symmetric, unitary, S²=-I, with given T
# We'll parametrize all symmetric S that satisfy these and search for
# the one that has Y_vec as eigenvector with eigenvalue -i.
# ============================================================
print("\n" + "=" * 70)
print("Search for ρ(S) with Y_3̂^(3)(i) as -i eigenvector")
print("=" * 70)

# Most general symmetric 3x3 complex matrix with S² = -I:
# S = [[a, b, c], [b, d, e], [c, e, f]] with appropriate constraints.

# Numerical approach: solve eigvec[Y_vec, -i] given S² = -I and (ST)³ = I
# S T S T S T = I  ⟹  S T S T = T⁻¹ S⁻¹ ⟹ ... non-linear.

# Simpler: Try all variants of M_block · diag(±1, ±1, ±1) and similar.
M_block = np.array([[0, np.sqrt(2), np.sqrt(2)],
                    [np.sqrt(2), -1, 1],
                    [np.sqrt(2), 1, -1]], dtype=complex)

T_3hat = np.diag([1j, -1, 1])

# Candidates: ρ(S) = α · D · M · D' where D, D' are sign diagonals
# This is getting big. Let me just enumerate sign-diag conjugations of base.

print("\nTrying transformed bases ρ(S) = α (D M D⁻¹) with α=-i/2:")
import itertools
for signs in itertools.product([1, -1], repeat=3):
    D = np.diag(signs).astype(complex)
    M_alt = D @ M_block @ D
    S_test = (-1j / 2) * M_alt
    # Test S² = -I
    S2_diff = np.linalg.norm(S_test @ S_test + np.eye(3))
    # Test (ST)³ = I
    ST = S_test @ T_3hat
    ST3_diff = np.linalg.norm(ST @ ST @ ST - np.eye(3))
    # Test eigenvector:
    SY = S_test @ Y_vec
    target = -1j * Y_vec
    eigvec_diff = np.linalg.norm(SY - target)
    if S2_diff < 1e-10 and ST3_diff < 1e-10:
        print(f"  signs={signs}: S²=−I✓, (ST)³=I✓, |SY+iY|={eigvec_diff:.6f}")

# Try permutation conjugations
print("\nTrying permutation-conjugated M:")
from itertools import permutations
for perm in permutations(range(3)):
    P = np.zeros((3, 3), dtype=complex)
    for i, j in enumerate(perm):
        P[i, j] = 1
    M_perm = P @ M_block @ P.T
    S_test = (-1j / 2) * M_perm
    S2_diff = np.linalg.norm(S_test @ S_test + np.eye(3))
    if S2_diff < 1e-10:
        # Check (ST)³
        ST = S_test @ T_3hat
        ST3_diff = np.linalg.norm(ST @ ST @ ST - np.eye(3))
        SY = S_test @ Y_vec
        eigvec_diff = np.linalg.norm(SY - (-1j) * Y_vec)
        print(f"  perm={perm}: S²=−I✓, |(ST)³-I|={ST3_diff:.4f}, |SY+iY|={eigvec_diff:.6f}")


# ============================================================
# Key insight: maybe check if Y_3̂^(3)(i) is EIGENVECTOR with some
# OTHER eigenvalue (not -i), then the Z_2 selection rule INCLUDES that
# Y_3̂^(3)(i) is selected with non-trivial eigenvalue
# ============================================================
print("\n" + "=" * 70)
print("Direct eigendecomposition of ρ_3̂(S) = (-i/2) M_block")
print("=" * 70)

S = (-1j / 2) * M_block
print(f"S = (-i/2) M:")
for i in range(3):
    print(f"  {[f'{S[i,j]:+.4f}' for j in range(3)]}")

eigvals, eigvecs = np.linalg.eig(S)
print(f"\nEigenvalues: {eigvals}")
for k in range(3):
    print(f"  λ_{k} = {eigvals[k]}, eigvec = {eigvecs[:,k]}")

# Express Y_vec in eigenbasis
print(f"\nY_3̂^(3)(i) = {Y_vec}")
# Solve eigvecs @ c = Y_vec
c = np.linalg.solve(eigvecs, Y_vec)
print(f"\nY_vec in eigenbasis (coefficients):")
for k in range(3):
    print(f"  c_{k} (eigval {eigvals[k]:.4f}) = {c[k]}, |c_k| = {abs(c[k]):.6f}")

# Project Y_vec onto +i eigenspace and -i eigenspace
# (S has eigenvalues +i, -i, ?)


# ============================================================
# SECOND APPROACH: Compute Y_3̂^(3)(S·τ_test) directly and check
# Y(-1/τ) = (-τ)^3 ρ(S) Y(τ) at τ NEAR i (e.g. 1.001 i)
# ============================================================
print("\n" + "=" * 70)
print("Direct verification: Y_3̂^(3)(-1/τ) = (-τ)^3 ρ(S) Y_3̂^(3)(τ) for τ near i")
print("=" * 70)

# Test at τ = 1.5i
def compute_Y3hat(tau):
    th, ep = theta_eps(tau, N=200)
    pre = 1 / (2 * mp.sqrt(2))
    return mp.matrix([[pre * (ep ** 5 * th + ep * th ** 5)],
                      [pre * (5 * ep ** 2 * th ** 4 - ep ** 6)],
                      [pre * (th ** 6 - 5 * ep ** 4 * th ** 2)]])

tau_test = mp.mpc(0, "1.5")
Stau_test = -1 / tau_test  # = i/1.5
Y_at_tau = compute_Y3hat(tau_test)
Y_at_Stau = compute_Y3hat(Stau_test)

print(f"τ = 1.5i, S·τ = -1/(1.5i) = {Stau_test}")
print(f"\nY_3̂^(3)(τ=1.5i):")
for r in range(3):
    print(f"  [{r}] = {Y_at_tau[r]}")
print(f"\nY_3̂^(3)(S·τ = i/1.5):")
for r in range(3):
    print(f"  [{r}] = {Y_at_Stau[r]}")

# Required: Y(Sτ) = (-τ)^3 ρ(S) Y(τ)
# (-τ)^3 = (-1.5i)^3 = -((1.5i)^3) = -(-3.375 i) = +3.375 i
neg_tau3 = (-tau_test) ** 3
print(f"\n(-τ)^3 = {neg_tau3}")

# Compute (-τ)^3 ρ_3̂(S) Y(τ) using each candidate ρ:
for label, alpha in [("(-i/2)·M", mp.mpc(0, -1)/2)]:
    rho_S = alpha * mp.matrix([[mp.mpc(0), mp.sqrt(2), mp.sqrt(2)],
                                [mp.sqrt(2), -1, 1],
                                [mp.sqrt(2), 1, -1]])
    rhs = neg_tau3 * (rho_S * Y_at_tau)
    print(f"\n{label}: (-τ)^3 ρ(S) Y(τ):")
    for r in range(3):
        print(f"  [{r}] = {rhs[r]}")
    # Compare with Y_at_Stau
    print(f"  Differences from Y(Sτ):")
    for r in range(3):
        d = rhs[r] - Y_at_Stau[r]
        print(f"    [{r}]: {d}, |·| = {abs(d)}")
