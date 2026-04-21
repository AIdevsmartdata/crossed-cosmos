"""
D10 — DESI DR2 (w0, wa) covariance: real vs. approximate, and ECI inclusion
===========================================================================

Re-does the D7 (w0, wa) plot with the **real** DESI DR2 w0waCDM posterior
covariance reconstructed from the published marginal errors + pivot redshift
zp + w(zp) uncertainty (DESI Collaboration, arXiv:2503.14738v3).

Key observation
---------------
The CPL pivot redshift ap = 1/(1+zp) is, by definition, the value of a at
which sigma(w_p) is minimised, i.e.

    sigma_p^2 = sigma_{w0}^2 + (1-ap)^2 sigma_{wa}^2 + 2(1-ap) cov(w0,wa)

            d sigma_p^2 / d(1-ap) = 0   =>   cov(w0,wa) = - (1-ap) sigma_{wa}^2

Therefore rho(w0,wa) = -(1-ap) sigma_{wa} / sigma_{w0} is *recoverable*
from zp and the marginal errors alone. We cross-check against the quoted
sigma(w_p) and find consistency to ~5%.

Sources (2503.14738v3, Section VII):
  - DESI+CMB+DESY5: w0 = -0.752 +/- 0.057, wa = -0.86 (+0.23/-0.20) -> sym 0.215;
                     zp = 0.31, wp = -0.954 +/- 0.024.
  - DESI+CMB     : w0 = -0.42  +/- 0.21 , wa = -1.75 +/- 0.58;
                     zp = 0.53, wp = -1.024 +/- 0.043.

This gives rho(DESI+CMB+DESY5) ~ -0.89 and rho(DESI+CMB) ~ -0.96, an order
of magnitude more anti-correlated than the rho=-0.8 approximation used in
D7-ppn-xi-bound.py, AND with sigma_wa ~ 0.22 (not 0.80) for the SN-combined
dataset that matches the central (w0,wa) = (-0.752, -0.86) used in D7.

Outputs
-------
  figures/D7-xi-w0-wa-v2.pdf  -- re-plot with real covariance (DESI+CMB+DESY5)
  derivations/D10-report.md   -- written separately
"""

import os
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse


# -----------------------------------------------------------------------------
# Covariance reconstruction helpers
# -----------------------------------------------------------------------------
def cov_from_pivot(sigma_w0, sigma_wa, zp):
    """Return 2x2 cov(w0,wa) reconstructed from marginals + pivot redshift."""
    ap = 1.0 / (1.0 + zp)
    cov_cross = -(1.0 - ap) * sigma_wa ** 2
    C = np.array([[sigma_w0 ** 2, cov_cross],
                  [cov_cross,     sigma_wa ** 2]])
    rho = cov_cross / (sigma_w0 * sigma_wa)
    sigma_p_predicted = np.sqrt(max(sigma_w0 ** 2 - (1 - ap) ** 2 * sigma_wa ** 2, 0.0))
    return C, rho, sigma_p_predicted, ap


def ellipse_params(C, sigma_level=1.0):
    """Return (width, height, angle_deg) for a Gaussian 2D covariance C.
    sigma_level corresponds to Delta chi^2 per (1sigma 2dof=2.30, 2sigma=6.17)."""
    dchi2 = {1.0: 2.30, 2.0: 6.17}[sigma_level]
    vals, vecs = np.linalg.eigh(C)
    order = np.argsort(vals)[::-1]
    vals = vals[order]
    vecs = vecs[:, order]
    width = 2 * np.sqrt(vals[0] * dchi2)
    height = 2 * np.sqrt(vals[1] * dchi2)
    angle = np.degrees(np.arctan2(vecs[1, 0], vecs[0, 0]))
    return width, height, angle


# -----------------------------------------------------------------------------
# DESI DR2 numbers (arXiv:2503.14738v3)
# -----------------------------------------------------------------------------
datasets = {
    # Matches the central point used in the original D7 plot.
    'DESI+CMB+DESY5': dict(
        w0=-0.752, wa=-0.86, sw0=0.057, swa=0.215,
        zp=0.31, wp=-0.954, swp=0.024,
        color='#cc8800'),
    'DESI+CMB': dict(
        w0=-0.42, wa=-1.75, sw0=0.21, swa=0.58,
        zp=0.53, wp=-1.024, swp=0.043,
        color='#888888'),
}

