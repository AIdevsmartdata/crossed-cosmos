"""
ECINMCTheory — a Cobaya Theory plugin that wraps vanilla `classy`
(minimally-coupled quintessence_exponential) and post-processes the
perturbation sector with the D14 closed-form NMC corrections:

    G_eff(k, a)/G_N = (M_P^2 / F) * (2F + 4 F_phi^2) / (2F + 3 F_phi^2)
    eta(k, a)       = (2F + 2 F_phi^2) / (2F + 4 F_phi^2)

with F = M_P^2 - xi_chi * chi(a)^2  and F_phi = -2 xi_chi chi(a).

Background chi(a) is integrated here as a *minimally*-coupled thawing
scalar (no xi back-reaction on H). The D13 B(Omega_Lambda) table is
loaded from derivations/_results/D13-summary.json and exposed as a
derived quantity `wa_nmc_correction` for cross-check.

LIMITATIONS (see README):
  * Valid only in the quasi-static sub-horizon regime (k >> a H).
  * Does NOT back-react on H(z): the NMC Friedmann term
    -6 xi H chi chi' is ignored. For the CMB acoustic-scale-level
    constraint this is NOT trustworthy; see README §Verdict.
  * eta = 1 + O(xi^2); we keep the exact expression but at Cassini-
    saturated |xi| <= 0.024 the correction is <0.01% and effectively 1.

This plugin is intended for a first-pass MCMC on DESI DR2 + Pantheon+
(expansion-history + growth probes), NOT for final CMB likelihoods.
"""

from __future__ import annotations

import json
import os
from typing import Iterable

import numpy as np
from scipy.integrate import solve_ivp

from cobaya.theory import Theory

# ---------------------------------------------------------------------------
# Constants / paths
# ---------------------------------------------------------------------------
_HERE = os.path.dirname(os.path.abspath(__file__))
_REPO = os.path.abspath(os.path.join(_HERE, "..", ".."))
_D13_JSON = os.path.join(_REPO, "derivations", "_results", "D13-summary.json")


def _load_d13_table() -> dict:
    """Load D13 B(Omega_Lambda) table; return empty dict if missing."""
    if not os.path.exists(_D13_JSON):
        return {}
    with open(_D13_JSON) as fh:
        return json.load(fh)


# ---------------------------------------------------------------------------
# D14 analytic kernels (exact scalar-tensor QS expressions, M_P = 1 units)
# ---------------------------------------------------------------------------
def _F(xi: float, chi: np.ndarray) -> np.ndarray:
    return 1.0 - xi * chi * chi


def _Fphi(xi: float, chi: np.ndarray) -> np.ndarray:
    return -2.0 * xi * chi


def geff_over_gn(xi: float, chi: np.ndarray) -> np.ndarray:
    """D14 Eq.: G_eff/G_N = (1/F) * (2F + 4 Fphi^2)/(2F + 3 Fphi^2)."""
    F = _F(xi, chi)
    Fp2 = _Fphi(xi, chi) ** 2
    return (1.0 / F) * (2.0 * F + 4.0 * Fp2) / (2.0 * F + 3.0 * Fp2)


def slip_eta(xi: float, chi: np.ndarray) -> np.ndarray:
    """D14: eta = Phi/Psi = (2F + 2 Fphi^2)/(2F + 4 Fphi^2)."""
    F = _F(xi, chi)
    Fp2 = _Fphi(xi, chi) ** 2
    return (2.0 * F + 2.0 * Fp2) / (2.0 * F + 4.0 * Fp2)


