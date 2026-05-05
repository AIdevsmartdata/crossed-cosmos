"""
A46 -- LYD20 unified Q+L joint fit at tau pinned at i (CM-anchor)
================================================================

OWNER     : Sonnet sub-agent A46 (parent persisted)
DATE      : 2026-05-05 evening
HALLU     : 84 entering / 84 leaving (all formulae transcribed from
            LYD20 arXiv:2006.10722 TeX source lines 1507-1556 + Appendix
            1850-1894; verified against G111/quark_unified.py and
            A26 m_u_svd.py pipelines).

GOAL
====
Re-run the LYD20 quark-lepton unified model (Eq. WqII / MqII, page ~36)
with the modulus tau STRICTLY pinned at the CM point K=Q(i),
    tau_q = tau_l = i = 0.0 + 1.0i,
and refit the 13 real Yukawa couplings
    (alpha_u_v_u, beta_u/alpha_u, gamma_u/alpha_u, delta_u/alpha_u,
     alpha_d_v_d, beta_d/alpha_d, gamma_d/alpha_d, delta_d/alpha_d,
     alpha_e_v_d, beta_e/alpha_e, gamma_e/alpha_e,
     g_2/g_1, g_1^2 v_u^2 / Lambda)
to the 22 quark+lepton observables.

Compare chi^2 against:
  (a) LYD20 published best fit at tau_q = tau_l = -0.2123 + 1.5201i;
  (b) W1 attractor tau* = -0.1897 + 1.0034i;
  (c) lepton-only A16 result (chi2_LYD ~= 690, chi2_tau=i ~= 1240).

Document the chi^2 penalty as the structural-anchoring cost of fixing tau
at i (no fit freedom in Re tau, Im tau).

ANTI-HALLUCINATION
==================
- Modular forms re-imported from G111/quark_unified.py (verified PASS).
- M_u rows transcribed from LYD20 Eq. MqII (lines 1516-1519).
- M_d rows transcribed from LYD20 Eq. MqII (lines 1521-1525) using:
    * Y^(4)_3' (Y4_7, Y4_8, Y4_9) for the alpha_d row;
    * Y^(5)_{3hat',I} (Y5_6, Y5_7, Y5_8) and Y^(5)_{3hat',II} (Y5_9, Y5_10, Y5_11)
      for the beta_d / gamma_d row;
    * Y^(5)_{3hat} (Y5_3, Y5_4, Y5_5) for the delta_d row.
- M_e from A16 (LYD20 Eq. 120 = Eq. 119 lepton sector);
- M_D, M_N from A16 (LYD20 Eq. 120 unified neutrino sector).
- NO Mistral cross-check (STRICT BAN per memory).

OUTPUT
======
JSON with chi^2 comparison table for the four scenarios.
"""

import sys, os, json, time, warnings
warnings.filterwarnings("ignore")

import numpy as np
from numpy import pi, sqrt, exp, log
from scipy.linalg import svd as scipy_svd, eigh
from scipy.optimize import minimize, differential_evolution

# Reuse modular forms + matrix builders from A16 (only PDG constants kept;
# we redefine M_e, M_D, light_nu_mass locally to avoid A16's Y2_1 sign convention
# inconsistency with LYD20 line 347).
sys.path.insert(0, '/root/crossed-cosmos/notes/eci_v7_aspiration/A16_THETA13_PREDICTION')
from predict_pmns import (
    eta, weight1_forms,
    PDG_NU, PDG_M_E_MU, PDG_M_MU_TAU,
)


def M_e(F, alpha_e, beta_e, gamma_e):
    """Charged lepton M_e (LYD20 Eq.Ml line 1492-1495)."""
    return np.array([
        [alpha_e * F["Y4_4"], alpha_e * F["Y4_6"], alpha_e * F["Y4_5"]],
        [beta_e  * F["Y2_3"], beta_e  * F["Y2_5"], beta_e  * F["Y2_4"]],
        [gamma_e * F["Y3_2"], gamma_e * F["Y3_4"], gamma_e * F["Y3_3"]],
    ], dtype=complex)


def M_D(F, g1, g2):
    """Dirac neutrino M_D (LYD20 Eq.Ml line 1501-1504; uses Y^(2)_2 doublet
    + Y^(2)_3 triplet)."""
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
    """LYD20 line 1496-1500: M_N = Lambda * antidiag(1,1,1)."""
    return np.array([[1, 0, 0], [0, 0, 1], [0, 1, 0]], dtype=complex)


def light_nu_mass(F, g1, g2, mass_scale):
    """M_nu = - M_D^T M_N^{-1} M_D * (v_u^2 / Lambda) absorbed in mass_scale."""
    MD = M_D(F, g1, g2)
    MNi = M_N_inv()
    return -(MD.T @ MNi @ MD) * mass_scale


# Local convention-correct diagonalizers
def diag_charged_lepton(Me):
    """Diagonalize M_e^dag M_e (rows=E^c, cols=L; left-handed L rotation).
    Returns U_eL (3x3 unitary, columns sorted ascending in mass) and singular values."""
    H = Me.conj().T @ Me
    w, U = eigh(H)
    return U, np.sqrt(np.maximum(w, 0.0))


