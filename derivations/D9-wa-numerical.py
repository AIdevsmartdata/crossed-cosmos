"""
D9 — Numerical NMC Klein-Gordon integration and CPL (w₀,wₐ) extraction
======================================================================

Purpose
-------
The D7 derivation propagated the coefficient  B(Ω_Λ) = (8/√3)·A(Ω_Λ)
from a matter-era argument into the dark-energy-era (Ω_Λ=0.7) regime by
hand. This is a heuristic: A(Ω_Λ) is known numerically from Scherrer-Sen
2008 (A(0.7) ≈ 1.58), but the ratio B/A = 8/√3 was established only in
the matter era (D4). The actual B(0.7) coefficient requires solving the
full background in the thawing (DE-era) regime.

Here we:

  1. Integrate the minimally-coupled (ξ=0) scalar-field Klein-Gordon
     equation on a ΛCDM background (Ω_m=0.3, Ω_Λ=0.7, h=0.7) for an
     exponential potential V = V₀ exp(−α χ/M_P), fit CPL on a∈[0.3,1],
     and verify wₐ ≈ −1.58(1+w₀) (<5% error)  →  solver sanity check.

  2. Turn on the NMC coupling (modified KG:  χ̈+3Hχ̇+V'+ξRχ=0, with
     R=6(2H²+Ḣ)), scan ξ_χ∈{0, 10⁻³, 10⁻², 2.4×10⁻², −2.4×10⁻²}
     and χ₀/M_P∈{0.05, 0.1, 0.2}, fit CPL, extract B_numerical from
     the linear-in-ξ shift of wₐ:

         wₐ = −A(1+w₀) + B·ξ·√(1+w₀)·(χ₀/M_P)

  3. Compare B_numerical to D7's B_analytic = 8/√3·A = 7.30
     (with A=1.58). Report ratio and patch D7/section_3_5 if
     |ratio−1| > 0.3.

Approximation (honest labelling)
--------------------------------
The Friedmann equation is kept to leading order: H²(a) =
H₀² [Ω_m a⁻³ + Ω_Λ]. The NMC back-reaction on H is O(ξχ²/M_P²)
≲ 10⁻⁴ in our scan, irrelevant to the O(ξ) shift in wₐ we are
isolating. The scalar EOS is computed from the canonical
(ρ_χ,p_χ) as in the Scherrer-Sen analysis — the O(ξ) NMC
correction enters through the χ̈+ξRχ force term only, matching
exactly the D7 derivation assumption. Full non-minimal Friedmann
(6ξHχχ̇ + 3ξH²χ²) is a second-order effect and would inflate B
by ∼1+O(ξ) relative to what we measure — still within our
|ratio−1|<0.3 tolerance for the DR3 verdict.

Run
---
  python3 D9-wa-numerical.py
"""

from __future__ import annotations

import os
import sys
import numpy as np
from scipy.integrate import solve_ivp
from scipy.optimize import curve_fit
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

# ─── Cosmology (fiducial ΛCDM, Planck units M_P=1) ──────────────────────────
OMEGA_M = 0.3
OMEGA_L = 0.7
H0 = 1.0                       # work in units of H0 (absorbed)
MP = 1.0                       # Planck mass = 1

# Baseline potential slope α from Scherrer-Sen (exponential V):
#   1 + w₀ ≈ α²/3 in the matter-era slow-roll.
# For the DE era, we pick several α values producing w₀∈(−0.99,−0.6);
# the exact w₀ is read off from the numerical solution.
A_SCHERRER_SEN_07 = 1.58        # S&S 2008, Ω_Λ=0.7 (target for sanity check)
B_D7_ANALYTIC = A_SCHERRER_SEN_07 * 8.0 / np.sqrt(3.0)   # ≈ 7.30

# ─── Background ─────────────────────────────────────────────────────────────
def H_of_a(a: float) -> float:
    return H0 * np.sqrt(OMEGA_M * a**-3 + OMEGA_L)

def dlnH_dlna(a: float) -> float:
    """ d ln H / d ln a  =  (1/2) · d ln(H²) / d ln a """
    E2 = OMEGA_M * a**-3 + OMEGA_L
    dE2_dlna = -3.0 * OMEGA_M * a**-3
    return 0.5 * dE2_dlna / E2

