#!/usr/bin/env python3
"""
D18b — Bias marginalisation / orthogonality test for the ECI v6 falsifier
========================================================================

Context
-------
D18 forecasts S/N for the falsifier

    Δfσ_8(z)/fσ_8(z)|_ECI = ε_0 · Θ(PH_2[δn(z)]) · (1+z)^{-γ}

while holding the galaxy-bias nuisance fixed.  The ELG tracer used by
DESI DR3 in z ∈ [0.8, 1.6] has a *scale-dependent* bias

    b(z, k) = b_0(z) + b_k · k^2

and cosmic filaments — which carry the PH_2 topological signal — are
traced precisely by ELGs.  If the (z,k)-dependence of Θ(PH_2) is
degenerate with a renormalisation of b(z,k), the ECI signal is absorbed
into the bias fit and the falsifier dies.

Test
----
We build a Fisher matrix for the RSD observable

    fσ_8(z)^{obs} = fσ_8^{ΛCDM}(z) · [1 + ε_0·Θ(z)·(1+z)^{-γ}]
                    · g(b(z,k_eff), μ_eff)

expanded around the fiducial (b_0, b_k, ε_0, α).  We use the
Kaiser-like monopole-equivalent factor

    g(b, μ) ≈ b + f μ²,  averaged over μ  ⇒  ⟨g⟩ = b + f/3

so that the *measured* fσ_8 is degenerate with an overall rescaling of
the linear bias only if ∂/∂b and ∂/∂ε_0 project identically onto z-bins.
We evaluate b(z, k_eff(z)) at the effective scale k_eff(z) of each
redshift bin (≈ 0.1 h/Mpc for DESI ELG RSD).

Fisher → correlation coefficient ρ(b_0, ε_0) and ρ(b_k, ε_0).

Thresholds (owner spec):
    |ρ| < 0.5          → ORTHOGONAL   (falsifier viable, JCAP)
    0.5 ≤ |ρ| < 0.9    → MIXED        (degraded)
    |ρ| ≥ 0.9          → DEGENERATE   (JHEP fallback)

We also compute the marginalised / fixed-bias degradation factor

    R = σ(ε_0)_marg / σ(ε_0)_fix

and the ε_0 at which the marginalised S/N crosses 1.

Scale-dependence argument (analytic)
------------------------------------
Polynomial b(z,k) = b_0 + b_k k² is smooth in k.  PH_2 at filtration
scale k_*  ~ 0.15 h/Mpc has a sharp activator Θ(x) = exp(-(x/x_c)^α)
with α = 0.095 (flat → cliff).  At k=k_*  the topological kernel has
support concentrated on ∼ one wavenumber octave whereas polynomial
bias is entire on that band — hence their k-projections on the RSD
window are weakly correlated.  The numerics below quantify the same
statement on the *redshift* axis at fixed k_eff.

Outputs
-------
    figures/D18b-bias-orthogonality.pdf
    _results/D18b-summary.json
    D18b-report.md (separately)
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
# 1. Cosmology fiducial (same as D18, kept local to avoid import side-effects)
# ──────────────────────────────────────────────────────────────────────
OMEGA_M0 = 0.315
OMEGA_L0 = 1.0 - OMEGA_M0
SIGMA8_0 = 0.811


def E(z):
    return np.sqrt(OMEGA_M0 * (1 + z) ** 3 + OMEGA_L0)


def Omega_m(z):
    return OMEGA_M0 * (1 + z) ** 3 / E(z) ** 2


def growth_D(z):
    def g(Om, OL):
        return 2.5 * Om / (Om ** (4.0 / 7.0) - OL + (1 + Om / 2) * (1 + OL / 70))
    Om_z = Omega_m(z)
    OL_z = OMEGA_L0 / E(z) ** 2
    return g(Om_z, OL_z) / (1 + z) / g(OMEGA_M0, OMEGA_L0)


def f_growth(z):
    return Omega_m(z) ** 0.55


def fsigma8_fid(z):
    return f_growth(z) * SIGMA8_0 * growth_D(z)


def theta_A(z, alpha):
    x = (growth_D(z) / growth_D(0.0)) ** 2
    return np.exp(-(x ** alpha))


# ──────────────────────────────────────────────────────────────────────
# 2. Galaxy bias model (ELG, DESI)
# ──────────────────────────────────────────────────────────────────────
# DESI Y1 ELG fits (cf. DESI DR1 RSD papers): b_0(z) ≈ 0.84 / D(z)
# (so that b_0·σ_8(z) is ~ constant).  Scale term b_k·k² small at k ≲ 0.2.
def b0_fid(z):
    return 0.84 / growth_D(z)


BK_FID = 0.8          # h^{-2} Mpc^2  (typical ELG 1-loop coefficient)
K_EFF = 0.12          # h/Mpc effective RSD scale for DESI ELG

# Kaiser monopole-equivalent: ⟨(b + f μ²)²⟩_μ = b² + 2 b f/3 + f²/5
# but the measured fσ_8 is extracted via the RSD *template* that divides
# by (b + f/3) to first order, so we model the *residual* bias projection
# on fσ_8 as:  fσ_8^obs(z) = fσ_8^true(z) · [1 + δb/(b0 + f/3)]
# i.e. a small misestimate of b(z,k) leaks proportionally into fσ_8.
# The leakage coefficient is L(z) = 1 / (b0(z) + f(z)/3).


def leakage(z):
    return 1.0 / (b0_fid(z) + f_growth(z) / 3.0)


# ──────────────────────────────────────────────────────────────────────
# 3. Observable model with bias nuisance + ECI
# ──────────────────────────────────────────────────────────────────────
EPS_FID = 0.02
ALPHA_FID = 0.095
GAMMA_FID = 1.0


def model_fs8(z, b0_shift, bk_shift, eps0, alpha=ALPHA_FID, gamma=GAMMA_FID):
    """fσ_8 observed with bias shift (b0_shift, bk_shift) and ECI (eps0)."""
    # Bias-induced multiplicative leakage (linear in shifts):
    db_k = b0_shift + bk_shift * K_EFF ** 2
    bias_leak = 1.0 + db_k * leakage(z)
    eci = 1.0 + eps0 * theta_A(z, alpha) * (1 + z) ** (-gamma)
    return fsigma8_fid(z) * bias_leak * eci


# ──────────────────────────────────────────────────────────────────────
# 4. Sympy sanity: derivatives are what we expect
# ──────────────────────────────────────────────────────────────────────
zsym, b0sh, bksh, epsh, aeps, th = sp.symbols(
    "z b0sh bksh eps alpha theta", real=True)
L, keff = sp.symbols("L k_eff", positive=True)
fs8 = sp.symbols("fs8", positive=True)
model = fs8 * (1 + (b0sh + bksh * keff ** 2) * L) * (1 + epsh * th)
# ∂/∂ε must be fs8 · (1 + bias_leak) · θ  (≈ fs8 · θ  to O(shift))
d_eps = sp.simplify(sp.diff(model, epsh))
# ∂/∂b0 = fs8 · L · (1 + ε θ)
d_b0 = sp.simplify(sp.diff(model, b0sh))
d_bk = sp.simplify(sp.diff(model, bksh))
assert d_b0 == fs8 * L * (1 + epsh * th)
assert d_bk == fs8 * L * keff ** 2 * (1 + epsh * th)
assert d_eps == fs8 * th * (1 + (b0sh + bksh * keff ** 2) * L)


# ──────────────────────────────────────────────────────────────────────
# 5. Survey spec (same numbers as D18)
# ──────────────────────────────────────────────────────────────────────
def bins(zmin, zmax, dz=0.1):
    n = int(round((zmax - zmin) / dz))
    edges = np.linspace(zmin, zmax, n + 1)
    return 0.5 * (edges[:-1] + edges[1:])


SURVEYS = {
    "DESI-DR3-ELG": {"z": bins(0.8, 1.6, 0.1), "sig": 0.015},
    "Euclid-DR1":   {"z": bins(0.9, 1.8, 0.1), "sig": 0.020},
}
COMBOS = {
    "DR3":         ["DESI-DR3-ELG"],
    "DR3+Euclid":  ["DESI-DR3-ELG", "Euclid-DR1"],
}

# Nuisance priors.  DESI BOSS-style Gaussian priors on the bias
# coefficients (loose): σ(b0)=0.5, σ(bk)=2.0 h^-2 Mpc^2.  These allow
# significant bias freedom — worst case for orthogonality.
SIG_B0_PRIOR = 0.5
SIG_BK_PRIOR = 2.0


# ──────────────────────────────────────────────────────────────────────
# 6. Fisher matrix
# ──────────────────────────────────────────────────────────────────────
# Parameter vector θ = (ε_0, b_0_shift, b_k_shift).  Fiducial shifts = 0.
# Derivatives evaluated at fiducial.
def derivs_at_fid(z):
    fs8v = fsigma8_fid(z)
    Lv = leakage(z)
    thv = theta_A(z, ALPHA_FID) * (1 + z) ** (-GAMMA_FID)
    d_eps = fs8v * thv                       # ∂/∂ε0
    d_b0 = fs8v * Lv                          # ∂/∂b0_shift
    d_bk = fs8v * Lv * K_EFF ** 2             # ∂/∂bk_shift
    return np.array([d_eps, d_b0, d_bk])


def fisher(combo, include_priors=True):
    F = np.zeros((3, 3))
    for sname in COMBOS[combo]:
        s = SURVEYS[sname]
        for z in s["z"]:
            d = derivs_at_fid(z)
            F += np.outer(d, d) / s["sig"] ** 2
    if include_priors:
        F[1, 1] += 1.0 / SIG_B0_PRIOR ** 2
        F[2, 2] += 1.0 / SIG_BK_PRIOR ** 2
    return F


def covariance(F):
    return np.linalg.inv(F)


def correlations(C):
    d = np.sqrt(np.diag(C))
    R = C / np.outer(d, d)
    return R


# ──────────────────────────────────────────────────────────────────────
# 7. Evaluate
# ──────────────────────────────────────────────────────────────────────
results = {}
for combo in COMBOS:
    F = fisher(combo, include_priors=True)
    C = covariance(F)
    R = correlations(C)
    sig_eps_marg = np.sqrt(C[0, 0])
    # Fixed-bias Fisher: only ε direction
    F_fix = np.zeros_like(F); F_fix[0, 0] = F[0, 0]
    sig_eps_fix = 1.0 / np.sqrt(F[0, 0])
    degr = sig_eps_marg / sig_eps_fix
    results[combo] = {
        "F": F.tolist(),
        "C": C.tolist(),
        "rho_eps_b0": float(R[0, 1]),
        "rho_eps_bk": float(R[0, 2]),
        "sigma_eps_marg": float(sig_eps_marg),
        "sigma_eps_fix":  float(sig_eps_fix),
        "degradation": float(degr),
        "sn_marg_at_fid":  float(EPS_FID / sig_eps_marg),
        "sn_fix_at_fid":   float(EPS_FID / sig_eps_fix),
        "eps0_sn1_marg":   float(sig_eps_marg),
        "eps0_sn1_fix":    float(sig_eps_fix),
    }
    print(f"\n=== {combo} ===")
    print(f"  ρ(ε0,b0) = {R[0,1]:+.3f}   ρ(ε0,bk) = {R[0,2]:+.3f}")
    print(f"  σ(ε0) fix-bias = {sig_eps_fix:.4f}")
    print(f"  σ(ε0) marg     = {sig_eps_marg:.4f}")
    print(f"  degradation    = {degr:.2f}×")
    print(f"  S/N@ε0=0.02 marg = {EPS_FID/sig_eps_marg:.2f}   "
          f"fix = {EPS_FID/sig_eps_fix:.2f}")


# ──────────────────────────────────────────────────────────────────────
# 8. ε_0 sweep  S/N(ε_0) ∈ [0.005, 0.05]
# ──────────────────────────────────────────────────────────────────────
eps_sweep = np.linspace(0.005, 0.05, 46)
sweep = {}
for combo, r in results.items():
    sn_marg = eps_sweep / r["sigma_eps_marg"]
    sn_fix = eps_sweep / r["sigma_eps_fix"]
    sweep[combo] = {
        "eps0": eps_sweep.tolist(),
        "sn_marg": sn_marg.tolist(),
        "sn_fix": sn_fix.tolist(),
    }


# ──────────────────────────────────────────────────────────────────────
# 9. Verdict
# ──────────────────────────────────────────────────────────────────────
# Take the larger |ρ| over the two bias parameters, DR3+Euclid combo
R_DR3E = np.array(results["DR3+Euclid"]["C"])
R_corr = correlations(R_DR3E)
rho_max = max(abs(R_corr[0, 1]), abs(R_corr[0, 2]))
if rho_max < 0.5:
    verdict = "ORTHOGONAL"
elif rho_max < 0.9:
    verdict = "MIXED"
else:
    verdict = "DEGENERATE"

impact = {
    "ORTHOGONAL": "confirms D18 — JCAP falsifier viable",
    "MIXED":      "degrades D18 — S/N reduced by the degradation factor",
    "DEGENERATE": "overrides D18 — pivot to JHEP-fallback",
}[verdict]
print(f"\nVERDICT: {verdict}   (max |ρ| = {rho_max:.3f})")
print(f"Impact on D18: {impact}")


# ──────────────────────────────────────────────────────────────────────
# 10. Figure — 2-panel: (ε_0, b_0) contour + S/N sweep
# ──────────────────────────────────────────────────────────────────────
fig = plt.figure(figsize=(11.5, 4.6))
gs = gridspec.GridSpec(1, 2, wspace=0.28)


def ellipse_xy(C2, center, nsig=1.0, npts=200):
    """2σ ellipse pts from 2×2 covariance."""
    vals, vecs = np.linalg.eigh(C2)
    t = np.linspace(0, 2 * np.pi, npts)
    circ = np.vstack([np.sqrt(vals[0]) * np.cos(t),
                      np.sqrt(vals[1]) * np.sin(t)])
    xy = vecs @ circ * nsig
    return xy[0] + center[0], xy[1] + center[1]


# (a) 2D posterior in (ε_0, b_0_shift)
ax = fig.add_subplot(gs[0, 0])
for combo, color in [("DR3", "tab:blue"), ("DR3+Euclid", "tab:red")]:
    C = np.array(results[combo]["C"])
    C2 = C[np.ix_([0, 1], [0, 1])]
    for ns, alpha_f in [(1.0, 0.35), (2.0, 0.15)]:
        x, y = ellipse_xy(C2, (EPS_FID, 0.0), nsig=ns)
        ax.fill(x, y, color=color, alpha=alpha_f,
                label=f"{combo} {int(ns)}σ" if ns == 1.0 else None)
ax.axvline(EPS_FID, color="k", ls="--", lw=0.8, label="ε0 fid = 0.02")
ax.axhline(0.0, color="k", ls=":", lw=0.6)
ax.axvline(0.0, color="gray", ls=":", lw=0.6)
ax.set_xlabel(r"$\varepsilon_0$")
ax.set_ylabel(r"$\delta b_0$")
ax.set_title(r"(a) joint posterior  (ε$_0$, δb$_0$)")
ax.grid(alpha=0.3); ax.legend(fontsize=8, loc="upper right")
# Annotate correlation
r01 = results["DR3+Euclid"]["rho_eps_b0"]
ax.text(0.02, 0.95, fr"$\rho(\varepsilon_0,\,b_0)_{{DR3+E}} = {r01:+.3f}$",
        transform=ax.transAxes, fontsize=9, va="top",
        bbox=dict(boxstyle="round", fc="white", alpha=0.8))

# (b) S/N(ε_0) sweep
ax = fig.add_subplot(gs[0, 1])
for combo, color in [("DR3", "tab:blue"), ("DR3+Euclid", "tab:red")]:
    sw = sweep[combo]
    ax.plot(sw["eps0"], sw["sn_marg"], color=color, lw=1.6,
            label=f"{combo} (marg)")
    ax.plot(sw["eps0"], sw["sn_fix"],  color=color, lw=1.0, ls="--",
            label=f"{combo} (fix-bias)")
ax.axhline(1.0, color="k", ls="--", lw=0.8)
ax.axhline(0.5, color="gray", ls=":", lw=0.8)
ax.axvline(EPS_FID, color="r", ls=":", lw=0.8)
ax.set_xlabel(r"$\varepsilon_0$"); ax.set_ylabel("S/N")
ax.set_title("(b) S/N(ε$_0$) — marginalised vs fixed-bias")
ax.grid(alpha=0.3); ax.legend(fontsize=8, loc="upper left")
ax.set_xlim(0.005, 0.05)

fig.suptitle("D18b — ECI v6 falsifier vs ELG bias nuisance "
             f"(verdict: {verdict}, max|ρ|={rho_max:.2f})",
             fontsize=12, y=1.02)

outpdf = FIG / "D18b-bias-orthogonality.pdf"
fig.savefig(outpdf, bbox_inches="tight")
fig.savefig(FIG / "D18b-bias-orthogonality.png", dpi=130, bbox_inches="tight")
plt.close(fig)
print(f"\nWrote {outpdf}")


# ──────────────────────────────────────────────────────────────────────
# 11. Summary JSON
# ──────────────────────────────────────────────────────────────────────
summary = {
    "fiducial": {
        "eps0": EPS_FID, "alpha": ALPHA_FID, "gamma": GAMMA_FID,
        "k_eff_hMpc": K_EFF, "b_k_fid": BK_FID,
        "prior_sigma_b0": SIG_B0_PRIOR, "prior_sigma_bk": SIG_BK_PRIOR,
    },
    "results": {c: {k: v for k, v in r.items() if k not in ("F", "C")}
                for c, r in results.items()},
    "sweep": sweep,
    "rho_max_DR3_Euclid": float(rho_max),
    "verdict": verdict,
    "impact_on_D18": impact,
    "notes": [
        "Bias model: b(z,k)=b0(z)+bk·k² evaluated at k_eff=0.12 h/Mpc.",
        "Leakage of δb into fσ_8 via L(z)=1/(b0(z)+f(z)/3).",
        "Gaussian priors σ(b0)=0.5, σ(bk)=2 h^-2 Mpc^2 (loose, conservative).",
        "Analytic scale argument: Θ(PH_2) is a sharp activator in k at k_*~0.15; "
        "polynomial b(k) is smooth → weak k-projection overlap.",
    ],
}
with open(RES / "D18b-summary.json", "w") as f:
    json.dump(summary, f, indent=2)
print(f"Wrote {RES / 'D18b-summary.json'}")
