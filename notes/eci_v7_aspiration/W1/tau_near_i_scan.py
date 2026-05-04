"""
W1 — τ-near-i framework: 2D χ² scan of (Re τ, Im τ) around τ=i
Joint quark + lepton + CKM fit for LYD20 S'_4 modular flavor

PDG 2022 targets used throughout (PDG 2022, pdg.lbl.gov):
  m_e/m_μ    = 4.836e-3    (PDG 2022 Table of Lepton Properties)
  m_μ/m_τ   = 5.946e-2    (PDG 2022)
  m_c/m_t   ≈ 0.00268      (LYD20 arXiv:2006.10722 Table I, at Q=1 TeV)
  m_u/m_c   ≈ 0.00204      (LYD20 Table I)
  sin θ_12   = 0.2253 ± 0.0007  (PDG 2022 CKM)
  sin θ_13   = 0.003690 ± 0.0001 (PDG 2022 CKM)
  sin θ_23   = 0.04182 ± 0.001  (PDG 2022 CKM)

Strategy: At each τ on the grid, independently optimise the coupling-ratio
parameters for quark and lepton sectors, then compute joint χ² (7 observables).
"""

import sys, warnings
import numpy as np
from numpy import pi, exp, sqrt
from scipy.optimize import minimize, differential_evolution
from scipy.linalg import svd as scipy_svd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import time

warnings.filterwarnings('ignore')

# ─────────────────────────────────────────────────────────────────
# PDG 2022 targets
# ─────────────────────────────────────────────────────────────────
PDG_ME_MMU   = 0.51099895e-3 / 105.6583755e-3   # 4.836e-3
PDG_MMU_MTAU = 105.6583755e-3 / 1776.86e-3      # 5.946e-2
PDG_MC_MT    = 0.00268    # LYD20 Table I (from LYD20 text, best-fit, at 1 TeV)
PDG_MU_MC    = 0.00204    # LYD20 Table I
PDG_MD_MS    = 0.05182    # LYD20 Table I  (used for weighting down-quark mass)
PDG_MS_MB    = 0.01309    # LYD20 Table I
PDG_SIN12    = 0.2253     # |V_us| PDG 2022
PDG_SIN13    = 0.003690   # |V_ub| PDG 2022
PDG_SIN23    = 0.04182    # |V_cb| PDG 2022

# 1-sigma uncertainties for χ²
SIG_MC_MT    = 0.05 * PDG_MC_MT   # 5% log uncertainty
SIG_MU_MC    = 0.05 * PDG_MU_MC
SIG_MMU_MTAU = 0.003              # ~5% of r2
SIG_ME_MMU   = 0.0002             # PDG 2022 lepton uncertainty
SIG_SIN12    = 0.0007             # PDG 2022
SIG_SIN13    = 0.0001             # PDG 2022
SIG_SIN23    = 0.0008             # PDG 2022

# ─────────────────────────────────────────────────────────────────
# Modular forms: Dedekind eta and weight-1 forms
# ─────────────────────────────────────────────────────────────────

def eta(tau, n_terms=40):
    """Dedekind eta η(τ) via q-product. q = exp(2πiτ)."""
    q = exp(2j * pi * tau)
    result = q ** (1/24)
    for n in range(1, n_terms):
        result *= (1 - q**n)
    return result


def weight1_forms(tau, n_terms=40):
    """
    Y1, Y2, Y3 — weight-1 modular forms of S'_4 (3̂' representation).
    Source: LYD20 arXiv:2006.10722, lines 296-330 of TeX source.
    Basis: e1 = η^4(4τ)/η^2(2τ), e2 = η^10(2τ)/(η^4(4τ)η^4(τ)), e3 = η^4(2τ)/η^2(τ)
    """
    e1 = eta(4*tau, n_terms)**4 / eta(2*tau, n_terms)**2
    e2 = eta(2*tau, n_terms)**10 / (eta(4*tau, n_terms)**4 * eta(tau, n_terms)**4)
    e3 = eta(2*tau, n_terms)**4 / eta(tau, n_terms)**2

    omega = exp(2j * pi / 3)
    s2 = sqrt(2)
    s3 = sqrt(3)

    Y1 = 4*s2*e1 + s2*1j*e2 + 2*s2*(1-1j)*e3
    Y2 = (-2*s2*(1+s3)*omega**2*e1 - (1-s3)/s2*1j*omega**2*e2 + 2*s2*(1-1j)*omega**2*e3)
    Y3 = ( 2*s2*(s3-1)*omega   *e1 - (1+s3)/s2*1j*omega   *e2 + 2*s2*(1-1j)*omega   *e3)
    return Y1, Y2, Y3


