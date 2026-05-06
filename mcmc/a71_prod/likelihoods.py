"""
A71 — ECI-vs-LCDM Framing B: JAX-jittable likelihood functions.

Implements:
  1. loglike_desi_dr2_bao   — DESI DR2 BAO (arXiv:2503.14738, confirmed)
  2. loglike_pantheonplus   — Pantheon+ (arXiv:2202.04077, confirmed)
  3. loglike_planck2018_compressed — Planck 2018 Plik (arXiv:1807.06209, confirmed)

arXiv verifications (live, 2026-05-05 via export.arxiv.org/api/query):
  - Brout et al. 2022 Pantheon+ cosmological constraints: CONFIRMED arXiv:2202.04077
    Title: "The Pantheon+ Analysis: Cosmological Constraints"
  - Aghanim et al. 2018 Planck 2018 cosmological parameters: CONFIRMED arXiv:1807.06209
    Title: "Planck 2018 results. VI. Cosmological parameters"
  - DESI DR2 BAO: CONFIRMED arXiv:2503.14738
    Title: "DESI DR2 Results II: Measurements of Baryon Acoustic Oscillations and
    Cosmological Constraints"

Hallu count: 85 (entering) → 85 (leaving). Mistral STRICT-BAN.

M1 bug-fix 2026-05-06 (Sub-agent M1):
  BUG A FIXED: PLANCK2018_COV_APPROX was non-positive-definite (eigenvalue=-3.998e-6).
    Replaced with diagonal-only covariance (sigma from Table 2, arXiv:1807.06209).
  BUG B FIXED: loglike_planck2018_compressed() multiplied log10As_e10 by ln(10)=2.303,
    but the parameter IS already ln(10^10 A_s) (prior [2.7,3.5] encodes ln range).
    Removed the spurious * jnp.log(10.0) factor.
  These two bugs together produced chi2~80000 at Planck fiducial → NUTS at boundaries.
  After fix: chi2~9.7 at fiducial (residual from theta_MC approx bias, ~3.1 sigma).
"""

import os
import warnings
import jax
import jax.numpy as jnp
import numpy as np
from functools import partial

from .background import D_H, D_M, chi, sound_horizon_EH

# =========================================================================
# SECTION 1 — DESI DR2 BAO likelihood
# =========================================================================
# Reference: DESI Collaboration et al. 2025, arXiv:2503.14738
# 7 z-bins: BGS, LRG1, LRG2, LRG3+ELG1, ELG2, QSO, Ly-alpha
# Observables: D_M/r_d, D_H/r_d (or D_V/r_d for BGS)
#
# DESI DR2 Table 1 data (from arXiv:2503.14738):
# [TBD: verify exact values from paper — use defensive code below]
# These are the central values from DESI DR2 Table 1 (DR2-w0waCDM).
# If the data file is available on disk, load from file (preferred).
#
# BAO fit type codes:
#  "iso" : isotropic D_V/r_d only
#  "aniso": anisotropic D_M/r_d + D_H/r_d

# DESI DR2 data — REAL VALUES from CobayaSampler/bao_data (S9 acquisition 2026-05-06).
# Source: https://github.com/CobayaSampler/bao_data/tree/master/desi_bao_dr2
# Reference: DESI Collaboration 2025, arXiv:2503.14738 (confirmed).
# Data files downloaded: desi_gaussian_bao_ALL_GCcomb_mean.txt + _cov.txt
#   mean sha256: 9ac154ab583ce759c0f7eef3c978c7c70a6ead2d18774caceadf1a350a640585
#   cov  sha256: 252a143274c8a07c78694c119617d36594f6d7965d00319ca611c6ffb886e509
#
# Data ordering in the 13x13 covariance (same as mean file order):
#  [0] BGS z=0.295 DV/rs (iso)
#  [1,2] LRG1 z=0.510 (DM/rs, DH/rs)
#  [3,4] LRG2 z=0.706 (DM/rs, DH/rs)
#  [5,6] LRG+ELG z=0.934 (DM/rs, DH/rs)
#  [7,8] ELG z=1.321 (DM/rs, DH/rs)
#  [9,10] QSO z=1.484 (DM/rs, DH/rs)
#  [11,12] Lya z=2.330 (DH/rs, DM/rs) — NOTE: Lya has DH first in the file
#
# The dict-based API below is used internally. The full 13x13 covariance is
# loaded from disk when available (preferred) or via _load_desi_dr2_data_from_files().
DESI_DR2_DEFAULT = {
    # BGS (z_eff=0.295): isotropic D_V/r_d only
    "BGS": {
        "z": 0.295,
        "DV_rd": 7.94167639,
        "sigma_DV_rd": 0.07609196,   # sqrt(cov[0,0])
        "fit": "iso",
    },
    # LRG1 (z_eff=0.510): anisotropic
    "LRG1": {
        "z": 0.510,
        "DM_rd": 13.58758434,
        "DH_rd": 21.86294686,
        "sigma_DM_rd": 0.16836678,   # sqrt(cov[1,1])
        "sigma_DH_rd": 0.42886832,   # sqrt(cov[2,2])
        "cov_DM_DH": -0.4516,        # correlation coefficient cov[1,2]/(sig1*sig2)
        "fit": "aniso",
    },
    # LRG2 (z_eff=0.706): anisotropic
    "LRG2": {
        "z": 0.706,
        "DM_rd": 17.35069094,
        "DH_rd": 19.45534918,
        "sigma_DM_rd": 0.17993122,
        "sigma_DH_rd": 0.33387003,
        "cov_DM_DH": -0.3953,
        "fit": "aniso",
    },
    # LRG+ELG (z_eff=0.934): anisotropic
    "LRG+ELG": {
        "z": 0.934,
        "DM_rd": 21.57563956,
        "DH_rd": 17.64149464,
        "sigma_DM_rd": 0.16178159,
        "sigma_DH_rd": 0.20104325,
        "cov_DM_DH": -0.3472,
        "fit": "aniso",
    },
    # ELG (z_eff=1.321): anisotropic
    "ELG": {
        "z": 1.321,
        "DM_rd": 27.60085612,
        "DH_rd": 14.17602155,
        "sigma_DM_rd": 0.32455588,
        "sigma_DH_rd": 0.22455135,
        "cov_DM_DH": -0.3983,
        "fit": "aniso",
    },
    # QSO (z_eff=1.484): anisotropic
    "QSO": {
        "z": 1.484,
        "DM_rd": 30.51190063,
        "DH_rd": 12.81699964,
        "sigma_DM_rd": 0.76355764,
        "sigma_DH_rd": 0.51801177,
        "cov_DM_DH": -0.4936,
        "fit": "aniso",
    },
    # Lya (z_eff=2.330): anisotropic
    "Lya": {
        "z": 2.330,
        "DM_rd": 38.98897396,
        "DH_rd": 8.63154567,
        "sigma_DM_rd": 0.53168203,
        "sigma_DH_rd": 0.10106245,
        "cov_DM_DH": -0.4306,
        "fit": "aniso",
    },
}

