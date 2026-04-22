#!/usr/bin/env python3
"""
D18 — Forecast S/N for the ECI v6 cosmological falsifier
========================================================

Falsifier ansatz (owner, v6):

    Δfσ_8(z)/fσ_8(z)|_ECI = ε_0 · Θ(PH_2[δn(z)]) · (1+z)^{-γ}

with Θ(x) = exp[−(x/x_c)^α], α = 0.095.

PH_2 scaling
------------
Yip+2024 (arXiv:2410.18749) report PH_2 H_2 persistence-diagram feature
counts per (Gpc/h)^3 in Quijote halo catalogs at z≈0 of O(10^3–10^4).
Growth of H_2 features tracks non-linear shell-crossing, hence is
suppressed with linear growth D(z).  Two fiducial models:

    (A) Yip-anchored:  PH_2(z) ∝ D(z)^2       (shells ~ δ^2)
        x(z)/x_c     =  (D(z)/D(0))^2
        Θ(z) = exp[-((D(z)/D(0))^2)^α]
    (B) Ad-hoc:        PH_2(z) ∝ (1+z)^{-3/2}
        x(z)/x_c      = (1+z)^{-3/2}

Both bracket the plausible redshift behaviour.  Scenario (A) is adopted
for the fiducial forecast; (B) is reported as a cross-check.

Surveys
-------
DESI DR3 ELG (targets / DESI collaboration 2024 forecasts):
    z ∈ [0.8, 1.6], Δz = 0.1,  σ(fσ_8) ≈ 0.015 per bin.
LSST Y10 spectroscopic-photo cross (roughly):
    z ∈ [0.4, 1.2], Δz = 0.1,  σ(fσ_8) ≈ 0.020 per bin.
Euclid DR1 spectro (Euclid SRD, IST:Forecast):
    z ∈ [0.9, 1.8], Δz = 0.1,  σ(fσ_8) ≈ 0.020 per bin.

Fiducial fσ_8(z) from ΛCDM (Ω_m=0.315):
    f(z) ≈ Ω_m(z)^0.55,  σ_8(z) = σ_8(0) · D(z),
    D(z) via Carroll–Press–Turner fit.

Forecast
--------
    S/N(ε_0,α) = sqrt( Σ_z [Δfσ_8(z)]^2 / σ_survey(fσ_8;z)^2 )

Gate
----
    S/N ≥ 1  at fiducial (ε_0=0.02, α=0.095)  →  JCAP
    0.5 ≤ S/N < 1                             →  ambiguous
    S/N < 0.5                                 →  JHEP/PRD-formal fallback

Cassini cross-check
-------------------
Linearising the v6 equation around χ_0 = M_P/10 gives an estimate
    ε_0 ≃ k_v6 · |ξ_χ|, k_v6 ∈ [0.5, 2]  (order-unity coupling, D15).
We report the ε_0 band corresponding to |ξ_χ| ≤ 2.4·10⁻² (Cassini, D7).

Outputs
-------
    figures/D18-fsigma8-PH-forecast.pdf   (4-panel composite)
    _results/D18-summary.json

Run time ≲ 5 s; deterministic.
"""
from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import matplotlib.pyplot as plt
from matplotlib import gridspec
import sympy as sp

ROOT = Path(__file__).resolve().parent
FIG = ROOT / "figures"
RES = ROOT / "_results"
FIG.mkdir(exist_ok=True)
RES.mkdir(exist_ok=True)

# ──────────────────────────────────────────────────────────────────────
# 1. Cosmology fiducial
# ──────────────────────────────────────────────────────────────────────
OMEGA_M0 = 0.315
OMEGA_L0 = 1.0 - OMEGA_M0
SIGMA8_0 = 0.811


def E(z):
    return np.sqrt(OMEGA_M0 * (1 + z) ** 3 + OMEGA_L0)


def Omega_m(z):
    return OMEGA_M0 * (1 + z) ** 3 / E(z) ** 2


def growth_D(z):
    """Carroll–Press–Turner (1992) fitting formula, normalised D(0)=1."""
    def g(Om, OL):
        return 2.5 * Om / (Om ** (4.0 / 7.0) - OL + (1 + Om / 2) * (1 + OL / 70))
    Om_z = Omega_m(z)
    OL_z = OMEGA_L0 / E(z) ** 2
    D_unnorm = g(Om_z, OL_z) / (1 + z)
    D0 = g(OMEGA_M0, OMEGA_L0)
    return D_unnorm / D0


def f_growth(z):
    return Omega_m(z) ** 0.55


def fsigma8(z):
    return f_growth(z) * SIGMA8_0 * growth_D(z)


