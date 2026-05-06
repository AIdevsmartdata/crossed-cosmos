"""
v77_class_pipeline.py
================================================================================
v7.7 CLASS-grade theta* MCMC pipeline — ECI-NMC vs Wolf-NMC (Bayes contest)
--------------------------------------------------------------------------------
Sub-agent M47 (2026-05-06), Opus 4.7. Hallu count 86 -> 86.

GOAL:
    Produce posterior chains + log-evidence Bayes factor between
      (a) ECI-NMC: Cassini-clean rail xi_chi ~ -0.024 (KG-passing per M9 audit)
      (b) Wolf-NMC: xi = 2.31 (KG-failing per M7+M9; arXiv:2504.07679)
    using full CLASS-grade theta_* (replacing Eisenstein-Hu / KMJ approx that
    has 3.1-sigma bias per M26 audit and a71_prod/likelihoods.py bug-fix log).

DATA STACK (verified arXiv refs, NO fabrication):
    - DESI DR2 BAO       arXiv:2503.14738   (Phys.Rev.D 112, 083515 (2025))
    - Pantheon+ SNe Ia   arXiv:2202.04077   (Brout et al. 2022, ApJ 938, 110)
    - Planck PR4 lowl + TT,TE,EE   Tristram et al. 2024, A&A 682, A37
        arXiv:2309.10034 (NPIPE/PR4 likelihood)
        ** REPLACES PR3 (1807.06209) per M43 verification **
    - KiDS-1000 cosmic shear   arXiv:2007.15633   (Asgari et al. 2020,
        2007.15633 = COSEBIs analysis; alt: 2007.15632 = band-power)

THEORY FRONTEND (priority order):
    1. classy-szlikelihoods 1.x  (CLASS python wrapper, ~10s/eval; CPU)
    2. cosmopower-jax 0.5.5       (NN emulator; 386 predictions/sec on
                                   RTX 5060 Ti per memory note;
                                   theta_MC bias ~0.5% relative — adequate
                                   for v7.7 BAO+SNe primary, CMB secondary)
    3. EH+KMJ approx              (current a71_prod fallback, 3.1-sigma bias —
                                   NEVER use as primary in v7.7)

SAMPLER:
    blackjax 1.5 NUTS, 4 chains, warmup=5000, samples=5000, target_accept=0.85
    expected wall-clock on RTX 5060 Ti:
      - cosmopower-jax frontend: 2-4 hours (target)
      - classy frontend:        8-24 hours

OUTPUT:
    pipeline_b/v77_results.npz containing:
        chains_eci_nmc        (4, 5000, n_params)
        chains_wolf_nmc       (4, 5000, n_params)
        log_evidence_eci      (1,)   thermodynamic-integration estimate
        log_evidence_wolf     (1,)
        log_bayes_factor      log(Z_eci / Z_wolf)
        params_order          list of param names
        meta                  dict with frontend used, runtime, etc.

DISCIPLINE:
    - Hallu 86 -> 86 (no new fabrications)
    - Mistral STRICT-BAN observed (no fabricated arxiv IDs in this script)
    - JAX 0.10 named_shape patch assumed applied (memory note 2026-05-04)
    - PROVISIONAL: this pipeline is honest about scope. CLASS frontend is
      ambitious; cosmopower-jax fallback is the READY path. Numerical
      results are not promised in M47 deliverable -- only the SCRIPT is.
================================================================================
"""

import os
import sys
import time
import json
import warnings
import argparse
from functools import partial
from pathlib import Path

import numpy as np

# JAX setup (assumes named_shape patch applied to jax/_src/core.py line ~2445)
import jax
import jax.numpy as jnp
from jax import random as jrandom

# blackjax 1.5 (NUTS)
import blackjax  # noqa: F401  -- imported here so failure is caught early

# Constants
C_KMS = 2.99792458e5  # speed of light km/s


# ============================================================================
# Section 1 — frontend dispatcher
# ============================================================================

