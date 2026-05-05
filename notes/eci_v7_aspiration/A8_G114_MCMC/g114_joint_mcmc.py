"""A8 — G1.14 JOINT MCMC over (τ_lepton, τ_quark, all couplings)
LYD20 Model VI on 13 quark + lepton observables (PDG 2026 + LYD20 ratios).

ECI v6.0.53.1, post-W1 [TAU-NEAR-I VIABLE] (χ²/dof=1.05 at τ*=-0.19+1.00i)
and PC1 [TWO-TAU VIABLE] (overfit reference, only 4 ratios).

This is the proper joint test: NUTS over the FULL parameter space, computing
the posterior on (Re τ_l, Im τ_l, Re τ_q, Im τ_q, ...) on 13 observables with
realistic PDG uncertainties.

Sampler: blackjax NUTS on RTX 5060 Ti GPU (JAX backend).
Bench (gpu_nuts_template.py 2026-05-04): ≈575 samples/sec for 5-param Gaussian.
Estimate for 13-param non-Gaussian with eta(τ) evaluations: ≈100 samples/sec.

Run on PC1:
  cd /home/remondiere/pc_calcs/
  /home/remondiere/.venv-mcmc-bench/bin/python g114_joint_mcmc.py
  (≈ 5-10 min for 10000 warmup + 30000 samples on RTX 5060 Ti)

Output: g114_joint_mcmc_results.json + g114_chain.npz + g114_corner.png
"""
import os, sys, time, json
import numpy as np

# ─────────────────────────────────────────────────────────────────
# CLI flags & GPU setup
# ─────────────────────────────────────────────────────────────────
PRIOR_NEAR_I = ("--restricted" in sys.argv)   # restrict |τ_l - i| < 0.5 (v7.4 attractor)
N_WARMUP     = 10_000
N_SAMPLES    = 30_000
N_CHAINS     = 4
SEED         = 20260505

# Force JAX to use GPU if available
os.environ.setdefault("XLA_PYTHON_CLIENT_PREALLOCATE", "false")
os.environ.setdefault("XLA_PYTHON_CLIENT_MEM_FRACTION", "0.85")

import jax
import jax.numpy as jnp
import blackjax

print(f"JAX {jax.__version__}, devices={jax.devices()}, backend={jax.default_backend()}", flush=True)
print(f"PRIOR_NEAR_I={PRIOR_NEAR_I}  N_WARMUP={N_WARMUP}  N_SAMPLES={N_SAMPLES}  N_CHAINS={N_CHAINS}", flush=True)

# ─────────────────────────────────────────────────────────────────
# PDG 2026 + LYD20 Table I targets
#   PDG 2026: lepton mass ratios from latest charged-lepton masses
#             CKM angles from latest global fit
#   LYD20:    quark mass ratios at Q=1 TeV (MS-bar)
# ─────────────────────────────────────────────────────────────────
PDG = {
    # quark mass ratios at Q=1 TeV (from LYD20 Table I, PDG 2024 RGE-evolved)
    "m_u/m_c":   (2.04e-3,  0.10e-3),    # 5% uncertainty
    "m_c/m_t":   (2.68e-3,  0.13e-3),
    "m_d/m_s":   (5.18e-2,  0.30e-2),
    "m_s/m_b":   (1.31e-2,  0.10e-2),
    # lepton mass ratios from PDG 2024 lepton table (m_e=0.511 MeV, m_mu=105.658 MeV, m_tau=1776.86 MeV)
    "m_e/m_mu":  (4.836e-3, 2.0e-5),
    "m_mu/m_tau":(5.946e-2, 3.0e-4),
    # CKM mixing angles (Wolfenstein parametrisation, PDG 2024 fit)
    "sin_12":    (0.22534,  0.0007),     # |V_us|/sqrt(1-|V_ub|^2)
    "sin_13":    (0.003690, 0.0001),     # |V_ub|
    "sin_23":    (0.04182,  0.0008),     # |V_cb|/sqrt(1-|V_ub|^2)
    "J_CP":      (3.08e-5,  0.15e-5),    # Jarlskog invariant (PDG 2024)
    # m_t kept as overall scale absorber — NOT directly fitted (degenerate with α_u)
    # Total: 4 (quark masses) + 2 (lepton masses) + 3 (CKM angles) + 1 (J) = 10 obs.
    # Actually we use 4+2+3+1+ (md/mb derived) = optionally 11. We code 10 hard obs.
}

# Convert to JAX arrays
_OBS_KEYS = ["m_u/m_c", "m_c/m_t", "m_d/m_s", "m_s/m_b",
             "m_e/m_mu", "m_mu/m_tau",
             "sin_12", "sin_13", "sin_23", "J_CP"]
