"""
A16 -- PMNS angle prediction at W1 attractor tau_l = -0.19 + 1.00i

Implements LYD20 (arXiv:2006.10722) joint quark-lepton unified model
lepton sector (Eq. 119-120, p.36 of paper):

  Charged lepton M_e (Eq. 120): 3x3 with Y^(4)_3, Y^(2)_3, Y^(3)_3hat rows
  Type-I seesaw:
    Dirac M_D (Eq. 120): uses Y^(2)_2 (doublet) and Y^(2)_3 (triplet)
    Majorana M_N = Lambda * antidiag(1,1,1) (single param Lambda)
    Light neutrino:  M_nu = -M_D^T  M_N^-1  M_D  (factor v_u^2 absorbed)

LYD20 best-fit at tau = -0.2123 + 1.5201i (their Eq. 125):
    sin^2 theta_12 = 0.34981
    sin^2 theta_13 = 0.02193
    sin^2 theta_23 = 0.56393
    delta_CP       = 266.1824 deg
  Free params for neutrino: g2/g1, g1^2 v_u^2 / Lambda  (only 2 reals)

W1 attractor (this script):
    tau_l = -0.1897 + 1.0034i  (from W1 verdict log, also tau_q at W1 best)
  Refit (g2/g1, alpha_e, beta_e, gamma_e, m_nu_scale) at this tau.

Deliverable:
  Predicted (sin^2 theta_12, sin^2 theta_13, sin^2 theta_23, delta_CP)
  at the W1 attractor, vs PDG 2024 + JUNO 2026 reach + DUNE 2030+ reach.

NO Mistral cross-check (STRICT BAN per memory).
NO live arXiv API (paper already verified by direct PDF read).
"""

import numpy as np
from numpy import pi, sqrt, exp, sin, cos
from scipy.linalg import svd, eigh
from scipy.optimize import minimize, differential_evolution
import json, warnings
warnings.filterwarnings("ignore")

# ----------------------------------------------------------------
# Modular forms (transcribed from I1_5/lepton_unified.py + LYD20)
# ----------------------------------------------------------------
N_TERMS = 60

def eta(tau):
    q = exp(2j * pi * tau)
    out = q ** (1.0 / 24.0)
    for n in range(1, N_TERMS):
        out *= (1.0 - q ** n)
    return out


def weight1_forms(tau):
    """Y1, Y2, Y3 -- weight-1 in 3hat' rep."""
    e1 = eta(4 * tau) ** 4 / eta(2 * tau) ** 2
    e2 = eta(2 * tau) ** 10 / (eta(4 * tau) ** 4 * eta(tau) ** 4)
    e3 = eta(2 * tau) ** 4 / eta(tau) ** 2
    omega = exp(2j * pi / 3.0)
    s2 = sqrt(2.0); s3 = sqrt(3.0)
    Y1 = 4 * s2 * e1 + 1j * s2 * e2 + 2 * s2 * (1 - 1j) * e3
    Y2 = (-2 * s2 * (1 + s3) * omega ** 2 * e1
          - 1j * (1 - s3) / s2 * omega ** 2 * e2
          + 2 * s2 * (1 - 1j) * omega ** 2 * e3)
    Y3 = ( 2 * s2 * (s3 - 1) * omega * e1
          - 1j * (1 + s3) / s2 * omega * e2
          + 2 * s2 * (1 - 1j) * omega * e3)
    return Y1, Y2, Y3


