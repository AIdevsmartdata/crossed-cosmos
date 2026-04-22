#!/usr/bin/env python3
"""
V7 BK-fit: explicit Bogomolny-Keating 1996 2-point arithmetic correction
fit to the empirical residual R_2^emp(x) - R_2^GUE(x) measured on the first
10^5 Odlyzko Riemann zeros (see V7-test5-odlyzko.py).

Formula used.  We implement the Bogomolny-Keating (Nonlinearity 9, 1996,
"Random matrix theory and the Riemann zeros II") scaled two-point correction
in the form that is equivalent to Conrey-Snaith Theorem 4.3 (eq. 4.19 in
Snaith's review "Riemann zeros and random matrix theory", 2010) after
saddle-point evaluation of the r-integral around the mean level spacing.
The scaled two-point correlation at height T obeys

    R_2(x; T) = R_2^GUE(x) + Delta_BK(x; L),    L = log(T / 2 pi),

with the *arithmetic* piece

    Delta_BK(x; L) = (1 / (2 pi)^2) * d^2/dx^2  [ P(x; L) ]                (*)

    P(x; L) = -2 Re log zeta( 1 + 2 pi i x / L )

          ~  2 Re  Sum_p Sum_{k>=1}  (1/k) * p^{ -k - 2 pi i k x / L }

(this is the "off-diagonal" prime-pair contribution; derivation:
log zeta(1+s) = -Sum_p log(1 - p^{-1-s}) = Sum_{p,k} p^{-k(1+s)}/k.
The d^2/dx^2 brings down (log p)^2 (and k factors) and gives the standard
BK form).  The sign and (2 pi)^-2 prefactor agree with eq. (4.19) of
Conrey/Snaith (2007) / Snaith 2010 review when the bracket is expanded to
leading order near the mean level density.  See also Berry 1988, Keating
2005 "Random matrices and number theory" (Les Houches lectures), where the
same formula is reproduced.

Because several *equivalent* forms circulate in the literature (up to
overall amplitude conventions), we also fit a free prefactor A in front of
Delta_BK and an effective L_eff = log(T_eff / 2 pi).  A fit returning
A ~ 1, L_eff ~ L_measured = <log(gamma/2pi)>_{gamma in sample} confirms the
canonical BK.

Output.
  * prints chi^2 for: (GUE only), (GUE+BK, A=1 L fixed), (GUE+BK, A,L_eff
    free), (GUE+BK + extra free-phase Fourier residual term)
  * F-test / LRT between nested models
  * /home/remondiere/crossed-cosmos/derivations/V7-BK-fit.png  overlay
"""
from __future__ import annotations

from pathlib import Path

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from scipy.optimize import least_squares
from scipy.stats import chi2 as chi2_dist, f as f_dist

# ------------------------------------------------------------------
# 1.  Load data
# ------------------------------------------------------------------
CSV = Path("/tmp/V7-test5-residuals.csv")
data = np.loadtxt(CSV)
x, R2_emp, R2_GUE, resid, sigma = [data[:, k] for k in range(5)]
print(f"[data] loaded {len(x)} bins from {CSV}")

# mask x > 0.1  (same as test 5, dof=58)
mask = x > 0.1
xm, rm, sm = x[mask], resid[mask], sigma[mask]
dof_data = mask.sum()

# ------------------------------------------------------------------
# 2.  Effective height of sample
# ------------------------------------------------------------------
# Odlyzko zeros1: N=1e5, gamma_N ~ 74920.83.  The *mean* value of L over
# the sample (with log density weighting) is what enters the pair
# correlation.  Compute it directly.
ZEROS = Path("/tmp/odlyzko_zeros1.txt")
gammas = np.loadtxt(ZEROS)
L_arr = np.log(gammas / (2 * np.pi))
# pair correlation is a density weighted by #zeros per unit x, so the
# appropriate mean is just the arithmetic mean of log(gamma/2pi) (each
# zero contributes N_local ~ constant pairs in the scaled unfolding).
L_mean = L_arr.mean()
print(f"[height] N = {len(gammas)}, gamma_N = {gammas[-1]:.1f}")
print(f"[height] L = log(gamma/2pi): mean={L_mean:.4f} "
      f"min={L_arr.min():.2f} max={L_arr.max():.2f}")

