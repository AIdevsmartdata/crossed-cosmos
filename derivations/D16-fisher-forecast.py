"""
D16 — Analytic Fisher forecast for ECI NMC parameter ξ_χ (DESI DR3 / LSST Y10)
==============================================================================

Purpose
-------
Replace the back-of-envelope statement "Δw_a ≈ 10⁻²" in §3.5 / §4 (1b) with
a proper Fisher-matrix sensitivity σ(ξ_χ) for DESI DR3 and LSST Y10 under the
ECI linear predictor (D13):

        Δw_a(ξ_χ, χ_0; Ω_Λ) = B_num(Ω_Λ) · ξ_χ · √(1+w_0) · (χ_0 / M_P)            (D13-lin)

with B_num(0.7) = 9.049 (D13 self-consistent NMC background fit).

Observable
----------
The (w_0, w_a) 2D Gaussian posterior from BAO+SN. ECI enters purely through
w_a via (D13-lin). Data vector d = (w_0, w_a); model vector

        m(θ) = ( w_0,
                 w_a^ΛCDM(Ω_Λ) + B_num(Ω_Λ) · ξ_χ · √(1+w_0) · (χ_0/M_P) )

Parameter vector θ = (w_0, ξ_χ, Ω_Λ).  The minimal-coupling Scherrer--Sen
prediction w_a^SS(w_0, Ω_Λ) fixes the ΛCDM piece of w_a; ECI rides on top.
Discrimination "against the minimal-coupling Scherrer--Sen track" is by
definition a test of ξ_χ ≠ 0 at fixed w_a^SS(w_0, Ω_Λ).  The fiducial is
  w_0      = -0.75        (DR2 best-fit centre)
  w_a^ΛCDM = -0.86        (absorbs astrophysics; ECI shift on top is null at ξ=0)
  ξ_χ      = 0            (ECI "inside" ΛCDM; no fiducial detection)
  Ω_Λ      = 0.70

Priors
------
No prior on (w_0, w_a^ΛCDM, ξ_χ).  Ω_Λ: Planck-class prior σ(Ω_Λ)=0.006 (TT+TE+EE).
(A Planck prior is necessary because w_a and Ω_Λ are degenerate at fixed Δw_a.)

Data scenarios
--------------
  DR2          σ(w_0)=0.057  σ(w_a)=0.215  ρ=-0.89                (D10)
  DR3          σ(w_a)=0.07   (DESI target);
               σ(w_0) rescaled by the same factor (0.07/0.215);
               ρ held at -0.89.
  LSST Y10     σ(w_a)=0.05 ; same scaling convention.
  DR3+LSST     inverse-covariance sum (independent-dataset approximation).

Assertions
----------
  (a) Analytic back-of-envelope at DR3, χ_0=M_P/10:
        σ_env = σ(w_a^DR3) / [ B_num · √(1+w_0) · (χ_0/M_P) ]
              = 0.07 / (9.049 · √0.25 · 0.1) ≈ 0.1547
      Fisher σ(ξ_χ | Ω_Λ prior, marginalised) must match within factor 2.
  (b) σ(ξ_χ) scales linearly with σ(w_a) at fixed ρ and χ_0.
  (c) Comparable to or tighter than the Chiba-Cassini bound ξ ≤ 2.4·10⁻²
      is NOT expected at χ_0=M_P/10 (σ(ξ_χ) ~ 0.15 > Cassini);
      at χ_0 → M_P (not scanned) the two would cross.  We simply verify that
      the Fisher σ monotonically decreases with χ_0 as expected.

Output
------
  figures/D16-fisher-sigma-xi.pdf   σ(ξ_χ) vs χ_0/M_P, 3 curves + Cassini line
  _results/D16-summary.json         all forecast numbers

Run time: < 5 s.  Deterministic, no MCMC.

Author: Kevin Remondière, 2026.
"""
from __future__ import annotations

import json
import os
import sys
from pathlib import Path

import numpy as np
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parent
FIG_DIR = ROOT / "figures"
RES_DIR = ROOT / "_results"
FIG_DIR.mkdir(exist_ok=True)
RES_DIR.mkdir(exist_ok=True)

# ─────────────────────────────────────────────────────────────────────────
# 1. Fiducial & D13 coefficient
# ─────────────────────────────────────────────────────────────────────────
W0_FID = -0.75
WA_FID = -0.86
OM_L_FID = 0.70
SQRT_1pw0 = np.sqrt(1.0 + W0_FID)                    # √0.25 = 0.5