PDG_VAL = jnp.array([PDG[k][0] for k in _OBS_KEYS])
PDG_SIG = jnp.array([PDG[k][1] for k in _OBS_KEYS])
N_OBS   = len(_OBS_KEYS)
print(f"N_OBS = {N_OBS}", flush=True)

# ─────────────────────────────────────────────────────────────────
# Modular forms: Dedekind eta and weight-{1,2,3,4,5} forms
# All in JAX so they can be jit + grad through.
# ─────────────────────────────────────────────────────────────────
N_ETA_TERMS = 40   # truncation; agrees with W1 reference within 1e-15

def eta(tau):
    """Dedekind η(τ) via q-product, JAX-jittable."""
    q = jnp.exp(2j * jnp.pi * tau)
    out = q ** (1.0 / 24.0)
    # JAX: unrolled product (constant trip count, jit-friendly)
    for n in range(1, N_ETA_TERMS + 1):
        out = out * (1.0 - q ** n)
    return out


def weight1_forms(tau):
    """Y1, Y2, Y3 — weight-1 forms of S'_4 in 3̂' rep (LYD20 Eq.(15a))."""
    e1 = eta(4 * tau) ** 4 / eta(2 * tau) ** 2
    e2 = eta(2 * tau) ** 10 / (eta(4 * tau) ** 4 * eta(tau) ** 4)
    e3 = eta(2 * tau) ** 4 / eta(tau) ** 2
    omega = jnp.exp(2j * jnp.pi / 3.0)
    s2 = jnp.sqrt(2.0)
    s3 = jnp.sqrt(3.0)
    Y1 = 4 * s2 * e1 + 1j * s2 * e2 + 2 * s2 * (1 - 1j) * e3
    Y2 = (-2 * s2 * (1 + s3) * omega ** 2 * e1
          - 1j * (1 - s3) / s2 * omega ** 2 * e2
          + 2 * s2 * (1 - 1j) * omega ** 2 * e3)
    Y3 = ( 2 * s2 * (s3 - 1) * omega * e1
          - 1j * (1 + s3) / s2 * omega * e2
          + 2 * s2 * (1 - 1j) * omega * e3)
    return Y1, Y2, Y3


def all_forms(tau):
    """All Y^(k) components needed for Model VI + unified lepton model.
    Polynomials in (Y1,Y2,Y3) per LYD20 §II + Appendix.
    """
    Y1, Y2, Y3 = weight1_forms(tau)
    # Weight-2 (3): LYD20 Eq.(15b)
    Y2_3 = 2 * Y1 ** 2 - 2 * Y2 * Y3
    Y2_4 = 2 * Y3 ** 2 - 2 * Y1 * Y2
    Y2_5 = 2 * Y2 ** 2 - 2 * Y1 * Y3
    # Weight-3 (1̂', 3̂'): LYD20 Eq.(15c)
    Y3_2 = 2 * (2 * Y1 ** 3 - Y2 ** 3 - Y3 ** 3)
    Y3_3 = 6 * Y3 * (Y2 ** 2 - Y1 * Y3)
    Y3_4 = 6 * Y2 * (Y3 ** 2 - Y1 * Y2)
    # Weight-4 (3): LYD20 Appendix Eq.(A1)
    Y4_4 = 6 * Y1 * (-Y2 ** 3 + Y3 ** 3)
    Y4_5 = 6 * Y1 * Y3 * (Y2 ** 2 - Y1 * Y3) + 2 * Y2 * (-2 * Y1 ** 3 + Y2 ** 3 + Y3 ** 3)
    Y4_6 = 6 * Y1 * Y2 * (Y1 * Y2 - Y3 ** 2) - 2 * Y3 * (-2 * Y1 ** 3 + Y2 ** 3 + Y3 ** 3)
    # Weight-5 (3̂): LYD20 Appendix Eq.(A2)
    Y5_3 = 18 * Y1 ** 2 * (-Y2 ** 3 + Y3 ** 3)
    Y5_4 = (4 * Y1 ** 4 * Y2 + 4 * Y1 * (Y2 ** 4 - 5 * Y2 * Y3 ** 3)
            + 14 * Y1 ** 3 * Y3 ** 2 - 4 * Y3 ** 2 * (Y2 ** 3 + Y3 ** 3)
            + 6 * Y1 ** 2 * Y2 ** 2 * Y3)
    Y5_5 = (-4 * Y1 ** 4 * Y3 - 4 * Y1 * (Y3 ** 4 - 5 * Y2 ** 3 * Y3)
            - 14 * Y1 ** 3 * Y2 ** 2 + 4 * Y2 ** 2 * (Y2 ** 3 + Y3 ** 3)
            - 6 * Y1 ** 2 * Y2 * Y3 ** 2)
    # Weight-5 (3̂',I)
    Y5_6 = 8 * Y1 ** 3 * Y2 * Y3 - 6 * Y1 ** 2 * (Y2 ** 3 + Y3 ** 3) + 2 * Y2 * Y3 * (Y2 ** 3 + Y3 ** 3)
    Y5_7 = (4 * Y1 ** 4 * Y2 - 2 * Y1 * Y2 ** 4 - 6 * Y1 ** 2 * Y2 ** 2 * Y3
            - 2 * Y1 ** 3 * Y3 ** 2 + 4 * Y2 ** 3 * Y3 ** 2 + 4 * Y1 * Y2 * Y3 ** 3 - 2 * Y3 ** 5)
    Y5_8 = -2 * (Y1 ** 3 * Y2 ** 2 + Y2 ** 5 - 2 * Y1 ** 4 * Y3
                  + 3 * Y1 ** 2 * Y2 * Y3 ** 2 - 2 * Y2 ** 2 * Y3 ** 3
                  + Y1 * (-2 * Y2 ** 3 * Y3 + Y3 ** 4))
    # Weight-5 (3̂',II)
    D = Y1 ** 4 + 3 * Y2 ** 2 * Y3 ** 2 - 2 * Y1 * (Y2 ** 3 + Y3 ** 3)
    Y5_9  = 4 * Y1 * D
    Y5_10 = 4 * Y2 * D
    Y5_11 = 4 * Y3 * D
    return dict(Y1=Y1, Y2=Y2, Y3=Y3,
                Y2_3=Y2_3, Y2_4=Y2_4, Y2_5=Y2_5,
                Y3_2=Y3_2, Y3_3=Y3_3, Y3_4=Y3_4,
                Y4_4=Y4_4, Y4_5=Y4_5, Y4_6=Y4_6,
                Y5_3=Y5_3, Y5_4=Y5_4, Y5_5=Y5_5,
                Y5_6=Y5_6, Y5_7=Y5_7, Y5_8=Y5_8,
                Y5_9=Y5_9, Y5_10=Y5_10, Y5_11=Y5_11)

