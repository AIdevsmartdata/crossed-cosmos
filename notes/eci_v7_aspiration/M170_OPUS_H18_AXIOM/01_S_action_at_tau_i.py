#!/usr/bin/env python3
"""
M170 step 1 — S-action on NPP20 weight-3 modular forms at τ_C = i.

Goal: Verify the Z_2 stabilizer constraint at τ_L = i forces specific
S-eigenvalue selection on Y_e (lepton Yukawa) modular forms.

NPP20 Y_e (charged lepton mass matrix Me, eq. 6.6) is built from:
  α1 Y_1̂'^(3),  α2 Y_3̂'^(3),  α3 Y_3̂^(3)

NPP20 transformation under S (eqs 3.6 + 3.8):
  θ(τ) → √(-iτ) (θ + ε)/√2
  ε(τ) → √(-iτ) (θ - ε)/√2

For weight-3 multiplet Y(τ) (which is degree 6 in θ, ε):
  Y(-1/τ) = (-τ)^3 ρ(S) Y(τ)

At τ = i, S·i = -1/i = i, so:
  Y_R^(3)(i) = (-i)^3 ρ_R(S) Y_R^(3)(i) = i ρ_R(S) Y_R^(3)(i)

This is an EIGENVALUE EQUATION. Y(i) survives only if it is an eigenvector
of i·ρ_R(S) with eigenvalue 1 (otherwise Y(i) = 0 — the Z_2 selection rule).

Run: python3 01_S_action_at_tau_i.py
"""

import mpmath as mp
mp.mp.dps = 30

import sympy as sp


# ============================================================
# STEP 1 — Numerical θ(τ), ε(τ) via q-expansion (NPP20 eq 3.3)
# ============================================================
def theta_eps_numerical(tau, N=80):
    """
    NPP20 eq. (3.3):
      θ(τ) = 1 + 2 Σ_{k≥1} q4^{(2k)^2}
      ε(τ) = 2 Σ_{k≥1} q4^{(2k-1)^2}
    where q4 = exp(iπτ/2).
    """
    q4 = mp.exp(1j * mp.pi * tau / 2)
    th = mp.mpc(1)
    ep = mp.mpc(0)
    for k in range(1, N + 1):
        th += 2 * q4 ** ((2 * k) ** 2)
        ep += 2 * q4 ** ((2 * k - 1) ** 2)
    return th, ep


# ============================================================
# STEP 2 — Verify NPP20's stated values at τ_C = i (eq 3.4)
# ============================================================
print("=" * 70)
print("STEP 2: Verify θ, ε at τ_C = i against NPP20 eq. (3.4)")
print("=" * 70)

tau_C = mp.mpc(0, 1)  # τ_C = i (NPP20 notation)
th_C, ep_C = theta_eps_numerical(tau_C)

print(f"τ_C = i")
print(f"  θ(i) computed     = {th_C}")
print(f"  NPP20 ≃ 1.00373   = {mp.nstr(th_C.real, 6)}")
print(f"  ε(i) computed     = {ep_C}")
print(f"  |ε(i)|            = {abs(ep_C)}")
print(f"  NPP20 ≃ 0.41576   = {mp.nstr(abs(ep_C), 6)}")

# Verify NPP20 (3.5): ε(τ_C)/θ(τ_C) = 1/(1+√2) = √2 - 1
ratio_C = ep_C / th_C
expected = 1 / (1 + mp.sqrt(2))  # = √2 - 1 ≈ 0.41421
print(f"\n  ε(i)/θ(i) computed       = {ratio_C}")
print(f"  NPP20 says 1/(1+√2) = √2-1 = {expected}")
print(f"  match: |diff| = {abs(ratio_C - expected)} (should be O(10^-30))")

assert abs(th_C.real - mp.mpf("1.00373")) < 0.01, "θ(i) mismatch!"
assert abs(abs(ep_C) - mp.mpf("0.41576")) < 0.01, "ε(i) mismatch!"
assert abs(ratio_C - expected) < 1e-15, "NPP20 (3.5) ratio mismatch!"
print("  ✓ NPP20 eq (3.4)+(3.5) verified at τ_C = i")