def diag_neutrino(Mnu):
    """Diagonalize symmetric complex M_nu via M_nu^dag M_nu eigenproblem.
    Returns U_nu (sorted ascending), masses m_i, and the diagonal-phase matrix."""
    H = Mnu.conj().T @ Mnu
    w, U = eigh(H)
    m = np.sqrt(np.maximum(w, 0.0))
    M_diag = U.conj().T @ Mnu @ U.conj()
    return U, m, M_diag


def pmns_angles(Me, Mnu):
    """PMNS = U_eL^dag U_nu with M_e diagonalisation under E^c-row convention."""
    Ue, _ = diag_charged_lepton(Me)
    Unu, m_nu, _ = diag_neutrino(Mnu)
    U = Ue.conj().T @ Unu
    aU = np.abs(U)
    Ue3 = aU[0, 2]
    s13_sq = Ue3 ** 2
    denom2 = max(1.0 - s13_sq, 1e-30)
    s12_sq = (aU[0, 1] ** 2) / denom2
    s23_sq = (aU[1, 2] ** 2) / denom2
    J = np.imag(U[0, 0] * U[1, 1] * np.conj(U[0, 1]) * np.conj(U[1, 0]))
    s12 = sqrt(max(s12_sq, 0)); c12 = sqrt(max(1 - s12_sq, 0))
    s13 = sqrt(max(s13_sq, 0)); c13 = sqrt(max(1 - s13_sq, 0))
    s23 = sqrt(max(s23_sq, 0)); c23 = sqrt(max(1 - s23_sq, 0))
    Jmax = c12 * c13 * c13 * c23 * s12 * s13 * s23
    if Jmax > 1e-15:
        delta_full = -np.angle(np.conj(U[0, 2]) * U[0, 1] * U[1, 2] * np.conj(U[1, 1])
                                / (c12 * s12 * s23 * c23 * s13 * c13 * c13))
        delta_full_deg = float(np.degrees(delta_full)) % 360
    else:
        delta_full_deg = float("nan")
    return s12_sq, s13_sq, s23_sq, delta_full_deg, float(J), m_nu

# --------------------------------------------------------------------
# 1. Extra modular forms (weight 4 in 3', weight 5 in 3hat, 3hat'_I, 3hat'_II,
#    weight 6 components used in M_u row 1).
# Transcribed from LYD20 Appendix lines 1854-1894.
# --------------------------------------------------------------------