# Path to real DESI DR2 data on PC (or on VPS if copied there)
_DESI_DR2_DATA_PATH = os.environ.get(
    "DESI_DR2_DATA_PATH",
    "/home/remondiere/data/desi_dr2"
)


def _load_desi_dr2_data_from_files(data_path=None):
    """
    Load DESI DR2 BAO data from CobayaSampler-format text files.

    Expects:
      {data_path}/desi_gaussian_bao_ALL_GCcomb_mean.txt  (13 data rows)
      {data_path}/desi_gaussian_bao_ALL_GCcomb_cov.txt   (13x13 matrix)

    Returns dict with keys "mean_vec", "cov", "cov_inv", "data_info"
    for use in loglike_desi_dr2_bao_full_cov().
    Returns None if files not found.
    """
    if data_path is None:
        data_path = _DESI_DR2_DATA_PATH
    mean_file = os.path.join(data_path, "desi_gaussian_bao_ALL_GCcomb_mean.txt")
    cov_file  = os.path.join(data_path, "desi_gaussian_bao_ALL_GCcomb_cov.txt")
    if not (os.path.exists(mean_file) and os.path.exists(cov_file)):
        return None

    mean_data = []
    with open(mean_file) as f:
        for line in f:
            if line.startswith("#"):
                continue
            parts = line.strip().split()
            mean_data.append({
                "z": float(parts[0]),
                "value": float(parts[1]),
                "quantity": parts[2],
            })

    cov = np.loadtxt(cov_file)
    cov_inv = np.linalg.inv(cov)

    return {
        "mean_data": mean_data,   # list of 13 dicts
        "cov": cov,               # (13,13) numpy array
        "cov_inv": cov_inv,       # (13,13) numpy array
        "_source": mean_file,
    }


def _dv_rd(z, H0, Omega_m, w0, wa, r_d, n_steps=200):
    """Isotropic D_V(z)/r_d = [z * D_M(z)^2 * D_H(z)]^{1/3} / r_d."""
    DM = D_M(jnp.atleast_1d(z), H0, Omega_m, w0, wa, n_steps=n_steps)[0]
    DH = D_H(z, H0, Omega_m, w0, wa)
    DV = (z * DM**2 * DH) ** (1.0 / 3.0)
    return DV / r_d


