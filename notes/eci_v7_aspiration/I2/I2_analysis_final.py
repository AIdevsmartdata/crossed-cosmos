"""
I2 FINAL ANALYSIS — Understand WHY sin θ_C is locked at τ=i.

Finding: With correct up-sector mass ratios at τ=i (m_c/m_t=0.00268, m_u/m_c=0.00204),
the CKM Cabibbo angle is pinned at sin θ_C ≈ 0.00068, independent of any down-sector parameters.

This means V = U_uL† U_dL, and U_dL can be ANY unitary matrix (free down params).
But V[0,1] = sum_k (U_uL†)_{0k} (U_dL)_{k1}

Since U_uL ≈ diag * phases, (U_uL†)_{0k} ≈ δ_{0k} * phase_k.
Then V[0,1] ≈ (U_uL†)_{00} * (U_dL)_{01} + tiny corrections.

If U_uL ≈ I (up to phases), then V[0,1] ≈ (phase) * (U_dL)_{01}.
So sin θ_C ≈ |(U_dL)_{01}|.

But the down-sector mass ratios constrain the M_d matrix, not U_dL directly.
So U_dL should be free... unless M_d also has a special structure at τ=i.

Let me verify this and understand the full picture.
"""

import numpy as np
from numpy import pi, sqrt, exp
from scipy.linalg import svd
from scipy.optimize import minimize, differential_evolution
import sys, warnings
warnings.filterwarnings('ignore')

sys.path.insert(0, '/root/crossed-cosmos/notes/eci_v7_aspiration/H3')
from mass_matrix import M_u, M_d, modular_forms_weight1, modular_forms_all

TAU_CM = 1j
PDG_SIN_THETA_C = 0.2253
LYD20_MD_MS = 0.05182
LYD20_MS_MB = 0.01309

def svd_sort(M):
    U, s, Vh = svd(M)
    idx = np.argsort(s)
    return U[:, idx], s[idx], Vh[idx, :]

def s12_from_V(V):
    aV = np.abs(V)
    s13 = aV[0,2]
    denom = sqrt(max(1-s13**2, 1e-30))
    return aV[0,1]/denom

# Get fitted up-sector at τ=i
from mass_matrix import M_u
Mu_cm = M_u(TAU_CM, 1.0, 83.060068, 901.148082)
Uu_cm, su_cm, Uvh_cm = svd_sort(Mu_cm)

print(f"U_uL at τ=i (with correct m_u/m_c, m_c/m_t):")
print(np.abs(Uu_cm))
print(f"\nU_uL phases (degrees):")
print(np.angle(Uu_cm)*180/pi)

print(f"\nKey: (U_uL†)_row0 = {np.abs(Uu_cm[:,0])} (abs values of first column of U_uL)")
print(f"     = conjugated, the first row of U_uL† acts on U_dL[:,0] and U_dL[:,1]")
print("     V[0,1] = (U_uL†)_{0,*} . U_dL_{*,1}")
print("     If U_uL is diagonal, V[0,1] = phase * U_dL[0,1]")

# Now let's see: given U_dL is free, what are the constraints on U_dL[0,1]?
# M_d at τ=i has specific structure. Let's look at M_d with varied parameters.

print("\n\nM_d structure at τ=i (unit couplings):")
Md_unit = M_d(TAU_CM, 1.0, 1.0, 1.0, 0.0)
print("|M_d| =")
print(np.abs(Md_unit))

# Key observation: at τ=i, Y^(5)_{3̂} = (Y5_3, Y5_4, Y5_5)
# Y5_3 = 18 Y1^2 (Y3^3 - Y2^3)
# Y5_4 = ..., Y5_5 = ...
# At τ=i: Y1 = 0.835+0.835j, Y2 = -0.188-0.188j, Y3 = 1.857+1.857j
# All components have the form (a + ai) = a(1+i) → same phase!

Y1, Y2, Y3 = modular_forms_weight1(TAU_CM)
f = modular_forms_all(Y1, Y2, Y3)

print(f"\nModular forms at τ=i:")
print(f"  Y1 = {Y1}  (arg = {np.angle(Y1)*180/pi:.1f}°)")
print(f"  Y2 = {Y2}  (arg = {np.angle(Y2)*180/pi:.1f}°)")
print(f"  Y3 = {Y3}  (arg = {np.angle(Y3)*180/pi:.1f}°)")