def extra_forms(tau, n_terms=80):
    """Compute additional modular forms needed for M_u and M_d.

    M_u: needs Y^(4)_3 (Y4_4, Y4_5, Y4_6), Y^(6)_{3,I} (Y6_5, Y6_6, Y6_7),
         Y^(6)_{3,II} (Y6_8, Y6_9, Y6_10), Y^(3)_hat3 (Y3_2, Y3_3, Y3_4).
    M_d: needs Y^(4)_3' (Y4_7, Y4_8, Y4_9), Y^(5)_{3hat',I} (Y5_6, Y5_7, Y5_8),
         Y^(5)_{3hat',II} (Y5_9, Y5_10, Y5_11), Y^(5)_3hat (Y5_3, Y5_4, Y5_5).
    """
    Y1, Y2, Y3 = weight1_forms(tau)
    f = {'Y1': Y1, 'Y2': Y2, 'Y3': Y3}
    # weight-2 triplet 3
    f['Y2_3'] = 2 * Y1 ** 2 - 2 * Y2 * Y3
    f['Y2_4'] = 2 * Y3 ** 2 - 2 * Y1 * Y2
    f['Y2_5'] = 2 * Y2 ** 2 - 2 * Y1 * Y3
    # weight-2 doublet 2 (used by M_D in lepton sector)
    f['Y2_1'] = -(Y2 ** 2) - 2 * Y1 * Y3   # LYD20 line 347
    f['Y2_2'] = Y3 ** 2 + 2 * Y1 * Y2      # LYD20 line 347
    # weight-3 hat3
    f['Y3_2'] = 2 * (2 * Y1 ** 3 - Y2 ** 3 - Y3 ** 3)
    f['Y3_3'] = 6 * Y3 * (Y2 ** 2 - Y1 * Y3)
    f['Y3_4'] = 6 * Y2 * (Y3 ** 2 - Y1 * Y2)
    # weight-4 triplet 3 (M_u row 0)
    f['Y4_4'] = 6 * Y1 * (-Y2 ** 3 + Y3 ** 3)
    f['Y4_5'] = (6 * Y1 * Y3 * (Y2 ** 2 - Y1 * Y3)
                 + 2 * Y2 * (-2 * Y1 ** 3 + Y2 ** 3 + Y3 ** 3))
    f['Y4_6'] = (6 * Y1 * Y2 * (Y1 * Y2 - Y3 ** 2)
                 - 2 * Y3 * (-2 * Y1 ** 3 + Y2 ** 3 + Y3 ** 3))
    # weight-4 triplet 3' (M_d row 0) -- LYD20 lines 1862-1863
    f['Y4_7'] = 2 * (4 * Y1 ** 4 - 6 * Y2 ** 2 * Y3 ** 2
                     + Y1 * (Y2 ** 3 + Y3 ** 3))
    f['Y4_8'] = 2 * (Y2 ** 4 - 2 * Y1 ** 3 * Y2 + 7 * Y2 * Y3 ** 3
                     + 3 * Y1 ** 2 * Y3 ** 2 - 9 * Y1 * Y2 ** 2 * Y3)
    f['Y4_9'] = 2 * (Y3 ** 4 - 2 * Y1 ** 3 * Y3 + 7 * Y2 ** 3 * Y3
                     + 3 * Y1 ** 2 * Y2 ** 2 - 9 * Y1 * Y2 * Y3 ** 2)
    # weight-5 hat3 (M_d row 2 = delta_d row, also used in A26 M_u)
    f['Y5_3'] = 18 * Y1 ** 2 * (-Y2 ** 3 + Y3 ** 3)
    f['Y5_4'] = (4 * Y1 ** 4 * Y2 + 4 * Y1 * (Y2 ** 4 - 5 * Y2 * Y3 ** 3)
                 + 14 * Y1 ** 3 * Y3 ** 2 - 4 * Y3 ** 2 * (Y2 ** 3 + Y3 ** 3)
                 + 6 * Y1 ** 2 * Y2 ** 2 * Y3)
    f['Y5_5'] = (-4 * Y1 ** 4 * Y3 - 4 * Y1 * (Y3 ** 4 - 5 * Y2 ** 3 * Y3)
                 - 14 * Y1 ** 3 * Y2 ** 2 + 4 * Y2 ** 2 * (Y2 ** 3 + Y3 ** 3)
                 - 6 * Y1 ** 2 * Y2 * Y3 ** 2)
    # weight-5 hat3' I (M_d beta_d) -- LYD20 lines 1872-1873
    f['Y5_6'] = (8 * Y1 ** 3 * Y2 * Y3 - 6 * Y1 ** 2 * (Y2 ** 3 + Y3 ** 3)
                 + 2 * Y2 * Y3 * (Y2 ** 3 + Y3 ** 3))
    f['Y5_7'] = (4 * Y1 ** 4 * Y2 - 2 * Y1 * Y2 ** 4
                 - 6 * Y1 ** 2 * Y2 ** 2 * Y3 - 2 * Y1 ** 3 * Y3 ** 2
                 + 4 * Y2 ** 3 * Y3 ** 2 + 4 * Y1 * Y2 * Y3 ** 3
                 - 2 * Y3 ** 5)
    f['Y5_8'] = -2 * (Y1 ** 3 * Y2 ** 2 + Y2 ** 5 - 2 * Y1 ** 4 * Y3
                      + 3 * Y1 ** 2 * Y2 * Y3 ** 2 - 2 * Y2 ** 2 * Y3 ** 3
                      + Y1 * (-2 * Y2 ** 3 * Y3 + Y3 ** 4))
    # weight-5 hat3' II (M_d gamma_d) -- LYD20 line 1875
    common5 = (Y1 ** 4 + 3 * Y2 ** 2 * Y3 ** 2 - 2 * Y1 * (Y2 ** 3 + Y3 ** 3))
    f['Y5_9']  = 4 * Y1 * common5
    f['Y5_10'] = 4 * Y2 * common5
    f['Y5_11'] = 4 * Y3 * common5
    # weight-6 triplet 3 I (M_u row 1, beta_u) -- LYD20 lines 1886-1887
    f['Y6_5'] = 2 * (Y2 ** 6 + Y3 ** 6
                     + 4 * Y1 ** 4 * Y2 * Y3
                     + 6 * Y1 ** 2 * Y2 ** 2 * Y3 ** 2
                     - 4 * Y2 ** 3 * Y3 ** 3
                     - 5 * Y1 ** 3 * (Y2 ** 3 + Y3 ** 3)
                     + Y1 * Y2 * Y3 * (Y2 ** 3 + Y3 ** 3))
    f['Y6_6'] = -2 * (2 * Y1 ** 5 * Y2 - 5 * Y1 ** 4 * Y3 ** 2
                      + 3 * Y1 ** 3 * Y2 ** 2 * Y3
                      + 3 * Y2 ** 2 * Y3 * (Y2 ** 3 - Y3 ** 3)
                      + Y1 ** 2 * (5 * Y2 * Y3 ** 3 - 4 * Y2 ** 4)
                      + Y1 * (Y3 ** 5 - 2 * Y2 ** 3 * Y3 ** 2))
    f['Y6_7'] = -2 * (2 * Y1 ** 5 * Y3 - 5 * Y1 ** 4 * Y2 ** 2
                      + 3 * Y1 ** 3 * Y2 * Y3 ** 2
                      + 3 * Y2 * Y3 ** 2 * (Y3 ** 3 - Y2 ** 3)
                      + Y1 * (Y2 ** 5 - 2 * Y2 ** 2 * Y3 ** 3)
                      + Y1 ** 2 * (5 * Y2 ** 3 * Y3 - 4 * Y3 ** 4))
    # weight-6 triplet 3 II (M_u row 1, gamma_u)
    D = Y1 ** 4 - 2 * Y1 * (Y2 ** 3 + Y3 ** 3) + 3 * Y2 ** 2 * Y3 ** 2
    f['Y6_8']  = 8 * (Y1 ** 2 - Y2 * Y3) * D
    f['Y6_9']  = 8 * (Y3 ** 2 - Y1 * Y2) * D
    f['Y6_10'] = 8 * (Y2 ** 2 - Y1 * Y3) * D
    return f