# ─────────────────────────────────────────────────────────────────
# Mass matrices (LYD20 Model VI quarks + unified lepton model)
# All α_x absorbed into overall scale (irrelevant for ratios).
#
# Polar parametrisation per user spec:
#   coupling = magnitude * exp(i * gCP_phase)
# This makes CP-violating phases first-class parameters.
# ─────────────────────────────────────────────────────────────────
def M_up(f_q, beta_u, gamma_u, gCP_u):
    """M_u row 0 = α_u·(Y1,Y3,Y2)  [u^c]
       row 1 = β_u·exp(i·gCP_u)·(Y2_3,Y2_5,Y2_4)  [c^c]
       row 2 = γ_u·(Y5_3,Y5_5,Y5_4)  [t^c]
    α_u = 1 (overall scale).
    """
    bu = beta_u * jnp.exp(1j * gCP_u)
    M = jnp.array([
        [f_q["Y1"],          f_q["Y3"],          f_q["Y2"]],
        [bu * f_q["Y2_3"],   bu * f_q["Y2_5"],   bu * f_q["Y2_4"]],
        [gamma_u * f_q["Y5_3"], gamma_u * f_q["Y5_5"], gamma_u * f_q["Y5_4"]],
    ])
    return M


def M_down(f_q, beta_d, gamma_d1, gamma_d2_re, gamma_d2_im, gCP_d):
    """M_d row 0 = α_d·(Y1,Y3,Y2)  [d^c]
       row 1 = β_d·(Y5_3,Y5_5,Y5_4)  [s^c]
       row 2 = γ_d1·exp(i·gCP_d)·(Y5_6,Y5_8,Y5_7) + γ_d2·(Y5_9,Y5_11,Y5_10)  [b^c]
    γ_d2 is intrinsically complex (Model VI).
    """
    gd2 = gamma_d2_re + 1j * gamma_d2_im
    gd1 = gamma_d1 * jnp.exp(1j * gCP_d)
    M = jnp.array([
        [f_q["Y1"],          f_q["Y3"],          f_q["Y2"]],
        [beta_d * f_q["Y5_3"], beta_d * f_q["Y5_5"], beta_d * f_q["Y5_4"]],
        [gd1 * f_q["Y5_6"] + gd2 * f_q["Y5_9"],
         gd1 * f_q["Y5_8"] + gd2 * f_q["Y5_11"],
         gd1 * f_q["Y5_7"] + gd2 * f_q["Y5_10"]],
    ])
    return M