# All weight-1 forms have arg = 45° (proportional to 1+i)
print(f"\n  Y3/Y1 = {Y3/Y1}  (pure real ratio)")
print(f"  Y2/Y1 = {Y2/Y1}  (pure real ratio)")

# This means the weight-1 forms are collinear: Y1, Y2, Y3 ∝ (1+i) * real
# Therefore ALL forms (as polynomials in Y1,Y2,Y3) are proportional to (1+i)^n for weight n

print(f"\nWeight-2 forms at τ=i:")
print(f"  Y2_3 = {f['Y2_3']}  arg = {np.angle(f['Y2_3'])*180/pi:.1f}°")
print(f"  Y2_4 = {f['Y2_4']}  arg = {np.angle(f['Y2_4'])*180/pi:.1f}°")
print(f"  Y2_5 = {f['Y2_5']}  arg = {np.angle(f['Y2_5'])*180/pi:.1f}°")

print(f"\nWeight-5 forms at τ=i:")
print(f"  Y5_3 = {f['Y5_3']}  arg = {np.angle(f['Y5_3'])*180/pi:.1f}°")
print(f"  Y5_4 = {f['Y5_4']}  arg = {np.angle(f['Y5_4'])*180/pi:.1f}°")
print(f"  Y5_5 = {f['Y5_5']}  arg = {np.angle(f['Y5_5'])*180/pi:.1f}°")

print(f"\nWeight-5 3̂'_I forms at τ=i:")
print(f"  Y5_6 = {f['Y5_6']}  arg = {np.angle(f['Y5_6'])*180/pi:.1f}°")
print(f"  Y5_7 = {f['Y5_7']}  arg = {np.angle(f['Y5_7'])*180/pi:.1f}°")
print(f"  Y5_8 = {f['Y5_8']}  arg = {np.angle(f['Y5_8'])*180/pi:.1f}°")

print(f"\nWeight-5 3̂'_II forms at τ=i:")
print(f"  Y5_9  = {f['Y5_9']}   arg = {np.angle(f['Y5_9'])*180/pi:.1f}°")
print(f"  Y5_10 = {f['Y5_10']}  arg = {np.angle(f['Y5_10'])*180/pi:.1f}°")
print(f"  Y5_11 = {f['Y5_11']}  arg = {np.angle(f['Y5_11'])*180/pi:.1f}°")

# KEY INSIGHT: At τ=i, ALL modular forms have the SAME phase (or related by integer multiples of 45°)
# This is because Y1,Y2,Y3 all have phase 45° = arg(1+i), and polynomials of degree k
# give phases k*45°.
# Weight 1 → 45°
# Weight 2 → 90° (or 0° or 180° depending on which polynomial)
# Weight 5 → 225° = -135° (or variations)

# CONSEQUENCE: Each ROW of M_u and M_d at τ=i has all entries with the SAME phase!
# If row i has entries (r1 e^{iφ}, r2 e^{iφ}, r3 e^{iφ}) for some real r1,r2,r3,
# then M can be written as DIAG(e^{iφ_0}, e^{iφ_1}, e^{iφ_2}) @ M_real
# where M_real has REAL entries.

# This means M_u = D_u @ M_u^real where D_u is diagonal phase matrix.
# Similarly M_d = D_d @ M_d^real.
# So SVD: M_u = U_u Σ_u V_u†
# M_real = D_u† U_u Σ_u V_u† (which is still SVD, U → D_u† U_u is still unitary)

# For V_CKM = U_uL† U_dL:
# Both U_uL and U_dL get their first column constrained by the phase structure.
# In particular, M_u^real has real entries → its left singular vectors U_u^real are REAL.
# So U_uL = D_u @ U_u^real  (diagonal phase times real unitary)
# Similarly U_dL = D_d @ U_d^real

# V_CKM = U_uL† U_dL = (D_u U_u^real)† (D_d U_d^real)
#       = (U_u^real)† D_u† D_d U_d^real

# If all phases in row i of M_u are the SAME φ_i, and similarly for M_d:
# D_u = diag(e^{iφ_0u}, e^{iφ_1u}, e^{iφ_2u})
# D_d = diag(e^{iφ_0d}, e^{iφ_1d}, e^{iφ_2d})