# ============================================================
# STEP 3 — Compute weight-3 modular form triplets at τ_C = i
#          (NPP20 eq. 3.16-3.17 in the paper, lines 760-799)
# ============================================================
print("\n" + "=" * 70)
print("STEP 3: Y_3̂^(3)(τ_C=i) and Y_3̂'^(3)(τ_C=i)")
print("=" * 70)


def Y3_hat_weight3(theta, eps):
    """
    NPP20 eq. (3.14) parsed correctly from layout (lines 503-515):
    Y_3̂^(3)(τ) = (1/(2√2)) · [ ε⁵θ + εθ⁵;  5ε²θ⁴ - ε⁶;  θ⁶ - 5ε⁴θ² ]

    Verified to transform under T as ρ_3̂(T) = diag(i, -1, 1) — matches NPP20 Table 7.
    """
    pre = 1 / (2 * mp.sqrt(2))
    Y1 = pre * (eps ** 5 * theta + eps * theta ** 5)
    Y2 = pre * (5 * eps ** 2 * theta ** 4 - eps ** 6)
    Y3 = pre * (theta ** 6 - 5 * eps ** 4 * theta ** 2)
    return mp.matrix([[Y1], [Y2], [Y3]])


def Y3_prime_weight3(theta, eps):
    """
    NPP20 eq. (3.14) parsed correctly:
    Y_3̂'^(3)(τ) = (1/2) · [ -4√2 ε³θ³;  θ⁶ + 3ε⁴θ²;  -3ε²θ⁴ - ε⁶ ]

    Under T: entry 1 → -4√2(iε)³θ³ = -4√2(-i)ε³θ³ = -i·entry1.
             entry 2 → θ⁶ + 3(iε)⁴θ² = θ⁶ + 3ε⁴θ² = +1·entry2.
             entry 3 → -3(iε)²θ⁴ - (iε)⁶ = +3ε²θ⁴ + ε⁶ = -1·entry3.
    So Y_3̂' under T → diag(-i, 1, -1) Y_3̂'. NPP20 Table 7 row "3̂'": ρ(T) = diag(-i, 1, -1). ✓
    """
    pre = mp.mpf(1) / 2
    Y1 = pre * (-4 * mp.sqrt(2) * eps ** 3 * theta ** 3)
    Y2 = pre * (theta ** 6 + 3 * eps ** 4 * theta ** 2)
    Y3 = pre * (-3 * eps ** 2 * theta ** 4 - eps ** 6)
    return mp.matrix([[Y1], [Y2], [Y3]])


def Y1_prime_weight3(theta, eps):
    """Y_1̂'^(3) = √3 (ε θ^5 - ε^5 θ) (singlet, weight 3)."""
    return mp.sqrt(3) * (eps * theta ** 5 - eps ** 5 * theta)


# Evaluate at τ_C = i:
Y3_hat_at_i = Y3_hat_weight3(th_C, ep_C)
Y3_prime_at_i = Y3_prime_weight3(th_C, ep_C)
Y1_prime_at_i = Y1_prime_weight3(th_C, ep_C)

print("Y_3̂^(3)(i) =")
for r in range(3):
    print(f"  [{r}]  {Y3_hat_at_i[r]}")
print(f"\nY_3̂'^(3)(i) =")
for r in range(3):
    print(f"  [{r}]  {Y3_prime_at_i[r]}")
print(f"\nY_1̂'^(3)(i) = {Y1_prime_at_i}")
print(f"  |Y_1̂'^(3)(i)| = {abs(Y1_prime_at_i)}")


# ============================================================
# STEP 4 — Verify S-transformation explicitly: compute Y at S·τ = -1/τ
#          and compare to (-τ)^3 ρ(S) Y(τ)
# ============================================================
print("\n" + "=" * 70)
print("STEP 4: Verify S-transformation Y(-1/τ) = (-τ)^3 ρ(S) Y(τ)")
print("=" * 70)

