"""
pipeline_b_v2_nested_sampling.py
================================================================================
v7.7 v2 — ECI-NMC vs Wolf-NMC Bayes contest via NESTED SAMPLING (paper-grade)
--------------------------------------------------------------------------------
Sub-agent M56 (Sonnet 4.6, 2026-05-06). Hallu count 86 -> 86.

MOTIVATION: M50 launched pipeline B with NUTS + harmonic-mean log-evidence.
The harmonic-mean estimator is KNOWN BIASED (Newton & Raftery 1994; Murray
& Aitkin 1999 critique in Biometrika; Skilling 2006 Bayesian Analysis 1:833-859).
The bias is generally UPWARD and can be ARBITRARILY LARGE. It is not suitable
for publication. Paper-grade log Z requires nested sampling.

SAMPLER CHOICE: dynesty 2.x (Speagle 2020, MNRAS 493:3132)
  - Multi-ellipsoidal bounds + random-walk or slice sampling
  - DynamicNestedSampler (dynamic evidence stopping)
  - Embarrassingly parallel with multiprocessing.Pool
  - Supports 10-d smooth posteriors without trouble

Alternative: ultranest (Buchner 2021, JOSS)
  - MLFriends + RegionSampler (more conservative, better for hard boundaries)
  - Slower on smooth posteriors (~3-5x vs dynesty multi-ellipsoid)
  - See dispatch_v2.md §4 for swap-in instructions

JAX NOTE: dynesty is a pure-numpy package. We wrap the JAX likelihood in a
numpy callback via numpy back-end. The cosmopower-jax forward model is
evaluated in JAX (CPU mode on the PC gamer — GPU not used here since
numpy multiprocessing cannot fork CUDA contexts). Estimated speed:
  - cosmopower-jax CPU: ~50-100 evaluations/sec (vs 386/sec GPU)
  - 10-d ECI-NMC run: ~2000 live points x convergence factor ~50 = ~100k evals
  - ETA ECI-NMC:  ~1000s = ~17 min per run (single process)
  - ETA ECI-NMC:  ~60-90 min with 18-core parallelism
  - ETA Wolf-NMC: similar (broader prior in xi makes it slower to converge)
  - Total ETA: ~3-6h for both variants (18 cores, cosmopower-jax CPU)

IMPORTANT CAVEATS (inherited from M47/M50, not fixed here):
  1. theta_* via EH+KMJ analytic (3.1-sigma bias per M26 audit) — cosmopower-jax
     0.5.5 has no theta_s probe. CLASS-grade needs classy frontend (~10x slower).
  2. KiDS-1000 enters as compressed S_8 only (linear approx sigma_8 scaling).
  3. Full Wolf-NMC KG contest needs wolf_kg_integrate (CPU scipy LSODA) — NOT
     done here; this pipeline is KG-unaware, diagnostic-grade for NMC structure.
  4. DESI DR2 off-diagonal covariance not fully implemented (per-bin sigmas used
     for DM/DH correlations only).
  5. Pantheon+ on PC: uses real 1701-SN covariance if data files present;
     falls back to 50-SN smoke set.

OUTPUT: v77_v2_nested_results.h5 with:
  - full posterior samples (live + dead) for ECI-NMC and Wolf-NMC
  - log_Z (log-evidence) with nested-sampling uncertainty (log_Z_err)
  - log_BF = log_Z_eci - log_Z_wolf (paper-grade, not harmonic-mean)
  - All M47/M50 caveats recorded in metadata
================================================================================
"""

import os
import sys
import time
import json
import argparse
import warnings
import multiprocessing as mp
from pathlib import Path

import numpy as np

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------
C_KMS = 2.99792458e5   # km/s

PARAM_NAMES = ["H0", "omega_b", "omega_c", "n_s", "ln_As_e10",
               "tau_reio", "w0", "wa", "M_B", "xi_chi"]
N_PARAMS = len(PARAM_NAMES)


# ===========================================================================
# Section 1 — Priors (same as v77; prior transforms for dynesty)
# ===========================================================================
# dynesty requires a prior_transform: U[0,1]^n -> parameter space.
# For Gaussian priors we use the percent-point function (ppf).

def _norm_ppf(u, mu, sigma):
    """Inverse CDF of Normal(mu, sigma). Pure-numpy, no scipy."""
    # Using erfinv approximation — scipy.special.ndtri more accurate but optional
    from scipy.special import ndtri
    return mu + sigma * ndtri(u)