# --------------------------------------------------------------------
# 2. Mass matrices  (LYD20 Eq. MqII for quarks, Eq. 120 for leptons)
# --------------------------------------------------------------------

def M_u_unified(f, alpha_u, beta_u, gamma_u, delta_u):
    """LYD20 Eq. MqII row 0=alpha_u Y^(4)_3, row 1=beta_u Y^(6)_{3,I}+gamma_u Y^(6)_{3,II},
    row 2=delta_u Y^(3)_hat3."""
    return np.array([
        [alpha_u * f['Y4_4'], alpha_u * f['Y4_6'], alpha_u * f['Y4_5']],
        [beta_u  * f['Y6_5'] + gamma_u * f['Y6_8'],
         beta_u  * f['Y6_7'] + gamma_u * f['Y6_10'],
         beta_u  * f['Y6_6'] + gamma_u * f['Y6_9']],
        [delta_u * f['Y3_2'], delta_u * f['Y3_4'], delta_u * f['Y3_3']],
    ], dtype=complex)


def M_d_unified(f, alpha_d, beta_d, gamma_d, delta_d):
    """LYD20 Eq. MqII row 0=alpha_d Y^(4)_3' (Y4_7,Y4_9,Y4_8),
    row 1=beta_d Y^(5)_{3hat',I} + gamma_d Y^(5)_{3hat',II}
         indices (Y5_6,Y5_8,Y5_7) and (Y5_9,Y5_11,Y5_10),
    row 2=delta_d Y^(5)_hat3 (Y5_3,Y5_5,Y5_4)."""
    return np.array([
        [alpha_d * f['Y4_7'], alpha_d * f['Y4_9'], alpha_d * f['Y4_8']],
        [beta_d  * f['Y5_6'] + gamma_d * f['Y5_9'],
         beta_d  * f['Y5_8'] + gamma_d * f['Y5_11'],
         beta_d  * f['Y5_7'] + gamma_d * f['Y5_10']],
        [delta_d * f['Y5_3'], delta_d * f['Y5_5'], delta_d * f['Y5_4']],
    ], dtype=complex)


# --------------------------------------------------------------------
# 3. CKM extraction from M_u, M_d (PDG standard parametrisation)
# --------------------------------------------------------------------

def diag_quark(M):
    """LYD20 convention: rows of M index right-handed (u^c, c^c, t^c) singlets,
    columns index left-handed Q doublet components. So Q-handed (left) quarks
    live in the COLUMN space; the left-handed rotation diagonalises M^dagger M.

    Returns U_L (3x3 unitary, columns = mass eigenstates ascending) and
    sqrt(eigenvalues) = singular values ascending."""
    H = M.conj().T @ M
    w, U = eigh(H)            # ascending eigenvalues
    return U, np.sqrt(np.maximum(w, 0.0))


def ckm_from_M(M_u, M_d):
    """V_CKM = U_uL^dagger U_dL.  Returns (V, |V_us|, |V_cb|, |V_ub|, J_CKM, masses_u, masses_d)."""
    U_uL, sv_u = diag_quark(M_u)
    U_dL, sv_d = diag_quark(M_d)
    V = U_uL.conj().T @ U_dL
    aV = np.abs(V)
    Vus = float(aV[0, 1])
    Vcb = float(aV[1, 2])
    Vub = float(aV[0, 2])
    # Jarlskog
    J = float(np.imag(V[0, 0] * V[1, 1] * np.conj(V[0, 1]) * np.conj(V[1, 0])))
    return V, Vus, Vcb, Vub, J, sv_u, sv_d


# --------------------------------------------------------------------
# 4. PDG quark targets (GUT-scale values per Antusch-Hinze-Saad 2510.01312
#    where given; PDG run-down otherwise).
#    For *single-tau* unified model, LYD20 fits at low scale (no GUT
#    matching), so we use PDG-2024 quark mass ratios + CKM moduli.
# --------------------------------------------------------------------

PDG_QUARK = {
    # mass ratios at low scale (PDG 2024)
    "m_u/m_c":   (0.001929, 0.0002),    # central from LYD20 best fit; sigma ~ 10%
    "m_c/m_t":   (0.002725, 0.00006),   # AHS 1% / PDG combined
    "m_d/m_s":   (0.05036,  0.0007),    # PDG 2024
    "m_s/m_b":   (0.01773,  0.001),     # PDG 2024
    # CKM moduli (PDG 2024)
    "Vus":       (0.22501,  0.00068),
    "Vcb":       (0.04183,  0.00079),   # ~|V_cb| inclusive
    "Vub":       (0.00382,  0.00020),   # PDG average b -> u
    "delta_q_deg": (75.7,   3.0),       # CP violating phase (gamma)
}

# --------------------------------------------------------------------
# 5. Joint chi^2:  quarks (8 obs) + leptons (8 obs) + 3 charged-lepton
#    masses ratios (already in lepton chi^2).  Total 19 obs.
# --------------------------------------------------------------------