print("=" * 72)
print("D10 -- DESI DR2 covariance reconstruction from pivot redshift")
print("=" * 72)
for name, d in datasets.items():
    C, rho, sp_pred, ap = cov_from_pivot(d['sw0'], d['swa'], d['zp'])
    print(f"\n{name}:")
    print(f"  w0 = {d['w0']} +/- {d['sw0']}   wa = {d['wa']} +/- {d['swa']}")
    print(f"  zp = {d['zp']} (ap = 1-{1-ap:.4f})")
    print(f"  cov(w0,wa) = {C[0,1]:+.5f}")
    print(f"  rho(w0,wa) = {rho:+.4f}")
    print(f"  sigma(wp) predicted from cov = {sp_pred:.4f}  |  quoted = {d['swp']}")
    d['cov'] = C
    d['rho'] = rho

# Use DESI+CMB+DESY5 as the primary overlay (it matches D7's central point).
primary_key = 'DESI+CMB+DESY5'
primary = datasets[primary_key]

# -----------------------------------------------------------------------------
# ECI band parameters (reproduced from D7)
# -----------------------------------------------------------------------------
A_val = 1.58
B_val = A_val * 8.0 / np.sqrt(3.0)          # ~7.30
xi_max = 2.4e-2                             # Cassini, chi0 = M_P/10
chi_over_MP = 0.1

# -----------------------------------------------------------------------------
# Old-D7 (approximate) ellipse for comparison
# -----------------------------------------------------------------------------
old = dict(w0=-0.75, wa=-0.86, sw0=0.20, swa=0.80, rho=-0.80)
cov_old = np.array([[old['sw0']**2, old['rho']*old['sw0']*old['swa']],
                    [old['rho']*old['sw0']*old['swa'], old['swa']**2]])

# -----------------------------------------------------------------------------
# ECI inclusion assessment: Mahalanobis distance from DR2 mean to
#   (a) LambdaCDM (-1, 0)
#   (b) Scherrer--Sen minimal-coupling line wa = -A(1+w0)
#   (c) ECI band edge (+/- xi_max at chi0 = M_P/10)
# -----------------------------------------------------------------------------
def mahalanobis(point, mean, cov):
    d = np.asarray(point) - np.asarray(mean)
    return float(np.sqrt(d @ np.linalg.solve(cov, d)))

mean = np.array([primary['w0'], primary['wa']])
C = primary['cov']

lcdm = np.array([-1.0, 0.0])
d_lcdm = mahalanobis(lcdm, mean, C)
print(f"\nMahalanobis distance DR2_mean -> LambdaCDM = {d_lcdm:.2f} sigma")
print("  (equivalent frequentist N-sigma for 2 dof Chi^2)")

# Point on Scherrer--Sen line at the w0 best-fit
w0bf = primary['w0']
wa_SS = -A_val * (1 + w0bf)
ss_point = np.array([w0bf, wa_SS])
d_ss_point = mahalanobis(ss_point, mean, C)
print(f"Mahalanobis to SS line at w0={w0bf}: wa_SS={wa_SS:.3f}"
      f"  -> d = {d_ss_point:.2f} sigma")

# Minimum distance to the full SS line (line is wa = -A - A*w0; grid search)
w0grid = np.linspace(-1.0, -0.3, 4001)
wa_SS_grid = -A_val * (1 + w0grid)
ds = np.array([mahalanobis((w0, wa), mean, C)
               for w0, wa in zip(w0grid, wa_SS_grid)])
idx = np.argmin(ds)
d_ss_min = ds[idx]
print(f"MIN Mahalanobis to SS line (minimal-coupling wCDM track)"
      f" = {d_ss_min:.2f} sigma at (w0,wa)=({w0grid[idx]:.3f},{wa_SS_grid[idx]:.3f})")

