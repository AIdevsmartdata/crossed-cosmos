#!/usr/bin/env python3
"""
M170 step 9 — Verify NO eigenspace selection at τ_Q = i√(11/2) for K-K.

Strategy:
1. K-K Y_3^(2)(τ) is the weight-2 A_4 modular triplet (Γ(3) framework).
2. ρ_3(S) is the A_4 representation matrix for S in irrep 3 (specific known matrix).
3. At τ_Q, S·τ_Q ≠ τ_Q (since trivial stab).
4. Therefore Y_3^(2)(τ_Q) is NOT constrained by any eigenvalue equation.

Verify: compute ρ_3(S) Y_3^(2)(τ_Q) and check it does NOT equal a multiple of Y_3^(2)(τ_Q).
"""

import mpmath as mp
mp.mp.dps = 30
import numpy as np


# K-K Y_3^(2) at any τ (eta-quotient form from M140)
N_KK = 200
omega = mp.exp(2j * mp.pi / 3)


def eta_dlog(tau):
    q = mp.exp(2j * mp.pi * tau)
    s = mp.mpc(0, 0)
    for n in range(1, N_KK):
        s += n * q ** n / (1 - q ** n)
    return 2j * mp.pi * (mp.mpf(1) / 24 - s)


def Y_KK(tau):
    a = tau / 3
    b = (tau + 1) / 3
    c = (tau + 2) / 3
    d = 3 * tau
    da = eta_dlog(a)
    db = eta_dlog(b)
    dc = eta_dlog(c)
    dd = eta_dlog(d)
    Y1 = (1j / (2 * mp.pi)) * (da + db + dc - 27 * dd)
    Y2 = (-1j / mp.pi) * (da + omega ** 2 * db + omega * dc)
    Y3 = (-1j / mp.pi) * (da + omega * db + omega ** 2 * dc)
    return mp.matrix([[Y1], [Y2], [Y3]])


# Extract ρ_3(S) for K-K's Y_3^(2) basis
def extract_rho_S_KK():
    """Extract ρ_3(S) from K-K Y_3^(2) using 3 generic τ-points."""
    taus = [mp.mpc(0, "1.5"), mp.mpc(0, "2.5"), mp.mpc("0.05", "1.7")]
    Y_mat = mp.matrix(3, 3)
    SY_mat = mp.matrix(3, 3)
    for col, t in enumerate(taus):
        Y_t = Y_KK(t)
        Y_St = Y_KK(-1 / t)
        for row in range(3):
            Y_mat[row, col] = Y_t[row]
            SY_mat[row, col] = Y_St[row]
    diag_neg = mp.matrix(3, 3)
    for col, t in enumerate(taus):
        diag_neg[col, col] = 1 / (-t) ** 2  # weight 2
    return SY_mat * diag_neg * Y_mat ** (-1)


# ============================================================
# STEP 1 — Extract ρ_3(S) from K-K basis
# ============================================================
print("=" * 70)
print("STEP 1: Extract ρ_3(S) from K-K weight-2 A_4 triplet basis")
print("=" * 70)

rho_S_KK = extract_rho_S_KK()
print("ρ_3(S) (K-K basis):")
for r in range(3):
    row = [f"({float(rho_S_KK[r,c].real):+.4f}{float(rho_S_KK[r,c].imag):+.4f}j)" for c in range(3)]
    print(f"  {row}")

# Verify ρ(S)² = +I (since irrep 3 is R-even, S² = R = +I in PSL framework where R=I)
S2 = rho_S_KK * rho_S_KK
diff_pI = sum(abs(S2[r, c] - (1 if r == c else 0)) for r in range(3) for c in range(3))
print(f"\n|ρ_3(S)² - I| = {diff_pI}")

# Eigenvalues
rho_np = np.array([[complex(rho_S_KK[i, j]) for j in range(3)] for i in range(3)])
ev = np.linalg.eigvals(rho_np)
print(f"\nEigenvalues of ρ_3(S): {ev}")
print("(Expected for S² = I: eigvals ∈ {±1}, with multiplicity 1+2 or 2+1)")


# ============================================================
# STEP 2 — At τ_Q, verify Y(τ_Q) is NOT eigenvector of ρ_3(S)
# ============================================================
print("\n" + "=" * 70)
print("STEP 2: At τ_Q = i√(11/2), is Y_3^(2)(τ_Q) an eigenvector of ρ_3(S)?")
print("=" * 70)

tau_Q = mp.mpc(0, mp.sqrt(mp.mpf(11) / 2))
Y_at_Q = Y_KK(tau_Q)
print(f"τ_Q = i√(11/2) = {tau_Q}")
print(f"Y_3^(2)(τ_Q) = ")
for r in range(3):
    print(f"  [{r}] = {Y_at_Q[r]}")