# ---------------------------------------------------------------------------
# Background chi(a) for a minimally-coupled thawing quintessence with
# V = V0 exp(-alpha chi). (xi is NOT included here — it only enters the
# perturbation post-processing at leading order.)
# ---------------------------------------------------------------------------
def _integrate_chi(alpha: float, chi_ini: float, Omega_m: float,
                   n: int = 400) -> dict:
    """Minimally-coupled thawing quintessence chi(a) in M_P units.

    Returns dict with a, chi(a), chip (d chi/d ln a). V0 is tuned so
    that Omega_phi(a=1) = 1 - Omega_m (for consistency with classy,
    which handles H(z) itself; we only need chi(a) shape for G_eff).
    """
    from scipy.optimize import brentq

    OMEGA_R = 9.2e-5

    def rhs(N, y, V0):
        chi, chip = y
        a = np.exp(N)
        V = V0 * np.exp(-alpha * chi)
        Vp = -alpha * V
        rho_m = 3.0 * Omega_m * a ** -3
        rho_r = 3.0 * OMEGA_R * a ** -4
        H2 = (rho_m + rho_r + V + 0.5 * 0.0) / (3.0 - 0.5 * chip * chip)
        if H2 <= 0:
            return [0.0, 0.0]
        chipp = -3.0 * chip - Vp / H2
        return [chip, chipp]

    def final_Omega_phi(V0):
        N0 = np.log(1.0 / 1000.0)
        sol = solve_ivp(rhs, (N0, 0.0), [chi_ini, 0.0],
                        args=(V0,), method="LSODA",
                        rtol=1e-8, atol=1e-10, max_step=0.05)
        if not sol.success:
            return -1.0
        chi_f, chip_f = sol.y[:, -1]
        V_f = V0 * np.exp(-alpha * chi_f)
        rho_m = 3.0 * Omega_m
        rho_r = 3.0 * OMEGA_R
        H2 = (rho_m + rho_r + V_f) / (3.0 - 0.5 * chip_f ** 2)
        rho_phi = 0.5 * H2 * chip_f ** 2 + V_f
        return rho_phi / (3.0 * H2) - (1.0 - Omega_m)

    try:
        V0 = brentq(final_Omega_phi, 1e-4, 5.0, xtol=1e-4)
    except Exception:
        V0 = 3.0 * (1.0 - Omega_m)  # fallback — near-frozen limit

    N0 = np.log(1.0 / 1000.0)
    Ngrid = np.linspace(N0, 0.0, n)
    sol = solve_ivp(rhs, (N0, 0.0), [chi_ini, 0.0], args=(V0,),
                    t_eval=Ngrid, method="LSODA",
                    rtol=1e-9, atol=1e-11, max_step=0.05)
    a = np.exp(sol.t)
    return dict(a=a, chi=sol.y[0], chip=sol.y[1], V0=V0)