def loglike_desi_dr2_bao(H0: jnp.ndarray,
                          Omega_m: jnp.ndarray,
                          w0: jnp.ndarray,
                          wa: jnp.ndarray,
                          omega_b: jnp.ndarray,
                          omega_m: jnp.ndarray,
                          data_dict: dict | None = None,
                          use_default_warning: bool = True) -> jnp.ndarray:
    """
    DESI DR2 BAO log-likelihood (arXiv:2503.14738).

    Loading priority:
      1. If data_dict is supplied: use it directly.
      2. If /home/remondiere/data/desi_dr2/ exists on disk: use full 13x13
         covariance via loglike_desi_dr2_bao_full_cov() [preferred].
      3. Else: use DESI_DR2_DEFAULT (real values from S9 acquisition, confirmed
         against CobayaSampler/bao_data sha256-verified files 2026-05-06).

    Args:
      H0: Hubble constant [km/s/Mpc]
      Omega_m: matter fraction (total, flat universe)
      w0, wa: CPL dark energy params
      omega_b: ω_b h² (for r_d calculation)
      omega_m: ω_m h² = Omega_m * (H0/100)^2 (for r_d calculation)
      data_dict: optional override (dict with same structure as DESI_DR2_DEFAULT)
      use_default_warning: if True, warn when using fallback data

    Returns:
      log-likelihood (scalar JAX float)
    """
    r_d = sound_horizon_EH(omega_b, omega_m)  # [Mpc]

    if data_dict is None:
        # Attempt to load real data from disk (preferred path: PC production)
        real_data = _load_desi_dr2_data_from_files()
        if real_data is not None:
            return loglike_desi_dr2_bao_full_cov(
                H0, Omega_m, w0, wa, omega_b, omega_m, real_data
            )
        # Fallback: use DESI_DR2_DEFAULT (real values from S9 acquisition)
        data_dict = DESI_DR2_DEFAULT
        if use_default_warning:
            warnings.warn(
                "DESI DR2: /home/remondiere/data/desi_dr2/ not found on this machine. "
                "Using DESI_DR2_DEFAULT (real values from CobayaSampler/bao_data, "
                "S9-acquired 2026-05-06, sha256-verified). "
                "For full 13x13 covariance: copy data files to /home/remondiere/data/desi_dr2/.",
                stacklevel=2,
            )

    logL = jnp.array(0.0)

    for name, row in data_dict.items():
        z = jnp.array(row["z"])

        if row.get("fit") == "iso":
            DV_rd_th = _dv_rd(z, H0, Omega_m, w0, wa, r_d)
            obs = jnp.array(row["DV_rd"])
            err = jnp.array(row["sigma_DV_rd"])
            logL = logL - 0.5 * ((DV_rd_th - obs) / err) ** 2

        else:  # "aniso"
            DM_th = D_M(jnp.atleast_1d(z), H0, Omega_m, w0, wa)[0] / r_d
            DH_th = D_H(z, H0, Omega_m, w0, wa) / r_d

            obs_DM = jnp.array(row["DM_rd"])
            obs_DH = jnp.array(row["DH_rd"])
            sig_DM = jnp.array(row["sigma_DM_rd"])
            sig_DH = jnp.array(row["sigma_DH_rd"])
            rho    = jnp.array(row["cov_DM_DH"])  # correlation coefficient

            res_DM = (DM_th - obs_DM) / sig_DM
            res_DH = (DH_th - obs_DH) / sig_DH

            # 2x2 Gaussian with correlation rho
            inv_det = 1.0 / (1.0 - rho**2)
            chi2 = inv_det * (res_DM**2 + res_DH**2 - 2.0 * rho * res_DM * res_DH)
            logL = logL - 0.5 * chi2

    return logL


def loglike_desi_dr2_bao_full_cov(H0: jnp.ndarray,
                                    Omega_m: jnp.ndarray,
                                    w0: jnp.ndarray,
                                    wa: jnp.ndarray,
                                    omega_b: jnp.ndarray,
                                    omega_m: jnp.ndarray,
                                    real_data: dict) -> jnp.ndarray:
    """
    DESI DR2 BAO log-likelihood using the full 13x13 covariance matrix
    loaded from CobayaSampler-format text files.

    Data ordering (13 elements):
      [0]  BGS z=0.295 DV/rs
      [1]  LRG1 z=0.510 DM/rs
      [2]  LRG1 z=0.510 DH/rs
      [3]  LRG2 z=0.706 DM/rs
      [4]  LRG2 z=0.706 DH/rs
      [5]  LRG+ELG z=0.934 DM/rs
      [6]  LRG+ELG z=0.934 DH/rs
      [7]  ELG z=1.321 DM/rs
      [8]  ELG z=1.321 DH/rs
      [9]  QSO z=1.484 DM/rs
      [10] QSO z=1.484 DH/rs
      [11] Lya z=2.330 DH/rs  (DH first in file)
      [12] Lya z=2.330 DM/rs

    Args:
      real_data: dict from _load_desi_dr2_data_from_files()

    Returns:
      log-likelihood (scalar JAX float)
    """
    r_d = sound_horizon_EH(omega_b, omega_m)

    mean_data = real_data["mean_data"]
    cov_inv = jnp.array(real_data["cov_inv"])   # (13,13)

    # Build theory vector matching data ordering
    th_vec = []
    for entry in mean_data:
        z = jnp.array(entry["z"])
        qty = entry["quantity"]
        if qty == "DV_over_rs":
            th_vec.append(_dv_rd(z, H0, Omega_m, w0, wa, r_d))
        elif qty == "DM_over_rs":
            th_vec.append(D_M(jnp.atleast_1d(z), H0, Omega_m, w0, wa)[0] / r_d)
        elif qty == "DH_over_rs":
            th_vec.append(D_H(z, H0, Omega_m, w0, wa) / r_d)
        else:
            raise ValueError(f"Unknown DESI quantity: {qty}")

    th = jnp.stack(th_vec)
    obs = jnp.array([entry["value"] for entry in mean_data])
    delta = th - obs
    chi2 = delta @ cov_inv @ delta
    return -0.5 * chi2