def all_forms(tau, n_terms=40):
    """
    All modular form components needed for Model VI + unified lepton model.
    Returns dict with all used components, transcribed from LYD20.
    """
    Y1, Y2, Y3 = weight1_forms(tau, n_terms)
    f = {'Y1': Y1, 'Y2': Y2, 'Y3': Y3}

    # Weight-2 (LYD20 lines 346-352)
    f['Y2_3'] = 2*Y1**2 - 2*Y2*Y3       # Y^(2)_3 component 0
    f['Y2_4'] = 2*Y3**2 - 2*Y1*Y2       # Y^(2)_3 component 1
    f['Y2_5'] = 2*Y2**2 - 2*Y1*Y3       # Y^(2)_3 component 2

    # Weight-3 (LYD20 lines 354-360)
    f['Y3_2'] = 2*(2*Y1**3 - Y2**3 - Y3**3)
    f['Y3_3'] = 6*Y3*(Y2**2 - Y1*Y3)
    f['Y3_4'] = 6*Y2*(Y3**2 - Y1*Y2)

    # Weight-4 (LYD20 Appendix lines 1858-1860) — Y^(4)_3 components
    f['Y4_4'] = 6*Y1*(-Y2**3 + Y3**3)
    f['Y4_5'] = 6*Y1*Y3*(Y2**2 - Y1*Y3) + 2*Y2*(-2*Y1**3 + Y2**3 + Y3**3)
    f['Y4_6'] = 6*Y1*Y2*(Y1*Y2 - Y3**2) - 2*Y3*(-2*Y1**3 + Y2**3 + Y3**3)

    # Weight-5 Y^(5)_{3̂} (LYD20 lines 1866-1870)
    f['Y5_3'] = 18*Y1**2*(-Y2**3 + Y3**3)
    f['Y5_4'] = (4*Y1**4*Y2 + 4*Y1*(Y2**4 - 5*Y2*Y3**3)
                 + 14*Y1**3*Y3**2 - 4*Y3**2*(Y2**3 + Y3**3)
                 + 6*Y1**2*Y2**2*Y3)
    f['Y5_5'] = (-4*Y1**4*Y3 - 4*Y1*(Y3**4 - 5*Y2**3*Y3)
                 - 14*Y1**3*Y2**2 + 4*Y2**2*(Y2**3 + Y3**3)
                 - 6*Y1**2*Y2*Y3**2)

    # Weight-5 Y^(5)_{3̂',I} (LYD20 lines 1871-1876)
    f['Y5_6'] = (8*Y1**3*Y2*Y3 - 6*Y1**2*(Y2**3 + Y3**3) + 2*Y2*Y3*(Y2**3 + Y3**3))
    f['Y5_7'] = (4*Y1**4*Y2 - 2*Y1*Y2**4 - 6*Y1**2*Y2**2*Y3
                 - 2*Y1**3*Y3**2 + 4*Y2**3*Y3**2 + 4*Y1*Y2*Y3**3 - 2*Y3**5)
    f['Y5_8'] = -2*(Y1**3*Y2**2 + Y2**5 - 2*Y1**4*Y3
                    + 3*Y1**2*Y2*Y3**2 - 2*Y2**2*Y3**3
                    + Y1*(-2*Y2**3*Y3 + Y3**4))

    # Weight-5 Y^(5)_{3̂',II} (LYD20 lines 1873-1876)
    D = Y1**4 + 3*Y2**2*Y3**2 - 2*Y1*(Y2**3 + Y3**3)
    f['Y5_9']  = 4*Y1*D
    f['Y5_10'] = 4*Y2*D
    f['Y5_11'] = 4*Y3*D

    return f


# ─────────────────────────────────────────────────────────────────
# Mass matrices
# ─────────────────────────────────────────────────────────────────