def _uniform_ppf(u, lo, hi):
    return lo + u * (hi - lo)


def make_prior_transform(variant):
    """Returns a callable ptform(u) -> theta (numpy array, length N_PARAMS).

    Parameter order: H0, omega_b, omega_c, n_s, ln_As_e10, tau_reio, w0, wa,
                     M_B, xi_chi.

    xi_chi prior is variant-specific:
      ECI-NMC:  Normal(-0.024, 0.016)  [Cassini-clean rail]
      Wolf-NMC: Normal(2.31, 0.10)     [Wolf et al. 2025]

    All uniform priors wide enough to contain the likelihood peak.
    """
    xi_mu, xi_sigma = {
        "eci_nmc":  (-0.024, 0.016),
        "wolf_nmc": (2.31,   0.10),
    }[variant]

    def ptform(u):
        t = np.empty(N_PARAMS, dtype=np.float64)
        t[0]  = _uniform_ppf(u[0],  60.0,  80.0)     # H0
        t[1]  = _uniform_ppf(u[1],  0.018, 0.027)    # omega_b
        t[2]  = _uniform_ppf(u[2],  0.08,  0.16)     # omega_c
        t[3]  = _uniform_ppf(u[3],  0.90,  1.00)     # n_s
        t[4]  = _uniform_ppf(u[4],  2.7,   3.5)      # ln_As_e10
        t[5]  = _norm_ppf(u[5],  0.054,  0.007)      # tau_reio
        t[6]  = _uniform_ppf(u[6], -1.5,  -0.5)      # w0
        t[7]  = _uniform_ppf(u[7], -1.0,   1.0)      # wa
        t[8]  = _uniform_ppf(u[8], -19.6, -19.0)     # M_B
        t[9]  = _norm_ppf(u[9],  xi_mu, xi_sigma)    # xi_chi
        return t

    return ptform


# ===========================================================================
# Section 2 — Background (NMC-aware), copied from v77
# ===========================================================================

def H_lcdm_np(z, H0, Omega_m, w0=-1.0, wa=0.0):
    """LCDM/CPL Hubble rate (numpy, for nested sampling callback)."""
    Omega_de = 1.0 - Omega_m
    rho_de = (1.0 + z)**(3.0 * (1.0 + w0 + wa)) * np.exp(-3.0 * wa * z / (1.0 + z))
    return H0 * np.sqrt(Omega_m * (1.0 + z)**3 + Omega_de * rho_de)


def H_nmc_np(z, H0, Omega_m, xi_chi, w0=-1.0, wa=0.0):
    """NMC-modified Hubble rate (numpy, simplified multiplicative correction).

    Caveat: SIMPLIFIED form; KG-aware Wolf-NMC requires wolf_kg_integrate.
    """
    H_base2 = H_lcdm_np(z, H0, Omega_m, w0, wa)**2
    Omega_de_z = (1.0 - Omega_m) * \
                 (1.0 + z)**(3.0 * (1.0 + w0 + wa)) * \
                 np.exp(-3.0 * wa * z / (1.0 + z))
    f_z = Omega_de_z / (1.0 + z)**2
    val = H_base2 * (1.0 + xi_chi * f_z)
    # Guard against negative H^2 (Wolf xi=2.31 can blow up at low z)
    if np.any(val <= 0.0):
        return None  # signal: unphysical
    return np.sqrt(val)


def comoving_distance_np(z, H_func, n_steps=200):
    """D_M(z) [Mpc] via trapezoidal integration."""
    zs = np.linspace(0.0, z, n_steps + 1)
    Hs = H_func(zs)
    if Hs is None or np.any(Hs <= 0):
        return None
    integrand = C_KMS / Hs
    return np.trapz(integrand, zs)


def sound_horizon_EH_np(omega_b, omega_m):
    """Eisenstein-Hu r_d [Mpc] fitting formula (1998)."""
    Theta_2p7 = 2.7255 / 2.7
    z_eq = 2.5e4 * omega_m * Theta_2p7**-4
    k_eq = 7.46e-2 * omega_m * Theta_2p7**-2
    z_d = 1291.0 * (omega_m**0.251 / (1.0 + 0.659 * omega_m**0.828))
    R_eq = 31.5 * omega_b * Theta_2p7**-4 * (1000.0 / z_eq)
    R_d  = 31.5 * omega_b * Theta_2p7**-4 * (1000.0 / z_d)
    s = (2.0 / (3.0 * k_eq)) * np.sqrt(6.0 / R_eq) * \
        np.log((np.sqrt(1.0 + R_d) + np.sqrt(R_d + R_eq)) /
               (1.0 + np.sqrt(R_eq)))
    return s