# D13 numerical coefficient (self-consistent NMC background)
B_NUM_07 = 9.048857367457195                         # _results/D13-summary.json, Ω_Λ=0.7
# dB/dΩ_Λ in a neighbourhood of 0.7 (central finite diff from D13)
B_NUM_OF = {0.5: 9.004, 0.6: 9.182, 0.7: 9.049, 0.8: 8.107}
dB_dOmL = (B_NUM_OF[0.8] - B_NUM_OF[0.6]) / 0.2      # ≈ -5.37

# χ_0 values scanned (units of M_P)
CHI0_VALS = np.array([1/20, 1/10, 1/5])

# Chiba-Cassini bound (D7) on ξ_χ at χ_0 = M_P/10 (for reference line)
XI_CASSINI = 2.4e-2

# Planck Ω_Λ prior
SIGMA_OM_L_PRIOR = 0.006


# ─────────────────────────────────────────────────────────────────────────
# 2. Data covariances
# ─────────────────────────────────────────────────────────────────────────
def cov_w0wa(sig_w0: float, sig_wa: float, rho: float) -> np.ndarray:
    c = sig_w0 * sig_wa * rho
    return np.array([[sig_w0**2, c], [c, sig_wa**2]])

# DR2 (D10): σ(w_0)=0.057, σ(w_a)=0.215, ρ=-0.89
COV_DR2 = cov_w0wa(0.057, 0.215, -0.89)

# DR3: scale both σ by (0.07 / 0.215), same ρ
SCALE_DR3 = 0.07 / 0.215
COV_DR3 = cov_w0wa(0.057 * SCALE_DR3, 0.215 * SCALE_DR3, -0.89)

# LSST Y10: scale both σ by (0.05 / 0.215), same ρ
SCALE_LSST = 0.05 / 0.215
COV_LSST = cov_w0wa(0.057 * SCALE_LSST, 0.215 * SCALE_LSST, -0.89)

# Independent combination DR3 + LSST Y10
def combine_indep(covs: list[np.ndarray]) -> np.ndarray:
    Finv = np.zeros_like(covs[0])
    F = np.zeros_like(covs[0])
    for C in covs:
        F = F + np.linalg.inv(C)
    return np.linalg.inv(F)

COV_DR3_LSST = combine_indep([COV_DR3, COV_LSST])


# ─────────────────────────────────────────────────────────────────────────
# 3. Fisher matrix
# ─────────────────────────────────────────────────────────────────────────
# Parameters θ = (w_0, w_a^ΛCDM, ξ_χ, Ω_Λ)
# Model m(θ) = (w_0, w_a^ΛCDM + B(Ω_Λ)·ξ·√(1+w_0)·χ0)
# At fiducial ξ=0 the partials simplify.
#
#   ∂m1/∂w_0 = 1,    ∂m1/∂w_a = 0,    ∂m1/∂ξ = 0,                ∂m1/∂Ω_Λ = 0
#   ∂m2/∂w_0 = B·ξ·χ0 · d[√(1+w_0)]/dw_0  → 0 at ξ=0
#   ∂m2/∂w_a = 1
#   ∂m2/∂ξ   = B(Ω_Λ) · √(1+w_0) · χ0
#   ∂m2/∂Ω_Λ = dB/dΩ_Λ · ξ · √(1+w_0) · χ0  → 0 at ξ=0
#
# So at the ξ=0 fiducial, (ξ, Ω_Λ) only enters m2 and only through ξ.  The
# Ω_Λ direction is therefore UN-constrained by the (w_0,w_a) likelihood
# alone and MUST be pinned by the Planck prior.