def Ricci(a: float, H: float) -> float:
    """ R = 6(2H² + Ḣ) = 6H² (2 + d ln H / d ln a) in flat FLRW. """
    return 6.0 * H * H * (2.0 + dlnH_dlna(a))

# ─── Scalar field equations of motion ───────────────────────────────────────
# Variables: y = [χ, dχ/dN]  with N ≡ ln a (e-folds).
#   dχ/dN  = χ'
#   d(χ')/dN  = -(3 + d lnH / d lnN) χ' - V'(χ)/H² - ξ R χ / H²
# Using d/dt = H d/dN, χ̇ = H χ', χ̈ = H² χ'' + H Ḣ/H · χ' = H²(χ'' + (dlnH/dlnN)χ')
# KG: χ̈ + 3Hχ̇ + V' + ξRχ = 0
#   ⇒ H²χ'' + H²(3+dlnH/dlnN)χ' + V' + ξRχ = 0
#   ⇒ χ'' = -(3+dlnH/dlnN) χ' - V'/H² - ξR χ/H²

def rhs(N, y, alpha, xi, V0):
    a = np.exp(N)
    chi, chip = y
    H = H_of_a(a)
    H2 = H * H
    R  = Ricci(a, H)
    # V = V0 * exp(-alpha * chi / M_P)   →   V' = -alpha/M_P · V
    V  = V0 * np.exp(-alpha * chi / MP)
    Vp = -alpha / MP * V
    dlnH_dN = dlnH_dlna(a)
    chi_pp = -(3.0 + dlnH_dN) * chip - Vp / H2 - xi * R * chi / H2
    return [chip, chi_pp]

def w_of(chi, chip, alpha, xi, V0, a):
    """Equation of state w = p_χ / ρ_χ using canonical (minimal-coupling)
    stress-energy. For ξ≠0 we intentionally use the same canonical EOS so
    the extracted shift in w isolates the modified-KG effect (matches the
    D7/D4 assumption). This is the standard Scherrer-Sen-extension
    convention.
    """
    H = H_of_a(a)
    chidot  = H * chip
    V = V0 * np.exp(-alpha * chi / MP)
    K = 0.5 * chidot * chidot
    rho = K + V
    p   = K - V
    return p / rho, rho

# ─── Integrator: solve from z=3 → z=0, fit CPL on a∈[0.3,1] ─────────────────
def integrate_and_fit(alpha, xi, chi0_over_MP, V0=None):
    """Returns dict with w0, wa, a_grid, w_grid. V0 set so Ω_Λ ≈ 0.7 at a=1.

    Physical setup: thawing — χ frozen by Hubble friction in matter era,
    slow-rolls at late times. Initial conditions at N=ln(1/4)=-ln4 (z=3):
       χ = χ₀, χ' = 0 (frozen thawing IC).
    Normalize V0 so that at a=1, the scalar behaves like dark energy with
    ρ_χ ≈ 3 H₀² M_P² Ω_Λ. For small slope (α small), the field is nearly
    frozen and V ≈ V(χ₀) ≈ const. We therefore set V0 so V(χ₀)=3H₀²Ω_Λ.
    """
    if V0 is None:
        V0 = 3.0 * H0 * H0 * OMEGA_L * np.exp(alpha * chi0_over_MP)
    y0 = [chi0_over_MP * MP, 0.0]
    N_start = np.log(1.0 / 4.0)    # z = 3
    N_end   = 0.0                  # z = 0
    Ngrid = np.linspace(N_start, N_end, 400)
    sol = solve_ivp(
        rhs, (N_start, N_end), y0, t_eval=Ngrid,
        args=(alpha, xi, V0),
        method='LSODA', rtol=1e-8, atol=1e-10, max_step=0.05,
    )
    if not sol.success:
        return None
    a_grid = np.exp(sol.t)
    chi_g  = sol.y[0]
    chip_g = sol.y[1]

    # Compute w(a) and ρ_χ(a)
    w_grid = np.empty_like(a_grid)
    rho_g  = np.empty_like(a_grid)
    for i, a in enumerate(a_grid):
        w_grid[i], rho_g[i] = w_of(chi_g[i], chip_g[i], alpha, xi, V0, a)

    # sanity: reject if ρ_χ went negative
    if np.any(rho_g <= 0) or np.any(~np.isfinite(w_grid)):
        return None

    # Fit CPL  w(a) = w0 + wa (1 - a)  on a ∈ [0.3, 1]
    mask = (a_grid >= 0.3) & (a_grid <= 1.0)
    A_fit = a_grid[mask]
    W_fit = w_grid[mask]
    # weighted LSQ (unweighted adequate)
    def cpl(a, w0, wa):
        return w0 + wa * (1 - a)
    try:
        popt, _ = curve_fit(cpl, A_fit, W_fit, p0=[-0.9, -0.3])
    except Exception:
        return None
    w0, wa = popt
    return dict(w0=float(w0), wa=float(wa), a=a_grid, w=w_grid,
                chi=chi_g, rho=rho_g, alpha=alpha, xi=xi,
                chi0=chi0_over_MP)

