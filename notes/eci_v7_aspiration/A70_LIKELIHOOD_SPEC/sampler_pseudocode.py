"""
A70 — Sampler pipeline pseudocode skeleton for A71 (PC GPU MCMC).

STATUS: SPEC ONLY. Not executable. No imports are resolved.
Designed for RTX 5060 Ti + JAX 0.10+ (named_shape patch applied per MEMORY.md).
Parent task: ECI-vs-Wolf Bayes contest, two framings.

Two pipelines:
  Pipeline A: PolyChord (primary, Framing A — KG-physics gate)
  Pipeline B: NUTS via numpyro (secondary, Framing B — CPL-effective)

Hallu count: 85 (entering) -> 85 (must not change).
Mistral STRICT-BAN.
"""

# =========================================================================
# SECTION 0 — Shared constants
# =========================================================================

# KG-gate thresholds (see likelihood_spec.md sec 3.5)
PHI_RUNAWAY_THRESHOLD = 10.0      # in M_P units
F_COLLAPSE_THRESHOLD  = 0.01      # F(phi) = 1 - xi phi^2 < this -> reject
FRIEDMANN_CLOSURE_TOL = 0.05      # |a_today - 1| > this -> reject
N_INIT = -8.0                     # ln(a_init) = ln(1/3000) ~= -8
N_TODAY = 0.0

# PolyChord settings (Framing A)
POLYCHORD_NLIVE    = 500
POLYCHORD_REPEATS  = 30
POLYCHORD_OUTPUT   = "/home/remondiere/pc_calcs/A71/polychord_runs/"

# NUTS settings (Framing B)
N_CHAINS        = 8
N_WARMUP        = 4000
N_PRODUCTION    = 8000
TARGET_R_HAT    = 1.01
TARGET_ESS      = 400
NUTS_OUTPUT     = "/home/remondiere/pc_calcs/A71/nuts_runs/"

# =========================================================================
# SECTION 1 — Prior specifications (Framing A)
# =========================================================================

PRIORS_ECI_CASSINI = {
    "H0":          ("Uniform",   50.0,   90.0),
    "omega_b":     ("Gaussian",  0.02218, 0.00055),
    "omega_c":     ("Uniform",   0.08,   0.20),
    "n_s":         ("Uniform",   0.90,   1.05),
    "log10As_e10": ("Uniform",   2.7,    3.5),
    "tau_reio":    ("Gaussian",  0.054,  0.007),
    "xi_chi":      ("Uniform",  -0.024, +0.024),
    "lambda_chi":  ("Uniform",   0.5,    4.0),
    "chi0_over_MP":("Uniform",   5e-3,   5e-2),
}

PRIORS_WOLF_KG = {
    "H0":          ("Uniform",   50.0,   90.0),
    "omega_b":     ("Gaussian",  0.02218, 0.00055),
    "omega_c":     ("Uniform",   0.08,   0.20),
    "n_s":         ("Uniform",   0.90,   1.05),
    "log10As_e10": ("Uniform",   2.7,    3.5),
    "tau_reio":    ("Gaussian",  0.054,  0.007),
    "xi_wolf":     ("Uniform",  -5.0,   +0.20),
    "beta_wolf":   ("Uniform",  -10.0,  +10.0),
    "m2_wolf":     ("Uniform",  -10.0,  +10.0),
    "phi_init":    ("Uniform",   1e-3,   5e-2),
    "phidot_init": ("Uniform",  -0.1,   +0.1),
}

PRIORS_LCDM = {
    "H0":          ("Uniform",   50.0,   90.0),
    "omega_b":     ("Gaussian",  0.02218, 0.00055),
    "omega_c":     ("Uniform",   0.08,   0.20),
    "n_s":         ("Uniform",   0.90,   1.05),
    "log10As_e10": ("Uniform",   2.7,    3.5),
    "tau_reio":    ("Gaussian",  0.054,  0.007),
}


# =========================================================================
# SECTION 2 — KG stability gate (Framing A only)
# =========================================================================

def kg_gate(phi_trajectory, F_trajectory, a_today):
    """
    SPEC: Returns True if sample is KG-physical, False if reject.
    Rejection: max(|phi|) > PHI_RUNAWAY_THRESHOLD, OR
               min(F) < F_COLLAPSE_THRESHOLD, OR
               |a_today - 1| > FRIEDMANN_CLOSURE_TOL.
    Potential-agnostic; integrates dynamically per sample.
    """
    raise NotImplementedError("Wire to ODE integrator output.")


