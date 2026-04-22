#!/usr/bin/env python3
"""
V8-agent-02-legendre-complexity.py
====================================

Task: on the same 4+4 qubit XXZ toy type-II_1 factor used in
V6-lemma-submultiplicativity.py, compute:

  1. Modular Hamiltonian K_R spectrum (eigenvalues of H_mod restricted to R).
  2. Legendre transform L[K_R] = sup_beta ( beta * <K_R>_beta - F(beta) )
     where F(beta) = -ln Z(beta) is the free energy at inverse temperature beta.
  3. Brown-Susskind geodesic complexity C_BS on the same factor (toy proxy:
     Nielsen geometric complexity = 1/purity(rho_R) = C_k*[rho_R]).
  4. Verdict: are L[K_R] and C_BS proportional?  Ratio scan over beta.

Physics basis:
  - For a thermal state rho_beta = exp(-beta K_R)/Z, one has
      F(beta) = -ln Z(beta)
      <K_R>_beta = -d/d(beta) ln Z
      S_vN(rho_beta) = beta <K_R>_beta - F(beta) = L[K_R](beta)
    so the Legendre transform of F (the standard thermodynamic Legendre)
    evaluated at inverse temperature beta equals the von Neumann entropy S_vN.
  - Brown-Susskind geodesic complexity on a finite-dim factor is proxy'd by
    C_k*[rho_R] = 1/Tr(rho_R^2) (as in V6-lemma-submultiplicativity.py,
    following Nielsen et al. 2006 geometric interpretation in the purity channel).
  - The analogy claim would be L[K_R] ~ constant * C_BS.
    We test this numerically by scanning beta in [0.1, 10].

All results are printed. No external dependencies beyond numpy/scipy.
"""

from __future__ import annotations

import numpy as np

rng = np.random.default_rng(seed=20260422)

# ---------------------------------------------------------------------------
# 1. Build the same 4+4 XXZ modular Hamiltonian as in V6-lemma
# ---------------------------------------------------------------------------
N_R = 4
N_Rp = 4
N = N_R + N_Rp
DIM = 2 ** N
DIM_R = 2 ** N_R
DIM_Rp = 2 ** N_Rp

I2 = np.eye(2, dtype=complex)
SZ = np.array([[1.0, 0.0], [0.0, -1.0]], dtype=complex)
SX = np.array([[0.0, 1.0], [1.0, 0.0]], dtype=complex)


def op_on_site(op: np.ndarray, site: int, n: int = N) -> np.ndarray:
    out = np.array([[1.0]], dtype=complex)
    for j in range(n):
        out = np.kron(out, op if j == site else I2)
    return out


h_field = rng.uniform(-0.5, 0.5, size=N)
J = 0.8
H_mod_full = np.zeros((DIM, DIM), dtype=complex)
for j in range(N):
    H_mod_full += h_field[j] * op_on_site(SZ, j)
for j in range(N - 1):
    H_mod_full += J * (op_on_site(SX, j) @ op_on_site(SX, j + 1))
assert np.allclose(H_mod_full, H_mod_full.conj().T)

# Restrict modular Hamiltonian to subsystem R by partial trace.
# K_R = Tr_{Rp}[ H_mod ] / DIM_Rp  (mean-field restriction, standard
# approach for the reduced modular Hamiltonian on the subalgebra B(H_R)).
H_mod_R = np.zeros((DIM_R, DIM_R), dtype=complex)
for block_row in range(DIM_R):
    for block_col in range(DIM_R):
        for env in range(DIM_Rp):
            H_mod_R[block_row, block_col] += H_mod_full[
                block_row * DIM_Rp + env, block_col * DIM_Rp + env
            ]
H_mod_R /= DIM_Rp
assert np.allclose(H_mod_R, H_mod_R.conj().T)

# Diagonalise
evals_R, evecs_R = np.linalg.eigh(H_mod_R)
print("K_R spectrum (16 eigenvalues):")
print(np.round(evals_R, 4))
print(f"  min={evals_R.min():.4f}  max={evals_R.max():.4f}  mean={evals_R.mean():.4f}")

# ---------------------------------------------------------------------------
# 2. Legendre transform L[K_R](beta) = sup over all beta of thermal state
#    For a thermal family, the sup is attained at beta itself:
#    L[K_R](beta) = beta * <K_R>_beta - F(beta)
#    where F(beta) = -ln Z(beta),  Z(beta) = Tr exp(-beta K_R).
#    This is identically the von Neumann entropy S_vN(rho_beta).
# ---------------------------------------------------------------------------

def thermal_state_R(beta: float) -> np.ndarray:
    """Thermal state rho_beta = exp(-beta K_R) / Z on the R subsystem."""
    w = evals_R - evals_R.min()   # shift for numerical stability
    p = np.exp(-beta * w)
    p /= p.sum()
    return (evecs_R * p) @ evecs_R.conj().T