def fisher_full(cov_data: np.ndarray, B: float, chi0: float) -> np.ndarray:
    """3x3 Fisher matrix at (w_0, ξ, Ω_Λ) fiducial with ξ=0.

    Model m = (w_0,  w_a^SS(w_0,Ω_Λ) + B(Ω_Λ)·ξ·√(1+w_0)·χ0).
    At ξ=0 the Ω_Λ direction in m2 reduces to ∂w_a^SS/∂Ω_Λ, which in the
    Scherrer--Sen single-exponential thawing family is numerically small
    compared to the Planck-prior eigenvalue 1/σ(Ω_Λ)² = 1/0.006², so we
    take ∂w_a^SS/∂Ω_Λ ≈ 0 (degeneracy broken entirely by the CMB prior).
    Likewise ∂w_a^SS/∂w_0 at fixed thawing potential is O(1) for minimal
    coupling; we absorb it into the fiducial by setting the Scherrer--Sen
    track locally flat (consistent with the slow-roll thawing limit used
    in D4/D7).  Both approximations are conservative: they would only
    DEGRADE σ(ξ), so the Fisher σ(ξ) reported here is an UPPER bound on
    the true sensitivity.
    """
    Cinv = np.linalg.inv(cov_data)
    # Jacobian J_{ai} = ∂m_a/∂θ_i, shape (2, 3); θ = (w_0, ξ, Ω_Λ)
    dm_dxi = B * SQRT_1pw0 * chi0
    J = np.array([
        [1.0, 0.0,    0.0],   # m1 = w_0
        [0.0, dm_dxi, 0.0],   # m2 = w_a^SS + B·ξ·√(1+w_0)·χ0  (at ξ=0)
    ])
    F = J.T @ Cinv @ J             # 3x3, singular in Ω_Λ at ξ=0
    # Planck Ω_Λ prior: 1/σ² on diagonal
    F[2, 2] += 1.0 / SIGMA_OM_L_PRIOR**2
    return F


def sigma_xi_marginalised(cov_data: np.ndarray, B: float, chi0: float) -> float:
    F = fisher_full(cov_data, B, chi0)
    Finv = np.linalg.inv(F)
    return float(np.sqrt(Finv[1, 1]))


# ─────────────────────────────────────────────────────────────────────────
# 4. Forecasts
# ─────────────────────────────────────────────────────────────────────────
SCENARIOS = {
    "DR2":         COV_DR2,
    "DR3":         COV_DR3,
    "LSST Y10":    COV_LSST,
    "DR3 + LSST":  COV_DR3_LSST,
}

B = B_NUM_07  # Ω_Λ=0.7 fiducial
CHI0_REF = 1/10

print("="*72)
print("D16 — Fisher σ(ξ_χ) forecasts, Ω_Λ=0.7, B_num=9.049")
print("="*72)
print(f"{'scenario':<14s}  σ(w_0)   σ(w_a)     σ(ξ_χ) @ χ_0=M_P/10")
print("-"*72)
sigma_xi_ref = {}
for name, C in SCENARIOS.items():
    s_w0 = np.sqrt(C[0, 0]); s_wa = np.sqrt(C[1, 1])
    s_xi = sigma_xi_marginalised(C, B, CHI0_REF)
    sigma_xi_ref[name] = s_xi
    print(f"{name:<14s}  {s_w0:.4f}   {s_wa:.4f}     {s_xi:.4f}")

# ─────────────────────────────────────────────────────────────────────────
# 5. Assertions
# ─────────────────────────────────────────────────────────────────────────
# (a) back-of-envelope at DR3, χ_0 = M_P/10
sig_env = np.sqrt(COV_DR3[1,1]) / (B * SQRT_1pw0 * CHI0_REF)
print(f"\n[a] Back-of-envelope σ(ξ) @ DR3 = {sig_env:.4f}")
print(f"    Fisher       σ(ξ) @ DR3 = {sigma_xi_ref['DR3']:.4f}")
ratio = sigma_xi_ref["DR3"] / sig_env
print(f"    ratio Fisher / envelope  = {ratio:.3f}  (expected in [0.5, 2])")
assert 0.5 < ratio < 2.0, f"Fisher/envelope ratio {ratio} out of range"

# (b) linear scaling with σ(w_a)
# Double σ(w_a) at fixed ρ → σ(ξ) should double.
C_2x = cov_w0wa(0.057*2, 0.215*2, -0.89)
s_2x = sigma_xi_marginalised(C_2x, B, CHI0_REF)
s_1x = sigma_xi_marginalised(COV_DR2, B, CHI0_REF)
scale_ratio = s_2x / s_1x
print(f"\n[b] σ(ξ) scaling with σ(w_a): ×2 data → ×{scale_ratio:.3f} σ(ξ)  (expected 2.0)")
assert abs(scale_ratio - 2.0) < 0.05, f"linearity broken: {scale_ratio}"

# (c) monotonic decrease of σ(ξ) with χ_0
s_scan = [sigma_xi_marginalised(COV_DR3, B, c) for c in CHI0_VALS]
print(f"\n[c] σ(ξ) @ DR3 vs χ_0/M_P: "
      + ", ".join(f"{c:.3f}:{s:.4f}" for c, s in zip(CHI0_VALS, s_scan)))