def wolf_kg_ode(N, state, params):
    """
    SPEC: Homogeneous KG + Friedmann ODE for Wolf quadratic-V NMC.
    State: [phi, phidot, H_over_H0]; phidot = dphi/dN.
    Params: {xi, beta, m2, phi_init, phidot_init, omega_m, omega_r, H0}.
    V(phi) = V0 + beta*phi + 0.5*m2*phi^2 ; F(phi) = 1 - xi*phi^2.

    GBD background equations: see Clifton et al. 2012 review or hi_class
    source [TBD: cite concrete reference; do not fabricate].

    For PolyChord: scipy solve_ivp LSODA. Radau cross-check for stiff.
    For NUTS: jax.experimental.ode.odeint or diffrax Tsit5.
    """
    raise NotImplementedError("Implement GBD background equations.")


# =========================================================================
# SECTION 3 — Log-likelihood factories
# =========================================================================

def loglike_planck2018(theta, cls_TT, cls_TE, cls_EE):
    """SPEC: Planck 2018 Plik coadded via clik wrapper (NOT PR4 — A69)."""
    raise NotImplementedError


def loglike_desi_dr2_bao(H_of_z, chi_of_z, r_d, z_bins, data_vector, cov_inv):
    """
    SPEC: DESI DR2 BAO (arXiv:2503.14738). 7 z-bins.
    log L_BAO = -0.5 * (theory - data) @ cov_inv @ (theory - data).
    """
    raise NotImplementedError


def loglike_pantheonplus(mu_theory, mu_obs, cov_sne_inv, M_B):
    """
    SPEC: Pantheon+ (Brout et al. 2022) [TBD: verify arXiv ID].
    Marginalize M_B analytically.
    """
    raise NotImplementedError


def loglike_act_dr6_lensing(A_lens_theory, A_lens_obs=None, sigma_Alens=None):
    """
    SPEC: ACT DR6 lensing compressed.
    [TBD: verify A_lens_obs, sigma_Alens, alpha exponent from
     Madhavacheril et al. 2024; do NOT fabricate.]
    """
    raise NotImplementedError


def loglike_total_framing_a(theta, model="ECI_CASSINI", datasets=None):
    """
    SPEC: Combined log-L for Framing A.
    Steps:
      1. Unpack theta per model
      2. Integrate KG ODE -> (phi_traj, F_traj, a_today)
      3. Apply KG gate; if fails -> return -inf
      4. Run Boltzmann (hi_class or A25/extended emulator)
      5. Sum: CMB + BAO + SNe + lens
    """
    raise NotImplementedError


def loglike_total_framing_b(theta, datasets=None):
    """SPEC: Framing B (CPL-effective, no KG gate)."""
    raise NotImplementedError


# =========================================================================
# SECTION 4 — PolyChord pipeline (Framing A primary)
# =========================================================================

def run_polychord_framing_a(model_name, priors, loglike_fn, output_dir):
    """
    SPEC: PolyChord run for one model.
    model_name in {"ECI_CASSINI", "WOLF_KG", "LCDM"}.

    EXPECTED RUNTIME (RTX 5060 Ti, direct ODE):
      ECI_CASSINI:  ~2-4 h   (9 params, emulator possible)
      WOLF_KG:      ~8-16 h  (11 params, hard gate slows convergence)
      LCDM:         ~0.5-1 h (6 params)

    If WOLF_KG too slow: nlive=200, repeats=50.
    """
    raise NotImplementedError("Install pypolychord; verify GPU/CPU dispatch.")


# =========================================================================
# SECTION 5 — NUTS pipeline (Framing B + cross-check)
# =========================================================================

def run_nuts_framing_b(model_name, priors, loglike_fn, output_dir):
    """
    SPEC: NUTS via numpyro on RTX 5060 Ti.
    8 chains x 4000 warmup x 8000 production.
    Convergence: R_hat < 1.01, ESS > 400 per param.
    JAX named_shape patch required (MEMORY.md).
    """
    raise NotImplementedError("Wire to numpyro; load A25 emulator pkl.")


# =========================================================================
# SECTION 6 — Bayes factor extractors
# =========================================================================