def all_forms(tau):
    """All needed Y^(k)_r modular forms (LYD20 Appendix B)."""
    Y1, Y2, Y3 = weight1_forms(tau)
    # Weight-2 triplet 3:  Y^(2)_3 = (Y3^(2), Y4^(2), Y5^(2))
    Y2_3 = 2 * Y1 ** 2 - 2 * Y2 * Y3
    Y2_4 = 2 * Y3 ** 2 - 2 * Y1 * Y2
    Y2_5 = 2 * Y2 ** 2 - 2 * Y1 * Y3
    # Weight-2 doublet 2:  Y^(2)_2 = (Y1^(2), Y2^(2))
    Y2_1 = Y2 ** 2 + 2 * Y1 * Y3
    Y2_2 = Y3 ** 2 + 2 * Y1 * Y2
    # Weight-3 hat3:  Y^(3)_3hat = (Y2^(3), Y3^(3), Y4^(3))
    Y3_2 = 2 * (2 * Y1 ** 3 - Y2 ** 3 - Y3 ** 3)
    Y3_3 = 6 * Y3 * (Y2 ** 2 - Y1 * Y3)
    Y3_4 = 6 * Y2 * (Y3 ** 2 - Y1 * Y2)
    # Weight-4 triplet 3:  Y^(4)_3 = (Y4^(4), Y5^(4), Y6^(4))
    # LYD20 Appendix B.6
    Y4_4 = 6 * Y1 * (-Y2 ** 3 + Y3 ** 3)
    Y4_5 = 6 * Y1 * Y3 * (Y2 ** 2 - Y1 * Y3) + 2 * Y2 * (-2 * Y1 ** 3 + Y2 ** 3 + Y3 ** 3)
    Y4_6 = 6 * Y1 * Y2 * (Y1 * Y2 - Y3 ** 2) - 2 * Y3 * (-2 * Y1 ** 3 + Y2 ** 3 + Y3 ** 3)
    return dict(Y1=Y1, Y2=Y2, Y3=Y3,
                Y2_1=Y2_1, Y2_2=Y2_2,
                Y2_3=Y2_3, Y2_4=Y2_4, Y2_5=Y2_5,
                Y3_2=Y3_2, Y3_3=Y3_3, Y3_4=Y3_4,
                Y4_4=Y4_4, Y4_5=Y4_5, Y4_6=Y4_6)


# ----------------------------------------------------------------
# Mass matrices (LYD20 Eq. 120)
# ----------------------------------------------------------------
def M_e(F, alpha_e, beta_e, gamma_e):
    """Charged lepton mass matrix.
    Row 0 (E1^c, k=2): alpha_e * Y^(4)_3 = (Y4, Y6, Y5)
    Row 1 (E2^c, k=0): beta_e  * Y^(2)_3 = (Y3, Y5, Y4)
    Row 2 (E3^c, k=1): gamma_e * Y^(3)_3hat = (Y2, Y4, Y3)
    (Note column ordering matches LYD20 Eq. 120: (Y4,Y6,Y5)/(Y3,Y5,Y4)/(Y2,Y4,Y3))
    """
    return np.array([
        [alpha_e * F["Y4_4"], alpha_e * F["Y4_6"], alpha_e * F["Y4_5"]],
        [beta_e  * F["Y2_3"], beta_e  * F["Y2_5"], beta_e  * F["Y2_4"]],
        [gamma_e * F["Y3_2"], gamma_e * F["Y3_4"], gamma_e * F["Y3_3"]],
    ], dtype=complex)


def M_D(F, g1, g2):
    """Dirac neutrino mass matrix (LYD20 Eq. 120, transcribed exactly from PDF page 36).

    M_D = [ [ 0,                       g1 Y1^(2) - g2 Y5^(2),  g1 Y2^(2) + g2 Y4^(2) ],
            [ g1 Y1^(2) + g2 Y5^(2),   g1 Y2^(2),              -g2 Y3^(2) ],
            [ g1 Y2^(2) - g2 Y4^(2),   g2 Y3^(2),               g1 Y1^(2) ] ] * v_u

    In our shorthand: Y1^(2)=Y2_1, Y2^(2)=Y2_2 (doublet 2);
                       Y3^(2)=Y2_3, Y4^(2)=Y2_4, Y5^(2)=Y2_5 (triplet 3).
    v_u absorbed; ratios are scale-invariant.
    """
    return np.array([
        [0.0,
         g1 * F["Y2_1"] - g2 * F["Y2_5"],
         g1 * F["Y2_2"] + g2 * F["Y2_4"]],
        [g1 * F["Y2_1"] + g2 * F["Y2_5"],
         g1 * F["Y2_2"],
         -g2 * F["Y2_3"]],
        [g1 * F["Y2_2"] - g2 * F["Y2_4"],
         g2 * F["Y2_3"],
         g1 * F["Y2_1"]],
    ], dtype=complex)