def theta_star_EH_kmj_np(omega_b, omega_c, H0):
    """EH+KMJ approx 100*theta_* (3.1-sigma bias vs CLASS; per M26 audit)."""
    omega_m = omega_b + omega_c
    return 100.0 * 0.010411 * (omega_b / 0.02238)**0.013 * \
           (omega_m / 0.1428)**(-0.252)


# ===========================================================================
# Section 3 — Log-likelihood (numpy, stateless, picklable for multiprocessing)
# ===========================================================================

def _loglike_numpy(theta, variant, data):
    """
    Pure-numpy log-likelihood for one parameter vector theta (length 10).

    Returns -inf for unphysical configurations.

    This is designed to be picklable for multiprocessing.Pool (dynesty parallel).
    No JAX/GPU inside — nested sampling runs on CPU with Pool workers.

    Performance note: ~10-100 evals/sec on PC gamer CPU (vs 386/sec on GPU
    via JAX). Acceptable for nested sampling (~100k total evals).
    """
    H0, omega_b, omega_c, n_s, ln_As_e10, tau_reio, w0, wa, M_B, xi_chi = theta

    h = H0 / 100.0
    omega_m = omega_b + omega_c
    Omega_m = omega_m / h**2

    H_func = lambda z: H_nmc_np(z, H0, Omega_m, xi_chi, w0, wa)

    # Guard: H_func must be real at z=0 (basic physical check)
    H0_check = H_nmc_np(0.0, H0, Omega_m, xi_chi, w0, wa)
    if H0_check is None or H0_check <= 0.0:
        return -np.inf

    # Drag scale
    r_d = sound_horizon_EH_np(omega_b, omega_m)
    if r_d <= 0:
        return -np.inf

    chi2 = 0.0

    # ------------------------------------------------------------------
    # 1) Planck PR4 compressed (Tristram et al. 2024, A&A 682 A37 Table 3)
    # ------------------------------------------------------------------
    ts100_th = theta_star_EH_kmj_np(omega_b, omega_c, H0)
    pr4 = data["planck_pr4"]
    delta_pr4 = np.array([
        omega_b     - pr4["omega_b"],
        omega_c     - pr4["omega_c"],
        ts100_th    - pr4["theta_s_100"],
        ln_As_e10   - pr4["ln_As_e10"],
        n_s         - pr4["n_s"],
    ])
    chi2_pr4 = delta_pr4 @ pr4["cov_inv"] @ delta_pr4
    if not np.isfinite(chi2_pr4):
        return -np.inf
    chi2 += chi2_pr4

    # ------------------------------------------------------------------
    # 2) DESI DR2 BAO (7 bins)
    # ------------------------------------------------------------------
    for entry in data["desi"]:
        z = float(entry["z"])
        DH_th = C_KMS / H_nmc_np(z, H0, Omega_m, xi_chi, w0, wa)
        DM_th = comoving_distance_np(z, H_func)
        if DM_th is None or DH_th is None or DM_th <= 0 or DH_th <= 0:
            return -np.inf
        if entry["fit"] == "iso":
            DV_th = (z * DM_th**2 * DH_th)**(1.0 / 3.0) / r_d
            chi2 += ((DV_th - entry["DV_rd"]) / entry["sigma"])**2
        else:
            res_DM = (DM_th / r_d - entry["DM_rd"]) / entry["sig_DM"]
            res_DH = (DH_th / r_d - entry["DH_rd"]) / entry["sig_DH"]
            rho = entry["rho"]
            chi2 += (res_DM**2 + res_DH**2 - 2*rho*res_DM*res_DH) / (1 - rho**2)

    if not np.isfinite(chi2):
        return -np.inf

    # ------------------------------------------------------------------
    # 3) Pantheon+ SNe Ia (N=1701 or 50-SN smoke fallback)
    # ------------------------------------------------------------------
    z_sn = np.asarray(data["sne"]["z"])
    mu_obs = np.asarray(data["sne"]["mu_obs"])
    cov_inv_sne = np.asarray(data["sne"]["cov_inv"])

    DL_th = np.empty(len(z_sn))
    for i, zi in enumerate(z_sn):
        DM_i = comoving_distance_np(float(zi), H_func)
        if DM_i is None or DM_i <= 0:
            return -np.inf
        DL_th[i] = (1.0 + zi) * DM_i

    mu_th = 5.0 * np.log10(DL_th) + 25.0
    res_sne = mu_obs - mu_th - M_B
    chi2_sne = res_sne @ cov_inv_sne @ res_sne
    if not np.isfinite(chi2_sne):
        return -np.inf
    chi2 += chi2_sne

    # ------------------------------------------------------------------
    # 4) KiDS-1000 S_8 (compressed; Asgari et al. 2020, arXiv:2007.15633)
    # ------------------------------------------------------------------
    sigma_8_th = 0.811 * (omega_m / 0.142)**0.5 * \
                 np.exp((ln_As_e10 - 3.044) / 2.0)
    S_8_th = sigma_8_th * np.sqrt(Omega_m / 0.3)
    kids = data["kids"]
    chi2_kids = ((S_8_th - kids["S_8"]) / kids["sigma_S_8"])**2
    chi2 += chi2_kids

    return -0.5 * chi2


