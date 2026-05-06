#!/usr/bin/env python3
"""
M170 step 3 — Verify Y_3̂^(3)(i) is eigenvector of ρ_3̂(S) with eigenvalue +i.

Setup recap (verified in scripts 01, 02):
  • τ_C = i, S·i = i, (cτ+d) at S=((0,-1),(1,0)) is c·i+d = i
  • Weight k=3 form: Y(S·τ) = (cτ+d)^k ρ(S) Y(τ)
    At τ=i: Y(i) = i^3 ρ(S) Y(i) = -i · ρ(S) Y(i)
    ⟹ ρ(S) Y(i) = -1/(-i) Y(i) = (1/i) Y(i) = -i Y(i)
    Wait — let me redo: Y(i) = -i ρ(S) Y(i) ⟹ ρ(S) Y(i) = (1/(-i)) Y(i) = i Y(i)
    Hmm, since -i · ρ(S) Y(i) = Y(i), we have ρ(S) Y(i) = (1/-i) Y(i) = +i Y(i).

  • Y_3̂^(3)(τ) = (1/(2√2))[ε⁵θ + εθ⁵; 5ε²θ⁴ - ε⁶; θ⁶ - 5ε⁴θ²]  (NPP20 eq 3.14)
  • Y_3̂'^(3)(τ) = (1/2)[-4√2 ε³θ³; θ⁶ + 3ε⁴θ²; -3ε²θ⁴ - ε⁶]   (NPP20 eq 3.14)
  • Y_1̂'^(3)(τ) = √3 (εθ⁵ - ε⁵θ)                              (NPP20 eq 3.14, singlet)

  • ρ_3̂(S)  = (-i/2) M_block,    M_block = [[0,√2,√2],[√2,-1,1],[√2,1,-1]]
  • ρ_3̂'(S) = ?  We need to determine this.
  • ρ_1̂'(S) = -i  (from Table 7, scalar)
"""

import mpmath as mp
mp.mp.dps = 30

import numpy as np
import sympy as sp


# ============================================================
# STEP 1 — θ, ε at τ_C = i
# ============================================================
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


# ============================================================
# STEP 2 — Weight-3 modular forms at τ = i
# ============================================================
def Y3_hat_w3(theta, eps):
    pre = 1 / (2 * mp.sqrt(2))
    Y1 = pre * (eps ** 5 * theta + eps * theta ** 5)
    Y2 = pre * (5 * eps ** 2 * theta ** 4 - eps ** 6)
    Y3 = pre * (theta ** 6 - 5 * eps ** 4 * theta ** 2)
    return mp.matrix([[Y1], [Y2], [Y3]])


def Y3_prime_w3(theta, eps):
    pre = mp.mpf(1) / 2
    Y1 = pre * (-4 * mp.sqrt(2) * eps ** 3 * theta ** 3)
    Y2 = pre * (theta ** 6 + 3 * eps ** 4 * theta ** 2)
    Y3 = pre * (-3 * eps ** 2 * theta ** 4 - eps ** 6)
    return mp.matrix([[Y1], [Y2], [Y3]])


def Y1_prime_w3(theta, eps):
    return mp.sqrt(3) * (eps * theta ** 5 - eps ** 5 * theta)


Y_3hat_i = Y3_hat_w3(th_C, ep_C)
Y_3prime_i = Y3_prime_w3(th_C, ep_C)
Y_1prime_i = Y1_prime_w3(th_C, ep_C)

print("=" * 70)
print("STEP 1: Modular forms at τ_C = i (high precision)")
print("=" * 70)
print(f"\nY_3̂^(3)(i):")
for r in range(3):
    print(f"  [{r}] = {Y_3hat_i[r]}")
print(f"\nY_3̂'^(3)(i):")
for r in range(3):
    print(f"  [{r}] = {Y_3prime_i[r]}")
print(f"\nY_1̂'^(3)(i) = {Y_1prime_i}")


# ============================================================
# STEP 3 — Construct ρ_3̂(S) = -i/2 · M_block
# ============================================================
M_block = mp.matrix([[0, mp.sqrt(2), mp.sqrt(2)],
                     [mp.sqrt(2), -1, 1],
                     [mp.sqrt(2), 1, -1]])

rho_3hat_S = (mp.mpc(0, -1) / 2) * M_block

# Verify ρ²=−I, (ST)³=I
T_3hat = mp.matrix([[mp.mpc(0,1), 0, 0],
                    [0, -1, 0],
                    [0, 0, 1]])
