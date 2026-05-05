"""Sanity checks for f^{ij}(tau) — additional consistency tests."""
import numpy as np
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from f_ij_modular import Y123_at_tau, f_ij_numeric

# Sanity 1: Constraint Y1^2 + 2Y2Y3 = 0 at tau=i
tau = 1j
Y1, Y2, Y3 = Y123_at_tau(tau, 120)
print(f'Constraint Y1^2 + 2Y2Y3 at tau=i: {Y1**2 + 2*Y2*Y3:.4e} (should be ~0)')
print(f'Y1(i) = {Y1:.4e}')
print(f'Y2(i) = {Y2:.4e}')
print(f'Y3(i) = {Y3:.4e}')

# Sanity 2: At LYD20 best-fit tau
tau_bf = -0.4999 + 0.8958j
Y1, Y2, Y3 = Y123_at_tau(tau_bf, 120)
print(f'\nAt LYD20 BF tau={tau_bf}:')
print(f'Constraint Y1^2 + 2Y2Y3: {Y1**2 + 2*Y2*Y3:.4e}')
M_bf = f_ij_numeric(tau_bf, 120)
print('|f^{ij}(tau_BF)|:')
print(np.abs(M_bf))

# Sanity 3: Singular values
sv_i = np.sort(np.linalg.svd(f_ij_numeric(1j, 120), compute_uv=False))
print(f'\nSingular values of f(i) (sorted): {sv_i}')
print(f'Ratios at tau=i (uncoupled): u/c = {sv_i[0]/sv_i[1]:.4e}, c/t = {sv_i[1]/sv_i[2]:.4e}')

# Sanity 4: c-row entries
M = f_ij_numeric(1j, 120)
print(f'\nc-row entries of f(i):')
for j in range(3):
    print(f'  f[1,{j}] = Re={np.real(M[1,j]):.4e}, Im={np.imag(M[1,j]):.4e}, |.|={np.abs(M[1,j]):.4e}')