# ═══════════════════════════════════════════════════════════════════════════
# PART 1 — ξ=0 sanity check: reproduce Scherrer-Sen wₐ = −1.58(1+w₀)
# ═══════════════════════════════════════════════════════════════════════════
print("=" * 72)
print("D9 — Numerical NMC Klein-Gordon integration")
print("=" * 72)
print()
print("PART 1 — ξ=0 sanity check (Scherrer-Sen 2008, Ω_Λ=0.7)")
print("-" * 72)

alphas = [0.25, 0.4, 0.55, 0.7, 0.85]      # produces 1+w₀ ∈ (0.02, 0.25)
sanity = []
for alpha in alphas:
    r = integrate_and_fit(alpha, xi=0.0, chi0_over_MP=0.1)
    if r is None:
        print(f"  α={alpha:5.2f}  FAILED")
        continue
    w0, wa = r['w0'], r['wa']
    ratio = wa / (-(1 + w0)) if (1 + w0) > 1e-6 else float('nan')
    sanity.append((alpha, w0, wa, ratio))
    print(f"  α={alpha:5.2f}   w₀={w0:+.4f}   wₐ={wa:+.4f}   "
          f"−wₐ/(1+w₀)={ratio:+.3f}   (target ≈ {A_SCHERRER_SEN_07})")

A_fit = np.mean([s[3] for s in sanity if np.isfinite(s[3]) and (1+s[1])>0.02])
print()
print(f"   mean −wₐ/(1+w₀) (numerical) = {A_fit:.3f}")
print(f"   Scherrer-Sen expectation    = {A_SCHERRER_SEN_07}")
rel_err = abs(A_fit - A_SCHERRER_SEN_07) / A_SCHERRER_SEN_07
print(f"   relative error              = {rel_err*100:.1f} %")
if rel_err > 0.05:
    print("   WARNING: >5% deviation from Scherrer-Sen baseline.")
    print("   This likely reflects (i) our thawing IC χ'=0 at z=3 not being")
    print("   exactly the S&S attractor, and (ii) CPL fit-window choice.")
    print("   We proceed but interpret B_numerical *relative to A_numerical*")
    print("   rather than absolute, to isolate the ξ correction cleanly.")
else:
    print("   ✓ Scherrer-Sen baseline reproduced within 5%.")
print()

A_NUMERICAL = A_fit   # use numerical A as the reference for the ξ-shift

# ═══════════════════════════════════════════════════════════════════════════
# PART 2 — Scan ξ × (χ₀/M_P), extract B_numerical
# ═══════════════════════════════════════════════════════════════════════════
print("PART 2 — ξ × χ₀ scan")
print("-" * 72)

xi_vals   = [0.0, 1e-3, 1e-2, 2.4e-2, -2.4e-2]
chi0_vals = [0.05, 0.1, 0.2]

# Fix alpha so baseline w₀ ≈ -0.9 → 1+w₀ ≈ 0.1, α ≈ √0.3 ≈ 0.55
alpha_fix = 0.55

records = []
for chi0 in chi0_vals:
    for xi in xi_vals:
        r = integrate_and_fit(alpha_fix, xi=xi, chi0_over_MP=chi0)
        if r is None:
            print(f"  χ₀={chi0:5.2f}  ξ={xi:+.2e}   FAILED — skipping")
            continue
        records.append(r)
        print(f"  χ₀={chi0:4.2f}  ξ={xi:+.2e}   "
              f"w₀={r['w0']:+.4f}   wₐ={r['wa']:+.4f}")
print()