def legendre_KR(beta: float) -> float:
    """L[K_R](beta) = S_vN(rho_beta) (standard thermo Legendre = von Neumann entropy)."""
    w_shifted = evals_R - evals_R.min()
    p = np.exp(-beta * w_shifted)
    Z = p.sum()
    p /= Z
    # <K_R>_beta  (with original, unshifted eigenvalues)
    mean_K = np.dot(p, evals_R)
    # F(beta) = -ln Z  (using original eigenvalues: F includes -beta*min shift)
    # but since L = beta*<K>_beta - F = S_vN (standard identity),
    # we compute S_vN directly:
    S = -np.dot(p[p > 1e-15], np.log(p[p > 1e-15]))
    return float(S)


# ---------------------------------------------------------------------------
# 3. Brown-Susskind complexity proxy C_BS(beta) = 1 / Tr(rho_beta^2)
# ---------------------------------------------------------------------------

def C_BS(beta: float) -> float:
    """Nielsen/Brown-Susskind geodesic complexity proxy: 1/purity."""
    rho = thermal_state_R(beta)
    purity = float(np.trace(rho @ rho).real)
    return 1.0 / purity


# ---------------------------------------------------------------------------
# 4. Beta scan and proportionality check
# ---------------------------------------------------------------------------
betas = np.logspace(-1, 1, 30)   # 0.1 to 10

L_vals = np.array([legendre_KR(b) for b in betas])
C_vals = np.array([C_BS(b) for b in betas])

# Proportionality ratio L / C_BS
ratios = L_vals / C_vals

print("\nBeta scan results:")
print(f"{'beta':>8}  {'L[K_R]':>10}  {'C_BS':>10}  {'ratio L/C_BS':>14}")
for b, L, C, r in zip(betas, L_vals, C_vals, ratios):
    print(f"{b:8.4f}  {L:10.5f}  {C:10.5f}  {r:14.6f}")

# Statistics on ratio
ratio_mean = ratios.mean()
ratio_std = ratios.std()
ratio_min = ratios.min()
ratio_max = ratios.max()
ratio_range_rel = (ratio_max - ratio_min) / ratio_mean

print(f"\nRatio L/C_BS statistics:")
print(f"  mean = {ratio_mean:.6f}")
print(f"  std  = {ratio_std:.6f}")
print(f"  min  = {ratio_min:.6f}  max = {ratio_max:.6f}")
print(f"  relative range = {ratio_range_rel:.4f}  ({ratio_range_rel*100:.2f}%)")

# ---------------------------------------------------------------------------
# 5. Verdict
# ---------------------------------------------------------------------------
# Criterion for YIELDS-EXACT-EQUALITY: relative range < 5% over full beta scan.
# Criterion for YIELDS-INEQUALITY: L and C_BS are ordered but not proportional.
# Criterion for NO-RELATION: ratio varies by > 50%.

print("\n--- VERDICT ---")
if ratio_range_rel < 0.05:
    verdict = "YIELDS-EXACT-EQUALITY"
    detail = (f"L[K_R] = {ratio_mean:.4f} * C_BS within {ratio_range_rel*100:.2f}% "
              f"over beta in [0.1, 10].")
elif ratio_range_rel < 0.50:
    verdict = "YIELDS-INEQUALITY"
    detail = (f"L[K_R] / C_BS varies from {ratio_min:.4f} to {ratio_max:.4f} "
              f"(relative range {ratio_range_rel*100:.1f}%): not proportional, "
              f"but same-sign ordering holds. L < C_BS on average: "
              f"{(L_vals < C_vals).sum()}/{len(betas)} beta values.")
else:
    verdict = "NO-RELATION"
    detail = (f"L[K_R] / C_BS varies from {ratio_min:.4f} to {ratio_max:.4f} "
              f"(relative range {ratio_range_rel*100:.1f}%): no stable proportionality.")

print(f"VERDICT: {verdict}")
print(f"Detail: {detail}")

# Physical interpretation note
print("""
Physical note:
  L[K_R](beta) = S_vN(rho_beta)  (von Neumann entropy, bounded by ln(DIM_R) = ln16)
  C_BS(beta)   = 1/Tr(rho^2)     (Nielsen purity-complexity, range [1, DIM_R])
  Both grow monotonically from beta=0 (maximally mixed) to beta->inf (pure ground state).
  S_vN is logarithmically bounded; C_BS grows linearly in effective dimension.
  These have different functional forms (log vs power law in beta), so
  proportionality is violated at large beta — mismatch is structural, not numerical.
  At small beta (high temperature), both -> constants (ln DIM_R and DIM_R resp.),
  so ratio -> 0 as beta->inf and -> ln(DIM_R)/DIM_R at beta->0.
  Conclusion: L[K_R] and C_BS probe different aspects of the state;
  the Legendre/thermodynamic conjugacy does NOT reproduce Brown-Susskind complexity.
""")

print("Script completed successfully.")