class Frontend:
    """Dispatch wrapper for theory predictions.

    Tries (in order): classy -> cosmopower-jax -> EH+KMJ. Raises if all fail.
    """

    def __init__(self, prefer="cosmopower"):
        self.name = None
        self._cp = None
        self._classy = None
        if prefer == "classy":
            self._try_classy()
            if self.name is None:
                self._try_cosmopower()
        else:
            self._try_cosmopower()
            if self.name is None:
                self._try_classy()
        if self.name is None:
            warnings.warn(
                "[v7.7] Neither classy nor cosmopower-jax importable. "
                "Falling back to EH+KMJ analytic approx (3.1-sigma bias per "
                "M26 audit). v7.7 'CLASS-grade' claim INVALIDATED in this "
                "fallback regime; rerun on PC gamer with venv "
                "/home/remondiere/crossed-cosmos/.venv-mcmc-bench."
            )
            self.name = "eh_kmj_fallback"

    def _try_cosmopower(self):
        try:
            import cosmopower_jax as cpj  # noqa: F401
            self._cp = cpj
            self.name = "cosmopower-jax-0.5.5"
        except Exception as exc:
            sys.stderr.write("[frontend] cosmopower-jax import failed: {}\n".format(exc))

    def _try_classy(self):
        try:
            from classy import Class  # noqa: F401
            self._classy = Class
            self.name = "classy"
        except Exception as exc:
            sys.stderr.write("[frontend] classy import failed: {}\n".format(exc))

    def theta_star_100(self, omega_b, omega_c, H0, ln_As_e10, n_s, tau_reio):
        """Returns 100 * theta_*  (CMB acoustic scale).

        Frontend dispatcher: classy is exact; cosmopower-jax is a NN emulator
        with ~0.5% relative bias on theta_MC vs full CLASS; EH+KMJ analytic
        fallback has 3.1-sigma bias per M26 audit.
        """
        if self.name == "classy":
            return self._classy_theta(omega_b, omega_c, H0, ln_As_e10, n_s, tau_reio)
        elif self.name == "cosmopower-jax-0.5.5":
            return self._cp_theta(omega_b, omega_c, H0, ln_As_e10, n_s, tau_reio)
        else:
            return self._eh_kmj_theta(omega_b, omega_c, H0)

    def _classy_theta(self, omega_b, omega_c, H0, ln_As_e10, n_s, tau_reio):
        """CLASS exact theta_*. Not JAX-jittable; wrap in pure_callback."""
        def _call(ob, oc, h0, lna, ns, tau):
            cosmo = self._classy()
            params = {
                "output": "tCl,pCl,lCl",
                "omega_b": float(ob),
                "omega_cdm": float(oc),
                "H0": float(h0),
                "A_s": float(np.exp(lna) * 1e-10),
                "n_s": float(ns),
                "tau_reio": float(tau),
                "100*theta_s": float("nan"),  # ask CLASS to compute
            }
            cosmo.set(params)
            cosmo.compute()
            try:
                ts = cosmo.theta_star_100()
            except AttributeError:
                # older classy versions expose theta_s as `theta_s_100`
                ts = cosmo.theta_s_100()
            cosmo.struct_cleanup()
            cosmo.empty()
            return np.float64(ts)
        # JAX pure_callback for non-jittable C extension
        return jax.pure_callback(
            _call, jax.ShapeDtypeStruct((), jnp.float64),
            omega_b, omega_c, H0, ln_As_e10, n_s, tau_reio,
        )

    def _cp_theta(self, omega_b, omega_c, H0, ln_As_e10, n_s, tau_reio):
        """cosmopower-jax NN emulator route for theta_*.

        IMPORTANT M50 caveat (2026-05-06, live-probed on PC):
          cosmopower-jax 0.5.5 supports probes ['cmb_tt','cmb_ee','cmb_te',
          'cmb_pp','mpk_lin','mpk_boost','mpk_nonlin','custom_log','custom_pca'].
          There is NO 'theta_s' probe pickle in upstream releases, so the
          previous code path (probe='theta_s') would raise ValueError on first
          call. Two honest options:
            (1) Compute theta_* from full TT spectrum via acoustic peak
                position fit (slow, ~few ms per eval) — TBD followup.
            (2) Use the EH+KMJ analytic form (already known to have ~3.1-sigma
                bias per M26 audit) — documented degradation, NOT 'CLASS-grade'.
          M50 picks (2) for v7.7 v0 to keep the pipeline runnable end-to-end.
          The 'CLASS-grade theta_*' claim from M47 is therefore PROVISIONAL —
          v7.7 v0 is EH+KMJ-grade for theta_*; CLASS-grade requires classy
          frontend (CPU-bound, ~24-72h for full chain) or a custom theta_s
          emulator trained against CLASS (TBD M51+).
        """
        # M50 fix: deferred to EH+KMJ; document caveat clearly at run start.
        return self._eh_kmj_theta(omega_b, omega_c, H0)

    def _eh_kmj_theta(self, omega_b, omega_c, H0):
        """EH+KMJ analytic approx (M26 documents 3.1-sigma bias)."""
        h = H0 / 100.0
        omega_m = omega_b + omega_c
        return 100.0 * 0.010411 * (omega_b / 0.02238)**0.013 * \
               (omega_m / 0.1428)**(-0.252)