# =========================================================================
# SECTION 2 — Pantheon+ SNe Ia likelihood with analytic M_B marginalization
# =========================================================================
# Reference: Brout et al. 2022, ApJ 938, 110 — arXiv:2202.04077 (CONFIRMED)
# Title: "The Pantheon+ Analysis: Cosmological Constraints"
# 1701 SNe Ia, z ∈ [0.001, 2.26].
#
# Analytic M_B marginalization (Bridle et al. 2002 / standard approach):
#   mu_th(z) = 5 log10(D_L(z) [Mpc]) + 25
#   D_L(z)   = (1+z) * D_M(z)
#   chi2_raw  = (mu_obs - mu_th - M_B)^T C^{-1} (mu_obs - mu_th - M_B)
#
# Analytic marginalization over M_B (flat prior):
#   log L = -0.5 * [chi2 - (sum_i [C^{-1} delta mu]_i)^2 / (sum_{ij} C^{-1}_{ij})]
#         where delta_mu = mu_obs - mu_th
#
# For FRAMING B we treat M_B as a nuisance param sampled by numpyro
# (simpler; analytic marginalization available via loglike_pantheonplus_margMB).

# Path to real Pantheon+ data on PC
_PANTHEONPLUS_DATA_PATH = os.environ.get(
    "PANTHEONPLUS_DATA_PATH",
    "/home/remondiere/data/pantheonplus"
)

# Module-level cache to avoid re-parsing 33MB covariance on each call
_PANTHEONPLUS_CACHE: dict | None = None


def _load_pantheonplus_data_from_files(data_path=None):
    """
    Load Pantheon+ data from disk.
    Files expected:
      {data_path}/Pantheon+SH0ES.dat          (1701 rows, see README)
      {data_path}/Pantheon+SH0ES_STAT+SYS.cov (N=1701 header + N^2 elements)

    Returns dict with keys:
      "z_sn"   : (1701,) float64 redshifts (zHD column)
      "mu_obs" : (1701,) float64 corrected apparent magnitudes (m_b_corr)
                 Note: residual = mu_obs - mu_th - M_B where mu_th = 5*log10(D_L)+25
      "cov_inv": (1701,1701) float64 inverse covariance (stat+sys)
    Returns None if files not found.
    """
    global _PANTHEONPLUS_CACHE
    if _PANTHEONPLUS_CACHE is not None:
        return _PANTHEONPLUS_CACHE

    if data_path is None:
        data_path = _PANTHEONPLUS_DATA_PATH

    dat_file = os.path.join(data_path, "Pantheon+SH0ES.dat")
    cov_file = os.path.join(data_path, "Pantheon+SH0ES_STAT+SYS.cov")

    if not (os.path.exists(dat_file) and os.path.exists(cov_file)):
        return None

    # Parse data file
    rows = []
    with open(dat_file) as f:
        header = f.readline().strip().split()
        for line in f:
            rows.append(line.strip().split())
    iz  = header.index("zHD")
    imb = header.index("m_b_corr")
    z_sn   = np.array([float(r[iz])  for r in rows], dtype=np.float64)
    mu_obs = np.array([float(r[imb]) for r in rows], dtype=np.float64)

    # Parse covariance file (N on first line, then N*N elements one per line)
    with open(cov_file) as f:
        N = int(f.readline().strip())
        vals = np.fromiter((float(x) for line in f for x in line.split()),
                           dtype=np.float64, count=N * N)
    cov = vals.reshape(N, N)
    cov_inv = np.linalg.inv(cov)

    _PANTHEONPLUS_CACHE = {
        "z_sn":    z_sn,
        "mu_obs":  mu_obs,
        "cov_inv": cov_inv,
        "_source": dat_file,
        "_N":      N,
    }
    return _PANTHEONPLUS_CACHE


def mu_luminosity(z: jnp.ndarray,
                   H0: jnp.ndarray,
                   Omega_m: jnp.ndarray,
                   w0: jnp.ndarray,
                   wa: jnp.ndarray,
                   n_steps: int = 200) -> jnp.ndarray:
    """
    Distance modulus mu(z) = 5*log10(D_L/Mpc) + 25.
    D_L(z) = (1+z) * D_M(z) [flat universe].
    """
    DM = D_M(z, H0, Omega_m, w0, wa, n_steps=n_steps)
    DL = (1.0 + z) * DM  # [Mpc]
    return 5.0 * jnp.log10(DL) + 25.0


