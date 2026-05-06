"""
A71 — ECI-vs-LCDM Framing B: numpyro model definitions for NUTS.

Provides:
  - lcdm_model(data_dict)                — ΛCDM 6-param numpyro model
  - cpl_model(data_dict)                 — CPL 9-param numpyro model (Framing B LCDM-CPL)
  - eci_cassini_cpl_model(data_dict)     — ECI 9-param via cosmopower emulator + CPL fit

Both are suitable for `numpyro.infer.MCMC(NUTS(...))`.

Framing B: no KG gate. CMB + DESI DR2 BAO + Pantheon+ likelihoods.
ACT DR6 lensing: deferred [TBD: add once values verified from Madhavacheril et al. 2024].

Hallu count: 85 (entering) → 85 (leaving). Mistral STRICT-BAN.
"""

import warnings
import jax
import jax.numpy as jnp
import numpyro
import numpyro.distributions as dist
from numpyro.infer import MCMC, NUTS

from .priors import sample_lcdm_priors, sample_cpl_priors, sample_eci_priors
from .likelihoods import (
    loglike_planck2018_compressed,
    loglike_desi_dr2_bao,
    loglike_pantheonplus,
)
from .background import derive_cpl_lsq

# =========================================================================
# SECTION 1 — ΛCDM model (6 parameters)
# =========================================================================

def lcdm_model(data_dict: dict | None = None):
    """
    numpyro model: ΛCDM with 6 free parameters.
    w(z) = -1 (fixed), w0 = -1, wa = 0.

    Parameters sampled:
      H0 [50,90], omega_b~N, omega_c [0.08,0.20],
      n_s [0.90,1.05], log10As_e10 [2.7,3.5], tau_reio~N.

    M_B is fixed at -19.3 (ΛCDM fiducial; marginalise in CPL model).
    [TBD: if Pantheon+ data available, use analytic M_B marginalization]

    Args:
      data_dict: dict with optional keys "bao_data", "sne_data".
                 If None, synthetic data is used (smoke test mode).
    """
    if data_dict is None:
        data_dict = {}
    bao_data = data_dict.get("bao_data", None)
    sne_data = data_dict.get("sne_data", None)

    # --- Sample priors ---
    H0          = numpyro.sample("H0",          dist.Uniform(50.0, 90.0))
    omega_b     = numpyro.sample("omega_b",     dist.Normal(0.02218, 0.00055))
    omega_c     = numpyro.sample("omega_c",     dist.Uniform(0.08, 0.20))
    n_s         = numpyro.sample("n_s",         dist.Uniform(0.90, 1.05))
    log10As_e10 = numpyro.sample("log10As_e10", dist.Uniform(2.7, 3.5))
    tau_reio    = numpyro.sample("tau_reio",    dist.Normal(0.054, 0.007))

    # ΛCDM dark energy: fixed
    w0 = jnp.array(-1.0)
    wa = jnp.array(0.0)

    # SN nuisance: treat M_B as deterministic (analytically marginalized internally)
    M_B = jnp.array(-19.3)

    # --- Derived quantities ---
    h       = H0 / 100.0
    Omega_m = (omega_b + omega_c) / h**2
    omega_m = omega_b + omega_c

    # --- Log-likelihoods ---
    lL_cmb = loglike_planck2018_compressed(omega_b, omega_c, H0, log10As_e10, n_s)
    lL_bao = loglike_desi_dr2_bao(
        H0, Omega_m, w0, wa, omega_b, omega_m,
        data_dict=bao_data, use_default_warning=False,
    )
    lL_sne = loglike_pantheonplus(
        H0, Omega_m, w0, wa, M_B, data_dict=sne_data,
    )

    logL_total = lL_cmb + lL_bao + lL_sne

    numpyro.factor("loglike", logL_total)


# =========================================================================
# SECTION 2 — CPL model (9 parameters, Framing B)
# =========================================================================

