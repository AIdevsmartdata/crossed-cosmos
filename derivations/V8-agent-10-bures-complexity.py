#!/usr/bin/env python3
"""
V8-agent-10-bures-complexity.py
================================

Analogy: Bures-Uhlmann geodesic distance between states
         ↔ Brown-Susskind / Nielsen geometric complexity C_k under modular flow.

Question: does d_B(ρ_R(0), ρ_R(τ)) equal C_k to leading order (linear)?

Setup:
  - 3+3 qubit system (reduced from 4+4 for dim feasibility)
  - XXZ modular Hamiltonian on full system
  - ρ_R(0) = Tr_{R'}[ρ_β] (thermal state reduced to subsystem R)
  - ρ_R(τ) = Tr_{R'}[U(τ) ρ_β U(τ)†] where U(τ) = exp(-i K τ)
  - d_B = Bures distance (via scipy.linalg sqrtm)
  - C_BS = Nielsen complexity proxy: 1/Tr(ρ_R(τ)²)  [purity inverse]
    (follows same proxy used in V8-agent-02, Nielsen geometric complexity)

Verdict: LINEAR-EQUIVALENCE / POWER-LAW-NONLINEAR / NO-SIMPLE-RELATION
"""

from __future__ import annotations

import numpy as np
from scipy.linalg import sqrtm, expm
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
import warnings

warnings.filterwarnings("ignore")

rng = np.random.default_rng(seed=20260422)

# ---------------------------------------------------------------------------
# 1. Build 3+3 XXZ modular Hamiltonian
# ---------------------------------------------------------------------------
N_R = 3
N_Rp = 3
N = N_R + N_Rp
DIM = 2 ** N          # 64
DIM_R = 2 ** N_R      # 8
DIM_Rp = 2 ** N_Rp    # 8

I2 = np.eye(2, dtype=complex)
SZ = np.array([[1.0, 0.0], [0.0, -1.0]], dtype=complex)
SX = np.array([[0.0, 1.0], [1.0, 0.0]], dtype=complex)
SY = np.array([[0.0, -1j], [1j, 0.0]], dtype=complex)


def kron_site(op: np.ndarray, site: int, n: int) -> np.ndarray:
    ops = [I2] * n
    ops[site] = op
    out = ops[0]
    for o in ops[1:]:
        out = np.kron(out, o)
    return out


def build_xxz(n: int, delta: float = 1.5) -> np.ndarray:
    """XXZ Hamiltonian with PBC."""
    H = np.zeros((2**n, 2**n), dtype=complex)
    for i in range(n):
        j = (i + 1) % n
        H += kron_site(SX, i, n) @ kron_site(SX, j, n)
        H += kron_site(SY, i, n) @ kron_site(SY, j, n)
        H += delta * (kron_site(SZ, i, n) @ kron_site(SZ, j, n))
    return H


H_full = build_xxz(N, delta=1.5)

# ---------------------------------------------------------------------------
# 2. Thermal state at β=1 → reduce to R
# ---------------------------------------------------------------------------
beta = 1.0
rho_beta = expm(-beta * H_full)
rho_beta /= np.trace(rho_beta)

# Partial trace over R' (sites N_R..N-1 = last N_Rp sites)
# Reshape: (DIM_R, DIM_Rp, DIM_R, DIM_Rp) then trace over Rp indices
rho_full = rho_beta.reshape(DIM_R, DIM_Rp, DIM_R, DIM_Rp)
rho_R0 = np.einsum("iaja->ij", rho_full)  # shape (DIM_R, DIM_R)
rho_R0 /= np.trace(rho_R0)

# ---------------------------------------------------------------------------
# 3. Modular flow evolution
#    The modular Hamiltonian K = -ln(ρ_β) commutes with ρ_β, so it cannot
#    change ρ_β itself. The standard physics interpretation is:
#      - Evolve the *full* state under a *perturbed* Hamiltonian H' = H_full + V
#        where V is a boundary perturbation coupling R to R'.
#      - This mimics the physical scenario: the modular flow acts on observables,
#        and a boundary perturbation creates non-trivial evolution of ρ_R(τ).
#
#    Concretely: H_pert = H_full + λ * V_boundary
#    where V_boundary couples the edge sites of R and R'.
#    This is the correct setup for Brown-Susskind complexity growth:
#    the system evolves under H_full (or H_pert) and we measure the
#    complexity/Bures distance of the reduced state.
# ---------------------------------------------------------------------------

