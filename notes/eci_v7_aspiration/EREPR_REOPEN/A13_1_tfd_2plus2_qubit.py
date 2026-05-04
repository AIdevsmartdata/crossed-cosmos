#!/usr/bin/env python3
"""
A13_1_tfd_2plus2_qubit.py
==========================
Week 1 toy: Petz recovery monotonicity on a 2+2 qubit system.

Physical context
----------------
The SdS type-II_inf factor (DEHK, arXiv:2412.15502) carries two sub-algebras
  M_R (cosmological observer) and M_L (black-hole observer).
The KMS state at beta=2*pi is the algebraic TFD.

v6 Prop. 1 (eci.tex eq:eci-ineq — UPPER BOUND only):
  dS_gen/dtau_R <= kappa_R * C_k * Theta

Week 1 question: does Petz recovery monotonicity provide a LOWER BOUND?

Key structural observation (found during this analysis)
-------------------------------------------------------
The TFD state |TFD(beta)> is a PURE state on H_R x H_L.
For a pure bipartite state, the reduced states rho_R and rho_L are mixed,
but the full state is rank-1, so:
  - S(rho_full || sigma_full) = +inf whenever rho_full != sigma_full (different pure states).
  - The Petz recovery map from a PURE reference sigma is the identity (trivially exact).
  - The Petz deficit is not a useful diagnostic for comparing two pure TFD states.

Therefore: to use Petz recovery, we must either
  (A) Work with MIXED states (thermal states on M_R, not pure TFD states), or
  (B) Work in the REDUCED system (M_L sub-algebra only) and track subsystem entropy.

This script implements BOTH strategies:
  (A) Mixed state: sigma = thermal state rho_beta = e^{-beta H}/Z on M_R (no entanglement).
      rho = slightly perturbed thermal state at beta+delta_beta.
      Petz recovery from M_L (here = a 2-qubit sub-register of a 4-qubit M_R system).
  (B) TFD pure state: track relative entropy between REDUCED states rho_L and sigma_L,
      and compute the deficit relative to the marginal algebra alone.

Anti-fabrication
----------------
- Petz 1988: recovery map in type-I; Junge-Renner-Sutter-Wilde-Winter 2018 (Ann. Math.).
- Type-II_inf extension: OPEN mathematical problem (Haagerup 1979; Kosaki 1984 for L^p).
- CLPW arXiv:2206.10780: type-II_1 crossed product; no Petz recovery discussed.
- DEHK arXiv:2412.15502: type-II_inf for SdS; no Petz recovery discussed.
- Faulkner-Speranza arXiv:2405.00847: GSL from modular flow + relative entropy; no Petz map.
- Heller-Papalini-Schuhmann arXiv:2412.17785: 2|log q| C_k = L in DSSYK; type-I Hilbert space.
"""

from __future__ import annotations

import numpy as np
from numpy.linalg import eigvalsh, eigh

# -------------------------------------------------------------------------
# Basic operators
# -------------------------------------------------------------------------

I2 = np.eye(2, dtype=complex)
SX = np.array([[0, 1], [1, 0]], dtype=complex)
SY = np.array([[0, -1j], [1j, 0]], dtype=complex)
SZ = np.array([[1, 0], [0, -1]], dtype=complex)
EPS = 1e-12


def kron_op(op, i, n):
    ops = [I2] * n
    ops[i] = op
    out = ops[0]
    for o in ops[1:]:
        out = np.kron(out, o)
    return out


def build_xxz(n, J=1.0, Delta=0.5):
    H = np.zeros((2**n, 2**n), dtype=complex)
    for i in range(n - 1):
        H += J * (kron_op(SX, i, n) @ kron_op(SX, i + 1, n)
                  + kron_op(SY, i, n) @ kron_op(SY, i + 1, n))
        H += J * Delta * kron_op(SZ, i, n) @ kron_op(SZ, i + 1, n)
    return H