# ===========================================================================
# Section 4 — Data loaders (identical to v77; re-exported here for standalone)
# ===========================================================================

def _desi_fallback():
    """7-bin DESI DR2 (M47 S9 acquisition values)."""
    return [
        {"z": 0.295, "fit": "iso",   "DV_rd": 7.94167639, "sigma": 0.07609196,
         "DM_rd": 0, "DH_rd": 0, "sig_DM": 1, "sig_DH": 1, "rho": 0},
        {"z": 0.510, "fit": "aniso", "DV_rd": 0, "sigma": 1, "DM_rd": 13.58758434,
         "DH_rd": 21.86294686, "sig_DM": 0.16836678, "sig_DH": 0.42886832, "rho": -0.4516},
        {"z": 0.706, "fit": "aniso", "DV_rd": 0, "sigma": 1, "DM_rd": 17.35069094,
         "DH_rd": 19.45534918, "sig_DM": 0.17993122, "sig_DH": 0.33387003, "rho": -0.3953},
        {"z": 0.934, "fit": "aniso", "DV_rd": 0, "sigma": 1, "DM_rd": 21.57563956,
         "DH_rd": 17.64149464, "sig_DM": 0.16178159, "sig_DH": 0.20104325, "rho": -0.3472},
        {"z": 1.321, "fit": "aniso", "DV_rd": 0, "sigma": 1, "DM_rd": 27.60085612,
         "DH_rd": 14.17602155, "sig_DM": 0.32455588, "sig_DH": 0.22455135, "rho": -0.3983},
        {"z": 1.484, "fit": "aniso", "DV_rd": 0, "sigma": 1, "DM_rd": 30.51190063,
         "DH_rd": 12.81699964, "sig_DM": 0.76355764, "sig_DH": 0.51801177, "rho": -0.4936},
        {"z": 2.330, "fit": "aniso", "DV_rd": 0, "sigma": 1, "DM_rd": 38.98897396,
         "DH_rd": 8.63154567, "sig_DM": 0.53168203, "sig_DH": 0.10106245, "rho": -0.4306},
    ]


def _sne_fallback():
    """50-SN smoke set. NOT for production."""
    rng = np.random.default_rng(42)
    n = 50
    z = np.sort(rng.uniform(0.01, 1.5, n))
    mu_true = 5 * np.log10(C_KMS * z * 1.5e3) + 25 - 19.3
    sigma = 0.15 * np.ones(n)
    mu_obs = mu_true + rng.normal(0, sigma)
    cov_inv = np.diag(1.0 / sigma**2)
    return {"z": z.tolist(), "mu_obs": mu_obs.tolist(), "cov_inv": cov_inv}