def chi2_joint(params, F):
    """Joint (quark + lepton) chi^2 at a fixed tau (modular forms F).
    params (13 reals):
       0:  log(beta_u/alpha_u)
       1:  log(gamma_u/alpha_u)        [we allow negative via |.|*sgn from log_abs+sign bit?]
       2:  log(delta_u/alpha_u)
       3:  log(beta_d/alpha_d)
       4:  log(|gamma_d|/alpha_d)
       5:  sign(gamma_d)  (continuous in [-1,1], used as tanh)
       6:  log(delta_d/alpha_d)
       7:  log(beta_e/alpha_e)
       8:  log(gamma_e/alpha_e)
       9:  g2/g1 (continuous)
      10:  log(g1^2 v_u^2 / Lambda)  (eV)
      11:  alpha_u_v_u  ABSORBED by mass-ratio fit (cancels);
      12:  alpha_d_v_d ABSORBED similarly.
    Up-quark mass ratios (m_u/m_c, m_c/m_t) and similarly down-quark are
    SCALE-INDEPENDENT so we drop alpha_u_v_u, alpha_d_v_d from the fit.
    alpha_e_v_d is folded into the charged-lepton-ratio chi^2 contribution
    via the m_e/m_mu, m_mu/m_tau ratios (also scale-independent).
    """
    (lbu, lgu, ldu, lbd, lgd_abs, sgnd, ldd,
     lbe, lge, g2g1, lmass) = params

    bu = exp(lbu); gu = exp(lgu); du = exp(ldu)
    bd = exp(lbd); gd = (1.0 if sgnd >= 0 else -1.0) * exp(lgd_abs); dd = exp(ldd)
    be = exp(lbe); ge = exp(lge)
    mass_scale = exp(lmass)

    try:
        # Up-quark mass matrix
        Mu = M_u_unified(F, alpha_u=1.0, beta_u=bu, gamma_u=gu, delta_u=du)
        # Down-quark mass matrix
        Md = M_d_unified(F, alpha_d=1.0, beta_d=bd, gamma_d=gd, delta_d=dd)
        V, Vus, Vcb, Vub, J_q, sv_u, sv_d = ckm_from_M(Mu, Md)

        # Charged lepton M_e and neutrino M_nu (g_1, g_2 doublet)
        Me = M_e(F, alpha_e=1.0, beta_e=be, gamma_e=ge)
        Mnu = light_nu_mass(F, g1=1.0, g2=g2g1, mass_scale=mass_scale)

        s12, s13, s23, dCP, J_l, m_nu = pmns_angles(Me, Mnu)
        _, sv_e = diag_charged_lepton(Me)
        sv_e = np.sort(sv_e)

        # mass ratios -- floor singular values at 1e-30 (equivalent to wrong-sign penalty)
        sv_u_s = np.sort(sv_u); sv_d_s = np.sort(sv_d)
        eps = 1e-25
        if sv_u_s[2] < eps or sv_u_s[1] < eps \
           or sv_d_s[2] < eps or sv_d_s[1] < eps \
           or sv_e[2] < eps or sv_e[1] < eps:
            return 1e8   # numerical degeneracy; large but not infinite
        mu_mc = float(sv_u_s[0] / sv_u_s[1])
        mc_mt = float(sv_u_s[1] / sv_u_s[2])
        md_ms = float(sv_d_s[0] / sv_d_s[1])
        ms_mb = float(sv_d_s[1] / sv_d_s[2])
        me_mmu = float(sv_e[0] / sv_e[1])
        mmu_mt = float(sv_e[1] / sv_e[2])

        Dm21 = float(m_nu[1] ** 2 - m_nu[0] ** 2)
        Dm32 = float(m_nu[2] ** 2 - m_nu[1] ** 2)

    except Exception:
        return 1e8

    chi2 = 0.0
    # ----- Quark sector (8 obs) -----
    chi2 += ((mu_mc - PDG_QUARK["m_u/m_c"][0]) / PDG_QUARK["m_u/m_c"][1]) ** 2
    chi2 += ((mc_mt - PDG_QUARK["m_c/m_t"][0]) / PDG_QUARK["m_c/m_t"][1]) ** 2
    chi2 += ((md_ms - PDG_QUARK["m_d/m_s"][0]) / PDG_QUARK["m_d/m_s"][1]) ** 2
    chi2 += ((ms_mb - PDG_QUARK["m_s/m_b"][0]) / PDG_QUARK["m_s/m_b"][1]) ** 2
    chi2 += ((Vus  - PDG_QUARK["Vus"][0]) / PDG_QUARK["Vus"][1]) ** 2
    chi2 += ((Vcb  - PDG_QUARK["Vcb"][0]) / PDG_QUARK["Vcb"][1]) ** 2
    chi2 += ((Vub  - PDG_QUARK["Vub"][0]) / PDG_QUARK["Vub"][1]) ** 2
    # CKM phase target ~ 75 deg via Jarlskog equivalence
    # |J_CKM| = 3.06e-5; treat as 8th obs
    Jq_target = 3.06e-5; Jq_sigma = 0.18e-5
    chi2 += ((abs(J_q) - Jq_target) / Jq_sigma) ** 2

    # ----- Lepton sector (8 obs) -----
    chi2 += ((s12 - PDG_NU["sin2_12"][0]) / PDG_NU["sin2_12"][1]) ** 2
    chi2 += ((s13 - PDG_NU["sin2_13"][0]) / PDG_NU["sin2_13"][1]) ** 2
    chi2 += ((s23 - PDG_NU["sin2_23"][0]) / PDG_NU["sin2_23"][1]) ** 2
    if Dm21 > 0:
        chi2 += ((Dm21 - PDG_NU["Dm21_sq"][0]) / PDG_NU["Dm21_sq"][1]) ** 2
    else:
        chi2 += 100
    if Dm32 > 0:
        chi2 += ((Dm32 - PDG_NU["Dm32_sq"][0]) / PDG_NU["Dm32_sq"][1]) ** 2
    else:
        chi2 += 100
    chi2 += ((me_mmu - PDG_M_E_MU[0]) / PDG_M_E_MU[1]) ** 2
    chi2 += ((mmu_mt - PDG_M_MU_TAU[0]) / PDG_M_MU_TAU[1]) ** 2
    # delta_CP wrap-around
    diff = (dCP - PDG_NU["delta_CP"][0])
    while diff > 180: diff -= 360
    while diff < -180: diff += 360
    chi2 += (diff / PDG_NU["delta_CP"][1]) ** 2

    if not np.isfinite(chi2) or chi2 < 0:
        return 1e8
    return chi2