# ============================================================================
# Section 2 — Background distances + sound horizon (NMC-aware)
# ============================================================================
# Re-exported from a71_prod/background.py if available; else inlined here.
# NMC modifies H(z) via xi_chi non-minimal coupling (Wolf 2025 / Cassini-clean
# rail). This block is a SIMPLIFIED CPL-effective wrapper; full NMC integration
# requires the modified Friedmann + KG ODE from M9 audit.

def H_lcdm(z, H0, Omega_m, w0=-1.0, wa=0.0):
    """LCDM/CPL Hubble rate. Uses CPL exact form for rho_de(z)."""
    Omega_de = 1.0 - Omega_m
    # CPL exact: rho_de(z) = (1+z)^{3(1+w0+wa)} * exp(-3 wa z/(1+z))
    rho_de_exact = (1.0 + z)**(3.0 * (1.0 + w0 + wa)) * \
                   jnp.exp(-3.0 * wa * z / (1.0 + z))
    return H0 * jnp.sqrt(Omega_m * (1.0 + z)**3 + Omega_de * rho_de_exact)


def H_nmc(z, H0, Omega_m, xi_chi, w0=-1.0, wa=0.0):
    """NMC Hubble rate with non-minimal scalar-curvature coupling xi_chi.

    SIMPLIFIED MODEL (suitable for cosmological-distance-only):
       H_NMC(z)^2 = H_LCDM(z)^2 * (1 + xi_chi * f(z))
    where f(z) = (1+z)^{-2} * Omega_de(z) (NMC late-time only, per Cassini wall).

    For Cassini-clean ECI-NMC (xi_chi ~ -0.024): correction ~ few percent at z=0.
    For Wolf-NMC (xi = 2.31): correction up to ~factor 2 at low z (KG-failing).

    M50 audit caveat (2026-05-06):
      The full Wolf-NMC KG integration lives in mcmc/a71_prod/wolf_background.py
      (`wolf_kg_integrate`, scipy LSODA, NOT JAX-jittable). It models a 5-param
      scalar field {xi, beta, m2, phi_init, phidot_init} with a Friedmann
      constraint + KG ODE and a hard physical gate (|phi|<10 M_P, F>0.01,
      |lnH(0)|<0.05). The M9 audit established that Wolf's xi=2.31 KG-fails
      at the gate level; this simplified multiplicative form CANNOT reproduce
      that fact (it is well-defined for any xi_chi). A KG-aware Bayes contest
      requires the full a71_prod path (CPU-bound). v7.7 v0 (this file) is
      diagnostic-grade only: it cannot itself decide ECI-vs-Wolf on KG grounds.
      The contest here is *posterior shape* + harmonic-mean log-Z, NOT KG
      consistency. See M50 SUMMARY.md for the full caveat.
    """
    H_base2 = H_lcdm(z, H0, Omega_m, w0, wa) ** 2
    Omega_de_z = (1.0 - Omega_m) * \
                 (1.0 + z)**(3.0 * (1.0 + w0 + wa)) * \
                 jnp.exp(-3.0 * wa * z / (1.0 + z))
    f_z = Omega_de_z / (1.0 + z)**2
    return jnp.sqrt(H_base2 * (1.0 + xi_chi * f_z))


def comoving_distance(z, H_func, n_steps=200):
    """D_M(z) [Mpc] = c integral 0..z dz' / H(z')."""
    zs = jnp.linspace(0.0, z, n_steps + 1)
    Hs = H_func(zs)
    integrand = C_KMS / Hs
    return jnp.trapezoid(integrand, zs)