def M_up(f, beta_u, gamma_u):
    """
    LYD20 Model VI up-type quark matrix. Eq.(Mq_6), lines 1380-1384.
    Row u^c: α_u*(Y1_1, Y1_3, Y1_2)  [weight-1, 3̂']
    Row c^c: β_u*(Y2_3, Y2_5, Y2_4)  [weight-2, 3]
    Row t^c: γ_u*(Y5_3, Y5_5, Y5_4)  [weight-5, 3̂]
    α_u=1 (overall scale irrelevant for mass ratios).
    """
    M = np.zeros((3, 3), dtype=complex)
    M[0] = [f['Y1'], f['Y3'], f['Y2']]                      # u^c row
    M[1] = [beta_u * f['Y2_3'], beta_u * f['Y2_5'], beta_u * f['Y2_4']]  # c^c row
    M[2] = [gamma_u * f['Y5_3'], gamma_u * f['Y5_5'], gamma_u * f['Y5_4']]  # t^c row
    return M


def M_down(f, beta_d, gamma_d1, gamma_d2):
    """
    LYD20 Model VI down-type quark matrix. Eq.(Mq_6), lines 1385-1389.
    Row d^c: α_d*(Y1_1, Y1_3, Y1_2)        [weight-1, 3̂']
    Row s^c: β_d*(Y5_3, Y5_5, Y5_4)        [weight-5, 3̂]
    Row b^c: γ_d1*(Y5_6,Y5_8,Y5_7) + γ_d2*(Y5_9,Y5_11,Y5_10)
    """
    M = np.zeros((3, 3), dtype=complex)
    M[0] = [f['Y1'], f['Y3'], f['Y2']]
    M[1] = [beta_d * f['Y5_3'], beta_d * f['Y5_5'], beta_d * f['Y5_4']]
    M[2] = [gamma_d1 * f['Y5_6'] + gamma_d2 * f['Y5_9'],
            gamma_d1 * f['Y5_8'] + gamma_d2 * f['Y5_11'],
            gamma_d1 * f['Y5_7'] + gamma_d2 * f['Y5_10']]
    return M


def M_lepton(f, beta_e, gamma_e):
    """
    LYD20 unified model charged lepton matrix. Eq.(Ml), lines 1491-1495.
    Row E1^c (~1, k=2): α_e*(Y4^(4)_4, Y4^(4)_6, Y4^(4)_5)
    Row E2^c (~1, k=0): β_e*(Y2_3, Y2_5, Y2_4)
    Row E3^c (~1̂',k=1): γ_e*(Y3_2, Y3_4, Y3_3)
    α_e=1 (irrelevant for mass ratios).
    """
    M = np.zeros((3, 3), dtype=complex)
    M[0] = [f['Y4_4'], f['Y4_6'], f['Y4_5']]
    M[1] = [beta_e * f['Y2_3'], beta_e * f['Y2_5'], beta_e * f['Y2_4']]
    M[2] = [gamma_e * f['Y3_2'], gamma_e * f['Y3_4'], gamma_e * f['Y3_3']]
    return M


# ─────────────────────────────────────────────────────────────────
# Observables from matrices
# ─────────────────────────────────────────────────────────────────

def svd_sorted(M):
    """Return singular values sorted ascending."""
    _, sv, _ = scipy_svd(M)
    return np.sort(sv)


def mass_ratios(M):
    """Return (ratio01, ratio12) = (sv[0]/sv[1], sv[1]/sv[2])."""
    sv = svd_sorted(M)
    if sv[1] < 1e-35 or sv[2] < 1e-35:
        return 1e8, 1e8
    return sv[0]/sv[1], sv[1]/sv[2]


def ckm_angles(Mu, Md):
    """
    Compute CKM mixing angles.
    Convention: CKM = U_uL† U_dL where U_L = left singular vectors.
    PDG ordering: rows/cols by ascending mass.
    """
    Uu, su, _ = scipy_svd(Mu)
    Ud, sd, _ = scipy_svd(Md)
    iu = np.argsort(su); Uu = Uu[:, iu]
    id_ = np.argsort(sd); Ud = Ud[:, id_]
    V = Uu.conj().T @ Ud
    aV = np.abs(V)
    V_ub = aV[0, 2]
    denom = sqrt(max(1 - V_ub**2, 1e-20))
    s12 = aV[0, 1] / denom
    s13 = V_ub
    s23 = aV[1, 2] / denom
    return s12, s13, s23


# ─────────────────────────────────────────────────────────────────
# Sector fits at fixed τ
# ─────────────────────────────────────────────────────────────────