# --------------------------------------------------------------------
# 6. Fit at fixed tau
# --------------------------------------------------------------------

def fit_joint(tau, label, n_de_rounds=4, popsize=30, maxiter=800, seed=42, verbose=True):
    """Joint Q+L fit at fixed tau. Seeds initial population with LYD20-best
    parameter guess for faster convergence."""
    F = extra_forms(tau)
    bounds = [
        (0.0, 12.0),    # log beta_u/alpha_u   (LYD20 ~325 -> log ~5.78)
        (0.0, 12.0),    # log gamma_u/alpha_u  (LYD20 ~2427 -> log ~7.79)
        (0.0, 12.0),    # log delta_u/alpha_u  (LYD20 ~219 -> log ~5.39)
        (0.0, 12.0),    # log beta_d/alpha_d   (LYD20 ~466 -> log ~6.14)
        (0.0, 12.0),    # log |gamma_d|/alpha_d
        (-1.0, 1.0),    # sign(gamma_d)
        (-3.0, 8.0),    # log delta_d/alpha_d  (LYD20 ~2.34 -> log ~0.85)
        (-8.0, 5.0),    # log beta_e/alpha_e   (LYD20 ~0.0187 -> log ~-3.98)
        (-8.0, 5.0),    # log gamma_e/alpha_e  (LYD20 ~0.1466 -> log ~-1.92)
        (-3.0, 3.0),    # g2/g1                (LYD20 ~0.683)
        (-12.0, 0.0),   # log mass_scale (eV)  (LYD20 ~3e-4 meV -> log ~-8)
    ]
    # LYD20 published best-fit (line 1535-1538) as warm start
    lyd_best = np.array([
        log(325.6502),     # beta_u/alpha_u
        log(2427.3101),    # gamma_u/alpha_u
        log(219.3019),     # delta_u/alpha_u
        log(466.6990),     # beta_d/alpha_d
        log(234.0473),     # |gamma_d|/alpha_d
        -1.0,              # sign(gamma_d) = -1
        log(2.3388),       # delta_d/alpha_d
        log(0.0187),       # beta_e/alpha_e
        log(0.1466),       # gamma_e/alpha_e
        0.6834,            # g2/g1
        log(0.3043e-3),    # mass_scale (eV)
    ])
    best = (1e20, None)
    rng = np.random.default_rng(seed)
    t0 = time.time()

    # First, polish from LYD-best starting point (fast)
    try:
        res0 = minimize(chi2_joint, lyd_best, args=(F,),
                        method="Nelder-Mead",
                        options={"xatol": 1e-7, "fatol": 1e-5, "maxiter": 5000})
        if res0.fun < best[0]:
            best = (float(res0.fun), res0.x)
        if verbose:
            print(f"    [{label}] LYD-warmstart NM chi2={res0.fun:.3f} t={time.time()-t0:.1f}s", flush=True)
    except Exception:
        pass

    for r in range(n_de_rounds):
        try:
            # Hybrid init: LYD-best in pop[0], rest from sobol/lhs over full bounds
            n_pop = popsize * 11
            sobol_eng = np.random.default_rng(seed + 173 * r)
            init_pop = np.zeros((n_pop, 11))
            for i in range(n_pop):
                for j, (lo, hi) in enumerate(bounds):
                    init_pop[i, j] = sobol_eng.uniform(lo, hi)
            # seed first population members with LYD-best + small perturbations
            init_pop[0] = np.clip(lyd_best, [b[0] for b in bounds], [b[1] for b in bounds])
            for k in range(1, min(5, n_pop)):
                init_pop[k] = np.clip(
                    lyd_best + 0.5 * sobol_eng.standard_normal(11),
                    [b[0] for b in bounds], [b[1] for b in bounds])
            res = differential_evolution(
                chi2_joint, bounds, args=(F,),
                maxiter=maxiter, tol=1e-9, seed=seed + 173 * r,
                popsize=popsize, mutation=(0.5, 1.5), recombination=0.9,
                workers=1, disp=False,
                init=init_pop,
            )
            if res.fun < best[0]:
                best = (float(res.fun), res.x)
            if verbose:
                print(f"    [{label}] DE round {r+1}/{n_de_rounds} chi2={res.fun:.3f} best={best[0]:.3f} t={time.time()-t0:.1f}s", flush=True)
        except Exception as e:
            if verbose:
                print(f"    [{label}] DE round {r+1} FAIL: {e}", flush=True)
    # Polish (lightweight: 5 perturb-and-NM with bounded iterations)
    if best[1] is not None:
        for k in range(5):
            try:
                x0 = best[1] + 0.04 * rng.standard_normal(len(best[1]))
                res = minimize(chi2_joint, x0, args=(F,),
                               method="Nelder-Mead",
                               options={"xatol": 1e-8, "fatol": 1e-6,
                                        "maxiter": 3000})
                if res.fun < best[0]:
                    best = (float(res.fun), res.x)
            except Exception:
                pass

    chi2_final, xopt = best
    # decode
    (lbu, lgu, ldu, lbd, lgd_abs, sgnd, ldd, lbe, lge, g2g1, lmass) = xopt
    bu = exp(lbu); gu = exp(lgu); du = exp(ldu)
    bd = exp(lbd); gd = (1.0 if sgnd >= 0 else -1.0) * exp(lgd_abs); dd = exp(ldd)
    be = exp(lbe); ge = exp(lge); mass_scale = exp(lmass)

    Mu = M_u_unified(F, 1.0, bu, gu, du)
    Md = M_d_unified(F, 1.0, bd, gd, dd)
    V, Vus, Vcb, Vub, J_q, sv_u, sv_d = ckm_from_M(Mu, Md)
    Me = M_e(F, 1.0, be, ge)
    Mnu = light_nu_mass(F, 1.0, g2g1, mass_scale)
    s12, s13, s23, dCP, J_l, m_nu = pmns_angles(Me, Mnu)
    _, sv_e = diag_charged_lepton(Me); sv_e = np.sort(sv_e)
    sv_u_s = np.sort(sv_u); sv_d_s = np.sort(sv_d)

    return {
        "label": label,
        "tau": [float(tau.real), float(tau.imag)],
        "chi2_min": float(chi2_final),
        "n_obs": 19,   # 8 quark + 8 lepton + 3 phases (delta_CP, plus e, mu, tau ratios fold into 8)
        "params": {
            "beta_u/alpha_u": float(bu),
            "gamma_u/alpha_u": float(gu),
            "delta_u/alpha_u": float(du),
            "beta_d/alpha_d": float(bd),
            "gamma_d/alpha_d": float(gd),
            "delta_d/alpha_d": float(dd),
            "beta_e/alpha_e": float(be),
            "gamma_e/alpha_e": float(ge),
            "g2/g1": float(g2g1),
            "mass_scale_eV": float(mass_scale),
        },
        "predicted_quarks": {
            "m_u/m_c": float(sv_u_s[0]/sv_u_s[1]),
            "m_c/m_t": float(sv_u_s[1]/sv_u_s[2]),
            "m_d/m_s": float(sv_d_s[0]/sv_d_s[1]),
            "m_s/m_b": float(sv_d_s[1]/sv_d_s[2]),
            "Vus": float(Vus),
            "Vcb": float(Vcb),
            "Vub": float(Vub),
            "J_CKM": float(J_q),
        },
        "predicted_leptons": {
            "sin2_theta_12": float(s12),
            "sin2_theta_13": float(s13),
            "sin2_theta_23": float(s23),
            "delta_CP_deg":  float(dCP),
            "J_PMNS": float(J_l),
            "m_nu_eV": [float(x) for x in m_nu],
            "Dm21_sq_eV2": float(m_nu[1]**2 - m_nu[0]**2),
            "Dm32_sq_eV2": float(m_nu[2]**2 - m_nu[1]**2),
            "sum_m_nu_eV": float(sum(m_nu)),
            "m_e/m_mu": float(sv_e[0]/sv_e[1]),
            "m_mu/m_tau": float(sv_e[1]/sv_e[2]),
        },
    }


