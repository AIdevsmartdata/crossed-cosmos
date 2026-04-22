#!/usr/bin/env python3
# =============================================================================
# D17 — Post-MCMC posterior analysis (ECI v5.0 plugin route)
# -----------------------------------------------------------------------------
# Reads the 4 MPI chains from mcmc/chains/eci_v50_run1/ (Cobaya output, prefix
# `eci`) and produces:
#   - posterior medians + 1σ + 2σ + MAP best-fit for all 9 sampled params,
#   - marginalised 1D posterior on xi_chi (primary ECI result),
#   - best-fit χ² and Δχ² vs a ξ_χ=0 slice of the same chain (Bayesian
#     proxy for the ΛCDM-like nested model),
#   - effective sample size (ESS) / integrated autocorrelation time (IAT),
#   - Savage–Dickey density ratio at ξ_χ=0 → Bayes factor BF_{ξ≠0, ξ=0},
#   - figures/D17-triangle.pdf (full 9-param triangle),
#   - figures/D17-w0wa-eci-band.pdf (w0,wa with ECI ξ band + Scherrer–Sen
#     reference + DESI DR2+DESY5 fiducial ellipse),
#   - mcmc/_results/posterior_summary.json.
#
# Burn-in: first 30% of each chain (on top of Cobaya's internal learning
# drop). R-1 and NMC plugin conventions follow D14 / D13 / D16.
#
# Kevin Remondière, 2026-04-22.
# =============================================================================

from __future__ import annotations

import json
import os
import sys
from pathlib import Path

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse

from getdist import loadMCSamples, plots

ROOT = Path(__file__).resolve().parent.parent
CHAIN_PREFIX = ROOT / "mcmc" / "chains" / "eci_v50_run1" / "eci"
OUT_FIG = ROOT / "derivations" / "figures"
OUT_RES = ROOT / "mcmc" / "_results"
OUT_FIG.mkdir(parents=True, exist_ok=True)
OUT_RES.mkdir(parents=True, exist_ok=True)

PARAMS = [
    "H0", "omega_b", "omega_cdm", "n_s", "logA",
    "w0_fld", "wa_fld", "xi_chi", "chi_initial",
]
LATEX = {
    "H0": r"H_0",
    "omega_b": r"\Omega_\mathrm{b} h^2",
    "omega_cdm": r"\Omega_\mathrm{c} h^2",
    "n_s": r"n_\mathrm{s}",
    "logA": r"\log(10^{10} A_\mathrm{s})",
    "w0_fld": r"w_0",
    "wa_fld": r"w_a",
    "xi_chi": r"\xi_\chi",
    "chi_initial": r"\chi_0",
}


# -----------------------------------------------------------------------------
# 1. Load chains + remove burn-in
# -----------------------------------------------------------------------------
print(f"[D17] Loading chains from {CHAIN_PREFIX}.*.txt …")
samples = loadMCSamples(str(CHAIN_PREFIX), settings={"ignore_rows": 0.3})
# force gaussian KDE smoothing consistent across params
samples.updateSettings({"smooth_scale_2D": 0.3, "smooth_scale_1D": 0.3})
print(f"[D17] Loaded. N samples (post burn-in) = {samples.numrows}")
print(f"[D17] Parameter names present: {[p.name for p in samples.paramNames.names]}")

# -----------------------------------------------------------------------------
# 2. Summary stats (median, 68/95 CI, MAP) + ESS/IAT
# -----------------------------------------------------------------------------
summary = {}
marge = samples.getMargeStats()

# best-fit (MAP) = point with minimum -log(post)
col_logp = samples.index.get("minuslogpost", None)
if col_logp is None:
    # getdist stores it implicitly in samples.loglikes (this is minuslogpost)
    loglikes = samples.loglikes
else:
    loglikes = samples.samples[:, col_logp]
iMAP = int(np.argmin(loglikes))