S_Y = rho_S_KK * Y_at_Q
print(f"\nρ_3(S) · Y_3^(2)(τ_Q) = ")
for r in range(3):
    print(f"  [{r}] = {S_Y[r]}")

# Check ratio: if eigenvector, S_Y[r] / Y[r] should be CONSTANT
print(f"\nRatio S_Y[r] / Y[r] (should be constant if eigenvector):")
ratios = []
for r in range(3):
    if abs(Y_at_Q[r]) > 1e-15:
        ratios.append(S_Y[r] / Y_at_Q[r])
        print(f"  [{r}]: {S_Y[r] / Y_at_Q[r]}")

# Check if Y(τ_Q) projects onto +1 or -1 eigenspace
P_p1 = (rho_S_KK + 1 * mp.eye(3)) / 2  # Wrong — need (ρ - λ_other I) / (λ - λ_other)
# For eigvals {+1, -1, -1}: P_{+1} = (ρ + I) / 2
# For eigvals {-1, +1, +1}: P_{-1} = (ρ - I) / (-2)
# Without knowing eigval pattern, just check both:
# P_{+1} = (ρ - (-1)I) / (1 - (-1)) = (ρ + I) / 2
# P_{-1} = (ρ - (+1)I) / (-1 - 1) = (ρ - I) / (-2)
P_plus1 = (rho_S_KK + mp.eye(3)) / 2
P_minus1 = (rho_S_KK - mp.eye(3)) / (-2)

PpY = P_plus1 * Y_at_Q
PmY = P_minus1 * Y_at_Q

print(f"\nP_{{+1}} · Y(τ_Q):")
for r in range(3):
    print(f"  [{r}] = {PpY[r]}")
mag_p = sum(abs(PpY[r]) for r in range(3))
print(f"  total |P_{{+1}} Y| = {mag_p}")

print(f"\nP_{{-1}} · Y(τ_Q):")
for r in range(3):
    print(f"  [{r}] = {PmY[r]}")
mag_m = sum(abs(PmY[r]) for r in range(3))
print(f"  total |P_{{-1}} Y| = {mag_m}")

print(f"\nIf BOTH non-zero: Y(τ_Q) has components in BOTH eigenspaces.")
print(f"  ⟹ NO Z_2 selection rule applies at τ_Q (trivial stab).")
if mag_p > 1e-10 and mag_m > 1e-10:
    print("\n✓✓✓ CONFIRMED: Y_3^(2)(τ_Q) lies in BOTH +1 and -1 eigenspaces of ρ_3(S)")
    print("    NO eigenspace selection — confirms TRIVIAL stab at τ_Q")
    print("    H18 LOWER HALF VERIFIED: K-K's free param structure is allowed.")


# ============================================================
# STEP 3 — Compare directly to τ=i (where Z_2 selection holds)
# ============================================================
print("\n\n" + "=" * 70)
print("STEP 3: Same K-K Y_3^(2) at τ=i (where stab IS Z_2)")
print("=" * 70)

# Y_KK is weight-2, so at τ=i, eigval = i^{-2} = -1
tau_i = mp.mpc(0, 1)
Y_at_i = Y_KK(tau_i)
print(f"Y_3^(2)(τ=i) = ")
for r in range(3):
    print(f"  [{r}] = {Y_at_i[r]}")

S_Y_i = rho_S_KK * Y_at_i
print(f"\nρ_3(S) · Y_3^(2)(i) = ")
for r in range(3):
    print(f"  [{r}] = {S_Y_i[r]}")

# Eigenvalue check: should give -1 · Y(i)
print(f"\n-1 · Y_3^(2)(i) = ")
for r in range(3):
    print(f"  [{r}] = {-Y_at_i[r]}")

print(f"\nDifference (S_Y - (-1)·Y), should be 0 if Z_2 selection holds at τ=i:")
total = mp.mpf(0)
for r in range(3):
    d = abs(S_Y_i[r] - (-Y_at_i[r]))
    total += d
    print(f"  [{r}]: {d}")
print(f"Total: {total}")

if total < 1e-15:
    print("\n✓✓✓ At τ=i, Y_3^(2)(i) IS in -1 eigenspace of ρ_3(S) (k=2 weight)")
    print("    Z_2 SELECTION RULE confirmed at τ=i in K-K basis too.")
else:
    print("\n⚠ Surprise: Y_3^(2)(i) is NOT in -1 eigenspace")
    # Project on each eigenspace
    PpY = (rho_S_KK + mp.eye(3)) / 2 * Y_at_i
    PmY = (rho_S_KK - mp.eye(3)) / (-2) * Y_at_i
    print(f"\nP_{{+1}} Y(i): total mag = {sum(abs(PpY[r]) for r in range(3))}")
    print(f"P_{{-1}} Y(i): total mag = {sum(abs(PmY[r]) for r in range(3))}")