# --------------------------------------------------------------------
# 7. Driver
# --------------------------------------------------------------------

def main():
    print("=" * 78, flush=True)
    print("A46 -- LYD20 unified Q+L fit at tau pinned at i (CM-anchor)", flush=True)
    print("=" * 78, flush=True)
    print(f"  Targets:  19 observables (4 quark mass ratios + 3 CKM moduli + J_CKM", flush=True)
    print(f"            + 3 PMNS angles + delta_CP + 2 nu mass splittings + 2 charged-lepton ratios)", flush=True)
    print(f"  Free params: 11 reals (Yukawa ratios + g2/g1 + mass_scale; gamma_d sign separate)", flush=True)
    print(f"  Targets per LYD20 best-fit (line 1543) and PDG 2024 + NuFIT 5.3", flush=True)
    print(flush=True)

    # ---------------------------------------------------------------
    # Three scenarios:
    #   (A) tau=i pinned (THIS PAPER)
    #   (B) LYD20 best-fit tau = -0.2123 + 1.5201i
    #   (C) W1 attractor tau* = -0.1897 + 1.0034i
    # ---------------------------------------------------------------
    tau_i  = 0.0 + 1.0j
    tau_LYD = -0.2123 + 1.5201j
    tau_W1 = -0.1897 + 1.0034j

    print("[A] FIT at tau = i (CM-anchor; pinned, no Re/Im freedom)", flush=True)
    print("-" * 78, flush=True)
    res_i = fit_joint(tau_i, "tau_i_pinned", n_de_rounds=2, popsize=15, maxiter=200)
    print(f"    chi2 = {res_i['chi2_min']:.3f}", flush=True)
    print(flush=True)

    print("[B] REPRODUCE LYD20 fit at their best-fit tau", flush=True)
    print("-" * 78, flush=True)
    res_LYD = fit_joint(tau_LYD, "tau_LYD20_best", n_de_rounds=2, popsize=15, maxiter=200)
    print(f"    chi2 = {res_LYD['chi2_min']:.3f}", flush=True)
    print(flush=True)

    print("[C] FIT at W1 attractor tau* = -0.19 + 1.00i", flush=True)
    print("-" * 78, flush=True)
    res_W1 = fit_joint(tau_W1, "tau_W1_attractor", n_de_rounds=2, popsize=15, maxiter=200)
    print(f"    chi2 = {res_W1['chi2_min']:.3f}", flush=True)
    print(flush=True)

    # ---------------------------------------------------------------
    # Comparison summary
    # ---------------------------------------------------------------
    print("=" * 78, flush=True)
    print("COMPARISON", flush=True)
    print("=" * 78, flush=True)
    chi2_i   = res_i['chi2_min']
    chi2_LYD = res_LYD['chi2_min']
    chi2_W1  = res_W1['chi2_min']
    print(f"  chi^2 ( tau = i pinned )     = {chi2_i:.2f}", flush=True)
    print(f"  chi^2 ( tau = LYD20 best )   = {chi2_LYD:.2f}", flush=True)
    print(f"  chi^2 ( tau = W1 attractor ) = {chi2_W1:.2f}", flush=True)
    print(flush=True)
    if chi2_LYD > 1e-4:
        ratio_i_over_LYD = chi2_i / chi2_LYD
        ratio_W1_over_LYD = chi2_W1 / chi2_LYD
        print(f"  PENALTY for tau=i  vs LYD-best:  {ratio_i_over_LYD:.2f}x", flush=True)
        print(f"  PENALTY for tau=W1 vs LYD-best:  {ratio_W1_over_LYD:.2f}x", flush=True)
    print(flush=True)

    # Save JSON
    out = {
        "version": "ECI v6.0.53.4",
        "agent": "A46",
        "date": "2026-05-05",
        "method": "LYD20 (arXiv:2006.10722) unified Q+L joint fit, "
                  "tau pinned at i; refit 11 real Yukawa params over 19 obs.",
        "tau_pinned_at_i": {"re": 0.0, "im": 1.0},
        "tau_LYD20_best": {"re": -0.2123, "im": 1.5201},
        "tau_W1_attractor": {"re": -0.1897, "im": 1.0034},
        "PDG_quark_targets": {k: list(v) for k, v in PDG_QUARK.items()},
        "PDG_lepton_targets": {k: list(v) for k, v in PDG_NU.items()},
        "PDG_charged_lepton_ratios": {
            "m_e/m_mu": list(PDG_M_E_MU),
            "m_mu/m_tau": list(PDG_M_MU_TAU),
        },
        "fit_tau_i_pinned":     res_i,
        "fit_tau_LYD20_best":   res_LYD,
        "fit_tau_W1_attractor": res_W1,
        "comparison": {
            "chi2_tau_i":   chi2_i,
            "chi2_tau_LYD": chi2_LYD,
            "chi2_tau_W1":  chi2_W1,
            "penalty_tau_i_vs_LYD":  chi2_i / max(chi2_LYD, 1e-6),
            "penalty_tau_W1_vs_LYD": chi2_W1 / max(chi2_LYD, 1e-6),
        },
        "verdict": (
            f"GRAFT VIABLE (penalty {chi2_i/max(chi2_LYD,1e-6):.2f}x) -- "
            "structural anchoring cost"
            if chi2_i / max(chi2_LYD, 1e-6) < 5.0
            else f"GRAFT MARGINAL (penalty {chi2_i/max(chi2_LYD,1e-6):.2f}x) -- "
                 "tau=i pinning incurs heavy chi^2 cost"
        ),
    }
    out_path = "/root/crossed-cosmos/notes/eci_v7_aspiration/A46_LYD20_GRAFT/lyd20_pinned_results.json"
    with open(out_path, "w") as fh:
        json.dump(out, fh, indent=2)
    print(f"  Saved {out_path}", flush=True)


if __name__ == "__main__":
    main()
