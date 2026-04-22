"""
D14 — Closed-form NMC perturbation observables (G_eff, η, fσ₈)
==============================================================

Purpose
-------
Peer-review-v2 priority-1 (GPT-5.4 + Grok 4 Q4). Provide analytic, first-order
expressions in ξ_χ for the three scale-dependent modified-gravity observables
that the NMC action

    S = ∫ √−g [ M_P²/2 R − ½(∂χ)² − V(χ) − ½ ξ_χ R χ² ]

(Faraoni convention, mostly-plus) predicts for LSS probes: the effective
Newton constant G_eff(k,a)/G_N, the gravitational slip η = Φ/Ψ, and the
growth observable fσ₈(z). We use the Boisseau–Esposito-Farèse–Polarski–
Starobinsky 2000 (BEFPS00, gr-qc/0001066) scalar-tensor result in the
sub-horizon quasi-static limit (their Eq. 7 + Eqs. 16–22):

    G_eff = 1/(8π F) · (2F + 4 F_Φ²)/(2F + 3 F_Φ²)

where F = M_P² − ξ_χ χ² (sign convention matches our action: the non-minimal
term enters the action with +ξ_χ R χ²/2 ⇒ coefficient of R in the Lagrangian
density becomes (M_P² − ξ_χ χ²)/2), and F_Φ = dF/dχ = −2ξ_χ χ.

The slip follows from the standard Bean-Tangen 2010 / BEFPS00 result
for scalar-tensor: Φ and Ψ differ through the Φ-fluctuation δF, giving

    η ≡ Φ/Ψ = (2F + 2 F_Φ²)/(2F + 4 F_Φ²)          (sub-horizon QS)

(equivalently, γ = Ψ/Φ = 1 + F_Φ²/(F + F_Φ²), cf. De Felice+2011). At first
order in ξ_χ (since F_Φ² = 4 ξ_χ² χ² is O(ξ_χ²)), both the G_eff correction
and the slip are dominated by the 1/F prefactor, i.e. the direct rescaling
of Newton's constant by the NMC shift F ≠ M_P².

Limitations (honest caveats)
----------------------------
(i)  The BEFPS00 formula is sub-horizon quasi-static. k-dependence only
     enters at the scale of the scalar Compton wavelength; for our massless-
     in-Jordan-frame χ (V ∝ e^{−αχ}, light effective mass m² = V''), the
     QS-limit applies for k ≫ a H, k ≫ a m_eff.
(ii) χ₀ evolves (thawing). The "closed-form" expressions below are closed in
     ξ_χ and χ(a), not in redshift: we feed χ(a) from the D13 self-consistent
     background. For the plot we take a constant fiducial χ₀ = M_P/10, which
     is the mid-value used throughout §3.5. This is accurate to O(1+w_0).
(iii) F_Φ² = 4 ξ_χ² χ² is second-order in ξ_χ → the leading first-order
     correction is the 1/F rescaling alone. The (2F+4F_Φ²)/(2F+3F_Φ²)
     factor only enters at O(ξ²) — we report both the strict O(ξ) result
     and the full expression evaluated at ξ_Cassini.

Outputs
-------
  derivations/figures/D14-Geff-eta-fsigma8.pdf / .png
  derivations/_results/D14-summary.json

Run
---
  python derivations/D14-nmc-perturbations.py
"""

from __future__ import annotations
import os, sys, json, time
import numpy as np
import sympy as sp
from scipy.integrate import solve_ivp
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

os.environ.setdefault('OMP_NUM_THREADS', '2')

t0 = time.time()
print("=" * 72)
print("D14 — Closed-form NMC perturbation observables")
print("=" * 72)

# ═══════════════════════════════════════════════════════════════════════════
# [1] SYMPY — Analytic derivation at leading order in ξ_χ
# ═══════════════════════════════════════════════════════════════════════════
print("\n[1] Sympy derivation of G_eff/G_N and η ...")

MP, xi, chi, k, a, H = sp.symbols('M_P xi chi k a H', positive=True, real=True)

# Jordan-frame F(χ) (coefficient of R/2 in the Lagrangian):
# Our action has  +M_P²/2 R  − ½ ξ R χ²  ⇒  L_grav = (M_P² − ξ χ²)/2 · R
# so F(χ) = M_P² − ξ χ² (BEFPS's F convention).
F     = MP**2 - xi * chi**2
F_phi = sp.diff(F, chi)          # = −2 ξ χ