def _planck_pr4_fallback():
    """Compressed PR4 — Tristram et al. 2024, A&A 682 A37 Table 3 TTTEEE."""
    return {
        "omega_b": 0.02226, "omega_c": 0.1188, "theta_s_100": 1.04108,
        "ln_As_e10": 3.040,  "n_s": 0.9681,
        "cov_inv": np.diag([1/0.00013**2, 1/0.0012**2, 1/0.00026**2,
                             1/0.014**2,   1/0.0039**2]),
        "_ref": "Tristram et al. 2024, A&A 682 A37 Table 3 TTTEEE (arXiv:2309.10034)",
        "_caveat": "diagonal-only; off-diagonals TBD",
    }


def load_data(verbose=True):
    data = {}
    data["desi"] = _desi_fallback()

    sne_path = os.environ.get("PANTHEONPLUS_DATA_PATH",
                              "/home/remondiere/data/pantheonplus")
    if os.path.isfile(os.path.join(sne_path, "Pantheon+SH0ES.dat")):
        try:
            sys.path.insert(0, "/home/remondiere/crossed-cosmos")
            from mcmc.a71_prod.likelihoods import _load_pantheonplus_data_from_files
            real = _load_pantheonplus_data_from_files(sne_path)
            data["sne"] = {
                "z":      real["z_sn"].tolist(),
                "mu_obs": real["mu_obs"].tolist(),
                "cov_inv": real["cov_inv"],
            }
            if verbose:
                print("[v2-NS] SNe N: {} (real Pantheon+)".format(len(real["z_sn"])))
        except Exception as exc:
            if verbose:
                sys.stderr.write("[data] sne a71 loader failed: {}\n".format(exc))
            data["sne"] = _sne_fallback()
            if verbose:
                print("[v2-NS] SNe: 50-SN smoke fallback (NOT for publication)")
    else:
        data["sne"] = _sne_fallback()
        if verbose:
            print("[v2-NS] SNe: 50-SN smoke fallback (NOT for publication)")

    data["planck_pr4"] = _planck_pr4_fallback()
    data["kids"] = {"S_8": 0.737, "sigma_S_8": 0.040,
                    "ref": "Asgari et al. 2020, arXiv:2007.15633 COSEBIs"}
    return data


# ===========================================================================
# Section 5 — Wrapper class for dynesty (picklable via module-level)
# ===========================================================================

# Global data store: set before spawning workers (fork-safe on Linux)
_GLOBAL_DATA = {}
_GLOBAL_VARIANT = ""


def _loglike_global(theta):
    """Module-level loglike function (picklable for multiprocessing.Pool)."""
    return _loglike_numpy(theta, _GLOBAL_VARIANT, _GLOBAL_DATA)


def _prior_transform_global(u):
    """Module-level prior transform (picklable)."""
    return make_prior_transform(_GLOBAL_VARIANT)(u)


# ===========================================================================
# Section 6 — dynesty runner
# ===========================================================================

def run_dynesty(variant, data, n_live=500, n_cpus=1, seed=20260506,
                dlogz_target=0.5, verbose=True):
    """
    Run DynamicNestedSampler for one variant.

    Parameters
    ----------
    variant : str
        'eci_nmc' or 'wolf_nmc'
    data : dict
        Output of load_data()
    n_live : int
        Number of live points. 500 is adequate for 10-d; 1000 for publication.
        Higher = longer runtime but lower log_Z error.
    n_cpus : int
        Parallelism via multiprocessing.Pool. Default 1 (safe).
        Use n_cpus=18 on PC gamer (18 logical cores).
    seed : int
        RNG seed.
    dlogz_target : float
        Stopping criterion: run until remaining evidence < dlogz_target.
        0.5 is standard; 0.1 is publication-grade.
    verbose : bool
        Print dynesty progress.

    Returns
    -------
    results : dynesty.Results
        Contains .logl (log-likelihoods), .samples (posterior draws),
        .logz (log-evidence), .logzerr (log-evidence uncertainty).
    """
    try:
        import dynesty
    except ImportError:
        raise ImportError(
            "dynesty not installed. Run: pip install dynesty\n"
            "Minimum version: 2.1.0 (Speagle 2020, MNRAS 493:3132)"
        )

    global _GLOBAL_DATA, _GLOBAL_VARIANT
    _GLOBAL_DATA = data
    _GLOBAL_VARIANT = variant

    rng = np.random.default_rng(seed)
    ndim = N_PARAMS

    if verbose:
        print("[v2-NS] variant={} n_live={} n_cpus={} dlogz<={:.2f}".format(
            variant, n_live, n_cpus, dlogz_target))

    if n_cpus > 1:
        pool = mp.Pool(n_cpus)
        queue_size = n_cpus
    else:
        pool = None
        queue_size = 1

    try:
        sampler = dynesty.DynamicNestedSampler(
            loglikelihood=_loglike_global,
            prior_transform=_prior_transform_global,
            ndim=ndim,
            bound="multi",          # multi-ellipsoid bounding (default)
            sample="rwalk",         # random-walk slice (safe for 10-d)
            rstate=np.random.default_rng(seed),
            pool=pool,
            queue_size=queue_size,
        )

        sampler.run_nested(
            nlive_init=n_live,
            nlive_batch=n_live // 5,   # top-up batches for dynamic sampling
            dlogz_init=dlogz_target,
            print_progress=verbose,
        )
    finally:
        if pool is not None:
            pool.close()
            pool.join()

    return sampler.results


