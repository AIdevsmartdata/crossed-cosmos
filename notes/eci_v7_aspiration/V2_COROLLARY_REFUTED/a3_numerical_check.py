"""Numerical sanity check using high-precision Dedekind eta values at tau=i."""
import sys
sys.path.insert(0, '/root/crossed-cosmos/notes/eci_v7_aspiration/V2')
from v2_audit import weight1_forms, all_forms
import numpy as np

tau = 1j
Y1, Y2, Y3 = weight1_forms(tau, n_terms=200)
f = all_forms(Y1, Y2, Y3)
print(f"Y1^2 + 2 Y2 Y3 = {Y1**2 + 2*Y2*Y3:.3e}  (should be ~0)")

# c^c row of M_u: weight-2, columns (Y2_3, Y2_5, Y2_4)
v_c = np.array([f['Y2_3'], f['Y2_5'], f['Y2_4']])
# t^c row of M_u: weight-5 3̂, columns (Y5_3, Y5_5, Y5_4)
v_t = np.array([f['Y5_3'], f['Y5_5'], f['Y5_4']])

print(f"\nc^c row phases (deg): {[np.angle(x)*180/np.pi for x in v_c]}")
print(f"t^c row phases (deg): {[np.angle(x)*180/np.pi for x in v_t]}")

# Hermitian inner product
inner = np.vdot(v_c, v_t)
nb = np.linalg.norm(v_c)
nt = np.linalg.norm(v_t)
cos = inner / (nb * nt)
print(f"\n<c^c row, t^c row>     = {inner:.6e}")
print(f"||c^c row|| ||t^c row|| = {nb*nt:.6e}")
print(f"cos(theta)              = {cos:.10e}")
print(f"|cos(theta)|            = {abs(cos):.10e}")
print(f"|cos(theta)|^2          = {abs(cos)**2:.10e}")
print(f"\ntheta (deg)             = {np.arccos(min(abs(cos),1.0))*180/np.pi:.6f}")

# Also check if it's small relative to typical alignment
# Random complex vector overlap is O(1)
print(f"\nFor reference, sin(theta) = {np.sqrt(1-abs(cos)**2):.10e}")