# ------------------------------------------------------------------
# 3.  Bogomolny-Keating arithmetic correction
# ------------------------------------------------------------------
# Precompute primes up to PMAX, with Mertens weight (log p)^k included.
from sympy import primerange
PMAX = 10**6   # far beyond the leading contribution; sum converges like
               # Sum log^2 p / p^2 which is ~0.49  (Mertens).
primes = np.array(list(primerange(2, PMAX + 1)), dtype=np.float64)
logp = np.log(primes)
print(f"[primes] {len(primes)} primes up to {PMAX}, "
      f"sum log^2 p / p^2 = {(logp**2 / primes**2).sum():.5f}")


def delta_BK(x: np.ndarray, A: float, L: float) -> np.ndarray:
    """
    Bogomolny-Keating arithmetic correction to the *scaled* two-point
    correlation.  This is the contribution of the B(ir) self-pairing
    prime-power term in Conrey-Snaith Theorem 4.3 / Snaith (2010)
    eq. (4.19)-(4.21), after the r-integral against the saddle at r=0.

    Canonical closed form (Berry-Keating 1999 "The Riemann Zeros and
    Eigenvalue Asymptotics", Rev. Mod. Phys., eq. near (49); Bogomolny-
    Keating 1996; reproduced e.g. in Keating "Random matrix theory and
    number theory", 2003 Les Houches lectures, eq. 4.35):

        Delta_BK(x; L) = - (2 / (2 pi)^2)
                          * Sum_p (log p / (p - 1))^2
                            * cos( 2 pi x log p / L ) .

    Here L = log(T / 2 pi) is the mean level spacing times 2 pi.
    The sum converges absolutely (Sum_p log^2 p / (p-1)^2 ~ 1.17).
    The overall factor A is set to 1 in the canonical BK prediction;
    we keep it free as a sanity check.
    """
    # shape (nx, nprimes)
    arg = (2.0 * np.pi / L) * np.outer(x, logp)
    weight = (logp / (primes - 1.0)) ** 2             # shape (nprimes,)
    sum_p = (np.cos(arg) * weight[None, :]).sum(axis=1)
    return A * (-2.0 / (2.0 * np.pi) ** 2) * sum_p


# ------------------------------------------------------------------
# 4.  Fits
# ------------------------------------------------------------------
def chi2_of(model):
    return float(((rm - model) / sm) ** 2).sum() if False else \
        float(np.sum(((rm - model) / sm) ** 2))


# M0 : GUE only (zero residual model)
m0 = np.zeros_like(xm)
chi2_0 = chi2_of(m0)

# M1 : GUE + BK canonical  (A=1, L = L_mean)
m1 = delta_BK(xm, A=1.0, L=L_mean)
chi2_1 = chi2_of(m1)

# M2 : GUE + BK with free A, L_eff
def resid_M2(params):
    A, L = params
    return (rm - delta_BK(xm, A=A, L=L)) / sm
res_M2 = least_squares(resid_M2, x0=[1.0, L_mean],
                       bounds=([0.0, 2.0], [5.0, 15.0]))
A_fit, L_fit = res_M2.x
chi2_2 = (res_M2.fun ** 2).sum()

# M3 : GUE + BK(A,L) + single free-frequency cosine residual C cos(2 pi x / x0 + phi)
def resid_M3(params):
    A, L, C, nu, phi = params
    extra = C * np.cos(2.0 * np.pi * nu * xm + phi)
    return (rm - delta_BK(xm, A=A, L=L) - extra) / sm
res_M3 = least_squares(
    resid_M3,
    x0=[A_fit, L_fit, 0.01, 1.0, 0.0],
    bounds=([0.0, 2.0, 0.0, 0.1, -np.pi],
            [5.0, 15.0, 1.0, 5.0, np.pi]),
)
A3, L3, C3, nu3, phi3 = res_M3.x
chi2_3 = (res_M3.fun ** 2).sum()

def pv(chi2, dof):
    return 1.0 - chi2_dist.cdf(chi2, dof)

print("\n==== chi^2 table ====")
rows = [
    ("M0  GUE only",                 chi2_0, dof_data,     0),
    ("M1  GUE+BK (A=1, L fixed)",    chi2_1, dof_data,     0),
    ("M2  GUE+BK (A, L_eff free)",   chi2_2, dof_data - 2, 2),
    ("M3  GUE+BK + Cos(nu x + phi)", chi2_3, dof_data - 5, 5),
]
print(f"{'model':32s}  chi^2     dof   chi^2/dof   p-value")
for name, c, d, _ in rows:
    print(f"{name:32s}  {c:8.2f}  {d:4d}   {c/d:7.3f}    {pv(c, d):.3e}")

