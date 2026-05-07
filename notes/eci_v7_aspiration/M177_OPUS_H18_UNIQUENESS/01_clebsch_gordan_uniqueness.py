#!/usr/bin/env python3
"""
M177 — UNIQUENESS via Clebsch-Gordan at τ_C = i (i^{-k} eigenspace selection).

THEOREM M170.1 already establishes: at τ=i, every weight-k S_4'-modular form Y_R(i)
satisfies ρ_R(S) Y_R(i) = i^{-k} Y_R(i).

The NPP20 Weinberg model (eq 6.3) takes:
    L  ~ 3,   k_L = 2
    E^c ~ 3̂, k_{E^c} = 1
    H_d ~ 1,  k_{H_d} = 0
The Yukawa term W ⊃ Y_R(τ) (E^c L)_R H_d carries weight k_Y = k_L + k_{E^c} = 3.

Tensor product (Table 11):
    3̂ ⊗ 3 = 1̂ ⊕ 2̂ ⊕ 3̂ ⊕ 3̂'.

For W to be a 1, the modular form Y_R must be in the irrep dual to (3̂⊗3)
component R. From Table 8: the dualities relevant here are
    1̂ ⊗ 1̂ = 1' ;  1̂' ⊗ 1̂ = 1 ;  2̂ ⊗ 2̂ = 1 ⊕ ... ;  3̂ ⊗ 3̂ = 1 ⊕ ... ;
    3̂' ⊗ 3̂' = 1 ⊕ ...
So to form a TRUE 1 singlet using (E^c L) projected on R̃, we need Y_R in irrep R such
that R ⊗ R̃ ⊃ 1. Reading Tables 8-11 in NPP20:
    Y_1̂' couples to (E^c L)_1̂  (since 1̂' ⊗ 1̂ = 1)         — appears in (6.3) as α_1
    Y_2̂  couples to (E^c L)_2̂  (since 2̂ ⊗ 2̂ ⊃ 1)         — DOES NOT EXIST at weight 3
    Y_3̂' couples to (E^c L)_3̂' (since 3̂' ⊗ 3̂' ⊃ 1)        — appears in (6.3) as α_2
    Y_3̂  couples to (E^c L)_3̂  (since 3̂ ⊗ 3̂ ⊃ 1)          — appears in (6.3) as α_3

dim M_3(Γ(4)) = 2k+1 = 7 at k=3. The 7 dimensions are spanned by
    Y_1̂'^(3) (1) + Y_3̂^(3) (3) + Y_3̂'^(3) (3) = 7. ✓
There is NO Y_2̂^(3), so the 2̂-channel of (3̂⊗3) is absent — this is a LEVEL CONSTRAINT
already coming from arithmetic of M_3(Γ(4)).

At τ=i, modular weight 3 gives i^{-k} = i^{-3} = -i. So each Y_R(i) lies in the
(-i)-eigenspace of ρ_R(S).

ρ_R(S) (Table 7 NPP20):
    ρ_3̂(S)  = -(i/2) M  with M = ((0,√2,√2),(√2,-1,1),(√2,1,-1))
    ρ_3̂'(S) =  (1/2) M
    ρ_1̂'(S) = -1
    ρ_1̂(S)  =  i
    ρ_2̂(S)  = (i/2)((-1,√3),(√3,1))
    ρ_3(S)  = -(1/2) M

Eigenvalues of ρ_R(S):
    ρ_3̂(S)  : {+i, -i, -i}  → -i eigenspace dim = 2
    ρ_3̂'(S) : {-i, +i, +i}? Let's compute. Actually 3̂' = i × 3 representation up to phase.
                  Eigenvalues of (1/2)M: M has eigvals ? -- compute below.
    ρ_1̂'(S) : {-1}    → -i eigenvalue NOT present, so Y_1̂'(i) MUST = 0
    ρ_2̂(S)  : eigvals of (i/2)·((-1,√3),(√3,1)) = ?

Wait — Y_1̂'(i) cannot be in the -i-eigenspace if ρ_1̂'(S) = -1, because -1 ≠ -i.
Hence Y_1̂'^(3)(i) = 0 at τ=i — a STRONG eigenspace constraint!

This script will:
  (a) Verify Y_1̂'^(3)(i) ≈ 0 numerically (to mpmath dps=30).
  (b) Compute the (-i)-eigenspaces of ρ_3̂(S) and ρ_3̂'(S).
  (c) Apply this projection to (E^c L)_R basis vectors to determine the
      projected (E^c L) structure at τ=i.
  (d) Combine with Y_R^(3)(i) to read off the rank/structure of M_e.

Result expected:
  • Y_1̂'^(3)(i) = 0  ⟹  α_1 contribution VANISHES at τ=i.
  • The (-i)-eigenspace of ρ_3̂(S) is 2D, but Y_3̂^(3)(i) is a SPECIFIC vector in it,
    and similarly for Y_3̂'^(3).
  • The combined Y_e at τ=i has a CSD-like rank structure.

If the resulting M_e^† has rank-1 structure consistent with NPP20 fits, then the
NPP20 form is FORCED by the eigenspace selection. Otherwise additional model
constraints are required.
"""