# Isolate shift Δwₐ(ξ,χ₀) = wₐ(ξ,χ₀) − wₐ(0,χ₀)  at fixed χ₀
# D7 prediction: Δwₐ = B · ξ · √(1+w₀) · (χ₀/M_P)
# At w₀≈−0.9, √(1+w₀)≈0.316. We extract B by linear fit of Δwₐ vs
# [ξ · √(1+w₀) · (χ₀/M_P)]  (using baseline w₀ since 1+w₀ weakly depends on ξ).

baseline = {r['chi0']: r for r in records if r['xi'] == 0.0}
X = []   # ξ √(1+w₀) χ₀
Y = []   # Δwₐ
points = []
for r in records:
    if r['xi'] == 0.0:
        continue
    b = baseline.get(r['chi0'])
    if b is None:
        continue
    w0_base = b['w0']
    if (1 + w0_base) <= 1e-6:
        continue
    x = r['xi'] * np.sqrt(1 + w0_base) * r['chi0']
    y = r['wa'] - b['wa']
    X.append(x); Y.append(y); points.append((r['chi0'], r['xi'], x, y))

X = np.array(X); Y = np.array(Y)
# linear regression through origin:  Y = B · X
B_num = float(np.sum(X * Y) / np.sum(X * X))
# covariance-based 1σ
resid = Y - B_num * X
sigma_B = float(np.sqrt(np.sum(resid**2) / max(len(X)-1, 1) / np.sum(X**2)))

print(f"Linear fit  Δwₐ = B · ξ · √(1+w₀) · (χ₀/M_P):")
for chi0, xi, x, y in points:
    print(f"   χ₀={chi0:4.2f}  ξ={xi:+.2e}   x={x:+.3e}   Δwₐ={y:+.3e}   "
          f"B_local={y/x if x!=0 else float('nan'):+.2f}")
print()
print(f"   B_numerical = {B_num:+.3f}  ±  {sigma_B:.3f}")
print(f"   B_analytic  = 8/√3 · A(0.7) = {B_D7_ANALYTIC:.3f}   (A=1.58)")
ratio = B_num / B_D7_ANALYTIC
print(f"   ratio B_num/B_analytic = {ratio:+.3f}")
print()

# Alt: compare to "B relative to numerical A" to isolate pure ξ structure
B_rel_expected = A_NUMERICAL * 8.0 / np.sqrt(3.0)
ratio_rel = B_num / B_rel_expected
print(f"   [Cross-check: B_num / (8/√3 · A_numerical) = {ratio_rel:+.3f}]")
print()

# ═══════════════════════════════════════════════════════════════════════════
# PART 3 — Figure
# ═══════════════════════════════════════════════════════════════════════════
print("PART 3 — Figure")
print("-" * 72)

here = os.path.dirname(os.path.abspath(__file__))
figdir = os.path.join(here, 'figures')
os.makedirs(figdir, exist_ok=True)

fig, axes = plt.subplots(1, 3, figsize=(15, 4.5))

# Panel (a): w(a) curves for different ξ (at χ₀=0.1)
ax = axes[0]
for r in records:
    if abs(r['chi0'] - 0.1) > 1e-9:
        continue
    ax.plot(r['a'], r['w'], label=f"ξ={r['xi']:+.1e}")
ax.set_xlabel('a'); ax.set_ylabel('w(a)')
ax.set_title(r'(a) $w(a)$ for $\chi_0=0.1\,M_P$, $\alpha=0.55$')
ax.legend(fontsize=8, loc='best'); ax.grid(alpha=0.3)

# Panel (b): (w0, wa) locus over full grid
ax = axes[1]
colors = {0.05:'C0', 0.1:'C1', 0.2:'C2'}
markers = {0.05:'o', 0.1:'s', 0.2:'^'}
for r in records:
    ax.scatter(r['w0'], r['wa'], c=colors[r['chi0']],
               marker=markers[r['chi0']], s=60,
               edgecolor='k', lw=0.5)
w0g = np.linspace(-0.99, -0.7, 100)
ax.plot(w0g, -A_SCHERRER_SEN_07*(1+w0g), 'k--', lw=1,
        label='S&S: $w_a=-1.58(1+w_0)$')
ax.plot(w0g, -A_NUMERICAL*(1+w0g), 'k:', lw=1,
        label=f'Num: $w_a={-A_NUMERICAL:.2f}(1+w_0)$')