def M_N_inv():
    """Inverse Majorana mass matrix.
    M_N = Lambda * antidiag(1,1,1) (paper Eq. 120: ((1,0,0),(0,0,1),(0,1,0))*Lambda)
    => M_N^-1 = (1/Lambda) * same matrix (it is its own inverse up to factor).
    Lambda is absorbed into overall neutrino mass scale.
    """
    return np.array([[1, 0, 0],
                     [0, 0, 1],
                     [0, 1, 0]], dtype=complex)


# ----------------------------------------------------------------
# PMNS extraction
# ----------------------------------------------------------------
def diag_charged_lepton(Me):
    """Diagonalize Me Me^dagger; return left-rotation U_eL with rows
    sorted ascending by mass."""
    H = Me @ Me.conj().T
    w, U = eigh(H)            # ascending eigenvalues
    return U, np.sqrt(np.maximum(w, 0.0))


def diag_neutrino(Mnu):
    """Diagonalize symmetric complex M_nu via Takagi decomposition.
    M_nu = U_nu* diag(m_i) U_nu^dagger
    Returns U_nu (with rows sorted ascending in mass) and masses m_i.
    """
    # Takagi: M = U^* d U^dagger, d real positive. Use SVD trick:
    U_, s, Vh = svd(Mnu)
    # Diagonal phases: M_nu being symmetric => U = U_ * sqrt(diag(Vh @ U_))
    # but a simpler robust route is to compute eigenvalues of M_nu^dagger M_nu
    # then build U_nu from eigh(M_nu^dagger M_nu). Phase ambiguity absorbed.
    H = Mnu.conj().T @ Mnu
    w, U = eigh(H)            # ascending
    # diag(s) and diag(sqrt(w)) should match (up to ordering)
    m = np.sqrt(np.maximum(w, 0.0))
    # Recover phase: M_nu @ U should equal U^* diag(m_i*phase)
    # For PMNS extraction we only need |U| up to Majorana phases, plus delta_CP
    # Compute diagonalization phases for delta_CP:
    M_diag = U.conj().T @ Mnu @ U.conj()
    # M_diag should be diagonal complex; its diagonal phases give Majorana phases
    return U, m, M_diag


def pmns_angles(Me, Mnu):
    """Extract PMNS angles + delta_CP from charged-lepton + neutrino mass matrices.
    Convention: rows of U_e and U_nu sorted ascending in mass; PMNS = U_eL^dagger U_nu.
    Returns (s12_sq, s13_sq, s23_sq, delta_CP_deg, J_CP, m_nu (3,)).
    """
    Ue, me_sv = diag_charged_lepton(Me)
    Unu, m_nu, _ = diag_neutrino(Mnu)
    U = Ue.conj().T @ Unu        # PMNS
    aU = np.abs(U)
    Ue3 = aU[0, 2]
    s13_sq = Ue3 ** 2
    denom2 = max(1.0 - s13_sq, 1e-30)
    s12_sq = (aU[0, 1] ** 2) / denom2
    s23_sq = (aU[1, 2] ** 2) / denom2
    # Jarlskog:  J = Im(U_{e1} U_{mu2} U*_{e2} U*_{mu1})  (PDG std parametrisation)
    J = np.imag(U[0, 0] * U[1, 1] * np.conj(U[0, 1]) * np.conj(U[1, 0]))
    # delta_CP from J = c12 c13^2 c23 s12 s13 s23 sin(delta) + sign convention
    s12 = sqrt(max(s12_sq, 0)); c12 = sqrt(max(1 - s12_sq, 0))
    s13 = sqrt(max(s13_sq, 0)); c13 = sqrt(max(1 - s13_sq, 0))
    s23 = sqrt(max(s23_sq, 0)); c23 = sqrt(max(1 - s23_sq, 0))
    Jmax = c12 * c13 * c13 * c23 * s12 * s13 * s23
    if Jmax > 1e-15:
        sin_d = J / Jmax
        sin_d = np.clip(sin_d, -1.0, 1.0)
        delta_deg = float(np.degrees(np.arcsin(sin_d)))
        # The arcsin gives delta in (-90, 90); fix quadrant by checking U_{e1}'s phase
        # For modular models near tau ~ i, delta is typically near 270 deg
        # Use a more direct extraction:
        # delta_CP = -arg(U_e1 U*_e3 U*_mu1 U_mu3 / (c12 c23 s12 s13 s23 c13^2))
        # Actually: standard PDG Dirac phase convention from
        #    U_e3 = s13 e^{-i delta} (real basis), so delta = -arg(U_e3 / s13)
        # but in our generic complex U we instead read full delta from PMNS rephasing.
        delta_full = -np.angle(np.conj(U[0, 2]) * U[0, 1] * U[1, 2] * np.conj(U[1, 1])
                                / (c12 * s12 * s23 * c23 * s13 * c13 * c13))
        delta_full_deg = float(np.degrees(delta_full)) % 360
    else:
        delta_full_deg = float("nan")
    return s12_sq, s13_sq, s23_sq, delta_full_deg, float(J), m_nu