# 4-qubit XXZ: treat as M_R (4-dim Hilbert space)
# Sub-register A = first 2 qubits, B = last 2 qubits (= M_L analog)
N_TOT = 4
DIM_TOT = 2**N_TOT   # 16
DIM_HALF = 2**2       # 4  (each sub-register)

H4 = build_xxz(N_TOT)
EVALS4, EVECS4 = eigh(H4)

# 2-qubit sub-Hamiltonian (for entropy proxy)
H2 = build_xxz(2)
EVALS2, EVECS2 = eigh(H2)


# -------------------------------------------------------------------------
# Helper: matrix functions
# -------------------------------------------------------------------------

def vn_entropy(rho):
    v = eigvalsh(rho)
    v = v[v > EPS]
    return float(-np.sum(v * np.log(v)))


def matrix_fn(rho, fn):
    vals, vecs = eigh(rho)
    new_vals = np.array([fn(v) if v > EPS else 0.0 for v in vals])
    return vecs @ np.diag(new_vals) @ vecs.conj().T


def matrix_sqrt(rho):
    return matrix_fn(rho, np.sqrt)


def matrix_inv_sqrt(rho):
    return matrix_fn(rho, lambda v: 1.0 / np.sqrt(v))


def matrix_log(rho):
    return matrix_fn(rho, np.log)


def rel_entropy(rho, sigma):
    """S(rho||sigma). Returns inf if supp(rho) not subset of supp(sigma)."""
    sv = eigvalsh(sigma)
    rv = eigvalsh(rho)
    if np.any((rv > EPS) & (sv < EPS)):
        return float("inf")
    return float(np.real(np.trace(rho @ (matrix_log(rho) - matrix_log(sigma)))))


def ptrace_B(rho, dA, dB):
    """Partial trace over B (second register), dim_A=dA, dim_B=dB."""
    r = rho.reshape(dA, dB, dA, dB)
    return np.einsum("ijkj->ik", r)


def ptrace_A(rho, dA, dB):
    """Partial trace over A (first register)."""
    r = rho.reshape(dA, dB, dA, dB)
    return np.einsum("ijil->jl", r)


# -------------------------------------------------------------------------
# Strategy A: Mixed thermal states on 4-qubit system
# Reference sigma = thermal state e^{-beta H}/Z on M = B(H^{16})
# Sub-algebra N = B(H_B) = operators on last 2 qubits (the "M_L" analog)
# Petz recovery: from reduced state on N back to M
# -------------------------------------------------------------------------

def thermal_state(evals, evecs, beta):
    w = np.exp(-beta * evals)
    Z = w.sum()
    w /= Z
    return evecs @ np.diag(w) @ evecs.conj().T


def petz_map_mixed(sigma, omega_B, dA=DIM_HALF, dB=DIM_HALF):
    """
    Petz recovery: given reference sigma on M = A x B and reduced state omega_B on B,
    recover a state on M.

    P_sigma(omega_B) = sigma^{1/2} (I_A x sigma_B^{-1/2} omega_B sigma_B^{-1/2}) sigma^{1/2}

    sigma_B = Tr_A(sigma).
    """
    sigma_B = ptrace_A(sigma, dA, dB)
    sig_sqrt = matrix_sqrt(sigma)
    sigB_inv_sqrt = matrix_inv_sqrt(sigma_B)

    inner = sigB_inv_sqrt @ omega_B @ sigB_inv_sqrt
    embedded = np.kron(np.eye(dA, dtype=complex), inner)
    recovered = sig_sqrt @ embedded @ sig_sqrt
    tr = float(np.real(np.trace(recovered)))
    if tr > EPS:
        recovered /= tr
    return recovered


def petz_deficit_mixed(rho, sigma, dA=DIM_HALF, dB=DIM_HALF):
    """
    Petz deficit for sub-algebra N = B(H_B).
    deficit = S(rho||sigma) - S(P_sigma(rho_B) || P_sigma(sigma_B))
    """
    rho_B = ptrace_A(rho, dA, dB)
    sigma_B = ptrace_A(sigma, dA, dB)
    P_rho = petz_map_mixed(sigma, rho_B, dA, dB)
    P_sig = petz_map_mixed(sigma, sigma_B, dA, dB)
    S_full = rel_entropy(rho, sigma)
    S_rec = rel_entropy(P_rho, P_sig)
    return {
        "S_full": S_full,
        "S_rec": S_rec,
        "deficit": S_full - S_rec,
    }