for p in PARAMS:
    if p not in samples.index:
        print(f"[D17] WARNING: param {p} not in chain, skipping.")
        continue
    col = samples.index[p]
    arr = samples.samples[:, col]
    w = samples.weights
    # weighted median & CIs via getdist
    pstats = marge.parWithName(p)
    med = float(pstats.mean)  # getdist 'mean' (weighted)
    # quantiles 16/84 and 2.5/97.5
    order = np.argsort(arr)
    cw = np.cumsum(w[order])
    cw /= cw[-1]
    q = lambda f: float(np.interp(f, cw, arr[order]))
    median = q(0.5)
    lo1, hi1 = q(0.16), q(0.84)
    lo2, hi2 = q(0.025), q(0.975)
    map_val = float(arr[iMAP])
    # IAT (integrated autocorrelation) via getdist per-chain
    try:
        iat = float(samples.getEffectiveSamples(col))
        ess = iat  # getEffectiveSamples already returns ESS
    except Exception:
        ess = float("nan")
    summary[p] = {
        "latex": LATEX.get(p, p),
        "mean": med,
        "median": median,
        "sigma1_lo": lo1,
        "sigma1_hi": hi1,
        "sigma2_lo": lo2,
        "sigma2_hi": hi2,
        "MAP": map_val,
        "ESS": ess,
    }
    print(f"  {p:14s}  median={median: .5f}  68%=[{lo1: .5f},{hi1: .5f}]  "
          f"95%=[{lo2: .5f},{hi2: .5f}]  MAP={map_val: .5f}  ESS={ess:.0f}")

# -----------------------------------------------------------------------------
# 3. R-1 (final) from Cobaya progress file + acceptance
# -----------------------------------------------------------------------------
prog = CHAIN_PREFIX.with_suffix(".progress")
R_final = None
acc_final = None
N_final = None
if prog.exists():
    lines = [l for l in prog.read_text().splitlines() if l.strip() and not l.startswith("#")]
    if lines:
        last = lines[-1].split()
        N_final = float(last[0])
        acc_final = float(last[2])
        R_final = float(last[3])
        print(f"[D17] Final R-1 = {R_final:.4f}  acceptance = {acc_final:.3f}  "
              f"N = {N_final:.0f}")

# -----------------------------------------------------------------------------
# 4. Best-fit χ² (total) and Δχ² vs a ξ_χ=0 restricted sub-sample
# -----------------------------------------------------------------------------
chi2_bao = samples.samples[iMAP, samples.index["chi2__bao.desi_dr2.desi_bao_all"]]
chi2_sn = samples.samples[iMAP, samples.index["chi2__sn.pantheonplus"]]
chi2_tot = float(chi2_bao + chi2_sn)
print(f"[D17] Best-fit χ²: BAO={chi2_bao:.2f}  SN={chi2_sn:.2f}  total={chi2_tot:.2f}")

# ΛCDM-like proxy: minimum χ² among samples with |xi_chi| < 0.005
xi_col = samples.index["xi_chi"]
mask_lcdm = np.abs(samples.samples[:, xi_col]) < 0.005
if mask_lcdm.sum() > 50:
    chi2_tot_all = (samples.samples[:, samples.index["chi2__bao.desi_dr2.desi_bao_all"]]
                    + samples.samples[:, samples.index["chi2__sn.pantheonplus"]])
    chi2_lcdm_proxy = float(np.min(chi2_tot_all[mask_lcdm]))
    dchi2 = chi2_tot - chi2_lcdm_proxy
    print(f"[D17] ΛCDM-like (|ξ|<0.005) min χ² proxy = {chi2_lcdm_proxy:.2f}  "
          f"Δχ² = {dchi2:+.3f}")
else:
    chi2_lcdm_proxy = None
    dchi2 = None
    print("[D17] Not enough |ξ|<0.005 samples for ΛCDM-like proxy.")

# -----------------------------------------------------------------------------
# 5. Savage–Dickey Bayes factor at ξ_χ=0
# -----------------------------------------------------------------------------
# BF_{ξ≠0 vs ξ=0} = π(ξ=0) / p(ξ=0 | data)  (uniform prior on [-0.1,0.1])
prior_width = 0.2
prior_density_at_0 = 1.0 / prior_width