# ----------------------------------------------------------------
# Light neutrino mass matrix from seesaw
# ----------------------------------------------------------------
def light_nu_mass(F, g1, g2, mass_scale):
    """M_nu (light) = -M_D^T M_N^-1 M_D * (v_u^2 / Lambda)"""
    MD = M_D(F, g1, g2)
    MNi = M_N_inv()
    Mnu = -(MD.T @ MNi @ MD) * mass_scale
    return Mnu


# ----------------------------------------------------------------
# PDG 2024 lepton sector targets (NuFIT 5.3 normal ordering, 2024)
# ----------------------------------------------------------------
# NuFIT 5.3 (Esteban+ 2024, arXiv:2410.05380) normal ordering best fit:
PDG_NU = {
    "sin2_12":   (0.307,    0.012),     # solar
    "sin2_13":   (0.02195,  0.0007),    # reactor (Daya Bay+RENO+T2K dominated)
    "sin2_23":   (0.572,    0.020),     # atmospheric (octant: upper)
    "delta_CP":  (197.0,    25.0),      # deg (NO best-fit, ~190-220)
    "Dm21_sq":   (7.49e-5,  0.20e-5),   # eV^2 (solar mass split)
    "Dm32_sq":   (2.534e-3, 0.026e-3),  # eV^2 (atm mass split, NO)
}
PDG_M_E_MU  = (4.836e-3, 2.0e-5)
PDG_M_MU_TAU = (5.946e-2, 3.0e-4)


def chi2_neutrino(params, F, mass_split_only=False):
    """Fit (g2_g1, log_mass_scale, log_alpha_e, log_beta_e, log_gamma_e)
    to PMNS angles + neutrino mass splittings + charged-lepton ratios."""
    g2_g1, log_mass, log_ae, log_be, log_ge = params
    g1 = 1.0
    g2 = g2_g1
    mass_scale = exp(log_mass)
    alpha_e = exp(log_ae)
    beta_e  = exp(log_be)
    gamma_e = exp(log_ge)

    Me = M_e(F, alpha_e, beta_e, gamma_e)
    Mnu = light_nu_mass(F, g1, g2, mass_scale)

    try:
        s12, s13, s23, dCP, J, m_nu = pmns_angles(Me, Mnu)
        # charged-lepton ratios
        _, sv_e = diag_charged_lepton(Me)
        sv_e = np.sort(sv_e)
        if sv_e[2] < 1e-30 or sv_e[1] < 1e-30:
            return 1e10
        me_mmu = sv_e[0] / sv_e[1]
        mmu_mt = sv_e[1] / sv_e[2]
    except Exception:
        return 1e10

    # mass splittings
    Dm21 = m_nu[1] ** 2 - m_nu[0] ** 2
    Dm32 = m_nu[2] ** 2 - m_nu[1] ** 2

    chi2 = 0.0
    # PMNS angles (from NuFIT 5.3)
    chi2 += ((s12 - PDG_NU["sin2_12"][0]) / PDG_NU["sin2_12"][1]) ** 2
    chi2 += ((s13 - PDG_NU["sin2_13"][0]) / PDG_NU["sin2_13"][1]) ** 2
    chi2 += ((s23 - PDG_NU["sin2_23"][0]) / PDG_NU["sin2_23"][1]) ** 2
    # mass splittings (in units of eV^2)
    if Dm21 > 0:
        chi2 += ((Dm21 - PDG_NU["Dm21_sq"][0]) / PDG_NU["Dm21_sq"][1]) ** 2
    else:
        chi2 += 100  # wrong sign penalty
    if Dm32 > 0:
        chi2 += ((Dm32 - PDG_NU["Dm32_sq"][0]) / PDG_NU["Dm32_sq"][1]) ** 2
    else:
        chi2 += 100
    # charged-lepton mass ratios (must hold exactly)
    chi2 += ((me_mmu - PDG_M_E_MU[0]) / PDG_M_E_MU[1]) ** 2
    chi2 += ((mmu_mt - PDG_M_MU_TAU[0]) / PDG_M_MU_TAU[1]) ** 2

    if not np.isfinite(chi2) or chi2 < 0:
        return 1e10
    return chi2


