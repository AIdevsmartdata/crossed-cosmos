"""
A64 — Wolf-vs-ECI dual-branch Bayes contest: likelihood specification skeleton.

STATUS: SPEC ONLY. Not executable as-is. References A25 NMC backend
(/root/crossed-cosmos/notes/eci_v7_aspiration/A25_NMC_JAX_ADAPTER/nmc_kg_backend_jax.py)
which provides the cosmopower-jax-compatible custom_log emulators for log10 H(z)
and rescaled w(z) on the |xi|<0.10 grid. A56 will retrain to |xi|<10 to unlock
the ECI-V branch. J(chi)X^2 Galileon kinetic term backend is NOT YET WRITTEN.

Pre-registered hypotheses (see bayes_contest_design.md sec. 5):
  H0: log B(ECI-main vs ECI-V) > +1  -> Cassini-clean wedge wins
  H1: log B(ECI-V vs ECI-main) > +1  -> Wolf large-xi recovered
  H2: log B in [-1, +1]              -> tie

Refs (live-verified 2026-05-05 via arXiv):
  Wolf et al. 2025, arXiv:2504.07679, PRL 135, 081001 (log B = 7.34 +/- 0.6 vs LCDM)
  Karam, Sanchez Lopez, Terente Diaz 2026, arXiv:2604.16226 (PPN constraints)

DISCIPLINE: hallu 85, no fabrication. Do not invent dataset paths or emulator
file names that have not been confirmed on disk. Placeholder names are explicitly
marked TODO_PATH.
"""

from __future__ import annotations

# --- Imports (target stack; not executed in this spec) ---
# import jax
# import jax.numpy as jnp
# import numpyro
# import numpyro.distributions as dist
# from numpyro.infer import NUTS, MCMC
# from cosmopower_jax.cosmopower_jax import CPJ
# # from a25 nmc kg backend (already exists):
# # from notes.eci_v7_aspiration.A25_NMC_JAX_ADAPTER.nmc_kg_backend_jax import ...

# =========================================================================
# Section 1 -- Cosmological & NMC parameter priors
# =========================================================================

# Shared LCDM-like base (both branches)
PRIORS_BASE = {
    "H0":   ("Uniform", 50.0, 90.0),       # km/s/Mpc
    "ombh2":("Uniform", 0.018, 0.026),
    "omch2":("Uniform", 0.08,  0.20),
    "ns":   ("Uniform", 0.90,  1.05),
    "log_A_s_e10": ("Uniform", 2.7, 3.5),  # log(10^10 A_s)
    "tau":  ("Uniform", 0.02,  0.12),
}

# NMC sector shared
PRIORS_NMC_SHARED = {
    "m_chi":  ("LogUniform", 1e-33, 1e-30),  # eV; ultra-light scalar
    "chi0_over_MP": ("Uniform", 1e-4, 5e-2), # explicit, NOT buried in derived bound
}

# ECI-main branch -- HARD Cassini cutoff
# Justification: |xi_chi| * (chi0/M_P)^2 <~ 6e-6
# At chi0/M_P ~ 0.016 the linear bound is |xi_chi| <~ 0.024.
# We adopt |xi_chi| < 0.024 as a hard prior wall.
PRIORS_ECI_MAIN = {
    **PRIORS_BASE,
    **PRIORS_NMC_SHARED,
    "xi_chi": ("Uniform", -0.024, +0.024),   # hard Cassini wall
}

# ECI-V branch -- smooth super-Gaussian on [-5, +10], plus J(chi)X^2 Galileon
PRIORS_ECI_V = {
    **PRIORS_BASE,
    **PRIORS_NMC_SHARED,
    "xi_chi":  ("SuperGaussian", -5.0, +10.0, 3.0, 4),  # (lo, hi, sigma, exponent)
    "log_alpha_J":  ("Uniform", -2.0, 2.0),             # log10 of dimensionless Galileon coupling
    "log_Lambda_J": ("Uniform", -3.0, -1.0),            # log10(Lambda_J / eV)
}


# =========================================================================
# Section 2 -- J(chi) X^2 Galileon kinetic term hook (NOT YET IMPLEMENTED)
# =========================================================================

def friedmann_with_galileon(a, params):
    """
    H^2(a) modified by J(chi)X^2 contribution.

    H^2 = (1/3 M_P^2) * [ rho_m + rho_r + rho_chi + rho_galileon ]

    where:
        rho_chi      = (1/2) chi_dot^2 + V(chi) - 3 H xi_chi chi^2 (Faraoni)
        rho_galileon = (3/2) alpha_J / Lambda_J^4 * chi_dot^4   (leading ESS)

    Vainshtein radius:
        r_V = (xi_chi * M_eff^2 / M_P^2)^{1/3} * Lambda_J^{-1}

    REQUIREMENT: r_V > 10 AU at solar-system to evade Cassini in ECI-V.
    This is the screening mechanism that frees xi_chi from the |xi_chi| < 0.024 wall.

    TODO_BACKEND: implement coupled (Friedmann, KG-chi, J-modified KG) ODE
    and emulate via cosmopower-jax custom_log. Validate against synthetic
    Wolf-mock data (xi=2.31, log B=+7.34) before A64 production run.

    CRITICAL CHECK before implementation: read Wolf 2025 sec. III + IV in full
    to confirm Wolf's screening mechanism is J(chi)X^2 Galileon and NOT
    chameleon, k-mouflage, or conformal coupling. If different, ECI-V is not
    a fair contest and this entire spec must be revised.
    """
    raise NotImplementedError("J(chi)X^2 Galileon backend not yet written. "
                              "Gated on A56 NMC retrain to |xi|<10, then ~1-2 wk dev.")