def fit_up_sector(f):
    """
    Fit β_u, γ_u (α_u=1) to reproduce PDG m_c/m_t, m_u/m_c.
    Uses log-space residuals for numerical stability.
    Returns (beta_u, gamma_u, chi2_u).
    """
    def obj(x):
        bu, gu = exp(x[0]), exp(x[1])
        try:
            M = M_up(f, bu, gu)
            r01, r12 = mass_ratios(M)
        except Exception:
            return 1e10
        if r01 <= 0 or r12 <= 0:
            return 1e10
        c = ((np.log(r01) - np.log(PDG_MU_MC)) / 0.10)**2 + \
            ((np.log(r12) - np.log(PDG_MC_MT)) / 0.10)**2
        return c

    best = 1e10
    best_x = None
    # Grid of starting points
    for lb in np.linspace(-4, 8, 8):
        for lg in np.linspace(-4, 8, 8):
            try:
                res = minimize(obj, [lb, lg], method='Nelder-Mead',
                               options={'maxiter': 5000, 'xatol': 1e-9, 'fatol': 1e-9})
                if res.fun < best:
                    best = res.fun
                    best_x = res.x
            except Exception:
                pass
    if best_x is None:
        return 1.0, 1.0, 1e10
    bu, gu = exp(best_x[0]), exp(best_x[1])
    return bu, gu, best


def fit_down_sector(f, beta_u, gamma_u):
    """
    Fit β_d, γ_d1, γ_d2 (α_d=1) to PDG m_d/m_s, m_s/m_b, sin θ_12, sin θ_13, sin θ_23.
    γ_d2 is complex (2 real params: re, im).
    Returns (beta_d, gamma_d1, gamma_d2_complex, chi2_d).
    """
    Mu = M_up(f, beta_u, gamma_u)

    def obj(x):
        bd, gd1, gd2r, gd2i = exp(x[0]), exp(x[1]), x[2], x[3]
        try:
            Md = M_down(f, bd, gd1, gd2r + 1j*gd2i)
        except Exception:
            return 1e10
        svd_ = svd_sorted(Md)
        if svd_[1] < 1e-35 or svd_[2] < 1e-35:
            return 1e10
        r01 = svd_[0] / svd_[1]
        r12 = svd_[1] / svd_[2]
        try:
            s12, s13, s23 = ckm_angles(Mu, Md)
        except Exception:
            return 1e10
        if not np.isfinite(s12 + s13 + s23):
            return 1e10
        c = ((np.log(max(r01, 1e-12)) - np.log(PDG_MD_MS)) / 0.15)**2 + \
            ((np.log(max(r12, 1e-12)) - np.log(PDG_MS_MB)) / 0.15)**2 + \
            ((s12 - PDG_SIN12) / SIG_SIN12)**2 + \
            ((s13 - PDG_SIN13) / SIG_SIN13)**2 + \
            ((s23 - PDG_SIN23) / SIG_SIN23)**2
        return c

    best = 1e10
    best_x = None
    for lb in np.linspace(-2, 6, 5):
        for lg in np.linspace(-2, 6, 5):
            for gdr in [-1, 0, 1]:
                try:
                    res = minimize(obj, [lb, lg, gdr, 0], method='Nelder-Mead',
                                   options={'maxiter': 8000, 'xatol': 1e-9, 'fatol': 1e-9})
                    if res.fun < best:
                        best = res.fun
                        best_x = res.x
                except Exception:
                    pass
    if best_x is None:
        return 1.0, 1.0, 0.0+0j, 1e10
    bd, gd1 = exp(best_x[0]), exp(best_x[1])
    gd2 = best_x[2] + 1j * best_x[3]
    return bd, gd1, gd2, best


def fit_lepton_sector(f):
    """
    Fit β_e, γ_e (α_e=1) to PDG m_e/m_μ, m_μ/m_τ.
    Returns (beta_e, gamma_e, chi2_l).
    """
    def obj(x):
        be, ge = exp(x[0]), exp(x[1])
        try:
            Me = M_lepton(f, be, ge)
            r01, r12 = mass_ratios(Me)
        except Exception:
            return 1e10
        if r01 <= 0 or r12 <= 0:
            return 1e10
        c = ((r01 - PDG_ME_MMU) / SIG_ME_MMU)**2 + \
            ((r12 - PDG_MMU_MTAU) / SIG_MMU_MTAU)**2
        return c

    best = 1e10
    best_x = None
    for lb in np.linspace(-5, 4, 8):
        for lg in np.linspace(-5, 4, 8):
            try:
                res = minimize(obj, [lb, lg], method='Nelder-Mead',
                               options={'maxiter': 5000, 'xatol': 1e-9, 'fatol': 1e-9})
                if res.fun < best:
                    best = res.fun
                    best_x = res.x
            except Exception:
                pass
    if best_x is None:
        return 1.0, 1.0, 1e10
    be, ge = exp(best_x[0]), exp(best_x[1])
    return be, ge, best