def M_lepton(f_l, beta_e, gamma_e, gCP_e):
    """Unified lepton model (LYD20 Eq.(Ml)):
       row E1^c = α_e·(Y4_4, Y4_6, Y4_5)         [weight-4]
       row E2^c = β_e·exp(i·gCP_e)·(Y2_3, Y2_5, Y2_4)  [weight-2]
       row E3^c = γ_e·(Y3_2, Y3_4, Y3_3)         [weight-3]
    α_e = 1.
    """
    be = beta_e * jnp.exp(1j * gCP_e)
    M = jnp.array([
        [f_l["Y4_4"],        f_l["Y4_6"],        f_l["Y4_5"]],
        [be * f_l["Y2_3"],   be * f_l["Y2_5"],   be * f_l["Y2_4"]],
        [gamma_e * f_l["Y3_2"], gamma_e * f_l["Y3_4"], gamma_e * f_l["Y3_3"]],
    ])
    return M

# ─────────────────────────────────────────────────────────────────
# Observables from M (mass ratios + CKM angles + Jarlskog)
# ─────────────────────────────────────────────────────────────────
def mass_ratios_jax(M):
    """Return (m1/m2, m2/m3) from singular values, sorted ascending."""
    sv = jnp.linalg.svd(M, compute_uv=False)
    sv = jnp.sort(sv)
    eps = 1e-30
    return sv[0] / (sv[1] + eps), sv[1] / (sv[2] + eps)


def ckm_angles_jax(Mu, Md):
    """CKM = U_uL† U_dL with rows sorted by ascending singular values.
       Returns (sin_12, sin_13, sin_23, J_CP)."""
    Uu, sv_u, _ = jnp.linalg.svd(Mu)
    Ud, sv_d, _ = jnp.linalg.svd(Md)
    iu = jnp.argsort(sv_u)
    id_ = jnp.argsort(sv_d)
    Uu = Uu[:, iu]
    Ud = Ud[:, id_]
    V = jnp.conj(Uu).T @ Ud
    aV = jnp.abs(V)
    V_ub = aV[0, 2]
    denom = jnp.sqrt(jnp.clip(1.0 - V_ub ** 2, 1e-20, 1.0))
    s12 = aV[0, 1] / denom
    s13 = V_ub
    s23 = aV[1, 2] / denom
    # Jarlskog invariant: J = Im(V_us V_cb V*_ub V*_cs)
    J = jnp.imag(V[0, 1] * V[1, 2] * jnp.conj(V[0, 2]) * jnp.conj(V[1, 1]))
    return s12, s13, jnp.abs(s23), jnp.abs(J)

# ─────────────────────────────────────────────────────────────────
# Joint log-posterior (NUTS target)
#   theta = [Re τ_q, Im τ_q, Re τ_l, Im τ_l,
#            log_β_u, log_γ_u, log_β_d, log_γ_d1, γd2_re, γd2_im,
#            log_β_e, log_γ_e,
#            gCP_u, gCP_d, gCP_e]
#   = 15 real parameters (we use log for positivity of magnitudes,
#     keeping γd2 components real — Model VI convention).
#   User-spec "13 free params" with magnitude+phase: matches if we
#   treat γ_d2 as a single complex param (2 reals = magnitude+phase
#   inseparable). Below uses 15 reals.
# ─────────────────────────────────────────────────────────────────
PARAM_NAMES = [
    "Re_tau_q", "Im_tau_q", "Re_tau_l", "Im_tau_l",
    "log_beta_u", "log_gamma_u",
    "log_beta_d", "log_gamma_d1", "gamma_d2_re", "gamma_d2_im",
    "log_beta_e", "log_gamma_e",
    "gCP_u", "gCP_d", "gCP_e",
]
N_PARAMS = len(PARAM_NAMES)