# ----------------------------------------------------------------
# Main: predict PMNS at W1 attractor tau_l = -0.19 + 1.00i
# ----------------------------------------------------------------
def fit_at_tau(tau_l, label, n_starts=200, seed=42):
    """Fit (g2/g1, mass_scale, alpha_e, beta_e, gamma_e) at fixed tau_l."""
    F = all_forms(tau_l)
    rng = np.random.default_rng(seed)
    best = (1e20, None)
    bounds = [(-10.0, 10.0),     # g2/g1 (LYD20 best ~ 0.68)
              (-15.0, 5.0),      # log(g1^2 v_u^2 / Lambda) in eV
              (-5.0, 8.0),       # log alpha_e
              (-5.0, 8.0),       # log beta_e
              (-5.0, 8.0)]       # log gamma_e
    # Multi-start DE with different seeds (PMNS landscape is multimodal)
    candidates = []
    for s in range(5):
        r = differential_evolution(
            chi2_neutrino, bounds, args=(F,),
            maxiter=3000, tol=1e-10, seed=seed + 100 * s, popsize=40,
            mutation=(0.5, 1.5), recombination=0.9, workers=1, disp=False,
            init="sobol" if s == 0 else "latinhypercube"
        )
        candidates.append((float(r.fun), r.x))
    candidates.sort(key=lambda c: c[0])
    best = candidates[0]

    # Polish each top candidate
    for cand in candidates[:3]:
        x_try = cand[1]
        for _ in range(5):
            x0 = x_try + 0.05 * rng.standard_normal(len(x_try))
            try:
                r = minimize(chi2_neutrino, x0, args=(F,), method="Nelder-Mead",
                             options={"xatol": 1e-12, "fatol": 1e-12, "maxiter": 100000})
                if r.fun < best[0]:
                    best = (float(r.fun), r.x)
            except Exception:
                pass

    chi2_final, x = best
    g2_g1, log_mass, log_ae, log_be, log_ge = x
    g1 = 1.0
    g2 = g2_g1
    mass_scale = exp(log_mass)
    alpha_e = exp(log_ae)
    beta_e  = exp(log_be)
    gamma_e = exp(log_ge)
    Me  = M_e(F, alpha_e, beta_e, gamma_e)
    Mnu = light_nu_mass(F, g1, g2, mass_scale)
    s12, s13, s23, dCP, J, m_nu = pmns_angles(Me, Mnu)
    _, sv_e = diag_charged_lepton(Me)
    sv_e = np.sort(sv_e)
    me_mmu = float(sv_e[0] / sv_e[1])
    mmu_mt = float(sv_e[1] / sv_e[2])
    Dm21 = float(m_nu[1] ** 2 - m_nu[0] ** 2)
    Dm32 = float(m_nu[2] ** 2 - m_nu[1] ** 2)
    return {
        "label": label,
        "tau_l": [float(tau_l.real), float(tau_l.imag)],
        "chi2_min": float(chi2_final),
        "params": {
            "g2/g1":      float(g2_g1),
            "mass_scale_eV": float(mass_scale),
            "alpha_e":    float(alpha_e),
            "beta_e":     float(beta_e),
            "gamma_e":    float(gamma_e),
        },
        "predicted": {
            "sin2_theta_12": float(s12),
            "sin2_theta_13": float(s13),
            "sin2_theta_23": float(s23),
            "delta_CP_deg":  float(dCP),
            "J_PMNS":        float(J),
            "m_nu_eV":       [float(x) for x in m_nu],
            "Dm21_sq_eV2":   Dm21,
            "Dm32_sq_eV2":   Dm32,
            "sum_m_nu_eV":   float(sum(m_nu)),
            "m_e/m_mu":      me_mmu,
            "m_mu/m_tau":    mmu_mt,
        },
    }