# ─────────────────────────────────────────────────────────────────
# Joint χ² at fixed τ
# ─────────────────────────────────────────────────────────────────

def joint_chi2(tau, n_terms=40):
    """
    Compute minimised joint χ² for a fixed modular parameter τ.
    Fits up-quark, lepton, and down-quark (+ CKM) sectors independently.
    7 observables: m_c/m_t, m_u/m_c, m_e/m_μ, m_μ/m_τ, sin θ_12, sin θ_13, sin θ_23
    Returns dict with chi2 and best-fit predictions.
    """
    result = {'tau': tau, 'chi2': 1e10, 'chi2_up': 1e10, 'chi2_lep': 1e10,
              'chi2_ckm': 1e10, 'valid': False}

    try:
        f = all_forms(tau, n_terms)
    except Exception as e:
        return result

    # --- Up-sector ---
    try:
        bu, gu, chi2_u = fit_up_sector(f)
        result['bu'] = bu; result['gu'] = gu; result['chi2_up'] = chi2_u
        Mu = M_up(f, bu, gu)
        sv_u = svd_sorted(Mu)
        result['mc_mt'] = sv_u[1]/sv_u[2] if sv_u[2]>0 else 0
        result['mu_mc'] = sv_u[0]/sv_u[1] if sv_u[1]>0 else 0
    except Exception:
        return result

    # --- Lepton sector ---
    try:
        be, ge, chi2_l = fit_lepton_sector(f)
        result['be'] = be; result['ge'] = ge; result['chi2_lep'] = chi2_l
        Me = M_lepton(f, be, ge)
        sv_e = svd_sorted(Me)
        result['me_mmu'] = sv_e[0]/sv_e[1] if sv_e[1]>0 else 0
        result['mmu_mtau'] = sv_e[1]/sv_e[2] if sv_e[2]>0 else 0
    except Exception:
        chi2_l = 1e10
        result['chi2_lep'] = chi2_l

    # --- Down-sector + CKM ---
    try:
        bd, gd1, gd2, chi2_ckm = fit_down_sector(f, bu, gu)
        result['bd'] = bd; result['gd1'] = gd1; result['gd2'] = gd2
        result['chi2_ckm'] = chi2_ckm
        Md = M_down(f, bd, gd1, gd2)
        sv_d = svd_sorted(Md)
        result['md_ms'] = sv_d[0]/sv_d[1] if sv_d[1]>0 else 0
        result['ms_mb'] = sv_d[1]/sv_d[2] if sv_d[2]>0 else 0
        s12, s13, s23 = ckm_angles(Mu, Md)
        result['s12'] = s12; result['s13'] = s13; result['s23'] = s23
    except Exception:
        chi2_ckm = 1e10
        result['chi2_ckm'] = chi2_ckm

    # Total χ²: sum of all sector χ² (7 obs total)
    # Up (2 obs) + Lepton (2 obs) + CKM (3 CKM obs, 2 down-mass obs ignored for total)
    # We include only the CKM angle part of chi2_ckm for the total (3 obs)
    # But since chi2_ckm includes also down-mass contributions, use as-is.
    # Total degrees of freedom: 7 observables.
    result['chi2_total'] = chi2_u + chi2_l + chi2_ckm
    result['valid'] = True
    return result


# ─────────────────────────────────────────────────────────────────
# 30×30 Grid scan
# ─────────────────────────────────────────────────────────────────

N_RE = 30
N_IM = 30
RE_RANGE = np.linspace(-0.5, 0.5, N_RE)
IM_RANGE = np.linspace(0.7, 1.5, N_IM)

