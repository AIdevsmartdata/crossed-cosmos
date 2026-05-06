#!/usr/bin/env python3
"""
M170 step 5 — Use NPP20's actual transformation rules to verify Y_3̂^(3)(τ)
under S directly, then EXTRACT ρ_3̂(S) from the transformation.

Strategy:
  • For τ near i, compute Y(τ) and Y(-1/τ).
  • Then ρ_3̂(S) = (1/(-τ)^3) Y(-1/τ) Y(τ)^{-1}    (for invertible Y matrix —
    but Y is a column, not invertible)
  • Use multiple values of τ to build a matrix equation for ρ(S):

  Use τ_1, τ_2, τ_3 (three independent points). Stack Y(τ_k) into 3×3 matrix Y_τ.
  Stack Y(Sτ_k) into Y_Sτ. Then ρ(S) = Y_Sτ · diag((-τ_k)^{-3}) · Y_τ^{-1}.

This will GIVE us the actual ρ_3̂(S) matrix that NPP20 uses.
"""

import mpmath as mp
mp.mp.dps = 30

import numpy as np


def theta_eps(tau, N=200):
    q4 = mp.exp(1j * mp.pi * tau / 2)
    th = mp.mpc(1)
    ep = mp.mpc(0)
    for k in range(1, N + 1):
        th += 2 * q4 ** ((2 * k) ** 2)
        ep += 2 * q4 ** ((2 * k - 1) ** 2)
    return th, ep


def Y3_hat_w3(tau):
    th, ep = theta_eps(tau)
    pre = 1 / (2 * mp.sqrt(2))
    return mp.matrix([[pre * (ep ** 5 * th + ep * th ** 5)],
                      [pre * (5 * ep ** 2 * th ** 4 - ep ** 6)],
                      [pre * (th ** 6 - 5 * ep ** 4 * th ** 2)]])


# ============================================================
# STEP 1 — Use 3 distinct τ-values to extract ρ(S)
# ============================================================
taus = [mp.mpc(0, "1.3"), mp.mpc(0, "2.0"), mp.mpc("0.1", "1.5")]
Y_at_taus = [Y3_hat_w3(t) for t in taus]
Y_at_Staus = [Y3_hat_w3(-1/t) for t in taus]

# Stack into matrices
Y_mat = mp.matrix(3, 3)
SY_mat = mp.matrix(3, 3)
for col, t in enumerate(taus):
    for row in range(3):
        Y_mat[row, col] = Y_at_taus[col][row]
        SY_mat[row, col] = Y_at_Staus[col][row]

# Apply (-τ)^{-3} factors:
# Y(Sτ) = (-τ)^3 ρ(S) Y(τ)  ⟹  ρ(S) = Y(Sτ) · diag((-τ)^{-3}) · Y(τ)^{-1}
diag_neg = mp.matrix(3, 3)
for col, t in enumerate(taus):
    diag_neg[col, col] = 1 / (-t) ** 3

print("Y(τ) matrix:")
for r in range(3):
    print(f"  {[Y_mat[r,c] for c in range(3)]}")
print("\nY(Sτ) matrix:")
for r in range(3):
    print(f"  {[SY_mat[r,c] for c in range(3)]}")
print("\ndiag (-τ)^(-3):")
for r in range(3):
    print(f"  {[diag_neg[r,c] for c in range(3)]}")

# ρ(S) = SY_mat · diag_neg · Y_mat^(-1)
rho_S_extracted = SY_mat * diag_neg * Y_mat ** (-1)
print("\n" + "=" * 70)
print("EXTRACTED ρ_3̂(S):")
print("=" * 70)
for r in range(3):
    for c in range(3):
        val = rho_S_extracted[r, c]
        print(f"  [{r},{c}] = {val}")

# Compare to candidates
print("\nCompare with (-i/2) M_block:")
M_block = mp.matrix([[0, mp.sqrt(2), mp.sqrt(2)],
                     [mp.sqrt(2), -1, 1],
                     [mp.sqrt(2), 1, -1]])
target_S = (mp.mpc(0, -1) / 2) * M_block
diff_norm = sum(abs(rho_S_extracted[r,c] - target_S[r,c]) for r in range(3) for c in range(3))
print(f"|extracted - (-i/2)M| = {diff_norm}")

print("\nCompare with (i/2) M_block:")
target_S2 = (mp.mpc(0, 1) / 2) * M_block
diff_norm2 = sum(abs(rho_S_extracted[r,c] - target_S2[r,c]) for r in range(3) for c in range(3))
print(f"|extracted - (i/2)M| = {diff_norm2}")


# ============================================================
# STEP 2 — Verify extracted ρ(S) satisfies group relations + ρ²=−I
# ============================================================
print("\n" + "=" * 70)
print("Verify extracted matrix satisfies group relations")
print("=" * 70)
S = rho_S_extracted
S2 = S * S
print(f"S²:")
for r in range(3):
    for c in range(3):
        print(f"  [{r},{c}] = {S2[r,c]}")
print(f"\n|S² - (-I)| = {sum(abs(S2[r,c] - (-1 if r==c else 0)) for r in range(3) for c in range(3))}")
print(f"|S² - (+I)| = {sum(abs(S2[r,c] - (+1 if r==c else 0)) for r in range(3) for c in range(3))}")

T_3hat = mp.matrix([[mp.mpc(0, 1), 0, 0], [0, -1, 0], [0, 0, 1]])
ST = S * T_3hat
ST3 = ST * ST * ST
print(f"\n(ST)³:")
for r in range(3):
    for c in range(3):
        print(f"  [{r},{c}] = {ST3[r,c]}")


# ============================================================
# STEP 3 — Once we have correct ρ(S), test eigenvalue at τ=i
# ============================================================
print("\n" + "=" * 70)
print("Y_3̂^(3)(i) eigenvalue test with EXTRACTED ρ(S)")
print("=" * 70)

tau_C = mp.mpc(0, 1)
Y_at_i = Y3_hat_w3(tau_C)
print(f"Y_3̂^(3)(i) = ")
for r in range(3):
    print(f"  [{r}] = {Y_at_i[r]}")

S_Y = rho_S_extracted * Y_at_i
print(f"\nρ_3̂(S) · Y_3̂^(3)(i) = ")
for r in range(3):
    print(f"  [{r}] = {S_Y[r]}")

# Expected: (-i)^3 ρ(S) Y(i) = Y(i) ⟹ ρ(S) Y(i) = (1/(-i)^3) Y(i) = (1/i) Y(i) = -i Y(i)
# Wait, (-i)^3 = +i, so Y(i) = i ρ(S) Y(i) ⟹ ρ(S) Y(i) = -i Y(i).
print(f"\n-i · Y_3̂^(3)(i) = ")
for r in range(3):
    print(f"  [{r}] = {mp.mpc(0, -1) * Y_at_i[r]}")

print(f"\nDifference (should be 0):")
diffs = []
for r in range(3):
    d = S_Y[r] - mp.mpc(0, -1) * Y_at_i[r]
    diffs.append(abs(d))
    print(f"  [{r}]: {d}, |·| = {abs(d)}")
print(f"\nMax |diff| = {max(diffs)}")
if max(diffs) < 1e-15:
    print("\n✓✓✓ Y_3̂^(3)(i) IS eigenvector of ρ_3̂(S) with eigenvalue -i ✓✓✓")
    print("    (Z_2 SELECTION RULE VERIFIED)")