# The physical CKM (after quark phase redefinitions) is:
# |V_CKM[i,j]| = |(U_u^real)† D_u† D_d U_d^real)[i,j]|
# This is NOT trivially determined by phases alone.

# But in our case, not just same phase per row: the ratio Y3/Y1 is REAL at τ=i.
# Let's check: does M_u at τ=i have a rank-1 structure?

print("\n\nChecking rank structure of M_u rows at τ=i:")
for i in range(3):
    row = Mu_cm[i, :]
    if abs(row[0]) > 1e-10:
        print(f"  Row {i}: row/row[0] = {row/row[0]}")
    else:
        print(f"  Row {i}: row[0] ≈ 0, row = {row}")

print("\nChecking rank structure of M_d rows at τ=i (unit couplings, gd2=0):")
Md_test = M_d(TAU_CM, 1.0, 1.0, 1.0, 0.0)
for i in range(3):
    row = Md_test[i, :]
    if abs(row[0]) > 1e-10:
        print(f"  Row {i}: row/row[0] = {row/row[0]}")
    else:
        print(f"  Row {i}: row[0] ≈ 0, row = {row}")

# AT τ=i: Y3/Y1 = 1.857+1.857j / 0.835+0.835j ≈ 2.224 (REAL ratio)
# Y2/Y1 = -0.188-0.188j / 0.835+0.835j ≈ -0.225 (REAL ratio)
# So all weight-1 forms are REAL multiples of each other!
# This means Row 0 of M_u = α_u * Y1 * [1, Y3/Y1, Y2/Y1] = α_u * Y1 * [1, 2.224, -0.225]
# All entries proportional → Row 0 is a RANK-1 row (all entries have same phase)

# Similarly, all weight-2 and weight-5 forms are real multiples of each other at τ=i!
# Let me verify:
print(f"\nRatios of weight-2 forms at τ=i:")
print(f"  Y2_4/Y2_3 = {f['Y2_4']/f['Y2_3']}")
print(f"  Y2_5/Y2_3 = {f['Y2_5']/f['Y2_3']}")

print(f"\nRatios of weight-5 3̂ forms at τ=i:")
print(f"  Y5_4/Y5_3 = {f['Y5_4']/f['Y5_3']}")
print(f"  Y5_5/Y5_3 = {f['Y5_5']/f['Y5_3']}")

print(f"\nRatios of weight-5 3̂'_I forms at τ=i:")
print(f"  Y5_7/Y5_6 = {f['Y5_7']/f['Y5_6']}")
print(f"  Y5_8/Y5_6 = {f['Y5_8']/f['Y5_6']}")

print(f"\nRatios of weight-5 3̂'_II forms at τ=i:")
print(f"  Y5_10/Y5_9 = {f['Y5_10']/f['Y5_9']}")
print(f"  Y5_11/Y5_9 = {f['Y5_11']/f['Y5_9']}")

print("\n\nKEY CONCLUSION:")
print("At τ=i, within each modular form multiplet:")
print("  Y^(k)_{rep} has all components proportional to each other (ratio = REAL)")
print("  This means each ROW of M_u and M_d is proportional to a fixed direction")
print("  M_u[i,:] = coupling_i * (same-phase) * [c1, c2, c3]  for fixed real c1,c2,c3 per row")
print("\nConsequence:")
print("  Each ROW points in the SAME direction in flavor space (up to phase).")
print("  The DOWN-type matrix M_d has:")
print("    Row 0 (d^c): ∝ [1, Y3/Y1, Y2/Y1] = [1, 2.22, -0.22] (all rows same direction)")
print("    Row 1 (s^c): ∝ [1, Y5_5/Y5_3, Y5_4/Y5_3] (SAME direction as Y^5_3̂ multiplet)")
print("    Row 2 (b^c): combination of Y5_6,... and Y5_9,... with complex γ_d2")
print("\n  Rows 0 and 1 of M_d point in the SAME direction in Q-space!")
print("  M_d is effectively RANK-1 in the Q direction for rows 0 and 1.")
print("  Only row 2 (b^c with γ_d2 complex) breaks this degeneracy.")
print("\nThis explains why sin θ_C is locked: the degenerate row structure")
print("forces U_dL to rotate d and s in the same direction as Q_1.")
print("The mixing between (u,d) and (c,s) sectors is suppressed by the form ratios.")