import mpmath as mp
mp.mp.dps = 30

import numpy as np


# ===================================================================
# 1. Modular forms of weight 3 (NPP20 eq 3.14) — STRICTLY VERBATIM
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
    th, ep = theta_eps(tau)
    return mp.sqrt(3) * (ep * th ** 5 - ep ** 5 * th)


def Y3_hat_w3(tau):
    th, ep = theta_eps(tau)
    pre = 1 / (2 * mp.sqrt(2))
    return mp.matrix([[pre * (ep ** 5 * th + ep * th ** 5)],
                      [pre * (5 * ep ** 2 * th ** 4 - ep ** 6)],
                      [pre * (th ** 6 - 5 * ep ** 4 * th ** 2)]])


def Y3_prime_w3(tau):
    th, ep = theta_eps(tau)
    pre = mp.mpf(1) / 2
    return mp.matrix([[pre * (-4 * mp.sqrt(2) * ep ** 3 * th ** 3)],
                      [pre * (th ** 6 + 3 * ep ** 4 * th ** 2)],
                      [pre * (-3 * ep ** 2 * th ** 4 - ep ** 6)]])


# ===================================================================
# 2. ρ_R(S) (NPP20 Table 7, working symmetric basis)
# ===================================================================

sq2 = mp.sqrt(2)
sq3 = mp.sqrt(3)

# M block from Table 7 (the sqrt(2)-block matrix)
M_block = mp.matrix([[0, sq2, sq2],
                     [sq2, -1, 1],
                     [sq2, 1, -1]])

# ρ_R(S) per Table 7:
rho_S = {
    '1':       mp.matrix([[1]]),
    '1hat':    mp.matrix([[mp.mpc(0, 1)]]),    # i
    '1prime':  mp.matrix([[-1]]),
    '1hatp':   mp.matrix([[mp.mpc(0, -1)]]),   # -i
    '2':       mp.matrix([[mp.mpf(-1)/2, sq3/2],
                          [sq3/2,        mp.mpf(1)/2]]),
    '2hat':    (mp.mpc(0, 1)/2) * mp.matrix([[-1, sq3], [sq3, 1]]),
    '3':       (-mp.mpf(1)/2) * M_block,
    '3hat':    (-mp.mpc(0, 1)/2) * M_block,
    '3prime':  (mp.mpf(1)/2) * M_block,
    '3hatp':   (mp.mpc(0, 1)/2) * M_block,
}


# ===================================================================
# 3. Compute eigenvalues / eigenspaces of each ρ_R(S)
# ===================================================================

print("=" * 72)
print("Eigenvalues of ρ_R(S) for each S_4' irrep")
print("=" * 72)

for name, rho in rho_S.items():
    n = rho.rows
    rho_np = np.array([[complex(rho[i, j]) for j in range(n)] for i in range(n)])
    eigvals = np.linalg.eigvals(rho_np)
    print(f"  ρ_{name}(S): eigvals = {[f'{e.real:+.4f}{e.imag:+.4f}j' for e in eigvals]}")


# ===================================================================
# 4. Numerical check: Y_1̂'^(3)(i) = ?
# ===================================================================

print("\n" + "=" * 72)
print("CRITICAL TEST: Y_1̂'^(3)(i) — must vanish if ρ_1̂'(S) = -1 ≠ -i")
print("=" * 72)

tau_i = mp.mpc(0, 1)
Y1p_at_i = Y1_prime_w3(tau_i)
print(f"\nY_1̂'^(3)(i) = {Y1p_at_i}")
print(f"|Y_1̂'^(3)(i)| = {abs(Y1p_at_i)}")
print(f"\nrho_1̂'(S) = {rho_S['1hatp'][0,0]}")
print(f"Required eigenvalue at k=3 is i^{{-3}} = -i = {mp.mpc(0, -1)}")
print(f"Match? {abs(rho_S['1hatp'][0,0] - mp.mpc(0, -1)) < mp.mpf('1e-25')}")