# ──────────────────────────────────────────────────────────────────────
# 2. PH_2 theta factor
# ──────────────────────────────────────────────────────────────────────
def theta_A(z, alpha):
    """Yip-anchored: PH_2 ∝ D(z)^2 ; x/x_c = (D(z)/D(0))^2 ≤ 1."""
    x = (growth_D(z) / growth_D(0.0)) ** 2
    return np.exp(-(x ** alpha))


def theta_B(z, alpha):
    x = (1 + z) ** (-1.5)
    return np.exp(-(x ** alpha))


# ──────────────────────────────────────────────────────────────────────
# 3. Survey configurations
# ──────────────────────────────────────────────────────────────────────
def bins(zmin, zmax, dz=0.1):
    n = int(round((zmax - zmin) / dz))
    edges = np.linspace(zmin, zmax, n + 1)
    return 0.5 * (edges[:-1] + edges[1:])


SURVEYS = {
    "DESI-DR3-ELG":  {"z": bins(0.8, 1.6, 0.1), "sig": 0.015},
    "LSST-Y10":      {"z": bins(0.4, 1.2, 0.1), "sig": 0.020},
    "Euclid-DR1":    {"z": bins(0.9, 1.8, 0.1), "sig": 0.020},
}

# combos (independent-dataset assumption; overlap small because redshift
# windows only partially coincide and tracers differ).
COMBOS = {
    "DR3":            ["DESI-DR3-ELG"],
    "DR3+LSST":       ["DESI-DR3-ELG", "LSST-Y10"],
    "DR3+Euclid":     ["DESI-DR3-ELG", "Euclid-DR1"],
    "DR3+LSST+Euclid": ["DESI-DR3-ELG", "LSST-Y10", "Euclid-DR1"],
}


# ──────────────────────────────────────────────────────────────────────
# 4. Forecast S/N
# ──────────────────────────────────────────────────────────────────────
def delta_fs8(z, eps0, alpha, gamma=1.0, theta=theta_A):
    return eps0 * theta(z, alpha) * (1 + z) ** (-gamma) * fsigma8(z)


def sn_survey(name, eps0, alpha, gamma=1.0, theta=theta_A):
    s = SURVEYS[name]
    d = delta_fs8(s["z"], eps0, alpha, gamma, theta)
    return float(np.sqrt(np.sum((d / s["sig"]) ** 2)))


def sn_combo(names, eps0, alpha, gamma=1.0, theta=theta_A):
    acc = 0.0
    for n in names:
        acc += sn_survey(n, eps0, alpha, gamma, theta) ** 2
    return float(np.sqrt(acc))


# ──────────────────────────────────────────────────────────────────────
# 5. Fiducial evaluation
# ──────────────────────────────────────────────────────────────────────
EPS_FID = 0.02
ALPHA_FID = 0.095
GAMMA_FID = 1.0

fid_sn = {c: sn_combo(s, EPS_FID, ALPHA_FID, GAMMA_FID, theta_A)
          for c, s in COMBOS.items()}
fid_sn_B = {c: sn_combo(s, EPS_FID, ALPHA_FID, GAMMA_FID, theta_B)
            for c, s in COMBOS.items()}

print("Fiducial S/N (theta_A, Yip-anchored):")
for k, v in fid_sn.items():
    print(f"  {k:20s}  S/N = {v:.3f}")
print("Fiducial S/N (theta_B, (1+z)^-3/2):")
for k, v in fid_sn_B.items():
    print(f"  {k:20s}  S/N = {v:.3f}")


# ──────────────────────────────────────────────────────────────────────
# 6. Minimum ε_0 for S/N = 1 (scales linearly in ε_0)
# ──────────────────────────────────────────────────────────────────────
def eps_min(combo, target_sn=1.0, alpha=ALPHA_FID, theta=theta_A):
    s0 = sn_combo(COMBOS[combo], 1.0, alpha, GAMMA_FID, theta)  # linear in eps
    return target_sn / s0


eps_min_1sig = {c: eps_min(c, 1.0, ALPHA_FID, theta_A) for c in COMBOS}
eps_min_05sig = {c: eps_min(c, 0.5, ALPHA_FID, theta_A) for c in COMBOS}

print("\nMin ε_0 for 1σ detection:")
for k, v in eps_min_1sig.items():
    print(f"  {k:20s}  ε0_min = {v:.4f}")


# ──────────────────────────────────────────────────────────────────────
# 7. 2-D contour (ε_0, α) plane for DR3+Euclid
# ──────────────────────────────────────────────────────────────────────
eps_grid = np.linspace(0.005, 0.10, 60)
alpha_grid = np.linspace(0.05, 0.15, 55)
E_M, A_M = np.meshgrid(eps_grid, alpha_grid, indexing="ij")