# posterior density at 0 from 1D marginalised KDE (normalise to unit area)
dens = samples.get1DDensity("xi_chi")
dens.normalize(by="integral", in_place=True)
post_density_at_0 = float(dens.Prob(0.0))
# Savage–Dickey: BF_{M0 vs M1} = p(θ=0|D) / π(θ=0).  BF>1 favours nested (ξ=0 / ΛCDM-like).
SD_BF_null = post_density_at_0 / prior_density_at_0
SD_BF_alt = 1.0 / SD_BF_null if SD_BF_null > 0 else float("inf")
print(f"[D17] Savage–Dickey:  π(0)={prior_density_at_0:.3f}  p(0|D)={post_density_at_0:.3f}")
print(f"        BF(ξ=0 / ξ≠0) [favours ΛCDM-like] = {SD_BF_null:.3f}  "
      f"ln BF = {np.log(SD_BF_null):+.3f}")
print(f"        BF(ξ≠0 / ξ=0) [favours ECI]       = {SD_BF_alt:.3f}")

# -----------------------------------------------------------------------------
# 6. Wolf 2025 bound comparison
# -----------------------------------------------------------------------------
# ξ_χ * (chi_0 / M_P)² ≤ 6e-6, evaluated at posterior median / 95% bound
xi_med = summary["xi_chi"]["median"]
chi_med = summary["chi_initial"]["median"]
xi_hi2 = summary["xi_chi"]["sigma2_hi"]
chi_hi2 = summary["chi_initial"]["sigma2_hi"]
wolf_median = abs(xi_med) * chi_med**2
wolf_95 = max(abs(xi_hi2), abs(summary["xi_chi"]["sigma2_lo"])) * max(chi_med, chi_hi2)**2
print(f"[D17] |ξ_χ|(χ_0/M_P)² : median={wolf_median:.2e}  95%-envelope={wolf_95:.2e} "
      f" (Wolf 2025 bound = 6e-6)")

# -----------------------------------------------------------------------------
# 7. JSON summary
# -----------------------------------------------------------------------------
out_json = {
    "mcmc": {
        "chain_prefix": str(CHAIN_PREFIX),
        "n_samples_post_burnin": int(samples.numrows),
        "burn_in_fraction": 0.30,
        "R_minus_1_final": R_final,
        "acceptance_final": acc_final,
        "N_steps_final": N_final,
    },
    "params": summary,
    "bestfit": {
        "index": iMAP,
        "minuslogpost": float(loglikes[iMAP]),
        "chi2_BAO": float(chi2_bao),
        "chi2_SN": float(chi2_sn),
        "chi2_total": chi2_tot,
    },
    "lcdm_like_proxy": {
        "definition": "min chi2 among samples with |xi_chi|<0.005",
        "chi2_total": chi2_lcdm_proxy,
        "delta_chi2_ECI_minus_LCDM": dchi2,
    },
    "bayes_factor_savage_dickey": {
        "prior_density_at_zero": prior_density_at_0,
        "posterior_density_at_zero": post_density_at_0,
        "BF_xi_eq_0_vs_xi_ne_0": SD_BF_null,
        "BF_xi_ne_0_vs_xi_eq_0": SD_BF_alt,
        "ln_BF_null_over_alt": float(np.log(SD_BF_null)) if SD_BF_null > 0 else None,
        "interpretation": (
            "Savage–Dickey BF(M0/M1) = p(0|D)/π(0). BF>1 favours ΛCDM-like (ξ=0); "
            "BF<1 favours ECI (ξ≠0). Jeffreys: |ln BF|<1 inconclusive, 1–3 moderate, "
            ">3 strong."
        ),
    },
    "wolf2025_comparison": {
        "bound_xi_chi_over_MP_squared": 6.0e-6,
        "median_value": wolf_median,
        "envelope_95pct": wolf_95,
        "note": (
            "Wolf+2025 Cassini/DESI joint PPN bound. χ_0 here is the cosmological "
            "thawing-excursion scale, not the solar-system local χ; the two coincide "
            "in the unscreened case used here."
        ),
    },
}
with open(OUT_RES / "posterior_summary.json", "w") as f:
    json.dump(out_json, f, indent=2, default=float)
print(f"[D17] Wrote {OUT_RES/'posterior_summary.json'}")

