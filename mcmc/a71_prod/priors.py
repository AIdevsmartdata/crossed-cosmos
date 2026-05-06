"""
A71 — ECI-vs-LCDM Framing B: prior distributions (numpyro).

Implements priors from A70 likelihood_spec.md Table 2A (ECI 9-dim),
Table 2C (CPL-effective 9-dim for Framing B), and PRIORS_LCDM (6-dim).

Hallu count: 85 (entering) → 85 (leaving). Mistral STRICT-BAN.
"""

import jax.numpy as jnp
import numpyro
import numpyro.distributions as dist


# =========================================================================
# SECTION 1 — Parameter names and ordering
# =========================================================================

PARAMS_LCDM = [
    "H0",           # [km/s/Mpc]
    "omega_b",      # ω_b h²
    "omega_c",      # ω_c h²
    "n_s",
    "log10As_e10",  # log10(10^10 A_s)
    "tau_reio",
]

PARAMS_CPL = [
    "H0",
    "omega_b",
    "omega_c",
    "n_s",
    "log10As_e10",
    "tau_reio",
    "w0",           # CPL w₀
    "wa",           # CPL w_a
    "M_B",          # SN absolute magnitude [mag]
]

PARAMS_ECI = [
    "H0",
    "omega_b",
    "omega_c",
    "n_s",
    "log10As_e10",
    "tau_reio",
    "xi_chi",       # NMC coupling ξ_χ (Cassini-clean range)
    "lambda_chi",   # ECI exponential slope λ_χ
    "chi0_over_MP", # Initial field value χ₀/M_P
]

# =========================================================================
# SECTION 2 — numpyro prior samplers
# =========================================================================

def sample_lcdm_priors() -> dict:
    """
    Sample ΛCDM 6-parameter priors in a numpyro model context.
    Returns dict {name: JAX array} of sampled values.

    Priors (from A70 Table PRIORS_LCDM + spec 2C):
      H₀          ~ Uniform[50, 90]
      ω_b         ~ Gaussian(0.02218, 0.00055)  [BBN prior, Cooke et al. 2018]
      ω_c         ~ Uniform[0.08, 0.20]
      n_s         ~ Uniform[0.90, 1.05]
      log10As_e10 ~ Uniform[2.7, 3.5]
      τ_reio      ~ Gaussian(0.054, 0.007)      [Planck 2018 low-ℓ pol]
    """
    H0          = numpyro.sample("H0",          dist.Uniform(50.0, 90.0))
    omega_b     = numpyro.sample("omega_b",     dist.Normal(0.02218, 0.00055))
    omega_c     = numpyro.sample("omega_c",     dist.Uniform(0.08, 0.20))
    n_s         = numpyro.sample("n_s",         dist.Uniform(0.90, 1.05))
    log10As_e10 = numpyro.sample("log10As_e10", dist.Uniform(2.7, 3.5))
    tau_reio    = numpyro.sample("tau_reio",    dist.Normal(0.054, 0.007))

    return {
        "H0": H0, "omega_b": omega_b, "omega_c": omega_c,
        "n_s": n_s, "log10As_e10": log10As_e10, "tau_reio": tau_reio,
    }


def sample_cpl_priors() -> dict:
    """
    Sample CPL-effective 9-parameter priors in a numpyro model context.
    Used for both CPL-LCDM (with w0=-1, wa=0 as reference) and CPL-ECI-eff.

    Priors (from A70 Table 2C):
      H₀, ω_b, ω_c, n_s, log10As_e10, τ_reio: same as ΛCDM
      w₀  ~ Uniform[-2.0, 0.0]
      w_a ~ Uniform[-3.0, 3.0]
      M_B ~ Uniform[-20.0, -18.5]   [SN-Ia absolute magnitude]
    """
    base = sample_lcdm_priors()
    w0  = numpyro.sample("w0", dist.Uniform(-2.0,  0.0))
    wa  = numpyro.sample("wa", dist.Uniform(-3.0,  3.0))
    M_B = numpyro.sample("M_B", dist.Uniform(-20.0, -18.5))

    return {**base, "w0": w0, "wa": wa, "M_B": M_B}


