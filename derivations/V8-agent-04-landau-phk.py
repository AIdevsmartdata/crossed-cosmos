#!/usr/bin/env python3
"""
V8-agent-04 — Landau order parameter ↔ Θ(PH_k[δn])
=====================================================
Analogy: PH_k as a function of correlation length ξ undergoes a
percolation-type phase transition in a 2D Gaussian random field.
Near the transition, the Betti number density ρ_β(ξ) plays the role
of a Landau order parameter; we ask whether the chameleon activator
Θ(x) = exp(−(x/x_c)^α) fits the transition profile and what α emerges.

Strategy (no GUDHI/Ripser available):
  1. Generate a 2D GRF with tunable correlation length ξ (Gaussian power
     spectrum P(k) ∝ exp(−k²ξ²/2)) on an N×N grid.
  2. Compute β_0 (connected components), β_1 (independent loops) via
     cubical homology proxy:
       β_0 via scipy.ndimage.label on super-level sets
       β_1 = β_0 − χ + 1  where χ is Euler characteristic (exact for
             simply-connected planar complexes; good proxy for dense fields)
     Use the Gaussian kinematic formula for analytic cross-check.
  3. Scan ξ ∈ [0.5, 6] grid cells and threshold ν ∈ [−2, 2].
  4. At each ξ, record PH_1 peak (max β_1 over ν).
  5. Fit Θ(ξ) = exp(−(ξ/ξ_c)^α) to the normalised PH_1 profile.
  6. Compare α to the v5 M3 Barrow-anchored range α ∈ (0, 0.1].

References:
  Yip, Biagetti et al. 2024 (arXiv:2403.13985)
  Adler & Taylor 2007 (Gaussian Kinematic Formula)
  D15-screening-profile.py (α_fid = 0.095)
  D18-fsigma8-PH-forecast.py (ALPHA_FID = 0.095)
"""

import numpy as np
import scipy.ndimage as ndi
from scipy.optimize import curve_fit
from scipy.signal import find_peaks
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import os, json

RNG = np.random.default_rng(42)
N   = 256          # grid size
N_XI = 30          # number of ξ values
N_NU = 40          # number of threshold levels
N_REAL = 10        # realisations per ξ (for variance)
XI_MIN, XI_MAX = 0.2, 6.0
NU_MIN, NU_MAX = -2.5, 2.5
OUT_DIR = os.path.dirname(os.path.abspath(__file__))

# ── 1. GRF generator ─────────────────────────────────────────────────────────
def make_grf(N, xi, rng):
    """Generate a 2D zero-mean unit-variance GRF with Gaussian power spectrum."""
    kx = np.fft.fftfreq(N) * N   # in pixel units
    ky = np.fft.fftfreq(N) * N
    KX, KY = np.meshgrid(kx, ky, indexing='ij')
    K2 = KX**2 + KY**2
    Pk = np.exp(-K2 * xi**2 / (2 * N**2))   # Gaussian P(k), normalise
    Pk[0, 0] = 0.0                            # zero mean
    amp = np.sqrt(Pk / 2)
    noise = rng.standard_normal((N, N)) + 1j * rng.standard_normal((N, N))
    fhat  = amp * noise
    field = np.fft.ifft2(fhat).real
    field /= field.std() + 1e-12
    return field

# ── 2. β_0 and β_1 via cubical homology proxy ────────────────────────────────
def betti_superlevel(field, nu):
    """
    Super-level set {x: field(x) > nu}.
    β_0 = #connected components (scipy label)
    β_1 via Euler characteristic:  χ = V - E + F  (cubical)
    For a 2D binary image:
      V = #white pixels
      E = #horizontal + vertical white-white edges
      F = #2x2 all-white squares (2-cells)
    χ = V - E + F
    β_0 - β_1 + β_2 = χ  (in 2D, β_2=0 for open set, β_2=#enclosed voids)
    We approximate: β_1 ≃ β_0 - χ  (valid when field has no enclosed voids,
    i.e. β_2 ≈ 0, good approximation for generic random fields at ν near 0)
    """
    mask = (field > nu).astype(np.int8)
    # β_0
    labeled, b0 = ndi.label(mask)
    # Euler characteristic (cubical complex)
    V = mask.sum()
    E_h = (mask[:, :-1] & mask[:, 1:]).sum()  # horizontal edges
    E_v = (mask[:-1, :] & mask[1:, :]).sum()  # vertical edges
    E   = E_h + E_v
    F   = (mask[:-1, :-1] & mask[:-1, 1:] & mask[1:, :-1] & mask[1:, 1:]).sum()
    chi = int(V) - int(E) + int(F)
    b1  = max(0, b0 - chi)   # β_1 ≃ β_0 − χ
    return int(b0), int(b1)