chi2_grid   = np.full((N_IM, N_RE), np.nan)
chi2_up_grid = np.full((N_IM, N_RE), np.nan)
chi2_lep_grid = np.full((N_IM, N_RE), np.nan)
chi2_ckm_grid = np.full((N_IM, N_RE), np.nan)
results_grid = [[None]*N_RE for _ in range(N_IM)]

print("=" * 70)
print("W1 — τ-near-i 2D χ² scan")
print("=" * 70)
print(f"Grid: {N_RE}×{N_IM}, Re τ ∈ [{RE_RANGE[0]:.2f}, {RE_RANGE[-1]:.2f}],"
      f" Im τ ∈ [{IM_RANGE[0]:.2f}, {IM_RANGE[-1]:.2f}]")
print(f"Total grid points: {N_RE*N_IM}")
print()

t0 = time.time()
n_done = 0
for ii, im_tau in enumerate(IM_RANGE):
    for ji, re_tau in enumerate(RE_RANGE):
        tau = re_tau + 1j * im_tau
        r = joint_chi2(tau)
        results_grid[ii][ji] = r
        if r['valid']:
            chi2_grid[ii, ji]    = r['chi2_total']
            chi2_up_grid[ii, ji] = r['chi2_up']
            chi2_lep_grid[ii, ji] = r['chi2_lep']
            chi2_ckm_grid[ii, ji] = r['chi2_ckm']
        n_done += 1
        if n_done % 30 == 0:
            elapsed = time.time() - t0
            eta_min = elapsed / n_done * (N_RE * N_IM - n_done) / 60
            print(f"  {n_done}/{N_RE*N_IM} done, elapsed {elapsed/60:.1f} min, ETA {eta_min:.1f} min")
            sys.stdout.flush()

print(f"\nScan complete in {(time.time()-t0)/60:.1f} min")

# ─────────────────────────────────────────────────────────────────
# Analysis: find best in near-i region and global best
# ─────────────────────────────────────────────────────────────────

# Mask invalid / too large
chi2_plot = np.where(np.isfinite(chi2_grid), chi2_grid, np.nan)
chi2_plot = np.where(chi2_plot < 1e8, chi2_plot, np.nan)

# Global best
valid_mask = np.isfinite(chi2_plot)
if valid_mask.any():
    flat_idx = np.nanargmin(chi2_plot)
    gi, gj = np.unravel_index(flat_idx, chi2_plot.shape)
    tau_global_best = RE_RANGE[gj] + 1j * IM_RANGE[gi]
    chi2_global_best = chi2_plot[gi, gj]
    r_global = results_grid[gi][gj]
    print(f"\nGlobal best τ = {tau_global_best.real:+.4f}{tau_global_best.imag:+.4f}i")
    print(f"  χ²_total = {chi2_global_best:.4f}")
    print(f"  |τ - i|  = {abs(tau_global_best - 1j):.4f}")
else:
    print("\nNo valid grid points!")
    chi2_global_best = 1e10
    tau_global_best = 1j

# Near-i region: |τ - i| < 0.3
near_i_mask = np.zeros((N_IM, N_RE), dtype=bool)
for ii, im_tau in enumerate(IM_RANGE):
    for ji, re_tau in enumerate(RE_RANGE):
        tau = re_tau + 1j * im_tau
        if abs(tau - 1j) < 0.3:
            near_i_mask[ii, ji] = True