# BEFPS00 Eq.(7) — effective Newton constant (sub-horizon QS):
#   G_eff = 1/(8π F) · (2F + 4 F_Φ²)/(2F + 3 F_Φ²)
# G_N (today, Cavendish) = 1/(8π F_0) with F_0 = M_P² (ξ=0 limit / today).
# For an observable ratio we use G_eff/G_N = (M_P²/F) · (2F+4F_Φ²)/(2F+3F_Φ²).
G_eff_over_GN = (MP**2 / F) * (2*F + 4*F_phi**2) / (2*F + 3*F_phi**2)
G_eff_over_GN_simpl = sp.simplify(G_eff_over_GN)

# Gravitational slip η = Φ/Ψ. BEFPS00 (and e.g. De Felice-Tsujikawa 2010 Eq.5.8
# specialised to scalar-tensor with mass ≪ k/a) give in the sub-horizon QS:
#   Ψ − Φ = δF/F,  with  δF = F_Φ · δχ = −φ · F · F_Φ² / (F + 2 F_Φ²)
# (BEFPS00 Eq. 21 inverted). Combining with the Poisson equation for Φ, one
# obtains the standard scalar-tensor slip
#   η = Φ/Ψ = (2F + 2 F_Φ²)/(2F + 4 F_Φ²)
# (e.g. Boisseau-Esposito-Farese-Polarski-Starobinsky 2000; also Amendola et al
# 2008 arXiv:0712.2268 Eq. 24 with Brans-Dicke ω = F/F_Φ²).
eta = (2*F + 2*F_phi**2) / (2*F + 4*F_phi**2)
eta_simpl = sp.simplify(eta)

# Series expansion in ξ
x = sp.symbols('x')  # x = ξ χ²/M_P² small parameter (dimensionless)
rule = {xi: x * MP**2 / chi**2}    # inject x
Geff_series = sp.series(G_eff_over_GN.subs(rule), x, 0, 3).removeO()
eta_series  = sp.series(eta.subs(rule),            x, 0, 3).removeO()
Geff_series = sp.simplify(Geff_series)
eta_series  = sp.simplify(eta_series)

print("    G_eff/G_N  (exact):        ", sp.simplify(G_eff_over_GN))
print("    G_eff/G_N  (O(ξ³) series): ", Geff_series,
      "   where x ≡ ξ χ²/M_P²")
print("    η = Φ/Ψ    (exact):        ", sp.simplify(eta))
print("    η          (O(ξ³) series): ", eta_series)

# Assertion (a): ξ→0 reproduces GR
assert sp.simplify(G_eff_over_GN.subs(xi, 0) - 1) == 0, "G_eff(ξ=0) ≠ G_N"
assert sp.simplify(eta.subs(xi, 0)          - 1) == 0, "η(ξ=0) ≠ 1"
print("    ✓ ξ→0 limit: G_eff/G_N = 1, η = 1")

# Leading correction: G_eff/G_N ≈ 1 + x + O(x²) = 1 + ξχ²/M_P²,
# because F_Φ²/M_P² = 4 ξ² χ²/M_P² is O(ξ²).
lead_G = sp.series(G_eff_over_GN.subs(rule), x, 0, 2).removeO()
assert sp.simplify(lead_G - (1 + x)) == 0, \
    f"G_eff leading not 1+x: got {lead_G}"
# η leading correction: F_Φ²/F = O(ξ²), so η = 1 − F_Φ²/F + O(ξ³).
# ⇒ η(x) ≈ 1 at O(x); the first nontrivial correction is at O(x²).
lead_eta_1 = sp.series(eta.subs(rule), x, 0, 2).removeO()
assert sp.simplify(lead_eta_1 - 1) == 0, \
    f"η leading not 1 at O(x): got {lead_eta_1}"
print("    ✓ Leading order: G_eff/G_N = 1 + ξχ²/M_P² + O(ξ²);  "
      "η = 1 + O(ξ²)")

# Numerical lambdas (φ → chi in M_P units)
Geff_fn = sp.lambdify((xi, chi), G_eff_over_GN.subs(MP, 1), 'numpy')
eta_fn  = sp.lambdify((xi, chi), eta.subs(MP, 1),          'numpy')

