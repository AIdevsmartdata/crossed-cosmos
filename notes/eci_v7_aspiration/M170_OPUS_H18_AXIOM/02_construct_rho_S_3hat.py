#!/usr/bin/env python3
"""
M170 step 2 — Construct ρ_3̂(S) for irrep 3̂ of S4' = SL(2,Z_4).

Constraints:
  ρ_3̂(T) = diag(i, -1, 1)   (NPP20 Table 7)
  ρ_3̂(S)^2 = ρ_3̂(R) = -I    (since 3̂ is a hatted, R-odd irrep)
  (ρ_3̂(S) · ρ_3̂(T))^3 = ρ_3̂(R) = -I  (relation R = (ST)^3 in S4' is wrong;
                                  actually NPP20 eq 2.8: (ST)^3 = 1, R^2 = 1)
  Also ρ_3̂(S) is unitary, symmetric (Table 7 caption: symmetric basis)

Then: at τ = i, we compute Y_3̂^(3)(i) (using corrected formulas from script 01)
and check it is an eigenvector of ρ_3̂(S) with the right eigenvalue.

Also: at τ = i, S = ((0,-1),(1,0)) gives c=1, d=0, so cτ+d = i, (cτ+d)^k = i^k.
For weight k=3 modular form with values at i:
  Y(S·i) = (cτ+d)^k ρ(S) Y(τ) = i^3 ρ(S) Y(i) = -i ρ(S) Y(i)
But S·i = i, so Y(i) = -i ρ(S) Y(i)  ⟺  ρ(S) Y(i) = i · Y(i).

So we need Y_3̂^(3)(i) to be an eigenvector of ρ_3̂(S) with eigenvalue +i.
"""

import mpmath as mp
mp.mp.dps = 30

import numpy as np
import sympy as sp


# ============================================================
# STEP 1 — Solve ρ_3̂(S) symbolically given constraints
# ============================================================
# Ansatz: ρ_3̂(S) = α · M, where M is symmetric, unitary up to factor
# From Table 7, the basis is symmetric. The S-matrix should have the form
#   ρ_3̂(S) = α · [[a, b, b], [b, c, d], [b, d, c]]
# with appropriate symmetry under permutation of last two columns.

# Use NPP20's claim from layout: ρ_3̂(S) = (i/2 OR -i/2) · M_block
# We'll determine which by demanding ρ_3̂(S)^2 = -I (since 3̂ is R-odd).

M_block = sp.Matrix([[0, sp.sqrt(2), sp.sqrt(2)],
                     [sp.sqrt(2), -1, 1],
                     [sp.sqrt(2), 1, -1]])

print("M_block =")
sp.pprint(M_block)

print("\nM_block^2 =")
M_block2 = M_block * M_block
sp.pprint(M_block2)
# Should be 2·I (so M_block^2 = 2·I and (i/2 · M)^2 = -1/4 · 2I = -1/2 · I)
# Hmm — we want ρ(S)^2 = -I, so we need (α M)^2 = α² · 2I = -I  ⟹  α² = -1/2 ⟹ α = ±i/√2
# Not ±i/2!

# Let me check more carefully:
print("\nα² · 2 = -1 ⟹ α = ±i/√2")
alpha_sq = sp.Rational(-1, 2)
print(f"  α² = {alpha_sq}, α = ±i/√2 ≈ ±{1/sp.sqrt(2)}j")

# So ρ_3̂(S) = (±i/√2) · M_block ?
# But Table 7 visually shows "i/2" prefactor — maybe the normalization of M_block is different.
# Let me try alternative: M' = M_block / √2, then M'^2 = M_block^2 / 2 = I.
# Then (αM')^2 = α² · I = -I ⟹ α = ±i. Compact form: ρ(S) = ±i · M_block/√2 = ±i·M_block/√2.
# That doesn't match Table 7's "i/2" either.

# Try: ρ_3̂(S) = (i/2) M_block. Then ρ(S)^2 = -1/4 · 2 · I = -1/2 I, NOT -I.
# This is INCONSISTENT! Table 7 readout must be wrong.

# Try alt M_block structures:
M_alt = sp.Matrix([[-1, sp.sqrt(2), sp.sqrt(2)],
                   [sp.sqrt(2), 1, -1],
                   [sp.sqrt(2), -1, 1]])
print(f"\nAlt M (with (1,1) = -1): M^2 =")
sp.pprint(M_alt * M_alt)

# Try: M_alt2 = [[0, √2, √2],[√2, -1, 1],[√2, 1, -1]] but check OFF-diagonal of M^2
# This is M_block. M_block^2 already computed = ...

# So M_block · M_block:
print("\nDouble-check M_block² entries:")
for i in range(3):
    for j in range(3):
        print(f"  M²[{i},{j}] = {M_block2[i,j]}")