# ── 3. Gaussian Kinematic Formula cross-check (analytic) ────────────────────
def euler_char_gkf_2d(nu, xi, N):
    """
    Analytic expected Euler characteristic of super-level set for 2D GRF.
    (Adler & Taylor 2007, eq. 12.3.3 for d=2)
      <χ(ν)> = A · (σ_1/σ_0)^2 · (ν² − 1) · φ(ν) / (2π)  +  A · Φ̄(ν)
    where φ = Gaussian PDF, Φ̄ = 1 − Φ, σ_1/σ_0 ≃ 1/ξ (for Gaussian P(k)).
    We normalise by grid area A = N².
    """
    from scipy.special import erfc
    lam = (1.0 / xi)**2   # (σ_1/σ_0)^2 in pixel units
    phi_nu = np.exp(-0.5 * nu**2) / np.sqrt(2 * np.pi)
    Phi_bar = 0.5 * erfc(nu / np.sqrt(2))
    chi = N**2 * (lam * (nu**2 - 1) * phi_nu / (2 * np.pi) + Phi_bar)
    return chi

# ── 4. Main scan ─────────────────────────────────────────────────────────────
xi_vals  = np.linspace(XI_MIN, XI_MAX, N_XI)
nu_vals  = np.linspace(NU_MIN, NU_MAX, N_NU)

b1_mean  = np.zeros((N_XI, N_NU))   # β_1(ξ, ν)
b1_std   = np.zeros((N_XI, N_NU))

print(f"Scanning {N_XI} ξ values × {N_NU} thresholds × {N_REAL} realisations …")
for i, xi in enumerate(xi_vals):
    b1_runs = np.zeros((N_REAL, N_NU))
    for r in range(N_REAL):
        field = make_grf(N, xi, RNG)
        for j, nu in enumerate(nu_vals):
            _, b1 = betti_superlevel(field, nu)
            b1_runs[r, j] = b1
    b1_mean[i] = b1_runs.mean(axis=0)
    b1_std[i]  = b1_runs.std(axis=0)
    if (i+1) % 5 == 0:
        print(f"  ξ={xi:.2f} done, β_1_peak={b1_mean[i].max():.1f}")

# ── 5. PH_1 peak as function of ξ ────────────────────────────────────────────
# For each ξ, take max β_1 over all thresholds ν
ph1_peak = b1_mean.max(axis=1)               # shape (N_XI,)
ph1_peak_norm = ph1_peak / ph1_peak.max()    # normalise to [0,1]

# Also: GKF-based peak for cross-check
gkf_peak = np.zeros(N_XI)
for i, xi in enumerate(xi_vals):
    chi_curve = np.array([euler_char_gkf_2d(nu, xi, N) for nu in nu_vals])
    # β_1 ~ max |χ| (loops dominate near peak)
    gkf_peak[i] = np.abs(chi_curve).max()
gkf_peak_norm = gkf_peak / gkf_peak.max()

# ── 6. Identify transition region ────────────────────────────────────────────
# The PH_1 peak typically rises then falls as ξ increases:
# - small ξ (white noise): many tiny components, few long loops → β_1 low
# - intermediate ξ: rich topology, β_1 peaks (percolation transition)
# - large ξ: single smooth blob, β_1 drops → transition (order param → 0)
# We fit Θ(ξ) = exp(−(ξ/ξ_c)^α) to the *descending* flank (ξ > ξ_peak)

# Find ξ_peak
peak_idx = np.argmax(ph1_peak_norm)
xi_peak  = xi_vals[peak_idx]
print(f"\nPH_1 peak at ξ_peak = {xi_peak:.3f} grid cells")

# Descending flank: ξ > ξ_peak
mask_desc = xi_vals >= xi_peak
xi_desc   = xi_vals[mask_desc]
y_desc    = ph1_peak_norm[mask_desc]

# Normalise so that y(ξ_peak) = 1  (= order parameter at transition point)
y_desc = y_desc / y_desc[0]