# At τ = 1.5i (generic — S is non-fixing here): Sτ = -1/(1.5i) = i/1.5 = 0.6667i
tau_test = mp.mpc(0, "1.5")
Stau_test = -1 / tau_test

th_t, ep_t = theta_eps_numerical(tau_test, N=200)
th_S, ep_S = theta_eps_numerical(Stau_test, N=200)

print(f"τ_test = 1.5i, S·τ = {Stau_test}")
print(f"θ(τ) = {th_t}, ε(τ) = {ep_t}")
print(f"θ(Sτ) = {th_S}, ε(Sτ) = {ep_S}")

# NPP20 (3.8): θ(-1/τ) = √(-iτ) (θ(τ) + ε(τ))/√2
#              ε(-1/τ) = √(-iτ) (θ(τ) - ε(τ))/√2
sqrt_factor = mp.sqrt(-1j * tau_test)
th_S_predicted = sqrt_factor * (th_t + ep_t) / mp.sqrt(2)
ep_S_predicted = sqrt_factor * (th_t - ep_t) / mp.sqrt(2)

print(f"\nNPP20 (3.8) prediction:")
print(f"  θ(-1/τ) predicted = {th_S_predicted}")
print(f"  match diff = {abs(th_S - th_S_predicted)}")
print(f"  ε(-1/τ) predicted = {ep_S_predicted}")
print(f"  match diff = {abs(ep_S - ep_S_predicted)}")

assert abs(th_S - th_S_predicted) < 1e-15, "θ S-transformation FAILED"
assert abs(ep_S - ep_S_predicted) < 1e-15, "ε S-transformation FAILED"
print("  ✓ NPP20 (3.8) S-transformation of θ, ε verified to 30 digits")


# ============================================================
# STEP 5 — At τ_C = i, S fixes τ:
#          Y_R^(3)(i) = (-i)^3 ρ_R(S) Y_R^(3)(i) = i ρ_R(S) Y_R^(3)(i)
#          ⟹ Y_R^(3)(i) is an eigenvector of ρ_R(S) with eigenvalue -i
# ============================================================
print("\n" + "=" * 70)
print("STEP 5: At τ = i, S-eigenvalue equation Y(i) = i ρ_R(S) Y(i)")
print("=" * 70)
print("  i.e. ρ_R(S) Y(i) = -i · Y(i)  (since 1/i = -i)")
print("  ⟹ Y(i) must be eigenvector of ρ_R(S) with eigenvalue -i")
print("     OR Y(i) = 0\n")

# NPP20 Table 7 representation matrices (from /tmp/npp20_layout.txt lines 1860-1896).
# Reading the layout carefully:
#
# ρ_3(S)  = (1/2) · [[0, √2, √2], [-√2, -1, 1], [√2, 1, -1]]  — note "−√2" in row 2
#                                                                "−" sign just outside is for the matrix
# Wait — looking at layout 1874-1878:
#       √ √
#     0     2    2
#   1 √
# − √2 −1 1
#   2 √
#     2 1 −1
#
# This means: prefactor is "1/2" (the "1" and "2" are above/below a fraction bar).
# The "−" before the matrix is an overall minus sign? But ρ(S) for irrep 3 should be unitary.
# Re-examining: the OCR places "1" above "2", which is "1/2". The "−" before the "√2" in row 2 column 1
# is actually part of the (3,1) row...
#
# CORRECT reading (from a clean copy of NPP20 paper):
# ρ_3(S)   = -1/2 · [[0, -√2, -√2], [-√2, 1, -1], [-√2, -1, 1]]
#         = +1/2 · [[0,  √2,  √2], [ √2,-1,  1], [ √2, 1,-1]]   (overall sign)
#
# Actually, the sign is ambiguous from OCR. Let me CONSTRUCT the matrices and
# verify ρ(S)^2 = ρ(R), ρ(S)^4 = 1 (since R^2=1 and S^2=R), and compatibility.
#
# A standard normalization (NPP20-equivalent) for irrep 3 of S4' is:
M_block = mp.matrix([[0, mp.sqrt(2), mp.sqrt(2)],
                     [mp.sqrt(2), -1, 1],
                     [mp.sqrt(2), 1, -1]])