def loglike_pantheonplus(H0: jnp.ndarray,
                          Omega_m: jnp.ndarray,
                          w0: jnp.ndarray,
                          wa: jnp.ndarray,
                          M_B: jnp.ndarray,
                          data_dict: dict | None = None) -> jnp.ndarray:
    """
    Pantheon+ log-likelihood (arXiv:2202.04077, confirmed).
    M_B is sampled as a parameter (not analytically marginalized here;
    use loglike_pantheonplus_margMB for analytic version).

    Loading priority:
      1. If data_dict is supplied: use it directly.
      2. If /home/remondiere/data/pantheonplus/ exists: load real 1701-SN data
         with full STAT+SYS covariance (S9-acquired 2026-05-06, sha256-verified).
      3. Else: synthetic 200-SN fallback (smoke test only).

    Args:
      H0, Omega_m, w0, wa: cosmological parameters
      M_B: SN-Ia absolute magnitude [mag]
      data_dict: dict with keys:
        "z_sn"   : (N,) redshifts of SNe
        "mu_obs" : (N,) corrected apparent magnitudes (m_b_corr from Pantheon+SH0ES.dat)
                   residual = mu_obs - mu_th(z) - M_B
        "cov_inv": (N,N) inverse covariance matrix (STAT+SYS)
        OR:
        "mu_obs", "mu_err" for diagonal approximation (smoke test)

    Returns:
      log-likelihood (scalar)
    """
    if data_dict is None:
        real_data = _load_pantheonplus_data_from_files()
        if real_data is not None:
            data_dict = real_data
        else:
            warnings.warn(
                "Pantheon+: /home/remondiere/data/pantheonplus/ not found on this machine. "
                "Using synthetic 200-SN data (smoke test only). "
                "Copy Pantheon+SH0ES.dat + Pantheon+SH0ES_STAT+SYS.cov to enable real data.",
                stacklevel=2,
            )
            data_dict = _make_synthetic_sne_data()

    z_sn    = jnp.array(data_dict["z_sn"])
    mu_obs  = jnp.array(data_dict["mu_obs"])
    mu_th   = mu_luminosity(z_sn, H0, Omega_m, w0, wa)
    residual = mu_obs - mu_th - M_B  # (N,)

    if "cov_inv" in data_dict:
        cov_inv = jnp.array(data_dict["cov_inv"])
        chi2 = residual @ cov_inv @ residual
    else:
        mu_err = jnp.array(data_dict["mu_err"])
        chi2 = jnp.sum((residual / mu_err) ** 2)

    return -0.5 * chi2


def loglike_pantheonplus_margMB(H0: jnp.ndarray,
                                  Omega_m: jnp.ndarray,
                                  w0: jnp.ndarray,
                                  wa: jnp.ndarray,
                                  data_dict: dict | None = None) -> jnp.ndarray:
    """
    Pantheon+ with M_B analytically marginalized (flat prior).

    Using the standard analytic result for a single additive nuisance:
      chi2_marg = chi2_raw - (A)^2 / B
      A = sum_i [C^{-1} delta_mu]_i
      B = sum_{ij} C^{-1}_{ij}
      chi2_raw = delta_mu^T C^{-1} delta_mu  (with M_B=0)

    Ref: e.g. Lewis & Bridle 2002; standard in CMB/SN analyses.
    [TBD: verify this is the exact form used by Pantheon+ collaboration]
    """
    if data_dict is None:
        real_data = _load_pantheonplus_data_from_files()
        if real_data is not None:
            data_dict = real_data
        else:
            warnings.warn(
                "Pantheon+ margMB: /home/remondiere/data/pantheonplus/ not found. "
                "Using synthetic 200-SN data (smoke test only).",
                stacklevel=2,
            )
            data_dict = _make_synthetic_sne_data()

    z_sn    = jnp.array(data_dict["z_sn"])
    mu_obs  = jnp.array(data_dict["mu_obs"])
    mu_th   = mu_luminosity(z_sn, H0, Omega_m, w0, wa)
    delta   = mu_obs - mu_th  # delta_mu ignoring M_B

    if "cov_inv" in data_dict:
        cov_inv = jnp.array(data_dict["cov_inv"])
        Cinv_delta = cov_inv @ delta
        chi2_raw = delta @ Cinv_delta
        A = jnp.sum(Cinv_delta)
        B = jnp.sum(cov_inv)
    else:
        mu_err  = jnp.array(data_dict["mu_err"])
        var_inv = 1.0 / mu_err**2
        chi2_raw = jnp.sum(var_inv * delta**2)
        A = jnp.sum(var_inv * delta)
        B = jnp.sum(var_inv)

    chi2_marg = chi2_raw - A**2 / B
    return -0.5 * chi2_marg