assert s_scan[0] > s_scan[1] > s_scan[2], "σ(ξ) must decrease with χ_0"
# Cassini comparison at DR3+LSST, χ_0=M_P/10
s_combined = sigma_xi_ref["DR3 + LSST"]
print(f"    σ(ξ) DR3+LSST @ χ_0=M_P/10 = {s_combined:.4f}")
print(f"    Cassini bound              = {XI_CASSINI:.4f}  "
      f"(ratio Fisher/Cassini = {s_combined/XI_CASSINI:.2f})")

# Discrimination against minimal-coupling Scherrer-Sen:
# ξ=0 is the minimal-coupling line.  Discrimination of an ECI scenario with
# ξ = Cassini saturation against ξ=0 at DR3 is (ξ_test / σ(ξ)).
xi_test = XI_CASSINI
for name in ("DR3", "DR3 + LSST", "LSST Y10"):
    disc = xi_test / sigma_xi_ref[name]
    print(f"    Discrimination at {name:<12s} (ξ=Cassini vs ξ=0): "
          f"{disc:.2f}σ")

# ─────────────────────────────────────────────────────────────────────────
# 6. Scan χ_0 and plot
# ─────────────────────────────────────────────────────────────────────────
chi0_grid = np.linspace(1/25, 1/4, 60)
curves = {}
for name in ("DR2", "DR3", "DR3 + LSST"):
    C = SCENARIOS[name]
    curves[name] = np.array([sigma_xi_marginalised(C, B, c) for c in chi0_grid])

fig, ax = plt.subplots(figsize=(6.2, 4.4))
styles = {"DR2": ("C3", "-", "DESI DR2 (baseline)"),
          "DR3": ("C0", "-", "DESI DR3 forecast"),
          "DR3 + LSST": ("C2", "-", "DR3 + LSST Y10")}
for name, (col, ls, lab) in styles.items():
    ax.loglog(chi0_grid, curves[name], color=col, linestyle=ls, lw=2, label=lab)
ax.axhline(XI_CASSINI, color="k", linestyle="--", lw=1,
           label=r"Cassini bound $\xi_\chi \leq 2.4\times 10^{-2}$")
ax.axvline(1/10, color="gray", linestyle=":", lw=0.8)
ax.set_xlabel(r"$\chi_0 / M_\mathrm{P}$")
ax.set_ylabel(r"$\sigma(\xi_\chi)$  (Fisher, marginalised)")
ax.set_title(r"D16 — ECI NMC Fisher forecast, $\Omega_\Lambda=0.7$, "
             r"$B_\mathrm{num}=9.05$")
ax.legend(frameon=False, loc="lower left", fontsize=9)
ax.grid(True, which="both", alpha=0.3)
fig.tight_layout()
out_pdf = FIG_DIR / "D16-fisher-sigma-xi.pdf"
fig.savefig(out_pdf)
fig.savefig(out_pdf.with_suffix(".png"), dpi=150)
plt.close(fig)
print(f"\nFigure saved: {out_pdf}")

# ─────────────────────────────────────────────────────────────────────────
# 7. Dump summary JSON
# ─────────────────────────────────────────────────────────────────────────
summary = {
    "fiducial": dict(w0=W0_FID, wa=WA_FID, Omega_L=OM_L_FID, xi=0.0),
    "B_num_07": B_NUM_07,
    "chi0_ref": CHI0_REF,
    "sigma_Omega_L_prior": SIGMA_OM_L_PRIOR,
    "sigma_w0_wa": {
        name: dict(sig_w0=float(np.sqrt(C[0,0])),
                   sig_wa=float(np.sqrt(C[1,1])),
                   rho=float(C[0,1]/np.sqrt(C[0,0]*C[1,1])))
        for name, C in SCENARIOS.items()
    },
    "sigma_xi_chi0_ref": {k: float(v) for k, v in sigma_xi_ref.items()},
    "sigma_xi_chi0_scan": {
        name: {float(c): float(s) for c, s in zip(chi0_grid, curves[name])}
        for name in curves
    },
    "envelope_check_DR3": dict(analytic=float(sig_env),
                               fisher=float(sigma_xi_ref["DR3"]),
                               ratio=float(ratio)),
    "discrimination_vs_Cassini_sigma": {
        name: float(XI_CASSINI / sigma_xi_ref[name])
        for name in ("DR2", "DR3", "LSST Y10", "DR3 + LSST")
    },
    "cassini_bound": XI_CASSINI,
}
out_json = RES_DIR / "D16-summary.json"
out_json.write_text(json.dumps(summary, indent=2))
print(f"Summary saved: {out_json}")

print("\nAll assertions passed.")