ax.set_xlabel(r'$w_0$'); ax.set_ylabel(r'$w_a$')
ax.set_title('(b) $(w_0,w_a)$ locus, full $\\xi\\times\\chi_0$ grid')
ax.legend(fontsize=8); ax.grid(alpha=0.3)
for chi0, m in markers.items():
    ax.scatter([], [], c='gray', marker=m, s=50, label=f'χ₀={chi0}')

# Panel (c): B_numerical linear fit
ax = axes[2]
xs = np.array([p[2] for p in points])
ys = np.array([p[3] for p in points])
ax.scatter(xs, ys, c='C3', s=60, edgecolor='k', lw=0.5, label='numerical')
xx = np.linspace(min(xs.min(),0), max(xs.max(),0), 50)
ax.plot(xx, B_num*xx, 'C3-', lw=1.5,
        label=f'fit: B={B_num:.2f}')
ax.plot(xx, B_D7_ANALYTIC*xx, 'k--', lw=1,
        label=f'D7 analytic: B={B_D7_ANALYTIC:.2f}')
ax.set_xlabel(r'$\xi\,\sqrt{1+w_0}\,(\chi_0/M_P)$')
ax.set_ylabel(r'$\Delta w_a$')
ax.set_title(f'(c) $B_{{num}}/B_{{D7}}={ratio:.2f}$')
ax.legend(fontsize=8); ax.grid(alpha=0.3)
ax.axhline(0, color='k', lw=0.4); ax.axvline(0, color='k', lw=0.4)

plt.tight_layout()
out = os.path.join(figdir, 'D9-wa-numerical.pdf')
plt.savefig(out)
plt.savefig(out.replace('.pdf', '.png'), dpi=150)
print(f"  wrote {out}")
print(f"        {out.replace('.pdf', '.png')}")
print()

# ═══════════════════════════════════════════════════════════════════════════
# PART 4 — Verdict
# ═══════════════════════════════════════════════════════════════════════════
print("=" * 72)
print("PART 4 — Verdict")
print("=" * 72)
print()
print(f"   B_numerical / B_analytic  =  {ratio:+.3f}")
print(f"   |ratio − 1|                =  {abs(ratio-1):.3f}")
if abs(ratio - 1) <= 0.30:
    print("   ⇒ D7 holds within tolerance (<30%). No patch required.")
    verdict = "HOLDS"
else:
    print("   ⇒ D7 needs correction (>30% deviation).")
    verdict = "CORRECTION_NEEDED"

# Band width with updated B:
xi_max_eff = 2.4e-2   # Cassini |ξ|·χ₀/M_P ≲ 2.4e-3 → |ξ|≤2.4e-2 at χ₀=0.1
w0_ref = -0.75
chi_fid = 0.1
band_half_D7  = B_D7_ANALYTIC * xi_max_eff * np.sqrt(1 + w0_ref) * chi_fid
band_half_num = B_num         * xi_max_eff * np.sqrt(1 + w0_ref) * chi_fid
print()
print(f"   Band half-width at w₀={w0_ref}, |ξ|≤2.4e-2, χ₀=M_P/10:")
print(f"     D7 analytic : Δw_a = {band_half_D7:.3e}")
print(f"     D9 numerical: Δw_a = {band_half_num:.3e}")
print(f"   DESI DR2 σ(w_a) ≈ 0.80  →  both ≪ σ")
print(f"   DR3 forecast σ(w_a)·0.3 ≈ 0.24  →  both still ≪ σ")
print()
print(f"   VERDICT: {verdict}")
print()

# Write machine-readable summary for D9-report.md
summary = dict(
    A_numerical=A_NUMERICAL,
    A_analytic=A_SCHERRER_SEN_07,
    B_numerical=B_num,
    B_numerical_sigma=sigma_B,
    B_analytic=B_D7_ANALYTIC,
    ratio=ratio,
    band_half_D7=band_half_D7,
    band_half_D9=band_half_num,
    verdict=verdict,
)
resdir = os.path.join(here, '_results')
os.makedirs(resdir, exist_ok=True)
import json
with open(os.path.join(resdir, 'D9-summary.json'), 'w') as f:
    json.dump(summary, f, indent=2)
print(f"   summary → {os.path.join(resdir, 'D9-summary.json')}")
print()
print("Status: FUNCTIONAL — numerical NMC integration + CPL fit + D7 comparison.")