# ═══════════════════════════════════════════════════════════════════════════
# [2] Background χ(a) from thawing NMC scalar (mirrors D13 conventions)
# ═══════════════════════════════════════════════════════════════════════════
print("\n[2] Thawing χ(a) from NMC background (α=0.55, χ₀=0.1 M_P) ...")
# We reuse the D13 self-consistent integration to get χ(a). For economy we
# re-integrate a compact version here; if D13 summary is present, validate.

OMEGA_M0 = 0.3
OMEGA_R0 = 9.2e-5
alpha    = 0.55
chi0_fid = 0.10           # M_P units
xi_Cass  = 2.4e-2         # Cassini-saturated value (PPN bound from D7)
# Calibrate V₀ so Ω_χ(a=1) ≈ 0.7 at ξ=0 using the same protocol as D13.

def H2_of_state(chi_, chip, rho_m, rho_r, V, xi_):
    denom = 3.0*(1.0 - xi_*chi_*chi_) + 6.0*xi_*chi_*chip - 0.5*chip*chip
    num   = rho_m + rho_r + V
    if denom <= 0 or num <= 0:
        return float('nan')
    return num/denom

def rhs(N, y, xi_, V0):
    chi_, chip, ln_rho_m = y
    a_    = np.exp(N)
    rho_m = np.exp(ln_rho_m)
    rho_r = 3*OMEGA_R0 * a_**-4
    V     = V0 * np.exp(-alpha*chi_)
    Vp    = -alpha * V
    H2    = H2_of_state(chi_, chip, rho_m, rho_r, V, xi_)
    if not np.isfinite(H2) or H2 <= 0:
        return [0.0, 0.0, 0.0]
    denom = 3.0*(1.0 - xi_*chi_*chi_) + 6.0*xi_*chi_*chip - 0.5*chip*chip
    num   = rho_m + rho_r + V
    A0 = -3.0*chip - Vp/H2 - 12.0*xi_*chi_
    A1 = -0.5*chip - 3.0*xi_*chi_
    dnum_dN       = -3.0*rho_m - 4.0*rho_r + Vp*chip
    ddenom_base_0 = -6.0*xi_*chi_*chip + 6.0*xi_*chip*chip
    ddenom_c_coef =  6.0*xi_*chi_ - chip
    B0 = dnum_dN/num - ddenom_base_0/denom
    B1 = -ddenom_c_coef/denom
    det = 1.0 - A1*B1
    if abs(det) < 1e-14:
        return [0.0, 0.0, 0.0]
    chipp = (A0 + A1*B0) / det
    return [chip, chipp, -3.0]

def solve_background(xi_, V0, N_start=np.log(1/1000.), N_end=0.0, n=600):
    rho_m0 = 3.0 * OMEGA_M0
    y0 = [chi0_fid, 0.0, np.log(rho_m0) - 3.0*N_start]
    Ngrid = np.linspace(N_start, N_end, n)
    sol = solve_ivp(lambda N, y: rhs(N, y, xi_, V0),
                    (N_start, N_end), y0, t_eval=Ngrid,
                    method='LSODA', rtol=1e-8, atol=1e-10, max_step=0.05)
    if not sol.success:
        return None
    a_  = np.exp(sol.t)
    chi_= sol.y[0]; chip = sol.y[1]
    rho_m = np.exp(sol.y[2])
    rho_r = 3*OMEGA_R0 * a_**-4
    V = V0 * np.exp(-alpha*chi_)
    H2 = np.array([H2_of_state(c, cp, rm, rr, v, xi_)
                   for c, cp, rm, rr, v in zip(chi_, chip, rho_m, rho_r, V)])
    Om_chi = (0.5*(H2*chip*chip) + V) / (3.0*H2)
    return dict(a=a_, N=sol.t, chi=chi_, chip=chip, H2=H2, Om_chi=Om_chi)

# Calibrate V0 at ξ=0
from scipy.optimize import brentq
def resid(V0, xi_=0.0):
    r = solve_background(xi_, V0, n=300)
    if r is None:
        return 1.0
    return r['Om_chi'][-1] - 0.7
V0 = brentq(resid, 1e-3, 5.0, xtol=1e-4)
print(f"    V₀ = {V0:.4f}   (Ω_χ(a=1)=0.7 at ξ=0, χ₀=M_P/10)")

bg0    = solve_background(0.0,      V0)
bg_pos = solve_background(+xi_Cass, V0)
bg_neg = solve_background(-xi_Cass, V0)
assert bg0 and bg_pos and bg_neg, "background integration failed"