# =========================================================================
# Section 3 -- Likelihood factories
# =========================================================================

def loglike_eci_main(theta, datasets):
    """
    ECI-main likelihood: standard NMC, no Galileon.

    Uses A25 backend (cosmopower-jax custom_log emulator for log10 H(z) and w(z))
    on the |xi|<0.10 grid -- safe because the prior |xi|<0.024 is well inside.

    Datasets:
        - Planck PR4 (HiLLiPoP+LoLLiPoP)
        - DESI DR2 BAO  (TODO_PATH)
        - Pantheon+ SN-Ia (TODO_PATH)
        - KiDS-Legacy S_8 + xi_pm (TODO_PATH)
    """
    # H_of_z = a25_emulator_H(theta)
    # w_of_z = a25_emulator_w(theta)
    # logL = (planck_logL(theta, H_of_z) + desi_logL(theta, H_of_z)
    #        + pantheon_logL(theta, H_of_z) + kids_logL(theta, w_of_z))
    # return logL
    raise NotImplementedError("Wire to A25 backend + dataset loaders.")


def loglike_eci_v(theta, datasets):
    """
    ECI-V likelihood: NMC + J(chi)X^2 Galileon kinetic term.

    Requires:
      - A56-retrained emulator with |xi|<10 grid
      - New Friedmann backend friedmann_with_galileon()
      - Vainshtein radius constraint enforced as soft prior:
            log_prior += -0.5 * ((r_V_AU - 100)/30)^2 if r_V_AU < 10  (steep penalty)
                         else 0
    """
    raise NotImplementedError("Gated on A56 + J(chi)X^2 backend.")


# =========================================================================
# Section 4 -- numpyro models (skeleton)
# =========================================================================

def model_eci_main(datasets):
    # for name, spec in PRIORS_ECI_MAIN.items():
    #     numpyro.sample(name, _to_dist(spec))
    # numpyro.factor("logL", loglike_eci_main(theta, datasets))
    raise NotImplementedError


def model_eci_v(datasets):
    # for name, spec in PRIORS_ECI_V.items():
    #     numpyro.sample(name, _to_dist(spec))
    # numpyro.factor("logL", loglike_eci_v(theta, datasets))
    raise NotImplementedError


# =========================================================================
# Section 5 -- Bayes factor extractors
# =========================================================================

def savage_dickey_log_b(samples, param="xi_chi", test_point=0.0,
                        kde_bandwidth="silverman", prior_density_at_test=None):
    """
    Savage-Dickey density ratio:
        B(M vs M_nested) = pi(theta_test) / p(theta_test | data)

    For ECI-main vs LCDM-NMC limit: test_point = 0 on xi_chi.
    For ECI-V vs Wolf-vanilla cross-check: test_point = 2.31.

    Returns log B with KDE-based posterior density estimate.
    Bandwidth: Silverman default (robust to ~10^4 samples).

    REQUIREMENT: prior_density_at_test must be passed explicitly (not inferred)
    to avoid silent errors when prior is non-uniform (e.g. SuperGaussian on ECI-V).
    """
    # from sklearn.neighbors import KernelDensity
    # kde = KernelDensity(bandwidth=kde_bandwidth).fit(samples[param][:, None])
    # log_post = kde.score_samples(jnp.array([[test_point]]))[0]
    # return jnp.log(prior_density_at_test) - log_post
    raise NotImplementedError


def thermodynamic_integration_log_z(model, datasets, n_temps=16, n_samples_per=2000,
                                    beta_min=1e-4):
    """
    Estimate log Z by TI.
        log Z = integral_0^1 <log L>_beta d beta

    Geometric beta schedule: beta_i = beta_min * (1/beta_min)^(i/(n_temps-1))
    Trapezoidal rule for the integral.

    Used for the PRIMARY contest:
        log B(ECI-main vs ECI-V) = log Z_main - log Z_V

    Cross-check requirement (sec 4 of design): SDDR and TI must agree within
    +/- 0.5 log units. If discrepancy > 1, flag posterior multimodality.
    """
    raise NotImplementedError


# =========================================================================
# Section 6 -- Run plan (text only)
# =========================================================================

RUN_PLAN = """
A64 production run plan (gated):

1. Verify A56 NMC retrain to |xi|<10 is numerically clean (R^2 > 0.999 on holdout)
2. Verify A57 C4 v6 11-model MCMC has converged (R-hat < 1.01)
3. Code J(chi)X^2 Galileon backend in friedmann_with_galileon()
4. Train new emulator for ECI-V branch on |xi|<10 + alpha_J grid
5. Validate ECI-V on synthetic Wolf-mock data:
     - Inject xi=2.31 mock, recover with log B sanity within +/- 2sigma of +7.34
     - If FAILS: STOP, debug, do not publish
6. Run NUTS:
     - 8 chains, 4000 warmup, 8000 production for both branches
     - Save samples to /root/crossed-cosmos/runs/A64/eci_main_samples.h5
                       /root/crossed-cosmos/runs/A64/eci_v_samples.h5
7. Compute log B via SDDR (primary) and TI (cross-check)
8. Apply pre-registered hypothesis decision:
     H0: log B(main vs V) > +1   -> Cassini-clean wins
     H1: log B(V vs main) > +1   -> Wolf recovered
     H2: in [-1, +1]              -> tie
9. Report results in A64_PRODUCTION_RESULTS.md (frozen template, see design sec. 7)
"""

if __name__ == "__main__":
    print(__doc__)
    print(RUN_PLAN)