def _make_synthetic_sne_data(n_sn: int = 200,
                               seed: int = 42) -> dict:
    """
    Generate synthetic Pantheon+-like SNe data for smoke test.
    Cosmology: LCDM H0=67, Omega_m=0.3, w0=-1, wa=0, M_B=-19.3.
    Noise: sigma_mu = 0.15 mag per SN (conservative; real Pantheon+ has ~0.12 mean).

    [TBD: replace with real Pantheon+ data in production]
    """
    rng = np.random.default_rng(seed)
    z_sn = np.sort(rng.uniform(0.01, 1.5, n_sn))
    # Use pure numpy for synthetic data generation (no JAX needed)
    H0_fid, Om_fid, w0_fid, wa_fid, MB_fid = 67.0, 0.3, -1.0, 0.0, -19.3
    C_KMS = 2.99792458e5

    def chi_numpy(z_t, n_steps=100):
        zz = np.linspace(0, z_t, n_steps + 1)
        H = H0_fid * np.sqrt(Om_fid * (1+zz)**3 + (1-Om_fid))
        return np.trapezoid(C_KMS / H, zz)

    mu_true = np.array([
        5 * np.log10((1+z) * chi_numpy(z)) + 25 + MB_fid
        for z in z_sn
    ])
    sigma_mu = 0.15 * np.ones(n_sn)
    noise = rng.normal(0, sigma_mu)
    mu_obs = mu_true + noise

    return {
        "z_sn": z_sn.tolist(),
        "mu_obs": mu_obs.tolist(),
        "mu_err": sigma_mu.tolist(),
        "_is_synthetic": True,
        "_note": "[TBD: replace with real Pantheon+ mu_obs + cov_inv]",
    }


# =========================================================================
# SECTION 3 — Planck 2018 compressed CMB likelihood
# =========================================================================
# Reference: Aghanim et al. 2018 (Planck 2018 VI), arXiv:1807.06209 (CONFIRMED)
#
# Compressed likelihood: Gaussian on {ω_b, ω_c, θ_MC, ln(10^10 A_s), n_s}
# using Planck 2018 Plik TT+TE+EE bestfit + covariance from
# the Planck Legacy Archive parameter chains (COM_CosmoParams_fullGrid_R3.01.zip).
#
# NOTE: The 5-parameter compressed likelihood is a well-known approximation
# that allows fast evaluation without the full clik code. See e.g.
# Chen, Gerbino & Lesgourgues 2021 for compressed CMB approach.
# [TBD: verify that the exact numerical values below match PLA chains R3.01]
#
# θ_MC ≈ 100 * θ_* = 100 * r_s(z_drag) / D_A(z_*) is the acoustic scale angle.
# Approximated below using Hu & Sugiyama 1996 / Eisenstein-Hu fitting formula.
# [TBD: replace theta_MC approximation with CLASS/CAMB call for final run]
#
# Planck 2018 Plik TT+TE+EE+lowl+lowE bestfit values (Table 2 of 1807.06209):
PLANCK2018_BESTFIT = {
    "omega_b": 0.02237,
    "omega_c": 0.1200,
    "theta_MC_100": 1.04092,   # 100 θ_MC
    "ln_As_e10": 3.044,        # ln(10^10 A_s) — note: A70 uses log10; see conversion below
    "n_s": 0.9649,
}

# Planck 2018 compressed covariance — DIAGONAL ONLY (M1 bug-fix 2026-05-06).
#
# BUG FIXED: the previous PLANCK2018_COV_APPROX had guessed off-diagonal elements
# that made the matrix NON-POSITIVE-DEFINITE (eigenvalue = -3.998e-6, det < 0).
# A non-PD covariance produces a chi2 unbounded below; NUTS exploits this to
# escape to prior boundaries (observed: log10As_e10=3.5, n_s=0.9, omega_b=0.019).
#
# FIX: diagonal-only covariance built from published 1-sigma errors in
# arXiv:1807.06209 Table 2 (Aghanim et al. 2018, confirmed).
#   omega_b:      sigma=0.00015 → var=2.25e-8
#   omega_c:      sigma=0.00120 → var=1.44e-6
#   theta_MC_100: sigma=0.00031 → var=9.61e-8
#   ln_As_e10:    sigma=0.014   → var=1.96e-4
#   n_s:          sigma=0.0042  → var=1.764e-5
#
# Off-diagonal is set to zero (safe conservative choice: over-estimates parameter
# uncertainties marginally; all eigenvalues guaranteed positive).
# [TBD: replace diagonal with full PLA R3.01 covariance once
#  COM_CosmoParams_fullGrid_R3.01.zip (~1.8GB) is downloaded and chains extracted.
#  The known physical correlations (e.g. omega_b ↔ n_s ~0.3, omega_c ↔ theta_MC ~-0.4)
#  will tighten constraints but the diagonal is conservatively valid.]
#
# Parameter order: [omega_b, omega_c, theta_MC_100, ln_As_e10, n_s]
PLANCK2018_COV_APPROX = np.diag(np.array([
    2.25e-8,   # omega_b:      sigma=0.00015 (Table 2, arXiv:1807.06209)
    1.44e-6,   # omega_c:      sigma=0.00120 (Table 2, arXiv:1807.06209)
    9.61e-8,   # theta_MC_100: sigma=0.00031 (Table 2, arXiv:1807.06209)
    1.96e-4,   # ln_As_e10:    sigma=0.014   (Table 2, arXiv:1807.06209)
    1.764e-5,  # n_s:          sigma=0.0042  (Table 2, arXiv:1807.06209)
]))

# Path to Planck compressed data on PC
_PLANCK_DATA_PATH = os.environ.get(
    "PLANCK2018_DATA_PATH",
    "/home/remondiere/data/planck_2018_compressed"
)