SN_DR3E = np.zeros_like(E_M)
SN_ALL = np.zeros_like(E_M)
for i in range(E_M.shape[0]):
    for j in range(E_M.shape[1]):
        SN_DR3E[i, j] = sn_combo(COMBOS["DR3+Euclid"], E_M[i, j], A_M[i, j],
                                 GAMMA_FID, theta_A)
        SN_ALL[i, j] = sn_combo(COMBOS["DR3+LSST+Euclid"], E_M[i, j],
                                A_M[i, j], GAMMA_FID, theta_A)


# ──────────────────────────────────────────────────────────────────────
# 8. Cassini / Swampland cross-check
# ──────────────────────────────────────────────────────────────────────
# v6 links Δfσ_8 amplitude ε_0 to the NMC coupling ξ_χ through the
# perturbation equation (D14, eq. for G_eff).  A back-of-envelope
# linearisation at χ_0=M_P/10 and gradient ln(δn)~O(1) gives
#     ε_0 ≃ k_v6 |ξ_χ|,   k_v6 ∈ [0.5, 2].
XI_CASSINI = 2.4e-2
K_V6_LO, K_V6_HI = 0.5, 2.0
EPS_CASS_LO = K_V6_LO * XI_CASSINI      # 0.012
EPS_CASS_HI = K_V6_HI * XI_CASSINI      # 0.048


# ──────────────────────────────────────────────────────────────────────
# 9. Sanity: symbolic consistency of the ansatz
# ──────────────────────────────────────────────────────────────────────
z_s, e0_s, a_s, g_s, xc_s, x_s = sp.symbols("z eps0 alpha gamma x_c x",
                                            positive=True, real=True)
theta_sym = sp.exp(-(x_s / xc_s) ** a_s)
delta_sym = e0_s * theta_sym * (1 + z_s) ** (-g_s)
# derivative w.r.t. eps0 must be theta·(1+z)^-g (linearity check)
dd_de = sp.simplify(sp.diff(delta_sym, e0_s) - theta_sym * (1 + z_s) ** (-g_s))
assert dd_de == 0, "linearity check failed"


# ──────────────────────────────────────────────────────────────────────
# 10. Figure
# ──────────────────────────────────────────────────────────────────────
fig = plt.figure(figsize=(11.5, 9.0))
gs = gridspec.GridSpec(2, 2, wspace=0.28, hspace=0.32)

# (a) fσ_8(z) + ECI correction curves per survey
ax = fig.add_subplot(gs[0, 0])
z_plot = np.linspace(0.2, 1.9, 120)
ax.plot(z_plot, fsigma8(z_plot), "k-", lw=1.6, label=r"$f\sigma_8^{\Lambda\rm CDM}(z)$")
for name, s in SURVEYS.items():
    ax.errorbar(s["z"], fsigma8(s["z"]), yerr=s["sig"], fmt="o", ms=4,
                label=f"{name} σ={s['sig']}")
d_fid = delta_fs8(z_plot, EPS_FID, ALPHA_FID, GAMMA_FID, theta_A)
ax.plot(z_plot, fsigma8(z_plot) + d_fid, "r--", lw=1.3,
        label=rf"ECI ε$_0$={EPS_FID}, α={ALPHA_FID}")
ax.set_xlabel("z"); ax.set_ylabel(r"$f\sigma_8$")
ax.set_title("(a) Fiducial fσ_8 + ECI v6 shift")
ax.legend(fontsize=7, loc="lower left"); ax.grid(alpha=0.3)

# (b) Residual Δfσ_8(z) vs survey error bars
ax = fig.add_subplot(gs[0, 1])
ax.plot(z_plot, d_fid, "r-", lw=1.6, label=r"Δfσ$_8$ ECI (θ_A)")
ax.plot(z_plot, delta_fs8(z_plot, EPS_FID, ALPHA_FID, GAMMA_FID, theta_B),
        "m--", lw=1.2, label=r"Δfσ$_8$ ECI (θ_B)")
for name, s in SURVEYS.items():
    ax.fill_between(s["z"], -s["sig"], s["sig"], alpha=0.18, label=name)
ax.axhline(0, color="k", lw=0.5)
ax.set_xlabel("z"); ax.set_ylabel(r"Δfσ$_8$")
ax.set_title(f"(b) ECI signal vs survey σ (ε0={EPS_FID}, α={ALPHA_FID})")
ax.legend(fontsize=7); ax.grid(alpha=0.3)

# (c) S/N contour DR3+Euclid
ax = fig.add_subplot(gs[1, 0])
levels = [0.5, 1.0, 2.0, 3.0, 5.0]
cs = ax.contourf(E_M, A_M, SN_DR3E, levels=[0] + levels + [1e3],
                 cmap="viridis", alpha=0.85)