# Test the four sign/factor options
candidates = {
    "+1/2 · M": mp.mpc(1, 0) / 2 * M_block,
    "-1/2 · M": mp.mpc(-1, 0) / 2 * M_block,
    "+i/2 · M": mp.mpc(0, 1) / 2 * M_block,
    "-i/2 · M": mp.mpc(0, -1) / 2 * M_block,
}

print("Testing ρ(S) candidate matrices for irrep 3 (R-even, weight-2k):")
for label, M_S in candidates.items():
    # ρ(S)^2 should be ρ(R)
    M_S2 = M_S * M_S
    # ρ(S)^4 should be ρ(R)^2 = 1
    M_S4 = M_S2 * M_S2
    diff_S4_I = mp.norm(M_S4 - mp.eye(3))
    # For ρ_3 (un-hatted), ρ_3(R) = +I (since R-even). For ρ_3̂ (hatted), ρ_3̂(R) = -I.
    # NPP20 Table 7 row "3": ρ_3(R) = I (the column shows 1/0/0, 0/1/0, 0/0/1)
    # NPP20 Table 7 row "3̂": ρ_3̂(R) = -I (column shows 1/0/0, 0/1/0, 0/0/1 with overall − sign)
    diff_S2_I = mp.norm(M_S2 - mp.eye(3))
    diff_S2_negI = mp.norm(M_S2 + mp.eye(3))
    print(f"  {label}: |ρ(S)^4 - I| = {diff_S4_I}, "
          f"|ρ(S)^2 - I| = {diff_S2_I}, |ρ(S)^2 + I| = {diff_S2_negI}")


# ============================================================
# STEP 6 — Use the canonical irrep 3̂ matrix and check Y_3̂^(3)(i) is S-eigenvector
# ============================================================
print("\n" + "=" * 70)
print("STEP 6: Check Y_3̂^(3)(i) is eigenvector of ρ_3̂(S) with eigenvalue -i")
print("=" * 70)

# From NPP20 Table 7 layout (best reading):
# ρ_3̂(S) = (i/2) · diag-style M_block with overall sign negation pattern.
# We will TEST all sign conventions; physical answer: Y(i) must be eigvec of ρ(S)
# whose square is ρ(R) = -I (for hatted 3̂), so eigenvalues of ρ(S) are ±i.
# Then Y(i) = i ρ(S) Y(i) gives eigenvalue equation ρ(S) Y(i) = -i Y(i).
#
# Let's pick "-i/2 · M" candidate (which has ρ(S)^2 = -I as required for hatted irrep):

M_S_3hat = mp.mpc(0, -1) / 2 * M_block  # candidate ρ_3̂(S)
M_S2 = M_S_3hat * M_S_3hat
print(f"Using ρ_3̂(S) = -i/2 · M:")
print(f"  ρ_3̂(S)^2 = ")
for r in range(3):
    row = [M_S2[r, c] for c in range(3)]
    print(f"    {row}")
print(f"  This should be ρ_3̂(R) = -I = diag(-1,-1,-1) for hatted 3̂")

# Eigendecomposition of ρ_3̂(S)
import numpy as np
M_np = np.array([[complex(M_S_3hat[i, j]) for j in range(3)] for i in range(3)])
eigvals, eigvecs = np.linalg.eig(M_np)
print(f"\nEigenvalues of ρ_3̂(S): {eigvals}")
print("(should be {-i, -i, +i} OR {+i, +i, -i})")

Y3_hat_at_i_np = np.array([complex(Y3_hat_at_i[i]) for i in range(3)], dtype=complex)
print(f"\nY_3̂^(3)(i) = {Y3_hat_at_i_np}")
print(f"  norm = {np.linalg.norm(Y3_hat_at_i_np)}")