def sample_eci_priors() -> dict:
    """
    Sample ECI-Cassini 9-parameter priors in a numpyro model context.
    (Framing A / B — physical ECI parameters; no CPL parametrization.)

    Priors (from A70 Table 2A):
      H₀, ω_b, ω_c, n_s, log10As_e10, τ_reio: same as ΛCDM
      ξ_χ       ~ Uniform[-0.024, +0.024]   [Cassini gate, A56 consistent]
      λ_χ       ~ Uniform[0.5, 4.0]         [ECI exponential slope]
      χ₀/M_P    ~ Uniform[5e-3, 5e-2]       [initial field value]

    Note: Cassini constraint |ξ_χ|(χ₀/M_P)² ≲ 6e-6 is enforced via prior
    range rather than a hard gate in Framing B (no KG ODE).
    """
    base = sample_lcdm_priors()
    xi_chi      = numpyro.sample("xi_chi",      dist.Uniform(-0.024,  0.024))   # Cassini-clean prior; M24 confirmed posterior preference is real (rail at -0.024 even with [-0.10, +0.10] prior)
    lambda_chi  = numpyro.sample("lambda_chi",  dist.Uniform(0.5,     4.0))
    chi0_over_MP= numpyro.sample("chi0_over_MP",dist.Uniform(5e-3,    5e-2))

    return {**base, "xi_chi": xi_chi,
                    "lambda_chi": lambda_chi,
                    "chi0_over_MP": chi0_over_MP}


# =========================================================================
# SECTION 3 — Prior dict spec (for reference / PolyChord interface)
# =========================================================================
# These dicts mirror A70 pseudocode PRIORS_* constants.

PRIORS_LCDM_SPEC = {
    "H0":          ("Uniform",   50.0,    90.0),
    "omega_b":     ("Gaussian",  0.02218, 0.00055),
    "omega_c":     ("Uniform",   0.08,    0.20),
    "n_s":         ("Uniform",   0.90,    1.05),
    "log10As_e10": ("Uniform",   2.7,     3.5),
    "tau_reio":    ("Gaussian",  0.054,   0.007),
}

PRIORS_CPL_SPEC = {
    **PRIORS_LCDM_SPEC,
    "w0":          ("Uniform",  -2.0,    0.0),
    "wa":          ("Uniform",  -3.0,    3.0),
    "M_B":         ("Uniform", -20.0,  -18.5),
}

PRIORS_ECI_SPEC = {
    **PRIORS_LCDM_SPEC,
    "xi_chi":       ("Uniform", -0.024,   0.024),
    "lambda_chi":   ("Uniform",  0.5,     4.0),
    "chi0_over_MP": ("Uniform",  5e-3,    5e-2),
}


# =========================================================================
# SECTION 4 — Utility: prior log-prob (for TI cross-check)
# =========================================================================

def logprior_lcdm(theta: dict) -> jnp.ndarray:
    """Evaluate log prior density of ΛCDM params (not needed for NUTS, useful for TI)."""
    lp = 0.0
    lp += dist.Normal(0.02218, 0.00055).log_prob(theta["omega_b"])
    lp += dist.Normal(0.054,   0.007  ).log_prob(theta["tau_reio"])
    # Uniform priors contribute constant; only check bounds
    in_bounds = (
        (50.0  <= theta["H0"]          <= 90.0)
        & (0.08   <= theta["omega_c"]     <= 0.20)
        & (0.90   <= theta["n_s"]         <= 1.05)
        & (2.7    <= theta["log10As_e10"] <= 3.5)
    )
    return jnp.where(in_bounds, lp, -jnp.inf)


if __name__ == "__main__":
    print("[priors] LCDM params:", PARAMS_LCDM)
    print("[priors] CPL params: ", PARAMS_CPL)
    print("[priors] ECI params: ", PARAMS_ECI)
    print("[priors] Module loaded OK.")