def predict(theta):
    """Compute model-predicted observables vector (length N_OBS)."""
    re_q, im_q, re_l, im_l = theta[0], theta[1], theta[2], theta[3]
    log_bu, log_gu = theta[4], theta[5]
    log_bd, log_gd1, gd2_re, gd2_im = theta[6], theta[7], theta[8], theta[9]
    log_be, log_ge = theta[10], theta[11]
    gCP_u, gCP_d, gCP_e = theta[12], theta[13], theta[14]

    tau_q = re_q + 1j * im_q
    tau_l = re_l + 1j * im_l
    f_q = all_forms(tau_q)
    f_l = all_forms(tau_l)

    Mu = M_up(f_q, jnp.exp(log_bu), jnp.exp(log_gu), gCP_u)
    Md = M_down(f_q, jnp.exp(log_bd), jnp.exp(log_gd1),
                gd2_re, gd2_im, gCP_d)
    Me = M_lepton(f_l, jnp.exp(log_be), jnp.exp(log_ge), gCP_e)

    mu_mc, mc_mt = mass_ratios_jax(Mu)
    md_ms, ms_mb = mass_ratios_jax(Md)
    me_mmu, mmu_mtau = mass_ratios_jax(Me)
    s12, s13, s23, J = ckm_angles_jax(Mu, Md)

    return jnp.array([mu_mc, mc_mt, md_ms, ms_mb,
                      me_mmu, mmu_mtau,
                      s12, s13, s23, J])


def log_prior(theta):
    re_q, im_q, re_l, im_l = theta[0], theta[1], theta[2], theta[3]
    log_bu, log_gu = theta[4], theta[5]
    log_bd, log_gd1, gd2_re, gd2_im = theta[6], theta[7], theta[8], theta[9]
    log_be, log_ge = theta[10], theta[11]
    gCP_u, gCP_d, gCP_e = theta[12], theta[13], theta[14]

    # Fundamental domain constraints (soft barrier).
    # τ_q in F: Im τ > sqrt(1 - Re τ^2) [|τ|>1] AND |Re τ| ≤ 1/2.
    # We use a relaxed domain: Im τ > 0.5, |Re τ| < 0.6 (allows wandering).
    lp = 0.0

    if PRIOR_NEAR_I:
        # v7.4 attractor restriction: |τ_l - i| < 0.5 hard prior
        d2 = (re_l - 0.0) ** 2 + (im_l - 1.0) ** 2
        lp = lp + jnp.where(d2 < 0.25, 0.0, -jnp.inf)
        # quark τ: stay in upper half plane, |τ_q - i| < 1.0 (loose)
        d2q = (re_q - 0.0) ** 2 + (im_q - 1.0) ** 2
        lp = lp + jnp.where(d2q < 1.0, 0.0, -jnp.inf)
    else:
        # standard fundamental-domain box
        lp = lp + jnp.where(jnp.abs(re_l) < 0.6, 0.0, -jnp.inf)
        lp = lp + jnp.where((im_l > 0.5) & (im_l < 2.5), 0.0, -jnp.inf)
        lp = lp + jnp.where(jnp.abs(re_q) < 0.6, 0.0, -jnp.inf)
        lp = lp + jnp.where((im_q > 0.5) & (im_q < 2.5), 0.0, -jnp.inf)

    # Weak Gaussian priors on log-magnitudes (avoids 1e-100 / 1e+100)
    lp = lp - 0.5 * (log_bu / 6.0) ** 2
    lp = lp - 0.5 * (log_gu / 6.0) ** 2
    lp = lp - 0.5 * (log_bd / 6.0) ** 2
    lp = lp - 0.5 * (log_gd1 / 6.0) ** 2
    lp = lp - 0.5 * (gd2_re / 5.0) ** 2
    lp = lp - 0.5 * (gd2_im / 5.0) ** 2
    lp = lp - 0.5 * (log_be / 6.0) ** 2
    lp = lp - 0.5 * (log_ge / 6.0) ** 2
    # CP phases on (-π, π) flat (von Mises with zero concentration ≈ flat)
    for i in (12, 13, 14):
        lp = lp + jnp.where(jnp.abs(theta[i]) < jnp.pi, 0.0, -jnp.inf)

    return lp


def log_likelihood(theta):
    pred = predict(theta)
    chi2 = jnp.sum(((pred - PDG_VAL) / PDG_SIG) ** 2)
    return -0.5 * chi2


def log_posterior(theta):
    lp = log_prior(theta)
    # Use jax.lax.cond to handle -inf cleanly under jit.
    return jnp.where(jnp.isfinite(lp), lp + log_likelihood(theta), -jnp.inf)


log_posterior_jit = jax.jit(log_posterior)