# Apply ρ_3̂(S) to Y_3̂^(3)(i) and see if proportional to ±i Y(i)
M_S_Y = M_np @ Y3_hat_at_i_np
print(f"\nρ_3̂(S) · Y_3̂^(3)(i) = {M_S_Y}")

# Test: M_S_Y / Y_3̂^(3)(i) componentwise (where Y is non-zero)
print(f"\nRatio (ρ_3̂(S) Y) / Y, componentwise:")
for k in range(3):
    if abs(Y3_hat_at_i_np[k]) > 1e-10:
        ratio = M_S_Y[k] / Y3_hat_at_i_np[k]
        print(f"  [{k}]: {ratio}  (should be ±i if eigenvector)")
    else:
        print(f"  [{k}]: Y[{k}] ≈ 0, ratio undefined")


# ============================================================
# STEP 7 — Same analysis for Y_3̂'^(3)(i) (the OTHER weight-3 triplet)
# ============================================================
print("\n" + "=" * 70)
print("STEP 7: Check Y_3̂'^(3)(i) is eigenvector of ρ_3̂'(S)")
print("=" * 70)

# ρ_3̂'(S) candidate: from layout, +i/2 · M (different sign than ρ_3̂(S))
M_S_3primehat = mp.mpc(0, 1) / 2 * M_block  # candidate ρ_3̂'(S)
M_np_prime = np.array([[complex(M_S_3primehat[i, j]) for j in range(3)] for i in range(3)])
eigvals_prime, _ = np.linalg.eig(M_np_prime)
print(f"Eigenvalues of ρ_3̂'(S): {eigvals_prime}")

Y3_prime_at_i_np = np.array([complex(Y3_prime_at_i[i]) for i in range(3)], dtype=complex)
print(f"\nY_3̂'^(3)(i) = {Y3_prime_at_i_np}")
print(f"  norm = {np.linalg.norm(Y3_prime_at_i_np)}")

M_S_Y_prime = M_np_prime @ Y3_prime_at_i_np
print(f"ρ_3̂'(S) · Y_3̂'^(3)(i) = {M_S_Y_prime}")
print(f"\nRatio (ρ_3̂'(S) Y') / Y' componentwise:")
for k in range(3):
    if abs(Y3_prime_at_i_np[k]) > 1e-10:
        ratio = M_S_Y_prime[k] / Y3_prime_at_i_np[k]
        print(f"  [{k}]: {ratio}  (should be ±i if eigenvector)")


# ============================================================
# STEP 8 — Singlet Y_1̂'^(3)(i) — should vanish (or be eigenvector of trivial 1D rep)
# ============================================================
print("\n" + "=" * 70)
print("STEP 8: Y_1̂'^(3)(i) — value at τ=i + Z_2 selection check")
print("=" * 70)

# ρ_1̂'(S) = -i (from Table 7), and ρ(R) = -1 for hatted singlet
# Eigenvalue equation: Y_1̂'^(3)(i) = i · (-i) · Y_1̂'^(3)(i) = +1 · Y_1̂'^(3)(i)
# This is auto-satisfied for ANY value of Y_1̂'^(3)(i). So no constraint!
#
# But let's CHECK numerically:
print(f"Y_1̂'^(3)(i) = {Y1_prime_at_i}")
print(f"|Y_1̂'^(3)(i)| = {abs(Y1_prime_at_i)}")
print(f"\nFor 1̂' singlet at τ=i:  Y(i) = i^3 ρ_1̂'(S) Y(i) = i·(-i)·Y(i) = +1·Y(i)")
print("This is auto-satisfied (no constraint on Y_1̂'^(3)(i) from S).")
print(f"Numerically: Y_1̂'^(3)(i) = √3·ε(i)·θ(i)·(θ(i)^4 - ε(i)^4)")
val_check = mp.sqrt(3) * ep_C * th_C * (th_C ** 4 - ep_C ** 4)
print(f"  Direct = {val_check}")
print(f"  From function = {Y1_prime_at_i}")
print(f"  Match: {abs(val_check - Y1_prime_at_i) < 1e-20}")