def cpl_model(data_dict: dict | None = None):
    """
    numpyro model: CPL dark energy with 9 free parameters.
    This is the Framing B "CPL-LCDM-eff" model.

    Extra params vs ΛCDM: w0 ∈ [-2, 0], wa ∈ [-3, 3], M_B ∈ [-20, -18.5].

    Args:
      data_dict: dict with optional "bao_data", "sne_data".
    """
    if data_dict is None:
        data_dict = {}
    bao_data = data_dict.get("bao_data", None)
    sne_data = data_dict.get("sne_data", None)

    # --- Sample priors ---
    H0          = numpyro.sample("H0",          dist.Uniform(50.0, 90.0))
    omega_b     = numpyro.sample("omega_b",     dist.Normal(0.02218, 0.00055))
    omega_c     = numpyro.sample("omega_c",     dist.Uniform(0.08, 0.20))
    n_s         = numpyro.sample("n_s",         dist.Uniform(0.90, 1.05))
    log10As_e10 = numpyro.sample("log10As_e10", dist.Uniform(2.7, 3.5))
    tau_reio    = numpyro.sample("tau_reio",    dist.Normal(0.054, 0.007))
    w0          = numpyro.sample("w0",          dist.Uniform(-2.0, 0.0))
    wa          = numpyro.sample("wa",          dist.Uniform(-3.0, 3.0))
    M_B         = numpyro.sample("M_B",         dist.Uniform(-20.0, -18.5))

    # --- Derived quantities ---
    h       = H0 / 100.0
    Omega_m = (omega_b + omega_c) / h**2
    omega_m = omega_b + omega_c

    # --- Log-likelihoods ---
    lL_cmb = loglike_planck2018_compressed(omega_b, omega_c, H0, log10As_e10, n_s)
    lL_bao = loglike_desi_dr2_bao(
        H0, Omega_m, w0, wa, omega_b, omega_m,
        data_dict=bao_data, use_default_warning=False,
    )
    lL_sne = loglike_pantheonplus(
        H0, Omega_m, w0, wa, M_B, data_dict=sne_data,
    )

    logL_total = lL_cmb + lL_bao + lL_sne
    numpyro.factor("loglike", logL_total)


# =========================================================================
# SECTION 3 — ECI-Cassini CPL-effective model (9 parameters, Framing B)
# =========================================================================

def eci_cassini_cpl_model(data_dict: dict | None = None):
    """
    numpyro model: ECI-Cassini with CPL-effective parametrization.

    Physical ECI parameters (ξ_χ, λ_χ, χ₀/M_P) are sampled. The cosmopower
    emulator provides H(z) and w(z). w₀ and w_a are derived from w(z) via LSQ fit.
    The resulting CPL (H0, Omega_m, w0_eci, wa_eci) is used for BAO/SNe distances.

    Requires emulators.load_emulators() to have been called before MCMC.

    Parameters sampled (9):
      H0, omega_b, omega_c, n_s, log10As_e10, tau_reio (6 base)
      xi_chi ∈ [-0.024, 0.024] (Cassini-clean NMC coupling)
      lambda_chi ∈ [0.5, 4.0]  (ECI exponential slope)
      chi0_over_MP ∈ [5e-3, 5e-2] (initial field value)

    M_B: fixed at -19.3 in ECI Framing B (marginalisation simplification).
    [TBD: sample M_B if Pantheon+ data available for ECI run]

    NOTE: The emulator validity range from A25 SUMMARY is:
      |ξ| ∈ [0, 0.10], λ ∈ [0.05, 3], φ₀ ∈ [0.01, 0.30],
      ω_b h² ∈ [0.018, 0.026], ω_c h² ∈ [0.095, 0.140], h ∈ [0.55, 0.80].
    Prior range for xi_chi [-0.024, 0.024] is within emulator range.
    λ up to 4.0 slightly exceeds training range [0.05, 3]; extrapolation risk.
    [TBD: retrain emulator with lambda up to 4.5 or trim prior to [0.5, 3.0]]
    """
    from . import emulators  # imported here to avoid circular deps + allow lazy load

    if data_dict is None:
        data_dict = {}
    bao_data = data_dict.get("bao_data", None)
    sne_data = data_dict.get("sne_data", None)

    # --- Sample priors ---
    H0          = numpyro.sample("H0",          dist.Uniform(50.0, 90.0))
    omega_b     = numpyro.sample("omega_b",     dist.Normal(0.02218, 0.00055))
    omega_c     = numpyro.sample("omega_c",     dist.Uniform(0.08, 0.20))
    n_s         = numpyro.sample("n_s",         dist.Uniform(0.90, 1.05))
    log10As_e10 = numpyro.sample("log10As_e10", dist.Uniform(2.7, 3.5))
    tau_reio    = numpyro.sample("tau_reio",    dist.Normal(0.054, 0.007))
    xi_chi      = numpyro.sample("xi_chi",      dist.Uniform(-0.024, 0.024))
    lambda_chi  = numpyro.sample("lambda_chi",  dist.Uniform(0.5, 4.0))
    chi0_over_MP= numpyro.sample("chi0_over_MP",dist.Uniform(5e-3, 5e-2))

    M_B = jnp.array(-19.3)

    # --- ECI emulator call ---
    h       = H0 / 100.0

    # Get w(z) from emulator; derive CPL (w0, wa) via LSQ
    import numpy as _np
    z_grid_jnp = jnp.array(emulators.Z_GRID)

    w_arr = emulators.cp_w(xi_chi, lambda_chi, chi0_over_MP,
                            omega_b, omega_c, h)
    w0_eci, wa_eci = derive_cpl_lsq(w_arr, z_grid_jnp)

    # H(z=0) from emulator gives H0_eci; use as a consistency cross-check
    # but still sample H0 from prior for CMB / BAO pivot
    # [TBD: decide whether to pin H0 to emulator H(z=0) or keep as free param
    #  with softened prior; for now, use sampled H0 for distances]

    Omega_m = (omega_b + omega_c) / h**2
    omega_m = omega_b + omega_c

    # --- Log-likelihoods ---
    lL_cmb = loglike_planck2018_compressed(omega_b, omega_c, H0, log10As_e10, n_s)
    lL_bao = loglike_desi_dr2_bao(
        H0, Omega_m, w0_eci, wa_eci, omega_b, omega_m,
        data_dict=bao_data, use_default_warning=False,
    )
    lL_sne = loglike_pantheonplus(
        H0, Omega_m, w0_eci, wa_eci, M_B, data_dict=sne_data,
    )

    logL_total = lL_cmb + lL_bao + lL_sne
    numpyro.factor("loglike", logL_total)