def main():
    print("=" * 72)
    print("A16 -- PMNS PREDICTION at W1 attractor tau_l = -0.19 + 1.00i")
    print("=" * 72)
    print()
    print("LYD20 model: arXiv:2006.10722 unified quark-lepton (Eq. 119-120)")
    print("Neutrino sector: type-I seesaw with N^c ~ two triplets of S'_4")
    print()

    # --- Step 1: reproduce LYD20 result at their tau ---
    tau_LYD = -0.2123 + 1.5201j
    print(f"[1] Sanity check: refit at LYD20's tau = {tau_LYD}")
    print(f"    (LYD20 reports sin^2 t12=0.34981, sin^2 t13=0.02193,")
    print(f"     sin^2 t23=0.56393, delta_CP=266.18 deg)")
    res_LYD = fit_at_tau(tau_LYD, "LYD20_check")
    print(f"    chi2_min = {res_LYD['chi2_min']:.3f}")
    p = res_LYD["predicted"]
    print(f"    sin^2 t12 = {p['sin2_theta_12']:.5f}  (LYD20: 0.34981)")
    print(f"    sin^2 t13 = {p['sin2_theta_13']:.5f}  (LYD20: 0.02193)")
    print(f"    sin^2 t23 = {p['sin2_theta_23']:.5f}  (LYD20: 0.56393)")
    print(f"    delta_CP  = {p['delta_CP_deg']:.2f} deg (LYD20: 266.18 deg)")
    print(f"    Dm21^2    = {p['Dm21_sq_eV2']:.3e} eV^2  (NuFIT: 7.49e-5)")
    print(f"    Dm32^2    = {p['Dm32_sq_eV2']:.3e} eV^2  (NuFIT: 2.534e-3)")
    print()

    # --- Step 2: predict at W1 attractor ---
    tau_W1 = -0.1897 + 1.0034j
    print(f"[2] Predict at W1 attractor tau_l = {tau_W1}")
    res_W1 = fit_at_tau(tau_W1, "W1_attractor")
    print(f"    chi2_min = {res_W1['chi2_min']:.3f}")
    p = res_W1["predicted"]
    print(f"    sin^2 t12 = {p['sin2_theta_12']:.5f}")
    print(f"    sin^2 t13 = {p['sin2_theta_13']:.5f}")
    print(f"    sin^2 t23 = {p['sin2_theta_23']:.5f}")
    print(f"    delta_CP  = {p['delta_CP_deg']:.2f} deg")
    print(f"    Dm21^2    = {p['Dm21_sq_eV2']:.3e} eV^2")
    print(f"    Dm32^2    = {p['Dm32_sq_eV2']:.3e} eV^2")
    print(f"    sum m_nu  = {p['sum_m_nu_eV']*1e3:.2f} meV")
    print()

    # --- Step 3: also try tau = i exactly (CM-anchored attractor) ---
    tau_i = 0.0 + 1.0j
    print(f"[3] Predict at exact CM point tau_l = i")
    res_i = fit_at_tau(tau_i, "tau_eq_i")
    print(f"    chi2_min = {res_i['chi2_min']:.3f}")
    p = res_i["predicted"]
    print(f"    sin^2 t12 = {p['sin2_theta_12']:.5f}")
    print(f"    sin^2 t13 = {p['sin2_theta_13']:.5f}")
    print(f"    sin^2 t23 = {p['sin2_theta_23']:.5f}")
    print(f"    delta_CP  = {p['delta_CP_deg']:.2f} deg")
    print()

    # --- Compare to PDG ---
    print("=" * 72)
    print("COMPARISON to PDG 2024 / NuFIT 5.3 + experimental projections")
    print("=" * 72)
    print()
    print(f"  PDG/NuFIT 2024 (NO):  sin^2 t13 = {PDG_NU['sin2_13'][0]:.5f} +/- {PDG_NU['sin2_13'][1]:.5f}")
    print(f"  W1 attractor pred:    sin^2 t13 = {res_W1['predicted']['sin2_theta_13']:.5f}")
    print(f"  tau=i pred:           sin^2 t13 = {res_i['predicted']['sin2_theta_13']:.5f}")
    print()
    print("  JUNO 2026+ reach:     sigma(sin^2 t13) ~ 0.0007 (1-2% rel)")
    print("  DUNE 2030+ reach:     sigma(sin^2 t13) ~ 0.0001 (~0.5% rel)")
    print()

    # --- Save JSON deliverable ---
    out = {
        "version": "ECI v6.0.53.2",
        "agent": "A16",
        "date": "2026-05-05",
        "method": "LYD20 (arXiv:2006.10722) unified-model lepton sector,"
                  " refit at W1 attractor tau",
        "pdg_nufit_2024": {
            "sin2_theta_12": list(PDG_NU["sin2_12"]),
            "sin2_theta_13": list(PDG_NU["sin2_13"]),
            "sin2_theta_23": list(PDG_NU["sin2_23"]),
            "delta_CP_deg":  list(PDG_NU["delta_CP"]),
            "Dm21_sq":       list(PDG_NU["Dm21_sq"]),
            "Dm32_sq":       list(PDG_NU["Dm32_sq"]),
        },
        "experimental_reach": {
            "Daya_Bay_RENO_2024": {"sigma_sin2_t13": 0.0007, "year": 2024},
            "JUNO_2026":          {"sigma_sin2_t13": 0.0005, "year": 2026,
                                   "ref": "JUNO Collaboration arXiv:2204.13249"},
            "DUNE_2030":          {"sigma_sin2_t13": 0.0001, "year": 2030,
                                   "ref": "DUNE TDR Vol II arXiv:2002.03005"},
            "T2HK_2030":          {"sigma_delta_CP_deg": 7.0, "year": 2030,
                                   "ref": "Hyper-K Design Report 2018"},
        },
        "fit_LYD20_check":  res_LYD,
        "fit_W1_attractor": res_W1,
        "fit_tau_eq_i":     res_i,
    }

    # --- Verdict ---
    s13_W1 = res_W1["predicted"]["sin2_theta_13"]
    s13_pdg, s13_pdg_sigma = PDG_NU["sin2_13"]
    pull_W1 = (s13_W1 - s13_pdg) / s13_pdg_sigma
    s13_i = res_i["predicted"]["sin2_theta_13"]
    pull_i = (s13_i - s13_pdg) / s13_pdg_sigma

    if abs(pull_W1) > 1.0 and res_W1["chi2_min"] < 50:
        verdict = (f"PREDICTION DIFFERS FROM PDG (testable): "
                   f"W1 attractor predicts sin^2 t13 = {s13_W1:.4f} "
                   f"vs PDG {s13_pdg:.4f} (pull = {pull_W1:.2f} sigma)")
    elif res_W1["chi2_min"] > 50:
        verdict = (f"FIT POOR (chi2 = {res_W1['chi2_min']:.1f}); "
                   f"W1 tau may not accommodate lepton sector")
    else:
        verdict = (f"WITHIN ERRORS: W1 sin^2 t13 = {s13_W1:.4f} "
                   f"vs PDG {s13_pdg:.4f} (pull = {pull_W1:.2f} sigma)")
    out["verdict"] = verdict
    out["pull_W1_vs_PDG_sin2_t13"] = float(pull_W1)
    out["pull_tau_i_vs_PDG_sin2_t13"] = float(pull_i)

    with open("/root/crossed-cosmos/notes/eci_v7_aspiration/A16_THETA13_PREDICTION/theta13_prediction.json", "w") as f:
        json.dump(out, f, indent=2)
    print(f"VERDICT: {verdict}")
    print()
    print("Saved theta13_prediction.json")


if __name__ == "__main__":
    main()