# ═══════════════════════════════════════════════════════════════════════════
# [3] G_eff/G_N(a) and η(a) along the trajectories
# ═══════════════════════════════════════════════════════════════════════════
print("\n[3] G_eff/G_N(a), η(a) along χ(a) ...")

def obs_along(bg, xi_):
    chi_of_a = bg['chi']
    G = Geff_fn(xi_, chi_of_a)
    e = eta_fn(xi_,  chi_of_a)
    return np.asarray(G), np.asarray(e)

G0,  e0  = obs_along(bg0,    0.0)
Gp,  ep  = obs_along(bg_pos, +xi_Cass)
Gn,  en  = obs_along(bg_neg, -xi_Cass)

# assertion (b): ξ=0 branch ⇒ G_eff/G_N ≡ 1, η ≡ 1
assert np.allclose(G0, 1.0, atol=1e-12) and np.allclose(e0, 1.0, atol=1e-12), \
    "ξ=0 branch did not reproduce GR"
print("    ✓ ξ=0 branch: G_eff/G_N ≡ 1, η ≡ 1")

# Report at selected a values
a_report = [0.3, 0.5, 0.7, 1.0]
print(f"    Cassini ξ = +{xi_Cass}:")
for ar in a_report:
    i = int(np.argmin(np.abs(bg_pos['a'] - ar)))
    print(f"        a={ar:.2f}  χ={bg_pos['chi'][i]:+.4f}  "
          f"G_eff/G_N={Gp[i]:.6f}  η={ep[i]:.8f}  "
          f"(ΔG/G={100*(Gp[i]-1):+.3f}%)")
print(f"    Cassini ξ = −{xi_Cass}:")
for ar in a_report:
    i = int(np.argmin(np.abs(bg_neg['a'] - ar)))
    print(f"        a={ar:.2f}  χ={bg_neg['chi'][i]:+.4f}  "
          f"G_eff/G_N={Gn[i]:.6f}  η={en[i]:.8f}  "
          f"(ΔG/G={100*(Gn[i]-1):+.3f}%)")

# ═══════════════════════════════════════════════════════════════════════════
# [4] fσ₈(z): integrate δ'' + 2H δ' − 4π G_eff ρ_m δ = 0 in N = ln a
# ═══════════════════════════════════════════════════════════════════════════
print("\n[4] fσ₈(z) from quasi-static growth equation ...")
# In N = ln a variable (prime = d/dN):
#   δ'' + (2 + H'/H) δ' − (3/2) Ω_m(a) (G_eff/G_N) δ = 0
# with Ω_m(a) = ρ_m/(3H²) using the self-consistent H(a).
# Matter IC at z=50: δ ∝ a (linear growth in matter era) ⇒ δ=a, δ'=a.

SIGMA8_TODAY = 0.811     # Planck 2018 fiducial

def integrate_growth(bg, xi_):
    """Returns interpolators for δ(N), f(N) and fσ₈(z)."""
    a_  = bg['a']; N = bg['N']
    chi_= bg['chi']; chip = bg['chip']; H2 = bg['H2']
    rho_m = 3.0*OMEGA_M0 * a_**-3
    Om_m  = rho_m / (3.0*H2)
    G_of_a = Geff_fn(xi_, chi_)
    # d ln H / dN from finite differences on ln H
    lnH = 0.5*np.log(H2)
    dlnH_dN = np.gradient(lnH, N)
    # Build callables via interpolation on grid
    def coefs(Nq):
        Omm = np.interp(Nq, N, Om_m)
        G   = np.interp(Nq, N, G_of_a)
        dln = np.interp(Nq, N, dlnH_dN)
        return Omm, G, dln
    def rhs_growth(Nq, y):
        d, dp = y
        Omm, G, dln = coefs(Nq)
        ddp = - (2.0 + dln) * dp + 1.5 * Omm * G * d
        return [dp, ddp]
    # IC at z=50: a_ic = 1/51 → N_ic = -ln(51)
    N_ic = -np.log(51.0)
    a_ic = np.exp(N_ic)
    # Normalise δ(a_ic) = a_ic; δ'(a_ic) = a_ic (matter era: δ∝a ⇒ δ' = δ)
    y0 = [a_ic, a_ic]
    Ngrid = np.linspace(N_ic, 0.0, 800)
    sol = solve_ivp(rhs_growth, (N_ic, 0.0), y0, t_eval=Ngrid,
                    method='LSODA', rtol=1e-9, atol=1e-12)
    assert sol.success, "growth ODE failed"
    delta = sol.y[0]; deltap = sol.y[1]
    f = deltap / delta             # f = d ln δ / d ln a
    # σ₈(z) = σ₈(0) · δ(z)/δ(0)
    delta_today = delta[-1]
    sigma8 = SIGMA8_TODAY * (delta / delta_today)
    z = 1.0/np.exp(sol.t) - 1.0
    fsigma8 = f * sigma8
    return dict(z=z, f=f, sigma8=sigma8, fsigma8=fsigma8,
                delta=delta, N=sol.t)