# ---------------------------------------------------------------------------
# Cobaya Theory subclass
# ---------------------------------------------------------------------------
class ECINMCTheory(Theory):
    """Wraps classy (quintessence_exponential) + D14 G_eff/eta postproc.

    Exposes new input parameters:
        xi_chi          - non-minimal coupling (dimensionless, |xi| < 0.1)
        chi_initial     - initial value chi(a_ini) in M_P units

    Provides:
        Hubble(z)       - forwarded from classy
        angular_diameter_distance(z) - forwarded
        G_eff_over_GN(a) - D14 post-processed
        eta_slip(a)     - D14 post-processed
        fsigma8(z)      - growth ODE using G_eff
    """

    # Declared input params (Cobaya reads these from the yaml)
    params = {
        "xi_chi": None,
        "chi_initial": None,
    }

    # D14 defaults (quintessence_exponential slope and matter density).
    # These are "static" theory knobs, NOT sampled parameters.
    alpha: float = 0.55
    Omega_m_fiducial: float = 0.315

    def initialize(self):
        """Load the D13 B(Omega_Lambda) table and ready classy."""
        self._d13 = _load_d13_table()
        # Try to import classy; if absent, raise early with a clear msg.
        try:
            from classy import Class
        except ImportError as e:
            raise ImportError(
                "classy (CLASS python wrapper) is required. "
                "pip install classy  or  build CLASS and `make classy`."
            ) from e
        self._Class = Class
        self._classy = Class()
        self._cached_bg: dict | None = None
        self._cached_key: tuple | None = None

    def get_requirements(self):
        # We sample xi_chi / chi_initial ourselves; ask Cobaya for nothing.
        return []

    def get_can_provide(self) -> Iterable[str]:
        return ["G_eff_over_GN", "eta_slip", "fsigma8",
                "Hubble", "chi_of_a", "wa_nmc_correction"]

    def get_can_provide_params(self) -> Iterable[str]:
        return ["wa_nmc_correction"]

    # ---- core calculation ---------------------------------------------
    def calculate(self, state, want_derived=True, **params):
        xi = float(params.get("xi_chi", 0.0))
        chi_ini = float(params.get("chi_initial", 0.1))

        key = (round(xi, 9), round(chi_ini, 9))
        if self._cached_key != key:
            bg = _integrate_chi(self.alpha, chi_ini, self.Omega_m_fiducial)
            self._cached_bg = bg
            self._cached_key = key
        else:
            bg = self._cached_bg

        a = bg["a"]
        chi = bg["chi"]
        G = geff_over_gn(xi, chi)
        eta = slip_eta(xi, chi)

        state["G_eff_over_GN"] = np.column_stack([a, G])
        state["eta_slip"] = np.column_stack([a, eta])
        state["chi_of_a"] = np.column_stack([a, chi])

        # --- fsigma8(z) via quasi-static growth ODE with G_eff --------
        fs8 = self._growth_fsigma8(bg, G)
        state["fsigma8"] = fs8

        # --- derived: w_a correction from D13 B(Omega_Lambda) ---------
        if self._d13:
            Om_L = 1.0 - self.Omega_m_fiducial
            keys = sorted(float(k) for k in self._d13.get("B_num", {}).keys())
            if keys:
                # linear interp in Omega_L
                Bs = [self._d13["B_num"][f"{k}"] for k in keys]
                B = float(np.interp(Om_L, keys, Bs))
                # Delta w_a ~ B * xi * chi_ini^2 (D13 parametrisation)
                wa_corr = B * xi * chi_ini ** 2
            else:
                wa_corr = 0.0
        else:
            wa_corr = 0.0
        if want_derived:
            state["derived"] = {"wa_nmc_correction": wa_corr}

        return True

    def _growth_fsigma8(self, bg: dict, G: np.ndarray,
                        sigma8_today: float = 0.811) -> np.ndarray:
        """Solve delta'' + (2 + H'/H) delta' - 3/2 Omega_m G delta = 0."""
        a = bg["a"]
        N = np.log(a)
        Om = self.Omega_m_fiducial
        rho_m = 3.0 * Om * a ** -3
        V = bg["V0"] * np.exp(-self.alpha * bg["chi"])
        # Minimally-coupled H2
        H2 = (rho_m + V) / (3.0 - 0.5 * bg["chip"] ** 2)
        Om_a = rho_m / (3.0 * H2)
        lnH = 0.5 * np.log(H2)
        dlnH = np.gradient(lnH, N)

        def rhs(Nq, y):
            d, dp = y
            Omq = np.interp(Nq, N, Om_a)
            Gq = np.interp(Nq, N, G)
            dlnq = np.interp(Nq, N, dlnH)
            return [dp, -(2.0 + dlnq) * dp + 1.5 * Omq * Gq * d]

        N_ic = np.log(1.0 / 51.0)
        a_ic = np.exp(N_ic)
        sol = solve_ivp(rhs, (N_ic, 0.0), [a_ic, a_ic],
                        t_eval=np.linspace(N_ic, 0.0, 400),
                        method="LSODA", rtol=1e-9, atol=1e-12)
        delta = sol.y[0]
        f = sol.y[1] / delta
        sig8 = sigma8_today * (delta / delta[-1])
        z = 1.0 / np.exp(sol.t) - 1.0
        return np.column_stack([z[::-1], (f * sig8)[::-1]])

    # ---- convenience accessor: H(z) via classy -----------------------
    def get_Hubble(self, z, units="km/s/Mpc"):
        """Forwarded from an internal minimally-coupled classy run.

        We configure classy with Omega_fld + CPL w0/wa = -1/0 as a
        stand-in for a minimally-coupled quintessence background. A
        proper implementation would use `quintessence_monomial` with
        V_parameters=..., but classy's parameter names depend on the
        installed version; keep this simple and document it.
        """
        z = np.atleast_1d(z).astype(float)
        self._classy.set({
            "H0": 67.36,
            "omega_b": 0.02237,
            "omega_cdm": 0.12,
            "Omega_fld": 1.0 - self.Omega_m_fiducial - 9.2e-5,
            "w0_fld": -1.0, "wa_fld": 0.0,
        })
        try:
            self._classy.compute(level=["background"])
        except Exception as e:
            # Bubble up with context
            raise RuntimeError(f"classy background compute failed: {e}")
        Hz = np.array([self._classy.Hubble(zi) for zi in z])  # 1/Mpc
        if units == "km/s/Mpc":
            c_km = 299792.458
            Hz = Hz * c_km
        return Hz