def polychord_bayes_factors(logZ_dict):
    """
    SPEC: Extract log B from PolyChord log Z outputs.
    Hypothesis tests per A70 SUMMARY frozen table:
      H_A0: log_B_WOLF_LCDM < 0
      H_A1: log_B_WOLF_LCDM > +3
      H_ECI: log_B_ECI_LCDM in [-3, +1]
    """
    raise NotImplementedError


def savage_dickey_log_b(samples_xi, prior_lo, prior_hi, test_point=0.0,
                         kde_bandwidth="silverman"):
    """
    SPEC: Savage-Dickey for Framing B.
    log B = log(1/(prior_hi-prior_lo)) - log_kde(test_point).
    Pass prior_lo, prior_hi explicitly; NEVER infer from samples.
    """
    raise NotImplementedError


def thermodynamic_integration_log_z(loglike_fn, prior_fn, n_dims,
                                     n_temps=16, n_samples_per=2000,
                                     beta_min=1e-4):
    """
    SPEC: TI cross-check. 16 temps geometric beta in [1e-4, 1.0].
    log Z ~ trapezoidal sum_i 0.5*(beta_{i+1}-beta_i)*(<log L>_{i+1} + <log L>_i).
    Consistency gate: |log Z_TI - log Z_PolyChord| < 0.5.
    """
    raise NotImplementedError


# =========================================================================
# SECTION 7 — Master run script (order of operations for A71)
# =========================================================================

RUN_ORDER = """
A71 EXECUTION ORDER (do not skip; gates are hard):

PHASE 0 — Environment setup
  0a. Apply JAX named_shape patch (MEMORY.md reference_jax_patch.md)
  0b. Load A25 cosmopower-jax pkl:
        /home/remondiere/pc_calcs/cosmopower_nmc_emulator/nmc_kg_w.pkl
        /home/remondiere/pc_calcs/cosmopower_nmc_emulator/nmc_kg_logH.pkl
      Plus extended emulator (NEW 2026-05-05 night):
        /home/remondiere/pc_calcs/cosmopower_nmc_emulator_extended/nmc_kg_w_extended.pkl
        /home/remondiere/pc_calcs/cosmopower_nmc_emulator_extended/nmc_kg_logH_extended.pkl
  0c. Load DESI DR2 BAO data + cov.
  0d. Load Pantheon+ distance moduli + cov.
  0e. Load ACT DR6 lensing A_lens [TBD: verify values].

PHASE 1 — LCDM baseline (PolyChord, ~0.5h)
  1a. Run PolyChord on LCDM (6 params)
  1b. Record logZ_LCDM ± sigma_LCDM
  1c. log B = 0.0 by definition.

PHASE 2 — ECI-Cassini (PolyChord, Framing A, ~2-4h)
  2a. Run PolyChord on ECI (9 params, A25 emulator)
  2b. Sanity: H_0 posterior peak ~ 70 ± 8 (A25 baseline).

PHASE 3 — Wolf-NMC-KG (PolyChord, Framing A, ~8-16h)
  3a. PREREQUISITE: wolf_kg_ode tested on synthetic data first.
      phi_init=0.01, xi=0.10 -> stable. xi=0.30 -> gate triggers.
  3b. Run PolyChord on WOLF_KG (11 params)
  3c. SANITY GATE H_sanity: xi posterior peaks at xi < 0.20.
      If xi > 0.20: gate impl bug — STOP.

PHASE 4 — Bayes factors (Framing A)
  4a. log_B_ECI_LCDM  -> H_ECI
  4b. log_B_WOLF_LCDM -> H_A0/H_A1
  4c. log_B_ECI_WOLF  -> primary contest

PHASE 5 — TI cross-check (NUTS)
  5a. TI for ECI (16 temps × 2000)
  5b. TI for WOLF_KG
  5c. |logZ_TI - logZ_PolyChord| < 0.5 each.
  5d. Discrepancy > 1: flag, do NOT publish.

PHASE 6 — Framing B (NUTS CPL, diagnostic)
  6a. NUTS on CPL-ECI and CPL-Wolf (8 chains × 4000+8000)
  6b. Savage-Dickey at w0=-1, wa=0.
  6c. Appendix only.

PHASE 7 — Convergence + output
  7a. R_hat < 1.01, ESS > 400.
  7b. Save samples.npz + diagnostics.json.
  7c. Write A71_RESULTS.md (log B values + decisions + hallu count = 85).
"""


if __name__ == "__main__":
    print(__doc__)
    print(RUN_ORDER)