gr0  = integrate_growth(bg0,    0.0)
grp  = integrate_growth(bg_pos, +xi_Cass)
grn  = integrate_growth(bg_neg, -xi_Cass)

# assertion (c): ξ=0 reproduces ΛCDM-like fσ₈ (within thawing-DE corrections)
# At z=0 in ΛCDM with Ω_m=0.3, fσ₈ ≈ 0.44 (Planck-like).
fs8_0_xi0 = float(np.interp(0.0, gr0['z'][::-1], gr0['fsigma8'][::-1]))
print(f"    ξ=0: fσ₈(z=0) = {fs8_0_xi0:.4f}  (ΛCDM-like ~0.44)")
assert 0.40 < fs8_0_xi0 < 0.50, (
    f"ξ=0 fσ₈(0)={fs8_0_xi0:.3f} outside ΛCDM-thawing band [0.40, 0.50]")

z_bins = [0.1, 0.5, 1.0]
def at_z(gr, z_):
    # ensure monotonic
    z_arr = gr['z'][::-1]; f_arr = gr['fsigma8'][::-1]
    return float(np.interp(z_, z_arr, f_arr))

print("    fσ₈(z) at Euclid/LSST bins:")
print(f"       z      ξ=0          ξ=+{xi_Cass}         ξ=−{xi_Cass}"
      f"     ΔfS₈/fS₈(+)   ΔfS₈/fS₈(−)")
results_fs8 = {}
for z_ in z_bins:
    f0 = at_z(gr0, z_); fp = at_z(grp, z_); fn = at_z(grn, z_)
    dpp = 100*(fp-f0)/f0
    dnn = 100*(fn-f0)/f0
    results_fs8[z_] = dict(fs8_0=f0, fs8_pos=fp, fs8_neg=fn,
                           delta_pct_pos=dpp, delta_pct_neg=dnn)
    print(f"      {z_:4.2f}   {f0:.4f}      {fp:.4f}        {fn:.4f}"
          f"      {dpp:+.3f}%     {dnn:+.3f}%")

# Euclid/LSST Y10 per-bin σ(fσ₈) ~ 1% → detectability
detect_1pct = any(max(abs(results_fs8[z_]['delta_pct_pos']),
                      abs(results_fs8[z_]['delta_pct_neg'])) >= 1.0
                  for z_ in z_bins)
print(f"\n    Detectable at Euclid/LSST Y10 σ(fσ₈)~1% per-bin? "
      f"{'YES' if detect_1pct else 'NO'}")

# ═══════════════════════════════════════════════════════════════════════════
# [5] Figure
# ═══════════════════════════════════════════════════════════════════════════
here   = os.path.dirname(os.path.abspath(__file__))
figdir = os.path.join(here, 'figures'); os.makedirs(figdir, exist_ok=True)
resdir = os.path.join(here, '_results'); os.makedirs(resdir, exist_ok=True)

fig, axes = plt.subplots(1, 3, figsize=(14, 4.3))

ax = axes[0]
ax.axhline(1.0, color='k', ls=':', lw=0.8, label=r'$G_N$')
ax.plot(bg_pos['a'], Gp, 'C3-',  lw=1.5, label=rf'$\xi_\chi=+{xi_Cass}$')
ax.plot(bg_neg['a'], Gn, 'C0-',  lw=1.5, label=rf'$\xi_\chi=-{xi_Cass}$')
ax.plot(bg0['a'],   G0, 'k--',  lw=1.0, alpha=0.7, label=r'$\xi_\chi=0$')
ax.set_xscale('log'); ax.set_xlabel(r'$a$')
ax.set_ylabel(r'$G_{\mathrm{eff}}(a)/G_N$')
ax.set_title(r'(a) Effective Newton constant')
ax.legend(fontsize=9); ax.grid(alpha=0.3)