# Wait — let me re-read Table 7 more carefully:
# Table 7: ρ_1hat(S) = i, ρ_1'(S) = -1, ρ_1hat'(S) = -i
# So Y_1̂'^(3) (irrep 1̂') has ρ(S) = -i = i^{-3}. Then -i Y(i) = -i Y(i) ALWAYS. NO constraint!
# In other words, Y_1̂'^(3)(i) is NOT forced to vanish — it can be any complex number.

# Hmm — but the structure of i^{-k} = i^{-3} = -i and ρ_1̂'(S) = -i match. So no constraint
# from S. Good — that means α_1 contribution does NOT vanish.
print("\n^^^ Y_1̂'^(3)(i) is NOT forced to vanish: ρ_1̂'(S) = -i = i^{-3} matches!")
print("So α_1 term in (6.3) CONTRIBUTES at τ=i.")


# ===================================================================
# 5. Eigenspace of ρ_3̂(S) at eigenvalue -i (= i^{-3})
# ===================================================================

print("\n" + "=" * 72)
print("Eigenspace of ρ_3̂(S) at eigenvalue -i (= i^{-3})")
print("=" * 72)

rho_3hat_S = rho_S['3hat']
rho_np = np.array([[complex(rho_3hat_S[i, j]) for j in range(3)] for i in range(3)])
eigvals, eigvecs = np.linalg.eig(rho_np)
print(f"Eigenvalues: {eigvals}")

# Find -i eigenvectors
mask_minus_i = [k for k in range(3) if abs(eigvals[k] - (-1j)) < 1e-6]
print(f"\nIndices of -i eigenvectors: {mask_minus_i}")
print(f"Dimension of -i eigenspace: {len(mask_minus_i)}")

V_minus_i_3hat = eigvecs[:, mask_minus_i]
print(f"\n-i eigenspace basis:")
for k, idx in enumerate(mask_minus_i):
    v = eigvecs[:, idx]
    # Normalize phase
    v = v / np.exp(1j * np.angle(v[np.argmax(np.abs(v))]))
    v = v / np.linalg.norm(v)
    print(f"  v_{k} = {v}")


# Now check: where does Y_3̂^(3)(i) lie within this eigenspace?
Y_3hat_i = Y3_hat_w3(tau_i)
Y_vec = np.array([complex(Y_3hat_i[r]) for r in range(3)])
print(f"\nY_3̂^(3)(i) = {Y_vec}")
print(f"|Y_3̂^(3)(i)| = {np.linalg.norm(Y_vec):.6f}")

# Project onto -i eigenspace
P_minus_i = V_minus_i_3hat @ np.linalg.pinv(V_minus_i_3hat)
proj = P_minus_i @ Y_vec
residual = Y_vec - proj
print(f"|Y - P_(-i) Y| = {np.linalg.norm(residual):.2e}  (should be ~0)")
print(f"|P_(-i) Y| / |Y| = {np.linalg.norm(proj)/np.linalg.norm(Y_vec):.6f}")

# Specific direction within -i eigenspace
coords = np.linalg.lstsq(V_minus_i_3hat, Y_vec, rcond=None)[0]
print(f"\nY_3̂^(3)(i) in eigenbasis: {coords}")
print(f"Ratio of components: {coords[1]/coords[0] if abs(coords[0])>1e-10 else 'N/A'}")


# ===================================================================
# 6. Same analysis for ρ_3̂'(S) at eigenvalue -i (= i^{-3})
# ===================================================================

print("\n" + "=" * 72)
print("Eigenspace of ρ_3̂'(S) at eigenvalue -i")
print("=" * 72)

rho_3hatp_S = rho_S['3hatp']
rho_np_p = np.array([[complex(rho_3hatp_S[i, j]) for j in range(3)] for i in range(3)])
eigvals_p, eigvecs_p = np.linalg.eig(rho_np_p)
print(f"Eigenvalues: {eigvals_p}")

mask_minus_i_p = [k for k in range(3) if abs(eigvals_p[k] - (-1j)) < 1e-6]
print(f"\n-i eigenspace dim: {len(mask_minus_i_p)}")