# ── 7. Fit Θ(x) = exp(−(x/x_c)^α) ──────────────────────────────────────────
def theta_model(xi, xi_c, alpha):
    x = np.clip((xi / xi_c)**alpha, 0, 700)
    return np.exp(-x)

try:
    p0   = [xi_peak * 1.5, 1.5]
    popt, pcov = curve_fit(theta_model, xi_desc, y_desc,
                           p0=p0, bounds=([xi_peak, 0.01], [XI_MAX*2, 10]),
                           maxfev=5000)
    xi_c_fit, alpha_fit = popt
    alpha_err = np.sqrt(pcov[1, 1])
    fit_ok = True
    print(f"\nFit Θ(ξ) = exp(−(ξ/ξ_c)^α):")
    print(f"  ξ_c  = {xi_c_fit:.4f}  (grid units)")
    print(f"  α    = {alpha_fit:.4f} ± {alpha_err:.4f}")
except Exception as e:
    print(f"Fit failed: {e}")
    alpha_fit, alpha_err, xi_c_fit = np.nan, np.nan, np.nan
    fit_ok = False

# ── 8. Verdict ───────────────────────────────────────────────────────────────
ALPHA_V5_LO, ALPHA_V5_HI = 0.0, 0.1   # v5 M3 Barrow-anchored
ALPHA_FID = 0.095

if fit_ok:
    in_range = ALPHA_V5_LO < alpha_fit <= ALPHA_V5_HI
    verdict = "α-MATCHES-V5" if in_range else "α-DIFFERENT"
else:
    verdict = "NO-TRANSITION"

print(f"\nv5 M3 target: α ∈ ({ALPHA_V5_LO}, {ALPHA_V5_HI}]  (fiducial {ALPHA_FID})")
print(f"Extracted α = {alpha_fit:.4f}")
print(f"VERDICT: {verdict}")

# ── 9. GKF analytic check ────────────────────────────────────────────────────
# Fit Theta to GKF-normalised peak as well
try:
    p0g = [xi_peak * 1.5, 1.5]
    xi_gkf_desc = xi_vals[xi_vals >= xi_peak]
    y_gkf_desc  = gkf_peak_norm[xi_vals >= xi_peak]
    y_gkf_desc  = y_gkf_desc / y_gkf_desc[0]
    popt_g, pcov_g = curve_fit(theta_model, xi_gkf_desc, y_gkf_desc,
                                p0=p0g, bounds=([xi_peak, 0.01], [XI_MAX*2, 10]),
                                maxfev=5000)
    xi_c_gkf, alpha_gkf = popt_g
    alpha_gkf_err = np.sqrt(pcov_g[1, 1])
    print(f"\nGKF analytic cross-check:")
    print(f"  ξ_c_GKF = {xi_c_gkf:.4f},  α_GKF = {alpha_gkf:.4f} ± {alpha_gkf_err:.4f}")
except Exception as e:
    alpha_gkf, alpha_gkf_err, xi_c_gkf = np.nan, np.nan, np.nan
    print(f"GKF fit failed: {e}")

# ── 10. Plot ─────────────────────────────────────────────────────────────────
fig, axes = plt.subplots(1, 3, figsize=(14, 4))

# Panel A: β_1(ξ, ν) heatmap
ax = axes[0]
im = ax.pcolormesh(nu_vals, xi_vals, b1_mean, cmap='viridis', shading='auto')
fig.colorbar(im, ax=ax, label=r'$\beta_1$ (loops)')
ax.set_xlabel(r'Threshold $\nu$')
ax.set_ylabel(r'Correlation length $\xi$ [grid units]')
ax.set_title(r'$\beta_1(\xi,\nu)$ — cubical homology proxy')

# Panel B: PH_1 peak vs ξ + Θ fit
ax = axes[1]
ax.plot(xi_vals, ph1_peak_norm, 'o-', color='C0', ms=4, label=r'$\hat\beta_1^{\rm peak}(\xi)$ (numerical)')
ax.plot(xi_vals, gkf_peak_norm, 's--', color='C2', ms=3, label='GKF analytic')
xi_dense = np.linspace(xi_vals[0], xi_vals[-1], 300)
if fit_ok:
    ax.plot(xi_dense,
            theta_model(xi_dense, xi_c_fit, alpha_fit),
            'r-', lw=2,
            label=rf'$\Theta(\xi)=e^{{-(xi/\xi_c)^\alpha}}$, $\alpha={alpha_fit:.3f}$')