ax = axes[1]
ax.axhline(1.0, color='k', ls=':', lw=0.8, label=r'GR ($\eta=1$)')
ax.plot(bg_pos['a'], ep, 'C3-', lw=1.5, label=rf'$\xi_\chi=+{xi_Cass}$')
ax.plot(bg_neg['a'], en, 'C0-', lw=1.5, label=rf'$\xi_\chi=-{xi_Cass}$')
ax.set_xscale('log'); ax.set_xlabel(r'$a$')
ax.set_ylabel(r'$\eta\equiv \Phi/\Psi$')
ax.set_title(r'(b) Gravitational slip')
# η corrections are O(ξ²) → essentially invisible; annotate the order
ax.legend(fontsize=9); ax.grid(alpha=0.3)
ax.text(0.04, 0.06, r'$\eta-1=\mathcal{O}(\xi_\chi^2\chi^2/M_P^2)$',
        transform=ax.transAxes, fontsize=9,
        bbox=dict(fc='w', ec='0.7', alpha=0.9))

ax = axes[2]
ax.plot(gr0['z'],  gr0['fsigma8'],  'k--', lw=1.0, label=r'$\xi_\chi=0$ (ref)')
ax.plot(grp['z'],  grp['fsigma8'],  'C3-', lw=1.5, label=rf'$\xi_\chi=+{xi_Cass}$')
ax.plot(grn['z'],  grn['fsigma8'],  'C0-', lw=1.5, label=rf'$\xi_\chi=-{xi_Cass}$')
for z_ in z_bins:
    ax.axvline(z_, color='gray', ls=':', lw=0.6, alpha=0.5)
ax.set_xlim(0, 1.5); ax.set_xlabel(r'$z$')
ax.set_ylabel(r'$f\sigma_8(z)$')
ax.set_title(r'(c) Growth observable')
ax.legend(fontsize=9); ax.grid(alpha=0.3)

plt.tight_layout()
outpdf = os.path.join(figdir, 'D14-Geff-eta-fsigma8.pdf')
plt.savefig(outpdf)
plt.savefig(outpdf.replace('.pdf', '.png'), dpi=150)
print(f"\n[5] Figure: {outpdf}")

# ═══════════════════════════════════════════════════════════════════════════
# [6] JSON summary
# ═══════════════════════════════════════════════════════════════════════════
def _at_a(bg, arr, a_val):
    i = int(np.argmin(np.abs(bg['a'] - a_val)))
    return float(arr[i])

summary = dict(
    action_convention="L = (M_P^2 - xi chi^2)/2 · R - 1/2 (∂χ)^2 - V(χ)",
    reference="BEFPS00 (gr-qc/0001066), Eq. 7 + Eqs. 16-22 sub-horizon QS",
    xi_Cassini=xi_Cass,
    chi0=chi0_fid,
    alpha=alpha,
    V0=V0,
    Geff_over_GN_series_in_x="1 + x + O(x^2),  x = ξ χ²/M_P²",
    eta_series_in_x="1 + O(x^2)  [first correction O(ξ^2)]",
    Geff_over_GN_at_a={
        f"{ar}": {"xi=0": _at_a(bg0, G0, ar),
                   "xi=+cassini": _at_a(bg_pos, Gp, ar),
                   "xi=-cassini": _at_a(bg_neg, Gn, ar)}
        for ar in a_report},
    eta_at_a={
        f"{ar}": {"xi=0": _at_a(bg0, e0, ar),
                   "xi=+cassini": _at_a(bg_pos, ep, ar),
                   "xi=-cassini": _at_a(bg_neg, en, ar)}
        for ar in a_report},
    fsigma8={f"{z_}": results_fs8[z_] for z_ in z_bins},
    detectable_EuclidLSST_Y10=detect_1pct,
    runtime_s=time.time()-t0,
)
with open(os.path.join(resdir, 'D14-summary.json'), 'w') as fh:
    json.dump(summary, fh, indent=2, default=float)
print(f"     Summary: {os.path.join(resdir, 'D14-summary.json')}")

print(f"\n[7] Runtime: {time.time()-t0:.1f} s")
print("\n" + "=" * 72)
print("D14 PASS — NMC perturbation observables derived, asserts passed.")
print("=" * 72)