# ============================================================
# STEP 2 — Solve for ρ_3̂(S) using symbolic constraint solver
# ============================================================
print("\n" + "=" * 70)
print("STEP 2: Solve for ρ_3̂(S) given ρ(T) and S² = -I, (ST)³ = I")
print("=" * 70)

# ρ_3̂(T) = diag(i, -1, 1)
T_3hat = sp.diag(sp.I, -1, 1)
print("ρ_3̂(T) = ")
sp.pprint(T_3hat)

# General ansatz for symmetric S of form a M_block (possible diagonal too)
# Try ρ_3̂(S) = α M_block
alpha = sp.symbols('alpha')
S_ansatz = alpha * M_block

S2 = S_ansatz * S_ansatz
print("\nρ(S)² = α² · M² =")
sp.pprint(sp.simplify(S2))

# We need ρ(S)² = -I. Let's check what α gives this:
# α² · 2 · I + nondiag ?
# Hmm — let me re-multiply M_block by itself carefully:
print("\nReconstruct M_block² explicitly:")
expanded = sp.zeros(3, 3)
for i in range(3):
    for j in range(3):
        expr = sum(M_block[i, k] * M_block[k, j] for k in range(3))
        expanded[i, j] = sp.simplify(expr)
sp.pprint(expanded)


# ============================================================
# STEP 3 — Test eigenvalues of ρ(T) S ρ(T) S ... structure
# ============================================================
print("\n" + "=" * 70)
print("STEP 3: Solve for α from (ST)^3 = I and S^2 = ±I")
print("=" * 70)

# Try α = i/√2 first
alpha_val = sp.I / sp.sqrt(2)
S_test = alpha_val * M_block
S2_test = sp.simplify(S_test * S_test)
print(f"α = i/√2:  S² =")
sp.pprint(S2_test)

ST = S_test * T_3hat
ST3 = ST * ST * ST
print(f"\n(ST)³ for α=i/√2 =")
sp.pprint(sp.simplify(ST3))


# Try α = -i/√2
alpha_val2 = -sp.I / sp.sqrt(2)
S_test2 = alpha_val2 * M_block
S2_test2 = sp.simplify(S_test2 * S_test2)
print(f"\nα = -i/√2:  S² =")
sp.pprint(S2_test2)

ST2 = S_test2 * T_3hat
ST3_2 = ST2 * ST2 * ST2
print(f"\n(ST)³ for α=-i/√2 =")
sp.pprint(sp.simplify(ST3_2))


# ============================================================
# STEP 4 — Fast numerical test with NPP20 quoted ρ_3̂(S) = (-i/2) M
#          Check eigenvectors of this to see if Y(i) is among them
# ============================================================
print("\n" + "=" * 70)
print("STEP 4: Numerical eigendecomposition of various candidate ρ_3̂(S)")
print("=" * 70)

# Candidates with different normalization
def make_S(alpha_complex, M):
    return np.array([[alpha_complex * complex(M[i, j]) for j in range(3)] for i in range(3)])

M_np = np.array([[float(M_block[i, j]) for j in range(3)] for i in range(3)])
T_np = np.diag([1j, -1, 1])

# alpha options
import itertools
options = {}
for amp_str, amp_val in [("i/2", 0.5j), ("-i/2", -0.5j),
                          ("i/sqrt2", 1j / np.sqrt(2)), ("-i/sqrt2", -1j / np.sqrt(2)),
                          ("1/2", 0.5), ("-1/2", -0.5),
                          ("1/sqrt2", 1 / np.sqrt(2))]:
    S_candidate = amp_val * M_np
    # Check S^2 = ?I, ?
    S2 = S_candidate @ S_candidate
    sq_diff_pI = np.linalg.norm(S2 - np.eye(3))
    sq_diff_nI = np.linalg.norm(S2 + np.eye(3))
    # Check (ST)^3 = ?I
    ST = S_candidate @ T_np
    ST3 = ST @ ST @ ST
    cube_diff_pI = np.linalg.norm(ST3 - np.eye(3))
    cube_diff_nI = np.linalg.norm(ST3 + np.eye(3))
    options[amp_str] = (S_candidate, sq_diff_pI, sq_diff_nI, cube_diff_pI, cube_diff_nI)
    print(f"  α = {amp_str}:  |S²-I|={sq_diff_pI:.4f}  |S²+I|={sq_diff_nI:.4f}  "
          f"|(ST)³-I|={cube_diff_pI:.4f}  |(ST)³+I|={cube_diff_nI:.4f}")

print("\n→ For irrep 3̂ (hatted, R-odd), expect ρ(R) = -I, so S² = -I (i.e. small |S²+I|)")
print("→ And (ST)³ = 1 always, so small |(ST)³-I|")