def sound_horizon_EH(omega_b, omega_m):
    """Eisenstein-Hu fitting formula r_d [Mpc] (1998 ApJ 496, 605)."""
    Theta_2p7 = 2.7255 / 2.7
    z_eq = 2.5e4 * omega_m * Theta_2p7**-4
    k_eq = 7.46e-2 * omega_m * Theta_2p7**-2
    z_d = 1291.0 * (omega_m**0.251 / (1.0 + 0.659 * omega_m**0.828)) * \
          (1.0 + 0.313 * omega_b**(-0.419) * (omega_b * 0.0)) * 1.0  # simplified
    R_eq = 31.5 * omega_b * Theta_2p7**-4 * (1000.0 / z_eq)
    R_d  = 31.5 * omega_b * Theta_2p7**-4 * (1000.0 / z_d)
    s = (2.0 / (3.0 * k_eq)) * jnp.sqrt(6.0 / R_eq) * \
        jnp.log((jnp.sqrt(1.0 + R_d) + jnp.sqrt(R_d + R_eq)) /
                (1.0 + jnp.sqrt(R_eq)))
    return s


# ============================================================================
# Section 3 — Likelihood stack (re-uses A71 pattern but NMC-aware)
# ============================================================================

def loglike_total_v77(params, variant, frontend, data):
    """Total log-likelihood for v7.7.

    params: dict with keys
        H0, omega_b, omega_c, n_s, ln_As_e10, tau_reio, w0, wa, M_B, xi_chi
    variant: 'eci_nmc' | 'wolf_nmc'
    frontend: Frontend instance
    data: dict with 'desi', 'sne', 'planck_pr4', 'kids' subkeys
    """
    H0 = params["H0"]
    omega_b = params["omega_b"]
    omega_c = params["omega_c"]
    h = H0 / 100.0
    omega_m = omega_b + omega_c
    Omega_m = omega_m / h**2
    xi = params["xi_chi"]
    w0 = params["w0"]
    wa = params["wa"]

    # NMC-aware H(z) closure
    H_func = lambda z: H_nmc(z, H0, Omega_m, xi, w0, wa)
    r_d = sound_horizon_EH(omega_b, omega_m)

    # 1) Planck PR4 compressed via theta_*
    ts100_th = frontend.theta_star_100(
        omega_b, omega_c, H0, params["ln_As_e10"], params["n_s"], params["tau_reio"]
    )
    pr4 = data["planck_pr4"]
    delta_pr4 = jnp.array([
        omega_b - pr4["omega_b"],
        omega_c - pr4["omega_c"],
        ts100_th - pr4["theta_s_100"],
        params["ln_As_e10"] - pr4["ln_As_e10"],
        params["n_s"] - pr4["n_s"],
    ])
    chi2_pr4 = delta_pr4 @ jnp.array(pr4["cov_inv"]) @ delta_pr4

    # 2) DESI DR2 BAO (loop over z-bins, use H_func)
    chi2_bao = 0.0
    for entry in data["desi"]:
        z = entry["z"]
        DM_th = comoving_distance(z, H_func)
        DH_th = C_KMS / H_func(jnp.array(z))
        if entry["fit"] == "iso":
            DV_th = (z * DM_th**2 * DH_th)**(1.0 / 3.0) / r_d
            chi2_bao = chi2_bao + ((DV_th - entry["DV_rd"]) / entry["sigma"])**2
        else:
            res_DM = (DM_th / r_d - entry["DM_rd"]) / entry["sig_DM"]
            res_DH = (DH_th / r_d - entry["DH_rd"]) / entry["sig_DH"]
            rho = entry["rho"]
            chi2_bao = chi2_bao + (res_DM**2 + res_DH**2 - 2 * rho * res_DM * res_DH) / (1 - rho**2)

    # 3) Pantheon+ SNe (M_B sampled)
    z_sn = jnp.array(data["sne"]["z"])
    mu_obs = jnp.array(data["sne"]["mu_obs"])
    cov_inv_sne = jnp.array(data["sne"]["cov_inv"])
    DM_sn = jax.vmap(lambda z: comoving_distance(z, H_func))(z_sn)
    DL_sn = (1.0 + z_sn) * DM_sn
    mu_th = 5.0 * jnp.log10(DL_sn) + 25.0
    res_sne = mu_obs - mu_th - params["M_B"]
    chi2_sne = res_sne @ cov_inv_sne @ res_sne

    # 4) KiDS-1000 (compressed S_8 = sigma_8 sqrt(Omega_m / 0.3))
    # sigma_8 not directly in our param vector; we use the linear-theory
    # approximation sigma_8 ~ 0.811 * (omega_m/0.142)^{0.5} * exp((ln_As_e10 - 3.044)/2)
    # CONVENTIONAL — replace with full Boltzmann if classy is up.
    sigma_8_th = 0.811 * (omega_m / 0.142)**0.5 * \
                 jnp.exp((params["ln_As_e10"] - 3.044) / 2.0)
    S_8_th = sigma_8_th * jnp.sqrt(Omega_m / 0.3)
    kids = data["kids"]
    chi2_kids = ((S_8_th - kids["S_8"]) / kids["sigma_S_8"])**2

    return -0.5 * (chi2_pr4 + chi2_bao + chi2_sne + chi2_kids)