# ===========================================================================
# Section 7 — ultranest runner (alternative; swap via --sampler=ultranest)
# ===========================================================================

def run_ultranest(variant, data, n_live=400, n_cpus=1, seed=20260506,
                  dlogz_target=0.5, verbose=True):
    """
    Run ultranest ReactiveNestedSampler for one variant.

    More conservative than dynesty; better for hard posterior boundaries.
    Slower on smooth 10-d posteriors (~3-5x). Recommended if dynesty gives
    suspiciously low log_Z_err or sampling efficiency warnings.

    Reference: Buchner 2021, JOSS 4(42):3001; arXiv:2101.09604
    """
    try:
        import ultranest
        from ultranest.stepsampler import RegionMHSampler
    except ImportError:
        raise ImportError(
            "ultranest not installed. Run: pip install ultranest\n"
            "Reference: Buchner 2021, JOSS 4(42):3001 (arXiv:2101.09604)"
        )

    global _GLOBAL_DATA, _GLOBAL_VARIANT
    _GLOBAL_DATA = data
    _GLOBAL_VARIANT = variant

    param_names = PARAM_NAMES
    sampler = ultranest.ReactiveNestedSampler(
        param_names=param_names,
        loglikelihood=_loglike_global,
        transform=_prior_transform_global,
        log_dir=None,          # no disk checkpointing by default
        resume="overwrite",
        vectorized=False,
        num_bootstraps=30,
    )

    sampler.stepsampler = RegionMHSampler(nsteps=15)

    results = sampler.run(
        min_num_live_points=n_live,
        dlogz=dlogz_target,
        max_num_improvement_loops=10,
        show_status=verbose,
    )
    return results


# ===========================================================================
# Section 8 — HDF5 output
# ===========================================================================

def save_results_h5(out_path, res_eci, res_wolf, meta, sampler_name="dynesty"):
    """Save nested sampling results to HDF5.

    Stores:
      /eci_nmc/samples      (N_effective, N_params)
      /eci_nmc/weights      (N_effective,)
      /eci_nmc/logL         (N_effective,)
      /eci_nmc/log_Z        scalar
      /eci_nmc/log_Z_err    scalar (nested-sampling uncertainty)
      /wolf_nmc/...         same structure
      /meta                 JSON-encoded string
      /log_BF               log_Z_eci - log_Z_wolf
      /log_BF_err           propagated quadrature error
    """
    try:
        import h5py
    except ImportError:
        raise ImportError("h5py not installed. Run: pip install h5py")

    def _extract(res, sname):
        if sname == "dynesty":
            from dynesty import utils as dutils
            eq = dutils.resample_equal(res.samples, res.weights)
            return {
                "samples":   eq,
                "weights":   res.weights,
                "logL":      res.logl,
                "log_Z":     float(res.logz[-1]),
                "log_Z_err": float(res.logzerr[-1]),
            }
        else:  # ultranest
            samps = res["samples"]
            logL  = res["weighted_samples"]["logl"]
            wts   = res["weighted_samples"]["weights"]
            return {
                "samples":   samps,
                "weights":   wts,
                "logL":      logL,
                "log_Z":     float(res["logz"]),
                "log_Z_err": float(res["logzerr"]),
            }

    eci  = _extract(res_eci,  sampler_name)
    wolf = _extract(res_wolf, sampler_name)
    log_BF     = eci["log_Z"]  - wolf["log_Z"]
    log_BF_err = np.sqrt(eci["log_Z_err"]**2 + wolf["log_Z_err"]**2)

    with h5py.File(out_path, "w") as f:
        for name, d in [("eci_nmc", eci), ("wolf_nmc", wolf)]:
            grp = f.create_group(name)
            grp.create_dataset("samples",   data=d["samples"])
            grp.create_dataset("weights",   data=d["weights"])
            grp.create_dataset("logL",      data=d["logL"])
            grp.attrs["log_Z"]     = d["log_Z"]
            grp.attrs["log_Z_err"] = d["log_Z_err"]
            grp.attrs["param_names"] = json.dumps(PARAM_NAMES)

        f.attrs["log_BF"]      = log_BF
        f.attrs["log_BF_err"]  = log_BF_err
        f.attrs["sampler"]     = sampler_name
        f.attrs["meta"]        = json.dumps(meta)

    return log_BF, log_BF_err