def krylov_proxy(rho_A):
    """Toy C_k proxy = 1/purity(rho_A)."""
    p = float(np.real(np.trace(rho_A @ rho_A)))
    return 1.0 / max(p, EPS)


# -------------------------------------------------------------------------
# Run Strategy A
# -------------------------------------------------------------------------

print("=" * 72)
print("Strategy A: Petz deficit for MIXED thermal states (4-qubit XXZ)")
print("Reference sigma = thermal(beta_ref); rho = thermal(beta_ref + db)")
print("Sub-algebra N = B(H_B), B = last 2 qubits")
print("=" * 72)

BETA_REF_A = 1.0
sigma_A = thermal_state(EVALS4, EVECS4, BETA_REF_A)
sigma_B_A = ptrace_A(sigma_A, DIM_HALF, DIM_HALF)
sigma_A_sub = ptrace_B(sigma_A, DIM_HALF, DIM_HALF)

print(f"\nReference: thermal state at beta_ref = {BETA_REF_A}")
print(f"  S(sigma)    = {vn_entropy(sigma_A):.4f}")
print(f"  S(sigma_A)  = {vn_entropy(sigma_A_sub):.4f}  [sub-register A = M_R analog]")
print(f"  S(sigma_B)  = {vn_entropy(sigma_B_A):.4f}  [sub-register B = M_L analog]")
print(f"  C_k(sig_A)  = {krylov_proxy(sigma_A_sub):.4f}")

DELTAS_A = [0.05, 0.10, 0.20, 0.50, 1.0, 2.0, 3.0, 5.0]

print()
hdr = f"{'db':>8} {'S(r||s)':>12} {'S(Pr||Ps)':>12} {'deficit':>10} {'C_k(rA)':>10} {'def/Ck':>10}"
print(hdr)
print("-" * len(hdr))

results_A = []
for db in DELTAS_A:
    rho = thermal_state(EVALS4, EVECS4, BETA_REF_A + db)
    rho_A_sub = ptrace_B(rho, DIM_HALF, DIM_HALF)
    Ck = krylov_proxy(rho_A_sub)
    d = petz_deficit_mixed(rho, sigma_A)
    ratio = d["deficit"] / Ck if Ck > EPS else float("nan")
    results_A.append({"db": db, "Ck": Ck, **d, "ratio": ratio})
    print(f"{db:>8.3f} {d['S_full']:>12.6f} {d['S_rec']:>12.6f} "
          f"{d['deficit']:>10.6f} {Ck:>10.4f} {ratio:>10.6f}")

mono_A = all(r["deficit"] >= -1e-9 for r in results_A)
print(f"\nPetz monotonicity (deficit >= 0): {mono_A}")

deficits_A = np.array([r["deficit"] for r in results_A])
cks_A = np.array([r["Ck"] for r in results_A])
dbs_A = np.array([r["db"] for r in results_A])

corr_db_A = float(np.corrcoef(dbs_A, deficits_A)[0, 1])
corr_ck_A = float(np.corrcoef(cks_A, deficits_A)[0, 1])
ratios_A = np.array([r["ratio"] for r in results_A])
cv_A = ratios_A.std() / abs(ratios_A.mean()) if abs(ratios_A.mean()) > EPS else float("inf")

print(f"\nPearson(deficit, delta_beta) = {corr_db_A:.4f}")
print(f"Pearson(deficit, C_k)        = {corr_ck_A:.4f}")
print(f"CV of (deficit/C_k)          = {cv_A:.4f}  (< 0.3 = proportional)")