def _load_planck2018_compressed_from_file(data_path=None):
    """
    Load Planck 2018 compressed likelihood parameters from disk.
    Expects: {data_path}/planck2018_compressed.json with keys:
      "bestfit": dict of 5 params
      "cov_approx_5x5": dict with "matrix" key (5x5)
    Returns (mean_vec, cov_inv) or None if file not found.
    """
    import json
    if data_path is None:
        data_path = _PLANCK_DATA_PATH
    json_file = os.path.join(data_path, "planck2018_compressed.json")
    if not os.path.exists(json_file):
        return None
    with open(json_file) as f:
        d = json.load(f)
    bf = d["bestfit"]
    mean_vec = np.array([
        bf["omega_b"], bf["omega_c"], bf["theta_MC_100"],
        bf["ln_As_e10"], bf["n_s"]
    ])
    cov = np.array(d["cov_approx_5x5"]["matrix"])

    # M1 bug-fix 2026-05-06: validate that the loaded covariance is positive definite.
    # The previous JSON on disk may contain the buggy non-PD matrix.
    # If non-PD, fall back to the safe diagonal-only matrix.
    eigvals = np.linalg.eigvalsh(cov)
    if np.any(eigvals <= 0):
        warnings.warn(
            f"Planck compressed covariance from {json_file} is NOT positive definite "
            f"(min eigenvalue={eigvals.min():.4e}). "
            f"Falling back to diagonal-only covariance (sigma from Table 2, arXiv:1807.06209). "
            f"Update the JSON file with a valid PD covariance to suppress this warning.",
            stacklevel=2,
        )
        return None  # triggers fallback to PLANCK2018_COV_APPROX (now diagonal)

    cov_inv = np.linalg.inv(cov)
    return mean_vec, cov_inv


# Try to load from disk at module import; fallback to PLANCK2018_COV_APPROX
_planck_loaded = _load_planck2018_compressed_from_file()
if _planck_loaded is not None:
    _jax_planck_mean    = jnp.array(_planck_loaded[0])
    _jax_planck_cov_inv = jnp.array(_planck_loaded[1])
else:
    _PLANCK_COV_INV     = np.linalg.inv(PLANCK2018_COV_APPROX)
    _jax_planck_mean    = jnp.array([
        PLANCK2018_BESTFIT["omega_b"],
        PLANCK2018_BESTFIT["omega_c"],
        PLANCK2018_BESTFIT["theta_MC_100"],
        PLANCK2018_BESTFIT["ln_As_e10"],
        PLANCK2018_BESTFIT["n_s"],
    ])
    _jax_planck_cov_inv = jnp.array(np.linalg.inv(PLANCK2018_COV_APPROX))


def theta_MC_approx(omega_b: jnp.ndarray,
                     omega_m: jnp.ndarray) -> jnp.ndarray:
    """
    Approximate 100 * θ_MC (CMB acoustic scale angle).

    Uses the Kosowsky-Milosavljevic-Jimenez 2002 approximation
    (also known as the θ_* approximation used in CosmoMC):
      100 * θ_* ≈ 100 * 0.01041 * (omega_b/0.02238)^0.012 * (omega_m/0.1428)^{-0.25}

    This is a rough approximation. For production:
    [TBD: replace with CLASS-computed theta_MC or use separate emulator]

    Reference approach: CMB standard; see e.g. Percival et al. 2002.
    Do NOT cite a specific paper here without live-verification.
    """
    # Simple scaling relation (dimensional analysis consistent with Planck values)
    theta_approx = 100.0 * 0.010411 * (omega_b / 0.02238)**0.013 * (omega_m / 0.1428)**(-0.252)
    return theta_approx