cl = ax.contour(E_M, A_M, SN_DR3E, levels=levels, colors="w", linewidths=1.0)
ax.clabel(cl, fmt="%.1fσ", fontsize=7)
ax.axvline(EPS_FID, color="r", ls="--", lw=1.0, label=f"ε0 fid={EPS_FID}")
ax.axhline(ALPHA_FID, color="r", ls=":", lw=1.0, label=f"α fid={ALPHA_FID}")
ax.axvspan(EPS_CASS_LO, EPS_CASS_HI, color="orange", alpha=0.25,
           label="Cassini-allowed ε0")
ax.set_xlabel(r"ε$_0$"); ax.set_ylabel(r"α")
ax.set_title("(c) S/N — DR3 + Euclid DR1 joint")
ax.legend(fontsize=7, loc="upper right")
fig.colorbar(cs, ax=ax, label="S/N")

# (d) S/N vs ε_0 at α=0.095 for all combos + gate lines
ax = fig.add_subplot(gs[1, 1])
eps_lin = np.linspace(0.0, 0.10, 200)
for c in COMBOS:
    s0 = sn_combo(COMBOS[c], 1.0, ALPHA_FID, GAMMA_FID, theta_A)
    ax.plot(eps_lin, s0 * eps_lin, lw=1.4, label=c)
ax.axhline(1.0, color="k", ls="--", lw=0.8, label="1σ gate")
ax.axhline(0.5, color="gray", ls=":", lw=0.8, label="0.5σ gate")
ax.axvline(EPS_FID, color="r", ls="--", lw=1.0)
ax.axvspan(EPS_CASS_LO, EPS_CASS_HI, color="orange", alpha=0.2)
ax.set_xlabel(r"ε$_0$"); ax.set_ylabel("S/N")
ax.set_title("(d) S/N(ε0) at α=0.095 — gate decision")
ax.grid(alpha=0.3); ax.legend(fontsize=7, loc="upper left")
ax.set_xlim(0, 0.10); ax.set_ylim(0, 6)

fig.suptitle("D18 — fσ_8 persistent-homology falsifier forecast (v6 gate)",
             fontsize=12, y=0.995)
outpdf = FIG / "D18-fsigma8-PH-forecast.pdf"
fig.savefig(outpdf, bbox_inches="tight")
fig.savefig(FIG / "D18-fsigma8-PH-forecast.png", dpi=130, bbox_inches="tight")
plt.close(fig)
print(f"\nWrote {outpdf}")


# ──────────────────────────────────────────────────────────────────────
# 11. Verdict
# ──────────────────────────────────────────────────────────────────────
sn_key = fid_sn["DR3+Euclid"]
if sn_key >= 1.0:
    verdict = "JCAP"
elif sn_key >= 0.5:
    verdict = "AMBIGUOUS"
else:
    verdict = "JHEP_FALLBACK"

# Cassini compatibility of required ε_0
cass_ok_1sig = {c: (eps_min_1sig[c] <= EPS_CASS_HI) for c in COMBOS}

summary = {
    "fiducial": {"eps0": EPS_FID, "alpha": ALPHA_FID, "gamma": GAMMA_FID},
    "SN_thetaA": fid_sn,
    "SN_thetaB": fid_sn_B,
    "eps_min_1sigma": eps_min_1sig,
    "eps_min_0p5sigma": eps_min_05sig,
    "cassini_band_eps0": [EPS_CASS_LO, EPS_CASS_HI],
    "cassini_compat_1sig": cass_ok_1sig,
    "verdict": verdict,
    "notes": [
        "theta_A (Yip-anchored PH_2 ∝ D^2) is the fiducial model.",
        "theta_B ((1+z)^-3/2) reported as cross-check only.",
        "k_v6 in [0.5, 2] maps ε_0 to |ξ_χ| via D14/D15 linearisation.",
        "Survey σ(fσ_8) are SRD/DESI target values, not realised.",
    ],
}
with open(RES / "D18-summary.json", "w") as f:
    json.dump(summary, f, indent=2)

print(f"\nVerdict for v6 target:  {verdict}")
print(f"  S/N[DR3]         = {fid_sn['DR3']:.3f}")
print(f"  S/N[DR3+LSST]    = {fid_sn['DR3+LSST']:.3f}")
print(f"  S/N[DR3+Euclid]  = {fid_sn['DR3+Euclid']:.3f}")
print(f"  S/N[DR3+LSST+E]  = {fid_sn['DR3+LSST+Euclid']:.3f}")
print(f"  ε0_min(1σ) DR3+E = {eps_min_1sig['DR3+Euclid']:.4f}")
print(f"  Cassini band     = [{EPS_CASS_LO:.3f}, {EPS_CASS_HI:.3f}]")