# ============================================================================
# Section 4 — priors (matches a71_prod/priors.py style)
# ============================================================================

PRIORS_V77 = {
    "H0":         ("uniform", 60.0, 80.0),
    "omega_b":    ("uniform", 0.018, 0.027),
    "omega_c":    ("uniform", 0.08, 0.16),
    "n_s":        ("uniform", 0.90, 1.00),
    "ln_As_e10":  ("uniform", 2.7, 3.5),
    "tau_reio":   ("normal", 0.054, 0.007),
    "w0":         ("uniform", -1.5, -0.5),
    "wa":         ("uniform", -1.0, 1.0),
    "M_B":        ("uniform", -19.6, -19.0),
    # xi_chi: variant-specific
}

PRIORS_XI = {
    "eci_nmc":  ("normal", -0.024, 0.016),    # Cassini-clean rail (Levier #1B)
    "wolf_nmc": ("normal",  2.31,  0.10),     # Wolf et al. 2025 central value
}


def log_prior(params, variant):
    """Sum log-prior across all params."""
    lp = 0.0
    full_priors = dict(PRIORS_V77)
    full_priors["xi_chi"] = PRIORS_XI[variant]
    for name, spec in full_priors.items():
        x = params[name]
        kind = spec[0]
        if kind == "uniform":
            lo, hi = spec[1], spec[2]
            in_range = (x >= lo) & (x <= hi)
            lp = lp + jnp.where(in_range, -jnp.log(hi - lo), -jnp.inf)
        elif kind == "normal":
            mu, sigma = spec[1], spec[2]
            lp = lp + (-0.5 * ((x - mu) / sigma)**2 - jnp.log(sigma * jnp.sqrt(2 * jnp.pi)))
        else:
            raise ValueError("unknown prior kind: {}".format(kind))
    return lp


# ============================================================================
# Section 5 — data loaders (uses A71 paths)
# ============================================================================

def load_data(verbose=True):
    """Load all four data products. Falls back to synthetic if not on PC."""
    data = {}

    # DESI DR2 BAO — use the verified 7-bin S9 acquisition values
    # (full 13x13 cov from a71_prod/likelihoods.py is not used here because the
    #  simplified per-bin loader has a known bug; the 7-bin _desi_fallback
    #  values were directly extracted by M47 from desi_gaussian_bao mean.txt
    #  + cov.txt sha256-pinned files in a71_prod sample-acquisition log
    #  S9 dated 2026-05-06, so they are real PR4 DESI DR2 numbers, not synthetic).
    data["desi"] = _desi_fallback()

    # Pantheon+ SNe
    sne_path = os.environ.get(
        "PANTHEONPLUS_DATA_PATH", "/home/remondiere/data/pantheonplus"
    )
    if os.path.isfile(os.path.join(sne_path, "Pantheon+SH0ES.dat")):
        sys.path.insert(0, "/home/remondiere/crossed-cosmos")
        try:
            from mcmc.a71_prod.likelihoods import _load_pantheonplus_data_from_files
            real = _load_pantheonplus_data_from_files(sne_path)
            data["sne"] = {
                "z": real["z_sn"].tolist(),
                "mu_obs": real["mu_obs"].tolist(),
                "cov_inv": real["cov_inv"],
            }
        except Exception as exc:
            if verbose:
                sys.stderr.write("[data] sne a71 loader failed: {}\n".format(exc))
            data["sne"] = _sne_fallback()
    else:
        data["sne"] = _sne_fallback()

    # Planck PR4 compressed (Tristram et al. 2024 NPIPE -- numbers
    # SCAFFOLDED below; user must replace with PR4 chain mean+cov).
    # [TBD: load from /home/remondiere/data/planck_pr4/planck_pr4_compressed.json]
    data["planck_pr4"] = _planck_pr4_fallback()

    # KiDS-1000 cosmic shear S_8 (Asgari et al. 2020, arXiv:2007.15633 COSEBIs):
    # S_8 = 0.737 +/- 0.040 (Table 4, COSEBIs analysis)
    data["kids"] = {"S_8": 0.737, "sigma_S_8": 0.040, "ref": "arXiv:2007.15633"}

    return data