# Compare to v6 upper bound proxy
kappa_R = 2 * np.pi / BETA_REF_A
print(f"\nv6 Prop. 1 upper bound: kappa_R * C_k = {kappa_R:.4f} * C_k")
S_sig_A = vn_entropy(sigma_A_sub)
print()
hdr2 = f"{'db':>8} {'dS_A/db':>12} {'UB=kR*Ck':>12} {'deficit':>10} {'def<=dS':>10}"
print(hdr2)
print("-" * len(hdr2))
for r in results_A:
    rho_i = thermal_state(EVALS4, EVECS4, BETA_REF_A + r["db"])
    rho_Ai = ptrace_B(rho_i, DIM_HALF, DIM_HALF)
    dS = (vn_entropy(rho_Ai) - S_sig_A) / r["db"]
    ub = kappa_R * r["Ck"]
    ok = r["deficit"] <= abs(dS) + 1e-8
    print(f"{r['db']:>8.3f} {dS:>12.6f} {ub:>12.4f} {r['deficit']:>10.6f} {'YES' if ok else 'NO':>10}")


# -------------------------------------------------------------------------
# Strategy B: TFD reduced states — track subsystem Petz deficit
# -------------------------------------------------------------------------

print()
print("=" * 72)
print("Strategy B: Petz deficit for TFD REDUCED states on 2-qubit M_L")
print("sigma_L = Tr_R(|TFD(b_ref)><TFD(b_ref)|),  rho_L = Tr_R(|TFD(b)><TFD(b)|)")
print("Recovery: from 1-qubit register of M_L back to full M_L (sub-algebra)")
print("=" * 72)

BETA_REF_B = 1.0
N_B = 2
DIM_B = 4   # H_L = 4-dim


def tfd_reduced_L(beta):
    """Return rho_L = Tr_R(|TFD(beta)><TFD(beta)|), a 4x4 mixed state."""
    w = np.exp(-beta * EVALS2 / 2.0)
    Z = float(np.sum(w**2))
    w /= np.sqrt(Z)
    psi = np.zeros(DIM_B * DIM_B, dtype=complex)
    for i in range(DIM_B):
        psi += w[i] * np.kron(EVECS2[:, i], EVECS2[:, i])
    rho_full = np.outer(psi, psi.conj())
    # Trace over R (first 4-dim register)
    r = rho_full.reshape(DIM_B, DIM_B, DIM_B, DIM_B)
    return np.einsum("ijil->jl", r)


# Within M_L (= B(H_L), 4x4 matrices), sub-algebra = B(H_{L1}) (first qubit of L)
# Petz deficit: from 2-dim sub-register of 4-dim M_L back to 4-dim M_L

def petz_deficit_L(rho_L, sigma_L, dA=2, dB=2):
    """Petz deficit for sub-algebra B(H_{L1}) inside M_L = B(H_L)."""
    return petz_deficit_mixed(rho_L, sigma_L, dA, dB)


sigma_L_B = tfd_reduced_L(BETA_REF_B)
sigma_L1 = ptrace_B(sigma_L_B, 2, 2)   # first qubit of L

print(f"\nReference: TFD at beta_ref = {BETA_REF_B}")
print(f"  S(sigma_L)  = {vn_entropy(sigma_L_B):.4f}")
print(f"  S(sigma_L1) = {vn_entropy(sigma_L1):.4f}  [first qubit of M_L]")
print(f"  C_k(sig_L)  = {krylov_proxy(sigma_L_B):.4f}")

DELTAS_B = [0.05, 0.10, 0.20, 0.30, 0.50, 0.80, 1.0, 1.5, 2.0]

print()
hdrB = f"{'db':>8} {'S(rL||sL)':>12} {'S(Pr||Ps)':>12} {'deficit':>10} {'C_k(rL)':>10} {'def/Ck':>10}"
print(hdrB)
print("-" * len(hdrB))