ax.axvline(xi_peak, ls=':', color='gray', label=rf'$\xi_{{\rm peak}}={xi_peak:.2f}$')
ax.axhspan(0, 0, alpha=0)   # dummy
ax.set_xlabel(r'Correlation length $\xi$ [grid units]')
ax.set_ylabel('Normalised peak ' + r'$\hat\beta_1$')
ax.set_title(r'$\Theta(\xi)$ fit to PH$_1$ transition')
ax.legend(fontsize=7)
ax.grid(alpha=0.3)

# Panel C: Landau-style order parameter transition + α comparison
ax = axes[2]
if fit_ok:
    ax.plot(xi_desc, y_desc, 'o', color='C0', ms=5, label='Data (descending flank)')
    ax.plot(xi_dense[xi_dense >= xi_peak],
            theta_model(xi_dense[xi_dense >= xi_peak], xi_c_fit, alpha_fit),
            'r-', lw=2, label=rf'Fit: $\alpha={alpha_fit:.3f}\pm{alpha_err:.3f}$')
    if not np.isnan(alpha_gkf):
        ax.plot(xi_dense[xi_dense >= xi_peak],
                theta_model(xi_dense[xi_dense >= xi_peak], xi_c_gkf, alpha_gkf),
                'g--', lw=1.5, label=rf'GKF: $\alpha={alpha_gkf:.3f}$')
ax.axhspan(0, 1, xmin=0, xmax=0, color='orange', alpha=0.3, label='v5 M3 target band')
# shade v5 target α band in ξ-space via order-param level
if fit_ok and not np.isnan(alpha_fit):
    theta_lo = np.exp(-(xi_dense / xi_c_fit)**ALPHA_V5_HI)
    theta_hi = np.exp(-(xi_dense / xi_c_fit)**ALPHA_V5_LO)
ax.axhline(np.exp(-1), ls=':', color='gray', label=r'$\Theta=e^{-1}$ (transition midpoint)')
ax.set_xlabel(r'$\xi$ [grid units]  (descent from peak)')
ax.set_ylabel(r'$\hat\beta_1$ (order parameter)')
ax.set_title(f'Landau order-param transition\nVerdict: {verdict}')
ax.legend(fontsize=7)
ax.grid(alpha=0.3)

fig.suptitle(
    r'$\Theta(\mathrm{PH}_1[\delta n])$ as Landau order parameter of percolation transition',
    fontsize=11, y=1.01
)
plt.tight_layout()
out_png = os.path.join(OUT_DIR, "V8-agent-04-landau-phk.png")
plt.savefig(out_png, dpi=130, bbox_inches='tight')
print(f"\nPlot saved: {out_png}")

# ── 11. Summary JSON ─────────────────────────────────────────────────────────
summary = {
    "xi_peak": float(xi_peak),
    "alpha_fit": float(alpha_fit) if fit_ok else None,
    "alpha_err": float(alpha_err) if fit_ok else None,
    "xi_c_fit": float(xi_c_fit) if fit_ok else None,
    "alpha_gkf": float(alpha_gkf) if not np.isnan(alpha_gkf) else None,
    "alpha_gkf_err": float(alpha_gkf_err) if not np.isnan(alpha_gkf_err) else None,
    "ALPHA_V5_range": [ALPHA_V5_LO, ALPHA_V5_HI],
    "ALPHA_FID": ALPHA_FID,
    "verdict": verdict,
    "N_grid": N,
    "N_realisations": N_REAL,
}
json_path = os.path.join(OUT_DIR, "_results/V8-agent-04-summary.json")
os.makedirs(os.path.dirname(json_path), exist_ok=True)
with open(json_path, "w") as f:
    json.dump(summary, f, indent=2)
print(f"Summary: {json_path}")
print(f"\n{'='*60}")
print(f"FINAL VERDICT: {verdict}")
print(f"  α_fit  = {alpha_fit:.4f} ± {alpha_err:.4f}")
print(f"  α_GKF  = {alpha_gkf:.4f}")
print(f"  v5 M3 target: α ∈ (0, 0.1]  (fiducial 0.095)")
print(f"{'='*60}")