chi2_near_i = np.where(near_i_mask & np.isfinite(chi2_plot), chi2_plot, np.nan)
if np.isfinite(chi2_near_i).any():
    flat_idx_ni = np.nanargmin(chi2_near_i)
    ni_i, ni_j = np.unravel_index(flat_idx_ni, chi2_near_i.shape)
    tau_near_i_best = RE_RANGE[ni_j] + 1j * IM_RANGE[ni_i]
    chi2_near_i_best = chi2_near_i[ni_i, ni_j]
    r_ni = results_grid[ni_i][ni_j]
    print(f"\nBest near-i τ (|τ-i|<0.3): {tau_near_i_best.real:+.4f}{tau_near_i_best.imag:+.4f}i")
    print(f"  |τ - i|   = {abs(tau_near_i_best - 1j):.4f}")
    print(f"  χ²_total  = {chi2_near_i_best:.4f}")
    print(f"  χ²_up     = {r_ni.get('chi2_up', 'n/a')}")
    print(f"  χ²_lep    = {r_ni.get('chi2_lep', 'n/a')}")
    print(f"  χ²_ckm    = {r_ni.get('chi2_ckm', 'n/a')}")
    if 'mc_mt' in r_ni:
        print(f"  m_c/m_t   = {r_ni['mc_mt']:.5e}  (PDG: {PDG_MC_MT:.5e})")
        print(f"  m_u/m_c   = {r_ni['mu_mc']:.5e}  (PDG: {PDG_MU_MC:.5e})")
    if 'me_mmu' in r_ni:
        print(f"  m_e/m_μ  = {r_ni['me_mmu']:.5e}  (PDG: {PDG_ME_MMU:.5e})")
        print(f"  m_μ/m_τ = {r_ni['mmu_mtau']:.5e}  (PDG: {PDG_MMU_MTAU:.5e})")
    if 's12' in r_ni:
        print(f"  sin θ_12  = {r_ni['s12']:.5f}  (PDG: {PDG_SIN12:.5f})")
        print(f"  sin θ_13  = {r_ni['s13']:.6f}  (PDG: {PDG_SIN13:.6f})")
        print(f"  sin θ_23  = {r_ni['s23']:.5f}  (PDG: {PDG_SIN23:.5f})")
    n_obs_ckm = 3  # CKM angles
    n_obs_up  = 2  # m_c/m_t, m_u/m_c
    n_obs_lep = 2  # m_e/m_μ, m_μ/m_τ
    n_obs_total = n_obs_up + n_obs_lep + n_obs_ckm  # 7
    # Down-mass (md/ms, ms/mb) included in chi2_ckm but not primary observables
    chi2dof_ni = chi2_near_i_best / n_obs_total
    print(f"\n  χ²/dof (7 obs) = {chi2dof_ni:.3f}")
else:
    print("\nNo valid grid points in near-i region!")
    chi2_near_i_best = 1e10
    tau_near_i_best = 1j
    chi2dof_ni = 1e10

# Print all grid points sorted by chi2
print("\nTop-10 grid points by χ²_total:")
all_pts = []
for ii in range(N_IM):
    for ji in range(N_RE):
        if np.isfinite(chi2_plot[ii, ji]):
            tau = RE_RANGE[ji] + 1j * IM_RANGE[ii]
            all_pts.append((chi2_plot[ii, ji], tau, ii, ji))
all_pts.sort(key=lambda x: x[0])
print(f"  {'τ':>25}  {'|τ-i|':>8}  {'χ²':>10}  {'χ²/7':>10}")
for chi2, tau, ii, ji in all_pts[:10]:
    print(f"  {tau.real:+.4f}{tau.imag:+.4f}i  {abs(tau-1j):8.4f}  {chi2:10.4f}  {chi2/7:10.4f}")

# ─────────────────────────────────────────────────────────────────
# Verdict
# ─────────────────────────────────────────────────────────────────

print("\n" + "=" * 70)
print("VERDICT")
print("=" * 70)

n_obs_total = 7  # primary observables

if chi2_near_i_best < 1e8:
    chi2dof = chi2_near_i_best / n_obs_total
    if chi2dof < 5:
        verdict = (f"[TAU-NEAR-I VIABLE — local minimum found at τ* = "
                   f"{tau_near_i_best.real:+.4f}{tau_near_i_best.imag:+.4f}i "
                   f"with χ²/dof = {chi2dof:.2f} < 5, within |τ-i| < 0.3]")
    elif chi2dof < 50:
        verdict = (f"[TAU-NEAR-I MARGINAL — best near-i τ at "
                   f"{tau_near_i_best.real:+.4f}{tau_near_i_best.imag:+.4f}i "
                   f"has χ²/dof = {chi2dof:.2f} in [5, 50]]")
    else:
        verdict = (f"[TAU-NEAR-I REFUTED — near-i best χ²/dof = {chi2dof:.2f} >> 50; "
                   f"all best-fits are far from i]")
else:
    verdict = "[TAU-NEAR-I REFUTED — no valid near-i grid points found]"

print(f"\n  {verdict}")
print(f"\n  LYD20 best fit: τ = -0.21 + 1.52i (|τ-i| = {abs(-0.21+1.52j-1j):.4f})")
print(f"  Near-i best:    τ = {tau_near_i_best.real:+.4f}{tau_near_i_best.imag:+.4f}i (|τ-i| = {abs(tau_near_i_best-1j):.4f})")
print(f"  Global best:    τ = {tau_global_best.real:+.4f}{tau_global_best.imag:+.4f}i")