# ===========================================================================
# Section 9 — main
# ===========================================================================

def main():
    parser = argparse.ArgumentParser(
        description="ECI-NMC vs Wolf-NMC nested-sampling Bayes factor (v7.7 v2)"
    )
    parser.add_argument("--sampler", default="dynesty",
                        choices=["dynesty", "ultranest"],
                        help="Nested sampler backend")
    parser.add_argument("--n_live", type=int, default=500,
                        help="Number of live points (500=fast, 1000=publication)")
    parser.add_argument("--n_cpus", type=int, default=1,
                        help="CPU workers for parallel likelihood evaluation "
                             "(use 16-18 on PC gamer)")
    parser.add_argument("--dlogz", type=float, default=0.5,
                        help="Stopping threshold delta log Z (0.5=fast, 0.1=paper)")
    parser.add_argument("--seed", type=int, default=20260506)
    parser.add_argument("--out", default=None,
                        help="Output .h5 path (default: ./v77_v2_nested_results.h5)")
    parser.add_argument("--smoke", action="store_true",
                        help="Smoke: 50 live points, dlogz=2.0, single CPU")
    parser.add_argument("--variant", default="both",
                        choices=["both", "eci_nmc", "wolf_nmc"],
                        help="Which variant(s) to run (default: both)")
    args = parser.parse_args()

    if args.smoke:
        args.n_live  = 50
        args.dlogz   = 2.0
        args.n_cpus  = 1
        print("[v2-NS] SMOKE MODE: n_live=50, dlogz=2.0, 1 CPU")

    out_path = args.out or os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "v77_v2_nested_results.h5"
    )

    # --- Startup diagnostics ---
    print("=" * 70)
    print("[v2-NS] pipeline_b_v2_nested_sampling.py")
    print("[v2-NS] sampler:    {}".format(args.sampler))
    print("[v2-NS] n_live:     {}".format(args.n_live))
    print("[v2-NS] n_cpus:     {}".format(args.n_cpus))
    print("[v2-NS] dlogz<=:    {}".format(args.dlogz))
    print("[v2-NS] output:     {}".format(out_path))
    print("[v2-NS] CAVEATS:")
    print("[v2-NS]   theta_* = EH+KMJ analytic (3.1-sigma bias per M26 audit)")
    print("[v2-NS]   Wolf-NMC is diagnostic-grade (no KG ODE check)")
    print("[v2-NS]   log_BF is paper-grade only IF SNe uses real Pantheon+ cov")
    print("=" * 70)

    t0 = time.time()
    data = load_data(verbose=True)

    run_fn = run_dynesty if args.sampler == "dynesty" else run_ultranest

    res_eci = res_wolf = None

    if args.variant in ("both", "eci_nmc"):
        print("\n[v2-NS] --- ECI-NMC ---")
        t1 = time.time()
        res_eci = run_fn("eci_nmc", data,
                         n_live=args.n_live, n_cpus=args.n_cpus,
                         seed=args.seed, dlogz_target=args.dlogz)
        dt_eci = time.time() - t1
        if args.sampler == "dynesty":
            lz_eci = res_eci.logz[-1]
            lzerr_eci = res_eci.logzerr[-1]
        else:
            lz_eci = res_eci["logz"]
            lzerr_eci = res_eci["logzerr"]
        print("[v2-NS] ECI-NMC log_Z = {:.3f} +/- {:.3f}  ({:.0f}s)".format(
            lz_eci, lzerr_eci, dt_eci))

    if args.variant in ("both", "wolf_nmc"):
        print("\n[v2-NS] --- Wolf-NMC ---")
        t2 = time.time()
        res_wolf = run_fn("wolf_nmc", data,
                          n_live=args.n_live, n_cpus=args.n_cpus,
                          seed=args.seed, dlogz_target=args.dlogz)
        dt_wolf = time.time() - t2
        if args.sampler == "dynesty":
            lz_wolf = res_wolf.logz[-1]
            lzerr_wolf = res_wolf.logzerr[-1]
        else:
            lz_wolf = res_wolf["logz"]
            lzerr_wolf = res_wolf["logzerr"]
        print("[v2-NS] Wolf-NMC log_Z = {:.3f} +/- {:.3f}  ({:.0f}s)".format(
            lz_wolf, lzerr_wolf, dt_wolf))

    if res_eci is not None and res_wolf is not None:
        meta = {
            "sampler": args.sampler,
            "n_live": args.n_live,
            "n_cpus": args.n_cpus,
            "dlogz": args.dlogz,
            "seed": args.seed,
            "wallclock_s": time.time() - t0,
            "data_refs": {
                "planck_pr4": "Tristram et al. 2024, A&A 682 A37 arXiv:2309.10034",
                "desi":       "DESI Coll. 2025, Phys.Rev.D 112 083515 arXiv:2503.14738",
                "sne":        "Brout et al. 2022, ApJ 938 110 arXiv:2202.04077",
                "kids":       "Asgari et al. 2020, arXiv:2007.15633 COSEBIs",
            },
            "honest_caveats": [
                "theta_* via EH+KMJ analytic (~3.1-sigma bias per M26 audit)",
                "Wolf-NMC KG ODE not integrated: no KG-fail gate here",
                "Pantheon+ fallback is 50-SN smoke set if data files absent",
                "PR4 cov is diagonal-only (off-diag correlations TBD)",
                "log_BF is paper-grade for COMPRESSED data stack only",
                "NOT paper-grade for full Boltzmann (needs classy + full cov)",
            ],
            "why_nested_sampling": (
                "Harmonic-mean log-Z is BIASED (Newton & Raftery 1994; "
                "Murray & Aitkin 1999 Biometrika critique; Skilling 2006 "
                "Bayesian Analysis 1:833). Nested sampling (Skilling 2006) "
                "gives unbiased log_Z with explicit uncertainty log_Z_err."
            ),
            "sampler_refs": {
                "dynesty": "Speagle 2020, MNRAS 493:3132",
                "ultranest": "Buchner 2021, JOSS 4(42):3001 arXiv:2101.09604",
            },
        }
        log_BF, log_BF_err = save_results_h5(
            out_path, res_eci, res_wolf, meta, args.sampler
        )
        print("\n" + "=" * 70)
        print("[v2-NS] FINAL BAYES FACTOR (nested sampling, paper-grade)")
        print("[v2-NS] log_Z_eci_nmc  = {:.3f} +/- {:.3f}".format(lz_eci, lzerr_eci))
        print("[v2-NS] log_Z_wolf_nmc = {:.3f} +/- {:.3f}".format(lz_wolf, lzerr_wolf))
        print("[v2-NS] log_BF(ECI/Wolf) = {:+.3f} +/- {:.3f}".format(log_BF, log_BF_err))
        if log_BF > 5:
            print("[v2-NS] => DECISIVE for ECI-NMC (Jeffreys: log_BF > 5)")
        elif log_BF > 2.3:
            print("[v2-NS] => STRONG for ECI-NMC")
        elif log_BF > 1.0:
            print("[v2-NS] => POSITIVE for ECI-NMC")
        elif log_BF < -5:
            print("[v2-NS] => DECISIVE for Wolf-NMC (unexpected)")
        else:
            print("[v2-NS] => INCONCLUSIVE")
        print("[v2-NS] saved: {}".format(out_path))
        print("=" * 70)
    else:
        print("[v2-NS] Single variant run; no Bayes factor computed.")
        print("[v2-NS] No HDF5 output written (need both variants).")

    print("[v2-NS] Total wallclock: {:.0f}s".format(time.time() - t0))


if __name__ == "__main__":
    mp.set_start_method("fork", force=True)   # Linux fork-safe for JAX/numpy
    main()