print("\n" + "=" * 70)
print("STEP 3: Verify ρ_3̂(S) satisfies group relations")
print("=" * 70)
S2 = rho_3hat_S * rho_3hat_S
S2_norm = sum(abs(S2[i, j] - (-1 if i == j else 0)) for i in range(3) for j in range(3))
print(f"|ρ_3̂(S)² - (-I)| = {S2_norm}")

ST = rho_3hat_S * T_3hat
ST3 = ST * ST * ST
ST3_norm = sum(abs(ST3[i, j] - (1 if i == j else 0)) for i in range(3) for j in range(3))
print(f"|(ρ_3̂(S)·ρ_3̂(T))³ - I| = {ST3_norm}")


# ============================================================
# STEP 4 — Apply ρ_3̂(S) to Y_3̂^(3)(i) and check eigenvalue
# ============================================================
print("\n" + "=" * 70)
print("STEP 4: Eigenvalue test for Y_3̂^(3)(i)")
print("=" * 70)
print("Expected: ρ_3̂(S) · Y_3̂^(3)(i) = i · Y_3̂^(3)(i)")
print("(since at τ=i with k=3: Y(i) = -i ρ(S) Y(i) ⟹ ρ(S) Y(i) = +i · Y(i))")

S_Y = rho_3hat_S * Y_3hat_i
print(f"\nρ_3̂(S) · Y_3̂^(3)(i) =")
for r in range(3):
    print(f"  [{r}] = {S_Y[r]}")

print(f"\ni · Y_3̂^(3)(i) =")
i_Y = [mp.mpc(0, 1) * Y_3hat_i[r] for r in range(3)]
for r in range(3):
    print(f"  [{r}] = {i_Y[r]}")

print(f"\nDifference (should be 0):")
diffs = []
for r in range(3):
    d = S_Y[r] - i_Y[r]
    diffs.append(abs(d))
    print(f"  [{r}]: {d}  |·| = {abs(d)}")
print(f"\nMax |diff| = {max(diffs)}")

if max(diffs) < 1e-25:
    print("✓✓✓ Y_3̂^(3)(i) IS an eigenvector of ρ_3̂(S) with eigenvalue +i ✓✓✓")
else:
    # Try eigenvalue -i instead:
    print("\nNot eigenvector with eigenvalue +i. Trying -i:")
    diffs2 = []
    for r in range(3):
        d = S_Y[r] - mp.mpc(0, -1) * Y_3hat_i[r]
        diffs2.append(abs(d))
        print(f"  [{r}]: diff with -i Y = {d}, |·| = {abs(d)}")
    print(f"Max |diff with -i| = {max(diffs2)}")


# ============================================================
# STEP 5 — Construct ρ_3̂'(S) and test on Y_3̂'^(3)(i)
# ============================================================
print("\n" + "=" * 70)
print("STEP 5: Eigenvalue test for Y_3̂'^(3)(i)")
print("=" * 70)

# T-eigenvalues for 3̂': diag(-i, 1, -1) [from Step 1 of 01_S_action])
T_3prime = mp.matrix([[mp.mpc(0, -1), 0, 0],
                      [0, 1, 0],
                      [0, 0, -1]])

# Try alpha = +i/2 for 3̂' (from layout: M with same M_block but +i/2)
# Verify: (i/2 M_block)² = -1/4 · 4I = -I ✓ same as before
# Now (S T_3prime)³ = ?
rho_3prime_S = (mp.mpc(0, 1) / 2) * M_block
S2p = rho_3prime_S * rho_3prime_S
print(f"|ρ_3̂'(S)² - (-I)| = {sum(abs(S2p[i,j] - (-1 if i==j else 0)) for i in range(3) for j in range(3))}")

STp = rho_3prime_S * T_3prime
ST3p = STp * STp * STp
print(f"|(ρ_3̂'(S)·ρ_3̂'(T))³ - I| = {sum(abs(ST3p[i,j] - (1 if i==j else 0)) for i in range(3) for j in range(3))}")

# Try -i/2 instead
rho_3prime_S_neg = (mp.mpc(0, -1) / 2) * M_block
ST3p_neg = (rho_3prime_S_neg * T_3prime)
ST3p_neg = ST3p_neg * ST3p_neg * ST3p_neg
print(f"|(-(i/2) M · T_3prime)³ - I| = {sum(abs(ST3p_neg[i,j] - (1 if i==j else 0)) for i in range(3) for j in range(3))}")
print(f"|(-(i/2) M · T_3prime)³ + I| = {sum(abs(ST3p_neg[i,j] - (-1 if i==j else 0)) for i in range(3) for j in range(3))}")


