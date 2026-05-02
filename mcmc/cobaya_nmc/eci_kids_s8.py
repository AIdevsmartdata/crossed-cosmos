"""
ECIKiDSS8Likelihood — Cobaya external likelihood for Levier #1.

Implements three independent contributions to log P:

1. KiDS-1000 3x2pt S8 Gaussian prior
   S_8 = sigma8 * (Omega_m / 0.3)^0.5 = 0.766 +/- 0.020
   Source: Asgari et al. 2021, A&A 645, A104 (KiDS-1000 3x2pt combined)

2. Cassini hard wall on xi_chi (optional, enabled by default)
   |xi_chi| * (chi0 / M_P)^2 < 6e-6
   Source: Bertotti, Iess & Tortora 2003, Nature 425, 374
   (Solar-system Shapiro delay; GR confirmed at 2e-5 level)
   chi0/M_P is a fixed fiducial, not sampled. Default: chi0 = M_P/10.

3. ACT DR6 N_eff diagnostic on c'_DD (optional, enabled by default)
   If c'_DD > 0.18: Gaussian penalty centred at 0.18, sigma = 0.01.
   This is a quadratic regulariser, not a hard cut, consistent with the
   Levier #1 spec in notes/calculation_triage_2026_05_02.md §A1.
   The 0.18 threshold approximates the ACT DR6 3-sigma boundary on
   Delta N_eff from additional relativistic species (Madhavacheril et al. 2024).

LIMITATIONS:
  - The KiDS S8 prior is a Gaussian approximation to the full 3x2pt posterior.
    The actual KiDS-1000 likelihood is publicly available via CosmoSIS/Monte Python;
    this approximation is appropriate for a first-pass joint MCMC.
  - The Cassini wall uses chi0 = M_P/10 as a fixed fiducial. For a proper
    treatment, chi0 should be a derived quantity from the NMC sector background
    integration. This requires reading chi_of_a from ECINMCTheory state at a=1.
    Upgrade path: set use_derived_chi0=true and read chi0 from provider.
  - The ACT DR6 penalty is phenomenological. The full calculation requires
    the N2 Boltzmann freeze-in (see notes/calculation_triage_2026_05_02.md §A4).
"""

from __future__ import annotations

import numpy as np

from cobaya.likelihood import Likelihood


class ECIKiDSS8Likelihood(Likelihood):
    """KiDS-1000 S8 prior + Cassini hard wall + ACT DR6 c'_DD diagnostic."""

    # Configurable parameters (set in YAML likelihood block)
    kids_s8_mean: float = 0.766
    kids_s8_sigma: float = 0.020

    apply_cassini_wall: bool = True
    chi0_over_MP: float = 0.1     # chi0 / M_P (dimensionless, M_P = 1 units)
    cassini_limit: float = 6.0e-6  # |xi_chi| * (chi0/M_P)^2 < this value

    apply_act_penalty: bool = True
    act_cdd_threshold: float = 0.18
    act_penalty_sigma: float = 0.01

    def initialize(self):
        """Precompute fixed quantities; log configuration at startup."""
        self.log.info(
            "ECIKiDSS8Likelihood: KiDS-1000 S8 = %.3f +/- %.3f",
            self.kids_s8_mean,
            self.kids_s8_sigma,
        )
        if self.apply_cassini_wall:
            self.log.info(
                "Cassini hard wall active: |xi_chi| * (%.2f)^2 < %.2e",
                self.chi0_over_MP,
                self.cassini_limit,
            )
        if self.apply_act_penalty:
            self.log.info(
                "ACT DR6 c'_DD penalty active: threshold = %.2f, sigma = %.3f",
                self.act_cdd_threshold,
                self.act_penalty_sigma,
            )

    def get_requirements(self):
        """Declare which theory quantities and parameters we need."""
        reqs = {
            "sigma8": None,
            "Omega_m": None,
        }
        return reqs

    def logp(self, **params_values):
        """Compute log P = log P_KiDS + log P_Cassini + log P_ACT."""
        logp_total = 0.0

        # ------------------------------------------------------------------
        # 1. KiDS-1000 S8 prior
        # ------------------------------------------------------------------
        sigma8 = self.provider.get_param("sigma8")
        Omega_m = self.provider.get_param("Omega_m")
        S8 = sigma8 * (Omega_m / 0.3) ** 0.5
        delta_s8 = (S8 - self.kids_s8_mean) / self.kids_s8_sigma
        logp_kids = -0.5 * delta_s8 ** 2
        logp_total += logp_kids

        # ------------------------------------------------------------------
        # 2. Cassini hard wall on xi_chi
        # ------------------------------------------------------------------
        if self.apply_cassini_wall:
            xi_chi = params_values.get("xi_chi", 0.0)
            cassini_test = abs(xi_chi) * self.chi0_over_MP ** 2
            if cassini_test >= self.cassini_limit:
                # Return -inf: this point is excluded by Cassini
                return -np.inf

        # ------------------------------------------------------------------
        # 3. ACT DR6 N_eff diagnostic on c'_DD
        # ------------------------------------------------------------------
        if self.apply_act_penalty:
            c_prime_DD = params_values.get("c_prime_DD", 0.0)
            if c_prime_DD > self.act_cdd_threshold:
                excess = (c_prime_DD - self.act_cdd_threshold) / self.act_penalty_sigma
                logp_act = -0.5 * excess ** 2
                logp_total += logp_act

        return logp_total