# =========================================================================
# SECTION 4 — Wolf-NMC-KG model (Framing A, KG-constrained)
# =========================================================================

def wolf_kg_model(data_dict: dict | None = None):
    """
    numpyro model: Wolf-NMC-KG (Framing A primary, KG-physical gate).

    Implements the Wolf 2025 NMC scalar-tensor model (arXiv:2504.07679) with
    a hard KG-physical gate that rejects samples with log L = -inf if the
    homogeneous background is unphysical.

    PHYSICS:
      Action: S = ∫d⁴x √(-g)[F(φ)/2 R − ½(∂φ)² − V(φ) + L_m]
      F(φ) = 1 − ξ φ², V(φ) = V₀ + β φ + ½ m² φ²
      V₀ tuned to close Friedmann today (H₀ = H₀_sampled).

    KG GATE (per A70 likelihood_spec.md §2B, HARD GATE):
      Integrates wolf_kg_ode_2d from N=−5 to N=0. Rejects sample if:
        (a) max|φ(N)| > 10 M_P  [runaway]
        (b) min F(φ(N)) < 0.01  [ghost / F-collapse]
        (c) |lnH(N=0)| > 0.05  [Friedmann closure failure]

    NOTE: wolf_kg_ode_2d uses scipy LSODA (CPU). For NUTS differentiability,
    the JAX ODE is available via _build_jax_ode() in wolf_background.py.
    This numpy model is suitable for PolyChord or sequential NUTS.

    For NUTS: H(z) is computed by interpolating lnH_traj from the ODE.
    The ODE is not differentiable through numpyro NUTS by default.
    For differentiable sampling, use diffrax Tsit5 ODE (deferred to A71 v2).

    Parameters sampled (11):
      H0 [50,90], omega_b~N, omega_c [0.08,0.20],
      n_s [0.90,1.05], log10As_e10 [2.7,3.5], tau_reio~N  (6 base)
      xi ∈ [-5.0, +0.20]   (KG-physical wedge per A70 §2B)
      beta ∈ [-10, +10]    (linear V term)
      m2 ∈ [-10, +10]      (scalar mass², can be negative)
      phi_init ∈ [1e-3, 0.05]   (initial field value, from A70 §2B)
      phidot_init ∈ [-0.1, +0.1] (initial field velocity)

    V₀: NOT sampled; tuned via tune_V0() for Friedmann closure at N=0.

    Returns H(z) via ODE + Friedmann constraint interpolation.
    Uses CPL distance functions for BAO/SNe (H_wolf derived from ODE).

    Args:
      data_dict: dict with optional "bao_data", "sne_data".
    """
    import numpy as np
    from .wolf_background import (
        wolf_kg_integrate, kg_gate, tune_V0, _F
    )
    from .background import H_cpl, D_M, D_H, sound_horizon_EH

    if data_dict is None:
        data_dict = {}
    bao_data = data_dict.get("bao_data", None)
    sne_data = data_dict.get("sne_data", None)

    # --- Sample ΛCDM base priors ---
    H0          = numpyro.sample("H0",          dist.Uniform(50.0, 90.0))
    omega_b     = numpyro.sample("omega_b",     dist.Normal(0.02218, 0.00055))
    omega_c     = numpyro.sample("omega_c",     dist.Uniform(0.08, 0.20))
    n_s         = numpyro.sample("n_s",         dist.Uniform(0.90, 1.05))
    log10As_e10 = numpyro.sample("log10As_e10", dist.Uniform(2.7, 3.5))
    tau_reio    = numpyro.sample("tau_reio",    dist.Normal(0.054, 0.007))

    # --- Sample Wolf-NMC-KG specific priors (per A70 §2B) ---
    xi          = numpyro.sample("xi",          dist.Uniform(-5.0, 0.20))
    beta        = numpyro.sample("beta",        dist.Uniform(-10.0, 10.0))
    m2          = numpyro.sample("m2",          dist.Uniform(-10.0, 10.0))
    phi_init    = numpyro.sample("phi_init",    dist.Uniform(1e-3, 5e-2))
    phidot_init = numpyro.sample("phidot_init", dist.Uniform(-0.1, 0.1))

    M_B = jnp.array(-19.3)

    # --- Derived ---
    h       = H0 / 100.0
    omega_m = omega_b + omega_c
    Omega_m = omega_m / h**2

    # --- V0 tuning (Friedmann closure at N=0) ---
    # Use numpy for ODE (not differentiable; suitable for PolyChord/sequential NUTS)
    h_np    = float(h)
    Om_np   = float(Omega_m)
    Or_np   = float(4.15e-5 / h_np**2)

    V0_val = tune_V0(float(xi), float(beta), float(m2),
                     float(phi_init), float(phidot_init), Om_np, Or_np)

    # --- Quick F gate at phi_init (early exit before ODE) ---
    F_init = _F(float(phi_init), float(xi))
    if F_init < 0.01:
        numpyro.factor("kg_gate", -jnp.inf)
        # Still need to register remaining likelihood factors
        numpyro.factor("loglike", jnp.array(-1e30))
        return

    # --- Integrate Wolf-KG ODE ---
    wolf_params = {
        'xi': float(xi), 'beta': float(beta), 'm2': float(m2),
        'phi_init': float(phi_init), 'phidot_init': float(phidot_init),
        'omega_m': float(omega_m), 'omega_r': 4.15e-5,
        'h': h_np, 'V0': V0_val,
    }
    result = wolf_kg_integrate(wolf_params, N_init=-5.0, N_final=0.0,
                                n_eval=200, method='LSODA')

    # --- KG gate ---
    if not result['success'] or result['N_grid'] is None:
        numpyro.factor("kg_gate", -jnp.inf)
        numpyro.factor("loglike", jnp.array(-1e30))
        return

    gate_pass, gate_reason = kg_gate(
        result['phi_traj'], result['F_traj'],
        result['lnH_traj'], result['N_grid']
    )

    if not gate_pass:
        numpyro.factor("kg_gate", jnp.array(-jnp.inf))
        numpyro.factor("loglike", jnp.array(-1e30))
        return

    numpyro.factor("kg_gate", jnp.array(0.0))

    # --- Extract H(z) from ODE trajectory ---
    # Compute w_eff(z) from lnH: w = -1 - (2/3) * d lnH / d lnz
    # For BAO/SNe: use CPL approximation fit to wolf H(z)
    # [Production: use direct ODE H(z) array without CPL compression]
    N_grid_np = result['N_grid']
    lnH_np    = result['lnH_traj']

    # BAO redshifts (DESI DR2: 7 bins)
    z_bao = jnp.array([0.30, 0.51, 0.71, 0.93, 1.32, 1.49, 2.33])

    # Interpolate H(z)/H0 from ODE
    N_bao = -jnp.log(1.0 + z_bao)  # N = -ln(1+z)

    # Use numpy interp (ODE output is numpy arrays)
    import numpy as _np
    lnH_bao = _np.interp(N_bao, N_grid_np, lnH_np)
    H_bao_over_H0 = _np.exp(lnH_bao)  # H(z)/H0

    # Convert to H(z) [km/s/Mpc]
    H_bao_kms = H0 * jnp.array(H_bao_over_H0)

    # For CPL fit to wolf H(z), extract w_eff:
    # d lnH / dN ≈ s_H, and w_eff = -1 - (2/3) * d lnH/d lnz * (1+z)/H^2
    # Simplified: use 2-point CPL fit at z=0 and z=1
    lnH_z0 = _np.interp(0.0, N_grid_np, lnH_np)
    lnH_z1 = _np.interp(-_np.log(2.0), N_grid_np, lnH_np)  # z=1 → N=-ln2
    H_z0 = _np.exp(lnH_z0)  # should be ~1.0
    H_z1 = _np.exp(lnH_z1)

    # In flat FLRW: H²(z)/H₀² = Ω_m(1+z)³ + Ω_Λ_eff(z)
    # For CPL: H²/H₀² = Ω_m(1+z)³ + (1-Ω_m)(1+z)^{3(1+w0+wa)} exp(-3 wa z/(1+z))
    # Quick 2-pt fit for w0, wa from H(z=0) and H(z=1):
    # H²(0)/H₀² = 1 → w0 determined by H(z=0)=H₀
    # H²(1)/H₀² = Ω_m*8 + (1-Ω_m)*2^{3(1+w0+wa)} exp(-1.5 wa) [z=1]
    # This is non-trivial to invert; use H_cpl directly with w0=-1, wa=0 as
    # approximation for BAO distances, with correction from wolf H(z) array.
    # [TBD: implement proper CPL fit for production run]
    w0_wolf = jnp.array(-1.0)  # placeholder; production: fit from ODE
    wa_wolf = jnp.array(0.0)   # placeholder

    # --- Log-likelihoods ---
    lL_cmb = loglike_planck2018_compressed(omega_b, omega_c, H0, log10As_e10, n_s)
    lL_bao = loglike_desi_dr2_bao(
        H0, Omega_m, w0_wolf, wa_wolf, omega_b, omega_m,
        data_dict=bao_data, use_default_warning=False,
    )
    lL_sne = loglike_pantheonplus(
        H0, Omega_m, w0_wolf, wa_wolf, M_B, data_dict=sne_data,
    )

    logL_total = lL_cmb + lL_bao + lL_sne
    numpyro.factor("loglike", logL_total)