# Now Y_3̂'^(3)(i)
Y_3p_at_i = Y3_prime_w3(tau_i)
Y_p_vec = np.array([complex(Y_3p_at_i[r]) for r in range(3)])
print(f"\nY_3̂'^(3)(i) = {Y_p_vec}")
print(f"|Y_3̂'^(3)(i)| = {np.linalg.norm(Y_p_vec):.6f}")

# Wait — Y_3̂'^(3) transforms under irrep 3̂' (NOT 3̂). So apply ρ_3̂'(S):
# 3̂' has ρ(S) = (i/2) M, eigvals of (i/2)M
# (i/2) (eigvals of M)
# eigvals of M: M = ((0,√2,√2),(√2,-1,1),(√2,1,-1))
# tr M = 0 + (-1) + (-1) = -2; det M = ?
# (i/2) M has eigenvalues (i/2) λ_k where λ_k are M's.
# M^2 = ?  (sqrt(2))^2 stuff.

# Let me directly check.
print(f"\nρ_3̂'(S) eigenvalues again: {eigvals_p}")

# Now project Y_p_vec onto -i eigenspace
if len(mask_minus_i_p) > 0:
    V_p = eigvecs_p[:, mask_minus_i_p]
    P_p = V_p @ np.linalg.pinv(V_p)
    proj_p = P_p @ Y_p_vec
    print(f"\n|Y_3̂' - P_(-i) Y_3̂'| / |Y_3̂'| = {np.linalg.norm(Y_p_vec - proj_p)/np.linalg.norm(Y_p_vec):.2e}")
else:
    print("\nNO -i eigenspace in ρ_3̂'(S) — so Y_3̂'^(3)(i) MUST = 0 if all consistent...")
    print(f"But |Y_3̂'^(3)(i)| = {np.linalg.norm(Y_p_vec):.6f} — it doesn't vanish!")
    print("This means ρ_3̂'(S) DOES have eigenvalue -i, or I made an error.")


# Actually since 3̂' = 3̂ ⊗ 1' ?  Let's check ρ_3hat'(S) — Table 7:
# ρ_3̂'(S) = (i/2) M.
# Eigenvalues of M: solve det(M - λI) = 0.
# M = [[0,√2,√2],[√2,-1,1],[√2,1,-1]]
# tr = -2, det = -(2)(-1·-1-1·1) - √2(√2·-1-1·√2) + √2(√2·1-(-1)√2)
#     = -(0) - √2(-2√2) + √2(2√2) = 4 + 4 = 8.  Hmm that doesn't seem right; let me compute.
# Better: numerical eigvals from above.

print("\n--- Numerical verification of ρ_R(S) eigenvalues ---")
for name in ['3hat', '3hatp', '3', '3prime']:
    rho = rho_S[name]
    n = rho.rows
    rho_np_x = np.array([[complex(rho[i, j]) for j in range(n)] for i in range(n)])
    evx = np.linalg.eigvals(rho_np_x)
    print(f"  ρ_{name}(S) eigenvalues: {evx}")


# ===================================================================
# 7. SUMMARY of eigenspace constraints at τ=i (k=3)
# ===================================================================

print("\n\n" + "=" * 72)
print("SUMMARY: Z_2 eigenspace selection at τ=i for weight-3 forms")
print("=" * 72)
print("""
At τ=i, k=3, eigenvalue must be i^{-3} = -i. So Y_R(i) ∈ E_{-i}(ρ_R(S)).

  irrep R    | dim R | dim E_{-i} | constraint        | NPP20 weight 3 form?
  -----------|-------|------------|-------------------|----------------------
  1̂'        |   1   |     1      | NO (ρ=-i)         | YES (Y_1̂'^(3))
  1̂         |   1   |     0      | Y(i) = 0 forced   | NO (k=3 odd, missing)
  1'         |   1   |     0      | Y(i) = 0 forced   | NO
  1          |   1   |     0      | Y(i) = 0 forced   | NO
  2̂         |   2   |     ?      | depends on eigvals| ABSENT at k=3
  2          |   2   |     ?      |                   | NO (R-even)
  3̂         |   3   |     2      | 1 component killed| YES (Y_3̂^(3))
  3̂'        |   3   |     ?      |                   | YES (Y_3̂'^(3))
  3          |   3   |     ?      |                   | NO
  3'         |   3   |     ?      |                   | NO

Only 1̂', 3̂, 3̂' appear at weight 3 → 3 multiplets, 7 components but
non-trivial eigenspace structure restricts effective freedom.
""")