# Pick whichever works for (ST)³ = I
# Then test on Y_3prime_i
print(f"\nTrying ρ_3̂'(S) = +i/2 · M:")
S_Yp = rho_3prime_S * Y_3prime_i
print(f"\nρ_3̂'(S) · Y_3̂'^(3)(i) =")
for r in range(3):
    print(f"  [{r}] = {S_Yp[r]}")
# Eigenvalue at τ=i for k=3 form: ρ(S) Y(i) = +i Y(i)  (same calculation)
print(f"\ni · Y_3̂'^(3)(i) =")
for r in range(3):
    print(f"  [{r}] = {mp.mpc(0,1) * Y_3prime_i[r]}")
print(f"\nDifference:")
diffsp = []
for r in range(3):
    d = S_Yp[r] - mp.mpc(0,1) * Y_3prime_i[r]
    diffsp.append(abs(d))
    print(f"  [{r}]: {d}, |·| = {abs(d)}")
print(f"Max diff = {max(diffsp)}")


# ============================================================
# STEP 6 — Y_1̂'^(3)(i) eigenvalue test
# ============================================================
print("\n" + "=" * 70)
print("STEP 6: Y_1̂'^(3)(i) eigenvalue check")
print("=" * 70)

# ρ_1̂'(S) = -i, ρ_1̂'(T) = i
# At τ=i, k=3: Y(i) = -i · ρ(S) Y(i) = -i · (-i) Y(i) = -1 · Y(i)
# This forces Y_1̂'^(3)(i) = 0!

# Wait let's recompute: At τ=i, Y(i) = (cτ+d)^k ρ(S) Y(i) where (cτ+d) at S=i = i
# So Y(i) = i^3 ρ(S) Y(i) = -i · ρ(S) Y(i)
# For 1̂' with ρ(S) = -i: Y(i) = -i · (-i) Y(i) = -1 · Y(i) ⟹ 2 Y(i) = 0 ⟹ Y_1̂'^(3)(i) = 0!
print("For Y_1̂'^(3)(τ) at τ = i:")
print(f"  Eigenvalue eqn: Y(i) = i^3 · ρ_1̂'(S) Y(i) = -i · (-i) Y(i) = -Y(i)")
print(f"  ⟹ Y_1̂'^(3)(i) = 0  (Z_2 forbids this contribution!)")
print(f"\nNumerical: Y_1̂'^(3)(i) = {Y_1prime_i}")
print(f"  |Y_1̂'^(3)(i)| = {abs(Y_1prime_i)}")
print(f"\n⚠ But computed value is NON-ZERO! Investigate...")

# Wait — let me reconsider. Y_1̂'^(3) = √3 (εθ⁵ - ε⁵θ) at τ=i is √3 ε(i) θ(i) (θ(i)⁴ - ε(i)⁴)
val = mp.sqrt(3) * ep_C * th_C * (th_C ** 4 - ep_C ** 4)
print(f"  Direct: √3 ε(i) θ(i) (θ(i)⁴ - ε(i)⁴) = {val}")

# Hmm, non-zero. Must mean ρ_1̂'(S) is NOT -i, or my eigenvalue argument is wrong.
# Let me check Table 7 again carefully.
# From layout 1864: row "1̂0" (which is 1̂') has ρ(S) = "-i", ρ(T) = "i", ρ(R) = "-1"
# Let me try Y(i) = -i · (-i) Y(i) more carefully.
# Y(S·i) = Y(i) on LHS
# RHS = (cτ+d)^k ρ(S) Y(τ=i) = i^3 · (-i) Y(i) = -i · -i Y(i) = -1 · Y(i) ✗

# But the computed value is non-zero. So contradicition.
# Either: (a) Y_1̂'^(3) is NOT a valid weight-3 modular form transforming with ρ_1̂'(S)=-i
#         (b) My S-action formula is wrong
#         (c) Y_1̂' is not a singlet; I misidentified something.
print("\n⚠ Resolution needed: either Y_1̂'^(3) is not really a singlet at τ=i")
print("  (which would mean it's a Z_2-FORBIDDEN form by H18 selection rule)")