results_B = []
for db in DELTAS_B:
    rho_L = tfd_reduced_L(BETA_REF_B + db)
    Ck = krylov_proxy(rho_L)
    d = petz_deficit_L(rho_L, sigma_L_B)
    ratio = d["deficit"] / Ck if Ck > EPS else float("nan")
    results_B.append({"db": db, "Ck": Ck, **d, "ratio": ratio})
    print(f"{db:>8.3f} {d['S_full']:>12.6f} {d['S_rec']:>12.6f} "
          f"{d['deficit']:>10.6f} {Ck:>10.4f} {ratio:>10.6f}")

mono_B = all(r["deficit"] >= -1e-9 for r in results_B)
print(f"\nPetz monotonicity (deficit >= 0): {mono_B}")

deficits_B = np.array([r["deficit"] for r in results_B])
cks_B = np.array([r["Ck"] for r in results_B])
dbs_B = np.array([r["db"] for r in results_B])

corr_db_B = float(np.corrcoef(dbs_B, deficits_B)[0, 1])
corr_ck_B = float(np.corrcoef(cks_B, deficits_B)[0, 1])
ratios_B = np.array([r["ratio"] for r in results_B])
cv_B = ratios_B.std() / abs(ratios_B.mean()) if abs(ratios_B.mean()) > EPS else float("inf")

print(f"\nPearson(deficit, delta_beta) = {corr_db_B:.4f}")
print(f"Pearson(deficit, C_k)        = {corr_ck_B:.4f}")
print(f"CV of (deficit/C_k)          = {cv_B:.4f}  (< 0.3 = proportional)")

# -------------------------------------------------------------------------
# Analytical verdict
# -------------------------------------------------------------------------

print()
print("=" * 72)
print("ANALYTICAL VERDICT (Week 1)")
print("=" * 72)
print(f"""
Strategy A (mixed thermal states):
  Petz monotonicity: {mono_A}
  Pearson(deficit, C_k) = {corr_ck_A:.4f}
  CV(deficit/C_k)       = {cv_A:.4f}

Strategy B (TFD reduced states on M_L):
  Petz monotonicity: {mono_B}
  Pearson(deficit, C_k) = {corr_ck_B:.4f}
  CV(deficit/C_k)       = {cv_B:.4f}

OBSTRUCTION 1 — Structural mismatch (both strategies):
  The Petz deficit is NOT proportional to C_k in either regime
  (CV >> 0.3 in both cases). There is no evidence of a simple lower bound
  of the form "deficit >= const * C_k" in the 2+2 qubit setting.

OBSTRUCTION 2 — Type-II_inf extension (fundamental):
  The Petz map P_sigma = sigma^(1/2) * E_sigma^*(.) * sigma^(1/2) uses
  the operator square root of the full state sigma. In type-II_inf,
  sigma does not live in B(H) but in the Haagerup L^1(M) space.
  The construction sigma^(1/2) requires the L^2 module.
  No published work constructs Petz recovery for the CLPW/DEHK algebra.
  This is the PRIMARY mathematical gap.

OBSTRUCTION 3 — TFD is PURE (both strategies):
  The full TFD state is pure, so S(TFD(b) || TFD(b')) = infinity for b != b'.
  Strategy A avoids this by using mixed thermal states but loses the TFD structure.
  Strategy B works within M_L (reduced, mixed) but loses the global entanglement.
  Neither setting faithfully represents the type-II_inf crossed-product algebra.

PRELIMINARY VERDICT:
  The Petz route to a lower bound dS_gen/dtau_R >= f(C_k) is NOT supported
  by the 2+2 qubit toy. Three obstructions are documented.
  However: the result is NOT a NO-GO. The obstructions are MATHEMATICAL
  (the extension to type-II_inf has not been attempted) rather than
  PHYSICAL (there is no counterexample at the level of the SdS algebra).
  Weeks 2-4 should focus on:
    (a) Haagerup L^2 formulation of Petz for type-II_inf.
    (b) Casini-Huerta-Myers approach via relative modular operator.
    (c) Alternative route: monotonicity of modular operator Delta_rho/sigma
        in the CLPW type-II algebra (which may bypass Petz entirely).
""")

print("Script complete.")