# ---- F-tests / LRT between nested models ------------------------
def f_test(chi2_full, dof_full, chi2_red, dof_red):
    """F = ((chi2_red - chi2_full) / (dof_red - dof_full)) /
         (chi2_full / dof_full).  higher = full model better."""
    dnum = dof_red - dof_full
    if dnum <= 0:
        return None
    F = ((chi2_red - chi2_full) / dnum) / (chi2_full / dof_full)
    p = 1.0 - f_dist.cdf(F, dnum, dof_full)
    return F, p

print("\n==== F-tests (nested) ====")
print(f"M0 -> M1  delta chi^2 = {chi2_0 - chi2_1:8.2f} (0 new params, cannot F-test)")
print(f"M0 -> M2  F, p = {f_test(chi2_2, dof_data-2, chi2_0, dof_data)}")
print(f"M1 -> M2  F, p = {f_test(chi2_2, dof_data-2, chi2_1, dof_data)}")
print(f"M2 -> M3  F, p = {f_test(chi2_3, dof_data-5, chi2_2, dof_data-2)}")

print(f"\n[M2 best-fit]  A = {A_fit:.4f}, L_eff = {L_fit:.4f}  "
      f"(L_mean from data = {L_mean:.4f})")
print(f"[M3 best-fit]  A = {A3:.4f}, L = {L3:.4f}, "
      f"C = {C3:.5f}, nu = {nu3:.3f}, phi = {phi3:.3f}")

# ------------------------------------------------------------------
# 5.  Plot
# ------------------------------------------------------------------
xx = np.linspace(0.02, x.max(), 400)
d_canonical = delta_BK(xx, A=1.0, L=L_mean)
d_M2        = delta_BK(xx, A=A_fit, L=L_fit)

fig, (ax1, ax2) = plt.subplots(
    2, 1, figsize=(8, 8), sharex=True,
    gridspec_kw={"height_ratios": [3, 2]},
)

ax1.errorbar(x, R2_emp, yerr=sigma, fmt="o", ms=3, lw=0.8,
             color="tab:blue", label="Odlyzko 10^5")
ax1.plot(xx, 1.0 - (np.sin(np.pi * xx) / (np.pi * xx))**2, "-",
         color="tab:red", label="GUE")
ax1.plot(xx, 1.0 - (np.sin(np.pi * xx) / (np.pi * xx))**2 + d_M2, "--",
         color="tab:green",
         label=f"GUE + BK (A={A_fit:.2f}, L_eff={L_fit:.2f})")
ax1.set_ylabel(r"$R_2(x)$")
ax1.set_title(
    "Bogomolny-Keating fit to Odlyzko 10^5 residual\n"
    f"chi^2/dof: GUE={chi2_0/dof_data:.2f}  "
    f"GUE+BK(A=1)={chi2_1/dof_data:.2f}  "
    f"GUE+BK(free A,L)={chi2_2/(dof_data-2):.2f}"
)
ax1.legend(loc="lower right")
ax1.grid(alpha=0.3)

ax2.errorbar(x, resid, yerr=sigma, fmt="o", ms=3, lw=0.8,
             color="tab:purple", label="empirical residual")
ax2.plot(xx, d_canonical, "-", color="tab:orange",
         label=f"BK canonical (A=1, L={L_mean:.2f})")
ax2.plot(xx, d_M2, "--", color="tab:green",
         label=f"BK fit (A={A_fit:.2f}, L_eff={L_fit:.2f})")
ax2.axhline(0, color="black", lw=0.6)
ax2.set_xlabel("x (normalised spacing)")
ax2.set_ylabel(r"$R_2^{\rm emp}-R_2^{\rm GUE}$")
ax2.legend(fontsize=9)
ax2.grid(alpha=0.3)

OUT = Path("/home/remondiere/crossed-cosmos/derivations/V7-BK-fit.png")
plt.tight_layout()
plt.savefig(OUT, dpi=120)
print(f"\n[plot] saved {OUT}")

# Summary dict for report
print("\nRESULT:", dict(
    chi2_GUE=chi2_0,
    chi2_BK_canonical=chi2_1,
    chi2_BK_free=chi2_2,
    chi2_BK_plus_cos=chi2_3,
    A_fit=A_fit, L_fit=L_fit, L_mean=L_mean,
    dof=dof_data,
))