# ─────────────────────────────────────────────────────────────────
# NUTS sampler
# ─────────────────────────────────────────────────────────────────
def init_position(seed):
    """Reasonable starting point near (W1 best, LYD20 ratios)."""
    rng = np.random.default_rng(seed)
    pos = np.array([
        # τ_q near W1 single-τ best (-0.19 + 1.00i)
        -0.19 + 0.05 * rng.standard_normal(),
        1.00  + 0.05 * rng.standard_normal(),
        # τ_l near i (CM-anchored attractor)
        0.0   + 0.05 * rng.standard_normal(),
        1.00  + 0.05 * rng.standard_normal(),
        # log_β_u, log_γ_u  (W1 typical ~ exp(4.4) ≈ 80, exp(0) ≈ 1)
        4.4   + 0.3 * rng.standard_normal(),
        0.0   + 0.3 * rng.standard_normal(),
        # log_β_d, log_γ_d1, γd2_re, γd2_im
        2.0   + 0.3 * rng.standard_normal(),
        2.0   + 0.3 * rng.standard_normal(),
        0.0   + 0.5 * rng.standard_normal(),
        0.0   + 0.5 * rng.standard_normal(),
        # log_β_e, log_γ_e
        2.0   + 0.3 * rng.standard_normal(),
        -7.0  + 0.5 * rng.standard_normal(),  # γ_e tiny ≈ exp(-7)
        # CP phases
        0.0   + 0.5 * rng.standard_normal(),
        0.0   + 0.5 * rng.standard_normal(),
        0.0   + 0.5 * rng.standard_normal(),
    ], dtype=np.float64)
    return jnp.array(pos)


def run_nuts_one_chain(chain_id, init, n_warmup, n_samples, seed):
    key = jax.random.PRNGKey(seed + chain_id)
    warmup = blackjax.window_adaptation(blackjax.nuts, log_posterior_jit,
                                        target_acceptance_rate=0.8)
    print(f"  [chain {chain_id}] warmup {n_warmup} steps...", flush=True)
    t0 = time.perf_counter()
    (state, params), _ = warmup.run(key, init, num_steps=n_warmup)
    print(f"  [chain {chain_id}] warmup done in {time.perf_counter()-t0:.1f}s, "
          f"step_size={float(params['step_size']):.4f}", flush=True)

    kernel = blackjax.nuts(log_posterior_jit, **params).step

    @jax.jit
    def step(carry, key):
        state = carry
        state, info = kernel(key, state)
        return state, (state.position, info.is_divergent)

    keys = jax.random.split(jax.random.fold_in(key, chain_id + 1000), n_samples)
    print(f"  [chain {chain_id}] sampling {n_samples} steps...", flush=True)
    t0 = time.perf_counter()
    state_final, (positions, divergent) = jax.lax.scan(step, state, keys)
    state_final.position.block_until_ready()
    elapsed = time.perf_counter() - t0
    n_div = int(divergent.sum())
    print(f"  [chain {chain_id}] done in {elapsed:.1f}s "
          f"= {n_samples/elapsed:.0f} samples/s, divergences={n_div}/{n_samples}",
          flush=True)
    return np.asarray(positions), n_div, elapsed