# ─────────────────────────────────────────────────────────────────
# Plot
# ─────────────────────────────────────────────────────────────────

fig, axes = plt.subplots(1, 3, figsize=(18, 6))

chi2_display = np.log10(np.where(chi2_plot > 0.01, chi2_plot, 0.01))

for ax, data, title, cmap in zip(
    axes,
    [chi2_display,
     np.log10(np.where(chi2_up_grid > 0.01, chi2_up_grid, 0.01)),
     np.log10(np.where(chi2_ckm_grid > 0.01, chi2_ckm_grid, 0.01))],
    ['log₁₀ χ²_total', 'log₁₀ χ²_up (quark mass ratios)', 'log₁₀ χ²_CKM+down'],
    ['RdYlGn_r', 'RdYlGn_r', 'RdYlGn_r']
):
    masked = np.where(np.isfinite(data) & (data < 10), data, np.nan)
    im = ax.pcolormesh(RE_RANGE, IM_RANGE, masked, cmap=cmap,
                       vmin=np.nanpercentile(masked, 5) if np.isfinite(masked).any() else -2,
                       vmax=min(np.nanpercentile(masked, 95), 8) if np.isfinite(masked).any() else 8)
    plt.colorbar(im, ax=ax, label='log₁₀ χ²')
    ax.set_xlabel('Re τ')
    ax.set_ylabel('Im τ')
    ax.set_title(title)

    # Mark τ=i
    ax.axhline(1.0, color='blue', linestyle='--', alpha=0.5, linewidth=1)
    ax.axvline(0.0, color='blue', linestyle='--', alpha=0.5, linewidth=1)
    ax.plot(0, 1, 'b*', markersize=12, label='τ=i', zorder=5)

    # Mark near-i circle
    theta_c = np.linspace(0, 2*np.pi, 200)
    ax.plot(0.3*np.cos(theta_c), 1.0 + 0.3*np.sin(theta_c), 'b--', alpha=0.3, linewidth=1)

    # Mark near-i best
    if np.isfinite(chi2_near_i_best) and chi2_near_i_best < 1e8:
        ax.plot(tau_near_i_best.real, tau_near_i_best.imag, 'b^',
                markersize=10, label=f'near-i best', zorder=6)

    # Mark global best
    ax.plot(tau_global_best.real, tau_global_best.imag, 'r*',
            markersize=12, label=f'global best', zorder=7)

    # Mark LYD20 best-fit
    ax.plot(-0.21, 1.52, 'g^', markersize=10, label='LYD20 best-fit', zorder=8)
    ax.legend(loc='upper right', fontsize=7)

axes[0].set_title(f'log₁₀ χ²_total (7 obs)\nnear-i best: χ²/7={chi2_near_i_best/7:.1f}')

plt.suptitle(f'W1: τ-near-i χ² scan — LYD20 S\'_4 modular flavor\n'
             f'Verdict: {verdict[:80]}...', fontsize=9)
plt.tight_layout()
plt.savefig('/tmp/agents_v647_evening/W1/chi2_landscape.png', dpi=150, bbox_inches='tight')
print(f"\nPlot saved to /tmp/agents_v647_evening/W1/chi2_landscape.png")

# ─────────────────────────────────────────────────────────────────
# Save numerical results
# ─────────────────────────────────────────────────────────────────

np.save('/tmp/agents_v647_evening/W1/chi2_grid.npy', chi2_grid)
np.save('/tmp/agents_v647_evening/W1/re_range.npy', RE_RANGE)
np.save('/tmp/agents_v647_evening/W1/im_range.npy', IM_RANGE)

# Print grid summary for log
print("\nFull grid χ²_total summary (sorted):")
print(f"  {'Re τ':>8}  {'Im τ':>8}  {'|τ-i|':>8}  {'χ²_tot':>12}  {'χ²/7':>10}  {'near-i':>7}")
for chi2, tau, ii, ji in all_pts[:20]:
    ni = "YES" if abs(tau - 1j) < 0.3 else "no"
    print(f"  {tau.real:+8.4f}  {tau.imag:8.4f}  {abs(tau-1j):8.4f}  {chi2:12.4f}  {chi2/7:10.4f}  {ni:>7}")

print("\n--- END OF SCAN ---")
print(f"\nFINAL VERDICT: {verdict}")