# -----------------------------------------------------------------------------
# 8. Triangle plot (9 params)
# -----------------------------------------------------------------------------
print("[D17] Building triangle plot…")
g = plots.get_subplot_plotter(width_inch=11)
g.settings.axes_fontsize = 8
g.settings.lab_fontsize = 10
g.settings.title_limit_fontsize = 9
g.triangle_plot(
    samples,
    params=PARAMS,
    filled=True,
    title_limit=1,
)
plt.savefig(OUT_FIG / "D17-triangle.pdf", bbox_inches="tight")
plt.close("all")
print(f"[D17] Wrote {OUT_FIG/'D17-triangle.pdf'}")

# -----------------------------------------------------------------------------
# 9. (w0, wa) + ECI band + Scherrer–Sen + DESI DR2+DESY5 ellipse
# -----------------------------------------------------------------------------
print("[D17] Building (w0,wa) ECI-band plot…")
fig, ax = plt.subplots(figsize=(6.5, 5.2))

# MCMC contours via getdist
g2 = plots.get_single_plotter(width_inch=6.5)
g2.settings.alpha_filled_add = 0.4
g2.plot_2d(
    samples,
    "w0_fld", "wa_fld",
    filled=True,
    contour_colors=["#1f77b4"],
    lims=[-1.15, -0.55, -1.8, 0.1],
    ax=ax,
)

# Scherrer–Sen line at Ω_Λ=0.7 : wa = -1.58 (1+w0)
w0_grid = np.linspace(-1.15, -0.55, 200)
ax.plot(w0_grid, -1.58 * (1 + w0_grid),
        "--", color="#2ca02c", lw=1.6, label=r"Scherrer–Sen ($\Omega_\Lambda=0.7$)")

# ECI band : wa = -1.58(1+w0) + B ξ sqrt(1+w0) (χ_0/M_P), |ξ|≤ 2σ posterior
xi_2sig = max(abs(summary["xi_chi"]["sigma2_hi"]),
              abs(summary["xi_chi"]["sigma2_lo"]))
chi0 = summary["chi_initial"]["median"]
B_num = 9.05  # D13 numerical at Ω_Λ=0.7
w0_pos = w0_grid[w0_grid > -1.0]
wa_centre = -1.58 * (1 + w0_pos)
halfband = B_num * xi_2sig * np.sqrt(1 + w0_pos) * chi0
ax.fill_between(w0_pos, wa_centre - halfband, wa_centre + halfband,
                color="#2ca02c", alpha=0.18,
                label=fr"ECI band $|\xi_\chi|\le{xi_2sig:.3f}$ (2$\sigma$), $\chi_0={chi0:.3f}M_P$")

# DESI DR2+DESY5 fiducial ellipse: centre (-0.752,-0.86), σ_w0=0.057, σ_wa=0.215, ρ=-0.89
cx, cy = -0.752, -0.86
sx, sy, rho = 0.057, 0.215, -0.89
cov = np.array([[sx*sx, rho*sx*sy], [rho*sx*sy, sy*sy]])
vals, vecs = np.linalg.eigh(cov)
angle = np.degrees(np.arctan2(*vecs[:, 1][::-1]))
for nsig, alpha in [(1.52, 0.55), (2.49, 0.30)]:  # 68% / 95% for 2-dof
    w, h = 2 * nsig * np.sqrt(vals)
    ax.add_patch(Ellipse((cx, cy), w, h, angle=angle,
                         facecolor="none", edgecolor="#ff7f0e",
                         lw=1.4, alpha=alpha))
ax.plot([cx], [cy], "x", color="#ff7f0e", ms=8, label="DESI DR2 + DESY5 fiducial")

# ΛCDM marker
ax.plot([-1.0], [0.0], "k*", ms=10, label=r"$\Lambda$CDM")

ax.set_xlabel(r"$w_0$")
ax.set_ylabel(r"$w_a$")
ax.set_xlim(-1.15, -0.55)
ax.set_ylim(-1.8, 0.1)
ax.legend(loc="lower left", fontsize=8, framealpha=0.9)
ax.set_title("ECI v5.0 MCMC posterior — DESI DR2 + Pantheon+ (plugin route)")
ax.grid(alpha=0.3)
plt.tight_layout()
plt.savefig(OUT_FIG / "D17-w0wa-eci-band.pdf", bbox_inches="tight")
plt.close("all")
print(f"[D17] Wrote {OUT_FIG/'D17-w0wa-eci-band.pdf'}")

print("[D17] Done.")