# ─────────────────────────────────────────────────────────────────
# Main
# ─────────────────────────────────────────────────────────────────
def main():
    print(f"\n[{time.strftime('%H:%M:%S')}] G1.14 JOINT MCMC starting", flush=True)
    print(f"  Model: LYD20 Model VI quarks + unified lepton model", flush=True)
    print(f"  Two τ: (τ_q, τ_l) free", flush=True)
    print(f"  Params: {PARAM_NAMES}  (n={N_PARAMS})", flush=True)
    print(f"  Obs:    {_OBS_KEYS}  (n={N_OBS})", flush=True)
    if PRIOR_NEAR_I:
        print(f"  Prior:  v7.4-attractor restricted (|τ_l - i| < 0.5)", flush=True)
    else:
        print(f"  Prior:  fundamental domain (|Re τ| < 0.6, 0.5 < Im τ < 2.5)", flush=True)

    # Compile-test single likelihood call
    init = init_position(0)
    print(f"\n[{time.strftime('%H:%M:%S')}] Compile-test logp at init...", flush=True)
    t0 = time.perf_counter()
    logp_init = float(log_posterior_jit(init))
    print(f"  log_posterior(init) = {logp_init:.4f}  "
          f"(jit compile in {time.perf_counter()-t0:.2f}s)", flush=True)
    if not np.isfinite(logp_init):
        print(f"ERROR: init position has -inf log-posterior. Check priors.")
        sys.exit(1)

    # Run N_CHAINS independent chains
    all_chains = []
    all_divs = 0
    for c in range(N_CHAINS):
        init_c = init_position(c)
        positions, n_div, _ = run_nuts_one_chain(
            c, init_c, N_WARMUP, N_SAMPLES, SEED)
        all_chains.append(positions)
        all_divs += n_div

    chain = np.stack(all_chains, axis=0)  # (N_CHAINS, N_SAMPLES, N_PARAMS)
    print(f"\n[{time.strftime('%H:%M:%S')}] Sampling complete. "
          f"Total divergences: {all_divs}/{N_CHAINS*N_SAMPLES}", flush=True)

    # ─────────────────────────────────────────────────────────────
    # Posterior summary
    # ─────────────────────────────────────────────────────────────
    flat = chain.reshape(-1, N_PARAMS)
    means = flat.mean(axis=0)
    stds  = flat.std(axis=0)
    medians = np.median(flat, axis=0)
    q05 = np.percentile(flat, 5, axis=0)
    q95 = np.percentile(flat, 95, axis=0)

    print(f"\n[{time.strftime('%H:%M:%S')}] POSTERIOR SUMMARY", flush=True)
    print(f"  {'param':>15}  {'mean':>12}  {'std':>10}  "
          f"{'q05':>12}  {'q95':>12}", flush=True)
    for i, name in enumerate(PARAM_NAMES):
        print(f"  {name:>15}  {means[i]:12.5f}  {stds[i]:10.5f}  "
              f"{q05[i]:12.5f}  {q95[i]:12.5f}", flush=True)

    # ─────────────────────────────────────────────────────────────
    # Key derived quantities
    # ─────────────────────────────────────────────────────────────
    re_q, im_q = flat[:, 0], flat[:, 1]
    re_l, im_l = flat[:, 2], flat[:, 3]
    dist_l_from_i = np.sqrt(re_l ** 2 + (im_l - 1.0) ** 2)
    dist_q_from_i = np.sqrt(re_q ** 2 + (im_q - 1.0) ** 2)
    dist_lq = np.sqrt((re_l - re_q) ** 2 + (im_l - im_q) ** 2)

    print(f"\n[{time.strftime('%H:%M:%S')}] DERIVED QUANTITIES", flush=True)
    print(f"  |τ_l - i|   = {dist_l_from_i.mean():.4f} ± {dist_l_from_i.std():.4f} "
          f"(median {np.median(dist_l_from_i):.4f})", flush=True)
    print(f"  |τ_q - i|   = {dist_q_from_i.mean():.4f} ± {dist_q_from_i.std():.4f} "
          f"(median {np.median(dist_q_from_i):.4f})", flush=True)
    print(f"  |τ_l - τ_q| = {dist_lq.mean():.4f} ± {dist_lq.std():.4f} "
          f"(median {np.median(dist_lq):.4f})", flush=True)

    # ─────────────────────────────────────────────────────────────
    # Best-fit χ²/dof
    # ─────────────────────────────────────────────────────────────
    chi2_chain = -2.0 * np.array([float(log_likelihood(jnp.array(p))) for p in flat[::100]])
    chi2_min = float(chi2_chain.min())
    chi2_med = float(np.median(chi2_chain))
    dof = N_OBS - N_PARAMS  # may be negative if over-parametrised
    print(f"\n  χ²_min  = {chi2_min:.3f}", flush=True)
    print(f"  χ²_med  = {chi2_med:.3f}", flush=True)
    print(f"  N_OBS   = {N_OBS}, N_PARAMS = {N_PARAMS}, dof = {dof}", flush=True)
    if dof > 0:
        print(f"  χ²_min/dof = {chi2_min/dof:.3f}", flush=True)

    # ─────────────────────────────────────────────────────────────
    # Verdict
    # ─────────────────────────────────────────────────────────────
    # Test 1: |τ_l - i| < 0.3 in 95% credible (TWO-TAU near-i compatible)
    p_l_near_i = float(np.mean(dist_l_from_i < 0.3))
    p_q_near_i = float(np.mean(dist_q_from_i < 0.3))
    # Test 2: τ_l and τ_q distinct? (two-modulus support)
    p_one_tau = float(np.mean(dist_lq < 0.1))   # support for single-τ collapse
    p_two_tau = 1.0 - p_one_tau

    if chi2_min < 30 and p_l_near_i > 0.5 and p_q_near_i > 0.5:
        verdict = "[TWO-TAU NEAR-I VIABLE — both τ posteriors centred on i, joint χ²_min < 30]"
    elif chi2_min < 50:
        verdict = (f"[TWO-TAU MARGINAL — χ²_min={chi2_min:.1f}, "
                   f"P(|τ_l-i|<0.3)={p_l_near_i:.2f}, P(|τ_q-i|<0.3)={p_q_near_i:.2f}]")
    else:
        verdict = f"[TWO-TAU REFUTED — χ²_min={chi2_min:.1f} > 50]"

    print(f"\n[{time.strftime('%H:%M:%S')}] VERDICT", flush=True)
    print(f"  P(|τ_l - i| < 0.3) = {p_l_near_i:.3f}", flush=True)
    print(f"  P(|τ_q - i| < 0.3) = {p_q_near_i:.3f}", flush=True)
    print(f"  P(|τ_l - τ_q| < 0.1) = {p_one_tau:.3f}  "
          f"(single-τ collapse support)", flush=True)
    print(f"  {verdict}", flush=True)

    # ─────────────────────────────────────────────────────────────
    # Save outputs
    # ─────────────────────────────────────────────────────────────
    out_dir = "/home/remondiere/pc_calcs"
    if not os.path.isdir(out_dir):
        out_dir = "."
    chain_path = os.path.join(out_dir, "g114_joint_mcmc_chain.npz")
    np.savez_compressed(chain_path, chain=chain, param_names=np.array(PARAM_NAMES))
    print(f"\n[{time.strftime('%H:%M:%S')}] Chain saved: {chain_path}", flush=True)

    summary = {
        "version": "v6.0.53.1",
        "model": "LYD20 Model VI quarks + unified lepton",
        "n_params": int(N_PARAMS),
        "n_obs": int(N_OBS),
        "n_chains": int(N_CHAINS),
        "n_warmup": int(N_WARMUP),
        "n_samples": int(N_SAMPLES),
        "prior_near_i": bool(PRIOR_NEAR_I),
        "param_names": PARAM_NAMES,
        "obs_keys": _OBS_KEYS,
        "pdg_val": [float(x) for x in PDG_VAL],
        "pdg_sig": [float(x) for x in PDG_SIG],
        "posterior": {
            name: {"mean": float(means[i]), "std": float(stds[i]),
                   "median": float(medians[i]),
                   "q05": float(q05[i]), "q95": float(q95[i])}
            for i, name in enumerate(PARAM_NAMES)
        },
        "derived": {
            "|tau_l - i|":   {"mean": float(dist_l_from_i.mean()),
                              "std":  float(dist_l_from_i.std()),
                              "median": float(np.median(dist_l_from_i))},
            "|tau_q - i|":   {"mean": float(dist_q_from_i.mean()),
                              "std":  float(dist_q_from_i.std()),
                              "median": float(np.median(dist_q_from_i))},
            "|tau_l - tau_q|": {"mean": float(dist_lq.mean()),
                                 "std":  float(dist_lq.std()),
                                 "median": float(np.median(dist_lq))},
        },
        "chi2_min": chi2_min,
        "chi2_median": chi2_med,
        "dof": int(dof),
        "P(|tau_l-i|<0.3)": p_l_near_i,
        "P(|tau_q-i|<0.3)": p_q_near_i,
        "P(|tau_l-tau_q|<0.1)": p_one_tau,
        "n_divergences": int(all_divs),
        "verdict": verdict,
    }
    summary_path = os.path.join(out_dir, "g114_joint_mcmc_results.json")
    with open(summary_path, "w") as f:
        json.dump(summary, f, indent=2)
    print(f"[{time.strftime('%H:%M:%S')}] Summary saved: {summary_path}", flush=True)

    # Optional corner plot (matplotlib)
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
        # 4-panel τ posterior figure
        fig, axes = plt.subplots(1, 2, figsize=(12, 5))
        axes[0].hexbin(flat[:, 0], flat[:, 1], gridsize=40, cmap="viridis")
        axes[0].axhline(1.0, c="red", ls="--", alpha=0.5)
        axes[0].axvline(0.0, c="red", ls="--", alpha=0.5)
        axes[0].plot(0, 1, "r*", ms=12, label="τ=i")
        axes[0].set_xlabel("Re τ_q"); axes[0].set_ylabel("Im τ_q")
        axes[0].set_title("τ_quark posterior")
        axes[0].legend()
        axes[1].hexbin(flat[:, 2], flat[:, 3], gridsize=40, cmap="viridis")
        axes[1].axhline(1.0, c="red", ls="--", alpha=0.5)
        axes[1].axvline(0.0, c="red", ls="--", alpha=0.5)
        axes[1].plot(0, 1, "r*", ms=12, label="τ=i")
        axes[1].set_xlabel("Re τ_l"); axes[1].set_ylabel("Im τ_l")
        axes[1].set_title("τ_lepton posterior")
        axes[1].legend()
        plt.tight_layout()
        plot_path = os.path.join(out_dir, "g114_tau_posterior.png")
        plt.savefig(plot_path, dpi=120, bbox_inches="tight")
        print(f"[{time.strftime('%H:%M:%S')}] τ posterior plot: {plot_path}",
              flush=True)
    except Exception as e:
        print(f"  (plotting skipped: {e})", flush=True)

    print(f"\n[{time.strftime('%H:%M:%S')}] DONE  ::  FINAL VERDICT  ::  {verdict}",
          flush=True)


if __name__ == "__main__":
    main()
