#!/usr/bin/env python3
"""
M170 step 7 — Clean eigenspace projection for Y_3̂^(3)(i).

Verify: Y(i) is in the i^{-k}-eigenspace of ρ(S). I.e.
  ρ(S) Y(i) = i^{-k} Y(i) = -i · Y(i)  (for k=3).

Use orthonormal basis for each eigenspace, and explicit projector.
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


def extract_rho_S(Y_func, weight):
    taus = [mp.mpc(0, "1.3"), mp.mpc(0, "2.0"), mp.mpc("0.1", "1.5")]
    Y_mat = mp.matrix(3, 3)
    SY_mat = mp.matrix(3, 3)
    for col, t in enumerate(taus):
        Y_t = Y_func(t)
        Y_St = Y_func(-1 / t)
        for row in range(3):
            Y_mat[row, col] = Y_t[row]
            SY_mat[row, col] = Y_St[row]
    diag_neg = mp.matrix(3, 3)
    for col, t in enumerate(taus):
        diag_neg[col, col] = 1 / (-t) ** weight
    return SY_mat * diag_neg * Y_mat ** (-1)


# ============================================================
# STEP 1 — Extract ρ_3̂(S) and apply DIRECTLY to Y_3̂^(3)(i)
# ============================================================
rho_S_3hat = extract_rho_S(Y3_hat_w3, 3)
tau_C = mp.mpc(0, 1)
Y_at_i = Y3_hat_w3(tau_C)

print("Y_3̂^(3)(i) =")
for r in range(3):
    print(f"  [{r}] = {Y_at_i[r]}")

print("\nρ_3̂(S) · Y_3̂^(3)(i) =")
S_Y = rho_S_3hat * Y_at_i
for r in range(3):
    print(f"  [{r}] = {S_Y[r]}")

print("\nExpected: ρ(S) Y(i) = i^{-3} Y(i) = -i Y(i) for k=3")
print("\n-i · Y_3̂^(3)(i) =")
for r in range(3):
    print(f"  [{r}] = {mp.mpc(0,-1) * Y_at_i[r]}")

print("\nDifference (should be ~10^-30):")
diff_total = mp.mpf(0)
for r in range(3):
    d = abs(S_Y[r] - mp.mpc(0, -1) * Y_at_i[r])
    diff_total += d
    print(f"  [{r}]: |diff| = {d}")
print(f"\nTotal: {diff_total}")

if diff_total < 1e-15:
    print("\n" + "=" * 70)
    print("✓✓✓ Y_3̂^(3)(i) IS EIGENVECTOR of ρ_3̂(S) WITH EIGENVALUE -i ✓✓✓")
    print("    Z_2 SELECTION RULE PROVED at τ = i for irrep 3̂, weight k=3")
    print("=" * 70)


# ============================================================
# STEP 2 — Why was the eigenspace projection misleading?
# Because numpy.linalg.eig returns NON-orthonormal basis for degenerate eigenspaces.
# Verify here:
# ============================================================
print("\n\n" + "=" * 70)
print("STEP 2: Numerical eigvec basis for ρ_3̂(S)")
print("=" * 70)
rho_np = np.array([[complex(rho_S_3hat[i, j]) for j in range(3)] for i in range(3)])
ev, evecs = np.linalg.eig(rho_np)
print(f"Eigenvalues: {ev}")
for k in range(3):
    print(f"  λ = {ev[k]:.4f}, eigvec = {evecs[:, k]}")

# Inner product matrix
G = evecs.conj().T @ evecs
print(f"\nGram matrix G[i,j] = <eigvec_i, eigvec_j>:")
for r in range(3):
    print(f"  {[f'{G[r,c]:+.4f}' for c in range(3)]}")
print("\n(Off-diagonal nonzero entries indicate non-orthogonal eigvecs in degenerate eigenspace)")


# Properly construct PROJECTOR onto -i eigenspace
print("\n" + "=" * 70)
print("STEP 3: Project Y_3̂^(3)(i) onto -i eigenspace via P = (ρ(S) - i I)/(-2i)")
print("=" * 70)
# For unitary ρ(S) with simple eigenvalues {-i, +i, +i} (one -i, two +i),
# the projector onto the -i eigenspace is:
#   P_{-i} = (ρ(S) - λ_other I) / (λ_{-i} - λ_other) = (ρ(S) - iI) / (-2i)
P_minus_i = (rho_S_3hat - mp.mpc(0, 1) * mp.eye(3)) / (mp.mpc(0, -2))

# Apply to Y(i)
PYatI = P_minus_i * Y_at_i
print("P_{-i} · Y_3̂^(3)(i) = ")
for r in range(3):
    print(f"  [{r}] = {PYatI[r]}")
print("\nY_3̂^(3)(i) (for comparison) =")
for r in range(3):
    print(f"  [{r}] = {Y_at_i[r]}")

# Difference
print("\n|P_{-i} Y - Y| (should be 0 if Y is fully in -i eigenspace):")
total = mp.mpf(0)
for r in range(3):
    total += abs(PYatI[r] - Y_at_i[r])
print(f"  total = {total}")

# Project onto +i eigenspace
P_plus_i = (rho_S_3hat - mp.mpc(0, -1) * mp.eye(3)) / (mp.mpc(0, 2))
PpYatI = P_plus_i * Y_at_i
print("\nP_{+i} · Y_3̂^(3)(i) = ")
for r in range(3):
    print(f"  [{r}] = {PpYatI[r]}")
total_plus = mp.mpf(0)
for r in range(3):
    total_plus += abs(PpYatI[r])
print(f"\n|P_{'{+i}'} Y| (should be 0 if Y fully in -i eigenspace):")
print(f"  total = {total_plus}")