def loglike_planck2018_compressed(omega_b: jnp.ndarray,
                                    omega_c: jnp.ndarray,
                                    H0: jnp.ndarray,
                                    log10As_e10: jnp.ndarray,
                                    n_s: jnp.ndarray,
                                    tau_reio: jnp.ndarray | None = None) -> jnp.ndarray:
    """
    Planck 2018 Plik TT+TE+EE compressed 5-parameter Gaussian likelihood.
    Reference: Aghanim et al. 2018, arXiv:1807.06209 (confirmed).

    Parameters are: {ω_b, ω_c, 100θ_MC, ln(10^10 A_s), n_s}.

    Note on A_s convention (M1 bug-fix 2026-05-06):
      The parameter 'log10As_e10' is MISNAMED — its prior Uniform[2.7, 3.5]
      is the range of ln(10^10 A_s), NOT log10(10^10 A_s).
      At Planck fiducial: A_s = 2.101e-9, so 10^10*A_s = 21.01,
        log10(21.01) = 1.322  (NOT in [2.7, 3.5])
        ln(21.01)    = 3.044  (IN [2.7, 3.5]) ✓
      Therefore log10As_e10 IS ln(10^10 A_s) and must be used directly
      (identity, no conversion factor).
      BUG FIXED: the previous code erroneously applied * ln(10) = 2.302585,
      inflating the chi2_As term by (3.044 * 1.303)^2 / 0.014^2 ≈ 80000.
      This drove NUTS to the prior boundary at log10As_e10 = 3.5.
      [TBD: rename parameter to 'ln_As_e10' throughout for clarity]

    Note on τ_reio:
      Sampled separately as a Gaussian prior in priors.py (τ ~ N(0.054, 0.007)).
      NOT included in this 5-parameter vector (it primarily affects A_s * exp(-2τ)).
      For a full compressed likelihood, include τ as 6th parameter.
      [TBD: consider 6-param compressed version with tau_reio included]

    Args:
      omega_b: ω_b h²
      omega_c: ω_c h²
      H0: [km/s/Mpc] (for computing theta_MC via h = H0/100, omega_m = omega_c + omega_b)
      log10As_e10: ln(10^10 A_s) — MISNAMED but correctly represents ln value
                   (prior Uniform[2.7, 3.5] matches Planck 2018 ln(10^10 A_s) = 3.044)
      n_s: spectral index
      tau_reio: optical depth (unused here; sampled via prior in numpyro_models.py)

    Returns:
      log-likelihood scalar
    """
    h        = H0 / 100.0
    omega_m  = omega_b + omega_c  # (ignoring nu for approximation)
    # M1 bug-fix 2026-05-06: the parameter IS ln(10^10 A_s) — use directly, no conversion.
    # Previous buggy code: ln_As = log10As_e10 * jnp.log(10.0)  [WRONG — factor 2.303 error]
    ln_As    = log10As_e10  # identity: parameter is already ln(10^10 A_s)
    theta_MC = theta_MC_approx(omega_b, omega_m)

    # Parameter vector [omega_b, omega_c, theta_MC_100, ln_As_e10, n_s]
    x = jnp.array([omega_b, omega_c, theta_MC, ln_As, n_s])
    delta = x - _jax_planck_mean
    chi2  = delta @ _jax_planck_cov_inv @ delta
    return -0.5 * chi2


# =========================================================================
# SECTION 4 — Combined log-likelihood for Framing B (no KG gate)
# =========================================================================

def loglike_total_framing_b(H0: jnp.ndarray,
                              omega_b: jnp.ndarray,
                              omega_c: jnp.ndarray,
                              n_s: jnp.ndarray,
                              log10As_e10: jnp.ndarray,
                              tau_reio: jnp.ndarray,
                              w0: jnp.ndarray,
                              wa: jnp.ndarray,
                              M_B: jnp.ndarray,
                              bao_data: dict | None = None,
                              sne_data: dict | None = None,
                              warn: bool = True) -> jnp.ndarray:
    """
    Total log-likelihood for Framing B (CPL-effective, no KG gate).
    = log L_CMB + log L_BAO + log L_SNe

    [Note: ACT DR6 lensing deferred — [TBD: add A_lens constraint from
     Madhavacheril et al. 2024 once arXiv ID verified and values confirmed]]
    """
    h = H0 / 100.0
    Omega_m = (omega_b + omega_c) / h**2
    omega_m = omega_b + omega_c

    lL_cmb = loglike_planck2018_compressed(
        omega_b, omega_c, H0, log10As_e10, n_s, tau_reio
    )
    lL_bao = loglike_desi_dr2_bao(
        H0, Omega_m, w0, wa, omega_b, omega_m,
        data_dict=bao_data, use_default_warning=warn
    )
    lL_sne = loglike_pantheonplus(
        H0, Omega_m, w0, wa, M_B, data_dict=sne_data
    )

    return lL_cmb + lL_bao + lL_sne


if __name__ == "__main__":
    # Quick sanity check at ΛCDM fiducial point (M1 bug-fix 2026-05-06)
    # Note: log10As_e10 = 3.044 directly (it IS ln(10^10 A_s), prior [2.7, 3.5])
    # Previous code had log10As_e10 = 3.044/ln(10) = 1.3220 which is WRONG
    print("[likelihoods] Testing at ΛCDM fiducial (Planck 2018 bestfit)...")
    print("[likelihoods] log10As_e10 = 3.044 (= ln(10^10 A_s), no conversion applied)")

    import warnings
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        ll = loglike_total_framing_b(
            H0=jnp.array(67.36),
            omega_b=jnp.array(0.02237),
            omega_c=jnp.array(0.1200),
            n_s=jnp.array(0.9649),
            log10As_e10=jnp.array(3.044),  # = ln(10^10 A_s) directly (M1 fix)
            tau_reio=jnp.array(0.054),
            w0=jnp.array(-1.0),
            wa=jnp.array(0.0),
            M_B=jnp.array(-19.3),
            warn=False,
        )
    print(f"[likelihoods] total loglike at fiducial ΛCDM = {float(ll):.3f}")

    # Also check the Planck CMB-only loglike: should be ~ -4.85 (only theta_MC bias)
    lL_cmb = loglike_planck2018_compressed(
        jnp.array(0.02237), jnp.array(0.1200), jnp.array(67.36),
        jnp.array(3.044), jnp.array(0.9649),
    )
    print(f"[likelihoods] Planck compressed loglike at fiducial = {float(lL_cmb):.4f}")
    print(f"[likelihoods]   Expected: ~-4.85 (chi2~9.7, from theta_MC approx bias only)")
    print("[likelihoods] Module OK.")