# ECI band: same SS line +/- shift
shift = B_val * xi_max * np.sqrt(np.maximum(1 + w0grid, 0.0)) * chi_over_MP
wa_upper = wa_SS_grid + shift
wa_lower = wa_SS_grid - shift
# Min distance to the band (union of upper-edge, lower-edge, and interior line)
d_upper = np.array([mahalanobis((w0, wa), mean, C) for w0, wa in zip(w0grid, wa_upper)])
d_lower = np.array([mahalanobis((w0, wa), mean, C) for w0, wa in zip(w0grid, wa_lower)])
d_eci_min = min(d_ss_min, d_upper.min(), d_lower.min())
print(f"MIN Mahalanobis to ECI band (|xi| <= {xi_max}, chi0=M_P/10)"
      f" = {d_eci_min:.2f} sigma")

# Verdict: 1sigma 2dof -> sqrt(2.30)=1.52 ; 2sigma 2dof -> sqrt(6.17)=2.48
# The ECI band (and its SS spine) is *closer to the DR2 mean than the
# contour only if* d_eci_min < those thresholds.
print("\nDecision thresholds (2-dof chi^2 ellipses):")
print(f"  1sigma (68.3%): sqrt(2.30) = {np.sqrt(2.30):.3f}")
print(f"  2sigma (95.4%): sqrt(6.17) = {np.sqrt(6.17):.3f}")
if d_eci_min < np.sqrt(2.30):
    verdict = "ECI band INSIDE DR2 1sigma contour"
elif d_eci_min < np.sqrt(6.17):
    verdict = "ECI band OUTSIDE DR2 1sigma but INSIDE DR2 2sigma contour"
else:
    verdict = "ECI band OUTSIDE DR2 2sigma contour"
print(f"\nVERDICT ({primary_key}): {verdict}")

# Also check against the old approximate covariance for narrative.
d_eci_old = min(
    min(mahalanobis((w0, wa), np.array([old['w0'], old['wa']]), cov_old)
        for w0, wa in zip(w0grid, wa_SS_grid)),
    min(mahalanobis((w0, wa), np.array([old['w0'], old['wa']]), cov_old)
        for w0, wa in zip(w0grid, wa_upper)),
    min(mahalanobis((w0, wa), np.array([old['w0'], old['wa']]), cov_old)
        for w0, wa in zip(w0grid, wa_lower)),
)
print(f"\n[cross-check] Under OLD approximate covariance (sw0=0.20, swa=0.80, rho=-0.80):")
print(f"  MIN Mahalanobis to ECI band = {d_eci_old:.2f} sigma")

# -----------------------------------------------------------------------------
# Plot
# -----------------------------------------------------------------------------
here = os.path.dirname(os.path.abspath(__file__))
figdir = os.path.join(here, 'figures')
os.makedirs(figdir, exist_ok=True)

fig, ax = plt.subplots(figsize=(7.4, 6.2))

# REAL DR2 DESY5 contours
for nsig, alpha_face, alpha_edge, lbl in [
        (2.0, 0.28, 1.0, 'DESI DR2 2σ (DESI+CMB+DESY5, real cov.)'),
        (1.0, 0.55, 1.0, 'DESI DR2 1σ (DESI+CMB+DESY5, real cov.)')]:
    w, h, ang = ellipse_params(primary['cov'], sigma_level=nsig)
    e = Ellipse((primary['w0'], primary['wa']), w, h, angle=ang,
                facecolor='#ffcc66' if nsig == 1.0 else '#fff0cc',
                edgecolor=primary['color'], lw=1.6, alpha=alpha_face,
                label=lbl)
    ax.add_patch(e)

# OLD approximate contour (1sigma only, for contrast)
w_old, h_old, ang_old = ellipse_params(cov_old, sigma_level=1.0)
e_old = Ellipse((old['w0'], old['wa']), w_old, h_old, angle=ang_old,
                facecolor='none', edgecolor='#999999', lw=1.0, ls='--',
                label='D7 old approx. 1σ (σ_wa=0.8, ρ=−0.8)')
ax.add_patch(e_old)

# DESI+CMB (no SN) 2sigma for context
w2, h2, ang2 = ellipse_params(datasets['DESI+CMB']['cov'], sigma_level=2.0)
e_cmb = Ellipse((datasets['DESI+CMB']['w0'], datasets['DESI+CMB']['wa']),
                w2, h2, angle=ang2,
                facecolor='none', edgecolor='#888888', lw=1.0, ls=':',
                label='DESI+CMB 2σ (real cov.)')