# Perturbation: coupling between R boundary site (N_R-1) and R' site (0=N_R)
lam = 0.3
V_boundary = np.zeros((DIM, DIM), dtype=complex)
# SX_{N_R-1} ⊗ SX_{N_R} coupling
for op in [SX, SY, SZ]:
    V_boundary += (kron_site(op, N_R - 1, N) @ kron_site(op, N_R, N))
H_pert = H_full + lam * V_boundary

print("H_pert built. DIM =", DIM)
print("H_full operator norm:", np.linalg.norm(H_full, ord=2))
print("V_boundary norm:", lam * np.linalg.norm(V_boundary, ord=2))


def evolved_rho_R(tau: float) -> np.ndarray:
    """Evolve full thermal state under H_pert, then trace out R'."""
    U = expm(-1j * H_pert * tau)
    rho_tau = U @ rho_beta @ U.conj().T
    rho_tau_r = rho_tau.reshape(DIM_R, DIM_Rp, DIM_R, DIM_Rp)
    rho_R_tau = np.einsum("iaja->ij", rho_tau_r)
    rho_R_tau = 0.5 * (rho_R_tau + rho_R_tau.conj().T)
    rho_R_tau /= np.trace(rho_R_tau)
    return rho_R_tau


# ---------------------------------------------------------------------------
# 4. Bures distance
# ---------------------------------------------------------------------------

def bures_distance(rho: np.ndarray, sigma: np.ndarray) -> float:
    """
    d_B(ρ, σ) = sqrt(2 - 2 * sqrt(F(ρ,σ)))
    where F(ρ,σ) = (Tr sqrt(sqrt(ρ) σ sqrt(ρ)))^2 is quantum fidelity.
    """
    # sqrt(ρ)
    sqrt_rho = sqrtm(rho)
    # M = sqrt(ρ) σ sqrt(ρ)
    M = sqrt_rho @ sigma @ sqrt_rho
    # fidelity = (Tr sqrt(M))^2
    sqrt_M = sqrtm(M)
    fidelity = np.real(np.trace(sqrt_M)) ** 2
    fidelity = np.clip(fidelity, 0.0, 1.0)
    db = np.sqrt(max(0.0, 2.0 - 2.0 * np.sqrt(fidelity)))
    return float(db)


# ---------------------------------------------------------------------------
# 5. Brown-Susskind complexity proxy: C_BS(τ) = 1/Tr(ρ_R(τ)²)
# ---------------------------------------------------------------------------

def complexity_bs(rho: np.ndarray) -> float:
    """Nielsen/Brown-Susskind proxy: inverse purity."""
    purity = np.real(np.trace(rho @ rho))
    return 1.0 / purity


# ---------------------------------------------------------------------------
# 6. Scan τ values
# ---------------------------------------------------------------------------
tau_values = np.linspace(0.0, 3.0, 60)

d_B_vals = []
C_BS_vals = []
C_BS_0 = complexity_bs(rho_R0)

for tau in tau_values:
    rho_tau = evolved_rho_R(tau)
    db = bures_distance(rho_R0, rho_tau)
    cbs = complexity_bs(rho_tau)
    d_B_vals.append(db)
    C_BS_vals.append(cbs)

d_B_vals = np.array(d_B_vals)
C_BS_vals = np.array(C_BS_vals)

# Complexity change ΔC_BS = C_BS(τ) - C_BS(0)
delta_C = C_BS_vals - C_BS_0

print(f"C_BS(0)  = {C_BS_0:.6f}")
print(f"C_BS max = {C_BS_vals.max():.6f}")
print(f"d_B max  = {d_B_vals.max():.6f}")

# ---------------------------------------------------------------------------
# 7. Fit d_B = A * (ΔC_BS)^β  over non-trivial range
# ---------------------------------------------------------------------------
# Use only τ > 0 and ΔC_BS > 1e-6
mask = (tau_values > 0.05) & (delta_C > 1e-6) & (d_B_vals > 1e-6)
x_fit = delta_C[mask]
y_fit = d_B_vals[mask]

def power_law(x, A, beta_exp):
    return A * x ** beta_exp

popt, pcov = curve_fit(power_law, x_fit, y_fit,
                       p0=[1.0, 1.0],
                       bounds=([0, 0.1], [1e3, 5.0]),
                       maxfev=10000)
A_fit, beta_fit = popt
perr = np.sqrt(np.diag(pcov))