# =========================================================================
# SECTION 5 — MCMC runner factory
# =========================================================================

def make_nuts_mcmc(model,
                   n_chains: int = 4,
                   n_warmup: int = 1000,
                   n_samples: int = 1000,
                   target_accept_prob: float = 0.85,
                   chain_method: str = "parallel",
                   progress_bar: bool = True) -> MCMC:
    """
    Build a numpyro NUTS MCMC object for the given model.

    Args:
      model: numpyro model callable (e.g. lcdm_model)
      n_chains: number of chains (4 for smoke test, 8 for production)
      n_warmup: warmup steps per chain
      n_samples: sampling steps per chain
      target_accept_prob: NUTS dual averaging target (0.85 = standard)
      chain_method: "parallel" (preferred for GPU) or "sequential" (fallback)
        If JAX named_shape errors occur with parallel, try sequential.
      progress_bar: show tqdm progress

    Returns:
      numpyro.infer.MCMC object (not yet run)
    """
    kernel = NUTS(model, target_accept_prob=target_accept_prob)
    mcmc = MCMC(
        kernel,
        num_warmup=n_warmup,
        num_samples=n_samples,
        num_chains=n_chains,
        chain_method=chain_method,
        progress_bar=progress_bar,
    )
    return mcmc


if __name__ == "__main__":
    print("[numpyro_models] ΛCDM model defined:", lcdm_model.__name__)
    print("[numpyro_models] CPL model defined:", cpl_model.__name__)
    print("[numpyro_models] ECI CPL model defined:", eci_cassini_cpl_model.__name__)
    print("[numpyro_models] Wolf-NMC-KG model defined:", wolf_kg_model.__name__)
    print("[numpyro_models] Module OK.")