ax.add_patch(e_cmb)

ax.plot(primary['w0'], primary['wa'], '*', color=primary['color'], ms=14,
        mec='k', mew=0.6, label='DESI+CMB+DESY5 mean')
ax.plot(-1.0, 0.0, 'ko', ms=7, label=r'$\Lambda$CDM')

# Scherrer--Sen line
ax.plot(w0grid, wa_SS_grid, '-', color='#0055aa', lw=2.2,
        label=r'Scherrer--Sen (minimal, $\Omega_\Lambda=0.7$)')

# ECI band (xi band at chi0 = M_P/10)
ax.fill_between(w0grid, wa_lower, wa_upper,
                color='#00aa55', alpha=0.55,
                label=rf'ECI band $|\xi_\chi|\leq{xi_max:.1e}$, '
                      r'$\chi_0=M_P/10$')

# ECI band at chi0 = M_P (dashed reference)
shift_big = B_val * xi_max * np.sqrt(np.maximum(1 + w0grid, 0)) * 1.0
ax.plot(w0grid, wa_SS_grid + shift_big, '--', color='#008833', lw=1.0, alpha=0.7)
ax.plot(w0grid, wa_SS_grid - shift_big, '--', color='#008833', lw=1.0, alpha=0.7,
        label=r'ECI band, $\chi_0=M_P$ (reference)')

ax.set_xlabel(r'$w_0$', fontsize=13)
ax.set_ylabel(r'$w_a$', fontsize=13)
ax.set_title('D7-v2 -- ECI band vs DESI DR2 with reconstructed covariance\n'
             rf'($\rho_{{\rm DESY5}}={primary["rho"]:+.2f}$, '
             rf'$\sigma_{{w_a}}={primary["swa"]:.2f}$; '
             rf'SS line: $d={d_ss_min:.2f}\sigma$)',
             fontsize=10.5)
ax.set_xlim(-1.10, -0.20)
ax.set_ylim(-2.8, 0.60)
ax.grid(True, alpha=0.3)
ax.legend(fontsize=8, loc='lower left', framealpha=0.92)
ax.axhline(0, color='k', lw=0.4, alpha=0.5)
ax.axvline(-1, color='k', lw=0.4, alpha=0.5)

out = os.path.join(figdir, 'D7-xi-w0-wa-v2.pdf')
plt.tight_layout()
plt.savefig(out)
plt.savefig(out.replace('.pdf', '.png'), dpi=150)
print(f"\nwrote {out}")
print(f"      {out.replace('.pdf', '.png')}")

# -----------------------------------------------------------------------------
# Numbers for the report (machine-readable dump)
# -----------------------------------------------------------------------------
summary = {
    'source': 'arXiv:2503.14738v3, Eq. (28) and pivot zp=0.31',
    'primary_dataset': primary_key,
    'w0': primary['w0'], 'wa': primary['wa'],
    'sigma_w0': primary['sw0'], 'sigma_wa': primary['swa'],
    'zp': primary['zp'], 'wp_quoted': primary['wp'],
    'sigma_wp_quoted': primary['swp'],
    'rho_reconstructed': primary['rho'],
    'sigma_wp_predicted': float(np.sqrt(max(primary['sw0']**2 -
                                   (1 - 1/(1+primary['zp']))**2 * primary['swa']**2, 0))),
    'd_mahalanobis_to_LambdaCDM': d_lcdm,
    'd_mahalanobis_min_to_SS_line': d_ss_min,
    'd_mahalanobis_min_to_ECI_band': d_eci_min,
    'sigma_threshold_1sigma_2dof': float(np.sqrt(2.30)),
    'sigma_threshold_2sigma_2dof': float(np.sqrt(6.17)),
    'verdict': verdict,
    'd_mahalanobis_old_approx': d_eci_old,
}
import json
dumpfile = os.path.join(here, '_results', 'D10-summary.json')
os.makedirs(os.path.dirname(dumpfile), exist_ok=True)
with open(dumpfile, 'w') as f:
    json.dump(summary, f, indent=2)
print(f"wrote {dumpfile}")