print(f"\nFit d_B = A * (ΔC_BS)^β:")
print(f"  A    = {A_fit:.6f} ± {perr[0]:.6f}")
print(f"  β    = {beta_fit:.6f} ± {perr[1]:.6f}")

# Linear residuals (β=1 forced)
def linear(x, A):
    return A * x

popt_lin, _ = curve_fit(linear, x_fit, y_fit, p0=[1.0])
A_lin = popt_lin[0]
resid_power = np.sum((y_fit - power_law(x_fit, A_fit, beta_fit))**2)
resid_lin   = np.sum((y_fit - linear(x_fit, A_lin))**2)
r2_power = 1.0 - resid_power / np.sum((y_fit - y_fit.mean())**2)
r2_lin   = 1.0 - resid_lin   / np.sum((y_fit - y_fit.mean())**2)

print(f"\n  R² (power-law fit): {r2_power:.6f}")
print(f"  R² (linear β=1):    {r2_lin:.6f}")

# Verdict
beta_lo = beta_fit - 2 * perr[1]
beta_hi = beta_fit + 2 * perr[1]
if beta_lo <= 1.0 <= beta_hi and r2_lin >= 0.97:
    verdict = "LINEAR-EQUIVALENCE"
elif r2_power >= 0.95:
    verdict = "POWER-LAW-NONLINEAR"
else:
    verdict = "NO-SIMPLE-RELATION"

print(f"\nVERDICT: {verdict}")
print(f"  β = {beta_fit:.3f} ± {perr[1]:.3f}  (2σ interval [{beta_lo:.3f}, {beta_hi:.3f}])")

# ---------------------------------------------------------------------------
# 8. Plot
# ---------------------------------------------------------------------------
fig, axes = plt.subplots(1, 2, figsize=(12, 5))

ax1 = axes[0]
ax1.plot(tau_values, d_B_vals, "b-o", ms=3, label=r"$d_B(\rho_R(0),\rho_R(\tau))$")
ax1_r = ax1.twinx()
ax1_r.plot(tau_values, delta_C, "r--s", ms=3, label=r"$\Delta C_{BS}(\tau)$")
ax1.set_xlabel(r"$\tau$")
ax1.set_ylabel(r"Bures distance $d_B$", color="blue")
ax1_r.set_ylabel(r"$\Delta C_{BS} = C_{BS}(\tau) - C_{BS}(0)$", color="red")
ax1.set_title("Bures distance & complexity vs. modular time τ\n(3+3 qubit XXZ)")
lines1, labels1 = ax1.get_legend_handles_labels()
lines2, labels2 = ax1_r.get_legend_handles_labels()
ax1.legend(lines1 + lines2, labels1 + labels2, loc="upper left", fontsize=8)

ax2 = axes[1]
x_plot = np.linspace(x_fit.min(), x_fit.max(), 200)
ax2.scatter(x_fit, y_fit, c="blue", s=15, label="data", zorder=3)
ax2.plot(x_plot, power_law(x_plot, A_fit, beta_fit), "r-",
         label=rf"power-law: $A\cdot\Delta C^{{\beta}}$, $\beta={beta_fit:.3f}$")
ax2.plot(x_plot, linear(x_plot, A_lin), "g--",
         label=rf"linear ($\beta=1$), $R^2={r2_lin:.4f}$")
ax2.set_xlabel(r"$\Delta C_{BS}(\tau)$")
ax2.set_ylabel(r"$d_B(\rho_R(0), \rho_R(\tau))$")
ax2.set_title(f"Bures ↔ C_BS  —  VERDICT: {verdict}\n"
              rf"$\beta={beta_fit:.3f}\pm{perr[1]:.3f}$, $R^2_{{PL}}={r2_power:.4f}$, $R^2_{{lin}}={r2_lin:.4f}$")
ax2.legend(fontsize=8)

plt.tight_layout()
out_png = "/home/remondiere/crossed-cosmos/derivations/V8-agent-10-bures-complexity.png"
plt.savefig(out_png, dpi=150)
print(f"\nPlot saved → {out_png}")

# ---------------------------------------------------------------------------
# 9. Summary table
# ---------------------------------------------------------------------------
print("\n--- Summary table (τ, d_B, ΔC_BS) ---")
for i in range(0, len(tau_values), 6):
    print(f"  τ={tau_values[i]:.2f}  d_B={d_B_vals[i]:.5f}  ΔC_BS={delta_C[i]:.5f}")