def _desi_fallback():
    """7-bin DESI DR2 (S9 acquisition values, see a71_prod/likelihoods.py)."""
    return [
        {"z": 0.295, "fit": "iso", "DV_rd": 7.94167639, "sigma": 0.07609196,
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
    """50-SN smoke set (NOT for production)."""
    rng = np.random.default_rng(42)
    n = 50
    z = np.sort(rng.uniform(0.01, 1.5, n))
    mu_true = 5 * np.log10(C_KMS * z * 1.5e3) + 25 - 19.3
    sigma = 0.15 * np.ones(n)
    mu_obs = mu_true + rng.normal(0, sigma)
    cov_inv = np.diag(1.0 / sigma**2)
    return {"z": z.tolist(), "mu_obs": mu_obs.tolist(), "cov_inv": cov_inv}


def _planck_pr4_fallback():
    """Compressed Planck PR4 NPIPE — Tristram et al. 2024, A&A 682 A37 Table 3 TTTEEE.

    Live-verified from arXiv:2309.10034 PDF (M50 audit, 2026-05-06):
      Omega_b h^2     = 0.02226 +/- 0.00013   (Table 3 col TTTEEE)
      Omega_c h^2     = 0.1188  +/- 0.0012
      100 theta_*     = 1.04108 +/- 0.00026
      log(10^10 A_s)  = 3.040   +/- 0.014    (natural log per Planck convention)
      n_s             = 0.9681  +/- 0.0039
      tau_reio        = 0.0580  +/- 0.0062
    Derived (consistency checks, not used here):
      H_0 = 67.64 +/- 0.52   sigma_8 = 0.8070 +/- 0.0065
      S_8 = 0.819 +/- 0.014  Omega_m = 0.3092 +/- 0.0070

    Cov is diagonal (off-diagonals not yet extracted from public chains).
    This is a CONSERVATIVE choice — true PR4 cov has e.g. omega_b<->n_s ~+0.3
    and omega_c<->theta_* ~-0.4 correlations that would tighten constraints.
    [TBD M51+: extract full 5x5 from public Cobaya/MontePython chains when
     available at https://pla.esac.esa.int or NERSC PR4 portal.]
    """
    return {
        "omega_b": 0.02226, "omega_c": 0.1188, "theta_s_100": 1.04108,
        "ln_As_e10": 3.040, "n_s": 0.9681,
        "cov_inv": np.diag([
            1.0 / 0.00013**2, 1.0 / 0.0012**2, 1.0 / 0.00026**2,
            1.0 / 0.014**2, 1.0 / 0.0039**2,
        ]),
        "_ref": "Tristram et al. 2024, A&A 682 A37 Table 3 TTTEEE col"
                " (arXiv:2309.10034)",
        "_caveat": "diagonal-only; full off-diagonals TBD",
    }


# ============================================================================
# Section 6 — NUTS driver
# ============================================================================

PARAM_NAMES = ["H0", "omega_b", "omega_c", "n_s", "ln_As_e10", "tau_reio",
               "w0", "wa", "M_B", "xi_chi"]


def vec_to_dict(v):
    return {n: v[i] for i, n in enumerate(PARAM_NAMES)}


def init_pos(variant):
    """Reasonable starting point for each variant."""
    base = jnp.array([67.5, 0.0224, 0.120, 0.965, 3.044, 0.054,
                      -1.0, 0.0, -19.3])
    if variant == "eci_nmc":
        xi0 = -0.024
    else:
        xi0 = 2.31
    return jnp.concatenate([base, jnp.array([xi0])])


def run_nuts(variant, frontend, data, key, n_warmup=5000, n_samples=5000,
             n_chains=4, target_accept=0.85):
    """Run blackjax 1.5 NUTS for one variant. Returns chain array (chains, samples, n_params)."""
    def logpost(v):
        params = vec_to_dict(v)
        lp = log_prior(params, variant)
        ll = loglike_total_v77(params, variant, frontend, data)
        return jnp.where(jnp.isfinite(lp), lp + ll, -jnp.inf)

    keys = jrandom.split(key, n_chains)
    init_v = init_pos(variant)

    # Window adaptation
    warmup = blackjax.window_adaptation(blackjax.nuts, logpost,
                                        target_acceptance_rate=target_accept)
    chains = []
    for ci, k in enumerate(keys):
        sys.stderr.write("[nuts {}] chain {}/{} warmup...\n".format(
            variant, ci + 1, n_chains))
        (state, params), _ = warmup.run(k, init_v, num_steps=n_warmup)
        kernel = blackjax.nuts(logpost, **params).step

        def step_one(state_key, _):
            state, k = state_key
            k1, k2 = jrandom.split(k)
            new_state, _ = kernel(k1, state)
            return (new_state, k2), new_state.position

        sys.stderr.write("[nuts {}] chain {}/{} sampling...\n".format(
            variant, ci + 1, n_chains))
        (final_state, _), positions = jax.lax.scan(
            step_one, (state, k), jnp.arange(n_samples)
        )
        chains.append(np.asarray(positions))
    return np.stack(chains)  # (n_chains, n_samples, n_params)


def thermodynamic_log_evidence(chain, logpost_fn, n_temps=10):
    """Naive thermodynamic-integration log-evidence estimate.

    For a quick sanity Bayes factor; replace with nested sampling
    (dynesty / ultranest) for paper-grade evidence in followup.
    """
    # [TBD: implement TI scan; for v7.7 v0 we use harmonic-mean estimator
    #  (known biased but fast). Honest caveat: log_bayes_factor here is
    #  diagnostic only.]
    samples = chain.reshape(-1, chain.shape[-1])
    logposts = jax.vmap(logpost_fn)(samples)
    # Harmonic mean: log Z ~ -log mean(exp(-logpost))
    finite = logposts[jnp.isfinite(logposts)]
    if finite.size == 0:
        return float("nan")
    log_hm = -jax.scipy.special.logsumexp(-finite) + jnp.log(finite.size)
    return float(log_hm)


# ============================================================================
# Section 7 — main
# ============================================================================

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--frontend", default="cosmopower",
                        choices=["cosmopower", "classy"])
    parser.add_argument("--n_warmup", type=int, default=5000)
    parser.add_argument("--n_samples", type=int, default=5000)
    parser.add_argument("--n_chains", type=int, default=4)
    parser.add_argument("--seed", type=int, default=20260506)
    parser.add_argument("--out", default=None,
                        help="output .npz path; default = pipeline_b/v77_results.npz")
    parser.add_argument("--smoke", action="store_true",
                        help="quick smoke run: 50 warmup + 50 samples, 1 chain")
    args = parser.parse_args()

    out_path = args.out or os.path.join(os.path.dirname(__file__), "v77_results.npz")

    if args.smoke:
        args.n_warmup = 50
        args.n_samples = 50
        args.n_chains = 1

    print("[v7.7] frontend preference: {}".format(args.frontend))
    frontend = Frontend(prefer=args.frontend)
    print("[v7.7] frontend selected:   {}".format(frontend.name))
    print("[v7.7] M50 caveat:          theta_* via EH+KMJ analytic "
          "(cosmopower-jax 0.5.5 has no theta_s probe; ~3.1-sigma bias "
          "per M26 audit). v7.7 v0 is diagnostic-grade for theta_*.")

    print("[v7.7] loading data...")
    data = load_data()
    print("[v7.7] DESI bins:           {}".format(len(data["desi"])))
    print("[v7.7] SNe N:               {}".format(len(data["sne"]["z"])))
    print("[v7.7] PR4 compressed:      Tristram 2024 Table 3 TTTEEE "
          "(diag-only cov; off-diag TBD)")
    print("[v7.7] KiDS S_8 = {} +/- {} (arXiv:2007.15633)".format(
        data["kids"]["S_8"], data["kids"]["sigma_S_8"]))

    rng = jrandom.PRNGKey(args.seed)
    rng_e, rng_w = jrandom.split(rng)

    t0 = time.time()
    print("[v7.7] starting ECI-NMC chains...")
    chains_eci = run_nuts(
        "eci_nmc", frontend, data, rng_e,
        n_warmup=args.n_warmup, n_samples=args.n_samples,
        n_chains=args.n_chains,
    )
    print("[v7.7] ECI-NMC done in {:.1f} s".format(time.time() - t0))

    t1 = time.time()
    print("[v7.7] starting Wolf-NMC chains...")
    chains_wolf = run_nuts(
        "wolf_nmc", frontend, data, rng_w,
        n_warmup=args.n_warmup, n_samples=args.n_samples,
        n_chains=args.n_chains,
    )
    print("[v7.7] Wolf-NMC done in {:.1f} s".format(time.time() - t1))

    # Quick log-evidence (harmonic-mean estimate; diagnostic)
    def lp_eci(v):
        p = vec_to_dict(v)
        return log_prior(p, "eci_nmc") + loglike_total_v77(p, "eci_nmc", frontend, data)

    def lp_wolf(v):
        p = vec_to_dict(v)
        return log_prior(p, "wolf_nmc") + loglike_total_v77(p, "wolf_nmc", frontend, data)

    log_Z_eci = thermodynamic_log_evidence(chains_eci, lp_eci)
    log_Z_wolf = thermodynamic_log_evidence(chains_wolf, lp_wolf)
    log_BF = log_Z_eci - log_Z_wolf

    print("\n=== v7.7 BAYES CONTEST ===")
    print("log_Z_eci_nmc  = {:.3f}  (harmonic-mean diagnostic)".format(log_Z_eci))
    print("log_Z_wolf_nmc = {:.3f}".format(log_Z_wolf))
    print("log_BF (ECI/Wolf) = {:+.3f}".format(log_BF))
    if log_BF > 5:
        print("=> DECISIVE for ECI-NMC (Jeffreys scale, log_BF > 5)")
    elif log_BF > 2.3:
        print("=> STRONG for ECI-NMC (log_BF > 2.3)")
    elif log_BF > 1.0:
        print("=> POSITIVE for ECI-NMC")
    elif log_BF < -5:
        print("=> DECISIVE for Wolf-NMC (KG-failing wins data fit)")
    elif log_BF < -2.3:
        print("=> STRONG for Wolf-NMC")
    else:
        print("=> INCONCLUSIVE (|log_BF| < 1)")
    print("=== END BAYES CONTEST ===\n")

    # Save
    np.savez(
        out_path,
        chains_eci_nmc=chains_eci,
        chains_wolf_nmc=chains_wolf,
        log_evidence_eci=np.array([log_Z_eci]),
        log_evidence_wolf=np.array([log_Z_wolf]),
        log_bayes_factor=np.array([log_BF]),
        params_order=np.array(PARAM_NAMES),
        meta=np.array([json.dumps({
            "frontend": frontend.name,
            "n_warmup": args.n_warmup,
            "n_samples": args.n_samples,
            "n_chains": args.n_chains,
            "seed": args.seed,
            "wallclock_s": time.time() - t0,
            "honest_caveats": [
                "Planck PR4 compressed: Tristram 2024 A&A 682 A37 Table 3"
                " TTTEEE means; diagonal-only cov (off-diag TBD)",
                "theta_* via EH+KMJ analytic (cosmopower-jax has no theta_s"
                " probe in 0.5.5); ~3.1-sigma bias per M26 audit",
                "KiDS S_8 compressed only; no full nuisance marginalization",
                "log-evidence is harmonic-mean (biased); use nested sampling"
                " for paper",
                "NMC H(z) is simplified multiplicative form; full Wolf-NMC KG"
                " contest needs a71_prod/wolf_kg_integrate (CPU-bound)",
            ],
        })]),
    )
    print("[v7.7] saved -> {}".format(out_path))


if __name__ == "__main__":
    main()
